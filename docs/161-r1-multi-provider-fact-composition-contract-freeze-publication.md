# R1 Multi-Provider Applicability / Fact Composition 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_FROZEN /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_ALLOWED /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 上游系统审计：[Fact/Evidence 冻结后下一闭环系统审计](159-r1-post-fact-evidence-next-closure-system-audit.md)
>
> 冻结对象：[Multi-Provider Applicability / Fact Composition 最小合同 0.1](160-r1-multi-provider-applicability-and-fact-composition-contract.md)
>
> 候选合入基线：`main@9c336e02318791b411c9abfa8cf662fb97f61f47`
>
> 候选合入 Tree：`0048298cda0174997287d7cb7416cd989164e67c`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只外部绑定文档 160 的合同候选、有效本地回归、原始远端门、受保护主线合入、新 exact-main
门禁与 fresh anonymous installed-product readback，并发布一条窄实现入口。本文不创建或修改源码、测试、
Schema、corpus、identity vector、依赖、CI、Provider、parser、FactSet/DerivationEvidence publisher、
Relation、Slice、Coverage、Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，
以及针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为
当前主线事实；在此以前，本分支文字不授权任何实现。

## 2. 本次冻结的最小对象

本次只冻结一个 private、closed-test 的 multi-Provider applicability / Fact composition 合同：

```text
sealed capability requirements
  -> application-owned closed conformance table
  -> exact ordered Provider descriptors / bindings
  -> one parent composition attempt + one shared BudgetContext
  -> serial existing single-Provider child execution cells
  -> run-local terminal conformance
  -> same-ID semantic merge / provenance union
  -> same-subject FactConflict construction
  -> required/optional terminal join
  -> immutable private composition result
```

合同不建立 public Provider registry、ambient discovery、real parser、公共 Artifact 或调度系统。composition
controller 只串行编排既有单 Provider cell；它不发明 multi-Provider wire envelope，也不取得 Q 的并行、复用或
Gate 选择权。

## 3. 已冻结不变量

### 3.1 requirement、applicability、descriptor、binding 与 run 不是同一身份

capability requirement 只声明所需能力与 requiredness；application-owned fixed table 决定该 requirement 在当前
closed profile 下是否唯一映射到一个精确 descriptor/binding tuple。Provider identity、一次 ProviderRun 与一次
composition attempt 分别拥有自己的坐标。caller 不能补选 Provider、改变 requiredness 或扫描 ambient
installation。

### 3.2 一个父 attempt、一个共享预算、多个串行 child cell

所有 child cell 共享父 attempt 已创建的同一 `BudgetContext`、absolute deadline、artifact accounting 与 single
stop latch；后继 Provider 不能刷新预算。现有 `veritrail-review-derivation-cell/0.1` 仍是单 descriptor、单 terminal
frame 协议，每个 child cell 各自完成 preparation、execution、terminal mapping 与 residue-free release。

```text
same parent BudgetContext
  != one multi-Provider transport process
  != one refreshed budget per child
```

### 3.3 parent eligibility 与 run-local eligibility 分开

run-local nonconformance 只否定该 run 的 canonical candidate 资格。若 exact run identity 已成立、child release
闭合且 parent shared context 仍可用，controller 可以继续观察后续 Provider，以保留 required/optional terminal
事实。shared deadline/cancel/memory stop、identity 不可建立、release failure 或 parent composition integrity
failure 会不可逆撤销父 attempt 的 normal eligibility，并阻止后继启动。

### 3.4 child transport 不拥有 Fact 权

完整 terminal frame 只形成一个 execution-cell phase value。candidate validation、application canonicalization、
Fact admission 与跨来源 composition 仍是后继 controller 的独立步骤：

```text
transport accepted
  != Provider run conformance accepted
  != canonical Fact admitted
  != composed FactSet publishable
```

partial、duplicate、trailing frame 与 invalid canonical JSON 都只能形成 run-local failure 或更高层 stop；不能让
transport bytes 直接成为 Fact。

### 3.5 same-ID merge、same-subject conflict 与 identity collision 分开

只有 Fact ID 和 provenance-free semantic object 同时相同，才合并为一个 Fact，并对 provenance 与 reported
run references 做排序并集。same ID 配不同 semantic object 是 identity integrity failure，不是 `FactConflict`；
同一 subject 的不同 Fact IDs 表达互不相容语义时，保留各 candidate，并建立确定性、排序、可追溯的
`FactConflict`。optional 来源产生的冲突不能因其 optional 身份被删除。

### 3.6 terminal join 不获得根因解释权

required/optional 只影响 composition-level status join，不改变来源事实：

- required run 的 `FAILED` 使 overall 不能 `COMPLETED`；
- required run 的 `UNAVAILABLE` 在没有更强已观察状态时保留不可用；
- optional run 的 non-success 可以与 required completed sources 共存，但 run 与 diagnostic 必须保留；
- non-completed overall 的 final reported Fact/conflict IDs 必须机械清空；
- 多个失败同时存在时不臆造单一根因或时间优先级。

### 3.7 first slice 仍然 non-published

本合同不预留 output coordinate，不创建 writer/publisher/Manifest role，也不允许 first private slice 生成
`EXECUTION_ARTIFACT_BUDGET`。Fact composition 只有在全部已启动 child cell terminal 且安全释放以后才能 join；
任何非 completed overall 都原子撤销 parent normal continuation。Schema/corpus/vector bytes 保持不变，因为现有
shape 已能表达多 run、provenance union、FactConflict 与 optional non-success，而本切片仍不发布 Artifact。

## 4. 冻结后唯一实现授权

本文自己的最后门全部成立后，只允许从新的 exact main 严格按以下顺序实现：

```text
A. private closed applicability table and exact binding-set admission
B. one shared-budget composition controller + serial single-Provider child cells
C. run-local candidate validation and terminal join
D. same-ID merge / same-subject FactConflict construction
E. bidirectional provenance and final Evidence projection
F. immutable private composition result
G. MP-001..028 hardening
```

每一步都是停止线。若实现证明 fixed private applicability、shared-budget serial child-cell orchestration 或既有
Schema 无法同时满足，必须回到本合同；不能通过新 wire envelope、first-success shortcut、caller-selected Provider、
optional-source suppression 或 identity 放宽继续施工。

## 5. 候选与 exact-main 远端门

[PR #145](https://github.com/NoctilumeDev/VeriTrail/pull/145) 的精确链为：

```text
base    = 22df05698f05380e910ac8a4e0cc6ba1276842e7
head    = 3bda18fa591d94a91ad472d7dcff467b63ce508f
merge   = 9c336e02318791b411c9abfa8cf662fb97f61f47
parents = 22df05698f05380e910ac8a4e0cc6ba1276842e7
          3bda18fa591d94a91ad472d7dcff467b63ce508f
tree    = 0048298cda0174997287d7cb7416cd989164e67c
```

PR #145 原始 [Public CI run 34862613854](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34862613854)
为 `pull_request / attempt 1 / 11/11 SUCCESS`。候选以普通 merge commit 合入受保护主线；exact
`main@9c336e0...` 的新门为：

```text
Public CI      run 34864526961  push / attempt 1  11/11 SUCCESS
Browser Smoke run 34864526953  push / attempt 1   1/1 SUCCESS
```

## 6. 候选 fresh anonymous installed-product readback

读回在 fresh CPython 3.13 venv 中匿名下载固定 Release wheel，复算 SHA-256 后安装，并从该 venv 的
`site-packages` 导入：

```text
Core 0.13.0 wheel
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0 wheel
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf

Playwright 1.62.0 + matching Chromium
```

清空 `GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 后，针对 exact `9c336e0...` 建立三次互不复用的
`P1 API -> P2 Render -> P3 handoff -> Core` session。三者都使用专属 acceptance identity，summary kind 固定为
`R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE_READBACK`，boundary 固定为
`ANONYMOUS_PUBLIC_EXACT_SHA_INSTALLED_PRODUCT`。

| Target | Marker / count | HTTP | P1/P2 coverage | Stable | Core |
| --- | --- | ---: | --- | --- | --- |
| `README.md` | `R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE` / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/160-r1-multi-provider-applicability-and-fact-composition-contract.md` | same / 2 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/milestones.md` | same / 1 | 200 | COMPLETE / COMPLETE | true | PASS |

三次 requested/final URL 相同，三样本稳定；active stream、coverage reason、conflict 与 cleanup error 均为 0。
三个 collection session 与三个 sealed Plan 均不复用：

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-f8ddfd85583843089e43dbbcc86d5f4c` | `9909a07a41639cabb43fc55a972cb88427b05bb72b4a309e9d13dbda8db2e88a` | `a6a5cfd658eec62573e2f56088356ad576662d91e22e169269bfa3839e7f9919` | `90afc570e288c61f1c014ebeb0b622abf604d43633c681f1e6e5f0fb517fa636` | `ad948ff6958227c09b84df10bd0adee6a87438f3f50f2cd44ec9c81e69c059ed` | `53a9964d98bfdaf9d8370aa939af71214dde2bd69d8509e9eba8d61198a5b535` |
| Document 160 | `github-paired-c301d457106f4596b53e2605a895ca52` | `2eed9f3328bdc5a75c22a521f601bdc6421d44f3dc965c5f5c2e54224ac0f49b` | `c940b745dbebe6db38f421343656d01868630a87e72653a8d81ea65e8a1a11bb` | `b16c2a6df3ec815ed71cbde61d4a1a0600adc9ffd01147400400013d5650b192` | `c595502ac8057424d394334a33bd7fa5c20a34e86fcbedca652e551590903a4f` | `fe8065dd96523e3c60d3463fb51de6918ab865fd9788214de06868c6bf3ed3fe` |
| Milestones | `github-paired-9e5397b1b85847689b13aedfc2714154` | `ac7f63384d3eaa627c3e8456f124e30ee6791a469dfdaf95753b9f32ca4f62ac` | `6c33a82f79ad16e3be7ace06cb00c9977ccbb766b08c00a0e8adc3ca84f4ecfa` | `431e473e4426eb4941388c72327d2513c5a6201aed7e8b5f53034e821c717909` | `3ba7a8c235949d7fa047d7f22252b8211b3fcd38887df1c46339f3a3c41daa9a` | `6f4d4ace4f8991584bb86c1ff3f9bb04d7e9a42d991be58080fddbc91ae2e867` |

三份 canonical summary bytes 按 README、文档 160、milestones 固定顺序连接后的联合 SHA-256 为：

```text
82a160f94a5e8f5bc8adfaf836e886c6b70f3c7f28cf31e2131b1813a4ff0905
```

## 7. 保留的本地证据污染与有效回归

候选的第一轮本地完整回归复用了旧 venv，其 `pywin32` distribution metadata 不完整，产生 57 个环境失败；
首次 fresh CPython 3.10 venv 又遗漏 `jsonschema` test extra，在 108 项通过后 import 失败。两次均被判为
test-environment coordinate 不完整，不计入通过证据，也不解释成产品失败或由后续绿灯抹除。

之后使用两个 exact interpreter 新建专用 venv，显式安装 `pywin32==312` 与 `jsonschema==4.25.1`，并把
`PYTHONPATH` 同时钉住候选 worktree 的 Core src、Review Attention src、plugin tests 与 Core tests。有效完整
回归为：

```text
CPython 3.10 normal  133/133  286.497s
CPython 3.10 -O      133/133  284.220s
CPython 3.13 normal  133/133  278.568s
CPython 3.13 -O      133/133  280.299s
total                532/532
```

这些本地结果只证明 docs-only candidate 没有暗改冻结 runtime/Schema bytes，不替代远端或公开读回。

本状态发布又从 exact candidate main 新建两套独立 venv，使用同样的 locked test capabilities 与当前
worktree source/test roots，串行重跑 19 项 Fact/Evidence closure 与 8 项 public-boundary gate：

```text
CPython 3.10 normal  27/27  13.061s
CPython 3.10 -O      27/27  13.457s
CPython 3.13 normal  27/27  13.161s
CPython 3.13 -O      27/27  12.986s
total                108/108
```

这四格只确认冻结发布没有改变 private runtime 或 public boundary，不替代本文自己的远端门。

## 8. 明确未授权与下一停止线

即使本文自己的最后门全部成立，本次仍不授权：

- real parser、public Provider authorization/SPI/registry/discovery 或 ambient installation scan；
- output coordinate、Artifact writer、FactSet/DerivationEvidence publisher 或任何 R1 文件落盘；
- RelationSet、Relation Graph、conflict/UNKNOWN 的后继传播与解释；
- ReviewSliceSet、CoverageLedger、COMPLETE/DIAGNOSTIC Manifest；
- CLI、Workbench 写入、Core 新判断、Q implementation、D product shell 或 JPyxis adapter；
- Linux/macOS cell、hostile-code sandbox、并行/分布式、多租户或 Server/Cloud。

唯一合法下一步是在本文冻结以后，从新的 exact main 实现第 4 节 A–G；实现完成后必须先做系统级审计与
独立冻结候选，不能直接进入 real parser、Relation、Slice、Coverage 或完整 Derivation。发现新裂缝不自动要求
修改合同；只有反例真正击穿已冻结不变量时，才重开最小受影响边界。

## 9. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须
通过适用 Review Attention focused regression、Markdown 相对链接、fence/heading、状态 marker、敏感模式、
exact scope 与 `git diff --check`。这些本地结果不替代本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
  -> exact head 合入受保护 main
  -> 新 exact main 的 Public CI / Browser Smoke 成立
  -> fresh anonymous installed-product readback of README / 本文 / milestones
  -> R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_FROZEN 成为当前主线事实
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用文档 160、PR #145、候选 exact-main 门或候选
读回替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
