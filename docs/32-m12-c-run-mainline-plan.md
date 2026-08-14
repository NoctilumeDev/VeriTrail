# M12-C 空间令牌与 Runs 主链计划 0.1

> 状态：`IMPLEMENTATION_IN_PROGRESS`
> 日期：2026-08-14
> 前置事实：[M12-B 四向公共视图与十字中轴骨架运行事实](31-m12-b-cross-axis-navigation-facts.md)
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 目标

M12-C 只把 M12-B 已验证的 Runs 主链从高对比线框推进到可读、可扫描的宫阙验迹空间：全局院落轴线、
Catalog 行式目录、Run 身份与 Core 裁决、原因、概览和适用边界。它不实施 Comparison、Pairing、Batch
或 Browser Evidence 的终稿，也不把“故宫”简化为红金换皮。

## 2. 令牌与所有权

- `tokens.css` 建立表面、文字、结构、交互、状态与焦点的语义角色；原有历史名称只作为未迁移视图的
  兼容别名，已迁移的 Runs 范围不得继续直接使用它们；
- 结构朱只用于固定轴线/标识，FAIL/ERROR 使用独立警示朱；PASS、PENDING、ABORTED、INCONCLUSIVE 保留
  独立文字、形状、位置和边界，不只依赖颜色；
- `palace-theme.css` 只拥有页面、轴线、masthead 与 footer；`components.css` 只重写 Catalog、Run 主链及
  其响应式规则，不追加未归属的全局覆盖层；
- 不新增图片、纹理、字体、CDN、图标库、遥测、路由库或状态库。

## 3. 预注册实现范围

1. 用明确的院落表面、台基边界、深色中轴和冷暖制衡重写全局 tokens 与页面骨架；
   M12-B 十字导航只随该 token 层迁移颜色、边界和空间层级，已冻结的 DOM、URL、焦点与键盘行为不变；
2. 将 Catalog 从等权卡片墙改为稳定列序的档案簿行式目录；`ABORTED + PENDING`、长 Run ID、Plan 身份、
   时间和隔离问题在桌面与移动均保持可扫描；
3. 重组/样式化 Runs 的身份、Core status gate、原因、概览与适用边界，使 Verdict/原因先于高密度数据；
4. 保留所有现有 `data-testid`、可访问名称、Loader、URL/history、Catalog 返回焦点和原始证据内容；
5. 对本切片实际触及的样式删除旧规则，不能用 M12-C override 堆叠掩盖 M3 CSS。

## 4. 预注册验收

- 更新组件测试，以稳定列序和文字/状态同时可见约束 Catalog；
- `npm test`、lint、type-check、production build 严格串行；
- 生产 Chromium 使用同一 M11 Gate B 四个真实 Run，验证 PASS、FAIL、ABORTED/PENDING、长内容、
  Catalog return focus、真实 MATCH Comparison 与根级无溢出；
- Codex 内置浏览器验证桌面、390 px、360 px 的 Runs/Catalog、正/负/中止 Run、返回/前进、Console 与
  同源网络；
- 对文本和非文本关键边界进行对比度复核；测试服务、端口和 SQLite sidecar 必须回零。

M12-C 运行事实形成前，M12 保持 `IMPLEMENTING`，不得创建 `m12-v0.13.0`，不得进入 M12-D/E 的派生
分析或 Browser Evidence 终稿。
