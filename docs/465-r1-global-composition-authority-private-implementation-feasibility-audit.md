# R1 global composition authority private implementation feasibility audit

日期：2026-11-28

> 当前状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@3ddf67e400fc91e8e2cad0d83bbe168bef32f94c`，tree
> `7041352ae69920756c0e9fd8a407257e890d9a39`。
>
> 影响：`L0_DOCUMENTATION / PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_ONLY`。本文只判断冻结的
> `R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1`能否由一个有界private owner补丁实现；不创建runtime、
> 不授权实现、不修改Schema/public export/CLI/publisher/Core/persistence，也不启动public Review、R2–R6、
> 外部开源系统集成或R1后的human+AI全项目检查。

## 1. CONTROL LOOP输入与合同冻结事实

PR #529已经把[合同冻结发布](464-r1-global-composition-authority-contract-freeze-publication.md)从exact base
`5d06cbe831015aff56cde6b6263c1de2bf780d64`、candidate head
`49cb6d99b3b36ae29e1085b0dc8200e639e4174b`、tree
`7041352ae69920756c0e9fd8a407257e890d9a39`精确合入本基线。original Public CI `46092721018`、
exact-main Public CI `46097074891`与Browser Smoke `46097074897`均为attempt 1 SUCCESS（15/15、15/15、1/1）。

fresh README/doc463/doc464 Render与AGENTS/milestones raw-byte observations各有唯一qualifying PASS。README
diagnostic #1的proof-facility `plan_id`长度错误和doc464 formal #1的GitHub public page HTTP 503 / Render
`PARTIAL` / `ERROR` / lower cause `UNKNOWN`均按原identity保留；新的独立doc464 formal #2才是qualifying PASS。
独立reconciliation、130-artifact finite closeout与post-closeout integrity分别为：

```text
reconciliation  be4646b3b23bf4019266a61db38f497ec49f1b903bb211f9196fd33235eb55b0
finite closeout  7682cf8d8ec0c9ecaffeeafd897c5cf268d6a290f9d9502e265a1c354fcd2a5a
integrity        2da1b95b04a1309786b56126c252efe5b4c76f6298987048743c79f43dcc8c9d
```

因此`R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN`已经生效。该新事实只解除可行性审计的停止线；
runtime仍为`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 需要回答的问题，而不是需要证明的替代命题

本审计的原问题是：能否在不改变任何冻结上游语义的前提下，以一个private production模块和一个focused test模块建立
唯一global composition owner，使它：

1. 绑定sealed exact input、ReviewPolicy、Review Profile与Provider roster；
2. 拥有一个live `BudgetContext`和一个same-attempt capture slot；
3. 在同一attempt内按冻结顺序选择四个normal或四个qualified negative world的唯一合法路线；
4. 只调用既有冻结private successor，传播最早failure并闭合owned resource；
5. 把同一attempt的copy-owned结果交给独立admission，得到one-shot private admitted result；
6. 不获取现实事实、Core Verdict或证据充分性裁决权。

不能把以下较弱命题当作答案：模块可以import、fixture能生成八个对象、Manifest能写出文件、测试可以PASS，或业务层认为证据
已经足够。`Proof is not problem-solving`在本层的机械含义是：审计必须保持原问题、冻结denominator、authority ceiling与停止线；
若实现必须改变它们，就应报告不可行，而不是换一个更容易证明的目标。

## 3. exact frozen source与八个live worlds

审计绑定[当前状态审计](462-r1-global-composition-authority-current-state-audit.md)、
[versioned合同](463-r1-versioned-global-composition-authority-contract.md)、doc464、primary `audit.json`、PR #529 closeout与
下列八个private source identity：

```text
_post_terminal_fact_dual_successor.py                    d7f19f631f4527278f4f660a2aa7a57b661ced0ec51a2a5cffa954b15e2e0742
_unified_review_coverage_output_admission.py              5194c7431429a9181c8e2a744fe419816699be835a05b54b831c806d05b5be51
_same_attempt_derivation_evidence_continuity.py           6c11b5e04c16a86157fd69c74b7bf1c308861ac6e5f5351cbbc00e5b6d2c8d3c
_derivation_evidence_manifest_carrier_successor.py        276d9a3b001d9ce616b1b138395187cd5813969b5137cd71bae26d2327e11a7c
_review_derivation_manifest_0_2.py                        2960da3f6dd511d8da8aed1629a40dcea36adc4de8e461e83292e341b1db1985
_review_derivation_manifest_0_2_conformance.py            a059f1967c9ae08854523f9d0d6b2d2a26799dbb43d00e7fc309fe9ed01b6cec
_relation_transition_slice_composition.py                 93c82eca051908fc69756881aa2ba392aec7d4d1b651e5cd52f2712517e3a8b1
_negative_world_coverage_authority_recovery.py             a8dfbff70ed914af35e924be66c5448e88a9d10777e94a892e0885372fdb90d6
```

read-only审计在每格重新构建并消费：

| world | class | terminal branch | selector route |
| --- | --- | --- | --- |
| `NORMAL_CONSISTENT` | normal | `NORMAL_FULFILLED` | `RELATION_HANDOFF` |
| `NORMAL_BRANCH_EMPTY` | normal | `NORMAL_FULFILLED` | `RELATION_HANDOFF` |
| `NORMAL_SLICE_PARTIAL` | normal | `NORMAL_FULFILLED` | `RELATION_HANDOFF` |
| `NORMAL_RELATION_CONFLICT` | normal | `NORMAL_FULFILLED` | `RELATION_HANDOFF` |
| `ZERO_PARSE_DENOMINATOR` | qualified negative | `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` |
| `ALL_PARSE_REJECTED` | qualified negative | `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` |
| `PROJECTION_BLOCKED` | qualified negative | `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | qualified negative | `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` |

每个world都经过carrier projection/candidate/independent validation/admission、Manifest 0.2
candidate/independent validation/admission/consume/private staging；staging replay统一拒绝为
`MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED`。carrier replay、candidate mutation、admitted copy与unknown version也分别按冻结family
fail closed。

## 4. 最小private实现边界

审计确认一个最小补丁可以保持所有上游文件只读：

```text
add plugins/review-attention/src/veritrail_review/_global_review_composition_authority.py
add plugins/review-attention/tests/test_global_review_composition_authority.py
modify existing runtime files = none
modify public files           = none
```

production模块只允许包含versioned private binding/owner/admission/result。它可以保存对exact sealed inputs、live context、roster与
冻结private value的引用，机械调用现有successor，并让独立admission从copy-owned material与这些exact reference复算identity、digest、
route、topology、earliest failure和resource closure。它不得新增第二条Fact路线、公共carrier、Schema、CLI、publisher或持久化格式。

这不是实现设计的任意扩张。若施工发现上述一个模块无法满足合同，必须停下并把真实反例归到最小受影响合同边界；不能靠修改上游、
放宽public面或增加特殊例外维持“可行”结论。

## 5. hard stop审计

四格审计对以下停止条件全部得到`false`：

```text
frozen upstream semantic change required  = false
public Schema or export required           = false
Core change required                       = false
persistence required                       = false
Provider semantic change required          = false
second Fact route required                 = false
world denominator change required          = false
Verdict authority required                 = false
```

当前public export仍没有global owner符号，review plugin仍没有`[project.scripts]`，publisher仍不处理Manifest 0.2；拟议production/test
文件也确实尚不存在。因此审计没有把“缺少实现”偷换成“已经实现”。

## 6. 四格semantic audit与focused witness

Python 3.10.6 / 3.13.13 × normal / `-O`四格分别从exact base重建八world。四格共同semantic projection为：

```text
fc91e59b7f2a2b46af9f388872c7f0c0b674273dee2a821a7e834f3df12a7541
```

audit matrix SHA-256为
`c474505bf19c7a5d94689fe06ab5a94f7f212a1119a9f32b3c204e3053092a01`，四格均PASS。

focused matrix attempt 1错误地把四个private plugin tests注册为不存在的repository-root `tests.*`模块；每格得到四个
`ModuleNotFoundError`，只运行另一个同名schema suite的五项测试，并错误报告9项。该
`b0a92443f579ac30837f444636c988e2c2b109cefb3ef55e0b32323ea3969116`矩阵与全部日志永久保留为
`PROOF_FACILITY_TEST_ROOT_SETUP_ERROR / NON_QUALIFYING / EFFECT_NONE`；同一attempt的global/local hygiene仍为8/8 PASS。

新identity的attempt 2从plugin test root运行五套冻结private回归：

```text
Python 3.10.6 normal  115 tests / PASS
Python 3.10.6 -O      115 tests / PASS
Python 3.13.13 normal 115 tests / PASS
Python 3.13.13 -O     115 tests / PASS
```

global/local hygiene同样8/8 PASS；attempt 2矩阵SHA-256为
`ce321cabb44fa80e2dc52be7d8c3843d11110a9c265733e95fdef384faa2ba57`。这些结果只作可行性witness，
不替代未来implementation自己的测试与资格链。

## 7. 审计结论与authority ceiling

结论是：`FEASIBLE_WITHIN_FROZEN_CONTRACT`。它只意味着冻结合同目前存在一个不要求扩张边界的有界private实现路径。

Reality仍拥有现实事实；Provider只拥有自己实际观察到的事实与来源；R/Q/O/T只在冻结合同内承担分析、观察与调度；global
composition owner只组织同attempt流程与能力选择；Core仍独占Evidence binding、integrity、sufficiency、determinacy与Verdict。
Business/global owner可以停止重复采集或请求补充条件，不能自行宣布证据充分或PASS。

本文自己的完整资格链闭合后也最多成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。下一步只能返回CONTROL LOOP，另建独立
docs-only private implementation authorization publication；其唯一seam identity为
`DOCS_ONLY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION`。在该publication完整资格化以前，拟议两个源码文件不得创建。

## 8. 本候选资格链

tracked scope只允许README、AGENTS、本文与milestones。local exact scope、UTF-8/LF/final LF、Markdown/link、`git diff --check`、
primary audit continuity、双Python普通/`-O` semantic audit、focused regression与global/local hygiene成立后，再依次完成：

```text
original PR Public CI 15/15
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc464 / 本文 Render
    -> fresh AGENTS / milestones raw-byte observation
    -> independent reconciliation + finite closeout
    -> FEASIBILITY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

当前只允许：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

