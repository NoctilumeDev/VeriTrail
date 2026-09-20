# M10 listener owner mismatch 测试夹具时序修正

> 状态：`CORRECTION_CANDIDATE / R1_OBSERVATION_QUALIFICATION_CONTRACT_REQUALIFICATION_BLOCKED`
>
> 精确基线：`main@559bf9b9a052f0b542227b1cea069dd15c696cc8`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core 生命周期、readiness、cleanup、R1 合同或公共产品语义

## 1. 触发事实与首败身份

R1 Declared Relation Observation Domain / Composition Qualification docs-only 候选 PR
[#160](https://github.com/NoctilumeDev/VeriTrail/pull/160) 的 head
`44caffaa08ab67bcb83760d86bdbad7e30081b6f` 只修改四份 Markdown。它的原始 Public CI
[run 35530411983](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35530411983) 在 Python 3.13
真正发现并执行 450 tests 后，由既有公共自举用例停止：

```text
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_listener_owner_mismatch_aborts_without_killing_external_listener

subtest: node='application'
expected: LISTENER_OWNERSHIP_MISMATCH
actual:   READINESS_TIMEOUT
```

同一候选的 Python 3.10 job 成功；精确 base `main@559bf9b...` 的 Public CI
run `35527351489` attempt 1 曾在 Python 3.13 normal 与 `-O` 下通过同一用例。上述差异不能把
PR #160 attempt 1 的失败删除、降格或改称没有发生。准确归因是：该正式 CI attempt 在当时测试夹具下
合法失败；后继诊断把原因定位到既有测试时序假设，而不是 docs-only 合同差异。

PR #160 不在旧 head 上 rerun 洗白。它继续停止，直到本维护候选取得自己的独立资格并合入新 exact main，
再绑定新的 source snapshot 重新接受完整门禁。

## 2. 失败模型

旧夹具在调用 `run_observed_bootstrap(...)` **之前**启动存活 `1.5s` 的外部 listener。dependency 争议场景会
很快进入目标 readiness；application 争议场景却必须先完成 dependency readiness。于是同一个寿命参数同时
包含了两类时间：

```text
fixture 建立外部 owner
-> 前置非争议节点耗时
-> 争议节点真正开始 readiness
-> listener ownership probe
```

当共享 runner 较慢时，前置 dependency 会消耗 application 外部 listener 的大部分或全部寿命。争议节点开始
探测时端口已经自然释放，产品只能诚实走到 `READINESS_TIMEOUT`；夹具却要求观察
`LISTENER_OWNERSHIP_MISMATCH`。测试因此把“外部 owner 在争议节点 readiness 内存在”绑定到了更早且无关的
前置阶段耗时。

这个事实不改变冻结产品语义。原用例仍必须同时证明：

1. VeriTrail 观察到 listener owner 不属于当前 Job 时拒绝 READY；
2. VeriTrail 不接管或终止外部 owner；
3. 外部 owner 在既有 cleanup deadline 内自行退出，端口最终释放。

## 3. 被反例否定的修法

第一项本地诊断曾把外部 listener 寿命延长到 `30s`，并要求 Run 返回时它仍存活。目标用例随后在 dependency
与 application 两个子场景都合法得到 `CLEANUP_ERROR`：sealed cleanup 预算要求争议端口在 deadline 内释放，
而持续存活的外部 owner 使该条件不成立。

```text
原假设：延长 external listener lifetime 可以消除 readiness race。
实际事实：跨过 cleanup deadline 的外部 listener 会合法触发 CLEANUP_ERROR。
修正结论：不能扩大 listener 生命周期；必须修正建立 listener 的观察坐标。
```

这次本地诊断没有进入提交或远端门禁，不是 PR #160 的第二个正式失败。它作为 invalidated assumption 保留，
防止后继用更长 timeout 或更宽 cleanup 掩盖同一夹具问题。

## 4. 最小修正

测试继续调用冻结的 `probe_owned_http_readiness`。它只增加一个测试层 wrapper：当 disputed node 的真实
readiness adapter 被调用，且 `session.port` 等于本子场景封存的 contested port 时，才建立既有
`serve-for 1.5` 外部 owner，等待该端口开始监听，再委托原 readiness probe。

```text
when disputed node enters its readiness phase
-> establish external owner for the sealed contested port
-> wait until the listener is observable
-> delegate to frozen owned-readiness adapter
```

注入条件不依赖“第 N 次调用”、私有函数名或偶然调用顺序；它绑定封存 session 的 disputed port 与既有
readiness seam。`1.5s` 自然退出和 `external.wait(timeout=3) == 0` 保持不变，因此 no-kill 与 cleanup-release
两个目标仍同时受观察。

本修正不改变：

- runtime、Schema、Evidence、Verdict、Plan/Profile 或公共 API；
- readiness、lifecycle、cleanup 或 cancellation deadline；
- listener owner mismatch 的错误分类与 fail-closed 行为；
- PR #160 合同内容、R1 authority 或 RelationSet/Slice/Coverage 施工权限。

## 5. 本地候选证据

精确目标用例在 CPython 3.10/3.13 normal 与 `-O` 四格均为 1/1 PASS：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 1/1 PASS | 6.605s |
| 3.10.6 | `-O` | 1/1 PASS | 6.347s |
| 3.13 | normal | 1/1 PASS | 6.791s |
| 3.13 | `-O` | 1/1 PASS | 7.425s |

完整 `tests.test_bootstrap_run_cli` 在同一四格均为 23/23 PASS：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 23/23 PASS | 79.507s |
| 3.10.6 | `-O` | 23/23 PASS | 90.894s |
| 3.13 | normal | 23/23 PASS | 57.990s |
| 3.13 | `-O` | 23/23 PASS | 54.081s |

Core broader regression 又显式把 `veritrail`、Starter、GitHub Evidence 与 Review Attention 四个 package 的
`src` root 绑定到本维护 worktree；`__file__` probe 证明四个 import 都来自该 worktree。450-test command 在
四格均发现 450 tests 并成功结束：

| Python | mode | result | elapsed |
| --- | --- | --- | ---: |
| 3.10.6 | normal | 450-test suite PASS | 143.124s |
| 3.10.6 | `-O` | 450-test suite PASS | 145.424s |
| 3.13 | normal | 450-test suite PASS | 133.946s |
| 3.13 | `-O` | 450-test suite PASS | 135.255s |

这些结果只证明 **local current-source broader regression**。source identity 正确不等于 installation topology
与 Public CI 相同；本地 `PYTHONPATH` 组合不能冒充 wheel/install/runner 资格。维护 PR 自己的远端 Public CI
负责证明 installed-product/CI topology。

第一次 broader 命令只加入 Core `src`，在 discovery 阶段因缺少 `veritrail_github` 得到 440-test import
error。该命令没有复刻完整四 package source topology，也没有形成预期的 450-test observation，因此只保留为
local gate setup failure，不是产品回归失败或可用于维护资格的测试结果。

## 6. 停止线

本维护只有在下列事实串行成立后才可关闭：

1. 最终 diff 只含测试夹具与本维护记录，没有 runtime、timeout 或合同改动；
2. 维护 PR 自己的原始 Public CI required checks 全部成功；
3. 维护 PR 通过受保护 `main` 合入；
4. 新 exact main 的 Public CI 与 Browser Smoke 原始门全部成功。

第 4 项成立以前，状态只能是：

```text
M10_LISTENER_OWNER_MISMATCH_FIXTURE_CORRECTION_CANDIDATE
R1_OBSERVATION_QUALIFICATION_CONTRACT_REQUALIFICATION_BLOCKED
```

地基维护闭合后，PR #160 必须吸收新 main，形成新的 head SHA，并在该新 source state 上取得独立完整门禁。
维护 PR 的绿色不能解释成 PR #160 已经绿色；PR #160 attempt 1 的 Python 3.13 失败继续作为历史事实保留。
