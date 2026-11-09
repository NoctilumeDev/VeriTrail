# R1 same-attempt DerivationEvidence continuity最小合同 0.1

日期：2026-11-10

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@a1d1ff8eac47506d25a65eae9c8b00a2ba89c3b1`，tree
> `15ba0f333d75462aaf246e229810ff3872860271`。
>
> 影响：`L3_SYSTEM_DESIGN + L2_CONTRACT + L0_DOCUMENTATION`。本文只冻结versioned private continuity owner、原执行期
> controller capture、五分支same-attempt binding与fail-closed lifecycle；不实现runtime，不创建或修改public Schema、Artifact、
> manifest、persistence、CLI、Workbench、Provider、Collector、Core Verdict、public Review或R2–R6 authority。

## 1. CONTROL LOOP 与qualified起点

[feasibility recovery audit](396-r1-same-attempt-derivation-evidence-continuity-feasibility-recovery.md)由PR #455以
`base=831c7646c324427d8b582ee6320efa6737406fa2 / head=47677502f338401105bacd49ff3ca62177b6228e /
tree=15ba0f333d75462aaf246e229810ff3872860271 / 1 commit / 4 docs files`精确合入本构造坐标。original Public CI
`42700099718`、exact-main Public CI `42706462980`与Browser Smoke `42706462959`均为attempt 1 SUCCESS，分别为11/11、
11/11与1/1，没有rerun。

fresh exact-main README/doc395/doc396各自完成唯一`FORMAL_READBACK_PASS`；AGENTS/milestones各自完成anonymous raw、Contents API与
exact Git全字节一致观察。independent reconciliation、152-artifact finite closeout与finite integrity SHA-256为：

```text
2a16256a3a5ef293d62228d78ac174682548a77bdc6786b69867ef7e3ce24a31
6460e4922121866ab3689054a3cb0d725e45b47f4dac28fef4f7b107cb9ef925
d8a6ba042cc0c2a24be77a5aa5611fa556a5a5fb6592279e7669db44498bbc7e
```

所以doc396是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。PR #453仍保持closed、unmerged、original Public CI failed、
not-qualified；其缺失的两个job/check-run identity与lower cause `UNKNOWN`不被本合同解释或回填。fresh CONTROL LOOP重新读取exact-main
AGENTS、working method、hygiene、remote main、open PR与primary audit，只授权本文这个独立docs-only contract；没有授权runtime。

## 2. 原工程问题、合同义务与适用世界

原工程问题保持为：

```text
normal corrected route与四个qualified negative Coverage route
在同一原始attempt内形成可复核的
input -> Fact -> Relation/negative branch -> Slice/Coverage -> final admission连续证据。
```

本文只冻结未来实现必须满足的合同，不证明Evidence已经存在：

```text
original engineering problem != contract proof obligation
contract content                != contract qualification
qualified contract candidate   != frozen contract
frozen contract                != implementation authorization
implementation                 != global composition proof
proof_is_not_problem_solving   = true
local_not_global               = true
post_r1_global_check_required  = true
```

适用世界严格是本exact source、projection 0.8 frozen、qualified doc395/doc396 history、frozen Fact/Relation/Slice/Coverage与private
unified output admission，以及Python 3.10.6/3.13.13 normal/`-O`的后继witness。语言外推、public Review、持久化、manifest、发布和
R2–R6均不属于本合同。

## 3. versioned normative identities

本文冻结以下private semantic identities：

```text
contract function
    r1-same-attempt-derivation-evidence-continuity/0.1

private continuity domain
    SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1

controller capture function
    r1-derivation-evidence-controller-capture/0.1

branch projection function
    r1-derivation-evidence-continuity-branch-projection/0.1

independent reconciliation function
    r1-derivation-evidence-continuity-reconciliation/0.1
```

这些identity不预先选择最终Python module、class、field或wire shape，也不创建public Artifact kind或Schema resource。closest-version
fallback、string alias、duck typing、subclass、legacy wrapper或把相同digest当成同一live owner都必须拒绝。未来若改变branch partition、
capture denominator、timing authority、binding denominator或authority ceiling，必须显式version bump，不能静默修改0.1。

## 4. legacy Evidence 0.2 immutable 与non-alias rule

`schemas/review-derivation-evidence-0.2.schema.json`及其既有projector继续逐字节冻结。legacy 0.2的`COMPLETED`必须含
`relation_admission`；非成功状态必须令admission为null并清空reported Fact/Relation IDs。它只能消费exact legacy
`OwnedRelationSetAdmissionState`。

本合同的五个qualified application outputs不能被压回该shape：

- normal corrected route使用新的Fact→Relation transition、Relation→Slice bridge、Coverage composition与private unified admission；
- 四个negative routes有qualified Coverage result但没有FactSet/RelationSet，它们不是`FAILED`或`UNAVAILABLE`；
- 把negative写成legacy non-success会改写已资格化业务状态；把它写成legacy `COMPLETED`会虚构Relation admission；
- 把normal successor交给legacy projector会把两个authority path冒充为同一个。

因此未来private continuity value不得自称legacy `DERIVATION_EVIDENCE 0.2`，不得传给legacy projector，也不得让旧consumer按fallback接收。
若未来需要public Artifact/Schema，必须另开versioned Schema与publication合同；本文不预先授予该权力。

## 5. authority topology 与唯一owner

规范拓扑为：

```text
original DerivationInputSet + one live BudgetContext
    -> admitted Fact attempt and controller-owned capture slot
    -> complete terminal Fact source
    -> frozen post-terminal selector exact one-shot claim
    -> normal corrected transition OR qualified negative Coverage path
    -> exact application-level unified output admission
    -> independent continuity reconciliation
    -> one private committed continuity value
```

| owner | 可以决定 | 不得决定 |
| --- | --- | --- |
| Reality / Provider | 自己实际观察到的源码事实与来源 | controller时间、application admission、Core Verdict |
| Fact controller | attempt/run/phase时钟观察、terminal mapping、Fact phase owned result | Relation/Slice/Coverage truth |
| Relation controller | normal route的run/phase时钟观察与terminal mapping | negative branch或最终admission |
| selector | complete Fact terminal source的唯一route claim | downstream result是否合格 |
| route-specific downstream | 自己合同内的normal composition或negative Coverage result | 共同Evidence continuity |
| unified output admission | exact route/result是否属于同一live world | 重写Fact/Relation/Coverage truth |
| continuity owner | copy-own各owner已签发material并机械证明same-attempt连续性 | 新观察事实、缩小denominator、产生Verdict或Seal |
| digest/content holder | immutable bytes与digest | object identity、attempt、clock、one-shot或admission authority |

continuity owner必须在原Fact attempt被admit时取得唯一capture slot，并沿同一live object graph推进；不得在最终结果产生后事后收集日志、
路径、Provider state或clock来“拼回”连续性。continuity owner是证明装配者，不是现实事实超级owner。

continuity commit只证明本合同范围内的证据连续性，不宣布证据已经充分，更不产生`PASS`。业务层可以选择能力、安排顺序、并行采集或
请求补充条件，但不能改变sealed acceptance obligation；Core只能依据sealed合同裁决binding、integrity、sufficiency与determinacy，
也不能反向取得Provider观察到的现实事实authority。

## 6. 原执行期capture protocol

### 6.1 common capture

每个合法attempt必须在原执行期间copy-own：

1. exact `DerivationInputSet` object、canonical bytes、五个冻结digest与request provenance；
2. same live `BudgetContext` object、absolute monotonic deadline、stop/eligibility state与cleanup outcome；
3. Fact controller承认的attempt start、每个applicable ProviderRun start/finish、Fact phase finish与terminal classification；
4. complete terminal Fact source、Fact branch、whole-attempt closure、provider history与exact selector claim；
5. exact downstream result与application-level unified output admission identity；
6. final continuity reconciliation finish observation。

所有UTC时间只作provenance；deadline/remaining判断只使用原BudgetContext的monotonic时钟。controller时间不得由Provider、worker、文件mtime、
日志行、Git时间或serialization时间替代，也不得在attempt结束后补测。

### 6.2 normal-only capture

`NORMAL_FULFILLED / RELATION_HANDOFF`还必须在one-shot continuation消费前copy-own完整transition admission，并在原执行期间捕获：

```text
Fact phase finished_at
    <= each applicable Relation ProviderRun started_at
    <= corresponding ProviderRun finished_at
    <= Relation phase finished_at
    <= Slice/Coverage composition commit
    <= unified output admission commit
    <= continuity reconciliation finished_at
```

normal owner还必须绑定FactSet、RelationSet、provider lineage、transition admission、Relation→Slice bridge、ReviewSliceSet disposition、
CoverageLedger ordered root chain、composition identity与exact unified output result。Relation conflict允许`review_slice_set = null`且仍是normal
qualified unknown；不得因Slice absence重分类为negative。

### 6.3 negative-only capture

四个negative branches只允许：

```text
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

它们必须绑定complete terminal Fact source、exact-input handoff successor、negative Coverage candidate、独立validation、admission、
CoverageLedger qualified-absence root chain与unified output result。不存在的FactSet/RelationSet/ReviewSliceSet必须记录为branch-governed
qualified absence，不能制造placeholder。没有启动的Provider/phase明确为`NOT_STARTED / no timing`；实际启动后non-success的Provider则必须
保留controller-owned start/finish/status。`NOT_STARTED`与missing capture不是同义词。

## 7. exact same-attempt binding denominator

一次成功continuity commit必须机械绑定并持续重验：

```text
exact continuity-owner object and semantic version
exact derivation_id / attempt identity / selector claim_id
exact original DerivationInputSet object, canonical bytes and five frozen digests
same live BudgetContext object, deadline, stop, eligibility and cleanup outcome
Fact attempt / provider / phase controller timing and terminal source
exact terminal branch, selector route and one-shot claim object
normal transition/Relation lineage/timing OR negative exact-input/admission lineage
exact nominal downstream result object and route-specific admission identity
exact CoverageLedger bytes, ordered root bindings, root-chain digest and ledger digest
exact application-level unified output admission object, route/result binding and authority ceiling
contract/capture/branch/reconciliation semantic versions
```

相同bytes、相同digest、相同`derivation_id`字符串、相同clock值或相同serialized document都不能替代exact live object graph。reconciliation必须从
terminal Fact source独立重演五分支mapping、调用route-specific frozen validator、核对Coverage root chain，并证明final admission消费的正是
同一claim与result。共同canonicalization或validator必须列为common-mode trust root，不能被写成独立事实来源。

## 8. private continuity value 与branch model

未来成功结果必须是不可公开构造、不可复制、不可pickle/JSON恢复的private value，并显式判别：

```text
NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY
NEGATIVE_WORLD_COVERAGE_CONTINUITY
```

normal accessor只返回原exact positive composition与其transition lineage；negative accessor只返回原exact admitted negative Coverage与其
qualified-absence lineage。wrong accessor必须fail closed。不得提供让caller自行选择variant的union carrier，也不得把private proof bytes
授予Artifact、Schema、manifest、persistence或public API身份。

private value不得重新计算或替代Fact/Relation/Slice/Coverage canonical identity。runtime时钟与continuity semantic version不得污染
provenance-free Fact/Relation content identity；它们只属于attempt/Evidence continuity provenance。

## 9. one-shot lifecycle 与不可恢复失败

每个capture slot只允许：

```text
PROVISIONAL
    -> CAPTURING_FACT
    -> FACT_CLOSED
    -> CAPTURING_NORMAL | CAPTURING_NEGATIVE
    -> OUTPUT_ADMITTED
    -> COMMITTED

any invalid transition -> REVOKED
REVOKED -> no transition back
```

必须满足：

1. capture slot只能在exact Fact attempt admission时创建一次；pre-admission failure没有continuity value；
2. 每个controller observation只能提交一次，且提交后copy-owned；
3. selector claim只绑定一次，并只进入合法branch；
4. normal transition必须在continuation消费前捕获；late capture永久revoke；
5. 第一次final result提交无论成功或失败都消费commit机会；
6. 成功后replay、第二result、第二wrapper或另一branch全部拒绝；
7. 失败后不能用copy、equal bytes、new clock、new slot或fallback route恢复authority；
8. stop/deadline/context revoke、missing capture、mutation、cleanup incomplete或controller exception都永久revoke；
9. 并发提交最多一个线程到达`COMMITTED`，其他全部拒绝；
10. retry必须使用新的derivation attempt、inputs binding、BudgetContext与capture slot，不能复用partial state。

continuity proof failure表示没有same-attempt continuity authority；它不是Reality缺陷、产品`UNKNOWN`、Provider failure或Core Verdict。

## 10. complete/disjoint five-route mapping

| Fact terminal branch | selector route | required downstream | continuity variant |
| --- | --- | --- | --- |
| `NORMAL_FULFILLED` | `RELATION_HANDOFF` | exact `OwnedReviewSliceCoverageComposition` + unified normal admission | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` + unified negative admission | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` + unified negative admission | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` + unified negative admission | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | exact `AdmittedNegativeWorldCoverage` + unified negative admission | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |

五分支必须complete/disjoint。unknown branch、branch/route mismatch、wrong nominal type、foreign admission或任何fallback都直接revoke；不得把
unknown branch塞进negative catch-all。

## 11. typed failure families

后继implementation至少必须区分：

```text
EVIDENCE_CONTINUITY_INPUT_REJECTED
EVIDENCE_CONTINUITY_CAPTURE_ORDER_REJECTED
EVIDENCE_CONTINUITY_CONTROLLER_TIMING_MISSING
EVIDENCE_CONTINUITY_CONTROLLER_TIMING_REJECTED
EVIDENCE_CONTINUITY_BRANCH_REJECTED
EVIDENCE_CONTINUITY_TRANSITION_CAPTURE_REJECTED
EVIDENCE_CONTINUITY_SAME_ATTEMPT_REJECTED
EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
EVIDENCE_CONTINUITY_LEDGER_RECONCILIATION_REJECTED
EVIDENCE_CONTINUITY_LEGACY_ALIAS_REJECTED
EVIDENCE_CONTINUITY_ALREADY_COMMITTED
EVIDENCE_CONTINUITY_CONTEXT_REVOKED
EVIDENCE_CONTINUITY_AUTHORITY_CEILING_REJECTED
```

这些是private proof failure families，不修改既有public diagnostic enum，不归因到Reality、Provider或用户，不产生Verdict，也不把
proof-facility error重命名为product failure。底层原因无法由正向观察确定时保持`UNKNOWN`。

## 12. normative falsifier matrix

| ID | falsifier | required result |
| --- | --- | --- |
| `DEC-000` | complete normal world + exact captures + exact unified admission | exactly one normal continuity commit |
| `DEC-001` | 任一四类negative world + exact captures + exact unified admission | exactly one negative continuity commit |
| `DEC-002` | equal input bytes/digests但foreign attempt/context object | same-attempt reject |
| `DEC-003` | same `derivation_id`字符串但different admitted attempt | attempt identity reject |
| `DEC-004` | Provider/worker自报controller timing | timing authority reject |
| `DEC-005` | attempt结束后从clock/log/path补写timing | late capture reject并revoke |
| `DEC-006` | missing Fact ProviderRun start/finish或phase finish | no commit |
| `DEC-007` | normal route缺完整transition admission | no commit |
| `DEC-008` | normal transition在one-shot continuation消费后才捕获 | no recovered authority |
| `DEC-009` | normal Relation lineage缺run/phase finish | no commit |
| `DEC-010` | negative `NOT_STARTED` Provider被赋予fabricated timing | reject |
| `DEC-011` | actually started negative Provider缺controller timing | reject |
| `DEC-012` | negative branch伪造FactSet/RelationSet/ReviewSliceSet placeholder | reject |
| `DEC-013` | normal Relation-conflict且Slice null | 保持normal qualified unknown，不得重分类negative |
| `DEC-014` | normal route提交negative result或反向 | branch/result reject |
| `DEC-015` | unknown terminal branch进入negative catch-all | reject并revoke |
| `DEC-016` | equal CoverageLedger bytes来自foreign attempt | ledger/object-graph reject |
| `DEC-017` | selector claim/result/final admission任一属于foreign route或attempt | binding reject |
| `DEC-018` | legacy `OwnedRelationSetAdmissionState` wrapper或projector alias | legacy alias reject |
| `DEC-019` | negative qualified output重写为`FAILED/UNAVAILABLE` | semantic rewrite reject |
| `DEC-020` | private value声明legacy/public Evidence Artifact或Schema identity | authority ceiling reject |
| `DEC-021` | stop/deadline/context revoke在commit前赢得 | no commit |
| `DEC-022` | cleanup incomplete或release failure | no commit；cause不伪造 |
| `DEC-023` | capture/result/input/ledger绑定后mutation | reject并永久revoke |
| `DEC-024` | 同一result replay或第二wrapper | second commit reject |
| `DEC-025` | 两线程竞争final commit | 最多一个commit |
| `DEC-026` | copy/pickle/JSON/duck type恢复private continuity | construction/use reject |
| `DEC-027` | private value声明manifest/persistence/public Review/Core Verdict | authority ceiling reject |
| `DEC-028` | 同semantic report来自另一SHA/tree/attempt | qualification inheritance reject |
| `DEC-029` | 所有局部矩阵PASS但原问题或适用world漂移 | stop并返回CONTROL LOOP |

后继feasibility与implementation必须在Python 3.10.6/3.13.13 × normal/`-O`比较canonical semantic report，并保留全部FAIL、ERROR、
CANCELLED、setup failure与UNKNOWN。有限矩阵只作witness；exact owner、live binding和完整qualification pipeline拥有authority。

## 13. authority ceiling 与明确defer

后继qualified implementation的最高上限也只能是：

```text
private_same_attempt_continuity = true
normal_or_negative_branch       = exact / discriminated / one shot
controller_timing_provenance    = original execution only
fact/relation/slice/coverage     = unchanged
legacy Evidence 0.2             = unchanged / non-alias
public Evidence Schema          = false
manifest                        = false
persistence                     = false
public Review                    = false
Core Verdict                     = false
global composition authority     = false
R2_R6                           = false
```

本文不选择public wire version、Artifact cardinality、Manifest role/path、publisher、storage、retention或Release identity。也不自动恢复
[manifest successor合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)的implementation authority；Evidence
continuity未来即使frozen，仍必须返回CONTROL LOOP重新审计manifest的全部前提。

## 14. UNKNOWN、UNSAT 与全局后验义务

若后继feasibility不能构造满足本文的private owner，只能记录`UNKNOWN / NO_QUALIFIED_CONSTRUCTION`。有限候选全部失败不等于整个空间
UNSAT；只有穷尽本文明确且完整的bounded candidate space并提供机械不可满足性证明，才可声明UNSAT。

即使所有falsifier通过，也只证明声明world中的局部合同或候选没有被这些反例击穿。R1完整闭合后仍必须独立global check：复核阶段间
前提连续性、authority/qualification断点、局部结论可组合性与最终用户能力。该未来义务不扩张本文authority，也不能提前混入当前
contract qualification。

## 15. exact docs-only scope 与frozen-byte stop

本candidate只允许：

```text
README.md
AGENTS.md
docs/397-r1-same-attempt-derivation-evidence-continuity-contract.md
docs/milestones.md
```

`docs/project-state.md`、doc318、doc377–396、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、
Verdict与全部frozen semantic bytes必须保持base bytes。尤其不得借本合同修改legacy Evidence 0.2、Fact/Relation controller、selector、
positive/negative Coverage、unified output admission或manifest topology。

## 16. candidate qualification 与fresh readback责任

final bytes至少完成exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、unique marker、doc396 qualification、
legacy 0.2 immutability、`git diff --check`、read-only global/local hygiene，以及声明的Python 3.10.6/3.13.13 normal/`-O`
semantic/focused witnesses。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc396 / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source-byte / five-route / timing-owner / retained-failure reconciliation
    -> qualified contract candidate / not frozen
    -> return CONTROL LOOP
    -> separate docs-only contract freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN becomes effective
```

README/doc396/本文各运行唯一Render diagnostic+formal；AGENTS/milestones各运行唯一anonymous raw+Contents API+exact Git全字节对账。
所有产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用`http://127.0.0.1:7897`。任何
non-success保留原identity，不得rerun洗白、回填PR #453或拼接different worlds。

## 17. 当前状态、target ceiling 与下一步

当前只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合后，最多成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。随后必须返回CONTROL LOOP并建立独立
docs-only contract freeze publication；该publication最后门闭合前`CONTRACT_FROZEN`不生效，private implementation feasibility与runtime
仍未授权。本文没有把合同形式正确当成工程问题已解决，也没有把局部正确冒充全局正确。
