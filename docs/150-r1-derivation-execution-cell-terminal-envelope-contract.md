# R1 Derivation Execution Cell / Terminal Envelope 最小合同 0.1

> 状态：`R1_DERIVATION_EXECUTION_CELL_PRECONTRACT_AUDITED /
> R1_DERIVATION_EXECUTION_CELL_CONTRACT_CANDIDATE /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@2de46c21997d85a437820decfeb2bd8bb7b69ee1`
>
> 前置审计：[R1 Derivation Execution Cell 与 Terminal Continuity 系统审计](149-r1-derivation-execution-cell-system-audit.md)
>
> 上游冻结输入：[R1 Derivation Attempt 与 Fact Provenance 最小运行合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)、
> [DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)、
> [R1 Derivation Budget Primitive 最小合同](145-r1-derivation-budget-primitive-contract.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文不创建或修改 runtime、Schema、corpus、identity vector、
> 测试、依赖、CI、Provider、parser、FactSet、DerivationEvidence、Relation、Slice、Coverage、Manifest、CLI、
> Workbench、Core、P/Q/D、tag 或 Release

## 1. 目的与停止线

冻结的 Budget Primitive 只拥有 process-tree containment、terminal-stop latch、phase completion checkpoint 与
cleanup release。它没有定义 Provider 与 application canonicalization 怎样共同进入受控 cell，也没有定义
request/result transport 怎样建立唯一、完整、可提交的 terminal phase result。

本文只冻结第一条 execution-cell 接缝：

```text
owned DerivationInputSet
+ opaque derivation_id
+ explicit closed test Provider binding
        ↓
provisional budget start + inactive cell preparation
        ↓
atomic attempt admission + ProviderRun start
        ↓
contained application worker
        ├─ Provider produces bounded candidates
        └─ application validates and canonicalizes Facts
        ↓
bounded single-terminal envelope
        ↓
controller-owned stop / release / commit checkpoint
        ↓
copy-owned phase result OR typed non-public failure
```

本文不授权：

```text
real Python parser
third-party Provider discovery or authorization
FactSet / DerivationEvidence / Manifest publication
Relation / conflict / UNKNOWN propagation
Slice / Coverage
cross-platform execution cell
hostile-code sandbox
CLI / Workbench / Core handoff
```

本合同冻结后也只能解除本节最小 test Provider/Fact phase 的实现门；不能把 execution cell 的存在外推成完整
R1 Derivation 已成立。

## 2. 五个对象不能再压成一个“worker run”

首版必须分别保存以下语义：

```text
Derivation Attempt
  caller-created request instance；后继完整 derivation 的生命周期所有者

BudgetContext
  sealed execution permission；从一个 monotonic t0 消费，不按 phase 刷新

Execution Cell
  本次受控 application worker process tree、transport 与 owned resources

ProviderRun
  针对 exact operands 的一次 Provider 运行坐标

Terminal Envelope
  worker 对本 phase 的唯一协议终态消息；不是公共 Artifact 或 Evidence
```

因此：

```text
cell process exited
  != ProviderRun completed
  != terminal envelope valid
  != resources released
  != phase result committed
  != derivation complete
```

Execution Cell 与 transport frame 不获得新的语义摘要、Artifact role 或公共 Schema identity。它们是一次 attempt
内部的运行对象；`fact_id / provider_run_id / derivation_evidence_digest` 继续按文档 120/137 的冻结投影计算。

## 3. Authority topology

### 3.1 trusted controller 位于 cell 外

controller 只拥有运行边界，不拥有源码事实解释权。它负责：

```text
validate and copy-own request, descriptor and safety limits
derive request provenance, operands_digest and provider_run_id
own monotonic/UTC clocks and cancellation observation
start the one BudgetContext and prepare the inactive cell
resolve the closed launch binding
frame and deliver exact request bytes
own terminal-stop latch and attempt eligibility
validate frame/protocol/continuity mechanically
observe process-tree and handle release
map terminal outcome to status/diagnostic-shaped values
commit or reject the phase result atomically
```

controller 不得：

```text
run Provider/parser outside containment
interpret Python source
repair or silently drop candidate output
canonicalize Fact identity after bytes leave the cell
infer memory/provider cause from exit code or stderr
turn process exit 0 into COMPLETED
```

### 3.2 application worker 位于受控 cell 内

application worker 是受信 VeriTrail application code，不是 Provider。它与 Provider/parser/candidate/canonical
staging 一起受同一个 process-tree memory hard ceiling 约束。它负责：

```text
strict request-envelope validation
exact input continuity validation
closed launch-binding resolution inside the application allow-list
Provider invocation
candidate shape / anchor / profile conformance
subject_key_digest and fact_id recomputation
application-owned provenance_refs and reported-ID summary
terminal envelope construction
```

因此 application-owned canonicalization 可以发生在 child worker 内；进程边界不把 canonical authority 转交给
Provider，也不要求 controller 在 hard memory boundary 外重新解释 candidate。

### 3.3 Provider 仍只拥有 bounded observation

Provider 只能通过文档 137 冻结的窄 protocol 返回 candidate observation 或受限 provider-local failure signal。
它不能提交：

```text
canonical Fact identity
ProviderRun started_at / finished_at
public execution_status
public diagnostic subject
reported_fact_ids / reported_relation_ids
DerivationEvidence or Manifest
```

Provider callable 返回成功只说明 candidate channel 正常返回；application validation、canonicalization、terminal
framing、resource closure 与 controller checkpoint 尚未完成时，仍无 `COMPLETED` phase result。

首版 invocation boundary 的 closed mapping 固定为：

```text
Provider returns a finite candidate sequence
  -> application validation/canonicalization

Provider raises application-defined ProviderUnavailableSignal
  -> PROVIDER_UNAVAILABLE terminal kind

any other exception crossing the exact Provider invocation boundary
  -> PROVIDER_FAILED terminal kind

exception before entering or after leaving that boundary in application worker code
  -> INTERNAL_DERIVATION_ERROR terminal kind
```

exception type只承担本机 protocol 分流，不进入 Artifact；exception message、traceback 与 Provider 自报字符串
全部丢弃，不得进入 terminal envelope 或公共 diagnostic。candidate sequence 必须先受 transport/memory 边界约束，
不能通过 generator 在 terminal commit 后继续隐式执行。

### 3.4 当前不是 hostile-code sandbox

controller、application worker 与首版 test Provider 都属于 trusted local product runtime。Job/process containment
只证明资源与生命周期边界，不隔离 filesystem、network、credential、native extension、module mutation 或恶意
Provider。第三方 Provider trust/authorization 与 hostile-code isolation 必须另开威胁模型，不能从本合同推导。

## 4. Preflight、budget start、cell preparation 与 admission

### 4.1 四个边界必须分开

```text
capability preflight
  != concrete cell prepared
  != derivation attempt admitted
  != ProviderRun started
```

仅能导入平台 binding 或检查 API 存在不证明本次 Job/port/pipe/worker 已建立。反过来，把具体准备放在 t0 前，
又会把真实 setup cost 移出 sealed wall-clock budget。

### 4.2 唯一合法顺序

首版顺序固定为：

```text
1. validate and copy-own DerivationInputSet, derivation_id,
   exact single descriptor, closed launch key and transport safety limits

2. derive exact request provenance; capture resolved_at

3. capture monotonic t0 and provisional UTC attempt_started_at
   execution_deadline = t0 + sealed wall_clock_ms
   create exactly one provisional BudgetContext

4. under that same deadline, prepare an inactive execution cell
   build the exact bounded request frame
   create inactive containment
   -> apply/read back hard limits
   -> associate observation surface
   -> create bounded request/result channels
   -> create application worker suspended
   -> assign worker to containment

5. final pre-admission checkpoint
   no stop observed
   deadline not crossed
   exact descriptor/request/binding continuity valid
   inactive cell and owned resources complete

6. atomically commit Derivation Attempt admission

7. capture provider_run_started_at in the controller,
   commit ProviderRun start, then immediately resume the contained worker
```

步骤 3 的 BudgetContext 在步骤 6 以前只提供**临时准备资格**，不构成一条已发布或可被 Evidence 描述的合法
Derivation Attempt。若步骤 3–5 失败，controller 必须撤销该资格、清理 provisional cell，并返回 admission
error；不得构造 ProviderRun、phase result 或 DerivationEvidence。

文档 145 中 primitive-local 的 `ADMITTED/RUNNING` 表达 BudgetContext 是否能够参与一次 atomic stop/completion
决策；它不自动等于本合同的 Derivation Attempt 已经 admission。组合以后必须同时满足 budget eligibility 与
attempt eligibility，不能拿其中一层替代另一层。

一旦步骤 6 成功，任何 resume/transport/worker/protocol failure 都属于 admitted attempt 的运行结果，不得退回
“从未开始”。`attempt_started_at` 仍等于步骤 3 的 UTC 时间，因此 setup 成本诚实地处于本次 execution
window 内；`provider_run_started_at` 不得早于 attempt admission。

时间顺序固定为：

```text
resolved_at
  <= attempt_started_at (paired with monotonic t0)
  <= provider_run_started_at
  <= provider_run_finished_at
  <= phase_finished_at
```

UTC 只记录 provenance；全部 deadline/remaining 计算继续只使用同一个 monotonic t0。

### 4.3 pre-admission error 不冒充 Evidence

步骤 6 以前的失败只返回调用层 typed error：

| 条件 | error code | ProviderRun / Evidence |
| --- | --- | --- |
| request、ID、safety-limit 形状非法 | `INVALID_DERIVATION_ATTEMPT_REQUEST` | 不存在 |
| descriptor 与 closed launch key 不一一对应 | `PROVIDER_BINDING_MISMATCH` | 不存在 |
| 所需平台 capability/containment 无法建立 | `DERIVATION_RUNTIME_UNAVAILABLE` | 不存在 |
| exact request frame 超出 application-owned request cap | `DERIVATION_TRANSPORT_LIMIT_INSUFFICIENT` | 不存在 |
| preparation 期间 deadline 已到 | `DERIVATION_ADMISSION_DEADLINE` | 不存在 |
| preparation 期间 caller cancellation | `DERIVATION_ADMISSION_CANCELLED` | 不存在 |
| 其他 preparation/controller invariant 失败 | `INTERNAL_DERIVATION_ADMISSION_ERROR` | 不存在 |

这些 code 只允许固定说明，不携带绝对路径、源码、stack trace 或 locale 文本。它们不是
`DerivationEvidence.diagnostic_code`，也不能被后来“升级”为一次已经运行的 Provider 事实。

## 5. Closed launch binding

文档 137 的 `implementation handle` 在本切片收窄为 application-owned closed launch binding：

```text
ProviderBinding
  ├─ frozen public descriptor
  └─ local launch_key

application runtime
  launch_key -> one compiled/registered test implementation
```

要求：

1. `launch_key` 只来自本版本 application worker 的闭合 allow-list；
2. 每个 key 与一个 exact descriptor 一一对应，admission 和 worker 两端都验证该映射；
3. key 是 operation binding，不进入 ReviewPolicy、Provider operands、Fact identity 或 Artifact；
4. worker 不根据 module string、file path、entry point、`sys.path`、editable install、虚拟环境或当前安装包扫描
   implementation；
5. 不允许 pickle/cloudpickle 或其他可执行 object serialization 穿过边界；
6. 至少两个确定性 test Provider 能对同一 owned input 产生同一规范 candidate，以证明替换实现不改 Fact identity。

`launch_key` 作为 process-start 时的 application-owned operational input 交给 worker，不进入第 7 节规范 request
envelope；worker 只能用它索引自身闭合 allow-list，并必须确认解析出的 descriptor 与 request envelope 中的 exact
descriptor 相同。transport safety limits 使用同一类非语义 start configuration 交付，不能从 Provider output 或
ambient environment 读取。controller 与 worker 都必须先把它们限制在 product-owned finite hard cap 内，再允许
任何 frame allocation；外部调用方不能通过提交任意大上限解除该 cap。

descriptor echo/复算只证明本次 protocol continuity，不证明代码签名、第三方信任或未来 Provider registry 已成立。

## 6. 内部 framing 与 safety limits

### 6.1 两条单向 channel

首版使用两个 application-owned 单向 byte channel：

```text
controller -> worker : exactly one request frame
worker -> controller : exactly one terminal frame
```

它们可以由平台安全映射为 stdin/stdout 或专用 inherited pipe，但被选作 protocol channel 后只能承载本合同
字节。日志、progress、traceback 或 Provider `print` 不得混入；stderr 不是规范结果来源，也不能被解析为终止原因。

不得使用 shared temporary result path、unverified reread、pickle、ambient socket server 或多消息 progress protocol
替代这两条 channel。

### 6.2 exact frame

每个 frame 固定为：

```text
8-byte unsigned big-endian payload length N
N bytes canonical_json_bytes(document)
immediate EOF
```

规则：

- `N >= 1`；
- request 与 terminal payload 分别受 copy-owned `request_payload_bytes`、`terminal_payload_bytes` inclusive 上限；
- controller/worker 在完整分配 payload 前先检查 declared length；
- payload 必须 strict UTF-8、恰为一个 JSON object，且重新规范化后的字节与原 payload 完全相同；
- header/body 截断、EOF 过早、第二个 frame、重复 envelope、尾随 byte、BOM、LF、CRLF 或非规范 JSON 全部拒绝；
- 成功读取 terminal payload 后也必须继续确认 EOF；“第一个对象可解析”不等于 channel 完整。

`ExecutionCellTransportSafetyLimits` 是 application-owned、preflight 时 copy-owned 的闭合运行对象：

```text
request_payload_bytes  PositiveInteger
terminal_payload_bytes PositiveInteger
```

二者分别约束 payload `N`，不包含固定 8-byte header。它们：

```text
control whether this attempt can finish
do not consume artifact_bytes
do not enter request provenance, Provider operands, Fact identity or Evidence identity
do not permit partial acceptance when exhausted
```

任何超限都 fail closed。若两个 safety-limit 组合均充分且其余语义输入相同，它们必须生成相同的
provenance-free canonical Fact content projection 与 `fact_id`；实现不得把 limit 写入 candidate 或规范 Fact。
不同 attempt 的 `provenance_refs` 可以且应当随各自 `provider_run_id` 变化，因此不要求完整 Fact object bytes
跨 attempt 相同。

## 7. Request envelope

request payload 顶层只允许：

```text
protocol = "veritrail-review-derivation-cell/0.1"
message_kind = "DERIVATION_CELL_REQUEST"
derivation_id
request_provenance
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
provider_descriptor
operands_digest
source_snapshot
review_policy
derivation_profile
source_blobs[]
```

`source_snapshot / review_policy / derivation_profile / source_blobs[]` 是 `DerivationInputSet` 已验证内容的一次
copy-owned transport projection。每个 blob 项固定包含：

```text
git_path
size_bytes
content_sha256
content_base64
```

`source_blobs` 按冻结 Git path 顺序排列；`content_base64` 使用 RFC 4648 standard alphabet、带规范 padding，解码后
必须与 Snapshot inventory 的 size/digest 完全一致。worker 必须重新验证三份文档的 canonical bytes、semantic
digest、cross-reference 与 exact blob continuity；不能只信 controller 声明的摘要。

request envelope 是内部 transport value，不是第四份输入 Artifact。它不获得 self-digest，也不进入 Manifest。
controller 的 mechanical serialization 不拥有源码解释权；传入 worker 后形成的 copy 与解码/validation 内存全部
处于 execution-cell hard memory ceiling 内。

## 8. Terminal envelope

### 8.1 exact shape

terminal payload 顶层只允许：

```text
protocol = "veritrail-review-derivation-cell/0.1"
message_kind = "DERIVATION_CELL_TERMINAL"
derivation_id
provider_descriptor
operands_digest
provider_run_id
terminal_kind
canonical_facts[]
reported_fact_ids[]
reported_relation_ids[]
```

`terminal_kind` 闭集：

```text
COMPLETED
PROVIDER_UNAVAILABLE
PROVIDER_FAILED
NONCONFORMANT_PROVIDER_OUTPUT
INTERNAL_DERIVATION_ERROR
```

规则：

- `COMPLETED` 才允许非空 `canonical_facts/reported_fact_ids`；成功空输出仍合法；
- 其他 kind 的三个 reported/canonical 数组必须全部为空；
- `reported_relation_ids` 在本切片永远为空；
- `reported_fact_ids` 必须等于 application worker 规范 Facts 的排序唯一 `fact_id`；
- 每个 Fact 的 `provenance_refs` 必须恰为 `[provider_run_id]`；
- descriptor、operands、run ID 与 request 必须完全连续；
- terminal payload 不包含时间、公共 execution status、自由文本、stack trace、本机路径或 Provider 自报资源原因。

Provider exception、unavailability 或 bad candidate 只有经过 application worker 的 closed mapping 后才能成为相应
terminal kind。Provider 自己写出的同名字符串不具有 authority。

### 8.2 envelope 仍不是 phase completion

合法 terminal envelope 只是一项 commit candidate。controller 仍必须确认：

```text
no positive stop won the latch
monotonic now <= execution deadline
frame/protocol/continuity valid
worker/process tree and phase-owned channels/handles are closed
attempt eligibility remains admitted
```

然后才能与 Budget Primitive 共用同一个原子 checkpoint 提交 `COMPLETED_FOR_PHASE` 或 copy-owned non-success
phase result。terminal envelope 已到但资源未闭合时不得先提交；deadline 可以在等待闭合期间赢得 stop latch。

## 9. Mechanical outcome mapping

controller 只按正向 observation 和已验证 envelope 映射，不读 stderr 猜原因：

| observation | Provider Run | phase | diagnostic-shaped value |
| --- | --- | --- | --- |
| deadline latch wins | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_DEADLINE` |
| cancellation latch wins | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_CANCELLED` |
| positive owned memory event wins | `INTERRUPTED` | `INTERRUPTED` | `EXECUTION_MEMORY_BUDGET` |
| valid `COMPLETED` envelope + closed resources + commit wins | `COMPLETED` | `COMPLETED` | none |
| valid `PROVIDER_UNAVAILABLE` envelope | `UNAVAILABLE` | `UNAVAILABLE` | `PROVIDER_UNAVAILABLE` |
| valid `PROVIDER_FAILED` envelope | `FAILED` | `FAILED` | `PROVIDER_FAILED` |
| valid `NONCONFORMANT_PROVIDER_OUTPUT` envelope | `FAILED` | `FAILED` | `NONCONFORMANT_PROVIDER_OUTPUT` |
| valid `INTERNAL_DERIVATION_ERROR` envelope | `FAILED` | `FAILED` | `INTERNAL_DERIVATION_ERROR` |
| no/partial/duplicate/trailing/noncanonical/unknown envelope | `FAILED` | `FAILED` | `INTERNAL_DERIVATION_ERROR` |
| resume/transport/worker termination without narrower positive warrant | `FAILED` | `FAILED` | `INTERNAL_DERIVATION_ERROR` |

若 whole-phase stop 与 terminal envelope 竞争，冻结 terminal-stop latch 和 completion checkpoint 决定唯一结果；
late envelope 不恢复成功。memory hard limit active、worker OOM 文本、非零 exit、`STATUS_NO_MEMORY` 或异常结束
都不能单独产生 `EXECUTION_MEMORY_BUDGET`。没有合法 Provider exception envelope 时，也不能构造
`PROVIDER_FAILED`。

transport/protocol/application continuity failure 使用 `INTERNAL_DERIVATION_ERROR`，不表示已确定故障发生在
controller、OS、worker、Provider 或某个具体函数。它只声明：

> 一个已开始的 owned ProviderRun 没有建立可提交的合法 terminal phase result，且没有更窄的正向 warrant。

这一语义是 epistemic fallback，不是 catch-all 便利分支；已知 deadline、cancellation、positive memory、
Provider unavailable/exception 或 nonconformant candidate 必须使用各自更窄映射。

## 10. `DerivationEvidence 0.1.1` 不升级

本反例不要求新 Schema revision：

1. `INTERNAL_DERIVATION_ERROR` 已是 `0.1/0.1.1` 冻结闭集成员；
2. 现有 Schema 已允许它绑定 `PROVIDER_RUN` subject；
3. 这里没有发现一个可被稳定正向观察、值得获得新公共名称的根因；
4. 新增 `WORKER_EXITED` 或 `TRANSPORT_FAILED` 会把运行位置/机制误写成已知因果，并扩大公共 ontology。

未来 Evidence assembler 若消费本 phase result，admission 后的上述 fallback 必须使用：

```text
diagnostic_code = INTERNAL_DERIVATION_ERROR
subject_ref = {ref_kind: PROVIDER_RUN, provider_run_id: <exact run>}
```

admission 前失败没有 ProviderRun，也没有 DerivationEvidence，因此不需要 `subject_ref=null` 的伪记录。本合同不
新增字段、不改 digest projection、不改 `0.1.1` Schema bytes/corpus，也不声称当前 phase 已发布 Evidence。

文档 137 中的“unknown application fault”应按本合同精确理解为“unknown application/runtime continuity
fault after ProviderRun start”；它不能被解释为已证明 application code 是平台根因。

## 11. 不可恢复的 attempt eligibility revocation

### 11.1 controller-owned eligibility gate

Budget Primitive 的 `BudgetContext` 不单独拥有 attempt-level protocol failure。后继 controller 必须把 raw
context 封装在不可绕过的 eligibility gate 内：

```text
PROVISIONAL
   ├─ preparation succeeds -> ADMITTED
   └─ any preparation failure -> REVOKED

ADMITTED
   ├─ successful phase commit -> remains ADMITTED for future phase
   └─ stop / non-success / primitive / protocol / cleanup failure -> REVOKED

REVOKED -> no transition back
```

raw `BudgetContext` 不得从 controller API 泄露给 Provider、worker 或调用方。所有 start、receive、canonical
result acceptance、`try_complete_phase` 与 future-phase admission 都必须先经过 eligibility gate。这样即使底层
context 在 primitive exception 后机械状态仍为 `RUNNING`，它也不再拥有可达的成功提交路径。

### 11.2 revocation 与 release outcome 分离

`REVOKED` 只说明执行资格已永久撤销，不说明资源已释放。controller 必须再使用唯一 cleanup-only envelope：

```text
revocation
  -> stop/terminate owned cell as needed
  -> drain bounded channels
  -> observe tree zero
  -> close owned handles/threads
  -> remove owned staging if any
  -> RELEASED | RELEASE_FAILED
```

协议/primitive failure 触发的 revocation 不得伪造 Budget stop diagnostic；cleanup envelope 不得执行任何
Artifact staging，cleanup 成功也不能把 normal eligibility 从 `REVOKED` 恢复为 `ADMITTED`。若已经有正向
stop latch，原 stop reason 保持不变；后到的 protocol/exit signal 只能作为非规范运行诊断，不能改写公共原因。
有合法 phase result、且没有预算 stop 的 execution-cell non-success 在 release 成功后是否获得独立
DIAGNOSTIC closure eligibility，由
[文档 155](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)另行收窄；它不是本 gate 的恢复转换。

`RELEASE_FAILED` 是 typed controller failure 和 conformance-gate failure。它禁止 phase result commit、任何
R1 Artifact（包括 DIAGNOSTIC）发布与继续执行；现有公共 Evidence 不能证明资源已闭合，因此本切片不为它伪造
`INTERNAL_DERIVATION_ERROR` Artifact。成功 release 是返回任何 terminal phase result 的必要条件。

retry 必须使用新 `derivation_id`、重新 copy-own binding、建立新 BudgetContext 与新 execution cell。不得复用
partial request/result buffer、worker、ProviderRun 或被 revoke 的 context。

## 12. 时间、状态与 summary ownership

controller/application 的最终 ownership 固定为：

```text
controller clock observations
  -> attempt/run started_at and finished_at

validated terminal kind + positive stop observations
  -> ProviderRun / phase status

controller mapping
  -> diagnostic code and subject_ref

application canonical Facts, accepted by controller continuity check
  -> reported_fact_ids
```

Provider/worker envelope 不携带 UTC 时间。`provider_run_finished_at` 在 controller 建立 terminal classification
时捕获，不能从 worker 自报；`phase_finished_at` 只在 resource release 与 final controller checkpoint 结束后
捕获。两者都可以晚于 execution deadline，但不恢复 deadline 后的结果资格。phase result 必须是新建
copy-owned value；不得把 terminal envelope mapping 原地交给后继 assembler 修改。

非 `COMPLETED` phase 的 Facts 与 reported IDs 必须为空。成功 Fact value 一经 phase commit，后继 phase 消费同一
owned value，不重新读取 channel、临时路径或 Provider state。

## 13. Safety limit 与预算不进入 Fact identity

对相同 owned Snapshot、Profile、descriptor 与规范 observation，若两个 execution/transport safety profile 都
足以让 phase 正常提交：

```text
budget/safety A != budget/safety B
Complete(A) AND Complete(B)
  -> provenance-free canonical Fact content projections are byte-identical
  -> subject_key_digest(A) = subject_key_digest(B)
  -> fact_id(A) = fact_id(B)
```

attempt/run/Evidence identity 仍可因新的 `derivation_id`、Provider descriptor 或时间而不同；完整 Fact object 的
`provenance_refs` 也必须诚实绑定各自 run。这里不要求完整 Fact 或 phase result bytes 相同，因为运行 provenance
本来不同；只禁止 runtime safety input 污染规范源码事实。

预算或 transport 上限不足时可以得到 admission error、`INTERRUPTED` 或 `FAILED`，但不得输出“在较小上限下
观察到的部分 FactSet”。

## 14. Phase result 与公共 Artifact 的边界

本切片返回的 copy-owned phase result 至少包含：

```text
derivation_id
request_provenance
input semantic digests
admitted provider descriptor
operands_digest / provider_run_id
controller-owned run timing and terminal status
typed diagnostic-shaped values
canonical Facts, only when COMPLETED
reported IDs, only when COMPLETED
release outcome
```

它不是：

```text
FactSet
DerivationEvidence
R1_DERIVATION Manifest
Coverage proof
Core Evidence
Verdict
```

不得把 standalone test phase result 事后包装成 Bundle。后继完整 assembler 必须在同一 BudgetContext 下继续
Relation/Slice/Coverage、artifact reservation、canonical publication 与 Manifest closure，并重新验证所有
cross-reference；这些合同尚未开始。

## 15. 最小 conformance matrix

| ID | 单变量义务 | 预期 |
| --- | --- | --- |
| EC-001 | preflight 后开始 t0，再准备 inactive cell | setup 成本处于 absolute budget 内 |
| EC-002 | concrete preparation 失败 | 无 attempt/run/Evidence；eligibility revoke；zero residue |
| EC-003 | preparation 期间 deadline/cancel | typed admission error；无伪 stop Evidence |
| EC-004 | suspended worker 未 assign 到 hard containment | 不得 resume/admit |
| EC-005 | attempt admitted 后 resume 失败 | FAILED / INTERNAL fallback；若 release 成功才返回 phase result |
| EC-006 | exact request payload exceeds cap during preparation | `DERIVATION_TRANSPORT_LIMIT_INSUFFICIENT`；无 attempt/run |
| EC-006a | admitted worker observes partial/noncanonical request transport | FAILED / INTERNAL；无 Fact |
| EC-007 | ambient module string/entry-point Provider | binding rejection before execution |
| EC-008 | two closed test Providers, same normalized observation | same provenance-free Fact content/ID；provenance binds each run |
| EC-009 | Provider success, valid empty result | COMPLETED run + empty Facts/IDs |
| EC-010 | positive Provider exception envelope | FAILED / PROVIDER_FAILED |
| EC-011 | positive Provider unavailable envelope | UNAVAILABLE / PROVIDER_UNAVAILABLE |
| EC-012 | bad candidate caught by application worker | FAILED / NONCONFORMANT_PROVIDER_OUTPUT |
| EC-013 | worker exits 0 without terminal envelope | FAILED / INTERNAL；不是 COMPLETED |
| EC-014 | abnormal exit/OOM text without positive memory event | FAILED / INTERNAL；禁止 memory/provider cause |
| EC-015 | partial/duplicate/trailing terminal bytes | FAILED / INTERNAL；无 partial acceptance |
| EC-016 | valid terminal envelope but tree/handle not closed by deadline | deadline stop；禁止 success commit |
| EC-017 | deadline/cancel/memory latch races with envelope | one atomic winner；late envelope cannot restore success |
| EC-018 | primitive/protocol failure, raw BudgetContext still mechanically RUNNING | controller eligibility已撤销；later completion impossible |
| EC-019 | cleanup succeeds after revocation | context remains revoked |
| EC-020 | cleanup misses shared release deadline | RELEASE_FAILED；no phase result/normal Artifact |
| EC-021 | Provider self-reports time/status/reported IDs | ignored/rejected；controller/application own summary |
| EC-022 | two sufficient transport limits / budgets | provenance-free Fact content projection and IDs identical |
| EC-023 | non-COMPLETED terminal path contains Fact/reported ID | conformance rejection |
| EC-024 | retry after any non-success | new derivation/binding/context/cell; no hidden resume state |

测试必须在当前 worktree 的 exact source/import coordinate 下运行。清 `sys.modules` 不能模拟 fresh interpreter；
需要 fresh-process dependency/binding 证明时使用独立 subprocess。

## 16. 实现分段与停止线

本合同只有在候选远端门、受保护主线合入、exact-main 门、fresh anonymous public readback 与独立 docs-only
冻结发布全部成立后，才允许按顺序施工：

```text
A. attempt eligibility + provisional admission correction
B. bounded request/result frame codec
C. contained application worker + closed launch binding
D. terminal mapping + context revocation/release
E. deterministic test Provider + EC-001..024
F. copy-owned phase result continuity
```

每段只能证明本合同边界。不得在 E 中使用真实 `ast.parse`，不得在 F 中写 FactSet/Evidence/Manifest，也不得
提前创建 Relation/Slice/Coverage 占位对象。

若实现探针证明 chosen framing、pre-start containment、process handle delivery 或 result closure 无法按本文机制
成立，必须停止并重开被反例击穿的最小条款；不得降级为临时文件、in-process Provider、post-hoc memory check
或“进程退出即成功”。

## 17. 候选验收门

本文只有满足以下条件后才有资格冻结：

1. 与文档 120、137、140、145、148、149 的 identity/authority/stop semantics 全局一致；
2. controller、application worker、Provider 三层 authority 不依赖进程位置猜测；
3. preflight、t0、cell preparation、attempt admission 与 ProviderRun start 只有一个顺序；
4. partial/duplicate/trailing/oversize/no-envelope 都没有成功或 partial-Fact 路径；
5. protocol/primitive failure 后 raw BudgetContext 不再有可达的 completion path；
6. positive stop、Provider-local failure与 epistemic fallback 不互相冒充；
7. `DerivationEvidence 0.1.1` 不变决定有 Schema/corpus 与认识论边界支撑；
8. sufficient safety-limit/budget invariance 不把 runtime profile写入 Fact identity；
9. diff 只有本文、必要的冻结合同一致性修正与状态入口文档；
10. 原始远端门、受保护主线、exact-main 门、匿名正/负 marker 读回和独立状态发布全部成立。

门禁全绿不能覆盖新的组合反例。发现问题不自动要求扩大合同；只有击穿当前不变量或使两份冻结文本无法同时
满足的反例，才允许最小重开。

## 18. 当前候选事实与 Fresh-Agent 交接

本文只裁决了审计 149 的 execution-cell/terminal-envelope 接缝。当前状态是：

```text
Frozen:
  SourceSnapshot
  DerivationInputSet
  DerivationEvidence 0.1.1 correction
  Derivation Budget Primitive

Candidate only:
  Derivation Execution Cell / Terminal Envelope Contract 0.1

Not implemented:
  execution-cell Provider/Fact phase

Still forbidden:
  real parser
  FactSet / DerivationEvidence publication
  Relation / conflict / UNKNOWN propagation
  Slice / Coverage
  COMPLETE or DIAGNOSTIC runtime Manifest
  CLI / Workbench / Core handoff
```

一个没有聊天上下文的新 Agent 只读仓库时，应当先审本文与上游冻结文本能否同时成立；不得把 `CONTRACT_CANDIDATE`
读成 runtime authorization，也不得因为现有 Schema 能表达 `INTERNAL_DERIVATION_ERROR` 就宣称 execution cell 已实现。

## 19. 本地候选证据

docs-only 候选在 exact worktree source/test coordinate 下完成：

```text
relative Markdown links       PASS
git diff --check              PASS
runtime/schema/corpus diff    empty

Budget + Boundary regression
  CPython 3.10 normal         27/27
  CPython 3.10 -O             27/27
  CPython 3.13 normal         27/27
  CPython 3.13 -O             27/27

DerivationEvidence 0.1.1 correction regression
  CPython 3.10 normal          5/5
  CPython 3.10 -O              5/5
  CPython 3.13 normal          5/5
  CPython 3.13 -O              5/5
```

另有一次不落盘的内存 specimen 将冻结 correction corpus 的 memory-interrupted Evidence 单变量改成
`FAILED / INTERNAL_DERIVATION_ERROR / PROVIDER_RUN subject / empty reported IDs`，复算
`derivation_evidence_digest=8ad1343f69fe4ca60b9385ce7c71d9d15220d10641fb4534d4947b9e44b28d96`；现有
`0.1.1` Schema 与 correction conformance validator 均接受。该探针只证明现有公共形状足以承载本文的
epistemic fallback，不把临时 specimen 变成冻结 corpus，也不证明后继 runtime mapping 已实现。
