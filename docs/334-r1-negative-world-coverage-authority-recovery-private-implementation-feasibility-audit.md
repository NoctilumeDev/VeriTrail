# R1 negative-world Coverage authority recovery 私有实现可行性审计

日期：2026-10-28

> 候选状态：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是qualified history，也不授权runtime施工。
>
> 审计基线：`main@637c51079151860e2634c1e7cdc60655ebf9ca45`；tree
> `756a2925da2d0394d5bd4ae4c9263ceeacc3ddaa`。
>
> 上游：[0.1合同](332-r1-negative-world-coverage-authority-recovery-contract.md)、
> [合同独立冻结发布](333-r1-negative-world-coverage-authority-recovery-contract-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_IMPLEMENTATION_FEASIBILITY_AUDIT`。

## 1. CONTROL LOOP与qualified起点

文档333由PR #384以
`base=a170489cf3adc59679b62da16c1d4aa9c2ae431c / head=9822a16c7856e3ab96d1ce0f0681426cccea27a1 /
tree=756a2925da2d0394d5bd4ae4c9263ceeacc3ddaa`受保护合入本审计基线。original Public CI
`40680647199`、exact-main Public CI `40684793219`与Browser Smoke `40684793073`均为attempt 1
SUCCESS，分别11/11、11/11与1/1。

fresh anonymous installed-product readback对README、doc332、doc333与milestones各取得唯一
`FORMAL_READBACK_PASS`。四个render diagnostic均为`DIAGNOSTIC_ONLY_NON_QUALIFYING`；anonymous rate diagnostic与
exact-commit preflight分别观察到remaining 10与HTTP 200。independent reconciliation、157-artifact finite closeout、
self-capture mismatch与finite integrity的SHA-256为：

```text
a4cf07587c6155e7672bbfe334e7ca1bf711ecdc6a7f2efea426a5aac23df995
97f4b4e2d106dc9e9a846811f3a495b44951ded80033c340a8069f763bfd672c
831dd9af0fcddb10e72766329aa39e19d0cdd015780d299e7cee121443cb8525
0de265c49be77d72060084d4f186ba1be4324e874207ce8c0576e5ae61eed330
```

其余156项终态一致；self-capture只属于wrapper ordering，semantic与qualification effect均为`NONE`。因此本轮qualified起点是：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDITED_INPUT_AVAILABLE_PRODUCER_ABSENT
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

fresh CONTROL LOOP只问：冻结合同能否在不改变既有frozen边界的前提下，由一个bounded private patch实现并独立反证。它不把
合同冻结自动解释为implementation authorization。

## 2. 七个live denominator worlds

审计从当前0.2 `ClaimedFactToCoverageExactInputHandoff`的original inputs与terminal source重建七个live worlds：

| world | Fact branch | expected overall |
| --- | --- | --- |
| empty inventory | `ZERO_PARSE_DENOMINATOR` | `COMPLETE` |
| unsupported-only | `ZERO_PARSE_DENOMINATOR` | `PARTIAL` |
| policy-excluded-only | `ZERO_PARSE_DENOMINATOR` | `PARTIAL` |
| all Parse rejected | `ALL_PARSE_REJECTED` | `PARTIAL` |
| projection blocked | `PROJECTION_BLOCKED` | `UNKNOWN` |
| required Provider failed | `REQUIRED_PROVIDER_NON_SUCCESS` | `UNKNOWN` |
| required Provider unavailable | `REQUIRED_PROVIDER_NON_SUCCESS` | `UNKNOWN` |

三类zero-parse world共享Fact terminal branch却不能共享denominator或overall；Provider failed/unavailable也保留不同terminal
outcome与reason。当前carrier已经能向独立推导路径提供Snapshot、Policy、Language、Parse、Fact、blob map、五digest、
BudgetContext与terminal source，不要求修改carrier identity或扩大public API。

## 3. common-mode falsifier可构造性

实现资格不能只比较producer candidate与producer source。审计机械保留三类独立攻击：

1. `SELF_CONSISTENT_DENOMINATOR_SHRINK`：从all-rejected world删除一个Parse item，同时缩小candidate与conformance source；
2. `SELF_CONSISTENT_BRANCH_REWRITE`：把all-rejected world连同root/stage/digest一致改写为zero-denominator；
3. `FIXTURE_WITHOUT_LIVE_ADMISSION`：冻结fixture通过0.3 conformance，却没有live carrier、same-object context与one-shot commit。

现有validation-only seam对前两类self-consistent输入可以PASS，这是其声明边界，不是产品defect。后继独立validator必须从
original carrier重新枚举，才能拒绝这些candidate；admission再拒绝第三类copy-owned fixture。

## 4. 可复用primitive与最小实现面

current source已经提供：

- 0.2 exact-input carrier、terminal-bound original input accessor与每次read重验；
- shared one-shot claim与`BudgetContext.try_complete_phase(..., resources_closed=True)`；
- CoverageLedger 0.3 canonical builder、root binding、stage projection与validation-only conformance；
- frozen Fact terminal history与Provider responsibility；
- typed stop/deadline/cancellation和permanent revoke pattern。

因此bounded implementation可以停在：

```text
one new private producer / independent-validator / admission module
    +
at most one minimal private carrier consume hook
    +
one focused private test module
    +
documentation status files
```

它不需要修改：

```text
CoverageLedger 0.3 Schema / reason order
positive composition
Fact terminal semantics
0.2 carrier identity / public method list
manifest / Evidence / persistence / public Review
```

具体class、method、locking与weak-map布局仍是implementation non-decision。feasibility只证明有限解空间存在，不提前选择最终代码形状。

## 5. producer与validator的独立性边界

“两个函数名”不等于独立。后继patch必须让：

- producer从carrier构造candidate；
- validator不调用producer的denominator/root/stage helper，也不接收producer source；
- validator从同一original carrier另行恢复完整分母与branch-specific history；
- existing 0.3 conformance只校验validator自己的source与candidate；
- admission绑定同一live carrier、context、candidate digest与validation result，并exactly once commit。

shared canonical serializer、frozen enums与0.3 validator可以复用；被测试的关键projector、denominator owner与branch chooser不得由
producer和expected oracle共同拥有。若施工时只能共享该关键错误路径，必须停止并重开最小合同边界。

## 6. read-only机械结果

审计identity为：

```text
r1-negative-world-coverage-authority-recovery-private-implementation-feasibility/0.1
```

Python 3.10.6 / 3.13.13 × normal / `-O`四格均PASS，canonical report逐字节一致：

```text
61eb43f9594ec296d62daceecd060e667576ca5e52f63df2844dc5a377a29238
```

focused witness覆盖CoverageLedger 0.3、Language Support、Fact terminal、0.1/0.2 handoff、Fact→Relation transition与positive
composition；四格各`139 tests / 138 passed / 1 skipped`。测试只证明current base与本审计判断稳定，不创建runtime或authority。

## 7. 状态上限与下一合法seam

本审计自己的完整资格链闭合以后，最多支持：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
```

下一seam只能是独立docs-only `PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION`。该publication必须重新绑定本审计的exact
资格历史并条件化授权bounded private patch；本文自身不能被runtime消费。

## 8. stop conditions

以下任一事实出现时停止当前施工，只重开被击穿的最小边界：

- original carrier无法独立恢复完整Snapshot/Policy/Language/Parse/Fact denominator；
- Provider responsibility或Fact terminal branch必须由caller选择；
- producer与validator只能共享同一个关键denominator/root/stage projector；
- one-shot consumption要求修改0.2 identity或public method list；
- 0.3 conformance、positive composition或frozen fixtures必须被弱化才能通过；
- negative result必须取得manifest/Evidence/persistence/public authority才能存在。

这些反例不会被改写成`UNKNOWN` Ledger；它们属于implementation/admission无资格。

## 9. 本candidate资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/334-r1-negative-world-coverage-authority-recovery-private-implementation-feasibility-audit.md
docs/milestones.md
```

final bytes至少复核exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、unique headings、
状态markers、upstream frozen hashes、`git diff --check`、read-only global/local hygiene与primary `audit.json` continuity。随后依次：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc333 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / frozen-history reconciliation
    -> FEASIBILITY_AUDITED qualified history
    -> return CONTROL LOOP
```

任何FAIL、ERROR、CANCELLED、setup failure、rate-limit或UNKNOWN保持原identity；不得rerun until PASS或把后继PASS回填旧world。
本文完整资格链闭合以前，开头的candidate marker不升级。闭合以后仍不得直接施工runtime、消费旧composition authority、实现
manifest/Evidence、选择persistence、发布public Review或启动post-R1 Benchmark/R2–R6。
