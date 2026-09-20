# R1 Declared Relation Observation Domain / Composition Qualification 最小合同 0.1 候选

> 状态：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_CANDIDATE /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 前置审计闭合与首份候选起草基线：`main@559bf9b9a052f0b542227b1cea069dd15c696cc8`
>
> 当前重资格候选基线：`main@962251d91bc2695afe984ee47845ac4fe1a80f7e`
>
> 重资格因果：PR #160 原始 head `44caffaa08ab67bcb83760d86bdbad7e30081b6f` 的 Public CI run
> `35530411983` attempt 1 在 Python 3.13 真正执行 450 tests 后 FAIL；该正式首败继续保留。独立维护
> PR #161 修正既有 listener-owner-mismatch fixture 的时间坐标，并经原始 11/11、受保护合入、
> `main@962251d91bc2695afe984ee47845ac4fe1a80f7e` 的 Public CI run `35533373276` attempt 1、11/11 与 Browser Smoke run
> `35533373269` attempt 1、1/1 取得资格。本文语义不因维护改变；当前候选从该 exact main 重新绑定 source state。
>
> 前置审计：[Declared Relation Observation Domain / Composition Qualification 系统审计](173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md)
>
> 冻结输入：[确定性语义切片合同](113-r1-deterministic-semantic-slice-contract.md)、
> [Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Fact Admission / DerivationEvidence Closure 合同](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)、
> [Multi-Provider Applicability / Fact Composition 合同](160-r1-multi-provider-applicability-and-fact-composition-contract.md)、
> [Relation Derivation Authority / Operand Continuity 合同](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)与
> [Relation Derivation 实现冻结发布](172-r1-relation-derivation-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本候选只裁决 private closed-test
> observation responsibility、exact FactSet-derived denominator、required source-set closure、omission accounting、
> explicit per-item fulfillment accounting、multi-source candidate composition 与 qualification identity；不修改 Schema、corpus、identity vector、runtime、
> tests、Provider、parser、publisher、Manifest、CLI、Workbench、Core、P/Q/D/Cu、tag 或 Release。

## 1. 目的与停止线

冻结的 Relation Derivation 能证明一个 exact ProviderRun 在 exact FactSet、真实 parser identity 与共享
`BudgetContext` 下正常结束，并诚实报告自己的 private candidates。它不能证明：

```text
ProviderRun COMPLETED
  -> sealed responsibility domain was fully observed
  -> every required Relation source was observed
  -> every required relation family / operand subject was accounted
  -> RelationSet may be admitted
```

文档 173 的 `RO-000` 已给出反例：Profile 同时列出 `LEXICAL_CONTAINS` 与
`IMPORT_TARGET_LITERAL`，当前 ProviderRun `COMPLETED`，却只报告前一类。本合同只关闭中间的资格层：

```text
exact normal FactSet
  -> predeclared private observation profile
  -> exact Provider responsibility map
  -> FactSet-derived observation items
  -> all required Relation sources terminal
  -> explicit source-local per-item outcomes
  -> application-validated fulfillment accounting
  -> deterministic candidate merge / conflict preservation
  -> private composition qualification result
```

即使后继冻结并实现，这条闭环也只产生 private、copy-owned、non-published qualification state。它不创建
`RelationSet`，不形成 final `DerivationEvidence`，不发布 Bundle，也不授权完整 Python Relation algorithm、
import zero/one/many resolution、public Provider SPI、Slice、Coverage 或 Attention ranking。

这里的 **Declared Relation Observation Domain** 是本次 sealed closed proof 有义务观察的 relation family 与
Fact-backed operand subject 集，不是源码世界里所有可能 Relation 的数学全集。禁止在字段、类型、注释或 UI 中
把它缩写成 `candidate universe` 或“全部关系”。

## 2. `RO-000..007` 的唯一裁决

| Falsifier | 本合同裁决 | 仍禁止的推理 |
| --- | --- | --- |
| `RO-000` Provider 完成但漏一类 | Provider terminal 与 observation qualification 分离；由 application 对预先固定的 item 集逐项对账 | `COMPLETED` 等于看够 |
| `RO-001` A 完成、required B 未运行 | required source-set terminal closure 为 incomplete；不得 composition qualified | A 成功取消 B |
| `RO-002` A `COMPLETED + []`、B unavailable | non-empty assignment 上 A 没有 outcomes，A/B 均未形成 fulfillment closure | `relations=[]` 等于无 Relation |
| `RO-003` A/B 分别覆盖不同 family、无责任图 | responsibility map 缺失时在 Provider 执行前拒绝；terminal 集不能补造 map | 全部 run terminal 自动形成完整域 |
| `RO-004` A/B candidates 各自合法但同 subject 不兼容 | observation 可完整，candidate composition 必须保留 private conflict；RelationSet admission 仍未授权 | candidate validity 足以任选 winner |
| `RO-005` Profile 只列 kind 闭集 | Profile 只提供允许词汇与 rank；本合同的 closed observation profile 才为首个 proof 固定 required families 与 source responsibilities | allowed kind 等于 required observation |
| `RO-006` non-empty exact domain、Provider `COMPLETED`、candidates 为空，但没有逐 item outcome | source-local fulfillment 不成立；每个 assigned item 必须有显式、可验证的 terminal outcome | 已定义 denominator 加空 candidates 等于全部观察 |
| `RO-007` `i1/i2` 中只有 `i1` 有 candidate/outcome，`i2` 没有 outcome | `i1` candidate 可以合法，`i2` 仍是未履行义务；source receipt 不闭合 | 部分合法 candidate 等于整个责任域已观察 |

这些裁决不重开文档 172 的 bounded Relation Derivation。它们只阻止后继把 execution success、observation closure、
candidate agreement 与 Artifact admission 压成一个状态。

`RO-006/007` 把本合同再拆开一层：**responsibility defined != responsibility discharged**。application
不能从“item 已被列入责任域”或“candidate 没有出现”推导 Provider 已经检查该 item。

## 3. 八个对象与 authority 不能合并

```text
DerivationProfile
  冻结 relation-kind 词汇、rank 与 Relation identity 规则

ProviderRequirement
  sealed Policy 中的 capability requiredness 与 CUMULATIVE 组合规则

ObservationProfile
  本合同的 private versioned closed table；选择首个 proof 必须观察的 families 与 subject rule

ProviderResponsibility
  exact Provider descriptor 对哪些 observation items 负责任

ProviderRun
  Provider 在 exact operands 上真实执行和 terminal 的事实

ObservationOutcome
  Provider 对一个 assigned item 作出的显式 terminal 履责记录；与 candidate 数组独立承载并接受双向对账

ObservationReceipt
  application 对该 run 的 assigned items、outcomes 与 candidates 做的机械对账

CompositionQualification
  required source-set、全部 receipts 与 candidate merge/conflict 的 private immutable projection
```

因此：

```text
Profile vocabulary       != required observation families
capability requiredness  != Provider responsibility
responsibility defined   != responsibility discharged
Provider terminal        != per-item outcome closure
per-item outcome         != Relation truth
observation closure      != candidate agreement
composition qualified    != RelationSet admission
private receipt          != CoverageLedger
```

Human Seal authority 仍只拥有 Policy/Profile 选择与 requiredness。Provider 只拥有 bounded candidate observation，
并对自己逐 item 的 terminal disposition 作出显式声明。application 可以按本合同固定的 closed table 建立责任与
对账，但不能自造 Relation、替 Provider 补 negative outcome、修改 Provider candidate、选择冲突 winner 或把 private
qualification 发布成事实 Artifact。`ObservationOutcome` 是履责记录通道，不是独立事实来源：它能让 silent omission
可见，不能证明 Provider 内部认知过程，也不能把 candidate 升级为真值。当前 closed table 不是 public authorization
registry；真实 Provider/publication 以前仍须建立第三方可复核的版本化 authority coordinate。

## 4. 首个 private observation profile

### 4.1 exact Profile 与 capability 前置

首个 proof 只接受：

```text
DerivationProfile
  profile_id      = veritrail-python-source-3.10
  profile_version = 0.1
  relation_kinds  = [LEXICAL_CONTAINS, IMPORT_TARGET_LITERAL]

ReviewPolicy requirement
  capability_id   = review-relation-derivation
  required        = true
  composition_mode = CUMULATIVE
```

Profile 的双 kind 闭集仍不自动产生义务。本合同另固定 private observation profile：

```text
observation_profile_id      = closed-python-import-observation
observation_profile_version = 0.1-test
required_relation_families  = [LEXICAL_CONTAINS, IMPORT_TARGET_LITERAL]
```

该 profile 还必须冻结每个 family 的 subject 规则、candidate cardinality 与 negative-outcome policy。首个 proof 的
两类 item 都是 total obligation：item 只有在对应 Fact 已足以确定一条 bounded Relation 时才会建立，所以规则为：

```text
LEXICAL_CONTAINS
  subject_role             = TARGET_FACT
  subject_fact_kinds       = [IMPORT_DECLARATION]
  candidate_cardinality    = EXACTLY_ONE
  negative_outcome_allowed = false

IMPORT_TARGET_LITERAL
  subject_role             = SOURCE_FACT
  subject_fact_kinds       = [IMPORT_DECLARATION]
  candidate_cardinality    = EXACTLY_ONE
  negative_outcome_allowed = false
```

因此当前 profile 中，非空 assigned item 不能用 `NO_CANDIDATE_OBSERVED` 关闭。未来若某 family 的 truthful
observation 可以得到 closed negative，必须由新的冻结 profile 明确允许该 disposition，并定义它能证明到哪里；
Provider 或 application 不能临场把 candidate 缺席解释成负结论。

首个 implementation profile 不接受 optional Relation requirement。若 sealed Policy 把
`review-relation-derivation` 设为 optional、缺失、重复或改成其他 composition mode，必须在任何 Provider code
运行前拒绝；不得在 runtime 中把它临时提升为 required。未来 optional Relation source 必须显式保存
`optional_observation_gaps`，不能借本合同的 required-only proof 偷渡。

### 4.2 exact 两来源责任表

首个 proof 使用同一 capability 下两个 exact required Relation sources：

| Provider | exact responsibility |
| --- | --- |
| `closed-relation-provider-a / 0.1-test` | 全部 `LEXICAL_CONTAINS` observation items |
| `closed-relation-provider-b / 0.1-test` | 全部 `LEXICAL_CONTAINS` 与 `IMPORT_TARGET_LITERAL` observation items |

两者共同固定：

```text
capability_id    = review-relation-derivation
parser_id        = closed-deterministic-test-parser
parser_version   = 0.1-test
runtime_id       = veritrail-review-test-runtime
runtime_version  = 0.1-test
```

两个 Provider 都必须真实使用该 parser；不能因为 B 的 import target 可以从 Fact attributes 复制，就虚报 parser
identity。B 对 `IMPORT_TARGET_LITERAL` 的首版输出只保留 source literal 与保守
`UNRESOLVED / UNKNOWN / resolved_fact_ids=[]`；它不执行完整 module resolution，也不声称 runtime import truth。

A/B 同时负责 lexical items 是有意的：它让首个 proof 真实覆盖 same-ID provenance union，并允许用单变量
negative fixture 证明 same-subject incompatibility 不会被 completion order 或 provider priority 吞掉。它不是为了
“多模型投票”，两个来源一致也不产生更高事实 authority。

完整 submitted binding multiset 必须在 Fact Provider 启动前与 closed table 完全相等。缺失 B、额外 Relation
binding、descriptor/handle 漂移、重复 identity 或 ambient installed Provider 均为 pre-admission mismatch：无
derivation attempt、无 ProviderRun、无 ObservationDomain、无 Evidence。执行途中因 stop 未启动 B 则保留为另一条
真实历史：attempt 已存在，但 required source-set terminal closure 不成立。

## 5. exact FactSet-derived observation items

### 5.1 首个 closed input domain

首个 proof 只接受 normal、conflict-free、无 optional Fact-source gap 的 exact FactSet，并继续服从文档 165/172
的 upstream gate。为避免把 fixture proof 冒充完整 Python algorithm，首个 observation profile 只接受：

```text
one supported ordinary Python blob
exactly one MODULE Fact for that blob
zero or more IMPORT_DECLARATION Facts produced by single-name ast.Import statements
no CLASS / FUNCTION / METHOD Fact in this proof
all Fact identities, anchors, attributes and provenance already closed
```

不满足该 closed shape 时，首个 implementation 必须在 Relation source 执行前拒绝 qualification construction；它不把
未支持输入缩成较小 denominator，也不生成 `UNKNOWN` RelationSet。

### 5.2 item identity

application 从 exact copy-owned FactSet 机械建立 observation items，不运行 Relation Provider，也不猜 candidate
target。固定 family-to-subject 规则为：

```text
LEXICAL_CONTAINS
  one item for every non-MODULE Fact
  subject_role = TARGET_FACT
  subject_fact_id = that Fact identity

IMPORT_TARGET_LITERAL
  one item for every IMPORT_DECLARATION Fact
  subject_role = SOURCE_FACT
  subject_fact_id = that Fact identity
```

首版 closed input 只有 IMPORT declarations，所以每个 import 产生两个不同 family items。item identity 为：

```text
domain  = veritrail.review.relation-observation-item/0.1
payload = {
  source_snapshot_digest,
  derivation_profile_digest,
  fact_set_digest,
  relation_kind,
  subject_role,
  subject_fact_id
}
```

items 按 Profile relation-kind rank，再按 `SOURCE_FACT < TARGET_FACT`、`subject_fact_id` Unicode code-point
排序且唯一。该 identity
只表示“这一 family 对这一 Fact-backed subject 有一次观察义务”，不等于 `relation_subject_digest`，也不提前决定
Relation target、resolution status、local ordinal 或 candidate truth。

### 5.3 declared domain 与 responsibility identity

observation profile 先形成自己的语义摘要：

```text
domain  = veritrail.review.relation-observation-profile/0.1
payload = {
  observation_profile_id,
  observation_profile_version,
  derivation_profile_digest,
  capability_id,
  required,
  composition_mode,
  family_rules,
  provider_responsibility_rules
}
```

`family_rules` 绑定 relation family、subject role、eligible Fact kinds、candidate cardinality 与
`negative_outcome_allowed`；`provider_responsibility_rules` 绑定 exact Provider descriptor 与 assigned families。
因此同一个 FactSet 若换了 Profile/Policy responsibility semantics，会先改变 `observation_profile_digest`，不能
沿用旧 denominator 或旧履责证据。

private `DeclaredRelationObservationDomain 0.1` 至少 copy-own：

```text
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
fact_set_digest
observation_profile_id / version
observation_profile_digest
capability_id / required / composition_mode
observation_items[]
provider_responsibilities[]:
  exact provider descriptor
  required
  assigned_observation_item_ids[]
observation_domain_digest
```

`observation_domain_digest` 不覆盖完整 `policy_digest` 中的 wall-clock、memory 与 governance 噪声；精确投影为：

```text
domain  = veritrail.review.relation-observation-domain/0.1
payload = {
  source_snapshot_digest,
  analysis_scope_digest,
  derivation_profile_digest,
  fact_set_digest,
  observation_profile_id,
  observation_profile_version,
  observation_profile_digest,
  capability_id,
  required,
  composition_mode,
  observation_items,
  provider_responsibilities
}
```

其中 responsibilities 按文档 160 的 descriptor rank 排序，assigned IDs 排序且唯一。它们包含完整 descriptor 与
assigned IDs；`observation_profile_digest` 又绑定决定这些 assignments 的冻结 family/Policy responsibility rules。
因此改变负责来源、family assignment、negative policy 或 item denominator 都会改变 domain identity。完整
`policy_digest` 留在 private value 中，供同一次 execution 绑定；wall-clock 与 memory 等非责任语义不进入正常
observation-domain semantic identity。

domain 必须在第一个 Relation Provider code 运行前 canonicalize、复算并 copy-own。Provider 不能增删 item，caller
不能在 A terminal 后为 B 补 responsibility，application 也不能用实际 candidates 反向构造 denominator。

## 6. relation-only identity 与 wire 必须版本化

冻结的 `veritrail.review.provider-operands/0.2` 只绑定 `fact_set_digest`，不能区分同一 FactSet 上两份不同责任图。
它继续属于文档 165/172 的历史 single-source proof，不得原位改写。本合同候选为后继实现提出 relation-only：

```text
domain  = veritrail.review.provider-operands/0.3
payload = provider-operands/0.2 payload + {
  observation_domain_digest,
  assigned_observation_item_ids
}
```

每个 Relation Provider 的 assigned item IDs 可以不同，所以 A/B 在同一 FactSet 上仍有不同 operands digest；
`provider_run_id` 继续使用冻结的 `veritrail.review.provider-run/0.1` 公式，不升级历史 run IDs。

当前 `veritrail-review-relation-cell/0.1` request/terminal 没有 domain identity、item assignment 或逐 item outcome。
后继实现必须新增
private `veritrail-review-relation-cell/0.2`，至少让 request 绑定：

```text
observation_domain_digest
assigned_observation_item_ids
provider-operands/0.3 digest
```

terminal 必须分别报告真实 canonical Relation candidates/IDs 与 canonical `observation_outcomes[]`。Provider 不自己
签发 ObservationReceipt，也不能把 `assigned_observation_item_ids` 原样 echo 就冒充观察完成；每个 outcome 必须在
对应 bounded operation 已完成后形成。application 对 outcomes、candidate references 与 candidate endpoints 做
双向机械对账，不能只从 candidate presence/absence 猜履责状态。

`/0.2` wire 与 `/0.3` operands 仍是 private protocol/identity，不是公共 Schema 或 SPI。若后继实现证明无法在不
修改公共 Artifact 的情况下保持 exact binding，应停止并重开最小 Schema 边界，不得让 `/0.1` 接受额外字段。

## 7. execution、terminal 与 source-local receipt

两个 Relation sources 与全部 Fact sources 继续属于同一 derivation、同一个 live `BudgetContext`、absolute
monotonic deadline 与 stop latch。Relation sources 按冻结 descriptor rank 串行执行；每个 source 不刷新预算，也
不借用 Q 并行调度。

只要 shared context 仍安全、前一 child residue-free release，普通 `FAILED / UNAVAILABLE` 不获得 first-failure
short-circuit 权。controller 必须继续观察剩余 required source，使“B 未运行”和“B 真实 unavailable”保持不同。
deadline/cancel/memory stop、release failure、shared-context 破损或 identity/protocol integrity failure 才阻止后继
source 启动。

ProviderRun 的 `execution_status` 不因后继 item accounting 被改写。与该 run 绑定的 private relation-cell terminal
另报告 `ObservationOutcome[]`；outcome 与 Relation candidate 数组是两个独立字段，不能修改公共 ProviderRun
Schema：

```text
observation_item_id
disposition = CANDIDATE_REPORTED | NO_CANDIDATE_OBSERVED
reported_relation_ids[]
```

outcome semantic identity 为：

```text
domain  = veritrail.review.relation-observation-outcome/0.1
payload = {
  provider_run_id,
  observation_item_id,
  disposition,
  reported_relation_ids
}

observation_outcome_id = semantic_digest(domain, payload)
```

outcomes 按 item identity 排序且每个 assigned item 最多一个；relation IDs 排序且唯一。Provider 只能为已分配 item
报告 outcome。`CANDIDATE_REPORTED` 的 IDs 必须符合冻结 family cardinality；当前 profile 恰为一个。
`NO_CANDIDATE_OBSERVED` 必须没有 relation ID，且只有冻结 family rule 明确设置
`negative_outcome_allowed=true` 时才合法；当前两个 family 均拒绝该 disposition。

只有 `execution_status=COMPLETED` 且 residue-free release 的 terminal outcomes 才能进入 accepted accounting。
`FAILED/UNAVAILABLE/INTERRUPTED` 的任何 partial outcomes 只能随 attempt history 保留，不能关闭 item；deadline、
cancel 或 memory stop 后仍沿用文档 165/172 的 no-prefix-candidate 规则，也不得留下可 qualification 的 prefix outcome。

candidate 到 item 的首版映射固定为：

```text
LEXICAL_CONTAINS
  candidate.target.fact_id accounts for TARGET_FACT item

IMPORT_TARGET_LITERAL
  candidate.source_fact_id accounts for SOURCE_FACT item
```

application 必须验证双向 closure：每个 assigned item 恰有一个合法 outcome；每个
`CANDIDATE_REPORTED` ID 指向该 terminal 的 canonical candidate 且该 candidate 按上述规则映射回同一 item；每个
terminal candidate 也恰被一个 outcome 引用。缺 outcome、重复/额外 outcome、dangling/mismatched relation ID、
未被任何 outcome 引用的 candidate 或违反 negative policy，任一都使 source-local fulfillment 不成立。

application 随后为每个 required source 建立 private `ObservationReceipt`：

```text
provider_run_id | null when never started
provider_descriptor
required
execution_status | NOT_STARTED
assigned_observation_item_ids[]
accepted_observation_outcomes[]
missing_observation_item_ids[]
unexpected_observation_item_ids[]
duplicate_observation_item_ids[]
unexpected_relation_ids[]
unreferenced_relation_ids[]
invalid_outcome_ids[]
```

`missing_observation_item_ids` 只能由“assigned item 没有合法 outcome”得出，不能由 candidate 缺席直接推断；同理，
application 不能替 Provider 补 `NO_CANDIDATE_OBSERVED`。`missing/unexpected/duplicate/invalid` 不删除 run-local
outcomes/candidates，也不把 truthful `COMPLETED` 反写为 `FAILED`；它们使 source observation closure 不成立，并
永久阻止本次 normal composition qualification。

每份 receipt 的数组使用 item/outcome/relation identity 排序且唯一。receipt 是 application 对 Provider 履责声明与
candidate bytes 的机械 projection，不是 CoverageLedger、新事实来源或 Provider 正确性的独立证明。

## 8. successful empty、未启动与遗漏

首个 profile 的 empty 语义固定为：

```text
assigned items = []
+ ProviderRun actually STARTED
+ terminal = COMPLETED
+ observation outcomes = []
+ candidates = []
+ residue-free release
=> this source receipt is complete-empty
```

以下状态都不是 complete-empty：

```text
NOT_STARTED
FAILED
UNAVAILABLE
INTERRUPTED
COMPLETED + non-empty assigned items + []
COMPLETED + missing outcomes
COMPLETED + candidate but missing/mismatched outcome
COMPLETED + invalid negative outcome
COMPLETED + unexpected outcome/candidate
```

当 whole declared domain 为空，A/B 仍必须各自真实启动、terminal、release，并各自获得 complete-empty receipt；
只有这样才能说“这个 exact empty domain 的两次 required execution 都已闭合，且没有 candidate”。这仍不能升级成
“源码中不存在任何 Relation”或“完整 Python Relation universe 为空”。

非空 domain 的 closed negative 与 empty-domain 不同。它至少需要冻结 family rule 允许 negative、Provider 为每个
assigned item 显式报告合法 `NO_CANDIDATE_OBSERVED`、application 完成 outcome closure，且没有 candidate/reference
残留。首个 profile 不允许这条路径，因此 `COMPLETED + []` 在 non-empty domain 上永远不能 qualification。

required source 未启动、失败或 unavailable 时，domain identity 和已经完成的 receipts 继续保留；不得删除 B 的
responsibility 后重算更小 domain。private candidates 可以作为 attempt history 保留，但不能进入 normal composition
member set、RelationSet 或 final reported IDs。

## 9. required source-set terminal closure 与 observation closure

qualification result 必须分别保存：

```text
required_source_set_terminal_closure
  COMPLETE   = 每个 required responsibility 都有真实 terminal ProviderRun
  INCOMPLETE = 至少一个 required source NOT_STARTED

required_observation_closure
  COMPLETE   = 每个 required source terminal COMPLETED，且每个 assigned item 有一个合法 outcome，
               outcome/candidate 双向闭合，receipt 无 missing/unexpected/duplicate/invalid
  INCOMPLETE = 其他全部情况
```

terminal closure 只回答 required runs 是否都到达真实终态；它允许某 run 是 `FAILED/UNAVAILABLE`，因此不能替代
observation closure。observation closure 也不回答多个 sources 是否一致。

首个 profile 没有 optional Relation source。未来若引入 optional responsibility，必须另外保存
`optional_source_terminal_gaps` 与 `optional_observation_gaps`；required closure 不得删除它们，也不得把“required
complete”显示为“all applicable complete”。

## 10. multi-source candidate composition

只有 required observation closure `COMPLETE` 时，application 才能进入 private candidate composition；composition
只消费被合法 outcomes 引用的 candidates。否则
`candidate_composition_status = NOT_COMPOSED`，并保留全部 run/receipt history。

### 10.1 same ID union

多个 complete receipts 报告相同 `relation_id` 时，先删除 `provenance_refs` 比较完整 canonical Relation semantic
object：

```text
same relation_id + byte-identical provenance-free semantic object
  -> one private merged candidate
  -> provenance_refs = sorted unique union(reporting provider_run_ids)
  -> every reporting receipt retains its own item accounting
```

同一 `relation_id` 对应不同 semantic bytes 是 identity/integrity failure，不是 RelationConflict；composition status
为 `INTEGRITY_FAILED`，qualification 不成立。

### 10.2 same subject incompatibility

不同 `relation_id` 具有相同冻结 `relation_subject_digest` 时，全部 candidates 保留，并按文档 120 的冻结公式形成
private conflict record：

```text
conflict_id = semantic_digest(
  "veritrail.review.relation-conflict/0.1",
  {relation_subject_digest, candidate_relation_ids}
)
```

conflict provenance 是全部 candidate provenance 的排序唯一并集。completion order、provider priority、confidence、
requiredness 或多数一致都不能选择 winner。

该路径允许：

```text
required_observation_closure = COMPLETE
candidate_composition_status = CONFLICTING
```

这不是矛盾：所有 declared items 都有通过机械对账的 fulfillment records，但 sources 报告的 candidates 不一致。
它仍不自动获得 RelationSet admission；后继合同必须决定 conflict-bearing RelationSet、Slice empty 与 Coverage
UNKNOWN 的确切闭包。

### 10.3 composition status

private candidate composition status 闭集为：

```text
NOT_COMPOSED
CONSISTENT
CONFLICTING
INTEGRITY_FAILED
```

`CONSISTENT/CONFLICTING` 都只表示 deterministic composition 结果；它们不是事实真值、缺陷判断或 admission。

## 11. private qualification result 与 identity

private `RelationCompositionQualification 0.1` 至少 copy-own：

```text
exact input semantic digests
observation_domain_digest
all required ProviderRun terminal facts
all ObservationReceipts
required_source_set_terminal_closure
required_observation_closure
candidate_composition_status
qualification_status
merged candidate Relation bytes, when composed
private RelationConflict bytes, when composed
reason_codes[]
qualification_digest
```

`qualification_digest` 通过 receipts 绑定全部 accepted outcomes，并绑定完整 domain、terminal closure、observation
closure、composition status、merged candidate IDs、conflict IDs 与 reasons；运行时间仍留在 ProviderRun/Evidence，
不进入正常 qualification semantic identity。精确投影为：

```text
domain  = veritrail.review.relation-composition-qualification/0.1
payload = {
  observation_domain_digest,
  provider_run_terminals: [{provider_run_id, execution_status}],
  observation_receipts,
  required_source_set_terminal_closure,
  required_observation_closure,
  candidate_composition_status,
  qualification_status,
  merged_candidate_relation_ids,
  private_conflict_ids,
  reason_codes
}
```

`reason_codes` 闭集与 rank 固定为：

```text
REQUIRED_SOURCE_NOT_STARTED
REQUIRED_SOURCE_FAILED
REQUIRED_SOURCE_UNAVAILABLE
REQUIRED_SOURCE_INTERRUPTED
OBSERVATION_OUTCOME_MISSING
OBSERVATION_OUTCOME_UNEXPECTED
OBSERVATION_OUTCOME_DUPLICATE
OBSERVATION_OUTCOME_INVALID
OBSERVATION_CANDIDATE_REFERENCE_MISMATCH
UNEXPECTED_RELATION_CANDIDATE
RELATION_IDENTITY_COLLISION
SHARED_CONTEXT_FAILURE
RELEASE_FAILURE
```

只保留实际成立的排序唯一 reasons；不得把未识别异常塞进最接近的 Provider reason。无法安全归因时沿既有
`DERIVATION_INTEGRITY_FAILURE` 停止，不生成伪精确 qualification receipt。

`qualification_status` 闭集为 `QUALIFIED / NOT_QUALIFIED / INTEGRITY_FAILED`。只有同时满足以下条件才可标记
`QUALIFIED`：

1. exact observation domain 已在执行前形成并通过复算；
2. required source-set terminal closure 为 `COMPLETE`；
3. required observation closure 为 `COMPLETE`；
4. candidate composition status 为 `CONSISTENT` 或 `CONFLICTING`；
5. 无 identity collision、shared-context/release failure 或 terminal-stop contamination；
6. 全部 values/bytes copy-owned，caller mutation 不改变结果。

`QUALIFIED` 只回答“本合同声明的 bounded observation obligations 已有显式履责记录、通过机械对账并完成
composition”。它不证明 Provider 内部真的检查了什么，不回答 candidate 是否真实、不回答 conflicts 是否可接受，
也不授予 RelationSet、Slice、Coverage、final Evidence 或 publication authority。

qualification 不成立时，truthful ProviderRuns、domain、receipts 与 reasons 可以留在 private result；final
ProviderRun `reported_relation_ids` 继续按文档 155/165 清空。不得为了输出更漂亮而把 incomplete source 删除、
缩小 domain 或新建 BudgetContext 重试后拼成同一次 attempt。

## 12. 公共 Schema 与 RelationSet 的裁决

当前公共 `RelationSet 0.1` 能保存 candidates、conflicts 与 `fact_set_digest`，但没有：

```text
observation_domain_digest
provider responsibility map
per-item observation outcomes
source-local receipts
required source-set terminal closure
observation closure / omission accounting
qualification identity
```

`DerivationEvidence 0.1.1` 的 ProviderRuns 也只报告 execution/provenance，不能从 descriptor 与空数组复算某 source
本应观察哪些 items。因此现有公共 shape **不足以让第三方只凭 Bundle 证明 composition qualification**。

本合同不因这个结论立即升级 Schema。首个实现把 domain/receipt/qualification 保持为 private construction state，
不写文件、不进 Manifest、不形成 RelationSet。实现冻结后的系统审计必须在以下路径中重新选择最小者：

1. versioned public qualification Artifact/receipt；
2. RelationSet / DerivationEvidence / Manifest 的最小绑定修正；
3. 明确把某种 RelationSet 降格为 observed prefix，并让 Coverage denominator 保持 `UNKNOWN`。

在该选择完成前，`candidates -> relation-set.json` 仍然禁止。Schema-valid RelationSet shape 不能替代 qualification
authority，qualification `QUALIFIED` 也不能替代 RelationSet membership/admission conformance。

## 13. 最小 conformance matrix

后继获授权实现至少逐格证明：

| ID | 单变量义务 | 预期 |
| --- | --- | --- |
| `RQ-001` | Profile 双 kind + exact required CUMULATIVE requirement + exact A/B bindings | preflight 成功；domain 尚未执行 Provider |
| `RQ-002` | Profile 只列双 kind，但 observation profile/responsibility table 缺失 | pre-admission reject；不得从 Profile 猜义务 |
| `RQ-003` | 缺 B、额外 binding、重复/漂移 descriptor 或 ambient Provider | pre-admission reject；无 run/domain/Evidence |
| `RQ-004` | sealed Relation requirement optional 或 composition mode 漂移 | current closed profile reject |
| `RQ-005` | one MODULE + one IMPORT Fact | exactly two observation items；A one assignment，B two |
| `RQ-006` | MODULE-only FactSet | empty domain；A/B 仍各自真实 complete-empty 后才 QUALIFIED |
| `RQ-007` | CLASS/FUNCTION/METHOD Fact 或非 closed import shape | qualification construction reject；不缩 denominator |
| `RQ-008` | FactSet/digest 变化，其他坐标相同 | item/domain `/0.3` operands 与 run IDs 改变 |
| `RQ-009` | responsibility assignment 变化，FactSet 相同 | observation domain 与 affected operands 改变 |
| `RQ-010` | A COMPLETED 且 candidates 完整，B NOT_STARTED | terminal closure INCOMPLETE；NOT_COMPOSED |
| `RQ-011` | A 有完整 outcomes/candidates、B UNAVAILABLE，domain non-empty | observation INCOMPLETE；不能声明 relation domain complete |
| `RQ-012` | non-empty assignments + Provider COMPLETED + candidates/outcomes 都为空 | run status 保持；全部 items missing；qualification 否决 |
| `RQ-013` | `i1/i2` 只有 `i1` 的合法 candidate/outcome，`i2` 无 outcome | `i1` candidate 合法；domain closure INCOMPLETE |
| `RQ-014` | 当前 profile 对 non-empty item 报 `NO_CANDIDATE_OBSERVED` | negative policy violation；qualification 否决 |
| `RQ-015` | Provider 报告未 assigned family/subject outcome 或 candidate | receipt unexpected；qualification 否决 |
| `RQ-016` | 一个 item 有重复 outcomes 或两个 candidates | source-local accounting nonconformant |
| `RQ-017` | outcome 引用 dangling/mismatched candidate，或 candidate 未被 outcome 引用 | 双向 closure 失败；qualification 否决 |
| `RQ-018` | A/B 报告相同 lexical Relation 与各自合法 outcome | one merged candidate；provenance union；receipts 独立 |
| `RQ-019` | A/B same subject、different valid IDs/outcomes | observation COMPLETE；composition CONFLICTING；无 winner |
| `RQ-020` | same relation ID、different semantic bytes | INTEGRITY_FAILED；不是 RelationConflict |
| `RQ-021` | required source FAILED/UNAVAILABLE 后 context 仍安全 | 继续观察后继 required source；保留全部真实 terminals |
| `RQ-022` | deadline/cancel/memory/release failure | stop 后不启动后继 source；no qualification/Artifact |
| `RQ-023` | 每个 Relation source 获得新 budget | 明确拒绝；沿用 original live BudgetContext |
| `RQ-024` | B 输出 conservative IMPORT literal candidate/outcome | literal 与 Fact 精确相同；`UNRESOLVED/UNKNOWN`；不冒充 resolver |
| `RQ-025` | B 报告 parser identity/outcomes 但未实际调用 parser | conformance reject；outcome 不能替代真实 operation |
| `RQ-026` | caller 修改 domain/outcome/receipt/candidate views | owned canonical bytes/digests 不变 |
| `RQ-027` | private result 接收 output path/RelationSet/publisher probe | no such capability；零文件 |
| `RQ-028` | CPython 3.10/3.13 normal/`-O` | items、domain、outcomes、receipts、composition 与 qualification bytes 一致 |

`RO-000..007` 必须继续作为合同级反例；`RQ-001..028` 是后继 implementation conformance，不把测试数量当成
scope KPI。

## 14. 实现分段与停止线

本合同只有完成候选远端门、受保护主线合入、exact-main 门、fresh anonymous product readback 与后继独立
docs-only 冻结发布后，才可以严格按顺序实现：

```text
A. private observation profile + exact A/B responsibility/binding admission
B. FactSet-derived observation items + domain identity
C. relation-only provider-operands/0.3 + relation-cell/0.2
D. shared-budget serial A/B execution + Provider-owned per-item outcomes
E. application outcome/candidate reconciliation + source-local receipts
F. same-ID union / same-subject private conflict / qualification projection
G. immutable OwnedRelationCompositionQualificationResult
H. RQ-001..028 hardening
```

每一步都是停止线。A–H 不得创建或修改公共 Schema、RelationSet、CoverageLedger、ReviewSliceSet、final Evidence、
Manifest、output path、public Provider registry、完整 resolver、CLI 或 Workbench。若实现证明 FactSet 不能机械建立
首版 item denominator、parser identity 无法诚实绑定、`/0.3` 不能保持历史兼容或 current Schema 必须提前变化，
必须回到合同；不得缩小 denominator、复用 `/0.2` identity、从 candidate 缺席补 negative outcome 或把 Provider
自述当成独立事实 authority。

## 15. 候选验收与冻结序列

本文只有满足以下条件才有资格进入独立冻结发布：

1. `RO-000..007` 均有唯一裁决；
2. Profile vocabulary、Policy requiredness、observation profile、responsibility、run、outcome、receipt 与 qualification identity 分离；
3. first proof 的 Fact-backed item denominator 能在 Provider 运行前机械构造；
4. A/B exact responsibility、required-only 边界与 same-ID overlap 没有 caller 自由度；
5. `/0.3` operands 与 `/0.2` relation wire 不改写历史 `/0.2` operands 或 `/0.1` wire；
6. responsibility definition、Provider terminal、per-item fulfillment、required terminal closure、observation closure 与 candidate composition 保持正交；
7. outcome/candidate 双向闭合；candidate 缺席不能生成负结论，当前 total-obligation families 不接受 negative outcome；
8. empty、missing、unexpected、not-started、unavailable、failed、interrupted 与 conflict 不共用空数组；
9. `QUALIFIED` 不授予 RelationSet admission/publication，现有公共 Schema 不被误写为足以承载 qualification；
10. diff 只有本文、README、AGENTS 与 milestones 状态入口；
11. 本地 Markdown、状态、敏感/本机路径、exact scope 与适用双 Python normal/`-O` 回归成立；
12. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
13. 新 exact main Public CI、Browser Smoke 与 README/本文/milestones 的 fresh anonymous installed-product readback 成立；
14. 后继独立 docs-only 状态发布完成相同最后门。

只有第 14 项完成后，才可写：

```text
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_ALLOWED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

授权只覆盖第 14 节 A–H。不得从合同候选、候选绿灯、合入或 exact-main CI 单独推导 implementation authority。

## 16. 当前候选事实与 Fresh-Agent 交接

当前只能写：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_CANDIDATE
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

新的、没有聊天上下文的 Agent 必须先读文档 113、120、155、160、165、172、173 与本文，然后只审计这些
合同能否同时成立。重点攻击：Fact-backed item 是否真的足以防止 denominator shrink、responsibility definition
是否被偷换成 fulfillment、outcome 是否只是 assigned IDs echo、candidate/outcome 双向 closure 是否有逃逸路径、
observation profile digest 是否完整绑定责任语义、A/B overlap 是否产生虚假独立性暗示、complete-empty 是否仍有
逃逸路径、conflict-bearing qualification 是否被误读成 admission，以及 private receipt 是否在无公共 Schema 下越权。

外部 production case 仍未触发：本地 `RO-000..007`、冻结 Schema 与 runtime 已足以选择
responsibility/item/outcome/receipt
模型。只有合同审计出现无法由本地 falsifier 选择的真实 failure shape，才按问题族查询公开一手材料；公司名、
产品架构或模型 KPI 都不直接产生本合同 authority。

## 17. 本地候选证据

本文语义候选最初从 exact `main@559bf9b9a052f0b542227b1cea069dd15c696cc8` 的独立 worktree 建立。PR #160 原始 head 的正式
Python 3.13 首败随后证明既有测试夹具的时间坐标需要独立维护；它没有反证或改写本文合同。维护闭环取得
`main@962251d91bc2695afe984ee47845ac4fe1a80f7e` 的 exact-main 资格后，当前候选从该 source state 重新绑定、顺延为文档 175，并重新接受
完整门禁。当前 diff 不得包含 runtime、Schema、corpus、vector、tests、Provider、parser、依赖、CI 或发布文件。

候选提交前至少复核：

1. relative Markdown links、fence/heading、状态 marker、敏感/本机路径与 exact scope；
2. `git diff --check`；
3. Relation derivation 与 broad boundary focused suites 在 CPython 3.10/3.13、normal/`-O`；
4. test module `__file__` 与 `veritrail_review` import 均绑定当前 worktree。

最终候选本地结果：

```text
exact diff scope
  PASS: README.md / AGENTS.md / docs/milestones.md / this document only

Markdown/static
  PASS: git diff --check
  PASS: 342 relative links, balanced fences, no tab/local-path/sensitive marker
  PASS: tests.test_markdown, CPython 3.10.6, 4/4
  PASS: tests.test_markdown, CPython 3.13.13, 4/4

focused frozen-runtime regression
  PASS: CPython 3.10.6 normal, 24/24, 37.933s
  PASS: CPython 3.10.6 -O,     24/24, 39.313s
  PASS: CPython 3.13.13 normal, 24/24, 37.951s
  PASS: CPython 3.13.13 -O,     24/24, 37.572s
```

两次 command-construction probe 在 unittest 启动前即被拒绝：第一次 Markdown probe 未把 root `tests` 加入
`PYTHONPATH`；第一次 focused probe 又把 root `tests` 放到 Review plugin tests 前，导致 `support` 名称遮蔽。
两者均未执行测试、未产生产品 observation，不记作正式 regression 首败；修正后的命令都用 `__file__` 证明绑定
当前 worktree，随后得到上述结果。

这些本地门只证明 docs-only candidate 没有暗改冻结实现，不替代本文自己的 PR、合入、exact-main 双门、专属
anonymous installed-product readback 或后继独立合同冻结发布。
