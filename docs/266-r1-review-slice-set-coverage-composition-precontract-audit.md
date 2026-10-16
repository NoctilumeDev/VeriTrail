# R1 ReviewSliceSet / Coverage composition precontract audit

日期：2026-10-16

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDIT_CANDIDATE`。
>
> 基线：`main@ceaec8fce6b695a35f5eb5ea35847b6f60063b63`。
>
> 上游：[R1 总合同](113-r1-deterministic-semantic-slice-contract.md)、
> [post-Slice system audit](192-r1-post-slice-input-closure-slice-coverage-qualification-system-audit.md)、
> [Fact/Parse prerequisite correction](194-r1-fact-parse-observation-fulfillment-coverage-prerequisite-system-audit.md)、
> [Fact → Coverage handoff 私有实现冻结发布](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)与
> [composition current-state audit](265-r1-review-slice-set-coverage-composition-current-state-audit.md)。
>
> 影响：`L2_PRECONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本文只收敛 future
> ReviewSliceSet / Coverage composition 合同的最小语义面；不创建合同、runtime、tests、Schema、fixture、public carrier、
> persistence、Evidence、Bundle、publisher、CLI、Workbench、Core、AttentionProposal、tag 或 Release。

## 1. CONTROL LOOP 与 exact coordinate

doc265 已在本基线完成自己的资格链。PR #306 的 first original Public CI `38751708053` 因 outer timeout
`CANCELLED`，原身份永久保留；fresh independent original run `38755858920` 为 attempt 1 / 11/11 SUCCESS。
exact-main Public CI `38759957319` 与 Browser Smoke `38759957354` 均为 attempt 1 SUCCESS，分别 11/11 与 1/1。

fresh README/doc265/milestones 都取得 qualifying PASS；milestones formal attempt 1 的 GitHub Render
`PARTIAL / CONTENT_SCOPE_COUNT_MISMATCH` 保留为正式 ERROR，底层原因 `UNKNOWN`。independent reconciliation 为：

```text
e3961fc50a2317cdca2b36e41eae8bcd42419ef9b8ff48d59f12a912c9d164c8
```

修正 closeout 自包含枚举后的 149-artifact closeout 为：

```text
0c4a89aa1401e215a5d1e1c35e82bd4feef9393ff189178802695be815cebe1f
```

stale wheel key、stale summary filename 与首次 closeout 把自身 output 纳入枚举的失败继续留在 proof-facility / setup
层，不被最后 PASS 覆盖。由此当前事实是：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

remote `main` 与本基线一致；open PR 只有旧 Dependabot #293、#164、#163。primary checkout 中用户未跟踪
`audit.json` 不属于本审计，也不得修改。doc265 的新事实只授权本 precontract audit，不授权合同或 runtime。

## 2. 审计问题与停止线

当前问题不是“Coverage 应该有哪些字段”，而是：

> 哪一种最小 composition topology 能让已经冻结的 Fact-stage history、Relation qualification/admission 与 Slice closure
> 属于同一个可机械核账的 attempt，并且在 public boundary 上先形成 qualified ReviewSliceSet，再形成 Coverage qualification？

本文只回答：

1. composition 必须 join 哪两类不同 authority；
2. 哪些 topology 已被现有冻结事实直接否定；
3. 七个 stage 的 denominator 分别由谁拥有；
4. ReviewSliceSet admission 与 Coverage qualification 的顺序和 identity；
5. normal、closed-empty、conflict/blocked 与 unknown worlds 怎样保持可区分；
6. `U=3 / E=2` blocker 在现有 public vocabulary 上造成哪条 version stop line；
7. future contract 的最大语义面与 falsifier。

本文不选择类名、wire format、Schema 文件、successor version、persistence Route A/B、assembler、percentage UI 或发布形式。

## 3. Composition 必须 join 两类不同 authority

### 3.1 attempt-neutral exact semantic input

Relation observation 不能只消费一个 FactSet。当前冻结实现需要 `DerivationInputSet`，其中至少保有 exact
SourceSnapshot、sealed Policy、frozen Profile、verified source blobs 与 canonical input identities。该对象在 acquisition 后
copy-owned、immutable，可以在合同允许时复用同一个 exact semantic world。

### 3.2 one-shot live Fact handoff

`ClaimedFactToCoverageHandoff` 保有原始 `BudgetContext` 与完整 Fact-stage terminal history，包括 Parse partition、U/E、
projection blockers、逐 Provider responsibility/lifecycle、FactSet-or-absence 与 original attempt identity。它是 one-shot live
authority，不能由相同 bytes、digest 或重新构造的 BudgetContext 继承。

handoff 的 public document surface 只有 `document_copy`。序列化 source 不包含完整 SourceSnapshot、Policy、Profile bodies 或
verified blob bytes。因此：

```text
Fact handoff alone
    != complete Relation derivation input

DerivationInputSet alone
    != Fact fulfillment / continuation authority
```

future composition contract 必须显式 join：

```text
attempt-neutral, immutable exact DerivationInputSet
    +
one-shot live Fact handoff on the original BudgetContext
```

语义输入可以复用，不等于 live authority 可以复用。

## 4. Composition topology 裁决

### 4.1 被否定的 topology

| 候选 | 裁决 | 原因 |
| --- | --- | --- |
| 按 digest 拼接既有 Fact 与 Relation/Slice histories | **拒绝** | content equality 不继承 attempt 或 join authority |
| 给 Coverage 与 Relation 各复制一份 one-shot source | **拒绝** | 破坏 handoff/legacy source 的 exactly-one claim |
| 为 Relation/Slice 新建 BudgetContext 并重跑 Fact | **拒绝** | 形成另一 attempt 的 Fact truth，不能冒充 frozen handoff history |
| 让 Provider 自己取得 exact inputs 与 handoff | **拒绝** | Provider 无 denominator、claim 或 composition authority |
| 先造 public Ledger，再由 Ledger 反推 histories | **拒绝** | public shape/digest 不能成为 upstream fulfillment authority |

### 4.2 未被现有反例击穿的最小候选

当前唯一尚未被否定的最小 topology 是：

```text
one application-owned composition attempt
    -> revalidate exact immutable DerivationInputSet
    -> claim frozen Fact handoff exactly once
    -> keep original BudgetContext / attempt identity
    -> run successor Relation qualification and admission
    -> run successor private Slice obligation closure
    -> project and admit ReviewSliceSet
    -> qualify Coverage against the same owned history
```

这是 future contract 的候选 topology，不是 implementation feasibility 结论。本文没有证明现有 primitive 足以无改动实现它，
也没有授权 successor runtime。

## 5. 七阶段 denominator authority

Coverage 只能核账 authoritative universe，不能通过自己能表达或实际收到什么来定义考试范围。

| Stage | denominator owner | KNOWN 的最小前提 | 不允许的缩减 |
| --- | --- | --- | --- |
| `SNAPSHOT_INVENTORY` | exact terminal SourceSnapshot inventory | Snapshot terminal、identity/bytes 已资格化 | 只保留后续能读取的文件 |
| `POLICY_SCOPE` | Snapshot inventory；Policy 只拥有逐项分类 | 每个 inventory member 有 sealed scope terminal | 只统计 `IN_SCOPE` 输出并忘掉其他 terminal |
| `LANGUAGE_SUPPORT` | sealed Policy 中全部 `IN_SCOPE` entries | versioned total qualification 对每项闭合 | 用 `supported_paths` positive projection 作全集 |
| `PARSE_FULFILLMENT` | Language Support eligible parse units | 每项 parse terminal 与同 attempt reconciliation 闭合 | 只按 ACCEPTED products 反推分母 |
| `FACT_DERIVATION` | accepted products 上 frozen projection rule 枚举的完整 U | U enumeration、E/blockers、Provider responsibility 与 terminal history 闭合 | 用 E、actual Facts 或 representability 缩小 U |
| `RELATION_OBSERVATION` | declared observation domain 下的 relation-subject obligation universe | domain、responsibility、outcomes 与 admission 均资格化 | 用实际 candidates 或 partial prefix 定义完整 universe |
| `SLICE_CONSTRUCTION` | conflict-free admitted graph 上由 sealed Policy 枚举的 anchor/spec obligations | upstream branch 与全部 obligations/outcomes 闭合 | 把 conflict、zero anchor 与 missing obligations 混成 empty |

这些 universe 的 item kinds 不同。相邻 stage 之间必须有 frozen transition proof，不能用数量相等、digest 相等或 caller 提供的
数组顺序代替。例如 Snapshot item 到 Policy item、Parse product 到 Fact U slot、Relation outcome 到 Slice obligation 都需要各自
的 canonical transition relation。

## 6. ReviewSliceSet 先于 Coverage qualification

R1 公开依赖保持：

```text
FactSet -> RelationSet -> ReviewSliceSet -> CoverageLedger
```

因此 future application 必须先决定 private Slice closure 是否有资格投影并 admit 一个 ReviewSliceSet；CoverageLedger 再绑定该
qualified set 和相同 composition history。两者由同一个 application-owned composition owner 管理，但 identity 与 qualification
彼此独立：

```text
same Slice members
    != same qualified ReviewSliceSet

qualified ReviewSliceSet
    != Coverage qualification already complete
```

Coverage 不能参与 ReviewSliceSet identity 或 admission，R3 AttentionProposal 也不能通过 priority 反向缩小 R1 universe。

### 6.1 Slice branch 保真

| upstream private branch | ReviewSliceSet eligibility | Coverage implication ceiling |
| --- | --- | --- |
| `NORMAL_CLOSED` | 可形成 populated semantic set，仍需独立 admission | 可继续核账；不自动 COMPLETE |
| `CLOSED_EMPTY` | 可形成 admitted empty semantic set | 只证明已知 zero-anchor closed world |
| admitted Relation conflict / blocked receipt | 可形成 branch-bound empty semantic set | Slice denominator 为 UNKNOWN/blocked；绝不能冒充 `CLOSED_EMPTY` |
| missing/unqualified upstream | 不得取得 normal projection authority | Coverage 只能保留 unknown/incomplete，不能补造 set |
| interrupted/foreign attempt | 不得 admission | 不得拼入当前 composition |

semantic set 同为空，不代表 closure branch、authority history 或 Coverage disposition 相同。

## 7. Coverage applicability 与 terminal qualification

`NOT_APPLICABLE` 不能被含混地放进 denominator 内，与其他 terminal 并列。future contract 应先形成 authoritative applicability
partition：

```text
authoritative subject universe
    -> APPLICABLE
    -> NOT_APPLICABLE
```

然后只对 `APPLICABLE` members 形成 Coverage denominator 与 terminal qualification。最少要保持这些语义差异：

```text
COVERED
    obligation exists and qualified evidence fulfills it

MISSING
    obligation exists and qualified execution completed without required result

BLOCKED
    obligation exists and an exact typed upstream blocker is known

UNKNOWN
    available authority/history is insufficient to assign a normal terminal
```

这些只是 precontract semantic distinctions，不是 public Schema enum 决定。Coverage 可以映射已冻结的上游事实，不能重命名、
消除或事后解释上游失败。

## 8. U-slot identity 与 vocabulary version stop

`U=3 / E=2` projection-blocked world 已证明 blocker slot 的 `subject_key_digest` 是现有 `FACT CoverageItemRef` 的合法 item
identity。它不需要为了 identity 再造一种 item kind。

但 exact reason：

```text
UNREPRESENTABLE_EXPECTED_FACT
```

不在 Coverage 0.1 的 reason vocabulary 中。把它改写为 `DERIVATION_ERROR`、
`UPSTREAM_DENOMINATOR_UNKNOWN`、Parse rejection 或普通 missing 都会丢失 frozen semantics。

因此 future contract 必须设置硬停止线：

1. 先证明现有 vocabulary 能无损表达全部 required negative worlds；
2. 若这个具体反例仍不可表达，显式审查最小 versioned Coverage vocabulary correction；
3. correction 只扩被击穿的 reason/disposition boundary，不借机改变 item identity、denominator、public carrier 或其他 stage；
4. 在 version 决策前，不得把 shape-valid item 当作语义已 admitted。

本文只证明存在 version decision seam，不选择版本号、Schema 文件或迁移策略。

## 9. 三种资格不得合并

后继必须同时区分：

```text
private composition qualification
    histories 是否属于同一合法 attempt / owner / transition chain

semantic content qualification
    ReviewSliceSet members 与 Coverage partitions 是否满足 frozen rules

public closure binding
    public bytes 是否绑定 exact qualified identities 和 authority history
```

任何一层 PASS 都不能替代另一层。尤其：

```text
same content digest
    != same authority history

all local equations valid
    != cross-stage history valid

public serialization valid
    != private composition qualified
```

public carrier 与 persistence 继续保持 non-decision。若 future offline consumer 无法重新取得 exact inputs，是否需要 canonical derived
projection 应在消费边界有证据后单独裁决。

## 10. Future contract 的最大语义面

若本文完成自己的资格链，下一轮最多有资格起草一份 docs-only minimal composition qualification contract，冻结：

1. canonical composition semantic input identity；
2. exact `DerivationInputSet` revalidation 与 Fact handoff one-shot claim；
3. application-owned single-attempt composition owner；
4. successor Relation qualification/admission 和 Slice closure 的顺序及 authority ceiling；
5. 七阶段 denominator owner 与 applicability partition；
6. 相邻 stage transition proof 与 cross-stage reconciliation；
7. ReviewSliceSet semantic projection eligibility、admission 和 identity；
8. Coverage qualification 对同一 ReviewSliceSet/history 的 binding；
9. normal、closed-empty、conflict/blocked、missing、unknown 与 foreign worlds；
10. U-slot identity revalidation 和 exact blocker reason preservation；
11. 当前 vocabulary 不足时的最小 version-stop rule；
12. same-attempt continuation 只能在全部 required composition reconciliation 后签发。

下一合同仍不得授权 runtime/tests、Schema successor、persistence、public carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、
R2/R3、CLAIM_FIDELITY、tag 或 Release。implementation feasibility 与 authorization 必须另行取得。

## 11. 最小 falsifier 矩阵

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RCP-000` | exact inputs 相同、Fact/Relation attempts 不同 | digest equality 足以 join histories |
| `RCP-001` | handoff document 存在、exact input bodies 缺失 | document surface 足以运行 Relation qualification |
| `RCP-002` | immutable DerivationInputSet 存在、live handoff 未 claim | exact inputs 自动继承 Fact authority |
| `RCP-003` | handoff 与 legacy continuation 同时 claim | 可以复制 one-shot source |
| `RCP-004` | fresh Context 重跑 Fact 后得到相同 semantics | 新 attempt 可以继承原 handoff authority |
| `RCP-005` | U=3/E=2/actual=2 | E 或 actual outputs 可以缩小 FACT denominator |
| `RCP-006` | exact blocker item 可命名、reason vocabulary 无对应语义 | shape-valid item 足以把 blocker 改名 admission |
| `RCP-007` | two Providers 各完成 responsibility 一半 | 合并局部输出即可冒充逐 Provider complete |
| `RCP-008` | Parse denominator unknown | 下游 empty 可以变成 COMPLETE |
| `RCP-009` | Relation conflict branch 与 zero-anchor branch 都为空 | empty content 证明相同 closure semantics |
| `RCP-010` | Slice normal partial / frontier 未闭合 | admitted prefix 可以形成完整 ReviewSliceSet |
| `RCP-011` | Snapshot first stage empty、Policy next stage reappears | Schema/局部方程全绿证明 cross-stage continuity |
| `RCP-012` | Coverage 或 R3 priority 反向参与 Slice admission | 下游可以定义上游集合或考试范围 |

future contract 至少必须机械区分这些 worlds。happy path 不能代替 negative-world coverage。

## 12. 审计 witness

仓库外 audit 脚本只读 exact source、Schema 与 frozen fixtures，机械核对：

- handoff 保留 original Context/history，但 serialized source 不含完整 exact inputs；
- Relation qualification 需要 `DerivationInputSet` 与 source blobs；
- current Relation/Slice path 使用 fresh Context 且不消费 handoff；
- U/E blocker identity 合法、exact reason 不在 Coverage 0.1 vocabulary；
- false cross-stage Ledger 同时通过 Schema、digest 与逐 stage 局部方程，并输出 COMPLETE；
- public dependency为 ReviewSliceSet → CoverageLedger；
- normal closed、closed empty、conflict/blocked 三个 Slice branches 保持区分。

CPython 3.10.6 / 3.13.13、normal / `-O` 四个 fresh cells 均 exit 0、stderr empty，canonical report 逐字节一致：

```text
report bytes  = 2726
report SHA-256 = eafcb77cdf5454f033f0bdbb6e592bedb853507a0af49e3111e1ff3c8b3e36ae
```

六项聚合 assertion 全部为 true。测试只作 witness；它不证明 future implementation feasibility，也不把 current Schema、
public carrier 或 persistence 升格为已选择。

final-byte regression 的首次 3.10 normal 调用没有设置 repository `src` import path，27 项执行后在加载
`tests.test_markdown` 时以 `ModuleNotFoundError: veritrail` 停止，归为
`LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`。fresh attempt 2 只修调用方 `PYTHONPATH`，没有修改产品、测试、
oracle 或断言；3.10/3.13 normal/`-O` 四格各 31/31 PASS。首个 setup error 与四份终态日志同时保留。

## 13. 候选资格链与停止线

本文候选的 tracked scope 只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc113、doc120、
doc175、doc183、doc189、doc192、doc194、doc258–265、runtime、tests、workflows、Schema、Profile、Policy、fixtures、
identity vectors 与 corpus 必须保持 base bytes。

final bytes 必须完成声明的 Markdown/Schema regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态 marker、
四文件 scope、敏感字面量、上游 frozen-byte continuity、`git diff --check` 与 read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> precontract audit becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权 composition contract、Fact/Relation/Slice successor runtime、ReviewSliceSet/CoverageLedger assembler、Schema
successor、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag 或 Release。资格闭合后
必须重新进入 [CONTROL LOOP](working-method.md)，不能按文档编号自动起草合同。
