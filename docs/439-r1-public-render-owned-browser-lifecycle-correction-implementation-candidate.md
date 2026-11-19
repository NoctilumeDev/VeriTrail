# R1 Public Render owned-browser 生命周期修正实现候选

> 状态：`IMPLEMENTATION_CANDIDATE / NOT_MERGED / NOT_QUALIFIED / NOT_FROZEN`
>
> 精确基线：`main@5fee88a3ff4d3803288c3c79e4c38498336b39ed / tree=6b5a794087054cd9a7af054172afbd238e55e4f8`
>
> 合同：[文档438](438-r1-public-render-owned-browser-lifecycle-correction-contract.md)
>
> 影响层级：`L3_IMPLEMENTATION`；只实现冻结的 P2 owned Playwright driver lifecycle/cleanup 边界。

## 1. 施工授权来自 doc438 的完整闭环

PR #500 把 doc438 候选
`base=24d728065b1d165eb3e241c872606c8356fabd10 / head=8aef9dd009a4d81f9998c10706d3cf764e908e63 /
tree=6b5a794087054cd9a7af054172afbd238e55e4f8` 精确合入当前主线。original Public CI
`44575160885`、exact-main Public CI `44583241629` 与 Browser Smoke `44583241839` 均为 attempt 1
SUCCESS（15/15、15/15、1/1）。fresh exact-main readback 没有使用待修正的 P2 充当自己的证明：一个 P1 API
formal 与 README/doc437/doc438/milestones 四个 raw/API/exact-Git formal 各有唯一 PASS，且显式不声称 Render
completeness。独立 reconciliation、44-artifact finite closeout 与 post-closeout integrity SHA-256 依次为：

```text
831dd635446415591162ab6cf16e019e3d17a2dbd70804c15bdc7247dcff39a9
7e1570220cc2962b6bef1c0fc5b9cb3f0fcc498761bd9aab0f31a3f2beb1eb8f
c772337e967170b796cc1aac712d4b399b24cc40a6a339dedd65630ececfd420
```

因此只有以下授权生效：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_CONTRACT_0_2_FROZEN
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_ALLOWED
```

这不是实现资格、公开发行资格、doc437 恢复、Manifest 0.2 授权或 R1 全局完成。原 formal ERROR、PowerShell
setup errors、in-progress log proof-facility limitation 与 doc438 closeout identity 全部继续保留。

## 2. 最小实现

实现只修改 `public_render_browser.py` 及两个既有测试文件：

1. production `RenderBrowserSession` 在锁定的 Playwright `1.62.0` 启动后，从该 session 自己的 transport
   取得 driver process identity；identity 缺失、非正整数或没有 termination capability 时，在 Chromium launch
   以前 fail closed；
2. 每个 session 无条件创建 `_PlaywrightDriverDeadlineGuard`，不能因注入自定义 Playwright factory 而绕过；
3. guard 只等待 `RenderBrowserSession.open()` 已建立的同一个绝对 collection deadline；normal close 先完成时取消，
   不杀 driver，也不刷新时间预算；
4. deadline 到达而同步 browser/cleanup call 仍阻塞时，guard 只终止该 session 已绑定的 Playwright driver；不做
   任意 PID discovery、远端 cleanup、重试、恢复 attempt 或新事实采集；
5. cleanup 仍按 response-body controller、CDP、context、browser、Playwright 顺序尝试。transport 终止造成的
   `close-failed` 与 `playwright-driver:deadline-terminated` 都保留，因而 Evidence 必须保持 `ERROR`；
6. guard termination failure、guard thread 超过冻结的 5 秒 release envelope 与既有 cleanup failure 都进入
   `cleanup_errors`，不能被吞掉或重命名为成功。

实现没有修改 observation/fact Schema、coverage reason、normalization semantics、Core evaluator/Verdict、P3 handoff、
R1 Manifest、45 秒采集窗口、network/body budget 或 URL allowlist。GitHub Evidence 源码仍为既有未发布
`0.1.1.dev0`；不可移动的公开 `github-evidence-v0.1.0` 字节没有变化，也不包含本修正。

## 3. 本地 witness

### 3.1 源码与真实 Chromium

Python 3.10.6 / 3.13.13 × normal / `-O` 的 GitHub Evidence full suite 各为 189/189 PASS。该集合保留既有
normal COMPLETE、404/500、aborted navigation、response-body limit、paired P1→P2 与 P3 handoff，同时新增：

- normal cleanup 不触发 driver termination；
- response-body close、CDP detach、context close、browser close、Playwright stop 五种同步阻塞均由同一 deadline
  释放；
- missing/invalid identity 在 browser launch 前拒绝；
- termination failure 与 guard-thread residue 显式进入 cleanup error；
- matching Playwright/Chromium 的 5 秒 blocked-call test 在 10 秒上限内返回。

### 3.2 wheel-only 与 residue

从本候选重建的 Core 与 GitHub Evidence wheel SHA-256 为：

```text
veritrail-0.13.0-py3-none-any.whl
3c25fd80e9c520f8566b34c8a343943110686cb88352cfa6ca5dd1b47e0250ea

veritrail_github_evidence-0.1.1.dev0-py3-none-any.whl
477a9cf61ef7541d27d0a3a208a60083df52af97aadb86049a6ff3beae1c3985
```

两个 clean installed-wheel probe 都只从各自 site-packages 加载修正模块。Python 3.10.6 在 5.016 秒、Python
3.13.13 在 5.023 秒形成 terminal result；driver `returncode=1`，完整 owned process-tree 的 retained PID 集合在
终态后均无 residue。CDP/context/browser 的 transport-close failure 与 deadline termination 全部保留。插件卸载后，
两个 Python 的 Core-only probe 又分别导入并验证 P1/P2 retained Evidence，插件 distribution 与 capabilities 均不存在。

wheel probe attempt 1 因 proof script 假定 async `Process` 具有 `poll()` 而 ERROR；attempt 2 又把预期保留的
CDP/context/browser close-failed 错写成“不允许出现”的 oracle，因此返回 FAIL。两者都保留为
`PROOF_FACILITY_ERROR / EFFECT_NONE`；attempt 3/4 与 3.13 attempt 1/2 没有覆盖这些身份。

## 4. 候选资格链与状态上限

本实现候选最终 scope 只能是：

```text
plugins/github-evidence/src/veritrail_github/public_render_browser.py
plugins/github-evidence/tests/public_render/test_browser_session.py
plugins/github-evidence/tests/public_render/test_chromium_fixture.py
README.md
AGENTS.md
docs/439-r1-public-render-owned-browser-lifecycle-correction-implementation-candidate.md
docs/milestones.md
```

它仍须完成：final bytes local qualification、original PR attempt 1、protected exact-head merge、新 exact-main Public CI
与 Browser Smoke、从该 exact main 重建的 exact-source wheel negative lifecycle readback、README/doc437/doc438/doc439/
milestones 的 fresh P1/API + raw exact-Git byte observation、独立 reconciliation 与 finite closeout。任何 non-success
保留原身份，不 rerun 洗白。

全部门闭合后最多成为：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED_NOT_AUTHORIZED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回 CONTROL LOOP，独立决定 source freeze 与 GitHub Evidence `0.1.1` public release contract；不能把
exact-source repaired wheel 写成 public installed-product 已恢复，也不能直接恢复 doc437 或 Manifest 0.2。
`proof_is_not_problem_solving = true`、`local_not_global = true`；R1 完成后的 human + AI 全项目复核仍是独立目标。
