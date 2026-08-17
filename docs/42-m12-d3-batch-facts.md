# M12-D3 Batch 运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
>
> 前置合同：[M12-D3 Batch 双状态矩阵与 Wave 账册表现计划 0.1](41-m12-d3-batch-presentation-plan.md)
>
> 前置事实：[M12-D2 Pairing 运行事实](40-m12-d2-pairing-facts.md)、[M12-R2 Runs 主链表现运行事实](38-m12-r2-runs-presentation-facts.md)
>
> 影响：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`；未触及 `L2_CONTRACT / L3_SYSTEM`

## 1. 已实现的表现关系

`BatchAnalysisView.vue` 已从借用的 `comparison-*` 容器分离，改由仅属 Batch 的 `.batch-*` court、双状态门、
封存 policy 账册、Profile 矩阵、wave/slot 连续账册、判词与边界构成。矩阵新增的
`.batch-matrix-scroll` 只是其具名、本地横向滚动边界；不改变 table、`scope`、`role="region"`、
`aria-label="全因子 Profile 矩阵"` 或 `tabindex="0"` 合同。

三层事实保持分离：

1. `CoverageStatus` 只回答矩阵是否完整可信；
2. `HypothesisStatus` 只回答预注册 outcome 是否成立；
3. wave/slot 继续显示来源 Run 的 `ExecutionStatus / Verdict`，并保留“不证明真实并行”和非统计边界。

窄屏下双状态门和 slot 账册纵向展开；矩阵维持真实 table 的最小宽度，仅在自身 region 内横滚。可见检查发现
Profile 和 slot ID 在窄宽时会黏连为一段文本，随即以私有 `.batch-slot__identity-copy` 的 grid 分组修正；该修正未
影响输入、顺序、裁决或共享状态组件。

## 2. 固定输入与反例

生产验收只读取 Git 忽略的既有 M8 `m8-batch-runtime-v3-20260811` 材料；没有新建 M8/M11 Batch，也没有修改历史
artifact。

| 状态组合 | 输入目录 | 必须保留的事实 |
| --- | --- | --- |
| `COMPLETE / SUPPORTED` | `analyses/supported` | `combined` 的来源 Run 仍为 `FAIL` |
| `COMPLETE / CONTRADICTED` | `analyses/contradicted` | coverage 完整，预注册 outcome 稳定不符 |
| `INCOMPLETE / INCONCLUSIVE` | `analyses/incomplete` | 固定 slot 留在原位且显示 `MISSING` |
| `INCONCLUSIVE / INCONCLUSIVE` | `analyses/inconclusive` | `WAVE_ORDER_MISMATCH` 独立保留在判词 |

四种包都只经既有四文件入口读取。对 `batch-analysis.json` 追加一个字节会得到
`BATCH_SIZE_MISMATCH`，页面不显示部分可信 Batch；显式重新选择完整 `SUPPORTED` 文件才恢复。刷新后得到
`BATCH_RESELECT_REQUIRED`，证明本地文件没有进入 URL、Catalog 或持久化状态。

## 3. 自动化与生产 Chromium

| 门禁 | 结果 | 事实 |
| --- | --- | --- |
| Batch 局部回归 | `8/8 PASS` | 四态、来源 `FAIL`、缺格、判词、长 Profile ID、顺序、matrix region 与原生 details |
| Workbench 回归 | `67/67 PASS` | 全量组件、Loader 与 App 回归 |
| lint / type-check / production build | `PASS` | 零 warning；最终生产 CSS/JS 构建成功 |
| `m12_d3_batch_acceptance.py` | `9/9 PASS` | 1440px、390px、360px；四态、顺序、历史、损坏恢复、刷新重选、局部滚动、溢出、Console/Network 与清理 |
| 同一脚本 `python -O` | `9/9 PASS` | 所有硬门禁使用显式 `require()`，不依赖优化模式移除的内建 `assert` |

两轮生产脚本复用 M11 Gate B 只读 Catalog，分别使用独立回环端口和输出目录。每轮都记录 `16` 个同源成功
`GET`：外部请求、写请求、HTTP error、Console warning/error、page error 与 request failure 均为 `0`。完成后端口释放、
服务线程停止，Catalog 无 SQLite `-wal/-shm` sidecar。

## 4. Codex 内置浏览器

用户在运行中的内置浏览器真实选择 `SUPPORTED` 的四个本地 Batch 文件，并完成物理键盘验收：

- `CoverageStatus = COMPLETE` 与 `HypothesisStatus = SUPPORTED` 同时显示，来源 `COMPLETED / FAIL` 仍在 wave ledger 内可见；
- 根横向溢出为 `0px`；矩阵 region 从 `scrollLeft 0` 实际横向滚到 `76.7px`，而根页面没有随之横移；
- 用户以系统 `Tab` 进入矩阵，按左右方向键在本地矩阵中滚动，并展开一个原生 `Outcome` `details`；
- 刷新后页面要求重新选择本地文件，Console 无 warning/error。

内置浏览器只提供真实可见导入、物理键盘、局部滚动、原生交互和响应式证据。response Network 与 Console 的可重复
结论仍来自生产 Chromium/CDP；没有把内置浏览器冒充为 F12 response 抓包。

## 5. 范围与下一入口

D3 不证明 Batch 的统计效度、真实微并行、M11 中真实 Batch、Browser Evidence 终稿、全局 loading/error、
forced-colors、200% zoom、色觉差异、M12 冻结、版本标签或发布。没有修改 `App.vue`、Core、Schema、Catalog/API、
domain、裁决规则、共享 `StatusBadge.vue` 或安全边界。

M12-D 已关闭，M12 仍是 `IMPLEMENTING / NOT_FROZEN`。唯一下一入口是先建立 M12-E 的独立计划；D3 的通过不构成
Browser Evidence、全局状态或 M12 终稿的完成结论。
