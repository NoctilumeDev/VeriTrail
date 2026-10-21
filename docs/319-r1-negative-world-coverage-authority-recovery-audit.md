# R1 negative-world Coverage authority recovery current-state correction audit

日期：2026-10-21

> 候选状态：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDIT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是 qualified history，也不授权创建 Fact→Coverage handoff successor、Coverage
> producer、manifest、Evidence、persistence 或 public Review 产品。
>
> 审计基线：`main@03b6d49a37a09f0d3cd2cdac4dca29454206e704`；tree
> `1abe4a4fcc958ba306f59c420f355718af699922`。
>
> 上游：[manifest implementation feasibility correction audit](318-r1-review-derivation-manifest-negative-world-successor-implementation-feasibility-correction-audit.md)、
> [Fact→Coverage handoff 0.1 contract](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)与
> [0.1 implementation freeze](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_CORRECTION_AUDIT`。

## 1. CONTROL LOOP 与已取得资格的起点

文档318由PR #365从
`base=8cdd613c3848476f7c4c0162f42581dc32903a33 / head=65e6e4c98f1cc4a4da18c4c1df4a5d1a141eb748 /
tree=1abe4a4fcc958ba306f59c420f355718af699922`受保护合入本审计基线。original Public CI
`39537858764`、exact-main Public CI `39540823614`与Browser Smoke `39540823601`均为attempt 1 SUCCESS，
分别为11/11、11/11与1/1。

fresh anonymous installed-product readback对README、doc317、doc318与milestones各保留一份唯一
`FORMAL_READBACK_PASS`。independent reconciliation与234-artifact finite closeout为：

```text
3bb7c89c434d526b675430c9539469aca96b307c6eb5119ebfed4f4399602743
048fdd8f0196d90d3d14c8fb103b21bd18bae01f3accc6d783055f2b32a47776
```

因此本审计基线已经发布：

```text
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_FEASIBILITY_AUDITED_BLOCKED_BY_UPSTREAM_PRIVATE_AUTHORITY_GAPS
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

fresh CONTROL LOOP只重开文档318指出的第一条最小上游seam：现有`ClaimedFactToCoverageHandoff`能否在不改变冻结
0.1历史、不发明输入authority的条件下，直接支持四个Fact阻断world的Coverage构造。

## 2. 审计问题与判定纪律

本轮只回答：

```text
现有Fact→Coverage handoff 0.1是否已经携带足够、可机械证明的same-attempt输入authority，
使Coverage producer能够完整构造SNAPSHOT_INVENTORY与POLICY_SCOPE obligation universe？
```

必须同时满足：

1. Snapshot分母是exact terminal SourceSnapshot inventory，不能只保留下游可读文件；
2. Policy分母对Snapshot成员执行total classification，不能只保留`IN_SCOPE`成员；
3. carrier必须证明输入属于原始same-attempt object graph，不能用一个后来重建、内容相等的对象替代；
4. Fact阻断状态、one-shot ownership、live `BudgetContext`与0.1 frozen bytes必须保持；
5. digest只能证明被摘要字节的identity，不能代替成员枚举、对象来源或消费权限。

这是一项authority与denominator审计，不是Coverage算法选择，也不把“当前接口不足”误写成“合法算法不存在”。

## 3. 正常路径拥有输入，但不能消费Fact阻断世界

corrected Fact→Relation transition通过`_claim_relation_handoff_source()`取得原始`DerivationInputSet`，并在private
`_inputs_ref`中保持live same-attempt引用。normal composition随后从该对象调用：

```text
source_snapshot_document_copy()
review_policy_document_copy()
```

由此构造`SNAPSHOT_INVENTORY`与`POLICY_SCOPE`。这条路径说明当前runtime能够在已有authority时保留完整输入；它不是
“所有路径都丢失原始输入”的反例。

但`_fact_relation_transition.py`的source identity验证要求：

```text
source.branch == NORMAL_FULFILLED
FactSet is complete
```

因此以下四个Fact阻断world不能进入normal Relation composition：

```text
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

normal path的authority不能越过自己的applicability边界替这些world签发Coverage。

## 4. 0.1 handoff保留阶段历史，但不携带Coverage输入分母

`ClaimedFactToCoverageHandoff` copy-own canonical document bytes并携带live `BudgetContext`。它公开的产品接口只有
`document_copy()`，private接口只有`_context_ref()`；它没有`_inputs_ref()`，也没有可枚举的SourceSnapshot/Policy成员carrier。

`_fact_fulfillment.py`写入handoff source的字段包括：

```text
branch
input identity digests and attempt identifiers
parse_partition
fact_projection
provider_history
fact_set or null
whole-attempt budget and eligibility
```

它不序列化SourceSnapshot inventory、Policy scope decisions、input canonical bytes、verified blob map，也不保留原始
`DerivationInputSet`引用。因此0.1能证明“这个Fact阶段怎样终结”，不能证明Coverage所需的全部输入成员是什么。

文档259把0.1 semantic input绑定到exact `DerivationInputSet`；文档264同时冻结它是Fact-stage history handoff，并明确不授予
Coverage vocabulary、status、join或publication。当前缺口是后续Coverage用途首次提出的新输入责任，不是对0.1历史的追溯违约。

## 5. 三个机械反例：相同的Fact可见状态，不同的Coverage分母

read-only harness以三个exact input world调用现有Fact fulfillment与handoff：

| world | Snapshot inventory | Policy scope | handoff branch | Parse denominator/accepted/rejected | Fact U/E | FactSet |
| --- | ---: | ---: | --- | --- | --- | --- |
| empty Snapshot | 0 | 0 | `ZERO_PARSE_DENOMINATOR` | `0/0/0` | `0/0` | null |
| unsupported-only `a.txt` | 1 | 1 | `ZERO_PARSE_DENOMINATOR` | `0/0/0` | `0/0` | null |
| Policy-excluded-only Python | 1 | 1 | `ZERO_PARSE_DENOMINATOR` | `0/0/0` | `0/0` | null |

三个world在Fact阶段的可见计数与终态完全相同，但Coverage的Snapshot/Policy obligation universe不同。handoff文档中的digest
可以区分完整输入identity，却不能从digest逆推出成员列表、每个成员的Policy disposition或blob authority。

如果Coverage producer把`ZERO_PARSE_DENOMINATOR + 0/0/0 + Fact U/E 0/0`解释成前两个Coverage stage也是空集，
它会在后两个world缩小真实分母。这正是既有`SCQ-001`类反例：局部Schema与方程可能全部成立，最终`COMPLETE`仍然是假的。

## 6. 内容相等的旁路输入不能恢复原始authority

调用者可以在handoff之外保留一个`DerivationInputSet`，甚至重建一个canonical bytes与digest完全相等的对象。但当前handoff没有
对象引用、one-shot claim或其他binding，能够机械证明这个旁路对象就是产生handoff的原始same-attempt input graph。

因此：

```text
equal bytes / equal digest != original object-graph authority
```

允许任意调用者把内容相等对象与handoff拼接，会重新引入cross-world与cross-attempt authority substitution。禁止这种拼接不否认
semantic equality；它只拒绝让equality自动取得消费权限。

## 7. 判定：版本化successor是最小重开边界

审计结果为：

| 观察 | 分类 | 影响 |
| --- | --- | --- |
| 0.1准确保留五个Fact终态与same-attempt Fact历史 | frozen history remains valid | 不重写doc259–264 |
| normal Relation path保留原始inputs | existing positive authority | 不修改normal transition/composition |
| normal path拒绝四个Fact阻断world | intended applicability boundary | 不绕过source validation |
| 0.1 handoff不能枚举Snapshot/Policy完整分母，也无inputs reference | unproved downstream authority seam | negative-world Coverage不得开始 |
| 最终successor结构 | open construction problem | 本文不选择实现 |

最小后继是：

```text
VERSIONED_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR
```

后继可行性审计必须至少比较：保留live original `DerivationInputSet`引用，或copy-own一个包含exact terminal Snapshot inventory、
total Policy classifications与必要blob identity的输入carrier。无论选择哪一种，都必须保持0.1 bytes/history、五分支、one-shot、
live `BudgetContext`、attempt identity与no-Coverage-status ceiling；不得让successor自己生成expected denominator再自证完整。

在该successor取得独立合同、授权、实现与冻结资格以前：

```text
negative-world Coverage producer = NOT_STARTED / NOT_AUTHORIZED
manifest implementation          = NOT_STARTED / NOT_AUTHORIZED
same-attempt Evidence continuity = NOT_STARTED / NOT_AUTHORIZED
```

## 8. 机械审计与回归witness

read-only audit identity为：

```text
r1-negative-world-coverage-authority-recovery-audit/0.1
```

attempt 1的Policy-only fixture错误使用不存在的`EXCLUDED` disposition；四格均在fixture setup阶段失败，没有产品执行、产品观察或
oracle变化。该identity以`AUDIT_PROOF_FACILITY_POLICY_DISPOSITION_FIXTURE_SETUP_ERROR`保留。

独立冻结的attempt 2只把fixture值改为frozen Policy vocabulary中的`OUT_OF_SCOPE`。Python 3.10.6/3.13.13 × normal/`-O`
四格均PASS，canonical report SHA-256一致：

```text
a5c55a127b157e06df616b0b4e5634adbfc5908e5b6aa50e77d4c0877b0634e4
```

candidate audit attempt 1虽然四格退出0，但证明设施用`strip()`读取porcelain输出，导致第一行` M AGENTS.md`被错误记录为
`M AGENTS.md`；这组输出以
`CANDIDATE_AUDIT_PROOF_FACILITY_PORCELAIN_LEADING_COLUMN_ERROR`保留且不参与资格。独立冻结的修正只把输出处理改成移除行尾，
不改变产品调用、world构造或oracle。final audit脚本SHA-256为：

```text
2732cb3709f7a3aa782fd9844702fba303c33e1e7a2472b7dc13d9840415cf8a
```

修正后的clean-base attempt 3仍在四格得到同一canonical report SHA
`a5c55a127b157e06df616b0b4e5634adbfc5908e5b6aa50e77d4c0877b0634e4`；candidate attempt 2也在四格稳定保留
exact four-file porcelain状态，canonical report SHA为
`fd2ad9f31583c7f2261a95491728819adf8b35750ef0b0f8b3bf6a94e94f6a65`。

focused witness覆盖CoverageLedger 0.3、Fact→Coverage handoff、Fact→Relation transition与current composition。Python
3.10.6/3.13.13 × normal/`-O`四格各99/99 PASS。测试只验证冻结行为与本审计观察稳定，不授予缺失authority。

## 9. 本候选资格门与状态上限

tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。doc259–318、runtime、tests、workflows、
Schema、fixtures、CoverageLedger、composition、Evidence、Policy/Profile、persistence与public产品必须保持base bytes。

final bytes至少复核exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、unique headings、
状态markers、frozen hashes、`git diff --check`、read-only global/local hygiene与primary `audit.json` continuity。随后依次：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc318 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / frozen-history reconciliation
    -> qualified correction audit history
    -> return CONTROL LOOP
```

全部闭合以后，状态上限为：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_FEASIBILITY_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合以前，上述`AUDITED` target不生效。闭合以后必须返回CONTROL LOOP，从新的exact main独立建立
Fact→Coverage exact-input successor feasibility审计；不得从本审计直接创建successor、Coverage producer或manifest实现。
