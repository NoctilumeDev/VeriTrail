# R1 DerivationEvidence Schema 修正前置审计

> 状态：`R1_DERIVATION_EVIDENCE_SCHEMA_PRECONTRACT_AUDITED /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_NOT_FROZEN /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@f69f2818d06834da0d9e8e95288f6f72aada6beb`
>
> 上游冻结输入：[R1 Derivation Attempt 与 Fact Provenance 最小运行合同冻结发布](138-r1-derivation-provenance-contract-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L0_DOCUMENTATION`；本文不修改冻结 Schema/corpus、identity vector、
> runtime、Provider、parser、FactSet、DerivationEvidence Artifact、Relation、Slice、Coverage、Manifest、
> CLI、Workbench、Core、P/Q、CI、依赖或发布坐标

## 1. 审计问题

文档 137/138 已经只授权下一步修正两个局部语义：

```text
DerivationEvidence 缺少 memory/artifact budget typed diagnostic

non-COMPLETED run / overall derivation
    -> no reported canonical Fact/Relation identity
```

本轮不问怎样写 Provider 或 parser，而问：

> 已公开冻结的 `DerivationEvidence 0.1` 怎样接受必要修正，同时不覆盖原 Schema 身份、不回写历史
> COMPLETE specimen，也不让修正过程替未来 runtime 决定额外语义？

## 2. 冻结输入与当前消费者

### 2.1 已公开冻结的字节

文档 126 已将以下对象作为 exact-main 可寻址事实公开冻结：

```text
schemas/review-derivation-evidence-0.1.schema.json
SHA-256 = 2efbd1d4f73f20fb045c2110136e7f3089e07408b9d496f59c30492a2c3666e7

tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-evidence.json
SHA-256 = 563664e5675cb861c7c22d4017c97d186a7e370bca4851dbf7bb09df49afb555

tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-31.json
SHA-256 = a5f66942a218870d7b4a236244e768ae234a00c5b3cb4c1c1ae3810395cecd48
```

旧 Schema 的 `$id` 也是它自己的公共资源身份。Git 历史能保留旧字节，不等于当前主线可以在相同
`path + $id + version` 下静默发布另一种验证语言。

### 2.2 消费者矩阵

| 消费者 | 当前依赖 | 本次修正允许的影响 |
| --- | --- | --- |
| 历史 `0.1` Schema/corpus | 已冻结的十个 Schema、十九个 corpus 文件与完整 COMPLETE bundle | 必须逐字节保持不变 |
| `tests/test_review_r1_schema_payload.py` | 证明旧 payload 的结构、身份与二十项兼容义务 | 旧证明必须继续成立；后继测试只能显式识别新增修正资源 |
| SourceSnapshot/Input runtime | 只消费 Snapshot/Policy/Profile 与 exact Git bytes | 不应受影响 |
| 未来 Derivation runtime | 需要两个新 diagnostic 与非成功 ID 约束 | 修正冻结后必须选择新 Evidence Schema 身份 |
| Derivation Manifest | 只绑定实际 Evidence 文件字节与 semantic digest | 本轮不修改 Manifest Schema/file set/outcome |
| Core、P、Q、Workbench | 不理解 R1 DerivationEvidence 内部语义 | 零实现依赖、零 authority 变化 |

当前仓库尚无 DerivationEvidence runtime consumer。这个零迁移窗口允许增加一个窄补丁版本，但不允许假装
旧公开资源从未存在。

## 3. 可复现的当前反例

在 exact 审计基线上，现有 22 项 Schema/conformance 测试通过；这只证明旧合同被稳定实现。直接从已冻结
COMPLETE Evidence 构造单变量变体，当前 Schema 得到：

| 变体 | 当前结果 | 应有语义 |
| --- | --- | --- |
| Provider Run 改为 `FAILED`，保留 non-empty reported IDs | `ACCEPTED` | 拒绝 |
| overall 改为 `INTERRUPTED`，COMPLETED run 保留 IDs | `ACCEPTED` | 拒绝 |
| 增加 `EXECUTION_MEMORY_BUDGET` | `REJECTED` | 新补丁版本应接受合法形状 |
| 增加 `EXECUTION_ARTIFACT_BUDGET` | `REJECTED` | 新补丁版本应接受合法形状 |

这证明：

```text
Old tests green
    !=
New frozen provenance invariant expressible
```

### 3.1 相邻但不属于本次修正的现象

旧 Schema 也会接受 friendly `requested_ref`。这不是本次 Schema 缺口：文档 120 的通用
`RequestProvenance` 明确允许未来 alias-aware resolver；文档 137 只是把首个 runtime 收窄为 exact OID。
因此 exact request provenance 必须由后继 runtime conformance 验证，不能为了本次预算修正把通用
`RequestProvenance` 永久缩成 exact-only。

## 4. 版本身份反例

### 4.1 不能原位改写 `0.1`

若直接编辑现有文件：

```text
same path
same $id
same title/version
different accepted language
different public bytes
```

则两个不同 Schema resource 共享同一个规范身份。依赖 exact commit 的读者仍能找到历史字节，但依赖 `$id`
或默认主线 URL 的 registry/cache 无法区分。这会把“Git 历史可恢复”误写成“Schema 身份没有变化”。

### 4.2 不需要把整个 R1 升级为 `0.2`

本次不增加 Evidence 字段，不改变 canonicalization profile、semantic digest projection、ProviderRun identity、
其他八种 Artifact 或 Manifest shape。整体升级十个 Schema 会把一个 Evidence 局部修正扩散成整个 R1
payload 迁移。

### 4.3 最小身份边界

审计选择：

```text
Historical DerivationEvidence Schema resource
    = review-derivation-evidence-0.1.schema.json

Corrected DerivationEvidence Schema resource
    = review-derivation-evidence-0.1.1.schema.json

Historical Evidence document
    schema_version = 0.1

New runtime Evidence document
    schema_version = 0.1.1
```

`0.1.1` 是 DerivationEvidence Artifact 的补丁版本，不是 R1 全家桶的新版本。旧 Schema、fixture 与向量不
修改；新 Schema 使用新的 path、`$id`、title 与 document `schema_version`。Manifest 自己的
`schema_version = 0.1` 仍只表示 Manifest shape，子 Artifact 继续通过自身字段自描述。

## 5. Schema 与 conformance 的责任分配

### 5.1 Schema 可以直接证明

Draft 2020-12 条件约束足以表达：

```text
ProviderRun.execution_status != COMPLETED
    -> reported_fact_ids.maxItems = 0
    -> reported_relation_ids.maxItems = 0

DerivationEvidence.overall_execution_status != COMPLETED
    -> every ProviderRun reported array has maxItems = 0
```

新 diagnostic 的闭集、Artifact budget code 不得出现在 ProviderRun diagnostics、以及新 code 对
`INTERRUPTED` 状态的局部蕴含也可由 Schema 表达。

### 5.2 conformance test 仍必须证明

JSON Schema 不负责跨数组引用和完整 derivation 历史。测试仍须证明：

- memory diagnostic 指向 Evidence 内真实且 active 的同一 `provider_run_id`；
- artifact diagnostic 发生在 run 已终止后的 staging 层，不能反写历史 run status；
- diagnostic 数组满足冻结排序与去重规则；
- Evidence semantic digest 使用原 `veritrail.review.derivation-evidence/0.1` projection 复算；
- DIAGNOSTIC Manifest 精确绑定同一份 corrected Evidence bytes，且不携带 Fact/Relation/Slice/Coverage；
- COMPLETE bundle 中 run/Facts/Relations 的双向闭包仍由后继完整 conformance 负责。

## 6. 两个新 diagnostic 的最小放置语义

### 6.1 memory budget

memory containment 在 Provider Run 尚 active 的 execution cell 内停止本次尝试：

```text
overall_execution_status = INTERRUPTED
active ProviderRun.execution_status = INTERRUPTED
all reported IDs = []

ProviderRun.diagnostics
    contains EXECUTION_MEMORY_BUDGET
    subject_ref = that ProviderRun

top-level diagnostics
    contains the same typed cause
    subject_ref = that ProviderRun
```

这不是 `PROVIDER_FAILED`，也不产生部分 canonical Fact。

### 6.2 artifact budget

artifact staging 发生在 Provider Run 已经真实结束之后：

```text
overall_execution_status = INTERRUPTED
completed ProviderRun remains COMPLETED
all reported IDs = []
ProviderRun.diagnostics does not contain EXECUTION_ARTIFACT_BUDGET

top-level diagnostics
    contains EXECUTION_ARTIFACT_BUDGET
    subject_ref = null
```

`null` 是因为当前 `SubjectRef` 没有未发布 staging directory 的合法身份；不能错误借用输入 Artifact 或
ProviderRun subject。若未来需要可寻址 staging measurement，必须新增版本化 Artifact/subject contract。

## 7. 修正 corpus 必须证明什么

旧 `review-r1-schema-0.1` corpus 保持不变。新 correction corpus 至少拥有：

1. 一个 `0.1.1 / COMPLETED` 正例，证明成功 run 仍可报告规范 IDs；
2. 一个 memory-budget DIAGNOSTIC 正例；
3. 一个 artifact-budget DIAGNOSTIC 正例；
4. `INTERRUPTED / FAILED / UNAVAILABLE` run 携带任一 reported ID 的负例；
5. overall 非 `COMPLETED`、但任一 completed run 仍携带 ID 的负例；
6. 两个新 diagnostic 的错误 status、错误层级、错误 subject 的负例；
7. 三个正例的 canonical bytes 与 `derivation_evidence_digest` 复算向量；
8. 旧 `0.1` Schema/corpus exact SHA-256 未漂移的守卫。

新 corpus 只能增加新的稳定 case namespace；不得把 `R1-CV-001..020` 原地改名、扩义或重新编号。

## 8. 停止线与下一步

本审计只选择最小合同边界。它没有冻结 `0.1.1` 文件集，也没有授权编辑 Schema。下一步只能起草并冻结
独立 docs-only correction contract；该合同必须先完成自己的远端门、主线合入、exact-main 门与匿名读回。

当前状态保持：

```text
R1_DERIVATION_EVIDENCE_SCHEMA_PRECONTRACT_AUDITED
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_NOT_FROZEN
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

任何 fresh Agent 只读仓库后都必须知道：旧 `0.1` 不能原位改写；`0.1.1` 只修 DerivationEvidence；
request provenance、Provider runtime、Fact、Relation、Slice、Coverage 与完整 Manifest 均不属于本次施工。
