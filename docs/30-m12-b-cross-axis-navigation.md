# M12-B 四向公共视图与十字中轴骨架 0.1

> 状态：`IMPLEMENTED_AND_RUNTIME_VALIDATED / M12_NOT_FROZEN`
> 日期：2026-08-14
> 前置基线：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
> 上游设计合同：[M12 宫阙验迹表现系统重构设计计划 0.1](28-m12-palace-workbench-design-plan.md)
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 运行事实：[M12-B 四向公共视图与十字中轴骨架运行事实](31-m12-b-cross-axis-navigation-facts.md)

## 1. 目的与边界

本切片只把既有 Workbench 的公共入口重组成四个有限视图，并把 Catalog 从所有视图的固定前置内容
改为 Runs 视图内部内容。它不改变任何 Bundle、Catalog、Comparison、Pairing、Batch、Verdict、导入
校验或只读 API 语义。

四向映射固定为：北 `Runs / Catalog`、东 `Batch`、南 `Comparison`、西 `Pairing`。中心按钮只表达
当前视图并控制展开，不产生第五种业务状态。Run 详情、Browser Evidence 和原始证据仍属于 Runs。

M12-B 只使用高对比、无装饰的结构样式；颜色令牌、故宫色彩、密度和最终视觉语言留给 M12-C。不得
通过追加全局 CSS override 覆盖旧规则，也不得触及 `src/veritrail`、`web/src/domain/` 或 M11 的冻结
语义。

## 2. 设计与 URL 规则

- 新增独立 `CrossAxisNavigation` 表现组件，使用原生 button 与文字优先名称；不引入路由库或图标依赖。
- 收拢时只有中心按钮可聚焦；展开后 DOM 顺序为中心、北、东、南、西，且方向键遵循几何位置。
- `Enter`/`Space` 切换中心展开；`Esc` 收拢并恢复中心焦点；选择方向后收拢并将焦点移至目标视图标题。
- 未加载本地文件的分析视图以 `?view=comparison|pairing|batch` 表达；已有历史的
  `?fixture=comparison|pairing|batch` 仍保留，并仍在刷新后要求重新选择本地文件。
- Runs 继续沿用 `?run=`、`?fixture=positive|negative|invalid|local`；从十字导航回 Runs 时进入只读 Catalog。
- 每类导入控件移入对应公共视图，但保留已有 `data-testid` 和可访问名称。

## 3. 预注册验收

代码完成后按严格串行顺序证明：

1. 组件测试证明收拢/展开、Tab 顺序、方向键焦点、Esc 回归与四个选择事件；
2. App 测试证明 Catalog 只在 Runs 视图出现，四个导入入口在相应视图出现，既有 fixture/import、损坏
   隔离、URL、返回 Catalog 焦点和本地文件刷新重选语义未漂移；
3. 前端 `test`、lint、type-check 与 production build 全部通过；
4. 生产 Chromium 脚本证明真实 M11 Gate B Catalog/Run/Comparison、历史和同源只读网络仍成立，并增加
   四向导航与无内容分析入口检查；
5. Codex 内置浏览器在桌面和移动视口验证十字导航、真实 Run、Comparison、返回/前进、根节点无横向
   溢出，以及 Console/Network 无未解释错误；
6. 验收进程退出后，核验受控端口、受控服务进程和 SQLite sidecar 均为零。

上述事实形成前，M12 仍是进行中，不能标记 `FROZEN`，也不能开始 M12-C 的色彩与最终视觉实现。
