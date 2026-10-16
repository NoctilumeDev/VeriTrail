# R1 ReviewSliceSet / Coverage Schema correction 可行性审计

日期：2026-10-17

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 基线：`main@142bc264bbcddb155e5169fa0fa58659dedfa665`。
>
> 上游：[vocabulary correction 最小合同](270-r1-review-slice-set-coverage-vocabulary-correction-contract.md)与
> [独立冻结发布](271-r1-review-slice-set-coverage-vocabulary-correction-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_AUDIT + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只判断显式 successor identity / Schema
> correction 是否可在保持 Coverage 0.1 immutable 的条件下形成有限合同问题；不创建或修改 Schema、fixture、vector、
> runtime、test、manifest、consumer、Profile、Policy 或 corpus，不选择 successor 版本号、文件名、字段名、migration、
> persistence，也不启动 composition feasibility / implementation、public `ReviewSliceSet` / `CoverageLedger` assembler、
> Evidence、Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 exact coordinate

文档 271 的最后门已经在本基线闭合。PR #313 final head
`592ae6dd40b91ea91e4c829d7f6f47cb65c7520a` 合入为
`main@142bc264bbcddb155e5169fa0fa58659dedfa665`，tree 为
`2a614508899e1333b0cc1d964f398ac4b8dc069e`。原始 Public CI `38894454185`、exact-main Public CI
`38897295769` 与 Browser Smoke `38897295757` 均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1；
Review Attention 四格各为 `513 reported / 510 passed / 3 skipped`。

fresh README/doc271/milestones 各有一份 qualifying PASS。milestones formal observation #1 的 P2 COMPLETE、P1 匿名
API `403 / remaining=0 / COLLECTION_BUDGET_EXHAUSTED` ERROR 与后继 #2 PASS 同时保留；额度耗尽的外部原因保持
UNKNOWN。independent reconciliation 与 126-artifact closeout 分别为：

```text
7330df0c1832d5e8601c98a15c91e01a4e6cccd7780fdf6d1242f2da8430d645
97de5369a6bda0a2776859dabd3a92dfa0097210b3f5493c91d50be53f4502a9
```

文档 270 与 271 的 full-file SHA-256 分别保持：

```text
f205c6dca120d5951565b43c317d8906c9d113bb03fb520b9d9480f0f0e4f7a4
2da37c9c929b87dfc62e26f413641d92bbea72f1d4c825feca24f750705f99a5
```

因此以下是本文的 frozen upstream，不是本文的 target：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

remote `main`、本 worktree HEAD 与基线一致；open PR 只有既有 Dependabot 依赖更新，没有新的 semantic PR。主检出仍保留
用户 `audit.json`，本文不触碰它。本轮只取得 Schema correction feasibility 的问题审计权。

## 2. 当前 Schema 与 version stop

Coverage 0.1 的冻结公开 surface 为：

```text
schemas/review-coverage-ledger-0.1.schema.json
tests/fixtures/review-r1-schema-0.1/**
veritrail.review.coverage-ledger/0.1
review-derivation-manifest-0.1.schema.json
```

它只有 `completed / unsupported / unresolved / conflicts / parse_failed / execution_failed / truncated / frontier` 等 carrier，
没有独立 semantic `BLOCKED` disposition，也没有 `UNREPRESENTABLE_EXPECTED_FACT` reason。文档 270 已冻结的完整 tuple 为：

```text
terminal class       = BLOCKED
disposition family   = SEMANTIC_PROJECTION_BLOCKER
exact reason         = UNREPRESENTABLE_EXPECTED_FACT
subject identity     = exact FACT U-slot identity
provenance           = exact blocker + same-attempt history
```

因此旧 0.1 不能原地修补，也不能把 tuple 改名为 `DERIVATION_ERROR / execution_failed`。当前问题是能否建立显式、有限且
fail-closed 的 successor boundary，不是立即选择 `0.2` 或新增某个字段。

## 3. 仓库内 precedent：child successor 不要求 common 先升级

仓库已有 `DerivationEvidence 0.1.1 / 0.2` precedent：

- child Schema 自己拥有不同 `schema_version` 与 identity domain；
- 它们继续复用 `review-r1-common-0.1` 中未改变的基础类型，但不复用 common 的 `SchemaVersion` 常量；
- `review-derivation-manifest-0.1` 的 role/path/byte/digest topology保持不变；
- 旧 child Schema 不会把 successor bytes 当作旧版本接受；
- successor 仍需要自己的 fixture、identity vectors 与 conformance validation。

这个 precedent 只证明结构路径存在，不自动决定 Coverage 应使用 patch、minor 或其他版本，也不证明现有 consumer 已经拥有
Coverage child dispatch。Schema/version authority 仍必须由后继合同单独取得。

## 4. 七个机械 world

仓库外 read-only harness 从 exact 0.1 Schema、common types、manifest 与 frozen `valid-complete` fixture 构造一个明确标注为
audit-only 的 successor shape。该 shape 只用于回答“有限表示是否可能”，字段名、Schema version 与 identity domain 均不是
产品 proposal。

| world | 观察 |
| --- | --- |
| `BASELINE_0_1` | 0.1 fixture继续通过原 Schema |
| `REASON_ONLY_IN_EXECUTION_FAILED` | exact blocker reason被0.1拒绝 |
| `SILENT_RENAME_AS_DERIVATION_ERROR` | 0.1 Schema接受，但上游语义被错误改名 |
| `AUDIT_ONLY_DISTINCT_BLOCKED_SUCCESSOR` | 独立 successor可表达完整 blocker tuple，旧0.1明确拒绝该 child |
| `CONFLICTING_COVERED_AND_BLOCKED` | JSON Schema可同时接受两份互斥 terminal witness；独立 conformance拒绝 |
| `MANIFEST_0_1_BINDS_SUCCESSOR_CHILD` | 旧 manifest可绑定 successor bytes/digest，但不负责选择 child Schema |
| `UNKNOWN_CHILD_VERSION` | 已知旧/新 validator均 fail closed |

首次 harness attempt 把 audit-only `$id` 放在不同 URI base，导致相对 common `$ref` 解析失败；它作为
`UNRESOLVABLE_REFERENCE_SETUP_ERROR / qualification effect NONE` 保留。fresh attempt只修 proof-facility URI base，并把
`assert` 改为普通/`-O` 都执行的显式检查，没有修改仓库、产品、语义问题或 oracle。

CPython 3.10.6 / 3.13.13、normal / `-O` 四格 canonical report 逐字节相同：

```text
e54642dc26f7a4a9f2e7317c462217eff5375b3c8aaf9e380912ea22661deacc
```

声明的 Schema/compatibility/Markdown/hygiene 本地矩阵首次直接调用未绑定 repository `src`，在
`tests.test_markdown` import 时留下 `LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`；已报告的42项中41项通过、
1个test module import ERROR。fresh attempt只修调用方`PYTHONPATH`，未改产品、test、文档语义或oracle；四格各为：

```text
45 reported / 45 passed
```

## 5. Schema 可表达不等于 total semantics 成立

mechanical world证明独立 child Schema可以有限表达 exact blocker tuple，但 JSON Schema 不能仅凭两个数组的局部 shape，机械
证明同一个 denominator member没有同时出现在 `COVERED` 与 `BLOCKED`。同理，Schema shape本身也不拥有：

```text
denominator authority
applicability authority
reason qualification
same-attempt provenance
terminal witness admission
cross-stage transition proof
stage / overall conservative join
```

因此后继最小 correction 不能只是一个 `.schema.json` 文件。它至少必须同时冻结：

1. self-describing successor Schema identity；
2. distinct coverage-ledger identity domain；
3. exact blocker tuple的无损 carrier；
4. versioned conformance rule，拒绝重复、遗漏、互斥 terminal witness、misbound reason与错误 join；
5. positive/negative fixture与identity vectors；
6. old 0.1 byte guards与unknown-version fail-closed rule。

这里的 conformance 是 Schema correction 的语义搭档，不是 composition runtime，也不取得生成 ledger 的 authority。

## 6. manifest 与 consumer dispatch 边界

`review-derivation-manifest-0.1` 的 `COVERAGE_LEDGER / coverage-ledger.json / sha256 / semantic_digest` entry可以绑定
successor child bytes。该事实说明当前没有证据要求先升级 manifest topology；它不说明 manifest 0.1 能判断 child 属于哪个
Schema。manifest 只证明“这些 bytes/digest被列入 bundle”，不能证明：

```text
child schema version recognized
child conformance passed
semantic mapping admitted
old consumer may reinterpret successor as 0.1
```

后继合同必须明确 consumer dispatch：先读取并验证 self-description，再选择精确已知 Schema/conformance；未知版本必须停止。
如果现有 consumer/publication path不能机械实施该规则，就必须停在 private successor Schema/corpus boundary，并重新审查是否需要
manifest successor。当前审计没有资格预先选择新的 manifest 版本。

## 7. identity、compatibility 与 migration

Coverage 0.1 digest domain必须继续 immutable。successor 即使成员、stage或最终 status与0.1看起来相同，也必须拥有显式不同的
identity domain；相同 semantic content不继承0.1 digest identity。后继合同还必须区分：

```text
old 0.1 consumer rejects unknown successor
    !=
successor consumer can validate and admit it

manifest binds child bytes
    !=
manifest grants child semantic authority

shape migration exists
    !=
historical 0.1 Bundle may be rewritten
```

本审计没有证明需要把历史0.1迁移到successor，也没有选择双写、转换工具、兼容窗口或public directory。migration保持
non-decision。

## 8. 最小否定矩阵

后继合同至少必须保留并直接攻击以下 worlds：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RSCSF-000` | 0.1 baseline | correction可以改变旧bytes/identity |
| `RSCSF-001` | successor只增加reason | reason存在就等于disposition无损 |
| `RSCSF-002` | blocker改名为`DERIVATION_ERROR` | Schema-valid保持上游语义 |
| `RSCSF-003` | same item同时covered与blocked | JSON Schema通过即total partition成立 |
| `RSCSF-004` | successor child放入manifest 0.1 | manifest自动完成child dispatch/conformance |
| `RSCSF-005` | unknown child version | consumer可以按最接近版本解释 |
| `RSCSF-006` | common 0.1 types可复用 | common `SchemaVersion=0.1`可以冒充successor version |
| `RSCSF-007` | successor shape可表达tuple | shape自动授予mapping/admission authority |
| `RSCSF-008` | successor digest与0.1内容相似 | 可以继承0.1 identity domain |
| `RSCSF-009` | manifest topology当前可复用 | 永远不需要重新审查manifest/version boundary |

## 9. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| vocabulary correction合同是否已经frozen | **是** |
| explicit successor Schema correction是否仍是最早合法seam | **是** |
| finite additive child Schema是否可行 | **是** |
| 是否必须先升级common Schema | **否，当前反例未证明** |
| 是否必须先升级manifest topology | **否，当前反例未证明** |
| manifest/consumer child dispatch是否必须显式冻结 | **是** |
| JSON Schema是否足以证明total terminal semantics | **否** |
| 是否需要versioned conformance rule | **是** |
| 当前是否已选择successor版本、文件名或字段shape | **否** |
| composition feasibility/runtime是否已授权 | **否** |
| persistence是否成为当前blocker | **否** |

因此下一份最小合同不是“大改全部 R1 Schema”，也不是直接实现 `CoverageLedger`。它应只冻结一个 self-describing、独立 identity
的 Coverage successor Schema + conformance boundary，并明确旧 0.1 immutability、manifest/consumer dispatch、fixture/vector与
unknown-version fail-closed discipline。

## 10. 后继合同最小问题面

如果本文完成自己的资格链，下一轮最多有资格起草 docs-only Schema correction contract candidate，回答：

1. successor child的规范 identity、version与identity domain；
2. exact blocker tuple的完整字段语义与canonical order；
3. terminal partition、reason ownership与stage applicability；
4. Schema负责的shape与conformance负责的跨字段不变量；
5. digest construction、positive/negative corpus与identity vectors；
6. 0.1全字节守卫、unknown-version拒绝与旧consumer fail-closed；
7. manifest 0.1绑定successor child时的dispatch/conformance rule；
8. 何种反例才要求manifest successor或common successor；
9. private/public consumer ceiling与migration non-decision；
10. composition runtime、persistence与publication继续禁止的边界。

只有该合同完成自己的资格链以后，才重新审查 Schema实现授权；private composition feasibility仍须等 Schema correction自身资格化，
不能与它合并施工。

## 11. 候选资格链与停止线

本文候选的 tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc267–271、runtime、tests、
workflows、Schema、manifest、fixtures、Profile、Policy、identity vectors、corpus与架构资产保持base bytes。

final bytes必须完成Markdown/Schema baseline regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态marker、
四文件scope、敏感字面量、上游frozen-byte continuity、`git diff --check`与read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> feasibility audit becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权Schema contract、Schema/runtime/tests、composition feasibility/implementation、public `ReviewSliceSet` /
`CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。
完成资格以后必须重新进入[CONTROL LOOP](working-method.md)，不能按文档编号自动施工。
