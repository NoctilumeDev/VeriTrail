# R1 M10 subject-drift Browser first-failure observation correction

日期：2026-11-16

> 候选状态：
> `R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_CANDIDATE / NOT_QUALIFIED`
>
> exact base：`main@f298b042ccb5124d117f6a82d76dbf93624a861d`
>
> 影响层：`L0_TEST_PROOF_FACILITY`；不修改Core runtime、Browser collector、Verdict、Plan/Profile、timeout、retry、workflow或产品Schema

## 1. 入口事实

PR #476 original Public CI `43728958491` attempt 1在Python 3.10 full Core regression的
`test_subject_drift_is_preserved_and_makes_public_verdict_inconclusive`中观察到：

```text
expected contamination = {BOOTSTRAP_SUBJECT_DRIFT}
observed extra item     = BROWSER_STATUS_CONFLICT
Ran 497 tests in 128.218s
FAILED (failures=1, skipped=1)
```

该run没有rerun，PR已关闭且未合并。后继隔离四格与其他绿灯都不回填这项required failure。PR #478与#479已经分别资格化
failure-boundary successor与read-only feasibility；PR #480又把doc419精确合入本候选的base，并闭合：

```text
original Public CI              = 43768756904 / attempt 1 / 15 of 15 SUCCESS
exact-main Public CI            = 43772262297 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser Smoke        = 43772262310 / attempt 1 / 1 of 1 SUCCESS
independent reconciliation      = ca643e0ce7828bff50e2cc53fc49b2e4847c7ebb59cffa345cf13c9fb9fd3be8
113-artifact finite closeout     = 6cca37f17df02f4ee86a4edc02ba90ba47d701505cf93c3363a373b5079dc096
expected self-capture mismatch  = cbf8b91ccae6cbe4e36abc0a89c2b5cd21583cd369bcc329817f0548c2e337ae
finite integrity                = 32c380e62a678763f1ee8e427906175c64a0059b5f19571a4e152f13b8f978b2
```

doc419因此是`M10_STABILITY_FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。它证明有限test-only修正路线存在，不证明原
`BROWSER_STATUS_CONFLICT`的lower cause；该cause继续是`UNKNOWN`。

doc419 readback的Windows `rg` glob setup error、anonymous rate/preflight diagnostics、reconciliation attempt 1
`local_not_global` multiplicity proof-target error与closeout self-capture mismatch均保留原identity。attempt 2只修本地对账断言，未重跑
四份产品观察。

## 2. 本轮真正修正的缺口

原真实集成测试在exact contamination断言以前只保留最终report。若Browser capture不完整，CI日志会显示多出
`BROWSER_STATUS_CONFLICT`，但不会同时保存以下cause facts：

```text
capture_complete / all_steps_passed / collection_errors
viewport status / step status and error
failed network rows
Browser cleanup
bootstrap stop / subject observation / browser exercise / lifecycle / cleanup
```

因此原attempt只能证明subject drift与Browser capture incomplete同时发生；不能从不可变日志判断capture为什么不完整。该缺口属于
test proof facility，不属于Verdict defect、runtime semantic defect或可忽略的额外污染。

## 3. 最小test-only correction

本候选只修改`tests/test_bootstrap_run_cli.py`：

1. 新增private `_subject_drift_failure_diagnostic`，从已经生成的report、`browser.session`与`runtime.bootstrap`投影上述有界facts；
2. 只保存failed/unfinished network rows，不把全部正常网络流量写入失败消息；
3. 真实Chromium subject-drift测试在原exact-set断言以前生成确定性JSON diagnostic，并把它绑定为该断言的failure message；
4. 同一真实测试继续直接断言Browser `capture_complete / all_steps_passed / cleanup_complete`、空collection errors与空failed network；
5. 新增一个不启动产品的controlled proof-facility witness，只证明incomplete Browser facts不会被投影器丢失；它不替代真实Chromium测试。

原断言保持：

```python
self.assertEqual(
    {"BOOTSTRAP_SUBJECT_DRIFT"},
    {item["code"] for item in result.report["contamination"]},
    msg=diagnostic_message,
)
```

因此若未来再次出现额外`BROWSER_STATUS_CONFLICT`，test仍然FAIL；区别只是首败日志会同时包含可归层的Browser/bootstrap现场。

## 4. 不变边界

本候选不做以下事情：

```text
不把exact set改成contains/subset
不删除、忽略、重命名BROWSER_STATUS_CONFLICT
不增加timeout、retry或rerun
不跳过真实Chromium或用controlled witness代替它
不修改src/、workflow、Plan/Profile、Schema、Collector或Verdict
不宣称PR #476 lower cause已经查明
不重建doc415，不启动carrier runtime或R2-R6
```

tracked diff必须只包含：

```text
README.md
AGENTS.md
docs/420-r1-m10-subject-drift-browser-first-failure-observation-correction.md
docs/milestones.md
tests/test_bootstrap_run_cli.py
```

## 5. 本候选的资格门

最终字节必须串行通过：

1. target pair在CPython 3.10.6 / 3.13.13、normal / `-O`四格各2/2 PASS；
2. complete Core current-source regression在相同四格成立，保留实际count、skip与elapsed；
3. `git diff --check`、compile、global/local hygiene、Markdown/links、exact five-file scope与primary `audit.json` continuity；
4. candidate commit的exact base/head/tree与original PR attempt 1 required gates；
5. protected exact-head merge、新exact-main Public CI与Browser Smoke attempt 1；
6. fresh anonymous installed-product README/doc420 Render与AGENTS/milestones raw/API/exact-Git byte observation；
7. independent reconciliation与finite closeout。

任何FAIL、ERROR、CANCELLED、setup failure或UNKNOWN按原identity保留，不自动retry，不用后继PASS覆盖。

## 6. final-byte local witness

target pair在同一最终test字节四格各2/2 PASS：

| interpreter | mode | result | elapsed |
| --- | --- | ---: | ---: |
| CPython 3.10.6 | normal | 2/2 PASS | 3.322s |
| CPython 3.10.6 | `-O` | 2/2 PASS | 3.115s |
| CPython 3.13.13 | normal | 2/2 PASS | 3.392s |
| CPython 3.13.13 | `-O` | 2/2 PASS | 3.133s |

complete Core current-source regression显式绑定repository root、Core、Starter、GitHub Evidence与Review Attention source roots；四格各
498/498 PASS：

| interpreter | mode | result | elapsed |
| --- | --- | ---: | ---: |
| CPython 3.10.6 | normal | 498/498 PASS | 148.382s |
| CPython 3.10.6 | `-O` | 498/498 PASS | 149.853s |
| CPython 3.13.13 | normal | 498/498 PASS | 147.502s |
| CPython 3.13.13 | `-O` | 498/498 PASS | 146.843s |

第一次3.10 normal full invocation只绑定repository root与Core `src`；488项执行后，discovery导入P4辅助模块时得到
`ModuleNotFoundError: veritrail_github`。该次按
`LOCAL_FULL_REGRESSION_IMPORT_PATH_SETUP_ERROR / qualification effect NONE`保留；fresh attempt 2补齐声明的current-source roots后才取得
上表PASS。它没有修改test、runtime或oracle，也不被后继PASS删除。

四格global hygiene各自PASS；第一次local hygiene wrapper把`--local`的单元素数组折叠成scalar后逐字符splat，四次都在
`argparse`前终结。该组保留为`LOCAL_HYGIENE_POWERSHELL_ARGUMENT_SPLAT_SETUP_ERROR / qualification effect NONE`；fresh local
attempt 2只修命令参数传递并取得四格PASS，没有删除第一次stderr或修改仓库。

这些local witnesses不替代candidate commit、original PR、exact-main或fresh installed-product门。

## 7. 状态上限与下一停止线

在上述最后门全部闭合以前：

```text
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后，本候选最多成为
`M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_QUALIFIED`。publication形成新事实后必须返回CONTROL LOOP，
从新的exact main独立重建PR #476所对应的manifest carrier successor contract；不得复用旧head、回填旧失败或直接开始carrier runtime。

`proof_is_not_problem_solving = true`：首败可观察性改善不等于lower cause已知，也不等于原工程问题已经解决。

`local_not_global = true`：本修正只覆盖M10 subject-drift proof facility；R1完成后的人类+AI全项目检查仍是独立义务。
