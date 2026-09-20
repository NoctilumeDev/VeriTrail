# R1 Relation Derivation 实现冻结候选

> 候选记录状态：`R1_RELATION_DERIVATION_IMPLEMENTED /
> R1_RELATION_DERIVATION_FREEZE_CANDIDATE /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`04cdc6bd3aa33ee77819af9e5764591d3469004c`
>
> 实现提交：`db6148020b3333104a93ec602c7a7c1c5a5e3ab6`
>
> 受保护主线实现基线：`122d0c6b9d3c7a4518f12aec2f503f8979018dda`
>
> 主线 Tree：`5db4e21a7fceda54eab184b0fea498d365da1fee`
>
> 实现影响：`L1_COMPONENT_INTERNAL`；验证影响：`L3_SYSTEM`

## 1. 当前裁决

[文档 165](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)与
[文档 170](170-r1-relation-derivation-contract-freeze-publication.md)授权的 private closed Relation
Derivation proof 已实现并合入受保护主线。实现只证明以下命题：

> 在一个 exact composed FactSet、固定 phase table 与原 live `BudgetContext` 上，application 可以先完成
> Fact-stage private join，经保守 upstream gate 后启动 distinct Relation execution cell；closed deterministic
> Provider 只在 copy-owned exact operands 上产生候选，application 机械复算 identity/provenance，Relation
> terminal 后再计算 final phase join。

该实现没有创建完整 Relation algorithm、真实 import resolution、RelationSet composition/admission、
RelationConflict ledger、conflict/optional-gap 的局部派生、public Provider、publisher、Slice、Coverage、CLI 或
Workbench，也没有修改 Core、P、Q、D 或 Cu。本文只是 docs-only implementation freeze candidate；它自己的
远端门禁、受保护主线合入、新 exact-main 双门、匿名产品读回与后继独立最终状态发布尚未发生，因此当前不得写成
`R1_RELATION_DERIVATION_FROZEN`。

## 2. 实现边界

实现修改十一份文件：

```text
plugins/review-attention/src/veritrail_review/
  _relation_closed_provider.py
  _relation_derivation.py
  _relation_derivation_values.py
  _relation_execution_cell.py
  _relation_execution_cell_application.py
  _relation_execution_cell_binding.py
  _relation_execution_cell_values.py
  _relation_execution_cell_worker.py

plugins/review-attention/tests/
  support.py
  test_boundaries.py
  test_relation_derivation.py
```

源码 diff 为 3099 insertions、2 deletions。八个新增 runtime 模块保持私有；`veritrail_review.__init__` 没有新增
export，base package 没有新增默认依赖。现有 Fact execution cell、multi-Provider Fact composition、公共 Schema
与 Artifact 路径没有改名或原位改写。

private 入口没有 output directory、writer、publisher、Manifest、caller-provided Provider registry 或 ambient
discovery。application-owned fixed table 唯一选择 closed capability/provider/parser/runtime identity；调用方不能用
任意 descriptor、安装顺序或 import path 取得 Relation authority。

## 3. Exact operand、phase 与预算连续性

Relation-only operands 使用新 domain：

```text
veritrail.review.provider-operands/0.2
```

其 payload 是冻结 `/0.1` 投影加 exact `fact_set_digest`。固定 compatibility vector 为：

```text
4218eb9a094ad94287e8ff1628498a26e3189bc4dd3112ec6b4f0b5a57f83406
```

请求不仅携带摘要，还携带去除 provenance 后的完整 canonical FactSet semantic projection 与 source bytes。
application 和 worker 分别复算 Fact identity、FactSet digest、source/snapshot、Policy、scope、Profile 与 operands；
任何摘要、成员、顺序或 source bytes 漂移都在 Provider 候选取得资格前 fail closed。

固定 phase table 只有：

```text
python-ast                 FACT / required
python-ast-advisory        FACT / optional
review-relation-derivation RELATION / required
```

integrated parent 只 admission 一次 budget，Fact children 先 terminal，private Fact-stage join 只消费 Fact runs；
upstream gate 通过后，Relation child 继续使用同一个 live `BudgetContext`、absolute deadline 与 stop latch。Relation
requirement 不参加产生自身输入的 Fact-stage join，final phase join 也不会在 Relation terminal 前冒充完成。

## 4. Distinct Relation cell 与真实 Provider identity

Relation execution 使用独立 wire：

```text
veritrail-review-relation-cell/0.1
```

descriptor 固定为：

```text
capability       review-relation-derivation
provider         closed-relation-provider-a
provider_version 0.1-test
parser           closed-deterministic-test-parser
parser_version   0.1-test
runtime          veritrail-review-test-runtime
runtime_version  0.1-test
```

`_relation_closed_provider.py` 中的 Provider 真实调用 `ast.parse(..., feature_version=(3, 10))`；parser identity
不是为满足既有 shape 虚填。首版 producer 只在已知 fixture 上产生 direct
`MODULE -> IMPORT_DECLARATION / LEXICAL_CONTAINS` candidate，不做 import target resolution，也不生成
`IMPORT_TARGET_LITERAL`。

Relation cell 保持 one request、at-most-one terminal、exact echo、bounded frame、terminal stop 后 cleanup-only 与
residue-free release。每个 candidate provenance 必须恰好指向实际报告它的 Relation ProviderRun；Fact run 不会
回填 Relation IDs，application 也不会补 edge、换 target 或自造 producer。

## 5. 保守 upstream gate 与 final projection

首版 gate 只允许以下输入启动 Relation：

```text
normal exact FactSet
+ every applicable Fact source COMPLETED
+ no FactConflict
+ live shared BudgetContext remains eligible
```

下列情形均保留 typed upstream truth 且不制造 Relation run：

- FactConflict；
- 任一 optional Fact source `FAILED` 或 `UNAVAILABLE`；
- required Fact source non-success；
- whole-attempt stop；
- absent normal FactSet。

`NOT_STARTED / INELIGIBLE` 与已启动 Provider 的 `UNAVAILABLE` 分离；成功空 Relation run 也与未启动分离。
Relation deadline、cancellation 或 positive memory stop 会撤销 prefix candidate，不能刷新预算再跑。若共享预算在
Fact-stage 完成后、Relation 启动前停止，结果保留真实 completed Fact-stage status，不把历史重写为
`INTERRUPTED`。

private result 分开保留 Fact status、Relation start、Relation terminal、final status、typed upstream reasons 与
run-local candidate history。当前不存在 RelationSet admission；final provider-run projection 因而继续清空 reported
Fact/Relation IDs，不能把 private history 提升为可发布 normal world。

## 6. `RD-001..017` 合同映射

| 合同族 | 已实现的证明义务 |
| --- | --- |
| `RD-001..003` | Fact-stage terminal/join、exact FactSet replacement rejection、Fact run 不回填 Relation |
| `RD-004..006` | candidate 必须有真实 Relation provenance、run identity 区分 attempt、sealed requirement 才能启动 |
| `RD-007..009` | FactConflict、optional gap、required non-success 均 fail closed，不裁决 winner 或缩小 normal world |
| `RD-010..012` | empty success / no-start 分离、stop 撤销 prefix、Relation provenance 不能指向 Fact run |
| `RD-013` | `/0.2` canonical vector、dispatch 与双边复算已经物化，不把 string 字段存在当成 identity proof |
| `RD-014` | fixture producer 不实现 zero/one/many import resolution，不把 target 分歧偷写成 RelationConflict |
| `RD-015..017` | final IDs 继续为空、同一 live budget 不刷新、Fact-stage join 排除 Relation requirement |

这些向量证明的是 authority / continuity seam。它们不证明真实仓库的 Relation completeness、semantic accuracy、
RelationSet eligibility 或 Coverage denominator。

## 7. 实现后系统审计

本轮审计不以 finding 数量作为完成指标。冻结合同、implementation diff、测试、既有公共 Schema、package
boundary、Fact composition compatibility 与 exact-main 门逐项比较后，没有发现要求重开文档 165/170 的
blocker。

已确认：

1. Provider 接收经过验证数据的独立 owned copy；恶意 closed fixture 修改其副本不能改写 application-held
   FactSet authority；
2. application 在 canonicalization 时继续使用原始 validated state，不接受 Provider 回传的另一份 Fact world；
3. broad boundary test 继续扫描 `*execution_cell*.py`，没有因 Relation 文件增加而漏掉 Windows execution cell；
4. relation memory-stop 使用真实 lower-cell 路径，不用伪造 terminal；
5. absent normal FactSet、optional gap、FactConflict、deadline、cancel 与 memory stop 分别进入 typed path；
6. private modules 无 public export、文件写入、Artifact role 或默认依赖扩张。

本轮仍延期：

- 真实 import zero/one/many resolution、encoding/anchor、partial AST 与 unsupported language；
- 多 Relation Provider composition、same-ID merge、RelationConflict、UNKNOWN 与 RelationSet admission；
- conflict-bearing FactSet 或 optional-gap 已知前缀的派生资格；
- ReviewSliceSet、CoverageLedger、AttentionProposal 与 omission/denominator 语义；
- COMPLETE/DIAGNOSTIC publisher、Artifact budget、Manifest、CLI 与 Workbench；
- hostile Provider sandbox、Linux/macOS cell、并发、缓存、Q scheduling、D product shell 与 Cu attention projection。

## 8. 本地、Schema 与打包证据

实现 worktree 的最终完整 Review Attention 回归四格均为 `178/178`：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `178 tests / 369.838s / OK` |
| CPython 3.10.6 `-O` | `178 tests / 362.075s / OK` |
| CPython 3.13.13 normal | `178 tests / 362.667s / OK` |
| CPython 3.13.13 `-O` | `178 tests / 360.233s / OK` |

本文起草 worktree 又从实现 exact main 串行重跑 Relation + boundary focused matrix：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `24 tests / 37.989s / OK` |
| CPython 3.10.6 `-O` | `24 tests / 37.194s / OK` |
| CPython 3.13.13 normal | `24 tests / 38.525s / OK` |
| CPython 3.13.13 `-O` | `24 tests / 37.871s / OK` |

同一 docs-only worktree 的完整 CPython 3.13 normal 回归为 `178 tests / 357.479s / OK`；root Schema 回归在
3.10/3.13 均为 `27/27`。两套解释器均对全部十一份变更 Python 文件完成 `py_compile`。

最终 wheel 为 `veritrail_review_attention-0.1.0.dev0-py3-none-any.whl`，SHA-256：

```text
dea2b8fc00d843185fe2f9629f9183fe49ebd5d91d158dd3c7b1b3b4483dea0d
```

wheel 已安装到 fresh CPython 3.13 venv，从 isolated `site-packages` 导入 private Relation modules 并核对 wire；
顶层 package 没有导出 private `run_closed_test_relation_derivation`。第一次 clean-wheel 脚本因 PowerShell
`Select-Object -Single` 不是合法参数而在选择 wheel 时失败；它没有运行产品 probe。后继使用新 fresh venv 与
明确数组计数完成上述安装验证，没有把脚本输入错误解释成产品失败。

## 9. 远端实现因果链

实现从冻结合同 exact main 建立：

```text
base = 04cdc6bd3aa33ee77819af9e5764591d3469004c
head = db6148020b3333104a93ec602c7a7c1c5a5e3ab6
merge = 122d0c6b9d3c7a4518f12aec2f503f8979018dda
parents = 04cdc6bd3aa33ee77819af9e5764591d3469004c
          db6148020b3333104a93ec602c7a7c1c5a5e3ab6
tree = 5db4e21a7fceda54eab184b0fea498d365da1fee
```

[PR #156](https://github.com/NoctilumeDev/VeriTrail/pull/156) 的原始
[Public CI run 35512727369](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35512727369) 为 attempt 1、
11/11 SUCCESS。PR 以普通 merge commit 合入受保护 `main`；candidate head 与 merge commit 的 tree 相同。

新 exact main 的 [Public CI run 35513598312](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35513598312)
为 attempt 1、11/11 SUCCESS；
[Browser Smoke run 35513598411](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35513598411) 为 attempt 1、
1/1 SUCCESS。没有 repair PR、rebase、rerun 或后继成功覆盖先前失败的因果分支。

## 10. 匿名 exact-SHA 源码读回

在无 GitHub token 的 fresh HTTP client 中，从 `raw.githubusercontent.com` 对 exact
`122d0c6b9d3c7a4518f12aec2f503f8979018dda` 读取全部十一份变更文件。请求均为 HTTP 200、无 URL 漂移；远端
bytes 与本地 exact merge tree 逐项同大小、同 SHA-256，重新计算的 Git blob identity 也逐项匹配 merge tree。

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `_relation_closed_provider.py` | 5159 | `efb6526b03f84357ee8cdc373ba2eb7b711d12e951fd66790415b84de6640346` |
| `_relation_derivation.py` | 24840 | `fdaf5d9da2d57310c12f927e7d44984e670dd287c3c5abdc332ee2691f7594aa` |
| `_relation_derivation_values.py` | 4227 | `079689d49785b9bb0351bcadae959400586f130bb25267d00dac857d42b52835` |
| `_relation_execution_cell.py` | 13336 | `a0f059d32730b114e938235ed1240b3c7814664cdf75e490575f4af1c54d0f93` |
| `_relation_execution_cell_application.py` | 27632 | `49ef448c6d095d7b417e62b5095263a621ac59f5d02d2d961165cf4ad3fddde8` |
| `_relation_execution_cell_binding.py` | 1928 | `f214051174c96e18cff53222b7169859405832d99031a0efe228f01a63bf2ccf` |
| `_relation_execution_cell_values.py` | 1794 | `5e3021b25affb524b6588141a2ec78cc9c26680987f266911a3170de054e80fd` |
| `_relation_execution_cell_worker.py` | 2609 | `672e58ce408a13d22d7d0dc3b3e1b0bbd1ece3ce4b3fec80eba2cae2655b5da2` |
| `tests/support.py` | 4761 | `5bff903949120320335e7b2acf28b81c171f31ed1df40d98cbed2691acc63a61` |
| `tests/test_boundaries.py` | 11052 | `b351d50080f3564d6808642a1e5fb30fa8f0232daf7c258610eb5cbd910a5e18` |
| `tests/test_relation_derivation.py` | 33085 | `36f0216bf21d6b5fc771bd9d62ae536da0c67a2255493d89195da8c43951ca40` |

表中短路径位于 `plugins/review-attention/src/veritrail_review/` 或
`plugins/review-attention/tests/` 对应目录。按 `path<TAB>bytes<TAB>sha256`、LF join 形成的规范行 SHA-256 为：

```text
52510795bf4a479d3f6b58cd1aaa643eb0560d6f764f726b89ee0c9e37b8ea4f
```

该读回只证明公开 exact bytes 与 Git tree 身份一致；HTTP 成功本身不证明实现符合合同。

## 11. 本候选自己的最后门

本文与入口索引完成后，当前状态只能是 implementation freeze candidate。本文必须重新完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、敏感模式、生成物与 `git diff --check` 成立；
3. Relation + boundary focused 24 项在 CPython 3.10/3.13 normal/`-O` 下成立；
4. 原始 PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写 `R1_RELATION_DERIVATION_FROZEN`。

任一门失败，保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、继承 PR #156 或旧合同门
作为本文证据，也不得开始完整 Relation algorithm、RelationSet、Slice、Coverage、publisher、CLI 或 Workbench。

## 12. 下一门与 Fresh-Agent 交接

当前 fresh Agent 的唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，
仍须从新的 exact main 创建独立最终冻结发布；只有该发布完成自身门禁、合入与匿名产品读回以后，才允许再做
一次系统级俯瞰并选择下一个最小合同闭环。

后继选择不得由本文预先承诺。真实 parser 扩展、RelationSet admission/conflict/UNKNOWN、Slice、Coverage、
DIAGNOSTIC/COMPLETE publisher 都只是待比较候选；不得因一条 private Relation candidate 已经可以诚实存在，就
把 R1 描述成完成，更不得一次并行实现多条后继链。
