# R1 RelationSet Admission / Explicit Admission Witness / Public Qualification Binding 最小合同 0.1

> 状态：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN /
> R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_ALLOWED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 最初候选基线：`main@1ffc4494dbbb61a056dcc8beed2530e7313f6116`
>
> 当前重新资格化基线：`main@f4aec949258ed16830b2e8dd828273435498764b`
>
> 冻结发布：[文档 185](185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)
>
> 前置审计：[RelationSet Admission / Qualification Evidence Binding 系统审计](182-r1-post-qualification-relation-set-admission-and-evidence-binding-system-audit.md)
>
> 冻结输入：[确定性语义切片合同](113-r1-deterministic-semantic-slice-contract.md)、
> [Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Fact Admission / DerivationEvidence Closure 合同](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)、
> [Relation Derivation Authority / Operand Continuity 合同](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)、
> [Relation Observation / Composition Qualification 合同](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)与
> [Qualification 实现冻结发布](179-r1-relation-observation-composition-qualification-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本合同只冻结 private
> RelationSet admission、explicit admission witness、版本化 Evidence public binding、历史 Schema byte guard
> 与 cross-object conformance；不创建或修改 Schema、corpus、identity vector、runtime、publisher、Manifest、
> Slice、Coverage、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 目的与停止线

冻结的 qualification 能证明：在一个 exact FactSet、Declared Relation Observation Domain 与 required source
责任图下，逐 item observation outcomes 已闭合，candidate composition 已得到 `CONSISTENT` 或
`CONFLICTING`，且结果为 `QUALIFIED`。它仍不授予任何公共 Artifact membership：

```text
QUALIFIED composition
    != admitted RelationSet
    != publicly verifiable admission witness
    != published COMPLETE Bundle
```

文档 182 的 H1/H2/H3 反例又证明：相同 Relation semantics 可以来自不同合格 attempts；相同 raw candidates
也可以来自合格与未合格历史。`relation_set_digest` 稳定、RelationSet 文件 bytes 带各自 provenance 都是正常
现象，但二者都不能独立证明 admission authority。

本合同只关闭下列接缝：

```text
exact owned QUALIFIED result
    -> deterministic admission eligibility
    -> exact RelationSet membership / conflict / provenance closure
    -> private admitted RelationSet value
    -> explicit admission witness
    -> versioned public Evidence binding shape
```

首个实现即使以后获授权，也只建立 private、copy-owned、non-published proof，并分阶段实现 Schema/corpus。
它不创建输出目录、不写八文件 Bundle、不开始 Slice/Coverage，也不把 Schema-valid 或 witness presence 当成
publication authority。

## 2. 五层 authority 必须分开

```text
Relation observation
  Provider 对 assigned item 报告 outcome 与 candidate

Composition qualification
  application 验证责任域、terminal、outcome、candidate 与 conflict 已闭合

RelationSet admission
  application 决定 exact qualified members 能否进入一个 normal RelationSet

Admission witness
  application 对这一次 admission 的 exact history 与成员闭包形成可复算声明

Public binding / publication
  versioned Evidence 承载 witness；Manifest 绑定最终文件；publisher 另行取得写入资格
```

因此：

```text
content identity reusable        != admission authority reusable
qualification digest valid      != RelationSet membership valid
RelationSet Schema-valid        != admitted
witness present                 != witness conformant
Evidence carries witness        != Evidence owns admission decision
Manifest binds bytes            != Manifest judges eligibility
admitted RelationSet            != Slice/Coverage eligible
```

Human Seal 继续只拥有 Policy/Profile 与 requiredness。Provider 只拥有 bounded observation。deterministic
application 是 admission rule 与 witness construction 的唯一所有者；Evidence 只是 versioned carrier，Manifest
只是 file binder，二者都不能自我签发 eligibility。

## 3. admission eligibility 与 fail-closed gate

### 3.1 唯一正向输入

首个 admission 只接受文档 175/179 冻结的 `OwnedRelationCompositionQualificationResult`，且必须逐项复核：

```text
qualification_status                  = QUALIFIED
required_source_set_terminal_closure  = COMPLETE
required_observation_closure          = COMPLETE
candidate_composition_status          in {CONSISTENT, CONFLICTING}
reason_codes                          = []
all Fact and Relation phases          copy-owned and terminal
all participating child release       = RELEASED
same derivation/input/domain identities remain exact
qualification_digest                  recomputes from the frozen 0.1 projection
```

`NOT_QUALIFIED`、`INTEGRITY_FAILED`、`NOT_COMPOSED`、缺失 phase、release failure、shared stop、identity
collision 或任何 owned bytes/digest 不一致都必须在 RelationSet construction 前 fail closed。不得从 raw phase
candidates、ProviderRun `COMPLETED`、Schema-valid candidate 或 caller-supplied digest 绕过 qualification。

admission 重新机械验证 frozen qualification；它不重新运行 Provider，不读取 path/ambient registry，不补 outcome，
不改变 candidate，也不重新解释 closed responsibility table。

### 3.2 admission 不是 publication

正向 gate 只形成 private admission eligibility。它不创建 `relation-set.json`、final Evidence、Manifest 或文件
reservation。后继 staging/release 失败不能把已经算出的 private bytes 自动变成 Artifact。

## 4. RelationSet exact membership closure

admission 必须从同一个 qualified owned result 重新建立 `RelationSet 0.1` document，并满足：

1. `source_snapshot_digest / policy_digest / analysis_scope_digest / derivation_profile_digest /
   fact_set_digest` 与 exact qualification/Facts 连续；
2. `relations` 恰等于 qualification 的 merged candidates，按 `relation_id` 排序且唯一；不得遗漏、额外加入、
   用 raw pre-reconciliation candidate 替换，或按 Provider priority 选 winner；
3. 每个 Relation 的 subject/identity/endpoint/target 按冻结 Profile、FactSet 与 Relation identity domain 复算；
4. same-ID candidate 只合并 provenance，`provenance_refs` 恰等于所有 accepted outcomes 报告该 ID 的
   `provider_run_id` 排序唯一并集；
5. 每个 provenance ref 必须解析到本次 qualification 的 exact Relation ProviderRun；反向上，每个 Relation
   ProviderRun 的 final `reported_relation_ids` 必须恰等于其 accepted outcomes 的 candidate IDs；
6. `conflicts` 恰等于 same-subject incompatible Relation IDs 的规范分组；每个 conflict 保留全部候选、规范
   `conflict_id` 与候选 provenance 并集；
7. `relation_set_digest` 继续按文档 120 的 provenance-free `veritrail.review.relation-set/0.1` 投影复算；
8. 完整 RelationSet canonical bytes 可以因独立 attempt 的 provenance 不同而不同；这不改变 content identity，
   也不允许一次 attempt 继承另一次 admission。

`RelationSet 0.1` 不新增 `admission_status`、`qualification_digest` 或 witness 字段。它保存语义内容与诚实
provenance，不负责证明自己的准入合法性。

## 5. conflict-bearing QUALIFIED 的唯一裁决

`QUALIFIED / CONFLICTING` 允许形成 admitted RelationSet，因为 qualification 与 conflict 是正交维度：

```text
observation responsibility closed = yes
candidate disagreement present    = yes
winner selected                    = no
```

此时 RelationSet 必须保留全部 incompatible candidates 与 conflict records。admission witness 也必须绑定
`candidate_composition_status=CONFLICTING` 及 exact conflict IDs，不能改写为 `CONSISTENT`。

但该 admission 不授予 normal traversal。下游 gate 必须由公开的 composition/conflict 状态机械得出：

```text
future normal Slice gate = BLOCKED_BY_RELATION_CONFLICT
ReviewSliceSet.slices    = future empty projection only
Coverage relation/slice denominator = future UNKNOWN with conflict reason
```

本合同只冻结这个下游 gate，不构造 ReviewSliceSet/CoverageLedger，也不决定后继文件 publication。未来 Slice/
Coverage 合同若需要不同表示，必须用新反例重开该最小条款，不能在 admission 中静默选 winner。

## 6. explicit admission witness

### 6.1 witness claim

witness 只声明：

> 对一个 exact derivation history，application 已复算 qualification closure，并按本合同把 exact qualified
> Relation members/conflicts 接纳为这一份 RelationSet。

它不声明 Relation 是现实真相，不证明 Provider 内部认知过程，不提高多来源一致的事实权威，也不证明 Slice、
Coverage 或最终 Verdict。

### 6.2 可复算 public projection

为让第三方不依赖 private runtime object，witness public value 必须包含：

```text
witness_version = 0.1

observation_domain
  完整 canonical DeclaredRelationObservationDomain 0.1
  含 Fact-backed items、exact responsibilities 与 observation_domain_digest

qualification_claim
  provider_run_terminals[]
  observation_receipts[]
  required_source_set_terminal_closure
  required_observation_closure
  candidate_composition_status
  qualification_status = QUALIFIED
  merged_candidate_relation_ids[]
  private_conflict_ids[]
  reason_codes = []
  qualification_digest

admission_claim
  derivation_id
  source_snapshot_digest
  policy_digest
  analysis_scope_digest
  derivation_profile_digest
  fact_set_digest
  observation_domain_digest
  qualification_digest
  relation_provider_run_ids[]
  admitted_relation_ids[]
  admitted_conflict_ids[]
  relation_set_digest
  admission_witness_digest
```

`qualification_claim` 除 `qualification_digest` 外的字段恰为冻结
`veritrail.review.relation-composition-qualification/0.1` payload；保留其中历史字段名
`private_conflict_ids` 是为了逐字节复算既有 identity，不表示 public verifier 依赖 private state。

`admission_witness_digest` 固定为：

```text
domain  = veritrail.review.relation-set-admission-witness/0.1
payload = admission_claim without admission_witness_digest
```

该 identity 有意包含 `derivation_id`、exact ProviderRun IDs、`qualification_digest` 与 Policy coordinate，因此
两个 attempts 即使共享 `relation_set_digest`，也必须具有各自 witness。它不包含
`derivation_evidence_digest`，避免 witness 与外层 Evidence identity 形成循环。

### 6.3 第三方 conformance

第三方必须能只用完整 Bundle 中的 SourceSnapshot、Policy、Profile、FactSet、RelationSet 与 Evidence 复算：

1. observation domain 的 item/responsibility identity 与 exact FactSet/Policy/Profile 闭合；
2. qualification claim 的 terminals 与 Evidence 中 exact Relation ProviderRuns 闭合；
3. receipts 的 assignments、outcome identities、candidate refs 与 RelationSet members 双向闭合；
4. qualification digest、admission witness digest 与 RelationSet digest 各按自己的 domain 成立；
5. Evidence final `reported_relation_ids`、witness admitted IDs 与 RelationSet membership 三者完全相等；
6. same-ID provenance、conflict membership 与 reverse provider-run closure 成立。

只携带 `qualification_digest`、只携带 Relation IDs、或只由 Manifest 指向两个文件都不足以形成 witness。

identity dependency 必须保持单向且无环：

```text
FactSet + ObservationDomain + ProviderRuns/outcomes
    -> qualification_digest

qualification + exact members/conflicts
    -> RelationSet 0.1 + relation_set_digest

qualification + RelationSet identity/membership
    -> admission_witness_digest

ProviderRuns + witness + final outcome
    -> DerivationEvidence 0.2 + derivation_evidence_digest

final file bytes/digests
    -> Manifest 0.1 entries
```

RelationSet 不反向引用 witness，witness 不引用 Evidence digest，Manifest 不进入任何子 Artifact semantic identity。

## 7. public binding 选择：DerivationEvidence 0.2

### 7.1 为什么选择 Evidence carrier

首个 public encoding 选择 versioned `DerivationEvidence 0.2` root required field：

```text
relation_admission: <explicit admission witness object> | null
```

理由是 witness 本质上绑定一个 exact derivation attempt、ProviderRuns 与 final reported arrays；这些坐标已由
Evidence 拥有。把它编码在 Evidence 可以保持 Manifest 的八文件 topology，不新增第九个仅为重复 attempt
坐标而存在的 Artifact。

这个选择只决定**存放位置**：application 先形成 private admitted value 与 witness，Evidence assembler 后续只
copy-own 并序列化已成立的 witness。Evidence 不能从 RelationSet presence、digest 或自己的
`overall_execution_status` 反向签发 witness。

### 7.2 0.2 shape 与 identity

`DerivationEvidence 0.2` 以冻结的 `0.1.1` closed shape 为基线，新增上述 required field，并使用新的 semantic
identity domain：

```text
schema_version = 0.2
domain         = veritrail.review.derivation-evidence/0.2
payload        = complete Evidence document without derivation_evidence_digest
```

规则固定为：

```text
overall_execution_status = COMPLETED
  -> relation_admission must be a conformant witness object
  -> all final reported Relation IDs resolve exactly once

overall_execution_status in {INTERRUPTED, FAILED, UNAVAILABLE}
  -> relation_admission = null
  -> all final reported Fact/Relation IDs remain empty
```

首个 reference implementation 不获得 diagnostic publication authority；`null` 只冻结 future shape 与 fail-closed
关系，不能借此为当前 private 失败新建 Artifact。

### 7.3 历史 byte guard

以下文件与 identities 必须逐字节保留：

```text
review-derivation-evidence-0.1.schema.json
review-derivation-evidence-0.1.1.schema.json
all existing 0.1/0.1.1 correction corpus and identity vectors
veritrail.review.derivation-evidence/0.1
```

后继 Schema 实现必须新增 `review-derivation-evidence-0.2.schema.json`、独立 correction/admission corpus 与新的
0.2 identity vectors，不能改写旧 fixture 让历史 Evidence 看起来拥有 admission。历史 0.1/0.1.1 Evidence
仍是其原合同下的合法样本；它不能在 admission-capable runtime profile 中与新 RelationSet 组合并冒充 0.2
complete Evidence。

## 8. Manifest 0.1 保持 binder

当前没有反例要求第九文件或新 role。`Manifest 0.1` 继续只做：

```text
DERIVATION_EVIDENCE entry
  -> exact derivation-evidence.json bytes / size / semantic digest

RELATION_SET entry
  -> exact relation-set.json bytes / size / semantic digest
```

完整 Bundle conformance validator 再读取两个已绑定文件，复算第 6 节的 cross-object closure。Manifest 看到
八个文件、正确 SHA-256 与 semantic digests，仍不能单独推出 witness 合法。

Manifest Schema、role、path、八文件顺序与 diagnostic 四文件顺序本轮保持逐字节不变。若后继实现证明
Evidence carrier 无法形成充分、无环、可复算绑定，必须停下并用新反例重开 encoding 选择；不得顺手添加
第九文件。

## 9. qualification 后失败与历史保留

以下历史必须分开：

```text
Provider phases / outcomes / private qualification
    已发生的 observation history

private admission eligibility / witness construction
    application 后继动作

Artifact staging / publication
    尚未授权的外部事实
```

qualification 已成功，但 admission membership、witness construction、final Evidence projection、artifact budget、
staging、release 或 cleanup 任一失败时：

- 原 private phase/receipt/qualification bytes 保持不变；
- 不形成 normal admitted RelationSet 或 conformant non-null public witness；
- 若未来另有合同允许 diagnostic Evidence，final reported Fact/Relation IDs 必须为空，`relation_admission=null`；
- 不得把 partially built RelationSet、witness 或 staging prefix 发布为 normal Artifact；
- 后继成功 attempt 不解释或覆盖早先失败。

## 10. `RAE-000..010` 的唯一裁决

| Falsifier | 本合同裁决 |
| --- | --- |
| `RAE-000` H1/H3 raw candidates 相同 | H3 非 `QUALIFIED`，admission gate 前拒绝；零 RelationSet/witness |
| `RAE-001` QUALIFIED / CONSISTENT、成员精确相等 | 可形成 private admission/witness；仍无 publication |
| `RAE-002` 只有 qualification digest | 缺 domain/receipts/run/member closure，cross-object reject |
| `RAE-003` RelationSet 少/多一个 candidate | membership equality reject，不缩小 qualified set |
| `RAE-004` provenance 指向错误 run | reverse closure reject |
| `RAE-005` QUALIFIED / CONFLICTING | admission 允许；全部 candidates/conflicts 保留，无 winner；Slice gate blocked |
| `RAE-006` historical Evidence 0.1/0.1.1 | 不能冒充 admission-capable Evidence 0.2 |
| `RAE-007` non-COMPLETED 或后继失败 | no normal RelationSet；future final arrays empty；witness null |
| `RAE-008` RelationSet valid、witness 缺失 | admission-capable complete-bundle conformance reject |
| `RAE-009` 两个独立合法 attempts、同 semantics | relation_set_digest 可同；provenance bytes、witness、Evidence 各自成立 |
| `RAE-010` Manifest 精确绑定、witness 无效 | Manifest 不补 eligibility；cross-object reject |

后继实现还必须加入：

| ID | 单变量世界 | 预期 |
| --- | --- | --- |
| `RAE-011` RelationSet 自报 `admission_status` | RelationSet 0.1 closed Schema reject；不构成 witness |
| `RAE-012` Evidence 内 witness bytes 正确但由 caller 构造、无 admitted private value | application API 无此入口；reject |
| `RAE-013` witness 从 H1 复制到同 semantic H2 | run/qualification/provenance closure reject |
| `RAE-014` qualification claim 改一个 receipt/outcome 后只重算 Evidence digest | qualification/witness digest reject |
| `RAE-015` conflicting composition 删除一个候选或选 winner | admission reject；normal slice 仍 blocked |
| `RAE-016` Evidence/witness 互相包含 digest | contract/schema review reject identity cycle |
| `RAE-017` eighth-file Manifest 改为 ninth-file shortcut | historical Manifest byte guard reject |

## 11. 实现分段与停止线

本合同只有完成候选门、受保护主线合入、新 exact-main 双门、fresh anonymous public readback 与后继独立
docs-only 冻结发布后，才可严格按顺序实现：

```text
A. private admission gate and exact RelationSet construction state
B. same-ID provenance / conflict / reverse-run conformance
C. private explicit admission witness construction
D. DerivationEvidence 0.2 Schema + independent corpus + identity vectors
E. private non-published Evidence 0.2 projection boundary
F. RAE-000..017 hardening and cross-runtime byte proof
```

A–C 不依赖公共文件；D 只能新增版本化 Schema/corpus；E 不得提前生成 provisional `COMPLETED` Evidence，只有
future final outcome 所需的全部上游值已经存在时才能建立 new-copy projection。任何一步若要求 publisher、
Manifest role 扩张、Slice 或 Coverage 才能成立，立即停止并重开最小合同边界。

完成 F 仍不得实现：

- output path、artifact reservation/writer、八文件 publication 或 Release；
- standalone admission Artifact、第九 Manifest role/file 或 Manifest judge；
- full import resolution、public Provider SPI/registry/discovery；
- ReviewSlice traversal、CoverageLedger、Attention ranking；
- CLI、Workbench、Core、P/Q/D/Cu/O/T。

## 12. 候选验收与冻结序列

本文只有满足以下条件才有资格进入冻结发布：

1. 文档 182 的十二个待裁决问题与 `RAE-000..010` 均有唯一答案；
2. admission rule、witness owner、public carrier 与 Manifest binder 四种 authority 分离；
3. RelationSet membership/provenance/conflict 与 Evidence final arrays 的双向闭包可机械复算；
4. conflict-bearing `QUALIFIED` 保留 disagreement，并明确阻止 normal Slice traversal；
5. witness projection 足以复算 qualification 与 admission，不依赖 private runtime object；
6. Evidence 0.2 identity 无循环，历史 0.1/0.1.1 bytes 与 domain 不变；
7. Manifest 0.1 保持八/四文件 binder 有充分反例依据；
8. private admission、Schema/corpus、Evidence projection 与 publication 分段授权；
9. diff 只有本文、文档 182 closure 与必要 README/AGENTS/map/milestones 状态同步；
10. 本地 Markdown、链接、状态、敏感与适用文档门成立；
11. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
12. 新 exact main Public CI、Browser Smoke 与 README/本文/milestones 的 fresh anonymous 产品读回成立；
13. 后继独立 docs-only 合同冻结发布完成同样最后门。

只有第 13 项完成后，才可写：

```text
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_ALLOWED
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

## 13. 冻结裁决与 Fresh-Agent 交接

本文 original head `cffd64d941b76bdae746fab4190d5c56c1d33366` 的 Public CI run `35629971691`
attempt 1 保留 Python 3.10 `-O` 首败；其精确原因仍为 `UNKNOWN`。独立 maintenance 已经由 PR #172、
`main@f4aec949258ed16830b2e8dd828273435498764b` 及该 exact main 双门取得资格。本文正从该新 source state
形成新 head；maintenance 的成功不解释旧失败，新 head 必须独立满足第 11–12 项。

PR #171 的新 head `53d4b9991e0df4a3c0328e7426f9c7de23c31d67` 已在 maintenance-qualified
source state 上重新接受两次同-head 11/11，合入 `main@9299c24fdde489957cb39dfc687296ea3dc59718` 后又完成
exact-main 11/11、Browser Smoke 1/1、三份 fresh anonymous paired readback 与能力地图 render-only readback。
[文档 185](185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)保留完整因果链，
包括第一次 README 匿名配额首败。该状态发布自己的最后门全部成立后，当前状态为：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_ALLOWED
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

新的、没有聊天上下文的 Agent 必须先读文档 113、120、155、165、175、179、182、本文与文档 185，并先
审查这些合同能否同时成立。实现授权只覆盖第 11 节 A–F 的 private closed proof；不得因为 Evidence 0.2
carrier 已冻结就提前创建 publisher、公共 Bundle、Slice 或 Coverage，更不得把 admission 当成 Relation
correctness、Slice eligibility、Coverage COMPLETE 或 final Evidence publication。

当前原则冻结为：

> Same semantic content may be re-observed; admission authority must be independently established for each
> admissible publication history.

中文：**内容身份可以复用，来源历史可以不同，但准入资格必须逐次成立，不能因为字节或语义摘要相同而继承。**
