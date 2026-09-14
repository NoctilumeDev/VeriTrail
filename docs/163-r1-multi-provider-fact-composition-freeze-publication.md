# R1 Multi-Provider Applicability / Fact Composition 实现冻结发布

## 1. 文档身份

> 状态目标：`R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[Multi-Provider Applicability / Fact Composition 最小合同 0.1](160-r1-multi-provider-applicability-and-fact-composition-contract.md)
>
> 合同冻结：[Multi-Provider Applicability / Fact Composition 合同冻结发布](161-r1-multi-provider-fact-composition-contract-freeze-publication.md)
>
> 实现候选：[Multi-Provider Applicability / Fact Composition 实现冻结候选](162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@66b2252c5261387e1d1b40899f3e009e6ed6cecf`
>
> 候选合入 Tree：`7583f0007843253bff334a5ff43f5585157cb04e`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 160/161 冻结的 private multi-Provider applicability / Fact composition 已按文档 162 完成
实现、实现后审计、候选门禁、受保护主线合入、新 exact-main 双门与 fresh anonymous installed-product
readback 的事实。本文不创建或修改源码、测试、Schema、corpus、identity vector、依赖、CI、Provider/parser、
publisher、Relation、Slice、Coverage、Manifest、CLI、Workbench、Core、P/Q/D、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及
针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为当前
主线事实；在此以前，本分支文字不授权任何后继实现。

## 2. 本次冻结的最小对象

本次冻结只覆盖一个 private、closed-test、non-published implementation closure：

```text
sealed capability requirements
        ↓
application-owned closed applicability table
        ↓
exact canonical Provider bindings
        ↓
one parent composition attempt
  + one BudgetContext / absolute deadline / stop latch
        ↓
strictly serial single-Provider child cells
        ↓
run-local conformance for every produced source
        ↓
same-ID semantic merge / same-subject FactConflict
        ↓
required + optional terminal join
        ↓
private non-published FactSet construction state
  + private DerivationEvidence projection
```

该对象没有 public Provider registry、ambient discovery、output coordinate、Artifact writer、publisher 或 Manifest
role。它不会把 requirement、applicability、descriptor、binding 与 ProviderRun 压成一个身份，也不会把
FactConflict、terminal Evidence 或 Schema-valid bytes 提升为 Relation、Coverage 或 publication authority。

## 3. 已冻结不变量

### 3.1 Applicable set 由 sealed requirement 与 application authority 决定

caller 只能提交与 frozen closed table 导出的 exact descriptor/binding tuple 相同的集合；missing、extra、duplicate、
descriptor drift、handle drift 与 multi-only binding 绕过 single-Provider admission 均 fail closed。ambient package、
import discovery 与调用方顺序不能改变 applicable set、requiredness 或 canonical execution order。

### 3.2 一个 composition attempt 只有一个预算世界

parent 与所有 child cells 共享同一 BudgetContext、absolute deadline、request provenance、attempt start observation
与 terminal stop latch。child eligibility 各自独立，但不能创建新预算、刷新 deadline 或在 parent stop 后制造未真实
启动的 ProviderRun。deadline、caller cancellation、positive memory stop、release failure 与 shared-context failure
都会不可逆停止后继执行。

### 3.3 Run-local conformance 先于跨来源组合

每个 ProviderRun 必须先独立闭合 candidate shape、canonical Fact identity、anchor/scope/profile、run-local duplicate、
reported-ID 与 provenance；跨来源 composition 不能借另一个合法来源掩盖 malformed same-source output。

```text
same fact_id + same semantics
  -> one Fact + sorted provenance union

same fact_id + different semantics
  -> integrity failure
  -> not a FactConflict

same subject + different fact_id
  -> deterministic FactConflict
```

Fact 与 ProviderRun 的引用必须双向闭合，不能出现 dangling provenance 或单向 reported-ID。

### 3.4 Terminal join 不推断根因

required terminal status 机械采用：

```text
FAILED > UNAVAILABLE > COMPLETED
```

该顺序只选择 final status，不裁决多个失败中的根因。ordinary run-local failure 在 release 安全且 parent context 仍可
继续时不短路后继来源；optional non-success 保留 diagnostics，但不覆盖 required success。任何 final non-completed
Evidence 都清空 final reported Fact IDs。

### 3.5 Runtime 与 publication authority 继续分离

成功只形成 copy-owned private values；调用方 mutation 不改变 controller-owned state。canonical bytes、digest、
Schema conformance 与 diagnostic eligibility 都不能单独产生 path、Artifact membership、Manifest role 或 writer
authority。预算、attempt number、retry history 与 terminal timing 也不进入 Fact semantic identity。

## 4. 实现、审计与本地证据

实现从冻结合同 exact main 建立：

```text
contract base = f42c722951bc82ae840c80bae264dcfa52d54278
implementation head = f23c042cf11f872da2e6413d4c0ee76210fb43e7
implementation merge = 590df332fbd60bdfc857a4ea3f3c35937ce03d8a
implementation tree = 4814149bc175886bdcc92ffc45fd65376373a4ba
```

实现只修改七个文件，源码 diff 为 1930 insertions、18 deletions。三个新增模块保持私有；顶层 package 没有新增
export，base dependency surface 没有变化，single-Provider 入口保持原语义。

实现后审计逐条映射 `MP-001..028`，没有发现要求重开冻结合同的新 blocker。重点确认：

1. applicability、execution、composition 与 terminal join 没有取得 public discovery/authorization 权；
2. parent 与 children 共用一个 absolute budget，没有跨抽象边界刷新 deadline；
3. malformed frame、deadline、cancellation 与 positive memory-stop 由真实 lower-cell 路径进入 composition；
4. normal、conflict 与 diagnostic private projections 由独立 Draft 2020-12 validator 验证现有公共 Schema；
5. single-Provider API 拒绝 multi-only binding，旧入口没有成为绕过点；
6. private result 无 writer/path/reservation/Manifest surface，边界测试观察到零文件写入。

candidate exact-main worktree 的 focused gate 在 CPython 3.10/3.13 normal/`-O` 四格均为 `29/29`；最终本地完整
Review Attention 回归在 CPython 3.13 normal 为 `162/162`，root Schema 回归为 `27/27`。clean wheel 从 isolated
`site-packages` 导入 private modules，顶层包没有导出 composition。当前本机没有 `ruff`，因此没有虚构本地 lint
证据；远端 Workbench lint/build 与完整 Public CI 仍照常执行。

固定 MP-028 compatibility vector 为：

```text
required FactSet digest
  f466d18769a1630cfbaa4bcff01d71193475324b8d4990ceb8e3d535ce47e813

required fact_id
  bd3fe913ed53476a9362372f88782dbbb4349fa45aa908191f5b83d049db1fc4

advisory FactSet digest
  dada6a2ad992edc5cec3af2c8d480b0bf494c61e2996f4ae46d1c3d2982bbdbc

advisory fact_ids
  3434c02de4fc0fbc83d9593dddd6ec29bfd1bfa7c5b9235aa90ecc5a6d948c8d
  bd3fe913ed53476a9362372f88782dbbb4349fa45aa908191f5b83d049db1fc4

conflict_id
  731af487d12164d26754adb241c35b6073a50d5db463ccd0daf2798e01022013
```

## 5. 实现与候选的远端门

[PR #147](https://github.com/NoctilumeDev/VeriTrail/pull/147) 的原始
[Public CI run 34880944564](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34880944564) 为 attempt 1、
11/11 SUCCESS。实现以普通 merge commit 合入受保护主线；`main@590df332...` 的新门为：

```text
Public CI      run 34882727275  push / attempt 1  11/11 SUCCESS
Browser Smoke run 34882727435  push / attempt 1   1/1 SUCCESS
```

实现 exact main 的全部七个变更文件又完成无 token raw-byte 读回，远端 bytes 与 Git tree 逐项同大小、同
SHA-256 和同 blob identity。按 `path<TAB>bytes<TAB>sha256`、LF join 形成的规范行 SHA-256 为：

```text
8ecdf360ffea918222c565bd9530bf4990e454b6f56d5a0a8f78ae6ac6fcadda
```

实现冻结候选 [PR #148](https://github.com/NoctilumeDev/VeriTrail/pull/148) 的精确链为：

```text
base = 590df332fbd60bdfc857a4ea3f3c35937ce03d8a
head = ba0d30699eab8ac957bedebb9094df724ded36bd
merge = 66b2252c5261387e1d1b40899f3e009e6ed6cecf
parents = 590df332fbd60bdfc857a4ea3f3c35937ce03d8a
          ba0d30699eab8ac957bedebb9094df724ded36bd
tree = 7583f0007843253bff334a5ff43f5585157cb04e
```

PR #148 原始 [Public CI run 34885652717](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34885652717)
为 pull_request / attempt 1 / 11/11 SUCCESS。候选以普通 merge commit 合入受保护主线；candidate exact main 的
新门为：

```text
Public CI      run 34887431677  push / attempt 1  11/11 SUCCESS
Browser Smoke run 34887431658  push / attempt 1   1/1 SUCCESS
```

## 6. 候选 fresh anonymous installed-product readback

读回从 exact `main@66b2252...` 的 detached worktree 取得 orchestration probe，在 fresh CPython 3.13 venv 中
匿名下载并复算固定 Release wheel SHA-256：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

两项下载均在无 token 的第一个 attempt 成功；随后安装 Playwright 1.62.0 与 matching Chromium。Core 与 GitHub
Evidence 的 import path 都位于该 fresh venv 的 `site-packages`。清空 `GH_TOKEN`、`GITHUB_TOKEN` 与
`PYTHONPATH` 后，针对 exact `66b2252...` 建立三次互不复用的
`P1 API -> P2 Render -> P3 handoff -> Core` session：

| Target | Viewport | Marker / count | HTTP | P1/P2 coverage | Stable | Core |
| --- | --- | --- | ---: | --- | --- | --- |
| `README.md` | `DESKTOP_1365X768` | `R1_MULTI_PROVIDER_FACT_COMPOSITION_FREEZE_CANDIDATE` / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md` | `DESKTOP_1365X768` | same / 1 | 200 | COMPLETE / COMPLETE | true | PASS |
| `docs/milestones.md` | `DESKTOP_1365X768` | same / 1 | 200 | COMPLETE / COMPLETE | true | PASS |

三次 requested/final URL 均相同，三样本稳定；active stream、coverage reason、conflict 与 cleanup error 均为 0。
读回使用专属 acceptance ID `r1-multi-provider-implementation-candidate-readback`，summary kind 固定为
`R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_CANDIDATE_READBACK`，boundary 固定为
`ANONYMOUS_PUBLIC_EXACT_SHA_INSTALLED_PRODUCT`。

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-6fe9a4deffbc4dcca9d0f6e9103dcb79` | `e75e3e83bb49db6c42cd319084603a2b81547270fdf375a4933af4784762fc6c` | `b51e2b92fc0eacc87f80f6c99b183fc74b55e4c165cc9295a61db2833b969805` | `ca6b6190134159683efc96583e9e50e61d59592254a308403e30f5743e311fcd` | `d3045318aa1f06040d9313abc8d79fe72900b118256374138369597deaf30e69` | `640f5caf9d78b1fcd2d9af47b3941cd7482411019a0a5b697f83f06353781381` |
| Document 162 | `github-paired-9dc5d0dbc37b4636a5e7269141caf724` | `6dc14f97906e4d712bfc774d40785f33e7fc7d834a0c91babc491dc16abc2ba7` | `a72bc2c06c6a276787a140a20044c24bc3f09359b92b57d3dc192045c4645ea4` | `2b800504025d71f7197d938c3a3fba92c3b122dda16ec876d59bfc1f838fdf66` | `f4fcc91366ab36d5473ea7f0f299d2455e238a4bc0dff14752f0c381269ab91d` | `a08ae7c52c64d719889f053392403d8783016ac75b5be811f27ef048af17f3b9` |
| Milestones | `github-paired-a7eba926fe9f45d8a993058378297733` | `5c7f7a93bfb327b257df0f8f73f07de49607a33343ff840b7bc2441e94b9c34e` | `7ef1c9a9b1014749dbaedb59c643dd6ae0200983a5963ce632bc4cf750bcbde7` | `afbb33a51137ebd472176e000bcf540a2d8293aca84baff759a950e915327a04` | `cb71f04b8dc77b11cd95164031a283ba59b3d76a90e610b237bc9adda91fe7a7` | `dee71cb6fa7a20f93db10705072df2249fb0ffaee8d07af5e96ce8939d53f85c` |

三份 canonical summary bytes 按 README、文档 162、milestones 固定顺序连接后的联合 SHA-256 为：

```text
c098ffeefea338b9ab220bca0e2c521ec5d0faaae9970699367c20deab8fa7da
```

第一次 README readback 使用了 68 字符的 `plan_id`，超过 Core 的 64 字符上限，因而在 browser collection 与
output directory 创建前被 public validator 拒绝。该失败没有解释成产品或网络故障，也没有复用状态；工具身份缩短
为 51 字符并单独通过 Core seal 后，才从新输出目录建立上表 README attempt 2。后续 Document 162 与 milestones
也各自使用新 session 与 sealed Plan。

## 7. 明确未冻结与下一停止线

本次没有冻结、实现或授权：

- output coordinate、Artifact writer、public publisher 或任何 R1 文件落盘；
- real parser、public Provider authorization/SPI/discovery、encoding/anchor 与 partial AST；
- RelationSet、derived relation authority、conflict/UNKNOWN 向 Relation 的传播；
- ReviewSliceSet、CoverageLedger、COMPLETE/DIAGNOSTIC Manifest；
- CLI、Workbench 写入、Core 新判断、Q implementation、D product shell 或 JPyxis adapter；
- hostile-code sandbox、Linux/macOS cell、Server/Cloud、并发、分布式或多租户能力。

本文自己的最后门全部成立后，唯一合法下一步是从新的 exact main 再做一次系统级俯瞰，比较延期接缝，然后只
选择下一个最小合同闭环。本文不预先决定 publisher、real parser、Relation/conflict/UNKNOWN、Slice、Coverage
或其他候选谁先施工。发现风险不等于必须当场修改，也不得一次并行启动多条后继链。

## 8. 本状态发布自己的最后门

本 docs-only 状态发布只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过
focused 29 项四格回归、Markdown relative links、fence/heading、状态 marker、敏感模式、scope 与
`git diff --check`。这些本地结果不替代本发布自己的远端 required checks。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN 成为当前主线事实
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用文档 162、PR #148、candidate exact-main 门或
candidate readback 替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
