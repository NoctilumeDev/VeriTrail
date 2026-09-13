# R1 Fact Admission 与 DerivationEvidence Closure 系统审计

> 状态：`R1_DERIVATION_EXECUTION_CELL_FROZEN /
> R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED /
> R1_FACT_EVIDENCE_CLOSURE_CONTRACT_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@a96912fa3f141a783e728f95e0feb26341197a32`
>
> 上游冻结事实：[R1 Derivation Execution Cell 实现冻结发布](153-r1-derivation-execution-cell-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改 Schema、corpus、
> runtime、测试、依赖、CI、Provider、parser、FactSet、DerivationEvidence、Relation、Slice、Coverage、
> Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release

## 1. 审计问题与停止线

Execution Cell 已经证明：一个 closed deterministic test Provider 可以在受控 cell 内产生 candidate，application
可以复算 canonical Fact identity，controller 可以形成 copy-owned、non-published terminal phase result，并在
失败时不可恢复地撤销 attempt success eligibility。

它没有授权把该 phase result 直接包装成公共 Artifact。本轮只问：

> ProviderRun 的执行事实、application-canonical Fact、FactSet membership、DerivationEvidence projection 与
> DIAGNOSTIC/COMPLETE publication eligibility 怎样组合，才不会让局部合法对象在接缝处获得过强身份？

本轮明确不问真实 Python parser、Relation、conflict/UNKNOWN、Slice、Coverage 或完整 Derivation 怎样实现，
也不把现有 Schema 能表达某个文档误读为 runtime 已拥有发布它的权力。

## 2. 冻结输入没有漂移

审计开始时的关键字节为：

```text
docs/120-r1-schema-and-canonical-identity-contract.md
SHA-256 c9c7105ef01d189733092901ee39ef0fde189ba19a41fdafb8b43ac671aad091

docs/132-r1-derivation-input-binding-contract.md
SHA-256 99c9bd7bb0451e2c22c1ebc28e382f1e128da0976c10b69b2700a83b81416961

docs/137-r1-derivation-attempt-and-fact-provenance-contract.md
SHA-256 7d3580d74b658450d07aa0ca7987d7278fe5441064869b9a45601b698bf43044

docs/140-r1-derivation-evidence-schema-correction-contract.md
SHA-256 95dc176ac312da99831c0dc12dbdd4c291634dd8026e0647ea96f47d848a3bca

docs/145-r1-derivation-budget-primitive-contract.md
SHA-256 9a7f4c470ca4b3869c3600e6e4dedd2ebd02c15257cdece428b15032f88ea9f5

docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md
SHA-256 e1e74ad96c6d16b4ef01943cbf9076247d237913fc27b24760752e29961a1906

docs/153-r1-derivation-execution-cell-freeze-publication.md
SHA-256 ebc34864fe29256cd36bfb633f309d71e97f300d34e39ffb57b731202b19d474

schemas/review-fact-set-0.1.schema.json
SHA-256 e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1

schemas/review-derivation-evidence-0.1.1.schema.json
SHA-256 a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045

schemas/review-derivation-manifest-0.1.schema.json
SHA-256 69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
```

实现侧的精确审计输入为：

```text
plugins/review-attention/src/veritrail_review/_execution_cell.py
SHA-256 56d058938905fe567c3b8f8a5f664fdf494c39ee3e7e4cd44d26e25343b91548

plugins/review-attention/src/veritrail_review/_execution_cell_values.py
SHA-256 d742fd5c48a250948031ee27610b9960510b7d89530ac48b3f3bb8f40711879e

plugins/review-attention/src/veritrail_review/budget.py
SHA-256 df20e3cd8a5299146ad2128c468afcc6057747540ea640ee96232f4957231b6b
```

本轮没有发现需要推翻以下上位事实的反例：

- `DerivationInputSet` copy-own 三份输入 Artifact exact bytes 与源码 blob bytes；
- Provider 只报告 candidate，application 拥有结构校验、规范化与 Fact identity；
- Fact identity 不包含 attempt、run、budget、时间或 provenance；
- phase result 不是 FactSet、DerivationEvidence 或 Manifest；
- COMPLETE 固定八文件，DIAGNOSTIC 固定四文件；
- whole derivation 只能消费同一个 `ReviewPolicy.execution_budget`；
- Relation、Slice、Coverage、conflict/UNKNOWN 与真实 parser 尚未获得实现权。

## 3. 当前真实组合形状

当前 private runtime 的成功输出是：

```text
Owned DerivationInputSet
        +
opaque derivation_id
        +
closed test Provider binding
        ↓
one contained execution cell
        ↓
Provider candidate observations
        ↓
application validation + canonical Fact identity
        ↓
controller terminal continuity + phase commit
        ↓
OwnedExecutionCellPhaseResult
```

该 result 保存 input digests、request provenance、Provider descriptor、operands/run identity、run/phase 时间与
状态、一个 terminal diagnostic code、成功态 canonical Fact bytes/IDs 和 release outcome。它不暴露
`BudgetContext`，也没有公共 Artifact kind、Schema version、semantic digest、Manifest role 或输出路径。

公共 Schema 则描述另一个更晚的世界：

```text
DerivationEvidence
  ↔ ProviderRun reported IDs
  ↔ FactSet Facts/provenance
  ↔ Relation/Slice/Coverage
  ↔ COMPLETE Manifest

or

DerivationEvidence without normal derived artifacts
  ↔ DIAGNOSTIC Manifest
```

因此下一步不是“给 phase result 加一个 `to_json()`”，而是先关闭两个世界之间的 authority、identity、预算与
发布资格。

## 4. 四种身份不能压成一个 canonical Fact

```text
Provider candidate observation
  Provider 在本次 run 中报告的有界观察；没有 canonical identity authority

application-canonical Fact value
  application 根据 owned Snapshot/Profile/source bytes 复算出的稳定 Fact identity 与内容

admitted FactSet member
  通过 derivation-level cross-reference、排序、去重、provenance 与 conflict policy 后，进入 owned FactSet
  construction state 的成员

published Fact Artifact member
  被完整、原子、create-new R1_DERIVATION Bundle 的 FactSet 文件与 Manifest exact bytes 共同绑定的成员
```

现有 execution cell 已建立第二层，但没有建立第三、第四层。文档 153 中“canonical Fact admission 尚未实现”
应按这个边界理解；它不否定 application 已经复算 canonical Fact identity，也不允许后继把 identity conformance
自动升级成 FactSet/publication membership。

核心不变量为：

```text
Canonical identity conformance != FactSet admission
FactSet admission             != Artifact publication
Artifact publication          != Derivation COMPLETE
```

## 5. 系统审计发现

### 5.1 phase-level reported IDs 与 Evidence-level reported IDs 不是同一投影

成功 phase result 可以保存：

```text
phase.provider_run_status = COMPLETED
phase.reported_fact_ids    = IDs of application-canonical phase Facts
```

但最终 `DerivationEvidence` 只有在 whole derivation `COMPLETED`、对应正常 FactSet/RelationSet 随 Bundle 发布且
双向引用闭合时，才可以保存非空 reported IDs。若后继 Relation/Slice/Coverage 或 staging 失败：

```text
ProviderRun.execution_status remains COMPLETED
overall_execution_status becomes non-COMPLETED
all Evidence reported_*_ids become []
```

这不是改写 ProviderRun 历史，而是两个不同投影：

```text
phase summary
  -> 本 phase 曾规范产生哪些 identity

Evidence reported IDs
  -> 本 Bundle 中哪些正常 Artifact identity 可被解析
```

后继 assembler 不能原地修改 phase result、盲拷 reported IDs，或把空数组解释成 Provider 没有运行。它必须
新建 copy-owned Evidence projection，并在最终 outcome 已知后机械决定 reported arrays。

### 5.2 FactSet admission 必须重新关闭双向 provenance

当前 phase result 的每个成功 Fact 已被检查为：

```text
fact.provenance_refs == [provider_run_id]
reported_fact_ids    == sorted(unique(fact.fact_id))
```

这仍不足以授权 FactSet membership。admission 至少还须对同一 owned values 重新验证：

1. 每个 Fact 的 Snapshot/Profile/anchor/scope 仍与 admitted input 相同；
2. Facts 按 `fact_id` 排序，重复 identity 只能按冻结规则合并 provenance；
3. 每个 provenance ref 指向同一 future Evidence 中真实存在的 ProviderRun；
4. 每个 Evidence reported fact ID 在 admitted FactSet 中恰有一个解析目标；
5. 每个 admitted Fact 的 run provenance 反向出现在 Evidence summary；
6. 首个 single-Provider profile 不制造 multi-Provider conflict，`conflicts=[]`。

这里消费 phase result 的 owned bytes/value，不重新读取 channel、Provider state、临时文件或输入路径。

### 5.3 COMPLETED FactSet/Evidence 不能形成 standalone 公共切片

Manifest 0.1 没有“Fact-only complete”或“partial normal derivation” outcome。`COMPLETE` 必须同时包含：

```text
Snapshot + Policy + Profile + Evidence
+ FactSet + RelationSet + ReviewSliceSet + CoverageLedger
```

因此即使 Fact admission 与一个 provisional completed Evidence projection 都已在内存中闭合，也只能是后继
完整 derivation 的 owned construction state。当前不得发布：

```text
fact-set.json only
completed derivation-evidence.json only
Snapshot + Policy + Profile + Evidence + FactSet
placeholder Relation/Slice/Coverage
third Manifest outcome
```

Schema 能单独验证一个 FactSet 文档，不等于 runtime 获得单文件发布权。下一合同必须显式区分“closure
eligible construction state”和“publicly published closure”。

### 5.4 non-budget diagnostic 的规范放置尚未冻结

`DerivationEvidence` 的顶层与每个 ProviderRun 都有 `diagnostics[]`，且两处都进入
`derivation_evidence_digest`。冻结文本已经精确规定：

- memory stop：同一 tuple 同时出现在 active run 与顶层；
- artifact staging stop：只出现在顶层，subject 为 `null`。

但以下 code 只有 status/code 映射，没有 exact placement/cardinality：

```text
PROVIDER_UNAVAILABLE
PROVIDER_FAILED
NONCONFORMANT_PROVIDER_OUTPUT
EXECUTION_DEADLINE
EXECUTION_CANCELLED
INTERNAL_DERIVATION_ERROR
```

文档 120 的“顶层 diagnostics 可以汇总”不是规范投影。一次单变量 `PROVIDER_FAILED` 可以形成三份不同文档：

```text
run only
top-level only
run + top-level
```

本轮从 frozen memory specimen 建立共同的首版 exact-OID request provenance，再只改变 diagnostic placement
并分别复算 digest；三份文档均被
`review-derivation-evidence-0.1.1.schema.json` 接受：

```text
RUN_ONLY  7e6edc8c75f7dcd14c6f68bd8160a2828d59d6a72bc8d4729d37131198372441
TOP_ONLY  9e6d858c2d39430fb23abc7a9bf19cd5743be40b81703390785033bde7f26dcb
BOTH      3ddec86a4cf47b1fa3c992c8955e44eee1756dda66a9144bc419377e96c4c80c
```

Schema 只负责 shape，因此接受不构成缺陷；缺失的是 canonical assembler 的 conformance rule。若不先冻结，
两个正确实现会对同一 terminal fact 产生不同 Evidence identity。

### 5.5 success eligibility、diagnostic publication eligibility 与 cleanup permission 尚未分开

现有合同已经分开：

```text
attempt success eligibility
cleanup-only release permission
```

但 DIAGNOSTIC publication 落在两者之间，目前没有明确所有者。

对于 Provider failure/unavailable/nonconformance，execution cell 会撤销成功资格并返回 non-success phase
result；若绝对 execution deadline 仍有余量，未来 integrated controller 是否可继续消费同一 BudgetContext
发布 DIAGNOSTIC，尚未冻结。

对于 deadline/cancel/positive memory stop，冲突更直接：

```text
terminal stop latch wins
  -> BudgetContext leaves RUNNING
  -> cleanup-only release envelope
  -> no new semantic/staging work
```

但 Manifest 合同又允许 `INTERRUPTED` 只以 DIAGNOSTIC 四文件表达。若把“Schema 可表达”误读成“reference
runtime 必须发布”，runtime 将没有合法 artifact reservation/staging 权。

artifact budget stop 是最小反例：

```text
normal bundle staging
  -> next exact file would exceed artifact_bytes
  -> EXECUTION_ARTIFACT_BUDGET latch
  -> delete staging under cleanup-only envelope
  -> no further staging permission
```

此时若再写四个 DIAGNOSTIC 文件，就是在 stop 后重新授予 artifact work；若不写，correction corpus 中的
artifact-budget DIAGNOSTIC 只能继续是 shape/identity specimen。文档 140 已明确该 specimen 不授权 runtime
publication，本轮确认这个停止线必须保留。

这里暂不宣称冻结 Schema 自相矛盾，因为：

```text
INTERRUPTED / FAILED / UNAVAILABLE can only publish DIAGNOSTIC
```

可以被解释为“如果发布，只能使用 DIAGNOSTIC”，并不必然表示每次终止都必须发布 Bundle。真正未冻结的是：

```text
which terminal classes publish no R1 artifact?
which may publish best-effort DIAGNOSTIC under remaining execution budget?
does any post-stop diagnostic publication authority exist?
if it exists, which bounded budget owns it?
```

这些问题会改变 runtime、artifact budget 与失败证据强度，不能由实现便利决定。

### 5.6 standalone Execution Cell 不是 future assembler continuation API

当前 `run_closed_test_execution_cell(...)` 自己创建 BudgetContext，只返回 phase result，不暴露 context 或
eligibility gate。这是冻结停止线，不是漏掉一个返回字段：

```text
standalone component proof
  !=
continuable full-derivation controller
```

后继不得执行：

```text
call standalone phase
  -> receive result
  -> create new BudgetContext
  -> assemble FactSet/Evidence
  -> call it the same derivation
```

若后继需要可继续的内部组合，必须由一个新的 trusted integrated controller 在调用 execution phase 以前拥有
同一 context/eligibility，并在返回 public boundary 以前完成被授权的后继工作。raw context 仍不得泄露给
Provider、worker 或外部调用方；也不能为了复用现有函数而把 standalone phase result 变成隐藏 checkpoint。

## 6. 当前不改的边界

### 6.1 Fact semantic identity 与运行 provenance 继续正交

`fact_id` 不包含 ProviderRun、attempt、时间或 budget；Fact 的 `provenance_refs` 进入文件 bytes，但不进入
Fact semantic identity。`fact_set_digest` 同样去除 provenance，并故意不覆盖完整 `policy_digest`；Manifest
SHA-256 继续绑定完整文件差异。

因此两个不同 run 对相同源码观察可满足：

```text
same fact_id / same provenance-free fact semantics
different provider_run_id / provenance_refs / FactSet file SHA-256
```

本轮没有证据要求修改 Fact、FactSet 或 digest projection。

### 6.2 single Provider 不提前实现 conflict

首个冻结 profile 只有一个 required `python-ast` Provider。该 Provider 在同一 subject 报告不兼容 candidate
时，execution phase 已按 nonconformant output fail closed。后继最小 Fact admission 只能得到
`conflicts=[]`，不能借 FactSet Schema 已有 `conflicts[]` 就提前实现 cross-Provider conflict/UNKNOWN。

### 6.3 空成功仍是成功来源事实

Provider 正常运行并规范返回空 candidate set 时：

```text
ProviderRun = COMPLETED
phase Facts = []
phase reported_fact_ids = []
```

未来完整 derivation 可以形成 empty FactSet，但不能把它解释为 Provider 未运行、source unsupported 或
execution failure。Coverage 对空事实意味着什么属于后继 Coverage 合同，不在本轮发明。

### 6.4 输入 Artifact 继续逐字节连续

`DerivationInputSet` 已 copy-own imported Snapshot/Policy/Profile canonical bytes 与复获源码 blob bytes。后继
staging 必须复制/消费这些 exact owned inputs，不能重新打开原路径、重新解析 worktree、从移动 ref 取值，或
重新序列化一份“语义一样”的 Snapshot 替代已验证文件身份。

### 6.5 目前没有 Schema revision 结论

diagnostic placement 可以由 cross-object conformance 冻结，不天然要求改 JSON Schema；DIAGNOSTIC
publishability 是 runtime authority/budget 问题，也不等于先给 Schema 加字段。本审计因此不升级任何公共
Schema，也不把“可能无需升级”提前写成最终裁决。

## 7. 发现分类

| 类别 | 观察 | 当前裁决 |
| --- | --- | --- |
| Freeze blocker | application-canonical Fact 与 admitted/published Fact membership 仍共用“canonical admission”措辞 | 下一合同必须拆 identity conformance、FactSet admission 与 publication |
| Freeze blocker | phase reported IDs 与 final Evidence reported IDs 的条件不同 | 冻结 new-copy projection 与 final-outcome double closure |
| Freeze blocker | non-budget terminal diagnostics 的 run/top-level placement 未冻结，能产生多个合法 digest | 冻结 exact placement/cardinality conformance；不让实现任选 |
| Freeze blocker | stop 后 DIAGNOSTIC 是否可发布、由哪份预算/资格发布没有答案 | 先冻结 terminal-class publication capability matrix；不得在 cleanup envelope 内偷偷恢复 staging |
| Implementation gate | full assembler 必须在调用前拥有同一 BudgetContext 与 eligibility | 不复用 standalone API 作为 checkpoint；合同后再设计 private integrated controller |
| Implementation gate | FactSet/Evidence 双向引用、排序、去重、时间与 exact bytes 必须一次闭合 | 建立 owned unpublished construction state 与反例矩阵；不先写 Artifact |
| No change | COMPLETE 仍需要八文件，DIAGNOSTIC 仍需要四文件 | 不新增 Fact-only/partial Manifest outcome |
| No change | Fact/FactSet semantic digest 与 run provenance 正交 | 不修改 frozen identity projection |
| Deferred seam | multi-Provider merge/conflict、Relation IDs、UNKNOWN 与 Coverage | 继续等待各自 pre-contract audit |
| Deferred product seam | real parser、public CLI/Workbench、R2–R6、Q/D | 不由本合同反向扩大 |

## 8. 选定的下一个最小合同闭环

下一步只能从新的 exact main 起草一个独立 docs-only：

```text
R1 Fact Admission / DerivationEvidence Closure Contract 0.1
```

它必须逐项回答：

1. application-canonical Fact 怎样进入 owned、non-published FactSet construction state；
2. phase summary 与 final Evidence reported IDs 怎样保持不同 immutable projection；
3. single Provider 成功、空成功与失败时 Facts/provenance/conflicts 的 exact 形状；
4. FactSet、ProviderRun 与 Evidence 怎样完成双向 cross-reference；
5. 每个 terminal diagnostic 的 run/top-level placement、subject 与 cardinality；
6. 哪些 terminal class 不发布 R1 Artifact，哪些在何种剩余预算/资格下可发布 DIAGNOSTIC；
7. artifact-budget stop 怎样避免“为了报告超限而在超限后继续写”的自我矛盾；
8. success eligibility、diagnostic publication eligibility 与 cleanup permission 是否需要三个不同状态；
9. integrated controller 怎样持有同一 BudgetContext，而不把 raw context 或 standalone phase result变成公共 API；
10. 哪些问题可由 conformance 关闭，哪些确实要求最小修正既有冻结合同或 Schema。

合同候选可以修正被本审计击穿的最小原文，但不能写“新文档覆盖旧文档”。若既有条款不能同时满足，必须
回到拥有该语义的原合同做最小一致性修正，并保留反例与兼容边界。

该合同即使冻结，也只可授权自身明确列出的 non-published admission/Evidence projection 或合法
DIAGNOSTIC closure implementation；它不能自动授权真实 parser、Relation、Slice、Coverage、conflict/UNKNOWN
或 COMPLETE Manifest implementation。

## 9. 反例矩阵

| # | 单变量反例 | 错误推理 | 必须保持的裁决 |
| ---: | --- | --- | --- |
| 1 | Provider candidate 通过 application canonicalization | canonical Fact 已存在，所以已进入 FactSet | identity conformance 不等于 membership |
| 2 | phase COMPLETED 且 reported IDs 非空，后继 staging 失败 | 原样复制 reported IDs 到 non-completed Evidence | final Evidence 全部 reported arrays 清空 |
| 3 | ProviderRun 历史 COMPLETED，overall INTERRUPTED | 把 run 改写成 INTERRUPTED 才能清空 IDs | run status 保留；new-copy Evidence projection 清空 IDs |
| 4 | FactSet locally valid | 单独发布 `fact-set.json` | 无授权 Manifest outcome；不发布 |
| 5 | completed Evidence locally valid | 发布四文件 DIAGNOSTIC | DIAGNOSTIC 不得携带 completed normal derivation 语义 |
| 6 | run-only `PROVIDER_FAILED` diagnostic | Schema 接受，所以是唯一 canonical projection | placement 未冻结；合同先裁决 |
| 7 | top-only `PROVIDER_FAILED` diagnostic | 同上 | 同上 |
| 8 | run+top `PROVIDER_FAILED` diagnostic | 同上 | 同上 |
| 9 | deadline latch 后准备 DIAGNOSTIC staging | 诊断比正常产物特殊，所以可继续写 | cleanup-only permission 不授权 Artifact work |
| 10 | artifact reservation over ceiling | 删除 normal staging 后另写 DIAGNOSTIC | 不得用第二预算或 stop 后 staging 掩盖超限 |
| 11 | Provider failure且 deadline 尚有余量 | success eligibility revoked，所以任何诊断都不能留 | 先冻结独立 diagnostic publication eligibility；不由实现猜 |
| 12 | standalone phase result 返回 | 另建预算继续 assemble | 新 attempt；不能冒充同一 derivation |
| 13 | 相同 Fact semantics 来自不同 run | provenance 不同，所以 fact_id 不同 | fact_id 相同；run/file identity不同 |
| 14 | single Provider 同 subject 给出不兼容 candidate | 生成 FactConflict | 当前 phase fail closed；multi-source conflict 未授权 |
| 15 | Provider 成功返回空 set | 解释为未执行或 UNKNOWN | COMPLETED empty source；Coverage 含义延期 |
| 16 | 输入路径在 phase 后变化 | staging 重新打开路径获取最新 bytes | 只消费 DerivationInputSet 已拥有的 exact bytes |
| 17 | release cleanup 成功 | cleanup 成功恢复 attempt eligibility | eligibility 不可恢复；release 只证明无残留 |
| 18 | Schema 能表达 artifact-budget Evidence | reference runtime 已证明能发布它 | shape/identity expressibility 不等于 runtime publishability |

## 10. 本地审计证据

本轮在 clean worktree
`docs/r1-derivation-provenance-admission-audit@a96912fa3f141a783e728f95e0feb26341197a32` 上完成：

1. 逐项重读文档 120、132、137、140、145、149、150、152、153；
2. 复算本文第 2 节的冻结文件 SHA-256；
3. 对 FactSet、DerivationEvidence 0.1.1 与 Manifest 0.1 Schema 做字段/条件组合审计；
4. 对 `_execution_cell.py`、`_execution_cell_values.py` 与 `budget.py` 审计 context、eligibility、terminal
   mapping、phase result 与 artifact reservation 的真实边界；
5. 使用 CPython 3.13 与锁定 `jsonschema==4.25.1` 运行不落盘单变量 probe，证明同一
   `PROVIDER_FAILED` terminal fact 的 run-only、top-only 与 duplicated placement 均被当前 Schema 接受且产生
   三个不同 digest；
6. 确认 correction corpus 自己已声明 DIAGNOSTIC manifest 只是 test-only shape specimen，不授权 runtime
   publication。

Schema 接受多个 projection 是预期的 shape 边界，不被记录为 Schema 缺陷；probe 只证明 canonical
conformance 不能继续留给实现猜。它没有创建 corpus、fixture、runtime 或可发布 Artifact。

现有冻结边界的定向回归为：

| Runner | Execution Cell | Schema + correction corpus |
| --- | ---: | ---: |
| CPython 3.10 normal | 22/22 | 27/27 |
| CPython 3.10 `-O` | 22/22 | 27/27 |
| CPython 3.13 normal | 22/22 | 27/27 |
| CPython 3.13 `-O` | 22/22 | 27/27 |

四格都把 `src`、plugin `src` 与 test root 显式绑定到当前 worktree；没有把主工作树的 editable import
当成当前变更证据。另有：

```text
changed files
  = AGENTS.md
  + README.md
  + docs/milestones.md
  + this audit

relative Markdown links       = PASS
sensitive/local-path scan     = PASS
git diff --check              = PASS
```

这些 focused 结果只证明 docs-only 审计没有破坏它引用的当前冻结边界，不替代后继远端 Public CI、Browser
Smoke、受保护主线合入或 exact-main 匿名产品读回。

## 11. Fresh-Agent 交接与当前停止线

新的、没有聊天上下文的 Agent 应按以下顺序继续：

1. 读取 `README.md`、`AGENTS.md` 与文档 120、132、137、140、145、150、153、本文；
2. 从本文最终合入后的新 exact main 建立独立 docs-only contract worktree；
3. 先冻结四层 Fact identity/membership、reported-ID projection、diagnostic placement 与 terminal publication
   capability matrix；
4. 若需要修正文档 120/137/140/145/150，只修改被反例击穿的最小条款，不改变历史字节或用“latest wins”；
5. 合同未完成自己的门禁、受保护主线合入、exact-main 门与匿名产品读回前，不写 implementation allowed；
6. 不创建真实 parser、Provider SPI、FactSet/Evidence publisher、Relation、conflict/UNKNOWN、Slice、Coverage、
   COMPLETE Manifest、CLI 或 Workbench。

当前状态只能写成：

```text
R1_DERIVATION_EXECUTION_CELL_FROZEN
R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED
R1_FACT_EVIDENCE_CLOSURE_CONTRACT_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本审计找到了两个必须在下一合同前关闭的实质接缝：canonical diagnostic placement 与 terminal DIAGNOSTIC
publication authority/budget。它没有因此宣称 R1 上位架构错误，也没有授权任何新运行实现。
