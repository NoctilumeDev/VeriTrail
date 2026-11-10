# R1 same-attempt DerivationEvidence continuity 合同冻结恢复发布

日期：2026-11-10

> 条件化状态目标：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，该目标不是生效事实。
>
> 发布基线：`main@d06c15082abf00163feeccecd9c9ae7afcd275fd`，tree
> `200169d1df56b852cd41abef9ca1c0b291c7f5c3`。
>
> 上游：[最小合同 0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)与
> [PR #457 original-gate cancellation boundary](399-r1-same-attempt-evidence-continuity-freeze-publication-original-gate-cancellation-boundary.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不复用PR #457 commit、doc398或PR metadata；不修改
> doc397、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、
> Fact/Relation/Slice/Coverage semantics、manifest、Evidence persistence、public Review、global composition authority或R2–R6 authority。

## 1. CONTROL LOOP 与恢复起点

PR #456已经使doc397成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。它固定的最小语义仍是：由versioned private
continuity owner copy-own既有owner已经签发的material，在原执行期由controller捕获normal与四类qualified negative branch，
机械证明exact same-attempt binding，并按one-shot、fail-closed lifecycle完成独立reconciliation。该合同没有被新反例击穿。

后继PR #457没有取得original PR qualification。它的original creation Public CI `42740181591` attempt 1在Agent编辑PR body后，
被同head `pull_request.edited` run `42740610446`按workflow concurrency取消。PR #457保持closed、unmerged、not-qualified；
doc398没有进入main。后继run无论终态都不能替代、重跑或回填original creation gate。

PR #458只审计这个失败边界。它已经以自己的独立资格链精确合入：

```text
base                 = 9578c173a60a7735ec2cb1792a46f6a19eb36c6c
head                 = 4ea4b18f1a87d14d477c9ef6bc0f43e220d013da
merge                = d06c15082abf00163feeccecd9c9ae7afcd275fd
candidate/merge tree = 200169d1df56b852cd41abef9ca1c0b291c7f5c3
scope                = 1 commit / 4 docs files
```

original Public CI `42746126616`、exact-main Public CI `42777936150`与Browser Smoke `42777936071`均为attempt 1
SUCCESS（11/11、11/11、1/1），没有rerun。fresh README/doc399 formal、AGENTS/milestones raw-byte observation、independent
reconciliation与109-artifact finite closeout全部成立；关键SHA-256为：

```text
original qualification = 9b8c049ebb4c544ab53c2313957a8c0d07bfa7f8c378ace3eba6c326a4443707
protected merge        = 7e9065a70015202d2e536d8247b2f2cfeac1c5c98fc0045f285c93e98a2d9ed3
exact-main gates       = 0e4820073bbe4bede0edf562ab6ddb766f6e88b69445d4a2c7001003d3e73ca1
reconciliation         = cf57c494db3cb81aa5b1e2567550d5d971f305c263fb6d53fb1240d8991b11c1
finite closeout        = 6abf27f119166a708ee95f5096a6b75eb19bb13c11f4f814b9244766677169df
finite integrity       = 7810561f5872b884484dab3a3c55460bbb8457dacd01f8f8de36841247e451f5
```

因此doc399现在是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。它只恢复了从新exact main独立重建freeze publication的资格；
没有资格化doc398、没有把PR #457改写为PASS，也没有冻结合同或授权runtime。

## 2. 本publication的唯一职责

fresh CONTROL LOOP重新核对原工程问题：normal corrected route与四类qualified negative Coverage route仍缺少一个被正式冻结的、
同一原始attempt内贯穿input→Fact→Relation/negative branch→Slice/Coverage→final admission的连续证据合同。doc397已经给出
最小合法合同边界；当前新事实没有要求version bump、修改owner topology或增加例外。

因此本文只承担一个职责：在自己的独立完整资格链闭合后，把doc397的已资格化合同字节发布为frozen contract。它不证明：

- runtime已经实现；
- continuity proof已经在真实attempt中产生；
- global composition authority已经恢复；
- manifest、persistence或public Review已经得到授权；
- R1的全部局部结论已经全局可组合；
- R2–R6可以启动。

## 3. Qualification worlds不可拼接

本文机械分开四个world：

| World | Identity | Qualification effect |
| --- | --- | --- |
| 合同候选 | PR #456 / doc397 | `QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN` |
| 失败publication | PR #457 / doc398 / original run `42740181591` | `CANCELLED / NONE` |
| 失败边界审计 | PR #458 / doc399 / exact main `d06c150…` | `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY` |
| 当前恢复publication | 本文自己的base/head/tree/final bytes/original run/readback | 尚未资格化 |

本文不得从前三个world拼接自己的qualification。特别是：

1. PR #457的same-head edited-event run不能替代它被取消的original run；
2. PR #458的11/11只资格化failure-boundary audit，不资格化本文；
3. doc397内容正确且已资格化不等于本文的frozen target已经生效；
4. 本文即使与失败doc398表达相近，也必须拥有新的commit、tree、original run、merge、exact-main gates与readback；
5. 后继PASS不解释PR #457的取消，也不删除其Agent qualification-procedure error identity。

## 4. 冻结对象与authority ceiling

本文发布的唯一semantic对象仍是doc397定义的：

```text
contract function                 r1-same-attempt-derivation-evidence-continuity/0.1
private continuity domain         SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1
controller capture function       r1-derivation-evidence-controller-capture/0.1
branch projection function        r1-derivation-evidence-continuity-branch-projection/0.1
independent reconciliation        r1-derivation-evidence-continuity-reconciliation/0.1
```

冻结以后仍必须保持：

- Reality与Provider拥有各自现实观察；continuity owner只copy-own已签发material并证明连续性；
- Business Layer可以组织能力、并行和采集顺序，但不能缩小sealed denominator或自行宣布证据充分/PASS；
- Core只裁决binding、integrity、sufficiency与determinacy，不取得Provider现实事实authority；
- normal与四类negative route必须exact discriminated、同一attempt、同一live `BudgetContext`并one-shot；
- post-hoc拼接、foreign attempt、replay、clock substitution、cleanup incomplete、mutation与placeholder都fail closed；
- legacy Evidence 0.2、Fact/Relation/Slice/Coverage语义、application output admission与全部历史冻结字节不变；
- public Evidence Schema、manifest、persistence、public Review、Core Verdict、global composition authority与R2–R6继续为false。

`CONTRACT_FROZEN`只解除后继private implementation feasibility审计的阶段阻断；它不等于implementation authorized。

## 5. 原问题、当前证明义务与适用世界

```text
original engineering problem = normal与四类negative route需要same-attempt端到端证据连续性
current proof obligation      = 本恢复publication自己的全部最后门与跨表面状态一致性
applicability world           = 本publication exact base/head/tree/final bytes/original attempt/fresh readback identity
proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

形式上证明本文资格链成立，不等于原工程问题已经由runtime解决；局部合同冻结也不等于整个R1的全部authority、qualification与
用户能力已经全局可组合。R1完成后必须另做global check；该后验义务不扩张本文authority。

## 6. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/400-r1-same-attempt-derivation-evidence-continuity-contract-freeze-publication-recovery.md
docs/milestones.md
```

doc397、doc399、失败PR #457中的doc398、`docs/project-state.md`、doc318、doc377–399、runtime、tests、fixtures、workflow、
Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持base不变。

本层local gates只重核publication边界：exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、
unique headings、条件marker、doc397/doc399资格与历史分离、PR #457 retained cancellation、authority ceiling、原工程问题/当前证明义务/
适用世界分离、`git diff --check`、read-only global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。
Public CI仍执行自己的完整原始门。

## 7. 独立资格链与original-gate操作纪律

```text
publication final bytes / declared local gates
    -> original creation-event publication PR gate 11/11, attempt 1, no rerun
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc397 / doc399 / 本文 readback
    -> fresh AGENTS / milestones raw+Contents API+exact-Git byte observations
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> finite closeout and integrity
    -> conditional target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

PR title/body/base metadata必须在创建PR以前完成。original creation gate终态前不得执行`gh pr edit`或任何会触发
`pull_request.edited`的新metadata mutation；补充本地证据只能写入外部append-only evidence，不改变PR event world。若original gate
出现任何non-success，按原identity保留并停止，不使用same-head后继run替代。

本publication自己的fresh Plan/session/Evidence不可复用PR #456/#458 readback；diagnostic不计入资格，任何non-success按原identity
保留。本地checkout alignment、worktree侧栏登记与cleanup属于housekeeping/setup，不追加语义门。

## 8. 条件化target与停止线

本文进入仓库不等于冻结生效。在自己的全部最后门闭合以前，只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_PR457_CLOSED_UNMERGED_ORIGINAL_GATE_CANCELLED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文最后门全部闭合后，开头的conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，独立审计private
implementation feasibility或其他仍成立的最小seam；不得把合同冻结解释为runtime已经开始，或直接施工manifest、Evidence
persistence、public Review或R2–R6。
