# R1 Parse fulfillment 最小合同前置审计

> 状态：`R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED /
> R1_PARSE_FULFILLMENT_PRECONTRACT_AUDIT_CANDIDATE /
> R1_PARSE_FULFILLMENT_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 基线：`main@5d0769b8ce9d7823b5a095de3657531085d19e83`
>
> 上游问题审计：[Parse fulfillment authority 问题审计](213-r1-parse-fulfillment-authority-problem-audit.md)

文档 213 的 original PR、受保护合入、new exact-main 双门、README / doc213 / milestones fresh installed-product
readback 与 independent reconciliation 已全部闭合。它据此成为 qualified problem history，但没有同时给出
Parse 合同答案。

本文只把该问题边界压成下一份最小语义合同必须覆盖的表面。它不发布合同，不实现 parser，不创建 AST carrier、
receipt、Schema 或 public Artifact，也不授权 Fact fulfillment、Coverage 或共同 ledger。

## 1. 当前问题

当前 exact source world 已经拥有：

```text
exact SourceSnapshot / Policy / Profile
    -> deterministic Language Support classification
    -> exact ELIGIBLE subjects
    -> eligible-only operation projection
    -> same-attempt one-shot gate
    -> Provider-visible exact bytes
```

但 current Fact Provider 可以在没有调用 parser 的情况下对 syntax-invalid bytes 报告 `COMPLETED` 和 `MODULE`
Fact。因而下一合同不能从 Provider lifecycle 或 Fact membership 倒推 Parse fulfillment，而必须独立回答：

```text
谁定义 Parse denominator？
哪一个 versioned function 的成功或拒绝算 Parse 事实？
semantic result、execution lifecycle 与 missing obligation 怎样分离？
成功 Parse product 怎样被后继 Fact stage 消费而不重新观察？
```

## 2. 停止线

本文不修改：

```text
runtime / parser / tests / fixtures
SourceSnapshot / ReviewPolicy / DerivationProfile
Language Support 0.2 / eligible operation projection / same-attempt gate
Provider descriptor / ProviderRun / FactSet / RelationSet / Slice
public Schema / compatibility corpus / identity vectors
CoverageLedger / Evidence / Manifest / publisher / Bundle
```

现有 `review-coverage-ledger-0.1` 中出现 `UNSUPPORTED_SYNTAX_VERSION` 与 `PARSE_ERROR`，只证明 Schema 可以承载
这些字符串；它不拥有 reason semantics，也不能反向决定 private Parse 合同。

## 3. denominator 与 obligation ownership

### 3.1 denominator 来自 exact Language Support result

首版 Parse denominator 必须恰好等于同一个 exact `OwnedLanguageSupportClassification` 中全部 `ELIGIBLE`
subjects 的有序集合：

```text
exact Language Support classification
    -> all and only ELIGIBLE subject identities
    -> Parse denominator
```

Language Support 已经拥有 scope/support qualification；Parse 不得重新加入 unsupported subject、删除 eligible
subject，或按 Fact Provider 实际返回的 Fact 缩小考试范围。zero-eligible world 可以产生 known-empty Parse
denominator，但它本身不证明后继 Fact/Coverage 已闭合。

### 3.2 一个 subject 只有一个共享 Parse obligation

current multi-Provider Fact composition 会把同一组 eligible subjects 分配给多个 Provider。该 duplication 是现有
test topology，不是 Parse denominator authority。若按 Provider 数量复制 Parse obligation，将得到：

```text
same exact source
    -> parser observation A
    -> parser observation B
    -> disagreement has no authoritative owner
```

因此一个 exact eligible subject 在一次 parent attempt 中只有一个共享 Parse obligation。多个 parser worker 或
Fact Provider 可以产生 observation，但必须由 application-owned reconciliation 归入这一个 obligation；它们不能
各自创建互不相干的 shared Parse truth。

## 4. versioned parser semantics

### 4.1 `PYTHON_3_10` 不足以唯一标识 parser function

Profile 的 `language_semantics = PYTHON_3_10` 只给出语言目标，尚未冻结 patch-level parser implementation、
invocation flags、AST schema 或 normalization。Python 官方文档明确把新版宿主上的
[`ast.parse(feature_version=...)`](https://docs.python.org/3.13/library/ast.html#ast.parse)称为 best-effort，并声明
成功或失败不保证与目标 Python 版本真实运行结果相同。CPython 也保存过 lower `feature_version` 接受目标版本
不支持语法的[公开缺陷](https://github.com/python/cpython/issues/96587)。

因此：

```text
host ast.parse(feature_version=(3, 10))
    !=
CPython 3.10.6 parser identity
```

ambient host、`sys.version_info`、未绑定 patch version 的 AST classes 与 Provider 自报 descriptor 都不能成为
implicit authority。下一合同必须冻结一个可审计 parser/function identity，并明确 mode、type-comment handling、
feature flags、resource bounds 以及成功 output 的语义边界。

### 4.2 grammar parse 不等于 executable validity

Python 3.10 文档同时说明：[`ast.parse()`](https://docs.python.org/3.10/library/ast.html#ast.parse)成功不会执行
完整 compilation/scoping checks；例如 top-level `return 42` 可以形成 AST，但不能独立编译。

R1 当前需要的是供源码 Fact derivation 消费的 syntax tree，不是证明源码可执行。因此首版 Parse semantic success
最多承诺：

> frozen parser function 对 exact decoded source 返回一个符合其冻结 output contract 的 parse product。

它不承诺 import 可解析、name/scope 正确、bytecode 可生成、程序可执行或运行行为正确。若未来需要 compile-validity，
必须另开 authority seam，不能把它偷进 `PARSE_ERROR`。

## 5. semantic result、execution lifecycle 与 reconciliation 必须正交

下一合同至少需要机械区分三层：

```text
semantic Parse result
    parser accepted / parser rejected exact subject

execution lifecycle
    completed / interrupted / failed / unavailable

denominator reconciliation
    exactly one admitted result / missing / duplicate / dangling / cross-attempt
```

最终 enum 名称仍未授权，但语义关系必须保持：

- parser reject 是一次已执行 observation 的 semantic result；
- infrastructure failure、resource stop 或 parser unavailable 没有资格伪装成 syntax reject；
- `never attempted` 不是 parser 产生的 terminal result，而是 application 对 denominator 发现的 missing obligation；
- duplicate、dangling 与 cross-attempt result 不是第二种成功，必须由 reconciliation 拒绝；
-只有 lifecycle 与 reconciliation 都允许时，semantic success 才能产生后继 continuation。

这延续 VeriTrail 已有的基本分离：执行发生、语义结论和继续行动的 authority 是三件事。

## 6. `UNSUPPORTED_SYNTAX_VERSION` 当前不可机械声明

一个 CPython 3.10 parser 对以下两类 source 都只会给出 syntax rejection：

```text
valid in a later Python version, invalid in 3.10
ordinary malformed source, invalid in every compared version
```

要区分二者，需要另一个冻结且有 authority 的 version discriminator。用 ambient current-host parser 作为第二
oracle 会让结论随宿主升级漂移；本轮 audit 中 `except*` 在 CPython 3.10.6 current compile 与 3.10 feature parse
均失败，而在 CPython 3.13.13 current compile 成功、3.10 feature parse 失败，已经展示该漂移。

因此首版最小合同可以冻结“目标 parser 拒绝”这一事实，但在另一个 version-discrimination contract 成立前，
不得声称该拒绝必然是 `UNSUPPORTED_SYNTAX_VERSION`。现有 public Schema vocabulary 不是补足该 authority 的证据。

## 7. authority owners 与 binding

### 7.1 owner 切分

| Authority | Owner | 明确不拥有 |
| --- | --- | --- |
| Parse denominator | application 从 exact Language Support classification 导出 | parser / Fact Provider 不得增删 denominator |
| parser semantics | frozen contract + 版本化 implementation/conformance identity | ambient host 与 descriptor 自报不拥有 |
| per-subject observation | admitted parser execution | parser 不得自证 denominator complete |
| terminal validation / reconciliation | application-owned qualification gate | Fact Provider 不得把 Fact list 反填为 Parse closure |
| Fact candidate production | 后继 Fact stage | 不得重解释 upstream Parse result |
| continuation | original same-attempt authority chain | semantic equality不继承另一次 attempt 的 authority |

parser 是 observation producer，不是 denominator owner 或最终 qualification authority。application 可以验证 frozen
shape、binding 与 complete reconciliation，但也不能在 parser 从未运行时自行补写 success。

### 7.2 minimum binding semantics

每个 admitted Parse result 至少必须绑定：

```text
exact Language Support subject identity
exact blob identity / bytes
source snapshot + Policy + Profile coordinates
versioned parser/function identity and invocation semantics
eligible operation projection
original BudgetContext / parent attempt / one-shot child claim
terminal lifecycle and reconciliation identity
```

相同 path、相同 bytes、相同 parser output 或相同 semantic disposition，都不能自动继承另一 attempt 的 live
continuation。descriptor 中存在 `parser_id / parser_version` 只证明 metadata 出现，不证明该 function 被执行。

## 8. successful Parse product 到 Fact 的消费边界

只保存 `parser accepted` 的 terminal bit 不足以支撑 Fact fulfillment。若 Fact Provider随后重新 parse exact bytes，
它产生的是另一次 observation；即使结果看起来相同，也不能继承 upstream Parse success 的 authority。

下一合同必须要求：

```text
admitted Parse success
    -> exact, immutable/copy-owned parse product or verifiably bound product identity
    -> same-attempt Fact consumer
```

Fact stage 可以消费该 product 并按自己的 frozen projection rule 枚举 Fact obligations，但不能：

- 用自己重新 parse 的结果改写 upstream Parse terminal；
- 用 reported Facts 反向证明 parse product complete；
- 省略 product identity 后只凭 `COMPLETED` 或 source bytes 声称同一 observation；
- 把 AST schema、Fact candidate universe 与 Parse success 混成一个自证 output。

本文不决定 parse product 是 private in-memory value、canonical normalized tree、AST digest 还是其他 carrier；但若
后继 Fact consumer 不能取得同一个 admitted product 或验证其 exact identity，Parse success 不能为 Fact
fulfillment 提供 authority。

## 9. persistence 仍是 non-decision

两条路线继续保持 OPEN：

```text
Route A
private same-attempt immutable parse product
    -> live Fact consumption

Route B
canonical derived parse projection
    -> historical / offline verification
```

当前只证明 same-attempt consumer 需要 exact product binding。public/offline consumer 是否必须 self-contained、
是否保证 reacquire exact bytes/parser，以及 Language Support Route A/B 如何与 Parse 对齐，仍须由后继消费边界裁决。
不能因为未来可能需要 Bundle 就现在创建 public AST/receipt，也不能因为 live path 足够就预判 persistence 永远不需要。

## 10. 资格否定矩阵

| ID | 已知世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `PFP-000` | Language Support subject 为 `ELIGIBLE` | eligibility 等于 Parse success |
| `PFP-001` | 两个 Fact Providers 都收到同一 eligible set | Parse denominator 按 Provider 数量复制 |
| `PFP-002` | descriptor 携带 parser metadata | parser 实际运行且具备 frozen semantics |
| `PFP-003` | host 3.13 `feature_version=(3,10)` 接受/拒绝某 source | 结果等价于 CPython 3.10.6 oracle |
| `PFP-004` | `ast.parse` 返回 AST | source 可编译或可执行 |
| `PFP-005` | target parser 拒绝 source | 可机械断言 `UNSUPPORTED_SYNTAX_VERSION` |
| `PFP-006` | ProviderRun `COMPLETED` | denominator 每个 subject 恰好有一个 Parse result |
| `PFP-007` | parser unavailable / execution failed | 可以伪装成 semantic syntax rejection |
| `PFP-008` | denominator member 没有 result | `never attempted` 是 parser terminal outcome |
| `PFP-009` | Fact Provider 重新 parse 得到相同 tree | 新 observation 继承 upstream success authority |
| `PFP-010` | successful terminal bit 存在 | Fact consumer 已取得 exact admitted parse product |
| `PFP-011` | same bytes + same semantic result | 另一 attempt 可继承 one-shot continuation |

## 11. 审计实证

仓库外 audit-only script 位于：

```text
<local-workspace>/tmp/parse-precontract-audit/parse_matrix.py
```

script SHA-256：

```text
6bbfb033193650d8f2a3fffbc0b18ba48fed62b315fd80298c55d52f8ec97fab
```

它在 CPython 3.10.6 / 3.13.13、normal / `-O` 四个独立进程中检查 grammar parse、current-host
compile 与完整 AST field shape。normal / `-O` 在各自版本内除 optimize metadata 外语义相同；四份 report 为：

```text
a77c3b60a7e206688e25ec975ba62690611b212077a1c70f00789cb5b5aa7b05  py310-normal.json
fcec849c53de3531afe5a46b3fc693c512be267b2ff3f012cae2bddc2b005b74  py310-opt.json
3df689c408c17fd94e8703b58ebf799e94a5bf3780d5610f1ee8e338e14c4d50  py313-normal.json
4f5d50f7c75bc8c1210cc7a73ab3b680dfd5ea8a8275246acfc3bf328f6d9915  py313-opt.json
```

关键 observations：

- same Python 3.10 function/class source 在两宿主均 parse success，但 3.13 AST fields 额外包含 `type_params`；
- `match` 的本轮 normalized shape 相同，说明 drift 不是“所有 tree 必然不同”，而是不能无证据假设等价；
- `except*` 在两宿主的 3.10 feature parse 都拒绝，但 current-host compile 只在 3.13 成功；
- top-level `return 42` 在两宿主都 parse success、compile failure；
- ordinary malformed source 在两宿主都 parse/compile failure。

这组 report 是 precontract falsifier，不是正式 product Evidence。它没有选定 future parser，也不证明有限 corpus
覆盖全部 grammar；它只足以拒绝 ambient-host equivalence、AST-shape equivalence 与 parse-success/compile-validity
三种未经证明的推理。

## 12. 下一合同的最小边界

本审计自己的最后门闭合后，最多授权一份 docs-only minimal contract 冻结：

```text
Parse denominator = exact Language Support ELIGIBLE subjects
one shared obligation per exact subject / parent attempt
versioned parser/function and invocation semantics
grammar-parse success boundary, excluding compile/execution claims
semantic result / execution lifecycle / denominator reconciliation separation
exactly-one admitted result or explicit missing/invalid reconciliation
UNSUPPORTED_SYNTAX_VERSION non-authority until a discriminator is frozen
exact subject/blob/Profile/projection/attempt/one-shot binding
application / parser / Fact Provider authority separation
same-attempt exact parse-product consumer boundary
persistence as an explicit non-decision
```

合同可以命名最少的 private semantics，但不得由现有类名、Schema enum 或 audit script 反推 solution shape。

## 13. 明确 non-decisions

本文不授权：

```text
real parser implementation / subprocess topology
canonical AST serialization / normalized tree algorithm / AST digest
Parse class / enum / receipt / result / ledger / public Artifact / Schema
UNSUPPORTED_SYNTAX_VERSION discriminator
Fact obligation-universe derivation or fulfillment
Language Support / Parse persistence Route A/B
shared Language Support / Parse / Fact carrier
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
CLI / Workbench / release
```

existing Language Support、Fact/Relation、Slice 与 public Schema 均不被重解释。

## 14. 本候选自己的最后门

本文是 docs-only precontract audit candidate。条件化状态只有在以下链条全部成立后生效：

```text
final README / AGENTS / milestones / 本文 bytes
    -> local docs / Schema / static gates
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> PRECONTRACT_AUDITED becomes qualified history
```

任一 failure、ERROR、setup failure 或 UNKNOWN 保留原 identity；后继 PASS 不改写历史。official docs、CPython issue、
audit script 与测试都只是 witness，不拥有 contract authority。

## 15. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新判断 Parse minimal contract 是否仍是最小
合法问题。本文编号、官方文字、本地四格或绿色 CI 都不能自动授权 parser、AST carrier、runtime、Fact、persistence、
Coverage 或 public Artifact。

若后继反例证明 patch-level parser semantics、parse-product identity 或 same-attempt consumer binding 仍缺更早前提，
只重开被击穿的最小 seam；不得按文档编号机械进入 implementation。
