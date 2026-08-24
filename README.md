# VeriTrail / 验迹

[![Public CI](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml)
[![Browser Smoke](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml)
[![Python 3.10 and 3.13](https://img.shields.io/badge/Python-3.10%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml)
[![Release v0.12.0](https://img.shields.io/badge/release-v0.12.0-8A6A2F)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.0)
[![License](https://img.shields.io/github/license/NoctilumeDev/VeriTrail)](LICENSE)

> 单变量证明因果，组合批次验证交互，固定种子寻找偶发故障，真实链路形成系统结论。

VeriTrail（验迹）是面向独立开发者和小型工程团队的本地优先验收证据工作台。它把计划、测试、
浏览器 F12、进程、端口和资源事实组织成不可变、可比较、可审计的 Run，并由确定性规则给出结论。

## 当前状态

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

当前稳定基线为 [`v0.12.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.0)。M14 没有
增加能力，而是在安全整改后对 VeriTrail 自证目标与 InkNarratives 精确提交完成常规/优化双轮真实
复验，并形成首个稳定 Release。最终门禁包括：双 Python 各 `318/318`、Workbench `171/171`、
lint/type-check/生产构建、依赖审计、wheel/sdist 独立安装运行、Release ZIP 逐文件复核、真实 Chromium、
内置浏览器桌面/390/360 px、失败恢复、敏感扫描和零残留。

自证目标的 13 个预注册出口覆盖 `PASS / FAIL / INCONCLUSIVE / PENDING` 与
`COMPLETED / ABORTED / ERROR`，正向重复 Comparison 为 `MATCH`、0 differences；InkNarratives
按预注册顺序取得 `PASS / FAIL / PENDING / PASS`，恢复 Comparison 同样为 `MATCH`。最终标准安全
扫描覆盖 375 个文件、12 个攻击面，可报告发现为 0。准确环境、资源峰值、安全边界、资产摘要与
读回规则见 [M14 最终验证与发布事实](docs/56-m14-final-validation-and-release-facts.md)，安装和故障恢复见
[0.12.0 Release Notes](docs/57-v0.12.0-release-notes.md)。

M11 的 `m11-v0.12.0` 与 M12 的 `m12-v0.13.0` 是不可移动的里程碑标签；前者不是稳定 Release，
后者仍使用 `0.12.0.dev1` 包版本。M13 的分层终审事实继续由
[文档 53](docs/53-m13-system-and-layered-code-quality-audit-facts.md) 保存，不因 M14 发布而被改写。

准确合同见[单节点能力与真实项目双门合同](docs/23-m11-single-node-real-project-contract.md)，Gate A
事实见[M11 Gate A 验证](docs/25-m11-gate-a-validation.md)，v1 失败分层见
[M11 Gate B Plan v1 首次真实失败](docs/26-m11-gate-b-plan-v1-failure.md)，v2 与终审事实见
[M11 Gate B 真实项目验证](docs/27-m11-gate-b-validation.md)。

## 快速开始

第一次接触验迹，请先阅读 [从这里开始](START_HERE.md)。它按“第一次认识、已有本地 Web 项目、
高级合同作者”分开入口，并链接已完成的 Starter PASS/FAIL 黄金路径。Starter S0/S1 与 Authoring
Skill A0 已作为独立的 E1 `0.1.0` 产品发布：[Starter 0.1.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.1.0)
与 [Authoring Skill 0.1.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.1.0)。
两个标签共同钉在提交 `c7d3c8d`；GitHub 公共下载副本已通过 Python 3.10/3.13 clean-install、官方
Skill 结构校验、DRAFT 逐字节等价与真实 PASS/FAIL 黄金路径门禁。

核心需要 Python 3.10+；浏览器采集和 Windows 受控进程能力使用可选依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --editable ".[browser,command-windows]"
.\.venv\Scripts\python.exe -m playwright install chromium
```

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

运行 Core 回归：

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

构建只读 Workbench：

```powershell
Set-Location web
npm ci
npm test
npm run lint
npm run build
```

## 公开 CI 与真实验收边界

`Public CI` 在每次 main push、PR 更新与 merge queue 上，以 Windows Runner 运行双 Python Core／
Starter 回归和 wheel/sdist 构建，并在独立 Linux Runner 上运行 Workbench test、lint、type-check、
生产构建和 moderate 级依赖审计。两个基础门禁通过后，独立 Windows Runner 还会运行 Starter 的
真实 PASS/FAIL 双 Bundle、Catalog 与生产 Workbench 黄金路径。PR 改 base 也会重新触发，避免堆叠
分支只保留旧合并事实。

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

## 项目来源

VeriTrail 的方法论来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、固定种子
复现偶发故障，并在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是重要参考案例，但
VeriTrail 不把任何电商服务、中间件或业务状态机硬编码为产品前提。

## License

[Apache License 2.0](LICENSE)
