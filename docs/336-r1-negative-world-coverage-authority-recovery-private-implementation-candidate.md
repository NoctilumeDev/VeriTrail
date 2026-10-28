# R1 negative-world Coverage authority recovery 私有实现候选

日期：2026-10-29

> 状态：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_CANDIDATE / NOT_FROZEN`。
>
> 施工基线：`main@e9602e0dc771ae9abf0fd4edd0e2f94a1bfba6d8`，tree
> `88762c45ab51ad7cdef894f727e11b495198bacf`。
>
> 本文只实现[文档335](335-r1-negative-world-coverage-authority-recovery-private-implementation-authorization-publication.md)
> 已生效的bounded A–J private producer、independent validator与same-attempt admission。不修改CoverageLedger 0.3、positive
> composition、Fact terminal、manifest、Evidence、persistence或public Review，也不启动R2–R6。

## 1. CONTROL LOOP 与已生效授权

文档335由PR #386从`main@91a7e6ba466b375ff6e4568ccc3a57ddd60ca044`建立，final head为
`ce98337a108721d0506b0e3cfbfb1ad5ac47c9c7`，candidate/merge tree为
`88762c45ab51ad7cdef894f727e11b495198bacf`，受保护合入后的exact main为本施工基线。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #386 original Public CI | `40719298650` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `40724767076` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `40724767006` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc334、doc335与milestones各有唯一qualifying PASS。independent reconciliation、
1360-artifact closeout、finite integrity与保留的stdout self-capture mismatch分别为：

```text
f1483e93b72fb5fe0f3213344df7737591c38f0dba5b098a73cf2dbeb8f4d91f
c2f1a621efc632ef4eb185b365ce4631327cd24c34da663e163e8455163dc7a2
2b156324547e7a8cadb96966c650b6bef68280e2b745aa7448c1997f081c5f21
afeffa6503cd6efbbb892493f18a7d88879a4bfa5da914e02b3f709bdb0f34cd
```

因此`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效；stdout self-capture只属于
proof-facility ordering，semantic effect为NONE。fresh CONTROL LOOP重验exact main、合同A–J、旧composition ceiling与primary
`audit.json`后，没有反例要求扩大施工面。

## 2. private identity 与tracked runtime surface

本候选实现并严格匹配以下冻结identity：

```text
consumer       r1-negative-world-coverage-exact-input-consumer/0.1
composition    r1-negative-world-review-coverage-composition/0.1
validation     r1-negative-world-review-coverage-independent-validation/0.1
admission      r1-negative-world-review-coverage-admission/0.1
relation absent r1-negative-world-relation-set-predecessor-absence/0.1
slice absent   r1-negative-world-review-slice-set-predecessor-absence/0.1
```

runtime只新增一个private producer/validator/admission module，并在0.2 carrier增加一个opaque-token private consume hook；package
`__init__.py`、public method list、0.3 conformance、positive composition与默认路径不变。新private result的authority ceiling只允许
`private_negative_world_coverage_ledger=true`，其余Fact/Relation/Slice/manifest/Evidence/persistence/public Review均为false。

## 3. 七阶段完整分母与branch语义

producer从同一live carrier重新取得original `DerivationInputSet`、Snapshot、Policy、Profile、verified blobs、Fact terminal source与
`BudgetContext`。Snapshot、Policy、Language、Parse与Fact分母都从original world枚举；Relation/Slice只在Fact universe确知为空时
known-empty，否则保持`UPSTREAM_DENOMINATOR_UNKNOWN`。

七个live world保持以下独立结果：

| world | Fact branch | overall |
| --- | --- | --- |
| empty inventory | `ZERO_PARSE_DENOMINATOR` | COMPLETE |
| unsupported-only | `ZERO_PARSE_DENOMINATOR` | PARTIAL |
| policy-excluded-only | `ZERO_PARSE_DENOMINATOR` | PARTIAL |
| all parse rejected | `ALL_PARSE_REJECTED` | PARTIAL |
| projection blocked | `PROJECTION_BLOCKED` | UNKNOWN |
| required Provider failed | `REQUIRED_PROVIDER_NON_SUCCESS` | UNKNOWN |
| required Provider unavailable | `REQUIRED_PROVIDER_NON_SUCCESS` | UNKNOWN |

同branch不会抹除前序stage partition。Fact `U`与`fact_projection.universe[]`双向绑定；representable成员用冻结`fact_id`，
unrepresentable成员使用冻结obligation domain。Provider completed bytes必须canonical且与expected semantic Fact匹配；non-success
Provider不能携带completed bytes，missing ref必须由assigned product responsibility覆盖。

## 4. independent validation 与common-mode防线

producer与validator拥有分离的known/unknown stage、Fact partition、overall、history projection与root-chain实现。它们只共享冻结常量、
canonical排序与既有0.3 conformance；validator不调用producer的关键projector，也不接受producer生成的conformance source。

validator直接从original carrier重建七阶段分母、三段branch-specific absent root、root chain、全部digest与expected candidate，然后用自己的
projections调用`bind_coverage_ledger_conformance_source(..., authority_safe=True)`。即使caller同步重签digest，以下rewrite仍被拒绝：

```text
Parse / Fact denominator shrink
all-rejected -> zero-denominator branch rewrite
semantic blocker -> DERIVATION_ERROR
FAILED / UNAVAILABLE reason collapse
expected -> completed without Provider terminal proof
qualified absence -> fabricated artifact root
dependent UNKNOWN -> COMPLETE
fixture conformance PASS without live admission
```

## 5. same-attempt、copy与one-shot admission

carrier private hook把lock与consumed bit放在同一个copy-stable state对象中。因此carrier保持原有浅拷贝行为，但original与所有浅拷贝
共享一个消费slot；并发或顺序消费恰有一个成功。新建的attempt、validation与admitted result都显式拒绝浅拷贝和深拷贝，不能靠复制
one-shot flags重放authority。

admission绑定原carrier claim id、原`DerivationInputSet`对象、原`BudgetContext`对象、Fact source digest、candidate bytes与同attempt
validation result，并只调用一次原始`BudgetContext.try_complete_phase(..., resources_closed=True)`。每次read重新验证carrier、context、
committed phase、candidate与validation；late stop、mutation、foreign validation、closest identity或replay都永久fail closed。

## 6. retained prequalification history

正式资格以前的non-success和review finding全部保留原identity：

1. remote-main命令坐标、两个PowerShell pipeline、Windows wildcard与缺少pytest属于setup/environment error；
2. 首轮focused run错误解释nested parse partition，产生4个ERROR；修正test oracle后未覆盖旧结果；
3. 首轮failure-family test发现admission错误泄漏validator failure family，已收紧为same-attempt family；
4. source review发现producer与validator共享高层stage/root projector的common-mode defect；分离实现并加入producer-only mutation falsifier；
5. imported `TestCase`导致direct unittest把历史case重复计入23-test分母；改用module helper后，新模块分母为14项；
6. shallow-copy carrier最初共享锁但复制consumed bool，original与copy各取得一个attempt；已改为共享copy-stable consume state；
7. shallow-copy attempt或validation最初可以各自admit；三个新authority-bearing type现均拒绝copy/deepcopy。

这些都在formal candidate qualification以前发现，没有可回填的formal product PASS，也不得被后继PASS删除。

## 7. final local qualification

最终candidate runtime字节的focused与完整Review Attention四格均以原始一次运行闭合；四格都绑定相同carrier、producer/validator与
owned test SHA-256。任何后继文档投影都不改变这些runtime bytes。

```text
focused matrix:
  Python 3.10.6 normal/-O  153 reported / 152 passed / 1 skipped
  Python 3.13.13 normal/-O 153 reported / 152 passed / 1 skipped

full matrix:
  Python 3.10.6 normal/-O  600 reported / 597 passed / 3 skipped
  Python 3.13.13 normal/-O 600 reported / 598 passed / 2 skipped
```

七个live world又由独立evidence facility在四格中逐一执行producer、independent validation与same-attempt admission；每格都单独核对
branch、七阶段status、overall与authority ceiling。由于claim/object identity合法地进入每个Ledger digest，四格的具体Ledger digest
不应相等；去除该per-attempt digest后的完整语义投影一致，normalized semantic SHA-256为：

```text
1d15e8b4ed37d5bb442d37cd034107f1ba00f6e530b0f414c987edb0b2686641
```

最终local gates还必须覆盖Python 3.10.6/3.13.13 normal/`-O` compile、`git diff --check`、global/local hygiene、Markdown、
exact scope、public export guard、frozen 0.3/positive-composition bytes与primary `audit.json` continuity。测试只是candidate witness，不能替代
original PR、protected merge、exact-main gates、installed-product readback或independent reconciliation。

## 8. tracked scope 与资格上限

本候选只允许七个tracked path：

```text
README.md
AGENTS.md
docs/336-r1-negative-world-coverage-authority-recovery-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_fact_to_coverage_exact_input_handoff.py
plugins/review-attention/src/veritrail_review/_negative_world_coverage_authority_recovery.py
plugins/review-attention/tests/test_negative_world_coverage_authority_recovery.py
```

完整资格链为：

```text
final implementation bytes + declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent reconciliation + finite closeout
```

全部闭合后最高仍只是：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_EXACT_MAIN_VERIFIED
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_READBACK_QUALIFIED
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_FROZEN
```

`FROZEN`必须由fresh CONTROL LOOP建立独立docs-only freeze publication并完成自己的资格链。本文不恢复旧composition消费权，不实现
manifest successor、same-attempt Evidence continuity、persistence或public Review，也不启动R2–R6。

## 9. 当前状态

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
