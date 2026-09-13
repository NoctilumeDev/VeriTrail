# R1 Derivation Execution Cell 与 Terminal Continuity 系统审计

> 状态：`R1_DERIVATION_EXECUTION_CELL_PRECONTRACT_AUDITED /
> R1_DERIVATION_EXECUTION_CELL_CONTRACT_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@c33aeac9fa198bd8a0b9b5dc8340372757ba04b7`
>
> 上游冻结事实：[R1 Derivation Budget Primitive 实现冻结发布](148-r1-derivation-budget-primitive-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L0_DOCUMENTATION`；本文不修改 Schema、corpus、identity vector、
> runtime、测试、依赖、CI、Provider、parser、Fact、Relation、Slice、Coverage、Manifest、CLI、Workbench、
> Core、P/Q/D、tag 或 Release

## 1. 审计问题

Budget Primitive 已经证明绝对 deadline、Windows Job memory containment、正向 memory attribution、单一
terminal-stop latch、cleanup-only release envelope 与 artifact reservation 可以分别成立。它没有承诺怎样
把 Provider、application-owned canonicalization、terminal result transport 与未来 ProviderRun/Fact
provenance 接到这个 primitive 上。

本轮因此不问 Relation、Slice、Coverage 或完整 Derivation 怎样实现，只问：

> 在允许 Derivation Attempt / Provider Run / canonical Fact runtime 施工以前，受控 execution cell、结果
> 连续性、失败归因与 context 终止还有哪些组合语义没有资格交给代码决定？

审计只使用仓库内冻结合同、公共 Schema、exact-main runtime 与一次不落盘的确定性 failure-injection probe。
聊天草稿、实现便利和未来产品设想不构成规范输入。

## 2. 冻结输入没有漂移

审计基线上的关键字节为：

```text
docs/137-r1-derivation-attempt-and-fact-provenance-contract.md
SHA-256 91cf8ee1ddade04433eb28c9b834886aee79ee8316893b211d633876f4bc5742

docs/140-r1-derivation-evidence-schema-correction-contract.md
SHA-256 95dc176ac312da99831c0dc12dbdd4c291634dd8026e0647ea96f47d848a3bca

docs/145-r1-derivation-budget-primitive-contract.md
SHA-256 9a7f4c470ca4b3869c3600e6e4dedd2ebd02c15257cdece428b15032f88ea9f5

docs/148-r1-derivation-budget-primitive-freeze-publication.md
SHA-256 97816cec59b16eb9ec70c16cd33e28f217bf27e4b265d7852a1a3e3e6c95f64b

schemas/review-policy-0.1.schema.json
SHA-256 101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f

schemas/review-derivation-evidence-0.1.1.schema.json
SHA-256 a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045

schemas/review-fact-set-0.1.schema.json
SHA-256 e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1

plugins/review-attention/src/veritrail_review/budget.py
SHA-256 df20e3cd8a5299146ad2128c468afcc6057747540ea640ee96232f4957231b6b

plugins/review-attention/src/veritrail_review/_windows_budget.py
SHA-256 c452552f478ce24ff2403715faf2d45f374de31a6adc74beb4b174666ff0277b
```

这些输入继续保持：

- `DerivationInputSet` 是已验证、copy-owned 的 exact input；
- `derivation_id` 是 caller-created attempt identity，不是语义摘要；
- `ProviderBinding` 必须显式给出，不从 ambient installation 推断；
- Provider 只拥有 bounded observation，application 拥有 conformance 与 canonical Fact identity；
- whole attempt 只消费一个 `BudgetContext`；
- 非成功 run 或非成功 overall Evidence 的 `reported_*_ids` 必须为空；
- Fact phase result 不是 FactSet、DerivationEvidence 或 Manifest。

本轮没有发现需要推翻上述上位模型的反例。

## 3. 当前可组合边界

现有 runtime 的真实形状是：

```text
DerivationInputSet
        ↓
admit_derivation_budget(...)
        ↓
BudgetContext in trusted controller process
        ↓
_run_owned_process_cell(...)
        ↓
Windows Job-contained child process tree
        ↓
WindowsExecutionObservation
```

`_run_owned_process_cell(...)` 明确只管理 process cell，不解释 result transport。它接收 executable/arguments，
返回 containment、stop、tree-zero 与 handle-release observation；它没有 Provider request/result envelope、
candidate channel、canonical Fact value 或 terminal ProviderRun summary。

这不是 Budget Primitive 的缺陷。它正是该冻结 primitive 的停止线。但它意味着文档 137 的 C–E 阶段还不能
通过“把一个 Provider callable 塞进去”直接施工。

## 4. 系统审计发现

### 4.1 hard memory containment 与 application-owned canonicalization 尚未落在同一执行拓扑

冻结合同同时要求：

```text
memory_bytes
  covers worker runtime + Provider + parser + candidate + canonical staging

Provider
  owns bounded observation

application
  validates candidate and owns canonical Fact identity
```

三个直觉实现都不闭合：

```text
Provider callable 在 controller 进程运行
  -> Provider/parser/candidate 不在 Job hard ceiling 内

Provider 在 child，candidate 回 controller 后再 canonicalize
  -> candidate copy 与 application canonicalization 逃出 execution-cell memory boundary

Provider 在 child 直接返回完整 Fact
  -> Provider 越权取得 canonical identity
```

因此下一合同必须先明确：哪些 application-owned validation/canonicalization 代码在受控 cell 内执行，trusted
controller 在 cell 外只拥有哪一层 admission、latch、transport validation 与 result commit 权。进程边界不能
被误作 authority 边界；application 代码可以位于 worker，但 Provider candidate 不能绕过它直接取得 Fact
authority。

这是 **Freeze blocker**。在执行拓扑闭合以前直接实现 Provider/Fact，会在 memory containment 与 canonical
authority 之间任选其一失真。

### 4.2 result transport 仍没有完整性、边界与唯一终态语义

现有 process-cell primitive 没有定义：

```text
exact request bytes 怎样进入 child
candidate / canonical result 怎样返回
partial frame / duplicate frame / trailing bytes 怎样处理
normal exit without terminal envelope 怎样处理
terminal envelope arrived but resource closure failed 怎样处理
transport bytes 由什么非语义 safety limit 约束
```

stdout 文本、临时文件或 Python object serialization 都不能被实现自行默认为合同。它们分别会引入 framing、
路径/TOCTOU、ambient import、代码执行或部分结果误接纳问题。

下一合同必须定义一个 bounded、copy-owned、单终态的内部 envelope。transport safety limit 只控制本次尝试能否
完成，不得进入 Fact identity；两个不同但都充分的 transport limit 必须产生相同 canonical Facts。

这是 **Freeze blocker**。`Process exited 0`、`bytes arrived` 与 `valid terminal phase result committed` 不是同一事实。

### 4.3 primitive 异常以后，BudgetContext 当前仍可继续授予成功资格

文档 147/148 已把 primitive 异常后的 context discard/invalidation 明确留给后继 Provider attempt。exact-main
确定性 failure injection 证实这个接缝真实存在：

```text
module
  = exact audit worktree veritrail_review

injected primitive failure
  = PLATFORM_CAPABILITY_UNAVAILABLE

BudgetContext after failure
  state = RUNNING
  stop_trigger = null

subsequent try_complete_phase(..., resources_closed=true)
  = allowed
```

该探针没有修改仓库文件，也不把测试注入解释成真实平台故障。它只证明：当前 primitive 不拥有 attempt-level
discard 权；如果后继 controller 漏做失效处理，同一 context 可以在已知 execution-cell failure 后继续提交成功。

因此下一合同必须定义一个不可恢复的 context invalidation/discard transition，并明确：

- 哪些 setup、transport、protocol 或 cleanup failure 触发它；
- invalidated context 不能启动 worker、接纳 candidate、canonicalize、commit phase 或进入后继 phase；
- invalidation 与 cleanup outcome 分离，不能因 residue 已清理而恢复 execution eligibility；
- retry 必须创建新 `derivation_id`、新 binding 与新 BudgetContext。

这是 **Freeze blocker**，不是对已冻结 primitive 的追溯否定。上游主动没有拥有这层状态；现在必须由 attempt
controller 接住。

### 4.4 未归因 execution-cell termination 没有已冻结的公共映射

Budget Primitive 已冻结：hard memory ceiling 可以成立，而 Job memory message 不保证到达。若 child 在没有合法
terminal envelope、没有 deadline/cancellation latch、也没有 positive memory event 时终止，当前证据只允许说：

> owned execution cell terminated before a valid phase result was established; the cause was not positively observed.

现有公共 diagnostic 都不能自动承担这句话：

```text
EXECUTION_MEMORY_BUDGET
  -> 需要 positive owned memory event

PROVIDER_FAILED
  -> 需要 Provider execution exception 的正向边界

PROVIDER_UNAVAILABLE
  -> 不是已开始 cell 的无解释终止

INTERNAL_DERIVATION_ERROR
  -> 文档 137 当前只把它分配给 unknown application fault
```

把异常退出、OOM 文本或 active hard ceiling 反推为 memory/provider cause 都被上游明确禁止。下一合同必须先
裁决：现有 `INTERNAL_DERIVATION_ERROR` 是否被精确定义为不声明根因的 epistemic fallback，还是需要新的
自描述 Evidence Schema revision 与 typed diagnostic。审计阶段不替该合同预选 Schema 方案。

这是 **Freeze blocker**。失败可以未知，但不能无合法表达，也不能借最接近的 enum 编造原因。

### 4.5 attempt admission 与具体 cell preparation 还不是一个原子边界

文档 137 要求无法建立 memory containment 时在 admission 前 fail closed。当前公共组合先创建带 absolute `t0`
的 `BudgetContext`，具体 inactive Job、limit readback、completion port、suspended child 与 assignment 则由后续
process-cell 调用建立。

因此需要明确区分：

```text
capability preflight
  != concrete execution-cell preparation
  != derivation attempt admitted
  != Provider run started
```

仅检查 `pywin32` 可导入不能证明本次 Job/port/process cell 已经建立；反过来，若在 `t0` 以前做无界具体准备，
又会把真实 setup 成本藏在 execution budget 之外。下一合同必须冻结准备顺序、预算起点、失败归属和清理责任，
不能让函数调用顺序替 admission 语义作答。

这是 **Freeze blocker**，与 4.3 的 context invalidation 共同形成 attempt atomicity 问题。

### 4.6 `implementation handle` 尚不是可跨 process boundary 的稳定操作数

文档 137 冻结了 Provider descriptor，并把 `implementation handle` 留作非 Artifact 的调用能力。这足以排除
ambient discovery，但没有说明一个 Python object/callable 怎样进入新进程，也没有授权 pickle、module string、
editable install 或 `sys.path` 成为运行身份。

首个测试 Provider 需要一个 application-owned、closed-world launch binding：controller 冻结 descriptor 与
本次 operation binding，worker 只能解析由该 runtime 明确提供的测试 implementation，不扫描环境。descriptor
echo/复算可以证明协议连续性，但不能被宣传成第三方 Provider trust 或代码签名。

这是下一合同的 **Implementation gate**。真实 parser、第三方 Provider authorization/registry 与恶意代码沙箱
继续延期，不因测试 Provider 的 launch binding 获得授权。

### 4.7 run 时间与 terminal summary 必须由 controller/application 拥有

Provider candidate 的冻结闭集不包含 `started_at / finished_at / status / diagnostics / reported_*_ids`，因此这些
值不能从 Provider 自报文本盲拷贝。下一合同应明确 controller/application 的 observation 与 commit boundary
拥有时间、terminal status、diagnostic 映射和 canonical reported-ID summary；Provider 只报告 candidate 或
一个受验证的 provider-local failure signal。

这是 **Implementation gate**，不要求改 Fact identity 或公共时间字段。

## 5. 已审计但当前不改的边界

### 5.1 completed run 与 non-completed overall 的 reported IDs 已经分层

`ProviderRun.execution_status` 保存运行历史；`reported_*_ids` 保存本份 Evidence 能解析到正式 Artifact 的
canonical identity summary。完整 derivation 后继中断时可以保留较早 run 的 `COMPLETED`，但 DIAGNOSTIC
Evidence 必须清空所有 reported IDs。该规则已由 `DerivationEvidence 0.1.1` 与 correction corpus 冻结。

这不是本轮需要修正的“历史改写”。phase result 的 ProviderRun-shaped facts 与最终 Evidence projection 必须
保持不同身份，后继 assembler 不能把同一个 mutable mapping 原地改写。

### 5.2 non-published phase bytes 不消费 artifact budget

Fact phase 不发布 Artifact，因此内存中的 candidate/result 不伪装成 staging bytes，也不消费
`artifact_bytes`。这条边界继续成立。内部 transport 仍需独立 safety bound，但不能借 artifact ceiling 偷换成
IPC payload identity 或提前授权 FactSet publication。

### 5.3 opaque attempt identity 与 stable Fact identity 保持不变

新的 execution topology、transport 或 context invalidation 都不得进入 `fact_id`。相同 owned source、Profile
与规范 observation 在不同 attempt/provider runtime 下仍应得到相同 Fact identity；ProviderRun/Evidence
identity 继续保存执行差异。

### 5.4 当前不是恶意代码隔离合同

Windows Job memory/process containment 不提供 filesystem、network、credential、module monkeypatch 或 hostile
Provider sandbox。首版 Provider 与 application worker 属于 trusted local runtime。真实不可信 Provider 隔离
需要独立威胁模型和能力边界，不在本轮补写。

## 6. 发现分类

| 类别 | 观察 | 当前裁决 |
| --- | --- | --- |
| Freeze blocker | Provider/candidate/canonicalization 无法按现有直觉组合同时满足 hard memory 与 Fact authority | 先冻结 execution-cell authority topology |
| Freeze blocker | process primitive 没有 request/result framing、size、partial/duplicate/terminal envelope 语义 | 先冻结 bounded single-terminal transport |
| Freeze blocker | primitive failure 后 context 仍为 RUNNING，且可提交后继 success | attempt controller 必须拥有不可恢复 invalidation |
| Freeze blocker | 无 terminal envelope 且无 positive cause event 时，公共 diagnostic 映射未闭合 | 合同先裁决 epistemic fallback 或 Schema revision |
| Freeze blocker | capability preflight、concrete cell preparation、attempt admission 与 run start 没有唯一顺序 | 冻结 setup/budget/cleanup 原子边界 |
| Implementation gate | `implementation handle` 不是天然可跨进程身份 | 首版只允许 application-owned closed test binding |
| Implementation gate | Provider 不能自报 Evidence 时间、状态或 canonical reported IDs | controller/application 观察并提交 |
| Deferred seam | 真实 Python 3.10 parser、parse failure、encoding/anchor 与 partial AST | 等 execution cell 冻结后独立审计 |
| Deferred seam | 第三方 Provider registry/authorization、跨平台 cell、不可信代码沙箱 | 不为未来假设预冻结 |
| Observe only | README 系统家族表仍写 Budget Primitive “进入冻结候选” | 本 PR 做最小状态修正；不推翻 frozen implementation |
| No change | `ReviewPolicy 0.1`、Fact identity、FactSet、Manifest file set | 当前反例不要求改动 |
| No change | DerivationEvidence 0.1.1 reported-ID projection | 已有 Schema/corpus 闭合 |

## 7. 选定的下一个最小合同闭环

下一步不直接实现文档 137 的 C–E，而先起草一个独立 docs-only：

```text
R1 Derivation Execution Cell / Terminal Envelope Contract 0.1
```

它只允许冻结：

```text
owned DerivationInputSet + opaque derivation_id + explicit test Provider binding
        ↓
concrete cell preparation / exact admission boundary / one BudgetContext
        ↓
application-owned contained worker
        ├─ Provider candidate observation
        └─ application validation + canonicalization
        ↓
bounded copy-owned single-terminal envelope
        ↓
controller checkpoint + resource closure + atomic phase commit
        ↓
success result OR typed non-success + non-reusable context
```

合同必须逐项回答：

1. inactive cell、budget `t0`、attempt admission 与 Provider run start 的唯一顺序；
2. controller、application worker 与 Provider 各自拥有的 authority；
3. exact input/result envelope、framing、上限、partial/duplicate/trailing-byte 拒绝规则；
4. closed test Provider binding 怎样跨进程而不恢复 ambient discovery；
5. Provider exception、nonconformant output、no-envelope exit、platform error 与 stop latch 的机械映射；
6. primitive/protocol/cleanup failure 后 context 怎样不可恢复失效；
7. started/finished time、diagnostic 与 terminal summary 的观察权；
8. 两个充分 safety profile/budget 下 canonical result bytes/Fact IDs 怎样保持一致；
9. 是否需要 `DerivationEvidence` 新 revision；若不需要，现有 diagnostic 的认识论含义怎样被精确收窄；
10. 为什么该内部 phase result 仍不是 FactSet、Evidence、Manifest 或完整 derivation。

该合同冻结以前，不实现 worker transport、Provider protocol、candidate-to-Fact、phase result 或新 Schema。
合同冻结也只能解除自身列明的最小 implementation gate，不能自动授权真实 parser 或完整 Derivation。

## 8. 反例矩阵

| # | 单变量反例 | 错误推理 | 必须保持的裁决 |
| ---: | --- | --- | --- |
| 1 | in-process Provider 在 controller 内分配大量 candidate | 配置了 Job，所以 Provider 已受 memory containment | 拒绝；语义工作必须落入 frozen cell topology |
| 2 | child 返回 candidate，controller 在 Job 外 canonicalize | Provider 在 Job 内，所以完整 phase 都受约束 | 拒绝；application canonicalization 也必须满足冻结覆盖 |
| 3 | child 直接返回 Provider 声明的完整 Fact | process isolation 等于 canonical authority | application 必须独立拥有 validation/identity |
| 4 | result channel 只写出半帧后进程退出 | 有 bytes 等于有 phase result | non-success；无 canonical Fact 外泄 |
| 5 | 进程异常退出但没有 memory/deadline/cancel event | active memory limit 等于 memory cause | 保留未归因事实，不猜原因 |
| 6 | primitive setup 抛错后继续使用原 context | cleanup/exception 等于 context 已安全重置 | context 不可恢复失效；retry 建新 attempt |
| 7 | terminal envelope 已到达但 tree/handle 未在 deadline 前闭合 | Provider result 等于 phase complete | 禁止 success commit |
| 8 | worker 通过 module string 从 ambient `sys.path` 发现 Provider | explicit descriptor 等于 exact implementation binding | 拒绝 ambient discovery；使用 closed launch binding |
| 9 | Provider 自报 started/finished/status/reported IDs | Provider success 赋予 Evidence authority | controller/application 复算与提交 |
| 10 | transport safety limit 改变且两次均充分 | runtime safety profile 是 Fact identity | canonical result bytes/Fact IDs 必须相同 |

## 9. 公开状态残留

审计发现 README 的当前状态表和主叙事已经写成
`R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN`，但“系统家族与未来边界”中的 R 行仍写“Budget Primitive 已实现并
进入冻结候选”。这是同一公开页面内的状态不一致。

此前匿名读回只证明冻结 marker 正向存在，没有检查旧 candidate 描述不存在，因此不能把该读回外推为
README 全局状态一致性证明。本 PR 将该行最小修正为 frozen，并要求后继状态读回同时检查目标状态存在与
互斥旧状态缺失：

```text
Positive marker presence
  != whole-document state consistency
```

该修正不改变 Budget Primitive runtime、合同、PR/CI/readback 历史或冻结资格。

## 10. 本地审计证据

静态检查已经确认：

```text
changed files
  = AGENTS.md
  + README.md
  + docs/milestones.md
  + this audit

relative Markdown links
  = PASS

git diff --check
  = PASS

forbidden future-state marker scan
  = PASS

stale "Budget Primitive 已实现并进入冻结候选" in README
  = absent
```

Budget/Boundary 定向回归为：

| Runner | Budget | Boundary | 合计 |
| --- | ---: | ---: | ---: |
| CPython 3.10 normal | 21/21 | 6/6 | 27/27 |
| CPython 3.10 `-O` | 21/21 | 6/6 | 27/27 |
| CPython 3.13 normal | 21/21 | 6/6 | 27/27 |
| CPython 3.13 `-O` | 21/21 | 6/6 | 27/27 |

第一次本地命令曾尝试运行完整 Review Attention 83 项 suite，但外层工具在 120 秒先到且没有返回 unittest
终态；该次只能记为 `NO_TERMINAL_RESULT`，不能算 PASS，也不能归因为产品测试失败。后续 focused matrix 使用
独立命令和足够外层时间建立，只证明本 docs-only 变更没有破坏当前 Budget/Boundary 边界，不替代完整远端门。

本轮没有运行真实 Provider/parser/Fact，因为这些对象尚未取得合同与实现资格。

## 11. Fresh-Agent 交接与停止线

一个没有聊天上下文的新 Agent 只读仓库时，必须得出：

```text
Frozen:
  SourceSnapshot
  DerivationInputSet
  DerivationEvidence 0.1.1 correction
  Derivation Budget Primitive

Audited but not contracted:
  Derivation Execution Cell / Terminal Envelope

Not implemented:
  Provider Run / canonical Fact provenance

Still forbidden:
  real parser
  FactSet / DerivationEvidence publication
  Relation / conflict / UNKNOWN propagation
  Slice / Coverage
  COMPLETE or DIAGNOSTIC runtime Manifest
  CLI / Workbench / Core handoff
```

本轮没有冻结 worker topology、transport format、new diagnostic、Schema revision 或 implementation API。下一步
只能从新的 exact main 起草 docs-only execution-cell/terminal-envelope 合同；该候选自己的远端门、受保护
主线合入、exact-main 门、匿名公开读回与独立冻结发布全部成立以前，不得开始代码施工。
