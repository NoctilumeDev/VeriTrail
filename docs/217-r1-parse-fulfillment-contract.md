# R1 Parse fulfillment 最小合同 0.1

> 状态目标（仅[独立冻结发布](218-r1-parse-fulfillment-contract-freeze-publication.md)最后门闭合后生效）：`R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED / DOCS_ONLY / NO_RUNTIME`
>
> 候选基线：`main@63daada4157e0068bb2a1333953f821f56f61894`
>
> 前置审计：[Parse fulfillment authority 问题审计](213-r1-parse-fulfillment-authority-problem-audit.md)、
> [Parse fulfillment 最小合同前置审计](214-r1-parse-fulfillment-precontract-audit.md)、
> [Parse → Fact consumer projection 前置资格审计](215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)与
> [Parse product → Fact consumer binding 最小前合同审计](216-r1-parse-product-fact-consumer-binding-precontract-audit.md)
>
> 冻结上游：[Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [SourceSnapshot runtime 合同](127-r1-source-snapshot-runtime-contract.md)、
> [Derivation Input Binding 合同](132-r1-derivation-input-binding-contract.md)、
> [Derivation Attempt / Fact Provenance 合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)、
> [Language Support Qualification 合同 0.1](198-r1-language-support-qualification-contract.md)、
> [codec-conformance 修正合同 0.2](202-r1-language-support-codec-conformance-correction-contract.md)与
> [eligible-only operation projection 合同 0.1](208-r1-language-support-eligible-operation-projection-contract.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本候选只冻结 Parse denominator、
> versioned parser/function semantics、per-subject semantic result、execution/reconciliation 分离、完整 denominator
> closure、application-owned admitted product/product-set identity、same-attempt product access 与 continuation boundary。
> 它不创建或修改 runtime、parser、AST carrier、Schema、Fact wire、Evidence、Manifest、publisher、Bundle、CLI、
> Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 目的与停止线

文档 213 已证明 current Provider completion、Fact membership 与 parser metadata 都不能证明 Parse fulfillment；文档
214 把 Parse denominator、versioned parser、semantic result、execution lifecycle 与 reconciliation 分开；文档 215
又证明 current Fact wire 仍把全部 Language Support eligible source bodies 作为 operation set；文档 216 最终把
consumer membership、exact product binding 与 product-use authority 拆成三层。

本合同只关闭以下上游语义链：

```text
exact Language Support classification
    -> all and only ELIGIBLE subjects
    -> one shared Parse obligation per subject / parent attempt
    -> versioned parser observation
    -> ACCEPTED with exact product | REJECTED without product
    -> application-owned complete reconciliation
    -> admitted product / product-set semantic identity
    -> same-attempt immutable/copy-owned product access boundary
```

它不冻结 Fact Provider 如何证明实际消费该 product，不决定 zero-accepted world 是否启动 Fact child，也不选择 product
carrier、digest algorithm 或 persistence 路线。即使本候选以后冻结，任何代码施工仍须由独立实现资格审计授权；本文
字节本身不授予 runtime authority。

## 2. authority topology

Parse 0.1 的 authority 固定为：

```text
SourceSnapshot / DerivationInputSet
  拥有 exact inventory、Git object identity 与 copy-owned blob bytes

OwnedLanguageSupportClassification 0.2
  拥有 Parse denominator membership、subject identity 与 effective source encoding

Parse contract + conforming implementation
  拥有 versioned parser/function 与 invocation semantics

admitted parser execution
  只产生一个 exact subject 的 parser observation

deterministic application
  拥有 binding validation、denominator reconciliation、product admission 与 product-set composition

Fact Provider
  不拥有 Parse denominator、Parse terminal、product identity 或 reconciliation authority

same-attempt continuation chain
  拥有从本次 admitted product set 继续申请后继 consumer claim 的 live authority
```

因此：

```text
Language Support ELIGIBLE                 != Parse ACCEPTED
ProviderRun COMPLETED                     != Parse obligation fulfilled
parser_id / parser_version metadata       != frozen parser executed
ast.parse returned                        != source compile-valid or executable
accepted subject IDs                      != exact product-set identity
product identity echoed                   != product consumed
same product bytes                        != same attempt authority
known-empty admitted product set          != Fact or Coverage closed empty
```

## 3. authoritative denominator 与 obligation

### 3.1 唯一 denominator

首版 Parse denominator 必须恰好等于同一个 exact `OwnedLanguageSupportClassification` 0.2 中全部 `ELIGIBLE`
subjects，并保持该 classification 的 raw Git path byte order：

```text
exact classification subjects
    WHERE disposition == ELIGIBLE
    ORDER BY raw Git path bytes
        -> Parse denominator
```

application 必须先重新验证 classification seal、Snapshot / Policy / Profile coordinates、Language Support function
identity、subject identity、exact inventory binding 与 blob bytes。caller、parser、Fact Provider 与 reported Facts 都
不得增删 denominator member。`UNSUPPORTED` subject 不进入 Parse denominator，也不能由 parser 改写其 Language
Support reasons。

zero-eligible world 形成 authoritative known-empty Parse denominator；它只说明本 stage 没有 Parse obligation，不证明
Fact child 应启动、FactSet 为空或 Coverage 已闭合。

### 3.2 每个 subject 只有一个共享 obligation

一个 exact eligible subject 在一次 parent attempt 中恰好对应一个 Parse obligation。worker 数量、Fact Provider 数量、
重试次数或诊断观察次数都不能复制 denominator：

```text
one exact subject / one parent attempt
    -> one application-owned Parse obligation
    -> zero or more execution observations
    -> exactly one admitted semantic result or invalid reconciliation
```

多个执行者可以产生候选 observation，但不能分别创建自己的 Parse truth。application 只能从绑定本 obligation 的
observations 中完成 reconciliation；它也不能在 parser 未运行时自行补写 ACCEPTED 或 REJECTED。

## 4. semantic input identity 与 decoded source

### 4.1 exact subject world

一个 Parse subject 的完整 semantic input 至少绑定：

```text
SourceSnapshot / Policy / analysis-scope / DerivationProfile coordinates
Language Support function and classification identity
exact Language Support subject identity
exact inventory item, Git object identity, size and SHA-256
exact copy-owned blob bytes
effective source encoding
Parse function identity and invocation semantics
```

raw path、blob SHA-256、Language Support subject ID 或 parser descriptor 任一单独字段都不是完整 identity。同一路径、
同 bytes 或同 eligible disposition 出现在另一 exact world 时，不继承本 subject 的 product 或 live claim。

### 4.2 decoded source 只继承已冻结的 encoding result

Parse 不重新运行 encoding detection，也不允许 parser tolerance 扩大 Profile。它只按当前 exact eligible subject 的
`effective_source_encoding` 从 exact blob bytes 导出 parser input：

```text
UTF-8
    -> strict UTF-8 decode of all exact bytes

UTF-8-SIG
    -> require exact UTF-8 BOM
    -> remove that BOM once
    -> strict UTF-8 decode of all remaining exact bytes
```

不得执行 newline normalization、Unicode normalization、locale decode、default encoding fallback 或 replacement decode。
若 blob、encoding 或重新 decode 的结果与 qualified Language Support world 不一致，整个 Parse input binding 失败；
不得把 integrity mismatch 改写成 `PARSE_ERROR`。

## 5. versioned parser/function semantics

### 5.1 function identity

首版函数 identity 冻结为：

```text
r1-python-parse/0.1
```

其规范参照是 **CPython 3.10.6** 对 section 4 exact decoded `str` 执行以下 grammar parse：

```python
ast.parse(
    source_text,
    filename="<veritrail-r1-parse>",
    mode="exec",
    type_comments=False,
    feature_version=(3, 10),
)
```

`PYTHON_3_10` Profile 字符串、ambient `sys.version_info`、较新宿主上的 `feature_version=(3, 10)`、Provider descriptor
自报或“多数样本相同”都不能替代该 function identity。实现可以使用 exact reference runtime，也可以使用另一机制，
但必须以独立 conformance 证明其对授权 input domain 的 semantic result 与 product semantics 等价；宿主 API 成功本身
不是 authority。

### 5.2 semantic acceptance 与 rejection

规范函数返回 `ast.Module` 时，subject 的 semantic disposition 为 `ACCEPTED`，并产生一个 exact Parse product。
规范函数因 source grammar/input 本身拒绝时，disposition 为 `REJECTED`，canonical reason 仅为 `PARSE_ERROR`。首版
source rejection 包括 CPython 3.10.6 的 `SyntaxError` 族，以及 exact decoded text 含 U+0000 时该 reference function
产生的 source-input `ValueError`。

以下情况不属于 semantic rejection：

```text
parser/runtime unavailable
process or worker infrastructure failure
BudgetContext stop or deadline expiry
resource exhaustion or internal parser failure
input/history/integrity binding failure
```

这些 world 没有资格产生 `PARSE_ERROR`，必须留给 execution lifecycle 与 reconciliation 表达。

仓库外 audit-only probe 位于：

```text
<local-workspace>/tmp/probe_parse_exceptions.py
```

script SHA-256 为：

```text
26c61b066574ed2dee67855097a7d1fab5148519cf2c3d5a3f6a5c7c426b86f6
```

同一 NUL input 在 CPython 3.10.6 reference 上产生 source-input `ValueError`，在当前 CPython 3.13.13 host 上产生
`SyntaxError`；两者都拒绝 source，但 exception class 不同。该 witness 只证明 ambient exception class 不能拥有
canonical reason，不是产品 Evidence，也不授权使用当前 host parser。

### 5.3 grammar parse 的上界

`ACCEPTED` 只承诺 frozen grammar function 产生符合 section 7 的 product。它不承诺：

```text
compile / symbol-table validity
import resolution
name, type or scope correctness
bytecode generation
program executability
runtime behavior
```

例如 top-level `return 42` 可以形成 `ast.Module`，但后继 compile 仍可拒绝。compile-validity 若成为需求，必须另开
authority seam，不能倒填到本合同。

### 5.4 不声明 unsupported syntax version

首版没有第二个冻结且独立的 version discriminator。目标 parser 拒绝 source 时，只能声明 `PARSE_ERROR`；不得仅因
较新宿主接受同一文本而声明 `UNSUPPORTED_SYNTAX_VERSION`。diagnostic message、line excerpt、exception class、
traceback 与宿主版本不进入 canonical semantic disposition，也不能决定后继 authority。

## 6. semantic result、execution lifecycle 与 reconciliation

三层必须保持正交：

```text
semantic result
    ACCEPTED(product) | REJECTED(PARSE_ERROR)

execution lifecycle
    parser execution completed | interrupted | failed | unavailable

denominator reconciliation
    exactly one admitted result | missing | duplicate | dangling | foreign/binding-invalid
```

只有 execution lifecycle 允许且 candidate observation 通过 exact binding validation，才可能形成 semantic result。
`never attempted` 是 application 在 denominator reconciliation 中发现的 missing obligation，不是 parser terminal。
duplicate、dangling、foreign-attempt 或 malformed result 也不是第二种 rejection；它们使 normal reconciliation 失败。

具体 private enum、exception hierarchy、worker protocol 与 diagnostic carrier 仍是实现 non-decision，但任何实现都必须
能机械区分上述 world，不能把字段缺失压成最接近的 terminal。

## 7. admitted product 与 product identity

### 7.1 ACCEPTED 必须拥有 exact product

`ACCEPTED` 不能只有 boolean、subject ID 或 parser-completed bit。它必须同时拥有该 exact invocation 返回的 Parse
product；`REJECTED` 不得携带 product。product 至少保留后继 frozen Fact projection 可以观察的完整 tree semantics，
包括 node kind、field values、ordering 与 source-location semantics，不得用只覆盖当前少数 Facts 的摘要冒充完整
product。

本合同不决定 product 是 private immutable tree、copy-owned normalized value、opaque owned object、canonical bytes
或其他 carrier，也不冻结 digest algorithm。任何后继 carrier 若声称 product semantic identity，必须对所有被授权
consumer-observable semantics 完整绑定；path-only、accepted-bit-only、selected-node-only 或裸 digest 都不合格。

### 7.2 semantic identity 与 admission binding 分开

每个 product semantic identity 必须绑定：

```text
exact subject / blob / decoded-source identity
Parse function and invocation identity
exact product semantics
```

该 identity 是 attempt-neutral semantic value，不含 `BudgetContext`、deadline、one-shot handle 或 mutable process state。
application 随后建立单独的 admitted product binding，把 product semantic identity 与 exact `ACCEPTED` result、parent
attempt、obligation 和 reconciliation coordinates 绑定。parser 只能提出 observation，Fact Provider 不能从自己的
输出反向定义 product。相同 accepted subject set 可以对应不同 products，因此 accepted membership 不能成为
product-set semantic identity；相同 product semantic identity 也不能代替本次 admission binding。

### 7.3 immutable/copy-owned access

一旦 product 被 admitted，后继 same-attempt consumer 只能取得该 product 的 immutable/copy-owned view 或能机械解析到
同一 owned value 的引用。consumer 不得修改 upstream product，也不得按 raw bytes 重新 parse 后声称“语义看起来相同”
就是同一 observation。

## 8. complete reconciliation 与 product set

application 必须对完整 Parse denominator 一次性验证：

1. 每个 denominator member 恰好一个 admitted semantic result；
2. 没有 missing、duplicate、dangling、foreign-attempt、cross-world 或 binding-invalid result；
3. 每个 `ACCEPTED` result 恰好一个 admitted product，且 identity 回连 exact subject/function/invocation；
4. 每个 `REJECTED` result 仅有 `PARSE_ERROR`，没有 product；
5. lifecycle non-success 不伪装 semantic result；
6. result order 与 denominator raw Git path byte order一致；
7. denominator、accepted、rejected 形成无遗漏、无重叠 closure。

只有上述条件全部成立，application 才能形成 reconciled product set：

```text
Parse denominator
    = accepted U rejected

admitted product set
    = exact ordered products of accepted members
```

product-set semantic identity 必须绑定 exact denominator semantics、完整 accepted/rejected partition、Parse function 与
每个 admitted product semantic identity，但不得包含 live handle。application 另以 attempt-bound admitted product-set
binding 连接 parent attempt、完整 reconciliation 与该 semantic identity。zero denominator 与 all-rejected complete 都
可以形成 known-empty admitted product set，但两者仍有不同的 denominator/partition semantics 与 reconciliation
history；missing 或 lifecycle non-success 不能通过“accepted list 为空”伪装 known-empty。

known-empty product set 只关闭 Parse stage。它不决定 required Fact Provider 是否启动，也不证明 empty FactSet 或
Coverage closure。

## 9. semantic value 与 live continuation authority

相同 exact semantic input与相同 function 可以在不同合法 attempts 中产生相同 result/product/product-set semantics：

```text
same semantic product set
    != same parent attempt
    != same BudgetContext
    != same deadline/resource ownership
    != same one-shot claim history
    != right to start Fact consumption
```

normal continuation 必须继续绑定 original live `BudgetContext`、parent `AttemptEligibility`、exact Language Support
continuation、Parse child claim、complete reconciliation 与本次 product-set identity。新建 limits 相同的 context、读取
历史 product bytes、比较 digest 或 caller 传入 boolean 都不能恢复 live authority。

attempt-neutral semantic value 与 attempt-bound live claim 必须分开保存和验证。semantic value 可以复算或比较；live
claim 必须针对每次 attempt 独立取得且 one-shot 消费。

## 10. Fact consumer boundary

本合同只建立 future consumer 可以依赖的 upstream truth：

```text
complete Parse reconciliation
    -> application-owned admitted product set
    -> same-attempt immutable/copy-owned product access
```

它不建立 Provider-bound product-use proof。后继 Fact consumer correction contract 必须另行冻结：

```text
consumer membership and versioned successor projection
provider-bound one-shot request claim
product is actually used as derivation authority
rejected/missing/non-success raw bodies are not visible through side channels
Fact output and continuation bind the same admitted product set
zero-accepted Provider scheduling and required-provider closure
```

current `private-source-operation-projection/0.1` 与 Fact wire `/0.2` 继续只解释历史上的 pre-Parse source-body request，
不能通过增加字段静默继承本合同。multiple Fact Providers 可以共享一份 application-owned product truth，但必须各自领取
provider-bound child claim；一个 Provider 的 terminal 不能修改 upstream product set 或替另一个 Provider 领取 claim。

## 11. persistence 是显式 non-decision

本合同同时允许：

```text
Route A
private same-attempt immutable/copy-owned product
    -> live consumer access

Route B
canonical derived product projection
    -> historical / offline verification
```

public/offline consumer 是否被保证能取得 exact bytes、parser 与 product，Bundle 是否要求 self-contained verification，
以及 Language Support 的 persistence 路线怎样与 Parse 对齐，仍须由后继消费边界裁决。工程便利、调试需要或“多留
证据”不能代替该判断。

本合同不新增 public Artifact、Schema role、Evidence field、Manifest entry、Bundle file、output root 或 publisher。
private implementation 也不能仅凭本合同自行把 Route A 解释成永久选择。

## 12. execution 与 resource boundary

所有 Parse execution 必须继续使用 original parent attempt 的 live resource authority，不得创建 limits 相同的新
`BudgetContext`、重置 deadline 或用 retry 生成第二个 normal obligation。exact blob size、现有 artifact budget 与
parent stop reason 继续约束 parser；具体 in-process/subprocess/worker topology 由后继实现审计决定。

deadline、interrupt、resource stop、parser crash 或 unavailable 必须 fail closed 为 lifecycle/reconciliation non-success，
不得自动重试后覆盖首个 observation，也不得改写成 `PARSE_ERROR`。diagnostic retry 若未来存在，必须拥有独立 identity，
且不能替代原 normal attempt。

## 13. 资格否定矩阵

| ID | 已知 world | 必须拒绝的结论 |
| --- | --- | --- |
| `PFCT-000` | Language Support subject 为 `ELIGIBLE` | eligibility 等于 Parse `ACCEPTED` |
| `PFCT-001` | 多个 Fact Providers 需要同一 subject | Parse obligation 按 Provider 数量复制 |
| `PFCT-002` | descriptor 携带 parser metadata | frozen parser/function 已执行 |
| `PFCT-003` | host 3.13 `feature_version=(3,10)` 得到结果 | 结果自动等价于 CPython 3.10.6 reference |
| `PFCT-004` | `ast.parse` 返回 `ast.Module` | source compile-valid 或 executable |
| `PFCT-005` | CPython 3.10.6 对 NUL input 抛 `ValueError`，另一宿主抛 `SyntaxError` | ambient exception class 可拥有 semantic reason |
| `PFCT-006` | target parser 拒绝 source | 可声明 `UNSUPPORTED_SYNTAX_VERSION` |
| `PFCT-007` | ProviderRun `COMPLETED` | denominator 每个 obligation 已 fulfilled |
| `PFCT-008` | parser unavailable、超时或 resource stop | 可伪装成 semantic `REJECTED` |
| `PFCT-009` | denominator member 没有 result | `never attempted` 是 parser terminal |
| `PFCT-010` | 同一 obligation 有两个 results | application 可择一形成 normal closure |
| `PFCT-011` | accepted subject IDs 相同 | exact products / product-set 相同 |
| `PFCT-012` | product digest 出现在 request 或 terminal | consumer 实际取得并使用该 product |
| `PFCT-013` | product-set semantics 逐字节相同 | 另一 attempt 可继承 continuation |
| `PFCT-014` | all-rejected reconciliation complete | Fact child 必须启动或 Fact/Coverage closed empty |
| `PFCT-015` | accepted list 为空 | 可以忽略 missing、lifecycle non-success 或 foreign result |
| `PFCT-016` | 当前 Fact wire 与 tests 全绿 | post-Parse consumer protocol 已冻结 |

这些 falsifiers 冻结拒绝边界，不预造 private class、public enum、AST schema、wire version 或 persistence carrier。

## 14. 后继实现边界

本候选冻结以前不授权代码。若独立 freeze publication 最终成立，后继仍须从新的 exact main 重新审计最小实现面；
最多可以考虑：

```text
exact Parse input/history revalidation
versioned private parser function or conformance boundary
per-subject candidate observation
semantic/lifecycle separation
complete denominator reconciliation
private admitted product / product-set identity
same-attempt immutable/copy-owned product access
one-shot continuation proof
PFCT-000..016 hardening
```

该列表不是当前施工授权。尤其不得从本合同直接开始：

```text
public Parse Schema / corpus / identity vector
public AST/product carrier or Bundle file
persistence Route A/B selection
Fact consumer projection/request/wire correction
Fact Provider scheduling or product-use enforcement
Fact obligation-universe derivation / fulfillment
shared ObservationReceipt / FulfillmentLedger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root
Attention / CLI / Workbench / Core / Q / O / T
```

若 private proof 必须先选择 persistence、修改 public identity、重新暴露 rejected raw source 或借用 Fact output authority
才成立，必须停止并用新反例重开对应最小边界。

## 15. 本地候选资格

CONTROL LOOP 从 `main@63daada4157e0068bb2a1333953f821f56f61894` 重新绑定 exact source、三条旧
Dependabot PR、文档 213–216 与 current Review Attention runtime。没有并行 human mainline PR，也没有隐藏的
qualified Parse carrier；current parser calls 仍只存在于历史 test/Relation Provider paths，current Fact wire 仍是
pre-Parse source-body protocol。文档 216 的 independent manifest 与 source bytes 已重新核对，product-use enforcement
与 zero-accepted scheduling 继续留在 future Fact consumer contract，因此 Parse 最小合同仍是当前最小合法问题。

本轮保留以下没有形成 product observation 的 setup/checker failures：

1. 托管 worktree 工具因聊天根目录 `GitHubProjects` 不是 Git repository 而拒绝；没有创建 checkout，后继从已验证
   `main@63daada...` 使用原生 Git 建立独立 worktree；
2. 第一次文档列表命令误用 Bash heredoc，PowerShell 在执行前拒绝，未改文件；
3. 第一次 README / AGENTS / milestones 组合补丁的 AGENTS 尾段 anchor 与实际换行不一致，`apply_patch` 在写入前
   整体拒绝；
4. 第一次 final static checker 把 audited/candidate marker 的合法叙述次数预期为 5，实际为 7，因此在 marker assertion
   停止；逐文件人工核对 7 次均属于状态块或资格叙述后，只修 checker expectation，不删候选内容迎合计数。

最终五文件候选通过：

```text
changed scope 5/5                         PASS
relative Markdown links                  PASS
UTF-8 without BOM / LF / final LF        PASS
balanced fences                          PASS
candidate markers                        PASS
base identity                            PASS
audit script hash                        PASS
git diff --check                         PASS
```

绑定 exact checkout source paths 后，以下 docs/Schema suite 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格各
`40/40 PASS`：

```text
tests.test_markdown
tests.test_review_r1_admission_evidence_schema
tests.test_review_r1_derivation_evidence_schema_correction
tests.test_review_r1_schema_payload
```

与本文 source claims 直接相关的 gate / Fact wire / controller / multi-Provider suite 在同一四格各 `67/67 PASS`：

```text
plugins.review-attention.tests.test_source_operation_gate
plugins.review-attention.tests.test_source_operation_fact_wire
plugins.review-attention.tests.test_source_operation_controller_integration
plugins.review-attention.tests.test_multi_provider_fact_composition
```

这些结果只使 final docs-only candidate 具备提交资格，不替代 original PR、exact-main、installed-product readback、
independent reconciliation 或独立 freeze publication，也不授予 runtime authority。

## 16. candidate freeze gates

本节保留合同候选的冻结门。[独立冻结发布](218-r1-parse-fulfillment-contract-freeze-publication.md)记录候选资格与
发布目标；只有以下链条完整成立后，合同状态才可生效为
`R1_PARSE_FULFILLMENT_CONTRACT_FROZEN`：

1. 文档 213–216 都已经形成 qualified history，且其 authority claim 没有被扩大或推翻；
2. denominator、one-obligation rule、CPython 3.10.6 function、decoded-source semantics、grammar-only boundary、
   semantic/lifecycle/reconciliation separation、product identity/access 与 persistence non-decision 可以独立复核；
3. `PFCT-000..016` 均能从 frozen inputs 与既有 paired-world evidence 重建；
4. diff 只包含本文、文档 216 资格闭合与 README / AGENTS / milestones 状态导航同步；
5. Markdown links、UTF-8、LF/final-LF、fence/heading、敏感路径、marker 与 `git diff --check` 成立；
6. 与 source claims 直接相关的现有 Language Support / source-operation / Fact wire / multi-Provider suites 在本层声明的
   Python normal / `-O` 矩阵中不被击穿；
7. candidate PR original required checks 全部成功并经受保护主线合入；
8. candidate exact main 的 Public CI 与 Browser Smoke 成立；
9. README、本文与 milestones 的 fresh installed-product public readback 与 independent reconciliation 成立；
10. 独立 docs-only freeze publication 自己的 original PR 门、受保护合入、new exact-main gates 与 fresh readback 再次
    成立。

第 10 项以前，本合同只能是 candidate，不能自称 frozen，也不能授权 runtime。任何新反例都可否决冻结或只重开被
击穿的最小条款。

当前原则候选冻结为：

> Parse fulfillment belongs to a complete exact denominator reconciliation; an accepted result carries an admitted
> product, while equal product semantics never transfer live execution authority.

中文：**Parse 履责属于完整 exact denominator 的机械对账；接受结果必须携带 admitted product，而相同 product 语义
永远不能转移 live execution authority。**
