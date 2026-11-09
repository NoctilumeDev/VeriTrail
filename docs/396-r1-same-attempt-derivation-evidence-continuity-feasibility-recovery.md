# R1 same-attempt DerivationEvidence continuity feasibility recovery audit

日期：2026-11-10

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@831c7646c324427d8b582ee6320efa6737406fa2`，tree
> `9e69965b89348fb674b0c7ae6fd4193f336e66f4`。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文从已资格化的original-gate failure boundary之后重新运行source audit与
> unchanged-runtime witnesses；不继承PR #453的commit、attempt或资格，不解释其`UNKNOWN` lower cause，不创建Evidence runtime、
> Schema、manifest、persistence、public Review、Core Verdict或R2–R6 authority。

## 1. CONTROL LOOP 与恢复起点

[projection 0.8 freeze publication](393-r1-public-project-state-projection-0.8-freeze-publication.md)已经在
`main@03f3f03b6ad116ccf345041cec6ba393a385cd62`完成original/exact-main双门、fresh installed-product readback、raw-byte
observation、independent reconciliation与finite closeout。因此：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
```

后继PR #453绑定`base=03f3f03… / head=948ba1d… / tree=af62c70… / 1 commit / 4 docs files`，其local semantic、focused
与hygiene witnesses成立，但original Public CI `42666764972` attempt 1为`FAILURE`。该run仅实例化9个job且均SUCCESS；
`Acceptance Core freeze on Python 3.10`与`Starter PASS/FAIL golden path`没有形成job/check-run identity。PR #453已经关闭、
未合并、未rerun；candidate regression、Subject failure与product assertion failure均未建立，lower cause保持`UNKNOWN`。

[original-gate failure boundary](395-r1-same-attempt-derivation-evidence-continuity-audit-original-gate-failure-boundary.md)
随后由PR #454精确合入当前`main@831c7646c324427d8b582ee6320efa6737406fa2`。original Public CI `42674693508`、
exact-main Public CI `42679344349`与Browser Smoke `42679344175`均attempt 1 SUCCESS（11/11、11/11、1/1）。fresh
README/doc395 formal、AGENTS/milestones raw-byte observation、independent reconciliation与finite closeout全部成立；关键SHA-256为：

```text
independent reconciliation
0be09400219a67e84462b83741c900cbee11a2f6b7fc3553806d2a7385ffbed4

110-artifact finite closeout
1de468b24b2690bdeaa9bb9f19fff6cf98d71f872da7995864521d7d2afb2e2b

expected stdout self-capture mismatch
b09eff64923c506f93b4a87fe7721da139419d39320d9620287a57624ccbb4c3

finite integrity
670ff0253ffe5b196e9962691b7335f04acc22396cf37e4a7e0aa9ab7863d281
```

README diagnostic的过长plan ID proof-facility failure、anonymous rate exhaustion及全部setup failures继续按原identity保留。后继PASS
没有覆盖它们。doc395现在只作为：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
```

被消费；它不资格化doc394或PR #453。fresh CONTROL LOOP重新读取current exact-main AGENTS、working method、hygiene、remote main、
open PR与primary audit，确认最小恢复责任只是从新exact main独立重建docs-only feasibility audit。

## 2. 原工程问题、证明义务与适用世界

三个身份继续机械分离：

```text
original engineering problem
    让normal corrected route与四个qualified negative Coverage route都能在同一原始attempt内
    形成可复核的input -> Fact -> Relation/negative branch -> Slice/Coverage -> final admission连续证据

current proof obligation
    在doc395 qualified failure boundary之后，从exact main 831c764/tree 9e69965独立重建docs-only feasibility audit；
    不继承PR #453资格，不解释其UNKNOWN lower cause，不把feasibility写成implementation或工程问题已解决

applicability world
    exact main 831c764/tree 9e69965 + projection 0.8 frozen + doc395 qualified history
    + frozen output admission + normal corrected route
    + ZERO_PARSE_DENOMINATOR / ALL_PARSE_REJECTED / PROJECTION_BLOCKED /
      REQUIRED_PROVIDER_NON_SUCCESS四条qualified negative route
    + CPython 3.10.6/3.13.13 normal/-O

proof_is_not_problem_solving = true
local_not_global = true
post_r1_global_check_required = true
```

本轮局部审计即使完整通过，也不能证明R1各阶段前提可以全局组合。R1完成以后必须另开global check，检查阶段间前提连续性、
authority/qualification断点、局部结论的可组合性以及最终用户能力；该未来责任不扩张当前R1施工权。

## 3. 失败世界不被拼接

本恢复候选与PR #453严格分属不同世界：

1. PR #453的base/head/tree、original attempt、9个已实例化job与2个缺失identity保持原样；
2. doc395只证明失败边界分类与恢复责任，不给失败候选补发资格；
3. 本文使用新的exact base/tree、fresh semantic reports、fresh focused logs与自己的后继门；
4. 本文后继PASS不能回填run `42666764972`，也不能把lower cause从`UNKNOWN`改名；
5. PR #453的semantic内容未被反例推翻，不等于它已经资格化。

failure classification与seal SHA-256继续是：

```text
30c7c3512afae63fd4d16ba9c23e542708f5e2c3790cc74b22d22fa5378b5ae2
052373a1b96764a1789e10f855db3e68954dc00ae1ca4b3285ef9f367ac3eccb
```

## 4. Legacy Evidence 0.2表达边界

当前`review-derivation-evidence-0.2.schema.json`只允许`COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE`。其中
`COMPLETED`必须携带非空`relation_admission`；非成功状态必须令`relation_admission = null`并把reported Fact/Relation IDs
约束为空。legacy projector只接受exact `OwnedRelationSetAdmissionState`并固定输出`COMPLETED`。

四个negative route不是FAILED或UNAVAILABLE，而是已经资格化的application outputs：它们没有FactSet/RelationSet，但有
branch-specific CoverageLedger与private unified admission。把它们写成legacy non-success会改写事实；写成legacy COMPLETED会虚构
Relation admission。因此旧Evidence 0.2不能诚实表达五条qualified outputs，也不得通过alias、duck type或status重分类复用。

## 5. Exact-source current state

exact source已经保留的bounded same-attempt material包括：

1. selector route、original `DerivationInputSet`、live `BudgetContext`与terminal Fact source；
2. normal transition admission中的exact Fact source、FactSet、RelationSet、provider lineage与request provenance；
3. normal final composition中的ReviewSliceSet、CoverageLedger与root chain；
4. 四个negative outputs中的exact branch、terminal Fact source、CoverageLedger与route/result binding；
5. final unified admission中的one-shot route discriminant、result identity与authority ceiling。

但完整final Evidence material尚未被一个owner连续保留：normal composition没有完整transition admission；Product Fact provider history
没有controller-owned wall-clock start/finish；Relation provider lineage缺provider/phase finish wall-clock；final unified output admission明确
保持`derivation_evidence = false`且没有Evidence continuation owner。negative routes没有FactSet/RelationSet则是分支语义，不是待填空洞。

## 6. Bounded versioned successor construction

最小可行construction需要新的private、versioned Evidence continuity owner，并在同一原attempt中依次捕获：

1. terminal Fact source、original `DerivationInputSet`与live `BudgetContext`；
2. Fact controller在原执行期间观察到的attempt/provider/phase wall timings；
3. normal route的transition admission，在one-shot continuation消费前取得；
4. Relation controller在原执行期间观察到的provider/phase finish wall timings；
5. normal Slice/Coverage composition或四个negative route之一的admitted Coverage result；
6. final unified admission identity与exact route/result binding。

owner必须绑定同一个selector claim与original attempt。normal与negative是discriminated branches；copy-equal、same-digest foreign attempt、
replay、wrong route/result、late stop、mutation、缺失capture与第二次提交都必须fail closed。controller-owned timing只能在原执行期间
copy-own，不得在attempt结束后重读clock、Provider、path、log或mutable external state。

## 7. 不需要重开的冻结面

本结论不要求改变Fact、Relation、ReviewSliceSet、CoverageLedger、selector、negative taxonomy、Coverage root binding、reason oracle、
unified admission、legacy Evidence 0.2、public export、manifest、persistence、CLI、Workbench、Provider、Collector、workflow、projection 0.8、
Release资产或primary `audit.json`。后继若需要修改任一项，必须返回CONTROL LOOP并显式重开/version被击穿的最小边界。

## 8. Fresh mechanical audit

fresh source audit从current exact base构造normal corrected route与四个negative routes，核对legacy Schema/projector、transition/material
retention、unified admission ceiling与exact source hashes。Python 3.10.6/3.13.13 × normal/`-O`四格逐字节semantic digest一致：

```text
semantic digest
731dc439dcbb07faba0f7a02423cbaf97bb92345769d3827e561026cab34b71f

audit script SHA-256
3d94c438e739ac7d35fd085e714e21940c7b50980fbaf559114b4d4a8896fca0
```

四个formal report file SHA-256分别为：

```text
802d6b8166b7f34947cbe179e9193057b6b7533c7b47f306676ffe31a677c580
018dc4470e73e7cac9ba3db9e479b8e49a3350aabd10809b7c9035a76e2771ff
7d9a6f94d4c1172b3d2d55fd624e78633553a15a2879e793309cde988d73496a
fece161985593bc952aeb53a1b4172f5cebe04d16597494c56446cbec41f3504
```

fresh focused witness覆盖post-terminal selector、Fact fulfillment、Fact/Relation transition、normal Slice/Coverage composition、四个
negative Coverage routes、unified output admission、Relation admission与legacy Evidence rejection。四格各运行同一组126个非重叠测试，
全部PASS。record/log SHA-256按3.10 normal、3.10 `-O`、3.13 normal、3.13 `-O`顺序为：

```text
d590c6d34ac6ed0968daff984196ab4a02e23d40fea858e735ee10ac4b4bbb9e
332d354ab91b0bb3459649c71c2e2362de7b74dfc953e90dde110b8fe8f0d857
e6a6ee365511fccc0168106a153661387ef801fb3e5393cb6520284808aebd58
d4a6cc1935cfc216a3d23a38dbaecb50983e45c077ed94ac1175c4cb61679646
23d8db1f71516414e5da31a341a766a04c592284b37a2db672398aae85fb24b2
083ac62f1e49305df02b40592fdd5f9697849a2257cdb6784092e1b5be7c9b48
fde48191ba5987b719c1bd2972869bb1f6c6fc24b870000e799fca7513097678
88867cd7525e44d840c2b2d951d8b327a16f013af8aa4315a48b7ee21ebe58f8
```

managed-worktree attachment cap、PowerShell revision parsing与LiteralPath glob errors全部保留为`NON_QUALIFYING / NONE`；它们没有
改变产品、测试、candidate或primary audit bytes。

## 9. Feasibility result 与stop conditions

本candidate的局部结果是：

```text
FEASIBLE_WITH_VERSIONED_PRIVATE_OWNER_AND_BOUNDED_CONTROLLER_CAPTURE_ADDITIONS
current_final_output_directly_retains_full_normal_continuity = false
current_source_retains_complete_final_evidence_material       = false
existing_same_attempt_identity_and_semantic_material_is_bounded = true
legacy_shape_can_represent_all_five_qualified_outputs         = false
versioned_successor_required                                  = true
implementation_present                                        = false
implementation_authorized                                     = false
local_not_global                                             = true
post_r1_global_check_required                                = true
proof_is_not_problem_solving                                  = true
```

如果legacy 0.2必须被重解释、negative Coverage必须被改写成non-success、冻结的Fact/Relation/Slice/Coverage/admission semantics必须
移动、需要post-attempt外部重读、需要public Schema/manifest/persistence，或必须用equal digest拼接different attempts/worlds，则本文
feasibility结论立即停止。

## 10. 后继最小合同责任

只有本文完整资格且fresh CONTROL LOOP没有新反例，后继独立docs-only contract才可冻结：

1. 新private/versioned Evidence identity、owner、branch model与legacy non-alias rule；
2. 六个原执行期capture points及controller ownership；
3. normal与四个negative route的complete/disjoint mapping；
4. original attempt/selector claim/input/context/terminal source/downstream result/final admission双向binding；
5. one-shot claim、copy-owned values、timing责任、late capture拒绝与fail-closed lifecycle；
6. wrong route/result、foreign attempt、same-digest substitution、replay、mutation、missing timing、legacy alias与negative status rewrite的
   direct falsifiers；
7. authority ceiling继续拒绝manifest、persistence、public Review、Core Verdict与R2–R6。

本文不选择successor版本号、wire/Schema格式、manifest cardinality或public release identity。

## 11. Authority ceiling 与全局后验义务

本文最多支持：

```text
same-attempt Evidence continuity feasibility = audited local witness only
Evidence runtime                              = false
contract frozen                               = false
implementation authority                      = false
manifest successor                            = false
persistence                                   = false
global composition authority                  = false
public Review / Core Verdict / R2-R6           = false
```

测试只证明exact applicability world中的bounded witness。它不证明Evidence已经产生、不证明原工程问题已经闭合、不证明各R1局部
结论能够全局组合。post-R1 global check是独立后验义务，不能提前进入本candidate或替代当前资格链。

## 12. Exact docs-only scope 与资格链

本candidate只允许：

```text
README.md
AGENTS.md
docs/396-r1-same-attempt-derivation-evidence-continuity-feasibility-recovery.md
docs/milestones.md
```

`docs/project-state.md`、doc318、doc377–395、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与
全部frozen semantic bytes必须保持base bytes。资格链为：

```text
final docs-only recovery bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc395 / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source-byte / problem-identity / five-route / retained-history reconciliation
    -> FEASIBILITY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
    -> separate docs-only versioned EVIDENCE_CONTINUITY_CONTRACT
```

任何non-success必须保留原identity；不得rerun洗白、回填PR #453或拼接different worlds。

## 13. 当前状态与下一合法边界

在本文自己的全部最后门闭合以前，只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整资格链闭合后最多成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP并建立独立docs-only versioned
Evidence continuity contract；该合同自己的完整资格链闭合以前runtime继续`NOT_STARTED / NOT_AUTHORIZED`。R1最终完成后还必须
执行独立global check；不得从本文直接施工Evidence、manifest、persistence、public Review或R2–R6。
