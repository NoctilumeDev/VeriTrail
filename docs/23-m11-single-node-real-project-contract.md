# M11 单节点能力与真实项目全链路合同 0.3

> 状态：`CONTRACT_CORRECTED / TARGET_SELECTED / GATE_A_VALIDATED / GATE_B_NOT_STARTED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`
> 前置基线：`m10-v0.11.1` @ `f4efdd25c50b19077c61994bce3e2aca5244d5ec`
> 固定真实目标：`InkNarratives main @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 用户确认：2026-08-14，确认 `OPTION_B`、精确 ref、Gate A -> Gate B 严格串行与不适用项
> 历史冻结引用：Contract 0.2 首次进入 `CONTRACT_FROZEN` 的提交 `eb39c0a`

Contract 0.2 已在 `eb39c0a` 留下不可变历史。Gate A 实现前的严格 Plan/Profile 绑定测试证明，
0.2 第 8.1 节让一个 sealed Plan 同时绑定四个不同 sealed Profile，在既有
`bootstrap_profile.profile_sha256` 权威关系下不可实现。0.3 只把三个生命周期变体各自分配给独立
Plan authority；不改变 Profile、Run 顺序、出口、资源预算、裁决、Gate A -> Gate B 门禁或真实目标。
这项纠偏发生在任何 Gate A Run 之前，不能被解释为观察结果后移动标准。

## 1. 合同只解决什么

M11 要证明 VeriTrail 能验收一个不同于自身 fixture 的真实项目。现有探针已经取得两组运行事实：

- M5 `STATIC_HTTP` 不能直接快照 InkNarratives 原始仓库根目录，首次确定性拒绝为隐藏路径；
- InkNarratives README 认可的 `python -m http.server` 单节点形态可由原始目录服务五页，五页均真实
  返回 HTTP 200，代表页也已通过 Codex 内置 Chromium 的桌面/移动加载、可见性、溢出和 Console 检查。

因此固定 `OPTION_B`：先独立交付**通用单应用节点 C1 生命周期**，再锁定该能力去验证
InkNarratives。不能通过给目标添加假依赖、统一入口、发布目录或 VeriTrail 专用脚本绕开能力缺口。

Contract 0.3 的 Gate A 已以 Profile 0.2、Plan 0.7、单节点生命周期、13 个公共出口、
Catalog/Comparison、资源、安全和零残留事实关闭，详见文档 25。它仍不证明真实项目能力：Gate B
尚未开始，M11 继续保持 `PLANNED`，不得创建 M11 标签或进入 M12。

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

不能放宽旧版本原地兼容。冻结新增版本如下：

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

Profile 0.2 固定新增显式字段：

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
| `bootstrap_public_run.py` / `bootstrap_run.py` | 只接受已验证的一节点 0.2/0.7 或两节点 0.1/0.6，不开放任意长度 |
| `bootstrap_lifecycle.py` / Windows adapters | 单节点复用既有 Job/listener/readiness 所有权，不弱化启动、停止或竞态检查 |
| resource monitor | 单节点只记 application；不伪造 dependency 样本 |
| subject snapshot | `.` 继续按既有有界语义包含隐藏目录；不得为目标新增隐式排除规则 |
| Browser Adapter | 复用冻结适配器并消费 Plan 0.7 步骤；本里程碑不增加 reduced-motion 仿真 |
| staging/Evidence | 版本化一节点顺序、两附件和 collector 0.3 |
| `evidence.py` | 按 collector/Profile 版本验证两附件或四附件；旧四附件规则不原地放宽 |
| Bundle/Verdict/reporting | 封存 Profile 0.2/Plan 0.7，并重推导 authority、Browser reference、cleanup 和污染 |
| Catalog/API | 从 sealed Plan/Profile/Evidence 重算，不只信任 report 摘要 |
| Comparison | 接受同 0.7/0.2，拒绝跨 Plan/Profile 版本比较 |
| Pairing/Batch | 明确拒绝 Plan 0.7 |
| Workbench | 生产代码继续通用只读显示；新增单节点账册夹具，不自行推断缺失 dependency |
| README/docs | 只在运行事实成立后更新能力与限制，不提前标记 M11 |

冻结审查已逐项搜索并读取 `0.6`、ProjectProfile、`runtime.bootstrap`、collector、sealed Profile 和
附件基数消费者。生产 Workbench 当前没有双节点硬编码，只有 M10 通用账册测试夹具；它仍进入回归，
但不借 M11 新增前端业务逻辑。任何实际 diff 触及列表外公共消费者时，影响面立即重新审查；不得以
“只是数组从 2 变 1”降为 L1/L2。

## 8. Gate A：目标无关能力验收

Gate A 必须新增一个脱敏、无业务含义的单应用 HTTP helper 与公开示例 Plan/Profile。它只证明通用
生命周期，不得复制 InkNarratives 文件、路径、中文标题或页面结构。

### 8.1 冻结 authority

| Authority | ID | Version | Use |
| --- | --- | ---: | --- |
| positive Plan | `m11-single-app-gatea-positive` | 1 | 两次正向及使用 positive Profile 的预注册负向 |
| Browser-negative Plan | `m11-single-app-gatea-browser-negative` | 1 | 只把一个已具名 selector 换成确定不存在的 selector |
| early-exit Plan | `m11-single-app-gatea-early-exit` | 1 | 只绑定 early-exit Profile；Browser 步骤不改 |
| readiness-timeout Plan | `m11-single-app-gatea-readiness-timeout` | 1 | 只绑定 timeout Profile；Browser 步骤不改 |
| owner-mismatch Plan | `m11-single-app-gatea-owner-mismatch` | 1 | 只绑定 owner-mismatch Profile；Browser 步骤不改 |
| positive Profile | `m11-single-app-helper` | 1 | 正向、Browser/collector/subject/cleanup/staging/memory 与外部端口竞争 |
| early-exit Profile | `m11-single-app-helper-early-exit` | 1 | application 在 READY 前退出 |
| timeout Profile | `m11-single-app-helper-readiness-timeout` | 1 | owned application 存活但不满足 readiness |
| owner-mismatch Profile | `m11-single-app-helper-owner-mismatch` | 1 | owned application 不拥有被观察 listener |

全部 Profile 只绑定同一个 Gate A helper；变体只用结构化参数选择已预注册行为，不增加第二个进程、
隐藏节点、Shell 或运行时环境变量开关。每个 Plan 只绑定表中唯一 Profile 的 ID、version 与摘要；
Plan/Profile 必须在首个对应 Run 前 seal，观察结果后只能升版本，不能移动同 ID/version 的 authority。

### 8.2 冻结 HARD 断言

| Assertion ID | Evidence path / relation | Expected and applicability |
| --- | --- | --- |
| `m11-preflight-snapshot-complete` | `runtime.preflight:/facts/snapshot_complete` | 所有 Run 为 `true`；live preflight 不能复用 Preview 摘要冒充 |
| `m11-bootstrap-service-ready` | `runtime.bootstrap:/facts/services_ready` | 进入 Browser 的 Run 为 `true`；READY 前失败按阶段不适用 |
| `m11-bootstrap-order` | sealed/attempted/completed order | 启动只有 application；清理也只有 application，且三者与 Profile 0.2 一致 |
| `m11-bootstrap-stream-cardinality` | bootstrap attachments | collector 0.3 恰好 application stdout/stderr 两份；不得出现 dependency 占位附件 |
| `m11-browser-capture-complete` | `browser.session:/facts/capture_complete` | Browser 适用且 collector 正常时为 `true` |
| `m11-browser-steps-passed` | `browser.session:/facts/all_steps_passed` | 正向为 `true`；预注册 selector 负向为 `false` |
| `m11-browser-console-clean` | unexpected Console errors | 正向为 `0` |
| `m11-browser-page-clean` | page errors | 正向为 `0` |
| `m11-browser-request-clean` | failed requests | 正向为 `0` |
| `m11-browser-http-clean` | unexpected HTTP errors | 正向为 `0` |
| `m11-browser-write-clean` | duplicate write request groups | 全部 Browser Run 为 `0` |
| `m11-browser-overflow-clean` | horizontal-overflow viewports | 正向为 `0` |
| `m11-browser-viewport-coverage` | `browser.session:/facts/viewport_count` | 正向为 `2`；必须实际完成桌面与移动两个视口 |
| `m11-browser-screenshot-coverage` | `browser.session:/facts/screenshot_count` | 正向为 `2`；每个固定视口各有一份已入清单截图 |
| `m11-browser-cleanup-complete` | Browser cleanup fact | 启动 Browser 的 Run 为 `true`，除预注册 collector error 仍必须 best-effort 后准确记录 |
| `m11-bootstrap-cleanup-complete` | bootstrap cleanup fact | 除 cleanup-failure 负向外为 `true`；负向必须为 `false` 并阻断 PASS |
| `m11-subject-unchanged` | before/after Subject fingerprint | 非 drift Run 相同；drift Run 的 Evidence reason 为 `SUBJECT_DRIFT`，Verdict 断言代码为 `BOOTSTRAP_SUBJECT_DRIFT` |
| `m11-catalog-rederivation` | sealed authorities -> Catalog | Catalog 重算后的 status/verdict、适用性与 Report 一致，损坏副本被隔离 |
| `m11-zero-owned-residual` | owned process/Job/listener/Browser/staging/run-work | 每轮结束回到预注册起点；cleanup-failure 先保留失败事实，再完成独立恢复才允许下一 Run |

表中指向单一 Evidence JSON path 的条目进入 sealed Plan 0.7 的 `assertions`。跨多个 path 的启动/清理
顺序关系、bootstrap stdout/stderr 附件基数、Catalog 重算和外部残留属于 Gate A 验收关系断言：专用
验收器必须从不可变 Bundle 与当前机器事实独立核对，不能用某个布尔汇总字段替代这些关系，也不能因
它们不适合单 path 运算符就从门禁中删去。

### 8.3 冻结 Run 顺序与出口

严格串行执行下表顺序；Run ID 不得复用，失败 Run 不删除。`stop / status / verdict` 中的 stop 是
`runtime.bootstrap` 的既有 reason；预检期端口竞争不生成 bootstrap stop reason。

| Order | Run ID | Plan / Profile | Frozen scenario | Expected stop / status / verdict |
| ---: | --- | --- | --- | --- |
| 1 | `m11-gatea-positive-01` | positive / positive | 正向 READY、双视口 Browser、完整清理 | `NONE / COMPLETED / PASS` |
| 2 | `m11-gatea-positive-02` | positive / positive | 同 sealed Plan/Profile 独立复跑 | `NONE / COMPLETED / PASS` |
| 3 | `m11-gatea-early-exit-01` | early-exit / early-exit | application READY 前退出 | `NODE_EARLY_EXIT / COMPLETED / FAIL` |
| 4 | `m11-gatea-readiness-timeout-01` | readiness-timeout / timeout | owned listener 永不满足 readiness | `READINESS_TIMEOUT / ABORTED / FAIL` |
| 5 | `m11-gatea-owner-mismatch-01` | owner-mismatch / owner-mismatch | readiness 命中错误 listener owner | `LISTENER_OWNERSHIP_MISMATCH / ABORTED / FAIL` |
| 6 | `m11-gatea-port-conflict-01` | positive / positive | Preview 后、live preflight 前外部进程占端口 | preflight-only / `ABORTED / PENDING` |
| 7 | `m11-gatea-user-cancel-ready-01` | positive / positive | application READY 后 cooperative cancel，Browser 尚未创建 | `USER_CANCELLED / ABORTED / PENDING` |
| 8 | `m11-gatea-browser-negative-01` | Browser-negative / positive | 独立 sealed Plan 的不存在 selector | `BROWSER_HARD_FAILURE / COMPLETED / FAIL` |
| 9 | `m11-gatea-browser-collector-error-01` | positive / positive | 已具名 Browser observer/collector error | `COLLECTOR_ERROR / ERROR / PENDING` |
| 10 | `m11-gatea-subject-drift-01` | positive / positive | Browser 后、after snapshot 前的已具名 Subject 变化 | `SUBJECT_DRIFT / COMPLETED / INCONCLUSIVE` |
| 11 | `m11-gatea-cleanup-failure-01` | positive / positive | 已具名 cleanup 观测失败 | `CLEANUP_ERROR / ERROR / FAIL` |
| 12 | `m11-gatea-staging-failure-01` | positive / positive | 显式 pre-teardown staging writer 失败 | `EVIDENCE_ERROR / ERROR / PENDING` |
| 13 | `m11-gatea-memory-stop-01` | positive / positive | 运行期 soft memory stop，且没有更早的决定性失败 | `RESOURCE_MEMORY_SOFT_LIMIT / ABORTED / PENDING` |

`m11-gatea-positive-01` 与 `m11-gatea-positive-02` 必须以 M6 Comparison 得到 `MATCH` 和 0 差异；
任何其他 Run 都不得塞入该比较。旧 Plan 0.6 双节点公共出口、M0–M10 全回归和 Pairing/Batch 对 0.7
的显式拒绝必须同时通过。每个失败出口均由 Catalog 独立验真，并在下一轮前完成第 10.3 节的残留
门禁；外部 listener 只能由它自己的测试 owner 结束，VeriTrail 不得接管或终止。

Gate A 的自动化、真实运行和清理事实固定为一个提交后，Gate B 才可开始。资源压力只做受限微并行，
不得同时运行其他项目技术栈；并发数字必须声明总请求、同时在途和实例数。

## 9. Gate B：InkNarratives 精确目标合同

目标固定为提交 `b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`。运行前必须从远端读回该提交，
本地工作区干净；观察结果后不得换 ref。目标不新增 `index.html`、发布目录、依赖或适配代码。

### 9.1 冻结 authority 与运行形态

| Authority | ID | Version | Use |
| --- | --- | ---: | --- |
| positive Plan | `m11-ink-single-app-positive` | 1 | 正向、端口竞争和恢复正向 |
| Browser-negative Plan | `m11-ink-single-app-browser-negative` | 1 | 只把一个具名 selector 换为 `#veritrail-m11-missing-selector` |
| ProjectProfile | `m11-ink-single-app` | 1 | 全部 Gate B Run |

固定运行形态：

- Python 3.10.6，直接参数 `-m http.server <application-port> --bind 127.0.0.1`；
- application 工作目录为 Subject 根，C1 起点没有目标服务运行；
- `subject_watch_roots=["."]`，按现有指纹语义纳入 `.git`、治理文件、文档、脚本与五个 HTML；不得
  增加排除规则把 Subject 偷换成五页子集，且从运行前快照到运行后快照之间不得执行 Git 命令；
- readiness 固定为 `/%E7%8E%8B%E7%BB%B4.html`，Browser 入口固定为
  `/%E8%8B%8F%E8%BD%BC.html`；
- Profile 只继承既有最小 Windows 环境，不读取 `.env`、凭据或浏览器 Profile；
- Subject watch root 为仓库根；目标漂移只记录、不回滚。

冻结预算如下；变更必须升 Plan/Profile 版本，运行观察后不得移动原版本：

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
observer RSS delta soft 线 64 MiB。Gate B readiness 页面已由 `002` 观察为 31,741 字节，低于冻结
65,536 字节上限；最终仍必须由受控 readiness 实际重测，不能继承探针结果。

### 9.2 自动 Browser Plan 步骤

positive Plan 在桌面 `1440x960` 与移动 `390x844` 上执行完全相同的下表步骤。`goto` 使用 Gate B
application origin 与表中百分号编码 path；每次导航后均先验证文档 200、`main` 可见、`h1` 包含固定
文本，再执行交互。总步骤不得超过既有 50 步上限，截图 action 不得超过 4 个。

| Order | Page/path | Fixed H1 | Deterministic interaction and expected state |
| ---: | --- | --- | --- |
| 1 | `/%E8%8B%8F%E8%BD%BC.html` | `苏轼生平全记录` | click `a[href="#chapter11"]`; `#chapter11` visible |
| 2 | `/%E6%9A%97%E5%AE%A4.html` | `暗室 · 藏书` | `#library` visible; click `.book[data-title="封装之书"]`; `#readerTitle` contains `封装之书` |
| 3 | `/%E6%9F%B3%E6%B0%B8.html` | `乐章集` | click `a[href="#juan8"]`; `#juan8` visible |
| 4 | `/%E7%8E%8B%E7%BB%B4.html` | `空山见王维` | click `a[href="#c6"]`; `#c6` visible |
| 5 | `/%E9%95%BF%E5%8D%B7.html` | `夜航船` | click `a[href="#cabin"]`, then `.book[data-book="mountain"]`; `#reader-title` contains `空山之后` |

固定截图放在苏轼章节、暗室读者层、王维末章和长卷读者层之后。Browser-negative Plan 与 positive Plan
的 authority、Profile、目标、资源、页面顺序和其他步骤完全相同，只把苏轼 `#chapter11` 的
`expect_visible` selector 换成 `#veritrail-m11-missing-selector`；它必须独立 seal，不能在正向 Plan
中运行时改 selector。

自动 Browser Evidence 必须断言：

- 每页 HTTP 文档为 200，Console、page error、failed request 和未解释 4xx/5xx 为 0；
- `main` 与关键标题可见，根视口无横向溢出；
- 固定截图与步骤时间线进入 Bundle；
- `capture_complete=true`、正向 `all_steps_passed=true`、重复写请求组为 0；
- Browser cleanup 与 bootstrap cleanup 完整，preflight snapshot 完整且 application 曾进入 READY；
- 默认动效按目标现有质量边界检查；当前 Browser Adapter 未声明 `prefers-reduced-motion` 仿真，M11
  不顺手扩展该公共能力，减少动效保持 `NOT_PROVEN`，只引用目标既有基线而不继承其 PASS；
- Codex 内置浏览器验收按第 10.2 节独立执行，不能混入自动 Run 的 Bundle。

目标不存在写业务、数据库、中间件、多角色或最终一致性语义；这些项必须标记 `NOT_APPLICABLE`，不能
制造假请求、假身份或假多实例来点亮能力。

## 10. Gate B 失败、恢复与复跑

### 10.1 冻结 Run 顺序

| Order | Run ID | Plan | Frozen scenario | Expected |
| ---: | --- | --- | --- | --- |
| 1 | `m11-gateb-ink-positive-01` | positive | 精确 ref、五页双视口正向 | `NONE / COMPLETED / PASS` |
| 2 | `m11-gateb-ink-browser-negative-01` | Browser-negative | 苏轼页预注册不存在 selector | `BROWSER_HARD_FAILURE / COMPLETED / FAIL` |
| 3 | `m11-gateb-ink-port-conflict-01` | positive | Preview 后、live preflight 前由外部 owner 占用 18775 | preflight-only / `ABORTED / PENDING` |
| 4 | `m11-gateb-ink-recovery-positive-02` | positive | 外部 owner 自行结束并证明端口恢复后，同 ref 恢复正向 | `NONE / COMPLETED / PASS` |

四个 Bundle 均保留且由 Catalog 独立验真。只比较
`m11-gateb-ink-positive-01` 与 `m11-gateb-ink-recovery-positive-02`；两者必须绑定完全相同的 sealed
positive Plan/Profile，并以 M6 Comparison 得到 `MATCH`。若实际为 `DRIFT/INCONCLUSIVE`，必须解释
来源并停止冻结，不能放宽比较规则。Browser-negative 因 selector 不同而必须使用独立 sealed Plan，
不得参加比较。Pairing/Batch 在本目标没有真实反事实或组合语义，保持 `NOT_APPLICABLE`。

Catalog 必须同时接纳正向、负向和恢复 Run，损坏副本被隔离。Workbench 只从生产构建和只读 API
读回 sealed Evidence、Report 与 Comparison，不重新裁决；这项 Workbench 读回是 Bundle 事实的独立
浏览器验收，不替代目标项目的自动 Browser Evidence。

### 10.2 Codex 内置浏览器补充验收边界

自动 Gate B Run teardown 后，其 18775 listener 已经不存在，不能为了人工复核偷偷复用或延长
Run-owned application。Codex 内置浏览器补充验收固定使用：

- 同一目标 ref、同一 Python 3.10.6 module/参数形态和同一 Subject 根；
- 独立 owned 临时进程与专用回环端口 `18776`；
- 五页完整桌面/移动浏览、固定交互、刷新/返回、物理键盘，以及 F12 Console/Network 复核；
- 单独的 acceptance record，明确进程 owner、开始/结束时间、页面结果、Console/Network 和残留；
- 验收后只清理该独立进程并证明 18776 释放。

该记录是用户可见补充验收，不进入、不修改也不替代任一 Gate B Bundle，不能把人工观察倒填为
`browser.session`。Workbench 的生产读回再使用其自身独立受控服务；目标进程、Workbench 服务和
Catalog API 不得同时留在后台。

### 10.3 自动清理与只读残留门禁

每个 Run 都必须先封存 pre-teardown 事实，再由 lifecycle 终止当前 Run 的 Browser Job（若适用）和
application Job，关闭流 reader，等待 owned PID 与端口释放，最后原子发布或隔离 Bundle。验收器随后
只读核对：

1. Profile 的 application PID/进程树和 Job 不再存活；不得用进程名匹配或全局 `taskkill` 代替所有权；
2. 当前 Run 端口不再 LISTEN；端口竞争夹具的外部 owner 不由 VeriTrail 关闭；
3. Chromium/CDP observer、stdout/stderr reader 和临时 listener 无 owned handle 残留；
4. staging 与 run-work 无未解释目录；不可变 Bundle 是产物，不算临时残留，也不得被后续 Run 覆盖；
5. Subject after snapshot 已完成，且其前后指纹满足对应 Run 断言；两次 snapshot 之间没有 Git 命令；
6. snapshot 完成后才允许只读确认目标 `HEAD` 仍为固定 ref、工作区干净；不执行 reset/checkout/clean；
7. cleanup-failure 负向先保留 `CLEANUP_ERROR` Bundle，再通过独立、具名、owned 恢复步骤回到起点；
   恢复证据成立前不得开始下一 Run。

任何 residual 无法证明归属或清除时停止 Gate，不以人工口头说明标记通过。最终 18774、18775、18776、
owned process、Job、Chromium、staging、run-work、Workbench/Catalog 服务与目标 Git 状态全部回到起点。

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

合同冻结门禁：

- [x] 用户确认 `OPTION_B`、目标 ref、双门顺序和不适用项；
- [x] 列表中的所有已知公共消费者完成逐项审查；
- [x] 成功、失败和状态归因在运行前具名；
- [x] Gate A/Gate B 端口、资源线、精确步骤、断言、Run ID 和清理/残留规则已冻结；
- [x] 新增版本以显式分派实现，不原地放宽 M10 冻结合同；
- [x] Contract 0.2 冻结提交只创建文档合同，没有创建实现代码、Schema、版本或 M11 标签；
- [x] Contract 0.3 在任何 Gate A Run 前纠正 Plan/Profile 一对一绑定，不改变出口和判定标准；
- [x] Gate A 实现与 13 个真实出口已从 Run 1 全量通过，并进入固定实现提交；事实见文档 25。

前八项说明合同内容与 Gate A 事实已关闭，不说明 Gate B 或整个 M11 已实现。README 里 M11 在 Gate B
取得事实前必须继续显示 `PLANNED`；开始编码后也只能使用准确的内部阶段状态，不能提前写 `FROZEN`。

M11 只有在 Gate A 和 Gate B 均完成代码事实、自动化、真实 Chromium、Codex 内置浏览器、失败恢复、
Catalog/Workbench、Comparison、敏感扫描、资源和零残留证据后，才能标记 `FROZEN` 并创建不可移动
`m11-v0.12.0` 标签。合同、实现或运行中任一硬条件未满足时保持 `PLANNED/IMPLEMENTING/PENDING` 的
准确状态，计划文字不得替代运行事实。
