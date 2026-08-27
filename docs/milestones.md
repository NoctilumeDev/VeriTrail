# VeriTrail 里程碑冻结历史

## 1. 用途

本文件承接 README 不再展开的 M0–M14 冻结历史。它记录每个冻结基线回答的问题、真实取得的
证据、明确没有证明的能力，以及必须继续保留的失败事实。

里程碑标签实际指向的 Git 提交是版本寻址权威；实现提交、合同提交、运行哈希和完整退出条件
仍以对应的里程碑文档为准。M0–M9 已于 2026-08-11 从 `origin` 核验；M10 当前补丁基线与 M11
冻结基线于 2026-08-14 核验；M12 冻结基线于 2026-08-22 核验；M13 与 M14 最终发布基线于
2026-08-23 核验。

## 2. 冻结与当前路线索引

| Milestone | Capability | Status | Frozen ref |
| --- | --- | --- | --- |
| M0 | 封存单变量计划、结构化证据、确定性 Verdict 与开放报告 | `FROZEN` | `m0-v0.1.0` @ `6367843` |
| M1 | 启动前资源采样、`PROCEED / STOP_ESCALATION / ABORT` | `FROZEN` | `m1-v0.2.0` @ `a9b795e` |
| M2 | 回环站点的有界 Chromium、Console/Network/截图证据 | `FROZEN` | `m2-v0.3.0` @ `fbaaf71` |
| M3 | 本地只读 Vue Workbench 与“宫阙验迹”CSS 主题 | `FROZEN` | `m3-v0.4.0` @ `e46f633` |
| M4 | 可重建 SQLite Run Catalog、只读 API 与轻量自举 | `FROZEN` | `m4-v0.5.0` @ `d095057` |
| M5 | `STATIC_HTTP` 目标的有界生命周期与单一 `run` 入口 | `FROZEN` | `m5-v0.6.0` @ `d3b9cd7` |
| M6 | 同 sealed Plan 的不可变 Run 确定性比较 | `FROZEN` | `m6-v0.7.0` @ `807ef1e` |
| M7 | 固定四角色、预注册 outcome 的配对反事实分析 | `FROZEN` | `m7-v0.8.0` @ `e5c6e27` |
| M8 | 4–16 格全因子 Profile 与固定种子扰动分析 | `FROZEN` | `m8-v0.9.0` @ `c6fbd73` |
| M9 | 可信一次性项目进程的受控执行与证据闭环 | `FROZEN` | `m9-v0.10.0` @ `3181d69` |
| M10 | Windows 11/C1 有界完整项目自举 | `FROZEN` | `m10-v0.11.1` @ `f4efdd2`；历史 `m10-v0.11.0` @ `0084443` |
| M11 | 不同类型真实项目功能全链路 | `FROZEN` | `m11-v0.12.0` @ `b13e2fb` |
| M12 | 故宫主题前端终稿 | `FROZEN` | `m12-v0.13.0` @ `5f32c33` |
| M13 | 系统思维与分层代码质量终审 | `FROZEN` | 计划/事实：文档 52、53；实现 `63e6354` |
| M14 | 整改后终局复验与发布收束 | `FROZEN / RELEASED` | `v0.12.0`；合同/整改/事实：文档 54–57 |

`FROZEN` 只对该行声明的能力和对应文档中的环境、输入、资源及安全边界成立。代码、依赖、
Schema、数据、拓扑、浏览器或规则越过容差时，旧结论必须标记过期并重新验收。

## 3. 证据与边界

| Milestone | 真实取得的关键证据 | 明确没有证明 |
| --- | --- | --- |
| M0 | 双 Python 自动化、5 个真实 CLI Run、四类 Verdict、证据包与清单哈希 | 资源、浏览器、数据库、组合矩阵或项目执行 |
| M1 | 三类真实预检、M0 兼容、资源中止与观察者开销 | 工作负载执行、运行中监控或自动清理外部服务 |
| M2 | 正/负真实 Chromium、Codex 内置浏览器、附件哈希与清理 | 被测站点生命周期、远程认证或并行 Context |
| M3 | 生产构建、桌面/移动、正负/损坏包、本地导入与同源网络 | SQLite、API、计划编辑、执行编排或完整自举 |
| M4 | Catalog 确定性重建、只读 SQLite/API、两阶段自举与源变化隔离 | 跨 Run 比较、任意被测对象启动或通用元数据写模型 |
| M5 | 正/负真实 Run、ABORT/STOP、端口竞争、源变化与目标清理 | Shell、npm/Maven、Docker、真实后端或中间件编排 |
| M6 | `MATCH / DRIFT / INCONCLUSIVE`、逐字节复建与来源损坏拒绝 | 处理效果、跨变量因果、自动挑选 Run 或统计结论 |
| M7 | 四角色三态、恢复基线、负对照、Catalog 隔离与浏览器验真 | 组合变量、统计显著性、任意配对或跨批次聚合 |
| M8 | 8 个独立 M5 Run、四类批次状态、固定种子、来源 `FAIL` 保留与人工键盘终验 | 组件级多变量因果、真实并行、生产容量或任意项目命令 |
| M9 | Python/Node 可信命令、重复 Run、非零/超时/漂移/后代负向、Job 回收、双视口、人工键盘与远端读回 | Shell、包管理器、服务、其他平台、不可信代码隔离或完整自举 |
| M10 | 双节点长运行 Job/readiness/逆序清理、严格 `runtime.bootstrap` 四附件、Run-owned staging、subject 指纹/资源分账、真实 Browser、完整公共退出矩阵、重复/竞争/漂移/故障封存、Catalog/Workbench 读回、地基与安全整改、同候选严格串行复验、独立度 1/2/3、取消交错、1000 总请求压力审计及远端读回 | 正式通用并行、生产容量、第二类真实项目、C2/C3、Docker、跨平台或不可信代码隔离 |
| M11 | Profile 0.2 / Plan 0.7 单 application、13 个 Gate A 公共出口、InkNarratives 精确 ref 四 Run、真实双视口 Chromium、v1 失败保留、恢复 Comparison `MATCH`、Catalog/Workbench、物理键盘、双 Python 与零残留 | 动态后端、数据库/中间件、多角色、多实例、最终一致性、C2/C3、Docker、跨平台或不可信代码隔离 |
| M12 | 156/156 Workbench、双 Python 278/278、D1/D2/D3、两轮 13 项生产 Chromium、636 个同源只读请求、桌面/390/360 px、内置浏览器、逐页用户确认、零外网/写请求/HTTP 错误与零残留 | 新后端、Schema、执行器、裁决能力、跨平台、生产容量、M13 代码质量结论或 M14 最终发布 |
| M13 | 权威/消费者/失败/恢复矩阵、双 Python 279/279、Workbench 156/156、常规/优化两轮 13 项/636 请求、标准安全扫描、依赖审计、真实空态 Browser、四项整改与零残留 | M14 双真实目标终局复验、最终版本/Release、生产容量、C2/C3、Docker、跨平台、恶意代码隔离或新增能力 |
| M14 | 双 Python 318/318、Workbench 171/171、wheel/sdist 独立安装运行、Release ZIP 63/63、双真实目标常规/优化复验、桌面/390/360 px 内置浏览器、375 文件/12 攻击面零发现、安全/依赖/资产/远端读回与零残留 | 生产容量、C0/C2/C3、Docker、跨平台、多服务、恶意代码隔离、通用脚手架、AI 裁决或新增能力 |

M8 的 wave 仍由验收脚本串行执行，冻结结论固定为
`runtime_overlap_claim=NOT_PROVEN`。它证明有界调度、Assignment 和分析语义，不证明同一 wave
中的 Run 曾经真实时间重叠。

## 4. 必须保留的失败事实

这些反例是冻结证据的一部分，不能在整理历史或美化演示时删除：

- M4：自举 Plan v1 的 `PASS` 选择器同时匹配目录卡片与详情状态门；失败 Run 保留，Plan v2
  只收窄选择器后重新验收；
- M5：首轮合法 query 被错误裁为 400；合同没有后移，修复为文件查找忽略 query、账册只保存
  脱敏 path，并保留原失败 Run；
- M6：损坏 Comparison 与预览端口残留用于证明输出隔离和清理门禁；
- M7：目录选择器在 Codex 内置浏览器中没有触发导入；入口改为显式选择四个文件，失败事实
  与修复后的终验同时保留；
- M8：第一次用裸静态服务器启动 Workbench 产生 `/api/v1/catalog` 404，该轮被判失败并丢弃；
  生产 `catalog-serve` 重跑后才形成浏览器证据。内置浏览器控制面不能合成 `Tab`，最终由真实
  Chromium 自动化和用户在内置浏览器中手动按一次系统 `Tab` 共同完成键盘验收；
- M9：`r1` 错把非秘密 Authorization 字段名也当作必须消失，`r2` 读取了错误的 Comparison 字段；
  两轮均停止并以新目录完整复跑。浏览器服务的 Windows venv launcher/基础解释器在终端中断后曾
  残留，最终按 PID、父子关系和完整命令核验后清理，并以端口与进程残留为 0 作为退出事实。
- M11：Gate B Plan v1 在移动长卷页引用了隐藏导航，首个正向 Run 得到 `COMPLETED/FAIL`，后续 v1
  Run 未启动；Contract 0.4 只升 Plan 版本并使用新 Run ID。两次 Gate B v2 验收器失败和首次 Python
  3.13 Playwright 关闭警告均保留。长卷页约 1280px 时已有 13px 根级测量溢出，归为目标 L0 延期，
  不修改固定 Subject ref，也不倒填为预注册 1440/390 的失败。

## 5. 当前能力边界

M0–M12 已冻结的是一条逐层增长的本地验收链：

```text
Plan / Evidence / Verdict
  -> Resource preflight
  -> Browser evidence
  -> Read-only Workbench
  -> Local Run Catalog
  -> Bounded static target lifecycle
  -> Deterministic rerun comparison
  -> Four-role paired analysis
  -> Full-factorial batch analysis
  -> Controlled trusted one-shot process
  -> Windows/C1 bounded two-node project bootstrap
  -> Windows/C1 bounded single-application real-project validation
  -> Frozen Palace Evidence presentation system
```

当前仍未实现：

- 计划编辑器与在线写；
- 任意或不可信项目命令、Shell、npm/Maven、Docker 或中间件生命周期；
- wave 内真实微并行执行；
- C2/C3、Docker、跨平台与不可信代码隔离；
- 统计显著性、生产容量结论和 AI 裁决。

后继里程碑可以提前规划，但只有当前冻结标签仍有效、且新实现没有越过其兼容容差时，才能
消费这些基线。发现范围上浮时必须回到所有者、消费者和证据矩阵重新评审。

后继阶段的 [Post-M8 收束路线 Plan v1](13-post-m8-roadmap.md) 已以
`post-m8-plan-v1` 冻结为规划基线；M10–M14 均已冻结。M13 事实见文档 53；M14 已按文档
54–57 完成安全整改、双目标终局复验、稳定 `0.12.0` 与首个最终 Release。M9 受控
项目命令执行合同 0.2 已在
`290b618` 进入 `CONTRACT_FROZEN`；`4d2bc84` 完成 Plan 0.5、ToolBindings 0.1、CommandPreview 0.1
与只读 CLI，`9f979c8` 完成锁定 `pywin32==312` 的 Windows Job Object 所有权后端和真实 helper
自动化，`fa27b51` 完成 Plan 0.5 `run`、严格 `runtime.command`、最终状态漂移阻断、文本附件
脱敏和 Bundle/Catalog/API/Workbench 通用读回自动化。`9031719` 新增两个独立轻量 Subject 与真实
验收矩阵；Python module、直接 `node.exe` script、重复 Run、适用负向、桌面/移动 Chromium、
Catalog/Workbench、Console/Network、双运行时回归、内置浏览器物理键盘和最终清理均已通过。
冻结提交 `3181d69` 及 `m9-v0.10.0` 标签已从 GitHub 远端读回，M9 在合同边界内标记 `FROZEN`。
M10 已按 Contract 0.2 实现 ProjectProfile 0.1、Plan 0.6 跨文档 seal、BootstrapPreview 0.1 与只读
Windows IP Helper listener 表，并已加入每节点独立长运行 Job、owned HTTP readiness、双节点严格
串行启动和 best-effort 逆序清理组件。当前新增严格 `runtime.bootstrap` 构造/校验与固定四流附件，
Plan 0.6 Bundle 同时封存 Profile，Catalog/Comparison 复核权威身份，Pairing/Batch 显式拒绝 0.6。
内部 observed-run 还拥有并释放 work/staging、封存并读回 teardown 前脱敏事实与流快照、比较 subject
指纹并分账四方资源。冻结的 M2 Browser Adapter 已在两节点 READY 后生成真实 `browser.session`，并由
M10-only CDP observer 以内存态进程 handles 分账 Chromium RSS、确认关闭；真实双视口正向与选择器
失败负向均完成逆序清理。公共 Plan 0.6 `run` 已在审批与预检 `PROCEED` 后串起上述事实：正向生成
`COMPLETED/PASS`、选择器失败生成无 `BROWSER_STATUS_CONFLICT` 的 `COMPLETED/FAIL`，两类 Bundle 均由
Catalog 验真；`STOP_ESCALATION/ABORT` 零启动并形成仅含 preflight 的 `ABORTED/PENDING` Bundle，
Catalog 独立复核其证据适用性；审批摘要不一致仍零启动、零 Bundle。bootstrap 后的 dependency 提前
退出和 application readiness 超时也已通过公共 `run`，分别形成
`NODE_EARLY_EXIT / COMPLETED/FAIL` 与 `READINESS_TIMEOUT / ABORTED/FAIL`；两者均不生成 browser Evidence，
保留四个有界流附件并通过 Catalog、端口与 staging 清理验证。application READY 后 user cancel 也已
接入公共 Bundle 和 CLI signal 桥接，形成 `USER_CANCELLED / ABORTED/PENDING`、零 browser Evidence 与
完整逆序清理；Python 3.10/3.13 开发回归均为 206/206。live Preview 通过后外部进程分别抢占
dependency/application 端口的公共切片也已在 preflight 安全停止为 `ABORTED/PENDING`，不调用
observed runner、不接管或终止外部 listener，并由 Catalog 验真仅含 preflight 的 Bundle；双 Python
开发回归均为 207/207。dependency/application 的公共 owner-mismatch 切片也均拒绝 READY、不终止
外部 listener；外部进程按计划自然退出后 owned Job 完成逆序清理，形成
`LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL` 且 Catalog 可验真；双 Python 开发回归均为 208/208。
相同 sealed Plan/Profile 的连续两个公共正向 Run 也均为 `COMPLETED/PASS`，权威/Preview 一致、首份
Bundle 未被覆盖，轮间无残留且 M6 Comparison 为 `MATCH`、0 differences；双 Python 开发回归均为
209/209。subject watch root 漂移公共切片保留用户修改、不回滚；它发现并修复了 Evidence 已记录
`SUBJECT_DRIFT` 但 Verdict 错误 PASS 的消费者缺口，现在以 `BOOTSTRAP_SUBJECT_DRIFT` 形成
`COMPLETED/INCONCLUSIVE`，Browser/Catalog/清理均成立；双 Python 开发回归均为 210/210。cleanup
注入失败公共链路仍继续 application→dependency best-effort 回收，并以 HARD cleanup 断言形成
`CLEANUP_ERROR / ERROR/FAIL`；Catalog 拒绝伪装 clean，独立残留为零。Python 3.10 首轮全量曾无诊断
非零退出，定向与完整复跑未复现；最终双 Python 开发回归均为 211/211。staging 写入失败也已由
teardown 前稳定 `EVIDENCE_STAGING_FAILED` 进入受限 fallback，完整逆序清理后形成
`EVIDENCE_ERROR / ERROR/PENDING` 公共 Bundle，Catalog 可验真且未知 callback 反例被拒绝；双 Python
开发回归均为 213/213。随后所有公共出口的单包验证与组合 Catalog 门禁连接：真实正向/预检停止
Bundle 被同时接纳，损坏副本被隔离；生产 Workbench 由 Codex 内置浏览器真实读回
`runtime.bootstrap`，双 Python 214/214、前端 55/55 及构建/清理门禁通过。随后地基审查修复了
Plan 0.6 Report 重推导、READY 响应后 ownership、只读 API 稳定读取三个接缝，并同步 Workbench 版本；
双 Python 216/216 与前端门禁复验通过。随后严格串行轮逐项通过公共退出、双运行时、前端、依赖和
生产 Workbench 正负浏览器链；一次 Python 3.13 editable 环境漂移及全序列重跑被保留。随后压力
harness 的三次验收器失败被保留并逐次从 Wave A 重跑；首次完整通过后的发布审查又补强硬停止/超时
worker 子树回收。最终候选 `88d083a` 再次完成独立度 1/2/3、
READY 后取消交错和 1000 总请求，11 个 Bundle/Catalog 独立验真，最低可用内存 7323 MiB 且最终
零残留。其后发布安全整改封闭 11 条原攻击路径与 Job 内存硬限制，最终候选又从头完成严格串行
13/13、双 Python 228/228、Workbench 58/58、最低可用内存 6770 MiB 的压力轮与内置浏览器复验。
`0084443` 和 `m10-v0.11.0^{}` 已从 GitHub 精确读回一致，M10 标记 `FROZEN`；第二类真实项目
仍属于 M11。

冻结后系统审查又发现 Verdict 归因优先级、Browser 生命周期停止、运行期宿主机内存停止线与
Windows 目录原子发布等地基层缺口。补丁候选从头完成双 Python 262/262、Workbench 59/59、公共
出口、独立度 1/2/3、取消交错、1000 总请求、生产浏览器和清理复验；实现提交 `f4efdd2` 与
`m10-v0.11.1^{}` 已从 GitHub 精确读回。旧 `m10-v0.11.0` 不移动，M11 必须引用新补丁基线。

## 6. 详细文档

- [M0 纵向切片](04-m0-vertical-slice.md)
- [M1 资源与环境预检](05-m1-resource-preflight.md)
- [M2 真实浏览器证据](06-m2-browser-evidence.md)
- [M3 Vue 证据工作台](07-m3-vue-workbench.md)
- [M4 本地 Run 目录与轻量自举](08-m4-local-run-catalog.md)
- [M5 有界运行编排与静态目标生命周期](09-m5-bounded-run-orchestrator.md)
- [M6 同计划复跑确定性比较](10-m6-deterministic-rerun-comparison.md)
- [M7 预注册四角色配对反事实分析](11-m7-preregistered-paired-analysis.md)
- [M8 预注册全因子批次矩阵与固定种子扰动](12-m8-preregistered-batch-matrix.md)
- [M9 受控项目命令执行合同](14-m9-controlled-command-execution.md)
- [M10 有界完整项目自举 Contract 0.2（CONTRACT_FROZEN）](15-m10-bounded-project-bootstrap.md)
- [M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md)
- [M10 动态地基系统与代码质量审查](17-m10-foundation-review.md)
- [M10 第一轮严格串行完整复验](18-m10-serial-validation.md)
- [M10 第二轮 16 GB 有界压力审计](19-m10-bounded-stress-audit.md)
- [M10 发布安全整改与冻结复验](20-m10-release-security-remediation.md)
- [M10 冻结后地基纠偏与重新验收](21-m10-post-freeze-foundation-remediation.md)
- [M11 真实项目候选适配性与合同形成记录](22-m11-real-project-suitability-and-contract-draft.md)
- [M11 单节点能力与真实项目双门 Contract 0.4](23-m11-single-node-real-project-contract.md)
- [M11 入口治理与 M0-M10 当前复验](24-m11-entry-governance.md)
- [M11 Gate A 单应用能力验证](25-m11-gate-a-validation.md)
- [M11 Gate B Plan v1 首次真实失败](26-m11-gate-b-plan-v1-failure.md)
- [M11 Gate B 真实项目验证与冻结门禁](27-m11-gate-b-validation.md)
- [M12 宫阙验迹表现系统重构设计计划 0.1](28-m12-palace-workbench-design-plan.md)
- [M12-A 控制组与当前状态审计](29-m12-a-control-baseline-audit.md)
- [M12-B 四向公共视图与十字中轴骨架](30-m12-b-cross-axis-navigation.md)
- [M12-B 运行事实](31-m12-b-cross-axis-navigation-facts.md)
- [M12-C 空间令牌与 Runs 主链计划](32-m12-c-run-mainline-plan.md)
- [M12-C 空间令牌与 Runs 主链运行事实](33-m12-c-run-mainline-facts.md)
- [M12-D 派生分析视图计划](34-m12-d-derived-analysis-plan.md)
- [M12-D1 Comparison 运行事实](35-m12-d1-comparison-facts.md)
- [M12-B/C 空间收束与 Runs 目录整改计划](36-m12-bc-spatial-recomposition-plan.md)
- [M12-R1 紧凑中枢与过门运行事实](37-m12-r1-compact-shell-facts.md)
- [M12-R2 Runs 主链表现运行事实](38-m12-r2-runs-presentation-facts.md)
- [M12-D2 Pairing 四角色有向序列表现计划](39-m12-d2-pairing-presentation-plan.md)
- [M12-D2 Pairing 运行事实](40-m12-d2-pairing-facts.md)
- [M12-D3 Batch 双状态矩阵与 Wave 账册表现计划](41-m12-d3-batch-presentation-plan.md)
- [M12-D3 Batch 运行事实](42-m12-d3-batch-facts.md)
- [M12-E Browser Evidence 与全局状态表现计划](43-m12-e-browser-evidence-and-global-state-plan.md)
- [M12-E Browser Evidence 与全局状态运行事实](44-m12-e-browser-evidence-and-global-state-facts.md)
- [M12-F 总体验收与冻结计划](45-m12-f-final-validation-and-freeze-plan.md)
- [M12 参考图驱动的空间重组计划](46-m12-reference-guided-recomposition-plan.md)
- [M12 Visual Reference Contract 1.0](47-m12-visual-reference-contract.md)
- [M12-R3 参考图优先的 Catalog 重建合同](49-m12-r3-reference-first-catalog-rebuild.md)
- [M12-R3 Catalog 参考图测量与采用记录](50-m12-r3-catalog-reference-measurement.md)
- [M12-F 总体验收与冻结运行事实](51-m12-f-final-validation-facts.md)
- [M13 系统思维与分层代码质量终审计划](52-m13-system-and-layered-code-quality-audit-plan.md)
- [M13 系统思维与分层代码质量终审事实](53-m13-system-and-layered-code-quality-audit-facts.md)
- [M14 整改后终局复验与发布收束合同](54-m14-final-validation-and-release-contract.md)
- [M14 安全整改与重新基线合同](55-m14-security-remediation-and-rebaseline-contract.md)
- [M14 整改后终局复验与发布事实](56-m14-final-validation-and-release-facts.md)
- [VeriTrail 0.12.0 Release Notes](57-v0.12.0-release-notes.md)
- [Post-Core 独立入口层 Plan v1](58-post-core-entry-layer-plan.md)
- [VeriTrail Starter 0.1 single-webapp 合同](59-starter-single-webapp-contract.md)
- [VeriTrail Authoring Skill 0.1 合同](60-authoring-skill-contract.md)
- [VeriTrail Starter 0.1 十分钟 PASS/FAIL 黄金路径](61-starter-single-webapp-golden-path.md)
- [VeriTrail Authoring Skill A0 冻结事实](62-authoring-skill-a0-facts.md)
- [Post-Core 入口层 E1 独立发布合同](63-entry-layer-e1-release-contract.md)
- [VeriTrail 入口层 E1 0.1.0 发布说明](64-entry-layer-e1-release-notes.md)
- [GitHub 公共展示面收束事实](65-github-public-presentation-facts.md)
- [VeriTrail Starter 0.2 static-site 合同](66-starter-static-site-contract.md)
- [VeriTrail Authoring Skill 0.2 合同](67-authoring-skill-0.2-contract.md)
- [Post-Core 入口层 E2 static-site 实现事实](68-entry-layer-e2-static-site-facts.md)
- [Post-Core 入口层 E3 0.2.0 独立发布合同](69-entry-layer-e3-0.2-release-contract.md)
- [VeriTrail 入口层 E3 0.2.0 发布说明](70-entry-layer-e3-0.2-release-notes.md)
- [Core 无 checkout 首跑维护合同](71-core-first-run-maintenance-contract.md)
- [VeriTrail 0.12.1 Release Notes](72-v0.12.1-release-notes.md)
- [Core 0.12.1 发布与公开读回事实](73-core-v0.12.1-release-readback-facts.md)
- [Core demo Catalog 最终位置绑定维护合同](74-core-demo-catalog-binding-maintenance-contract.md)

文档 58–70 是 `v0.12.0` 发布后的独立入口层规划、验收、发布、公共展示、第二 Preset 实现与 0.2 发布事实，不是 M15，也不改变 M0–M14 的
冻结结论。Starter S0/S1 与 Authoring Skill A0 已完成源码冻结；E1 随后完成独立版本化、双 Python
clean install、公共入口、GitHub Release 与下载读回，两个入口产品现在可以准确描述为已发布的
`0.1.0`。E2 又以独立合同实现 Starter/Skill `0.2.0` 与有限 `static-site`；E3 已完成两个 0.2.0
带注释标签、独立非 Latest Release、七个资产、双 Python 公共下载读回与 GitHub 展示收口。E1 的
0.1.0 坐标继续不可变，E3 也不继承两个有限 Preset 之外的能力。

文档 71 是 `v0.12.0` 之后的 Core 维护合同：它只关闭 wheel 独立首跑缺口并增加无 checkout 门禁，
不重开 M0–M14，也不授予 Starter 或 AI 封存、运行与裁决权限。
文档 72 是对应的 `0.12.1` 维护 Release 说明；文档 73 记录受保护标签、精确提交、发布资产摘要与
公开下载复验。文档 71 的停止线已经满足，Core `0.12.1` 状态为 `RELEASED / MAINTENANCE FROZEN`。
文档 74 另行记录归档审查发现的 demo 最终位置绑定缺口与 `0.12.2.dev0` 未发布维护候选；它不改写
文档 71–73 的历史发布事实，也不把实现候选冒充新 Release。
- M11–M14 的规划边界见 [Post-M8 收束路线 Plan v1](13-post-m8-roadmap.md) 第 7–10 节。
