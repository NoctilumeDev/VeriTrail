# R1 same-attempt DerivationEvidence continuity 合同冻结恢复发布 v2

日期：2026-11-11

> 条件化状态目标：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，该目标不是生效事实。
>
> 发布基线：`main@07e78c18fe9bbea0825936af4218e28192d5a761`，tree
> `a56a90ca887dfa23b8798b3707479a34207f01c0`。
>
> 上游：[最小合同 0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [第一次恢复发布](400-r1-same-attempt-derivation-evidence-continuity-contract-freeze-publication-recovery.md)与
> [formal readback failure boundary](401-r1-same-attempt-evidence-continuity-freeze-recovery-formal-readback-failure-boundary.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改doc397、doc400或doc401历史，不复用PR #459
> 的formal PASS/ERROR，不修改runtime、tests、workflow、Schema、Provider、Collector、oracle、Verdict、manifest、
> persistence、public Review、global composition authority或R2–R6 authority。

## 1. CONTROL LOOP 与恢复起点

doc397已经由PR #456资格化为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。它冻结前的最小语义仍然是：versioned
private continuity owner在原执行期copy-own既有owner签发的material，捕获normal与四类qualified negative branch，证明exact
same-attempt binding，并以one-shot、fail-closed lifecycle完成独立reconciliation。后继事实没有击穿这些semantic bytes。

第一次freeze publication PR #457因Agent在original creation gate终态前编辑PR metadata而触发同head replacement run；original run
`42740181591` attempt 1为`CANCELLED`，PR关闭且未合并。PR #458只资格化这个操作失败边界，doc399成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；它没有资格化PR #457或冻结合同。

第二次publication PR #459从新exact main独立重建doc400。它的original Public CI `42821799379`、exact-main Public CI
`42828992788`与Browser Smoke `42828992853`均attempt 1 SUCCESS（11/11、11/11、1/1）。但是合入后唯一doc400 formal readback
得到`API COMPLETE / Render PARTIAL / HTTP 503 / no Core Verdict / FORMAL_READBACK_ERROR`。README、doc397、doc399的三个
formal PASS不能补齐doc400，故doc400保持`MERGED / NOT_QUALIFIED / NOT_FROZEN`；失败分类保持
`FORMAL_READBACK_RENDER_HTTP_503_PARTIAL_CONTENT_SCOPE_MISSING`，lower cause保持`UNKNOWN`。

PR #460只审计这个exact-main readback失败边界。它已经把doc401 candidate
`eacba181ceffd8afd04f458e04badd0c9542a64d`、tree `a56a90ca887dfa23b8798b3707479a34207f01c0`精确合入本发布基线。
original Public CI `42865862410`、exact-main Public CI `42873786269`与Browser Smoke `42873786277`均attempt 1 SUCCESS
（11/11、11/11、1/1），没有rerun。fresh README/doc401 formal与AGENTS/milestones raw-byte observations均唯一PASS；独立
reconciliation、135-artifact finite closeout与finite integrity SHA-256为：

```text
4aeb976426cf77d9a4e1d42d8ff7de8414f7b24d907a38254b19cbea00efaf0e
4cecfbec298c283f625af36417c5847e918aed02874dc8b1d69cc3f574179838
bef3d52b1de4fd99460c12f8abfd3dda76008e99d2034b898cf91e8e72033ab6
```

所以doc401现在是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。diagnostic plan ID长度与可变history误冻结两个proof-facility
setup error均以`NONE`保留；它们没有形成产品观察，也没有改变oracle。PR #459的HTTP 503首败、三个相邻formal PASS和未执行的
raw observation仍各自保持原identity，不能被PR #460后继PASS解释或覆盖。

## 2. 本publication的唯一职责

fresh CONTROL LOOP重新检查原工程问题、doc397适用世界与当前最小seam。same-attempt continuity合同仍有必要，doc397内容仍有效，
当前缺口仍只是尚无一个完成自身全部最后门的freeze publication。因此本文只承担一个职责：

```text
在本文自己的独立资格链全部闭合以后，
把doc397已经资格化的合同字节发布为frozen contract。
```

本文不证明runtime已经实现，不产生continuity value，不恢复global composition authority，不创建manifest、persistence或public Review，
也不授权R2–R6。

## 3. Qualification worlds不可拼接

| World | Identity | Qualification effect |
| --- | --- | --- |
| 合同候选 | PR #456 / doc397 | `QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN` |
| 第一次失败publication | PR #457 / original run `42740181591` | `CANCELLED / NONE` |
| 第一次失败边界 | PR #458 / doc399 | `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY` |
| 第二次失败publication | PR #459 / doc400 formal #1 | `MERGED / FORMAL_READBACK_ERROR / NONE` |
| 第二次失败边界 | PR #460 / doc401 | `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY` |
| 当前恢复publication | 本文自己的base/head/tree/final bytes/original run/readback | 尚未资格化 |

机械约束是：

1. PR #457后继run不能替代被取消的original run；
2. PR #459相邻三个formal PASS不能替代doc400 formal ERROR；
3. PR #460的PASS只资格化doc401，不回填doc400，也不解释HTTP 503；
4. doc397内容正确且已资格化不等于本文的conditional target已经生效；
5. 本文必须拥有新的commit、tree、original creation run、protected merge、exact-main gates与fresh product readback；
6. 本文后继PASS不能删除任何既有FAIL、ERROR、CANCELLED、setup failure或`UNKNOWN`。

## 4. 冻结对象与authority ceiling

本文只发布doc397定义的五个private identities：

```text
contract function                 r1-same-attempt-derivation-evidence-continuity/0.1
private continuity domain         SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1
controller capture function       r1-derivation-evidence-controller-capture/0.1
branch projection function        r1-derivation-evidence-continuity-branch-projection/0.1
independent reconciliation        r1-derivation-evidence-continuity-reconciliation/0.1
```

冻结以后仍保持：Reality/Provider拥有各自现实观察；continuity owner只copy-own既有material并证明连续性；Business Layer可以组织能力、
顺序和并行，但不能缩小sealed denominator或宣布PASS；Core只裁决binding、integrity、sufficiency与determinacy，不取得现实事实authority。
normal与四类negative route必须exact、same-attempt、same live `BudgetContext`、one-shot且fail closed。legacy Evidence 0.2与既有
Fact/Relation/Slice/Coverage、unified output admission及全部历史冻结字节不变。

`CONTRACT_FROZEN`只解除后继private implementation feasibility审计的阶段阻断；它不等于implementation authorized，更不授予
public Schema、manifest、persistence、public Review、Core Verdict、global composition authority或R2–R6 authority。

## 5. 原问题、当前证明义务与适用世界

```text
original engineering problem = normal与四类negative route需要same-attempt端到端证据连续性
current proof obligation      = 本恢复publication v2自己的全部最后门与跨表面状态一致性
applicability world           = 本publication exact base/head/tree/final bytes/original attempt/fresh readback
proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

形式上证明本文资格链成立，不等于runtime已经解决原工程问题；局部合同冻结也不等于R1各局部结论已经全局可组合。R1完整闭合后必须
另做global check；该未来义务不扩张本文authority。

## 6. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/402-r1-same-attempt-derivation-evidence-continuity-contract-freeze-publication-recovery-v2.md
docs/milestones.md
```

doc397、doc399、doc400、doc401、失败PR #457中的doc398、`docs/project-state.md`、runtime、tests、fixtures、workflow、Schema、
Provider、Collector、oracle、Verdict与全部frozen semantic bytes保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、唯一条件
marker、doc397合同字节、doc399/doc401 qualified history、PR #457与PR #459失败身份、authority ceiling、
`git diff --check`、global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

## 7. 独立资格链与original-gate操作纪律

```text
publication v2 final bytes / declared local gates
    -> original creation-event Public CI 11/11, attempt 1, no rerun
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc397 / doc399 / doc400 / doc401 / 本文 readback
    -> fresh AGENTS / milestones raw+Contents API+exact-Git byte observations
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> finite closeout and integrity
    -> conditional target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

PR title、body与base metadata必须在创建PR前完成。original creation gate终态前禁止`gh pr edit`或任何触发
`pull_request.edited`的metadata mutation。补充本地证据只进入外部append-only evidence。任何non-success按原identity保留并停止，
不得使用same-head后继run、rerun或retry-until-PASS替代。

本文fresh Plan/session/Evidence不可复用PR #459/#460 readback；diagnostic不计入资格。产品调用必须清除GitHub token、`NO_PROXY`、
`PYTHONPATH`与`PYTHONHOME`，仅按命令使用`http://127.0.0.1:7897`。本地worktree挂载、proof wrapper与sidecar错误只在其实际
层级保留，不得冒充产品结论。

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
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_PR459_MERGED_EXACT_MAIN_FORMAL_READBACK_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_EXACT_MAIN_FORMAL_READBACK_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_V2_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文最后门全部闭合后，开头的conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，独立审计private
implementation feasibility；不得把合同冻结解释为runtime已开始，或按文档编号自动进入manifest、persistence、public Review或R2–R6。
