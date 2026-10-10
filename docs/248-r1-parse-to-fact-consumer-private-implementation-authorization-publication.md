# R1 Parse → Fact consumer correction private implementation 授权发布

日期：2026-10-11

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_ALLOWED /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 发布基线：`main@fca688e399af2b24776e23bf490cb6e4b589880f`，Git tree
> `285d2a46776be1f1d380c570b3f83f401819889c`
>
> 冻结合同：[Parse → Fact consumer correction 最小合同](245-r1-parse-to-fact-consumer-correction-contract.md)
>
> 合同冻结发布：[Parse → Fact consumer correction 合同冻结发布](246-r1-parse-to-fact-consumer-correction-contract-freeze-publication.md)
>
> 可行性审计：[Parse → Fact consumer correction private implementation 可行性审计](247-r1-parse-to-fact-consumer-private-implementation-feasibility-audit.md)
>
> 影响层级：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`。本轮不修改 runtime、tests、
> Schema、Profile、Policy、corpus、Provider、Fact/Relation/Slice/Coverage、Evidence、Manifest、publisher、
> Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. CONTROL LOOP 结论

文档 247 已完成自己的 final-byte local gates、PR #284 原始 required checks、受保护主线合入、新 exact-main
双门、三份 fresh anonymous installed-product readback 与 independent reconciliation。因此：

```text
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
```

已经是 qualified history。该事实只证明文档 247 的 bounded private successor 没有被声明的反例击穿；它本身没有
授予 runtime authority。

本轮重新绑定 `main@fca688e399af2b24776e23bf490cb6e4b589880f`，复核 frozen contract、current runtime、
retained setup/error history、三个 unrelated Dependabot PR 与文档 247 的 `PFC-I-001..018`。PR #284 只修改
README、AGENTS、milestones 与 doc247；current Parse product/continuation、historical Fact projection `/0.1`、
Fact wire `/0.2`、multi-Provider controller 与 Windows execution cell 没有发生语义变化。没有发现更早的 authority
seam，也没有发现必须选择 persistence、public carrier、Fact fulfillment 或 Coverage 才能实现 bounded private
consumer 的新反例。

因此当前最小合法下一刀仍是文档 247 第 8 节 A–J private implementation。本文只条件化发布这项有限 authority；
本文自己的最后门闭合以前，runtime 继续 `NOT_STARTED / NOT_AUTHORIZED`。

## 2. feasibility audit 的资格身份

文档 247 候选的最终坐标为：

```text
base  = 54eda4577e64cc3cf80eee464bd0ad116b710548
head  = 9c42a903458dfb83181e5fa84aea26408811c902
merge = fca688e399af2b24776e23bf490cb6e4b589880f
tree  = 285d2a46776be1f1d380c570b3f83f401819889c
```

原始与 exact-main 门均在 attempt 1 成立：

| 门 | Run | 结果 |
| --- | --- | --- |
| PR #284 Public CI | `38079982368` | `11/11 SUCCESS` |
| exact-main Public CI | `38081660490` | `11/11 SUCCESS` |
| exact-main Browser Smoke | `38081660497` | `1/1 SUCCESS` |

README、doc247 与 milestones 使用三个新 Plan / collection session / handoff identity 完成 exact-SHA 匿名产品读回：

| Target | Plan | API / render | Core |
| --- | --- | --- | --- |
| README | `r1-pfc-feas-audit-readme-fca688e` | `COMPLETE / COMPLETE` | `PASS` |
| doc247 | `r1-pfc-feas-audit-doc247-fca688e` | `COMPLETE / COMPLETE` | `PASS` |
| milestones | `r1-pfc-feas-audit-milestones-fca688e` | `COMPLETE / COMPLETE` | `PASS` |

每份 public render 都保留 requested/final identity、三次稳定采样、唯一 candidate marker、零 active stream、零 cleanup
error、零 coverage reason 与零 conflict。三个匿名 raw 文件逐字节等于 exact Git blobs。independent reconciliation 为：

```text
sha256_json = 4a34719d1a1116760b5fe4fb659b93151848ce7f4a3d5a686d9b011003bfcd19
```

正式 readback 三份均为独立 PASS。读回准备阶段的 Windows `rg` wildcard、harness marker replacement、匿名 API
额度耗尽、direct DNS 不可用与两次 Playwright shutdown warning 共六项 setup observation 均保留为
`NON_QUALIFYING`；它们发生在正式 Plan 以前，没有被写成产品失败或后来 PASS 的原因。

## 3. current exact-main continuity

当前上游文档与关键 runtime SHA-256 为：

```text
b3f0b08b02092bcc33fcf0227038c550c968193d868a6824686a5609f69de636  docs/245-r1-parse-to-fact-consumer-correction-contract.md
fda7d2e0ecc14d800e5d8c4ea21636e5ca836957121872bd70869889d5461d39  docs/246-r1-parse-to-fact-consumer-correction-contract-freeze-publication.md
e23311a2a02d08ffe689ee2a24dc94153e7af78c3a36d174e005a40f0f8f16c4  docs/247-r1-parse-to-fact-consumer-private-implementation-feasibility-audit.md

2c845899213b81c5cee32017ec889d1c304199e02df636bfb026a1f17b6a0f3a  _parse_fulfillment.py
5d5f5125ddebeb934712e793e081cf0e191a8a193962afd028b30659df3afda2  _parse_fulfillment_values.py
e54f8da698efd3811dc5cf4b499238dd0d29132815d5ba16881e7e2e6d024ac8  _parse_fulfillment_worker.py
eeb82823563aeb7460cd06eec4cec08091e7342fdc74d251ed5f2a35234e0dbd  _source_operation_fact_application.py
252f8018404c294daffecedb74519203dce33fb6b734ce99cd9405db0b82b4f9  _source_operation_fact_worker.py
3c185099c113a18f6ba76cfd0ad3356ae5ab4bd27c3f9d4d5da6fade7a92d674  _multi_provider_fact_composition.py
c90412ec2218110350dc7fef87ad8292113ffc550ec770eddb9ea46bae852af3  _windows_execution_cell.py
```

这些摘要只证明本文 re-audit 使用的 exact bytes。实现分支仍须从 authorization publication 生效后的新 exact main
重新读取源文件，不得把摘要或相同内容当作 continuation authority。

## 4. 发布的有限 authority

本文最后门全部成立后，下一单用途 implementation branch 最多实现文档 247 已审计的 private stages：

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

实现必须继续满足：

1. 新对象、projection、wire 与 controller 保持 `veritrail_review` private；
2. parent 必须领取原 `ClaimedParseContinuation`，复用 original live `BudgetContext` / eligibility，不得 fresh/reissue；
3. 每个 existing-applicability admitted Provider 获得完整 accepted product membership 与独立 provider-bound one-shot claim；
4. worker 只能得到 copy-owned products 与 application 生成的 anchor metadata，不能得到 raw body、source text、path
   loader、lazy handle 或 reparse authority；
5. raw bytes 只由 trusted application 用于 product location 到 exact byte anchor 的机械转换与边界验证；
6. candidate 必须绑定 exact assigned subject/product/provider run；foreign、rejected、missing 或 lifecycle non-success
   candidate 使整个 child fail closed；
7. required children 必须在同一 parent attempt 完整 reconciliation 后才允许 private continuation；
8. zero denominator 与 all-rejected complete 继续保持不同 identity；accepted count 为零只允许
   `BLOCKED_NO_ACCEPTED_PRODUCTS`，不产生 Fact child、Fact terminal、FactSet 或 Coverage claim；
9. historical `private-source-operation-projection/0.1` 与 `veritrail-review-derivation-cell/0.2` 保持原义；
10. `PFC-I-001..018` 必须成为直接 falsifier，不得由 happy path 或 digest echo 替代。

这项 authority 只允许开始实现，不预先声明实现正确、完成、合入、exact-main verified 或 frozen。

## 5. 明确不授权

```text
Fact obligation-universe enumeration
Fact fulfillment / exact completeness proof
zero-member FactSet or Coverage closure
Language Support / Parse persistence Route selection
public Schema / carrier / corpus / Evidence / Manifest / publisher / Bundle
ReviewSliceSet / CoverageLedger
CLI / Workbench / Core / other top-level tracks
DECLARED_CLAIM_FIDELITY
tag / Release
```

尤其：

```text
PRIVATE_IMPLEMENTATION_ALLOWED
    != implementation started
    != current Fact consumer corrected
    != Fact fulfillment established
    != persistence selected
    != Coverage authorized
```

若 implementation 证明 frozen boundary 无法在上述有限范围内成立，必须保留反例，停止施工，并只显式 reopen/version
被击穿的最小边界；不得因为本文已授权而扩大 runtime。

## 6. implementation 的后继资格链

实现形成最终字节后仍须独立经过：

```text
implementation final bytes
    -> implementation layer declared local gates
    -> original PR required checks
    -> protected main merge
    -> new exact-main Public CI + Browser Smoke
    -> required fresh product observation / reconciliation
    -> implementation fact publication
    -> return to CONTROL LOOP
```

本文不预先决定 implementation 文件布局、private class 名称、test count 或后继 publication 形状。测试只作 witness，
不能扩大 A–J、修改 contract、选择 persistence 或启动 Fact fulfillment / Coverage。

## 7. 本 publication 的最后门

本 docs-only publication 只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。doc245/246/247、
runtime、tests、Schema、Profile、Policy、corpus、architecture DOT/SVG 与 identity vectors 必须保持原字节。

提交前必须通过本层声明的双 Python normal / `-O` docs/Schema regressions、relative links、UTF-8 without BOM、
LF/final-LF、heading/fence、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与 `git diff --check`。
随后必须完成：

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / doc247 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> conditional authorization state takes effect
```

任一非成功观察都保留原身份；后继 PASS 不覆盖首败。本文中的
`R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_ALLOWED` 在最后门闭合以前只是 target marker，不能
授权 runtime branch 提前开始。最后门闭合后也必须重新绑定新的 exact main 并返回 CONTROL LOOP；只有 A–J 仍是
最小合法问题时，才可创建 implementation branch。

## 8. stop line

```text
before publication qualification:
    feasibility audit = AUDITED
    implementation authority = NOT_AUTHORIZED
    implementation = NOT_STARTED

after publication qualification:
    feasibility audit = AUDITED
    private implementation = ALLOWED
    implementation = NOT_STARTED
```

当前授权原则候选冻结为：

> The Parse-to-Fact consumer correction may enter private implementation only through the bounded A–J successor audited
> by doc247; that authority does not establish implementation, Fact fulfillment, persistence, or Coverage.

中文：**Parse → Fact consumer correction 只能在 doc247 已审计的 A–J private successor 边界内进入实现；这项授权
不证明实现已经发生，也不建立 Fact fulfillment、persistence 或 Coverage。**
