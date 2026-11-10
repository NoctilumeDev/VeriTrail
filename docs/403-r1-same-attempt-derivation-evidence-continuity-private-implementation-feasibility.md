# R1 same-attempt DerivationEvidence continuity private implementation 可行性审计

日期：2026-11-11

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@08ac4eff9e14d7c31e09f963105d84a923021225`，tree
> `c60c67f7057547e47b0b915a1807799d3ed6f9c9`。
>
> 上游：[最小合同 0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [合同冻结恢复发布 v2](402-r1-same-attempt-derivation-evidence-continuity-contract-freeze-publication-recovery-v2.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只审计private implementation feasibility；不创建runtime、tests、Schema、
> manifest、persistence、public Review、Core Verdict、global composition authority或R2–R6 authority。

## 1. CONTROL LOOP 与exact起点

PR #461已把doc402 candidate `68a986337f1e015c03c0bd07956fed2622bd2e60`、tree
`c60c67f7057547e47b0b915a1807799d3ed6f9c9`精确合入本审计基线。original Public CI `42887559185`、exact-main Public CI
`42893919168`与Browser Smoke `42893919002`均attempt 1 SUCCESS（11/11、11/11、1/1），没有rerun。original qualification与
exact-main gate seal SHA-256为：

```text
d18e8bb93e545e9ca2d2e690ea5b487d35906be49ba618eee69dc1d86ed9e956
53dd337cb002fa8c26d9eebea4147b5158ea525bf4aa8d3dcc7b4c9f5e394ceb
```

fresh README/doc397/doc399/doc400/doc401/doc402 formal各自唯一PASS；AGENTS/milestones raw-byte observations也PASS。independent
reconciliation、199-artifact finite closeout与finite integrity SHA-256为：

```text
4b0a4435230dc58ae5033bd8657c669d3f6addcef6148f562cfc45896cb0c572
5a7e135b6280d0102ad4b3b97e84e4eda98fc4209306d0674c143bf3d35f9aed
fc909233d94538219153fbb0d6b6e901f17e14d9860543328cb41df9322f5b9a
```

因此`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN`已经生效。该事实不回填PR #459/doc400的HTTP 503
formal ERROR；doc400仍是merged、not-qualified、not-frozen，lower cause仍为`UNKNOWN`。doc401继续只是qualified
failure-boundary history。

fresh CONTROL LOOP重新读取exact-main AGENTS、working method、hygiene、remote main与primary audit，确认下一最小seam只是独立
private implementation feasibility audit。合同冻结没有自动授予runtime施工权。

## 2. 原工程问题、当前证明义务与适用世界

```text
original engineering problem = normal与四类negative route需要same-attempt端到端DerivationEvidence连续性
current proof obligation      = 冻结doc397边界能否由有界private owner与原执行期capture实现，且不移动既有oracle
applicability world           = exact main 08ac4ef/tree c60c67f + frozen doc397/doc402
                              + normal corrected route + 四类qualified negative route
                              + CPython 3.10.6/3.13.13 normal/-O
proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

可行性成立不等于实现存在，更不等于原工程问题已经解决。用户反馈、局部PASS与形式证明都必须继续绑定原始目标；不能让“证明了一个
自洽construction”替代“实际产出continuity evidence”。R1全部完成后仍须独立做global composition check，检查局部结论的前提连续性、
authority/qualification断点、可组合性与最终用户能力；该未来责任不扩张本文authority。

## 3. 冻结语义与不可重解释面

本文机械消费doc397冻结的五个private identities：

```text
contract function                 r1-same-attempt-derivation-evidence-continuity/0.1
private continuity domain         SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1
controller capture function       r1-derivation-evidence-controller-capture/0.1
branch projection function        r1-derivation-evidence-continuity-branch-projection/0.1
independent reconciliation        r1-derivation-evidence-continuity-reconciliation/0.1
```

legacy `review-derivation-evidence-0.2`只允许`COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE`；`COMPLETED`要求非空Relation admission，
non-success要求空Relation admission与空reported identities。四类negative outputs是已资格化的application Coverage结果，不是FAILED或
UNAVAILABLE；因此legacy shape不能诚实表达全部五条route，也不得通过alias、duck type或status重分类复用。

Fact、Relation、ReviewSliceSet、CoverageLedger、selector、negative taxonomy、reason oracle、unified output admission、public exports、
manifest、persistence、CLI、Workbench、Provider、Collector、workflow、projection 0.8、Release资产与primary `audit.json`都不需要重开。
若实现必须移动其中任一冻结面，本文立即停止并返回CONTROL LOOP，只重开被真实反例击穿的最小边界。

## 4. Exact-source保留与缺口

current source已经保留：

1. selector route、original `DerivationInputSet`、live `BudgetContext`与terminal Fact source；
2. normal transition admission中的exact Fact source、FactSet、RelationSet、provider lineage与request provenance；
3. normal final composition中的ReviewSliceSet、CoverageLedger与root chain；
4. 四个negative outputs中的exact branch、terminal Fact source、CoverageLedger与route/result binding；
5. final unified admission中的one-shot route discriminant、result identity与authority ceiling。

但是完整final Evidence material尚未被一个owner连续保留：

```text
normal final composition does not retain the full transition admission document
Product Fact provider history does not retain controller-owned wall-clock start and finish fields
Relation provider lineage omits provider-run and phase finish wall-clock fields
final application output has no Evidence continuation owner
```

四类negative route没有FactSet/RelationSet是分支语义，不是待填空洞。当前final output的`derivation_evidence = false`也是现状事实，不能
被文档或测试改写成实现已存在。

## 5. 最小有界construction

exact source与冻结合同支持一个新的private、versioned continuity owner，在同一原始attempt内依次copy-own：

1. terminal Fact source、original `DerivationInputSet`与live `BudgetContext`；
2. Fact controller在原执行期间观察到的attempt/provider/phase wall timings；
3. normal transition admission document，在one-shot continuation消费前取得；
4. Relation controller在原执行期间观察到的provider/phase finish wall timings；
5. normal Slice/Coverage composition或四个negative route之一的admitted Coverage result；
6. final unified admission identity与exact route/result binding。

normal与negative是discriminated branches。owner必须绑定同一个selector claim、original attempt、input/context identity、terminal source、
downstream result与final admission；copy-equal foreign attempt、same-digest substitution、replay、wrong route/result、late stop、mutation、
missing capture、post-attempt clock/provider/path/log reread与第二次提交必须fail closed。controller-owned timing只能在原执行期间copy-own。

局部可行结论是：

```text
FEASIBLE_WITH_VERSIONED_PRIVATE_OWNER_AND_BOUNDED_CONTROLLER_CAPTURE_ADDITIONS
current_final_output_directly_retains_full_normal_continuity = false
current_source_retains_complete_final_evidence_material = false
existing_same_attempt_identity_and_semantic_material_is_bounded = true
legacy_shape_can_represent_all_five_qualified_outputs = false
versioned_successor_required = true
implementation_present = false
implementation_authorized = false
```

## 6. Fresh semantic与focused witnesses

fresh semantic audit从exact base构造normal corrected route与四个negative routes，核对legacy rejection、现有retention、六个capture point、
30个`DEC-000`至`DEC-029` falsifier、unified authority ceiling与source hashes。Python 3.10.6/3.13.13 × normal/`-O`四格的
canonical semantic SHA-256逐字节一致：

```text
b15ab4fc975ea4e63ff2b4dcf6030f6c70004d88be30c9f85d57dbf8f580c39d
```

semantic matrix与audit runner SHA-256为：

```text
ceac04f70f542d19659787be295e6f07d06ed80aa50b749043a508ce6deb9df7
4af1938286ef6ceabf014433df0d30dfee9b86ececafb87f7678a3d0a495800e
```

四份formal semantic report file SHA-256依次为3.10 normal、3.10 `-O`、3.13 normal、3.13 `-O`：

```text
c113658a7c0c2fed8216d19fc852b568ae18cf7dc6d047461050b1405ec52466
60dd00bfccd28f9670b577516b7d1f796b1988bea9b76d992b81b8ea13a6832f
024b508439d56faf6419401f4e9def9141746e89b16fecd16b0acb6cdcfaa6be
5d671156295e0848992f9af4d616a82bd766949b4ca2e53942c6be11b404748a
```

fresh focused witness覆盖post-terminal selector、Fact fulfillment、Fact/Relation transition、normal Slice/Coverage composition、四个
negative Coverage routes、Relation admission、unified output admission与legacy Evidence rejection。四格各运行相同126个测试并全部PASS；
focused matrix SHA-256为`605c9917d8cc9d2b16d256b651a838448073cbff309919f1a6592a9682e6405f`。四份record/log
SHA-256依次为：

```text
ff76417f4ef3bcfc00b7b72b12976e2ffbd9ab81ee3df8c95e7f4798db8ef7af
59937705ab97dfe1172166f5e9f9822fed4984ad01462437dd0cc0c5e29d1f8d
899eb1d8f1ef2c8a35c03791f3a992a45d1634ea14f40d62360ef10df8ed9a69
01775fc8e3c4936c17cbeeb153c519db231953f10468e5a5b14d02640dd10cbb
e492b95998de4adaa880359d037e19cd93a15762cbe3fd61a91f026121f0f0a8
11c4078291146a088a74ba6d056cd2041152dc8e923a291098790eb2c5bc90bf
e7d8b2a6203457211e74b2b999581688237d7da745f0ae308bca8a12490c5a7c
0af5f9b919b48bd6285ad57d6a1e7b5c33745db46b0a05ed22a2d862feaeec80
```

global/local hygiene在两套Python normal/`-O`共8格全部PASS，matrix SHA-256为
`092e992d89da8bbd61bffbc2f4262b9e89bc8d4ad4bda2cee70681f184b121e4`。primary audit SHA-256仍为
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 7. Retained setup errors与UI排除项

以下事实按原identity保留，但没有改变产品、repository、test或candidate bytes：

1. managed worktree创建完成，但chat registration因累计artifact identity超过100而失败；显式attach retry得到相同错误；
2. 一次source coordinate probe误以evidence root为working directory，audit hash成功而Git命令返回`not a git repository`；
3. Codex desktop反复出现的`{"detail":"Bad Request"}`已由用户确认是官方近期app bug，明确排除于VeriTrail失败与证据。

前两项均为`NON_QUALIFYING / NONE`。第三项是外部UI故障排除项，不得写入VeriTrail产品qualification。

## 8. Authority ceiling与停止线

本文最多支持一个local feasibility结论：private owner与原执行期bounded capture在当前exact world可实现。它不授权：

```text
runtime or tests                         false
public Schema or wire                    false
manifest or persistence                  false
public Review                            false
Core Verdict                             false
global composition authority             false
R2-R6                                    false
```

如果发现必须重解释legacy 0.2、把negative Coverage改成non-success、移动Fact/Relation/Slice/Coverage/admission semantics、在attempt结束后
重读外部状态、用equal digest拼接different attempts/worlds、删除retained failure或弱化任何oracle，本文结论立即停止。理论遇到反例必须
先检查前提、适用域和模型，而不是追加例外；局部PASS不能外推为全局正确。

## 9. Exact docs-only scope与资格链

本candidate只允许：

```text
README.md
AGENTS.md
docs/403-r1-same-attempt-derivation-evidence-continuity-private-implementation-feasibility.md
docs/milestones.md
```

doc397、doc399、doc400、doc401、doc402、失败PR #457中的doc398、`docs/project-state.md`、runtime、tests、fixtures、workflow、Schema、
Provider、Collector、oracle、Verdict与全部frozen semantic bytes必须保持base bytes。

资格链为：

```text
final docs-only feasibility bytes / declared local gates
    -> original creation-event Public CI 11/11, attempt 1, no rerun
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc397 / doc402 / 本文 readback
    -> fresh AGENTS / milestones raw+Contents API+exact-Git byte observations
    -> independent source-byte / contract-identity / five-route / retained-history reconciliation
    -> finite closeout and integrity
    -> FEASIBILITY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
    -> separate docs-only private implementation authorization publication
```

PR title、body与base metadata必须在创建前完成；original creation gate终态前禁止metadata edit。任何non-success保留原identity并停止，
不得rerun、retry-until-PASS或拼接different worlds。fresh installed-product observation必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。

## 10. 当前状态与下一合法边界

本文自己的全部最后门闭合以前，只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整资格链闭合后最多成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP并建立独立docs-only private
implementation authorization publication；该publication自己的全部最后门闭合以前runtime继续`NOT_STARTED / NOT_AUTHORIZED`。R1最终
完成后还必须执行独立global composition check；不得从本文直接进入manifest、persistence、public Review或R2–R6。
