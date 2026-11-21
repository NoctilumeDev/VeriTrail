# R1 picomatch 公告撤回与 Workbench 审计恢复读回资格恢复

日期：2026-11-21

> 候选状态：
> `R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_READBACK_QUALIFICATION_RECOVERY_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@844385457663dc95fc310a1b961aa6f4ec218d84`，tree
> `71e859aaaef307c05f52bd393a271864407dfaff`。
>
> 上游：[审计源恢复候选](437-r1-picomatch-advisory-withdrawal-and-workbench-audit-recovery.md)、
> [owned-browser 生命周期修正冻结发布](440-r1-public-render-owned-browser-lifecycle-correction-implementation-freeze-publication.md)、
> [GitHub Evidence 0.1.1 公开发行事实](445-r1-github-evidence-0-1-1-public-release-readback-facts.md)与
> [证据反馈工作法](working-method.md)。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_RECOVERY_HISTORY_ONLY`。本文不修改 dependency、lock、Workbench、
> workflow、audit oracle、runtime、test、Schema、Provider、Collector、Core、Verdict、Manifest 0.2 或 global
> composition authority。

## 1. CONTROL LOOP：恢复资格，不改写失败

[文档 437](437-r1-picomatch-advisory-withdrawal-and-workbench-audit-recovery.md)保存了两个不同 external audit world：

1. PR #498 original Public CI `44148053612` attempt 1 的 required Workbench audit 对 exact lock 观察到
   `GHSA-fc5q-39xc-vjpf / picomatch <=4.0.7`，最终为 13 SUCCESS、1 FAILURE、1 SKIPPED；PR 关闭、未合并、未 rerun；
2. 公告撤回以后，同一 official bulk request 第一次仍返回 advisory，后继 observation 才返回空集合。internal
   propagation/cache root cause 保持 `UNKNOWN`。

doc437 自己随后经 PR #499 合入 `main@24d728065b1d165eb3e241c872606c8356fabd10`，original/exact-main
Public CI 与 Browser Smoke 均通过；但 fresh formal `r1d437-formal-doc437-1-24d7280` 在 P1
`COMPLETE` 后出现 P2 navigation 约 30 秒 `ERROR`，frozen 45 秒窗口到期以后 cleanup 继续阻塞约 25 分钟，只有外部终止
该 session 的 Playwright driver 才形成 terminal `FORMAL_READBACK_ERROR`。没有 Core Verdict，lower cause 继续是
`UNKNOWN`。因此 doc437 当前只能是：

```text
MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED
```

本文不 rerun 该 attempt，不把后来的 source fix 或 public Release PASS 拼回它，也不把公告撤回解释为所有 glob 输入都已被证明安全。
本文建立新的 publication、Plan、collection session 与 formal identity，只恢复 doc437 未闭合的 product-readback 资格责任。

## 2. 被击穿的最小边界已经独立修正并冻结

doc437 first formal 暴露的边界只属于
`P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_AND_CLEANUP`。后继没有提高 45 秒采集预算，也没有改变
fact/coverage/Core/R1 oracle；它按独立合同 0.2 让每个 production session 绑定自己的 Playwright driver 与原绝对 deadline，
并以 5 秒 cleanup-only release envelope 对 owned driver 做 bounded containment。

[文档 440](440-r1-public-render-owned-browser-lifecycle-correction-implementation-freeze-publication.md)自己的完整资格链闭合后，
以下 source 状态已经生效：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
```

这项 source freeze 没有回填 doc437，也没有修改公开 0.1.0。它只证明可以继续建立独立 public-product recovery；不能单独升级
doc437 的资格状态。

## 3. public 0.1.1 产品坐标已经形成并冻结

PR #508 把
[文档 445](445-r1-github-evidence-0-1-1-public-release-readback-facts.md)以以下 identity 精确合入：

```text
base   = f65b611749fe668c1dbba4d5b972c1221d76bf60
head   = 82e5facb8a1aa15d08e297688aeb132a19d2cf57
tree   = 71e859aaaef307c05f52bd393a271864407dfaff
scope  = 1 commit / 4 files
merge  = 844385457663dc95fc310a1b961aa6f4ec218d84
```

original Public CI `44860527517`、exact-main Public CI `44864299522` 与 Browser Smoke `44864299506` 均为
attempt 1 SUCCESS（15/15、15/15、1/1）。original qualification 与 exact-main gates SHA-256 为：

```text
fcbb49300bda478e5e800a477eb6d00bbfe40b675952532df328a6811cc532a9
12533ea599e60761d019f68de0b8b33d3ce59ccefbee2d22d4522b87ef80494c
```

第一次 readback root 的唯一 P1 formal 返回 `coverage=ERROR / facts.commit=null`；lower cause `UNKNOWN`，且旧 adapter
在保存该 failure 时又因 null commit 触发 `AttributeError`。该 root 没有重用或 rerun，failure retention SHA-256 为：

```text
5a7b61a52e89a629335e444058b62412873c65ade0217aead98dd44cce3d645e
```

successor root 只修正 proof facility 的 null-safe retention，并以新的 formal identity 完成 P1 与
README/doc441/doc442/doc443/doc444/doc445/milestones raw/API/exact-Git readback。independent reconciliation、
62-artifact finite closeout 与 post-closeout integrity SHA-256 分别为：

```text
354f56cd203b78789a39726fd2e4bb37e224c502f77a539037d8f3f67ffc1f46
d49806c116ed930201a395e9b1aff1fe37ef0cb592ff1aa027ee6e3cb53500f7
5e1bc27fe22a51aa8411a893ae20e14dfa07acd9e46b2af3534aa5717c28652e
```

因此以下 public-product 状态已经生效：

```text
GITHUB_EVIDENCE_0_1_1_RELEASED
GITHUB_EVIDENCE_0_1_1_PUBLIC_READBACK_COMPLETE
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_FROZEN
```

受保护 annotated tag、non-Latest Release、四项公开资产与历史 failure identity 都保持 doc445 所固定的坐标；本文不重发 tag、
Release 或 asset。

## 4. source 与 lock continuity

当前 exact main 的 Workbench lock 继续与 doc437 audit world 逐字节相同：

```text
path             = web/package-lock.json
git blob         = 2ebdeec76eee0b6368f202aebdccf58ecd184945
SHA-256          = ff6b4bb86dbe3c369d29f6230633b7db57c73a650ddc3fe923e6d5c821aa9904
locked picomatch = 4.0.5
```

从 doc437 merge world 到当前 main，lock 与 dependency graph 没有为了通过审计而修改；workflow 的后继变化只同步了
GitHub Evidence 0.1.1 exact version binding，不降低 audit level、不改变 registry、不加入 ignore/waiver。新的 original PR 仍必须由
未改写的 required Workbench audit 在自己的 exact head 与 attempt 中重新裁决。

## 5. 本 recovery 的 fresh public-product obligation

本文只有在自己的 merge world 中完成以下新的 observation 才能恢复 doc437 历史资格：

1. 从公开 `github-evidence-v0.1.1` 与公开 Core 0.13.0 asset 建立 fresh、无 token 的 installed-product world；不得用
   exact-source wheel 代替 public distribution；
2. 从新 exact main 派生 sealed request，运行一个新的 P1 repository formal，要求 exact commit 且
   `coverage=COMPLETE`；
3. 使用同一新的 Plan/attempt 边界运行 P2 public Render formal；必须在冻结总 deadline 内 terminal，cleanup-only release
   bounded，owned driver terminal 且 residual process set 为空；P1 与 P2 必须各自保留标准 Evidence，不能互相替代；
4. 对 README、doc437、doc440、doc445、本文与 milestones 分别执行唯一一次 fresh anonymous
   raw/API/exact-Git byte observation；已成功目标不得重复；
5. independent reconciliation 必须同时绑定 #498、doc437 first formal、doc440 source freeze、doc445 public product、当前
   exact base/head/tree、new Plan/session/Evidence、lock identity、全部 retained non-success 与 primary audit；
6. 建立 finite closeout 与 post-closeout integrity，不作 self-inclusion 声明。

这条 formal 只验证被重新开放并已经冻结的 public-product lifecycle seam。P1/P2 Provider 只提供观察事实，不拥有
doc437 的证据充分性裁决；publication frozen obligation 与 independent reconciliation 决定资格是否闭合。本文不创建或覆盖
Core Verdict，也不把没有 Core Verdict 的 docs-only readback 偷换成业务证明。

## 6. 必须继续保留的 non-success

后继 PASS 不得删除、改名或解释以下身份：

- PR #498 original required Workbench audit FAILURE、dependent Starter SKIPPED、关闭未合并、无 rerun；
- 公告撤回后第一次 official bulk observation 仍返回 advisory，internal propagation cause `UNKNOWN`；
- doc437 first formal 的 P1 COMPLETE、P2 navigation ERROR、约 25 分钟 cleanup block、external containment、无 Core Verdict与
  lower cause `UNKNOWN`；
- doc439、doc440、doc441–445 固定的全部 FAIL、ERROR、CANCELLED、setup failure 与 `UNKNOWN`；
- doc445 first readback P1 `coverage=ERROR / facts.commit=null` 与 old adapter retention `AttributeError`；
- 本 CONTROL LOOP 首次未引用 PowerShell `HEAD^{tree}` 导致 revision 误解析，以及未显式按命令注入代理导致 remote
  `Recv failure: Connection was reset`；两者均为 setup/network identity，qualification effect 为 `NONE`；
- Codex sidebar attachment cap 与其他 UI 注册问题；它们不删除 filesystem/GitHub evidence，也不改变产品状态。

primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json` 必须继续保持 SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 7. 本 publication 自己的资格链

tracked scope 只允许：

```text
README.md
AGENTS.md
docs/446-r1-picomatch-advisory-withdrawal-workbench-audit-readback-qualification-recovery.md
docs/milestones.md
```

local gates 必须重核 exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
required markers、`git diff --check`、global/local hygiene、lock continuity、forbidden runtime/export drift 与 primary audit continuity。

完整资格链是：

```text
final docs-only recovery bytes / declared local gates
  -> original recovery PR Public CI 15/15 attempt 1 without rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous public 0.1.1 installed-product P1 + P2 formal
  -> README/doc437/doc440/doc445/doc446/milestones unique raw-byte observations
  -> independent reconciliation + finite closeout + post-closeout integrity
  -> doc437 AUDIT_SOURCE_RECOVERY_AUDITED / QUALIFIED_HISTORY
  -> return CONTROL LOOP
```

任何 non-success 都保留原 identity 并停止；不得 rerun until PASS、复用旧 PASS、弱化 oracle 或拼接不同 world。

## 8. 当前状态与后继停止线

本文自己的全部门闭合以前只能声明：

```text
GITHUB_EVIDENCE_0_1_1_RELEASED
GITHUB_EVIDENCE_0_1_1_PUBLIC_READBACK_COMPLETE
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_FROZEN
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_READBACK_QUALIFICATION_RECOVERY_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门成立后，只允许把 doc437 升级为 `AUDIT_SOURCE_RECOVERY_AUDITED / QUALIFIED_HISTORY`，同时保留 #498 与首次
readback failure world。形成该新事实后必须返回 CONTROL LOOP；只有重新审计冻结 Manifest contracts、当前 exact source、公开
0.1.1 product 与新的反例后，才可决定是否建立 versioned Manifest 0.2 feasibility successor。不得从本文直接施工 runtime、恢复
global composition 或启动 R2–R6。

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
```
