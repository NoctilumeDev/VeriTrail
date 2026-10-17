# M10 Browser hard-failure fixture resource-isolation maintenance

Status:

```text
M10_BROWSER_HARD_FAILURE_FIXTURE_RESOURCE_ISOLATION_MAINTENANCE_CANDIDATE
PR_317_ORIGINAL_FAILURE_RETAINED
PR_317_ROOT_CAUSE_UNKNOWN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_AUDIT_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文件只记录并修正一个 test-support seam：Browser / lifecycle 语义用例过去会隐式继承 production-style
`4096 / 2048 MiB` host available-memory 阈值，因此宿主资源波动可以在 Browser exercise 之前终止 world，
而用例仍把 `result.browser is not None` 当作无条件前提。它不修改产品资源合同、Browser runtime、timeout、
retry、Schema、Coverage 或 R1 frozen contract。

## 1. exact failure identity

R1 root-binding current-state audit 候选 PR #317 使用：

```text
base = 9aa94dcac8c1bc5bb4d4852a5136d3d7bf3fe583
head = e1b59f3936e1a61416dfe1e1cb7e89cb9fa24b92
Public CI = 39002394071
attempt = 1
```

原始 Public CI 的 Python 3.10 车道在 `Run Core regression tests` 中终结为 `FAILURE`：

```text
test_real_browser_hard_failure_keeps_evidence_and_cleans_resources

expected:
    result.browser is not None

observed:
    result.error_type is None
    result.browser is None

suite:
    470 reported
    468 passed
    1 failed
    1 skipped
```

Python 3.13、Workbench 与 E3 在同一 workflow attempt 中成功；依赖 Python 3.10 artifact 的后继 jobs 被
GitHub Actions 跳过。PR #317 没有 rerun，也没有更新 head，随后保持关闭。它的失败身份不能被任何后继
PASS 覆盖。

## 2. evidence limit

失败发生在 Browser assertion，但原 assertion 没有打印 lifecycle stop reason、trigger reason 或 resource observation。
因此现有远端日志不足以唯一确定：

```text
RESOURCE_MEMORY_SOFT_LIMIT
RESOURCE_MEMORY_HARD_LIMIT
另一个 Browser-before-exercise lifecycle stop
```

中的哪一个实际发生。精确 root cause 必须保持 `UNKNOWN`。

但源码复核确认一个独立、真实的 fixture defect：`_authorities()` 从 production-style bootstrap Plan 继承
`available_memory_soft_min_mb = 4096` 与 `available_memory_hard_min_mb = 2048`，并把它用于本来只验证 Browser
business failure、collector、staging、drift 与 cleanup 语义的测试。于是：

```text
Browser semantic world
    + unrelated live host-memory threshold
    -> Browser may never start
    -> result.browser may be None
```

这个 defect 即使不是 PR #317 首败的唯一原因，也足以让该测试 topology 不具备稳定资格。

## 3. minimal correction

`tests/test_bootstrap_run.py` 的私有 `_authorities()` 现在默认把非资源语义 world 的 host-memory threshold 固定为：

```text
available_memory_soft_min_mb = 1
available_memory_hard_min_mb = 1
```

这只改变 test-owned sealed Plan。两个直接验证 host-memory fail-closed 语义的测试显式 opt in：

```text
available_memory_soft_min_mb = 4096
available_memory_hard_min_mb = 2048

hard world observed available = 100 MiB
soft world observed available = 3000 MiB
```

因此 Browser / lifecycle 测试不再由宿主剩余内存偶然调度；resource-limit tests 仍机械证明原阈值下的
`RESOURCE_MEMORY_HARD_LIMIT` 与 `RESOURCE_MEMORY_SOFT_LIMIT`。

四个需要 Browser Artifact 的 assertions 同时增加 canonical diagnostic message，至少保留：

```text
error_type
trigger_reason
stop_reason
resource_observation
```

若同型失败再次发生，日志不再只留下 `result.browser is None`。

## 4. retained local observations

第一次定向本地调用清除了 `PYTHONPATH`，但没有先安装 editable Core，因而以：

```text
ModuleNotFoundError: No module named 'veritrail'
```

终结。它是 `LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`，不属于产品或 fixture 反例。fresh 调用显式把
当前 `src` 加入该命令的 import path 后，同一失败单例与完整 `BootstrapObservedRunTests` 均通过。

第一次全仓本地调用只挂载了 Core `src`，没有同时挂载 GitHub Evidence plugin `src`；因此
`tests.test_github_evidence_release_assets` 在 discovery 时以：

```text
ModuleNotFoundError: No module named 'veritrail_github'
```

终结。该调用已完成的 459 项测试均通过，但整次调用只能归为
`LOCAL_TEST_INVOCATION_PLUGIN_IMPORT_PATH_SETUP_ERROR`。fresh 全仓调用在同一命令中显式挂载 Core 与 plugin
两个 source root；它没有复用或覆盖前一次调用的身份。

修正后的定向四格为：

```text
CPython 3.10.6 normal    14/14 PASS
CPython 3.10.6 -O        14/14 PASS
CPython 3.13.13 normal   14/14 PASS
CPython 3.13.13 -O       14/14 PASS
```

修正最终字节的完整四格为：

```text
CPython 3.10.6 normal    470/470 PASS
CPython 3.10.6 -O        470/470 PASS
CPython 3.13.13 normal   470/470 PASS
CPython 3.13.13 -O       470/470 PASS
```

这些测试是 maintenance witness，不解释或覆盖 PR #317 的远端首败。

## 5. authority boundary

本维护不得修改：

```text
src/veritrail runtime
production preflight thresholds
Browser timeout / retry / collector semantics
doc267--274 frozen bytes
Coverage 0.1 or planned 0.2 Schema
manifest / fixture / corpus / identity vectors
root-binding audit semantics
persistence
ReviewSliceSet / Coverage composition runtime
```

它也不让 PR #317 重新取得资格。maintenance 自己完成 final bytes、完整 local gates、original PR gates、
受保护合入、新 exact-main Public CI / Browser Smoke、fresh README / 本文件 / milestones 产品读回与 independent
reconciliation 后，只能建立新的合格 source state。

随后必须返回 CONTROL LOOP，从该新 exact main 重新生成 root-binding current-state audit candidate。原 doc275
语义推理可以复用，但 candidate/source identity、original PR gates 与后继资格必须重新取得；Schema implementation、
root-binding correction contract、composition feasibility、persistence 与 public product 均不得在本维护中启动。

