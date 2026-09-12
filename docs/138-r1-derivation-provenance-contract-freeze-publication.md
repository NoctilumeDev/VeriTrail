# R1 Derivation Attempt 与 Fact Provenance 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_PROVENANCE_CONTRACT_FROZEN /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[R1 Derivation Attempt 与 Fact Provenance 最小运行合同 0.1](137-r1-derivation-attempt-and-fact-provenance-contract.md)
>
> 前置审计：[R1 Derivation Attempt 与 Fact Provenance 前置审计](136-r1-derivation-attempt-and-fact-provenance-audit.md)
>
> 候选合入基线：`main@4893b0062b397adc3983eecb0a7db7c9b24ab4c9`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 Derivation Attempt、Provider Run 与 canonical Fact provenance 合同候选已经完成审计、本地复验、
原始 PR 门禁、受保护主线合入、新 exact-main 门禁与匿名公共渲染读回的事实。本文不修改 R1 Schema/corpus、
runtime、Provider、parser、FactSet、DerivationEvidence、Relation、Slice、Coverage、Manifest、Core、P/Q、CI、
依赖或发布坐标。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不能授权任何 Schema 或运行实现。

## 2. 审计裁决

[前置审计](136-r1-derivation-attempt-and-fact-provenance-audit.md)没有把冻结的 Derivation Input 直接解释成
“可以开始写 parser”。它确认下一层还缺少四组必须先闭合的语义：

```text
exact DerivationInputSet
        ↓
attempt identity + exact request provenance
        ↓
explicit provider applicability
        ↓
one shared absolute execution budget
        ↓
Provider candidate facts
        ↓ application-owned canonicalization
canonical Facts + bidirectional run provenance
```

如果这些边界未冻结，代码会替合同决定 branch provenance、Provider discovery、预算所有权、Fact identity 和
失败运行是否可以污染正式 FactSet。十三个反例因此被压成一个最小合同闭环，而不是被分散到未来实现细节。

## 3. 冻结的合同边界

合同 0.1 冻结以下最小语义：

- `derivation_id` 是 caller-owned opaque attempt identity；同一 attempt 的输入、Provider binding、Profile 与
  execution budget 不能中途漂移，但这些操作数不被重复编码进该字符串；
- `request_provenance` 只来自 SourceSnapshot 已冻结的 exact commit OID，不借用 branch、tag、HEAD、远端
  历史或当前 worktree；
- 0.1 只允许一个显式、required、`CUMULATIVE` 的 `python-ast` Provider binding；不得 ambient discover、
  entry-point 猜测、`sys.path` 扫描、first-success 或 fallback；
- caller 只选择本次允许调用的 Provider capability，不因此赋予 Provider 事实权、Verdict 权或信任等级；
- Input Binding acquisition budget 已经结束；Derivation Attempt 从进入执行态开始创建一个绝对 deadline，
  Provider Run、canonicalization 与终态收束共同消费剩余预算，不得跨阶段刷新；
- wall、memory 与 artifact budget 都控制本次尝试能否完成，不进入 canonical Fact 身份。不同但充分的预算必须
  产生相同规范事实；预算耗尽必须 fail closed；
- Provider 只能返回 candidate facts。application 负责验证 SourceSnapshot 坐标、规范化 payload、生成
  `fact_id` 并建立 `Fact.provider_run_ids ↔ ProviderRun.reported_fact_ids` 双向闭包；
- `provider_id != provider_run_id`；每个进入正式 FactSet 的 Fact 都必须追到同一次 Derivation bundle 中真实、
  terminal 且一致的 Provider Run；
- 只要整个 derivation 不是 `COMPLETED`，每个 Provider Run 的 `reported_fact_ids` 与
  `reported_relation_ids` 都必须为空；失败期间的候选只能留在临时构造/诊断层；
- 本阶段结果是非发布的 owned phase value，不创建 FactSet、DerivationEvidence、Manifest 或 partial Artifact。

其中继续成立：

```text
Provider capability != Fact authority
Provider identity != Provider Run identity
Candidate fact != Canonical Fact
Runtime budget controls completion, not semantic identity
Failed attempt diagnostic != Partial canonical FactSet
Artifact publication != In-memory phase completion
```

## 4. 本地候选证据

候选从 exact `main@7e0950ba2544476049e6defe1545f786971a89bd` 建立两笔独立提交：

```text
ed4e504
  docs: audit R1 derivation provenance boundary

9b93efe60bbdf28e9d36c03f96e762810e57be95
  docs: define R1 derivation provenance contract
```

本地先完成 docs-only scope、Markdown link、敏感模式与 `git diff --check`。第一次总回归使用 15 分钟外层
timeout 且输出被缓冲，终态不能被完整观察，因此没有被算作有效证据。随后按当前 worktree 的 Core、GitHub
Evidence、Review Attention、Starter 与 Authoring Skill source/test roots 重建四条独立 lane。

第一次 CPython 3.10 normal lane 又误写了 Authoring Skill 测试路径；Core 441 项虽已通过，该命令仍被整体
判为无效。按 `.github/workflows/ci.yml` 的真实路径修正后，四条有效 lane 为：

| Lane | Core | Authoring | GitHub Evidence | Review Attention |
| --- | ---: | ---: | ---: | ---: |
| CPython 3.10 normal | 441 | 24 | 180 | 61 |
| CPython 3.10 `-O` | 441 | 24 | 180 | 61 |
| CPython 3.13 normal | 441 | 24 | 180 | 61 |
| CPython 3.13 `-O` | 441 | 24 | 180 | 61 |

四条 lane 全部通过；测试源码与 imported production module 均绑定当前候选 worktree。现有 R1 Schema payload
22 项也在四个 Python/optimization 组合中通过。旧 editable install、超时命令与错误测试路径没有被用于替代
有效终态。

## 5. PR 候选与受保护主线

[PR #117 `docs: define R1 derivation provenance contract`](https://github.com/NoctilumeDev/VeriTrail/pull/117)
的 base 为 `7e0950ba2544476049e6defe1545f786971a89bd`，head 为：

```text
9b93efe60bbdf28e9d36c03f96e762810e57be95
```

原始 [Public CI run 34695173317](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34695173317)
在 attempt 1 取得 11/11；没有失败 job 被 rerun，也没有在门禁运行期间追加提交。PR 于
`2026-09-12T13:15:05Z` 合入：

```text
merge commit:
4893b0062b397adc3983eecb0a7db7c9b24ab4c9

tree:
9a8eeaf8c57b9e19032e9b57977b349d7841d009

parents:
7e0950ba2544476049e6defe1545f786971a89bd
9b93efe60bbdf28e9d36c03f96e762810e57be95
```

候选只修改 `AGENTS.md`、`README.md` 与五个 `docs/*.md` 文件，没有修改源码、Schema/corpus、测试、CI、
依赖、tag 或 Release。

## 6. exact-main 门禁

候选合入后，只接受 exact `main@4893b0062b397adc3983eecb0a7db7c9b24ab4c9` 由 push 事件创建的原始
workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34695903182](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34695903182) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34695903181](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34695903181) | 1 | `1/1 SUCCESS` |

PR head、本地矩阵、旧 main 与 Browser Smoke 单项均未替代 exact-main Public CI 的完整结果。

## 7. 匿名已安装产品读回

读回从公共 Release 下载 Core `0.13.0` 与 GitHub Evidence `0.1.0` wheel，分别独立复核 SHA-256：

```text
Core:
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence:
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

两份 wheel 与 Playwright `1.62.0`、matching Chromium 安装到 clean venv；导入坐标来自 `site-packages`，
不是 checkout 或 editable install。环境移除 `GITHUB_TOKEN`、`GH_TOKEN` 与 `VERITRAIL_GITHUB_TOKEN`。
每个 target 使用独立 sealed AcceptancePlan、fresh anonymous Chromium context、exact commit Markdown 坐标、
固定正文 scope、三样本稳定窗口与预先声明的 literal marker。

| Target | Coverage / HTTP / samples / scope | Marker occurrences | Facts digest | Evidence SHA-256 |
| --- | --- | ---: | --- | --- |
| `README.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE`：1 | `5d029e1ed20b917de9e2a1eeef1607c1c7d7dc15020c58ed7fb9d830c6e8b220` | `974f66610716402b2982bc566fec9a77238f8e214d21365e2f809a705f971e00` |
| `docs/136-r1-derivation-attempt-and-fact-provenance-audit.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_PROVENANCE_PRECONTRACT_AUDITED`：2 | `6730d7c3d40cd9ffc7f115652481f540c4c44b8737cdb4a335c85ceb22fa26a2` | `cd7078cf336e6f4005ff036d97c79bac0d04315955f55352a6ff1e5ac0cadaf7` |
| `docs/137-r1-derivation-attempt-and-fact-provenance-contract.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE`：2 | `0f9826e84f289269959f328144f47a6322757a392188a06fbdc4e66b4910cf56` | `1c09c4a3bd36d9a6e98ef0d4ccbda174c87d633af8a64388321b8b9e129c21ed` |
| `docs/milestones.md` | `COMPLETE / 200 / 3 stable / 1 usable` | `R1_DERIVATION_PROVENANCE_CONTRACT_CANDIDATE`：1 | `06b854b0dcc5a021d97affbc00824c5a9cbe41ad1319af5463b3e427acb72244` | `62b9e21d55af45863325b90d56c269edcd7ce6d4d2f0a57b50295cec4106c2a7` |

四项 `access_mode` 都是 `ANONYMOUS_FRESH_CONTEXT`；collection errors、cleanup errors 都为 0；requested URL
与 final URL 保持 exact SHA 和原 repository path。

第一次 milestones 读回预先声明了该页面并不存在的 marker
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED`。Collector 完成采集后，验收脚本正确拒绝 marker
不匹配；该失败属于 Plan expectation 错误，不是 GitHub、Collector 或正文失败。失败目录被保留，随后用页面
真实存在的候选 marker 和 fresh context 在新目录重新采集。成功重试没有覆盖第一次错误 Plan 的事实。

读回证明采集时 GitHub 公共渲染可观察到候选内容，并证明已发布 P1/P2 产品能完成该次匿名观察；它不证明
GitHub 之外的源头真实性，也不赋予 Collector、脚本或本冻结文档 Verdict 权。

## 8. 保留边界与唯一下一步

本次没有冻结、实现或授权：

- Evidence Schema/corpus 的 memory/artifact budget typed diagnostic 修正；
- wall/memory/artifact budget runtime primitive、Provider runtime、真实 Python parser 或 ambient discovery；
- FactSet、DerivationEvidence、RelationSet、conflict / UNKNOWN 传播、ReviewSliceSet 或 CoverageLedger；
- COMPLETE/DIAGNOSTIC `R1_DERIVATION` Manifest、Artifact 目录发布、CLI、Workbench 或 Core handoff；
- AI proposal、HumanDisposition、Q scheduling/cache/lane/reuse、D Desktop、JPyxis 或许可证治理操作；
- remote fetch、branch/tag/HEAD resolver、版本、tag、Release、跨平台或 Server/Cloud 能力；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门成立后，当前状态为：

```text
R1_DERIVATION_PROVENANCE_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只允许从新的 exact main 建立独立 Schema/corpus correction：增加
`EXECUTION_MEMORY_BUDGET`、`EXECUTION_ARTIFACT_BUDGET` typed diagnostics，并冻结以下兼容不变量：

```text
ProviderRun.status != COMPLETED
    -> reported_fact_ids == []
    -> reported_relation_ids == []

DerivationEvidence.overall_execution_status != COMPLETED
    -> every ProviderRun reports no canonical Fact or Relation identity
```

该 correction 必须拥有自己的合同/兼容向量、远端门禁、受保护主线合入与冻结闭环。它完成前不得开始 budget
primitive、Provider、parser、Fact provenance runtime，更不得越过 Relation、Slice、Coverage 或完整 Derivation。
任何新反例仍可否决后继施工或只重开被击穿的最小合同边界。
