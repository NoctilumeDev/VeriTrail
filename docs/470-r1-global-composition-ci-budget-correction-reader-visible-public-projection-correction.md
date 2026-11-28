# R1 global composition CI budget correction reader-visible public-projection correction

日期：2026-11-29

> 状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造基线：`main@1809f291b23b7ae4a6a1c4db711548e43873bc8a`，tree
> `db9fb1b4ef971258d5447e85464df33fe6a9bfb5`。
>
> 最小责任：让PR #533预注册的doc468精确reader marker及其真实未资格状态在README默认读者可见区出现；不改变事实、oracle或实现。

## 1. 为什么仍需独立correction

PR #533的workflow修正本身通过original与exact-main双门，但fresh README diagnostic在`COMPLETE / HTTP 200`条件下观察到预注册marker
`R1 global composition authority exact-main CI budget correction`为0。doc467与doc468各自marker=1只证明两个局部目标可见，不能覆盖README
入口失败，也不能把源码中第1182行的链接当作默认读者已经看见。

PR #534没有修改这个投影。它只封存反例与责任边界，并在以下新exact-main world闭合自己的资格：

```text
merge main          = 1809f291b23b7ae4a6a1c4db711548e43873bc8a
tree                = db9fb1b4ef971258d5447e85464df33fe6a9bfb5
original Public CI  = 46176382601 attempt 1 / 15 of 15 SUCCESS
exact-main Public CI= 46181535692 attempt 1 / 15 of 15 SUCCESS
Browser Smoke       = 46181535691 attempt 1 / 1 of 1 SUCCESS
```

fresh README/doc467/doc468/doc469 Render observations与AGENTS/milestones raw-byte observations各自唯一PASS；独立reconciliation
SHA-256为`583af0de7571483ad953e6cb04b109582686366d6f73da7f89fce1cd3e348989`，140-artifact finite closeout SHA-256为
`8a5e032d8780cd80caf408198b9575abf1d575b87b3d3341e57746965034e6de`，finite integrity SHA-256为
`9b1dc90b71d56406b2051ebad033bc4f5a1094179a625d2cf67bf4a8e1a318e7`。因此doc469现在是
`READER_VISIBLE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`，但doc468仍`READBACK_NOT_QUALIFIED`，doc467仍`NOT_QUALIFIED / NOT_FROZEN`。

## 2. 保留的非成功事实

以下identity继续不可覆盖：

```text
PR #532 exact-main Public CI       = 46158724296 attempt 1 / CANCELLED
PR #532 gate artifact SHA-256      = 90cd4da3963429ac479f54d44edc648fce3539a32b2d272ec8a0ece8615e1ba1
PR #532 non-success capture SHA-256= 259979d3de37d74c88ba39edbb2056a8ef36681ed762f0d63fffdd72e9b86bf7
PR #533 README diagnostic identity = r1-p533-gcacibc-diagnostic-readme-1-c530824
PR #533 failed readback capture    = a2cb7b4c7e446f36282f7db0e9bcba697c584194241f04d82e9594ef0135b334
```

PR #534 fresh readback的wheel digest transcription、wrong-Python help、pre-formal proof-target与post-closeout display-path setup failures也按各自
identity保留；它们不改变最终PASS，也不允许删除。后继不得重跑PR #533 diagnostic、把PR #532改写为PASS或拼接不同world。

## 3. 被击穿的前提与最小修正

被击穿的前提不是“README没有任何相关文字”，而是：

```text
raw Markdown中存在doc468链接
    => 默认GitHub Public Render稳定窗口中的读者看到了预注册doc468 marker
```

真实反例已否定这个蕴含。理论遇到反例时检查前提，而不是增加例外。因此本候选只在README顶部R1状态块中使用同一个预注册marker作为
doc468链接文字，并同时说明：

- PR #532 exact-main仍是CANCELLED历史；
- doc468仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED`；
- doc467仍是`MERGED / NOT_QUALIFIED / NOT_FROZEN`；
- doc469只是qualified history；
- 本correction仍需自己的完整资格链。

它不换用无关的可见短语，不要求Collector滚动、展开或搜索，也不修改Public Render窗口或验收规则。

## 4. Exact scope与不变量

tracked scope只能是：

```text
README.md
AGENTS.md
docs/470-r1-global-composition-ci-budget-correction-reader-visible-public-projection-correction.md
docs/milestones.md
```

下列内容必须保持`1809f291…` base bytes：

```text
.github/workflows/**
src/**
tests/**
plugins/review-attention/src/**
plugins/review-attention/tests/**
docs/467-r1-global-composition-authority-private-implementation-candidate.md
docs/468-r1-global-composition-authority-exact-main-ci-budget-correction.md
docs/469-r1-global-composition-ci-budget-correction-reader-visible-failure-boundary-audit.md
all frozen contracts / fixtures / Schema / Provider / Collector / Core or P2 oracle
```

## 5. Local witness

local validation至少必须核对：

- exact base/head/tree与four-file scope；
- UTF-8 without BOM、LF/final LF、balanced fences、unique headings与links；
- README顶部同一个预注册doc468 reader marker唯一存在；
- doc469 closeout三项摘要与PR #532/#533失败identity完整保留；
- workflow、runtime、tests、doc467、doc468、doc469与全部semantic bytes无变化；
- Python 3.10/3.13 × normal/`-O` global/local hygiene、`git diff --check`与primary `audit.json`连续性。

local PASS只作witness，不使状态生效。

## 6. 资格链

```text
final four-file bytes / local witness
    -> original PR required Public CI
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc467 / doc468 / doc469 / doc470 Render
    -> fresh AGENTS / milestones raw bytes
    -> independent reconciliation
    -> finite closeout
```

任何non-success都按原identity保留；不得rerun洗白或重复已有PASS。全部闭合以前，本候选不产生资格。

## 7. 闭合后的authority ceiling

全部门成立后，只允许：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTED_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_EXACT_MAIN_CI_BUDGET_CORRECTION_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

它不自动资格化或冻结doc467。publication形成新事实后必须返回CONTROL LOOP，从新的exact main建立独立implementation qualification
recovery；不能继承PR #532/#533的旧资格，也不能直接启动public Review、外部开源系统集成、R2–R6或R1后的human+AI全项目检查。

## 8. Fail-closed条件

以下任一条件发生都必须停止并归层：

- original或exact-main gate不是SUCCESS；
- README默认reader-visible窗口中原预注册marker不是唯一1次；
- 任一formal/raw目标不是唯一PASS；
- remote main、commit、tree、parents、scope或target bytes漂移；
- doc467/doc468/doc469、workflow、runtime、tests、oracle或frozen bytes发生变化；
- primary `audit.json` SHA-256改变；
- reconciliation试图把doc469 history、doc468 correction与doc467 implementation合并成同一资格。

## 9. 当前机械状态

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_EXACT_MAIN_CI_BUDGET_CORRECTION_MERGED_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`proof_is_not_problem_solving = true`、`local_not_global = true`、`post_r1_human_ai_global_check_required = true`。
