# M11 单节点能力与真实项目全链路合同草案 0.1

> 状态：`DRAFT / TARGET_PROPOSED / CONTRACT_NOT_FROZEN / IMPLEMENTATION_NOT_AUTHORIZED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`
> 前置基线：`m10-v0.11.1` @ `f4efdd25c50b19077c61994bce3e2aca5244d5ec`
> 拟选真实目标：`InkNarratives main @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 冻结引用：尚未创建

## 1. 合同只解决什么

M11 要证明 VeriTrail 能验收一个不同于自身 fixture 的真实项目。现有探针已经取得两组运行事实：

- M5 `STATIC_HTTP` 不能直接快照 InkNarratives 原始仓库根目录，首次确定性拒绝为隐藏路径；
- InkNarratives README 认可的 `python -m http.server` 单节点形态可由原始目录服务五页，五页均真实
  返回 HTTP 200，代表页也已通过 Codex 内置 Chromium 的桌面/移动加载、可见性、溢出和 Console 检查。

因此拟选 `OPTION_B`：先独立交付**通用单应用节点 C1 生命周期**，再锁定该能力去验证
InkNarratives。不能通过给目标添加假依赖、统一入口、发布目录或 VeriTrail 专用脚本绕开能力缺口。

本合同草案不授权实现。用户确认、合同一致性审查和冻结提交完成前，M11 保持 `PLANNED`。

## 2. 两道门必须严格串行

```text
Gate A：通用单节点能力
  ProjectProfile/Plan/Preview/生命周期/Evidence/消费者
  -> 目标无关夹具的正向、负向、恢复、清理
  -> 独立固定实现提交

Gate B：InkNarratives 真实项目
  固定消费 Gate A 提交，不再修改公共合同
  -> 原始仓库、真实命令、五页 Chromium、失败恢复、复跑比较
  -> Catalog/Workbench/内置浏览器读回与最终清理
```

Gate A 通过不能冒充真实项目通过；Gate B 若暴露公共能力缺口，必须停止并回到新版本 Gate A，不能在
目标运行中热修 Core 后继续沿用旧计划。两道门的 Run、Bundle、失败事实和清理证据分别保存。

## 3. 控制变量与不变量

Gate A 的唯一主要变量是：

> `project_bootstrap_topology = veritrail_managed_windows_c1_single_application`

相对冻结 M10，以下全部保持受控：Windows 11、`C1_PROCESS_COLD`、可信本地进程、结构化参数、
ToolBindings 0.1、Windows Job Object、owned PID HTTP readiness、回环端口、Browser Adapter、资源
软/硬停止线、ExecutionStatus/Verdict、Bundle/Catalog 权威关系、subject 漂移检测和 teardown 前事实
封存。

Gate B 使用相同主要变量和值，另行冻结 Subject、Git ref、工具、端口、五页路径、浏览器步骤、资源
预算和失败注入。它不是 Gate A 的同计划对照组，不把“换项目”解释为因果处理效果。

持续成立的硬性不变量：

1. 旧 ProjectProfile 0.1 与 Plan 0.6 仍只接受 dependency -> application 两节点；
2. 单节点 Profile 只能含一个 `APPLICATION`，不得含空节点、隐藏 dependency 或预热外部服务；
3. 应用必须由当前 Run 创建、加入 Job、拥有 listener，并由当前 Run 清理；
4. readiness 必须核对 listener owner，HTTP 200 不能替代进程所有权；
5. Browser 只能在 application READY 后开始，失败/中止也必须先封存事实再清理；
6. 目标文件漂移不回滚用户数据，必须阻断无条件 PASS；
7. 资源超限可以中止，不能降低证据、清理或安全标准；
8. 不新增 Shell、stdin/TTY、包管理器、Docker、C0/C2/C3、跨平台或不可信代码隔离声明。

## 4. 公共版本策略

不能放宽旧版本原地兼容。拟新增版本如下：

| Contract | New version | Exact scope | Old version remains |
| --- | --- | --- | --- |
| ProjectProfile | `0.2` | 仅 `SINGLE_APPLICATION` | `0.1` 仍恰好两节点 |
| ExperimentPlan | `0.7` | 仅绑定 Profile 0.2 | `0.6` 仍绑定 Profile 0.1 |
| BootstrapPreview | `0.2` | 明示单节点 topology 和单元素顺序 | `0.1` 仍恰好两节点 |
| bootstrap pre-teardown record | `0.2` | 单节点 staging 事实 | `0.1` 保持可读 |
| runtime.bootstrap collector | `bootstrap-lifecycle/0.3` | 单节点 Evidence | `0.1/0.2` 保持可读 |

Evidence、Report、Evidence Manifest 与 Bundle 外层仍为 `0.1`；它们只在能够无歧义消费新 Plan/Profile
与 collector 的前提下保持版本。若实现证明外层不能兼容，必须暂停并回到合同升级，不能静默扩字段。

Plan 0.7 的唯一 PRIMARY 固定为：

```text
name  = project_bootstrap_topology
value = veritrail_managed_windows_c1_single_application
```

Pairing 与 Batch 继续显式拒绝 Plan 0.7。Comparison 只允许相同 sealed Plan 0.7 与相同 sealed Profile
0.2 的两个 Run，继续输出既有 `MATCH / DRIFT / INCONCLUSIVE`，不得比较 0.6 与 0.7。

## 5. ProjectProfile 0.2 最小模型

Profile 0.2 新增显式字段：

```json
{
  "schema_version": "0.2",
  "topology": "SINGLE_APPLICATION",
  "nodes": ["exactly one APPLICATION node"],
  "start_order": ["application-node-id"],
  "teardown_order": ["application-node-id"],
  "application_node_id": "application-node-id"
}
```

唯一节点必须满足：

- `role=APPLICATION`、`depends_on=[]`、`adapter=TRUSTED_PROCESS_SERVICE`；
- 一个 ToolBinding、结构化参数、受 Subject 约束的工作目录和既有最小环境投影；
- 一个 1024–65535 的回环端口；
- `HTTP_GET_LOOPBACK_OWNED_PID` readiness；
- 既有 stdout/stderr、进程数、Job 内存和 shutdown 上限；
- typed `node_port` / `node_origin` 只能自引用当前 application；不得引用不存在的 dependency。

Profile 0.2 不接受两节点或通用 DAG。多节点、非 HTTP readiness 和数据库所有权继续留给独立合同。

## 6. 生命周期与 Evidence 语义

单节点状态机固定为：

```text
PREPARED
  -> APPLICATION_STARTING
  -> APPLICATION_READY
  -> BROWSER_EXERCISE
  -> EVIDENCE_FINALIZED
  -> TEARDOWN_APPLICATION
  -> TEARDOWN_COMPLETE
```

任一阶段均可进入 `ABORTING -> EVIDENCE_FINALIZED -> TEARDOWN_APPLICATION`。单节点 teardown 虽然退化
为一个元素，仍必须分别记录 sealed、attempted 和 completed 顺序，不能用“只有一个所以肯定清理”
替代运行事实。

`runtime.bootstrap` 0.3 保持既有 facts 大类，但按 collector 版本验证：

- `nodes` 恰好一个 `APPLICATION`，顺序与 Profile 0.2 一致；
- stdout/stderr 附件恰好两份；不生成伪 dependency 空附件；
- resource observation 中 `application_peak_rss_mb` 必须按启动事实采集，
  `dependency_peak_rss_mb` 必须为 `null`，Profile/节点事实负责表达“该角色不存在”；
- `observed_variables.project_bootstrap_topology` 固定为单应用节点值；
- 既有 listener owner、Job、readiness、Browser reference、subject、resource、cleanup 和状态冲突校验
  继续适用；
- 旧 collector 0.1/0.2 的双节点 cardinality、四附件和 observed variable 规则不变。

ExecutionStatus/Verdict 不新增值。既有错误原因沿用其准确语义；如果实现需要新原因，必须先列出
归因优先级、Evidence 适用性和所有消费者，再修订合同。

## 7. 已知消费者与爆炸半径

| Owner/consumer | Required change |
| --- | --- |
| JSON Schema | 新增 Profile 0.2、Plan 0.7、Preview 0.2；旧 schema 不改 |
| `project_profile.py` | 按 schema version 分派两个严格 validator/seal 路径 |
| `plan.py` | Plan 0.7 只绑定 Profile 0.2、单端口和 application origin |
| CLI | seal/preview/run 显式接受 0.7；错误信息区分 0.6/0.7 |
| preflight/resource decision | 接受 0.7 的单端口、相同宿主机停止线与单节点预算，不伪造第二端口 |
| `bootstrap_preview.py` | 生成 Preview 0.2；继续生成并验证 0.1 |
| lifecycle/run | 只接受已验证的一节点 0.2 或两节点 0.1，不开放任意长度 |
| resource monitor | 单节点只记 application；不伪造 dependency 样本 |
| subject snapshot | `.` 继续按既有有界语义包含隐藏目录；不得为目标新增隐式排除规则 |
| Browser Adapter | 复用冻结适配器并消费 Plan 0.7 步骤；本里程碑不增加 reduced-motion 仿真 |
| staging/Evidence | 版本化一节点顺序、两附件和 collector 0.3 |
| Bundle/Verdict/reporting | 封存 Profile 0.2/Plan 0.7，并重推导 authority、Browser reference、cleanup 和污染 |
| Catalog/API | 从 sealed Plan/Profile/Evidence 重算，不只信任 report 摘要 |
| Comparison | 接受同 0.7/0.2，拒绝跨 Plan/Profile 版本比较 |
| Pairing/Batch | 明确拒绝 Plan 0.7 |
| Workbench | 继续只读显示权威 Report/Evidence；不自行推断缺失 dependency |
| README/docs | 只在运行事实成立后更新能力与限制，不提前标记 M11 |

任何实际 diff 触及列表外公共消费者时，影响面立即重新审查；不得以“只是数组从 2 变 1”降为 L1/L2。

## 8. Gate A：目标无关能力验收

Gate A 必须新增一个脱敏、无业务含义的单应用 HTTP helper 与公开示例 Plan/Profile。它只证明通用
生命周期，不得复制 InkNarratives 文件、路径、中文标题或页面结构。

至少真实运行：

1. 正向 READY -> 双视口 Browser -> `COMPLETED/PASS` -> 单节点 cleanup；
2. application 提前退出 -> 可解释 FAIL 与零残留；
3. readiness timeout 与 listener owner mismatch；外部 listener 不被接管或终止；
4. READY 后 cooperative user cancel -> `ABORTED/PENDING`、Browser 不启动或按阶段准确适用；
5. Browser 硬失败、subject drift、cleanup failure、staging failure和运行期内存停止；
6. 相同 sealed Plan/Profile 连续两次正向 Run，首份 Bundle 不覆盖，Comparison 为 `MATCH`；
7. 旧 Plan 0.6 双节点公共出口与 M0–M10 全回归不退化；
8. 每个失败出口均由 Catalog 独立验真，并检查进程、Job、端口、浏览器、staging 与 run-work 残留。

Gate A 的自动化、真实运行和清理事实固定为一个提交后，Gate B 才可开始。资源压力只做受限微并行，
不得同时运行其他项目技术栈；并发数字必须声明总请求、同时在途和实例数。

## 9. Gate B：InkNarratives 精确目标合同

目标拟固定为提交 `b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`。运行前必须从远端读回该提交，
本地工作区干净；观察结果后不得换 ref。目标不新增 `index.html`、发布目录、依赖或适配代码。

草案拟固定的运行形态：

- Python 3.10.6，直接参数 `-m http.server <application-port> --bind 127.0.0.1`；
- application 工作目录为 Subject 根，C1 起点没有目标服务运行；
- `subject_watch_roots=["."]`，按现有指纹语义纳入 `.git`、治理文件、文档、脚本与五个 HTML；不得
  增加排除规则把 Subject 偷换成五页子集，且从运行前快照到运行后快照之间不得执行 Git 命令；
- readiness 使用一个低于既有响应上限的百分号编码页面路径，Browser 入口使用
  `/%E8%8B%8F%E8%BD%BC.html`；具体 readiness 页面和端口在冻结 Plan/Profile 时写死；
- Profile 只继承既有最小 Windows 环境，不读取 `.env`、凭据或浏览器 Profile；
- Subject watch root 为仓库根；目标漂移只记录、不回滚。

草案拟定的冻结预算如下；合同确认前仍可评审，运行观察后不得移动：

| Policy | Gate A | Gate B |
| --- | ---: | ---: |
| application port | `18774` | `18775` |
| readiness path | `/health` | `/%E7%8E%8B%E7%BB%B4.html` |
| readiness response maximum | 4,096 bytes | 65,536 bytes |
| application Job memory | 512 MiB | 512 MiB |
| application process maximum | 8 | 8 |
| stdout / stderr maximum | 262,144 bytes each | 262,144 bytes each |
| lifecycle timeout | 120,000 ms | 120,000 ms |
| process / port / reader release | 5,000 ms each | 5,000 ms each |
| Browser Job memory | 1,024 MiB | 1,024 MiB |
| available-memory soft / hard line | 4,096 / 2,048 MiB | 4,096 / 2,048 MiB |
| output-volume free hard line | 1,024 MiB | 1,024 MiB |
| per-evidence-artifact maximum | 5 MiB | 5 MiB |
| subject watch file / byte maximum | 2,000 / 64 MiB | 2,000 / 64 MiB |
| virtual users / in-flight requests | 1 / 1 | 1 / 1 |

两门都使用 3 次 preflight 样本、50 ms 间隔、连续 2 次 hard breach 停止；collector RSS 上限 256 MiB，
observer RSS delta soft 线 64 MiB。Gate B readiness 页面已由 `002` 观察为 31,741 字节，低于拟定
65,536 字节上限；最终仍必须由受控 readiness 实际重测，不能继承探针结果。

真实浏览器必须按固定顺序覆盖 `暗室.html`、`柳永.html`、`苏轼.html`、`王维.html`、`长卷.html`，
并在桌面 `1440x960` 与移动 `390x844` 中检查：

- 每页 HTTP 文档为 200，Console、page error、failed request 和未解释 4xx/5xx 为 0；
- `main` 与关键标题可见，根视口无横向溢出；
- 固定截图与步骤时间线进入 Bundle；
- 默认动效按目标现有质量边界检查；当前 Browser Adapter 未声明 `prefers-reduced-motion` 仿真，M11
  不顺手扩展该公共能力，减少动效保持 `NOT_PROVEN`，只引用目标既有基线而不继承其 PASS；
- Codex 内置浏览器再执行完整五页浏览、刷新/返回、物理键盘、桌面/移动与 Console/Network 复核。

目标不存在写业务、数据库、中间件、多角色或最终一致性语义；这些项必须标记 `NOT_APPLICABLE`，不能
制造假请求、假身份或假多实例来点亮能力。

## 10. Gate B 失败、恢复与复跑

至少保留：

1. 一个预注册 Browser 负向 Run（例如不存在的 selector），形成真实 `COMPLETED/FAIL`，不能改目标
   文件制造失败；
2. 一个 owned service 中断或端口竞争负向，证明不误杀外部 listener；
3. 负向清理后从同一 ref、同一 Plan/Profile 完成正向恢复 Run；
4. 两次独立正向 Run 生成不可覆盖 Bundle，并以 M6 Comparison 得到可解释结果；
5. Catalog 同时接纳正向、负向和恢复 Run，损坏副本被隔离；
6. Workbench 从生产构建和只读 API 读回 Evidence，不重新裁决；
7. 最终端口、owned process、Job、Chromium、staging、run-work 和目标 Git 状态全部回到起点。

Comparison 若不是 `MATCH`，必须解释差异来源并决定 `DRIFT/INCONCLUSIVE`，不能为了 M11 完成而放宽
比较规则。Pairing/Batch 在本目标没有真实反事实或组合语义，保持不适用。

## 11. 安全、资源与适用边界

- 16 GB 宿主机默认严格串行；启动前重新采样内存、磁盘和端口；
- soft/hard 内存线、Job 内存、输出、生命周期、Browser 与附件上限必须在 Plan/Profile 中冻结；
- Python `http.server` 会在回环范围服务声明工作目录，VeriTrail 不声称文件系统或网络隔离；本目标是
  公开且已核验无 `.env` 的仓库，但该事实不能推广到其他项目；
- 不持久化绝对路径、PID、请求头/正文、环境值、Cookie 或私密数据；
- 不启动 Docker、MySQL、Redis、RabbitMQ 或其他无关中间件；
- 该结论只适用于 Windows 11、Python 3.10.6、C1、本地可信单应用进程与目标精确 ref；Linux、macOS、
  Docker、C2/C3、动态后端、多节点和不可信代码继续 `NOT_PROVEN/NOT_SUPPORTED`。

## 12. 冻结出口与停止条件

合同冻结前必须：

- [ ] 用户确认拟选 `OPTION_B`、目标 ref、双门顺序和不适用项；
- [ ] 列表中的所有公共消费者完成逐项审查；
- [ ] 成功、失败和状态归因在运行前具名，不能再出现成功状态名遗漏；
- [ ] 复核 Gate A 与 Gate B 的拟定端口、资源线，并补齐精确步骤、断言、Run ID 规则和清理命令；
- [ ] 确认新增版本不原地放宽 M10 冻结合同；
- [ ] 创建合同冻结提交；冻结前不创建实现代码或 M11 标签。

M11 只有在 Gate A 和 Gate B 均完成代码事实、自动化、真实 Chromium、Codex 内置浏览器、失败恢复、
Catalog/Workbench、Comparison、敏感扫描、资源和零残留证据后，才能标记 `FROZEN` 并创建不可移动
`m11-v0.12.0` 标签。合同、实现或运行中任一硬条件未满足时保持 `PLANNED/IMPLEMENTING/PENDING` 的
准确状态，计划文字不得替代运行事实。
