# R1 public project-state projection 0.8 dual original-gate failure-boundary recovery audit

日期：2026-11-09

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_0_8_DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@6dd0b76184a8739e4930a517f18cb32488c459b3`，tree
> `fde358619660c7d6d86eaffa1718a9477389bc37`。
>
> 受审对象：PR #447 projection 0.8 candidate与PR #448 first failure-boundary audit candidate各自的original-gate failure，
> 以及PR #449仅对release-asset recovery proof facility成立的独立恢复资格。
>
> 影响：`L0_DOCUMENTATION / DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_ONLY`。本文不创建或资格化projection 0.8
> semantic bytes，不修改`docs/project-state.md`、runtime、tests、fixtures、workflow、download recovery tool、Release资产、Schema、
> Provider、Collector、P2/Core oracle、Verdict、既有frozen semantic bytes、manifest、Evidence、persistence、public Review或R2–R6。

## 1. CONTROL LOOP输入：#446的语义状态与两个未合入失败world

PR #446已经把[文档390](390-r1-application-level-unified-review-coverage-output-admission-private-implementation-freeze-qualification-recovery.md)
精确合入`main@f2ab7b78f86a057431cf5c8f4cbc3b0337338118`。original Public CI `42557756555`、exact-main Public CI
`42560991201`与Browser Smoke `42560991124`均attempt 1 SUCCESS（11/11、11/11、1/1）；fresh README/doc389/doc390
formal、AGENTS/milestones raw-byte observation、independent reconciliation与finite closeout全部成立。因此：

```text
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FREEZE_QUALIFICATION_RECOVERY_0_1_QUALIFIED_HISTORY
```

这项bounded private semantic freeze没有恢复global composition authority，也没有授权manifest、same-attempt Evidence continuity、
persistence、public Review或R2–R6。PR #443的`CANCELLED`、lower cause `UNKNOWN`与doc389 not-qualified history继续保留。

fresh CONTROL LOOP随后建立projection 0.8 candidate PR #447：

```text
base         = f2ab7b78f86a057431cf5c8f4cbc3b0337338118
head         = 1e554754d43e3b2bf0d6e7780852537857399797
tree         = 521c75df9908a7c6d1b30836da8d4c23f22d2801
scope        = 1 commit / 5 docs files
original run = 42568657029 / attempt 1 / FAILURE
state        = CLOSED / UNMERGED / NOT_QUALIFIED / NOT_FROZEN
```

旧`docs/391-r1-public-project-state-projection-successor-0.8-contract.md`只存在于该closed PR world，从未进入main。它的local
qualification、内容摘要、project-state bytes或未来相同文字不能继承original-gate qualification。

为保存#447 failure而建立的PR #448也在自己的original gate失败：

```text
base         = f2ab7b78f86a057431cf5c8f4cbc3b0337338118
head         = 5dd1933fe57591058f6dafcd572535b5ecac5848
tree         = bad7b851e5f37400a824f40c42bb745913d6f5cc
scope        = 1 commit / 4 docs files
original run = 42576411794 / attempt 1 / FAILURE
state        = CLOSED / UNMERGED / NOT_QUALIFIED / NOT_FROZEN
```

旧`docs/392-r1-public-project-state-projection-0.8-original-gate-failure-boundary-audit.md`同样只存在于closed PR world，从未进入
main。因为当前main最高已合入文档仍是doc390，本文合法使用主线doc391；这不是删除、覆盖或改写上述两个未合入历史身份。

## 2. PR #447 original-gate failure identity

PR #447的required Public CI没有rerun。三个required job在冻结Release资产delivery path失败：

| job | job id | 已完成事实 | 直接失败 |
| --- | ---: | --- | --- |
| E3 0.2 release download acceptance | `129000700153` | Core wheel与Starter wheel摘要已验证 | Starter 0.2.0 sdist连续7次HTTP 504，120秒multi-asset恢复预算耗尽 |
| Python 3.13 on Windows | `129000700027` | Core/GitHub Evidence/Review Attention normal/`-O`均SUCCESS | Core 0.12.2 wheel连续5次HTTP 504，默认60秒预算耗尽 |
| Python 3.10 on Windows | `129000700095` | 同一产品测试边界均SUCCESS | Core 0.12.2 wheel连续4次HTTP 504，默认60秒预算耗尽 |

Workbench job `129000700069` SUCCESS；四个依赖job group因required predecessor未全部成功而SKIPPED。不同lane、不同asset与不同
Python world的PASS不能拼成original Public CI通过。失败log/capture、terminal与post-close SHA-256为：

```text
E3 log      acd6bb21ac909cb33c69baedf3debf0f508721086fa0be25f6cff03835efd109
E3 capture  3079ca5aeb8e592a5b30d2bd6fc400bdd4b3775367aa3a5cc2d63163e8351336
Py3.13 log  2e4a4047ee131853811c9667507c11bf3eae6cea68a0abb3fd3f54b0d486e3c0
Py3.13 cap  01bc04b9bb8da442732523977e5f4016b5369af5ca90ee349a689692dd50ee35
Py3.10 log  9d7d10b7b73a581e6fca2058e8e72f2acce9354b442385dfc09a819f9ec6ba28
Py3.10 cap  bc700e80e200bc152ee956b2590864402aa5c2fb3d7719c9b04cd244c19df276
terminal    d6d4956530e7bd208a0ea8318598e8f7ebe35da1fe3cc434c50ed6cddaf96393
post-close  f5877883ea5723ff3068f43963cdbcd2786e888b9475c124ebf728d52c9af8df
```

fresh installed-product readback、independent reconciliation与qualifying closeout没有启动。projection 0.8 bytes因此保持closed
PR-only history；projection 0.7继续是current frozen mainline projection。

## 3. PR #448 original-gate failure identity

PR #448同样没有rerun。它只修改四份文档，但original Public CI `42576411794` attempt 1在required Python 3.10 job
`129025031742`的`Download the frozen E1 entry-layer release assets`步骤失败。此前Core、Authoring Skill、GitHub Evidence、Review
Attention、Starter 0.2.0 declared lane、build与Artifact upload均SUCCESS；E3、Python 3.13与Workbench required jobs也SUCCESS。

E1 assets循环中Starter 0.1.0 wheel曾先收到一次504再成功。随后Starter 0.1.0 sdist记录8个`outcome=retry`的HTTP 504，
并由第9个HTTP 504产生最终bounded-budget failure；120秒恢复预算不足以承担下一次retry，下载器fail closed。旧failure record最初
把它写成8次总计，append-only correction保留原记录并更正为9次，不改变失败identity或归层：

```text
failed step log SHA-256       be3bdc74c4589a463e1fcef6419104a04f106106b5c602333ceaaf9809c4d7f1
failed job log SHA-256        cc23571c25b18bb9e8ae20c75963d52dc0fa64850828c711db7fd28bd187dbcc
original failure record       fca2720332a6d21e50545bebddc27785f475c31848eaf4396e7ce575f30fd984
attempt-count correction      1ea2fcee1efd6314de6affc137f308c76830b05ac9fd13d4e46e4ff0ef0b5f20
post-close failure identity   155163b58ce14cd663606bbbffe3a2eadd01daec7d36f75d80c01f79725c4ca3
```

PR #448已经关闭且未合并，fresh readback没有启动。因此它既没有使#447 failure boundary成为qualified history，也没有形成新的
mainline state。其local PASS、doc392内容或未来后继PASS都不能回填run `42576411794`。

## 4. PR #449只资格化proof-facility recovery

两个相邻original attempts在相同Release asset delivery layer暴露旧恢复窗口对共享外部瞬时失败的容量不足。fresh CONTROL LOOP只
授权独立proof-facility maintenance，不修改产品、测试命令、Release identity、digest、retryable status集合、backoff、per-request
15秒上限、owned partial cleanup、required gate、product oracle或任何R1 semantic authority：

```text
default absolute recovery budget = 60 -> 120 seconds
E1/E3 multi-asset lane budget    = 120 -> 240 seconds
backoff                           = 2 / 4 / 8 / 16 seconds, unchanged
digest equality                   = required, unchanged
permanent error behavior          = fail closed, unchanged
```

PR #449的identity与qualification为：

```text
base                 = f2ab7b78f86a057431cf5c8f4cbc3b0337338118
head                 = 4a07cc8e406e0a20b5e1a38a2659b7a59c237cc0
candidate tree       = fde358619660c7d6d86eaffa1718a9477389bc37
merge / exact main   = 6dd0b76184a8739e4930a517f18cb32488c459b3
scope                = 1 commit / 3 proof-facility files
original Public CI   = 42585159817 / attempt 1 / 11 of 11 SUCCESS
exact-main Public CI = 42590826814 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke        = 42590826778 / attempt 1 / 1 of 1 SUCCESS
```

attempt 1 formal full matrix因四格并发竞争本机资源且漏掉插件source root，产生相同3项runtime-resource failure与1项
`veritrail_github` import error；该world按原identity保留为setup/contamination，不作产品结果。修正后的attempt 2串行四格、显式
Core/Starter/GitHub/Review roots，每格focused 15/15与full 497/497均PASS。local、original、exact-main qualification SHA-256为：

```text
e76850907e40c9f6e746244e98924eb093e81d4959503b77f3f365b839136428
dfb43c68568cab8740260ee9b0cdfacaae4026d25cf4250db711fb656adb1e22
f5462dc1eb82ccdbb01b3c07933a0435c759c09d8e54fd8cd32ff9b453405b24
```

fresh exact-main对三个changed path的anonymous raw/API/Git字节观察、independent reconciliation、combined manifest、102-artifact
closeout与finite integrity SHA-256为：

```text
8fb76de113d296aa0ee9c1f0f6b3145498c73f543227f4326fa9c8f3b7ca96d6
e910713f4005893f42d6af60507f7b897cb20804efade75ac380017cae76ecf8
df575ddeb0b327ce371825abfc662281badc9433387e1fec1b1da4fad18f8683
3b6aa81a99950eee49e2eff5058f381d7c9a49b082547269fe7527716245073d
c1d701a9f9df8802aee7f803e18963ebcf3153958efc2e793b38cc377dcabf04
```

GitHub API EOF、concurrent attempt、path omission、validation literal mismatch、cache cleanup policy rejection与worktree attachment cap
均按原identity保留。#449的qualification effect只有`MAINTENANCE_EXACT_MAIN_QUALIFIED`：它证明后继required gates能够在不弱化
oracle的情况下闭合，但不把#447/#448改写成PASS，不资格化doc391/doc392旧字节，也不解释lower cause `UNKNOWN`。

## 5. 归层、资格与责任边界

当前证据只允许：

```text
#447 original required gate failure          ESTABLISHED
#448 original required gate failure          ESTABLISHED
observed failure layer                       FROZEN_RELEASE_ASSET_DELIVERY_PATH
observed HTTP status                         504 / RETRYABLE
bounded recovery exhaustion                  ESTABLISHED
download tool fail-closed behavior           CONFORMING
wrong bytes accepted                         NOT_OBSERVED
asset digest mismatch                        NOT_OBSERVED
projection candidate semantic regression     NOT_ESTABLISHED
failure-audit candidate semantic regression  NOT_ESTABLISHED
Subject failure                              NOT_ESTABLISHED
shared single root cause                      NOT_ESTABLISHED
GitHub/proxy/shared-egress/network cause      UNKNOWN
proof-facility recovery on #449 exact world  QUALIFIED
```

#449改变了后继证明设施的capacity，但没有改变两个旧attempt发生过什么。它也没有证明旧预算“错误”；旧下载器在其冻结边界内正确
fail closed。只有新的CONTROL LOOP可以从新exact main判断projection lag与0.8 successor是否仍需施工。

## 6. 问题连续性与最小合法后继

```text
original engineering problem = 维护准确、自洽、可公开观察且不越权的bounded current-state projection
current proof obligation      = 只资格化#447/#448 failure identities、#449 recovery effect与最小后继责任
applicability world           = exact main 6dd0b761/tree fde3586 + 两个retained attempt + 本audit自己的final bytes/资格链
proof_is_not_problem_solving  = true
```

本audit将来qualified只意味着dual original-gate failure boundary成为可消费历史；它不等于projection 0.8已存在、0.8内容正确或公开
projection问题已经解决。恢复必须继续串行：

1. 本docs-only audit先取得自己的完整资格，只发布failure/recovery history；
2. publication形成新事实后返回CONTROL LOOP，复核projection 0.7、#446 frozen state、#447/#448 retained failures、#449 recovery与
   当前公开projection lag；
3. 只有0.8仍必要且没有新反例时，才从新的exact main独立重建versioned projection candidate；
4. 旧doc391/doc392、旧project-state bytes、旧commit或旧attempt不得cherry-pick、空提交重放或继承资格；
5. 新candidate必须取得自己的base/head/tree、source binding、original attempt、protected merge、exact-main gates、fresh readback与
   independent reconciliation；
6. 若本audit自己的required lane再次失败，保留新identity并重新判断最小failure/proof-facility boundary，不能弱化oracle。

## 7. 本audit自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/391-r1-public-project-state-projection-0.8-dual-original-gate-failure-boundary-recovery-audit.md
docs/milestones.md
```

`docs/project-state.md`、doc375–390、runtime、tests、fixtures、workflows、download policy、Release assets、Schema、Provider、Collector、
P2/Core oracle、Verdict与全部frozen semantic bytes必须保持`6dd0b761…` base bytes。final bytes至少通过exact四文件scope、UTF-8
without BOM、LF/final LF、links/fences/headings、required markers、#447/#448 retained failure摘要、#449 exact qualification、
`git diff --check`、global/local hygiene、focused Python 3.10.6 / 3.13.13 × normal / `-O`四格及primary `audit.json` continuity。

pre-record local qualification已经对四文件scope、871个local links、Markdown、两个retained failure、maintenance closeout、
`docs/project-state.md`不变与primary audit continuity完成PASS；release-asset recovery focused matrix在Python 3.10.6 / 3.13.13 ×
normal / `-O`四格各15/15 PASS，global/local hygiene 8/8 PASS。pre-record local qualification与test matrix SHA-256为：

```text
685f8c6dcf149443faa29ca7b8f4ed18cc00175498dab3d5c09639d3d250ed5a
6cdd34c335d4778907b701e76a1d17f1f5957e240beef8df40a09c2b42bb54fc
```

first local validator遗漏untracked doc391的scope setup error已按`NON_QUALIFYING_NONE`保留。这些PASS属于写入本段以前的
pre-record bytes；final bytes必须重新运行相同local qualification，并由外部evidence seal固定，不能继承pre-record资格。

```text
final docs-only dual failure/recovery audit bytes + declared local gates
    -> original PR required gates (new attempt; no rerun of #447/#448)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source / failure / recovery / problem-identity reconciliation
    -> finite closeout / integrity
    -> DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止，不重复已有PASS。

## 8. 当前状态与停止线

全部最后门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_PR447_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FAILURE_AUDIT_PR448_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_RELEASE_ASSET_RECOVERY_PROOF_FACILITY_SUCCESSOR_V2_PR449_EXACT_MAIN_QUALIFIED
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_NOT_MAINLINE_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_0_8_DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED / QUALIFIED_HISTORY`。projection 0.7继续是
current frozen mainline projection；PR #447/#448、旧doc391/doc392、两个original failures、所有setup errors与lower `UNKNOWN`均不
回填。随后必须返回CONTROL LOOP，不能按文档编号自动重建projection或启动任何runtime seam。
