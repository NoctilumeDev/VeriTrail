# R1 DerivationEvidence Schema 0.1.1 修正合同冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_FROZEN /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTATION_ALLOWED /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[R1 DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)
>
> 前置审计：[R1 DerivationEvidence Schema 修正前置审计](139-r1-derivation-evidence-schema-correction-audit.md)
>
> 候选合入基线：`main@2973926358c686d86233dbc2054a2e1f064f13ad`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 DerivationEvidence `0.1.1` Schema 修正合同已经完成审计、本地复验、原始 PR 门禁、受保护
主线合入、新 exact-main 门禁与匿名公共渲染读回的事实。本文不创建或修改 Schema、corpus、identity vector、
测试、runtime、Provider、parser、FactSet、DerivationEvidence Artifact、Relation、Slice、Coverage、Manifest、
CLI、Workbench、Core、P/Q、CI、依赖、tag 或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不能授权 correction implementation。

## 2. 为什么必须新增补丁身份

前置审计在冻结的 `0.1` COMPLETE specimen 上构造单变量反例，确认旧 Schema 会接受：

```text
non-COMPLETED ProviderRun + non-empty reported IDs

non-COMPLETED overall Evidence
    + completed ProviderRun retaining reported IDs
```

同时，旧 Schema 会拒绝 provenance 合同已经要求的：

```text
EXECUTION_MEMORY_BUDGET
EXECUTION_ARTIFACT_BUDGET
```

这不是运行实现缺陷，而是公共验证语言缺少必要语义。文档 126 又已将旧 Schema path、`$id` 与 bytes
逐字节冻结，因此不能在相同身份下原位扩充 enum 或条件约束。合同选择的最小修正是：

```text
historical document/schema = DerivationEvidence 0.1
corrected document/schema  = DerivationEvidence 0.1.1
```

其他 R1 Artifact、Manifest shape 与 semantic digest projection 均不升级。

## 3. 冻结的最小合同

文档 140 只冻结以下变化：

- 新 Evidence document 自描述为 `artifact_kind = DERIVATION_EVIDENCE`、`schema_version = 0.1.1`；
- 新 root 唯一路径为 `schemas/review-derivation-evidence-0.1.1.schema.json`，并拥有新的 `$id` 与 title；
- 历史 `review-derivation-evidence-0.1.schema.json` 与 `tests/fixtures/review-r1-schema-0.1/**` 原字节不变；
- `Diagnostic.diagnostic_code` 只增加 `EXECUTION_MEMORY_BUDGET` 与
  `EXECUTION_ARTIFACT_BUDGET`；
- non-`COMPLETED` ProviderRun 的两个 reported-ID 数组必须为空；
- overall 非 `COMPLETED` 时，每个 ProviderRun 的两个 reported-ID 数组都必须为空，即使某个 run 本身已经
  `COMPLETED`；
- memory containment stop 同时保留 run-local 与 top-level typed diagnostic，并指向同一 active run；
- artifact staging stop 不反写已经完成的 run，只产生 `subject_ref = null` 的 top-level typed diagnostic；
- semantic digest 继续使用 `veritrail.review.derivation-evidence/0.1` domain 与原投影；document payload 中既有
  `schema_version` 自然区分 `0.1` 与 `0.1.1`；
- correction corpus 使用独立 `R1-DE-CV-001..010` namespace，不改写 `R1-CV-001..020`；
- Manifest 仍只绑定实际 Artifact bytes 与 semantic digest，不获得新的 outcome、file set 或 Schema shape。

继续成立：

```text
Historical recoverability != Permission to reuse a public Schema identity
Schema validity != Full derivation conformance
Provider execution status != Published canonical identity summary
Availability diagnostic != Partial canonical Fact authority
Artifact Schema version != Manifest Schema version
```

## 4. 本地候选证据

候选从 exact `main@f69f2818d06834da0d9e8e95288f6f72aada6beb` 建立单一提交：

```text
6f5dcf6dcc3da50d58ac5a308811c5d73372b7e1
docs: define R1 derivation evidence schema correction

tree:
de704b5968abd8f9561150a02c34e8a4cd4ea2c2
```

diff 只有 `AGENTS.md`、`README.md` 与五个 `docs/*.md` 文件，共 7 个文档/状态文件；没有 Schema、corpus、
测试、源码、workflow、依赖或发布坐标变化。

本地完成 docs-only scope、Markdown relative link、敏感模式与 `git diff --check`。现有 R1 Schema/conformance
focused suite 在以下四条 lane 各取得 `22/22`：

| Python | Mode | Result |
| --- | --- | ---: |
| CPython 3.10 | normal | 22/22 |
| CPython 3.10 | `-O` | 22/22 |
| CPython 3.13 | normal | 22/22 |
| CPython 3.13 | `-O` | 22/22 |

旧冻结字节再次复核为：

```text
schemas/review-derivation-evidence-0.1.schema.json
2efbd1d4f73f20fb045c2110136e7f3089e07408b9d496f59c30492a2c3666e7

tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-evidence.json
563664e5675cb861c7c22d4017c97d186a7e370bca4851dbf7bb09df49afb555

tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-31.json
a5f66942a218870d7b4a236244e768ae234a00c5b3cb4c1c1ae3810395cecd48
```

内存中的 Draft 2020-12 feasibility probe 只验证合同条件可表达，没有向仓库写入 Schema 或 fixture。它接受
COMPLETE、memory-budget 与 artifact-budget 三个正例，拒绝 failed run retaining IDs、failed overall retaining
IDs、memory diagnostic 配 completed status，以及 artifact diagnostic 被塞入 run-local diagnostics 的反例。

## 5. PR 候选与受保护主线

[PR #119 `docs: define R1 DerivationEvidence Schema correction contract`](https://github.com/NoctilumeDev/VeriTrail/pull/119)
的 base 为 `f69f2818d06834da0d9e8e95288f6f72aada6beb`，head 为：

```text
6f5dcf6dcc3da50d58ac5a308811c5d73372b7e1
```

原始 [Public CI run 34700914790](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34700914790)
在 attempt 1 取得 11/11；没有失败 job 被 rerun，也没有在门禁运行期间追加提交。PR 于
`2026-09-12T15:13:56Z` 合入：

```text
merge commit:
2973926358c686d86233dbc2054a2e1f064f13ad

tree:
de704b5968abd8f9561150a02c34e8a4cd4ea2c2

parents:
f69f2818d06834da0d9e8e95288f6f72aada6beb
6f5dcf6dcc3da50d58ac5a308811c5d73372b7e1
```

## 6. exact-main 门禁

候选合入后，只接受 exact `main@2973926358c686d86233dbc2054a2e1f064f13ad` 由 push 事件创建的原始
workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34701600940](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34701600940) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34701600927](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34701600927) | 1 | `1/1 SUCCESS` |

PR head、本地 focused suite、旧 main 与 Browser Smoke 单项均未替代 exact-main Public CI 的完整结果。

## 7. 匿名已安装产品读回

读回使用已发布 Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。
导入坐标来自 clean environment 的 `site-packages`，不是 checkout 或 editable install；环境移除 GitHub token，
每个 target 使用独立 sealed AcceptancePlan、fresh anonymous Chromium context、exact commit Markdown 坐标、固定
正文 scope、三样本稳定窗口与预先声明的 literal marker。

| Target | Coverage / HTTP / samples / scope | Marker occurrences | Facts digest | Product canonical Evidence SHA-256 | Report SHA-256 |
| --- | --- | ---: | --- | --- | --- |
| `README.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE`：1 | `d49df8ec2a79cb9ec98b969120dbaa01c71d60aa30290b2e591137ec0564bc29` | `ec00ff364e2228ffc9e9df6312b59625de6e97dd5744520b002c10664eb3b11c` | `3b70ff73c5447ac53481c5da3823f8ea60acce34a4720e9f9df0ebd9de36416e` |
| `docs/139-r1-derivation-evidence-schema-correction-audit.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_EVIDENCE_SCHEMA_PRECONTRACT_AUDITED`：2 | `a9b74d21a14258f0c9455edf709a702e3efbfadc957a5f5b362485b2929c886d` | `c380c8005b1e1b661e83cb3e8bd0f9ca3432b96b31c8e25491eb5befef4d4117` | `5493922ddfb821b66382695d0564739266eca77b183931ae19014d09c903fc08` |
| `docs/140-r1-derivation-evidence-schema-correction-contract.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE`：2 | `44ba8dfc479033aefc66c4b4f45289bc4d8d6985c1b17b3359c66b9d3794f34b` | `9548107868a293ffa2717a22d01ae7d7fce9d1e10b1dc461d453eeff9ab2d87c` | `383b934c905c4d9ffa96c85cb4ebd7d46fc179548b2d564afb30bc3430e04f68` |
| `docs/milestones.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE`：1 | `5389a9b0af37cd35865a065cf1d85906db78c99a310dc1fafd8991071c25d49e` | `75749c2177f6226e43a08400965cfc852b6b993ab39def5e85b2beb66cbb8949` | `65c7ff0f550dc4fc8faf72fc0525f81638d8bfddd05b79b04e66054d29f99890` |

四项最终 Core Verdict 均为 `PASS`；`access_mode` 均为 `ANONYMOUS_FRESH_CONTEXT`；collection errors、coverage
conflicts、cleanup errors 与 active streams 都为 0；requested URL 与 final URL 保持 exact SHA 和原 repository
path。表中的 Evidence SHA-256 是产品对 canonical Evidence bytes 的摘要，不是本地文件包含尾部换行时的原始
文件摘要。

该读回只证明 GitHub 公共渲染在采集时可观察到候选内容，并证明已发布 P1/P2 产品能完成该次匿名观察；它不
证明 GitHub 之外的源头真实性，也不赋予 Collector、脚本或本文 Verdict 权。

## 8. 保留边界与唯一下一步

本次没有冻结、实现或授权：

- wall/memory/artifact budget runtime primitive、Provider runtime、真实 Python parser 或 ambient discovery；
- canonical Fact production、FactSet 或 DerivationEvidence Artifact publication；
- RelationSet、conflict / UNKNOWN 传播、ReviewSliceSet 或 CoverageLedger；
- COMPLETE/DIAGNOSTIC runtime Manifest、Artifact 目录发布、CLI、Workbench 或 Core handoff；
- Q scheduling/cache/lane/reuse、D Desktop、JPyxis、AI Execution OS 或许可证治理操作；
- tag、Release、跨平台、Server/Cloud、多租户、分布式执行或并发能力；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门成立后，当前状态为：

```text
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTATION_ALLOWED
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

唯一下一步是从新的 exact main 建立独立 correction implementation，只物化文档 140 第 7 节允许的
`0.1.1` Schema、corpus 与测试资源。实现候选必须完成自己的兼容向量、双 Python normal/`-O`、完整回归、
原始远端门禁、受保护主线合入、新 exact-main 门、匿名 byte readback 与后继独立状态发布。

correction payload 冻结以前不得开始 budget primitive；即使 payload 冻结，Provider、parser 与 Fact runtime 也
仍须先完成独立 budget primitive feasibility 并取得明确授权。Relation、Slice、Coverage 与完整 Derivation
继续没有施工资格。任何新反例仍可否决后继施工或只重开被击穿的最小边界。
