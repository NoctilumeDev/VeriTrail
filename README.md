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

`FROZEN` 表示该里程碑已在自身边界内完成代码、自动化、适用的真实运行、浏览器、安全与清理
验收，并以 Git 标签形成可寻址基线；它不等于整个 v0 已完成。计划编辑、任意项目命令、真实
并行、完整自举和第二项目证明仍未实现。提交链、保留的失败事实与逐里程碑边界见
[里程碑冻结历史](docs/milestones.md)。

Post-M8 Plan v1 已冻结为**规划基线**；M9–M14 仍只是 `PLANNED`，当前只允许起草 M9 独立
合同，不代表任何后继能力已经实现。

## 为什么需要验迹

工程项目很容易把局部通过误当成整体完成：单元测试是绿色的，但真实浏览器存在失败请求；
单实例正常，多实例产生重复副作用；数据库事实正确，缓存、消息或页面却没有最终收敛；
一次压测写着“并发 1000”，却没有说明它是虚拟用户、同时在途请求、请求总数、RPS，
还是热点竞争数。

验迹不替代测试框架。它解决的是更上层的问题：

> 在明确的环境与资源边界内，这次实验究竟改变了什么，证据是否足以支持结论？

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

- **Python Core**：CLI、计划/证据、确定性裁决、启动前资源预检、有界浏览器采集，以及 M4
  离线 Catalog、固定回环只读 API 与 M8 全因子批次派生分析；通用项目执行编排仍是计划能力。
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
- [M9 受控项目命令执行合同（DRAFT）](docs/14-m9-controlled-command-execution.md)

## 项目来源

验迹的方法论来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、
固定种子复现偶发故障、在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是
重要参考案例，但验迹不会把任何电商服务、中间件或业务状态机硬编码为产品前提。

## License

[Apache License 2.0](LICENSE)
