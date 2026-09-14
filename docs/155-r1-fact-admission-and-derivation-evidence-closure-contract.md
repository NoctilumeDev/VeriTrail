# R1 Fact Admission / DerivationEvidence Closure 最小合同 0.1

> 状态：`R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED /
> R1_FACT_EVIDENCE_CLOSURE_CONTRACT_CANDIDATE /
> R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@0b2ca79191adc3743b2cf4663cd0cda7574a7912`
>
> 前置审计：[R1 Fact Admission 与 DerivationEvidence Closure 系统审计](154-r1-fact-evidence-closure-system-audit.md)
>
> 上游冻结输入：[R1 Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Derivation Attempt 与 Fact Provenance 合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)、
> [DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)、
> [Derivation Budget Primitive 合同](145-r1-derivation-budget-primitive-contract.md)、
> [Execution Cell / Terminal Envelope 合同](150-r1-derivation-execution-cell-terminal-envelope-contract.md)与
> [Execution Cell 实现冻结发布](153-r1-derivation-execution-cell-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`；本文只冻结 Fact membership、
> final Evidence projection、diagnostic placement 与 terminal publication capability，不创建或修改 runtime、
> Schema、corpus、identity vector、测试、Provider、parser、FactSet/Evidence publisher、Relation、Slice、
> Coverage、Manifest、CLI、Workbench、Core、P/Q/D、依赖、CI、tag 或 Release

## 1. 目的与停止线

Execution Cell 已经能返回 copy-owned、non-published phase result；其中成功 Fact 已由 application 复算
canonical identity，失败路径已由 controller 收敛为 typed terminal facts。该结果还不是 FactSet membership、
DerivationEvidence 或公共 R1 Artifact。

本文只关闭下一条最小接缝：

```text
same integrated controller
  owns DerivationInputSet + BudgetContext + attempt eligibility
        ↓
consume one immutable Execution Cell phase result
        ↓
application-canonical Fact admission
        ↓
owned, non-published FactSet construction state
        +
owned final-outcome Evidence projection
        ↓
explicit normal / diagnostic / cleanup capability boundary
```

本文不定义输出目录或公共 publisher，也不发布 `fact-set.json`、`derivation-evidence.json` 或
`manifest.json`。即使本合同以后冻结，首个获授权实现也只能建立内存中的 admission/projection 与
conformance matrix；真实 Python parser、Provider SPI、Relation、conflict/UNKNOWN、Slice、Coverage、
COMPLETE Manifest 与公共 Artifact publication 继续禁止。

## 2. 四层 Fact 身份与 membership

四层继续严格分开：

```text
Provider candidate observation
  Provider 对 owned source bytes 的一次有界报告；无 canonical ID authority

application-canonical Fact
  application 已复算 subject_key_digest / fact_id 的规范源码事实

admitted FactSet member
  通过 derivation-level identity、排序、去重与双向 provenance 后，
  被 owned FactSet construction state 接纳的成员

published Fact Artifact member
  被 COMPLETE 八文件目录与 exact Manifest file identity 共同绑定的成员
```

因此：

```text
candidate returned                != canonical Fact
canonical Fact identity valid     != FactSet membership
FactSet construction state closed != FactSet published
FactSet published                 != R1 derivation COMPLETE
```

本文只到第三层。第四层必须等待 RelationSet、ReviewSliceSet、CoverageLedger 与完整八文件 publication
合同共同成立，不能用 standalone FactSet、placeholder downstream Artifact 或第三种 Manifest outcome 提前实现。

## 3. Integrated controller 与同一预算连续性

现有 `run_closed_test_execution_cell(...)` 是组件证明入口，不是 full-derivation continuation API。后继实现必须
在调用 execution phase **以前**由一个新的 trusted integrated controller 拥有：

```text
owned DerivationInputSet
opaque derivation_id
copy-owned Provider binding
one BudgetContext
one attempt eligibility gate
```

controller 直接消费同一次调用返回的 immutable phase value；不得重新读取 transport、Provider state、输入路径
或临时文件，也不得调用 standalone phase 后另建 BudgetContext 冒充同一 derivation。

raw `BudgetContext`、eligibility gate 与 mutable construction state 都不得越过 controller boundary。Provider、
worker 与外部调用方不能取得 artifact reservation、Evidence projection 或 phase continuation authority。

本合同不要求改写冻结的 standalone API。首个实现可以抽取 private composition primitive，并让 standalone
入口与 integrated controller 分别在各自边界调用它；二者不能通过序列化 phase result、隐藏 checkpoint 或
新的完整 timeout 拼接。

## 4. Fact admission

### 4.1 admission 前置条件

只有同时满足以下条件才允许开始 FactSet admission：

```text
phase_status = COMPLETED
ProviderRun status = COMPLETED
release_outcome = RELEASED
attempt eligibility remains ADMITTED
BudgetContext remains RUNNING
no terminal-stop latch exists
phase canonical Facts and reported IDs are copy-owned
```

非成功 phase、release failure、已锁存 stop 或被 revoke 的 eligibility 不能进入“空 FactSet”路径。失败不是空成功。

### 4.2 机械闭包

admission 必须针对同一 owned phase values 重新验证：

1. `derivation_id`、request provenance、五个 input semantic digest、Provider descriptor、
   `operands_digest` 与 `provider_run_id` 与 admitted attempt 完全连续；
2. 每个 Fact 的 `source_snapshot_digest / derivation_profile_digest`、anchor path、scope 与 exact owned input 一致；
3. 每个 Fact 的 `subject_key_digest / fact_id` 由冻结 Profile 与 identity domain 复算成立；
4. 每个 Fact 的 `provenance_refs` 恰为 `[provider_run_id]`；
5. `facts` 按 `fact_id` 排序，相同 ID 只保留一个 byte-identical semantic member；
6. `ProviderRun.reported_fact_ids` 恰等于 admitted Fact ID 的排序唯一全集；
7. `reported_relation_ids=[]`；
8. single-Provider 首版不制造 multi-source conflict，`conflicts=[]`；
9. `fact_set_digest` 严格按文档 120 的 provenance-free projection 复算；
10. 完整 FactSet document 的规范 bytes 由 owned value 一次建立，并使用文档 120 冻结的
    `canonical_json_bytes(document) + LF` 文件字节规则；调用方不能原地修改。

同一 Provider 对同一 subject 返回不兼容 candidate 已由 Execution Cell 作为
`NONCONFORMANT_PROVIDER_OUTPUT` fail closed；Fact admission 不能把它重新解释为首个 conflict。成功空输出形成：

```text
ProviderRun = COMPLETED
facts = []
conflicts = []
reported_fact_ids = []
```

它是已执行且为空的来源事实，不是 `UNAVAILABLE`、`UNKNOWN` 或 Coverage COMPLETE。

### 4.3 owned construction state

成功 admission 形成 private、copy-owned、non-published construction state，至少拥有：

```text
exact input semantic digests
one immutable ProviderRun phase projection
canonical Fact values
canonical FactSet document value
canonical FactSet bytes
fact_set_digest
normal-continuation eligibility reference
```

它没有路径、Manifest role、公共生命周期或 standalone publication authority。`canonical FactSet bytes` 表示未来
完整 assembler 若获授权，应消费的 exact bytes；当前不会调用 artifact reservation，也不会把这些内存 bytes
计为已发布 Artifact。

## 5. Phase summary 与 final Evidence projection

phase result 和 final `DerivationEvidence` 是两个 immutable projection，不能原地改写或盲拷：

```text
phase reported IDs
  = 本 phase 曾经 application-canonicalize 并成功提交的 identities

final Evidence reported IDs
  = 本次最终发布的 normal FactSet/RelationSet 中可解析的 identities
```

机械规则固定为：

```text
future final outcome = COMPLETE
  -> ProviderRun.reported_fact_ids must resolve exactly once in published FactSet
  -> ProviderRun.reported_relation_ids must resolve exactly once in published RelationSet
  -> reverse provenance closure must also hold

final outcome in {INTERRUPTED, FAILED, UNAVAILABLE}
  -> every ProviderRun.reported_fact_ids = []
  -> every ProviderRun.reported_relation_ids = []
```

因此一个 phase 可以保留 `ProviderRun = COMPLETED` 与非空 phase IDs，而后继失败形成的 final Evidence 仍保留
该 run status、但必须清空全部 final reported arrays。清空不是抹除历史；它声明 DIAGNOSTIC file set 没有正常
Fact/Relation Artifact 可供这些 ID 解析。

当前 success 路径只建立 FactSet construction state，不建立“临时 COMPLETED DerivationEvidence”。最终
COMPLETED Evidence 必须等待 Relation/Slice/Coverage 与八文件 closure 一次形成；不得先生成再原地修补。

## 6. Canonical diagnostic placement

Schema 继续只验证 shape；本节冻结首个 single-Provider Fact phase 的跨对象 conformance。数组仍按
`(diagnostic_code, canonical_json_bytes(subject_ref))` 排序并在每个数组内去重。

### 6.1 admitted active run 的 terminal facts

以下 code 都绑定当前 exact `provider_run_id`，并沿用文档 137/150 已冻结的状态映射：

| Diagnostic code | ProviderRun status | Evidence overall status |
| --- | --- | --- |
| `PROVIDER_UNAVAILABLE` | `UNAVAILABLE` | `UNAVAILABLE` |
| `PROVIDER_FAILED` | `FAILED` | `FAILED` |
| `NONCONFORMANT_PROVIDER_OUTPUT` | `FAILED` | `FAILED` |
| `INTERNAL_DERIVATION_ERROR` | `FAILED` | `FAILED` |
| `EXECUTION_DEADLINE` | `INTERRUPTED` | `INTERRUPTED` |
| `EXECUTION_CANCELLED` | `INTERRUPTED` | `INTERRUPTED` |
| `EXECUTION_MEMORY_BUDGET` | `INTERRUPTED` | `INTERRUPTED` |

当其中一个 code 成为本 phase 的唯一 terminal classification 时，canonical placement 固定为：

```text
ProviderRun.diagnostics contains exactly once:
  {diagnostic_code: <code>,
   subject_ref: {ref_kind: PROVIDER_RUN, provider_run_id: <exact run>}}

top-level diagnostics contains the same tuple exactly once
```

run-local tuple 回答“哪次 ProviderRun 被分类”；top-level tuple 回答“哪项 terminal fact 决定本次 Evidence
outcome”。两处是同一事实的两个规范投影，不是两个根因或两次事件。run-only、top-only 与 duplicated tuple
都不是 canonical Evidence，即使 JSON Schema 接受其形状。

### 6.2 artifact staging stop

`EXECUTION_ARTIFACT_BUDGET` 不归因给已经终止的 ProviderRun：

```text
ProviderRun.diagnostics contains no EXECUTION_ARTIFACT_BUDGET

top-level diagnostics contains exactly once:
  {diagnostic_code: EXECUTION_ARTIFACT_BUDGET, subject_ref: null}
```

已经 `COMPLETED` 的 run status 不反写；Evidence overall status 为 `INTERRUPTED`，final reported arrays 全部清空。

### 6.3 pre-admission source/input failure

当前 exact-only Input Binding 在 attempt admission 前处理 source object/content mismatch。没有合法
Derivation Attempt 或 ProviderRun 时，不创建 DerivationEvidence，也不存在 diagnostic placement。
`SOURCE_OBJECT_MISSING / SOURCE_CONTENT_MISMATCH` 继续保留在通用 Schema 词汇中，但首个 reference runtime
不得为了使用该 code 而伪造 attempt。未来 alias-aware resolver 若要在 admission 后产生这些 code，必须另开
合同冻结 subject 与 cardinality。

## 7. 三种能力不能合并

```text
normal continuation eligibility
  允许后继正常 Relation/Slice/Coverage 与 COMPLETE closure 工作

diagnostic closure eligibility
  只允许从已验证 non-success phase facts 形成固定四文件 DIAGNOSTIC closure

cleanup-only permission
  只允许终止/释放 owned process、channel、handle 与 staging residue
```

它们不是一个 boolean。任一时刻只能按冻结状态进入对应动作；cleanup 成功不恢复 normal 或 diagnostic
eligibility，diagnostic eligibility 也不能启动 Provider、parser、Relation、Slice 或 Coverage。

normal path 在 Fact admission 成功后继续使用同一 RUNNING BudgetContext；本合同只返回 construction state，
不执行后继阶段。non-success path 先不可恢复地 revoke normal eligibility，并完成 execution-cell resource release；
只有第 8 节明确允许的 execution-cell non-success，才能在 release 成功后取得一次性的 diagnostic closure
eligibility。

## 8. Terminal capability matrix

首个 reference runtime 的 capability matrix 固定如下。`Eligible` 只表示未来 publisher 合同可以消费该资格；
本文没有定义输出坐标，也不授权公共 publication。

| Terminal class | Normal continuation | Diagnostic closure eligibility | Cleanup | 当前公共 R1 Artifact |
| --- | --- | --- | --- | --- |
| pre-admission request/input/runtime failure | no attempt | none | provisional resources only | none |
| Fact phase `COMPLETED` + admission closed | eligible | none | phase resources already closed | none；等待完整 derivation |
| `PROVIDER_UNAVAILABLE` | revoked | eligible under §8.1 | required before eligibility | none in this slice |
| `PROVIDER_FAILED` | revoked | eligible under §8.1 | required before eligibility | none in this slice |
| `NONCONFORMANT_PROVIDER_OUTPUT` | revoked | eligible under §8.1 | required before eligibility | none in this slice |
| `INTERNAL_DERIVATION_ERROR` with a returned phase result | revoked | eligible under §8.1 | required before eligibility | none in this slice |
| `EXECUTION_DEADLINE` | revoked | none | cleanup-only | none |
| `EXECUTION_CANCELLED` | revoked | none | cleanup-only | none |
| `EXECUTION_MEMORY_BUDGET` | revoked | none | cleanup-only | none |
| `EXECUTION_ARTIFACT_BUDGET` | revoked | none | cleanup-only | none |
| `RELEASE_FAILED` / no valid phase result | revoked | none | failed | none |

### 8.1 diagnostic eligibility 的全部条件

有合法 phase result、且没有预算 stop 的 execution-cell non-success，只有同时满足以下条件才形成一次性
eligibility：

```text
attempt was admitted
one valid copy-owned non-success phase result exists
phase diagnostic placement is canonical
execution-cell release outcome = RELEASED
BudgetContext state remains RUNNING
execution deadline has not been reached
no cancellation/memory/artifact stop latch exists
reserved_artifact_bytes = 0
normal continuation eligibility is revoked
```

这份 eligibility 不是 Artifact，也不进入 Evidence identity。它只能被同一 integrated controller 消费一次；
任何新的 stop、deadline、reservation、projection failure 或 publisher failure 都会使其永久失效。不得通过重建
BudgetContext、释放既有 reservation、增加第二份预算或新 `derivation_id` 继续称为同一 attempt。

### 8.2 为什么 terminal stop 不发布

deadline、caller cancellation、positive memory stop 与 artifact reservation stop 已使 BudgetContext 离开
`RUNNING`，后继只有 cleanup-only permission。reference runtime 不会在 stop 后为“记录 stop”重新授予
Artifact work；即使 Schema/corpus 能表达该 DIAGNOSTIC，也只证明 shape/identity capability。

因此：

```text
terminal stop observed
  -> cleanup and calling-layer typed result
  -> no R1 Artifact
```

这不是丢弃一份本来已经发布的 Evidence，而是拒绝把未获预算授权的 bytes 伪装成合法 Bundle。

## 9. Future DIAGNOSTIC closure 的唯一预算语义

后继独立 publisher 合同若消费 §8.1 eligibility，只能：

1. 使用同一个仍为 `RUNNING` 的 BudgetContext 与剩余 absolute deadline；
2. 从 owned input exact bytes 与 final non-success Evidence projection 构造固定四文件 bytes；
3. 在打开任何 staging file 前计算四个文件的 exact bytes；
4. 按 Manifest role rank 对全部 regular-file bytes 逐项执行现有 inclusive artifact reservation；
5. 任一 reservation 被拒绝时锁存 `EXECUTION_ARTIFACT_BUDGET`、不打开下一文件、清理 staging，并发布 nothing；
6. 所有 reservation 成功后才 create-new 写入 owned staging，复算 file/semantic digest 与 cross-reference；
7. 在同一 execution deadline 内原子 create-new 发布完整目录；
8. 任一 write/verify/publish failure 清理 staging 并发布 nothing。

不能先把三份输入复制到 staging 再猜 Manifest 是否还能放下；也不能删除 normal staging 后“退还”计数、另写
更小 DIAGNOSTIC。首版只有 `reserved_artifact_bytes=0` 的 eligible execution-cell non-success 可以取得
eligibility，
因此不会产生 reservation rollback 语义。

本文只冻结未来 publisher 必须遵守的能力/预算边界，不冻结 output path、public API、错误对象或实现布局。
这些坐标未定义以前，首个实现不得实际写出四文件目录。

## 10. DerivationEvidence projection

### 10.1 non-success final projection

§8.1 的 eligible phase result 可以形成 owned、non-published `DerivationEvidence 0.1.1` value：

```text
exact derivation_id and request_provenance from phase
five input semantic digests from admitted inputs
exactly one ProviderRun
run/overall status mechanically derived from terminal class
controller-owned phase timing
all reported arrays = []
canonical diagnostics from §6
derivation_evidence_digest recomputed from the complete projection
```

`started_at` 使用 admitted attempt 的开始时间；ProviderRun 起止与 `finished_at` 使用 phase result 已拥有的
controller observations。Evidence projection 不重读时钟、worker、path 或日志，也不发明 publication timestamp。

### 10.2 success path 不提前形成 final Evidence

Fact phase 成功时只保存 phase run facts 与 FactSet construction state。因为后继 Relation/Slice/Coverage 仍可能
失败或停止，当前不能决定 final overall status、reported relation IDs、diagnostics 或 Manifest outcome。

因此不得建立可被外部误读的 provisional `COMPLETED DerivationEvidence`，也不得在后继失败时原地清空 IDs。
完整 assembler 必须等 final outcome 已知后新建 final Evidence projection。

## 11. Schema 与既有合同裁决

本合同不升级任何公共 Schema 或 semantic digest domain：

- FactSet 0.1 已能表达首个 single-Provider `facts + conflicts=[]`；
- DerivationEvidence 0.1.1 已直接拒绝 non-completed overall/run 携带 reported IDs；
- canonical diagnostic placement 是跨对象 conformance，不是 shape；
- Manifest 0.1 已区分 COMPLETE 八文件与 DIAGNOSTIC 四文件；
- runtime publication authority 不应通过给 Schema 新增字段来伪装。

本文只对文档 120、145 与 150 中被审计 154 暴露的 residual wording 做最小一致性修正：Manifest shape
不自动授予 publication，cleanup-only envelope 不允许任何 DIAGNOSTIC staging。历史 Schema/corpus/vector
字节与 digest 不变；不得把“现有 Schema 接受”写成当前 reference runtime 已能发布。

## 12. 最小 conformance matrix

后继获授权实现至少逐格证明：

| ID | 单变量义务 | 预期 |
| --- | --- | --- |
| FA-001 | completed phase + one canonical Fact | one owned admitted Fact；无文件 |
| FA-002 | completed phase + empty candidate set | completed empty FactSet construction state |
| FA-003 | duplicate byte-identical Fact ID | one member；provenance 仍恰为该 run |
| FA-004 | Fact anchor/input/profile/ID 任一漂移 | admission reject；normal eligibility revoke；无 Artifact |
| FA-005 | run 漏报 admitted Fact | bidirectional closure reject |
| FA-006 | run 报告不存在 Fact | bidirectional closure reject |
| FA-007 | single Provider 同 subject 不兼容 Fact | 不生成 conflict；nonconformant failure |
| FA-008 | phase result mapping 被调用方修改 | owned values/bytes 不变 |
| FA-009 | FactSet locally valid 后尝试 standalone publication | public API 无此能力；零文件 |
| FA-010 | completed phase 后模拟 downstream failure | phase run status/IDs 不变；new-copy final Evidence IDs 清空 |
| FA-011 | `PROVIDER_UNAVAILABLE` | run+top same tuple exactly once；eligible diagnostic closure |
| FA-012 | `PROVIDER_FAILED` | run+top same tuple exactly once；eligible diagnostic closure |
| FA-013 | `NONCONFORMANT_PROVIDER_OUTPUT` | run+top same tuple exactly once；eligible diagnostic closure |
| FA-014 | valid `INTERNAL_DERIVATION_ERROR` phase | run+top same tuple exactly once；eligible diagnostic closure |
| FA-015 | deadline/cancel/memory active-run stop | canonical run+top projection；no diagnostic publication eligibility |
| FA-016 | artifact reservation stop | top-only/null subject；no second reservation or publication |
| FA-017 | release failure | no phase/Evidence closure and no Artifact |
| FA-018 | Provider failure 但 BudgetContext stopped/expired | no diagnostic eligibility |
| FA-019 | Provider failure 但 existing artifact reservation 非零 | no diagnostic eligibility |
| FA-020 | run-only/top-only/run+top duplicated diagnostic variants | Schema may accept shape；conformance rejects noncanonical projection |
| FA-021 | two sufficient runtime budgets | same FactSet semantic bytes/digest except truthful run provenance |
| FA-022 | standalone Execution Cell result + new BudgetContext | reject as a new attempt; cannot continue same derivation |
| FA-023 | CPython 3.10/3.13 normal/`-O` | deterministic admission/projection bytes and decisions agree |
| FA-024 | output path / publisher / manifest probe | no public parameter or file output in first implementation |

FA-021 比较 provenance-free FactSet semantic projection 与 `fact_set_digest`；不同 `provider_run_id` 会使完整 FactSet
file bytes 不同，这是诚实 provenance，不是 budget identity pollution。

## 13. 实现分段与停止线

本合同只有完成候选远端门、受保护主线合入、exact-main 门、fresh anonymous public readback 与后继独立
docs-only 冻结发布后，才可以按顺序实现：

```text
A. private integrated-controller composition boundary
B. application-canonical Fact admission and FactSet construction state
C. immutable phase-vs-final ProviderRun projection
D. canonical diagnostic placement / cardinality conformance
E. owned non-published DerivationEvidence projection
F. FA-001..024 hardening
```

首个实现不得包含 output path、artifact writer、Manifest、real parser、public Provider SPI、Relation、
conflict/UNKNOWN、Slice 或 Coverage。完成 F 也只得到 non-published closure；后继若要发布 DIAGNOSTIC，必须
另开 publisher 合同补齐 output coordinate、create-new boundary、错误模型与真实 artifact-budget proof。

## 14. 候选验收与冻结序列

本文只有满足以下条件才有资格进入冻结发布：

1. 文档 154 的十八个反例逐项有唯一裁决；
2. 四层 Fact identity/membership 不再共用一个“canonical admission”概念；
3. phase IDs、final Evidence IDs 与 published Artifact membership 保持三种投影；
4. 七个 active-run terminal code 与 artifact-budget code 的 placement/cardinality 没有实现自由度；
5. normal continuation、diagnostic closure 与 cleanup permission 不再共用 eligibility；
6. artifact stop 后没有第二预算、reservation rollback 或 DIAGNOSTIC staging 路径；
7. Schema/corpus/vector 字节与 digest projection 保持不变有充分理由；
8. diff 只有本文、必要的旧合同 residual wording 与状态入口文档；
9. 本地 Markdown、状态、敏感、双 Python normal/`-O` 及适用回归成立；
10. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
11. 新 exact main Public CI、Browser Smoke 与 README/本文/milestones 的 fresh anonymous 产品读回成立；
12. 后继独立 docs-only 状态发布完成同样最后门。

只有第 12 项完成后，才可写：

```text
R1_FACT_EVIDENCE_CLOSURE_CONTRACT_FROZEN
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_ALLOWED
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该授权只覆盖第 13 节 A–F；不传播给 public publisher、parser、Provider discovery、Relation、Slice、Coverage、
COMPLETE Manifest、CLI 或 Workbench。

## 15. 当前候选裁决与 Fresh-Agent 交接

当前只能写：

```text
R1_DERIVATION_EXECUTION_CELL_FROZEN
R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED
R1_FACT_EVIDENCE_CLOSURE_CONTRACT_CANDIDATE
R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

新的、没有聊天上下文的 Agent 必须先读文档 120、132、137、140、145、150、153、154 与本文，然后只审计
这些合同能否同时成立。不得把 `CONTRACT_CANDIDATE` 解释为 implementation authorization，不得因为本文定义
了 future DIAGNOSTIC eligibility 就创建 output path/publisher，也不得因 FactSet bytes 已在内存中闭合就发布
standalone Artifact。

任一新反例都可以否决候选或只重开被击穿的最小边界。门禁全绿不能覆盖新的组合语义冲突；反之，发现
延期问题也不自动要求扩大当前合同。

## 16. 本地候选证据

候选完成后，从同一 worktree、同一 source coordinate 串行执行本地门禁：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| R1 Schema / identity / Evidence 0.1.1 normal | `27/27` | `27/27` |
| R1 Schema / identity / Evidence 0.1.1 `-O` | `27/27` | `27/27` |
| Review Attention complete regression normal | `113/113`（266.096 s） | `113/113`（262.394 s） |
| Review Attention complete regression `-O` | `113/113`（268.466 s） | `113/113`（261.252 s） |

relative Markdown links、fence/heading structure、状态 marker、变更范围、敏感/个人路径扫描与
`git diff --check` 均成立。diff 只有本文、README/AGENTS/milestones 入口，以及文档 120/145/150 被审计
154 击穿的最小 residual wording；没有 runtime、Schema、corpus、vector、测试、依赖、CI 或发布文件变化。

第一次完整插件回归启动错误地使用了过短的外层工具执行窗口；外层在 5.08 秒超时并留下仍在运行的 exact
Python 3.10 child。该进程按 PID、命令行与当前 worktree 确认后被终止，子进程残留复核为空；该次尝试不构成
产品失败，也不进入通过证据。表中四格均由后继 fresh process、独立空日志、exact interpreter 与 exact
worktree 重新建立。
