# R1 same-attempt Evidence continuity freeze recovery formal readback failure boundary

日期：2026-11-11

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_EXACT_MAIN_FORMAL_READBACK_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@2c80f09c19d6196e6d5f745996e1d22e4a8d72c5`，tree
> `a5336a3cd1d7be7f694b34200ca3a072455ae4f7`。
>
> 影响：`L0_DOCUMENTATION / EXACT_MAIN_READBACK_FAILURE_BOUNDARY_AUDIT_ONLY`。本文只保存PR #459合入后doc400唯一
> formal installed-product readback的HTTP 503 / `PARTIAL`失败、已经成立的其他观察、未知归因与最小恢复边界；不重跑失败identity，
> 不把三个PASS拼成完整资格，不修改Collector、workflow、oracle、合同语义或runtime，也不授权R2–R6。

## 1. CONTROL LOOP 与精确候选坐标

PR #458已经使doc399成为`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。后继PR #459只从新exact main重建doc397的
合同冻结恢复发布，绑定：

```text
base                 = d06c15082abf00163feeccecd9c9ae7afcd275fd
head                 = 55909103f4a6af7d3d191fe5dddd32893e1e81a2
tree                 = a5336a3cd1d7be7f694b34200ca3a072455ae4f7
scope                = 1 commit / 4 docs files
original Public CI   = 42821799379 / attempt 1 / SUCCESS / 11 of 11
protected merge      = 2c80f09c19d6196e6d5f745996e1d22e4a8d72c5
exact-main Public CI = 42828992788 / attempt 1 / SUCCESS / 11 of 11
Browser Smoke        = 42828992853 / attempt 1 / SUCCESS / 1 of 1
```

original qualification、protected merge与exact-main gate seal SHA-256分别为：

```text
e2f2e1835bc9953bbf0cd9014060c726936310eefbeddab7fc8c33d8234506d3
6262588b2797b20aa96484efb23a3c36a35d34c84894154add301d7cbd31b8f9
69eb468657ddfdd95061c9c4fd4151046da6725cfedd4621d11a5ed14b6919a1
```

这些事实证明PR #459候选、protected merge和new exact-main双门成立；它们不替代合入后的fresh installed-product readback。

## 2. Fresh readback 世界与保留的diagnostic事实

fresh detached worktree只认`2c80f09… / tree=a5336a3…`。公共Core `0.13.0`、GitHub Evidence `0.1.0`、
Python 3.13.13与bundled Chromium在隔离venv中安装；产品调用清除了`NO_PROXY`、`PYTHONPATH`、`PYTHONHOME`和全部GitHub token变量，
仅按命令使用`http://127.0.0.1:7897`。

初始pre-formal validation与adapter freeze SHA-256为：

```text
11460c2f0898d3fb16632979553bd9168244159c66f4a81d09c7bffe0fc47523
2818b1fea5114876f45bc5a243032e0fce872062779a99d40b1f7230badc4cdb
```

README diagnostic #1首先得到公开Render HTTP 503、`PARTIAL`、content scope count 0与missing content window；Collector本身没有记录
collection error或cleanup error，active streams为0。两个proof wrapper又因未把`content/window = null`归一化为映射而抛出
`AttributeError`。这两个层次均永久保留：底层Render失败不是wrapper制造，wrapper错误也不能冒充产品失败。

只修正proof facility的null handling以后，新的pre-formal validation与adapter freeze SHA-256为：

```text
5153b83ed1362d7bab178a12ca9ced5f24592b12ed0da1b6d0b59543a6634d0c
c58d354814479e198c0fb58f9402ecd226e522cf5007e2d3159fc322e3d1b1c9
```

README diagnostic #2以及doc397、doc399、doc400各自fresh diagnostic均为`COMPLETE / HTTP 200 / marker=1`。这些diagnostic只确认
formal前观察设施可用，`qualification effect = NONE`；它们不能替代后继formal identity，也不覆盖README diagnostic #1。

## 3. 唯一formal结果与首败

正式installed-product readback依次形成：

| Target | Formal identity | API | Render | HTTP | Marker | Core | Result |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| README | `formal-readme-1-2c80f09` | `COMPLETE` | `COMPLETE` | 200 | 1 | `PASS` | `FORMAL_READBACK_PASS` |
| doc397 | `formal-doc397-1-2c80f09` | `COMPLETE` | `COMPLETE` | 200 | 1 | `PASS` | `FORMAL_READBACK_PASS` |
| doc399 | `formal-doc399-1-2c80f09` | `COMPLETE` | `COMPLETE` | 200 | 1 | `PASS` | `FORMAL_READBACK_PASS` |
| doc400 | `formal-doc400-1-2c80f09` | `COMPLETE` | `PARTIAL` | 503 | unknown | none | `FORMAL_READBACK_ERROR` |

doc400失败观察的精确事实是：

```text
top-level status                   = 503
public Render coverage             = PARTIAL
content scope observed_count       = 0
content window                     = null
coverage reasons                   = CONTENT_SCOPE_NOT_UNIQUE
                                     CONTENT_WINDOW_MISSING
                                     FACT_CONFLICTS_RETAINED
collector errors                   = []
cleanup errors                     = []
active response streams            = 0
delivered response body bytes      = 56635
API side                           = COMPLETE
Core Verdict                       = none
underlying cause                   = UNKNOWN
qualification effect               = NONE
```

formal failure classification seal SHA-256为：

```text
classification = FORMAL_READBACK_RENDER_HTTP_503_PARTIAL_CONTENT_SCOPE_MISSING
6f2bd5f0b1bbd7f6e14a670fe3f3935d6a0e86d41a5713884583167bd3db9f8f
```

系统在Render不完整时拒绝构造Core PASS，属于正确的fail-closed行为。当前证据不建立candidate regression、Subject failure、
product classification failure或oracle defect；它也不能把HTTP 503的下层原因从`UNKNOWN`改写为GitHub、代理、网络、浏览器或仓库中的
任意单一原因。

失败出现后立即停止，AGENTS与milestones的formal raw-byte observation没有启动。未执行不能写成PASS，也不能为了补齐清单继续拼接另一个
world。

## 4. 三个PASS不能拼成完整资格

本publication冻结门要求README、doc397、doc399、doc400四个目标各有自己的唯一formal PASS，并要求raw observations、独立
reconciliation与finite closeout全部成立。当前世界只有前三个formal PASS；doc400为明确ERROR，因此：

```text
3 formal PASS + 1 formal ERROR != 4 formal PASS
diagnostic PASS                 != formal PASS
exact-main green               != installed-product qualification
cleanup complete               != target content observed
later independent PASS         != overwrite this ERROR
```

doc400已经随PR #459进入main，但状态仍是`MERGED / NOT_QUALIFIED / NOT_FROZEN`。doc397继续只是
`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`，continuity contract没有生效，private implementation继续
`NOT_STARTED / NOT_AUTHORIZED`。

## 5. 反例处理与适用前提

本失败继续采用：

> 理论遇到反例，先检查前提、适用域与观察是否成立，而不是不断增加例外。

机械含义是：

1. 不把相邻目标的PASS增加为doc400的替代证据；
2. 不因diagnostic doc400曾经HTTP 200就宣布formal目标可观察；不同session不是同一观察；
3. 不把HTTP 503列入“允许忽略的外部波动”，也不降低`COMPLETE / marker=1 / Core PASS` oracle；
4. 不重跑、retry-until-PASS或复用formal identity #1；
5. 不从cleanup完整推导页面内容完整；cleanup只证明生命周期收口，不证明目标正文已出现；
6. 不把未知下层原因包装成已知根因；
7. 不修改runtime、Collector、timeout、重试策略或workflow来保护publication目标。

## 6. 最小恢复边界

本反例只重开：

```text
PR459_EXACT_MAIN_FORMAL_READBACK_QUALIFICATION_BOUNDARY_ONLY
```

最小恢复顺序是：

1. 本docs-only failure-boundary audit以自己的final bytes完成local qualification、original PR gate、protected merge、new exact-main
   gates、fresh installed-product readback、raw-byte observation、independent reconciliation与finite closeout；
2. 返回fresh CONTROL LOOP，从新的exact main确认doc397合同字节仍有效、doc400失败仍保留、恢复publication仍是最小合法seam；
3. 若无新反例，创建新的docs-only recovery publication；不得修改doc400历史、不得复用本次formal PASS或ERROR的authority；
4. 新publication必须获得自己的exact base/head/tree、original creation run、protected merge、new exact-main双门与fresh readback；
5. 后继PASS只证明新world成立，不解释、覆盖或回填本次HTTP 503；
6. runtime、Schema、manifest、persistence、public Review与R2–R6继续禁止。

## 7. 本候选范围与停止线

本候选只允许：

```text
README.md
AGENTS.md
docs/401-r1-same-attempt-evidence-continuity-freeze-recovery-formal-readback-failure-boundary.md
docs/milestones.md
```

doc397、doc399、doc400、失败PR中的doc398、runtime、tests、fixtures、workflow、Schema、Provider、Collector、oracle和全部frozen
semantic bytes保持base不变。完整资格链闭合后，本文最多成为`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；它不冻结contract，
不授权private implementation，也不自动创建后继publication。

## 8. 当前状态上限

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
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FREEZE_RECOVERY_PUBLICATION_EXACT_MAIN_FORMAL_READBACK_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`local_not_global = true`与`post_r1_global_check_required = true`继续成立。它们要求R1完整闭合后再独立检查全局前提、authority、
qualification与用户能力是否可组合，但不扩张本failure-boundary audit的局部授权。
