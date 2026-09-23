# R1 ReviewSlice Admitted-Graph Input / Anchor-Spec Obligation Closure 合同 0.1

> 状态（合同候选）：`R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_CANDIDATE /
> R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 起始基线：`main@0c2ab31671a89b7c96fb5a44c390c85e7820c8c5`，Git tree
> `ccc8a8f49aec2c976c9996c952542b25015a4565`
>
> 前置审计：[Post-Admission ReviewSlice Input / Obligation Closure 系统审计](188-r1-post-admission-review-slice-input-obligation-closure-system-audit.md)
>
> 冻结输入：[确定性语义切片合同](113-r1-deterministic-semantic-slice-contract.md)、
> [Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Declared Relation Observation Domain / Composition Qualification 合同](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)、
> [RelationSet Admission / Public Qualification Binding 合同](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)与
> [Admission 实现冻结发布](187-r1-relation-set-admission-and-public-qualification-binding-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本合同只冻结 admitted-graph
> input continuity、anchor/spec obligation domain、private per-obligation outcome 与 reconciliation 的最小
> authority。当前提交不修改 Schema、corpus、identity vector、runtime、测试、依赖、CI、Provider、parser、
> publisher、Manifest、ReviewSliceSet、CoverageLedger、Attention、CLI、Workbench、Core、P/Q/D/Cu/O/T、
> tag 或 Release。

## 1. 目的与停止线

文档 187 已冻结 private RelationSet admission 与 attempt-bound admission witness；文档 188 又证明：

```text
RelationSet admission established
    != downstream Slice input continuity established

anchor/spec responsibility enumerated
    != responsibility discharged

self-consistent Coverage denominator
    != authoritative denominator
```

本合同只关闭下列接缝：

```text
exact DerivationInputSet
+ exact owned qualification history
+ exact OwnedRelationSetAdmissionState
+ same-attempt live continuation
    -> one eligible admitted-graph Slice input
    -> deterministic anchor/spec obligation domain
    -> exactly one permitted outcome per obligation
    -> private obligation reconciliation
```

它不直接创建公共 `ReviewSliceSet`、`CoverageLedger`、DerivationEvidence 新版本、Manifest entry 或 Bundle，
也不授权完整 publisher、Attention、Verdict、CLI 或 Workbench。首个实现即使后续获准，也必须停在 private、
copy-owned、non-published closed proof；公共 SliceSet admission 与 Coverage/publication 继续由后继合同决定。

本合同不把 BFS 当作问题选择的起点。规范遍历仍由文档 120 冻结；它只有在 exact input eligibility 与
obligation domain 已建立后，才有资格为逐项履责提供结果。

## 2. 七层 authority 必须分开

```text
1. sealed ReviewPolicy / DerivationProfile
   拥有 anchor kinds、allowed relations、结构预算与规范遍历语义

2. Fact composition / RelationSet admission
   拥有 exact Fact membership 与 admitted graph membership

3. Slice input join
   证明 Policy/Profile/FactSet/RelationSet 来自同一 eligible attempt

4. obligation domain construction
   机械枚举本轮必须履行的全部 anchor/spec

5. per-obligation traversal
   对一个 exact spec 报告 normal Slice 或 typed non-success

6. obligation reconciliation
   验证每个责任恰有一个允许 outcome，且 Slice/frontier 不悬空

7. SliceSet / Coverage / publication
   后继把已成立的 private closure 编码为公共 Artifact 并绑定文件
```

因此：

```text
admitted RelationSet                  != eligible Slice input
same relation_set_digest              != same execution authority
same Slice semantics                  != same attempt receipt
obligation domain exists              != obligations fulfilled
one Slice exists                      != all anchors closed
Coverage partition is self-consistent != denominator authoritative
private closure established           != ReviewSliceSet admitted
private closure established           != public Bundle publishable
```

Coverage 只能消费 obligation domain，不能拥有或缩小它；traversal 只能报告一个 assigned spec 的结果，不能
选择自己的 denominator；reconciler 只能验账，不能替 traversal 补造 Slice、negative 或 gap。

## 3. exact admitted-graph input continuity

### 3.1 首个正向输入必须同时具备四类所有权

首个 Slice input join 必须从同一运行链获得：

```text
DerivationInputSet
  exact canonical SourceSnapshot / ReviewPolicy / DerivationProfile bytes
  exact verified source blob snapshot

OwnedRelationCompositionQualificationResult
  exact Fact phase bytes、Relation phase bytes、observation domain、receipts 与 qualification

OwnedRelationSetAdmissionState
  exact admitted RelationSet bytes、admission witness 与全部 attempt coordinates

opaque same-attempt continuation
  原始 live BudgetContext 与 parent eligibility 的不可伪造连续性
```

这里的“同时具备”不要求把既有 frozen public Artifact 改成一个大对象。实现可以形成新的 private owned state，
也可以在一个集成 controller 内保持引用；但不得用 raw JSON、路径、digest-only、caller boolean、caller witness、
新建 `BudgetContext` 或相同 limit 的另一 context 替代。

当前 `OwnedRelationSetAdmissionState` 有意不 copy-own FactSet/Policy bytes，也不暴露 live continuation。这不是旧
admission 合同缺陷，而是本合同必须显式关闭的下游 seam。后继实现若需携带新的 opaque continuation，应新增
private state/handle 或集成 controller，不得改写 RelationSet、admission witness、Evidence 0.2 或任何历史 identity。

### 3.2 join 必须重新验证的闭包

join 至少必须逐项重算并比较：

1. `derivation_id` 与 request provenance 属于同一 attempt；
2. `source_snapshot_digest / policy_digest / analysis_scope_digest / slice_policy_digest /
   derivation_profile_digest / fact_set_digest / relation_set_digest` 全部连续；
3. ReviewPolicy seal、Profile digest、SourceSnapshot digest 与 copy-owned canonical bytes 成立；
4. Fact phase 的 canonical Facts、provenance、conflicts 与 `fact_set_digest` 可重新闭合；
5. qualification domain/receipts/candidates/conflicts 与 `qualification_digest` 可重新闭合；
6. admitted RelationSet membership、provenance/conflicts、witness 与 `admission_witness_digest` 可重新闭合；
7. admission witness 的 exact run/qualification coordinates 与本次 qualification history 一致；
8. continuation 仍属于原 parent attempt、原绝对 deadline 与原 artifact/memory budget，且尚未 revoke、stop、
   release 或被另一个 Slice execution claim 消费。

任何一项失败都必须在 obligation enumeration 前 fail closed。join 不重新运行 Provider、不重新解析 mutable path、
不重发预算、不选择 conflict winner，也不因 semantic digest 相同而从另一 attempt 借 witness。

### 3.3 input state 的最小所有权

正向 join 最多形成一个 private `AdmittedGraphSliceInput` 等价值，copy-own 或不可变引用下列内容：

```text
exact canonical Policy/Profile/Snapshot input bytes
exact reconstructed canonical FactSet bytes
exact admitted RelationSet bytes
exact qualification/admission identities
exact verified source blob snapshot required by the frozen Profile
opaque one-attempt continuation eligibility
```

名称不冻结；语义冻结。该值没有 path、output root、Manifest、publisher、Artifact role 或 final Evidence authority。

## 4. upstream gate、conflict 与 closed empty

三种世界必须分开：

### 4.1 conflict-free admitted graph

只有同时满足下列条件，才允许建立 normal obligation domain：

```text
candidate_composition_status = CONSISTENT
RelationSet.conflicts         = []
all exact input closures      = valid
same-attempt continuation     = live and exclusively claimed
```

### 4.2 conflict-bearing admitted graph

`QUALIFIED / CONFLICTING` 仍是合法 admitted RelationSet，但不是 normal traversal input。必须机械形成：

```text
slice_input_status = BLOCKED_BY_RELATION_CONFLICT
normal obligation domain = absent
normal Slice candidates = []
future SLICE_DERIVATION denominator = UNKNOWN
future reason includes PROVIDER_CONFLICT + UPSTREAM_DENOMINATOR_UNKNOWN
```

这不是“零 obligation”。它是上游图语义无法建立，不能借空数组改写为 closed empty，也不能只遍历未冲突的
局部连通分量。后继若要 conflict isolation，必须独立冻结合同。

### 4.3 真正零 anchor

若 exact conflict-free FactSet 中没有任何 `fact_kind` 命中 sealed `anchor_fact_kinds`，则：

```text
obligation domain = KNOWN and empty
obligation accounting = CLOSED_EMPTY
normal Slice candidates = []
```

该空结果只能由独立 domain construction 证明，不能由 traversal 没报告 Slice、caller 提交空列表或 Coverage
自报 denominator 为空得出。

shared interruption、invalid join、upstream non-normal state 与 conflict world 都不得冒充这种 closed empty。

## 5. anchor/spec obligation domain

### 5.1 唯一枚举规则

在 conflict-free eligible input 上，actual anchors 恰为 canonical FactSet 中：

```text
fact.fact_kind in ReviewPolicy.slice_policy.anchor_fact_kinds
```

每个 actual anchor 必须机械产生恰好一个完整 `ReviewSliceSpec 0.1`：

```text
source_snapshot_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
fact_set_digest
relation_set_digest
anchor_fact_id
allowed_relations[]
max_depth
max_symbols
max_files
max_relations
slice_spec_digest
```

字段与 `slice_spec_digest` 计算沿用文档 120；request/CLI/traversal 不得覆盖。anchor 按
`(Profile fact-kind rank, fact_id)` 排序，最终 obligations 按该顺序唯一保存；同一 `slice_spec_digest` 不得重复。

### 5.2 domain document 与 identity

首个 private domain 至少绑定：

```text
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
fact_set_digest
relation_set_digest
obligations[] = complete ordered ReviewSliceSpec values
slice_obligation_domain_digest
```

精确 identity 固定为：

```text
domain  = veritrail.review.slice-obligation-domain/0.1
payload = {
  source_snapshot_digest,
  analysis_scope_digest,
  slice_policy_digest,
  derivation_profile_digest,
  fact_set_digest,
  relation_set_digest,
  obligations
}
```

`policy_digest` 留在完整 private domain 中并由 input join 复核，但不进入 content digest；同一 sealed slice
semantics、FactSet 与 RelationSet 可以在不同合法 Policy/attempt 中共享 domain content identity。attempt authority
由后述 closure receipt 单独绑定，不能写入 `slice_spec_digest` 或未来 `slice_id`。

该 domain 是 future `SLICE_DERIVATION` denominator 的唯一来源。Coverage item refs 必须由完整 obligations 的
`slice_spec_digest` 机械投影；Coverage 不得反向决定或修剪 domain。

## 6. obligation fulfillment 与 outcome

### 6.1 一项责任只接受一个 terminal outcome

每个非空 domain obligation 必须被 exactly-once assigned 给 deterministic Slice traversal。首版不引入可插拔
Slice Provider；规范遍历属于 application semantics。每个 outcome 至少绑定：

```text
derivation_id
admission_witness_digest
slice_obligation_domain_digest
slice_spec_digest
outcome_status
normal Slice candidate or typed failure detail
```

允许的正向 outcome 只有：

```text
NORMAL_COMPLETE
  -> one normal Slice candidate
  -> frontier = []
  -> Slice coverage_status = COMPLETE

NORMAL_PARTIAL
  -> one normal Slice candidate
  -> frontier != []
  -> every frontier reason is a frozen structural limit
  -> Slice coverage_status = PARTIAL
```

结构预算造成的 `NORMAL_PARTIAL` 是一次已履责结果，不是 wall-clock partial。未来 Coverage 必须把其 spec 记入
`truncated` 并逐项复制 frontier；不得把它计入 `completed`，也不得因存在 normal Slice 就显示 COMPLETE。

### 6.2 non-success 不生成 normal Slice authority

以下情况必须保留 typed private failure/diagnostic，但不能形成 normal Slice candidate：

```text
EXECUTION_DEADLINE
EXECUTION_CANCELLED
EXECUTION_MEMORY_BUDGET
EXECUTION_ARTIFACT_BUDGET
DERIVATION_ERROR
INTEGRITY_FAILURE
```

首个 private closed proof 中，任一 non-success 都使 normal obligation closure 不成立；timeout/cancel/memory 后的
偶然 BFS prefix 必须丢弃，不能得到 `slice_id`。后继若要把确定性的 per-obligation `DERIVATION_ERROR` 编码为
公共 Coverage `execution_failed`，必须在 SliceSet/Coverage 合同中独立证明，不由本合同提前授予 publication。

### 6.3 outcome 不能自选责任

traversal 只接受一个由 domain assignment 产生的 opaque spec claim。它不能：

- 提交 caller-supplied spec 或 anchor；
- 把一个 outcome 绑定到另一 domain/attempt；
- 返回未分配的 Slice；
- 把没有 candidate 的结果写成 negative/complete；
- 在结构预算触发后省略 frontier；
- 用 wall time 决定 normal Slice members。

## 7. reconciliation 与资格边界

reconciler 必须从 independent domain 与 trusted traversal outcomes 双向验账：

```text
assigned spec IDs
  = domain obligation IDs
  = terminal outcome spec IDs

normal Slice candidate spec IDs
  = outcome_status in {NORMAL_COMPLETE, NORMAL_PARTIAL}
```

并逐项验证：

1. 没有 missing、unexpected、duplicate 或 cross-attempt outcome；
2. 每个 normal Slice 的完整 `slice_spec` 与 domain obligation 逐字节规范相等；
3. included Fact/Relation IDs 全部属于 exact FactSet/RelationSet；
4. anchor 始终在 included Facts，relation endpoint 不悬空；
5. `slice_id`、member order、frontier encounter order 与 coverage status 可按文档 120 重算；
6. COMPLETE outcome 无 frontier，PARTIAL outcome 有非空且完整的 structural frontier；
7. zero-domain 只有零 assignment、零 outcome、零 Slice candidate；
8. conflict/upstream-unknown world 没有 normal domain，也不能提交空-domain closure。

正向 reconciliation 最多形成 private `SliceObligationClosure` 等价值，包含 exact admitted input identity、domain、
normal Slice candidates、outcomes 与 attempt-bound closure digest。该值证明“该看的均已按允许结果记账”，不证明
SliceSet 已 admitted、Coverage 已形成、Repository 已理解或 Verdict 已成立。

attempt-bound closure identity 必须包含：

```text
derivation_id
admission_witness_digest
slice_obligation_domain_digest
ordered outcome identities
closure status
```

因此两个独立合法 attempts 可以共享 `slice_obligation_domain_digest` 与未来 `slice_set_digest`，但 closure receipt
bytes/digest 必须不同。attempt receipt 不进入 `slice_id` 或 `slice_set_digest`，避免把执行权威污染成内容身份。

## 8. future SliceSet / Coverage 的机械映射

本合同不创建公共 Artifact，但后继 encoding 必须满足下列单向关系：

```text
domain obligations
    -> Coverage.SLICE_DERIVATION.denominator

NORMAL_COMPLETE outcomes
    -> ReviewSliceSet member
    -> Coverage completed

NORMAL_PARTIAL outcomes
    -> ReviewSliceSet member
    -> Coverage truncated + exact frontier

typed non-success
    -> no normal Slice member
    -> only a separately authorized Coverage/diagnostic mapping
```

至少必须拒绝：

- Coverage `completed` 引用不存在的 Slice；
- Slice 存在但 domain 中无对应 spec；
- domain 有 spec 而 Slice/outcome 都缺失；
- Slice、denominator 与 completed 一起缩小；
- frontier 只在 Slice 或只在 Coverage 一侧出现；
- partial Slice 被 Coverage 写入 completed；
- conflict world 使用 KNOWN empty denominator。

当前 `ReviewSliceSet 0.1` 与 `CoverageLedger 0.1` 的 semantic fields 足以表达正常 Slice、structural frontier 与
KNOWN/UNKNOWN denominator；本合同没有获得必须升级 Schema 的反例。因此本轮禁止先加字段。后继若证明
attempt-bound closure 无法通过现有 Evidence/cross-object conformance 外部复算，必须以新反例重开 public
binding，不得让 SliceSet 自报 admission/closure。

## 9. shared BudgetContext 与 interruption

Fact、Relation、admission-bound Slice input 与后继 traversal 必须消费同一个绝对 `BudgetContext`：

```text
Fact / Relation phases consume time and memory
    -> remaining live budget
    -> Slice input/domain/traversal continue
```

不得为 Slice 刷新 wall clock、memory 或 artifact budget。content domain/identity 不包含 wall time；execution
receipt 必须保留本次 attempt 的实际停止事实。

same-attempt continuation 必须是不可伪造、至多消费一次的 private capability。concurrent/replayed claim、另一个
attempt 的 context、已 stop/release 的 context、deadline 后 claim 或 admission state 被篡改，都必须在任何 normal
Slice identity 建立前拒绝。

若 interruption 在 domain 建立前发生，不形成 normal domain。若发生在 traversal 中，domain 作为已枚举的 private
责任事实可以留在 diagnostic state，但任何偶然 prefix、部分 outcome set 与 provisional Slice candidates 都没有
normal closure authority。

## 10. `RS-000..016` 的唯一裁决

| ID | 单变量世界 | 本合同裁决 |
| --- | --- | --- |
| `RS-000` | eligible anchor 仍在，Slice 被删，Coverage 保留 completed | cross-object reject；completed 不能补 Slice |
| `RS-001` | Slice 与 denominator 一起缩为空 | domain 从 exact Policy+FactSet 独立重建，较小集合 reject |
| `RS-002` | same semantic graph、different attempt/witness | content identity 可同；input eligibility/closure receipt 不可继承 |
| `RS-003` | raw RelationSet valid，无 owned admission state | input join 前 reject |
| `RS-004` | 两个 anchors，只履行一个 | missing outcome；closure 不成立 |
| `RS-005` | exact FactSet 无 allowed anchor kind | KNOWN empty domain；`CLOSED_EMPTY` |
| `RS-006` | conflict-bearing admitted graph 输出 normal Slice | conflict gate reject；无 normal domain |
| `RS-007` | Slice frontier 与 Coverage frontier/truncated 不同 | future cross-object reject；private outcome 以 exact frontier 为源 |
| `RS-008` | timeout 后保留 traversal prefix | prefix 无 `slice_id`/normal authority；closure 不成立 |
| `RS-009` | digest 全同但 Policy/Profile canonical bytes 不属于该 input set | exact-byte/seal join reject |
| `RS-010` | 用 fresh BudgetContext 复刻同 limits | continuation reject；相同预算参数不是同一 attempt |
| `RS-011` | 同一 continuation 被 replay/concurrent claim | exactly-once claim reject |
| `RS-012` | outcome 指向另一 domain/attempt 的 spec | assignment/attempt closure reject |
| `RS-013` | Partial Slice 有 frontier，但 outcome 自报 COMPLETE | mechanical status reject |
| `RS-014` | Slice 引用 graph 外 Fact/Relation 或留下半条 edge | membership/endpoint closure reject |
| `RS-015` | same content 的 H1/H2 复制 closure receipt | witness/derivation/outcome identity reject |
| `RS-016` | zero-domain 由 caller 空数组而非 exact FactSet 枚举得出 | domain construction gate reject |

这些 falsifier 限制下一实现，不授权当前提交创建 runtime、公共文件或 fixture rewrite。

## 11. 首个实现分段与停止线

只有本合同候选自己的原始远端门、受保护主线合入、新 exact-main 双门、fresh anonymous installed-product
readback 与后继独立 docs-only 冻结发布全部成立后，才允许严格按顺序实现：

```text
A. same-attempt continuation and admitted-graph input join
B. exact FactSet reconstruction + Policy/Profile/admission cross-validation
C. conflict gate + deterministic anchor/spec obligation domain
D. private obligation assignment and deterministic traversal boundary
E. normal COMPLETE/PARTIAL outcome + structural frontier proof
F. missing/duplicate/dangling/cross-attempt reconciliation
G. zero-anchor closed-empty + conflict/upstream-unknown negative worlds
H. RS-000..016 hardening and cross-runtime byte proof
```

A–H 只允许 private values 与测试，不得写 output root，不得创建公共 ReviewSliceSet/CoverageLedger/Evidence/Manifest，
不得修改 Schema、Corpus 或 identity vector。若 D–E 证明 deterministic BFS 与 input/domain closure 无法在不扩张
publisher/public contract 的情况下形成 private proof，必须停下重审，不得越 scope 硬做。

首个实现仍只覆盖冻结的 Python 3.10 Profile、`LEXICAL_CONTAINS / IMPORT_TARGET_LITERAL` 与 closed fixtures；
不新增 import resolution、CALLS、动态语义、risk finding、base/head diff、完整 Relation algorithm、Attention ranking
或 human disposition。

## 12. 合同候选门

合同候选至少必须通过：

1. `git diff --check`、文档状态/链接/敏感信息检查；
2. 现有 contract/documentation gates；
3. current full relevant Python regression 的 normal 与 `-O`；
4. CPython 3.10 与 3.13 的合同关键字节一致性；
5. `RS-000/001/002` 历史反例坐标保留，不能被改写为当前实现事实；
6. PR original checks、受保护主线合入、新 exact-main Public CI 与 Browser Smoke；
7. README、本文与 milestones 使用不同 Plan/session/output root 的 fresh anonymous readback；
8. architecture DOT/SVG 若无能力拓扑变化必须保持字节不变；若状态投影变化则 README/AGENTS/milestones 同步。

只有上述闭环与独立 freeze publication 成立，状态才能推进为：

```text
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_FROZEN
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

在此之前，当前状态只能是合同候选；不得按 A–H 施工。

## 13. 反证与最小重开

| 新事实 | 最小影响 |
| --- | --- |
| exact main 已有不可伪造的 Slice continuation 与 owned input join | 收窄 A，不重开 domain/fulfillment |
| FactSet 无法从 qualification history 复算为 exact bytes | input join 模型失效；先修正上游 ownership，不得从 digest 猜 |
| frozen contract 允许 Slice 不消费 RelationSet | 重新评估 admission-bound graph input，不改写 admission 历史 |
| existing Schema 无法表达 normal COMPLETE/PARTIAL 与 exact frontier mapping | 以最小反例重开 public encoding；本合同不自动授权升级 |
| deterministic traversal 必须由独立 Provider 承担 | 重开 outcome authority；不得把 caller output 当 trusted outcome |
| shared BudgetContext 在合法 architecture 中必须在 admission 后结束 | 重新定义 phase budget handoff；不得静默刷新整份预算 |

任何重开都只影响被反例击穿的条款，不移动文档 113/120/175/183/187 的历史冻结坐标。

## 14. 非声明

本合同候选不声明：

- ReviewSlice BFS、ReviewSliceSet、CoverageLedger 或 publisher 已实现；
- public Schema、Manifest role 或八文件 Bundle 已修改；
- private obligation closure 等于 SliceSet admission 或 final Evidence；
- `CLOSED_EMPTY` 等于“源码中没有关系”或“仓库已完整理解”；
- structural `PARTIAL` 等于 execution failure；
- same content 可以继承另一 attempt 的 admission/closure authority；
- Agent、模型 confidence、ranking、KPI 或 human disposition 获得 Verdict authority；
- R1、D、Cu、Q、O 或 T 的后继施工已获授权。

本轮也不启动外部大厂 failure-shape survey。内部冻结合同、当前 private runtime 与 `RS-000..002` 已足以决定
该 seam；外部案例只有在后继 public gap/receipt encoding 出现真实经验缺口时才定向查询。
