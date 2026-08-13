# M10 发布安全整改与冻结复验

> 状态：`VERIFIED / FREEZE_PENDING`
> 日期：2026-08-13
> 依据：[M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md)
> 基线扫描：Codex Security Standard Scan `de6f7688-0571-49c8-ab90-a93f553a24f4`

## 1. 目的与顺序

阶段 D 的压力审计通过后，发布门禁对同一候选执行了一次全仓安全扫描。扫描报告列出 2 个中等和
9 个低风险问题；另有 1 个不满足 M10 资源合同、但在“仅运行操作者自己信任的代码”威胁模型下不按
漏洞上报的内存硬限制缺口。M10 不以“风险较低”代替修复，也不把旧的串行/压力绿色结果拼接成新
候选的冻结证据。

整改顺序固定为：

1. 先封闭 Report/Verdict 权威、文件读取和进程创建边界；
2. 再封闭浏览器网络、截图、脱敏、Markdown 和前端语义/容量边界；
3. 把 M10 服务节点与 Chromium 的内存上限写入 sealed Plan/Profile，并由 Windows Job Object 强制；
4. 运行攻击反例与合法控制组；
5. 从 Python 双运行时、前端门禁和 M10 串行轮重新开始；
6. 资源允许时重跑受影响压力波次，最后完成内置浏览器、残留、GitHub 提交和标签读回。

任一安全、权威、所有权、Evidence、Verdict 或清理不变量失败，M10 保持未冻结，M11 不得开始。

## 2. 整改矩阵

| ID | 原问题 | 最小完整整改 | 验证门 |
|---|---|---|---|
| SEC-M10-001 | Catalog 对 M0–M9 Report 只验文件哈希，未独立重推导 Verdict | 由 sealed Plan、同一批已验 Evidence bytes 和 ExecutionStatus 调用 Core `evaluate`，逐字段比对 Report | 伪造 Verdict 并重算 Manifest 仍隔离 |
| SEC-M10-002 | Workbench 直接导入把自报 Verdict 与 Core 权威裁决混在同一“已验证”标签 | 所有 Bundle 必须绑定自封存 Plan；Catalog 来源标记为 `Core 裁决 / 已核验`，直接导入明确标记为 `Bundle 字节 / 自报 Verdict` | 缺失/错绑 Plan 拒绝；两类 UI 标签不混淆 |
| SEC-M10-003 | Preview 后到 `CreateProcess` 前可执行文件身份可漂移 | 普通单链接 PE、路径身份与摘要复核；持有禁止写入/删除/改名的 handle 跨越 `CreateProcess` | 错误摘要不创建进程；重命名 Shell 仍拒绝 |
| SEC-M10-004 | 工作目录在 Preview 后可被替换 | 解析 subject containment、拒绝 reparse，并持有禁止删除/改名的目录 handle 跨越创建 | reparse/身份漂移安全停止 |
| SEC-M10-005 | 浏览器 HTTP 路由未覆盖 WebSocket 与 Service Worker | Context 固定 `service_workers=block`；WebSocket 仅允许 sealed loopback origin | 非回环 WS 关闭，SW 不启动，HTTP 规则保持 |
| SEC-M10-006 | 常见 session/Cookie/认证形式未被文本脱敏器覆盖 | 增加认证头、Cookie/Set-Cookie、session/sid/auth/credential 的键与文本规则 | 合成凭据全部脱敏，普通文本保留 |
| SEC-M10-007 | PNG 像素未做 OCR/图像脱敏 | 不伪称自动脱敏；Plan 0.6 必须显式封存 `UNREDACTED_OPERATOR_ACKNOWLEDGED` | 缺失确认的 M10 Plan 拒绝 |
| SEC-M10-008 | Pair/Batch Markdown 可被 Plan 控制文本注入链接/HTML | 输出前转义 HTML、链接、图片、反引号、括号和换行 | 恶意 limits 只作为文本呈现 |
| SEC-M10-009 | Shell 禁止只比较 basename | 读取 PE `OriginalFilename/InternalName/FileDescription` 并在 Preview/创建前复核 | 复制并重命名的 `cmd.exe` 拒绝 |
| SEC-M10-010 | Catalog 可对一版 bytes 哈希、对另一版 bytes 解析 | 每个文件普通单链接稳定读取一次；同一内存 bytes 同时用于哈希、解析和导入 | 文件身份漂移拒绝；无重开解析 |
| SEC-M10-011 | 浏览器 Evidence 数组只受 Bundle 字节上限约束 | Workbench 对 viewport/step/console/page error/network/screenshot 设置语义上界并核对派生计数 | 501 条 Console 等超界事实拒绝 |
| REL-M10-001 | 服务与 Chromium 只观测 RSS，没有内核级内存硬上限 | ProjectProfile 节点和 Plan 0.6 Browser 封存 MiB 上限；Job Object 同时设置 active-process、job-memory 与 kill-on-close，立即回读并写入 Evidence/Verdict | 未生效不能继续；真实节点/Chromium 与清理复验 |

## 3. 历史兼容与爆炸半径

- `screenshot_safety` 与 Browser Job 内存上限只进入 Plan 0.6，不修改 M3–M9 已冻结 Plan bytes；
- 节点内存上限进入 M10 独立 ProjectProfile 0.1；M9 的 Job 内部获得默认硬上限，但其 Plan 0.5、
  CommandPreview 和 `runtime.command` 公共字段保持不变；
- Catalog 对旧 Plan 的重推导属于消费者验真加固，不修改来源 Bundle；
- Workbench 保留直接查看本地 Bundle 的能力，但不再把“字节完整”写成“Core 已重算”；
- Markdown 仍输出同一信息，只改变不可信控制文本的呈现编码。

整改期间全仓回归曾发现 Python 3.10 的 `HTTPStatus.OK` 在 orchestration `status_counts` 中写成枚举名，
而请求事实落盘为 `200`。生产者现先把请求状态正规化为整数，再生成请求与计数；该问题必须纳入
3.10/3.13 双运行时复验，不能以 Catalog 放宽校验规避。

最终代码质量复审还发现：启动身份虽然已有禁止写入/删除/改名的外层 handle，但摘要曾通过路径二次
打开；浏览器采集异常路径关闭 Job 后也没有逐个关闭已捕获进程 handle。最终候选改为从跨越
`CreateProcess` 的同一 handle 读取 PE 签名与 SHA-256，并在 Browser abort 中释放 Job 和全部进程
handle；两项均有独立回归。Playwright driver 也在 Chromium 启动前进入 owned Job，使 Chromium 从
创建起继承进程数、内存和 kill-on-close 限制，避免事后 Job assignment 与 Chromium sandbox Job 竞争。

## 4. 冻结前复验清单

- [x] 每项安全边界已有最小攻击反例或强等价回归；
- [x] 合法控制组通过聚焦测试；
- [x] Python 3.10 全仓测试、compileall、依赖一致性通过；
- [x] Python 3.13 全仓测试、compileall、依赖一致性通过；
- [x] Workbench test/lint/type-check/build/npm audit 通过；
- [x] M10 严格串行公共退出重新通过；
- [x] 受影响的 bounded microparallel、取消和 1000 总请求压力波次重新通过；
- [x] Codex 内置浏览器完整链路、Console、Network、桌面/移动与键盘复验通过；
- [x] 端口、Job、helper、Chromium、staging 和服务残留为零；
- [x] 修复后按 11 条原攻击路径逐项重审，无未解释发布阻断项；
- [ ] 文档、提交、`origin/main` 和 `m10-v0.11.0` 标签读回一致。

## 5. 最终候选验证事实

- 严格串行公共出口在最后一次代码变更后从第 1 项重启，13/13 通过，用时 41.822 秒；
- Python 3.10.6 与 3.13.13 全仓均为 228/228，分别用时 103.107 秒和 102.298 秒；双运行时
  `compileall`、`pip check` 均通过；
- Workbench 58/58、lint、type-check、production build 通过；production/full npm audit 均为
  0 vulnerabilities；
- 最终压力轮固定种子 `20260813`，Catalog 11 Runs、0 issues、0 duplicates；独立度 1/2/3 共 6 个
  `COMPLETED/PASS`，三个 READY 后取消均为 `USER_CANCELLED / ABORTED/PENDING`，同端口竞争两个 Run
  均安全 `ABORTED/FAIL`；100/200/300/400 四阶共 1000 个回环请求零错误；
- 压力轮可用内存从 7579 MiB 开始，最低 6770 MiB，结束 7496 MiB，未触及 3072/2048 MiB
  软/硬停止线；最终端口和 staging 为零；
- Codex 内置浏览器真实读取同一 Catalog 的 PASS、取消 PENDING 和竞争 FAIL；正向页显示
  `Core 裁决 / 已核验`、13/13 PASS、Console 0、Network 4。刷新/返回、物理 Tab 焦点、资源账册、
  390×844 移动视口均通过，移动 `scrollWidth == clientWidth == 375`，最终 Console warning/error 为零；
- 浏览器标签、临时视口和只读 Catalog server 均已关闭；18774 已释放，server/helper/Chromium 和
  repository staging 均为零。

## 6. 保留的失败事实

本轮没有删除或改写不利运行：

- 首次安全整改后的串行第 4 项把业务失败误报为 `COLLECTOR_ERROR`。根因是 Job 强制终止后未二次
  等待 renderer 句柄释放；修复后二次等待证明 cleanup；
- Python 3.13 全仓曾把正向 Run 随机降级为 `COLLECTOR_ERROR`。40 次诊断抓到 Chromium sandbox Job
  先于事后 assignment；改为 Playwright driver 启动后、Chromium 启动前进入 owned Job；
- Workbench type-check 曾发现 Comparison/Pairing/Batch 缺少 `authorityVerified`。三类本地派生包
  只做字节/结构验证，现明确为 `false` 并有断言，不能冒充 Core 重算；
- 最终代码复审补上同一 pinned handle 摘要与 Browser abort 句柄释放后，13 项、双运行时和压力轮
  再次从头运行，未拼接旧绿色结果。

当前只剩远端可寻址性门禁。只有 `origin/main`、冻结候选提交和 `m10-v0.11.0` 标签均成功读回，
本文与 README 才能由 `FREEZE_PENDING / STRESS_AUDITED` 更新为 `FROZEN`；M11 仍不得开始。
