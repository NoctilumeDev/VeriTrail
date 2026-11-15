# R1 manifest carrier failure-boundary audit readback-target correction

日期：2026-11-16

> 状态：`R1_MANIFEST_CARRIER_FAILURE_BOUNDARY_AUDIT_READBACK_TARGET_CORRECTION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@c645ee7f68537c81023b693274701c465b81ef5d`，tree
> `5194c5d44072458cbf8efcd955bffde91ae50e26`。
>
> 受审对象：[文档416](416-r1-manifest-carrier-successor-original-gate-failure-boundary-audit.md)自身的fresh
> installed-product readback failure。
>
> 影响：`L3_QUALIFICATION_BOUNDARY + L0_DOCUMENTATION`。本文只保存失败identity、判断被击穿的proof-facility
> target seam，并恢复正确的readback责任；不修改runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core
> oracle、Verdict、doc414、doc416、doc415或任何frozen semantic bytes。

## 1. CONTROL LOOP重新区分三件事

原工程问题仍是：为future Review derivation Manifest建立不会path reread、snapshot drift、authority inversion或伪造topology的
same-attempt DerivationEvidence + private copy-owned exact snapshot carrier边界。

PR #476又留下一个独立事实：其original Public CI在Python 3.10 full-suite subject-drift world观察到额外
`BROWSER_STATUS_CONFLICT`，lower cause仍为`UNKNOWN`。doc416的证明义务只是资格化这个首败、未知归因、保守oracle与最小基础边界；
它不解决原工程问题，也不修M10。

本轮新事实只回答doc416是否完成自己的readback资格：答案是否定的。因此必须继续分开：

```text
original engineering problem != doc416 failure-boundary audit
doc416 semantic content       != doc416 readback qualification
marker occurrence             != complete product observation
proof_is_not_problem_solving  = true
```

## 2. PR #477 candidate、merge与远端门

PR #477的immutable candidate identity为：

```text
base  = ce4fe48356a088bee2d2cd12cc0bbaf590980925
head  = 47543ac7c1a43747fbe857672f51b0fa1ae87e09
tree  = 5194c5d44072458cbf8efcd955bffde91ae50e26
scope = README.md
        AGENTS.md
        docs/416-r1-manifest-carrier-successor-original-gate-failure-boundary-audit.md
        docs/milestones.md
```

original Public CI `43733903868` attempt 1为15/15 SUCCESS。protected exact-head merge形成
`main@c645ee7f68537c81023b693274701c465b81ef5d`，merge tree仍为
`5194c5d44072458cbf8efcd955bffde91ae50e26`；该exact main的Public CI `43737446035` attempt 1为
15/15 SUCCESS，Browser Smoke `43737446011` attempt 1为1/1 SUCCESS。全部没有rerun。

这些门只证明candidate与exact-main gate成立，不能替代fresh installed-product readback。

## 3. fresh readback真实失败

fresh detached worktree只认`c645ee7…`world，使用公开Core 0.13.0、GitHub Evidence 0.1.0、Python 3.13.13、
matching Chromium与anonymous/no-token环境。pre-observation adapter freeze SHA256为：

```text
cd605b87d0b113282a8221d0fe32d5fdc5ab1ad7a031411135cb053960014982
```

reset前anonymous rate diagnostic #1为`remaining=5`，preflight #1为4；没有在已知不足窗口运行readback。reset后diagnostic #2为60，
preflight #2为59。README、doc414与doc416各自取得唯一`FORMAL_READBACK_PASS`，不重复。

milestones的唯一diagnostic与唯一formal分别保留为：

```text
diagnostic classification = DIAGNOSTIC_ONLY_NON_QUALIFYING_ERROR
formal classification     = FORMAL_READBACK_ERROR
top-level HTTP status     = 200
marker occurrences        = 1
coverage                  = PARTIAL
coverage reason           = CONTENT_TRUNCATED
rendered-text limit       = 524288 UTF-8 bytes
observed rendered text    = 699273 UTF-8 bytes
overage                   = 174985 UTF-8 bytes
Core PASS                 = NOT_ESTABLISHED
```

P2正确保留marker并拒绝把不完整观察写成`COMPLETE`。failed readback boundary、128-artifact failed closeout与finite integrity
SHA256为：

```text
37378ff8ca48db8c19350c36e0c5ad82513b241bbeafaddd620ca00c874b15e6
8fe4f1b0b19cc4eac06b5a8a391c9b3b03a70f8f2828f0c3e006448461e7146e
bde9ae48a0fdcd1ec92016c1f2b512598ba36b5a8e51453ee8ab93b1d2a9d52d
```

因此doc416只能是：

```text
MERGED / ORIGINAL_GATE_PASS / EXACT_MAIN_DUAL_GATES_PASS /
READBACK_NOT_QUALIFIED / NOT_QUALIFIED_HISTORY
```

## 4. 被击穿的是readback target选择

仓库已有qualified correction history证明，完整append-only milestones超过frozen 524288-byte Public Render上限时，正确责任分工是：

- bounded读者表面使用P2 Public Render diagnostic + unique formal；
- 完整append-only milestones使用anonymous exact-commit public raw bytes、GitHub Contents API与exact Git三向逐字节对账；
- raw bytes只证明完整字节identity，不冒充Render `COMPLETE`。

doc416 §11却把README、doc414、本文和milestones全部列为readback，并在fresh facility里把milestones注册为Render target。直接归层为：

```text
P2 Collector conformance                         = ESTABLISHED
README/doc414/doc416 unique formal PASS          = ESTABLISHED / RETAINED
milestones Public Render                         = PARTIAL / CONTENT_TRUNCATED
proof-facility readback-target selection failure = ESTABLISHED
subject/runtime/Collector regression             = NOT_ESTABLISHED
doc416 semantic conclusion contradiction         = NOT_ESTABLISHED
doc416 exact-main readback qualification          = FAILED
```

该事实不回填PR #476，也不把它的`UNKNOWN`改名；同时不授予按doc416继续施工M10 feasibility的authority。

## 5. 禁止的伪恢复

```text
重复milestones diagnostic或formal
重复README/doc414/doc416已有PASS
提高、绕过或重命名frozen 524288-byte limit
用marker=1宣称Render COMPLETE
把raw bytes拼入失败formal identity
把doc416静默写成qualified history
把target selection failure解释成runtime、Subject或Collector defect
删除任何setup/error/failure/UNKNOWN identity
直接修M10 test、重建doc415或启动carrier/runtime/Manifest/public Review/R2-R6
```

## 6. 本candidate精确scope与正确readback责任

tracked scope只能是：

```text
README.md
AGENTS.md
docs/417-r1-manifest-carrier-failure-boundary-audit-readback-target-correction.md
docs/milestones.md
```

doc414、doc416、runtime、tests、fixtures、workflows、Schema、Provider、Collector、P2/Core oracle、Verdict、Evidence、carrier、Manifest与
persistence必须保持`c645ee7…` base bytes。

本candidate自己的fresh observations机械分为：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal readback |
| 本文 | anonymous P2 Public Render diagnostic + unique formal readback |
| `AGENTS.md` | anonymous exact-commit public raw + GitHub Contents API + exact Git全字节对账 |
| `docs/milestones.md` | anonymous exact-commit public/API/Git全字节对账；不重复doc416的Render failure |

## 7. 资格链与状态上限

```text
final docs-only bytes / exact four-file scope / local gates
    -> original PR required Public CI (attempt 1; any non-success retained and stop)
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / doc417 unique formal readbacks
    -> fresh AGENTS / milestones exact-commit public+API+Git raw observations
    -> independent reconciliation + finite closeout
    -> READBACK_TARGET_CORRECTION_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合后，本文最多成为readback-target correction qualified history。它不资格化或回填doc416；后继只能从新的exact main重建独立
failure-boundary audit successor，使用正确的bounded Render + raw-byte责任，然后才有资格重新判断M10 feasibility。不得直接修test、
重建doc415、启动runtime、恢复global composition或启动public Review/R2–R6。

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_SUCCESSOR_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_MERGED_READBACK_NOT_QUALIFIED
R1_MANIFEST_CARRIER_FAILURE_BOUNDARY_AUDIT_READBACK_TARGET_CORRECTION_CANDIDATE_NOT_QUALIFIED
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_NOT_STARTED_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`local_not_global = true`，R1完成后的人类+AI全项目检查继续是独立义务。
