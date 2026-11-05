# R1 public project-state projection failure-chain audit readback recovery 0.1

日期：2026-11-06

> 候选状态：
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@2270374bd288d34c35fe5848318b915d584a4156`，tree
> `2c2a66d4f6ffe628dac881352152bccb2a7844d5`。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只以新的exact world重发
> [文档358](358-r1-public-state-projection-failure-chain-audit.md)的联合审计责任，并绑定
> [文档359](359-r1-public-state-projection-failure-chain-audit-readback-rate-exhaustion-failure-boundary.md)已经完成的失败边界资格；
> 不修改doc358/doc359、workflow、runtime、tests、Schema、Provider、Collector、下载器、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict或任何frozen contract。

## 1. CONTROL LOOP结论：旧formal不重跑，联合审计用新publication重新受审

doc358由PR #410合入且original/exact-main双门成立，但它自己的唯一README formal在anonymous API额度耗尽时fail closed，
因此doc358与failure-chain audit始终是`MERGED / READBACK_NOT_QUALIFIED`。后继PASS不能写回#410，也不能继续其未运行目标后
拼接资格。

doc359只保存#410的新失败边界。它在PR #411的独立资格链最终闭合后成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。这项新事实允许新的versioned publication重新承担doc358的联合审计内容，
但不允许改变旧attempt、旧文档状态或`UNKNOWN`归因。

因此本candidate的最小职责是：以doc360的新字节、新PR、新merge与新fresh readback重新发布#406/#407/#408三条失败和
#409 maintenance qualification。它不是doc358 retry，也不从doc359继承readback authority。

## 2. 联合审计的四个独立world保持不变

| identity | exact coordinate | observed boundary | retained state |
| --- | --- | --- | --- |
| #406 / doc354 | merge `95add9053c2984c0efe0cb87d1a4b64812215683` | unique formal：API `403 / COLLECTION_BUDGET_EXHAUSTED`；同session Render COMPLETE | merged / readback NOT_QUALIFIED |
| #407 / doc355 candidate | head `ade665c3b4e760a57c2d2de4fb1c92fcd21d1b98` | Python 3.10 E1第6项asset连续HTTP 504并耗尽60秒恢复预算 | FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED |
| #408 / doc356 candidate | head `3409a0a5136d4578762a9a8c68b4bede2d73d52b` | E3首个plugin asset连续HTTP 504并耗尽60秒恢复预算 | FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED |
| #409 / doc357 | merge `fa26311fb156d2e07a79ecc76c8d8b5169f64891` | 两个multi-asset lane显式120秒；默认下载器与外层budget不变 | `RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN` |

#406 failure-boundary、failed closeout与finite integrity继续是：

```text
5f7abf1afbc8cef0430c19a9c2598ce54f25568d818b1789d95a41b3d803c994
049fc88c8aa3f4c379b3e2697d9ddc0a7b32f285acfd9661968d53bcaa294705
cbefd722d816d0d736cb575dd12469583267bfcf13fe610be595acbf62b4e29d
```

#407与#408各自的failure-boundary / failed closeout / finite integrity继续分别是：

```text
48c43a66843c6fdf010650b186c6b82e3773a79fe641e2b59cbb2aaf3cf3323e
c01e86ea670dc0a2d0de9bdfb1c7d2145fe8c0185c7590f595d6198baa7ef896
b010e77087f24330a168e48023b3708005bd163503bdb29d701ef8696bb5607c

032318a3eccfffd880943c31c9bda2ac4a6f87fe34883f492e4b6a14e0d4ada6
3114367067545beb3a9b9f2710e74c25d2587d884e742c75c3faaf475a29bcd8
0618adba88a223c04061e398cd1a3dacf9612fb0ba817c94b7c266ae5b105dda
```

#409的independent reconciliation、93-artifact closeout与finite integrity继续是：

```text
38f57c488fa9ab67ed5d5d42d056d2b8083142e2eba2e37db03c73f2ed135385
3828981eee1ae9458090a6f28a8d7ab42082584c35f518d8437c5cfa4cfff9e3
b13fe22900b2d939168e73a5ccf05136fa5081a93e27e6b4a610f38abf04187a
```

这些事实只允许并列，不允许把不同world的成功job、Render、download或maintenance结果拼成失败world的PASS。

## 3. #410失败保持原身份

PR #410的精确身份为：

```text
base = fa26311fb156d2e07a79ecc76c8d8b5169f64891
head = 9f7e0071178e0c9a9f5e62ac4c745a5d1cc2e47d
tree = fcce220c39605f316ad917e0457a072675901895
merge = c613129814cec4812066d747e34ebdb40e44fa03
original Public CI = 42084370751 / attempt 1 / 11 of 11 SUCCESS
exact-main Public CI = 42090149115 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42090149265 / attempt 1 / 1 of 1 SUCCESS
```

fresh README/doc358 diagnostics都是Public Render `COMPLETE / HTTP 200`。rate diagnostic #1与API preflight #1分别观察到
remaining 17与16；约43秒后的唯一README formal
`r1-projection-failure-chain-formal-readme-1-c613129`在同一session内取得Render
`COMPLETE / HTTP 200 / marker once / cleanup complete`，但API首个repository probe为
`403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0`，Core Verdict未创建。doc358 formal与AGENTS/milestones raw目标没有运行。

```text
failure boundary = 0d5cb71ca998418f286fb68607f650387f1b6fa1cee7459dfc65c2bb12996262
failed closeout = 2531254a857f1be4bd4c1ee9b44cb1b6fc2fc93c86e7967afd549b4f4f465143
finite integrity = ac8707c94a8248dcea037953e17d387daeace9be7f8cfc98d97b31e8aa04c612
underlying consumer / egress allocation cause = UNKNOWN
candidate semantic regression = NOT_ESTABLISHED
Collector regression = NOT_ESTABLISHED
```

本recovery不重跑该formal、不继续未运行目标、不使用认证替代，也不把任何新PASS回填给#410。

## 4. #411只资格化失败边界，并保留一次reconciliation defect

doc359由PR #411以以下坐标进入自己的资格链：

```text
base = c613129814cec4812066d747e34ebdb40e44fa03
head = 45d1738c8c22eb590d40e46ec0325cbfb8bb6d8d
tree = 2c2a66d4f6ffe628dac881352152bccb2a7844d5
merge = 2270374bd288d34c35fe5848318b915d584a4156
original Public CI = 42100538777 / attempt 1 / 11 of 11 SUCCESS
exact-main Public CI = 42105874643 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42105874834 / attempt 1 / 1 of 1 SUCCESS
```

fresh README/doc359 diagnostic均`COMPLETE / HTTP 200`，各自唯一formal均为API/Render `COMPLETE`、Core `PASS`；
AGENTS/milestones各自唯一raw/API/exact-Git观察逐字节一致。pre-formal rate diagnostic与API preflight分别观察remaining 55与54。

第一次independent reconciliation误把下一seam写成doc354 recovery，而doc359明确授权versioned doc358 recovery。该矛盾在
closeout以后发现，归层为`PROOF_FACILITY_RECONCILIATION_STALE_NEXT_SEAM_DEFECT`。以下字节永久保留为non-qualifying：

```text
attempt 1 reconciliation = 2ad99f53610265a469304be028995280263763529615e4fb860449157911a053
attempt 1 99-artifact closeout = 1d51cd28762f6ad1be24507b39c4c4d0048c1725f245008c74ab544fde4a4618
attempt 1 finite integrity = 2e1908610062b89f1226eaa77b387b96ee39d83a20dcf05bd156572b8c944de1
defect failure boundary = c0e5ffe01a83cc4d08706bcd804dc723a18cb8de9643bd31188e226d3550fd11
qualification effect = NONE
```

没有重跑任何产品diagnostic、formal或raw observation。纠正后的proof facility另行冻结，attempt 2只对相同immutable
observation artifacts重新reconcile并建立新的finite closeout：

```text
corrected adapter freeze = e5452bc773bc0bb949ded3b281a4a6c7ec606e9bab2baa1679d9d2b4474cdf21
attempt 2 reconciliation = 79f5de7c77181fef2667402fdf8b2c6752fc814eb269e2b9a01613e86efe17b2
attempt 2 118-artifact closeout = e4b3a78245cc5d04025f72c26068eeb7ffb56b792657bcf002863aa6b9f28f3e
attempt 2 self-capture mismatch = a40955f46cfcc99d3e9c1762d44834c211446cdea695491bf2cc207337d43aeb
attempt 2 finite integrity = 922beb2a662bdaf31bf893147c38a9e8e695fcd9c987f76ab986710715aa5392
```

因此只有doc359 failure boundary成为qualified history；doc358仍没有资格。

## 5. 本versioned recovery的authority上限

本candidate重新发布的对象是“#406/#407/#408分离失败 + #409 qualified maintenance”的联合审计责任。全部门闭合后，
允许的新事实仅为：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY
```

这不把doc358改名为qualified，不把#410 formal改成PASS，也不使doc354、projection 0.2、private implementation、global
composition authority、manifest、Evidence、persistence或public Review获得资格。它只恢复从新exact main建立versioned doc354
readback recovery publication的资格。

## 6. tracked scope与fresh公开观察

tracked scope只能是：

```text
README.md
AGENTS.md
docs/360-r1-public-state-projection-failure-chain-audit-readback-recovery.md
docs/milestones.md
```

合入后必须fresh观察：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；sealed reader-visible literal为`#410 readback rate-exhaustion failure boundary 已完成自身资格，failure-chain audit recovery 0.1 仍是候选` |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte equality；不得冒充Render COMPLETE |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte equality；不得冒充Render COMPLETE |

independent reconciliation必须复核#406–#411的exact identities、#411 corrected attempt 2、四文件scope、四个fresh observation、
primary audit continuity、旧non-success与本文authority上限。

## 7. 本candidate资格链

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、
`git diff --check`、global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O`
focused unchanged-runtime witness。测试只证明本docs-only candidate没有修改runtime，不解释旧失败的`UNKNOWN`。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 6
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一non-success都保留原身份并停止。本文形成新事实后必须返回CONTROL LOOP；不得按文档编号自动进入下一阶段。

## 8. 当前状态与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_PR_410_MERGED_READBACK_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED
RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部资格门闭合后下一步最多是从新的exact main建立独立、versioned doc354 readback recovery publication。不得回填#410、
重跑其formal、复用#411产品观察资格、弱化anonymous/API/Render/Core或raw-byte oracle、直接恢复projection/private
implementation，或启动manifest/Evidence/persistence/public Review/R2–R6。
