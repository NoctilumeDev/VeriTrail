# R1 Derivation Budget Primitive 最小合同

> 状态：`R1_DERIVATION_BUDGET_PRIMITIVE_PRECONTRACT_AUDITED /
> R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_CANDIDATE /
> R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@3a1374c2e7c5861ab9746052dceb8f50a1544d3e`
>
> 前置审计：[R1 Derivation Budget Primitive 前置审计](144-r1-derivation-budget-primitive-precontract-audit.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文只修正 budget primitive 的 authority、stop observation、
> deadline 与 cleanup 语义，不创建 runtime、Provider、parser、Fact、Relation、Slice、Coverage、Manifest、
> CLI、Workbench、Schema、依赖、CI、tag 或 Release

## 1. 目的与边界

本文只冻结下一条可实现闭环：

```text
sealed ReviewPolicy.execution_budget
        ↓
one owned BudgetContext
        ↓
absolute acceptance deadline
+ pre-start process-tree memory containment
+ positive stop observations
+ producer-side artifact reservation
        ↓
one terminal-stop latch
        ↓
one bounded release envelope
        ↓
no late accepted result / no process or staging residue
```

Budget primitive 只回答“本次 derivation 还是否拥有继续执行、接纳结果或发布 bytes 的资格”。它不生成
Fact，不解释源码，不决定 Provider applicability，不发布 DerivationEvidence/Manifest，也不输出 Verdict。

## 2. 五个身份不可压缩

```text
sealed ceiling
  ReviewPolicy 中的人类确认上限

containment mechanism
  runtime 用来限制 process tree / staged bytes 的能力

positive stop observation
  controller 真正看到的 deadline/cancel/event/reservation fact

latched stop trigger
  一次从 RUNNING -> STOPPING 的唯一胜出触发器

underlying root cause
  平台或 Provider 内部为什么走到该状态；首版通常未知
```

必须保持：

```text
Configured == true      does not imply Cause == memory
Process exited abnormally does not imply Cause == memory
Stop trigger observed    does not imply unique platform root cause
```

## 3. BudgetContext 所有权

### 3.1 单次创建

admission 在任何 Provider/parser/candidate 活动前 copy-own sealed 三维上限，并创建一次 BudgetContext：

```text
t0 = monotonic_now()
execution_deadline = t0 + wall_clock_ms
memory_ceiling = memory_bytes
artifact_ceiling = artifact_bytes
state = RUNNING
```

后继 phase 只能消费同一 context；不能序列化后重建、按阶段刷新或把 retry 当成同一 attempt。充分预算不同
时，canonical Source/Fact bytes 与 identity 仍必须相同。

### 3.2 状态机

BudgetContext 自身只表达整个 attempt 的共享执行资格：

```text
ADMITTED
   ↓
RUNNING
   └─ positive stop observation wins one atomic latch
          ↓
       STOPPING
          ↓ cleanup only
       RELEASED | RELEASE_FAILED
```

`COMPLETED_FOR_PHASE` 是 phase result，不是 BudgetContext 状态。它不终止、重建或刷新 context，
也不是完整 R1 Derivation COMPLETE，不授权发布 FactSet、Evidence 或 Manifest。后继 phase
仍消费同一个 `RUNNING` context 的剩余 deadline/counters。

该 phase result 只能在 result 已通过当前 commit check，且该 phase 拥有的 worker/process
tree、observation thread/channel 与 handles 已在 execution deadline 前闭合时产生。Provider
callable 返回、worker 输出已到达或 root process 单独退出都不充分。若 normal result 已到达
但 phase-owned 资源在 deadline 前未闭合，不得先写 `COMPLETED_FOR_PHASE`；deadline 在后续
checkpoint 仍可获得 stop latch，并转入唯一 cleanup-only release envelope。

phase completion commit 与 terminal stop latch 必须共享同一个原子决策边界。completion checkpoint 先形成
已观察 stop 集合并读取 monotonic now；只有在无 stop、未超 deadline、资源已闭合且
context 仍为 `RUNNING` 时，才可原子提交 `COMPLETED_FOR_PHASE`。若并发 stop 已抢先使 context
进入 `STOPPING`，phase completion 必须失败；反之，已提交的 phase result 不给该 phase 之后到达的
event 以追溯改写权，但 context 未终止，后继 phase 仍须继续检查它。

## 4. Absolute deadline 是结果资格边界

`execution_deadline` 从 admission 的单一 monotonic `t0` 计算，不受 UTC、系统时钟、Provider start、phase
切换、retry、force termination 或 cleanup 影响。

通用 OS 不能保证在 deadline 对应的物理瞬间冻结全部进程。因此首版准确承诺为：

1. controller 在 deadline 后第一个控制机会尝试锁存 `EXECUTION_DEADLINE` 并停止 execution cell；
2. 每个 candidate acceptance、canonical commit、phase completion 与 artifact reservation 前都重新检查
   deadline；
3. `completed_at_monotonic > execution_deadline` 的 late output 一律没有成功资格；
4. deadline 后不得启动新 Provider、parser、canonicalization、Relation/Slice/Coverage 或 staging 工作；
5. normal phase completion 还必须证明该 phase 拥有的 execution resources 已闭合；不得把后续
   resource release 移出 deadline 后再补写成功；
6. 轮询/调度延迟不增加可接受 execution time，也不能被写成新的相对 timeout。

因此：

```text
deadline reached
-> no successful result can cross the commit boundary
-> physical tree release follows under the cleanup-only envelope
```

## 5. Memory containment 与 attribution

### 5.1 Pre-start hard containment

Windows reference primitive 必须按以下安全顺序建立：

```text
create inactive Job
-> set exact job-wide hard memory ceiling + KILL_ON_JOB_CLOSE
-> read back required limits
-> associate observation channel while Job is inactive
-> create worker suspended
-> assign worker to Job
-> resume worker
```

任何一步失败都发生在受控 execution 获得运行权以前。不能降级为普通 `Popen`、PID/name 轮询、Provider
自报、采样 RSS 或 post-hoc peak 检查。child/descendant 不得拥有 silent/breakaway 逃逸权。

### 5.2 Positive observation warrant

`EXECUTION_MEMORY_BUDGET` 的 warrant 固定为：

```text
positive platform memory-limit event observed
AND event refers to the owned Job/process tree
AND memory trigger wins the terminal-stop latch
```

以下均不充分：

```text
hard limit configured only
worker MemoryError / OOM text
non-zero or abnormal exit code
peak/accounting value near the ceiling
missing completion-port message
```

message 未到时，hard containment 仍然成立，但 memory attribution 不成立。primitive 必须保留内部
`MEMORY_ATTRIBUTION_NOT_OBSERVED` 状态或等价不可成功判断，且禁止构造
`EXECUTION_MEMORY_BUDGET`。该内部状态不是新公共 Schema code；未来 Provider phase 怎样映射未归因退出，
必须另由其合同冻结。

worker 看似先退出时，controller 必须先做一次 bounded、non-blocking observation-channel drain，再决定没有
memory event；但 drain 仍不能把平台未承诺的 message 变成必达。

### 5.3 当前 Schema 的含义

sealed hard ceiling 由 `policy_digest` 绑定；typed diagnostic 只表示 positive/latching stop trigger。现有
`DerivationEvidence 0.1.1` 不保存 event sequence、peak memory、poll interval 或 root-cause proof，本文不
增加这些字段。

## 6. Cancellation、竞态与唯一 latch

所有 terminal observations 进入同一个 controller；从 `RUNNING` 到 `STOPPING` 只能原子成功一次。一个
control checkpoint 必须先形成已观察集合，再按以下固定 rank 选择：

```text
1. EXECUTION_DEADLINE
2. EXECUTION_CANCELLED
3. EXECUTION_MEMORY_BUDGET
4. EXECUTION_ARTIFACT_BUDGET
```

deadline 排第一，因为其绝对 monotonic 边界可复算；deadline 已过时，没有其他结果仍有成功资格。
caller cancellation 是第二个显式 authority。memory 必须先有 positive platform event。artifact 是同步
reservation 失败，并且 reservation 前必须先执行 deadline/cancel/memory checkpoint。

这个 rank 只决定同一 checkpoint 的 stop-trigger 表达，不声称知道平台事件的隐藏因果先后。latch 成功后：

- 只保留胜出的 terminal budget/cancellation diagnostic；
- 后到的事件不能重写或升级原因；
- exit code、异常文本与 cleanup 结果不能反推原因；
- pure single-variable memory/artifact specimens 继续满足文档 140 的 exactly-one diagnostic 规则。

normal phase completion 的原子 commit 与该 stop latch 互斥；不允许两者在同一 phase 都声称成功。
这个互斥不把 phase completion 变成 BudgetContext 终态，只守住本 phase 的 result commit。

## 7. Cleanup release envelope

execution permission 与 cleanup permission 必须分开。terminal latch 成功时，runtime 只创建一次：

```text
release_deadline = latch_monotonic + 5_000 ms
```

`5_000 ms` 是当前 reference primitive 的 cleanup-only runtime constant，不进入 `ReviewPolicy`、Fact identity、
Policy digest 或 Artifact content。所有动作只消费同一 release deadline 的剩余量：

```text
signal cancellation
terminate owned Job if needed
drain observation channel
wait for ACTIVE_PROCESS_ZERO / equivalent tree-zero fact
close worker/job/port/pipe/thread handles
delete owned staging
confirm zero residue
```

禁止：

```text
graceful close -> new 5 s
force kill     -> another 5 s
thread join    -> another 5 s
staging delete -> another 5 s
```

release envelope 内不能继续语义工作、接纳 late candidate、恢复 `COMPLETED` 或发布正常 Artifact。
`finished_at` 可以晚于 execution deadline，因为它记录终态与 cleanup 完成后的 UTC provenance；这不代表
deadline 后仍有执行权。

若 release deadline 到达仍有 owned process/thread/handle/staging residue，primitive 为
`RELEASE_FAILED`，conformance gate 必须失败；不得用原 stop diagnostic 冒充 cleanup 已成功，也不得发布
正常 FactSet/DerivationEvidence/Manifest。

## 8. Artifact byte primitive

Artifact budget 使用 application-owned exact bytes，不依赖文件系统事后 size 猜测：

```text
projected = reserved_regular_file_bytes + len(exact_bytes)

projected <= artifact_bytes
    -> reserve atomically
    -> create-new write inside owned staging

projected > artifact_bytes
    -> latch EXECUTION_ARTIFACT_BUDGET
    -> do not open/create the next target
    -> cleanup staging under the shared release envelope
```

边界是 inclusive：恰好等于 ceiling 合法。计数对象继续沿用文档 137：完整 derivation staging 内全部
regular-file bytes，包括被复制的三份输入 Artifact、派生 Artifact 与 Manifest；目录项、外部日志、临时
内存与文件系统 allocation unit 不计入。只有完整 file set 验证闭合后才可从 staging create-new 发布最终
目录；部分文件、`.tmp` 或失败目录没有 Bundle/Manifest authority。

## 9. 平台与包边界

审计只证明当前 Windows 参考宿主存在可组合的原生 primitive，不冻结生产 binding。后继实现必须：

- 以 Review Attention 自己的公开/内部稳定边界拥有 budget capability；
- 不 import `veritrail.windows_job` 私有函数，不让 R 依赖 Core implementation identity；
- 对 native binding、锁定依赖、wheel extra 与 base-import 行为另做 package-boundary 证明；
- 缺少可靠 containment 或 observation surface 时在 admission 前 fail closed；
- 不把 ctypes 探针、ambient global install 或当前机器偶然状态写成通用 capability。

`pywin32==312` 的现有 wrapper 缺口是实现审查点，不授权本合同选择 ctypes、修改 Core M9 backend 或增加
依赖。绑定选择必须在 implementation candidate 中显式列出消费者、版本和 clean-install 证据。

## 10. 后继最小 conformance matrix

合同冻结以后，只允许建立不含真实 Provider/parser 的 deterministic helper lab，至少证明：

| ID | 单变量场景 | 必须证明 |
| --- | --- | --- |
| BP-001 | sufficient budget | result 与 phase-owned resources 均在 deadline 前闭合；不发布 R1 Artifact |
| BP-002 | 绝对 deadline | late result 被拒绝；`EXECUTION_DEADLINE`；tree zero |
| BP-003 | caller cancellation | `EXECUTION_CANCELLED`；tree zero |
| BP-004 | hard memory event observed | memory diagnostic 有正向 event warrant；tree zero |
| BP-005 | hard limit active but event absent | 禁止 memory diagnostic；不猜原因 |
| BP-006 | memory/cancel/deadline 同 checkpoint | fixed rank；只锁存一次 |
| BP-007 | artifact bytes exactly equal | reservation 与 staging 成功 |
| BP-008 | artifact bytes exceed by one | next target 写前停止；无 final/staging residue |
| BP-009 | execution deadline 后 cleanup | cleanup 可完成，但 late result 永不恢复成功 |
| BP-010 | cleanup phase escalation | 全部共享同一 release deadline，不刷新 |
| BP-011 | process creates descendants | assignment before resume；最终 whole tree zero |
| BP-012 | two sufficient budget values | canonical helper output bytes 相同 |
| BP-013 | Python 3.10/3.13 normal/`-O` | deterministic cases 同义，真实机制均闭合 |
| BP-014 | base install lacks optional capability | 基础 import 不崩；使用 capability 时 typed unavailable |
| BP-015 | result 先到，phase resource 超过 deadline 才归零 | 禁止 `COMPLETED_FOR_PHASE`；deadline stop 与 release envelope 闭合 |
| BP-016 | stop 在 completion check 与 commit 之间并发到达 | 同一原子决策边界；stop 与 phase success 最多一个成立 |

真实 memory message 正例不能证明 delivery guarantee；BP-005 必须用可控 observation backend/fake event
source 单变量证明“不观察就不归因”。fake 只证明决策逻辑，不能替代 BP-004/011 的真实 Windows Job。

## 11. 发布物与非目标

budget primitive implementation 最多产生内存中的 owned result 与测试诊断，不产生：

```text
Fact / FactSet
DerivationEvidence Artifact
RelationSet / ReviewSliceSet / CoverageLedger
COMPLETE / DIAGNOSTIC Manifest
ReviewBundle / AttentionProposal / HumanDisposition
Core Verdict
```

Provider binding、真实 Python parser、candidate-to-Fact canonicalization、完整 derivation staging、CLI、
Workbench、R2–R6、Q、D、JPyxis 与 AI Execution OS 均不属于本合同。

## 12. 候选冻结与后继授权

本文只有完成以下事实才有资格被冻结：

1. 文档 144 的 counterexample、平台合同与 probe 观察均有唯一裁决；
2. 文档 137/140 的 residual wording 已做最小一致性修正；
3. `ReviewPolicy 0.1`、`DerivationEvidence 0.1.1`、旧 corpus/vector 字节不变；
4. diff 仍为 docs-only，没有 runtime/test/dependency/CI 施工；
5. 本地 docs/static gate 与完整现有回归成立；
6. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
7. 新 exact main Public CI、Browser Smoke 与 fresh anonymous exact-SHA 产品读回成立；
8. 后继独立 docs-only 状态发布完成最后门。

候选阶段只能写：

```text
R1_DERIVATION_BUDGET_PRIMITIVE_PRECONTRACT_AUDITED
R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_CANDIDATE
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

候选合入不等于实现已获授权。只有独立冻结发布成立后，才可从新的 exact main 建立 BP-001..016
conformance harness 与最小 budget primitive；Provider/parser/Fact 仍须等待该实现自身冻结及后继明确授权。
