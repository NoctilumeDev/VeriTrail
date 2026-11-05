# R1 public project-state projection doc354 readback anonymous rate exhaustion failure boundary

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_ANONYMOUS_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@95add9053c2984c0efe0cb87d1a4b64812215683`，tree
> `3619ceeba79145ebfe3af230e4ba22c89798c306`。
>
> 受审失败：PR #406 合入后的 README fresh anonymous formal API rate-budget exhaustion。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只冻结失败 identity、已完成的 Render observation、未运行目标、
> fail-closed 归层与后继责任；不修改 workflow、runtime、tests、Schema、Provider、Collector、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict、doc354、doc353、doc350、`docs/project-state.md` 或任何 frozen contract。

## 1. CONTROL LOOP 输入：#405 不被回填，#406 形成新的独立 world

[文档354](354-r1-public-state-projection-doc353-readback-marker-drift-failure-boundary.md)审计 PR #405 合入后的 README
fresh formal marker drift。#405 继续是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
第三个 formal 的源码 marker 一次、rendered-text marker 零次以及 GitHub render/visibility 根因 `UNKNOWN` 永久保留。

doc354 自己由 PR #406 以新的精确坐标进入资格链：

```text
base = 6af0dac952ec2bd3e015bc827b2b709908282036
head = a5dd28fa8b24b5517a09e5be9733e7e479658746
candidate tree = 3619ceeba79145ebfe3af230e4ba22c89798c306
commit count = 1
scope = README.md
        AGENTS.md
        docs/354-r1-public-state-projection-doc353-readback-marker-drift-failure-boundary.md
        docs/milestones.md
```

local qualification、original Public CI、protected merge 与 new exact-main gates 均成立：

```text
original Public CI = 42003156856 / attempt 1 / 11 of 11 SUCCESS
protected merge = 95add9053c2984c0efe0cb87d1a4b64812215683
merge tree = 3619ceeba79145ebfe3af230e4ba22c89798c306
parents = 6af0dac952ec2bd3e015bc827b2b709908282036
          a5dd28fa8b24b5517a09e5be9733e7e479658746
exact-main Public CI = 42007684666 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42007684466 / attempt 1 / 1 of 1 SUCCESS
```

original、protected-merge 与 exact-main dual-gate qualification SHA-256 分别为：

```text
ef8d0301a65d813db1038c7faa81cc8f8121075cccc0abd63b62ab15c35a08d3
8175e6d0291a6279635fc68e14eef83d2f7ad0541445fe9c13e178ecac8c508a
eebc5ea29f5019a63033efed0a585316afba2dd8d4261f57b2d50077944f34af
```

exact-main Public CI monitor 的 GitHub API EOF 与 fresh worktree 首次 missing-local-ref 均按 setup error 原 identity 保留；
后继成功没有覆盖它们。上述门只证明 doc354 exact bytes 的声明门通过，不自动使 doc354 成为 qualified history。

## 2. fresh installed-product observation 与 adapter freeze

fresh detached worktree 精确绑定 `main@95add905…`，短 output root 为 `C:\\vt354e`。显式 Python 3.13.13 venv、公开
Core 0.13.0 与 GitHub Evidence 0.1.0 wheel、Playwright 1.62.0、public bytes、pre-plan、pre-formal validation 与
path budget 141/240 均成立。pre-observation adapter freeze SHA-256 为：

```text
b572e3f49445e05e3762d9a9ec3d5173e34974bad02c213e5199c8342f6a272e
```

setup inventory 的 PowerShell empty-pipe parser error 与首次假定不存在的 `D:\\python-3.13.13\\python.exe` 路径错误均以
`NON_QUALIFYING / NONE` 保留；实际 Python 3.13.13 来自 `D:\\Miniconda\\python.exe`。它们不改变产品或资格语义。

匿名 rate diagnostic 保留三个独立 identity：

1. #1：HTTP 200，core `remaining=0`，reset `1793875977`；
2. #2：reset 后仍为 `remaining=0`，新的 reset `1793876878`；
3. #3：HTTP 200，core `remaining=2`，reset `1793884245`。

API preflight #1 随后对 exact commit 返回 HTTP 200，并观察到另一匿名出口视图 `remaining=28`。这些都是 setup diagnostic，
不是正式 product observation，也不能保证紧接着的 paired formal 使用同一匿名出口额度。

## 3. 唯一 README formal 的真实 non-success

README diagnostic identity `r1-psp-doc353-readback-fb-diagnostic-readme-1-95add90` 为
`DIAGNOSTIC_ONLY_NON_QUALIFYING / RENDER COMPLETE / HTTP 200`。

唯一 formal identity 为：

```text
r1-psp-doc353-readback-fb-formal-readme-1-95add90
```

该 formal 使用同一个 `collection_session_id` 采集 paired API 与 Render。Render 结果为：

```text
coverage = COMPLETE
top-level HTTP = 200
requested URL = final URL = exact 95add905 README
sample digest = 665114ab4f05d1e68d8001157e7cb76d0fa316b6eedc285cf7f93364c338e0ff
three samples stable = true
literal = doc353 的 README 正式读回失败已按原身份保留
source occurrences = 1
rendered-text occurrences = 1
active streams = 0
cleanup errors = 0
```

API 的第一个 `repository` probe 则返回：

```text
HTTP status = 403
outcome = COLLECTION_BUDGET_EXHAUSTED
rate limit = limit 60 / used 60 / remaining 0
reset = 1793884245
coverage = ERROR
```

因此 Core 的 `api-coverage-complete` 证明义务没有得到 Evidence，Verdict 没有创建。Render COMPLETE、marker 一次或此前 preflight
HTTP 200 均不能和 API ERROR 拼成 PASS；Collector 按合同 fail closed。

## 4. 失败归层与归因上限

当前证据只允许：

```text
README formal API observation = ERROR / HTTP 403 / COLLECTION_BUDGET_EXHAUSTED
README formal Render observation = COMPLETE / HTTP 200 / MARKER ONCE / CLEANUP COMPLETE
README formal readback qualification = ERROR / NOT_QUALIFIED
Core verdict = NOT_CREATED
Collector fail-closed behavior = CONFORMING
anonymous API rate-budget exhaustion = ESTABLISHED
candidate semantic regression = NOT_ESTABLISHED
Collector regression = NOT_ESTABLISHED
shared-egress rate allocation or external usage cause = UNKNOWN
PR #405 marker-drift failure backfilled = false
```

rate diagnostic、preflight 与 formal 观察到不同 remaining 值，最多说明匿名出口/缓存/共享使用可能不同；不能据此任选代理、GitHub、
本机、并发调用或外部用户作为单一根因。也不能用认证 token 替代合同要求的 fresh anonymous installed-product observation。

failure-boundary、92-artifact failed closeout 与 finite integrity SHA-256 为：

```text
5f7abf1afbc8cef0430c19a9c2598ce54f25568d818b1789d95a41b3d803c994
049fc88c8aa3f4c379b3e2697d9ddc0a7b32f285acfd9661968d53bcaa294705
cbefd722d816d0d736cb575dd12469583267bfcf13fe610be595acbf62b4e29d
```

## 5. 未运行目标与禁止拼接

README formal non-success 后，资格链停止：

```text
doc354 diagnostic/formal = NOT_RUN
AGENTS raw formal = NOT_RUN
milestones raw formal = NOT_RUN
independent success reconciliation = NOT_RUN
```

后继不得重跑该 README formal、等待到额度恢复后 retry until PASS、继续其他目标再拼接，或借用 #403/#405/其他 exact world 的
readback。新的独立 observation 可以形成新事实，但不能改变本 identity 的 ERROR。

## 6. retained history 不被回填

- PR #402/doc350 仍是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #403/doc351 仍是 `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
- PR #404/doc352 仍是 `CANCELLED / CLOSED / UNMERGED / NOT_QUALIFIED`，duration variance 仍为 `UNKNOWN`；
- PR #405/doc353 仍是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #406/doc354 现在也是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- projection 0.2、private implementation 与 global composition authority 均没有因此冻结或恢复；manifest、Evidence、persistence、
  public Review 与 R2–R6 仍未授权。

## 7. 本审计的最小职责与公开观察面

tracked scope 只能是：

```text
README.md
AGENTS.md
docs/355-r1-public-state-projection-doc354-readback-anonymous-rate-exhaustion-failure-boundary.md
docs/milestones.md
```

本文自己的合入后 observation 必须机械区分：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；sealed literal 是 reader-visible 的 `doc354 的 README 正式读回匿名 API 额度耗尽已按原身份保留` |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整 bytes 与 digest |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation；raw bytes 不冒充 Render COMPLETE |

independent reconciliation 必须核对 base/head/tree、四文件 scope、#405/#406 retained failures、#406 original/protected/exact-main gates、
全部 setup/diagnostic/formal non-success、failure-boundary/failed closeout/finite integrity、doc351 qualified history、primary audit continuity
与四个 fresh observations。

## 8. 本审计自己的资格链

final bytes 至少通过 UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、`git diff --check`、
global/local hygiene、primary audit continuity，以及 Python 3.10.6 / 3.13.13 × normal/`-O` focused unchanged-runtime witness。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 7
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_ANONYMOUS_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一 non-success 都保留原身份并停止。全部门闭合后本文也只成为 qualified history；它不使 doc354、doc353、doc350、projection 0.2
或 private implementation qualified/frozen。

## 9. 当前状态与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_PR_404_CANCELLED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_RECOVERY_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC353_READBACK_MARKER_DRIFT_FAILURE_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_ANONYMOUS_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文形成新事实后必须返回 CONTROL LOOP。若没有新反例，下一最小 seam 才是从新的 exact main 建立独立、versioned doc354
readback recovery publication；不得复用 #406 formal identity、静默修改旧 publication、以认证替代匿名观察、扩张 35 分钟
containment budget、冻结 projection/private implementation 或启动 manifest/Evidence/persistence/public Review/R2–R6。
