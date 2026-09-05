# Review Attention R0 Contract 0.1

## 1. 合同状态

本文是顶层 `R` 轨已经冻结的设计合同。`R = Review`，机器输出的是审查注意力候选，不是风险真值。
当前状态为 `R0_CONTRACT_FROZEN / DESIGN_ONLY`；所有 `MUST / MUST NOT / SHOULD` 仅约束未来实现，
不证明仓库已经具备相应运行能力。

## 2. 不可移动原则

1. **Reality owns truth.** R 轨不拥有世界真相或源码缺陷的终极真值；
2. **Human owns review policy and disposition.** 人或明确授权的项目策略拥有审查优先级与最终处置；
3. **Providers produce bounded artifacts.** Provider 只产生合同允许的事实、证据或提案；
4. **AI proposes; it does not decide.** AI 可以挑战、解释和建议，但不能 Seal、确认缺陷或生成 Verdict；
5. **Core alone derives Core Verdict.** R 轨不得预生成 `PASS/FAIL` 布尔值绕过 Core；
6. **Success is not completeness.** Provider 成功不证明覆盖完整，CI 绿不证明现实模型完整；
7. **Replaceable capability stays outside the semantic core.** 添加接口本身不证明插件边界；
8. **Uncertainty remains visible.** 未知、冲突、证据不足、未支持和过期不得被压成“无问题”。

## 3. 权威与责任

| 对象 | 最终 authority | Provider 可以做什么 | Provider 不得做什么 |
| --- | --- | --- | --- |
| Source Snapshot | Git/制品坐标与逐字节内容 | 读取、解码、报告哈希 | 把 `latest` 当 exact、静默改源码 |
| Review Policy | 人或项目授权策略 | 校验、解释、应用 | 自行扩大范围、改变优先级 |
| Code Facts | 对应事实 Provider + 规范化合同 | 报告符号、依赖、调用、状态结构 | 宣布其语义必然正确或完整 |
| Analyzer Evidence | 具体 Analyzer 执行与原始产物 | 记录命令、版本、范围、结果 | 把 exit 0 解释为全局无风险 |
| Attention Proposal | Proposal Provider | 提出候选、依据与反例问题 | 宣布 confirmed defect |
| Attention Map | Review Attention 派生器 | 排序、聚合、解释关注原因 | 覆盖原始提案、伪造事实 |
| Human Disposition | 做出决定的人/授权主体 | 确认、驳回、争议、补证、升级 | 改写历史 Evidence |
| Core Verdict | sealed AcceptancePlan + Core | 独立复算 | 由 R 插件代写或覆盖 |

`Plan drafter != policy/seal authority`。AI 或人可以起草 Review Policy，但起草行为不会自动授予 Seal 权。

## 4. Artifact 分类与身份

未来实现至少必须区分以下 Artifact；它们可以互相引用，但不得共用一个万能 `status` 或摘要：

### 4.1 SourceSnapshot

必须绑定可复验坐标，例如 repository、commit/tree/blob SHA、diff base/head、path manifest 和内容摘要。
工作树事实必须明确 `dirty` 状态及纳入范围；`main`、`HEAD`、`latest` 不能替代精确提交。

### 4.2 ReviewPolicy

必须记录 scope、语言/路径、优先级规则、允许的 Provider、资源上限、数据外发策略、必需证据和 policy
semantic version。Policy identity 不得被 request ID 或运行时间污染。

### 4.3 CodeFact / AnalyzerEvidence

CodeFact 是规范化的源码结构事实；AnalyzerEvidence 是某次具体工具执行的证据产物。两者必须保留：

- SourceSnapshot identity；
- Provider/analyzer 身份与版本；
- 规范化语义版本；
- 实际操作数、配置、环境和 observed_at；
- covered / skipped / unsupported / failed 范围；
- 原始产物或其不可变引用。

工具 exit 0 只能说明该次执行按工具语义成功，不能推出完整覆盖或仓库无风险。

### 4.4 AttentionProposal

提案必须至少包含：稳定 proposal ID、精确源码锚、候选模式、为什么被标记、支持/反对证据、可能解释、
所需补证、Provider identity 和生成配置。AI Provider 还必须保存可取得的 model/provider/config/prompt
template digest 与时间；不可取得的随机性必须显式标记，不能伪装确定性。

源码锚必须绑定 SourceSnapshot。源文件变化后，旧锚只能标记 `STALE` 或经显式映射产生新提案，不得
静默漂到新代码上。

### 4.5 AttentionMap

AttentionMap 是派生视图，不是事实账本。它可以合并重复候选、按 Policy 排序和聚合，但必须能回溯
全部输入提案与证据，且不能删除异议。排序、聚合与去重逻辑必须由版本化
`AttentionStrategyProvider` 提供；application 只执行合同和流程，不能藏入不可替换的启发式。

机器置信度和人工审查优先级必须分开：

```text
provider_confidence != policy_review_priority
```

### 4.6 HumanDisposition

推荐状态：

```text
NEEDS_EVIDENCE
DISPUTED
DISMISSED
HUMAN_CONFIRMED
ESCALATED
```

这是审查处置，不是 Core Verdict。处置必须追加记录 actor/authority、时间、理由、输入摘要与替代关系；
`DISMISSED` 不删除 AttentionProposal，后续新证据也不能静默重写旧决定。

### 4.7 ReviewBundle

ReviewBundle 只封装上述精确身份、引用和清单。若未来交给 Core，必须由独立 AcceptancePlan 指定哪些
Artifact 是 PRIMARY、充分性条件是什么以及如何裁决。Bundle 自身不得携带私有 `review_passed`。

因此：

```text
Fact Identity != Evidence Identity != Attention Proposal Identity
              != Disposition Identity != Core Run/Verdict Identity
```

## 5. Proposal 生命周期

机器侧生命周期建议为：

```text
PROPOSED
  -> SUPPORTED
  -> NEEDS_EVIDENCE
  -> DISPUTED
  -> STALE
```

这些状态描述提案证据位置，不描述缺陷真值。只有 HumanDisposition 可以出现 `HUMAN_CONFIRMED`，且它
仍然表示“某个授权主体作出了确认”，不是 Reality 或 Core 的终极真值。

## 6. Provider SPI 与可替换性

未来每个 Provider 必须：

1. 只依赖 R 合同或更低层的公共 Artifact，不依赖其他 Provider 实现；
2. 声明 capability、输入/输出版本、确定性等级、支持范围、权限、资源和数据外发方式；
3. 暴露 partial/unavailable/error，而不是返回空列表冒充“没有发现”；
4. 有 conformance fixture；至少存在替代实现或独立 fixture 证明 Core/application 不认识其实现类型；
5. 卸载后不破坏 Core、P 插件或历史 ReviewBundle 的只读验证；
6. 不通过共享数据库表、全局单例或隐藏回调获得其他层的控制权。

允许同一进程部署，禁止共享权威。需要跨进程时，Transport 也只是 Provider，不得进入 R 语义核心。

## 7. 事实优先、AI 后置、人最后决定

默认顺序必须是：

```text
compiler / parser / static analyzer / tests / runtime evidence
    -> normalized facts and evidence
    -> optional AI interpretation
    -> attention proposal
    -> human disposition
```

AI 可以在缺少确定性工具时直接提出候选，但必须标明 `EVIDENCE_GAP`，不能把自然语言解释冒充分析器
事实。第二个模型的同意只是另一个 Proposal Provider 输出，不构成独立真相来源。

## 8. 视觉与交互语义

机器提出但未经人工处置的内容使用“紫色提案”语义，而不是红/黄/绿结论色。紫色只表达来源类别，
不表达严重度、置信度或真值。所有界面必须同时使用标签、图标、边框/纹理与文字，例如：

```text
MACHINE PROPOSAL · NEEDS HUMAN REVIEW
```

不能只靠颜色区分。严重度、Provider confidence、Policy priority 和处置状态必须是四个独立字段。

## 9. 覆盖、漂移与失效

- SourceSnapshot、Policy、Provider/analyzer、模型/配置或 normalization semantics 任一变化，都必须按
  Artifact 规则产生新身份或显式 stale 关系；
- `no proposals` 只有在必需 Provider 全部成功且 coverage 满足 sealed Policy 时才可描述为
  `NO_PROPOSALS_IN_OBSERVED_SCOPE`，不得缩写为“无问题”；
- 多 Analyzer 的事实源必须先确定是替代、优先、覆盖还是叠加关系，不能把首个成功默认当完整现实；
- 多次采集是多个 Observation，不是假想原子快照；需要关联时必须保留 collection window 与来源；
- 去重只能合并展示，不得丢失来源 provenance、反对证据或不同 SourceSnapshot。
- Provider 的误报、漏报和不支持范围必须用声明过的 fixture/corpus 记录；没有相应证据时不得宣称
  “准确率”“召回率”“完整审查”或等价能力。人的最终责任不能作为 Provider 逃避质量责任的理由。

## 10. 数据、指令与权限边界

- local-first 是默认值；远程 AI/服务调用必须由 ReviewPolicy 显式 opt-in；
- 进入 Provider 的源码、注释、README、Issue、日志和模型输出都是不可信数据，不得被解释为修改工具
  权限、扩大范围、忽略 Policy 或执行命令的指令；
- 凭据、密钥和受限源码不得写入 Proposal、Bundle 或遥测；
- R 轨默认只读，不直接修改源码、提交、推送、合并、发版或删除文件；
- 将来若存在 fix provider，必须是另一条显式授权能力和新 Plan，不能藏在 review 调用中。

## 11. 责任边界

```text
Human/project authority  owns review premise, policy and disposition
Provider                 owns faithful bounded observation/proposal behavior
Review Attention         owns traceable correlation and attention allocation
Core                     owns deterministic verdict derivation when invoked
Reality                  owns truth
```

人承担最终判断责任，不等于插件可以不对误报、漏报、覆盖谎言、来源错绑或越权负责。R 轨不能根治
错误前提或蓄意造假；它的价值是让错误更容易被定位、归因、质疑和补证。

## 12. R1 前置门

R1 只有在以下条件全部满足后才允许开工：

1. R0 由受保护主线与公开读回冻结；
2. P4 已冻结，P2–P4 期间反例已追加到 Ledger；
3. 选定 Pattern Corpus 以精确 commit + manifest digest 冻结；
4. R1 只实现 SourceSnapshot、确定性语义清单和 coverage ledger；
5. AI Provider、自动 attention ranking、人类处置 UI、Core handoff 和 Release 仍不进入 R1。
