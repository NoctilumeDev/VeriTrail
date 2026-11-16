# R1 M10 repeatability exact-main failure-boundary audit

日期：2026-11-16

> 候选状态：`R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@2a9a2af4221175064ba4e9cd7a424472804df985`，tree
> `4e86702a4d1c1618bd9b0951f0c16bcbbdc8dbf4`。
>
> 受审对象：PR #481精确合并后的exact-main Public CI `43783429314` attempt 1 failure。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只保存失败identity、资格影响、
> `UNKNOWN`上限、failure-observation缺口与最小后继责任；不修改runtime、tests、fixture、Browser collector、timeout、retry、workflow、
> Schema、Verdict、doc420、carrier、Manifest、persistence、public Review或R2–R6。

## 1. CONTROL LOOP触发事实

[文档420](420-r1-m10-subject-drift-browser-first-failure-observation-correction.md)的test-only candidate精确绑定：

```text
base    = f298b042ccb5124d117f6a82d76dbf93624a861d
head    = 46e0ec07997c0d083c3db9cb14f96d3382a6e787
tree    = 4e86702a4d1c1618bd9b0951f0c16bcbbdc8dbf4
commits = 1
files   = 5
scope   = README.md
          AGENTS.md
          docs/420-r1-m10-subject-drift-browser-first-failure-observation-correction.md
          docs/milestones.md
          tests/test_bootstrap_run_cli.py
```

它只给subject-drift exact-set witness增加bounded Browser/bootstrap failure projection与controlled proof-facility witness；没有修改Core
runtime、Browser collector、timeout、retry、workflow、Schema、Verdict或carrier。

本地最终字节的focused四格各2/2 PASS、full Core四格各498/498 PASS、global/local hygiene 8/8 PASS；local qualification SHA-256为
`914781c3a9e98f0816c45a761304644c6b0d8e8800a47401f0f2f266959226a0`，58-artifact post-commit seal SHA-256为
`10c9330f6354db012bc107a7c49667c8274542b15bf90d6ee0f8a7d73f2661e6`。这些local witness不替代远端资格门。

## 2. original gate与protected merge

PR #481 original Public CI `43780269329` attempt 1在candidate head上取得15/15 SUCCESS，没有rerun。original qualification record
SHA-256为`4bb42d5c0c6f86e7bf65585be0f7bb3de44abb51f7254f4d673718b2880baf2c`。

受保护exact-head merge形成：

```text
merge   = 2a9a2af4221175064ba4e9cd7a424472804df985
tree    = 4e86702a4d1c1618bd9b0951f0c16bcbbdc8dbf4
parents = f298b042ccb5124d117f6a82d76dbf93624a861d
          46e0ec07997c0d083c3db9cb14f96d3382a6e787
```

protected-merge evidence SHA-256为
`23fa9cb93f5141abb364766440e81f4ab034c99f81419895a1ec952f8a35fb1b`。首次candidate tree probe因PowerShell未引用
`HEAD^{tree}`而被解析为operator；该setup error SHA-256
`932cb73aba7e8169f533dc7762522a8d8f1570709ae4f64b23180cea3e6bee38`按原identity保留，后继正确引用只修命令，不删除第一次事实。

## 3. exact-main required gate failure

exact-main Browser Smoke `43783429308` attempt 1为1/1 SUCCESS；exact-main Public CI `43783429314` attempt 1以FAILURE终结，
没有rerun。失败坐标为：

```text
run         = 43783429314 / attempt 1
head        = 2a9a2af4221175064ba4e9cd7a424472804df985
job         = Python 3.13 on Windows / 133034359378
failed step = Run Core regression tests
failed test = tests.test_bootstrap_run_cli.BootstrapRunCliTests.
              test_same_sealed_authorities_repeat_without_residual_contamination
```

原始assertion现场为：

```text
expected execution_status = COMPLETED
observed execution_status = ERROR
stop_reason               = COLLECTOR_ERROR
verdict                   = FAIL
browser_capture_complete  = false
browser_completed         = false
cleanup_complete          = true
browser_error_types       = ()

Ran 498 tests in 115.873s
FAILED (failures=1, skipped=1)
```

failed job log SHA-256为
`302e8a372493ba0ba19280d62991d621c760d2478e2686f6a2cdf2d2b3bbb95f`；结构化failure record SHA-256为
`44f98e2280e8732913b3d8e8e08f6420405bf86b2c66b61144f0641575d9117c`。第一次在run尚未终结时抓取failed log只得到
“run is still in progress”；该preterminal setup error SHA-256
`7046d56fea66d06a889743b2886deeeddb03dd8a257818e4f5de4d6fd5b6f755`永久保留。

Python 3.10 on Windows、Workbench、E3 release acceptance与Review Attention四格均SUCCESS；四个下游required group因前驱未全部成功而
SKIPPED。该run只产生四份成功Python 3.10 distribution Artifact：

| artifact | id | digest |
| --- | ---: | --- |
| `github-evidence-wheel-3.10` | `14190323629` | `sha256:e57e524b1fa64edb8057aba69d47948c3ce3d23faa09267ab59f158a67e8431c` |
| `core-sdist-3.10` | `14190278685` | `sha256:aadbe171fe6e9ee8fe84ac915847640ce7ab83bda369f273911be740b71e9d5b` |
| `p3-wheel-probe-3.10` | `14190243932` | `sha256:7458251bc89c0b3cc3afb38b4f90051372363e552001df08b2f9820943cfc46b` |
| `core-wheel-3.10` | `14190164666` | `sha256:9f4b18209abfa9533f25926032d1d34bc5a53f0c112151715c22ad0d529c116b` |

没有failed evidence Artifact。另一Python lane与Browser Smoke的PASS不能与失败lane拼接成exact-main qualification。

## 4. 资格影响

doc420的资格链在new exact-main required Public CI处停止：

```text
doc420 publication       = MERGED / NOT_QUALIFIED
exact-main Public CI     = FAILED
fresh product readback   = NOT_STARTED / FORBIDDEN_AFTER_GATE_FAILURE
independent reconciliation = NOT_STARTED
finite qualifying closeout = NOT_STARTED
```

original gate成功、protected merge成立与Browser Smoke成功都不能替代失败的exact-main Public CI；相同tree也不产生资格继承。doc420因此
不能成为`M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_QUALIFIED`，也不能按原文自动进入manifest carrier contract。

## 5. failure-observation gap与归层上限

失败test现有diagnostic只保留public payload与`browser_error_types`。后者只在patched Browser collector抛出
`ObservedBrowserCollectionError`时追加private error type；本次payload已经是`COLLECTOR_ERROR`，但tuple仍为空，且失败发生在Bundle形成以前，
没有Browser/bootstrap Evidence可供后验投影。因此不可变现场没有保存足以区分下列可能边界的lower facts：

```text
Browser collection exception
service/readiness/process coordination
full-suite residual resource interaction
test trace coverage gap
runner or environment condition
```

这些只是待区分边界，不是已证明根因。当前证据只允许：

```text
required exact-main gate failure                     ESTABLISHED
repeatability witness observed ERROR/COLLECTOR_ERROR ESTABLISHED
cleanup_complete                                     OBSERVED_TRUE
existing lower error trace                           EMPTY
failure-observation insufficiency                    ESTABLISHED
stable isolated local reproduction                   NOT_OBSERVED
doc420 semantic contradiction                        NOT_ESTABLISHED
runtime semantic defect                              NOT_ESTABLISHED
test oracle defect                                   NOT_ESTABLISHED
workflow defect                                      NOT_ESTABLISHED
underlying product/environment cause                 UNKNOWN
```

exact-main source上的精确失败test在CPython 3.10.6 / 3.13.13 × normal / `-O`四格各1/1 PASS；unittest elapsed分别为
6.952s、6.741s、7.047s、6.533s。该结果只分类为`NON_QUALIFYING_DIAGNOSTIC`：它证明稳定隔离复现未被观察到，不解释
original exact-main failure，也不能回填run `43783429314`。

## 6. 被击穿的最小边界

doc420新建的subject-drift diagnostic没有被失败test调用；本次失败也没有观察到原`BROWSER_STATUS_CONFLICT` exact-set反例。因此不能把
本次failure拼接为doc420修正对象的同一根因。

当前最小重开边界是：

```text
M10 same-sealed-authorities repeatability witness under full-suite load
plus its first-failure observation/retention facility
```

它目前只允许audit。现有证据尚不能决定后继应只扩充test failure capture、调整deterministic fixture、修复Browser/runner coordination，还是
归入外部环境。必须先由独立read-only feasibility audit建立可重复证据与最小落点，才能申请任何test-only或runtime施工权。

## 7. 禁止的伪恢复

以下动作均不能使doc420取得资格：

```text
rerun Public CI 43783429314
retry until PASS
用Browser Smoke、Python 3.10或其他job PASS覆盖Python 3.13 failure
用四格隔离PASS覆盖full-suite failure
把空browser_error_types解释为Browser/collector一定没有失败
把COLLECTOR_ERROR命名成已证明的Browser、资源、平台或环境根因
增加timeout、retry、skip或放宽required gate
弱化COMPLETED/PASS/cleanup/repeatability oracle
直接修改test或runtime而跳过failure-boundary与feasibility资格链
用后继candidate绿灯回填doc420或run 43783429314
直接重建manifest carrier contract
```

## 8. 最小合法后继 seam

恢复必须串行：

1. 本docs-only failure-boundary audit先通过自己的完整资格链，只把exact-main failure identity、doc420 qualification effect、
   `UNKNOWN`与authority ceiling升级为qualified history；
2. 返回fresh CONTROL LOOP，从新的exact main建立独立read-only repeatability failure-observation feasibility audit；
3. feasibility只允许复核current exact source、保留失败log、既有M10合同/历史与有界诊断，不得修改test/runtime或rerun失败attempt；
4. 只有feasibility自己的完整资格链闭合并定位最小责任后，才可另建versioned correction/authorization publication；
5. 只有被重开的M10边界重新闭合，才可从新的exact main重建manifest carrier successor contract。

若本审计自己的required gate再次出现同类failure，必须保留新identity并纳入同一最小边界；不能把重复失败变成弱化oracle的理由。

## 9. 当前状态与authority ceiling

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_FAILURE_BOUNDARY_AUDIT_READBACK_TARGET_CORRECTION_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDITED_QUALIFIED_HISTORY

R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_PR481_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_NOT_STARTED_NOT_AUTHORIZED

R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文不修改doc420或任何frozen runtime/test事实，也不授权Schema、carrier/runtime、Manifest、persistence、global composition、public Review
或R2–R6施工。

## 10. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/421-r1-m10-repeatability-exact-main-failure-boundary-audit.md
docs/milestones.md
```

doc420、Core/Workbench runtime、tests、fixtures、workflows、Schema、Evidence、carrier、Manifest与persistence必须保持
`2a9a2af…` base bytes。final bytes至少通过exact scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
retained failure hashes、source/test/oracle/history continuity、`git diff --check`、global/local hygiene、focused四格与primary `audit.json`
continuity。

本worktree的Codex侧栏登记因本聊天累计超过100个artifact identity失败；setup error SHA-256为
`b89bfddb3cb5530042f47e4ce4dc7f8422151caa8f80d0b64eb677aa2afa168a`，effect `NONE`。source identity record
SHA-256为`22034f58494368e288fc92719df958dc093c389e4aa034f038c6484470650ce8`。两者不改变Git、GitHub或产品观察面。

final docs字节形成后，repeatability witness、controlled Browser error trace与doc420 diagnostic witness在CPython 3.10.6 / 3.13.13 ×
normal / `-O`四格各3/3 PASS；matrix summary SHA-256为
`61dacd16d7ef1c87e09c6df9fa149d2f40d15b98e413d31ecb6955122c97e573`。global/local hygiene 8/8 PASS，summary
SHA-256为`27444f5cc256297b636525eeef98bc2687fbf5232c63e61839269a424191adb7`。精确失败test的独立四格diagnostic
summary SHA-256为`8e9e4dc2356a26643aa3bb80f645ae72b90b26957d1969c43252afa69fc05dd0`。这些都只作local witness，不解释或
覆盖exact-main failure。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required Public CI (new run; no rerun of 43783429314)
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc420 / doc421 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source/failure/problem-identity reconciliation
    -> finite closeout/integrity
    -> M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止，不重复已有PASS。全部最后门闭合后，doc420仍保持`MERGED / NOT_QUALIFIED`，run
`43783429314`与lower `UNKNOWN`均不回填。随后必须返回CONTROL LOOP，不能按文档编号自动修test/runtime或重建carrier。

`proof_is_not_problem_solving = true`：把失败边界写清并资格化，不等于底层工程问题已解决。

`local_not_global = true`：本审计只处理该M10 repeatability failure world；R1完成后的人类+AI全项目检查仍是独立义务。
