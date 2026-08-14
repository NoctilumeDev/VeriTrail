# M11 真实项目候选适配性与合同形成记录

> 状态：`PLANNED / HISTORICAL_PROBES / SUPERSEDED_BY_CONTRACT_0.2 / IMPLEMENTATION_NOT_STARTED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`（候选盘点、已清理探索探针与合同规划；不修改代码、Schema 或目标仓库）
> 前置地基：`m10-v0.11.1` @ `f4efdd25c50b19077c61994bce3e2aca5244d5ec`
> 后继合同：[文档 23 Contract 0.2](23-m11-single-node-real-project-contract.md)

## 1. 本阶段只回答一个问题

> 能否在不扭曲被测项目真实拓扑、不为候选硬编码 Core、也不越过 16 GB 宿主机边界的前提下，
> 选择并预注册一个不同于 VeriTrail fixture 的真实项目，完成 M11 代表性全链路？

本文件登记候选、能力差距和已经清理的非验收探针，不授权实现。用户随后确认 `OPTION_B`、
InkNarratives 精确 ref、Gate A -> Gate B 严格串行和不适用项；可执行边界已进入文档 23 Contract
0.2。本文件保留当时的探索与决策历史，不再充当当前合同，也不能被引用为运行验收事实。

## 2. 当前 M10 可消费边界

M10 ProjectProfile 0.1 固定为 Windows 11 / `C1 PROCESS_COLD` / 宿主机可信本地进程，并要求：

- 恰好一个 `DEPENDENCY` 与一个 `APPLICATION`；
- 两个节点各有独立回环端口和 owned HTTP readiness；
- 启动顺序固定 dependency -> application，清理顺序严格相反；
- application 是唯一 Browser origin；
- 不支持零依赖、三节点以上、Docker、C2/C3、包管理器生命周期或跨平台；
- 只能使用已冻结能力验证真实项目，不能在 M11 中为目标临时改写 Profile、Evidence 或 Verdict。

M11 不是“随便找一个仓库跑一下”。候选的真实最小拓扑必须天然落在上述边界内，或先触发独立的
通用能力合同。若需要扩展节点图、静态单节点或 Docker 适配，必须把该变化作为单独主要变量验收，
不能同时声称已经证明了真实项目功能全链路。

## 3. 只读候选盘点

盘点只读取仓库、文档、构建声明和远端引用；没有读取 `.env`，也没有启动 Docker、数据库、Maven、
Node 服务或浏览器目标。

| Candidate | Frozen/read-back ref | Real minimum shape | Browser/business value | Current fit |
| --- | --- | --- | --- | --- |
| DarkRoomLibrary | `v1.2.5` @ `718c1f3` | MySQL -> Spring Boot API -> Vue；完整 Compose 另含 Redis、RabbitMQ，共五服务 | 六身份、借阅/预约/采购/治理、真实数据库与降级边界，代表性强 | `BLOCKED_BY_TOPOLOGY_AND_READINESS`：至少三节点，MySQL 不是 HTTP readiness，Docker 形态又超出 M10；不能把 MySQL 当作外部预热服务后仍宣称 C1 冷自举 |
| InkNarratives | `main` @ `b443a1c`，无冻结标签 | 单个静态 HTTP 目标，五个零依赖 HTML | 真实响应式、滚动、键盘、减少动效与内容展示，浏览器价值明确 | `BLOCKED_BY_TOPOLOGY`：零依赖单节点，不符合恰好两节点；人为增加假 dependency 会污染实验 |
| PlainJournal | `v1.0.7` @ `9cd0b83` | 多服务、多个中间件与前后端组合 | 分布式一致性和故障恢复价值最高 | `DEFERRED_RESOURCE_AND_SCOPE`：明显超出 M10 拓扑与 16 GB 首个 M11 样本预算，保留为后续高强度案例 |

当前结论不是“三个候选都不行”，而是：**三个现有可运行外部候选中，没有一个可以在保持真实最小
拓扑的同时，直接装入 M10 恰好两节点合同。** 这是有价值的系统事实，不能通过增加假依赖、隐藏
数据库或选择在线 Mock 演示来消除。

## 4. 目标选择规则

独立 M11 合同冻结前，候选必须全部满足：

1. 引用可寻址且已从远端读回的目标提交或标签；目标仓库工作区必须干净；
2. 使用目标项目自身文档认可的最小真实运行形态，不另造只为 VeriTrail 服务的启动分支；
3. 明确一个主要变量；工具版本、目标代码、数据集、端口、身份、浏览器步骤和资源预算均冻结；
4. 至少有一个无需读取或持久化秘密的用户可见业务链，且能定义可重复成功、业务失败和恢复事实；
5. 所有必要进程都能被当前 Run 创建、观测并逆序清理；既有原生服务不能被静默接管；
6. 浏览器入口必须来自真实运行目标，不得用 GitHub Pages、demo adapter 或 Mock 替代真实后端结论；
7. 16 GB 预算允许严格串行重复、失败恢复和最终清理；资源不足时保持 `PENDING`；
8. 目标选择在运行前封存；失败后不得换成更容易通过的项目。

## 5. 当时决策门与拟选项（历史）

在合同确认前，M11 保持 `PLANNED`，当时三条候选路径的架构判断如下：

- `OPTION_A`：先独立扩展 ProjectProfile 为通用有向无环多节点本地进程拓扑，再另行验证版本化的
  非 HTTP readiness 与数据库进程/数据所有权；两项不能在同一实验中引入。全部前置能力分别冻结后，
  才能选择 DarkRoomLibrary 的真实三节点最小形态；
- `OPTION_B`（`TARGET_PROPOSED`）：增加真实零依赖单节点 Profile 形态并独立冻结，再用
  InkNarratives 证明不同类型项目；
- `OPTION_C`：建立一个天然符合 dependency -> application 的独立真实小项目，但它必须有自身产品
  价值和用户链，不能成为专为让 VeriTrail 通过而制作的第二个 fixture。

这三个选项不能在同一实验中并行引入。选择顺序以“对通用模型的必要性、真实项目代表性、新增爆炸
半径、16 GB 可重复验收成本”评分，而不是以实现快慢决定。DarkRoomLibrary 的外部效度最强，但
前置能力不止一个；InkNarratives 的能力增量最小，却只能证明静态项目、浏览器与单节点生命周期，
不能被包装成动态后端或数据库链路。基于当时已完成探针，只提出 `OPTION_B`，`OPTION_A/C` 延后；
该拟选结果后来已由用户确认并进入文档 23 Contract 0.2，但实现仍未开始。

## 6. 后继合同已补齐的门禁

- [x] 用户确认唯一主目标、精确 ref 与其余候选的延后边界；
- [x] 单节点 Profile/Schema 作为 Gate A 独立主要变量，并列出生产者与消费者；
- [x] 成功、业务失败、基础设施失败、恢复和状态归因已冻结；
- [x] 自动 Browser、Codex 内置浏览器补充验收和 Workbench 读回边界已分开；
- [x] 不适用的写业务、数据库、中间件、多角色与一致性语义已明确；
- [x] 工具、端口、Subject、资源停止线和清理责任已冻结；
- [x] 只使用具有真实复跑语义的 Comparison；Paired/Batch 保持不适用；
- [x] 失败保留、Run ID、复跑、远端读回和未来标签规则已进入文档 23。

以上勾选是后继合同事实，不是实现或运行事实；M11 继续保持 `PLANNED`。

## 7. 预注册探索探针：InkNarratives 仓库根目录

> 探针编号：`M11-FEASIBILITY-INK-ROOT-001`
> 状态：`PREREGISTERED / EXPLORATORY / NON_ACCEPTANCE`
> 目标引用：`InkNarratives main @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 工具引用：`VeriTrail m10-v0.11.1 @ f4efdd25c50b19077c61994bce3e2aca5244d5ec`

本探针只回答：**冻结的 M5 `STATIC_HTTP` 快照入口能否直接接受 InkNarratives 的真实仓库根目录，
且无需修改 VeriTrail Core、Schema 或 InkNarratives？** 它不是 M11 合同、验收、目标选择或冻结依据。

运行边界固定如下：

1. 使用 `examples/orchestration/plan.json` 的 Plan 0.4 作为只读投影，仅把 `target.root` 改为 `.`；
2. 以 InkNarratives 原始仓库根目录作为 `subject_root`，不排除 `.git`、文档、脚本或许可证；
3. 只调用冻结的 `prepare_static_target()` 做路径与静态快照准入检查，不启动 HTTP 服务、Chromium
   或任何目标进程；
4. 不修改两个仓库，不创建适配目录，不复制/重命名五个 HTML，也不补造 `index.html`；
5. 完整保留首次返回结果；失败后不得通过改变根目录、忽略规则或预处理文件重跑同一探针；
6. 允许的预期拒绝事实包括隐藏路径、无 `index.html`、不受支持的静态文件类型；实际首先命中哪条
   由冻结实现和原始目录顺序决定，不能事后改写成另一条；
7. 若意外通过，只能说明快照准入成立，仍不能推出浏览器链路、内容完整性或 M11 验收成立。

判定规则：

- `ACCEPTED_DIRECT_ROOT`：冻结 M5 接受未经处理的仓库根目录；
- `REJECTED_DIRECT_ROOT`：冻结 M5 返回确定性准入错误；必须原样记录首个错误；
- `PROBE_INVALID`：目标 ref、工具 ref 或工作区状态与预注册不一致，或执行过程修改了任一仓库。

任何结果都不授权立即改造 InkNarratives。若直接根目录被拒绝，下一步必须独立判断“目标自有的静态
发布根”是否对 InkNarratives 本身成立，不能把 VeriTrail 专用适配包装成真实项目能力。

### 7.1 运行事实（2026-08-14T09:35:28+08:00）

预注册提交先于探针结果创建：`4f6e6b1 docs(m11): preregister Ink root feasibility probe`。有效调用前
只读核对结果为：

- VeriTrail 与 InkNarratives 工作区均干净；
- InkNarratives `HEAD` 精确等于 `b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`；
- `m10-v0.11.1^{}` 精确等于 `f4efdd25c50b19077c61994bce3e2aca5244d5ec`；
- 当前 `src/veritrail/orchestration.py` 与 `examples/orchestration/plan.json` 相对该标签无差异。

第一次临时调用在导入阶段返回 `ModuleNotFoundError: No module named 'veritrail'`，原因是仓库采用
`src/` 布局而临时解释器未设置模块搜索路径；它没有进入 `prepare_static_target()`，因此登记为夹具
失败，不作为目标准入结果。随后只补充 `PYTHONPATH=<VeriTrail>/src`，未改变 Plan、目标或判定规则。

有效探针使用 Python 3.10.6，首次目标返回原文为：

```json
{"classification":"REJECTED_DIRECT_ROOT","errors":["target contains a hidden or control-character path"],"probe_id":"M11-FEASIBILITY-INK-ROOT-001","python":"3.10.6"}
```

因此本探针事实判定为 `REJECTED_DIRECT_ROOT`。冻结 M5 对原始仓库根目录执行 fail-fast 扫描时，首先
被隐藏路径（仓库中的 `.git`/`.github` 类路径）阻断；它没有继续到 `index.html` 或文件后缀检查，
所以本次运行**不能**把那些静态观察提升为同一探针的运行错误。

运行后两个仓库仍无目标代码变化，未启动 HTTP、Chromium 或目标进程，也没有创建适配目录。该探针
本身没有选择目标或授权实现；“冻结 M5 可直接验收 InkNarratives 原始仓库根目录”的假设已被真实
运行否定。当前 M11 总状态以页首和第 8 节为准。

### 7.2 目标自有发布根复核

对目标精确提交执行 `git ls-tree -r --name-only b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
确认：版本树只有五个仓库根级独立 HTML、仓库治理文件、`docs/`、`scripts/` 与 GitHub workflow；不存在
`index.html`、统一展厅或独立静态发布目录。目标 README 也明确声明“当前没有统一入口页”，并把稳定
英文目录、统一入口和 Pages 放在视觉与文章骨架稳定之后。

补充运行 `D:\Node.js\node-v24.14.0-win-x64\node.exe scripts\verify-repository.mjs`，Node
v24.14.0 返回：`Repository verification passed: 5 standalone HTML demos.`。该结果证明目标自己的五页
仓库基线通过，不改变 M5 的准入拒绝，也不是 VeriTrail Bundle 或 M11 结论。

因此当前 ref 没有可直接复用的目标自有发布根。此时仅为 VeriTrail 新建 `index.html`、复制选择文件
或增加发布目录，会提前改变 InkNarratives 已声明的产品路线，属于目标扭曲而非中性适配。`OPTION_B`
若继续，必须先成为独立、通用的 Profile 能力实验；它不能以当前 InkNarratives ref 作为“已经存在
发布根”的事实前提。

### 7.3 预注册探索探针：原始目录的单节点静态 HTTP 运行形态

> 探针编号：`M11-FEASIBILITY-INK-SINGLE-NODE-002`
> 状态：`PREREGISTERED / EXPLORATORY / NON_ACCEPTANCE`
> 目标引用：`InkNarratives main @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 工具引用：Python 3.10.6，标准库 `http.server`
> 固定端口：`127.0.0.1:18773`

这个探针只检验一项更窄的事实：在 InkNarratives README 已允许的“任意静态文件服务器”运行形态中，
原始仓库目录能否作为**一个** loopback HTTP 应用节点服务五个现有页面。它不调用或修改 VeriTrail
Core，不生成 Bundle，不证明 ProjectProfile 已支持单节点，也不构成 M11 用户链、验收或冻结。

预注册边界：

1. 只在目标 `HEAD`、VeriTrail 工作区与端口均通过运行前核验时执行；
2. 由 Python 3.10.6 以 `-m http.server`、回环 bind 和 InkNarratives 原始目录启动一个临时只读服务；
   不创建入口页、发布目录、依赖安装、数据文件或项目配置；
3. 精确请求并预期 HTTP 200 的页面是 `暗室.html`、`柳永.html`、`苏轼.html`、`王维.html` 与
   `长卷.html`；目录 listing、Git 路径可访问性、统一入口和远程部署均不属于该探针；
4. 对 `苏轼.html` 执行一次真实 Chromium 桌面和移动加载，检查页面可见、根视口横向溢出、Console
   与 Network 中未解释的加载错误；不把单页结果外推为五页完整可访问性或内容验收；
5. 结束时只终止本探针创建且 PID 一致的 Python 进程，并核验端口释放；若所有权、端口或清理不成立，
   记录 `PROBE_INVALID`，不尝试接管或终止外部进程。

判定规则：

- `SINGLE_NODE_TRANSPORT_OBSERVED`：五页均由原始目录的临时 loopback 服务返回预期状态，且代表性
  浏览器加载与 owned cleanup 均成立；
- `SINGLE_NODE_TRANSPORT_REJECTED`：目标服务、路由或浏览器事实未满足预注册条件；
- `PROBE_INVALID`：运行前提、进程所有权、端口所有权或清理前提无法核验。

即使获得第一种结果，它也只证明一个未来通用单节点 Profile 值得独立立项；它不改变 M10 两节点
冻结语义，也不把外部 `http.server` 变成 VeriTrail 已实现的管理能力。

### 7.4 `002` 已完成传输事实与收束

运行前的目标 ref、工作区、可用内存和 `127.0.0.1:18773` 均通过预检；Python 3.10.6 创建了唯一
回环监听进程，监听 PID 与创建 PID 一致。原始目录中五个页面均由该进程返回 HTTP `200`：

| 页面 | 响应字节数 |
| --- | ---: |
| `暗室.html` | 38,727 |
| `柳永.html` | 60,037 |
| `苏轼.html` | 109,579 |
| `王维.html` | 31,741 |
| `长卷.html` | 55,612 |

由于原 `002` 合同没有冻结精确桌面/移动视口，浏览器部分在产生任何页面观察前主动停止；因此本记录
仅为 `TRANSPORT_OBSERVED / BROWSER_NOT_EXECUTED`，不满足 `SINGLE_NODE_TRANSPORT_OBSERVED` 的完整
条件。随后只在确认创建 PID 为 Python `http.server` 且命令身份匹配后终止该 PID；进程与端口均已
释放。没有生成 VeriTrail Bundle，也没有改动目标仓库。

### 7.5 预注册探索探针：单节点 Chromium 代表页

> 探针编号：`M11-FEASIBILITY-INK-SINGLE-NODE-BROWSER-003`
> 状态：`PREREGISTERED / EXPLORATORY / NON_ACCEPTANCE`
> 目标引用：`InkNarratives main @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 工具引用：Python 3.10.6 标准库 `http.server`；Codex 内置 Chromium
> 固定端口与路径：`127.0.0.1:18773`、`/苏轼.html`

本探针重新创建一个同样受控的单节点回环服务，只验证已知最完整的 `苏轼.html` 在真实 Chromium 中的
代表性加载。固定视口为桌面 `1440x960` 与移动 `390x844`；每个视口都必须满足：页面完成加载、
`main` 存在且可见、根视口没有横向溢出、页面 title 非空，且 Console 中没有 `error`。页面网络
入口的 HTTP `200` 由 `002` 的保留事实作独立交叉证据；本探针不把一页外推为其余四页的浏览器验收。

服务的创建、PID/端口所有权、目标 ref、工作区与资源预检，以及结束时只清理 owned PID 并核验端口
释放，均沿用 `002` 的同一限制。任一前置、浏览器断言或清理不成立均记录为
`SINGLE_NODE_BROWSER_REJECTED` 或 `PROBE_INVALID`；无论结果如何，都不授权开始 ProjectProfile、Plan、
Evidence 或 M11 实现。

### 7.6 `003` 运行事实与精确结论

运行前核验通过：目标 `HEAD` 仍为 `b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`、目标工作区干净、
可用物理内存为 5,925 MiB，固定端口空闲。新建 Python 3.10.6 进程的 PID 与回环 listener owner
一致；它只服务 InkNarratives 原始目录。目标浏览器入口为
`http://127.0.0.1:18773/%E8%8B%8F%E8%BD%BC.html`。

真实 Codex 内置 Chromium 观察如下：

| 视口 | 完成加载 | Title | `main` 可见 | 根横向溢出 | Console `error` |
| --- | --- | --- | --- | --- | ---: |
| `1440x960` | `complete` | `苏轼生平全记录` | 是 | 否（1425 <= 1440） | 0 |
| `390x844` | `complete` | `苏轼生平全记录` | 是 | 否（375 <= 390） | 0 |

运行期间曾尝试从浏览器只读评估环境读取 `performance.getEntriesByType()`；该环境不暴露该 API，调用在
采集器侧以 `TypeError` 停止，未进入页面代码，也未改变上述页面事实。网络入口 HTTP `200` 继续由
`002` 中独立保存的五页传输记录承担，不能把采集器限制改写成页面网络异常。

浏览器视口已重置，临时页已关闭。结束时先核验 Python `http.server` 进程身份与本探针一致，再终止
该 owned PID；进程、端口均已释放，InkNarratives 工作区保持干净。

`003` 的预注册文本定义了失败状态，却遗漏成功状态名。这是合同文字缺口；为避免事后发明正式状态，
本次只记录为：**所有预注册浏览器断言逐项成立**。它与 `002` 合在一起证明的准确范围是：

> InkNarratives 当前原始目录，在其 README 认可的回环静态服务器形态下，可以作为一个真实的单节点
> HTTP 应用服务五页，并已对其中代表页取得桌面/移动真实 Chromium 加载事实。

它仍然不证明 ProjectProfile 已支持单节点、M10 已管理该服务、五页均完成浏览器/键盘/减少动效验收、
或 M11 已开始、通过或冻结。

## 8. 当前准确结论

M10 地基已经稳定并可寻址，但它的固定两节点证明范围与现有候选项目的真实最小拓扑不完全重合。
InkNarratives 已从“静态根目录不能被 M5 直接快照”进一步获得了真实的单节点 HTTP/代表页浏览器
可运行事实；这说明独立单节点 Profile 合同具有实际目标，不等于 M10 边界已经扩展。基于现有事实，
`OPTION_B` 与 InkNarratives 精确 ref 已进入[双门 Contract 0.2](23-m11-single-node-real-project-contract.md)，
状态为 `CONTRACT_FROZEN / TARGET_SELECTED / IMPLEMENTATION_NOT_STARTED`。因此 M11 里程碑仍为
`PLANNED`，尚未开始 Gate A 实现，更没有真实项目 Bundle 或冻结标签。这个边界防止 VeriTrail 为了
证明自己“通用”而先扭曲真实项目。
