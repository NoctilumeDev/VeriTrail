# R1 ReviewSliceSet / Coverage composition authority recovery 当前状态审计

日期：2026-10-20

> 状态：`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDIT_CANDIDATE`。
>
> 坐标：`main@e88310ca1c4c5a382d097e8d0b68193b106549c5`，tree
> `43ac035e0cd2e012fac5b390f54244f591551a40`。
>
> 上游：[composition qualification 合同](267-r1-review-slice-set-coverage-composition-qualification-contract.md)、
> [composition 私有实现可行性审计](287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)、
> [旧 composition 实现授权](288-r1-review-slice-set-coverage-composition-private-implementation-authorization-publication.md)、
> [Fact → Relation transition 候选](309-r1-fact-handoff-relation-corrected-successor-private-transition-implementation-candidate.md)与
> [transition 冻结发布](310-r1-fact-handoff-relation-corrected-successor-private-transition-implementation-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只审计冻结 Fact → Relation transition 后旧 composition stop
> condition 与 authority recovery 的 current state；不修改 runtime、tests、workflows、Schema、Policy/Profile、manifest、
> persistence、Coverage、public Review 产品或 R2–R6，也不恢复 implementation authority。

## 1. CONTROL LOOP 与 exact source state

文档 310 由 PR #355 从 base `eadccc6023196e5b31c3bf312f5de2c4578d2f5d`、head
`c2dd1ed7b9b8d2cb6e82a523eadfabbc390ae77b`、tree
`43ac035e0cd2e012fac5b390f54244f591551a40` 精确合入本基线。三个公开门均使用原始 attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #355 original Public CI | `39421644660` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39425547417` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39425547424` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product doc309、doc310、milestones 与 README 各有唯一 `FORMAL_READBACK_PASS`。independent
reconciliation、162-artifact closeout 与 finite integrity 分别为：

```text
f4fac71760ebb77cc676e2040852be29d6df36ee1da9e0f02e5cad55af5232e5
bd97fe2171315408a2248bcd2e045946d7727865d1aa6b816abb265d72552054
671d65e2680a0c69ef785cbbfe43ef9089f8d907dda71186c678555a9abb5d37
```

milestones marker preconfiguration、GraphQL review-thread query、reconciliation inspection encoding、publication wrapper quoting、
remote-main no-proxy、Codex sidebar artifact cap 与 `Start-Process` policy rejection 均保留为 setup/proof-facility history；它们没有
修改产品字节、oracle、formal observation 或资格结论。closeout stdout self-capture mismatch也只涉及wrapper自己的输出；其余161项
终态一致。因此：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
```

现在已经生效。本文从这个 exact world 重新审计 composition；不把文档编号、局部节点资格或后继 PASS 当作旧 authority 自动复活。

## 2. Fact → Relation stop condition 已解决，但 authority ceiling 没有跨到 Slice

冻结 transition 在同一 sealed Policy、完整 authoritative FactSet、original live `BudgetContext` 与 one-shot handoff 上取得
`QUALIFIED` admission。fresh audit 的默认 world 为：

```text
Fact count       = 14
obligation count = 10
Relation count   = 10
```

obligation 与 Relation cardinality闭合，admission继续绑定stage applicability、per-product closure、total Fact partition、完整Provider
assignment、terminal/receipt lineage与same-attempt identity。continuation保留同一个`DerivationInputSet`、`BudgetContext`与
`AttemptEligibility`对象，且第二次claim正确拒绝。

但冻结carrier自己的authority ceiling明确为：

```text
private Relation transition = true
ReviewSliceSet              = false
Coverage                    = false
manifest                    = false
persistence                 = false
public Review               = false
```

这不是缺陷。文档290、309与310从未声称Fact → Relation边会自动生成Relation → Slice或Coverage authority。把
`PRIVATE_IMPLEMENTATION_FROZEN`解释为整个A–J composition已经恢复，会再次犯“两个合法节点自动产生合法箭头”的错误。

## 3. current Slice input 对新 transition 正确 fail closed

current Slice入口
`admit_relation_set_for_slice_input_private_closed_proof()`只接受exact
`OwnedRelationQualificationContinuation`。它在运行时使用exact type gate，并只允许由private
`_QUALIFICATION_BINDING_TOKEN`构造的legacy same-attempt continuation进入后续admission binding。

新 transition产生的是两个不同对象：

```text
OwnedFactRelationTransitionAdmission
ClaimedFactRelationTransitionContinuation
```

fresh audit分别把这两个对象交给current Slice入口，均得到：

```text
ADMISSION_BINDING_REJECTED
```

源码中没有`ClaimedFactRelationTransitionContinuation` consumer，也没有从新transition admission到
`OwnedRelationQualificationContinuation`的adapter。content相同、RelationSet完整、same input/context/eligibility或digest holder都不能
绕过exact type与constructor token。current rejection因此保护了旧Slice authority边界；不得通过放宽type check、暴露token、伪造legacy
qualification或重跑standalone Relation来“接通”流水线。

## 4. 缺失的是 versioned Relation → Slice authority bridge

当前 source state同时保留了继续研究所需的低层事实：

- transition continuation copy-own exact admission bytes，并保留original live inputs/context/eligibility；
- transition admission包含complete RelationSet、Fact handoff history、Provider terminal/receipt与same-attempt lineage；
- existing Slice primitives已经分别实现exact admission binding、input claim、cross-validation、obligation domain、assignment、traversal、
  reconciliation、closed-empty与blocked-input receipt；
- CoverageLedger 0.3 conformance继续只作validation-only拒绝器，不生成authority；
- 文档267与287已冻结application-owned single composition attempt、versioned Slice successor、ReviewSliceSet admission、seven-stage
  denominator/transition proof、ordered root binding与conservative Coverage join的语义边界。

因此current exact world没有证明“旧入口可直接复用”，也没有证明需要重开frozen Fact、Relation、Slice、composition qualification或
CoverageLedger 0.3合同。缺失的最小对象是一个application-owned、versioned、one-shot的
`RELATION_TRANSITION_TO_SLICE_AUTHORITY_BRIDGE`：它必须独立重验transition admission、exact inputs、same context/eligibility、
complete RelationSet与terminal history，然后才可签发与existing Slice primitives兼容的successor authority。

这个bridge不能修改或扩张冻结transition本身的ceiling。正确结构是：transition继续只拥有Relation edge；composition application在
消费其one-shot continuation以后，依据独立合同与证据取得下一条边的authority。bridge失败或unknown时，transition的局部资格保持，
composition停止。

## 5. 旧 composition authority 仍不可直接消费

文档288的bounded A–J authorization历史保持真实；文档289的exact-input反例随后触发其stop condition。文档309/310解决了该反例中
Fact → Relation admission这一个最小边界，却没有回填旧world，也没有给旧authorization追加新transition identity、carrier或Slice
binding规则。

因此当前裁决是：

```text
old composition authorization history
    PRESERVED

direct consumption of old authorization
    NOT_ALLOWED

Fact -> corrected Relation admission
    FROZEN

Relation transition -> Slice authority bridge
    ABSENT

ReviewSliceSet / Coverage composition runtime
    NOT_STARTED
```

下一最小合法seam是：

```text
DOCS_ONLY_COMPOSITION_AUTHORITY_RECOVERY_PUBLICATION
```

该publication至多条件化恢复一个bounded private implementation authority：新增versioned application bridge消费exact transition
continuation，保留其original identity与ceiling，机械绑定existing Slice input primitives，再继续文档267/287限定的ReviewSliceSet与
Coverage A–J。publication不能自己构造bridge、启动runtime或声称composition已完成。

## 6. authority recovery publication 必须保留的边界

后继publication若仍是最小合法seam，必须明确禁止：

- 把transition admission或RelationSet digest直接当作Slice authority；
- 让legacy Slice exact-type gate接受successor bytes，或暴露/复用private constructor token；
- 重跑standalone Relation qualification、创建新`BudgetContext`或用equal inputs拼接另一attempt；
- 修改doc267/287、transition 0.1、legacy Relation/Slice types/history bytes或CoverageLedger 0.3 conformance；
- 在bridge前消费Slice obligation、构造ReviewSliceSet或让Coverage反向定义上游denominator；
- 丢弃blocked/unknown/closed-empty/partial Provider history，或把后继局部PASS回填旧stop world；
- 选择manifest successor、persistence route、public carrier/product、Evidence/Bundle/publisher、R2–R6、tag或Release。

后继implementation出现以下任一条件必须停下并重开被击穿的最小边界：无法在不修改transition ceiling的前提下消费one-shot
continuation；必须伪造legacy qualification；无法把exact transition admission与existing Slice primitives做双向重算；negative world必须
先选择manifest/persistence；Coverage必须改写上游failure/denominator/terminal identity；或只能靠放宽oracle获得PASS。

## 7. audit evidence 与 focused regression

read-only audit在CPython 3.10.6 / 3.13.13 × normal / `-O`四格得到同一semantic digest：

```text
audit script SHA-256 = c0048740269c3896fd533e966343ed2e3f8b1e6651b3c8b77b26bbf92d4a49a3
semantic digest      = 29a2cc8b30cd43b18cb8be214de88803dfdf9879e0930129a9ed26f7b943608b
audit summary SHA-256= cd14f3b04861c8643a19d0aa77be3c6cb5947b9fa463db5e4dc17479ca444423
verdict               = COMPOSITION_AUTHORITY_RECOVERY_FEASIBLE_PUBLICATION_REQUIRED
```

audit attempt 1错误地把`from __future__ import annotations`产生的string annotation按对象identity比较，四格均在report construction前
停止；`FUTURE_ANNOTATION_OBJECT_IDENTITY_COMPARISON_ERROR`原样保留，semantic/qualification effect均为`NONE`。attempt 2只修
proof facility的annotation检查，不改产品或audit worlds。

focused attempt 1从plugin tests目录运行，遗漏repository root tests import root；四格各在170项主体后以
`test_review_coverage_ledger_0_3` loader error终结。`TEST_ROOT_SELECTION_SETUP_ERROR`保持non-qualifying原identity。
fresh attempt 2显式包含两个test roots，Python 3.10.6 / 3.13.13 × normal / `-O`四格各为：

```text
193 reported / 193 passed / 0 skipped
focused summary SHA-256 = 770cf74e9a42158ac3637c04d21d40775eb02b1bb67c7b3a9e0b0d8dcbcefaf3
```

测试只见证transition、import-form Provider、Relation qualification/admission、Slice input join与CoverageLedger 0.3既有边界；它不拥有
authority recovery或bridge implementation资格。

## 8. 本 audit candidate 的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/311-r1-review-slice-set-coverage-composition-authority-recovery-current-state-audit.md
docs/milestones.md
```

doc267、doc287–310、runtime、tests、workflows、Schema、Policy/Profile、manifest、persistence、fixtures与全部保留evidence必须保持
`e88310c…` base bytes。final bytes至少完成exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、conditional
markers、upstream byte continuity、`git diff --check`、read-only global/local hygiene、primary `audit.json` hash continuity、audit四格与
fresh focused四格。

local validation attempt 1把正文状态声明与状态上限中合法重复出现的marker误设为全文唯一，因
`MARKER_CARDINALITY_PROOF_FACILITY_ERROR`在产品与资格裁决前停止；原脚本、trace与分类保持non-qualifying历史，semantic与
qualification effect均为`NONE`。attempt 2只把约束修正为“每项required marker至少存在一次”，没有修改本文结论、产品字节、audit
world、focused tests或oracle。该attempt随后又因proof facility引用了旧摘要中的doc299/303–308文件名而在upstream byte
continuity读取时停止；`UPSTREAM_FILENAME_SELECTION_PROOF_FACILITY_ERROR`同样保留为无semantic/qualification effect的
non-qualifying历史。attempt 3从exact tree修正这些文件名后，Windows Git的`git show <rev>:<long-path>`因命令行参数被当作
filesystem path而以`Filename too long`停止；`LONG_REV_PATH_GIT_SHOW_PROOF_FACILITY_ERROR`不否定`git ls-tree`与
`git cat-file -e`均确认该blob属于base。attempt 4只把同一blob读取改为`git cat-file blob`，不改变待比较文件集合、bytes或规则。

随后仍需：

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CURRENT_STATE_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

在全部门闭合以前，本审计只能是candidate。任何formal non-success必须保留原identity，N从history机械枚举；housekeeping不追加语义门。

## 9. 当前状态上限

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_RESOLVED_THROUGH_RELATION_ADMISSION_ONLY
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

若本候选取得资格，它最多成为`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。后继必须单独发布docs-only composition authority
recovery，不能从本文直接开始bridge施工，也不能选择manifest、persistence、Coverage public product或R2–R6。
