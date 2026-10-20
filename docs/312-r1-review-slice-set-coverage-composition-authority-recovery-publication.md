# R1 ReviewSliceSet / Coverage composition authority recovery publication

日期：2026-10-21

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@35e99a872d33234c4fb923a64995ccb148d9e3ba`，tree
> `b2c8e9dfd0cf2adb3e87ffbf8b1b01c9b044f155`。
>
> 上游：[composition qualification 合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [private implementation feasibility](287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)、
> [旧 implementation authorization](288-r1-review-slice-set-coverage-composition-private-implementation-authorization-publication.md)、
> [Fact → Relation transition freeze](310-r1-fact-handoff-relation-corrected-successor-private-transition-implementation-freeze-publication.md)
> 与 [authority recovery current-state audit](311-r1-review-slice-set-coverage-composition-authority-recovery-current-state-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_RECOVERY_PUBLICATION_ONLY`。本文只条件化恢复一个 bounded、private、versioned、
> application-owned Relation transition → Slice authority bridge implementation authority；不修改 runtime、tests、workflows、
> Schema、Policy/Profile、Fact/Relation transition、legacy Slice、CoverageLedger、manifest、persistence、public Review 产品或 R2–R6。
> 本文自己的完整资格链闭合以前，新的 `ALLOWED` 不生效。

## 1. CONTROL LOOP 与 qualified publication input

文档 311 由 PR #356 final head `af9e8c225efe14d5a9a3f5a0fb729f2fb6dbb360` 从
`main@e88310ca1c4c5a382d097e8d0b68193b106549c5` 构造，candidate 与 merge tree 均为
`b2c8e9dfd0cf2adb3e87ffbf8b1b01c9b044f155`，受保护合入后的 exact main 为本构造坐标。三个公开门均使用原始 attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #356 original Public CI | `39435033981` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39439635290` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39439635449` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product readback 的最终 qualifying set 是 README、doc311、milestones 各唯一一个
`FORMAL_READBACK_PASS`。它没有覆盖此前的失败路径：setup1 中 doc311 formal #1 的 render navigation timeout、README formal #1
把 Markdown link destination 误作 rendered marker；setup2 中 fixed render window 对 deep README marker 不可见；setup3 中 README
formal #1 的匿名额度耗尽与 render timeout、README formal #2 的 response body error，以及 milestones formal #1 的另一匿名 egress
bucket 耗尽与 render timeout，全部按原 identity 保留。后继 fresh diagnostic、真实 reset 与新 Plan/session/output 只取得新的资格事实，
没有重解释旧观察。

setup1 与 setup2 的最小分类分别为：

```text
e3858e3439ae157f45c71592e71dca59a71892cd4aef9fc2676f010e54ea2c12
c84ce92f4a39fe5ab26bcea4b2b670f3d3b20f3189aa83c1c52efb8c32d3a45e
```

setup3 independent reconciliation 与 230-artifact finite closeout 分别为：

```text
71bc49fcb4c6c0b943f5c825cf61d885cd914f54d82253b5345fa607a397ad4f
7a062bb3589d2252b3e999eda48338c5949c18fb3b970affb70efeeb56a432ba
```

因此 doc311 现在是 `CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。它证明新的最小合法 seam 是本 docs-only authority
recovery publication；它没有自行恢复 authority，也没有创建 bridge 或 composition runtime。

Fact → Relation corrected successor private transition 已由 doc310 的独立资格链冻结。它保留 exact `DerivationInputSet`、original live
`BudgetContext`、`AttemptEligibility`、complete RelationSet 与 one-shot continuation，但它的 authority ceiling 明确不拥有
ReviewSliceSet / Coverage。

## 2. authority recovery 的对象是 Relation → Slice 边

当前分别成立：

```text
Fact -> corrected Relation transition is FROZEN
transition admission is QUALIFIED
transition continuation is one-shot and exact-world-bound
legacy Slice primitives remain unchanged
CoverageLedger 0.3 validation-only conformance is FROZEN
```

这些局部事实不能推出 composition edge 已经成立。current Slice input 只接受 exact legacy
`OwnedRelationQualificationContinuation`；对 `OwnedFactRelationTransitionAdmission` 与
`ClaimedFactRelationTransitionContinuation` 都以 `ADMISSION_BINDING_REJECTED` 正确 fail closed。相同 RelationSet、digest、inputs、
context、eligibility 或 semantic result 都不能把 successor transition 冒充 legacy Slice authority。

本文条件化恢复的 implementation authority 只允许建立：

```text
RELATION_TRANSITION_TO_SLICE_AUTHORITY_BRIDGE
```

该 bridge 必须由 application 拥有、versioned、private、one-shot，并独立证明 exact transition continuation 有资格连接 existing
Slice primitives。它不能修改 transition ceiling、放宽 legacy exact-type gate、暴露或复用 legacy private token、伪造 legacy
qualification，也不能重新运行 Relation。

## 3. 条件化恢复的 bounded A–J

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多落实以下 A–J：

| ID | 最大施工面 |
| --- | --- |
| A | application 对 exact one-shot `ClaimedFactRelationTransitionContinuation` 建立单一 bridge attempt；绑定 original transition admission、request、terminal partition、complete RelationSet、`DerivationInputSet`、live `BudgetContext` 与 `AttemptEligibility`，不创建第二个 claim、context 或 Relation rerun |
| B | 在任何 Slice work 前逐项复核 transition identity/version、admission `QUALIFIED`、same-attempt lineage、complete expected/emitted/terminal equality、source/policy/profile/product/path identities、claim active state与original live-object identity；foreign world、consumed claim或digest-only holder fail closed |
| C | 新增可区分的 application-owned versioned bridge identity、request、admission与continuation carrier；legacy Relation/Slice classes、constructors、tokens与wire bytes保持不变 |
| D | 从 transition admission与完整 RelationSet双向机械重算 bridge input universe；每个 Relation、terminal outcome与历史成员都必须可追溯，blocked、unknown、partial与closed-empty不得丢失、折叠或按成功项缩小 |
| E | 通过新的 private bridge path调用existing Slice input validation primitives并签发versioned successor Slice authority；不得让legacy exact-type gate直接接受successor bytes，也不得把RelationSet digest当作authority |
| F | 只有 bridge admission成功后才允许复用doc267/287限定的Slice obligation、assignment、traversal、reconciliation与closure primitives；Slice denominator由冻结规则从完整上游世界推导，不由实际output、representability或UI convenience反推 |
| G | 从exact Slice closure构造private `ReviewSliceSet` successor，保留member identity、closure authority、normal/partial/blocked/unknown/closed-empty terminal history与same-attempt provenance；相同members或digest不继承authority |
| H | 对七阶段`S/A/N/D` universe、stage transition proofs、ordered root chain、expected/emitted/terminal accounting与Coverage item/disposition mapping做total、bidirectional、exactly-once reconciliation；任何gap、overlap、duplicate、foreign或denominator drift停止 |
| I | `CoverageLedger 0.3`只作为validation-only conformance与root-chain witness；不能创建上游事实、改变terminal state、生成Slice authority、选择manifest successor或取得publication authority |
| J | 固化transition→bridge foreign/consumed/digest-only/new-context/rerun/legacy-token falsifiers、missing/duplicate/foreign Relation与Slice members、blocked/unknown/partial/closed-empty preservation、old/new wire rejection、legacy-byte guards及Python 3.10 / 3.13 × normal / `-O` canonical reports |

Python class、protocol suffix、字段布局与测试数量由后继实现选择，但必须保持 bounded、versioned、private、可区分与可机械复算。
A–J 是 authority ceiling，不是 implementation 已存在的事实，也不要求用一个万能对象承载所有责任。

## 4. 不变量与 authority ceiling

后继实现必须保持：

```text
transition continuation identity and one-shot state are preserved
original inputs/context/eligibility remain the same live world
complete RelationSet and terminal history are never projected away
Slice obligation universe is derived independently from frozen rules
ReviewSliceSet membership identity != Slice closure authority
Coverage qualification cannot rewrite upstream truth or denominator
same bytes or digest != same authority
```

本文最后门闭合以后只允许：

```text
实现 bounded private Relation-transition-to-Slice bridge A–J
+ 增加对应 private tests / audit fixtures / falsifiers
+ 复用已冻结 Fact -> Relation transition、legacy Slice primitives与CoverageLedger 0.3 conformance
+ 形成独立 implementation candidate
```

它不允许：

- 修改 doc267/287/290/294/299/306/310/311 的 frozen 或 qualified history；
- 修改、过滤或重跑 Fact / Relation，创建新 `BudgetContext`，或跨 attempt 拼接 equal inputs；
- 让 legacy Slice gate 接受 successor bytes，暴露或复用 private constructor token，或伪造 legacy qualification；
- 用 RelationSet digest、successful subset、actual outputs、caller bool 或 representability 定义 Slice/Coverage denominator；
- 丢弃 blocked、unknown、partial、closed-empty 或 failed Provider / transition / Slice history；
- 修改 public/default composition、Schema、Policy/Profile、CoverageLedger 0.3 semantics、workflow 或 required gates；
- 选择 manifest successor、persistence Route A/B、public carrier/product、Evidence/Bundle/publisher、post-R1 Benchmark、R2–R6、tag 或 Release。

## 5. 历史 authority 与新 authority 不得合并

doc288 曾发布 composition private implementation authority，后被 Fact → Relation exact-input反例触发停止线。该历史继续成立：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
```

doc290–310 修复并冻结 Fact → Relation 依赖；doc311只审计current authority topology。本 publication以新的exact world、资格链和
更窄 ceiling恢复当前可消费 authority。因此不得推导：

```text
old allowed history == current consumable authority
Fact -> Relation frozen == Relation -> Slice edge implemented
current-state audit qualified == bridge authority recovered
same A-J labels == same authorization identity
later implementation PASS == old stopped world backfilled
```

新 authority 只在本 publication 的全部门闭合后生效；随后仍须返回 CONTROL LOOP，不能把 publication 自身算作 implementation。

## 6. implementation stop conditions

授权生效后的施工出现以下任一条件，必须保留首个反例并停止，只重开被击穿的最小边界：

1. exact transition continuation无法在消费前机械绑定到original admission/history/inputs/context/eligibility同一world；
2. 必须修改transition ceiling、创建新claim/context、重跑Relation或使用digest-only authority才能进入Slice；
3. 必须放宽legacy Slice type gate、复用private token或伪造legacy qualification；
4. 无法从transition admission与complete RelationSet双向重算bridge input universe；
5. Slice obligation universe只能由actual outputs、representable subset、caller bool或成功项定义；
6. blocked/unknown/partial/closed-empty历史不能无损进入ReviewSliceSet/Coverage reconciliation；
7. expected/emitted/terminal或seven-stage join出现missing、duplicate、foreign、unassigned、cross-world或denominator drift；
8. 必须修改public/default bytes、CoverageLedger semantics、manifest、persistence或publisher才能闭合private composition；
9. direct falsifier击穿doc267/281/287/310 frozen semantics，而不是暴露局部implementation defect；
10. 只有弱化oracle、删除negative history、拼接不同world、重跑到PASS或移动成功条件才能取得PASS。

已经生效的 authority也不能成为扩大scope、静默reopen frozen contract、覆盖旧失败或启动后续阶段的理由。

## 7. 本 publication 的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/312-r1-review-slice-set-coverage-composition-authority-recovery-publication.md
docs/milestones.md
```

doc267、doc281、doc287–311、runtime、tests、workflows、Schema、Policy/Profile、Fact/Relation transition、legacy Slice、
CoverageLedger、manifest、persistence与全部保留evidence必须保持`35e99a8…` base bytes。local gates至少复算四文件scope、
UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、`git diff --check`、read-only global/local hygiene、
doc311完整资格链、Fact → Relation freeze完整资格链、#346 retained failure与primary `audit.json` hash continuity。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc311 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure / qualified-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

README render qualification必须用可见、稳定、非link-destination的marker并同时核对exact public raw bytes；deep README link text不在固定
render window内时不能冒充缺字节，也不能把raw-byte equality冒充render proof。每个required target必须有唯一qualifying PASS；formal
non-success、diagnostic与setup history从实际记录机械枚举。same patch、相同tree、original PR green或后继PASS不能替代任一门。

## 8. 当前 target 与生效上限

全部门闭合以前只能记录：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只允许升级为：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
```

旧 composition authority仍作为历史保留；manifest、persistence、public Review、post-R1 Benchmark与R2–R6状态不变。后继必须从新的
exact main重新执行 CONTROL LOOP，确认A–J仍是最小合法seam，才可创建implementation branch。
