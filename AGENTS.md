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
  自动化补证与内置浏览器人工 `Tab` 通过事实必须继续保留。计划编辑、任意项目命令、真实并行
  和完整自举仍未实现。
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
