# R1 Derivation Budget Primitive 前置审计

> 状态：`R1_DERIVATION_BUDGET_PRIMITIVE_PRECONTRACT_AUDITED /
> R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_NOT_FROZEN /
> R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@3a1374c2e7c5861ab9746052dceb8f50a1544d3e`
>
> 上游冻结输入：[R1 Derivation Attempt 与 Fact Provenance 合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)、
> [DerivationEvidence 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)与
> [修正实现冻结发布](143-r1-derivation-evidence-schema-correction-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L0_DOCUMENTATION`；本轮只使用仓库外一次性机制探针，不创建或修改
> runtime、Provider、parser、Fact、Relation、Slice、Coverage、Manifest、CLI、Workbench、Core、P/Q/D、
> Schema、依赖、CI、tag 或 Release

## 1. 审计问题

上游合同已经要求下一步证明：

```text
one absolute monotonic deadline
pre-start process-tree memory containment
cancellation / cleanup / no residue
artifact staging hard stop
```

本轮不问 Provider 怎样产生 Fact，而问四个更早的问题：

1. sealed 上限能否真实限制执行；
2. runtime 能否可靠知道是哪一类停止触发了终止；
3. execution deadline 耗尽后，process-tree cleanup 由谁拥有预算；
4. artifact byte 上限能否在发布前兑现，而不是写完以后才检查。

原合同把其中若干局部事实写得过于接近，真实平台机制证明必须先拆开：

```text
Containment != Attribution
Execution deadline != Physical release deadline
Configured limit != Positively observed stop trigger
Late process exit != Eligible late result
```

## 2. 冻结输入没有漂移

审计开始时的关键字节为：

```text
docs/137-r1-derivation-attempt-and-fact-provenance-contract.md
SHA-256 618e4895904d675a029fae119a9470d46aa3dbc45e1530815c533206e5edb532

docs/140-r1-derivation-evidence-schema-correction-contract.md
SHA-256 5a353b77899b648406036df0c05c997ce107d0eb7bc944042ebd6f5a1f3a4629

schemas/review-policy-0.1.schema.json
SHA-256 101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f

schemas/review-derivation-evidence-0.1.1.schema.json
SHA-256 a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045
```

`ReviewPolicy.execution_budget` 继续只有 `wall_clock_ms / memory_bytes / artifact_bytes` 三个正整数；
`DerivationEvidence 0.1.1` 继续用 sealed `policy_digest` 绑定上限，并以 typed diagnostic 保存终止观察。
本审计没有发现必须新增字段或升级 Schema 的证据。

## 3. 平台合同给出的上限

当前参考宿主为 Windows 11 `10.0.26200`，Python `3.10.6 / 3.13.13`，两套环境均安装锁定的
`pywin32==312`。

微软 Win32 合同明确区分两类机制：

- `JOB_OBJECT_LIMIT_JOB_MEMORY` 是 job-wide committed-memory hard limit；超额 commit 会失败；
- Job 可以把 memory-limit event 发送到关联的 I/O completion port；
- 但除 notification-limit 类以外，普通 Job completion-port message 的投递不保证；消息未到不证明事件
  未发生；
- notification-limit message 的投递有保证，但它是通知阈值，进程仍可继续分配，不能单独替代 hard limit。

来源：

- [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information)
- [JOBOBJECT_ASSOCIATE_COMPLETION_PORT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_NOTIFICATION_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information)

因此不能从以下组合推出 memory attribution：

```text
hard limit configured
+ worker OOM / abnormal exit / non-zero exit
-> EXECUTION_MEMORY_BUDGET
```

真正有资格支持该 diagnostic 的是：

```text
positive JOB_OBJECT_MSG_JOB_MEMORY_LIMIT observation
+ that observation wins the terminal-stop latch
-> EXECUTION_MEMORY_BUDGET
```

## 4. 一次性机制探针

探针位于仓库外临时目录，不是产品实现、公共 API、CI fixture 或可发布 Artifact。它只用于攻击合同假设；
下面的观察不能替代后继可复算 conformance harness。

### 4.1 Memory containment 与正向观察

探针顺序固定为：

```text
create inactive Job
-> set/read back 64 MiB hard job-memory limit
-> associate completion port
-> create Python worker suspended
-> assign worker before resume
-> worker grows memory
-> positively receive JOB_OBJECT_MSG_JOB_MEMORY_LIMIT
-> terminate the whole Job
-> receive JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO
```

Python 3.10 与 3.13 各运行四次，共八次。八次均观察到 memory-limit message、主动终止与
`ACTIVE_PROCESS_ZERO`；3.10 的完整收口为约 `485–531 ms`，3.13 为约 `354–357 ms`。这些事实证明当前
宿主上的 containment、正向 event observation 与 whole-tree release 可以组合，但不能把八次观察外推成
Win32 未承诺的消息必达保证。

探针同时发现：pywin32 312 虽暴露相关常量，但其 `SetInformationJobObject` wrapper 不接受 completion-port
association information；Job completion message 又把 PID 放在原生 `lpOverlapped` 位置，不能把普通文件
I/O wrapper 的对象假设直接套用。一次性探针因此使用窄 ctypes Win32 surface。后继实现必须独立冻结绑定
与依赖边界，不能私自导入 Core 的 `windows_job.py`，也不能把探针代码冒充公共 capability。

### 4.2 Deadline、cancellation 与 release

第二个探针让受控 root worker 再生成后继进程，并分别在 caller cancellation 与 500 ms monotonic deadline
上停止整棵 Job。四种 runner mode 均得到 root signaled、`ACTIVE_PROCESS_ZERO` 与单一 release envelope 内
清理完成：

```text
Python 3.10 normal/-O
  cancel latch   203–219 ms
  deadline latch 500–515 ms
  post-latch release 0–16 ms

Python 3.13 normal/-O
  cancel latch   213–227 ms
  deadline latch 513–527 ms
  post-latch release 约 2–4 ms
```

500 ms threshold 不等于通用 OS 会在 500.000 ms 物理冻结进程。调度和轮询只能在截止点后的第一个控制机会
发出终止。因此 `wall_clock_ms` 必须约束结果资格与 controller stop decision：deadline 以后到达的结果不得
接纳；物理释放由另一个 bounded cleanup envelope 完成。否则“deadline 已耗尽”和“仍要清理到零残留”无法
同时兑现。

### 4.3 Artifact producer-side stop

第三个探针按将写入的 exact bytes 做包含式 reservation，再 create-new 写入 staging，全部闭合后才 rename
发布。总 payload 为 9 bytes：

```text
budget = 9 -> publish two files
budget = 8 -> reject before second file; no final directory; staging removed
budget = 1 -> reject before first file; no final directory; staging removed
```

Python 3.10/3.13、normal/`-O` 四种模式结果一致。这里应用拥有 exact bytes，因此不需要从外部平台事件推断
原因；`projected_bytes > artifact_bytes` 本身就是正向、可复算的 stop observation。

## 5. 反例裁决

### 5.1 Hard ceiling 与原因归属分离

hard memory limit 的配置/readback 证明 containment active；它不证明某次异常退出由该限制触发。
`EXECUTION_MEMORY_BUDGET` 只能表示正向 memory event 已被观察且被 controller 锁存为本次停止触发器，
不能表示操作系统或应用已经证明唯一根因。

若 message 未观察到：

```text
containment remains true
memory attribution remains unproven
EXECUTION_MEMORY_BUDGET is forbidden
```

未来 Provider phase 可以按自己的冻结映射记录 structured failure；没有该合同以前，本 primitive 不替它
发明 `PROVIDER_FAILED` 或新公共 `UNKNOWN` code。

### 5.2 Deadline 控制 acceptance，不承诺瞬时物理停止

deadline 从 admission 的单一 monotonic `t0` 计算，绝不刷新。到达 deadline 后：

- 不得启动新语义工作；
- 已返回但尚未 commit 的 candidate/result 必须重新检查 deadline；
- deadline 后到达的 worker output 不得进入 canonical Fact 或成功 phase result；
- controller 在第一个可调度控制机会请求终止。

这保留了 hard acceptance boundary，同时不编造通用 OS 不提供的瞬时暂停保证。

### 5.3 Cleanup 不是第二份 execution budget

terminal stop 锁存后可创建一次固定、非语义的 release envelope。它只允许 cancellation、Job termination、
queue drain、handle/thread close 与零残留确认；不能运行 Provider、接纳 candidate、canonicalize、stage 或
恢复成功。所有 cleanup phase 共用同一绝对 release deadline，任何 escalation 不得刷新。
正常 phase 完成不需要第二份 release 预算：它的完成资格本身就要求 result 与 phase-owned
execution resources 在 execution deadline 前一起闭合。只观察到 Provider 返回或 root process 退出
不足以先写成功，再把资源清理移到 deadline 之外。

因此：

```text
Execution permission ends at execution_deadline or earlier latched stop
Release permission ends at one cleanup release_deadline
```

### 5.4 Stop trigger 不是隐藏根因

deadline、cancellation、positive memory event 与 artifact reservation failure 可以竞态。runtime 必须通过
一个原子 latch 只选择一次 terminal stop trigger，并冻结同一 checkpoint 的 tie-break；不得根据 exit code、
OOM 字符串、接近阈值或 cleanup 结果重写已锁存原因。

## 6. 最小合同修正范围

审计结论要求对文档 137/140 做最小一致性修正：

1. 把 memory diagnostic 从“hard limit 存在/worker 异常”收窄到“positive event 赢得 stop latch”；
2. 把 `wall_clock_ms` 从不可兑现的瞬时物理停止，收窄为绝对 acceptance/stop-decision deadline；
3. 明确一次性 cleanup release envelope 不延长 derivation execution budget；
4. 明确 terminal code 是 observed/latching trigger，不是平台根因声明；
5. 保留 `ReviewPolicy 0.1` 与 `DerivationEvidence 0.1.1` 的全部公共字节和字段。

不需要增加 `configured / positively_observed` 字段：configured ceilings 已由 sealed `policy_digest` 绑定；
是否有资格写 typed diagnostic 由 runtime conformance 强制。若未来要求第三方从 Evidence 单独复核消息序列、
peak memory 或 latch chronology，必须新增版本化 measurement Artifact，不能让当前 Schema 假装已经保存。

## 7. 候选合同后的系统级俯瞰

本轮不以“多找问题”为目标，而是再次检查 budget primitive 与上下游冻结对象的组合语义。
每个观察只能进入以下一类，“被发现”不自动等于“现在必须改”：

| 类别 | 当前观察 | 裁决 |
| --- | --- | --- |
| Freeze blocker | `COMPLETED_FOR_PHASE` 曾被误画成 BudgetContext 终态，与后继 phase 共用 context 矛盾 | 已在候选中拆成 phase result 与 context lifecycle |
| Freeze blocker | normal completion check 与 terminal stop latch 之间存在竞态 | 已收窄为同一原子决策边界 |
| Implementation gate | native Job/port binding、message drain、whole-tree zero 与 cleanup envelope 需要可复算 harness | 不在 docs-only 候选选型或写代码 |
| Implementation gate | normal result 必须与 phase-owned resources 一起在 deadline 前闭合 | 新增 BP-015/016，等合同冻结后才施工 |
| Deferred contract seam | 未归因 worker exit 如何进入未来 ProviderRun/DerivationEvidence | 当前 primitive 只禁止伪造 memory cause，不替后继发明公共 code |
| Deferred contract seam | event chronology、peak memory 与 consumption 是否要成为可移植 Evidence | 当前 Schema 不声称保存；真实需求出现时再版本化 |
| Deferred platform seam | POSIX/cgroup 或第二参考宿主 | Windows-only reference 边界保持不变，不预冻结未验证等价物 |
| Observe only | R 四矩阵当前单路约需 140 秒 | 只记为验证成本事实；不改门、不开 Q、不弱化回归 |
| No change | `ReviewPolicy 0.1` 与 `DerivationEvidence 0.1.1` 字段 | 当前反例可由 warrant/conformance 闭合，不为对称性加字段 |

俯瞰没有发现第三个必须重开 Schema 或上位 R1 对象的反例。当前两个 Freeze blocker 都是候选
自身的组合缝隙，已做最小修正；其余观察保持在各自的后继权威层。

## 8. 当前停止线

本审计没有冻结合同，也没有建立可复用 budget primitive。下一步只能建立独立 docs-only 最小合同候选，
并为后继 conformance harness 固定：正向原因观测、deadline acceptance、单一 release envelope、artifact
producer-side reservation 与竞态 stop-latch 规则。

当前状态保持：

```text
R1_DERIVATION_BUDGET_PRIMITIVE_PRECONTRACT_AUDITED
R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_NOT_FROZEN
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

Provider/parser/Fact runtime、Relation、Slice、Coverage、conflict/UNKNOWN、完整 Derivation、Manifest 与真实
repo end-to-end 继续禁止。
