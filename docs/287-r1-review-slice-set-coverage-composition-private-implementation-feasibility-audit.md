# R1 ReviewSliceSet / Coverage composition 私有实现可行性审计

日期：2026-10-18

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 坐标：`main@ac41b5c852a7f79607fa3bcc771ea0b7858abeb9`，tree
> `ea50038d80a8cac89fa62e052e754942d15c616e`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [root binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)与
> [CoverageLedger 0.3 私有实现冻结发布](286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本轮只审 private composition implementation 是否可由现有
> frozen upstream 与 bounded versioned successor 实现；不修改 runtime、tests、Schema、manifest、fixtures、
> vectors 或 corpus，不选择 persistence，也不启动 public Review 产品。

## 1. CONTROL LOOP 与 exact source state

PR #328 final head `f29d170987ffd693d0575c91d0853ad0252038ed` 已合入当前主线。original Public CI
`39108536749`、exact-main Public CI `39110162970` 与 Browser Smoke `39110162978` 均为 attempt 1
SUCCESS，分别为 11/11、11/11 与 1/1。fresh README/doc285/doc286/milestones 为 4/4 qualifying PASS。
independent reconciliation 与 165-artifact closeout 分别为：

```text
26bc4b18172a0317d5f82d011b56bb0767f1fb35a1b65b24767483740e40b8e3
1c5215761e4524435d0d4cf48fce817d66406b042f977d97275eeae4974b91ba
```

reconciliation attempt 1 只因 Windows Git long-path checkout 失败而保留；fresh attempt 2 使用 process-local
`core.longpaths` 后 PASS。它没有修改产品、全局 Git 配置或冻结 oracle。因此以下事实已经生效：

```text
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

fresh CONTROL LOOP 重新核对远端、open PR、冻结合同、current private runtime、CoverageLedger 0.3
Schema/conformance、manifest 0.1 与 compatibility corpus。远端仍为该 exact main，open PR 只有旧
Dependabot；没有新的 semantic source state，也没有反例要求重开 Fact、Relation、ReviewSlice、composition
qualification、root-binding 或 CoverageLedger 0.3 合同。

## 2. 当前桥头：Fact handoff 已冻结

`_fact_to_coverage_handoff.py` 已实现 one-shot、copy-owned 的 `ClaimedFactToCoverageHandoff`，consumer identity 为：

```text
veritrail-review-private-coverage-composition/0.1
```

它只暴露 source document copy 与原始 `BudgetContext` reference。`_fact_fulfillment.py` 对 source document 做
exact input、classification、Fact qualification 与对象身份复核，并保留：

```text
branch
input identity
parse partition
Fact U / E / blockers
Provider history
FactSet or qualified absence
whole-attempt history
```

因此 current upstream 已经提供 composition contract 所需的 authoritative Fact history；相同 source bytes、
FactSet digest 或 semantic result 仍不能复用 claim、attempt 或 continuation authority。

## 3. 旧高层 Relation / Slice 入口不能原样复用

current high-level Relation qualifier仍从 `DerivationInputSet` 调用 `admit_derivation_budget(inputs)` 创建新
`BudgetContext`，随后执行自己的 Fact child attempts 并重新组合 FactSet。若把它直接放在 claimed handoff 之后，会同时发生：

```text
new attempt context
+
Fact execution replay
```

这违反 frozen same-attempt 与 no-Fact-rerun 边界。

current RelationSet admission也绑定 legacy `fact_phase_results`、closed-test Fact bindings 与 source-operation
history；它不能把 handoff-sourced qualification 当作旧 qualification 接受。current Slice entry继续要求
`OwnedRelationQualificationContinuation` 与对应 legacy admission/context。因此：

> 可复用 frozen semantic primitives；不能冒充旧高层 authority path 与新 handoff path 是同一个路径。

后继实现必须增加 bounded versioned successor，旧路径及其 bytes保持不变。

## 4. 有限可复用面

仓库已有的低层 primitive 足以形成有限 successor：

1. `build_declared_relation_observation_domain(inputs, fact_set_document, relation_bindings)` 接受 exact inputs 与
   handoff FactSet；
2. `build_prepared_relation_observation_attempt(...)` 接受显式原始 context、eligibility、FactSet 与 observation
   domain，不要求自己重跑 Fact；
3. Slice normal / partial、closed-empty 与 blocked-input closure 已有 one-shot、same-context private carrier；
4. CoverageLedger 0.3 conformance 能复算 fixed seven-stage vector、three-root chain、terminal histories、overall join 与
   Ledger digest；
5. 八个 frozen compatibility worlds已覆盖 normal、branch-empty、slice-partial、zero-Parse-denominator、all-rejected、
   projection-blocked、required-Provider-non-success 与 qualified-unknown。

这些 primitive只证明有限实现路径存在。仓库当前仍没有 production ReviewSliceSet projection/admission 或
ReviewSliceSet/Coverage composition assembler。

## 5. Coverage conformance 的 authority ceiling

`_review_coverage_ledger_conformance.py` 明确是 validation-only。caller向它传入 stage/root projections 与
`authority_safe`；validator只能拒绝不合格 candidate，不能因为 caller写了 `authority_safe=True` 就生成：

```text
denominator authority
root truth
terminal-history completeness
same-attempt composition claim
ReviewSliceSet admission
```

因此 future application-owned composition 必须先从 exact upstream history构造 source，再让 conformance单向核验。
conformance不能修补、重分类或扩大 source，也不能拥有考试范围。

## 6. manifest successor 仍是独立 seam

manifest 0.1 的 `COMPLETE` 精确要求八个文件，包含 FactSet、RelationSet、ReviewSliceSet 与 CoverageLedger；
`DIAGNOSTIC` 又只允许四个输入文件且禁止 Ledger。negative worlds的 public publication topology仍未解决。

但 composition contract当前只要求 private same-attempt closure。因此：

```text
manifest negative-world publication gap
    != private composition feasibility blocker
```

本轮不选择 manifest version、role、path、files cardinality 或 migration，也不把 private candidate冒充可发布 Bundle。

## 7. mechanical audit

read-only audit从 exact source、AST、Schema 与 fixtures复算当前拓扑，并在 CPython 3.10.6 / 3.13.13、normal / `-O`
四格运行。attempt 4 四份 canonical report逐字节一致：

```text
14210f1ce528b09f7ab9c5808105637287c1c082175f79a1c1c7b6fb6d03fed3
```

它确认：

- one-shot handoff、原始 context 与完整 Fact terminal history仍存在；
- legacy Relation high-level path仍创建新 context并运行 Fact attempts；
- low-level Relation domain/cell可以消费 handoff FactSet与原始 context；
- legacy Relation admission 与 Slice entry仍绑定旧 qualification/continuation；
- normal / empty / blocked Slice closure carriers存在；
- production composition assembler与ReviewSliceSet projection/admission不存在；
- CoverageLedger 0.3仍是七阶段、三 root binding、八个 distinct compatibility worlds；
- conformance仍为 caller-supplied-source validation；
- manifest 0.1 COMPLETE/DIAGNOSTIC topology gap仍独立存在。

前三次四格 attempt均为审计器 setup failure并永久保留：

1. attempt 1 把 `relation_bindings` 参数名臆测成 `bindings`；
2. attempt 2 错把 `_merge_and_validate_facts` 当作 public admission entry 的直接调用，而实际调用位于
   `_validate_qualification`；
3. attempt 3 用过宽 filename predicate把上游 `_multi_provider_fact_composition.py` 误判成 Coverage composition。

三次都没有修改或执行产品 runtime，也没有资格成为产品反例。fresh attempt 4只修 audit harness，与 frozen oracle、
expected topology和产品字节无关。

作为独立baseline witness，既有R1 Schema payload与CoverageLedger 0.3 conformance tests也在同一四格各
`46/46 PASS`；这些测试不授予composition authority。

## 8. bounded successor A–J

若本可行性候选最终取得资格，后继授权最多可以覆盖以下 bounded A–J；本轮不实施：

### A. composition attempt ownership

application创建一个 private composition attempt，绑定 exact `DerivationInputSet`、一个 claimed Fact handoff与其原始
`BudgetContext`。相同 bytes、digest、limits 或语义结果不能继承该 attempt。

### B. handoff source revalidation

在消费前复核 exact source、safe branch、Fact terminal history、Provider responsibility、FactSet或qualified absence与原始
context object；不得从序列化文档或digest-only输入重新取得live authority。

### C. post-handoff Relation qualification

增加versioned private successor：从 handoff FactSet、sealed Relation domain与现有low-level workers在原始context中形成
Relation qualification；不得创建新Fact attempts或回退到legacy high-level入口。

### D. successor RelationSet admission

增加versioned admission，绑定新qualification、Provider responsibility、same attempt、request provenance与完整终态；旧
admission path及bytes保持不变。

### E. same-attempt Slice successor

以exact successor admission、inputs与context进入Slice，复用现有obligation、traversal、reconciliation与normal/partial/
closed-empty/blocked closure primitive；不得凭RelationSet digest恢复continuation。

### F. ReviewSliceSet projection and admission

从exact Slice closure构造private ReviewSliceSet projection，再由独立application admission核对normal、partial、
closed-empty、blocked与unknown world。内容identity与admission authority保持分离。

### G. seven-stage history construction

从authoritative upstream history构造七段 `S/A/N/D` 与六个transition proofs；不得缩小denominator、让已消失成员重新出现，
或用可表示集合冒充obligation universe。

### H. total terminal qualification

形成total stage qualification、conservative overall join、ordered root binding与0.3 candidate；最后才调用validation-only
conformance。Coverage只能解释自己的stage status，不能改写上游失败身份。

### I. one-shot closure

全部required reconciliation完成后才产生one-shot private composition closure/continuation；它不取得persistence、manifest、
public product、Evidence或publisher authority。

### J. direct falsifiers and byte guards

直接固化 `RSCQC-000..017`、`RBCC-000..011`、legacy byte guards与3.10/3.13 normal/`-O` canonical reports；重点拒绝
foreign attempt、Fact rerun、digest-only authority、partial Provider merge冒充complete、unknown promotion、denominator
shrink/reappearance与caller bool自授权。

## 9. feasibility stop conditions

后继若出现以下任一条件，必须停下并只重开被击穿边界：

- low-level Relation domain/cell无法消费handoff FactSet与原始context；
- 必须修改legacy Relation/Slice types或history bytes，而不能增加versioned bounded successor；
- ReviewSliceSet admission无法绑定exact Slice closure与same-attempt history；
- private negative worlds必须先取得manifest successor或persistence才能闭合；
- 必须信任caller bool、serialized source或digest holder生成authority；
- Coverage需要重新定义上游denominator、failure identity或terminal history；
- 必须重开Fact、Relation、ReviewSlice、composition qualification、root-binding或0.3 Schema/conformance frozen semantics。

## 10. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| CoverageLedger 0.3 child implementation是否已经 frozen | **是** |
| Fact handoff是否提供composition所需upstream history | **是** |
| legacy high-level Relation/Slice path能否原样复用 | **否** |
| bounded versioned successor是否可行 | **是** |
| 是否需要重开frozen合同或Schema | **否** |
| manifest successor是否阻塞private composition | **否** |
| persistence是否成为当前blocker | **否** |
| composition implementation是否已授权 | **否** |
| public Review product是否已开始 | **否** |

本轮没有发现需要重开 frozen contract 的反例。若本候选完成自己的资格链，它最多成为
`FEASIBILITY_AUDITED` history；随后必须返回 CONTROL LOOP，单独判断 docs-only implementation authorization
publication 是否仍是下一最小合法 seam。

## 11. 本候选资格门与停止线

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc259–286、runtime、tests、
workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产必须保持base bytes。

final bytes至少完成：四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、状态marker、上游frozen-byte
continuity、`git diff --check`、read-only hygiene与声明的Markdown/Schema baseline regression。机械audit与四格报告必须在
提交前复核；测试只作witness。

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
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本文不授权 implementation publication、composition runtime/tests/fixtures/vectors、manifest successor、persistence、
public `ReviewSliceSet` / `CoverageLedger`、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag
或 Release。
