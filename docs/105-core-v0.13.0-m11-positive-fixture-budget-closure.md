# Core 0.13.0 M11 正向夹具预算修正闭环事实

> 状态发布目标：`M11_POSITIVE_FIXTURE_BUDGET_CORRECTION_CLOSED / C2_READY / CORE_0.13.0_NOT_RELEASED / P4_BLOCKED`
>
> 状态发布重建基线：`main@43c8e9105adf84641d203514594d3e0c5a1251e8`
>
> 本文只记录[文档 104](104-core-v0.13.0-m11-positive-fixture-budget-correction.md)的最小测试夹具修正已经
> 取得的本地、PR、主线与匿名公开读回事实；本状态发布自己的原始门禁、受保护主线合入和合入后
> exact-main 读回全部成立后，C2 才恢复施工资格。

## 1. 被保留的反例

Core 0.13.0 候选 PR [#79](https://github.com/NoctilumeDev/VeriTrail/pull/79) 原始 Public CI 11/11
成功并合入 `main@a5ba0e1bd8f181851db83de611981524da1da8f5`。该 exact main 的首轮
[Public CI run 34295582018](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34295582018)
在 Python 3.13 `-O` 下得到约 18.125 秒的正向真实浏览器链，并由夹具的 15000 ms 外层生命周期正确
终止。失败没有被 rerun、删除或改称偶发；同一 SHA 的
[Browser Smoke run 34295582009](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34295582009)
成功，也没有被用来覆盖 Public CI 失败。

该反例只证明正向 M11 夹具混入了未冻结的 15 秒 wall-clock 期待，不证明 Core 生命周期、Browser
单操作 timeout 或清理预算存在产品缺陷。

## 2. 最小修正与本地证据

修正提交 `1b7640739f4a493177e191b27732d8b4790ef35c` 只把 M11 正向双 viewport 真实 Chromium
夹具的外层有界 fail-safe 从 15000 ms 恢复为 120000 ms，并记录边界；没有修改生命周期实现、取消、
中断、清理、Browser 单操作 timeout、Acceptance 语义、发行身份或 P4 合同。

在明确绑定当前 worktree 的 Core、Starter 与 GitHub Evidence 源码坐标后：

- 精确 M11 正向 CLI、生命周期与 Browser 定向集合共 20 项，在 Python 3.10/3.13 的 normal 与
  `-O` 四组全部通过；
- Core 全量 416 项在相同四矩阵全部通过；
- `git diff --check`、变更文档本地链接检查与私有路径/令牌/私钥扫描通过。

这些结果证明最小修正在本地没有破坏专门拥有 deadline/cancellation 语义的测试，但不替代远端门禁。

## 3. PR 与 exact-main 门禁

1. PR [#80](https://github.com/NoctilumeDev/VeriTrail/pull/80) 精确绑定修正提交
   `1b7640739f4a493177e191b27732d8b4790ef35c`；
2. PR #80 原始
   [Public CI run 34297611554](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34297611554)
   在 attempt 1 完成 11/11 success，没有 rerun；
3. PR #80 经受保护主线合入 merge commit
   `43c8e9105adf84641d203514594d3e0c5a1251e8`；
4. 合入后的
   [Public CI run 34298465734](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34298465734)
   在同一 exact head、attempt 1 完成 11/11 success；
5. 同一 exact head 的
   [Browser Smoke run 34298465714](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34298465714)
   完成 1/1 success。

这条新因果链修复并复验了失败夹具；它不抹去 `34295582018`，也不把 CI 构建物升级为 Core 0.13.0
公开发行资产。

## 4. exact-main 匿名公开读回

从 `main@43c8e9105adf84641d203514594d3e0c5a1251e8` 建立 clean detached worktree，使用仓库内
P2 Public Render Collector 为 README 与文档 104 分别建立 sealed Plan 和独立 fresh anonymous
Chromium context。两次初态均为 `cookies=0 / origins=0`，requested/final URL 保持同一 exact-SHA
Markdown 坐标。

| 页面 | Coverage | 三样本 | 字面标记 | 请求数 | Facts digest |
| --- | --- | --- | --- | ---: | --- |
| exact README | `COMPLETE` | stable | `M11 正向真实浏览器夹具` × 1 | 150 | `531f26ccbe022a90b77455059fff9993e5f12c13c0f31cd37a85e6ea85f5e563` |
| exact 文档 104 | `COMPLETE` | stable | `Core 0.13.0 M11 正向夹具预算修正` × 1 | 141 | `6770c1bc6dbcdad06292a37557834025647abb74010d5bca35dd3c9513f5910e` |

两条读回都没有 coverage conflict、Collector error 或 cleanup error。它们证明该 exact main 的公开页面
保留修正事实，不证明 Core 0.13.0 tag、Release、最终资产或匿名下载已经存在。

## 5. 边界与下一步

本状态发布自己的原始门禁、主线合入与合入后 exact-main 读回成立后，M11 修正才能闭环，C2 才可以从
新的 exact main 重新构建最终 Core 0.13.0 资产。C2 仍必须独立完成[文档 102](102-core-v0.13.0-release-candidate-plan.md)
第 5–7 节的构建、摘要、clean install、公开下载与停止线；不得复用 C1 候选字节。

在 C2 建立 `v0.13.0` 的真实公开坐标并完成匿名读回以前：

```text
CORE_0.13.0_NOT_RELEASED
NO_CORE_0.13.0_TAG_OR_RELEASE
P4_BLOCKED
NO_GITHUB_EVIDENCE_TAG_OR_RELEASE
```

因此本轮解除的是 M11 修正阻断，不是 P4 阻断，也不提前修改 Release 下载恢复策略、资产身份、摘要
语义或插件发布坐标。
