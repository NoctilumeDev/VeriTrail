# R1 M10 repeatability failure-observation feasibility audit

日期：2026-11-16

> 候选状态：`R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@5b15c715f6da16153a37025d5477bcf53b4b4c8c`，tree
> `ddac2c0f17094aed9300b73f6ea599879ee51a72`。
>
> 受审问题：PR #481 exact-main Public CI `43783429314` attempt 1中的M10 repeatability首败，及其
> first-failure observation/retention seam。
>
> 影响：`L3_SYSTEM_DIAGNOSIS + L1_TEST_PROOF_FACILITY + L0_DOCUMENTATION /
> READ_ONLY_FEASIBILITY_AUDIT_ONLY`。本文不修改runtime、tests、fixture、Browser collector、timeout、retry、workflow、
> Schema、Verdict、doc420、carrier、Manifest、persistence、public Review或R2–R6。

## 1. CONTROL LOOP与qualified起点

[文档421](421-r1-m10-repeatability-exact-main-failure-boundary-audit.md)的candidate精确绑定：

```text
base    = 2a9a2af4221175064ba4e9cd7a424472804df985
head    = 26154d3153c8e141392b78f2ea8b2fbe79010b3c
tree    = ddac2c0f17094aed9300b73f6ea599879ee51a72
commits = 1
files   = 4
```

PR #483 original Public CI `43788645830` attempt 1为15/15 SUCCESS；protected exact-head merge形成本文构造坐标，tree保持
`ddac2c0f…`。new exact-main Public CI `43792414561`与Browser Smoke `43792414586`均attempt 1 SUCCESS。

fresh exact-main readback只认`5b15c715…` world。README/doc420/doc421各自唯一formal Render为`COMPLETE / PASS`；AGENTS与
milestones各自唯一raw/API/exact-Git byte observation逐字节一致。第一次readback root因plan ID超过Core 64-character bound而在产品采集以前
终结，保留为setup failure；fresh root用缩短identity重新取得全部PASS。independent reconciliation attempt 1又因doc421 marker multiplicity
proof target错误终结，attempt 2只修正expected count后PASS，没有重复任何产品PASS。

最终identity为：

```text
independent reconciliation = d55e5a2915665da5d9fe1e651b18860b8b5f0046dbb37fb49f09ac265f90d5b5
125-artifact closeout       = dc1271add62bff0dd6cf9dcb7754c100c512c51f42290862687d7df45418d7ca
stdout self-capture mismatch= 68f7555a7d62b5c65f61727a7b788b13a3f1f6c95679bb958c05f1aafb13147b
finite integrity            = a5b646a94f453eef5ba8dc294d59fe8576d3bb145e3974bd663a90b3bb23d3a0
```

因此doc421现在是`M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。doc420仍为
`MERGED / NOT_QUALIFIED`，run `43783429314`与lower cause `UNKNOWN`都没有被回填。fresh CONTROL LOOP重新核对remote main、活动
PR、source/test bytes与primary `audit.json`后，只授权本read-only feasibility audit。

## 2. 受审首败与不可扩大事实

不可变首败只证明：

```text
execution_status       = ERROR
stop_reason            = COLLECTOR_ERROR
verdict                = FAIL
browser_capture_complete = false
browser_completed      = false
cleanup_complete       = true
browser_error_types    = ()
```

failed job log SHA-256仍为
`302e8a372493ba0ba19280d62991d621c760d2478e2686f6a2cdf2d2b3bbb95f`，failure record SHA-256仍为
`44f98e2280e8732913b3d8e8e08f6420405bf86b2c66b61144f0641575d9117c`。没有failed evidence Artifact，不能从后继本地
probe补写old attempt的Browser、资源、service、runner或环境根因。

本审计要回答的不是“旧失败究竟是什么”，而是：

```text
能否在不改变runtime、oracle、timeout、retry与public payload的前提下，
让同一repeatability witness下次首败时保存足以归层的same-attempt lower facts？
```

## 3. exact source中的现有观察面

### 3.1 现有Browser private trace只覆盖一条异常路径

`tests/test_bootstrap_run_cli.py::_run_with_browser_error_trace`只包住
`veritrail.bootstrap_run.collect_observed_browser_evidence`。它在`ObservedBrowserCollectionError`出现时保存
`error_type`并立即重抛同一异常；成功路径原样返回。

这能解释为什么`browser_error_types=()`不能推出“Browser一定没有失败”：

```text
Browser returns an incomplete Evidence object
resource monitor requests COLLECTOR_ERROR
service/readiness/finalization layer yields COLLECTOR_ERROR
post-lifecycle observed result carries another error_type
```

这些路径都不会经过`ObservedBrowserCollectionError`的private tuple。

### 3.2 lifecycle与observed result已经保留更细facts

`BootstrapLifecycleObservation`已经包含event vector、node start/readiness/teardown、services-ready callback、trigger/stop reason、cleanup与
elapsed；其中service start、readiness、evidence finalization与teardown各有不同event result。`BootstrapObservedRunResult`又保存Browser
Evidence、resource/subject observation、workspace release flags、staged digest与post-lifecycle `error_type`。

`run_bootstrap_bundle`把完整`BootstrapObservedRunResult`放在`BootstrapPublicRunResult.observed`中；CLI实际调用的是导入到
`veritrail.cli.run_bootstrap_bundle`的同一symbol，但随后公共summary只投影high-level状态。因此same-attempt lower facts在test assertion以前仍然
存在，只是repeatability proof facility没有保存它们，临时目录在失败退出后又消失。

### 3.3 resource monitor也有独立可观察边界

resource sampler读取Core/host/node memory；任何采样异常都会把`sampling_complete`设为false并请求公共
`COLLECTOR_ERROR`。final observation保存`sampling_complete`与`limit_trigger_reason`，但不保存未授权的Python exception message。这足以把
“resource observation incomplete”与“Browser private exception”分层，仍不足以凭空宣布单一底层原因。

## 4. 外置受控probe

本审计没有修改tracked test/runtime。外部probe只在test process中包住`veritrail.cli.run_bootstrap_bundle`：

```text
original returns result
-> project bounded lower facts
-> return the exact same result object

original raises exception
-> record exception class/message at test boundary
-> re-raise the same exception
```

它在CPython 3.10.6 / 3.13.13 × normal / `-O`四格运行四种world；每种world的稳定语义投影在四格逐字节一致：

| controlled world | public result | additional bounded observation | semantic SHA-256 |
| --- | --- | --- | --- |
| success | `COMPLETED / PASS / NONE` | complete lifecycle、Browser present、workspace released | `53bd2faa88cf76753aaf6e1f453abab76fcb1e71553a7559df2939e31965f900` |
| Browser private exception | `ERROR / PENDING / COLLECTOR_ERROR` | `DiagnosticSentinel` + `EXERCISED/COLLECTOR_ERROR` | `8964399472615ab22493d97fa11846d31abcf72b1e842112d24040d75d01a90f` |
| Browser formed failure facts | `ERROR / PENDING / COLLECTOR_ERROR` | `HostSocketNoBufferSpace` + raw `net::ERR_NO_BUFFER_SPACE` | `23ca0c4add716ad4716fa8242ea5383e6be5216d29616f9b5bb77f6ae48529ae` |
| resource sampling failure | `ERROR / PENDING / COLLECTOR_ERROR` | `sampling_complete=false`、no Browser private type | `2cf4a28c250394fadb1a58fd0e066986e86d8b89950a9c60b6f620af29b3b6cc` |

16-row matrix summary SHA-256为
`99389be0116c2b04b95c78f660b5cbb2f09743ab842ad8626ec6b9894b95dda4`。该probe只证明观察面与透明capture seam
可机械使用；synthetic failure不是old attempt事实，也不是public product observation。

第一次Browser formed-facts probe把冻结witness的`ERROR / PENDING`误写成`COMPLETED / FAIL`，在assertion处终结；stderr SHA-256为
`04c30948d6aa3fade689f5ff9da0bb8cf6cc75ee85d162a3f237714f125b3324`。attempt 2只修正外部probe expectation后形成上表PASS。
第一次summary又要求早期已经PASS的probe result含后加的`browser`projection key，得到`KeyError`；stderr SHA-256为
`ced7275bc0ea930eb81ff2584476f28da7a47fbd95011e11873dd47d849f46a2`。attempt 2让summarizer兼容早期result shape，未重复产品
probe。这两项均为`qualification effect NONE`，没有修改仓库或生成正式产品failure。

## 5. real repeatability diagnostic仍不解释首败

当前exact source上的原repeatability test在四格各1/1 PASS：

| interpreter | mode | result |
| --- | --- | ---: |
| CPython 3.10.6 | normal | 1/1 PASS |
| CPython 3.10.6 | `-O` | 1/1 PASS |
| CPython 3.13.13 | normal | 1/1 PASS |
| CPython 3.13.13 | `-O` | 1/1 PASS |

这是`NON_QUALIFYING_LOCAL_DIAGNOSTIC`。它只证明稳定隔离复现仍未被观察到；不能把full-suite failure降格为偶发、不能说明旧失败已经消失，也
不能让doc420取得资格。

## 6. 可行性结论与最小未来责任

结论为：**test-only first-failure observation correction可行，但尚未授权施工。** 最小future correction应同时保留三层，不合并authority：

1. 原public payload与exact oracle；
2. `BootstrapPublicRunResult.observed`中的lifecycle/node/resource/subject/workspace facts；
3. 既有Browser private exception trace，以及已成形Browser Evidence中的bounded collection/network facts。

最小实现形状应是：

```text
patch only the test proof facility
-> wrap veritrail.cli.run_bootstrap_bundle exactly once
-> return the original result unchanged
-> re-raise the original exception unchanged
-> project bounded same-attempt facts before the first repeatability assertion
-> attach deterministic projection to assertion diagnostics
-> keep exact COMPLETED/PASS/cleanup/repeatability oracle
```

controlled witnesses必须分别证明success透明、Browser private exception、Browser formed facts与resource sampling incomplete；它们不能代替真实
repeatability witness。后继不得新增runtime字段、public Evidence、timeout、retry、rerun、skip、subset assertion或workflow relaxation。

该结论没有选择Browser、resource、service、runner或environment为旧失败根因。未来再次出现非成功时，保存的facts只能支持按实际观察归层；仍缺证据的
部分必须保持`UNKNOWN`。

## 7. 禁止的推论

```text
transparent capture seam feasible
!= correction implemented or qualified

four-grid controlled PASS
!= old exact-main failure explained

isolated repeatability PASS
!= full-suite repeatability guaranteed

formed Browser facts available
!= old failure was a Browser network failure

resource facts distinguishable
!= old failure was resource exhaustion

better diagnostics
!= engineering problem solved
```

doc420、run `43783429314`、failed log、failure record与`UNKNOWN`都继续保持原identity。

## 8. 本候选的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/422-r1-m10-repeatability-failure-observation-feasibility-audit.md
docs/milestones.md
```

final docs bytes至少必须通过：

1. exact source/test/doc421 closeout/failure identity continuity；
2. CPython 3.10.6 / 3.13.13 × normal / `-O`的focused现有witness；
3. external controlled probe四world四格、semantic equivalence与所有setup failure retention；
4. UTF-8 without BOM、LF/final LF、links/fences/headings、`git diff --check`、global/local hygiene与primary `audit.json` continuity；
5. candidate exact base/head/tree、original PR attempt 1 required Public CI；
6. protected exact-head merge、新exact-main Public CI与Browser Smoke attempt 1；
7. fresh anonymous installed-product README/doc421/doc422 Render与AGENTS/milestones raw/API/exact-Git byte observations；
8. independent source/problem/failure/authority reconciliation与finite closeout。

任何FAIL、ERROR、CANCELLED、setup failure或UNKNOWN按原identity保留，不自动retry，不用后继PASS覆盖。

### 8.1 final-byte local witness

final docs bytes下，repeatability、Browser private-type sentinel与formed Browser fact witness在四格各3/3 PASS：

| interpreter | mode | result |
| --- | --- | ---: |
| CPython 3.10.6 | normal | 3/3 PASS |
| CPython 3.10.6 | `-O` | 3/3 PASS |
| CPython 3.13.13 | normal | 3/3 PASS |
| CPython 3.13.13 | `-O` | 3/3 PASS |

global/local hygiene在同一四格为8/8 PASS；exact four-file scope、source/test continuity、doc421 closeout identity、primary audit continuity、
UTF-8/LF/final LF、relative links、fences/headings与`git diff --check`也成立。

第一次local validation只因proof script搜索`Hygiene PASS`而不是工具实际输出`Residual Hygiene: PASS`终结；stderr SHA-256为
`aa8b3138c000ddee0ddef79bf9eef8cd50c8ae1d0af3693f85ac67607638b89a`。attempt 2只修proof marker，没有重跑或改写已经PASS的
hygiene/test产品观察。该setup failure保持`qualification effect NONE`。

## 9. 状态上限与下一停止线

本文全部最后门闭合以前：

```text
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_PR481_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_NOT_STARTED_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后，本文最多成为`M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回
CONTROL LOOP，从新的exact main独立建立versioned test-only correction/authorization publication；不得在本文中修改test/runtime、直接重建
carrier、回填doc420或启动R2–R6。

`proof_is_not_problem_solving = true`：证明首败观察设施可改进，不等于解释或修复old failure。

`local_not_global = true`：本文只覆盖M10 repeatability first-failure observation seam；R1完成后的人类+AI全项目检查仍是独立义务。
