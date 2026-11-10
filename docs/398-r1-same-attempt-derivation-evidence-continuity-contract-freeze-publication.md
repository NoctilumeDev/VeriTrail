# R1 same-attempt DerivationEvidence continuity 合同冻结发布

日期：2026-11-10

> 条件化状态目标：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，该目标不是生效事实。
>
> 发布基线：`main@9578c173a60a7735ec2cb1792a46f6a19eb36c6c`，tree
> `85d095636db341d14eab2758ba8dd181b73f3fec`。
>
> 上游：[最小合同0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [feasibility recovery](396-r1-same-attempt-derivation-evidence-continuity-feasibility-recovery.md)与
> [original-gate failure boundary](395-r1-same-attempt-derivation-evidence-continuity-audit-original-gate-failure-boundary.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改doc397、runtime、tests、fixtures、workflow、Schema、
> Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Slice/Coverage semantics、manifest、Evidence、persistence、
> public Review、global composition authority或R2–R6 authority。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #456已经把doc397固定的versioned private continuity合同精确合入新的main world。它自己的final bytes、local qualification、
original PR gate、protected exact-head merge、新exact-main双门、fresh anonymous installed-product readback、raw-byte observation、
independent reconciliation与finite closeout均已成立。因此doc397现在最多是：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified contract candidate不等于frozen contract。fresh CONTROL LOOP重验原工程问题仍是让normal corrected route与四类qualified
negative Coverage route，在同一原始attempt内形成可复核的input→Fact→Relation/negative branch→Slice/Coverage→final admission
连续证据。doc397定义的versioned private owner、原执行期controller capture、五分支exact binding、one-shot commit与fail-closed
lifecycle仍是最小合法合同边界；没有新事实授权直接实现runtime、恢复global composition authority或启动manifest、persistence、
public Review、R2–R6。

因此本文只承担一个职责：在自己的独立完整资格链闭合后，把doc397固定的semantic bytes从qualified contract candidate发布为
frozen contract。本文不会把合同资格化冒充工程问题已经解决，也不会把局部合同正确冒充全局可组合性已经成立。

## 2. Exact contract candidate qualification

```text
PR                   = #456
base                 = a1d1ff8eac47506d25a65eae9c8b00a2ba89c3b1
head                 = a12d433f395108295f1b4b98f46804d129925972
ordinary merge       = 9578c173a60a7735ec2cb1792a46f6a19eb36c6c
candidate/merge tree = 85d095636db341d14eab2758ba8dd181b73f3fec
diff                 = 1 commit / 4 docs files
```

original Public CI `42723300711`、exact-main Public CI `42728102024`与Browser Smoke `42728101444`均为attempt 1
SUCCESS，分别11/11、11/11与1/1；没有rerun。PR #453曾缺失的两个required identity在PR #456自己的original attempt中均实际
instantiated并SUCCESS；这只资格化PR #456，不回填或解释PR #453。

candidate-local Python 3.10.6/3.13.13 × normal/`-O` semantic audit四格逐字节一致，canonical SHA-256为
`c775057ae337bed8400ee1f66baaf185cfa5486c52d1c4c82f871fcd73478e01`；focused witness四格各126项PASS。
candidate local qualification、precommit seal、postcommit seal、original PR/protected merge qualification、exact-main dual-gate
qualification与seal SHA-256为：

```text
9852af916b19a57f265ca352a085c9e3c7aab9d873aa2f8606bb4db6b7ceb25e
a9be78d75fe85b1613741ad85b8fac20082627dd27cb4212bd944369d32aa2fb
03a0e16bee5507f57f9e8bda579583d03425fbe7a38f71fabc502f8e0d6e80ad
41250df5b4627b6ff309623aecf4ce560e8668ccc554c3f855acc1ad4f75c242
c3f0cc311f6207a61d2affa35e4876c67466ca10d000f0a99d2c59150d55c7fc
285bb3a40d3dce4bd5ab26842155c2175a856a6e2db4edfdc94ca07206228b9c
```

PR #453仍保持closed、unmerged、original Public CI failed、not-qualified；missing required identities与lower cause继续为
`UNKNOWN`。doc395 failure-boundary与doc396 feasibility recovery只作为qualified history，不重解释失败world。

## 3. Fresh exact-main installed-product readback

fresh detached exact `main@9578c17…`上建立显式CPython 3.13.13 venv，安装公开Core 0.13.0与GitHub Evidence 0.1.0
wheel、Playwright 1.62.0与matching Chromium。产品观察清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按
命令注入；没有复用旧PASS。

README、doc396与doc397各有唯一qualifying formal；AGENTS与milestones各有唯一anonymous raw/Contents API/exact-Git全字节
一致观察：

| Target | Qualifying identity | Session / byte identity | Result |
| --- | --- | --- | --- |
| README | `r1-saec-contract-formal-readme-2-9578c17` | `github-paired-143d319ef69245c6a23283cf49ac31e7` | API/Render COMPLETE、Core PASS |
| doc396 | `r1-saec-contract-formal-doc396-1-9578c17` | `github-paired-9a917e08d5594e09809454c68b9ac73f` | API/Render COMPLETE、Core PASS |
| doc397 | `r1-saec-contract-formal-doc397-1-9578c17` | `github-paired-d619acf89d7f4c5f8372b8e0cf4e4bdb` | API/Render COMPLETE、Core PASS |
| AGENTS | `r1-same-attempt-evidence-continuity-contract-raw-agents-1-9578c17` | 647310 bytes / `9d63820d…f179e` | raw = API = exact Git |
| milestones | `r1-same-attempt-evidence-continuity-contract-raw-milestones-1-9578c17` | 701226 bytes / `c8112f49…c0dab` | raw = API = exact Git |

README formal #1必须永久保留：其public Render为`COMPLETE`、HTTP 200、marker一次，但anonymous GitHub API返回403与
`COLLECTION_BUDGET_EXHAUSTED`，所以API coverage为`ERROR`、Core Verdict未创建、qualification effect为`NONE`。preflight与formal
落入不同anonymous rate bucket的lower cause仍为`UNKNOWN`；较晚reset后的formal #2是新identity，不是rerun或洗白。

preformal、adapter-freeze attempt 1、adapter-freeze attempt 2、independent reconciliation、220-artifact finite closeout与finite
integrity SHA-256为：

```text
d3025cd53f394a560bd5f2826c4f10469cb74dc0e4433c6a22b76518a56c4024
ab5e1bb213f63d36ea5c48796a6e4363d87426034add515c8021d5a435c20f5b
f1c6ead0d6ad568d4f01180056abb1d86986beefa20c5bc57e5d6c041d19dfff
3814da77684be889954ae2f941acd431d03b0f71f46684fae39d3246de514637
91737bbeef61d19f440d8fccb9ce04a0110afcac9b9e13abf51d70ef8af88cd1
85baf887bbd6d1b71789d1bdf3b64c740f95d0b3e775daf146e77e4b055aed4d
```

Codex attachment cap、stale task cwd、append-only setup-history hash、adapter inherited plan prefix、anonymous rate diagnostic/preflight
#1与README formal #1全部保留原identity。adapter attempt 2只修正proof-facility identity；没有修改产品oracle、合同语义或旧失败。

## 4. 冻结对象、authority ceiling 与全局后验义务

本文发布的唯一semantic对象仍是doc397定义的：

```text
contract function                 r1-same-attempt-derivation-evidence-continuity/0.1
private continuity domain         SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1
controller capture function       r1-derivation-evidence-controller-capture/0.1
branch projection function        r1-derivation-evidence-continuity-branch-projection/0.1
independent reconciliation        r1-derivation-evidence-continuity-reconciliation/0.1
```

冻结以后仍必须保持：

- continuity owner只copy-own各owner已经签发的material并机械证明same-attempt连续性；它不拥有现实事实、不能缩小denominator、
  不能产生Seal、Verdict或sufficiency裁决；
- Reality与Provider拥有各自现实观察；Business Layer可组织能力与采集顺序，但不能改变sealed obligation或宣布PASS；
- Core只裁决binding、integrity、sufficiency与determinacy，不反向取得Provider现实事实authority；
- normal route与四类negative route必须exact discriminated、同一attempt、同一live BudgetContext并one-shot；post-hoc拼接、copy、
  replay、foreign attempt、clock substitution、cleanup incomplete与mutation都fail closed；
- legacy Evidence 0.2、Fact/Relation/Slice/Coverage语义、application output admission与全部历史冻结字节保持不变；
- public Evidence Schema、manifest、persistence、public Review、Core Verdict、global composition authority与R2–R6继续为false。

本publication机械分开：

```text
original engineering problem = normal与四类negative route需要same-attempt端到端证据连续性
current proof obligation      = 本freeze publication自己的全部最后门与跨表面状态一致性
applicability world           = 本publication exact base/head/tree/final bytes/attempt/fresh readback identity
proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

`CONTRACT_FROZEN`只解除private implementation feasibility的阶段阻断；不证明合同可实现，不授权runtime施工。R1最终完成以后仍必须
独立global check阶段间前提连续性、authority/qualification断点、局部结论可组合性与最终用户能力；该后验义务不扩张当前publication。

## 5. 本publication自己的exact scope与最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc318、doc377–397、
`docs/project-state.md`、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen semantic
bytes必须保持base不变。

本层local gates只重核publication边界：exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique
headings、条件marker、doc397资格与evidence continuity、PR #453 retained failure、authority ceiling、原工程问题/proof obligation/
applicability world分离、`git diff --check`、read-only global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json`
continuity。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc397 / 本文 readback
    -> fresh AGENTS / milestones raw+API+exact-Git byte observations
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> conditional target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP for private implementation feasibility
```

publication自己的fresh Plan/session/Evidence不可复用PR #456 readback；diagnostic不计入资格，任何non-success按原identity保留。
本地checkout alignment、worktree侧栏登记与cleanup只属于housekeeping/setup，不追加语义门。

## 6. 条件化target与停止线

本文进入仓库不等于冻结生效。在自己的全部最后门闭合以前，只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文最后门全部闭合后，开头的conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，独立审计private
implementation feasibility；不得把合同冻结解释为runtime已开始，或直接施工manifest、Evidence persistence、public Review或R2–R6。
