# R1 same-attempt DerivationEvidence manifest carrier successor最小合同0.1

日期：2026-11-15

> 候选状态：
> `R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
> 本文自己的完整资格链闭合以前不是qualified contract；即使闭合也只成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`，必须由
> 独立docs-only freeze publication完成全部最后门后合同才生效。
>
> 构造坐标：`main@ce4fe48356a088bee2d2cd12cc0bbaf590980925`；tree
> `cd395c903b2e9b96d480d7361d035f700023d0d9`。
>
> 上游：[manifest 0.2冻结合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)、
> [same-attempt continuity合同](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [private implementation冻结发布](411-r1-same-attempt-derivation-evidence-continuity-private-implementation-freeze-publication.md)、
> [implementation feasibility recovery audit](413-r1-review-derivation-manifest-successor-implementation-feasibility-recovery-audit.md)与
> [carrier seam precontract audit](414-r1-same-attempt-derivation-evidence-manifest-carrier-successor-precontract-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L2_CONTRACT + L0_DOCUMENTATION / CONTRACT_CANDIDATE_ONLY`。本文不创建或修改Schema、fixture、
> runtime、tests、workflow、Manifest、publisher、persistence、Provider、Collector、P2/Core oracle、Verdict或任何frozen semantic bytes。

## 1. CONTROL LOOP与qualified起点

PR #475把doc414 candidate
`base=af39730a4527157cc820d23ad40557f5d2c3de30 / head=101fffa801df1eb6dcd556323b0ca7469987a317 /
tree=cd395c903b2e9b96d480d7361d035f700023d0d9`精确合入本构造坐标。original Public CI `43715023036`与
exact-main Public CI `43717832528`均attempt 1 15/15 SUCCESS；Browser Smoke `43717832351`为attempt 1 1/1 SUCCESS，没有rerun。

fresh README/doc316/doc397/doc413/doc414各有唯一`FORMAL_READBACK_PASS`；AGENTS、milestones、legacy Evidence/Manifest Schema与七个
private source-test target各有唯一anonymous raw、Contents API与exact Git全字节一致PASS。anonymous rate diagnostic/preflight、
worktree attachment cap、source-marker regex与PowerShell revision query setup errors按原identity保留，qualification effect为`NONE`。

independent reconciliation、185-artifact closeout与finite integrity分别为：

```text
85c82705e91818b1465709bc8b0a3adaf1c199aa801ac0a5068bdfaa2b6ee557
01212800a12d4e8bd3d671e9aee56371fe2e71e670a6568a114887a5c7b069af
1d47fce0d6a6bead52d5c5673a7cef25c1963f8cf85a96357797cf075ce99577
```

因此doc414是`PRECONTRACT_AUDITED / QUALIFIED_HISTORY`。fresh CONTROL LOOP又核对remote main、exact tree、primary audit、当前open PR、
source与冻结合同；没有新反例击穿carrier seam，四个open Dependabot PR也不属于本因果链。当前最小合法动作只是冻结successor合同内容，
不是创建Schema或实现。

## 2. 合同目标与严格非目标

本合同只解决一个工程边界：

```text
committed same-attempt continuity
  -> versioned DerivationEvidence claim
  -> copy-owned exact snapshot carrier
  -> independent carrier conformance/admission
  -> future Manifest producer one-shot consumption
```

它不解决也不宣称已经解决：

```text
Manifest 0.2 runtime / publisher / Bundle
persistence Route A/B
global composition authority
Core sufficiency or Verdict
public Review product
language-support persistence
post-R1 global optimization
R2-R6
```

合同内容正确、合同资格成立、合同冻结、生效后的实现授权、实现完成与原工程问题解决必须继续分开。

## 3. versioned normative identities

本文选择下列唯一successor identities：

```text
contract function
    r1-derivation-evidence-manifest-carrier-successor/0.1

public Evidence Schema resource
    schemas/review-derivation-evidence-0.3.schema.json

public Evidence identity
    artifact_kind            = DERIVATION_EVIDENCE
    schema_version           = 0.3
    title                    = VeriTrail Review DerivationEvidence 0.3
    canonicalization_profile = veritrail-json-c14n/1

Evidence application-output binding
    r1-derivation-evidence-application-output-binding/0.1

private projection claim
    r1-derivation-evidence-successor-projection-claim/0.1

private exact snapshot carrier
    r1-derivation-manifest-snapshot-carrier/0.1

independent carrier conformance
    r1-derivation-manifest-snapshot-carrier-conformance/0.1

private carrier admission
    r1-derivation-manifest-snapshot-carrier-admission/0.1

one-shot consumer protocol
    r1-derivation-manifest-snapshot-carrier-consumption/0.1
```

unknown version、closest-version fallback、duck typing、subclass、string alias、legacy wrapper、equal bytes/digest或同一`derivation_id`字符串都
不能冒充这些identity。改变branch partition、Evidence binding denominator、carrier file universe、independent conformance、one-shot lifecycle或
authority ceiling必须显式version bump，不能静默修改0.1/0.3。

## 4. legacy Evidence 0.2与Manifest role/path immutable

下列对象继续逐字节immutable：

```text
schemas/review-derivation-evidence-0.2.schema.json
sha256 = 66190e12fad8c3bbec3615c25b1bbaf3cfb1ef723267e0e99185dcf05b8238e6

schemas/review-derivation-manifest-0.1.schema.json
sha256 = 69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
```

legacy Evidence 0.2的`COMPLETED`仍要求`relation_admission`，非成功状态仍不能报告Fact/Relation IDs；它不接受0.3，也不作为0.3 fallback。
Manifest 0.1与冻结的Manifest 0.2合同仍使用：

```text
role = DERIVATION_EVIDENCE
path = derivation-evidence.json
```

role/path不因Evidence version改变。future consumer必须先按exact `schema_version`显式dispatch；不得修改0.1/0.2 bytes、扩大旧enum，或让
legacy projector/consumer接受0.3。

## 5. DerivationEvidence 0.3的最小语义shape

0.3只允许从已提交的same-attempt continuity与exact unified application admission形成。它至少必须要求并绑定：

1. `artifact_kind`、`schema_version`与`canonicalization_profile`；
2. exact `derivation_id`与既有request provenance；
3. `source_snapshot_digest`、`policy_digest`、`analysis_scope_digest`、`slice_policy_digest`、`derivation_profile_digest`；
4. `terminal_branch`、`selector_route`与`continuity_variant`；
5. exact `continuity_digest`与`application_admission_digest`；
6. exact `coverage_ledger_digest`与`root_chain_digest`；
7. 0.3自身的`derivation_evidence_digest`。

discriminated binding必须完整且互斥：

| terminal branch | selector route | continuity variant |
| --- | --- | --- |
| `NORMAL_FULFILLED` | `RELATION_HANDOFF` | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |

0.3不复制Ledger的root binding state，不声明Fact/Relation/Slice必然存在，也不包含让caller自行选择route的union。它只绑定Ledger identity与
已admit的application output；actual child topology仍由CoverageLedger 0.3与stage owners决定。runtime/controller时间属于provenance，
不得污染Fact/Relation/Slice/Coverage的既有content identity。

## 6. public Evidence不是authority升级

Evidence 0.3可以公开序列化，是因为Manifest需要一份actual Evidence file；这不把private continuity对象本身公开，也不让Evidence取得
新的事实权威：

| owner | 继续拥有的authority |
| --- | --- |
| Reality / Provider | 自己实际观察到的事实及来源 |
| Source/Policy/Profile与各stage owner | 自己创建、校验与admit的exact bytes及stage语义 |
| CoverageLedger root bindings | Fact/Relation/Slice的present/qualified-absent/qualified-unknown topology |
| unified application admission | exact route/result的same-attempt application admission |
| continuity owner | 已提交attempt的input/controller/transition/result continuity |
| Evidence 0.3 | 对上述已admit identity的versioned claim；不新增事实 |
| private carrier | copy-owned byte handoff；不解释事实 |
| Manifest | role/path/digest transport；不裁决truth或sufficiency |
| Core | sealed Plan/session integrity、binding、sufficiency与Verdict |

业务层可以选择能力、安排顺序与请求补充条件，但不能因为0.3或carrier存在就宣布证据充分或`PASS`。

## 7. private copy-owned exact snapshot carrier

carrier candidate必须是不可公开构造、不可pickle/JSON恢复、不可复制的private one-shot value。它在同一live object graph中一次性copy-own：

1. `SourceSnapshot`、`ReviewPolicy`、`DerivationProfile` canonical exact bytes；
2. 刚形成并通过0.3 Schema与application-output binding conformance的Evidence exact bytes；
3. 仅对Ledger root为`ARTIFACT_PRESENT`的`FactSet`、`RelationSet`、`ReviewSliceSet` canonical exact bytes；
4. 已通过CoverageLedger 0.3 Schema/root-binding conformance的Ledger exact bytes；
5. 每份actual file的冻结role/path、raw SHA-256、`size_bytes`与既有semantic digest；
6. Ledger `root_chain_digest`、每个`binding_digest`与完整root topology proof；
7. exact continuity、application admission、attempt/context与one-shot lifecycle binding；
8. optional child的qualified absence/unknown证明，但不为其创建file record、empty document或placeholder digest。

carrier形成以后，producer、validator与future Manifest consumer都不得回读mutable path、stage private internals或重新调用Provider。carrier
也不得暴露可替换单项bytes的mutator、mapping或caller-selected constructor。

## 8. live topology与compatibility-only topology分离

live carrier正例分母是八个world：

| live world | Fact | Relation | Slice |
| --- | --- | --- | --- |
| normal consistent | present | present | present |
| normal branch-empty | present | present | present |
| normal slice-partial | present | present | present |
| normal relation-conflict | present | present | qualified unknown |
| zero parse denominator | qualified absent | qualified absent | qualified absent |
| all parse rejected | qualified absent | qualified absent | qualified absent |
| projection blocked | qualified absent | qualified absent | qualified absent |
| required Provider non-success | qualified absent | qualified absent | qualified absent |

doc316冻结fixture中的`Fact present / Relation qualified unknown / Slice qualified unknown`仍是Manifest/Coverage compatibility-only world；它没有
当前live selector/continuity route，不得由0.1 carrier projector伪造或当成第六live branch。Manifest conformance可以独立验证其静态bytes，
但live carrier admission必须拒绝无exact continuity/application admission的fixture object。

branch-empty、closed-empty与partial Slice都有actual admitted bytes，必须是present；relation-conflict不能重分类为negative；四个negative world
不能制造Fact/Relation/Slice placeholder。

## 9. independent conformance与admission

projection claim形成0.3 bytes与carrier candidate后，独立conformance必须不调用producer的expected-document projector，并从copy-owned raw
bytes与frozen rules独立复算：

1. 每份JSON的canonical bytes与exact version dispatch；
2. Evidence 0.3 required shape、branch/route/variant与digest；
3. CoverageLedger 0.3 Schema、root-binding conformance与root-chain digest；
4. Ledger topology与actual file presence严格一致；
5. role/path、raw SHA-256、size与semantic digest；
6. input digests、continuity、application admission、attempt与context identity；
7. unsafe/interrupted/revoked/incomplete/cleanup-failed world没有admission authority；
8. candidate尚未消费，且producer/validator未共享mutable projector state。

conformance成功只能签发exact private carrier admission；不能修改candidate、补文件、修Ledger、推断truth或产生Manifest/Verdict。第一次validation
成功或失败都消费candidate的validation opportunity；失败后不能用equal bytes/new wrapper恢复。admitted carrier只允许future Manifest producer
消费一次，任何replay、第二Manifest或并发竞争都必须fail closed。

## 10. typed private failure families

后继implementation至少必须可区分：

```text
MANIFEST_CARRIER_SUCCESSOR_VERSION_REJECTED
MANIFEST_CARRIER_PROJECTION_CLAIM_REJECTED
MANIFEST_CARRIER_EVIDENCE_BINDING_REJECTED
MANIFEST_CARRIER_LEDGER_CONFORMANCE_REJECTED
MANIFEST_CARRIER_TOPOLOGY_REJECTED
MANIFEST_CARRIER_CHILD_BINDING_REJECTED
MANIFEST_CARRIER_SNAPSHOT_MUTATION_REJECTED
MANIFEST_CARRIER_SAME_ATTEMPT_REJECTED
MANIFEST_CARRIER_CONTEXT_REVOKED
MANIFEST_CARRIER_COMMON_MODE_ORACLE_REJECTED
MANIFEST_CARRIER_LEGACY_ALIAS_REJECTED
MANIFEST_CARRIER_ALREADY_VALIDATED
MANIFEST_CARRIER_ALREADY_CONSUMED
MANIFEST_CARRIER_AUTHORITY_CEILING_REJECTED
```

这些是private proof failures，不扩既有public diagnostic enum，不归因到Reality、Provider或用户，不产生Verdict。底层原因无法从证据确定时
保持`UNKNOWN`。

## 11. normative falsifier matrix

| ID | falsifier | required result |
| --- | --- | --- |
| `DEMC-000` | 任一八个live world + exact continuity/admission/bytes | exactly one admitted carrier |
| `DEMC-001` | Evidence 0.2或unknown version进入0.3 path | version reject，无fallback |
| `DEMC-002` | branch/route/variant任一不匹配 | Evidence binding reject |
| `DEMC-003` | Evidence Ledger/root-chain digest与actual Ledger不一致 | reject |
| `DEMC-004` | equal bytes/digest但foreign attempt/context | same-attempt reject |
| `DEMC-005` | carrier形成前后任一owned bytes mutation | mutation reject并永久revoke |
| `DEMC-006` | present root缺file或non-present root存在file | topology reject |
| `DEMC-007` | absence/unknown被empty/placeholder file冒充 | topology reject |
| `DEMC-008` | branch-empty/closed-empty被当作absence | reject |
| `DEMC-009` | relation-conflict被改为negative或Slice present/absent | reject |
| `DEMC-010` | fixture-only Fact-present unknown伪造成live route | route/continuity reject |
| `DEMC-011` | role/path交换、重复、自定义或Ledger非最后一项 | reject |
| `DEMC-012` | raw SHA、size或semantic digest任一不一致 | child binding reject |
| `DEMC-013` | producer与validator共享expected bytes/projector state | common-mode oracle reject |
| `DEMC-014` | validator/consumer从path或private owner重读 | snapshot boundary reject |
| `DEMC-015` | stop/deadline/unsafe/interrupted/incomplete/cleanup failure | no admission |
| `DEMC-016` | validation replay、第二wrapper或两线程竞争 | 最多一次结果；其余reject |
| `DEMC-017` | admitted carrier被第二Manifest消费 | already consumed reject |
| `DEMC-018` | Evidence/carrier/Manifest宣布truth、sufficiency或Verdict | authority ceiling reject |
| `DEMC-019` | legacy 0.2 bytes、digest或consumer被修改 | immutable-history reject |

测试只能作witness。expected version、route、topology、role/path与digest rules必须由独立冻结向量枚举，不能通过调用被测producer生成。

## 12. implementation前置停止线

命中任一条件必须停止，只重开被击穿的最小合同边界：

- Evidence 0.3不能在不改0.2 bytes/semantics下显式dispatch；
- current continuity/application admission不能无损形成第5节binding；
- carrier必须重新读取path或依赖mutable shared projector；
- live relation-conflict或四个negative topology无法由Ledger机械区分；
- conformance必须由producer自我认证；
- carrier必须取得stage truth、Manifest、persistence、Core或Verdict authority才能实现；
- fixture-only topology必须伪造成live world才能通过；
- 必须同时实现Manifest 0.2、persistence或public Review才能证明本合同。

真实反例出现时先保留原identity与exact world，再显式version bump/reopen最小边界；不得增加例外、弱化oracle或用后继PASS覆盖。

## 13. 后继资格与状态上限

本docs-only candidate只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。Schema、fixture、runtime、tests、workflow、
Manifest、publisher、persistence、Core与全部frozen bytes保持base不变。

local gates至少重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、required markers、
immutable hashes、successor artifacts仍不存在、四格read-only semantic audit、focused regression、global/local hygiene、`git diff --check`与primary
`audit.json` continuity。随后依次：

```text
final docs-only contract bytes / declared local gates
  -> original contract PR Public CI 15/15
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc316 / doc397 / doc414 / 本文 Public Render
  -> fresh AGENTS / milestones / exact Schema/source-test raw+API+exact-Git byte observations
  -> independent source-byte / live-route / topology / authority-ceiling / retained-history reconciliation
  -> QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN
  -> return CONTROL LOOP
```

必须由独立docs-only freeze publication完成它自己的local/original PR/protected merge/new exact-main双门/fresh readback/reconciliation/finite
closeout后，`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN`才可生效。之后仍须返回CONTROL LOOP，独立
判断implementation feasibility；不得从本合同直接创建Schema、carrier或Manifest runtime。

本文自己的最后门闭合以前，只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

局部合同不等于完整R1或用户工程问题已经解决：

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
```
