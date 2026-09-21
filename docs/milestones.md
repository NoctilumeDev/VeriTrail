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

候选随后经 PR #122 原始 Public CI attempt 1 的 11/11 合入
`main@a940259a4c286f64d39a92854397eea25c442e0f`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
以及 README、文档 142、milestones 三项已安装产品 fresh anonymous exact-SHA 读回均成立，Core 三次
均为 `PASS`。[文档 143](143-r1-derivation-evidence-schema-correction-freeze-publication.md)独立发布冻结事实；
其自身最后门全部成立后，当前状态为
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只允许后继建立独立 budget primitive
feasibility；Provider/parser、canonical Fact runtime 与下游对象仍须等待 feasibility 和后继明确授权。

后继审计从 exact `main@3a1374c2e7c5861ab9746052dceb8f50a1544d3e` 开始，不写 Provider/parser/Fact
或产品 runtime。[文档 144](144-r1-derivation-budget-primitive-precontract-audit.md)以当前 Windows 11、
Python 3.10/3.13 与锁定 pywin32 环境攻击旧预算模型：真实 Job 探针在八次 memory case 中均完成 pre-start
hard containment、positive memory-limit message、whole-Job termination 与 `ACTIVE_PROCESS_ZERO`，但 Win32
公共合同明确普通 Job completion message 不保证投递，因此 configured hard ceiling 与 terminal attribution
必须分离；deadline/cancellation tree probe 又证明绝对 deadline 是结果资格边界，物理 cleanup 必须使用一次
创建、全阶段共享且不恢复语义工作的 release envelope；正常 phase 则只有在 result 与其所有
execution resources 于 deadline 前一起闭合时才能成功。artifact 探针则证明 exact bytes producer-side
reservation 可在超限文件写前停止并删除 staging。

[文档 145](145-r1-derivation-budget-primitive-contract.md)据此建立 docs-only
`R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_CANDIDATE`：不改 `ReviewPolicy 0.1` 或
`DerivationEvidence 0.1.1`，只冻结 positive-event warrant、single terminal-stop latch、absolute acceptance
deadline、5 秒 cleanup-only release envelope 与 inclusive artifact reservation。当前没有 budget primitive
runtime、conformance harness、Provider、parser、Fact、Relation、Slice、Coverage 或 Manifest；候选自己的
远端门、主线合入、exact-main 门、匿名读回与后继独立冻结发布完成前，不得开始实现。

该候选经 PR #124 原始 Public CI attempt 1 的 11/11 合入
`main@9a969af10f705abe66ac7816bc27e9369ea7206a`；candidate tree 与 merge tree 相同。该 exact main 的
Public CI 11/11、Browser Smoke 1/1、六个候选路径匿名 raw bytes 读回，以及 README、文档 145、milestones
三次已安装产品 fresh anonymous exact-SHA 读回均成立，Core 三次为 `PASS`。冻结前第二轮系统俯瞰不以
finding 数量为目标：它只把 `COMPLETED_FOR_PHASE` 错作 BudgetContext terminal state 和 normal completion
check/terminal-stop latch 竞态认定为 Freeze blocker，并已在候选中最小修正；native binding/cleanup harness
保留为实现门，无正向 event 的 exit mapping 与跨平台 primitive 延期，单 lane 约 140 秒只记为资源事实。

[文档 146](146-r1-derivation-budget-primitive-contract-freeze-publication.md)独立发布冻结事实；其自身最后门
全部成立后，当前状态为
`R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_FROZEN /
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_ALLOWED /
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只允许从新 exact main 实现文档 145 的
budget primitive 与 `BP-001..016` conformance；Provider/parser/Fact 必须等待该实现自身冻结及后继明确授权，
Relation、Slice、Coverage、conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。

[文档 147](147-r1-derivation-budget-primitive-implementation-freeze-candidate.md)从独立 implementation PR #126
记录该 primitive 的实现与系统审计事实：base package 不依赖 `pywin32`，Windows extra exact 锁定
`pywin32==312`；共享 BudgetContext 使用 absolute deadline、single terminal-stop latch、inclusive artifact
reservation 和 cleanup-only release envelope；Job hard containment 与 terminal attribution 保持分离，只有
正向 memory-limit event 才能授权 `EXECUTION_MEMORY_BUDGET`。实现后审计修正了 local cleanup 冒充 global
release、expired context 仍可 resume worker，以及内部 attribution state 顶层导出三处接缝。第一次 PR head
只因 BP-014 用 `--no-build-isolation` 假设 ambient build backend 而红，未 rerun；独立测试修正后的新 head
原始 Public CI 11/11，随后合入 `main@8f8af815d1a566bbf35096e318d209bdc17bf7b3`，该 exact main 的
Public CI 11/11、Browser Smoke 1/1 与四项匿名 raw byte 读回成立。当前仍只是
`R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTED /
R1_DERIVATION_BUDGET_PRIMITIVE_FREEZE_CANDIDATE`；文档 147 自身的门、合入、exact-main 门、匿名产品读回
与后继最终状态发布完成前不得写成 frozen，也不得开始 Provider/parser/Fact、Relation、Slice、Coverage、
conflict/UNKNOWN 或完整 Derivation/Manifest。

[文档 148](148-r1-derivation-budget-primitive-freeze-publication.md)从候选合入基线
`main@571139df5db94159f5e439619176f17a02f86f94` 独立发布实现冻结。PR #127 第一个 docs-only head 的
Public CI 以 `startup_failure` 结束且没有实例化 jobs/check-runs；该 run 未 rerun，后继新 head 原始 Public CI
11/11、受保护主线合入、新 exact-main Public CI 11/11 与 Browser Smoke 1/1 均成立。第一次匿名已安装产品
读回又在 README 的 P1 API 命中公开额度 0；同次 P2 Render 完成但没有 Core PASS，输出被保留且未复用。
额度 reset 后从空 output 重建 README、文档 147 与 milestones 三个 paired session，均为 `PASS`，summary
digest 为 `0b3ae1e8ae68789c3b30253e1b5557e81404a1b754bed383cdac1e38596a988c`。文档 148 自身的原始门、
受保护主线合入、新 exact-main 门和针对本文坐标的 fresh anonymous 读回全部成立后，当前状态为
`R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。唯一下一步是重新审计 Derivation Attempt / Provider
Run / Fact provenance 接缝；审计不授权实现。Provider/parser/Fact、Relation、Slice、Coverage、
conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。

[文档 149](149-r1-derivation-execution-cell-system-audit.md)从 exact
`main@c33aeac9fa198bd8a0b9b5dc8340372757ba04b7` 重新审计冻结 Budget Primitive 与后继 Provider/Fact phase 的
组合语义。审计确认 hard memory containment 与 application-owned canonicalization 仍缺少共同 execution
topology，process primitive 尚无 bounded terminal envelope，primitive failure 后 context 仍可保持 `RUNNING`，
且无正向原因事件的 worker termination 没有已冻结公共映射。因此当前状态只推进到
`R1_DERIVATION_EXECUTION_CELL_PRECONTRACT_AUDITED /
R1_DERIVATION_EXECUTION_CELL_CONTRACT_NOT_STARTED /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只能起草 docs-only Execution Cell / Terminal
Envelope 合同；Schema 是否需要新 revision 必须由该合同裁决，不能由 runtime 先猜。Provider/parser/Fact、
Relation、Slice、Coverage、conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。

[文档 150](150-r1-derivation-execution-cell-terminal-envelope-contract.md)从 exact
`main@2de46c21997d85a437820decfeb2bd8bb7b69ee1` 起草上述 docs-only 最小合同。候选将 trusted controller、
contained application worker 与 Provider 分成不同 authority；具体 cell preparation 从 provisional budget t0
开始，成功后才原子 admit attempt 并启动 ProviderRun；request/result 使用 bounded、copy-owned、单终态规范
JSON frame；closed test launch binding 不恢复 ambient discovery；primitive/protocol/cleanup failure 会不可恢复地
撤销 attempt eligibility。当前裁决是不升级 `DerivationEvidence 0.1.1`：无合法 terminal envelope 且无更窄正向
warrant 的已启动 run 使用 `INTERNAL_DERIVATION_ERROR` 作为不声明平台/Provider 根因的 epistemic fallback。
当前状态为 `R1_DERIVATION_EXECUTION_CELL_CONTRACT_CANDIDATE /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该候选完成自己的远端、合入、exact-main、匿名读回与
独立冻结发布以前，不得实现 transport/test Provider/Fact phase，也不得开始真实 parser、Relation、Slice、
Coverage、conflict/UNKNOWN 或完整 Derivation/Manifest。

该候选由 PR #130 以提交 `ff801ba9cac96379bad851a1c822c2229dec0df2` 建立；原始 Public CI run
`34755844078`、attempt 1 完成 11/11 SUCCESS，随后合入 exact
`main@e1f91a94afb3e3afd4e85d3605240b77d379f57a`。该 main 的 Public CI run `34756474790` attempt 1
为 11/11 SUCCESS，Browser Smoke run `34756474928` attempt 1 为 1/1 SUCCESS；README、文档 150 与
milestones 三次 fresh anonymous installed-product paired readback 均由 Core 判为 PASS，summary digest 为
`481e864bc169ef50afdff0d28e8c3be0d8bbe6661cdddf74125b9ba3037217e9`。冻结前第二轮系统俯瞰只把“不同
attempt 的完整 Fact bytes 相同”与真实 `provenance_refs` 不可同时满足认定为 blocker，并已最小改为
provenance-free content/Fact ID invariance；其他 framing/platform/parser 风险保留为实现门或延期接缝。

[文档 151](151-r1-derivation-execution-cell-contract-freeze-publication.md)独立发布冻结事实。其自身最后门全部
成立后，状态为 `R1_DERIVATION_EXECUTION_CELL_CONTRACT_FROZEN /
R1_DERIVATION_EXECUTION_CELL_IMPLEMENTATION_ALLOWED /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只允许文档 150 的 attempt eligibility、bounded
frame codec、contained application worker、closed deterministic test Provider 与 copy-owned non-published Fact
phase result；真实 parser、FactSet/DerivationEvidence publication、Relation、conflict/UNKNOWN、Slice、Coverage
与完整 Derivation/Manifest 继续禁止。

[文档 152](152-r1-derivation-execution-cell-implementation-freeze-candidate.md)记录上述窄实现已经由 PR #132
从 exact 合同基线 `3c89f8eb94333986fc4901b9a1b91edf47d0059f` 施工。实现提交
`02e4d05dcfc7c062c97ecfa21c00b26f601b9140` 的原始 Public CI attempt 1 为 11/11 success，随后以
`main@8b77305cea3a95690660adcb25f76d2b42c6e5e1` 合入受保护主线；该 exact main 的 Public CI 11/11、
Browser Smoke 1/1 与全部十二个变更文件的匿名 exact-SHA byte readback 均成立。实现保持 controller、
contained application worker 与 closed test Provider 三层 authority，建立 bounded single-terminal framing、
不可恢复 attempt eligibility、positive-warrant terminal mapping 与 copy-owned non-published Fact phase result；
没有公开 execution-cell API，也没有真实 parser、FactSet/Evidence publication、Relation、Slice、Coverage 或
Manifest。实现后审计修正 rejected terminal identity leakage、primitive commit failure revoke、pre-admission
runtime loss mapping、release failure 与 late-stop/early-terminal 接缝；第一次受父进程 `PYTHONPATH` 污染的
BP-014 clean-wheel 结果被作废，并在 fresh interpreter 安装坐标上重建。当前状态只能记为
`R1_DERIVATION_EXECUTION_CELL_IMPLEMENTED /
R1_DERIVATION_EXECUTION_CELL_FREEZE_CANDIDATE /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。本文候选自己的门、合入、exact-main 门、匿名产品
读回与后继独立最终状态发布完成前，不得写成 frozen，也不得提前审计或实现下一个 provenance closure。

[文档 153](153-r1-derivation-execution-cell-freeze-publication.md)发布文档 152 候选的完整闭环。PR #133 的
base/head 为 `8b77305cea3a95690660adcb25f76d2b42c6e5e1` / `84a986010c42ef43f785e3725ea6d65b87d3b063`，
原始 Public CI attempt 1 为 11/11 SUCCESS；候选以 merge commit
`c2349b2a7c4d9ed002311d46f7212cb35856caf6`、tree `63239304e6d32479a888ebf1e5a077a4143292bb`
合入受保护主线。该 exact main 的 Public CI `34770503241` 为 11/11、Browser Smoke `34770503260` 为 1/1，
均是 attempt 1。fresh anonymous installed-product readback 对 README、文档 152 与 milestones 建立三次独立
paired session；三者均 HTTP 200、requested/final 相同、三样本稳定、无 stream/cleanup/coverage 残留且 Core
Verdict 为 PASS，summary digest 为 `94654f6f58fcf82a2a6230521164e8f98176dff1ab40e97d2c695a67d8c98045`。
文档 153 自身的原始门、受保护主线合入、新 exact-main 门与匿名产品读回全部成立后，状态才成为
`R1_DERIVATION_EXECUTION_CELL_FROZEN /
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。唯一后继是先审计 Provider Run 到 canonical Fact
admission 与 FactSet/DerivationEvidence closure eligibility；真实 parser、publication、Relation、
conflict/UNKNOWN、Slice、Coverage 与完整 Manifest 继续没有实现授权。

[文档 154](154-r1-fact-evidence-closure-system-audit.md)从 exact
`main@a96912fa3f141a783e728f95e0feb26341197a32` 执行该前合同系统审计。它确认 execution cell 已拥有
application-canonical Fact identity，但 FactSet admission、final Evidence reported-ID projection 与公共 Artifact
membership 仍是不同边界；COMPLETE 八文件合同禁止把 FactSet 或 completed Evidence 单独发布。审计用三个
Schema-valid、digest 不同的 `PROVIDER_FAILED` 单变量 Evidence 证明 run/top-level diagnostic placement 仍未
规范化，并确认 deadline/cancel/memory/artifact stop 后只有 cleanup permission 时，DIAGNOSTIC publication
是否存在、由哪份 artifact budget/eligibility 拥有尚未冻结。当前状态只推进到
`R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED /
R1_FACT_EVIDENCE_CLOSURE_CONTRACT_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只能从新的 exact main 起草 docs-only Fact
Admission / DerivationEvidence Closure 最小合同；真实 parser、Provider SPI、FactSet/Evidence publisher、
Relation、conflict/UNKNOWN、Slice、Coverage 与完整 Manifest implementation 继续禁止。

[文档 155](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)从 exact
`main@0b2ca79191adc3743b2cf4663cd0cda7574a7912` 起草 docs-only Fact Admission / DerivationEvidence
Closure 最小合同候选。它冻结四层 Fact identity/membership、phase 与 final Evidence reported-ID 的 immutable
projection、首个 single-Provider terminal diagnostic 的 run/top-level canonical placement，以及 normal
continuation、future DIAGNOSTIC closure 与 cleanup-only 三种独立 capability。有合法 phase result、且没有预算
stop 的 execution-cell non-success，只有在 release 已完成、原 BudgetContext 仍为 RUNNING、没有 stop latch 且
artifact reservation 为零时，才可取得一次性 future DIAGNOSTIC eligibility；deadline/cancel/memory/artifact
stop 与 RELEASE_FAILED 均不发布 R1 Artifact。
候选不定义 output path 或 publisher，当前状态只能是
`R1_FACT_EVIDENCE_CLOSURE_CONTRACT_CANDIDATE /
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。候选自己的远端门、受保护主线合入、exact-main 门、
匿名产品读回与后继独立冻结发布完成前，不得开始 runtime、public Artifact、real parser、Relation、Slice、
Coverage 或完整 Manifest 实现。

[文档 156](156-r1-fact-evidence-closure-contract-freeze-publication.md)从候选合入基线
`main@3c237555b4924f08b7e82c523f675fbd28512e3c` 独立发布冻结事实。PR #136 base/head 为
`0b2ca79191adc3743b2cf4663cd0cda7574a7912` / `a9eb0c77c311423c14104f50de87a1604438e4e4`，原始
Public CI run `34793979272` attempt 1 为 11/11 SUCCESS；候选以 merge commit
`3c237555b4924f08b7e82c523f675fbd28512e3c`、tree `b2bc95fbc51f57cd895634361b5fdae81baad6cf`
合入受保护主线。该 exact main 的 Public CI `34794900875` 为 11/11、Browser Smoke `34794900949` 为 1/1，
均是 attempt 1；README、文档 155 与 milestones 三次 fresh anonymous installed-product paired readback 均为
HTTP 200、三样本稳定、P1/P2 coverage COMPLETE、无 stream/cleanup/conflict 残留且 Core Verdict 为 PASS。
冻结前第二轮系统审计用现有 Schema/correction fixture 构造 7 个 active-run terminal projection 与 1 个
artifact-budget projection，全部通过 Schema、固定 status/cardinality、空 reported IDs 与 digest 复算；未发现
新 blocker。文档 156 自身的远端门、受保护主线合入、新 exact-main 双门与匿名产品读回全部成立后，状态才是
`R1_FACT_EVIDENCE_CLOSURE_CONTRACT_FROZEN /
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_ALLOWED /
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。授权只覆盖文档 155 第 13 节 A–F 的 private、
non-published closure；output path/publisher、real parser、Relation、Slice、Coverage 与完整 Manifest 继续禁止。

[文档 157](157-r1-fact-evidence-closure-implementation-freeze-candidate.md)记录文档 155/156 授权的 private
Fact/Evidence closure 已完成实现、系统审计并由 PR #140 合入受保护主线。实现把 existing execution-cell
拆成 one-shot prepared attempt 与 consume boundary，在同一 BudgetContext、attempt eligibility、inputs、binding
与 phase snapshot 上完成 application-canonical Fact admission、owned non-published FactSet construction state、
non-success Evidence projection 与一次性 diagnostic eligibility；没有 output path、publisher、真实 parser、
Provider SPI、Relation、conflict/UNKNOWN、Slice、Coverage 或 Manifest 能力。

PR #140 的首次 pre-rebase Public CI 在 Python 3.10 aggregated job 到达既有 15 分钟 outer timeout 后被取消；
该失败事实被保留，没有称为 flake 或 rerun 洗白。独立 PR #141 只把 workflow 外层 containment 调整为 20 分钟，
不修改任何 inner product timeout、gate 或 acceptance threshold；其原始 11/11、exact-main 双门与匿名 workflow
byte readback 均成立。实现以相同 patch-id rebase 后，PR #140 原始有效 Public CI 为 11/11，并以
`main@86b62464b9eef00a5e9da8d0549f093767be27e2` 合入；该 exact main 的 Public CI 11/11、Browser Smoke
1/1、五个变更文件匿名 exact-SHA 读回与 clean-wheel isolated site-packages probe 均成立。冻结前系统审计未
发现新 blocker，focused FA/boundary 27 项在 CPython 3.10/3.13 normal/`-O` 四格均通过。当前状态只能是：

```text
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTED
R1_FACT_EVIDENCE_CLOSURE_FREEZE_CANDIDATE
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

文档 157 自己的远端门、受保护主线合入、新 exact-main 双门、匿名 installed-product readback 与后继独立最终
状态发布完成前，不得写成 frozen，也不得开始 public Artifact、真实 parser、Relation、Slice、Coverage 或完整
Derivation 实现。

[文档 158](158-r1-fact-evidence-closure-freeze-publication.md)从候选合入基线
`main@a4c63607d8a586a5ec19eae1cdc4279cda1ffa88` 独立发布实现冻结事实。实现候选 PR #142 的原始 Public CI
为 11/11 SUCCESS；候选合入后的 exact-main Public CI 为 11/11、Browser Smoke 为 1/1。fresh venv 中从
`site-packages` 导入公开 Core 0.13.0、GitHub Evidence 0.1.0 与 Playwright 1.62.0，针对 README、文档 157 与
milestones 建立三次独立的 R1 专属 anonymous exact-SHA readback，P1/P2 coverage 均为 COMPLETE、三样本稳定、
Core 均为 PASS，规范 summary 联合 SHA-256 为
`b967c60409f495245b91727f447c28581adf58adefe98b38d1c92795c62e1ee2`。最初三次运行误用
`P4_REAL_GITHUB_RELEASE_CANDIDATE` label，虽技术路径通过，但不能证明 R1 candidate intent；这些证据已作废，
没有进入冻结链。

文档 158 自身的原始门、受保护主线合入、新 exact-main 双门与 fresh anonymous installed-product readback 全部
成立后，当前状态才是：

```text
R1_FACT_EVIDENCE_CLOSURE_FROZEN
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步必须从新的 exact main 再做系统级俯瞰，比较延期接缝后只选择一个最小合同；文档 158 不预先承诺
publisher、parser、multi-Provider Fact 或 Relation 谁先施工，也不授权直接开始 Slice、Coverage 或完整 Derivation。

[文档 159](159-r1-post-fact-evidence-next-closure-system-audit.md)从 exact
`main@7141999383489f51cf6f87806d2d271496499584` 执行上述系统级俯瞰。审计把 DIAGNOSTIC publisher 认定为
合法但正交的失败留档闭环，把 COMPLETE publisher 判定为必须等待八文件 closure，并确认 real parser 若先行会让
首个实现替合同决定 Provider applicability。multi-Provider 的 exact descriptor set、共享 BudgetContext、
required/optional status join、same-ID provenance merge 与 same-subject conflict 会同时改变 FactSet、Evidence、
Relation 输入、Slice conflict gate 与 Coverage `UNKNOWN`，因此它是当前多个后继共同依赖的 authority bottleneck。
本文自己的远端门、受保护主线合入、新 exact-main Public CI / Browser Smoke 与 R1 专属 fresh anonymous
public readback 全部成立后，状态才是：

```text
R1_FACT_EVIDENCE_CLOSURE_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只能从新 exact main 起草 docs-only Multi-Provider Applicability and Fact Composition Contract 0.1；审计不
授权 runtime。real parser、public Provider SPI/discovery、DIAGNOSTIC/COMPLETE publisher、Relation、Slice、
Coverage、CLI 与 Workbench 继续禁止。

[文档 160](160-r1-multi-provider-applicability-and-fact-composition-contract.md)从 exact
`main@22df05698f05380e910ac8a4e0cc6ba1276842e7` 建立该 docs-only 候选。首个 closed conformance profile 只由
application-owned 固定表把 sealed capability requirement 映射为 exact descriptor/binding tuple；不扫描 ambient
installation，也不创建 public registry。requiredness 由 requirement 继承，所有 run 严格串行消费同一
BudgetContext；每个来源先完成 run-local conformance，再跨来源执行 same-ID semantic merge/provenance union 与
same-subject conflict construction。required/optional terminal join、composition-level unknown attribution、final
reported-ID 清空与 conflict-bearing FactSet continuation 均由机械规则约束。现有 Schema/corpus/vector bytes 保持
不变，因为本切片仍不发布 Artifact，且现有 shape 已能表达多 run、provenance union、FactConflict 与 optional
non-success。当前状态只能是：

```text
R1_FACT_EVIDENCE_CLOSURE_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

候选自己的原始远端门、受保护主线合入、新 exact-main 双门、R1 专属 fresh anonymous product readback 与后继
独立 docs-only 冻结发布全部成立前，不得开始实现。即使以后冻结，也只允许 private closed test applicability、
multi-Provider execution/composition 与 `MP-001..028`；real parser、public Provider authorization/SPI/discovery、
publisher、Relation、Slice、Coverage、Manifest、CLI 与 Workbench 继续未授权。

[文档 161](161-r1-multi-provider-fact-composition-contract-freeze-publication.md)从候选合入基线
`main@9c336e02318791b411c9abfa8cf662fb97f61f47` 独立发布冻结事实。PR #145 原始 Public CI attempt 1 为
11/11 SUCCESS；候选 exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。fresh CPython 3.13 venv
匿名下载并复算 Core 0.13.0 与 GitHub Evidence 0.1.0 wheel，安装 Playwright 1.62.0 与 matching Chromium，
随后针对 README、文档 160 与 milestones 建立三次独立 R1 专属 readback；三者均 HTTP 200、requested/final
相同、P1/P2 coverage COMPLETE、三样本稳定、零 conflict/coverage reason/cleanup error，Core 均为 PASS。
三份 canonical summary 的联合 SHA-256 为
`82a160f94a5e8f5bc8adfaf836e886c6b70f3c7f28cf31e2131b1813a4ff0905`。

文档 161 自身的原始门、受保护主线合入、新 exact-main 双门与 fresh anonymous installed-product readback
全部成立后，当前状态才是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_ALLOWED
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该授权只覆盖 private closed applicability table、一个 parent composition attempt、共享 BudgetContext、严格串行
single-Provider child cells、run-local conformance、same-ID merge、same-subject FactConflict、terminal join 与
`MP-001..028`。real parser、public Provider authorization/SPI/discovery、publisher、Relation、Slice、Coverage、
Manifest、CLI 与 Workbench 继续未授权；实现必须从新 exact main 独立开始，不能从合同分支续写。

[文档 162](162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md)记录该 private 实现由
PR #147 以提交 `f23c042cf11f872da2e6413d4c0ee76210fb43e7` 建立；原始 Public CI run
`34880944564` 为 attempt 1、11/11 SUCCESS。实现以普通 merge commit
`main@590df332fbd60bdfc857a4ea3f3c35937ce03d8a` 合入，candidate 与 merge tree 均为
`4814149bc175886bdcc92ffc45fd65376373a4ba`；新 exact main 的 Public CI run `34882727275` 为 attempt 1、
11/11 SUCCESS，Browser Smoke run `34882727435` 为 attempt 1、1/1 SUCCESS。全部七个变更文件又从该 exact
SHA 完成无 token raw-byte 读回，逐项与 Git tree 同大小、同 SHA-256 和同 blob identity，规范行摘要为
`8ecdf360ffea918222c565bd9530bf4990e454b6f56d5a0a8f78ae6ac6fcadda`。实现保持一个 parent budget、严格
串行 children、run-local closure、Fact merge/conflict、terminal join、private non-published projection 与
`MP-001..028`；没有新增 public API、默认依赖、Artifact writer 或延期能力。当前状态只能是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTED
R1_MULTI_PROVIDER_FACT_COMPOSITION_FREEZE_CANDIDATE
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

文档 162 自己的远端门、受保护主线合入、新 exact-main 双门、R1 专属 fresh anonymous installed-product
readback 与后继独立最终状态发布完成前，不得写成 frozen。后继不得直接开始 real parser、public Provider
SPI/discovery、publisher、Relation、Slice、Coverage、Manifest、CLI 或 Workbench；冻结后仍须先做系统级审计，
再选择一个最小合同闭环。

[文档 163](163-r1-multi-provider-fact-composition-freeze-publication.md)从候选合入基线
`main@66b2252c5261387e1d1b40899f3e009e6ed6cecf` 独立发布实现冻结事实。实现候选 PR #148 的原始 Public CI
run `34885652717` 为 attempt 1、11/11 SUCCESS；候选 exact main 的 Public CI run `34887431677` 为 attempt 1、
11/11 SUCCESS，Browser Smoke run `34887431658` 为 attempt 1、1/1 SUCCESS。fresh venv 匿名下载并复算
Core 0.13.0 与 GitHub Evidence 0.1.0 固定 Release wheel，安装 Playwright 1.62.0 与 matching Chromium；README、
文档 162 与 milestones 的三次 R1 专属 readback 均为 HTTP 200、P1/P2 COMPLETE、三样本稳定、零 conflict/
coverage reason/cleanup error、Core PASS，三 session 与三 sealed Plan 均不复用，联合 summary SHA-256 为
`c098ffeefea338b9ab220bca0e2c521ec5d0faaae9970699367c20deab8fa7da`。第一次 README readback 的工具
`plan_id` 长度不合法，在 browser collection 与 output directory 前被 Core validator 拒绝；该尝试未计入通过
证据，修正后从新目录建立有效 attempt 2。

文档 163 自身的原始门、受保护主线合入、新 exact-main 双门与 fresh anonymous installed-product readback
全部成立后，当前状态才是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步必须从新的 exact main 再做系统级俯瞰，比较 DIAGNOSTIC publisher、real parser/provider boundary、
Relation/conflict/UNKNOWN、Slice、Coverage 与 COMPLETE publisher 后只选择一个最小合同。本文不预先决定顺序，
也不授权同时启动多条后继实现。

[文档 164](164-r1-post-composition-next-closure-system-audit.md)从 exact
`main@3575cc90faffd41c7172339f461c583e748f2215` 执行上述系统级俯瞰。审计确认公共 Relation Schema 与
valid-complete fixture 只能证明 shape/identity capability；当前 runtime 的 Provider terminal 只交付 Facts，
`reported_relation_ids` 固定为空。`IMPORT_TARGET_LITERAL` 的 resolution 又依赖 multi-Provider composition 后的
exact FactSet，而现有 Provider operands identity 不绑定 `fact_set_digest`。若先实现 parser、Relation 或 Slice，
实现将被迫在“原 Provider 自报、第二阶段 Provider、application 派生或隐藏 recipe”之间替合同选择，并可能虚构
Relation provenance。因此下一最小合同只选择 Relation derivation authority、exact FactSet operand continuity、
ProviderRun/reporting provenance 以及 minimum upstream eligibility gate；完整 Relation 算法、RelationSet
composition/admission 与 conflict/UNKNOWN 账册不因本审计自动进入同一合同。

本文自己的远端门、受保护主线合入、新 exact-main Public CI / Browser Smoke 与 R1 专属 fresh anonymous
installed-product readback 全部成立后，状态才是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_PRECONTRACT_AUDITED
R1_RELATION_DERIVATION_CONTRACT_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只能从新 exact main 先复核文档 164 的反证条件，再起草独立 docs-only Relation Derivation Authority and
Operand Continuity Contract 0.1。审计不授权 Schema/runtime；facts-only real parser 是可独立审议的后继，但
不得替 Relation 决定跨阶段 authority；public Provider SPI/discovery、完整 RelationSet composition/admission、
DIAGNOSTIC/COMPLETE publisher、Slice、Coverage、CLI 与 Workbench 继续禁止。

文档 164 的最后门现已按 `main@41a398783d5eaf25e15574df5beafb8465d0a91e` 核实。PR #150 head 的原始
11 项 required checks 全绿；合入后 Public CI run `34930110622` attempt 1 保留 10/11 FAILURE：E3 第四份
Release asset 六次 HTTP 500，在冻结的 60 秒有界恢复预算内停止，clean-install acceptance 当时未运行。
failed-jobs rerun 的 attempt 2 最终组合 11/11 SUCCESS，仅 E3 在第二次窗口重新执行并通过资产校验与
acceptance，其他十项沿用首次成功事实；Browser Smoke run `34930110603` attempt 1 为 1/1 SUCCESS。
fresh CPython 3.13.13 venv 匿名首次下载并复算 Core 0.13.0 与 GitHub Evidence 0.1.0 冻结 wheel，安装
Playwright 1.62.0 与 matching Chromium；README、文档 164、milestones 按顺序建立三个互不复用的
P1→P2→P3→Core session，均为 HTTP 200、P1/P2 COMPLETE、三样本稳定、marker 恰好一次、零 conflict/
coverage reason/cleanup error、Core PASS。三份 canonical summary 的联合 SHA-256 为
`9fd68f63fc6ce3ea60f1d3aea014b8c61018b8f9adadd9637ad9bc79cbed08bf`。attempt 2 的绿色组合结果
没有抹掉 attempt 1 的红灯，也不能解释成十一项全部新跑。

[文档 165](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)从该新 exact main 独立复核
文档 164 第 4.1 节的五项反证，未发现推翻选题的新证据，并起草最小 docs-only 合同候选。首个 closed proof
候选让 newly sealed `review-relation-derivation` requirement 对应一个 composed FactSet 后的 distinct
Relation ProviderRun；Relation 候选只归因于真实 Relation run，Fact runs 不回填报告，application 不自造
Relation target。relation-only operands `/0.2` 是**未冻结的版本化投影提案**，须显式绑定
`fact_set_digest`，并证明外部 verifier/identity vector 可复算。新 profile 的 Fact-stage private join 必须
先构造 FactSet，Relation terminal 后才形成 final overall；不得让 required Relation run 与 FactSet 循环
等待。当前 Fact-only wire 不得冒充 Relation terminal。首版 FactConflict、optional-source gap 与 absent normal FactSet 保留 typed upstream truth，
不建立较小 normal Relation world。当前分支状态只为：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_PRECONTRACT_AUDITED
R1_RELATION_DERIVATION_CONTRACT_CANDIDATE
R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

文档 165 自己的 focused/local 门、原始远端门、受保护合入、新 exact-main 双门、R1 专属匿名读回与后继独立
冻结发布成立前不得写成合同 FROZEN 或进入实现。真实 parser、public Provider SPI/discovery、完整 Relation
算法、RelationSet composition/admission、Schema/runtime correction、publisher/Manifest、Slice、Coverage、
CLI 与 Workbench 仍未授权；这些问题不能因为本候选选择 producer 模型而自动并入同一施工。

[文档 170](170-r1-relation-derivation-contract-freeze-publication.md)从当前
`main@8e5c0007c20b8c495195cdbdbb3a68891d88c3df` 独立发布该最小合同。它绑定候选 PR #151 的
base `41a398783d5eaf25e15574df5beafb8465d0a91e`、head
`8ccc1066d665d2b7e290f929c2c84f22645def01`、merge
`301f5248b77c67284b5e52bf287c23f286590e6b` 与 tree
`c82cb015516e817304e0ea8804dfc9375c9e1627`。候选 Public CI run `34953748989` attempt 1 保留
10/11 FAILURE；failed-jobs rerun 只新执行失败的 Python 3.13 wheel-only job。随后同一 head 的全新 run
`34955710084` attempt 1 为 11/11 SUCCESS。候选 exact main 的 Public CI run `34957252663` 为 11/11，
Browser Smoke run `34957252725` 为 1/1；README、文档 165、milestones 三次匿名 installed-product
readback 均为 P1/P2 COMPLETE、三样本稳定、唯一 marker、零 conflict/error/cleanup error、Core PASS，联合
summary SHA-256 为 `b099b3b49b9092f915f684768807896ac4be616e4dd73f0cac9a326547d04b6c`。

文档 168/169 后续收紧 source-state continuity 与 GitHub workflow/attempt authority，但不改写 R1 候选历史，
也未提供推翻 Relation authority、FactSet operand continuity、phase join 或 upstream gate 的新证据。本文自己
的本地门、原始远端门、受保护合入、新 exact-main 双门与三次 fresh anonymous installed-product readback
全部成立后，状态才是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_PRECONTRACT_AUDITED
R1_RELATION_DERIVATION_CONTRACT_FROZEN
R1_RELATION_DERIVATION_IMPLEMENTATION_ALLOWED
R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该冻结只允许 relation-only `provider-operands/0.2` identity/vector、固定 Fact/Relation phase join、distinct
relation-only request/terminal、首版保守 upstream gate、原 live `BudgetContext` 与 `RD-001..017` 的 private
closed implementation。若 Provider 不实际使用 parser，必须先独立审议最小 Evidence 修正，不得虚填身份。
完整 Relation algorithm/import resolution、RelationSet composition/admission、conflict/UNKNOWN 扩展资格、
public Provider、publisher/Manifest、Slice、Coverage、CLI、Workbench、D、Cu 与 Q 继续未授权。

[文档 171](171-r1-relation-derivation-implementation-freeze-candidate.md)记录该 private closed 实现由
PR #156 以提交 `db6148020b3333104a93ec602c7a7c1c5a5e3ab6` 建立；原始 Public CI run
`35512727369` 为 attempt 1、11/11 SUCCESS。实现以普通 merge commit
`main@122d0c6b9d3c7a4518f12aec2f503f8979018dda` 合入，candidate 与 merge tree 均为
`5db4e21a7fceda54eab184b0fea498d365da1fee`；新 exact main 的 Public CI run `35513598312` 为 attempt 1、
11/11 SUCCESS，Browser Smoke run `35513598411` 为 attempt 1、1/1 SUCCESS。全部十一份变更文件又从该 exact
SHA 完成无 token raw-byte 读回，逐项与 Git tree 同大小、同 SHA-256 和同 blob identity，规范行摘要为
`52510795bf4a479d3f6b58cd1aaa643eb0560d6f764f726b89ee0c9e37b8ea4f`。

实现物化 relation-only `provider-operands/0.2`、独立 Relation cell、固定 phase join、保守 upstream gate、共享
live `BudgetContext`、真实 Python 3.10 grammar parser identity 与 `RD-001..017`。它没有 public export、文件
publisher、完整 import resolution、RelationSet admission、RelationConflict、Slice 或 Coverage。当前状态只能是：

```text
R1_RELATION_DERIVATION_IMPLEMENTED
R1_RELATION_DERIVATION_FREEZE_CANDIDATE
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

文档 171 自己的远端门、受保护主线合入、新 exact-main 双门、R1 专属 fresh anonymous installed-product
readback 与后继独立最终状态发布完成前，不得写成 frozen。后继不得直接开始完整 Relation algorithm、真实
import resolution、RelationSet、publisher、Slice、Coverage、CLI 或 Workbench；冻结后仍须先做系统级俯瞰，
再选择一个最小合同闭环。

[文档 172](172-r1-relation-derivation-freeze-publication.md)从候选合入基线
`main@eb75d360b828fd45007be9f94892e4101af27e50` 独立发布实现冻结事实。PR #157 原始 Public CI run
`35514936331` 为 attempt 1、11/11 SUCCESS；candidate exact main 的 Public CI run `35515864709` 为
attempt 1、11/11 SUCCESS，Browser Smoke run `35515864729` 为 attempt 1、1/1 SUCCESS。README、文档 171 与
milestones 三次正式 fresh anonymous installed-product readback 均为 P1/P2 COMPLETE、三样本稳定、唯一 marker、
零 conflict/error/cleanup error 与 Core PASS，联合 manifest SHA-256 为
`8cd8efe6499cd754ab2668e87e8534c26858a178fd65da55141ae8a1761746d2`。

第一条 README session `github-paired-79f112178b8a48829710e7d47aaec085` 的 P2 在 final-health 成功后留下
`PublicRenderNetworkError / ERROR`，继续作为不合格事实保留。源码、合同与后继同型计数证明两个
coverage-neutral telemetry write 不是已证原因；0.1 Artifact 无法恢复精确 response-stage 根因，因此保持
`UNKNOWN`。旁路诊断 session 不进入门禁；后继正式成功使用新 sealed execution、session 与输出根，不改写首败。

文档 172 自己的原始远端门、受保护主线合入、新 exact-main 双门与三次 fresh anonymous installed-product
readback 全部成立后，当前状态才是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

冻结后必须从新 exact main 先做 system audit；完整 Relation algorithm、import resolution、RelationSet、
conflict/UNKNOWN、publisher、Slice、Coverage、CLI 与 Workbench 不因本状态发布自动取得施工授权。

[文档 173](173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md)从冻结 exact
`main@d54ee43170779f54ec88b9839ad80d48056aa033` 独立俯瞰下一闭环。只读本地反例在 source
`import pkg.mod`、MODULE + IMPORT_DECLARATION FactSet 与冻结双-kind Profile 上得到：Fact stage、Relation
ProviderRun 与 final private phase 都是 `COMPLETED`，但 Provider 只报告一个 `LEXICAL_CONTAINS` candidate，
没有 `IMPORT_TARGET_LITERAL`；final Evidence IDs 仍正确保持空。该事实不击穿文档 165/172 的 bounded private
proof，却证明 `ProviderRun COMPLETED` 不能升级为本轮 declared Relation observation obligations 已全部履行。

Policy 0.1 能固定 capability requiredness 与 `CUMULATIVE`，Profile 能固定 relation-kind 闭集与 rank，现有
descriptor/Relation request/RelationSet shape 却没有绑定 source responsibility、observation subject denominator
或 observation-domain qualification。若直接做 RelationSet admission，后继会被迫把“来源正常结束”偷换成“已经看够”。
因此下一问题面识别为 declared Relation observation domain / composition qualification，先审议 required source-set terminal、
successful-empty 边界、multi-source same-ID union/conflict 与 qualification identity；RelationSet admission、完整
algorithm/import resolution、real parser/public Provider、final Evidence、Slice、Coverage 与 publisher继续延期。

文档 173 自己的原始远端门、受保护主线合入、新 exact-main Public CI / Browser Smoke 与三次专属 fresh
anonymous installed-product readback 全部成立后，当前状态才是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该最后门现已成立：PR #159 head `a00c0fb9f31f4b4282560bb554b59d7aa05627fb` 的原始 Public CI 为
attempt 1、11/11 SUCCESS，合入后的 exact `main@559bf9b9a052f0b542227b1cea069dd15c696cc8` 上，Public CI
run `35527351489` 为 attempt 1、11/11 SUCCESS，Browser Smoke run `35527351523` 为 attempt 1、1/1
SUCCESS。README、文档 173 与 milestones 使用三个不同 sealed Plan 和 collection session 完成 fresh anonymous
installed-product readback，P1/P2 均 `COMPLETE`、HTTP 200、三样本稳定、唯一 marker、零
conflict/error/coverage reason/cleanup error/active stream，Core 均为 `PASS`。联合 canonical manifest 的
`sha256_json` 为 `6a88636093691394ced966199c153bd9cc95e331fadbcc968aebfd48436c6fe1`。

[文档 175](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)的首份语义候选最初只从该审计 exact
main 起草 docs-only 最小合同。候选用 private observation profile 区分 Profile vocabulary 与 required
observation families；从 exact FactSet 为 lexical target Fact 与 import source Fact 机械建立 observation items，
再把 items 预先分配给 exact A/B required Relation sources。A 负责 lexical，B 负责 lexical 与 import-literal，
两者同属 sealed `CUMULATIVE` capability、共享原 live BudgetContext；新的 relation-only operands `/0.3` 与
private relation-cell `/0.2` 绑定 exact domain，不改写历史 `/0.2` operands 或 `/0.1` wire。

Provider terminal、required source-set terminal closure、source-local item closure 与 candidate composition
分别保存。冻结 `observation_profile_digest` 绑定 family/negative policy/Provider responsibility semantics；同一个
FactSet 不能在责任语义变化后沿用旧 domain。与每个 terminal run 绑定的 private relation-cell terminal 另报
explicit per-item outcomes，application 对 outcomes 与 candidates 双向
对账；定义 denominator 不等于履行义务，candidate absence 也不能生成 negative。
`RO-006/007` 固定 non-empty 零 candidate/无 outcomes 与 partial candidate/漏 outcome 都不得 qualification。
complete-empty 必须同时具有 empty assigned item set、真实 start、`COMPLETED`、empty outcomes/candidates 与
residue-free release；漏 outcome 或 unexpected candidate 不反写 truthful run terminal，但会否决 qualification。
same-ID candidate 只合并 provenance；same-subject incompatibility 可以与 observation closure `COMPLETE` 同时
存在，必须保留 private conflict，不能任选 winner。现有 RelationSet 0.1 与 Evidence 0.1.1 没有 responsibility、
domain 或 receipt binding，不能凭 shape 证明 qualification；因此本合同不授权 RelationSet 或 public Artifact。

当前状态只能是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_CANDIDATE
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

候选自己的原始远端门、受保护主线合入、exact-main 双门、专属匿名产品读回与后继独立 docs-only 合同冻结
发布成立前，不得开始 runtime。完整 Relation algorithm/import resolution、public Provider、Schema correction、
RelationSet admission、final Evidence、publisher、Slice、Coverage、CLI 与 Workbench 继续延期。

本轮没有触发外部 production failure-shape survey：本地冻结 bytes 已提供决定性反例。若后继合同仍无法在
responsibility/denominator/omission receipt 方案之间选择，才按 failure family 查公开一手案例，再回到本地
反例验证；外部案例不直接产生 R 的合同 authority。

[文档 174](174-m10-listener-owner-mismatch-fixture-timing-correction.md)记录后继 docs-only PR #160 的原始
Python 3.13 Public CI 在真正执行 450 tests 后，由既有 listener-owner-mismatch 测试夹具停止。该正式首败
继续保留；诊断证明 application 争议场景的 dependency readiness 会提前消耗 `1.5s` external listener 寿命，
而把寿命延长到 `30s` 又会因端口未在 cleanup deadline 内释放而合法得到 `CLEANUP_ERROR`。最小维护只把
外部 owner 的建立时刻移到 disputed node 进入既有 readiness adapter 的真实起点，不改变 runtime、timeout、
合同或错误接受边界。目标用例、完整 bootstrap module 与显式绑定四个当前 source root 的 450-test broader
suite 已在双 Python normal/`-O` 四格成立；后者不冒充 installed-product/CI topology。维护 PR #161 原始
Public CI run `35532371731` attempt 1 为 11/11，随后受保护合入 `main@962251d91bc2695afe984ee47845ac4fe1a80f7e`；该 exact main 的
Public CI run `35533373276` attempt 1 为 11/11，Browser Smoke run `35533373269` attempt 1 为 1/1。

PR #160 原始 head `44caffaa08ab67bcb83760d86bdbad7e30081b6f` 的正式 Python 3.13 首败继续保留，
没有以维护绿色或旧 head rerun 覆盖。合同语义没有被 maintenance 改写；文档 175 当前只从上述
maintenance-qualified exact main 重新绑定 source state、形成新 head 并重新接受完整门禁。

[文档 176](176-r1-relation-observation-composition-qualification-contract-freeze-publication.md)从
`main@bc495eb92c70f85566505d51d00677ac14f38ff2` 独立发布该最小合同。重新资格化 head
`fde8df8279c27b5a222d58d2b0a5fd73c261a54f` 的有效 PR Public CI run `35534770529` attempt 1 为
11/11 SUCCESS；PR body edit 触发的同 head run `35534733454` 被 concurrency 行政取消，没有形成完整测试
结论。候选合入后的 exact-main Public CI run `35535740629` 为 attempt 1、11/11 SUCCESS，Browser Smoke
run `35535740617` 为 attempt 1、1/1 SUCCESS。

README、文档 175 与 milestones 使用三个不同 sealed Plan、collection session 与 output root 完成 fresh
anonymous installed-product readback，P1/P2 均 `COMPLETE`、HTTP 200、requested/final exact SHA path 一致、
三样本稳定、唯一 marker、零 conflict/error/coverage reason/cleanup error/active stream，Core 均为 `PASS`。
联合 canonical manifest 的 `sha256_json` 为
`0df7a15fb0193f2d86d26b07fc96991cdada73d28058e5edb6e7cbf426bc194c`。

本文自己的本地门、原始远端门、受保护合入、新 exact-main 双门与 README/本文/milestones 三次专属 fresh
anonymous installed-product readback 全部成立后，状态才是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_ALLOWED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该冻结只允许文档 175 A–H 的 private observation profile、FactSet-derived items、A/B responsibility、
relation-only operands `/0.3`、private relation-cell `/0.2`、per-item outcomes、receipts、candidate composition 与
owned qualification result。完整 Relation algorithm/import resolution、public Provider、公共 Schema、RelationSet
admission、final Evidence、publisher、Slice、Coverage、CLI、Workbench、D、Cu 与 Q 继续未授权。

[文档 177](177-m10-ci-fixture-observation-correction.md)记录后继 private implementation PR #165 原始 Public CI
run `35569800950` 的两条不同正式首败。Python 3.13 `-O` 的 emergency-cleanup 用例在 cleanup 调用前发现
预选端口仍为空；源码审计证明旧夹具先关闭 port-0 probe、稍后才要求 child 绑定该具体端口，把瞬时空闲观察
误作预约。旧 Artifact 没有 child stderr、exit status 或 listener owner，因而只证明夹具前置条件未成立，
不能恢复该次失败的唯一底层触发。Python 3.10 `-O` 的 repeat 公共 Run 已完成 service readiness，但 Browser
collector fail closed 为
`COLLECTOR_ERROR`；现有冻结 Artifact 与 CLI summary 无法恢复 private error type，定向本地复验也未稳定复现，
因此精确根因保持 `UNKNOWN`。

独立 L0 maintenance 只让 emergency-cleanup child 自己绑定 port 0，并在 `listen()` 成功后把实际端口报告给
测试；repeat 用例只在测试层记录并立即重抛 `ObservedBrowserCollectionError`，deterministic sentinel 证明
诊断钩子不吞错误或改变公共结果。它不修改 runtime、timeout、Browser collector、公共 Evidence、R1 合同或
#165 实现。三个精确用例已在双 Python normal/`-O` 四格各 3/3 成立，完整 public bootstrap CLI 加 M10
stress 两个 module 在同一四格各 27/27 成立；完整 Core current-source 451-test 也在双 Python normal/`-O`
四格分别以 150.647s、139.365s、135.696s、136.843s 全部通过。该本地门不冒充远端 installed/editable
topology；维护 PR、自身 exact-main Public CI 与 Browser Smoke 仍待完成。
当前状态只能是：

```text
M10_CI_FIXTURE_OBSERVATION_CORRECTION_CANDIDATE
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_REQUALIFICATION_BLOCKED
```

维护候选自己的原始 Public CI、受保护合入、新 exact-main Public CI 与 Browser Smoke 成立前，不得让 #165
用 rerun 覆盖原始失败。维护地基闭合后，#165 仍须从新的 exact main 形成新 head，重新取得独立完整门禁；
维护绿色不能冒充 implementation candidate 绿色。

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
