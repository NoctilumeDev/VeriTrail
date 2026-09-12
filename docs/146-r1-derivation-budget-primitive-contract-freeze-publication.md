# R1 Derivation Budget Primitive 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_FROZEN /
> R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_ALLOWED /
> R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 前置审计：[R1 Derivation Budget Primitive 前置审计](144-r1-derivation-budget-primitive-precontract-audit.md)
>
> 冻结合同：[R1 Derivation Budget Primitive 最小合同](145-r1-derivation-budget-primitive-contract.md)
>
> 候选合入基线：`main@9a969af10f705abe66ac7816bc27e9369ea7206a`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只在 AGENTS、README、milestones 与本状态文档中发布 budget primitive 合同候选已经完成审计、
本地回归、原始 PR 门禁、受保护主线合入、exact-main 门禁、匿名 raw bytes 读回与已安装产品公共渲染
读回的事实。本文不修改文档 144/145、公共 Schema、corpus、测试、依赖、CI 或任何 runtime，也不创建
Provider、parser、Fact、Relation、Slice、Coverage、Manifest、CLI、Workbench、tag 或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main Public CI / Browser Smoke 与最终匿名
exact-SHA 产品读回。只有这些最后门全部成立，状态目标才成为当前主线事实；在此之前，本分支文字不
授权实现。

## 2. 冻结对象与语义边界

本次冻结的是文档 145 所定义的最小 budget primitive 合同，不是其实现。核心不变量为：

- hard memory containment 与 terminal cause attribution 分离；只有绑定当前 owned execution cell、并赢得
  terminal-stop latch 的正向 memory-limit event，才可报告 `EXECUTION_MEMORY_BUDGET`；
- configured hard limit、OOM、allocation failure、非零退出、接近上限的 peak 或缺失通知都不得反推该原因；
- `wall_clock_ms` 是从 attempt 执行态开始共享的 absolute monotonic acceptance/result-eligibility deadline，
  不是“到点即已物理清理完成”的承诺；
- normal result 与所有 phase-owned resources 必须在同一 deadline 前闭合，normal completion commit 与
  terminal-stop latch 共用一个原子决定边界；
- deadline、cancellation、positive memory event 与 artifact reservation failure 只能通过一个 terminal-stop
  latch 取得停止权；同一 checkpoint 的固定顺序为 deadline、cancellation、memory event、artifact failure；
- terminal stop 之后只创建一次 5000 ms cleanup-only release envelope；全阶段共同消费剩余预算，不刷新、
  不恢复语义工作、不接纳迟到结果；
- artifact budget 使用 inclusive producer-side reservation：恰好等于上限合法，一字节超限必须在打开输出文件
  前拒绝，并且不得留下 final 或 staging artifact；
- runtime binding 仍是实现期选择；合同没有选择 `ctypes`，也没有授权导入 Core 私有 Windows Job 实现。

因此继续成立：

```text
Containment configured != Cause positively observed
Phase returned != Phase successfully completed
Deadline expired != Process tree already released
Cleanup envelope != New semantic execution budget
Artifact reservation failure != Partially publishable artifact
Contract frozen != Provider/parser/Fact implementation authorized
```

`ReviewPolicy 0.1` 与 `DerivationEvidence 0.1.1` 的公共 bytes、identity 和语义均未重开：

| Frozen object | SHA-256 |
| --- | --- |
| `schemas/review-policy-0.1.schema.json` | `101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f` |
| `schemas/review-derivation-evidence-0.1.1.schema.json` | `a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045` |

## 3. 候选、本地回归与保留事实

合同候选从 exact `main@3a1374c2e7c5861ab9746052dceb8f50a1544d3e` 建立：

```text
candidate commit:
bee572d4ae96d07c1968ffd7702e69c39f500711

candidate / merge tree:
76a78b58fc0a1723812bc676c0a41f2a6427ef9e
```

候选只修改七个文档路径；没有产品代码、Schema、依赖、CI 或测试变化。有效本地回归均显式绑定同一
候选 worktree 的源码与测试坐标：

| 门 | CPython 3.10 normal / `-O` | CPython 3.13 normal / `-O` |
| --- | ---: | ---: |
| Review Attention | `61/61` / `61/61` | `61/61` / `61/61` |
| Core | `446/446` / `446/446` | `446/446` / `446/446` |
| GitHub Evidence | `180/180` / `180/180` | `180/180` / `180/180` |
| Authoring Skill | `24/24` / `24/24` | `24/24` / `24/24` |

Workbench 在 `npm ci` 后为 `173/173`，lint、type-check/build 与 dependency audit 均通过，audit 为 0
vulnerability。第一次并行运行四条 Review lane 时，本地总命令 124 秒超时，留下四个可精确归属的 Python
进程；这些进程经命令行坐标核对后全部终止，结果被分类为本地 orchestration/resource-contention 事实，
没有冒充产品失败，也没有用后续串行成功抹去。第一次 Workbench 尝试因候选 worktree 尚无
`node_modules` 而在产品测试前停止，同样保留为环境准备事实。

## 4. PR #124 与 exact-main 门禁

[PR #124](https://github.com/NoctilumeDev/VeriTrail/pull/124) 的 base 为上述 exact main，head 为 candidate
commit，diff 只含七个 docs-only 路径。原始
[Public CI run 34716400860](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34716400860)
在 attempt 1 取得 11/11 success，没有 rerun。PR 以以下 merge commit 合入：

```text
merge commit:
9a969af10f705abe66ac7816bc27e9369ea7206a

parents:
3a1374c2e7c5861ab9746052dceb8f50a1544d3e
bee572d4ae96d07c1968ffd7702e69c39f500711
```

merge tree 与 candidate tree 相同。该 exact main 的门禁为：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34717066992](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34717066992) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34717067020](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34717067020) | 1 | `1/1 SUCCESS` |

## 5. 匿名 exact-SHA raw bytes 读回

没有 GitHub token 的 raw readback 取得以下公开字节，并与 merge tree 逐字节相等：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 23300 | `dbae2dc6bea480582e8c113c8089112aedca6ee5284321c63a53d6b10ba9105f` |
| `docs/137-r1-derivation-attempt-and-fact-provenance-contract.md` | 30102 | `91cf8ee1ddade04433eb28c9b834886aee79ee8316893b211d633876f4bc5742` |
| `docs/140-r1-derivation-evidence-schema-correction-contract.md` | 12970 | `95dc176ac312da99831c0dc12dbdd4c291634dd8026e0647ea96f47d848a3bca` |
| `docs/144-r1-derivation-budget-primitive-precontract-audit.md` | 13567 | `905b01839c92568518ebced7fb1884201d1c67bf17aa81b971b6e23077d9914d` |
| `docs/145-r1-derivation-budget-primitive-contract.md` | 15800 | `9a7f4c470ca4b3869c3600e6e4dedd2ebd02c15257cdece428b15032f88ea9f5` |
| `docs/milestones.md` | 72155 | `5634833c4522ab0076ade5d15c7f34f64bc6d144f3fb089e3ff1a2e193f26e7b` |

raw transport success 只证明该时刻的 exact public bytes 可取得，不替代合同正确性、门禁或产品读回。

## 6. 匿名已安装产品读回

读回使用既有 clean venv 中从 `site-packages` 导入的 Core、GitHub Evidence 与 Playwright，不使用 checkout、
editable install 或候选 `PYTHONPATH`；环境移除 GitHub token。三个 target 使用独立 sealed AcceptancePlan、
独立 paired session、固定 `P1 API -> P2 Render` 顺序、fresh anonymous Chromium、exact commit Markdown
坐标与三样本稳定窗口。

| Target / viewport | Marker occurrences | Facts digest | Render Evidence SHA-256 | Report SHA-256 |
| --- | ---: | --- | --- | --- |
| `README.md` / desktop | 1 | `5162b46945e756f8657d2f90604a3e405dba4cfd37a45d65073f268ddcc09b89` | `a3b7c9336683796c63f43d5f0acc62e75a30ee1c4435ded95eaaa9a1097b37a8` | `19900bd581115ffcb44710afb5b6335060d843ba59e289d354b18313cea67344` |
| `docs/145-r1-derivation-budget-primitive-contract.md` / narrow | 2 | `fe956d128dd3d7b59636fc43b7e958039c68b478fcd475bb5b9ff104c7cac738` | `edf6b8ac0740e6698a4dac8204060e6709be298b55e24413ef03f1d462025aea` | `a6af748f21e85fd79e0cfa8f3fcf86078e10c7d148f46a1f9d50e5bf4207974a` |
| `docs/milestones.md` / narrow | 1 | `7357750900a321997a6241ac001455684e0eed92bf758e94595d79942fc2448a` | `22db30e7edd4551c4bd08dc69f018c93df786777797e2ede47f532e225afcdef` | `6e8845fd91078abb389d85a9df25637eb4172f74ee36814f5ae837e14d059e2e` |

三项 coverage 均为 `COMPLETE`、HTTP 200、三样本稳定、一个 usable scope，Core Verdict 均为 `PASS`；
collection errors、coverage conflicts、cleanup errors 与 active streams 均为 0。summary digest 为
`a0490c3dc1e1b10c6dd6688afde60ffbab348759a61094328a77ae01ebb71f93`。

第一版读回 wrapper 引用了已经不存在的旧 Plan template 路径，在任何 collection 与 GitHub 访问前以
`FileNotFoundError` 停止，且没有输出。后继只修正 wrapper，让三例分别从现存 sealed Plan 结构重新绑定
exact path/SHA/marker 后再 seal；失败事实没有被改名为产品失败或网络失败。

该读回只证明采集时 GitHub 公共渲染可观察到候选内容，并证明已发布产品能完成该次 observation 与 Core
验收；它不证明 GitHub 之外的来源真实性，也不让 Collector、本文或模型取得现实真值裁决权。

## 7. 第二轮系统俯瞰与问题分类

候选冻结前又执行一次系统级组合审计。目标不是增加 finding 数量，而是检查局部合同拼接后是否出现新的
authority、identity、lifecycle 或 completeness 裂缝；发现项不自动产生修改义务。

### 7.1 Freeze blockers：已在候选中最小修正

1. `COMPLETED_FOR_PHASE` 原本被误画为 `BudgetContext` terminal state，但后继 phase 必须复用同一 context；
   修正后它只是 phase result，context 在后继 phase 之间继续 `RUNNING`。
2. normal completion eligibility check 与 terminal-stop latch 原本可能发生竞态；修正后 completion commit 与
   stop latch 共用一个原子决定边界，至多一个成功，并增加 late-resource-close 与 check/commit race 反例。

### 7.2 Implementation gates：不重开合同，施工时必须证明

- Windows native binding、消息 drain、process-tree zero 与 cleanup residue 的真实 harness；
- normal result 与 worker/process tree、observer thread/channel、handle 的 deadline-before closure；
- `BP-001..016` 的双 Python、normal/`-O`、真实 process tree 与 artifact staging conformance。

### 7.3 Deferred seams：准确记账，不在本轮解决

- 没有正向 event 的 worker exit 最终映射为何种通用 terminal cause；
- event chronology、peak 与 consumption facts 将来是否进入更丰富 Evidence；
- POSIX/cgroup 对等 primitive、跨平台与分布式执行。

### 7.4 Observe only：不触发修改

Review Attention 单 lane 在当前 16 GB reference host 上约需 140 秒。这是后继验证调度与资源规划的现实输入，
不是降低 gate、并入 Q 实现或改变 R1 合同的理由。本轮没有发现第三个需要重开 Schema、Corpus、
ReviewPolicy、DerivationEvidence 或上游 R1 identity 的 Freeze blocker。

## 8. 保留边界与唯一下一步

本次没有冻结、实现或授权：

- budget primitive runtime、本机可复用 conformance harness 或任何 Provider execution；
- Provider binding/attempt kernel、parser、canonical Fact、FactSet 或 DerivationEvidence publication；
- RelationSet、conflict/UNKNOWN 传播、ReviewSliceSet、CoverageLedger 或完整 Derivation Manifest；
- CLI、Workbench、Core handoff、Q implementation、D product shell、JPyxis 或 AI Execution OS；
- Linux/macOS、Server/Cloud、并发、分布式、tag 或 Release；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本 docs-only 状态发布只修改 AGENTS、README、milestones 并新增本文；文档 144/145 与两个 frozen Schema
必须逐字节不变。本文自己的最后门全部成立后，当前状态为：

```text
R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_FROZEN
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_ALLOWED
R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

唯一下一步是从新的 exact main 建立独立 budget primitive implementation，并只实现文档 145 的 runtime
primitive 与 `BP-001..016` conformance。该实现自身完成审查、门禁、主线合入、真实 readback 与独立冻结
以前，不得启动 Provider/parser/Fact。

Relation、Slice、Coverage、conflict/UNKNOWN 与完整 Derivation 继续没有施工资格。任何新反例仍可否决
实现、只重开被击穿的最小边界，或被分类为非阻断观察；审计发现本身不是修改 KPI。
