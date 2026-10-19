# R1 Relation Provider import-form conformance 修正最小合同 0.1

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_CANDIDATE`。
>
> 基线：`main@85bb22896b978b6f9480b58681c69c5b5ac10c55`；tree
> `95d84a0e95388b23dc9e9a1cd9447be5d12ef7db`。
>
> 上游：[Fact handoff → Relation exact-input interoperability correction 合同](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)、
> [stage applicability capability identity 修正合同](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)、
> [corrected successor 私有实现可行性审计](296-r1-fact-relation-corrected-successor-private-implementation-feasibility-audit.md)、
> [实现授权发布](297-r1-fact-relation-corrected-successor-private-implementation-authorization-publication.md)与
> [Provider import-form conformance 修正可行性审计](298-r1-relation-provider-import-form-conformance-correction-feasibility-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结 versioned private Relation Provider 对完整
> `IMPORT_DECLARATION` form universe 的 conformance、AST occurrence 与 authoritative Fact 的双向 exact binding、
> complete assignment execution、legacy byte compatibility 与 fail-closed 语义；不创建或修改 runtime、tests、fixtures、Schema、
> Profile、Policy、manifest、persistence、Coverage、public Review、Evidence、Bundle、publisher、CLI、Workbench、Core、R2、R3、
> tag 或 Release。

## 1. CONTROL LOOP 与 qualified upstream

文档 298 已由 PR #343 final head `51ca59a5ad1bacc63c9f10aaa4bbad8f16fe1962` 合入本基线。original Public CI
`39279104121`、exact-main Public CI `39286685392` 与 Browser Smoke `39286685584` 均为 attempt 1 SUCCESS，分别为
11/11、11/11 与 1/1。fresh README/doc298/milestones 各有 qualifying PASS；setup1 选择了存在于 source、却未进入 public
stable render window 的 README marker，正式 README observation 因 marker drift 保留为
`FORMAL_READBACK_MARKER_SELECTION_SETUP_ERROR`。setup2 在任何正式 observation 前改用已证明公开可见的 marker；doc298
formal #1 随后因 anonymous API rate exhaustion 保留为 `FORMAL_READBACK_ERROR`，fresh identity #2 才取得 PASS。

independent reconciliation 与 142-artifact closeout 分别为：

```text
58552b25d98294099608e177b7f7e750c1862874393ee9533652ebe6df5e7bb3
f0ff0d0166127aca487a782fc589b00447eb7490cee95f647f6438e1d3bed736
```

因此文档 298 已成为 qualified history。重新绑定 exact main、当前 Provider source、doc175/290/294/296/297 与所有保留反例后，
没有发现需要重开 Fact truth、Relation profile、application-owned obligation projection、candidate semantics、Policy/Profile、Schema、
manifest 或 persistence 的更早 seam。当前最小合法问题是本 semantic contract。

## 2. 本合同解决的问题

冻结的 application semantics 已经能够从完整 authoritative FactSet 机械构造完整 Relation obligation universe，并把每个 obligation
分配给 frozen profile 指定的 Provider。current Provider algorithms 却只处理 top-level、single-alias `ast.Import`：

```text
complete assigned obligations
    include Import / ImportFrom
    include multiple aliases
    include relative / star
    include nested imports
    include multiple paths

current Provider execution
    scans tree.body only
    accepts ast.Import only
    requires len(node.names) == 1
```

因此：

```text
legal assignment
    != Provider conformance

Provider conformance failure
    != permission to shrink assignment
```

本文冻结的修正是一个新的 private Provider algorithm/descriptor semantic identity。它必须在完整 exact world 中执行 application 已经
分配的 obligations，并证明 source occurrence、authoritative Fact、assigned obligation、terminal outcome 与 candidate 之间不存在遗漏、
重复或跨 world 拼接。它不能过滤 FactSet、改变 Profile、重算 denominator 或恢复旧 live authority。

## 3. authority owner 与边界

| 主体 | 拥有 | 不拥有 |
| --- | --- | --- |
| frozen Policy/Profile | relation families、eligible subject role、Provider responsibility、requiredness 与 immutable identity | Provider 执行结果、live claim |
| complete Fact handoff | authoritative FactSet、Fact provenance、accepted products、same-attempt terminal history | Relation applicability、Provider conformance |
| application | stage applicability、per-product closure、完整 obligation universe、assignment、qualification 与 admission | 修改 Fact truth、伪造 Provider outcome |
| corrected Provider successor | assigned obligation 的 bounded source observation、terminal outcome 与 candidate | 选择 denominator、删减 assignment、签发 qualification/admission |
| parser/conformance mechanism | 对 exact source 的 versioned occurrence projection | Fact identity、Policy authority、live continuation |
| digest/content holder | 对应 immutable bytes | attempt、BudgetContext、claim、ProviderRun、qualification 或 continuation |

Provider 不能因为无法表示某种 import form，就将其重新分类为 non-applicable、missing input、optional 或 out of scope。application 也不能
根据 Provider 实际输出反向构造 expected universe。

## 4. normative identities 与完整输入

本合同冻结以下 semantic function identities：

```text
contract function
    r1-relation-provider-import-form-conformance-correction/0.1

import occurrence projection
    r1-python-3.10.6-import-alias-occurrence-projection/0.1

occurrence-to-fact binding
    r1-relation-import-occurrence-fact-binding/0.1

provider assignment execution
    r1-relation-import-assignment-execution/0.1

child ordinal projection
    r1-relation-import-child-ordinal/0.1
```

它们冻结 semantic function，不预先决定 Python class、field、module 或 public Schema。corrected Provider 必须有新的、可区分的
private algorithm/descriptor/run identity；legacy `closed-python-import-observation / 0.1-test` 与既有 request/operands identities 保持
immutable，不能 closest-version fallback 或静默接受 successor bytes。

每个 Provider run 的 exact immutable input 至少同时绑定：

```text
source snapshot / derivation input identity
exact source bytes for every assigned product/path
complete authoritative FactSet bytes and digest
complete stage applicability / per-product closure / obligation projection
frozen Policy/Profile bytes, identities and digests
application-owned Provider assignment
attempt / BudgetContext / deadline / stop-revocation state
Provider algorithm/descriptor identity
```

只传 path、Fact IDs、digest、selected facts 或从 ambient filesystem 重新取得 source，均不构成完整输入。

## 5. complete import-form universe 与 versioned parser semantics

current frozen `IMPORT_DECLARATION` semantic universe 至少包括：

```text
ast.Import
ast.ImportFrom
one or more aliases per statement
absolute imports
relative imports
star imports
imports nested in functions, classes, branches and other legal statement bodies
multiple accepted products / paths
```

规范枚举单位是 **alias occurrence**，不是 statement 数量。一个含两个 aliases 的 statement 产生两个可独立绑定的 occurrences；
不同 lexical scopes 不改变其属于 source product/path 的身份。

语法与 AST 坐标语义绑定 CPython 3.10.6。实现可以使用 exact 3.10.6 runtime，或使用已经独立取得 conformance 资格的等价机制；
宿主解释器的 `ast.parse(..., feature_version=(3, 10))` 只能是候选机制，不能仅凭该参数取得 3.10.6 conformance authority。
host 3.13、normal 与 `-O` 必须对合同声明的 semantic projection 产生相同 canonical 结果；任何 parser/coordinate/encoding drift 必须
fail closed，而不是选择宿主输出作为新事实。

source bytes 必须来自已经资格化的 exact input。Provider 不重新取得 Language Support 或 Parse authority；它只在上游已授权的
source world 中复算本合同所需的 import occurrence projection。

## 6. AST occurrence ↔ authoritative Fact 双向 exact binding

对每个 accepted product/path，application 与 corrected Provider 必须证明 source occurrence 集合 `X` 与 assigned applicable
`IMPORT_DECLARATION` Fact 集合 `F_R` 之间存在双向、一一对应的 exact binding。匹配键至少语义绑定：

```text
accepted product identity
exact git path bytes
source byte start / end
import_form
relative_level
module_parts
imported_name
alias_name
alias/local ordinal within the statement
```

必须同时成立：

```text
for every f in F_R:
    count(matching occurrence in X) == 1

for every x in X:
    count(matching authoritative Fact in F_R) == 1
```

只证明 emitted occurrence 都能找到 Fact 不足以证明完整性；只证明 Fact 都找到 occurrence 也不能排除 source 中未进入 Fact truth 的额外
occurrence。missing、duplicate、foreign product/path/span、wrong alias ordinal、semantic drift、unmatched occurrence 或 unmatched Fact
一律停止。匹配不能修改 Fact bytes/digest，也不能把 occurrence projection 冒充新的 FactSet。

## 7. complete assignment execution 与 terminal composition

设 application 分配给 Provider `p` 的完整 responsibility 为 `A_p`。Provider 必须只消费该 immutable assignment，并产生完整
terminal outcome set `T_p`：

```text
A_p = expected obligations assigned to p

count(outcome for obligation a) == 1
    for every a in A_p

outcome_obligations(T_p) - A_p = empty
A_p - outcome_obligations(T_p) = empty
```

每个 successful candidate 继续使用 frozen canonical relation semantics 验证；candidate 本身不替代 terminal outcome。一个 obligation
产生零个、多个、foreign-attempt 或 foreign-Provider terminal，Provider 只返回部分结果，或 candidate/outcome identity 不一致，均不能
取得 complete execution。

application 仍独立重算 expected assignment、核对 terminal partition、执行 qualification 与 admission。Provider `COMPLETED`、进程退出
成功、candidate 数量正确或某一 relation family 成功，都不能自行证明全部责任已经履行。

## 8. deterministic child ordinal 与 legacy compatibility

legacy Relation subject identity把 top-level、single-alias `ast.Import` 的 `body_ordinal` 写入 child identity。successor 必须同时满足：

1. legacy narrow world 中，该 occurrence 继续使用原 `body_ordinal`；
2. legacy candidate/outcome 的 canonical semantic bytes 逐字节相同；
3. additional aliases、`ImportFrom` 与 nested occurrences 使用独立 extension ordinal space；
4. extension occurrences 按同一路径内的 lexical byte span、import form、alias ordinal 与 canonical semantic tie-break 排序；
5. extension ordinals 从 `len(tree.body)` 开始，因此不与 legacy top-level body ordinals 冲突；
6. 若完整排序键仍不能唯一标识 occurrence，必须拒绝，不能依赖遍历偶然顺序；
7. full identity 始终绑定 accepted product 与 exact path，不同 path 可重用 ordinal，不能互换 MODULE parent 或 child identity。

本文冻结 ordinal 的语义性质与 compatibility，不冻结某个 Python helper 名称或 carrier field。任何未来不同编码必须以新 identity证明同一
性质，不能改变 legacy bytes。

## 9. fail-closed reason ownership

至少下列世界必须在 Provider/conformance stage fail closed：

- exact input 缺失、损坏、digest/path/product/attempt 不一致；
- parser、decoder、AST coordinate 或 3.10.6 conformance 不能建立；
- authoritative Fact 与 occurrence 的 missing、duplicate、extra 或 semantic drift；
- assignment 漏项、重复、包含 foreign obligation，或 Provider 输出 assignment 外结果；
- terminal outcome 缺失、重复、foreign ProviderRun/attempt 或 candidate identity 不一致；
- ordinal 冲突、legacy byte drift 或 cross-path/cross-product parent exchange；
- deadline、budget、stop/revocation 或 worker lifecycle 未安全闭合。

这些失败不改写 Fact truth，不把合法上游 Fact 降格为 malformed，也不由 Provider解释成 application admission。Provider stage 只拥有其
bounded execution reason；application qualification/admission 与 cross-Provider reconciliation 继续由各自 frozen owner裁决。

一个 required Provider 的 failure 不能被另一个 Provider 的 success 抵消。完整组合必须证明每个 required assignment 恰有一个合法
terminal；optional/required/shared-safety语义继续按 frozen Profile 保留，不因 expanded import support而改变。

## 10. same-attempt lifecycle 与 authority ceiling

corrected successor 必须在 doc290/294/297 已限定的同一 composition attempt 中运行：

```text
revalidate exact immutable inputs
    -> consume existing one-shot Fact handoff claim
    -> construct complete application-owned assignments
    -> execute new versioned Provider successor
    -> reconcile exact terminal history
    -> application qualification / admission
```

semantic bytes、equal digest、same limits 或 identical candidate output 都不能复用另一个 attempt 的 claim、BudgetContext、ProviderRun、
terminal history、admission 或 continuation。失败、revoked 或已消费的 live authority不能从缓存恢复。

本合同最多定义 Provider conformance 修正。即使后继实现全部通过，也不自动：

- 恢复 doc297 或旧 composition A–J 的施工权；
- 创建/admit RelationSet、ReviewSliceSet 或 CoverageLedger；
- 选择 manifest successor、persistence Route A/B、public Schema/carrier；
- 启动 public Review、R2、R3 或 post-R1 Benchmark。

这些必须在本合同冻结、后继 feasibility 与独立授权以后，由 fresh CONTROL LOOP重新判断。

## 11. normative falsifier obligations

后继 feasibility 与实现至少必须直接攻击下列 worlds：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `RPIF-000` | top-level single-alias plain import | successor改变legacy candidate/outcome bytes或body ordinal |
| `RPIF-001` | `pass` 后的legacy import | 用compact reindex替换原body ordinal |
| `RPIF-002` | `import a, b` | statement只产生一个alias obligation/outcome |
| `RPIF-003` | `from pkg import a, b` | 只匹配第一个alias或把module/name语义合并 |
| `RPIF-004` | relative与star import | 丢失relative level、module或imported name |
| `RPIF-005` | function/class/branch内nested import | 只扫描`tree.body`仍宣称complete |
| `RPIF-006` | 多path mixed forms | 跨path交换MODULE、Fact或ordinal仍通过 |
| `RPIF-007` | authoritative Fact missing | unmatched source occurrence被忽略 |
| `RPIF-008` | extra/duplicate authoritative Fact | 多个Fact绑定同一occurrence仍通过 |
| `RPIF-009` | span、form、module、name、alias或ordinal单字段漂移 | approximate matching仍通过 |
| `RPIF-010` | assignment漏掉一个eligible obligation | Provider实际输出反向缩小denominator |
| `RPIF-011` | assignment重复或含foreign obligation | terminal count看似相等即complete |
| `RPIF-012` | terminal missing/duplicate/foreign attempt | process COMPLETED即履责 |
| `RPIF-013` | host parser与3.10.6 projection漂移 | 选择宿主结果作为authority |
| `RPIF-014` | extension ordinal排序键碰撞 | 依赖遍历偶然顺序生成identity |
| `RPIF-015` | identical bytes/digest、different attempt | 恢复live claim或continuation |

规范矩阵必须在 Python 3.10 / 3.13 × normal / `-O` 比较 canonical semantic report。矩阵相等只是 witness；合同完整性、版本边界与
authority仍由本文及上游 frozen truth拥有。

## 12. 本合同不决定什么

本文不决定：

- 最终 Python class、module、field、protocol suffix、descriptor shape或worker topology；
- public Provider SPI、Schema、manifest successor或persistence Route A/B；
- 新的 Relation family、module resolution、cross-file symbol resolution或跨语言语义；
- RelationSet admission以后如何恢复 ReviewSliceSet / Coverage composition；
- public Review、R2 Evidence、R3 Attention、HumanDisposition或Core handoff；
- runtime/tests/fixtures何时取得施工权。

如果后继 feasibility 证明 bounded private successor无法在本合同内构造，必须保留 `UNKNOWN / NO_QUALIFIED_CONSTRUCTION`，或对本文
明确且完整的候选空间给出机械 UNSAT 证明；有限测试失败不能冒充“算法不存在”。

## 13. 当前裁决、资格门与停止线

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT
    FROZEN

R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY
    ALLOWED_HISTORY_PRESERVED
    STOP_CONDITION_TRIGGERED
    NOT_CONSUMABLE

R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION
    NOT_STARTED

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDIT
    AUDITED
    QUALIFIED_HISTORY

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT
    CANDIDATE
    NOT_FROZEN

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR
    NOT_STARTED
    NOT_AUTHORIZED

R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION
    STOP_CONDITION_TRIGGERED

R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR
    NOT_SELECTED

R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE
    OPEN

R1_PUBLIC_REVIEW_PRODUCT / R2 / R3
    NOT_STARTED
```

本候选只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/299-r1-relation-provider-import-form-conformance-correction-contract.md
```

最终字节必须通过本层声明的 local Markdown/link/hygiene/focused regression gates、original PR Public CI、受保护 exact-head merge、
new exact-main Public CI与Browser Smoke、fresh installed-product README/doc299/milestones readback及independent reconciliation。

全部门闭合以后，最多形成：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
```

`CONTRACT_CANDIDATE`不自动变成`FROZEN`。必须保留本文已资格化字节并进行独立 docs-only freeze publication；该 publication 自己的
original/exact-main gates、fresh product readback与independent reconciliation全部闭合以后，`FROZEN`才生效。随后必须返回
CONTROL LOOP，重新审计 private successor feasibility；不得自动修改 Provider/runtime/tests/Schema、恢复旧授权或 composition、选择
manifest/persistence、启动 Coverage、public Review、R2/R3或post-R1 Benchmark。
