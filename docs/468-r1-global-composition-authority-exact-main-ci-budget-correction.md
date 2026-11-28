# R1 global composition authority exact-main CI budget correction

## 1. 文档性质

本文是独立的 CI proof-facility maintenance candidate。它保存 PR #532 的 exact-main 首败，并只修正随着
Review Attention suite 增长而失效的 job 外层预算。它不是 doc467 的 PASS、freeze publication、产品性能豁免，
也不授权 public Review、外部开源系统集成、R2–R6 或 R1 后的 human+AI 全项目检查。

## 2. Exact coordinates 与不可回填事实

```text
candidate base  = fc3345f032aa4df558cdb86b39284c22b5d99505
candidate head  = 3e06107453aff5e4ff32d6e03c003ef9fbaf37a9
candidate tree  = a9fe9b9672e830991d03c8ac00e3671ea5818a58
PR              = 532
original run    = 46154246322 attempt 1 / SUCCESS / 15 of 15
protected merge = 2d56c97db41a208d999bad017cb00cf99c48f66e
exact-main CI   = 46158724296 attempt 1 / CANCELLED / NON_QUALIFYING
exact-main smoke= 46158724268 attempt 1 / SUCCESS / 1 of 1
```

exact-main Public CI 的 Python 3.10 optimized Review Attention job `141021012091` 从
`2026-11-28T15:13:28Z` 运行到 `2026-11-28T15:58:32Z`，在 test suite 仍正常推进时收到
`KeyboardInterrupt` 与 `The operation was canceled`。随后 Windows jobs `141033207197` 和
`141033207238` 机械拒绝 `cancelled` prerequisite，四个后续 jobs 被跳过。remote main 在观察时仍是
`2d56c97...`，因此没有证据支持“被新 push 取代”的解释。

该完整 CANCELLED / FAILURE / SKIPPED 链永久保留。exact-main gate artifact SHA-256 是
`90cd4da3963429ac479f54d44edc648fce3539a32b2d272ec8a0ece8615e1ba1`；三项非成功 job 的独立
capture attempt 2 SHA-256 是
`259979d3de37d74c88ba39edbb2056a8ef36681ed762f0d63fffdd72e9b86bf7`。不得 rerun #532，
不得用后继 PASS 把它改写成成功，也不得启动 #532 world 的 fresh readback。

## 3. 归层

同一候选的 original PR Python 3.10 optimized job `141007259871` 在约 40 分 32 秒后成功；本地最终
四格 full suite 均为 725 reported，Python 3.10 为 722 passed / 3 skipped，Python 3.13 为
723 passed / 2 skipped。exact-main 取消日志没有测试 assertion failure，而是在 45 分钟 job 外层预算边界
中断正常运行的既有 UAO 路径。

新增 focused module 在本地 Python 3.10 `-O` 中仍为 10/10 PASS，耗时约 299 秒。该事实说明当前 suite
相对 45 分钟预算已经缺少可重复资格所需的余量；它不证明每个 runner 的剩余耗时，也不把运行时差异归因给
GitHub、Python、产品或单一测试。lower variance 保持 `UNKNOWN`。

## 4. 最小修正边界

唯一运行变更是：

```text
.github/workflows/ci.yml
jobs.review-attention.timeout-minutes: 45 -> 60
```

以下内容逐字节或语义保持不变：

- 725 项完整 Review Attention test denominator；
- Python 3.10 / 3.13 与 normal / `-O` 四格；
- 所有测试 assertion、falsifier 与产品 inner deadline；
- `fail-fast: false`、required Windows barrier 与下游 fail-closed 顺序；
- job/check 名称、产品源码、public Schema/export/CLI/publisher、Core、persistence 与 Verdict authority；
- doc467 的 `NOT_QUALIFIED / NOT_FROZEN` 状态。

60 分钟只为当前完整 suite 提供独立外层执行窗口，不改变任何工程声明的通过条件。若 successor 仍耗尽预算，
该 non-success 必须按新 identity 保留并重新归层；不得继续增加例外或跳过测试。

## 5. 本候选资格与 authority ceiling

本候选精确 scope 仅为：

```text
.github/workflows/ci.yml
README.md
AGENTS.md
docs/468-r1-global-composition-authority-exact-main-ci-budget-correction.md
docs/milestones.md
```

它必须重新通过 local validation、自己的 original PR attempt、protected merge、新 exact-main Public CI
15/15 与 Browser Smoke 1/1、fresh README/doc467/doc468 Render、AGENTS/milestones raw-byte observation、
independent reconciliation 和 finite closeout。全部成立后也只允许：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_EXACT_MAIN_CI_BUDGET_CORRECTION_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_MERGED_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回 CONTROL LOOP，从新的 exact main 建立独立 implementation qualification recovery。
该 successor 必须重新绑定 doc467 的 exact implementation bytes 与新 proof-facility world，完成自己的全部门，
而不是继承本 maintenance 的资格。
