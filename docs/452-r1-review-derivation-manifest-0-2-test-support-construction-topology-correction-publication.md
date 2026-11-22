# R1 Review Derivation Manifest 0.2测试支撑构造拓扑修正发布

日期：2026-11-22

> 候选状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@68cfba79009671adce59b66e366db95f3a9aa2f6`，tree
> `9c1e220ada9afbbef7036180718265dc426d5923`。
>
> 影响：`L0_DOCUMENTATION / CONDITIONAL_TEST_SUPPORT_CORRECTION_PUBLICATION_ONLY`。本文不修改workflow、runtime、
> Schema、fixture、oracle或tests；只在自己的完整资格链闭合后，为新的Manifest 0.2 implementation successor冻结一个
> candidate-only测试支撑构造拓扑修正边界。它不恢复global composition，不启动public Review或R2–R6。

## 1. CONTROL LOOP输入

[文档451](451-r1-review-derivation-manifest-0-2-ci-budget-recovery-test-support-topology-audit.md)已经以PR #514完成：

```text
candidate base          dd734631a335b075aaef534c539177f1d9204e5d
candidate head          1f78923e966cdb293be3bb2353abb13b4d69aa2c
candidate tree          9c1e220ada9afbbef7036180718265dc426d5923
original Public CI      44987173486 / attempt 1 / 15 of 15 SUCCESS
protected merge         68cfba79009671adce59b66e366db95f3a9aa2f6
exact-main Public CI    44990531002 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser      44990530953 / attempt 1 / 1 of 1 SUCCESS
```

第一次fresh readback把832401-byte `docs/milestones.md`预注册为bounded Public Render target，得到HTTP 200、marker=1，
但coverage为`PARTIAL / CONTENT_TRUNCATED`。它没有Core Verdict、没有formal observation，也没有资格作用；该world已以
failure-boundary `e21c24be8975513065a73bf23b7227e4b814bc14cf31e65588f08ff81877282a`、83-artifact closeout
`272a3ea6983bc96d31c92c95e0ead210446b10ffe4bfd31624f6d887b3a652dd`与integrity
`f25aa91966cc91cdf0c43505d39c7ff7f40a51a06b71d4dfeb63ec83e987cda6`永久保留，没有重跑。

fresh successor只对README、doc450与doc451执行Public Render diagnostic/formal，对AGENTS与milestones执行匿名raw/API/exact-Git
byte observation。三项Render和两项raw目标各自唯一PASS；independent reconciliation attempt 1的raw-history `exit_code`
schema-key setup error以`2bee7a8f2409db1c5d39dc7f46b5dc9b5811c997c9628cc02ad8ebdb4c6f6c1d`保留，独立v2没有覆盖它。
最终身份为：

```text
independent reconciliation  fc128185c71a474ac007cba57c213b743f6516b86a9647ab58d72186906b53ef
123-artifact finite closeout  0e19553b634f259cd228fada1ec1262481ca5b98fe864be87872ee5e3664deef
post-closeout integrity       334430c6ce8264cf206331f38183d355957ba70db835be66024b95536f51e64c
```

因此doc451现在是`RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDITED / QUALIFIED_HISTORY`。它证明了有界恢复方案存在，但没有把
不可资格化原型变成产品字节，也没有让PR #512续期。

## 2. 保留的失败边界

PR #512继续绑定：

```text
base                  50819b8ab16800a415439285dc9fcf909d5b435a
head                  a9c60eea76aad5e0801e76be639dc620388ce492
tree                  04629a631652ac5a75faf42b313a5d64bd2b9563
original Public CI    44969144404 / attempt 1 / CANCELLED
Python 3.10 normal    job 137044844539 / CANCELLED at 45m0s
Python 3.10 -O        job 137044844604 / CANCELLED at 45m0s
```

PR已关闭、未合并、未rerun。两个Python 3.13 cells的SUCCESS、本地四格PASS或后继probe不得回填两个CANCELLED cells与required
aggregator FAILURE。产品断言失败没有建立；全部CI variance的唯一底层原因仍为`UNKNOWN`。

## 3. 已建立的最小修正前提

失败候选新增的21个Manifest plugin tests在Python 3.10 normal逐测试诊断中21/21 PASS、耗时722.135202秒。多数falsifier只消费
`_normal_worlds()[0]`或`[1]`，candidate-only helper却在每次调用时先构造四个完整world。不可资格化原型只按索引构造被消费的
world；它保持21个test names、全部assertion/subTest call multisets与完整八world主测试，Python 3.10 normal/`-O`仍21/21 PASS，
分别为284.273858秒与281.004309秒。probe summary SHA-256为
`be4a412f073152c188d043aeaa7d922ce22a80a0441bb543bdd0a212cc8cb9e4`。

该证据只把已测出的重复构造成本从`UNKNOWN`集合中分离。它不证明GitHub runner的唯一慢因，不证明PR #512原本会PASS，也不授权
增加timeout、拆分workflow或修改产品语义。

## 4. 条件化冻结的修正边界

本文自己的全部资格门闭合后，新的implementation successor只允许在candidate-only测试支撑中：

1. 保留`_normal_worlds()`作为完整四normal-world denominator的构造入口；
2. 新增按既有索引`0..3`调用同一既有world builder的单一world helper；
3. 对只消费一个world的falsifier，把“先构造四个再取一个”机械改为“只构造同一个被选world”；
4. 对确实消费多个或全部world的测试继续构造所需完整集合；
5. 保持每个world的Provider调用次数、source/carrier identity、one-shot与mutation观察、断言顺序及expected failure不变。

唯一允许的test-support产品路径是：

```text
plugins/review-attention/tests/test_review_derivation_manifest_0_2.py
```

该文件可以与从新exact main重建的Manifest 0.2 implementation successor同属一个候选，但修正必须能在diff中独立机械识别。

## 5. 必须保持不变的oracle与边界

implementation successor不得改变：

- `.github/workflows/ci.yml`中的45分钟outer budget、四个Python/version-mode cells与required aggregators；
- 21个plugin test identities、全部assertion与`subTest`调用多重集；
- 完整四normal + 四negative world denominator及主测试；
- `RDMC-000..013` proof obligations、negative reason、projection、publication与one-shot拒绝语义；
- Manifest 0.2 Schema、compatibility fixture、runtime、private Provider、projector、consumer与publisher的冻结合同；
- doc448 bounded private implementation authority、doc450失败历史与doc451审计结论；
- primary `audit.json`、global composition authority、public Review与R2–R6停止线。

如果新的candidate需要删除测试、减少world、改变断言、提高timeout或修改runtime来取得预算，它必须停止并把真实反例归入被击穿的
最小边界；不得在本publication名义下扩张。

## 6. Implementation successor的身份要求

后继不能复用PR #512 commit、tree、original run或本地qualification。必须从本publication资格化后的新exact main重新构造：

```text
new exact base
    + previously authorized Manifest 0.2 product bytes reconstructed as a new candidate
    + only the frozen candidate-test construction-topology correction
    -> new head / new tree / new original PR attempt
```

必须重新运行双Python normal/`-O` focused与full Review Attention witness、semantic equivalence、scope/hygiene、原始PR门、protected
exact-head merge、new exact-main双门、fresh installed-product readback与独立reconciliation。PR #512的任何PASS/CANCELLED都不继承。

## 7. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/452-r1-review-derivation-manifest-0-2-test-support-construction-topology-correction-publication.md
docs/milestones.md
```

workflow、runtime、tests、Schema、fixture、doc316–451、`docs/project-state.md`与primary `audit.json`必须保持
`68cfba7…` base bytes。local gates至少复算exact scope、UTF-8/LF/final-LF、links/fences/headings、required markers、
`git diff --check`、global/local hygiene、doc451 qualified-history evidence、PR #512 retained evidence、probe summary、remote main与primary
audit continuity。

## 8. Qualification pipeline

```text
final docs-only publication bytes / declared local gates
    -> immutable PR body seal
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc451 / 本文 formal
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent retained-failure / audit / correction-boundary reconciliation
    -> finite closeout + post-closeout integrity
    -> TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_FROZEN
    -> return CONTROL LOOP
```

每个formal identity只运行一次；任何non-success保留原identity。产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。后继PASS不得覆盖PR #512、第一次readback截断或reconciliation
attempt 1 setup failure。

## 9. 当前状态与生效条件

本文自己的最后门闭合以前只允许：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_DERIVATION_MANIFEST_0_2_ORIGINAL_PUBLIC_CI_BUDGET_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_CI_BUDGET_RECOVERY_TEST_SUPPORT_TOPOLOGY_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_REBUILD_NOT_AUTHORIZED_BY_CORRECTION_PUBLICATION
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后才条件化变为：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_REBUILD_ALLOWED_WITH_FROZEN_TEST_SUPPORT_TOPOLOGY_CORRECTION
```

随后必须返回CONTROL LOOP，从新的exact main重建implementation successor。本文不让PR #512续期，不宣称Manifest 0.2实现已经完成，
也不恢复global composition或启动public Review/R2–R6。`proof_is_not_problem_solving = true`、`local_not_global = true`、
`target_continuity_over_local_correction = true`继续成立。
