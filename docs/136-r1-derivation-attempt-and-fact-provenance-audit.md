# R1 Derivation Attempt 与 Fact Provenance 前置审计

> 状态：`R1_DERIVATION_PROVENANCE_PRECONTRACT_AUDITED /
> R1_DERIVATION_PROVENANCE_CONTRACT_NOT_STARTED /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@7e0950ba2544476049e6defe1545f786971a89bd`
>
> 上游冻结事实：[R1 Derivation Input Binding 最小运行切片冻结发布](135-r1-derivation-input-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L0_DOCUMENTATION`；本文不修改冻结 Schema、兼容 corpus、
> SourceSnapshot/Input Binding runtime、Core、P/Q、CI 或发布坐标，也不创建 parser、Provider、Fact、
> Evidence、Relation、Slice、Coverage、Manifest、CLI 或 Workbench 实现

## 1. 审计问题

R1 已经能够把已发布 `SourceSnapshot`、sealed `ReviewPolicy`、固定 `DerivationProfile` 与 exact local Git
blob bytes 绑定成一个 copy-owned `DerivationInputSet`。这只证明后继消费者得到的是已经验证过的同一组
输入，没有证明一次 derivation 怎样开始、哪些 Provider 必须运行、Provider 输出怎样取得规范 Fact 身份，
也没有证明 Fact 与执行 Evidence 已经形成闭环。

本轮不问 Relation、Slice 或 Coverage 怎样实现，只问：

> 在允许 parser 或 Fact runtime 施工以前，Derivation Attempt、Provider Run、Fact provenance 与失败边界
> 还有哪些语义必须先冻结？

审计输入包括文档 86、113、120、127、131–135，十个冻结 R1 Schema、兼容 corpus、规范 identity vectors、
SourceSnapshot/Input Binding runtime 与测试。审计不把聊天记录、实现便利或未来产品设想当作规范来源。

## 2. 已经冻结且不得重解释的身份

### 2.1 `derivation_id` 是实例身份，不是语义输入摘要

冻结合同已经明确：

```text
derivation_id
  = caller-created opaque request-instance identity
  != digest(SourceSnapshot + Policy + Profile + Provider + Budget)
```

不同 derivation 不得复用该 ID；失败后若重新发布一个新 Bundle，必须使用新 ID。相同语义输入可以产生多次
独立 attempt；它们可以得到相同 Fact content identity，但不能伪装成同一次执行。

Provider 的实际语义与运行操作数由 `operands_digest` 绑定；`provider_run_id` 再绑定：

```text
derivation_id + capability_id + provider_id + operands_digest
```

因此必须继续保持：

```text
Derivation instance identity
  != Provider operands identity
  != Fact content identity
```

### 2.2 Fact identity 与 provenance identity 已经分离

`subject_key_digest` 与 `fact_id` 绑定 exact Snapshot、Profile、source anchor、subject space、ordinal、kind 与
规范属性；`provenance_refs[]` 不进入 Fact content identity。两个 Provider 报告相同规范 Fact 时可以共享
`fact_id`，同时保留不同 `provider_run_id`。

这意味着后继 runtime 不能为了携带执行 provenance 而把 attempt、时间、Provider 版本或 budget 塞进
`fact_id`，也不能为了保持稳定 `fact_id` 而丢掉 Provider Run。

## 3. 审计发现的合同接缝

### 3.1 必填 `request_provenance` 当前没有连续来源

冻结的 `DerivationEvidence` 必须包含：

```text
requested_repository_id
requested_ref
resolver_id
resolver_version
resolved_at
```

但当前 SourceSnapshot 首版明确拒绝 branch、tag、`HEAD`、缩写与 revision expression，只接收 exact commit
OID。发布的 `source-snapshot.json` 保存 exact repository/commit/tree/root/inventory identity，不保存 friendly
ref、resolver 或 resolution time；`DerivationInputSet` 也故意不保存 wall-clock、attempt 或运行 provenance。
`SourceSnapshotRuntimeProvenance` 只记录 acquisition profile、Git/Python/OS 身份，同样没有这五个字段。

因此未来 derivation runtime 不能从冻结输入复原示例中的 branch provenance。若不补合同，它只能：

1. 接受调用方在事后给出的不可核对叙述；
2. 把 derivation 时刻误写成早先 Snapshot acquisition 的 resolution time；
3. 发明一个并未发生的 branch/tag resolver；或
4. 留空必填字段并产生 Schema-invalid Evidence。

四种做法都不合格。后继合同必须明确 `request_provenance` 描述的是哪一次请求解析，并为 exact-only 首版
建立可诚实产生、可验证、可随同 attempt 消费的来源。不能通过重写 SourceSnapshot content identity 偷渡
运行时间。

### 3.2 capability requirement 还没有闭合 Provider applicability

sealed `ReviewPolicy.provider_requirements[]` 只绑定 `capability_id / required / CUMULATIVE`，不绑定
`provider_id`。`DerivationEvidence` 则记录实际 Provider、parser、runtime 与版本。冻结文本要求所有适用且
required 的来源都被观察，并禁止 `first-success`，但当前没有版本化 Provider manifest、registry snapshot、
discovery result 或首版 applicability 规则。

于是同一组冻结输入可能面对：

```text
Host A: capability C has Provider P1
Host B: capability C has Provider P1 + P2
```

如果应用只运行自己先找到的一个 Provider，两台宿主都可以声称满足了同一 Policy，却对“所有适用来源”
拥有不同分母。安装状态、迭代顺序或 entry-point 顺序不能暗中成为 coverage authority。

后继合同必须明确区分：

```text
Policy capability requirement
  != Provider implementation identity
  != Provider applicability/binding for this attempt
  != ambient installed packages
```

首版可以收窄为一个显式、可验证的 Provider binding 规则，但不能用“当前机器只装了什么”替代冻结边界，
也不能为了方便 parser 实现而扩大 R1 为通用插件发现系统。

### 3.3 三类 execution budget 的终止语义没有同等闭合

`ReviewPolicy.execution_budget` 固定包含：

```text
wall_clock_ms
memory_bytes
artifact_bytes
```

并要求整个 derivation 共用一个绝对预算，子阶段不得刷新。但当前 `DerivationEvidence` 的 typed diagnostics
只有 `EXECUTION_DEADLINE` 与 `EXECUTION_CANCELLED` 能表达 whole-operation interruption；没有内存或 Artifact
预算耗尽的明确 code，冻结文字也只把 wall-clock timeout 明确映射为 `INTERRUPTED`。

因此以下结果尚无唯一合法表达：

```text
memory budget exhausted before Provider completes
artifact budget exhausted while canonical Fact bytes are staged
```

把它们写成 `PROVIDER_FAILED` 会把 runtime safety stop 错归给 Provider；写成
`INTERNAL_DERIVATION_ERROR` 会把预期停止线冒充未知错误；只在本地日志记录又无法支持后继 DIAGNOSTIC
Bundle。

此外，冻结 Evidence 只记录起止时间与状态，没有峰值内存、Artifact byte consumption 或 budget deadline。
后继合同必须先决定：这些预算只要求 trusted runtime 执行，还是还要求标准 Evidence 可独立复核消费事实。
若要求后者，现有 Schema 字段不足，必须显式重开 Schema/corpus/identity vectors；不得由 runtime 添加私有
字段或借自由文本日志补洞。

### 3.4 `reported_*_ids` 与正式 Artifact 只有单向一致性

当前 conformance test 已检查：

```text
Fact.provenance_refs subset-of DerivationEvidence.provider_run_id
Relation.provenance_refs subset-of DerivationEvidence.provider_run_id
```

但它没有检查反向关系：

```text
ProviderRun.reported_fact_ids
  == the canonical Facts attributed to that run

ProviderRun.reported_relation_ids
  == the canonical Relations attributed to that run
```

于是一个 Schema-valid Bundle 可以让 ProviderRun 报告不存在的 ID、漏报已经归属于它的 Fact，或让 Fact
引用该 run 而 run 不承认该 Fact。路径、摘要和局部 Schema 全部合法，也不能推出 provenance closure。

`FAILED / INTERRUPTED / UNAVAILABLE` run 仍允许任意 `reported_*_ids`，而 DIAGNOSTIC Manifest 又禁止携带
FactSet/RelationSet。这会产生第二个歧义：这些 ID 是允许悬空的非权威 candidate 标识，还是失败 run 必须
使用空数组？冻结文本只说已观察前缀可留在 typed diagnostics/Evidence，但当前 diagnostic shape 不能携带
Fact body，尚不足以回答。

组合后还有更深一层：ProviderRun 可以先 `COMPLETED` 并报告 Fact IDs，随后整个 derivation 在 Relation、
Slice、Coverage 或 staging 阶段中断。最终 DIAGNOSTIC Bundle 同样没有 FactSet/RelationSet，因此即使 run
自身成功，这些 ID 仍然悬空。只约束 `run.status != COMPLETED` 不足以闭合 Manifest。

后继合同必须同时定义完整成功态的双向闭包、非成功 run 与非成功 overall derivation 的 ID 语义；不能只
验证“Fact 指向某个存在的 run”。

### 3.5 Provider 输出不能自行取得 canonical authority

R0 允许 Provider 报告有界事实，但 Fact 身份与规范化合同共同拥有 canonical identity。若 Provider 直接返回
完整 `fact_id`，application 不复算 anchor、kind/space、attributes、ordinal 与 digest，那么 Provider 实际上
同时成为观察者和身份裁判。若 application 只按最后一个 Provider 覆盖，又会丢掉累计 provenance 与 conflict。

后继合同必须选择并冻结边界：Provider 可以返回 typed candidate observation；R application 必须以冻结
Profile 对同一 owned source bytes 独立校验、规范化并复算 content identity。Provider 声明的 ID 最多是待核对
输出，不能因为 Provider execution success 自动成为 canonical Fact。

### 3.6 Manifest 资格仍属于完整闭环，而不是 Fact runtime

冻结 Manifest 只有：

```text
COMPLETE
  -> Snapshot + Policy + Profile + Evidence + Fact + Relation + Slice + Coverage

DIAGNOSTIC
  -> Snapshot + Policy + Profile + Evidence
```

因此即使后继 runtime 能生成规范 Fact 与 Provider Run，也不能发布五文件 `FACT_COMPLETE` Bundle，不能用空
Relation/Slice/Coverage 占位，也不能把一个内存态 result 叫作 Derivation Manifest。

Fact runtime 的成功只证明 Fact provenance 最小闭环成立，不证明 Relation、Slice、Coverage 或完整
derivation 已经完成。

## 4. 反例矩阵

| # | 单变量反例 | 若不补合同会发生什么 | 必须保持的裁决 |
| ---: | --- | --- | --- |
| 1 | 相同输入使用两个不同 `derivation_id` | attempt 被错误去重为同一次执行 | Fact identity 可相同，run/evidence identity 必须不同 |
| 2 | `derivation_id` 相同但 Provider operands 改变 | 同一 attempt 中途换操作数 | 拒绝；operands 在 run 前固定 |
| 3 | exact-only Snapshot 没有 branch/tag 历史 | runtime 伪造 friendly provenance | 只记录真实发生且可解释的 exact request provenance |
| 4 | 同 capability 在宿主上存在两个 Provider | `first-success` 把另一个来源静默排除 | applicability 分母必须显式且可复算 |
| 5 | required Provider 成功返回空集合 | 空集合被误解为 capability 未观察 | 合法空观察；不得取消其他 required source |
| 6 | optional Provider 失败 | 整体被错误写成 UNAVAILABLE，或失败被删除 | 保留 run/diagnostic；按冻结 merge rule 处理整体状态 |
| 7 | memory/artifact budget 先耗尽 | safety stop 被误写成 Provider failure | 先冻结 typed terminal semantics；未闭合前不实现 |
| 8 | ProviderRun 报告不存在的 `fact_id` | Evidence 内出现悬空事实声明 | COMPLETE closure 必须双向一致 |
| 9 | Fact 引用 run，但 run 漏报该 Fact | provenance 只有单向可达 | 拒绝；run 与 canonical FactSet 必须互相闭合 |
| 10 | FAILED run 带非空 `reported_fact_ids`，DIAGNOSTIC 无 FactSet | ID 无法解释或复核 | 明确其为禁止值或另有非权威语义；不得含糊 |
| 11 | Provider 返回错误但形状合法的 `fact_id` | Provider 自授 canonical authority | application 独立复算并拒绝不一致 |
| 12 | Fact runtime 成功后直接发布五文件目录 | 新增未冻结 Manifest outcome | 禁止；runtime value 不等于可发布 Bundle |
| 13 | ProviderRun 已完成，后继阶段中断，overall 为 INTERRUPTED | DIAGNOSTIC 中保留无法解析的 Fact/Relation IDs | overall 非 COMPLETED 时所有 reported IDs 必须为空 |

## 5. 候选边界比较

| 候选 | 是否形成最小闭环 | 裁决 |
| --- | --- | --- |
| 直接实现 Python parser + FactSet | request/provider/budget/provenance 仍有歧义 | 拒绝 |
| 直接实现完整 Derivation | 一次跨过 Provider、Fact、Relation、Slice、Coverage 与 Manifest | 拒绝 |
| 只增加 Provider discovery | 没有 attempt、budget 或 Fact 消费者，且会扩大为通用插件系统 | 拒绝 |
| 只修一条 `request_provenance` 字段 | 其余三个组合接缝仍会由实现替合同决定 | 拒绝 |
| 冻结 Derivation Attempt / Provider Binding / Fact Provenance runtime contract | 能先闭合真实来源、适用分母、预算所有权和双向 provenance，再允许 parser/Fact 施工 | 选择 |

## 6. 选定的下一个最小合同闭环

后继合同只允许定义：

```text
owned DerivationInputSet
        +
caller-owned opaque derivation_id
        +
truthful exact request provenance
        +
explicit bounded Provider applicability/binding
        ↓
one derivation-attempt lifecycle
        ↓
one shared absolute execution budget
        ↓
typed Provider Run result(s)
        ↓
application-normalized canonical Fact candidates
        ↓
bidirectionally closed ProviderRun <-> Fact provenance
        ↓
one copy-owned, non-published runtime result
```

合同可以为首个 Python 3.10 deterministic Fact provider 收窄 applicability 与运行环境，但必须保持
Provider implementation 可替换、Fact identity 由公共合同复算，并且失败不能伪装成空成功。

成功 runtime value 不是 `FactSet` Artifact、`DerivationEvidence` Artifact 或 Manifest；它只保存后继完整
derivation 所需的同一次 attempt 事实。失败/中断结果必须足以在未来形成合法 DIAGNOSTIC Evidence，但本切片
不得自行发布 Bundle。

## 7. 后继合同必须先回答的问题

1. `request_provenance` 精确描述哪次 resolution；exact-only 首版怎样产生五个必填字段；
2. Provider applicability 由谁冻结，怎样与 capability-level Policy 对齐；
3. 首版是否限制每个 capability 一个显式 Provider binding，以及未来多来源怎样升级；
4. derivation attempt 的 admission point、预算起点、绝对 deadline 与 cancellation owner；
5. memory/artifact budget exhaustion 的 terminal status、typed diagnostic 与证据充分性；
6. 是否要求标准 Evidence 保存可复核 budget consumption；若需要，怎样显式重开 Schema；
7. Provider candidate output 与 application canonical Fact 之间的校验、规范化和 identity ownership；
8. COMPLETE derivation 中 `reported_*_ids` 与正式 Artifact 的双向闭包；
9. run 或 overall derivation 非 COMPLETED 时是否必须使用空 `reported_*_ids`；
10. copy-owned runtime result 怎样保证 verified/normalized bytes 与后继消费者连续；
11. 哪些失败发生在 attempt admission 前，因此没有合法 DerivationEvidence；
12. 本切片怎样证明 Provider 可替换，但不提前创建动态 discovery、CLI 或公共发布格式。

## 8. Fresh-Agent 交接与停止线

本文是下一个合同的导航入口，不复制或覆盖文档 120 的冻结 Schema。一个没有聊天上下文的新 Agent 只依赖
仓库时，必须得出以下结论：

```text
Current frozen input:
  SourceSnapshot + DerivationInputSet

Only allowed next work:
  docs-only Derivation Attempt / Provider Binding / Fact Provenance contract

Still forbidden:
  runtime implementation
  Relation / Slice / Coverage
  complete Derivation Manifest
  AI proposal / ranking / HumanDisposition
  Q implementation or D product shell
```

若 fresh Agent 认为可以直接创建 FactSet、从 ambient packages 猜 Provider、伪造 branch provenance、刷新每个
Provider 的完整 budget，或发布 Fact-only Manifest，则交接材料或后继合同仍不充分。

本轮只完成审计并选择候选合同边界，没有冻结 API、Provider 数量、budget failure mapping、Schema 修正或
实现类型。下一步只允许从新的 exact main 起草 docs-only 合同；合同候选自己的门禁、受保护主线合入、
exact-main 门与匿名公开读回全部成立前，状态继续保持：

```text
R1_DERIVATION_PROVENANCE_PRECONTRACT_AUDITED
R1_DERIVATION_PROVENANCE_CONTRACT_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```
