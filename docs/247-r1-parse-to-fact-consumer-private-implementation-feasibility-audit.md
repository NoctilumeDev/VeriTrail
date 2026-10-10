# R1 Parse → Fact consumer correction private implementation 可行性审计

日期：2026-10-11

> 当前条件状态：
> `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@54eda4577e64cc3cf80eee464bd0ad116b710548`，Git tree
> `546ef4db989d715572b935c8c631c9db697be969`
>
> 冻结合同：[Parse → Fact consumer correction 最小合同 0.1](245-r1-parse-to-fact-consumer-correction-contract.md)
>
> 冻结发布：[Parse → Fact consumer correction 合同冻结发布](246-r1-parse-to-fact-consumer-correction-contract-freeze-publication.md)
>
> 影响层级：`L2_IMPLEMENTATION_FEASIBILITY_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本文不修改
> runtime、tests、Schema、Profile、Policy、corpus、Provider、Fact/Relation/Slice/Coverage、Evidence、Manifest、
> publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 问题与结论

文档 246 的全部冻结门已经闭合，因此
`R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN` 是当前事实；合同冻结没有自动授予 runtime 施工权。
本文重新进入 CONTROL LOOP，只问：

> 能否复用现有 live-attempt、Provider applicability、execution-cell 与 Fact canonicalization primitive，在不向
> Provider 暴露 raw source、不选择 persistence、不定义 Fact obligation universe、也不修改历史
> `private-source-operation-projection/0.1` / `derivation-cell/0.2` 语义的前提下，实现文档 245 §13 的 private
> Parse-product consumer closure？

结论是：**在一个新的 versioned private successor boundary 内可行。** 最小闭包为：

```text
claimed same-attempt Parse continuation
    -> revalidate exact admitted Parse product set
    -> derive one complete product membership for every applicable Fact Provider
    -> mint independent provider-bound one-shot claims
    -> application derives exact anchor metadata from product locations + exact bytes
    -> product-only copy-owned worker request; no source bytes/text/path reread
    -> validate every Fact candidate against its assigned product subject
    -> reconcile all required provider children in the same live parent attempt
    -> expose a private continuation only after complete qualified reconciliation
```

现有 budget、eligibility、contained execution、Provider applicability、Fact canonicalization 与 multi-Provider join
primitive 可以继续复用；历史 source-operation identity 不能被增加字段后静默改义。Parse continuation 当前只暴露
product set / product copies，因此后继实现需要一个有界 private handoff，把 original live attempt authority 交给新的
application-owned consumer controller；这不是 public carrier，也不能重建 fresh `BudgetContext`。

本文仍只是 docs-only candidate。它自己的资格链闭合后最多成为 `FEASIBILITY_AUDITED` qualified history；随后仍须
返回 CONTROL LOOP，并由独立 authorization publication 取得自己的资格，runtime 才可能获得施工权。在此以前 runtime
继续 `NOT_STARTED / NOT_AUTHORIZED`。

## 2. exact source state 与冻结资格

Parse → Fact consumer correction freeze publication 已合入：

```text
exact main = 54eda4577e64cc3cf80eee464bd0ad116b710548
tree       = 546ef4db989d715572b935c8c631c9db697be969

PR #283 original Public CI 38012722163
attempt 1 = 11/11 SUCCESS

exact-main Public CI 38014271058
attempt 1 = 11/11 SUCCESS

exact-main Browser Smoke 38014271039
attempt 1 = 1/1 SUCCESS
```

README、doc246 与 milestones 的 freeze target 已由 fresh installed-product observations 和 independent
reconciliation 闭合。README 第一次正式 observation 因匿名 GitHub API `403 / remaining=0` 保持
`ERROR / NON_QUALIFYING`；fresh README #2、doc246 与 milestones 才取得 PASS。后继成功没有覆盖首败。

最终 local reconciliation 记录为：

```text
sha256_json = 0454c821633ca742dfb9d93f11c62872b490a4b75748c01cf4989c48129d3182
```

本审计不追加事后 freeze 条件，也不重新解释这些历史 identity。它只把已经生效的 frozen contract 当作新的
CONTROL LOOP 输入。

## 3. current runtime topology

### 3.1 upstream Parse truth 已经足够

当前 private Parse implementation 已提供：

- application-owned、attempt-neutral、copy-owned `OwnedParseProductSet`；
- denominator / accepted / rejected partition 与 exact product-set digest；
- `OwnedParseFulfillmentClosure.claim_continuation()` 的 one-shot claim；
- `ClaimedParseContinuation` 对 original live attempt 的授权检查和 product copy access；
- equal product semantics from another attempt 不继承 continuation authority。

因此文档 215 / 216 当年缺失的 product identity、complete reconciliation 与 same-attempt product access 已经成为
qualified upstream truth。后继 consumer 不需要从 Fact output、accepted path list 或 digest echo 反推 Parse authority。

### 3.2 current Fact runtime 仍是历史 raw-source authority

当前 Fact request 的 frozen identity 仍为：

```text
private-source-operation-projection/0.1
veritrail-review-derivation-cell/0.2
```

`ValidatedFactSourceOperationRequest` 仍携带 `supported_paths` 与 `source_blobs_by_path_hex`；request document 仍包含
`source_blobs`。Fact worker 从 raw source 派生 candidate。current request、gate、worker 与 multi-Provider controller
都没有：

```text
OwnedParseProductSet
ClaimedParseContinuation
provider-bound Parse-product claim
admitted product binding
product-use authority
```

所以 source tests 全绿只能证明历史 pre-Parse wire 仍稳定，不能证明它已经消费 Parse product。`/0.1` projection 与
`/0.2` wire 必须保持历史含义；后继只能创建新的 private successor identity。

### 3.3 一个 parent consumer attempt，多个 child claims

current multi-Provider controller 已有 application-owned applicability / requiredness、child execution 与 final join；但它在
Fact 阶段自行创建 context，并不知道 Parse continuation。后继不能在 Parse 之后再创建 equal-limits fresh context。

可行 topology 是：

```text
one claimed Parse continuation
    -> one consumer parent attempt bound to original context + parent eligibility
    -> one shared exact Parse product set
    -> Provider A claim
    -> Provider B claim
    -> ...
    -> one final required-child reconciliation
```

不同 Providers 共享 semantic Parse truth，不共享 child claim。一个 Provider 的 terminal 不替代另一个 Provider 的
requiredness，也不修改 shared product set。

## 4. raw-source exclusion 与 exact byte anchor

### 4.1 现有 Fact anchor 不能被降级

frozen Fact `SourceAnchor` 使用 exact raw blob byte offsets。UTF-8 BOM、CRLF 与多字节字符都会使 AST 的 line/column
location 不能直接冒充 raw byte offset。只把 canonical AST 交给 Provider 而丢掉 exact-anchor semantics，会击穿既有
Fact identity。

### 4.2 application 可以完成 location → byte translation

audit-only world 使用 UTF-8-SIG、CRLF 与多字节文本证明：application 可以在 Provider boundary 以前，用：

```text
admitted canonical Parse product source locations
+ exact verified raw blob bytes already owned by application
+ frozen effective encoding
    -> exact SourceAnchor byte metadata
```

为 `ClassDef` 得到的 raw byte range 为 `[23, 75)`。该 translation 不把 raw bytes 变成 Provider operand：

- application 只从 admitted product locations 选择 anchor；
- raw bytes 只用于机械转换与边界验证；
- worker request 不含 raw body、source text、repository path loader、lazy handle 或 reread authority；
- Provider 不得自行 parse、decode 或根据 path 取得 source；
- application 对 candidate 的 subject、path、anchor range 与 assigned product 重新核账。

因此：

```text
application uses exact bytes to preserve frozen anchor identity
    !=
Provider receives raw-source derivation authority
```

若实现发现 canonical product locations 不足以机械生成全部既有 Fact anchor，或必须把 raw source 交给 Provider 才能
产生 Fact，必须停止并显式 reopen/version 被击穿的最小边界。

## 5. successor identity 与 product-use proof

### 5.1 private successor 不能继承历史 identity

后继至少需要一个新的 versioned private consumer function / projection / wire identity，绑定：

```text
exact input digests
Language Support classification identity
Parse function + product-set identity
complete Parse reconciliation
Provider descriptor / binding
complete assigned product membership
consumer function version
parent attempt binding
```

具体类名、模块切分与字段布局属于 implementation detail；本文不冻结 public Schema。无论如何，历史
`private-source-operation-projection/0.1` 与 `derivation-cell/0.2` bytes 不能被重新解释。

### 5.2 one-shot claim 必须绑定 Provider

每个 applicable Provider 领取自己的 claim。claim validation 至少保证：

- original Parse continuation 只被 consumer parent 领取一次；
- parent context / eligibility 仍是 original live objects；
- descriptor / binding 与 application-owned applicability 完全一致；
- membership 是同一完整 accepted product set，不接受 caller subset；
- claim success / failure 都消费该 claim，避免失败后重领；
- concurrency 下同一 child 只有一个 winner。

相同 product-set digest、相同 Provider descriptor、相同 limits 或相同 semantic outputs 都不能跨 attempt 继承 claim。

### 5.3 candidate provenance 必须解析到 assigned product

worker 的 internal candidate 必须携带足够的 private provenance，使 application 可以机械确认：

```text
candidate subject
    belongs to this Provider's complete assigned membership
candidate anchor
    belongs to that exact product subject
candidate provider run
    belongs to this child claim
```

foreign、rejected、missing 或 lifecycle non-success subject 出现 candidate 时，整个 normal child 必须 fail closed；不能
丢弃非法 candidate 后保留其余输出。public Fact shape可以保持不变，但 internal candidate admission 不能只靠 path、
product digest echo 或 terminal `COMPLETED`。

## 6. zero-accepted 与 multi-Provider 停止线

zero denominator 与 all-rejected complete 继续保留不同 upstream identity。两者在 0.1 都只能：

```text
validate complete Parse reconciliation
    -> derive accepted_count = 0
    -> BLOCKED_NO_ACCEPTED_PRODUCTS
    -> create no Fact child
    -> create no Fact terminal
    -> create no FactSet
```

这不是 required Provider fulfilled，也不是 empty FactSet、Fact fulfillment 或 Coverage closure。missing、duplicate、
dangling、foreign、incomplete 或 lifecycle non-success Parse history 不能借空 accepted list 混入该阻断状态。

当 accepted products 非空时，每个 existing-applicability admitted Provider 得到同一完整 membership 和独立 claim；0.1
不新增 Provider-specific product subset authority。后继若需要 capability-specific subset，必须先形成新的合同事实。

## 7. 可以复用与必须新增的边界

| 项目 | 审计结论 |
| --- | --- |
| `BudgetContext` / `AttemptEligibility` | 复用 original live objects；不得 fresh/reissue |
| Parse product set / continuation | 复用 frozen semantic truth 与 one-shot handoff |
| Provider applicability / requiredness | 复用 existing application-owned rules |
| Windows execution cell | 可复用 containment / lifecycle primitive |
| Fact canonicalization / multi-Provider join | 可复用最终语义核账，但须增加 product provenance admission |
| source-operation projection `/0.1` | 历史 identity 保留；不得改义 |
| Fact wire `/0.2` | 历史 raw-source identity 保留；不得改义 |
| successor consumer projection / claim boundary | 必须新增 private versioned identity |
| public carrier / persistence | 不需要；继续 OPEN / NOT AUTHORIZED |
| Fact obligation universe / fulfillment | 不需要；继续 NOT AUTHORIZED |

本审计没有发现需要第二套 budget framework、第二套 Provider registry 或 public Parse Artifact 的证据。

## 8. 后继 private implementation 最大分段

本文自己的资格门闭合后仍须返回 CONTROL LOOP；若后继独立 authorization publication 也取得资格，下一实现最多按
以下 private stages 物化：

```text
A. exact upstream Parse product-set / continuation revalidation
B. versioned successor consumer identity + complete Provider membership
C. provider-bound one-shot claims under original live attempt
D. product-only copy-owned worker request + raw-source side-channel exclusion
E. application-owned product-location -> exact-byte-anchor translation
F. Fact candidate provenance / assigned-product admission
G. same-attempt multi-Provider lifecycle / requiredness reconciliation
H. zero-accepted explicit blocking
I. private continuation after complete qualified reconciliation
J. PFC / PFCB / PFC-C falsifier hardening
```

这些 stages 是最大实现边界，不是本文件授予的 runtime authority。实现不得顺手开始：

```text
Fact obligation-universe enumeration
Fact fulfillment / exact completeness proof
zero-member FactSet or Coverage closure
Language Support / Parse persistence Route selection
public Schema / carrier / Evidence / Manifest / publisher / Bundle
ReviewSliceSet / CoverageLedger
CLI / Workbench / Core / other top-level tracks
DECLARED_CLAIM_FIDELITY
```

若任一 stage 必须越过这些边界才能成立，停止并回到 CONTROL LOOP；不能用实现方便性扩大 frozen contract。

## 9. falsifier matrix

后继实现至少必须直接拒绝以下世界：

| ID | 反例 | 必须得到的边界 |
| --- | --- | --- |
| `PFC-I-001` | same product-set semantics from fresh attempt | 不继承 parent/child claim |
| `PFC-I-002` | equal-limits fresh `BudgetContext` | 不继承 original attempt |
| `PFC-I-003` | caller 只交 accepted subset | membership derivation fail closed |
| `PFC-I-004` | Provider A 使用 Provider B claim | descriptor/binding mismatch |
| `PFC-I-005` | 同一 claim 并发领取 | exactly one winner |
| `PFC-I-006` | worker request 含 raw body/source text/path loader | request rejected before execution |
| `PFC-I-007` | worker reparse / path reread | no normal product-use qualification |
| `PFC-I-008` | candidate 指向 rejected / foreign subject | entire child invalid |
| `PFC-I-009` | application 丢弃非法 candidate 后保留其余结果 | prohibited |
| `PFC-I-010` | product digest echo but no product-bound derivation | no product-use proof |
| `PFC-I-011` | one Provider completed | other required children remain independent |
| `PFC-I-012` | first child normal completion | parent budget/eligibility remain valid for later child |
| `PFC-I-013` | accepted list empty but reconciliation incomplete | not zero-accepted blocking |
| `PFC-I-014` | all rejected complete | no child, terminal, FactSet or continuation |
| `PFC-I-015` | product location maps outside exact blob boundary | child invalid |
| `PFC-I-016` | BOM/CRLF/multibyte location mapped as character offset | exact byte-anchor mismatch rejected |
| `PFC-I-017` | historical `/0.1` or `/0.2` gains successor fields | identity continuity failure |
| `PFC-I-018` | final Provider terminal `COMPLETED` only | 不证明 product use 或 Fact fulfillment |

Tests 只能作这些边界的 witness，不能自行解释或扩大 contract。

## 10. audit-only executable probe

仓库外 probe 位于：

```text
<local-workspace>/tmp/parse-fact-consumer-implementation-feasibility-audit-54eda45/
```

关键脚本：

```text
feasibility_matrix.py
SHA-256 = 303e67195d1f8ff4f4630cf8609260c141d92994d30b41d0df1a7bff9f0d80c7

product_consumer_worker.py
SHA-256 = 62bbc73207d6b9b6e5f652d5c903bff366bbc228f2f75eeae9dad17498ef1de4
```

CPython 3.10.6 / 3.13.13、normal / `-O` 四格 report 均为 2639 bytes，逐字节相同：

```text
file SHA-256   = c10d3da0e5874e6fdad1803405830aa9acfdfe3e1ba98829bc056a6021a30510
report SHA-256 = dc0fdc26ddf0b80f0c4247ab9edc4c4eb3f0fb549c86b3bfe0359b34dfe4720b
result         = PASS
```

probe 机械证明：

```text
upstream denominator = 2
ACCEPTED = 1
REJECTED = 1
same semantic product set from two attempts uses distinct objects

two Providers share one product-set digest
two Providers have distinct projection digests and run IDs
one-shot concurrency = exactly one CLAIMED + one REJECTED
assigned paths = pkg/accepted.py only
rejected path visible = false
forbidden raw-source keys = false
worker Fact kinds = MODULE + CLASS_DECLARATION
foreign candidate = REJECTED
class raw byte anchor = [23, 75)

after two children:
BudgetContext = RUNNING
parent eligibility = ADMITTED

all rejected complete:
BLOCKED_NO_ACCEPTED_PRODUCTS
no Fact terminal
no FactSet
```

这只是 feasibility witness；它没有写入 product runtime，也不拥有 future class/module/API naming authority。

## 11. retained setup failure 与 existing test witness

第一次 targeted CPython 3.10 normal command 错写了不存在的
`tests.test_multi_provider_applicability`。unittest 虽运行其他模块，最后仍以 `ModuleNotFoundError` 停止。该身份永久保留为：

```text
TEST_HARNESS_IMPORT_SETUP_ERROR
root cause = DECLARED_TEST_MODULE_DOES_NOT_EXIST
product_observation = false
attempt = NON_QUALIFYING
```

fresh attempt 2 使用实际模块：

```text
tests.test_parse_fulfillment
tests.test_source_operation_projection
tests.test_source_operation_gate
tests.test_source_operation_fact_wire
tests.test_source_operation_controller_integration
tests.test_source_operation_hardening
tests.test_multi_provider_fact_composition
```

四格结果：

```text
CPython 3.10.6 normal  = 122 OK / skipped=1
CPython 3.10.6 -O      = 122 OK / skipped=1
CPython 3.13.13 normal = 122/122 PASS
CPython 3.13.13 -O     = 122/122 PASS
```

这些结果只证明 frozen Parse implementation 与 historical Fact chain 在 exact source 上继续成立；它们不把 audit probe
升级为 runtime，也不把 current Fact wire解释成 corrected consumer。

### 11.1 local final-byte docs qualification

本轮第一次 encoding 与 fence 检查命令都在 PowerShell parser 阶段因直接把 `foreach` statement 接到 pipeline 而停止；
两次命令都没有读取或修改候选文件，保持
`OPERATOR_STATIC_CHECK_COMMAND_SETUP_ERROR / product_observation=false / NON_QUALIFYING`。fresh commands 改为先
收集或逐项输出，不改变被检查字节。

pre-final review 还发现早期 draft 把“后继 implementation authorization publication”误列为本 feasibility audit 自身
取得资格的前提，形成循环资格依赖。该 draft 在 commit / PR 前被修正：本审计以自己的 readback / reconciliation 取得
`FEASIBILITY_AUDITED`，随后返回 CONTROL LOOP；authorization publication 另行取得资格。该修正没有创建 runtime
observation，也没有授予 implementation authority。

最终四文件候选的 static gate 为：

```text
changed scope = README.md / AGENTS.md / docs/milestones.md / doc247 only
UTF-8 without BOM = PASS
LF only / final LF = PASS
balanced fences = PASS
candidate markers = PASS
relative Markdown links = PASS
git diff --check = PASS
```

docs/Schema suite 使用 exact checkout source paths；CPython 3.10.6 / 3.13.13、normal / `-O` 四格各
`40/40 PASS`：

```text
tests.test_markdown
tests.test_review_r1_admission_evidence_schema
tests.test_review_r1_derivation_evidence_schema_correction
tests.test_review_r1_schema_payload
```

这些 gates 只使 docs-only candidate 具备提交资格，不替代 PR、merge、exact-main 或 public product observation。

## 12. authority table

| Authority | Owner | 明确不拥有 |
| --- | --- | --- |
| exact Parse truth | frozen Parse closure / product set | Fact Provider、caller、digest echo |
| consumer parent attempt | application + original live Parse continuation | equal context/attempt reconstruction |
| applicable Providers | existing frozen applicability | Provider self-registration |
| per-Provider membership | application 从完整 accepted product set 导出 | caller subset、reported Fact paths |
| child claim | application-owned provider-bound one-shot claim | shared claim、terminal self-report |
| product-only worker operands | successor private projection | raw source、path reread、reparse |
| exact byte anchor translation | application from admitted product locations + exact bytes | Provider raw-source authority |
| Fact candidate admission | application validates assigned subject/product/run | Provider `COMPLETED` |
| final child reconciliation | application under existing requiredness/lifecycle | first success、single Provider completion |
| Fact obligation / fulfillment / Coverage | future contract | 本审计、Provider self-report |

## 13. 明确 non-decisions

本文不选择：

- successor class/module 名称或 public API；
- persistence Route A/B；
- public Parse product / Fact consumer Schema；
- Fact obligation universe、per-product Fact completeness 或 exact fulfillment；
- empty FactSet / zero-member closure；
- ReviewSliceSet / Coverage denominator；
- remote runtime distribution、attestation 或 cross-machine product transport；
- `DECLARED_CLAIM_FIDELITY` obligation family。

这些问题若以后成为最小合法 seam，必须重新经过自己的 CONTROL LOOP 与 qualification pipeline。

## 14. candidate qualification gates

本审计只有在以下链条成立后，才可以成为 qualified feasibility history：

1. exact baseline 保持 `54eda4577e64cc3cf80eee464bd0ad116b710548` / tree
   `546ef4db989d715572b935c8c631c9db697be969`，且没有未审 parallel semantic PR 改写 seam；
2. doc245 / doc246 与 frozen Parse implementation 的历史 claims 不被扩大或倒改；
3. current source 继续证明 Parse continuation 已存在、Fact runtime 仍是 historical raw-source authority；
4. section 3–12 的 successor topology、raw-source exclusion、anchor translation、multi-Provider、zero-accepted 与
   authority boundary 可以独立复核；
5. audit-only 四格 report 逐字节一致，retained setup error 保持原身份；
6. targeted existing tests 在本层声明的 Python normal / `-O` 矩阵中不被击穿；
7. diff 只包含本文与 README / AGENTS / milestones 条件状态同步；
8. Markdown links、UTF-8、LF/final-LF、fence/heading、敏感路径、marker 与 `git diff --check` 成立；
9. docs/Schema suite 在本层声明的 Python normal / `-O` 矩阵中成立；
10. candidate PR original required checks 全部成功并经受保护主线合入；
11. new exact-main Public CI 与 Browser Smoke 成立；
12. README、本文与 milestones 的 fresh anonymous installed-product readback 与 independent reconciliation 成立。

第 12 项以前，本文只能发布顶部 candidate marker。第 12 项闭合后才可成为
`R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED` qualified history；这仍
不等于 implementation authorization，runtime 继续 `NOT_STARTED / NOT_AUTHORIZED`。任一反例只重开它击穿的
最小边界。

## 15. stop line

若本审计最终取得资格，下一步也不是写 runtime。必须返回新的 exact main，重新核对 frozen contract、current source、
并行 PR、retained failures 与本审计的 falsifier；只有没有新反例时，才能创建独立 docs-only implementation
authorization publication。

当前原则候选冻结为：

> A private Parse-product Fact consumer is feasible only when one application-owned parent preserves the original live
> attempt, assigns the complete admitted product set through independent provider-bound claims, excludes raw-source
> derivation from workers, and admits every candidate against its exact product provenance before reconciliation.

中文：**private Parse-product Fact consumer 只有在一个 application-owned parent 保留 original live attempt、通过独立
Provider claim 分配完整 admitted product set、禁止 worker 取得 raw-source derivation authority，并在 reconciliation
以前按 exact product provenance 核账每个 candidate 时，才具备可实现性。**
