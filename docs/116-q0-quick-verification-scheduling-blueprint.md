# Q0 Quick Verification Scheduling Plugin 蓝图 0.1

> 状态：`Q0_BLUEPRINT_CANDIDATE / Q_IMPLEMENTATION_NOT_STARTED`
>
> 精确起草基线：`main@5807c53e87ea385d7a1c9de2bc32a64faeafc00e`
>
> 影响层级：`L3_SYSTEM / DOCUMENTATION_ONLY / NO_RUNTIME_CHANGE`
>
> 口号：**Prove no less. Repeat no more. / 验证不减，重复不做。**

## 1. 名称与当前停止线

顶层 `Q` 轨中的 `Q = Quick`。它不表示 `Quality`、`Qualification` 或单纯的 `Queue`：

- `Quality` 会误导读者认为 Q 拥有质量真值或 Verdict；
- `Qualification` 会与 Core 的充分性和裁决权重叠；
- `Queue` 只覆盖排队，容纳不了 Evidence 身份复用、影响证明与确定性汇合；
- `Quick` 只描述减少重复计算和无谓串行的优化目标，不授予降低证明标准的权力。

正式能力名为 **Verification Scheduling Plugin**。`Quick` 不是性能 SLO，也不承诺所有变更都更快：

> **Quick means reducing redundant work, not weakening verification.**

Q0 只冻结候选插件的身份、权威、分层、反例、实现前置门和拒绝边界。本文不创建 Schema、源码包、
CLI、CI、缓存、调度器、执行 Lane、标签、Release 或空插件目录；也不修改任何现有 workflow。

Q0 不预编 `Q1–Qn`。蓝图即使最终冻结，也只会形成：

```text
Q0_BLUEPRINT_FROZEN
Q_IMPLEMENTATION_NOT_STARTED
NO_GATE_SKIP_AUTHORITY
```

它不会自动授予下一阶段施工权。

## 2. 为什么独立开 Q 轨

VeriTrail 现有能力分别回答不同问题：

| 能力 | 回答的问题 | 优化目标 | 不拥有 |
| --- | --- | --- | --- |
| P / Platform Evidence | 去外部平台哪里、怎样取得有界事实 | Observation correctness | Verdict、审查排序 |
| R / Review Attention | 人应该优先看哪里 | Human attention | Gate 调度、缺陷真值、Verdict |
| Q / Verification Scheduling | 已声明的证明义务怎样避免无效重复并有界执行 | Verification wall-clock / recompute | Gate 定义、Evidence 语义、Verdict |
| Core | 给定 sealed Plan 与 Evidence，证据是否充分、规则得到什么结论 | Judgment discipline | 调度、平台观察、世界真相 |

因此：

```text
Attention Optimization != Verification Optimization
Scheduling != Judgment
Evidence Reuse != Evidence Sufficiency
Parallel Execution != Parallel Authority
```

Q 不能塞进 R。否则 R 会从“帮助人理解代码”膨胀为缓存、CI 调度和运行编排器；Q 也不能进入 Core，
否则 Core 会同时拥有“选择哪些证据被生产”和“判断证据是否充分”的循环权威。

这也是一条**语义解耦**规则，而不只是目录拆分：

```text
Dependency != Ownership
Consumption != Succession
Composition != Integration
```

R 的 Artifact 即使未来被 Q 消费，也不表示 Q 是 R 的后继阶段、两者共享状态机，或 R 必须按 Q 的发布
节奏演进。不同含义应拥有不同身份；相同进程、相同仓库或相同开发者也不能把语义、生命周期和权威
自动合并。

这些边界来自真实反例，但“被反例逼出来”不等于必须永久保留。只有某个分离仍拥有独立的 authority、
lifecycle、Artifact identity、failure mode 或 evolution pressure，才有资格继续作为单独边界；若这些差异
消失，它就只是历史脚手架，应允许在不丢失语义的前提下收敛。Q0 冻结的是当前仍成立的差异，不把字母
数量本身当成架构质量。

## 3. 当前真实触发与证据上限

仓库已经多次观察到：即使是 documentation/status-only 变更，为守住公共冻结纪律，仍会执行完整远端
门禁、构建、双 Python、wheel、真实浏览器或发布资产读回。PR #90 的 R1 合同冻结状态发布就是一个
公开、精确的近期样本：其合并后 Public CI 仍完整执行 11 项 Job，Browser Smoke 也独立运行。

这些事实只证明：

```text
current verification path has measurable recomputation and serial/queue cost
```

它们不证明：

```text
docs-only is always safe to skip
all existing jobs are redundant
parallel execution is safe
cached PASS remains valid
Q will necessarily reduce every wall-clock
```

Q 的出现是一个已经可观察的问题方向，不是已经完成的性能结论。没有精确依赖闭包和证明义务身份时，
当前完整门禁仍是正确的 fail-closed 基线。

## 4. 权威地图

```text
Human / sealed policy
    owns goals, proof obligations, allowed reuse policy and authorization

AcceptancePlan / Gate Contract
    owns what Evidence is required and what counts as satisfaction

Change / Dependency Providers
    report exact change facts and declared gate-input relations

Q Plugin
    derives an auditable VerificationSchedule from those frozen inputs
    may bind reusable Evidence candidates and arrange authorized lanes

Gate / Collector / Runner
    produces new Evidence and execution facts

Core
    validates exact Evidence bindings, sufficiency, integrity and Verdict

Reality
    owns truth and can still produce a new counterexample
```

Q 可以：

```text
schedule
bind an existing Evidence candidate
plan bounded isolated lanes
join execution results deterministically
explain why a gate must run or why a prior artifact is a reuse candidate
```

Q 不可以：

```text
PASS
declare SAFE_TO_SKIP
weaken or rewrite a Gate
invent missing dependency facts
change Evidence meaning
turn old green CI into current truth
override Core, Human Seal or a fresh external-observation requirement
```

Q 不复制 AcceptancePlan 的期望值。它只消费已封存的证明义务并生成执行安排；`VerificationSchedule`
不是第二份验收计划。

## 5. 候选分层

```text
Exact ChangeSet / deterministic change facts
                  |
Frozen Gate Dependency Model
                  |
Available Evidence Index + execution/resource profile
                  v
         Verification Scheduling Plugin
        +--------------------------------+
        | Impact Planner                 |
        | Evidence Reuse Planner         |
        | Isolated Lane Scheduler        |
        | Deterministic Join             |
        +--------------------------------+
                  |
                  v
        VerificationSchedule
        + Evidence references
        + lane/join provenance
                  |
                  v
            Gate execution
                  |
                  v
                Core
```

四块可以位于同一个高内聚插件进程中，不拆成四个微服务。分层要求的是版本化 Artifact 和单向依赖，
不是部署碎片化。

未来可替换 Provider 只能通过稳定合同接入。Q 内核若存在，只应拥有合同校验、身份、生命周期、manifest
和 capability discovery；依赖分析器、缓存后端、Lane runner、资源策略和展示层都属于可替换能力。

## 6. 输入身份：文件名和提交 SHA 都不够

Q 不能使用：

```text
changed_files = docs/foo.md
    -> docs-only
    -> skip Core
```

文件后缀、目录名、提交信息和 PR 标签都不是影响证明。最低限度需要把一个 Gate 的输入世界区分为：

```text
Gate Contract Identity
Subject Coordinate and Content Closure
Workflow / Gate Implementation Identity
Toolchain and Dependency Identity
Fixture / Schema / Configuration Identity
Environment and Capability Profile
Credential / Trust-domain Policy Identity (never secret values)
Freshness / Observation-window Requirement
```

可以概念化为：

```text
GateInputIdentity =
    frozen gate semantics
    + exact transitive input closure
    + execution profile
    + observation policy
```

Q0 不冻结字段名、canonical bytes 或兼容算法。首个未来证明切片只允许 exact identity；版本兼容、
语义等价或“该变化肯定无关”的推断必须另有冻结规则，不能由实现便利偷偷放宽。

若依赖闭包未知、不完整、冲突或包含无法证明的动态输入，Q 必须安排完整执行，或在完整执行不可用时
保留 `BLOCKED / UNKNOWN`；不能把未知改写成可复用。

## 7. Evidence 复用不是普通缓存

“之前绿过”不是可复用事实。候选复用对象至少需要绑定：

```text
Evidence identity and immutable bytes
exact subject / input-closure identity
Gate contract identity
producer / collector identity
toolchain and environment profile
production time and provenance
freshness and invalidation facts
Evidence format / normalization semantics
```

因此：

```text
Cache Hit != PASS
Cache Hit != Sufficient Evidence
Same Fact != Same Evidence
Same Commit != Same Observation
```

Q 输出的是 **Evidence reuse binding candidate**。Core 仍需按 sealed AcceptancePlan 校验该 Evidence 的
role、identity、sufficiency、integrity 和 assertions。

外部开放世界尤其不能只靠 exact source SHA 复用。例如 exact commit 固定的是 Markdown 源坐标，GitHub
公共渲染仍可能随平台 renderer 和观察时间变化；如果 Plan 要求 fresh public readback，旧 Render
Evidence 即使指向同一 commit 也不能替代新观察。P 轨的 freshness、匿名、session 与 public render
合同继续拥有自己的语义。

## 8. 构建一次、核验一次、消费同一字节

Q 的未来优化不应反复构建“看起来相同”的资产，再让不同 Gate 各自消费不同字节。候选模式是：

```text
build once
    -> own immutable artifact snapshot
    -> hash once
    -> publish exact reference
    -> downstream gates consume the same verified bytes
```

这不表示所有 Gate 可以共享工作目录、虚拟环境或可变缓存。路径只负责定位，快照负责身份；被核验的
Artifact 必须继续成为下游实际消费的 Artifact，不能重新构建后沿用旧摘要。

## 9. 有界并行与资源所有权

Q 的验证 Lane 候选必须至少隔离：

```text
exact source/worktree
interpreter / venv / package resolution
temporary root and artifact namespace
ports and owned processes
environment variables and credentials
cancellation and cleanup
resource budget
```

网络出口、GitHub rate limit、CPU、内存、磁盘和浏览器缓存可能仍是共享资源；目录不同不自动证明 Lane
独立。默认 16 GB Windows 基线继续串行或有界微并行，只有真实资源 Profile 证明后才允许扩大并发。

Q 的验证调度并行与 M8/CAP-008 的实验 wave 并行必须分开：

```text
Verification-lane parallelism
    changes how proof obligations are executed

Experiment/workload parallelism
    changes the subject load and experimental semantics
```

前者成立不能证明后者，后者的 overlap 事实也不能自动授予 Q Lane 隔离。

## 10. 预算、失败与确定性汇合

所有 Lane、重试、等待和清理必须消费已声明的绝对预算；子阶段不能各自刷新一份完整 timeout。Q 不接管
Gate 内部的 transport retry 或生命周期语义，只负责保存 Gate 已声明的预算和跨 Lane 资源安排。

确定性汇合至少保留：

```text
scheduled obligations
executed obligations
reuse candidates and exact Evidence refs
blocked / cancelled / failed lanes
missing outputs
per-lane provenance and cleanup state
stable join ordering
```

`8/11 jobs succeeded` 不能被 join 成“验证完成”。缺失、失败、取消和未知继续进入 Evidence/Core，不能
由 Q 使用多数票、最后成功或最佳结果覆盖。

## 11. 与 R1、未来 ChangeSet 能力的关系

R1 0.1 只建立**单一 SourceSnapshot**上的 Python 3.10 结构事实、关系、ReviewSlice 和 CoverageLedger；
它明确不提供 change blast radius。Q 不得为了获得 impact graph 反向扩大 R1：

```text
R1 0.1
    single-snapshot structural facts

future R2 or independent ChangeSet Provider
    base/head/change-set deterministic facts
                |
                v
Q
```

Q 可以消费未来 R Provider 的标准 Artifact，但不能导入 R 实现、要求 R 产生“safe to skip”，也不能把
AttentionProposal 当成依赖事实。Review Attention 提醒人看哪里；Q 规划既定证明义务怎样执行，二者没有
上下级关系。

## 12. 规则—反例—停止线矩阵

| 候选规则 | 最小反例 | Q 必须怎样处理 |
| --- | --- | --- |
| 文件类型不是影响证明 | `docs/*.md` 被 packaging、doctest 或发布清单消费 | 没有完整依赖闭包就执行 Gate |
| commit 相同不等于外部观察仍新鲜 | 同 SHA 的 GitHub 页面由新 renderer 重新呈现 | 按 sealed freshness 要求重新观察 |
| last green 不等于 reusable Evidence | 旧绿灯来自另一 Python/toolchain/Profile | 身份不符，不绑定复用 |
| 局部依赖图成功不等于闭包完整 | 动态配置或生成输入未进入图 | 保留 UNKNOWN，fail-closed |
| 两次安全构建不等于同一 Artifact | 下游重建产生不同 wheel 字节 | 消费同一已核验快照 |
| Lane 目录不同不等于隔离 | 两个浏览器 Gate 共用端口或 rate limit | 串行或显式共享资源预算 |
| 并行结束顺序不拥有结果顺序 | 机器负载改变完成先后 | 用稳定 obligation identity 汇合 |
| Planner success 不等于验证完成 | Schedule 完成但一个 Gate 没有 Evidence | 交给 Core 得到非 PASS 结果 |
| 重试不能刷新全局预算 | 每次 attempt 获得新的完整 timeout | 共享绝对 deadline |
| Q 不得自证自己的 impact model | Planner 用自己生成的闭包证明自己可以复用 | 依赖冻结 Provider Evidence 与独立负例 |

新反例继续高于现有绿灯：若真实 Gate 证明 Q 的输入模型漏掉依赖，停止复用该类 Evidence，保留失败事实，
并只重开受影响的合同边界。

## 13. 首个未来 Reference Lab 决策

Q0 只冻结首个实验的形态，不执行实验：

```text
one frozen synthetic dependency graph
two exact source coordinates: base / head
one gate whose exact input closure remains identical
one gate whose exact input closure changes
one unknown/dynamic dependency negative control
one bounded serial baseline
one candidate optimized schedule
```

需要证明：

1. 不变 Gate 只能绑定 exact-identity 仍成立的旧 Evidence；
2. 变化 Gate 必须重新执行并产生新 Evidence；
3. unknown dependency 必须退回完整执行，而不是复用；
4. serial baseline 与 optimized schedule 向 Core 提供等价的证明义务覆盖，不要求 Evidence 文件身份相同；
5. 任一 reuse binding 被篡改、过期或错绑时，Core 不能得到错误 `PASS`；
6. 删除 Q 插件后，现有完整串行门禁和 Core 仍可独立工作。

这个合成实验只能证明机制。未来实现冻结前还必须在真实 docs、源码、依赖/打包和开放世界观察变更上
建立有界 Profile；不能把一个“docs-only”样本外推为通用影响模型。

## 14. 实现入口前置门

Q0 冻结后仍不得实现。进入任何后继施工前，至少需要另行证明并冻结：

1. 一个 exact base/head `ChangeSet` 或等价 Provider Artifact；
2. Gate contract 与 transitive input-closure 的身份模型；
3. Evidence freshness、invalidity 与 reuse policy 的权威归属；
4. 一组覆盖 documentation、source、dependency/packaging 与 public observation 的真实验证 Profile；
5. 16 GB 主机上的串行基线、资源分账和候选隔离预算；
6. Q 缺失、失败或卸载时，现有 Core/P/R/CI 不受影响；
7. first reference lab 的 sealed acceptance contract、负向矩阵和停止线；
8. 明确的新施工授权与 exact-main 基线。

这些条件不必由 R1 提供，也不预设未来一定进入实现。若采集到的真实 Profile 表明调度复杂度高于节省
收益，Q 应收缩、延后或拒绝实现。

## 15. 包与仓库边界

若未来实现，优先作为 VeriTrail 仓库内的独立插件边界孵化，例如概念位置：

```text
plugins/verification-scheduling
```

本文不创建该目录，也不冻结 distribution 名。只有出现独立版本生命周期、独立用户、独立依赖栈、独立
发布或贡献边界后，才讨论拆成新仓库。现在拆仓只会让协调成本大于隔离收益。

Q 不能成为 Core、P、R、Starter 或 Workbench 的默认依赖。基础安装没有 Q 时，完整串行验证必须保持
可用；Q wheel 卸载后，既有标准 Evidence 仍应由 Core 读取。

## 16. Q0 候选冻结门

Q0 只有满足以下条件后才有资格冻结：

1. README、AGENTS、milestones、能力地图和本文对 Q 的身份与权威没有竞争定义；
2. 明确区分 P、R、Q、Core、M8/CAP-008 与未来 ChangeSet Provider；
3. 输入闭包、Evidence 复用、开放世界 freshness、Lane 隔离、绝对预算和 deterministic join 均有反例；
4. `Quick` 没有被写成性能承诺、Gate 豁免或 `SAFE_TO_SKIP` 权威；
5. diff 只包含文档，不出现 Schema、源码、CLI、CI、缓存、调度器、标签、Release 或空插件目录；
6. 候选通过受保护主线合入，从新的 exact main 匿名读回 README、能力地图与本文；
7. 后继独立 docs-only 状态发布完成自己的原始门禁、合入和合入后读回后，才允许写：

```text
Q0_BLUEPRINT_FROZEN
Q_IMPLEMENTATION_NOT_STARTED
NO_GATE_SKIP_AUTHORITY
```

在此之前状态保持：

```text
Q0_BLUEPRINT_CANDIDATE
Q_IMPLEMENTATION_NOT_STARTED
```

Q0 的完成只意味着“这个问题被正确放进了自己的边界”，不意味着优化已经存在，也不改变 R1 已获准的
Schema 起草入口。Q0 闭环后，当前主线返回 R1 Schema；Q 继续等待实现前置事实。
