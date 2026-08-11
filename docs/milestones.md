# VeriTrail 里程碑冻结历史

## 1. 用途

本文件承接 README 不再展开的 M0–M8 历史。它记录每个冻结基线回答的问题、真实取得的证据、
明确没有证明的能力，以及必须继续保留的失败事实。

里程碑标签实际指向的 Git 提交是版本寻址权威；实现提交、合同提交、运行哈希和完整退出条件
仍以对应的里程碑文档为准。下表中的标签与提交已于 2026-08-11 从 `origin` 核验。

## 2. 冻结索引

| Milestone | Capability | Status | Frozen ref |
| --- | --- | --- | --- |
| M0 | 封存单变量计划、结构化证据、确定性 Verdict 与开放报告 | `FROZEN` | `m0-v0.1.0` @ `6367843` |
| M1 | 启动前资源采样、`PROCEED / STOP_ESCALATION / ABORT` | `FROZEN` | `m1-v0.2.0` @ `a9b795e` |
| M2 | 回环站点的有界 Chromium、Console/Network/截图证据 | `FROZEN` | `m2-v0.3.0` @ `fbaaf71` |
| M3 | 本地只读 Vue Workbench 与“宫阙验迹”CSS 主题 | `FROZEN` | `m3-v0.4.0` @ `e46f633` |
| M4 | 可重建 SQLite Run Catalog、只读 API 与轻量自举 | `FROZEN` | `m4-v0.5.0` @ `d095057` |
| M5 | `STATIC_HTTP` 目标的有界生命周期与单一 `run` 入口 | `FROZEN` | `m5-v0.6.0` @ `d3b9cd7` |
| M6 | 同 sealed Plan 的不可变 Run 确定性比较 | `FROZEN` | `m6-v0.7.0` @ `807ef1e` |
| M7 | 固定四角色、预注册 outcome 的配对反事实分析 | `FROZEN` | `m7-v0.8.0` @ `e5c6e27` |
| M8 | 4–16 格全因子 Profile 与固定种子扰动分析 | `FROZEN` | `m8-v0.9.0` @ `c6fbd73` |

`FROZEN` 只对该行声明的能力和对应文档中的环境、输入、资源及安全边界成立。代码、依赖、
Schema、数据、拓扑、浏览器或规则越过容差时，旧结论必须标记过期并重新验收。

## 3. 证据与边界

| Milestone | 真实取得的关键证据 | 明确没有证明 |
| --- | --- | --- |
| M0 | 双 Python 自动化、5 个真实 CLI Run、四类 Verdict、证据包与清单哈希 | 资源、浏览器、数据库、组合矩阵或项目执行 |
| M1 | 三类真实预检、M0 兼容、资源中止与观察者开销 | 工作负载执行、运行中监控或自动清理外部服务 |
| M2 | 正/负真实 Chromium、Codex 内置浏览器、附件哈希与清理 | 被测站点生命周期、远程认证或并行 Context |
| M3 | 生产构建、桌面/移动、正负/损坏包、本地导入与同源网络 | SQLite、API、计划编辑、执行编排或完整自举 |
| M4 | Catalog 确定性重建、只读 SQLite/API、两阶段自举与源变化隔离 | 跨 Run 比较、任意被测对象启动或通用元数据写模型 |
| M5 | 正/负真实 Run、ABORT/STOP、端口竞争、源变化与目标清理 | Shell、npm/Maven、Docker、真实后端或中间件编排 |
| M6 | `MATCH / DRIFT / INCONCLUSIVE`、逐字节复建与来源损坏拒绝 | 处理效果、跨变量因果、自动挑选 Run 或统计结论 |
| M7 | 四角色三态、恢复基线、负对照、Catalog 隔离与浏览器验真 | 组合变量、统计显著性、任意配对或跨批次聚合 |
| M8 | 8 个独立 M5 Run、四类批次状态、固定种子、来源 `FAIL` 保留与人工键盘终验 | 组件级多变量因果、真实并行、生产容量或任意项目命令 |

M8 的 wave 仍由验收脚本串行执行，冻结结论固定为
`runtime_overlap_claim=NOT_PROVEN`。它证明有界调度、Assignment 和分析语义，不证明同一 wave
中的 Run 曾经真实时间重叠。

## 4. 必须保留的失败事实

这些反例是冻结证据的一部分，不能在整理历史或美化演示时删除：

- M4：自举 Plan v1 的 `PASS` 选择器同时匹配目录卡片与详情状态门；失败 Run 保留，Plan v2
  只收窄选择器后重新验收；
- M5：首轮合法 query 被错误裁为 400；合同没有后移，修复为文件查找忽略 query、账册只保存
  脱敏 path，并保留原失败 Run；
- M6：损坏 Comparison 与预览端口残留用于证明输出隔离和清理门禁；
- M7：目录选择器在 Codex 内置浏览器中没有触发导入；入口改为显式选择四个文件，失败事实
  与修复后的终验同时保留；
- M8：第一次用裸静态服务器启动 Workbench 产生 `/api/v1/catalog` 404，该轮被判失败并丢弃；
  生产 `catalog-serve` 重跑后才形成浏览器证据。内置浏览器控制面不能合成 `Tab`，最终由真实
  Chromium 自动化和用户在内置浏览器中手动按一次系统 `Tab` 共同完成键盘验收。

## 5. 当前能力边界

M0–M8 已冻结的是一条逐层增长的本地验收链：

```text
Plan / Evidence / Verdict
  -> Resource preflight
  -> Browser evidence
  -> Read-only Workbench
  -> Local Run Catalog
  -> Bounded static target lifecycle
  -> Deterministic rerun comparison
  -> Four-role paired analysis
  -> Full-factorial batch analysis
```

当前仍未实现：

- 计划编辑器与在线写；
- 任意项目命令、Shell、npm/Maven、Docker 或中间件生命周期；
- wave 内真实微并行执行；
- 完整 v0 自举与第二个不同类型项目证明；
- 统计显著性、生产容量结论和 AI 裁决。

后继里程碑可以提前规划，但只有当前冻结标签仍有效、且新实现没有越过其兼容容差时，才能
消费这些基线。发现范围上浮时必须回到所有者、消费者和证据矩阵重新评审。

后继阶段的 [Post-M8 收束路线 Plan v1](13-post-m8-roadmap.md) 已以
`post-m8-plan-v1` 冻结为规划基线；M10–M14 仍为 `PLANNED`。M9 受控项目命令执行合同 0.2 已在
`290b618` 进入 `CONTRACT_FROZEN`；`4d2bc84` 完成 Plan 0.5、ToolBindings 0.1、CommandPreview 0.1
与只读 CLI，`9f979c8` 完成锁定 `pywin32==312` 的 Windows Job Object 所有权后端和真实 helper
自动化，`fa27b51` 完成 Plan 0.5 `run`、严格 `runtime.command`、最终状态漂移阻断、文本附件
脱敏和 Bundle/Catalog/API/Workbench 通用读回自动化。`9031719` 新增两个独立轻量 Subject 与真实
验收矩阵；Python module、直接 `node.exe` script、重复 Run、适用负向、桌面/移动 Chromium、
Catalog/Workbench、Console/Network 和双运行时回归已通过。内置浏览器物理键盘、最终清理、冻结
提交及 `m9-v0.10.0` GitHub 远端标签读回仍不存在，不能把当前真实中间状态写成里程碑完成。

## 6. 详细文档

- [M0 纵向切片](04-m0-vertical-slice.md)
- [M1 资源与环境预检](05-m1-resource-preflight.md)
- [M2 真实浏览器证据](06-m2-browser-evidence.md)
- [M3 Vue 证据工作台](07-m3-vue-workbench.md)
- [M4 本地 Run 目录与轻量自举](08-m4-local-run-catalog.md)
- [M5 有界运行编排与静态目标生命周期](09-m5-bounded-run-orchestrator.md)
- [M6 同计划复跑确定性比较](10-m6-deterministic-rerun-comparison.md)
- [M7 预注册四角色配对反事实分析](11-m7-preregistered-paired-analysis.md)
- [M8 预注册全因子批次矩阵与固定种子扰动](12-m8-preregistered-batch-matrix.md)
- [M9 受控项目命令执行合同](14-m9-controlled-command-execution.md)
