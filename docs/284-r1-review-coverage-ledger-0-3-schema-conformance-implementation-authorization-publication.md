# R1 CoverageLedger 0.3 child Schema / conformance 实现授权发布

日期：2026-10-18

> 状态：`R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 基线：`main@dd4cd19d23623516416c8d0a6803c22d15960e36`，tree
> `b0ec9ddaaa889ed4b41b5062f4e05306000a4ad2`。
>
> 上游：[root binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)、
> [独立冻结发布](282-r1-review-slice-set-coverage-root-binding-correction-contract-freeze-publication.md)与
> [0.3 child Schema / conformance 可行性审计](283-r1-review-coverage-ledger-0-3-schema-conformance-feasibility-audit.md)。
>
> 影响：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`；docs-only。
> `SCHEMA_IMPLEMENTATION_ALLOWED` 仅为条件目标，本文最后门全部闭合以前不生效；Schema、validator、tests、fixtures、vectors
> 与 composition runtime 仍未开始。

## 1. CONTROL LOOP 与当前 authority

文档 283 已由 PR #325 final head `734f35a328e706fe843ec6f2f9590c6e2ac90f83` 合入本基线。original Public CI
`39094291800`、exact-main Public CI `39095889099` 与 Browser Smoke `39095889019` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1。fresh README/doc283/milestones 各有且仅有一份 qualifying PASS；independent reconciliation
与 145-artifact closeout 分别为：

```text
afb2bf3dfc5054ee0fb8b00504e4a485125d4e8c3552d7eac318c48fcc9b405d
0e26367f1d3614d56e3ddc130f45d41003205818154a433d30ed16cf543c57d2
```

文档 283 的 full-file SHA-256 为：

```text
6cbcdfd3942d80a5eba8df2024ad1a8034a30e153eb9d53f7c071e7133d88fb7
```

因此以下事实已经成为 qualified history：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

fresh CONTROL LOOP 重新核对本基线、open PR、Schema、manifest、fixtures、tests 与 current private history。没有新的
semantic PR，也没有反例要求重开 Fact、Relation、ReviewSlice、Schema correction 或 root-binding contract。仓库仍只有
CoverageLedger 0.1 Schema；0.2/0.3 文件、0.3 conformance 与 composition runtime 均不存在。

doc283 已经证明 0.3 child 可以在不先物化 0.2、不修改 common/manifest、不选择 persistence、也不启动 composition
assembler 的条件下形成有限实现。当前没有更早 prerequisite；最小合法候选因此是 doc283 §8 定义的 child
Schema / conformance implementation authority。本文不重复 feasibility，也不把另外两条 seam——manifest negative-world
topology 与 composition runtime——并入授权。

## 2. audit witness 不冒充实现证明

doc283 的 audit-only root fragment 只证明新增 root shape 与冻结的 0.2 semantic surface没有结构冲突。八个 positive worlds、
八类 mutation、`RBCC-000..011` 归层与四格 byte-identical report只作 feasibility witness：

```text
06be5d0ac56ff70762bfe6680e1cc137abc288123fe53b8b6a7b68d32c9594b0
```

它们不证明完整 product Schema、versioned conformance、fixture/vector corpus 或 implementation 已存在。首轮 pre-formal
Plan ID 超长、后继 plan-check superseded identities、PowerShell `$error` 自动变量冲突，以及上游 closeout wrapper stdout
post-seal mutation均继续由各自 setup/proof-facility history拥有；后继 PASS 没有覆盖这些身份。

特别是：

```text
finite feasibility
    != implementation authority
    != implementation started
    != implementation qualified
    != composition feasibility
```

## 3. 条件化的最小施工面

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多实现以下边界。各项只落实
doc273 与 doc281 已冻结语义，不新增 Coverage qualification、manifest topology 或 public carrier。

| ID | 最大施工面 |
| --- | --- |
| A | 新建 exact `schemas/review-coverage-ledger-0.3.schema.json`，固定 `$id`、`artifact_kind`、`schema_version=0.3`、canonicalization profile 与 closed root shape |
| B | 直接实现冻结的 0.3 child：保留 0.2 seven-stage、blocker、reason、canonical order 与 conservative join，只替换被击穿的三个 required digest root；不要求先创建 0.2 文件 |
| C | 固定 `FACT_SET -> RELATION_SET -> REVIEW_SLICE_SET` ordered root chain，以及 present / qualified absent / qualified unknown 的 state-local required/forbidden members |
| D | 实现独立、versioned、fail-closed 的 `r1-review-coverage-ledger-conformance/0.3`；Schema 只证明局部 shape，conformance 不生成、修补或重分类 candidate |
| E | 从 application-owned exact terminal history复算 projection、binding、predecessor、chain 与 Ledger digest；semantic bytes/digest不得继承 live claim、attempt、closure或admission authority |
| F | 建立 normal、branch-empty、partial、zero denominator、all rejected、projection blocked、required Provider non-success与qualified unknown等规范 positive fixtures / identity vectors |
| G | 将 `RSCSC-000..016` 与 `RBCC-000..011` 落为直接 falsifiers，覆盖state/artifact矛盾、foreign predecessor、unknown promotion、version fallback、顺序交换与authority错层 |
| H | 为0.3提供精确version dispatch并拒绝unknown/future/未实现child；不得fallback到closest version、冒充已实现0.2，或继承0.1/0.2 digest identity |
| I | 对 CoverageLedger 0.1、common 0.1、manifest 0.1及其历史 fixtures / bundles建立全字节守卫；允许只读验证manifest正常topology，不允许修改manifest或把child conformance升级为transport资格 |
| J | 在CPython 3.10.6/3.13.13、normal/`-O`与既有Schema regressions中证明canonical bytes、direct negatives、旧版本隔离与无optimization-only assertion gap |

文件布局、private helper名和测试数量不是本文的合同。若 pure conformance helper进入 `src`，它也只能验证由调用方显式提供的
exact candidate与application-owned history；不得枚举root、消费live continuation、取得composition claim或输出public
admission。实现可以在tests中保留oracle，但测试仍只是witness，不拥有语义扩张权。

该 authority 允许施工，不预先证明 implementation 正确、完成、merged、exact-main verified 或 FROZEN。

## 4. 必须保持的 authority ceiling

后继实现不得：

- 创建 CoverageLedger assembler、枚举 seven-stage denominator、决定 stage status 或 overall join；
- 修改 CoverageLedger 0.1、common 0.1、manifest 0.1、历史 fixtures、digest domain 或 frozen 0.2/0.3 contracts；
- 让 Schema、validator、manifest、Provider、publisher、caller或digest holder生成root truth；
- 用 empty、placeholder、synthetic或foreign digest表达 qualified absence / unknown；
- 把 branch-empty artifact改写为absence，或把unsafe/interrupted/foreign attempt提升为qualified unknown Ledger；
- 选择manifest successor、negative-world publication topology、persistence Route A/B或public self-contained verification；
- 启动composition feasibility/runtime、public `ReviewSliceSet` / `CoverageLedger`、Evidence、Bundle、publisher、CLI、
  Workbench、Core、R2/R3、CLAIM_FIDELITY、tag或Release。

manifest 0.1只能在FactSet、RelationSet、ReviewSliceSet均present且child独立conformance时绑定正常topology。negative-world
child仍没有合格public transport；这一事实必须保留为独立stop，不得为了让测试通过而改manifest。

## 5. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止，只重开被击穿的最小边界：

1. 无法在不先创建0.2 Schema或修改common/manifest的条件下实现完整0.3 child；
2. 无法从stage-owned history形成total、deterministic、copy-owned projection；
3. 需要先实现composition assembler、manifest successor、persistence或public Evidence才能验证child；
4. 需要从caller输入恢复stage truth、branch、predecessor或terminal-history members；
5. 需要让root conformance决定Coverage denominator、status或overall join；
6. 需要把semantic summary当作live claim、attempt、one-shot ownership或continuation authority；
7. `RSCSC` / `RBCC` direct falsifier暴露合同内部矛盾，而不是局部implementation defect；
8. known negative world只能通过弱化shape、跳过conformance或移动oracle获得PASS。

授权已经生效也不能成为修改oracle、扩大scope或静默reopen frozen contract的理由。

## 6. 本 publication 的资格门

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc259–283、runtime、tests、
workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产必须保持base bytes。

首次窄Schema回归调用没有显式设置`PYTHONPATH=src`，`tests.test_contracts`以`ModuleNotFoundError: veritrail`停止，身份为
`LOCAL_TEST_ENVIRONMENT_SETUP_ERROR`；其余已加载模块当时报告37项通过，不能替代完整门。fresh独立四格使用exact source
path后，CPython 3.10.6/3.13.13、normal/`-O`各44/44 PASS。后继成功没有把首次setup error改写成产品或合同失败。

final bytes至少完成：四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、状态marker、上游frozen-byte
continuity、`git diff --check`、read-only hygiene，以及声明的Markdown/Schema baseline regressions。随后仍需：

```text
final docs-only publication bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc283 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> SCHEMA_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

same patch、tree、content、digest、semantic result或feasibility witness都不能替代上述任一资格身份。本地checkout对齐只作
housekeeping，不新增授权生效门。

## 7. 生效前后与实现自己的门

本文进入仓库、PR CI绿色或target marker可见以前后，事实必须分开：

```text
before publication last gate:
    feasibility audit = AUDITED
    implementation authority = NOT_AUTHORIZED
    implementation = NOT_STARTED

after publication last gate:
    feasibility audit = AUDITED
    schema / conformance implementation = ALLOWED
    implementation = NOT_STARTED
```

本文第6节全部门闭合以前，只允许发布：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

最后门闭合以后也只是 `ALLOWED / NOT_STARTED`。必须重新绑定新的 exact main、检查并行事实并确认 A–J 仍是最小合法
seam，才可创建 implementation branch。后继 implementation需要自己的final bytes、direct falsifiers、四格、original PR、
protected merge、exact-main gates、fresh product observation、independent reconciliation与独立冻结发布；本文不替它证明或冻结。

## 8. stop line

本文不授权Schema/conformance implementation candidate本身，也不授权composition、manifest successor、persistence或public
Review产品。当前授权原则候选冻结为：

> CoverageLedger 0.3 child Schema and versioned conformance may enter implementation only through the bounded A–J surface
> qualified by doc283; that authority does not establish implementation, composition, transport or publication.

中文：**CoverageLedger 0.3 child Schema与versioned conformance只能在doc283已审计的A–J有限边界内进入实现；这项授权不等于
实现已经成立，也不授予composition、transport或publication。**
