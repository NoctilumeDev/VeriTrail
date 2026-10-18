# R1 Fact handoff → Relation exact-input interoperability correction 最小合同 0.1

日期：2026-10-18

> 状态：`R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_CANDIDATE`。
>
> 基线：`main@2f57c71e6e3a9ecb3e2d2da050d331fff7bb004a`；tree
> `c4699e65a64a05b4de3f2a4a17d8eb276daf4a2f`。
>
> 上游：[Declared Relation Observation Domain 合同](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)、
> [ReviewSliceSet / Coverage composition 私有实现可行性审计](287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)、
> [composition 私有实现授权发布](288-r1-review-slice-set-coverage-composition-private-implementation-authorization-publication.md)与
> [Fact handoff → Relation exact-input interoperability 可行性修正审计](289-r1-fact-handoff-relation-exact-input-interoperability-feasibility-correction-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结同一 sealed Policy 的 stage-scoped applicability、完整
> authoritative FactSet 到 Relation obligation universe 的 total projection、逐 accepted product/path 的 MODULE closure、
> successor identity 与 same-attempt authority ceiling；不创建或修改 runtime、tests、Schema、fixtures、Profile、Policy、
> manifest、persistence、public carrier、Coverage composition、Evidence、Bundle、publisher、CLI、Workbench、Core、R2、R3、
> tag 或 Release。

## 1. CONTROL LOOP 与 qualified upstream

文档 289 已由 PR #332 final head `79027d49c515a249a049e49fd81d273f4f3b1cc5` 合入本基线。original Public CI
`39129451257`、exact-main Public CI `39131588569` 与 Browser Smoke `39131588645` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1。fresh README/doc289/milestones 各有 qualifying PASS；第一次 milestones formal observation 的
public render 503 / `PARTIAL` 保留原 `FORMAL_READBACK_ERROR` 身份，后继 fresh identity 才取得 PASS。independent
reconciliation attempt 1 的 derived marker metadata mismatch 作为 proof-facility failure 保留；attempt 2 只修对账设施，
不改产品、Plan、Evidence、oracle 或 doc289 bytes，并取得 PASS：

```text
7df17cfa65f5ee800c7df52c4c7de80016666198ba7b2726a6c781e43b14a015
```

176-artifact closeout 为：

```text
56bc8017443700422926336a59993f70b8aa6297df6b2dedcbf9e199cf79f8b8
```

因此文档 289 已成为 qualified history。composition implementation 的旧 `ALLOWED` 历史仍然成立，但施工前真实反例
已触发其停止线；没有 runtime diff，A–J 没有开始。重新核对 exact main、current Policy/Fact/Relation source、frozen
contracts 与保留反例，没有发现需要重开 Fact truth、Relation candidate semantics、Provider algorithm，或先选择 persistence /
public Schema 的更早 seam。当前最小合法问题是本 correction semantic contract。

## 2. 本合同解决的问题

现有两段 frozen truth 各自在自己的 closed world 中成立：

```text
complete same-attempt Fact handoff
    -> complete authoritative FactSet

closed Relation observation domain 0.1
    -> one MODULE + zero-or-more IMPORT_DECLARATION Facts
    -> two import relation families
```

但 current runtime 把“Relation stage 对哪些 Fact 产生 obligation”压成了“Relation stage 接受哪一种 FactSet shape”，并让
Fact stage 与 Relation stage 分别要求整份 sealed Policy 只包含自己的 capability。结果是：完整五类 FactSet、多 accepted
product FactSet 与同一 Policy 中的 Fact+Relation requirements 都没有共同可接受 world。

本合同冻结的修正不是过滤 FactSet、换 Policy 或放宽 global MODULE count，而是：

```text
P = complete sealed Policy
F = complete authoritative FactSet
H = complete same-attempt Fact handoff history
R = frozen Relation observation profile

A_s(P) = stage s 对完整 Policy 的 applicability partition
C_H(F) = 由 handoff history 约束的逐 accepted product/path closure
O_R(F) = Relation profile 从完整 FactSet 投影出的 obligation universe
```

核心不变量为：

```text
P 永远不被 A_s(P) 替代
F 永远不被 O_R(F) 替代

applicability projection
    = 这个 stage 拥有什么责任
    != 世界里只剩什么
    != 其他 stage 已经履责
```

本合同不假设任意两个 qualified states天然存在合法连线。给定 frozen world `W`、transition contract version `v`、候选机制
`C`与其证据 `π`，application只能机械裁决：

```text
Accept_v(A, C, B, π | W)
    = Verify_v(W, A, C, B, π)
```

它不负责保证 `C` 存在，也不把“端点 A 与 B 各自合法”当作转移证明。没有合格 `C/π` 时必须停止；不得为了到达 B 而
缩小 W、改写 A、预设 B 已成立或补造中间 authority。

## 3. authority owner 与禁止自证

| 主体 | 拥有 | 不拥有 |
| --- | --- | --- |
| sealed Policy | 完整 capability requirements、requiredness、composition mode 与 policy identity | 任一 stage 的履责结果 |
| frozen Fact handoff | complete Fact truth、FactSet、accepted products、U/E/blockers、Provider terminal history与same-attempt claim | Relation applicability、Relation obligation或Relation truth |
| Relation observation profile | relation family、eligible subject kind/role、cardinality、negative policy与Provider responsibility rules | Fact truth、Policy identity、live claim |
| application | stage applicability partition、per-product closure、obligation enumeration、assignment与机械对账 | 增删 Policy/Fact、补造 Provider outcome、选择 Relation truth |
| Relation Provider | assigned obligation 的 bounded observation、outcome与candidate | 自选 denominator、过滤 FactSet、改换 MODULE anchor、签发 admission |
| digest/content holder | 对应 semantic bytes | live attempt、one-shot claim、continuation或qualification authority |

Provider、caller、Schema、manifest、publisher 与 Coverage 都不能定义 `A_s(P)`、`C_H(F)` 或 `O_R(F)`。application 也只能
按照本文与 frozen profile 机械构造；不能根据 Provider 实际输出反向缩小 obligation universe。

## 4. normative function identities

本合同的规范 function identities 为：

```text
contract function
    r1-fact-handoff-relation-interoperability-correction/0.1

stage applicability
    r1-fact-relation-stage-applicability/0.1

per-product closure
    r1-fact-relation-product-closure/0.1

obligation projection
    r1-fact-relation-obligation-projection/0.1
```

这些 identities 冻结 semantic function，不预先决定 Python class、field、file 或 public Schema。current
`closed-python-import-observation / 0.1-test`、`veritrail.review.relation-observation-item/0.1`、
`veritrail.review.relation-observation-domain/0.1` 与既有 request/operands identities 均保持 immutable。后继 runtime 必须使用
可区分的 private successor identity；不得原位扩张、closest-version fallback 或让 legacy consumer静默接受 successor bytes。

若 feasibility 证明现有 private carrier 无法无损绑定本文语义，必须在新的最小 carrier/version seam 停止；本文不因此预选
public Schema 或 manifest successor。

## 5. same-policy stage applicability

application 必须对同一份 copy-owned sealed Policy `P` 构造 total partition：

```text
requirements(P)
    = applicable_requirements(stage)
    disjoint-union non_applicable_requirements(stage)
```

private exact value 必须 copy-own 完整 Policy 与 `policy_digest`。stage applicability 的 semantic projection 绑定 stage
identity、applicability function identity 与两侧完整 requirement identities；与当前 stage applicability 无关的 execution / governance
字段不进入这个 semantic digest，但始终留在 exact world 中。首个 bounded correction 至少要求：

```text
FACT stage
    owns review-fact-derivation requirement

RELATION stage
    owns review-relation-derivation requirement
```

每个 stage 只核自己拥有的 requirement；另一个 stage 的 requirement 在当前 stage 是 `NON_APPLICABLE_TO_STAGE`，不是
optional、fulfilled、deleted、unknown 或 globally out of scope。它继续留在完整 Policy 与 partition history 中。任一 stage 都
不能为另一 stage 签发 fulfillment，也不能用自己的 successful terminal 抵消另一 stage 的 requiredness。

只比较 applicable subset 不足以确定 semantic input；`NON_APPLICABLE_TO_STAGE` 一侧也是 total partition 的一部分。两份 Policy
若只在与当前 stage 无关的 execution / governance 字段上不同，可以得到相同 stage-applicability semantic projection；但完整
Policy bytes/digest 与 exact world 仍不同，不能继承 qualification、attempt、claim或live authority。

## 6. complete authoritative FactSet 不得被投影

Relation successor 的 exact operand 是 handoff 中的完整 authoritative FactSet `F`，并同时绑定完整 same-attempt Fact history
`H`。application 与 Provider 都不得：

- 删除 `CLASS / FUNCTION / METHOD` 或其他当前 Relation profile 不适用的 Fact；
- 构造只含 `MODULE + IMPORT_DECLARATION` 的替代 FactSet；
- 重新计算一个 filtered `fact_set_digest` 后把它称为原 handoff truth；
- 只传 `fact_set_digest`、path list 或 selected Fact IDs，再从环境恢复其余 bytes；
- 从另一个 attempt、另一个 Policy、另一个 accepted product history 或 legacy continuation 拼接 Fact bytes；
- 用 Relation profile 的表达能力反向定义 Fact universe。

`O_R(F)` 只是 `F` 上的 derived responsibility universe。它不能取得新的 FactSet identity，也不能作为 downstream
RelationSet、Coverage denominator 或 public truth carrier。

## 7. per accepted product/path MODULE closure

global `exactly one MODULE` 被替换为由 frozen handoff history 约束的逐 product closure：

```text
for each accepted product q in H:
    facts_q = all Facts in F whose qualified provenance belongs to q
    path_q  = exact path owned by q

    exactly one MODULE in facts_q
    every Fact in facts_q binds path_q
    every applicable subject in facts_q uses that same MODULE anchor
```

同时必须证明：

```text
accepted_products(H)
    = product identities represented by F

union(facts_q)
    = all Facts in F

facts_q sets are pairwise disjoint
```

path string不是 product identity。相同 path 的 foreign attempt/product、相同 Fact bytes、相同 FactSet digest holder或另一个
MODULE candidate都不能替换 qualified product provenance。两个不同 products 不能交换 MODULE；同一 product/path 有零个或多个
MODULE、Fact跨 path、foreign product Fact、dangling product、重复 product identity，任一都使 closure construction fail closed。

`MODULE` 在 current import profile 中是 structural anchor，不因此自动成为 relation obligation subject。未来 profile 若让
MODULE 成为 subject，必须通过新的 profile/function identity显式改变 obligation projection，不能复用 current projection。

## 8. total Fact partition 与 obligation projection

对 current frozen import profile，application 必须在执行任何 Relation Provider 前，将 `F` 的全部 members分成互斥且完备的：

```text
STRUCTURAL_ANCHOR
    current profile 所需的 per-product MODULE Facts

APPLICABLE_SUBJECT
    profile family rule命中的 IMPORT_DECLARATION Facts

PROFILE_NON_APPLICABLE
    F 中其余完整 Facts，例如当前 profile 下的 CLASS / FUNCTION / METHOD
```

三类并集必须等于完整 `F`，交集必须为空。`PROFILE_NON_APPLICABLE` 不是被删除的 Fact，也不是 Relation outcome；它保留 exact
Fact identity与“为什么当前 profile 不产生 obligation”的规则 provenance。

`O_R(F)` 对每个 applicable subject、每个 matching family机械生成一个 obligation。每个 obligation identity至少语义绑定：

```text
complete fact_set_digest
Relation profile identity/version/digest
per-product closure identity
accepted product identity and exact path
same-product MODULE fact identity
relation family/kind
subject role
subject Fact identity
obligation projection function identity
```

current profile 中每个 `IMPORT_DECLARATION` 产生：

```text
LEXICAL_CONTAINS / TARGET_FACT
IMPORT_TARGET_LITERAL / SOURCE_FACT
```

`CLASS / FUNCTION / METHOD` 不产生 current obligations，但继续存在于 `F` 与 total partition 中。未来 versioned profile 可增加
例如 `CALLS <- FUNCTION / METHOD`、`INHERITS <- CLASS`；这会改变 profile与 `O_R(F)` identity，不需要也不允许改写同一份
FactSet truth。

Provider responsibility继续由 frozen Relation profile定义。application 必须由完整 `O_R(F)` 导出每个 Provider assignment；
Provider/caller不能自选 subset。每个 obligation必须进入所有对应 responsibility，不能因另一个 Provider也负责同一 family而消失。

`O_R(F)` 的完整性本身是一项独立证明义务。application必须分别从完整 `F`、`P`、`R`、`C_H(F)` 机械重算
`O_expected`，并与准备交给 Relation stage 的 `O_emitted` 做双向、基数与唯一性核账：

```text
O_emitted - O_expected = empty    # 不得凭空新增
O_expected - O_emitted = empty    # 不得遗漏适用义务
count(identity in O_emitted) = 1  # 不得重复
```

仅证明“每个 emitted obligation 都能追溯到某个 Fact”不构成完整性。两个适用 Import 只投影其中一个，即使完整 FactSet、digest、
attempt 与已执行检查都真实，也必须 fail closed。每个完整 obligation还必须进入 frozen Provider responsibility并按文档175取得
合法 terminal observation；未执行、重复、foreign-attempt、缺失terminal或由输出反向消失的 obligation均不能取得successor
continuation。

## 9. known-empty、missing 与 unknown 不能合并

只有同时满足以下条件，current Relation obligation universe 才能是 known empty：

1. 同一 sealed Policy 的 Fact 与 Relation stage applicability均已合法取得；
2. complete same-attempt Fact handoff已被一次性领取且仍安全；
3. complete authoritative FactSet与全部 accepted product histories可用；
4. per-product closure完整；
5. total Fact partition完整；
6. frozen profile对所有 applicable Fact kinds的投影得到 `O_R(F) = []`。

此时必须保留“完整 F、当前 profile没有 applicable subject”的证明。它不等于 FactSet missing、Fact projection blocked、handoff
未 claim、accepted product history不完整、closure失败、foreign attempt、unknown profile或 filtered empty FactSet。

文档 175 的 empty execution semantics继续原样成立：whole declared domain known empty时，两个 required Relation sources仍分别
真实启动、terminal `COMPLETED`、报告 empty outcomes/candidates并 residue-free release，才能取得各自 complete-empty receipt。
本合同不把 `O_R(F)=[]` 偷换成“无需执行”、空 RelationSet、Coverage complete或“源码中不存在 Relation”。

## 10. same-attempt claim 与 continuation ceiling

successor construction必须消费 original Fact handoff的同一 live `BudgetContext`、attempt、deadline与stop/revocation state。顺序至少为：

```text
revalidate exact immutable inputs
    -> one-shot claim complete Fact handoff
    -> validate same sealed Policy and stage partitions
    -> construct per-product closure
    -> construct total Fact partition and O_R(F)
    -> construct versioned Relation domain / exact Provider assignments
    -> execute frozen Relation observation semantics
```

semantic bytes、Policy/FactSet/projection digest、equal limits或相同 Relation outputs都不能恢复已消费、失败、revoked或foreign
attempt 的 live claim。attempt-neutral summary/cache未来可以复用 semantic content，但不能复用 claim、ProviderRun、receipt、
admission、continuation或BudgetContext identity。

“当前尝试过的所有候选 C 都失败”只能得到 `UNKNOWN / NO_QUALIFIED_CONSTRUCTION`。只有对本文明确限定的完整候选空间给出
机械不可满足性证明，才可以声明该 versioned contract 下 `UNSAT / NO_CONSTRUCTION_EXISTS`。有限测试、多个反例、经验穷举或
没有想到新结构，都不能把 UNKNOWN 升格为不存在。

本合同最多恢复 doc287 stage C 的 implementation feasibility。它不签发 RelationSet admission、Slice closure、
ReviewSliceSet/Coverage composition continuation、persistence或public publication authority。

## 11. normative falsifier obligations

后继 feasibility / implementation至少必须直接攻击以下 worlds；本轮 audit-only model只证明合同区分可行，不冒充 runtime已实现：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `FRIC-000` | 完整五类 F；current profile只匹配 import | 过滤 F 后仍继承原 FactSet identity |
| `FRIC-001` | same stage-owned requirement；完整 Policy 多一个 unrelated row | applicable subset相同即可继承 Policy authority |
| `FRIC-002` | Fact-only Policy缺 Relation requirement | Fact stage成功自动授权 Relation stage |
| `FRIC-003` | 一个 accepted product/path有两个 MODULE | 任取其一仍形成合法 closure |
| `FRIC-004` | Fact provenance属于 product A，但 path或MODULE来自 B | path/content equality允许跨 product anchor |
| `FRIC-005` | 两个 accepted products各有 MODULE+IMPORT | global one-MODULE rule拒绝或跨 path交换parent |
| `FRIC-006` | 完整 F含 MODULE/CLASS/FUNCTION/METHOD、无 import | known-empty等于 Fact missing或无需 required execution |
| `FRIC-007` | Fact handoff/closure不完整，当前输出为空 | empty output允许构造known-empty domain |
| `FRIC-008` | Provider只领取自己实际会产出candidate的 subset | Provider output反向定义obligation universe |
| `FRIC-009` | 两个 Provider各覆盖一半 responsibility | union output冒充逐 Provider closure |
| `FRIC-010` | same semantic P/F/projection，fresh equal-limits attempt | semantic equality继承one-shot claim |
| `FRIC-011` | current F不变，profile增加 CALLS/INHERITS | 旧 `O_R(F)` identity继续适用 |
| `FRIC-012` | legacy 0.1 domain/request收到successor bytes | closest-version fallback或静默扩张 |
| `FRIC-013` | non-applicable Facts未出现在投影输出 | 不适用等于可以从 authoritative history删除 |
| `FRIC-014` | obligation绑定正确subject但错误same-path MODULE | FactSet digest alone足以证明parent closure |
| `FRIC-015` |已消费/失败的handoff只有digest holder|内容持有者恢复live authority|
| `FRIC-016` | 两个适用Import只投影其中一个 | emitted obligations可自行缩小完整denominator |
| `FRIC-017` | 同一适用subject/family被投影两次 | duplicate obligation仍可取得complete reconciliation |
| `FRIC-018` | 所有已测试candidate structures均失败 | 未穷尽候选空间即可宣称合同数学无解 |

任何 implementation若只能通过换 Policy、过滤 FactSet、修改 frozen 0.1 identity、放宽为“one or more MODULE”、让 Provider
自证 subset、拼接 foreign attempt或弱化 empty execution semantics 才通过，必须停止并返回被击穿的最小合同边界。

## 12. audit-only mechanical witness

本合同起草前在基线外构造了 pure semantic audit model。它不改 runtime/tests，也不作为产品 implementation证据。首个
attempt把排序后最后一个 requirement误当作 unrelated capability，实际删除 Relation requirement，留下
`AUDIT_FIXTURE_SETUP_ERROR`；没有产品语义到达，也没有覆盖。

fresh attempt 2 证明了核心 projection worlds，但合同复读发现它把完整 `policy_digest` 过度绑定进 stage semantic digest；该
attempt作为中间witness保留，不作为最终合同语义。fresh attempt 3 只修audit model的semantic/exact binding，不改产品oracle；
随后“两个适用Import只emitted一个obligation”的反例证明单向provenance仍不足以证明完整。fresh attempt 4增加expected/emitted
双向、基数与唯一性核账，并在CPython 3.10.6 / 3.13.13、normal / `-O`四格逐字节一致：

```text
semantic report digest
02f33ff455057ad1010ac392fdc1132b1e33fc9cf6b8e5bc65bc89f273cd7c07

report file SHA256
22d1d9016217bc28b145173f570767c9076c61dd43dc1c80ff40a184f97c1f61
```

attempt 3完成后，摘要展示命令把单个hash字符串当作scalar，并把索引零解释为`System.Char`后调用`ToLower()`，保留为
`OPERATOR_REPORTING_ERROR`；四份完整report均已终态，不受该展示错误影响。

候选validator第一次用`attempt3-*.json`选择report时同时匹配了该summary-error JSON，保留为
`VALIDATION_REPORT_SELECTION_SETUP_ERROR / product_observation=false`；后继只把选择式收窄为明确的Python grid文件，不改
合同、audit worlds或产品oracle。

四个 positive worlds分别证明：

```text
five-kind single product: 5 Facts -> 2 current obligations
two products:             4 Facts -> 4 current obligations
known-empty no import:    4 Facts -> 0 obligations + required empty execution
future profile:           same FactSet -> 5 obligations under distinct profile
```

negative worlds直接拒绝 filtered FactSet inheritance、缺 Relation requirement、same-product duplicate MODULE、cross-path Fact、
foreign-product Fact、遗漏适用obligation与重复obligation。另证明 unrelated Policy requirement变化不改变stage-owned rows、但改变完整two-sided partition identity；
只改变execution/governance字段可以保持stage semantic projection不变，但exact Policy world仍不同。fresh attempt可以有相同
semantic FactSet digest，却不能继承 claim。

## 13. 本合同不决定什么

本文明确不决定：

- successor Python class、field、serialization、public Schema或manifest file；
- Relation Provider algorithm扩张、完整 Python relation families或module resolution；
- existing Provider是否需要代码变化；
- RelationSet admission、Slice traversal、ReviewSliceSet/Coverage composition A–J；
- Coverage denominator、terminal partition、overall join或public product；
- persistence Route A/B、cache format、offline verification或Bundle topology；
- public Provider SPI、R2 Evidence、R3 Attention、人类 disposition或Core Verdict；
- composition implementation authority是否恢复。

## 14. 当前裁决与后继停止线

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED

R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED

R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选自己的最终 tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc175、doc287、
doc288、doc289、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors与corpus必须保持base bytes。

final bytes至少完成：四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、status markers、上游byte continuity、
`git diff --check`、read-only hygiene、声明的Markdown/baseline regression与四格audit report复核。测试只作witness。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate
    -> separate docs-only freeze publication
    -> freeze publication's own original PR / merge / exact-main / readback / reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

全部门闭合以前，本合同不是 frozen fact。即使最终 frozen，也不自动授权 successor runtime、恢复composition A–J、选择
manifest/persistence或启动public Review产品。后继若仍需要 implementation，必须重新证明本合同在current private primitives上
可行，并取得独立、明确的实施授权。
