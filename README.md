# VeriTrail / 验迹

[![Public CI](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml)
[![Browser Smoke](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml)
[![Python 3.10 and 3.13](https://img.shields.io/badge/Python-3.10%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml)
[![Core v0.12.2](https://img.shields.io/badge/Core-v0.12.2-0B4B50)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2)
[![Starter v0.2.0](https://img.shields.io/badge/Starter-v0.2.0-8A6A2F)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0)
[![Authoring Skill v0.2.0](https://img.shields.io/badge/Authoring%20Skill-v0.2.0-A22D1F)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0)
[![License](https://img.shields.io/github/license/NoctilumeDev/VeriTrail)](LICENSE)

![VeriTrail 宫阙验迹工作台：本地 Run 目录](docs/assets/veritrail-workbench-catalog.png)

> **让每一项结论，都沿证据中轴归位。**
>
> 单变量建立可归因事实，组合批次验证交互，固定种子复现偶发故障，真实链路形成系统结论。

VeriTrail（验迹）是面向独立开发者和小型工程团队的本地优先验收证据工作台。它把计划、测试、
浏览器 F12、进程、端口和资源事实组织成不可变、可比较、可审计的 Run，并由确定性规则给出结论。

## 选择入口

| 我现在要做什么 | 从这里进入 | 你会得到什么 |
| --- | --- | --- |
| 十分钟认识验迹 | [从这里开始](START_HERE.md) | 同一预注册标准下的一次真实 `PASS` 和一次故意 `FAIL` |
| 接入一个本地 Web 项目 | [Starter 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0) | 有界 `single-webapp` / `static-site` 草案；保持 `DRAFT / NOT SEALED` |
| 用 AI 协助填写合同 | [Authoring Skill 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0) | 有限 Preset 识别、缺失信息追问和候选草案；不封存、不裁决 |
| 直接使用稳定内核 | [Core 0.12.2](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2) | Plan、Evidence、Verdict、Bundle、合成首跑与本地只读 Workbench |

## 发布状态

Core `0.12.2` 已作为有界维护版发布；Starter 与 Authoring Skill 以独立 `0.2.0` 坐标发布，历史 `0.1.0`
Release 继续保留。入口层只能降低合同填写成本，不能扩张 Core 的裁决权。GitHub 公开 CI 与
Browser Smoke 当前共同守住可重复基线。

`v0.12.1` 只关闭 wheel 独立首跑缺口，不重开 M0–M14，也不改写不可移动的 `v0.12.0`。新增的
`veritrail demo` 无需 Git checkout，只从 Core wheel 自身
生成同 Plan 的 `PASS`／故意 `FAIL` Bundle 与 Catalog，并始终标记
`SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE`。它不探测项目、不修改断言、不批准 Starter 草案，
也不把合成结果冒充项目验收。精确合同与发布说明见[文档 71](docs/71-core-first-run-maintenance-contract.md)
和 [0.12.1 Release Notes](docs/72-v0.12.1-release-notes.md)，标签、资产摘要与公开下载复验见
[发布读回事实](docs/73-core-v0.12.1-release-readback-facts.md)。

归档审查证明 `0.12.1` 的 demo Catalog 在 staging 整目录改名后保留了旧 Artifact root 绑定。
`0.12.2` 只修 producer 的最终位置绑定，不放宽 `catalog-serve` 的 fail-closed 合同；受保护注释标签、
五项 Release 资产、公开下载摘要、双 Python wheel、sdist 和搬移负对照均已完成读回。范围、发布说明
与精确证据见
[demo Catalog 最终位置绑定维护合同](docs/74-core-demo-catalog-binding-maintenance-contract.md)和
[0.12.2 Release Notes](docs/75-v0.12.2-release-notes.md)，以及
[0.12.2 发布与公开读回事实](docs/76-core-v0.12.2-release-readback-facts.md)。

Starter/Authoring Skill `0.2.0` 只增加第二个有限 Preset `static-site`：它面向无需构建、无需远程
资源的现存静态 HTML，并始终保持 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`。两个带注释标签共同
钉在提交 `c9592e1`；七个 GitHub 下载资产已通过 Python 3.10/3.13 clean install、双 Preset、普通/
优化模式、官方 Skill 校验与逐字节公开读回。Preset 合同见[文档 66](docs/66-starter-static-site-contract.md)与
[文档 67](docs/67-authoring-skill-0.2-contract.md)，发布事实见
[文档 70](docs/70-entry-layer-e3-0.2-release-notes.md)。

### 平台证据插件轨（P1 已冻结）

GitHub 上的本地提交、远端分支、PR 门禁、主线、Release 和公开页面是不同证据层。VeriTrail 已为
这类外部平台事实建立独立 `P` 轨。P0 设计合同和 P1 实现均已冻结；P1 现有独立源码包、只读 CLI、
离线合同测试、真实 GitHub 纵向切片与公开读回，但仍没有插件标签、Release 或稳定发布坐标。
它不是 M15，也不属于 Starter/Authoring Skill；插件只负责只读采集与规范化，最终
`PASS / FAIL / INCONCLUSIVE / PENDING` 仍由 sealed Plan 和 Core 决定。

简单说，sealed Plan 决定“什么算通过”；observation request 只是带着 `plan_digest` 的有界取证清单，
负责说明“去哪里看”，不再复制另一套通过规则。写 Plan 的人或 AI 也不会因为负责起草就自动获得
Seal 权。

同一平台事实也不等于同一次观察：`facts_digest` 只标识规范化事实内容，现有 EvidenceArtifact
SHA-256 标识带来源与采集上下文的具体证据文件，Core Run 再标识一次执行。两次独立采集看见相同事实
时，事实摘要可以相同，证据文件与 Run 仍必须保持可区分。sealed request 也可以重放；每次真实采集
另有 Collection Session，同一 request 的不同 session 不能冒充同一次观察或静默混配 API/页面产物。

这条链验证的是精确坐标封存后的证据一致性与漂移，不是“真理证明”：GitHub API 与公开页面是同一
平台的两个观察面，不是两个独立权威；插件和 Core 也不能证明信任锚建立前的源码、数据或结果未被
预先伪造。工程上可概括为“防君子，不防小人”：提高误操作、事后漂移与低成本篡改的发现成本，不把
内部自洽当作现实真实。**它防的是漂移，不是阴谋。** GitHub 之外的外部锚不纳入本产品；准确边界
见插件合同。

它还有独立的认识论上限：VeriTrail 不裁定一个被声明的观点在终极意义上是否正确，只裁定其预先
声明的验收条件是否被保留证据满足。现实若模糊、不完整、冲突或不可判，这种不确定性必须继续可见。
**现实拥有真相，VeriTrail 只拥有裁决纪律。** 它提供的是分层故障定位与责任归因，不是消灭误判、
误解或蓄意造假的根治机制。

设计边界见[平台证据插件 Plan](docs/77-post-core-platform-plugin-plan.md)、
[GitHub Evidence Plugin 0.1 合同](docs/78-github-evidence-plugin-contract.md)与
[P0 架构评审](docs/79-p0-github-plugin-design-review.md)。P0 三轮均已完成受保护主线合入与公开渲染
读回。Core 0.12.2 离线探针确认单源字面事实可以裁决，但也确认未观察的
PRIMARY 仍可得到 `PASS`，且跨 Evidence 的动态 session 无法由现有 Assertion 比较。独立的
[Post-P0 Core 兼容桥合同](docs/80-p0-core-compatibility-contract.md)因此定义了并列的
`AcceptancePlan`、Evidence 精确绑定、sufficiency / integrity / assertion 三类规则与跨 Evidence
operand。[PC1 通用 Acceptance Core](docs/81-pc1-acceptance-core-implementation.md)现已实现独立的
Schema、validator/seal、规则求值、AcceptanceBundle 与显式 CLI。[PC2 冻结事实](docs/82-pc2-acceptance-core-freeze-candidate.md)
又在双 Python、普通/优化模式、旧消费者、Workbench 与 wheel clean install 中完成正负 Bundle 的
独立复算，并经 PR #26 九项远端检查、受保护主线合入和真实 GitHub 渲染读回固定在实现基线
`fa8a5acac753456d37325bb0d9fac1b85add912b`。PC2 当前为 `FROZEN`；
[P1 Structured GitHub API Collector 施工合同](docs/83-p1-structured-github-api-collector-contract.md)的
0.1 版已在 PR #28 九项远端门禁、受保护主线合入和真实 GitHub 页面读回后冻结；Freeze 前发现
rulesets 与 classic branch protection 被误建模为 fallback，因此 0.2 只重开这一处来源叠加语义。
独立实现与本地/真实网络证据见
[P1 实现与冻结事实](docs/84-p1-structured-github-api-collector-freeze-candidate.md)。0.2 修正已通过
[PR #32](https://github.com/NoctilumeDev/VeriTrail/pull/32) 的 11 项门禁，合入
`main@5b363637f59be9786d58eed61a14e3bd663dd6d8`，并完成精确主线与匿名 README/事实文档读回。
当前状态为 `P1_FROZEN / P2_NOT_STARTED`。插件不得预生成“已通过”布尔值、占位实验字段或私有
比较器绕过 Core。

<details>
<summary>展开 M0–M14 冻结状态与最终发布事实</summary>


| Milestone | Capability | Status |
| --- | --- | --- |
| M0 | 封存计划、证据导入与确定性裁决 | `FROZEN` |
| M1 | 启动前资源与环境预检 | `FROZEN` |
| M2 | 有界真实 Chromium 证据 | `FROZEN` |
| M3 | 只读 Vue 证据工作台 | `FROZEN` |
| M4 | 本地 Run Catalog 与轻量自举 | `FROZEN` |
| M5 | 有界运行编排与静态目标生命周期 | `FROZEN` |
| M6 | 同计划复跑确定性比较 | `FROZEN` |
| M7 | 预注册四角色配对反事实分析 | `FROZEN` |
| M8 | 全因子批次矩阵与固定种子扰动 | `FROZEN` |
| M9 | 受控项目命令执行 | `FROZEN` |
| M10 | 有界完整项目自举 | `FROZEN` |
| M11 | 真实项目功能全链路 | `FROZEN` |
| M12 | 故宫主题前端终稿 | `FROZEN` |
| M13 | 系统思维与分层代码质量终审 | `FROZEN` |
| M14 | 整改后终局复验与发布收束 | `FROZEN / RELEASED` |

M14 冻结基线仍为不可移动的 [`v0.12.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.0)；
当前稳定 Core 是在 `0.12.1` 无 checkout 首跑基础上继续修复 demo 最终位置绑定的
[`v0.12.2`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2)。M14 没有
增加能力，而是在安全整改后对 VeriTrail 自证目标与 InkNarratives 精确提交完成常规/优化双轮真实
复验，并形成首个稳定 Release。最终门禁包括：双 Python 各 `318/318`、Workbench `171/171`、
lint/type-check/生产构建、依赖审计、wheel/sdist 独立安装运行、Release ZIP 逐文件复核、真实 Chromium、
内置浏览器桌面/390/360 px、失败恢复、敏感扫描和零残留。

自证目标的 13 个预注册出口覆盖 `PASS / FAIL / INCONCLUSIVE / PENDING` 与
`COMPLETED / ABORTED / ERROR`，正向重复 Comparison 为 `MATCH`、0 differences；InkNarratives
按预注册顺序取得 `PASS / FAIL / PENDING / PASS`，恢复 Comparison 同样为 `MATCH`。最终标准安全
扫描覆盖 375 个文件、12 个攻击面，可报告发现为 0。准确环境、资源峰值、安全边界、资产摘要与
读回规则见 [M14 最终验证与发布事实](docs/56-m14-final-validation-and-release-facts.md)，安装和故障恢复见
[0.12.0 Release Notes](docs/57-v0.12.0-release-notes.md)。0.12.1 的无 checkout 首跑维护事实继续由
[0.12.1 Release Notes](docs/72-v0.12.1-release-notes.md)和
[0.12.1 发布读回事实](docs/73-core-v0.12.1-release-readback-facts.md)保存；0.12.2 的有界增量与公开
读回见[维护合同](docs/74-core-demo-catalog-binding-maintenance-contract.md)、
[Release Notes](docs/75-v0.12.2-release-notes.md)和
[发布读回事实](docs/76-core-v0.12.2-release-readback-facts.md)。

M11 的 `m11-v0.12.0` 与 M12 的 `m12-v0.13.0` 是不可移动的里程碑标签；前者不是稳定 Release，
后者仍使用 `0.12.0.dev1` 包版本。M13 的分层终审事实继续由
[文档 53](docs/53-m13-system-and-layered-code-quality-audit-facts.md) 保存，不因 M14 发布而被改写。

准确合同见[单节点能力与真实项目双门合同](docs/23-m11-single-node-real-project-contract.md)，Gate A
事实见[M11 Gate A 验证](docs/25-m11-gate-a-validation.md)，v1 失败分层见
[M11 Gate B Plan v1 首次真实失败](docs/26-m11-gate-b-plan-v1-failure.md)，v2 与终审事实见
[M11 Gate B 真实项目验证](docs/27-m11-gate-b-validation.md)。

</details>

## 快速开始

第一次接触验迹，请先阅读 [从这里开始](START_HERE.md)。它按“第一次认识、已有本地 Web 项目、
高级合同作者”分开入口，并链接已完成的 Starter PASS/FAIL 黄金路径。当前稳定入口是
[Starter 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0) 与
[Authoring Skill 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0)。
两个标签共同钉在提交 `c9592e1`；GitHub 公共下载副本已通过 Python 3.10.6/3.13.13、双 Preset、
官方 Skill 结构校验和 DRAFT 逐字节等价门禁。E1 `0.1.0` Release 及其提交 `c7d3c8d` 保持不可变，
继续作为历史复现坐标。

核心需要 Python 3.10+；浏览器采集和 Windows 受控进程能力使用可选依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --editable ".[browser,command-windows]"
.\.venv\Scripts\python.exe -m pip install --editable ./starter
.\.venv\Scripts\python.exe -m playwright install chromium
```

这里分别安装 Core 与独立 Starter 入口层；Starter 只生成并校验草案，不接管 Core 的封存、运行或裁决。

封存一个最小计划并计算 Run：

```powershell
.\.venv\Scripts\veritrail.exe seal `
  --plan examples\minimal\plan.json `
  --output artifacts\m0-sealed-plan.json

.\.venv\Scripts\veritrail.exe evaluate `
  --plan artifacts\m0-sealed-plan.json `
  --evidence examples\minimal\evidence-pass.json `
  --run-id my-first-run `
  --output artifacts\my-first-run
```

运行与公开 CI 对齐的 Core、Starter 和 Authoring Skill 基础回归：

```powershell
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe -O -m unittest -v
.\.venv\Scripts\python.exe -m unittest discover -s starter/tests -v
.\.venv\Scripts\python.exe -O -m unittest discover -s starter/tests -v
.\.venv\Scripts\python.exe -m unittest discover -s skills/veritrail-authoring/tests -v
.\.venv\Scripts\python.exe -O -m unittest discover -s skills/veritrail-authoring/tests -v
.\.venv\Scripts\python.exe scripts/authoring_skill_acceptance.py
```

构建只读 Workbench：

```powershell
Set-Location web
npm ci
npm test
npm run lint
npm run build
npm audit --audit-level=moderate --registry=https://registry.npmjs.org
```

## 公开 CI 与真实验收边界

`Public CI` 在每次 main push、PR 更新与 merge queue 上，以 Windows Runner 运行双 Python Core／
Starter／Authoring Skill 回归、`single-webapp` 与 `static-site` 两条真实 DRAFT 链、wheel/sdist 构建，
并从 GitHub Release 下载冻结的 E1 0.1.0 资产做 checksum 与 clean-install 回读；独立 Linux Runner
运行 Workbench test、lint、type-check、生产构建和 moderate 级依赖审计。新的 Core 候选还由独立
Windows 双 Python matrix 在**不 checkout 仓库**的空工作区里只安装刚构建的 wheel，复核同 Plan
`PASS`／故意 `FAIL`、Catalog、边界标记和本机绝对路径泄漏。基础门禁通过后，另一独立 Windows
Runner 还会运行 Starter 的真实 PASS/FAIL 双 Bundle、Catalog 与生产 Workbench 黄金路径。
PR 改 base 也会重新触发，避免堆叠分支只保留旧合并事实。

`Browser Smoke` 在 main 与每周定时任务上使用仓库内公开、合成、脱敏的 M2 证据包运行真实
Chromium，检查桌面与 390 px、Console、Network、失败重试、历史导航和根横向溢出，并上传短期证据。

这些公开门禁证明平台对齐的快速基线可重复，但**不替代**物理键盘、完整真实项目、受控宿主机上的
资源停止线与清理读回。后者仍须按对应冻结合同在受控环境中执行；GitHub 的绿灯
不得被解释为整个里程碑的 `PASS`。

每个 Run ID 必须唯一；sealed Plan、Run、Comparison、PairedAnalysis 和 BatchAnalysis 均拒绝覆盖。
M4–M10 的完整命令需要相应 Profile、ToolBindings、资源预算和审批摘要，按对应里程碑合同执行。

## 它解决什么

工程项目很容易把局部通过误当成整体完成：单元测试是绿色的，但真实浏览器存在失败请求；
单实例正常，多实例产生重复副作用；一次压测写着“并发 1000”，却没有说明是总请求、同时在途、
RPS 还是热点竞争数。

VeriTrail 不替代测试框架。它回答的是：

> 在明确的环境与资源边界内，这次实验改变了什么，证据是否足以支持结论？

```text
sealed Plan / Profile
  -> live resource preflight
  -> bounded target lifecycle
  -> structured evidence collection
  -> real Chromium facts
  -> deterministic Verdict
  -> immutable Bundle and Catalog
  -> applicable comparison / paired / batch analysis
  -> owned cleanup and residual verification
```

## 核心方法

1. **基线**：冻结代码、配置、数据、拓扑、负载语义和资源预算。
2. **单变量串行**：一次只改变一个主要变量，建立可归因证据。
3. **分批组合**：覆盖声明的 Profile，验证交互但不突破宿主机预算。
4. **固定种子扰动**：在确定性矩阵后扰动顺序，并保存种子以便复现。
5. **代表性全链路**：运行真实浏览器、故障、恢复和适用的一致性验收。

硬件限制可以停止升压，但不能降低业务不变量。资源超限是运行中止，不等于产品失败；多个主要
变量同时变化会使结论不可归因，也不能包装成通过。

## 结论语言

运行状态与验收结论分开保存：

| Dimension | Values | Meaning |
| --- | --- | --- |
| ExecutionStatus | `PLANNED / RUNNING / COMPLETED / ABORTED / ERROR` | 实验是否完整执行 |
| Verdict | `PASS / FAIL / INCONCLUSIVE / PENDING` | 当前证据能否支持判断 |

- `PASS`：适用证据齐全，硬性不变量成立。
- `FAIL`：至少一个硬性不变量被可复现证据否定。
- `INCONCLUSIVE`：变量污染、环境漂移或证据冲突导致无法归因。
- `PENDING`：计划尚未取得要求的真实证据。
- `ABORTED` 是运行状态；触发资源停止线时保存现场，不伪造 `PASS/FAIL`。

## 能力索引

| Milestone | Public capability | Exact boundary |
| --- | --- | --- |
| M0 | seal / evaluate / immutable report | 单变量、结构化 JSON 证据 |
| M1 | preflight resource Evidence | 只读采样，不启动工作负载 |
| M2 | browser-capture | 显式回环 origin、串行视口、无认证材料持久化 |
| M3 | Vue Workbench | 只读验真，不重新裁决 |
| M4 | catalog-build / catalog-serve | SQLite 是可重建派生索引 |
| M5 | bounded `STATIC_HTTP` run | 不执行任意项目命令 |
| M6 | compare | 只比较同 sealed Plan 的两个独立 Run |
| M7 | pair | 固定四角色，不冒充统计因果 |
| M8 | batch | 4–16 格矩阵；wave 内真实重叠仍未证明 |
| M9 | trusted ONESHOT command | Windows Job、无 Shell/stdin/TTY，不是沙箱 |
| M10 | two-node project bootstrap | Windows/C1、dependency -> application、owned readiness/cleanup |
| M11 | single-node real-project chain | InkNarratives 精确 ref、预注册 Gate A/B，不泛化到任意项目 |
| M12 | Palace Evidence Workbench | L0 / bounded L1 表现系统，不重算 Verdict |
| M13 | system and layered quality audit | L0–L3 所有者/消费者/失败/恢复审查，不增加功能 |
| M14 | final rerun and stable release | 双真实目标、安装/浏览器/安全/资产读回，版本 `0.12.0` |

所有详细 Schema、退出矩阵、保留失败和真实验收事实都在对应文档中；README 不复制其完整战争史。

## 架构

- **Python Core**：Plan/Profile、Evidence、Verdict、资源预检、生命周期、Catalog 与派生分析。
- **Browser Adapter**：Playwright/Chromium 回环证据，采集步骤、Console、Network、截图和溢出事实。
- **Artifact Store**：不可变 JSON、Markdown、日志、截图与两层哈希清单，默认不进入 Git。
- **SQLite Catalog**：可删除、可重建的只读 Run 索引，不拥有 Verdict 真相。
- **Vue Workbench**：本地只读展示 Bundle、Comparison、PairedAnalysis 与 BatchAnalysis。

M12 Workbench“宫阙验迹 / Palace Evidence”使用 CSS 中轴、院落、格栅和状态令牌，并只引用仓库内受控的
本地纹样、材质与图标资产；不依赖 CDN、远程字体或统计脚本。结构朱只表达固定空间，`FAIL`、`ERROR`
使用独立警示朱，两个层级都不能让状态只依赖颜色传达；M12 已由不可移动标签与 GitHub 精确读回冻结。

## 安全边界

- 默认只接受显式回环目标，不读取浏览器 Profile，不持久化 Cookie、Authorization、请求/响应正文；
- 计划、Evidence、报告、附件和 sealed Profile 使用规范化 JSON 与 SHA-256 形成可复核关系；
- M9/M10 只执行结构化、预览摘要批准的可信本地命令，不接受 Shell 字符串或包管理器生命周期；
- Windows Job Object、listener owner 和端口门禁限制误杀与进程树残留，但不构成恶意代码沙箱；
- AI 可以解释异常或建议下一步，不能决定 `PASS/FAIL`。

## 证据边界与诚信用途

预注册、失败保留和不可变 Bundle 会提高事后移动标准、只挑最好结果或随手改报告的成本，因此可以
对“偷懒的造假”形成附带威慑，也可辅助复现、审查和审计。

VeriTrail 不是学术不端检测器、反欺诈系统、可信时间戳或身份认证系统。同一方若能够设计虚假
Subject、Plan、适配器和输入，甚至重建整套自洽 Bundle，VeriTrail 不能单独识别精心设计的骗局。
高风险结论仍需要独立数据源、同行审查、外部签名/时间锚与独立复现。

## 路线边界

Post-M8 收束顺序固定为：

```text
M9 controlled command
  -> M10 bounded bootstrap
  -> M11 real-project end-to-end
  -> M12 final Palace visual system
  -> M13 system and layered code-quality audit
  -> M14 final rerun and release
```

M12 已在 M11 功能事实稳定后完成并冻结；M13 没有借“代码质量”重写合同；M14 没有增加能力，
只完成整改后复验、归档和稳定发布。Post-M8 主线现已全部冻结。
完整路线见 [Post-M8 收束路线](docs/13-post-m8-roadmap.md)。

## 文档

建议从以下入口阅读：

- [产品定义](docs/00-product-brief.md)
- [证据与实验模型](docs/01-evidence-model.md)
- [架构与安全边界](docs/02-architecture.md)
- [验收标准](docs/03-acceptance.md)
- [里程碑冻结历史与文档索引](docs/milestones.md)
- [M10 有界完整项目自举合同](docs/15-m10-bounded-project-bootstrap.md)
- [M10 冻结后地基纠偏与重新验收](docs/21-m10-post-freeze-foundation-remediation.md)
- [M11 候选适配性与合同形成记录](docs/22-m11-real-project-suitability-and-contract-draft.md)
- [M11 单节点能力与真实项目双门合同](docs/23-m11-single-node-real-project-contract.md)
- [M11 入口治理与 M0-M10 当前复验](docs/24-m11-entry-governance.md)
- [M11 Gate A 单应用能力验证](docs/25-m11-gate-a-validation.md)
- [M11 Gate B Plan v1 首次真实失败](docs/26-m11-gate-b-plan-v1-failure.md)
- [M11 Gate B 真实项目验证与冻结门禁](docs/27-m11-gate-b-validation.md)
- [M12 宫阙验迹表现系统重构设计计划 0.1](docs/28-m12-palace-workbench-design-plan.md)
- [M12-A 控制组与当前状态审计](docs/29-m12-a-control-baseline-audit.md)
- [M12-B 四向公共视图与十字中轴骨架](docs/30-m12-b-cross-axis-navigation.md)
- [M12-B 运行事实](docs/31-m12-b-cross-axis-navigation-facts.md)
- [M12-C 空间令牌与 Runs 主链计划](docs/32-m12-c-run-mainline-plan.md)
- [M12-C 空间令牌与 Runs 主链运行事实](docs/33-m12-c-run-mainline-facts.md)
- [M12-D 派生分析视图计划](docs/34-m12-d-derived-analysis-plan.md)
- [M12-D1 Comparison 运行事实](docs/35-m12-d1-comparison-facts.md)
- [M12-B/C 空间收束与 Runs 目录整改计划](docs/36-m12-bc-spatial-recomposition-plan.md)
- [M12-R1 紧凑中枢与过门运行事实](docs/37-m12-r1-compact-shell-facts.md)
- [M12-R2 Runs 主链表现运行事实](docs/38-m12-r2-runs-presentation-facts.md)
- [M12-D2 Pairing 四角色有向序列表现计划](docs/39-m12-d2-pairing-presentation-plan.md)
- [M12-D2 Pairing 运行事实](docs/40-m12-d2-pairing-facts.md)
- [M12-D3 Batch 双状态矩阵与 Wave 账册表现计划](docs/41-m12-d3-batch-presentation-plan.md)
- [M12-D3 Batch 运行事实](docs/42-m12-d3-batch-facts.md)
- [M12-E Browser Evidence 与全局状态表现计划](docs/43-m12-e-browser-evidence-and-global-state-plan.md)
- [M12-E Browser Evidence 与全局状态运行事实](docs/44-m12-e-browser-evidence-and-global-state-facts.md)
- [M12-F 总体验收与冻结计划](docs/45-m12-f-final-validation-and-freeze-plan.md)
- [M12 参考图驱动的空间重组计划](docs/46-m12-reference-guided-recomposition-plan.md)
- [M12 Visual Reference Contract 1.0](docs/47-m12-visual-reference-contract.md)
- [M12-R3 参考图优先的 Catalog 重建合同](docs/49-m12-r3-reference-first-catalog-rebuild.md)
- [M12-R3 Catalog 参考图测量与采用记录](docs/50-m12-r3-catalog-reference-measurement.md)
- [M12-F 总体验收与冻结运行事实](docs/51-m12-f-final-validation-facts.md)
- [M13 系统思维与分层代码质量终审计划 0.1](docs/52-m13-system-and-layered-code-quality-audit-plan.md)
- [M13 系统思维与分层代码质量终审事实 0.1](docs/53-m13-system-and-layered-code-quality-audit-facts.md)
- [M14 整改后终局复验与发布收束合同 0.1](docs/54-m14-final-validation-and-release-contract.md)
- [M14 安全整改与重新基线合同 0.1](docs/55-m14-security-remediation-and-rebaseline-contract.md)
- [M14 整改后终局复验与发布事实 1.0](docs/56-m14-final-validation-and-release-facts.md)
- [VeriTrail 0.12.0 Release Notes](docs/57-v0.12.0-release-notes.md)
- [Post-Core 独立入口层 Plan v1](docs/58-post-core-entry-layer-plan.md)
- [VeriTrail Starter 0.1 single-webapp 合同](docs/59-starter-single-webapp-contract.md)
- [VeriTrail Authoring Skill 0.1 合同](docs/60-authoring-skill-contract.md)
- [VeriTrail Starter 0.1 十分钟 PASS/FAIL 黄金路径](docs/61-starter-single-webapp-golden-path.md)
- [VeriTrail Authoring Skill A0 冻结事实](docs/62-authoring-skill-a0-facts.md)
- [Post-Core 入口层 E1 独立发布合同 0.1](docs/63-entry-layer-e1-release-contract.md)
- [VeriTrail 入口层 E1 0.1.0 发布说明](docs/64-entry-layer-e1-release-notes.md)
- [GitHub 公共展示面收束事实](docs/65-github-public-presentation-facts.md)
- [VeriTrail Starter 0.2 static-site 合同](docs/66-starter-static-site-contract.md)
- [VeriTrail Authoring Skill 0.2 合同](docs/67-authoring-skill-0.2-contract.md)
- [Post-Core 入口层 E2 static-site 实现事实](docs/68-entry-layer-e2-static-site-facts.md)
- [Post-Core 入口层 E3 0.2.0 独立发布合同](docs/69-entry-layer-e3-0.2-release-contract.md)
- [VeriTrail 入口层 E3 0.2.0 发布说明](docs/70-entry-layer-e3-0.2-release-notes.md)
- [Core 无 checkout 首跑维护合同](docs/71-core-first-run-maintenance-contract.md)
- [VeriTrail 0.12.1 Release Notes](docs/72-v0.12.1-release-notes.md)
- [Core 0.12.1 发布与公开读回事实](docs/73-core-v0.12.1-release-readback-facts.md)
- [Core demo Catalog 最终位置绑定维护合同](docs/74-core-demo-catalog-binding-maintenance-contract.md)
- [VeriTrail 0.12.2 Release Notes](docs/75-v0.12.2-release-notes.md)
- [Core 0.12.2 发布与公开读回事实](docs/76-core-v0.12.2-release-readback-facts.md)
- [Post-Core 平台证据插件 Plan v1](docs/77-post-core-platform-plugin-plan.md)
- [VeriTrail GitHub Evidence Plugin 0.1 合同](docs/78-github-evidence-plugin-contract.md)
- [P0 GitHub Evidence Plugin 架构评审与冻结事实](docs/79-p0-github-plugin-design-review.md)
- [Post-P0 Core 兼容桥合同 0.1：AcceptancePlan 与跨 Evidence 关系](docs/80-p0-core-compatibility-contract.md)
- [PC1 通用 Acceptance Core 实现与候选事实 0.1](docs/81-pc1-acceptance-core-implementation.md)
- [PC2 Acceptance Core 兼容与冻结事实 0.1](docs/82-pc2-acceptance-core-freeze-candidate.md)
- [P1 Structured GitHub API Collector 施工合同 0.1](docs/83-p1-structured-github-api-collector-contract.md)
- [P1 Structured GitHub API Collector 实现与冻结候选事实 0.1](docs/84-p1-structured-github-api-collector-freeze-candidate.md)

## 项目来源

VeriTrail 的方法论来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、固定种子
复现偶发故障，并在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是重要参考案例，但
VeriTrail 不把任何电商服务、中间件或业务状态机硬编码为产品前提。

## 参与协作

- 提交可复现缺陷、边界明确的能力提案或 Pull Request 前，请阅读[贡献指南](CONTRIBUTING.md)；
- 参与公开讨论与评审时，请遵守[社区行为准则](CODE_OF_CONDUCT.md)；
- 安全问题不要公开披露，请按[安全策略](SECURITY.md)使用私下报告路径。

## License

[Apache License 2.0](LICENSE)
