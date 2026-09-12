# R1 SourceSnapshot 后继最小闭环审计

> 状态：`R1_DERIVATION_INPUT_PRECONTRACT_AUDITED /
> R1_DERIVATION_INPUT_CONTRACT_NOT_STARTED /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@b1a58143ae2fd359b885a575587aa4682aef8a04`
>
> 上游冻结事实：[R1 SourceSnapshot 最小运行切片冻结发布](130-r1-source-snapshot-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L0_DOCUMENTATION`；本文件不修改 Schema/corpus、SourceSnapshot
> runtime、Core、P/Q、CI 或发布坐标，也不创建 parser、Fact、Relation、Slice、Coverage、Manifest、CLI
> 或 Provider 实现

## 1. 审计问题

SourceSnapshot 已经能够从 exact Git object 建立完整 inventory、拥有源码 blob bytes，并单独发布一个
规范 `source-snapshot.json`。这只关闭了源码世界的身份与获取边界，没有自动回答后继派生应从哪里开始。

本轮不问“怎样尽快生成 Relation Graph”，只问：

> SourceSnapshot 之后，哪个最小边界既是后继派生不可缺少的前提，又能在不借用 Relation、Slice、
> Coverage 或完整 Derivation 的情况下独立验证？

审计输入包括文档 113、120、127–130，十个已冻结 R1 Schema、兼容 corpus、SourceSnapshot runtime 与
测试。任何候选边界必须继续满足：

```text
Artifact identity != path identity
Verified bytes == bytes later consumed
Schema-valid != R1-conformant
Input binding != semantic derivation
```

## 2. 发现的合同接缝

### 2.1 `FactSet` 还不是合法的独立发布闭环

每个 Fact 的 `provenance_refs[]` 必须引用同一交付闭环中的 `DerivationEvidence.provider_run_id`。但是冻结的
`R1_DERIVATION` Manifest 只有两种合法形态：

```text
COMPLETE
  -> Snapshot + Policy + Profile + Evidence + Fact + Relation + Slice + Coverage

DIAGNOSTIC
  -> Snapshot + Policy + Profile + Evidence
```

它没有 `FACT_ONLY`、五文件成功态或任意 partial file set。因而下一步若直接发布 FactSet，只能在以下错误
方案中选择：

1. 让 Fact 的 provenance 指向不存在的 Evidence；
2. 伪造 Relation/Slice/Coverage 占位文件；
3. 为实现便利增加第三种 Manifest outcome；
4. 发布无 Manifest 的多文件集合，却把它称为完整 Bundle。

四种方案都会改写已冻结语义。结论是：

```text
Fact mapping can be planned next
!=
FactSet publication is already authorized
```

### 2.2 独立 Snapshot Artifact 不携带源码正文

`source-snapshot.json` 保存 inventory、Git object identity、SHA-256 与 size，不复制 blob body。当前
`OwnedSourceSnapshot` 在同一进程内保留已核验 blob bytes；进程结束以后，单文件 Artifact 自身不足以让
parser 获得源码正文。

后继只能：

1. 消费同一 acquisition 已拥有的 bytes；或
2. 从 Snapshot 记录的 exact Git object OID 重新取得 bytes，并同时复核 object OID、SHA-256、size 与
   Snapshot canonical identity。

它不能读取 worktree path，也不能把重新生成的一份“语义上应该相同”的 Snapshot 替换已发布 Artifact。
因此 SourceSnapshot 与 parser 之间仍缺少一个明确的 owned-input continuity boundary。

### 2.3 三类输入不能共享权威

后继派生至少依赖：

```text
SourceSnapshot
  -> 已观察并冻结的源码世界

DerivationProfile
  -> 版本化 Python 3.10 语义、词汇与规范规则

ReviewPolicy
  -> Human Seal authority 选择的 scope、Provider requirement、module mapping、slice policy 与执行预算
```

Profile 不能由 Provider 自报，Policy 不能从 Snapshot 文件名或仓库布局推测，Snapshot 也不能被 Policy
重写。路径只定位输入；通过规范字节、语义摘要和交叉引用验证以后形成的 owned values 才能进入后继派生。

### 2.4 Policy 自带的预算不能负责安全读取它自己

`ReviewPolicy.execution_budget` 在 Policy 完整读取、规范验证和 Seal 复算之后才可信。实现不能先无限读取
Policy，再声称读取过程由该 Policy 内的 budget 保护；也不能为每个后继阶段重新刷新一次完整预算。

这要求区分：

```text
trusted derivation-input acquisition safety profile
  -> 保护三个输入文件与本地 Git object reacquisition
  -> 不进入任何语义 Artifact identity

sealed ReviewPolicy.execution_budget
  -> 在 owned input tuple 成立后约束后继 derivation
  -> 后继所有阶段共同消费一个绝对 budget
```

前者只决定本次绑定尝试能否存在，不能改变输入语义。后者的精确开始点与跨阶段 deadline ownership 留给
完整 derivation runtime 合同；本轮不得提前实现或刷新它。

### 2.5 Schema 不能证明跨 Artifact 一致性

当前 JSON Schema 能检查局部 shape，却不能独立证明：

- Policy 的 `source_snapshot_digest` 是否等于实际 imported Snapshot；
- Policy 的 `derivation_profile_digest` 是否等于实际 imported Profile；
- `scope_decisions` 是否与 Snapshot terminal inventory 构成精确一一对应；
- `python_module_mapping.module_root` 是否等于或位于 analysis root 内；
- Profile 与 Policy 的数组是否满足冻结 rank、唯一性和规范摘要投影；
- Policy Seal 是否覆盖经过复算的三个摘要；
- reacquired Git bytes 是否正是 Snapshot inventory 已绑定的内容。

这些属于 runtime conformance，不得用“通过 Draft 2020-12 Schema”替代。

### 2.6 输入绑定不能解释后继语义

完整 ReviewPolicy 已经包含 `slice_policy`，DerivationProfile 也包含 relation/traversal 规则。输入绑定必须
验证并保留这些规范字段，但不能因为看到了它们就开始：

```text
select anchors
parse Python
map Facts
resolve imports
compose Providers
propagate conflicts / UNKNOWN
generate Slices or Coverage
```

验证一个被封存的值，不等于获得执行该值所描述能力的权力。

## 3. 候选边界比较

| 候选 | 是否闭环 | 裁决 |
| --- | --- | --- |
| 直接实现 FactSet | provenance 与合法发布集合未闭合 | 拒绝 |
| 直接实现 Relation/Slice/Coverage | 上游 Fact/Evidence 尚不存在 | 拒绝 |
| 提前实现完整 Derivation | 一次跨越所有高风险接缝 | 拒绝 |
| 只实现 ReviewPolicy authoring | 会把 Human Seal 流程混入 runtime | 拒绝 |
| 冻结 Derivation Input Binding | 能独立证明输入身份、连续性与交叉引用，不产生下游语义 | 选择 |

## 4. 选定的下一个最小合同闭环

后继合同只定义：

```text
published source-snapshot.json
        +
canonical sealed review-policy.json
        +
canonical derivation-profile.json
        +
exact local Git object database
        ↓
one bounded read / independent validation per Artifact
        ↓
cross-Artifact digest, Seal, scope and module-root conformance
        ↓
exact Git object reacquisition and byte verification
        ↓
one owned DerivationInputSet value
```

`DerivationInputSet` 只是运行时拥有关系，不是新的公共 Artifact，不获得新的 semantic digest，也不发布
`manifest.json`。它的职责是保证：

```text
verified Snapshot / Policy / Profile bytes
and verified source blob bytes
are the same bytes later handed to a derivation consumer
```

本边界不产出 FactSet 或 DerivationEvidence，因此不会制造 dangling provenance，也不会提前占用完整
Derivation Bundle 的文件布局。

## 5. 后继合同必须回答的问题

1. 三份输入文件的读取上限、总预算与一个绝对 acquisition deadline；
2. ordinary file、symlink/reparse point、替换竞争和读取后路径漂移的处理；
3. canonical bytes、Schema、摘要、Seal、排序、唯一性和交叉引用的验证顺序；
4. SourceSnapshot 如何从 exact local object database 重获并复核全部 blob bytes；
5. Policy scope 与 Snapshot inventory 的精确双射，以及 module root 的 raw-component containment；
6. owned values 如何防止调用方在验证后修改 document 或 bytes；
7. 失败类型、无输出保证与重试历史边界；
8. 不同但充分的安全预算、不同输入路径和 CPython normal/`-O` 是否产生相同 owned semantic inputs；
9. Reference Lab 与合成 TOCTOU、错误 Seal、错 Snapshot/Profile binding 的单变量负例；
10. 哪些行为明确保留给 Fact、Relation、Slice、Coverage 与完整 Derivation 合同。

## 6. 当前裁决与停止线

本轮审计只选定合同边界，没有冻结字段、预算或实现 API。当前状态是：

```text
R1_SOURCE_SNAPSHOT_FROZEN
R1_DERIVATION_INPUT_PRECONTRACT_AUDITED
R1_DERIVATION_INPUT_CONTRACT_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只允许从本审计结论起草 docs-only `Derivation Input Binding Contract 0.1`。合同候选不得创建运行
源码、Schema、corpus、CLI、Provider、Manifest、标签或 Release；任何新反例仍可改变所选最小边界。
