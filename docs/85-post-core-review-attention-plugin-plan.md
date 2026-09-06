# Post-Core Review Attention Plugin Plan v1.2

## 1. 文档身份

- 轨道：顶层 `R` 轨；`R = Review`，不表示 `Risk`；
- 当前阶段：`R0_ARCHITECTURE_FROZEN / PATTERN_LEDGER_OPEN / DESIGN_ONLY`；
- 并行状态：`P1_FROZEN / P2_FROZEN / P3_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`；
- 影响等级：`L2_CONTRACT + L3_SYSTEM / DESIGN_ONLY`；
- 本文不创建源码包、Schema、CLI、CI、标签、Release 或可运行审查器；
- 本文不重开 M0–M14、E 轨、PC 兼容桥或 P0/P1 冻结结论。

冻结闭环与公开读回事实见[文档 88](88-r0-review-attention-design-review.md)。

仓库历史中的 `M12-R1/R2/R3` 是 M12 内部的表现层重组阶段。本文的顶层 `R0–R6` 必须始终写出
`Review Attention` 全名；未来包、标签和发布坐标不得只使用裸 `r*`，以免与历史阶段混淆。

## 2. 为什么另开 R 轨

AI 可以快速生成大量结构完整、测试齐全、内部自洽的代码，但人的理解与复核吞吐不会同步增长。
真正的风险不只来自语法错误，而是来自更隐蔽的现实模型偏差：实现、测试和 CI 都可能忠实执行一个
不完整的前提。

R 轨的目标不是自动替人判定代码对错，而是把有限注意力送到最需要人确认的结构上：

```text
精确源码坐标
    -> 可复算的代码事实与分析证据
    -> 不拥有真值的关注提案
    -> 可解释的注意力地图
    -> 人工确认、驳回、争议或补证
    -> 可追溯 Review Bundle
```

它减的是阅读负担，不减判断责任；它帮助发现问题，不替任何人决定问题。

## 3. 与现有能力的关系

| 能力 | 拥有什么 | 不拥有什么 |
| --- | --- | --- |
| Core | sealed 条件、Evidence 关系、确定性 Verdict | 代码审查启发式、AI 提案、人类审查决定 |
| M13 | 一次已冻结的系统与分层代码质量终审事实 | 可复用审查产品、持续规则库、插件运行时 |
| P 轨 | GitHub/API/公开页面等平台事实采集 | 源码风险真值、审查优先级、人类决定 |
| R 轨 | 代码事实、分析来源、关注提案、注意力地图和审查处置的边界 | Core Verdict、现实真相、Seal 权、仓库写权限 |

R 轨可以消费 P 轨留下的反例与平台 Evidence，但不得导入 P 插件实现，也不得要求 P2–P4 为自己改变
合同。P2–P4 仍按自身路线施工；其中发现的新模式只追加到 R 的 Pattern Ledger。

## 4. 系统闭环

```text
Human Seal Authority
    seals ReviewPolicy and retains final disposition authority
                         |
                         v
Exact Source Snapshot -> Source/Semantic Providers -> Code Facts
                         |                         |
                         |                         v
                         +-> Deterministic Analyzers / Runtime Evidence
                                                   |
                                                   v
                                      Proposal Provider (optional AI)
                                                   |
                                                   v
                                           Attention Map
                                                   |
                                                   v
                                          Human Disposition
                                      /        |         \
                              dismiss   need evidence   confirm/escalate
                                               |             |
                                               +-------------+
                                                   |
                                                   v
                                           Review Bundle
                                                   |
                                 optional exact handoff to Core
```

闭环成立依赖五个不同责任层：

1. 人拥有 ReviewPolicy 的 Seal 决定与最终 HumanDisposition；
2. 已封存 ReviewPolicy 机械约束审查范围、优先级、必审项、允许的数据外发方式和 Provider；它不能
   生成、驳回或替代 HumanDisposition；
3. 可替换 Provider 产生带来源的事实、证据或提案；
4. Review Attention application 只执行合同校验、Artifact 关联和流程状态，不生成 Core Verdict；
   规范化、分析、提案、排序与展示均来自可替换 Provider；
5. Core 仅在未来显式 handoff 且存在 sealed AcceptancePlan 时独立裁决。

`need evidence` 会回到证据 Provider，而不是让 AI 自行把猜测升级为事实。一次驳回也不删除原提案；
处置以新 Artifact 保留。因此来源、推导、决定和最终验收可以分别追溯。

## 5. 分层，而不是微服务碎片化

“一切皆插件”在本轨的含义是：**可替换能力通过稳定合同接入，不可替换的权威与语义留在薄边界中。**
它不要求每个 Provider 都成为独立进程或微服务。

R 轨不可替换的薄内核只允许包含：Contract、Artifact identity、生命周期规则、manifest 校验和
capability discovery。语言解析器、Analyzer、模型、排序、去重、传输、存储和界面都没有资格成为
内核实现依赖。

未来可以有一个高内聚产品边界，例如 `plugins/review-attention`，内部暴露窄 SPI：

```text
SourceProvider
SemanticMapper
AnalyzerProvider
RuntimeEvidenceProvider
ProposalProvider
AttentionStrategyProvider
PolicyProvider
PresentationAdapter
```

`PolicyProvider` 只能加载、校验和应用已封存 ReviewPolicy；它不能因自动规则命中而代替人产生
`HumanDisposition`。若未来确需自动处置，必须另建身份不同的 `PolicyDisposition`，不得复用人工签字语义。

Provider 之间只交换版本化 Artifact，不共享可变控制状态，不直接调用彼此的实现类型。排序、聚合、去重
和展示策略同样属于可替换能力；Review Attention application 只执行合同允许的流程与状态转换，不内置
某家模型或某套启发式。部署时可以同进程，
但依赖方向仍然是：

```text
Provider implementation -> R contracts <- Review Attention application
                                      |
                                      v
                              optional Core handoff adapter
```

如果一个单体进程同时拥有源码事实、AI 提案、人类决定和 Verdict，哪怕目录拆得很漂亮，也不算分层。

## 5.1 R1 的 Semantic Review Slice 设计边界

源码不是线性文章，而是由 symbol、调用、状态、资源、authority 与变更关系组成的图。R1 不应把每行
代码唯一切进某个固定“段落”，也不应以等长 token/file chunk 冒充语义边界。未来的确定性语义清单
应先建立可追溯关系，再派生多个允许重叠的 `Semantic Review Slice` 视图：

```text
Exact Source Snapshot
    -> deterministic Code Facts
    -> typed semantic relations
    -> bounded overlapping Review Slices
    -> coverage ledger
```

候选 slice 至少包括 symbol、call path、state transition、ownership/authority、resource lifecycle 与
change blast radius。一个源码锚可以同时出现在多个 slice 中，因为 slice 是认知视图，不是源码存储或
唯一真值分区。

每个派生 slice 必须能解释并复算其：

```text
anchor
relation kind and direction
expansion depth
max symbols / files
stop conditions
coverage
truncation reason
SourceSnapshot binding
```

达到边界时必须保留 `PARTIAL` 与截断原因，不得把有界子图描述为完整调用链或完整状态所有权。R1
优先使用解析器、编译器或确定性规则建立这套骨架；AI 只能在 R3 提议多个 slice 可能属于同一审查主题，
不能反向改写 CodeFact 或把自己选择的上下文用来证明自己的提案。

三种权责继续分离：

```text
segmentation / slice derivation != analysis != attention ranking
```

本节只补充 R1 的未来施工问题，不冻结 `ReviewSlice` Schema，不把它加入已冻结 R0 Artifact 清单，也
不解除 `R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE`。具体 Schema、语言支持、关系类型和 coverage 算法
仍须在 R1 开工前从精确 Pattern Corpus 单独定稿。

## 6. 阶段路线

| 阶段 | 只回答的问题 | 明确不进入 |
| --- | --- | --- |
| R0 | 权威、Artifact、依赖、失败、视觉语义和 Pattern Ledger 如何冻结 | 任何实现 |
| R1 | 如何对精确 Source Snapshot 建立确定性语义清单、关系图、可重叠有界 Slice 与覆盖账册 | AI、自动排序、人类结论 |
| R2 | 如何接入静态分析、编译器、测试、Profiler/Sanitizer 等可复算证据 | AI 判错、Core Verdict |
| R3 | AI/规则如何提出带依据的关注候选并形成注意力地图 | 自动确认缺陷、自动合并 |
| R4 | 人如何确认、驳回、争议、请求补证并保留责任链 | 用处置覆盖原始证据 |
| R5 | 如何将选定事实与处置按精确坐标交给 Core 独立验收 | 私有比较器、Verdict 泄漏 |
| R6 | 如何独立打包、卸载、发布并完成公开读回 | 回填 Core、改写旧 Release |

R0 可以先冻结，但 **R1 不得在 P4 之前启动**。P2–P4 完成后，必须从开放 Ledger 中选择一份精确
Pattern Corpus 快照，绑定提交与摘要，作为 R1 的输入基线。这样 P 轨反哺 R 轨，但不形成施工耦合。

## 7. 反例资产的双层冻结

R0 冻结：

- 产品身份、权威分配和依赖方向；
- Artifact 类别与身份不混用规则；
- Provider SPI 的能力边界；
- AI、人、Core 的职责；
- 紫色机器提案语义和非颜色提示要求；
- R1–R6 路线与 R1 前置门；
- Pattern Ledger 的正交分类、不可变修订身份与状态提升规则。

R0 不冻结全部未来审查规则。`docs/87-review-pattern-ledger.md` 在 P4 前保持 append-only/open：新反例
和状态提升都必须追加新的不可变 revision，不得原地改写旧记录，也不能反向改写 R0 权威。P4 后只冻结
一个供 R1 使用的 corpus snapshot；manifest 必须为每个模式绑定 `pattern_id + selected_record_digest`，
历史 revision 继续保留。

## 8. 资源与权限边界

- 默认 local-first；远程 AI Provider 必须由 sealed policy 明确允许；
- 源码、评论、Issue、README 和生成内容一律视为待分析数据，不能成为工具指令；
- R0 不要求 GPU、Docker、数据库、消息队列或多机；
- Provider 的成功不等于仓库覆盖完整；未支持文件、跳过规则和失败范围必须显式保留；
- AI 不拥有写仓库、合并 PR、修改 Plan、Seal 或 Verdict 的权限；
- Codex Security 深扫、攻击路径分析和漏洞结论不属于本轨当前范围。

## 9. R0 停止线

R0 只有在以下事实全部成立后才可标记 `R0_ARCHITECTURE_FROZEN`：

1. 本 Plan、R0 合同和 Ledger Schema 经外部读者与语义反例复核；
2. 文档只通过受保护主线合入，不绕过远端门禁；
3. 精确 main SHA、匿名 README、Plan、合同与冻结事实页完成公开读回；
4. R0 首次冻结事实继续保留当时的 `P1_FROZEN / P2_NOT_STARTED`；本文当前并行状态另行反映
   `P2_FROZEN / P3_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`，两者不得互相改写；
5. 仓库中不存在 R 轨源码包、Schema、CLI、CI、标签或 Release；
6. R0 首次冻结记录中的状态继续保留为：

```text
R0_ARCHITECTURE_FROZEN
PATTERN_LEDGER_OPEN
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
P2_NOT_STARTED
```

本文当前状态只更新并行事实为
`P2_FROZEN / P3_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`；它不把 R0 当时尚未发生的
P2 写回历史，也不因 P3 合同冻结解除 R1 阻断。
