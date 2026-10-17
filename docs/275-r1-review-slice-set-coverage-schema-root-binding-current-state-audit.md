# R1 ReviewSliceSet / Coverage Schema root binding 当前状态审计

日期：2026-10-17

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_CANDIDATE`。
>
> 基线：`main@9aa94dcac8c1bc5bb4d4852a5136d3d7bf3fe583`；tree
> `65475b77a8235eb591e4857032e3318da8ab56cf`。
>
> 上游：[Schema correction 最小合同](273-r1-review-slice-set-coverage-schema-correction-contract.md)与
> [独立冻结发布](274-r1-review-slice-set-coverage-schema-correction-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_AUDIT + L2_CONTRACT_AUDIT + L0_DOCUMENTATION`。本文只判断冻结的 CoverageLedger 0.2
> root binding 是否已足以支持有限 Schema implementation；不修改合同、Schema、runtime、tests、fixtures、vectors、
> manifest、Profile、Policy 或 corpus，不选择 persistence，不启动 composition feasibility / implementation、public
> `ReviewSliceSet` / `CoverageLedger`、Evidence、Bundle、publisher、CLI、Workbench、Core、R2 或 R3。

## 1. CONTROL LOOP 与 exact coordinate

文档 274 的最后门已在本基线闭合。PR #316 final head
`a5ce50238aac1ce411938ceed3bd69e93fc3648c` 合入为本 exact main。原始 Public CI `38984368378`、
exact-main Public CI `38999769024` 与 Browser Smoke `38999769037` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1；Review Attention 四格各为 `513 reported / 510 passed / 3 skipped`。

fresh README/doc274/milestones 各有一份 qualifying PASS。independent reconciliation 与 122-artifact closeout 分别为：

```text
853031c9650a5df1999710eaa0064ffdfcfb3df68539410b8b04a27826f81272
ebb99cd2e8c8b824162f2e0c21fd4fb99da8603444607ea315406e35242b6a4a
```

首次 detached worktree creation 因本机尚未取得 exact object，以 `WORKTREE_OBJECT_NOT_FETCHED_SETUP_ERROR` 保留；后继 fetch
没有把该 setup identity 改写成产品失败。文档 273 的 qualified full-file SHA-256 继续为：

```text
0fe8f2714333c5802ffaa83b867a5f687d80abbfe78b5351dc7a39d11d41f8ec
```

因此以下是本文的 frozen upstream：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

remote `main`、本 worktree HEAD 与基线一致；open PR 只有既有 Dependabot 更新。主检出保留用户 `audit.json`，本文不触碰。

## 2. CONTROL LOOP 发现更早的 root-binding seam

文档 273 已冻结 CoverageLedger 0.2 的 child identity、`blocked` carrier、versioned conformance、dispatch 与 0.1
immutability。它同时要求 successor 保留 Coverage 0.1 root bindings，其中包括必填：

```text
fact_set_digest
relation_set_digest
slice_set_digest
```

但 frozen Fact → Coverage handoff 的 projection-blocked world 明确保留：

```text
branch      = PROJECTION_BLOCKED
U / E / B   = 3 / 2 / 1
fact_set    = null
```

这不是缺少 ordinary Fact output 的偶发现象。Fact fulfillment 已冻结：当完整 `U` 中存在不可表示 slot 时，不产生 ordinary
claim、FactSet 或 continuation；handoff 只交出完整 U/E/blocker、Provider/Parse history、exact absence 与 live authority。

因此当前存在一个比写 `review-coverage-ledger-0.2.schema.json` 更早的问题：

```text
qualified upstream says FactSet is absent
        +
CoverageLedger root requires fact_set_digest
        =
no authorized root value
```

`blocked` 数组解决的是 terminal disposition carrier；它没有 authority 发明一个不存在的 FactSet identity。

## 3. 三个不可混淆的世界

| world | local shape | authority result |
| --- | --- | --- |
| 省略 `fact_set_digest` | successor root 不完整 | JSON Schema 必须拒绝 |
| 填任意或占位 digest | closed shape 可以通过 | 没有 FactSet / admission source，semantic conformance 必须拒绝 |
| 由 downstream 自建 empty FactSet | 可以获得某个 digest | 改写 frozen Fact absence，当前无创建或 admission authority |

同理，manifest 0.1 的 COMPLETE topology 同时要求 `FACT_SET` 与 `COVERAGE_LEDGER` entry。manifest 能绑定 bytes/digest，
但不能为 projection-blocked branch 生成 FactSet、选择 synthetic identity 或证明 empty content 属于哪个 terminal history。

当前不能用下列替代物填补 root：

- blocker `subject_key_digest`：它标识 U slot，不是 FactSet；
- `E` 或 actual output 的 digest：它会缩小 authoritative U；
- arbitrary empty FactSet digest：它会把 projection-blocked 伪装成 zero/fulfilled empty；
- foreign normal attempt 的 FactSet：content equality 不继承 same-attempt authority；
- manifest `semantic_digest`：它绑定 child bytes，不拥有 child root semantics。

## 4. 对 frozen 历史的影响

本 finding 不推翻以下事实：

```text
Fact projection / fulfillment contract and private implementation
    remain FROZEN

Fact -> Coverage handoff private implementation
    remains FROZEN

Coverage vocabulary and blocker tuple
    remain FROZEN

CoverageLedger 0.2 Schema correction contract
    remains historical frozen authority
```

它切断的是后继推导：

```text
Schema correction contract FROZEN
    -> finite 0.2 Schema implementation is already feasible
```

文档 273 对 blocker child shape 的结论仍成立；但其“保留 0.1 root binding”与 positive projection-blocked world 之间缺少
FactSet-absence binding semantics。冻结合同不是静默修改许可证。后继只能显式重开这一最小 root-binding boundary，或给出一个
不改变 frozen Fact absence 且可机械验证的既有 authority source。

## 5. mechanical audit

仓库外 read-only harness 直接构造 frozen projection-blocked handoff，并从 exact Schema/manifest/fixture 构造 audit-only 0.2
child。它验证：

1. live handoff 是 `PROJECTION_BLOCKED`，U/E/blocker 为 `3/2/1`，`fact_set` 为 null；
2. Coverage 0.1 root 的 `fact_set_digest` 必填约束被 0.2 合同继承；
3. manifest COMPLETE topology同时要求 FactSet 与 CoverageLedger；
4. 不带 `fact_set_digest` 的 audit-only child 被 Schema 拒绝；
5. 填入未获 authority 的 64 位占位 digest 后 shape 可以通过，证明 Schema validity 不能修复 root authority；
6. Coverage/common/manifest 0.1 bytes保持 frozen SHA-256。

attempt 1 使用了与 frozen 文本不完全相同的中文锚点，以
`AUDIT_HARNESS_TEXT_ANCHOR_MISMATCH_SETUP_ERROR` 保留。fresh attempt 2 只把调用方检查改为稳定子串组合，不修改产品、
Schema、world 或 oracle。CPython 3.10.6 / 3.13.13、normal / `-O` 四格 canonical report 逐字节一致：

```text
f7f7affd123f9a2bce9b33ea3c87effa6d2a9c0cbb711159503428944688e478
```

报告中的核心裁决为：

```text
finding              = FACT_ABSENCE_ROOT_BINDING_GAP
qualification_effect = SCHEMA_IMPLEMENTATION_FEASIBILITY_NOT_ESTABLISHED
```

声明的 Markdown / frozen Schema regression 首次直接调用没有绑定 repository `src`，在 `tests.test_markdown` import时留下
`LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`；37项中36项通过、1个test module import ERROR。fresh attempt只修调用方
`PYTHONPATH`，未改产品、测试、文档语义或oracle；CPython 3.10/3.13、normal/`-O`四格各为`40 reported / 40 passed`。

测试只作 witness。它不把 placeholder 升格成产品 proposal，也不把 absence of FactSet解释成 Fact runtime defect。

## 6. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| Schema correction 合同是否 frozen | **是** |
| `blocked` carrier 是否可以有限表达 exact tuple | **是** |
| projection-blocked handoff 是否拥有 FactSet | **否** |
| frozen 0.2 root 是否要求 `fact_set_digest` | **是** |
| 当前是否有 authority 生成该 branch 的 FactSet digest | **没有证明** |
| arbitrary/empty digest 是否可以补位 | **否** |
| finite Schema implementation feasibility 是否成立 | **否，当前未建立** |
| 是否应直接修改 Schema/tests | **否** |
| persistence 是否成为 blocker | **否** |

所以当前最小合法问题不是 Schema implementation，也不是 composition assembler。它是一个 docs-only root-binding correction
问题：projection-blocked / FactSet-absent branch 怎样被 CoverageLedger root 精确绑定，同时不把 absence 改写成 empty FactSet、
不让 Schema/manifest/downstream consumer生成上游事实。

## 7. 后继最小问题面

如果本文完成自己的资格链，下一轮最多有资格审查：

1. Coverage root 对 `present FactSet` 与 `qualified absence` 的判别责任由谁拥有；
2. exact absence 需要绑定哪些 branch、U/E/blocker、same-attempt 与 admission identity；
3. root carrier 是否必须 versioned correction，以及 0.2 identity是否仍可保持；
4. RelationSet / ReviewSliceSet downstream absence或 branch-bound empty content怎样保持单向依赖；
5. manifest COMPLETE/DIAGNOSTIC topology是否仍足够，何种反例才要求 manifest successor；
6. normal 0.2 baseline、projection-blocked、required Provider failure与 zero worlds如何保持不同；
7. 哪些选择会重开 frozen Fact contract，因而必须禁止或单独 version；
8. Schema implementation、composition feasibility与 persistence继续停止的边界。

本文不选择 optional/null/union 字段形状，不定义 synthetic FactSet，不升级 manifest，也不起草 correction contract。

## 8. 候选资格链与停止线

本文候选的 tracked scope只能是 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc267–274、runtime、
tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产保持 base bytes。

final bytes必须完成 Markdown/Schema baseline regression、links/fences/headings、UTF-8 without BOM、LF/final LF、状态 marker、
四文件scope、敏感字面量、上游 frozen-byte continuity、`git diff --check`与read-only hygiene；随后仍需：

```text
original PR gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / identity / retained-history reconciliation
    -> current-state audit becomes qualified history
    -> return CONTROL LOOP
```

在这条链闭合前，本文只是 candidate。它不修改 frozen contract，也不授权 root-binding correction contract、Schema
implementation、composition feasibility/runtime、public assembler、persistence、Evidence/Bundle/publisher、CLI/Workbench/
Core、R2/R3、CLAIM_FIDELITY、tag或Release。
