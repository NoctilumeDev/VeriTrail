# R1 Multi-Provider Applicability / Fact Composition 实现冻结候选

> 候选记录状态：`R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTED /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_FREEZE_CANDIDATE /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`f42c722951bc82ae840c80bae264dcfa52d54278`
>
> 实现提交：`f23c042cf11f872da2e6413d4c0ee76210fb43e7`
>
> 受保护主线实现基线：`590df332fbd60bdfc857a4ea3f3c35937ce03d8a`
>
> 主线 Tree：`4814149bc175886bdcc92ffc45fd65376373a4ba`
>
> 实现影响：`L1_COMPONENT_INTERNAL`；验证影响：`L3_SYSTEM`

## 1. 当前裁决

[文档 160](160-r1-multi-provider-applicability-and-fact-composition-contract.md)与
[文档 161](161-r1-multi-provider-fact-composition-contract-freeze-publication.md)授权的 private
multi-Provider applicability / Fact composition 已实现并合入受保护主线。实现只证明以下命题：

> application-owned closed applicability table 可以把 sealed requirements 映射为 exact Provider bindings；一个
> parent composition attempt 可以在同一 BudgetContext 与 stop latch 下严格串行运行 child cells，先闭合各自
> run-local conformance，再机械执行 same-ID semantic merge、same-subject conflict、required/optional terminal
> join，以及 non-published FactSet / DerivationEvidence projection。

该实现没有创建真实 parser、公共 Provider authorization/SPI/discovery、output coordinate、Artifact writer、
publisher、Relation、Slice、Coverage、Manifest、CLI 或 Workbench，也没有修改 Core、P、Q 或 D。本文只是
docs-only implementation freeze candidate；它自己的门禁、受保护主线合入、新 exact-main 双门、匿名产品读回
与后继独立最终状态发布尚未发生，因此当前不得写成
`R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN`。

## 2. 实现边界

实现只修改七个文件：

```text
plugins/review-attention/src/veritrail_review/
  _execution_cell.py
  _execution_cell_application.py
  _execution_cell_binding.py
  _multi_provider_applicability.py
  _multi_provider_fact_composition.py
  _multi_provider_values.py

plugins/review-attention/tests/
  test_multi_provider_fact_composition.py
```

源码 diff 为 1930 insertions、18 deletions。三个新增模块保持私有；`veritrail_review.__init__` 没有新增
export，base package 没有新增默认依赖。现有 single-Provider execution-cell 入口仍保持原签名与语义；只新增
private prepared-child 能力，并拒绝 multi-only binding 绕过 exact binding-set admission。

private composition 入口没有 output directory、path、writer、publisher、Manifest 或 caller-provided Provider
registry。closed Provider descriptor/binding 仍由 application-owned 固定表决定；ambient installation、import
discovery 与调用方顺序均不能改变 applicable set 或执行顺序。

## 3. 共享 attempt、预算与停止语义

parent composition attempt 一次拥有：

```text
DerivationInputSet
derivation_id
exact applicable binding tuple
one BudgetContext
one parent attempt eligibility
one absolute deadline
one cancellation / memory stop latch
```

每个 child cell 拥有独立 child eligibility 与 ProviderRun identity，但共享同一个 parent BudgetContext、deadline、
request provenance 与 attempt start observation。Provider 严格串行执行；不得为后继 child 创建新预算、刷新
deadline、续接 hidden checkpoint，或在 parent stop 后制造一个“未执行但已失败”的 ProviderRun。

普通 run-local failure 在 release 安全且 parent context 仍可继续时不短路后继来源；deadline、caller cancellation、
positive memory-stop、release failure 或 shared-context failure 会不可逆停止 composition。后到的成功 frame 不能
恢复已失效 attempt，stop 路径也不取得 diagnostic publication authority。

## 4. Fact composition 与 terminal join

每个来源必须先独立闭合：candidate shape、canonical identity、anchor/scope/profile、run-local duplicate、
reported-ID 与 provenance。跨来源 composition 只消费这些已闭合的 immutable run-local values：

```text
same fact_id + same semantics
  -> one canonical Fact + sorted provenance union

same fact_id + different semantics
  -> integrity failure / INTERNAL_DERIVATION_ERROR
  -> not a FactConflict

same subject + different fact_id
  -> deterministic FactConflict
```

Fact 与 ProviderRun 的 provenance closure 双向验证：每个 admitted Fact 的 provenance 必须指向同一 bundle 内真实
ProviderRun，每个 run 的 reported Fact IDs 也必须精确反向闭合。required terminal join 固定为：

```text
required FAILED
  > required UNAVAILABLE
  > COMPLETED
```

该优先级只选择 final status，不声称多个失败中的根因。optional non-success 会保留在 Evidence diagnostics 中，
但不覆盖已经闭合的 required success；任何 final non-completed Evidence 都清空所有 final reported Fact IDs。

成功只返回 copy-owned、private、non-published FactSet construction state 与 Evidence projection。调用方修改副本
不会改变 controller-owned value；canonical bytes、digest 或 Schema-valid shape 均不获得路径、Artifact role、
Manifest membership 或发布权。

## 5. `MP-001..028` 合同映射

| 合同族 | 已实现的证明义务 |
| --- | --- |
| MP-001..007 | fixed applicability、exact bindings、requiredness 继承、ambient exclusion 与 canonical order |
| MP-008..010 | one shared BudgetContext/deadline、预算不污染语义 identity、合法 empty source continuation |
| MP-011..016 | same-ID merge、integrity collision、same-subject conflict、单来源冲突 fail closed |
| MP-017..021 | required/optional terminal join、diagnostic 保留与 final reported-ID 清空 |
| MP-022..023 | bidirectional provenance closure 与 caller order independence |
| MP-024..025 | parent stop、无 fabricated run、safe run-local failure continuation 与真实 malformed-frame 路径 |
| MP-026..027 | copy ownership、private boundary、零文件写入与无 publication surface |
| MP-028 | 双 Python normal/`-O` 下固定 FactSet、Fact 与 FactConflict compatibility vector |

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

## 6. 实现后系统审计

本轮没有按 finding 数量凑审计 KPI。审计逐条比较冻结合同、implementation diff、测试、现有公共 Schema、
package boundary、single-Provider compatibility 与真实 exact-main 门；没有发现要求重开文档 160/161 的 blocker。

已确认：

1. applicability、execution、composition 与 terminal join 没有取得 public Provider discovery/authorization 权；
2. parent 与 children 共享一个 absolute budget，未在抽象边界刷新 deadline；
3. malformed frame、deadline、cancellation 与 positive memory-stop 由真实 lower-cell 路径进入 composition；
4. normal、conflict 与 diagnostic private projections 均由独立 Draft 2020-12 validator 验证现有公共 Schema；
5. single-Provider API 不能接收 multi-only binding，旧调用面没有被暗中扩大；
6. private result 无 writer/path/reservation/Manifest surface，运行测试观察到零文件写入。

本轮仍不改以下延期风险：

- real parser、encoding/anchor、partial AST、unsupported language 与 public Provider lifecycle；
- output coordinate、DIAGNOSTIC/COMPLETE publisher、artifact budget 与完整八文件 Manifest；
- RelationSet、conflict/UNKNOWN 向 Relation 的传播与 derived-relation authority；
- ReviewSliceSet、CoverageLedger 及其 denominator / PARTIAL 语义；
- hostile Provider sandbox、cross-platform execution cell、Q scheduling/cache、D product shell、JPyxis adapter 与
  AI Execution OS。

这些对象仍可能在下一轮系统审计中反向约束当前假设；没有证据要求本候选提前扩张。

## 7. 本地、Schema 与打包证据

candidate exact-main worktree 的 focused multi-Provider gate 在四格均为 `29/29`：

| 门 | CPython 3.10 | CPython 3.10 `-O` | CPython 3.13 | CPython 3.13 `-O` |
| --- | ---: | ---: | ---: | ---: |
| Multi-Provider Fact composition | `29/29` | `29/29` | `29/29` | `29/29` |

最终完整 Review Attention 回归在 CPython 3.13 normal 为 `162/162`；root Schema 回归为 `27/27`。两套
interpreter 均对全部变更源码与测试完成 `py_compile`。实现中途曾在补充直接 stop/controller、真实 malformed
frame 与独立 Schema validation 前得到较小测试集的通过结果；这些结果没有替代最终 focused matrix。

clean wheel 从 isolated `site-packages` 导入新增 private modules 并执行 probe；顶层 package 没有导出 private
composition，也未加载额外 runtime capability。当前环境没有安装 `ruff`，因此没有把不存在的本地 lint 运行
记录成证据；远端 Workbench lint/build 与仓库公开门仍照常执行。

## 8. 远端实现因果链

实现从冻结合同 exact main 建立：

```text
base = f42c722951bc82ae840c80bae264dcfa52d54278
head = f23c042cf11f872da2e6413d4c0ee76210fb43e7
merge = 590df332fbd60bdfc857a4ea3f3c35937ce03d8a
parents = f42c722951bc82ae840c80bae264dcfa52d54278
          f23c042cf11f872da2e6413d4c0ee76210fb43e7
tree = 4814149bc175886bdcc92ffc45fd65376373a4ba
```

[PR #147](https://github.com/NoctilumeDev/VeriTrail/pull/147) 的原始
[Public CI run 34880944564](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34880944564) 为 attempt 1、
11/11 SUCCESS。PR 以普通 merge commit 合入受保护 `main`；candidate head 与 merge commit 的 tree 相同。

新 exact main 的 [Public CI run 34882727275](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34882727275)
为 attempt 1、11/11 SUCCESS；
[Browser Smoke run 34882727435](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34882727435) 为 attempt 1、
1/1 SUCCESS。没有 repair PR、rebase、rerun 或后继成功覆盖先前失败的因果分支。

## 9. 匿名 exact-SHA 源码读回

在无 GitHub token 的 fresh HTTP client 中，从 `raw.githubusercontent.com` 对 exact
`590df332fbd60bdfc857a4ea3f3c35937ce03d8a` 读取全部七个变更文件。远端 bytes 与本地 exact merge tree 逐项
同大小、同 SHA-256；远端 bytes 重新计算的 Git blob identity 也逐项匹配 merge tree：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `_execution_cell.py` | 19851 | `bd2037368946f2f10ccb462819f7b9c3f4b62fd7a05ad341d772fa7d593008fa` |
| `_execution_cell_application.py` | 27082 | `62933f560f2df275bdde5097ba7bc8a292962a7125c6a4f2988fdcda34176559` |
| `_execution_cell_binding.py` | 3996 | `411f41ab94f397f0b5cfe930bccd6165620f69af8681c481f206bac28ca21dc9` |
| `_multi_provider_applicability.py` | 4796 | `4ecdf11339c680e06fe74d83b9145ac73c90c6e8391c336d48bf5bdc7ce04310` |
| `_multi_provider_fact_composition.py` | 29188 | `48636e52e1e2b5ecef60f517f3273fb58536d1f52a043cbb34bee0fc2b5dcab5` |
| `_multi_provider_values.py` | 4481 | `d736d87d038855c810102544bbbeeeb51cdf0765c82a01d70023e7e6ff87f84d` |
| `test_multi_provider_fact_composition.py` | 31978 | `890ba8ee43179716fdd03b6155865fd4ae664de9bbbe5a0f7951878318ec7f75` |

表中短路径位于 `plugins/review-attention/src/veritrail_review/` 或
`plugins/review-attention/tests/` 对应目录。按 `path<TAB>bytes<TAB>sha256`、LF join 形成的规范行 SHA-256 为：

```text
8ecdf360ffea918222c565bd9530bf4990e454b6f56d5a0a8f78ae6ac6fcadda
```

该读回只证明公开 exact bytes 与 Git tree 身份一致；HTTP 成功本身不证明实现符合合同。

## 10. 本候选自己的最后门

本文与入口索引完成后，当前状态只能是 implementation freeze candidate。本文必须重新完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、敏感模式、生成物与 `git diff --check` 成立；
3. multi-Provider focused 29 项在 CPython 3.10/3.13 normal/`-O` 下成立；
4. 原始 PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN`。

任一门失败，保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、继承 PR #147 或旧合同门
作为本文证据，也不得开始真实 parser、public Provider SPI/discovery、publisher、Relation、Slice、Coverage、
Manifest、CLI 或 Workbench。

## 11. 下一门与 Fresh-Agent 交接

当前 fresh Agent 的唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，
仍须从新的 exact main 创建独立最终冻结发布；只有该发布完成自身门禁、合入与匿名读回以后，才允许再做一次
系统级俯瞰并选择下一个最小合同闭环。

后继选择不得由本文预先承诺。DIAGNOSTIC publisher、real parser/provider boundary、Relation/conflict/UNKNOWN、
Slice、Coverage 与 COMPLETE publisher 都只是待比较候选；不得因 private FactSet/Evidence projection 已闭合就直接
进入其中任何一项，更不得一次并行实现多条后继链。
