# R1 picomatch 公告撤回与 Workbench 审计源恢复

日期：2026-11-19

> 候选状态：`R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@8a9233582a519760e2c3008e6d8e1324442ba687`，tree
> `18624af19890d064f7b11a184a124023fccdc70a`。
>
> 上游：[manifest carrier successor private implementation 冻结发布](435-r1-manifest-carrier-successor-private-implementation-freeze-publication.md)。
>
> 影响：`L0_DOCUMENTATION / EXTERNAL_AUDIT_SOURCE_RECOVERY_HISTORY_ONLY`。本文不修改依赖、lock、Workbench、workflow、
> audit level、registry、runtime、tests、fixtures、Schema、Provider、Core oracle、Verdict或任何frozen semantic bytes。

## 1. CONTROL LOOP：先保留 #498，再判断外部世界是否改变

PR #497把doc435以
`base=d9d4d9ae0ae8de8ab263845e1b9c7eb744882ad3 / head=ffbe1c993e5ea6016ce4a9b7cbc1835161256358 /
tree=18624af19890d064f7b11a184a124023fccdc70a`精确合入本审计基线。original Public CI `44067075447`、
exact-main Public CI `44072793203`与Browser Smoke `44072793191`均为attempt 1 SUCCESS（15/15、15/15、1/1）。fresh
README、doc434、doc435与milestones各有唯一qualifying formal PASS；independent reconciliation、206-artifact closeout、expected
stdout self-capture mismatch与209-artifact finite integrity均已闭合。因此：

```text
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
```

随后从同一exact main建立的第一次Manifest 0.2 private implementation feasibility audit是PR #498：

```text
base  = 8a9233582a519760e2c3008e6d8e1324442ba687
head  = 574c1fd1d6e29400a7e54bd7c92acdfc64a3dc70
tree  = a2bf714cb00e4b46b5ed7abcb8b49182ba64db82
scope = 1 commit / 4 docs files
```

其original Public CI `44148053612` attempt 1真实结束为13 SUCCESS、1 FAILURE、1 SKIPPED。唯一失败job
`134268474044`是required `Workbench tests, lint, build, and audit`：tests、lint、type-check/build均通过；未改写的
`npx --yes npm@11.19.1 audit --audit-level=moderate --registry=https://registry.npmjs.org`返回13个high severity
vulnerabilities，决定性条目为`GHSA-fc5q-39xc-vjpf / picomatch <=4.0.7`，exact lock版本是`4.0.5`。dependent
Starter job只因该失败被SKIPPED，不是独立根因。PR没有rerun，已经关闭且未合并；doc436继续只属于失败world，不能在main复用编号、
内容资格或状态身份。

同一时间，clean exact main的相同lock也复现13 high audit failure。由此固定：

```text
PR #498 original required gate failure            = TRUE
candidate content failure established             = FALSE
Manifest semantic counterexample established      = FALSE
candidate regression established                  = FALSE
shared Workbench dependency qualification failure = TRUE
lower activation mechanism                         = UNKNOWN
```

后来的公告撤回或审计源恢复不能把这个world改写成PASS。

## 2. 不变的源码与lock身份

两次外部观察都绑定同一exact source和lock：

```text
exact main       = 8a9233582a519760e2c3008e6d8e1324442ba687
exact tree       = 18624af19890d064f7b11a184a124023fccdc70a
lock path        = web/package-lock.json
lock blob        = 2ebdeec76eee0b6368f202aebdccf58ecd184945
lock SHA-256     = ff6b4bb86dbe3c369d29f6230633b7db57c73a650ddc3fe923e6d5c821aa9904
locked picomatch = 4.0.5
```

[GitHub Advisory Database](https://github.com/advisories/GHSA-fc5q-39xc-vjpf)当前公开页面把
`GHSA-fc5q-39xc-vjpf`标为`Withdrawn`，明确记录“withdrawn on Nov 18, 2026”；
页面仍展示affected versions `<=4.0.7`与patched versions `None`。该页面的fresh anonymous HTML/headers SHA-256分别为：

```text
3a52cbffa03e45e0ccbdab2faa4dcbe80b684f032222343209cb4d02d82566c0
8fea952ba0a4d9e9061816f3a9aa5c60b68cc8f73f404667e684f282f283784a
```

因此当前事实不是“官方已经发布修复版”，而是“外部公告提供方撤回了先前裁决”。`picomatch`官方registry latest仍是`4.0.7`；
没有新的patched coordinate可以机械升级。

## 3. 同一请求观察到审计提供方投影先滞后、后恢复

从exact lock机械生成official npm bulk advisory request；两次request字节完全相同，SHA-256均为：

```text
957df6f4a0a421846a8c32a9e0222cdfa61ce194798fd3accfef97984e71fe44
```

观察时间与结果：

| Observation | HTTP/Cache | Response | Response SHA-256 |
| --- | --- | --- | --- |
| 2026-11-18 17:02:08 UTC | 200 / `CF-Cache-Status: DYNAMIC` | 仍返回`GHSA-fc5q-39xc-vjpf` | `22027ad35cba50a926129f603a4d15ec8ed540788c9f5f24dd480f9909599888` |
| 2026-11-19 13:41:28 UTC | 200 / `CF-Cache-Status: DYNAMIC` | `{}` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |

第二份headers SHA-256为`7a85f3291c96146dfb54f9b4cadf18118a158ac85589a3d199258675ae4af374`。这只能证明：

```text
GitHub advisory public classification changed        = TRUE
npm audit-provider projection lag was observed       = TRUE
same official bulk request later returned no advisory = TRUE
project source/lock regression established           = FALSE
internal propagation/cache root cause                 = UNKNOWN
```

它不证明所有复杂glob输入在所有调用面都绝对安全，也不把维护者与报告方的争议裁成一般真理。现实世界的公告裁决与审计投影都是
带时间坐标的外部证据；source identity不变不代表外部qualification world不变。

## 4. Oracle没有改变，本candidate也不是dismissal

本恢复候选明确禁止：

- 降低`--audit-level=moderate`、改registry、增加ignore/allowlist/waiver或手工dismissal；
- 运行`npm audit fix --force`、降级Vitest、伪造patched version或修改lock来迎合已撤回条目；
- 把第二次bulk observation拼接进#498 original attempt，或用未来绿灯回填#498；
- 把“withdrawn”解释成“库在所有现实输入下已形式证明无风险”；
- 直接恢复doc436、创建Manifest 0.2 runtime或授予其implementation authority。

required Workbench gate继续执行原命令、原阈值和原registry。本docs-only候选的original PR必须让该真实package-manager gate在自己的
exact head/attempt中重新裁决；direct bulk response只证明进入该新门已有事实基础，不替代门本身。

## 5. 保留的non-success与证据边界

以下身份永久保留，不被本candidate或未来PASS覆盖：

1. PR #498 original run `44148053612` attempt 1的required Workbench FAILURE、Starter SKIPPED、关闭未合并且无rerun；
2. clean exact-main live audit同样得到13 high的失败记录；
3. 公告撤回以后第一次official npm bulk observation仍返回该advisory，证明提供方投影并非同步瞬变；
4. unauthenticated GitHub advisory API请求命中rate limit，只是setup/external-rate failure；成功证据来自后继fresh anonymous HTML；
5. PowerShell未引用`HEAD^{tree}`、Windows wildcard docs lookup与Codex sidebar超过100个attachment identity等setup failures；
6. #498本地feasibility bytes、测试PASS和semantic结果只属于未资格化candidate，不可转移到本docs-only恢复world。

清理Codex侧栏旧attachment只删除UI挂载记录，不删除GitHub PR、仓库文件、分支、worktree或上述evidence identity；它没有产品语义效果。
primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`继续保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 6. 本candidate自己的资格责任

tracked scope只允许：

```text
README.md
AGENTS.md
docs/437-r1-picomatch-advisory-withdrawal-and-workbench-audit-recovery.md
docs/milestones.md
```

`web/package.json`、`web/package-lock.json`、workflows、runtime、tests、fixtures、Schema与doc435必须逐字节保持base。local gates重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. #497 qualified freeze、#498 original failure、same-lock identity、两个official bulk observations与全部保留non-success continuity；
3. `git diff --check`、read-only global/local hygiene与primary audit continuity；
4. original PR required Workbench lane执行未修改的test/lint/build/audit；
5. exact-head protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
6. fresh anonymous installed-product README/doc435/本文 Render与milestones适用的raw/API/exact-Git byte observation；
7. independent source-byte/lock/advisory-timeline/#498-retention reconciliation与finite closeout。

完整资格链是：

```text
final docs-only recovery bytes / declared local gates
  -> original recovery PR required gates without rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product readback
  -> independent reconciliation + finite closeout
  -> AUDIT_SOURCE_RECOVERY_AUDITED / QUALIFIED_HISTORY
  -> return CONTROL LOOP
```

任何non-success都保留原identity并停止；不得rerun until PASS或把different worlds拼成资格。

## 7. 当前状态与下一最小seam

本文完整资格链闭合以前只能记录：

```text
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FEASIBILITY_PR498_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只使本次外部审计源恢复成为qualified history；#498与doc436保持失败world。fresh CONTROL LOOP若没有新反例，才可从新的
exact main重建versioned Manifest 0.2 feasibility successor。不得复用#498 commit/run/qualification，也不得从本文直接施工Schema、fixture、
validator、producer、consumer、publisher、persistence或public Review。

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
```
