# R1 same-attempt DerivationEvidence continuity private implementation 授权发布

日期：2026-11-11

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@ffe57f80d3c0eef85dcb5ad39753a0d7a1abbb11`，tree
> `d65c8a1b8bd832d3f782e83e67d6a5fd9b7add1e`。
>
> 上游：[最小合同 0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [合同冻结恢复发布 v2](402-r1-same-attempt-derivation-evidence-continuity-contract-freeze-publication-recovery-v2.md)与
> [private implementation 可行性审计](403-r1-same-attempt-derivation-evidence-continuity-private-implementation-feasibility.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只条件化发布bounded private implementation authority；不修改
> runtime、tests、Schema、manifest、persistence、public Review、Core Verdict、global composition authority或R2–R6。本文自己的
> 完整资格链闭合以前，`PRIVATE_IMPLEMENTATION_ALLOWED`不生效。

## 1. publication输入已经取得资格

PR #462把doc403 candidate
`base=08ac4eff9e14d7c31e09f963105d84a923021225 / head=184e6613264d7cc579363ff43dc280eeba1ee09f /
tree=d65c8a1b8bd832d3f782e83e67d6a5fd9b7add1e`精确合入
`main@ffe57f80d3c0eef85dcb5ad39753a0d7a1abbb11`。original Public CI `42911165390`、exact-main Public CI
`42917309917`与Browser Smoke `42917309911`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；没有rerun。

fresh detached exact-main world只认`ffe57f8… / d65c8a1…`。README、doc397、doc402与doc403各有唯一qualifying formal PASS；
AGENTS与milestones各有唯一anonymous raw/Contents API/exact-Git全字节一致PASS。README formal #1的anonymous API rate exhaustion
ERROR继续按原identity保留，formal #2才是该目标唯一qualifying PASS。independent reconciliation、172-artifact finite closeout与finite
integrity SHA-256为：

```text
2decaadb089a943346e508fe4c1cb6ad518925234e7acdb2bf3832fe2d69c35c
104b52d417a5ce4aed5a20137cb95c490ce1009221f4611a09c708fed3c89bba
7e1bc79e75c3860b2ac2cd41994d40708d591741a5066d4cfbe9aec929f7907c
```

doc403 full-file SHA-256为
`416811a3dd1b76a70f559fbbbdc03f57db633a3d1252f1f252b0ab19ca323360`。因此doc403现在是
`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；doc397合同继续
`FROZEN`。这两项事实只解除独立authorization publication的阶段阻断；runtime仍是`NOT_STARTED / NOT_AUTHORIZED`。

```text
qualified feasibility finding = FEASIBLE_WITH_VERSIONED_PRIVATE_OWNER_AND_BOUNDED_CONTROLLER_CAPTURE_ADDITIONS
```

## 2. 保留的失败、setup error与证明设施边界

以下身份继续保留，不被后继PASS回填：

- PR #453 original Public CI的missing required job/check identities、closed/unmerged/not-qualified与lower cause `UNKNOWN`；
- PR #457 original creation gate因PR metadata edit触发同head concurrency而`CANCELLED`，第二run仍为`NON_QUALIFYING / NONE`；
- PR #459/doc400 formal Render HTTP 503、`PARTIAL`、no Core Verdict、not-qualified/not-frozen与lower cause `UNKNOWN`；
- PR #462 fresh README formal #1的`API ERROR / Render COMPLETE / HTTP 200 / no Core Verdict`，底层匿名额度原因已观察，
  failure seal SHA-256为`2c46febe713c4984fd9ef3cfbaf1432ee71d8b9928d0a8874d99732e3c36ef9f`；
- formal adapter v2把可追加history逐字节冻结，只安全承载README formal #2一次追加；发现该边界后没有用已知drift adapter启动下一目标。
  边界记录SHA-256为`00c2155288f49e943da23eeb5cb26a39f7fb1047e74ad4d106e4ab9479fee8d4`；
- versioned v3 adapter只把既有history改成不可改写前缀并允许新identity追加；它没有重跑任何PASS或改变产品oracle，freeze
  SHA-256为`c18832118d87b335bc26e8099d34eb4a197b175b23c27b0b09d6f5e3fa023afb`；
- managed worktree attachment cap、PowerShell tree expression与venv path assumption均为`NON_QUALIFYING / NONE`；
- Codex desktop的`{"detail":"Bad Request"}`由用户确认为近期官方app bug，继续排除于VeriTrail产品与资格证据。

这些记录只证明失败与proof facility修正被分层保留，不证明旧失败没有发生，也不扩大本文authority。

## 3. 原工程问题、当前证明义务与适用世界

```text
original engineering problem
    normal与四类negative route需要same-attempt端到端DerivationEvidence连续性

current proof obligation
    只发布frozen doc397与qualified doc403允许的bounded private implementation authority；
    不把授权、测试或未来candidate解释为runtime存在或原工程问题已解决

applicability world
    exact main ffe57f8 source + frozen doc397/doc402 contract world
    + qualified doc403 feasibility world + retained failed/setup identities

proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

若原工程问题、证明义务或适用世界漂移，即使本文门禁全绿也必须停止。授权只是允许在指定边界内施工；它不证明施工已经发生、
same-attempt continuity已经产出、全局组合正确或用户目标已经完成。

## 4. 授权对象是bounded A–J

本文最后门闭合、返回CONTROL LOOP且前提仍成立以后，唯一允许的private implementation scope如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 新建versioned private continuity owner、binding/profile/wire identity；不得新增public export或重解释legacy Evidence 0.2。 |
| B | owner在同一个original attempt内绑定selector claim、`DerivationInputSet`、live `BudgetContext`、terminal Fact source与final admission identity。 |
| C | Fact controller只在原执行期间copy-own attempt/provider/phase wall start/finish；禁止attempt结束后重读clock、provider、path、log或外部状态。 |
| D | normal branch在one-shot continuation消费前copy-own exact transition admission document及其FactSet、RelationSet与provider/request lineage。 |
| E | Relation controller只在原执行期间copy-own provider-run与phase finish wall timing，并绑定同一个Fact source、RelationSet与attempt。 |
| F | normal branch绑定exact ReviewSliceSet、CoverageLedger、root chain、unified admitted result与final route/result identity；不得从artifact shape反推route。 |
| G | 四类negative branch绑定exact qualified negative Coverage result、terminal Fact source、selector claim、original inputs/context与final admission；不得虚构FactSet/RelationSet。 |
| H | copy-equal foreign attempt、same-digest substitution、wrong branch/result、replay、mutation、missing capture、late stop、proxy/subclass与concurrent second submit全部fail closed并revoke。 |
| I | owner与independent reconciler分别机械证明五条route的exact occurrence、one-shot lifecycle、empty/non-empty branch obligations与authority ceiling；共享同一个被测关键projector禁止。 |
| J | 把doc397 direct falsifiers与doc403 `DEC-000`至`DEC-029`转成private tests；运行Python 3.10.6/3.13.13 × normal/`-O`、legacy/full regression、compile/hygiene/scope/audit continuity并形成独立implementation candidate。 |

class、method、field、锁与文件布局仍由后继candidate决定。允许复用既有canonical serializer、frozen enum、live-context revalidation与
one-shot primitive；禁止让tests、expected result或candidate自己成为branch、reason、status或authority来源。

## 5. authority ceiling

本文最后门闭合后只允许：

```text
实现 bounded private continuity A–J
+ 增加对应private tests / audit fixtures
+ 运行冻结合同的五route矩阵、旧consumer与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改legacy Evidence 0.2、Fact/Relation/Slice/Coverage/admission语义或public exports
把四类negative Coverage重分类为FAILED / UNAVAILABLE或为其虚构FactSet/RelationSet
创建manifest、persistence、public carrier、public Review或Core Verdict
恢复或宣称global composition authority
启动language-support persistence、R2–R6、tag或Release
```

`PRIVATE_IMPLEMENTATION_ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。runtime patch必须拥有新的
source、branch、candidate head/tree、original PR门、protected merge、exact-main双门、fresh installed-product readback与independent
reconciliation；真实反例出现时停止当前施工，只重开被击穿的最小边界。

## 6. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止：

1. 五条route只能通过expected result、artifact presence、requester或candidate选择；
2. continuity必须拼接different attempts/worlds、copy-equal authority或post-attempt external reread；
3. normal transition admission无法在continuation消费前由original attempt owner取得；
4. controller timing只能事后重建，或需要修改既有Fact/Relation semantics才能表达；
5. negative route必须伪造FactSet/RelationSet或改写为legacy non-success才能通过；
6. bounded patch必须修改public Schema/export、manifest/persistence、Coverage reason/order或Core Verdict；
7. one-shot lifecycle无法绑定同一selector/input/context/terminal source/result/final admission，或revocation/resource closure无法机械证明；
8. DEC falsifier只有弱化oracle、删除首败、拼接不同world或重解释冻结历史才能通过。

授权已经生效也不能成为扩大scope、静默reopen合同或增加例外的理由。理论遇到反例先检查前提、适用域和模型；局部证明必须在R1
完成后接受独立human+AI global composition check。

## 7. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/404-r1-same-attempt-derivation-evidence-continuity-private-implementation-authorization-publication.md
docs/milestones.md
```

doc397、doc402、doc403、`docs/project-state.md`、runtime、tests、workflows、fixtures、Schema、Provider、Collector、oracle、Verdict与全部
frozen semantic bytes必须保持`ffe57f8…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/
headings、required markers、`git diff --check`、global/local hygiene、doc397/doc402/doc403/project-state full-file SHA、#462 exact gates、fresh
readback histories、retained failure、independent reconciliation、finite closeout/integrity与primary `audit.json` continuity。focused matrix与
read-only feasibility audit只能作witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original creation-event Public CI 11/11, attempt 1, no rerun
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc397 / doc402 / doc403 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> finite closeout and integrity
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用`http://127.0.0.1:7897`。任何non-success保留
原identity；不得rerun洗白、重复已有PASS或拼接不同world。PR title、body与base metadata必须在创建前完成，original creation gate终态前
禁止edit。

## 8. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把
`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内开始新的private implementation candidate；
不得把authority publication、形式矩阵或doc403 qualified history算作runtime证据。
