# VeriTrail 项目指令

## 当前阶段

- 当前阶段是 `v0 Implementation`。M0 已在提交 `64497779add1351014d802b38d46f73a4ce394ac`
  上冻结；M1 已在提交 `21d555cf1a8d5b4f3bc9430b4241c3f70ff0d48f` 上通过两套 Python、
  M0 兼容、三类真实预检、证据包哈希、敏感扫描和残留检查并标记 `FROZEN`；M2 已在提交
  `3db07aa284e16db2afe3b84136371f35ec2091fc` 上通过两套 Python、真实 Chromium 正/负链路、
  Codex 内置浏览器、附件哈希、敏感扫描和残留检查并标记 `FROZEN`；M3 已在提交
  `ef2a8d64f781ba61bf7fbd9c1511a3419a6cfbaa` 上完成只读 Vue 工作台，并通过前端自动化、两套
  Python 兼容回归、真实 Chromium、Codex 内置浏览器、同源网络、依赖审计和残留检查，标记
  `FROZEN`。M4“本地 Run 目录与轻量自举”已在实现提交
  `ddcfa314b40bf9ba3332fec1e190e6335a4c1502` 上完成离线 Bundle 校验、SQLite 派生索引、固定
  回环只读 API、Catalog UI 和两阶段轻量自举，并通过双 Python、真实 Chromium、Codex 内置
  浏览器、敏感与残留复核，标记 `FROZEN`。Plan v1 的选择器歧义失败 Run 必须继续保留。
  M5“有界运行编排与静态目标生命周期”已在实现提交
  `98d3b69798e278da7603ea0ce04c39607e3a6407` 上完成 Plan 0.4、内置只读 `STATIC_HTTP`、
  `runtime.orchestration` 与 `run` CLI，并通过双 Python、真实正/负 Chromium、ABORT/STOP、
  端口竞争、源变化、Catalog/Workbench、Codex 内置浏览器、敏感与残留复核，标记 `FROZEN`。
  首个查询参数 400 失败 Run 必须继续保留。M6“同计划复跑确定性比较”已在实现提交
  `1a5eeaa6b5516c5b53248411e1284f6a2568e5e2` 上完成 Core/CLI、Comparison 0.1 与
  Workbench，并通过双 Python、真实三态 Comparison、逐字节复建、生产与 Codex 内置浏览器、
  资源、安全和清理终验，标记 `FROZEN`。损坏 Comparison 与预览端口残留反例必须继续保留。
  M7“预注册四角色配对反事实分析”已在合同提交 `7daf3b4`、实现提交 `9046f25` 与本地文件
  导入修复 `c726fe8` 上完成 PairingPlan/PairedAnalysis、CLI 与 Workbench，并通过双 Python、
  真实四角色三态、逐字节复建、来源损坏拒绝、Catalog 隔离、生产与 Codex 内置浏览器、资源、
  安全和清理终验，标记 `FROZEN`。目录选择器在内置浏览器中不触发导入的失败事实与改成显式
  四文件导入的修复必须继续保留。计划编辑、任意项目命令和完整自举仍未实现。
  M8“预注册全因子批次矩阵与固定种子扰动”已在合同 `b1ca45b`、Core `0510915`、Workbench
  `a067f4c`、真实批次 `5caee26` 与浏览器终验 `ba77feb` 上完成四个公共 Schema、两个 CLI、
  BatchAnalysis 四文件 Loader 和只读矩阵/wave 视图，并通过双 Python、8 个独立 M5 Run、四类
  分析、确定性/反例、生产及 Codex 内置浏览器、人工系统键盘、资源、安全和清理终验，标记
  `FROZEN`。裸静态服务的 Catalog 404 失败事实、内置浏览器合成 `Tab` 限制、真实 Chromium
  自动化补证与内置浏览器人工 `Tab` 通过事实必须继续保留。
- Post-M8 收束路线 Plan v1 位于 `docs/13-post-m8-roadmap.md`，已以 `post-m8-plan-v1` 冻结为
  规划基线。M10、M11 已冻结，M12–M14 仍为 `PLANNED`；冻结合同不代表
  后继能力已经实现或验收。
- M9 独立合同 0.2 位于 `docs/14-m9-controlled-command-execution.md`，已在 `290b618` 进入
  `IMPLEMENTING`；`4d2bc84` 完成 Plan 0.5、ToolBindings 0.1、CommandPreview 0.1 与
  `command-preview` CLI，`9f979c8` 完成锁定 `pywin32==312` 的 Windows Job Object 所有权后端和
  真实 helper 自动化，`fa27b51` 完成 Plan 0.5 `run` 与严格 `runtime.command`，`9031719` 新增
  两个独立轻量 Subject 和真实 Python/Node 正负矩阵。冻结提交 `3181d69` 已通过真实命令、重复 Run、
  适用负向、双视口 Chromium、Catalog/Workbench、Console/Network、内置浏览器物理键盘、双 Python/
  前端回归与最终清理，并已从 GitHub 读回 `main` 和 `m9-v0.10.0` 标签，状态为 `FROZEN`。M9 仍只
  允许一个可信、直接启动、无 Shell、无 stdin/TTY 的 `ONESHOT` 进程；不得顺手加入服务、
  自举、包管理器或前端控制台，也不得把结构化 runner 描述成文件系统、网络、TOCTOU 或恶意代码沙箱。目标
  标签 `m9-v0.10.0` 必须继续指向 `3181d69`；越过合同边界时必须开启后继里程碑而不是改写该基线。
- M10 独立 Contract 0.2 位于 `docs/15-m10-bounded-project-bootstrap.md`。冻结提交
  `008444319a4af54de3291fe5c0ab602001c30754` 已完成公共退出矩阵、M0–M10 地基与安全审查、严格
  串行、双 Python 228/228、Workbench 58/58、16 GB 有界压力、Codex 内置浏览器与零残留复验；
  冻结读回时 GitHub `main` 和 `m10-v0.11.0^{}` 均指向该提交。冻结后地基纠偏已在实现提交
  `f4efdd25c50b19077c61994bce3e2aca5244d5ec` 完成双 Python 262/262、Workbench 59/59、公共出口、
  16 GB 有界压力、生产浏览器与清理复验；首次补丁冻结读回时，GitHub `main` 与
  `m10-v0.11.1^{}` 均指向该提交，当前 M10 地基状态为 `FROZEN`。`m10-v0.11.0` 和
  `m10-v0.11.1` 均不得移动。M10 只证明 Windows 11、
  `C1 PROCESS_COLD`、一个 Run-owned dependency、一个 application、
  `HTTP_GET_LOOPBACK_OWNED_PID` readiness、既有 Browser Adapter 与逆序 Job 清理；C0 接管、
  C2/C3、Docker、跨平台、包管理器、第二类真实项目、不可信代码隔离和优雅停机均未证明。不得把
  M10 冻结解释为允许跳过后继合同。
- M11 只读候选盘点与探索探针位于 `docs/22-m11-real-project-suitability-and-contract-draft.md`。探针已
  证明现有候选不能直接装入 M10 两节点边界，并证明 InkNarratives 原始目录的单节点 HTTP/代表页
  浏览器形态真实可运行。用户已确认 `OPTION_B`、精确 ref、Gate A -> Gate B 严格串行和不适用项；
  `docs/23-m11-single-node-real-project-contract.md` 的 0.2 已在 `eb39c0a` 留下历史，Contract 0.3
  纠正 Plan/Profile 一对一权威绑定，当前 Contract 0.4 只版本化 Gate B 的响应式交互纠偏。Gate A 已完成 Profile 0.2、Plan 0.7、单 APPLICATION、
  collector 0.3、双 Python、真实 Chromium、13 个预注册出口、Catalog/Comparison、资源、安全、
  清理与 Workbench 验证，事实见 `docs/25-m11-gate-a-validation.md`。Gate B Plan v1 已在预注册提交
  `2c14393` 后启动；首个正向 Run 因移动视口长卷导航隐藏而
  得到 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`，失败目录
  `tmp/m11-gateb-contract03-20260814-160143` 必须保留，后续三个 v1 Run 未启动。Contract 0.4 将两个
  Gate B Plan 升为 version 2、保留 Profile v1 与全部资源/裁决边界，并使用新 Run ID；v2 已严格串行
  取得 `PASS / FAIL / PENDING / PASS`、Comparison `MATCH`、Catalog/Workbench、内置浏览器物理键盘、
  双 Python 277/277 与零残留事实。系统审查修复了 Workbench 验收脚本在 `python -O` 下会移除关键
  `assert` 的门禁缺陷；优化模式完整 Workbench 复跑通过。冻结提交
  `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40` 已推送；冻结读回时远端 `main` 和
  `m11-v0.12.0^{}` 均精确指向该提交，M11 状态为 `FROZEN`。事实见文档 26、27；M12–M14 仍为
  `PLANNED`。
- M11 入口治理与 M0-M10 当前复验位于 `docs/24-m11-entry-governance.md`。它保留首次 Python 3.10
  Chromium 瞬态失败以及后续双解释器完整全绿事实，只允许继续入口枝叶整理；它不证明 M11 已实现。
- M12 表现系统重构设计计划 0.1 位于 `docs/28-m12-palace-workbench-design-plan.md`，当前状态为
  `DESIGN_FROZEN / PRODUCTION_IMPLEMENTATION_NOT_STARTED`。它把 M11 冻结界面作为控制组，允许 `L0 + bounded L1`
  的信息空间、十字中轴导航和表现组件重构，但禁止触及任何 L2/L3 数据、裁决或安全合同。用户确认并
  形成的本计划提交必须先于生产代码。M12-A 控制组审计已在
  `docs/29-m12-a-control-baseline-audit.md` 闭环：`web/` 与 M11 标签 tree 一致，60/60 前端测试、lint、
  type-check、production build、最终 Gate B 自动 Chromium、内置浏览器状态矩阵、计划视口控制组和零残留均有
  事实；它没有修改生产前端，也不表示 M12 已实现。下一入口只允许 M12-B 无装饰信息架构与十字导航
  骨架，不得跳到主题色、Catalog 视觉终稿、版本或 M12 标签。
- 开始工作前依次阅读 `README.md`、`docs/00-product-brief.md`、`docs/01-evidence-model.md`、`docs/02-architecture.md` 和 `docs/03-acceptance.md`。
- 产品事实与代码不一致时先停止并指出冲突；不得静默降低方法论或安全边界。

## 核心原则

- 控制变量法是产品核心：一个可归因实验只能有一个主要变量。其他变量必须冻结、记录为受控变量，或明确列为干扰/未知变量。
- 单变量证明因果，组合批次验证交互，固定种子随机扰动寻找偶发故障，代表性全链路形成系统级结论。
- 运行状态与验收结论分离。资源中止使用 `ABORTED`；证据不足使用 `PENDING`；变量污染或无法归因使用 `INCONCLUSIVE`；不得借硬件限制伪造 `PASS/FAIL`。
- 吞吐目标可以受资源限制，一致性、安全和其他硬性不变量不能降级。
- 实验开始前冻结计划、断言、停止线和裁决规则。观察结果后若需修改，创建新计划版本并保留旧运行，不得移动原实验的判定标准。
- 重要结论应支持重复、配对或反事实复跑；验迹自身的 CPU、内存、连接和采样开销与被测对象分开记录。

## 开发与资源边界

- 优先建立最小纵向闭环，再扩展适配器；不要先堆积导入器、仪表盘或中间件集成。
- 16 GB Windows 主机默认串行或受限微并行。测试必须有启动前资源预检、软/硬停止线、现场保存和批次清理确认。
- v0 架构规划使用 Python Core、SQLite、Vue Workbench 和 Playwright/CDP；当前冻结基线已包含
  Python Core、可重建 SQLite Catalog、固定回环只读 API、Vue Workbench 与 Playwright/CDP。
  不要求 Docker、MQ、搜索或外部云服务。
- M3 Workbench 只读消费 Report/Evidence/Manifest 和浏览器附件，不在前端重新裁决，不修改
  M0–M2 Schema；M3 本身不包含 SQLite、本地 API 或自举闭环，这些由 M4 独立合同交付。
  不能把 M3/M4 的只读 UI 与轻量自举当成计划编辑或执行编排已经完成。
- M4 必须保持 Bundle 为权威事实、SQLite 为可重建派生索引、服务为固定回环只读
  API；不得在该里程碑加入在线写、文件监视、跨 Run 差异、任意命令或被测对象生命周期管理。
- M5 冻结基线只允许 Core 内置的 `STATIC_HTTP` 目标适配器；不得扩大为任意 Shell、外部
  可执行文件、npm/Maven、Docker、中间件或项目服务生命周期管理。Plan 0.4 必须向后兼容，
  所有异常路径先清理再形成证据，定义和自动化都不得冒充真实运行。
- M6 冻结合同只比较两个不同 Run ID、同 sealed Plan 的不可变 Bundle，生成独立 Comparison
  Bundle；不得修改来源 Verdict、自动挑选成功 Run、把 Comparison 写进 M4 Run-only Catalog，
  或把同计划复跑一致性扩张为处理组因果结论。
- M7 冻结合同固定 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL` 四角色，
  新增独立 PairingPlan/PairedAnalysis；不得修改 M0–M6 契约、删减不利角色、把配对结果写成
  来源 `PASS/FAIL`，或扩大为统计显著性、组合变量与任意执行器。
- M8 冻结合同使用独立 BatchPlan/BatchAnalysis 表达 4–16 格全因子 Profile；确定性 coverage
  必须先完成，seed 只能改变 perturbation 顺序，不能改变成员或补写缺格。M8 不执行来源 Run、
  不证明真实并行，不把 Profile 信号写成组件级因果或来源 `PASS/FAIL`。
- v0 不接受任意 Shell 字符串执行。若未来引入命令执行，必须采用结构化参数、显式预览、最小权限和可审计允许列表。
- M9 Windows 进程后端锁定为项目虚拟环境内的 `pywin32==312` 可选依赖；只能在实施时显式安装到
  Git 忽略的项目虚拟环境，不得自动安装、全局安装、运行 `pywin32_postinstall`，也不得在缺失时
  降级为 `ctypes`、普通 `Popen` 或 PID/进程名轮询。
- 不记录或提交 `.env` 值、令牌、Cookie、Authorization 头、私钥、个人路径或原始敏感业务数据。采集器必须默认脱敏。

## 分层审查与里程碑门禁

- 变更开始前必须声明影响层级：`L0 表现层`、`L1 组件内部`、`L2 公共契约`、`L3 系统级`。实际 diff 越界时立即升级审查与验收范围。
- 局部需求不得顺手修改全局序列化、共享配置、公共 Schema、通用中间件、状态机、安全或数据所有权。确需修改时，列出全部消费者、兼容策略和回归矩阵。
- 审查先确定所有者、调用者、数据流、失败边界和爆炸半径，再讨论实现细节；避免用全局改动解决局部问题。
- 里程碑可以提前规划，但前一里程碑没有完成代码事实、自动化证据、真实运行证据并冻结为可寻址基线前，不得开始下一里程碑的实现。
- 资源不足导致前一里程碑最终验收 `PENDING` 时，下一里程碑继续保持 `PLANNED`；不得把未闭环问题向后传递。
- 代码、配置、依赖、数据或拓扑越过基线容差后，旧结论标记过期并重新验收；不得把历史 `PASS` 自动继承给新版本。

## 验收门槛

- 单元测试、静态检查和 Mock 只算自动化证据，不能替代真实浏览器与真实运行证据。
- 浏览器能力必须检查 Console、Network、关键交互、失败重试、桌面/移动视口和未解释的 4xx/5xx。
- 涉及多实例、幂等、消息、缓存或最终一致性时，必须核对权威事实、重复副作用、故障恢复和退出条件。
- 每个证据文件都应进入清单并计算哈希；报告必须能追溯到代码版本、环境快照、实验计划和随机种子。
- 无法完成最终验收时，明确标记 `PENDING`，不要用“实现完成”冒充“产品完成”。

## Git 与文档

- 保持提交单一意图，提交前检查 `git diff --check`、敏感信息和生成物。
- `artifacts/`、本地数据库、浏览器 trace/HAR、截图和运行日志默认不提交；只有经过脱敏的最小夹具可进入仓库。
- 修改模型或结论语义时同步更新全部相关文档，并写明迁移或兼容边界。
