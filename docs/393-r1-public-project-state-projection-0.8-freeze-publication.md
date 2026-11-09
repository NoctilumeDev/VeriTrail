# R1 public project-state projection 0.8 freeze publication

日期：2026-11-09

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，两个目标都不是生效事实。
>
> 发布基线：`main@cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3`，tree
> `8b38acf9b4a6a061dd655fabd68c3353d4b1c50a`。
>
> 上游：[0.8 reconstruction contract candidate](392-r1-public-project-state-projection-successor-0.8-reconstruction-contract.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / COHERENT_CONDITIONAL_STATUS_PUBLICATION_ONLY`。本文不修改runtime、tests、fixtures、workflow、
> release-download recovery、Release资产、Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Slice/Coverage
> semantics、doc375–392历史字节、projection 0.7 frozen history或任何其他frozen contract。

## 1. CONTROL LOOP：为什么本publication必须同步project-state

PR #451已经使doc392与projection 0.8成为`QUALIFIED_CANDIDATE / NOT_FROZEN`。candidate资格只证明该有界阅读面在自己的
exact world内可消费，不自动产生frozen state，也不恢复global composition authority。fresh CONTROL LOOP重新读取exact main的
AGENTS、working method与hygiene，并绑定remote main、tree、open PR与primary audit：

```text
exact main     = cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3
tree           = 8b38acf9b4a6a061dd655fabd68c3353d4b1c50a
remote main    = cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3
primary audit  = sha256:4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c
```

没有新的产品或合同反例击穿0.8边界。现存open PR都是与本seam无关、基于更早坐标的dependency update，不能授予或阻断本
publication语义。当前唯一未闭合责任是qualified candidate与frozen public projection之间的publication lag。

PR #425/#426的历史反例已经证明：若publication只更新README、AGENTS、milestones与publication正文，却让
`docs/project-state.md`继续声明旧状态，即使自动门与marker observation全绿，也没有解决“公开投影内部自洽”这个原工程问题。因此
本publication的最小合法scope必须同步project-state。状态规则固定为：

```text
before every doc393 final gate closes = QUALIFIED_CANDIDATE / NOT_FROZEN
after every doc393 final gate closes  = FROZEN
```

该条件不是文档给自己授予状态；是否满足只能由本文声明的外部资格链与independent reconciliation决定。

## 2. Exact 0.8 candidate qualification

```text
PR                   = #451
base                 = 69c1832a560dc24e0d4ea06f5bd2d4198518accd
head                 = 445948db9cb03a5ddc81f3617ad897d303d6dc83
ordinary merge       = cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3
candidate/merge tree = 8b38acf9b4a6a061dd655fabd68c3353d4b1c50a
diff                 = 1 commit / 5 docs files
```

original Public CI `42619102447`、exact-main Public CI `42624859116`与Browser Smoke `42624859171`均attempt 1
SUCCESS，分别为11/11、11/11与1/1；没有rerun。local qualification、precommit seal、postcommit seal、original qualification、
protected merge与exact-main gate qualification SHA-256为：

```text
48d9f7988338cd668f9b397acdbcda63a599ac38d3ef1b2e9ce8eb5935c73900
a908566aad919a41db689031e3dc487a60a123726688462a0e64df981cbaa886
66ca9abe96fc6fd8c1dfdf4db648e21fe1352819a22caf94620a19bb0e14981f
bc5af90f30faf5d5e649e091b066eda4cf5a237cffb163e2b8f5db64840ecaa8
f5c0af6316d2611bb12a317a0a8aa6b40e8bd47367c8a05361dd3431dbab8000
2f76167e7622fdb599d9b6369f0f1e2fba9f42f00f6d445739f657424767dff6
```

fresh exact-main readback从全新Python 3.13 installed-product环境只认`cae001d…`world。README、project-state、doc376、doc390、
doc392各自在formal observation 1 PASS；doc391 formal observation 1由产品保留为Render `ERROR`，包含
`NAVIGATION_NOT_OBSERVED / NAVIGATION_PROJECTION_MISSING / RENDER_NAVIGATION_FAILED /
RESPONSE_BODY_OBSERVATION_FAILED`，lower cause `UNKNOWN`、cleanup complete且Core Verdict未创建。frozen postprocessor随后对
`facts.content=null`发生的`AttributeError`是独立setup error。doc391 diagnostic 2 COMPLETE后，formal observation 2才独立PASS；
后继PASS不删除、解释或回填observation 1。AGENTS与milestones各有唯一raw.githubusercontent、Contents API与exact Git全字节一致
observation。

independent reconciliation attempt 1只暴露synthetic proof-target token与公开文字表达不一致的setup error；attempt 2按实际
`projection/contract 0.7 + FROZEN HISTORICAL`语义重新绑定后PASS。preformal validation、adapter freeze、independent reconciliation、
187-artifact closeout与finite integrity SHA-256为：

```text
2afa2b319648f5f9b6495d9be85739361dc45a39e7f106e744d073ae2c41edd5
2a69bbbef80cf83334b149c50fc54cf3f10d0142fc7d95a05995402400f8d5d8
3f7241fbdd0fe60f28c9a8289d61cba38cab3bbd0ddb0da676b76bfa7a8b7a39
a1dddaf6df487c6781a9bd55843bf3115dde338abded3013961f573b13674751
179a8f5e5b8f056e5c41677ff0fa02c61d4514375c2cd332561eaf8c8477991f
```

所有local proof-target、PowerShell parser、API EOF、delayed session、output truncation、worktree attachment、Windows glob与
readback product/setup errors继续按原identity保留，qualification effect为`NONE`。PR #447/#448仍是closed/unmerged/original-gate
failures，#449只拥有maintenance资格；#451的PASS不回填或解释它们。

## 3. Final same-candidate milestones binding

本publication先完成milestones final bytes，再机械写入本页与project-state；milestones不记录自己的摘要，因而没有自引用：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 692175
sha256    = 612c67a3d65f739921d31e0d71c23f0039503acece868d5a22897fd2e824de3e
blob_sha1 = 856459d50516de0244730a3ffd63d6df78fb3525
```

project-state必须继续小于65536 UTF-8 bytes，不复制完整milestones，也不能把上述binding冒充资格或状态权威。

## 4. 问题连续性与权威边界

本publication机械分开并绑定：

```text
original engineering problem = 维护准确、自洽、可公开观察且不越权的bounded current-state projection
current proof obligation      = 0.8 frozen-status publication的全部最后门与跨表面一致性
applicability world           = exact base cae001d/tree 8b38acf、本candidate final bytes、attempt与fresh readback identity
proof_is_not_problem_solving  = true
```

marker presence与CI绿灯都只是bounded witness，不能替代跨文档状态一致性。Reality仍拥有现实事实；人类授权者仍拥有目标、验收前提与
必要Seal决定；Provider只拥有实际观察及来源；Business Layer不能裁定证据充分性或宣布PASS；Core裁决证据完整性、绑定、充分性与
确定性，但不成为现实事实的超级所有者。

`PROJECTION_0_8_FROZEN`不把projection变成source of truth、scheduler、qualification authority或施工授权，不证明完整Review产品，
也不恢复global composition authority。

## 5. Exact scope与最后门

本docs-only candidate只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/project-state.md
docs/393-r1-public-project-state-projection-0.8-freeze-publication.md
```

doc375–392、runtime、tests、fixtures、workflow、release-download recovery、Release资产、Schema、Provider、Collector、P2/Core
oracle、Verdict、`audit.json`与全部frozen semantic bytes必须保持base不变。

本层local gates重核exact scope、final milestones binding、project-state小于65536 bytes、UTF-8/LF/final LF、links/fences/headings、
required markers、#451 qualification evidence、#447/#448 retained original failures、#451 retained doc391 readback error、
`git diff --check`、global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc376 / doc390 / doc391 / doc392 / doc393 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / problem-identity / retained-history reconciliation
  -> conditional target PROJECTION_0_8_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可由#451 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。

## 6. 条件化target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN_HISTORICAL
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_PR447_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FAILURE_AUDIT_PR448_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_RELEASE_ASSET_RECOVERY_PROOF_FACILITY_SUCCESSOR_V2_PR449_EXACT_MAIN_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_0_8_DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后，本文开头的两个conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，重新判断下一最小合法
seam；不得按文档编号自动恢复global composition authority或施工manifest、Evidence、persistence、public Review、R2–R6。
