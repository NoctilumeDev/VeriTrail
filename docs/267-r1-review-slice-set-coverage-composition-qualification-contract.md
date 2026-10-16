# R1 ReviewSliceSet / Coverage composition qualification 最小合同 0.1

日期：2026-10-16

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_CANDIDATE`。
>
> 基线：`main@becf49db117be20ecdb4d860c1763ad7bc0eaae7`；tree
> `835a5648939d4b989d7db773e5af134af91bd687`。
>
> 上游：[R1 总合同](113-r1-deterministic-semantic-slice-contract.md)、
> [Schema 与 canonical identity 合同](120-r1-schema-and-canonical-identity-contract.md)、
> [ReviewSlice input / obligation closure 合同](189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md)、
> [Fact → Coverage handoff 合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)、
> [handoff 私有实现冻结发布](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)、
> [composition current-state audit](265-r1-review-slice-set-coverage-composition-current-state-audit.md)与
> [composition precontract audit](266-r1-review-slice-set-coverage-composition-precontract-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结 private composition qualification、
> `ReviewSliceSet` admission 与 seven-stage Coverage qualification 的最小语义；不创建 runtime、tests、Schema、fixture、
> public carrier、persistence、Evidence、Bundle、publisher、CLI、Workbench、Core、AttentionProposal、tag 或 Release。

## 1. CONTROL LOOP 与 qualified upstream

doc266 已在本基线完成自己的完整资格链。原 candidate run `38784791544` 的 outer-timeout `CANCELLED` 永久保留；
独立维护 PR #308 只恢复 Public CI Python job 的外层 timeout headroom，经 original Public CI `38788780236`、
exact-main Public CI `38792831098` 与 Browser Smoke `38792830916` 资格化为
`main@59708a6f6809d8f5ade794cfcaa7b7e73fb8633a`。doc266 semantic patch 在该主线上保持字节不变，PR #307
final head `ab24666f69b7fd92b506b974d203332d3c8129ad` 的 original Public CI `38797013986` attempt 1 / 11/11
SUCCESS，ordinary merge 形成本基线。

本基线的 Public CI `38830203256` 与 Browser Smoke `38830203238` 均为 attempt 1 SUCCESS，分别 11/11 与
1/1。fresh README/doc266/milestones installed-product observations 各自 P1/P2 COMPLETE、Core PASS，公开字节等于
同一 exact main 的 Git blobs。independent reconciliation attempt 1 的 stale key 与首次 adapter construction 的过宽
diff assertion 作为 proof-facility/setup failures 保留；versioned attempt 3 只修读取路径与 adapter 证明，不改产品、Plan、
Evidence、oracle 或 doc266 字节，并取得 PASS：

```text
independent reconciliation = 09d11235e5a50bb158049c6976e657431d94bf396faaa43befa746985b1895b3
127-artifact closeout       = c9b37740eb8665df2cbcafaabbdfaf79608510ce9fd6ffc7fa58abf90c9edf33
```

因此本合同消费：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDITED
```

重新核对 remote main、并行 PR、frozen contracts、Coverage 0.1 vocabulary、current private object graph 与 retained
counterexamples，没有发现需要重开 Fact / Relation / Slice、先选择 persistence 或直接修改 public Schema 的新事实。
当前代码仍没有 production handoff consumer，也没有现成 composition authority。因此当前最小合法问题是本语义合同，
不是 successor runtime、Schema correction 或 public Ledger assembler。

## 2. 本合同解决的问题

现有两类 authority 都已经成立，但不能互相替代：

```text
attempt-neutral immutable DerivationInputSet
    exact Snapshot / Policy / Profile / verified blobs

one-shot live ClaimedFactToCoverageHandoff
    original BudgetContext / attempt / complete Fact-stage history
```

前者足以让 successor Relation observation 在 exact source world 上运行，却不拥有 Fact fulfillment；后者拥有完整 Fact
history 与 live claim，却不携带 Relation 所需的全部 exact input bodies。相同 digest、FactSet、limits 或 semantic output
不能把两套独立 histories 拼成一条 authority history。

本合同冻结一条最小 composition qualification：application 在同一个 live attempt 中重验 exact inputs、领取一次 frozen
Fact handoff，顺序取得 successor Relation admission、private Slice closure、`ReviewSliceSet` admission，再对相同 owned
history 做 seven-stage Coverage qualification。它不把“收到 history”解释成 Coverage complete，也不让 Coverage 反向定义
upstream universe。

## 3. authority topology

| 对象 / 决定 | authority owner | 明确没有 authority 的主体 |
| --- | --- | --- |
| exact semantic input world | qualified immutable `DerivationInputSet` 与 frozen upstream contracts | caller、Provider、digest holder |
| live Fact-stage claim | original owned Fact closure / BudgetContext，通过 application one-shot source | equal bytes、fresh Context、serialized handoff |
| Relation observation domain / responsibility | sealed Policy/Profile 与 frozen Relation contracts | actual Relation outputs、successful Provider subset |
| Slice obligation universe / closure branch | sealed Policy 与 frozen Slice input/closure contracts | actual Slice members、Coverage、R3 priority |
| single composition attempt / execution order | application-owned composition function | Provider、public assembler、publisher |
| `ReviewSliceSet` semantic projection | frozen Slice content rules | Coverage result、Attention selection |
| `ReviewSliceSet` admission | application 对 exact Slice obligation history 的独立资格判断 | matching member digest、empty content、Schema validity |
| seven-stage subject universes / applicability | 各 frozen upstream owner及相邻 transition rules | Coverage output、UI、representability、actual members |
| Coverage terminal qualification / conservative join | 本合同的 application-owned qualification function | upstream Provider、ReviewSliceSet content alone |
| publication / Evidence / Verdict / human disposition | 后继独立 authority | 本合同与 private composition attempt |

核心分离为：

```text
semantic content identity
    != fulfillment / admission authority
    != same-attempt composition authority
    != Coverage qualification
    != public closure
```

## 4. semantic function 与完整 input identity

首版 composition qualification function identity 冻结为：

```text
r1-review-slice-coverage-composition-qualification/0.1
```

完整 semantic input 必须共同绑定：

```text
exact qualified DerivationInputSet semantic identity and bodies
exact claimed Fact handoff source / claim identity / original attempt
complete Parse partition, Fact U/E/blockers and Provider terminal history
sealed Relation observation domains, Provider responsibility and relation rules
sealed Slice anchor obligations, expansion policy and budgets
successor Relation qualification/admission history
successor private Slice assignment/outcome/closure history
ReviewSliceSet projection and admission function identity
seven stage transition / applicability / terminal qualification rules
composition qualification function identity
original BudgetContext object / deadline / stop state
```

任一 source digest、FactSet/RelationSet/SliceSet digest、public Schema object、closure document、normal continuation 或
caller-supplied stage 都不是完整 input identity。semantic summaries 可以在相同 exact inputs 与 function 下复算；live claim、
attempt、BudgetContext、one-shot ownership 与 continuation 必须重新取得，不能随 summary 复用。

## 5. one-shot single-attempt composition

唯一被本合同允许的 normative order 是：

```text
application creates one composition attempt
    -> revalidate qualified immutable DerivationInputSet
    -> claim frozen Fact handoff exactly once
    -> retain original BudgetContext / attempt identity
    -> construct successor Relation responsibility from sealed domain
    -> qualify and admit successor RelationSet
    -> enumerate and close successor private Slice obligations
    -> project ReviewSliceSet semantic content
    -> qualify and admit that ReviewSliceSet against exact closure history
    -> qualify seven Coverage stages against the same owned history
    -> reconcile all required transitions and terminal partitions
    -> only then permit same-attempt continuation
```

以下 topology 一律拒绝：

- 按 digest 拼接 historical Fact 与另一次 Relation/Slice attempt；
- 为 Relation、Slice 或 Coverage 复制 handoff source，或同时领取 legacy continuation；
- 在 fresh equal-limits `BudgetContext` 重跑 Fact 后继承原 handoff authority；
- 让 Provider、caller、Schema builder 或 publisher自行取得 exact inputs与 denominator；
- 先生成 public Ledger，再从 Ledger shape/digest 反推 fulfillment history；
- 以 persistence、cache 或 semantic summary 恢复已消费、失败或 revoked 的 live claim。

任一 revalidation、claim、required successor qualification 或 attempt safety 检查失败时，composition fail closed；已观察
prefix 可以作为 typed diagnostic history 保存，不能取得 normal `ReviewSliceSet` / Coverage publication authority。

## 6. stage subject universe、applicability 与 denominator

每个 stage 必须先区分三件事：

```text
S(stage) = authoritative subject universe entering the stage
A(stage) = subjects to which this stage's qualification applies
N(stage) = S(stage) - A(stage), with exact not-applicable provenance
D(stage) = A(stage), the qualification denominator
```

`N(stage)` 不与 `COVERED / MISSING / BLOCKED / UNKNOWN` 混成 denominator 内的 terminal；它仍须被完整保留，防止通过
删除“不适用”历史改变相邻 stage transition。各 stage 的 `S/A/D` authority 为：

| Stage | authoritative subject universe `S` | applicability / denominator owner | 不允许的缩减 |
| --- | --- | --- | --- |
| `SNAPSHOT_INVENTORY` | exact terminal Snapshot inventory obligations | Snapshot contract；该层适用项即其 inventory obligations | 只保留后继能读取的文件 |
| `POLICY_SCOPE` | exact Snapshot inventory members | sealed Policy 对每个 member 的 total scope classification obligation | 只统计 `IN_SCOPE` output；忘掉 excluded/unclassified terminal |
| `LANGUAGE_SUPPORT` | complete Policy scope terminal partition | 只有 sealed `IN_SCOPE` members 适用；total Language function拥有 denominator | 用 `supported_paths` positive projection 作全集 |
| `PARSE_FULFILLMENT` | complete Language terminal partition | 只有 Language-eligible units 适用；Parse contract/history拥有 denominator | 只按 ACCEPTED products 反推分母 |
| `FACT_DERIVATION` | accepted products 上 frozen projection rule 枚举的完整 `U` | 全部 constructible U slots 均适用；representability 不得缩小 denominator | 用 `E`、actual Facts、FactSet 或 Schema shape 缩小 `U` |
| `RELATION_DERIVATION` | sealed declared relation observation assignments | frozen Relation domain / Provider responsibility拥有 denominator | 用 reported candidates 或 admitted relations反推 domain |
| `SLICE_DERIVATION` | sealed Policy 枚举的 anchor/assignment obligations | frozen Slice input contract拥有 denominator | 用实际 Slice members、empty output 或 R3 attention缩小 obligations |

这里的语义集合不预选 public Schema 字段。若现有 0.1 `denominator` 字段把 input universe、applicability 与 qualification
denominator 压成一个结构，后继 feasibility 必须证明无损投影；不能让旧字段反向改写本合同的三层语义。

## 7. 相邻 stage transition proof 与 cross-stage reconciliation

每个相邻 transition 必须由 application-owned canonical relation证明，而不是只检查两个 stage 的局部集合方程。每个
transition 至少绑定：

```text
source stage qualified identity and complete terminal partition
transition function identity
which source terminals become next-stage subjects
which source terminals are not applicable downstream and why
next-stage subject identity construction
complete predecessor/successor mapping
same composition attempt identity
```

cross-stage reconciliation 必须同时证明：

1. 每个 next-stage subject 恰有合法 predecessor witness；不得从 foreign attempt 或未授权 source reappear；
2. 每个应流向下一 stage 的 predecessor 恰有 successor 或精确 typed blocker；不得静默消失；
3. not-applicable、failed、blocked 与 unknown predecessors 保持原语义，不能因下一 stage 没有 member 而消失；
4. source universe / transition authority 为 unknown 时，依赖它的 downstream universe 只能 unknown；
5. stage order固定为 Snapshot → Policy → Language → Parse → Fact → Relation → Slice，不得跳跃或回边；
6. 同一 item 在重叠 Slice 中只按 canonical identity 核账，不按出现次数扩张 denominator；
7. 所有 stage 与 transition 都绑定同一 composition attempt、exact input world 与 owned history。

因此 `SCQ-001` 的“上一 stage 0 项、下一 stage 重新出现 1 项、局部方程和 digest 全绿”必须被拒绝；局部 Schema validity
不是 cross-stage continuity authority。

## 8. ReviewSliceSet projection、admission 与 branch fidelity

public dependency 继续单向保持：

```text
FactSet -> RelationSet -> ReviewSliceSet -> CoverageLedger
```

Coverage 不得参与 `ReviewSliceSet` content identity 或 admission。application 必须先根据 exact Slice obligation history决定
projection eligibility，再独立 admit semantic set：

| private Slice branch | projection / admission rule | Coverage ceiling |
| --- | --- | --- |
| normal closed | 所有 assignment/outcome/reconciliation 完整后可投影 members并 admission | 只取得 set authority；不自动 COMPLETE |
| normal partial with frontier | 可投影 exact prefix/frontier并以 partial branch admission | 不得称 complete Slice closure |
| known zero-anchor `CLOSED_EMPTY` | 可 admit empty semantic set，必须绑定 zero-obligation proof | 只证明该 stage 已知 empty |
| admitted conflict / blocked | 只有完整 typed branch history时才可形成 branch-bound empty semantic content | 不得与 `CLOSED_EMPTY` 等价；依赖 stage保留 blocked/unknown |
| missing / unqualified upstream | 不得取得 normal projection/admission authority | Coverage 只能保留 unknown/incomplete |
| interrupted / foreign attempt | 不得 admission | 不得拼入当前 composition |

`slice_set_digest` 是 semantic content identity，不是 admission authority。相同 members 或相同 empty bytes 可对应不同 closure
branches；application 必须另有 exact admission identity绑定 composition attempt、obligation history、branch、RelationSet 与
projection function。本文不选择该 identity 的 public carrier；content equality 永远不继承 admission。

R3 `AttentionProposal` 只允许在 R1 closure 之后消费 admitted slices。priority、selected subset 或 human disposition 不能
反向改变 `ReviewSliceSet` members、Slice denominator 或 Coverage universe。

## 9. Coverage terminal qualification 与 conservative join

Coverage 只能对第 6 节的 `D(stage)` 做 terminal qualification。规范语义必须至少区分：

```text
COVERED
    obligation exists and its required terminal fulfillment is qualified

MISSING
    obligation exists; complete owned execution proves the required terminal result absent

BLOCKED
    obligation exists; a typed upstream or stage-local blocker prevents normal fulfillment

UNKNOWN
    available universe, transition, attempt or terminal authority is insufficient
```

这些名称描述合同语义，不预选 public enum。现有 stage-specific reasons 与 dispositions 可以作为投影候选，但 mapping 必须
无损、total、versioned；Coverage 不能把 blocker 改名成最接近的旧 reason，也不能把 unknown 解释成 ordinary missing。

stage qualification 规则冻结为：

- `COMPLETE` 只在 `S/A/D` 已知、每个 denominator member 均 `COVERED`、全部 not-applicable history与相邻 transition已核账、
  无 missing/blocked/unknown/frontier、对应 upstream set已取得 admission时成立；
- denominator 已知但存在 missing、typed blocked terminal 或 Slice frontier时只能 `PARTIAL`；
- universe、applicability、transition、attempt、required history 或 upstream admission authority不足时必须 `UNKNOWN`；
- 一个已知 stage-local blocker可以使本 stage `PARTIAL`，但若它阻止 downstream universe枚举，后继 stage必须 `UNKNOWN`；
- overall status 继续保守机械汇合：任一 `UNKNOWN` → `UNKNOWN`；否则任一 `PARTIAL` → `PARTIAL`；其余才是
  `COMPLETE`。

Coverage qualification 必须绑定 exact admitted `ReviewSliceSet` **及其 admission identity**、同一 composition history、七个
stage/transition identities。另一个 attempt 中内容相同的 set/ledger 不能移植；Coverage result 也不能反向修正 upstream
set、history 或 denominator。

## 10. U-slot blocker 与 mandatory version stop

projection-blocked `U=3 / E=2` world 已证明第三个 U slot 的 `subject_key_digest` 可按 frozen Fact subject domain 精确复算，
且满足现有 `FACT CoverageItemRef` shape。identity 不是当前 blocker。

现有 Coverage 0.1 reason vocabulary却没有：

```text
UNREPRESENTABLE_EXPECTED_FACT
```

把它改写为 `DERIVATION_ERROR`、`UPSTREAM_DENOMINATOR_UNKNOWN`、Parse rejection、ordinary missing 或 arbitrary Fact ID 都会
丢失 frozen semantics。因此本合同冻结以下停止线：

1. current Coverage 0.1 **不足以**无损发布这个 FACT_DERIVATION world；
2. successor implementation / Ledger assembly 开始前，必须独立审查并资格化最小 versioned vocabulary correction；
3. correction 只能扩被该反例击穿的 reason/disposition boundary，不改变 `FACT` item identity、U owner、其他 stage、public
   carrier 或 overall join；
4. 在 version 决策与资格闭合前，shape-valid item 不得获得 semantic disposition admission；
5. runtime 不得以兼容性、UI 简化或“最终仍是 PARTIAL”为理由静默重命名。

本文只冻结“必须停并做最小 versioned correction”这一语义，不选择版本号、Schema 文件、迁移策略或实现顺序。

## 11. total composition branches 与 continuation ceiling

composition qualification 必须对以下 worlds 作 total classification，同时保持各自 authority history：

| world | 最低可发布语义 | 禁止推导 |
| --- | --- | --- |
| all stages normal closed | admitted set + fully reconciled stage histories | 自动 COMPLETE；repository truth complete |
| known zero denominator / zero anchor | exact known-empty proof | 与 rejected、blocked 或 unknown empty 等价 |
| upstream rejected / unsupported | exact applicability / terminal history | subject 从更早 stage universe 消失 |
| Fact projection blocked | full U、E subset、blocker slot/reason | 用 E/actual output缩小 U |
| required Provider non-success | full responsibility与terminal history | successful subset补齐履责 |
| Relation conflict / unresolved | admitted typed conflict branch | 当作 zero relation或 empty closed Slice |
| Slice partial / frontier | exact partial members/frontier与obligation history | admitted prefix冒充 complete set |
| denominator / transition unknown | known prefixes与unknown cause | empty/current prefix变成 COMPLETE |
| unsafe / interrupted / foreign attempt | retained diagnostic/stop history | normal set、Ledger 或 continuation |

same-attempt continuation 只有在 required exact-input revalidation、one-shot Fact claim、Relation admission、Slice closure/
admission、所有 stage terminal partitions与cross-stage reconciliation全部完成后才能签发。continuation只携带当前 private
composition authority；它不授予 persistence、publication、R2 Evidence、R3 Attention 或 Core Verdict authority。

## 12. normative falsifier obligations

后继 feasibility / implementation 至少必须直接攻击这些 worlds；本节不冒充已有 runtime tests：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RSCQC-000` | exact inputs相同，Fact与Relation属于不同 attempts | digest equality足以 join histories |
| `RSCQC-001` | handoff document存在，exact input bodies缺失 | serialized surface足以运行 successor Relation |
| `RSCQC-002` | immutable exact inputs存在，live handoff未 claim | semantic world自动继承 Fact authority |
| `RSCQC-003` | handoff与legacy continuation并发领取 | one-shot source可以复制 |
| `RSCQC-004` | fresh equal-limits Context重跑 Fact得到相同 semantics | 新 attempt继承原 authority |
| `RSCQC-005` | U=3/E=2/actual=2 | E或actual outputs定义 FACT denominator |
| `RSCQC-006` | blocker item可命名，0.1 reason不可表达 | shape-valid ref可以改名 admission |
| `RSCQC-007` | two Providers各完成一半 responsibility | union output证明逐 Provider complete |
| `RSCQC-008` | Policy excluded member不进入 Language applicability | 它可以从历史中完全删除 |
| `RSCQC-009` | Parse denominator unknown、downstream empty | empty output允许 downstream COMPLETE |
| `RSCQC-010` | Relation conflict与zero-relation normal world内容相同 | empty content证明相同 branch |
| `RSCQC-011` | zero-anchor与blocked Slice都投影 empty set | same slice bytes继承 admission authority |
| `RSCQC-012` | Slice partial/frontier保留 admitted prefix | prefix可以形成 complete ReviewSliceSet |
| `RSCQC-013` | Snapshot前一 stage 0项、下一 stage reappear 1项 | 局部Schema/方程全绿证明transition valid |
| `RSCQC-014` | same set bytes来自foreign attempt | content identity足以绑定 Coverage history |
| `RSCQC-015` | R3只选择部分 slices | attention subset可以缩小R1 denominator |
| `RSCQC-016` | seven stage local equations全成立 | local consistency自动证明cross-stage completeness |
| `RSCQC-017` | complete composition semantic history存在 | composition自己拥有publication/Verdict authority |

happy path不能替代 negative worlds；Schema validation、测试通过或 canonical bytes相同都只作 witness。

## 13. persistence、carrier 与 authority ceiling

本合同只选择 same-attempt private composition semantics，不选择 Language Support persistence Route A/B，也不证明 offline/
public consumer能重建 live authority。可以缓存 attempt-neutral semantic summary；不得缓存、复制或恢复 claim、BudgetContext、
continuation、one-shot ownership或 admission authority。

具体 class、field、wire、storage、Schema、builder与public directory是 implementation non-decision。以下任一条件出现时必须
停在后继 feasibility / correction boundary：

- 只能修改 frozen upstream denominator、terminal semantics 或 branch identity才能实现；
- 需要按 digest拼接 foreign histories、重跑上游或刷新 BudgetContext；
- 需要让 Provider、Coverage、R3或publisher拥有 composition/denominator authority；
- 需要把 `UNREPRESENTABLE_EXPECTED_FACT` 静默映射进 Coverage 0.1；
- 需要用 persistence、Evidence、Bundle或public carrier补造 live authority；
- current public `ReviewSliceSet` identity无法与独立 admission authority无损绑定；
- 需要让 Coverage反向参与 Slice admission或定义考试范围。

本合同不授权 successor runtime/tests、Schema correction、assembler、persistence、public product、Evidence/Bundle/publisher、
CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。feasibility、version correction与implementation authorization均须
各自通过后继 CONTROL LOOP 和独立资格链。

## 14. 本候选自己的资格门

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc113、doc120、doc175、doc183、
doc189、doc192、doc194、doc258–266、runtime、tests、workflows、Schema、Profile、Policy、fixtures、identity vectors、
corpus与架构资产必须保持 base bytes。

final bytes的本地门至少包括：UTF-8 without BOM、LF/final LF、links/fences/headings、状态 marker、四文件 scope、敏感
字面量、上游 frozen-byte continuity、`git diff --check`与read-only hygiene；R1 Schema semantics、handoff、Slice join及相关
Markdown regressions按声明矩阵在CPython 3.10/3.13、normal/`-O`运行。测试只作 witness，不把 current Coverage 0.1或
absence of runtime升格为本合同实现。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate history
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN
    -> return CONTROL LOOP / version correction and feasibility remain separate
```

最后门闭合前只允许：

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

即使本合同以后冻结，也不自动授权 Schema correction、composition runtime、`ReviewSliceSet` / `CoverageLedger` assembler、
persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。下一步必须从新 exact
main重新进入 CONTROL LOOP；不得按文档编号自动施工。
