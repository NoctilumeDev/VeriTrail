# R1 public project-state projection 0.6 冻结发布

日期：2026-11-07

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，这两个目标都不是生效事实。
>
> 发布基线：`main@69a17b2da86a2f4d9dd09e5ab5724e5fa0ec82e0`，tree
> `2898a6610e8a0ba05f9a9fe384179dd10d9f7fcf`。
>
> 上游：[0.6 contract candidate](372-r1-public-project-state-projection-successor-0.6-contract.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改project-state、doc372、runtime、tests、fixtures、workflow、
> Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #424已经把versioned projection 0.6 candidate精确合入新的main world；其local gates、original PR gates、protected
exact-head merge、new exact-main双门、fresh anonymous installed-product readback、independent reconciliation与finite closeout已经
全部成立。因此doc372与projection 0.6现在最多是：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified candidate不等于frozen projection。fresh CONTROL LOOP重新检查后，0.6仍是private dual-successor implementation冻结以后，
重新绑定current effective facts与完整milestones source bytes的最小versioned边界；没有新事实授权修改产品oracle、恢复global
composition authority或启动后续runtime。

因此本文只承担一个职责：在自己的独立完整资格链闭合后，把固定doc372/project-state 0.6 semantic bytes从qualified candidate
发布为frozen public projection。本文不是roadmap scheduler，也不选择manifest、Evidence、persistence、public Review或R2–R6。

## 2. Exact 0.6 candidate qualification

```text
PR                   = #424
base                 = 12d170633657871985727be6cf68d031534faf16
head                 = 5552df905fc36f6cb1351ee9be2777b92bb14bac
ordinary merge       = 69a17b2da86a2f4d9dd09e5ab5724e5fa0ec82e0
candidate/merge tree = 2898a6610e8a0ba05f9a9fe384179dd10d9f7fcf
diff                 = 1 commit / 5 files
```

original Public CI `42321856710`、exact-main Public CI `42325178086`与Browser Smoke `42325178091`均为attempt 1
SUCCESS，分别为11/11、11/11与1/1。local qualification、final diff review、pre-PR seal、post-commit seal与original
qualification SHA-256为：

```text
678edc175703ea05065a5e5e826d02a545b3e485f82107ae4fcf8c2758329c0f
9bc95b2780d6ea85bbac308487e8f68498f61f0d46345226d26e2e48bc360df1
bd04c4516e05ce7525c10152c28e0fe476f337995d02e6fe5ac45f0e0dc1505b
7f84eba50d27b5ade13a0a41a3af97c288ee0d2d6d3805cb1de78a4ab074444a
532e21b5e74d392b6c4bfa643734782e4b0d30963b3163c2d48a35c68370ac8d
```

protected merge与exact-main dual-gate evidence SHA-256为：

```text
7aebfdf47e24442ce6b694ef58098c52c9b829b327c415c8ce89f149d07d1af0
203b4718ba2d9eacd06cf4e2bd3f73f07e19dcfd1151966711e7edc63a9c18e3
```

0.6 source milestones binding已经在candidate local qualification与合入后exact Git world重新复算：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 627708
sha256    = b288c3e344e2cbb547bf0619799ae01f55213097550dd8535b8384f9324b6a77
blob_sha1 = e8cf9edd57a2f7935caaa3eedbc627fc81385165
```

`docs/project-state.md`为11269 UTF-8 bytes，继续小于65536-byte contract上限。它没有复制完整milestones，也没有给自己授予
状态、qualification或scheduler authority。

## 3. Fresh exact-main installed-product readback

第一个fresh evidence root只认`69a17b2…`world，但其formal proof facility在adapter freeze与anonymous preflight之后被发现仍把
Plan `change_scope.owner`绑定到上一轮private implementation freeze publication；observation identity与preflight provenance也保留
旧问题标签。该world在任何target diagnostic、formal或raw formal之前停止，Core Verdict没有创建。它不是产品失败，而是
`PROOF_FACILITY_IDENTITY_BINDING_ERROR / REJECTED_NON_QUALIFYING`；有限拒绝closeout SHA-256为：

```text
7c2e00440c72ec7e15b0d5b39b75eedad937b7130e87ce7945ddc0bf4fddb019
```

这个反例机械保存了原问题、证明义务与适用world的同一性要求：推导形式正确，不能替代“证明对象仍是用户当前要求的问题”。

第二个fresh root只修正上述proof identity binding，并从零重建Core 0.13.0、GitHub Evidence 0.1.0、Playwright 1.62.0与matching
Chromium installed-product environment。公开wheel只复用重新校验的immutable release bytes。所有产品调用清除token、`NO_PROXY`、
`PYTHONPATH`与`PYTHONHOME`，代理只按命令注入。

README、project-state、doc365、doc370、doc371与doc372各自只运行一次diagnostic与唯一formal。六项formal均为API/Render
`COMPLETE`、HTTP 200、marker一次、cleanup complete与Core `PASS`。AGENTS与milestones各自的raw.githubusercontent、GitHub
Contents API与exact Git bytes逐字节一致；milestones观察再次得到627708 bytes、SHA-256 `b288c3…`与blob SHA-1 `e8cf9e…`。

pre-observation adapter、preformal validation、independent reconciliation、176-artifact finite closeout、expected stdout
self-capture mismatch与finite integrity SHA-256为：

```text
7ce07b41960507a5f5b3634cf86b1328235fe9c9c8568a06ddc67ca3c643953a
005ec79ce5e5edfb135e1085eb668f85f2425cdfaeb3e3c58fe1d710e5666c94
4cacba33183de5e6fac2048b4cbe4769ea7e10b695ff23819bbcd9b52fd387e3
0f219a910409f73c00bb9f6cd18560bd7a81bf4df07427f2b2d7ca178c26395d
ab930bcee5ff1e7177bc57f336c70f5ac191801ebc4dced94b50da4753d64121
5c2803d1036c3490172eb231ee856957b918eaabdfbc53d2e28bd1a20db472d5
```

candidate阶段的PowerShell、marker proof-target与Codex sidebar attachment setup errors，PR #423首个README formal error，以及本轮
stale proof-identity world继续保留，qualification effect为NONE。后继PASS不删除、不解释或回填它们。

## 4. 冻结对象与权威边界

本文最终发布的semantic对象是doc372定义并由`docs/project-state.md`承载的：

```text
projection contract = R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6
binding kind        = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source milestones   = 627708 bytes / sha256:b288c3e3… / blob:e8cf9edd…
```

冻结以后仍必须保持：

- Reality拥有现实事实；人类授权者拥有目标、验收前提与必要Seal决定；
- Provider只拥有自己实际观察的事实与来源；R/Q/O/T只拥有各自冻结合同职责；
- Business Layer可以组织流程、选择能力和请求补证，但不能裁定证据充分性或宣布PASS；
- Core拥有证据完整性、绑定、充分性与确定性裁决，但不成为现实事实的超级所有者；
- original engineering problem、proof obligation与applicability world必须保持同一身份，形式证明不得静默更换研究对象；
- milestones继续拥有完整append-only工程历史；project-state只提供小于65536 bytes的有界reader projection；
- 任一source milestones bytes或current effective state变化都要求新的versioned projection/rebind；
- 验迹的最终优化目标始终是用户提出的工程问题，而不是插件、Provider或证明步骤自身的存在价值。

`PROJECTION_0_6_FROZEN`不把projection变成source of truth、scheduler、qualification authority或施工授权，也不恢复被显式停止的
runtime seam。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。project-state、doc372、runtime、tests、
fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
required markers、doc372 qualified-candidate evidence continuity、retained failure identities、`git diff --check`、read-only global/local
hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc372 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / identity / retained-history reconciliation
  -> target PROJECTION_0_6_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可由#424 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。
本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN_HISTORICAL
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后，本文开头的两个conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，重新判断下一最小合法
seam；不得按文档编号自动恢复composition authority或施工manifest、Evidence、persistence、public Review或R2–R6。
