# 验迹是否提高开发效率？

## ——从代码生成速度到工程闭环的自主运行

> 状态：`RESEARCH_NOTE / NON_NORMATIVE / NO_R1_STATE_CHANGE / NO_IMPLEMENTATION_AUTHORITY`
>
> 观察日期：2026-10-15
>
> VeriTrail 基线：`main@2a97b5cd6cdf0598db07a26d3640e4408f84713b`
>
> 案例：`NoctilumeDev/Qixu` 与 `NoctilumeDev/GuiHongMail`

本文记录两次工程实践对一个问题提供了什么证据：**验迹是否提高开发效率？**

它不修改 VeriTrail 的产品定义、R1 合同、冻结状态或 roadmap，不授权 R1、persistence、Coverage、Schema、
runtime、publisher、CLI 或后继研究施工。文中的时间、提交与人工介入只按各项目实际保留的口径陈述；两个案例的
记录结构不同，不能把相似的墙钟数字直接当成可比实验结果。

## 1. 先把“效率”拆开

如果效率只指单位时间生成多少代码，现有证据不能回答验迹是否更快。验迹会增加 Plan、Evidence、负控、fresh
checkout、公开读回和失败保留，本身也会引入采集器、路径、序列化与证明设施问题。

但软件工程的完成条件不只是“代码已经生成”。至少还有四个不同问题：

```text
实现速度
    代码和测试多快产生

工程闭环吞吐
    多快得到边界明确、可复核的合格交付

人工协调成本
    人需要多久、多少次回到执行关键路径

恢复与交接成本
    失败、换模型、压缩上下文或换工作树后，需要重建多少事实
```

验迹最可能改变的是后三项。它提供的不是自动施工本身，而是独立、可重复的裁决依据：

```text
Human Seal / contract
        ↓
Agent implements and runs
        ↓
independent evidence collection
        ↓
VeriTrail adjudicates
        ↓
Agent / scheduler continues or stops under the contract
```

因此要把两件事分开：

```text
Agent + contract
    owns automatic continuation

VeriTrail
    supplies independent, reproducible adjudication
```

只有二者组合，人才有可能不再持续占据工程执行的关键路径。

## 2. 案例一：期序

### 2.1 可直接观察的事实

期序的 Git 历史从根提交
[`5ca946d`](https://github.com/NoctilumeDev/Qixu/commit/5ca946da02032ebd8f9a0064add3f977b2da7bb5)
开始冻结 M0 合同与 Evidence gates，到
[`4cbdbd2`](https://github.com/NoctilumeDev/Qixu/commit/4cbdbd276ed03c838973b74399c0c03d980fc84e)
发布 M9 qualified engineering candidate：

| 观察项 | 事实 |
| --- | --- |
| 首个合同提交 | 2026-10-03 01:45:50 +08:00 |
| M9 候选发布 | 2026-10-04 11:21:45 +08:00 |
| Git 可观察区间 | 33 小时 35 分 55 秒 |
| 区间内主线可达提交 | 34 个，含起止提交 |
| 主要范围 | MySQL 与事务、权限、确定性分配、候补、恢复与治理、浏览器与故障反例、两次 fresh reproduction、公开候选 |

这不是简单 CRUD。提交历史同时保留了合同、实现、真实反例、修复、保护合入和可复现发布候选。

### 2.2 证据边界

这 33 小时 35 分 55 秒是两个提交时间之间的 **Git 可观察区间**，不是连续 Agent 运行时间，也不是人工工时。
期序没有像归鸿一样保存逐次人工介入账册，因此：

```text
存在持续的合同驱动施工与资格闭环
    SUPPORTED

精确人工介入次数
    UNKNOWN

精确人工工作时间
    UNKNOWN

相对无验迹流程节省了多少时间
    UNKNOWN
```

期序能支持的是工程模式的可行性，不支持精确提速幅度。

## 3. 案例二：归鸿

### 3.1 可直接观察的事实

归鸿保存了独立的
[`run-ledger.md`](https://github.com/NoctilumeDev/GuiHongMail/blob/d57b3612b436f3a879867730f0b6f7232b046419/docs/run-ledger.md)
与
[`m6-go.md`](https://github.com/NoctilumeDev/GuiHongMail/blob/d57b3612b436f3a879867730f0b6f7232b046419/docs/acceptance/m6-go.md)：

| 观察项 | 事实 |
| --- | --- |
| M1 第一施工动作 | 2026-10-13T04:06:43.7320975Z |
| M6 最后一项预注册退出门 | 2026-10-14T10:51:37.996974Z |
| 实际墙钟 | 30 小时 44 分 54.2648765 秒 |
| 具名人工介入 | 7 次 |
| 人工实际工时 | UNKNOWN |
| 主要范围 | 三个 Go 服务、MySQL、SeaweedFS S3、RocketMQ、SMTP、分类、故障恢复、双 fresh build、prerelease 读回 |

七次介入主要发生在必须由人承担责任或作出取舍的边界：释放本机资源、修订资源准入、确认 RocketMQ 参数，以及
决定从 Java 迁移到 Go。它们没有被自动系统伪装成技术上唯一的答案。

归鸿也保留了大量无需人工逐次裁决的失败与恢复：环境预检、Broker 权限与内存、采集器错误、对象状态、提交响应
丢失、负控和 fresh reproduction。后继成功没有覆盖这些首败。

### 3.2 证据边界

归鸿比期序多证明了一件事：在复杂度更高、资源条件会改变决策的工程中，连续施工仍能在少量具名介入下保持可追溯
闭环。但“7 次”不能换算成人工工时；也不能与没有验迹的假想流程直接相减。

## 4. 两个案例共同支持什么

两次实践共同支持下列较窄结论：

1. 验迹能够为长时间 Agent 施工提供独立裁决、失败归层、Evidence 追溯和 exact-state 恢复。
2. 合同可以把继续、停止和请求人工判断的条件提前固定，减少每一步都由人重新判断“算不算完成”的需要。
3. 在两个非简单 CRUD 项目中，约 30 多小时的施工窗口内都形成了跨多个阶段的 qualified engineering output。
4. 归鸿进一步观察到：人可以主要在资源、架构取舍与 authority 边界介入，而不必持续监督每个实现和修复动作。

这足以把下面命题当作一个已经获得两次工程实践、但证据强度不同的研究假设：

> **“验迹 + 合同驱动的 Agent 连续施工”可以形成一种无需人工持续监督的连续工程闭环；它是否稳定提高闭环吞吐、降低人工工时，仍需后继项目检验。**

这里的“支持”是两案例可行性证据，不是一般因果定律。

## 5. 仍然没有证明什么

两个案例没有 matched control。模型能力、前期设计、自动化程度、硬件资源、项目领域与实现者经验同时发生作用，
因此目前不能声称：

```text
VeriTrail alone caused the observed delivery time
VeriTrail reduced wall-clock time by X%
VeriTrail reduced human labor by X hours
VeriTrail will reduce long-term rework by X%
```

期序与归鸿的 milestone 也不是等价单位。把它们压成：

```text
qualified milestones / human interventions
```

会重新制造一个失真的 KPI：SMTP 收发、事务恢复、确定性分配和视觉收口的复杂度、风险与验收成本并不相同。

即使故障后能从 SHA、Plan、Evidence 与 Verdict 恢复，也只能先证明恢复过程具有可追溯性与可重入性。没有对照记录，
不能把这种能力直接折算成节约了多少恢复时间。

## 6. 更值得检验的效率假设

传统工程中，验收越严格，通常意味着更多人工复核、更长协调周期。两个案例提示，验迹可能改变的不是单一速度，而是
三者之间的耦合：

```text
acceptance rigor
human coordination cost
delivery cycle
```

更准确的待验证命题是：

> **验迹能否让验收强度提高，而人工协调成本不同比例上升，并在此基础上维持可接受的交付周期？**

即使项目仍用 30 小时，只要在相近人工投入下得到更多可复核的正确性证据、保留更多反例，并降低状态重建的不确定性，
也可能构成效率提升。这种提升属于“单位人工协调所支撑的合格工程强度”，不能只用代码行数或完成速度衡量。

## 7. 后继项目应怎样记录

后继实践若要把假设推进为可量化结论，应在施工前冻结记录口径，至少分别保存：

| 维度 | 最小记录 |
| --- | --- |
| 阶段范围 | 原始合同、风险、退出门与延期项 |
| 墙钟 | 明确起止事件、暂停区间与运行窗口 |
| 人工投入 | 每次介入的原因、起止、active minutes 与决定内容 |
| 自动施工 | 无人工介入的连续区间及其边界 |
| 失败与恢复 | 首败身份、归层、恢复起点、恢复完成与是否复用旧事实 |
| 合格产出 | 通过什么 gates、保留什么 negative controls、哪些声明仍未知 |
| 资源条件 | 模型、硬件、依赖服务、并发与资源停止线 |
| 长期结果 | 后续缺陷、返工、回归、交接和状态重建成本 |

这些量应分别保留，不强行合成一个总分。若条件允许，再选择范围、模型、硬件和质量要求相近的项目或阶段作对照；
否则继续把结论保持在 case-study 层级。

## 8. 真正值得优化的不是裁决速度

当前最有价值的工程方向，是降低新项目接入验迹的边际成本。可以复用的包括：

```text
resource collection
fresh-checkout rebuild
fault injection harness
negative-control patterns
release / public readback
cleanup and residual hygiene
```

但模板只能复用机制，不能默认继承 oracle 与 authority：

```text
collector template may be reusable
acceptance truth is project-owned

readback harness may be reusable
what counts as qualified remains contract-owned
```

如果“什么算正确”和“谁有资格裁决”也被模板默认继承，验迹就会退化成自动盖章系统。

## 9. 当前结论

目前最稳的结论不是“AI 两天写完了两个复杂项目”，也不是“验迹已经证明能提速”。

更准确的说法是：

> **过去往往需要人持续介入才能维持的工程闭环，在期序与归鸿两次实践中，已经开始能够依靠合同、Agent 与独立裁决连续运行；人主要回到需要承担责任、修改边界或作出现实取舍的位置。**

已经得到支持的是连续施工能力、独立裁决、失败历史、可重入状态和较低的持续人工占用。尚待证明的是：在相同质量要求
下，这套方式能否稳定减少总墙钟、人工工时和长期返工成本，以及分别减少多少。

因此，下一阶段真正值得研究的问题是：

> **验迹能否打破验收强度、人工投入和交付周期之间的强耦合关系？**

本文到此只形成研究问题与两案例观察，不改变任何 VeriTrail 主线状态。后继 R1 施工仍必须从新的 exact main 与
CONTROL LOOP 重新取得 authority。

## 10. 观察坐标

```text
Qixu
  start/root  5ca946da02032ebd8f9a0064add3f977b2da7bb5
  end         4cbdbd276ed03c838973b74399c0c03d980fc84e
  inclusive main-reachable commits  34

GuiHongMail
  observed repository head  d57b3612b436f3a879867730f0b6f7232b046419
  docs/run-ledger.md SHA-256
    5758e3fa711d39499a0fe01de4e9c4560ff4d840fb25e0e1244928f3059a16ba
  docs/acceptance/m6-go.md SHA-256
    2dba179505fa284285077a94a491f724b917d9227cb2111f06bc45539a010e2a
```

这些坐标只支持本文列出的工程观察，不授予对两个项目未记录的人工作时、对照组或长期维护结果作推断。
