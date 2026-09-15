# R1 Multi-Provider Fact Composition 冻结后下一闭环系统审计

> 状态（本文最后门全部成立后）：`R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN /
> R1_RELATION_DERIVATION_PRECONTRACT_AUDITED /
> R1_RELATION_DERIVATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@3575cc90faffd41c7172339f461c583e748f2215`
>
> 上游冻结事实：[R1 Multi-Provider Applicability / Fact Composition 实现冻结发布](163-r1-multi-provider-fact-composition-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改 Schema、corpus、
> identity vector、源码、测试、依赖、CI、Provider、parser、publisher、Relation、Slice、Coverage、Manifest、
> CLI、Workbench、Core、P/Q/D、tag 或 Release

## 1. 审计问题与停止线

Multi-Provider Fact Composition 已经证明多个 closed test Provider 可以在同一预算世界中形成稳定的、
conflict-bearing、private、non-published FactSet construction state，并能保留完整 ProviderRun 与 final Evidence
projection 所需的运行事实。它没有回答 Relation 由谁派生、消费哪一个 exact FactSet、怎样取得 provenance，
也没有授权任何 Relation/Slice/Coverage 或文件发布。

本轮只问：

> Fact composition 之后，哪一个尚未冻结的接缝已经成为最多后继能力共同依赖、且最容易被 parser、Slice、
> Coverage 或 publisher 实现反向替合同作决定的 authority bottleneck？

本轮比较 `DIAGNOSTIC publisher`、real parser/public Provider boundary、Relation derivation、Slice、Coverage 与
COMPLETE publisher。选择一个候选只允许下一步从新 exact main 起草独立 docs-only 合同；不产生 Schema 或
runtime 实现授权。

为避免先形成“Relation 应该下一步”的叙事再回头寻找理由，候选统一按以下五项比较：

1. 是否被两个以上正常后继共同消费；
2. 若不先冻结，后继实现是否必须替合同选择 authority、identity 或 failure semantics；
3. 是否可以独立闭环，而不要求同时建立 public product surface；
4. 是否已有足够冻结输入构造单变量反例；
5. 候选即使先完成，是否仍会把同一个未决问题原样留给下游。

候选不会因为位于架构图“下一格”、实现较容易或已有 fixture 就自动胜出。第 4.1 节还明确记录使本轮选择失效
的反证条件；后继 Agent 若观察到其中任一条件，必须重开本审计结论，而不是继续维护既有叙事。

## 2. 冻结输入与当前实现坐标

审计开始时的关键文件 SHA-256 为：

```text
cdf948e44bd7d57b78bdaffbaf949af8df61d22d5ebe972c8864cbbf79fe32f0  docs/113-r1-deterministic-semantic-slice-contract.md
86b02ac5717190f7e12c720257ab6c46b996f427e048f19d1e631ad92b4bc8b3  docs/120-r1-schema-and-canonical-identity-contract.md
c64370e2f4faa5b7ae44b6872d5d5485b69b8f9fe54bb0b597abb4e4a890ecac  docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md
e70bdde807fcb1795bdca8e49d04c664024495b7e3f76ec4c696fc4ea48e8834  docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md
5287e7f74727b63f2daba9fd1afef8795dabc8235d131ce0d1a7c3b68f203ee5  docs/160-r1-multi-provider-applicability-and-fact-composition-contract.md
1960de4b966ea934060a100e92b365bcc9384a0c261ce9fbc4009778dd1d5ab0  docs/163-r1-multi-provider-fact-composition-freeze-publication.md

a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045  schemas/review-derivation-evidence-0.1.1.schema.json
e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1  schemas/review-fact-set-0.1.schema.json
397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744  schemas/review-relation-set-0.1.schema.json
e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545  schemas/review-coverage-ledger-0.1.schema.json
69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91  schemas/review-derivation-manifest-0.1.schema.json

62933f560f2df275bdde5097ba7bc8a292962a7125c6a4f2988fdcda34176559  plugins/review-attention/src/veritrail_review/_execution_cell_application.py
d742fd5c48a250948031ee27610b9960510b7d89530ac48b3f3bb8f40711879e  plugins/review-attention/src/veritrail_review/_execution_cell_values.py
48636e52e1e2b5ecef60f517f3273fb58536d1f52a043cbb34bee0fc2b5dcab5  plugins/review-attention/src/veritrail_review/_multi_provider_fact_composition.py
d736d87d038855c810102544bbbeeeb51cdf0765c82a01d70023e7e6ff87f84d  plugins/review-attention/src/veritrail_review/_multi_provider_values.py
```

当前实现事实继续是：

- Provider worker terminal envelope 只携带 `canonical_facts`；没有 relation candidate 或 relation recipe；
- `OwnedExecutionCellPhaseResult` 虽有 `reported_relation_ids`，当前所有合法路径都固定为空；
- multi-Provider controller 只组合 Facts/FactConflicts，并明确拒绝 child phase 报告 Relation ID；
- private result 没有 RelationSet、Relation continuation phase、output path、writer 或 Manifest authority；
- 公共 Schema 与 valid-complete fixture 已能描述 RelationSet 和非空 `reported_relation_ids`，但 shape 与样例不
  证明谁有资格生产这些值。

本轮没有证据要求改写已经冻结的 Fact/FactSet identity、multi-Provider applicability、BudgetContext、
FactConflict 或 existing Schema bytes。发现 Relation producer 接缝不等于这些冻结对象已经错误。

## 3. 当前组合边界后的依赖图

```text
SourceSnapshot + sealed ReviewPolicy + DerivationProfile
                         |
                         v
        applicable Fact Provider runs under one BudgetContext
                         |
                         v
          stable multi-source FactSet + FactConflicts
                         |
             unresolved authority seam
                         |
                         v
          Relation candidates / resolution / admission
                         |
                         v
              stable RelationSet + conflicts
                         |
                         v
             ReviewSliceSet -> CoverageLedger
                         |
                         v
          final DerivationEvidence + COMPLETE publication
```

DIAGNOSTIC publication 从 non-success branch 横向离开；real parser 进入上游 Fact producer boundary；Slice、
Coverage 与 COMPLETE publisher 位于 RelationSet 之后。当前共同瓶颈不是“怎样遍历图”，而是 Relation 图在
进入遍历前由谁、针对什么 exact input、以什么 provenance 产生。

## 4. 候选接缝比较

| 候选 | 已冻结基础 | 仍缺的语义 | 反向约束 / 下游依赖 | 当前裁决 |
| --- | --- | --- | --- | --- |
| DIAGNOSTIC output coordinate / publisher | 四文件 Manifest shape、one-shot eligibility、预算与 create-new 原则 | exact output coordinate、writer、原子四文件 publication | 关闭失败留档；不建立 normal Relation 输入 | 合法且正交；延期 |
| real parser / public Provider boundary | Python 3.10 Profile、anchor/encoding 规则、private applicability model | 真实 source bytes 输入、parser diagnostics、public authorization/SPI | 可严格收窄为 facts-only，并不必然固化 Relation API；但完成后仍未回答 Relation producer 与 composite FactSet continuity | 合法独立后继；不是本轮共同瓶颈 |
| Relation derivation authority + exact operand continuity | FactSet、Relation Schema、relation kinds、ProviderRun shape、shared budget | producer authority、exact FactSet operand、run/report provenance、最小 upstream eligibility gate | 同时约束 Evidence truthfulness、RelationSet 输入与后继 Slice/Coverage；不要求本合同包办完整 Relation 算法或 UNKNOWN 账册 | **下一问题面** |
| ReviewSliceSet | BFS、inclusive budgets、frontier、conflict 时空 Slice | 只缺 RelationSet 上的执行与 admission | 必须消费已闭合 RelationSet；不能决定 Relation 来源 | 延期 |
| CoverageLedger | 七阶段、typed gaps、KNOWN/UNKNOWN denominator | 需要每一上游阶段的 candidate universe 与 terminal disposition | 是保守消费者，不应倒推 producer/denominator | 延期 |
| COMPLETE publisher | 八文件 Manifest、create-new/atomic 原则 | 所有 normal Artifact final bytes 与 cross-reference | 位于全链出口 | 明确过早 |

### 4.1 反证条件与结论失效传播

本轮选择不是不可推翻的路线承诺。以下任一新证据成立时，`Relation derivation authority + exact operand
continuity` 不再自动拥有下一合同资格：

| 反证 | 直接失效的结论 | 必须重查的下游文本 |
| --- | --- | --- |
| 已冻结合同其实已经唯一指定一个能在 composition 后消费 exact FactSet、并诚实报告 Relation 的 producer/run 模型 | “producer authority 尚未冻结”失效 | 本文第 5–8 节、README、AGENTS、milestones |
| application 可只做既有冻结规则的机械 canonicalization，且现有 Schema 能不虚构 Provider 报告地表达其独立 provenance | application 模型的 provenance blocker 失效 | 第 5.4、6、7 节与候选排序 |
| 任何 private closed-test Relation proof 都必须先取得 public Provider authorization，无法以内部边界隔离 | public Provider boundary 的延期裁决失效 | 第 4、5.10、6、9 节 |
| conflict-bearing FactSet 在任何 Relation producer 选择前还需要一个独立、可闭环的 upstream eligibility 合同 | 本轮选定范围仍过大 | 第 5.6–5.8、6、8 节；下一步应改为该更窄合同 |
| Relation 不被 Slice、Coverage 或 final Evidence 消费，或存在无需 RelationSet 的冻结后继路径 | “共同瓶颈”判断失效 | 第 3、4、5.10 与 milestones |

本次反查没有找到上述证据。相反，冻结文本明确保留了 producer/run 来源、composite FactSet operand 与
conflict-bearing continuation 的未决状态。因此审计可以选择这个问题面，但不能把选择升级成 producer 模型、
Schema 版本或实现顺序的冻结。

## 5. 审计发现

### 5.1 当前 runtime 与完整 fixture 对 Relation 来源给出不同层级的事实

冻结的 valid-complete fixture 让一个 `python-ast` ProviderRun 同时报告 Fact 与 Relation：

```text
ProviderRun.reported_fact_ids      = non-empty
ProviderRun.reported_relation_ids  = non-empty
Fact.provenance_refs               = [that ProviderRun]
Relation.provenance_refs           = [that ProviderRun]
```

当前 runtime 则只允许：

```text
worker -> canonical_facts
phase  -> reported_fact_ids
phase  -> reported_relation_ids = []
```

两者不构成已经冻结的实现矛盾，因为 fixture 只证明完整 Schema/identity 可表达一种合法 Bundle，而当前 runtime
只实现更窄的 Fact phase。但它们共同证明 Relation producer contract 尚不存在：不能从“Schema 有字段”推出
“当前 Provider 已报告 Relation”。

### 5.2 `IMPORT_TARGET_LITERAL` 必须消费组合后的 exact FactSet

该 Relation 的 target 不只复制 import Fact 的 literal：它还可能携带
`RESOLVED / UNRESOLVED / UNSUPPORTED / CONFLICT`、topology 与 `resolved_fact_ids`。这些值依赖完整 module Fact
universe 与 sealed `python_module_mapping`。

在 multi-Provider world 中，一个 fact-producing child 只看见自己的 run-local candidates。它不能在其他来源
完成前证明 composite FactSet 中是否存在零个、一个或多个 module candidate。因此：

```text
run-local Fact Provider view
  !=
composed FactSet resolution world
```

让原 Fact Provider 在首次 terminal envelope 中同时给出最终 resolved import Relation，会把未观察到的其他来源
当成不存在，或要求 Provider 偷偷拥有 composition authority。

### 5.3 若 Relation 是第二阶段能力，现有 operands identity 没有绑定 FactSet

公共 Provider operands 投影当前绑定 Snapshot、Policy/Profile 与 Provider descriptor，但不含
`fact_set_digest`。这对 Fact producer 足够；对消费 composite FactSet 的 Relation phase 不足以单独证明 exact
operand continuity。

因此不能直接复用现有 `provider_run_id` 公式并声称“Relation Provider 已绑定 exact FactSet”。下一合同必须裁决：

- Relation 是否是独立 Provider run/capability；
- 若是，FactSet identity 怎样进入可复算 operands/run provenance；
- 是否需要版本化 Evidence/Schema correction；
- 还是存在另一种不虚构来源、且不把可替换语义硬编码进 application 的模型。

本审计不把这些问题偷塞进当前 `0.1.1` Schema，也不预先选择新版本号。

### 5.4 若 Relation 由 application 直接生成，provenance 与 replaceability 仍未闭合

application 可以机械复算 `relation_subject_digest / relation_id`，不等于它自动获得 Relation 事实生产权。
若直接把输入 Fact 的 ProviderRun 引用复制到 Relation：

- 这些 ProviderRun 没有实际报告 Relation；
- `reported_relation_ids` 若仍为空，Relation 的反向 provenance 无法闭合；
- 若事后把 Relation ID 填回原 run，Evidence 会把 application 后处理冒充成 Provider 报告；
- 若不记录任何 run，Relation Schema 的非空 provenance 无法满足；
- 若把算法永久写进薄 application，又可能违反可替换 capability 不进入 semantic core 的 R0 边界。

因此：

```text
deterministic derivation
  !=
unowned derivation
```

算法可复算不能替代 producer authority 与 provenance。

### 5.5 同一 Provider 的“两段运行”不能共用一个既有 run identity

现有 `provider_run_id` 绑定 `(derivation_id, capability_id, provider_id, operands_digest)`，同一 derivation 中
`(capability_id, provider_id)` 必须唯一。若同一个 Provider 先生成 Facts，待 composition 后再生成 Relations：

- 复用 run ID 会把两个不同 operand/time boundary 压成一次运行；
- 创建第二个同 identity run 会违反唯一性；
- 靠内部隐藏 resume state 会破坏 terminal envelope 与 retry/continuity 规则；
- 修改 capability identity 则必须由 sealed requirement 与 applicability authority 支持，不能由实现临时命名。

所以“让原 parser 再跑一下”不是无害实现细节。

### 5.6 FactConflict 对 Relation 启动资格的影响尚未有唯一裁决

已冻结规则只保证 FactConflict 不被挑 winner，并要求最终存在任一 Fact/Relation conflict 时
`ReviewSliceSet.slices=[]`、Slice denominator `UNKNOWN`。它尚未唯一决定 Relation phase 本身应当：

```text
A. FactSet 有任一 conflict -> RelationSet relations=[]，只保留 upstream uncertainty
B. 只为 conflict-free subjects 派生局部 Relations
C. 为全部 candidate 派生 Relations 并建立 RelationConflict
D. 形成另一种 typed non-success / no-RelationSet state
```

四种做法会产生不同 RelationSet、Evidence reported IDs、Coverage denominator 与 COMPLETE eligibility。Relation
实现不能自行选择。下一合同至少要决定哪些 upstream state 允许启动 Relation phase、哪些必须停止；它不必
同时冻结局部 conflict isolation、完整 RelationConflict composition 或 Coverage 的全部传播算法。局部 conflict
isolation 明确属于未来独立能力，首个合同不得在没有证明时偷用 B。

### 5.7 upstream UNKNOWN 不能在 Relation 边界退化为空集合

required Fact source non-success 已经禁止 normal FactSet；optional source non-success 允许 normal FactSet，但后继
Coverage 必须保留来源缺口。进入 Relation 时至少要区分：

```text
known empty relation universe
known relations over an explicitly bounded FactSet
unknown global relation denominator caused by upstream source gap
relation derivation execution failure
relation resolution UNRESOLVED / UNSUPPORTED / CONFLICT
```

`relations=[]` 本身无法表达这些区别。若下一层只返回空数组，Coverage 会被迫把 UNKNOWN 缩成较小 KNOWN，或把
未解析 target 错写成“没有 edge”。下一合同只需先冻结 Relation phase 的输入资格与终态 envelope 如何保留这种
差别；CoverageLedger 的完整 UNKNOWN denominator 投影仍属于后继合同。

### 5.8 Relation conflict 与 Fact conflict 不能共用一个模糊状态

Fact conflict 表示同一 Fact subject 的不兼容 candidate；Relation conflict 表示同一 edge slot 的 kind/target
分歧；import target 的 `resolution_status=CONFLICT` 又表示一个 Relation 内存在多个确定性 module target。
三者可同时出现，但身份、candidate 与 downstream 含义不同：

```text
FactConflict
  != RelationConflict
  != IMPORT target resolution CONFLICT
```

下一合同必须固定它们的构造顺序与传播规则，不能用一个 `has_conflict` boolean 抹平。

### 5.9 Shape、canonical bytes 与 producer authority 仍是三件事

`review-relation-set-0.1.schema.json`、identity vectors 与 valid-complete fixture 已冻结 Relation 的字段、排序、
摘要和一个兼容样例。它们不能证明：

- 哪个组件有权创建 Relation candidate；
- candidate 怎样针对 exact composite FactSet 运行；
- Provider/application 怎样分配 provenance；
- FactConflict 或 optional-source gap 怎样改变 Relation eligibility；
- Relation phase 失败怎样进入 final Evidence；
- 当前 runtime 已能建立 RelationSet construction state。

因此本轮不修改 Schema，也不把旧 fixture 当作 runtime authorization。

### 5.10 其他候选仍然真实，但不是当前共同瓶颈

- DIAGNOSTIC publisher 可独立关闭失败留档，不决定 normal graph；
- real parser 可以严格实现为 facts-only，不必等待 Relation；但它完成后仍不能替 Relation 决定复合输入与
  provenance，因此不是多个后继共同卡住的接缝；
- Slice 已有 deterministic BFS 规则，但没有稳定 RelationSet 就没有合法图输入；
- Coverage 必须记录 upstream truth，不能为得到数字反向定义 Relation candidate universe；
- COMPLETE publisher 必须等待 Fact/Relation/Slice/Coverage 与 final Evidence 同时闭合，不能用 placeholder 先行。

## 6. 选定的下一问题面与最小合同上限

下一步从本文最终合入后的新 exact main 起草一个独立 docs-only：

```text
R1 Relation Derivation Authority and Operand Continuity Contract 0.1
```

合同的最小闭环只应回答：

1. Relation candidate 的 producer authority 属于谁，为什么不违反 R0 的 replaceable-capability 边界；
2. Relation phase 消费的 exact input 是哪些 owned values，特别是怎样绑定 composite `fact_set_digest`；
3. Fact producer、Relation producer、application canonicalizer 与 RelationSet admission 各自拥有哪一步；
4. Relation producer 是否形成独立 ProviderRun；若形成，capability requirement、descriptor、operands 与 run identity
   怎样版本化；
5. 若不形成独立 ProviderRun，Relation provenance 与 `reported_relation_ids` 如何不虚构来源并保持双向闭包；
6. conflict-free FactSet、conflict-bearing FactSet、optional-source gap 与 absent normal FactSet 四种输入状态，哪些允许
   Relation phase 启动，哪些只能保留 upstream uncertainty；
7. Relation run/phase 的 success、empty success、nonconformant output、failure、unavailable 与 budget stop 怎样形成
   private terminal envelope，而不提前发布；
8. 哪些结果最多形成 private、copy-owned、non-published continuation；
9. 现有 Schema/Evidence 版本是否足够；若不够，只重开被反例证明无法表达的最小字段/版本边界；
10. 当前合同明确不授权 real parser、public SPI、完整 RelationSet composition/admission、Slice、Coverage、publisher
    或完整 Derivation。

下列问题必须被记录，但只有证明它们与上述 authority/operand 闭环不可分时才进入同一合同：

- `LEXICAL_CONTAINS` 与 `IMPORT_TARGET_LITERAL` 的完整 candidate universe 和 import zero/one/many resolution；
- Relation admission、same-ID merge、RelationConflict 与三类 conflict 的完整构造/传播；
- final DerivationEvidence、Coverage UNKNOWN denominator 与 COMPLETE eligibility；
- real parser/public Provider authorization 与完整 RelationSet publisher。

若 fresh-Agent 合同审查证明其中任一项可以形成更窄前置闭环，必须再次缩小范围，不能因为本文列过就全部纳入。

该合同即使冻结，也最多授权 closed deterministic Relation producer execution boundary 与 private terminal
continuation；是否同时授权 Relation admission 必须由合同阶段的最小性证明决定。它不能自动授权真实 Python
parser、public Provider discovery、完整 RelationSet composition、ReviewSlice、CoverageLedger、
DIAGNOSTIC/COMPLETE publisher、CLI 或 Workbench。

## 7. 候选 producer 模型不能由本审计预选

| 候选模型 | 当前优点 | 尚未闭合的反例 | 本轮裁决 |
| --- | --- | --- | --- |
| Fact Provider 在同一 terminal 中同时报告 Relations | fixture shape 直观 | 在 multi-Provider composition 前看不到 final FactSet；import resolution 可能错误 | 未授权 |
| composite FactSet 后启动独立 Relation Provider run | operand/provenance 边界清楚 | 现有 operands/run identity 未绑定 FactSet；需 sealed capability/applicability 与 shared-budget continuation | 合同候选需审议 |
| application 直接机械派生 Relations | 可避免第二个外部执行 | provenance/reporting 易失真；可替换语义可能倒灌薄 application | 合同候选需审议 |
| Fact Provider 先输出 relation recipe，application 后解析 | 可延迟 target resolution | recipe 不是冻结 Artifact/candidate identity，新增隐藏对象 | 未授权 |

下一合同可以证明其中一种模型成立，也可以在新反例下提出更窄模型；但不能通过已有代码便利性或 fixture 外观
直接选定。

## 8. 最小反例矩阵

| # | 单变量反例 | 错误推理 | 必须保持的裁决 |
| ---: | --- | --- | --- |
| 1 | valid fixture 的 run 有 relation IDs，runtime run 没有 | Schema 有字段，所以 runtime 已支持 Relation | shape 不授予 producer authority |
| 2 | Provider A 的 import target 只由 Provider B 报告 | A 可在自己的 terminal 中最终解析 import | resolution 必须消费 composite FactSet |
| 3 | Relation phase 更换 FactSet，其他 inputs 相同 | 原 operands digest 相同，所以输入相同 | Relation operand identity 必须绑定 exact FactSet |
| 4 | 同一 Provider 以同 run ID 先报 Fact、后报 Relation | 同一个实现就是同一次 run | 不同 operand/terminal phase 不能共用运行身份 |
| 5 | application 生成 Relation，却回填到 Fact Provider reported IDs | deterministic 后处理可归因给上游 Provider | 禁止虚构 Provider 报告 |
| 6 | application 生成 Relation 且 provenance 为空 | application 是可信的，所以无需来源 | Relation 必须有合法可复算 provenance |
| 7 | required source 不可用、另一来源有 Fact | 对已知 Fact 派生 RelationSet | 没有 normal FactSet，不能建立较小 normal Relation world |
| 8 | optional source 不可用、required sources 成功 | overall COMPLETED，所以全局 Relation denominator KNOWN | optional gap 必须继续可见 |
| 9 | FactSet 有 conflict，Relation 任选 candidate | Relation 只是在建图 | Relation 不拥有 Fact conflict 裁决权 |
| 10 | conflict-free component 可独立成图 | 不受影响，所以首版自然支持局部遍历 | 没有 conflict-isolation contract 就不得外推 |
| 11 | import 无 target candidate | relations=[] 表示没有依赖 | 保留 UNRESOLVED/UNKNOWN，而不是 edge absent |
| 12 | import 有两个 module candidate | 任选规范排序第一个 | 单 Relation target status CONFLICT，保留全部 candidate IDs |
| 13 | 两来源给同 edge slot 不兼容 target | 合并为 import resolution conflict | RelationConflict 与 target-level conflict identity 分离 |
| 14 | Relation producer success empty | 没有 Relation，所以 phase 缺失 | empty success 与 unavailable/unknown 分开 |
| 15 | Relation phase deadline 命中 | 保留此前已生成 relation prefix | terminal stop 不发布 normal RelationSet |
| 16 | Relation failure 后把 FactSet 单独发布 | 上游 Fact 已完成 | COMPLETE 固定八文件，禁止 partial normal bundle |
| 17 | Slice 需要图，先在 Slice builder 内补 Relation | 只是内部 helper | Slice 不能取得 Relation producer/admission authority |
| 18 | Coverage 需要 denominator，按已生成 Relations 计数 | observed set 就是候选全集 | candidate universe UNKNOWN 不得缩成较小 KNOWN |
| 19 | facts-only real parser 可以独立实现 | parser 必须等 Relation 合同 | 两者可并列；parser 不得顺便固定 Relation authority |
| 20 | DIAGNOSTIC publisher 已完成 | 失败能留档，所以 Relation 前置已闭合 | failure publication 与 normal graph 正交 |

## 9. 本轮不改的边界

- SourceSnapshot、DerivationInputSet、Fact/FactSet、FactConflict 与 multi-Provider composition identity 不变；
- 现有 Schema、corpus、identity vectors、valid-complete fixture 与 digest bytes 不因审计自动升级；
- 所有后继阶段继续消费同一个 BudgetContext 与 absolute deadline，不从 Relation 刷新预算；
- real parser 的 source encoding、partial AST、public authorization/SPI/discovery 继续延期；
- DIAGNOSTIC publisher 与 output coordinate 继续作为正交后继；
- ReviewSlice 的 BFS、inclusive budget、frontier 与 conflict isolation 不在本轮实现；
- CoverageLedger 只消费上游事实，不获得补造 candidate universe 的权力；
- COMPLETE 继续固定八文件；不增加 partial/Fact-only/Relation-only Manifest outcome；
- R2–R6、Q、D、Agent integration、JPyxis、Server/Cloud、并发和分布式能力不进入本闭环。

## 10. 本地审计证据

本轮从 clean independent worktree
`docs/r1-post-composition-next-closure-system-audit@3575cc90faffd41c7172339f461c583e748f2215` 完成：

1. 读取 `README.md`、`AGENTS.md`、文档 00–03、85、86、88、113、120、150、155、159、160、163；
2. 复算第 2 节关键合同、Schema、fixture 与 implementation 文件 SHA-256；
3. 审计 RelationSet、CoverageLedger、DerivationEvidence 0.1.1 与 Manifest 的真实字段和 cross-reference；
4. 审计 valid-complete fixture 中 Fact/Relation/ProviderRun 的双向 provenance；
5. 审计 execution-cell terminal envelope、phase value 与 multi-Provider result 的真实 runtime surface；
6. 建立第 3–8 节依赖、候选、authority 与反例矩阵。

本轮不新增 runtime probe。结论来自冻结 Artifact、fixture 与当前实现 surface 已存在的组合反例；为增加审计数量
而制造无关运行不能提高结论强度。

本地适用门在第一次执行即通过：

```text
Markdown relative links / fences / local-path scan / diff scope / git diff --check
  -> PASS

Review R1 Schema + identity + DerivationEvidence 0.1.1
  Python 3.10 normal / -O -> 27 / 27, 27 / 27
  Python 3.13 normal / -O -> 27 / 27, 27 / 27

Execution Cell protocol + Fact/Evidence closure + multi-Provider Fact composition
  Python 3.10 normal / -O -> 55 / 55, 55 / 55
  Python 3.13 normal / -O -> 55 / 55, 55 / 55
```

四组测试开始前都确认 Core、Review plugin 与 plugin test module 的实际导入坐标位于本 worktree；没有借用其他
editable install。上述结果只证明 docs-only 审计没有暗改冻结行为，不替代本文自己的远端门和公开读回。

## 11. 本审计自己的门与下一步

本文只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过：

1. Markdown relative links、fence/heading、状态 marker、敏感/本机路径与 `git diff --check`；
2. exact diff scope 与零 Schema/source/test/runtime change；
3. 当前 worktree 绑定下适用的 R1 Schema/identity/Evidence/composition focused regression；
4. 原始远端 required checks、受保护主线合入与新 exact-main Public CI / Browser Smoke；
5. README、本文与 milestones 的 R1 专属 fresh anonymous installed-product readback。

只有上述最后门全部成立，本文的审计状态才成为主线事实。随后唯一合法下一步是从新的 exact main 先复核第
4.1 节反证条件，再起草第 6 节 docs-only Relation Derivation Authority / Operand Continuity 合同；不得从本
审计直接开始 Schema correction 或 runtime。

若合同审查证明当前 Evidence/Schema 无法表达一个不虚构 provenance 的合法 Relation producer，必须只重开被该
反例击穿的最小版本化边界。不得为了保住 `0.1/0.1.1` 而让 Provider 背书未报告的 Relation，也不得因为新版本
更方便而无反例重写冻结 bytes。

## 12. Fresh-Agent 交接

新的、没有聊天上下文的 Agent 必须先读文档 113、120、150、155、159、160、163 与本文，然后回答：

```text
current frozen input:
  private multi-Provider Fact composition

selected next contract:
  Relation derivation authority / exact FactSet operand continuity /
  minimum upstream eligibility gate

current authorization:
  docs-only contract drafting after this audit's final gates

not authorized:
  Schema/runtime implementation
  real parser or public Provider SPI
  full RelationSet composition/admission
  publisher / Manifest
  ReviewSlice / CoverageLedger
  full Derivation
```

它还必须沿用以下施工纪律；这些是决策方法，不是要求维护上一段聊天的叙事：

1. 先 fetch 并记录 `origin/main` 的 exact SHA、当前 worktree/branch、dirty state 与并行 open PR；旧聊天、旧
   `origin/main`、旧 editable install 和旧测试结果都不能替代当前坐标；
2. `AGENTS.md`、冻结合同、Schema/fixture、实现、测试与远端事实是 source of truth；聊天总结只作为待复核索引；
3. 先平铺候选、反例与失效条件，再选一个最小闭环；不得先写结论后补理由，也不得为了“继续施工”解释掉矛盾；
4. 新证据击穿前提时，必须沿引用关系检查 README、milestones、AGENTS、合同、测试与状态 marker 的下游失效，
   不能只改最后一句；
5. 一次只推进一个合同/实现闭环。发现真实合同冲突立即停实现；未被当前闭环授权的 parser、publisher、
   RelationSet、Slice、Coverage、Q/D/JPyxis 等不顺手施工；
6. `shape != authority`、`path != snapshot`、`context != state`、`memory != truth`。证据身份或 provenance 不匹配时，
   即使技术路径通过也必须作废；
7. 状态只能在该阶段自己的 focused/local gates、原始远端 gates、受保护合入、new exact-main gates 与专属公开
   readback 成立后提升；不得借用上一个阶段的绿色结果；
8. 测试必须绑定当前 worktree 的 source/test coordinate；fresh-interpreter/clean-wheel 边界用真实隔离世界证明，
   不用当前解释器缓存手术模拟；
9. 第一次失败必须保留并先分类为 product、test-harness、environment、tool restriction、capacity 或 evidence
   incomplete；允许有依据地复验，不得用后续绿色结果抹去首次事实；
10. 测试失败先比较“合同实际承诺”与“断言实际要求”。测试若偷加了 byte identity、时序、完整性或 authority
    claim，应修测试模型，不能让生产代码迎合一个更强但未授权的世界；
11. 当前 16 GiB Windows 宿主上的重型矩阵、Chromium 与 clean-environment gate 串行执行；资源压力不是产品失败，
   也不能成为放宽不变量的理由；
12. 恢复上下文时先读完整 `AGENTS.md` 与最新审计，再只沿引用读取必要冻结文档；除非发现矛盾，不重新考古
    整个仓库，也不重复叙述已经冻结的历史；
13. 报告知道的事实、保留不知道的部分。发现裂缝不等于必须修改；只有反例使冻结不变量或候选合同无法同时
    成立时，才最小重开。

新 Agent 的第一轮只能完成重新绑定、读取与第 4.1 节反证复核，然后起草 docs-only 合同候选；不得在同一轮
借审计结论直接写 Schema 或 runtime。若复核推翻本文选择，应先提交新的审计修正，而不是悄悄改题。

当前分支只能写：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_SYSTEM_AUDIT_CANDIDATE
R1_RELATION_DERIVATION_CONTRACT_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

`candidate` 不能被 README、PR 文案或本地绿灯提前提升为 `PRECONTRACT_AUDITED`。新的语义反例仍有否决权；
发现风险不自动要求修改，只有使冻结不变量或候选合同无法同时成立的反例才触发最小重开。
