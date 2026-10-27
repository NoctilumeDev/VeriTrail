# R1 Workbench Vitest/undici maintenance 资格恢复候选

日期：2026-10-27

> 状态：`R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_QUALIFICATION_RECOVERY_CANDIDATE`。
>
> 坐标：`main@c8503321934a8f65fc8744dc503cb1d476ab28a2`，tree
> `739c9ed21cb5dcada0a66c6de651edc80665a768`。
>
> 上游：[Fact→Coverage exact-input successor合同冻结发布](322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md)
> 与[maintenance exact-main资格失败边界审计](324-r1-workbench-vitest-undici-maintenance-exact-main-qualification-failure-boundary-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文建立一份对既有失败历史承担新增责任的独立maintenance
> recovery candidate；不修改WorkBench/Core runtime、tests、fixtures、workflow、required lane、timeout、oracle、Schema、Coverage、
> manifest或persistence，也不把PR #372或PR #373补写成通过。

## 1. CONTROL LOOP 与新增事实

第一次Fact→Coverage private implementation authorization PR #372因Vitest 4.1.11与undici 7.30.0的五个advisory关闭且未合并，
保持`CLOSED / UNMERGED / NOT_QUALIFIED`。独立maintenance PR #373只修改`web/package.json`与
`web/package-lock.json`，把Vitest/`@vitest/mocker`更新到4.1.12、undici更新到7.30.1；它的original Public CI
`40474320234` attempt 1为11/11 SUCCESS，随后精确合入：

```text
merge = 5aeb53eeb0cca2dc92175fb5dfe4521388dca67a
tree  = 96ff0ce193799760c41676404f1d33af63652ba9
```

该merge的Browser Smoke `40478059772` attempt 1为1/1 SUCCESS，但exact-main Public CI `40478059827`
attempt 1在Python 3.10 required Core job `122101107016`观察到既有M10正向fixture的expected verdict `PASS`、actual
`FAIL`，run以3 SUCCESS / 1 FAILURE / 4 SKIPPED终结。日志和Artifact没有保留decisive assertion或临时Bundle，因此precise
cause仍只能是`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`。PR #373保持`MERGED / NOT_QUALIFIED`；没有启动installed-product
readback，也没有rerun。

[文档324](324-r1-workbench-vitest-undici-maintenance-exact-main-qualification-failure-boundary-audit.md)随后只冻结该失败的identity、
qualification effect与recovery seam。PR #375 candidate为：

```text
base = 5aeb53eeb0cca2dc92175fb5dfe4521388dca67a
head = 3604ef7a6316317212dd026f08e5346fa271357b
tree = 739c9ed21cb5dcada0a66c6de651edc80665a768
```

第一次original Public CI `40482098220` attempt 1因新的pull_request事件触发concurrency cancellation而终止；它保持
non-qualifying。独立第二次pull_request事件run `40482288836` attempt 1完成11/11 SUCCESS。PR随后精确合入
`main@c8503321934a8f65fc8744dc503cb1d476ab28a2`；new exact-main Public CI `40486037853`与Browser
Smoke `40486037792`均为attempt 1 SUCCESS，分别11/11与1/1。

fresh anonymous installed-product README、doc324、milestones为3/3 qualifying PASS。milestones formal #1因匿名GitHub
API预算耗尽以`FORMAL_READBACK_ERROR`终结并永久保留；真实reset后formal #2 PASS，不覆盖前一身份。independent
reconciliation与151-artifact finite closeout分别为：

```text
ebe07c9fd593d1f0c5d50d90677f6499352ad50c0169a14ee8f891f2b7d8915c
9bc218b6f52b6758f0b53dbb76ee0d063bc247254aedc8614894861fe59b05f2
```

因此failure boundary现为`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。这里形成两项相对PR #373的新事实与责任：

1. 在保持Core/Workbench runtime、tests、fixtures、workflow、required lane、timeout与oracle字节不变的后继docs-only world中，
   required gates完成，证明恢复不需要弱化产品门；
2. 后继maintenance recovery必须同时对账#373 exact-main失败、其`UNKNOWN`边界、PR #375 cancelled predecessor、doc324的
   完整资格链与自己的新exact world，不能只重放PR #373。

后继成功不解释#373为什么失败，也不把#375 PASS回填#373。它只使一份具有不同文档字节、新base/head/tree与新增资格责任的
recovery candidate成为合法。

## 2. failure identity 与恢复资格严格分离

PR #373失败identity继续固定为：

```text
exact-main run = 40478059827 attempt 1
failed job     = 122101107016
failed test    = test_catalog_accepts_public_m10_outcomes_and_isolates_a_corrupt_copy
expected       = PASS
actual         = FAIL
precise cause  = UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT
subject failure / candidate regression = NOT_ESTABLISHED
```

本文不借后继PASS推导该attempt“本应通过”，不把scope disjoint解释成qualification exemption，也不把`UNKNOWN`升级成任一
Subject、Chromium、socket、port、resource、fixture、timing或Core runtime根因。恢复的是**新candidate取得资格的可能性**，
不是旧candidate的资格。

任何reconciliation必须并列保留：

```text
#372 closed / unmerged / not-qualified authorization world
+ #373 merged / exact-main failed maintenance world
+ doc324 qualified failure-boundary history
+ current recovery candidate own world
```

四者不能拼接成一个attempt，也不能由相同dependency bytes继承另一world的authority。

## 3. 当前exact main重新核验dependency事实

本文在`main@c850332…`建立fresh local evidence root，重新执行`npm ci`、精确dependency tree、Workbench tests、lint、build
与官方registry advisory audit。观察为：

```text
Node.js                    = 24.14.0
npm                        = 11.9.0
Vitest                     = 4.1.12
@vitest/mocker             = 4.1.12
undici                     = 7.30.1
Vite                       = 8.2.4
Workbench tests            = 14 files / 179 tests PASS
lint                       = PASS
type-check + production build = PASS
official npm audit         = 0 advisories
```

第一次未指定registry的`npm audit --json`命中主机默认`https://registry.npmmirror.com`，该镜像不实现
`/-/npm/v1/security/advisories/bulk`并返回HTTP 404。它作为
`NPM_AUDIT_DEFAULT_REGISTRY_SETUP_ERROR / qualification effect NONE`保留；随后只对该命令显式指定
`https://registry.npmjs.org`，没有修改全局npm配置，得到零advisory正式观察。设施ERROR与正式PASS并存，前者不能被删除或
重解释为advisory结果。

这些本地结果只证明当前candidate的exact dependency/runtime witness仍成立；它们不回填PR #373，也不替代本candidate自己的
original PR、protected merge、new exact-main gates或installed-product readback。

## 4. recovery candidate新增的qualification responsibility

相对PR #373，本文新增的不是dependency版本，而是资格责任：

1. source、local evidence与最终readback绑定`c850332…`以后形成的独立exact world；
2. 独立复算Vitest/`@vitest/mocker` 4.1.12、undici 7.30.1、lockfile integrity与零advisory；
3. 独立对账#373 failed run/job/test、`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与未启动readback边界；
4. 独立对账PR #375的cancelled predecessor、qualifying original run、exact-main双门、3/3 fresh readback、reconciliation与closeout；
5. 自己的original PR与new exact-main required gates必须各自通过，任何non-success保留原identity；
6. fresh installed-product观察只能在自己的exact-main双门闭合后启动；
7. 后继PASS只能支持本文，不得回填#372/#373或消除#373失败。

因此当前变更不是空提交、retry-until-PASS或PR #373重放，而是一份对qualified failure history承担新增责任的独立candidate。

## 5. 禁止的推论

即使本文最终取得资格，也不能推出：

```text
#372或#373其实PASS
UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT已经解释
required Core lane、oracle、timeout或workflow可以放宽
Fact→Coverage successor private implementation已经授权或开始
Coverage producer已经实现
manifest successor、Evidence carrier或persistence已经选择
public Review、post-R1 Benchmark或R2-R6已经启动
```

若本文自己的required gate再次失败，必须保留新world并重新执行CONTROL LOOP；不得以已存在failure history为由自动创建第三个
candidate、rerun失败run或缩小required denominator。

## 6. 当前裁决与authority ceiling

| 问题 | 裁决 |
| --- | --- |
| Fact→Coverage exact-input successor 0.2合同是否frozen | **是** |
| #372 authorization失败是否永久保留 | **是** |
| #373 exact-main failure是否永久保留 | **是** |
| doc324 failure boundary是否qualified | **是** |
| required product oracle是否需要修改 | **否** |
| 当前exact dependency与零advisory是否重新观察 | **是，fresh local witness** |
| 当前candidate是否相对#373增加资格责任 | **是** |
| Fact→Coverage private implementation是否已授权或开始 | **否** |

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_372_CLOSED_UNMERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_ADVISORY_MAINTENANCE_MERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_PUBLIC_CI_FAILED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDITED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_QUALIFICATION_RECOVERY_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

## 7. 本candidate资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/325-r1-workbench-vitest-undici-maintenance-qualification-recovery.md
docs/milestones.md
```

`web/package.json`、`web/package-lock.json`、docs/321–324、Core/Workbench runtime、tests、fixtures、workflows、Schema、
Policy/Profile、Coverage、manifest与persistence必须保持`c850332…` base bytes。final bytes至少完成四文件scope、UTF-8 without
BOM、LF/final LF、links/fences/headings、required markers、dependency/lockfile与upstream failure-history continuity、
`git diff --check`、read-only hygiene、fresh `npm ci`、exact dependency tree、tests/lint/build与official-registry audit。

```text
final docs-only recovery candidate bytes / declared local gates
    -> original PR required gates
    -> continuously authorized exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc324 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / dependency / identity / retained-failure / failure-boundary reconciliation
    -> MAINTENANCE_QUALIFICATION_RECOVERY_AUDITED becomes qualified history for this candidate only
    -> return CONTROL LOOP
```

全部门闭合以前只能写candidate状态。闭合后最多允许fresh CONTROL LOOP重建独立docs-only Fact→Coverage private implementation
authorization publication；不得自动修改runtime、创建Coverage producer、选择manifest/Evidence/persistence或启动public Review、
post-R1 Benchmark、R2–R6。
