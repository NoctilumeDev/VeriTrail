# R1 ReviewSliceSet / Coverage root binding correction 最小合同 0.1

日期：2026-10-17

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_CANDIDATE`。
>
> 基线：`main@b2725e5069cfca0dde1e120192eb03d47fba8ff9`；tree
> `c7a06ecf58880762a4a6c1ec7eb220052e48e9b0`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [Schema correction 最小合同](273-r1-review-slice-set-coverage-schema-correction-contract.md)、
> [root binding 当前状态审计](279-r1-review-slice-set-coverage-schema-root-binding-current-state-audit.md)与
> [root binding correction 前合同审计](280-r1-review-slice-set-coverage-root-binding-correction-precontract-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结 CoverageLedger successor 的三段 root-chain
> 语义、identity、total classification、conformance 与 version / manifest 停止线；不创建或修改 Schema、manifest、
> runtime、tests、fixtures、vectors、Profile、Policy 或 corpus，不授权 Schema implementation、composition feasibility/runtime、
> public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence、Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 qualified upstream

文档 280 已由 PR #322 final head `9628b9334cad5cfb22327c7e28e833c3999608e5` 合入本基线。original Public CI
`39027041983`、exact-main Public CI `39029206479` 与 Browser Smoke `39029206492` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1；fresh README/doc280/milestones 各有且仅有一份 qualifying PASS。independent reconciliation 与
182-artifact closeout 分别为：

```text
ae9eba013266c43e430920754433455444171ac1747202de3ac9ce32b6c98144
4dc81ff765da8dde180dce25e79ec01111e4a6adbdad12f7dfabbc5572acab90
```

首个 readback setup 的 observation prefix 产生超过 64 字符的 Plan ID；它在任何 formal observation 以前以
`READBACK_PLAN_ID_SETUP_ERROR` 保留。fresh setup 使用较短 prefix，并在 observation 99 对全部 diagnostic/formal Plan ID
执行 `2..64` 硬断言。setup2 缺失 pip install log 与宿主拒绝递归删除命令的两个 setup/operator facts同样保留；它们没有产品、
合同或 formal qualification effect。

重新核对本基线、open PR、冻结合同、Schema、manifest、fixtures 与 closeout，未发现需要重开 Fact、Relation、Slice、
composition qualification 或既有 Schema correction 的新事实。本文因此消费：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_PRECONTRACT_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

当前最小合法问题是 versioned root-binding correction semantic contract，不是物化 Schema、升级 manifest或开始 composition。

## 2. 本合同解决的问题与 authority owner

CoverageLedger 0.1/0.2 的三个 required digest只能表示三份 artifact都存在的 world：

```text
fact_set_digest
relation_set_digest
slice_set_digest
```

它不能无损表示 qualified negative branch。省略字段会得到 shape failure；填入 empty、placeholder、foreign-attempt 或 synthetic
digest会伪造 artifact。问题也不能只修第一段：FactSet 不存在时，normal Relation derivation没有 authority启动；没有 admitted
RelationSet时，normal Slice derivation同样不能取得 ReviewSliceSet authority。

root decision 的唯一 owner 是 application-owned composition。各主体的 ceiling 为：

| 主体 | 拥有 | 不拥有 |
| --- | --- | --- |
| frozen Fact / Relation / Slice stage | 自己的 exact artifact、terminal branch、closure/admission或qualified non-success history | downstream root chain、Coverage status |
| application-owned composition | same-attempt ordered root decision、transition proof与cross-stage reconciliation | 改写 upstream branch、补造 artifact |
| CoverageLedger successor Schema | root carrier的局部shape、closed properties、version与cardinality | root truth、attempt、claim或admission authority |
| conformance function | exact candidate与same-attempt history之间的机械一致性 | 生成、修补或重分类candidate |
| manifest | 选定文件bytes、size与digest binding | child root semantics、absence或live authority |
| Provider / publisher / digest holder | 自己被授予的窄职责 | root decision、denominator或successor dispatch |

核心分离冻结为：

```text
upstream terminal truth
    != root semantic projection
    != live composition authority
    != Coverage stage status
    != manifest topology
    != public publication authority
```

## 3. successor identity 与 immutable versions

root semantics改变 CoverageLedger child identity。规范 successor冻结为：

```text
schema file              = schemas/review-coverage-ledger-0.3.schema.json
schema $id               = https://github.com/NoctilumeDev/VeriTrail/schemas/review-coverage-ledger-0.3.schema.json
artifact_kind            = COVERAGE_LEDGER
schema_version           = 0.3
canonicalization_profile = veritrail-json-c14n/1
ledger digest domain     = veritrail.review.coverage-ledger/0.3
root binding domain      = veritrail.review.coverage-root-binding/0.1
root chain domain        = veritrail.review.coverage-root-chain/0.1
terminal history domain  = veritrail.review.coverage-root-terminal-history/0.1
conformance identity     = r1-review-coverage-ledger-conformance/0.3
contract function        = r1-review-coverage-root-binding-correction/0.1
```

0.3必须保留 0.2 已冻结的 seven-stage、blocker、reason、canonical order与conservative join语义；只替换被新反例击穿的
三个 required digest root。0.1与0.2 Schema、domain、digest、fixtures、Bundle和历史consumer保持immutable。0.3不得用相同
stage bytes、相同最终status或相同artifact digest继承0.1/0.2 Ledger identity。

known-version dispatch扩展为精确registry：

```text
(COVERAGE_LEDGER, 0.1) -> exact 0.1 Schema/rules
(COVERAGE_LEDGER, 0.2) -> exact 0.2 Schema/conformance
(COVERAGE_LEDGER, 0.3) -> exact 0.3 Schema/r1-review-coverage-ledger-conformance/0.3
otherwise              -> UNKNOWN_CHILD_VERSION / fail closed
```

本文不让0.3 fallback到closest version，也不要求实现先公开发布0.2。是否只实现最新qualified successor由后继feasibility决定；
历史0.2合同不会因此被倒写成0.3。

## 4. ordered root chain 与 binding identity

0.3以一个ordered root chain取代三个平级required digest。root chain顺序固定为：

```text
FACT_SET -> RELATION_SET -> REVIEW_SLICE_SET
```

每个binding的规范semantic payload至少共同绑定：

```text
stage kind
binding state
exact producing/qualification function identity
exact terminal branch identity
versioned terminal-history projection identity
terminal-history semantic digest
artifact semantic digest or exact absence
artifact closure/admission semantic digest when present
predecessor binding digest or exact Fact handoff source digest
binding digest
```

字段名和private class不是本文的runtime承诺；但上述semantic members不得被省略、合并或从caller输入恢复。Fact binding以
frozen Fact→Coverage handoff semantic projection为predecessor；Relation binding精确绑定Fact binding digest；ReviewSlice binding
精确绑定Relation binding digest。root-chain digest按固定顺序绑定三个完整binding及root-chain function identity。

`terminal-history semantic digest`不是caller提供的不透明token。它必须由application使用
`veritrail.review.coverage-root-terminal-history/0.1`对stage-owned canonical terminal-history projection复算。该projection至少保留：

- 共同成员：stage、exact terminal branch、producing/qualification function、same-attempt source/claim semantic identity，以及
  complete terminal或exact known-prefix状态；
- Fact：frozen handoff / closure中的denominator、U、E、blocker与required/optional Provider responsibility / outcome partition，按
  该branch实际适用的成员完整投影；
- Relation：predecessor binding、relation obligation / responsibility universe、Provider terminal outcomes、conflict与admission branch，
  按该branch实际适用的成员完整投影；
- ReviewSlice：predecessor binding、Slice obligation universe、outcomes、frontier、closure与admission branch，按该branch实际适用的
  成员完整投影；
- `QUALIFIED_UNKNOWN`：已有known prefix、缺失的authority slot与typed cause；不得把未取得的成员补成empty或default。

不适用成员不得伪造，适用成员不得省略。两个world即使root state相同，只要denominator、responsibility、outcome、blocker、
terminal branch或known prefix不同，其terminal-history digest与binding identity就必须不同。

每个binding digest的构造为：移除自身digest，对完整binding payload执行`veritrail-json-c14n/1`，再使用
`veritrail.review.coverage-root-binding/0.1` domain计算semantic digest。root-chain digest同理使用
`veritrail.review.coverage-root-chain/0.1`。这些digest是可复算semantic identity，不是live claim、attempt、closure或admission
authority；相同bytes不能继承另一个attempt的composition authority。

## 5. 三种binding state与branch-empty规则

binding state只有以下三种规范语义。名称不预先强制最终JSON enum拼写：

| state | artifact digest | 必须证明 | 明确不等于 |
| --- | --- | --- | --- |
| `ARTIFACT_PRESENT` | exact semantic digest | artifact由该stage exact terminal branch产生并独立closure/admission；same-attempt predecessor合法 | bytes/digest holder拥有admission |
| `QUALIFIED_ABSENT` | 必须为空 | 完整terminal history明确证明该branch禁止或不产生artifact，且absence可由frozen rules复算 | empty artifact、missing field、unknown、execution prefix |
| `QUALIFIED_UNKNOWN` | 必须为空 | application拥有足够terminal authority证明当前不能取得present或qualified-absent结论，并保留exact known prefix/cause | ordinary missing、silent omission、unsafe attempt获得Ledger |

admitted branch-empty、known zero-anchor `CLOSED_EMPTY`、partial Slice与普通non-empty artifact都属于`ARTIFACT_PRESENT`：它们有
真实semantic content digest和独立admission，只是terminal branch不同。branch-empty不能使用`QUALIFIED_ABSENT`；两个empty
artifacts若branch/admission不同，也不能共享binding identity。

`QUALIFIED_UNKNOWN`只允许来自安全、完整、可归属的terminal source。interrupted、foreign-attempt、revoked claim、未完成
cleanup或unsafe release没有资格仅凭partial prefix生成0.3 Ledger；它们保留diagnostic history并fail closed。

## 6. total classification 与单向传播

application必须对以下world作total root classification，同时保留各自stage status所需的独立语义：

| world | Fact root | Relation root | ReviewSlice root | 禁止结论 |
| --- | --- | --- | --- | --- |
| normal fulfilled | present | present | present | artifact chain自动使Coverage COMPLETE |
| zero Parse denominator | qualified absent | qualified absent | qualified absent | 与all rejected共享absence identity；伪造empty sets |
| all Parse rejected | qualified absent | qualified absent | qualified absent | 与zero denominator等价 |
| Fact projection blocked | qualified absent | qualified absent | qualified absent | downstream stage status不是UNKNOWN；E缩小U |
| required Fact Provider non-success | qualified absent | qualified absent | qualified absent | successful subset补齐FactSet |
| admitted Relation conflict + independently admitted branch-empty Slice | present | present | present | empty Slice等于absence或`CLOSED_EMPTY` |
| Slice partial/frontier | present | present | present | partial artifact冒充complete closure |
| safely qualified upstream/transition insufficiency | exact known state | qualified unknown as applicable | qualified unknown as applicable | unknown被改写成empty/absent |
| unsafe/interrupted/foreign attempt | no admitted root chain | no admitted root chain | no admitted root chain | partial prefix产生normal Ledger |

表中的root state不预先决定seven-stage status。特别是projection-blocked world中，RelationSet/ReviewSliceSet absence可以被
application确认为predecessor禁止construction的`QUALIFIED_ABSENT`，而依赖stage的universe仍因无法完整枚举而保持
`UNKNOWN`。root absence与Coverage `UNKNOWN/PARTIAL/COMPLETE`属于不同函数。

单向chain必须满足：

1. downstream `ARTIFACT_PRESENT`要求predecessor `ARTIFACT_PRESENT`及合法transition/admission；
2. predecessor `QUALIFIED_ABSENT`只允许downstream在完整typed transition proof下成为`QUALIFIED_ABSENT`，否则是
   `QUALIFIED_UNKNOWN`；
3. predecessor `QUALIFIED_UNKNOWN`不能被downstream提升为present或qualified absent；
4. 每个downstream binding恰有一个predecessor digest，不接受foreign chain或caller-selected predecessor；
5. stage-owned terminal branch与history必须原样保留，root function不得把不同negative worlds重命名成同一个empty reason；
6. root chain与七阶段composition绑定同一exact input、attempt和one-shot composition claim。

## 7. conformance、canonical order与authority ceiling

JSON Schema只证明局部shape。0.3 conformance必须另外机械证明：

1. child self-description、root-chain function、version与digest domain精确匹配；
2. 三个binding顺序、stage、state、predecessor及所有digest construction正确；
3. present binding的artifact bytes、semantic digest、closure/admission与same-attempt source一致；
4. absent binding没有artifact digest，且terminal-history projection完整、total并由stage authority产生；
5. unknown binding没有artifact digest，保留known prefix/cause且没有取得unsafe live authority；
6. branch-empty artifact仍按present admission核验；
7. root chain与seven-stage denominator、transition、disposition、status及overall conservative join一致；
8. 0.2 blocker carrier与reason语义在0.3中保持；
9. candidate canonical arrays、canonical bytes、binding digests、chain digest与Ledger digest全部正确；
10. unknown child version、foreign attempt、replayed claim、placeholder/synthetic digest与post-result repair全部fail closed。

conformance不能创建root、选择“最接近”的branch、修补candidate或把Schema-valid升级为semantic admission。0.3 Ledger即使通过
shape与digest，也只在same-attempt composition authority完整时取得private semantic admission；本文不授予public self-contained
verification或publication authority。

## 8. manifest compatibility matrix与独立停止线

`review-derivation-manifest-0.1`保持immutable。兼容矩阵冻结为：

| 0.3 world | manifest 0.1资格 |
| --- | --- |
| FactSet、RelationSet、ReviewSliceSet均present，且CoverageLedger 0.3已知version/conformance | 现有`COMPLETE` topology可以绑定四份derived artifacts；child仍独立dispatch为0.3 |
| 任一set qualified absent或qualified unknown，同时存在CoverageLedger 0.3 | `COMPLETE`缺required set；`DIAGNOSTIC`禁止Ledger，因此两者都不合格 |
| unsafe/interrupted/foreign attempt | 不得借任一manifest outcome发布Ledger |

child root semantics与transport topology是两个seam。本文不把absence塞进manifest `semantic_digest`，不修改COMPLETE/DIAGNOSTIC，
也不选择manifest successor的版本、role、path或file cardinality。negative-world public publication若要成立，必须另行审计并冻结
manifest/topology successor；在此以前，0.3最多是private qualified child，不能伪装成完整public derivation bundle。

## 9. persistence与implementation stop conditions

本合同不选择persistence Route A/B。terminal-history digest与root-chain semantic projection可在same-attempt live graph中复算；
这不证明离线consumer能够重新取得exact history，也不把serialized projection变成live authority。

后继feasibility/implementation出现以下任一条件必须停止：

- 需要修改0.1/0.2 bytes、digest domain、fixture或historical Bundle；
- 需要用empty/synthetic/placeholder digest填补absence；
- 只能由Schema、manifest、Provider、publisher或caller决定root state；
- 需要让unknown/unsafe prefix取得normal Ledger authority；
- 需要先选择persistence或public Evidence才能完成private root projection；
- 需要同时升级manifest topology才能验证child本身；
- 需要重开Fact/Relation/Slice terminal semantics而不是只消费它们；
- 需要让root chain自己决定Coverage denominator、stage status或overall join。

若现有private history不能形成total、deterministic、copy-owned root projection，必须返回被击穿的最小上游边界；不能用更大的
ObservationLedger、通用receipt或public carrier掩盖缺口。

## 10. normative falsifier obligations

以下world是后继Schema feasibility / implementation必须直接攻击的合同反例；本轮mechanical audit只验证其可区分性，不冒充
runtime已经实现：

| ID | 单变量world | 必须拒绝的结论 |
| --- | --- | --- |
| `RBCC-000` | present Fact artifact与qualified-absent Fact branch只差root state | nullable/omitted digest足以表达二者 |
| `RBCC-001` | zero denominator与all rejected均无三个sets | 相同null/empty chain拥有相同identity |
| `RBCC-002` | projection blocked与required Provider non-success均无FactSet | downstream可丢失stage-owned cause |
| `RBCC-003` | Fact absent但移植foreign RelationSet/ReviewSliceSet digests | shape-valid successor证明chain合法 |
| `RBCC-004` | admitted branch-empty Slice与qualified-absent Slice均为0 members | empty content等于absence |
| `RBCC-005` | predecessor qualified unknown、downstream synthetic empty | downstream可把unknown提升成absence/complete |
| `RBCC-006` | exact binding bytes/digest相同，attempt/claim不同 | semantic identity继承live composition authority |
| `RBCC-007` | unsafe/interrupted attempt保留完整-looking prefix | partial history可生成qualified unknown Ledger |
| `RBCC-008` | 0.2与0.3 stage payload相同 | 可继承旧Ledger digest或按closest version解释 |
| `RBCC-009` | 0.3 negative child bytes合法但manifest 0.1 topology不合格 | child conformance自动升级manifest |
| `RBCC-010` | binding顺序或predecessor digest被交换 | 三个局部binding通过即可证明ordered chain |
| `RBCC-011` | root chain完整但Coverage transition/status错误 | root conformance拥有Coverage qualification authority |

positive vectors至少覆盖normal三段present、三类present empty/partial branch，以及四个safe-negative Fact branches；negative
vectors必须逐项覆盖state/artifact矛盾、digest mutation、foreign predecessor、unknown promotion、version fallback与manifest错层。

## 11. authority ceiling与后继顺序

本合同闭合只允许声明：

> CoverageLedger successor的root chain语义、identity、total classification、conformance与manifest compatibility stop已经冻结。

它不证明或授权：

```text
schemas/review-coverage-ledger-0.3.schema.json exists
0.3 conformance/runtime exists
ReviewSliceSet / Coverage composition is feasible or implemented
manifest successor exists
negative-world public Bundle exists
persistence is selected
Evidence / publisher / Workbench / Core is updated
```

合同冻结后仍须返回CONTROL LOOP。只有fresh evidence仍支持，才可分别审查：child Schema/conformance的有限可行性、manifest
negative-world topology，以及composition runtime。三者不得合成一个“大实现授权”。

## 12. 本候选自己的资格门

tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。doc259–280、runtime、tests、workflows、Schema、
manifest、fixtures、Profile、Policy、vectors、corpus与架构资产保持base bytes。

final bytes必须完成Markdown/Schema baseline regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态marker、
四文件scope、敏感字面量、上游frozen-byte continuity、`git diff --check`与read-only hygiene。read-only mechanical audit至少验证：

1. current 0.1 root仍要求三个digest，逐项省略被拒绝；
2. present、qualified absent、present branch-empty与qualified unknown canonical projections互不相同；
3. 四个safe-negative Fact worlds产生不同binding/chain identities；
4. absent→foreign present、unknown→synthetic absent、branch-empty→absent均被拒绝；
5. normal 0.2/0.3 identity与digest domain不互换；
6. manifest 0.1对normal present topology与negative topology的兼容矩阵保持；
7. CPython 3.10/3.13、normal/`-O`四格canonical report逐字节一致。

首轮audit脚本把规范检查写成Python `assert`，导致`-O`两格移除这些检查；即使四格都输出byte-identical
PASS-shaped report，也不具有资格。该身份按`OPTIMIZATION_ASSERTION_PROOF_GAP`完整保留，未产生产品或合同结论。
fresh attempt 2改用显式`require()`，但仍把terminal history构造成不透明label的digest，不能证明doc280要求的
denominator / U / E / blocker / responsibility partition确实进入identity；它按
`TERMINAL_HISTORY_PROJECTION_PROOF_GAP`保留，同样没有资格效果。fresh attempt 3进一步使用显式、state-specific canonical
terminal-history projection并验证适用成员变异会改变digest；CPython 3.10.6/3.13.13、normal/`-O`四格全部PASS，canonical
report逐字节一致：

```text
ea4674a6bab1b6b43315fb3ab680d6aa28da18cd5f3913be9ac15eaab39dd269
```

随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate history
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN
    -> return CONTROL LOOP
```

在这条链闭合前，本文只是candidate。它不授权Schema implementation、composition feasibility/runtime、manifest successor、
persistence、public Review产品、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。
