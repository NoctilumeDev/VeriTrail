# R1 Language Support eligible operation projection / same-attempt gate 实现冻结重新资格化发布

日期：2026-09-28

## 1. 文档身份与条件状态

> 状态目标：`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 208](208-r1-language-support-eligible-operation-projection-contract.md)
>
> 实现冻结候选：[文档 210](210-r1-language-support-eligible-operation-projection-implementation-freeze-candidate.md)
>
> 首次实现冻结发布：[文档 211](211-r1-language-support-eligible-operation-projection-implementation-freeze-publication.md)
>
> 重新资格化基线：`main@df7f3d5a190d317a47c0fc1fb9405419e6b76828`
>
> 基线 Tree：`7bcfa7788ee929e2b60b22246eac01cb977ac0cb`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_REQUALIFICATION_ONLY`

本文不修改文档 208、209、210、211 的合同或历史字节，也不重新实现 A–G。本文只保留首次冻结发布的
exact-main 正式失败、记录独立 test-support maintenance 的资格链，并以新的 source identity 重新发布同一 private
implementation frozen target。

本文不创建或修改 runtime、tests、Schema、Profile、Policy、corpus、identity vector、wire、operands、request、
controller、Provider、Parse、AST、Fact、Relation、ReviewSliceSet、Coverage、Evidence、Manifest、publisher、Bundle、
CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文自身仍须完成 final bytes local docs/Schema/static gates、original PR required checks、受保护主线合入、新
exact-main Public CI / Browser Smoke，以及 README、本文、milestones 的 fresh anonymous installed-product readback
与 independent reconciliation。只有这些门全部成立，状态目标才成为当前主线事实；在此以前，本分支中的 frozen
marker 仍只是 publication target。

## 2. 首次冻结发布没有取得资格

[PR #231](https://github.com/NoctilumeDev/VeriTrail/pull/231) head
`1be1077930360cbe0305e8c9c5aace771e439d34` 只修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增
文档 211。其 original [Public CI run 36342051676](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36342051676)
在 attempt 1 取得 11/11 SUCCESS；PR 以 ordinary merge 合入：

```text
publication merge = fd5628123e5460de21039c81dc7f9e9ed7ae9772
publication tree  = 748f36a548c192a00b3a2d6b0c571501b7c0dd22
merge parents     = e69ff64333300fc01bd89eb3dfbe69f447048b40
                    1be1077930360cbe0305e8c9c5aace771e439d34
```

该 exact main 的 Browser Smoke run `36343474807` attempt 1 为 1/1 SUCCESS；Public CI run `36343474761`
attempt 1 为 FAILURE。失败位于 Python 3.10 `-O` Review Attention：

```text
test_d_004_failed_assignment_validation_consumes_the_claim
    expected semantic assignment-validation world
    observed _ReviewSliceInputError:
        ADMISSION_BINDING_REJECTED
```

该 test 从 admission 到 binding 约消耗 `10.085s`，超过 sealed `wall_clock_ms = 10000`。runtime 在
`continuation.available()` checkpoint 正确 fail closed；失败没有证明合同、A–G runtime 或冻结语义错误。
它证明的是 test-support topology 把 Slice identity / ownership / one-shot 语义测试绑定到 hosted-runner wall clock，
从而可能在 runner 调度较慢时把语义测试静默变成 deadline 测试。

该 observation 永久保持 `FAILURE`。后继 maintenance 与后继成功不把它改写成 PASS，也不使文档 211 的 frozen
target 追溯生效。

## 3. 独立 test-support maintenance

[PR #232](https://github.com/NoctilumeDev/VeriTrail/pull/232) 从失败 exact main 建立，只修改
`plugins/review-attention/tests/test_review_slice_input_join.py`，共 `19 insertions / 0 deletions`。它在共享 setup
取得真实 `BudgetContext` 后，把该 suite 的 attempt-local test clock 固定在 admission 时刻；原始 context object、
limits、attempt identity、parent/child eligibility、one-shot claim 与 cancellation behavior 均保持不变。deadline
transition 仍由既有专用 budget/runtime tests 使用真实时钟验证。

因此该修正表达的是：

```text
Slice identity / ownership / one-shot semantic tests
    must not acquire deadline semantics from hosted-runner scheduling

real BudgetContext + cancellation semantics
    remain under test

product timeout / budget / fail-closed runtime
    unchanged
```

maintenance final bytes 的本地验证为：

| Lane | Triggering test | Slice-input module | Related | Full Review Attention |
| --- | --- | --- | --- | --- |
| CPython 3.10.6 normal | PASS | `85/85` | `182/182` / 302.125s | `417/417` / 570.543s |
| CPython 3.10.6 `-O` | PASS | `85/85` | `182/182` / 301.053s | `417/417` / 569.662s |
| CPython 3.13.13 normal | PASS | `85/85` | `182/182` / 301.810s | `417/417` / 563.408s |
| CPython 3.13.13 `-O` | PASS | `85/85` | `182/182` / 302.778s | `417/417` / 560.740s |

Python 3.10 / 3.13 `py_compile` 与 `git diff --check` 同时成立。该矩阵只证明 maintenance bytes，不替代远端门。

## 4. Maintenance 远端资格链

PR #232 只有一个 commit、一个 test-support 文件；head 为
`f7651732ea419865814bb9e755916795c4cc9fa1`。original
[Public CI run 36349719735](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36349719735) 在 attempt 1
取得 11/11 SUCCESS，没有 rerun 或 head 改写。

PR 以 ordinary merge 合入受保护 main：

```text
maintenance base  = fd5628123e5460de21039c81dc7f9e9ed7ae9772
maintenance head  = f7651732ea419865814bb9e755916795c4cc9fa1
maintenance merge = df7f3d5a190d317a47c0fc1fb9405419e6b76828
maintenance tree  = 7bcfa7788ee929e2b60b22246eac01cb977ac0cb
```

该 exact maintenance main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| Public CI | [36351246640](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36351246640) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [36351246642](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36351246642) | 1 | `1/1 SUCCESS` |

这条资格链证明 test-support maintenance 已成为新的合格 source state。它不追溯修复 run `36343474761`，也不
自动使文档 211 的 frozen target 生效。

## 5. 重新发布的最小状态

本文不改变文档 211 第 2、6 节列出的 implementation closure 与未授权能力。重新发布的仍是同一个有界事实：

```text
copy-owned exact DerivationInputSet
    -> deterministic Language Support classification / operation projection
    -> original BudgetContext + parent AttemptEligibility
    -> one-shot same-attempt child authority
    -> Fact / Relation derivation / Relation observation corrected input binding
    -> three controller integrations
    -> exact downstream history revalidation
    -> LSPC-000..018 hardening
```

以下能力继续未授权：

```text
Language Support persistence Route A or B
real parser / AST execution
per-unit Parse terminal fulfillment
Fact projection-universe derivation / fulfillment
shared observation receipt or ledger
public Language Support / Parse / Fact carrier or Schema
ReviewSliceSet / Coverage
Evidence / publisher / Bundle
CLI / Workbench
```

内容相同、semantic result 相同、limits 相同或 source patch 相同都不能继承另一条 qualification path。本文以新
source identity 重新取得 publication 资格，而不是宣布第一次发布“其实成功”。

## 6. 本发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档
208/209/210/211、architecture DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 必须
保持基线字节。

提交前必须在本文最终字节上完成：

1. 双 Python normal / `-O` docs/Schema regressions；
2. 全仓 Markdown prose relative links 零断链；
3. Markdown fence / heading、状态 marker、UTF-8 without BOM、LF / final LF、敏感路径、exact four-file scope 与
   frozen byte continuity 静态核对；
4. `git diff --check`。

最终 publication bytes 的本地结果为：

```text
docs / Schema
    CPython 3.10.6 normal  40/40 PASS
    CPython 3.10.6 -O      40/40 PASS
    CPython 3.13.13 normal 40/40 PASS
    CPython 3.13.13 -O     40/40 PASS

static
    exact four-file scope                       PASS
    prose relative links                        1026 / zero broken
    doc212 headings                              8 / unique
    final marker counts                          README 1 / doc212 1 / milestones 2
    UTF-8 without BOM / LF / final LF            PASS
    frozen doc208/209/210/211 + code continuity  PASS
    git diff --check                             PASS
```

milestones 中的两个 final marker 分别属于首次未生效的文档 211 条件 target 与本文新的 requalification target；它们
保留两次 publication identity，不能压成一次。README 与本文各只有一个当前 target marker。

这些本地门不能替代本发布自己的 original required checks。最终资格链为：

```text
requalification publication final bytes
    -> original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功 observation 必须保留原身份；诊断不计入资格，后继成功不改写先前失败。不得拿 PR #230、#231、
#232 的绿灯替代本文自己的门。

## 7. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新读取 frozen truth，再判断 Parse
fulfillment prerequisite 是否仍是当前最小合法问题。文档编号、implementation frozen 或绿色 CI 都不能自动授予
Parse、Fact、persistence、Coverage 或 public carrier 施工权。

若 fresh readback、reconciliation 或系统审计击穿当前 closure，只重开被击穿的最小 seam 并重新取得资格；不得
按原路线机械进入下一阶段。
