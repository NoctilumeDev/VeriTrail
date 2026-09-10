# VeriTrail 能力边界与系统认知地图 0.1

## 1. 文档身份

- 状态：`CAPABILITY_LEDGER_OPEN / DESIGN_SPACE_ONLY`；
- 决策：`Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY /
  R1_SCHEMA_PAYLOAD_CANDIDATE / R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED / R1_IMPLEMENTATION_NOT_STARTED`；
- 施工状态：`NO_LEDGER_ITEM_IMPLEMENTATION_STARTED`；
- 首次盘点基线：`main@9ab64121350b69ce81e6be79961ad426026bbc39`；
- 本次状态发布起点：`main@8aa70807c0de9c0f50ad977575d81f2a1d635a91`；
- 影响等级：`L3_SYSTEM / DOCUMENTATION_ONLY / NON_NORMATIVE_MAP`；
- 本文不创建源码、Schema、CLI、CI、标签、Release 或空目录；
- 本文不重开 M0–M14、E 轨、P0–P4、PC 兼容桥、R0 或 Pattern Corpus 的冻结结论；
- 本文不替代已经冻结的 R1 合同，也不改变 R1 Schema 的当前优先级。

文档编号 `114` 为本平行支线预留；`113` 已由独立 R1 合同候选使用。两条支线不互相继承未合入内容。

本文把仓库已经明确写下、但分散在里程碑“未证明/未实现”说明中的边界整理成一份开放账册。
它回答的是：**当前证明边界之外已经看见了什么，以及什么条件出现以后，它才有资格成为工程。**

它不是缺陷清单、欠债清单、版本承诺或隐藏路线图。

这里的 Capability Ledger 也不是 R 轨的不可变 Pattern Ledger。本文通过普通 Git 历史保留修订，
不创建 `record_digest`、追加式 Artifact Schema 或自动状态机；真正晋级仍须进入独立合同与证据闭环。

仓库里许多分离都由真实反例逼出：原来共用一个概念的两件事，在组合后产生了不同权威、身份、失败或
演化压力。这可以称为 counterexample-driven architecture，但它不是“拆过就永远保留”。只有语义差异
仍会改变工程行为时才保留独立身份；差异消失的历史脚手架应允许收敛。能力账记录理由，不把字母数量
当成架构成熟度。

## 2. 先分清五种身份

```text
FROZEN_CAPABILITY
    已由对应合同、实现、证据和冻结坐标支持的能力

OBSERVED_BOUNDARY
    当前合同明确没有证明或没有实现的边界

CANDIDATE_DIRECTION
    出现真实需求后可以审议的方向

COMMITTED_MILESTONE
    已经获得明确合同入口、责任边界和施工授权的阶段

ARCHITECTURAL_NON_CLAIM
    系统主动不拥有的权力或不作出的声明
```

它们不能互相代替：

```text
OBSERVED_BOUNDARY != DEFECT
OBSERVED_BOUNDARY != CANDIDATE_DIRECTION
CANDIDATE_DIRECTION != COMMITTED_MILESTONE
NOT_IMPLEMENTED != TECHNICAL_DEBT
ARCHITECTURAL_NON_CLAIM != TODO
```

因此，`AI 裁决未实现` 不能被解释成“以后给 AI 增加 PASS/FAIL 权”；`P 插件 0.1.0` 也不能因为
版本号较小就被解释成“尚未完成”。二者分别是权威边界和首个有界能力。

## 3. 当前事实、当前施工与设计空间

### 3.1 当前已经成立的有界事实

VeriTrail 当前已经拥有多条可组合但身份独立的冻结能力：

```text
sealed Plan / Profile
    -> bounded execution and lifecycle
    -> Observation / Evidence
    -> deterministic Core evaluation
    -> immutable reports and read-only Workbench
```

P 轨另行把 GitHub API 与公共渲染事实压成标准 Evidence，并通过薄 handoff 交给 Core。GitHub 是
被观察的平台事实来源，不是 VeriTrail Verdict 的所有者；插件负责忠实采集，Core 只按 sealed
AcceptancePlan 复算。内部运行 Evidence 与外部平台 Evidence 都可以成为验收输入，但它们的来源、
身份和充分性不能混成一个“系统已证明”布尔值。

### 3.2 当前合法施工入口

R0 与首个 Pattern Corpus 已冻结；R1 上位合同也已通过 PR #89/#90 的候选、门禁、受保护主线合入和匿名
公开读回。Schema 合同曾由文档 121 完成冻结发布；后继 payload preflight 发现部分嵌套身份仍需由实现
猜测，文档 123 因而只重开并补齐被击穿边界。文档 124 的最后门成立后恢复 Schema payload 施工资格；
后继[文档 125](125-r1-schema-payload-freeze-candidate.md)已从新 exact main 物化 Schema/corpus 测试资产，
当前状态为 `R1_SCHEMA_PAYLOAD_CANDIDATE / R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED /
R1_IMPLEMENTATION_NOT_STARTED`。
上位 R1 合同冻结范围是：

```text
Exact SourceSnapshot
    -> deterministic CodeFacts
    -> typed semantic relations
    -> bounded overlapping ReviewSlices
    -> CoverageLedger
```

R1 合同已经冻结首版语言范围、关系闭集、Slice 与 coverage 语义。后继
[Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)冻结字段词汇、canonical bytes、
路径可逆编码、源码锚、遍历端点、Coverage 分母与 Artifact 布局；历史冻结事实由
[文档 121](121-r1-schema-contract-freeze-publication.md)外部绑定。后继
[文档 123](123-r1-schema-payload-preflight-correction.md)补齐 item key、frontier、Coverage 与 provenance
identity 的不可编码缺口，[文档 124](124-r1-schema-payload-preflight-refreeze-publication.md)发布重新冻结边界。
Schema payload 与运行实现仍未产生。R1 只建立确定性理解骨架，不进入 AI 提案、自动排序、
HumanDisposition、Core Verdict 或自动修改。本能力账和 Q0 都不与 R1 抢合同权，也不以“未来完全体”
为理由提前创建后继实现。

Q0 是一个已经闭合的短暂、独立 docs-only 蓝图支线，只把已经显现的验证调度问题放进正确边界；它没有
修改 R1 合同，也没有创建 Q 实现。当前施工入口已经返回 R1 Schema。

### 3.3 上位设计空间，不是当前产品声明

若未来真实需求依次触发本账中的若干能力，VeriTrail 体系可能逐渐形成：

```text
Intent
    -> Bounded Execution
    -> Observation
    -> Evidence
    -> Review Attention
    -> Human Decision
    -> Deterministic Verification
```

这表达的是一种工作范式假设：人可以逐步从逐项操作的 `Human in the Execution Loop`，迁到负责
目标、授权边界、异常与最终签字的 `Human in the Authority Loop`。候选杠杆可以描述为：

```text
Verified Useful Work / Human Attention
```

但当前仓库没有冻结“完全体”、范式变化或杠杆提升数据。线性链也不是唯一运行路径：Core 验收可以
独立于 Review Attention 发生；HumanDisposition 与 Core Verdict 是不同 Artifact；任何一步缺证据都
必须保留 `PENDING / INCONCLUSIVE / PARTIAL / UNSUPPORTED`，不能为了故事完整而补出确定答案。

## 4. 体系职责地图

```text
AUTHORITY / EXECUTION
Human authority
    +-> FlowKernel -- future bounded action --> JPyxis
    +----------------------------------------> JPyxis

OBSERVATION / JUDGMENT
Reality (owns truth)
    +-- observed, never owned --> External platforms
    |                              -> Platform Evidence plugins --+
    +-- observed, never owned --> JPyxis                          +-> VeriTrail Core
                                   -> immutable execution artifacts-+
VeriTrail Core -> deterministic Verdict -> Human authority

REVIEW ATTENTION
Exact source / review artifacts -> Review Attention -> Human authority
Review Attention -- future exact handoff --> VeriTrail Core

VERIFICATION SCHEDULING
Exact source -- future exact change facts --+
Platform Evidence plugins -- Evidence refs -+-> Q / Verification Scheduling
Q -- schedule + Evidence refs --> VeriTrail Core
```

这里使用静态文本图，使匿名公共读回不依赖 GitHub 的 Mermaid 子资源；展示形式不增加新的集成声明。

这张图只描述候选责任关系，不声明仓库之间已经集成：

| 对象 | 回答的问题 | 当前事实边界 | 不拥有 |
| --- | --- | --- | --- |
| VeriTrail Core | 给定 sealed Plan 与 Evidence，怎样确定性推导 Verdict | 已有冻结能力 | 世界真相、执行资源、人工处置 |
| GitHub Evidence Plugin | GitHub API 与公开页面实际观察到了什么 | P0–P4 首个有界插件已冻结 | Core Verdict、GitHub 真相、其他平台完整性 |
| Review Attention | 人应该优先看哪些有依据的源码切片 | R0/Corpus/R1 合同已冻结；R1 Schema 是当前入口 | 缺陷真值、HumanDisposition、Core Verdict |
| Q / Verification Scheduling | 已声明的证明义务怎样避免无效重复并有界执行 | Q0 蓝图已冻结，没有实现 | Gate 定义、Evidence 语义、`SAFE_TO_SKIP`、Core Verdict |
| [JPyxis](https://github.com/NoctilumeDev/JPyxis) | 异构计算怎样保持控制、定义、运行时与合同分权 | 独立仓库 M0–M6 单机基线已冻结 | VeriTrail Verdict、FlowKernel 权限、业务真相 |
| [FlowKernel](https://github.com/NoctilumeDev/FlowKernel) | 不可靠策略怎样在确定性权限、资源、隔离与恢复边界内提出有界动作 | 独立仓库仍为 Planned，R0 尚未关闭 | 当前可运行内核、外部验收真值、VeriTrail Verdict |
| Human authority | 选择前提、Seal、授权边界并承担最终处置责任 | 系统宪法中的权威边界 | 世界终极真相 |

更准确的关系不是“JPyxis、FlowKernel 都是 VeriTrail 插件”，而是：

```text
independent system
    -> immutable artifact / observation boundary
    -> replaceable Evidence adapter
    -> VeriTrail standard Evidence
```

事件和不可变制品可以跨界；状态所有权、凭据、执行入口和 Verdict 权不能跨界。

### 4.1 字母是分层命名空间，不是一张平面路线

仓库历史使用过多组前缀，但它们不在同一层：

| 类别 | 命名空间 | 身份 |
| --- | --- | --- |
| 长期顶层轨道 | `M` Core Milestones、`E` Entry Layer、`P` Platform Evidence、`R` Review Attention | 各有独立问题域和冻结历史 |
| 顶层候选轨道 | `Q` Quick / Verification Scheduling | Q0 蓝图已冻结；尚无实现 |
| E 轨内部产品阶段 | `S` Starter、`A` Authoring Skill | 入口层的子产品/阶段，不是与 E 并列的系统 authority |
| 一次性兼容桥 | `PC` Platform Compatibility | P0 与 P1 之间已经关闭的临时桥，不是长期轨道 |
| 一次性发布闭环 | `C` Core 0.13.0 release completion | 已关闭的发行状态机；不是持续产品线 |
| 内部施工阶段 | `M12-A…F`、历史 `M12-R1…R3` | 只在所属里程碑内有意义 |
| Artifact / 治理编号 | `RA`、`CAP`、`AUTH`、`L0…L3` | Pattern、能力账、权威非声明和影响层级，不是路线 |

字母多不构成问题；脱离全名、生命周期或层级使用裸前缀才会制造歧义。尤其 `C0–C3` 还曾表示 M10
项目冷启动拓扑状态，因此未来文档必须写 `Core release C1` 或 `M10 topology C1`，不能只写 `C1`。
顶层 R 轨也必须继续写 `Review Attention R1`，与历史 `M12-R1` 分开；Q 轨同理应写
`Q0 Quick Verification Scheduling`，未来包、标签和 Release 不得只使用裸 `q*`。

### 4.2 Cross-Track Dependency / Authority Matrix

健康目标不是“各轨互不认识”，而是：

```text
Many Tracks
    + Few Stable Interfaces
    + Single State Owners
    + Versioned Immutable Artifacts
```

| 轨道/角色 | 可以读取或消费 | 自己拥有 | 禁止的反向依赖或写入 | 拔除后的预期 |
| --- | --- | --- | --- | --- |
| Core / M | sealed Plan、标准 Evidence、public conformance inputs | Core Schema、规则、Bundle、Verdict | 不导入 P/R/Q 实现，不改写 Collector/Provider 状态 | 没有 Core 时不能形成 Core Verdict；插件产物仍保持各自身份 |
| E / S / A | Core 公开合同、有限 Preset、用户答案 | DRAFT 入口 Artifact 与自身发行 | 不 Seal、不 Run、不写 Verdict，不要求 Core 导入入口实现 | Core/P/R/Q 语义不变，只失去起草便利 |
| P | sealed observation request、平台只读事实、Core 公开 Evidence 合同 | Collector Policy、平台 Evidence 与来源 provenance | 不写 AcceptancePlan/Verdict，不导入 R/Q 实现 | Core 仍验其他 Evidence；R 仍可审本地源码；非平台 Gate 不受影响 |
| R | exact source、版本化事实/分析 Artifact、ReviewPolicy | Review Artifact、AttentionProposal、HumanDisposition 流程边界 | 不修改 P Evidence，不替 Core 裁决，不导入 Q 实现 | Core/P/Q 保持；只失去审查注意力压缩能力 |
| Q | 未来 exact ChangeSet、Gate contract/closure、标准 Evidence refs、资源 Profile | VerificationSchedule、复用绑定与 Lane/join provenance | 不修改 R/P 事实，不输出 `SAFE_TO_SKIP` 或 Verdict，不导入 Core 私有实现 | 验证语义不变，退回完整串行执行，wall-clock 可能上升 |
| Human authority | 事实提醒、Plan 草案、Evidence、Attention 与 Verdict | premise/Seal/授权/HumanDisposition | 不把最终责任转移给 Provider，也不拥有世界真相 | 系统不能替人完成授权或最终处置 |

工程依赖必须保持单向：

```text
P implementation -> P standard Evidence ---------\
R implementation -> R versioned Artifacts --------+-> public Core boundary
Q implementation -> Schedule -> Gate execution -> standard Evidence ----/

Core -X-> P/R/Q implementation
P impl -X-> R/Q impl
R impl -X-> P/Q impl
Q impl -X-> P/R impl or Core internals
```

允许的是语义组合，不是实现纠缠：`Track_i` 可以消费 `Artifact_j`，但不能拥有或原地改写 `State_j`。
跨轨道需要新关系时，先增加版本化 Artifact/adapter 合同，再判断全部消费者；不能用 private import、共享
可变缓存或回调闭环把两条轨道绑成同一发布节奏。

“拔插件”是最小耦合门：删除任一插件后，其他不依赖该 capability 的轨道必须保持自身语义完整。特别是：

```text
Q unavailable
    -> performance may degrade
    -> full serial verification remains
    -> verification semantics do not change
```

### 4.3 何时形成独立子系统

语义解耦不等于微服务优先，存储拓扑也不自动决定服务拓扑：

```text
Sharding / multiple databases != mandatory microservices
Module boundary != deployment boundary
Separate nouns != separate consistency boundaries
```

拆分应由共同成立的工程压力揭示，而不是先画服务名再寻找理由：

```text
Semantic boundary
    -> State ownership boundary
    -> Transaction / invariant boundary
    -> Failure and recovery boundary
    -> Independent lifecycle / deployment boundary
```

这些线不必一开始全部重合，但只有当其中多条已形成稳定差异，独立系统边界才有充分理由。可以按三种
状态处理：

| 已知状态 | 默认选择 | 验证重点 |
| --- | --- | --- |
| 多个状态必须在一个 invariant/事务中共同正确 | 保持一个最小闭环；内部允许与语义依赖一致的强耦合 | 本地事务、原子性、闭环可独立复算 |
| 状态所有者、事务闭环、失败恢复或演化节奏已经分离 | 以闭环为单位拆分，通过版本化命令、事件、API 或 Artifact 交互 | 禁止跨所有权直接写库；跨界失败、幂等、补偿与对账可验证 |
| 业务边界、流量和访问模式仍未知 | `Minimum Closed System First`，等待真实反例暴露 boundary pressure | `UNKNOWN` 保持可见；不按业务名词预造服务 |

最小闭环必须 **closed by invariants, not by nouns**。闭环内部的耦合若正好维护同一不变量，并不是缺陷；
把它强拆成网络状态机反而会把一次本地事务升级成重试、幂等、乱序、部分失败和补偿问题。真正需要强
解耦的是闭环之间：一个边界可以消费另一个边界发布的合同或不可变 Artifact，但不能直接拥有、原地
修改或绕过另一个边界的状态。

因此 VeriTrail 的 P、R、Q 首先是语义、权威和生命周期边界，不等于必须部署成独立微服务。同仓库、
同进程或同一数据库都可以是当前实现选择；只要边界仍通过稳定合同组合、单一所有者推进状态，并能在
拔除可选能力后保持剩余闭环完整，就没有必要为了“解耦”制造部署碎片。

## 5. 能力域，而不是一张巨型 TODO

### 5.1 Product Surface

负责 Plan 起草、预览、Seal 前审查与只读/可写界面边界。它不能因为增加在线编辑就把 Workbench 变成
Verdict 所有者，也不能让 Plan drafter 自动获得 Seal authority。

### 5.2 Execution Platform

负责结构化工具链、服务、中间件、容器、拓扑、操作系统和隔离。通用 Shell、可信结构化命令与不可信
代码执行是三个不同安全问题；Docker 也不是恶意代码沙箱。

### 5.3 Experiment Engine

负责真实并行、统计推断与容量表征。它们依赖清楚的 workload、样本、独立性、停止规则、硬件、拓扑与
SLO 坐标，不能由“多跑几次”或“CI 很快”推出。

### 5.4 Evidence Ecosystem

负责 GitHub 之外的平台观察适配。新增平台需要新的来源语义、身份、匿名/认证边界和公开读回证据，
不能把 GitHub 0.1.0 当成通用平台能力。

### 5.5 Authority / Intelligence

负责智能解释、提案与人的注意力分配。AI judgment capability 可以成为候选 Provider；AI Verdict
authority 仍是明确的架构非声明，不能因“未实现”被提升成待办。

### 5.6 Verification Efficiency

负责已声明证明义务的影响规划、Evidence 身份复用、有界隔离 Lane 和确定性汇合。它优化 wall-clock 与
重复计算，不改变 Gate、Evidence 或 Verdict 语义；文件后缀、历史绿灯和可变别名都不能成为跳过依据。

## 6. 开放能力账

### CAP-001 · Plan authoring 与 Workbench write path

- **能力域：** Product Surface；
- **当前身份：** `OBSERVED_BOUNDARY`；
- **已观察边界：** 当前 Workbench 是只读验真面，M3 没有证明计划编辑器或在线写；
- **为什么可能重要：** 降低结构化 Plan 起草、预览、Seal 前纠错与项目接入成本；
- **为什么现在不做：** R1 当前研究确定性源码语义，写路径不阻断 R1–R6；
- **触发条件：** 出现持续的真实作者工作流，证明离线文件起草已成为主要错误源或使用瓶颈；
- **晋级前证据：** draft/Seal 权威分离、并发与冲突模型、审计历史、恢复路径、负向权限测试；
- **不表示：** Workbench 当前有缺陷，也不表示在线编辑可以改变既有 Verdict；
- **候选归属：** `UNASSIGNED`。

### CAP-002 · 结构化构建与包管理器适配

- **能力域：** Execution Platform；
- **当前身份：** `CANDIDATE_DIRECTION`；
- **已观察边界：** M9/M10 只证明结构化、预览摘要批准的可信命令，不接受自由 Shell 或完整 npm/Maven 生命周期；
- **为什么可能重要：** 让真实 Java/JavaScript 项目在可声明参数与生命周期内被构建和验收；
- **为什么现在不做：** 需要先区分工具 capability、命令 authority 与项目输入，不能用一个 Shell 字符串绕过合同；
- **触发条件：** 至少一个真实消费方无法由现有可信命令/Profile 有界表达；
- **晋级前证据：** typed command contract、allowlist/operand identity、secret boundary、timeout/cleanup、失败保留与干净复现；
- **不表示：** 任意 Shell、TTY、stdin、网络安装或不可信代码已经获准；
- **候选归属：** `UNASSIGNED`。

### CAP-003 · 服务与中间件生命周期

- **能力域：** Execution Platform；
- **当前身份：** `CANDIDATE_DIRECTION`；
- **已观察边界：** M10/M11 只冻结有界 C1 节点与单应用真实链，没有通用数据库、消息队列或中间件所有权；
- **为什么可能重要：** 支持需要数据库、缓存、队列或多服务依赖的真实验收对象；
- **为什么现在不做：** readiness、数据初始化、事实所有权、逆序回收和残留恢复都不能由“进程启动成功”替代；
- **触发条件：** 出现不能用静态外部依赖或现有 C1 Profile 表达的真实闭环；
- **晋级前证据：** per-service owner、readiness、data seed/provenance、teardown、crash recovery、残留检测与负向矩阵；
- **不表示：** Docker 是必需实现，也不表示服务成功等于业务事实成立；
- **候选归属：** `UNASSIGNED`。

### CAP-004 · Container lifecycle

- **能力域：** Execution Platform；
- **当前身份：** `OBSERVED_BOUNDARY`；
- **已观察边界：** M0–M14 没有冻结 Docker/容器生命周期；
- **为什么可能重要：** 为可复现环境、服务组合与依赖分发提供候选载体；
- **为什么现在不做：** 容器是部署与资源能力，不自动解决状态所有权、数据真实性、跨平台或恶意代码隔离；
- **触发条件：** 真实消费方证明容器比现有本地 Profile 更能降低环境漂移且成本可控；
- **晋级前证据：** image digest、runtime/version、network/volume ownership、secret policy、cleanup、download provenance 与离线/干净复现；
- **不表示：** 容器等于沙箱，也不表示 C2/C3 必须依赖 Docker；
- **候选归属：** `UNASSIGNED`。

### CAP-005 · C2/C3 与多服务拓扑

- **能力域：** Execution Platform；
- **当前身份：** `OBSERVED_BOUNDARY`；
- **已观察边界：** 当前冻结能力集中在 Windows/C1 和有界单应用链；
- **为什么可能重要：** 表达多角色、多实例、动态依赖和跨节点失败传播；
- **为什么现在不做：** 节点数量上升会同时扩大 pairing、时间窗口、部分失败、重试、数据与回收语义；
- **触发条件：** 出现有明确所有者、拓扑和验收条件的真实 C2/C3 Subject；
- **晋级前证据：** topology identity、per-node lifecycle、cross-node correlation、partial failure、global budget 与 recovery matrix；
- **不表示：** 当前 C1 证明可外推到多节点，也不把“同时启动”冒充分布式正确性；
- **候选归属：** `UNASSIGNED`。

### CAP-006 · Cross-platform execution

- **能力域：** Execution Platform；
- **当前身份：** `OBSERVED_BOUNDARY`；
- **已观察边界：** 进程、listener owner 与 Job Object 的冻结事实是 Windows 特定语义；
- **为什么可能重要：** 让 Linux/macOS 等消费方获得各自真实的生命周期和资源证据；
- **为什么现在不做：** 跨平台不是删除 `win32` 判断；每个平台都需要独立所有权、信号、进程树与资源语义；
- **触发条件：** 出现真实非 Windows 消费方或维护环境；
- **晋级前证据：** platform profile、process ownership、signal/exit semantics、port attribution、cleanup 与干净机器矩阵；
- **不表示：** 当前 Windows 实现有 bug，也不表示各平台必须拥有相同底层机制；
- **候选归属：** `UNASSIGNED`。

### CAP-007 · Untrusted execution isolation

- **能力域：** Execution Platform / Authority；
- **当前身份：** `OBSERVED_BOUNDARY`，并受独立安全门约束；
- **已观察边界：** Windows Job、资源上限、容器候选和可信命令均不构成恶意代码沙箱；
- **为什么可能重要：** 若未来允许未知第三方代码或 Agent 生成物直接执行，需要限制真实世界影响半径；
- **为什么现在不做：** 这是独立威胁模型、隔离机制和旁路验证问题，不能作为普通 adapter 补丁加入；
- **触发条件：** 项目明确选择把不可信执行纳入产品身份，并接受相应安全与维护成本；
- **晋级前证据：** threat model、trust root、escape/side-channel 边界、network/filesystem/device policy、kill/recovery 与独立攻击验证；
- **不表示：** Docker、Job Object 或低权限账户已经满足隔离要求；
- **候选归属：** `UNASSIGNED`。

### CAP-008 · Wave 内真实微并行

- **能力域：** Experiment Engine；
- **当前身份：** `OBSERVED_BOUNDARY`；
- **已观察边界：** M8 的 `runtime_overlap_claim=NOT_PROVEN`；现有 wave/Assignment 语义不能证明运行时重叠；
- **为什么可能重要：** 提高有界实验吞吐，并研究共享资源下的交互效应；
- **为什么现在不做：** 并行会改变总预算、取消、资源竞争、Evidence pairing 与失败归因；
- **触发条件：** 串行成本成为已测瓶颈，且真实 workload 需要同窗重叠而不是简单批处理；
- **晋级前证据：** overlap clock、shared absolute budget、cancellation propagation、resource contention、deterministic ledger 与残留清理；
- **不表示：** Assignment 并行、线程存在或吞吐提高就证明真实并行正确；
- **候选归属：** `UNASSIGNED`。

### CAP-009 · Statistical inference

- **能力域：** Experiment Engine；
- **当前身份：** `CANDIDATE_DIRECTION`；
- **已观察边界：** M7/M8 没有证明统计显著性或一般因果结论；
- **为什么可能重要：** 当单变量复验不足以描述噪声 workload 时，提供有前提的效应估计；
- **为什么现在不做：** 没有 sample model、独立性、effect size、stopping rule 与 multiple-testing 规则时，统计输出只会制造更强错觉；
- **触发条件：** 出现稳定、可重复采样且确实需要概率推断的真实实验；
- **晋级前证据：** preregistered estimand、sampling model、power/effect、stopping rule、missing-data 与复算 fixture；
- **不表示：** 增加 `p < 0.05` 就得到因果或生产结论；
- **候选归属：** `UNASSIGNED`。

### CAP-010 · Capacity characterization

- **能力域：** Experiment Engine；
- **当前身份：** `CANDIDATE_DIRECTION`；
- **已观察边界：** 当前没有生产容量结论；
- **为什么可能重要：** 为特定硬件、拓扑、workload 与 SLO 提供可复验的容量范围；
- **为什么现在不做：** 没有精确坐标时，“支持多少并发”不是稳定命题；
- **触发条件：** 出现真实部署决策，需要容量证据而非功能正确性证据；
- **晋级前证据：** workload/version、hardware/topology、warmup、duration、SLO、failure profile、statistical method 与重复实验；
- **不表示：** 单机基线、CI 时长或一次压测可以外推成 production capacity；
- **候选归属：** `UNASSIGNED`。

### CAP-011 · Additional platform Evidence adapters

- **能力域：** Evidence Ecosystem；
- **当前身份：** `CANDIDATE_DIRECTION`；
- **已观察边界：** P0–P4 只冻结 GitHub API/Public Render 首个插件；
- **为什么可能重要：** 从其他代码托管、制品、CI/CD 或部署平台取得独立来源事实；
- **为什么现在不做：** 每个平台的身份、信任域、公开渲染和失败语义不同，不能复制 GitHub 字段后声称通用；
- **触发条件：** R 轨或真实项目出现 GitHub Evidence 无法回答的 sealed claim；
- **晋级前证据：** platform contract、read-only permission、source identity、rate/retry policy、anonymous/auth boundary、real public slice 与 Core handoff；
- **不表示：** GitHub 0.1.0 未完成，也不表示多个 API 的成功自动构成完整现实；
- **候选归属：** `UNASSIGNED`。

### CAP-012 · AI/Rule AttentionProposal Provider

- **能力域：** Authority / Intelligence；
- **当前身份：** `CANDIDATE_DIRECTION`，已在既有 R3/R4 路线中分配问题位置，但尚未取得当前施工权；
- **已观察边界：** R3 可以研究 AI/规则怎样提出有依据的 AttentionProposal，R4 仍由人产生 HumanDisposition；
- **为什么可能重要：** 把大规模机器产物压缩成有限、高价值且可追溯的人工审查入口；
- **为什么现在不做：** R1/R2 的确定性事实、关系、覆盖和分析证据尚未建立；
- **触发条件：** 仅按已冻结 R1–R6 阶段门推进；
- **晋级前证据：** exact SourceSnapshot binding、provider identity、supporting/opposing evidence、coverage、stale semantics、human disposition trace；
- **不表示：** AI 拥有缺陷真值、Seal、HumanDisposition、仓库写权限或 Core Verdict；
- **候选归属：** `R3 / R4` 已有阶段边界。

### CAP-013 · Q / Verification Scheduling Plugin

- **能力域：** Verification Efficiency；
- **当前身份：** `CANDIDATE_DIRECTION / Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED`；
- **已观察边界：** 当前完整门禁能守住证明纪律，但 documentation/status-only 等小变更仍会重复运行全部
  Gate；仓库尚无 Gate input closure、Evidence reuse 或隔离 Lane 调度能力；
- **为什么可能重要：** 在证明义务不变的前提下减少无效重算、重复构建和可安全解除的串行等待；
- **为什么现在不实现：** R1 0.1 只有单快照结构事实，尚无 exact base/head ChangeSet、Gate 依赖闭包、
  freshness 或复用合同；
- **触发条件：** 先完成 [Q0 蓝图](116-q0-quick-verification-scheduling-blueprint.md)，再由真实验证 Profile、
  独立 ChangeSet Provider 和新合同决定是否有资格施工；
- **晋级前证据：** exact GateInput identity、Evidence invalidation/freshness、serial baseline、资源隔离、
  deterministic join、unknown fail-closed、插件卸载后完整门禁仍成立；
- **不表示：** Q 可以输出 `SAFE_TO_SKIP`、PASS、修改 Gate、把旧绿灯当当前事实，或要求 R1 增加 diff；
- **候选归属：** 独立顶层 `Q` 轨；`Q = Quick`，正式能力名为 Verification Scheduling Plugin。

## 7. 明确不进入候选队列的权力

以下项目不是因为“还没时间”而未实现，而是当前架构主动不授予：

| Boundary ID | 非声明 | 原因 |
| --- | --- | --- |
| AUTH-001 | AI 自动产生 Core `PASS/FAIL` | Core 只按 sealed Plan 与 Evidence 确定性推导；AI 最多提出解释或 AttentionProposal |
| AUTH-002 | Workbench 重新裁决或改写历史 Verdict | Workbench 是只读验真面，展示不拥有事实 |
| AUTH-003 | Provider 成功推出 coverage 完整或“无问题” | Success、completeness 与 truth 是三个不同命题 |
| AUTH-004 | Docker/Job Object/资源上限推出恶意代码安全 | 资源控制、生命周期所有权与不可信隔离不是同一能力 |
| AUTH-005 | 人承担最终责任成为 Provider 质量免责 | Provider 仍须对来源错绑、越权、误报、漏报与覆盖谎言负责 |
| AUTH-006 | Q 输出 `SAFE_TO_SKIP`、削弱 Gate 或产生 Verdict | Q 只形成可审计 Schedule/Evidence 引用；充分性与 Verdict 仍属于 sealed Plan 和 Core |

若未来要改变其中任何一条，必须先重开对应宪法与权威合同；不能通过实现便利、配置开关或新插件
静默获得权力。

## 8. 候选之间的关系

这些候选不是一条固定流水线：

```text
Plan authoring
    可以独立演进，但必须先守住 drafter / seal authority

Structured toolchain
    可以为 service lifecycle 提供能力，不自动获得自由 Shell 权

Service lifecycle
    可以运行在本机或容器，不以 Docker 为必要前提

Container lifecycle
    可以改善环境分发，不自动证明跨平台或不可信隔离

C2/C3 topology
    依赖显式节点所有权与全局预算，不等于“多启动几个进程”

Cross-platform
    需要平台特定机制证据，不以统一实现细节为目标

Real overlap
    可独立于 C2/C3 研究，但必须重新证明预算、取消和归因

Statistics / capacity
    只在真实 workload 与问题定义出现后启动

Additional Evidence adapters
    由 sealed claim 的信息缺口触发，不由插件数量目标触发

Verification Scheduling
    可以消费未来 ChangeSet 与 Gate closure Artifact，不反向扩大 R1，也不把 Review Attention 变成 CI 调度器
```

`Untrusted execution isolation` 是横切安全边界，不应被藏在 Shell、Docker、C2/C3 或跨平台实现内部。
R1–R6 当前也不依赖上述未分配候选；提前施工只会扩大证明表面积。

## 9. 晋级门

一条能力只有同时具备以下信息，才可从开放账进入 `CONTRACT_CANDIDATE`：

1. 一个不能由现有冻结能力满足的真实消费方或可复验反例；
2. 精确问题命题与明确 non-goals；
3. authority、owner、consumer 与 state ownership；
4. 输入、输出、Artifact identity 与失败语义；
5. 资源、权限、数据与恢复边界；
6. 与现有 Core、P、R 轨及外部仓库的单向依赖关系；
7. 最小单变量证明切片与停止线；
8. 干净环境、负向矩阵和公开读回方案；
9. 明确的退出条件，以及若证据不成立时的拒绝/收缩路径。

晋级仍不等于实现授权。只有后继独立合同冻结并建立 exact main 施工基线后，才可以写代码。

## 10. 当前裁决

```text
M0–M14                         FROZEN
P0–P4                          FROZEN
R0 + Pattern Corpus 0.1        FROZEN
R1 Contract                    FROZEN
R1 Schema Contract             CORRECTION CANDIDATE
R1 Schema Payload              BLOCKED / NOT STARTED
Q0 Blueprint                   FROZEN
Q implementation               NOT STARTED

Capability Ledger              OPEN
New capability milestone       NOT COMMITTED
“Complete system” claim         NOT PROVEN
Ledger-item implementation     NOT STARTED
```

Q0 的 docs-only 蓝图已经闭环，冻结事实见
[文档 117](117-q0-verification-scheduling-freeze-publication.md)；它没有建立 Q 实现入口。当前施工已经返回
R1 Schema Contract，只允许按冻结的 SourceSnapshot、CodeFact、Relation、ReviewSlice 与 CoverageLedger
语义审查字段、身份、端点、布局和未来兼容向量，仍不创建实际 Schema 或运行实现。本账只负责让未来方向
不再遗忘、不互相冒充，也不因为“地图上有路”就替项目决定必须走哪条路。
