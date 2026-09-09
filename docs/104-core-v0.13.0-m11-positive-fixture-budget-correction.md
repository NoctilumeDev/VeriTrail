# Core 0.13.0 M11 正向夹具预算修正

> 状态：`CORRECTION_CANDIDATE / CORE_0.13.0_NOT_RELEASED / P4_BLOCKED`
>
> 精确基线：`main@a5ba0e1bd8f181851db83de611981524da1da8f5`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core 生命周期、Browser、Acceptance 或发布语义

## 1. 触发事实

Core 0.13.0 候选 PR
[#79](https://github.com/NoctilumeDev/VeriTrail/pull/79) 的原始 Public CI 11/11 成功，并以
`a5ba0e1bd8f181851db83de611981524da1da8f5` 合入主线。同一 exact main 的 Browser Smoke
[`34295582009`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34295582009) 成功；但 Public CI
[`34295582018`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34295582018) 在 Python 3.13
`-O` 的 M11 单应用正向 CLI 用例停止。

失败保留的 pre-teardown 事实为：

```text
services ready                 182.894 ms
browser exercise completed  18125.040 ms
ready callback completed     18125.047 ms
lifecycle timeout observed   18125.058 ms
```

Browser 已完成且清理完整，但夹具封存的外层生命周期只有 15000 ms，因此 Core 正确产出
`LIFECYCLE_TIMEOUT / ABORTED / PENDING`，与该正向测试期待的 `NONE / COMPLETED / PASS` 冲突。
Python 3.10 的同一主线门成功；本机 Python 3.13 `-O` 隔离复验三次分别约 2.1–2.3 秒完成。以上事实
不能证明共享 runner 的内部负载根因，也不能把失败称为偶发。

## 2. 模型缺口

该测试验证的是：

```text
sealed single-application plan
-> real service
-> two real Chromium viewports
-> staged runtime.bootstrap Evidence
-> public PASS Bundle
```

但测试夹具又把 `lifecycle_timeout_ms` 从通用正向配置的 120000 ms 收紧为 15000 ms。Browser 合同为
每个 Playwright 操作保留 10000 ms 上限，并串行执行两个 viewport；不存在“整个正向浏览器链必定在
15000 ms 内完成”的冻结性能承诺。因此旧测试同时混入了一个未声明的 wall-clock SLO：

```text
functional correctness
        +
unowned 15-second performance expectation
```

实现忠实执行生命周期合同；不自洽的是正向夹具预算与测试所要求的真实工作量。该缺口不同于曾经的
cleanup deadline 重复刷新：本次没有发现产品预算被重新创建，也没有证据支持放宽任何公开阈值。

## 3. 最小修正

只把 M11 正向夹具的外层生命周期 fail-safe 恢复为 120000 ms，与通用 bootstrap profile、Starter 与
Authoring 真实黄金路径保持同一有界量级。真正验证 deadline、取消、中断和清理上限的定向测试不变；
Browser 单操作 timeout、CI job timeout、产品默认值与所有公开合同也不变。

因此：

```text
positive functional timeout
!=
performance acceptance threshold
```

## 4. 必需证据与停止线

本修正必须串行证明：

1. 精确 M11 正向 CLI 用例在 Python 3.10/3.13 的 normal 与 `-O` 下通过；
2. 生命周期 deadline、取消、Browser interruption 与 cleanup 定向测试仍通过；
3. Core 全量 416 项在双 Python normal/`-O` 四矩阵通过；
4. 候选 PR 原始 Public CI 11/11 成功；
5. 合入后新的 exact main Public CI 11/11 与 Browser Smoke 1/1 成功。

在第 5 项成立前，C2 不得构建最终资产、创建 `v0.13.0` 标签或 Release，P4 继续阻断。第一次主线
失败不通过 rerun 洗白；修正必须以新的提交、PR 和 exact-main 事实建立独立因果链。
