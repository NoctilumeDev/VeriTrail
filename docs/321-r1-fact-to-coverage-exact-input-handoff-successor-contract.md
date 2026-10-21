# R1 Fact → Coverage exact-input handoff successor 最小合同 0.2

日期：2026-10-21

> 候选状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是 qualified contract history；独立冻结发布闭合以前，本文不是 frozen contract。
>
> 合同基线：`main@b8a1ecd6e01d711f380d0774e7a6920aad005fc8`；tree
> `f58e3be4110885ab0760e4faa2d71ff3321e7dbf`。
>
> 上游：[negative-world Coverage authority recovery 审计](319-r1-negative-world-coverage-authority-recovery-audit.md)、
> [exact-input successor 私有实现可行性审计](320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)、
> [Fact → Coverage handoff 0.1 合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)与
> [0.1 私有实现冻结](264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / CONTRACT_ONLY`。本文只冻结 versioned private exact-input
> handoff 的 semantic identity、五终态、原始输入 authority、same-attempt one-shot 竞争、live BudgetContext 与 fail-closed
> 条件；不修改 runtime、tests、workflows、Schema、fixtures、Policy/Profile、CoverageLedger、composition、manifest、
> Evidence、persistence、publisher、CLI、Workbench、Core、public Review、Benchmark、R2–R6、tag 或 Release。

## 1. CONTROL LOOP 与 qualified upstream

文档 320 已由 PR #367 从：

```text
base = 9701b192b6b60499b70a5e429ecbbb83b1134b70
head = 89abdf0467aeaa4c2bf7f09e84790ba458976f7c
tree = f58e3be4110885ab0760e4faa2d71ff3321e7dbf
```

受保护合入本合同基线。original Public CI `39555193491`、exact-main Public CI `39558171201` 与 Browser Smoke
`39558171203` 均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1。fresh anonymous installed-product readback
对 README、doc319、doc320 与 milestones 各保留唯一 `FORMAL_READBACK_PASS`。independent reconciliation 与
166-artifact finite closeout 分别为：

```text
2959c0b5288abd97e15e00547a6845327f8ee64849e095831d33d0314877beb5
7d235b233a27878dfe8e6150a6eaf0d0485ccfe024b78e8cfcc4de621e96e9a0
```

因此 qualified 起点为：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

fresh CONTROL LOOP 未发现需要重开 Fact truth、0.1 handoff、CoverageLedger 0.3、composition 或 manifest 0.2 合同的
反例。最小合法问题是：在保留 0.1 bytes/history、单一 claim 槽和已撤销 Provider eligibility 的前提下，冻结一个能把
terminal-validated original `DerivationInputSet` 交给 future negative-world Coverage consumer 的 successor 合同。

## 2. 合同解决的问题

0.1 handoff 已经完整保存 Fact-stage terminal history、U/E/blockers、Provider observations、FactSet 或其精确 absence、
original `BudgetContext` 与 one-shot claim。但它不携带原始 `DerivationInputSet`，因此不能证明 future Coverage 使用的：

```text
Snapshot inventory
total Policy scope
canonical SourceSnapshot / ReviewPolicy / DerivationProfile bytes
verified blob bytes by object identity
five input digests
```

与产生该 Fact closure 的 original same-attempt object graph 是同一个输入世界。

digest 相等、canonical bytes 相等或 caller 重建的 `DerivationInputSet` 只能证明内容相等，不能继承 original binding。直接调用
live parent `_inputs_ref()` 也不是总解：`REQUIRED_PROVIDER_NON_SUCCESS` 会正确撤销 parent eligibility，而合法的 terminal
handoff 仍必须能够保留该 safe-negative world。

本合同冻结的箭头为：

```text
qualified terminal Fact closure
    -> parent-owned terminal revalidation
    -> original bound immutable DerivationInputSet reference
    -> original live BudgetContext
    -> versioned private exact-input carrier
```

端点各自成立不自动证明该箭头。本合同只定义候选实现与证据必须满足的有界验证条件；它不保证任何实现一定存在。

## 3. authority topology

| 主体 | 拥有 | 不拥有 |
| --- | --- | --- |
| original `DerivationInputSet` | 三份 canonical bytes、verified blob map、五 digest 与 copy-owned document views | attempt、claim、Coverage status |
| Fact parent / closure | original input binding、Fact terminal history、one-shot claim、terminal revalidation | Coverage denominator/disposition、manifest/Evidence |
| original `BudgetContext` | attempt deadline、RUNNING/stop latch 与 same-attempt budget identity | input contents、Coverage outcome |
| 本合同 application | successor identity、claim purpose、terminal validation order、carrier invariants与fail-closed判定 | 修改 Fact history、复活 Provider、定义 Coverage success |
| successor carrier | 已验证的 original inputs/context/source 的受限 private view | Provider/Parse执行、repository handle、eligibility mutation |
| future Coverage consumer | 在后继合同下消费 exact inputs 并独立构造 obligation/denominator 的候选权 | 从收到 carrier 推导 COMPLETE、manifest或Evidence authority |
| digest/content holder | 对应 semantic bytes | original object binding、same-attempt、one-shot或live authority |

caller、Provider、Schema、CoverageLedger、manifest、publisher 与 serialized projection 均不能自证 original input binding。future
Coverage consumer 必须独立取得自己的 denominator、item identity、disposition 与 completion qualification。

## 4. normative identities 与版本停止线

本合同冻结以下 semantic identities：

```text
contract function
    r1-fact-to-coverage-exact-input-handoff-successor/0.2

claim purpose
    FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2

private consumer
    r1-negative-world-coverage-exact-input-consumer/0.1

private carrier
    r1-terminal-validated-original-derivation-input-carrier/0.1

audited primitive shape
    TERMINAL_VALIDATED_ORIGINAL_DERIVATION_INPUT_SET_REFERENCE
```

这些名称冻结 semantic purpose，不预选 Python class、method、field 或 exception 名。任何实现都必须精确 dispatch；未知版本、
closest-version fallback、把 0.2 当 0.1、把 Relation handoff 当 Coverage successor 或只比较 suffix 的行为均 fail closed。

0.1 以下对象保持 immutable：

```text
r1-fact-to-coverage-handoff/0.1 semantic function
claim_fact_to_coverage_handoff consumer identity
0.1 source document bytes and public document_copy()
existing 0.1 tests, retained failures and qualification history
```

0.2 不在 0.1 document 中追加字段，不让旧 consumer 读取 original inputs，也不把后继成功回填为 0.1 已经拥有 exact-input
authority。

## 5. total terminal domain 与 denominator preservation

0.2 必须对以下五个已冻结 terminal branches total：

| branch | Fact-stage truth | exact-input责任 |
| --- | --- | --- |
| `NORMAL_FULFILLED` | complete U/E、FactSet、required fulfillment与optional gaps | 保留 original complete inputs |
| `ZERO_PARSE_DENOMINATOR` | Parse `0/0/0`、U/E空、无FactSet | 保留真实 Snapshot/Policy 分母，不能仅凭可见零值重建 |
| `ALL_PARSE_REJECTED` | non-zero Parse denominator、accepted=0、complete rejection history | 保留导致 rejected partition 的 original inputs |
| `PROJECTION_BLOCKED` | complete constructible U、representable E子集与全部blockers | 保留未被E/actual缩小的 input universe |
| `REQUIRED_PROVIDER_NON_SUCCESS` | complete U/E、全部applicable responsibility、真实child history、无FactSet | terminal handoff合法，但不得复活parent eligibility |

`interrupted / unsafe attempt` 不成为第六个可消费 branch。stop、release、incomplete reconciliation、非 terminal source 或无法独立
验证的 partial prefix 必须拒绝 0.2 claim。

三个 `ZERO_PARSE_DENOMINATOR` worlds 必须保持可区分：

```text
empty inventory       = Snapshot 0 / Policy 0
unsupported-only      = Snapshot 1 / Policy 1
Policy-excluded-only  = Snapshot 1 / Policy 1
```

它们的 Fact 可见结果可以同为 Parse `0/0/0`、Fact U/E `0/0` 与 FactSet absent；carrier 仍必须允许从 original inputs
无损恢复 inventory、Policy decisions 与 blob identity。不得用一个“空 Fact 结果”把三个分母 world 合并。

## 6. terminal validation 与 original input binding

成功 claim 的顺序固定为：

1. closure 在单一 one-shot 槽中原子领取 0.2 purpose；
2. parent 执行与 0.1 相同强度的完整 `_handoff_source_document(closure)` terminal revalidation；
3. revalidation 必须先于任何 input reference 交付；
4. 在同一同步调用内返回 validated source、original `BudgetContext` 与 parent-bound original `DerivationInputSet`；
5. successor carrier 记录并封存 source/input/context/object identities；
6. 每次 private document/blob/input view 都重新检查 carrier binding、input seal 与 live context。

normative original input identity 共同包含：

```text
exact DerivationInputSet object identity
source_snapshot_canonical_bytes
review_policy_canonical_bytes
derivation_profile_canonical_bytes
verified_blob_bytes_by_object_identity with exact keys and bytes
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
input_state_seal over all fields above
```

`DerivationInputSet.create(...)` 生成的 equal foreign object，即使每个 byte、key、digest 与 seal 都相等，也不是 original object。
carrier 只能接收 parent 在 terminal validation 内部返回的 bound reference；caller 不能提交、替换或建议 inputs。

required-provider-failure world 中，terminal validation只证明 terminal source与original inputs连续。它不得调用需要 live
eligibility 的 parent accessor，不得把 `REVOKED` 改回 `ADMITTED`，也不得重新执行 Parse/Provider。

## 7. one-shot、same-attempt 与 revocation

0.2 与下列既有路径共享 closure-level 单一 claim 槽：

```text
LEGACY_CONTINUATION
COVERAGE_HANDOFF                 # 0.1
RELATION_HANDOFF
FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2
```

任一路径先成功领取、验证失败或竞争失败以后，其他路径不得重放。新建 closure、复制 source document、重建等价 inputs、刷新
`BudgetContext` 或更换 consumer identity 均不能恢复已消费 authority。

claim 与 carrier 每次读取至少重新验证：

```text
original parent / closure / observations identity
original Fact attempt and exact terminal branch
original DerivationInputSet identity and input_state_seal
original BudgetContext object, limits, start/deadline and RUNNING state
absence of stop trigger and successful checkpoint
source document bytes and terminal history continuity
0.2 function / purpose / consumer / carrier identity
```

late stop、deadline exhaustion、input mutation、source mutation、foreign observation、duplicate claim、cross-attempt substitution 或
context replacement 都使 carrier 永久 fail closed。已复制给 consumer 的 semantic document 不能变成 detached replay authority。

## 8. carrier capability ceiling

0.2 carrier 只允许 future bounded application consumer：

- 获取 copy-owned SourceSnapshot、ReviewPolicy 与 DerivationProfile document；
- 枚举 exact verified blob object identities 并取得 copy-owned bytes；
- 读取五个 frozen digests；
- 读取 0.1 handoff 的 validated Fact terminal source copy；
- 证明这些值来自同一 original input/context/closure object graph。

carrier 不得暴露：

```text
mutable repository handle or lazy loader
Parse / Provider execution or retry
parent eligibility mutation
Fact history mutation
Coverage item/disposition/status authority
ReviewSliceSet / CoverageLedger construction authority
manifest / Evidence / Bundle / persistence / publisher authority
public API, Schema, CLI or Workbench surface
```

收到 exact inputs 只证明输入连续性。它不证明 Coverage obligation universe 完整、每项已履责、Coverage status 可以确定、manifest
0.2 可发布或 same-attempt Evidence 已形成。

## 9. qualification semantics：soundness优先，UNKNOWN合法

给定 frozen world `W`、0.2 candidate `C` 与证据 `π`：

```text
Verify_0.2(W, C, π) = ACCEPT
    => C binds the terminal Fact source, original inputs and live context
       under the exact one-shot contract above
```

本合同不要求所有实际合法构造都能被当前 verifier 接受：

```text
Qualified_0.2(W, C)
    !=> current verifier can always construct or accept C
```

测试过的所有实现失败，只能得到 `UNKNOWN / NO_QUALIFIED_CONSTRUCTION_OBSERVED`。只有对已声明的有界候选空间给出机械穷尽与
不可满足证明，才允许写 `UNSAT_WITHIN_DECLARED_BOUND`；不得由若干失败候选推出数学意义上的算法不存在。

失败分类不得混合：contract violation、product defect、test/proof-facility failure、environment/network failure 与 unknown root
必须保留原身份。后继 PASS 不覆盖先前 FAIL/ERROR/CANCELLED/UNKNOWN。

## 10. normative falsifier matrix

| ID | 必须拒绝或保持的反例 | 被禁止的错误推论 |
| --- | --- | --- |
| `FCXI-000` | caller提交equal foreign `DerivationInputSet` | 相同bytes/digests继承original binding |
| `FCXI-001` | required-provider-failure后调用live parent `_inputs_ref()` | terminal authority复活execution eligibility |
| `FCXI-002` | terminal validation以前交付inputs | 后置检查可以补回泄漏的authority |
| `FCXI-003` | legacy continuation先领取，再领0.2 | 不同purpose拥有独立claim槽 |
| `FCXI-004` | 0.1 Coverage handoff先领取，再领0.2 | successor可重放旧source |
| `FCXI-005` | Relation handoff先领取，再领0.2 | stage不同即可重复消费 |
| `FCXI-006` | 0.2先领取，再领任一旧路径 | successor不占用全局one-shot |
| `FCXI-007` | claim后触发stop/deadline，再读取carrier | 已领取即可忽略live context |
| `FCXI-008` | 替换input bytes、blob key/value、任一digest或seal | 局部一致足以代表完整input identity |
| `FCXI-009` | fresh equal-limits `BudgetContext` | 等价预算继承same-attempt authority |
| `FCXI-010` | foreign closure/observation/parent或cross-attempt source | semantic equality继承object graph |
| `FCXI-011` | Snapshot/Policy行缺失、重复、额外或跨path混入 | downstream可以自行修剪denominator |
| `FCXI-012` | verified blob缺失、额外、key交换或bytes mismatch | digest holder拥有blob membership authority |
| `FCXI-013` | 五terminal branch任一无法形成0.2 input | normal world代表total domain |
| `FCXI-014` | 三个zero-Parse denominator worlds被合并 | 相同Fact可见结果证明相同input universe |
| `FCXI-015` | interrupted/unsafe partial source被包装成terminal carrier | fail-closed可由placeholder恢复 |
| `FCXI-016` | unknown/closest version被接受 | version fallback保持semantic identity |
| `FCXI-017` | 0.2修改0.1 source bytes/API/test expectation | successor资格回写legacy合同 |
| `FCXI-018` | carrier直接产生Coverage COMPLETE/PARTIAL/UNKNOWN | input continuity等于Coverage qualification |
| `FCXI-019` | public export/default composition发生变化 | private contract自动授权public surface |

positive denominator必须独立覆盖五terminal branches、三个zero-Parse worlds、全部原始input字段与one-shot竞争；expected results
不得只由被测实现自身生成。falsifier只是合同 witness，不能自行授予implementation或freeze authority。

## 11. implementation non-decisions 与后继停止线

本文不决定：

- Python class、method、field、token、lock 或 exception 的具体名称；
- carrier 是否由独立 module 或现有 private module 承载；
- Coverage obligation、item、disposition、status 或 ledger producer；
- negative-world manifest 0.2 producer；
- same-attempt DerivationEvidence carrier；
- persistence Route A/B、public Schema、publisher 或产品 UI；
- Benchmark、Attention、R2–R6 的实现次序。

implementation feasibility、authorization、implementation candidate 与 freeze publication必须分别进入CONTROL LOOP和自己的完整
资格链。合同不能由测试绿灯、代码存在或 doc320 的可行性结论自动冻结。

## 12. 本candidate资格门与状态上限

tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。doc259–320、runtime、tests、workflows、
Schema、fixtures、Policy/Profile、CoverageLedger、composition、manifest、Evidence、persistence与public产品保持base bytes。

final bytes至少复核：

```text
exact four-file scope
relative links
UTF-8 without BOM
LF and final LF
balanced fences and unique headings
state markers and exact upstream identities
legacy 0.1 / frozen history byte continuity
git diff --check
read-only global/local hygiene
primary audit.json SHA-256 continuity
```

随后依次闭合：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc320 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / history reconciliation
    -> finite closeout
    -> qualified contract candidate / NOT_FROZEN
    -> return CONTROL LOOP
```

全部闭合后状态上限为：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的完整资格链闭合以前，上述 qualified target 不生效。即使闭合，合同仍为 `NOT_FROZEN`；必须从新 exact main
建立独立 docs-only freeze publication并完成其全部资格门。不得从本candidate直接修改runtime、创建Coverage producer、实现
manifest/Evidence、选择persistence或启动public Review、post-R1 Benchmark与R2–R6。
