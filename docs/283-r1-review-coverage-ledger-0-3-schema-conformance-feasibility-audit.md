# R1 CoverageLedger 0.3 child Schema / conformance 可行性审计

日期：2026-10-18

> 状态：`R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 坐标：`main@6709f5890c6b2cf9bf5acd84d8531af49ac00c76`，tree
> `af3e81d12bb69d54b13ab67d0a5ffd243e727d26`。
>
> 上游：[Schema correction 合同](273-r1-review-slice-set-coverage-schema-correction-contract.md)、
> [root binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)及其
> [独立冻结发布](282-r1-review-slice-set-coverage-root-binding-correction-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本轮只审有限 child Schema / conformance implementation
> 是否可行；不创建 Schema、validator、fixture、vector、runtime 或 manifest successor，不启动 composition，
> 不选择 persistence，也不形成 public Review 产品。

## 1. CONTROL LOOP 与 exact source state

PR #324 final head `4874cd21f223ece7f5c17a6369cc512012d23d68` 已合入当前主线。original Public CI
`39047963366`、exact-main Public CI `39091698699` 与 Browser Smoke `39091698666` 均为 attempt 1
SUCCESS，分别为 11/11、11/11 与 1/1。fresh README/doc281/doc282/milestones 取得 4/4 qualifying
PASS；doc282 首个 formal observation 的匿名 API quota ERROR 继续保留。independent reconciliation 与
238-artifact closeout 分别为：

```text
884d3a4765ca1111e40fa8305159a710c5ba15876a15c5c8a328d5611d4b0ebd
4307edd2c672581a52ccf696528ec97160aabadbbe03022bc30d27d61b92fcb3
```

因此以下事实已经生效：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

fresh CONTROL LOOP 重新核对远端、open PR、Schema、manifest、fixtures 与 current private history。远端仍为该
exact main；open PR 只有旧 Dependabot。没有新的 semantic source state，也没有更早反例要求重开 Fact、Relation、
ReviewSlice 或 root-binding 合同。

## 2. 当前实现事实

仓库当前只有：

```text
schemas/review-coverage-ledger-0.1.schema.json
```

以下文件均不存在：

```text
schemas/review-coverage-ledger-0.2.schema.json
schemas/review-coverage-ledger-0.3.schema.json
```

因此 0.2 / 0.3 仍然只是 frozen semantic identity，不能被描述成已实现。当前 0.1 root 继续要求
`fact_set_digest / relation_set_digest / slice_set_digest`；common 0.1 又把 `SchemaVersion` 固定为 `0.1`。
后继 child 必须在自身 Schema 中声明 `const: "0.3"`，只能复用未改变的基础类型，不能修改 common 0.1。

同时，private history 已保留后继 conformance 所需的上游材料：

| stage | current private source | 可提供的冻结事实 |
| --- | --- | --- |
| Fact | `OwnedProductFactClosure` → fixed handoff source | exact branch、input identity、Parse partition、U/E/blocker projection、Provider history、FactSet 或 qualified absence |
| Relation | `OwnedRelationSetAdmissionState` | observation domain、qualification、Provider runs、request provenance、RelationSet、conflict 与 admission witness |
| ReviewSlice | normal closure、empty-domain closure、blocked-input receipt | obligation domain、outcomes、frontier、normal/partial/empty/blocked branch 与 closure identity |

这些对象证明“原料存在”，不证明 root projection 或 composition 已实现。semantic summary 可以复制，live claim、attempt 与
continuation authority不能由相同 bytes 或 digest 继承。

## 3. 有限 child boundary

0.3 可以保持为一个有限 child successor，不需要 common 或 manifest 同步升级：

1. 继承 doc273 冻结的 0.2 seven-stage、blocker、reason、canonical order 与 digest 语义；
2. 把旧的三个必填 set digest root 替换为固定三成员 ordered root chain；
3. 每个 binding 只允许 `ARTIFACT_PRESENT / QUALIFIED_ABSENT / QUALIFIED_UNKNOWN` 三种封闭 shape；
4. `schema_version`、digest domain、root function 与 conformance identity由 child 自己精确声明；
5. JSON Schema只证明局部 closed shape；versioned conformance另行复算 terminal-history、binding、predecessor、chain 与
   Ledger digest，并消费 same-attempt application history；
6. unknown child version、closest-version fallback、placeholder digest 与 caller-selected predecessor全部 fail closed。

本轮 audit-only Schema 是 **root fragment**，不是产品 Schema。它故意不重复实现 doc273 的完整 seven-stage child，
也不进入仓库。它只验证新增 root fragment 与既有 0.2 semantic surface没有结构冲突。完整 0.3 child implementation仍为
`NOT_STARTED`。

## 4. mechanical audit

read-only audit 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格运行。四份 canonical report 逐字节一致：

```text
06be5d0ac56ff70762bfe6680e1cc137abc288123fe53b8b6a7b68d32c9594b0
```

八个 positive worlds均形成不同 root-chain identity：

| world | root chain |
| --- | --- |
| normal | present → present → present |
| zero Parse denominator | absent → absent → absent |
| all Parse rejected | absent → absent → absent；history 与 zero-denominator 不同 |
| Fact projection blocked | absent → absent → absent；保留 U/E/blocker |
| required Fact Provider non-success | absent → absent → absent；保留 Provider failure history |
| admitted Relation conflict + `CLOSED_EMPTY` Slice | present → present → present |
| Slice partial/frontier | present → present → present；保留 partial history |
| qualified upstream insufficiency | present → unknown → unknown |

audit 直接拒绝八类 mutation：present 改写为 absent、foreign Relation transplant、branch-empty 改写为 absence、
unknown promotion、binding 交换、terminal-history mutation、closest-version fallback 与 unsafe/interrupted prefix。四个 safe-negative Fact worlds虽有
相同 root state sequence，terminal-history 与 chain identity仍互不相同。

`RBCC-000..011`均被显式归层：001/002由identity separation反证，000/003/004/005/007/008/010由shape或
conformance拒绝，006由object-bound one-shot live authority ceiling保证，009保持manifest compatibility stop，011保持
root fragment不拥有Coverage status authority。

audit 还重新核对 immutable bytes：

```text
CoverageLedger 0.1 Schema = e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545
common 0.1 Schema         = e36f0d4ba494645bc991736b780c2c5354be13789466ab82d72b4963c674da4a
manifest 0.1 Schema       = 69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
```

本报告证明 root fragment有有限表达与机械核验路径；它不证明 product Schema、conformance validator、composition runtime
或 public Bundle 已存在。

## 5. Schema、conformance 与 composition 的责任边界

| 层 | 本轮证明可承担 | 仍不能承担 |
| --- | --- | --- |
| 0.3 Schema | self-description、固定 binding 顺序、state-local required/forbidden members、closed properties | root truth、terminal-history completeness、same-attempt authority |
| 0.3 conformance | 对 exact candidate 与 application-owned history做单向机械核验 | 创建/修复 candidate、选择 branch、取得 composition claim |
| composition runtime | 本轮未审 | 枚举 root、组装 seven-stage Ledger、continuation |
| manifest | 绑定合法 child bytes/digest | child dispatch、absence truth、negative-world topology |

因此：

```text
finite child Schema/conformance feasibility
    != Schema implementation authorization
    != composition feasibility
    != manifest successor selection
```

## 6. manifest compatibility stop 仍然独立

现有 manifest 0.1 在 FactSet、RelationSet、ReviewSliceSet 全部 present 时，可以用 COMPLETE topology绑定一个已知且
独立 conformance 的 0.3 child。任一 set qualified absent/unknown 时，COMPLETE缺失 required set，DIAGNOSTIC又禁止
CoverageLedger。

这个 topology gap没有阻塞 private child feasibility，也没有被 child Schema解决。negative-world public publication必须在
独立 CONTROL LOOP 中审查；本轮不选择 successor version、role、path、cardinality 或 migration。

## 7. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| root-binding 合同是否已经 frozen | **是** |
| current private histories是否保留所需语义材料 | **是** |
| 0.3 root fragment是否可作为有限 closed child shape表达 | **是** |
| versioned conformance是否可以与 Schema责任分离 | **是** |
| 是否需要修改0.1/0.2、common或manifest才能验证 child | **否** |
| manifest negative-world topology是否已解决 | **否，独立 seam** |
| composition runtime是否已经证明可行 | **否** |
| 0.3 Schema/conformance implementation是否已授权 | **否** |
| persistence是否成为当前 blocker | **否** |

本轮没有发现需要重开 frozen contract 的反例。若本候选完成自己的资格链，它最多成为
`FEASIBILITY_AUDITED` history；随后仍须返回 CONTROL LOOP，单独判断 docs-only implementation authorization 是否是
下一最小合法 seam。

## 8. 后继 implementation stop conditions

后继若出现以下任一条件，必须停下并只重开被击穿边界：

- 需要修改 0.1/0.2/common/manifest 历史 bytes 或 digest identity；
- 需要让 Schema、manifest、Provider、publisher、caller 或 digest holder生成 root truth；
- 需要 synthetic/placeholder digest表达 absence；
- 无法从 stage-owned terminal history形成 total projection；
- 需要把 same semantic summary 当作 live attempt/claim/continuation authority；
- 需要先实现 composition assembler、manifest successor、persistence或public Evidence才能验证 child；
- 需要让 root conformance决定 seven-stage denominator、status或overall join；
- 需要把 unknown/unsafe prefix提升为 absent、present或normal Ledger。

## 9. 本候选资格门与停止线

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc259–282、runtime、tests、
workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产必须保持 base bytes。

final bytes至少完成：四文件 scope、UTF-8 without BOM、LF/final LF、links/fences/headings、状态 marker、上游 frozen-byte
continuity、`git diff --check`、read-only hygiene，以及声明的 Markdown/Schema baseline regression。机械 audit与四格报告必须
在提交前复核；测试只作 witness。

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> FEASIBILITY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合前只能写：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文不授权 implementation publication、Schema/conformance/runtime/tests/fixtures/vectors、composition feasibility/runtime、
manifest successor、public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、
R2/R3、CLAIM_FIDELITY、tag 或 Release。
