# M12-R1 紧凑中枢与过门运行事实

> 状态：`VALIDATED / R1_CLOSED`
> 日期：2026-08-14
> 代码候选：本提交（R1 实现、验收脚本与事实同次封存）
> 上游合同：[M12-B/C 空间收束与 Runs 目录整改计划 0.1](36-m12-bc-spatial-recomposition-plan.md)
> 控制组：M11 Gate B v2 Catalog，`tmp/m11-gateb-contract04-20260814-161647`
> 影响层级：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`

## 1. 结论

R1 已完成并通过。公共页头从 Hero 式堆叠收束为位置身份与紧凑十字中枢；页头和正文之间新增窄台基过门，
原贯穿正文的结构朱轴线被移除。四向公共视图、URL/history、方向键、Esc、焦点归还、Bundle/Catalog 只读边界和
Comparison 的既有 DOM 顺序没有改变。

这只证明公共外壳的表现纠偏成立。Runs 的来源工具区、Catalog 行式档案簿和 Runs 上下文状态呈现仍属于 R2；D2 Pairing、
D3 Batch、Browser Evidence 终稿和 M12 冻结均未开始。

## 2. 实现边界

| 所有者 | 实际改动 | 未改动的边界 |
| --- | --- | --- |
| `web/src/App.vue` | 将品牌与十字导航组合为页头主组；新增纯表现的 `court-threshold` | 导航事件、URL/history、公共 view 类型、Loader、报告数据 |
| `web/src/components/CrossAxisNavigation.vue` | 只压缩固定 stage 几何、入口尺寸、边界与色面 | 展开/收拢、四向映射、Tab 顺序、方向键、Esc、焦点逻辑 |
| `web/src/styles/palace-theme.css` | 页头、品牌、状态门和过门的局部表现；移除正文贯穿红轴 | token、共享 `StatusBadge.vue`、Catalog/API、Domain、裁决 |
| `scripts/m12_r1_shell_acceptance.py` | 新增生产几何与移动入口门禁 | 不修改产品运行期逻辑 |

`StatusBadge.vue` 未改。R1 没有修改 `components.css` 的 Runs/Catalog 规则，也没有触及任何 L2/L3 契约。

## 3. 自动化与生产构建

在 Node 24.14.0、项目依赖已安装、单任务串行条件下：

| 门禁 | 结果 |
| --- | --- |
| CrossAxis + App 目标测试 | `10/10 PASS` |
| 前端完整测试 | `64/64 PASS` |
| `npm run lint` | `PASS`，零 warning |
| `npm run type-check` | `PASS` |
| `npm run build` | `PASS`，生产 `dist` 已生成 |
| M11 Gate B Production Workbench 回归 | `11 checks / COMPLETED / PASS`，113 个同源只读请求、0 外部、0 写、0 HTTP error、端口释放、SQLite sidecar `0` |
| M12-D1 Comparison 回归 | `7 checks / COMPLETED / PASS`，12 个同源只读请求、0 外部、0 写、0 HTTP error、端口释放 |

生产构建首次因 R1 CSS 块多出的闭合大括号被压缩器拒绝；该语法错误在任何浏览器验收前被修复，随后完整生产构建通过。

## 4. R1 专用生产验收

`scripts/m12_r1_shell_acceptance.py` 使用 M11 Gate B 真实 Catalog、生产 `web/dist` 与临时固定回环只读服务。
它不读取外部项目、不启动 Docker 或中间件，也不覆盖已有证据目录。

普通解释器和 `python -O` 各进行一次独立运行，均为：

```text
desktop-first-screen-stability-target-size-and-keyboard
mobile-390-cross-axis-targets-and-no-overflow
mobile-360-cross-axis-targets-and-no-overflow
=> COMPLETED / PASS
```

普通解释器的摘要事实：

| 断言 | 实测 |
| --- | --- |
| 桌面视口 | `1440 x 960` |
| 页头高度 | `194.188px`，低于首屏一半 `480px` |
| 中心入口 | `136 x 44px` |
| Runs 标题 | 顶部 `280.188px` |
| 第一条真实 Catalog Run | 顶部 `580.094px`，位于初始视口 |
| 展开前后第一 Run 位移 | `0px`，不超过 `24px` 门槛 |
| 桌面四向入口 | `125.531–156.922px x 44px` |
| 390px 移动四向入口 | `113.125–135.750px x 45.328–45.344px` |
| 360px 移动四向入口 | `103.750–124.500px x 45.328–45.344px` |
| 根横向溢出 | 桌面、390px、360px 均为 `0px` |
| Console/page/request failure | 均为 `0` |
| Network | 12 个 `GET`，仅同源，全部 `200`；0 写、0 外部、0 HTTP error |
| 清理 | `18781` 与 `18782` 均释放，服务线程均停止 |

验收输出位于 Git 忽略的 `artifacts/m12-r1-shell-acceptance-final-20260814` 和
`artifacts/m12-r1-shell-acceptance-final-optimized-20260814`；两套摘要的截图哈希、几何值与通过结论一致。

## 5. Codex 内置浏览器补证

对新生产构建的独立只读 `127.0.0.1:18783` 服务完成真实桌面操作后：

1. 初始页面同时显示唯一 H1、紧凑中枢、`Runs / Catalog` H2 和真实四 Run Catalog；
2. 展开十字后四向目标可见，`ArrowRight` 从北向 Runs 移至东向 Batch，`Esc` 收拢并将焦点归还中心；
3. 经 Comparison 入口跳转后，焦点落在 `view-comparison-title`，`Back/Forward` 在 Runs 与 Comparison 之间保持 URL 和视图一致；
4. 展开状态下根横向溢出为 `0px`，Console 为 `0` 条异常；
5. 同一候选的 Chromium 生产验收已经覆盖同源 Network、390px 与 360px；内置浏览器临时页和 `18783` 服务在补证后均已关闭/释放。

内置浏览器补证不替代上述生产 Chromium 的 Network 记录；两者共同构成用户可见交互与可重复自动化证据。

## 6. R1 后续边界

下一步只能是 R2：Runs 标题、来源工具区、Catalog 目录行与 Runs 父级的局部状态样式。R2 开始前，R1 的实现、
本事实与入口状态必须在同一提交内可寻址。任何将共享 `StatusBadge.vue`、证据 Schema、Catalog/API 或 D2/D3
混入 R2 的改动都构成范围漂移。
