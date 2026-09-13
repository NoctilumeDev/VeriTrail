# R1 Derivation Budget Primitive 实现冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[R1 Derivation Budget Primitive 最小合同候选](145-r1-derivation-budget-primitive-contract.md)
>
> 合同冻结：[R1 Derivation Budget Primitive 合同冻结发布](146-r1-derivation-budget-primitive-contract-freeze-publication.md)
>
> 实现候选：[R1 Derivation Budget Primitive 实现冻结候选](147-r1-derivation-budget-primitive-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@571139df5db94159f5e439619176f17a02f86f94`
>
> 候选合入 Tree：`e1e296ef99ce70a88d7d1618274d612909015bcc`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 145/146 冻结的 budget primitive 已按文档 147 的边界完成实现、系统审计、候选门禁、
受保护主线合入、新 exact-main 门禁与匿名已安装产品读回的事实。本文不创建或修改 Schema、corpus、
identity vector、源码、测试、CI、依赖、Provider、parser、Fact、Relation、Slice、Coverage、Manifest、CLI、
Workbench、Core、P/Q、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，
以及针对本文合入坐标的 fresh anonymous 产品读回。只有这些最后门全部成立，状态目标才成为当前主线事实；
在此以前，本分支文字不授权 provenance runtime 或任何后继对象实现。

## 2. 本次冻结的最小对象

本次冻结只覆盖独立 `veritrail-review-attention` 包中的 Derivation Budget Primitive：

```text
sealed execution limits
        ↓
absolute monotonic BudgetContext
        ↓
single terminal-stop latch
        ├─ deadline / cancellation
        ├─ positively observed memory-limit event
        └─ artifact reservation overflow
        ↓
cleanup-only shared release envelope
        ↓
controller-confirmed global release
```

其公共语义固定为：

- acceptance deadline 是从 admission 建立的一次性绝对时间坐标；phase、retry、stop 或 cleanup 都不能刷新它；
- normal completion 必须同时满足 result closure、全部 phase-owned resource closure，且 terminal stop 尚未赢得竞态；
- terminal-stop latch 只能提交一次，较晚 observation 不得覆盖已经成立的原因；
- Windows worker 必须 suspended-create、assign-to-owned-Job、resume，先建立 hard containment 再允许执行；
- 只有正向 Job memory-limit event 才能授权 memory-budget attribution；OOM、exit code、异常退出或已配置上限
  均不能反推原因；
- artifact reservation 是 inclusive producer-side 约束；完整写入与摘要验证以前只存在 create-new staging，
  超限或失败不得暴露 final artifact；
- local backend cleanup 只证明自身 residue 已闭合，不能冒充整个 BudgetContext 已全局 release；
- base package 不依赖或顶层导入 `pywin32`；Windows capability 只通过 exact `pywin32==312` optional extra
  和 lazy typed boundary 提供。

上述对象实现 `BP-001..016`，但不拥有 Provider applicability、Fact authority、DerivationEvidence publication、
storage topology 或最终 Verdict。

## 3. 实现与审计证据

[PR #126](https://github.com/NoctilumeDev/VeriTrail/pull/126) 从合同冻结基线
`4c4d81bfeed7bea9d159a58bb91097f8d98fb0c8` 实现该 primitive：

| 坐标 | 事实 |
| --- | --- |
| `998b6ef52665bcafc0e7f9b6b8f2cbc0bedb2341` | 主实现与 `BP-001..016` conformance |
| Public CI `34746174728` | 第一个 head 在双 Python 的 BP-014 失败；未 rerun |
| `b23488e7f12b719c6fc331af31ff9bb9032659ca` | 删除测试对 ambient build backend 的错误假设，改用隔离构建 |
| Public CI `34746649307` | 新 head、attempt 1、`11/11 SUCCESS` |
| `main@8f8af815d1a566bbf35096e318d209bdc17bf7b3` | PR #126 受保护主线合入坐标 |
| Public CI `34747270706` | exact-main、attempt 1、`11/11 SUCCESS` |
| Browser Smoke `34747270771` | exact-main、attempt 1、`1/1 SUCCESS` |

第一次 BP-014 红灯证明测试并未建立它声称验证的隔离构建世界，不是 base package 偷引入 `pywin32`。旧 run
保持失败；后继修正通过新 head 建立新证据，没有用 rerun 或降低验收标准覆盖原事实。

实现后系统俯瞰没有按 finding 数量追求修改，而只修正三个会击穿冻结语义的接缝：

1. local cleanup 曾能错误提交 global release；现在只有拥有全部 resource view 的 controller 可以提交；
2. `RUNNING` enum 曾被误作当前执行资格；现在 create/resume 前均检查同一 absolute deadline；
3. 内部 memory attribution state 曾意外进入顶层公共 API；最终候选删除该导出。

Provider 异常后的 context discard/invalidation，以及任意文件系统 cleanup 的可抢占性，仍留给后继合同所有者；
primitive 不为未知异常伪造原因，也不把有限 helper 扩张成通用 storage cleanup policy。

## 4. 实现候选发布链

[PR #127](https://github.com/NoctilumeDev/VeriTrail/pull/127) 只记录实现候选及三处状态索引：

| 坐标 | 事实 |
| --- | --- |
| `04215568e0d067cdb62edccffc099b99e6d350d2` | 第一个 docs-only candidate head |
| Public CI `34748434202` | attempt 1、`startup_failure`；`jobs=[]`、`check_runs=[]`、无 logs/Artifact |
| `e48d47839dd5d5ff8f8d06b482b1903044bdf566` | 只把首次启动失败写回候选历史 |
| Public CI `34748592992` | 新 head、attempt 1、`11/11 SUCCESS` |
| `main@571139df5db94159f5e439619176f17a02f86f94` | PR #127 受保护主线合入坐标 |
| Public CI `34749049541` | exact-main、attempt 1、`11/11 SUCCESS` |
| Browser Smoke `34749049536` | exact-main、attempt 1、`1/1 SUCCESS` |

第一次启动失败没有实例化任何 test job，因此既不是 required checks 成功，也不能归因为某个产品测试失败。
当时公开状态页未报告 Actions incident，同样不构成 GitHub、代理、仓库或 runner 根因的正向证据。该 run
没有 rerun；后继 green head 保留而不覆盖它。

## 5. 匿名已安装产品读回

读回在 fresh CPython 3.13 venv 中安装已冻结 Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0`
与 `pywin32 312`。安装前重新核对两份公开 Release wheel：

```text
Core:
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence:
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

Core、GitHub Evidence 与 Playwright 均从 fresh venv 的 `site-packages` 导入，不使用 checkout、editable
install 或 `PYTHONPATH`；环境不提供 GitHub token。

### 5.1 保留的首次读回失败

第一次完整读回在 README 的 P1 API 采集收到匿名 GitHub API HTTP 403，返回 `remaining=0`，reset 为
`2026-09-13T09:44:16Z`。同一 paired attempt 的 P2 Render 仍取得 HTTP 200、三次稳定样本、唯一可用 scope、
marker 1、零 coverage/cleanup error 和 zero active stream，但没有 P1 Evidence 就没有 Core PASS，也没有继续
后两个 target。该 output 被保留且未复用；它证明本次匿名 API 额度不足，不授权外推 Collector、GitHub 平台
或代理的更强根因。

### 5.2 reset 后从零建立的完整读回

额度 reset 后从空 output 重新执行三个独立 paired session。每个 target 使用独立 sealed AcceptancePlan，固定
`P1 API -> P2 Render` 顺序、fresh anonymous Chromium context、exact commit Markdown、三样本稳定窗口与预先
声明 marker：

| Target | Coverage / HTTP / samples / scope | Marker | Facts digest | Render Evidence SHA-256 | Report SHA-256 |
| --- | --- | ---: | --- | --- | --- |
| `README.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `bcb05591ca2e12279d336f55f9ab2c946f74581c8a125544b45d3f9fd64d961a` | `cbe9a793d6f7db19fcbb5047c68103beccce0e2c79a8b3b7853a980061cbcc2a` | `8a0e99b7696103dce7622a257be3c9714382404b5193e8e38082d60210cd34d0` |
| `docs/147-r1-derivation-budget-primitive-implementation-freeze-candidate.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `beba34ebf0c8738f56f3a672946baa752377715b263e90c9b25d140bd63d5532` | `2b2f8feda959a5c92bf59c27df527e466829a0dbf5b618dea3bf7bd1dd42aaa4` | `b3de23b28c819c3ef41ae7ab0cd00fce194127c4e90d560a258f64407745a776` |
| `docs/milestones.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `b236f223c4f2d047e15de6cadf6a5c494ca34dd36e718c8a6318f090af6606bf` | `a9b2c10789e68bd46b9db34d3da41e8ab192d5f59ed040778ee3ec0b3a74948e` | `3dea328a1c36a61118a5089900d6c19da3d07a81dedb714a084fed9ee4a91b86` |

三项 Core Verdict 均为 `PASS`；`access_mode` 均为 `ANONYMOUS_FRESH_CONTEXT`。collection errors、coverage
conflicts、cleanup errors 与 active streams 都为 0；requested/final URL 保持 exact SHA 与原 repository path。
summary digest 为 `0b3ae1e8ae68789c3b30253e1b5557e81404a1b754bed383cdac1e38596a988c`。

该读回只证明采集时 GitHub 公共渲染可观察到候选内容，并证明已发布产品可以完成该次 observation 与 Core
验收；它不证明 GitHub 之外的源头真实性，也不赋予 Collector、本文或模型现实真值裁决权。

## 6. 停止线与唯一下一步

本次没有冻结、实现或授权：

- Derivation Attempt、Provider Run、Provider applicability、parser 或 CodeFact runtime；
- FactSet、DerivationEvidence runtime publication 或完整 Derivation Manifest；
- RelationSet、conflict / UNKNOWN 传播、ReviewSliceSet 或 CoverageLedger；
- CLI、Workbench、Core handoff、Q implementation、D product shell、JPyxis 或 AI Execution OS；
- tag、Release、Linux/macOS、容器、恶意代码沙箱、Server/Cloud、并发或分布式能力；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门全部成立后，唯一下一步是从新的 exact main 对 Derivation Attempt / Provider Run / Fact
provenance 接缝再做一轮独立 pre-implementation system audit。审计必须重新检查 attempt identity、provider
run ownership、budget consumption、terminal state、failed-run diagnostics、Fact 双向 provenance 和完整
Manifest eligibility；它可以发现裂缝并分类，但不以 finding 数量为 KPI，也不因发现问题自动修改合同。

该审计不等于实现授权。Provider/parser/Fact 仍须等待后继最小合同明确闭环；Relation、Slice、Coverage、
conflict/UNKNOWN 与完整 Derivation 继续没有施工资格。

## 7. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 AGENTS、README、milestones 并新增本文。提交前必须通过定向 budget/boundary
四矩阵、Markdown 相对链接、精确路径、implementation/main identity、敏感模式与 `git diff --check` 检查。
这些本地结果不替代本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README、本文与 milestones
    -> 状态目标成为当前主线事实
```

任何新反例仍可否决冻结或只重开被击穿的最小边界。不得用文档 147、PR #127 或其匿名读回替代本文自己的
最后门，也不得因为本文是 docs-only 就跳过完整门禁。
