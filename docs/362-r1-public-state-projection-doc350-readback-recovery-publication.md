# R1 public project-state projection doc350 readback recovery publication 0.2

日期：2026-11-06

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_2_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@605adc43602422361f52d1f62fc13b089177141a`，tree
> `6e5d67824b8431b7bbef539faf59b9d7049741a6`。
>
> 受审对象：doc350 failure-boundary audit 在新的 exact world 中的公开可观察性与资格恢复。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_RECOVERY`。本文不修改doc350、doc351、doc353、doc354、doc361、
> doc349、`docs/project-state.md`、runtime、tests、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict或任何
> frozen contract。

## 1. CONTROL LOOP 输入：旧失败不变，最小恢复责任仍成立

[文档361](361-r1-public-state-projection-doc354-readback-recovery.md)已经在自己的exact world完成完整资格链。该新事实只使
doc361成为qualified history，不回填#405/#406，也不把更早的doc350或projection 0.2自动资格化。重新核对现有失败链后，没有
出现要求重开runtime、Collector、Core或oracle的新反例；当前最小合法seam仍是一个新的、versioned、docs-only publication，
重新发布doc350的failure-boundary audit责任并取得自己的资格。

本publication不是已关闭PR #404的rerun，也不复用其head、tree、attempt、readback plan或资格。0.1身份继续只属于原失败world；
本文使用0.2身份和新的exact coordinate。

## 2. doc350原world与readback失败永久保留

[文档350](350-r1-public-state-projection-successor-readback-failure-boundary-audit.md)由PR #402以candidate
`77c9140a736f95b311617e568ad06a5ce5f4b679`、tree `0ea5aaed6e0dfe50e6af2c50a7f7891108be8141`合入
`main@4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea`。original Public CI `41956025003`、exact-main Public CI
`41960100228`与Browser Smoke `41960100243`均attempt 1 SUCCESS。

fresh README diagnostic为`COMPLETE / HTTP 200`。唯一formal
`r1-psp-v2-readback-fb-audit-formal-readme-1-4fd9a78`也取得API/Render `COMPLETE`、marker一次、samples稳定与
cleanup complete；随后Acceptance Core在Verdict形成前持久化Evidence时，对271字符本地目标路径触发
`FileNotFoundError [Errno 2]`。formal因此是`FORMAL_READBACK_ERROR / VERDICT_NOT_CREATED`，doc350 formal与
AGENTS/milestones raw目标没有继续。

failure-boundary、93-artifact failed closeout与finite integrity为：

```text
6e33bedd7228ac7f080f9209374b9fa3671d8e12e6fb318832e943477e90e397
87592d66e1c3d3eed5e2ea5b73a60f3bbd90047c15416318a3b18ee04e31dd7e
35ea330b2d05646fbef5b7693fc78fa417526e1130419ed5b61f0d960396f6a6
```

legacy Windows `MAX_PATH`只保留为hypothesis；底层本地文件系统机制为`UNKNOWN`。后继短路径PASS不能解释或覆盖该失败。

## 3. 0.1失败candidate与后继failure-boundary链继续分离

旧doc350 recovery publication 0.1只存在于PR #404：

```text
base = da6a6b3e692bf2486ca428dd5ed9c2068918e982
head = 74ede8dff9fb4bf9a79b8749b5ed6f593f161371
tree = 2ae6b7bd3604397def22c88ac826b0ba236c287f
scope = README / AGENTS / unmerged doc352 / milestones
```

其original Public CI `41980701750` attempt 1终态为`CANCELLED`：required Python 3.10 job `127089895170`耗尽35分钟
outer containment budget。PR #404已关闭、未合并、未重跑；duration variance底层原因保持`UNKNOWN`。Python 3.13或后继PASS不能
与该run拼接。

[文档353](353-r1-public-state-projection-doc350-recovery-original-gate-cancellation-boundary.md)保存该cancellation；它自己的
README readback后来暴露source marker一次、rendered marker零次。[文档354](354-r1-public-state-projection-doc353-readback-marker-drift-failure-boundary.md)
保存该marker-drift边界，但#406 fresh formal又在Render COMPLETE时遇到anonymous API
`403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0`，Core Verdict未创建。#405/#406及所有未运行目标继续保留原身份。

## 4. #413/doc361提供的新最小事实

doc361由PR #413以exact candidate：

```text
base = 4ba50edff463e9f9c0560abd17d502ebc5c4ce92
head = 5486c607f7a2aba88547f5c36331a0031d79f50b
tree = 6e5d67824b8431b7bbef539faf59b9d7049741a6
merge = 605adc43602422361f52d1f62fc13b089177141a
scope = README / AGENTS / doc361 / milestones
```

original Public CI `42125438657`、exact-main Public CI `42129541345`与Browser Smoke `42129541284`均attempt 1
SUCCESS（11/11、11/11、1/1）。fresh README/doc361各自唯一formal为API/Render `COMPLETE`、Core `PASS`；
AGENTS/milestones各自唯一raw/API/exact-Git观察逐字节一致。

anonymous rate diagnostic #1/#2及preflight #1/#2的zero-capacity结果、adapter path假设setup error与第一次reconciliation allowlist
setup error均按原identity保留，qualification effect为`NONE`。新编号#3恢复后没有重跑任何PASS。independent reconciliation、
112-artifact closeout、expected stdout self-capture mismatch与finite integrity为：

```text
f39cf6c6689bcec2d1a6e5feb7487fbce5585456fb1633f28193bd678e750354
bea8fdb91f7161c5edbf5ab6ac918036449d87da85e1851db3408d8556570b0c
9a0c56c99333de45ccb976883809c3b4fef1ba1ff3c73b07aae1ccfd91d501ad
2246c477b95aabe075991474bc4a3cab2cdcfc7028b855a2093300a2b22aba6b
```

因此doc361是`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY`。它只解除建立本文的
阶段停止线，不把任何旧world重写为PASS。

## 5. versioned recovery 0.2的最小边界

本publication固定以下边界：

1. doc350/doc351/doc353/doc354/doc361/doc349与project-state bytes保持不变；
2. #402的271字符失败路径、partial Bundle、failed closeout、`MAX_PATH` hypothesis与`UNKNOWN`永久保留；
3. #404的`CANCELLED / CLOSED / UNMERGED / NOT_QUALIFIED`身份永久保留；
4. #405 source/render marker contradiction与#406 API exhaustion、未运行目标和`UNKNOWN`永久保留；
5. 新world使用新的短evidence root，并在formal前机械核对最坏case acceptance-bundle path budget；
6. proof-facility path budget只约束本publication本地输出拓扑，不升级Core、Collector或产品语义；
7. 新formal继续要求API/Render `COMPLETE`、marker可见、Bundle完整持久化、Core Verdict `PASS`与cleanup complete；
8. 任一non-success按自己的identity保留并停止，不得换目录、重复target或借旧PASS拼接。

新的PASS若成立，只能证明doc350的审计责任在本publication exact world重新取得资格；不能证明#402或#404从未失败，也不能
使doc349/projection 0.2自动qualified或frozen。

## 6. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/362-r1-public-state-projection-doc350-readback-recovery-publication.md
docs/milestones.md
```

合入后只认新merge SHA，并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal；marker=`doc350 readback recovery publication 0.2` |
| doc350 | anonymous Public Render diagnostic + unique formal；重新证明被恢复审计正文可见 |
| doc361 | anonymous Public Render diagnostic + unique formal；绑定授权本文的qualified boundary |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致；不把raw bytes冒充Render COMPLETE |

所有render/raw target必须各有且只有一个qualifying PASS。fresh readback必须清除token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，只按命令使用代理。independent reconciliation必须核对base/head/tree、四文件scope、#401 marker failure、
#402 persistence failure、#404 cancellation、doc351/doc361 qualified history、primary audit continuity、path-budget preflight与全部
setup/non-success identity。

## 7. qualification pipeline

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、
`git diff --check`、global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O`
focused unchanged-runtime witness。

```text
final docs-only bytes / local gates / predeclared readback path budget
  -> original PR required gates (attempt 1; no rerun laundering)
  -> protected exact-head merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh six-target anonymous installed-product observations
  -> independent reconciliation + finite closeout
  -> R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_2_QUALIFIED_HISTORY
  -> return CONTROL LOOP
```

全部成立以前，本文只是一份candidate，doc350旧world继续`READBACK_NOT_QUALIFIED / NOT_FROZEN`。

## 8. 当前状态与停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_PR_404_CANCELLED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_2_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整闭合后也必须返回CONTROL LOOP，重新判断projection successor是否仍是最小合法seam。不得把doc350 recovery自动解释成
doc349/projection 0.2已资格化、private implementation已冻结、global composition authority已恢复，或runtime/manifest/Evidence/
persistence/public Review/R2–R6已获授权。
