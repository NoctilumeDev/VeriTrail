# M13 系统思维与分层代码质量终审计划

> 状态：`CONTRACT_FROZEN / AUDIT_IN_PROGRESS`
> 计划版本：`M13 System and Layered Code Quality Audit Plan 0.1`
> 影响层级：`L0 / L1 / L2 / L3 REVIEW`；整改层级必须逐项另行声明
> 冻结能力基线：`m12-v0.13.0^{}` @ `5f32c33ab3dac076151a4fcd9a93a74ccafcfaa9`
> 审查入口提交：`392e7608b7097aaae701ccb24524ba2dae868f73`
> 依赖规划：[Post-M8 收束路线 Plan v1 第 9 节](13-post-m8-roadmap.md)
> 后继门禁：M13 结论成立前，M14 只能保持 `PLANNED`

## 1. 目标与问题

M0–M12 已逐层形成计划、Evidence、Verdict、Catalog、三类派生分析、受控执行、自举、真实项目和
只读 Workbench。单个里程碑通过不自动证明这些能力连接成一个没有权威冲突、旁路、资源泄漏或
兼容断层的完整系统。M13 因此只回答以下问题：

1. 产品目标、非目标和真实用户链是否仍由同一组事实支持；
2. Plan、Run、Evidence、Verdict、Bundle、Catalog、Comparison、PairedAnalysis、BatchAnalysis、
   API 与 Workbench 是否各自只有一个明确所有者；
3. 命令、自举、Browser、资源与清理状态机是否存在可绕过门禁或被异常压平的出口；
4. 冻结 Schema、版本分派、序列化与全部消费者是否仍保持兼容；
5. L0–L3 的实现和测试是否足以维护这些合同，而不是只让局部测试变绿。

M13 是审查与有界整改里程碑，不增加产品功能，不扩展支持平台，不重写视觉主题，也不把自动化、
截图或日志单独当作系统成立的证据。

## 2. 固定边界与非目标

本轮固定以下边界：

- M12 标签不移动；历史 M0–M12 标签、失败 Run 和不利事实保持不可变；
- Python 包版本保持 `0.12.0.dev1`，Workbench 保持 `0.12.0-dev.1`；
- 不新增或调整公共 Schema、Verdict、ExecutionStatus、命令信任模型或支持矩阵；
- 不增加 Shell、包管理器、Docker、C2/C3、跨平台、不可信代码隔离、真实 wave 并行或 AI 裁决；
- 不为消除 warning、重复或文件行数而做无可观察收益的全仓重写；
- 不把 InkNarratives 固定目标的 1280 px 装饰层溢出改写成 VeriTrail M13 产品缺陷；
- 不提前执行 M14 的双目标终局全量复验、最终版本、Release 或发布材料收束。

如果发现必须改变冻结 L2/L3 语义才能修复的问题，立即停止对应整改，记录受影响基线、所有者、
消费者和最小独立合同。不得在“质量优化”名义下静默修改后继续宣称旧基线有效。

## 3. 入口门禁

审查开始前必须同时满足：

- [x] `m12-v0.13.0^{}` 精确读回 `5f32c33ab3dac076151a4fcd9a93a74ccafcfaa9`；
- [x] 入口工作树干净，`main` 与 `origin/main` 精确一致；
- [x] README、产品简报、证据模型、架构和验收标准已完整重读；
- [x] M10 地基审查、M11 终审债务和 Post-M8 第 9 节已复核；
- [x] M12 冻结事实没有授权 M13 修改 package、Schema、裁决或标签语义；
- [x] 用户已授权按收束路线继续主线。

审查入口若出现产品事实与代码、文档或远端引用冲突，先修复事实入口或停止；不能带着冲突继续
采样并把后续绿色结果拼成通过。

## 4. 权威链与消费者矩阵

M13 按下列顺序追踪所有权，不能从 UI 或报告表象反向推测事实：

```text
sealed authority
  -> execution / collection state machines
  -> immutable Evidence and attachments
  -> deterministic Verdict and Report
  -> Manifest / Bundle
  -> rebuildable Catalog
  -> Comparison / PairedAnalysis / BatchAnalysis
  -> loopback read-only API
  -> Workbench presentation and interaction state
```

每一层必须记录：

| 字段 | 要求 |
| --- | --- |
| 所有者 | 唯一可创建或决定该事实的模块 |
| 输入 | 直接权威、版本和校验边界 |
| 输出 | 公共形状、不可变性与失败问题码 |
| 消费者 | Core、CLI、Catalog、派生分析、API、Workbench、脚本和外部格式 |
| 禁止动作 | 反写 Verdict、信任自报派生字段、跳过 seal/hash 或扩大权限 |
| 失败语义 | 错误、中止、待定、不确定、失败与隔离的唯一组合 |
| 恢复/清理 | 句柄、进程、端口、Browser、work、staging、SQLite sidecar 和对象 URL |

公共版本至少覆盖 Plan 0.1–0.7、Profile 0.1–0.2、Preview 0.1–0.2、collector 0.1–0.3，以及全部冻结
Evidence、Report、Manifest、Comparison、Pairing 和 Batch 格式。未知版本必须拒绝，旧消费者不能
因新路径存在而被静默改写。

## 5. 审查阶段

### 5.1 A：仓库与冻结基线盘点

- 记录 tracked/untracked、提交、标签、包版本、依赖锁、工作流和生成物边界；
- 按 `src / schemas / tests / scripts / web / docs` 建立文件、行数和公共入口清单；
- 搜索宽泛异常、关键 `assert`、动态执行、原始 HTML、路径重开、全局可变状态、TODO/FIXME、
  重复状态映射和只覆盖成功路径的测试；
- 大文件只登记为热点，不因行数直接生成整改结论。

### 5.2 B：系统权威、数据流与状态机

- 从 seal、preview、preflight、run、browser、evidence、evaluate、bundle 到 catalog 逐段追踪；
- 核对 `COMPLETED / ABORTED / ERROR` 与 `PASS / FAIL / INCONCLUSIVE / PENDING` 的组合；
- 核对失败、重试、取消、超时、崩溃、Evidence staging 失败、cleanup 失败和部分成功没有被压平；
- 核对 Catalog 与三类派生分析从权威重建，不信任 Report 或 UI 自报；
- 核对 CLI、API、Workbench 和验收脚本没有第二套裁决或隐藏旁路。

### 5.3 C：安全、资源、并发与恢复

- 复核 executable/argv/cwd/environment、路径 containment、reparse/hardlink、文件身份、脱敏和秘密流；
- 复核 Job、进程树、listener owner、owned readiness、外部进程不误杀和逆序清理；
- 复核 Browser Context、请求账册、对象 URL、线程、SQLite sidecar、work/staging 和端口最终回零；
- 复核 Core、Subject、Browser、dependency/application 与 UI 的资源分账和停止线；
- 复核用户态采样、TOCTOU 与恶意代码隔离的已知上限没有被文档夸大。

### 5.4 D：L0–L3 分层代码质量

| 层级 | 审查重点 | 最低证据 |
| --- | --- | --- |
| `L0` | 语义、可访问性、响应式、焦点、history、错误/空态、渲染与前端状态边界 | 源码、组件测试、生产浏览器实际呈现与 Console/Network |
| `L1` | 单模块职责、长函数阶段边界、异常、超时、句柄释放、命名、重复与可测试性 | 调用者、characterization/负向测试、资源清理事实 |
| `L2` | Schema、版本分派、序列化、兼容、全部消费者与迁移 | consumer matrix、旧格式回归、损坏/未知版本拒绝 |
| `L3` | 跨模块状态机、权威、信任、竞态、爆炸半径、失败封存与恢复 | 端到端来源追踪、真实负向、资源和清理证据 |

M11 登记的 `bootstrap_evidence.py`、`bootstrap_run.py` 与两个 M11 harness 体量债务在本阶段只评估
“是否混有多个所有者或存在真实变更风险”。若阶段边界清晰、失败矩阵充分且拆分没有行为收益，
保留为维护债；若确认耦合缺陷，先补 characterization 门禁，再提出最小拆分。

### 5.5 E：证据复核与结论

- 初始发现先用静态来源、现有自动化和只读探针交叉验证；
- 只有与发现相关的真实链路才进入 M13 定向运行，不提前重复 M14 全量矩阵；
- 每次整改只对应一个发现或一个不可分割的所有权接缝，提交意图保持单一；
- 修复后从受影响层级的最早门禁重跑，不能挑选旧绿色结果；
- 最终形成 M13 事实文档，明确已修复、延期、基线失效、未证明能力和 M14 可否进入。

## 6. 发现分类与记录格式

每个发现使用稳定 ID `FND-M13-NNN`，并记录：

- `severity`：`BLOCKER / MUST_FIX / DEFERRED`；
- `layer`：`L0 / L1 / L2 / L3`；
- 事实所有者、调用者、全部消费者和可达入口；
- 源码、测试或运行证据，以及为何不是单纯风格偏好；
- 数据/状态/资源流、失败出口、爆炸半径和安全影响；
- 最小整改、禁止范围、回归起点和基线是否失效；
- 修复提交、首次失败、最终结果和仍未证明的边界。

分类口径：

- `BLOCKER`：可破坏权威、裁决、不可变证据、安全边界、兼容、资源所有权或清理，阻止继续审查/交接；
- `MUST_FIX`：不改变冻结语义，但真实影响用户链、可维护性、发布一致性或可靠回归，M13 内必须关闭；
- `DEFERRED`：边界明确、没有当前可达缺陷，且整改风险高于收益；必须写所有者与重新触发条件。

“文件很长”“重复看起来多”“某个 warning 存在”本身不构成发现；必须证明所有权混淆、旁路、
缺失负向、资源泄漏、兼容风险或可观察用户问题。

## 7. 资源与执行纪律

- 16 GB Windows 主机默认严格串行；不得同时运行双 Python 全量、生产 Browser 与前端构建；
- Workbench 测试保持最多 2 workers；Browser 验收一次只启动一个服务/Context；
- 任何探针都使用显式端口、输出目录、超时与清理；不扫描或终止不属于 VeriTrail 的进程；
- 启动重型步骤前读取可用内存；持续低于 3 GiB 停止升级，低于 2 GiB 立即中止并保存事实；
- 网络依赖审计和远端读回与产品测试分开记录，代理或 registry 失败不能伪装产品失败；
- 生成证据进入忽略目录，最终提交前执行敏感、绝对路径、生成物和残留复核。

## 8. M13 出口门禁

只有以下事实同时成立，M13 才能交接 M14：

- 系统权威链、版本/消费者矩阵和状态/失败/恢复矩阵均已形成可核查记录；
- L0–L3 全部审查完成，已知 `BLOCKER = 0`、`MUST_FIX = 0`；
- 所有整改都有最小爆炸半径、受影响回归和适用真实链路证据；
- 若存在 L2/L3 语义变更需求，已停止 M13 静默整改并建立独立合同与基线处置；
- Python、Workbench、Schema/消费者、依赖、安全、Browser 和残留门禁按发现影响范围通过；
- M12 标签保持不动，工作树干净，本地与远端提交精确读回；
- README、架构、验收、里程碑与 M13 事实使用同一状态和能力边界。

M13 通过只表示当前实现没有遗留的已知系统/代码质量阻断项；它不等于 M14 的双目标终局复验，
不创建最终 Release，也不外推生产容量、跨平台或未支持执行模型。
