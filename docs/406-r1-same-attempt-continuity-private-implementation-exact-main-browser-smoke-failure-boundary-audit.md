# R1 same-attempt continuity private implementation exact-main Browser Smoke failure-boundary audit recovery v2

> 日期：2026-11-15
> 状态：`RECOVERY_V2_CANDIDATE / NOT_QUALIFIED`
> exact base：`e17f7e6f42f715b1a478390cfcce7b5cc3e0a7e7`
> base tree：`eed2f3f5c1ed220c1bdd7688fe5395f0bee47b3e`
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只从新的exact main重建PR #464 Browser
> Smoke首败的bounded audit publication；不修改runtime、tests、workflow、Browser oracle、retry、timeout、Schema、manifest、
> persistence、public Review、Core Verdict、global composition authority或R2–R6。

## 1. 为什么必须从新world重建

[文档405](405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md)的实现candidate绑定：

```text
base / head / tree = b5ff07e... / b4fa42c... / c8f0bd1...
shape              = 1 commit / 10 files
original Public CI = 43034543495 / attempt 1 / 11 of 11 SUCCESS
protected merge    = a41b8ba3575419e754099725b5e1616af6cd1af4
exact-main CI      = 43040847982 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke      = 43040847817 / attempt 1 / FAILURE
```

Browser job在产品build/smoke以前的`Install Chromium`失败，doc405因此保持
`MERGED / PUBLIC_CI_PASS / BROWSER_SMOKE_FAILED / NOT_QUALIFIED / NOT_FROZEN`。

第一次docs-only failure-boundary candidate PR #465绑定`a41b8ba... / ffd09d2... / 9ef11a4...`，其original Public CI
`43056337145` attempt 1在Python 3.10 aggregate lane触到55分钟上限而`CANCELLED`；#465关闭、未合并、未rerun。
[文档407](407-r1-same-attempt-continuity-original-public-ci-timeout-failure-boundary-audit.md)随后以自己的完整资格链成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`，但不回填#465或doc405，下层变慢原因仍为`UNKNOWN`。

[文档408](408-r1-public-ci-review-attention-topology-containment-maintenance.md)没有继续增加aggregate timeout，而把Python
3.10/3.13 × normal/`-O`四个完整Review Attention suites拆到独立Windows cells，并让既有required Python jobs fail-closed消费
四格结果。PR #467在`main@e61b9a2c195633b238ba69884c43315b099ed1a6`完成original/exact-main 15/15、Browser 1/1、fresh
readback、independent reconciliation与finite closeout，所以该topology maintenance已经`FROZEN`；它仍不资格化doc405。

fresh doc406 recovery PR #468绑定`e61b9a2... / 6d0e645... / 010b71a...`。original Public CI `43641391725`
attempt 1的三个Review Attention cells成功，Python 3.10 `-O` cell在674 tests后于`DEC-001`第四个negative world报告1个
ERROR；两个required Python barriers正确fail closed。#468已经关闭、未合并、未rerun，lower cause保持`UNKNOWN`。

[文档409](409-r1-same-attempt-continuity-dec001-semantic-fixture-clock-correction.md)只修正该test的证明时钟，不增加60秒
budget、不修改runtime或真实deadline/cancellation oracle。PR #469的完整资格链绑定：

```text
candidate base / head / tree = e61b9a2... / f86972a... / eed2f3f...
original Public CI           = 43651437482 / attempt 1 / 15 of 15 SUCCESS
protected merge              = e17f7e6f42f715b1a478390cfcce7b5cc3e0a7e7
exact-main Public CI         = 43654317129 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser Smoke     = 43654317045 / attempt 1 / 1 of 1 SUCCESS
fresh reconciliation         = 13e54d9f1f55c68118d2392cc191edf084b344c2e902b78421bf3ff67aa80ea3
140-artifact closeout        = 9b5cac60266ae8264ca12472aa83d33f9acbb76979897a22a8d1147885e79c64
finite integrity             = bd6c6e492768a62a17a8399da94d46083b3e7a6fa112daae865a8540ccd8941f
```

milestones diagnostic #1的`PARTIAL / CONTENT_TRUNCATED`与README formal #1的anonymous
`COLLECTION_BUDGET_EXHAUSTED`均保留原identity；后继新identity PASS没有覆盖它们。successor只把过大的milestones移到
raw/API/exact-git byte responsibility，没有放宽`COMPLETE`或524288-byte Collector limit。因此
`R1_SAME_ATTEMPT_CONTINUITY_DEC001_SEMANTIC_FIXTURE_CLOCK_CORRECTION_FROZEN`已经生效，但PR #468、doc405和本文均不继承其资格。

## 2. PR #464 Browser首败的直接事实

```text
run         = 43040847817 / attempt 1
workflow    = Browser Smoke
job         = Production Workbench smoke / 130591908382
failed step = Install Chromium / step 6
command     = python -m playwright install --with-deps chromium
```

checkout、Python 3.13、Node.js 22与browser adapter安装成功。Chromium依赖安装开始后，Ubuntu mirror与security域名持续报告：

```text
Temporary failure resolving 'azure.archive.ubuntu.com'
Temporary failure resolving 'archive.ubuntu.com'
Temporary failure resolving 'security.ubuntu.com'
```

依赖下载最终以`apt` code 100、Playwright安装失败、step exit 1终结。production Workbench build与bounded browser smoke均
`SKIPPED`，Actions Artifact API返回`total_count = 0`。没有产品页面、浏览器断言、console、request或screenshot结果可裁定subject。

直接证据只允许：

```text
classification                                  EXACT_MAIN_BROWSER_SMOKE_CHROMIUM_INSTALL_DNS_SETUP_FAILURE
required exact-main Browser gate failure       ESTABLISHED
Chromium dependency-install DNS setup failure  ESTABLISHED
product build executed                         FALSE
product browser smoke executed                 FALSE
subject failure                                NOT_ESTABLISHED
candidate regression                           NOT_ESTABLISHED
exact lower runner / DNS / network cause       UNKNOWN
```

finite failure evidence与exact-main gate summary SHA-256分别为：

```text
697ffe7ae94d7f86d8c51bf5194a0f7e4b90e9d4a360566c047875dc4841a75b
2460a3d70cfd6c1ed2ecc31e1979bf52ac269e30e5a933e4ecccf3389d62da1c
```

## 3. 证明边界不是任务完成

本地runtime witness与PR #464 original Public CI证明candidate bytes在各自world通过；`43040847817`又足以否定其exact-main Browser
qualification。PR #466/#467/#469的后继Browser SUCCESS只证明各自exact world的门成立，不解释或回填首败：

```text
same or related bytes sometimes pass later != failed attempt passed
setup failure before product smoke          != product regression
qualified failure history                   != implementation qualification
proof that the boundary is known            != proof that the engineering task is complete
```

本文不得把DNS setup failure改名为GitHub、Ubuntu mirror、runner、代理或candidate代码的已知单一根因，也不得把doc408/doc409维护解释为
Browser失败已修复。局部修正不是全局完成；R1完成后的独立人类+AI全项目检查继续保留。

## 4. 当前最小合法seam

本文只让保留的`43040847817`失败identity在`e17f7e6...` world经过一条全新的docs-only资格链，成为可消费的qualified history：

1. 不复用PR #465或#468的commit、tree、attempt或资格；
2. 只发布失败identity、资格影响、`UNKNOWN` lower cause及后继authority ceiling；
3. 本candidate自己的Browser gate成功时，只证明当前qualification无需弱化门，不解释或回填`43040847817`；
4. 全部门闭合后只升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
5. publication形成新事实后返回CONTROL LOOP，重新核对doc404 authority、doc405 exact source hashes、保留首败与当前主线；
6. 只有新CONTROL LOOP没有反例时，才可另建implementation qualification recovery publication。

本文不直接恢复implementation qualification，不创建runtime patch，也不授权manifest、persistence、public Review、global composition或R2–R6。

## 5. 精确范围与local qualification

tracked scope只允许：

```text
README.md
AGENTS.md
docs/406-r1-same-attempt-continuity-private-implementation-exact-main-browser-smoke-failure-boundary-audit.md
docs/milestones.md
```

doc405、private runtime/tests、workflow、Browser oracle、Schema、manifest、persistence、Review、Core Verdict、doc407、doc408、doc409、
`docs/project-state.md`与primary `audit.json`必须保持base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、
links/fences/headings、required markers、failure identities、`git diff --check`、global/local hygiene、Python 3.10/3.13 × normal/`-O`
focused regression与primary `audit.json` continuity。

## 6. Qualification pipeline

```text
final docs-only recovery-v2 bytes / declared local gates
    -> original PR Public CI attempt 1 / 15 of 15
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc405 / doc406 / doc409 observation
    -> fresh anonymous AGENTS / milestones exact-commit raw-byte observation
    -> independent source / retained-failure / authority reconciliation
    -> finite closeout / integrity
    -> EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止；不得重复已有PASS。若milestones超过冻结Render窗口，只能保留diagnostic并把自身proof
responsibility移到raw/API/exact-git字节一致性，不能以raw bytes冒充render completeness。

## 7. 状态上限与停止线

全部最后门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_ORIGINAL_PUBLIC_CI_TIMEOUT_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN
R1_SAME_ATTEMPT_CONTINUITY_DEC001_SEMANTIC_FIXTURE_CLOCK_CORRECTION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDIT_RECOVERY_V2_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。doc405继续
`MERGED / NOT_QUALIFIED / NOT_FROZEN`，run `43040847817`、PR #465 `CANCELLED`、PR #468 original failure与全部lower cause不回填。
随后必须返回CONTROL LOOP，不能按文档号自动建立implementation recovery、冻结implementation、恢复manifest/global composition或进入R2–R6。
