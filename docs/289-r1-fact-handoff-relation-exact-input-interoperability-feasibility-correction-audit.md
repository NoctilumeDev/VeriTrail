# R1 Fact handoff → Relation exact-input interoperability 可行性修正审计

日期：2026-10-18

> 状态：`R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDIT_CANDIDATE`。
>
> 坐标：`main@3e491558d511f2578a5364d25822d235e91e8a14`，tree
> `4086fa5ec89d178fd6de594009da9a0e9cfdfeca`。
>
> 上游：[Relation observation qualification 合同](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)、
> [composition feasibility audit](287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)与
> [composition implementation authorization publication](288-r1-review-slice-set-coverage-composition-private-implementation-authorization-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本轮只审同一个 sealed Policy 下的 stage-scoped capability
> projection、完整 authoritative FactSet 到 Relation-applicable obligations 的投影、首版 single-module closed
> shape 边界，以及能否用 bounded versioned successor修复。它不修改 runtime、tests、Schema、Fact/Relation
> frozen bytes，不选择 persistence，也不启动 Coverage composition。

## 1. CONTROL LOOP 与 retained authority history

文档 287 已在自己的 exact-main world 完成资格链。文档 288 的 tracked bytes仍保留条件目标措辞，但其后独立
publication closeout已完成 4/4 fresh installed-product readback、independent reconciliation与 156-artifact closeout：

```text
independent reconciliation
ea069bfc0995a90c40e26cbb282f2420aaa3c8df72d91d094003e1e1931e96c1

closeout
892ea5494a0b9ab6785f42e16341b411d26cbc4c6aaed2878a8a303813c6d508
```

因此以下历史已经成立：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
```

历史 `ALLOWED` 不因后来的反例被删除；但授权不能越过文档 287 §9 / 文档 288 §5 的停止线继续消费。
fresh CONTROL LOOP 重新绑定当前 exact main、remote main、open PR、上游 frozen bytes 与当前 runtime。远端仍为
`3e491558…`，open PR只有旧 Dependabot，没有另一份 semantic source state。

## 2. 真反例：被授权施工面的前提不成立

文档 287 曾把以下命题作为可行性前提：

> low-level Relation domain/cell可以消费handoff FactSet与原始context。

施工在产生产品 diff 前建立 read-only counterexample，发现 current exact path没有一个共同输入世界能够同时满足：

```text
Fact handoff applicability
+
Relation observation applicability
+
exact handoff FactSet identity
```

三组反例为：

| world | frozen Fact result | current Relation / Fact boundary |
| --- | --- | --- |
| 完整五类 Fact handoff | `NORMAL_FULFILLED`，14 Facts，五个 Fact kinds | current Relation domain `REJECTED` |
| MODULE + IMPORT handoff，Fact-only Policy | 合法 FactSet | current Relation domain `REJECTED`，因为 Policy 没有 Relation requirement |
| 同一 Policy 同时声明 Fact + Relation capability | Relation applicability可表达 | current Product Fact consumer `REJECTED`，因为 Fact applicability只允许 Fact requirements |

第一轮四格在 CPython 3.10.6 / 3.13.13、normal / `-O` 全部退出 0，semantic report一致：

```text
c01f2c7b46fda251272abea8fad86d76a52ff731b593d4cb55f9bb1cb617bd50
```

封存 summary SHA-256：

```text
58994a05300fea3086ff11b437fbce419b46aa0c8cfc663e53b261067b5e17a3
```

这触发文档 287 §9 第一条停止条件。composition implementation保持 `NOT_STARTED`；runtime、tests、Schema均没有
修改。本轮不是用新审计否认旧资格链，而是保留旧 authorization history，同时停止消费已被反例击穿的施工前提。

## 3. capability intersection 为何为空

current Fact applicability在 `_multi_provider_applicability.py` 中把 Policy requirements严格限制为：

```text
{python-ast}
或
{python-ast, python-ast-advisory}
```

current Relation request/domain则要求同一个 Policy包含 required `review-relation-derivation`。legacy high-level Relation
qualifier确实接受组合 Policy，但它会创建新的 `BudgetContext`、重新运行 Fact children并重新组合 FactSet，不能继承
one-shot handoff authority。

因此不能用以下任一做法修复：

- 把 Fact-only Policy在 Relation 阶段静默改成另一份 Policy；
- 用新的 Policy digest接到旧 handoff；
- 调用 legacy high-level qualifier重跑 Fact；
- 让某个 stage把不属于自己的 capability当作已履责；
- 让 caller用 bool 声明“requirements 已满足”。

需要审查的是**同一 sealed Policy、同一 policy digest下的 stage-scoped applicability**：每一 stage只核验自己拥有的
capability requirements，同时保存完整 Policy identity与其他 required stages，不得删掉、重写或代替其他 stage履责。

## 4. full FactSet 与 Relation-applicable obligations 不是同一个集合

文档 175 的首个 closed proof明确只接受：

```text
one supported ordinary Python blob
exactly one MODULE
zero or more single-name ast.Import Facts
no CLASS / FUNCTION / METHOD
```

current `_relation_observation_domain.py`也机械执行这一限制：FactSet必须只有一个 MODULE与若干 IMPORT；任何其他
Fact kind或第二个 MODULE都会在 Provider启动前被拒绝。这个行为对 `/0.1` closed proof是正确的。

但 current Relation observation profile的两条 family rule都只把 `IMPORT_DECLARATION`列为 applicable subject kind：

```text
LEXICAL_CONTAINS       <- IMPORT_DECLARATION
IMPORT_TARGET_LITERAL  <- IMPORT_DECLARATION
```

因此 future interoperability不能把：

```text
complete authoritative FactSet
```

误解成：

```text
every Fact is a Relation obligation
```

正确边界是：完整 FactSet及其 digest继续作为 exact operand；application从 frozen Relation profile对完整 FactSet机械投影
applicable obligation universe。CLASS / FUNCTION / METHOD没有被删除，也没有被重分类；它们只是不属于当前 Relation
profile的 subject domain。

## 5. 过滤 FactSet 不是 interoperability

审计直接构造一个五类、5-Fact world，再把它过滤成 MODULE + IMPORT。结果为：

```text
original FactSet digest
47b4287d16b4ed60420efc6613854b3c165820383dd1af4d75c03cce358cbf62

filtered FactSet digest
b4b8471f2a1c026ae51e74530b42b9465b3328949c9dffe8431fc78c2f5ab970
```

二者不相等。过滤后保留原 digest会被 request builder以 `FactSet digest mismatch`拒绝；重新计算 digest则得到另一份
FactSet identity。因此：

> 从 authoritative FactSet抽出较小 MODULE + IMPORT FactSet，只能创建另一份内容身份，不能证明 exact-input
> interoperability，也不能继承原 handoff authority。

允许的是 obligation projection，不是 Fact truth projection。

## 6. multi-module closed-shape boundary

第二轮审计增加两个 accepted source products：

```text
pkg/a.py -> MODULE + IMPORT
pkg/b.py -> MODULE + IMPORT
```

Fact handoff得到 4 Facts、2 MODULE、2 IMPORT、2 paths；current Relation domain仍因 `exactly one MODULE`拒绝。这个反例
说明首版限制不仅是“额外 Fact kinds”，还包含全局 single-module cardinality。

future bounded successor至少必须证明：

```text
每个 accepted source product / exact path 恰好一个 MODULE
每个 applicable IMPORT只归属于同 path MODULE
不同 path不能共享或互换 MODULE parent
完整 FactSet与所有 path identity保持不变
```

它不能简单把全局 `one MODULE` 改成 `one or more MODULE` 后停止核账。

## 7. bounded versioned successor 的可行性

第二轮 read-only audit没有修改产品 validator，而是在 audit-only validated view后直接调用现有 closed Provider，用来区分
“Provider算法不能处理”与“现有 admission不能表达”。四格 canonical semantic report一致：

```text
51c17d6fce90fde5cee9152250ff59eb025eb4f236604db14699ab2e730c726f
```

audit script SHA-256：

```text
4587fc30b8f43e50f237af364cab2a90b0d91a9dbd2a4cb7a1c47589e5404765
```

两轮历史、四格文件与裁决汇总 SHA-256：

```text
5e1a2f485fef15c5bc29fe9de5b1959fb16cb20186010ac6865039db82826ff9
```

结果为：

| world | current domain | audit-only applicable obligations | Provider A | Provider B |
| --- | --- | ---: | --- | --- |
| 完整五类、单 path | REJECTED | 2 | 1/1 candidate/outcome | 2/2 candidates/outcomes |
| MODULE + IMPORT、双 path | REJECTED | 4 | 2/2 candidates/outcomes | 4/4 candidates/outcomes |

两组调用都保留完整 FactSet、原 `fact_set_digest`与全部 `facts_by_id`；只把 profile-applicable item IDs分配给 Provider。
current Provider已按每个 subject path取得 source blob，并按同 path选择唯一 MODULE parent。因此底层 parser/provider机制不是
这次 blocker。

审计据此得到有限结论：

1. 同一 sealed Policy可以由versioned application-owned applicability按 stage投影，但 full Policy bytes/digest必须继续绑定；
2. 完整 FactSet可以原样进入 Relation successor，obligation universe由 frozen Relation profile对其投影；
3. single-module限制可以由versioned domain/request/application successor替换为per-product/per-path闭包；
4. old `/0.1` domain、request、qualification、Fact truth、Relation candidate identity与Provider output semantics无需修改；
5. legacy high-level Relation path仍不可复用，因为它会重取attempt authority并重跑Fact。

这只证明修正路径有限且可反证，不等于该 successor合同或runtime已经存在。

## 8. 后继最小合同面

若本候选完成自己的资格链，下一次 CONTROL LOOP 最多可以审一份 docs-only correction contract。合同问题应限定为：

### A. same-policy stage applicability

同一个 sealed Policy与policy digest怎样让 Fact stage和Relation stage分别核验自己的 capability，而不删除其他 required
capability、不替其他 stage声明履责，也不改变Provider membership owner。

### B. exact Fact operand

successor必须绑定完整 handoff FactSet与原 digest。任何 filtered、reconstructed或digest-only Fact holder都不能取得同一
authority。

### C. applicable obligation projection

Relation profile拥有 family applicability；application机械枚举 applicable items并保留non-applicable Facts。Provider只执行
assigned items，不能定义Fact universe或自己缩小denominator。

### D. per-product module closure

从authoritative Fact history证明每个 accepted product/path的MODULE cardinality、IMPORT归属与source blob binding；不能把两个
路径、两个attempt或两个FactSet拼成一个合格world。

### E. version and authority ceiling

任何新identity必须是独立、versioned、bounded successor。它最多恢复doc287 C所需的post-handoff Relation qualification
feasibility；不能自动恢复composition implementation authority，更不能启动RelationSet/Slice/ReviewSliceSet/Coverage、
persistence、manifest或public product。

## 9. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| doc287 / doc288 的历史资格是否保留 | **是** |
| doc287“current low-level domain可消费handoff FactSet”是否仍成立 | **否，表述过宽** |
| current domain是否接受完整五类 FactSet | **否** |
| current domain是否接受多 MODULE exact FactSet | **否** |
| 过滤为MODULE + IMPORT是否可以保留handoff identity | **否** |
| current Provider能否处理完整Fact map上的applicable import obligations | **有限审计中是** |
| stage-scoped same-policy + full-FactSet obligation projection是否有bounded successor路径 | **是，候选可行** |
| 是否需要改写frozen Fact truth或Relation candidate semantics | **否** |
| composition implementation是否已经开始 | **否** |
| 既有ALLOWED是否可继续直接消费 | **否；stop condition已触发** |
| runtime / tests / Schema / persistence / Coverage是否获授权 | **否** |

当前状态为：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

## 10. 本候选资格门与停止线

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc175、doc287、doc288、runtime、
tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors与corpus必须保持base bytes。

final bytes至少完成：四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、marker、上游byte continuity、
`git diff --check`、read-only hygiene、声明的Markdown/baseline regression，以及两轮反例证据与第二轮四格报告复核。
测试只作witness。

本地窄基线的首次组合调用从plugin tests目录启动，前三个模块完成`115/115 PASS`，但把位于仓库根`tests/`的
`test_review_coverage_ledger_0_3`当作同目录模块导入，留下`TEST_INVOCATION_SETUP_ERROR`。它没有产品语义含义，也不被
覆盖。后继只从正确仓库根入口执行未运行的模块并取得`24/24 PASS`；已经完成的115项没有为了洗绿而重复执行。

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CORRECTION_FEASIBILITY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合前，本候选不能授权correction contract、successor runtime或composition implementation。即使闭合，下一步也只
能重新判断docs-only correction contract是否仍是最小合法问题；不得按文档编号自动施工。
