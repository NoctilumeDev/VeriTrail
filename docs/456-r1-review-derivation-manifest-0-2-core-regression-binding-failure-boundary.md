# R1 Review Derivation Manifest 0.2 Core regression binding failure boundary

日期：2026-11-23

> 当前状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_PR519_CORE_REGRESSION_BINDING_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@9d2a76e6edb3237946dd56806602a894fc70e028`，tree
> `d0a7222279f3e10e0803a2154fd4ab434c99f8ca`。
>
> 影响：`L0_DOCUMENTATION / ORIGINAL_REQUIRED_GATE_FAILURE_BOUNDARY_ONLY`。本文只保存PR #519
> original Public CI attempt 1的两套required Python Core regression失败、下游fail-closed、候选关闭未合并与最小重开边界；
> 不重跑、不合并失败候选，不修改runtime、tests、Schema、fixture、workflow、oracle或冻结历史。

## 1. CONTROL LOOP输入与失败候选坐标

PR #518已把[SourceSnapshot test-environment correction implementation freeze publication](454-r1-source-snapshot-test-environment-correction-implementation-freeze-publication.md)
精确合入：

```text
base                    = 72b9936c4cd2c0463401a19fc629babed5068a27
head                    = 435df1e9bbb26e8813a6c9ff215d6eae8d1fdfb7
tree                    = d0a7222279f3e10e0803a2154fd4ab434c99f8ca
protected merge / main  = 9d2a76e6edb3237946dd56806602a894fc70e028
original Public CI      = 45050642889 / attempt 1 / 15 of 15 SUCCESS
exact-main Public CI    = 45054044651 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser      = 45054044645 / attempt 1 / 1 of 1 SUCCESS
```

fresh README/doc453/doc454 Render formal与AGENTS/milestones raw/API/exact-Git observation各有唯一PASS；independent
reconciliation、finite closeout与post-closeout integrity SHA-256为：

```text
cd643bd0880ed584899ac8622eb1c76bf54b5ef4bd4bdab54059f30252a963be
f40de0d65bec941362ed0588167e36bd01e5b6551852975434c1ed0e853c30fa
101cc6674b41f548021320f00224624aebe2f38ff9b0912409757756b8d9e072
```

因此`R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_IMPLEMENTATION_FROZEN`已生效。PR #519随后从该exact main建立
独立Manifest 0.2 implementation successor v2：

```text
PR                     = https://github.com/NoctilumeDev/VeriTrail/pull/519
base                   = 9d2a76e6edb3237946dd56806602a894fc70e028
head                   = f5eff36f3a0d37a97b0d0d1e8a39f64cce76d2d6
tree                   = 36620b3471acb72a224321af83d2ee5496697380
scope                  = 1 commit / 11 files
original Public CI     = 45068502183 / attempt 1 / FAILURE
PR terminal state      = CLOSED / UNMERGED
same-head rerun        = NONE
```

候选新增versioned Manifest 0.2 Schema、compatibility fixture、private projector/admission/staging、独立conformance与tests；
Manifest 0.1、public exports、default composition、persistence、public Review与Core Verdict保持不变。本地final candidate四格
focused/root-payload/full Review Attention与compile/hygiene/scope/audit continuity曾PASS；这些只作local witness，不替代original gate。

## 2. Original gate的精确结果

run `45068502183`绑定上述exact head，attempt 1终态为`FAILURE`。机械job结果是：

| Layer | Job | Result |
| --- | ---: | --- |
| Workbench | `137349947489` | SUCCESS |
| Review Attention Python 3.13 normal | `137349947829` | SUCCESS / 30m42s |
| Review Attention Python 3.10 normal | `137349947842` | SUCCESS / 32m23s |
| E3 release acceptance | `137349947891` | SUCCESS |
| Review Attention Python 3.13 optimized | `137349947936` | SUCCESS / 30m44s |
| Review Attention Python 3.10 optimized | `137349948032` | SUCCESS / 43m31s |
| required Python 3.13 | `137362752917` | FAILURE |
| required Python 3.10 | `137362752919` | FAILURE |
| Acceptance Core freeze | `137363762637` | SKIPPED |
| GitHub Evidence wheel-only | `137363762641` | SKIPPED |
| Core wheel-only first run | `137363762804` | SKIPPED |
| Starter golden path | `137363762937` | SKIPPED |

四个Review Attention cells均在既有45分钟outer budget内完成，所以本次没有复现PR #512的timeout/cancellation。两个required
Python jobs分别运行509项Core regression，只产生同一个失败并保留一个skip：

```text
test_rae_016_017_identity_is_acyclic_and_manifest_topology_is_unchanged

actual:
  review-derivation-manifest-0.1.schema.json
  review-derivation-manifest-0.2.schema.json

expected:
  review-derivation-manifest-0.1.schema.json
```

Python 3.10为`Ran 509 tests in 103.867s / FAILED (failures=1, skipped=1)`；Python 3.13为
`Ran 509 tests in 135.610s / FAILED (failures=1, skipped=1)`。两个job都以exit 1终结，后继四门按workflow设计SKIPPED。

## 3. 冻结语义与失败断言不是同一命题

[RelationSet admission contract](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)的`RAE-017`要求：

```text
historical Manifest 0.1 byte guard rejects an eighth-file -> ninth-file shortcut
```

[Manifest 0.2 frozen contract](316-r1-review-derivation-manifest-negative-world-successor-contract.md)随后明确选择独立versioned identity：

```text
schemas/review-derivation-manifest-0.2.schema.json
schema_version = 0.2
outcome_kind   = COVERAGE
```

同时要求Manifest 0.1 bytes逐字节immutable。当前Core test已经通过`HISTORICAL_BYTE_GUARDS`固定0.1 SHA-256，并在
`test_rae_010_manifest_binding_cannot_repair_an_invalid_witness`中复算该hash；PR #519也未修改0.1。失败的最后一条目录断言却把：

```text
historical 0.1 bytes/topology must remain unchanged
```

近似成：

```text
the schema directory may forever contain only version 0.1
```

后一个命题已被doc316冻结的versioned successor边界显式取代。删除这条oracle、忽略0.1 byte guard或允许任意新文件都会弱化证明；
但继续要求目录永久只有0.1也会错误拒绝已授权的独立0.2版本。当前反例因此归层为：

```text
PR519 candidate scope completeness                    = FAILED
Core acceptance binding for the versioned schema set = STALE / COUNTEREXAMPLE ESTABLISHED
Manifest 0.2 product algorithm regression             = NOT_ESTABLISHED
Manifest 0.1 historical byte drift                    = NOT_OBSERVED
original PR qualification                             = FAILED / NOT_QUALIFIED
```

## 4. 不能拼接、覆盖或解释

以下身份必须并存：

1. doc316/doc317 frozen Manifest 0.2 contract；
2. doc448 bounded private implementation authority；
3. doc452与doc454已冻结的两项test-support correction；
4. PR #519 local final candidate witnesses PASS；
5. PR #519六个前置jobs SUCCESS；
6. PR #519两个required Python jobs FAILURE；
7. PR #519四个downstream jobs SKIPPED；
8. PR #519 closed/unmerged/no-rerun；
9. 本docs-only boundary仍只是candidate。

```text
local matrix PASS               != original gate PASS
Review Attention cells SUCCESS  != required Core jobs SUCCESS
authorized versioned Schema     != Core acceptance binding updated
later corrected successor PASS  != erase PR519 FAILURE
same product bytes recreated    != PR519 qualification inherited
```

## 5. 最小重开边界

当前只重开：

```text
PR519_ORIGINAL_REQUIRED_GATE_FAILURE_BOUNDARY
RAE_017_VERSIONED_MANIFEST_SCHEMA_SET_ACCEPTANCE_BINDING
```

不重开Manifest 0.2合同、0.1 immutable bytes、carrier freeze、bounded implementation authority、Schema/conformance/product
semantics、workflow budget、CoverageLedger、Provider、default/global composition、persistence、public Review、Core Verdict、
HumanDisposition或R2–R6。恢复顺序只能是：

1. 本failure-boundary audit完成自己的完整资格链；
2. 返回CONTROL LOOP，独立审计旧RAE-017证明义务与doc316 versioned roster的最小可同时满足表达；
3. 另建docs-only correction publication，明确保留0.1 byte guard、禁止shortcut并精确绑定允许的schema versions；
4. correction implementation以独立单文件test-support candidate资格化；
5. correction冻结后再次返回CONTROL LOOP，从新exact main机械重建Manifest implementation successor；
6. 所有后继PASS不回填PR #519。

本文不预先选择“改expected list”“重写test”“拆分test identity”中的具体实现，也不授权直接修改测试。

## 6. Retained evidence与setup history

PR #519 evidence root保存final candidate、original run、两个required job完整日志、annotations、PR close comment与closed state。
关键SHA-256为：

```text
terminal run capture       a59028d9069e737d5e3c6314eee34125b0ec117d2102f120f9419f1f008f2d91
Python 3.10 required log   4aadc4c33d71479aa817443ab70eee7f46af9ad5ca2edb9560a611306d164b13
Python 3.13 required log   cc37de984b9c3ff97ba1fc46bb4aab088bb2de5acf373b2414ddef7c1771333a
PR close comment           d1477a6b4c9c1ece60318a91d73dea838445e03e0fc4896b72d3fbfc31205d60
PR closed state            6ec8907d4620dd8696540ef68c8df05f259bb7f3d90dbb7b1c4a11f80c5e0751
```

第一次run capture使用不存在的`startedTime`字段，未生成run文件；v2改用`startedAt`后成功。该setup error及managed worktree
attachment cap错误均保留为`NON_QUALIFYING / NONE`，不覆盖正确capture。primary
`C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须继续保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 7. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/456-r1-review-derivation-manifest-0-2-core-regression-binding-failure-boundary.md
docs/milestones.md
```

PR #519的11个candidate files、runtime、tests、fixtures、Schema、workflow、doc316–454、`docs/project-state.md`与primary
`audit.json`必须保持base bytes。失败候选继续由原head与evidence root承担provenance；不得复制进本分支冒充main事实。

## 8. Qualification pipeline

final bytes至少复算exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、PR/run/job/
closed-unmerged identity、unchanged workflow/runtime/tests/Schema、remote main、primary audit、`git diff --check`、global/local hygiene，
以及Python 3.10.6/3.13.13 × normal/`-O`的read-only RAE/Core focused witnesses。

```text
final failure-boundary docs bytes / declared local gates
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc454 / 本文 Render
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent PR519 / run / RAE-017 / source-byte / retained-history reconciliation
    -> finite closeout + post-closeout integrity
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

本文自己的PASS不能资格化、合并或冻结PR #519，也不能自动授权test correction或Manifest successor。

## 9. 当前状态与停止线

本文只允许发布：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PR519_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PR519_CORE_REGRESSION_BINDING_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文全部门闭合后也只保存`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；必须返回CONTROL LOOP，不得按文档编号直接修改测试、
重建implementation、恢复global composition或启动public Review/R2–R6。`proof_is_not_problem_solving = true`、
`local_not_global = true`、`target_continuity_over_local_correction = true`继续成立。R1完成后的human+AI全项目检查与未来开源能力组合
仍是独立后续目标。
