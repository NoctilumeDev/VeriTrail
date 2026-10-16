# R1 ReviewSliceSet / Coverage vocabulary correction 最小合同 0.1

日期：2026-10-16

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_CANDIDATE`。
>
> 基线：`main@5ea7b001380e27c3e3a1e54d1675064f8d16b5a0`；tree
> `3f8e5177d4cfef661a70cf37873aeaee534720d5`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [独立冻结发布](268-r1-review-slice-set-coverage-qualification-contract-freeze-publication.md)与
> [vocabulary correction 当前状态审计](269-r1-review-slice-set-coverage-vocabulary-correction-current-state-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结 projection-blocked world 所需的 versioned、carrier-neutral
> reason + disposition vocabulary；不修改 Coverage 0.1、runtime、tests、Schema、fixtures、identity vectors、Profile、Policy、
> corpus 或 public directory，不选择 successor 版本号、Schema 文件、字段、class、migration、compatibility 或 persistence，
> 也不启动 composition feasibility / implementation、`ReviewSliceSet` / `CoverageLedger` assembler、Evidence、Bundle、publisher、
> CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 qualified upstream

文档 269 已从本基线完成独立资格链。PR #311 final head
`984ae8241b8f3513bc74762f23cf5260edbc131a` 的 original Public CI `38870827554`、exact-main Public CI
`38878798937` 与 Browser Smoke `38878798945` 均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1；Review
Attention 四格各为 `513 reported / 510 passed / 3 skipped`。

fresh README/doc269/milestones 三个 installed-product observations 均为 P1/P2 COMPLETE、Core PASS。首个 readback
facility 的 preparation ordering、gate-log parser、premature adapter freeze 与默认折叠 README marker 选择错误均保留；上游
doc268 closeout stdout 在 closeout mapping 建立后才写入的单文件 post-write mismatch 也按原 identity 保留。setup 2 的
classification correction没有改产品、Plan、Evidence 或 oracle，随后 independent reconciliation 与 117-artifact closeout 为：

```text
independent reconciliation = 041aa549bfe396bcdfd1b1ec8b774463eccba2c6585e326b88b525f8d5799a6d
117-artifact closeout       = afc10e8932ac94cb2ea5fc1464e152bf07ad6ebcea032c307cc2ab971d1569cd
```

因此本合同消费以下 frozen / qualified upstream：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

重新核对 remote main、并行 PR、Coverage 0.1、doc267–269 与 retained counterexamples，没有新的 semantic PR 或更早
authority seam。当前最小合法问题仍是本语义合同，不是 Schema successor、private composition runtime 或 public Ledger。

## 2. 本合同解决的问题

frozen `FACT_DERIVATION` world 已经拥有完整 Fact universe `U`、representable expectation subset `E` 与 exact blocker：

```text
U = 3
E = 2
blocker slots = 1
reason = UNREPRESENTABLE_EXPECTED_FACT
```

第三个 U slot 可以按 frozen Fact subject domain 精确命名，因此 item identity 不是 blocker。Coverage 0.1 却同时缺少 exact
reason 与独立 semantic-blocker disposition。只在 enum 中增加 reason，或把它放进 `execution_failed`，都会把 representation
blocker 改写成 Provider execution failure。

本合同冻结的最小 correction 不是具体字段，而是一个不可拆开的 semantic tuple：

```text
terminal_class      = BLOCKED
disposition_family  = SEMANTIC_PROJECTION_BLOCKER
reason              = UNREPRESENTABLE_EXPECTED_FACT
stage               = FACT_DERIVATION
item_kind           = FACT
```

缺少其中任何一层都不能获得 semantic admission。Schema-valid、同样导致 `PARTIAL`、相同 item digest 或相同 UI 文案均不能
替代这个 tuple。

## 3. function identity、input identity 与 authority owner

本合同的 semantic function identity 冻结为：

```text
r1-review-slice-coverage-vocabulary-correction/0.1
```

它不是 public CoverageLedger Schema version，也不预留 `0.2` 文件名。一次 qualification 的完整输入至少绑定：

```text
exact composition attempt identity
exact FACT_DERIVATION denominator identity
exact U-slot subject identity
complete frozen U / E / blocker history
blocker-producing projection function identity
blocker reason and provenance authority
same-attempt Fact closure / handoff / admission identities
coverage qualification function identity
this vocabulary correction function identity
```

authority 分配为：

| 决定 | authority owner | 明确没有 authority 的主体 |
| --- | --- | --- |
| U slot 是否存在、identity 是什么 | frozen Fact universe construction | Coverage、Schema、actual Fact output |
| 该 slot 是否不可表示及 exact reason | qualified Fact projection closure | Coverage、Provider、caller、UI |
| terminal class 与 disposition family mapping | 本合同的 application-owned correction function | old enum、field name、publisher |
| stage / overall conservative join | frozen composition qualification contract | reason producer、ReviewSliceSet content alone |
| public successor identity / carrier | 后继独立 Schema correction contract | 本合同与 private runtime |
| publication / Evidence / Verdict / attention | 后继独立 authority | vocabulary correction |

Coverage 只能验证并无损映射 qualified upstream reason；它不能发明、改名或删除 blocker。持有 reason 字面量、item digest 或
shape-valid object不等于持有 reason truth 或 disposition admission。

## 4. denominator 外 applicability 与 denominator 内 terminal partition

本合同沿用 doc267 的顺序：先决定 applicability，再分类 denominator member。

```text
S(stage)
    -> applicability partition
       -> NOT_APPLICABLE, retained outside denominator
       -> D(stage), each member needs one terminal qualification
```

`NOT_APPLICABLE` 不是第五个 terminal，也不能计入 covered / missing / blocked / unknown 分母。对 `D(stage)` 中的每个 member，
规范 terminal classes 保持：

```text
COVERED
MISSING
BLOCKED
UNKNOWN
```

其中：

- `COVERED` 需要 exact required fulfillment 的 qualified witness；
- `MISSING` 需要 complete owned execution 明确证明 required result absent；仅仅没有 output 不足；
- `BLOCKED` 需要 obligation 已知存在，并有 qualified typed blocker 阻止 normal fulfillment；
- `UNKNOWN` 表示 denominator、member、attempt、transition、history 或 terminal authority 不足。

absence of result 不能自动从 `UNKNOWN` 变成 `MISSING`；known blocker 不能为了避免 correction 变成 `UNKNOWN`；out-of-scope
history也不能从 `S(stage)` 中删除。

## 5. disposition family 与 reason ownership

terminal class 与 failure origin 必须分层保存。至少保持以下 distinction：

```text
BLOCKED / SEMANTIC_PROJECTION_BLOCKER / UNREPRESENTABLE_EXPECTED_FACT
    !=
BLOCKED-or-UNKNOWN / EXECUTION_FAILURE / PROVIDER_UNAVAILABLE-or-DERIVATION_ERROR
```

本合同新增资格的只有第一行。它的 applicability graph 固定为：

```text
stage == FACT_DERIVATION
item_kind == FACT
item identity == exact frozen U-slot subject_key_digest
reason == UNREPRESENTABLE_EXPECTED_FACT
reason provenance == qualified same-attempt Fact projection closure
```

任一条件不成立时，该 reason 不得进入 semantic-blocker family。尤其禁止：

- 把 `UNREPRESENTABLE_EXPECTED_FACT` 放入 execution-failure family；
- 把 `PROVIDER_UNAVAILABLE / DERIVATION_ERROR` 改名为 semantic projection blocker；
- 用 `UPSTREAM_DENOMINATOR_UNKNOWN` 替代已知 U slot；
- 用 arbitrary Fact ID 代替 exact blocker slot identity；
- 让 Coverage、Schema builder、Provider 或 caller生成新 semantic reason。

qualified execution failure 在 denominator/member/attempt authority 都完整时，可以保留为 typed execution-origin blocker；如果它
使 downstream universe、transition 或 terminal authority无法确定，依赖 stage必须是 `UNKNOWN`。无论哪条路径，execution origin
都不得与 semantic projection origin 合并。本合同不修改 Coverage 0.1 既有 `execution_failed` 语义。

## 6. total member qualification

application 对每个 applicable denominator member 必须机械执行：

```text
1. revalidate denominator / member / same-attempt / complete history authority
2. collect all qualified terminal witnesses
3. validate every reason against its owner, stage, item identity and disposition family
4. admit exactly one terminal class, or fail closed
```

规范结果为：

| 输入事实 | 结果 |
| --- | --- |
| applicability 为 false | `NOT_APPLICABLE`，保留在 denominator 外 |
| denominator/member/attempt/history authority不足 | `UNKNOWN` |
| 唯一 qualified fulfillment witness | `COVERED` |
| 唯一 complete-execution absence witness | `MISSING` |
| 唯一 qualified typed blocker | `BLOCKED`，同时保留 family + exact reason |
| 没有任何 terminal witness | `UNKNOWN`，不得猜成 missing |
| 两个或以上互斥 terminal witnesses | composition inadmissible；不得选择“优先级最高”的一个 |
| reason 未知、misbound 或 provenance 不足 | composition inadmissible；不得放入最接近的旧 bucket |

这里的 totality 是“每个合格输入都得到唯一结果，非法/矛盾输入被明确拒绝”，不是对非法世界任意选一个 terminal。reason
composition 必须消费完整 qualified reason set，不能依赖 check order 或 first failure；本合同只有一个新 semantic reason，后继
如需增加第二个 semantic blocker reason，必须重新审查 applicability、互斥性与 canonical composition。

## 7. stage aggregation 与 downstream ceiling

本合同不改变 doc267 的 conservative join：

- 只有 denominator、applicability、terminal partition、not-applicable history 与 transition 全部已知，且每个 member 都
  `COVERED`，stage 才能 `COMPLETE`；
- 任一 qualified `MISSING`、`BLOCKED` 或 frontier 使已知 stage至多 `PARTIAL`；
- 任一 denominator / transition / attempt / required-history `UNKNOWN` 使相关 stage为 `UNKNOWN`；
- overall status 为：任一 `UNKNOWN` → `UNKNOWN`；否则任一 `PARTIAL` → `PARTIAL`；其余才是 `COMPLETE`。

一个 known Fact semantic blocker可以使 `FACT_DERIVATION` 为 `PARTIAL`；如果该 blocker 使 Relation subject universe无法完整
枚举，`RELATION_DERIVATION` 及依赖 stage必须保留 `UNKNOWN`。Coverage 不能因为 blocker reason很精确，就补造 downstream
denominator，也不能因为最终 overall 仍是 `PARTIAL`，就省略 blocker provenance。

## 8. Coverage 0.1 immutability 与 successor discipline

以下 bytes / semantics 继续 immutable：

```text
schemas/review-coverage-ledger-0.1.schema.json
review-r1-schema-0.1 fixtures
0.1 identity vectors and digest domain
historical 0.1 Bundle / manifest identities
existing 0.1 consumer interpretation
```

0.1 对已有 world仍保持自己的 frozen validity；它不能无损表达本文的 projection-blocked world。任何实现本合同的 public/private
carrier都必须拥有显式不同于 Coverage 0.1 的 identity，并证明：

1. old 0.1 bytes没有变化；
2. new identity不会被 old consumer误认成 0.1；
3. semantic tuple不会被拆散、静默改名或只保留 stage-level reason；
4. canonical digest domain、fixture、vector与migration规则由后继合同显式拥有；
5. 无 successor carrier 时，composition 必须停在 publication前，不能回退写 0.1。

本文不选择 `0.2`、文件名、`blocked` 字段、tagged union、class 或 migration。具体 identity 与 shape 必须由独立 Schema
correction feasibility / contract 证明；“需要新 identity”不等于“本合同已经设计新 Schema”。

## 9. consumer boundary 与 version stop

same-attempt private composition可以在内存中消费本文的 carrier-neutral terminal tuple，但只有在本合同自身资格化之后，才有权把
该 tuple作为后继 Schema feasibility 的 frozen semantic input。它仍然不能：

- 写入 Coverage 0.1；
- 生成 public `CoverageLedger` 或 Bundle；
- 根据可表达 subset缩小 U；
- 改变 `ReviewSliceSet` identity/admission；
- 用 persistence恢复 live claim或跨 attempt拼接 history；
- 让 R3 attention subset改变 R1 denominator；
- 因为 private object“能表示”就宣称 public successor已存在。

若后继 feasibility 不能在保持 0.1 immutable、exact blocker tuple、four-way terminal semantics与 conservative join 的条件下
构造显式 successor identity，必须停在 Schema correction boundary。不得让 assembler、publisher或 UI 猜测缺失语义。

## 10. normative falsifier obligations

后继 Schema correction / feasibility 至少必须直接攻击以下 worlds；本节不冒充 runtime tests：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RSCVC-000` | U=3/E=2，第三 slot有 exact identity | E或actual Facts可以缩小 denominator |
| `RSCVC-001` | exact reason加入 Coverage 0.1 enum，但仍放在 execution failure | reason存在就证明 disposition正确 |
| `RSCVC-002` | blocker静默改名为 `DERIVATION_ERROR` 且 Schema-valid | shape validity保持语义 |
| `RSCVC-003` | known semantic blocker改成 `UPSTREAM_DENOMINATOR_UNKNOWN` | known world可以升级为unknown规避version stop |
| `RSCVC-004` | Provider未运行 | output absent证明`MISSING`或semantic blocker |
| `RSCVC-005` | qualified execution failure | 可以改名为semantic projection blocker |
| `RSCVC-006` | same member同时有covered与blocked witness | check order可以任选一个terminal |
| `RSCVC-007` | unknown semantic reason | 可以塞入最接近的existing bucket |
| `RSCVC-008` | Policy排除的subject | `NOT_APPLICABLE`是denominator内第五种terminal |
| `RSCVC-009` | Fact stage known blocker，downstream universe不可枚举 | downstream empty可以`COMPLETE` |
| `RSCVC-010` | successor shape可表达tuple | Schema shape自动授予reason/admission authority |
| `RSCVC-011` | 0.1历史Bundle与successor语义内容相似 | 可以原地改0.1或继承digest identity |
| `RSCVC-012` | public successor尚未选择 | private tuple可以冒充已发布Ledger |

happy path、stage-level `PARTIAL`相同或最终 UI 文案相同，均不能替代这些 negative worlds。

## 11. mechanical witness 与 non-decision

仓库外 read-only harness 在 exact main 上重新验证 Coverage 0.1 baseline、reason-only、silent rename、distinct blocked carrier，
并机械执行 11 个 carrier-neutral semantic worlds。canonical report SHA-256 为：

```text
6132507ebe296ce23d6648268038c15ce3cdfe9ed672a6dd3d4f27b882ab4131
```

它证明：

```text
0.1 baseline remains valid                         = true
reason-only correction is sufficient               = false
silent rename can remain Schema-valid              = true
0.1 has independent semantic-blocker carrier        = false
not-applicable remains outside denominator          = true
semantic and execution blocker origins stay distinct = true
conflicting terminal witnesses are inadmissible     = true
unknown reason requires a new contract              = true
public successor version / shape selected           = false
```

该 harness 是 contract witness，不是产品实现、Schema proposal或迁移工具。它不能把 Python dataclass、dict keys 或 classifier
branch当成后继 public object设计。

## 12. authority ceiling 与停止线

本合同不定义或授权：

```text
Coverage successor version / Schema / fixture / vector / class
migration / backward compatibility / public directory
composition private runtime / tests / assembler
ReviewSliceSet projection or admission changes
denominator / U / E / blocker production changes
persistence Route A/B
Evidence / Bundle / publisher / CLI / Workbench / Core
R2 / R3 / CLAIM_FIDELITY / tag / Release
```

任一后继若需要改变 frozen U owner、Fact blocker history、four-way terminal semantics、stage join、0.1 bytes或 same-attempt ceiling，
必须返回 CONTROL LOOP，只重开被反例击穿的最小边界。

## 13. 本候选自己的资格门

tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc267–269、runtime、tests、workflows、
Schema、Profile、Policy、fixtures、identity vectors、corpus与架构资产必须保持 base bytes。

final bytes的本地门至少包括：UTF-8 without BOM、LF/final LF、links/fences/headings、状态 marker、四文件 scope、敏感字面量、
上游 frozen-byte continuity、`git diff --check`与read-only hygiene；Coverage 0.1 Schema regression、contract semantic matrix及相关
Markdown regression按声明矩阵在CPython 3.10/3.13、normal/`-O`运行。测试只作 witness，不把本合同变成 Schema或runtime。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate history
    -> return CONTROL LOOP
```

在全部门闭合前只允许写：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权独立冻结发布、Schema correction feasibility、successor runtime/tests、composition feasibility/implementation、public
`ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、
tag或Release。候选资格闭合后必须重新进入 [CONTROL LOOP](working-method.md)，不能按文档编号自动施工。
