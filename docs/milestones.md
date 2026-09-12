# VeriTrail 里程碑冻结历史

## 1. 用途

本文件承接 README 不再展开的 M0–M14 冻结历史。它记录每个冻结基线回答的问题、真实取得的
证据、明确没有证明的能力，以及必须继续保留的失败事实。

里程碑标签实际指向的 Git 提交是版本寻址权威；实现提交、合同提交、运行哈希和完整退出条件
仍以对应的里程碑文档为准。M0–M9 已于 2026-08-11 从 `origin` 核验；M10 当前补丁基线与 M11
冻结基线于 2026-08-14 核验；M12 冻结基线于 2026-08-22 核验；M13 与 M14 最终发布基线于
2026-08-23 核验；Core 0.13.0 的公开发行基线于 2026-09-09 核验。

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

下列内容是**当前未证明/未实现的能力边界**，不是一张统一 TODO、欠债表或交付承诺：

- 产品表现候选：计划编辑器与在线写；
- 执行平台候选：结构化 npm/Maven 适配、服务/中间件生命周期、Docker、C2/C3 与跨平台；
- 独立安全边界：任意或不可信命令与恶意代码隔离，不能由 Shell、Docker、Job Object 或资源上限代替；
- 证据触发型研究方向：wave 内真实微并行、统计推断与容量表征；
- 权威非声明：AI 可以解释或提出候选，但 AI 裁决、Seal 与 HumanDisposition 不是待补功能。

这些对象的身份、触发条件、非目标和候选依赖见
[能力边界与系统认知地图](114-capability-boundary-and-system-map.md)。账册保持开放；R1 仍是当前唯一
施工优先级，账册条目不会自动获得里程碑身份。

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
- [VeriTrail 0.12.2 Release Notes](75-v0.12.2-release-notes.md)
- [Core 0.12.2 发布与公开读回事实](76-core-v0.12.2-release-readback-facts.md)
- [Post-Core 平台证据插件 Plan v1](77-post-core-platform-plugin-plan.md)
- [VeriTrail GitHub Evidence Plugin 0.1 合同](78-github-evidence-plugin-contract.md)
- [P0 GitHub Evidence Plugin 架构评审与冻结事实](79-p0-github-plugin-design-review.md)
- [Post-P0 Core 兼容桥合同 0.1：AcceptancePlan 与跨 Evidence 关系](80-p0-core-compatibility-contract.md)
- [PC1 通用 Acceptance Core 实现与候选事实 0.1](81-pc1-acceptance-core-implementation.md)
- [PC2 Acceptance Core 兼容与冻结事实 0.1](82-pc2-acceptance-core-freeze-candidate.md)
- [P1 Structured GitHub API Collector 施工合同 0.1](83-p1-structured-github-api-collector-contract.md)
- [P1 Structured GitHub API Collector 实现与冻结候选事实 0.1](84-p1-structured-github-api-collector-freeze-candidate.md)
- [Post-Core Review Attention Plugin Plan v1](85-post-core-review-attention-plugin-plan.md)
- [Review Attention R0 Contract 0.1](86-review-attention-r0-contract.md)
- [Review Attention Pattern Ledger 0.1](87-review-pattern-ledger.md)
- [R0 Review Attention 架构评审与冻结事实](88-r0-review-attention-design-review.md)
- [P2 Public Render Collector 施工合同 0.1](89-p2-public-render-collector-contract.md)
- [P2 Public Render Collector 实现与冻结事实 0.1](90-p2-public-render-collector-freeze-candidate.md)
- [受约束的开放世界观察方法 0.1](91-bounded-open-world-observation-method.md)
- [P3 Core Handoff 与真实正负链合同 0.1](92-p3-core-handoff-contract.md)
- [P3 Core Handoff 合同冻结事实](93-p3-core-handoff-contract-freeze.md)
- [P3 Core Handoff 实现与冻结候选事实 0.1](94-p3-core-handoff-implementation-freeze-candidate.md)
- [P3 Core Handoff 最终冻结状态发布](95-p3-core-handoff-freeze-publication.md)
- [P4 GitHub Evidence Plugin 独立发布合同 0.1](96-p4-github-evidence-release-contract.md)
- [P4 GitHub Evidence Plugin 独立发布合同冻结事实](97-p4-github-evidence-release-contract-freeze.md)
- [Release 资产下载恢复策略修正](98-release-download-recovery-correction.md)
- [P4 GitHub Evidence Plugin 发布准备候选事实 0.1](99-p4-github-evidence-release-preparation-candidate.md)
- [Core 0.13.0 Acceptance API 发布补全合同](100-core-v0.13.0-acceptance-api-release-contract.md)
- [Core 0.13.0 Acceptance API 合同冻结事实](101-core-v0.13.0-acceptance-api-contract-freeze.md)
- [Core 0.13.0 Release Candidate 施工计划](102-core-v0.13.0-release-candidate-plan.md)
- [VeriTrail 0.13.0 Release Notes](103-v0.13.0-release-notes.md)
- [Core 0.13.0 M11 正向夹具预算修正](104-core-v0.13.0-m11-positive-fixture-budget-correction.md)
- [Core 0.13.0 M11 正向夹具预算修正闭环事实](105-core-v0.13.0-m11-positive-fixture-budget-closure.md)
- [Core 0.13.0 发布与公开读回事实](106-core-v0.13.0-release-readback-facts.md)
- [P4 GitHub Evidence Plugin 发布恢复候选事实 0.1](107-p4-github-evidence-release-resume-candidate.md)
- [P4 GitHub Evidence Plugin 发布与公开读回事实](108-p4-github-evidence-release-readback-facts.md)
- [Review Attention Pattern Corpus 冻结合同 0.1](109-review-attention-pattern-corpus-freeze-contract.md)
- [Review Attention Pattern Corpus 合同冻结状态发布](110-review-attention-pattern-corpus-contract-freeze.md)
- [Review Attention Pattern Corpus 选择与 payload 候选](111-review-attention-pattern-corpus-selection-candidate.md)
- [Review Attention Pattern Corpus manifest 0.1](review-attention-pattern-corpus-0.1.json)
- [Review Attention Pattern Corpus 冻结闭环](112-review-attention-pattern-corpus-freeze-closure.md)
- [Review Attention R1 确定性语义切片合同 0.1](113-r1-deterministic-semantic-slice-contract.md)
- [VeriTrail 能力边界与系统认知地图 0.1](114-capability-boundary-and-system-map.md)
- [Review Attention R1 合同冻结状态发布](115-r1-contract-freeze-publication.md)
- [Q0 Quick Verification Scheduling Plugin 蓝图 0.1](116-q0-quick-verification-scheduling-blueprint.md)
- [Q0 Quick Verification Scheduling 蓝图冻结状态发布](117-q0-verification-scheduling-freeze-publication.md)
- [Release 资产下载恢复截止时间修正](118-release-download-recovery-deadline-correction.md)
- [Q0 Quick Verification Scheduling 最终冻结闭环](119-q0-verification-scheduling-final-freeze-closure.md)
- [Review Attention R1 Schema 与规范身份合同 0.1](120-r1-schema-and-canonical-identity-contract.md)
- [Review Attention R1 Schema 与规范身份合同冻结发布](121-r1-schema-contract-freeze-publication.md)
- [M10 公共自举正向夹具生命周期预算对齐](122-m10-public-bootstrap-positive-fixture-budget-alignment.md)
- [R1 Schema payload 前置审计与合同修正候选](123-r1-schema-payload-preflight-correction.md)
- [R1 Schema payload 前置修正重新冻结发布](124-r1-schema-payload-preflight-refreeze-publication.md)
- [Review Attention R1 Schema payload 冻结候选](125-r1-schema-payload-freeze-candidate.md)
- [Review Attention R1 Schema payload 冻结发布](126-r1-schema-payload-freeze-publication.md)
- [Review Attention R1 SourceSnapshot 首个运行切片合同 0.1](127-r1-source-snapshot-runtime-contract.md)
- [Review Attention R1 SourceSnapshot 运行合同冻结发布](128-r1-source-snapshot-runtime-contract-freeze-publication.md)
- [Review Attention R1 SourceSnapshot 实现冻结候选](129-r1-source-snapshot-implementation-freeze-candidate.md)
- [Review Attention R1 SourceSnapshot 最小运行切片冻结发布](130-r1-source-snapshot-freeze-publication.md)
- [R1 SourceSnapshot 后继最小闭环审计](131-r1-post-snapshot-derivation-input-audit.md)
- [R1 Derivation Input Binding 最小运行合同 0.1](132-r1-derivation-input-binding-contract.md)
- [R1 Derivation Input Binding 合同冻结发布](133-r1-derivation-input-binding-contract-freeze-publication.md)
- [R1 Derivation Input Binding 实现冻结候选](134-r1-derivation-input-implementation-freeze-candidate.md)
- [R1 Derivation Input Binding 最小运行切片冻结发布](135-r1-derivation-input-freeze-publication.md)
- [R1 Derivation Attempt 与 Fact Provenance 前置审计](136-r1-derivation-attempt-and-fact-provenance-audit.md)
- [R1 Derivation Attempt 与 Fact Provenance 最小运行合同 0.1](137-r1-derivation-attempt-and-fact-provenance-contract.md)
- [R1 Derivation Attempt 与 Fact Provenance 合同冻结发布](138-r1-derivation-provenance-contract-freeze-publication.md)
- [R1 DerivationEvidence Schema 修正前置审计](139-r1-derivation-evidence-schema-correction-audit.md)
- [R1 DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)
- [R1 DerivationEvidence Schema 0.1.1 修正合同冻结发布](141-r1-derivation-evidence-schema-correction-contract-freeze-publication.md)

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
文档 74 另行记录归档审查发现的 demo 最终位置绑定缺口与 `0.12.2` 有界维护合同；文档 75 记录
Release 说明与门禁；文档 76 记录受保护标签、精确提交、五项资产、公开下载、clean install、
正负组合链和清理读回。文档 74 的停止线已经满足，Core `0.12.2` 状态为
`RELEASED / MAINTENANCE FROZEN`。文档 74–76 不改写文档 71–73 的 `0.12.1` 历史发布事实。

文档 77–79 新开独立平台插件 `P` 轨。P0 只冻结 GitHub 外部平台事实的架构、合同、权限、失败语义
与后继验收入口；它不是 M15，也不是 E4，不修改 Core、Starter、Authoring Skill、Workbench、
Schema、CI 或任何既有版本。首轮 P0 文档已由 PR #21 合入
`8944549a080e331a7021337e40de5c8accc49649`；身份语义补丁又由 PR #22 合入
`6635280c7aaa5b54da8f1a371b337658c0cb7317`，两轮均从真实 GitHub README、合同与评审渲染页完成公开
读回。P0 没有可运行插件与发布坐标，P1 仍须从最新受保护主线另行施工。P0 的信任上限只覆盖声明
信任域内的证据一致性与承诺后完整性；GitHub API 和公开页面
不是两个独立权威，也不能证明首次封存前的上游事实真实。P0 的认识论上限同样不裁定提出者观点，
只检查 sealed 条件与 Evidence 的关系并保留不确定性。sealed Plan 是期望的唯一权威；派生 request、
Plan drafter、check identity 与非原子采集窗口均有独立边界。GitHub 之外的独立锚不进入当前产品路线。
P0 还把 `facts_digest`、现有 EvidenceArtifact SHA-256、request identity 与 Core Run identity 分开：采集
实现版本进入 provenance，只有规范化含义变化才升级事实语义版本；同事实的独立证据不得被去重。
最终收口再把可重放 request 与实际 Collection Session 分开，窗口只使用 monotonic elapsed 判断，并
为 Plan/Schema 语义、Core assertion expressibility 与 `veritrail-json-c14n/1` 建立 P1 前置门；P1 0.1
禁用 conditional GET，tag 使用 peeled commit，认证只保留无秘密 access mode provenance。Core 0.12.2
双 Python 离线探针曾确认单源字面断言可执行，同时确认未观察 PRIMARY 仍可 `PASS`、不同 Evidence 的
session 无法直接比较；这些缺口不能用插件布尔值、虚构实验字段、偶然的变量冲突检测或缓存事实绕过。
文档
80 已把该桥定义为一次性、串行的 `PC0 -> PC1 -> PC2`：PC0 只冻结独立 AcceptancePlan、公共
Evidence binding、跨 Evidence 关系与旧消费者隔离；81 已完成平台无关的 PC1 Core 实现；82 已在
精确候选上完成 PC2 双 Python、全消费者、Workbench、正负 Bundle 独立复算、wheel clean install、
敏感与清理门禁，并通过 PR #26 九项远端检查、受保护主线合入及真实 GitHub 渲染读回。PC2 当前为
`PC2_FROZEN`，上述兼容前置门已经关闭。文档 83 的 P1 合同 0.1 随后冻结，文档 84 已据此实现独立
只读 GitHub REST Collector、Evidence 规范化、双 Python 离线/兼容矩阵、wheel clean install 与真实
GitHub 纵向切片；Freeze 前发现 rulesets 与 classic branch protection 的来源叠加反例，0.2 因而只重开
这一模型点。修正已通过 PR #32 的 11 项门禁，以
`main@5b363637f59be9786d58eed61a14e3bd663dd6d8` 合入，并完成精确主线与匿名 README/事实文档
读回。P1 状态为 `P1_FROZEN`；文档 89 从精确主线
`cdc2c250f21b37a0be9f815295f7b7c3c5081d0d` 定义 P2 0.1，随后经 PR #38 最终 11 项门禁、受保护主线
合入与 exact-SHA 匿名 Render 读回固定在 `main@8c624ec3aa83fe462e3578d8aa215e8ef9908332`。默认 Pages
根坐标反例随后经 PR #40 的 11 项门禁、受保护主线合入和 exact-SHA 匿名 Render 读回，将空
`pages_path` 冻结为站点根 `/` 的唯一表示。completion-time Network 计数不能冒充 response-body 硬截断；
该精确计量与 Chromium Fetch 流控制修正已由 PR #42 的 11 项门禁、受保护主线与 exact-SHA 匿名
README/合同/Ledger 读回重新冻结。P2 Collector 随后完成 request/URL、浏览器生命周期、response-body
预算、固定作用域、三样本、Evidence assembly 与 P1 → P2 串行协调；候选经 PR #49 的 11 项门禁合入
`main@ca6b8aaa33bc06795c96610b9e9085506efef9a0`，并由产品 Collector 从 exact main 完成 desktop/narrow
README 真实读回。docs-only closure 随后通过 PR #50 的 11 项门禁合入
`main@2d3877df41d7ec5a3b7b932404f6b622f06862a8`，并由产品 Collector 对该 exact main 的 README/事实
文档完成匿名读回。最终发布 PR #51 又被原始 Python 3.10 `-O` 门禁中的 `13.688s > 9s` M10 生命周期
反例否决并关闭，未合并、未以 rerun 覆盖；P2 实现事实保持成立，冻结资格被单独阻断。独立 PR #52
沿完整中断链统一生命周期与 Chromium 释放预算，并阻止 owned termination 后的失效观察；其原始
11 项门禁全绿后合入 `main@bb8f2d44c0c681862a5e63506ae57d4b4a8d7947`，修正后的 exact main 又完成
匿名 README desktop 与 `RA-018 rev2` Ledger narrow 读回。本状态发布以自身门禁、受保护主线合入和
合入后匿名读回为生效条件；该链成立后状态为 `P2_FROZEN / P3_NOT_STARTED`。尚无 P3 正式 handoff、
插件标签或 Release。
第一次 docs-only closure PR #43 又因重复出现的 M10 Chromium cleanup timing failure 被否决并关闭，未合入；
独立 PR #44 以共享绝对 deadline 修复预算刷新，经 11 项门禁合入
`main@25ff62f50a01fddc086c41740af802d9c2df0495`。后继 closure 没有把失败尝试洗成成功，也没有把任何
M10 修复冒充 P2 实现。

文档 85–88 新开独立顶层 Review Attention `R` 轨；它不是 M15、P5 或 M13 的重跑。R0 只设计
精确 Source Snapshot、ReviewPolicy、CodeFact/AnalyzerEvidence、机器 Proposal、Attention Map、
HumanDisposition 和可选 Core handoff 的权威与 Artifact 边界。`R = Review`，不表示 Risk；机器提案
不能冒充缺陷事实或 Core Verdict。R0 宪法与 Ledger Schema 可以先冻结，真实模式账册则在 P2–P4
期间保持 append-only/open。冻结后合同一致性修正又将问题层与机制类拆为 `problem_layer /
pattern_class`，并要求每次状态提升追加 `record_revision / supersedes_digest / record_digest`；只有人类
authority 能创建 HumanDisposition，Policy 不能自动处置。P4 以后才选择 exact commit + manifest digest
且逐项绑定 `pattern_id + selected_record_digest` 的 Pattern Corpus 供 R1 使用。R0 设计候选已通过 PR #34 的 11 项门禁，以
`main@411a43814632df8a5dc5ae4a9d4e66b11ab7aed1` 合入，并完成精确主线和未登录 GitHub HTML 读回。
当前为 `R0_ARCHITECTURE_FROZEN / PATTERN_LEDGER_OPEN / DESIGN_ONLY`，没有源码包、Schema、CLI、CI、
标签或 Release；R1 被明确阻塞到 P4 与 corpus freeze 之后。R0 冻结发生时 P2 仍未启动；后续 P2
合同候选不会反向改写该历史事实或改变 R0 范围。

文档 91 将 P1/P2 施工中形成的平台适配、运行时控制、观察语义与证据工程四层方法归纳为
`METHOD_NOTE / NON_CONTRACTUAL`。同一补丁把 R1 的未来问题补充为：从精确 Source Snapshot 的确定性
关系图派生允许重叠、有界且带 coverage/truncation 的 Semantic Review Slice，并保持 slice derivation、
analysis 与 attention ranking 分权。该说明不修改已冻结 R0 Artifact，不启动 R1，也不表示 P3 已开始。

文档 92 从 `main@3e785d197c8040c8baa4120fc63301eb347e5bc8` 新开 P3 合同候选。它不新增 Collector，
只定义 P1/P2 标准 Evidence、仅绑定 role/path/digest 的极薄 handoff manifest 与现有 Acceptance Core 的
串行交接，并把 Plan binding、session integrity 与 Verdict 权留在 Core；同时冻结四态正负链、身份、
失败、安装和真实 GitHub 验收边界。PR #55 的原始 11 项门禁与候选合入后，匿名产品读回发现 P 轨
路线图因 GitHub Mermaid 子框架导航稳定得到有界 `PARTIAL`，而不是旧冻结门假定的 `COMPLETE`。
PR #56 没有删除 Mermaid 或放宽 P2，只把这一现实边界写回合同；其原始 11 项门禁全部通过并以
`main@9eb630c1c502cbae0f76c3e783084c412792bba1` 合入。文档 93 保留候选、修正、失败观察与修正后
exact-main 匿名读回，作为独立 docs-only 状态发布；其自身门禁、合入和读回全部成立后，状态为
`P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`，下一步只能从新的 exact main
串行开始 P3-A。

P3 后继实现从 `main@589bbad7261cceda1aa3a6412278a48473a9b1b7` 严格串行完成 A–E。实现候选
`fa26dda516c354a5ddd08335202d3fd1cf5dbabb` 经 PR #64 原始 11 项门禁合入
`main@c0bce6cb7a3c9f3684d1845beda355084f232d0a`；合入后产品 P1/P2 Collector 又对 exact README 与 P3
合同完成匿名 `COMPLETE` 读回并由 Core 得到 `PASS`。第一次真实 E 暴露 synthetic fixture 与生产 P2
fact path 漂移，提交 `7e10e7a` 只修正 C 并将经验追加为 `RA-021 rev1`，没有改 P2 或 Verdict 语义。
候选阶段为 `P3_IMPLEMENTED / FREEZE_CANDIDATE / P4_NOT_STARTED`；文档 94 的 docs-only closure 完成门禁、
主线合入和合入后读回以前，不得标记 `P3_FROZEN` 或启动 P4。

文档 94 的 docs-only 候选提交 `f9f85693b879643b038a9fc29f8c331d2119671b` 经 PR #65 原始
11 项门禁合入 `main@ec5ac70dcfa72b1b9859602af62cc3c9344389de`，合入后 README 与文档 94 又以
fresh anonymous P1/P2 产品链读回为 `COMPLETE`，Core 均为 `PASS`。独立最终状态发布的自身门禁、合入
和合入后读回全部成立后，当前为 `P3_FROZEN / P4_NOT_STARTED`；这不自动启动 P4，也不解除 R1 的
`P4_AND_CORPUS_FREEZE` 阻断。

文档 96 从 `main@f30647577e6de68c4d40a96f4f9b223fb24140bb` 重建 P4 docs-only 发布合同候选。先前
PR #68 的原始门禁暴露既有 M11 CLI 聚合 `ERROR` 后停止且未合入；PR #69 只补充分层诊断，并以
原始 11/11 门禁合入当前 exact main。后继成功不覆盖 #68，也不把未复现冒充根因裁决。本文只冻结
GitHub Evidence Plugin `0.1.0` 的 source/distribution/asset/tag/Release/public-download 身份、固定四项
资产、base/render 安装矩阵、non-Latest 约束、失败恢复与匿名读回门禁；不修改 P1–P3 或 Core 语义。
盘点确认现有 tag ruleset 尚未覆盖 `refs/tags/github-evidence-v*`，因此独立标签保护必须先于 tag 创建。
该候选阶段保持为 `P4_CONTRACT_0.1_CANDIDATE / RELEASE_NOT_STARTED`；合同自己的门禁、受保护主线合入、
exact-main 匿名产品读回与独立冻结发布完成前，不得创建插件 ruleset、tag、Release 或公开资产。

PR #70 将重建候选合入 `main@f27507c3735a68134fa428344f63265601c93715` 后，冻结前身份核账发现
validation summary 若记录“每个 payload”的摘要会要求它声明自身摘要。候选因此保持未冻结，并以
最小修正明确 `wheel/sdist -> summary -> checksum -> external release facts` 的非自指生成与绑定顺序；
该反例没有触发 tag ruleset、tag、Release、资产上传或 P1–P3 语义修改。

非自指修正经 PR #71 原始 11/11 门禁合入
`main@eb4dcb60230a516503bf80ce26e13b25cd9b9d97`；该 exact main 的 Public CI 11/11 与 Browser Smoke
1/1 成功，随后产品 P1/P2 Collector 对 README desktop 与文档 96 narrow 完成 fresh anonymous
`PUBLISHED / COMPLETE` 读回，两条 Core 链均为 `PASS`。独立
[文档 97](97-p4-github-evidence-release-contract-freeze.md)的自身门禁、主线合入和合入后读回全部成立后，
当前状态为 `P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`；插件 tag ruleset、tag、Release 与公开
资产仍不存在，R1 继续等待 P4 最终冻结与 Pattern Corpus 冻结。

发布准备候选合入后的最终 exact-main clean-install 门发现公开 `v0.12.2` wheel 不含 P3 所需
Acceptance API，而先前准备矩阵使用了同版本号的当前源码本地 wheel。P4 因而保持 `BLOCKED`；
[文档 100](100-core-v0.13.0-acceptance-api-release-contract.md)将既有冻结 Acceptance 能力的公开发行
补全为独立 Core 0.13.0 前置闭环。该修正不移动或重制历史 `v0.12.2`，也不提前创建插件发布坐标。
合同候选经 PR #77 原始 11/11 门禁合入
`main@5b28ac3076ff4a08added47cbfc66c960c3dbdea`；该 exact main 的 Public CI 11/11、Browser Smoke
1/1，以及 README/合同正文的两个独立匿名产品读回均已成立。[文档 101](101-core-v0.13.0-acceptance-api-contract-freeze.md)
的最后门全部成立后，合同状态为 `CORE_0.13.0_CONTRACT_FROZEN / P4_BLOCKED`。C1 已从 exact
`main@e69f3844254947f795564cb845056652f2dcf3ac` 进入
[Release Candidate 施工计划](102-core-v0.13.0-release-candidate-plan.md)：Starter 0.2.0 的冻结
`>=0.12,<0.13` 边界、继承该边界的 Authoring Skill 真实 DRAFT 链、GitHub Evidence 的源码前向兼容、
distribution 声明兼容与公开 clean install 分开取证，Starter/插件历史 metadata 保持只读。当前源码发行身份已进入
`0.13.0 / RELEASE CANDIDATE / PENDING PUBLIC READBACK`，说明见
[0.13.0 Release Notes](103-v0.13.0-release-notes.md)；P4 与 R1 仍保持阻断。
候选 PR #79 原始 11/11 已成立并合入 `main@a5ba0e1bd8f181851db83de611981524da1da8f5`；首轮
exact-main Public CI 随后在 Python 3.13 `-O` 暴露 M11 正向真实浏览器夹具的 15 秒外层预算不自洽。
[文档 104](104-core-v0.13.0-m11-positive-fixture-budget-correction.md)只修正该测试夹具，C2 与 P4 在新的
PR 和 exact-main 门禁成立前继续阻断。
独立修正 PR #80 原始 11/11 成功并合入 `main@43c8e9105adf84641d203514594d3e0c5a1251e8`；该
exact main 的 Public CI 11/11、Browser Smoke 1/1，以及 README/文档 104 的两个 fresh anonymous
Render 读回均已成立。[文档 105](105-core-v0.13.0-m11-positive-fixture-budget-closure.md)发布该闭环事实；
它自己的最后门成立后只恢复 C2 施工资格，Core 0.13.0 仍未发布，P4 仍阻断。

C2 随后从 exact `main@cd6f85246c0a789a3117861144af95deeb1b7077` 重新构建最终 Core 0.13.0
wheel、sdist、Workbench 伴随 ZIP、validation summary 与非自指 checksum；受保护注释标签
`v0.13.0` 的 tag object `a03c7a1fbcff88291c8cb86f2718c8d76d1ed709` 解引用到同一提交。GitHub
Release 已成为非 draft、非 prerelease 的 Latest Core；五项上传资产、匿名下载副本与冻结 SHA-256
逐项一致。公开 wheel/sdist 已在 Python 3.10/3.13 仓库外 clean install 并复算四 Verdict 与同一
imported snapshot；Workbench ZIP 已完成独立解压与真实 Chromium 5/5。匿名 Release body 三样本稳定、
无 coverage/Collector/cleanup error，精确事实见
[文档 106](106-core-v0.13.0-release-readback-facts.md)。该文档自己的原始门禁、受保护主线合入与
合入后 exact-main 匿名读回全部成立后，状态才推进为
`CORE_0.13.0_RELEASED / MAINTENANCE_FROZEN / C3_CLOSED / P4_RELEASE_NOT_STARTED`；这只解除 P4
的 Core 发行阻断，不创建插件发布坐标，也不解除 R1 的 P4/Pattern Corpus 双前置门。

P4 随后从 exact `main@ab874d3cfd9ac140654e35d84b0025c2503e10cd` 恢复发布准备；提交
`beaf006574e23d3d3f0c3541d9ea0708d23fa097` 只把 GitHub Evidence Plugin 0.1.0 的 distribution 与
发布核验绑定到公开 `veritrail==0.13.0`。双 Python 源码矩阵、base/sdist/render clean install、插件
卸载后的 Core-only 复算、可重复本地资产与两条匿名真实 GitHub 候选链已经成立，精确事实及保留失败见
[文档 107](107-p4-github-evidence-release-resume-candidate.md)。当前仍为
`P4_RELEASE_PREPARATION_CANDIDATE / NO_TAG / NO_RELEASE / NO_PUBLIC_DOWNLOAD_CLAIM`；原始远端门禁与
受保护主线合入完成前不得建立发布坐标，合入后必须从新的 exact main 重建最终字节。

后继 PR #83 原始 11/11 门禁合入
`main@548b17ccb1f20d55a9f9beef6666e913af5f65d9`；该 exact main 的 Public CI 11/11 与 Browser Smoke
1/1 均在 attempt 1 成立。P4 从该坐标重新构建最终 wheel、sdist、pre-tag validation summary 与
非自指 checksum；tag ruleset `22613490` 先于受保护注释标签 `github-evidence-v0.1.0` 生效。non-Latest
Release `385275245` 的四项资产、匿名下载摘要、双 Python clean install/runtime/uninstall、真实 GitHub
正向链及匿名 Release body 均已读回，Core `v0.13.0` 继续是 Latest。精确事实见
[文档 108](108-p4-github-evidence-release-readback-facts.md)。该状态补丁自己的原始门禁、受保护主线合入
与合入后 exact-main 匿名读回全部成立后，状态才推进为
`P4_GITHUB_EVIDENCE_0.1.0_RELEASED / P4_FROZEN / R1_BLOCKED_UNTIL_PATTERN_CORPUS_FREEZE`；P4 只解除
R1 的发布前置条件，不自动选择 Pattern Corpus 或启动 R1。

P4 后的首次 Corpus 前置核账确认 Ledger 的完整机器 revision 仍停在 `RA-021`，而 P2–P4 事实文档还
保留了六类未物化的真实反例。独立 docs-only 候选因此先追加 `RA-022` 至 `RA-027`，并由
[文档 109](109-review-attention-pattern-corpus-freeze-contract.md)定义最小充分选择、非自指 manifest、exact
Corpus source commit 与后继 closure 的边界。候选经 PR #85 原始 11/11 门禁合入
`main@8526c5551cce3a9a9e916917381e0e0463a082f0`，合入后的 Public CI、Browser Smoke、README 与合同
正文匿名产品读回均已成立。[文档 110](110-review-attention-pattern-corpus-contract-freeze.md)自身门禁、受保护
主线合入和 exact-main 匿名读回成立后，状态推进为
`CORPUS_CONTRACT_0.1_FROZEN / LEDGER_OPEN / CORPUS_NOT_SELECTED / R1_BLOCKED`。后继候选 revision、
manifest 与最终公开 closure 仍须继续串行；合同冻结不等于 Corpus 已经冻结。

下一条独立 payload 候选从 exact `main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a` 开始，先将
`RA-003 / RA-004 / RA-008 / RA-023` 物化为完整 `CONTRACT_CANDIDATE` revision 并在双 Python
normal/`-O` 下独立复算，再完成 `RA-001` 至 `RA-027` 的逐条最小性审议。只有这四条形成线性
`FROZEN_PATTERN` successor，并由
[manifest 0.1](review-attention-pattern-corpus-0.1.json)按精确 digest 选择；选择记录见
[文档 111](111-review-attention-pattern-corpus-selection-candidate.md)。当前状态为
`CORPUS_PAYLOAD_CANDIDATE / CORPUS_CLOSURE_NOT_STARTED / R1_BLOCKED`。候选没有预填未来合入 commit，
manifest 也不自含摘要；最终 identity 必须由后继 closure 外部绑定 payload 合入后的 exact source commit
和 manifest digest，并完成匿名公开读回。

Payload 候选提交 `415bc3d28ae86ab298cb99f9e6a16164094e67f4` 经 PR #87 原始 11/11 门禁合入
`main@9bdcef30517309bbc87ed7fdb0fec395197ef58a`；该 exact main 的 Public CI 11/11 与 Browser Smoke 1/1
成功。Closure 在双 Python normal/`-O` 下重新验证 20 条 revision、14 条线性 chain 与 4 个 manifest
entry，并用产品 P2 Collector 匿名读取 README 与文档 111；raw manifest 的 1,085 bytes 也从 exact source
commit 匿名下载并与工作树逐字节一致。[文档 112](112-review-attention-pattern-corpus-freeze-closure.md)
外部绑定 source commit 与 manifest digest
`sha256:ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`。该状态发布自身门禁、受保护
主线合入与合入后 exact-main 读回全部成立后，状态推进为
`PATTERN_CORPUS_0.1_FROZEN / LEDGER_OPEN / R1_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`；R1 必须
从新的 exact main 单独起草合同，本闭环不创建 R1 实现。

后继 [文档 113](113-r1-deterministic-semantic-slice-contract.md) 已从
`main@9ab64121350b69ce81e6be79961ad426026bbc39` 建立 docs-only R1 0.1 候选，将首版范围明确为
`SourceSnapshot -> CodeFacts -> typed structural Relations -> bounded overlapping ReviewSlices ->
CoverageLedger`，并冻结 Python 3.10 Profile 的能力上限、分阶段 coverage、来源组合与快照连续性原则。
候选提交 `d93e70321fa9db15ac31f5048f9091d59c954dfd` 经 PR #89 原始 11/11 门禁合入
`main@617e99ddd8217fbcaf26037c0f9ac15014795f15`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
以及 README、合同、里程碑三次匿名产品读回均成立。后继
[文档 115](115-r1-contract-freeze-publication.md)只发布该候选闭环；其自身门禁、受保护主线合入与合入后
exact-main 匿名读回全部成立后，状态才是
`R1_CONTRACT_FROZEN / R1_SCHEMA_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。下一步只获准从新的
exact main 独立起草 Schema 与兼容向量；Schema、源码、CLI、运行 CI、Provider、标签和 Release 均未存在。

README 读者骨架与对称 SVG 已分别完成独立受保护主线闭环，R1 Schema 施工随后从
`main@35774838b3e9aeb5f062cfb101e96d76cea0e8ac` 恢复。后继
[文档 120](120-r1-schema-and-canonical-identity-contract.md)只建立 docs-only Schema 合同候选，冻结候选字段、
`veritrail-json-c14n/1` 文件字节、domain-separated semantic digest、可逆 Git path hex、raw blob 半开
byte anchor、确定性 BFS、inclusive budget、Coverage denominator 与固定 Artifact layout。实际 JSON
Schema、兼容向量、源码、CLI、Provider 与运行 CI 仍不存在，也不得与候选合同混在同一分支。

该合同候选经 PR #99 原始 11/11 门禁合入
`main@49a2d69d44cca21024808fe5c298db8bac7f64c4`，后继 docs-only 冻结状态发布 PR #100 的原始门禁却在
Python 3.10 `-O` 复现 M10 公共自举正向夹具的 15000 ms 隐藏性能门，因此保持未合入。该失败不推翻
R1 Schema 候选证据，也不能由 rerun 覆盖；[文档 122](122-m10-public-bootstrap-positive-fixture-budget-alignment.md)
只对齐同文档 104/105 已裁决的正向夹具边界。PR #100 随后关闭且没有 rerun；独立修正 PR #101 的
原始 11/11 门禁已合入 `main@8aa70807c0de9c0f50ad977575d81f2a1d635a91`，新 exact main 的 Public CI
11/11、Browser Smoke 1/1 与文档 122 匿名产品读回均已成立。

[文档 121](121-r1-schema-contract-freeze-publication.md)从该新 exact main 重建冻结发布，保留候选闭环、
首次发布被否决和独立修正的完整因果链。它自己的门禁、受保护主线合入与合入后匿名读回全部成立后，
状态才推进为
`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。后继
payload preflight 在写入第一份 Schema 前发现 scope item key、frontier、Coverage denominator 与 Provider
provenance identity 仍存在实现自由度，因此[文档 123](123-r1-schema-payload-preflight-correction.md)只重开
该边界；当前为 `R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE / R1_SCHEMA_PAYLOAD_BLOCKED /
R1_IMPLEMENTATION_NOT_STARTED`。修正重新冻结前，Schema payload、runtime importer、parser、
relation/slice engine、CLI、Provider、标签和 Release 全部禁止。

修正候选 `19a923cae37b057879ae9879296e789c6e348cf2` 经 PR #103 原始 11/11 门禁合入
`main@839877ca38489d0518a5b67d5956c7907152529c`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
与 README、文档 120、文档 123、milestones 四次 fresh anonymous 产品读回均成立，规范 summary digest
为 `sha256:3a77672fd78a8f893117f9f5bfe440496f2b9305528f992d0e4e080b301606f6`。后继
[文档 124](124-r1-schema-payload-preflight-refreeze-publication.md)只发布这条修正链；其自身门禁、受保护主线
合入与合入后 exact-main 匿名读回全部成立后，状态恢复为
`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。这只允许
从新的 exact main 创建十个固定 JSON Schema、纯数据兼容 corpus、规范字节/摘要向量与
Schema/conformance tests；运行实现、CLI、Provider、标签和 Release 仍未开始。

后继 [文档 125](125-r1-schema-payload-freeze-candidate.md)从 exact
`main@4ef8b6434597b6557d6306100b91aebd9c1b3ecd` 物化十个 Draft 2020-12 Schema、20 项数据型兼容
义务、24 个 identity domain 的规范字节/摘要向量以及一份九文件 synthetic COMPLETE bundle；
`jsonschema==4.25.1` 只作为 `schema-test` extra 进入 CI 测试安装，Core base wheel 不获得运行依赖。
当前状态为 `R1_SCHEMA_PAYLOAD_CANDIDATE / R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED /
R1_IMPLEMENTATION_NOT_STARTED`。候选自己的原始远端门、受保护主线合入、exact-main 门与匿名逐字节读回
成立前，不得冻结 payload 或启动 R1 runtime。

候选提交 `88ece8443904c83cc74b6ee3608d84e03e4951af` 经 PR #105 原始 11/11 门禁合入
`main@4a25ef3d4009395f3510e847909f1efbaa29c5ac`；新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1
均在 attempt 1 成功。十个 Schema 与十九个 corpus 文件已从 exact commit 匿名逐字节读回，全部与候选
一致，汇总摘要为 `sha256:afd3fcca87e873a4a797ff8fd8ffd053d826969202a2ec1da643882e339a8796`；
公开 Core 0.13.0 与 GitHub Evidence Plugin 0.1.0 又对 README、文档 125 建立两个独立
`P1 -> P2 -> P3/Core` session，均取得 `PUBLISHED / COMPLETE / PASS`，summary digest 为
`sha256:1513f6b4df79116cc1eb75243ed44fc725cdc10c6cbda883db84e427cf206a93`。后继
[文档 126](126-r1-schema-payload-freeze-publication.md)只发布这条冻结链；其自身最后门成立后，状态推进为
`R1_SCHEMA_PAYLOAD_FROZEN / R1_IMPLEMENTATION_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`。运行实现
只能从新的 exact main 另建单一意图坐标，不能把 payload 候选绿灯当成 runtime 证据。

后继 [文档 127](127-r1-source-snapshot-runtime-contract.md)先审计首个 SourceSnapshot 切片，没有写运行
代码。审计证明冻结的 `R1_DERIVATION` Manifest 不能合法描述单文件 Snapshot publication，并且后继
`ReviewPolicy.execution_budget` 不能反向拥有 acquisition 安全边界；文档 120 只删除竞争残句，不修改
Schema payload。当前状态为
`R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_CANDIDATE / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`：只有
候选自己的门禁、受保护主线合入、exact-main 匿名读回与独立状态发布全部成立后，才允许创建首个 runtime。

候选提交 `ac3d4169732529ad7662672222156c7e140d0fc8` 经 PR #107 原始 11/11 门禁合入
`main@def98c6a116b50fc9c0e7c849dd9118b70285eba`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
与 README、文档 120/127 的匿名 Public Render 读回均成立。[文档 128](128-r1-source-snapshot-runtime-contract-freeze-publication.md)
只发布这条事实链；它自己的最后门成立后，状态才推进为
`R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED /
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`。该授权只覆盖 SourceSnapshot 最小实现，不向
Fact/Relation/Slice/Coverage 或完整 Derivation Manifest 传播。

SourceSnapshot 最小实现从 exact `main@24c41c0ac9221ba4d8ae642c08ca5cdc08587b20` 另开单一意图分支。
PR #109 首次 head 的 Python 3.10/3.13 门均在 exact Reference Lab fail closed：Actions shallow checkout
没有冻结的 `9ab64121350b69ce81e6be79961ad426026bbc39` object，而实现按合同拒绝网络/lazy fetch。该失败没有
rerun；后继提交只将 Python CI checkout 改为完整本地 history，不修改产品、预算、摘要或验收期望。
修正 head 原始 Public CI 11/11 后，PR #109 以
`main@4f5c41a9f163056ed4c2d2cfd686d321ecba5605` 合入；新 exact main 的 Public CI 11/11、Browser Smoke
1/1 与独立 Reference Lab 读回均成立。当前状态为
`R1_SOURCE_SNAPSHOT_IMPLEMENTED / FREEZE_CANDIDATE /
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`，证据边界见
[文档 129](129-r1-source-snapshot-implementation-freeze-candidate.md)。该文档自己的受保护主线闭环与后继
独立冻结发布成立前，不得写 `R1_SOURCE_SNAPSHOT_FROZEN`。

冻结候选经 docs-only PR #110 的原始 Public CI attempt 1 取得 11/11，并以
`main@ee249d35e1000d3f15f0a0b4e1ef9eb66a425b32` 合入。新 exact main 的 Public CI 11/11、Browser
Smoke 1/1，以及 README 与文档 129 的 fresh anonymous P2 Collector exact-SHA 读回均成立。
[文档 130](130-r1-source-snapshot-freeze-publication.md)独立发布这些事实；其自身最后门全部成立后，状态为
`R1_SOURCE_SNAPSHOT_FROZEN / R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。
冻结只覆盖单一 `source-snapshot.json` 最小运行切片；后继 Fact、Relation、Slice、Coverage、conflict /
UNKNOWN 传播与完整 Derivation Manifest 仍须各自先完成合同闭环。

后继审计从 exact `main@b1a58143ae2fd359b885a575587aa4682aef8a04` 开始，只检查 Snapshot 之后哪个
最小边界有资格进入合同，没有写实现。[文档 131](131-r1-post-snapshot-derivation-input-audit.md)确认 FactSet
必须绑定 DerivationEvidence，而冻结 Manifest 又没有 Fact-only file set；直接施工 Fact 会制造 dangling
provenance 或占位 Artifact。因而[文档 132](132-r1-derivation-input-binding-contract.md)只建立
`R1_DERIVATION_INPUT_BINDING_CONTRACT_CANDIDATE`：候选拟将已发布 Snapshot、sealed Policy、固定 Profile
与 exact local Git bytes 绑定成不发布的新 owned runtime value。它没有创建 runtime、parser、Fact、
Evidence、Relation、Slice、Coverage 或完整 Derivation Manifest；只有候选自身闭环与后继独立 docs-only
冻结发布全部成立后，才可能解除这一窄边界的实现停止线。

候选提交 `8706a8ecd9978c28615d2d686cbc7ce2727d7c64` 经 PR #112 原始 Public CI attempt 1 的 11/11 门禁
合入 `main@b807ee095630c14edd73621c43943437b6cdddff`。该 exact main 的 Public CI 11/11、Browser Smoke 1/1，
以及 README、文档 132 与 milestones 的 fresh anonymous P2 Collector 读回均成立。[文档 133](133-r1-derivation-input-binding-contract-freeze-publication.md)
只发布该闭环；其自身门禁、受保护主线合入、exact-main 门与匿名读回全部成立后，状态推进为
`R1_DERIVATION_INPUT_BINDING_CONTRACT_FROZEN / R1_DERIVATION_INPUT_IMPLEMENTATION_ALLOWED /
R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED / R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。
下一步只允许从新的 exact main 建立 Input Binding runtime 与合同二十二格证据；parser、Fact、Evidence、
Relation、Slice、Coverage、conflict / UNKNOWN 传播与完整 Derivation Manifest 仍不得启动。

Derivation Input runtime 从 exact `main@84512755b6475cfa40ca352f43e4cb7be953a761` 建立四路径有界读取、
三个 canonical Artifact 的独立复算与 cross-binding、exact local Git byte reacquisition，以及不发布的
copy-owned `DerivationInputSet`。实现审计发现宿主 CPython 3.13 的 `str.isidentifier()` 会接受 Python 3.10
尚未拥有的 Unicode code point，因此改用冻结 Python 3.10 词汇并以完整 identifier truth-set 摘要复验；
没有让宿主 runtime identity 倒灌 Profile。PR #114 head
`5447a0c0947c44cbbd80af6e90f74438b9950d1f` 的原始 Public CI attempt 1 为 11/11，随后以
`main@46bb81625b9f2dcb4fa1284bd75344e89ed4be5f` 合入。该 exact main 的 Public CI run
`34685266682` 为 11/11、Browser Smoke run `34685266683` 为 1/1，均为 attempt 1。当前只进入
`R1_DERIVATION_INPUT_IMPLEMENTED / FREEZE_CANDIDATE /
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`；[文档 134](134-r1-derivation-input-implementation-freeze-candidate.md)
记录二十二格合同矩阵、本地/远端证据和停止线。独立最终状态发布成立前不得写
`R1_DERIVATION_INPUT_FROZEN`，也不得把该绿灯传播为下游派生施工资格。

冻结候选经 docs-only PR #115 的原始 Public CI attempt 1 取得 11/11，并以
`main@aa7ff1140aa8c988e84b38808cb8cb1eebe3fbf3` 合入。新 exact main 的 Public CI 11/11、Browser
Smoke 1/1，以及 README 与文档 134 的 fresh anonymous P2 Collector exact-SHA 读回均成立。
[文档 135](135-r1-derivation-input-freeze-publication.md)独立发布这些事实；其自身最后门全部成立后，状态为
`R1_DERIVATION_INPUT_FROZEN / R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。冻结只覆盖
不发布 Artifact 的 Input Binding runtime；parser、Fact、Relation、Slice、Coverage、conflict / UNKNOWN
传播与完整 Derivation Manifest 仍须各自先完成合同闭环。

后继审计从 exact `main@7e0950ba2544476049e6defe1545f786971a89bd` 开始，不写 parser 或运行代码。
[文档 136](136-r1-derivation-attempt-and-fact-provenance-audit.md)确认必填 request provenance 没有连续来源、
capability-level Policy 尚未闭合 Provider applicability、memory/artifact budget 缺少 typed terminal code，
且 ProviderRun 与 Fact 目前只有单向引用。[文档 137](137-r1-derivation-attempt-and-fact-provenance-contract.md)
因此先建立 docs-only `R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE`：exact-only provenance、显式单
`python-ast` binding、共享绝对预算、application-owned Fact identity 与双向 provenance。候选明确要求先
完成 Evidence Schema/corpus 修正和真实 budget primitive feasibility；在它们各自独立冻结以前，runtime、
真实 parser、Relation、Slice、Coverage 与完整 Derivation Manifest 继续禁止。

候选经 PR #117 原始 Public CI attempt 1 的 11/11、受保护主线合入、
`main@4893b0062b397adc3983eecb0a7db7c9b24ab4c9` 的 Public CI 11/11 与 Browser Smoke 1/1，以及
README、文档 136/137 和 milestones 的已安装产品 fresh anonymous exact-SHA 读回后，由
[文档 138](138-r1-derivation-provenance-contract-freeze-publication.md)独立发布冻结事实。当前状态为
`R1_DERIVATION_PROVENANCE_CONTRACT_FROZEN /
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED /
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只允许后继从新 exact main 建立独立
Schema/corpus correction；它不授权 budget primitive、Provider、parser、Fact runtime 或任何下游对象。

后继从 exact `main@f69f2818d06834da0d9e8e95288f6f72aada6beb` 先做 docs-only Schema correction 审计。
[文档 139](139-r1-derivation-evidence-schema-correction-audit.md)以单变量变体证明旧 Schema 会接受
non-COMPLETED run/overall 的悬空 reported IDs，并拒绝 memory/artifact budget typed diagnostic；同时确认
文档 126 已冻结的 `0.1` Schema path、`$id` 与 public bytes 不能原位改写。[文档 140](140-r1-derivation-evidence-schema-correction-contract.md)
因此只建立自描述的 `DerivationEvidence 0.1.1` 补丁合同：旧 Schema/corpus/vector 原字节保留，其他 R1
Artifact、Manifest 与 digest projection 不升级。候选经 PR #119 原始 Public CI attempt 1 的 11/11、受保护
主线合入、`main@2973926358c686d86233dbc2054a2e1f064f13ad` 的 Public CI 11/11 与 Browser Smoke 1/1，
以及 README、文档 139/140 和 milestones 的已安装产品 fresh anonymous exact-SHA 读回后，由
[文档 141](141-r1-derivation-evidence-schema-correction-contract-freeze-publication.md)独立发布冻结事实。当前状态为
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_FROZEN /
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTATION_ALLOWED /
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只允许物化合同限定的 correction payload；其
独立冻结以后仍须先完成 budget primitive feasibility 与 runtime 授权。

后继从 exact `main@19cb4ff4300e6c7aeb08aa315802abb29e183d60` 物化独立的
`DerivationEvidence 0.1.1` root、`R1-DE-CV-001..010` correction corpus 与兼容守卫；旧 `0.1` 的十个
Schema 和十九个 corpus 文件继续逐字节不变。实现 PR #121 原始 Public CI attempt 1 为 11/11 success，
并以 `main@99826ec1564e8447524c477ff9f271fa5d062ea6` 完成 exact-main Public CI 11/11、Browser Smoke 1/1
与三项匿名逐字节读回。[文档 142](142-r1-derivation-evidence-schema-correction-implementation-freeze-candidate.md)
因此建立 docs-only 冻结候选，当前状态为
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTED /
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FREEZE_CANDIDATE /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该候选自己的原始远端门、受保护主线合入、
新 exact-main 门与匿名公开读回仍是最终冻结前置条件；budget primitive、Provider/parser、Fact runtime
及全部下游实现继续禁止。

R1 Schema 施工前又从真实门禁成本中显现出独立的 Verification Scheduling 问题。该问题不并入 R 轨或
Core，而以顶层候选 `Q` 轨建模：`Q = Quick`，只表示减少无效重算和可解除的串行等待，不授予降低证明
标准的权力。[能力地图](114-capability-boundary-and-system-map.md)记录跨轨道 Dependency/Authority Matrix，
[Q0 蓝图](116-q0-quick-verification-scheduling-blueprint.md)只冻结候选身份、权威、分层、反例与实现前置门。
候选经 PR #91 合入后，首次严格公开读回发现能力地图的 Mermaid 子资源使 P2 coverage 保持 `PARTIAL`；
PR #92 只把关系图改为等价静态文本，并在新的 exact main 上重新完成门禁与三次匿名产品读回。
[文档 117](117-q0-verification-scheduling-freeze-publication.md)发布此前的完整因果链。该状态发布合入后的
exact-main Public CI 随后在 E3 0.2 Release 下载门停止：旧实现把四级退避表误作
五次尝试上限，在 60 秒绝对恢复预算仍有约 29 秒时提前退出。独立
[文档 118](118-release-download-recovery-deadline-correction.md)只修正这一预算所有权，不改变 Q0、P4、资产坐标、
冻结 SHA-256 或错误接受边界。该修正经 PR #94 原始 11/11 门禁合入
`main@c2f488e8274b43dea6ad39402a94c3f6a1ee7753`；新 exact main 的 Public CI 11/11、Browser Smoke 1/1 与
README、文档 118、milestones 三次匿名产品读回均已成立。完整恢复链见
[文档 119](119-q0-verification-scheduling-final-freeze-closure.md)；该状态发布自身的门禁、受保护主线合入与
合入后匿名读回全部成立后，当前状态为
`Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY`：没有 Schema、源码、CLI、
缓存、调度器、CI 修改、标签或 Release，不预编 Q1–Qn，也不要求 R1 扩大为 base/head diff。下一步只
允许从新的 exact main 独立重构 README 读者骨架；SVG 随后独立施工，R1 Schema 尚未恢复。

- M11–M14 的规划边界见 [Post-M8 收束路线 Plan v1](13-post-m8-roadmap.md) 第 7–10 节。
