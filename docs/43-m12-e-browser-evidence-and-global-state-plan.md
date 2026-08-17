# M12-E 浏览器事实与全局状态表现计划 0.1

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
>
> 日期：2026-08-14
>
> 前置事实：[M12-D3 Batch 运行事实](42-m12-d3-batch-facts.md)
>
> 控制组：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
>
> 当前代码基线：D3 已闭环的工作树
>
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
>
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 目标、单一变量与非结论

M12-E 是 M12 的最后一个表现切片，不是 M12-F 的提前终验，也不以“最后一块页面”名义重写全局 Loader、Evidence 或 Verdict。当前 Browser Evidence 已拥有正确的基础交互：四个标准 tabs、roving tabindex、`ArrowLeft` / `ArrowRight` / `Home` / `End`、原生 `dialog` 和关闭后的触发元素焦点恢复；全局状态也已拥有正确的读取、隔离、重试与隐私语义。它们尚未形成同一套清晰、可审计的“证据西庑与状态院落”。

本切片唯一主要变量为：

```text
browser_evidence_and_global_state_presentation = evidence_chamber_and_state_courts_m12
```

它只改变既有事实在 Workbench 中的空间、层级、边界、文本密度、焦点可见性与响应式表现。下列关系必须保持不变：

```text
可信 Run
  -> Browser Evidence 是否存在
       -> steps / Console / Network / screenshots

读取生命周期
  -> loading | empty | invalid-untrusted | operational-error | privacy-reselect
```

两组关系并不互相推出结论。特别是：没有 Browser Evidence 不等于浏览器检查通过；`Console` 或 `Network` 条目不自行重算 Run Verdict；本地文件刷新后的重选要求不是损坏，也不是网络故障。

E 不证明 M12 已完成、全局 200% 浏览器缩放已通过、M13 代码质量已审查或 `m12-v0.13.0` 可以创建。只有 M12-F 可汇集此前所有切片的完整终验并决定冻结。

## 2. 冻结输入与状态样本

实现和生产验收只读取既有、Git 忽略的冻结材料；不新建 M11 运行、不改写历史 Bundle，也不为让视觉状态“更好看”而伪造浏览器事实。

| 输入 | 用途 | 必须保持的事实 |
| --- | --- | --- |
| `tmp/m11-gateb-contract04-20260814-161647` 的四个 Gate B v2 Run | 真实 Catalog/Run、真实 `browser.session`、桌面与移动记录 | `PASS / FAIL / PENDING / PASS`、v1 移动端失败的保留事实、正向恢复 Comparison 均不得被 UI 吞并 |
| 既有 M2 正/负 Browser Bundle | Browser Evidence 的真实正/负浏览器条目、截图附件和有/无异常摘要 | 只读取 Manifest 已验证的原始 Browser Evidence；不把生产数据改造成展示夹具 |
| 内置 `?fixture=positive`、`?fixture=negative`、`?fixture=invalid` | Run 的无 Browser、负向与损坏隔离路径 | `browser-empty` 继续声明“不等于浏览器检查通过”；损坏 Bundle 不展示部分可信内容 |
| 本地 Comparison、Pairing、Batch 的现有四文件入口 | loading、空态、损坏拒绝、刷新隐私重选与恢复 | File 仅留在内存；刷新、Back/Forward 后必须显式重选，不能进入 URL、Catalog 或持久化 |

进入实现前，验收脚本必须先对上述材料逐项做只读输入审计，记录每个来源实际含有的 steps、Console、Network、截图与异常计数。若某个既有生产 Bundle 不含预期的失败类型，不能把组件测试中的合成对象冒充为生产事实；该项保持 `PENDING`，并以新计划版本预注册额外输入后才能补测。

## 3. 所有权、保持项与停止线

### 3.1 必须保持不变

- `web/src/domain/**` 中 Bundle 读取、Manifest/SHA、对象 URL 生命周期、错误映射、Browser 类型与数据上限；
- Python Core、Schema、Evidence、Verdict、Catalog/API、Comparison/Pairing/Batch 的所有语义与权威顺序；
- `App.vue` 的 Loader 调用、`loadSequence` 竞争保护、URL/history、File input 清空、隐私重选、重试和返回焦点；
- Browser Evidence 的四个 tab ID、顺序、`role="tablist"` / `tab` / `tabpanel`、可访问名称、键盘行为、`dialog`、关闭与触发元素焦点恢复；
- 已有 `data-testid`、真实文字语义、状态码、Console/Network 原始条目、图片 URL 和 Run 可读性；
- `StatusBadge.vue`、共享 token 的状态含义、Runs / Comparison / Pairing / Batch 的已闭环范围。

### 3.2 允许所有者

| 文件/区域 | 允许工作 | 明确禁止 |
| --- | --- | --- |
| `web/src/components/BrowserEvidence.vue` | 私有结构分组、私有 class、可读标题/计数/边界、截图 dialog 的布局标记 | 改 tab 顺序、键盘规则、图片加载、事实计算、对话框机制或 focus restoration |
| `web/src/App.vue` | 仅既有 loading / error / empty / privacy-reselect 的表现性分组与 class；保留每条错误文字和当前 action | 改 Loader、state machine、URL/history、retry、File 生命周期、Catalog/API 调用或事实文案含义 |
| `web/src/styles/components.css` | Browser Evidence 与全局 state-court 私有 CSS；删除被该私有规则替代的旧局部规则 | 改 token 语义、`.status-badge`、`.comparison-*`、`.paired-*`、`.batch-*` 或用全局 override 兜底 |
| `web/tests/browser-evidence.test.ts`、`web/tests/app.test.ts` | 对既有 DOM/语义/交互增加回归，覆盖状态区分、长文本与焦点 | 改 domain/Loader 测试以迁就表现 |
| 新建 `scripts/m12_e_browser_evidence_acceptance.py` | 独立生产 Chromium、CDP、状态输入审计、端口与残留检查 | 改产品代码、创建新业务运行或覆写既有 M11/M2 脚本 |

实际 diff 只要触及 domain、Core、Schema、共享 Badge/token、Catalog/API 或本地文件生命周期，就立即停止。这不再是 `L0 + bounded L1`，必须先列出消费者与爆炸半径，不能把它偷渡进 E。

## 4. 状态语义与空间合同

### 4.1 Browser Evidence：西庑账册，不是附属日志

Browser Evidence 保持在 Run 详情的“浏览器事实”区，但内部采用“摘要台基 -> 视口札记 -> 证据四门 -> 具体账册”的阅读顺序：

1. 摘要台基同时显示采集完整性、清理完整性、视口数和异常事实数。`0` 异常必须有文字和固定位置，不是单靠绿色；大于 `0` 的异常必须保留数字、文字、边界和警示朱。
2. 视口记录保留名称、尺寸和根溢出数。`0px` 不等于“所有浏览器验收通过”，只陈述该项事实。
3. tabs 仍是唯一的四个入口：步骤按时间顺序，Console 与 Network 按采集事实，截图按真实附件。选中态、计数、焦点环和 tabpanel 对应关系必须在移除颜色后仍可辨。
4. Steps 是时间线而不是进度装饰。失败 step 保留其 `step_id`、viewport、action、elapsed 与错误文字；不因成功条目更多而折叠或弱化失败。
5. Console 的 level、文本和 viewport；Network 的 method、URL、status/failure 与资源类型都必须完整可读。`error`、HTTP `>=400` 或 request failure 继续以状态文字、图形/边界和位置共同表达，不能被建筑朱、金色选中线或默认折叠掩盖。
6. 截图仍是被验附件，不是主题装饰。缩略图保留名称、viewport、大小和可访问名称；原生 dialog 的关闭、`Esc` 和触发元素焦点恢复必须成立。长 SHA 换行但不撑破 dialog 或根页面。

不得增加第五种 tab、图标-only 控件、点击整块日志的伪折叠、tooltip 依赖、浮层导航、图片背景或古建图案。

### 4.2 五类全局状态：不是一座红色错误宫

`loading`、空、invalid/untrusted、operational error 和 privacy reselect 分别是不同事实。实现可以在 `App.vue` 中为既有分支加入表现 class 或明确描述，但不得合并或改写原有错误码、消息、按钮和 input。

| 状态 | 事实含义 | 必须呈现 | 明确不得误读为 |
| --- | --- | --- | --- |
| `loading` | 读取/哈希/交叉引用尚未结束 | `role=status`、当前在核验什么、非必要动效可降级 | 已通过、失败或页面假死 |
| 空 | 该公共视图尚未选择本地包，或无可读条目 | 下一步选择动作和该视图身份 | `PENDING` Verdict、损坏或网络错误 |
| `no-browser` | Run 已可信加载，但没有 `browser.session` | “未包含浏览器证据”及“不等于浏览器检查通过” | Browser PASS 或错误 Bundle |
| `invalid / untrusted` | Manifest、SHA、解析或来源交叉引用失败 | 错误码、未展示部分可信内容、准确重试/重选动作 | 业务 Verdict 的 FAIL、普通空态或可忽略警告 |
| `operational error` | Catalog/API/读取路径当前不可完成，或 URL Run 不存在 | 错误来源、稳定错误码、适当的目录返回/重试路径 | 输入已可信、隐私行为或结论改变 |
| `privacy reselect` | 刷新/历史恢复后本地 File 未持久化 | “为保护隐私”的明确原因、原视图与原生重新选择入口 | 文件损坏、上传失败、网络错误或数据丢失 |

`invalid / untrusted` 与 `operational error` 可以使用警示朱，但必须保留 code、来源、边界和 action。`privacy reselect` 采用中性或石青的提醒边界，不能使用“止”印或失败朱。空态和 no-browser 使用不同的标题、位置和解释；两者都不是错误。

### 4.3 响应式、可访问性和信息压力

- `1440 x 960` 以证据四门横向可扫描为主；`390 x 844` 与 `360 x 800` 可将摘要和日志纵向展开，但 tab 仍可识别、可进入、可离开。tabs 若因最小触控尺寸需要局部横滚，滚动只发生在具名 `.tab-list`，根页面横向溢出恒为 `0px`。
- 长 Console 文本、Network URL、step error、截图名和 SHA 只能换行或在明确局部边界内滚动，不能裁剪、重叠、改变 tab/header/close button 的稳定尺寸，亦不能令截图 dialog 溢出视口。
- `prefers-reduced-motion: reduce` 下 loading 不旋转、dialog/tab 不使用非必要过渡；阅读与焦点反馈仍清晰。
- `forced-colors: active` / Windows High Contrast 下，状态依靠可见文本、顺序、边界、图形及 action 继续成立；不能仅断言 CSS token 仍存在。
- “200% zoom”只在可证明为浏览器级放大的真实会话中记为通过。生产 CDP 可以检查等价的窄宽 reflow 压力，但不得把 CSS `zoom`、截图缩放或设备像素比伪称为浏览器 200% 缩放；若自动化没有可复现的浏览器级机制，此项交给用户在内置浏览器实际设置后记录为人工事实。

## 5. 测试与实现前置合同

先扩展局部测试，再改私有 DOM/CSS。至少新增以下可重复断言：

1. `BrowserEvidence` 的四个 tab 保持顺序、ARIA 关联、roving tabindex 和 `ArrowLeft` / `ArrowRight` / `Home` / `End`；正常 `Tab` 可以进入和离开该控件组；
2. steps 的时间/错误字段、Console error 与 Network 404/request failure 同时保留文字、来源和状态边界；
3. no-browser 的文字继续明确“不等于浏览器检查通过”；空 Console/Network 不被呈现为成功；
4. 截图按钮的可访问名称、原生 dialog 开启/关闭、`Esc` 和焦点回到原截图触发点；
5. 长 URL、Console 文本和 SHA 在窄宽下不会产生根级溢出；
6. `App` 的 invalid/untrusted、Catalog operational error、空分析视图和 `LOCAL/COMPARISON/PAIRING/BATCH_RESELECT_REQUIRED` 仍分别显示其稳定 code、真实说明与正确入口；
7. 任何 error state 均不显示部分可信 Run/analysis；恢复操作继续使用既有 Loader，不修改 Verdict；
8. 回归保留 D1/D2/D3 及 Runs 的 URL、刷新、历史、文件暂存与焦点合同。

实现应以 Browser 私有 class 和 state-court 私有 class 替换其范围内旧的通用外壳，不得在 `components.css` 末尾追加全局 `!important` 层。若 CSS 审计显示一个选择器由其他切片拥有，停止并保留它。

## 6. 严格实施与生产验收顺序

全部运行遵守 16 GB 单机串行策略。实际启动浏览器、Node、Python 或端口前，重新读取 `C:\Users\lenovo\.codex\machine-profile.md`，再检查当前可用内存、磁盘和回环端口；不启动 Docker、中间件、第二项目栈或 M11 新 Run。

1. **输入与所有权审计**：记录第 2 节材料的只读 SHA/文件存在性、Browser 数据覆盖及当前 git diff；确认只触及本计划所有者。
2. **局部自动化先行**：新增第 5 节断言，先让现有 semantics、dialog/focus、错误/重选区分失败，再写表现。
3. **私有表现实现**：仅迁移 Browser Evidence 和 state-court。用院落、台基、账册、细边和受控朱/青/白建立层次，不使用雾化、柔焦、米灰一统、红金铺底、龙纹、屋檐、云纹、贴图、CDN、远程字体、图标库或遥测。
4. **静态门禁**：串行运行 `npm test`、lint（零 warning）、type-check、production build 和 `git diff --check`。任何失败先定位当前单一变量，不通过删测试、改 domain 或放宽断言解决。
5. **独立生产 Chromium**：新脚本只使用生产 `web/dist`、只读 M11 Catalog 与第 2 节既有输入；默认输出目录拒绝覆盖，显式绑定回环端口。普通 Python 与 `python -O` 各独立运行一次，所有硬门禁只能使用显式 `require()`，不得依赖内建 `assert`。
6. **自动浏览器门禁**：脚本验证 Browser tab 与 URL/history、真实 Browser 事实/无 Browser、Console/Network 失败可见、截图 dialog/focus restoration、invalid 拒绝与恢复、privacy reselect、1440/390/360、长文本、根/局部溢出、reduced-motion、forced-colors，以及每轮的 Console、page error、request failure、同源 `GET/HEAD`、外部 origin、写请求、HTTP 4xx/5xx、重复请求、端口/线程/SQLite sidecar 清理。
7. **Codex 内置浏览器与人工事实**：用户从真实 M11 Catalog 打开有 Browser 的 Run，以物理 `Tab` 进入 tabs，以方向键切换，核对 Console/Network 的失败行，打开截图再以 close/`Esc` 返回原触发点；随后核对 no-browser、损坏隔离、隐私重选与移动视口。在该真实会话中完成 200% 浏览器缩放和 Windows High Contrast 可用时的人工检视。内置浏览器只记录可见内容、物理键盘和焦点；response Network 与 Console 的完整结论仍由 Chromium/CDP 记录，不能称为 F12 response 抓包。
8. **事实归档**：所有门禁均通过后才创建 M12-E facts、同步索引并由用户确认。那仍只是 E 闭环；随后唯一下一入口是 M12-F 计划/终验，不得创建 M12 标签或进入 M13。

## 7. 明确非目标与审阅门禁

本计划不调整 API/Schema、Browser 采集器、数据脱敏、报告生成、Verdict、Catalog、File 生命周期、全局 token、主题切换、国际化、视觉回归快照门禁、M12-F、M13、M14、版本号、提交、推送或发布。

- [x] M12 父合同、D3 事实、现有 Browser Evidence、App 状态分支、测试与 CSS 所有权已经只读审计；
- [x] 单一变量、固定输入、五类状态、焦点/缩放/高对比与生产/人工验收边界已预注册；
- [x] 用户审阅并确认本计划 0.1；
- [x] M12-E 生产代码、测试、构建与独立生产 Chromium 已按本合同完成；
- [x] M12-E 已形成自动化、内置浏览器与用户物理键盘运行事实，见 [M12-E Browser Evidence 与全局状态运行事实](44-m12-e-browser-evidence-and-global-state-facts.md)；
- [ ] M12 已冻结。

本文件是实施合同，不替代运行事实。M12-E 的实际页面、真实 Chromium、Console/Network、物理键盘、资源检查与清理证据见文档 44；M12 仍未冻结。
