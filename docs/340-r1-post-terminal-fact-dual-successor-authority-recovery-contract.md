# R1 post-terminal Fact dual-successor authority recovery 最小合同 0.1

日期：2026-10-29

> 状态：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_CANDIDATE / NOT_FROZEN`。
>
> Exact source world：`main@328ba21aa885a51f99c234ed90bee7056e8a320f`；tree
> `a0b21cdc13af58c9db2b8709e291b2fd1a9dd0bf`。
>
> 上游：[positive ReviewSliceSet / Coverage composition freeze](314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)、
> [Fact → Coverage exact-input successor freeze](330-r1-fact-to-coverage-exact-input-successor-private-implementation-freeze-publication.md)、
> [negative-world Coverage authority recovery freeze](338-r1-negative-world-coverage-authority-recovery-private-implementation-freeze-successor-publication.md)与
> [Review / Coverage composition authority recovery current-state audit](339-r1-review-coverage-composition-authority-recovery-current-state-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结一个versioned、private、same-attempt、post-terminal
> dual-successor authority seam；不实现runtime，不生成Relation、Coverage、manifest、Evidence、persistence或public Review结果。

## 1. CONTROL LOOP 与qualified起点

文档339由PR #391以`base=4baf57268f6a06e584a4396b6d4e7a9d24735744`、
`head=35332adabb8bd7c9259680e4a5132dbda5b808ce`精确合入本基线。candidate与merge tree均为
`a0b21cdc13af58c9db2b8709e291b2fd1a9dd0bf`。original Public CI `40789265601`、exact-main Public CI
`40792519912`与Browser Smoke `40792519857`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。

fresh anonymous installed-product README/doc339/milestones各取得唯一`FORMAL_READBACK_PASS`。README formal #1与
milestones formal #1因匿名GitHub API budget exhaustion分别保留为`FORMAL_READBACK_ERROR`；后继独立identity才取得PASS，
错误没有被覆盖。independent reconciliation、191-artifact finite closeout、保留的stdout self-capture mismatch与finite integrity为：

```text
69ee5b048581dc3afa80401fd864339245148a7a20f1d07a8802f8c02440791b
dd056c1a795b7b912515c6d7fa85f1e7618560a394ee42f77a22797fd3d011fa
b3abc805297dfd94efc059c4434708bc5dfcdf08406131a097c3cd63b278d846
c89da379acdf8237f3e34550d7e354470ccf68160015c20a34ef44774c6bf89b
```

因此doc339已经成为`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。它证明：normal branch的positive composition与四类
negative branch的negative Coverage producer分别在自己的applicability内成立，五分支partition total且disjoint；但current Fact
consumer在terminal branch可知以前已经固定互斥handoff domain，wrong-route/fallback还会烧毁共享one-shot。当前缺口不是结果union，
而是一个能够在Fact terminal source成立以后、只签发唯一合法route claim的application-owned authority seam。

本合同只重开：

```text
pre-terminal Fact consumer domain selection
post-terminal branch-to-route qualification
shared one-shot dual-successor claim authority
```

Fact truth、Relation算法、positive composition、negative Coverage producer、CoverageLedger 0.3与所有历史合同字节保持不变。

## 2. 本合同解决的问题

current runtime存在两个分别正确、但不能由同一application attempt安全选择的入口：

```text
RELATION_TRANSITION
    -> NORMAL_FULFILLED only
    -> Relation handoff

LEGACY
    -> four negative terminal branches need exact-input successor 0.2
    -> negative Coverage producer
```

选择发生在Fact执行以前，合法route却只能在完整Fact terminal history形成以后确定。试错routing不安全：错误claim会消费或撤销live
authority，后继fallback不能取得第二份资格。由此：

```text
local positive validity
  + local negative validity
  + total/disjoint branch partition
  != consumable application route authority
```

本文冻结的修正不是允许两种handoff并存，也不是让application先试后退；它是一个新的private successor domain，在pre-terminal只绑定
完整world，在post-terminal完成独立branch重验以后，exactly once签发Relation或exact-input二者之一。

## 3. authority topology 与owner分离

规范拓扑为：

```text
qualified Parse closure + complete sealed Policy/Profile + original DerivationInputSet
    │
    ▼
versioned post-terminal dual-successor Fact consumer
    │ pre-terminal: execute Fact only; route authority = NONE
    ▼
complete Fact terminal closure / history
    │
    ├── NORMAL_FULFILLED
    │      └── one-shot Relation handoff claim
    │
    └── four negative terminal branches
           └── one-shot exact-input successor 0.2 claim
```

| owner | 可以决定 | 不得决定 |
| --- | --- | --- |
| sealed Policy/Profile | complete requirement/profile bytes、stage applicability inputs与digest | Fact terminal branch、route claim或downstream result |
| Fact consumer | Fact Provider assignment、execution与complete terminal history | 根据期望downstream提前选择route |
| dual-successor selector | 从original terminal source重验branch并签发唯一route claim | 修改Fact truth、缩小Policy/Fact denominator、生成Relation/Coverage |
| Relation handoff | normal world中的完整Fact handoff | negative Coverage或global composition admission |
| exact-input successor 0.2 | negative world中的original input truth与terminal source | Coverage candidate、validation或admission |
| positive/negative downstream | 自己冻结边界内的candidate/validation/admission | 定义dual-successor branch、恢复第二份claim |
| digest/content holder | 对应immutable bytes | attempt、BudgetContext、claim、consume slot或continuation authority |

route requester、Relation Provider、Coverage producer、UI、manifest与publisher都不能定义branch或恢复已消费authority。

## 4. versioned normative identities

本合同冻结以下semantic identities：

```text
contract function
    r1-post-terminal-fact-dual-successor-authority-recovery/0.1

Fact consumer handoff domain
    POST_TERMINAL_DUAL_SUCCESSOR_0_1

terminal route-selection function
    r1-post-terminal-fact-route-selection/0.1

shared claim function
    r1-post-terminal-fact-dual-successor-claim/0.1
```

它们定义semantic function，不预先选择Python class、module、field、wire shape或public Schema。`LEGACY`、`RELATION_TRANSITION`、
`FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`及其既有对象、历史与bytes不修改；新domain不是旧domain alias，也不能closest-version
fallback。旧consumer即使得到同样terminal branch，也不能把自己的claim升级为本文successor。

## 5. pre-terminal sealed state：可以创建，不能claim

successor必须在Fact执行前创建，以便同一application attempt拥有完整Fact execution；但创建只允许绑定：

```text
original DerivationInputSet object and canonical bytes
live BudgetContext object, limits, deadline and stop state
complete sealed Policy / Profile bytes and digests
Fact stage applicability /0.2 and complete owner partition
Parse closure, classification, accepted products and Provider assignment
Fact consumer attempt / source identity
contract, route-selection and claim function identities
one shared consume slot
```

pre-terminal状态只能是`SEALED_NOT_ROUTABLE`。在complete terminal closure形成以前，Relation claim、exact-input claim、branch query、
route preview或序列化恢复请求都必须fail closed并永久撤销本successor；不能以“尚未决定”返回一个可稍后复用的半claim。

successor不得通过选择`RELATION_TRANSITION`或`LEGACY`既有domain来实现本合同。它必须使用可区分的新domain，并保持两个旧constructor
及旧history逐字节兼容。

## 6. post-terminal branch partition 与唯一route

selector必须从同一original Fact consumer与complete terminal closure重新验证terminal history，并应用以下total、disjoint mapping：

| exact Fact terminal branch | 唯一合法route | 禁止route |
| --- | --- | --- |
| `NORMAL_FULFILLED` | Relation handoff | exact-input successor |
| `ZERO_PARSE_DENOMINATOR` | exact-input successor 0.2 | Relation handoff |
| `ALL_PARSE_REJECTED` | exact-input successor 0.2 | Relation handoff |
| `PROJECTION_BLOCKED` | exact-input successor 0.2 | Relation handoff |
| `REQUIRED_PROVIDER_NON_SUCCESS` | exact-input successor 0.2 | Relation handoff |

必须同时证明：

```text
known terminal branches = exactly the five rows above
every accepted terminal source maps to exactly one route
normal and negative route domains are disjoint
unknown / malformed / interrupted / foreign terminal source maps to no route
```

branch不能由requester参数、下游candidate类型、FactSet presence、Provider success count或Coverage producer输出反推。selector必须重验
terminal source的canonical bytes、branch-specific history与same-object binding；branch rewrite、history删项或equal-copy closure一律拒绝。

## 7. normal route保留完整Policy与Fact truth

`NORMAL_FULFILLED`route必须继续满足Fact → Relation correction `/0.2`的完整约束：

1. 绑定same sealed Policy/Profile，而不是只传Relation row或只传Fact row；
2. stage applicability `/0.2`对完整Policy形成total、disjoint、exactly-once owner partition；
3. handoff保留完整authoritative FactSet、accepted products、per-product MODULE closure、terminal history与original input identity；
4. Relation obligation projection从完整Fact truth机械推导，不通过过滤unhandled Fact制造兼容；
5. current corrected Relation Provider、assignment、qualification与admission仍由各自owner裁决。

本文只签发进入既有positive path所需的有限Relation handoff claim；它不生成RelationSet、ReviewSliceSet、CoverageLedger或positive
composition admission。

## 8. negative route保留original exact input与absence truth

四类negative branch只能签发冻结的Fact → Coverage exact-input successor 0.2语义。claim必须保留：

```text
original DerivationInputSet object and five digests
exact source/blob bytes and maps
same live BudgetContext
complete Fact terminal source and branch-specific history
same attempt / source / closure identity
```

dual-successor不生成Coverage candidate，也不替negative producer重枚举denominator。producer、independent validator与same-attempt
admission仍按文档332/338工作。`QUALIFIED_ABSENT`不能由route selector改写成empty FactSet/RelationSet/ReviewSliceSet，negative result也
不能恢复Fact/Relation/Slice authority。

## 9. shared consume slot 与永久撤销

两类route共享同一个不可复制的consume slot。状态机只能是：

```text
SEALED_NOT_ROUTABLE
    -> TERMINAL_READY(exact branch, exact route)
    -> CLAIMED_RELATION | CLAIMED_EXACT_INPUT

any invalid transition
    -> REVOKED
```

必须满足：

1. correct claim成功恰好一次；成功后任何第二次、另一route、并发请求或read-reclaim均拒绝；
2. wrong-route、pre-terminal claim、validation failure、foreign/equal-copy source、replay或version mismatch永久撤销slot；
3. 失败以后不能fallback到另一route，也不能创建copy-equal successor取得新slot；
4. shallow/deep copy、serialization、same bytes/digest或重新构造相同closure均不继承object-graph authority；
5. late cancellation、deadline、stop、input/source/history mutation或cleanup failure使本successor永久不可claim；
6. concurrent correct/wrong route竞争最多一个线程进入terminal claim；其余都拒绝，不能产生两个downstream object graphs；
7. downstream claim的每次读取继续重验successor、context、terminal source、route与consume state。

本文不允许“失败不消费、成功才消费”的optimistic fallback模型；这会重新引入doc339已经证明不安全的trial routing。

## 10. claim-specific independence 与common-mode防线

branch selector与两个downstream producer不能共享“由downstream期望结果推导branch”的关键错误因果链。至少要求：

- selector只从original Fact terminal closure与frozen Fact semantics重演branch，不读取Relation/Coverage candidate；
- Relation path不能用自己的applicability projector证明`NORMAL_FULFILLED`；
- negative producer不能用自己的denominator/root projector证明negative branch；
- application必须独立核对selector输出与terminal branch mapping；
- mutation falsifier必须证明：即使requester与downstream同时把branch、denominator或candidate改成自洽错误world，selector仍从original
  terminal source拒绝。

这里的independence是claim-specific，不要求所有代码、canonicalization或immutable source完全不共享；必须明确共同信任根与共同失效面，
不能把`expected == actual`冒充oracle正确。

## 11. typed failure families 与authority ceiling

后继implementation至少必须区分：

```text
DUAL_SUCCESSOR_INPUT_REJECTED
DUAL_SUCCESSOR_PRE_TERMINAL_CLAIM_REJECTED
DUAL_SUCCESSOR_TERMINAL_SOURCE_REJECTED
DUAL_SUCCESSOR_BRANCH_RECONCILIATION_REJECTED
DUAL_SUCCESSOR_WRONG_ROUTE_REJECTED
DUAL_SUCCESSOR_ALREADY_CONSUMED
DUAL_SUCCESSOR_SAME_ATTEMPT_REJECTED
DUAL_SUCCESSOR_CONTEXT_REVOKED
```

这些是private failure families，不修改既有Fact/Relation/Coverage reason enum。拒绝unsafe claim不生成合法`UNKNOWN`产品；它表示没有
route authority。

本文的authority ceiling固定为：

```text
post_terminal_relation_handoff_claim = conditional / one shot / normal only
post_terminal_exact_input_claim      = conditional / one shot / negative only
fact_truth                           = unchanged
relation_set                         = false
review_slice_set                     = false
coverage_ledger                      = false
global_composition_admission         = false
manifest                             = false
evidence                             = false
persistence                          = false
public_review                        = false
R2_R6                                = false
```

## 12. normative falsifier matrix

| ID | falsifier | required result |
| --- | --- | --- |
| `PTDS-000` | complete normal world请求Relation route | 恰好一个Relation claim；无exact-input claim |
| `PTDS-001` | 任一四类negative world请求exact-input route | 恰好一个0.2 claim；无Relation claim |
| `PTDS-002` | terminal closure形成前请求任一路由 | reject并永久revoke |
| `PTDS-003` | normal world先请求exact-input、再fallback Relation | 两次都不能取得authority |
| `PTDS-004` | negative world先请求Relation、再fallback exact-input | 两次都不能取得authority |
| `PTDS-005` | correct claim成功后请求另一route | second claim reject |
| `PTDS-006` | correct claim成功后同route replay | replay reject |
| `PTDS-007` | concurrent Relation/exact-input竞争 | 最多一个claim；只有branch合法route可成功 |
| `PTDS-008` | equal-copy successor/closure/input/context | same-attempt object binding reject |
| `PTDS-009` | terminal branch字段改写但history/digest同步重算 | original terminal-source revalidation reject |
| `PTDS-010` | normal route缩小Policy或Fact denominator | complete Policy/Fact truth check reject |
| `PTDS-011` | negative route删除一个original input/blob/history item | exact-input 0.2 revalidation reject |
| `PTDS-012` | requester与downstream共享错误projector并得到一致branch | independent branch reconciliation reject |
| `PTDS-013` | late stop/deadline/context revoke/cleanup incomplete | no route claim |
| `PTDS-014` | `LEGACY`或`RELATION_TRANSITION`对象声称新domain | exact version/domain reject |
| `PTDS-015` | 未知、第六branch、interrupted或malformed terminal | no route claim / fail closed |
| `PTDS-016` | single union carrier同时暴露两种live claim | construction/admission reject |
| `PTDS-017` | route claim直接声明Coverage/global composition完成 | authority ceiling reject |

后继feasibility与implementation必须在Python 3.10/3.13 × normal/`-O`比较canonical semantic report，并保留全部FAIL、ERROR、
CANCELLED、setup failure与UNKNOWN。矩阵相等只是witness；合同、live object binding与qualification pipeline拥有authority。

## 13. UNKNOWN、UNSAT 与本合同不决定什么

若后继feasibility尚不能构造满足本文的successor，只能记录`UNKNOWN / NO_QUALIFIED_CONSTRUCTION`。有限candidate全部失败不等于整个
候选空间UNSAT；只有穷尽本文明确且完整的bounded candidate space并提供机械不可满足性证明，才可声明`UNSAT`。

本文不决定：

- 最终Python class/module/field、wire Schema、manifest或serialization；
- route claim以后Relation/Coverage结果是否通过各自qualification；
- application-level unified Review/Coverage output admission；
- manifest successor、Evidence continuity、persistence Route A/B、publisher、CLI、Workbench或Core；
- public Review、post-R1 Benchmark、R2 Evidence、R3 Attention或human-work improvement；
- implementation feasibility、implementation authority或runtime施工时间。

即使本合同及后继实现冻结，仍须在新的exact main独立审计unified output admission；共同route不自动证明共同输出有资格。

## 14. candidate qualification 与停止线

本docs-only candidate只允许：

```text
README.md
AGENTS.md
docs/340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md
docs/milestones.md
```

doc339与更早合同/runtime/tests/workflows/Schema/Profile/Policy/manifest/Evidence/persistence/public Review/post-R1计划必须保持base bytes。
final bytes至少完成exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、unique marker、doc339 qualification与
upstream frozen-byte continuity、`git diff --check`、read-only global/local hygiene及声明的四格semantic/focused witness。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate / not frozen
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP for private implementation feasibility
```

candidate-local semantic audit在Python 3.10.6 / 3.13.13 × normal / `-O`四格得到逐字节一致report；audit source与
canonical report SHA-256分别为：

```text
47b5c4ab2185a51d2721ebfa37ae14b7dad02a6afd5e039e1886fe57722a8a4b
254cac8a3d722d8e5cc95f0c89859689ea4da411e768463aa75ecf38f13b9dae
```

focused matrix四格各运行214项，均为213 passed / 1 skipped，覆盖Language、Fact fulfillment、两个handoff、Fact → Relation、
ReviewSlice input join、positive composition与negative-world recovery。attempt 1的assertion/fragment error、attempt 2的falsifier coverage
incomplete，以及focused runner首次syntax setup error全部保留；它们的qualification effect均为`NONE`。这些finite witnesses只支持
合同candidate，没有实现或冻结authority。

当前只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_CANDIDATE_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate的完整资格链闭合后，最多成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。必须另建docs-only freeze publication；
不能从doc339或本合同直接修改runtime、恢复旧global composition authority、选择manifest/Evidence/persistence或启动public Review/R2–R6。
