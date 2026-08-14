# 03. 验收标准

## 1. 证据状态

当前仓库处于 `v0 Implementation`。M0 只覆盖封存计划、结构化证据导入、确定性裁决和
证据包导出，并已独立冻结；M1 启动前资源预检、M2 有界真实浏览器证据与 M3 只读 Vue
证据工作台也已分别独立冻结。M4 本地 Run 目录与轻量自举已在干净实现提交上通过 SQLite、
本地 API、目录一致性、桌面/移动 UI、两阶段自举、敏感与清理验收并独立冻结。M5 内置静态
目标的有界运行编排也已通过代码、自动化、真实正/负 Chromium、资源决策、端口竞争、源变化、
Catalog/Workbench 和清理验收并独立冻结。M6 同计划复跑确定性比较也已通过双 Python、真实
三态 Comparison、逐字节复建、生产与 Codex 内置浏览器、资源、安全和清理终验并独立冻结。
M7 四角色配对/反事实分析也已通过双 Python、真实四角色三态、逐字节复建、损坏拒绝、
Catalog 隔离、生产与 Codex 内置浏览器、资源、安全和清理终验并独立冻结。每个里程碑只有代码、
自动化和适用的真实运行证据齐全后，才能独立冻结。

M8 全因子批次矩阵与固定种子扰动已 `FROZEN`：四个公共
Schema、两个 CLI、脱敏 2×2 矩阵、三态/污染/确定性/安全反例，以及四文件只读 Loader、矩阵/
wave/来源状态视图已经完成；8 个独立 M5 Run 的真实 2×2 批次、四类分析、确定性、反例与
批次清理已经验证。生产 Workbench 的 Codex 内置浏览器四态、损坏恢复、刷新/返回、桌面/移动
和 Console/Network 已验证，真实 Chromium 补证自动化键盘顺序与同源只读网络，人工系统键盘
最终在内置浏览器中证明焦点进入全因子矩阵；资源、安全、残留、提交与标签门禁均已完成。
M8 仍不证明真实并行、任意项目命令或完整自举。

M9 受控项目命令执行已 `FROZEN`：Plan 0.5、ToolBindings 0.1、CommandPreview 0.1、Windows Job
Object trusted process runner 与 `runtime.command` 已通过双 Python、Python/Node 真实命令、重复
Run、适用负向、桌面/移动 Chromium、Catalog/Workbench、内置浏览器物理键盘、资源、安全、清理
与 GitHub/tag 读回。它仍不证明 Shell、包管理器、长运行服务、完整自举、其他平台或不可信代码。

M10 有界完整项目自举与 M11 真实项目功能全链路均已 `FROZEN`，M12 为 `IMPLEMENTING`，M13–M14 为 `PLANNED`。M11 Contract 0.3 已冻结
`OPTION_B`、InkNarratives 精确 ref 和 Gate A -> Gate B 严格串行，并纠正 Plan/Profile 一对一绑定；
Profile 0.2、Plan 0.7、单节点生命周期和 collector 0.3 已通过 Gate A 的双 Python、真实 Chromium、
13 个预注册出口、Catalog/Comparison、资源、安全、清理与 Workbench 消费验证；真实项目 Gate B
Plan v1 首个 Run 已按 `COMPLETED/FAIL` 保留，Contract 0.4 的 Plan v2 随后严格串行取得
`PASS / FAIL / PENDING / PASS`，正向恢复 Comparison 为 `MATCH`、0 differences。生产 Workbench、内置
浏览器物理键盘、双 Python 277/277、优化模式验收门禁与零残留也已形成事实；冻结提交 `b13e2fb`
已推送；冻结读回时远端 `main` 与 `m11-v0.12.0^{}` 均精确指向该提交。准确矩阵与事实见文档
23、25、26、27。ProjectProfile 0.1、Plan 0.6
跨文档 seal、BootstrapPreview 0.1、Windows listener 表、逐节点长运行 Job、owned HTTP readiness、
双节点串行启动、pre-teardown fact-finalization 门禁和 best-effort 逆序清理已有代码与真实 helper
自动化；严格 `runtime.bootstrap`、
四个流附件、Plan/Profile Bundle、Catalog/Comparison 权威复核和 Pairing/Batch 显式拒绝也已有
自动化。内部 observed-run 已真实创建并核验 Run-owned work/staging，在 teardown 前落盘并读回
脱敏生命周期/流快照，teardown 后复核并释放，同时生成 subject 前后指纹和四方资源分账；成功、
subject 漂移不回滚、staging 失败仍逆序清理已有 Windows helper 自动化。公共 Plan 0.6 `run` 已在
Preview 精确审批和预检 `PROCEED` 后完成真实 Browser 正/负、确定性裁决、不可变 Bundle 与 Catalog
验真：正向为 `COMPLETED/PASS`，选择器业务失败为 `COMPLETED/FAIL`；预检
`STOP_ESCALATION/ABORT` 在零被测进程下生成仅含 preflight 的 `ABORTED/PENDING` Bundle，摘要不一致
仍在进程创建前拒绝且不生成 Run。dependency 提前退出和 application readiness 超时也已通过公共
`run` 形成严格的无 browser Bundle，分别得到 `NODE_EARLY_EXIT / COMPLETED/FAIL` 与
`READINESS_TIMEOUT / ABORTED/FAIL`；Catalog 接纳两者，并复核 browser 不适用、逆序清理与端口/staging
释放。application READY 后 user cancel 也已通过 cooperative event 和 CLI Ctrl+C/Ctrl+Break 桥接形成
`USER_CANCELLED / ABORTED/PENDING`，Browser 未启动、四流附件与 application→dependency 清理完整，
Catalog 验真通过。实时 Preview 通过后，dependency/application 端口分别被外部监听者抢占的公共
TOCTOU 场景也得到预检期 `ABORTED/PENDING`：runner 未启动，外部监听者未被接管或终止，Bundle 只含
preflight 且 Catalog 验真通过。dependency/application 的公共 listener owner mismatch 也均拒绝 READY，
外部进程按自身计划自然退出且未被 VeriTrail 终止，owned Job 随后逆序清理并形成
`LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL`；Catalog 接纳且无污染。相同 sealed Plan/Profile 已连续
完成两次 `COMPLETED/PASS` 公共 Run：权威与
Preview 一致，第一份 Bundle 未被覆盖，M6 Comparison 为 `MATCH`、0 差异且轮间无残留。第二类真实项目证明属于
M11。subject watch root 漂移的公共链路会保留用户修改、不执行回滚，并以
`BOOTSTRAP_SUBJECT_DRIFT` 把完整执行裁决为 `COMPLETED/INCONCLUSIVE`；该切片修复了 Evidence 已记录
漂移但旧 Verdict 仍错误 PASS 的消费者缺口。cleanup 观测注入失败时，应用节点失败不会跳过依赖
回收；公共 Bundle 形成 `CLEANUP_ERROR / ERROR/FAIL`，HARD cleanup 断言、污染检测与 Catalog 复算
一致。staging writer 显式失败时，生命周期在 teardown 前记录 `EVIDENCE_STAGING_FAILED`，随后完成
逆序清理并从内存中生成只能表达失败的 fallback `runtime.bootstrap`；公共 Bundle/Catalog 为
`EVIDENCE_ERROR / ERROR/PENDING`，普通未知 callback 异常不能走该路径。真实正向与预检停止 Bundle
已在同一 Catalog 中接纳，损坏副本被隔离；生产 Workbench 已由 Codex 内置浏览器经只读 API 读回
`runtime.bootstrap`，刷新后保持既有裁决且 Console/Warning 为零。完整功能矩阵因而闭环。其后的
M0–M10 地基审查已经修复 Catalog 报告重推导、READY 响应后 ownership 与只读 API 稳定读取三个
接缝，并完成双 Python 216/216 及前端门禁。其后的冻结候选严格串行轮已按预注册顺序通过所有公共
退出、双运行时、前端、依赖与生产 Workbench 正负 Run/刷新/返回/键盘/移动/Console/资源账册。其后
同一候选从 Wave A 完整重跑 16 GB 有界压力审计：同端口竞争安全拒绝错误 owner，独立度 1/2/3 为
6/6 `COMPLETED/PASS`，READY 后取消为 3/3 `ABORTED/PENDING`，1000 次回环请求零错误；最低可用内存
7323 MiB，11 个 Bundle/Catalog 独立验真且端口、进程、staging 回零。随后发布安全整改封闭 11 条
原攻击路径与 Job 内存硬限制，并从新候选完成严格串行 13/13、双 Python 228/228、Workbench 58/58、
最终压力、Codex 内置浏览器与零残留复验；`0084443` 和 `m10-v0.11.0^{}` 已从 GitHub 精确读回，
形成里程碑冻结事实。
冻结后地基纠偏又修复 Verdict 归因优先级、Browser 取消/所有权、运行期宿主机内存停止、阶段断言
适用性、Windows 瞬时目录锁和历史浏览器验收合同漂移；双 Python 262/262、Workbench 59/59、
1000 总请求、生产浏览器与清理门禁从新候选通过。首次补丁冻结读回时，GitHub `main` 与
`m10-v0.11.1^{}` 均精确指向 `f4efdd2`，当前 M10 地基基线更新为该补丁标签；旧
`m10-v0.11.0` 保持历史不动。
M10 的完整退出矩阵以
[独立 Contract 0.2](15-m10-bounded-project-bootstrap.md) 为准；已完成的审查见
[M10 动态地基系统与代码质量审查](17-m10-foundation-review.md)，已完成的串行轮见
[M10 第一轮严格串行完整复验](18-m10-serial-validation.md)，已完成的压力轮见
[M10 第二轮 16 GB 有界压力审计](19-m10-bounded-stress-audit.md)，整体顺序按
[M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md) 执行。双轮事实不能
替代最终发布回归、代码质量、安全、浏览器、残留与远端标签门禁。

## 2. v0 完整闭环

v0 必须以一个真实、轻量、非硬编码项目完成以下流程：

1. 创建 Subject、Baseline 和版本化 ExperimentPlan；
2. 定义一个主要变量、受控变量、负载语义、资源停止线和硬性不变量；
3. 运行启动前预检并记录环境指纹；
4. 执行确定性步骤，采集至少自动化与真实浏览器两层证据；
5. 记录 Console、Network、截图、资源和用户断言事实；
6. 检测变量漂移、证据缺口和批次残留；
7. 使用版本化规则计算 Verdict；
8. 导出 Markdown、JSON、证据清单和哈希；
9. 使用相同计划与种子复跑，比较基线和新 Run；
10. 清理本轮资源，并证明下一轮未被污染。

任何一步只能由手工拼报告完成，都说明产品闭环尚未成立。

## 3. 控制变量验收

必须提供可重复测试证明：

- 单变量计划接受并保留完整变量来源；
- 两个未声明主要变量会被拒绝或裁决为 `INCONCLUSIVE`；
- 显式组合实验要求组合矩阵与对应基线；
- 受控变量漂移进入报告并影响可比较性；
- 未知变量默认阻断因果 `PASS`；
- 随机顺序保存种子，相同种子可以重建相同计划顺序；
- 确定性覆盖矩阵未完成时，随机运行不能补写为覆盖完成；
- 上一批残留被发现时，下一批默认不开始或结果为 `INCONCLUSIVE`。
- 首次运行前计划被封存并哈希，运行后修改断言或停止线会产生新版本；
- 重复组保留全部计划内运行，不能只挑选最优结果；
- 配对实验能够表达基线、处理和恢复基线，且保留顺序与预热事实；
- 负对照不应产生处理效果，否则结论进入 `INCONCLUSIVE`。

## 4. 负载与资源验收

- 模型拒绝或警告没有单位与形态的“并发”数字；
- 虚拟用户、在途请求、请求总数、RPS、热点竞争、连接数和消息速率可分别表达；
- 阶梯负载每一级都能关联资源快照和不变量检查；
- 软阈值停止升压，硬阈值中止运行并保存现场；
- `ABORTED` 不自动变成 `FAIL`，也不能变成 `PASS`；
- 工具自身资源与被测对象资源分开记录；
- 采样率与采集器开销进入环境事实，超出容差时阻止无条件性能 `PASS`；
- 批次结束验证进程、端口、连接和临时数据释放；
- 报告声明硬件、拓扑、版本、数据规模和负载适用边界。

## 5. 故障与恢复验收

通用模型能够表达并区分：完全不可用、变慢、间歇失败、结果未知和恢复重放。

至少一个自举场景应证明：

- 失败注入参数进入主要变量或组合矩阵；
- 运行中止前保存时间线和已取得证据；
- 重试不会让同一步骤静默产生重复证据或重复副作用；
- 恢复后重新检查退出条件，而不是只检查服务“重新在线”；
- 不能确定操作是否完成时报告结果未知，不把超时直接解释为失败。

## 6. 浏览器验收

- 使用真实 Chromium 操作用户入口和关键步骤；
- 捕获 Console、Network、截图、视口与步骤时间线；
- 未解释的 JavaScript 错误、请求失败、4xx/5xx 和重复写请求进入断言；
- 至少覆盖桌面和移动关键视口，检查横向溢出；
- 只读工作台必须用 Codex 内置浏览器再次完成正向、负向、损坏包重试、本地目录导入、键盘
  与截图链路，并检查页面实际 Console、Network、同源资源和未解释 4xx/5xx；
- 需要角色隔离时使用独立 Browser Context；
- Mock、组件测试、构建成功和截图不能替代真实交互与网络证据；
- 敏感请求头、Cookie 和正文不会出现在持久化报告中。

## 7. 证据与报告验收

- 所有证据进入不可变清单并计算 SHA-256；
- 解析后的事实可追溯到原证据、采集步骤和解析器版本；
- 同一 Run 的证据不能静默覆盖；
- 缺失必需证据产生 `PENDING`；
- 证据冲突、变量污染或无效基线产生 `INCONCLUSIVE`；
- 硬性不变量失败产生 `FAIL`，且不能被体验评分抵消；
- `PASS` 报告包含基线、变量、边界、种子、证据、断言、清理与复现方法；
- Markdown 与 JSON 对同一裁决给出一致结果；
- 导出包通过敏感信息扫描。

## 8. 安全验收

- v0 不执行任意 Shell 字符串；
- 本地 API 默认只监听回环；
- 路径穿越、恶意文件名和导入 HTML 不导致代码执行；
- 浏览器端证据包在显示前核对清单路径、大小、SHA-256 和交叉引用；失败包不泄露部分可信状态，
  已创建的对象 URL 在切换、卸载或后续校验失败时释放；
- 日志与 HAR 默认脱敏认证材料；
- `.env`、密钥、浏览器 Profile 和系统凭据不进入证据包；
- 资源采集与浏览器步骤有超时、取消和清理路径；
- AI 功能缺席不影响裁决，未来加入也不能修改最终 Verdict。

## 9. 自举与跨项目证明

首个自举对象优先选择轻量静态/前端项目，以便在 16 GB 机器上反复跑通完整闭环。
随后至少用第二个不同类型对象证明核心没有绑定第一个项目。

PlainJournal 可以在后续作为复杂参考案例，用于验证批次 Profile、故障分类、负载语义和最终
一致性适配能力；它不是 v0 的依赖，也不能成为核心 schema 的业务模板。

## 10. 分层代码审查验收

- 计划必须声明 `L0/L1/L2/L3` 影响层级、所有者和预期爆炸半径；
- 只改文案/样式的 L0 不被迫启动无关后端多实例，但必须完成真实浏览器验收；
- L1 不能触及公共契约；一旦触及则自动升级到 L2；
- L2 必须枚举全部已知消费者、兼容策略和契约回归；
- L3 必须覆盖状态机、数据所有权、一致性、安全、故障与恢复等适用系统证据；
- 实际 diff 或运行事实超出声明范围时产生范围漂移，不允许低层结论继续 `PASS`；
- 局部需求使用全局修改时，报告必须解释必要性并验证全部下游，不能以“改动行数少”降级审查。

## 11. 里程碑门禁验收

- 后继里程碑可以创建 `PLANNED` 文档，但前置里程碑未闭环时不能进入实现；
- `IMPLEMENTED`、`AUTOMATED` 和 `RUNTIME_VALIDATED` 不得混为“完成”；
- 只有真实运行、不变量、恢复、清理和证据包满足退出条件后才能 `FROZEN`；
- 前置里程碑为 `PENDING`、`FAIL` 或 `INCONCLUSIVE` 时，后继实现入口被硬阻止；
- 硬件资源不足不会自动豁免门禁；只能等待资源、缩小同一里程碑的实验批次或补充证据；
- 修复前置里程碑后重新冻结基线，后继计划必须引用新基线并检查是否需要重审。
- 代码、配置、依赖、数据、拓扑或规则越过容差时旧基线变为 `EXPIRED`，历史 `PASS` 不自动继承。

## 12. 发布门禁

首个实现版本发布前必须：

- 文档、schema、代码和 UI 使用相同状态与裁决语义；
- 自动化测试、静态检查和安全检查通过；
- 在干净工作区完成真实浏览器自举验收；
- 完成一次资源中止、一次变量污染和一次硬不变量失败的负路径；
- 导出并复核脱敏证据包；
- 在内置浏览器中检查公开 README、安装路径和演示链路；
- 不把尚未验证的多实例、数据库或 AI 能力写入已完成功能。

前端表现系统重构是收尾阶段：先证明产品闭环、证据与裁决成立，再调整信息空间、交互与视觉语言；
不得借表现重构顺手改变实验语义、数据所有权或安全边界。
