# Review Attention R1 确定性语义切片合同 0.1

> 状态：`R1_CONTRACT_CANDIDATE / R1_SCHEMA_NOT_STARTED / R1_IMPLEMENTATION_NOT_STARTED`
>
> 精确基线：`main@9ab64121350b69ce81e6be79961ad426026bbc39`
>
> 冻结输入：Pattern Corpus source commit
> `9bdcef30517309bbc87ed7fdb0fec395197ef58a`；manifest SHA-256
> `ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文只收敛 R1 0.1 的语义边界，不创建 Schema、源码包、
> CLI、CI、Provider、标签、Release 或可运行审查器

## 1. 目的与当前停止线

P4 与首个 Pattern Corpus 已经冻结，因此 R1 可以合法地定义合同；这不等于 R1 已经实现。R1 0.1
只回答一个有界问题：

```text
在一个精确、只读的源码快照上，
怎样产生可复算的结构事实与关系，
再派生允许重叠但有界的审查切片，
并诚实记录覆盖、未支持、失败和截断？
```

R1 0.1 的完整范围是：

```text
Exact SourceSnapshot
    -> deterministic CodeFacts
    -> typed structural Relations
    -> bounded overlapping ReviewSlices
    -> staged CoverageLedger
```

这一定义消除 [R 轨 Plan](85-post-core-review-attention-plugin-plan.md) 与
[R0 Contract](86-review-attention-r0-contract.md) 之间的局部表述差异：R1 同时包含关系图与语义切片，
不是只有源码清单和覆盖账册。R0 的权威、Artifact 分类和后续 R2–R6 边界不被改写。

本文仍处于候选状态。只有合同自己的远端门禁、受保护主线合入、精确主线与匿名公开读回全部成立后，
才允许另行发布 `R1_CONTRACT_FROZEN`；在 Schema 合同另行冻结前仍不得写实现。

## 2. 明确不进入 R1 0.1

R1 0.1 不做以下事情：

- 不判断代码正确、错误、安全或高风险；
- 不生成 AttentionProposal、AttentionMap、HumanDisposition 或 Core Verdict；
- 不调用 AI，不做自动排序、自动修复、自动合并或仓库写入；
- 不执行或导入待审源码，不以运行结果冒充静态事实；
- 不建立动态调用图、完整控制流、数据流、ownership、authority 或状态真值；
- 不声称理解整个多语言仓库，也不把 Python 子集成功外推为 repository completeness；
- 不分析 dirty worktree、未跟踪文件、工作区缓存或本机构建产物；
- 不通过网络、Docker、数据库、消息队列、GPU 或远程模型才能完成首个 reference lab；
- 不把 R1 代码放进 Core 或 GitHub Evidence Plugin，也不让后两者依赖 R1。

R2 可以在后继合同中增加静态分析器、编译器、测试和运行证据；R3 才允许产生机器关注提案。后继阶段
不得把自己的能力倒填成 R1 0.1 已经拥有的事实。

## 3. 权威与身份分层

同一份源码可以被不同策略、规范化规则或 Provider 分析；同一事实也可以由多次独立执行观察到。因此
R1 必须至少保持以下身份分离：

```text
Source Coordinate Identity
!= Source Content Identity
!= Derivation Profile Identity
!= Semantic Fact/Relation Identity
!= Derivation Evidence Identity
!= ReviewSlice Identity
!= CoverageLedger Identity
```

其中：

| 身份 | 只回答的问题 | 不回答的问题 |
| --- | --- | --- |
| resolved source coordinate | 去哪个 repository/commit/tree/root 取源码 | 该源码内容是否与别的提交相同 |
| source content | 精确快照包含哪些 Git 对象与字节 | 为什么选择这些文件做语义分析 |
| ReviewPolicy | 人封存了什么范围、语言与能力约束 | Provider 实际使用了什么实现 |
| DerivationProfile | 什么语义版本、词汇和有界派生规则可复算 | 某次执行是否成功 |
| CodeFact / Relation | 在该快照与 Profile 下派生了什么结构事实 | 该结构是否是缺陷或运行时真值 |
| DerivationEvidence | 哪个 Provider 按哪个 Policy/Profile、以什么版本、操作数和环境执行过 | 事实本身的唯一身份 |
| ReviewSlice | 某个锚按什么 SliceSpec 得到哪些事实、关系与 frontier | 完整业务语义或唯一源码分区 |
| CoverageLedger | 每个派生阶段的分母、完成项和缺口是什么 | “仓库已经看懂”的单一百分比 |

友好输入如 branch、`HEAD` 或标签只允许作为请求别名。别名必须在派生开始前解析一次，后继 Artifact
只能绑定解析后的精确坐标；运行期间不得再次解释别名。

## 4. SourceSnapshot 0.1

### 4.1 精确源码世界

R1 0.1 的 SourceSnapshot 必须由以下坐标共同限定：

```text
repository identity
exact commit identity
exact tree identity
exact analysis root
tracked-entry inventory
```

分析根可以是 repository root，也可以是提交内的精确子树。repository root 使用一个专门的规范表示；
非根路径必须是相对 POSIX 路径，并拒绝绝对路径、空段、`.`、`..` 和别名归一化歧义。具体字段名与
根路径编码留给 Schema 合同，但不得改变此语义。

SourceSnapshot inventory 必须覆盖该 root 下全部 Git tracked entry，而不是只列“成功解析的源码”。每项
至少保留可复算的 Git path、mode、object identity、node kind 和内容身份。读取来源必须是精确 Git
对象或等价不可变快照；不得遍历当前工作目录后把 `__pycache__`、忽略文件、本地构建产物或未跟踪文件
混入快照。

Git path identity 不做大小写折叠或 Unicode 归一化。未来 Schema 必须选择可逆表示，保证两个不同 Git
path 不会因宿主文件系统或显示层规则被合并。

### 4.2 特殊条目与边界外对象

symlink、submodule、特殊 mode 和非普通 blob 必须留在 inventory 并显式分类，不能静默跟随或丢弃。
首个 reference lab 只声明普通 Python blob 具备语义派生能力；其他条目仍属于源码快照，但可能进入
`OUT_OF_SCOPE` 或 `UNSUPPORTED`，具体原因必须由 Policy 与能力事实共同解释。

引用指向分析 root 之外时，目标是 `EXTERNAL_TO_SNAPSHOT`，不是“目标不存在”。这是一项拓扑事实，
必须与 `RESOLVED / UNRESOLVED / UNSUPPORTED / CONFLICT` 等解析状态正交保存。

### 4.3 快照连续性

路径只负责定位，已读取的内容快照才负责派生身份：

```text
locate exact source
    -> read/own one immutable snapshot
    -> verify content identity
    -> derive facts, relations, slices and coverage from that same snapshot
```

禁止 `verify(mutable path) -> reread(mutable path) -> derive`。如果实现必须分阶段运行，后继阶段必须
消费前一阶段已经绑定的不可变内容，或从有独立不可变性保证的内容寻址对象重新读取并复核同一身份，
而不是重新解释可变别名。该约束直接落实 Corpus 的 `RA-023`。

dirty worktree、index-only change 和未跟踪内容留给后继版本另行建模；R1 0.1 不把它们偷偷压成某个
伪造 commit。

## 5. ReviewPolicy、DerivationProfile 与 Provider

三者不能共享权威：

```text
ReviewPolicy
    人类 Seal authority 选择允许/要求的范围、语言、Profile、Provider capability、
    slice-generation 参数与非语义执行安全预算

DerivationProfile
    冻结语义版本、支持语言、事实/关系闭集、规范化规则、规范遍历与边界解释规则

ReviewSliceSpec
    从 exact Snapshot、sealed Policy、Profile 和 selected anchor 机械实例化，
    绑定关系方向、实际结构预算与停止条件；它不另有参数权威

Provider Evidence
    报告该次实际 Provider/解析器实现、版本、环境、操作数、起止和结果
```

Policy 引用不可变 `DerivationProfile` identity，不复制一套竞争的派生语义。Profile 定义“参数如何解释
与规范遍历”，Policy 选择允许的参数值、锚生成范围，并设置 wall-clock、memory 等不进入正常派生身份的
安全预算；ReviewSliceSpec 只把 exact Snapshot、Policy、Profile 与某个实际 anchor 机械绑定成一次可复算
的派生说明。CLI 或 request 不得另造参数权威；运行参数只能由已封存 Policy/Profile 机械派生，或只影响
非语义执行预算并进入 Evidence。

首个 Profile 是 **Python source 3.10 semantic profile**：只接受该 Profile 明确支持的 Python 3.10 语法，
采用 R1 自有、版本化的规范化投影；不得把 CPython 原始 AST、对象 `repr`、哈希随机化结果或解释器私有
字段直接作为 Artifact 身份。相同输入必须在 CPython 3.10/3.13、normal/`-O` 下产生相同规范化事实与
摘要。只有 3.13 能解析的语法必须被首个 Profile 有类型地拒绝，不能因运行解释器更强而悄悄扩大
Profile；具体拒绝分类留给 Schema 合同，不在此把它混同为普通语法错误。

Provider implementation identity 不进入 Fact identity；只有规范化语义或派生规则变化才需要升级
DerivationProfile。实现版本、解析器版本和运行环境全部保留在 DerivationEvidence 中。

## 6. CodeFact 与 Relation 的边界

### 6.1 首版闭集

首个 Profile 只产生可由 path/Profile 或语法节点直接定位的结构事实：

```text
module entity derived from the exact Git path
class declaration
function declaration
method declaration
import declaration
```

每个 Fact 必须绑定 SourceSnapshot、DerivationProfile、精确 Git path 与源码字节锚。行号和列号可以作为
显示坐标，但不能单独构成身份；锚的规范编码与端点规则必须在 Schema 合同中冻结。

首版 Relation 闭集只包含能由同一快照直接、确定性派生的结构关系：

```text
LEXICAL_CONTAINS
IMPORT_TARGET_LITERAL
```

`IMPORT_TARGET_LITERAL` 保留源码中声明的 import target 和边界状态；它不声称目标已经被运行时加载，也
不推导动态 import 结果。首版有意不提供 `CALLS`：没有静态绑定语义支持时，函数调用语法不等于已解析
的调用目标。

以下内容明确不是 R1 0.1 的 CodeFact/Relation：

```text
runtime call target
state ownership or authority
resource lifecycle truth
business invariant
defect/risk judgment
change blast radius
```

change blast radius 至少需要 base/head/change set 身份，不得从单快照关系图凭空派生。

### 6.2 确定性不等于权威真值

同样输入得到同样输出只证明派生规则可复算，不证明其完整描述 Python、运行时或业务世界。所有 Fact 与
Relation 都必须保留 Profile 和来源；`DETERMINISTIC` 不能被显示成 `AUTHORITATIVE`。

## 7. 多来源组合与冲突

Provider 或派生来源的组合规则必须显式声明，不能因为一个来源成功就默认其他来源不适用。首个 Profile
可以只要求一个 SemanticMapper，但合同与夹具必须保留下列通用语义：

- 独立适用来源按声明的 composition rule 聚合，不能偷偷使用 `first success` 或 fallback；
- 规范化后相同的 Fact/Relation 可以共享内容身份，但必须保留全部来源 provenance；
- 来源对同一规范化 subject/key 给出不兼容属性时，必须保留冲突与双方证据，不能 last-write-wins；
- 一个来源为空只说明该来源没有报告内容，不能取消另一来源，也不能证明组合结果完整；
- 任一必需来源不可观察时，CoverageLedger 必须保留不确定性。

这直接落实 Corpus 的 `RA-003`。fallback 本身并非错误；只有外部或合同语义确实声明来源互斥、优先或
替代时，才允许相应组合。

## 8. CoverageLedger 是分阶段依赖账册

R1 0.1 不输出一个“repository coverage 百分比”。CoverageLedger 必须把覆盖写成可追溯依赖链：

```text
Snapshot Inventory
    -> Policy Scope
    -> Language Support
    -> Parse
    -> Fact Derivation
    -> Relation Derivation
    -> Slice Derivation
```

每一阶段至少必须回答：

```text
denominator source and digest
denominator state: KNOWN or UNKNOWN
eligible items
completed items
out-of-scope items
unsupported items
unresolved items
conflicts
parse failures / execution failures
truncated items and frontier
upstream dependency state
```

这些状态不能互相冒充：

| 状态 | 语义 |
| --- | --- |
| `OUT_OF_SCOPE` | Policy 明确排除；不是能力缺失 |
| `UNSUPPORTED` | Policy 请求了能力，但当前 Profile/Provider 不具备 |
| `UNRESOLVED` | 观察到引用，但目标在允许的解析世界内仍未解析 |
| `CONFLICT` | 两个适用来源给出不兼容观察 |
| `PARSE_FAILED` | 输入被声明 eligible，但无法按 Profile 解析 |
| `TRUNCATED` | 有界派生主动停止并保留 frontier |

混合仓库中，Python 分母完整不等于 repository 分母完整。若 TypeScript/Vue/JavaScript 等 tracked entries
不在首个 Profile 中，它们必须留在 Snapshot/Policy/Language Support 阶段；报告只能声明
`Python-profile coverage`，不能写“仓库已完整分析”。

若某个本应进入符号空间的文件解析失败，则完整符号分母无法建立：系统可以声明“对成功解析的子集完成”，
但 repository/global symbol denominator 必须为 `UNKNOWN`，不得使用较小的已知子集重新定义全局分母。

这直接落实 Corpus 的 `RA-004`：bounded success 可以有用，但不能冒充 complete。

## 9. 执行状态与覆盖状态分离

执行是否完成，与结果覆盖是否完整，是两个正交维度：

```text
execution: COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE
coverage:  COMPLETE / PARTIAL / UNKNOWN
```

精确枚举与字段名留给 Schema 合同，但以下组合语义现在冻结：

- 达到确定性的 `max_depth / max_symbols / max_files / max_relations` 可以是 execution `COMPLETED`，同时
  coverage 为 `PARTIAL`；
- parser failure、缺少必需 Provider 或未知上游分母不能被写成 `COMPLETE`；
- wall-clock timeout 只是一项安全预算，具有环境与调度噪声；超时产生 execution `INTERRUPTED`，不得把
  当时偶然得到的前缀发布成正常完成的 FactSet、RelationSet、ReviewSlice 或 CoverageLedger；已经观察到
  的单项事实可以留作带中断 provenance 的诊断 Evidence，但不能冒充完整派生产物；
- 后继版本只有先冻结确定性 checkpoint/resume 规则，才可以把 timed partial 作为不同身份的 Artifact；
  R1 0.1 不这样做。

确定性边界必须依赖已封存的结构预算、规范遍历顺序与明确的端点规则。循环、重复路径和 frontier 也必须
通过稳定 identity 去重或记录；不能依赖集合迭代顺序、线程完成顺序或 wall time 决定切片内容。

## 10. ReviewSlice 0.1

ReviewSlice 是派生认知视图，不是源码唯一分区，也不是风险结论。它至少绑定：

```text
SourceSnapshot identity
DerivationProfile identity
FactSet / RelationSet identity
ReviewSliceSpec identity
anchor identity
included Fact/Relation identities
frontier and truncation facts
```

CoverageLedger 在切片派生后单向引用 ReviewSlice 与该阶段分母；它不进入 ReviewSlice identity，避免
`ReviewSlice -> CoverageLedger -> ReviewSlice` 的循环身份。

ReviewSliceSpec 必须冻结 anchor、允许的 relation kind/direction、确定性 expansion bounds、stop policy 与
规范遍历顺序。具体字段名、边界是否 inclusive 和 tie-break 编码必须在 Schema 合同中定稿。

切片只引用 CodeFact/Relation identity，不复制并改写事实。不同切片允许包含相同 symbol 或 relation；
CoverageLedger 对唯一 identity 计数，不能把重叠出现次数当成额外覆盖。同一组成员由不同 SliceSpec 派生
时仍是不同 ReviewSlice，因为“为什么看见这些内容”不同。切片达到边界时必须保留 frontier 和
`PARTIAL` 原因，不得宣称完整调用链、状态机或影响面。

## 11. 冻结 Pattern 到设计约束

| Pattern 与 selected record digest | R1 设计约束 | 最小反例 | 非声明 |
| --- | --- | --- | --- |
| `RA-003 rev2`<br>`sha256:1e20737718ec5e4056dc39d91f750e81c0ccbfefa965b72c1d918bd679f669f7` | 来源关系必须显式为叠加、替代、优先或互斥；保留全部 provenance | 来源 A 报告事实 x，来源 B 报告事实 y；`first-success(A)` 丢失 y | fallback 不自动等于 bug |
| `RA-004 rev2`<br>`sha256:1915e4aba5b7604ed417c640ff54494c720cc2bb72c815bf4305f65f4d439077` | 每个有界结果保留分母、frontier、截断和 coverage state | `max_depth=1` 只见 A→B，却声称完整链中没有 C | partial 结果不自动等于无用 |
| `RA-008 rev2`<br>`sha256:194cd1eae23cf3d063a41a9f0b5b3f664a19b3b4b283034acaee07bbddb2198f` | 别名只解析一次，所有派生 Artifact 绑定 exact SourceSnapshot | `main` 在两阶段间移动，Fact 与 Slice来自不同 commit | 不禁止友好请求坐标 |
| `RA-023 rev3`<br>`sha256:fcf5d2a2364aa89413ae6d9884380cf7a3ff3f43a309970230d3e204d91b538b` | 被核验的内容快照必须继续成为派生所消费的快照 | 先 hash mutable path，再替换文件，后继重新读取同一路径 | 不要求所有内容常驻内存，也不禁止从有独立不可变性保证的内容寻址存储重复读取 |

Pattern 不是 `if` 规则，也不是缺陷标签。它们约束 R1 必须提出哪些身份、来源、覆盖和连续性问题；命中
只能产生事实或后续关注候选，不能直接产生 HumanDisposition 或 Verdict。

## 12. 规则—反例—非声明矩阵

| 冻结规则 | 反例夹具 | R1 不得声称 |
| --- | --- | --- |
| 精确坐标与内容身份分离 | 两个 commit 指向逐字节相同 subtree | 相同内容就是同一交付坐标 |
| Profile 与 Provider identity 分离 | 两个 Provider 实现同一 Profile 并产生同一 FactSet | Provider 相同才是同一事实 |
| 快照 inventory 与语言覆盖分离 | Python + TypeScript 混合 root，首版只支持 Python | Python 全绿即仓库全绿 |
| 工作树不替代 Git 快照 | exact tree 外存在 `__pycache__` 和 ignored file | 目录遍历结果就是提交内容 |
| Fact 必须有直接源码锚 | Analyzer 只给出“可能拥有资源”的解释 | 推测是结构事实 |
| 外部目标与不存在分离 | import target 位于分析 root 之外 | 当前子图没目标即世界中无目标 |
| 来源组合显式 | A 为空、B 有事实，或 A/B 冲突 | A 成功/为空取消 B |
| 分母具有 provenance | parse failure 后只数成功文件 | 较小子集的 100% 是全局 100% |
| bounded execution 与 coverage 分离 | 深度预算耗尽但执行正常结束 | process success 等于完整关系图 |
| wall timeout 不生成普通确定性切片 | 同输入在快慢机器上超时时成员集合不同 | timeout partial 可稳定复算 |
| overlap 不重复扩大覆盖 | 同一 Fact 出现在五个 Slice | 覆盖了五个不同 Fact |
| 核验快照与消费快照连续 | 验证后 path 被替换 | 两次各自安全读取保证组合身份 |

## 13. 首个 Reference Lab

首个实验固定在本合同基线的：

```text
repository: NoctilumeDev/VeriTrail
commit:     9ab64121350b69ce81e6be79961ad426026bbc39
root:       plugins/github-evidence/src/veritrail_github
tracked ordinary Python blobs: 22
total blob bytes:              259553
language profile:              Python source 3.10
```

它只验证：

```text
module entity and class/function/method/import declaration facts
LEXICAL_CONTAINS and IMPORT_TARGET_LITERAL relations
bounded overlapping slices
staged coverage and truncation
deterministic identities across supported Python runners
```

至少还要有独立合成夹具证明：

1. branch alias 在解析后移动，不改变已建立的 SourceSnapshot；
2. 同一路径内容在核验后被替换，派生仍只消费已拥有的快照；
3. 来源 A/B 叠加、A 为空/B 有事实和 A/B 冲突均保留正确 provenance；
4. 图边位于 expansion bound 之外时，execution 可完成而 coverage 为 partial；
5. Python/TypeScript 混合 root 不会被报告成 repository complete；
6. CPython 3.10/3.13 原始 AST 差异不会改变首个 Profile 的规范化输出；
7. Python 3.13-only 语法不会因运行于 3.13 而进入 Python 3.10 Profile；
8. 同一输入重复执行以及双 Python normal/`-O` 的 Fact、Relation、Slice 与 Coverage 摘要一致。

Reference lab 不执行或 import 待审模块，不访问网络，也不把该插件包的结果外推为所有 Python 项目事实。

## 14. 包与依赖边界

未来 R1 实现必须位于独立 Review Attention 产品边界，不能进入 Core 或 `plugins/github-evidence`。
Core、P 插件和 Workbench 不得因 R1 增加默认运行或安装负担。

R1 可以遵循 `veritrail-json-c14n/1` 的公共规范与数据型 conformance vectors，但不得为省事导入 Core
私有 canonicalization、Evidence importer 或 P 插件 validator。共享规范/夹具不等于共享实现：

```text
R implementation A --\
                     +-> same public conformance corpus
R implementation B --/
```

是否以单独 package、可选 extra 或仓库内部工具发布，属于后继打包合同；本文不创建空 package 骨架。
R5 的可选 Core handoff adapter 也不得提前进入 R1。

## 15. 候选合同验收门

本合同只有满足以下条件后才有资格冻结：

1. 精确绑定已冻结 Pattern Corpus source commit、manifest digest 与四条 selected revision；
2. R 轨 Plan、R0 Contract、Corpus、README、AGENTS 与 milestones 对 R1 0.1 范围没有竞争定义；
3. `SourceSnapshot -> Facts -> Relations -> Slices -> CoverageLedger` 五层身份、权威和失败语义可逐层解释；
4. 规则—反例—非声明矩阵覆盖 source composition、coverage、coordinate staleness 与 snapshot continuity；
5. 文档链接、Markdown 和既有全仓门禁保持成立；
6. diff 仅包含 R1 合同与状态入口文档，不出现 R 轨 Schema、源码、CLI、CI、标签或 Release；
7. 候选通过受保护主线合入，从新的 exact main 完成 README 与本文的匿名公开读回；
8. 后继独立 docs-only 状态发布完成自己的门禁、合入和读回后，才允许写：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_DRAFTING_ALLOWED
R1_IMPLEMENTATION_NOT_STARTED
```

即使合同冻结，Schema 字段、枚举、canonical bytes、path 可逆编码、源码锚端点、遍历 tie-break、预算
inclusive 规则和 Artifact 文件布局仍须另行冻结。Schema 实现不得替这些问题作决定。

## 16. 当前候选事实

本补丁只把 R1 pre-contract audit 的结论整理成合同候选，并同步用户入口与工程状态。它没有创建任何
R1 Schema 或运行能力，也没有把审计发现写成已验证实现事实。

当前状态保持：

```text
R1_CONTRACT_CANDIDATE
R1_SCHEMA_NOT_STARTED
R1_IMPLEMENTATION_NOT_STARTED
```

新的反例仍高于已有文档一致性。若合同在冻结前被反例击穿，只重开受影响的最小语义边界，不以“已经
写完”或“门禁全绿”为由继续施工。
