# R1 negative-world Coverage authority recovery — exact-input 后继审计

日期：2026-10-28

> 候选状态：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDIT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是 qualified history，也不授权 Coverage producer、manifest、Evidence、persistence
> 或 public Review 施工。
>
> 审计基线：`main@02705eb21e9d416ab34f857f1b09e463fc37551e`；tree
> `437a7af7c567b14dd92a3d0e774294656a87cafc`。
>
> 上游：[negative-world Coverage authority recovery审计](319-r1-negative-world-coverage-authority-recovery-audit.md)、
> [CoverageLedger 0.3冻结发布](286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)、
> [positive composition冻结发布](314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)与
> [Fact→Coverage exact-input successor实现冻结发布](330-r1-fact-to-coverage-exact-input-successor-private-implementation-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_CURRENT_STATE_AUDIT`。

## 1. CONTROL LOOP 与qualified起点

文档330由PR #381以
`base=8f258e3c4fb425af3d057493a63009c3099f03c4 / head=04fb41973ca1dc99ea8962b20d0eff6925103587 /
tree=437a7af7c567b14dd92a3d0e774294656a87cafc`受保护合入本审计基线。original Public CI
`40563101450`、exact-main Public CI `40567545888`与Browser Smoke `40567545741`均为attempt 1 SUCCESS，分别为
11/11、11/11与1/1。

fresh anonymous installed-product readback对README、doc329、doc330与milestones各取得唯一
`FORMAL_READBACK_PASS`。milestones diagnostic #1的HTTP 200 response-body观察中出现3个`BlockedByClient`与1个
`ConnectionClosed`，按原identity保留为`DIAGNOSTIC_ONLY_NON_QUALIFYING`；fresh diagnostic #2与formal使用新identity，
不覆盖它。independent reconciliation、161-artifact finite closeout与finite integrity为：

```text
f569847502882ea85a2455bdba5ea01d4a727cebed945fb64996983ce43137be
36b7e8b16c0016969e80bcfef6ae923ac56f1992d0689651eaac81d7ec501e00
d3cc4dc518627d59090166465cb1cf916e3c306e54f3205b047f31bb9811c816
```

closeout stdout self-capture mismatch
`a2a81680c904759d5e33553a720eef1aeb9f5e7664f9db5ad1f9d3c2bf302273`继续保留；其余160项终态一致。
因此起点事实是：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

fresh CONTROL LOOP只重审doc319留下的第一条upstream seam：0.2 exact-input carrier冻结以后，四个Fact阻断world是否已经
拥有可消费的Coverage结果构造authority。第二条same-attempt DerivationEvidence continuity保持正交，本文不提前进入。

## 2. 必须分开的三个问题

本轮把“输入可得”“目标语义存在”与“runtime有权构造结果”分开：

```text
exact original input authority
    != negative-world Coverage semantics
    != application-owned Coverage producer/admission
```

doc319证明0.1 handoff只有Fact terminal history与digests，无法枚举完整Snapshot/Policy分母。doc329–330新增并冻结的0.2
carrier解决的是第一个问题：它在Fact terminal重验以后，把产生该closure的原始`DerivationInputSet`、原始`BudgetContext`、
exact source与one-shot claim绑定到同一object graph。它明确不产生Coverage obligation、status、Ledger、manifest或publication
authority。

CoverageLedger 0.3已经解决第二个问题：冻结conformance corpus包含四个safe-negative Fact branches、ordered absent predecessor
bindings、七stage partition与保守overall status。validator仍是validation-only；它不枚举root、不生成candidate、不取得live claim。

所以当前审计的关键问题不是“Ledger会不会表示负世界”，而是：是否已经存在一个应用侧producer，能消费0.2 carrier，机械构造
完整denominator、branch-specific root history、Coverage stages与0.3 candidate，并取得same-attempt admission。

## 3. 0.2已经关闭原input-authority blocker

read-only audit在五个terminal worlds重建carrier：normal、zero Parse、all Parse rejected、projection blocked与required Provider
non-success。四个Fact阻断world均保持`fact_set = null`，但carrier仍能逐项读取：

- exact SourceSnapshot inventory；
- total ReviewPolicy scope decisions；
- DerivationProfile；
- verified blob map；
- 五个input digests、三份canonical bytes与input-state seal；
- Fact terminal branch、parse partition、Fact U/E/blockers、Provider history与责任；
- 原始BudgetContext与shared one-shot claim identity。

`ZERO_PARSE_DENOMINATOR`的empty与unsupported-only world仍分别恢复`Snapshot/Policy = 0/0`与`1/1`；它们不再因为Fact可见
状态相同而被压成同一分母。required Provider failure中parent eligibility保持`REVOKED`，carrier依靠terminal authority工作，
没有复活Provider execution authority。

因此doc319的历史结论继续成立于0.1，但当前0.2 world中的input-authority blocker已经关闭：

```text
prior blocker = CLOSED_BY_FROZEN_EXACT_INPUT_SUCCESSOR
```

这不回写doc319，也不把0.2 carrier升级成Coverage producer。

## 4. 负世界Coverage目标语义已经冻结

`review-coverage-ledger-0.3` compatibility corpus中的四个positive negative-world vectors均由当前conformance重新验证通过：

| Fact branch | Fact root | Relation root | Slice root | overall |
| --- | --- | --- | --- | --- |
| `ZERO_PARSE_DENOMINATOR` | `QUALIFIED_ABSENT` | `PREDECESSOR_ABSENT` | `PREDECESSOR_ABSENT` | `COMPLETE` |
| `ALL_PARSE_REJECTED` | `QUALIFIED_ABSENT` | `PREDECESSOR_ABSENT` | `PREDECESSOR_ABSENT` | `PARTIAL` |
| `PROJECTION_BLOCKED` | `QUALIFIED_ABSENT` | `PREDECESSOR_ABSENT` | `PREDECESSOR_ABSENT` | `UNKNOWN` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `QUALIFIED_ABSENT` | `PREDECESSOR_ABSENT` | `PREDECESSOR_ABSENT` | `UNKNOWN` |

这些vectors证明目标branch/state/history/status vocabulary存在且可被0.3 validator接受。它们是conformance witnesses，不是
当前attempt的owned runtime result，也不能被复制成live authority。

## 5. 当前runtime仍没有consumer/producer

current source的机械结果是：

1. `ClaimedFactToCoverageExactInputHandoff`在private runtime中只出现在它自己的定义模块；没有第二个runtime模块消费它；
2. frozen positive composition的唯一入口类型是`ClaimedRelationTransitionSliceBridgeContinuation`，而Fact→Relation transition
   明确只接受`NORMAL_FULFILLED`；四个Fact阻断world无法进入该入口；
3. positive composition虽能从其原始inputs枚举Snapshot/Policy并构造七stage Coverage，但其Relation/Slice authority与
   negative predecessor-absent world不同，不能把旧成功路径的authority别名给负世界；
4. CoverageLedger conformance明确不枚举root、不修复candidate、不取得composition claim；
5. 没有application-owned result wrapper、phase commit、negative-world admission或one-shot consumption boundary。

所以当前结论是：

```text
exact input authority                  = AVAILABLE
negative-world Coverage 0.3 semantics = AVAILABLE
negative-world runtime producer       = ABSENT
direct construction authority         = NOT_AUTHORIZED
missing authority boundary             = APPLICATION_OWNED_NEGATIVE_WORLD_COVERAGE_PRODUCER_AND_ADMISSION
```

这不是算法不存在，也不是0.3或positive composition被击穿。缺的是一个有限、独立、application-owned的producer与admission seam。

## 6. 最小后继合同边界

最小下一seam是：

```text
NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT
```

后继合同应只冻结以下责任：

1. exact consumer/function/result identities与四个适用Fact terminal branches；
2. 只接受unconsumed、live、exact 0.2 carrier，拒绝legacy 0.1、normal Relation continuation、equal foreign inputs与replay；
3. 从carrier独立重建完整Snapshot inventory、Policy scope、Language Support、Parse与Fact partitions；
4. 从Fact terminal history构造branch-specific `QUALIFIED_ABSENT` Fact root，并把Relation/Slice严格标为
   `PREDECESSOR_ABSENT`，不得生成synthetic empty artifacts；
5. producer与独立validator分别计算denominator、root chain、stage partition、reason与overall status，避免共同漏项；
6. 复用frozen CoverageLedger 0.3 conformance，但不得修改Schema、reason order、root semantics或positive composition；
7. 在同一BudgetContext中exactly-once commit，任何stop、mutation、foreign object、unknown branch或conformance mismatch均撤销；
8. authority ceiling停在private negative-world Coverage result，不授予manifest、Evidence、persistence、public Review或R2–R6。

具体class、method、字段、异常类型与实现算法仍是implementation non-decision。合同、freeze、implementation feasibility、authorization、
candidate与freeze publication必须分别取得自己的资格。

## 7. 机械审计与回归witness

read-only audit identity为：

```text
r1-negative-world-coverage-authority-recovery-after-exact-input-audit/0.1
```

Python 3.10.6/3.13.13 × normal/`-O`四格均PASS，canonical report逐字节一致：

```text
851fd5814cc8997611241c1a00fa13a06f207c42b6a1547605f5eb9640a2ee86
```

focused witness覆盖CoverageLedger 0.3、Language Support、Fact terminal、0.1 handoff、0.2 exact-input successor、Fact→Relation
transition与positive composition；四格各`139 tests / 138 passed / 1 skipped`。测试只证明current bytes与本审计观察稳定，
不创建producer authority。

首次尝试使用Codex managed-worktree API时，`sourceRoot`不是chat workspace root；随后对manual worktree执行attach又被拒绝为
not-managed checkout。另一个旧同名worktree已经承担doc319历史，新的施工使用不同path/branch，没有删除、重置或覆盖旧身份。
这些都是operator/setup observations，未修改产品、oracle或审计结论。

## 8. 本candidate资格门与状态上限

tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。doc281、doc286、doc314、doc318–330、runtime、
tests、workflows、Schema、fixtures、CoverageLedger、composition、Evidence、Policy/Profile、persistence与public产品保持base bytes。

final bytes至少复核exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、unique headings、
状态markers、frozen hashes、`git diff --check`、read-only global/local hygiene与primary `audit.json` continuity。随后依次：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc330 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / frozen-history reconciliation
    -> qualified current-state audit history
    -> return CONTROL LOOP
```

全部闭合以后，状态上限为：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDITED_INPUT_AVAILABLE_PRODUCER_ABSENT
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整资格链闭合以前，上述`AUDITED` target不生效。闭合以后必须返回CONTROL LOOP，从新exact main独立建立最小producer
合同；不得直接修改runtime、消费旧composition authority、实现manifest/Evidence、选择persistence或启动public Review、
post-R1 Benchmark与R2–R6。
