# M12-R2 Runs 主链表现运行事实

> 状态：`VALIDATED / R2_CLOSED`
> 日期：2026-08-14
> 实现提交：`005ab1a`（`feat(m12): recompose runs catalog`）
> 上游合同：[M12-B/C 空间收束与 Runs 目录整改计划 0.1](36-m12-bc-spatial-recomposition-plan.md)
> 控制内容：M11 Gate B v2 Catalog，`tmp/m11-gateb-contract04-20260814-161647`
> 影响层级：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`

## 1. 结论

R2 已完成并通过。Runs 的标题、来源工具区、Catalog 档案行和 Runs 语境内的状态铭牌完成表现收束：示例证据
与本地导入已分组且保持原生入口，真实 Run 继续是可返回焦点的原生按钮行；execution 与 verdict 保持独立文字、
图形和边界语法。真实 PASS、FAIL、ABORTED/PENDING、长 Run ID、隔离 Catalog 问题、本地 Bundle 导入和损坏恢复
均保持原有证据事实。

这只证明 Runs 主链的表现整改成立。共享 `StatusBadge.vue`、Catalog/API、Bundle/Manifest 校验、Comparison、
Pairing、Batch、Browser Evidence 终稿、M12 冻结和任何 L2/L3 契约均未改变。

## 2. 实现边界

| 所有者 | 实际改动 | 明确未改动 |
| --- | --- | --- |
| `web/src/App.vue` | Runs 标题与工具区重新分组；示例入口与本地目录导入形成主次 | 来源选择、导入、URL、Bundle 校验和状态语义 |
| `web/src/styles/components.css` | 工具区、Catalog 标题、行式目录与 `.catalog-run` 父级的局部状态边界 | 全局 token、共享状态组件、其他公共视图 |
| `web/tests/app.test.ts` | 锁定“示例证据”分组与本地原生 label/input 所有权 | 不修改领域或 API 测试 |
| `scripts/m12_r2_runs_acceptance.py` | 新增生产 Chromium 的 R2 专用验收和清理门禁 | 不修改运行期产品逻辑 |

`RunCatalog.vue` 的既有列顺序、原生 Run button、测试 ID 和返回焦点契约均保持原样；`StatusBadge.vue` 完全未修改。
没有加入图片、远程字体/CDN、遥测、主题切换、`!important` 覆盖或第二个项目栈。

## 3. 自动化与构建

在 Node 24.14.0、项目既有依赖、单任务串行条件下，提交 `005ab1a` 的前端门禁为：

| 门禁 | 结果 |
| --- | --- |
| 完整前端测试 | `65/65 PASS` |
| `npm run lint` | `PASS`，零 warning |
| `npm run type-check` | `PASS` |
| `npm run build` | `PASS`，生产 `web/dist` 已生成 |
| R2 专用生产 Chromium | `6 checks / COMPLETED / PASS` |
| R2 专用生产 Chromium（`python -O`） | `6 checks / COMPLETED / PASS` |

优化模式复跑使用脚本自有 `require()` 门禁，不依赖会被 `python -O` 删除的内建 `assert`。

## 4. 生产 Chromium 事实

`scripts/m12_r2_runs_acceptance.py` 使用同一 M11 Gate B v2 Catalog、生产 `web/dist`、临时固定回环只读服务，
不启动 Docker、中间件或第二个项目栈。标准解释器运行在 `18784`，优化模式运行在 `18785`；两次退出后端口均释放，
服务线程均停止。

每次都严格验证以下 6 项：

1. 在 `1440 x 960` 中，四条真实 Catalog 行保持 `Run / 时间 -> execution -> verdict -> Plan / 目录事实` 列序，
   含 `COMPLETED/PASS`、`COMPLETED/FAIL` 与 `ABORTED/PENDING`；execution 为 1px 框式语法，verdict 为 3px 左铭牌语法；
2. 示例正/负证据切换不丢失状态事实；
3. 详情页返回后，焦点回到触发详情的同一 Run button；
4. 本地正向 Bundle 仍能导入，损坏目录仍被隔离，显式恢复后回到正向事实；
5. `390 x 844` 与 `360 x 800` 中工具区、四条 Catalog 行和 `ABORTED/PENDING` 均可见，根横向溢出均为 `0px`；
6. Console、page error 与 request failure 均为 `0`；标准运行记录 58 个请求，全部为同源只读 `GET 200`，无外部请求、
   写请求或 HTTP error。

标准运行的截图哈希位于 Git 忽略目录 `artifacts/m12-r2-runs-acceptance`，优化模式的独立输出位于
`artifacts/m12-r2-runs-acceptance-optimized`。输出目录拒绝覆盖，避免把后续运行混入本次事实。

## 5. Codex 内置浏览器补证

在运行中的只读 `127.0.0.1:18778` Workbench 中，真实当前响应式布局完成以下操作：

1. 读取四条 M11 Gate B Run，确认长 ID、`COMPLETED/PASS`、`COMPLETED/FAIL`、`ABORTED/PENDING` 与 Catalog
   Diagnostics 同时保留；根横向溢出为 `0px`；
2. 进入首条真实 Run 详情后使用 `catalog-return` 返回，焦点准确归还给原始 Catalog Run button；
3. Console 无 warning/error，页面没有未解释网络错误；
4. 本轮未将内置浏览器的临时固定视口覆盖误写成 390/360px 事实。精确尺寸由上节可重复生产 Chromium 取得；
   内置浏览器补证只证明用户可见的真实交互、焦点与当前响应式页面状态。

内置浏览器补证不替代生产 Chromium 的 Network 与固定视口证据，两者共同构成 R2 的交互、浏览器与清理结论。

## 6. 交接边界

R2 已关闭。下一步只能先写 M12-D2 Pairing 的独立计划，再实施 Pairing 视图；不能把其实现混入 R2，也不能借
“表现收尾”触及 `StatusBadge.vue`、Schema、Catalog/API、裁决或安全边界。M12 仍为 `IMPLEMENTING`，不创建 M12
标签或版本。
