# R1 DerivationEvidence manifest carrier successor 私有实现授权发布 successor

日期：2026-11-17

> 候选状态：`R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_SUCCESSOR_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@f21f310c1e99d5e7fa8b4f944d545f3163c9d627`，tree
> `ee8448d834c299f381140748a66ef49e94413103`。
>
> 上游：[最小合同 0.1](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)、
> [合同冻结发布](429-r1-manifest-carrier-successor-contract-recovery-freeze-publication.md)、
> [private implementation feasibility audit](430-r1-manifest-carrier-successor-private-implementation-feasibility-audit.md)与
> [PR #493 original-gate cancellation boundary](432-r1-manifest-carrier-authorization-original-gate-cancellation-boundary.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_SUCCESSOR_ONLY`。本文从新的 exact main 独立重建同一 bounded private
> implementation authority；不复用 PR #493 commit、run、qualification 或 metadata world，不修改 runtime、tests、workflows、fixtures、
> Schema、carrier、Manifest、persistence、Provider、public Review、Core Verdict、global composition authority 或 R2–R6。本文自己的
> 完整资格链闭合以前，`PRIVATE_IMPLEMENTATION_ALLOWED`不生效。

## 1. CONTROL LOOP 与当前成立的输入

PR #492 已把 doc430 精确合入`main@2b747deb7fdf4edc51668e02365da817e55c5e60`。original Public CI
`43956270989`、exact-main Public CI `43962198744`与 Browser Smoke `43962198868`均为 attempt 1 SUCCESS，分别
15/15、15/15 与 1/1。fresh 4 项 Render、6 项 raw-byte observations、independent reconciliation 与 finite closeout 均已成立，
所以 doc430 是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。

第一次 authorization publication PR #493 绑定：

```text
base  2b747deb7fdf4edc51668e02365da817e55c5e60
head  4dcc1a1f631e92b5c6430e0e17d7fe29726ee76d
tree  f5eb52d09837f7700f2b4327e45c5c91566b5a01
```

其 original run `43974353022` attempt 1 因 PR body `edited` event产生第二run `43974456082`，在同 ref
`cancel-in-progress`下被取消；两个 Windows aggregator 因 prerequisite 为`cancelled`而 FAIL。PR #493 已关闭、未合并、未资格化，
第二run的 qualification inheritance 为`NONE`，没有 rerun。

PR #494 随后只发布 doc432 failure-boundary audit，并精确合入当前 exact main：

```text
base  2b747deb7fdf4edc51668e02365da817e55c5e60
head  5932f8c7e9deba580b4a3eb1ef16e5a24e4e9729
tree  ee8448d834c299f381140748a66ef49e94413103
merge f21f310c1e99d5e7fa8b4f944d545f3163c9d627
```

original Public CI `43978322915`、exact-main Public CI `43983345552`与 Browser Smoke `43983345564`均 attempt 1
SUCCESS（15/15、15/15、1/1）。fresh README/doc430/doc432 Render formal 与 AGENTS/milestones/workflow raw-byte observations
各自唯一 PASS。README diagnostic #1 的`COMPLETE / HTTP 200 / marker 0 / ERROR`与 proof-target correction 均保留；没有重复该诊断。

independent reconciliation attempt 1错误地要求 adapter freeze v2 与其 v3 successor 的同名脚本哈希同时成立，按原 identity 保留；
v2 facility只保留旧freeze身份并按v3核最终文件，没有重跑任何产品观察。最终 reconciliation、173-artifact closeout、expected stdout
self-capture mismatch 与 finite integrity SHA-256 依次为：

```text
f0972144aecd7942c03b2ee048f18492b6fbdffd13b2707676e8a17a180c92c0
060830aceeccd6c0f962e908a11e0f13cee2ea56ed63ea16d0d660210f3eee1d
44a23fcc8c80b921959ec4125bdf1481c975c657b5d444fb68db629f12b43ba9
52a61f4611821ab604ab5a7d8e224c47821b1a349c9d6455e86bd4bcc28d6a33
```

因此 doc432 现在是`ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。PR #493 的 CANCELLED/FAILURE 与
closed/unmerged/not-qualified身份保持不变；该新事实只解除“另建独立 authorization successor”的阶段阻断。

## 2. 冻结输入与不继承的历史

本 successor 只消费以下冻结/资格化输入：

| input | SHA-256 / state |
| --- | --- |
| doc426 frozen contract semantics | `93e7033276e35890b8a390ec041e6bb64cc770ba0e3684900ee08f5d6a260800` |
| doc429 freeze publication | `ed9662a82aee491f3d9b0ccbd4c96ce89c1d5d98d69eb76ab35cc4548b70519c` |
| doc430 feasibility audit | `090c18e917b09029486d47c77bc797076182efc8a586dc02b7f4dc0517d4d834` / `QUALIFIED_HISTORY` |
| doc432 failure boundary | `fe973196b4a37033f9326fdffc022e3d5999b5cf4535382d6b0f53a7df7b2700` / `QUALIFIED_HISTORY` |
| Public CI workflow | `7efc5daa2f9f8e3b9bd52f208e4de0ca36f69a82bb6a6216274a04207fdca0c6` / unchanged |

以下 identity 只保留，不继承：

- PR #493 candidate head/tree、local seal、body、original run、edited-event run 与全部 qualification；
- original run `CANCELLED`、两个 Windows aggregator `FAILURE`与第二run inheritance `NONE`；
- doc430、doc432资格化过程中的全部 FAIL/ERROR/setup failure/UNKNOWN；
- 任何旧 worktree、old Plan/session、anonymous quota、render/raw observation 或 reconciliation authority。

新 PR body 必须在创建前完成并逐字节封存。original gate 终态以前不得执行会触发`pull_request: edited`的 metadata 修改；若 body
确有错误，保留该 world、关闭未合并并返回 CONTROL LOOP，而不是修改活动 PR 或用后继run覆盖。

## 3. 原工程问题、当前证明义务与适用世界

```text
original engineering problem
    为 future Review derivation Manifest 建立 same-attempt、copy-owned、
    可独立验真的 DerivationEvidence carrier

current proof obligation
    只发布 frozen doc426/doc429 + qualified doc430/doc432 允许的 bounded private implementation authority；
    不把授权、测试或未来 candidate 解释为 runtime 已存在或原工程问题已解决

applicability world
    exact main f21f310 source + frozen doc426/doc429 contract world
    + qualified doc430 feasibility world + qualified doc432 failure-boundary world
    + PR #493 retained CANCELLED/FAILURE/closed/unmerged/not-qualified identity

proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

若这些前提或适用世界漂移，即使本文本地或远端门仍绿也必须停止。授权只说明指定边界内可以施工；它不证明施工已经发生、结果正确、
用户问题已经解决或 global composition 已成立。

## 4. 唯一授权对象：bounded A–J

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，唯一允许的 private implementation scope 如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 新增显式 `review-derivation-evidence-0.3` Schema 与 exact-version dispatch；Evidence 0.2 与 Manifest 0.1 bytes、role/path、consumer 保持逐字节不变，unknown/closest version 无 fallback。 |
| B | continuity owner 只增加一个窄 private coordinate，返回它已 copy-own 的 inputs、transition、result、application admission、attempt/context 与 lifecycle binding；不得暴露 mutable state。 |
| C | 新建 versioned private projection claim 与 Evidence 0.3 projector，只从 B 的 exact material 和 frozen rules 形成 canonical bytes；不得回读 path、重调 Provider 或从 expected result 反推 route。 |
| D | 新建不可 public 构造、不可 copy/pickle/JSON 恢复的 one-shot exact snapshot carrier；copy-own exact Evidence、present child、Ledger、role/path、raw SHA、size、semantic digest、root topology 与 qualified absence/unknown proof。 |
| E | 新建独立 conformance owner；不得调用 producer 的 expected-document projector，必须从 copy-owned raw bytes 与独立冻结向量复算 Schema、branch/route/variant、Ledger/root-chain、topology、child binding、attempt/context 与 lifecycle。 |
| F | 正例分母固定为 doc426 的八个 live worlds；branch-empty/closed-empty/partial 保持 present，relation-conflict 保持 Slice qualified unknown，四个 negative world 不制造 placeholder；compatibility-only fixture 不能冒充 live route。 |
| G | 第一次 validation 成功或失败都永久消费 candidate validation opportunity；成功只能签发 exact private admission。admitted carrier 只暴露 future Manifest producer 的 one-shot consumption protocol，不在本阶段创建 Manifest runtime。 |
| H | wrong version/type/branch/route/variant、subclass/proxy/copy、foreign attempt/context、mutation、role/path swap、digest drift、common-mode oracle、replay、late stop 与 concurrent second use 全部以 doc426 typed private failure family fail closed；未知 lower cause 保持 `UNKNOWN`。 |
| I | Evidence 0.3、carrier、conformance 与 consumption protocol 不取得 Reality、Provider、stage truth、evidence sufficiency、Core Verdict、Manifest transport 或 global composition authority；public export 只限 frozen Schema resource。 |
| J | 把 `DEMC-000..019`、八个 live worlds、legacy compatibility、copy isolation 与 one-shot races 转成 focused tests；运行 CPython 3.10.6/3.13.13 × normal/`-O`、legacy/full regression、compile、hygiene、scope 与 audit continuity，形成独立 implementation candidate。 |

class、method、field、lock、retention 与文件布局仍由后继 implementation candidate 决定。测试只作 witness；expected version、route、topology、
role/path 与 digest rules 必须来自独立冻结向量，不能由被测 producer 生成。

## 5. authority ceiling 与 stop conditions

本文最后门闭合以后只允许实现 bounded A–J、增加 Evidence 0.3 Schema 与对应 private modules、增加 private tests/audit fixtures、运行
DEMC/八个live worlds/legacy/full/四格falsifiers并形成独立 implementation candidate。它不允许：

- 修改 Evidence 0.2 / Manifest 0.1 bytes、role/path或legacy consumer；
- 让 producer 自验、回读 mutable path、重调 Provider或伪造fixture-only live world；
- 让 carrier/Evidence/Manifest 宣布truth、sufficiency或Verdict；
- 实现 Manifest 0.2 runtime、publisher、Bundle或persistence Route A/B；
- 恢复global composition authority、关闭language-support persistence，或启动public Review、R2–R6、tag或Release。

后继施工遇到以下任一反例必须保留并停止：Evidence 0.3不能保持0.2逐字节兼容；continuity/application admission不能提供exact
material；carrier必须回读path或重调Provider；live/negative topology不能由Ledger机械区分；independent conformance只能调用producer
expected projector；one-shot边界不能绑定same attempt/context/root chain；bounded patch被迫同时实现Manifest/persistence/public Review/
Core Verdict/global composition；或`DEMC-000..019`只能通过弱化oracle、删除首败、拼接world、增加例外或重解释历史才能通过。

`PRIVATE_IMPLEMENTATION_ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。理论遇到反例先检查
前提与适用域，不不断增加例外。

## 6. 本 publication successor 的资格链

tracked scope 只允许：

```text
README.md
AGENTS.md
docs/433-r1-manifest-carrier-successor-private-implementation-authorization-successor.md
docs/milestones.md
```

doc426、doc429、doc430、doc432、`docs/project-state.md`、runtime、tests、fixtures、workflows、Schema、carrier、Manifest、persistence、Provider
与全部 frozen semantic bytes必须保持`f21f310…` base不变。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/
fences/headings、required markers、`git diff --check`、global/local hygiene、四份输入full-file SHA、PR #493/PR #494历史、primary
`audit.json` continuity、focused matrix 与 read-only feasibility audit。它们只作 witness，不冒充授权生效。

```text
publication successor final bytes / declared local gates
    -> immutable pre-created PR body seal
    -> original PR required 15/15 gate without metadata edit or rerun
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc430 / doc432 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones / workflow raw-byte observation
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个Render目标各运行唯一 diagnostic+formal；每个raw目标各运行唯一 anonymous raw+Contents API+exact-Git全字节对账。产品调用必须清除
GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。任何 non-success 保留原
identity；不得rerun洗白、重复已有PASS、编辑活动PR metadata或拼接不同world。

## 7. 当前 target 与停止线

全部门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_AUTHORIZATION_PR493_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_CANCELLED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_AUTHORIZATION_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_SUCCESSOR_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回 CONTROL LOOP，才允许在本文 ceiling 内建立新的 private implementation
candidate；不得把 authority publication、形式矩阵、doc430 feasibility 或 doc432 failure audit算作runtime证据。
