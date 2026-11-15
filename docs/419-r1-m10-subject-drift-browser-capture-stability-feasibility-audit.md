# R1 M10 subject-drift / Browser capture stability feasibility audit

日期：2026-11-16

> 候选状态：
> `R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
> 本文自己的完整资格链闭合以前不是qualified history，也不授权修改test/runtime、重建doc415或继续carrier实现。
>
> 构造坐标：`main@36ec79c735640066d30aa5a5911e995ddd09f6d1`；tree
> `f1f424d2a041cde89bd1b346c390a3c40ab5db5f`。
>
> 上游：[carrier precontract audit](414-r1-same-attempt-derivation-evidence-manifest-carrier-successor-precontract-audit.md)、
> closed/unmerged PR #476中的doc415 contract identity、
> [original-gate failure-boundary audit](416-r1-manifest-carrier-successor-original-gate-failure-boundary-audit.md)、
> [readback-target correction](417-r1-manifest-carrier-failure-boundary-audit-readback-target-correction.md)与
> [failure-boundary audit successor](418-r1-manifest-carrier-original-gate-failure-boundary-audit-successor.md)。doc415路径只在closed/unmerged
> head中存在；该链接不表示它已进入main。
>
> 影响：`L3_SYSTEM_DESIGN + L1_TEST_PROOF_FACILITY + L0_DOCUMENTATION / READ_ONLY_FEASIBILITY_AUDIT_ONLY`。
> 本文不改Schema、runtime、tests、workflow、timeout、retry、fixture、Browser Collector、Verdict、Manifest、Provider或public product。

## 1. CONTROL LOOP与qualified起点

PR #479把doc418 candidate
`base=16889cae4c66da5860de0d06ed5125e7b939ff2d / head=b828e6be28b82315abf11355e59dbe5fdfedd981 /
tree=f1f424d2a041cde89bd1b346c390a3c40ab5db5f`精确合入本构造坐标。original Public CI `43753244377`与
exact-main Public CI `43756291479`均attempt 1 15/15 SUCCESS；Browser Smoke `43756291481`为attempt 1 1/1 SUCCESS，没有rerun。

fresh README/doc418各自唯一Render formal为`COMPLETE / PASS`；AGENTS/milestones各自唯一anonymous raw、Contents API与exact Git
byte observation逐字节一致。worktree首次对象未fetch、thread attachment identity cap与一次combined apply-patch source replacement setup
failure全部按原identity保留，qualification effect为`NONE`。independent reconciliation、103-artifact closeout、expected stdout
self-capture mismatch与finite integrity分别为：

```text
e40e1aa7310b1697fa07ca8880dc572bd5f511030eab2a5e1e4084898a12dd94
aa0f050c5bae39595b22ef648ed010733ca44c6764186d920ac8d90770b6891e
c7587c22a4f7f1408ed8f2e5006b459a63a9ed179f104a843903a966d6f3fd87
12b3b5a64ac5ed5522e340c55667f8f31a304137df04e61db705587dc3eb7230
```

因此doc418是`FAILURE_BOUNDARY_AUDITED_SUCCESSOR / QUALIFIED_HISTORY`。这只允许本轮从新exact main审计M10 stability
feasibility；不把doc416写成qualified，不解释PR #476 lower cause，也不授权修复。

## 2. 原始反例继续成立

PR #476的original Public CI `43728958491` attempt 1在Python 3.10 job `132864515924`运行497项full Core regression时，
`test_subject_drift_is_preserved_and_makes_public_verdict_inconclusive`得到：

```text
expected contamination = {BOOTSTRAP_SUBJECT_DRIFT}
observed extra item     = BROWSER_STATUS_CONFLICT
Ran 497 tests in 128.218s
FAILED (failures=1, skipped=1)
```

该run没有rerun，PR closed/unmerged，doc415没有进入main。当前exact main与failed head的下列五个文件逐字节一致：

```text
tests/test_bootstrap_run_cli.py
src/veritrail/bootstrap_public_run.py
src/veritrail/bootstrap_run.py
src/veritrail/browser.py
src/veritrail/verdict.py
```

所以不能把失败归因于doc415正文，也不能用后来的PASS重写失败。original log、gate record与local diagnostic摘要的SHA-256继续是：

```text
d4d685f33dc0b470341803471c8ce3cbcb01440faf9c36f343e46303d1a18469
8d54f5f0c2c2b46fdd48e8d02468df0be435c52d5cbbe673e216e0e64c36ad7c
04780ffb8e9b98dbab1e57c9d9ab29751c90c31af6f212e36115fc89ee9cb5b2
```

## 3. 不把理论反例变成例外表

本轮不以增加例外回答反例，而先检查当前proof target同时假设了什么。精确test把两件事耦合在一次真实集成运行中：

1. watched subject在application ready以后发生确定变更，最终必须得到`BOOTSTRAP_SUBJECT_DRIFT`；
2. 同一次真实Chromium capture必须独立完成，不能产生任何额外contamination。

第一个是subject-drift语义证明；第二个是Browser capture stability证明。它们可以在同一次运行同时成立，但并非同一命题。原失败只证明
第二个前提在该attempt中不成立；它没有证明subject drift处理错误，也没有证明`BROWSER_STATUS_CONFLICT`错误。

因此禁止以下伪修复：

```text
把exact-set assertion改成contains/subset
删除、忽略或重命名BROWSER_STATUS_CONFLICT
因为Verdict已经INCONCLUSIVE就忽略第二个contamination
提高timeout、增加retry或只重跑失败job
用synthetic Browser PASS替代真实Browser稳定性责任
用fresh四格PASS宣布原失败根因已知或已经修复
```

## 4. current source的责任边界

静态审计确认八个机械事实：

1. test仍使用exact set `{BOOTSTRAP_SUBJECT_DRIFT}`；
2. drift fixture只写入`subject/watched/state.txt`；
3. public runner已有private `observed_runner`注入点；
4. observed runner已有private `browser_runner`注入点；
5. controlled Browser path显式存在，不需要修改runtime API；
6. `capture_complete`继续是steps、viewport、collection errors与cleanup的conjunction；
7. `capture_complete=false + COMPLETED`仍由Verdict保守加入`BROWSER_STATUS_CONFLICT`；
8. bootstrap stop reason `SUBJECT_DRIFT`仍独立加入`BOOTSTRAP_SUBJECT_DRIFT`。

static audit SHA-256为：

```text
349cbf03182ce56d372670a055624175132bab9e8026a2580dc2b87a48b10d72
```

所以当前没有证据要求改变runtime或oracle。可行边界首先位于test proof facility与失败留档，不位于产品语义。

## 5. fresh可重复性观察

在本exact main上，Python 3.10.6 / 3.13.13 × normal / `-O`四格各运行一次原real integrated exact test，四格均1/1 PASS。
matrix summary SHA-256为：

```text
8662244d52ebf09555365290d72f53f56e94a79b1f93292deaa3f36c6be9bddf
```

这只支持`stable local reproduction = NOT_OBSERVED`，不支持`original failure = false`或`root cause = fixed`。

同一四格又通过既有private seam向observed runner提供conformant、complete、copy-owned synthetic Browser Evidence，同时保留真实service
lifecycle、readiness、subject mutation、post-teardown snapshot、Bundle与Catalog验证。四格均得到：

```text
execution_status          = COMPLETED
verdict                   = INCONCLUSIVE
contamination             = [BOOTSTRAP_SUBJECT_DRIFT]
browser_capture_complete  = true
browser_collection_errors = []
bootstrap_stop_reason     = SUBJECT_DRIFT
cleanup_complete          = true
```

controlled matrix summary SHA-256为：

```text
2c52ad2cd11199fac3ce7f744b863c9296c3f300a6629dd791c6d8cd3f9dc572
```

该结果只证明责任可机械隔离；synthetic Browser不是原attempt事实、不是public product observation，也不能替代real integrated witness。

## 6. 可行的最小修正方向

本审计只建立feasibility，不选择最终patch。后继若获得独立授权，最小顺序必须是：

1. 保持real integrated test、exact-set assertion、runtime与Verdict oracle不变；
2. 在assertion失败前保留Browser `capture_complete / all_steps_passed / collection_errors / viewport status / step status /
   failed network / cleanup`、bootstrap lifecycle与subject observation；
3. full-suite任何non-success按first-failure identity永久保留，不自动retry；
4. 只有新现场支持某一lower cause时，才重开该最小premise；
5. 若未来确需拆分proof target，controlled subject-drift proof必须与real Browser stability witness同时存在，前者不得替代后者。

这一路径不需要增加timeout、不需要把exact set改成subset，也不需要修改产品runtime。它优先解决当前真正缺失的东西：失败发生时没有留下足够
Browser facts，导致只能知道两个contamination同时出现，不能判断capture为何不完整。

## 7. 当前保守分类

```text
original required failure                         = ESTABLISHED / RETAINED
subject drift observed in original attempt        = TRUE
Browser capture incomplete in original attempt    = TRUE
precise lower cause                               = UNKNOWN
stable fresh reproduction                         = NOT_OBSERVED
runtime semantic defect                           = NOT_ESTABLISHED
conservative Verdict defect                       = NOT_ESTABLISHED
test proof-facility observability gap              = ESTABLISHED
test-only bounded correction feasibility           = ESTABLISHED
doc415 qualification                              = NOT_ESTABLISHED
carrier implementation authority                  = NOT_GRANTED
```

理论遇到反例时应检查前提，不应不断添加例外；但局部前提检查也不能冒充全局问题已经解决。本结论只覆盖该M10 proof target，
`local_not_global = true`。

## 8. 资格链与target责任

本文只允许修改：

```text
README.md
AGENTS.md
docs/419-r1-m10-subject-drift-browser-capture-stability-feasibility-audit.md
docs/milestones.md
```

资格链必须是：

```text
final docs-only bytes / exact four-file scope / declared local gates
    -> original PR required Public CI (attempt 1; any non-success retained and stop)
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / doc419 unique Render diagnostic + formal readbacks
    -> fresh AGENTS / milestones exact-commit anonymous public+API+Git raw observations
    -> independent reconciliation + finite closeout
    -> M10_STABILITY_FEASIBILITY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

README/doc419由GitHub Render证明完整公开阅读，AGENTS/milestones因已超过frozen Render complete window，必须只用raw/API/Git byte
identity证明公开精确字节，不能再制造已知的truncation formal。

## 9. 状态投影与下一停止线

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_SUCCESSOR_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_MERGED_READBACK_NOT_QUALIFIED
R1_MANIFEST_CARRIER_FAILURE_BOUNDARY_AUDIT_READBACK_TARGET_CORRECTION_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_PROOF_FACILITY_CORRECTION_NOT_STARTED_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合后，最多成为`M10_STABILITY_FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。publication形成新事实后必须返回
CONTROL LOOP；下一步可以选择一个独立、test-only proof-facility correction，但不能从本文直接施工。doc415必须等该基础边界重新资格化以后，
再从新的exact main独立重建；不得复用PR #476 head或把本文资格回填给它。

`proof_is_not_problem_solving = true`：本审计证明一条不弱化oracle的有限修正路线存在，不代表原lower cause已知、test已修、doc415已
qualified、carrier已实现或原工程问题已经解决。

`local_not_global = true`：R1完成后仍须执行人类+AI全项目检查，不得把本地M10可行性结论外推为整个R1、Review产品或系统全局最优。
