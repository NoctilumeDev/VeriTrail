# M12-A 控制组与当前状态审计

> 状态：`CONTROL_BASELINE_AUDITED / PRODUCTION_IMPLEMENTATION_NOT_STARTED`
> 日期：2026-08-14
> 控制组：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
> 审计入口：`02ff99ea91f5dbd4cd18f87e195ef06961f4ea9d`
> 影响层级：`L0_PRESENTATION + BOUNDED_L1_COMPONENT` 的只读审计
> 禁止解释：本文不证明 M12 已实现，不创建版本或里程碑标签

## 1. 结论

M11 Workbench 可以作为 M12 的稳定控制组。当前 `main` 与 `m11-v0.12.0` 的 `web/` Git tree 都是
`9ae3b416d4cdcb00b71a37e9ff3620c3f413e400`；两者在 Vue、TypeScript、CSS、测试和生产构建输入上没有
差异。M12-A 没有修改任何生产前端、Loader、Schema、Verdict、Evidence、Catalog 或只读 API。

控制组功能事实通过，但表现系统确有结构性债务：七个来源/导入动作混在同一横向入口，Catalog 卡片墙
固定占据所有分析视图之前，移动端第一屏几乎全部用于入口与状态块；Comparison、Pairing、Batch 虽已
加载，仍需越过完整 Catalog 才能看到。这不是功能失败，却正是 M12-B 必须先重构信息架构、不能直接
叠加主题 CSS 的运行事实。

因此：允许下一切片进入 **M12-B 无装饰信息架构与十字导航骨架**；仍不允许进入故宫色彩、Catalog
视觉终稿、M12 版本号或 `m12-v0.13.0` 标签。

## 2. 控制变量与环境

| 项目 | 本轮事实 |
| --- | --- |
| 操作系统与资源策略 | Windows 11，16 GB 主机，全部步骤严格串行 |
| Python | 项目 `.venv`：Python 3.10.6 |
| Node / npm | Node 24.14.0 / npm 11.9.0，满足 Workbench engines |
| 初始可用内存 | 约 7866 MiB；自动 Chromium 开始时 7851.484 MiB |
| 自动 Chromium 结束内存 | 7778.660 MiB |
| 本轮浏览器审计后可用内存 | 约 7639 MiB |
| C 盘余量 | 约 141.10–141.15 GiB |
| 测试数据 | `tmp/m11-gateb-contract04-20260814-161647` 及 M6–M8 脱敏历史分析包 |
| Workbench 服务 | 单个 owned、只读、`127.0.0.1:18778` 服务 |
| 清理结果 | owned 进程 0；18770–18779 监听 0；SQLite WAL/SHM sidecar 0 |

未启动 Docker、中间件或第二个浏览器实例，没有修改代理、防火墙、端口或系统服务。

## 3. 自动化控制组

严格串行结果：

| 门禁 | 事实 |
| --- | --- |
| Workbench unit/component | 8 files，60/60 tests passed |
| ESLint | `--max-warnings=0` 通过 |
| TypeScript | `vue-tsc` 与 Node `tsc` 通过 |
| Production build | 34 modules；CSS 40.45 kB / gzip 7.37 kB；JS 168.91 kB / gzip 53.10 kB |
| M11 Gate B production Workbench | `COMPLETED / PASS`，9 项检查 |
| Chromium | 151.0.7922.34；桌面 1440×960、移动 390×844 |
| Network | 113 请求；HTTP error 0；external origin 0；write request 0 |
| Browser runtime | Console error 0；page error 0；request failure 0 |
| 自动验收清理 | 服务线程停止，端口释放，SQLite sidecar 0 |

生产验收逐项复核四个真实 Run、Catalog history、真实 `MATCH` Comparison，以及移动负向 Run 与
Comparison 的根级无横向溢出。生成物保存在 Git 忽略目录
`artifacts/m12-a-control-workbench/`，不作为仓库源码提交。

## 4. 内置浏览器运行事实

### 4.1 Run 与通用 Bundle 状态

最终 M11 Catalog 的四个 Run 全部由只读 API 重新读取：

| Run | Execution | Verdict | Browser Evidence | 根级横向溢出 |
| --- | --- | --- | --- | --- |
| `m11-gateb-v2-ink-positive-01` | `COMPLETED` | `PASS` | 有 | 0 |
| `m11-gateb-v2-ink-browser-negative-01` | `COMPLETED` | `FAIL` | 有 | 0 |
| `m11-gateb-v2-ink-port-conflict-01` | `ABORTED` | `PENDING` | 无，明确显示“不等于浏览器检查通过” | 0 |
| `m11-gateb-v2-ink-recovery-positive-02` | `COMPLETED` | `PASS` | 有 | 0 |

内置正向、负向和损坏 Bundle 也分别得到 `COMPLETED/PASS`、`COMPLETED/FAIL` 和
`MISSING_ROOT_FILE`。损坏状态不显示断言或证据账册；点击重试恢复到正向 Bundle，旧错误状态消失。

### 4.2 派生分析状态矩阵

| 视图 | 已真实加载的状态 | 损坏拒绝 |
| --- | --- | --- |
| Comparison | `MATCH`、`DRIFT`（7 differences）、`INCONCLUSIVE`（3 differences） | `COMPARISON_SIZE_MISMATCH` |
| Pairing | `SUPPORTED`、`CONTRADICTED`、`INCONCLUSIVE` | `PAIRING_FILE_SET_MISMATCH` |
| Batch | `COMPLETE/SUPPORTED`、`COMPLETE/CONTRADICTED`、`INCONCLUSIVE/INCONCLUSIVE`、`INCOMPLETE/INCONCLUSIVE` | `BATCH_SIZE_MISMATCH` |

全部成功态保留来源 Execution/Verdict 与派生分析状态的分离；全部损坏态隐藏部分可信视图并保留重试
入口。各状态在 1440×960 下根页面横向溢出都为 0。

### 4.3 Console、网络与历史

- 内置浏览器最终 Console `warning/error` 为 0；
- 正向真实 Run 页面观察到 22 个页面资源：1 stylesheet、1 script、1 Catalog fetch、19 个同源
  Bundle 文件/附件 fetch；全部 origin 为 `http://127.0.0.1:18778`，没有远程字体、CDN 或装饰资产；
- HTTP 状态、失败请求、外部 origin 与写请求的精确否定由同一生产构建的自动 Chromium 113 请求
  记录交叉证明；
- Run -> Catalog 返回后，原 Catalog 行重新获得焦点；浏览器 Back 恢复同一 Run，Forward 回到 Catalog；
- URL 分别保持根 Catalog、`?run=<catalog-run-id>` 与 `?fixture=comparison|pairing|batch` 语义。

### 4.4 键盘基线

Browser Evidence 继续使用标准 `tablist/tab/tabpanel`：四个 tab 中只有当前项 `tabindex=0`，其余为
`-1`；从“步骤”按 `ArrowRight` 后，焦点和可见 panel 同时移动到 Console。M11 冻结轮的用户物理
`Tab`、方向键、截图对话框和返回焦点事实继续作为控制证据。

本轮内置浏览器的合成 `Tab` 仍不能产生系统级焦点迁移，这是 M8/M11 已记录的控制工具限制，不能
据此把页面判为失败，也不能据此宣称新的物理键盘通过。M12-F 仍必须由用户重新完成物理键盘终验。

## 5. 视口与首屏几何

正向 Run 的控制组几何如下；所有视口根级横向溢出均为 0：

| 视口 | Header 高度 | 来源入口 | Catalog 起点 | 运行事实 |
| --- | ---: | --- | ---: | --- |
| 1440×960 | 约 385 px | 7 项单行 | 约 433 px | Catalog 约 545 px 高，第一屏只显示其大部 |
| 1280×800 | 约 385 px | 7 项单行 | 约 433 px | Catalog 明显越过首屏 |
| 1024×768 | 约 433 px | 第 7 项换行 | 约 481 px | 导航与状态占据过多垂直空间 |
| 390×844 | 约 805 px | 7 项全部单列 | 约 829 px | 第一屏几乎只剩来源入口和状态块 |

在 390×844 的根 Catalog 页面，Catalog 本身从约 540 px 开始并高约 1723 px。加载派生分析后，
Comparison、Pairing、Batch 都从页面约 2287 px 才开始；三者没有获得真正的顶层视图位置。Batch
矩阵没有污染根宽度，而是在具名、可聚焦区域内形成 304 px client width / 672 px scroll width 的
局部滚动，这一边界应保留。

当前控制组没有 `forced-colors` 专属规则，也没有可重复的 200% zoom 自动门禁。两项不是 M12-A
阻断项，却是 M12-E/F 的硬验收缺口；不能从“根级无溢出”推导它们已经通过。

## 6. DOM、组件与数据所有权

`App.vue` 当前 840 行，拥有来源选择、URL/history、Catalog 选择、四类 Loader 入口、全局 loading/
error 和 Run 详情组合；它包含 15 个普通函数、4 个 computed 和 17 个模板 test ID。当前层级是：

```text
App
  -> Masthead + 七项 source switcher + 可选 status gate
  -> RunCatalog（只要 Catalog loading/data/error 任一存在就始终渲染）
  -> ComparisonView | PairedAnalysisView | BatchAnalysisView | Run detail
       Run detail:
       -> SectionFrame × 5
       -> StatusBadge
       -> BrowserEvidence
```

这解释了为什么分析视图总在 Catalog 之后：Catalog 不是与三类分析互斥的顶层视图，而是一个先行
兄弟节点。M12-B 可以改变组件组合、DOM 分组、信息顺序和焦点路径，但以下所有权必须保持：

- `domain/bundle.ts`、`catalog.ts`、`comparison.ts`、`pairing.ts`、`batch.ts` 继续拥有解析与验真；
- UI 只消费生产者 Verdict/Analysis，不在组件中重新裁决；
- Catalog 继续是可重建派生索引，Bundle 继续拥有事实；
- 本地选择继续只在内存读取，不上传、不写回；
- `StatusBadge`、错误态和边界文本继续同时用文字与形状表达，不只依赖颜色。

## 7. CSS 所有权审计

加载顺序固定为 `reset -> tokens -> palace-theme -> components`。

| 文件 | 行数 | 当前所有权与风险 |
| --- | ---: | --- |
| `reset.css` | 58 | box sizing、最小视口、基础 focus-visible；全局基础所有者 |
| `tokens.css` | 48 | 颜色、字体、间距、半径、内容宽度和动画 token |
| `palace-theme.css` | 182 | body、skip link、masthead、全局中轴、footer、720px 与 reduced-motion |
| `components.css` | 2385 | 120 个 class 名、379 个规则块、3 个响应式断点和 1 个 loading keyframe |

`components.css` 有 521 次 token 引用，但仍有 32 个 hex 和 13 个 rgb/rgba 直接色值、11 处阴影；精确
颜色没有完全由语义 token 所有。四个 `!important` 全部只在 reduced-motion 全局保护内，不存在一层
新的主题 override；`palace-theme.css` 与 `components.css` 也没有重复 class selector。问题不是当前
已经形成覆盖战争，而是 2385 行组件规则只有文件级所有者，没有清晰的组件级边界。

静态组件所有权：App 34 个 class，BrowserEvidence 20，Batch 20，Pairing 13，RunCatalog 13，
Comparison 10，SectionFrame 5，StatusBadge 3。`comparison-court`、`comparison-verdict`、
`comparison-sources`、`comparison-boundary` 又被 Pairing/Batch 复用，说明“比较视图”样式已经兼任
派生分析通用 primitive；M12-D 迁移时必须显式命名所有权，不能按文件名误删。

有 21 个状态 modifier 只由动态 class 字符串生成，简单静态扫描会误报为 unused；不得借 M12 清理
删除 `status--*`、`comparison-verdict--*`、`paired-verdict--*`、`batch-status--*` 等裁决状态。

## 8. Test ID 与消费者合同

M12-B 允许调整 DOM，但不得静默删除以下稳定入口：

| 合同组 | 主要消费者 |
| --- | --- |
| `fixture-*`、`local-bundle-input` | App tests、M3/M4 browser acceptance |
| `local-comparison-input`、`comparison-view` | App tests、M6、M11 production Workbench acceptance |
| `local-pairing-input`、`paired-analysis-view` | App tests、M7 acceptance |
| `local-batch-input`、`batch-analysis-view` | App tests、M8 browser acceptance |
| `run-catalog`、Catalog 行、`catalog-return` | Catalog tests、M4、M11 acceptance |
| `status-gate`、`browser-evidence`、`browser-empty` | App/Catalog tests、M3/M4/M11 acceptance |
| Browser tab ARIA 关系 | BrowserEvidence tests、M3 与人工键盘验收 |

新增十字导航需要新合同，但旧数据入口的 test ID 应保持或通过单一、明确的兼容层迁移；不能让测试
因页面重新排版而改成只检查截图或模糊文本。

## 9. M12-B 施工边界

M12-B 只处理以下主干：

1. 把“正/负/损坏 fixture、四类本地导入”和“四个公共视图”从同一层级拆开；
2. 以 Runs/Catalog（北）、Comparison（南）、Pairing（西）、Batch（东）建立真实十字中轴导航；
3. 让当前公共视图成为主要内容，而不是永远排在完整 Catalog 之后；
4. 保持 URL、Back/Forward、Catalog 返回焦点、文件选择焦点和错误重试事实；
5. 用无装饰、高对比线框装入真实长 Run ID、SHA、FAIL、ABORTED/PENDING、矩阵和原始证据；
6. 每次只迁移导航/空间骨架，不引入新颜色、纹样、动效或 Schema。

后续切片再分别拥有：M12-C token 与 Run 主链，M12-D 三类派生分析，M12-E Browser Evidence 与全局
状态，M12-F 真实终验。若 M12-B diff 触及 domain Loader、公共类型、裁决文本或 API，立即视为范围
漂移并停止，不能用本审计为 L2/L3 变化背书。

## 10. 非结论

- M12-A 的测试全绿不等于 M12 页面已经设计或实现；
- 当前无横向溢出不等于信息架构、首屏检索、200% zoom 或 forced-colors 已通过；
- 历史物理键盘事实只定义控制组，不替代 M12 新结构的物理键盘验收；
- 当前配色可读不等于结构朱/失败朱、矿物色彩张力或“院落之空”已经成立；
- 本文没有提高版本、移动 M11 标签或创建 M12 标签。
