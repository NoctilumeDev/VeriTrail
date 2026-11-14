# R1 same-attempt continuity original Public CI timeout failure boundary audit

日期：2026-11-14

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_ORIGINAL_PUBLIC_CI_TIMEOUT_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@a41b8ba3575419e754099725b5e1616af6cd1af4`，tree
> `c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255`。
>
> 影响：`L0_DOCUMENTATION / ORIGINAL_GATE_AND_CI_CONTAINMENT_PREMISE_AUDIT_ONLY`。本文只保存PR #465 original
> Public CI attempt 1在Python 3.10 aggregated Windows lane触及55分钟job timeout后`CANCELLED`的事实、同runtime时长对照、未知下层原因与
> 最小重开边界；不重跑、不合并失败候选、不修改workflow、runtime、tests、oracle、合同或既有失败历史。

## 1. CONTROL LOOP 与两层失败坐标

PR #464把[private implementation候选](405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md)精确合入：

```text
base                    = b5ff07e03630d57060384883d28a49dc57bdf0df
head                    = b4fa42cc16b814f9d23e8c025bc4499dcb412084
tree                    = c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255
protected merge / main  = a41b8ba3575419e754099725b5e1616af6cd1af4
original Public CI      = 43034543495 / attempt 1 / SUCCESS / 11 of 11
exact-main Public CI    = 43040847982 / attempt 1 / SUCCESS / 11 of 11
exact-main Browser      = 43040847817 / attempt 1 / FAILURE
```

Browser Smoke失败发生在`Install Chromium`：Ubuntu mirror DNS解析失败，`apt`退出100，产品build/smoke没有启动，artifact count为0。
因此直接分类保持：

```text
EXACT_MAIN_BROWSER_SMOKE_CHROMIUM_INSTALL_DNS_SETUP_FAILURE
lower cause                    = UNKNOWN
candidate product regression   = NOT_ESTABLISHED
Subject failure                = NOT_ESTABLISHED
doc405 qualification           = MERGED / NOT_QUALIFIED / NOT_FROZEN
```

PR #465随后从未变化的exact main建立docs-only doc406 failure-boundary audit candidate：

```text
base         = a41b8ba3575419e754099725b5e1616af6cd1af4
head         = ffd09d2ac5bfd2b35f433a31b64c72158d396ab9
tree         = 9ef11a45990d75e4e208043288f4f2b4901e7caf
scope        = 1 commit / 4 docs files
PR state     = CLOSED / UNMERGED
```

该候选local final bytes曾通过Python 3.10.6/3.13.13 × normal/`-O`四格focused witness（各152项）、8/8 hygiene、exact
four-file validation与primary `audit.json` continuity；local qualification与73-artifact seal不能替代后继original gate。PR #465没有编辑
metadata、没有rerun，也没有形成第二个same-head run。

## 2. Original gate 的直接timeout事实

PR #465 original Public CI身份是：

```text
workflow run   = 43056337145
attempt        = 1
event          = pull_request
head           = ffd09d2ac5bfd2b35f433a31b64c72158d396ab9
status         = completed
conclusion     = CANCELLED
concrete jobs  = 8
artifacts      = 0
same-head runs = 1
```

`.github/workflows/ci.yml`在该exact candidate声明Python matrix aggregated lane：

```yaml
jobs:
  python:
    name: Python ${{ matrix.python-version }} on Windows
    runs-on: windows-latest
    timeout-minutes: 55
```

Python 3.10 job `130646682500`从`2026-11-11T16:14:32Z`运行到`17:09:37Z`，API终态为`CANCELLED`。其
`Run Review Attention contract tests`在1463秒后SUCCESS；随后`Run Review Attention contract tests with assertions disabled`运行1451秒，
在测试过程中收到`KeyboardInterrupt`并记录`The operation was canceled.`。GitHub check-run annotation同时明确给出：

```text
The job has exceeded the maximum execution time of 55m0s
```

所以直接failure identity不是泛化的`UNKNOWN cancellation`，而是：

```text
PR465_ORIGINAL_PUBLIC_CI_ATTEMPT1_PYTHON310_AGGREGATE_JOB_TIMEOUT_CANCELLED
CONFIGURED_PUBLIC_CI_PYTHON310_AGGREGATE_JOB_TIMEOUT_BOUNDARY_REACHED
```

Python 3.13、Workbench与E3 jobs已SUCCESS，四个下游required job只形成`SKIPPED`模板identity；它们不能与已完成步骤拼接成11/11。

## 3. 同runtime时长对照与UNKNOWN边界

PR #465只改四个docs文件；Review Attention runtime/test bytes与PR #464两个成功world相同。三次Python 3.10精确时长为：

| World | Job | normal | `-O` |
| --- | ---: | ---: | ---: |
| #464 original `43034543495` | 1958s / SUCCESS | 802s / SUCCESS | 791s / SUCCESS |
| #464 exact-main `43040847982` | 2215s / SUCCESS | 917s / SUCCESS | 912s / SUCCESS |
| #465 original `43056337145` | 3305s / CANCELLED | 1463s / SUCCESS | 1451s / CANCELLED |

这组观察机械证明：workflow中“55分钟outer containment budget必须为normal hosted-runner variance保留恢复余量”的前提，在本次真实runner
world中被反例击穿。它不证明：

- doc406文字或doc405 private implementation导致性能回归；
- `-O`测试自身产生assertion failure；
- GitHub runner、Windows、Python、某个test或某段runtime代码是单一根因；
- 调高timeout、拆分job、删减测试或重跑原run中的任一方案已经获得授权。

因此分层结论是：

```text
original PR qualification          = CANCELLED / NOT_QUALIFIED
doc406 candidate                   = CLOSED / UNMERGED / NOT_QUALIFIED
candidate product regression       = NOT_ESTABLISHED
cancelled step product result      = NOT_ESTABLISHED
containment premise counterexample = ESTABLISHED
runtime slowdown lower cause       = UNKNOWN
```

## 4. 既有PASS、FAIL与CANCELLED不得拼接

以下身份必须并存：

1. PR #464 original Public CI 11/11 SUCCESS；
2. PR #464 exact-main Public CI 11/11 SUCCESS；
3. PR #464 exact-main Browser Smoke setup FAILURE；
4. PR #465 local qualification PASS；
5. PR #465 original Public CI attempt 1 CANCELLED；
6. PR #465 closed/unmerged；
7. 本文作为新candidate仍未取得任何远端资格。

它们不能组合成另一个world的PASS：

```text
prior runtime PASS             != PR465 original gate PASS
local 152/152                  != required Public CI completion
Python 3.13 SUCCESS            != Python 3.10 SUCCESS
completed upstream steps       != 11/11
timeout cause known            != product result known
closed PR                      != failed gate repaired
later independent PASS         != erase PR465 CANCELLED
```

## 5. Retained evidence 与proof-facility history

PR #465原始失败证据保存在独立root；关键SHA-256为：

```text
cancellation classification  e9144a8162f18f951e7211837aab3787ad63bb3218808876f1639d0cb45cb638
103-artifact pre-close seal  de2052b4d8b87d5d5c06b42eb06acc9cf4ec06fa496e08e3d9cff0ae75c8cf71
post-close closeout          7474d92eda9d931bbbf5cd9d146a65e60e2e056e0bc05ffec0004a51f51d2743
113-artifact finite seal     8cd944a4e2c2d86f75429873b72f581e011690a7e41818b94153c7499a45734f
```

原root还保留workflow filename 404、hash wildcard、缺少repo context、absent-log inspection与PowerShell parser setup errors；它们全部是
`NON_QUALIFYING / NONE`，不覆盖最终抓到的GitHub run/job/check-run/annotation/log。本candidate的managed worktree创建与attach重试又因本
聊天超过100个attachment identity失败；两次都只影响Codex侧栏登记，不改变checkout或产品字节。

## 6. 反例先检查前提

本失败继续采用：

> 理论遇到反例，先检查前提、适用域与观察是否成立，而不是不断增加例外。

机械含义是：

1. 不把55分钟改成更大的任意数字后宣称原前提仍正确；
2. 不把偶发runner variance当成可忽略例外，因为required gate实际因此无法完成；
3. 不因同runtime先前成功就把本次timeout改写成PASS；
4. 不把timeout annotation已定位误写成下层性能根因已定位；
5. 不通过删测试、只跑normal、忽略`-O`或接受8个job来弱化oracle；
6. 不在failure-boundary audit中顺带修改workflow；先资格化失败边界，再由fresh CONTROL LOOP判断containment premise是否需要独立维护。

这也是局部与全局分离：本反例只击穿当前Public CI aggregate lane的资格前提，不自动推翻doc397合同或doc405语义；但它也不能因“局部”而在
全局资格链中被忽略。

## 7. 最小重开边界

当前只重开：

```text
DOC406_ORIGINAL_PR_QUALIFICATION_BOUNDARY_ONLY
PUBLIC_CI_AGGREGATE_PYTHON_WINDOWS_LANE_CONTAINMENT_PREMISE_AUDIT
```

不重开doc397合同、doc404授权、doc405 runtime semantics、旧Schema、public export、manifest、persistence、public Review、Core Verdict或
R2–R6。最小恢复顺序是：

1. 本docs-only failure-boundary audit以自己的final bytes完成完整资格链；
2. 返回fresh CONTROL LOOP，重新核对当前aggregate lane的测试总量、真实时长分布、恢复余量与required job topology；
3. 只有该回路证明现有containment premise不再成立并授予最小维护边界，才可另建独立workflow/test-topology maintenance；
4. maintenance不能复用PR #465 run或qualification，也不能把PR #464 Browser setup failure改写成已解决；
5. maintenance若成立，implementation failure-boundary recovery仍须从新的exact main独立重建并取得自己的完整资格；
6. 任何后继PASS只证明新world，不回填PR #465的`CANCELLED`。

本文不预选“提高timeout”“拆分lane”或“优化测试”中的任一方案，因为现有证据只建立premise counterexample，未建立下层唯一根因。

## 8. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/407-r1-same-attempt-continuity-original-public-ci-timeout-failure-boundary-audit.md
docs/milestones.md
```

`.github/workflows/ci.yml`、doc397、doc405、所有runtime/test bytes、fixtures、Schema、manifest、`docs/project-state.md`与primary
`audit.json`必须保持base bytes。

## 9. Qualification pipeline

final bytes必须完成exact four-file scope、UTF-8/LF/final-LF、links/fences/headings、PR #464/#465/run/job/check-run/annotation与workflow
timeout核对、closed/unmerged identity、unchanged workflow/runtime/doc397/doc405、remote main、primary audit、`git diff --check`、read-only
global/local hygiene及Python 3.10.6/3.13.13 × normal/`-O` focused unchanged-runtime witness。

```text
final failure-boundary docs bytes / declared local gates
    -> original PR required 11/11 gate
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent PR / run / timeout / source-byte / retained-history reconciliation
    -> finite closeout
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

本文自己的PASS不能资格化doc406或doc405，也不能自动授权workflow maintenance。

## 10. 当前状态与停止线

在本文自己的全部最后门闭合以前，只允许：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_EXACT_MAIN_BROWSER_FAILURE_BOUNDARY_AUDIT_PR465_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_TIMEOUT_CANCELLED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_ORIGINAL_PUBLIC_CI_TIMEOUT_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`local_not_global = true`与`post_r1_global_check_required = true`继续成立。本审计完整闭合后也只保存一个qualified history；必须返回
CONTROL LOOP，不得按文档编号直接修改workflow、重建doc406、冻结implementation或启动manifest/public Review/R2–R6。R1完整闭合后，仍须由
人类与AI共同执行独立全项目检查。
