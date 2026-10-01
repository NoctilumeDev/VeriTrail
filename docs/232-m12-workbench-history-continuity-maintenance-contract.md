# M12 Workbench 历史连续性维护合同

> 身份：`M12_MAINTENANCE_CONTRACT_CANDIDATE / IMPLEMENTED_ON_FIX_BRANCH / NOT_EFFECTIVE`。
>
> 日期：2026-10-01。
>
> 起始坐标：`main@d794731d2402efe98ff572a38cfcf898c22352d7`。
>
> 影响层级：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`。本维护只显式重开 Workbench 的浏览器历史
> 连续性；不可移动 `m12-v0.13.0`，也不重开 Evidence、Bundle、Verdict、Catalog/API 或 Core 语义。

## 1. 真实反例

移动端主要依赖时间顺序保存上下文。维护前，Workbench 从目录进入 Run 详情、再进入详情子面板后，关闭
子面板或返回目录会继续 `pushState` 一个父页面：

```text
父页面 -> 子页面 -> 新父页面
```

因此 Browser Back 会重新打开刚刚关闭的子页面；重复“进入 / 返回”还会继续增长历史。直接打开子页面时，
简单执行 Back 又可能离开 Workbench，而不是进入一个可解释的同源兜底页。

这是已冻结 M12 Workbench 的导航连续性反例，不是 Evidence 内容、Catalog 事实或裁决缺陷。历史 M12 实现、
标签、验收记录和冻结结论保持只读；本合同只授权一个独立维护候选重新取得资格。

## 2. 最小维护语义

1. Workbench 内部 `push` 子页面时，在该子页面的浏览器 history state 中记录精确父 URL。
2. 返回目标与记录的精确父 URL 相同时，使用原生 Browser Back；不得再追加一个父页面 entry。
3. 直接深链、过期记录或目标不匹配时，使用 `replaceState` 进入声明的安全父页面；不得猜测一个不存在的来源。
4. 嵌套子面板只返回一层。Browser Forward 可以重新进入刚才离开的子页面，但不得生成新历史记录。
5. 从目录真实进入详情再返回时，保留浏览器拥有的滚动位置；只有无历史兜底才回到目录顶部。
6. history state 只是 UI 导航投影，不成为 Run、Evidence、Bundle、Comparison 或 Verdict 的事实源。

## 3. 禁止扩张

本维护不得：

- 修改 Python Core、公共 Schema、Evidence、Bundle、Verdict 或 Comparison 语义；
- 修改 Catalog/API 的读取、排序、身份或文件边界；
- 把 URL、history state、焦点或滚动位置写入 Evidence；
- 发明通用导航框架、跨标签页状态协议或持久化会话；
- 为移动端返回强制降级桌面端已有的多窗口、多标签页或直接链接能力；
- 改写历史 M12 文档、标签或验收产物来让本候选看起来已冻结。

## 4. 必须保留的反证

- 父页面进入子页面后关闭：返回原父 entry，Browser Back 不得再次打开子页面。
- 返回父页面后 Browser Forward：只恢复既有子 entry，不得增加新的 entry。
- 目录进入 Run 详情、详情进入子面板：两次返回分别只退一层，并恢复对应上下文。
- 直接打开 Run 详情或子面板：返回进入安全父页面，不离开 Workbench。
- 非 Workbench 查询参数与 hash 不得被维护逻辑误删。
- 桌面与 `390 x 844` 移动视口均无横向溢出、控制台错误或焦点不可达。

## 5. 资格停止线

当前文件只建立维护候选身份，不声明维护已经生效。至少需要：

1. Workbench 单元测试、lint、type-check 与 production build 全部通过；
2. 桌面与 `390 x 844` 真实 Chromium 完成目录、详情、子面板、Back/Forward 与直达兜底链；
3. `git diff --check` 通过，且 diff 只包含本合同授权的 Workbench 导航边界；
4. 独立 PR 在原始 required checks 通过后受保护合入；
5. 新 exact-main 重新运行同一门禁并完成 fresh Workbench 读回；
6. 独立 reconciliation 确认 M12 历史标签未移动、Core/Evidence/Catalog 语义未漂移。

这些门全部成立以前，只能写 `M12 Workbench history-continuity maintenance candidate`，不能写成新的
M12 冻结事实。
