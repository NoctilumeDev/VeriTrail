# R1 Fact handoff → Relation corrected successor 私有实现授权发布

日期：2026-10-19

> 状态：`R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 基线：`main@e8171b93b526f16ca2dee0c90537780cec91a212`，tree
> `482b63e78c663fddbbe6c4fb79fcfce9cb997f5e`。
>
> 上游：[interoperability correction 合同](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)、
> [stage applicability capability identity 修正合同](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)与
> [corrected successor 私有实现可行性审计](296-r1-fact-relation-corrected-successor-private-implementation-feasibility-audit.md)。
>
> 影响：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`；docs-only。
> `CORRECTION_IMPLEMENTATION_ALLOWED` 仅为条件目标，本文最后门全部闭合以前不生效；runtime、tests、Schema、
> manifest successor、persistence、Coverage、public Review 产品与 R2/R3 均不启动。

## 1. CONTROL LOOP 与当前 authority

文档 296 由 PR #341 final head `34fba6ca71122d8a71a55ddf98567486744fa189` 合入本基线：

```text
base  = b293b263c85fec36164830869c76f560cad8cb2d
head  = 34fba6ca71122d8a71a55ddf98567486744fa189
merge = e8171b93b526f16ca2dee0c90537780cec91a212
tree  = 482b63e78c663fddbbe6c4fb79fcfce9cb997f5e
```

original Public CI `39241157801`、exact-main Public CI `39247733436` 与 Browser Smoke `39247733582`
均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1。fresh anonymous installed-product README、doc296、
milestones 各有一份 qualifying PASS。README formal #1 的 P1 API 为 COMPLETE，但 P2 public render navigation timeout，
保留为 `FORMAL_READBACK_ERROR`；fresh formal #2 才取得 README PASS，不能覆盖前一身份。

independent reconciliation 与 142-artifact closeout 分别为：

```text
bad8c6125ef0e0432d2d81568c0f41edfed7be1e2732857fd5d356d39ac5340f
5b0861c6b1ee31cf09ff5f907ae52e0f0d4627b31d69544bd052db4ecce8041a
```

第一次 pre-formal validation 错误假定上游 closeout 会把自身正在写入的 stdout 纳入封存，保留为
`UPSTREAM_CLOSEOUT_SELF_CAPTURE_ASSUMPTION_SETUP_ERROR`；fresh attempt 2 只修 proof-facility assumption，未修改
产品 oracle、target、预算、合同或正式 observation。doc296 full-file SHA-256 为：

```text
bb9d46ca81498cdb5d390418da73e0e079ffda91654675af0daae51ce5d3a045
```

因此以下事实已经成为 qualified history：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

fresh CONTROL LOOP 重新核对 remote main、主仓、open PR、doc290/doc294/doc296、Fact handoff、Relation
domain/request/Provider 与保留 artifacts。remote main 与本基线相同，open PR 只有依赖更新；PR #341 是四文件 docs-only
publication，没有 runtime、tests、Schema、Profile、Policy、Provider 或 manifest 漂移，也没有并行 semantic implementation。

没有新反例击穿 doc296 的 bounded feasibility。当前最小合法候选仍是：只发布 doc296 §7 A–J 的 private implementation
authority。本轮不重做 feasibility，不实现 successor，也不把历史 composition `ALLOWED` 恢复成可消费 authority。

## 2. feasibility witness 不冒充 runtime

文档 296 的 read-only audit 证明以下有限路线可表达：

```text
exact immutable DerivationInputSet
+ claimed Fact handoff
+ original live BudgetContext
    -> same-world join
    -> stage-scoped Policy applicability
    -> complete per-product closure
    -> complete Relation obligation projection
    -> bounded successor carrier / qualification / admission
```

它同时证明 current Relation domain `/0.1` 与 request protocol `/0.2` 不能无损表达该 successor。现有 closed Relation
Provider algorithms 只有在 application 已经完整构造并分配 obligations 后才可复用。five-kind single-path 与 two-path
witness 中，完整 FactSet bytes/digest 均未改变；profile-non-applicable Facts 仍保留 identity。

四格 CPython 3.10.6 / 3.13.13、normal / `-O` 的 fresh attempt 2 semantic digest一致：

```text
27de95e632aaee5b6ef26ac332846184ac79b5011f319ce4d34152c53e003eaa
```

nonce canonicalization setup error 与相对 PYTHONPATH invocation error继续保留。现有窄回归四格各
`Ran 77 tests / OK (skipped=1)`，即 76 passed、1 skipped；测试只作 witness，不拥有 implementation authority。

因此：

```text
bounded feasibility
    != implementation authority
    != implementation started
    != implementation qualified
    != old composition authority restored
```

## 3. 条件化的最小施工面

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多落实文档 296 §7 的 A–J：

| ID | 最大施工面 |
| --- | --- |
| A | 由 application 建立一个 private composition attempt，绑定 exact `DerivationInputSet`、一次领取的 Fact handoff 与其原始 `BudgetContext`；不创建第二个 Fact claim 或新 context |
| B | 在 Relation work 前逐项复核 exact input、safe branch、Fact terminal history、FactSet 或 qualified absence、live object identity 与 same-world join；digest-only 或 consumed claim fail closed |
| C | 构造 `/0.2` Fact / Relation applicability documents 与 total、disjoint、exactly-once cross-stage ownership reconciliation；unknown、gap、overlap、duplicate、missing 与 requiredness drift均停止 |
| D | 对完整 FactSet 建立 total per-product/path closure；每个 accepted product/path 恰好一个 MODULE，Import 只绑定同 path MODULE，全部其他 Facts 保持原 identity |
| E | 从完整 F、sealed Policy、Relation Profile 与 closure 独立构造 `O_expected`，再生成 per-Provider responsibility；不得从 candidates、Provider output 或 representable subset反推 denominator |
| F | 增加可区分的 private successor domain/request/terminal carrier，绑定完整 F、applicability、ownership、closure、expected/assigned obligations、exact source blobs、provenance 与 same attempt；legacy bytes不变 |
| G | 复用现有 closed Relation Provider algorithms，只执行 application明确分配的 obligations；Provider不能定义 applicability、修改 FactSet 或取得未分配责任 |
| H | 独立核对 expected/emitted 双向相等、每个 assigned obligation恰好一个 terminal outcome、Provider requiredness、same attempt、request provenance 与完整 terminal history，再形成 successor admission |
| I | 仅在全部 required reconciliation完成后产生 one-shot private continuation；它不取得 manifest、persistence、Coverage、public product、Evidence 或 publisher authority |
| J | 固化 `FRIC-000..018`、`FRIC-CID-001..012`、foreign-policy、consumed claim、FactSet filter、global multi-MODULE、cross-path parent、missing/duplicate/foreign obligation 与 legacy-byte guards，并保留四格 canonical reports |

实现文件布局、Python class、field、protocol suffix与测试数量不属于本授权。允许增加 bounded、versioned、private successor；
不允许把 application-only projection写成新的 Fact truth，也不允许让 current legacy carrier悄悄扩大含义。

## 4. 必须保持的 authority ceiling

后继实现不得：

- 过滤、重算或替换 authoritative FactSet，或删除 profile-non-applicable Facts；
- 改写 sealed Policy，只向 Provider传一份缩小 Policy，或让 Provider自行选择 stage applicability；
- 从 emitted candidates、Provider terminal output 或实际成功项反向生成 `O_expected`；
- 只证明 emitted obligations 可追溯，却不证明 expected/emitted cardinality与成员双向相等；
- 把全局 `exactly one MODULE`粗改成`one or more MODULE`，或允许 Import跨 path借用 parent MODULE；
- 创建第二个 Fact claimant、新 `BudgetContext`、Fact rerun，或用相同 bytes/digest/limits/result恢复 live authority；
- 修改 legacy domain/request/history、doc290–296、frozen fixtures/corpus、Profile、Policy、Provider public surface或 Schema；
- 恢复旧 ReviewSliceSet/Coverage composition A–J，选择 manifest successor 或 persistence Route A/B；
- 启动 Coverage、public Review product、Evidence、Bundle、publisher、CLI、Workbench、Core、R2/R3、
  CLAIM_FIDELITY、post-R1 Benchmark、tag 或 Release。

Fact owns完整 Fact truth；application owns stage applicability、obligation projection、assignment、qualification与 admission；
Provider只观察 assigned obligations。`P` 与 `A_s(P)`、`F` 与 `O_R(F)` 的身份必须始终分开：applicability说明本 stage
该管什么，不把世界改写成只剩什么。

## 5. implementation stop conditions

授权生效以后，施工出现以下任一条件必须保留反例并停止，只重开被击穿的最小边界：

1. exact input、claimed handoff 与 original context无法在消费前机械绑定到同一 world；
2. 必须创建第二个 Fact claim、新 context或重跑 Fact才能进入 Relation；
3. 必须过滤 FactSet、改写 Policy或让 Provider定义 applicability；
4. 现有 Relation Provider algorithms在合法 assignment下仍不能处理完整 five-kind或multi-path world；
5. successor carrier无法无损绑定 ownership、per-product closure、完整 obligation denominator与same-attempt provenance；
6. complete projection只能依赖 Provider自证、caller bool、digest holder、actual outputs或跨 attempt result；
7. 必须修改 legacy bytes、public Schema、manifest或persistence才能闭合 private successor；
8. direct falsifier击穿 doc290/doc294 frozen semantics，而不是暴露局部 implementation defect；
9. 只有弱化 oracle、删除 negative history或移动成功条件才能取得 PASS。

已经生效的授权也不能成为扩大 scope、修 oracle、静默 reopen frozen contract 或覆盖首败的理由。

## 6. 本 publication 的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/297-r1-fact-relation-corrected-successor-private-implementation-authorization-publication.md
docs/milestones.md
```

doc290–296、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、Provider、vectors、corpus与
post-R1计划必须保持 `e8171b93…` base bytes。final bytes至少完成四文件 scope、UTF-8 without BOM、LF/final LF、
links/fences/headings、marker、doc296与上游 byte continuity、`git diff --check`、read-only hygiene及声明的 Markdown baseline checks。

随后仍需：

```text
final docs-only authorization publication bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc296 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CORRECTION_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

same patch、tree、content、digest、semantic result或feasibility witness不能替代上述任一资格身份。本地主仓 fast-forward
只作 housekeeping，不增加授权生效门。

## 7. 生效前后与实现自己的门

本文第 6 节全部门闭合以前，只允许发布：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

最后门闭合以后，状态上限是：

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_ALLOWED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
```

旧 composition authorization仍只是历史事实，不能因为本 successor authority生效而自动恢复消费。必须重新绑定新的 exact main、
核对并行事实、current runtime与本节 stop conditions，并确认 A–J仍是最小合法 seam，才可创建 implementation branch。

后继 implementation必须取得自己的 final bytes、local gates、original PR资格、单独批准的 exact-head merge、new exact-main
双门、fresh installed-product readback与独立对账；这些门闭合以前最多是 implementation candidate，不能写 frozen，也不能进入
旧 composition、manifest、persistence或Coverage。

## 8. 当前裁决

```text
stage capability identity correction contract
    FROZEN

corrected successor feasibility
    AUDITED / QUALIFIED_HISTORY

corrected successor authorization publication
    CANDIDATE

corrected successor implementation authority
    NOT_AUTHORIZED

corrected successor implementation
    NOT_STARTED

old composition authorization
    ALLOWED_HISTORY_PRESERVED / NOT_CONSUMABLE

manifest successor
    NOT_SELECTED / NOT_AUTHORIZED

persistence
    OPEN / NOT_SELECTED

Coverage / public Review / R2 / R3
    NOT_STARTED
```

本文只发布一段有界的 private implementation authority。它不证明代码已经存在，不证明实现将成功，也不改变任何 frozen
upstream truth；如果后继反例证明该 A–J 无法在 authority ceiling内实现，正确结果是停止并返回 CONTROL LOOP。
