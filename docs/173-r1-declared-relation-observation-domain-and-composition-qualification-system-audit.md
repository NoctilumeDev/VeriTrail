# R1 Declared Relation Observation Domain / Composition Qualification 系统审计

> 状态（本文最后门全部成立后）：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@d54ee43170779f54ec88b9839ad80d48056aa033`，Git tree
> `ae91fd3ef62a7589c1a7d70d77dde9cd257fab83`
>
> 上游冻结事实：[R1 Relation Derivation 实现冻结发布](172-r1-relation-derivation-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改 Schema、corpus、
> identity vector、源码、测试、依赖、CI、Provider、parser、RelationSet、Slice、Coverage、publisher、
> Manifest、CLI、Workbench、Core、P/Q/D/Cu、tag 或 Release

## 1. 审计问题与停止线

Relation Derivation 第一刀已经证明：在 exact composed FactSet、relation-only `/0.2` operands、独立
ProviderRun、真实使用的 closed parser 与同一个 live `BudgetContext` 下，一个 bounded Relation source 可以
诚实终态并交付 private canonical candidates。失败、不可用、中断、upstream hold 与成功空集保持不同；
private reported IDs 不会提前进入 final DerivationEvidence。

它没有证明：

```text
ProviderRun COMPLETED
  -> this source completed its bounded attempt

does not imply

all declared Relation observation obligations were discharged
  -> bounded observation domain qualified
  -> RelationSet eligible
```

本轮只问：

> 在任何 RelationSet admission 以前，哪一份 sealed authority 能说明 Relation source 的责任域、必需来源集合、
> observation subject 分母与 successful-empty 的边界，并使多个合法 candidate source 的 merge/conflict 不把
> “来源正常结束”升级成“本轮声明有义务观察的 Relation 已全部观察”？

本轮比较直接 RelationSet admission、完整 Relation algorithm/import resolution、multi-Provider Relation
composition、real parser/public Provider、conflict/UNKNOWN 扩展、Slice、Coverage 与 publisher。选择一个候选
只允许下一步从新 exact main 起草独立 docs-only 合同；不产生 Schema 或 runtime 实现授权。

## 2. exact main、并行状态与冻结输入

审计开始时，本地 `HEAD` 与 `origin/main` 都是
`d54ee43170779f54ec88b9839ad80d48056aa033`，worktree clean。远端只有 Dependabot PR #16、#137 与 #138；
没有并行 R1 feature PR。关键字节为：

```text
cdf948e44bd7d57b78bdaffbaf949af8df61d22d5ebe972c8864cbbf79fe32f0  docs/113-r1-deterministic-semantic-slice-contract.md
86b02ac5717190f7e12c720257ab6c46b996f427e048f19d1e631ad92b4bc8b3  docs/120-r1-schema-and-canonical-identity-contract.md
e70bdde807fcb1795bdca8e49d04c664024495b7e3f76ec4c696fc4ea48e8834  docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md
2da5ceca38fb94527ca12470fccbeef1512e7eb62d199d604379ed1cb1c51fd5  docs/165-r1-relation-derivation-authority-and-operand-continuity-contract.md
396d6bbca82b8b04f108c73d684e01b7fc66413aad5eb1cdc5435aed8543c533  docs/172-r1-relation-derivation-freeze-publication.md
cd2995c30ce2529ae60a2673c366411d91cb08e0753a6a19a89f74cca6159dce  schemas/review-derivation-profile-0.1.schema.json
397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744  schemas/review-relation-set-0.1.schema.json
a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045  schemas/review-derivation-evidence-0.1.1.schema.json
fdaf5d9da2d57310c12f927e7d44984e670dd287c3c5abdc332ee2691f7594aa  plugins/review-attention/src/veritrail_review/_relation_derivation.py
079689d49785b9bb0351bcadae959400586f130bb25267d00dac857d42b52835  plugins/review-attention/src/veritrail_review/_relation_derivation_values.py
efb6526b03f84357ee8cdc373ba2eb7b711d12e951fd66790415b84de6640346  plugins/review-attention/src/veritrail_review/_relation_closed_provider.py
49ef448c6d095d7b417e62b5095263a621ac59f5d02d2d961165cf4ad3fddde8  plugins/review-attention/src/veritrail_review/_relation_execution_cell_application.py
36f0216bf21d6b5fc771bd9d62ae536da0c67a2255493d89195da8c43951ca40  plugins/review-attention/tests/test_relation_derivation.py
```

本文不把聊天总结、完整 fixture、Schema shape 或历史绿色结果当成当前 runtime authority。

## 3. 当前四种语义没有闭合成一个结论

### 3.1 Provider terminal 只拥有一次 bounded attempt

`ProviderRun.execution_status=COMPLETED` 表示该 run 在 exact operands 上正常结束，包括成功空输出。当前
Relation phase 还证明 run-local candidate/report 双向闭包、真实 provenance 与 residue-free release。

它不拥有以下判断：

- 其他 required Relation source 是否存在或已运行；
- 该 Provider 覆盖哪些 `relation_kinds`、source Facts 或 relation subject slots；
- 未报告的 relation 是不存在、超出责任域，还是从未观察；
- 当前输出是否足以形成 normal RelationSet。

### 3.2 ReviewPolicy 规定 capability requiredness，不规定 Relation 覆盖域

冻结 Policy 0.1 规定 `provider_requirements[]` 的 `capability_id / required / CUMULATIVE`。所有适用且 required
来源都必须观察；一个来源成功或空输出不能取消其他来源。Relation 第一刀又将 exact
`review-relation-derivation` requirement 固定为 required，并把一个 exact closed descriptor 绑定到 Relation stage。

但当前 Policy、descriptor 与 relation-only request 都没有声明：

```text
supported/required relation kinds
eligible source Fact kinds
candidate subject denominator or digest
source-local coverage claim
```

因此“全部 sealed required bindings terminal”可以机械成立，而“本轮 declared observation obligations 已全部
履行”仍无冻结推导路径。

### 3.3 DerivationProfile 列出语义闭集与 rank，不分配 producer 责任

Profile 0.1 固定：

```text
relation_kinds = [LEXICAL_CONTAINS, IMPORT_TARGET_LITERAL]
```

该数组冻结可表达的 Relation 语义与规范顺序。它没有字段把某个 kind、Fact 区域或 candidate subject 分配给
某个 capability/provider，也没有声明数组中的 kind 是“允许表达”还是“每次派生都已被完整观察”的证明。
把 `relation_kinds` 直接当 required-source map 会给 Profile 新增未冻结 authority。

### 3.4 RelationSet shape 能装内容，不能证明观测责任域资格

RelationSet 0.1 能表达 Relations、same-ID provenance union 与 RelationConflict；其 digest 绑定 exact FactSet。
DerivationEvidence 0.1.1 能表达 Relation ProviderRun 与 `reported_relation_ids`。两者都没有独立字段记录
observation subject denominator、source responsibility 或 observation-domain qualification receipt。

所以：

```text
schema-valid RelationSet
!= all declared Relation observation obligations completed
!= qualified bounded Relation view
```

Coverage 以后可以诚实消费上游 KNOWN/UNKNOWN，但不能倒过来替 Relation producer 发明遗漏的分母。

## 4. exact-main 本地反例

### 4.1 已观察反例：COMPLETED 仍只覆盖一个 Relation family

审计只读调用当前 `test_relation_derivation.py` 已有 fixture/helper，没有修改源码或测试。输入 source 是
`import pkg.mod`，FactSet 包含 MODULE 与 IMPORT_DECLARATION，Profile 同时列出两个 Relation kinds。结果为：

```json
{"candidate_count":1,"candidate_relation_kinds":["LEXICAL_CONTAINS"],"fact_stage_status":"COMPLETED","final_phase_status":"COMPLETED","final_reported_relation_ids":[[],[],[]],"profile_relation_kinds":["LEXICAL_CONTAINS","IMPORT_TARGET_LITERAL"],"provider_execution_status":"COMPLETED","provider_reported_relation_ids":["4e42c7e39960bd9e247da522260afbcd36aa9df49e5d4ac5f9fad6d927df02d2"],"relation_start_status":"STARTED"}
```

该单行 UTF-8 bytes 的 SHA-256 是
`efac906d0c4fc2905dcbb63a26b7363f4bf031d79a99cea9d449d450ad402acf`。

当前 closed Provider 明确只为一个单名 `ast.Import` 生成 `LEXICAL_CONTAINS`；它不生成
`IMPORT_TARGET_LITERAL`，也不执行 import zero/one/many resolution。valid-complete fixture 对同型 source 则能
表达两类 Relation。由此只允许结论：

```text
the sealed closed source completed and reported one legal candidate
```

不得升级为：

```text
all Profile Relation families were observed
```

这不是 Relation Derivation 冻结事实失败。文档 165 已把首刀明确限制为 bounded private candidate proof，并把
完整 algorithm、declared observation domain、RelationSet admission 与 import resolution 留给后继。

### 4.2 F0 与五个必须由下一合同裁决的资格否定测试

| ID | 单变量反例 | 禁止的推理 |
| --- | --- | --- |
| `RO-000` | **已观察**：Provider `COMPLETED`，Profile 列两类 Relation，实际只报告一类 | Provider completion 等于 observation-domain completion |
| `RO-001` | Provider A `COMPLETED`；sealed required Provider B 未运行 | A 成功足以形成完整 bounded Relation view |
| `RO-002` | A `COMPLETED` 且空；B `UNAVAILABLE` | `relations=[]` 证明没有 Relation |
| `RO-003` | A/B 都 `COMPLETED`，但分别只覆盖不同 relation families，且没有冻结 responsibility map | 所有 runs terminal 自动证明 declared observation obligations 已履行 |
| `RO-004` | A/B 各自 candidate 合法，但同一 subject 内容不兼容 | candidate validity 足以直接 admission；可任选 winner |
| `RO-005` | Profile 只列 relation-kind 闭集；Provider descriptor 不声明覆盖域 | allowed semantic kind 等于 required observation 已满足 |

`RO-000..005` 不是要求现在实现两个 Provider、完整 import resolver 或新 Schema。它们只是阻止下一合同把四种
不同状态压成一个 `COMPLETED`。

## 5. 必须保持独立的六层身份

下一合同至少必须逐层回答，不得用同一个 boolean 或空数组代替：

```text
1. provider terminal
   该 exact run 是否真实结束

2. source-local output closure
   该 run 报告的 candidate 集是否完整、canonical、双向 provenance 闭合

3. required source-set terminal closure
   sealed applicability 下所有 required Relation sources 是否取得允许终态

4. declared observation-domain qualification
   对哪个 exact FactSet、relation families、operand subjects 与 source set，本轮观测义务是否闭合

5. RelationSet admission
   哪些 candidates/conflicts 获得稳定成员身份

6. final Evidence/publication
   哪些 admitted IDs 可以进入 final Evidence 与完整 Bundle
```

当前冻结实现完成第 1、2 层，并为第 3 层保留 exact applicability/terminal history；第 4 层尚无冻结语义。
因此第 5 层不能先行。

successful empty 也只能证明：

> 该 source 在 exact operands 与自己已冻结的责任域内没有报告 candidate。

在责任域和 required source-set 尚未闭合时，它不能证明“没有 Relation”。

## 6. 候选比较

| 候选 | 它能关闭什么 | 仍留下的共同 blocker | 结论 |
| --- | --- | --- | --- |
| **Declared Relation observation domain / composition qualification** | source responsibility、applicability、required observation、empty 边界、omission accounting 与 multi-source merge/conflict | RelationSet admission 仍是后继，但不再替上游猜是否看够 | **下一问题面** |
| 直接 RelationSet admission / final Evidence projection | 稳定成员与 reported-ID 闭包 | 必须自行猜 Provider completion 是否等于 observation-domain completion | 延期 |
| 完整 Relation algorithm / import resolution | 能产生更多真实 candidates | 多来源 requiredness、遗漏与 conflict qualification 仍未解决 | 过大且不能独立解锁 |
| 只做 multi-Provider Relation composition | same-ID union 与 conflict 可执行 | 若来源责任域未封存，全部 Provider terminal 仍不证明看够 | 被下一问题面包含但不能单独胜出 |
| real parser / public Provider SPI | 真实输入与生态入口 | 增加来源不会建立责任域、分母或 admission authority | 正交延期 |
| optional gap / conflict-bearing FactSet 扩展 | 允许更多上游状态继续 | 正常无 gap 路径仍缺 observation-domain qualification | 延期 |
| ReviewSliceSet | 消费稳定图并执行遍历 | 没有合格 Relation view | 过早 |
| CoverageLedger | 保存 denominator 与 typed gaps | 只能消费上游 truth，不能补造 observation obligations | 过早 |
| DIAGNOSTIC/COMPLETE publisher | 文件与 Manifest 原子发布 | 所有上游 Artifact authority 尚未闭合 | 过早 |

这个选择不是因为它在架构图上排在 RelationSet 前，而是因为 RelationSet、Slice、Coverage 与 final Evidence
都必须消费它；若跳过，每个后继都会各自发明一次“看够了”的定义。

## 7. 下一合同必须决定、但本文不替它决定的事项

下一份 docs-only 最小合同至少要裁决：

1. **Observation responsibility**：谁在执行前封存 Relation source 对哪些 families / operand subjects 的观测责任，
   谁只能报告 run-local facts；
2. **Applicability**：responsibility 怎样绑定 exact capability/provider implementation、FactSet、Profile relation
   kinds 与 operand subject domain，避免 ambient registry 或 caller 临时补 source；
3. **Requiredness**：适用后怎样绑定 required/optional，`required + CUMULATIVE` 的 terminal join 怎样解释；
4. **Observation closure**：什么条件下可以说一个责任域观察完成，identity 怎样外部复算；
5. **Empty semantics**：successful non-empty/empty、not-started、unavailable、failed 与 interrupted 怎样保持不同；
6. **Omission accounting**：required provider/family 未观察和 optional source gap 必须显式保留什么状态；
7. **Composition qualification**：multiple sources 的 same-ID provenance union、same-subject incompatibility、
   deterministic ordering 与全部 sealed responsibilities 闭合后，何时才形成有边界 Relation view；
8. qualification 失败时哪些 private candidates/ProviderRuns 可保留为历史，哪些绝不能进入 normal RelationSet；
9. 当前 Schema 是否足以诚实承载后继，还是必须增加最小版本化 receipt/field；shape 不能替代该论证；
10. RelationSet admission 是否能与 qualification 在同一最小合同闭环，还是必须继续独立；最小反例而非路线图决定；
11. 首个 closed proof 是单 source 还是 multi-source、覆盖哪些 relation families；不得用 fixture 方便性冒充完整
    Python Relation algorithm。

本文不预先选择“descriptor 声明 family”“独立 observation receipt”“Coverage denominator 前移”或其他具体
字段，也不锁死下一份合同标题。这些是后继合同候选要用 `RO-000..005` 比较的方案，不是审计事实。

## 8. 反证条件与最小重开规则

若后继发现以下任一事实，本审计选择必须重开：

| 反证 | 对本审计的影响 |
| --- | --- |
| 冻结字段已经无歧义绑定每个 Relation source 的 family/subject responsibility 与候选分母 | “qualification 尚缺”判断失效 |
| RelationSet 冻结语义明确允许无 qualifier 的任意 observed prefix，且所有消费者都必须独立 UNKNOWN | 需要重新评估 admission 是否可先行 |
| Slice/Coverage 存在不消费 RelationSet 或不依赖 declared observation domain 的合法冻结路径 | “共同 blocker”排序需重算 |
| 当前 closed Provider 已被另一冻结合同赋予并完成 Profile 两类 Relation 的全部观测责任 | 本地反例失效，需重新运行并保存新事实 |
| Relation qualification 无法在不完成 real parser/public Provider 的情况下做任何 closed proof | 下一合同必须收窄或改选问题面 |

新证据只重开被击穿的最小条款。不得因为发现 qualification 缝隙而改写文档 165/172 已冻结的 bounded
Relation Derivation 事实。

## 9. 外部 production case 的插入规则

本轮没有触发外部大厂 failure-shape survey。原因不是外部经验没有价值，而是 exact-main runtime、冻结 Profile
与 closed Provider 已经给出决定性本地反例；外部案例不能比本地事实更高权威，也不需要替本文选择问题面。

若下一合同在“怎样表达 source responsibility / observation denominator / omission receipt”之间仍缺真实失败经验，
才按 failure family 定向查公开一手材料：

```text
public production case
  -> candidate failure shape
  -> local RO falsifier
  -> reproducible local Evidence
  -> possible contract requirement
```

不按公司抄架构，不用公开案例直接产生 `R MUST implement X`。

## 10. README 状态漂移

审计发现 README 两处概览仍写 Relation Derivation“进入冻结候选”，而同一 README 当前状态表、AGENTS、
milestones 与文档 172 已写明最终 `FROZEN`。本轮只把两处旧措辞同步为 frozen，不改变任何产品事实、合同或
历史 Evidence。这是文档导航漂移，不是 Relation runtime 失败。

## 11. 本轮验证与生效条件

本文变更范围只允许：

```text
AGENTS.md
README.md
docs/milestones.md
docs/173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md
```

提交前必须通过 relative Markdown links、fence/heading、状态 marker、敏感/本机路径、exact scope、
`git diff --check` 与绑定当前 worktree 的适用 focused regression。它们只证明 docs-only 候选自洽，不替代：

```text
changed files
  = AGENTS.md
  + README.md
  + docs/milestones.md
  + this audit

relative Markdown links       = PASS (333 checked across changed files)
fence / heading / status      = PASS
sensitive / local-path scan   = PASS
exact diff scope              = PASS
git diff --check              = PASS

Schema + Evidence + Execution Cell + Fact/Evidence + Fact composition + Relation derivation
  Python 3.10 normal / -O -> 97 / 97, 97 / 97
  Python 3.13 normal / -O -> 97 / 97, 97 / 97
```

四个测试格都由 test module 的当前 `__file__` 坐标绑定本 worktree；另以两个解释器分别复核实际导入的
`veritrail_review._relation_derivation` 位于本 worktree plugin source。没有借用主工作树 editable install。

上述本地门之后仍必须完成：

1. docs-only PR 的原始 Public CI 完整通过；
2. PR 合入受保护 `main`；
3. 新 exact main 的 Public CI 与 Browser Smoke 通过；
4. 从新 exact main 对 README、本文与 milestones 完成 fresh anonymous installed-product readback；
5. 读回使用本审计专属 Evidence identity，不复用 Relation freeze 或其他 claim label。

最后门以前，当前分支只能写成：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_SYSTEM_AUDIT_CANDIDATE
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

## 12. Fresh-Agent 交接与当前停止线

本文最后门全部成立后，新的、没有聊天上下文的 Agent 应：

1. 读取 README、AGENTS 与文档 113、120、155、165、172、本文；
2. 从新的 exact main 建立独立 docs-only qualification contract worktree；
3. 先复跑/复核 `RO-000..005` 与第 8 节反证，不把本文选择当不可推翻路线图；
4. 区分 provider terminal、source-local closure、required source-set terminal、observation-domain qualification、
   RelationSet admission 与 final publication；
5. 只在本地模型仍不足以选择 responsibility/denominator 表达时，定向使用公开 production failure cases；
6. 合同未完成自己的候选门、受保护合入、exact-main 门、匿名读回与独立冻结发布以前，不写 runtime；
7. 不创建完整 import resolver、public Provider discovery、RelationSet、final Evidence、Slice、Coverage、publisher、
   CLI、Workbench、D、Cu 或 Q。

本文最后门全部成立后，当前状态才可写成：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本审计识别 declared Relation observation domain / composition qualification 为下一阻塞 seam，因为当前最大
风险不是“candidate 还没装进 RelationSet”，而是把一个 source 的正常结束误读成本轮声明的全部观测义务已经
履行。它没有授权任何
新实现，也没有宣称下一合同必须把 RelationSet admission、完整 Relation algorithm 或公共 Provider 一并收入。
