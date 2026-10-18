# Post-R1 外部错题本 Benchmark 与 Oracle 资格计划 0.1

日期：2026-10-19

## 1. 状态与目的

本文保存 R1 完整闭合后的外部反例攻击计划，避免当前研究所得在后续阶段被压缩成“找一些公开案例跑测试”。
它不是 R1 合同、Benchmark 合同、Oracle 实现、测试语料、R2/R3 授权或当前施工状态。

```text
POST_R1_EXTERNAL_COUNTEREXAMPLE_BENCHMARK_PLAN_0_1
    PLANNED
    NOT_STARTED
    NOT_AUTHORIZED_FOR_CURRENT_R1

R1
    REMAINS_CURRENT

R2 / R3 / PUBLIC BENCHMARK PRODUCT
    NOT_STARTED BY THIS PLAN
```

用户已经授权：R1 终态资格链闭合后，不再重新讨论“要不要做这轮外部错题本攻击”，而是直接从当时的
exact main 返回 CONTROL LOOP，确认没有更早反例后执行本计划的第一阶段。该长期授权不替代届时的 exact-coordinate
绑定、阶段合同、原始门禁、protected merge、installed-product readback 或任何不可逆动作所需的独立资格。

## 2. 这轮工作真正要验证什么

外部案例的价值不在于统计 R1 “发现了多少大厂 Bug”，而在于用公开事故、工具限制、研究反例与工程错题攻击
R1 已经取得资格的声明边界。

核心问题不是：

> R1 的输出是否与一份 expected output 相同？

而是：

> 这份案例有没有资格裁决指定 claim？expected obligation universe 如何取得资格？Oracle 是否沿用了被测实现的
> 关键错误因果链？R1 的实际结果又是否在同一冻结世界中完整履行了这些义务？

因此本 Benchmark 至少拆成三层责任：

```text
Case qualification
    -> 案例 X 对 claim K 到底有资格证明什么？

Independent oracle construction
    -> expected obligations / terminal states 从哪里来？
    -> 与 DUT 共享了哪些代码、规则、数据与可信假设？

DUT reconciliation
    -> R1 actual 与 qualified oracle 是否完整、双向、逐项一致？
```

三层任何一层未闭合，都不能把结果写成 R1 `BREACH` 或 `PASS`。

## 3. Case qualification 必须绑定具体 claim

对每个外部案例 `X` 与待审主张 `K`，先构造：

\[
\operatorname{QualifyCase}(X,K)
\]

Case record 至少保存：

1. exact source identity、版本、日期、许可与可复核原文；
2. 案例直接支持的事实，以及不能支持的外推；
3. 待审 claim `K` 的精确语义与 authority owner；
4. 从案例到 R1 obligation 的翻译规则；
5. ground truth、人工标注、第三方事实与仍未证明假设的边界；
6. 预先声明的 falsifiers、失效条件和预期分类；
7. case、Oracle、DUT、harness 与环境失败的分层身份。

公开案例存在、来自大型厂商或曾造成真实事故，都不自动使它成为 R1 的合格试题。案例只能在它实际拥有证据的
claim domain 内取得资格。

## 4. Oracle independence 是 claim-specific 的

冻结只能证明标准没有被事后改写，不能证明标准起初正确。以下世界必须被显式攻击：

```text
真实合同要求 17 个 obligations

R1 obligation projector
    -> 漏掉 #17

Benchmark Oracle 复用同一 projector
    -> 同样漏掉 #17

expected == actual
    -> 形式一致，但共同错误
```

因此：

\[
\operatorname{Agreement}\neq\operatorname{Correctness}
\]

“外部 Oracle”不以文件、进程、仓库或团队边界定义，而以关键 claim 的因果独立性定义。验证“应当存在 17 个
obligations”时，expected universe 不能只调用 DUT 自己的 obligation projector、denominator constructor 或等价实现。

不要求 Oracle 与 DUT 完全不共享任何东西。每个 case 必须公开一张 independence map：

```text
claim K
    -> independent evidence roots
    -> shared trusted roots
    -> shared code / normalization / projection paths
    -> common-mode failure surface
    -> unresolved assumptions
```

共享本身不是失败；未公开共享关键错误路径，却宣称 independent verification，才是不合格。

Oracle construction 可以组合冻结合同的独立枚举、不同实现、mutation falsifiers、第三方事实与必要的人工 ground
truth。任何来源都只承担其明确 claim，不产生万能裁判。

## 5. Oracle 与 Benchmark 自身的 falsifiers

Benchmark harness 必须先证明“这张卷子没有少题”，再允许裁决 DUT。首批至少包含：

```text
OBLIGATION_OMISSION
    故意漏掉一个 required obligation

OBLIGATION_DUPLICATION
    故意重复一个 obligation

CROSS_SUBJECT_CONTAMINATION
    把另一路径、产品或 attempt 的 item 混入 expected universe

DUT_PROJECTOR_REUSE
    用被测 projector 同时生成 expected 与 actual

SHARED_NORMALIZATION_DEFECT
    Oracle 与 DUT 共享同一 normalization / identity bug

REQUIRED_EVIDENCE_REMOVAL
    删除一个 Oracle qualification 所依赖的证据根

UNKNOWN_TO_COMPLETE
    把未知、缺证据或 Oracle 未资格化偷换成 COMPLETE

DENOMINATOR_SHRINKAGE
    根据 DUT 能表达或实际产生的结果缩小 expected universe
```

这些 falsifiers 检验 Oracle 与测试协议，不计作 R1 缺陷。测试环境、case qualification 或 Oracle 证据不足时，结果必须
停在各自层，例如 `CASE_UNQUALIFIED`、`ORACLE_UNQUALIFIED`、`HARNESS_ERROR` 或 `UNKNOWN`；不得误报为 R1
`BREACH`。

这些名称目前只是计划中的概念标签，不是 public Schema 枚举。

## 6. 优先可靠性，不要求万能完备性

本计划优先保证 soundness：

\[
V_W(A,C,B,\pi)=\operatorname{ACCEPT}
\Rightarrow
\operatorname{Qualified}_W(A,C,B)
\]

不要求所有实际合法的路径都能被现有验证器接受：

\[
\operatorname{Qualified}_W(A,C,B)
\not\Rightarrow
\exists\pi:V_W(A,C,B,\pi)=\operatorname{ACCEPT}
\]

`UNKNOWN` 可以是正确地拒绝虚假确定性。测试过的候选全部失败，只能证明已测试集合内没有合格构造；除非对合同
明确限定的完整候选空间给出机械不可满足性证明，否则不能宣称 `UNSAT / NO_CONSTRUCTION_EXISTS`。

这里的可复用元规则是：

> Local validity does not compose by default; composition itself carries proof obligations.

节点 A 与 B 各自取得资格，不证明边 `A -> B` 存在。候选转移 `C`、它的合同版本、冻结世界 `W` 与证明 `π` 必须
作为独立对象受审。

## 7. 不用代理指标冒充目标

外部 Benchmark 不以 PASS 数、发现数、UNKNOWN 数、分组数或一致率作为最终成功定义：

```text
PASS count          != correctness
UNKNOWN count       != epistemic quality
expected == actual  != oracle correctness
local validity      != compositional validity
```

统一纪律是：

\[
\operatorname{ProxySuccess}\not\Rightarrow\operatorname{GoalSuccess}
\]

除非 `Proxy -> Goal` 这条边拥有自己的证据与适用范围。

## 8. Attention 相关知识作为非线性关系保存

本计划只保存 R1 研究对后续 R3 的约束，不启动 Attention 实现。Attention 不应被建模成从分组到省工的线性资格链，
而应保留几条正交证明轴：

```text
Qualified Residual Obligations
        |
        +-- Cause relation
        |     为什么这些 obligation 没闭合？
        |
        +-- Action relation
        |     什么干预可能推动哪些 obligation？
        |
        +-- Intervention observation
        |     动作执行后，哪些 obligation 状态实际变化？
        |
        +-- Human-work evaluation
              相对基线，人工成本真的下降了吗？
```

每个 residual obligation 的 identity、terminal state、blocker、provenance 与 authority 必须保持。分组必须能够无损展开
原始 obligation universe；一个 obligation 可以同时属于多个 cause/action relation，不能强迫它们形成 partition。

更一般地，分别保存两张 incidence relation：

\[
R_{UC}\subseteq U\times C
\]

\[
R_{UA}\subseteq U\times A
\]

`R_UC`记录 residual obligation 与 cause claim 的关系，`R_UA`记录 residual obligation 与 action claim 的关系。二者
必须分别保存证据、资格与 UNKNOWN；不能从一张关系图机械生成另一张关系图。

两条关键反例必须保留：

\[
\operatorname{CommonCause}\not\Rightarrow\operatorname{SharedResolution}
\]

\[
\operatorname{SharedResolution}\not\Rightarrow\operatorname{CommonCause}
\]

共同原因是因果主张；共享动作是干预主张。相同 error string、同类证据缺口或同一个展示 cluster 都不能让二者互相
继承 authority。

即使一个动作实际闭合了 63 个 obligations，也只证明该动作在该世界中的 intervention effectiveness。它不证明 Attention
比基线节省人工。任何 human-work reduction claim 都必须有可比较的 baseline，并分别记录 review time、context switches、
duplicate inspections、manual evidence gathering、independent decisions、miss/error rate 与 rework cost；不同指标发生冲突时
不得压成一个未经授权的总分。

\[
\operatorname{InterventionEffectiveness}\not\Rightarrow\operatorname{AttentionEfficiency}
\]

因此：

\[
\boxed{
\text{Truth Validity}
\not\Rightarrow\text{Representation Validity}
\not\Rightarrow\text{Causal Validity}
\not\Rightarrow\text{Intervention Effectiveness}
\not\Rightarrow\text{Utility Improvement}
}
\]

每一条箭头都有独立 proof obligation。Attention 可以 cluster、rank、提出 cause/action hypotheses；不能自动宣称共同根因、
动作有效或人工成本已经下降。

## 9. 对 R2–R6 的方法约束

R1 的困难给后续阶段留下的不是一份固定功能流水线，而是一条统一资格原则：

\[
\operatorname{Qualified}(A)\land\operatorname{Qualified}(B)
\not\Rightarrow
\operatorname{Qualified}(A\rightarrow B)
\]

每个新阶段都必须说明它消费什么上游证据、保持哪些 identity 与不变量、由谁拥有 claim、履行哪些 obligations、如何
处理 negative worlds，以及结论最多取得什么资格。R2–R6 逐步扩展的是可取得资格的 claim domain，不是让下游位置自动
继承更高真实性。

统一的是 qualification discipline，不是所有领域共用一种 verifier：

| Claim domain | 主要证明方法 | 不能偷换成 |
| --- | --- | --- |
| 结构事实与完整性 | 冻结输入、机械枚举、双向核账与 falsifier | 因果结论 |
| 因果关系 | 识别假设、独立证据与替代解释排除 | 相同错误字符串或展示分组 |
| 干预效果 | 受控动作与执行前后 observation | 共同根因或预测性建议 |
| 人工效益 | 可比较 baseline、工作量与质量的经验测量 | obligation closure 或系统自报省时 |

因此本计划不创建一个能够裁决事实、因果、干预与效益的超级验证器。它只要求：每条跨层箭头形成有界、可检验的
claim；证据不足时保留 UNKNOWN；新反例只重开被击穿的最小边界。

研究可以没有预先知道的终点，但每个版本已经发布的确定性主张必须有封闭的证明责任。

## 10. R1 结束后的执行顺序

启动条件：R1 的终态合同、private proof、public state 与该层声明的最后资格门全部闭合；当时 exact main 没有尚未归层的
R1 反例；fresh CONTROL LOOP 仍确认本计划是最小合法下一问题。

满足条件后，不再进行一轮泛化的“是否值得做”讨论，直接依次执行：

1. **外部材料清单**：枚举公开事故、工具限制、论文、规范与工程错题；只记录 exact source，不先写 expected。
2. **claim inventory**：为每个案例列出候选 claim `K`，区分事实、关系、转移、完整性与效益主张。
3. **case qualification**：确定每个案例能证明什么、不能证明什么，以及其 ground-truth owner。
4. **Oracle independence audit**：绘制 independence map，暴露共享 projector、denominator、normalization 与可信根。
5. **Oracle falsifier suite**：先攻击卷子本身；未通过不得运行 DUT 裁决。
6. **bounded DUT run**：在冻结 world 中执行 R1，保存完整 obligation universe、negative worlds 与 attempt identity。
7. **independent reconciliation**：双向核账 expected/actual，区分 DUT、Oracle、case、harness 与环境结果。
8. **counterexample feedback**：真实反例只重开被击穿的最小 R1 边界；原资格历史保持，不用后继 PASS 洗掉。
9. **result publication**：发布 claim-specific 结论、共享假设、未决 UNKNOWN 与可复核 artifacts，不发布“全仓正确率”。

第一批执行不得同时启动 R2/R3，也不得用 Attention 分组改变 R1 truth。R1 Benchmark 先回答结构事实、义务、转移与完整性
边界；因果、干预与人工效益另行取得 authority。

## 11. 停止线

本计划不预先冻结具体厂商清单、案例数量、Oracle Schema、公共 Benchmark 格式、评分公式、排行榜、R2 Evidence carrier、
R3 Attention model、人工实验设计或发布产品。

执行期间出现以下任一条件必须停止并归层：

- case 无法对 claim 取得资格；
- Oracle 的关键义务推导只能复用 DUT 被审路径，且没有独立 falsifier；
- expected universe 的完整性无法证明；
- DUT 与 Oracle 使用了不同 world、Policy、Profile、attempt 或 subject identity；
- harness 自身失败，却试图输出 DUT `BREACH`；
- 为提高分数而缩小 denominator、丢弃 UNKNOWN 或重分类 negative world；
- Attention/效益主张被顺手带入 R1 Benchmark；
- 新反例击穿当前 frozen R1 claim 的前提。

这份计划保存的是方法与未来启动条件，不保存未来事实。R1 结束时仍必须从 exact main 和保留证据重建坐标；计划顺序不能
替代 CONTROL LOOP。
