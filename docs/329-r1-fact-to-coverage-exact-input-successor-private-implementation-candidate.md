# R1 Fact→Coverage exact-input successor 私有实现候选

日期：2026-10-28

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE`。
>
> 施工基线：`main@494fedb1fbae9d5f847cb9f1873e7e13996b893a`，tree
> `c60c01e5a1a380fe1aba0c217faa834241bea545`。
>
> 本文只认领[文档328](328-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-successor-publication.md)
> 已生效的bounded A–I private implementation。它不创建Coverage producer，不恢复旧composition authority，不选择manifest、
> Evidence或persistence，不发布public Review产品，也不启动R2–R6。

## 1. CONTROL LOOP 与已生效授权

文档328由PR #379完成资格链并精确合入本施工基线。original Public CI `40531345541`、exact-main Public CI
`40535859530`与Browser Smoke `40535859486`均为attempt 1 SUCCESS。fresh anonymous installed-product readback、independent
reconciliation与finite closeout均闭合：

```text
readback targets: 7/7 FORMAL_READBACK_PASS
reconciliation: 8861f480d643904fd75ed61afe09ccd61a4c978a8a3fcb253625d7927e729050
closeout:       72ae34c8ec41ab963c4dee2a8bc005c131f60d12e69982f521250bfa0d15e382
adapter freeze: 8799458f7bb570e8291c00f206537ecdf49602ba3b75941d1e7f5e61762cef7c
```

pre-formal attempt 1的错误upstream coordinate与过早adapter freeze attempt 1均保持原identity；attempt 2不覆盖它们。
因此`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`已生效。fresh CONTROL LOOP重验
exact main、冻结0.2合同、0.1历史、#377失败、#378 failure-boundary资格、#379授权与primary `audit.json`，没有反例要求
重开合同或授权边界；当前最小施工面仍为A–I private carrier implementation。

## 2. versioned private identity 与边界

本候选新增且只新增以下private identity：

```text
handoff function  r1-fact-to-coverage-exact-input-handoff-successor/0.2
claim purpose     FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2
consumer          r1-negative-world-coverage-exact-input-consumer/0.1
carrier           r1-terminal-validated-original-derivation-input-carrier/0.1
```

旧`r1-fact-to-coverage-handoff/0.1`文件与bytes保持不变；package public exports、默认composition、Relation transition、
Schema、Policy/Profile、Coverage producer、workflows与public产品均保持base语义。新module没有加入`veritrail_review.__init__`。

## 3. A–I 实现映射

| ID | 本候选实现 |
| --- | --- |
| A | 只接受四个exact identity；unknown、近似或版本混用在消费closure以前拒绝。 |
| B | parent-only terminal accessor先完整重验Fact terminal source，再原子返回同一source、原始`BudgetContext`与原始`DerivationInputSet`。 |
| C | successor与legacy continuation、Coverage 0.1 handoff、Relation handoff共享同一个`__claimed` one-shot slot；并发竞争只有一个胜者。 |
| D | carrier绑定原始input object、input seal、三份canonical bytes、verified blob keys/bytes、五个digest、context identity、source bytes与claim identity。 |
| E | `REQUIRED_PROVIDER_NON_SUCCESS`从terminal-bound原始inputs构造，不调用会因eligibility revoked而拒绝的`_inputs_ref()`，也不恢复eligibility。 |
| F | 每个carrier read都重验context、deadline/stop、input seal、canonical bytes、blob map、五digest、source、closure claim与同一object graph；失败永久fail closed。 |
| G | 直接覆盖五个Fact terminal branches与empty inventory、unsupported language、policy-excluded三种zero-Parse denominator worlds。 |
| H | 对外只返回copy-owned Snapshot、Policy、Profile、verified blob bytes、Fact terminal source与input identity proof；不产生Coverage outcome、ledger或manifest authority。 |
| I | private falsifier覆盖identity、object/context substitution、late stop、digest/canonical/blob drift、unsafe source、one-shot race、legacy/public surface与copy ownership。 |

## 4. terminal-bound exact input

旧0.1 handoff只保存Fact terminal source copy，无法证明下游取得的是同一attempt中Fact实际消费的完整原始输入。本候选没有从
terminal document、digest或重新加载的文件重造`DerivationInputSet`，而是在`OwnedProductFactConsumer`内部新增token-guarded
accessor：

```text
closure exact one-shot claim
    -> full terminal source revalidation
    -> original BudgetContext identity
    -> original DerivationInputSet identity + seal
    -> private carrier binding
```

equal-bytes foreign input仍然被拒绝。carrier保留三份canonical input bytes、完整verified blob map与五个digest，并在每次读取时把
live object重新与绑定值比较。这样下游以后可以消费完整原始world，而不是通过过滤FactSet或重载bytes缩小分母。

## 5. required-provider-failure 与one-shot discipline

Fact required Provider失败时，parent eligibility按既有规则保持`REVOKED`；但Fact terminal branch已经合法形成，且其原始input仍是
该terminal history的一部分。successor通过terminal-bound accessor读取它，不调用live-authority `_inputs_ref()`，因此可以保存
`REQUIRED_PROVIDER_NON_SUCCESS`的完整输入身份，同时不把parent eligibility改回`ADMITTED`。

四类source consumer共享一个锁保护的claim slot：

```text
legacy continuation
Coverage handoff 0.1
Relation transition
Fact→Coverage exact-input successor 0.2
```

任何一个先成功，其他全部拒绝；并发successor/legacy竞争也只能产生一个成功。carrier后续读取只重验已经取得的claim，不创建第二份
continuation或新的authority。

## 6. fail-closed 与copy boundary

carrier读取前同时检查：

```text
bound closure/input/context/claim/source/document identities
BudgetContext limits + start/deadline identity
RUNNING + no stop + checkpoint
DerivationInputSet seal
three canonical byte fields
verified blob keys and bytes
five input digests
terminal source bytes and closure claim purpose
```

任一不一致都会把carrier永久标记为failed，并撤销原始绑定closure的parent eligibility。即使攻击者把当前closure字段替换成
foreign closure，失败路径仍优先撤销原始bound closure；同时也尽力撤销当前字段，不能靠object-graph substitution留下原authority。

公开copy方法只有：

```text
fact_terminal_source_copy
source_snapshot_document_copy
review_policy_document_copy
derivation_profile_document_copy
verified_blob_bytes_copy
input_identity_copy
```

返回值可由调用者任意修改而不会改变carrier内部bytes。返回文档不含Coverage status、obligation、ledger、manifest role或public
completion claim。

## 7. terminal branch 与denominator falsifiers

private suite直接观察：

```text
NORMAL_FULFILLED
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

zero-Parse又保留三个不同输入世界：

| world | Snapshot inventory | Policy scope decision | branch |
| --- | ---: | ---: | --- |
| empty inventory | 0 | 0 | `ZERO_PARSE_DENOMINATOR` |
| unsupported language | 1 | 1 | `ZERO_PARSE_DENOMINATOR` |
| policy excluded | 1 | 1 | `ZERO_PARSE_DENOMINATOR` |

共同terminal label不会抹除原始Snapshot、Policy、Profile、blob map或input digest身份；因此representation相同不被冒充为输入world相同。

## 8. final local qualification

focused matrix由既有Coverage ledger、language support、Fact fulfillment、0.1 handoff、Relation transition、Relation→Slice composition
回归与新增12项successor falsifier组成。四格均使用source review修正后的final bytes：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 139 reported / 138 passed / 1 skipped |
| 3.10.6 | `-O` | 139 reported / 138 passed / 1 skipped |
| 3.13.13 | normal | 139 reported / 138 passed / 1 skipped |
| 3.13.13 | `-O` | 139 reported / 138 passed / 1 skipped |

完整Review Attention suite的final矩阵为：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 586 reported / 583 passed / 3 skipped |
| 3.10.6 | `-O` | 586 reported / 583 passed / 3 skipped |
| 3.13.13 | normal | 586 reported / 584 passed / 2 skipped |
| 3.13.13 | `-O` | 586 reported / 584 passed / 2 skipped |

独立semantic report不使用DUT生成预期terminal branch或denominator counts；冻结oracle显式枚举五branch与三个zero-Parse world。
四格final report语义一致：

```text
a6866781bd574b7f899c7127d241bcca1eb290696d081a45401f8fb413391c7f
```

semantic comparison SHA-256为：

```text
d89420ad52385525610c9f5246a30058b51c43966c09c42ffdf9a5f20ca1fdbf
```

Python 3.10/3.13 compileall、`git diff --check`、global/local hygiene、Markdown、exact scope、public export guard、old 0.1
SHA与primary `audit.json` continuity必须在commit前对final candidate bytes再次PASS。测试只作为本candidate witness，不替代original PR、
exact-main或installed-product门。

## 9. retained prequalification history

所有prequalification history保持原identity：

1. 第一轮targeted test错误使用缺少0.2 capability的legacy Relation fixture，属于test setup error；改用既有Relation helper，未改产品。
2. empty-world fixture第一轮从plugin root寻找profile，属于test setup error；只修正test-only repository root。
3. 一次早期focused nested session没有保存final output identity，整次观察不计入资格。
4. semantic report attempt 1假定required-failure总有FactSet，对合法null FactSet触发`TypeError`；attempt 2只修proof facility。
5. source review发现初版carrier在foreign closure substitution时只撤销mutable current closure，可能保留原始authority；在formal qualification前
   改为始终撤销bound closure，并增加原eligibility必须`REVOKED`的falsifier。
6. 上述source correction发生时已运行中的两套full与四套focused旧字节进程全部降为non-qualifying；其中运行中进程被中止，已成功的
   两个focused结果也不回填final bytes。final matrix使用独立fresh process identities重跑。
7. semantic attempt 2属于source review以前的bytes，保留但不计；attempt 3才是final semantic identity。
8. 第一轮Core Markdown/hygiene unittest命令遗漏repository `src` import path，Markdown module import失败；fresh attempt 2只在
   该命令内设置`PYTHONPATH`并完成9/9 PASS，不修改全局环境或产品bytes。

这些记录不构成formal product failure，也不得被后继PASS删除或重解释。

## 10. tracked scope 与资格上限

本候选只允许七个tracked path：

```text
README.md
AGENTS.md
docs/329-r1-fact-to-coverage-exact-input-successor-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_fact_fulfillment.py
plugins/review-attention/src/veritrail_review/_fact_to_coverage_exact_input_handoff.py
plugins/review-attention/tests/test_fact_to_coverage_exact_input_handoff.py
```

完整资格链为：

```text
final implementation bytes + declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> finite closeout
```

全部闭合以后，最高状态仍只是：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_EXACT_MAIN_VERIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_READBACK_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_FROZEN
```

`FROZEN`必须由fresh CONTROL LOOP建立独立docs-only freeze publication并完成自己的资格链。本文不授权Coverage producer、旧
composition消费、manifest successor、Evidence、persistence、public Review产品或R2–R6。

## 11. 当前状态

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
