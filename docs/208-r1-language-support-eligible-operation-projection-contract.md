# R1 Language Support eligible operation projection / same-attempt gate 最小合同 0.1

日期：2026-09-27

## 1. 文档身份与停止线

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_ALLOWED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 合同基线：`main@940b6fc9ad974c4e4afb4f6f3e2f635efe780e1c`，Git tree
> `5af79de7314a8f1c2447d3563b1905c0397eee63`
>
> 前置审计：[文档 207](207-r1-language-support-eligible-operation-projection-precontract-audit.md)
>
> 冻结发布：[文档 209](209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)
>
> 冻结上游：[Language Support 0.2 合同](202-r1-language-support-codec-conformance-correction-contract.md)、
> [private classifier 冻结发布](206-r1-language-support-private-classifier-implementation-freeze-publication.md)、
> [Fact execution-cell 合同](150-r1-derivation-execution-cell-terminal-envelope-contract.md)、
> [Relation derivation 合同](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)与
> [Relation observation / composition qualification 合同](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本轮不修改 runtime、tests、Schema、Profile、Policy、corpus、
> identity vector、Provider、parser、AST、Fact、Relation、Slice、Coverage、Evidence、Manifest、publisher、Bundle、
> CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文只冻结一条 private input-authority seam：

```text
exact frozen inputs
    -> r1-python-language-support/0.2 classification
    -> exact eligible subject upper bound
    -> cell-specific source operation projection
    -> same-attempt one-shot request claim
    -> Provider-visible source bodies
```

它回答“哪些 exact bytes 有资格进入这次 source-body operation，以及该资格是否仍属于原 live attempt”。它不运行
真实 parser，不定义 Parse terminal outcome，不证明 Fact/Relation/Coverage fulfillment，也不选择 classification
persistence。候选资格已经闭合；上述 frozen / allowed target 只有[文档 209](209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)
完成自己的同等级资格链后才生效，并且只授权本文第 14 节的有限 private implementation。

## 2. 合同结论

冻结语义为：

```text
Language Support classification
    owns deterministic eligibility semantics

source operation projection
    owns one request's exact source-body set

same-attempt gate
    owns whether that projection may enter one live child request

Provider
    consumes only the projected bodies
    owns neither eligibility nor projection
```

每个 source-body-carrying request 必须同时证明：

1. classification 来自 exact Snapshot / Policy / Profile 与冻结 `r1-python-language-support/0.2`；
2. Provider-visible source bodies **恰好等于**该 cell 的 canonical operation subject set；
3. operation subject set 是 exact eligible subject set 的子集；
4. projection、operands 与 ProviderRun identity 区分不同 function、classification、operation set 或 downstream
   semantic coordinate；
5. request claim 绑定原 `BudgetContext`、parent/child `AttemptEligibility` 与 one-shot prepared request；
6. stop、integrity failure、payload insufficiency 或重复 claim 发生时 fail closed。

因此：

```text
eligible upper bound
    != operation fulfillment

same projection bytes
    != same attempt authority

Provider terminal success
    != upstream input authority

empty operation set
    != Parse / Fact / Coverage CLOSED_EMPTY
```

## 3. 冻结输入与历史 identity 不改写

### 3.1 Language Support 0.2 是唯一 eligibility authority

本合同只消费已经冻结的 private classification：

```text
language_support_function = r1-python-language-support/0.2
classification domain     = veritrail.review.private-language-support-classification/0.2
subject domain            = veritrail.review.language-support-subject/0.2
```

分类由 exact copy-owned `DerivationInputSet` 复算；`ELIGIBLE` subject 的 `semantic_input.inventory_item` 给出 exact
Snapshot inventory identity，完整 subject identity 又绑定 IN_SCOPE Policy semantics、Profile support semantics 与 function
identity。Provider、parser tolerance、path suffix helper、caller path list 或 terminal output 均不能增删 eligible set。

### 3.2 三个旧 wire 与三个旧 operands domain 永久只读

以下 identity 已经冻结，继续只解释历史 bytes：

| source-body cell | 历史 request/terminal protocol | 历史 operands domain |
| --- | --- | --- |
| Fact derivation | `veritrail-review-derivation-cell/0.1` | `veritrail.review.provider-operands/0.1` |
| Relation derivation | `veritrail-review-relation-cell/0.1` | `veritrail.review.provider-operands/0.2` |
| Relation observation | `veritrail-review-relation-cell/0.2` | `veritrail.review.provider-operands/0.3` |

它们都要求或实际携带全量 Snapshot BLOB bodies。不得在这些 identity 下改变 `source_blobs` cardinality、增加
classification/projection 字段、重算旧 operands、ProviderRun、terminal 或历史 vector。

### 3.3 本合同不修改 Language Support persistence 决策

classification 可以从 exact live inputs 复算，不等于 public/offline consumer 一定能重新取得 exact blob bytes；它也不
等于必须持久化一个新 Artifact。本合同只允许 attempt 内 private copy-owned classification/projection。Route A/B 继续
保持 `OPEN`。

## 4. Authority topology

| 对象 | owner | 明确不拥有 |
| --- | --- | --- |
| exact source bytes/history | qualified `DerivationInputSet` | mutable path、ambient checkout、digest 字符串 |
| eligible subject set | `r1-python-language-support/0.2` application | Provider、parser、caller |
| operation subject set | application 根据该 cell 的冻结 downstream coordinates 机械构造 | Provider 自选、输出反推 |
| live gate | controller-owned original `BudgetContext` + parent/child `AttemptEligibility` | classification digest、同 limits 新 context |
| request validation | trusted application worker | Provider self-report |
| bounded observation | Provider | eligibility、projection、admission、publication |

controller 负责在 Provider admission 以前复算/校验 classification、建立 projection、构造 filtered frame 并绑定 live
claim。application worker 负责重新验证 exact document/digest continuity、classification/projection shape、included-byte
continuity 与 set equality。Provider 只得到 operation bodies 的 owned copy，不能看到任何 omitted body，也不能通过
“没有使用某个 key”证明最小授权。

本合同约束的是 **source body authority**。Snapshot/Policy/Profile 的 frozen metadata 仍可作为 application request
validation 输入；本文不新增路径保密或 metadata confidentiality 声明。

## 5. Private Source Operation Projection 0.1

### 5.1 规范 projection

每个 child request 必须先形成一个 private canonical projection。identity domain 固定为：

```text
veritrail.review.private-source-operation-projection/0.1
```

规范 payload 固定包含：

```text
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
language_support_function
classification_digest
operation_coordinate
eligible_subject_ids[]
operation_subject_ids[]
```

`eligible_subject_ids[]` 必须恰好等于 classification 中全部 `ELIGIBLE` subject identities；
`operation_subject_ids[]` 必须是其子集。两数组都按 classification 的 exact raw Git path order 排列、唯一且无 caller
自由度。projection document 另含：

```text
source_operation_projection_digest
```

其值为上述 domain 对移除 self-digest 后完整 payload 的 `semantic_digest`。projection 是 private derived value，不是
Artifact、Evidence、receipt、Coverage denominator 或 persistence 选择。

### 5.2 operation coordinate

`operation_coordinate` 是 closed tagged object，固定包含：

```text
operation_kind
provider_descriptor
fact_set_digest
observation_domain_digest
assigned_observation_item_ids[]
```

不适用字段必须使用本合同规定的 exact `null` 或空数组，不能 missing 或由实现填默认值：

| `operation_kind` | `fact_set_digest` | `observation_domain_digest` | assigned IDs |
| --- | --- | --- | --- |
| `FACT_DERIVATION` | `null` | `null` | `[]` |
| `RELATION_DERIVATION` | exact digest | `null` | `[]` |
| `RELATION_OBSERVATION` | exact digest | exact digest | exact assigned IDs |

exact `provider_descriptor` 使相同 subject set 不能从一个 Provider request 移植成另一个 Provider 的 source authority；
FactSet、observation domain 与 assignment 又把后继 projection 绑定到本次 downstream obligation world。

### 5.3 request 必须携带可机械核账的 projection

新 wire request 必须携带：

```text
language_support_classification
source_operation_projection
source_blobs[]
```

前两项使用 private canonical documents；第三项只含 operation subjects 对应的 bodies。application worker 至少复算：

1. classification 与 exact Snapshot/Policy/Profile digests、function、subject identities、counts 和 self-digest 一致；
2. projection 的 eligible IDs 恰好等于 classification `ELIGIBLE` IDs；
3. operation IDs 是 canonical eligible subset，且与 operation coordinate 的 stage-specific derivation 结果完全一致；
4. `source_blobs[]` path/body set 恰好等于 operation IDs 映射的 inventory items；
5. 每个 included body 的 path、size、SHA-256、base64 与 Snapshot exact identity 一致；
6. operands digest 与新 projection digest 一致。

worker 不需要、也不得通过把 omitted raw bytes 再交给 Provider来重跑 classification。controller 是 trusted application
authority；worker 验证的是 versioned projection continuity，不把 Provider 变成 omission certifier。

## 6. 三类 canonical operation set

### 6.1 Fact derivation

Fact operation subjects 恰好等于全部 eligible subjects：

```text
FACT_DERIVATION operation_subject_ids
    = classification eligible_subject_ids
```

Fact Provider 不得收到 OUT_OF_SCOPE、`UNCLASSIFIED_SOURCE`、unsupported entry kind、non-Python path 或 unsupported
encoding 的 body。多个合法 Fact Provider 各有自己的 provider-bound projection 与 child claim；一个 Provider 的
projection 不能授权另一个 Provider。

### 6.2 Relation derivation

Relation derivation operation subjects由 exact FactSet 中全部 canonical Fact `source_anchor.git_path` 的唯一集合机械
导出；每个 path 必须映射到同一 classification 的一个 eligible subject。出现 dangling path、unsupported path、foreign
Snapshot、ambiguous mapping 或 noncanonical FactSet 时，projection construction 整体失败，不能缩小 set 继续。

```text
RELATION_DERIVATION operation paths
    = unique source paths referenced by exact FactSet
```

FactSet 没有引用的其他 eligible bodies 不进入该 Provider request。terminal/output filtering 不能补做这项收窄。

### 6.3 Relation observation

每个 observation Provider 的 operation subjects由其 exact `assigned_observation_item_ids[]` 所引用的 canonical Facts 的
source paths 唯一导出。assignment、FactSet 或 observation-domain drift 必须改变 projection 与 operands identity。

```text
RELATION_OBSERVATION operation paths
    = unique source paths required by that Provider's assigned items
```

另一个 Provider 的 assigned item、同 domain 中未分配给本 Provider 的 eligible source 或全量 Snapshot bodies 均不得
进入该 request。

### 6.4 exactly-equal，而不只是 subset

eligible set 是 universal upper bound；stage-specific operation set 是 exact request denominator。因此：

```text
Provider-visible bodies subset of eligible bodies
    is necessary

Provider-visible bodies exactly equal operation bodies
    is also required
```

只证明 subset 会允许 caller 静默漏掉本应操作的 eligible source，再用较小输入自证完成。operation set 的完整性必须由
application 从冻结 downstream coordinates 构造，Provider不能增删。

## 7. Same-attempt gate 与 one-shot claims

### 7.1 semantic value 与 live authority 分离

classification/projection 可以在相同 exact inputs 下逐字节相同，但二者都不携带 attempt authority。合法 gate 必须同时
绑定：

```text
exact DerivationInputSet object/history
original live BudgetContext object identity
parent AttemptEligibility object identity
exact classification identity
closed child request coordinate
child AttemptEligibility object identity
one prepared request frame
```

caller 提交 classification object、digest、path set、boolean、序列化 token 或 limits 相同的新 `BudgetContext` 都不能
构造/恢复 gate。

### 7.2 一个 parent 可以有多个 child claim，但每个 child 只能消费一次

Fact multi-provider 与后继 Relation cells 需要共享同一 live attempt。gate 因此不是“全局一次使用后销毁”的 token；它是
controller-owned parent state，按 closed child coordinate 产生有限、不可伪造的 claims。每个 claim：

1. 只绑定一个 exact projection、request frame 与 child eligibility；
2. 最多一个并发调用者成功 claim；
3. 不能换 descriptor、projection、frame 或 child eligibility 后复用；
4. 被 claim 后无论 validation/execution 成败都不可恢复；
5. parent/context stop 后所有未消费 claims 永久失效。

多个 child semantic projection 相同也不共享 claim。多个 attempts 得到同 projection bytes 也不共享 parent authority。

### 7.3 合法顺序

首版 correction 的最小顺序固定为：

```text
validate closed applicability and exact inputs
    -> create one original BudgetContext / provisional parent
    -> classify Language Support under that same deadline
    -> checkpoint cancellation/deadline/integrity
    -> construct exact child operation projections directly from owned inputs
    -> construct filtered request documents and frames
    -> bind distinct child eligibilities and one-shot claims
    -> final parent admission checkpoint
    -> admit parent
    -> each child rechecks parent/context, claims once, admits and runs
```

后继 Relation request只能在 FactSet/domain 成为同一 attempt 的合法 private result后构造；它继续消费原 context 与
parent，不重新发放 wall-clock/memory/artifact budget。构造 classification/projection、过滤 bytes 和编码 frame 的成本都
必须处于原 budget window 内。

## 8. Wire 与 operands version correction

### 8.1 新 wire identities

本合同为三种不同 request shape 分别冻结新 identity：

| cell | 新 request/terminal protocol |
| --- | --- |
| Fact derivation | `veritrail-review-derivation-cell/0.2` |
| Relation derivation | `veritrail-review-relation-cell/0.3` |
| Relation observation | `veritrail-review-relation-cell/0.4` |

Relation `/0.2` 已属于冻结 observation wire，因此 Relation derivation 不能占用或重解释它。新 terminal 继续执行各自
既有 terminal semantics，但必须 echo exact 新 protocol 与新 operands/run identity；旧 protocol validator不得接受新
shape，新 validator也不得把旧全量-body request 升格为 eligible-only。

### 8.2 新 operands identities

新 operands domains 分别固定为：

```text
Fact derivation       veritrail.review.provider-operands/0.4
Relation derivation   veritrail.review.provider-operands/0.5
Relation observation  veritrail.review.provider-operands/0.6
```

每个 payload 是对应历史 payload 的完整字段，加：

```text
language_support_function
classification_digest
source_operation_projection_digest
```

因此 `/0.4` 继承历史 Fact `/0.1` payload，`/0.5` 继承历史 Relation `/0.2` payload，`/0.6` 继承历史 observation
`/0.3` payload。不能把不同历史 payload 压成一个带 optional fields 的开放结构。

`provider_run_id` 继续使用冻结的 `veritrail.review.provider-run/0.1` 公式；新 operands digest 已使不同
classification/projection world 产生不同 run identity，不需要改写公共 ProviderRun shape。现有 Schema 的 digest string
capacity 不等于本合同已经授权 public Evidence；它只说明无需为 private identity correction 提前升级 Schema。

### 8.3 先投影，再编码

controller 必须从 owned exact bytes 直接构造 filtered `source_blobs[]`，再编码 request frame。禁止：

```text
build full all-blob frame
    -> exceed payload/budget
    -> filter afterward
```

request safety cap 判断的是最终 qualified frame，但构造/哈希/过滤过程仍受原 shared budget。terminal output 不得改变
projection或 retroactively authorize omitted/included bytes。

## 9. Empty worlds 与 terminal 强度

至少保持三类空 world 可区分：

```text
A. Language Support denominator empty
B. denominator non-empty, eligible set empty
C. eligible set non-empty, later cell operation set empty
```

A/B 由完整 classification document 区分；C 由 non-empty eligible IDs 与 stage-specific empty operation IDs 区分。三者
不得共享 projection identity。

empty operation projection 是合法 private input shape，request `source_blobs[]` 必须恰为空。本合同不改变既有
applicability 或 requiredness：凡冻结 downstream execution plan 已判定 applicable、且在没有 Language Support gate 时
本应启动的 child，仍必须在原 attempt 内真实启动、terminal、release；区别只在它收到 exact empty-body request。不得因
operation set 为空把 applicable child 改写成 NOT_STARTED，也不得为避免真实 empty terminal 临场缩小 binding set。

因此首个 closed profile 的唯一行为是：

```text
Fact applicable child + empty Fact operation set
    -> run exact empty-body Fact request

Relation derivation child + legal empty FactSet-derived operation set
    -> run exact empty-body Relation request

Relation observation A/B + empty declared domain/assignment
    -> A and B each run, terminal and release against its own empty projection
```

stop、deadline、cancellation 或 integrity failure 仍可阻止尚未启动的 child；那是 typed non-success history，不是合法
empty-world 调度选择。

本文只冻结共同边界：

- 不能启动携带 unsupported/OUT_OF_SCOPE bodies 的 child；
- empty Provider terminal 只证明该 cell 的真实 terminal；后继 FactSet/Relation qualification 仍只能按各自冻结合同决定，
  且不证明 Parse/Coverage completion；
- A/B/C 不能因最终都没有 bodies 而被压成同一 history；
- 不得把 A/B 自动发布成 `CLOSED_EMPTY`、known-empty Coverage 或 complete Fact universe。

后继 implementation若发现既有 downstream contracts 没有唯一决定 empty-child 是否启动，必须停回合同；不得任选更方便的
行为。

## 10. Failure、stop 与 revocation

| 边界 | 最小结果 |
| --- | --- |
| exact input/classification integrity失败 | pre-child fail closed；无 ProviderRun |
| projection denominator/subset/equality失败 | pre-child fail closed；无该 child ProviderRun |
| protocol/operands/frame不一致 | admission integrity failure；旧/new identity 不互相 fallback |
| final qualified frame超过 payload cap | transport insufficiency；不发送 partial frame |
| classification/projection后 deadline/cancel/parent revoke | 全部未消费 claim revoked；已编码 frame 不再有效 |
| concurrent/double claim | one winner；其余拒绝且不能 mint replacement |
| Provider 收到 request 后 terminal失败 | 保留真实 admitted child history；不能回退成“未开始” |
| release/shared-context failure | 撤销后继 claims；不拼接另一个 attempt 的成功结果 |
| 无法安全归因的 application invariant failure | 使用既有 integrity boundary；不伪造具体 Provider reason |

classification/projection失败不是 unsupported disposition；不能把 integrity failure 伪装为“所有 subject 不支持”。child
output被 FactSet/Relation reconciliation 拒绝也不能倒写 input exposure 没有发生。

## 11. Scope closure

首个 implementation scope 必须覆盖 exact main 上全部三类 source-body-carrying child builders、validators 与 Provider
copies：

```text
Fact execution cell
Relation derivation cell
Relation observation cell
```

只修第一条 Fact request 不成立。每条链都必须证明：

```text
no ambient checkout/path reread
no full Snapshot body side channel
no application document copy retaining omitted bodies
no Provider copy exceeding operation set
no terminal/output filter substituting input gate
```

未来新增 source-body-carrying child protocol 时，必须显式消费本合同或形成版本化等强 correction；“使用同一
DerivationInputSet”不自动建立 projection authority。三个实现可以共享 lower-level helper，但 helper 不能成为新的
authority owner，也不能把各 stage 的 operation denominator 合并。

## 12. 必须拒绝的 falsifiers

| ID | world | 必须拒绝的错误推理 |
| --- | --- | --- |
| `LSPC-000` | mixed eligible/unsupported；Fact old cell 可在 rejected path 完成 | terminal success证明 input authorized |
| `LSPC-001` | all subjects unsupported，request 仍带 bodies | Provider empty/failed output补做 gate |
| `LSPC-002` | OUT_OF_SCOPE body 进入后续 terminal filter | later rejection撤销 prior exposure |
| `LSPC-003` | Provider-visible set 是 eligible subset，但漏一个 required Fact operation subject | subset 足以证明 complete operation projection |
| `LSPC-004` | Relation FactSet 只引用一个 eligible path，但 request 带全部 eligible bodies | eligible upper bound就是least authority |
| `LSPC-005` | observation Provider 收到另一个 Provider assignment 的 body | shared domain 等于 shared source authority |
| `LSPC-006` | classification bytes 相同但来自另一个 attempt | semantic equality继承live claim |
| `LSPC-007` | limits 相同的新 `BudgetContext` | equal limits 等于 original attempt |
| `LSPC-008` | caller传 path set/digest/boolean | assertion拥有projection authority |
| `LSPC-009` | projection/function变化，old operands/run identity不变 | exact input digests绑定所有未来 gate |
| `LSPC-010` | new shape仍使用旧 `0.1/0.1/0.2` wire | historical protocol可静默改变cardinality |
| `LSPC-011` | 同一 claim 并发/重复执行 | prepared projection可多次消费 |
| `LSPC-012` | classification后 deadline/cancel latch | stale frame仍可启动 Provider |
| `LSPC-013` | full frame超 cap、filtered frame可容纳 | 先编码全量再过滤仍满足 admission |
| `LSPC-014` | denominator empty、all unsupported、later empty assignment | 三种无-body world 具有同一 closure |
| `LSPC-015` | worker只核 projection digest，不核 included-byte equality | self-consistent document证明 exact exposure |
| `LSPC-016` | Provider仍可从 document/side channel取得 omitted bodies | filtered map就是完整 input boundary |
| `LSPC-017` | child失败后用新 attempt成功结果拼接 | same semantic world恢复原 authority |
| `LSPC-018` | projection tests 全绿 | Parse/Fact/Coverage fulfillment 已经成立 |

测试只能 witness 这些边界，不能修改 wording、挑选 empty semantics、授予 implementation 或把 candidate 升格为
frozen。

## 13. 明确 non-decisions

本文不决定或授权：

```text
classification persistence Route A/B
public Language Support/operation carrier or Schema
historical/offline exact blob reacquisition
real parser / AST / syntax-version discrimination
Parse per-subject terminal outcome or fulfillment
Fact obligation-universe derivation or fulfillment correction
Relation semantic/profile changes
public Provider registry or hostile-code sandbox
shared ObservationReceipt / OperationLedger
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
CLI / Workbench / Core / Q / O / T
```

本文中的 `Parse gate` 只表示进入 source-body operation 的资格边界，不把任何 Provider invocation 重命名为 Parse
fulfillment。Language Support、Parse 与 Fact 继续是三个不同 authority seams。

## 14. 后继有限实现段与逐段停止线

只有本文后继独立冻结发布完成最后门后，才允许严格串行实现：

```text
A. private projection value / canonical digest / use-time seal
B. controller-owned same-attempt gate and per-child one-shot claims
C. Fact wire 0.2 + operands 0.4 correction
D. Relation derivation wire 0.3 + operands 0.5 correction
E. Relation observation wire 0.4 + operands 0.6 correction
F. three controller integrations and exact empty-world behavior
G. LSPC-000..018 hardening and four-lane byte stability
```

每一步都是停止线。A–G 不得修改公共 Schema、Profile/Policy、public Evidence、Fact/Relation identity、Parse terminal、
Coverage、Manifest、publisher、Bundle、CLI 或 Workbench。若实现证明：

- operation set 不能从冻结 FactSet/domain mechanical derivation；
- application validator 无法在不向 Provider泄露 omitted bytes 的前提下验证 projection continuity；
- implementation 无法在保持既有 applicable-child 真实运行语义时承载 exact empty-body projection；
- new wire/operands identities 无法保持历史兼容；
- current public Schema 必须提前变化；

则必须停回本合同或显式 reopen 被击穿的最小上游，不能缩小 denominator、旁路 gate、复用旧 identity 或先写 runtime
再事后解释。

## 15. 候选验收与冻结序列

本文只有同时满足以下条件才可进入独立冻结发布：

1. `LSPC-000..018` 均有唯一合同裁决；
2. classification、operation projection、live gate、child claim、ProviderRun 与 fulfillment authority 分离；
3. exact eligible upper bound 与三类 stage-specific operation denominator 均无 caller/Provider自由度；
4. Provider-visible source bodies 对 operation set 是 exactly-equal，而不是仅 subset；
5. original context/parent/child eligibility 与 one-shot prepared frame 的绑定完整，多个合法 child claims 又不被压成一个；
6. old/new wire 和 operands identity 不冲突、不 fallback、不重算历史；
7. empty denominator、all unsupported 与 later empty assignment 保持可区分且不生成高阶 closure；
8. diff 只有本文、README、AGENTS 与 milestones 状态入口；
9. local Markdown/Schema/static gates、exact scope、UTF-8/LF/final-LF 与 `git diff --check` 成立；
10. 候选 PR original required checks 全部成功并经受保护 main 合入；
11. new exact main Public CI、Browser Smoke，以及 README/本文/milestones 的 fresh anonymous installed-product
    readback 与 independent reconciliation 成立；
12. 后继独立 docs-only freeze publication 完成自己的同等级 final bytes、original PR、merge、exact-main 双门与 fresh
    readback/reconciliation。

只有第 12 项完成后，才可发布：

```text
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_ALLOWED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_STARTED
```

授权只覆盖第 14 节 A–G。合同候选、candidate PR 绿灯、merge 或 exact-main CI 都不能单独授予 implementation。

## 16. 已资格化候选与冻结发布交接

PR #221 original Public CI、受保护合入 `main@f4d531bd49de330bd7a186633699262997e949f4`、该 exact main
Public CI / Browser Smoke、README / 本文 / milestones 的 fresh installed-product readback 与 independent
reconciliation 已成立；本合同候选因而成为 qualified history。第 1 节的唯一完整 marker block 仍只是
[文档 209](209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)的条件化 target；
冻结发布自己的最后门闭合以前，runtime 继续未授权，persistence 与 SliceSet/Coverage 后继保持未开始。

新的 Agent 必须先读文档 150、165、175、202、206、207 与本文，然后重点攻击：operation denominator 是否能从
existing frozen Facts/domain 唯一导出、provider-bound projection 是否仍可跨 purpose 移植、worker validation 是否偷信
controller path list、多个 child claims 是否复用了 authority、empty child 是否被任意选择、filtered request 是否仍保留
omitted body side channel，以及 new operands 是否真的改变 ProviderRun identity。

## 17. 本地候选证据

本文从 exact `main@940b6fc9ad974c4e4afb4f6f3e2f635efe780e1c` 的独立分支建立。当前 diff 不得包含
runtime/tests/Schema/Profile/Policy/corpus/vector/Provider/parser/CI 或发布文件。

提交前至少复核：

1. relative Markdown links、heading/fence、状态 marker、敏感/本机路径与 exact scope；
2. `git diff --check`；
3. applicable docs/Schema regressions 在 CPython 3.10/3.13 normal/`-O`；
4. 文档 207 六 world/four-lane audit 的 canonical bytes 未因本 docs-only patch 改变；
5. old protocol/runtime bytes 与 frozen identity files 保持不变。

最终候选本地结果：

```text
exact diff scope
  PASS: README.md / AGENTS.md / docs/milestones.md / this document only

Markdown / Schema
  PASS: CPython 3.10.6 normal, 40/40
  PASS: CPython 3.10.6 -O,     40/40
  PASS: CPython 3.13.13 normal, 40/40
  PASS: CPython 3.13.13 -O,     40/40

static
  PASS: 497 relative links
  PASS: UTF-8 without BOM, LF, final LF, balanced fences
  PASS: candidate marker exactly once in each of four files
  PASS: git diff --check

doc207 six-world runtime observation continuity
  PASS: CPython 3.10.6 / 3.13.13 normal / -O
  PASS: each canonical report 3072 bytes
  PASS: each SHA-256 fec549e3181d02c0ef200c0d3ddc91ebec5d32866519ea0de6f6b9e3d2737ca0
  PASS: each byte-equal to the qualified doc207 reference
```

第一次四车道 invocation 未设置 current worktree `src` 的 `PYTHONPATH`：每车道 37 个 Schema tests 已通过，但
`tests.test_markdown` 在 import 阶段以 `ModuleNotFoundError: veritrail` 停止。该组只记为
`INVALID_LOCAL_TEST_SETUP`；修正命令先打印 `veritrail` 与 test module 的 current-worktree `__file__`，再得到上述
40/40。

六 world continuity 复核又保留三项 audit-harness setup observations：第一次 `Get-FileHash -LiteralPath` 错把 `*`
当 literal path；第一次 report writer 多写一个 LF，形成四份一致但无资格的 3073-byte files，且 PowerShell 对单一 hash
字符串索引成字符后仍打印了错误 PASS；第二次 binary capture 把 CRLF strip 字符串双重转义，形成四份 3074-byte
files，并由 fail-fast hash check 拒绝。最终 runner 使用 `bytes((13,10))` 消除转义歧义，严格检查 unique hash、expected
hash 与 reference byte equality，才形成上述 qualified result。这些 setup observations没有修改 repo 或产品 runtime，
也不被最终 PASS 改写成未发生。

最终字节复核的第一次 combined tool call 又因 JavaScript template 中的 Markdown fence 反引号在 command construction
阶段触发 `SyntaxError`；没有任何子命令启动。后继把四个 test lanes 与不含反引号字面量的 static checker 分开，才形成
最终门禁结果。

PR 门、merge、exact-main 双门和 readback 结果必须在形成后追加；不得先写成已通过。
