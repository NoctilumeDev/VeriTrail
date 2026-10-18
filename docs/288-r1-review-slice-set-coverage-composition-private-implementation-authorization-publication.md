# R1 ReviewSliceSet / Coverage composition 私有实现授权发布

日期：2026-10-18

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 基线：`main@de21b3a2fadf436b22d91b7d90c218a6c868f77c`，tree
> `a211c8b3f1bb8333215bd45f8834d37d0a027ad7`。
>
> 上游：[composition qualification 合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [root binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)、
> [CoverageLedger 0.3 私有实现冻结发布](286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)与
> [composition 私有实现可行性审计](287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)。
>
> 影响：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`；docs-only。
> `COMPOSITION_IMPLEMENTATION_ALLOWED` 仅为条件目标，本文最后门全部闭合以前不生效；composition runtime、tests、
> fixtures、vectors、manifest successor、persistence 与 public Review 产品仍未开始。

## 1. CONTROL LOOP 与当前 authority

文档 287 已由 PR #329 final head `fd02f92ea1047ac6b246585bb167d4681625bca3` 合入本基线的祖先：

```text
base  = ac41b5c852a7f79607fa3bcc771ea0b7858abeb9
head  = fd02f92ea1047ac6b246585bb167d4681625bca3
merge = 0dc7f832b7f77a1926c6ab7807805f9939e56246
tree  = 643719aa3b29b31d276915e225685c5deb86f5a2
```

original Public CI `39113130924`、exact-main Public CI `39114897070` 与 Browser Smoke `39114897054` 均为
attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1。fresh README/doc287/milestones 各有且仅有一份 qualifying
PASS；independent reconciliation 与 141-artifact closeout 分别为：

```text
07cf069ccc901f30ce8ac28d01623a6b711256e665fa14211a92038a80f657d4
efccb6067ff3e974361e043cfd22bbd27489b5833d638492223740b19a9e51b9
```

文档 287 的 full-file SHA-256 为：

```text
18171855a8fe250e5531e5675349539287fa2e769fba99fe47f80b72c8a96490
```

因此以下事实已经成为 qualified history：

```text
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

PR #330 final head `a90595f2e5c46d5859f74d7d0fd441713b4c13eb` 随后只修改 README 的读者说明，并合入当前
`main@de21b3a2fadf436b22d91b7d90c218a6c868f77c`；它没有修改合同、runtime、Schema、tests 或文档 287，也不拥有
R1 状态 authority。fresh CONTROL LOOP 已因此放弃旧基线上的候选资格，重新绑定当前 exact main、frozen contracts、
Fact handoff、legacy Relation/Slice path、CoverageLedger 0.3 conformance 与 manifest 0.1，不能跨 world 继承旧资格。

没有新反例要求重开 Fact、Relation、ReviewSlice、composition qualification、root-binding 或 CoverageLedger 0.3
合同。文档 287 已证明 bounded versioned successor 可在原始 Fact handoff、原始 `BudgetContext`、现有低层 Relation
primitive、现有 Slice closure 与 validation-only 0.3 conformance 上实现；manifest negative-world publication 与
persistence 均不是 private composition blocker。当前最小合法候选仍是文档 287 §8 的 A–J 私有实现 authority。

## 2. feasibility witness 不冒充实现证明

文档 287 的 read-only audit只证明当前 source topology 存在一条有限实现路径。CPython 3.10.6 / 3.13.13、normal /
`-O` 四格的 canonical report 逐字节一致：

```text
14210f1ce528b09f7ab9c5808105637287c1c082175f79a1c1c7b6fb6d03fed3
```

前三次 audit harness 失败分别来自参数名臆测、调用图层级误判与过宽 filename predicate；后继 PASS 没有覆盖它们。
installed-product readback 前的 adapter replacement、PowerShell native glob、Plan ID 长度与 mutable setup history freeze
问题也继续由 setup/proof-facility history 拥有。fresh freeze只修复证明设施边界，没有修改产品 oracle、预算、target或正式
observation；formal history 为3 PASS / 0 non-success。

因此：

```text
finite feasibility
    != implementation authority
    != implementation started
    != implementation qualified
    != implementation frozen
```

## 3. 条件化的最小施工面

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多实现文档 287 §8 的
bounded A–J：

| ID | 最大施工面 |
| --- | --- |
| A | application 创建一个 private composition attempt，绑定 exact `DerivationInputSet`、一次领取的 Fact handoff 与其原始 `BudgetContext`；相同 bytes、digest、limits 或 semantic result 不继承 attempt |
| B | 消费前复核 exact source、safe branch、Fact terminal history、Provider responsibility、FactSet 或 qualified absence 与原始 context object；serialized document 或 digest holder 不取得 live authority |
| C | 增加 versioned post-handoff Relation qualification successor；只用 handoff FactSet、sealed Relation domain 与现有 low-level workers，在原始 context 中运行，不创建新 Fact attempts |
| D | 增加 successor RelationSet admission，绑定新 qualification、Provider responsibility、same attempt、request provenance 与完整 terminal history；legacy admission bytes保持不变 |
| E | 增加 same-attempt Slice successor，以 exact successor admission、inputs 与 context进入现有 obligation/traversal/reconciliation/closure primitive；不得由 RelationSet digest恢复 continuation |
| F | 从 exact Slice closure 构造 private ReviewSliceSet projection，再由独立 application admission核对 normal、partial、closed-empty、blocked 与 unknown worlds；content identity 与 admission authority 分离 |
| G | 从 authoritative upstream history构造七段 `S/A/N/D` 与六个 transition proofs；不得缩小 denominator、允许成员重现，或用 representable set 冒充 obligation universe |
| H | 形成 total stage qualification、conservative overall join、ordered root binding 与 0.3 candidate；最后才调用 validation-only conformance，且 Coverage 不改写上游失败身份 |
| I | 全部 required reconciliation 完成后才产生 one-shot private composition closure/continuation；它不取得 persistence、manifest、public product、Evidence 或 publisher authority |
| J | 固化 `RSCQC-000..017`、`RBCC-000..011`、legacy byte guards及3.10/3.13 normal/`-O` canonical reports，直接拒绝 foreign attempt、Fact rerun、digest-only authority、partial Provider merge、unknown promotion、denominator shrink/reappearance 与 caller bool自授权 |

文件布局、private helper 名和测试数量不是本文的合同。实现允许增加 bounded versioned private successor，但必须保留 legacy
high-level Relation/Slice entry、admission、Schema 与历史 bytes。测试只作 witness，不拥有 denominator、classification、
fulfillment、admission 或 continuation authority。

## 4. 必须保持的 authority ceiling

后继实现不得：

- 调用 legacy high-level Relation qualifier而创建新 `BudgetContext` 或重跑 Fact；
- 让 Relation/Slice/Coverage 通过 content digest、serialized source或equal-limits context继承live authority；
- 让 Provider、caller、Schema、conformance、manifest或digest holder定义denominator、root truth或same-attempt claim；
- 把 representable set当作obligation universe，丢弃不可表示、missing、blocked、unknown或qualified absence历史；
- 把多个Provider的partial history拼成complete，或把unknown/failure重分类为normal completion；
- 修改doc259–287、legacy runtime/types、CoverageLedger 0.1、common 0.1、manifest 0.1或冻结fixtures/corpus；
- 选择manifest successor、negative-world publication topology、persistence Route A/B或public self-contained verification；
- 启动public `ReviewSliceSet` / `CoverageLedger`、Evidence、Bundle、publisher、CLI、Workbench、Core、R2/R3、
  CLAIM_FIDELITY、tag或Release。

CoverageLedger 0.3 conformance仍只允许validation-only：application先从exact authoritative history构造candidate，conformance
随后单向拒绝不合格输入。caller提供`authority_safe=True`、通过Schema或得到合法digest，都不能生成未取得的authority。

## 5. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止，只重开被击穿的最小边界：

1. low-level Relation domain/cell无法消费handoff FactSet与原始context；
2. 必须修改legacy Relation/Slice types或history bytes，而不能增加bounded versioned successor；
3. ReviewSliceSet admission无法绑定exact Slice closure与same-attempt history；
4. private negative worlds必须先取得manifest successor、persistence或public carrier才能闭合；
5. 必须信任caller bool、serialized source或digest holder生成authority；
6. Coverage必须重新定义上游denominator、failure identity或terminal history；
7. `RSCQC` / `RBCC` direct falsifier暴露冻结合同内部矛盾，而不是局部implementation defect；
8. known negative world只能通过弱化oracle、跳过conformance或移动成功条件获得PASS。

授权已经生效也不能成为扩大scope、修 oracle 或静默 reopen frozen contract 的理由。

## 6. 本 publication 的资格门

tracked scope只允许 `README.md`、`AGENTS.md`、`docs/milestones.md` 与新增本文。doc259–287、runtime、tests、
workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产必须保持base bytes。

final bytes至少完成：四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、状态marker、上游frozen-byte
continuity、`git diff --check`、read-only hygiene，以及声明的Markdown/Schema baseline regressions。随后仍需：

```text
final docs-only publication bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc287 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> COMPOSITION_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

same patch、tree、content、digest、semantic result或feasibility witness都不能替代上述任一资格身份。本地checkout对齐只作
housekeeping，不新增授权生效门。

## 7. 生效前后与实现自己的门

本文进入仓库、PR CI绿色或target marker可见前后，事实必须分开：

```text
before publication last gate:
    feasibility audit = AUDITED
    composition implementation authority = NOT_AUTHORIZED
    composition implementation = NOT_STARTED

after publication last gate:
    feasibility audit = AUDITED
    composition implementation authority = ALLOWED
    composition implementation = NOT_STARTED
```

本文第6节全部门闭合以前，只允许发布：

```text
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

最后门闭合以后也只是 `ALLOWED / NOT_STARTED`。必须重新绑定新的 exact main、检查并行事实并确认 A–J仍是最小合法
seam，才可创建 implementation branch。后继 implementation需要自己的final bytes、direct falsifiers、四格、original PR、
protected merge、exact-main gates、fresh product observation、independent reconciliation与独立冻结发布；本文不替它证明或冻结。

## 8. stop line

本文不授权 composition implementation candidate本身，也不授权manifest successor、persistence或public Review产品。当前授权
原则候选冻结为：

> ReviewSliceSet / Coverage composition may enter private implementation only through doc287's bounded A–J versioned
> successor, preserving the original Fact attempt and upstream failure identities; this authority does not establish the
> implementation, transport, persistence or public publication.

中文：**ReviewSliceSet / Coverage composition只能沿doc287限定的A–J versioned successor进入私有实现，并保留原始Fact
attempt与全部上游失败身份；这项授权不等于实现已经成立，也不授予transport、persistence或public publication。**
