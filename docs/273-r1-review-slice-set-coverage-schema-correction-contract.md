# R1 ReviewSliceSet / Coverage Schema correction 最小合同 0.1

日期：2026-10-17

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE`。
>
> 基线：`main@406aa8ee9440db8738ee2bd3a35aae558dc105c6`；tree
> `360f5cfd49f82e7e4194c425998dee277da4dc75`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [vocabulary correction 最小合同](270-r1-review-slice-set-coverage-vocabulary-correction-contract.md)、
> [vocabulary correction 独立冻结发布](271-r1-review-slice-set-coverage-vocabulary-correction-contract-freeze-publication.md)与
> [Schema correction 可行性审计](272-r1-review-slice-set-coverage-schema-correction-feasibility-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只冻结 CoverageLedger successor 的
> child identity、最小 additive blocker carrier、versioned conformance、manifest/consumer dispatch 与 Coverage 0.1
> immutability；不创建或修改 Schema、runtime、tests、fixtures、vectors、manifest、Profile、Policy 或 corpus，不授权
> composition feasibility / implementation、public `ReviewSliceSet` / `CoverageLedger` assembler、persistence、Evidence、
> Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 qualified upstream

文档 272 已从本基线完成独立资格链。PR #314 final head
`a2577e1f05f1ebd685a35120181fc2b85bfffa7a` 的 original Public CI `38964769464`、exact-main Public CI
`38967921677` 与 Browser Smoke `38967921685` 均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1；Review
Attention 四格各为 `513 reported / 510 passed / 3 skipped`。

setup 1 的 public wheel wildcard、incomplete adapter preparation、upstream live-stdout self-reference 与折叠 README marker
选择错误均保留；README formal #1 的 `READBACK_MARKER_SELECTION_SETUP_ERROR` 没有被后继 PASS 覆盖。setup 2 的 fresh
README/doc272/milestones 各有且仅有一份 qualifying PASS，independent reconciliation 与 119-artifact closeout 分别为：

```text
d32b662933368546e14fb01d8477b6be5452fa9c5ecafaa695a35aba789d3672
741ed5551b423597bcebda0ee94f6102ffa872160e4cbe6a3649d34eab08a2f8
```

文档 270、271 与 272 的 full-file SHA-256 分别保持：

```text
f205c6dca120d5951565b43c317d8906c9d113bb03fb520b9d9480f0f0e4f7a4
2da37c9c929b87dfc62e26f413641d92bbea72f1d4c825feca24f750705f99a5
fca72be67b1245922d20ad6df00848964bd777aaaf318ad3a63a8ba42ea83435
```

remote `main`、本工作树基线与该 exact main 一致；open PR 只有既有 Dependabot 更新，没有新的 semantic PR。doc272
的七个 mechanical worlds 与 version stop 没有被新反例击穿。因此本文消费以下 frozen / qualified upstream：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

当前最小合法问题仍是 Schema correction 语义合同，不是直接物化 Schema，也不是开始 composition runtime。

## 2. successor identity 与 version boundary

Coverage successor 的规范 child identity 冻结为：

```text
schema file              = schemas/review-coverage-ledger-0.2.schema.json
schema $id               = https://github.com/NoctilumeDev/VeriTrail/schemas/review-coverage-ledger-0.2.schema.json
artifact_kind            = COVERAGE_LEDGER
schema_version           = 0.2
canonicalization_profile = veritrail-json-c14n/1
semantic digest domain   = veritrail.review.coverage-ledger/0.2
conformance identity     = r1-review-coverage-ledger-conformance/0.2
contract function        = r1-review-slice-coverage-schema-correction/0.1
manifest role/path       = COVERAGE_LEDGER / coverage-ledger.json
```

`0.2` 表示 CoverageLedger child 的语义与 digest identity 改变；它不是对 common 或 manifest 的版本声明。successor 可以复用
`review-r1-common-0.1` 的 `CanonicalizationProfile`、digest 与 `CoverageItemRef` 等未改变基础类型，但 `schema_version`
必须由 child 自己以 `const: "0.2"` 声明，不能引用 common 0.1 的 `SchemaVersion`。

以下 identity 不得互换：

```text
veritrail.review.coverage-ledger/0.1
    != veritrail.review.coverage-ledger/0.2

schema_version == 0.2
    != manifest schema_version == 0.1

manifest binds bytes/digest
    != child schema recognized
    != child conformance admitted
```

相同 stage content、相同 final status 或相同 UI 文案不能继承 0.1 digest identity。unknown child version 必须 fail closed。

## 3. additive child shape

successor 保留 Coverage 0.1 的 root binding、固定七阶段顺序、既有 disposition carriers、`overall_coverage_status` 与
`coverage_ledger_digest`。它只在被反例击穿的边界增加：

1. `CoverageReason` 增加 `UNREPRESENTABLE_EXPECTED_FACT`；
2. 每个 stage 必须带一个 `blocked` 数组，空数组是显式无 blocker，而不是字段缺失；
3. `blocked` member 的规范 shape 为：

```json
{
  "item_ref": {
    "item_kind": "FACT",
    "item_id": "<exact frozen U-slot subject_key_digest>"
  },
  "disposition_family": "SEMANTIC_PROJECTION_BLOCKER",
  "reason_codes": ["UNREPRESENTABLE_EXPECTED_FACT"]
}
```

本 version 只允许该 tuple 出现在 `FACT_DERIVATION` stage，`item_kind` 只能为 `FACT`，`reason_codes` 恰有一个成员。
其他六个 stage 的 `blocked` 必须为空。增加其他 blocker family、reason、stage 或 item kind 需要新合同；不得把本 version
当作开放字符串容器。

`blocked` 是 terminal disposition carrier。它不取代 `eligible` applicability projection，也不把 `NOT_APPLICABLE` 搬进
denominator。一个 blocked item 可以继续出现在 `eligible`，但不得同时出现在 `completed`、`unsupported`、`unresolved`、
`conflicts`、`parse_failed`、`execution_failed`、`truncated`、`frontier` 或 `out_of_scope` 的 terminal/disposition carrier 中。

## 4. blocker provenance 不由字段自证

successor entry 保存 exact item、family 与 reason，但这些字面字段没有自行生成语义事实的 authority。conformance 只有在消费
同一 composition attempt 的 qualified Fact projection history 后，才可 admission 该 entry：

```text
exact FACT_DERIVATION denominator / U identity
exact U-slot subject_key_digest
complete U / E / blocker partition
qualified blocker reason and producing function identity
same-attempt Fact closure / handoff / composition identity
candidate CoverageLedger root bindings
```

root 中的 `fact_set_digest`、`slice_set_digest` 或 manifest `semantic_digest` 只绑定 semantic content，不能替代 live claim、
attempt、closure 或 admission authority。本文不把 private attempt identity写入 public Schema，也不允许 digest holder自行生成
`blocked`。未来 public Evidence 如何携带 admission provenance 保持后继问题；在该 authority 尚未建立时，0.2 child最多是
private qualified artifact，不能冒充公开自证结果。

## 5. Schema 与 conformance 的责任分离

JSON Schema 只拥有局部 shape：required fields、closed properties、固定 version、enum、item kind、array cardinality 与 stage-local
applicability。versioned conformance rule 必须另外机械证明：

1. root digests、stage 顺序、upstream stage 与 exact artifact bindings一致；
2. known denominator 的 member来自 authoritative stage universe；unknown denominator只保留 exact known prefix；
3. 每个 blocked item属于 known denominator `item_refs`，或 unknown denominator 的 `known_item_refs`；
4. 同一 item没有两个 blocker entry，也没有互斥 terminal witness；
5. family、reason、stage、item kind 与 qualified upstream provenance完全匹配；
6. `stage.reason_codes` 等于该 stage 所有 denominator/disposition/frontier reason 的 canonical union；
7. blocked 非空时该 stage不得为 `COMPLETE`；
8. blocker使 downstream universe不可完整枚举时，依赖 stage必须为 `UNKNOWN`；
9. seven-stage conservative join 与 `overall_coverage_status`一致；
10. canonical order、canonical bytes与 0.2 semantic digest均正确。

Schema-valid 只取得 shape witness；只有 exact 0.2 Schema与 exact 0.2 conformance都通过，且上游 authority完整，candidate 才能
取得 semantic admission。conformance不能生成 ledger、修复 candidate、选择最接近 reason，或把冲突世界折叠成某个 terminal。

## 6. canonical order 与 digest construction

所有会影响 0.2 semantic digest 的 array 必须由实现按冻结顺序构造，不依赖 Provider report order、Python iteration order、
filesystem order 或 consumer traversal order：

```text
stage order:
  SNAPSHOT_INVENTORY
  POLICY_SCOPE
  LANGUAGE_SUPPORT
  PARSE
  FACT_DERIVATION
  RELATION_DERIVATION
  SLICE_DERIVATION

CoverageItemRef order:
  INVENTORY_ENTRY < PARSE_UNIT < FACT < RELATION < REVIEW_SLICE
  then item_id by lowercase UTF-8 byte order

disposition order:
  item_ref order
  then disposition_family
  then canonical reason rank
```

本 version 的新 reason rank 位于既有 Coverage 0.1 reason list之后。`stage.reason_codes` 使用同一 canonical rank并去重。
`coverage_ledger_digest` 的构造为：移除该字段，对剩余完整 payload执行 `veritrail-json-c14n/1`，再以
`veritrail.review.coverage-ledger/0.2` domain计算 semantic digest。0.1 domain、0.1 digest或普通文件 SHA-256 均不能替代。

后继实现必须提供至少一组 positive identity vector与逐项 negative digest vectors；Schema fixture通过不能替代 digest identity
验证。

## 7. manifest 与 consumer dispatch

`review-derivation-manifest-0.1` 继续只绑定：

```text
role = COVERAGE_LEDGER
path = coverage-ledger.json
sha256 / size_bytes / semantic_digest
```

consumer 必须先读取 child 的最小 self-description，只允许按精确 registry key dispatch：

```text
(artifact_kind = COVERAGE_LEDGER, schema_version = 0.1)
    -> exact 0.1 Schema / 0.1 rules

(artifact_kind = COVERAGE_LEDGER, schema_version = 0.2)
    -> exact 0.2 Schema / r1-review-coverage-ledger-conformance/0.2

otherwise
    -> UNKNOWN_CHILD_VERSION / fail closed
```

dispatch前不得按 0.1字段解释 successor；dispatch后不得让 0.2 validator修补或重解释 0.1。manifest中存在 entry、path相同、
hash正确或 semantic digest看似匹配，都不授予 child version recognition或conformance admission。

若后继实现审计证明 current consumer无法在不改 manifest topology的条件下安全取得 self-description，必须停下并重新审查
manifest successor；本文不预先授权修改 manifest 0.1。

## 8. Coverage 0.1 immutability 与 compatibility

以下 0.1 bytes / semantics 保持 immutable：

```text
schemas/review-coverage-ledger-0.1.schema.json
    sha256 = e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545

schemas/review-r1-common-0.1.schema.json
    sha256 = e36f0d4ba494645bc991736b780c2c5354be13789466ab82d72b4963c674da4a

schemas/review-derivation-manifest-0.1.schema.json
    sha256 = 69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91

tests/fixtures/review-r1-schema-0.1/**
    19-file manifest sha256 = 5dc48dc45b89b58e57bef8768206b87ce94df5cb9cabf6dcb5d850788141e67f
```

旧 0.1 consumer必须拒绝 0.2 bytes；0.2 consumer可以显式支持0.1和0.2，但必须分别验证各自identity，不能把0.1自动升级
成0.2。历史Bundle、manifest、digest与fixture不迁移、不重写、不双写。migration tool、compatibility window与public directory
均为 non-decision。

## 9. corpus 与 identity vectors

后继 implementation feasibility 至少必须证明以下 positive worlds可以被精确表达并由0.2 conformance裁决：

| ID | world | required result |
| --- | --- | --- |
| `RSCSC-P00` | 同一个normal baseline world按0.2独立构造，全部`blocked=[]` | 0.2 PASS；0.1 bytes仍原样 PASS |
| `RSCSC-P01` | FACT U=3、E=2、一个 exact blocker slot | FACT stage PARTIAL；完整tuple保留 |
| `RSCSC-P02` | blocker使 Relation universe不能完整枚举 | Fact PARTIAL；Relation及依赖 stage UNKNOWN |
| `RSCSC-P03` | manifest 0.1绑定合法0.2 child bytes/digest | manifest shape PASS；consumer独立dispatch+conformance PASS |

至少必须拒绝以下 negative worlds：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RSCSC-000` | 修改 Coverage 0.1 Schema/fixture bytes | successor允许重写历史0.1 |
| `RSCSC-001` | 0.2缺少`blocked`字段 | 字段缺失等于显式empty |
| `RSCSC-002` | reason存在但family缺失或错误 | reason-only保持完整tuple |
| `RSCSC-003` | blocker改名为`DERIVATION_ERROR`/execution failure | shape近似等于语义相同 |
| `RSCSC-004` | blocker出现在非Fact stage或非Fact item | 任意stage/item都可消费该reason |
| `RSCSC-005` | blocker item不属于denominator/known prefix | 字面item ref自己创建obligation |
| `RSCSC-006` | same item同时completed与blocked | Schema PASS即total partition成立 |
| `RSCSC-007` | duplicate blocker entries | 重复相同事实不改变identity |
| `RSCSC-008` | blocked非空但stage写COMPLETE | status字段可以覆盖terminal history |
| `RSCSC-009` | downstream universe未知却写COMPLETE/known-empty | precise upstream blocker补造downstream truth |
| `RSCSC-010` | stage reason summary漏掉或多出reason | summary无需与terminal carriers对账 |
| `RSCSC-011` | arrays非canonical order | JSON语义近似允许不同digest identity |
| `RSCSC-012` | 0.2 payload使用0.1 digest domain | content相同允许继承旧identity |
| `RSCSC-013` | manifest hash正确但child version未知 | manifest entry拥有dispatch authority |
| `RSCSC-014` | old consumer按0.1解释0.2 | closest-version fallback安全 |
| `RSCSC-015` | entry字段正确但upstream provenance属于foreign attempt | shape/digest继承same-attempt authority |
| `RSCSC-016` | 只运行JSON Schema，不运行conformance | 局部shape证明cross-field semantics |
| `RSCSC-017` | 0.2 child合法 | child自己拥有composition/publication authority |

positive fixture不能替代这些 falsifier；同样的 `PARTIAL` 或相同 UI 文案也不能证明 disposition无损。

## 10. implementation boundary 与 stop conditions

合同以后若资格化，下一轮最多有资格审查一个有限 Schema implementation：

```text
new 0.2 child Schema
new 0.2 positive/negative fixtures
new 0.2 identity vectors
versioned conformance validator/tests
0.1 byte guards
known-version consumer dispatch at the private validation boundary
```

它仍不授权 ledger assembler、same-attempt composition runtime、public bundle publication、persistence或迁移。出现以下任一条件
必须返回 CONTROL LOOP：

- 只有修改 0.1 bytes、common 0.1或manifest 0.1才能实现；
- 需要让 manifest、Schema、consumer、Provider或publisher生成 blocker truth；
- 无法在不暴露或恢复 live claim的情况下验证same-attempt provenance；
- 需要增加第二个 blocker family/reason或改变其他 stage semantics；
- 需要按内容相似度fallback到未知 child version；
- 需要先实现 composition assembler才能证明 child conformance；
- 需要选择 persistence Route A/B、migration或public directory才能继续。

## 11. authority ceiling

本文不定义或授权：

```text
Schema/runtime/tests/fixtures/vectors/conformance implementation
composition feasibility / private runtime / assembler
ReviewSliceSet projection or admission changes
denominator / U / E / blocker production changes
manifest/common successor or migration
persistence Route A/B
public Evidence / Bundle / publisher / CLI / Workbench / Core
R2 / R3 / CLAIM_FIDELITY / tag / Release
```

`CoverageLedger 0.2` 的 child identity被本文选择，不代表对应文件、validator、fixture、consumer或产品已经存在。合同候选的
Schema描述也不是可运行Schema。

## 12. 本候选自己的资格门

tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc267–272、runtime、tests、workflows、
Schema、manifest、fixtures、Profile、Policy、identity vectors、corpus与架构资产必须保持base bytes。

final bytes的本地门至少包括：UTF-8 without BOM、LF/final LF、links/fences/headings、状态marker、四文件scope、敏感字面量、
上游frozen-byte continuity、`git diff --check`与read-only hygiene；Coverage 0.1 Schema regression、existing Schema correction
regression及相关Markdown regression按声明矩阵在CPython 3.10/3.13、normal/`-O`运行。测试只作witness，不把本合同变成
Schema或runtime。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权独立冻结发布、Schema implementation、composition feasibility/implementation、public `ReviewSliceSet` /
`CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。
候选资格闭合以后必须重新进入 [CONTROL LOOP](working-method.md)，不能按文档编号自动施工。
