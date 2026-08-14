# M12-B/C 空间收束与 Runs 目录整改计划 0.1

> 状态：`R1_VALIDATED / R2_VALIDATED`
> 日期：2026-08-14
> 当前实现基线：`005ab1a`（R2 Runs 主链已形成事实）
> 上游合同：[M12 宫阙验迹表现系统重构设计计划 0.1](28-m12-palace-workbench-design-plan.md)
> 纠偏来源：M12 实页审美复核
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 问题与单一变量

当前 M12 的信息架构、十字映射、只读入口、Catalog 行式语义和 D1 Comparison 已有独立事实，但公共外壳仍有
“深色 Hero + 大白导航框 + 后台工具条”的拼装感。问题不在于继续增加故宫色，而在于空间重心没有让真实证据
成为首屏主角。

本计划只引入一个主要变量：

```text
shell_and_runs_presentation = compact_court_thresholded_m12
```

目标是让导航成为紧凑的空间中枢，让 Header 只提供位置身份，让 Runs/Catalog 成为首个真正的“正殿”。
它不是新主题、不是 D2 Pairing、不是 D3 Batch，也不重开 M11 的功能事实。

## 2. 保持不变与所有权

### 2.1 必须保持不变

- 四向映射、URL、Back/Forward、展开/收拢、Tab 顺序、方向键、Esc 和焦点归还；
- Bundle/Manifest 校验、Catalog/API 只读边界、本地文件导入、损坏隔离和对象 URL 回收；
- Run、Comparison、Pairing、Batch 的状态、Verdict、来源 authority、test ID 和数据语义；
- 既有 D1 Comparison 的 `BASELINE -> REPEAT -> ComparisonStatus` DOM 顺序和表现事实；
- 单一应用、无图片、无纹理、无远程字体/CDN/遥测、无主题切换器。

### 2.2 允许所有者

| 子切片 | 允许文件/所有者 | 不得越过 |
| --- | --- | --- |
| R1 公共外壳 | `App.vue` 的 masthead 表现分组、`CrossAxisNavigation.vue`、`palace-theme.css`、其目标测试 | 导航行为、URL/history、公共 view 类型、Loader |
| R2 Runs 主链 | `App.vue` 的 Runs 标题/来源工具区、`RunCatalog.vue`、`components.css` 的 `.source-switcher`、`.catalog-*` 与 Runs 父级 `.status-badge` 上下文样式、其目标测试 | `StatusBadge.vue` 公共组件、domain 类型、Catalog/API、Run 语义 |

`StatusBadge.vue` 同时被 App、Comparison、Pairing 和 Batch 消费。本计划只能通过 `.catalog-run`、Runs
`status-gate` 等父级上下文把它呈现为事实铭牌，不能修改共享组件、图形含义或全局状态 token。若后续确实
需要全局状态系统重构，必须列出全部消费者并按独立 L2 审查，不得借本计划偷渡。

## 3. 设计约束

### 3.1 R1: 紧凑中枢与过门

- Header 从品牌 Hero 收束为位置身份：保留“迹”、眉题、中文名称与一句辅助说明，但缩小其面积和权重；
  不创造第二个营销区；
- 十字默认收拢为内容宽度内的中枢。展开时北南轴强于东西轴，四向入口仍在固定几何位置、具文字名称和
  不小于 `44 x 44` CSS px 的触控目标；
- 收拢和展开共享稳定 stage 尺寸，不让工作区因状态变化产生明显纵向跳动；白色大框、厚黑边和悬浮卡片阴影
  不得作为导航的主要形态；
- Header 到正文只保留窄台基、细结构线或明确色面转折，形成“宫墙/中枢 -> 过门 -> 院落/工作区”，不使用
  渐变、雾化、玻璃或红线贯穿整页；
- 应用名称继续是唯一文档 H1；`Runs / Catalog`、`Rerun Comparison` 等公共视图标题保持 H2 语义，但在其
  工作区内拥有首要视觉层级。

### 3.2 R2: Runs 的工具、档案簿与状态

- Runs 视图标题、来源工具区和 Catalog 的左轴必须统一；工具区按“示例证据”与“选择本地证据包”分主次，
  不再把四个入口做成等权后台标签；
- Catalog 保持真实原生 `button` 行，整行仍可进入详情；视觉上改为档案记录行，不重新变成卡片墙或在行内
  添加嵌套交互控件；
- 表头与真实列严格对齐：`Run / 时间` 首要，execution / verdict 并列但不混并，Plan/目录事实为密度较高的
  技术区；长 Run ID 自然换行；
- 在 Runs 上下文，`COMPLETED`、`PASS`、`ABORTED + PENDING` 以文字、图形、边界和位置构成事实铭牌，
  不伪装成第二组按钮。execution 与 verdict 使用不同形状/边界语法；FAIL/ERROR 继续只使用警示朱，
  结构朱不承担状态；
- 边界以细线、局部上沿、台基层次和空白定义。禁止完整粗黑框、页面段落卡片化、卡片套卡片、阴影分层和
  追加全局 `!important` 覆盖。

## 4. 可验证的视觉退出条件

视觉判断不能只写“更紧凑”。在真实 M11 Gate B Catalog、`1440 x 960`、导航收拢的 Runs 首屏中，必须同时满足：

1. 页面身份、中枢、Runs 标题和至少一条真实 Catalog Run 均出现在初始视口；
2. Header/导航不再单独占用超过首屏的一半，展开/收拢前后 Catalog 首行的纵向位置变化不超过 `24 px`；
3. 根级横向溢出为 `0 px`，不存在相互遮挡的标题、状态、十字臂或工具控件；
4. `COMPLETED / PASS`、`COMPLETED / FAIL`、`ABORTED / PENDING` 都保留独立文字区，不依赖颜色且不被压成
   一个状态；
5. `390 x 844` 与 `360 x 800` 中，十字的中心/四向入口仍保持 `44 x 44` CSS px 最小触控尺寸，工具区自然
   换行或纵向排列，Catalog 行不根溢出；
6. 视图标题不新增 H1，Catalog 的 run button、十字的 native button 和本地导入 label/input 的可访问名称不变。

第 2 条是空间稳定性门槛，不是用来替代真实焦点、历史或浏览器验收。若以视觉压缩为名使其中任何交互或
证据事实不可见，本计划直接失败。

## 5. 实施顺序与控制变量

严格串行，每个切片有自己的实现、验收和事实文档。不得把 R1、R2 与 D2 Pairing 混在一个 diff 中。

### R1: Header、十字中枢与过门

1. 审计 masthead、CrossAxisNavigation 的当前几何、焦点与公共消费者；
2. 只调整 R1 所有者的 DOM 表现分组、scoped CSS 和外壳 CSS；不改导航事件、键盘函数或 URL 代码；
3. 桌面先以真实 Catalog 验证首屏和收拢/展开稳定性，再验证 `390` / `360`；
4. 通过目标组件、全量前端、生产 Chromium、内置浏览器和清理门禁后，写 R1 事实；
5. R1 未形成事实前，不进入 R2。

### R2: Runs 标题、工具、Catalog 与状态上下文

1. 只调整 Runs 的标题/工具分组和 Catalog 行式样式；共享 `StatusBadge.vue` 不改；
2. 使用同一 M11 Gate B 的 PASS、FAIL、ABORTED/PENDING、隔离问题、长 ID 与本地 Bundle 入口作为内容压力；
3. 首先验证表头/行对齐、状态分离、文本换行和无根溢出，再验证 Catalog return focus、刷新/返回和本地导入；
4. 通过目标组件、全量前端、生产 Chromium、内置浏览器和清理门禁后，写 R2 事实；
5. R2 未形成事实前，D2 Pairing 继续 `NOT_IMPLEMENTED`。

## 6. 预注册验收矩阵

每个子切片的门禁严格串行，且不启动 Docker、中间件或第二个项目栈。

| 层级 | R1 | R2 |
| --- | --- | --- |
| 代码 | CrossAxis DOM、H1/H2、stage 及其消费者不越界 | Runs/App/Catalog 局部 DOM、父级状态样式不越界 |
| 自动化 | 十字的展开/收拢、Tab/方向键/Esc、URL/history 既有测试 | Catalog 列序、四个状态组合、长 ID、工具入口与既有导入测试 |
| 静态 | `npm test`、lint 零 warning、type-check、production build | 同左 |
| Chromium | 1440/1280/1024、390/360；真实 Catalog 首屏、焦点、Back/Forward、Console/Network、根溢出 | 同一 M11 Gate B Run/隔离问题、详情返回、导入/损坏恢复、同源只读 Network、根溢出 |
| 内置浏览器 | 收拢/展开、键盘焦点、首屏、390/360、Console | 真实 PASS/FAIL/ABORTED+PENDING、长行、导入、返回焦点、390/360、Console |
| 边界/清理 | `prefers-reduced-motion` 不制造必要动效；临时服务/端口释放 | 状态文字与形状仍可辨；临时服务、端口、SQLite sidecar 和对象 URL 不残留 |

R1/R2 不提前宣称 200% zoom、完整 forced-colors、色觉差异、Browser Evidence、Pairing、Batch 或 M12-F
终验。这些保持原属 E/F 的最终矩阵；若 R1/R2 发现阻断性问题，只能记录并修复当前切片，不得扩大到后续能力。

## 7. 完成与交接

本计划只有在以下顺序全部成立时才算闭环：

```text
Plan confirmation
  -> R1 facts (closed: [document 37](37-m12-r1-compact-shell-facts.md))
  -> R2 facts (closed: [document 38](38-m12-r2-runs-presentation-facts.md))
  -> D2 Pairing plan/implementation (next)
```

R1/R2 的事实只证明公共空间与 Runs 主链的表现纠偏，没有推翻 M11、M12-B/C 或 D1 的功能结论，也不代表
M12 已冻结。每项完成必须同步 README、`docs/milestones.md`、项目 `AGENTS.md` 与独立运行事实；代码、
生产构建、浏览器和清理证据必须指向同一候选提交。

## 8. 计划确认门禁

- [x] M11 与 M12-D1 均已有可寻址实现/事实基线；
- [x] 已确认问题是空间、层级和密度，不是简单替换颜色；
- [x] 已确认 Header/十字、Runs/Catalog 和共享 StatusBadge 的所有者/消费者不同；
- [x] 已明确状态视觉仅在 Runs 父级上下文收束，不全局改写共享组件；
- [x] 已明确 `Runs / Catalog` 维持 H2 语义，不引入第二个 H1；
- [x] 用户审阅并确认本计划 0.1；
- [x] 计划先于任何 R1/R2 生产代码提交；
- [x] R1 公共外壳已形成独立实现、生产 Chromium、内置浏览器与清理事实；
- [x] R2 Runs 主链已形成独立实现、生产 Chromium、内置浏览器与清理事实；

本文件是已确认的实施合同，不替代运行事实。R1、R2 的独立事实见文档 37、38；下一步只有 D2，仍必须先形成
自己的计划和运行事实。
