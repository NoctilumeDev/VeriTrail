# R1 same-attempt DerivationEvidence continuity private implementation qualification recovery publication

日期：2026-11-15

> 状态：`QUALIFICATION_RECOVERY_PUBLICATION_CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`。
>
> exact base：`818b64a2bf23cce0ebd821f768652f5b83a6d94b`，tree
> `3f31835d22b170b436b7b4f118e4247a6a32d80e`。
>
> 影响：`L0_DOCUMENTATION / IMPLEMENTATION_QUALIFICATION_RECOVERY_ONLY`。本文不修改runtime、tests、workflow、Browser oracle、
> timeout、Schema、manifest、persistence、public Review、Core Verdict、global composition authority或R2–R6。自己的完整资格链闭合以前，
> doc405继续`MERGED / NOT_QUALIFIED / NOT_FROZEN`。

## 1. CONTROL LOOP重建结果

[授权发布](404-r1-same-attempt-derivation-evidence-continuity-private-implementation-authorization-publication.md)已经以自己的完整资格链使
`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED`生效。PR #464随后把
[实现候选](405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md)精确合入：

```text
candidate base / head / tree = b5ff07e... / b4fa42c... / c8f0bd1...
original Public CI           = 43034543495 / attempt 1 / 11 of 11 SUCCESS
protected merge              = a41b8ba3575419e754099725b5e1616af6cd1af4
exact-main Public CI         = 43040847982 / attempt 1 / 11 of 11 SUCCESS
exact-main Browser Smoke     = 43040847817 / attempt 1 / FAILURE before product build
```

该Browser job在`Install Chromium`阶段遇到DNS setup failure，产品build/smoke没有执行；所以doc405保持
`MERGED / PUBLIC_CI_PASS / BROWSER_SMOKE_FAILED / NOT_QUALIFIED / NOT_FROZEN`。后继资格链没有回填首败：

- [doc407](407-r1-same-attempt-continuity-original-public-ci-timeout-failure-boundary-audit.md)只资格化PR #465 original gate timeout边界；
- [doc408](408-r1-public-ci-review-attention-topology-containment-maintenance.md)冻结Review Attention四格拓扑维护，不资格化doc405；
- [doc409](409-r1-same-attempt-continuity-dec001-semantic-fixture-clock-correction.md)只冻结DEC-001测试证明时钟修正，不改变runtime；
- [doc406](406-r1-same-attempt-continuity-private-implementation-exact-main-browser-smoke-failure-boundary-audit.md)经PR #470闭合后只把
  `43040847817`升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。

PR #470绑定`e17f7e6... / 86ce1b4... / 3f31835...`并精确合入当前`main@818b64a...`。original Public CI
`43660628037`与exact-main Public CI `43663846845`均15/15 SUCCESS，Browser Smoke `43663846915`为1/1 SUCCESS；fresh
README/doc405/doc406/doc409 Render与AGENTS/milestones raw observations全部取得各自唯一qualifying PASS。independent reconciliation、
140-artifact closeout与finite integrity SHA-256为：

```text
00ad45ddfd052bb7c76b6b680f17b1d80bfc076a0ec25008ace8e8640022e22d
a503ac1f751fa1fce439e8b356bb533935bcdc9a908194f1762ec6302b1c5eba
87eb1bae540b401bc3a2a0b91c7d63cd6d88c3bee424f957444c05711adf3ce0
```

reconciliation attempt 1的schema-key setup error、worktree attachment cap、command policy rejection与anonymous rate exhaustion均按原identity
保留，effect为`NONE`。这些事实解除独立implementation qualification recovery publication的阶段阻断，不把任何后继PASS继承给PR #464。

## 2. exact implementation source与唯一test successor

CONTROL LOOP逐字节比较PR #464 candidate commit `b4fa42c...`与当前exact main。五个private runtime文件完全相同；唯一变化是doc409已经
独立冻结的DEC-001 test proof clock successor：

| Path | PR #464 SHA-256 | 当前 SHA-256 | 解释 |
| --- | --- | --- | --- |
| `_fact_fulfillment.py` | `f2dad4e394edff4323d26eedf0647ade7a0d48f2e7f425ba63ee21e5313742cb` | `f2dad4e394edff4323d26eedf0647ade7a0d48f2e7f425ba63ee21e5313742cb` | unchanged runtime |
| `_fact_relation_transition.py` | `e6ce67331b7055623971f1edb3a9830b89e0c2fb47020ea67093714538eeaa8d` | `e6ce67331b7055623971f1edb3a9830b89e0c2fb47020ea67093714538eeaa8d` | unchanged runtime |
| `_post_terminal_fact_dual_successor.py` | `d7f19f631f4527278f4f660a2aa7a57b661ced0ec51a2a5cffa954b15e2e0742` | `d7f19f631f4527278f4f660a2aa7a57b661ced0ec51a2a5cffa954b15e2e0742` | unchanged runtime |
| `_unified_review_coverage_output_admission.py` | `5194c7431429a9181c8e2a744fe419816699be835a05b54b831c806d05b5be51` | `5194c7431429a9181c8e2a744fe419816699be835a05b54b831c806d05b5be51` | unchanged runtime |
| `_same_attempt_derivation_evidence_continuity.py` | `dc42d38c68ed6cc96dc072f5d51a5289b67648f4252e29af7a1c3d2b2a759a42` | `dc42d38c68ed6cc96dc072f5d51a5289b67648f4252e29af7a1c3d2b2a759a42` | unchanged runtime |
| `test_same_attempt_derivation_evidence_continuity.py` | `4ada737c77b7e7a0c033a18c59f9ca837f11b9e5586cbcde69241da0e3c5ba11` | `ad2b32664da792f318cf3235af22cb49e3bf079f908a42eb5cbf58b0736a53f5` | doc409 frozen proof-clock successor |

`b4fa42c..818b64a`之间只有`f86972a test(review-attention): isolate DEC-001 semantic clock`触及这六个路径。本文不把test
successor伪装成原candidate bytes；它明确把当前runtime bytes与已冻结test successor作为新的qualification world。

## 3. 原问题、当前证明义务与适用世界

```text
original engineering problem
    normal与四类negative route需要same-attempt端到端DerivationEvidence连续性

current proof obligation
    对已经合入但因PR #464 exact-main Browser setup首败而未资格化的private implementation，
    从当前exact source + doc409 test successor + qualified failure histories建立新的资格链

applicability world
    main@818b64a / tree 3f31835
    + PR #464 exact implementation source bytes
    + doc409 frozen test successor
    + doc406/doc407 qualified failure boundaries
    + doc408 frozen topology maintenance

proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

本文只恢复doc405的qualification，不解释PR #464 DNS setup failure、PR #465 slowdown或PR #468 DEC-001 failure的唯一底层原因；三者继续
`UNKNOWN`。局部qualification也不恢复global composition authority。

## 4. final local qualification

final candidate必须在当前六个source/test hashes上重跑：

- Python 3.10.6/3.13.13 × normal/`-O`的five-route semantic report；
- 八个focused suites；
- 完整Review Attention discover suite；
- compile、`git diff --check`、global/local hygiene、forbidden public export guard、link/encoding/scope与primary audit continuity。

最终记录由本candidate的local evidence seal机械绑定；测试只作当前world witness，不继承PR #464资格，也不取代original PR、protected merge、
exact-main gates、installed-product readback或independent reconciliation。

final local matrices绑定当前六个source/test hashes，结果为：

| Matrix | Python 3.10.6 normal / `-O` | Python 3.13.13 normal / `-O` | SHA-256 |
| --- | --- | --- | --- |
| five-route semantic | PASS / PASS | PASS / PASS | `efeffcc2d5806b772f1920fbe4ecfed70e6081afcf263399025070b6aaccaaed` |
| focused suites | 152/152 / 152/152 | 152/152 / 152/152 | `0cddbbc0a4225529162b6a5318674b0fb2f3a0be3e612e95b455190a60369e02` |
| full discover | 674/674 / 674/674 | 674/674 / 674/674 | `f69dab4d097085a517f3734a0fd6f7c3157d63c51eb6d12a48ec133acbe54deb` |

四格semantic canonical digest为
`198171903f032ef03249631457dcc45d9c7a95a1f3a3740e2a26fe85875ee34a`；exact source audit SHA-256为
`b157c42c5dfccfa39b0ccee4e8c5f936c62e6999b4e400be2779d3422252ca54`。这些结果仍只属于本candidate的local witness。

## 5. tracked scope

本publication只允许：

```text
README.md
AGENTS.md
docs/410-r1-same-attempt-derivation-evidence-continuity-private-implementation-qualification-recovery-publication.md
docs/milestones.md
```

doc397–409、private runtime/tests、workflow、Browser oracle、Schema、manifest、persistence、public Review、Core Verdict、
`docs/project-state.md`、primary `audit.json`与R2–R6必须保持base bytes。source/test文件只读复算，不能在本candidate内修补。

## 6. qualification pipeline

```text
final docs-only recovery bytes / declared local gates
    -> original PR Public CI attempt 1 / 15 of 15
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc405 / doc406 / doc409 / doc410 observation
    -> fresh anonymous AGENTS / milestones / six implementation source-test exact-commit raw-byte observation
    -> independent source-byte / five-route / authority / retained-failure reconciliation
    -> finite closeout / integrity
    -> doc405 IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED at most
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止；不得重复已有PASS或用后继PASS覆盖历史。若Render目标超过冻结窗口，只能保留diagnostic并把该目标的
证明责任显式移到raw/API/exact-git一致性，不能用raw bytes冒充Render completeness。

## 7. state ceiling

全部门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_CONTINUITY_DEC001_SEMANTIC_FIXTURE_CLOCK_CORRECTION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_QUALIFICATION_RECOVERY_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后，doc405最多成为`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED`，仍不是`FROZEN`。随后必须返回
CONTROL LOOP，只有前提继续成立才可建立独立docs-only implementation freeze publication；不得从本文直接启动manifest、persistence、
public Review、global composition或R2–R6。
