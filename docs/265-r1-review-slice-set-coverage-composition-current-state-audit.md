# R1 ReviewSliceSet / Coverage composition 当前状态审计

日期：2026-10-15

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDIT_CANDIDATE`。
>
> 基线：`main@20dd549d3f07f7b9185215eb3c8377dcd0f13a2c`。
>
> 上游：[R1 总合同](113-r1-deterministic-semantic-slice-contract.md)、
> [post-Slice system audit](192-r1-post-slice-input-closure-slice-coverage-qualification-system-audit.md)、
> [Fact/Parse prerequisite correction](194-r1-fact-parse-observation-fulfillment-coverage-prerequisite-system-audit.md)、
> [Fact → Coverage handoff 合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)与
> [handoff 私有实现冻结发布](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_AUDIT + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只复核当前 private histories、
> public 0.1 identity/vocabulary 与 seven-stage composition 的 blocking seam；不创建或修改 runtime、tests、Schema、
> fixtures、public carrier、persistence、ReviewSliceSet、CoverageLedger、Evidence、Bundle、publisher、CLI、Workbench、
> Core、AttentionProposal、tag 或 Release。

## 1. CONTROL LOOP 与 exact coordinate

doc264 的最后门已经在本基线闭合。PR #304 original Public CI `38715944983`、exact-main Public CI
`38736844425` 与 Browser Smoke `38736844350` 均为 attempt 1 SUCCESS，分别 11/11、11/11 与 1/1。fresh
README/doc264/milestones 三个 formal observations 均 P1/P2 COMPLETE、Core PASS；independent reconciliation 为：

```text
830fa170391e1ae5689538337d4d62ebf47d550b44de5633a175830445b70108
```

156-artifact closeout 为：

```text
a5898cce497e89dbb95e86fd5286a8e39719705273ed9cdc02fe55a499050516
```

因此以下是当前 frozen upstream，而不是本文的 target：

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

remote `main` 与本基线一致；主仓只有用户未跟踪 `audit.json`，未进入本审计。open PR 只有旧 Dependabot #293、#164、
#163，没有并行 semantic PR。新事实授权重新审计 Coverage 前置边界，不自动授权 Coverage 合同或 runtime。

## 2. 本轮先审 composition topology，不先审状态枚举

冻结 handoff 已经能从 exact `OwnedProductFactClosure` 一次性交出完整 Fact-stage history：Parse partition、U/E、
projection blockers、Provider responsibility/lifecycle、FactSet-or-absence 与 original attempt authority。问题不再是 Fact
history 是否存在，而是 seven-stage ledger 的全部上游 history 是否已经属于一个可合法核账的 composition world。

当前源码实际存在两条不同的 private path：

```text
new Parse / Fact path
    -> OwnedProductFactClosure
    -> ClaimedFactToCoverageHandoff
    -> no production downstream consumer yet

historical Relation / Slice path
    -> new independent BudgetContext / attempt
    -> rerun historical Fact source operations
    -> construct its own FactSet
    -> Relation qualification / admission
    -> private Slice obligation closure
```

`_relation_derivation.py` 与 `_relation_observation_qualification.py` 均不导入 new `_fact_fulfillment` 或
`_fact_to_coverage_handoff`；`_review_slice_input.py` 消费 `OwnedRelationQualificationContinuation`，不消费 handoff。整个
production source 中除 handoff 模块自身外，没有 `ClaimedFactToCoverageHandoff` 或 fixed handoff consumer 的使用点。

这不证明历史 Relation/Slice runtime 有 defect。它证明 current private histories 尚未取得把下列两件事写成同一次
seven-stage fulfillment history 的 join authority：

```text
frozen Fact handoff history
    + independently executed Relation / Slice history
    != one authoritative seven-stage history
```

相同 Snapshot/Profile/Policy、相同 Fact semantics 或相同 digest 都不能替代这个 join。

## 3. One-shot source 不能被复制成两份 authority

handoff 与 legacy `ClaimedProductFactContinuation` 共享 `OwnedProductFactClosure` 的一个 mutually-exclusive source claim：

```text
legacy continuation first -> handoff rejected
handoff first             -> legacy continuation rejected
concurrent claims         -> exactly one winner
```

这项冻结行为防止一个 live Fact closure 同时给两个 consumer 各自签发 continuation authority。后继 composition 不能为方便
join 而复制 closure、重置 `__claimed`、复用相同 bytes/digest，或把两个独立 attempts 描述成一个 attempt。

当前 historical Relation/Slice path 并不依赖这个 legacy Fact continuation；它更早地从 `DerivationInputSet` 重新执行自己的
Fact/Relation chain。因此下一合同不能只决定“handoff 给 Coverage 还是给 Relation”。它必须先回答：

> 怎样让 Fact、Relation、Slice 的 authoritative histories 属于一个可机械验证的 composition topology，同时既不重跑已冻结
> Fact truth，也不复制 one-shot authority？

本文不预选 successor pipeline、fan-out capability、composition owner 或 persistence carrier。

## 4. U slot identity 可以表达，disposition 仍未取得资格

projection-blocked world 的实际结果为：

```text
U = 3
E = 2
blockers = 1
reason = UNREPRESENTABLE_EXPECTED_FACT
```

blocker slot 的 `subject_key_digest` 可按 doc120 的 frozen domain
`veritrail.review.fact-subject/0.1` 从 exact source anchor、subject space、ordinal、Snapshot 与 Profile 重算，结果精确等于：

```text
2c23e714673452e9118b0f9dcf45fc3ba05cefe49db95e0965271ae96c983e41
```

doc120 §10.1 已规定 `FACT CoverageItemRef.item_id = candidate subject_key_digest`。因此：

```text
{item_kind: FACT, item_id: exact slot subject_key_digest}
```

在结构上可以通过现有 common 0.1 Schema。过去把“没有合法 output Fact ID”直接外推成“public 0.1 完全不能命名该 U slot”
过强；后继不应为了 identity 本身先造新 item kind。

但这不授予 mapping authority。handoff implementation 正确地没有生成 Coverage item；只有 future Coverage contract 才能
决定 U slot 到 `CoverageItemRef` 的完整 revalidation 与 admission。更关键的是，Coverage 0.1 的 reason 闭集没有
`UNREPRESENTABLE_EXPECTED_FACT`，而 frozen handoff 又明确禁止把它偷换成 `DERIVATION_ERROR`、
`UPSTREAM_DENOMINATOR_UNKNOWN` 或 Parse rejection。因此当前状态是：

```text
slot identity is structurally expressible
    != item mapping is authorized
    != blocker disposition is semantically expressible
```

后继必须先证明现有 disposition vocabulary 可无损映射，或在具体反例支持下审查最小 successor/Schema；本文不预选答案。

## 5. Schema 自洽仍不能证明 cross-stage history

本文重新执行 doc192 `SCQ-001`。从 frozen `valid-complete` fixture 只把 `SNAPSHOT_INVENTORY` 改成 KNOWN empty，重算
denominator 与 Ledger digest，下一 `POLICY_SCOPE` stage 仍保留一个 entry。结果：

```text
SourceSnapshot inventory count        = 1
SNAPSHOT_INVENTORY denominator count  = 0
POLICY_SCOPE denominator count        = 1
Coverage Schema valid                 = true
all local stage equations valid       = true
overall_coverage_status               = COMPLETE
false ledger SHA-256                  = e0b3482234aa0dc444892d46510a3f04096ed8b35dc01c780365e96a57cc865e
```

所以 Coverage application 必须从 exact owned histories 重建七个 stage 的 denominator、terminal partition 与 cross-stage
continuity。caller 提交的 Schema-valid stages、digest、output members 或局部方程不能成为 denominator authority。

## 6. Public dependency direction 不能倒置

R1 冻结依赖仍是：

```text
FactSet -> RelationSet -> ReviewSliceSet -> CoverageLedger
```

`CoverageLedger 0.1` 顶层必须绑定 `slice_set_digest`；`ReviewSliceSet 0.1` 不绑定 Coverage digest。CoverageLedger 在 Slice
派生后单向核账，不能形成：

```text
ReviewSlice -> Coverage -> ReviewSlice
```

因此后继允许提前准备 stage history，但公共资格顺序仍必须是：

```text
private Slice obligation closure
    -> ReviewSliceSet semantic projection eligibility / admission
    -> seven-stage Coverage composition qualification
```

AttentionProposal 属于 R3，不进入本次 R1 composition，也不能反向筛选 ReviewSliceSet 或 Coverage denominator。

## 7. 当前裁决

| 问题 | 裁决 | 边界 |
| --- | --- | --- |
| frozen Fact handoff 是否足够提供 Fact-stage history | **是** | doc259–264 已冻结完整 normal/safe-negative source |
| current Relation/Slice history 是否来自该 handoff | **否** | 它在独立 attempt 内重跑 historical Fact source operations |
| current source 是否已有 production handoff consumer | **否** | handoff 只被 direct falsifier tests 消费 |
| 是否可以按 digest 拼接两套 histories | **否** | content equality 不继承 attempt/join authority |
| unrepresentable U slot 是否结构上无法命名 | **否** | exact subject digest 符合现有 `FACT` item ref identity |
| blocker 是否已有无损 Coverage disposition | **否** | exact reason 不在 0.1 vocabulary，重命名没有 authority |
| Schema/局部方程是否证明 seven-stage completeness | **否** | `SCQ-001` 仍可产生 false COMPLETE |
| 是否必须先选择 persistence | **否** | 当前问题是 live private composition topology；offline responsibility 仍 OPEN |
| 是否已可起草完整 Coverage contract | **否** | composition owner/topology、SliceSet admission 与 blocker disposition 尚未闭合 |

因此当前最小 blocking seam 不是一个 `CoverageInput` 对象，也不是五个新的 status 枚举，而是：

```text
authoritative upstream histories
    -> one application-owned composition topology
    -> ReviewSliceSet projection/admission
    -> seven-stage denominator + terminal partition join
```

## 8. 后继最小问题

如果本审计完成自己的资格链，后继最多有资格进行 docs-only composition precontract audit，分别回答：

1. **history owner**：哪个 application-owned object graph 同时拥有 Fact handoff、Relation admission 与 Slice closure；
2. **topology**：如何避免重跑 Fact、复制 one-shot claim 或跨 attempt 拼接；
3. **stage denominator owner**：七个 denominator 分别来自哪份 frozen history，何时是 KNOWN，何时只能 UNKNOWN；
4. **terminal mapping**：上游 typed failures 怎样无损进入自己的 Coverage dispositions，谁无权重新解释；
5. **ReviewSliceSet admission**：private normal/empty/blocked Slice closure 何时有资格形成公共 semantic set；
6. **cross-stage join**：怎样机械拒绝 stage omission、reappearance、foreign history 与 output-defined denominator；
7. **identity bridge**：U slot 到 `FACT` item ref 怎样按 doc120 重验，而不是把任意 digest 当合法 subject；
8. **version stop line**：只有现有 vocabulary 不能无损表达时，才审查最小 successor/Schema；
9. **authority ceiling**：composition qualification 不拥有 publication、Evidence、Bundle、R3 attention 或 human disposition。

这些问题未闭合以前，不得先设计 public assembler、Ledger builder 或 percentage UI。

## 9. 最小资格否定矩阵

| ID | 单变量 world | 必须拒绝的结论 |
| --- | --- | --- |
| `RSC-000` | Fact handoff 与 Relation/Slice history semantic inputs 相同、attempt 不同 | 相同输入/digest 自动形成一条履责历史 |
| `RSC-001` | current handoff 没有 production consumer | frozen producer 自动证明 downstream composition 存在 |
| `RSC-002` | handoff 与 legacy continuation 竞争同一 source | 可以复制 claim 让两个 consumer 都成功 |
| `RSC-003` | Snapshot 1 项、首 stage 0 项、下一 stage 1 项，Schema/方程全绿 | 局部自洽证明 cross-stage completeness |
| `RSC-004` | U=3/E=2，slot subject digest 可命名，exact blocker reason 不可表达 | shape-valid item ref 足以合法改名 blocker |
| `RSC-005` | actual FactSet 少于 U | output members 可以反向定义 FACT denominator |
| `RSC-006` | Coverage result参与 ReviewSlice identity/admission | 可以建立 ReviewSlice/Coverage 循环身份 |
| `RSC-007` | Attention projection只选部分 Slice | R3 priority 可以反向缩小 R1 Coverage universe |

后继必须保留这些反例；不能用一个 normal complete happy path 替代。

## 10. 本地审计与保留失败

审计脚本位于仓库外临时 evidence root，只读复用 exact source、test helper、Schema 与 frozen fixture；没有修改产品、测试、
fixture 或 oracle。attempt 1 因未把 repository `src` 加入 import path，以 `ModuleNotFoundError: veritrail` 停止；attempt 2
又因顶层与插件测试目录同名 `support.py` 的解析顺序错误而停止。两者均保留为 audit-harness setup ERROR。

attempt 3 的全部语义断言已经 PASS；报告仅因包含 interpreter version 字段而在 3.10/3.13 间出现两种 bytes。该字段不是
问题事实，attempt 4 将 runtime identity 移入 run manifest，未改产品、Schema、反例或断言。CPython 3.10.6 / 3.13.13、
normal / `-O` 四个 fresh cells 的 canonical report 逐字节相同：

```text
report SHA-256 = 89498f07c7d5b8cabaecf91e85b02c2484e56e94d871197f9a33c76ffeef5d78
run manifest   = 042a95716be695a98dffebd43c2e8e44bdd3cc63e2947c4e661072435a4c49e3
```

七项机械断言全部成立：blocker slot identity 可复算/通过 item-ref Schema、exact blocker reason 不在 Coverage vocabulary、
false ledger 通过 Schema 与局部方程、production handoff consumer 为空、Relation/Slice 不消费 handoff、公共依赖为
SliceSet → Coverage，以及 one-shot source 互斥。

测试只作 witness。它不把 current Schema升格为足够、不把 absence of consumer 解释成 runtime defect，也不授予下一合同。

## 11. 候选资格链与停止线

本文候选的 tracked scope 只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc113、doc192、
doc194、doc259–264、runtime、tests、workflows、Schema、Profile、Policy、fixtures、identity vectors 与 corpus 保持 base 字节。

final bytes 必须完成声明的 Markdown/Schema regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态 marker、
四文件 scope、敏感字面量、上游 frozen-byte continuity、`git diff --check` 与 read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> current-state audit becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权 composition contract、Fact/Relation/Slice successor runtime、ReviewSliceSet/CoverageLedger assembler、Schema
successor、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag 或 Release。完成资格后
必须重新进入 [CONTROL LOOP](working-method.md)，不能按 doc 编号自动起草合同。
