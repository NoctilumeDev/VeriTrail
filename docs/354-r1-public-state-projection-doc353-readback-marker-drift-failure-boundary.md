# R1 public project-state projection doc353 readback marker-drift failure boundary

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC353_READBACK_MARKER_DRIFT_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@6af0dac952ec2bd3e015bc827b2b709908282036`，tree
> `1fe75d2b3431b04167fe87262a7bc27c67b3a2d3`。
>
> 受审失败：PR #405 合入后的 README fresh anonymous formal marker drift。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只冻结失败身份、未运行目标、fail-closed
> 归层与后继 proof-target 责任；不修改 workflow、runtime、tests、Schema、Provider、Collector、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict、doc353、doc350、`docs/project-state.md` 或任何 frozen contract。

## 1. CONTROL LOOP 输入：#404 不被回填，#405 形成新的独立 world

[文档353](353-r1-public-state-projection-doc350-recovery-original-gate-cancellation-boundary.md)审计 PR #404 original
Public CI `41980701750` attempt 1 的 Python 3.10 required job cancellation。#404 继续是
`CANCELLED / CLOSED / UNMERGED / NOT_QUALIFIED`；`RUNNER_JOB_TIMEOUT_BUDGET_EXHAUSTED` 已建立，底层 duration
variance 原因保持 `UNKNOWN`，没有 rerun 或 later-PASS 回填。

doc353 自己由 PR #405 以新的精确坐标进入资格链：

```text
base = da6a6b3e692bf2486ca428dd5ed9c2068918e982
head = 400d469b821d69816a17ccd7c060046ae66ccb45
candidate tree = 1fe75d2b3431b04167fe87262a7bc27c67b3a2d3
commit count = 1
scope = README.md
        AGENTS.md
        docs/353-r1-public-state-projection-doc350-recovery-original-gate-cancellation-boundary.md
        docs/milestones.md
```

local qualification、original Public CI、protected merge 与 new exact-main gates 均成立：

```text
original Public CI = 41987752615 / attempt 1 / 11 of 11 SUCCESS
protected merge = 6af0dac952ec2bd3e015bc827b2b709908282036
merge tree = 1fe75d2b3431b04167fe87262a7bc27c67b3a2d3
parents = da6a6b3e692bf2486ca428dd5ed9c2068918e982
          400d469b821d69816a17ccd7c060046ae66ccb45
exact-main Public CI = 41991308866 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 41991308859 / attempt 1 / 1 of 1 SUCCESS
```

original、protected-merge 与 exact-main dual-gate qualification SHA-256 分别为：

```text
c0b3d13f3c4ded2035e3de6c04f987e519930adb880a8868b08dd6d4a8271021
3b7592fefb6faf91b960cdf35e923d0caaaa3a4fc0c9ffff1997f20ec0270184
5babb5739e7537e7f0e20dcbbfd53b0719fe4a382af760d2d9cfa19eac894db4
```

该新 world 在没有修改 35 分钟 workflow budget、runtime、tests 或 oracle 的条件下使 Python 3.10 与 Python 3.13
required lanes 都完成。它证明恢复不要求先扩张 containment budget；它不解释或覆盖 #404 的 `CANCELLED / UNKNOWN`。
上述门也不自动使 doc353 成为 qualified history。

## 2. fresh installed-product observation 与保留的 non-success

fresh detached worktree 精确绑定 `main@6af0dac…`，短 output root 为 `C:\\vt353e`。显式 Python 3.13.13 venv、公开
Core 0.13.0 与 GitHub Evidence 0.1.0 安装、public bytes、pre-plan 与 pre-formal validation 均成立；最终 active adapter
freeze SHA-256 为：

```text
095fe39b04b0d6851b87ce17af89ee71842cfbc5c89ec8a1b496d1b6c13eb223
```

所有 setup 与 diagnostic 身份均原样保留，包括 missing local ref、PowerShell parser/native glob、missing public-wheel
directory、source-sequence missing gate files、configure `kind` KeyError、65-character plan ID、anonymous rate exhaustion、
HTTP 504 与 navigation timeout。它们没有 qualification authority，也没有被后继观察删除或改名。

README formal 保留三个独立 non-success identity：

1. `r1-psp353-formal-readme-1-6af0dac`：API anonymous 403 `COLLECTION_BUDGET_EXHAUSTED`，Render
   `PARTIAL / HTTP 504`，Verdict 未创建；
2. `r1-psp353-formal-readme-2-6af0dac`：API `COMPLETE`，Render navigation timeout / response-body
   observation error，cleanup complete，Verdict 未创建；
3. `r1-psp353-formal-readme-3-6af0dac`：API 与 Render 都 `COMPLETE / HTTP 200`，三次 sample 稳定，但 sealed
   source marker 一次、rendered-text marker 零次，因此在 Verdict 形成前 fail closed。

第三次 formal 的 content-window sample digest 三次均为：

```text
27557fc5014841ef83c2c9b85679a182c34507e90040b6dca0725f3d5a8e6876
```

formal 使用的 literal 为 `doc350 recovery publication 0.1`。exact README source 中该 literal 出现一次，fresh public
rendered-text observation 中为零。产品因此以 `RuntimeError: Render Evidence marker drifted` 停止，没有创建 Core
Verdict 或 PASS。

## 3. 失败归层与归因上限

当前证据只允许：

```text
README public observation on formal #3 = API COMPLETE / RENDER COMPLETE / HTTP 200 / SAMPLES STABLE
sealed source marker occurrence = 1
rendered-text marker occurrence = 0
README formal readback qualification = ERROR / NOT_QUALIFIED
Core verdict = NOT_CREATED
Collector fail-closed behavior = CONFORMING
proof-target public observability counterexample = ESTABLISHED
candidate semantic regression = NOT_ESTABLISHED
Collector regression = NOT_ESTABLISHED
GitHub render / visibility mechanism root cause = UNKNOWN
```

不能把 diagnostic `COMPLETE`、formal 的 API/Render `COMPLETE` 或 source occurrence 拼成 PASS。也不能从 marker 零次任选
GitHub 折叠、DOM、viewport、缓存、链接文本、采集窗口或 Collector 作为单一根因。后继可在新的 versioned publication 中把
proof target 放入 reader-visible README surface，并从新的 exact world 重新受审；本 formal identity 永久保持 ERROR。

failure-boundary、140-artifact failed closeout 与 finite integrity SHA-256 为：

```text
e393470939acc052a94f3ac44d89694b8a8012b0389e207912ba3658663d4c61
4165a90d119830e54aa91bcb6ab30306ac260b6e9bcf4a0a2633c0834e775737
aac1c1afe19b384857b7fabcc0966a52d7fbceb2085f6613247e798d1611f72a
```

## 4. 未运行目标与禁止拼接

README formal #3 non-success 后，资格链停止：

```text
doc353 formal = NOT_RUN
AGENTS raw formal = NOT_RUN
milestones raw formal = NOT_RUN
independent success reconciliation = NOT_RUN
```

doc353 diagnostic `COMPLETE / HTTP 200` 仍只是 diagnostic。未运行目标不能借用 #403、#404、#405 diagnostic 或其他 exact
world；#405 的 original/exact-main 绿灯也不能覆盖 fresh formal failure。

## 5. retained history 不被回填

- PR #402/doc350 仍是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #403/doc351 仍是 `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`，其本地文件系统根因仍为 `UNKNOWN`；
- PR #404/doc352 仍是 `CANCELLED / CLOSED / UNMERGED / NOT_QUALIFIED`，duration variance 仍为 `UNKNOWN`；
- PR #405/doc353 现在是 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- projection 0.2、private implementation、global composition authority 均没有因此冻结或恢复；manifest、Evidence、persistence、
  public Review 与 R2–R6 仍未授权。

## 6. 禁止的伪恢复

```text
重跑 #405 README formal 或 retry until PASS
继续 doc353/AGENTS/milestones 后与 README 拼接
把 diagnostic COMPLETE、HTTP 200 或 source marker occurrence 当作 formal PASS
弱化 marker oracle、删除 rendered-text check 或把零次改名为成功
用 #403 或其他 world 的 readback 继承给 #405
把 #405 exact-main Python 3.10 PASS 回填为 #404 PASS 或解释其 UNKNOWN
因 #404 单次超时直接扩张 35 分钟 workflow budget
猜测 GitHub render / visibility 的单一根因
从本审计直接恢复 doc353/doc350、冻结 projection 或启动后续 runtime seam
```

## 7. 本审计的最小职责与公开观察面

tracked scope 只能是：

```text
README.md
AGENTS.md
docs/354-r1-public-state-projection-doc353-readback-marker-drift-failure-boundary.md
docs/milestones.md
```

README 的新增 marker 位于 reader-visible 首页，不改变 `>=1` rendered-text oracle。本文自己的合入后 observation 必须机械区分：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；sealed literal 是首页可见的 `doc353 的 README 正式读回失败已按原身份保留` |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整 bytes 与 digest |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation；不把 raw bytes 冒充 Render COMPLETE |

independent reconciliation 必须核对 base/head/tree、四文件 scope、#404 retained cancellation、#405 original/protected/exact-main gates、
全部 setup/diagnostic/formal non-success、failure-boundary/failed closeout/finite integrity、doc351 qualified history、primary audit continuity
与四个 fresh observations。

## 8. 本审计自己的资格链

final bytes 至少通过 UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、
`git diff --check`、global/local hygiene、primary audit continuity，以及 Python 3.10.6 / 3.13.13 × normal/`-O` focused
unchanged-runtime witness。测试只证明本 docs-only candidate 没有修改 runtime，不解释 #404 或 #405 的底层 UNKNOWN。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 7
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC353_READBACK_MARKER_DRIFT_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一 non-success 都保留原身份并停止。全部门闭合后本文也只成为 qualified history；它不使 doc353、doc350、projection 0.2
或 private implementation qualified/frozen。

## 9. 当前状态与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_PR_404_CANCELLED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_RECOVERY_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC353_READBACK_MARKER_DRIFT_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文形成新事实后必须返回 CONTROL LOOP。若没有新反例，下一最小 seam 才是从新的 exact main 建立独立、versioned doc350
readback recovery publication，并把 public proof target 放在 reader-visible surface；不得复用 #405 formal identity、静默修改旧
publication、扩张 35 分钟 containment budget、冻结 projection/private implementation 或启动 manifest/Evidence/persistence/public
Review/R2–R6。
