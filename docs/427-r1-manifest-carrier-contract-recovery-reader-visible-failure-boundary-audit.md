# R1 manifest carrier contract recovery reader-visible failure-boundary audit

日期：2026-11-16

> 状态：`R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 坐标：`main@72b5e95ae30933d139967c94dc50f5c11c6c8a5b`，tree
> `7f87e0e0624328168363db105237f0e84a27cad6`。
>
> 受审对象：PR #488 / doc426在original与exact-main双门成功后的fresh README reader-visible diagnostic failure。
>
> 影响：`L3_QUALIFICATION_BOUNDARY + L0_PUBLIC_DOCUMENTATION`。本文只保存失败identity、公开可见性边界、资格影响与最小后继责任；
> 不修改doc426合同语义、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、carrier、Manifest、
> persistence或public Review，也不把失败候选升级为qualified history。

## 1. CONTROL LOOP进入点

[文档425](425-r1-m10-repeatability-failure-observation-correction-implementation-freeze-publication.md)已经由PR #487完成
original/exact-main双门、fresh installed-product readback、independent reconciliation与finite closeout，所以有界test proof-facility
correction现在是`FROZEN`。PR #481的exact-main failure、doc420资格状态与lower cause `UNKNOWN`没有回填。

fresh CONTROL LOOP随后确认旧PR #476合同候选仍为`CLOSED / UNMERGED / ORIGINAL_PUBLIC_CI_FAILED / NOT_QUALIFIED`，但击穿它的
最小M10 proof-facility边界已经由docs416–425分别审计、修正并资格化。从新的exact main独立建立的
[文档426](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)只重建合同内容，不继承旧坐标、attempt、
qualification或authority。

## 2. PR #488 exact candidate与自动门

```text
base    = 663ca58054f56e8e3eada7ee2347225d0e9484e7
head    = c0fe7a218d1f60be9a1075c5837785b4ed1465db
tree    = 7f87e0e0624328168363db105237f0e84a27cad6
scope   = README.md
          AGENTS.md
          docs/426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md
          docs/milestones.md
commits = 1
files   = 4
```

candidate local semantic matrix、focused regression、global/local hygiene与qualification均PASS。主要identity为：

```text
semantic canonical SHA256 = 0f2e1586fbe77c7c186a7d73a66d3b5a19f7bd951d5706ef7991fccfaddd0cc7
focused matrix SHA256      = 18e31e7069e252eb76035f76c06f790e71fa74a085733925222d6fe67af822a8
local qualification SHA256 = d90cafced5b084b1f57e2ea954adb999c70b85c0136a78bdd6afae6e1eb34113
pre-PR seal SHA256          = c9da065786a8bccda36bfe42f2777bd6f75252e25a8242aad0e39e254d6bea9a
post-commit seal SHA256     = 1fc455cf32e4b8142592ee20f4f0fddd9e4a181422f5bd7edd1e28f62911c9e0
```

original Public CI `43866121290` attempt 1为15/15 SUCCESS。protected exact-head merge形成
`main@72b5e95ae30933d139967c94dc50f5c11c6c8a5b`，tree保持不变，parents依次为exact base与head。new exact-main
Public CI `43872002039` attempt 1为15/15 SUCCESS，Browser Smoke `43872002011` attempt 1为1/1 SUCCESS；没有rerun。

original qualification、protected merge与exact-main gate seal SHA-256为：

```text
fbfb2d8dc8c084bb07968796c791d743ee301a51369820ddcef37fd88e496287
6d853294db1725d083136aa4d9fc72dae7cf8547db663457d7a7ce4841430973
ebd531c00b381a8a31620bc210a1740ad31a7f4618127086e2f2cacfa08be2d9
```

这些门只证明各自exact world。它们不能替代fresh installed-product readback，也不能自动冻结doc426。

## 3. fresh readback world与保留的setup identities

fresh detached worktree只认`72b5e95…`world。Python 3.13.13环境从公开Core 0.13.0与GitHub Evidence 0.1.0 wheel建立；
exact source、worktree、remote main、candidate/original/merge/gate identities与primary `audit.json`均在preformal中重验。
preformal validation与pre-observation adapter freeze SHA-256为：

```text
02c05bda0814c806c1e64a0dcc2ead8595612e19c26df17923e7b1ca1ec3c7da
acf4732fb5f7a89b33ce63ce79fc9aa2cbb0e530c85b158dcea740b984961e99
```

以下setup/proof-facility identities全部按原状态保留且effect为`NONE`：

- fresh worktree侧栏登记因本聊天累计超过100个attachment identity失败；worktree本身创建成功；
- Windows `rg` wildcard触发OS error 123，后改用`--glob '*.py'`；
- 一次`apply_patch`尝试对同一文件执行多个update operation被工具拒绝，未产生修改；
- reset前anonymous rate diagnostic #1为HTTP 200但remaining 0，API preflight #1为403；
- reset后重新核账exact world，diagnostic #2观察remaining 60，preflight #2为HTTP 200且remaining 58。

没有使用认证替代，也没有在reset前制造重复观察。

## 4. README diagnostic的直接反例

README diagnostic immutable identity为：

```text
identity              = r1d426-diagnostic-readme-1-72b5e95
collection session    = github-render-0ad5edf155364a36a26fad0b0b77539b
coverage              = COMPLETE
top-level HTTP status = 200
reader marker count   = 0
Core Verdict          = NONE
classification        = DIAGNOSTIC_ONLY_NON_QUALIFYING_ERROR
```

Render collection没有coverage reason或cleanup error，三个content-window sample稳定；网络写请求按冻结policy被阻断，不影响coverage。
因此该观察不支持网络或Collector defect。

对exact README source的独立检查得到：

```text
target phrase source occurrence = line 981 only
enclosing <details> open         = line 895
enclosing </details> close       = line 998
details open attribute           = absent
reader-visible rendered count    = 0
```

也就是说，doc426入口存在于raw Markdown，却只在默认折叠的历史索引内；README顶部读者可见状态截至doc425，没有公开doc426 candidate。
这是`PUBLIC_READER_VISIBLE_PROJECTION_DEFECT`，不是“marker选错”或“GitHub未渲染”。

source/readback contradiction record与64-artifact failed closeout SHA-256为：

```text
cb5a22d7a970f2a5bde22b2f9b21808cfd0a814092956a0e9f465bd158668991
bccf9b2ba20793628b3d583ea135538a5c14a55302029a1b85ab3d6882035ef6
```

README formal、其余六个Render target与十一个raw target均未启动；没有Core Verdict、independent reconciliation或success closeout。
同一diagnostic不得重跑，后继也不得复用本world的未完成资格链。

## 5. 当前资格影响与authority ceiling

机械状态只能是：

```text
doc426 = MERGED / ORIGINAL_GATE_PASS / EXACT_MAIN_DUAL_GATES_PASS /
         READBACK_NOT_QUALIFIED / NOT_FROZEN

manifest carrier successor runtime = NOT_STARTED / NOT_AUTHORIZED
global composition authority        = NOT_RESTORED / NOT_AUTHORIZED
public Review                       = NOT_STARTED
R2-R6                               = NOT_STARTED
```

PR #476 original failure、PR #481 exact-main failure及其各自lower cause `UNKNOWN`继续保留。PR #488的readback failure既不解释它们，
也不被它们解释；三个exact world不得拼接。

## 6. 禁止的伪恢复

```text
retry r1d426-diagnostic-readme-1-72b5e95 until marker appears
replace the marker with a phrase from another visible state while leaving doc426 hidden
open the collapsed details only in the proof facility and call it default reader-visible
splice original/exact-main green gates with a different readback world
reuse unstarted doc316/doc397/doc414/doc419/doc425/doc426 or raw target observations
rewrite doc426 as qualified or frozen history
move or delete PR #476, PR #481 or PR #488 failure evidence
create Schema 0.3, carrier, Manifest runtime, persistence or public Review
restore global composition authority or start R2-R6
```

## 7. 最小合法后继seam

恢复必须串行进行：

1. 本docs-only failure-boundary audit先取得自己的完整资格，只固定PR #488 dual-gate成功、reader-visible failure与authority ceiling；
2. 返回fresh CONTROL LOOP，从新的exact main建立独立public-projection correction/recovery candidate；
3. correction只能使当前合同状态在默认reader-visible README中准确可见，并重新绑定fresh readback责任；不得修改doc426合同语义；
4. correction自己的完整资格链闭合后，仍须返回CONTROL LOOP判断是重建合同资格还是另建freeze publication；不得继承PR #488资格。

理论遇到反例时先检查前提，而不是增加例外。本次被击穿的前提是“raw Markdown中的链接等于默认reader-visible公开状态”，所以最小
重开对象是public projection责任，不是P2 oracle、合同语义或runtime。

## 8. 本audit candidate的精确scope

tracked scope只允许：

```text
README.md
AGENTS.md
docs/427-r1-manifest-carrier-contract-recovery-reader-visible-failure-boundary-audit.md
docs/milestones.md
```

doc426、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、carrier、Manifest、persistence与全部
frozen semantic bytes必须保持`72b5e95…` base bytes。README只公开记录失败状态与本文入口；它不修正或重试doc426资格。

local gates至少核对exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、reader-visible README audit marker、
PR #488 exact identities、retained diagnostic/contradiction/closeout hashes、unchanged source/Schema/test/history bytes、`git diff --check`、
read-only global/local hygiene与primary `audit.json` continuity。

## 9. 本audit自己的资格链

```text
final docs-only audit bytes / declared local gates
    -> original PR required Public CI
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc426 / 本文 Render observations
    -> fresh AGENTS / milestones raw.githubusercontent + Contents API + exact-Git observations
    -> independent reconciliation
    -> finite closeout
    -> READER_VISIBLE_FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是candidate。闭合后也只允许进入独立public-projection correction/recovery；不得自动重建doc426资格、冻结
合同、创建runtime或恢复global composition authority。

```text
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`proof_is_not_problem_solving = true`、`local_not_global = true`、
`post_r1_human_ai_global_check_required = true`；R1完成后仍必须由人类+AI共同执行独立全项目检查。
