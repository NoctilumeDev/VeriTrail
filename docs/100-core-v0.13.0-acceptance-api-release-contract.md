# Core 0.13.0 Acceptance API 发布补全合同

> 状态发布目标：`CORE_0.13.0_CONTRACT_FROZEN / C1_NOT_STARTED / P4_BLOCKED / NO_TAG / NO_RELEASE`
>
> 候选门禁、受保护主线合入与合入后匿名产品读回见
> [合同冻结事实](101-core-v0.13.0-acceptance-api-contract-freeze.md)。该状态发布自身的最后门未全部成立前，
> 本文仍按 `CONTRACT_CANDIDATE` 解释。
>
> 发现基线：`main@8e51a03113a54230c5120d7bf5084035c78fe63e`
>
> 影响层级：`L2_CONTRACT`；只补齐已经冻结的 Acceptance Core 公共能力与公开发行坐标之间的缺口，
> 不新增 Acceptance 语义，不重开 P1–P3，不移动任何历史 tag 或 Release

## 1. 发现的事实

P4 最终资产必须从新的 exact main 重建，并用公开稳定 Core wheel 完成仓库外 clean install。该门在
Python 3.10 的全新环境中得到以下反例：

```text
公开 v0.12.2 wheel
SHA-256 3a42f28db6f4ed12351dade3fbb6f57fa1d5aa3fdd6d28210492f676bc1562de
    -> 不包含 veritrail.acceptance_plan

当前 main 的本地 Core wheel
    -> 包含 acceptance_plan / acceptance_evaluation / acceptance_reporting
    -> 仍声明 version = 0.12.2

GitHub Evidence 0.1.0
    -> 精确依赖 veritrail==0.12.2
    -> P3 handoff 与真实 P4 候选门需要上述 Acceptance API
```

公开 `v0.12.2` 标签解引用到
`f961930ae1e69d7d88849fa2b0d40befb3e94c89`；首个通用 Acceptance Core 实现直到后继提交
`0e01dbf3c31631bc62993944d39fbccd79303555` 才进入主线。两份 wheel 使用同一版本号却提供不同公共能力，
因此准备阶段从当前源码构建的 Core wheel 不能替代公开 `v0.12.2` 资产，既有 clean-install 成功也不能
证明插件可由公开坐标复现。

该问题分类为：

```text
PUBLICATION_IDENTITY_MISMATCH
!= plugin implementation regression
!= download availability failure
!= digest failure
```

第一次 Python 3.10 最终矩阵失败必须保留；后继成功不得把它改写成安装命令错误或网络抖动。

## 2. 裁决与版本边界

已冻结的 AcceptancePlan、Acceptance Evaluation、AcceptanceBundle/imported snapshot 公共入口属于新增
能力，而不是 `0.12.2` 的维护补丁。新的公开 Core 坐标因此固定为候选 `0.13.0`，不重制
`v0.12.2`，也不使用 `0.12.3` 把新增公共 API 冒充补丁维护。

`0.13.0` 只允许发布当前主线已经存在且已经分别冻结的 Core 增量：

- PC2 的通用 AcceptancePlan、Evidence binding、四 Verdict evaluator 与 Bundle 入口；
- P3 所需的同一 `ImportedEvidence` snapshot 公共入口；
- 自 `v0.12.2` 后已经独立闭合的 Browser lifecycle/cancellation 修正；
- 与上述公共能力直接相关的 CLI、测试和包装 metadata。

本合同不授权新增 Schema、修改 Verdict 优先级、改变 P1/P2 facts、引入 GitHub 语义、启动 R1，或把
GitHub Evidence 插件打进 Core wheel。Core 仍不得依赖 `veritrail_github`。

## 3. 串行施工顺序

```text
C0  本合同经原始门禁、受保护主线合入与 exact-main 公开读回冻结
    ↓
C1  从新的 exact main 建立 Core 0.13.0 release candidate
    - version / release notes / public entry points
    - 双 Python normal / -O 全回归
    - wheel + sdist clean install
    - Acceptance four-verdict 与 imported-snapshot 纵向门
    - Starter / Workbench / Browser Smoke 兼容回归
    ↓
C2  候选经原始门禁合入后，从新 exact main 重建最终 Core 资产
    - 受保护 annotated tag v0.13.0
    - Core Release 成为 Latest
    - 匿名公开下载、摘要与仓库外复验
    ↓
C3  docs-only 发布事实闭合
    ↓
P4  重开唯一依赖坐标修正
    - veritrail-github-evidence 0.1.0 精确依赖 veritrail==0.13.0
    - 只使用公开下载的 Core 0.13.0 wheel/sdist 重跑最终矩阵
```

前一阶段没有达到出口，后一阶段不得先做。`github-evidence-v0.1.0` 的 tag ruleset、tag、Release、
validation summary 和 checksum 在 Core 0.13.0 公开读回前继续禁止创建。

## 4. 身份与资产停止线

必须始终区分：

```text
source version
!= Git commit
!= annotated tag
!= GitHub Release
!= uploaded asset bytes
!= anonymously downloaded bytes
```

Core 0.13.0 的最低公开资产集合、摘要生成顺序与 Release 说明必须在 C1 明确；任何候选字节都不能在其
准备 PR 合入前成为最终资产。成功文件必须先构建到 owned temporary path，完成 metadata、归档边界、
摘要和安装验证后再以 create-new 方式发布。历史 `v0.12.0`、`v0.12.1`、`v0.12.2` 及其 Release 资产
只读，不移动、不覆盖、不补传。

## 5. C0 出口

C0 只有在以下事实全部成立后才冻结：

1. 本合同及索引只描述已观察到的版本/能力错配，没有把本地构建冒充公开资产；
2. `0.13.0` 被明确为新增 Acceptance 公共能力的独立 Core 版本；
3. P4 被明确阻断，且没有创建插件 tag ruleset、tag、Release、summary 或 checksum；
4. P1–P3、Core evaluator、历史 Release 与既有资产均未修改；
5. 文档链接、敏感信息、版本口径和完整仓库回归通过；
6. C0 候选经原始远端门禁、受保护主线合入与合入后公开读回。

在 C0 冻结以前，下一步只能修正本合同，不能进入 Core 发布实现。
