# M10 Browser 业务失败分类首败诊断覆盖修正

> 状态：`CORRECTION_CANDIDATE /
> R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_AUDIT_REQUALIFICATION_BLOCKED`
>
> 精确基线：`main@042654e8f9467fbaa8e26cf31690b8f878541eda`
>
> 影响层级：`L0_TEST_FIXTURE + L0_DOCUMENTATION`；不修改 Core runtime、Browser collector、公共
> Evidence、Schema、timeout、CI、R1 合同或文档 192 的审计结论

## 1. 触发事实与首败身份

Post-Slice-Input Closure / Slice-Coverage Qualification docs-only audit PR
[#200](https://github.com/NoctilumeDev/VeriTrail/pull/200) 的 original Public CI
[run 36126771319](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36126771319) attempt 1 为
11/11 PASS，随后合入上述 exact main。该 exact main 的 Browser Smoke
[run 36128804624](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36128804624) attempt 1 为
1/1 PASS；Public CI
[run 36128804576](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36128804576) attempt 1 则在
Python 3.13 的 Core regression 中形成正式失败：

```text
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_browser_business_failure_is_completed_fail_not_contamination

expected stop_reason = BROWSER_HARD_FAILURE
actual   stop_reason = COLLECTOR_ERROR

AssertionError:
'BROWSER_HARD_FAILURE' != 'COLLECTOR_ERROR'
```

同一 run 的 Python 3.10、Workbench 与 E3 均成功；依赖 Python 双车道的后继 jobs 被跳过。原 workflow
没有 rerun。该 run 证明 exact-main 资格没有成立，也证明预注册 browser business failure world 在该次
Python 3.13 观察中发生了分类漂移；它不证明 docs-only diff 修改了 runtime，也不证明漂移来自某个已知的
Browser、collector、runner 或时序根因。

## 2. 已知位置与未知原因必须分开

失败位置已经明确：业务失败用例预期得到 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`，实际公共 summary
得到 `COLLECTOR_ERROR`。但是冻结的 `runtime.bootstrap` Artifact 与 CLI summary 只保存公共 stop reason，
不保存 private `ObservedBrowserCollectionError.error_type`。原始首败因此无法继续区分：

```text
Playwright startup
Chromium launch / CDP ownership
resource checkpoint sampling
context / browser / driver cleanup
response or route lifecycle
other collector exception
```

在相同 exact main 上，Python 3.13 使用既有 test-only transparent wrapper 对同一业务失败 world 做了五个
全新本地诊断 sessions。五次均得到：

```text
stop_reason              = BROWSER_HARD_FAILURE
execution_status         = COMPLETED
verdict                  = FAIL
browser_capture_complete = false
cleanup_complete         = true
browser_error_types      = []
```

这些诊断只证明远端漂移没有在五次本地观察中稳定复现；不能把远端首败降格为偶发，不能解释其根因，也不能
冒充 exact-main qualification。

## 3. 现有诊断承诺的覆盖缺口

[文档 177](177-m10-ci-fixture-observation-correction.md) 已为 public repeat 用例增加 test-only
`_run_with_browser_error_trace(...)`：它捕获 exact private error type，随后立即重抛同一个
`ObservedBrowserCollectionError`，不改变产品的 stop reason、Verdict、Evidence 或 cleanup。确定性的
`DiagnosticSentinel` 测试又证明该 wrapper 不吞异常、不转 PASS。

但是本次失败的 browser business-failure 用例仍调用普通 `_run(...)`。因此“同型失败再次出现时不再只留下
`COLLECTOR_ERROR`”只覆盖 repeat world，没有覆盖另一个长期存在且历史上也曾发生 collector 分类漂移的
business-failure world。该覆盖缺口不会制造产品错误，却会在正式失败发生时再次丢失唯一可恢复的 private
错误类型。

## 4. 最小修正

本维护只把 `test_browser_business_failure_is_completed_fail_not_contamination` 接到既有 transparent tracing
helper：

```text
collector success
-> original result unchanged
-> browser_error_types == ()

ObservedBrowserCollectionError(error_type)
-> append exact private type to assertion diagnostic
-> re-raise the same exception
-> product keeps fail-closed COLLECTOR_ERROR semantics
```

业务失败用例的 expected public semantics 不变。它仍必须证明：

```text
BROWSER_HARD_FAILURE
COMPLETED / FAIL
capture incomplete
cleanup complete
no private collector error
```

本修正不增加 retry，不扩大 timeout，不改变 Browser lifecycle、resource observer、Artifact、Schema、CLI、
workflow 或 R1 runtime。它也不声称已经修复 run `36128804576` 的未知根因；只保证同一测试 world 下次若
再次落入 `COLLECTOR_ERROR`，assertion 会同时保留 exact private error type。

## 5. 当前状态与停止线

以下推论继续禁止：

```text
five local diagnostic PASS
!= remote exact-main failure did not happen

private error tracing added
!= collector failure root cause fixed

maintenance PR PASS
!= PR #200 exact-main qualified

later exact-main PASS
!= run 36128804576 was PASS or explained
```

当前公开状态必须收回到：

```text
R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_AUDIT_MERGED
R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_AUDIT_REQUALIFICATION_BLOCKED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本维护只有在下列事实串行成立后才可关闭：

1. 最终 diff 只包含 test-only diagnostic coverage、本记录与必要状态同步；
2. business-failure、repeat 与 diagnostic sentinel 在 Python 3.10/3.13 normal/`-O` 同一最终字节通过；
3. 完整 `test_bootstrap_run_cli` 与适用 Core regression 在双 Python normal/`-O` 通过；
4. 维护 PR 自己的 original Public CI required checks 全部成功；
5. 维护经受保护主线合入，新的 exact-main Public CI 与 Browser Smoke original gates 全部成功；
6. 只有从第 5 项成立后的 exact main 独立发布状态，文档 192 才能取得
   `...PRECONTRACT_AUDITED`，下一份最小合同才有资格开始。

第 5 项以前，不得把本维护写成 collector 修复，也不得开始 ReviewSliceSet/Coverage qualification 合同、
Schema、Evidence、Manifest、runtime、publisher、output root、公共 Bundle、Attention、CLI 或 Workbench。

## 6. 当前本地候选证据

业务失败、repeat 与 diagnostic sentinel 三个精确用例在同一最终 source bytes 上完成四格：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 3/3 PASS | 16.240s |
| 3.10.6 | `-O` | 3/3 PASS | 12.571s |
| 3.13.13 | normal | 3/3 PASS | 12.632s |
| 3.13.13 | `-O` | 3/3 PASS | 12.618s |

完整 `test_bootstrap_run_cli` 也在四格成立：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 24/24 PASS | 56.118s |
| 3.10.6 | `-O` | 24/24 PASS | 56.037s |
| 3.13.13 | normal | 24/24 PASS | 54.437s |
| 3.13.13 | `-O` | 24/24 PASS | 55.294s |

完整 Core current-source suite 在四格成立：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 460/460 PASS | 149.609s |
| 3.10.6 | `-O` | 460/460 PASS | 139.305s |
| 3.13.13 | normal | 460/460 PASS | 136.148s |
| 3.13.13 | `-O` | 460/460 PASS | 137.689s |

完整 suite 使用当前 worktree 的 Core、Starter、GitHub Evidence 与 Review Attention `src` roots，证明的是
current-source regression，不冒充 GitHub runner 的 editable-install topology。维护 PR、自身 exact-main 双门与
后继状态发布仍未执行，因此当前仍是 correction candidate 与 audit requalification blocked。
