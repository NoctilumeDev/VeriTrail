# R1 Review Derivation Manifest 0.2 CI 预算恢复测试支撑拓扑审计

日期：2026-11-22

> 候选状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_CI_BUDGET_RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@dd734631a335b075aaef534c539177f1d9204e5d`，tree
> `d55b326fc75aab2afcfc22ec1cbd973c5f3233a3`。
>
> 影响：`L0_DOCUMENTATION / READ_ONLY_RECOVERY_FEASIBILITY_AUDIT_ONLY`。本文只比较PR #512失败候选的
> original CI步骤时长、本地逐测试成本、当前workflow拓扑和一个不可资格化的测试支撑原型；不修改workflow、
> runtime、Schema、fixture、oracle或PR #512，不创建新的实现候选，也不恢复global composition或启动public Review/R2–R6。

## 1. CONTROL LOOP 输入

[文档450](450-r1-review-derivation-manifest-0-2-original-ci-budget-failure-boundary.md)已经通过自己的完整资格链：

```text
candidate base          50819b8ab16800a415439285dc9fcf909d5b435a
candidate head          deba1f6970584533fabc23fea8fd3da178a177fd
candidate tree          d55b326fc75aab2afcfc22ec1cbd973c5f3233a3
original Public CI      44974179853 / attempt 1 / 15 of 15 SUCCESS
protected merge         dd734631a335b075aaef534c539177f1d9204e5d
exact-main Public CI    44977819504 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser      44977819583 / attempt 1 / 1 of 1 SUCCESS
```

fresh exact-main installed-product README/doc450/milestones formal与AGENTS/milestones raw-byte observation各自唯一PASS；
independent reconciliation、97-artifact finite closeout和post-closeout integrity分别为：

```text
8ad805964ea28f587089b426f632e3a8fef8efed901baa2a34de46537bbf605e
a5b8b4bde2f565bd0fa49ffbf85a809683f080f1ccc4fbaea052fc76babc0a32
e88922cfc31482d34ab1d64ab6ad41231a6e857456964768a4389e9081771b43
```

第一次fresh root中的Python 3.13/bootstrap和public GitHub Evidence `0.1.0`版本漂移setup failure、第二个root中的
`py_compile *.py`未展开wildcard setup failure继续保留原identity；后继PASS没有覆盖它们。因此doc450现在最多是
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`，而PR #512仍为
`CLOSED / UNMERGED / ORIGINAL_PUBLIC_CI_CANCELLED / NOT_QUALIFIED / NOT_FROZEN / NO_RERUN`。

fresh CONTROL LOOP随后重新读取exact main、当前`.github/workflows/ci.yml`、失败head、原始run/job steps、本地final
matrix和candidate-only tests，才进入本审计。doc450的`UNKNOWN`不能直接替换成某个方便修复的解释。

## 2. 失败world与当前workflow没有漂移

PR #512继续绑定：

```text
base                  50819b8ab16800a415439285dc9fcf909d5b435a
head                  a9c60eea76aad5e0801e76be639dc620388ce492
tree                  04629a631652ac5a75faf42b313a5d64bd2b9563
original Public CI    44969144404 / attempt 1 / CANCELLED
Python 3.10 normal    job 137044844539 / CANCELLED
Python 3.10 -O        job 137044844604 / CANCELLED
```

两个job从`Run Review Attention ... contract tests`开始到外部取消分别经过2626秒与2625秒；整个job的outer budget仍为
2700秒。安装和exact editable candidate校验均已SUCCESS，测试步骤没有产生完整`Ran N tests`终结摘要。

current exact-main workflow SHA-256为
`6d93030cf27f68f16eb26480ec154f59077a1abf75c2c248ba3b04e4c3be5690`，仍为四个独立
`Python 3.10/3.13 × normal/-O` Review Attention cells、每格45分钟、required Python aggregators fail closed；本审计
没有发现base到failed candidate之间的workflow漂移。45分钟边界仍是真实约束，不是建议值。

## 3. 候选新增成本的逐测试定位

失败候选本地final full Review Attention矩阵四格各报告715项；3.10 normal/`-O`分别为2467.569秒与2459.967秒，
均为`712 passed / 3 skipped`。其中新增Manifest 0.2 focused witness有5个root Schema测试和21个plugin测试；root
Schema/payload测试不足1秒，成本集中在21个plugin测试。

在原失败head的不可修改副本上，Python 3.10 normal逐测试诊断得到：

```text
tests                    21 / 21 PASS
elapsed                  722.135202 seconds
slowest complete-world   87.590213 seconds
timing SHA-256           5e145199a6e30110abcb4f2647b1e9b107b986ffc520402da2fe9ae7a92f3144
```

静态审查证明主要重复来自candidate-only helper `_normal_worlds()`：多数falsifier只消费索引`0`或`1`，helper却先构造
`NORMAL_CONSISTENT / NORMAL_BRANCH_EMPTY / NORMAL_SLICE_PARTIAL / NORMAL_RELATION_CONFLICT`四个完整上游world，再丢弃
未选中的三个。`RDMC-008`为了两个world调用helper两次，因此构造八个world；这不是Manifest conformance自身的必要成本。

## 4. 不可资格化原型与oracle等价检查

为检验最小恢复假设，审计在独立detached诊断worktree中只改candidate-only测试文件：

```text
plugins/review-attention/tests/test_review_derivation_manifest_0_2.py
```

原型增加按索引构造单一world的helper，并把测试中的`_normal_worlds()[index][1]`机械替换为
`_normal_world(index)[1]`。它没有进入main、没有提交、没有PR，也没有资格作用。完整八world主测试仍调用全部四个normal world和
四个negative world；任何one-shot、race、staging、mutation、version、role/path、digest或topology断言都没有删除。

独立AST核对结果：

```text
test names                                      21 / identical
normalized test bodies                         21 / identical
assertion + subTest call multisets              21 / identical
original candidate test SHA-256                 512f4d26ea1e649f087fd2c5652b630668b7e7253e9d6cce65cef803e260c680
diagnostic prototype test SHA-256                4201dcbfc912deb6062c2eb58a5b070651494090f59f187a9a39b1bd67d68313
```

Python 3.10结果：

| World | Tests | Result | Elapsed |
| --- | ---: | --- | ---: |
| original candidate normal | 21 | PASS | 722.135202s |
| diagnostic prototype normal | 21 | PASS | 284.273858s |
| diagnostic prototype `-O` | 21 | PASS | 281.004309s |

normal减少437.861344秒，即60.6343%。完整八world主测试仍约87秒，没有通过削减denominator取得加速。probe summary
SHA-256为`be4a412f073152c188d043aeaa7d922ce22a80a0441bb543bdd0a212cc8cb9e4`。

这些结果只证明一个有界恢复方案存在；它们不资格化原型、不预测GitHub runner一定耗时，也不把本地PASS拼进PR #512。

## 5. 分层判断与未被证明的事情

当前证据支持：

```text
measured redundant cost                 ESTABLISHED
affected layer                          TEST_SUPPORT_CONSTRUCTION_TOPOLOGY
bounded recovery hypothesis             ESTABLISHED
Manifest runtime assertion failure      NOT_ESTABLISHED
Schema/conformance contract defect       NOT_ESTABLISHED
workflow topology defect                 NOT_ESTABLISHED
unique cause of all CI variance          UNKNOWN
PR512 qualification                      CANCELLED / NOT_QUALIFIED
```

因此不能把`UNKNOWN`全部改写成“已知就是测试helper”，但可以把已经机械测出的437.86秒重复构造从未知集合中分离，并选择只移除
这部分非证明成本。理论遇到反例先检查前提：这里被击穿的是“新增witness仍能在45分钟outer budget内完成”的测试成本前提，不是
Manifest 0.2合同、八world denominator或产品runtime语义。

## 6. 方案比较与最小后继边界

| 方案 | 当前判断 | 原因 |
| --- | --- | --- |
| 提高45分钟timeout | 不选择 | 会保留已测出的重复构造并吞掉后续回归信号；现有证据不要求改变containment policy。 |
| 拆分完整suite | 不选择 | 会新增workflow/status拓扑；在单文件按需构造已经恢复约7.3分钟时不是最小边界。 |
| 修改Manifest/runtime | 禁止 | 没有产品断言失败或runtime defect证据。 |
| 删除测试/缩小world | 禁止 | 会弱化`J`项oracle与八world denominator。 |
| candidate test按需构造world | 选择为后继候选边界 | 只消除没有进入断言的三份多余world，保留测试名、断言、falsifier和完整八world主测试。 |

本文仍不直接授权把诊断diff复制进实现。自己的完整资格链闭合后，下一最小seam只能是独立docs-only
`MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_PUBLICATION`：冻结“从新exact main重建implementation successor时，
只允许在candidate test中按需构造所选world”的施工边界，并明确workflow 45分钟、runtime、Schema、fixture、21个test identity、
全部assertion和八world denominator不变。该publication资格化以前不得重建implementation candidate。

## 7. 必须继续保留的non-success

- PR #512 original run、两个3.10 CANCELLED jobs、required aggregator FAILURE与下游SKIPPED；
- PR #512 closed/unmerged/no-rerun identity及本地PASS矩阵；
- doc450两个fresh readback roots中的Python/bootstrap、plugin version drift、wildcard compile setup failures；
- 本审计的原始722.135202秒诊断与两个不可资格化原型PASS；
- #498、doc437及后继public-product/readback链中的全部既有FAIL/ERROR/UNKNOWN。

后继PASS不得把“原型足够快”写成PR #512本来会PASS，也不得把新的实现successor解释成旧head续期。

## 8. Exact docs-only scope与本地门

本candidate只允许：

```text
README.md
AGENTS.md
docs/451-r1-review-derivation-manifest-0-2-ci-budget-recovery-test-support-topology-audit.md
docs/milestones.md
```

`.github/workflows/ci.yml`、runtime、tests、Schema、fixture、doc316–450、`docs/project-state.md`与primary `audit.json`必须保持
`dd73463…` base bytes。local gates至少复算exact scope、UTF-8/LF/final-LF、links/fences/headings、required markers、
`git diff --check`、global/local hygiene、workflow/doc450 SHA、failed head/test SHA、probe summary、remote main与primary audit continuity。

## 9. Qualification pipeline

```text
final docs-only audit bytes / declared local gates
    -> immutable PR body seal
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc450 / 本文 / milestones formal
    -> fresh anonymous exact-commit AGENTS raw-byte observation
    -> independent source-byte / run-step / timing / oracle-equivalence / retained-history reconciliation
    -> finite closeout + post-closeout integrity
    -> RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

每个formal identity只运行一次；已PASS目标不得重复。产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，
代理只按命令使用`http://127.0.0.1:7897`。任何non-success保留原identity；不得rerun until PASS、弱化oracle、拼接不同world
或用后继PASS回填首败。

## 10. 当前状态与停止线

本文自己的全部门闭合以前只允许：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_PR512_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_CANCELLED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_ORIGINAL_PUBLIC_CI_BUDGET_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_CI_BUDGET_RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后也只使本文成为`RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，
独立建立上述correction publication；不得直接修改workflow、重建implementation、恢复global composition或启动public Review/R2–R6。
`proof_is_not_problem_solving = true`、`local_not_global = true`、`target_continuity_over_local_correction = true`继续成立。
