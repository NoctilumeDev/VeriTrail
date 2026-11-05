# R1 public project-state projection audit readback bundle-persistence failure boundary

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea`，tree
> `0ea5aaed6e0dfe50e6af2c50a7f7891108be8141`。
>
> 受审对象：PR #402 合入后的 README formal acceptance-bundle evidence persistence error。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY + PROOF_FACILITY`。本文只冻结失败身份、未运行目标、资格影响、
> proof-facility归层与最小恢复责任；不修改runtime、tests、workflow、Schema、Provider、Collector、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict、doc350、doc349或`docs/project-state.md`。

## 1. CONTROL LOOP 输入：doc350 已合入，但自己的 readback 没有资格化

[文档350](350-r1-public-state-projection-successor-readback-failure-boundary-audit.md)只审计PR #401 successor 0.2的README
formal marker drift。它由PR #402以精确坐标进入资格链：

```text
base = f553822f8ce54793103efd97c2e1ac8da487349e
head = 77c9140a736f95b311617e568ad06a5ce5f4b679
candidate tree = 0ea5aaed6e0dfe50e6af2c50a7f7891108be8141
commit count = 1
scope = README.md
        AGENTS.md
        docs/350-r1-public-state-projection-successor-readback-failure-boundary-audit.md
        docs/milestones.md
```

local qualification、original Public CI `41956025003` attempt 1、protected merge与new exact-main gates均成立：

```text
protected merge = 4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea
merge tree = 0ea5aaed6e0dfe50e6af2c50a7f7891108be8141
parents = f553822f8ce54793103efd97c2e1ac8da487349e
          77c9140a736f95b311617e568ad06a5ce5f4b679
exact-main Public CI = 41960100228 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 41960100243 / attempt 1 / 1 of 1 SUCCESS
```

exact-main双门qualification SHA-256为：

```text
a4c3873bf9b0485be733efe7cd0c9f68c7430f93db69ea814abeaa0ce0e7d2d5
```

这些门不自动使doc350成为qualified history，也不允许继承doc350所审计的#401失败身份作为自己的readback资格。

## 2. fresh installed-product formal error identity

fresh detached worktree精确绑定`main@4fd9a78…`。显式Python 3.13.13 venv、公开0.13.0/0.1.0 wheel、public bytes、
pre-plan与pre-formal validation均成立；61-file adapter freeze SHA-256为：

```text
b6dfa70d4ff573e4f8d7dd2e7c6151b5796538c334f4b8cc08855593ac24b8f9
```

第一次anonymous rate diagnostic观察到remaining 0并保留reset；reset后exact source/setup/adapter/worktree、remote main与primary audit
重新核对无漂移，diagnostic #2与API preflight #1成功。README fresh diagnostic身份为：

```text
identity = r1-psp-v2-readback-fb-audit-diagnostic-readme-1-4fd9a78
classification = DIAGNOSTIC_ONLY_NON_QUALIFYING
render coverage = COMPLETE
top-level HTTP status = 200
```

唯一formal身份为：

```text
identity = r1-psp-v2-readback-fb-audit-formal-readme-1-4fd9a78
collection_session_id = github-paired-49ccb98df7cd4c3e9f72cd3d170cbc63
API coverage = COMPLETE
Render coverage = COMPLETE
top-level HTTP status = 200
literal marker = successor 0.2 的 README 正式读回失败已按原身份保留
rendered text occurrences = 1
samples stable = TRUE
active streams = 0
cleanup errors = 0
classification = FORMAL_READBACK_ERROR
Core verdict = NONE
```

三次content-window sample digest均为：

```text
43d4e87d519599c259f3324fa291b8aa82cb209a9ea409785dad2410d7752678
```

API与Public Render标准Evidence已经以同一collection session完成，marker也满足原oracle。Acceptance Core随后在Verdict形成前写入
acceptance-bundle Evidence时触发：

```text
FileNotFoundError: [Errno 2] No such file or directory
stage = ACCEPTANCE_BUNDLE_EVIDENCE_PERSISTENCE_BEFORE_CORE_VERDICT
failed path characters = 271
failed path exceeds legacy Windows MAX_PATH = TRUE
```

失败路径及stderr、API/Render Evidence、handoff、sealed input plan与历史均原样保留。271字符与错误共现只支持一个需要审计的
long-path compatibility hypothesis，不能把MAX_PATH、Python、Windows registry、临时目录清理、并发或其他文件系统机理任选一个宣布为根因。

failure-boundary、93-artifact failed-readback closeout与finite integrity SHA-256为：

```text
6e33bedd7228ac7f080f9209374b9fa3671d8e12e6fb318832e943477e90e397
87592d66e1c3d3eed5e2ea5b73a60f3bbd90047c15416318a3b18ee04e31dd7e
35ea330b2d05646fbef5b7693fc78fa417526e1130419ed5b61f0d960396f6a6
```

## 3. 失败归层

本次non-success不是GitHub API缺失、Public Render marker drift、coverage partial、HTTP错误、cleanup failure、Core FAIL或Verdict
不满足。当前证据只允许：

```text
README public observation = COMPLETE / MARKER PRESENT ONCE / CLEANUP COMPLETE
acceptance-bundle evidence persistence = ERROR / FAIL_CLOSED
Core verdict = NOT_CREATED
doc350 readback qualification = FAILED / NOT_QUALIFIED
Collector regression = NOT_ESTABLISHED
candidate semantic regression = NOT_ESTABLISHED
proof-facility local output failure = ESTABLISHED
legacy Windows MAX_PATH causality = HYPOTHESIS / NOT_ESTABLISHED
underlying local filesystem cause = UNKNOWN
```

产品没有在Evidence持久化不完整时生成Verdict或PASS，因此fail closed。该行为不把错误提升为产品语义资格，也不能把一次本地路径失败
解释成GitHub、Core evaluator、Collector或candidate bytes的单一缺陷。

## 4. 未运行目标与禁止拼接

README formal non-success后，资格链按停止线停止：

```text
doc350 diagnostic/formal = NOT_RUN
AGENTS raw formal = NOT_RUN
milestones raw formal = NOT_RUN
independent success reconciliation = NOT_RUN
```

这些目标不能借用#400、#401或任何旧exact world。README observation COMPLETE与marker PASS也不能绕过bundle persistence错误，拼成
doc350资格。

## 5. retained history 不被回填

本失败新增在既有历史之后，不改变：

- PR #398仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #399/doc347仍是failed、closed、unmerged、not qualified，runner/subprocess stall底层原因仍是`UNKNOWN`；
- doc348仍是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
- PR #401/doc349与projection 0.2仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #402/doc350现在是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- private implementation仍未冻结，global composition authority未恢复；manifest、Evidence、persistence、public Review与R2–R6仍未授权。

## 6. 禁止的伪恢复

以下动作都不能产生doc350资格：

```text
重跑README formal #1或在同一#402 world换短目录retry until PASS
继续运行doc350/AGENTS/milestones后拼接结果
把API/Render COMPLETE、marker一次或diagnostic COMPLETE当作formal PASS
删除或改写271字符失败路径、stderr、partial bundle或failed closeout
把MAX_PATH hypothesis改写成已证实单一根因
启用认证访问替代fresh anonymous installed-product observation
用#400/#401或其他exact world的readback继承给#402
弱化Evidence持久化、Bundle完整性或Core Verdict形成条件
从本审计直接恢复projection 0.2、创建successor 0.3或启动后续runtime seam
```

## 7. 本审计的最小职责与公开观察面

本candidate只允许：

```text
README.md
AGENTS.md
docs/351-r1-public-state-projection-audit-readback-bundle-persistence-failure-boundary.md
docs/milestones.md
```

它不修改doc350、doc349、`docs/project-state.md`、runtime、tests、workflows或frozen contracts。本审计自己的fresh readback必须在
formal前机械证明output root和最坏case acceptance-bundle target不超过声明的本地path budget；该preflight只约束证明设施，不回填或
重跑#402 formal。合入后observation继续区分：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；使用首页可见区新增的bundle-persistence failure marker |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整bytes与digest |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation；不把raw bytes冒充Render COMPLETE |

independent reconciliation必须核对base/head/tree、四文件scope、#402 gates、formal bundle-persistence error、failure-boundary/failed
closeout/finite integrity、doc348 qualified history、#398/#399/#401 retained identities、primary audit continuity与四个fresh observations。

## 8. 本审计自己的资格链

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、`git diff --check`、
global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O` focused unchanged-runtime witness。测试只证明
本docs-only candidate没有修改runtime，不解释#402底层根因。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 7
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一non-success都保留原身份并停止。全部门闭合后本文也只成为qualified history；它不使doc350、doc349或projection 0.2 qualified
或frozen。

## 9. 当前状态与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文形成新事实后必须返回CONTROL LOOP。若没有新反例，下一最小seam才是从新的exact main建立独立、versioned docs-only doc350
readback recovery publication，并为它建立新的短output root与fresh observation identities；不得重跑#402 formal、跳过audit recovery直接
创建projection successor 0.3、冻结private implementation或启动manifest/Evidence/persistence/public Review/R2–R6。
