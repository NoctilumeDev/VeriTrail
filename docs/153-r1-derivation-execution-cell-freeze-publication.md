# R1 Derivation Execution Cell 实现冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_EXECUTION_CELL_FROZEN /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[Execution Cell / Terminal Envelope 最小合同 0.1](150-r1-derivation-execution-cell-terminal-envelope-contract.md)
>
> 合同冻结：[Execution Cell / Terminal Envelope 合同冻结发布](151-r1-derivation-execution-cell-contract-freeze-publication.md)
>
> 实现候选：[Execution Cell 实现冻结候选](152-r1-derivation-execution-cell-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@c2349b2a7c4d9ed002311d46f7212cb35856caf6`
>
> 候选合入 Tree：`63239304e6d32479a888ebf1e5a077a4143292bb`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 150/151 冻结的 execution-cell 合同已经按文档 152 的边界完成实现、实现后系统审计、
候选门禁、受保护主线合入、新 exact-main 门禁与匿名已安装产品读回的事实。本文不创建或修改源码、测试、
Schema、corpus、identity vector、依赖、CI、Provider、parser、FactSet、DerivationEvidence、Relation、Slice、
Coverage、Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，
以及针对本文合入坐标的 fresh anonymous 产品读回。只有这些最后门全部成立，状态目标才成为当前主线事实；
在此以前，本分支文字不授权 provenance runtime 或任何后继实现。

## 2. 本次冻结的最小对象

本次冻结只覆盖私有 execution-cell 实现闭环：

```text
owned DerivationInputSet + closed test Provider binding
        ↓
one provisional BudgetContext + inactive Windows cell
        ↓
atomic attempt admission + provider run start
        ↓
hard-contained application worker
        ├─ Provider bounded observation
        └─ application-owned candidate validation / Fact identity
        ↓
bounded single-terminal canonical JSON envelope
        ↓
controller-owned latch / release / phase commit
        ↓
copy-owned non-published Fact phase result
```

冻结对象不是：

```text
real parser or public Provider SPI
canonical FactSet admission or DerivationEvidence publication
cross-Provider conflict / UNKNOWN propagation
RelationSet / ReviewSliceSet / CoverageLedger
COMPLETE or DIAGNOSTIC Derivation Manifest
hostile-code sandbox or cross-platform cell
```

## 3. 已冻结不变量

### 3.1 authority 没有因进程边界压扁

- trusted controller 拥有 admission、clock、stop latch、transport validation、release observation 与 phase commit；
- contained application worker 拥有 candidate conformance、规范化、canonical Fact identity 与 terminal summary；
- closed test Provider 只拥有 bounded observation，不能提交 public status、Fact ID、时间、diagnostic 或 Verdict；
- frame 可解析、child exit、OOM text、active hard limit 或 stderr 都不能自行取得 terminal-cause authority。

### 3.2 attempt eligibility 不可恢复

```text
PROVISIONAL -> ADMITTED
PROVISIONAL / ADMITTED -> REVOKED
```

primitive、protocol、terminal conformance、non-success 或 cleanup failure 一旦 revoke，后到的成功 terminal、
cleanup success 或仍显示 `RUNNING` 的底层 BudgetContext 都不能恢复提交资格。pre-admission failure 不伪造
ProviderRun；admission 后 continuity 丢失保留已开始 run，但只允许不归因失败。

### 3.3 正向观察才允许精确归因

```text
deadline latch                 -> EXECUTION_DEADLINE
caller cancellation latch      -> EXECUTION_CANCELLED
owned Job memory-limit event   -> EXECUTION_MEMORY_BUDGET
valid Provider failure         -> PROVIDER_FAILED
valid Provider unavailable     -> PROVIDER_UNAVAILABLE
application candidate reject   -> NONCONFORMANT_PROVIDER_OUTPUT
no narrower valid warrant      -> INTERNAL_DERIVATION_ERROR
```

`INTERNAL_DERIVATION_ERROR` 不声称 Provider、application、transport、OS 或 memory 是根因。配置了 containment
不等于观察到终止原因；terminal document 未通过 conformance 时，其中任何 reported identity 都不可信。

### 3.4 success 必须穿过完整 release barrier

success 同时要求：

```text
valid terminal
+ eligibility remains ADMITTED
+ no stop latch wins the race
+ process tree reaches zero
+ handles and channel threads release
+ BudgetContext phase commit succeeds inside the same deadline
```

terminal bytes 先到不等于 operation 已成功。release failure 不返回伪造的普通 phase result；late stop 可以否决
early terminal。任何失败路径都不能留下 canonical Fact bytes、Artifact path 或 Manifest。

### 3.5 phase value 不是发布闭包

`OwnedExecutionCellPhaseResult` 保存 copy-owned candidate values 与 canonical bytes，但没有输出路径、Manifest、
Artifact publication 或顶层公共 API。因此：

```text
candidate Fact generated != FactSet published
phase result returned      != Derivation closure
```

## 4. 实现与审计事实

实现从冻结合同基线 `3c89f8eb94333986fc4901b9a1b91edf47d0059f` 施工：

```text
implementation head = 02e4d05dcfc7c062c97ecfa21c00b26f601b9140
implementation merge = 8b77305cea3a95690660adcb25f76d2b42c6e5e1
implementation tree = d7f502908c4a1361f8756d15f238fd05a1864b04
```

实现只新增七个 private execution-cell 模块并扩充 execution-cell、Budget Primitive 与 public-boundary 测试；
`veritrail_review.__init__` 没有导出 execution-cell API，base package 也没有新增默认运行时依赖。

实现后审计修正了五个会击穿冻结不变量的接缝：

1. rejected terminal 不得泄漏 untrusted `provider_run_id`；
2. primitive commit failure 必须显式 revoke eligibility；
3. pre-admission runtime capability loss 必须映射为 typed unavailable，而非泄漏底层异常；
4. release failure 不得伪装成 `RELEASED` phase result；
5. late stop 必须仍能否决 early terminal。

第一次 BP-014 clean-wheel probe 因父进程 `PYTHONPATH` 与 editable metadata 污染安装坐标而作废；最终证据清空
父环境路径，由 fresh interpreter 从新构建 wheel 建立唯一 site-packages 坐标，没有用 force reinstall 掩盖问题。

## 5. 候选门禁与合入事实

### 5.1 本地门

实现 head 的 Review Attention 完整矩阵在 CPython 3.10/3.13 normal/`-O` 四格均为 `113/113`；冻结 R1
Schema/payload 消费回归四格均为 `27/27`。本发布又从候选合入后的 exact-main worktree 串行重跑以下定向门；
每格导入路径均指向当前工作树，`pywin32` 均为 312：

| 门 | CPython 3.10 | CPython 3.10 `-O` | CPython 3.13 | CPython 3.13 `-O` |
| --- | ---: | ---: | ---: | ---: |
| Execution Cell | `29/29` | `29/29` | `29/29` | `29/29` |
| Budget Primitive | `21/21` | `21/21` | `21/21` | `21/21` |
| Public boundary | `7/7` | `7/7` | `7/7` | `7/7` |

### 5.2 PR #133

[PR #133](https://github.com/NoctilumeDev/VeriTrail/pull/133) 的精确链为：

```text
base = 8b77305cea3a95690660adcb25f76d2b42c6e5e1
head = 84a986010c42ef43f785e3725ea6d65b87d3b063
merge = c2349b2a7c4d9ed002311d46f7212cb35856caf6
parents = 8b77305cea3a95690660adcb25f76d2b42c6e5e1
          84a986010c42ef43f785e3725ea6d65b87d3b063
tree = 63239304e6d32479a888ebf1e5a077a4143292bb
```

PR 原始 [Public CI run 34769531905](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34769531905)
为 attempt 1、11/11 SUCCESS，没有 rerun。PR 随后以普通 merge commit 合入受保护 `main`。

### 5.3 exact-main 门

`main@c2349b2a7c4d9ed002311d46f7212cb35856caf6` 的新门为：

```text
Public CI      run 34770503241  attempt 1  11/11 SUCCESS
Browser Smoke run 34770503260  attempt 1   1/1 SUCCESS
```

## 6. fresh anonymous installed-product readback

从不设置 `GH_TOKEN` / `GITHUB_TOKEN`、清空 `PYTHONPATH` 的 fresh CPython 3.13.13 venv 中，Core、GitHub
Evidence 与 Playwright 1.62.0 均从该 venv 的 `site-packages` 导入。探针针对 exact `c2349b2...` 建立三次
独立 paired session，固定 `P1 API -> P2 Render`：

| Target | Viewport | Marker occurrences | HTTP | Stable | Active streams | Core |
| --- | --- | ---: | ---: | --- | ---: | --- |
| `README.md` | `DESKTOP_1365X768` | `[1, 0]` | 200 | true | 0 | PASS |
| `docs/152-r1-derivation-execution-cell-implementation-freeze-candidate.md` | `NARROW_390X844` | `[1]` | 200 | true | 0 | PASS |
| `docs/milestones.md` | `NARROW_390X844` | `[1]` | 200 | true | 0 | PASS |

README 的第二个 marker 是旧 `IMPLEMENTATION_ALLOWED` 当前状态，计数必须为 0。三次 requested/final URL 均相同，
P1/P2 coverage 均为 COMPLETE，没有 cleanup error、coverage reason 或未关闭 response stream。三次 session、Plan
与 Evidence identity 分别独立；summary digest 为：

```text
94654f6f58fcf82a2a6230521164e8f98176dff1ab40e97d2c695a67d8c98045
```

这些读回只证明候选合入坐标的公开页面与已安装产品链可以共同成立，不替代本文自己的最终门。

## 7. 明确未冻结与后继停止线

本次没有冻结、实现或授权：

- real Python parser、encoding/anchor 与 partial AST；
- canonical Fact admission、FactSet 或 DerivationEvidence runtime publication；
- cross-Provider conflict / UNKNOWN 传播与完整 Derivation Manifest；
- RelationSet、ReviewSliceSet、CoverageLedger 或 Attention Proposal；
- CLI、Workbench 写入、Core 新判断、Q implementation、D product shell 或 JPyxis adapter；
- hostile-code sandbox、Linux/macOS cell、Server/Cloud、并发、分布式或多租户能力。

本文自己的最后门全部成立后，唯一下一步是从新的 exact main 对以下接缝做独立 pre-contract audit：

```text
Provider Run
  -> candidate Fact provenance
  -> canonical Fact admission
  -> FactSet / DerivationEvidence closure eligibility
```

审计可以发现并分类新裂缝，但不以 finding 数量为 KPI，也不因发现问题自动修改合同。它不等于 parser、
Provider 或 publication 实现授权；Relation、conflict/UNKNOWN、Slice、Coverage 与完整 Manifest 继续禁止。

## 8. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过
focused regression、Markdown 相对链接、状态 marker、敏感模式与 `git diff --check`。这些本地结果不替代
本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README、本文与 milestones
    -> 状态目标成为当前主线事实
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用文档 152、PR #133 或其读回替代本文自己的
最后门，也不得因为本文是 docs-only 就跳过完整门禁。
