# M10 公共自举正向夹具生命周期预算对齐

> 状态：`CORRECTION_CANDIDATE / R1_SCHEMA_FREEZE_PUBLICATION_BLOCKED`
>
> 精确基线：`main@49a2d69d44cca21024808fe5c298db8bac7f64c4`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core 生命周期、Browser、Acceptance 或 R1 Schema 语义

## 1. 触发事实

R1 Schema 合同已由 PR #99 的原始 11 项门禁合入精确主线
`49a2d69d44cca21024808fe5c298db8bac7f64c4`，该主线的 Public CI、Browser Smoke 与三次匿名产品读回
均已成立。后继 docs-only 冻结状态发布 PR
[#100](https://github.com/NoctilumeDev/VeriTrail/pull/100) 没有修改生产代码或测试，但其原始 Public CI
[run 34471577377](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34471577377) 在 Python 3.10
`-O` 的第二次公共自举正向运行停止：

```text
test_same_sealed_authorities_repeat_without_residual_contamination

browser_capture_complete = true
browser_completed        = true
services_ready           = true
cleanup_complete         = true
stop_reason              = LIFECYCLE_TIMEOUT
execution_status         = ABORTED
verdict                  = PENDING
```

同一门的普通 Python 3.10 与 Python 3.13 normal/`-O` 成立；本地精确绑定当前 worktree 的 Python 3.10
`-O` 两次复验也分别完成为 `COMPLETED / PASS`。这些事实不能把远端失败改称偶发，也不能证明共享
runner、代理、Chromium 或操作系统的单一根因。PR #100 因而保持未合入，后继门禁不得通过 rerun
覆盖该失败。

## 2. 模型缺口

失败测试使用 `tests.support.bootstrap_profile()` 建立共享 M10 公共自举夹具。该通用正向配置明确提供
120000 ms 的有界外层 lifecycle fail-safe，但夹具随后把它收紧为 15000 ms，并连续运行两次真实服务与
Chromium 链。测试要求证明的是：

```text
same sealed authorities
-> two independent public runs
-> COMPLETED / PASS
-> first Bundle remains immutable
-> no process, port or staging residue
```

它没有预注册“每次完整正向链必须在 15 秒内结束”的性能目标。Core 在真实链超过该隐藏阈值时产出
`LIFECYCLE_TIMEOUT / ABORTED / PENDING`，属于忠实执行封存 Profile；不自洽的是夹具同时要求功能完成，
又给同一功能链附加了无所有者的 wall-clock SLO。

该缺口与[文档 104](104-core-v0.13.0-m11-positive-fixture-budget-correction.md)和
[文档 105](105-core-v0.13.0-m11-positive-fixture-budget-closure.md)已经裁决的 M11 反例同构。先前修正只覆盖
M11 单应用正向夹具；M10 公共自举夹具自提交 `f397135af17bee3cf7974b64ec990824980a33ee` 起保留了同类
15000 ms 覆盖，因此这次失败属于既有测试证据边界债务，不属于 R1 Schema 回归。

## 3. 最小修正

共享 M10 公共自举夹具不再覆盖 `bootstrap_profile()` 的 120000 ms 有界外层 fail-safe，并增加一个不启动
进程或浏览器的确定性守卫，证明生成的 sealed Profile 继续保留该规范预算。真正拥有时间语义的生命周期
deadline、取消、Browser interruption、cleanup 与资源停止测试保持不变。

因此：

```text
positive functional fail-safe
!=
performance acceptance threshold
```

本修正不改变：

- Core 生命周期或单一绝对 deadline 的实现；
- Browser 单操作 timeout、readiness timeout、取消与逆序清理边界；
- Plan/Profile Schema、Evidence、Verdict 或 Catalog 语义；
- R1 Schema 合同候选、冻结标准或后继 payload 施工权限。

## 4. 必需证据与停止线

本修正必须串行取得：

1. 新增 fixture budget 守卫在 Python 3.10/3.13 的 normal 与 `-O` 下成立；
2. 精确 repeat 正向用例在同一四矩阵成立；
3. lifecycle deadline、取消、Browser interruption 与 cleanup 定向测试不变且成立；
4. Core 全量回归在双 Python normal/`-O` 四矩阵成立；
5. 独立修正 PR 的原始 Public CI 11/11 成功；
6. 合入后的新 exact main Public CI 11/11 与 Browser Smoke 1/1 成功。

第 6 项成立以前，不得重新发布 R1 Schema 冻结状态，不得启动 Schema payload，也不得把 PR #100 的失败
重解释为 R1 合同失败。地基修正闭环后，冻结状态发布必须从新的 exact main 重建并取得自己的完整门禁。
