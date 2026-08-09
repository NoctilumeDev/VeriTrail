# 08. M4 本地 Run 目录与轻量自举

## 状态与认识边界

`AUTOMATED（实现、自动化与候选真实运行已通过；最终冻结待干净提交复跑）`。M0–M3 已分别达到
`FROZEN`。本文件前半部分保留 M4 实现前预注册的问题、候选架构、控制变量、证伪条件和退出
门槛；文末候选运行记录只报告已经取得的事实，不回写或降低原合同标准。

真正判断来自实现后的自动化、真实数据库负路径、真实回环服务、真实浏览器、自举复跑、
资源与清理证据。如果运行事实反驳本合同中的候选设计，必须保留原合同与失败 Run，创建新的
合同版本说明修正原因；不得修改旧标准、删除反例或把 `IMPLEMENTED` 写成 `FROZEN`。

## 目标问题

M4 只回答：

> VeriTrail 能否在不改变原始证据包、不把 SQLite 升格为事实来源、也不引入任意命令执行的
> 前提下，把多个不可变 Run 建立为可重建的本地目录，通过只读同源回环 API 让现有工作台
> 发现并选择 Run，并最终索引和展示一份针对 VeriTrail 自身工作台生成的真实验收证据包？

这是一条用户可见的纵向能力，不按技术层拆成“只建表”“只写 API”“只做列表”三个孤立里程碑：

```text
不可变 Bundle
  -> 有界校验与目录快照
  -> SQLite 派生索引
  -> 只读回环 API
  -> Workbench Run 目录与 M3 详情
  -> VeriTrail 自身验收 Run 被再次索引和读取
```

SQLite、API 和 Vue 是同一条能力链的组成部分，不是三个实验主要变量。任一环节缺失时，M4
只能报告实际阶段，不能用数据库测试、HTTP 200 或页面截图单独宣称闭环。

## 待验证假设与可证伪结论

M4 预注册以下假设，运行后允许被否定：

1. 一个停止服务后构建、启动服务后只读的 SQLite 快照，足以避免 M4 过早引入在线写并发；
2. Bundle 仍作为唯一事实来源，SQLite 只保存重建所需的派生元数据，不会制造第二套 Verdict；
3. 固定回环、同源、只读 API 足以让工作台发现多个 Run，同时不扩大到通用文件服务器；
4. “构建目录 -> 启动工作台 -> 生成自验收 Run -> 重建目录 -> 再读取”的两阶段流程可以形成
   第一次轻量自举证据，而不需要 M4 执行项目命令；
5. 在 16 GB Windows 主机上，一个 Python 进程、一个只读 SQLite 连接集合、一个 Vue 生产构建
   和一个串行 Chromium 足以完成验收且不突破资源停止线。

只要出现以下任一事实，相应假设即被反证或需要降级为 `INCONCLUSIVE`：目录快照无法从 Bundle
重建；同一 Run 冲突时任意选择一个版本；源文件改变后 API 仍返回旧可信内容；UI 与源 Report
状态不一致；API 能越过声明根目录；本地文件被上传或外部来源读取；自举 Run 需要手工改报告；
资源、端口或数据库侧车残留污染下一轮。

## 影响层级、所有者与消费者

- 声明层级：`L2_CONTRACT`；新增版本化本地 HTTP API 和 SQLite 内部 Schema，工作台增加新的
  数据入口，但不改变 M0–M3 的 Report/Evidence/Plan 公共契约；
- 所有者：Python Catalog / Local Read-only API / Vue Workbench；
- 数据所有权：Bundle Artifact Store 是权威事实；Catalog 是可删除、可重建的派生索引；
- 写入者：离线 `catalog-build`；服务运行期间没有数据库或 Artifact 写入者；
- 读取者：`catalog-serve`、Vue Run Catalog、M3 Bundle Loader 和 M4 验收工具；
- 公共消费者：Workbench、浏览器自举计划、API 契约测试、未来跨 Run 比较；
- 保持不变：ExperimentPlan 0.1–0.3、Evidence/Report/Manifest 0.1、Verdict 优先级、M0–M3 CLI
  行为、既有 Plan 哈希、M3 本地目录入口与静态演示模式。

实际 diff 若修改现有 Schema、裁决规则、证据生成语义、M2 浏览器采集或任意命令执行边界，
必须停止 M4 并升级消费者矩阵；不能以“目录需要更多字段”为由顺手回写冻结生产者。

## 控制变量设计

M4 目录一致性实验使用一个主要变量：

```text
PRIMARY: catalog_bundle_set_state =
  empty
  | valid_single
  | valid_multiple
  | duplicate_identical
  | duplicate_conflicting
  | corrupt
  | missing_after_index
```

以下保持受控：同一代码提交、Catalog Schema/API 版本、Bundle 校验器、工作台构建物、Artifact
根目录规则、SQLite 参数、端口、浏览器版本、视口、排序、步骤、资源预算和自举 Plan。每次只
切换整个确定性 Bundle 集合状态；数据库、API 和页面随同一输入链路工作，不能在正/负组使用
不同规则或手工修补索引。

`empty` 是有效的空目录状态，不等于 Run `PENDING`；`duplicate_conflicting`、`corrupt` 和
`missing_after_index` 是 Catalog 诊断，不得改写源 Run 的 ExecutionStatus 或 Verdict。目录状态、
服务状态与 Run 裁决在 API 和 UI 中必须使用不同字段和视觉标签。

## M4 纵向边界

### 必须包含

1. 新增标准库优先的 `catalog-build`：只扫描用户显式给定 Artifact 根目录的直接子目录，验证
   Bundle 清单、路径、大小、SHA-256、版本与交叉引用，生成新的目录快照并拒绝覆盖已有输出；
2. 每个输出是独立目录，至少包含 `catalog.sqlite3` 与 `catalog-manifest.json`；先在同父目录的
   有界 staging 中完成，再原子发布，失败清理 staging，不留下半成品；
3. SQLite 保存 Catalog 版本、Run 摘要、Bundle 摘要、相对定位和目录问题；不复制 Evidence
   正文、截图、Markdown、认证材料或最终裁决规则；
4. 新增固定绑定 `127.0.0.1` 的 `catalog-serve`，同时提供 Vue 生产构建和只读版本化 API；
   服务只接受 `GET`/`HEAD`，不提供导入、刷新、删除、重裁决或任意文件浏览；
5. Workbench 在 Catalog API 存在时显示确定性排序的 Run 目录，允许选择 Run 后复用 M3
   Bundle Loader 完整校验和详情视图；API 缺席时 M3 演示包与本地目录入口继续工作；
6. 相同 Run ID 与相同 Bundle 摘要重复出现时幂等归并并记录重复数；相同 Run ID 对应不同摘要
   时形成冲突问题，不能任意选择赢家或覆盖旧事实；
7. Bundle 在索引后丢失、改变或哈希不符时，文件接口拒绝返回旧可信内容，UI 显示独立 Catalog
   错误，不复用上一次 Run 的状态卡；
8. 创建一份冻结的 M4 自举 Plan：真实 Chromium 验收 Catalog 工作台并生成标准 VeriTrail
   Bundle；随后停止服务、重建新目录快照、再启动并从 UI 读取该自举 Run；
9. 桌面与移动端完成空目录、多个 Run、正/负 Run、目录问题、API 不可用、选择、返回/刷新和
   错误恢复；检查 Console、Network、同源资源、焦点、横向溢出和非颜色状态；
10. 所有索引、服务、浏览器和数据库步骤遵守 M1 预检与 16 GB 串行/受限微并行策略。

### 明确不做

- 在线目录刷新、文件监视器、后台轮询、WebSocket、SSE 或运行中 SQLite 写入；
- POST/PUT/PATCH/DELETE API、浏览器上传、拖拽导入、删除/移动 Artifact 或修改源 Bundle；
- 计划编辑、Seal、Preflight、Browser Capture 或被测项目生命周期按钮；
- 任意 Shell、可执行文件/参数编排、Docker、账号、权限、远程访问、云同步或多用户协作；
- 跨 Run 差异算法、基线自动选择、趋势图、全文搜索、标签系统或报告发布；
- 把 Catalog 错误映射成 Run `FAIL/PENDING/INCONCLUSIVE`，或在 UI/API 中重新计算 Verdict；
- 实时并发写、多个 Catalog 进程争锁、网络文件系统和生产容量声明。

## Artifact 与 Catalog 权威边界

```text
Bundle JSON / Evidence / attachments  = 权威、不可变、可独立验证
catalog.sqlite3                       = 派生、可删除、可重建、只读服务
catalog-manifest.json                 = 目录快照自身的版本、摘要和构建事实
Vue Catalog                           = 目录与源 Bundle 的只读消费者
```

- Catalog 构建不能修改、补齐、规范化写回或移动输入 Bundle；
- 扫描只接受根目录内的普通直接子目录和普通文件；符号链接、junction、reparse point、硬链接
  混淆或解析后越过根目录的候选必须拒绝或记录稳定问题，不能跟随到其他位置；
- 数据库不能成为 Report、Verdict、Assertion 或 Evidence 的新生产者；
- Run 列表中的摘要字段必须来自已验证 Report，并在打开详情后与 M3 全量校验结果交叉一致；
- Bundle 身份摘要候选算法固定为：对 `schema_version`、`run_id` 与按路径排序后的
  `{path, sha256, size}` 列表生成规范 JSON，再计算 SHA-256；不能用目录名、文件时间、原始 JSON
  排版或数据库行号判断是否相同；
- 删除数据库并从同一受控 Bundle 集合重建，逻辑行、排序、问题代码和 Catalog 摘要必须确定性
  一致；仅允许构建时间等预先声明的非决定字段不同；
- 数据库损坏、版本未知或 Manifest/数据库哈希不一致时，服务拒绝启动，不以空目录掩盖错误；
- Catalog 输出默认位于 Git 忽略目录，不作为证据包或公开发布物提交。

## SQLite 快照合同

候选内部 Schema 版本为 `Catalog SQLite 0.1`，至少包含：

- `catalog_meta`：Schema 版本、Catalog ID、确定性 Bundle 集合摘要、构建工具版本；
- `catalog_runs`：不透明 Catalog Run ID、Run ID、创建时间、ExecutionStatus、Verdict、Plan
  ID/版本/哈希、Bundle 摘要、文件数、总字节、重复数和本地相对定位；
- `catalog_issues`：稳定问题代码、候选不透明 ID、Run ID（仅当已安全解析）、冲突摘要与计数；
- 必要唯一键、检查约束和索引。

约束：

- 服务以 SQLite URI 只读模式打开冻结数据库，禁止自动迁移和创建 journal/WAL 侧车；
- 每个请求使用有界读取连接或串行共享策略，不能跨线程误用写连接；
- API 不返回数据库路径、Artifact 根绝对路径、相对目录名、SQLite 行号或 SQL 错误文本；
- 数据库不保存公网 IP、账号、邮箱、令牌、Cookie、请求头、`.env` 值或个人绝对路径；
- 相对定位只在本地数据库内用于受控根目录解析，不进入 Catalog API、导出报告或日志；
- 构建上限初值：最多检查 1000 个直接子目录，每 Bundle 沿用 M3 的 256 文件、单文件 10 MiB、
  整包 64 MiB 上限；哈希按文件串行流式计算，不能一次把全部 Bundle 读入内存。

Catalog 构建状态独立于 Run 状态：`COMPLETED` 表示候选均有效或根为空；
`COMPLETED_WITH_ISSUES` 表示有效 Run 已形成快照，但损坏、冲突或不安全候选被隔离并记录；
`ERROR` 表示无法发布完整快照且不能留下输出。前两者代表命令成功并返回 0，但结构化 stdout
必须包含状态与问题数；已知校验/安全错误沿用退出码 2，未预期内部错误返回 1，二者都只输出
稳定错误码和脱敏消息，不回显堆栈。三种构建状态都不得映射为任何 Run Verdict，观察结果后
不能临时更换退出语义。

这些表名与限额仍是候选实现假设；若运行证明不够或不安全，需要新合同版本，不能静默漂移。

## 本地只读 API 0.1

候选端点：

```text
GET  /api/v1/health
HEAD /api/v1/health
GET  /api/v1/catalog
HEAD /api/v1/catalog
GET  /api/v1/runs/{catalog_run_id}/bundle/{bundle_relative_path}
HEAD /api/v1/runs/{catalog_run_id}/bundle/{bundle_relative_path}
```

最低契约：

- `/api/v1/health` 只返回服务/API/Catalog 版本、Catalog ID 和只读状态，不返回机器身份或路径；
- `/api/v1/catalog` 返回确定性排序的 Run 摘要、问题摘要和有界分页信息；默认页不超过 50，
  单页硬上限 100，未知参数与越界值返回结构化 400；
- `catalog_run_id` 是 Catalog 生成的不透明稳定标识，不直接使用目录路径；Bundle 路径继续经过
  与清单一致的规范化和允许列表检查；
- 文件接口只服务该 Run 清单中声明、当前读取时大小与 SHA-256 仍匹配的文件；不提供目录列表、
  Range、任意绝对路径、符号链接目标或清单外文件；
- 静态 Workbench 也只从显式生产构建根目录提供普通文件，拒绝路径穿越、符号链接和任意目录
  浏览；SPA fallback 不能吞掉 `/api/` 错误并伪装成 HTML 200；
- API 错误使用稳定代码，例如 `CATALOG_VERSION_UNSUPPORTED`、`RUN_NOT_FOUND`、
  `BUNDLE_UNAVAILABLE`、`BUNDLE_CHANGED`、`UNSAFE_PATH`，不回显本地路径或异常堆栈；
- 只绑定 IPv4 loopback `127.0.0.1`；Host 只接受显式回环主机与当前端口，拒绝 DNS rebinding
  形态；不发送允许跨源读取的 CORS 响应头；
- JSON 与静态资源设置 `X-Content-Type-Options: nosniff`、有界正文、明确 Content-Type 和
  `Cache-Control: no-store`；页面使用同源 CSP，不允许远程脚本、字体、图片或连接；
- 非 GET/HEAD 返回 405；畸形请求、慢请求、超长路径和并发连接必须有上限与超时；
- 服务启动前验证 Catalog Manifest、数据库 SHA-256、Schema 版本和 Artifact 根绑定；验证失败
  时不监听端口或立即清理退出。

API 的精确 JSON Schema 应在实现提交中版本化并由 Python、Vue 和真实 HTTP 契约测试共同消费。

## Workbench 增量合同

M4 在 M3“证据院落”前增加最小 Run 门厅，不重做详情页：

1. Catalog 不存在：保持 M3 正/负/损坏夹具和本地目录入口；
2. Catalog 为空：显示“目录有效但暂无 Run”，不显示 `PENDING` Verdict；
3. Catalog 有数据：按 `created_at DESC, run_id ASC, catalog_run_id ASC` 稳定排序，显示 Run ID、
   运行状态、裁决、Plan、时间、完整性摘要和重复数；
4. 选择 Run：URL 只保存不透明 `catalog_run_id`，通过固定同源 API 路径加载，仍由 M3 Loader
   逐文件校验；
5. Catalog 问题：单独区域显示问题代码和安全解释，不与断言失败、Run Verdict 或 M3
   完整性状态混为一谈；
6. API 中断、未知 Run、Bundle 改变：清空当前不可信详情，保留可恢复导航与重试，不回退到
   上一个 Run 冒充成功；
7. 浏览器返回/前进、刷新和移动端状态可理解；键盘可以从目录进入详情并回到原 Run 卡片；
8. 不引入远程字体、图标库、装饰图片、路由/状态库或第二套主题系统，继续复用 Palace
   Evidence 令牌和朱红语义边界。

## 轻量自举定义

M4 的“自举”只表示 VeriTrail 能读取自己产生的一份验收 Bundle，不表示完整 v0 自动执行：

1. 用冻结 M4 代码和固定脱敏种子 Bundle 构建 Catalog A；
2. 启动只读服务 A，使用 VeriTrail M2 `browser-capture` 执行冻结的 M4 自举 Plan；
3. 得到标准 `runtime.preflight + browser.session + report + manifests + screenshots` Bundle B；
4. 停止服务 A 并确认端口释放；
5. 用原种子 Bundle 加 Bundle B 构建新的 Catalog B，不能原地修改 Catalog A；
6. 启动只读服务 B，从 Catalog UI 找到 Bundle B，打开并核对其 ExecutionStatus、Verdict、
   Plan 哈希、浏览器事实和清理证据；
7. 再次停止服务并核对数据库、端口、浏览器和 staging 残留。

如果 Bundle B 需要手工编辑、复制 UI 自算的 Verdict、跳过哈希、修改自举 Plan 标准或由服务
运行中写入数据库，不能称为自举通过。

## 自动化验收矩阵

- Catalog 构建：空根、单 Run、多 Run、稳定排序、确定性重建、拒绝覆盖和 staging 清理；
- Bundle 验证：未知版本、非法/重复/缺失路径、绝对路径、反斜杠/NUL、大小/数量超限、哈希
  不符、跨 Manifest 引用不一致和受支持附件；
- 幂等与冲突：同 ID 同摘要归并且重复数稳定，同 ID 不同摘要隔离且无任意赢家；
- SQLite：Schema/约束/查询计划、数据库损坏、未知版本、Manifest 哈希不符、只读打开、无
  journal/WAL/SHM 残留和从同一输入确定性重建；
- API：健康、分页、稳定顺序、404/405、未知参数、Host 拒绝、无 CORS、路径穿越、符号链接、
  源文件删除/改变、内容类型、安全头、正文/连接/超时上限；
- Workbench：API 缺席兼容、空目录、多 Run 选择、正负裁决分离、问题区、未知/变化 Run、重试、
  历史导航、焦点归还、桌面/移动和零横向溢出；
- 兼容：M0–M3 Python 56 项、M3 前端 28 项、既有 Plan/Bundle 哈希与静态演示行为全部保持；
- 资源：Python 和前端测试串行或 worker 不超过 2；Catalog 构建逐 Bundle、逐文件串行；
- 安全：敏感扫描、无绝对路径 API/日志、无源 Bundle 修改、无外部请求、无任意命令执行。

自动化只能推进到 `AUTOMATED`，不能替代下面的真实运行。

## 真实运行退出条件

在干净的代码提交和当前 16 GB Windows 主机上串行执行：

1. 运行 M1 预检并记录可用内存、磁盘、采集器开销与计划端口；不使用 Docker；
2. 用真实 M2 正/负 Bundle 构建 Catalog，逐字节核对输入未改变、数据库 Manifest 与重建摘要；
3. 运行空、重复相同、冲突、损坏、索引后删除/改变、数据库损坏和端口占用负路径，证明无
   静默覆盖、旧内容回放或半成品目录；
4. 启动单个回环只读服务，用真实 HTTP 检查全部端点、Host、方法、安全头、分页、路径与同源；
5. 使用真实 Chromium 完成 Catalog 空/多 Run/正负/问题/失败重试/历史、本地目录兼容、桌面
   与移动链路；检查 Console、Network、4xx/5xx 解释、焦点、截图和横向溢出；
6. 使用 Codex 内置浏览器重复用户可见主链，检查 F12 Console/Network、请求方法/来源/状态、
   外部请求、移动视口和 API 中断后的恢复；
7. 按轻量自举七步生成、重建并读回 VeriTrail 自身 Bundle，逐字段和哈希追溯到冻结 Plan；
8. Python 3.10/3.13、前端自动化、API 契约、SQLite 与 M0–M3 兼容回归全部通过；
9. 完成敏感扫描，确认数据库/API/日志/报告没有个人绝对路径、账号、凭据、公网 IP 或原始
   敏感证据，Catalog 输出继续被 Git 忽略；
10. 结束后服务、浏览器、端口、SQLite 连接、journal/WAL/SHM、staging 和对象 URL 均释放；
    Git 工作区只包含预期提交，冻结提交与 `m4-v0.5.0` 标签可从 GitHub 读回。

只有全部成立，M4 才能从 `PLANNED` 依次推进到 `IMPLEMENTED`、`AUTOMATED`、
`RUNTIME_VALIDATED` 和 `FROZEN`。若某个候选架构假设失败，报告真实结果并回到合同版本设计；
不能因为页面可用、SQLite 有数据或自举脚本跑完就跳过一致性与安全反证。

## 候选实现与运行记录（2026-08-09）

- 实现版本：Python Core / Workbench `0.5.0.dev1` / `0.5.0-dev.1`；新增
  `catalog-build`、`catalog-serve`、Catalog SQLite 0.1、Local Read-only API 0.1、
  `schemas/catalog-api-0.1.schema.json` 与 Workbench Run 门厅；
- 自动化候选：Python 73 项与前端 33 项通过；Catalog 覆盖空根、单/多 Run、确定性重建、
  同摘要归并、冲突隔离、损坏/不安全路径/硬链接、只读 SQLite、数据库/Manifest 篡改、Host、
  方法、分页、Range、路径穿越、源丢失/变化、安全头、无 CORS 与 staging/sidecar 清理；
- Catalog A：两份冻结 M2 正/负 Bundle，2 Runs、0 issues、集合摘要
  `f93386e3d4c962e471584af1eba4cd12a928206452bcd55046d3af81323abbbb`；
- 自举 Plan v1：哈希 `c5a1cb7beab09cf573343dec690f33d572639c50b56d3f7d60f4a4d1fabade2e`；
  真实浏览器链到达详情，但 PASS 选择器同时匹配目录卡片与详情状态门，严格模式失败。该失败
  Run 保留，没有覆盖或改写为通过；
- 自举 Plan v2：唯一变更为把 PASS 选择器收窄到详情状态门；哈希
  `d3a8cd4e1d7405e91fd7b0cdac0eef94772b09617a19d3dffcd473d8a05e3a08`。真实 Chromium 返回
  `COMPLETED / PASS`，2 视口、2 截图、26 个 GET 200、0 Console/Page/Network/HTTP/重复写/
  横向溢出异常，并完成浏览器清理；
- Catalog B：两份种子加自举 Bundle B，3 Runs、0 issues、集合摘要
  `2c1f9fffd6b251953abcb04e9c548a22df3bd0199f0b5e85136201fa89ea0160`；Workbench 成功读回
  Bundle B 的 Run 状态、Verdict、Plan v2 哈希与浏览器事实；
- 控制组实跑：`empty` 为有效空目录；`duplicate_identical` 归并为 1 Run/1 重复；
  `duplicate_conflicting + corrupt` 形成 2 个独立 Catalog issues 且 0 Run，不选择赢家；
  `missing_after_index`/同尺寸内容变化由 API/UI 报 `BUNDLE_UNAVAILABLE`/`BUNDLE_CHANGED`，
  清空旧状态，源恢复后显式重试成功；
- 真实 Workbench 验收脚本完成 7 组检查、56 个只读同源请求、0 HTTP/外部/写请求，桌面与移动端
  均无横向溢出，端口与 SQLite sidecar 清理完成；Codex 内置浏览器另行完成正/负 Run、空目录、
  问题区、历史、焦点、API 中断/恢复和源变化/恢复链路，页面 Console 无未解释异常；
- 当前认识边界：以上仍是工作树候选证据。只有实现提交后重新跑完双 Python、生产构建、真实
  Chromium、内置浏览器、敏感扫描、端口/进程/staging/SQLite sidecar 与 Git 清洁检查，才能
  把本节状态改为 `RUNTIME_VALIDATED / FROZEN` 并创建 `m4-v0.5.0`。

## 计划冻结记录

- 前置冻结基线：M3 `e46f63308a95d3091492268b65020e1e052d70ff`（tag `m3-v0.4.0`）；
- 代码基线：M3 实现 `ef2a8d64f781ba61bf7fbd9c1511a3419a6cfbaa`；
- 计划版本：M4 Local Run Catalog Contract 0.1；
- 候选内部存储：Catalog SQLite 0.1；
- 候选公共接口：Local Read-only API 0.1；
- 当前里程碑状态：`AUTOMATED`；
- 合同提交：由首次将本文件与 M4 状态说明合并到 `main` 的独立提交固定；
- 合同冻结时未产生的结论：实现正确性、数据库一致性、API 安全性、资源适用性和轻量自举；
  当前候选结果记录在上一节，但尚未成为冻结基线。
