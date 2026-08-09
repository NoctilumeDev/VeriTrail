# VeriTrail / 验迹

> 单变量证明因果，组合批次验证交互，固定种子寻找偶发故障，真实链路形成系统结论。

VeriTrail（验迹）是一个面向独立开发者和小型工程团队的本地优先验收证据工作台。
它把分散在测试报告、浏览器 F12、HTTP、数据库、中间件、进程与资源快照中的事实，
组织成可比较、可复现、可审计的实验运行，并使用确定性规则给出结论。

**当前状态：v0 Implementation，M0/M1/M2/M3 FROZEN。** M0 已冻结计划封存、
结构化证据导入、确定性裁决和 JSON/Markdown 证据包；M1 已冻结启动前资源预检；M2 已冻结
有界真实 Chromium 采集；M3 已冻结只读 Vue 证据工作台和“宫阙验迹”故宫色彩主题。
SQLite、本地 API、计划编辑、执行编排和完整自举仍是后续里程碑，不能从路线图文字推断为
已完成能力。

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

- **Python Core**：CLI、计划/证据、确定性裁决、启动前资源预检和有界浏览器采集；本地 API
  与通用执行编排仍是计划能力。
- **SQLite**：本地元数据、运行关系和结论索引。
- **Artifact Store**：日志、HAR、截图、报告与哈希清单；默认不进入 Git。
- **Vue Workbench**：已实现 M3 只读证据包、断言和浏览器事实浏览；实验矩阵、计划编辑、
  跨 Run 差异和报告发布仍是后续能力。
- **Browser Adapter**：已实现基于 Playwright/Chromium 的回环站点证据采集；远程站点、认证、
  多角色与并行 Context 仍不在 M2 范围。

v0 不引入 Docker、微服务或云端必需依赖，不执行任意 Shell 字符串，也不让 AI 决定
`PASS/FAIL`。未来 AI 可以解释异常或建议下一步，但裁决权始终属于确定性规则。

## 文档

- [产品定义](docs/00-product-brief.md)
- [证据与实验模型](docs/01-evidence-model.md)
- [架构与安全边界](docs/02-architecture.md)
- [验收标准](docs/03-acceptance.md)
- [M0 纵向切片](docs/04-m0-vertical-slice.md)
- [M1 资源与环境预检](docs/05-m1-resource-preflight.md)
- [M2 真实浏览器证据（FROZEN）](docs/06-m2-browser-evidence.md)
- [M3 Vue 证据工作台（FROZEN）](docs/07-m3-vue-workbench.md)

## 项目来源

验迹的方法论来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、
固定种子复现偶发故障、在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是
重要参考案例，但验迹不会把任何电商服务、中间件或业务状态机硬编码为产品前提。

## License

[Apache License 2.0](LICENSE)
