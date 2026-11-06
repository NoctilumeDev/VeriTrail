# R1 public project-state projection 0.3 冻结发布

日期：2026-11-06

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，这两个目标都不是生效事实。
>
> 发布基线：`main@e5af3a0eecf8ef5b3a439bfe7f5948610c3834e6`，tree
> `643974d34df1829d2f4f10a40ffbf774262d6874`。
>
> 上游：[0.3 contract candidate](363-r1-public-project-state-projection-recovery-successor-0.3-contract.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改project-state、doc363、runtime、tests、workflow、Schema、
> Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #415已经把versioned projection 0.3 candidate精确合入新的main world；其local gates、original PR gates、protected
exact-head merge、new exact-main双门、fresh anonymous installed-product readback、independent reconciliation与finite closeout已经
全部成立。因此doc363与projection 0.3现在最多是：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified candidate不等于frozen projection。fresh CONTROL LOOP重新检查后，0.3仍是修复旧0.2 source binding与公开读回资格缺口的
最小边界；没有新事实授权回填#401/#402/#404/#405/#406、修改产品oracle、恢复global composition authority或启动后续runtime。

因此本文只承担一个职责：在自己的独立完整资格链闭合后，把固定doc363/project-state 0.3 semantic bytes从qualified candidate发布为
frozen public projection。本文不是roadmap scheduler，也不选择manifest、Evidence、persistence、public Review或R2-R6。

## 2. Exact 0.3 candidate qualification

```text
PR                   = #415
base                 = e5e8c8895e811f858850ae5f5094f7595eac9120
head                 = 8b60078f9fc90a9a685b843960f33a88a37d1e7e
ordinary merge       = e5af3a0eecf8ef5b3a439bfe7f5948610c3834e6
candidate/merge tree = 643974d34df1829d2f4f10a40ffbf774262d6874
diff                 = 1 commit / 5 files
```

original Public CI `42154452136`、exact-main Public CI `42158099293`与Browser Smoke `42158099307`均为attempt 1
SUCCESS，分别为11/11、11/11与1/1。local qualification、pre-PR seal、post-commit seal与original qualification SHA-256为：

```text
033abaf654e20a5a16e3c9378d262c0753a7703154fa2dab295e1a0e1563174c
c1434262af75d28b84ce9bb8b1b7f299ad065876b6a581cdee6205f303b95db7
f433b13204d0866b7e2e1ede525d8abe867ba1c56ca2888d66926fd7bbf0f5e5
318570e74e9a9cfae3532527e50ac3f9317943e6d798cde7aa6e4a18bc32c822
```

protected merge与exact-main dual-gate evidence SHA-256为：

```text
6743b91731a2aa77f7edbcfcff7050efc587c9b10a15f405162ab1ab6301c599
2da281dfcd91f2554f0111e2f17f60e0877a1e8758dde3012758c6eb9f88cb55
```

0.3 source milestones binding已经在candidate local qualification与合入后exact Git world重新复算：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 599729
sha256    = 4ad66def6e220eca45c334f65222022f5d5ace0ea5ad458873082acd0bd85fec
blob_sha1 = b2b983cacde0a6990d394a1087d92a3b78c83291
```

`docs/project-state.md`为7088 UTF-8 bytes，继续小于65536-byte contract上限。它没有复制完整milestones，也没有给自己授予状态、
qualification或scheduler authority。

## 3. Fresh exact-main installed-product readback

fresh evidence只认`e5af3a0…`world、Core 0.13.0、GitHub Evidence 0.1.0、Playwright 1.62.0与matching Chromium；公开
wheel只复用重新校验的immutable release bytes。所有产品调用清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令
注入。

三个早期root按原身份永久保留，且没有任何PASS被后继资格复用：

1. `project_state`被原样嵌入Plan ID，underscore违反released Core identifier grammar；formal未启动；
2. 改成`project-state`后diagnostic Plan ID长度为65，超过64上限；formal仍未启动；
3. 改成短内部key `state`后diagnostic Render为`COMPLETE / 200`，但唯一formal API命中
   `403 / COLLECTION_BUDGET_EXHAUSTED / remaining=0`，Render仍`COMPLETE`且Core Verdict未创建。

这些都是独立的proof-facility或anonymous resource identity。第三项正式失败不证明subject failure或candidate regression；它也没有被
后来的PASS解释成未发生。reset以后建立第四个fresh root，从空history重新运行全部目标，不复用任何先前README PASS。

第四个root中README、project-state、doc349、doc350、doc362与doc363各自的唯一formal均为API/Render `COMPLETE`、HTTP 200、
marker一次、cleanup complete与Core `PASS`；AGENTS/milestones各自的raw.githubusercontent、GitHub Contents API与exact Git
bytes逐字节一致。milestones观察再次得到599729 bytes、SHA-256 `4ad66d…`与blob SHA-1 `b2b983…`。

pre-observation adapter、independent reconciliation、184-artifact finite closeout、保留的stdout self-capture mismatch与finite
integrity SHA-256为：

```text
312c82e3c9410f6f6234f25798f0fa6265ff326187a0f9048ad85e856ba4d702
666383ffc709db2d3a78b0ef613ae6c1df71f010ea0949917a9f95dda9173dbb
1289a5a9cba5f14b30dc66e03e7bf5d43e7ff2d97ce4e9acf4da5640325b40c4
674826ee178624be561f9efc9f8c1777966b32661d0706d9931a56900e5ccb0c
0ff972fde5a1477fd4ec6c35ceb911de4a0ad4661824704870ffb39b277f59d1
```

第一次anonymous rate diagnostic/API preflight的later reset、第二次diagnostic/preflight的PASS、两个Plan-ID setup errors以及formal
rate-exhaustion error全部进入finite evidence；later PASS不覆盖它们。

## 4. 冻结对象与权威边界

本文最终发布的semantic对象是doc363定义并由`docs/project-state.md`承载的：

```text
projection contract = R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3
binding kind        = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source milestones   = 599729 bytes / sha256:4ad66def… / blob:b2b983ca…
```

冻结以后仍必须保持：

- Reality拥有现实事实；人类授权者拥有目标、验收前提与必要Seal决定；
- Provider只拥有自己实际观察的事实与来源；R/Q/O/T只拥有各自冻结合同职责；
- Business Layer可以组织流程、选择能力和请求补证，但不能裁定证据充分性或宣布PASS；
- Core拥有证据完整性、绑定、充分性与确定性裁决，但不成为现实事实的超级所有者；
- milestones继续拥有完整append-only工程历史；project-state只提供小于65536 bytes的有界reader projection；
- 任一source milestones bytes或current effective state变化都要求新的versioned projection/rebind；
- 验迹的最终优化目标始终是用户提出的工程问题，而不是插件或Provider自身的存在价值。

`PROJECTION_0_3_FROZEN`不把projection变成source of truth、scheduler、qualification authority或施工授权，也不恢复被显式停止的
runtime seam。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。project-state、doc363、runtime、tests、
workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
required markers、doc363 qualified-candidate evidence continuity、retained failure identities、`git diff --check`、read-only global/local
hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc363 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / identity / retained-history reconciliation
  -> target PROJECTION_0_3_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可由#415 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。
本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_2_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后，本文开头的两个conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，重新判断下一最小合法
seam；不得按文档编号自动施工manifest、Evidence、persistence、public Review或R2-R6。
