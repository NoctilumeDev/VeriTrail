# R1 Review Derivation Manifest 0.2 original CI budget failure boundary

日期：2026-11-22

> 当前状态：`R1_REVIEW_DERIVATION_MANIFEST_0_2_ORIGINAL_PUBLIC_CI_BUDGET_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@50819b8ab16800a415439285dc9fcf909d5b435a`，tree
> `42f4337bb1b49957929c15fedf207e1aecfa5c06`。
>
> 影响：`L0_DOCUMENTATION / ORIGINAL_GATE_AND_CI_CONTAINMENT_PREMISE_AUDIT_ONLY`。本文只保存PR #512 original
> Public CI attempt 1的两个Python 3.10 Review Attention cells在45分钟outer budget处被取消、required aggregators fail closed、
> candidate关闭未合并及最小重开边界；不重跑、不合并失败候选，不修改workflow、runtime、tests、Schema、fixture、oracle或既有历史。

## 1. CONTROL LOOP 输入与候选坐标

PR #511已经把[Manifest 0.2 private implementation授权发布](448-r1-review-derivation-manifest-0-2-private-implementation-authorization-publication.md)
精确合入：

```text
base                    = f2394bdbb2910d5cc14bd1296d7ef503d2b60e66
head                    = 59c05a002562fa77c887c81dab49302f5efb04dc
tree                    = 42f4337bb1b49957929c15fedf207e1aecfa5c06
protected merge / main  = 50819b8ab16800a415439285dc9fcf909d5b435a
original Public CI      = 44905508551 / attempt 1 / 15 of 15 SUCCESS
exact-main Public CI    = 44909682401 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser      = 44909682395 / attempt 1 / 1 of 1 SUCCESS
```

fresh public installed-product P1/P2 formal、七个raw-byte targets、independent reconciliation、110-artifact closeout与integrity
全部闭合，所以`R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。formal attempt 1/2
non-success继续保持原identity，后继PASS没有覆盖它们。

PR #512随后从该exact main建立独立implementation candidate：

```text
PR                     = https://github.com/NoctilumeDev/VeriTrail/pull/512
base                   = 50819b8ab16800a415439285dc9fcf909d5b435a
head                   = a9c60eea76aad5e0801e76be639dc620388ce492
tree                   = 04629a631652ac5a75faf42b313a5d64bd2b9563
scope                  = 1 commit / 11 files
original Public CI     = 44969144404 / attempt 1
PR terminal state      = CLOSED / UNMERGED
same-head rerun        = NONE
```

candidate新增Manifest 0.2 Schema、compatibility fixture、private projector/admission/staging、独立conformance与tests；旧Manifest 0.1、
public exports、default composition、persistence、public Review与Core Verdict保持不变。它的本地final bytes曾完成四格focused、full
Review Attention、root Schema/payload、global/local hygiene与scope/audit continuity；这些只作local witness，不能替代original gate。

## 2. Original gate 的直接timeout事实

run `44969144404`绑定上述exact head，attempt 1终态为`CANCELLED`。四个Review Attention cells的机械结果是：

| Cell | Job | Started | Completed | Result |
| --- | ---: | --- | --- | --- |
| Python 3.10 normal | `137044844539` | `00:57:38Z` | `01:42:42Z` | `CANCELLED` |
| Python 3.10 optimized | `137044844604` | `00:57:38Z` | `01:42:43Z` | `CANCELLED` |
| Python 3.13 normal | `137044844593` | `00:57:38Z` | `01:31:34Z` | `SUCCESS` |
| Python 3.13 optimized | `137044844642` | `00:57:38Z` | `01:35:36Z` | `SUCCESS` |

两个Python 3.10 check-run都给出同一明确annotation：

```text
The job has exceeded the maximum execution time of 45m0s
```

normal cell在`test_uao_001_all_negative_routes_admit_exact_negative_result`执行中收到`KeyboardInterrupt`；optimized cell在
`test_dec_024_025_replay_and_concurrent_second_submit_are_rejected`执行中收到`KeyboardInterrupt`。两者随后都记录：

```text
The operation was canceled.
```

两个日志均没有`Ran N tests`、`OK`或`FAILED (...)`终结摘要，也没有完成的product assertion failure summary。required
`Python 3.10 on Windows`与`Python 3.13 on Windows`aggregators随后按设计真实`FAILURE`，其余Acceptance Core、wheel-only、
GitHub Evidence wheel-only与Starter jobs为`SKIPPED`。Workbench与E3 clean-install已SUCCESS，但不能与未完成cells拼成15/15。

所以直接failure identity是：

```text
PR512_ORIGINAL_PUBLIC_CI_ATTEMPT1_PYTHON310_NORMAL_JOB_TIMEOUT_CANCELLED
PR512_ORIGINAL_PUBLIC_CI_ATTEMPT1_PYTHON310_OPTIMIZED_JOB_TIMEOUT_CANCELLED
CONFIGURED_REVIEW_ATTENTION_45_MINUTE_CONTAINMENT_BOUNDARY_REACHED
REQUIRED_PYTHON_AGGREGATORS_FAILED_CLOSED
```

## 3. 时长对照与UNKNOWN边界

`.github/workflows/ci.yml`在base与candidate world都声明每个Review Attention cell：

```yaml
timeout-minutes: 45
```

base exact-main run `44909682401`的相同四格全部SUCCESS，job-level wall clock约为：

| World | Python / mode | Wall clock |
| --- | --- | ---: |
| base exact main | 3.10 normal | 1726s |
| base exact main | 3.10 optimized | 1583s |
| base exact main | 3.13 normal | 1518s |
| base exact main | 3.13 optimized | 1032s |

PR #512 final bytes的本地full Review Attention witness各报告715项；3.10 normal / optimized分别为2467.569s与2459.967s，
3.13 normal / optimized分别为2001.534s与2010.291s。CI中的3.13 cells仍在2036s与2278s完成；两个3.10 cells则在
2704s/2705s job-level wall clock处触及45分钟上限。

这些事实证明：现有45分钟outer containment budget对该exact candidate没有保留完成与清理余量，原资格前提已被真实world击穿。
它们尚不证明：

- Manifest 0.2语义、Schema、conformance或admission出现产品断言失败；
- GitHub runner、Python 3.10、candidate新增测试、既有suite的累积成本或某个runtime path是唯一slowdown根因；
- 提高timeout、拆分suite、优化测试构造、修改runtime或放宽oracle中的任一方案已经获得授权；
- 3.13成功、local PASS或base exact-main成功能够替代本attempt未完成的3.10结果。

因此分层结论是：

```text
original PR qualification          = CANCELLED / NOT_QUALIFIED
PR512 candidate                    = CLOSED / UNMERGED / NOT_QUALIFIED / NOT_FROZEN
candidate product regression       = NOT_ESTABLISHED
cancelled cell product result      = NOT_ESTABLISHED
45-minute containment counterexample = ESTABLISHED
lower slowdown cause               = UNKNOWN
```

## 4. 不能拼接、覆盖或重跑

以下身份必须并存：

1. PR #511完整授权资格链PASS；
2. PR #512 final local candidate witnesses PASS；
3. PR #512 Python 3.13两格SUCCESS；
4. PR #512 Python 3.10两格CANCELLED；
5. PR #512 required aggregators FAILURE；
6. PR #512 downstream jobs SKIPPED；
7. PR #512 closed/unmerged；
8. 本文仍只是新docs-only candidate。

```text
local full-suite PASS       != original gate PASS
base exact-main PASS        != candidate head PASS
Python 3.13 SUCCESS         != Python 3.10 SUCCESS
timeout annotation known    != lower slowdown cause known
later independent PASS      != erase PR512 CANCELLED
same source recreated later != PR512 qualification inherited
```

PR #512没有rerun，没有metadata edit触发second run，也没有合并。其candidate source与local evidence继续由failed head和独立evidence
root承担provenance；它们不得复制进本文冒充main事实。

## 5. 反例先检查前提，且局部必须反馈全局

本失败继续采用：

> 理论遇到反例，应当检查前提，而不是不断增加例外。

其机械含义是：

1. 不先把45替换成更大数字后宣称原模型仍正确；
2. 不把candidate增长视作可忽略例外，因为required gate已经不能完成；
3. 不以“只是CI预算”忽略它对全局资格链的阻断；
4. 不以“局部不等于全局”为由扩张到Manifest合同、global composition或R2–R6；
5. 不删测试、不接受部分PASS、不缩小oracle denominator；
6. 先资格化失败边界，再由fresh CONTROL LOOP比较test topology、真实时长、runtime构造成本与恢复余量，选择最小合法修正。

这同时落实目标连续性：修复动作必须保留已经成立的authorization、candidate语义边界与失败历史，并让完整R1资格真正前进；不能只把
某个红灯变绿却破坏原始证明义务。

## 6. 最小重开边界

当前只重开：

```text
PR512_ORIGINAL_PR_QUALIFICATION_BOUNDARY_ONLY
PUBLIC_CI_REVIEW_ATTENTION_45_MINUTE_CONTAINMENT_PREMISE_AUDIT
```

不重开doc316/doc317合同、doc435 carrier freeze、doc447 feasibility、doc448 authorization、Manifest 0.1、Provider、default composition、
persistence、public Review、Core Verdict或R2–R6。最小恢复顺序是：

1. 本docs-only failure-boundary audit完成自己的完整资格链；
2. 返回CONTROL LOOP，核对base/candidate四格时长、增长来源、当前workflow topology与恢复余量；
3. 只有新回路授予的最小边界才可修改workflow、test-support topology或implementation/test成本；
4. maintenance/correction若成立，PR #512仍保持失败历史；
5. Manifest implementation successor必须从maintenance/correction后的新exact main独立重建，取得新的head/tree/run/merge/readback资格；
6. 后继PASS不回填PR #512。

本文不预选修正方案，也不把`UNKNOWN`下层原因包装成已定位。

## 7. Retained evidence 与setup history

PR #512 evidence root保存original run终态、两个job末端栈、check-run annotations、PR close identity与全部local history。新增关键记录
SHA-256为：

```text
terminal run observation       a1691df62fa3d5027dbe8c222a0799a1965af355937d8756626c10ecbc72604f
Py3.10 cancellation forensics  ea156cdd1fe45bec72f9530774708237f645ce06142b9b7c2aae5f24ea740ed4
check-run annotations          eec19021e4af11f3e11b47d852e9bcf1690d5d61d89de1309a7ce5d6f8b7f933
tree-expression setup error    90f2fc7b710723fa6be0ea08c12b5be0945e13378e9871536b1aa10d31665478
log-count parser setup error   aa9f51333c7a59524c83df6178aa339eda888096b2dbe290ab19f789049e7f44
```

workflow filename 404、Actions API POST 404、long-poll h2 transport、PowerShell tree expression与log-count pipeline parser errors都保持
`NON_QUALIFYING / NONE`；后继正确read-only capture不删除它们。primary `audit.json`继续必须为
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 8. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/450-r1-review-derivation-manifest-0-2-original-ci-budget-failure-boundary.md
docs/milestones.md
```

`.github/workflows/ci.yml`、PR #512的11个candidate files、所有runtime/tests/fixtures/Schema、doc316–448、
`docs/project-state.md`与primary `audit.json`必须保持base bytes。

## 9. Qualification pipeline

final bytes必须完成exact four-file scope、UTF-8/LF/final-LF、links/fences/headings、required marker、PR/run/job/check-run/annotation、
closed/unmerged identity、unchanged workflow/runtime/tests/Schema、remote main、primary audit、`git diff --check`、read-only global/local hygiene及
Python 3.10.6/3.13.13 × normal/`-O` focused carrier witness。

```text
final failure-boundary docs bytes / declared local gates
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> fresh anonymous exact-commit AGENTS raw-byte observation
    -> independent PR512 / run / timeout / source-byte / retained-history reconciliation
    -> finite closeout
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

本文自己的PASS不能资格化、合并或冻结PR #512，也不能自动授权下一种修正。

## 10. 当前状态与停止线

本文只允许发布：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FEASIBILITY_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_PR512_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_CANCELLED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_ORIGINAL_PUBLIC_CI_BUDGET_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的全部门闭合后也只保存`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；必须返回CONTROL LOOP，不得按文档编号直接修改
workflow、重建implementation、恢复global composition或启动public Review/R2–R6。`proof_is_not_problem_solving = true`、
`local_not_global = true`、`target_continuity_over_local_correction = true`继续成立。R1完整闭合后的人类+AI全项目检查与未来开源能力组合仍是
独立后续目标。
