# R1 DerivationEvidence Schema 0.1.1 修正合同

> 状态：`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@f69f2818d06834da0d9e8e95288f6f72aada6beb`
>
> 前置审计：[R1 DerivationEvidence Schema 修正前置审计](139-r1-derivation-evidence-schema-correction-audit.md)
>
> 上游冻结输入：[R1 Derivation Attempt 与 Fact Provenance 最小运行合同冻结发布](138-r1-derivation-provenance-contract-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文不创建或修改 Schema/corpus、identity vector、测试、
> runtime、Provider、parser、FactSet、DerivationEvidence Artifact、Relation、Slice、Coverage、Manifest、
> CLI、Workbench、Core、P/Q、CI、依赖、tag 或 Release

## 1. 目的与停止线

本文只冻结一个局部补丁版本的唯一生成规则：

```text
DerivationEvidence 0.1
    + two typed budget terminal causes
    + no dangling canonical IDs after non-success
    -> DerivationEvidence 0.1.1
```

它不授权本分支写 Schema。只有本文候选完成受保护主线闭环，并由后继独立 docs-only 状态发布明确写出
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTATION_ALLOWED`，才可从新的 exact main 物化补丁资源。

## 2. 三种版本身份必须分开

### 2.1 Artifact Schema version

新产生的 Evidence document 固定：

```json
"artifact_kind": "DERIVATION_EVIDENCE",
"schema_version": "0.1.1"
```

历史 document 继续自描述为 `0.1`，不得重写。

### 2.2 Schema resource identity

新 root Schema 唯一坐标固定为：

```text
path:
schemas/review-derivation-evidence-0.1.1.schema.json

$id:
https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.1.1.schema.json

title:
VeriTrail Review DerivationEvidence 0.1.1
```

它可以继续相对引用冻结的 `review-r1-common-0.1.schema.json`，但 `schema_version` 必须在新 root 中显式
固定为 `0.1.1`；不得修改 common Schema 让其他 R1 Artifact 意外接受补丁版本。

### 2.3 Semantic identity version

本补丁不改变 digest 算法或投影：

```text
domain  = veritrail.review.derivation-evidence/0.1
payload = DerivationEvidence with derivation_evidence_digest removed
```

`schema_version` 本来就在 payload 中，因此 `0.1` 与 `0.1.1` document 不会共享 semantic digest。保留 domain
表示 projection 没有变化，不表示 document bytes 或 Schema resource identity 相同。

## 3. 历史 `0.1` 保留合同

以下文件必须逐字节不变：

```text
schemas/review-derivation-evidence-0.1.schema.json
tests/fixtures/review-r1-schema-0.1/**
```

尤其不得：

- 在旧 enum 中追加 code；
- 在旧 root 中加入 `if/then`；
- 更新旧 COMPLETE Evidence 的 `schema_version`、digest 或 Manifest entry；
- 改写 `R1-CV-001..020`；
- 用“latest main 已修正”覆盖文档 126 记录的 exact bytes。

历史 `0.1` 的 Schema-valid 仍不自动等于当前 R1-conformant。后继 verifier 读取 `schema_version` 后选择对应
Schema resource，并继续执行当前冻结 conformance rules。

## 4. `0.1.1` 字段与闭集

除本节明确变化外，`0.1.1` 必须与 `0.1` 的字段、required set、closed objects、subject union、时间类型、
排序规则和 digest projection 同构。

`Diagnostic.diagnostic_code` 在旧闭集上只增加：

```text
EXECUTION_MEMORY_BUDGET
EXECUTION_ARTIFACT_BUDGET
```

不增加 peak memory、consumed bytes、deadline、自由文本、绝对路径、stack trace、attachment 或 staging path。

## 5. reported identity 的 Schema 不变量

### 5.1 run-local

新 Schema 必须直接拒绝：

```text
ProviderRun.execution_status in {INTERRUPTED, FAILED, UNAVAILABLE}
AND
(reported_fact_ids != [] OR reported_relation_ids != [])
```

`COMPLETED` run 可以合法报告排序唯一的 Fact/Relation IDs，也可以合法为空。

### 5.2 overall

新 Schema 还必须直接拒绝：

```text
DerivationEvidence.overall_execution_status in {INTERRUPTED, FAILED, UNAVAILABLE}
AND
any ProviderRun has non-empty reported_fact_ids or reported_relation_ids
```

该约束适用于 ProviderRun 自身仍为 `COMPLETED` 的情况。run status 是历史执行事实；reported arrays 是本份
Evidence 能安全解析到正式 Artifact 的 canonical identity summary。DIAGNOSTIC file set 没有普通
FactSet/RelationSet，因此两者不能被压成同一概念。

## 6. typed budget diagnostic 合同

### 6.1 positively observed memory stop

hard memory containment 的配置/readback 本身不授权该 diagnostic。只有 owned execution cell 的正向
memory-limit event 已被观察，并按后继冻结规则赢得 terminal-stop latch，才进入本节。OOM 文本、异常退出、
非零 exit code、accounting 接近上限或 completion message 缺失均不得反推 memory cause。

合法最小向量固定为：

```text
overall_execution_status = INTERRUPTED
active run.execution_status = INTERRUPTED
all reported arrays = []

run diagnostics contains exactly one:
  diagnostic_code = EXECUTION_MEMORY_BUDGET
  subject_ref.ref_kind = PROVIDER_RUN
  subject_ref.provider_run_id = active run.provider_run_id

top-level diagnostics contains the same typed tuple
```

这里的 `exactly one` 描述单变量 memory specimen 的 terminal diagnostic，不把 typed code 扩张成平台唯一
root-cause 证明。竞态选择、absolute deadline 与 cleanup release envelope 由
[Budget Primitive 合同](145-r1-derivation-budget-primitive-contract.md)冻结；当前 Schema 继续只保存胜出的正向
stop trigger，不保存 event chronology、peak memory 或轮询轨迹。

新 Schema 至少必须保证 code 只能与 `INTERRUPTED` 的本地/顶层状态组合，并要求 ProviderRun 层的 subject
shape 为 `PROVIDER_RUN`。conformance test 负责复核 subject ID 恰为同一 run。

### 6.2 artifact staging stop

合法最小向量固定为：

```text
overall_execution_status = INTERRUPTED
already terminal run remains COMPLETED
all reported arrays = []
run diagnostics does not contain EXECUTION_ARTIFACT_BUDGET

top-level diagnostics contains exactly one:
  diagnostic_code = EXECUTION_ARTIFACT_BUDGET
  subject_ref = null
```

新 Schema 必须禁止 artifact-budget code 出现在 ProviderRun diagnostics，并保证顶层出现该 code 时 overall
为 `INTERRUPTED`。当前 subject union 没有未发布 staging identity，故不得用输入 Artifact 或已完成 run 冒充。

### 6.3 不扩大旧 diagnostic 语义

本补丁不顺手重写 `SOURCE_* / PROVIDER_* / EXECUTION_DEADLINE / EXECUTION_CANCELLED /
INTERNAL_DERIVATION_ERROR` 的完整映射。它们继续受文档 120/137 与后继 conformance 约束。若未来反例证明
旧 code 也需要更强 Schema 条件，必须另开最小修正，不能借本补丁扩大范围。

## 7. 修正 payload 文件集

后继实现候选只允许增加或修改：

```text
schemas/review-derivation-evidence-0.1.1.schema.json
tests/fixtures/review-r1-derivation-evidence-0.1.1/README.md
tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json
tests/test_review_r1_derivation_evidence_schema_correction.py
tests/test_review_r1_schema_payload.py
candidate/freeze documentation and status pointers
```

其中 `tests/test_review_r1_schema_payload.py` 只可把当前公共 Schema 集分成“历史十文件 + 新 correction root”并
守住旧字节；不得重写旧二十项兼容义务。现有 `schema-test` extra 已固定 `jsonschema==4.25.1`，Public CI 已
通过 `python -m unittest -v` 自动发现 Core test，因此 `pyproject.toml` 与 workflow 必须保持不变。

## 8. correction corpus

新 namespace 固定为：

```text
R1-DE-CV-001..
```

`compatibility-cases.json` 至少包含以下稳定坐标：

| Case | 单变量义务 | 结果 |
| --- | --- | --- |
| `R1-DE-CV-001` | `0.1.1 / COMPLETED` run 报告规范 IDs | accept + digest recompute |
| `R1-DE-CV-002` | memory budget 合法向量 | accept + digest recompute |
| `R1-DE-CV-003` | artifact budget 合法向量 | accept + digest recompute |
| `R1-DE-CV-004` | non-COMPLETED run 带 fact ID | reject |
| `R1-DE-CV-005` | non-COMPLETED run 带 relation ID | reject |
| `R1-DE-CV-006` | non-COMPLETED overall 中 completed run 带 IDs | reject |
| `R1-DE-CV-007` | memory code 配 completed status | reject |
| `R1-DE-CV-008` | memory subject 指向其他 run/错误 kind | reject/conformance reject |
| `R1-DE-CV-009` | artifact code 放入 run diagnostics | reject |
| `R1-DE-CV-010` | artifact code 配非 interrupted overall 或非 null subject | reject |

三个正例必须保存完整 document、expected canonical UTF-8 bytes 与 expected
`derivation_evidence_digest`。负例必须从一个正例只改变一个语义变量；不得用缺字段、坏 JSON 或错误 hash
替代要证明的条件约束。

## 9. Manifest 与旧完整 fixture

本补丁不创建新的 Manifest outcome，也不修改 `review-derivation-manifest-0.1.schema.json`。测试可以构造一个
DIAGNOSTIC manifest specimen 来证明四文件布局和 corrected Evidence byte binding，但该 specimen 只能位于
新 correction corpus，不能回写旧九文件 COMPLETE bundle。

Manifest `schema_version = 0.1` 继续描述 Manifest 自身 shape；每个 Artifact 由自己的 `artifact_kind +
schema_version` 自描述。Manifest entry 的 `sha256 + semantic_digest` 绑定具体 corrected Evidence，不把不同
Evidence Schema 版本视作同一文件。

## 10. request provenance 与 Provider applicability

新 Schema 继续保留通用 `RequestProvenance` shape，不把 `requested_ref` 限制为 exact OID pattern。首个 runtime
必须按文档 137 从 owned Snapshot 复算 exact OID、固定 resolver id/version，并由 conformance test 验证；未来
alias-aware resolver 仍可使用同一 Evidence Artifact family。

同理，本补丁不验证 Provider 是否来自显式 binding、Policy 是否恰有一个 required cumulative `python-ast`
requirement，或 Fact 是否与 run 双向闭合。这些属于后继 runtime/complete-bundle conformance，不是单文件
Schema authority。

## 11. 实现验证门

后继 correction implementation 至少需要：

1. old `0.1` Schema/corpus 所有冻结文件 SHA-256 逐项不变；
2. old 22 项 focused test 原义继续通过；
3. 新十项 correction corpus 在 Python 3.10/3.13、normal/`-O` 下产生相同结果；
4. 两个新 diagnostic 的 canonical bytes/digest 在四个 runner mode 一致；
5. base Core wheel 不新增 `jsonschema` runtime dependency；
6. 完整 Core、GitHub Evidence、Review Attention、Starter、Authoring Skill 与 Workbench 回归按当前 CI 边界通过；
7. 候选 PR 原始 required checks、受保护主线合入、新 exact-main 门与匿名 Schema/corpus byte readback成立；
8. 后继独立 docs-only 状态发布完成自己的最后门。

第一次失败、资源停止或无终态命令必须保留，不能通过 rerun 改名为未发生。16GB 宿主继续串行执行高内存
lane，不以并行压测制造 Q 的虚假证据。

## 12. 实现后仍禁止

即使 correction payload 最终冻结，也不自动授权：

```text
budget primitive
Provider runtime / real parser
canonical Fact production
FactSet / DerivationEvidence publication
Relation / conflict / UNKNOWN propagation
Slice / Coverage
COMPLETE or DIAGNOSTIC runtime Manifest publication
CLI / Workbench / Core handoff
Q / D / JPyxis work
tag / Release
```

下一步只能是独立 budget primitive feasibility；只有其成立且后继明确发布 runtime authorization 后，才可开始
文档 137 的 Provider/Fact phase implementation。

## 13. 候选最后门

本文只有完成以下事实才有资格被冻结：

1. diff 仍为 docs-only，且没有 Schema/corpus/test/runtime 施工；
2. 文档链接、状态、版本身份、consumer matrix 与停止线一致；
3. 本地 docs/static gate 和受影响回归成立；
4. 候选 PR 原始 Public CI required checks 全部成功；
5. 只经受保护主线合入；
6. 新 exact main Public CI 与 Browser Smoke 成立；
7. README、本文、审计与 milestones 的 fresh anonymous exact-SHA 读回成立；
8. 后继独立 docs-only 冻结发布完成最后门。

候选阶段只能写：

```text
R1_DERIVATION_EVIDENCE_SCHEMA_PRECONTRACT_AUDITED
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

任一新反例都可以否决候选或只重开被击穿的最小边界。候选合入本身不等于 correction implementation 已获
授权，也不能把本地/PR 绿灯传播给后继 Schema bytes。
