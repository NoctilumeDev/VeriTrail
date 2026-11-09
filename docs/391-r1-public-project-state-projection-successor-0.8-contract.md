# R1 public project-state projection successor 0.8 contract

日期：2026-11-09

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@f2ab7b78f86a057431cf5c8f4cbc3b0337338118`，tree
> `280cbc4f54427b86b81854892af8a490559fed7d`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_VERSIONED_REBIND_ONLY`。本文不修改runtime、tests、fixtures、workflow、Schema、
> Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Slice/Coverage semantics、doc375–390历史字节、projection 0.7
> frozen bytes或任何其他frozen contract。

## 1. CONTROL LOOP输入：#446形成了0.7以后必须公开的新事实

projection 0.7由PR #427/#428完成candidate与独立freeze publication，当前继续是`FROZEN`历史。它在自己的exact world中准确，
但它的`当前有效事实`止于0.7冻结前后的状态，不能预先包含后来的application-level unified Review / Coverage output admission
合同、实现、失败边界、maintenance与最终freeze qualification recovery。

PR #446的exact identity为：

```text
base                 = 58ef15af9bfaec868439820de1b7bf0f5c5f27c7
head                 = 5cfce74ca85f58373212000d0f6eae219296a068
ordinary merge       = f2ab7b78f86a057431cf5c8f4cbc3b0337338118
candidate/merge tree = 280cbc4f54427b86b81854892af8a490559fed7d
diff                 = 1 commit / 4 docs files
```

original Public CI `42557756555`、exact-main Public CI `42560991201`与Browser Smoke `42560991124`均attempt 1
SUCCESS，分别为11/11、11/11与1/1；没有rerun。fresh exact-main只认`f2ab7b78…`world：README、doc389、doc390各有
唯一formal `PASS`，AGENTS与milestones各有唯一raw.githubusercontent、Contents API与exact Git全字节一致观察。

independent reconciliation、144-artifact finite closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
b0da3502dcc11b2f6593c31fa15844b59e431930c27176d1fb1a378b3d39593e
2bc7ef165aebb24d4a9dc329ab99da5316256828cf4d1a94c571a59b072f420a
cb97897d79c6cdab9b7dc29ff150b418ffb8a0f94d5e56d5596b1752f4a894d2
685578031f3bf6b4ed8d8f51567ca095424ffce94f0a2b7dc67618384c87b3ee
```

runner freeze-reference与reconciliation formal-kind proof-target setup errors、worktree attachment cap、display truncation、Windows
wildcard、cache cleanup policy block、anonymous diagnostic与preflight均按原identity保留，qualification effect为`NONE`。后继proof
facility没有重复任何formal PASS，也没有修改产品或oracle。

因此只有以下状态成为新事实：

```text
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FREEZE_QUALIFICATION_RECOVERY_0_1_QUALIFIED_HISTORY
```

PR #443的`CANCELLED`、lower cause `UNKNOWN`与doc389 `MERGED / NOT_QUALIFIED / NOT_FROZEN`不被回填；PR #445只拥有CI
containment maintenance资格，不向semantic freeze提供继承权。global composition authority、manifest、same-attempt Evidence continuity、
persistence、public Review与R2–R6也没有因此获得授权。

## 2. 为什么必须version 0.8，而不是重解释0.7

0.7的语义bytes绑定其construction base、final same-candidate milestones bytes、当时的current facts与fresh readback identity。#446在
0.7冻结以后形成新的effective state，所以当前`docs/project-state.md`已经发生publication lag；这不是0.7原world中的错误，也不授权
修改doc375/doc376或声称0.7当时已经知道未来事实。

本合同只version被新事实推进后产生的bounded public projection semantic boundary：

```text
projection 0.7 = FROZEN HISTORICAL
projection 0.8 = NEW CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
```

形式上只替换版本号、marker或摘要不能解决原工程问题。0.8必须把原工程问题、当前proof obligation与适用world机械分开，并重新
证明公开状态跨README、project-state、AGENTS、milestones与本文自洽。

## 3. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8`

0.8 candidate冻结以下合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes必须先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因此没有自引用；
4. projection 0.7必须显示为frozen historical，不能被0.8改写、回填或冒充当前candidate资格；
5. PR #429、#436、#437、#439、#440、#443及其`PARTIAL`、`FAILURE`、`CANCELLED`、setup failure和`UNKNOWN`
   必须继续可见，后继PASS不得覆盖；
6. fixed private unified output admission implementation只在doc380冻结合同与PR #446 exact world内为`FROZEN`；
7. global composition authority、manifest、same-attempt Evidence continuity、persistence、public Review与R2–R6继续未恢复、未开始或未授权；
8. Business Layer仍不能代替Core决定证据充分性，Core也不拥有Reality；本投影不获得事实、Seal、qualification或scheduler authority。

本candidate的milestones source binding为：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 682147
sha256    = 2746732b39f502e1e4b0d9bd3b8c97b3dccadaade15bc31b302058f83dd270fc
blob_sha1 = 123e0736ceb4f44c738b3c5dba92863eca5c4149
```

## 4. 问题连续性

```text
original engineering problem = 维护准确、自洽、可公开观察的有界current-state projection
current proof obligation      = 只资格化0.8 candidate的final bytes、source binding与跨表面一致性
applicability world           = exact base f2ab7b78/tree 280cbc4、本candidate final bytes、attempt与fresh readback identity
proof_is_not_problem_solving  = true
```

PR #446的semantic freeze是本projection必须准确陈述的既有事实，不是本文重新证明的产品对象。0.8 candidate资格成立也只表示该有界
阅读面在自己的world内可消费；它不等于完整Review产品、manifest、Evidence continuity或语言支持资格持久化已经完成。

## 5. Exact scope与不变量

本candidate只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/project-state.md
docs/391-r1-public-project-state-projection-successor-0.8-contract.md
```

以下surface必须与base逐字节相同：

```text
docs/375-r1-public-project-state-projection-successor-0.7-contract.md
docs/376-r1-public-project-state-projection-0.7-freeze-publication.md
docs/377-r1-application-level-unified-review-coverage-output-admission-current-state-audit.md
docs/378-r1-application-level-unified-output-admission-audit-readback-target-correction.md
docs/379-r1-application-level-unified-review-coverage-output-admission-current-state-audit-successor.md
docs/380-r1-application-level-unified-review-coverage-output-admission-contract.md
docs/381-r1-application-level-unified-review-coverage-output-admission-contract-freeze-publication.md
docs/382-r1-application-level-unified-review-coverage-output-admission-private-implementation-feasibility-audit.md
docs/383-r1-application-level-unified-review-coverage-output-admission-private-implementation-authorization-publication.md
docs/385-r1-unified-output-admission-implementation-original-gate-failure-boundary-audit.md
docs/386-r1-unified-output-admission-failure-boundary-exact-main-qualification-audit.md
docs/387-r1-application-level-unified-review-coverage-output-admission-private-implementation-successor-candidate.md
docs/388-r1-application-level-unified-review-coverage-output-admission-private-implementation-qualification-recovery.md
docs/389-r1-application-level-unified-review-coverage-output-admission-private-implementation-freeze-publication.md
docs/390-r1-application-level-unified-review-coverage-output-admission-private-implementation-freeze-qualification-recovery.md
src/**
plugins/**
tests/**
.github/workflows/**
audit.json
```

doc384不存在；本candidate不得为了编号连续性虚构它。

## 6. 资格链与fresh readback target

候选必须重新完成：local link/scope/source-binding/semantic review、声明的双Python普通/优化focused witness与global/local hygiene、
原始PR门、受保护exact-head普通merge、新exact-main Public CI与Browser Smoke。随后必须建立fresh detached exact-main worktree与全新
证据根，只认该merge world，并通过匿名installed-product观察验证：

| target | observation | 必须证明 |
| --- | --- | --- |
| README | Public Render + Contents API + Core | 0.8 candidate、0.7 frozen history、#446 freeze与后继stop一致 |
| project-state | Public Render + Contents API + Core | identity/status/current facts/source binding/failures/stop line内部一致 |
| doc376 | Public Render + Contents API + Core | projection 0.7 frozen history未被改写 |
| doc389 | Public Render + Contents API + Core | #443 publication仍not-qualified/not-frozen |
| doc390 | Public Render + Contents API + Core | #446 recovery责任与conditional target原字节可观察 |
| 本文 | Public Render + Contents API + Core | 0.8 contract exact bytes与candidate ceiling可观察 |
| AGENTS | raw.githubusercontent + Contents API + exact Git | 完整字节一致 |
| milestones | raw.githubusercontent + Contents API + exact Git | 完整append-only历史字节一致 |

所有产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用
`http://127.0.0.1:7897`。任何FAIL/ERROR/CANCELLED/setup failure与`UNKNOWN`按原identity保留；不同target、attempt或
world不能拼接。

全部target各自唯一PASS后，必须独立reconcile exact base/head/tree、原始PR、protected merge、exact-main gates、candidate source
binding、Public Render/API/raw/Git/Core identity、问题连续性与primary `audit.json`，再做finite closeout。

## 7. 候选上限与下一步

当前只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN_HISTORICAL
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FREEZE_PUBLICATION_PR443_MERGED_EXACT_MAIN_PUBLIC_CI_CANCELLED_NOT_QUALIFIED_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CI_HEADROOM_MAINTENANCE_SUCCESSOR_V2_PR445_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FREEZE_QUALIFICATION_RECOVERY_0_1_QUALIFIED_HISTORY
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后，本文与projection 0.8最多成为`QUALIFIED_CANDIDATE / NOT_FROZEN`。publication形成新事实后必须返回
CONTROL LOOP；独立docs-only freeze publication未闭合以前不得写`FROZEN`，也不得启动manifest、Evidence、persistence、public
Review或R2–R6。

## 8. 机器可检索标记

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN_HISTORICAL
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
