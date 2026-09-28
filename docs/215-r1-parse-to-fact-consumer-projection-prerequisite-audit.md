# R1 Parse → Fact consumer projection 前置资格审计

> 状态：`AUDIT_CANDIDATE / DOCS_ONLY / NO_CONTRACT_AUTHORITY / NO_RUNTIME`
>
> 基线：`main@5593f48256acafeda6205ffde174441781c87c2e`
>
> 证据坐标：文档 214 已完成 original PR、受保护合入、exact-main 双门与 fresh installed-product readback；
> 本文的新反例只重新审查 Parse 成功结果进入 Fact consumer 以前的 operation projection seam。

## 1. 结论

[文档 214](214-r1-parse-fulfillment-precontract-audit.md)的最后门已经闭合，
`R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED` 可以作为 qualified history 使用。但 CONTROL LOOP 在准备起草
Parse 最小合同以前发现了一个更早的接缝：

```text
Language Support ELIGIBLE subjects
    -> current FACT_DERIVATION operation set
    -> all eligible source bodies enter every Fact Provider

future Parse fulfillment
    -> ACCEPTED / REJECTED per subject
    -> only ACCEPTED products may support Fact derivation
```

当前 frozen [文档 208](208-r1-language-support-eligible-operation-projection-contract.md)及其 private implementation
把 Fact operation set 固定为全部 Language Support eligible subjects；request builder、worker validator 与 provider
input 都机械执行这个等式。只要 Language Support eligible 但 syntax-invalid 的 source 存在，current Fact Provider
就仍可取得该 source body，并对它报告 canonical Fact。

因此：

```text
Language Support eligible upper bound
    != post-Parse Fact consumer denominator

current FACT_DERIVATION operation projection
    != proof that rejected Parse subjects cannot enter Fact derivation

Parse precontract audited
    != Parse minimal contract is ready to freeze
```

本文只选择下一个最小问题：**在冻结 Parse contract 以前，先审计并版本化闭合 Parse result → Fact consumer
operation projection / request binding。** 本文不修改文档 208，不起草 correction contract，不实现 parser、AST、
Fact 或新 wire。

## 2. 文档 214 的资格链

文档 214 候选 PR #237 的坐标为：

```text
base  = 5d0769b8ce9d7823b5a095de3657531085d19e83
head  = 9e76639ed42f69e43d7783180be143dee6acc8af
merge = 5593f48256acafeda6205ffde174441781c87c2e
tree  = c5d9fcc726b3c57019b0857c04c0e445f1e08386
```

PR original Public CI `36367307721` attempt 1 为 11/11 SUCCESS。new exact main 的 Public CI
`36400964690` attempt 1 为 11/11 SUCCESS，Browser Smoke `36400964718` attempt 1 为 1/1 SUCCESS。

README 与文档 214 的 fresh formal readback 分别取得 `COMPLETE / PASS`。milestones 第一次正式观察保留为：

```text
Plan    = r1-parse-precontract-milestones
session = github-paired-3dcf5cbcc0cf4a1a93443ab29faa73c9
result  = ERROR / NON_QUALIFYING
cause   = anonymous GitHub API HTTP 403 / remaining = 0
```

该 ERROR 发生在 summary/handoff/Bundle 以前；P2 public render 独立完成。匿名额度 reset 后，fresh Plan
`r1-parse-precontract-milestones-2` 与 session `github-paired-2530d43a51d644479ac9ce394874a690`
取得 `COMPLETE / PASS`。首个 ERROR 没有被删除、重跑或解释成产品 semantic failure。

三份 qualifying readback、四份 exact Git raw bytes、原始门禁与保留 ERROR 经 independent verifier 重新核账，
canonical manifest 为：

```text
sha256_json  = 4c7482a55bbaaf67585568b6e6b84c5cf3d12ec232a5bcbe5d4b85d1d134716b
sha256_bytes = cea42a376fc022da40d3e0b37b2e942475cf1dec25101d0e3ec72706a96b88b0
```

因此本文不是重新做文档 214，也不把后继反例倒写为“文档 214 错误”。后继反例证明的是：文档 214 所要求的
same-attempt Fact consumer binding 暴露了一个当时没有资格解决的更早 input-projection prerequisite。

## 3. 已冻结的 current Fact operation 语义

文档 208 同时冻结：

```text
eligible_subject_ids
    = classification 中全部 ELIGIBLE subject identities

FACT_DERIVATION operation_subject_ids
    = eligible_subject_ids

Provider-visible bodies
    = exact operation bodies
```

文档 208 §6.4 明确把 stage-specific operation set 称为 **exact request denominator**，并把少传一个 required
Fact operation subject 列为应拒绝 world；§13 又把 Parse fulfillment 与 Fact obligation correction 留作
non-decision。

当前 runtime 与该历史合同一致：

1. `build_fact_derivation_source_operation_projection()` 把 `operation_subject_ids` 直接设为全部
   `eligible_subject_ids`；
2. `build_prepared_fact_source_operation_attempt()` 没有 Parse result/product 输入，在 child claim 前直接构造上述
   projection 与 request；
3. `_validate_fact_projection()` 强制 `operation_subject_ids == eligible_ids`；
4. request builder 复制每个 operation subject 的 exact body；worker validator 要求 body cardinality、顺序、path、
   size 与 digest 和 operation set 恰好相等；
5. closed Fact Provider 对 `supported_paths` 产生 candidate Fact，不运行 parser。

所以这里不存在一个已实现但未记录的 Parse filter，也不存在 caller 可以合法传入的 accepted-subject subset。

## 4. Paired-world falsifier

仓库外 audit-only script 位于：

```text
<local-workspace>/tmp/parse-fact-boundary-audit/falsifier.py
```

script SHA-256：

```text
d49cff8b4564fb6206e250ea037a58a2313deda43e785697f3862cca1c9f9889
```

它构造同一个 Snapshot / Policy / Profile 中的两个 first-party UTF-8 Python subjects：

| path | Language Support | independent parse witness |
| --- | --- | --- |
| `pkg/valid.py` | `ELIGIBLE` | `ACCEPTED` |
| `pkg/invalid.py` | `ELIGIBLE` | `REJECTED` (`SyntaxError`) |

current projection/request 的结果为：

```text
FACT_DERIVATION operation paths
    = [pkg/invalid.py, pkg/valid.py]

validated Fact Provider paths
    = [pkg/invalid.py, pkg/valid.py]

proposed Parse accepted paths
    = [pkg/valid.py]

current closed Fact Provider reported Fact path
    = [pkg/invalid.py]
```

把 request body set 收窄为 `pkg/valid.py`，即使没有伪造新 Fact，也会被 current Fact wire 拒绝为
`FactSourceOperationProtocolError`，因为 request 不再与 frozen operation set 恰好相等。

CPython 3.10.6 / 3.13.13、normal / `-O` 四格各产生 1041-byte canonical report，逐字节一致：

```text
bf42f8051226388e3823b92f572a570071f2ec513c455d7c14685f283260203f
```

这些结果只证明 current source/runtime 与 frozen contract 的实际行为；它们不拥有 correction contract authority。

## 5. 为什么不是 harmless upper bound

把 current Fact request 解释为“Provider 可以看到、但不一定消费的上界”无法闭合当前矛盾：

1. 文档 208 已把 Fact operation set 定义为 exact request denominator，不是可选 exposure cap；
2. current Provider 没有 Parse product/result 输入，也没有冻结规则要求忽略 Parse-rejected subjects；
3. falsifier 中 Provider 实际对 rejected subject 报告了 canonical `MODULE` Fact；
4. 文档 214 要求 Fact 取得同一个 admitted parse product 或可验证 product identity，自行 reparse 或仅凭 raw bytes
   不能继承 upstream Parse authority；
5. rejected body 若继续通过 side channel 暴露给 Fact Provider，application 也无法只凭 terminal output 证明它未被
   消费。

因此 current operation projection 可以继续作为**历史上的 pre-Parse Language Support eligibility gate**，却不能在
没有版本化 correction 的情况下冒充 future post-Parse Fact consumer projection。

## 6. 不推翻哪些历史事实

本文不宣布文档 208 或 A–G runtime 在其原 claim domain 内失效。它们仍然正确证明：

```text
OUT_OF_SCOPE / Language Support UNSUPPORTED bytes
    cannot enter current source-body operations

same semantic projection
    does not inherit another attempt's live claim

Provider-visible bodies
    exactly match the current operation projection
```

新事实只切断以下外推：

```text
current exact Fact operation projection
    -> future Parse-authoritative Fact consumption is already ready
```

这是上层 consumer requirement 暴露下层未承诺的义务，不是把历史 qualification 倒改成失败。

## 7. Authority topology

当前可以保留的 owner 切分是：

| Authority | Owner | 明确不拥有 |
| --- | --- | --- |
| Language Support eligible upper bound | frozen classifier / application validation | parser、Fact Provider |
| Parse denominator | application 从 exact eligible subjects 导出 | caller、Provider duplication |
| per-subject Parse semantic result/product | admitted versioned parser execution + application validation | Fact output、descriptor metadata |
| post-Parse Fact consumer membership | future application-owned projection/reconciliation seam | current Fact Provider、caller subset、reported Facts |
| Fact candidate production | Fact Provider under qualified consumer request | Parse terminal rewrite、consumer denominator rewrite |
| continuation | original same-attempt authority chain | equal bytes/digest/result from another attempt |

本文只证明 `post-Parse Fact consumer membership` 尚无可继承的 frozen projection。它没有命名 carrier、字段或类。

## 8. 下一 precontract 必须回答的问题

本文最后门闭合后，下一步最多审计以下问题：

1. current `FACT_DERIVATION` identity 是否只保留为 historical pre-Parse wire；future post-Parse consumer 是否必须
   使用新的 versioned operation/wire/operands identity；
2. post-Parse Fact consumer set 是否由 exact Parse denominator 中全部 qualified `ACCEPTED` subjects 唯一导出，
   `REJECTED` 与 missing/non-success 怎样阻断或收窄后继；
3. successful Parse product / exact product identity 怎样进入 request binding，使 Provider 不能只凭 raw bytes 重新观察；
4. rejected/missing subjects 的 raw bodies 怎样从 Fact Provider authority 中移除，且不存在 document、shared map 或
   side channel；
5. 多个合法 Fact Providers 怎样共享同一份 admitted Parse products，而不复制 Parse truth 或跨 attempt 移植；
6. zero accepted、partial accepted、parser non-success 与 full accepted world 是否启动 Fact child，谁拥有该决定；
7. projection、request、ProviderRun、FactSet 与 downstream continuation 怎样共同绑定同一 parent attempt；
8. correction 是否只需要 versioned private successor，还是确有最小旧合同 wording 需要显式 reopen。

这些是待审问题，不是本文答案。

## 9. 必须拒绝的推理

| ID | world | 必须拒绝的推理 |
| --- | --- | --- |
| `PFC-000` | 一个 eligible source Parse accepted，另一个 rejected；Fact request 仍带两者 | eligible upper bound 等于 post-Parse consumer denominator |
| `PFC-001` | Provider 对 rejected source 报告 canonical Fact | Provider terminal/Fact membership 补做 Parse gate |
| `PFC-002` | caller 把 current request 缩到 accepted subset | caller subset assertion 拥有 consumer projection authority |
| `PFC-003` | request携带 accepted product，但仍有 rejected raw-body side channel | product binding 已建立 least authority |
| `PFC-004` | 同 bytes/Parse result 来自另一个 attempt | semantic equality 继承 live consumer claim |
| `PFC-005` | successful Parse bit 存在，没有 product identity | Fact 已消费同一个 admitted product |
| `PFC-006` | 全部 subjects Parse rejected，Fact Provider返回 empty | Fact/Coverage 已获得 known-empty closure |
| `PFC-007` | 多个 Fact Providers 分别 reparse exact bytes 且结果相同 | 多次新 observation 等于一个共享 Parse truth |
| `PFC-008` | doc208/A–G 历史测试全绿 | future Parse-authoritative consumer boundary 已冻结 |

## 10. 明确 non-decisions

本文不决定或授权：

```text
Parse function / parser runtime / subprocess topology
Parse terminal enum / reason composition
AST normalization / carrier / digest / persistence
post-Parse Fact projection document shape or class
wire / operands / ProviderRun version number
zero-accepted child scheduling
Fact obligation-universe derivation or fulfillment
public Artifact / Schema / Evidence / Manifest / publisher / Bundle
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / Coverage
CLI / Workbench / release
```

Language Support 0.2、current projection 0.1、current corrected private wires 与既有 Fact/Relation/Slice history 不被
静默重写。若后继选择新 identity，旧 identity 与历史 bytes 继续只读。

## 11. 条件化状态

本文只条件化发布：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED
R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

`PRECONTRACT_AUDITED` 来自文档 214 已闭合的独立资格链；新 prerequisite 仍只是 audit candidate。不得因同一状态块
同时出现两者，就把新反例写成 correction contract 已冻结。

## 12. 本地候选资格

第一次静态 checker invocation 在收集 changed paths 时把两组 PowerShell 输出包装成嵌套数组，因而以
`System.Object[]` scope mismatch 停止。该次没有进入候选内容检查，保留为
`INVALID_LOCAL_CHECKER_SETUP`，不记作文档、产品或语义 failure。

修正 checker 的 path collection 后，最终四文件候选通过：

```text
changed scope                         4/4 PASS
relative Markdown links                  PASS
UTF-8 without BOM / LF / final LF         PASS
balanced fences                           PASS
candidate marker                     4/4 PASS
base identity                             PASS
referenced frozen/source inputs unchanged PASS
git diff --check                          PASS
```

绑定 exact checkout 的 Core 与 Review Attention source paths 后，以下 suite 在 CPython 3.10.6 / 3.13.13、
normal / `-O` 四格各 `40/40 PASS`：

```text
tests.test_markdown
tests.test_review_r1_admission_evidence_schema
tests.test_review_r1_derivation_evidence_schema_correction
tests.test_review_r1_schema_payload
```

这些结果只使最终本地候选具备提交资格，不替代 original PR、exact-main、installed-product readback 或 independent
reconciliation。

## 13. 本候选自己的最后门

本文是 docs-only audit candidate。条件化状态只有在以下链条全部成立后生效：

```text
final README / AGENTS / milestones / 本文 bytes
    -> local docs / Schema / static gates
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> prerequisite audit candidate becomes qualified history
```

任一 failure、ERROR、setup failure 或 UNKNOWN 保留原 identity；后继 PASS 不改写历史。audit script、测试与
current Provider output 只作 witness，不拥有新 contract authority。

## 14. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP。下一步最多进入
`Parse result → Fact consumer projection / request binding` 的最小 precontract audit；不得直接修改文档 208、实现新
projection/wire/parser/AST/Fact、选择 persistence 或恢复 ReviewSliceSet/Coverage。

如果新的反例证明该问题还能拆成更早的 product-identity、least-authority 或 multi-Provider seam，只重开最小被击穿
边界；文档编号与绿色门禁都不能自动调度 correction contract。
