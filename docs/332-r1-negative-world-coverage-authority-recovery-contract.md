# R1 negative-world Coverage authority recovery 最小合同 0.1

> 状态：`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。本文只冻结一个私有、same-attempt、one-shot 的
> negative-world Coverage candidate / validation / admission seam；不实现 runtime，不修改 CoverageLedger 0.3、positive
> composition、manifest、Evidence、persistence 或 public Review。
>
> 上游：[Coverage root binding correction contract](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)、
> [CoverageLedger 0.3 implementation freeze](286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)、
> [positive Slice/Coverage composition freeze](314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)、
> [negative-world authority audit](319-r1-negative-world-coverage-authority-recovery-audit.md)、
> [exact-input carrier contract](321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)、
> [carrier implementation freeze](330-r1-fact-to-coverage-exact-input-successor-private-implementation-freeze-publication.md)、
> [exact-input 后继审计](331-r1-negative-world-coverage-authority-recovery-after-exact-input-audit.md)。

## 1. CONTROL LOOP 与qualified起点

本合同绑定exact `main@348b3bdcbf8b459d52f17d2091cb1bb00a60197d`，tree
`5a1ec99b4e115238977b2a2b1276e0f330a863b8`。该world已经机械证明：

1. `r1-fact-to-coverage-exact-input-handoff-successor/0.2`能够从五类Fact terminal branch交付terminal-validated
   original `DerivationInputSet`、原始`BudgetContext`、Snapshot/Policy/Profile/blob truth及same-object-graph proof；
2. CoverageLedger 0.3 Schema、root binding、seven-stage partition、conformance与四类safe-negative compatibility vectors已经冻结；
3. current runtime只有carrier，没有第二个模块消费`ClaimedFactToCoverageExactInputHandoff`；
4. positive composition只消费`ClaimedRelationTransitionSliceBridgeContinuation`，不能合法接管Fact阻断world；
5. `validate_review_coverage_ledger()`是validation-only seam：caller提供root/stage projections，它不枚举分母、不生成candidate，也不授予
   live authority。

qualified起点因此是：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDITED_INPUT_AVAILABLE_PRODUCER_ABSENT
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文只重开`application-owned negative-world Coverage producer + independent validation + admission`这一条最小边；不会回填
doc319、改写doc281–286或恢复旧composition authority。

## 2. 新反例：validation-only agreement不等于authority

current conformance在其声明边界内是正确的，但不能独自承担本合同的资格责任。read-only audit机械构造了两个caller同时改写
candidate和source的反例：

```text
original ALL_PARSE_REJECTED
  Parse denominator = 1
  parse_failed       = 1
  overall            = PARTIAL

self-consistent caller rewrite
  Parse denominator = 0
  parse_failed       = 0
  source.stage_projections同步缩小
  overall            = COMPLETE
  ledger digest / conformance source同步复算

current conformance result = PASS
```

同样，caller可以把该world连同root history一致改写为`ZERO_PARSE_DENOMINATOR`并通过validation-only seam。这个结果不是
CoverageLedger validator defect；它证明该validator只回答：

> candidate是否与caller提供的copy-owned history一致？

它没有资格回答：

> caller提供的history是否就是original input与terminal Fact world要求的完整history？

因此本合同冻结：producer不得提供自己的conformance oracle。independent validator必须从original carrier重新枚举分母、root和stage
history，再构造conformance source。只有`independent rederivation + existing 0.3 conformance + same-attempt admission`同时成功，candidate
才取得private资格。

## 3. authority topology

规范拓扑为：

```text
ClaimedFactToCoverageExactInputHandoff 0.2
    │ exact private consumer / one shot
    ▼
application-owned negative-world attempt
    ├── candidate producer
    │     └── CoverageLedger 0.3 candidate only
    ├── independent history validator
    │     ├── rederive complete denominators from original inputs
    │     ├── rederive branch-specific root/stage projections
    │     ├── bind_coverage_ledger_conformance_source(...)
    │     └── validate_review_coverage_ledger(...)
    └── same-attempt admission
          └── private admitted Coverage result
```

责任必须保持分离：

| owner | 可以决定 | 不得决定 |
| --- | --- | --- |
| carrier | exact Fact terminal source、original inputs/context、object identity、live/revoked state | Coverage分母、root、status或admission |
| producer | 根据已冻结规则构造一个0.3 candidate | 自己声明history完整、自己授予authority |
| independent validator | 从original carrier独立复算history并核candidate | 修补candidate、选择更方便的branch |
| existing 0.3 conformance | 校验canonical/root/stage/digest一致性 | 枚举分母、取得live claim |
| admission | 绑定同一carrier/context/validation result并exactly-once commit | 恢复upstream eligibility、授予manifest/public authority |

## 4. normative identities 与版本停止线

本文冻结以下private identity：

```text
input carrier function
  r1-fact-to-coverage-exact-input-handoff-successor/0.2

input consumer
  r1-negative-world-coverage-exact-input-consumer/0.1

composition function
  r1-negative-world-review-coverage-composition/0.1

independent validation function
  r1-negative-world-review-coverage-independent-validation/0.1

admission function
  r1-negative-world-review-coverage-admission/0.1

Relation absent producing function
  r1-negative-world-relation-set-predecessor-absence/0.1

ReviewSlice absent producing function
  r1-negative-world-review-slice-set-predecessor-absence/0.1

unrepresentable Fact obligation domain
  veritrail.review.negative-world-unrepresentable-fact-obligation/0.1
```

Coverage child继续精确使用：

```text
artifact_kind            COVERAGE_LEDGER
schema_version           0.3
canonicalization_profile veritrail-json-c14n/1
ledger domain            veritrail.review.coverage-ledger/0.3
root binding domain      veritrail.review.coverage-root-binding/0.1
root chain domain        veritrail.review.coverage-root-chain/0.1
terminal history domain  veritrail.review.coverage-root-terminal-history/0.1
root binding function    r1-review-coverage-root-binding-correction/0.1
conformance identity     r1-review-coverage-ledger-conformance/0.3
```

本文不创建CoverageLedger 0.4，也不修改0.3 Schema、fixture、reason enum或conformance。closest version、旧0.1 carrier、legacy
handoff、positive composition claim或caller自报identity必须fail closed。

## 5. total input domain 与负路径限定

negative consumer只接受以下四个Fact terminal branch：

```text
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

`NORMAL_FULFILLED`必须拒绝并保留给positive Fact→Relation→Slice composition；unsafe release、interrupted history、foreign/equal-copy
carrier、late stop、mutated inputs、replayed carrier和unknown branch都不得生成Ledger。拒绝negative path不等于negative Coverage
`UNKNOWN`；前者没有admitted candidate。

`REQUIRED_PROVIDER_NON_SUCCESS`的upstream eligibility可以正确保持`REVOKED`。consumer不得调用只允许live parent admission的
`_inputs_ref()`，不得把parent eligibility恢复为`ADMITTED`，也不得把terminal handoff合法性误写为Provider执行成功。它只消费
0.2 carrier中已经terminal-bound的original inputs与仍为`RUNNING`的原始BudgetContext。

## 6. 完整denominator必须从original inputs独立推导

seven-stage denominator顺序继续为：

```text
SNAPSHOT_INVENTORY
POLICY_SCOPE
LANGUAGE_SUPPORT
PARSE
FACT_DERIVATION
RELATION_DERIVATION
SLICE_DERIVATION
```

independent validator必须从carrier的original input bytes与terminal source复算下表；不得读取producer生成的stage作为oracle：

| stage | denominator source | total partition |
| --- | --- | --- |
| Snapshot | SourceSnapshot完整`inventory[]` | 全部`completed` |
| Policy | 同一完整inventory与逐项`scope_decisions[]` | in-scope进入`completed`；其余进入`out_of_scope / POLICY_EXCLUDED` |
| Language | 只对in-scope inventory独立复算`r1-python-language-support/0.2` subjects | eligible进入`completed`；其余进入`unsupported`并保留精确reason |
| Parse | 完整Language eligible subject identity集合 | accepted进入`completed`；rejected进入`parse_failed / PARSE_ERROR` |
| Fact | 完整`fact_projection.universe[]` | representable/completed、semantic blocker或execution non-success恰好一次 |
| Relation | Fact universe为空时known-empty；Fact artifact缺失且universe非空时unknown | empty completion或`UPSTREAM_DENOMINATOR_UNKNOWN` |
| Slice | Relation known-empty时known-empty；Relation denominator unknown时unknown | empty completion或`UPSTREAM_DENOMINATOR_UNKNOWN` |

Snapshot item identity继续使用`veritrail.review.coverage-inventory-entry/0.1`。Language/Parse item identity使用冻结的
`subject_identity`。所有array必须按CoverageLedger 0.3 canonical order排序并去重。

同一Fact branch不决定前面阶段status。机械反例冻结为：

| world | Snapshot | Policy | Language | Parse | Fact | Relation | Slice | overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| truly empty `ZERO_PARSE_DENOMINATOR` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE |
| unsupported-only `ZERO_PARSE_DENOMINATOR` | COMPLETE | COMPLETE | PARTIAL | COMPLETE | COMPLETE | COMPLETE | COMPLETE | PARTIAL |
| policy-excluded-only `ZERO_PARSE_DENOMINATOR` | COMPLETE | PARTIAL | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | PARTIAL |
| `ALL_PARSE_REJECTED` | COMPLETE | COMPLETE | COMPLETE | PARTIAL | COMPLETE | COMPLETE | COMPLETE | PARTIAL |
| `PROJECTION_BLOCKED` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN |
| `REQUIRED_PROVIDER_NON_SUCCESS` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN |

因此从branch直接复制compatibility fixture status、把三种zero-Parse world合并或只看`fact_set is null`都不合格。

## 7. Fact obligation identity、completion与non-success

Fact denominator必须与`fact_projection.universe[]`建立双向total binding：

1. 以`subject_key_digest`将每个universe slot与恰好一个`expected[]`或`blockers[]`成员绑定；
2. representable成员使用冻结的`fact_id`作为`FACT` item id；
3. unrepresentable成员没有合法Fact artifact identity，必须用
   `veritrail.review.negative-world-unrepresentable-fact-obligation/0.1`对完整input identity、slot和candidate计算obligation id；
4. missing、duplicate、collision、one slot同时expected/blocker或candidate无法canonicalize都fail closed；
5. `U`是全部Fact refs，`E`只包含独立证明已经完成的refs，不得以`expected[]`直接冒充`completed[]`。

branch-specific partition冻结为：

- `ZERO_PARSE_DENOMINATOR`与`ALL_PARSE_REJECTED`：Fact `U=E=∅`；前者仍保留上游Policy/Language disposition，后者保留全部
  rejected Parse refs；
- `PROJECTION_BLOCKED`：representable expected refs进入`completed`，blocked slot进入`blocked /
  UNREPRESENTABLE_EXPECTED_FACT`，Relation/Slice denominator为unknown；
- `REQUIRED_PROVIDER_NON_SUCCESS`：每个successful terminal的canonical Fact bytes必须重新admit并与expected id匹配后才能进入
  `completed`；其余ref必须由Provider request的assigned product responsibility覆盖。`UNAVAILABLE`映射
  `execution_failed / PROVIDER_UNAVAILABLE`，`FAILED`映射`execution_failed / DERIVATION_ERROR`；mixed world保留每项真实responsibility
  与reason union。没有non-success responsibility的missing ref、unexpected terminal fact或caller提供的successful subset都fail closed。

这条规则明确修正一个容易出现的代理错误：`expected count`不是`completed count`。

## 8. branch-specific absent roots 与stage status保持正交

四类negative world的root chain都为：

```text
FACT_SET        QUALIFIED_ABSENT / exact Fact terminal branch
RELATION_SET    QUALIFIED_ABSENT / PREDECESSOR_ABSENT
REVIEW_SLICE_SET QUALIFIED_ABSENT / PREDECESSOR_ABSENT
```

但binding identity必须保留branch-specific terminal history，不能共享一个“no facts”identity：

- Fact history按0.3已冻结member names保留`absence / blockers / denominator / e / u`，并在适用时保留
  `rejected_parse_products`或`provider_outcomes / provider_responsibility`；这些值必须是完整canonical projections，不得只留count；
- Relation/Slice history分别绑定exact predecessor binding digest、`PREDECESSOR_ABSENT`和原Fact transition branch；
- 所有absence binding没有artifact digest，禁止创建empty FactSet、RelationSet或ReviewSliceSet；
- `QUALIFIED_ABSENT`不自动把dependent stage变成COMPLETE。projection/provider world的Relation/Slice stage仍为UNKNOWN。

Fact producing function绑定terminal source中的`r1-fact-projection-fulfillment/0.1`。Relation/Slice predecessor absence使用§4两个新
private function identity。root binding、chain和Ledger digest仍按0.3冻结domain复算。

## 9. independent validation：不允许producer自证

independent validator必须直接接收同一live carrier/attempt与candidate，且必须：

1. 重新验证carrier object identity、original inputs、input seal、canonical bytes、blob map、五digest、Fact terminal source与live context；
2. 不调用producer的denominator/root/stage helper，不接受producer返回的conformance source；
3. 独立执行§6–8的total derivation，生成自己的root binding projections与stage projections；
4. 用自己的projections调用`bind_coverage_ledger_conformance_source(..., authority_safe=True)`；
5. 调用`validate_review_coverage_ledger(candidate, source)`验证0.3 canonical/root/stage/digest规则；
6. 比较candidate input identity与original `DerivationInputSet`五digest；
7. 输出一个不可由caller构造、绑定carrier claim id、candidate digest与validation function identity的private validation result。

“不同函数名”不构成independence。implementation qualification必须用mutation falsifiers证明：即使producer与candidate一起漏项、改branch或
重算全部digest，independent validator仍从original inputs恢复完整denominator并拒绝。

## 10. same-attempt、one-shot与admission

consumer与admission必须满足：

1. 一个carrier只能被negative consumer消费一次；并发消费恰有一个成功；
2. copy-equal carrier、foreign input/context、foreign validation result与serialized fixture都不能取得admission；
3. carrier claim id、original context object、input object、Fact source digest、candidate digest与validation result必须属于同一object graph；
4. late cancellation、deadline、stop trigger、input/blob/source mutation、replay或post-validation candidate mutation永久撤销本negative attempt；
5. admission只能在全部validation成功后以原始`BudgetContext.try_complete_phase(..., resources_closed=True)`exactly once commit；
6. `REQUIRED_PROVIDER_NON_SUCCESS`不得恢复upstream revoked eligibility；admission是新的、有限的negative Coverage authority，不是旧
   Fact/Relation/Slice eligibility复活；
7. admitted result每次read都重验carrier、context、committed phase、candidate bytes与validation binding。

authority ceiling固定为：

```text
private_negative_world_coverage_ledger = true
fact_set                              = false
relation_set                          = false
review_slice_set                      = false
positive_composition                  = false
manifest                              = false
evidence                              = false
persistence                           = false
public_review                         = false
```

## 11. typed failure families

后继implementation至少必须区分：

```text
NEGATIVE_INPUT_REJECTED
NEGATIVE_INPUT_ALREADY_CONSUMED
UNSUPPORTED_TERMINAL_BRANCH
DENOMINATOR_DERIVATION_REJECTED
FACT_OBLIGATION_BINDING_REJECTED
ROOT_PROJECTION_REJECTED
CANDIDATE_RECONCILIATION_REJECTED
INDEPENDENT_VALIDATION_REJECTED
SAME_ATTEMPT_ADMISSION_REJECTED
```

这些是private failure families，不修改CoverageLedger reason enum。unsafe/foreign/replay属于无admission，不得伪装成一个合法
Coverage `UNKNOWN`。

## 12. normative falsifier matrix

| ID | falsifier | required result |
| --- | --- | --- |
| NWCR-000 | `NORMAL_FULFILLED`送入negative consumer | exact reject；positive path不变 |
| NWCR-001 | empty / unsupported-only / policy-excluded-only共享`ZERO_PARSE_DENOMINATOR` | 三者保留不同stage partition与overall/digest |
| NWCR-002 | `ALL_PARSE_REJECTED`删除一个Parse item并同步缩小candidate/source | independent denominator reject |
| NWCR-003 | caller把all-rejected连同root/stage/digest改写为zero-denominator | branch authority reject |
| NWCR-004 | projection blocker从Fact `U`删除，或只保留representable `E` | total Fact binding reject |
| NWCR-005 | blocker塞入`execution_failed / DERIVATION_ERROR` | semantic disposition reject |
| NWCR-006 | Provider `FAILED`与`UNAVAILABLE`合并成同一reason | exact lifecycle/reason mapping reject |
| NWCR-007 | `expected[]`全部标为completed但Provider terminal non-success | completion proof reject |
| NWCR-008 | 创建empty FactSet/RelationSet/SliceSet替代qualified absence | root projection reject |
| NWCR-009 | dependent stage因root absent被强制写成COMPLETE | independent stage derivation reject |
| NWCR-010 | frozen fixture通过0.3 conformance但没有live carrier/admission | validation可PASS，authority必须REJECT |
| NWCR-011 | producer返回自己的conformance source | independent validation reject |
| NWCR-012 | equal-copy/foreign carrier、input、context或validation result | same-attempt reject |
| NWCR-013 | sequential/concurrent replay | exactly one admission；其余reject |
| NWCR-014 | validation后candidate、input、blob、source或context发生漂移 | permanent revoke / reject |
| NWCR-015 | late stop、deadline或cleanup不完整 | no admitted Ledger |
| NWCR-016 | closest version/function/consumer identity | exact identity reject |
| NWCR-017 | 借negative result启动manifest/Evidence/persistence/public Review | authority ceiling reject |
| NWCR-018 | 修改positive composition或Ledger 0.3 oracle让candidate通过 | STOP_CONDITION_TRIGGERED |

## 13. read-only feasibility evidence

在exact base上，read-only contract audit覆盖：

- seven live denominator worlds：empty、unsupported-only、policy-excluded-only、all-parse-rejected、projection-blocked、required Provider
  failed、required Provider unavailable；
- 四类frozen negative compatibility cases；
- self-consistent denominator shrink、branch rewrite及fixture-without-admission三个authority falsifiers；
- current source中不存在第二个exact-input carrier runtime consumer；
- frozen Ledger、carrier、positive composition与上游合同bytes未改。

Python 3.10.6 / 3.13.13 × normal / `-O`四格的canonical report SHA-256一致为：

```text
ed0450c8a63a2c99222d996d6832cbf8f14dea82e5022c0ef6cb2bcbe4a9a903
```

首轮diagnostic曾错误地把required-provider world的`expected`数汇总为`completed`数；该prequalification facility defect已按原identity
保留，修正后的四格才属于本candidate witness。read-only结果证明合同可构造，不证明runtime已经实现。

## 14. implementation non-decisions 与stop conditions

本文不决定private class/file布局、锁或weak-map实现，也不要求producer与validator运行在不同进程。后继feasibility可以选择最小实现，
但不得改变下列semantic边界：

- 不修改0.2 carrier identity或五类terminal truth；若需要新增private consume hook，必须保持既有public method list与copy semantics；
- 不修改CoverageLedger 0.3 Schema/conformance/fixture来适配producer；
- 不调用或扩大positive composition authority；
- 不把compatibility fixture当运行时oracle或ground truth source；
- 不把root absence、stage status、validation PASS与admission合并；
- 不选择manifest successor、Evidence continuity、persistence或public Review；
- 不启动post-R1 Benchmark或R2–R6。

实现若无法从original carrier独立恢复某一完整denominator、无法区分Provider responsibility、需要caller选择branch、或只能让producer
和validator共享同一关键projector，必须停止施工并重开被击穿的最小合同边界。

## 15. 本candidate资格门与状态上限

本candidate只允许修改：

```text
README.md
AGENTS.md
docs/332-r1-negative-world-coverage-authority-recovery-contract.md
docs/milestones.md
```

资格链必须依次闭合：

1. exact base/head/tree与上述4-file scope；
2. read-only audit四格canonical一致；
3. focused Ledger/carrier/Fact/positive composition regression四格；
4. links、Markdown、UTF-8/LF/final LF、global/local hygiene与primary `audit.json` continuity；
5. original PR required gates；
6. protected exact-head merge；
7. new exact-main Public CI 11/11与Browser Smoke 1/1；
8. fresh anonymous installed-product README/doc331/doc332/milestones readback；
9. independent reconciliation与finite closeout。

任何FAIL、ERROR、CANCELLED、setup failure、rate-limit或UNKNOWN保持原identity；不得rerun until PASS、回填旧world或修改oracle。全部
闭合后本文最多升级为：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
```

`CONTRACT_FROZEN`必须由后续独立docs-only freeze publication及其完整资格链生效。本candidate本身不授予implementation authority。

当前candidate target为：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDITED_INPUT_AVAILABLE_PRODUCER_ABSENT
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

下一步只能是本candidate自己的完整资格链。它成为qualified candidate后仍必须返回CONTROL LOOP，再决定独立contract freeze
publication；不能直接施工runtime。
