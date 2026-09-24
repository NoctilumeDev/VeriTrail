# Vera 方法参照：可吸收经验与边界记录

> 状态：`RELATED_WORK_NOTE / NON_AUTHORITATIVE / NO_IMPLEMENTATION_AUTHORITY`
>
> 观察日期：2026-09-24
>
> VeriTrail 基线：`main@1518e5ef7b8d4ee0a4af67524390d1a48cd4f150`
>
> Vera 论文：arXiv `2607.01793v2`（2026-07-04）
>
> Vera 公开源码：`Yunhao-Feng/Vera@9bd5ffd7e2c9219e458ff5b4df0510b645979d98`

本文只保存一次外部方法参照。它不修改 VeriTrail 的产品定义，不重解释既有冻结事实，也不授权
R1、Q、O、T、Core、Schema、publisher、运行时或 benchmark 施工。

## 1. 结论边界

Vera 与 VeriTrail 共享几条重要纪律：执行者的自报不能替代可观察事实；动作记录不能自动证明效果；
最终判断应尽量由可复算的确定性机制形成；不同 Agent 或 Evidence producer 不应因此获得裁决权。

这种相似不足以支持“机制同构”“角色对立”或“天然上下游”。更准确的关系是：

```text
Vera
  domain-specific agent safety testing
  + automated risk / case construction
  + adaptive adversarial execution
  + case-specific evidence-grounded verification

VeriTrail
  domain-general declared acceptance contract
  + evidence / provenance qualification
  + explicit epistemic outcome model
  + deterministic acceptance adjudication
```

Vera 主要回答：**一个具体 safety outcome 是否在有界沙箱中实际发生？**

VeriTrail 主要回答：**给定事先封存的 claim 与有来源、有边界、可能缺失或冲突的 Evidence，当前最多有资格支持什么 Verdict？**

两者可以在 Artifact 边界上组合，但当前没有 Vera adapter，也没有任何集成实现。

## 2. 直接支持的共同点

### 2.1 自报不是结果

Vera 明确以执行动作及其 observable effects 判定结果；仅把对抗内容放进 prompt、tool result 或初始环境，
不算攻击成功。VeriTrail 同样不允许 Report、UI、AI 或 Producer 自己决定 Verdict。

可迁移的不变量是：

```text
reported completion != observed effect
attempt evidence != effect evidence
execution completed != claim qualified
```

### 2.2 确定性机制保留最后判断

Vera 的 case-specific verifier 是确定性 Python 程序，成功主张必须由它结合环境状态、tool-call records
或 response 证实。VeriTrail Core 只按版本化规则从 sealed Plan 与标准 Evidence 重算 Verdict。

两边的确定性机制并不等价。Vera 使用 safety-goal-specific predicate；VeriTrail 使用预先封存的验收条件、
Evidence 合同与公开 Verdict 语义。

### 2.3 Artifact 保留比结论文本更重要

Vera 为 retained run 保存 `attack_plan`、完整 tool log、normalized trace 与 `verify.py`；VeriTrail 保存
Plan、Evidence、Run、Verdict、Bundle、Manifest 与 provenance。共同点不是文件名，而是让第三方不必只信
一段总结文字。

### 2.4 隔离属于实验语义

Vera 为并行执行分配独立 Docker Compose project、network namespace、service state 与 port offset。
这提示 VeriTrail 后继调度不能把并行只理解为吞吐优化：lane 的 environment identity、state ownership、
resource namespace、cleanup 与 join provenance 都会影响结果归属。

## 3. 不能抹平的差异

| 问题 | Vera | VeriTrail |
| --- | --- | --- |
| 首要目标域 | Agent safety 风险发现、case 构造、攻击执行与验证 | 通用软件验收的计划、证据、裁决与可复算历史 |
| 标准来源 | 自动化 taxonomy / case compilation 生成 safety goal、初始状态与 verifier | Human authority 封存 Plan；AI 只能起草，不能 Seal 或裁决 |
| 执行策略 | Control Agent 根据运行时观察自适应改变攻击步骤 | 当前 Core 验收条件固定；未来 Q 只能调度证明义务，不能改变条件 |
| Evidence 关系 | 对给定 goal，按 `state ▷ tool ▷ response` 的可定义 predicate fallback | Plan 声明所需 Evidence；缺失、冲突、过期和不可归因不能被全局优先级覆盖 |
| 结果模型 | case predicate 输出 `y ∈ {0,1}`；ESR 排除 infrastructure failure | `ExecutionStatus` 与 `PASS / FAIL / INCONCLUSIVE / PENDING` 正交 |
| 判断对称性 | Control Agent 报失败时可直接记录 `y=0`；报成功时才强制 verifier | Producer 报成功或失败都不能直接成为 Verdict |
| verifier 生命周期 | 公开实现可在执行后结合 recent turns 生成 `verify.py`，脚本失败时最多重生成三次 | 规则若在观察结果后改变，必须形成新的版本与资格历史，不能冒充原 sealed rule |
| 信任边界 | 威胁模型假定攻击者不能修改 target model、system instructions、agent implementation 或 internal tool code | 明确承认哈希不证明真实性，同一控制方可制造内部自洽 Bundle；Core 不拥有世界真相 |
| 基线 | 同一 base scenario 有 benign、single-channel、multi-channel 三种 setting | Baseline、paired counterfactual、expiry、observer effect 等是一般实验合同的一部分 |

因此，Vera 不是只有攻击者：它也运行 benign task 并验证合法任务是否完成。VeriTrail 也不是“公证人”或
“真理法庭”：它只判断封存条件与 Evidence 的关系，不替 Evidence 证明来源真实性。

## 4. 值得吸收的方法

### 4.1 把 Claim 编译成 executable proof obligations

Vera 把 executable safety case 表达为 `σ = <g, s0, Vg>`。VeriTrail 不应照搬这个三元组，但可以继续追问：

```text
sealed claim
  -> initial-state requirements
  -> required observation obligations
  -> deterministic predicates
  -> admissible Verdict set
```

这与 R1 已经暴露出的 `responsibility defined != responsibility discharged` 同向。它可以成为未来 Core、
T/O Evidence 或 conformance corpus 的研究问题；不是修改 doc189 A-H 的许可证。

### 4.2 区分 attempt evidence 与 effect evidence

Vera 的环境状态优先，不应复制成 VeriTrail 的全局 Evidence 优先级；其中可吸收的原则是：每个 claim
应明确哪些 observation 只证明“尝试过”，哪些足以证明“效果已发生”。

```text
tool call recorded != effect realized
test process exit 0 != acceptance invariant satisfied
agent says changed != exact bytes changed
PR merged != exact-main gates qualified
```

### 4.3 允许执行策略自适应，保持 oracle 身份固定

Vera 展示了运行时观察驱动的自适应执行价值。对 VeriTrail，值得保留的更强纪律是：

```text
sealed proof obligations stay fixed
  -> scheduler observes missing evidence
  -> scheduler chooses the next bounded action
  -> PASS conditions and denominator do not move
```

这是未来 Q 的候选方法，不是对 Vera 当前 verifier 生命周期的照抄。任何 AI 生成的 Assertion、Evidence
requirement 或 verifier 都只能作为 candidate；观察结果出现后再修改 oracle，必须获得新的版本身份与 Seal。

### 4.4 同时 falsify Subject、Verifier、Producer 与 Harness

Vera 的 benign setting 能暴露 case initialization 或 verifier calibration 的问题。VeriTrail 已经多次遇到
fixture timing、collector observability 与 readback harness 缝隙，可以把这种经验整理成四类反例：

```text
subject falsifier
verifier / rule falsifier
evidence-producer falsifier
harness / observer falsifier
```

通过“被测对象正确时会不会误杀”的正向对照，避免每个红灯都被归给 Subject。

### 4.5 把组合生成用于 conformance corpus

Vera 用 risk × attack method × environment 扩展 safety case。VeriTrail 不应据此自动扩大用户已经 Seal
的 acceptance criteria；组合生成更适合检验自身语义：

```text
claim type
× evidence source
× missing / stale / conflicting / tampered
× completed / aborted / error
× same-attempt / cross-attempt
× exact / replayed / duplicated
```

这可能形成一个带 gold semantics 的 Acceptance / Evidence Conformance Corpus，机械区分 `PASS`、`FAIL`、
`INCONCLUSIVE`、`PENDING` 及其与 `ExecutionStatus` 的组合。是否建设，须在 R1 闭合后另行审计。

### 4.6 把 benchmark 当作可移植反例集合

Vera-Bench 的价值不仅是规模数字，还在于 executable case 可以跨四种 Agent framework 运行。若 VeriTrail
走论文或公共评测路线，真正可复核的成果应包含极小、可移植、有 gold semantics 的世界，而不只是框架描述。

候选 world 可以包括：stale Evidence、conflicting Evidence、post-hoc rule mutation、baseline expiry、
observer contamination、cross-attempt transplant、false success report，以及 successful tool call without effect。

## 5. 明确不吸收的做法

### 5.1 不采用非对称自报裁决

Vera 为攻击成功率统计采用“Control Agent 报失败则 `y=0`，报成功才 verifier 确认”的非对称规则。
VeriTrail 保持：

```text
producer says success != PASS
producer says failure != FAIL
```

### 5.2 不在结果出现后静默重生成 oracle

Vera 重生成 syntax/schema 失败的 verifier 有其降低 false negative 的目的。VeriTrail 若修正规则或 verifier，
必须建立新的 source、version、Seal 与 Evidence identity；后继成功不能覆盖原失败。

### 5.3 不建立全局 Evidence 排名

`state ▷ tool ▷ response` 是 Vera 对 safety goal predicate 的 fallback，不是所有 claim 的普遍真理。
VeriTrail 继续由 sealed Plan / Profile 决定 required Evidence；相互冲突的 observation 必须保持可见。

### 5.4 不主张学界空白或公开优先权

软件 acceptance、assurance case、testing 与 reproducibility 已有长期研究传统。Vera 的 v1 也早于 VeriTrail
公开仓库。VeriTrail 的 2026-08-08 首个公开提交 `b84300647a0002962b797c43a509e1d799220ee4`
已经包含 sealed Plan、控制变量、四 Verdict、正交 ExecutionStatus、baseline、paired run 与
observer effect 等核心边界。这只能证明这些语义不是本次阅读 Vera 后才追加进仓库；它不能单凭 Git 历史
证明认知来源，也不能推出“首先发现”“独立首创”或“拥有验收定义权”。

## 6. 后继使用坐标

| 候选去向 | 可吸收问题 | 当前状态 |
| --- | --- | --- |
| R1 | 不吸收；保持 doc189 A-H 与 E-stage 停止线 | `NO_CHANGE` |
| Core 后继审计 | Claim 到 executable proof obligations 的机械编译 | `UNASSESSED` |
| Q | fixed obligations 下的 adaptive scheduling 与 lane isolation | `Q0_ONLY / NOT_STARTED` |
| O / T | attempt/effect Evidence 分类与 Producer/Harness falsifier | `PROBLEM_FRAMING_ONLY` |
| Benchmark / paper | Acceptance / Evidence Conformance Corpus | `CANDIDATE_RESEARCH_QUESTION` |
| Vera adapter | 把 Vera retained artifacts 导入标准 Evidence | `HYPOTHESIS / NO_IMPLEMENTATION` |

可能的组合只到概念层：

```text
Vera retained run artifacts
  -> future read-only Evidence adapter
  -> sealed VeriTrail AcceptancePlan
  -> Core evaluates a separately declared higher-level claim
```

Vera 的 verifier result 不能直接成为 VeriTrail Verdict；VeriTrail 也不替 Vera 发现风险、生成攻击或证明
其工具环境真实无欺骗。

## 7. 仍需后继审计的问题

1. executable proof obligation 与现有 Assertion / Evidence requirement 的边界是否已经足够，还是确有缺口？
2. AI 起草 verifier 时，什么信息必须在 Seal 前固定，什么运行时参数允许延迟绑定？
3. conformance corpus 的 gold semantics 由谁拥有，怎样避免 benchmark 自己成为未审裁判？
4. Q 的 adaptive scheduling 如何证明没有缩小 denominator、跳过 hard gate 或跨 attempt 继承 authority？
5. Vera Artifact 若进入 adapter，哪些是 source Evidence，哪些只是一方生成的派生声明？

在这些问题形成内部反例以前，本记录只用于扩大后继审计的反例搜索空间。

## 8. 来源

- [Vera 论文：Safety Testing LLM Agents at Scale](https://arxiv.org/abs/2607.01793)
- [Vera 官方仓库](https://github.com/Yunhao-Feng/Vera)
- [NIST SP 500-180：Guide to Software Acceptance](https://www.nist.gov/publications/guide-software-acceptance)
- [NIST CSRC：assurance case](https://csrc.nist.gov/glossary/term/assurance_case)
- VeriTrail 本地边界：[产品定义](00-product-brief.md)、[Evidence 模型](01-evidence-model.md)、
  [架构](02-architecture.md)、[能力边界与系统认知地图](114-capability-boundary-and-system-map.md)
