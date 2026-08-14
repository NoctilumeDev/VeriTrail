# M12-C 空间令牌与 Runs 主链运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
> 日期：2026-08-14
> 前置冻结基线：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
> 施工合同：[M12-C 空间令牌与 Runs 主链计划 0.1](32-m12-c-run-mainline-plan.md)
> 影响事实：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止误读：本文不完成 M12-C 的全部预注册浏览器验收，不冻结 M12，不创建版本或标签，也不允许进入 M12-D。

## 1. 本切片已实现的事实

- `tokens.css` 现在先定义表面、文字、结构、交互、状态与焦点的语义 token；历史颜色名称只保留给
  尚未迁移的视图作为兼容别名。结构朱只用于屋脊和中轴等固定空间，不再与 `FAIL/ERROR` 共用 token；
- `palace-theme.css` 将页面骨架改为深殿、院落台基和可见中轴。它没有使用图片、纹理、远程字体、CDN、
  遥测或模糊遮罩；
- M12-B 的十字导航仅迁移了 token、边界与空间层级。其四向映射、DOM、URL、焦点、方向键和 `Esc`
  行为没有改变；在 `forced-colors` 下显式回退到系统颜色；
- `RunCatalog.vue` 从两列卡片墙改为档案簿行。桌面固定顺序为 `Run / 时间 -> 运行状态 -> 验收结论 ->
  Plan / 目录事实`；移动端隐藏视觉列头但保留每行中两个独立、具文字和符号的状态区域；
- Runs 主链的身份牌、状态门、原因、概览、适用边界与庭院框架已迁移到新 token。长 Run ID、Plan SHA
  和原因仍按原有的换行/局部滚动边界显示；Bundle、API、Loader、Verdict 和证据所有权未改变。

## 2. 自动化与生产 Chromium 事实

全部门禁在 Windows 11、16 GB 主机上严格串行运行；未启动 Docker、中间件或第二个项目栈。

| 门禁 | 最终事实 |
| --- | --- |
| Workbench unit/component | 9 files，`64/64` tests passed；新增稳定列序与双状态区域断言 |
| ESLint | `--max-warnings=0` 通过 |
| TypeScript | `vue-tsc` 与 Node `tsc` 通过 |
| Production build | 38 modules；CSS 46.84 kB / gzip 8.55 kB；JS 177.83 kB / gzip 54.96 kB |
| M11 Gate B production Workbench | 常规与 `python -O` 均为 `COMPLETED / PASS`，各 11 项检查 |
| Chromium | 151.0.7922.34；桌面 1440 x 960、移动 390 x 844 |
| Network | 113 requests；HTTP error、external origin、write request 均为 0 |
| Browser runtime | Console error、page error、request failure 均为 0 |
| 自动清理 | 服务线程停止、端口释放、SQLite sidecar 0 |

生产 Chromium 对同一份 M11 Gate B 四个真实 Run 和隔离损坏候选确认：

1. Catalog 读回四个真实 Run 与一个独立问题；所有 Run 行均分别呈现 execution 与 verdict；
2. `COMPLETED / PASS`、`COMPLETED / FAIL`、`ABORTED / PENDING`、`COMPLETED / PASS` 均可进入详情、
   回到原 Catalog 焦点，64 字符 Plan SHA-256 的 title authority 未漂移；
3. 桌面和 390 px 移动 Catalog、详情、十字导航和真实 `MATCH / 0 differences` Comparison 的根级横向
   溢出均为 0；移动 Catalog 的列头已隐藏，但 `ABORTED` 与 `PENDING` 仍在同一行的独立区域可见；
4. Catalog/Comparison 的历史、只读 HTTP 负向合同、M12-B 的十字焦点和公共视图回归全部成立。

自动输出位于 Git 忽略目录：

- `artifacts/m12-c-workbench-acceptance-20260814-final/acceptance.json`
- `artifacts/m12-c-workbench-acceptance-20260814-final-optimized/acceptance.json`

它们是生产构建对真实 M11 数据的运行记录，不提交到仓库，也不是替代内置浏览器验收的截图。

## 3. 视觉与对比度复核

生产截图使用真实 Catalog 内容而非空 Mock。可见结构为：深色正殿承接十字中枢，结构朱只压住屋脊与
页面中轴，Runs 作为下方档案簿展开；`ABORTED` 的方形图形/虚线边界与 `PENDING` 的省略图形/实线边界
不依赖单一颜色。

依据最终 token 色值计算的前景/背景对比度如下：

| 语义 | 对比度 |
| --- | ---: |
| 正文 / 院落 | `16.59:1` |
| 深殿正文 | `11.18:1` |
| PASS | `5.88:1` |
| FAIL | `5.54:1` |
| RUNNING | `7.74:1` |
| INCONCLUSIVE | `5.88:1` |
| PENDING | `5.20:1` |
| ABORTED | `6.04:1` |

这些数值满足本切片涉及的普通文本最低 `4.5:1` 目标；状态同时保留文字、图形、位置和边界，不以色彩
作为唯一渠道。`forced-colors` 的完整用户链、200% zoom 与色觉差异矩阵仍属于 M12-E/F，不在本切片冒充完成。

## 4. Codex 内置浏览器补证

在同一份 `127.0.0.1:18778` 只读生产构建中，Codex 内置浏览器完成了以下真实用户可见交互；读取的
仍是 M11 Gate B 的四个 Run、一个隔离损坏候选和同计划的本地 Comparison 目录，不是 Mock 或截图替代品。

### 4.1 桌面主链、焦点与历史

- Catalog 显示四个真实 Run 和一个独立目录问题；每行都分开显示 execution 与 verdict：两个
  `COMPLETED / PASS`、一个 `COMPLETED / FAIL`、一个 `ABORTED / PENDING`；
- 十字展开后，北向 `Runs / Catalog` 上按 `ArrowRight` 真实进入东向 `Batch Analysis`；按 `Esc` 收拢并
  把焦点返回中心；选择南向后 URL 为 `?view=comparison`，焦点进入 Comparison 标题且 Catalog 不在 DOM；
- 浏览器 Back 返回 Catalog，Forward 返回 Comparison；再从北向回 Catalog 后，四个 Run 都逐一进入详情，
  并由 `返回 Run 目录` 恢复到各自的原行焦点；
- 正向和恢复 Run 均为 `COMPLETED / PASS` 且存在 Browser Evidence；负向 Run 为 `COMPLETED / FAIL` 且仍
  存在 Browser Evidence；端口冲突 Run 为 `ABORTED / PENDING` 并明确显示 Browser Evidence 不适用；
- 从恢复正向 Run 的 `?run=...` 详情 Back/Forward 后，分别真实回到 Catalog 与同一 Run 详情；所有上述
  页面根级横向溢出均为 `0 px`；
- 向本机工作台导入脱敏的真实 M11 Comparison 目录后，页面显示 `MATCH / 0 differences`，来源为
  `m11-gateb-v2-ink-positive-01` 与 `m11-gateb-v2-ink-recovery-positive-02`，根级横向溢出为 `0 px`。

### 4.2 窄屏内容压力

内置浏览器以真实 CSS 视口而非缩放截图验证：

| 视口 | Catalog 列头 | Catalog / 十字 / 详情溢出 | 已验证内容 | 结论 |
| --- | --- | --- | --- | --- |
| `390 x 844` | `display: none` | 均为 `0 px` | `ABORTED / PENDING` 行、十字展开、负向 `COMPLETED / FAIL` 详情 | PASS |
| `360 x 844` | `display: none` | 均为 `0 px` | 十字展开、正向 `COMPLETED / PASS` 详情 | PASS |

在 `360 px` 下，中心与东/西入口的实际间距均约为 `14.1 px`，三者不相交；触控目标没有靠缩小高度来换取
宽度。该结论只覆盖本切片的 Runs/Catalog 主链和十字骨架，不提前替 M12-E/F 声称 200% zoom、完整
forced-colors 或色觉差异矩阵已经通过。

### 4.3 Console 与 Network 的证据边界

- 内置浏览器的桌面与移动 Tab Console 读取到 `0` 条 `warning` 或 `error`；
- 内置浏览器控制接口没有暴露 Network response 事件或资源时序读取，因此不把它伪称为 F12 Network 抓包；
- 同一生产构建的 M11 Gate B Chromium 受控验收已记录 `113` 个请求、`0` HTTP error、`0` external origin、
  `0` write request、`0` request failure，见第 2 节。这是本切片的完整同源只读 Network/CDP 证据；
  内置浏览器在本节承担真实可见交互、焦点、历史和响应式验证。

## 5. 资源、边界与下一步

本轮在既有的本机回环只读服务上完成浏览器补证；未修改 Docker、中间件、代理、防火墙、系统服务、
Python Core、`web/src/domain/`、Schema、Verdict、Evidence、Catalog、Comparison 或本地只读 API。服务
与端口的最终释放仍须由 M12 后续切片各自的验收和最终 M12-F 统一复核，不能从本节的页面事实外推。

M12 保持 `IMPLEMENTING / NOT_FROZEN`。M12-C 的预注册范围和内置浏览器补证现已闭环，下一入口允许进入
M12-D 的 Comparison、Pairing 与 Batch 表现迁移；Browser Evidence 与全局状态仍属于 M12-E，最终可访问性、
系统和发布级复验仍不得提前完成。
