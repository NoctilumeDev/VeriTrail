# R1 Derivation Budget Primitive 实现冻结候选

> 候选记录状态：`R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTED /
> R1_DERIVATION_BUDGET_PRIMITIVE_FREEZE_CANDIDATE /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`4c4d81bfeed7bea9d159a58bb91097f8d98fb0c8`
>
> 主实现提交：`998b6ef52665bcafc0e7f9b6b8f2cbc0bedb2341`
>
> 测试隔离修正：`b23488e7f12b719c6fc331af31ff9bb9032659ca`
>
> 受保护主线实现基线：`8f8af815d1a566bbf35096e318d209bdc17bf7b3`
>
> 主线 Tree：`c871fba70982670b49a15487a8aa34ffe9107dd1`
>
> 实际影响层级：`L1_COMPONENT_INTERNAL + BOUNDED_L2_PUBLIC_API + L3_SYSTEM`

## 1. 当前裁决

文档 145/146 冻结的 Derivation Budget Primitive 与 `BP-001..016` 已经实现并合入受保护主线。实现建立
独立 Review Attention 包、共享绝对 monotonic deadline、单次 terminal-stop latch、精确 artifact reservation、
Windows Job memory containment、正向 memory-limit event attribution，以及 terminal stop 后一次性共享的
cleanup-only release envelope。

本实现没有创建 Provider、parser、CodeFact、FactSet、DerivationEvidence runtime publication、Relation、
Slice、Coverage、完整 Derivation Manifest、CLI 或 Workbench 能力，也没有修改 Core Verdict。本文只是
docs-only implementation freeze candidate；它自己的门禁、主线合入和 exact-main 读回尚未发生，因此当前
不得写成 `R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN`，也不解除 provenance runtime 的实现停止线。

## 2. 包与依赖边界

实现新增独立包：

```text
plugins/review-attention/
  pyproject.toml
  src/veritrail_review/
    __init__.py
    budget.py
    errors.py
    _artifact_budget.py
    _windows_budget.py
```

边界保持如下：

- base package 无运行时依赖，导入 `veritrail_review` 不导入 `pywin32`；
- Windows primitive 只在显式调用时 lazy import，并要求 exact `pywin32==312`；
- 可选能力坐标是 `budget-windows` extra，缺失或版本不符时 typed fail-closed，不回退到 `ctypes`、普通
  `Popen`、PID/进程名轮询或软内存采样；
- CI 只在需要验证 Windows primitive 的环境显式安装该 extra；
- 顶层公共 API 暴露冻结的 budget 操作与 typed errors，但内部 `ExecutionBudgetLimits` 和
  `MemoryAttributionState` 不成为公共 API；
- 包没有依赖 GitHub Evidence、Core 私有 API、Q、D、JPyxis 或未来 AI Execution OS。

## 3. 运行与权威边界

### 3.1 Shared BudgetContext

`BudgetContext` 在 sealed limits admission 后建立一个绝对 deadline。所有检查只消费同一时间坐标；暂停、
重试、phase 切换和 cleanup 不能刷新 acceptance budget。terminal-stop latch 是一次性、原子的，已经停止的
上下文不能被较晚 observation 改写原因。

normal result 只有在 deadline 内同时满足以下条件时才有资格完成：

```text
result closure
+ all phase-owned resource closure
+ no terminal stop won the race
```

`COMPLETED_FOR_PHASE` 只是 phase result，不是 `BudgetContext` terminal state。上下文只有完整 controller
确认它所知的全部 owned resources 都已释放后，才能进入全局 `RELEASED`。

### 3.2 Memory containment and attribution

Windows worker 通过 suspended-create、assign-to-owned-Job、resume 的顺序进入 hard Job memory ceiling，
避免工作负载先于 containment 执行。Job completion port 的正向 memory-limit event 是
`EXECUTION_MEMORY_BUDGET` 的唯一授权来源；OOM、异常退出、exit code、接近上限或“已经配置 hard limit”
均不能反推该原因。

收到正向事件后，primitive 赢取 terminal-stop latch、终止 owned Job tree，并在同一 release envelope 内等待
`ACTIVE_PROCESS_ZERO`。如果平台没有提供正向原因事件，系统可以记录 containment 已配置和进程终止事实，
但必须把 terminal cause 保持为 UNKNOWN/其他已正向观察到的原因，不能猜测内存归因。

### 3.3 Artifact reservation and publication

artifact budget 使用 inclusive producer-side reservation：`current + requested <= limit` 才允许写入。每次写入
进入 create-new owned staging；完整写入和摘要验证以前不暴露 final artifact，超限或失败会清理该 staging。
因此：

```text
produced bytes != published artifact
reservation success != global context release
```

## 4. `BP-001..016` conformance

| 向量 | 已实现的单变量义务 |
| --- | --- |
| BP-001 | sufficient budget 下 result 与 phase-owned resources 在 deadline 前闭合；不发布 R1 Artifact |
| BP-002 | absolute deadline 拒绝 late result，锁存 `EXECUTION_DEADLINE` 并使 tree zero |
| BP-003 | caller cancellation 锁存 `EXECUTION_CANCELLED` 并使 tree zero |
| BP-004 | 真实 hard-memory event 为 memory diagnostic 提供正向 warrant，并使 tree zero |
| BP-005 | hard limit active 但 event absent 时禁止 memory attribution，不猜原因 |
| BP-006 | memory/cancel/deadline 同 checkpoint 时按 fixed rank 只锁存一次 |
| BP-007 | artifact bytes 刚好等于上限时 reservation 与 staging 成功 |
| BP-008 | artifact bytes 超限一个 byte 时在下一目标写前停止，且无 final/staging residue |
| BP-009 | execution deadline 后 cleanup 可完成，但 late result 永不恢复成功 |
| BP-010 | cleanup phase escalation 全部共享同一 release deadline，不刷新 |
| BP-011 | worker 创建 descendants 时 assignment-before-resume，最终 whole tree zero |
| BP-012 | 两个充分但不同的 budget values 生成相同 canonical helper output bytes |
| BP-013 | Python 3.10/3.13 normal/`-O` 下 deterministic cases 同义且真实机制闭合 |
| BP-014 | base wheel 在无 `pywin32` 环境仍可导入并 typed unavailable |
| BP-015 | result 先到但 phase resource 超过 deadline 才归零时禁止 `COMPLETED_FOR_PHASE`，并闭合 stop/release |
| BP-016 | stop 在 completion check 与 commit 之间并发到达时，只允许 stop/phase success 一个成立 |

以上表格是合同义务索引，不新增 Schema 或把测试名称变成新的产品语义。

## 5. 实现后系统审计

实现完成后没有按 finding 数量凑审计 KPI，而是重新画 ownership、execution eligibility 与 publication 的组合
边界。两项真实接缝在 PR 前被修正：

1. **local cleanup 不等于 global release**：早期 artifact staging 和 Windows process cell 能依据自己的局部
   residue 把整个 `BudgetContext` 标成 `RELEASED`。修正后 local backend 只报告自身清理结果，只有拥有完整
   resource view 的 controller 可以调用全局 release transition；
2. **`RUNNING` 枚举不等于当前仍有执行资格**：早期 process cell 在 absolute deadline 已经过期、但尚无
   checkpoint 改写状态时仍可能 resume worker。现在 worker create 前与 resume 前均检查同一 deadline；真实
   Windows 反例证明 expired context 不再授予执行权。

另有一项公共边界修正：内部 memory attribution state 曾被顶层 `__all__` 暴露，最终候选删除该导出，只保留
冻结合同需要的公共能力。

审计同时保留两个后继接缝，但没有越权替未来 Provider/full Derivation 作决定：

- platform primitive 抛出异常以后，未来 Provider attempt 必须拥有 context discard/invalidation；当前 primitive
  不为未知异常伪造 terminal cause；
- 任意文件系统删除并非天然可抢占。当前 helper 可以拒绝宣称 timely release；未来 publication/Provider 合同
  必须拥有 storage topology 与 cleanup semantics。

它们是显式延期问题，不是本候选已解决能力，也不阻断当前 primitive 已冻结义务的真实性。

## 6. 本地实现证据

最终候选的 Review Attention 定向 budget/boundary 检查为 `27/27`。完整 Review Attention 四矩阵曾在最后一个
公共导出收窄前达到：

| 门 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| Review Attention normal / `-O` | `83/83` / `83/83` | `83/83` / `83/83` |

最后 delta 只删除内部 enum 的顶层导出，并由最终 `27/27` budget/boundary tests 覆盖；最终 head 的全仓矩阵
由后述 PR 新 head 原始 Public CI 建立。其余本地串行回归为：

| 门 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| Core normal / `-O` | `446/446` / `446/446` | `446/446` / `446/446` |
| GitHub Evidence normal / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| Authoring Skill normal / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |

Workbench 为 `173/173`，lint、build 与使用官方 npm registry 的 audit 均通过，audit 为 0 vulnerability。第一次
Workbench 本地检查暴露 worktree 尚无 `node_modules`，随后一次镜像 registry audit 又因镜像不提供 audit API
失败；它们均属于本地依赖/registry provenance，不是产品通过事实，也没有通过修改仓库或全局 npm 配置掩盖。
从 official registry 执行 clean `npm ci` 后才建立最终前端证据。

独立 clean venv 安装 `.[budget-windows]` 后读到 package `0.1.0.dev0`、`pywin32 312` 与正确 extra metadata，
Windows capability 为 `AVAILABLE`。base-wheel 负向环境不安装 `pywin32`，仍可导入包，并在请求 Windows
capability 时得到 typed unavailable。`compileall`、`git diff --check`、trailing-whitespace 与敏感模式扫描均通过。

## 7. 首次远端红灯与测试模型修正

PR #126 第一个 head 为 `998b6ef52665bcafc0e7f9b6b8f2cbc0bedb2341`。原始
[Public CI run 34746174728](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34746174728) 中 Workbench、
E3 与无关门通过，但 Python 3.10/3.13 都只在 BP-014 失败，后继七项依赖门按工作流停止。失败没有 rerun。

BP-014 的测试用 `pip wheel --no-build-isolation` 构建 base wheel，因而错误假设调用者 ambient environment 已
安装 `setuptools.build_meta`。这不是 base package 偷依赖 `pywin32`，而是测试没有真正建立 pyproject 声明的
隔离构建世界。修正提交 `b23488e7f12b719c6fc331af31ff9bb9032659ca` 删除该假设，让 `pip wheel` 使用
isolated build environment，并在失败时保留 stdout/stderr。

修正后的 BP-014 在 CPython 3.10/3.13 × normal/`-O` 四格本地通过。PR 没有重跑旧 head，而是在新 head
`b23488e7f12b719c6fc331af31ff9bb9032659ca` 上建立新的
[Public CI run 34746649307](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34746649307)，attempt 1 为
11/11 success，全部七项下游门实际运行并通过。

## 8. 受保护主线与 exact-main 门

1. [PR #126](https://github.com/NoctilumeDev/VeriTrail/pull/126) base 为冻结合同基线
   `4c4d81bfeed7bea9d159a58bb91097f8d98fb0c8`，最终 head 为测试修正提交
   `b23488e7f12b719c6fc331af31ff9bb9032659ca`；
2. PR 以 merge commit `8f8af815d1a566bbf35096e318d209bdc17bf7b3` 合入受保护 `main`；
3. merge parents 为 `4c4d81bfeed7bea9d159a58bb91097f8d98fb0c8` 与
   `b23488e7f12b719c6fc331af31ff9bb9032659ca`，merge tree 为
   `c871fba70982670b49a15487a8aa34ffe9107dd1`；
4. exact-main [Public CI run 34747270706](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34747270706)
   为 attempt 1、11/11 success；
5. exact-main [Browser Smoke run 34747270771](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34747270771)
   为 attempt 1、1/1 success。

这些事实证明 final implementation head 与仓库完整门禁共同成立；它们不证明本文 docs-only candidate 已通过
自己的门，也不把 Windows primitive 外推为 Linux/macOS 或恶意代码隔离。

## 9. 匿名 exact-SHA 字节读回

在没有 GitHub token 的 fresh 请求中，从 `raw.githubusercontent.com` 的 exact merge commit 读取四项实现
坐标。四项均为 HTTP 200，最终 URL 保持 exact path，远端 bytes 与 merge tree 相等：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `plugins/review-attention/pyproject.toml` | 478 | `999b6fefed2884bef4cbd65a528b480597fef4434a7925a52d741d25d49363ae` |
| `plugins/review-attention/src/veritrail_review/budget.py` | 12359 | `df20e3cd8a5299146ad2128c468afcc6057747540ea640ee96232f4957231b6b` |
| `plugins/review-attention/src/veritrail_review/_windows_budget.py` | 13643 | `c452552f478ce24ff2403715faf2d45f374de31a6adc74beb4b174666ff0277b` |
| `plugins/review-attention/tests/test_budget_primitive.py` | 22571 | `440a6d303449dd4065fa72a0b5d1a8edd079b89a9fedd467cc3157f1650c7ba4` |

该读回只证明公开 exact bytes 可取得且与 Git tree 相同，不把 raw transport success 提升为 correctness；合同、
实现审计、conformance 和完整门禁共同承担后者。

## 10. 停止线与下一门

本候选继续禁止：

- Provider、parser、CodeFact、FactSet 或 DerivationEvidence runtime publication；
- Relation、conflict/UNKNOWN 传播、Slice、Coverage 或完整 Derivation Manifest；
- CLI、Workbench、Core handoff、Q scheduling/cache、D product shell、JPyxis 或 AI Execution OS 工作；
- tag、Release、Linux/macOS、容器、分布式、多租户或恶意代码沙箱声明；
- 以本 primitive 的 hard containment 冒充完整 attribution、Provider failure policy 或 storage cleanup policy。

本文与三处入口索引完成后，Budget + Boundary 定向门在 CPython 3.10 / 3.13 的 normal 与 `-O` 四种模式下
均为 `27/27`。这只证明 docs-only candidate 没有破坏当前 budget contract、public boundary 与实现停止线；
完整仓库、发布下载和浏览器事实仍必须由本文自己的远端 required checks 建立。

本文必须继续满足：

```text
docs-only candidate 原始 required checks 全部成功
    -> exact candidate 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README、本文与 milestones
    -> 后继独立最终状态发布
    -> R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN
```

任何新反例仍可否决冻结。最终状态发布以前，唯一下一步是完成本文自己的证据闭环；不得提前开始
Derivation provenance runtime，更不得越级进入 Relation、Slice、Coverage 或完整 Derivation。
