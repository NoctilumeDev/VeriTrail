# Review Attention 首个 Pattern Corpus 选择与 payload 候选

> 当前状态：`CORPUS_PAYLOAD_CANDIDATE / LEDGER_OPEN / CORPUS_CLOSURE_NOT_STARTED / R1_BLOCKED`
>
> 起始基线：`main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a`
>
> 冻结合同：[文档 109](109-review-attention-pattern-corpus-freeze-contract.md)
>
> 影响层级：`L0_DOCUMENTATION + L2_CONTRACT_PAYLOAD`；只选择首个 R1 Corpus、追加线性
> `FROZEN_PATTERN` revision 并生成非自引用 manifest，不实现 Provider、Schema、CLI、CI 或 R1 runtime

## 1. 裁决

首个 Corpus 只选择四条模式：

| R1 边界 | 选择 | 该模式独立约束什么 |
| --- | --- | --- |
| SourceSnapshot 入口身份 | `RA-008 rev2` | 友好别名必须只解析一次，并把精确源码坐标传播给派生物 |
| SourceSnapshot 消费连续性 | `RA-023 rev3` | 被核验的快照必须继续成为真正参与语义派生的快照 |
| 语义关系来源组合 | `RA-003 rev2` | 多个关系来源必须明确为互斥、优先、覆盖或叠加，成功不能自动短路其他适用来源 |
| 有界 Slice 与覆盖账本 | `RA-004 rev2` | 边界内执行成功不能冒充完整覆盖，停止原因与遗漏必须保持可见 |

四条共同覆盖文档 109 冻结的四类 R1 知识需求，但不把 Ledger 变成通用缺陷目录，也不把 P2–P4 的
浏览器、发布、重试或分发机制带入 R1。Manifest 位于
[`review-attention-pattern-corpus-0.1.json`](review-attention-pattern-corpus-0.1.json)，仅保存精确
`pattern_id + selected_record_digest` 及冻结分类投影。

## 2. 最小性证明

这不是按命中次数、流行度或条目数量选出的集合。依次删除任一条都会形成不同的合同缺口：

- 删除 `RA-008`：入口仍可用 `HEAD`、branch 或未绑定工作目录冒充 SourceSnapshot 身份；
- 删除 `RA-023`：即使入口摘要正确，后续仍可通过 locator 重读或共享可变对象消费另一份源码；
- 删除 `RA-003`：多 Provider 的关系事实仍可被 `fallback / first-success` 静默截断；
- 删除 `RA-004`：有界遍历仍可在达到深度、文件、符号或时间边界后冒充完整 Slice 与完整覆盖。

`RA-008` 与 `RA-023` 不是重复项：前者约束**坐标解析身份**，后者约束**核验后到消费时的快照连续性**。
同一个实现可以满足其中一条而违反另一条。`RA-003` 与 `RA-004` 也不重复：前者约束来源间组合，后者
约束单个或组合来源的覆盖声明。

## 3. 全 Ledger 逐条审议

`未选择` 不等于 `REJECTED`，也不表示模式无价值；它只表示该条不是首个 R1 Corpus 的最小必需知识。

| Pattern | 本轮裁决 | 理由 |
| --- | --- | --- |
| RA-001 | 未选择 | Verdict/处置权边界已由 R0 合同约束，不是 R1 SourceSnapshot、关系或 Slice 构造知识 |
| RA-002 | 未选择 | IdentityCollapse 过宽；R1 需要的源码身份问题已由 RA-008 与 RA-023 两个可证伪机制精确覆盖 |
| RA-003 | **选择** | 独立约束多关系来源是 fallback、precedence 还是 layering |
| RA-004 | **选择** | 独立约束 bounded Slice 的 coverage 与 truncation，不允许 local success 冒充 complete |
| RA-005 | 未选择 | 跨观察原子性主要属于 P1/P2 多来源观察；R1 首个单 SourceSnapshot 派生不需要该语义 |
| RA-006 | 未选择 | VerdictPriority 属于 Core 裁决，不应进入 Review Attention 的 R1 事实构造 |
| RA-007 | 未选择 | R1 不声明跨时间全序；如后续引入事件序列，应在相应里程碑重新审议 |
| RA-008 | **选择** | SourceSnapshot 精确坐标是所有 CodeFact、Relation 与 Slice 的入口身份 |
| RA-009 | 未选择 | Pairing 主要服务跨 Evidence handoff；R1 的单快照绑定由 RA-023 更直接约束 |
| RA-010 | 未选择 | 前提与 Seal 权威属于人和 Plan，不是 R1 Provider 可推导事实 |
| RA-011 | 未选择 | DependencyBoundary 已在 R0 插件架构冻结；不是首个 Corpus 需要重复携带的审查知识 |
| RA-012 | 未选择 | Presentation 层的 CompleteLabel 属于后续 AttentionMap/界面语义 |
| RA-013 | 未选择 | RetryBoundary 面向副作用执行，R1 只做只读静态派生 |
| RA-014 | 未选择 | ProposalCoverage 属于后续 Provider 输出质量；R1 基础 coverage 先由 RA-004 约束 |
| RA-015 | 未选择 | PolicyPriority 属于未来排序与人工策略，R1 不排序也不处置 |
| RA-016 | 未选择 | InstructionBoundary 已由 R0 威胁边界冻结，且不属于四个 R1 构造边界 |
| RA-017 | 未选择 | NetworkBudget 是 P2 浏览器采集机制，不适用于 R1 静态源码图 |
| RA-018 | 未选择 | LifecycleBudget 是运行时清理机制，不适用于首个 R1 Corpus |
| RA-019 | 未选择 | ExecutionProvenance 留待 R2 AnalyzerEvidence；R1 的源码 subject 先由 RA-008/023 约束 |
| RA-020 | 未选择 | LifecycleOwnership 属于浏览器/进程运行时，不是 R1 语义图构造 |
| RA-021 | 未选择 | ProductionFixtureConformance 留待 R2/R5 provider 与发布验证 |
| RA-022 | 未选择 | ObserverEffect 面向浏览器/动态观察；R1 只读静态派生不需要其网络语义 |
| RA-023 | **选择** | 防止“核验 A、消费 B”的 SourceSnapshot 连续性破坏 |
| RA-024 | 未选择 | ManifestSelfReference 已是 Corpus 构造合同规则，不应再作为 R1 审查模式重复输入 |
| RA-025 | 未选择 | RetryRecovery 是发布下载可用性策略，不适用于 R1 |
| RA-026 | 未选择 | DistributionIdentity 属于构建/Release 交付链，不适用于 R1 |
| RA-027 | 未选择 | AssertionScope 是测试计划预算问题，不适用于 R1 事实/关系/Slice 构造 |

## 4. 修订链与 manifest 边界

选择过程分成两个不可互相替代的步骤：

```text
完整 CONTRACT_CANDIDATE revision
    ↓ 独立摘要与线性链复算
FROZEN_PATTERN successor revision
    ↓ manifest 精确选择
Corpus payload candidate
```

当前 manifest：

- 只含合同允许的六个顶层字段；
- `entries` 按 `pattern_id` 升序；
- 每项只含五个允许字段；
- 不包含自身摘要、Git commit、当前 HEAD、时间戳、Verdict、HumanDisposition 或 Provider 分数；
- 未选 Ledger 记录不参与 manifest identity。

Manifest 的完整 UTF-8/LF 文件摘要会在后继 closure 中与 payload **合入后的 exact source commit** 一起外部
绑定。本文不预填未来 commit，也不把本地候选摘要冒充远端冻结事实。

本地候选复算使用仓库声明的 Python 3.10.6 与 3.13.13，并分别运行 normal 与 `-O`。审计器不依赖
`assert`，四条路径均显式验证 20 条完整 revision、14 个线性 pattern chain、4 个 manifest entry 和 15
个负例；四次得到相同候选 manifest SHA-256：
`ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`。该值只记录 pre-merge 字节复算，
不代替后继 closure 的权威绑定。

负例覆盖：已选语义篡改、缺字段、断链、revision 回退、并发 successor、seed/`GENERALIZED`/`REJECTED`
误选、重复 pattern、重复 digest、未排序 entry、未知 taxonomy/canonicalization、manifest 自引用字段和
entry 越权字段。另有正交不变量证明：修改未选 Ledger revision 不改变 manifest bytes；修改已选 revision
语义但不更新摘要必然拒绝。

扩大回归同样显式绑定本 worktree 的 Core 与 GitHub Evidence Plugin 源码坐标：Core 在 Python 3.10.6
与 3.13.13 的 normal 与 `-O` 下均为 `416/416`，GitHub Evidence Plugin 均为 `180/180`，Authoring Skill
均为 `24/24`。第一次 Core 扩大回归只绑定 Core `src`，在加载第 406 项时因无法导入同一 worktree 的
`veritrail_github` 而停止；该结果没有被归类为产品失败或通过。补齐两个源码坐标后从头重跑得到上述
四矩阵结果，原始 import failure 不被后继成功改写。

## 5. 当前停止线

本 payload 即使本地复算全部通过，也仍然只是候选。以下事实尚未成立：

```text
no protected-main merge for this payload
no exact merged Corpus source commit
no externally bound manifest digest
no anonymous exact-SHA manifest readback
no R1 implementation
```

后继只能先完成 payload 的原始远端门禁与受保护主线合入，再从新的 exact main 创建独立 closure 状态
文档，绑定 source commit 与 manifest digest，并完成匿名公开读回。任一失败或新反例都会继续保持
`R1_BLOCKED`。
