# R1 manifest carrier contract recovery reader-visible public-projection correction

日期：2026-11-17

> 候选状态：
> `R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@a8e7b096ac1820b254706ffd649957c10bdbcb27`，tree
> `462fc80e948de5dca5b35f84e6abdcb87a33ba5f`。
>
> 影响：`L0_PUBLIC_DOCUMENTATION + L3_QUALIFICATION_RECOVERY`。本文只校正当前合同状态在README默认读者可见区的投影，并为
> 该新world重新绑定fresh readback责任；不修改doc426合同语义、runtime、tests、fixtures、workflow、Schema、Provider、Collector、
> P2/Core oracle、Verdict、carrier、Manifest、persistence或public Review。

## 1. CONTROL LOOP结论

[文档427](427-r1-manifest-carrier-contract-recovery-reader-visible-failure-boundary-audit.md)已经在自己的exact world完成local、original
PR、protected merge、new exact-main双门、fresh installed-product readback、independent reconciliation与finite closeout。因此
`PUBLIC_READER_VISIBLE_PROJECTION_DEFECT`现在是qualified history；它没有回填[文档426](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)
的失败world。

重新核对原工程问题、当前证明义务与适用world后，没有出现要求修改合同语义、Collector、Core、runtime或tests的新反例。当前最小合法
seam仍是doc427预注册的独立docs-only public-projection correction：只让公开README准确显示doc427已资格化、doc426仍未资格化，并
在新的exact coordinate从零取得该公开投影自己的资格。

## 2. doc426失败world保持不可改写

PR #488 candidate与merge坐标为：

```text
base  = 663ca58054f56e8e3eada7ee2347225d0e9484e7
head  = c0fe7a218d1f60be9a1075c5837785b4ed1465db
tree  = 7f87e0e0624328168363db105237f0e84a27cad6
merge = 72b5e95ae30933d139967c94dc50f5c11c6c8a5b
```

original Public CI `43866121290`、exact-main Public CI `43872002039`与Browser Smoke `43872002011`均attempt 1 SUCCESS。fresh README
diagnostic的API/Render为`COMPLETE / HTTP 200`，但预注册reader-visible phrase出现0次；exact source证明doc426入口只位于默认折叠的
`<details>`内。source/readback contradiction与failed closeout SHA-256为：

```text
cb5a22d7a970f2a5bde22b2f9b21808cfd0a814092956a0e9f465bd158668991
bccf9b2ba20793628b3d583ea135538a5c14a55302029a1b85ab3d6882035ef6
```

formal、其他Render target与raw target在该world均未启动。doc426必须继续保持：

```text
MERGED / ORIGINAL_GATE_PASS / EXACT_MAIN_DUAL_GATES_PASS /
READBACK_NOT_QUALIFIED / NOT_FROZEN
```

后继PASS不能改写、解释或填补这个world。

## 3. doc427 qualified world与保留identity

PR #489 exact identity为：

```text
base    = 72b5e95ae30933d139967c94dc50f5c11c6c8a5b
head    = 63f6219b144cb108b47766ec9041d519eca4c269
tree    = 462fc80e948de5dca5b35f84e6abdcb87a33ba5f
merge   = a8e7b096ac1820b254706ffd649957c10bdbcb27
parents = 72b5e95ae30933d139967c94dc50f5c11c6c8a5b,
          63f6219b144cb108b47766ec9041d519eca4c269
```

original Public CI `43885662766`、exact-main Public CI `43892540882`与Browser Smoke `43892540898`均attempt 1 SUCCESS，分别为
15/15、15/15与1/1，没有rerun。original qualification、protected merge与exact-main gate seal SHA-256为：

```text
c504e5302c55f2eefeb3c119584b7842fe63c98a56f0a33e6f18730d60e7a829
bab7b73dc8982a6d2ae1a07a6e7218e79153dd829da879456666f9e33f20107b
7e5f37b7bfce288ce446e672b2a37b7ed3752bf3748624a88b6c5dea4e210979
```

fresh README/doc426/doc427各自唯一diagnostic与formal取得API/Render `COMPLETE`、marker一次、cleanup complete与Core `PASS`；
AGENTS/milestones各自唯一raw.githubusercontent、GitHub Contents API与exact Git观察逐字节一致。没有复用或重复任何旧PASS。

第一次independent reconciliation误把inline code中的`<details>`当成结构标签，在不重复产品观察的情况下保留为proof-target setup
error；versioned v2只识别行结构标签后通过。setup error record、v2 facility freeze、independent reconciliation、134-artifact
closeout与finite integrity SHA-256为：

```text
b779058a3cde590d10c9a493b6815b9c449f99ef3ab16899bb2e1216ab5756b6
41f1e939e56c8a6a5d7b3bc10df1ab6ca47b0a529af0e40a626333403e5df624
50ac845b3cb442adc8c177ac7259f51569b9e9961b4a09e680207d9d1572a007
745f1d0713defae1d74b0940847d4767c3646750e1b0825d737873bbda5f857d
f71b742d7b13c89d4396b2171f90b21bc8a55d97ffded8756b8c7a01214fe8f0
```

worktree attachment cap、PowerShell revision、Windows glob及expected stdout self-capture mismatch同样按原identity保留，effect为`NONE`。
因此doc427现在是`READER_VISIBLE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。

## 4. 本correction的精确边界

本candidate只建立以下公开投影：

```text
doc427 = READER_VISIBLE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
doc426 = MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN
public-projection correction = CANDIDATE / NOT_QUALIFIED
manifest carrier successor runtime = NOT_STARTED / NOT_AUTHORIZED
global composition authority = NOT_RESTORED / NOT_AUTHORIZED
language support qualification persistence = OPEN
public Review = NOT_STARTED
R2-R6 = NOT_STARTED
```

README默认读者可见区必须逐字包含以下未加折叠、未靠替代marker偷换证明对象的句子：

```text
Reader-visible correction: doc427 is qualified history; doc426 remains readback not qualified and not frozen.
```

该句只是准确投影现有qualified history与失败上限，不把公开可见性本身升级为合同资格、冻结或runtime authority。

## 5. 禁止的伪恢复

```text
rewrite doc426 as qualified or frozen
reuse PR #488 gates as doc426 fresh readback qualification
retry the failed doc426 diagnostic
open collapsed details only in the proof facility
choose a different visible marker while leaving the state inaccurate
splice doc427 readback with this candidate's future exact coordinate
modify runtime/tests/Schema/oracle/Collector to make a documentation problem disappear
infer carrier implementation or global composition authority from a corrected README
start public Review or R2-R6
```

理论遇到反例时先检查前提，而不是增加例外。本次只修正“raw link等于默认读者可见公开状态”这一错误前提对应的public projection责任。

## 6. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/428-r1-manifest-carrier-contract-recovery-reader-visible-public-projection-correction.md
docs/milestones.md
```

doc426、doc427、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、carrier、Manifest、persistence与
全部frozen semantic bytes必须保持`a8e7b096…` base bytes。

合入后只认新的merge SHA。fresh installed-product readback必须清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用代理，
并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal；验证第4节完整reader-visible state |
| doc426 | anonymous Public Render diagnostic + unique formal；只证明不可改写的合同正文可观察，不升级旧world |
| doc427 | anonymous Public Render diagnostic + unique formal；绑定已资格化failure boundary |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致 |

任何non-success必须保留原identity并停止；不得重复已有PASS或拼接不同world。independent reconciliation必须同时核对exact
base/head/tree、四文件scope、doc426 contradiction/failed closeout、doc427完整资格、README结构可见性、unchanged semantic files、
primary `audit.json` continuity与全部setup/non-success identity。

## 7. qualification pipeline

本candidate的第一次semantic comparator只移除了顶层runtime字段，却仍比较runtime-specific digest与exact-absence provenance；四个
单格报告各自成功，但摘要不一致，candidate validation因此fail closed。该proof-facility failure、失败semantic matrix与失败validation
分别按以下SHA-256保留，qualification与semantic effect均为`NONE`：

```text
8a7c410fd7b3e39c4199539613712e2cf1b2ec9850571a1fe330e7178c6f47ab
641255c87cc8b87cd7f39bb41ca6ff9758f9f17a329127de784467f1d313040a
54ff8b876b511e789c3db12cb9f4b0de355b70372ce9d0beef70f93a84cd3f5e
```

versioned v2沿用既有semantic projection，只比较authority、topology、availability shape、source hash与ceiling，并复用四个已生成的
单格报告；没有重跑semantic cell、focused test或hygiene。v2 semantic matrix PASS，focused四格各131项PASS，hygiene 8/8 PASS；
对应SHA-256为：

```text
1c3b267e700f41bcff1a9e7959a5c12857a1a3a5d3f39071ade2614b0ba30742
17cbb330baa02cea751b9110c1d391cd4f7bffe800d46adf31b14993ad9ee2d6
0cc35315a45623b6a21cc37e57e8c3c6b447f43276b8b8e52eef64a6c6b6716f
```

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、unique marker、exact scope、`git diff --check`、
global/local hygiene、primary `audit.json` continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O` focused unchanged-runtime witness。

```text
final docs-only correction bytes / declared local gates
  -> original PR required gates (attempt 1; no rerun laundering)
  -> protected exact-head merge
  -> new exact-main Public CI + Browser Smoke
  -> fresh six-target anonymous installed-product observations
  -> independent reconciliation
  -> finite closeout
  -> PUBLIC_PROJECTION_CORRECTION becomes qualified history at most
  -> return CONTROL LOOP
```

## 8. 当前状态与下一停止线

```text
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整闭合后也只允许成为
`R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_QUALIFIED_HISTORY`。随后必须从新的exact main
返回CONTROL LOOP，重新判断是重建doc426合同资格还是建立独立freeze publication；不得按文档编号自动施工runtime、恢复global
composition authority或启动public Review/R2-R6。

`proof_is_not_problem_solving = true`、`local_not_global = true`、
`post_r1_human_ai_global_check_required = true`；R1完成后仍必须由人类+AI共同执行独立全项目检查。
