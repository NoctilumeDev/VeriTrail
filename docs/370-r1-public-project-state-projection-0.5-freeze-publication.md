# R1 public project-state projection 0.5 冻结发布

日期：2026-11-07

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_5_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，这两个目标都不是生效事实。
>
> 发布基线：`main@e132e422706fa96dfa1882587a726b9b48b072c2`，tree
> `76ea275a1253de5c16d64e30aff84356bae981ed`。
>
> 上游：[0.5 contract candidate](369-r1-public-project-state-projection-successor-0.5-contract.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改project-state、doc369、runtime、tests、fixtures、workflow、
> Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #421已经把versioned projection 0.5 candidate精确合入新的main world；其local gates、original PR gates、protected
exact-head merge、new exact-main双门、fresh anonymous installed-product readback、independent reconciliation与finite closeout已经
全部成立。因此doc369与projection 0.5现在最多是：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_5_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified candidate不等于frozen projection。fresh CONTROL LOOP重新检查后，0.5仍是修复0.4 exact-main gate failure与
readback-target regression之后，重新绑定current facts与完整milestones source bytes的最小versioned边界；没有新事实授权回填
#418/#419、修改产品oracle、恢复global composition authority或启动后续runtime。

因此本文只承担一个职责：在自己的独立完整资格链闭合后，把固定doc369/project-state 0.5 semantic bytes从qualified candidate
发布为frozen public projection。本文不是roadmap scheduler，也不选择manifest、Evidence、persistence、public Review或R2–R6。

## 2. Exact 0.5 candidate qualification

```text
PR                   = #421
base                 = 9b87e61ce3a361abaa3da458f49e43d5c5a1b769
head                 = 17f95c93bee1f9ee8208b022eba95494031b2984
ordinary merge       = e132e422706fa96dfa1882587a726b9b48b072c2
candidate/merge tree = 76ea275a1253de5c16d64e30aff84356bae981ed
diff                 = 1 commit / 5 files
```

original Public CI `42285479954`、exact-main Public CI `42289873310`与Browser Smoke `42289873689`均为attempt 1
SUCCESS，分别为11/11、11/11与1/1。local qualification、final diff review、pre-PR seal、post-commit seal与original
qualification SHA-256为：

```text
ef83522798f94a441960f304a2c6c0afdb342165ef6ff9af3d590c79c7c28440
981999108531a6928c8b8a3c86748a6347d48171c0188a350a6b54952fbb6e97
5c903d8a67c16e57177f30f95a84028caa9b0e78730a15c146caa700ffa41dea
a62e966ef883a9e1fbac4bd6bc37b7e255534664832cf7f606ed7ba13950c199
403a9b7a2d92bf942af4f87e770686e2579249fc518ad900e1a96de1da2f264b
```

protected merge与exact-main dual-gate evidence SHA-256为：

```text
f0f903695681275ce746ef575e388d3d7dbde2ff94c3730bc57d7b5d48f747ff
7768add0e50d723634c52bcd7f5231222c7ef2ee31febc280f06deb5c184b9a2
```

0.5 source milestones binding已经在candidate local qualification与合入后exact Git world重新复算：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 619569
sha256    = 65c7c362fcfc0c2831bb7e60fc738b0d7278b37a4b4c2c5b8b83ae10425de7bd
blob_sha1 = a0d02fe3d24b855ed9609b0a8ac71bf1af814edc
```

`docs/project-state.md`为9426 UTF-8 bytes，继续小于65536-byte contract上限。它没有复制完整milestones，也没有给自己授予
状态、qualification或scheduler authority。

## 3. Fresh exact-main installed-product readback

fresh evidence只认`e132e42…`world、Core 0.13.0、GitHub Evidence 0.1.0、Playwright 1.62.0与matching Chromium；公开
wheel只复用重新校验的immutable release bytes。所有产品调用清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令
注入。

README、project-state、doc366、doc367、doc368与doc369各自只运行一次diagnostic与唯一formal。六项formal均为API/Render
`COMPLETE`、HTTP 200、marker一次、cleanup complete与Core `PASS`。AGENTS与milestones各自的raw.githubusercontent、GitHub
Contents API与exact Git bytes逐字节一致；milestones观察再次得到619569 bytes、SHA-256 `65c7c…`与blob SHA-1 `a0d02f…`。

anonymous rate diagnostic与API preflight分别只运行一次，观察到remaining 20与19；它们是non-qualifying setup observations，
没有替代产品formal。pre-observation adapter、preformal validation、independent reconciliation、178-artifact finite closeout、
expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
ba78110166a853dbc18f2e6bc05a442d5558ef68478cd52a63be02eea7b45e6c
72226da9cb590f342f84ada0008f02c52b64a452d656ed8bee196f7dcfb8c56e
50150e30c42e7a3159881ff0bc305589bade090916f60f4f7a32fe30ca708052
69396023c244221bcbf41b17683f14c4af1332c873a0bf8bc3eaf361be176297
eb84799ed5175d78435073769cd0a0be4ccc4c2ba7ca66d20a075227d744c2d7
712a1d397c6049beac0cbf5513fff17cd3571d2727b0d60b8390c5770eb407e1
```

candidate阶段两次local proof-target setup error与一次PowerShell revision-brace setup error继续保留，qualification effect为NONE；
#418 exact-main failure、#419 marker/truncation failures、#420 plan-id与anonymous rate observations也都保持原identity。后继PASS不
删除、不解释或回填它们。

## 4. 冻结对象与权威边界

本文最终发布的semantic对象是doc369定义并由`docs/project-state.md`承载的：

```text
projection contract = R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5
binding kind        = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source milestones   = 619569 bytes / sha256:65c7c362… / blob:a0d02fe3…
```

冻结以后仍必须保持：

- Reality拥有现实事实；人类授权者拥有目标、验收前提与必要Seal决定；
- Provider只拥有自己实际观察的事实与来源；R/Q/O/T只拥有各自冻结合同职责；
- Business Layer可以组织流程、选择能力和请求补证，但不能裁定证据充分性或宣布PASS；
- Core拥有证据完整性、绑定、充分性与确定性裁决，但不成为现实事实的超级所有者；
- milestones继续拥有完整append-only工程历史；project-state只提供小于65536 bytes的有界reader projection；
- 任一source milestones bytes或current effective state变化都要求新的versioned projection/rebind；
- 验迹的最终优化目标始终是用户提出的工程问题，而不是插件或Provider自身的存在价值。

`PROJECTION_0_5_FROZEN`不把projection变成source of truth、scheduler、qualification authority或施工授权，也不恢复被显式停止的
runtime seam。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。project-state、doc369、runtime、tests、
fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
required markers、doc369 qualified-candidate evidence continuity、retained failure identities、`git diff --check`、read-only global/local
hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc369 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / identity / retained-history reconciliation
  -> target PROJECTION_0_5_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可由#421 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。
本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_5_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN_HISTORICAL
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后，本文开头的两个conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，重新判断下一最小合法
seam；不得按文档编号自动恢复composition authority或施工manifest、Evidence、persistence、public Review或R2–R6。
