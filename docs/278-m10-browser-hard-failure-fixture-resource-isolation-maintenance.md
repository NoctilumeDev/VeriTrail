# M10 Browser hard-failure fixture resource-isolation maintenance

Status:

```text
M10_BROWSER_HARD_FAILURE_FIXTURE_RESOURCE_ISOLATION_MAINTENANCE_CANDIDATE
M10_PUBLIC_CLI_NATIVE_HARD_EXIT_DIAGNOSTIC_MAINTENANCE_QUALIFIED
PR_317_ORIGINAL_FAILURE_RETAINED
PR_317_ROOT_CAUSE_UNKNOWN
PR_318_ORIGINAL_FAILURE_RETAINED
PR_318_ROOT_CAUSE_UNKNOWN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_AUDIT_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文件从 `main@a5137525c2348334bf0b79a2e873895a8533e745` 重新创建独立候选，只修一个
test-support seam：普通 Browser / lifecycle 语义 world 不应隐式继承 production-style host-memory
门。它不修改产品资源合同、Browser runtime、timeout、retry、Schema、Coverage 或 R1 frozen contract。

## 1. qualified upstream 与保留失败

root-binding audit PR #317 的 original Public CI `39002394071` attempt 1 在 Python 3.10 Core regression
中观察到：

```text
test_real_browser_hard_failure_keeps_evidence_and_cleans_resources
expected result.browser is not None
observed result.browser is None
```

旧 assertion 没有保存 lifecycle stop/trigger 或 resource observation，因此它不能唯一证明 memory gate、
另一个 Browser-before-exercise stop，或其他根因。#317 保持关闭，原失败与 `UNKNOWN` root cause 永久保留。

第一次 fixture maintenance PR #318 head `ae59c118971614d99ec26413bc64aa07a5e1ab5a` 的 original
Public CI `39005021790` attempt 1 又在 Python 3.13 normal 观察到：

```text
test_dependency_early_exit_creates_completed_fail_bundle_without_browser
child returncode = 3221225477 / 0xC0000005
stdout = ""
stderr = ""
```

#318 没有 rerun、没有改 head并保持关闭。它没有资格证明 fixture patch 错误，也不能被后继 PASS 解释成
runner 抖动；其 native access violation root cause 继续为 `UNKNOWN`。

独立诊断维护 PR #319 只给既有 CLI child 增加 `-X faulthandler`。其 original Public CI
`39012354832`、merge `a5137525c2348334bf0b79a2e873895a8533e745` 上的 exact-main Public CI
`39014078302` 与 Browser Smoke `39014078260` 均为 attempt 1 SUCCESS；fresh README/doc277/milestones
读回与 independent reconciliation 也已闭合。因此诊断 source state qualified，但它不解释 #318，也不让
旧 fixture candidate 继承资格。

## 2. independently proven fixture defect

当前 exact main 的 `tests/test_bootstrap_run.py::_authorities()` 仍从 production-style bootstrap Plan 继承：

```text
available_memory_soft_min_mb = 4096
available_memory_hard_min_mb = 2048
```

该 helper 同时服务于 Browser business failure、collector、staging、drift、cleanup 与资源门测试。于是普通
Browser semantic world 的执行资格会被无关的实时宿主余量决定：

```text
Browser semantic obligation
    + unrelated live host-memory gate
    -> world may stop before Browser exercise
    -> result.browser may be None
```

这是一项真实 test-support topology defect。它独立于 #317 和 #318 的未知精确根因成立。

## 3. minimal correction

私有 `_authorities()` 对非资源语义 world 默认使用 test-owned：

```text
available_memory_soft_min_mb = 1
available_memory_hard_min_mb = 1
```

两个直接验证资源 fail-closed 语义的测试显式 opt in 原门：

```text
soft threshold = 4096 MiB
hard threshold = 2048 MiB
hard-world observed available = 100 MiB
soft-world observed available = 3000 MiB
```

因此普通 Browser/lifecycle world 不再由宿主内存偶然调度，resource-limit worlds 仍机械证明
`RESOURCE_MEMORY_HARD_LIMIT` 与 `RESOURCE_MEMORY_SOFT_LIMIT`。

四个要求 Browser Artifact 的 assertions 同时加入 canonical diagnostic message：

```text
error_type
trigger_reason
stop_reason
resource_observation
```

若同型失败再次发生，原始 CI 不再只留下 `result.browser is None`。这只是可观察性增强，不把后继信息
倒写成 #317 的历史 root cause。

## 4. candidate local observations

第一次尝试经 PowerShell 文本管道传递旧 Git diff 时发生重编码，`git apply` 在首个 hunk 前拒绝；没有形成
工作树 diff，也没有启动产品测试。该事件保留为 `PATCH_TRANSPORT_ENCODING_SETUP_ERROR`。fresh construction
直接从 #318 的 Git blob 复制单一测试文件，复制后 blob identity 精确为：

```text
3c1b4fb75c425ee220ef972d1cb4a06571e04cc2
```

候选代码字节的定向四格为：

| gate | CPython 3.10.6 | CPython 3.13.13 |
| --- | --- | --- |
| `BootstrapObservedRunTests` normal | `14/14 PASS` | `14/14 PASS` |
| `BootstrapObservedRunTests` `-O` | `14/14 PASS` | `14/14 PASS` |

同一代码字节的完整 Core 四格为：

| gate | CPython 3.10.6 | CPython 3.13.13 |
| --- | --- | --- |
| full Core normal | `470/470 PASS` | `470/470 PASS` |
| full Core `-O` | `470/470 PASS` | `470/470 PASS` |

这些结果只证明当前候选没有被所列 witness 击穿，不解释或覆盖 #317/#318 的原始失败。包含本文件、
AGENTS 与 milestones 的最终字节仍必须重新经过本层声明的完整 local gates。

## 5. authority boundary

本维护不得修改：

```text
src/veritrail runtime
production preflight thresholds
Browser timeout / retry / collector semantics
doc267--274 frozen bytes
Coverage 0.1 or planned 0.2 Schema
manifest / Profile / Policy / fixtures / vectors / corpus
root-binding audit semantics
persistence
ReviewSliceSet / Coverage composition runtime
```

它也不让 #317 或 #318 重新取得资格。maintenance 自己完成 final-byte local gates、original PR gates、
受保护合入、新 exact-main Public CI / Browser Smoke、fresh README / 本文件 / milestones installed-product
observations 与 independent reconciliation 后，只能建立新的 qualified source state。

随后必须返回 CONTROL LOOP，从该新 exact main 重新生成 root-binding current-state audit candidate。旧 doc275
的语义推理可以复用，但 candidate/source identity、original PR gates 与后继资格必须重新取得；Schema
implementation、root-binding correction contract、composition feasibility、persistence 与 public product 都不得在
本维护中启动。
