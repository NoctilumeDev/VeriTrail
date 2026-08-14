# M12-B 四向公共视图与十字中轴骨架运行事实

> 状态：`SLICE_IMPLEMENTED_AND_RUNTIME_VALIDATED / M12_NOT_FROZEN`
> 日期：2026-08-14
> 前置冻结基线：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
> 施工合同：[M12-B 四向公共视图与十字中轴骨架 0.1](30-m12-b-cross-axis-navigation.md)
> 影响事实：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止误读：本文不冻结 M12，不创建版本或标签，也不证明 M12-C 至 M12-F 已完成。

## 1. 本切片结论

M12-B 已将 M11 Workbench 的公共信息空间从“Catalog 永远先于所有分析”改为四个互斥公共视图：
北向 `Runs / Catalog`、南向 `Rerun Comparison`、西向 `Paired Analysis`、东向 `Batch Analysis`。
Run 详情、Browser Evidence 与原始证据仍属于 Runs；四类本地导入入口只在所属视图可见。

十字中心是原生 button，收拢时只有中心进入焦点顺序；展开后 DOM/Tab 顺序为中心、北、东、南、西。
方向键按几何位置移动焦点，`Esc` 收拢并回到中心。选择入口后，当前公共视图写入 URL、十字收拢且
焦点进入目标视图标题。Runs 保持 Catalog/Run 的既有 URL、返回焦点、只读 Loader 与 Bundle 验真；
Comparison、Pairing、Batch 的已有 `?fixture=` 刷新后重选语义未改变，未选择本地文件时新增
`?view=` 只表达公共空视图。

本切片没有修改 `src/veritrail`、`web/src/domain/`、Schema、Verdict、Evidence、Catalog、Comparison
生产逻辑或只读 API。它没有新增全局状态库、路由框架、远程资源、写能力或主题颜色体系。

## 2. 实现与测试边界

| 位置 | 事实 |
| --- | --- |
| `web/src/components/CrossAxisNavigation.vue` | 独立拥有十字的展开、焦点、方向键和窄屏几何；使用高对比线框，不接管 M12-C 色彩与最终样式 |
| `web/src/App.vue` | 新增仅表现层的 `PublicView` 投影；既有 `activeSource` 继续拥有 Loader 来源语义 |
| `web/tests/cross-axis-navigation.test.ts` | 覆盖收拢焦点、展开后的 DOM 顺序、方向键、Esc 与四个固定选择事件 |
| `web/tests/app.test.ts` | 覆盖相关导入入口的公共视图归属，并保留正/负/损坏 Bundle 与三种分析导入验真 |
| `scripts/m11_gateb_workbench_acceptance.py` | 基于真实 M11 Gate B 数据，增加四个公共视图、方向键、焦点、URL、Catalog 隔离及移动展开无溢出门禁 |

## 3. 严格串行自动化事实

在 Windows 11、16 GB 主机上严格串行完成；未启动 Docker、中间件或第二个项目栈。

| 门禁 | 最终事实 |
| --- | --- |
| Workbench unit/component | 9 files，`63/63` tests passed |
| ESLint | `--max-warnings=0` 通过 |
| TypeScript | `vue-tsc` 与 Node `tsc` 通过 |
| Production build | 38 modules；CSS 42.67 kB / gzip 7.76 kB；JS 177.55 kB / gzip 54.88 kB |
| M11 Gate B production Workbench | `COMPLETED / PASS`，10 项检查 |
| Chromium | 151.0.7922.34；桌面 1440 x 960、移动 390 x 844 |
| Network | 113 requests；HTTP error 0；external origin 0；write request 0 |
| Browser runtime | Console error 0；page error 0；request failure 0 |
| 自动验收清理 | 服务线程停止、端口释放、SQLite sidecar 0 |

最终自动输出为 Git 忽略目录
`artifacts/m12-b-cross-axis-workbench-r4/acceptance.json`。它使用同一份 M11 Gate B 四个真实 Run、隔离
损坏候选及真实 `MATCH` Comparison；不是 Mock 或截图替代品。

## 4. 内置浏览器运行事实

### 4.1 桌面公共视图与历史

- 在 `1440 x 960` 实际生产工作台中，北入口 `ArrowRight` 后焦点确实进入东入口；`Esc` 后
  `aria-expanded=false`；
- 选择南向后 URL 为 `?view=comparison`，页面只显示 Comparison 的本地导入和空状态，Catalog DOM 为 0；
- Browser Back 回到根 Catalog，Forward 返回 `?view=comparison` 与对应空状态；
- 西向与东向也分别显示其对应的文件选择入口，随后回到北向的标题和 Catalog；
- 从真实 `m11-gateb-v2-ink-positive-01` Run 进入详情，状态仍为 `COMPLETED / PASS`，Core 裁决已核验、
  Browser Evidence 存在、根级溢出为 0；返回 Catalog 后，原 Run 行重新获得焦点。

### 4.2 移动内容压力

初次移动实测发现两个实现缺口，而不是把“定义”当作事实：

1. 390 px 展开十字时，三列的固定中轴最小宽度造成 53 px 根级横向溢出；
2. 第一处修复后虽无溢出，但中心最小宽度压住东西两翼的触控边界。

修复后以真实页面复测：

| 视口 | 展开根级溢出 | 中心与东西入口 | 结论 |
| --- | ---: | --- | --- |
| 390 x 844 | 0 px | 不相交 | PASS |
| 320 x 844 | 0 px | 中心右边 206 px，东入口左边 215 px；中心左边 114 px，西入口右边 105 px | PASS |

窄屏不缩小触控高度；文字在有限宽度内自然换行。该结构事实不等于最终视觉密度或色彩已经冻结。

### 4.3 Console 与网络边界

- 内置浏览器最终 Console `error/warn` 为 0；
- 内置浏览器负责真实交互、焦点、URL、视觉和窄屏几何；
- 同一生产构建的 Chromium 验收负责完整 Network 观测：113 个请求全部同源只读，无 HTTP error、外部
  origin、写请求或 request failure。

## 5. 清理与资源

本轮为内置浏览器临时启动的唯一 `127.0.0.1:18775` catalog service 已停止；其 PID 与端口监听均为
0。自动 Chromium 所用 `18774` 也在脚本结束后释放，SQLite WAL/SHM sidecar 为 0。最终可用物理内存
约 7472 MiB。未改动 Docker、中间件、代理、防火墙或系统服务。

## 6. 未完成项与下一步

本事实只允许进入 M12-C 的 token 与 Runs 主链表现切片。它仍未证明：

- 故宫空间、色彩双层职责、结构朱与失败朱区分、矿物色张力或最终排版；
- Catalog 行式终稿、Run 详情信息层级、Comparison/Pairing/Batch 的最终空间章法；
- Browser Evidence、全局状态、200% zoom、`forced-colors`、色觉差异和 M12 物理键盘终验；
- M13 分层系统/代码质量终审或 M14 发布复验。

因此 M12 保持进行中；后续切片必须继续以 M11 冻结功能基线为控制组，不能借本次表现层重组改变
证据语义或裁决边界。
