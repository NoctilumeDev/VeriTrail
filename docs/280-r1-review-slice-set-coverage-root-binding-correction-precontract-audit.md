# R1 ReviewSliceSet / Coverage root binding correction 前合同审计

日期：2026-10-17

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_PRECONTRACT_AUDIT_CANDIDATE`。
>
> 基线：`main@acf248daee9bca362a84df27fb9f7d8c2385b0b9`；tree
> `3d596280422f10ee612ce3b7dc0b6c36f4ba12f9`。
>
> 上游：[composition qualification 最小合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [Schema correction 最小合同](273-r1-review-slice-set-coverage-schema-correction-contract.md)与
> [root binding 当前状态审计](279-r1-review-slice-set-coverage-schema-root-binding-current-state-audit.md)。
>
> 影响：`L3_SYSTEM_AUDIT + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只界定 CoverageLedger root 对
> present artifact 与 qualified absence 的最小语义问题，以及该问题与 Manifest topology 的边界；不选择字段、对象、
> Schema 文件、版本号、digest domain、manifest successor 或 migration，不修改合同、Schema、runtime、tests、fixtures、
> vectors、Profile、Policy 或 corpus，不授权 correction contract、Schema implementation、composition feasibility/runtime、
> public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence、Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 qualified source state

文档 279 已由 PR #321 final head `406923bdfa7e89ff3caaea9d66e402a9075bae03` 合入本基线。original Public CI
`39022612920`、exact-main Public CI `39024355114` 与 Browser Smoke `39024355171` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1；fresh README/doc279/milestones 各有且仅有一份 qualifying PASS。independent reconciliation 与
173-artifact closeout 分别为：

```text
9c78cbe29b76a6780d670f1ea51df825603eedec754f93b6870aeb476a202e3c
c0e886b08e4dcf990ade8f7890e9e6c07a61683e2c09e9e51288f9bac4aec6d4
```

gate seal attempt 1 错把 candidate CI 绑定到 merge SHA，按 `GATE_SEAL_IDENTITY_SETUP_ERROR` 保留；attempt 2 只修正
证明设施身份。它没有改写产品观察或冻结字节。文档 273 与 279 的 full-file SHA-256 分别保持：

```text
0fe8f2714333c5802ffaa83b867a5f687d80abbfe78b5351dc7a39d11d41f8ec
28f9a135bf428a45846c35786643877abbd3cf34ca74ef2a07467c96de5d6805
```

remote `main`、本工作树基线与该 exact main 一致；open PR 只有既有 Dependabot 更新，没有新的 semantic PR。本文因此消费：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

当前最小合法问题仍是 root-binding correction 的前合同边界，不是直接修 Schema，也不是开始 composition runtime。

## 2. finding 从单字段扩大为三段 root chain

文档 279 已证明 projection-blocked world 没有 FactSet，而 frozen CoverageLedger root 要求 `fact_set_digest`。重新读取
现有 Schema 与 frozen dependency 后，问题不能只写成：

```text
fact_set_digest: string -> string | null
```

CoverageLedger 0.1 及文档 273 冻结的 0.2 root 同时要求：

```text
fact_set_digest
relation_set_digest
slice_set_digest
```

public dependency 又保持：

```text
FactSet -> RelationSet -> ReviewSliceSet -> CoverageLedger
```

当 FactSet 因 qualified negative branch 不存在时，application 没有 authority 启动 normal Relation derivation；因此也没有
normal RelationSet。没有 qualified RelationSet 时，normal Slice derivation 与 ReviewSliceSet admission 同样不能发生。
只放宽第一项、再保留另一个 attempt 或 synthetic empty 的 RelationSet / ReviewSliceSet digest，仍然是 cross-world transplant。

所以当前 finding 是：

```text
THREE_STAGE_ROOT_BINDING_GAP

FactSet presence / qualified absence
        -> RelationSet presence / qualified absence
        -> ReviewSliceSet presence / qualified absence
        -> CoverageLedger root
```

这里的 `qualified absence` 是上游 branch 与履责历史的精确结论，不是空集合、缺字段或 unknown 的别名。

## 3. root decision 的 authority owner

root 判别只能由 application-owned composition 取得。它必须消费同一 attempt 的 live handoff、冻结的 transition rules、
Relation admission、Slice closure / admission 与 Coverage composition history。各层只拥有自己的职责：

```text
upstream stage
    owns exact semantic artifact or exact qualified absence history

application-owned composition
    owns the ordered present/absent root decision and cross-stage reconciliation

Schema
    owns local carrier shape only

manifest
    binds selected artifact bytes only

Provider / publisher / digest holder
    owns no root-decision authority
```

normal present branch 至少需要 exact semantic digest 与对应 admission/closure identity。qualified absence 至少必须绑定：

- exact upstream branch；
- denominator / U / E / blocker 或 responsibility partition；
- producing function 与 frozen transition identity；
- same-attempt claim、closure、admission 与 predecessor identity；
- absence 的 terminal class，而不是只有 `null` 或 reason string。

这些是合同问题面，不是本文选择的 public carrier。private attempt identity 是否进入 public Evidence 仍保持后继问题。

## 4. 五个世界不能共享一种 empty identity

fresh read-only audit 从同一 exact source 构造五个 world：

| world | Fact branch | U / E / blocker | FactSet | 最低 root 语义 |
| --- | --- | --- | --- | --- |
| normal fulfilled | `NORMAL_FULFILLED` | 14 / 14 / 0 | present | exact present binding |
| zero Parse denominator | `ZERO_PARSE_DENOMINATOR` | 0 / 0 / 0 | absent | qualified zero-denominator absence |
| all Parse rejected | `ALL_PARSE_REJECTED` | 0 / 0 / 0 | absent | qualified rejected-history absence |
| projection blocked | `PROJECTION_BLOCKED` | 3 / 2 / 1 | absent | qualified semantic-blocker absence |
| required Provider non-success | `REQUIRED_PROVIDER_NON_SUCCESS` | 14 / 14 / 0 | absent | qualified execution non-success absence |

后四个 world 都没有 FactSet，但它们的 denominator、terminal history 与 downstream meaning 不同。共同写成 empty digest、共同
`null` 或共同 `ABSENT` 只能取得局部 shape，不能取得 total semantic qualification。

unsafe / interrupted / foreign-attempt world 更弱：它没有 normal handoff claim，不能仅凭 retained diagnostic history取得可发布
Coverage root。`qualified absence` 不能成为把 unsafe world升格为 normal Ledger 的后门。

## 5. downstream absence 与 branch-bound empty set

文档 267 允许 admitted conflict / blocked Slice branch 在完整 typed history 下形成 branch-bound empty ReviewSliceSet semantic
content；它同时明确该 empty content 不得等同 `CLOSED_EMPTY`。这条规则不能反向应用到 Fact-stage blocker：

```text
Fact projection blocked
    -> Relation universe cannot be completely enumerated
    -> no normal RelationSet admission
    -> no normal ReviewSliceSet admission
    -> downstream stages remain UNKNOWN
```

因此 root correction 至少要区分：

1. artifact present and admitted；
2. artifact qualified absent because a typed predecessor branch forbids construction；
3. branch-bound empty semantic artifact that was independently admitted；
4. unknown / unqualified / interrupted history。

第 2 项没有 artifact digest；第 3 项有自己的 semantic content identity与 admission authority。二者不能共用一个“空”值。

## 6. CoverageLedger 0.2 的 version stop

文档 273 冻结 0.2 child identity时明确“保留 Coverage 0.1 的 root binding”。把 required digest 改成 presence/absence union，
或用新的 root-binding object取代三个 digest，都会改变已冻结的 0.2 root semantics 与 canonical digest input。

所以当前可以确定：

```text
CoverageLedger 0.2
    remains valid for the exact semantics it froze

CoverageLedger 0.2
    cannot be silently redefined to solve qualified absence

negative-world root binding
    requires an explicitly versioned successor boundary
```

本文不选择 `0.3`、sidecar、tagged union、三组独立 binding 或单一 chain binding。任何 proposal 都必须先证明：正常 0.2
baseline 不被改写、absence 不伪造 artifact、三段依赖保持单向、canonical digest与consumer dispatch有独立identity。

## 7. Manifest 是独立但耦合的 topology seam

`review-derivation-manifest-0.1` 的 `COMPLETE` 精确要求八个 artifact entries，包括 FactSet、RelationSet、ReviewSliceSet 与
CoverageLedger；`DIAGNOSTIC` 精确只允许前四个输入 artifact，不允许 CoverageLedger。

因此一个持有 qualified negative history 与 CoverageLedger、但没有三个 normal upstream set 的 world：

```text
COMPLETE
    -> rejected because three required set entries are absent

DIAGNOSTIC
    -> rejected because CoverageLedger is not allowed
```

这形成第二个 finding：

```text
MANIFEST_NEGATIVE_WORLD_TOPOLOGY_GAP
```

它不授权现在升级 manifest。root correction contract 必须把 child root semantics 与 manifest transport topology分开：先定义
什么事实有资格存在，再决定何种 versioned manifest能绑定这些 bytes。若未来选择不发布 negative-world CoverageLedger，也必须
显式说明它如何满足文档 267 已冻结的 Coverage negative-world 核账义务，不能靠省略 artifact让问题消失。

## 8. mechanical audit 与首败保留

仓库外 read-only harness 机械检查：

1. Coverage 0.1 root 的三个 set digest均为 required；逐项省略均被 Schema拒绝；
2. manifest COMPLETE 只带四个 input与 CoverageLedger 时被拒绝；
3. manifest DIAGNOSTIC 增加 CoverageLedger 时被拒绝；
4. normal与四个 safe-negative handoff保持五种不同 branch/history；
5. exact Schema、manifest与 doc273 bytes保持 frozen。

attempt 1 把所有 qualification branch都假定为显式携带 `blockers`，在 normal world触发 `KeyError('blockers')`。它被保留为
`AUDIT_HARNESS_SETUP_ERROR`，没有产品结论。fresh attempt 2 改为只在字段适用时读取，并在 CPython 3.10.6 / 3.13.13、
normal / `-O` 四格全部 PASS；canonical report逐字节一致：

```text
6bfbc73f8ff4cf33fb54570b585789df0dab74c75a012c113ffc66dd010d4f48
```

测试只作 witness。它没有生成新 root carrier、版本号或 manifest proposal。

## 9. 前合同裁决

| 问题 | 裁决 |
| --- | --- |
| root gap 是否只涉及 `fact_set_digest` | **否，Fact / Relation / ReviewSlice 三段都受影响** |
| qualified absence 是否等于 empty artifact | **否** |
| root decision owner 是否是 Schema / manifest / Provider | **否，属于 application-owned composition** |
| branch-bound empty ReviewSliceSet 是否可替代 upstream absence | **否** |
| frozen 0.2 是否可静默改变 root semantics | **否** |
| manifest 0.1 是否能携带 negative-world Ledger | **不能** |
| persistence 是否是当前 blocker | **否** |
| correction contract 是否已起草或授权 | **否** |
| Schema implementation / composition runtime 是否可开始 | **否** |

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_PRECONTRACT_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

当前有资格提出的下一问题是一个 docs-only correction contract：怎样以 versioned、total、same-attempt 的 root chain绑定
present artifact、qualified absence、branch-bound empty artifact与 unknown，同时保持 manifest topology为独立兼容性边界。

## 10. 后继最小合同面

如果本文完成自己的资格链，下一轮最多有资格起草：

1. Fact / Relation / ReviewSlice 三段 root binding 的 owner与有序依赖；
2. present、qualified absent、admitted branch-empty、unknown 四类语义及其适用条件；
3. negative Fact branch到 Relation / Slice absence 的 versioned transition proof；
4. normal 0.2 baseline、zero denominator、all rejected、projection blocked、required Provider non-success、Relation conflict、
   Slice frontier与unsafe history的total classification；
5. same-attempt claim、closure、admission与canonical digest construction；
6. CoverageLedger successor的version stop、known-version dispatch与0.2 immutability；
7. Manifest topology作为独立 successor / compatibility stop，而不是由child字段偷偷改写；
8. 哪些选择会重开 frozen Fact / Relation / Slice contract，因而必须禁止或单独 version；
9. Schema implementation、composition feasibility/runtime、persistence与public publication继续停止的边界。

下一合同仍不得选择 persistence、实现 Schema/runtime、发布 public artifact 或修改 frozen 0.1/0.2 bytes。若不能在不伪造
artifact identity、不恢复 foreign live authority的条件下形成 total root chain，必须停回问题审计。

## 11. 候选资格链与停止线

本文候选的 tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc259–279、runtime、
tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产保持 base bytes。

final bytes必须完成 Markdown/Schema baseline regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态 marker、
四文件scope、敏感字面量、上游 frozen-byte continuity、`git diff --check`与read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> precontract audit becomes qualified history
    -> return CONTROL LOOP
```

在这条链闭合前，本文只是 candidate。它不授权 correction contract、Schema implementation、composition feasibility/runtime、
public `ReviewSliceSet` / `CoverageLedger`、manifest successor、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、
R2/R3、CLAIM_FIDELITY、tag或Release。
