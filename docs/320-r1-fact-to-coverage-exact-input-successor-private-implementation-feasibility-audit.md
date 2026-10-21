# R1 Fact → Coverage exact-input successor 私有实现可行性审计

日期：2026-10-21

> 候选状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是 qualified history，也不授权创建 successor、Coverage producer、manifest、
> Evidence、persistence 或 public Review 产品。
>
> 审计基线：`main@9701b192b6b60499b70a5e429ecbbb83b1134b70`；tree
> `7615e0d04059f766d103c87383989851b57b7852`。
>
> 上游：[negative-world Coverage authority recovery审计](319-r1-negative-world-coverage-authority-recovery-audit.md)、
> [Fact→Coverage handoff 0.1合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)与
> [0.1实现冻结](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_FEASIBILITY_AUDIT`。

## 1. CONTROL LOOP 与qualified起点

文档319由PR #366从
`base=03b6d49a37a09f0d3cd2cdac4dca29454206e704 / head=02271650a83f099a58bd469d466d4c62c097f6c1 /
tree=7615e0d04059f766d103c87383989851b57b7852`受保护合入本审计基线。original Public CI
`39546108067`、exact-main Public CI `39548733536`与Browser Smoke `39548733661`均为attempt 1 SUCCESS，
分别为11/11、11/11与1/1。

fresh anonymous installed-product readback对README、doc318、doc319与milestones各保留一份唯一
`FORMAL_READBACK_PASS`。independent reconciliation与162-artifact finite closeout为：

```text
e4c080206842e189e31de01b900bd37c24c8149f9ab8aab5648855bd93407fb7
fd7c23e7665c42747a774decdf5efccc1f05eb4fe31056142876471e6312269e
```

因此起点状态是：

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

fresh CONTROL LOOP只审doc319重开的最小问题：能否在不修改0.1 bytes/history、不旁路one-shot claim、不复活已撤销
Provider执行权的条件下，把exact terminal Snapshot、total Policy scope与必要blob identity交给negative-world Coverage。

## 2. 判定问题与两个候选形状

本轮比较：

```text
A. live parent input accessor
   closure claim -> parent._inputs_ref()

B. terminal-validated original input carrier
   closure claim -> parent-owned terminal validation
                 -> same original DerivationInputSet object
                 -> successor-owned private binding
```

`DerivationInputSet`已经copy-own canonical Snapshot/Policy/Profile bytes与verified blob bytes，并且只提供document copy与不可变
identity字段。问题不是再复制一份相同字节，而是由谁证明下游拿到的是产生该Fact closure的原始对象，而不是调用者后来提交的
equal foreign object。

成功候选必须同时满足：

1. 覆盖`NORMAL_FULFILLED`与四个safe-negative Fact终态；
2. 逐项枚举exact Snapshot inventory与对其total、exactly-once的Policy scope decisions；
3. 保留原始`BudgetContext`、Fact attempt identity、one-shot竞争与late-stop撤销；
4. equal bytes/digests不继承original object binding；
5. 0.1 handoff的function、consumer、document bytes与public surface保持；
6. successor不取得Coverage status、manifest、Evidence、persistence或public publication authority。

## 3. 首个反例：live accessor不能覆盖required failure

审计attempt 1假设既有`parent._inputs_ref()`足以成为统一carrier。四个Python cell都在同一world否定该假设：required Fact
Provider non-success会正确撤销parent eligibility，但0.1仍允许把完整、safe-negative Fact history交给Coverage consumer。

因此：

```text
legal REQUIRED_PROVIDER_NON_SUCCESS handoff
    + parent eligibility REVOKED
    => parent._inputs_ref() rejects
```

该结果是`FEASIBILITY_DESIGN_COUNTEREXAMPLE`，不是环境、fixture或产品回归。四格原始失败、trace、脚本字节与汇总均保留；
后继PASS不把它重解释成未发生。它击穿的是“live parent accessor是五分支统一解”这个候选，不击穿0.1 handoff。

更关键的是，`_handoff_source_document()`已经为safe-negative分支独立执行完整terminal validation：

- parent/closure/input/context/classification/product/binding对象identity保持；
- `_input_state_seal`与五个input digests保持；
- exact inputs重新验证，Language classification与Fact qualification独立重算；
- terminal branch、Provider observations、responsibility与expected parent eligibility一致；
- context仍为原始RUNNING且无stop trigger。

它没有要求failed parent重新变回ADMITTED。由此可见，所需边界是terminal authority，不是被撤销的execution authority。

## 4. 可行的最小carrier

独立attempt 2选择：

```text
TERMINAL_VALIDATED_ORIGINAL_DERIVATION_INPUT_SET_REFERENCE
```

这不是调用者传入inputs，也不是在handoff之外按digest重建。可行的最小private seam是：

1. parent新增一个仅由closure调用的terminal exact-input handoff方法；
2. 该方法先执行现有`_handoff_source_document(closure)`完整验证；
3. 在同一同步调用内返回`source + original BudgetContext + parent-bound original DerivationInputSet`；
4. closure以新版本化purpose领取，但继续使用现有`__claimed`单一竞争槽；
5. successor carrier绑定`_inputs is _bound_inputs`、input seal、五个digest、context identity与token；
6. 每次private `_inputs_ref()`或document读取都重新检查context、input seal与source/input identity；
7. carrier只提供输入文档与blob identity，不暴露Parse/Provider执行、repository handle或eligibility mutation。

这里返回的原始`DerivationInputSet`本身已经是copy-owned immutable value。它在required-failure世界中不再代表live Provider
execution authority；其资格来自刚完成的terminal handoff validation与one-shot closure binding。不得从外部直接读取name-mangled
字段；审计proof facility的直接读取只证明现有对象确实存在，产品实现必须建立上述parent-owned方法。

## 5. 为什么不选择equal copy或扩写0.1

审计从original inputs构造了canonical bytes、五个digests与blob map完全相等的新`DerivationInputSet`。结果：

```text
semantic equality = true
object identity   = false
original binding = false
```

equal copy可以承载内容，但若由caller提供，它没有original object-graph authority。若在one-shot terminal method内部新建copy，仍需
新增source/input seal、constructor token与对象绑定；而现有original `DerivationInputSet`已经copy-owned并被parent seal覆盖，所以再复制
没有减少任何证明责任。

0.1也不能直接增加字段或private accessor：它的实现与consumer identity已经冻结。successor必须使用新的function/consumer identity，
同时复用closure-level one-shot slot；这样旧0.1 bytes、public `document_copy()`与历史测试无需改变。

## 6. 五终态与三分母world的机械结果

attempt 2在Python 3.10.6/3.13.13 × normal/`-O`四格得到相同canonical report：

```text
edcc90fdaba37646dc1065c24bb513f79ba2dac17741af0a4bdaef5ef8239a66
```

五个terminal worlds都保持原始inputs/context绑定：

| world | branch | FactSet | Snapshot / Policy | live parent accessor |
| --- | --- | --- | ---: | --- |
| normal | `NORMAL_FULFILLED` | present | `1 / 1` | available |
| unsupported-only | `ZERO_PARSE_DENOMINATOR` | null | `1 / 1` | available |
| syntax rejected | `ALL_PARSE_REJECTED` | null | `1 / 1` | available |
| projection blocked | `PROJECTION_BLOCKED` | null | `1 / 1` | available |
| required Provider failure | `REQUIRED_PROVIDER_NON_SUCCESS` | null | `1 / 1` | **revoked** |

额外三个`ZERO_PARSE_DENOMINATOR` worlds分别重建：

```text
empty inventory       = Snapshot 0 / Policy 0
unsupported-only      = Snapshot 1 / Policy 1
Policy-excluded-only  = Snapshot 1 / Policy 1
```

它们的Fact可见状态相同，但carrier从原始inputs恢复出的分母不同。另有直接falsifier证明：legacy 0.1领取后不能重放successor claim，
equal foreign inputs不被接受，context late stop使carrier失效。

## 7. feasibility判定与后继合同责任

结论是：

```text
BOUNDED_VERSIONED_FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_FEASIBLE
```

但“可行”不等于合同已冻结，更不等于runtime可以施工。后继合同必须明确冻结：

- 唯一versioned function与consumer identity；
- legacy-domain内的新claim purpose及与0.1/legacy continuation共享的one-shot竞争；
- terminal validation先于原始inputs引用交付；
- original object identity、input seal、五digest与exact bytes/blob map；
- required-failure时不复活parent eligibility或Provider execution；
- late stop、mutation、foreign equal input、duplicate claim与cross-world substitution fail closed；
- 0.1 bytes/API/history不变；
- authority ceiling停在private exact-input handoff，不产生Coverage结论。

具体class、method、field与异常类型仍是implementation non-decision。合同冻结、implementation authorization、implementation与
freeze publication必须各自拥有独立资格链。

## 8. 保留的反例与测试witness

read-only audit identity为：

```text
r1-fact-to-coverage-exact-input-successor-feasibility-audit/0.1
```

attempt 1四格一致失败，保留为
`AUDIT_ATTEMPT_1_LIVE_INPUT_REFERENCE_REQUIRED_PROVIDER_FAILURE_COUNTEREXAMPLE`。它证明live accessor候选不完备；没有修改产品、
fixture、预算、断言或oracle。

attempt 2只改变proof facility的候选carrier模型：从`parent._inputs_ref()`改为“现有terminal validation完成后由parent内部返回其
bound original inputs”。五终态、三分母world、产品调用与falsifiers不变，四格均PASS且report digest一致。

focused witness覆盖CoverageLedger 0.3、Language Support、Fact→Coverage 0.1、Fact→Relation transition与current composition。
最终四格均为`99/99 PASS`：

| Python | mode | result |
| --- | --- | --- |
| 3.10.6 | normal | `99/99 PASS` |
| 3.10.6 | `-O` | `99/99 PASS` |
| 3.13.13 | normal | `99/99 PASS` |
| 3.13.13 | `-O` | `99/99 PASS` |

测试只证明现有行为和本审计观察稳定，不授权successor实现。

## 9. 本candidate资格门与状态上限

tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。doc259–319、runtime、tests、workflows、
Schema、fixtures、CoverageLedger、composition、Evidence、Policy/Profile、persistence与public产品保持base bytes。

final bytes至少复核exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、unique headings、
状态markers、frozen hashes、`git diff --check`、read-only global/local hygiene与primary `audit.json` continuity。随后依次：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc319 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / frozen-history reconciliation
    -> qualified feasibility history
    -> return CONTROL LOOP
```

全部闭合以后，状态上限为：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合以前，上述`FEASIBILITY_AUDITED` target不生效。闭合以后必须返回CONTROL LOOP，从新exact main独立
建立最小successor contract；不得直接修改runtime、构造Coverage producer、实现manifest/Evidence、选择persistence或启动public
Review、post-R1 Benchmark与R2–R6。
