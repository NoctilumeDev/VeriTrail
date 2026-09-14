# R1 Fact Admission / DerivationEvidence Closure 实现冻结发布

## 1. 文档身份

> 状态目标：`R1_FACT_EVIDENCE_CLOSURE_FROZEN /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[Fact Admission / DerivationEvidence Closure 最小合同 0.1](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)
>
> 合同冻结：[Fact Admission / DerivationEvidence Closure 合同冻结发布](156-r1-fact-evidence-closure-contract-freeze-publication.md)
>
> 实现候选：[Fact Admission / DerivationEvidence Closure 实现冻结候选](157-r1-fact-evidence-closure-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@a4c63607d8a586a5ec19eae1cdc4279cda1ffa88`
>
> 候选合入 Tree：`862f3c4d05682fe2389537d5c1cb4d93093abe6b`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 155/156 冻结的 private Fact/Evidence closure 已按文档 157 完成实现、实现后系统审计、
候选门禁、受保护主线合入、新 exact-main 门禁与 fresh anonymous installed-product readback 的事实。本文不
创建或修改源码、测试、Schema、corpus、identity vector、依赖、CI、Provider、parser、output publisher、
Relation、conflict/UNKNOWN、Slice、Coverage、Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，
以及针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为
当前主线事实；在此以前，本分支文字不授权 Relation、Slice、Coverage、publisher、parser 或其他后继实现。

## 2. 本次冻结的最小对象

本次冻结只覆盖一个 private、non-published implementation closure：

```text
same prepared Derivation attempt
  owns exact inputs + binding + BudgetContext + eligibility
        ↓
consume the same immutable Execution Cell phase snapshot once
        ↓
application-canonical Fact admission
        ↓
owned non-published FactSet construction state
        +
owned non-published DerivationEvidence projection
        ↓
normal continuation / one-shot diagnostic eligibility / cleanup-only
remain separate capabilities
```

该对象没有 output coordinate、Artifact writer、publisher 或 Manifest role。它不会把 candidate、canonical Fact、
admitted member 与 published Artifact member 压成一个状态，也不会把 Schema 可表达的 terminal projection 解释为
runtime 已拥有 publication authority。

## 3. 已冻结不变量

### 3.1 verified snapshot 与 consumed snapshot 相同

integrated controller 消费同一个 one-shot prepared attempt 与同一次 execution call 返回的 immutable phase value；
它不重建 BudgetContext，不刷新 absolute deadline，也不按路径、transport 或 Provider state 二次读取。因此：

```text
verified attempt snapshot = admission/projection consumed snapshot
path identity or serialized copy != continuation authority
```

### 3.2 Fact 的四层身份继续分离

```text
Provider candidate
  != application-canonical Fact
  != admitted FactSet member
  != published Fact Artifact member
```

Fact admission 重新验证 input/binding continuity、anchor、scope、profile、Fact identity、单一 provenance、排序去重与
双向 reported-ID closure。成功只形成 copy-owned construction state；没有路径、Manifest role 或 public lifecycle。

### 3.3 phase 与 final Evidence 是不同 immutable projection

phase `ProviderRun` 可以保留已经成功提交的 canonical Fact IDs；后继 terminal projection 必须按冻结规则构造新值。
non-success 或 downstream artifact stop 不得原地改写 phase，也不得把 phase IDs 偷渡进 final reported arrays。

### 3.4 terminal capability 与 publication authority 不同

normal continuation、future DIAGNOSTIC closure eligibility 与 cleanup-only permission 不是一个 boolean。只有文档 155
允许的 non-budget terminal、仍然 `RUNNING` 的原 BudgetContext、已经完成的 release、零 artifact reservation 与
尚未出现 stop latch 共同成立时，才可能获得一次性 private diagnostic claim。

deadline、caller cancellation、positive memory stop、artifact reservation stop 与 release failure 不取得 R1 Artifact
publication 权。private helper 能构造 Schema-valid terminal shape，只证明 conformance capability，不证明 writer、
reservation、path 或 Manifest 已经存在。

### 3.5 runtime budget 不进入 Fact 语义

同一 BudgetContext 只控制本次执行是否仍有资格完成。只要不同充分预算都完成同一输入与 binding，canonical Fact
bytes、Fact identity 与 provenance-free `fact_set_digest` 必须相同；timeout、retry history 与宿主恢复事实不能进入
源码事实身份。

## 4. 实现、审计与打包事实

实现从冻结合同 exact main `23b07d6059d13107044746b2a4627c26f302bb4f` 施工，并在独立 CI capacity 修正后以
相同 patch-id rebase：

```text
original implementation head = 4b390ac37839fa8b65ec9202c4a1e0e46152a17e
final implementation head    = 8b397fc70d444048a2c8fcd04ccc00cb593fa1b1
implementation merge         = 86b62464b9eef00a5e9da8d0549f093767be27e2
implementation tree          = 8bfd7a404b73057365c58b5493e3a10d4a074450
patch-id                     = c6a6162cf93df276c7db1734d732a72b27da9177
```

实现只修改五个文件，新增 private integrated controller、owned non-published FactSet construction state、
non-success Evidence projection 与 one-shot diagnostic eligibility。源码 diff 为 1626 insertions、2 deletions；
顶层包没有新增 export，base dependency surface 没有变化。

实现后系统审计逐条映射 FA-001..024，没有发现需要重开冻结合同的新 blocker。重点确认：

1. execution 与 admission/projection 共用同一 BudgetContext、absolute deadline 与 eligibility；
2. controller 消费同一次 execution call 的 immutable phase value，不重新定位或读取；
3. construction bytes 没有 output path、writer、reservation、publisher 或 Manifest role；
4. stop projection 的形状能力没有被提升为 stop 后 publication 权；
5. 对外值由 canonical bytes 重建 owned copy，调用方 mutation 不改变 controller state；
6. private closure 没有进入公共 package surface。

实现 head 的 Review Attention 完整回归在 CPython 3.10/3.13 normal/`-O` 四格均为 `133/133`；focused
Fact/Evidence closure + boundary gate 四格均为 `27/27`。隔离构建与安装证据为：

```text
veritrail_review_attention-0.1.0.dev0-py3-none-any.whl
SHA-256 a2276e192d8f1bba636f6a14d7bda80f6342d64a1f493e588b79bf160cbb7e40
```

fresh `-I` child 从 isolated `site-packages` 导入该 wheel；private closure 未由顶层包导出，`win32api` 未加载。

## 5. 保留的首次失败与独立 CI capacity 修正

[PR #140](https://github.com/NoctilumeDev/VeriTrail/pull/140) 首次 pre-rebase
[Public CI run 34819121759](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34819121759) 在 Python 3.10
aggregated job 到达既有 15 分钟 outer timeout 后被取消。取消前产品测试与 E1 asset download/digest 已通过，但
clean-install acceptance 尚未闭合；该结果没有称为 flake，也没有用后续成功覆盖。

独立 [PR #141](https://github.com/NoctilumeDev/VeriTrail/pull/141) 只把 aggregated Python lane 的 CI outer
containment 从 15 分钟调整为 20 分钟：

```text
repair head  = 2b51cb607588bf220e19cf23715210324584d028
repair merge = cee30f68db1693eb9185cda7a827a2629660c621
repair tree  = 3d3da8af5ef73823fa97877198326b0476c73bdf
```

PR #141 原始 run `34820959395` 为 attempt 1、11/11 SUCCESS；repair exact main 的 Public CI `34822412395`
为 11/11、Browser Smoke `34822412401` 为 1/1。匿名 workflow bytes SHA-256 为
`4c0ab5d4c87558dbb4308b9d47bdce26825019469170a12e2bf533f8008ee183`。该修正不改变任何 product timeout、
gate、资产坐标、摘要或 acceptance threshold。

## 6. 实现与候选的远端门

rebase 后 PR #140 的有效原始 [Public CI run 34824079525](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34824079525)
为 attempt 1、11/11 SUCCESS。实现以普通 merge commit 合入受保护主线；`main@86b62464...` 的 Public CI
`34825496310` 为 attempt 1、11/11 SUCCESS，Browser Smoke `34825496263` 为 attempt 1、1/1 SUCCESS。

实现冻结候选 [PR #142](https://github.com/NoctilumeDev/VeriTrail/pull/142) 的精确链为：

```text
base = 86b62464b9eef00a5e9da8d0549f093767be27e2
head = 192a2f5e572c8305084acbe22e5ee1973ef816d9
merge = a4c63607d8a586a5ec19eae1cdc4279cda1ffa88
parents = 86b62464b9eef00a5e9da8d0549f093767be27e2
          192a2f5e572c8305084acbe22e5ee1973ef816d9
tree = 862f3c4d05682fe2389537d5c1cb4d93093abe6b
```

PR #142 原始 [Public CI run 34828490782](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34828490782)
为 attempt 1、11/11 SUCCESS；Python 3.13 / 3.10 aggregated jobs 分别耗时 13m58s / 14m56s，说明 outer
containment headroom 确有必要，但不改变产品语义。候选 exact main 的新门为：

```text
Public CI      run 34830066250  attempt 1  11/11 SUCCESS
Browser Smoke run 34830066475  attempt 1   1/1 SUCCESS
```

## 7. 候选 fresh anonymous installed-product readback

读回在 fresh venv 中安装并从 `site-packages` 导入 Core 0.13.0、GitHub Evidence 0.1.0、Playwright 1.62.0 与
matching Chromium。公开 Release wheel 复算 SHA-256 为：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

清空 `GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 后，针对 exact `a4c63607...` 建立三次互不复用的
`P1 API -> P2 Render -> P3 handoff -> Core` session：

| Target | Viewport | Marker / count | HTTP | P1/P2 coverage | Stable | Core |
| --- | --- | --- | ---: | --- | --- | --- |
| `README.md` | `DESKTOP_1365X768` | `R1_FACT_EVIDENCE_CLOSURE_FREEZE_CANDIDATE` / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/157-r1-fact-evidence-closure-implementation-freeze-candidate.md` | `DESKTOP_1365X768` | same / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/milestones.md` | `DESKTOP_1365X768` | same / 1 | 200 | COMPLETE / COMPLETE | true | PASS |

三次 requested/final URL 均相同，redirect chain 只有最终 HTTP 200；三样本稳定，active stream、coverage reason、
conflict 与 cleanup error 均为 0。读回使用专属 acceptance identity
`r1-fact-evidence-implementation-candidate-public-readback`，summary kind 固定为
`R1_FACT_EVIDENCE_IMPLEMENTATION_CANDIDATE_PUBLIC_READBACK`，boundary 固定为
`ANONYMOUS_PUBLIC_EXACT_SHA_INSTALLED_PRODUCT`。

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-b6e33e88a6eb4c2c9274fdd999476b0d` | `7f31d0a860b2...` | `a8e7597f1dd9...` | `e09f8fb1e642...` | `498e9c66d5ab...` | `4b1aba4ae43a...` |
| Document 157 | `github-paired-9f7d9d71273d474595f492bcb8c220eb` | `30052e99f863...` | `212eac87c8c...` | `d6f468c42300...` | `c677c88a2018...` | `f85debf22eb2...` |
| Milestones | `github-paired-d4d9dae6efcc408486e6a6f5b3078f47` | `7369a4505d0a...` | `5b2ede528f89...` | `2ea2916a61c4...` | `cd07bd1fe5de...` | `8d8d405b3615...` |

三份规范 summary 的联合 SHA-256 为：

```text
b967c60409f495245b91727f447c28581adf58adefe98b38d1c92795c62e1ee2
```

最初三次运行复用了 P4 release-candidate probe，其技术路径虽通过，却把 summary 标成
`P4_REAL_GITHUB_RELEASE_CANDIDATE`。该标签不能证明 R1 candidate 的 acceptance intent；三份结果已明确作废，
没有进入上表或联合摘要。运行机制正确不等于证据身份可以借用。随后以新 sealed Plan、R1 专属 acceptance ID、
kind 与 boundary 重新建立上表三份 v2 证据。

## 8. 明确未冻结与下一停止线

本次没有冻结、实现或授权：

- output coordinate、Artifact writer、public publisher 或任何 R1 文件落盘；
- real parser、public Provider SPI、ambient discovery、encoding/anchor 与 partial AST；
- multi-Provider Fact closure、RelationSet、conflict/UNKNOWN 传播；
- ReviewSliceSet、CoverageLedger、COMPLETE/DIAGNOSTIC Manifest；
- CLI、Workbench 写入、Core 新判断、Q implementation、D product shell 或 JPyxis adapter；
- hostile-code sandbox、Linux/macOS cell、Server/Cloud、并发、分布式或多租户能力。

本文自己的最后门全部成立后，唯一合法下一步是从新的 exact main 再做一次系统级俯瞰，比较尚未冻结的接缝，
然后只选择下一个最小合同闭环。本文不预先决定 publisher、parser、multi-Provider Fact、Relation 或其他候选谁先
施工。发现风险不等于必须当场修改；Relation、Slice、Coverage 与完整 Derivation 不能直接开始实现。

## 9. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过
focused 27 项四格回归、Markdown 相对链接、fence/heading、状态 marker、敏感模式、scope 与
`git diff --check`。这些本地结果不替代本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_FACT_EVIDENCE_CLOSURE_FROZEN 成为当前主线事实
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用文档 157、PR #142、候选 exact-main 门或候选
读回替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
