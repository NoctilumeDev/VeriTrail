# R1 Fact handoff → Relation corrected successor 私有实现 authority recovery publication

日期：2026-10-20

> 状态：`R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@2a461ad476aaeed207f4d60bcabd3e235c4aba7e`，tree
> `0fcd57aa20b32b1b882d391a76a52cbc03b793ab`。
>
> 上游：[Fact handoff → Relation correction 合同](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)、
> [stage applicability capability identity 修正合同](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)、
> [旧 corrected successor 授权](297-r1-fact-relation-corrected-successor-private-implementation-authorization-publication.md)、
> [import-form Provider implementation freeze](306-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-freeze-publication.md)
> 与 [current-state audit](307-r1-fact-relation-corrected-successor-authority-recovery-current-state-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_RECOVERY_PUBLICATION_ONLY`。本文只条件化恢复一段 bounded、private、versioned、
> handoff-owned transition implementation authority；不修改 runtime、tests、workflows、Schema、Policy/Profile、Provider、
> manifest、persistence、Coverage、public Review 产品或 R2–R6。本文自己的完整资格链闭合以前，`ALLOWED` 不生效。

## 1. CONTROL LOOP 与 qualified publication input

文档 307 由 PR #352 final head `ed5211609271dd522b3ca474201b76cc02748139` 从
`main@6cbd7ae5088bb232cbb64e51acc7298441272ab6` 构造，candidate 与 merge tree 均为
`0fcd57aa20b32b1b882d391a76a52cbc03b793ab`，受保护合入后的 exact main 为本构造坐标。三个公开门都使用原始 attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #352 original Public CI | `39375812065` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39378248233` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39378248142` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product doc307、milestones 与 README 各有唯一 `FORMAL_READBACK_PASS`。README formal #1 在 P2
render `COMPLETE` 的同时由匿名 P1 API 观察到 `403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0`，reset 后先以新的
rate diagnostic 与 exact-commit preflight确认额度恢复，再由新的 Plan/session/handoff identity 取得 formal #2 PASS。首个
`FORMAL_READBACK_ERROR`完整保留，未被覆盖或重解释。

independent reconciliation、162-artifact closeout 与 finite closeout integrity 分别为：

```text
e78ebd5296652e0168b73ef73cb1d8dbbd26ae2c7078379a76217e485435ef50
f10c27507f7fa799675525a0e8820dffe0c9aaf25fe27beee2cc1f16634efc27
44a2ca60f68f8fd458f19ad022e6a1c4fbb326af21b8726c208064a247b8ba44
```

因此文档 307 现在是 `CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。它证明下一最小合法 seam 是本 docs-only
authority recovery publication；它没有自行恢复 authority，也没有创建 transition runtime。

corrected import-form Provider implementation 已由文档 306 的独立资格链冻结在
`main@6cbd7ae5088bb232cbb64e51acc7298441272ab6`。其 independent reconciliation、159-artifact closeout 与 finite
integrity 分别为：

```text
43b74760aef0dcb102e0d0d8fcbd6ba068af7e1521f44b53db18f158613dafda
bc0a7f29b80272eb8287598529c1bc9fae0490837645593b522b91af5e165abe
bed71633b03a65bed58ddde4d0476ce3dd0478732ba8a22e40be3347210d2555
```

#346 exact-main Public CI `39321768248` 的 required Starter mobile `net::ERR_NO_BUFFER_SPACE`失败、Artifact、
`UNKNOWN`底层资源原因与 doc301 not-qualified 状态继续保留；doc302/doc303 的后继资格历史没有回填该 world。

## 2. authority recovery 的对象是一条 transition，不是两个节点的并置

当前已分别取得资格的事实是：

```text
complete same-attempt Fact handoff
corrected import-form Relation Provider
frozen interoperability and stage-applicability semantics
```

这些局部事实不能推出 Fact → Relation 边已经存在。当前 combined-policy Fact entry仍正确 fail closed；Fact-only handoff仍不能与
combined-policy exact input跨 world join；high-level Relation entry仍会创建新 `BudgetContext`并重跑 Fact。现有 import-form
carrier也没有完整绑定 handoff claim、original context、stage ownership、per-product closure、complete obligation projection或
expected/assigned obligation identities。

本文恢复的 authority 只允许实现：

```text
COMMON_EXACT_INPUT_PLUS_LIVE_HANDOFF_TO_CORRECTED_RELATION_ADMISSION
```

它要求候选 transition 自己承担证明责任。Fact 与 Provider 的局部资格、相同 digest、相同 semantic result或后继测试绿灯都不能替代
这条边的 qualification。

## 3. 条件化恢复的 bounded A–J

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多落实以下 A–J：

| ID | 最大施工面 |
| --- | --- |
| A | application 建立一个 private composition attempt，绑定 exact immutable `DerivationInputSet`、一次领取的完整 Fact handoff 与 handoff 的 original live `BudgetContext`；不创建第二个 Fact claim、新 context或 Fact rerun |
| B | 在任何 Relation work 前逐项复核 source snapshot、sealed Policy、analysis scope、derivation profile、slice policy、classification、Fact consumer attempt、product set、safe branch、terminal history与live object identity；foreign world、consumed claim或digest-only holder fail closed |
| C | 按冻结 `/0.2` identities 对完整 sealed Policy 构造 Fact / Relation stage applicability与 total、disjoint、exactly-once cross-stage ownership reconciliation；unknown、gap、overlap、duplicate、missing或requiredness drift均停止 |
| D | 对完整 authoritative FactSet建立 total per-product/path closure；每个 accepted product/path恰好一个 MODULE，Import只能引用同 path MODULE，全部其他 Facts 保持原 identity |
| E | 从完整 F、sealed Policy、Relation Profile与closure独立构造完整 `O_expected`，再生成 per-Provider responsibility与assignment；不得从 representable subset、candidates、Provider outputs或成功项反推 denominator |
| F | 增加可区分的 private handoff-owned successor domain/request/terminal carrier，绑定完整 F、applicability、ownership、closure、expected/assigned obligations、exact source blobs、claim/context identity、request provenance与same attempt；legacy carrier bytes不变 |
| G | 复用文档306冻结的versioned import-form Provider，只执行 application已经分配的完整obligations；Provider不能定义 applicability、修改 FactSet、扩张 Profile或取得未分配责任 |
| H | 独立核对 expected/emitted 双向相等、cardinality、每项恰有一个 terminal outcome、Provider requiredness、same-attempt provenance、完整 terminal partition与request lineage，再由新的private admission形成 Relation authority |
| I | 只有全部required reconciliation成功后才允许同一 composition attempt继续；continuation不取得ReviewSliceSet/Coverage composition、manifest、persistence、public product、Evidence、Bundle或publisher authority |
| J | 固化 `FRIC-000..018`、`FRIC-CID-001..012`、`RPIF-000..015`、foreign-policy join、consumed claim、new-context、Fact rerun、FactSet filter、cross-path parent、missing/duplicate/foreign obligation、old/new wire rejection与legacy-byte guards，并保留Python 3.10 / 3.13 × normal / `-O` canonical reports |

Python class、field、protocol suffix、文件布局与测试数量由实现选择，但必须保持 bounded、versioned、private与可区分。A–J是
authority ceiling，不是实现已存在的事实，也不是必须把十项写进一个万能类。

## 4. 不变量与 authority ceiling

后继实现必须同时保持：

```text
P = complete sealed Policy
F = complete authoritative FactSet
A_s(P) = stage s 的 applicability projection
C(F) = per-product/path closure
O_R(F) = Relation profile 的 complete obligation universe
```

并满足：

```text
P 永远不被 A_s(P) 替代
F 永远不被 C(F) 或 O_R(F) 替代
expected obligations == emitted obligations == terminally accounted obligations
same-attempt authority != same bytes or same digest
```

applicability只说明本 stage应承担什么；obligation projection只生成完整适用责任；两者都不能把世界改写成只剩可处理部分。

本文最后门闭合以后只允许：

```text
实现 bounded private Fact-handoff-owned Relation transition A–J
+ 增加对应 private tests / audit fixtures / falsifiers
+ 复用已冻结 corrected import-form Provider
+ 形成独立 implementation candidate
```

它不允许：

- 修改或过滤 complete Policy / FactSet，删除 profile-non-applicable Facts，或让 Provider定义 applicability；
- 从 Provider output、actual success或caller bool反向生成 denominator；
- 创建第二个 Fact claimant、新 `BudgetContext`、Fact rerun或跨 attempt authority；
- 把 Fact-only handoff与combined-policy exact input跨 world拼接；
- 修改 legacy Provider、public/default composition、frozen contracts、Schema、Profile/Policy或已有事实历史；
- 自动恢复旧 ReviewSliceSet/Coverage composition A–J，选择manifest successor或persistence Route A/B；
- 启动Coverage、public Review product、post-R1 Benchmark、R2–R6、tag或Release。

## 5. 历史 authority 与新 authority 不得合并

文档297曾发布 corrected successor authority，后来被完整import-form反例触发停止线。该历史继续成立：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
```

文档299–306只修复并冻结 Provider dependency；文档307只审计当前剩余边。本 publication以新的exact world、资格链和更窄
ceiling恢复当前可消费 authority。因此不得推导：

```text
old allowed history == current consumable authority
Provider frozen == transition implemented
current-state audit qualified == authority recovered
same A–J labels == same authorization identity
later implementation PASS == old stopped world backfilled
```

新 authority 只在本 publication 全部门闭合后生效；随后仍须返回 CONTROL LOOP，不能把 publication 自身算作 implementation。

## 6. implementation stop conditions

授权生效后的施工出现以下任一条件，必须保留首个反例并停止，只重开被击穿的最小边界：

1. exact input、claimed handoff与original context无法在消费前机械绑定到同一 world；
2. 必须创建第二个 Fact claim、新 context、Fact rerun或digest-only authority才能进入 Relation；
3. 必须过滤 FactSet、缩小 Policy或让 Provider定义 applicability；
4. 冻结 Provider在合法完整assignment下仍不能处理 required import-form world；
5. successor carrier不能无损绑定claim/context、stage ownership、per-product closure与完整obligation denominator；
6. completeness只能由Provider自证、caller bool、actual outputs或跨 attempt result证明；
7. expected/emitted/terminal partition出现missing、duplicate、foreign、unassigned或cross-path member；
8. 必须修改legacy/public bytes、manifest、persistence或Coverage才能闭合private transition；
9. direct falsifier击穿doc290/doc294/doc299 frozen semantics，而不是暴露局部implementation defect；
10. 只有弱化oracle、删除negative history、拼接不同world或移动成功条件才能取得PASS。

已经生效的 authority也不能成为扩大scope、静默reopen frozen contract、修改Provider ceiling或覆盖旧失败的理由。

## 7. 本 publication 的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/308-r1-fact-relation-corrected-successor-authority-recovery-publication.md
docs/milestones.md
```

doc290–307、runtime、tests、workflows、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage与post-R1计划
必须保持 `2a461ad…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required
markers、`git diff --check`、read-only hygiene、doc307完整资格链、Provider freeze完整资格链与#346 retained failure。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc307 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure / qualified-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一 qualifying PASS；formal non-success、diagnostic与setup history从实际记录机械枚举。same patch、相同
tree、相同semantic digest、original PR green或后继PASS不能替代任一门。

## 8. 当前 target 与生效上限

全部门闭合以前只能记录：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只允许升级为：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
```

旧 ReviewSliceSet/Coverage composition authority仍是 preserved history且继续受stop condition约束；manifest、persistence、Coverage、
public Review与R2–R6状态不变。后继必须从新的 exact main重新执行 CONTROL LOOP，确认A–J仍是最小合法seam，才可创建
implementation branch。
