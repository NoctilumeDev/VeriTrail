# M12-C 空间令牌与 Runs 主链运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_PRODUCTION_CHROMIUM_EVIDENCE / IN_APP_BROWSER_PENDING / M12_NOT_FROZEN`
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

## 4. 内置浏览器待补证

本轮尝试在 Codex 内置浏览器连接同一只读生产工作台时，浏览器控制会话无法把新建或已有标签绑定为
当前会话的可控 Tab。该失败发生在 Codex 浏览器会话层，不是页面 Console、Network、HTTP 或交互失败；
它没有被归入产品 `PASS`。

因此，本事实只证明自动化与生产 Chromium 已完成。下次 M12-C 继续前，必须在可正常绑定的 Codex 内置
浏览器中重跑桌面和 390/360 px 的 Runs/Catalog：验证 Catalog 行、PASS/FAIL/ABORTED+PENDING、详情、
返回焦点、后退/前进、Console 与同源 Network。完成这一事实后，才可将 M12-C 交接到 M12-D。

## 5. 资源、边界与下一步

本轮的临时 `127.0.0.1:18778` Catalog 服务在人工浏览器连接尝试后已显式停止；端口监听和 SQLite
sidecar 均为 0。未修改 Docker、中间件、代理、防火墙、系统服务、Python Core、`web/src/domain/`、
Schema、Verdict、Evidence、Catalog、Comparison 或本地只读 API。

M12 保持 `IMPLEMENTING / NOT_FROZEN`。在第 4 节补证前，下一入口仍然是 M12-C，不能开始 Comparison、
Pairing、Batch 或 Browser Evidence 的最终表现迁移，也不能把现有生产 Chromium 事实包装为 Codex 内置浏览器
事实。
