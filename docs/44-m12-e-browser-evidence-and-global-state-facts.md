# M12-E Browser Evidence 与全局状态运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
>
> 前置合同：[M12-E 浏览器事实与全局状态表现计划 0.1](43-m12-e-browser-evidence-and-global-state-plan.md)
>
> 前置事实：[M12-D3 Batch 运行事实](42-m12-d3-batch-facts.md)
>
> 影响：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`；未触及 `L2_CONTRACT / L3_SYSTEM`

## 1. 已实现的表现关系

`BrowserEvidence.vue` 现在按“摘要台基 -> 视口札记 -> 证据四门 -> 具体账册”组织既有 Browser
Evidence：采集与清理、视口数和异常事实数首先可见，随后保持原有四个 ARIA tab 的步骤、Console、Network
与截图入口。失败 step、Console error、HTTP error/request failure 仍以原始文本、数字和位置呈现；未增加
第五个 tab，也没有重算来源 Run 的 Verdict。

`App.vue` 只为既有读取分支补充 `data-state-kind` 与私有表现 class。`invalid`、`operational`、`privacy`、
`no-browser` 与空态保持独立：损坏 Bundle 不显示部分可信内容，Catalog 读取错误保留稳定 code，本地文件刷新后
仍明确要求重新选择而非被表述为损坏，缺少 `browser.session` 仍明确写作“不等于浏览器检查通过”。

代码只改动本合同列出的 `BrowserEvidence.vue`、`App.vue`、私有 `components.css`、对应 Vue 回归与独立验收脚本。
`StatusBadge.vue`、共享 token、domain、Python Core、Catalog/API、Schema、Verdict、URL/history、Loader 与本地
File 生命周期均未改动。

## 2. 自动化与生产 Chromium

| 门禁 | 结果 | 事实 |
| --- | --- | --- |
| Workbench 回归 | `70/70 PASS` | 保留四 tab、失败事实、原生 dialog 与焦点恢复；新增 no-browser、invalid 与 privacy reselect 分层回归 |
| lint / type-check / production build / `git diff --check` | `PASS` | 零 warning；生产构建和 diff 格式均可通过 |
| `m12_e_browser_evidence_acceptance.py` | `9/9 PASS` | M11 四个真实 Run、M2 正/负/损坏 Bundle、M8 本地 Batch 四文件入口；桌面、390px、360px、reduced motion 与 forced colors |
| 同一脚本 `python -O` | `9/9 PASS` | 关键门禁全部使用显式 `require()`，优化模式没有移除裁决条件 |

两轮只读生产 Chromium 分别使用独立回环端口和不可覆盖输出目录。每轮 `97` 个请求均为同源
`GET/HEAD` 或本地 blob：外部 origin、写请求、HTTP error、Console warning/error、page error 与 request
failure 均为 `0`。两轮均验证：负向 M2 中 Console 与 Network 失败行可见、截图 dialog 与触发焦点恢复、
invalid 拒绝后正向恢复、M11 无 Browser 的 `ABORTED / PENDING`、不存在 Run 的 operational error、刷新后的
Batch privacy reselect、360/390px 根无横向溢出与 forced-colors 文本/边界/focus 合同。服务线程停止，端口释放，
Catalog 未留下 SQLite sidecar；最小可用内存为 `7041.578 MiB`。

历史自动验收反例均保留在 Git 忽略的 artifacts：早期对负向 timeline、截图 SHA 与 tab 选择的错误假设，以及
`360px` 根溢出定位和修正过程没有被删改或覆盖。

## 3. 内置浏览器与人工键盘

在独立只读预览 `127.0.0.1:18782` 中，内置浏览器真实读取冻结 M11 Catalog/Run 和当前生产 `web/dist`。
浏览器可见链路确认如下：

- M2 负向包保持 `COMPLETED / FAIL`、三项失败断言、Browser summary 与四个证据 tab；Console/Network 的失败事实未被主题吞没；
- M11 port-conflict Run 显示 `ABORTED / PENDING` 与 `BROWSER EVIDENCE · 未适用`，并保留“不等于浏览器检查通过”；
- 损坏 Bundle 显示 `MISSING_ROOT_FILE`、不展示部分可信内容，既有正向重试恢复 `COMPLETED / PASS`；
- 真实选择 M8 Batch 四文件后可进入分析；刷新后显示 `BATCH_RESELECT_REQUIRED` 和“为保护隐私”，没有持久化或上传文件；
- 用户物理 `Tab` 进入“浏览器事实”，再进入 tablist 的“步骤”；方向键在四个标签间工作。到“截图”后，`Tab` 到截图触发器、`Enter` 打开，`Esc` 关闭；触发元素焦点恢复由上节生产 Chromium 与组件回归共同证明；
- 用户在浏览器 `200%` 缩放下复验。实际可视内容宽约 `354px`，根 `scrollWidth - clientWidth = 0px`；四个 tab 仍存在，局部横向移动只发生在具名 tablist，而非根页面。截图 dialog 的人工打开/关闭路径仍成立。

内置浏览器页面 Console 记录为零 warning/error。响应级 Network、外部 origin、写请求及 HTTP 错误的完整事实以
上节生产 Chromium/CDP 输出为准；内置浏览器没有被表述为 response 抓包。自动 forced-colors 已通过；本切片没有把
该自动事实伪称为人工 Windows High Contrast 事实。

本轮预览结束后，由本切片启动的 Python 只读服务已停止，`18782` 监听释放；原用户拥有的 `18778` 预览没有被接管或停止。

## 4. 结论与后继边界

M12-E 的单一变量 `browser_evidence_and_global_state_presentation = evidence_chamber_and_state_courts_m12` 已在固定
输入、自动化、生产 Chromium、内置浏览器和物理键盘下取得运行事实。它只证明 Browser Evidence 与既有全局状态的
表现和交互没有破坏各自的证据语义。

它不证明 M12 整体视觉终稿、M13 系统/代码质量审查、M14 发布复验、版本号、标签或 Release。唯一后继入口是先建立
M12-F 总体验收计划；M12 继续为 `IMPLEMENTING / NOT_FROZEN`。
