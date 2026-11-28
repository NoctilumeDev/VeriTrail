# R1 global composition authority contract冻结发布

日期：2026-11-28

> 条件化状态目标：`R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@5d06cbe831015aff56cde6b6263c1de2bf780d64`，tree
> `bcc74c41c140dc34a70e6a5a1839a3d743fe9ac2`。
>
> 上游：[global composition authority当前状态审计](462-r1-global-composition-authority-current-state-audit.md)与
> [versioned global composition authority contract](463-r1-versioned-global-composition-authority-contract.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改runtime、Schema、fixture、test、workflow、oracle、
> private implementation、Core Verdict或任何public产品面；只在自己的完整资格链闭合后发布doc463中同一
> `R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1`合同的`FROZEN`状态。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #528把doc463精确合入：

```text
base                 = 49a07ed029c15c5312a29aa0ef5f194ae3252489
head                 = 03e4375969077c625c8b4b72a19ae64f46a3e6f2
candidate/merge tree = bcc74c41c140dc34a70e6a5a1839a3d743fe9ac2
ordinary merge       = 5d06cbe831015aff56cde6b6263c1de2bf780d64
diff                 = 1 commit / 4 files
```

三个远端门只认各自original attempt，没有rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #528 original Public CI | `46077691048` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `46082842779` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `46082842666` | 1 | 1/1 SUCCESS |

candidate local evidence seal、post-commit seal、original qualification、protected merge与exact-main dual-gate record
SHA-256依次为：

```text
0da69c1ab7fcda82154661307b852d02fc36df09d068fde9b03c53c781a1828a
31de9d5f5c76b9b35b2829398ccd2f14ec17b862e4259e696ef0c3e524a9df00
b3b42c1f1675dda42b42efe7941e1851d3287b24968b97ef821c88c029903020
5891ea5e2fb4951a011346a6ff87cb42147e34dd5ba8764262009fb98d712db5
a5bce75119e9680a4f15f86947460a42ce53e5299307f79b609d59c1c84d8bb3
```

fresh installed-product world只认`5d06cbe...`。README、doc462与doc463各有唯一qualifying anonymous Render
formal，均为API/Render `COMPLETE`、marker唯一与Core `PASS`；AGENTS与milestones各有唯一qualifying anonymous
raw/API/exact-Git byte PASS。independent reconciliation、144-artifact finite closeout与post-closeout integrity SHA-256依次为：

```text
80b62eba0e59bfbf8de1b16122b4757cafa7a643a0a97d6a43014bb0fb606c95
f86d8d897155c34e0b908e16568128b5fd63f32d8a40dac38fe4e70d292ae071
267c044d2e416b95eb0e33a0603ca43018fca8a975c48b4f092dbcbd2f9033cd
```

因此当前最多是：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_CANDIDATE_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
```

fresh CONTROL LOOP没有发现需要扩大doc463、重开doc462或修改产品字节的新反例。下一最小合法seam只是新的docs-only
资格链，用来发布同一合同的`FROZEN`状态；它不自动授权private implementation或public Review。

## 2. 本publication冻结的exact合同

本文若完成自己的资格链，只冻结doc463中的以下合同身份和边界：

```text
contract identity = R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1
owner identity    = veritrail.review.global-composition-owner/0.1
```

冻结内容是：唯一private owner绑定sealed input、ReviewPolicy、Review Profile、Provider roster、一个live
`BudgetContext`与同attempt capture slot；它按冻结顺序运行八个live worlds，传播最早failure，闭合owned resource，随后把同一attempt
结果交给独立one-shot private admission。四个normal world与四个qualified negative world必须共用同一生产顺序与失败语义；qualified
negative是完整成功结果，不是unsafe、interrupted、cleanup-failed或缺证据world的别名。

权威边界保持不变：Reality拥有现实事实；Provider只拥有自己实际观察到的事实与来源；R/Q/O/T各自在冻结合同内分析、观察或调度；
private global owner只组织流程和能力选择；Core继续独占Evidence binding、integrity、sufficiency、determinacy与Verdict。Manifest 0.2
只运输role/path/digest，不复制事实、coverage、plan或裁决。业务层可以停止重复采集或请求补充条件，但不能自行宣布证据足够或`PASS`。

## 3. 明确不冻结和不授权的对象

本文不创建或授权：

- global owner runtime、public export、CLI、publisher、persistence或Core integration；
- public Review product、HumanDisposition automation或自动修复/行动层；
- 新Schema、Evidence字段、Manifest版本、Provider语义或Core Verdict优先级；
- R2–R6、开源外部系统集成或R1完成后的human+AI全项目复核。

```text
contract_frozen_target                    = conditional
private_implementation_started            = false
private_implementation_authorized         = false
public_review_product_started              = false
r2_r6_started                              = false
post_r1_human_ai_global_check_started      = false
proof_is_not_problem_solving               = true
local_not_global                           = true
```

只有本文资格化并使合同冻结后，新的CONTROL LOOP才可以独立审计private implementation feasibility。合同冻结本身不等于实现授权。

## 4. 必须继续保留的non-success

后继PASS不得删除、覆盖、改名或解释以下identity：

- doc462 audit attempt 1的普通模式AssertionError与`-O` false-PASS-shaped proof-facility缺陷；
- doc462 audit attempt 2缺少cross-cell semantic projection的proof-target gap；
- PR #527 readback README formal #1的anonymous rate exhaustion ERROR，以及preflight/formal出口桶差异和底层原因`UNKNOWN`；
- PR #528 fresh readback的worktree registration与唯一attach retry均因thread超过100个attachment identity失败；
- detached branch null `.Trim()`两次setup error、same-path delete/add patch原子拒绝、multi-file patch hunk syntax error与
  observe adapter expected-line patch setup error；
- README diagnostic #1把Markdown source link当作rendered text marker、diagnostic #2选择未进入稳定Render窗口的导航marker；
- doc462 diagnostic #1把Markdown heading的`# `语法当作rendered text marker；
- 上述三个diagnostic non-success均为HTTP 200与Render `COMPLETE`但marker 0；后继诊断PASS只证明修正后的proof target，
  不覆盖原identity；
- #528及全部更早的FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`。

primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 5. 本publication自己的资格责任

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc462、doc463、runtime、Schema、fixture、
test、workflow、oracle与primary `audit.json`必须保持base不变。

本层local gates重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. PR #528 exact base/head/tree/four-file diff、local/original/protected/exact-main gate evidence与fresh readback continuity；
3. Python 3.10.6 / 3.13.13 × normal / `-O`的bounded docs/roster witness；
4. doc463与当前private frozen source identities、`git diff --check`、global/local hygiene和primary audit continuity；
5. original publication PR gate只认本candidate exact head/tree/attempt；
6. protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
7. fresh anonymous installed-product README/doc463/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
8. independent contract-source/retained-failure/readback reconciliation与finite closeout。

PR #528 semantic matrix属于已经资格化的exact source world；本文不以docs-only diff伪造新的runtime语义。任何non-success必须保留原identity
并停止；不得rerun until PASS、弱化oracle、修改旧文档或复用旧PASS。

## 6. Candidate qualification pipeline

```text
publication final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original publication PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc463 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observation
  -> independent contract-source / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> target GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的Plan/session/Evidence不可复用#528 world；diagnostic不计入资格。worktree alignment与cleanup只属于housekeeping。

## 7. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CURRENT_STATE_AUDITED_QUALIFIED_HISTORY
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_CANDIDATE_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FREEZE_PUBLICATION_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN` target成为事实。随后必须从新的exact main返回
CONTROL LOOP，独立审计private implementation feasibility；不得按文档编号直接施工runtime、启动public Review、R2–R6、外部开源系统
集成或R1完成后的human+AI全项目检查。
