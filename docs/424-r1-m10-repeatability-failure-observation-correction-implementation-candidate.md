# R1 M10 repeatability failure-observation correction 0.1 implementation candidate

日期：2026-11-16

> 候选状态：
> `R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_CANDIDATE / NOT_QUALIFIED`
>
> exact base：`main@e9191b14bfc9d5848b30ee07f6765fcebfb23adc`，tree
> `f6a46404abef9c9f4903f61743dd3129883517e3`
>
> 影响层：`L0_TEST_PROOF_FACILITY`。本候选不修改runtime、public payload、Browser collector、oracle、
> timeout、retry、workflow、Schema、Verdict、carrier、Manifest或global composition authority。

## 1. 已生效的窄授权

PR #485把[授权发布](423-r1-m10-repeatability-failure-observation-correction-authorization-publication.md)的

```text
base = c76fc0dd71de281b21a4486bd68b2aebd3375c70
head = 385a07f5a16e0d893cff4de04a2f7a4932d768fa
tree = f6a46404abef9c9f4903f61743dd3129883517e3
```

精确合入`main@e9191b14bfc9d5848b30ee07f6765fcebfb23adc`。original Public CI `43814684449`、exact-main
Public CI `43818850121`与Browser Smoke `43818850080`均为attempt 1 SUCCESS，分别15/15、15/15与1/1；没有rerun。

fresh readback第一次使用过长evidence root；README产品API/Render已经`COMPLETE`后，Windows路径长度使proof-facility
Bundle持久化失败。该身份以
`FORMAL_README_OBSERVATION_WINDOWS_PATH_LENGTH_PROOF_FACILITY_SETUP_FAILURE / NON_QUALIFYING_NONE`永久保留，记录
SHA-256为`85aa22a3ff35cfa82b7e61862866f9cadfa8605cb8e85f83ca830cdee16d0a08`，旧root未删除或覆盖。

新的短root只认`e9191b1… / f6a4640…`：README、doc421、doc422与doc423各自唯一diagnostic为`COMPLETE`，各自唯一formal为
`COMPLETE / PASS`；AGENTS与milestones各自唯一anonymous raw/API/exact-Git全字节一致PASS。reconciliation attempt 1因空白
计数proof-target断言失败而保留，attempt 2只修本地断言并PASS，没有重跑产品观察；一个只读错误doc路径lookup也按setup error保留。
independent reconciliation、146-artifact closeout、expected stdout self-capture mismatch与finite integrity分别为：

```text
32836b09f2de86f267d457d7ca1d30fe551143288a99b86412c2aaf0798cd15d
0638cb066d4c4287b37fc30c110f5ca76001eff46ea5670d3dbdf0d54f9fc36d
42bcc3022342142d42da7da6f34036c450bee0fe64a6152826275bd68a5b5292
5fb596206f62d2a7347dabf22d87080c3d2875313bc40cc0010c6c6e1ad7d7f4
```

因此`R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED`已经生效；这只允许doc423 A–J的test-only
施工，不等于implementation已经资格化或old failure根因已知。

## 2. 原问题与本候选的最小责任

PR #481 exact-main Public CI `43783429314` attempt 1的repeatability witness观察到：

```text
execution_status = ERROR
stop_reason      = COLLECTOR_ERROR
verdict          = FAIL
browser capture = incomplete
cleanup          = complete
private browser error trace = empty
```

该required failure没有rerun；failed job log与结构化failure record SHA-256仍分别为
`302e8a372493ba0ba19280d62991d621c760d2478e2686f6a2cdf2d2b3bbb95f`与
`44f98e2280e8732913b3d8e8e08f6420405bf86b2c66b61144f0641575d9117c`。failed evidence Artifact不存在，lower cause继续是
`UNKNOWN`。本候选不解释、覆盖或回填这项历史，只让未来同一测试若再失败时保留同一attempt已经观察到的lower facts。

## 3. test-only实现

唯一产品相关代码改动位于`tests/test_bootstrap_run_cli.py`：

1. `_BootstrapAttemptObserver`透明包住每次原`veritrail.cli.run_bootstrap_bundle`调用，恰好调用一次；
2. original返回时保存同一个`BootstrapPublicRunResult`的有界、确定性、JSON-safe projection并返回同一对象；
3. original抛异常时只保存test-boundary异常type/message并重抛同一异常；
4. projection只读取result中已经存在的public execution/verdict、lifecycle event/node、resource/subject completion、workspace
   release与Browser Evidence completion/error facts；不回读临时目录、文件、clock或network，也不进行第二次产品执行；
5. 最大event/node/Browser row、text与最终diagnostic bytes均固定上限；foreign result、duplicate call、replacement、无界结果或
   diagnostic自身失败全部fail closed；
6. `test_same_sealed_authorities_repeat_without_residual_contamination`的expected values、status、Verdict、cleanup和exact assertions不变，
   projection只作为既有assertion failure message；
7. controlled witness覆盖success透明、Browser private exception、formed Browser failure facts、resource sampling incomplete，以及
   duplicate/foreign/replacement/unbounded/diagnostic failure拒绝；
8. 既有真实Chromium repeatability与subject-drift witnesses保持原样并继续执行。

test文件最终字节SHA-256为
`69d7a4a44fb26d0500b94e261c22c342e7c4fae85edd9d1d46039e3a3643747c`。本候选没有把test expected value、projection或synthetic
witness升级为产品authority。

## 4. 明确不做的事情

```text
不修改src/、runtime、CLI payload、Browser collector、resource monitor或lifecycle语义
不把exact assertion改成contains/subset，不改变status、Verdict或cleanup要求
不增加timeout、retry、rerun、skip或workflow relaxation
不读取attempt后的临时目录、外部文件、clock、log或network
不用controlled witness替代真实Chromium repeatability / subject-drift witness
不归因旧run 43783429314，不删除UNKNOWN，不回填doc420
不重建carrier/Manifest，不恢复global composition authority，不启动public Review或R2–R6
```

tracked scope只能是：

```text
README.md
AGENTS.md
docs/424-r1-m10-repeatability-failure-observation-correction-implementation-candidate.md
docs/milestones.md
tests/test_bootstrap_run_cli.py
```

## 5. final-byte local witness

focused set包含controlled observer、真实repeatability与真实subject-drift三个tests；最终test字节四格各3/3 PASS：

| interpreter | mode | result | elapsed | log SHA-256 |
| --- | --- | ---: | ---: | --- |
| CPython 3.10.6 | normal | 3/3 PASS | 9.926s | `c09764837198918f711c2fdb00791ce089a3184621337142dabf3930f82c3aa5` |
| CPython 3.10.6 | `-O` | 3/3 PASS | 10.012s | `c7f0d0fcbc07cdd6d46f6024c6a3e0409dd845751962c5faa2349c21c0bfa934` |
| CPython 3.13.13 | normal | 3/3 PASS | 10.384s | `5cf36a9db5239daa1aa04f81972de0c6fcbb98fbdd12d951d72102f28a844524` |
| CPython 3.13.13 | `-O` | 3/3 PASS | 10.052s | `b2de49c2c5465d6f82dac0557b54c9f6d5682bbbeaa13202cdc869acff1bc019` |

complete current-source regression显式绑定repository、Core、Starter、GitHub Evidence与Review Attention source roots；四格各
499/499 PASS：

| interpreter | mode | result | elapsed | log SHA-256 |
| --- | --- | ---: | ---: | --- |
| CPython 3.10.6 | normal | 499/499 PASS | 153.197s | `7f5e12dc9cd13a6aedfeff26877ec952671eced737cbb6c167a01889ba58fe19` |
| CPython 3.10.6 | `-O` | 499/499 PASS | 149.573s | `15b4ca207e9dae8c009b45be847f118d96d61b4fe724721c44e321ce42eec5d0` |
| CPython 3.13.13 | normal | 499/499 PASS | 147.198s | `225d5b4cdb37a539e2c8c5c59ef30278b6c6ff6af650073ad7d0e7ace425da68` |
| CPython 3.13.13 | `-O` | 499/499 PASS | 145.545s | `f5929f91d736d0ab62ac4ce75ac5e726f167fc3e7210110ab7d7b32d42822713` |

预资格第一次误用没有pytest的Miniconda解释器，第二次又没有绑定source roots，分别得到`No module named pytest`与
`No module named veritrail`。两次都在产品执行以前终结，永久保留为
`PREQUALIFICATION_PYTEST_NOT_INSTALLED_SETUP_ERROR / NON_QUALIFYING_NONE`与
`PREQUALIFICATION_SOURCE_ROOT_MISSING_SETUP_ERROR / NON_QUALIFYING_NONE`；后继PASS不删除这两个identity。错误日志SHA-256为：

```text
c7aeb3809bcf875e5352a613eda9d5ae5c531529022bb57eec248c57dbc790d7
883bb149eba8418b4c6ac59b7165cfdd63d79d5cd30fabef7c94a202e70c08b4
```

managed worktree attachment因本聊天累计超过100个artifact identity失败，历史type-location只读probe又使用了不存在的旧模块路径；
两者均以setup error保留，qualification effect为`NONE`。这些local witnesses均不替代candidate commit、original PR、protected merge、
new exact-main gates或fresh installed-product observation。

## 6. 本候选自己的资格链

最终五文件字节还必须串行通过：

1. compile、`git diff --check`、global/local hygiene、Markdown/links、UTF-8/LF、exact five-file scope、forbidden surface与primary
   `audit.json` continuity；
2. single candidate commit的exact base/head/tree与original creation-event Public CI 15/15 attempt 1；
3. protected exact-head merge；
4. new exact-main Public CI 15/15与Browser Smoke 1/1 attempt 1；
5. fresh anonymous installed-product README/doc423/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
6. independent Core/source-byte/problem-identity/retained-history reconciliation与finite closeout。

任何FAIL、ERROR、CANCELLED、setup failure或UNKNOWN按原identity保留；不得rerun洗白、重复已有PASS或拼接不同world。产品readback
必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。

## 7. 状态上限与下一停止线

全部门闭合以前只能记录：

```text
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_PR481_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后，本候选最多成为
`R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED /
READBACK_QUALIFIED / NOT_FROZEN`。随后必须返回CONTROL LOOP，建立独立docs-only implementation freeze publication；不得从candidate
绿灯直接重建carrier或恢复global composition authority。

`proof_is_not_problem_solving = true`：未来首败可观察性改善不等于旧failure根因已知，更不等于原工程问题解决。

`local_not_global = true`：本修正只覆盖M10 repeatability proof facility；R1结束后的人类+AI全项目检查仍是独立义务。
