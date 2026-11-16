# R1 M10 repeatability failure-observation correction 0.1 implementation 冻结发布

日期：2026-11-16

> 条件化状态目标：
> `R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@bb2e43701315d464a49ed84471e2aa967dbd77d2`，tree
> `6e6ae528839948ad02b44e3641818f135298be16`。
>
> 上游：[failure-boundary audit](421-r1-m10-repeatability-exact-main-failure-boundary-audit.md)、
> [feasibility audit](422-r1-m10-repeatability-failure-observation-feasibility-audit.md)、
> [authorization publication](423-r1-m10-repeatability-failure-observation-correction-authorization-publication.md)与
> [implementation candidate](424-r1-m10-repeatability-failure-observation-correction-implementation-candidate.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改test proof facility、runtime、public payload、Browser collector、
> oracle、timeout、retry、workflow、Schema、Verdict、carrier、Manifest、global composition authority或任何frozen contract。

## 1. CONTROL LOOP与本publication的唯一职责

PR #481 exact-main Public CI `43783429314` attempt 1在M10 repeatability witness中观察到
`ERROR / COLLECTOR_ERROR / FAIL`，Browser private trace为空，lower cause保持`UNKNOWN`。该run没有rerun；doc420保持
`MERGED / NOT_QUALIFIED`。doc421只资格化失败边界，doc422只证明未来首败可以透明保存same-attempt lower facts，doc423只发布
test-only A–J施工权；这些层次均没有回填旧attempt。

PR #486已经把doc424的test-only implementation candidate精确合入主线，并完成自己的original gate、protected merge、new
exact-main双门、fresh installed-product observation、independent reconciliation与finite closeout。该链闭合后doc424最多是：

```text
IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
```

fresh CONTROL LOOP复核远端main、开放PR、doc421–424、当前test bytes、保留首败、authority ceiling与primary `audit.json`后，没有发现
新事实击穿test-only correction 0.1的exactly-once、same-result/exception、bounded projection或fail-closed边界。当前最小合法seam只是在
新的docs-only完整资格链中发布`FROZEN`。本文不把改善未来失败可诊断性偷换成旧failure根因已知、runtime已修复、carrier已存在、global
composition authority已恢复或原工程问题已经解决。

## 2. Exact implementation qualification坐标

实现候选坐标为：

```text
PR                   = #486
base                 = e9191b14bfc9d5848b30ee07f6765fcebfb23adc
head                 = 6e4b680cb28c3a974e71482a90626122964b3419
ordinary merge       = bb2e43701315d464a49ed84471e2aa967dbd77d2
candidate/merge tree = 6e6ae528839948ad02b44e3641818f135298be16
diff                 = 1 commit / 5 files
```

original Public CI `43832893740`与exact-main Public CI `43838439457`均attempt 1为15/15 SUCCESS；Browser Smoke
`43838439528` attempt 1为1/1 SUCCESS，没有rerun。original qualification、protected merge与exact-main dual-gate evidence
SHA-256分别为：

```text
5d8dbd6e4e960c4553a7e37d7dc96d3a9945e6e01d1a02e3cadfe30cc9ba975b
11475665cee6ef3aa78006e29cc70e2679ff2ad4da3585b196b492ee317e4470
12854be2ff8c4b09065024b0770c4405635fa3db51c6db3fb342d7e59004f0e2
```

implementation test blob SHA-256为
`69d7a4a44fb26d0500b94e261c22c342e7c4fae85edd9d1d46039e3a3643747c`；doc424 full-file SHA-256为
`b2d64991a4df578abd9a5c7ea544f12b2985ddad9e3822232a349744fbc1d790`。本publication不修改这两个bytes。

## 3. Fresh installed-product observation与独立reconciliation

fresh detached worktree只认`main@bb2e437… / tree 6e6ae52…`。README、doc423与doc424各自唯一diagnostic均为
`DIAGNOSTIC_ONLY_NON_QUALIFYING / Render COMPLETE / HTTP 200 / marker=1`；各自唯一formal均为
`FORMAL_READBACK_PASS / API+Render COMPLETE / HTTP 200 / marker=1 / Core PASS`。AGENTS与milestones各自唯一anonymous
raw-byte formal均证明raw/API/exact-Git全字节一致、HTTP 200与marker存在。没有复用旧PASS。

proof facility构造阶段第一次PowerShell target-marker计数表达式解析失败；该identity以
`TARGET_MARKER_COUNT_POWERSHELL_PARSER_SETUP_ERROR / NON_QUALIFYING_NONE`永久保留，记录SHA-256为
`71b463b7dd42a6708028bacaee382893e6e2dbe458704dac5cea139ca39143b5`。它没有启动产品观察，后继正确表达式不删除第一次事实。

independent reconciliation、116-artifact finite closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
f2a66155968ff435ad03c502f820a09d676690bcb85b1ced1319ad97781971c8
92e69a33e0eb8aadd2d4c149584287ba9c455043e80b97de96907979a4da5466
e92e37832e2dea76a41464ad668c8cdb64031476cc91689627a1304f3f6a081f
a4888fd6f8f92ad09d5c39babe08f2903d382032dd84352db3e4aceb97256e9e
```

因此doc424取得exact-main/readback资格，但它仍不是冻结状态；本publication必须取得自己的fresh Plan/session/Evidence与完整资格链。

## 4. 冻结对象与proof strength

本文若完成自己的资格链，只冻结doc423/424限定的test-only failure-observation correction 0.1：

1. `_BootstrapAttemptObserver`只在M10 repeatability proof facility中透明、恰好一次调用原
   `veritrail.cli.run_bootstrap_bundle`；
2. original返回时保存同一个result的bounded deterministic JSON-safe projection并返回同一对象；original抛异常时保存test-boundary
   type/message并重抛同一异常；
3. projection只读取同一attempt result内已经存在的public execution/verdict、lifecycle event/node、resource/subject completion、workspace
   release、Browser Evidence completion/error与既有Browser private exception trace；
4. projection不回读临时目录、外部文件、clock、log或network，不进行第二次产品执行，且固定event/node/Browser/text/diagnostic上限；
5. foreign result、duplicate call、replacement、unbounded output与diagnostic自身失败继续fail closed；
6. 原exact expected set、status、Verdict、cleanup、真实repeatability/subject-drift witnesses与runtime/public bytes保持不变。

这只证明固定test proof-facility边界在Python 3.10.6/3.13.13 × normal/`-O`及声明的current-source world中取得资格。它不证明
PR #481 failure的底层原因、repository truth、runtime correctness、carrier/Manifest consumer authority、全仓Review完整性或最终用户问题已经
解决。

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
global_composition_authority_restored       = false
```

## 5. 必须继续保留的non-success与UNKNOWN

后继PASS不得删除、改名或解释以下identity：

- PR #481 exact-main Public CI `43783429314` attempt 1 failure、failed log/record、0 failed Evidence Artifact与lower cause
  `UNKNOWN`；
- doc420 `MERGED / NOT_QUALIFIED`与此前subject-drift/current-world历史；
- doc424预资格的pytest缺失、source-root缺失、managed-worktree attachment cap与历史错误模块路径只读probe；
- implementation readback的target-marker PowerShell parser setup error与expected stdout self-capture mismatch；
- 本publication CONTROL LOOP中的unquoted `HEAD^{tree}`、PowerShell pipeline、wrong reconciliation filename、wrong workdir与worktree
  registration attachment-cap setup errors；
- 所有更早FAIL、ERROR、CANCELLED、setup failure与UNKNOWN。

这些事实分别属于自己的exact coordinate；本publication不能把它们拼接成另一world的成功或失败解释。

## 6. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc421–424、
`tests/test_bootstrap_run_cli.py`、runtime、fixtures、workflows、Schema、Provider、Collector、public export、Core oracle与全部frozen semantic
bytes必须保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、required markers、
doc421–424/test blob与PR #486 qualification evidence、全部retained failures、Python 3.10.6/3.13.13 × normal/`-O` bounded focused
witness、`git diff --check`、read-only global/local hygiene及primary `audit.json` continuity。implementation full matrix属于已资格化的doc424
exact source world；本publication不重新解释它。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
  -> original publication PR Public CI 15/15, attempt 1, no rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc424 / 本文 Public Render
  -> fresh AGENTS / milestones / tests/test_bootstrap_run_cli.py raw+API+exact-Git byte observations
  -> independent Core / source-byte / problem-identity / retained-history reconciliation
  -> finite closeout and integrity
  -> target R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可复用doc424 world；diagnostic不计入资格，任何non-success必须保留原identity并停止。
产品readback必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令使用
`http://127.0.0.1:7897`。本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 7. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`...IMPLEMENTATION_FROZEN` target成为事实。随后必须从新的exact main返回CONTROL LOOP，重新审计
carrier、global composition authority、language-support persistence与剩余R1；不得按文档编号自动启动任何一个。R1完成以后必须由人类与
AI共同执行独立全项目检查。
