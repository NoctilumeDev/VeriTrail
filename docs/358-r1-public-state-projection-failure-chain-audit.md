# R1 public project-state projection failure-chain audit

日期：2026-11-06

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@fa26311fb156d2e07a79ecc76c8d8b5169f64891`，tree
> `b35a265d341f68bd16f6bca2ebc642446c0969fe`。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只发布三个分离的失败world与一个后继maintenance
> qualification；不修改workflow、runtime、tests、Schema、Provider、Collector、下载器、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict、既有文档或任何frozen contract。

## 1. CONTROL LOOP结论：联合发布，不拼接资格

PR #406、#407、#408与#409拥有不同的commit、tree、attempt与责任。#406已合入，但fresh installed-product readback
失败；#407/#408都在original PR gate失败后关闭、未合并；#409只修正两个multi-asset lane的显式可用性恢复窗口，
并完成自己的资格链。

| identity | exact coordinate | observed boundary | state |
| --- | --- | --- | --- |
| #406 / doc354 | merge `95add9053c2984c0efe0cb87d1a4b64812215683` | anonymous API `403 / COLLECTION_BUDGET_EXHAUSTED`；同session Render COMPLETE | merged / exact-main gates PASS / readback NOT_QUALIFIED |
| #407 / doc355 candidate | head `ade665c3b4e760a57c2d2de4fb1c92fcd21d1b98` | Python 3.10 E1 asset HTTP 504 recovery budget exhausted | FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED |
| #408 / doc356 candidate | head `3409a0a5136d4578762a9a8c68b4bede2d73d52b` | E3 first asset HTTP 504 recovery budget exhausted | FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED |
| #409 / doc357 | merge `fa26311fb156d2e07a79ecc76c8d8b5169f64891` | two explicit 120-second multi-asset lane windows | `RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN` |

本审计把相关事实放进同一reader-visible publication，但不把Render COMPLETE与API ERROR拼成PASS，不把不同run的成功job
拼成required gate PASS，也不把#409的PASS回填#407/#408。

## 2. #406：fresh anonymous API额度耗尽

#406的original Public CI `42003156856`、exact-main Public CI `42007684666`与Browser Smoke `42007684466`均为
attempt 1 SUCCESS。唯一README formal `r1-psp-doc353-readback-fb-formal-readme-1-95add90`在同一
`collection_session_id=github-paired-3d57f5f3e9c6484e9739f8082e5e0f1a`中观察：

```text
API = ERROR / HTTP 403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0
Render = COMPLETE / HTTP 200 / marker once / three stable samples / cleanup complete
Core Verdict = NOT_CREATED
formal qualification = ERROR / NOT_QUALIFIED
```

failure-boundary、92-artifact failed closeout与finite integrity SHA-256为：

```text
5f7abf1afbc8cef0430c19a9c2598ce54f25568d818b1789d95a41b3d803c994
049fc88c8aa3f4c379b3e2697d9ddc0a7b32f285acfd9661968d53bcaa294705
cbefd722d816d0d736cb575dd12469583267bfcf13fe610be595acbf62b4e29d
```

匿名shared-egress rate allocation或外部使用的底层原因仍为`UNKNOWN`。doc354、AGENTS与milestones目标在该formal失败后
未运行；不得在额度恢复后重跑同一formal或用认证观察替代。

## 3. #407：Python 3.10 E1资产下载失败

#407 original Public CI `42037283423` attempt 1的required job `127278597232`在第31步失败：前5项E1资产成功，
第6项`authoring-skill-e1-validation-summary.json`连续观察6次HTTP 504，60秒绝对恢复预算不能支付下一次
16秒capped backoff，E1 clean install与后续1项资产未运行。下载器没有接受错误字节、覆盖既有文件或遗留owned partial。

```text
classification = RELEASE_ASSET_HTTP_504_RECOVERY_BUDGET_EXHAUSTED
download tool = FAIL_CLOSED / CONFORMING
candidate semantic/docs failure = NOT_ESTABLISHED
underlying GitHub/proxy/shared-egress/network cause = UNKNOWN
```

failure-boundary、failed closeout与finite integrity SHA-256为：

```text
48c43a66843c6fdf010650b186c6b82e3773a79fe641e2b59cbb2aaf3cf3323e
c01e86ea670dc0a2d0de9bdfb1c7d2145fe8c0185c7590f595d6198baa7ef896
b010e77087f24330a168e48023b3708005bd163503bdb29d701ef8696bb5607c
```

Python 3.13、E3与Workbench的同run成功只作上下文；四个downstream required job的`SKIPPED`保持原结论。

## 4. #408：E3首项资产下载失败

#408 original Public CI `42045973076` attempt 1的required E3 job `127308876973`先成功下载Core wheel，随后首个
E3资产`veritrail_starter-0.2.0-py3-none-any.whl`连续观察6次HTTP 504，同样由60秒绝对预算停止；其余6项
E3资产与clean install未运行。其他10个job SUCCESS不能与该required job拼成11/11。

failure-boundary、failed closeout与finite integrity SHA-256为：

```text
032318a3eccfffd880943c31c9bda2ac4a6f87fe34883f492e4b6a14e0d4ada6
3114367067545beb3a9b9f2710e74c25d2587d884e742c75c3faaf475a29bcd8
0618adba88a223c04061e398cd1a3dacf9612fb0ba817c94b7c266ae5b105dda
```

#407与#408的HTTP状态、停止owner和归因上限相同，但run、job、head、asset与上下文不同；两条失败均永久保留。

## 5. #409：最小lane maintenance已经独立资格化

[文档357](357-release-download-multi-asset-lane-budget-correction.md)只让E1与E3 multi-asset loop显式传入120秒；下载器
默认60秒、15秒单请求、`2/4/8/16` capped backoff、retryable集合、owned partial、摘要、不覆盖发布与35/15分钟
外层containment budget均保持不变。

```text
candidate base = 95add9053c2984c0efe0cb87d1a4b64812215683
candidate head = aa037bd2b3aeb1e8c5c58b2ce6ba5b766ee14bad
candidate tree = b35a265d341f68bd16f6bca2ebc642446c0969fe
original Public CI = 42065715143 / attempt 1 / 11 of 11 SUCCESS
protected merge = fa26311fb156d2e07a79ecc76c8d8b5169f64891
exact-main Public CI = 42071677326 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42071677329 / attempt 1 / 1 of 1 SUCCESS
```

fresh installed-product README/doc357 formal均为API/Render`COMPLETE / PASS`；milestones raw/API/exact-Git全字节相等。
independent reconciliation、93-artifact closeout与finite integrity SHA-256为：

```text
38f57c488fa9ab67ed5d5d42d056d2b8083142e2eba2e37db03c73f2ed135385
3828981eee1ae9458090a6f28a8d7ab42082584c35f518d8437c5cfa4cfff9e3
b13fe22900b2d939168e73a5ccf05136fa5081a93e27e6b4a610f38abf04187a
```

anonymous rate diagnostic #1的`remaining=0`、reset后#2的`remaining=60`与closeout stdout self-capture mismatch均按
NON_QUALIFYING/NONE原身份保留。#409证明新exact world完成声明门，不解释#407/#408外部504的底层原因。

## 6. 归因上限与状态分离

```text
#406 anonymous API exhaustion = ESTABLISHED
#407/#408 release asset HTTP 504 recovery-budget exhaustion = ESTABLISHED
all three underlying external allocation/network causes = UNKNOWN
Collector/download fail-closed behavior = CONFORMING
candidate semantic regression = NOT_ESTABLISHED
#409 lane recovery 0.2 = FROZEN
doc355/doc356 candidates = UNMERGED / NOT_QUALIFIED
doc354 = MERGED / READBACK_NOT_QUALIFIED / NOT_FROZEN
projection 0.2 = NOT_FROZEN
```

内容正确、执行完成、资格成立、状态生效与下一步授权继续分开。maintenance qualified不等于失败审计qualified；本audit
qualified也不等于projection恢复。

## 7. 本审计的最小scope与公开观察面

tracked scope只能是：

```text
README.md
AGENTS.md
docs/358-r1-public-state-projection-failure-chain-audit.md
docs/milestones.md
```

合入后必须fresh观察：

| target | required observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；sealed literal为`#406/#407/#408 的三条失败边界已按原身份保留` |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte equality；不得冒充Render COMPLETE |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte equality；不得冒充Render COMPLETE |

independent reconciliation必须复核四个exact world、三条failure identity、#409全资格链、全部setup/non-success、四个fresh
observation、primary audit continuity与状态上限。

## 8. 本候选资格链与停止线

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、
`git diff --check`、global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O`
focused unchanged-runtime witness。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 7
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一non-success保留原身份并停止。全部闭合后本文也只成为qualified history；下一步最多从新exact main建立独立、
versioned doc354 readback recovery publication。不得重跑#406/#407/#408、复用doc355/doc356候选资格、弱化匿名/marker/
完整性oracle、修改primary audit、直接冻结projection/private implementation，或启动manifest/Evidence/persistence/public Review/R2–R6。

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_CANDIDATE_NOT_QUALIFIED
RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
