# R1 same-attempt continuity private implementation exact-main Browser Smoke failure-boundary audit recovery

> 日期：2026-11-15
> 状态：`RECOVERY_CANDIDATE / NOT_QUALIFIED`
> exact base：`e61b9a2c195633b238ba69884c43315b099ed1a6`
> base tree：`7921b30f560959b74b67eb4a189d1e4413f42121`
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只重建PR #464 exact-main Browser Smoke首败的
> bounded audit publication；不修改runtime、tests、workflow、Browser oracle、retry、timeout、Schema、manifest、persistence、public
> Review、Core Verdict、global composition authority或R2–R6。

## 1. 为什么必须重建，而不能恢复旧候选

[文档405](405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md)的实现candidate绑定：

```text
base   = b5ff07e03630d57060384883d28a49dc57bdf0df
head   = b4fa42cc16b814f9d23e8c025bc4499dcb412084
tree   = c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255
shape  = 1 commit / 10 files
```

original Public CI `43034543495` attempt 1为11/11 SUCCESS；protected merge形成
`main@a41b8ba3575419e754099725b5e1616af6cd1af4`。该exact main的Public CI `43040847982` attempt 1为11/11 SUCCESS，Browser
Smoke `43040847817` attempt 1在产品build/smoke以前FAILURE。doc405因此保持
`MERGED / PUBLIC_CI_PASS / BROWSER_SMOKE_FAILED / NOT_QUALIFIED / NOT_FROZEN`。

第一次docs-only Browser failure-boundary candidate由PR #465绑定：

```text
base   = a41b8ba3575419e754099725b5e1616af6cd1af4
head   = ffd09d2ac5bfd2b35f433a31b64c72158d396ab9
tree   = 9ef11a45990d75e4e208043288f4f2b4901e7caf
shape  = 1 commit / 4 docs files
```

其local final bytes通过，但original Public CI `43056337145` attempt 1的Python 3.10 aggregate job在55分钟上限被`CANCELLED`；PR #465
随后关闭、未合并、未rerun。旧candidate的内容不能从`a41b8ba…`跨world继承到当前主线，也不能用后继绿灯洗白其original gate。

## 2. 两条合格历史先闭合证明地基

[文档407](407-r1-same-attempt-continuity-original-public-ci-timeout-failure-boundary-audit.md)经PR #466自己的original 11/11、protected
merge、新exact-main 11/11+1/1、fresh readback、independent reconciliation与finite closeout，成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。它只确认PR #465的55分钟aggregate containment反例，不回填PR #465或doc405；下层变慢
原因仍为`UNKNOWN`。

[文档408](408-r1-public-ci-review-attention-topology-containment-maintenance.md)随后没有继续提高同一aggregate timeout，而是把Python
3.10/3.13 × normal/`-O`四个完整Review Attention suites拆到独立45分钟Windows cells，并让名字不变的required Python jobs用
job-level `always()`与显式success assertion fail-closed消费四格结果。PR #467资格链绑定：

```text
candidate base / head / tree = 272d581… / 3d2dfb9… / 7921b30…
original Public CI           = 43630464678 / attempt 1 / 15 of 15 SUCCESS
protected merge              = e61b9a2c195633b238ba69884c43315b099ed1a6
exact-main Public CI         = 43633875326 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser Smoke     = 43633875335 / attempt 1 / 1 of 1 SUCCESS
fresh reconciliation         = f12a12741023e87cd3d0b316d0725c7fb9991f7a3805b632ffe3e8901c2ea322
130-artifact closeout        = 8566ec8d64dcd110add13ea61443bbb0533041efdc375d820abadac1650d132a
finite integrity             = 8d7864b46afaa2120a31a86c5b0722ae430bc8a567bd74440a30f5d6359063ac
```

milestones Render diagnostic仍保留`PARTIAL / CONTENT_TRUNCATED / NON_QUALIFYING_NONE`：冻结Collector的524288-byte文本上限观测到
679784 bytes。没有放宽`COMPLETE`、修改Collector limit或rerun；milestones最终只以raw/API/exact-git字节一致性承担自己的proof
responsibility。该边界不削弱doc408的其他三项完整Render与三个raw-byte目标。

因此当前只恢复“从新exact main重建doc406”的资格，不恢复旧candidate qualification，也不恢复doc405。

## 3. PR #464 Browser首败的直接事实

失败坐标：

```text
run         = 43040847817 / attempt 1
workflow    = Browser Smoke
job         = Production Workbench smoke / 130591908382
failed step = Install Chromium / step 6
command     = python -m playwright install --with-deps chromium
```

checkout、Python 3.13、Node.js 22与browser adapter安装均SUCCESS。Chromium安装开始后，Ubuntu mirror与security域名持续报告：

```text
Temporary failure resolving 'azure.archive.ubuntu.com'
Temporary failure resolving 'archive.ubuntu.com'
Temporary failure resolving 'security.ubuntu.com'
```

依赖下载最终以`apt` code 100、Playwright安装失败、step exit 1终结。随后production Workbench build与bounded browser smoke均
SKIPPED；Actions Artifact API返回`total_count = 0`。没有产品页面、浏览器断言、console、request或screenshot结果可裁定subject。

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

## 4. semantic result、qualification result与后继成功分离

本地runtime witness与PR #464 original Public CI证明candidate bytes在各自world通过；`43040847817`又足以否定它的exact-main Browser
qualification。后继PR #466/#467 Browser SUCCESS只证明各自exact world的门成立，不解释或回填首败：

```text
same or related bytes sometimes pass later != failed attempt passed
setup failure before product smoke          != product regression
qualified failure history                   != implementation qualification
proof that the boundary is known            != proof that the engineering task is complete
```

因此本文不得把DNS setup failure改名为GitHub、Ubuntu mirror、runner、代理或candidate代码的已知单一根因；也不得把doc408维护解释为
Browser失败已修复。

## 5. 当前最小合法recovery seam

本文只做一件事：让保留的`43040847817`失败identity在当前exact main上经过一条全新的docs-only资格链，成为可消费的qualified
history。串行边界是：

1. 本candidate独立绑定`e61b9a2…`，不得复用PR #465 commit/tree或资格；
2. 本candidate只发布失败identity、资格影响、`UNKNOWN` lower cause及后继authority ceiling；
3. 如果本candidate自己的unchanged Browser gate成功，只证明无需弱化门，不解释或回填`43040847817`；
4. 全部门闭合后只把本文升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
5. publication形成新事实后必须返回CONTROL LOOP，重新复核doc404 authority、doc405 exact source hashes、保留首败与当前主线；
6. 只有新CONTROL LOOP没有发现反例时，才可另建implementation qualification recovery publication；该后继仍需自己的完整资格链。

本文不直接恢复implementation qualification，不创建runtime patch，也不授权manifest、persistence、public Review、global
composition或R2–R6。

## 6. 精确范围与本地资格

tracked scope只允许：

```text
README.md
AGENTS.md
docs/406-r1-same-attempt-continuity-private-implementation-exact-main-browser-smoke-failure-boundary-audit.md
docs/milestones.md
```

doc405、private runtime/tests、workflow、Browser oracle、Schema、manifest、persistence、Review、Core Verdict、doc407、doc408与全部frozen
semantic bytes必须保持base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required
markers、failure identity、`git diff --check`、global/local hygiene、focused Python 3.10/3.13 × normal/`-O`与primary `audit.json`
continuity。

## 7. Qualification pipeline

```text
final docs-only recovery bytes / declared local gates
    -> original PR Public CI attempt 1 / 15 of 15
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc405 / doc406 / milestones observation
    -> fresh anonymous AGENTS raw-byte observation
    -> independent source / failure / authority reconciliation
    -> finite closeout / integrity
    -> EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止；不得重复已有PASS。若milestones再次超过冻结Render窗口，必须保留diagnostic并在不弱化
`COMPLETE`的前提下重新划分proof responsibility，不能以raw bytes冒充render completeness。

## 8. 当前状态与停止线

全部最后门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_ORIGINAL_PUBLIC_CI_TIMEOUT_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDIT_RECOVERY_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。doc405继续保持
`MERGED / NOT_QUALIFIED / NOT_FROZEN`，run `43040847817`、PR #465 `CANCELLED`与lower causes `UNKNOWN`不回填。随后必须返回
CONTROL LOOP，不能按文档号自动建立implementation recovery、冻结implementation、恢复manifest/global composition或进入R2–R6。
