# R1 Parse fulfillment authority 问题审计

日期：2026-09-28

## 1. 文档身份与条件状态

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDIT_CANDIDATE /
> R1_PARSE_FULFILLMENT_PRECONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@0c82c55a521750698c969b26221bf776530aec16`，Git tree
> `5ca3bb0952360ec05c9c4a3ba1ee8e46cfe6843d`
>
> 冻结上游：[Language Support 0.2 合同](202-r1-language-support-codec-conformance-correction-contract.md)、
> [eligible operation projection 合同](208-r1-language-support-eligible-operation-projection-contract.md)与
> [private implementation 重新资格化发布](212-r1-language-support-eligible-operation-projection-implementation-freeze-requalification.md)
>
> 影响层级：`L3_SYSTEM_AUDIT + L2_CONTRACT_PROBLEM_BOUNDARY + L0_DOCUMENTATION`。本文只判断 Parse
> fulfillment 是否仍是当前最小合法问题，以及 current exact history 能证明到哪里；不创建或修改 runtime、tests、
> parser、AST carrier、terminal enum、Schema、Profile、Policy、Fact、Relation、Slice、Coverage、Evidence、
> Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文不是 Parse precontract，不授权 parser implementation，也不预选 `ParseReceipt`、`ParseOutcome`、
`ObservationLedger` 或共享 carrier。本文只回答：

> Language Support 0.2 classification、eligible-only source operation projection 与 same-attempt gate 已冻结后，
> 系统是否已经拥有每个 eligible parse unit 的 terminal Parse fact？

## 2. 上游 private implementation freeze 已成为事实

文档 212 的 publication PR #233 head 为 `ced2984fcf79c9b391bbbea681b8ba658f2a68dd`，original Public CI
`36353138086` attempt 1 为 11/11 SUCCESS。ordinary merge 后的 exact main 是
`0c82c55a521750698c969b26221bf776530aec16`；Public CI `36354589236` attempt 1 为 11/11 SUCCESS，
Browser Smoke `36354589265` attempt 1 为 1/1 SUCCESS。

README、文档 212 与 milestones 随后完成 fresh anonymous installed-product readback。README 与文档 212
首次正式 observations 直接 PASS。milestones 前两次正式 observations 均完成匿名采集与 Core `PASS`，但 runner
在写入长文件名 final summary 时触发 Windows path boundary，进程退出 1，因此两个 identity 永久保持
`ERROR / NON_QUALIFYING`：

| Identity | Plan | Session | Product report | Qualification |
| --- | --- | --- | --- | --- |
| `FORMAL-MILESTONES-001` | `r1-lspg-impl-requal-milestones` | `github-paired-3c9af6b236e54351a55a06de52e9da71` | `COMPLETED / PASS` | `ERROR` |
| `FORMAL-MILESTONES-002` | `r1-lspg-impl-requal-milestones-2` | `github-paired-9ecd7e20cb46460ebe542af0803e994a` | `COMPLETED / PASS` | `ERROR` |

资产随后只做 byte-preserving short-root copy；没有覆盖上述 output。第三次 milestones observation 使用新 Plan、session
与 output，和 README、文档 212 一起形成三份互不复用的正式 PASS：

| Target | Plan | Session | Result |
| --- | --- | --- | --- |
| README | `r1-lspg-impl-requal-readme` | `github-paired-e7728ab37857493b9872e74e2e3246de` | `COMPLETE / PASS` |
| 文档 212 | `r1-lspg-impl-requal-doc212` | `github-paired-503e35607f374ccdb27028996810b789` | `COMPLETE / PASS` |
| milestones | `r1-lspg-impl-requal-milestones-3` | `github-paired-18a6303cca2e43e0b64a5776d2d1582c` | `COMPLETE / PASS` |

四份 public raw bytes 与 exact Git blobs 相等；installed-product Core 独立重算并核对两次保留 ERROR 后生成最终
manifest：

```text
sha256_json  = 0354060769104d5647c322838740fc64af0c8e96d333698bdef963345fd16e82
sha256_bytes = 669c4af61877e8c9287a742bacb20b9dfc794ee0c30c4c0cc4f287ca6da00b08
```

因此当前审计消费的是已经生效的：

```text
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN
```

本文不追加 implementation freeze 的事后门，也不把两次 path error 重写成产品失败。

## 3. CONTROL LOOP 结论

重新绑定 exact main 后，Parse fulfillment 仍是最小合法问题，但其输入边界已比文档 195 时更窄：

```text
exact frozen source world
    -> r1-python-language-support/0.2 exactly-one classification
    -> exact ELIGIBLE subject identities
    -> FACT_DERIVATION operation subject set
    -> same-attempt one-shot source-body claim
    -> Provider-visible exact eligible bytes
```

文档 208 A–G 已经补齐“哪些 exact bytes 有资格进入哪个 child operation”与“该资格是否仍属于原 live
attempt”。它没有新增：

```text
per-eligible-subject parser execution
per-unit terminal Parse outcome
exact parse-result / AST identity
Parse denominator reconciliation
Parse-to-Fact consumption authority
```

因此：

```text
eligible input authority
    != parse execution
    != parse fulfillment
```

该缺口不是 current closed Fact Provider defect。closed Provider 的冻结用途是验证 execution-cell、替换、预算、
terminal、Fact identity、multi-Provider composition 与 provenance；它从未承诺真实 Python parser。

## 4. authority owner 重新核账

| 对象 | 当前 owner / source | 当前不能推出 |
| --- | --- | --- |
| Parse denominator 候选 | Language Support 0.2 `ELIGIBLE` subjects | 已逐项执行 parser |
| exact source bytes | copy-owned exact inputs + source operation projection | bytes 已形成 AST |
| live attempt / stop boundary | original `BudgetContext`、parent/child `AttemptEligibility` 与 one-shot claim | semantic equality 可继承另一次 attempt |
| Provider descriptor | capability/provider/parser/runtime identity metadata | 对每个 unit 的 parser 实际执行证据 |
| ProviderRun terminal | child run lifecycle | Parse denominator 已逐项闭合 |
| FactSet | reported Fact identity、membership、composition 与 provenance | 未报告 unit 已被 parse；Fact 输出可证明 parse success |

Parse 的 grammar / parser function authority、逐项 terminal fact owner 与 minimum parse-result identity 仍是
`UNKNOWN`。application 可以验证冻结后的 canonical shape，但当前不能在没有 parser observation 的情况下补写
Parse 事实；Fact Provider 也不能用自己的 Fact list 定义 Parse 考试范围。

## 5. paired exact-world 反例

审计在仓库外目录只读复用 exact main 的 Language Support classifier、Fact source-operation controller、两个 required
closed Fact Providers 与真实 same-attempt gate。两个 world 保持相同 path、size、Policy/Profile、Provider set 与
controller path，只改变 exact bytes：

| World | Exact source | Independent Python 3.10 parse |
| --- | --- | --- |
| `PFQ-VALID` | `def ok():\n 0\n` | `SUCCESS` |
| `PFQ-SYNTAX-ERROR` | `def broken(:\n` | `SYNTAX_ERROR` |

两份 source 都是 13 bytes，均被 Language Support 0.2 分类为单一 `ELIGIBLE` member，并进入两个
`veritrail-review-derivation-cell/0.2` child 的 exact one-subject operation projection。current result 对两个 world
给出完全相同的 terminal shape：

```text
required Provider attempts       = 2
ProviderRun statuses             = [COMPLETED, COMPLETED]
phase statuses                   = [COMPLETED, COMPLETED]
diagnostic codes                 = [null, null]
reported Fact count              = 1
reported Fact kind               = MODULE
overall execution                = COMPLETED
normal continuation              = true
per-unit parse outcome fields    = []
```

closed Fact Provider source 不调用 `ast.parse`。Provider descriptor 中出现 `parser_id / parser_version` 只证明 identity
metadata 被携带，不证明 parser 对任一 subject 实际运行。

审计脚本位于仓库外：

```text
<local-workspace>/tmp/veritrail-r1-parse-fulfillment-audit-0c82c55/
```

脚本 SHA-256：

```text
07448701daa0cb5621de3dea9da89f04ffe280be26faec95253410e4d8ff1ffa
```

CPython 3.10.6 / 3.13.13、normal / `-O` 四格严格串行运行，四份 4479-byte canonical report 逐字节相同：

```text
a942cf2662706b35a75140c16d5332754e9665ef2ca937068101a60ae61c4ce4
```

该反例是 contract/problem-boundary falsifier，不是正式 product Evidence。它证明 current exact history 无法区分：

```text
eligible unit -> parser SUCCESS
```

与：

```text
eligible unit -> parser never executed -> closed Fact Provider still reports MODULE
```

它不证明 future Parse implementation 必须使用 audit oracle，也不授权把 `ast.parse(feature_version=(3, 10))` 当作
frozen product parser。

## 6. downstream parser 不能反向补证

current Relation derivation / observation closed Providers 内部确实会调用 `ast.parse(..., feature_version=(3, 10))`。
该执行发生在 FactSet 已经形成以后，只接触 Fact/domain 所引用的 operation sources，并把 parser failure 映射到该
Relation Provider 的 lifecycle。它不能反向证明：

```text
all Language Support eligible subjects were parsed
```

也不能为 FactSet 没有引用的 subject 创造 Parse terminal fact。将 downstream Relation parser 提升为上游 Parse
authority，会让 admitted FactSet 先缩小考试范围，再用缩小后的范围证明自己完整，形成 self-certification loop。

## 7. 当前必须拒绝的结论

| ID | 当前 exact world | 必须拒绝的结论 |
| --- | --- | --- |
| `PFQ-000` | Language Support subject 为 `ELIGIBLE` | eligibility 等于 parse success |
| `PFQ-001` | exact eligible bytes 进入 same-attempt Provider request | input authority 等于 parse execution |
| `PFQ-002` | descriptor 携带 `parser_id / parser_version` | identity metadata 证明 parser 实际运行 |
| `PFQ-003` | required ProviderRuns 均 `COMPLETED` | whole-run terminal 证明 per-unit Parse closure |
| `PFQ-004` | syntax-invalid bytes 仍产生 `MODULE` Fact | Fact membership 证明 parse success |
| `PFQ-005` | Relation Provider 后续运行 parser | downstream subset observation 可补齐 upstream denominator |
| `PFQ-006` | valid / invalid world terminal shape 相同 | current carrier 有资格填入同一个 Parse outcome |
| `PFQ-007` | 两 world 都允许 normal continuation | continuation 等于 Parse fulfillment authority |

## 8. 后继 precontract audit 必须回答的问题

本文最后门闭合后，最多授权从新的 exact main 审计以下问题；它们现在仍不是合同答案：

1. Parse denominator 是否恰好等于一个 exact Language Support classification 的全部 `ELIGIBLE` subjects；多个 Fact
   Providers 是否共享一次 Parse responsibility，还是各自拥有不同 observation，不能由当前 duplication 偶然决定；
2. 谁拥有 versioned parser semantics。CPython 3.10.6 runtime、host `ast.parse(feature_version=(3, 10))` 与一个
   normative grammar identity 是否等价，必须由证据裁决，不能信 ambient host；
3. current semantics 至少需要区分哪些 world：parser success、实际 syntax failure、execution/infrastructure failure、
   Provider unavailable 与 never attempted；最终 enum 名称、reason composition 与优先级仍待审；
4. `UNSUPPORTED_SYNTAX_VERSION` 与 `PARSE_ERROR` 是否可被机械区分；若不能，不能为了沿用旧 Schema reason 而编造
   certainty；
5. Parse terminal result 最少怎样绑定 exact subject/blob、Profile、parser/function identity、operation projection、
   original attempt 与 one-shot claim；
6. Fact stage 消费成功 Parse result 时，是否必须获得 normalized parse-result / AST identity；若只保存 terminal
   receipt，application 能否在不重做 observation 的情况下验证 Fact denominator；
7. parser、Fact Provider 与 application 各自可以产生、验证或拒绝什么，怎样避免 producer 同时定义 denominator、
   输出结果并自证 complete；
8. 哪些信息只需要 private same-attempt 使用，哪些未来 public/offline consumer 必须持有；Language Support
   persistence Route A/B 继续保持 OPEN。

顺序必须保持：

```text
独立闭合 Parse problem semantics
    -> 证明最小共同不变量
    -> 才能判断是否复用 lower-level carrier
```

不能先创建一个通用 receipt / ledger，再把 Parse、Fact 与 Language Support 强行装进去。

## 9. 明确 non-decisions

本文不授权：

```text
real parser / AST execution
Parse terminal enum or reason table
Parse receipt / result / Artifact / Schema
Fact projection-universe derivation or fulfillment
Language Support persistence Route A/B
shared observation envelope / receipt / ledger
public Language Support / Parse / Fact carrier
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
CLI / Workbench / release
```

existing Language Support classifier、source operation projection、Fact/Relation semantics、Provider terminal、FactSet、
RelationSet 与 Slice closure 均不被重解释。

## 10. 本候选自己的最后门

本文是 docs-only problem audit candidate。条件化状态只有在以下链条全部成立后生效：

```text
final README / AGENTS / milestones / 本文 bytes
    -> local docs / Schema / static gates
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> problem boundary becomes qualified history
```

任一 failure、ERROR、setup failure 或 UNKNOWN 保留原 identity；后继 PASS 不改写历史。audit script 与测试只是
witness，不拥有 contract authority。

## 11. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新判断 Parse fulfillment precontract audit 是否
仍是最小合法问题。本文编号、四格相等或绿色 CI 都不能自动授予 precontract、parser、AST carrier、runtime、Fact、
persistence、Coverage 或 public Artifact 施工权。

若后继反例证明 denominator、parser semantics 或 same-attempt binding 仍缺更早前提，只重开被击穿的最小 seam；
不得按路线图机械进入 Parse implementation。
