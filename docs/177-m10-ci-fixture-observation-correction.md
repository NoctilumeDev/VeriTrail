# M10 CI 夹具端口预约与 Browser 首败诊断修正

> 状态：`CORRECTION_CANDIDATE / R1_OBSERVATION_QUALIFICATION_IMPLEMENTATION_REQUALIFICATION_BLOCKED`
>
> 精确基线：`main@65bdfa0a05f96693a7df9a1a86e27ecdb503b875`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core runtime、Browser collector、公共 Evidence、R1 合同或实现候选

## 1. 触发事实与首败身份

R1 Relation observation/composition qualification private implementation PR
[#165](https://github.com/NoctilumeDev/VeriTrail/pull/165) 的原始 head 为
`015bf8f19ca1269933749c53f67eebe33186bc58`，base 为上述 exact main。它的 diff 只包含
`plugins/review-attention` 私有实现、边界测试与 RQ-001..028 回归；没有修改 Core、M10、Browser、CI 或公共
Schema。原始 Public CI [run 35569800950](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35569800950)
在双 Python 的 normal 450-test step 成立后，于 `-O` step 保留两条不同的正式首败：

```text
Python 3.10 / -O
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_same_sealed_authorities_repeat_without_residual_contamination

services_ready           = true
browser_started          = true
browser_capture_complete = false
browser_completed        = false
cleanup_complete         = true
stop_reason              = COLLECTOR_ERROR
execution_status         = ERROR

Python 3.13 / -O
tests.test_m10_stress_acceptance.M10StressAcceptanceTests.
test_emergency_cleanup_terminates_venv_launcher_tree

expected: selected listener port is occupied before emergency cleanup
actual:   port_is_free(port) == true
```

两条 job 均真正发现并执行 450 tests，各只有上述一项失败；E3 release-download acceptance 与 Workbench 门成功，
后继依赖双 Python job 的 acceptance/wheel/Starter/GitHub Evidence 门被跳过。PR #165 没有 rerun；本维护的任何
绿色也不能把该 attempt 改写为成功。

## 2. 两条失败必须分开归因

### 2.1 Python 3.13：已证实的端口预约 race

旧 emergency-cleanup 夹具先在测试进程里把 loopback `port=0` 解析成一个当时空闲的具体端口，随即关闭
socket；之后才启动 parent/child process tree，并要求 child 绑定先前端口：

```text
probe bind(127.0.0.1, 0)
-> read selected port
-> close probe
-> later launch parent
-> later launch child
-> child bind(selected port)
```

`port_is_free` 只能观察一个瞬时状态，不拥有预约 authority。probe 关闭后，Windows 可把该端口分配给别的
进程或连接；child 也可能在报告 parent PID 以后、真正 `listen()` 以前退出。原断言因而可以在
`terminate_worker_trees(...)` 尚未被调用时失败，不能证明 emergency cleanup 产品行为错误。

### 2.2 Python 3.10：诚实 fail-closed，精确根因仍为 `UNKNOWN`

该 repeat 用例在第一次公共 Run 中已经完成 service readiness，Browser collector 随后 fail closed 为
`COLLECTOR_ERROR`，cleanup 成立。现有 CLI summary 与冻结 runtime.bootstrap Artifact 只保留公共停止原因，
不保留 private `ObservedBrowserCollectionError.error_type`；因此不能从不可变首败恢复是启动、CDP、采样、
Job ownership、response 还是 release 阶段错误。

本地在相同 base 上用 Python 3.10 `-O` 单独运行该测试 1 次成功；随后 5 轮独立测试方法、每轮 2 次真实公共
Run，共 10 次也全部成功。这个诊断只能说明失败未稳定复现，不能把远端红灯降格为偶发，也不能支持某个
未经观察的具体根因。

## 3. 最小修正

### 3.1 listener 自己取得并报告端口

emergency-cleanup child 不再消费由另一个已关闭 socket 猜测的端口。child 自己执行：

```text
bind(127.0.0.1, 0)
-> listen()
-> print(actual bound port, flush=True)
-> sleep while parent/child tree remains alive
```

外层测试读取 actual bound port 后才检查 listener 存在，再调用原 `terminate_worker_trees(...)` 并证明 parent
结束、child listener 消失、端口释放。这里同步的是被测前置条件，不扩大 timeout，不改变 cleanup 语义，也
不以 PID 输出冒充 listener readiness。

### 3.2 只在测试层保留 private collector error type

repeat 用例在调用原 CLI 路径时，用 test-only wrapper 包住既有
`veritrail.bootstrap_run.collect_observed_browser_evidence` seam：

```text
collector success
-> 原值原样返回

ObservedBrowserCollectionError(error_type)
-> 记录 exact private type 到 assertion diagnostic
-> 立即重抛同一异常
-> 产品继续按原合同 fail closed
```

wrapper 不吞异常、不重试、不改变 timeout、Verdict、Evidence 或 cleanup；成功路径另断言 diagnostic 为空。
一个 deterministic sentinel 用例注入 `DiagnosticSentinel` 并证明 CLI 仍返回 `ERROR`、cleanup 成立、测试层
恰好记录该 private type。这里不向公共 Artifact 新增字段，也不声称已经修复 Python 3.10 的未知根因；它只
确保同型失败再次出现时不再只留下 `COLLECTOR_ERROR`。

## 4. 无效推论与停止线

以下推论不成立：

```text
local targeted PASS
!= remote first failure did not happen

current PR does not touch Core
!= every Core failure may be ignored

test-only diagnostic wrapper
!= Browser collector repaired

maintenance PR PASS
!= PR #165 PASS
```

第一次本地 Python 3.13 诊断命令漏掉 Core `src` root，import 在测试执行前因找不到 `veritrail` 失败；修正
`PYTHONPATH` 后才形成正式定向观察。前一次只属于 local gate setup failure，不是产品回归或测试首败。

本维护只有在下列事实串行成立后才可关闭：

1. 最终 diff 只含两个测试夹具、本记录与必要状态导航，不修改 runtime、公共 Schema 或 #165 实现；
2. 两条触发测试与 diagnostic sentinel 在 Python 3.10/3.13 normal/`-O` 四格成立；
3. 完整 `test_bootstrap_run_cli`、M10 stress 与 Core 450-test regression 在双 Python normal/`-O` 成立；
4. 维护 PR 自己的原始 Public CI required checks 全部成功；
5. 维护 PR 受保护合入，新的 exact main Public CI 与 Browser Smoke 原始门全部成功；
6. PR #165 从该 maintenance-qualified exact main 形成新 head，并重新取得自己的完整门禁。

第 5 项以前，状态只能是：

```text
M10_CI_FIXTURE_OBSERVATION_CORRECTION_CANDIDATE
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_REQUALIFICATION_BLOCKED
```

第 6 项以前，不能发布 observation/composition qualification implementation freeze candidate，更不能开始
RelationSet、公共 Schema、Slice、Coverage、publisher、CLI 或 Workbench。

## 5. 当前本地候选证据

三个精确用例（listener、repeat、sentinel）在最小修正后的同一最终代码字节上通过四格：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 3/3 PASS | 8.781s |
| 3.10.6 | `-O` | 3/3 PASS | 9.366s |
| 3.13.13 | normal | 3/3 PASS | 12.734s |
| 3.13.13 | `-O` | 3/3 PASS | 8.596s |

完整 public bootstrap CLI 加 M10 stress 两个 module 也在四格成立：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 27/27 PASS | 56.181s |
| 3.10.6 | `-O` | 27/27 PASS | 56.517s |
| 3.13.13 | normal | 27/27 PASS | 55.446s |
| 3.13.13 | `-O` | 27/27 PASS | 55.846s |

完整 Core current-source 451-test 也在同一最终代码字节上通过四格：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 451/451 PASS | 150.647s |
| 3.10.6 | `-O` | 451/451 PASS | 139.365s |
| 3.13.13 | normal | 451/451 PASS | 135.696s |
| 3.13.13 | `-O` | 451/451 PASS | 136.843s |

该本地门以当前 worktree 的 Core、Starter、GitHub Evidence 与 Review Attention `src` roots 组合运行，证明的是
current-source broader regression；它不冒充远端 installed/editable topology。维护 PR、自身 exact-main Public CI
与 Browser Smoke 仍待执行，因此当前状态不是 correction frozen，也不是 #165 requalified。
