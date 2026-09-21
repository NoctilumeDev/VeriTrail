# M10 descendant readiness 正向夹具观察修正

> 状态：`CORRECTION_QUALIFIED / R1_RELATION_SET_ADMISSION_CONTRACT_REQUALIFICATION_IN_PROGRESS`
>
> 精确基线：`main@1ffc4494dbbb61a056dcc8beed2530e7313f6116`
>
> 维护闭合基线：`main@f4aec949258ed16830b2e8dd828273435498764b`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core runtime、readiness 合同、cleanup 合同、公共 Evidence、R1 合同候选或产品 timeout

## 1. 触发事实与正式首败

R1 RelationSet admission / explicit witness docs-only 候选 PR
[#171](https://github.com/NoctilumeDev/VeriTrail/pull/171) 的原始 head 为
`cffd64d941b76bdae746fab4190d5c56c1d33366`，base 为上述 exact main。该 head 只修改六份 Markdown；没有
修改 Core、M10、CI、测试、公共 Schema 或 R1 runtime。原始 Public CI
[run 35629971691](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35629971691) 为 attempt 1，并保留以下
正式失败：

```text
Python 3.10 / -O
tests.test_windows_service.WindowsServiceTests.
test_descendant_listener_becomes_ready_and_job_cleanup_releases_port

assertion: readiness.ready is true
actual:    false
```

同一 Python 3.10 job 的 normal 451-test step 成功；Python 3.13 normal 与 `-O`、E3 release-download
acceptance 和 Workbench 均成功。依赖双 Python job 的后继 acceptance/wheel/Starter/GitHub Evidence 门因该失败
被跳过。PR #171 不在原 head 上 rerun；本维护或后继候选的绿色都不能把该 attempt 改写成成功。

## 2. 已知事实与仍未知的原因

失败测试从 unittest 开始报告到下一测试开始约为 `3.045s`，而旧正向夹具的
`total_timeout_ms` 恰为 `3000`。但是旧断言只保存布尔值，没有输出 `OwnedReadinessObservation.error_type`、
attempt 序列或当时的 bounded stdout/stderr；断言又发生在显式 `session.terminate()` 以前。不可变远端日志因此
不能区分：

- listener 启动未在 3 秒内完成；
- listener 或 Job 状态在最后一个 observation 边界变化；
- 端口、stream 或 collector 出现其他未保存的失败；
- 其他只在原 runner 状态下成立的干扰。

所以原始 failure 的精确根因保持 `UNKNOWN`。约 `3.045s` 与旧预算的吻合只支持“deadline exhaustion 是高相关
候选”，不授权把它写成已证实唯一原因。

在相同 source state 上，CPython 3.10.6 `-O` 的独立诊断逐次建立真实 child-listener session，并在 `finally`
中回收；20/20 次均取得 READY，每次约 `0.391–0.469s`。这只能证明本机没有稳定复现，不能否定远端首败。
第一次诊断命令因脚本目录不在仓库、`PYTHONPATH` 又只包含 `src`，在 discovery 前得到
`ModuleNotFoundError: tests`；补齐 exact repository root 后才形成上述 20 次观察。前一次属于 local gate setup
failure，不是产品或夹具测试结果。

## 3. 独立存在的夹具缺口

无论远端首败的唯一原因是什么，源码已经证明旧测试同时存在两个 test-harness 问题：

1. 该正向用例要证明的是 owned descendant listener 能到达 READY、连续两次成功且 teardown 释放 Job/port；
   M10 合同没有要求这个测试夹具在 3 秒内冷启动。把正向正确性绑定到 `3000ms` 是额外的 runner-latency
   假设。
2. `session.terminate()` 只在 READY 断言以后调用。断言失败时，测试不再主动回收已创建的 owned Job tree，
   并且把能够解释失败的 observation 与 stream 前缀丢出日志。

这与产品 fail-closed 行为不是同一个问题。产品在封存 Profile 的 bounded timeout 内没有 READY 时仍必须失败；
这里只修测试怎样为一个预期成功、没有 3 秒 SLO 的 helper 分配观察预算并保存首败事实。

## 4. 最小修正

本维护只改一个正向测试：

```text
start owned session
-> immediately register idempotent cleanup
-> use one bounded 10s readiness window for this positive helper
-> if not READY, print exact observation + bounded stdout/stderr
-> on success, retain the same two-success / owned-listener / two-process /
   zero-active-process / port-release assertions
```

`10s` 仍在冻结 Profile 允许的 `500–30000ms` 范围内，也与仓库已经用于 hosted Windows 冷启动门的有界
正向观察窗口一致。它不增加 retry，不改变 `probe_owned_http_readiness`、默认 `_readiness()`、任何负向测试、
process/port cleanup deadline 或产品 Plan/Profile。若 helper 在 10 秒内仍不能 READY，测试继续失败；新的日志
会保留 exact terminal、attempts 和 bounded streams，cleanup 也会无条件执行。

本维护不声称：

```text
later PASS
=> old failure explained

10s fixture budget
=> production timeout changed

diagnostic detail
=> failure may be ignored

docs-only PR
=> Core red light is irrelevant
```

## 5. 资格与停止线

本维护只有在以下条件串行成立后才可关闭：

1. 最终 diff 只包含这个 test-only correction、本记录与必要状态索引；
2. 精确目标用例在 CPython 3.10/3.13 normal 与 `-O` 四格成立；
3. 完整 Core current-source 451-test 在同一最终字节、双 Python normal/`-O` 四格成立；
4. maintenance PR 自己的原始 Public CI required checks 全部成功；
5. 维护受保护合入，新 exact-main Public CI 与 Browser Smoke 原始门全部成功；
6. PR #171 从该 maintenance-qualified exact main 形成新 head，并重新取得自己的完整门禁。

第 5 项以前，历史状态只能是：

```text
M10_DESCENDANT_READINESS_FIXTURE_OBSERVATION_CORRECTION_CANDIDATE
R1_RELATION_SET_ADMISSION_CONTRACT_REQUALIFICATION_BLOCKED
```

第 6 项以前，不能发布 RelationSet admission contract freeze，也不能开始 Evidence 0.2、admission witness、
RelationSet、publisher、Slice、Coverage、CLI 或 Workbench 实现。

## 6. 当前本地候选证据

精确目标用例在同一最终代码字节上通过四格：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 1/1 PASS | 0.501s |
| 3.10.6 | `-O` | 1/1 PASS | 0.490s |
| 3.13.13 | normal | 1/1 PASS | 0.435s |
| 3.13.13 | `-O` | 1/1 PASS | 0.437s |

完整 Core current-source 451-test 在同一最终代码字节上也通过四格：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 451/451 PASS | 141.493s |
| 3.10.6 | `-O` | 451/451 PASS | 136.204s |
| 3.13.13 | normal | 451/451 PASS | 134.391s |
| 3.13.13 | `-O` | 451/451 PASS | 141.241s |

完整门通过显式 `PYTHONPATH` 组合本 worktree 的 Core、Starter、GitHub Evidence 与 Review Attention
`src` roots，证明 current-source broader regression；它不冒充 Public CI 的 editable/install topology。
## 7. 远端闭合与当前边界

maintenance PR [#172](https://github.com/NoctilumeDev/VeriTrail/pull/172) 的 original head
`d3342175aa5611ff1d2c6cefeb300137ac0696ef` 在 Public CI
[run 35634296113](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35634296113) attempt 1 取得
11/11 PASS。它随后受保护合入 `main@f4aec949258ed16830b2e8dd828273435498764b`；该 exact main 的
Public CI [run 35636414037](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35636414037) attempt 1
为 11/11 PASS，Browser Smoke
[run 35636414038](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35636414038) attempt 1 为 1/1 PASS。
因此第 1–5 项已经成立，当前状态为：

```text
M10_DESCENDANT_READINESS_FIXTURE_OBSERVATION_CORRECTION_QUALIFIED
R1_RELATION_SET_ADMISSION_CONTRACT_REQUALIFICATION_IN_PROGRESS
```

这些新事实不解释、覆盖或重写 PR #171 original head 的首败。PR #171 必须从上述 maintenance-qualified
exact main 形成新 head，并独立取得自己的完整门禁；只有第 6 项成立后，RelationSet admission 合同候选才可
进入后继 exact-main/readback 与独立 freeze publication 链。
