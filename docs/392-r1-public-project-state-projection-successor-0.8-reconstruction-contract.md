# R1 public project-state projection successor 0.8 reconstruction contract

日期：2026-11-09

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@69c1832a560dc24e0d4ea06f5bd2d4198518accd`，tree
> `89be58352da8e88e3a316b0c7e85d7b5fcf64866`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_FRESH_VERSIONED_RECONSTRUCTION_ONLY`。本文不修改runtime、tests、fixtures、workflow、
> release-download recovery、Release资产、Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Slice/Coverage
> semantics、doc375–391历史字节、projection 0.7 frozen bytes或任何其他frozen contract。

## 1. CONTROL LOOP输入：0.8仍必要，但旧0.8候选不可重放

projection 0.7由PR #427/#428完成candidate与独立freeze publication，当前继续是`FROZEN HISTORICAL`。它在自己的exact world中
准确，但其semantic bytes早于后来的application-level unified Review / Coverage output admission freeze、两个projection 0.8
original-gate failure、独立proof-facility maintenance与dual failure-boundary recovery qualification。

PR #446已经把[文档390](390-r1-application-level-unified-review-coverage-output-admission-private-implementation-freeze-qualification-recovery.md)
精确合入`main@f2ab7b78f86a057431cf5c8f4cbc3b0337338118`。original Public CI `42557756555`、exact-main Public CI
`42560991201`与Browser Smoke `42560991124`均attempt 1 SUCCESS（11/11、11/11、1/1）；fresh README/doc389/doc390
formal、AGENTS/milestones raw-byte observation、independent reconciliation与finite closeout全部成立。因此：

```text
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FREEZE_QUALIFICATION_RECOVERY_0_1_QUALIFIED_HISTORY
```

这项bounded private semantic freeze没有恢复global composition authority，也没有授权manifest、same-attempt Evidence continuity、
persistence、public Review或R2–R6。PR #443的`CANCELLED`、lower cause `UNKNOWN`与doc389 not-qualified history继续保留。

随后建立的旧projection 0.8 candidate PR #447与first failure-boundary audit PR #448各自在original gate失败：

```text
PR #447 = base f2ab7b78 / head 1e554754 / tree 521c75df / run 42568657029 attempt 1 FAILURE
PR #448 = base f2ab7b78 / head 5dd1933f / tree bad7b851 / run 42576411794 attempt 1 FAILURE
```

两者均关闭、未合并、未rerun，fresh readback没有启动。旧doc391、旧doc392与旧project-state bytes只属于closed PR world；它们的
内容、commit、local result与未来相同文字都不能继承original-gate qualification。

独立PR #449只version release-asset recovery proof facility：default absolute recovery 60→120秒，E1/E3 multi-asset lane
120→240秒；per-request 15秒、retry statuses、backoff、digest equality、owned partial cleanup、required gates与product oracle不变。
它在`main@6dd0b76184a8739e4930a517f18cb32488c459b3`完成自己的完整资格链，effect严格是
`MAINTENANCE_EXACT_MAIN_QUALIFIED`，不回填#447/#448或资格化projection语义。

## 2. #450只资格化failure history，不自动创建projection

PR #450从新的exact base建立
[dual original-gate failure-boundary recovery audit](391-r1-public-project-state-projection-0.8-dual-original-gate-failure-boundary-recovery-audit.md)：

```text
base                 = 6dd0b76184a8739e4930a517f18cb32488c459b3
head                 = fa18ab0a373c9c5773a05a24ec13148ebb3fa5e6
candidate/merge tree = 89be58352da8e88e3a316b0c7e85d7b5fcf64866
ordinary merge       = 69c1832a560dc24e0d4ea06f5bd2d4198518accd
scope                = 1 commit / 4 docs files
```

original Public CI `42599405745`、exact-main Public CI `42604418857`与Browser Smoke `42604418779`均attempt 1 SUCCESS，
分别为11/11、11/11与1/1；没有rerun。fresh exact-main只认`69c1832…`world：README与doc391各有唯一qualifying formal
`PASS`，AGENTS与milestones各有唯一raw.githubusercontent、Contents API与exact Git全字节一致观察。

README formal observation 1因anonymous API `remaining=0`终结为`ERROR / COLLECTION_BUDGET_EXHAUSTED`，同session Render仍
`COMPLETE / 200`，Core Verdict未创建；额度恢复后的observation 2才独立PASS。independent reconciliation attempts 1/2只在
remote-main query遇到TLS unexpected EOF；versioned proof facility仅显式传入per-command Git proxy，attempt 3 PASS。所有旧identity
永久保留，qualification effect为`NONE`。

independent reconciliation、138-artifact finite closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
5d19561a1e566078242974a23e24e57bc0c489024be029b2987c0b00b7d7c0f1
ef937fab434c700dca09341566727b72cab4998a4f374c5f990a5d8042244ab4
a5152bc4c40df3a60b9d6a89092a15bf5bc984053bc18b73ab9a2b1982a6546b
02c9724d08c43fc8158574908efe86919c40619ee7da39810593422c110ff924
```

因此doc391现在是`DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED / QUALIFIED_HISTORY`。它只使#447/#448 failure identity与
#449 recovery responsibility成为可消费历史；它没有创建、资格化或冻结projection 0.8，也没有选择任何runtime后继。

## 3. Fresh CONTROL LOOP为什么仍授权projection 0.8

新的CONTROL LOOP重新读取exact main的AGENTS、working method与hygiene，并独立绑定remote main、tree与primary audit：

```text
exact main     = 69c1832a560dc24e0d4ea06f5bd2d4198518accd
tree           = 89be58352da8e88e3a316b0c7e85d7b5fcf64866
remote main    = 69c1832a560dc24e0d4ea06f5bd2d4198518accd
primary audit  = sha256:4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c
```

current `docs/project-state.md`仍是projection 0.7 semantic world，查询不到#446、#447、#448、#449、#450、bounded private
implementation freeze或dual failure audit qualified identity。README虽已描述#446–#449，却仍把doc391写成完整资格链未闭合的candidate；
这与外部保留证据已经建立的#450 qualified history不再一致。

所以公开bounded projection存在publication lag。该lag不是0.7原world中的错误，也不允许修改doc375/doc376；最小合法修复只能是从
新的exact main独立重建0.8 candidate。旧#447 contract可以作为历史问题线索，但不能作为字节、资格或scheduler复用。

## 4. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8`

本fresh candidate冻结以下合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes必须先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因此没有自引用；
4. projection 0.7必须显示为frozen historical，不能被0.8改写、回填或冒充当前candidate资格；
5. PR #447/#448各自original failure、#449 maintenance-only effect与#450 qualified audit必须保持不同world和责任；
6. PR #443 `CANCELLED`、#447/#448 `FAILURE`、#450 readback/reconciliation setup errors与所有`UNKNOWN`继续可见；
7. bounded private unified output admission implementation只在doc380冻结合同与PR #446 exact world内为`FROZEN`；
8. global composition authority、manifest、same-attempt Evidence continuity、persistence、public Review与R2–R6继续未恢复、未开始或未授权；
9. Business Layer仍不能代替Core决定证据充分性，Core也不拥有Reality；本投影不获得事实、Seal、qualification或scheduler authority。

本candidate的milestones source binding为：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 687142
sha256    = 9280629d8177f5a3ce234dcfe7b75b0fc2ae7b473abb314f74d44d74dd9d42c0
blob_sha1 = c1c7bcff9adfc0a2b42dbd3881c0d31bef745a1f
```

## 5. 问题连续性

```text
original engineering problem = 维护准确、自洽、可公开观察且不越权的bounded current-state projection
current proof obligation      = 只资格化fresh 0.8 candidate的final bytes、source binding与跨表面一致性
applicability world           = exact base 69c1832/tree 89be583、本candidate final bytes、attempt与fresh readback identity
proof_is_not_problem_solving  = true
```

#446 semantic freeze、#447/#448 failure、#449 maintenance与#450 audit是本projection必须准确陈述的既有事实，不是本文重新证明的产品
对象。0.8 candidate资格成立只表示该有界阅读面在自己的world内可消费；它不等于完整Review产品或global composition问题已解决。

## 6. Exact scope与不变量

本candidate只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/project-state.md
docs/392-r1-public-project-state-projection-successor-0.8-reconstruction-contract.md
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
docs/391-r1-public-project-state-projection-0.8-dual-original-gate-failure-boundary-recovery-audit.md
src/**
plugins/**
tests/**
.github/workflows/**
audit.json
```

doc384不存在；本candidate不得为了编号连续性虚构它。closed PR #448使用过未合入的旧doc392路径不占用mainline编号，也不允许把旧字节
冒充本文。

## 7. 资格链与fresh readback target

候选必须重新完成：local link/scope/source-binding/semantic review、声明的双Python普通/优化focused witness与global/local hygiene、
原始PR门、受保护exact-head普通merge、新exact-main Public CI与Browser Smoke。随后必须建立fresh detached exact-main worktree与全新
证据根，只认该merge world，并通过匿名installed-product观察验证：

| target | observation | 必须证明 |
| --- | --- | --- |
| README | Public Render + Contents API + Core | 0.8 candidate、0.7 frozen history、#446 freeze与#450 qualified audit一致 |
| project-state | Public Render + Contents API + Core | identity/status/current facts/source binding/failures/stop line内部一致 |
| doc376 | Public Render + Contents API + Core | projection 0.7 frozen history未被改写 |
| doc390 | Public Render + Contents API + Core | #446 freeze recovery responsibility与历史字节可观察 |
| doc391 | Public Render + Contents API + Core | #447/#448/#449 failure/recovery audit历史字节可观察 |
| 本文 | Public Render + Contents API + Core | fresh 0.8 contract exact bytes与candidate ceiling可观察 |
| AGENTS | raw.githubusercontent + Contents API + exact Git | 完整字节一致 |
| milestones | raw.githubusercontent + Contents API + exact Git | 完整append-only历史字节一致 |

所有产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用
`http://127.0.0.1:7897`。任何FAIL/ERROR/CANCELLED/setup failure与`UNKNOWN`按原identity保留；不同target、attempt或world不能拼接。

全部target各自唯一PASS后，必须独立reconcile exact base/head/tree、原始PR、protected merge、exact-main gates、candidate source
binding、Public Render/API/raw/Git/Core identity、问题连续性与primary `audit.json`，再做finite closeout。

## 8. 候选上限与下一步

当前只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN_HISTORICAL
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_PR447_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FAILURE_AUDIT_PR448_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_RELEASE_ASSET_RECOVERY_PROOF_FACILITY_SUCCESSOR_V2_PR449_EXACT_MAIN_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_0_8_DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
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

## 9. 机器可检索标记

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN_HISTORICAL
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_0_8_DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_RECONSTRUCTION_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
