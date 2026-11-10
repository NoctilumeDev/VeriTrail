# R1 same-attempt Evidence continuity freeze publication original-gate cancellation boundary

日期：2026-11-10

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_PR457_ORIGINAL_GATE_CANCELLATION_BOUNDARY_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@9578c173a60a7735ec2cb1792a46f6a19eb36c6c`，tree
> `85d095636db341d14eab2758ba8dd181b73f3fec`。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_PROCEDURE_AUDIT_ONLY`。本文只保存PR #457 original creation run被同head
> `edited` event run触发的concurrency cancellation、检查被击穿的资格前提与最小恢复边界；不资格化失败publication、不修改
> workflow/concurrency/oracle、不得使用第二run替代original gate，也不实现runtime或授权manifest、persistence、public Review、R2–R6。

## 1. CONTROL LOOP 与失败坐标

上游PR #456已经把doc397合同候选精确合入
`main@9578c173a60a7735ec2cb1792a46f6a19eb36c6c / tree=85d095636db341d14eab2758ba8dd181b73f3fec`。
PR #456 original Public CI `42723300711`、exact-main Public CI `42728102024`与Browser Smoke `42728101444`均attempt 1
SUCCESS（11/11、11/11、1/1）；fresh installed-product readback、raw-byte observation、independent reconciliation与finite closeout也已闭合。
因此doc397保持`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。

PR #457绑定：

```text
base                 = 9578c173a60a7735ec2cb1792a46f6a19eb36c6c
head                 = 38e343ca036c3c6e3d1d68543107e9575abb3c0d
tree                 = c78106dd7122a70ffc1345316d2d899052320312
scope                = 1 commit / 4 docs files
original creation run = 42740181591 / attempt 1 / pull_request / created 2026-11-10T02:04:24Z
edited-event run       = 42740610446 / attempt 1 / pull_request / created 2026-11-10T02:08:01Z
```

candidate local final bytes曾通过Python 3.10.6/3.13.13 × normal/`-O`四格focused witness（各126项）、8/8 hygiene、exact
four-file publication validation与primary `audit.json` continuity。prequalification曾发现doc398指向doc395的relative link filename错误；修正后
重新运行了完整local matrix。local qualification、precommit seal、postcommit seal与post-seal proof-facility amendment SHA-256为：

```text
396e2e86d34ae890b7f5772fd8ac5ac4253c8980fd7f070922ba201064de7c80
210478a1a21322a281ff612259ff70be79d6a9a69bb203a8c6d368503bfb47e5
5569bcef7b289bb13c8f359bb7243267774f1cbc60e5ac5fa5ddf0eb66c8dee0
c3a6cccfdb1f6f035a935030cba34c26fd709e2655464407f644a0f8593ff54b
```

这些本地事实不能替代original PR gate。original creation run终态是`completed / cancelled`；PR #457已经关闭、未合并，remote main
继续为`9578c173…`。doc398没有进入main，也没有获得qualification或frozen状态。

## 2. Cancellation chain 与直接原因

`.github/workflows/ci.yml`在该exact base声明：

```yaml
pull_request:
  branches: [main]
  types: [opened, synchronize, reopened, edited]

concurrency:
  group: public-ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

original creation run `42740181591`运行期间，Agent为补充本地post-seal amendment identity执行了`gh pr edit`。该metadata edit在
`02:08:01Z`为同一PR、同一head创建新的pull-request run `42740610446`。concurrency随后取消original run：Python 3.13 job在
`Run Core regression tests with assertions disabled`中止，Python 3.10 job在`Run Core regression tests`中止；后继required jobs被记录为
`CANCELLED`。original run在`02:08:15Z`完成为`cancelled`。

因此直接failure identity是：

```text
ORIGINAL_PR_CREATION_PUBLIC_CI_CANCELLED_BY_SAME_PR_EDITED_EVENT_CONCURRENCY_REPLACEMENT
qualification procedure error = ESTABLISHED
candidate regression          = NOT_ESTABLISHED
Subject failure               = NOT_ESTABLISHED
product assertion failure     = NOT_ESTABLISHED
workflow byte defect          = NOT_ESTABLISHED
oracle defect                 = NOT_ESTABLISHED
```

这里不把原因降格为`UNKNOWN`：run创建时间、workflow `edited` trigger、concurrency key、`cancel-in-progress`以及原run cancellation时间形成
同一机械链。错误属于Agent的qualification procedure——在original gate终态前修改了会触发新run的PR metadata——而不是候选产品输出。

## 3. 两条run identity必须同时保留

original creation run `42740181591`保持：

```text
attempt 1 / completed / CANCELLED
Workbench = SUCCESS
E3 release acceptance = SUCCESS
Python 3.10 = CANCELLED
Python 3.13 = CANCELLED
downstream required jobs = CANCELLED
qualification effect = NONE
```

edited-event run `42740610446`是不同run identity，即使它后来SUCCESS，也只能证明metadata edit之后的新event world，不得替代、重跑或回填
original creation gate。关闭PR #457也不会把该run升级为资格输入。它的最终SUCCESS/FAILURE/CANCELLED均按自己的原identity保留，
`qualification effect = NONE`。

这次没有使用GitHub的rerun/retry命令；但“没有点击rerun”不等于original gate仍成立。新的event run已经让原run被concurrency取消，
所以original qualification事实确实失败。

## 4. Proof-facility failures 与candidate non-findings

以下identity继续保留：

- Codex侧栏超过100个artifact identity，worktree与PR attachment登记失败；
- 首个PowerShell branch probe对空结果调用`.Trim()`；
- 未引用的`HEAD^{tree}`在PowerShell中被错误拆分；
- doc398 prequalification attempt 1存在broken doc395 relative link，修正后全部local gates重跑；
- `gh run watch`本地显示进程被主动中断，只停止重复终端渲染，不取消GitHub run；
- 在precommit seal之后追加setup history，使原seal inventory成为历史而不是当前目录清单；独立post-seal amendment保留该事实；
- 为把amendment SHA补入PR body而执行`gh pr edit`，触发本次original-gate cancellation。

其中最后一项击穿资格链；其他项不能合并成产品失败，也不能用本地PASS抵消它。doc398内容的semantic反例没有建立；但doc398 candidate
仍为`NOT_QUALIFIED / NOT_MAINLINE / NOT_FROZEN`。

## 5. 反例处理原则

本失败继续使用：

> 理论遇到反例，先检查前提、适用域与观察是否成立，而不是不断增加例外。

本次机械含义是：

1. 不把“同head第二run可能全绿”增加为original gate的例外；
2. 不把local qualification、Workbench/E3 SUCCESS或未失败的步骤拼接成11/11；
3. 不把PR metadata edit说成“只改描述所以不影响资格”；它实际触发新run并取消original run；
4. 不因原因已定位为procedure error就回填原run为PASS；归因变化不改写`CANCELLED`；
5. 不修改workflow以绕过`edited` trigger或`cancel-in-progress`；当前最小边界是Agent操作纪律与独立新PR；
6. 不复用PR #457 commit、run或qualification。后继即使semantic文字相同，也必须从当时的新exact main重建commit/tree/original run。

## 6. 最小恢复边界

本反例只重开：

```text
FREEZE_PUBLICATION_ORIGINAL_PR_QUALIFICATION_PROCEDURE_ONLY
```

当前证据不授权修改doc397合同、workflow、required job count、concurrency、timeout、oracle、runtime、tests、fixtures、Schema或其他frozen
semantic bytes。最小恢复顺序是：

1. 本failure-boundary audit以自己的docs-only final bytes完成完整资格链；
2. 返回fresh CONTROL LOOP，从新exact main确认doc397仍为qualified candidate、freeze publication仍是最小合法seam；
3. 若无新反例，从新exact main独立重建freeze publication；不得cherry-pick PR #457 commit；
4. 新publication PR body必须在创建前完成并封存；original gate终态前不得执行会触发`edited` event的metadata修改；
5. attachment cap、补充证据或说明只能在不改变PR event world的外部append-only evidence中记录；
6. 新candidate仍必须完成自己的original 11/11、protected merge、new exact-main双门、fresh anonymous readback、raw-byte observation、
   independent reconciliation与finite closeout；
7. 后继PASS只证明新world成立，不解释、覆盖或回填PR #457。

如果本audit自己的original gate再次因Agent编辑PR metadata而被concurrency取消，才累计相同blocking condition；仍不得弱化gate。

## 7. Authority ceiling

本文最多支持：

```text
PR #457 publication candidate     = closed / unmerged / original gate cancelled / not qualified
doc397 contract candidate         = qualified candidate / not frozen
doc398 publication bytes          = not qualified / not mainline / not frozen
contract frozen                   = false
Evidence continuity runtime       = not started / not authorized
global composition authority      = not restored / not authorized
manifest / persistence / Review   = not started / not authorized
R2-R6                             = not started
```

`local_not_global = true`与`post_r1_global_check_required = true`继续成立。它们要求R1完成后独立检查阶段间前提、authority、qualification与
用户能力的全局可组合性；不扩张本failure-boundary audit。

## 8. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/399-r1-same-attempt-evidence-continuity-freeze-publication-original-gate-cancellation-boundary.md
docs/milestones.md
```

doc397、失败PR #457中的doc398、`docs/project-state.md`、doc318、doc377–397、runtime、tests、fixtures、workflow、Schema、Provider、
Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持base不变。

## 9. Qualification pipeline

本文final bytes必须完成exact scope、UTF-8/LF/final-LF、links/fences/headings、two-run identity与workflow trigger/concurrency核对、closed PR
identity、unchanged doc397/workflow、remote main、primary audit、`git diff --check`、read-only global/local hygiene与focused unchanged-runtime
witness。

```text
final failure-boundary docs bytes / local gates
    -> original PR required 11/11 gate
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent PR / run / workflow / source-byte / problem-identity reconciliation
    -> finite closeout
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

## 10. 当前状态与下一合法边界

在本文自己的全部最后门闭合以前，只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_PR457_CLOSED_UNMERGED_ORIGINAL_GATE_CANCELLED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_PUBLICATION_ORIGINAL_GATE_CANCELLATION_BOUNDARY_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整资格链闭合后最多成为`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；不得直接重建
publication、实现runtime、修改workflow，或启动manifest/persistence/public Review/R2–R6。
