# R1 same-attempt continuity DEC-001 semantic fixture clock correction

> 日期：2026-11-15
> 状态：`TEST_FIXTURE_CORRECTION_CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`
> exact base：`e61b9a2c195633b238ba69884c43315b099ed1a6`
> base tree：`7921b30f560959b74b67eb4a189d1e4413f42121`
> 影响：`L1_TEST_FIXTURE_ONLY`。本文与同一candidate中的唯一test patch只修正`DEC-001`的证明时钟；不修改runtime、
> production budget、workflow、Schema、合同、Provider、public Review或Core Verdict。

## 1. CONTROL LOOP 输入

[文档408](408-r1-public-ci-review-attention-topology-containment-maintenance.md)已经由PR #467自己的完整资格链闭合：

```text
candidate base / head / tree = 272d581... / 3d2dfb9... / 7921b30...
original Public CI           = 43630464678 / attempt 1 / 15 of 15 SUCCESS
protected merge              = e61b9a2c195633b238ba69884c43315b099ed1a6
exact-main Public CI         = 43633875326 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser Smoke     = 43633875335 / attempt 1 / 1 of 1 SUCCESS
fresh reconciliation         = f12a12741023e87cd3d0b316d0725c7fb9991f7a3805b632ffe3e8901c2ea322
130-artifact closeout        = 8566ec8d64dcd110add13ea61443bbb0533041efdc375d820abadac1650d132a
finite integrity             = 8d7864b46afaa2120a31a86c5b0722ae430bc8a567bd74440a30f5d6359063ac
```

因此`R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN`已经生效。它只修复完整suite的outer
containment与required-check fail-closed topology，不资格化doc405，也不解释PR #464 Browser setup failure或PR #465 slowdown的
`UNKNOWN` lower cause。

fresh CONTROL LOOP随后从该exact main建立docs-only doc406 recovery candidate PR #468：

```text
base / head / tree = e61b9a2... / 6d0e645... / 010b71a...
shape              = 1 commit / 4 docs files
original Public CI = 43641391725 / attempt 1 / FAILURE / no rerun
failed cell         = Review Attention optimized on Python 3.10
failed test         = DEC-001 / subtest index 3 / REQUIRED_PROVIDER_NON_SUCCESS
reported            = 674 tests / 1 error / 3 skipped
```

另外三个Review Attention cells成功；两个既有required Python jobs按文档408的新拓扑真实FAIL，没有被dependency skip误放行。PR #468
已经关闭、未合并、未rerun。后继观察不得把该原始失败改写成未发生。

## 2. 失败边界

PR #468保留的异常链是：

```text
FactToCoverageExactInputHandoffError: exact-input carrier is no longer live
  -> NegativeWorldCoverageError: NEGATIVE_INPUT_REJECTED
  -> SameAttemptDerivationEvidenceContinuityError: EVIDENCE_CONTINUITY_RESULT_BINDING_REJECTED
  -> UnifiedOutputAdmissionError: UNIFIED_OUTPUT_RESULT_BINDING_REJECTED
```

相同Python 3.10.6 `-O`测试在独立诊断中66.071秒PASS；instrumented四世界诊断58.875秒PASS，其中index 3的最小剩余预算为
17.88秒。CI日志支持整个test约101秒，但没有记录具体哪个liveness predicate先失败。因此：

```text
PR #468 original product-test failure       = ESTABLISHED
new fail-closed topology worked             = ESTABLISHED
60-second fixture context                   = ESTABLISHED
slow-runner sufficient-budget premise hit   = LEADING EXPLANATION
deadline was the unique failed predicate    = NOT ESTABLISHED
lower cause                                 = UNKNOWN
candidate regression                        = NOT ESTABLISHED
```

真正被反例击穿的是`DEC-001`把“证明四个terminal semantic branches”与“宿主在60秒内完成重复深链构造”绑定为同一证明前提。
提高60秒只是增加新的经验例外；它既不能证明语义，也会继续让host variance决定合同测试结果。

## 3. 最小修正

本candidate只修改
`plugins/review-attention/tests/test_same_attempt_derivation_evidence_continuity.py`：

1. `DEC-001`仍顺序构造`ZERO_PARSE_DENOMINATOR / ALL_PARSE_REJECTED / PROJECTION_BLOCKED /
   REQUIRED_PROVIDER_NON_SUCCESS`四个独立world，原断言一项不少；
2. 只在该test的lexical scope内把`ParseHelper._context`替换为test-only `BudgetContext._admit_for_testing`；
3. limits仍逐字节为`60_000ms / 512MiB / 64MiB`，只把fixture monotonic clock固定为`0.0`；
4. patch退出该test后立即恢复原helper；同文件所有normal transition、真实Windows execution cell、显式cancellation、cleanup和
   mutation falsifier继续使用真实clock；
5. production `budget.py`、runtime、workflow、fixtures、Schema、合同与任何public surface保持base bytes。

这使`DEC-001`只证明其声明的语义分支，不再把host wall time偷偷加入proof obligation；真实deadline仍由独立budget primitive与
execution-cell tests拥有。

## 4. 被否决的较宽原型

prequalification prototype曾在整个test class的`setUp`冻结clock。`DEC-001`通过，但
`DEC-021/022`进入真实Windows execution cell时把固定的`0+60`deadline与真实monotonic比较，正确地报
`DERIVATION_ADMISSION_DEADLINE`。该原型失败永久保留为
`PROTOTYPE_CLASSWIDE_SEMANTIC_CLOCK_FAILURE / NON_QUALIFYING / EFFECT_NONE`。

它证明修正不能覆盖整个class；最终patch只允许进入`DEC-001`的纯语义scope。后继PASS不能删除或重解释该原型失败。

## 5. 精确范围

本candidate只允许：

```text
plugins/review-attention/tests/test_same_attempt_derivation_evidence_continuity.py
README.md
AGENTS.md
docs/409-r1-same-attempt-continuity-dec001-semantic-fixture-clock-correction.md
docs/milestones.md
```

所有runtime source、其他tests、workflow、fixtures、Schema、doc397、doc405、doc407、doc408、`docs/project-state.md`和primary
`audit.json`必须保持base bytes。

## 6. Local qualification

final bytes必须证明：

- exact five-file scope、UTF-8/LF/final-LF、links/fences/headings与`git diff --check`；
- test patch只包住`DEC-001`，四个world和全部既有assertions仍存在，60秒/512MiB/64MiB limits不变；
- Python 3.10.6/3.13.13 × normal/`-O`的focused 152-test matrix全部PASS；
- 同一四格完整Review Attention 674-test matrix全部PASS；
- 两套Python普通/优化下，真实absolute deadline、late result rejection、cleanup不能恢复late result、cancellation/cleanup无commit均PASS；
- compile、diff、global/local hygiene、remote main与primary audit continuity PASS；
- PR #468 run/job/log/annotation、closed-unmerged identity与lower cause `UNKNOWN`可复算。

本地PASS只证明final candidate可送原始远端门，不自行冻结本maintenance，也不回填PR #468。

## 7. Qualification pipeline

```text
final five-file test-fixture correction bytes / declared local gates
    -> original PR Public CI: 15 of 15 jobs, including four full Review Attention cells
    -> existing seven required contexts PASS; no ruleset mutation
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc408 / 本文 / milestones readback
    -> fresh anonymous exact-commit AGENTS / corrected test raw-byte observation
    -> independent PR468 retained-failure / oracle / scope reconciliation
    -> finite closeout
    -> TEST_FIXTURE_CLOCK_CORRECTION_FROZEN at most
    -> return CONTROL LOOP
```

任何non-success保留自己的attempt与原始身份，不rerun。后继PASS不能解释或回填PR #468。

## 8. 状态上限与停止线

本文自己的全部最后门闭合以前，只允许：

```text
R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_DOC406_RECOVERY_PR468_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_CONTINUITY_DEC001_SEMANTIC_FIXTURE_CLOCK_CORRECTION_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门成立后，只把本maintenance升级为
`R1_SAME_ATTEMPT_CONTINUITY_DEC001_SEMANTIC_FIXTURE_CLOCK_CORRECTION_FROZEN`。doc405与PR #468均不因此资格化；fresh
CONTROL LOOP必须从新的exact main独立重建doc406 recovery。本文不授权manifest、public Review、global composition或R2–R6。
`local_not_global = true`与`post_r1_global_check_required = true`继续成立。
