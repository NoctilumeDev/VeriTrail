# R1 Fact handoff → Relation corrected successor 私有实现可行性审计

日期：2026-10-19

> 状态：`R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 坐标：`main@b293b263c85fec36164830869c76f560cad8cb2d`，tree
> `96a3c9ac52d1ee72561302b8af1e39197f5a5246`。
>
> 上游：[Fact handoff → Relation interoperability correction 合同](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)、
> [stage applicability capability identity 修正合同](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)与
> [独立冻结发布](295-r1-fact-relation-stage-applicability-capability-identity-correction-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只审查冻结语义能否由现有 private primitives 与一个有限、可区分的
> successor boundary 实现；不修改 runtime、tests、Schema、Profile、Policy、Provider、manifest、persistence、Coverage 或
> public Review 产品，也不授权实现。

## 1. CONTROL LOOP 与 exact source state

文档 295 由 PR #340 final head `80c299b383d66f442d1710b4502cd9baf23489d2` 合入当前主线。其 original Public CI
`39227323668`、exact-main Public CI `39234418094` 与 Browser Smoke `39234418220` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1。fresh README、doc294、doc295、milestones 为 4/4 qualifying PASS；independent reconciliation
与 147-artifact closeout 分别为：

```text
c7f941274b1824948f07c0a55cf22b6508b60a54218df9d03d12c3e01dde72db
a0918ed18de68b5a2352d16a17f5eb9a369f51f26313a51720826bcfd5c0056c
```

因此以下上游事实已经生效：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

fresh CONTROL LOOP 重新核对 remote main、open PR、冻结合同、Fact handoff、Relation domain/request/Provider 与相关 tests。
remote main 仍为上述 exact coordinate，open PR 只有依赖更新，没有并行 semantic PR 已经实现该 seam。没有新证据要求重开
Fact truth、Relation observation semantics、doc290 的 per-product closure / obligation projection或 doc294 的 owner map。

## 2. 当前 one-shot claim 可以拥有整段 composition attempt

`OwnedProductFactClosure` 只有一个 live source claim。`claim_continuation()` 会以 `LEGACY_CONTINUATION` 消费它，
`_claim_handoff_source()` 会以 `COVERAGE_HANDOFF` 消费它；两个 claimant 互斥且只能有一个 winner。

这不是本 successor 的 blocker。冻结的 handoff consumer identity：

```text
veritrail-review-private-coverage-composition/0.1
```

拥有的是未来完整 private composition attempt。corrected Relation successor 必须在该 attempt 内消费已经 claimed 的 handoff；
它不创建第二个 Fact claimant，也不从 FactSet digest、序列化文档或相同 semantic result恢复 live authority。

claimed handoff保留：

```text
branch
exact input identity
parse partition
Fact projection U / E / blockers
Provider terminal history
FactSet or qualified absence
whole-attempt budget history
original live BudgetContext object
```

本轮机械审计确认 claimed handoff 与原 closure 使用同一个 `BudgetContext` object。相同 limits、deadline 值或序列化字段仍不能
替代这个对象身份与 one-shot claim history。

## 3. handoff 与 exact DerivationInputSet 必须显式 join

handoff source 按冻结边界没有携带 source blob bytes，也不是一份 `DerivationInputSet`。现有 Relation worker 需要 exact source
blobs 执行观察。因此 successor composition attempt必须同时拥有：

```text
exact immutable DerivationInputSet I
+
claimed Fact handoff H
+
H 的 original BudgetContext C
```

application 在任何 Relation work开始前必须机械复核至少：

```text
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
slice_policy_digest
classification identity
Fact consumer attempt identity
Fact product-set identity
```

审计构造的 same-world join通过；只改变 Policy identity的 foreign-world join被拒绝。该结果证明一个有限 join可表达，不证明任意
digest holder、foreign attempt或重新取得的 blob bytes拥有 claim authority。I 只提供 exact immutable semantic input；H 与 C 才携带
本次 continuation authority。

## 4. current Relation carrier 不能表达冻结 successor

当前 Relation observation domain `/0.1` 是 intentional closed shape：

```text
exactly one MODULE globally
all Facts are MODULE or IMPORT_DECLARATION
```

因此完整 five-kind FactSet 与 multi-product / multi-path FactSet均被当前 domain正确拒绝。这个拒绝不是 Provider algorithm failure，
也不能通过过滤 FactSet或把全局 `one MODULE`改成粗糙的 `one or more MODULE`来规避。

当前 request protocol `veritrail-review-relation-cell/0.2` 也没有无损携带以下冻结输入：

```text
parent correction function identity
Fact / Relation stage applicability documents
cross-stage ownership reconciliation
per-product closure
complete obligation projection
expected / assigned obligation identities
```

所以 current carrier 的结论是：

```text
INSUFFICIENT_FOR_CORRECTED_SUCCESSOR
```

后继必须使用新的、可区分的 private domain/request/qualification/admission version boundary。本文只证明这种边界必要且有限，
不选择具体 class、field、protocol suffix、serialization或 public Schema。

## 5. Provider algorithm 可复用，Fact truth不得投影

audit-only validated view在不删除任何 Fact、不改变 FactSet bytes/digest的前提下，把 application-owned applicable obligations分配给
现有两个 closed Relation Providers。实际 Provider algorithms按 path读取完整 `facts_by_id`，对被分配的 Import obligations工作，
不会要求 CLASS、FUNCTION、METHOD从 FactSet消失。

机械 witness：

| world | 完整 Facts | MODULE | IMPORT | profile non-applicable Facts | Provider A | Provider B |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| five-kind single path | 5 | 1 | 1 | 3 | 1/1 | 2/2 |
| five-kind two path | 10 | 2 | 2 | 6 | 2/2 | 4/4 |

两个 world均保持完整 FactSet。multi-path world对每个 accepted product/path分别存在恰好一个 MODULE，Import只绑定同 path MODULE；
不同 path不能交换 parent MODULE。

因此当前最窄裁决是：

```text
Relation Provider algorithms
    REUSABLE AFTER APPLICATION-OWNED ASSIGNMENT

FactSet truth projection / filtering
    FORBIDDEN

successor carrier and admission boundary
    REQUIRED
```

## 6. stage applicability 与 obligation completeness

successor先执行冻结的：

```text
r1-fact-handoff-relation-interoperability-correction/0.2
r1-fact-relation-stage-applicability/0.2
```

并对完整 sealed Policy形成 Fact / Relation total、disjoint、exactly-once ownership。`python-ast`与存在时的
`python-ast-advisory`归 Fact；`review-relation-derivation`归 Relation。另一 stage的 rows必须保留为完整 non-applicable side，
不能被删除、改名或冒充已履责。

随后对完整 authoritative FactSet执行：

```text
C_H(F) = r1-fact-relation-product-closure/0.1
O_R(F) = r1-fact-relation-obligation-projection/0.1
```

`O_R(F)`是 Relation responsibility，不是新的 Fact truth。application必须独立复算 expected obligation universe，并证明：

```text
expected == emitted
cardinality equal
no missing
no duplicate
no foreign-path member
each obligation assigned exactly as frozen Provider responsibility requires
```

只证明 emitted obligations可追溯，不足以证明 denominator完整。Provider output不能反向生成或缩小 `O_R(F)`。

## 7. bounded private successor A–J

若本候选最终取得资格，后继独立授权最多可以覆盖以下 A–J；本轮不实施：

### A. composition attempt ownership

由 application在一个 private attempt中绑定 exact `DerivationInputSet`、一个 claimed Fact handoff与 handoff的 original
`BudgetContext`。不创建第二个 Fact claim或新 BudgetContext。

### B. exact input / handoff revalidation

逐项复核 §3 坐标、safe branch、Fact terminal history、FactSet或qualified absence与 live object identity；任何 foreign world、
consumed claim或 digest-only input fail closed。

### C. stage applicability construction

构造 `/0.2` Fact / Relation applicability documents与完整 cross-stage ownership reconciliation；unknown、missing、duplicate、
overlap、gap与 requiredness drift均不得继续。

### D. per-product closure

对完整 FactSet建立 total Fact partition；每个 accepted product/path恰好一个 MODULE，Import只能引用同 path MODULE，所有
profile-non-applicable Facts仍保留原 identity。

### E. complete obligation projection

从完整 F、Policy、Relation Profile与 closure独立构造 `O_expected`，再生成 per-Provider responsibility；不得从 candidate或
Provider output反推 denominator。

### F. successor Relation work carrier

增加可区分的 private domain/request/terminal carrier，绑定完整 F、applicability、ownership、closure、expected/assigned
obligations、exact source blobs、request provenance与 same attempt。旧 `/0.1` domain和 request `/0.2` bytes保持不变。

### G. unchanged Provider execution

复用现有 closed Relation Provider algorithms，只让它们执行 application明确分配的 obligations；Provider不能自行声明 applicability、
修改 FactSet或取得未分配责任。

### H. qualification and admission

独立核对 expected/emitted双向相等、每个 assigned obligation恰好一个 terminal outcome、Provider requiredness、same attempt、
request provenance与完整 terminal history，再由 versioned successor admission产生 Relation authority。

### I. one-shot continuation

只有全部 required reconciliation完成后，才允许同一 composition attempt继续进入后继 Slice/composition seam。该 continuation
不取得manifest、persistence、public product、Evidence或publisher authority。

### J. direct falsifiers and byte guards

直接固化 `FRIC-000..018`、`FRIC-CID-001..012`、foreign-policy join、consumed claim、FactSet filter、global multi-MODULE、
cross-path parent、missing/duplicate/foreign obligation与legacy-byte guards；同时保留3.10/3.13 normal/`-O` canonical reports。

## 8. mechanical audit 与保留失败

read-only audit在 CPython 3.10.6 / 3.13.13、normal / `-O`四格运行。fresh attempt 2四份 semantic report digest一致：

```text
audit script SHA256
cd0fb1fd37d881b8e611b4bebf409a1c54ac0b46bdcd00c9aac299ed8a6021bd

four-cell semantic digest
27de95e632aaee5b6ef26ac332846184ac79b5011f319ce4d34152c53e003eaa

audit summary SHA256
26453cf80f963eef333339fb1c33679ee0fa9b85da2bf23a9251316c030dde7f
```

四格共同得到：

```text
FEASIBLE_WITH_BOUNDED_PRIVATE_SUCCESSOR
```

并共同确认 current carrier `INSUFFICIENT_FOR_CORRECTED_SUCCESSOR`、same-world join通过、foreign-policy join拒绝、五类/多路径
Provider witness成立以及bounded capability negative worlds fail closed。

attempt 1把nonce-bound `fact_consumer_attempt_id`写入semantic report，导致四格在语义相同时产生不同report digest，保留为：

```text
AUDIT_CANONICALIZATION_SETUP_ERROR
798c99d2e4e53f668d481341fe59eae9c694252656713ea011702503eb8b5ffe
```

fresh attempt 2只把它规范为机械核验后的`fact_consumer_attempt_identity_bound = true`，未修改产品runtime、frozen contract或
audit oracle。

第一次3.10 normal窄回归命令从tests目录解析相对PYTHONPATH时产生
`TEST_INVOCATION_PYTHONPATH_SETUP_ERROR`；tests因自己的source-path setup仍运行并PASS，但该identity不用于四格资格。
fresh attempt 2使用absolute PYTHONPATH；四格各：

```text
Ran 77 tests
OK (skipped=1)
```

即每格76 passed、1 skipped。测试只证明没有观察到既有窄路径回归，不授权successor implementation。

## 9. feasibility stop conditions

后继若出现以下任一条件，必须停下并只重开被击穿边界：

- 无法在消费前把 exact `DerivationInputSet`与 claimed handoff机械绑定到同一 world；
- 必须创建第二个 Fact claimant、新 BudgetContext或重跑 Fact才能进入 Relation；
- 必须过滤/重算 FactSet、改变完整 Policy或让 Provider定义 applicability；
- 现有 Relation Provider algorithms在合法 assignment下仍不能处理完整五类或多路径 world；
- successor carrier无法无损绑定stage ownership、per-product closure与完整 obligation denominator；
- qualification/admission必须依赖 Provider自证、caller bool、digest holder或跨 attempt result；
- 必须修改 legacy domain/request/history bytes，而不能增加可区分 successor；
- 必须先选择manifest、persistence、public Schema或Coverage语义才能闭合 private Relation successor；
- 必须重开Fact truth、Relation observation、doc290或doc294 frozen semantics。

## 10. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| stage applicability capability identity correction合同是否已 frozen | **是** |
| current one-shot Fact handoff是否可拥有整个composition attempt | **是** |
| handoff alone是否包含Relation所需source blobs | **否** |
| exact input与claimed handoff是否可机械join | **是** |
| current Relation domain/request carrier是否足够 | **否** |
| 现有Relation Provider algorithms是否可复用 | **是，限application-owned assignment之后** |
| bounded versioned private successor是否可行 | **是** |
| 是否需要过滤FactSet或重跑Fact | **否，且禁止** |
| manifest/persistence/Coverage是否为当前blocker | **否** |
| correction implementation是否已授权 | **否** |

本候选没有发现需要重开 frozen semantic contract 的反例。它把当前 blocker收紧为一个 bounded private successor carrier、
qualification与admission seam；未证明 runtime已经实现，也未证明旧 composition A–J可以恢复消费。

## 11. 不决定什么

本文不决定：

- successor Python class、field、protocol suffix、Schema或serialization；
- runtime code、tests、fixtures、vectors或Provider实现修改；
- RelationSet之后的Slice、ReviewSliceSet/Coverage composition或manifest successor；
- persistence Route A/B、cache、Bundle、publisher、CLI、Workbench或Core；
- public Review product、R2/R3、CLAIM_FIDELITY、post-R1 Benchmark、tag或Release；
- successor implementation authorization或freeze publication。

## 12. 本候选资格门与停止线

tracked scope只允许：

```text
README.md
AGENTS.md
docs/296-r1-fact-relation-corrected-successor-private-implementation-feasibility-audit.md
docs/milestones.md
```

doc290–295、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、Provider、vectors、corpus与post-R1计划
必须保持 `b293b263…` base bytes。final bytes至少完成四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、
marker、上游byte continuity、`git diff --check`、read-only hygiene、机械audit复核与声明的窄回归；测试只作witness。

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> FEASIBILITY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只能写：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

若本候选最终取得资格，它最多成为 qualified feasibility history。随后必须从新 exact main返回 CONTROL LOOP，单独判断
docs-only corrected successor implementation authorization publication是否仍是下一最小合法 seam；不得自动修改runtime、恢复旧
composition授权、选择manifest/persistence或启动Coverage、public Review、R2/R3。
