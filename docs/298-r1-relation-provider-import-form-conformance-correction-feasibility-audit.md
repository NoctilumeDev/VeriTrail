# R1 Relation Provider import-form conformance 修正可行性审计

> 状态：`AUDIT_CANDIDATE / NOT_QUALIFIED_HISTORY`。
>
> 本文只审计一个被施工前反例击穿的前提：current closed Relation Provider algorithms 是否能够在 application 已完整、
> 无损地构造 `IMPORT_DECLARATION` obligations 后执行 frozen import profile 的全部 obligation universe。本文不修改
> runtime、tests、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage 或 public Review 产品，
> 也不授权修正合同或实现。

## 1. CONTROL LOOP 与 exact source state

本审计绑定：

```text
repository  = NoctilumeDev/VeriTrail
exact main  = cd74cfd8d212d200465a86391d2fdb08c123376c
tree        = f474e014b890d2533e5283ddb97d0f2f29cc9ada
upstream PR = #342
```

PR #342 的授权发布已经完成自己的 original PR、protected merge、exact-main 双门、fresh
README/doc296/doc297/milestones readback 与 independent reconciliation。其 closeout 记录：

```text
correction implementation authority
    ALLOWED

correction implementation
    NOT_STARTED

old composition authority
    ALLOWED_HISTORY_PRESERVED / NOT_CONSUMABLE
```

该 closeout 有 200 项 artifact；independent reconciliation SHA-256 为
`9d59a160a3bdacb166b620f169568de2dbd51e843e56dd18eb7eea28759a4799`，closeout 自身 SHA-256 为
`9cdd52106ac942b96a16cf4b5df8d11e14bbf95eaba1d4353846b7d0001fe824`。

fresh implementation CONTROL LOOP 随后从相同 exact main 重读 Fact projection、Relation profile、current Provider source 与
doc296/doc297 的 stop conditions。在任何 product diff 产生以前，完整 import-form world 击穿了 doc296 §5、§7G 与 doc297
§3G 的复用前提，并直接命中 doc296 §9 / doc297 §5：

> 现有 Relation Provider algorithms 在合法 assignment 下仍不能处理完整 obligation universe。

因此 #342 已生效的 authority 继续作为历史事实保留，但当前不可消费；implementation 仍是 `NOT_STARTED`。

## 2. 真实反例

current Fact stage 对 Python source 递归遍历 AST，并为每个 import alias 产生一个 `IMPORT_DECLARATION` Fact。冻结语义包含：

```text
ast.Import
ast.ImportFrom
multiple aliases
relative imports
star imports
nested imports
multiple accepted products / paths
```

current closed Relation Provider 则只遍历 `tree.body`，只接受 `ast.Import`，并要求 `len(node.names) == 1`。因此以下 world
虽然拥有完整、合法的 FactSet 与完整 application-owned assignment，Provider 仍然拒绝：

```python
import a, b
from pkg import a, b
from . import local
from pkg import *

def f():
    import nested
```

fresh four-cell reproduction 使用默认完整 14-Fact world；其中 5 个 import Facts 包含 2 个 `IMPORT` 与 3 个
`FROM_IMPORT`。Provider A 的 5 个 obligations 与 Provider B 的 10 个 obligations 均被 current algorithms拒绝。

控制世界同时证明：

- 单一 top-level `import x` 继续完成；
- 两个 path、每 path 一个单一 `import` 的旧窄路径继续完成；
- `from x import y`、mixed five-kind world 与上述完整 forms 均拒绝。

这不是 Fact truth、FactSet identity、stage ownership、obligation projection、Relation candidate semantics 或 runtime环境失败。
它是 **Provider algorithm applicability / conformance boundary** 的真实反例。

## 3. 为什么不能继续消费旧授权

doc296 的 audit-only witness 证明了：在完整 five-kind single-path / two-path FactSet 中，现有 Provider algorithms可以处理被分配的
单一 `ast.Import` obligations。它没有证明算法覆盖所有 frozen `IMPORT_DECLARATION` forms。

因此：

```text
complete Fact-kind shape witness
    != complete IMPORT_DECLARATION semantic-universe witness

legal obligation assignment
    != Provider conformance for every assigned obligation
```

后继实现不能通过以下方式制造成功：

- 只为 `ast.Import` 构造 obligations；
- 从 expected universe 中删除 `ImportFrom`、额外 alias 或 nested imports；
- 把同一个 AST statement 的多个 alias 合并成一个 obligation；
- 只扫描 `tree.body`；
- 过滤或重算完整 FactSet；
- 修改 frozen Profile，使 unsupported forms 变成 out of scope；
- 在 current Provider identity 下静默扩大 algorithm；
- 让 Provider 的实际输出反向定义 denominator。

这些做法都会把实现能力不足改写成问题不存在。

## 4. 最小 reopen 边界

冻结的 Fact truth、doc290 `/0.1` per-product closure / obligation projection、doc294 `/0.2` stage ownership 与完整 Policy / FactSet
identity 均未被本反例击穿。需要重开的最小边界只有：

```text
Relation Provider import-form conformance
    + private algorithm identity/version
    + exact AST occurrence ↔ authoritative Fact binding
    + deterministic child ordinal compatibility
```

修正不能修改 application-owned denominator。Provider 仍只消费 application 明确分配的 obligations，不取得 applicability、
responsibility、qualification 或 admission authority。

## 5. bounded versioned successor 可行域

本审计构造了一个 audit-only successor witness。它不进入仓库 runtime，但证明以下有限算法能够在既有 authority ceiling 内工作。

### 5.1 recursive occurrence discovery

对每个 accepted product/path 的 exact source bytes，以 `feature_version=(3, 10)`限定 import grammar/AST 语义，并递归枚举所有
`ast.Import` / `ast.ImportFrom` alias occurrence。枚举对象是 alias occurrence，不是 statement 数量；未来合同仍须明确禁止
未受约束的 host parser behavior成为隐式authority。

### 5.2 bidirectional exact binding

每个 AST occurrence 必须与 authoritative `IMPORT_DECLARATION` Fact 按以下完整键双向匹配：

```text
path
byte_start / byte_end
import_form
module
level
name
alias
alias_ordinal
```

必须同时证明：

```text
every applicable Fact has exactly one AST occurrence
every AST import occurrence has exactly one authoritative Fact
```

missing、duplicate、foreign path/span、wrong alias ordinal、semantic drift、unmatched AST occurrence 或 unmatched Fact 一律停止。

### 5.3 complete assignment execution

successor 只为 application 已经机械生成并分配的完整 obligations 产生 Provider outcome/candidate；它不能自行选择 subset。
每个 assigned obligation 必须恰好产生一个 terminal outcome，candidate 仍由 existing canonicalizer 验证。

### 5.4 deterministic collision-free child ordinals

legacy Relation identity把 top-level single-alias `ast.Import` 的 `body_ordinal` 写入 child identity。successor 必须保持这些旧窄世界
的 exact bytes，同时为 extra alias、`ImportFrom` 与 nested occurrence 分配稳定且无冲突的 child ordinal。

本审计采用一个有界 witness：

1. top-level single-alias `ast.Import` 保留原 `body_ordinal`；
2. 其余 occurrence 按 path 内 lexical byte span、form 与 alias ordinal排序；
3. 从 `len(tree.body)` 开始分配扩展 ordinal；
4. multi-path identity继续包含 exact path，不允许跨 path交换 MODULE parent。

该 witness证明存在有限解，不提前把具体 Python class、field或最终 ordinal encoding 冻结为合同。

### 5.5 version boundary

algorithm semantic domain已经扩大，不能在 legacy Provider identity下静默替换。未来合同至少必须要求：

```text
legacy Provider algorithm / descriptor identity
    unchanged

private corrected Provider successor
    new versioned identity
```

旧窄世界的 candidate/outcome bytes必须逐字节保持；新 world只能由新 identity取得资格。

## 6. mechanical audit

audit root：

```text
C:\Users\lenovo\Desktop\GitHubProjects\tmp\relation-provider-import-form-conformance-feasibility-cd74cfd
```

覆盖七组规范 world：

| world | 关键性质 | legacy | audit-only successor |
| --- | --- | --- | --- |
| plain import | top-level、单 alias | `COMPLETED` | `COMPLETED`，bytes相同 |
| legacy ordinal | `pass` 后单一 import | `COMPLETED` | `COMPLETED`，bytes相同 |
| multi-alias import | 一个 statement、两个 alias | `REJECTED` | complete |
| multi-alias from-import | `ImportFrom`、两个 alias | `REJECTED` | complete |
| relative / star | relative 与 `*` | `REJECTED` | complete |
| nested imports | function/branch 内 import forms | `REJECTED` | complete |
| multi-path mixed | 多 path、多 form、多 alias | `REJECTED` | complete |

每个 world 同时验证：

- 完整 FactSet bytes/identity不被替换；
- Provider A/B 的 assigned count 与 terminal outcome count相等；
- missing、duplicate 与 semantic drift matcher worlds fail closed；
- legacy controls保持 exact candidate bytes。

Python 3.10.6 / 3.13.13 × normal / `-O` 四格均为：

```text
FEASIBLE_WITH_VERSIONED_PRIVATE_PROVIDER_SUCCESSOR
semantic report SHA-256
14f5eb624116f5712005e05322e08b734379fcb4891b02289553b4b44177e241
```

10项输入 artifact 的 closeout 为 `PASS_FEASIBLE_WITH_VERSIONED_PRIVATE_PROVIDER_SUCCESSOR`，SHA-256：

```text
2330d91d16d58f67fd852b4921910a4a91025900ef36f0cda28c94b121c100a3
```

## 7. retained failure 与归层

触发本审计的 upstream counterexample closeout SHA-256 为：

```text
291a2297da7d8c13aabc45a1bbafd01530fbaadb02bb897bc7cf41aab1aa42b1
```

其第一次 diagnostic 错把 Parse exact inputs从 Fact handoff consumer对象读取，形成
`DIAGNOSTIC_FIXTURE_SETUP_ERROR`；fresh attempt 2才进入 product algorithm。该 setup failure继续保留，不被后继四格反例或本审计
PASS覆盖。

本审计的结论是：

```text
current Provider conformance premise
    REFUTED

bounded versioned private Provider successor
    FEASIBLE AS AUDIT WITNESS

provider correction contract
    NOT_STARTED / NOT_AUTHORIZED
```

## 8. 后继合同至少必须冻结的语义

如果本候选最终取得资格，fresh CONTROL LOOP最多可以选择一份 docs-only Provider correction contract。该合同至少要冻结：

1. complete frozen `IMPORT_DECLARATION` form universe；
2. recursive alias-occurrence discovery；
3. authoritative Fact 与 AST occurrence 的双向 exact matching；
4. expected/assigned/terminal 三个集合的完整相等与 exactly-once；
5. legacy narrow-world byte compatibility；
6. deterministic、collision-free child identity规则；
7. new private algorithm/descriptor version 与 legacy immutability；
8. malformed、missing、duplicate、drift、foreign-path 与 unsupported runtime worlds的 fail-closed语义；
9. Provider authority ceiling与application-owned admission；
10. same-attempt BudgetContext、claim、terminal history与continuation约束。

这不是该合同本身，也不授权按上述列表施工。

## 9. 本审计不决定什么

本文不决定：

- 最终 class、module、field、protocol suffix或descriptor shape；
- public Provider SPI、Schema、manifest successor或persistence Route A/B；
- 其他 Relation families、module resolution、Python runtime behavior或跨语言语义；
- RelationSet admission以后如何恢复 ReviewSliceSet / Coverage composition A–J；
- public Review、R2 Evidence、R3 Attention、HumanDisposition或Core handoff；
- runtime/tests/fixtures何时获得施工权。

## 10. 当前裁决

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
    CANDIDATE
    NOT_QUALIFIED_HISTORY

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT
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

## 11. 本候选资格门与停止线

本候选只允许：

```text
README.md
AGENTS.md
docs/milestones.md
docs/298-r1-relation-provider-import-form-conformance-correction-feasibility-audit.md
```

最终字节必须通过本层声明的 local docs/link/hygiene gates、original PR Public CI、单独批准的 exact-head protected merge、
new exact-main Public CI与Browser Smoke、fresh installed-product README/doc298/milestones readback及independent reconciliation。

全部门闭合以后，最多形成：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDITED
```

随后必须返回 CONTROL LOOP。不得自动起草修正合同、修改 Provider/runtime/tests/Schema、恢复doc297 A–J或旧composition、选择
manifest/persistence、启动Coverage、public Review、R2/R3或post-R1 Benchmark。若候选资格过程中出现新的 semantic counterexample，
保留现场并只重开被击穿的最小边界。
