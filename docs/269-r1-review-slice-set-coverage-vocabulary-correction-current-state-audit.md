# R1 ReviewSliceSet / Coverage vocabulary correction 当前状态审计

日期：2026-10-16

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_CANDIDATE`。
>
> 基线：`main@13e08177e9353d45ebc2fde1244ac37b2bfea2d6`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)与
> [独立冻结发布](268-r1-review-slice-set-coverage-qualification-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_AUDIT + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只复核 mandatory version stop
> 的最小问题边界；不修改 runtime、tests、Schema、fixtures、Profile、Policy、identity vectors 或 corpus，不选择
> successor 版本号、文件名、class、migration 或 persistence，也不启动 composition feasibility / implementation、
> `ReviewSliceSet` / `CoverageLedger` assembler、Evidence、Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 exact coordinate

文档 268 的最后门已经在本基线闭合。PR #310 final head
`294b67f3162c13a9b8bc3fdd888448aaea01742b` 的 original Public CI `38858809608`、exact-main Public CI
`38866243713` 与 Browser Smoke `38866243720` 均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1；
Review Attention 四格各为 `513 reported / 510 passed / 3 skipped`。

fresh README/doc268/milestones 三个 formal observations 均为 P1/P2 COMPLETE、Core PASS。首次 readback setup 的
Windows wildcard、遗漏 Playwright 与 doc268 marker 选择错误，以及首次 independent reconciliation 的 derived-summary
路径假设错误均保留原身份；fresh setup 2 又保留一次 adapter ownership setup error。setup 2 的 independent
reconciliation 与 120-artifact closeout 分别为：

```text
4a3a57357fd6523c872c5f0f326f859c35a960f9ce8021f101ffe442686903a8
5ddce0cd29ec8b5ef6b3150a5b5e752a5e7bd67bb9b12a744ad7f56810341a1b
```

文档 267 与 268 的 full-file SHA-256 分别保持：

```text
598ad8069df115a49baf35c7b62d43e286abe39096b4dc62ced23321d6024aa6
4d2ef691e36107c7967c80dae48ad9026a4f3720935de2e38e689df737975879
```

因此以下是本文的 frozen upstream，不是本文的 target：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

remote `main`、本 worktree HEAD 与基线一致；没有新的 semantic PR 插入。本审计只取得重新检查 mandatory vocabulary
version stop 的问题审计权，不因合同冻结自动获得 Schema correction 或 runtime authority。

## 2. 审计问题：缺的是 reason，还是 terminal disposition

文档 267 已冻结 projection-blocked world：

```text
Fact universe U = 3
representable expectations E = 2
blocker slots = 1
exact blocker reason = UNREPRESENTABLE_EXPECTED_FACT
```

冻结合同同时规定 denominator 内的 qualification semantics 为：

```text
COVERED / MISSING / BLOCKED / UNKNOWN
```

其中 `BLOCKED` 表示 obligation 已知存在，且存在精确、已取得资格的原因使正常 fulfillment 无法成立；它不是 Provider
执行失败，也不是 denominator 未知。当前 public Coverage 0.1 只提供：

```text
completed
unsupported
unresolved
conflicts
parse_failed
execution_failed
truncated
frontier
```

`CoverageReason` 不包含 `UNREPRESENTABLE_EXPECTED_FACT`，`ExecutionFailedDisposition` 又只允许
`PROVIDER_UNAVAILABLE / DERIVATION_ERROR`。因此当前问题不能预先缩成“在 reason enum 里再加一个值”。

## 3. 四个机械 world

仓库外只读 audit harness 以 exact 0.1 Schema 与 frozen `valid-complete` fixture 构造四个单变量 world：

| world | 0.1 Schema | 观察 |
| --- | --- | --- |
| `BASELINE_0_1` | valid | frozen complete fixture 保持可验证 |
| `NEW_REASON_IN_EXISTING_EXECUTION_FAILED` | invalid | stage reason 与 execution-failed reason 均拒绝 exact blocker reason |
| `SILENT_RENAME_AS_DERIVATION_ERROR` | valid | shape 通过，但 representation blocker 被改名为 execution failure |
| `DISTINCT_BLOCKED_DISPOSITION` | invalid | 0.1 同时拒绝新 reason 与额外 `blocked` carrier |

canonical report SHA-256 为：

```text
ca894439a2e96b7aa5ba943e7770545d02fd7848b90af53b8edb2f23aca847a2
```

这组结果证明：

```text
reason-only correction is sufficient                 = false
frozen 0.1 has distinct BLOCKED disposition          = false
silent rename can remain Schema-valid                = true
FACT item identity shape is the blocking seam        = false
minimal problem boundary                             = versioned reason + disposition vocabulary
```

Schema-valid 只证明结构接受；`SILENT_RENAME_AS_DERIVATION_ERROR` 恰好是反例，不能被当作现有 0.1 已经具备
无损语义的证据。

## 4. Identity 与 disposition 必须继续分开

文档 265–267 已证明 projection-blocked U slot 的 `subject_key_digest` 可以作为现有
`{item_kind: FACT, item_id: ...}` 表达。本文没有发现更早的 identity-shape blocker：

```text
slot can be named
    != slot mapping is admitted
    != terminal disposition is expressible
```

因此后继不能为了这个反例先造新的 item kind，也不能把任意 64-hex digest 当成合格 U-slot identity。future correction
仍须让 composition application 按 frozen Fact subject domain 重验 exact slot identity；但这个 revalidation 属于后继合同，
不改变本次 vocabulary 问题边界。

## 5. 不允许把上游事实重新解释成已有 bucket

以下三个 world 必须保持不同：

| 上游事实 | Coverage 最低保留语义 | 禁止改名 |
| --- | --- | --- |
| U slot 已知存在，但 frozen projection 不可表示 | semantic blocker | `DERIVATION_ERROR` / Provider execution failure |
| Provider 已运行但没有产生应有结果 | fulfillment failure | representation blocker |
| denominator、attempt 或 required history 不足 | `UNKNOWN` | known blocker / known missing |

把 `UNREPRESENTABLE_EXPECTED_FACT` 放进 `execution_failed` 会让数据仍在、语义却丢失；把它改成
`UPSTREAM_DENOMINATOR_UNKNOWN` 又会把 known U slot 变成 denominator unknown。两者都违反文档 267 的 authority ceiling。

Coverage 可以在自己的 stage vocabulary 中映射 typed upstream facts，但不能改变上游事实类型、补造前提或为了 0.1 shape
消除不确定性。

## 6. 0.1 必须保持 immutable

当前 Schema、fixtures 与 identity vectors 已承担 frozen historical / compatibility responsibility。本文没有取得静默修改
`review-coverage-ledger-0.1.schema.json` 的 authority，也没有证明所有现有 consumer 可以接受 shape 变化。

因此最低 version discipline 是：

```text
0.1 bytes / semantics remain immutable
    -> independent minimal correction contract
    -> explicit successor identity
    -> only then Schema / fixture / vector / consumer correction eligibility
```

“successor identity”不等于本文已经选择 `0.2`。版本号、Schema 文件、migration、compatibility strategy、public directory 与
class shape 均保持 non-decision。

## 7. 后继最小合同问题

如果本文完成自己的资格链，下一轮最多有资格起草一份 docs-only vocabulary correction contract candidate，回答：

1. **semantic input**：exact upstream blocker、denominator member、stage 与 attempt identity 的完整输入是什么；
2. **reason ownership**：哪些 frozen upstream reason 可以进入 successor vocabulary，谁无权新增或改名；
3. **disposition ownership**：`BLOCKED` 怎样与 `MISSING / UNKNOWN / execution failure` 保持互斥；
4. **total composition**：每个 applicable denominator member 怎样恰好进入一个 terminal partition；
5. **stage aggregation**：blocker 如何形成 conservative stage / overall status，不能让 incomplete world 成为 COMPLETE；
6. **0.1 immutability**：successor 如何不改写已有 Schema、fixture、vector 与 historical Bundle identity；
7. **consumer boundary**：哪些 private composition consumer需要新 vocabulary，哪些 public migration 继续不授权；
8. **version stop**：若 reason/disposition 仍不能无损表达，必须在哪一层停，而不是继续让 assembler 猜；
9. **authority ceiling**：correction 不定义 denominator、ReviewSliceSet admission、persistence、publication 或 R3 priority。

后继仍先冻结语义，不先设计对象。只有合同资格化以后，才重新审查 Schema correction feasibility；composition private
feasibility 也不能借本审计自动开始。

## 8. 最小否定矩阵

| ID | 单变量 world | 必须拒绝的结论 |
| --- | --- | --- |
| `RSCV-000` | U=3/E=2，第三 slot 可命名但不可表示 | E 或 actual Fact outputs 可以缩小 U |
| `RSCV-001` | exact blocker reason 不在 0.1 enum | 改名为 `DERIVATION_ERROR` 即保持语义 |
| `RSCV-002` | new reason 被塞入 `execution_failed` | reason 存在就证明 disposition 正确 |
| `RSCV-003` | distinct `blocked` carrier 被 0.1 拒绝 | 0.1 已无损表达四态 terminal partition |
| `RSCV-004` | denominator known，blocker known | 可升级为 `UNKNOWN` 消除 correction need |
| `RSCV-005` | Provider 未运行或 infrastructure failure | 可统一归入 semantic blocker |
| `RSCV-006` | 0.1 bytes 已冻结 | 可以原地增加 enum/property而不改变 identity |
| `RSCV-007` | successor shape 可表达 blocker | Schema shape 自动授予 mapping/admission authority |

normal complete happy path 不能替代这些 negative worlds。

## 9. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| composition qualification 合同是否已经 frozen | **是** |
| mandatory vocabulary version stop 是否仍是最早合法 seam | **是** |
| blocker slot identity 是否要求先新增 item kind | **否** |
| 只新增 `UNREPRESENTABLE_EXPECTED_FACT` reason 是否足够 | **否** |
| 0.1 是否已有独立 semantic `BLOCKED` carrier | **否** |
| 能否借 `DERIVATION_ERROR` / `execution_failed` 保持语义 | **否** |
| 当前是否已选择 successor 版本或 Schema shape | **否** |
| Schema correction / composition feasibility 是否已授权 | **否** |
| persistence 是否成为当前 blocker | **否** |

因此当前最小问题不是“实现 CoverageLedger”，而是：

> 为 frozen projection blocker 提供一个 versioned、无损且不重解释上游事实的 reason + disposition vocabulary，并保持
> 0.1 immutable；只有这条语义边界取得资格以后，才有权审查具体 Schema correction 与 composition feasibility。

## 10. 本地 witness 与保留边界

exact 0.1 baseline 与 mechanical worlds 均从仓库外 evidence root 运行，没有修改产品、Schema、fixture、test 或 oracle。
首次扩展本地矩阵调用没有绑定 repository `src`，在导入 `tests.test_markdown` 时留下
`LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`；已执行的 32 项中 32 项通过，1 个 test module import ERROR。fresh
attempt 只修调用方 `PYTHONPATH`，没有修改产品、文档语义、test 或 oracle。当前 frozen 0.1 regression 加
Markdown/hygiene 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格各为：

```text
36 reported / 36 passed
```

测试只证明 0.1 bytes 仍满足自己的 frozen tests，并证明上述 constructed worlds 的结构差异；它不把 `BLOCKED` 的最终
successor shape、版本号或 aggregation rule 变成已冻结事实。

本审计不改写 doc268 readback 的 setup/reconciliation failures，也不把它们算作 vocabulary product failures。
首次 final-byte checker 对完整 `git status --porcelain` 输出调用 `strip()`，误删首行的 leading status space并把
`AGENTS.md` 读成 `GENTS.md`，保留为 `FINAL_BYTE_SCOPE_PORCELAIN_PARSER_SETUP_ERROR`；fresh attempt 只把整段
输出改为去除结尾换行，没有改变 expected scope、产品字节或 oracle。

## 11. 候选资格链与停止线

本文候选的 tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc267–268、runtime、
tests、workflows、Schema、fixtures、Profile、Policy、identity vectors、corpus 与架构资产保持 base bytes。

final bytes必须完成声明的 Markdown/Schema regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态 marker、
四文件 scope、敏感字面量、上游 frozen-byte continuity、`git diff --check`与read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> current-state audit becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权 correction contract、Schema successor、runtime、tests、composition feasibility/implementation、public
`ReviewSliceSet` / `CoverageLedger` assembler、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
CLAIM_FIDELITY、tag 或 Release。完成资格以后必须重新进入 [CONTROL LOOP](working-method.md)，不能按文档编号自动施工。
