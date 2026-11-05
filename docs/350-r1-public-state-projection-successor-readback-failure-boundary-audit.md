# R1 public project-state projection successor readback failure-boundary audit

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@f553822f8ce54793103efd97c2e1ac8da487349e`，tree
> `116dc7dfa3ce98424a4fa89cf98209329e2c83ff`。
>
> 受审对象：PR #401 合入后的 README formal readback marker drift。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只冻结失败身份、资格影响、Collector
> fail-closed 行为与后继 versioned recovery 责任；不修改 runtime、tests、workflow、Schema、Provider、Collector、P2
> oracle、Fact/Relation/Coverage semantics、Verdict、doc349 或 `docs/project-state.md`。

## 1. CONTROL LOOP 输入：successor 0.2 已合入，但 readback 没有资格化

[文档349](349-r1-public-project-state-projection-recovery-successor-contract.md)与
[有界当前状态投影](project-state.md)由 PR #401 以精确坐标进入资格链：

```text
base = 34de9427d64ba8a3c77ac38eefe146fa8d2e2d77
head = fc20dfb9474924d37787d9022ebfefcac6894743
candidate tree = 116dc7dfa3ce98424a4fa89cf98209329e2c83ff
commit count = 1
scope = README.md
        AGENTS.md
        docs/349-r1-public-project-state-projection-recovery-successor-contract.md
        docs/project-state.md
```

local qualification、original Public CI `41932436048` attempt 1、protected merge 与 new exact-main gates 均成立：

```text
protected merge = f553822f8ce54793103efd97c2e1ac8da487349e
merge tree = 116dc7dfa3ce98424a4fa89cf98209329e2c83ff
parents = 34de9427d64ba8a3c77ac38eefe146fa8d2e2d77
          fc20dfb9474924d37787d9022ebfefcac6894743
exact-main Public CI = 41937014486 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 41937014373 / attempt 1 / 1 of 1 SUCCESS
```

这些门只证明 exact candidate/merge world 通过其声明的代码与浏览器门，不自动使 doc349 或 projection 0.2
资格化、冻结或生效。

## 2. fresh installed-product failure identity

fresh detached worktree 精确绑定 `main@f553822…`。pre-formal validation 与 57-file adapter freeze 已成立；adapter freeze
SHA-256 为：

```text
6d0b51ebe1e324ba97dc940a1888be0cfa90783a2b5e0bd2c68d9ce86b6265a9
```

匿名 rate diagnostic #1–#5 的 exhaustion/zero-capacity 结果与 reset 身份均保留；diagnostic #6 观察到可用窗口，API
preflight #1 成功。README fresh diagnostic 随后以
`r1-psp-recovery-v2-diagnostic-readme-1-f553822` 结束：

```text
classification = DIAGNOSTIC_ONLY_NON_QUALIFYING
render coverage = COMPLETE
top-level HTTP status = 200
```

唯一 README formal attempt 的身份为：

```text
identity = r1-psp-recovery-v2-formal-readme-1-f553822
collection_session_id = github-paired-20cfeb5a8cdf4ca2ba879e9c2f6a982f
API coverage = COMPLETE
Render coverage = COMPLETE
top-level HTTP status = 200
literal marker = versioned recovery successor 0.2
rendered text occurrences = 0
classification = FORMAL_READBACK_ERROR
Core verdict = NONE
```

formal 的三次 content-window sample digest 均为
`625c594915c3c084eaada4d0ede8ad2b301df885bdb3ba22f51675acf50926f8`。产品在 exact README source 中仍能机械定位
该 literal 一次（source line 409），但 fresh public rendered-text observation 中为零，因此 acceptance 在创建 Verdict 前以
`RuntimeError: Render Evidence marker drifted` fail closed。

failure-boundary、94-artifact failed-readback closeout 与 finite integrity SHA-256 为：

```text
36f6dca90c5c5a75aece92e3adc97b9a1d24c4e1c0988c2f91fe995e74fcda10
07d06a30890e6590dc6c759e0163ed2e8d84f4dc8cce7ebaac471b4eeeb2826f
6a44688d312185c659c7b6e09ada0f6e597335bf34f6a135ed99ce5ebd996543
```

## 3. 失败归层

这次 non-success 不是 API 缺失、Render coverage PARTIAL、HTTP 错误、Core FAIL 或 cleanup failure。产品完整观察后发现
封存的 literal marker 在 rendered text 中不存在，并在 Verdict 形成前停止。当前证据只允许：

```text
README formal readback failure = TRUE
candidate readback qualification = FAILED / NOT_QUALIFIED
Collector fail-closed behavior = CONFORMING
candidate public readback proof-target observability counterexample = ESTABLISHED
Collector regression = NOT_ESTABLISHED
private runtime semantic regression = NOT_ESTABLISHED
GitHub render / visibility mechanism root cause = UNKNOWN
```

README source 中存在 literal 不能替代 rendered-text observation；diagnostic coverage COMPLETE 也不证明 marker 存在。反过来，
rendered text 中 marker 为零也不能被猜测成单一的 GitHub 折叠、DOM、网络、viewport、链接文本、缓存或 Collector 根因。
后继可以改变最小 proof-target publication bytes，让新的 exact world 重新受审；不能给本 formal identity 补写 PASS。

## 4. 未运行目标与禁止拼接

README formal non-success 后，资格链按冻结停止线停止：

```text
project_state diagnostic/formal = NOT_RUN
doc349 diagnostic/formal = NOT_RUN
AGENTS raw formal = NOT_RUN
milestones raw formal = NOT_RUN
independent success reconciliation = NOT_RUN
```

未运行目标不能借用 #400 或更早 readback；README diagnostic COMPLETE 不能与任何旧 formal PASS 拼接成 #401 资格。#401 的
original/exact-main 绿灯继续保留，但不能覆盖 formal failure。

## 5. retained history 不被回填

本失败新增在既有历史之后，不改变这些事实：

- PR #398 仍是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #399/doc347 仍是 failed、closed、unmerged、not qualified，runner/subprocess stall 底层原因仍为 `UNKNOWN`；
- doc348 仍是 `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
- doc349 与 projection 0.2 现在是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- private implementation 仍未冻结，global composition authority 未恢复；manifest、Evidence、persistence、public Review 与
  R2–R6 仍未授权。

## 6. 禁止的伪恢复

以下动作都不能产生 successor 0.2 资格：

```text
重跑 README formal #1 或 retry until PASS
继续运行 project_state/doc349/AGENTS/milestones 后拼接结果
把 diagnostic COMPLETE 当作 formal PASS
用 exact source literal occurrence 代替 public rendered-text occurrence
弱化 >=1 marker oracle、删掉 marker rule 或把零次改名为 PASS
把 #400 或其他 exact world 的 readback 继承给 #401
静默追写 doc349/project-state 0.2 并保留同一版本身份
猜测 GitHub render/visibility 的单一根因
从本审计直接冻结 projection、private implementation 或启动后续 runtime seam
```

## 7. 本审计的最小职责与公开观察面

本候选只允许：

```text
README.md
AGENTS.md
docs/350-r1-public-state-projection-successor-readback-failure-boundary-audit.md
docs/milestones.md
```

它不修改 doc349、`docs/project-state.md`、runtime、tests、workflows 或 frozen contracts。由于完整 milestones 已超过 P2
Render 上限，本审计自己的合入后 observation 必须机械区分：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；使用本文在首页可见区新增的 failure-retention marker |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整 bytes 与 digest |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation；不把 raw bytes 冒充 Render COMPLETE |

independent reconciliation 必须核对 base/head/tree、四文件 scope、#401 gates、formal failure、failure-boundary/failed closeout/finite
integrity、doc348 qualified history、#398/#399 retained identities、primary audit continuity 与四个 fresh observations。

## 8. 本审计自己的资格链

final bytes 至少通过 UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、
`git diff --check`、global/local hygiene、primary audit continuity，以及 Python 3.10.6 / 3.13.13 × normal/`-O` 下
focused unchanged-runtime witness。测试只证明本 docs-only candidate 没有修改 runtime，不回填 #401。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 7
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一 non-success 都保留原身份并停止。全部门闭合后本文也只成为 qualified history；它不使 #401 qualified 或 frozen。

## 9. 当前状态与后继停止线

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_MERGED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_EXACT_MAIN_DUAL_GATES_PASS
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_PR_399_FAILED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文形成新事实后必须返回 CONTROL LOOP。若没有新反例，下一最小 seam 才是从新的 exact main 建立独立、versioned
docs-only projection readback recovery candidate，重新绑定可公开观察的 proof target；不得复用本 formal identity、静默修改
0.2、冻结 private implementation 或启动 manifest/Evidence/persistence/public Review/R2–R6。
