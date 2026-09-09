# Review Attention R1 合同冻结状态发布

> 状态发布目标：`R1_CONTRACT_FROZEN / R1_SCHEMA_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`
>
> 候选合同：[文档 113](113-r1-deterministic-semantic-slice-contract.md)
>
> 候选提交：`d93e70321fa9db15ac31f5048f9091d59c954dfd`
>
> 候选合入基线：`main@617e99ddd8217fbcaf26037c0f9ac15014795f15`
>
> 影响层级：`L0_DOCUMENTATION + L2_CONTRACT_STATUS`；本文只发布已经发生的合同候选、门禁、
> 受保护主线合入与公开读回事实，不创建 Schema、源码包、CLI、运行 CI、Provider、标签或 Release

## 1. 发布裁决

文档 113 已把 R1 0.1 的首个确定性语义切片边界固定为：

```text
Exact SourceSnapshot
    -> deterministic CodeFacts
    -> typed structural Relations
    -> bounded overlapping ReviewSlices
    -> staged CoverageLedger
```

首个 Analysis Profile 只承诺 Python 3.10 结构语义；未支持语言、generated/vendor、跨语言边界、动态调用、
预算截断和解析失败必须保留为显式分母、`PARTIAL`、`UNSUPPORTED` 或其他合同规定的不确定状态。它不把
支持子集外推成整个仓库已被理解，也不允许 Slice、Analyzer、Attention Proposal 或 HumanDisposition
彼此取得对方的权威。

候选合同已经完成自己的原始远端门禁、受保护主线合入、合入后 exact-main 门禁和三次 fresh anonymous
产品读回。本文只发布这条已经形成的候选闭环，不补写 Schema，也不把合同冻结冒充 R1 实现。本文自身
仍须经过原始远端门禁、受保护主线合入和合入后 exact-main 匿名读回；只有该链全部成立，状态发布目标
才成为当前主线事实。任何新反例仍可否决冻结资格。

## 2. 候选身份与受保护主线

| Identity | Exact value |
| --- | --- |
| Candidate base | `9ab64121350b69ce81e6be79961ad426026bbc39` |
| Candidate commit | `d93e70321fa9db15ac31f5048f9091d59c954dfd` |
| Candidate tree | `7a5de488b5da563900a749ffd8b02c116d72fb3f` |
| Pull request | [#89 `docs: define R1 deterministic semantic slice contract`](https://github.com/NoctilumeDev/VeriTrail/pull/89) |
| Merge commit | `617e99ddd8217fbcaf26037c0f9ac15014795f15` |
| Merge parents | `9ab64121350b69ce81e6be79961ad426026bbc39` + `d93e70321fa9db15ac31f5048f9091d59c954dfd` |
| Merge tree | `7a5de488b5da563900a749ffd8b02c116d72fb3f` |

PR #89 只修改 `AGENTS.md`、`README.md`、R 轨 Plan、里程碑索引并新增文档 113；没有 Schema、源码、
CLI、CI、Provider、标签或 Release。它于 `2026-09-09T21:06:42Z` 通过正常受保护分支流程合入，候选
tree 与 merge tree 一致，没有在合入时改写候选 payload。

## 3. 候选原始远端门禁

PR #89 的 Public CI run `34385349686` 在 attempt 1 生成并完成 11 个 job，全部为 `SUCCESS`：

1. Workbench tests, lint, build, and audit；
2. Python 3.10 on Windows；
3. Python 3.13 on Windows；
4. E3 0.2 release download acceptance；
5. Wheel-only first run on Python 3.10；
6. Wheel-only first run on Python 3.13；
7. GitHub Evidence wheel-only on Python 3.10；
8. GitHub Evidence wheel-only on Python 3.13；
9. Acceptance Core freeze on Python 3.10；
10. Acceptance Core freeze on Python 3.13；
11. Starter PASS/FAIL golden path。

没有失败 job 被 rerun 洗白，也没有用旧 PR 或旧 main 的绿灯替代候选 head。

## 4. 合入后 exact-main 门禁

合入后只接受精确 `617e99ddd8217fbcaf26037c0f9ac15014795f15` 上由 push 事件创建的运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34405045985`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34405045985) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34405046002`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34405046002) | 1 | `1/1 SUCCESS` |

该事实只证明合入后的仓库门禁成立；它不能替代匿名公开渲染，也不能把 docs-only 合同变成运行能力。

## 5. 匿名产品读回

读回使用公开发布的 Core `0.13.0` 与 GitHub Evidence Plugin `0.1.0` wheel，从隔离环境的
`site-packages` 导入；未提供 `GITHUB_TOKEN` 或 `GH_TOKEN`，浏览器使用插件要求的 matching Chromium。
三次 P1 API -> P2 Public Render -> Core 配对 session 均绑定 exact merge commit，并分别取得 `PASS`：

| Target | Required marker | API Evidence SHA-256 | Render Evidence SHA-256 | Acceptance report SHA-256 |
| --- | --- | --- | --- | --- |
| `README.md` | `R1_CONTRACT_CANDIDATE` | `e38081751491c19233361edbc73f6e826f5019539605a6fdae8fad0b6a1b9dec` | `cdccb4c3b2185e40e454a4303136270f8b105a628bfb456c1b2ba25feafe6235` | `c8c7bd73dfa88fa9d1f1726598a00dccf2bcaa14f164cacc4e34b2bd949d17eb` |
| `docs/113-r1-deterministic-semantic-slice-contract.md` | `R1_SCHEMA_NOT_STARTED` | `5ab0cedc1169409b531a12c1d2ae6e7185a33ed1ed18303bee4aed885d4c4d32` | `49679a635c2a2367b8643bae5a068b273cba4938e424867a00d4aeba4efa99c1` | `bc5c19b11d1f903f87de68e3ddf5d8ad96c06392471b84c07d562adabc247bc1` |
| `docs/milestones.md` | `R1_CONTRACT_CANDIDATE` | `9836fe77a8d10e419e49747ac4d20ba446ef6a26593cc3d27ca84f8363699938` | `f82159a6daa9270f1da45445dc1d42101831adbb56d5c652a84bc50a46c7f78d` | `2ca185bf2b3b423ff4a9c71fe53adb773cf0e843cb31d134f26b13ebdb7d01d1` |

三次 session ID 分别为：

```text
github-paired-58abd9059573467a91bb66ffaf0129a9
github-paired-8d51c9868de5417e8719674226f6901f
github-paired-8ffe1095327741739ffb00ed4fda404f
```

这些读回只证明精确公开坐标、API/Render Evidence、要求标记与 Core 规则在各自 session 内闭合；三个
session 不构成 GitHub 原子快照，也不被描述成三个独立信任域。

## 6. 冻结对象

冻结对象是文档 113 中的 R1 0.1 合同语义，包括：

- `SourceSnapshot / AnalysisProfile / CodeFact / Relation / ReviewSlice / CoverageLedger` 五层身份与依赖；
- Python 3.10 首版支持边界及 unsupported/generated/vendor/cross-language 分母；
- `Fact != Interpretation`、`Slice != Partition`、`Unknown != Absent`、`Truncated != Complete`；
- 快照一次读取形成同一 owned snapshot，再供 inventory、facts、relations、slices 与 coverage 消费；
- relation 来源不得混成统一 confidence，slice derivation、analysis 与 attention ranking 保持分权；
- `RA-003 / RA-004 / RA-008 / RA-023` 到设计约束、最小反例和非声明的追溯关系；
- Schema 与规范字节在合同冻结后的独立阶段才允许定稿。

文档 113 首屏继续保留其候选时点与设计基线，不被本文批量重写成“它从一开始就已冻结”。当前事实由
本状态发布外部绑定，保持 `Contract History != Current State Publication`。

## 7. 未产生的能力

截至候选合入基线，以下事实仍然不存在：

```text
no R1 Schema
no R1 canonical-byte vector
no SourceSnapshot importer
no Python parser / compiler adapter
no CodeFact or Relation graph runtime
no ReviewSlice derivation
no CoverageLedger producer
no R1 CLI or runtime CI
no Analyzer / AI / ranking Provider
no R1 tag or Release
```

`R1_SCHEMA_DRAFTING_ALLOWED` 只解除 Schema 设计停止线。它不等于 `R1_SCHEMA_FROZEN`，更不等于
`R1_IMPLEMENTED`。下一阶段只能从本状态发布闭环后的新 exact main 串行建立 Schema、规范字节和兼容
向量；若 Schema 设计暴露合同级反例，必须停止并显式重开对应合同边界。

## 8. 本状态发布的最后门

本补丁只允许本文、README、AGENTS、R 轨 Plan 与里程碑索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 使用公开 Core `0.13.0` 与 GitHub Evidence Plugin `0.1.0` 的产品链，fresh anonymous
   读取 README、本文和里程碑索引；
5. 三页均须保持 exact-SHA URL、HTTP 200、唯一 usable scope、`COMPLETE`、三样本稳定、指定 marker
   存在，且没有 error、conflict 或 cleanup error；
6. 确认 diff 中仍无 Schema、源码包、CLI、运行 CI、Provider、标签或 Release。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_DRAFTING_ALLOWED
R1_IMPLEMENTATION_NOT_STARTED
```

任一新反例都会否决本次状态发布。后继不得从本分支直接叠加 Schema 或实现，必须从完成读回后的新
exact main 重新建立独立施工坐标。
