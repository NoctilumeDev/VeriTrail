# R1 Derivation Attempt 与 Fact Provenance 最小运行合同 0.1

> 状态：`R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@7e0950ba2544476049e6defe1545f786971a89bd`
>
> 前置审计：[R1 Derivation Attempt 与 Fact Provenance 前置审计](136-r1-derivation-attempt-and-fact-provenance-audit.md)
>
> 上游冻结输入：[R1 Derivation Input Binding 最小运行切片冻结发布](135-r1-derivation-input-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文不创建或修改 Schema、兼容 corpus、identity vector、
> runtime、parser、Provider、FactSet、DerivationEvidence、Relation、Slice、Coverage、Manifest、CLI、
> Workbench、Core、P/Q 或发布坐标

## 1. 目的与停止线

R1 已经能够把 `SourceSnapshot + ReviewPolicy + DerivationProfile + exact Git blob bytes` 安全绑定为一个
copy-owned `DerivationInputSet`。下一步不能直接写 Python parser：一次真实推导还缺少 attempt 身份、请求
provenance、Provider 适用分母、共享预算所有权，以及 Provider Run 与 canonical Fact 的双向闭包。

本文只冻结下列边界：

```text
owned DerivationInputSet
        +
caller-owned opaque derivation_id
        +
one explicit bounded Provider binding
        +
one shared execution-budget context
        ↓
one Provider run
        ↓
typed candidate Fact observations
        ↓
application-side canonical identity
        ↓
closed ProviderRun <-> canonical Fact provenance
        ↓
copy-owned, non-published phase result
```

本合同不会授权：

```text
real Python parser
ambient Provider discovery
multiple Providers for one capability
FactSet / DerivationEvidence publication
Relation / Slice / Coverage
conflict / UNKNOWN propagation
complete R1_DERIVATION Manifest
AI proposal / ranking / HumanDisposition
Q implementation or D product shell
```

这里的目标不是提前做半个 Derivation，而是先证明：

```text
the source bytes verified for this attempt
  = the bytes observed by the Provider

the canonical Fact accepted by the application
  = the Fact named by the ProviderRun record
```

## 2. 已冻结且不重解释的输入

### 2.1 `DerivationInputSet`

运行边界只接收文档 132–135 已冻结的 owned value，不重新接收三份 Artifact 路径，也不重新从工作树读取
源码。Provider 只能消费其中已经复核并 copy-owned 的 exact blob bytes。

因此继续保持：

```text
Path locates input.
Owned bytes determine what was validated and may be consumed.
```

Input Binding 的 acquisition safety budget 已在返回 `DerivationInputSet` 时终止；它不延长、借用或预消费
本合同的 derivation execution budget。

### 2.2 `derivation_id`

`derivation_id` 由调用方在一次新 derivation 请求前生成，是 `NonEmptyText` 形状的 opaque
request-instance identity：

```text
derivation_id
  != semantic digest
  != provider operands digest
  != Fact identity
```

调用方负责不复用该 ID。runtime 能验证形状与本次请求内唯一性，不能在没有权威 registry 的情况下声称
已经证明全世界从未使用过它。失败后若发起新的 derivation，调用方必须提供新 ID。

### 2.3 sealed Policy 与固定 Profile

`ReviewPolicy` 继续拥有 scope、capability requirement、execution budget 与 governance；
`DerivationProfile` 继续拥有 Python 3.10 结构语义、Fact kind、anchor、identifier 与规范化规则。

Provider implementation、宿主 Python 版本、执行时间与运行状态不能进入 Fact content identity；它们只能进入
Provider operands、Provider Run 与后继 Evidence。

## 3. 首个 Provider applicability profile

### 3.1 只接受一个明确能力

首个运行切片只接受以下 sealed requirement：

```json
[
  {
    "capability_id": "python-ast",
    "required": true,
    "composition_mode": "CUMULATIVE"
  }
]
```

Policy 包含其他 capability、缺少该 requirement、把它改成 optional，或出现任何其他 requirement 集合时，
首切片在 attempt admission 前 fail closed。它不能把自己尚未实现的 capability 当成空成功，也不能改写已
sealed Policy。

这一收窄只定义首个实现适用域，不把 R1 0.1 的长期 Provider 模型永久限制为单来源。后继若要支持多个
capability 或同一 capability 的多个独立事实源，必须先冻结新的 applicability/组合合同与 conflict/
Coverage 传播，不能把循环顺序或 `first-success` 当成升级方案。

### 3.2 `ProviderBinding` 是显式操作输入

调用方必须显式提供恰好一个 binding；它至少固定：

```text
capability_id = python-ast
provider_id
provider_version
parser_id
parser_version
runtime_id
runtime_version
provider implementation handle
```

前七项必须在执行前 copy-own 并冻结；implementation handle 只提供调用能力，不进入 JSON Artifact。
runtime 不扫描 entry point、`sys.path`、editable install、虚拟环境或已安装包来猜“当前有哪些 Provider”。

binding 缺失、重复、含额外 capability、descriptor 为空，或执行时返回与冻结 descriptor 不一致的身份，均
不得进入正常 Provider execution。首版每个 capability 恰好一个 binding，因此：

```text
Policy requirement
  != Provider identity
  != ambient installation state

Applicable Provider set
  = the one explicit binding admitted under this contract
```

Seal authority 在现有 Policy 0.1 中授权的是 capability，不是具体 implementation；首切片的 caller 只拥有
本次运行的 operational selection，并且选择结果必须完整进入 Provider operands/run。protocol conformance
只能证明 implementation 能按接口交付候选，不能自动证明它值得信任。由于本切片不发布 Artifact，首版不
新增 Provider trust registry；真实 parser 进入公共 Evidence 前，后继合同必须在“固定内建 descriptor”与
“版本化 Provider authorization artifact”之间作出明确选择，不能把 caller selection 偷换成人类 Seal。

### 3.3 可替换性不等于动态发现

实现必须通过窄 Provider protocol 注入至少两个独立确定性测试 Provider，并证明：

```text
same owned source + same normalized observation
  -> same subject_key_digest / fact_id

different provider descriptor or derivation_id
  -> different operands_digest / provider_run_id
```

这足以证明 Provider 可替换，不需要在首版建立 registry、plugin discovery、远程 Provider 或多进程服务。

## 4. exact request provenance

### 4.1 它记录本次 attempt 真正请求的坐标

首版不伪造 SourceSnapshot 建立以前可能存在的 branch/tag 历史。`request_provenance` 描述的是本次
derivation attempt 对 owned Snapshot exact coordinate 的绑定：

```text
requested_repository_id
  = SourceSnapshot.source_coordinate.repository_id

requested_ref
  = "oid:" + lowercase(commit_oid.algorithm) + ":" + commit_oid.hex

resolver_id
  = "veritrail-r1-owned-snapshot-exact-oid"

resolver_version
  = "0.1"

resolved_at
  = trusted runtime 完成 exact coordinate admission 的 UTC 时间
```

例如：

```text
oid:sha1:0123456789abcdef0123456789abcdef01234567
oid:sha256:0123456789abcdef...<64 hex chars>
```

算法名来自冻结 `GitOid.algorithm`，只允许 `sha1 / sha256`；hex 使用冻结的小写规范形式。该字符串是
Evidence provenance，不替代结构化 `commit_oid`，也不进入 SourceSnapshot、Fact 或 Relation identity。

### 4.2 这不是历史别名恢复

首版 `requested_ref` 不声称：

```text
which branch was originally checked out
which tag a human had in mind
what HEAD pointed to during Snapshot acquisition
```

未来 alias-aware resolver 可以在真正执行并保存可验证 resolution 时记录 branch/tag，但不得从 exact
Snapshot 反向猜测。相同 Snapshot 由不同真实请求解析得到时，Fact identity 可以相同，Evidence identity
可以不同。

## 5. Admission、生命周期与时间

### 5.1 attempt admission 前

以下检查发生在 attempt admission 前：

1. `DerivationInputSet` 类型与 owned continuity 可用；
2. `derivation_id` 形状合法；
3. Policy requirement 与首版 applicability profile 完全一致；
4. Provider binding 与 requirement 构成一一对应；
5. descriptor 字段完整且可 copy-own；
6. monotonic clock、UTC clock、cancellation 与预算执行原语可用；
7. runtime 能建立本合同要求的 memory containment。

这些前置条件失败时，没有一次合法开始的 derivation attempt，因此不构造伪造
`DerivationEvidence/ProviderRun`。未来实现错误闭集至少区分：

```text
INVALID_DERIVATION_ATTEMPT_REQUEST
PROVIDER_BINDING_MISMATCH
DERIVATION_RUNTIME_UNAVAILABLE
INTERNAL_DERIVATION_ADMISSION_ERROR
```

错误只携带稳定 code 与固定说明，不泄露绝对路径、源码、stack trace 或 locale 文本。

### 5.2 admission 原子边界

一次 admission 必须在任何 Provider 初始化、parser 加载或 candidate 生成前完成：

```text
freeze request + descriptor
        ↓
derive exact request provenance
        ↓
capture resolved_at
        ↓
capture monotonic t0 and UTC started_at
        ↓
deadline = t0 + wall_clock_ms
        ↓
state = RUNNING
```

`resolved_at <= started_at`。UTC 用于 Artifact provenance；deadline 与 elapsed 判断只使用 monotonic clock，
不得因系统时钟回拨或 NTP 调整延长预算。

### 5.3 运行与终止

首版严格串行且只有一个 Provider Run。应用层不自动 retry；调用方 retry 必须使用新 `derivation_id` 与新
attempt。Provider 内部若未来需要 retry，必须由其版本化合同声明，并始终消费同一个 run identity 与剩余
预算；本切片的确定性测试 Provider 不 retry。

Provider Run 的终态仍使用冻结闭集：

```text
COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE
```

run 从 Provider 初始化前开始，直到 application 完成 candidate validation、canonical identity 复算与 run
summary 组装后才结束；仅“Provider callable 返回”还没有资格写 `COMPLETED`。descriptor 已在 admission
冻结，因此 Provider 初始化后不可用仍能形成真实 `UNAVAILABLE` run，而不是退回 ambient discovery。

phase result 的顶层状态先服从 whole-phase stop：deadline、cancellation 或 memory limit 在 Provider 执行、
application validation、canonicalization 或 result 组装期间发生时，顶层均为 `INTERRUPTED`；当时仍 active
的 run 同为 `INTERRUPTED`，已经终止的 run 不被反写。不存在 whole-phase stop 时，顶层状态才等于唯一
required Provider Run 的状态。`COMPLETED` 只表示本合同覆盖的 Provider/Fact phase 正常结束，不表示完整
R1 derivation、Coverage 或 Manifest 已完成。

## 6. 一个共享的 execution budget

### 6.1 所有权

`ReviewPolicy.execution_budget` 是本次 derivation 的 sealed 上限。runtime 在 admission 时只创建一次共享
budget context；Provider 初始化、执行、candidate 交付、application validation、canonicalization 与 phase
result 组装只能消费该 context 的剩余量。

不得出现：

```text
provider start     -> new full wall-clock budget
normalization      -> new full wall-clock budget
force termination  -> new full cleanup budget
future relation    -> new full derivation budget
```

后继完整 derivation 必须把同一个 context 继续传给 Relation/Slice/Coverage 与 staging；本切片不得创建一个
“Fact 已完成，所以后面重新计时”的断点。

### 6.2 三个维度

首版语义固定为：

```text
wall_clock_ms
  从 admission 的 monotonic t0 到 phase/future derivation 终止的绝对 elapsed 上限。

memory_bytes
  attempt execution cell 的 process-tree memory hard upper bound；worker runtime、Provider、parser、
  candidate 与 canonical staging 都在该 containment 内。调用方在 admission 前已经持有的
  DerivationInputSet 不计入该 cell，但传入 cell 后产生的副本计入。

artifact_bytes
  完整 derivation 将要 create-new 发布的 staging 目录内所有 regular-file bytes 的累计上限，包含三份
  输入 Artifact、DerivationEvidence、Fact/Relation/Slice/Coverage、Manifest；不包含目录项或外部日志。
```

当前切片不发布文件，因此 `artifact_bytes` 不会因为内存中的 candidate/result 被伪装成“已写 Artifact”而
消费；这些内存受 `memory_bytes` 约束。后继 staging 必须按实际将写入的 exact bytes 累加，并在超限时删除
staging，不发布半目录。

memory containment 可以由 Windows Job、受控 worker/cgroup 或未来等价 primitive 实现，但必须在 Provider
开始前生效，覆盖完整 execution cell，并在超限后 fail closed。只有采样、post-hoc RSS 检查或 Provider
自报用量，不能证明 hard upper bound；无法建立 containment 时在 admission 前返回
`DERIVATION_RUNTIME_UNAVAILABLE`。

### 6.3 Evidence 的认识论上限

现有 `DerivationEvidence` 绑定 sealed `policy_digest`、时间、status 与 typed diagnostic，但不保存 peak
memory、逐阶段 byte counter 或 monotonic deadline。首版不新增这些字段，也不声称标准 Evidence 可以独立
复算完整资源曲线。

因此首版只承诺：

```text
runtime conformance tests prove enforcement mechanism
Evidence records declared ceilings through policy_digest
Evidence records terminal dimension through typed diagnostic
```

若未来要求第三方仅凭 Bundle 复核 peak/consumption，必须新增版本化测量 Artifact 或升级 Evidence Schema；
不能把本机日志当成规范证据。

## 7. 必要的 Schema 语义修正

现有 `review-derivation-evidence-0.1.schema.json` 无法诚实区分 memory 与 artifact budget exhaustion。运行时
实现前必须单独完成 L2 Schema/corpus 修正，至少加入：

```text
EXECUTION_MEMORY_BUDGET
EXECUTION_ARTIFACT_BUDGET
```

终止映射固定为：

| 条件 | Provider Run | phase / future overall | diagnostic |
| --- | --- | --- | --- |
| wall-clock absolute deadline | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_DEADLINE` |
| caller cancellation | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_CANCELLED` |
| memory containment limit | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_MEMORY_BUDGET` |
| artifact staging limit | 当前 active run 已结束时不反写其状态 | `INTERRUPTED` | `EXECUTION_ARTIFACT_BUDGET` |
| Provider unavailable | `UNAVAILABLE` | `UNAVAILABLE` | `PROVIDER_UNAVAILABLE` |
| Provider execution exception | `FAILED` | `FAILED` | `PROVIDER_FAILED` |
| candidate conformance/identity failure | `FAILED` | `FAILED` | `NONCONFORMANT_PROVIDER_OUTPUT` |
| unknown application fault | `FAILED` | `FAILED` | `INTERNAL_DERIVATION_ERROR` |

Artifact limit 发生在后继 staging 时，已经 `COMPLETED` 的 ProviderRun status 是历史事实，不因下游失败
改写；完整 Evidence 顶层状态必须为 `INTERRUPTED`，同时所有 `reported_*_ids` 必须清空，因为 DIAGNOSTIC
Bundle 没有 FactSet/RelationSet 可解析它们。本 Fact phase 尚不触发该行，但必须先冻结同一预算未来怎样传播。

Schema/corpus 修正还必须表达或由 conformance test 强制：

```text
ProviderRun.status != COMPLETED
  -> reported_fact_ids == []
  -> reported_relation_ids == []

DerivationEvidence.overall_execution_status != COMPLETED
  -> every ProviderRun.reported_fact_ids == []
  -> every ProviderRun.reported_relation_ids == []
```

这次修正不新增 Evidence 字段、不改变已冻结 digest projection，也不回写历史 fixture。它需要新的负例、
Schema bytes 读回与独立冻结链；修正完成以前，本文即使合入也不授权 runtime implementation。

## 8. Provider 输出与 canonical Fact authority

### 8.1 Provider 只报告 candidate observation

Provider 不得把完整 Fact Artifact 当成受信输出。首版 Provider protocol 的语义输出只允许包含冻结 Profile
能够验证的 candidate 字段：

```text
subject_space
fact_kind
source_anchor
local_ordinal
semantic_attributes
```

Provider 不输出或不拥有：

```text
source_snapshot_digest
derivation_profile_digest
subject_key_digest
fact_id
provenance_refs
fact_set_digest
```

若具体传输格式为了调试携带 claimed digest，application 仍必须独立复算并在不一致时拒绝；claimed 值不因
Provider success 获得 authority。

### 8.2 application 负责规范身份

application 必须针对同一个 `DerivationInputSet`：

1. 验证 anchor path 指向 IN_SCOPE、受支持且已 reacquire 的 exact blob；
2. 验证半开 byte interval 落在该 blob 内；
3. 按固定 Profile 验证 `fact_kind / subject_space / ordinal / attributes`；
4. 规范化 identifier、path 与 attributes；
5. 复算 `subject_key_digest`；
6. 复算 `fact_id`；
7. 加入 application-owned `provenance_refs`。

Provider execution success 不推出 candidate 合法。任一 candidate 非规范、越界或身份不一致，唯一 required
run 与 phase 均为 `FAILED / NONCONFORMANT_PROVIDER_OUTPUT`；不能丢弃坏 candidate 后把剩余前缀叫成功。

application 的校验权只覆盖结构、规范化与 identity，不把它变成第二个事实观察者。没有真实 parser 时，
application 不能仅凭一个形状合法的 candidate 独立证明“源码确实声明了该 symbol”；该事实 authority 仍由
可追溯 Provider observation 提供。因而必须保持：

```text
Provider owns bounded observation.
Application owns conformance and canonical identity.
Neither one alone owns review judgment or Core Verdict.
```

### 8.3 首切片不实现真实 parser

首个实现只允许使用有界确定性测试 Provider，对 Reference Lab 已有 exact blob 产生预定 candidate，证明
替换、失败、空输出、预算和 provenance 机制。它不能把 fixture Provider 宣传成 Python 3.10 parser。

真实 parser 仍需下一轮审计，至少先回答：

```text
parse failure / unsupported entry 怎样成为后继 Coverage 输入
accepted encoding 怎样与 raw byte anchor 共存
parser diagnostics 怎样保持 typed 且不泄露源码
一个 file 的部分 AST 是否有资格产生 canonical Fact
```

这些问题未冻结前，不能通过“先用 ast.parse 跑起来”替合同作答。

## 9. ProviderRun 与 Fact provenance 双向闭包

### 9.1 成功态

首版唯一 run `COMPLETED` 时：

```text
accepted canonical Facts
  = all and only Facts whose provenance_refs contain provider_run_id

ProviderRun.reported_fact_ids
  = sorted(unique(accepted canonical fact_id))

ProviderRun.reported_relation_ids
  = []
```

每个 accepted Fact 的 `provenance_refs` 恰为 `[provider_run_id]`。成功空输出合法：Facts 与
`reported_fact_ids` 同时为空，但仍保留一个 `COMPLETED` ProviderRun，不能把空集合解释为未运行。

`reported_fact_ids` 是 application 在 Provider output 通过规范化与 identity 复算后写入的 run summary，
不是对 Provider 原始字符串的盲拷贝，也不表示 Provider 获得 canonical ID authority。

同一 Provider 重复报告字节级相同 candidate 时，application 可按 canonical identity 去重；如果同一
subject 在唯一 Provider 输出中出现不兼容 candidate，首切片视为非规范 Provider 输出并 fail closed。这个
裁决不替代未来多来源 conflict：首切片根本没有获得多来源 conflict 表达权。

### 9.2 非成功 run 或非成功 overall

`INTERRUPTED / FAILED / UNAVAILABLE` run 必须满足：

```text
reported_fact_ids = []
reported_relation_ids = []
no canonical Fact escapes the phase result
```

Provider 在失败前产生的部分 candidate 只属于临时 construction state；可以通过稳定 diagnostic 表达失败，
但不能获得 Fact identity、FactSet 身份或 dangling ID。失败不是空成功。

未来 `DerivationEvidence.overall_execution_status != COMPLETED` 时，即使某个较早 run 的 status 已经是
`COMPLETED`，该 Evidence 内所有 run 的 `reported_fact_ids/reported_relation_ids` 仍必须为空。run 的状态
可以保留历史成功，但 DIAGNOSTIC file set 不得引用没有随 Bundle 发布的 normal Artifact。

本切片同样适用：`phase status != COMPLETED` 时，phase result 不暴露 canonical Facts，且其中任何
ProviderRun-shaped summary 的 `reported_*_ids` 均为空，即使 whole-phase stop 发生前 Provider callable
已经成功返回。

### 9.3 digest 连续性

`operands_digest` 与 `provider_run_id` 严格复用文档 120 的 domain-separated projection。application 必须从
owned input digests 与 admitted descriptor 复算；Provider 不能提交私有 operands hash。

相同 candidate 在两个新 attempt 中应满足：

```text
fact_id(A) = fact_id(B)
provider_run_id(A) != provider_run_id(B)
```

相同 attempt ID 但 descriptor/operands 改变必须在执行前拒绝，不允许一个 run identity 中途换操作数。

## 10. 非发布 phase result 与连续性

成功或失败返回值至少 copy-own：

```text
derivation_id
exact request provenance
input semantic digests
admitted Provider descriptor
operands_digest
ProviderRun-shaped execution facts
accepted canonical Facts, only when COMPLETED
phase status
started_at / finished_at
typed diagnostics
```

它：

- 不是 JSON Artifact；
- 没有 `artifact_kind`、Schema、semantic digest、Manifest role 或发布路径；
- 不是 `FactSet` 或 `DerivationEvidence`；
- 不包含 Relation、Slice、Coverage 或完整 derivation status；
- 不得在 call 返回后重新开启一个完整 execution budget，再冒充同一次连续 derivation；
- document/mapping view 必须来自 owned value，不能被调用方就地修改后交给后继消费者。

未来完整 derivation 若复用该 phase 实现，必须在同一个尚未终止的 shared budget context 内调用它，并直接
消费同一 owned phase facts；不能执行：

```text
run fact phase
  -> serialize temporary file
  -> later reread
  -> start a new budget
  -> call it the same derivation
```

Standalone 首切片测试返回的 phase result 只证明组件语义，不具有事后升级成 Manifest 的资格。

## 11. 失败与重试

### 11.1 admission 前失败

无合法 attempt、无 ProviderRun、无 Evidence。调用方修正请求后重新调用。

### 11.2 admission 后失败

一旦进入 `RUNNING`，runtime 必须收敛到 typed terminal phase result，清理 execution cell，并保证非成功态
没有 canonical Fact 外泄。已知错误不能降格为 internal error；未知错误不能泄露本机或源码内容。

### 11.3 retry

调用方重试必须重新：

```text
generate derivation_id
admit exact Provider binding
create budget context
run Provider
```

前一次 candidate、worker、deadline、diagnostic buffer 或 phase result 不得作为隐藏 checkpoint 续用。
重试 history 不进入 SourceSnapshot、Fact 或 Profile identity。

## 12. 合同矩阵

| # | 单变量义务 | 预期 |
| ---: | --- | --- |
| 1 | owned InputSet + exact single Provider binding | admission 成功 |
| 2 | branch/tag/HEAD provenance 被调用方补写 | 拒绝，不伪造历史 alias |
| 3 | `requested_ref` 使用规范 exact OID | 可由 Snapshot coordinate 复算 |
| 4 | Policy 多一个 capability | pre-admission fail closed |
| 5 | binding 缺失、重复或多余 | `PROVIDER_BINDING_MISMATCH` |
| 6 | 两个可替换测试 Provider 报告相同 candidate | Fact ID 相同，run ID 不同 |
| 7 | 相同输入更换 `derivation_id` | Fact ID 相同，run ID 不同 |
| 8 | 相同 `derivation_id` 中途更换 descriptor | 执行前拒绝 |
| 9 | Provider 成功空输出 | COMPLETED run + empty Facts/IDs |
| 10 | Provider exception | FAILED；IDs 空；无 canonical Fact 外泄 |
| 11 | Provider runtime 不可用 | UNAVAILABLE；IDs 空 |
| 12 | candidate anchor 越界 | FAILED / NONCONFORMANT_PROVIDER_OUTPUT |
| 13 | candidate claimed digest 错误 | application 复算并拒绝 |
| 14 | wall-clock deadline | INTERRUPTED / EXECUTION_DEADLINE |
| 15 | caller cancellation | INTERRUPTED / EXECUTION_CANCELLED |
| 16 | memory containment limit | INTERRUPTED / EXECUTION_MEMORY_BUDGET |
| 17 | host 无法建立 memory containment | admission 前 DERIVATION_RUNTIME_UNAVAILABLE |
| 18 | non-COMPLETED run 带 reported ID | Schema/conformance 拒绝 |
| 19 | run COMPLETED，但 overall 后继中断且仍带 reported ID | DIAGNOSTIC conformance 拒绝 |
| 20 | COMPLETE run 漏报 accepted Fact | 双向 provenance 拒绝 |
| 21 | COMPLETE run 报告不存在 Fact | 双向 provenance 拒绝 |
| 22 | result mapping 被调用方修改 | owned value 不变 |
| 23 | phase result 被写成 FactSet/Evidence/Manifest | 明确拒绝，无发布物 |
| 24 | phase 后给 Relation 刷新完整 timeout | 拒绝；必须继续同一 context |
| 25 | 两个 budget 都足以正常完成 | canonical Fact bytes/IDs 相同 |

Schema 修正阶段还需为 memory/artifact diagnostic、非成功 reported IDs 与原有 completed fixture 建立兼容
向量；运行阶段必须在 Python 3.10/3.13 的 normal/`-O` 下复验所有不依赖真实 wall-clock 的 deterministic
cases。真实 deadline/containment 机制另设最小 producer-side/worker-side proof，不能只靠 mock counter。

## 13. 实现分段与停止线

即使本合同最终冻结，也只能按以下顺序继续：

```text
A. DerivationEvidence Schema/corpus semantic correction
   - two typed budget diagnostics
   - non-success reported IDs empty
   - compatibility/conformance vectors
   ↓
B. budget primitive feasibility
   - one absolute monotonic deadline
   - pre-start process-tree memory containment
   - cancellation / cleanup / no residue
   ↓
C. Provider-binding and attempt kernel
   - explicit single binding
   - exact request provenance
   - no ambient discovery
   ↓
D. deterministic replaceable test Provider
   - candidate -> application canonical Fact
   - empty/failure/interrupt cases
   - bidirectional provenance
   ↓
E. non-published phase result hardening
```

每一项是独立停止线。A 没冻结不能开始 B；B 不能证明真实 primitive 就回合同；D 完成也不能开始真实
Python parser。Relation、Slice、Coverage、conflict/UNKNOWN、Manifest 与完整 repo end-to-end 继续保持禁止。

## 14. 候选验收与冻结序列

本文成为实现前冻结合同，至少需要：

1. 文档 136 的十三个反例逐项有唯一裁决；
2. `request_provenance` 不再依赖不存在的 branch history；
3. Provider applicability 不依赖 ambient installation 或 first-success；
4. Input acquisition budget 与 derivation execution budget 不形成双 authority；
5. wall/memory/artifact 三类终止语义已唯一，Evidence 认识论上限明确；
6. Provider candidate 与 canonical Fact authority 分离；
7. COMPLETE 与 DIAGNOSTIC file set 下的 `reported_*_ids` 语义均闭合；
8. phase result 与 Artifact/Manifest 身份分离；
9. fresh Agent 只读仓库即可说出 A–E 顺序和全部停止线；
10. docs-only 候选本地门、远端 required checks、受保护主线合入、exact-main 门与匿名公开读回成立；
11. 后继独立 docs-only 状态发布完成最后门。

合同冻结只允许 A 阶段的 Schema/corpus 修正，不直接授权 Provider runtime。Schema 修正自身冻结、budget
primitive feasibility 与后继明确实现授权仍须各自独立成立。

## 15. 当前候选裁决

当前状态只允许写成：

```text
R1_DERIVATION_PROVENANCE_PRECONTRACT_AUDITED
R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

不得写成：

```text
R1_DERIVATION_PROVENANCE_CONTRACT_FROZEN
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_ALLOWED
R1_FACTS_IMPLEMENTED
R1_DERIVATION_COMPLETE
```

本文没有证明真实 Provider、FactSet、DerivationEvidence、Relation、Slice、Coverage 或 Manifest 已存在；
它只把下一次合法施工前必须固定的 authority、identity、budget 与 provenance 边界变成可审查合同候选。
