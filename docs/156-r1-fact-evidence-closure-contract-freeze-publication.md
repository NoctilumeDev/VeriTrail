# R1 Fact Admission / DerivationEvidence Closure 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_FACT_EVIDENCE_CLOSURE_CONTRACT_FROZEN /
> R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_ALLOWED /
> R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 前置审计：[Fact Admission 与 DerivationEvidence Closure 系统审计](154-r1-fact-evidence-closure-system-audit.md)
>
> 冻结对象：[Fact Admission / DerivationEvidence Closure 最小合同 0.1](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)
>
> 候选合入基线：`main@3c237555b4924f08b7e82c523f675fbd28512e3c`
>
> 候选合入 Tree：`b2bc95fbc51f57cd895634361b5fdae81baad6cf`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 155 的合同候选已经完成本地合同验证、原始远端门、受保护主线合入、新 exact-main 门、
fresh anonymous installed-product readback 与第二轮系统级冻结审计的事实。本文不创建或修改 runtime、Schema、
corpus、identity vector、测试、Provider、parser、FactSet/Evidence publisher、Relation、conflict/UNKNOWN、Slice、
Coverage、Manifest、CLI、Workbench、Core、P/Q/D、依赖、CI、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及
针对本文合入坐标的 fresh anonymous 产品读回。只有这些最后门全部成立，状态目标才成为当前主线事实；在此
以前，本分支文字不授权任何实现。

## 2. 本次冻结的最小边界

本次只冻结：

```text
same private integrated controller
  owns admitted DerivationInputSet
       + one BudgetContext
       + one attempt eligibility gate
       + one Provider binding
        ↓
consume the exact copy-owned Execution Cell phase result
        ↓
application-canonical Fact admission
        ↓
owned non-published FactSet construction state
        +
owned non-published final-outcome Evidence projection
        ↓
normal continuation / future diagnostic closure / cleanup-only
remain three different capabilities
```

它没有冻结公共 Artifact publication。`fact-set.json`、`derivation-evidence.json` 与 `manifest.json` 在当前切片均不
落盘；完整 derivation 仍须等待 RelationSet、ReviewSliceSet、CoverageLedger 与八文件 closure。

## 3. 已冻结不变量

### 3.1 四层 Fact 不能压成一个状态

```text
Provider candidate observation
!= application-canonical Fact
!= admitted FactSet member
!= published Fact Artifact member
```

canonical identity 成立只说明 application 能复算源码事实；它不自动取得 FactSet membership，更不取得文件、
Manifest role 或 publication authority。首个 single-Provider FactSet admission 必须重新验证 exact input continuity、
Fact identity、排序去重、双向 reported-ID/provenance closure 与 provenance-free `fact_set_digest`。

### 3.2 phase 与 final Evidence 是不同 immutable projection

phase reported IDs 记录该 phase 曾经成功提交的 application-canonical identities；final Evidence reported IDs 只
允许引用最终发布的 normal FactSet/RelationSet。后继阶段失败时，已经完成的 ProviderRun status 不被改写，但
new-copy final Evidence 的全部 reported arrays 必须为空。成功 Fact phase 当前只建立 construction state，不提前
构造 provisional `COMPLETED DerivationEvidence`。

### 3.3 terminal diagnostic placement 没有实现自由度

首个 active single-Provider run 的七种 terminal code 使用以下固定状态：

| Diagnostic code | ProviderRun | Evidence |
| --- | --- | --- |
| `PROVIDER_UNAVAILABLE` | `UNAVAILABLE` | `UNAVAILABLE` |
| `PROVIDER_FAILED` | `FAILED` | `FAILED` |
| `NONCONFORMANT_PROVIDER_OUTPUT` | `FAILED` | `FAILED` |
| `INTERNAL_DERIVATION_ERROR` | `FAILED` | `FAILED` |
| `EXECUTION_DEADLINE` | `INTERRUPTED` | `INTERRUPTED` |
| `EXECUTION_CANCELLED` | `INTERRUPTED` | `INTERRUPTED` |
| `EXECUTION_MEMORY_BUDGET` | `INTERRUPTED` | `INTERRUPTED` |

每个 code 都必须以同一个 exact `PROVIDER_RUN` subject tuple 在 run-local 与 top-level diagnostics 中各出现恰好
一次。`EXECUTION_ARTIFACT_BUDGET` 则只在 top-level 以 `subject_ref=null` 出现；已完成的 run 保持
`COMPLETED`，overall 为 `INTERRUPTED`，全部 final reported arrays 为空。Schema 只验证 shape；这些 placement、
cardinality 与 cross-object 约束属于 conformance。

### 3.4 三种能力与一个预算不能混用

normal continuation、future DIAGNOSTIC closure eligibility 与 cleanup-only permission 不是一个 boolean。只有拥有
合法 non-success phase result、没有预算 stop、release 已完成、原 BudgetContext 仍为 `RUNNING`、deadline 未到、
没有 cancel/memory/artifact latch、artifact reservation 为零且 normal continuation 已 revoke 的 attempt，才可能
取得一次性 future DIAGNOSTIC eligibility。

deadline、caller cancellation、positive memory stop、artifact reservation stop 与 `RELEASE_FAILED` 只有 cleanup
或调用层 typed result，不发布 R1 Artifact。不得重建 BudgetContext、刷新 deadline、退还 reservation、申请第二
份 artifact budget，或为了记录 stop 在 stop 后重新启动 DIAGNOSTIC staging。

### 3.5 Schema expressibility 不等于 runtime publication authority

`DerivationEvidence 0.1.1` 与既有 COMPLETE/DIAGNOSTIC Manifest 能表达某些形状，不代表当前 reference
runtime 已获得发布能力。因此本次不升级公共 Schema、corpus、identity domain 或 digest projection；文档
120、145、150 只修正了由审计 154 证明不可同时满足的 residual wording，没有以新文档覆盖旧合同。

## 4. 候选、门禁与合入事实

### 4.1 候选坐标

合同候选从 exact `main@0b2ca79191adc3743b2cf4663cd0cda7574a7912` 起草：

```text
candidate head = a9eb0c77c311423c14104f50de87a1604438e4e4
candidate tree = b2bc95fbc51f57cd895634361b5fdae81baad6cf
merge commit  = 3c237555b4924f08b7e82c523f675fbd28512e3c
merge parents = 0b2ca79191adc3743b2cf4663cd0cda7574a7912
                a9eb0c77c311423c14104f50de87a1604438e4e4
merge tree    = b2bc95fbc51f57cd895634361b5fdae81baad6cf
```

候选只新增文档 155，并修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 与文档 120/145/150 的必要
residual wording；没有 runtime、Schema、corpus、vector、test、dependency 或 CI 变化。

### 4.2 本地候选证据

候选 head 的 R1 Schema/identity/Evidence 定向矩阵在 CPython 3.10/3.13 normal/`-O` 四格均为 `27/27`；
Review Attention 完整矩阵四格均为 `113/113`：

| Runner | Schema / Evidence | Review Attention full |
| --- | ---: | ---: |
| CPython 3.10 normal | `27/27` | `113/113` |
| CPython 3.10 `-O` | `27/27` | `113/113` |
| CPython 3.13 normal | `27/27` | `113/113` |
| CPython 3.13 `-O` | `27/27` | `113/113` |

第一次完整矩阵调用使用了短于测试所需的外层工具 timeout；遗留的 exact Python child 被显式终止并确认无
残留，该次结果作废。上表来自随后重新启动的四次独立完整运行，不用后续结果覆盖失败的调用事实。

### 4.3 PR #136 与 exact-main 门

[PR #136](https://github.com/NoctilumeDev/VeriTrail/pull/136) 的 base/head 为
`0b2ca79191adc3743b2cf4663cd0cda7574a7912` / `a9eb0c77c311423c14104f50de87a1604438e4e4`。
原始 [Public CI run 34793979272](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34793979272)
为 attempt 1、11/11 SUCCESS，没有 rerun；候选随后以普通 merge commit 合入受保护 `main`。

`main@3c237555b4924f08b7e82c523f675fbd28512e3c` 的新门为：

```text
Public CI      run 34794900875  attempt 1  11/11 SUCCESS
Browser Smoke run 34794900949  attempt 1   1/1 SUCCESS
```

## 5. fresh anonymous installed-product readback

读回使用 fresh CPython 3.13.13 venv；Core 0.13.0、GitHub Evidence 0.1.0、Playwright 1.62.0 与 matching
Chromium 均从该 venv 的 `site-packages` 导入，而非仓库 checkout。公开 Release wheel 的复算 SHA-256 为：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

清空 `GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 后，针对 exact `3c237555...` 建立三次互不复用的
`P1 API -> P2 Render -> P3 handoff -> Core` session：

| Target | Viewport | Marker / count | HTTP | P1/P2 coverage | Stable | Core |
| --- | --- | --- | ---: | --- | --- | --- |
| `README.md` | `DESKTOP_1365X768` | `R1_FACT_EVIDENCE_CLOSURE_CONTRACT_CANDIDATE` / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md` | `NARROW_390X844` | `R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED` / 2 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/milestones.md` | `NARROW_390X844` | `R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED` / 1 | 200 | COMPLETE / COMPLETE | true | PASS |

三次 requested/final URL 均为同一 exact commit/path，redirect chain 只有最终 HTTP 200；三样本规范化结果稳定，
没有 coverage reason、conflict、cleanup error 或未关闭 stream。访问模式分别保持 `ANONYMOUS` 与
`ANONYMOUS_FRESH_CONTEXT`，且 P1/P2 都不声称 atomic snapshot。

三次 session / Plan / handoff / P1 Evidence / P2 Evidence / report identity 均两两不同：

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-61870d03ad6145bf88ae24045bc31b60` | `ce4760de7dca...` | `739889a46411...` | `76945efaeaa4...` | `d053dcc549ec...` | `9c150c5e1c1f...` |
| Contract 155 | `github-paired-1bee4e2b06dd4b71a1bb2897a0579482` | `3f2839d20793...` | `409c5be31b4f...` | `f8b861ba79e0...` | `54fbf2df6906...` | `212c8c2be00a...` |
| Milestones | `github-paired-8ea90249b94043abad1e19d37f4020fc` | `a55aea62bb5b...` | `75786f80230b...` | `fc007243d95e...` | `b24cdf9681d1...` | `e2d01fbd3afc...` |

一次 ambient Python 调用因没有安装 `veritrail_github` 在参数处理前失败，一次 milestones 调用因工作目录拼写
错误在进程创建前失败；两者都没有产生 Evidence。另一次 PowerShell 检查错误地把 Hashtable object identity
当作 URL value equality，结论被作废；字段与 canonical bytes 复核证明三次 requested/final URL 精确相等。

这些读回只证明候选合入坐标的公开页面与已安装产品链可以共同成立，不替代本文自己的最终门。

## 6. 第二轮系统级冻结审计

第二轮审计从 candidate exact main 独立进行，不以 finding 数量为目标。它重新检查审计 154 的十八个反例、
文档 155 的二十四项未来 conformance 义务、文档 120/145/150 residual 修正、Schema/corpus 边界、预算所有权、
terminal capability 与 public publication stop line。

### 6.1 机械终态 probe

使用 CPython 3.13、`jsonschema` Draft 2020-12 validator 与现有 `DerivationEvidence 0.1.1` Schema/correction
fixture，在内存中逐一构造 7 个 active-run terminal projection 与 1 个 artifact-budget projection。每个向量都：

- 通过当前 Schema；
- 满足合同固定的 run/overall status；
- 保持全部 reported Fact/Relation IDs 为空；
- 满足 run/top-level exact tuple cardinality，或 artifact-budget 的 top-only/null 规则；
- 从完整 projection 复算稳定的 `derivation_evidence_digest`。

| Vector | Run | Overall | Recomputed digest |
| --- | --- | --- | --- |
| `PROVIDER_UNAVAILABLE` | UNAVAILABLE | UNAVAILABLE | `674b220a7aa5e2eb2bab41263080b1fcf64a5e16be811f57bb9d84eaa8efb7a4` |
| `PROVIDER_FAILED` | FAILED | FAILED | `220c3b1cb7b519ba40bbff589f20e20c48912f805a1921d2a25ac2a6d8e2e059` |
| `NONCONFORMANT_PROVIDER_OUTPUT` | FAILED | FAILED | `21658e843e9a711759f73cbfddac11d992c792c07c652feea980bc5db3ba1d4d` |
| `INTERNAL_DERIVATION_ERROR` | FAILED | FAILED | `443519cf5912db8da8d52262cb69811fda484864592e09f2ff5db67fefd319fd` |
| `EXECUTION_DEADLINE` | INTERRUPTED | INTERRUPTED | `cb9267e04744f8b84c7b34ef77d9ffbb21ed80b253b94578b9530d0ad5fe40ff` |
| `EXECUTION_CANCELLED` | INTERRUPTED | INTERRUPTED | `1c3cc4b0f04c9d2e1b97552038eb5cde7d62bdb839f95b1d964d21b745347f9d` |
| `EXECUTION_MEMORY_BUDGET` | INTERRUPTED | INTERRUPTED | `960e52c8b97ee25a8025df6bfbee1bf300940086937ada54c101e68d3cd0e953` |
| `EXECUTION_ARTIFACT_BUDGET` | COMPLETED | INTERRUPTED | `1102c6e82177e779ed7c790d41033f764b15cf5eab999114c7f6f8f7c96d3b6e` |

这些是 freeze-audit in-memory specimens，不是新增 corpus、公共兼容向量或 runtime output。

### 6.2 本发布的聚焦本地门

冻结发布分支从 exact candidate main 串行绑定当前 worktree 的 Core `src`、Review Attention `src` 与 test root；
不复用 ambient editable install。结果为：

| Runner | Schema / Evidence | Public boundary | Markdown safety |
| --- | ---: | ---: | ---: |
| CPython 3.10 normal | `27/27` | `7/7` | `4/4` |
| CPython 3.10 `-O` | `27/27` | `7/7` | `4/4` |
| CPython 3.13 normal | `27/27` | `7/7` | `4/4` |
| CPython 3.13 `-O` | `27/27` | `7/7` | `4/4` |

相对链接、fence、状态 marker、敏感模式、本地绝对路径、exact diff scope 与 `git diff --check` 也全部通过。
候选 tree 已经完成四格 `113/113` Review Attention 完整回归，candidate exact main 又完成新的 11 项远端
全仓门；本 docs-only 状态发布不为增加测试数量而重复运行本地完整矩阵，远端 PR 仍必须重新执行全部门禁。

### 6.3 审计裁决

没有发现新的 freeze blocker。审计确认：

1. 审计 154 的十八个反例均由文档 155 的 identity、projection、capability 或 publication stop line 唯一裁决；
2. 所有 active-run terminal code 与 artifact-budget 的形状都能由现有 Schema 表达，不需要 Schema revision；
3. `INTERNAL_DERIVATION_ERROR` 仍是不声明 Provider、transport、application 或 OS 根因的 fallback，不获得
   Provider blame；
4. output coordinate、public publisher、真实 parser/Provider SPI、multi-provider conflict/UNKNOWN、Relation、
   Slice、Coverage 与完整 Manifest 都是明确延期边界，不是本合同被遗漏的实现自由度；
5. candidate tree 与 merge tree 相同，remote `origin/main` 仍精确位于 `3c237555...`，没有并行主线漂移。

因此冻结文档 155 不需要新的语义修正。发现延期风险不等于现在必须解决；本轮只确认它们没有被当前合同
伪装成已关闭能力。

## 7. 实现授权与停止线

本文自己的最后门全部成立后，只允许从新的 exact main 按文档 155 第 13 节 A–F 施工：

```text
private integrated-controller composition boundary
application-canonical Fact admission
owned non-published FactSet construction state
immutable phase-vs-final ProviderRun projection
canonical diagnostic placement / cardinality conformance
owned non-published DerivationEvidence projection
FA-001..024 hardening
```

仍未授权：

- output path、artifact writer、public publisher 或任何 R1 Artifact 文件；
- real parser、public Provider SPI、ambient discovery 或新 runtime dependency；
- Relation、cross-provider conflict/UNKNOWN、Slice、Coverage 或完整八文件 Derivation closure；
- CLI、Workbench 写入、Core 新判断、P/Q/D implementation、tag 或 Release；
- hostile-code sandbox、Linux/macOS cell、Server/Cloud、并发、分布式或多租户能力。

首个实现完成后仍只能进入自己的实现冻结候选，不能把合同冻结直接写成 runtime frozen。若实现反例击穿
Fact membership、projection identity、budget continuity 或 capability matrix，必须停止并只重开被击穿的最小边界。

## 8. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过
聚焦回归、Markdown 相对链接、fence/heading、状态 marker、敏感模式、scope 与 `git diff --check`。这些本地
结果不替代本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / docs 156 / milestones
    -> 状态目标成为当前主线事实
```

任一新反例都可否决冻结。不得用文档 155、PR #136、候选 exact-main 门或其匿名读回替代本文自己的最后门，
也不得因为本文是 docs-only 就跳过完整门禁。
