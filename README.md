# VeriTrail / 验迹

> 单变量证明因果，组合批次验证交互，固定种子寻找偶发故障，真实链路形成系统结论。

VeriTrail（验迹）是一个面向独立开发者和小型工程团队的本地优先验收证据工作台。
它把分散在测试报告、浏览器 F12、HTTP、数据库、中间件、进程与资源快照中的事实，
组织成可比较、可复现、可审计的实验运行，并使用确定性规则给出结论。

## 当前里程碑

| Milestone | Capability | Status |
| --- | --- | --- |
| M0 | 封存计划、证据导入与确定性裁决 | `FROZEN` |
| M1 | 启动前资源与环境预检 | `FROZEN` |
| M2 | 有界真实 Chromium 证据 | `FROZEN` |
| M3 | 只读 Vue 证据工作台 | `FROZEN` |
| M4 | 本地 Run Catalog 与轻量自举 | `FROZEN` |
| M5 | 有界运行编排与静态目标生命周期 | `FROZEN` |
| M6 | 同计划复跑确定性比较 | `FROZEN` |
| M7 | 预注册四角色配对反事实分析 | `FROZEN` |
| M8 | 全因子批次矩阵与固定种子扰动 | `FROZEN` |
| M9 | 受控项目命令执行 | `FROZEN` |
| M10 | 有界完整项目自举 | `STRESS_AUDITED` |
| M11 | 真实项目功能全链路 | `PLANNED` |
| M12 | 故宫主题前端终稿 | `PLANNED` |
| M13 | 系统思维与分层代码质量终审 | `PLANNED` |
| M14 | 整改后终局复验与发布收束 | `PLANNED` |

`FROZEN` 表示该里程碑已在自身边界内完成代码、自动化、适用的真实运行、浏览器、安全与清理
验收，并以 Git 标签形成可寻址基线；它不等于整个 v0 已完成。计划编辑、任意或不可信项目命令、
正式通用并行、第二项目证明和 M10 最终发布门禁仍未完成。提交链、保留的失败事实与逐里程碑边界见
[里程碑冻结历史](docs/milestones.md)。

`FEATURE_COMPLETE` 只表示当前合同内的功能与公共出口已经实现；`FOUNDATION_REVIEWED` 表示冻结前
M0–M10 地基审查的已知阻断项已整改并完成回归；`SERIAL_VALIDATED` 表示同一冻结候选的公共退出、
双运行时、前端、依赖与内置浏览器已经严格串行复验；`STRESS_AUDITED` 表示同一候选又通过预注册的
16 GB 有界微并行、取消交错和 1000 总请求压力诊断。它们都不是最终发布状态，也不授权提前实现
后继里程碑。

Post-M8 Plan v1 已冻结为**规划基线**；M9 已冻结，M10 Contract 0.2 已冻结，M11–M14
仍为 `PLANNED`。M9 0.2 独立合同已在
`290b618` 冻结；`4d2bc84` 交付 Plan 0.5、ToolBindings 0.1 与只读 CommandPreview 0.1，
`9f979c8` 交付锁定 `pywin32==312` 的 Windows Job Object 所有权后端与真实 helper 自动化。
`fa27b51` 已把审批一致的单个可信命令接入 Plan 0.5 `run`，生成严格的 `runtime.command`、
脱敏文本附件、subject 最终状态差异和清理事实，并完成 Bundle、Catalog、只读 API 与 Workbench
通用读回自动化。`9031719` 新增两个独立轻量 Subject 与真实验收矩阵；可信 Python module、直接
`node.exe` script、重复 Run、适用负向、桌面/移动 Chromium、Catalog 和现有 Workbench 已真实
跑通。Codex 内置浏览器的物理 `Tab/Enter` 已打开非零退出 Run 并读回 `COMPLETED/FAIL`，Console/
Warning 为 0；验收服务、约定端口、M9 进程与临时目录也已完成最终清理复核。GitHub `main` 与
`m9-v0.10.0` 标签均已读回冻结提交 `3181d69`，M9 在合同边界内标记 `FROZEN`。

M10 Contract 0.2 已冻结 Windows 11 / `C1 PROCESS_COLD` 的有界本地进程自举边界。当前实现已有
ProjectProfile 0.1、Plan 0.6 跨文档 seal、BootstrapPreview 0.1、Windows IP Helper listener 表，
以及 M10 独立的长运行 Job session、owned HTTP readiness、双节点串行启动和 best-effort 逆序清理
组件；成功的 pre-teardown fact-finalization 门禁之后，生命周期观测可转换为严格
`runtime.bootstrap`，固定生成四个脱敏流附件。Plan 0.6 Bundle
会同时封存并哈希 Plan/Profile，Catalog 复核 Plan/Profile/Evidence 身份，Comparison 同时要求 Plan SHA
与 Profile SHA，Pairing/Batch 则显式拒绝 0.6。当前内部 observed-run 切片还会创建并核验唯一
Run-owned work/staging，把脱敏的 teardown 前生命周期与流快照规范化落盘、读回并在 teardown 后
复核，同时比较 subject 前后指纹并分账 Core/dependency/application/browser 资源峰值。内部链路现已在
两节点 READY 后调用冻结的 M2 Browser Adapter，校验并引用真实 `browser.session`；M10-only CDP observer
以内存态进程 handles 完成 Chromium RSS 分账与关闭确认，真实双视口正向和选择器失败负向均已通过。
Plan 0.6 现已接入公共 `run`：它重建 live Preview；预检 `PROCEED` 后执行完整 observed-run，
再原子生成同时含 Plan/Profile、preflight/bootstrap/browser Evidence 及附件的不可变 Bundle；真实正向
得到 `COMPLETED/PASS`，可复现选择器失败得到 `COMPLETED/FAIL`，二者均通过 Catalog 验真并释放端口与
owned staging。预检 `STOP_ESCALATION/ABORT` 则在零被测进程下生成只含 preflight 的
`ABORTED/PENDING` Bundle，Catalog 独立验真证据适用性；Preview 摘要不一致仍在进程创建前拒绝且不生成
Run。bootstrap 已开始后的两类公共负向也已实跑：dependency 提前退出形成
`NODE_EARLY_EXIT / COMPLETED/FAIL`，application readiness 超时形成
`READINESS_TIMEOUT / ABORTED/FAIL`；两者都只包含 preflight/bootstrap Evidence、明确不生成 browser
Evidence，并由 Catalog 验真所有权清理事实。application READY 后的 cooperative user cancel 也已接入
公共 Bundle 与 CLI Ctrl+C/Ctrl+Break 桥接，形成 `USER_CANCELLED / ABORTED/PENDING`、零 browser Evidence
和完整逆序清理。实时 Preview 通过后由外部监听者抢占 dependency/application 端口的两种 TOCTOU
场景也已形成预检期 `ABORTED/PENDING` Bundle：受控 runner 从未启动，外部监听者未被接管或终止，
Catalog 与 staging 隔离成立。公共 listener owner mismatch 也已覆盖两个节点：外部 listener 不属于
当前 Job 时绝不判 READY，外部进程按自身计划自然退出，VeriTrail 只逆序回收 owned Job，形成
`LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL` 且 Catalog/清理成立。相同 sealed Plan/Profile 的连续
两次公共正向 Run 也已实跑为
`COMPLETED/PASS`，两份权威一致、首份 Bundle 未被覆盖，M6 Comparison 为 `MATCH` 且轮间无残留；
subject watch root 最终漂移也已贯通公共链路：不回滚用户文件，完整执行保持 `COMPLETED`，但固定
`BOOTSTRAP_SUBJECT_DRIFT` 阻止错误 PASS 并裁决为 `INCONCLUSIVE`。第二类真实项目、
cleanup 注入失败也已形成公共 `CLEANUP_ERROR / ERROR/FAIL` Bundle：应用清理失败不阻断依赖的
best-effort 回收，HARD cleanup 断言与 Catalog 均拒绝伪装 clean。staging 写入失败则以显式
`EVIDENCE_STAGING_FAILED` 进入受限 fallback Evidence，在逆序清理后形成 `EVIDENCE_ERROR / ERROR/PENDING`
公共 Bundle；未知 callback 错误不能使用该 fallback。最后，真实 `COMPLETED/PASS` 与预检
`ABORTED/PENDING` M10 Bundle 已在同一 Catalog 中被独立接纳，损坏副本被隔离；生产 Workbench 又由
Codex 内置浏览器从只读 API 真实读回 `runtime.preflight`、`runtime.bootstrap` 与 `browser.session`，
刷新后仍保持既有裁决，Console/Warning 为零。随后 M0–M10 地基审查发现并修复 Catalog 未完整重推导
Plan 0.6 Report、READY 响应后的 listener ownership 竞态、只读 API 校验后重开文件的竞态，并同步
Workbench M10 版本；双 Python 216/216 与前端门禁通过。其后的严格串行轮又按预注册顺序通过全部
公共出口、修复并保留一次 Python 3.13 editable 环境漂移、从头完成双运行时 216/216，以及生产
Workbench 正负 Run、刷新/返回、键盘、移动端、Console 与页面资源账册验收。M10 因而进入
`SERIAL_VALIDATED`，但 16 GB 压力轮、最终发布门禁与标签均未完成，不得标记 `FROZEN`。C2/C3、Docker
与跨平台不属于 M10 已证明范围。

## 为什么需要验迹

工程项目很容易把局部通过误当成整体完成：单元测试是绿色的，但真实浏览器存在失败请求；
单实例正常，多实例产生重复副作用；数据库事实正确，缓存、消息或页面却没有最终收敛；
一次压测写着“并发 1000”，却没有说明它是虚拟用户、同时在途请求、请求总数、RPS，
还是热点竞争数。

验迹不替代测试框架。它解决的是更上层的问题：

> 在明确的环境与资源边界内，这次实验究竟改变了什么，证据是否足以支持结论？

## 证据边界与诚信用途

预注册计划、保留不利运行、交叉证据和不可变 Bundle，会让事后移动标准、只挑最好结果、遗漏
失败事实和随手改报告更容易暴露。因此 VeriTrail 可以提高低成本造假的成本，对“偷懒的造假”
形成附带威慑，也可以作为复现、审查或审计的辅助材料。

但它不是学术不端检测器，也不是反欺诈、取证、可信时间戳或身份认证系统。一次 `PASS` 只表示：
在声明边界内，当前 Bundle 中的证据足以支持 sealed assertions；它不证明研究命题在现实中为真，
不证明样本具有代表性、未披露数据不存在，亦不证明操作者诚实。若同一方能够预先设计虚假 Subject、
Plan、适配器和输入，或重建整套自洽 Bundle，VeriTrail 不能单独识别这种精心设计的骗局。内容哈希
可以发现 Bundle 内未同步的变化，但没有外部可信锚点时，不能证明来源真实性或阻止整包重制。

VeriTrail 的设计初衷仍是工程验收与证据治理。相同机制也可用于教育、研究或合规场景，但用途和
治理责任由使用者决定；高风险结论仍需要独立数据来源、同行审查、外部签名/时间锚和独立复现。

## 核心方法

1. **基线**：冻结代码版本、配置、数据、拓扑、负载语义和资源预算。
2. **单变量串行**：一次只改变一个主要变量，用来建立因果证据。
3. **分批组合**：覆盖所有声明的 Profile，验证组件之间的交互，但不突破宿主机预算。
4. **固定种子扰动**：在确定性矩阵之后随机化批次或故障顺序，并保存种子以便复现。
5. **代表性全链路**：在资源允许的最大有效组合上运行真实浏览器、故障、恢复和一致性验收。

硬件限制可以停止升压，但不能降低业务不变量。资源超限是一次运行被中止，不等于产品失败；
多个主要变量同时变化会使结论不可归因，也不能包装成通过。

## 结论语言

运行状态与验收结论分开记录：

| 维度 | 值 | 含义 |
| --- | --- | --- |
| 运行状态 | `PLANNED / RUNNING / COMPLETED / ABORTED / ERROR` | 实验是否完整执行 |
| 验收结论 | `PASS / FAIL / INCONCLUSIVE / PENDING` | 当前证据能否支持判断 |

- `PASS`：适用证据齐全，且所有硬性不变量成立。
- `FAIL`：至少一个硬性不变量被可复现证据否定。
- `INCONCLUSIVE`：变量污染、环境漂移、证据冲突或其他问题导致无法归因。
- `PENDING`：计划尚未取得要求的真实证据。
- `ABORTED` 是运行状态；例如触发内存停止线时保存现场，不伪造 `PASS` 或 `FAIL`。

## v0 闭环

首个可运行版本计划完成：

- 定义基线、主要变量、受控变量、批次、负载语义、不变量和停止条件；
- 采集环境、版本、资源、进程、端口和拓扑快照；
- 导入测试、覆盖率、HTTP/HAR、日志和自定义断言证据；
- 通过真实 Chromium 记录 Console、Network、截图和关键交互；
- 为证据生成清单与哈希，使用确定性规则计算结论；
- 导出可读 Markdown 与机器可读 JSON 证据包；
- 先用一个轻量前端项目完成自举验收，再扩展真实后端和多实例适配器。

## M0 可运行切片

M0 使用 Python 3.10+ 标准库实现，不依赖数据库、Docker 或云服务。当前可以：

- 校验单变量实验计划，并用规范化 JSON 和 SHA-256 在首次运行前封存；
- 导入受大小限制的结构化 JSON 证据，落盘前脱敏认证字段、令牌、用户目录、邮箱和 IP；
- 检测未知变量、受控变量漂移、证据冲突、过期基线和证据缺口；
- 确定性计算 `PASS / FAIL / INCONCLUSIVE / PENDING`，并与 ExecutionStatus 分开保存；
- 导出 `report.json`、`report.md`、脱敏证据和两层哈希清单；
- 拒绝覆盖已有计划文件或 Run 目录。

M0 暂时只接受 `SINGLE_VARIABLE` 和结构化 JSON 导入，不采集浏览器、资源或项目命令。
完整边界见 [M0 纵向切片](docs/04-m0-vertical-slice.md)。

## M1 资源预检

`ExperimentPlan 0.2` 新增封存的预检策略，`preflight` 子命令会在启动工作负载前只读采集
可用内存、输出卷空间、采集器 RSS、显式回环端口和 VeriTrail 临时目录残留，并生成
`runtime.preflight` 证据包：

```powershell
.\.venv\Scripts\veritrail.exe preflight `
  --plan examples\preflight\plan-proceed.json `
  --run-id my-preflight-run `
  --output artifacts\my-preflight-run
```

资源决策与最终 Verdict 分开：

- `PROCEED`：当前起点允许进入下一阶段；
- `STOP_ESCALATION`：停止增加负载或并行度；
- `ABORT`：输出 `ABORTED`，没有独立业务失败证据时 Verdict 保持 `PENDING`。

M1 不执行项目命令，不启动/停止服务或容器，不枚举全部进程/端口，也不修改代理、防火墙和
系统参数。Plan 0.1 的 M0 行为保持兼容；只有 Plan 0.2 可以运行 `preflight`。

## M2 真实浏览器证据

`ExperimentPlan 0.3` 在 Plan 0.2 预检之后增加有界的 `browser-capture`：只允许显式回环
HTTP origin 和结构化步骤，按视口串行创建一个 Chromium Context 与 Page，并采集 Console、
页面异常、Network、步骤时间线、横向溢出和 PNG 截图。

浏览器能力作为可选依赖安装：

```powershell
.\.venv\Scripts\python.exe -m pip install --editable ".[browser]"
.\.venv\Scripts\python.exe -m playwright install chromium
```

在一个终端启动仓库内的非秘密夹具：

```powershell
.\.venv\Scripts\python.exe -m http.server 18765 `
  --bind 127.0.0.1 `
  --directory examples\browser\site
```

在第二个终端运行正向计划：

```powershell
.\.venv\Scripts\veritrail.exe browser-capture `
  --plan examples\browser\plan.json `
  --run-id my-browser-run `
  --output artifacts\my-browser-run
```

适配器不会持久化请求/响应头、Cookie、正文或 URL 查询值，也不会启动被测站点、读取浏览器
Profile 或执行任意 Shell。截图作为二进制附件进入 Evidence 清单与 Bundle 清单。Console、
页面错误、请求失败、4xx/5xx、重复写请求和横向溢出仍由封存断言裁决，不由适配器直接写
`PASS/FAIL`。完整边界见 [M2 真实浏览器证据](docs/06-m2-browser-evidence.md)。

## M3 Vue 证据工作台

M3 在 `web/` 中提供 Vue 3、TypeScript 与 Vite 的只读工作台。它会在显示前逐文件校验
Bundle Manifest 的路径、大小和 SHA-256，分开呈现 ExecutionStatus 与 Verdict，并展示断言、
Evidence 索引、浏览器步骤、Console、Network、视口和证据截图。仓库内置脱敏正/负/损坏包；
也可选择本地证据目录，文件只在浏览器内存中读取，不上传、不持久化。

“宫阙验迹 / Palace Evidence”使用纯 CSS 中轴、院落、格栅和状态令牌，不依赖装饰贴图、CDN、
远程字体或统计脚本。宫墙朱只表达 `FAIL`、`ERROR` 和异常；状态同时具备文字、符号和可访问
标签，不依赖颜色判断。

```powershell
Set-Location web
npm ci
npm run lint
npm test
npm run build
npm run preview
```

默认开发与预览服务只绑定 `127.0.0.1`。M3 不重新裁决报告，不执行项目命令，也不提供
SQLite、本地 API、计划编辑或跨 Run 比较。完整边界与冻结证据见
[M3 Vue 证据工作台](docs/07-m3-vue-workbench.md)。

## M4 本地 Run 目录（FROZEN）

M4 验证一条完整但窄的增量链路：离线校验多个不可变 Bundle，生成可重建的 SQLite
目录快照；由只读同源回环 API 供 Workbench 发现和选择 Run；最后把一份针对 VeriTrail
工作台自身生成的真实验收 Bundle 再次索引并读回。

这里的 SQLite 是派生索引，不是 Report、Evidence 或 Verdict 的事实来源。`catalog-build`
离线生成新快照，`catalog-serve` 只绑定 `127.0.0.1` 并提供 GET/HEAD 同源 API 与 Vue 生产构建；
服务期间没有数据库或 Artifact 写入者：

```powershell
.\.venv\Scripts\veritrail.exe catalog-build `
  --artifacts artifacts\m4-seeds `
  --output artifacts\m4-catalog

.\.venv\Scripts\veritrail.exe catalog-serve `
  --catalog artifacts\m4-catalog `
  --artifacts artifacts\m4-seeds `
  --web-root web\dist `
  --port 18767
```

生产构建、真实 HTTP 与桌面/移动 Chromium 验收：

```powershell
.\.venv\Scripts\python.exe scripts\m4_catalog_acceptance.py
```

完整退出门槛、失败反例与冻结证据见
[M4 本地 Run 目录与轻量自举](docs/08-m4-local-run-catalog.md)。

## M5 有界运行编排（FROZEN）

M5 使用向后兼容的 Plan 0.4 和一个 `run` CLI，把预检、内置只读静态回环目标、真实
Chromium、裁决、Bundle 与清理串成单一不可覆盖 Run。它不会执行任意 Shell、npm/Maven、
Docker 或项目服务命令，也不管理外部中间件。定义、自动化和真实运行的分层记录见
[M5 有界运行编排与静态目标生命周期](docs/09-m5-bounded-run-orchestrator.md)。

```powershell
.\.venv\Scripts\veritrail.exe run `
  --plan .\examples\orchestration\plan.json `
  --subject-root . `
  --run-id my-unique-run `
  --output .\artifacts\my-unique-run

.\.venv\Scripts\python.exe .\scripts\m5_orchestrator_acceptance.py `
  --output .\artifacts\my-unique-m5-acceptance
```

## M6 同计划复跑确定性比较（FROZEN）

M6 把两个独立、不可变、同 sealed Plan 的 Run 生成独立 Comparison Bundle，并在 Workbench
本地只读验真。它只判断已裁决语义的 `MATCH / DRIFT / INCONCLUSIVE`，不改写来源 Verdict，
也不把不同变量的处理效果冒充为本里程碑能力。双 Python、真实 Run、三态比较、逐字节复建、
生产与 Codex 内置浏览器、安全、资源和清理终验均已完成：

```powershell
.\.venv\Scripts\veritrail.exe compare `
  --baseline .\artifacts\baseline-run `
  --repeat .\artifacts\repeat-run `
  --output .\artifacts\comparison-baseline-repeat
```

完整预注册门槛、失败反例与冻结事实见
[M6 同计划复跑确定性比较](docs/10-m6-deterministic-rerun-comparison.md)。

## M7 预注册四角色配对反事实分析（FROZEN）

M7 冻结实现固定 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL`，只允许
ExperimentPlan 的版本、唯一主要变量值和 seal 变化。它生成独立 PairedAnalysis，不改写来源
Verdict；真实三态、损坏输入、确定性复建、Catalog 隔离和浏览器验收事实见
[M7 预注册四角色配对反事实分析](docs/11-m7-preregistered-paired-analysis.md)。

## M8 全因子批次矩阵与固定种子扰动（FROZEN）

M8 Core 要求先串行覆盖完整全因子 Profile 矩阵，再以 `SHA256_RANK_V1` 和固定种子生成
成员不变的扰动顺序；CoverageStatus、HypothesisStatus 与每个来源 Run Verdict 分开。当前已
实现 BatchPlan、RunAssignment、BatchAnalysis、Manifest 与两个 CLI，并自动化验证三态、顺序
污染、来源失败保留、确定性复建、损坏拒绝和 Catalog 隔离。Workbench 已实现显式四文件
导入、完整性/Plan seal、全因子与固定种子顺序重算、双状态、来源 Verdict 和 wave 边界展示。
`scripts/m8_batch_acceptance.py` 已在 16 GB Windows 主机上用 8 个独立 M5 `run` 完成 2×2
coverage 与固定种子 perturbation，并验证四类分析结果、逐字节复建、反例和清理。
`scripts/m8_batch_browser_acceptance.py` 与 Codex 内置浏览器已经验证四态导入、来源 `FAIL` 保留、
损坏恢复、刷新/返回、桌面/移动、Console/Network 和同源只读边界；最后由人工系统键盘在内置
浏览器中证明焦点从四文件入口移动到全因子矩阵。M8 不执行项目命令或真实并行，也不做统计
显著性和组件级多变量因果；冻结证据与完整边界见
[M8 预注册全因子批次矩阵与固定种子扰动](docs/12-m8-preregistered-batch-matrix.md)。

```powershell
.\.venv\Scripts\python.exe .\scripts\m8_batch_acceptance.py `
  --output .\artifacts\my-unique-m8-batch
```

生产 Workbench 的有界真实 Chromium 复验使用四个真实分析目录，并拒绝覆盖既有输出：

```powershell
.\.venv\Scripts\python.exe .\scripts\m8_batch_browser_acceptance.py `
  --supported .\artifacts\m8-batch-runtime\analyses\supported `
  --contradicted .\artifacts\m8-batch-runtime\analyses\contradicted `
  --incomplete .\artifacts\m8-batch-runtime\analyses\incomplete `
  --inconclusive .\artifacts\m8-batch-runtime\analyses\inconclusive `
  --output .\artifacts\my-unique-m8-browser
```

## M9 受控项目命令执行（FROZEN）

M9 只允许一个用户信任并明确批准的 `ONESHOT`：结构化参数直接启动普通 `.exe`，不经过 Shell、
stdin/TTY、npm/Maven 或 Docker。正向命令结束后继续 M5 的静态目标、双视口 Chromium、裁决与
不可变 Bundle；非零、超时、最终状态漂移和长存后代保留各自的状态语义。

仓库中的真实矩阵使用两个独立轻量 Subject，所有 Plan 在首个 Run 前一次性封存，并串行运行：

```powershell
.\.venv\Scripts\python.exe .\scripts\m9_command_acceptance.py `
  --node-executable C:\path\to\node.exe `
  --output .\artifacts\my-unique-m9-command-acceptance
```

通过最多证明冻结合同对本次可信 Python module 与直接 Node script 成立；不证明文件系统/网络
隔离、恶意代码 containment、通用包管理器、长运行服务、其他平台或完整自举。

## M10 有界完整项目自举（STRESS_AUDITED）

M10 在 M9 的可信进程所有权基础上，只增加 Windows 11/C1 的长运行生命周期：按依赖顺序启动
两个本地可信进程，以回环 HTTP 与 Job process list 共同证明就绪，由现有 Browser Adapter 完成
exercise，最后按应用、依赖的逆序强制回收并证明无残留。当前组件片已用真实 Windows 子进程与
端口验证：每节点独立 Job、依赖 READY 后才创建应用、listener owner 与实时 Job process list
交叉核验、连续两次 HTTP 200、失败后应用到依赖的逆序回收，以及 cleanup 失败时继续 best-effort
清理。该内存态组件本身不直接生成公共 Evidence；随后完成的证据切片已把该观测严格转换为
`runtime.bootstrap`，并要求 pre-teardown facts 先经回调封存成功，固定校验
两节点 stdout/stderr 四个附件，并让 Plan 0.6 Bundle、Catalog 与 Comparison 验证 sealed Profile；
Pairing/Batch 对 0.6 明确拒绝。当前还实现了带所有权 marker 的 Run work/staging、teardown 前脱敏
事实与流快照封存/读回、teardown 后安全释放，以及 subject 前后指纹和四方资源分账；真实 Windows
helper 已覆盖成功、subject 漂移不回滚和 staging 写入失败仍逆序清理。冻结的 M2 Browser Adapter
现已在两节点 READY 后生成并校验真实 `browser.session`，由 CDP 进程身份完成 Chromium RSS 与关闭
观测；双视口正向和缺失选择器负向都保持先封存、再逆序清理。公共 Plan 0.6 `run` 现已接通
Preview 精确审批、`PROCEED` 预检、真实 Browser、确定性裁决和不可变 Bundle/Catalog 验真；正向为
`COMPLETED/PASS`，业务步骤负向为 `COMPLETED/FAIL`，审批不一致与预检停止均保证零进程启动。
其中预检 `STOP_ESCALATION/ABORT` 已形成仅含 preflight 的 `ABORTED/PENDING` Bundle，不伪造
bootstrap/browser 生命周期；审批不一致仍为零 Bundle 拒绝。dependency 提前退出与 application
readiness 超时也已通过公共 `run` 形成严格的无 browser Bundle，分别裁决为
`COMPLETED/FAIL` 与 `ABORTED/FAIL`，并完成 Catalog 与端口/staging 清理验证。application READY 后
user cancel 也形成 `USER_CANCELLED / ABORTED/PENDING`，CLI 会把
Ctrl+C/Ctrl+Break 转为 cooperative cancel、等待证据封存和逆序清理，并恢复原 signal handler。其余
实时 Preview 通过后再由外部监听者抢占 dependency/application 端口的公共场景，均在 preflight
安全停止为 `ABORTED/PENDING`，未启动受控 runner、未误杀外部监听者且 Catalog 可验真。listener owner
mismatch 已在 dependency/application 两个节点公共实跑，均拒绝 READY、不启动 Browser、
不终止外部进程，并在外部进程自然退出后完成 owned Job 逆序清理；封存 HARD readiness 断言使结果为
`ABORTED/FAIL`。相同 sealed Plan/Profile 连续两次公共正向 Run 均为 `COMPLETED/PASS`，Comparison
为 `MATCH`，首份 Bundle 未被第二轮修改且轮间端口/staging 为零。subject drift 公共切片还发现并
修复了“Evidence 已记录漂移但 Verdict 错误 PASS”的消费者缺口；现在用户文件保持变化、不自动回滚，
结果为 `COMPLETED/INCONCLUSIVE` 且清理/Catalog 成立。cleanup 注入失败公共链路继续完成
application→dependency 两节点回收，并以 `CLEANUP_ERROR / ERROR/FAIL` 保留失败节点，不把实际
best-effort 成功冒充观测 clean。staging 写入失败也已从“清理后无 Bundle”提升为受限失败 Bundle：
真实 Browser 事实保留、逆序清理完整，ExecutionStatus/Verdict 为 `ERROR/PENDING`，绝不支持 PASS。
Catalog 组合门禁与生产 Workbench 的内置浏览器通用账册读回已经完成。其后的 M0–M10 地基审查已
整改 Catalog 报告重推导、readiness 响应后所有权和只读 API 稳定读取三个接缝；严格串行轮也已
逐出口、双运行时、前端、依赖和内置浏览器通过。其后同一最终候选从头完成 16 GB 有界压力轮：
同端口竞争安全失败，独立度 1/2/3 全部 PASS，三个 READY 后取消全部形成
`USER_CANCELLED / ABORTED/PENDING`，1000 次回环只读请求零错误，最低可用内存 7529 MiB，11 个 Bundle
和 Catalog 独立回读成立；最终候选最低可用内存 7323 MiB 且零残留。M10 当前为 `STRESS_AUDITED`，
仍未通过最终发布门禁。详见
[M10 有界完整项目自举合同 0.2](docs/15-m10-bounded-project-bootstrap.md)。M10 只有在功能矩阵闭环后，
才进入 M0–M10 地基系统/代码审查、严格串行完整复验和 16 GB 有界压力审计；开发期回归不冒充最终
两轮，具体顺序见
[M10 完成、地基审查与双轮冻结计划 0.1](docs/16-m10-completion-and-foundation-audit.md)，已完成的
地基审查事实见 [M10 动态地基系统与代码质量审查](docs/17-m10-foundation-review.md)，严格串行事实见
[M10 第一轮严格串行完整复验](docs/18-m10-serial-validation.md)，压力事实见
[M10 第二轮 16 GB 有界压力审计](docs/19-m10-bounded-stress-audit.md)。

### 本地运行

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install --editable .

.\.venv\Scripts\veritrail.exe seal `
  --plan examples\minimal\plan.json `
  --output artifacts\m0-sealed-plan.json

.\.venv\Scripts\veritrail.exe evaluate `
  --plan artifacts\m0-sealed-plan.json `
  --evidence examples\minimal\evidence-pass.json `
  --run-id my-first-run `
  --output artifacts\my-first-run
```

每个 Run ID 应唯一；已有输出不会被覆盖。运行测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 计划架构

- **Python Core**：CLI、计划/证据、确定性裁决、启动前资源预检、有界浏览器采集、M4 离线
  Catalog、固定回环只读 API、M8 全因子批次派生分析与 M9 可信一次性命令；M10 已进入合同层
  实现，并已有独立长运行 Job/readiness/逆序清理、严格 bootstrap Evidence、Plan/Profile Bundle
  验真、Run-owned staging、subject 指纹、资源分账和真实 Browser exercise；公共 Plan 0.6 `run` 的
  `PROCEED` 正/负、全部公共退出矩阵、Catalog 隔离与 Workbench 通用账册读回已经接入；冻结前地基
  审查、严格串行轮和 16 GB 有界压力轮已完成，最终发布门禁仍待完成。
- **SQLite**：M4 已实现的可删除、可重建派生目录快照；更完整的本地元数据、运行关系和结论
  索引仍是后续目标。
- **Artifact Store**：日志、HAR、截图、报告与哈希清单；默认不进入 Git。
- **Vue Workbench**：已实现 M3 只读证据包、断言和浏览器事实浏览，以及 M6 Comparison、
  M7 PairedAnalysis 与 M8 BatchAnalysis 的本地验真；计划编辑和报告发布仍是后续能力。
- **Browser Adapter**：已实现基于 Playwright/Chromium 的回环站点证据采集；远程站点、认证、
  多角色与并行 Context 仍不在 M2 范围。

v0 不引入 Docker、微服务或云端必需依赖，不执行任意 Shell 字符串，也不让 AI 决定
`PASS/FAIL`。未来 AI 可以解释异常或建议下一步，但裁决权始终属于确定性规则。

## 文档

- [里程碑冻结历史](docs/milestones.md)
- [产品定义](docs/00-product-brief.md)
- [证据与实验模型](docs/01-evidence-model.md)
- [架构与安全边界](docs/02-architecture.md)
- [验收标准](docs/03-acceptance.md)
- [M0 纵向切片](docs/04-m0-vertical-slice.md)
- [M1 资源与环境预检](docs/05-m1-resource-preflight.md)
- [M2 真实浏览器证据（FROZEN）](docs/06-m2-browser-evidence.md)
- [M3 Vue 证据工作台（FROZEN）](docs/07-m3-vue-workbench.md)
- [M4 本地 Run 目录与轻量自举（FROZEN）](docs/08-m4-local-run-catalog.md)
- [M5 有界运行编排与静态目标生命周期（FROZEN）](docs/09-m5-bounded-run-orchestrator.md)
- [M6 同计划复跑确定性比较（FROZEN）](docs/10-m6-deterministic-rerun-comparison.md)
- [M7 预注册四角色配对反事实分析（FROZEN）](docs/11-m7-preregistered-paired-analysis.md)
- [M8 预注册全因子批次矩阵与固定种子扰动（FROZEN）](docs/12-m8-preregistered-batch-matrix.md)
- [Post-M8 收束路线 Plan v1（FROZEN planning baseline）](docs/13-post-m8-roadmap.md)
- [M9 受控项目命令执行合同 0.2（CONTRACT_FROZEN）](docs/14-m9-controlled-command-execution.md)
- [M10 有界完整项目自举合同 0.2（CONTRACT_FROZEN）](docs/15-m10-bounded-project-bootstrap.md)
- [M10 完成、地基审查与双轮冻结计划 0.1（FROZEN execution plan）](docs/16-m10-completion-and-foundation-audit.md)
- [M10 动态地基系统与代码质量审查（FOUNDATION_REVIEWED）](docs/17-m10-foundation-review.md)
- [M10 第一轮严格串行完整复验（SERIAL_VALIDATED）](docs/18-m10-serial-validation.md)
- [M10 第二轮 16 GB 有界压力审计（STRESS_AUDITED）](docs/19-m10-bounded-stress-audit.md)

## 项目来源

验迹的方法论来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、
固定种子复现偶发故障、在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是
重要参考案例，但验迹不会把任何电商服务、中间件或业务状态机硬编码为产品前提。

## License

[Apache License 2.0](LICENSE)
