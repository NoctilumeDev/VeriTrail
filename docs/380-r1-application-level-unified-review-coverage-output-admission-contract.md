# R1 application-level unified Review / Coverage output admission 最小合同 0.1

日期：2026-11-08

> 候选状态：`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@84d987f1c9a164c04f1b692d7e5872ff555ef2da`，tree
> `a5be082641241ccbd81eebac5d6f031a07d9484d`。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结versioned、private、discriminated、one-shot的
> application output admission语义；不实现runtime，不创建public Schema、carrier、manifest、Evidence、persistence、
> public Review、Core Verdict或R2–R6 authority。

## 1. CONTROL LOOP 与qualified起点

[文档379](379-r1-application-level-unified-review-coverage-output-admission-current-state-audit-successor.md)由PR #431以
`base=9a0b124a2e9eccc4dc39916062e564fdc9591f28 / head=7485110261ce6cd34178d6dc1e830257b5972530 /
tree=a5be082641241ccbd81eebac5d6f031a07d9484d`精确合入本基线。original Public CI `42383607012`、
exact-main Public CI `42386480443`与Browser Smoke `42386480353`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。

fresh exact-main README/doc379各有唯一`FORMAL_READBACK_PASS`；AGENTS/milestones各有唯一anonymous
raw/Contents API/exact-Git全字节一致观察。README diagnostic #1因reader-visible marker含Markdown标点而得到0 occurrence，按
`DIAGNOSTIC_ONLY_NON_QUALIFYING`保留；v3 adapter只修正proof marker，没有修改产品或oracle。independent reconciliation、
134-artifact finite closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
654c26b1bf039698e43390d53fb68ccff074a6ff182b6a54d290297d84103dd0
976d38d58513b738d28d8bd435d9a7652ca0b0c07b1a5db67ca709f03b5cfe97
759558ebefe9acee80cbf15b831453cf3979f5b6d0ce596455a5b24baeb29c50
f35e141a21730b5665512b4d2fa79f6d6d308bfb1482f3073ca6e4cc4f9568ca
```

因此doc379是`CURRENT_STATE_AUDITED_SUCCESSOR / QUALIFIED_HISTORY`；doc378保持
`READBACK_TARGET_CORRECTION_AUDITED / QUALIFIED_HISTORY`；doc377继续是
`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_QUALIFIED_HISTORY`。后继PASS不回填旧失败。

doc379证明五类post-terminal route与两类private downstream result分别成立，但没有第三个runtime authority把它们签发为共同
application output。这个缺口是`UNPROVED_SEAM_NOT_CONTRADICTION`。fresh CONTROL LOOP只授权本文这个docs-only contract；
没有授权runtime。

## 2. 原工程问题、当前证明义务与适用世界

原工程问题保持为：

```text
为Review/Coverage normal与negative结果建立同一个application-level
可判别、one-shot、authority-preserving output admission边界。
```

本文当前证明义务是冻结这个边界的最小语义合同，而不是证明runtime已经实现，也不是重新证明doc379。

```text
original engineering problem != current contract proof obligation
current contract proof obligation != runtime implementation
runtime implementation != qualified or frozen state
same bytes or digest != same live attempt authority
proof_is_not_problem_solving = true
```

适用世界只包含本exact source、已经冻结的post-terminal selector与两类downstream private result，以及本文自己的
Python 3.10.6/3.13.13 × normal/`-O`和完整后继资格链。任何其他语言、public Review、持久化、manifest或Evidence world均不在
本文适用范围内。

## 3. 本合同解决的问题

当前normal与negative path分别能够产生：

```text
RELATION_HANDOFF / NORMAL_FULFILLED
    -> OwnedReviewSliceCoverageComposition

FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2 / four negative branches
    -> AdmittedNegativeWorldCoverage
```

两类result都绑定original inputs与live `BudgetContext`，但各自只签发局部authority。application若只根据Python union、
`review_slice_set` presence、CoverageLedger shape、display function或相同digest接受结果，会丢失selector route、terminal branch与
same-attempt object graph。

本文冻结一个新的private admission owner。它先绑定一个已由frozen selector签发的exact route claim，再把同一claim交给既有
downstream，最后只接受与该claim、original Fact attempt和live context逐项一致的exact nominal result。它不重新选择route，不修改
downstream result，也不把两个result合并成public union carrier。

## 4. versioned normative identities

本合同冻结以下semantic identities：

```text
contract function
    r1-application-level-unified-review-coverage-output-admission/0.1

private admission domain
    APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_0_1

route/result binding function
    r1-application-level-review-coverage-route-result-binding/0.1

application reconciliation function
    r1-application-level-review-coverage-output-reconciliation/0.1
```

这些identity不预先选择最终Python module、class、field或wire shape，也不创建public Schema。closest-version fallback、string alias、
duck typing或把旧result重新包装成本文domain都必须拒绝。未来若改变route partition、result nominal type、binding denominator或
authority ceiling，必须显式version bump；不能静默修改0.1。

## 5. private authority topology

规范拓扑为：

```text
complete Fact terminal closure
    -> frozen post-terminal selector
    -> exact one-shot route claim
    -> application-owned output-admission attempt binds that exact claim
    -> the same claim enters its already-frozen downstream
    -> exact nominal downstream result
    -> independent route/result/original-world reconciliation
    -> one private admitted application output
```

| owner | 可以决定 | 不得决定 |
| --- | --- | --- |
| Fact owner | complete terminal source、history、branch与original attempt | application output admission |
| post-terminal selector | 五分支中的唯一route与one-shot route claim | downstream result是否合格 |
| positive composition | normal world中的ReviewSlice/Coverage private result | negative classification或共同output admission |
| negative recovery | 四类negative world中的Coverage private result | normal classification或共同output admission |
| application admission owner | exact route claim与exact downstream result是否属于同一live world | 改写Fact truth、缩小denominator或产生Core Verdict |
| digest/content holder | immutable bytes与digest | object identity、attempt、BudgetContext、one-shot或admission authority |

application owner必须在downstream消费以前绑定exact route claim；不能在结果产生后只靠结果字段反推一个claim。绑定不得复制或序列化
claim，不得产生第二个selector slot，也不得从失败path fallback到另一route。

## 6. exact route/result partition

| terminal branch | frozen selector route | 唯一可接受result nominal type | ReviewSlice state |
| --- | --- | --- | --- |
| `NORMAL_FULFILLED` | `RELATION_HANDOFF` | exact `OwnedReviewSliceCoverageComposition` | present或qualified unknown |
| `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` | `QUALIFIED_ABSENT` |
| `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` | `QUALIFIED_ABSENT` |
| `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` | `QUALIFIED_ABSENT` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` | `QUALIFIED_ABSENT` |

normal route只接受exact `ClaimedPostTerminalRelationSource`沿既有Fact → Relation → Slice/Coverage chain产生的result；negative route
只接受exact `ClaimedFactToCoverageExactInputHandoff`沿既有negative recovery chain产生的result。subclass、proxy、copy-equal、
序列化重建、另一attempt的同字节对象或另一route的result全部拒绝。

route discriminant只来自selector签发的terminal identity。特别是normal Relation-conflict允许
`review_slice_set = null`且仍是normal-route qualified unknown；Slice缺失、Coverage overall或artifact shape都不能把它改写成negative。

## 7. same-attempt binding denominator

一次成功admission必须机械绑定并持续重验：

```text
exact route-claim object and selector claim_id
exact route, terminal branch and complete terminal-source canonical bytes
original Fact closure / attempt / eligibility identity
original DerivationInputSet object, canonical bytes and five frozen digests
same live BudgetContext object, deadline, stop state and checkpoint
exact downstream result object and nominal type
route-specific source / bridge / admission identity
exact CoverageLedger bytes, root chain and coverage_ledger_digest
normal composition_digest or negative admitted candidate identity
contract/domain/binding/reconciliation semantic versions
```

application reconciliation不能只比较result自己声明的`route`、digest或authority ceiling。它必须从original terminal source独立重演
五分支mapping，调用并约束既有route-specific validator，再核对result object graph、Coverage root chain与live context。共同使用
canonicalization、immutable source或frozen validator不等于独立性；必须显式列出共同信任根与common-mode failure surface。

## 8. one-shot state machine 与失败后状态

每个application attempt只允许：

```text
ROUTE_BOUND_NOT_ADMITTED
    -> ADMITTED_NORMAL | ADMITTED_NEGATIVE

any invalid transition
    -> REVOKED
```

必须满足：

1. route claim只能绑定一次并只交给其合法downstream；
2. exact result只能提交一次；第一次提交无论成功或失败都消费application admission机会；
3. 成功以后同result replay、另一result、另一route或第二个wrapper全部拒绝；
4. 失败以后不能用copy、equal bytes、new attempt wrapper或fallback route恢复authority；
5. 并发提交最多一个线程到达terminal state；其他线程拒绝；
6. late stop、deadline、context revoke、input/result/ledger mutation或cleanup不完整都使attempt永久`REVOKED`；
7. admitted object的每个读取继续重验exact result、context、route binding与terminal state；
8. shallow/deep copy、pickle/JSON serialization与public carrier conversion全部拒绝。

application admission失败表示没有共同output authority；它不是合法的产品`UNKNOWN`，也不允许UI把局部result显示成已admitted输出。

## 9. admitted private output 的判别与接口上限

成功结果必须是不可构造、不可复制、不可序列化的private admitted object，并显式携带只读判别：

```text
terminal_branch
selector_route
result_kind = NORMAL_REVIEW_SLICE_COVERAGE | NEGATIVE_WORLD_COVERAGE
exact original result object identity
application admission semantic identity
```

normal accessor只在normal variant返回原exact `OwnedReviewSliceCoverageComposition`；negative accessor只在negative variant返回原exact
`AdmittedNegativeWorldCoverage`。wrong accessor必须fail closed。不得提供同时暴露两种live result、允许调用者自行选择variant的union
carrier。内部canonical admission document若为机械证明所需，只能是private proof bytes，不获得public Schema、Artifact、manifest或
persistence身份。

## 10. authority ceiling 与明确defer

后继qualified implementation最多可以签发：

```text
private_application_output_admission = true
route_discriminant                   = exact / one shot
normal_private_result                = conditional / normal only
negative_private_result              = conditional / negative only
fact_truth                           = unchanged
selector_route                       = unchanged
review_slice_semantics               = unchanged
coverage_ledger_semantics            = unchanged
global_public_composition            = false
manifest                             = false
derivation_evidence                  = false
persistence                          = false
public_review                        = false
core_verdict                         = false
R2_R6                                = false
```

这里的`private_application_output_admission = true`只描述未来实现完整资格链闭合后的有限target，不是本文candidate的当前事实。本文
candidate、未来implementation candidate与freeze publication必须继续区分content、execution、qualification、effective state与next-step
authorization。

共同output admission不会补齐same-attempt DerivationEvidence continuity。Evidence必须另行证明同一attempt的Derivation input、Fact、
Relation、Slice、Coverage与application admission连续性；不得从本文result wrapper、digest或private proof bytes自动生成Evidence。

## 11. typed failure families

后继implementation至少必须区分：

```text
UNIFIED_OUTPUT_INPUT_REJECTED
UNIFIED_OUTPUT_ROUTE_REJECTED
UNIFIED_OUTPUT_RESULT_TYPE_REJECTED
UNIFIED_OUTPUT_SAME_ATTEMPT_REJECTED
UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
UNIFIED_OUTPUT_LEDGER_RECONCILIATION_REJECTED
UNIFIED_OUTPUT_ALREADY_ADMITTED
UNIFIED_OUTPUT_CONTEXT_REVOKED
UNIFIED_OUTPUT_AUTHORITY_CEILING_REJECTED
```

这些是private application failure families，不修改既有Fact/Relation/Slice/Coverage reason enum，不变成Core Verdict，也不把一个
admission proof failure解释成Reality中的缺陷。

## 12. normative falsifier matrix

| ID | falsifier | required result |
| --- | --- | --- |
| `UAO-000` | complete normal route + exact positive result | exactly one `ADMITTED_NORMAL` |
| `UAO-001` | 任一四类negative route + exact negative result | exactly one `ADMITTED_NEGATIVE` |
| `UAO-002` | normal route提交negative nominal result | reject并永久revoke |
| `UAO-003` | negative route提交positive nominal result | reject并永久revoke |
| `UAO-004` | subclass/proxy/equal-copy result | exact nominal identity reject |
| `UAO-005` | foreign selector claim或foreign Fact attempt result | same-attempt reject |
| `UAO-006` | equal terminal bytes但不同closure/inputs/context object | object-graph reject |
| `UAO-007` | route claim/result的branch或claim_id不一致 | route/result binding reject |
| `UAO-008` | CoverageLedger替换为另一attempt的equal-shape ledger | ledger reconciliation reject |
| `UAO-009` | normal composition的bridge/source identity被替换 | positive chain reject |
| `UAO-010` | negative admission的attempt/validation/candidate identity被替换 | negative chain reject |
| `UAO-011` | normal Relation-conflict且`review_slice_set = null` | 仍为normal；不得重分类negative |
| `UAO-012` | 成功后同result replay | second admission reject |
| `UAO-013` | 失败后换result或route fallback | no recovered authority |
| `UAO-014` | 并发两次admission | 最多一个terminal admission |
| `UAO-015` | late stop/deadline/context revoke/cleanup incomplete | no admission |
| `UAO-016` | result/ledger/input在绑定后mutation | reject并revoke |
| `UAO-017` | 序列化、copy或public union carrier恢复 | construction/admission reject |
| `UAO-018` | admitted object声明manifest/Evidence/persistence/public Review/Core Verdict | authority ceiling reject |
| `UAO-019` | 同一semantic report来自另一SHA/tree/attempt | qualification inheritance reject |
| `UAO-020` | 所有矩阵PASS但原工程问题或适用world已漂移 | stop；不得以形式PASS替代问题解决 |

后继feasibility与implementation必须在Python 3.10/3.13 × normal/`-O`比较canonical semantic report，并保留全部FAIL、ERROR、
CANCELLED、setup failure与UNKNOWN。finite matrix只是witness；contract、live object binding与完整qualification pipeline拥有authority。

## 13. UNKNOWN、UNSAT 与证明上限

若后继feasibility不能构造满足本文的private admission，只能记录`UNKNOWN / NO_QUALIFIED_CONSTRUCTION`。有限candidate全部失败不等于
整个空间UNSAT；只有穷尽本文明确且完整的bounded candidate space并提供机械不可满足性证明，才可声明`UNSAT`。

即使所有falsifier通过，也只证明声明world中的候选没有被这些反例击穿。它不证明用户最初工程问题已完整解决，不证明多语言、
public Review、真实缺陷检测收益或人类审查效率，也不证明Evidence continuity。任何新事实改变原问题、proof obligation或applicability
world时必须停止并回到CONTROL LOOP。

## 14. exact scope 与frozen-byte stop

本docs-only candidate只允许：

```text
README.md
AGENTS.md
docs/380-r1-application-level-unified-review-coverage-output-admission-contract.md
docs/milestones.md
```

doc377–379、`docs/project-state.md`、runtime、tests、fixtures、workflows、Schema、Provider、Collector、P2/Core oracle、Verdict与所有
frozen semantic bytes必须保持base bytes。尤其不得借本合同修改selector、positive composition或negative recovery实现。

## 15. candidate qualification 与fresh readback责任

final bytes至少完成exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、unique marker、doc379 qualification与
upstream frozen-byte continuity、`git diff --check`、read-only global/local hygiene及声明的四格semantic/focused witness。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent Core / source-byte / identity / retained-history reconciliation
    -> qualified contract candidate / not frozen
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP for private implementation feasibility
```

README/本文各运行唯一Render diagnostic+formal；AGENTS/milestones各运行唯一anonymous raw+Contents API+exact Git全字节对账。
不得把已知超过Render window的完整milestones重新注册为Render target。所有产品调用必须清除GitHub token、`NO_PROXY`、
`PYTHONPATH`与`PYTHONHOME`，只按命令使用`http://127.0.0.1:7897`。任何non-success保留原identity，不得rerun洗白或拼接world。

## 16. 当前状态、target ceiling 与下一步

当前只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CURRENT_STATE_AUDIT_MERGED_READBACK_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_AUDIT_READBACK_TARGET_CORRECTION_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CURRENT_STATE_AUDIT_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合后，最多成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。随后必须返回CONTROL LOOP，建立独立
docs-only freeze publication；其最后门闭合前`CONTRACT_FROZEN`不生效，private implementation feasibility/runtime仍未授权。

本文没有把形式证明替代问题解决：合同只固定将来必须证明什么、由谁证明以及证明在哪个world成立；它本身不证明共同output已经存在。
