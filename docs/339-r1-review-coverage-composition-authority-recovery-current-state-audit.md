# R1 Review / Coverage composition authority recovery 当前状态审计

日期：2026-10-29

> 候选状态：`R1_REVIEW_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDIT_CANDIDATE`。
> 本文自己的完整资格链闭合以前，它不是 qualified history。
>
> 审计基线：`main@4baf57268f6a06e584a4396b6d4e7a9d24735744`；tree
> `388892cc80caa5b7f9d135f11c621c427b8f07f7`。
>
> 已冻结上游：[positive composition](314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)、
> [Fact → Coverage exact-input successor](330-r1-fact-to-coverage-exact-input-successor-private-implementation-freeze-publication.md)、
> [negative-world Coverage producer](338-r1-negative-world-coverage-authority-recovery-private-implementation-freeze-successor-publication.md)。
>
> 影响层级：`L0_DOCUMENTATION / READ_ONLY_CURRENT_STATE_AUDIT`。

## 1. 审计问题与停止线

本文只回答一个有限问题：冻结的正常正路径composition与冻结的negative-world Coverage producer能否在当前Fact runtime中由同一个
application route安全、完备地选择并消费。

答案是：两个局部实现都在各自applicability内成立，五个Fact terminal branch也形成total、disjoint partition；但current runtime没有
一个有资格消费这两个结果的共同application route。缺口早于manifest、Evidence或persistence，也早于简单的结果union。Fact consumer的
handoff domain在执行Fact之前已经固定，而正/负路径只能在Fact terminal branch产生后才可决定。

因此本文触发最小停止线：

```text
minimal gap  = VERSIONED_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY
next boundary = POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT
```

本文不创建该合同，不修改runtime，不恢复旧global composition authority，也不授权manifest、Evidence、persistence、public Review或R2–R6。

## 2. 已资格化的冻结输入

[文档338](338-r1-negative-world-coverage-authority-recovery-private-implementation-freeze-successor-publication.md)由PR #390以
`base=c816c3700c7a6bf1d612d737abf7f3567f5f0554`、`head=7f31acdd88ffa10e4e88746465149c8b3841f586`精确合入
`main@4baf57268f6a06e584a4396b6d4e7a9d24735744`，candidate/merge tree均为
`388892cc80caa5b7f9d135f11c621c427b8f07f7`。original Public CI `40775454879`、exact-main Public CI
`40779905310`与Browser Smoke `40779905322`均为attempt 1 SUCCESS，分别11/11、11/11、1/1。

fresh anonymous installed-product README/doc336/doc338/milestones 4/4取得唯一qualifying PASS。independent reconciliation、finite
closeout、finite integrity与保留的stdout self-capture mismatch的SHA-256分别为：

```text
e85dc7c7d85f3178e26ede72ac613037c7b277886efceaed1767c838bbfbe63d
d38212c2994e756a6a6c50633d9e91c1f1314e0ec3defbeab56dbe97e0c0fb23
ed759c7f7e91bd8e312d16ca3ae2a19b22f39052d7d95136f7789e7e813d85e9
bbcde590980961ee95f6e53e8dcc6e470342bacd505c20b9f66e855eb7b164eb
```

因此以下两个局部事实是本审计的冻结输入，而不是本文重新授予的authority：

- `NORMAL_FULFILLED`世界中的private Relation → Slice → Coverage composition已经frozen；
- 四类negative terminal branch中的private negative-world Coverage producer/validator/admission已经frozen。

## 3. 五分支路由事实

read-only audit从current exact bytes构造一个normal world和七个negative denominator worlds，并得到下列机械partition：

| Fact terminal branch | 唯一适用后继 | 结果类型 |
| --- | --- | --- |
| `NORMAL_FULFILLED` | positive Relation / Slice / Coverage | `OwnedReviewSliceCoverageComposition` |
| `ZERO_PARSE_DENOMINATOR` | negative Coverage | `AdmittedNegativeWorldCoverage` |
| `ALL_PARSE_REJECTED` | negative Coverage | `AdmittedNegativeWorldCoverage` |
| `PROJECTION_BLOCKED` | negative Coverage | `AdmittedNegativeWorldCoverage` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | negative Coverage | `AdmittedNegativeWorldCoverage` |

normal world保留同一original `DerivationInputSet`、`BudgetContext`与transition eligibility，Fact/Relation/ReviewSlice三个root均为
`ARTIFACT_PRESENT`；negative worlds只取得private negative-world Coverage ledger authority，Fact/Relation/ReviewSlice authority均为false，
对应root为`QUALIFIED_ABSENT`。两类结果都不产生manifest、Evidence、persistence、public Review或repository-truth authority。

partition本身是total且disjoint，但这只证明“终态以后应走哪条路径”，不证明“终态以前应构造哪种Fact consumer”。

## 4. pre-terminal domain 与 post-terminal branch 的矛盾

current Fact consumer在构造时固定handoff domain：

- `create_product_fact_consumer_for_relation_transition()`选择`RELATION_TRANSITION`，只允许`RELATION_HANDOFF`；
- legacy `create_product_fact_consumer()`选择`LEGACY`，允许`FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`，但没有Relation handoff
  authority。

Fact terminal branch只有在consumer执行、逐Provider履责并封闭terminal history之后才可得知。因此application若在执行前选择
`RELATION_TRANSITION`，negative branch无法取得exact-input successor；若执行前选择`LEGACY`，normal branch无法取得Relation handoff。

这不是一个可由“先试一条、失败再fallback”修复的接口问题。handoff claim共享one-shot consume state；错误route会撤销或消费authority，
后继fallback不能取得新的资格。

## 5. 三个破坏性wrong-route反例

audit显式执行三种错误路由：

1. relation-domain normal closure先请求negative exact-input handoff：请求正确fail closed；随后positive fallback也因authority已经烧毁而拒绝；
2. legacy-domain normal closure先取得exact-input carrier并送入negative producer：producer以`UNSUPPORTED_TERMINAL_BRANCH`拒绝；随后positive
   fallback没有Relation handoff authority；
3. relation-domain negative closure先请求positive transition：请求拒绝；随后negative fallback也无法取得exact-input handoff。

所以：

```text
Local positive validity  = true within NORMAL_FULFILLED
Local negative validity  = true within four negative branches
Trial routing safety     = false
Shared route admission   = absent
Global consumable authority = not established
```

source inventory同时确认，没有runtime module共同消费`OwnedReviewSliceCoverageComposition`与`AdmittedNegativeWorldCoverage`。仅仅新增
一个Python union type或展示层分组不会修复pre-terminal authority选择，也没有资格把两个局部结果升级为统一Review/Coverage结论。

## 6. Read-only audit、矩阵与保留的非成功

独立audit facility位于保留证据根，不进入产品包：

```text
C:\Users\lenovo\Desktop\GitHubProjects\tmp\review-coverage-composition-authority-recovery-audit-4baf572
```

final audit source SHA-256为：

```text
c0a6780d11520c0f69e4e21ed85b3c563265d816eb1dbe14d7c894ea8dce1eee
```

Python 3.10.6 / 3.13.13 × normal / `-O`的final attempt 4均成功，canonical stdout SHA-256一致：

```text
0e595b9145244f3ea53b5e728fabca48be411042d1491f42d359403cd559ffaa
```

focused witness四格各运行153项，均为152 passed / 1 skipped；它覆盖Ledger 0.3、Language、Fact fulfillment、0.1/0.2 handoff、
Fact → Relation、positive composition与negative producer。

以下先行观察必须保留，不被final PASS重写：

- attempt 1错误从closure顶层读取`branch`，四格以`KeyError: 'branch'`终结；这是proof-facility field-selection error；
- attempt 2在relation-domain normal closure上直接请求exact-input handoff并正确fail closed；它暴露真实domain反例，但该次facility未完成完整
  audit report，保持non-qualifying；
- attempt 3在四格尚运行时修改audit facility，三个已启动进程命中错误的eligibility proof target，一个后启动进程读取修正后bytes并成功；
  整组属于mixed working-byte scheduling error，不是qualifying matrix，也没有产品语义效果；
- attempt 4才把固定同一facility bytes用于四格并取得一致结果。

这些失败不修改产品oracle，不弱化handoff domain、one-shot、branch、assignment或admission断言。

## 7. 下一最小合同必须承担的责任

下一步只能建立docs-only、versioned `POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT`。该合同至少必须冻结：

1. successor在Fact执行前创建，但在terminal source通过完整重验以前不签发任何route claim；
2. `NORMAL_FULFILLED`只能签发Relation handoff；四个negative branch只能签发exact-input handoff；branch partition无遗漏、无重叠；
3. 两种claim共享一个consume slot，任何成功、失败、replay、wrong-route或copy-equal尝试都不能产生第二份authority；
4. 两条route都绑定original `DerivationInputSet`、live `BudgetContext`、sealed Policy/Profile、terminal history、attempt与source identity；
5. normal route继续满足positive path所需的完整Policy/applicability，不用缩小Fact universe制造兼容；
6. legacy与`RELATION_TRANSITION` consumer bytes和既有历史保持不变；新合同只定义可区分的private successor；
7. 合同本身不生成Coverage结果，不授予manifest、Evidence、persistence、public Review或全局composition authority；
8. falsifier至少覆盖wrong-route、先失败后fallback、replay、copy-equal、branch rewrite、denominator shrink、共享projector common-mode与
   两种claim各自成功后尝试第二次消费。

该合同与实现冻结以后，仍需在新的exact main重新审计application-level unified Review/Coverage output admission。共同输入、共同route与
共同输出qualification是不同proof obligation，不能由合同编号或下游位置自动继承。

## 8. 本candidate自己的资格链与状态上限

本docs-only candidate只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc314、doc330、doc338、positive/
negative runtime、tests、workflows与全部冻结历史必须保持base bytes。

完整资格链仍为：final-byte local gates、original PR、exact-head protected merge、新exact-main Public CI与Browser Smoke、fresh anonymous
installed-product README/本文/milestones readback、independent reconciliation与finite closeout。全部闭合后最多成为
`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`，随后必须返回CONTROL LOOP建立独立合同候选。

在此以前只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDIT_CANDIDATE
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文不把proxy success当成goal success：两个局部实现均通过，不等于组合箭头取得资格；五分支partition完备，也不等于pre-terminal
authority选择安全。当前正确结果是停止全局composition声明，并把未完成证明责任压缩到上述versioned dual-successor seam。
