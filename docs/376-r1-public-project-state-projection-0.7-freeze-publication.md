# R1 public project-state projection 0.7 freeze publication

日期：2026-11-07

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_7_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，两个目标都不是生效事实。
>
> 发布基线：`main@84f1512b7ac59edcb3f180af1f6816d0dc7c96cb`，tree
> `77bae5ea781419676f3c015d1488ff4548001c0a`。
>
> 上游：[0.7 contract candidate](375-r1-public-project-state-projection-successor-0.7-contract.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / COHERENT_CONDITIONAL_STATUS_PUBLICATION_ONLY`。本文不修改runtime、tests、fixtures、workflow、
> Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、doc372–375历史字节或任何frozen contract。

## 1. CONTROL LOOP：为什么本publication必须同步project-state

PR #427已经使doc375与projection 0.7成为`QUALIFIED_CANDIDATE / NOT_FROZEN`。qualified candidate不等于frozen projection；
fresh CONTROL LOOP仍只允许独立docs-only freeze publication，不能自动恢复composition authority或启动后继runtime。

PR #425/#426已经证明一个四文件publication若只修改README、AGENTS、milestones与publication正文，而让
`docs/project-state.md`继续自称`NOT_QUALIFIED`，即使自动门和marker observation全绿，也没有解决“公开投影内部自洽”这个原工程
问题。因此本publication不能复刻doc373的scope。最小合法边界必须同步：

1. README的reader-visible current state；
2. project-state的version/status rule、上游资格与final milestones binding；
3. AGENTS与milestones的append-only事实；
4. 本publication的条件化target与完整最后门。

状态规则固定为：

```text
before every doc376 final gate closes = QUALIFIED_CANDIDATE / NOT_FROZEN
after every doc376 final gate closes  = FROZEN
```

该规则不是文档给自己授予状态；是否满足条件只能由本文声明的外部资格链与independent reconciliation决定。

## 2. Exact 0.7 candidate qualification

```text
PR                   = #427
base                 = 3bdf7cfd4d06d95955990f0336e098f5c27958a6
head                 = 53dce9a4260b6b7f8ddd72c99f1e96ca94f39605
ordinary merge       = 84f1512b7ac59edcb3f180af1f6816d0dc7c96cb
candidate/merge tree = 77bae5ea781419676f3c015d1488ff4548001c0a
diff                 = 1 commit / 5 files
```

original Public CI `42346423327`、exact-main Public CI `42348937241`与Browser Smoke `42348937213`均attempt 1
SUCCESS，分别为11/11、11/11与1/1；没有rerun。local qualification、final diff review、original qualification、protected merge与
exact-main dual-gate evidence SHA-256为：

```text
312c1997f87b23c7c80aec7ebf74d88d3cdd02893a2acae2735aa118cbf5e7b1
ffdf866765965aebd0b3397aa4a101b8089f669e163f76851aa4c93528c723fe
526aaeeb1832b4104716a61e1137eb0e6a3f97785eb96966ee2d7ae530fd4123
370820833c0ea0de4e68f21e19a75f7e6364ab84e9a3b1a9da92838fbf6d284a
5f96c3c25e1cb22fa0a59947ad170cb423bcce48f6add10450761199cea04a3f
```

fresh exact-main readback从全新Python 3.13 installed-product环境只认`84f1512…`world。README、project-state、doc372–375各有唯一
diagnostic与唯一formal；六项formal均为API/Render `COMPLETE`、HTTP 200、marker一次、cleanup complete与Core `PASS`。
AGENTS与637752-byte milestones各有唯一raw.githubusercontent、Contents API与exact Git全字节一致观察。pre-observation adapter、
preformal validation、independent reconciliation、182-artifact closeout、expected stdout self-capture mismatch与finite integrity
SHA-256为：

```text
0e1d66a41da128e122d55f5fb234129f5c62a2fd0ac3baf79a3274bf08aeaa3f
544eb2b4e275db3e37b30c5563be99982cf8c48eefe513df4aa1a7d0f6bf2cb7
1cf6c6bea3bbad58f34d9c8dbf173909d73c5c464df176ae5aa7792f4a5ce07f
f3eee941aabbba91dfbc268e0992eef0b08787da1db48aedcb8865d6c89bd859
9124c255dd1ebd3f18b1abc27424039a9e6ef3d6d4323250caf92e08af9f853b
aec6f6073a174cf0e36353a5863f877c5e6060c6a33277d7d03dff86efd61812
```

候选、fresh worktree与proof-facility setup errors继续按原identity保留，qualification effect为NONE。PR #425/#426的README/public
projection矛盾、未开始的formal/Core Verdict与failed closeout也继续保留；后继PASS不删除、不解释或回填它们。

## 3. Final same-candidate milestones binding

本publication先完成milestones final bytes，再机械写入本页与project-state；milestones不记录自己的摘要，因而没有自引用：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 640035
sha256    = 95a8548b812402ae476250f74bcc872eb90a20e9d5a222567c6b6764cf7c2e51
blob_sha1 = 6dd2e6ed6b3fd9cb2c63bc3414b53d7c5afa3390
```

project-state必须继续小于65536 UTF-8 bytes，不复制完整milestones，也不能把上述binding冒充资格或状态权威。

## 4. 问题连续性与权威边界

本publication机械分开并绑定：

```text
original engineering problem = 准确、自洽、可公开观察的有界project-state projection
current proof obligation      = 0.7 frozen-status publication的全部最后门与跨表面一致性
applicability world           = 本candidate的exact base/head/tree、final bytes、attempt与fresh readback identity
```

marker presence只是一项bounded witness，不能替代跨文档状态一致性。Reality仍拥有现实事实；人类授权者仍拥有目标、验收前提与必要
Seal决定；Provider只拥有实际观察及来源；Business Layer不能裁定证据充分性或宣布PASS；Core裁决证据完整性、绑定、充分性与确定性，
但不成为现实事实的超级所有者。

`PROJECTION_0_7_FROZEN`不把projection变成source of truth、scheduler、qualification authority或施工授权，不证明完整Review产品，
也不恢复global composition authority。

## 5. Exact scope与最后门

本docs-only candidate只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/project-state.md
docs/376-r1-public-project-state-projection-0.7-freeze-publication.md
```

doc372–375、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、`audit.json`与全部frozen
semantic bytes必须保持base不变。

本层local gates重核exact scope、final milestones binding、project-state小于65536 bytes、UTF-8/LF/final LF、links/fences/headings、
required markers、#427 qualification evidence、#425/#426 retained failure、`git diff --check`、global/local hygiene、focused
unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc373 / doc374 / doc375 / doc376 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / problem-identity / retained-history reconciliation
  -> conditional target PROJECTION_0_7_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可由#427 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。

## 6. 条件化target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_7_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FREEZE_PUBLICATION_MERGED_NOT_QUALIFIED_NOT_EFFECTIVE
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_READBACK_CONTRADICTION_CORRECTION_PUBLICATION_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_EFFECTIVE
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后，本文开头的两个conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，重新判断下一最小合法
seam；不得按文档编号自动恢复composition authority或施工manifest、Evidence、persistence、public Review或R2–R6。
