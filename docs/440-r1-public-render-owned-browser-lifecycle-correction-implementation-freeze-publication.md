# R1 Public Render owned-browser 生命周期修正实现冻结发布

日期：2026-11-20

> 条件化状态目标：
> `P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@36edc5119a41573be95cc3fd7c4fd0e8ff307cc7`，tree
> `3a693542b9fb98ed6e5ab1c974fb9a4d937b51cc`。
>
> 上游：[合同 0.2](438-r1-public-render-owned-browser-lifecycle-correction-contract.md)与
> [实现候选](439-r1-public-render-owned-browser-lifecycle-correction-implementation-candidate.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改 runtime、tests、fixtures、workflow、Schema、
> fact/coverage/Core/P3/R1 语义、45 秒采集窗口、公开 `github-evidence-v0.1.0` 字节或任何 frozen contract。

## 1. CONTROL LOOP 与本 publication 的唯一职责

PR #501 已把 doc439 与 bounded source 候选精确合入：

```text
base                 = 5fee88a3ff4d3803288c3c79e4c38498336b39ed
head                 = 69e456694950904917aeb2d082f8b99af012f95b
candidate/merge tree = 3a693542b9fb98ed6e5ab1c974fb9a4d937b51cc
ordinary merge       = 36edc5119a41573be95cc3fd7c4fd0e8ff307cc7
diff                 = 1 commit / 7 files
```

三个远端门均只认原始 attempt，没有 rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #501 original Public CI | `44599738492` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `44608036656` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `44608036720` | 1 | 1/1 SUCCESS |

original qualification、protected merge 与 exact-main gate qualification SHA-256 分别为：

```text
2a8e8f610474bdaf7d9b5843ad0cd4694e0b10be7d12c24141173e782ab4f136
3d7b076b8a1ab80be68ada2b27fda206c6c4ef3ba7641c09ec442c48238ff5ed
f9783e689eadcc8221a21856e444ff1f6ee787d6bc25a8e45a1836a9117a2e80
```

fresh detached exact-main world 只认 `36edc511...`。从该 exact source 重建的 Core 0.13.0 与 GitHub Evidence
0.1.1.dev0 wheel SHA-256 为：

```text
veritrail-0.13.0-py3-none-any.whl
98f496ef7aae6416233c71bdc67d49267702d2045a043bc49270e13b8aca9b1e

veritrail_github_evidence-0.1.1.dev0-py3-none-any.whl
a71e062dfba1739a671ab84e9997541eae71bb28d6669fd26ff7109337cc6487
```

fresh Python 3.13.13 installed-wheel negative lifecycle formal 在 5.030 秒内返回；driver terminal、完整 owned process tree
零残留，transport 终止造成的 CDP/context/browser close-failed 与
`playwright-driver:deadline-terminated` 全部保留，且没有声称 Render 内容成功。该 observation SHA-256 为：

```text
ac54459df97fd6e356122dc1a600ddc5d71671a808efd7bcf676a4e84b2e6541
```

同一 fresh world 的一个 P1 API formal 与 README/doc437/doc438/doc439/milestones 五个 raw/API/exact-Git formal
各有唯一 PASS；所有 raw bytes 与 exact Git blob 一致，显式不声称 Render completeness。独立 reconciliation、
56-artifact finite closeout 与 post-closeout integrity SHA-256 依次为：

```text
ba8a15332bfe999aa9567dfaac0710e55137f093401a99897ec8a8a7bc5837d0
4effcbaa82948119b3baa11ec4f0f5867a813d3475a71768d5d58cae8580dd3d
2e122c885b1c066880d4119c94eb106ae671c7ecaf19e447cd6e6d5fe65efef9
```

因此 doc439 现在最多是：

```text
IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
```

fresh CONTROL LOOP 重核 doc438 frozen contract、doc439 qualified candidate、current exact source 与全部保留 non-success。
没有新事实击穿 bounded lifecycle/cleanup 边界，也没有资格把 source PASS 扩张为公开发行、doc437 恢复、Manifest 0.2、
global composition 或完整 Review 产品。下一最小合法 seam 只是让一个新的 docs-only 完整资格链发布同一 source
implementation 的 `FROZEN` 状态。

## 2. 本 publication 冻结的 exact 对象

本文若完成自己的资格链，只冻结 doc438/439 限定的对象：

1. 每个 production `RenderBrowserSession` 在 Playwright 启动后取得自己的 driver process identity，并绑定原绝对 collection
   deadline；missing/invalid identity 或缺少 termination capability 在 Chromium launch 前 fail closed；
2. 每个 session 无条件创建 driver deadline guard；normal close 先完成时只取消 guard，不杀 driver、不刷新预算；
3. response-body、CDP、context、browser 或 Playwright 同步 cleanup 阻塞时，只终止该 session 已绑定的 driver；不做 PID
   discovery、远端 cleanup、重试、恢复 attempt 或新事实采集；
4. termination failure、guard thread 超过冻结的 5 秒 release envelope、transport close-failed 与 guard residue 都保持可见，
   Evidence 继续 `ERROR`，不得重命名为成功；
5. fact/coverage/Core/P3/R1 语义、45 秒窗口、network/body budget、URL allowlist、公开 0.1.0 字节和默认 authority ceiling 不变。

qualified exact main 中三个 implementation/test blob 的 SHA-256 为：

| Path | SHA-256 |
| --- | --- |
| `plugins/github-evidence/src/veritrail_github/public_render_browser.py` | `0d14319eab081ca87247492135d169741172e1fac2b4853e3567ba9eb71b85e2` |
| `plugins/github-evidence/tests/public_render/test_browser_session.py` | `2cea3841f62c17e27d1eb9d26c159fa9d1c8f8c4ab73d72b494a57aeaa8f720e` |
| `plugins/github-evidence/tests/public_render/test_chromium_fixture.py` | `fbec2e2558e85f5cc47676882acb53143ba96f99b587327faeecbe6ec778498d` |

doc438 与 doc439 SHA-256 分别保持：

```text
5d8abbf36d8e94bc54f4a533f9d19f7a498e0f45b0e705ba41ce9e3706d00238
62929497dd7c96d6a11ee69cdc28b29e6d58e879a74f7ac68178ceadfab82419
```

这只证明冻结输入与声明适用 world 中的 bounded source lifecycle correction；不证明公开 distribution 已更新、GitHub
平台真相、全仓语义、Manifest 产品、持久化、global composition、公共 Review 收益或原工程问题已经全部解决。

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
global_composition_authority_restored       = false
```

## 3. 必须继续保留的 non-success

后继 PASS 不得删除、改名或覆盖以下 identity：

- PR #498 required Workbench audit 的 picomatch advisory FAILURE、dependent Starter SKIPPED、关闭未合并/no-rerun world；
- doc437 fresh formal 在 P1 COMPLETE 后 P2 navigation ERROR、45 秒后 cleanup 长期阻塞、外部 containment 与 lower cause
  `UNKNOWN`；
- doc439 wheel probe attempt 1 的 async Process `poll()` proof-facility ERROR 与 attempt 2 的过窄 cleanup oracle FAIL；
- #501 candidate 的 PowerShell tree capture、untracked scope、Python version、wrong test root、remote-main capture 与 attachment
  setup errors；
- first fresh readback root 因错误 Python bootstrap 和缺少 `build` module 形成的 NON_QUALIFYING setup failure，记录 SHA-256
  `f19e8be813148c503e3315b1281f33ccffaad76c984b85f63ae4cf72741f16f7`；
- 本 publication CONTROL LOOP 的 PowerShell `HEAD^{tree}` 解析、错误相对 `audit.json` 路径、错误 `closeout.json` 文件名与
  JavaScript/PowerShell quoting setup errors；
- 更早所有 FAIL、ERROR、CANCELLED、setup failure 与 `UNKNOWN`。

这些事实分别属于自己的 exact coordinate；本 publication 不能把它们拼成另一 world，也不能用后继 PASS 回填底层原因。

## 4. 本 publication 自己的资格责任

本 docs-only patch 只允许修改 `README.md`、`AGENTS.md`、`docs/milestones.md` 并新增本文。doc437–439、private
runtime、tests、fixtures、workflows、Schema、Provider、Collector、Manifest、persistence、public export、Core oracle 与全部
frozen semantic bytes必须保持 base 不变。

本层 local gates 重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings 与 required markers；
2. doc438/439、三个 implementation/test blob、#498/#499/#501 与完整资格 evidence continuity；
3. Python 3.10.6 / 3.13.13 × normal / `-O` 的 documentation/Markdown/hygiene bounded witness；
4. read-only global/local hygiene、`git diff --check`、forbidden public export guard 与 primary `audit.json` continuity；
5. original publication PR gate只认本 candidate exact head/tree/attempt；
6. protected merge 后只认新的 merge SHA 与 new exact-main Public CI 15/15 + Browser Smoke 1/1；
7. 从该新 exact main 重建 exact-source wheel negative lifecycle，另做 installed P1 API 与
   README/doc437/doc438/doc439/本文/milestones raw/API/exact-Git byte observations；不得拿公开 0.1.0 的未修正 P2
   product path冒充 source freeze witness；
8. independent source-byte/lifecycle/readback/retained-history reconciliation 与 finite closeout。

implementation full matrix 属于已资格化 doc439 exact source world；本 publication 不以 docs-only diff 伪造新的 runtime 语义。
Public CI 仍执行自己的完整原始门。任何 non-success 必须保留原 identity 并停止；不得 rerun until PASS、弱化 oracle、修改
doc439 或复用旧 PASS。

## 5. Candidate qualification pipeline

```text
publication final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original publication PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh exact-source wheel negative lifecycle
  -> fresh anonymous installed P1 API + README/doc437/doc438/doc439/doc440/milestones raw exact bytes
  -> independent source-byte / lifecycle / readback / retained-history reconciliation
  -> target IMPLEMENTATION_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication 自己的 fresh Plan/session/Evidence 不可复用 #501 world；diagnostic 不计入资格。raw/API byte observation 不冒充
Render completeness。worktree alignment与cleanup只属于housekeeping。

## 6. 当前 publication target 与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_CONTRACT_0_2_FROZEN
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED_NOT_AUTHORIZED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的 source `IMPLEMENTATION_FROZEN` target 成为事实。随后必须从新的 exact main 返回
CONTROL LOOP，独立决定 GitHub Evidence 0.1.1 public release contract、doc437 恢复与 Manifest 0.2 successor；不得按文档编号
自动启动任一能力。R1 完成后必须由人类与 AI 共同执行独立全项目检查。
