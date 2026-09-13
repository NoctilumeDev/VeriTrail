# R1 Derivation Execution Cell / Terminal Envelope 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_EXECUTION_CELL_CONTRACT_FROZEN /
> R1_DERIVATION_EXECUTION_CELL_IMPLEMENTATION_ALLOWED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 前置审计：[R1 Derivation Execution Cell 与 Terminal Continuity 系统审计](149-r1-derivation-execution-cell-system-audit.md)
>
> 冻结合同：[R1 Derivation Execution Cell / Terminal Envelope 最小合同 0.1](150-r1-derivation-execution-cell-terminal-envelope-contract.md)
>
> 候选合入基线：`main@e1f91a94afb3e3afd4e85d3605240b77d379f57a`
>
> 候选合入 Tree：`388ecd40ac997dad94f84e270c81e3dda6c36c50`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 150 的合同候选已经完成本地组合审计、focused regression、原始 PR 门禁、受保护主线合入、
新 exact-main Public CI / Browser Smoke 与 fresh anonymous installed-product readback 的事实。本文不创建或修改
runtime、Schema、corpus、identity vector、测试、依赖、CI、Provider、parser、FactSet、DerivationEvidence、
Relation、Slice、Coverage、Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release。

本文自身仍须完成原始 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及针对
本文合入坐标的 fresh anonymous product readback。只有这些最后门全部成立，状态目标才成为当前主线事实；
在此以前，本分支文字不授权 execution-cell implementation。

## 2. 冻结对象

本次只冻结一条 test Provider / canonical Fact phase 的运行接缝：

```text
owned DerivationInputSet + explicit closed test Provider binding
        ↓
one provisional BudgetContext + inactive cell preparation
        ↓
atomic Derivation Attempt admission + ProviderRun start
        ↓
contained application worker
        ├─ Provider bounded observation
        └─ application validation / canonical Fact identity
        ↓
bounded single-terminal canonical JSON envelope
        ↓
controller-owned latch / release / phase commit
```

冻结对象不是：

```text
real Python parser
FactSet or DerivationEvidence publication
Relation / conflict / UNKNOWN propagation
Slice / Coverage
COMPLETE or DIAGNOSTIC R1 Manifest
third-party Provider registry or trust
hostile-code sandbox
cross-platform execution cell
```

## 3. 冻结不变量

### 3.1 authority 与 containment 同时闭合

- trusted controller 位于 cell 外，只拥有 admission、clock、latch、transport validation、release observation 与
  atomic commit，不解释源码或 canonicalize Fact；
- application worker 位于 hard memory-contained cell 内，拥有 candidate conformance、规范化、Fact identity 与
  reported-ID summary；
- Provider 只拥有 bounded observation，不能提交 canonical Fact、时间、public status、diagnostic 或 Evidence；
- 进程边界不是 authority 边界；application code 可以在 child 内，Provider 不能因同进程而继承 application
  authority。

### 3.2 setup 成本属于同一个 absolute budget

顺序固定为：

```text
capability preflight
-> exact request provenance / resolved_at
-> monotonic t0 + provisional attempt_started_at
-> one provisional BudgetContext
-> bounded request frame + inactive contained cell preparation
-> final pre-admission checkpoint
-> atomic attempt admission
-> controller-owned ProviderRun started_at
-> resume worker
```

preflight、concrete preparation、attempt admission 与 ProviderRun start 不是同一事实。preparation 失败时没有
ProviderRun/Evidence；一旦 attempt admitted，resume/transport/worker failure 不能退回“从未开始”。

### 3.3 transport 有且只有一个终态

- request 和 result 各使用一个 application-owned 单向 channel；
- frame 是 `8-byte unsigned big-endian length + exact canonical JSON payload + EOF`；
- partial header/body、oversize、duplicate、trailing bytes、BOM/newline、noncanonical JSON 与 normal exit without
  envelope 均 fail closed；
- `ExecutionCellTransportSafetyLimits` 只控制本次运行是否有资格完成，不进入 Fact/Evidence identity，也不消费
  artifact budget；
- launch key 只来自 product-owned closed allow-list，不使用 pickle、module string、entry point、`sys.path` 或
  ambient installation discovery。

### 3.4 positive warrant 与 epistemic fallback 分开

```text
positive deadline latch     -> EXECUTION_DEADLINE
positive caller cancel      -> EXECUTION_CANCELLED
positive owned memory event -> EXECUTION_MEMORY_BUDGET
valid Provider exception    -> PROVIDER_FAILED
valid unavailable signal    -> PROVIDER_UNAVAILABLE
bad candidate after app validation -> NONCONFORMANT_PROVIDER_OUTPUT
no valid terminal continuity and no narrower warrant -> INTERNAL_DERIVATION_ERROR
```

`INTERNAL_DERIVATION_ERROR` 只说明一个已开始的 owned ProviderRun 没有建立可提交 terminal result；它不归因于
Provider、memory、OS、transport 或 application 根因。exit code、OOM text、active hard limit 和 stderr 都不能
提高原因强度。

### 3.5 eligibility revoke 与 resource release 分开

primitive、protocol、non-success 或 cleanup failure 会不可恢复地撤销 attempt eligibility。raw BudgetContext 不得
从 controller 泄露；即使底层 context 机械状态仍为 `RUNNING`，revoke 后也不能启动 worker、接纳结果、调用
phase completion 或进入后继 phase。

revoke 不证明资源已经释放；cleanup 仍必须在唯一 release envelope 下收敛到 `RELEASED / RELEASE_FAILED`。
cleanup 成功不恢复 eligibility；`RELEASE_FAILED` 禁止 phase result 与正常 Artifact publication。

### 3.6 runtime safety 不污染 Fact identity

不同但都充分的 budget/transport safety profile 只能改变运行资格与 provenance，不能改变去 provenance 的
canonical Fact content、`subject_key_digest` 或 `fact_id`。完整 Fact object 的 `provenance_refs` 必须诚实绑定
各自 `provider_run_id`，因此不要求跨 attempt 的完整 Fact bytes 相同。

## 4. `DerivationEvidence 0.1.1` 不升级的裁决

系统审计曾保留两种方案：收窄已有 `INTERNAL_DERIVATION_ERROR`，或新增 Evidence revision/code。合同审计最终
选择前者，因为：

1. 现有 code 与 `PROVIDER_RUN` subject 已能表达“已启动 run 未建立有效终态”；
2. 当前没有稳定正向 observation 能支持更强的公共根因名称；
3. `WORKER_EXITED / TRANSPORT_FAILED` 会把运行位置或机制误写成原因；
4. pre-admission failure 根本没有 ProviderRun/Evidence，应保留为调用层 typed error。

本冻结不修改 `review-derivation-evidence-0.1.1.schema.json`、correction corpus 或 digest projection。未来若出现
新的正向可验证事实，再以独立 Schema revision 讨论；不能为了让 enum 更“具体”而先编造 ontology。

## 5. 冻结前第二轮系统俯瞰

本轮不以 finding 数量为目标。发现不自动要求修改，只有击穿当前不变量或使冻结文本不可同时满足的反例才
成为 blocker。

| 分类 | 观察 | 裁决 |
| --- | --- | --- |
| Freeze blocker，已修正 | 初稿要求不同 attempt 的完整 canonical Fact bytes 相同，但 `provenance_refs` 必须绑定不同 run | 只冻结 provenance-free content/Fact ID invariance；完整 Fact provenance 保持真实 |
| Contract closure | 文档 137 把 t0/admission/concrete preparation 压成一层 | 最小修正 137；t0 先于 preparation，成功后才 admit attempt |
| Contract closure | primitive-local `RUNNING` 可被误作公共 attempt 已开始 | 冻结 budget eligibility 与 attempt eligibility 双层 gate |
| No Schema change | no-envelope exit 没有更强正向 root-cause observation | 使用不归因的 `INTERNAL_DERIVATION_ERROR` |
| Implementation gate | Windows inherited channel、suspended worker assignment 与 EOF closure 必须真实证明 | 留给最小 implementation feasibility；做不到则重开合同，不降级 |
| Implementation gate | request serialization 位于 controller，但必须有 finite product cap | transport cap 与 frame streaming 必须进入 conformance；不赋予 Fact identity |
| Deferred | Provider stdout/stderr、真实 parser、encoding/anchor、partial AST | 不进入首个 test Provider implementation |
| Deferred | hostile Provider sandbox、third-party registry、cross-platform cell | 需要独立 threat/capability contract |
| No change | ReviewPolicy、Fact identity、FactSet、Manifest file set | 当前反例未击穿 |

这轮修正没有扩成 Relation、Slice 或 Coverage，也没有为了“审出问题”增加无证据字段。

## 6. 候选与 exact-main 证据

### 6.1 本地

合同候选在 exact `main@2de46c21997d85a437820decfeb2bd8bb7b69ee1` worktree 完成：

```text
relative Markdown links             PASS
git diff --check                    PASS
runtime/schema/corpus diff          empty

Budget + Boundary regression
  Python 3.10 / 3.10 -O             27/27 each
  Python 3.13 / 3.13 -O             27/27 each

DerivationEvidence correction
  Python 3.10 / 3.10 -O              5/5 each
  Python 3.13 / 3.13 -O              5/5 each
```

一个不落盘的 `FAILED / INTERNAL_DERIVATION_ERROR / PROVIDER_RUN / empty IDs` specimen 通过现有 `0.1.1`
Schema 与 correction conformance validator；复算 digest 为：

```text
8ad1343f69fe4ca60b9385ce7c71d9d15220d10641fb4534d4947b9e44b28d96
```

它只证明现有公共形状足够，不成为新 corpus。

### 6.2 PR #130 原始门

候选提交：

```text
ff801ba9cac96379bad851a1c822c2229dec0df2
```

PR #130 的 base 是 exact `2de46c21997d85a437820decfeb2bd8bb7b69ee1`，文件集恰为：

```text
AGENTS.md
README.md
docs/137-r1-derivation-attempt-and-fact-provenance-contract.md
docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md
docs/milestones.md
```

Public CI run `34755844078`、attempt 1 完成 11/11 SUCCESS。没有 rerun，也没有用后继 main 的绿灯替代 PR head。

### 6.3 受保护主线与 exact-main 门

PR #130 合入：

```text
main = e1f91a94afb3e3afd4e85d3605240b77d379f57a
parents = 2de46c21997d85a437820decfeb2bd8bb7b69ee1
          ff801ba9cac96379bad851a1c822c2229dec0df2
tree = 388ecd40ac997dad94f84e270c81e3dda6c36c50
```

该 exact main 的新门为：

```text
Public CI     run 34756474790  attempt 1  11/11 SUCCESS
Browser Smoke run 34756474928  attempt 1   1/1 SUCCESS
```

### 6.4 fresh anonymous installed-product readback

从不设置 GitHub token、清空 `PYTHONPATH` 的已安装 Core/GitHub Evidence/Playwright 环境，对 exact
`e1f91a94afb3e3afd4e85d3605240b77d379f57a` 建立三次独立 paired session：

```text
README.md
  viewport = DESKTOP_1365X768
  positive marker occurrences = 1
  stale CONTRACT_NOT_STARTED occurrences = 0
  Core Verdict = PASS

docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md
  viewport = NARROW_390X844
  positive marker occurrences = 1
  Core Verdict = PASS

docs/milestones.md
  viewport = NARROW_390X844
  positive marker occurrences = 1
  Core Verdict = PASS
```

每个 session 固定 `P1 API -> P2 Render`，但不冒充 atomic snapshot；三样本均稳定，无 cleanup error、coverage
reason 或 active stream。summary digest：

```text
481e864bc169ef50afdff0d28e8c3be0d8bbe6661cdddf74125b9ba3037217e9
```

## 7. 本状态发布自身的最后门

本文分支必须重新完成：

1. diff 只含 AGENTS、README、milestones 与本文；
2. relative links 与 `git diff --check` 通过；
3. 原始 PR required checks 全部成功；
4. 受保护主线合入且 merge parents/tree 可复核；
5. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
6. fresh anonymous readback 对 README、本文、milestones 各自 Core PASS；
7. README 同时证明 `CONTRACT_FROZEN` 存在、`CONTRACT_CANDIDATE` 不再作为当前状态出现。

任一门失败，状态继续保持 candidate；不得开始 implementation，也不得通过重写历史或放宽 marker 消除红灯。

## 8. 冻结后的唯一授权

所有最后门成立后，只允许从新的 exact main 实现文档 150 的 A–F：

```text
attempt eligibility + provisional admission
bounded frame codec
contained application worker
closed deterministic test Provider binding
terminal mapping + revoke/release
copy-owned non-published Fact phase result
EC-001..024 conformance
```

真实 parser、FactSet/DerivationEvidence publication、Relation、conflict/UNKNOWN、Slice、Coverage 与完整 Manifest
仍未授权。implementation 一旦遇到新的 runtime primitive 反例，必须先停止并只重开被击穿的最小条款。

当前分支状态仍是“冻结发布候选”，不是 implementation start。一个 fresh Agent 不得在本文自己的最终门完成前
创建 worker、transport、Provider、Fact 或 Schema 代码。
