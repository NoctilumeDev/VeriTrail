# R1 public project-state projection doc350 recovery original gate cancellation boundary

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_RECOVERY_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@da6a6b3e692bf2486ca428dd5ed9c2068918e982`，tree
> `102b1e3e5f6844b278edee3caa83d10dc6dc8179`。
>
> 受审失败：PR #404 original Public CI `41980701750` attempt 1 的required Python 3.10 job cancellation。
>
> 影响：`L0_DOCUMENTATION + L3_FAILURE_BOUNDARY_AUDIT`。本文不修改workflow、runtime、tests、Schema、Provider、Collector、
> P2 oracle、Core evaluator、Fact/Relation/Coverage semantics、Verdict或frozen contract。

## 1. 上游 qualified boundary 与失败candidate

[文档351](351-r1-public-state-projection-audit-readback-bundle-persistence-failure-boundary.md)由PR #403以exact
`base=4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea / head=d6ee533e9751380d4e981204c1d5c6e95fc26762 /
tree=102b1e3e5f6844b278edee3caa83d10dc6dc8179`合入本构造坐标。original Public CI `41968023423`、exact-main
Public CI `41971091826`与Browser Smoke `41971091790`均为attempt 1 SUCCESS。fresh README/doc351 formal与
AGENTS/milestones exact-commit raw-byte observation各有唯一PASS；independent reconciliation与finite closeout为：

```text
972b9fa8c37c90f6a214128cae28e60d1647662ae1808040c96efa074673d24f
45f26afccb77ea779bf0ed47b8780779129c22f7e17af27f802b518b8b00452f
0de80aa38eb2f223591e5d37f1214f33d3ada6d5044848f2433afafd180a8172
1b2243f5ec2a008c3145baed9398dfae69db0a1ecaebaaaf9facbd6653d3b70f
```

doc351因此是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；它不回填#402，也不解释原本地文件系统`UNKNOWN`。

fresh CONTROL LOOP随后建立doc350 recovery publication 0.1。失败candidate exact identity为：

```text
PR    = 404
base  = da6a6b3e692bf2486ca428dd5ed9c2068918e982
head  = 74ede8dff9fb4bf9a79b8749b5ed6f593f161371
tree  = 2ae6b7bd3604397def22c88ac826b0ba236c287f
scope = README / AGENTS / doc352 / milestones
```

local final qualification通过Python 3.10.6 / 3.13.13 × normal/`-O` focused witness、8组global/local hygiene、
767个local links、exact scope、retained-evidence binding、141字符最坏case readback path preflight、remote-main identity与
primary audit continuity。local qualification、pre-PR seal、post-commit seal分别为：

```text
dcafb51a86e196ff73fb48eba752e9f0700f541d3d40c556d56a0127d9999f37
e289f8f9c60ed871d48cf7a45e20266e1e00709a729eac3ec6068de8f224fd2d
39e79b5f25d3a884567eab198ab5616f7701d01e0369d36d9e32c6745b4f2b53
```

这些本地PASS只证明candidate bytes与本地声明门，不替代original PR gate。

## 2. original gate 的真实终态

Public CI `41980701750` attempt 1绑定exact head，终态为`CANCELLED`。required Python 3.10 job `127089895170`
从`2026-11-05T06:29:04Z`运行到`07:04:13Z`，总计2109秒：

1. step 1–31全部SUCCESS，包括Core normal/`-O`、GitHub Evidence、Review Attention normal/`-O`、Starter lane、build与公开资产下载；
2. step 32 `Run E1 release clean-install acceptance`从`07:03:34Z`开始；
3. `entry_layer_e1_acceptance.py`在optimized Authoring Skill acceptance子进程内收到`KeyboardInterrupt`；
4. GitHub随后记录`The operation was canceled`，step 32与job均为`CANCELLED`；
5. Python 3.13、E3 release与Workbench jobs为SUCCESS；四个依赖Python矩阵的downstream jobs为SKIPPED。

exact workflow `.github/workflows/ci.yml` SHA-256为
`f0d5bf5d3eb175a0f7d0b2d248185727ab3aa7bebd35283247881d2f5c18d097`，其Python aggregate job明确声明
`timeout-minutes: 35`。因此本run已建立：

```text
classification = RUNNER_JOB_TIMEOUT_BUDGET_EXHAUSTED
original PR gate = NOT_QUALIFIED
rerun = NOT_REQUESTED
protected merge = NOT_AUTHORIZED / NOT_RUN
exact-main gates = NOT_AUTHORIZED / NOT_RUN
fresh installed-product readback = NOT_AUTHORIZED / NOT_RUN
```

PR #404已关闭且未合并，remote main保持构造坐标。

## 3. 归因上限

candidate只改四个docs文件，workflow、runtime、tests与oracles相对exact base逐字节不变；同run Python 3.13完成，相同exact-main
之前也通过required gates。因此现有证据不建立doc352 semantic regression或产品功能失败。它只证明Python 3.10 aggregate job在本次
runner execution中耗尽既有35分钟外层containment budget。

为什么本次累计duration跨过budget——runner负载、子进程尾延迟、系统调度或其他资源因素——保持`UNKNOWN`。不能把
Python 3.13 PASS拼接为Python 3.10 PASS，也不能把later PASS用于覆盖本`CANCELLED` identity。

original cancellation boundary、794934-byte job log、73-artifact failed closeout与finite integrity为：

```text
a4a973bd5f0d7d03cde38d15467abe0fc56e85886cb4d3d312085d91295bf070
9b6e316956010ee41526e103a86b0ee6b317a60586012e399340aa30d8d3f41f
e583d7b9b3b3fdff5b0a1adf4f41f2f00f06d7e82ae146674d59a9131bba0b16
65651af8e72f1a1bb9bff67a39d66e8a3936d604331f36ce3283ad9a7495a614
```

run API EOF、错误workflow文件名、local `gh run watch` cancellation、两个PowerShell revision-parser setup error与两项local
prequalification finding均保留；它们不改变GitHub original gate结论。

## 4. 本audit的最小资格边界

tracked scope只能是：

```text
README.md
AGENTS.md
docs/353-r1-public-state-projection-doc350-recovery-original-gate-cancellation-boundary.md
docs/milestones.md
```

本audit不得修改35分钟budget，不得重跑#404，不得复用失败head或把doc352合入。final bytes至少通过UTF-8 without BOM、LF/final LF、
links/fences/headings、exact scope、`git diff --check`、global/local hygiene、primary audit continuity及Python 3.10.6 / 3.13.13 ×
normal/`-O` unchanged-runtime focused witness。

合入后README与本文使用fresh anonymous Public Render diagnostic + unique formal；AGENTS/milestones因milestones超过frozen P2 render
上限而使用exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致观察。raw bytes不得冒充Render COMPLETE。
independent reconciliation还必须核对#402 retained error、#403 qualified boundary、#404 exact cancellation、全部setup/non-success identity与
primary audit continuity。

```text
final docs-only bytes / local gates
    -> original PR required gates (new attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh changed-target installed-product observations
    -> independent reconciliation + finite closeout
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

## 5. 状态上限与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_PR_404_CANCELLED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_RECOVERY_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本audit自己的完整资格链闭合后也必须返回CONTROL LOOP。下一步只能独立审计CI containment budget maintenance是否仍是最小合法seam；
不得从本文直接增加timeout、恢复#404、创建doc350 recovery successor、恢复projection 0.2/0.3、或启动runtime/manifest/Evidence/
persistence/public Review/R2–R6。
