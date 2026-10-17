# M10 public CLI native hard-exit diagnostic maintenance

Status:

```text
M10_PUBLIC_CLI_NATIVE_HARD_EXIT_DIAGNOSTIC_MAINTENANCE_CANDIDATE
PR_318_ORIGINAL_FAILURE_RETAINED
PR_318_ROOT_CAUSE_UNKNOWN
M10_BROWSER_HARD_FAILURE_FIXTURE_RESOURCE_ISOLATION_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_AUDIT_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文件只修正一个 test-support 观察缺口：已经隔离到 child process 的公共 CLI negative world 能保留 native
hard-exit code，却没有启用 Python `faulthandler`，所以 `0xC0000005` 仍可能只留下空 stdout / stderr。本维护不修改
Core runtime、Windows Job / service lifecycle、产品 timeout、retry、资源阈值、Schema、Coverage 或任何 R1 frozen
contract；它也不声称解释或修复原生 access violation。

## 1. exact failure identity

M10 Browser fixture resource-isolation maintenance PR #318 使用：

```text
base = 9aa94dcac8c1bc5bb4d4852a5136d3d7bf3fe583
head = ae59c118971614d99ec26413bc64aa07a5e1ab5a
Public CI = 39005021790
attempt = 1
```

原始 Public CI 的 Python 3.13 normal `Run Core regression tests` 在以下用例终结为 `FAILURE`：

```text
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_dependency_early_exit_creates_completed_fail_bundle_without_browser

expected child return code = 0
observed child return code = 3221225477 = 0xC0000005
stdout = ""
stderr = ""

suite:
    470 reported
    468 passed
    1 failed
    1 skipped
```

Python 3.10、Workbench 与 E3 在同一 workflow attempt 中成功；Python 3.13 的后继步骤及依赖双 Python artifact
的聚合 jobs 被跳过。PR #318 没有 rerun、没有更新 head，随后保持关闭。它的 failure identity 不能被本维护或
任何后继 PASS 覆盖。

## 2. 与 doc191 的关系

[文档 191](191-m10-public-cli-host-exit-observation-correction.md)已经把这个 negative public-CLI world 从
unittest 宿主进程移入独立 child：

```text
unittest observer
    -> exact sys.executable
    -> preserve normal / -O mode
    -> python -m veritrail run ...
```

这次 #318 证明该修正有效保住了外层裁判：suite 继续运行并报告精确 child return code，而没有像 #191 的首败那样
让整个测试宿主无 traceback 消失。但旧 child invocation 没有启用 `faulthandler`，所以 native access violation 没有留下
Python current-thread stack。由此能够成立的是：

```text
outer observer survived
native hard-exit identity retained
native Python stack absent
```

不能推出：

```text
谁触发了 access violation
Windows Job / service lifecycle 存在 double close
pywin32 是根因
runner 或 Python 3.13.16 是根因
```

## 3. root-cause boundary

从 exact main 复核 `windows_job.py` 与 `windows_service.py` 的 process、thread、Job 与 pipe-handle ownership：主要关闭
路径在交接后置空；reader 自行关闭 read handle 与 teardown 的 forced close 由 thread liveness 分支隔离。当前源码审查
没有得到可证明的 duplicate close、use-after-close 或其他能够解释 `0xC0000005` 的反例。

同一 exact-main 目标用例在本机 CPython 3.13.13、`PYTHONFAULTHANDLER=1` 下使用 40 个 fresh child identity 连续
`40/40 PASS`。这只说明失败没有稳定复现，不证明失败不存在或属于 runner 抖动。#318 的 root cause 保持
`UNKNOWN`。

一个 audit-only synthetic child 在本机使用：

```text
python -X faulthandler <probe that triggers ctypes.string_at(0)>
```

终结为 Windows access violation，并在 stderr 留下 `Windows fatal exception: access violation` 与 Python current-thread
stack，证明该 interpreter boundary 可以增强同型 native crash 的诊断。probe 不进入候选字节。后续试图用另一层本地
process wrapper重复该 probe 时，命令在 child 启动前被执行策略拒绝；该事件只属于 operator/tool setup，不是产品或
候选反例。

## 4. minimal correction

目标用例的 child argv 只增加：

```text
-X faulthandler
```

位置在现有 normal / `-O` optimization 参数之后、`-m veritrail` 之前。于是：

```text
normal observer -> same interpreter + -X faulthandler
-O observer     -> same interpreter + -O + -X faulthandler
```

产品命令、sealed Plan/Profile、preview approval、run id、Bundle output 与全部 semantic assertions 不变。正常成功 world
仍必须满足 `stderr == ""`；若 native fault 再现，faulthandler 输出会使原断言携带捕获的 fatal stack，nonzero return code
仍然是 FAIL，不重试、不降级、不转换为 PASS。

## 5. candidate local qualification

最终候选字节在两个本地解释器的 normal / `-O` 四格中保持相同产品断言：

| gate | CPython 3.10.6 | CPython 3.13.13 |
| --- | --- | --- |
| exact target normal | `1/1 PASS` | `1/1 PASS` |
| exact target `-O` | `1/1 PASS` | `1/1 PASS` |
| full Core normal | `470/470 PASS` | `470/470 PASS` |
| full Core `-O` | `470/470 PASS` | `470/470 PASS` |
| hygiene | `5/5 PASS` | `5/5 PASS` |

`git diff --check` 与 tracked-diff absolute-path scan 同时通过。上述 PASS 只资格化本候选字节，不解释 #318 的
原始 access violation。

## 6. authority boundary and next control loop

本维护不得修改：

```text
src/veritrail runtime
Windows Job / service lifecycle
production memory thresholds
Browser fixture resource-isolation patch
Coverage 0.1 or planned 0.2 Schema
manifest / Profile / Policy / fixtures / vectors / corpus
root-binding audit semantics
persistence
ReviewSliceSet / Coverage composition runtime
```

它自己的 final bytes、local gates、original PR gates、受保护合入、新 exact-main Public CI / Browser Smoke、fresh
README / 本文件 / milestones installed-product observations 与 independent reconciliation 全部闭合后，只能建立一个
更强的 native hard-exit diagnostic source state。

之后必须返回 CONTROL LOOP，从该新 exact main 重新创建 Browser fixture resource-isolation maintenance；只有后者独立
资格化以后，才可再次创建 root-binding current-state audit。#317 与 #318 的原失败继续保留，Schema implementation、
root-binding correction contract、composition feasibility、persistence 与 public product 均不得在本维护中启动。
