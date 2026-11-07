# R1 public project-state projection successor 0.7 contract

日期：2026-11-07

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_7_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@3bdf7cfd4d06d95955990f0336e098f5c27958a6`，tree
> `4d90d735b7599e166069bd8c2016b008b5ea6645`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_SEMANTIC_CORRECTION_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改runtime、
> tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、
> doc372–374历史字节、projection 0.5 frozen bytes、0.4 failed bytes或任何其他frozen contract。

## 1. CONTROL LOOP 输入：#426证明0.6本体仍然自相矛盾

PR #425/doc373曾试图把0.6 qualified candidate发布为frozen projection。它的自动门全绿，但fresh README diagnostic与exact
source comparison证明README主状态仍称0.6未资格化；所以doc373保持`MERGED / NOT_QUALIFIED / NOT_EFFECTIVE`。

PR #426/doc374只修正README并version freeze-publication responsibility：

```text
base                 = 46493dc86422a7648d283881239787526b3ea039
head                 = 7424db6be7cb5e8ddba34c28771e1e6811a6f053
ordinary merge       = 3bdf7cfd4d06d95955990f0336e098f5c27958a6
candidate/merge tree = 4d90d735b7599e166069bd8c2016b008b5ea6645
diff                 = 1 commit / 4 files
```

original Public CI `42340071297`、exact-main Public CI `42342585325`与Browser Smoke `42342585323`均attempt 1 SUCCESS，
分别为11/11、11/11与1/1；没有rerun。original qualification、protected merge与exact-main gate evidence SHA-256为：

```text
6409eb171ed20847d6682fbf838d3b3de551813f8442baf169b7e6cc9a5c2dd2
619ad0662494fb61619addcca455dec77dff7afff4594e95b05c19a200162534
e4562fe955c352c9b079c36b6145e950fb9851fd1a5e4742f47c6ba2ee5af399
```

fresh exact-main在任何产品observation前先检查原问题、证明义务与适用world是否仍连续。exact source显示：

```text
README primary state             = 0.6 QUALIFIED_CANDIDATE / NOT_FROZEN
project-state projection_status  = CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
project-state current fact       = 0.6尚未资格化或冻结
doc372/doc373/doc374 premise     = #424 fixed 0.6 as QUALIFIED_CANDIDATE / NOT_FROZEN
```

所以#426没有运行installed-product diagnostic、formal、raw formal或Core Verdict。exact contradiction与7-artifact failed
readback closeout SHA-256为：

```text
d54994eceeb9ca0148d28bf57fa082037965df06158266c0f759d307bffe5056
9d5aacd0290a7460fba697c7af57de77e24a1103e2bec4e76633cb54d3cd7c85
```

这不是marker target问题。若选择本页中另一个已存在字符串去跑formal，只能证明字符串存在，不能证明公开状态自洽；那会把形式
证明替代原工程问题。

## 2. 为什么必须version 0.7，而不是第三次发布0.6

doc374把被击穿边界判断为README public-state / freeze-publication responsibility，并显式不修改`docs/project-state.md`。#426
反例现在证明错误也存在于project-state semantic bytes本身。因此被击穿的已不只是publication表面，而是0.6 projection candidate
本体；0.6不能保持可消费qualification authority，也不能由另一个freeze publication直接升级。

本合同保留而不改写：

```text
#424 automatic/readback records = retained exact evidence
0.6 semantic qualification       = REOPENED BY LATER COUNTEREXAMPLE
doc373                           = MERGED / NOT_QUALIFIED / NOT_EFFECTIVE
doc374                           = MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_EFFECTIVE
projection 0.5                  = FROZEN HISTORICAL
projection 0.4                  = MERGED / NOT_QUALIFIED / NOT_FROZEN
```

0.7只version被击穿的公开投影语义与readback target boundary。它不重算、删除或重解释#424–#426任何原始attempt、setup failure或
`UNKNOWN`，也不恢复global composition authority。

## 3. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7`

0.7 candidate冻结以下合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因而没有自引用；
4. 0.6必须显示为semantic qualification reopened/not frozen历史，不能继续提供当前authority；
5. #425/#426必须继续显示各自exact gates、未开始的formal/Core Verdict与failed closeout；
6. fixed private `POST_TERMINAL_DUAL_SUCCESSOR_0_1` implementation仍只在其声明world内为`FROZEN`；
7. manifest、same-attempt Evidence continuity、persistence、public Review与R2–R6继续`NOT_STARTED / NOT_AUTHORIZED`；
8. Business Layer仍不能代替Core决定证据充分性，Core也不拥有Reality；本投影不获得事实、Seal、qualification或scheduler authority。

本candidate的milestones source binding为：

```text
kind      = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
bytes     = 637752
sha256    = 8c393b4e43b473972bcd855aa5e695ce10b84c7749dfbe9da0ffdb23a17d5785
blob_sha1 = be867e83f0eb3ad7205acbc38103c39f1a99b077
```

## 4. Exact scope与不变量

本candidate只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/project-state.md
docs/375-r1-public-project-state-projection-successor-0.7-contract.md
```

以下blob必须与base逐字节相同：

```text
docs/372-r1-public-project-state-projection-successor-0.6-contract.md
docs/373-r1-public-project-state-projection-0.6-freeze-publication.md
docs/374-r1-public-project-state-projection-0.6-readback-contradiction-correction-publication.md
src/**
plugins/**
tests/**
.github/workflows/**
audit.json
```

## 5. 资格链与fresh readback target

候选必须重新完成：local link/scope/source-binding/semantic review、原始PR门、受保护exact-head普通merge、新exact-main Public CI与
Browser Smoke。随后必须建立fresh detached exact-main worktree与全新证据根，只认该merge world，并通过匿名installed-product
观察验证：

| target | observation | 必须证明 |
| --- | --- | --- |
| README | Public Render + Contents API + Core | 0.7 candidate、0.6 reopened与#425/#426失败边界一致 |
| project-state | Public Render + Contents API + Core | identity/status/current fact/source binding/stop line内部一致 |
| doc372 | Public Render + Contents API + Core | 0.6原合同字节与历史身份未被改写 |
| doc373 | Public Render + Contents API + Core | 首次freeze publication仍未资格化/未生效 |
| doc374 | Public Render + Contents API + Core | #426 failure world仍保留且未生效 |
| 本文 | Public Render + Contents API + Core | 0.7 correction contract exact bytes可观察 |
| AGENTS | raw.githubusercontent + Contents API + exact Git | 完整字节一致 |
| milestones | raw.githubusercontent + Contents API + exact Git | 完整append-only历史字节一致 |

所有产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用
`http://127.0.0.1:7897`。任何FAIL/ERROR/CANCELLED/setup failure与`UNKNOWN`按原identity保留；不同target、attempt或world不能拼接。

全部target各自唯一PASS后，必须独立reconcile exact base/head/tree、原始PR、protected merge、exact-main gates、candidate source
binding、Public Render/API/raw/Git/Core identity与primary `audit.json`，再做finite closeout。

## 6. 候选上限与下一步

当前只允许：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FREEZE_PUBLICATION_MERGED_NOT_QUALIFIED_NOT_EFFECTIVE
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_READBACK_CONTRADICTION_CORRECTION_PUBLICATION_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_EFFECTIVE
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_7_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后，本文与projection 0.7最多成为`QUALIFIED_CANDIDATE / NOT_FROZEN`。publication形成新事实后必须返回
CONTROL LOOP；独立docs-only freeze publication未闭合以前不得写`FROZEN`，也不得启动manifest、Evidence、persistence、public
Review或R2–R6。

## 7. 机器可检索标记

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_SEMANTIC_QUALIFICATION_REOPENED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_READBACK_CONTRADICTION_CORRECTION_PUBLICATION_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_EFFECTIVE
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_7_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
