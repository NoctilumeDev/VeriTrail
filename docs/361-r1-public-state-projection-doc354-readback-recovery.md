# R1 public project-state projection doc354 readback recovery 0.1

> 状态：`CANDIDATE / NOT_QUALIFIED`
>
> candidate base：`4ba50edff463e9f9c0560abd17d502ebc5c4ce92`
>
> candidate base tree：`ee26ff57e7d6737e1a2d615633ebf2d93036a61b`

## 1. CONTROL LOOP 结论

doc360已经在自己的exact world完成完整资格链，形成新事实：failure-chain audit recovery 0.1可作为qualified history。
这不回填#406/doc354，也不授权沿用旧product observation。当前最小合法seam是一个新的docs-only publication：重发
doc354对#405 marker-drift失败边界的审计责任，并重新取得自己的资格。

本publication不重跑#405/#406，不修改旧文档状态，不解释匿名额度耗尽或底层网络归因，也不恢复public projection 0.2。

## 2. #405 marker-drift world继续保留

PR #405 candidate坐标为：

```text
base = da6a6b3e692bf2486ca428dd5ed9c2068918e982
head = 400d469b821d69816a17ccd7c060046ae66ccb45
tree = 1fe75d2b3431b04167fe87262a7bc27c67b3a2d3
merge = 6af0dac952ec2bd3e015bc827b2b709908282036
```

original Public CI `41987752615`、exact-main Public CI `41991308866`与Browser Smoke `41991308859`均attempt 1
SUCCESS。唯一README formal #3在API和Render均`COMPLETE / HTTP 200`、public bytes稳定的情况下观察到source marker一次，
但rendered text marker为零，因此在Core Verdict之前fail closed。该contradiction不能被后继PASS改写。

failure-boundary、failed closeout与finite integrity为：

```text
e393470939acc052a94f3ac44d89694b8a8012b0389e207912ba3658663d4c61
4165a90d119830e54aa91bcb6ab30306ac260b6e9bcf4a0a2633c0834e775737
aac1c1afe19b384857b7fabcc0966a52d7fbceb2085f6613247e798d1611f72a
```

## 3. #406/doc354 merged world继续保留

doc354 candidate与merge坐标为：

```text
base = 6af0dac952ec2bd3e015bc827b2b709908282036
head = a5dd28fa8b24b5517a09e5be9733e7e479658746
tree = 3619ceeba79145ebfe3af230e4ba22c89798c306
merge = 95add9053c2984c0efe0cb87d1a4b64812215683
```

original Public CI `42003156856`、exact-main Public CI `42007684666`与Browser Smoke `42007684466`均attempt 1
SUCCESS。original qualification、protected merge与exact-main gate record SHA-256为：

```text
ef8d0301a65d813db1038c7faa81cc8f8121075cccc0abd63b62ab15c35a08d3
8175e6d0291a6279635fc68e14eef83d2f7ad0541445fe9c13e178ecac8c508a
eebc5ea29f5019a63033efed0a585316afba2dd8d4261f57b2d50077944f34af
```

fresh readback唯一README formal在同一paired session内得到Render
`COMPLETE / HTTP 200 / marker once / cleanup complete`，但API首个repository probe为
`403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0`；Core Verdict未创建。doc354 formal与AGENTS/milestones raw均未运行。
它们不得被重跑、续跑或与后继world拼接。匿名shared-egress consumer或egress allocation底层原因仍为`UNKNOWN`；
candidate semantic regression与Collector regression均未建立。

failure-boundary、failed closeout与finite integrity为：

```text
5f7abf1afbc8cef0430c19a9c2598ce54f25568d818b1789d95a41b3d803c994
049fc88c8aa3f4c379b3e2697d9ddc0a7b32f285acfd9661968d53bcaa294705
cbefd722d816d0d736cb575dd12469583267bfcf13fe610be595acbf62b4e29d
```

## 4. #412/doc360提供的新最小事实

doc360由PR #412以candidate `7d4e499ebb317a67f121b4b9a299d96edccef82f`、tree
`ee26ff57e7d6737e1a2d615633ebf2d93036a61b`精确合入`main@4ba50edff463e9f9c0560abd17d502ebc5c4ce92`。
original Public CI `42113565597`、exact-main Public CI `42118009840`与Browser Smoke `42118009860`均attempt 1
SUCCESS。fresh README/doc360各自唯一formal PASS，AGENTS/milestones各自唯一raw/API/exact-Git逐字节一致。

independent reconciliation、98-artifact closeout、expected stdout self-capture mismatch与finite integrity为：

```text
cdf60f515fd1b1ade4773d5735d35e491ee92e520189c4ebc4381a9dd9be8937
9574b941a3163cce545fe0153672aa0cb66bc3ae2d6acc585245b327e4baf79e
ef24861ad4b5d367577c072d25e9630a30a81d8f3f73b0ecbf4c15f04d5e4165
e80e1c1f240f702bed74785650b587d60f02008ce92ac414521549331635cca2
```

该新事实只证明doc360自己的联合审计责任已资格化。它没有回填doc354，也没有解释#406的`UNKNOWN`。

## 5. authority与状态上限

本publication只拥有以下责任：

- 在新的exact coordinate重新发布doc354的marker-drift failure-boundary责任；
- 保持#405 source/render contradiction、#406 API exhaustion、未运行目标与`UNKNOWN`原身份；
- 明确doc354旧world继续NOT_QUALIFIED，后继资格只属于本publication；
- 维持public projection 0.2、private implementation、manifest/Evidence、persistence与public Review停止线。

它不拥有runtime、workflow、tests、Schema、Provider、Collector、P2/Core oracle或frozen semantics的修改权，也不能把
doc350或projection 0.2声明为qualified/frozen。

## 6. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/361-r1-public-state-projection-doc354-readback-recovery.md
docs/milestones.md
```

合入后只认新merge SHA。fresh installed-product readback必须清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，按命令
使用代理，对README与doc361各运行唯一formal，并对AGENTS/milestones各运行唯一raw/API/exact-Git一致性观察。任何
non-success保留原身份；不得重跑已有PASS或把不同world拼接。

## 7. qualification pipeline

本candidate必须依次完成：

```text
final bytes
  -> declared local qualification
  -> original PR gates
  -> protected merge
  -> new exact-main Public CI 11/11
  -> new exact-main Browser Smoke 1/1
  -> fresh installed-product observations
  -> independent reconciliation
  -> finite closeout
```

任一环节non-success都停止升级并按原身份保留。

## 8. 当前状态与下一停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication完整闭合后，最多成为
`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_RECOVERY_0_1_QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；
若无新反例，下一最小seam最多是独立versioned doc350 readback recovery publication。不得直接恢复projection 0.2、
private implementation或任何后续runtime seam。
