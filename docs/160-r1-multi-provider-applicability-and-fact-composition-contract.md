# R1 Multi-Provider Applicability / Fact Composition 最小合同 0.1

> 状态：`R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@22df05698f05380e910ac8a4e0cc6ba1276842e7`
>
> 前置审计：[R1 Fact/Evidence 冻结后下一闭环系统审计](159-r1-post-fact-evidence-next-closure-system-audit.md)
>
> 上游冻结输入：[R1 确定性语义切片合同](113-r1-deterministic-semantic-slice-contract.md)、
> [R1 Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Derivation Attempt 与 Fact Provenance 合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)、
> [DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)、
> [Budget Primitive 合同](145-r1-derivation-budget-primitive-contract.md)、
> [Execution Cell / Terminal Envelope 合同](150-r1-derivation-execution-cell-terminal-envelope-contract.md)与
> [Fact Admission / DerivationEvidence Closure 合同](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`；本文只冻结 private closed-test
> applicability、multi-Provider terminal join、Fact composition/conflict 与 Evidence projection 规则，不创建或
> 修改 runtime、Schema、corpus、identity vector、测试、Provider、parser、publisher、Relation、Slice、Coverage、
> Manifest、CLI、Workbench、Core、P/Q/D、依赖、CI、tag 或 Release

## 1. 目的与停止线

当前 private Fact/Evidence closure 只接受一个显式 closed test `ProviderBinding`。R1 0.1 的公共合同已经允许
`CUMULATIVE` 多来源、Provider run 数组、Fact provenance 并集与 `FactConflict`，但还没有冻结：

```text
sealed capability requirements
        ↓
exact applicable Provider descriptor set
        ↓
one shared derivation execution permission
        ↓
all applicable Provider outcomes
        ↓
deterministic Fact merge / conflict / availability join
        ↓
owned, non-published FactSet or DerivationEvidence state
```

本文只关闭这条接缝。即使本文以后冻结，首个获授权实现也只能建立 closed deterministic multi-Provider test
path、private composition state 与 conformance matrix。它仍不授权：

```text
real Python parser
public Provider SPI / registry / discovery
caller-selected arbitrary Provider
DIAGNOSTIC or COMPLETE publisher
RelationSet
ReviewSliceSet
CoverageLedger
Manifest directory
CLI / Workbench / Core integration
```

## 2. 五个对象不能压成一个“Provider list”

```text
ProviderRequirement
  sealed Policy 中的 capability、requiredness 与 composition rule

ApplicabilityRule
  application-owned、版本化合同规则；把一个 requirement 映射到 exact descriptor set

ProviderDescriptor
  capability/provider/parser/runtime 的不可变实现坐标；不是 Seal 决定

ProviderBinding
  exact descriptor + private callable/launch handle；只提供执行能力

ProviderRun
  一个 descriptor 在一个 derivation attempt 中的真实执行事实
```

因此：

```text
capability requirement != provider implementation identity
descriptor              != implementation handle
applicable set          != ambient installation state
provider identity       != provider-run identity
composition result      != provider completion order
```

Policy 继续由 Human Seal authority 拥有。application 只拥有被冻结合同下的 applicability 与 conformance；
Provider 只拥有 bounded observation；Core、R 后继阶段和调用方都不能反向改写这些权威。

## 3. 首个 private applicability profile

### 3.1 只采用合同定义的 closed conformance 表

首个实现不建立公共授权 Artifact。它只允许 application package 内一个不可由调用方修改的 closed conformance
table。表的规范坐标固定为：

| capability requirement | exact applicable descriptors | requiredness |
| --- | --- | --- |
| `python-ast` | `closed-multi-provider-a`、`closed-multi-provider-b` | 继承 requirement 的 `required` |
| `python-ast-advisory` | `closed-multi-provider-advisory` | 继承 requirement 的 `required` |

三个 descriptor 的其余固定值为：

```text
provider_version = 0.1-test
parser_id         = closed-deterministic-test-parser
parser_version    = 0.1-test
runtime_id        = veritrail-review-test-runtime
runtime_version   = 0.1-test
```

`python-ast` 必须在首个 accepted Policy profile 中出现且满足：

```text
required = true
composition_mode = CUMULATIVE
```

`python-ast-advisory` 可以缺席；出现时必须满足：

```text
required = false
composition_mode = CUMULATIVE
```

任何其他 requirement、requiredness 或 composition mode 均不属于首个 private implementation profile。这个表只为
closed conformance lab 建立可复算的 applicability authority；它不是未来 real parser 的信任模型，也不得成为
公开 Provider compatibility 承诺。

真实 Provider 进入可发布 R1 Evidence 以前，必须另开合同决定固定内建 authorization、版本化 Provider
Authorization Artifact 或其他可独立复核的公共边界。不能把本节测试表改名成 registry 后直接对外。

### 3.2 完整集合先于执行

对于每个 Policy requirement，application 必须得到至少一个 exact descriptor。`required=false` 表示该来源的
terminal failure 不单独改变 overall status；它不表示 mapping 可以为空或从 Evidence 中消失。

调用方必须提交与规范表完全相等的 binding multiset。application 在任何 Provider code 获得执行权以前：

1. copy-own requirement 与全部 descriptor；
2. 验证 descriptor 的 `capability_id` 与 requirement exact 相等；
3. 验证每个 `(capability_id, provider_id)` 唯一；
4. 验证无缺失、无额外、无重复、无 descriptor 漂移；
5. 验证 private handle 精确匹配 closed allow-list；
6. 按第 3.3 节规范化为一个 immutable tuple。

mapping 缺失、binding 子集、额外 binding、caller 自定义 descriptor 或 allow-list handle 不匹配，均发生在
derivation admission 前；无 attempt、无 ProviderRun、无 DerivationEvidence。它们不能伪装成
`PROVIDER_UNAVAILABLE`，因为还没有一个合法开始的 ProviderRun。

### 3.3 规范顺序与基数

descriptor rank 固定为以下 Unicode code-point tuple：

```text
(
  capability_id,
  provider_id,
  provider_version,
  parser_id,
  parser_version,
  runtime_id,
  runtime_version
)
```

applicable binding tuple 与实际串行执行顺序都使用该 rank。调用方输入顺序、mapping insertion order、进程完成
顺序或 hash iteration 不能改变执行计划、Fact/conflict identity 或 canonical arrays。

`DerivationEvidence.provider_runs` 仍按冻结的 `provider_run_id` 排序，不按执行顺序排序。运行先后只由 truthful
`started_at/finished_at` 表达；排序本身不获得时序含义。

## 4. 一个 derivation、一个 BudgetContext、一个 composition controller

首个实现严格串行，不并行运行 Provider。Q 不参与 R1 Provider 调度。controller 在 full applicability/binding
tuple 通过 admission preflight 后，只创建一次：

```text
one derivation_id
one absolute monotonic deadline
one BudgetContext
one parent composition eligibility
one ordered sequence of bounded single-Provider child cells
```

所有 Provider 初始化、调用、candidate canonicalization、run summary、Fact merge/conflict 与 terminal envelope
construction 都消费该 context 的剩余资格。禁止：

```text
Provider A -> full new wall/memory budget
Provider B -> another full budget
composition -> refreshed timeout
optional Provider -> unmetered execution
```

首个实现必须逐字节保留现有 `veritrail-review-derivation-cell/0.1` 的 single-Provider request/terminal
协议：每个 child cell 仍只接收一个 exact descriptor、一个 request frame，并返回至多一个 terminal frame。本文不
发明 multi-Provider wire protocol 或 multi-run terminal envelope。multi-Provider path 只新增独立的 private
composition entry，由它在同一次调用内拥有全部 child cell、同一个 BudgetContext 与最终 join；不得把若干
standalone public phase result 在调用返回后拼接，并声称它们共享同一个 derivation execution permission。

composition entry 在第一个 worker resume 前已经 copy-own exact descriptor/binding tuple 与 owned source bytes；
Provider code 不能增删、替换或重排后继 source。每个 child terminal frame 继续按文档 150 独立验证；partial、重复、
trailing 或 descriptor continuity 破坏只能使该 run fail closed，不能接纳该 run 的部分 Fact。

parent composition eligibility 与每个 child 的 run-local eligibility 必须是不同对象。run-local eligibility 只控制
该 child 的 terminal commit；valid Provider non-success 或可诚实归因且已 residue-free release 的 child
transport/protocol failure，只撤销该 run 的 normal Fact eligibility。只有 whole-attempt stop、release failure、
shared-context 破损、binding/descriptor continuity 破坏或 composition-level integrity failure 才撤销 parent
eligibility。不得因“复用一个 boolean 比较方便”而让普通 Provider failure 获得 whole-attempt short-circuit 权。

本文首个 private slice 不执行 Artifact reservation：`artifact_bytes` 仍是 sealed BudgetContext 的冻结维度，但
`reserved_artifact_bytes` 在整个 composition result 返回时必须为 `0`。因此该 slice 自身不能生成
`EXECUTION_ARTIFACT_BUDGET`；Artifact reservation/stop 仍属于后继 publisher/derivation closure。

## 5. ProviderRun terminal join

### 5.1 run-local 状态

每个实际 admitted ProviderRun 仍使用：

```text
COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE
```

Provider callable 返回不等于 run `COMPLETED`。candidate validation、canonicalization、run-local ID closure 与当前
Provider child cell 资源关闭均成功后，run 才能提交 `COMPLETED`。

`CUMULATIVE` 禁止因一个 source 成功、为空、失败或不可用而把其他 applicable source 当成不适用。只要没有
whole-attempt terminal stop 或使继续执行不再安全的 release/shared-context/identity failure，controller 必须按
规范顺序继续观察剩余 Provider。valid `PROVIDER_FAILED`、`PROVIDER_UNAVAILABLE`、
`NONCONFORMANT_PROVIDER_OUTPUT`，以及 exact run identity 已知、child 已 residue-free release 的 invalid/no
terminal frame，均是 run-local non-success；普通 required failure 不是 `first failure wins` 的短路权。若 child
无法在共享 release deadline 内 residue-free release，后继 Provider 不得启动。

### 5.2 requiredness 属于 requirement

一个 descriptor 继承其匹配 requirement 的 requiredness；同一 capability 下不能由 caller 把某个 Provider
单独降为 optional。首版机械 join 为：

1. deadline、cancellation 或正向 memory stop 赢得 latch：overall `INTERRUPTED`；
2. 否则任一 required run 为 `FAILED`：overall `FAILED`；
3. 否则任一 required run 为 `UNAVAILABLE`：overall `UNAVAILABLE`；
4. 否则：overall `COMPLETED`。

optional run 的 `FAILED/UNAVAILABLE` 必须保留 ProviderRun 与 typed diagnostic，但不单独覆盖第 4 条。required
`FAILED` 的 rank 高于 required `UNAVAILABLE` 只是机械 outcome priority，不声称 failure 是更深的平台根因。

最终 join 只能提交一次：overall `COMPLETED` 才保留 parent normal eligibility；任何 non-completed overall 都原子
撤销 parent normal eligibility，并仅在第 7.2 节全部条件成立时产生一份不同身份的一次性 diagnostic eligibility。
不得通过清除 required failure、替换 child result 或重建 parent eligibility 重新计算 overall。

whole-attempt stop 后尚未开始的 source 不伪造 started time 或 ProviderRun。该路径没有 R1 Artifact publication
authority；调用层只能得到 typed terminal/cleanup result。没有一个“补齐 unavailable runs”的虚构步骤。

### 5.3 diagnostics 与 final reported IDs

每个 run-local Provider terminal diagnostic 必须绑定 exact `provider_run_id`，在 run-local 与 top-level arrays 中
各出现一次；top-level 数组是全部 run-local terminal tuple 的排序唯一并集。排序继续使用冻结的
`(diagnostic_code, canonical_json_bytes(subject_ref))`。

composition-level identity/protocol integrity failure 若不能诚实归因给一个 ProviderRun，只允许：

```text
diagnostic_code = INTERNAL_DERIVATION_ERROR
subject_ref = null
```

出现在 top-level 一次；不得为了满足 run-local shape 而任选一个无责任 Provider。该规则不把未知根因解释成
Provider failure。

final projection 继续服从：

```text
overall != COMPLETED
  -> every ProviderRun.reported_fact_ids = []
  -> every ProviderRun.reported_relation_ids = []
```

已经完成的 run 可以保留 `COMPLETED` status，但 DIAGNOSTIC file set 不能引用没有发布的 normal Fact/Relation。

## 6. 每个来源先独立关闭，再跨来源组合

### 6.1 run-local admission

每个 Provider 的 candidate 先在自己的 run boundary 内完成文档 137/155 的全部验证：

- candidate shape、anchor、scope、Profile 与 exact bytes 连续；
- application 复算 subject/fact identity；
- duplicate byte-identical semantic Fact 去重；
- run 内同 subject 不兼容 candidate 仍是 `NONCONFORMANT_PROVIDER_OUTPUT`；
- non-completed run 不向 composition stage 提交 canonical Fact；
- completed empty source 提交 observed empty set。

不得通过删除 single-source conflict check 来“支持 multi-source conflict”。只有多个独立、各自 conformance 成功的
run-local Fact set 才进入跨来源 composition。

跨来源 merge 只在所有仍可安全执行的 applicable child cells 已按规范顺序终态并 release 后开始；不得一边运行
后继 Provider，一边让 completion timing 改写 merged identity。whole-attempt stop 或 release/shared-context failure
发生时不进入跨来源 merge。

### 6.2 same ID 的唯一合法 merge

若多个 completed run 报告同一 `fact_id`，application 必须先删除 `provenance_refs` 后比较完整 canonical Fact
semantic object。

```text
same fact_id + byte-identical provenance-free semantic object
  -> one Fact member
  -> provenance_refs = sorted unique union(reporting provider_run_ids)
  -> every reporting COMPLETED run reports that fact_id
```

若 `fact_id` 相同但任一 provenance-free 字段不同，这是 identity collision/integrity failure，不是
`FactConflict`：candidate ID 集无法表达两个不同内容。attempt 以 composition-level
`FAILED / INTERNAL_DERIVATION_ERROR / subject_ref=null` 收束，normal continuation 永久失效。

### 6.3 same subject 的冲突

对全部 merged Fact 按 `subject_key_digest` 分组。一个 subject 出现两个或更多不同 `fact_id` 时：

```text
candidate_fact_ids = sorted unique fact IDs in that subject group
conflict_id = semantic_digest(
  "veritrail.review.fact-conflict/0.1",
  {subject_key_digest, candidate_fact_ids}
)
provenance_refs = sorted unique union(all candidate Fact provenance_refs)
```

所有候选 Fact 都保留在 `facts[]`；一个 subject 恰好产生一个 conflict group。conflict 数组按 `conflict_id` 排序。
Provider priority、requiredness、completion order 或 optional status 均不能选择 winner。

optional Provider 只有在自身 `COMPLETED` 并提交 canonical Fact 时才能参与 conflict；一旦参与，不能因为它
optional 而删除冲突。optional `FAILED/UNAVAILABLE` 不提交 Fact，也不能用失败前 partial candidate 制造冲突。

### 6.4 FactSet 与 provenance 双向闭包

当 overall `COMPLETED` 时，private FactSet construction state 必须同时满足：

```text
Fact.provenance_refs
  = all and only COMPLETED runs that reported this exact fact_id/content

ProviderRun.reported_fact_ids
  = all and only merged Fact IDs reported by that run

every provenance_ref resolves to exactly one ProviderRun
every reported_fact_id resolves to exactly one Fact containing that run provenance
FAILED/UNAVAILABLE run reported IDs are empty
reported_relation_ids are empty
```

`fact_set_digest` 继续使用文档 120 已冻结的 provenance-free projection。完整 FactSet canonical bytes 仍诚实包含
provenance 与完整 `policy_digest`。

## 7. normal、diagnostic 与 conflict-bearing continuation

### 7.1 all required sources terminal-success

所有 required runs `COMPLETED` 时，optional non-success 不阻止 private FactSet construction。optional gap 与
diagnostic 必须保存在后继 final Evidence/Coverage，不能被 FactSet 的成功构造解释成“所有来源完整”。

FactSet 无 conflict 时，controller 可持有 ordinary normal-continuation eligibility。FactSet 有 conflict 时仍是一个
合法、deterministic、conflict-bearing FactSet construction state，但它只允许后继合同保留冲突；不得挑选候选
作为 resolved Fact。

本文不替 Relation 决定局部派生算法。它只保持文档 120 的冻结规则：任何 Fact/Relation conflict 最终都要求
`ReviewSliceSet.slices=[]`，Coverage `SLICE_DERIVATION` denominator 为 `UNKNOWN`，直到未来独立 conflict
isolation 合同另有证明。

### 7.2 required source non-success

任一 required run `FAILED/UNAVAILABLE` 时：

- 不形成 normal FactSet construction state；
- 其他 completed run 的 facts 仍只属于 private attempt construction history；
- final non-success Evidence 清空全部 reported IDs；
- 若没有 budget stop、release 已成功且原 BudgetContext 仍 `RUNNING`，可形成一次性的 future DIAGNOSTIC
  closure eligibility；
- 不得把成功前缀发布成一个更小的 FactSet 或较小 `KNOWN` denominator。

多个 required non-success 仍只形成一个 final Evidence projection，包含所有真实 run status/diagnostics，并按
第 5.2 节机械得出 overall status。

### 7.3 terminal stop 与 unsafe integrity failure

deadline/cancel/memory stop 后只有 cleanup-only permission；没有 FactSet、Evidence 或 Manifest publication。任一
child release failure、shared BudgetContext 破损、same-ID integrity collision 或 binding/descriptor continuity 破坏
时，normal eligibility 不可恢复。run-local invalid/no terminal frame 本身不获得 Fact 权，但在 exact run identity
已知且 child residue-free release 时，可按文档 150 的 `FAILED / INTERNAL_DERIVATION_ERROR` 进入机械 join 并继续
观察后继 source。只有拥有合法 final phase facts且仍满足文档 155 全部资格的 non-budget failure，才可能形成
private Evidence projection。

## 8. 公共 Schema 与 identity 裁决

本合同不升级现有公共 Schema 或 digest domain：

- `ReviewPolicy 0.1` 已能表达 capability-level requiredness 与 `CUMULATIVE`；
- `FactSet 0.1` 已能表达多 run provenance、全部 candidate Facts 与 deterministic conflicts；
- `DerivationEvidence 0.1.1` 已能表达多个 ProviderRuns、optional non-success、整体机械 join 与 non-completed
  reported-ID 空集；
- Provider descriptor 与 run identity 已完整进入 operands/run/Evidence；
- applicability table、private binding handle 与 composition eligibility 不是当前公开 Artifact。

首个实现不发布 Artifact，因此 fixed closed table 可以作为 private conformance authority，而不会把 caller
selection 冒充 Human Seal。若后继 real parser/publication 需要第三方仅凭 Bundle 复算“哪些 Provider 本应适用”，
必须先新增版本化 authorization coordinate 或最小 Schema/Manifest 修正；本文不以 current package code 充当
永久公共 registry。

因此当前 Schema/corpus/vector bytes 必须保持不变。若实现前或 conformance vector 证明任何现有 shape 无法承载
上述合法状态，应停止实现并只重开被单变量反例击穿的最小版本化边界；不得原位改写 `0.1/0.1.1`。

## 9. private owned result

首个实现最多返回一个 private、copy-owned、non-published composition result：

```text
exact applicability/binding tuple
one derivation_id and request provenance
exact input semantic digests
all actual ProviderRun terminal facts
overall execution status
canonical diagnostics
merged canonical Facts and FactConflicts, only when overall COMPLETED
canonical FactSet document/bytes/digest, only when overall COMPLETED
owned final non-success Evidence projection, where eligible
normal / diagnostic / cleanup eligibility as distinct capabilities
```

它没有 output path、Manifest role、public lifecycle、writer 或 standalone publication authority。调用方不能修改
mapping view 后影响 owned bytes；也不能把 private result 序列化、稍后重读并以新 BudgetContext 继续同一次
derivation。

## 10. 最小 conformance matrix

后继获授权实现至少逐格证明：

| ID | 单变量义务 | 预期 |
| --- | --- | --- |
| MP-001 | exact required `python-ast` requirement + exact two bindings | preflight/admission 成功 |
| MP-002 | optional advisory requirement 缺席 | exact required set 仍成立 |
| MP-003 | optional advisory requirement 出现 + exact binding | exact three-binding set 成立 |
| MP-004 | mapping 无 descriptor、binding 缺失/额外/重复 | pre-admission reject；无 run/Evidence |
| MP-005 | descriptor 或 private handle 不匹配 closed table | pre-admission reject |
| MP-006 | ambient entry point/module/global install 存在额外 Provider | 不进入 applicable set |
| MP-007 | caller binding 顺序反转 | normalized execution/semantic result 不变 |
| MP-008 | Provider 各自获得完整 budget | 明确禁止；只消费同一 BudgetContext |
| MP-009 | sufficient budget A/B | same provenance-free Fact/conflict projection 与 fact_set_digest |
| MP-010 | required A empty、required B reports Fact | completed empty source 保留；B Fact 保留 |
| MP-011 | A/B same ID + same semantic object | one Fact；provenance/reporting 双向并集 |
| MP-012 | same ID + different semantic object | FAILED / top-only INTERNAL；不是 FactConflict |
| MP-013 | A/B same subject + different IDs | preserve candidates + one deterministic conflict |
| MP-014 | three candidates in one subject | one sorted conflict group；provenance 全并集 |
| MP-015 | optional completed source causes conflict | conflict 不因 optional 被删除 |
| MP-016 | one Provider internally reports same-subject incompatibility | that run nonconformant；不生成 multi-source conflict |
| MP-017 | required failure then later source | no short-circuit while safe；all truthful terminal runs preserved |
| MP-018 | required FAILED + required UNAVAILABLE | overall FAILED；不声称根因优先级 |
| MP-019 | required unavailable、others completed | overall UNAVAILABLE；no FactSet；final IDs empty |
| MP-020 | optional failed/unavailable、required completed | overall COMPLETED；run/diagnostic retained |
| MP-021 | non-completed overall contains completed run IDs | final projection clears all IDs |
| MP-022 | completed overall bidirectional Fact/run provenance mismatch | conformance reject |
| MP-023 | provider completion order differs from caller order | canonical arrays use frozen ranks, not arrival order |
| MP-024 | deadline/cancel/memory stop during later Provider | one latch；no R1 Artifact；no fabricated unstarted run |
| MP-025 | partial/duplicate/trailing child terminal frame | that run FAILED/INTERNAL + empty Facts；clean release 后按 requiredness join，否则 stop |
| MP-026 | result mapping/candidate arrays modified by caller | owned bytes/state unchanged |
| MP-027 | private result receives output path/publisher/Manifest probe | no such public capability；zero files |
| MP-028 | CPython 3.10/3.13 normal/`-O` | deterministic decisions and semantic bytes agree |

MP-009 不要求完整 FactSet bytes相同：Policy budget、`derivation_id` 与 ProviderRun provenance 是诚实的运行差异；
比较对象是删除 provenance 的 frozen semantic projection 与 `fact_set_digest`。

## 11. 实现分段与停止线

本文只有完成候选远端门、受保护主线合入、exact-main 门、fresh anonymous public readback 与后继独立
docs-only 冻结发布后，才可以按顺序实现：

```text
A. private closed applicability table and exact binding-set admission
B. one shared-budget composition controller + serial single-Provider child cells
C. run-local candidate validation and terminal join
D. same-ID merge / same-subject FactConflict construction
E. bidirectional provenance and final Evidence projection
F. immutable private composition result
G. MP-001..028 hardening
```

每一步都是停止线。A–G 不得创建 real parser、public Provider SPI/discovery、publisher、Relation、Slice、Coverage、
Manifest、CLI 或 Workbench。实现若证明 shared-budget child-cell orchestration、fixed private applicability 或现有
Schema 不能同时满足，必须回到合同；不能通过发明 multi-Provider wire envelope、放宽 identity、忽略 optional
source 或按 first success 继续。

## 12. 候选验收与冻结序列

本文只有满足以下条件才有资格进入独立冻结发布：

1. 文档 159 的十五个反例逐项有唯一裁决；
2. requirement、applicability、descriptor、binding 与 ProviderRun 五个对象不再共用 identity；
3. requiredness 的 capability-level 继承和 exact descriptor cardinality 没有 caller 自由度；
4. 所有 Provider 只消费一个 BudgetContext，且 R1 不借用 Q 的并行/调度 authority；
5. run-local conformance、same-ID merge、same-subject conflict 与 integrity collision 已分开；
6. required/optional join、diagnostic placement 与 final reported-ID 清空规则闭合；
7. conflict-bearing FactSet 不被 Relation/Slice 提前解释；Coverage 不缩小 UNKNOWN denominator；
8. 现有 Schema/corpus/vector bytes 不变有充分理由；
9. diff 只有本文、README、AGENTS 与 milestones 状态入口；
10. 本地 Markdown、状态、敏感路径、exact scope、适用双 Python/`-O` 回归成立；
11. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
12. 新 exact main Public CI、Browser Smoke 与 README/本文/milestones 的 fresh anonymous product readback 成立；
13. 后继独立 docs-only 状态发布完成相同最后门。

只有第 13 项完成后，才可写：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_ALLOWED
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该授权只覆盖第 11 节 A–G，不传播给 public authorization model、real parser、publisher、Relation、Slice、
Coverage、Manifest、CLI 或 Workbench。

## 13. 当前候选裁决与 Fresh-Agent 交接

当前只能写：

```text
R1_FACT_EVIDENCE_CLOSURE_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

新的、没有聊天上下文的 Agent 必须先读文档 113、120、137、140、145、150、155、159 与本文，然后只审计
这些合同能否同时成立。不得把 candidate 解释为 implementation authorization，不得把 private closed table
推广成 public registry，也不得因 Schema 已能表达 conflicts 就直接创建 FactSet publisher。

候选完成后仍要再做一次系统级俯瞰，重点攻击 applicability public verifiability、serial child-cell framing、
parent/run-local eligibility、required failure 后继续观察、composition-level internal diagnostic 与 shared
BudgetContext 连续性。发现新裂缝只说明需要裁决；不自动要求扩大当前合同或为了审计数量修改冻结对象。

## 14. 本地候选证据

候选只允许从 exact baseline 的独立 worktree 建立。至少复核：

1. 当前 Policy、FactSet、DerivationEvidence 0.1.1 与 common Schema 的真实字段；
2. current single-Provider binding、Execution Cell、Fact admission 与 Evidence projection runtime；
3. 既有 compatibility corpus 的 cumulative、conflict、interrupted publication 与 typed gap vectors；
4. relative Markdown links、fence/headings、状态 marker、敏感/本机路径、exact diff scope 与 `git diff --check`；
5. R1 Schema/identity/Evidence focused matrix 在 CPython 3.10/3.13、normal/`-O` 下仍成立。

当前候选的有效本地证据为：

```text
CPython 3.10 normal  133/133  286.497s
CPython 3.10 -O      133/133  284.220s
CPython 3.13 normal  133/133  278.568s
CPython 3.13 -O      133/133  280.299s
```

两套专用 venv 均由各自 exact interpreter 新建，并显式安装 `pywin32==312` 与
`jsonschema==4.25.1`；运行时 `PYTHONPATH` 同时钉住当前 worktree 的 Core src、Review Attention src、plugin tests
与 Core tests。此前复用旧审计 venv 的一次运行因没有 `pywin32` distribution metadata 而产生 57 个环境失败；
首次新建 3.10 venv 的一次运行又因遗漏 `schema-test` extra，在 108 项通过后无法 import
`test_source_snapshot_runtime`。两次均被判为不完整 test-environment coordinate，不计入通过证据，也不解释成
产品失败或用重跑覆盖。

这些证据只证明 docs-only candidate 没有暗改冻结 bytes，不替代本文自己的远端 PR、受保护主线、exact-main
双门、fresh anonymous installed-product readback 或后继独立冻结发布。
