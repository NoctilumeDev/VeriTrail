# VeriTrail / 验迹

[![Public CI](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml) [![Browser Smoke](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml/badge.svg)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/browser-smoke.yml) [![Python 3.10 and 3.13](https://img.shields.io/badge/Python-3.10%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/NoctilumeDev/VeriTrail/actions/workflows/ci.yml) [![Core v0.13.0](https://img.shields.io/badge/Core-v0.13.0-0B4B50)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.13.0) [![GitHub Evidence v0.1.0](https://img.shields.io/badge/GitHub%20Evidence-v0.1.0-6F42C1?logo=github)](https://github.com/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.0) [![License](https://img.shields.io/github/license/NoctilumeDev/VeriTrail)](LICENSE)

> **让每一项结论，都沿证据中轴归位。**
>
> A local-first workbench for evidence-bound, reproducible verification.

VeriTrail（验迹）把事先封存的验收条件、来自真实执行或外部平台的证据，以及确定性裁决分开保存。
它帮助独立开发者和小型团队回答：**这次到底证明了什么，依据是什么，边界在哪里，失败应回到哪一层排查。**

[开始使用](#开始使用) · [理解系统](#十秒认识-veritrail) · [查看状态](#当前状态) ·
[阅读文档](#阅读路径) · [完整里程碑](docs/milestones.md)

## 十秒认识 VeriTrail

VeriTrail 的核心关系很小：

![VeriTrail 架构关系：现实经 Evidence Producer 形成标准 Evidence；人封存 Plan；Plan 与 Evidence 只在 Core 中相遇并导出 Verdict 与不可变 Bundle；Workbench 支持最终人工处置；R 分配审查注意力，Q 调度证明工作，但二者均无 Verdict 权。](docs/assets/veritrail-architecture.svg)

<p align="center"><sub>中轴实线是证据与裁决链，两翼虚线是可替换的辅助能力；图中两端的 Human authority 属于同一权威域。</sub></p>

这不是一条把所有能力串成单体流水线的图。Core 只消费 sealed Plan 与标准 Evidence；R 面向人的审查
注意力，Q 面向证明义务的执行效率，两者都不能获得 Core Verdict 权。Workbench 负责展示和验真，
不在浏览器里重新裁决。

图中的 Evidence producer 是一个权威角色，不等于某个固定插件。当前已交付的是 GitHub Evidence P 轨；
[O0 Operations Evidence](docs/180-o0-operations-evidence-problem-framing.md) 与
[T0 Test Evidence](docs/181-t0-test-evidence-problem-framing.md) 只保存新的候选观察问题，没有运行时、
公共 Schema 或产品坐标。架构图因此只画通用只读 Evidence 边界，不把 O/T 预演成已实现模块。

| 责任 | 谁拥有 | 明确不拥有 |
| --- | --- | --- |
| 前提、目标与 Seal 决定 | Human authority | 世界终极真相 |
| 事实采集与来源说明 | Evidence producer / plugin | 验收标准与 Verdict |
| 证据充分性与确定性裁决 | VeriTrail Core | 外部事实、执行资源与人工处置 |
| 最终处置 | Human authority | 改写历史 Evidence 或伪造确定性 |

> **现实拥有真相，VeriTrail 只拥有裁决纪律。**

## 系统分层

各层通过版本化合同和不可变 Artifact 组合；依赖不等于 ownership，消费也不等于继承状态机。

| 层 | 回答的问题 | 主要产物 | 当前边界 |
| --- | --- | --- | --- |
| Entry / Authoring | 怎样更容易起草一个可检查的计划？ | `DRAFT / NOT_SEALED` Plan | Starter 与 Authoring Skill 不 Seal、不运行、不裁决 |
| Evidence | 真实执行或外部平台观察到了什么？ | 标准 Evidence + provenance | Producer 只报告事实，不能输出 Verdict-like 结论；P 已发布，O0/T0 仍是候选问题记录 |
| Core | 给定 Plan 与 Evidence，条件是否满足？ | `PASS / FAIL / INCONCLUSIVE / PENDING` + Bundle | 只使用版本化规则，不拥有世界真相 |
| Workbench | 人怎样读懂并复核这些 Artifact？ | 本地只读视图 | 不写回、不重新裁决 |
| Review Attention / R | 人应该优先看哪些源码关系与切片？ | Review Artifact / Attention Proposal | SourceSnapshot、Derivation Input runtime、Evidence Schema 0.1.1、Budget Primitive、Execution Cell、private Fact/Evidence closure、multi-Provider applicability / Fact composition、Relation derivation、private Relation observation / composition qualification，以及 private RelationSet admission / explicit witness / Evidence 0.2 binding 已冻结；Slice 与 Coverage 尚未实现 |
| Verification Scheduling / Q | 既定证明义务怎样减少无效重算？ | 候选 Schedule / Evidence reuse binding | Q0 仅冻结蓝图，尚无实现，也无 Gate 跳过权 |

![VeriTrail 宫阙验迹工作台：本地 Run 目录](docs/assets/veritrail-workbench-catalog.png)

<p align="center"><sub>Workbench 是证据的只读阅读面；宫阙视觉语言不改变任何裁决语义。</sub></p>

## 当前状态

下表刻意把“已经公开交付”“合同已冻结”和“只在设计空间”分开，避免把路线图当成实现证据。

| 轨道 / 产品 | 职责 | 当前事实 |
| --- | --- | --- |
| Core / M | 计划、证据、运行、裁决与不可变 Bundle | `v0.13.0 RELEASED / MAINTENANCE_FROZEN`；M0–M14 已冻结 |
| Entry / E | Starter 与 Authoring Skill | `0.2.0 RELEASED`；只生成并校验草案 |
| Platform / P | GitHub API 与 Public Render Evidence | `P4_GITHUB_EVIDENCE_0.1.0_RELEASED / P4_FROZEN` |
| Review / R | 确定性源码事实、语义切片与未来注意力提案 | `R1_RELATION_DERIVATION_FROZEN / R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN / R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN / R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_FROZEN / R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_IN_PROGRESS / R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_EXACT_MAIN_VERIFIED / R1_REVIEW_SLICE_INPUT_STAGES_D_H_NOT_STARTED / R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED` |
| Quick / Q | 验证调度与 Evidence 安全复用的候选边界 | `Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY` |
| Operations Evidence / O | 运行与系统状态的候选只读观察面 | `O0_OPERATIONS_EVIDENCE_CANDIDATE_DIRECTION / NO_IMPLEMENTATION_AUTHORITY / NO_RUNTIME` |
| Test Evidence / T | 测试发现、执行与报告身份的候选只读观察面 | `T0_TEST_EVIDENCE_CANDIDATE_DIRECTION / NO_IMPLEMENTATION_AUTHORITY / NO_RUNTIME` |

完整状态、不可移动坐标和保留失败由[里程碑与文档索引](docs/milestones.md)保存。能力边界、候选触发条件
以及 VeriTrail、JPyxis、FlowKernel 与 Human authority 的关系另见
[能力边界与系统认知地图](docs/114-capability-boundary-and-system-map.md)。

## 选择入口

| 我现在要做什么 | 从这里进入 | 你会得到什么 |
| --- | --- | --- |
| 十分钟认识验迹 | [从这里开始](START_HERE.md) | 同一预注册标准下的一次真实 `PASS` 和一次故意 `FAIL` |
| 接入一个本地 Web 项目 | [Starter 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0) | 有界 `single-webapp` / `static-site` 草案；保持 `DRAFT / NOT SEALED` |
| 用 AI 协助填写合同 | [Authoring Skill 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0) | 有限 Preset 识别、缺失信息追问和候选草案；不封存、不裁决 |
| 直接使用稳定内核 | [Core 0.13.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.13.0) | Plan、Evidence、四 Verdict、Acceptance Bundle、合成首跑与本地只读 Workbench |
| 采集公开 GitHub 事实 | [GitHub Evidence Plugin 0.1.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.0) | 只读 API / Public Render Evidence 与 Core handoff |

## 它解决什么

工程项目很容易把局部绿灯误当成整体完成：单元测试通过，但真实浏览器存在失败请求；单实例正常，
多实例出现重复副作用；一次压测写着“并发 1000”，却没有说明总请求、同时在途、RPS 或热点竞争数。

VeriTrail 不替代测试框架、CI、浏览器或监控。它在这些工具之上建立一条可复算的验收链：

```text
sealed Plan / Profile
  -> resource and environment preflight
  -> bounded target lifecycle
  -> structured Evidence collection
  -> deterministic Core evaluation
  -> immutable Bundle and Catalog
  -> comparison / paired / batch analysis where applicable
  -> owned cleanup and residual verification
```

核心方法只有五条：冻结基线；一次只改变一个主要变量；用显式组合矩阵验证交互；用固定种子寻找并
复现偶发问题；最后用真实链路验证系统结论。资源限制可以停止升压，但不能降低一致性与安全不变量。

## 结论语言

运行是否结束和证据能否支持结论是两件事，因此必须分开保存：

| Dimension | Values | Meaning |
| --- | --- | --- |
| ExecutionStatus | `PLANNED / RUNNING / COMPLETED / ABORTED / ERROR` | 实验是否完整执行 |
| Verdict | `PASS / FAIL / INCONCLUSIVE / PENDING` | 当前证据能否支持判断 |

- `PASS`：适用证据齐全，硬性不变量成立；
- `FAIL`：至少一个硬性不变量被可复现证据否定；
- `INCONCLUSIVE`：变量污染、环境漂移或证据冲突导致无法归因；
- `PENDING`：尚未取得计划要求的真实证据；
- `ABORTED` 是运行状态。资源停止线触发时保存现场，不伪造 `PASS / FAIL`。

## 开始使用

第一次接触请优先走 [START_HERE](START_HERE.md) 的十分钟 PASS / 故意 FAIL 黄金路径。下面是源码
工作区的最小 Core 入口；浏览器采集和 Windows 受控进程能力保持可选安装。

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

开发者需要复现 Public CI、Starter、Authoring Skill、Workbench 或发布资产时，请按
[贡献指南](CONTRIBUTING.md)和[里程碑索引](docs/milestones.md)中的对应合同运行完整矩阵；首页不复制整套
发布门禁命令。

## 已交付能力与边界

Core 的 M0–M14 已形成单机可验证闭环，覆盖 sealed Plan、资源预检、真实 Chromium Evidence、只读
Workbench、不可变 Catalog、同计划比较、四角色配对、批次矩阵、可信有界命令、完整项目自举、真实
项目链路与最终发布。每项能力只对其冻结合同中的环境、拓扑与威胁边界成立。

<details>
<summary><strong>展开 M0–M14 能力索引</strong></summary>

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
| M12 | Palace Evidence Workbench | `FROZEN` |
| M13 | 系统与分层代码质量终审 | `FROZEN` |
| M14 | 整改后终局复验与发布收束 | `FROZEN / RELEASED` |

</details>

平台插件与后继研究轨保持独立：

- GitHub Evidence Plugin `0.1.0` 已完成 P0–P4 的合同、Structured API、匿名 Public Render、同一
  Evidence snapshot handoff、公开资产与下载读回；插件只观察 GitHub，不成为新的事实中心。
- Review Attention 已冻结 R0、首个 Pattern Corpus 与 R1 合同。R1 首版只针对 Python 3.10 结构语义，
  不外推成整个多语言仓库已经被理解；[payload 前置审计](docs/123-r1-schema-payload-preflight-correction.md)
  在零改动施工前发现并补齐 item key、frontier、Coverage 与 provenance identity 缺口，
  [重新冻结发布](docs/124-r1-schema-payload-preflight-refreeze-publication.md)完成后只允许从新 exact main
  起草版本化 Schema、纯数据兼容 corpus 与规范摘要向量。[payload 候选](docs/125-r1-schema-payload-freeze-candidate.md)
  已经物化这些资产；其远端门、主线合入、exact-main 门与匿名读回由
  [冻结发布](docs/126-r1-schema-payload-freeze-publication.md)外部绑定。最后门成立后只解除独立运行实现合同
  或首个最小切片的入口。[SourceSnapshot 运行合同](docs/127-r1-source-snapshot-runtime-contract.md)已在
  写代码前拆开单 Artifact 与 Derivation Manifest、acquisition safety budget 与后继 Policy budget；其
  [冻结发布](docs/128-r1-source-snapshot-runtime-contract-freeze-publication.md)完成最后门后，只解除该最小
  实现入口。[SourceSnapshot 实现候选](docs/129-r1-source-snapshot-implementation-freeze-candidate.md)
  已从 exact Git object 建立 raw-path inventory、规范摘要与单文件 create-new publication；其
  [冻结发布](docs/130-r1-source-snapshot-freeze-publication.md)完成独立门禁与公开读回。当前只冻结这一
  最小运行切片。[后继最小闭环审计](docs/131-r1-post-snapshot-derivation-input-audit.md)进一步确认 FactSet
  不能脱离 DerivationEvidence 与完整 Manifest 单独发布，因此选择不产生新 Artifact 的
  [Derivation Input Binding 合同](docs/132-r1-derivation-input-binding-contract.md)。其
  [冻结发布](docs/133-r1-derivation-input-binding-contract-freeze-publication.md)完成候选门禁、受保护主线、
  exact-main 门与匿名读回后，只解除这一窄边界的实现停止线。[实现与冻结候选事实](docs/134-r1-derivation-input-implementation-freeze-candidate.md)
  已把三份 canonical Artifact、exact Git bytes 与 copy-owned runtime value 连续绑定，并以二十二格矩阵、
  双 Python/`-O`、受保护主线和 exact-main 门禁复验；[最终冻结发布](docs/135-r1-derivation-input-freeze-publication.md)
  外部绑定候选门禁、合入、exact-main 门与匿名读回。最后门成立后只冻结 Input Binding。后继
  [前置审计](docs/136-r1-derivation-attempt-and-fact-provenance-audit.md)没有直接启动 parser，而是先暴露
  request provenance、Provider applicability、三类 budget 与双向 Fact provenance 接缝；
  [最小运行合同候选](docs/137-r1-derivation-attempt-and-fact-provenance-contract.md)只冻结显式单 Provider、
  shared budget context、application-owned Fact identity 与 non-published phase result。后继
  [Schema 修正审计](docs/139-r1-derivation-evidence-schema-correction-audit.md)确认旧 `0.1` 公共 Schema 不能
  原位改写；[最小修正合同](docs/140-r1-derivation-evidence-schema-correction-contract.md)只为
  DerivationEvidence 建立自描述的 `0.1.1` 补丁身份、两类 budget diagnostic 与非成功 reported-ID 空集规则；
  [合同冻结发布](docs/141-r1-derivation-evidence-schema-correction-contract-freeze-publication.md)完成自己的最后门后，
  只授权该 Schema/corpus correction；其 bytes/corpus 已由[最终冻结发布](docs/143-r1-derivation-evidence-schema-correction-freeze-publication.md)
  独立闭合。随后 [Budget Primitive 前置审计](docs/144-r1-derivation-budget-primitive-precontract-audit.md)
  用真实 Windows Job 与 staging 探针拆开 hard containment、正向原因归属、absolute acceptance deadline 与
  cleanup release envelope；[最小合同候选](docs/145-r1-derivation-budget-primitive-contract.md)只修正这条
  authority 接缝；[合同冻结发布](docs/146-r1-derivation-budget-primitive-contract-freeze-publication.md)外部绑定
  候选门禁、exact-main 门、匿名 raw/product 读回与第二轮系统俯瞰。它自己的最后门全部成立后，只允许
  实现 budget primitive 与 `BP-001..016`。[实现冻结候选](docs/147-r1-derivation-budget-primitive-implementation-freeze-candidate.md)
  已记录独立 Review Attention 包、absolute deadline、single stop latch、inclusive artifact reservation、
  Windows Job containment/positive attribution、首次远端测试模型红灯及新 head 11/11；其候选门、受保护主线、
  exact-main 门与匿名已安装产品读回由[最终冻结发布](docs/148-r1-derivation-budget-primitive-freeze-publication.md)
  外部绑定。后继[系统审计](docs/149-r1-derivation-execution-cell-system-audit.md)确认 Budget Primitive 不能被
  直接拼成 Provider/Fact runtime：execution-cell 覆盖、terminal envelope、context invalidation 与未归因
  worker termination 仍需一个更窄的合同闭环。[Execution Cell / Terminal Envelope 合同候选](docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md)
  现已把 controller/application worker/Provider authority、具体 cell preparation 与 attempt admission、bounded
  single-terminal framing、closed test binding、未知终止的 epistemic fallback 及不可恢复 context revocation
  收窄为 docs-only 候选；[合同冻结发布](docs/151-r1-derivation-execution-cell-contract-freeze-publication.md)
  外部绑定候选的 PR、exact-main 门、匿名产品读回与冻结前第二轮系统俯瞰。它自己的最后门全部成立后，只允许
  实现 closed test Provider / non-published Fact phase；真实 parser、Relations、Slices、Coverage 与完整 Manifest
  继续未启动。[实现冻结候选](docs/152-r1-derivation-execution-cell-implementation-freeze-candidate.md)已记录
  private execution-cell、29 项协议/运行义务、PR #132、exact-main 双门、匿名逐字节读回，以及被作废后
  重建的 clean-wheel provenance 证据。[实现冻结发布](docs/153-r1-derivation-execution-cell-freeze-publication.md)
  已外部绑定候选的 PR、exact-main 双门与三次匿名 installed-product readback；它自己的最后门全部成立后，
  Execution Cell 才成为 frozen。后继[Fact Admission 与 DerivationEvidence Closure 系统审计](docs/154-r1-fact-evidence-closure-system-audit.md)
  已从新 exact main 拆开 application-canonical Fact、FactSet admission、Evidence reported IDs 与公共发布资格，
  并确认 non-budget diagnostic placement 和 terminal DIAGNOSTIC publication budget 仍是合同缺口。后继
  [Fact Admission / DerivationEvidence Closure 最小合同候选](docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md)
  已把四层 Fact membership、phase/final reported-ID、canonical diagnostic placement 以及 normal/diagnostic/
  cleanup 三种能力拆开。只有拥有合法 phase result、且没有预算 stop 的 execution-cell non-success，才可能取得
  future DIAGNOSTIC eligibility。候选经 PR #136、exact-main 双门与三次 fresh anonymous installed-product readback
  闭合；[独立冻结发布](docs/156-r1-fact-evidence-closure-contract-freeze-publication.md)又完成第二轮系统审计，
  没有发现新 blocker。该发布自己的最后门全部成立后，只允许实现 private integrated controller、non-published
  Fact admission/Evidence projection 与 FA-001..024；output path、publisher、真实 parser、Relation、Slice、
  Coverage 与完整 Manifest 继续未启动。[实现冻结候选](docs/157-r1-fact-evidence-closure-implementation-freeze-candidate.md)
  已记录该 private closure、FA-001..024、PR #140、独立 Public CI 外层 timeout capacity 修正、exact-main
  双门、匿名源码字节读回与 clean-wheel installed-product 证据。候选又经 PR #142、候选 exact-main 双门及
  三次 R1 专属 anonymous installed-product readback 闭合；最初误用 P4 acceptance label 的三份结果已作废，
  没有进入冻结证据。[实现冻结发布](docs/158-r1-fact-evidence-closure-freeze-publication.md)只外部绑定这些
  已成立事实；该发布自己的门、合入、exact-main 双门与匿名产品读回全部成立后，Fact/Evidence closure 才成为
  frozen。后继[下一闭环系统审计](docs/159-r1-post-fact-evidence-next-closure-system-audit.md)比较
  DIAGNOSTIC publisher、真实 parser、multi-Provider Fact composition、Relation、Slice、Coverage 与 COMPLETE
  publisher；其最后门成立后，只选择 multi-Provider applicability / Fact composition 作为下一份 docs-only
  合同。[合同候选](docs/160-r1-multi-provider-applicability-and-fact-composition-contract.md)进一步把
  requirement/applicability/descriptor/binding/run、capability-level requiredness、shared BudgetContext、terminal
  join、same-ID provenance merge 与 same-subject conflict 钉死为 private closed-test 边界。它没有实现授权，
  也不允许直接开始 public Provider authorization、publisher、真实 parser、Relation、Slice、Coverage 或完整
  Manifest。[合同冻结发布](docs/161-r1-multi-provider-fact-composition-contract-freeze-publication.md)外部绑定
  PR #145、candidate exact-main 双门与三次 R1 专属 anonymous installed-product readback；它自己的最后门全部
  成立后，只允许 private applicability/composition 与 `MP-001..028`，其他后继对象继续未授权。
  [实现冻结候选](docs/162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md)记录该 private
  implementation、固定 compatibility vector、PR #147、implementation exact-main 双门与七项匿名源码字节读回；
  本候选自己的门、合入、exact-main 门、匿名产品读回及后继独立最终状态发布成立前，不得写成 frozen。
  [实现冻结发布](docs/163-r1-multi-provider-fact-composition-freeze-publication.md)外部绑定 PR #148、候选
  exact-main 双门与三次专属 anonymous installed-product readback；该发布自己的最后门全部成立后，当前闭环
  才成为 frozen。后继[系统级审计](docs/164-r1-post-composition-next-closure-system-audit.md)确认当前 runtime
  只允许 Provider 报告 Facts，而完整 fixture 的 Relation provenance、`reported_relation_ids` 与 composite
  FactSet-dependent import resolution 尚无 producer authority 闭环；因此下一份合同只选择 Relation derivation
  authority、exact FactSet operand continuity 与 minimum upstream eligibility gate，不预先包办完整 Relation
  算法、conflict/UNKNOWN 账册或 admission。审计不授权 Schema 或 runtime；facts-only real parser 可作为独立
  后继，但不得借机固定 Relation authority，publisher、Slice、Coverage 与完整 Manifest 也仍未授权。
  [Relation authority / operand continuity 合同候选](docs/165-r1-relation-derivation-authority-and-operand-continuity-contract.md)
  从文档 164 最后门成立后的 exact main 独立起草：首个 closed proof 候选选择 composed FactSet 后的 distinct
  Relation capability/ProviderRun，Fact child 不回填 Relation 报告，application 不自造来源；relation-only
  operands 必须版本化绑定 `fact_set_digest`。新 closed profile 须区分 Fact-stage private join 与 Relation 后的
  final overall，避免 required Relation run 与 FactSet 相互等待；全程保留同一个共享 BudgetContext。首版 conflict-bearing FactSet、
  optional-source gap 与 absent normal FactSet 不启动 Relation run，保留 typed upstream truth；完整 Relation
  算法、import resolution、RelationSet admission、Schema/runtime correction 与后继 publisher 仍未授权。
  [合同冻结发布](docs/170-r1-relation-derivation-contract-freeze-publication.md)绑定候选 PR #151、候选 exact-main
  双门与三次专属 anonymous installed-product readback，并从当前维护基线重新复核 source-state 与 GitHub
  workflow/attempt authority。它自己的最后门全部成立后，只允许 relation-only `/0.2` identity、phase join、
  distinct Relation cell、保守 upstream gate、同一个 live BudgetContext 与 `RD-001..017` 的 private closed
  implementation；完整 Relation 算法、RelationSet、publisher、Slice 与 Coverage 继续未授权。
  [实现冻结候选](docs/171-r1-relation-derivation-implementation-freeze-candidate.md)记录该 private implementation、
  fixed identity vector、PR #156、implementation exact-main 双门与十一项匿名源码字节读回。它只证明一条
  Relation candidate 可以在 exact FactSet、真实 Provider identity 与共享预算下诚实存在；本候选自己的门、
  合入、exact-main 门、匿名产品读回及后继独立最终状态发布成立前，不得写成 frozen，也不得进入 RelationSet、
  Slice 或 Coverage。[实现冻结发布](docs/172-r1-relation-derivation-freeze-publication.md)外部绑定 PR #157、
  candidate exact-main 双门、三次正式 anonymous installed-product readback 与保留的首次 README
  `PublicRenderNetworkError`。该发布自己的门、合入、exact-main 双门与匿名产品读回全部成立后，Relation
  第一刀才成为 frozen；后继仍须先做系统级俯瞰，再选择一个最小合同闭环。
- [Declared Relation Observation Domain / Composition Qualification 系统审计](docs/173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md)
  在冻结 runtime 上复现：Relation ProviderRun 可以 `COMPLETED` 且只报告 `LEXICAL_CONTAINS`，同时 Profile
  仍列有 `IMPORT_TARGET_LITERAL`。因此 Provider terminal、required source-set terminal 与 bounded observation
  domain qualification 必须分开；下一问题面先关闭 source responsibility、successful-empty 边界与 multi-source
  composition qualification，不直接开始 RelationSet admission、完整 import resolution、Slice 或 Coverage。
- [Declared Relation Observation Domain / Composition Qualification 最小合同候选](docs/175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
  从 exact FactSet 机械建立 Fact-backed observation items，在 Provider 执行前固定 A/B exact responsibility，
  并用受冻结 profile semantics 约束的 digest 绑定 denominator 与责任规则。Provider 必须为每个 assigned item
  经 private relation-cell terminal 另报显式 outcome；application 对 outcome 与 candidate 做双向对账，不能从
  candidate 缺席推导负结论。
  因此 responsibility definition、Provider terminal、逐 item 履责、required source-set terminal、item closure 与
  candidate agreement 分开。首个 proof 使用两个 required closed sources：A 观察 lexical items，B 观察 lexical
  与 import-literal items；same-ID 只合并 provenance，same-subject 分歧保留 private conflict。`QUALIFIED` 仍没有
  RelationSet admission 或 publication
  authority，现有公共 Schema 也不能凭 shape 证明 qualification。
  [合同冻结发布](docs/176-r1-relation-observation-composition-qualification-contract-freeze-publication.md)绑定
  PR #160 的正式首败、独立 PR #161 fixture maintenance、重新资格化 head、候选 exact-main 双门与三次专属
  anonymous installed-product readback。它自己的最后门全部成立后，只允许文档 175 A–H 的 private closed
  implementation；RelationSet、公共 Schema、publisher、Slice 与 Coverage 继续未授权。
- [Relation Observation / Composition Qualification 实现冻结候选](docs/178-r1-relation-observation-composition-qualification-implementation-freeze-candidate.md)
  记录文档 175 A–H 的 private closed proof、PR #165 两条保留首败、独立 PR #166 CI 夹具维护、重新资格化
  implementation head、合入后的 exact-main 11/11 与 Browser Smoke 1/1，以及十一份变更文件的匿名 exact-SHA
  字节读回。当前只能是 `IMPLEMENTED / FREEZE_CANDIDATE`；本文自己的门、合入、fresh anonymous
  installed-product readback 与后继独立最终状态发布全部成立前，不得写成 frozen，也不得开始 RelationSet、
  公共 Schema、Slice 或 Coverage。
- [Relation Observation / Composition Qualification 实现冻结发布](docs/179-r1-relation-observation-composition-qualification-freeze-publication.md)
  外部绑定 PR #167、candidate exact-main 双门、三次互不复用的 anonymous installed-product readback 与
  canonical manifest。README wrapper 的后处理错误和文档 178 首次 anonymous API quota 首败均独立保留；
  后继成功不改写它们。该发布自己的门、合入、新 exact-main 双门与三次匿名读回全部成立后，private
  qualification closure 才成为 frozen；下一步仍须先做 system audit，不直接开始 RelationSet。
- [RelationSet Admission / Qualification Evidence Binding 系统审计](docs/182-r1-post-qualification-relation-set-admission-and-evidence-binding-system-audit.md)
  从 exact main 构造双 Python H1/H2/H3 identity matrix：两个独立合格 attempt 保留相同
  `relation_set_digest`、不同 provenance file bytes；合格历史与缺一个 outcome 的未合格历史又可保留相同 raw
  candidate projection。现有 private application 正确拒绝后者，但当前 RelationSet、Evidence 0.1.1 与
  Manifest 不能让完整 Bundle 对外复核 explicit admission witness。审计只选择 RelationSet admission /
  admission witness / public qualification binding 这一问题面，不冻结 witness 的 public encoding、字段或代码；
  RelationSet、corrected Evidence、Slice 与 Coverage 仍未获实现授权。
- [RelationSet Admission / Explicit Admission Witness / Public Qualification Binding 最小合同](docs/183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
  从审计闭合后的 exact main 分离 RelationSet semantics、provenance bytes、qualification 与 admission authority。
  候选保持 RelationSet 0.1 与八文件 Manifest 0.1 不变，选择 versioned DerivationEvidence 0.2 作为 witness
  carrier；deterministic application 仍拥有 admission rule 与 witness construction，Evidence 只承载，Manifest
  只绑定。合同只冻结 private admission、可复算 witness 与 public binding shape；实现授权严格限于文档 183
  的 A–F private closed proof，publisher、Slice、Coverage 与公共 Bundle 写入仍未授权。
- [RelationSet Admission / Public Qualification Binding 合同冻结发布](docs/185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)
  保留 PR #171 的 `UNKNOWN` 首败、独立 PR #172 测试观察维护、新 source state 的两次同-head 11/11、
  candidate exact-main 双门、首次 README 匿名配额首败、三份 fresh paired readback 与能力地图 render-only
  readback。该发布自己的门、合入和 fresh exact-main readback 全部成立后，合同才成为 frozen 并只授权 A–F；
  `RelationSet 0.1`、八文件 Manifest、架构 DOT/SVG 与所有历史失败均不被改写。
- [RelationSet Admission / Public Qualification Binding 实现冻结候选](docs/186-r1-relation-set-admission-and-public-qualification-binding-implementation-freeze-candidate.md)
  记录文档 183 A–F 的 private admission、explicit witness、Evidence 0.2 Schema/corpus/projection、PR #174、
  implementation exact-main 11/11 与 Browser Smoke 1/1，以及十五份变更文件的匿名 exact-SHA 字节读回。
  Evidence projection 只接受已经 admission 的 private state，不能从 raw candidates 或 caller witness 补资格；
  conflict 保留全部候选且没有 winner。候选随后经 PR #175 原始 11/11、受保护主线合入、exact-main 双门与
  README/本文/milestones 三份互不复用的 fresh anonymous installed-product readback 闭合；候选历史状态仍不被
  后继冻结发布改写。
- [RelationSet Admission / Public Qualification Binding 实现冻结发布](docs/187-r1-relation-set-admission-and-public-qualification-binding-freeze-publication.md)
  发布 PR #174 implementation、PR #175 docs-only candidate、exact-main 门、十五文件 source identity 与三份
  installed-product readback 的完整因果链。冻结只覆盖 private admission、explicit witness 与 Evidence 0.2
  binding；publisher、公共 Bundle、Manifest role 扩张、Slice、Coverage 与 Attention 仍未获授权。本文自己的
  门、合入、新 exact-main 双门与三份 fresh readback 全部成立后，下一步只能做 post-admission system audit。
- [Post-Admission ReviewSlice Input / Obligation Closure 系统审计](docs/188-r1-post-admission-review-slice-input-obligation-closure-system-audit.md)
  从 exact admission-freeze main 证明两个独立缺口：Coverage 可以为不存在的 Slice 自报 completed，也可以与
  SliceSet 一起把 Policy+FactSet 明确存在的 anchor/spec denominator 缩为空后继续自洽地声称 `COMPLETE`。
  审计同时确认 Slice semantic identity 可以跨合法 attempt 复用，但 execution eligibility 必须从 exact owned
  admission history 继续，不能靠 raw RelationSet 或 digest 继承。下一问题面只到 admitted-graph input 与
  anchor/spec obligation closure；BFS、SliceSet、Coverage、publisher 与 Schema 修改均未开始。
- [ReviewSlice Admitted-Graph Input / Anchor-Spec Obligation Closure 合同](docs/189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md)
  合同只定义 exact DerivationInputSet、qualification history、admitted RelationSet 与 same-attempt live
  continuation 的输入闭包，以及不可缩小的 anchor/spec domain、逐项 outcome 和 private reconciliation。
  semantic domain/Slice identity 可以跨合法 attempt 复用，execution closure receipt 不能复用；实现授权只覆盖
  文档 189 A–H 的 private closed proof，Schema、ReviewSliceSet、CoverageLedger、publisher 与公共 Bundle 仍未授权。
- [ReviewSlice Input / Obligation Closure 合同冻结发布](docs/190-r1-review-slice-input-obligation-closure-contract-freeze-publication.md)
  保存 PR #179 original 11/11、candidate exact-main 双门、README/文档 189/milestones 三份独立 anonymous
  installed-product readback 与 canonical manifest。该发布自己的门、合入、新 exact-main 双门及 fresh readback
  全部成立后，合同才成为 frozen 并只授权 A–H；BFS 产品化、公共 Schema、SliceSet、Coverage 与 publisher
  不因合同冻结自动获得资格。
- Q0 只冻结 Verification Scheduling 的身份与权威边界。Q 缺失或卸载时必须退回完整串行验证，
  Verification semantics 不得变化。

## 公开证据与安全边界

`Public CI` 和 `Browser Smoke` 提供平台对齐、双 Python、构建、真实 Chromium 与公开资产读回的快速
基线。它们不能替代物理键盘、完整真实项目、受控宿主机资源停止线或清理读回；GitHub 绿灯不自动等于
整个里程碑 `PASS`。

VeriTrail 的安全边界同样是有界的：

- 默认只接受显式回环目标，不读取浏览器 Profile，不持久化 Cookie、Authorization 或响应正文；
- Plan、Evidence、报告与附件通过规范化 JSON、清单和 SHA-256 建立可复核关系；
- M9/M10 只运行结构化、经预览摘要批准的可信本地命令，不接受 Shell 字符串；新版 Preview 还绑定
  精确受保护源码状态，并在启动前复核，边界见[获批源码状态连续性维护合同](docs/168-approved-source-state-continuity-maintenance-contract.md)；
- Windows Job Object、listener owner 与资源上限限制误杀和残留，但不构成恶意代码沙箱；
- AI 可以提出关注候选、解释异常或建议补证，不能确认缺陷真值，也不能决定 `PASS / FAIL`。

## 信任与认识论上限

VeriTrail 擅长发现封存坐标之后的漂移、错绑、漏证据与规则不一致；它不能仅凭一条内部自洽的证据链
证明最初事实真实，也不能裁定提出者的观点在终极意义上正确。

```text
Consistency != Authenticity != Truth
Verification Correctness != Specification Correctness
Not responsible for Truth != Not responsible for Uncertainty
```

现实若模糊、不完整、冲突或不可判，系统必须保留这种不确定性。精确边界见
[产品定义](docs/00-product-brief.md)与[GitHub Evidence Plugin 合同](docs/78-github-evidence-plugin-contract.md)。
简单说：**它防的是漂移，不是阴谋；它负责的是裁决秩序，不是真理本身。**

## 系统家族与未来边界

VeriTrail 不是把所有能力都吸进 Core 的“超级平台”。跨系统关系应通过稳定合同、不可变 Artifact 和
可替换 adapter 建立：

| 系统 / 轨道 | 负责 | 关系状态 |
| --- | --- | --- |
| [JPyxis](https://github.com/NoctilumeDev/JPyxis) | 异构计算中的控制、定义与运行时分权 | 独立系统；未来可通过 execution receipt / Evidence adapter 对接 |
| [FlowKernel](https://github.com/NoctilumeDev/FlowKernel) | 不可靠策略与确定性权限、资源、隔离边界 | 独立 Planned 仓库；不是当前可运行依赖 |
| Platform / P | 观察外部平台事实 | 已有 GitHub 0.1.0；其他平台仍是候选 |
| Review / R | 压缩人的代码审查注意力 | private closed Relation derivation 与 Relation observation / composition qualification 已冻结；private RelationSet admission / witness / Evidence 0.2 为实现冻结候选；Slice、Coverage 与公开产品化尚未开始 |
| Quick / Q | 优化证明义务的 wall-clock 与重算 | Q0 蓝图冻结；实现未开始 |
| Operations Evidence / O | 候选运行事实观察面 | O0 只记录问题与权威边界；没有插件、Provider、Schema 或动作权 |
| Test Evidence / T | 候选测试事实观察面 | T0 只记录问题；测试选择、执行、重试与 fixture authority 仍为 `UNKNOWN` |

这些关系是认知地图，不是当前集成声明。一个独立系统最多通过不可变 Artifact / Evidence adapter 接入
VeriTrail；事件可以跨界，状态所有权、执行入口、凭据与 Verdict 权不能跨界。

拆分也不由模块数量、业务名词或数据库数量机械决定。这里采用的原则是：**最小闭环内部允许与同一
不变量一致的强耦合；闭环之间必须通过稳定合同强解耦。**边界未知时先建立可验证的最小闭环，等待真实
反例暴露 state ownership、事务、失败恢复和独立生命周期压力。完整判据见
[能力边界与系统认知地图](docs/114-capability-boundary-and-system-map.md)。

## 发布坐标

- 当前 Latest Core：[`v0.13.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.13.0)，详见
  [0.13.0 Release Notes](docs/103-v0.13.0-release-notes.md)与
  [发布与公开读回事实](docs/106-core-v0.13.0-release-readback-facts.md)；
- 历史维护坐标：`v0.12.0 / v0.12.1 / v0.12.2` 均不可移动；
- GitHub Evidence Plugin：[`github-evidence-v0.1.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.0)，
  为 non-Latest 独立 Release；
- Starter 与 Authoring Skill：独立 `0.2.0` 坐标，并继续保持其 Core 0.12.x 兼容边界；
- [Core 0.12.2 发布与公开读回事实](docs/76-core-v0.12.2-release-readback-facts.md)继续保存旧维护线的精确证据。

已发布标签、资产和历史失败不得移动、重制或用后续绿灯覆盖。完整坐标与摘要见
[里程碑与文档索引](docs/milestones.md)。

## 阅读路径

### 第一次来

1. [十分钟 PASS / 故意 FAIL](START_HERE.md)
2. [产品定义](docs/00-product-brief.md)
3. [证据与实验模型](docs/01-evidence-model.md)

### 想理解系统边界

1. [架构与安全边界](docs/02-architecture.md)
2. [验收标准](docs/03-acceptance.md)
3. [能力边界与系统认知地图](docs/114-capability-boundary-and-system-map.md)

### 想知道当前主线之外保留了哪些问题

- [Product Delivery D0：真实任务入口的问题定位](docs/166-d0-product-delivery-problem-framing.md)与
  [Cu0：工程记忆注意力投影的问题定位](docs/167-cu0-engineering-memory-attention-projection-problem-framing.md)
  是 2026-09-15 的候选认知记录，不授权施工；Review Attention R 仍是当前串行施工主线，继续遵守自身合同门禁。
- [O0 Operations Evidence：运行事实观察的问题定位](docs/180-o0-operations-evidence-problem-framing.md)与
  [T0 Test Evidence：测试事实观察的问题定位](docs/181-t0-test-evidence-problem-framing.md)是 2026-09-21
  从 Core 通用性复核中保留下来的候选方向。两者都不改 Core，也未冻结“两个插件”的最终部署形状。
- [Q0 Quick Verification Scheduling 冻结记录](docs/119-q0-verification-scheduling-final-freeze-closure.md)
  已经存在；新的优先顺序不改写 Q0，也不启动 Q 实现。

### 想复核工程事实

1. [里程碑冻结历史与完整文档索引](docs/milestones.md)
2. [M14 最终验证与发布事实](docs/56-m14-final-validation-and-release-facts.md)
3. [GitHub Evidence Plugin 发布读回](docs/108-p4-github-evidence-release-readback-facts.md)
4. [Review Attention Pattern Corpus 冻结闭环](docs/112-review-attention-pattern-corpus-freeze-closure.md)
5. [Review Attention R1 合同](docs/113-r1-deterministic-semantic-slice-contract.md)
6. [Review Attention R1 Schema payload 冻结发布](docs/126-r1-schema-payload-freeze-publication.md)
7. [Review Attention R1 Derivation Input Binding 合同冻结发布](docs/133-r1-derivation-input-binding-contract-freeze-publication.md)
8. [Review Attention R1 Derivation Input Binding 实现冻结候选](docs/134-r1-derivation-input-implementation-freeze-candidate.md)
9. [Review Attention R1 Derivation Input Binding 最小运行切片冻结发布](docs/135-r1-derivation-input-freeze-publication.md)
10. [Review Attention R1 Derivation Attempt 与 Fact Provenance 前置审计](docs/136-r1-derivation-attempt-and-fact-provenance-audit.md)
11. [Review Attention R1 Derivation Attempt 与 Fact Provenance 合同候选](docs/137-r1-derivation-attempt-and-fact-provenance-contract.md)
12. [Review Attention R1 Derivation Attempt 与 Fact Provenance 合同冻结发布](docs/138-r1-derivation-provenance-contract-freeze-publication.md)
13. [Review Attention R1 DerivationEvidence Schema 修正前置审计](docs/139-r1-derivation-evidence-schema-correction-audit.md)
14. [Review Attention R1 DerivationEvidence Schema 0.1.1 修正合同](docs/140-r1-derivation-evidence-schema-correction-contract.md)
15. [Review Attention R1 DerivationEvidence Schema 0.1.1 修正合同冻结发布](docs/141-r1-derivation-evidence-schema-correction-contract-freeze-publication.md)
16. [Review Attention R1 DerivationEvidence Schema 0.1.1 实现冻结候选](docs/142-r1-derivation-evidence-schema-correction-implementation-freeze-candidate.md)
17. [Review Attention R1 DerivationEvidence Schema 0.1.1 实现冻结发布](docs/143-r1-derivation-evidence-schema-correction-freeze-publication.md)
18. [Review Attention R1 Derivation Budget Primitive 前置审计](docs/144-r1-derivation-budget-primitive-precontract-audit.md)
19. [Review Attention R1 Derivation Budget Primitive 最小合同候选](docs/145-r1-derivation-budget-primitive-contract.md)
20. [Review Attention R1 Derivation Budget Primitive 合同冻结发布](docs/146-r1-derivation-budget-primitive-contract-freeze-publication.md)
21. [Review Attention R1 Derivation Budget Primitive 实现冻结候选](docs/147-r1-derivation-budget-primitive-implementation-freeze-candidate.md)
22. [Review Attention R1 Derivation Budget Primitive 实现冻结发布](docs/148-r1-derivation-budget-primitive-freeze-publication.md)
23. [Review Attention R1 Derivation Execution Cell 与 Terminal Continuity 系统审计](docs/149-r1-derivation-execution-cell-system-audit.md)
24. [Review Attention R1 Derivation Execution Cell / Terminal Envelope 合同候选](docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md)
25. [Review Attention R1 Derivation Execution Cell / Terminal Envelope 合同冻结发布](docs/151-r1-derivation-execution-cell-contract-freeze-publication.md)
26. [Review Attention R1 Derivation Execution Cell 实现冻结候选](docs/152-r1-derivation-execution-cell-implementation-freeze-candidate.md)
27. [Review Attention R1 Derivation Execution Cell 实现冻结发布](docs/153-r1-derivation-execution-cell-freeze-publication.md)
28. [Review Attention R1 Fact Admission 与 DerivationEvidence Closure 系统审计](docs/154-r1-fact-evidence-closure-system-audit.md)
29. [Review Attention R1 Fact Admission / DerivationEvidence Closure 最小合同候选](docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md)
30. [Review Attention R1 Fact Admission / DerivationEvidence Closure 合同冻结发布](docs/156-r1-fact-evidence-closure-contract-freeze-publication.md)
31. [Review Attention R1 Fact Admission / DerivationEvidence Closure 实现冻结候选](docs/157-r1-fact-evidence-closure-implementation-freeze-candidate.md)
32. [Review Attention R1 Fact Admission / DerivationEvidence Closure 实现冻结发布](docs/158-r1-fact-evidence-closure-freeze-publication.md)
33. [Review Attention R1 Fact/Evidence 冻结后下一闭环系统审计](docs/159-r1-post-fact-evidence-next-closure-system-audit.md)
34. [Review Attention R1 Multi-Provider Applicability / Fact Composition 最小合同候选](docs/160-r1-multi-provider-applicability-and-fact-composition-contract.md)
35. [Review Attention R1 Multi-Provider Applicability / Fact Composition 合同冻结发布](docs/161-r1-multi-provider-fact-composition-contract-freeze-publication.md)
36. [Review Attention R1 Multi-Provider Applicability / Fact Composition 实现冻结候选](docs/162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md)
37. [Review Attention R1 Multi-Provider Applicability / Fact Composition 实现冻结发布](docs/163-r1-multi-provider-fact-composition-freeze-publication.md)
38. [Review Attention R1 Multi-Provider Fact Composition 冻结后下一闭环系统审计](docs/164-r1-post-composition-next-closure-system-audit.md)
39. [Review Attention R1 Relation Derivation Authority / Operand Continuity 最小合同候选](docs/165-r1-relation-derivation-authority-and-operand-continuity-contract.md)
40. [Review Attention R1 Relation Derivation Authority / Operand Continuity 合同冻结发布](docs/170-r1-relation-derivation-contract-freeze-publication.md)
41. [Review Attention R1 Relation Derivation 实现冻结候选](docs/171-r1-relation-derivation-implementation-freeze-candidate.md)
42. [Review Attention R1 Relation Derivation 实现冻结发布](docs/172-r1-relation-derivation-freeze-publication.md)
43. [Review Attention R1 Declared Relation Observation Domain / Composition Qualification 系统审计](docs/173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md)
44. [Review Attention R1 Declared Relation Observation Domain / Composition Qualification 最小合同候选](docs/175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
45. [Review Attention R1 Declared Relation Observation Domain / Composition Qualification 合同冻结发布](docs/176-r1-relation-observation-composition-qualification-contract-freeze-publication.md)
46. [Review Attention R1 Relation Observation / Composition Qualification 实现冻结候选](docs/178-r1-relation-observation-composition-qualification-implementation-freeze-candidate.md)
47. [Review Attention R1 Relation Observation / Composition Qualification 实现冻结发布](docs/179-r1-relation-observation-composition-qualification-freeze-publication.md)
48. [Review Attention R1 RelationSet Admission / Qualification Evidence Binding 系统审计](docs/182-r1-post-qualification-relation-set-admission-and-evidence-binding-system-audit.md)
49. [Review Attention R1 RelationSet Admission / Explicit Admission Witness / Public Qualification Binding 最小合同](docs/183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
50. [Review Attention R1 RelationSet Admission / Public Qualification Binding 合同冻结发布](docs/185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)
51. [Review Attention R1 RelationSet Admission / Public Qualification Binding 实现冻结候选](docs/186-r1-relation-set-admission-and-public-qualification-binding-implementation-freeze-candidate.md)
52. [Review Attention R1 RelationSet Admission / Public Qualification Binding 实现冻结发布](docs/187-r1-relation-set-admission-and-public-qualification-binding-freeze-publication.md)
53. [Review Attention R1 Post-Admission ReviewSlice Input / Obligation Closure 系统审计](docs/188-r1-post-admission-review-slice-input-obligation-closure-system-audit.md)
54. [Review Attention R1 ReviewSlice Admitted-Graph Input / Anchor-Spec Obligation Closure 最小合同](docs/189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md)
55. [Review Attention R1 ReviewSlice Input / Obligation Closure 合同冻结发布](docs/190-r1-review-slice-input-obligation-closure-contract-freeze-publication.md)
56. [Q0 最终冻结闭环](docs/119-q0-verification-scheduling-final-freeze-closure.md)

## 项目来源与协作

VeriTrail 的方法来自受限单机上的真实工程实践：单变量验证因果、组合 Profile 覆盖交互、固定种子复现
偶发故障，并在资源停止线内守住一致性。PlainJournal 的 M0–M8 冻结基线是重要参考案例，但 VeriTrail
不把任何电商服务、中间件或业务状态机硬编码为产品前提。

- 提交可复现缺陷、边界明确的能力提案或 Pull Request 前，请阅读[贡献指南](CONTRIBUTING.md)；
- 参与公开讨论与评审时，请遵守[社区行为准则](CODE_OF_CONDUCT.md)；
- 安全问题不要公开披露，请按[安全策略](SECURITY.md)使用私下报告路径。

## License

[Apache License 2.0](LICENSE)
