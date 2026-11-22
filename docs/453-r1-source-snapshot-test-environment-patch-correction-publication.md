# R1 SourceSnapshot 测试环境模拟机制反例与最小修正发布

日期：2026-11-22

> 候选状态：
> `R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@2a078fc69be89ca38b733c80700ccc98fc0b0576`，tree
> `ce725f3c8efc01477fb045ee0b04b972e6cdaadb`。
>
> 影响：`L0_DOCUMENTATION / CONDITIONAL_TEST_SUPPORT_CORRECTION_PUBLICATION_ONLY`。本文不修改 workflow、
> runtime、Schema、fixture、oracle 或 tests；只在自己的完整资格链闭合后，授权一个独立候选修正
> SourceSnapshot 合同测试的环境模拟机制。Manifest 0.2 候选继续停止，不恢复 global composition，不启动 public Review
> 或 R2–R6。

## 1. CONTROL LOOP 输入

[文档452](452-r1-review-derivation-manifest-0-2-test-support-construction-topology-correction-publication.md)已经完成自己的
local、original PR、protected merge、新 exact-main 双门、fresh installed-product readback、independent reconciliation 与 finite
closeout。当前 exact main 为：

```text
commit  2a078fc69be89ca38b733c80700ccc98fc0b0576
tree    ce725f3c8efc01477fb045ee0b04b972e6cdaadb
```

因此以下状态已经生效：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_REBUILD_ALLOWED_WITH_FROZEN_TEST_SUPPORT_TOPOLOGY_CORRECTION
```

新的 implementation successor 从该 exact main 重建了既有 Manifest 0.2 产品字节和 doc452 唯一允许的 candidate-only world
按需构造修正。focused 四格各 26/26 PASS，root/payload 四格各 27/27 PASS；这些 witness 没有给 full suite 失败续期。

## 2. 保留的正式失败边界

formal full Review Attention matrix attempt 1 四格全部失败。每格报告 715 个测试，Manifest tests 没有产品断言失败；
`test_source_snapshot_runtime` 每格各出现 20 个 repo setup error。Python 3.10 normal 的独立 serial v2 仍得到同样 20 个
error，因此“只由并发造成”的假设被反证。control loop 随即取消已经启动但尚未形成结果的 3.10 `-O` cell，并未启动
3.13 两格；没有用后继结果覆盖这些 identity。

```text
attempt1 full-matrix summary
ff640a3e1ceb4595170cf895fc582f5ba99d474b9858c10057373834074a9593

serial-v2 py310 normal log
df7f0ac8529aa09dab63b1526d8aa5c564b503d367fd5279a4ff2a276169305a

serial-v2 cancellation record
4cc93618a5b7a4b131480fd6e7b92deb4265fc855402db146d2ee46eee1c6e1f

retained failure boundary
eb9ca12f320fd6eb273cdd146c70f3aca1675c0753cb836875a1245045e3c9a2
```

该 successor 尚未提交、没有 PR、没有 original gate，也没有资格。它继续保持
`STOPPED_PRE_COMMIT_NOT_QUALIFIED`；本文不得把它改写为 implementation candidate。

## 3. 反例归层与最小原因

四组相互独立的非资格诊断把边界收敛为 test-support environment patch mechanism：

1. `test_source_snapshot_runtime.py` 单模块双 Python normal/`-O` 四格各 25/25 PASS；
2. Manifest 21 tests 后接 SourceSnapshot runtime 25 tests，同进程 46/46 PASS；
3. `test_source_snapshot_contracts` 后接 runtime 时稳定出现 20 个同类错误，真实 stderr 为：

   ```text
   error: missing config value GIT_CONFIG_VALUE_0
   fatal: unable to parse command-line config
   ```

4. 两个独立子进程证明：现有 `mock.patch.dict(os.environ, inherited, clear=False)` 稳定复现同一失败；只把
   `veritrail_review.git_objects.os.environ` 临时替换为独立 Python mapping 时，受测 blocked/safe-value 语义逐项相同，
   后继裸 `git init` 返回 0。

关键诊断摘要为：

```text
source-only matrix              3cd7dad3d25fbbe5d717211ea476d1ad88e7f3f9ec0421eb4cbc2bddffc044df
manifest -> source result       601e444558a75d29ca78718841e5426e3a9a51ed0fd62a5b28819fc78d8b61af
contracts -> runtime result     abe8e0776175ad876fd0991a2eef0817fbeaa605060016971ad0fcbca5a0569f
patch boundary diagnostic       34a6a04b70565283ae5e935ceee90f08c19207ac23fd23c9aef3e71ffdb82547
```

Windows/Codex 宿主提供的 `GIT_CONFIG_VALUE_0` 与 `GIT_CONFIG_VALUE_5` 是合法的空 helper value。合同测试直接修改
`os.environ` 后，Windows 环境恢复把空值项变成后继 Git 进程可见的缺值；错误发生在测试用 repo 的构造阶段，尚未进入
SourceSnapshot 产品采集。现有证据因此支持：

```text
layer                 TEST_SUPPORT_ENVIRONMENT_PATCH_MECHANISM
product defect        NOT ESTABLISHED
Manifest pollution    NOT ESTABLISHED
lower cause           KNOWN_TEST_SUPPORT_ENVIRONMENT_RESTORATION_INTERACTION
```

## 4. 条件化发布的唯一修正边界

本文自己的全部资格门闭合后，独立 test-support correction candidate 只允许修改：

```text
plugins/review-attention/tests/test_source_snapshot_contracts.py
```

唯一允许的语义等价修正是：

1. 保持同一个 `inherited` 字典、blocked key denominator、safe values 与断言不变；
2. 不再用 `mock.patch.dict` 写入真实进程 `os.environ`；
3. 只在 `_controlled_git_environment()` 调用期间，把 `veritrail_review.git_objects.os.environ` 指向
   `{**os.environ, **inherited}` 的独立 mapping；
4. context 退出时恢复 Python object reference，不对宿主 OS environment 执行 set/delete；
5. 增加直接证明：该合同测试后继的真实裸 `git init` 可以在同一 Python 进程中成功。

该修正必须能在 diff 中独立机械识别。它不得被解释为允许改动 SourceSnapshot runtime、Git 采集逻辑、错误 reason、
fixture、Schema、Manifest 产品或 workflow。

## 5. 必须保持不变的边界

test-support correction candidate 不得改变：

- `.github/workflows/ci.yml` 的 45 分钟 outer budget、四个 Python/version-mode cells 与 required aggregators；
- `_controlled_git_environment()` 产品实现、blocked keys、safe values 或 Git 命令；
- SourceSnapshot 的合同、runtime tests、fixture、error code、normalization 或 publisher；
- Manifest 0.2 当前未提交产品字节、21 个 plugin test identities、断言/subTest 多重集与八 world denominator；
- doc448 bounded implementation authority、doc450/#512 失败历史、doc451 审计和 doc452 frozen correction；
- primary `audit.json`、global composition authority、public Review 与 R2–R6 停止线。

若修正需要 runtime、workflow、oracle 或第二个 tracked test file 才能成立，它必须停止并重新归层，不得在本文名义下扩张。

## 6. 独立 correction candidate 的资格要求

本文资格化后，后继只能从新的 exact main 新建单一 test-support correction candidate。它至少必须重新证明：

```text
exact one-file source diff
    + direct legacy/isolated environment falsifier
    + contracts -> runtime same-process witness
    + SourceSnapshot focused double-Python normal/-O matrix
    + full Review Attention double-Python normal/-O matrix
    + diff / compile / global+local hygiene / primary audit continuity
    -> original PR gate
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh installed-product readback
    -> independent reconciliation + finite closeout
```

formal attempt 1 与 serial v2 的失败不能作为后继 PASS；当前 Manifest successor 产品字节也不能越过新 exact main 复用为
候选资格。correction 完成后必须返回 CONTROL LOOP，再从新的 exact main 重建 Manifest implementation successor。

## 7. Exact docs-only scope

本 candidate 只允许：

```text
README.md
AGENTS.md
docs/453-r1-source-snapshot-test-environment-patch-correction-publication.md
docs/milestones.md
```

workflow、runtime、tests、Schema、fixture、doc316–452、`docs/project-state.md` 与 primary `audit.json` 必须保持
`2a078fc…` base bytes。local gates 至少复算 exact scope、UTF-8/LF/final-LF、links/fences/headings、required markers、
`git diff --check`、global/local hygiene、doc452 qualified readback、formal failure boundary、diagnostic hashes、remote main 与 primary
audit continuity。

## 8. Qualification pipeline

```text
final docs-only publication bytes / declared local gates
    -> immutable PR body seal
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc452 / 本文 formal
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent retained-failure / diagnostic / correction-boundary reconciliation
    -> finite closeout + post-closeout integrity
    -> SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_ALLOWED
    -> return CONTROL LOOP
```

每个 formal identity 只运行一次；任何 non-success 保留原 identity。产品调用必须清除 GitHub token、`NO_PROXY`、
`PYTHONPATH` 与 `PYTHONHOME`，代理只按命令使用 `http://127.0.0.1:7897`。后继 PASS 不得覆盖当前 formal 四格失败、
serial v2 失败或任何 setup error。

## 9. 当前状态与生效条件

本文自己的最后门闭合以前只允许：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_STOPPED_PRE_COMMIT_FULL_MATRIX_FAILED_NOT_QUALIFIED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后才条件化变为：

```text
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_ALLOWED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_NOT_STARTED
```

随后必须返回 CONTROL LOOP，从新的 exact main 独立实施并资格化该单文件修正。本文不把 Manifest successor 升格为候选，
不恢复 global composition，不启动 public Review 或 R2–R6。`proof_is_not_problem_solving = true`、
`local_not_global = true`、`target_continuity_over_local_correction = true`继续成立。
