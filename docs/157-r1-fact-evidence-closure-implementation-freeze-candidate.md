# R1 Fact Admission / DerivationEvidence Closure 实现冻结候选

> 候选记录状态：`R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTED /
> R1_FACT_EVIDENCE_CLOSURE_FREEZE_CANDIDATE /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`23b07d6059d13107044746b2a4627c26f302bb4f`
>
> 实现提交：`8b397fc70d444048a2c8fcd04ccc00cb593fa1b1`
>
> 受保护主线实现基线：`86b62464b9eef00a5e9da8d0549f093767be27e2`
>
> 主线 Tree：`8bfd7a404b73057365c58b5493e3a10d4a074450`
>
> 实际影响层级：`L1_COMPONENT_INTERNAL`

## 1. 当前裁决

[文档 155](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)与
[文档 156](156-r1-fact-evidence-closure-contract-freeze-publication.md)授权的 private、non-published
Fact/Evidence closure 已实现并合入受保护主线。实现只证明以下命题：

> 同一个 integrated controller 可以沿用一次已拥有的 DerivationInputSet、BudgetContext、attempt eligibility、
> Provider binding 与 phase snapshot，在不重新读取 transport、路径或 Provider state 的前提下，完成
> application-canonical Fact admission、owned FactSet construction state、non-success Evidence projection 与
> 一次性 diagnostic closure eligibility 的机械闭合。

本实现没有创建 output path、Artifact writer、publisher、真实 Python parser、公共 Provider SPI、Relation、
conflict/UNKNOWN、Slice、Coverage、完整 R1 Manifest、CLI 或 Workbench 能力，也没有修改 Core、P、Q 或 D。
本文只是 docs-only implementation freeze candidate；它自己的门禁、受保护主线合入、exact-main 复验、匿名
产品读回与后继独立最终状态发布尚未发生，因此当前不得写成
`R1_FACT_EVIDENCE_CLOSURE_FROZEN`，也不解除 Relation/Slice/Coverage 或 publisher 的停止线。

## 2. 实现边界

实现只修改五个文件：

```text
plugins/review-attention/src/veritrail_review/
  _execution_cell.py
  _fact_evidence_closure.py
  _fact_evidence_values.py

plugins/review-attention/tests/
  test_boundaries.py
  test_fact_evidence_closure.py
```

源码 diff 为 1626 insertions、2 deletions。`_execution_cell.py` 只把既有 standalone cell 拆成 one-shot prepared
attempt 与 consume boundary，使后继 private controller 能沿用原始 BudgetContext、eligibility 与 owned inputs；
standalone 入口保持原签名与语义。两个新增模块都保持私有，`veritrail_review.__init__` 没有新增 export，base
package 也没有增加默认依赖。

新增 private 入口固定为：

```text
run_closed_test_fact_evidence_closure(
  inputs,
  *,
  derivation_id,
  binding,
  cancellation_requested,
  transport_limits
)
```

它没有 output directory、output path、publisher、Manifest、provider discovery 或 caller-selected budget 参数。
closed test Provider 仍由既有 product-owned allow-list 选择；本实现没有形成第三方 Provider API 或兼容承诺。

## 3. Identity、authority 与 snapshot continuity

### 3.1 同一 attempt 没有被路径或序列化重新定位

private `_PreparedExecutionAttempt` 一次拥有：

```text
DerivationInputSet
derivation_id
Provider binding
BudgetContext
AttemptEligibility
request provenance
attempt start observation
canonical request/frame bytes
```

prepared attempt 只能 claim 一次。integrated controller 直接消费同一个对象，不能用 standalone phase result 加新
BudgetContext 续接同一 derivation，也不重新读取 transport、Provider state、输入路径或临时文件。因此：

```text
verified phase snapshot = admission/projection consumed snapshot
path or serialized value != continuation authority
```

### 3.2 四层 Fact 身份仍然分离

```text
Provider candidate
  != application-canonical Fact
  != admitted FactSet member
  != published Fact Artifact member
```

application worker 仍拥有 candidate shape 与 canonical Fact identity；integrated controller 重新验证 phase/input/
binding continuity、Fact anchor/scope/profile、subject/fact digest、单一 provenance、排序去重与双向 reported-ID
closure。成功只形成 copy-owned `OwnedFactSetConstructionState`；其中 canonical bytes 没有路径、Manifest role、
public lifecycle 或 standalone publication authority。

### 3.3 phase 与 final Evidence 是不同 immutable projection

成功 phase 的 `ProviderRun` 可以保留已提交 Fact IDs；模拟 downstream artifact stop 时，新的 final Evidence
projection 保留 run status 但清空 final reported arrays。实现没有原地修改 phase value，也没有在成功路径提前
构造 provisional `COMPLETED DerivationEvidence`。

## 4. Eligibility 与 terminal capability

三种能力没有压成一个 boolean：

```text
normal continuation eligibility
diagnostic closure eligibility
cleanup-only permission
```

- completed phase 只有在 release 已完成、attempt 仍 ADMITTED、BudgetContext 仍 RUNNING、没有 stop latch 时才
  进入 Fact admission；admission 失败会不可恢复地 revoke eligibility；
- `PROVIDER_UNAVAILABLE`、`PROVIDER_FAILED`、`NONCONFORMANT_PROVIDER_OUTPUT` 与具有合法 phase result 的
  `INTERNAL_DERIVATION_ERROR`，只有在原 BudgetContext 仍 RUNNING、release 已闭合、没有 stop 且 artifact
  reservation 为零时，取得一次性 private diagnostic claim；
- deadline、caller cancellation、positive memory stop、artifact reservation stop 与 release failure 不取得
  diagnostic publication eligibility；
- projection 或 eligibility 检查失败会永久 revoke，后到的成功状态不能恢复资格。

stop 类 terminal 与 artifact-budget stop 可以在 private conformance helper 中形成 canonical in-memory Evidence
projection，以证明 status、diagnostic placement、空 reported arrays 与 digest 能同时成立；这种 shape capability
不等于 runtime publication capability。integrated runtime 对这些 stop 仍只返回 cleanup-only / calling-layer
结果，不授予 staging、reservation 或 publisher 权力。

## 5. `FA-001..024` 合同映射

| 合同族 | 已实现的证明义务 |
| --- | --- |
| FA-001..003 | 单 Fact、合法 empty 与 byte-identical duplicate 形成 owned、non-published construction state |
| FA-004..007 | anchor/input/profile/identity 漂移、双向 reported-ID 断裂与同 subject 不兼容 Fact 均 fail closed |
| FA-008..010 | copy ownership、无 publication surface，以及 phase/final reported-ID projection 分离 |
| FA-011..014 | 四类 non-budget terminal 的 run/top 同 tuple 与 one-shot diagnostic eligibility |
| FA-015..020 | stop/预算/release/placement/cardinality 负向矩阵，不把 shape capability提升为 publication |
| FA-021..022 | sufficient budget 不污染 provenance-free Fact semantics；standalone phase 不能用新 budget 续接 |
| FA-023..024 | 双 Python normal/`-O` 一致；private signature、imports 与 filesystem 均无 publisher/output 能力 |

`test_fact_evidence_closure.py` 的 19 个测试与 `test_boundaries.py` 的 8 个测试共同覆盖 27 个运行与边界义务。
表格只建立合同到证据的索引，不把测试方法、private helper 或 closed test Provider 写成公共产品语义。

## 6. 实现后系统审计

本轮没有按 finding 数量凑审计 KPI。审计逐条比较文档 155、实现对象、测试、包边界与 exact-main 运行事实；
没有发现需要重开冻结合同的新 blocker。

### 6.1 已确认成立的接缝

1. **Budget continuity**：execution 与 admission/projection 共享同一 BudgetContext、absolute deadline 与
   eligibility；没有 second budget、hidden checkpoint 或 timeout refresh；
2. **Snapshot continuity**：controller 消费同一次 execution call 返回的 immutable phase value，不按 path 或
   transport 二次读取；
3. **Publication separation**：FactSet artifact bytes 只是 future assembler 的 exact value；没有文件创建、路径、
   reservation、publisher 或 Manifest；
4. **Warrant separation**：stop projection 可由现有 Schema 表达，但 integrated runtime 不据此获得 stop 后写
   Artifact 的权力；
5. **Ownership separation**：所有对外 copy 都由 canonical bytes 重新解码，调用方 mutation 不改变 controller
   owned value；
6. **Package separation**：new closure 是 private site-packages module，顶层 API 与 base dependency surface 不变。

### 6.2 本轮未改的延期风险

- real parser、encoding/anchor、partial AST 与 unsupported language handling；
- multi-Provider Fact admission、RelationSet、conflict/UNKNOWN 传播；
- public FactSet/DerivationEvidence publisher、output coordinate、create-new directory 与 artifact-budget proof；
- ReviewSliceSet、CoverageLedger、COMPLETE/DIAGNOSTIC Manifest assembler；
- hostile Provider sandbox、cross-platform cell、Q scheduling/cache、D product shell、JPyxis adapter 与
  AI Execution OS。

这些问题仍可能在后继最小合同审计中暴露真实裂缝；它们没有证据要求本候选提前扩张。

## 7. 本地与打包证据

实现 head 的 Review Attention 完整矩阵在 CPython 3.10/3.13 normal/`-O` 四格均为 `133/133`。本文候选又从
exact-main worktree 串行重跑 Fact/Evidence closure 与 public-boundary focused gate：

| 门 | CPython 3.10 | CPython 3.10 `-O` | CPython 3.13 | CPython 3.13 `-O` |
| --- | ---: | ---: | ---: | ---: |
| Fact/Evidence closure + boundary | `27/27` | `27/27` | `27/27` | `27/27` |

每一格的 Core source、Review Attention source 与 test root 都绑定当前 exact-main worktree；没有继承其他
editable checkout 的实现坐标。

在 detached exact-main worktree 中，以已安装 `setuptools 80.9.0` / `wheel 0.46.3` 和
`pip wheel --no-deps --no-build-isolation` 构建 base wheel：

```text
veritrail_review_attention-0.1.0.dev0-py3-none-any.whl
SHA-256 a2276e192d8f1bba636f6a14d7bda80f6342d64a1f493e588b79bf160cbb7e40
```

fresh venv 以 `--no-deps` 安装该 wheel，`-I` child 从 isolated `site-packages` 导入 distribution 与
`_fact_evidence_closure.py`；`win32api` 未加载，顶层包没有导出 private closure。最初尝试使用
`python -m build` 时，重启后的本机 interpreter 不含 `build` module，因此在产生 artifact 前停止；随后按
pyproject 的 `setuptools.build_meta` 和本机实际 build capability 重建。这不是产品失败，也没有被记录为通过证据。

第一次 wheel probe 的 PowerShell 选择表达式无效，因而只创建 wheel/venv、未执行安装与 probe；该本地脚本
错误被作废，最终结果由显式 `wheel count == 1`、fresh install 与 `-I` import 重新建立。

## 8. 远端实现因果链

实现最初从冻结合同 exact main 建立：

```text
contract main = 23b07d6059d13107044746b2a4627c26f302bb4f
original implementation head = 4b390ac37839fa8b65ec9202c4a1e0e46152a17e
```

[PR #140](https://github.com/NoctilumeDev/VeriTrail/pull/140) 的首次
[Public CI run 34819121759](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34819121759) 在 Python 3.10
aggregated job 到达既有 15 分钟 job-level outer timeout 后被取消。取消前 Core、Authoring、GitHub Evidence、
Review Attention normal/`-O` 与七个 E1 资产下载/摘要均已通过；中断发生在 E1 clean-install acceptance，不能
叫 flake，也不能用后继成功替换该历史事实。

审计确认近期开销使 Python 3.10 exact-main jobs 已处于 10:44–14:27，15 分钟外层 containment 只剩最多数十秒
恢复余量；该限制不属于任何产品 timeout 或冻结语义。因此实现保持不动，独立
[PR #141](https://github.com/NoctilumeDev/VeriTrail/pull/141) 只把 aggregated Python lane 的 outer
containment 从 15 分钟调整为 20 分钟：

```text
repair head = 2b51cb607588bf220e19cf23715210324584d028
repair merge = cee30f68db1693eb9185cda7a827a2629660c621
repair tree = 3d3da8af5ef73823fa97877198326b0476c73bdf
```

PR #141 原始 [Public CI run 34820959395](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34820959395)
为 attempt 1、11/11 SUCCESS；repair exact main 的 Public CI `34822412395` 为 11/11、Browser Smoke
`34822412401` 为 1/1，均为 attempt 1。匿名 exact-SHA 读回的 workflow bytes SHA-256 为
`4c0ab5d4c87558dbb4308b9d47bdce26825019469170a12e2bf533f8008ee183`，与本地 Git tree 一致。该补丁只增加
外层恢复余量，不改变任何 inner product timeout、gate、资产坐标、摘要或 acceptance threshold。

实现随后 rebase 到 repair exact main；rebase 前后 patch-id 均为
`c6a6162cf93df276c7db1734d732a72b27da9177`：

```text
base = cee30f68db1693eb9185cda7a827a2629660c621
head = 8b397fc70d444048a2c8fcd04ccc00cb593fa1b1
merge = 86b62464b9eef00a5e9da8d0549f093767be27e2
parents = cee30f68db1693eb9185cda7a827a2629660c621
          8b397fc70d444048a2c8fcd04ccc00cb593fa1b1
tree = 8bfd7a404b73057365c58b5493e3a10d4a074450
```

rebase 后 PR #140 的原始有效
[Public CI run 34824079525](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34824079525) 为 attempt 1、
11/11 SUCCESS。PR 以普通 merge commit 合入受保护 `main`；新 exact main 的
[Public CI run 34825496310](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34825496310) 为 attempt 1、
11/11 SUCCESS，[Browser Smoke run 34825496263](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34825496263)
为 attempt 1、1/1 SUCCESS。

## 9. 匿名 exact-SHA 源码读回

在无 GitHub token 的 fresh HTTP client 中，从 `raw.githubusercontent.com` 对 exact
`86b62464b9eef00a5e9da8d0549f093767be27e2` 读取全部五个变更文件。远端 bytes 与本地 detached exact-main
worktree 均逐项同大小、同 SHA-256：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `_execution_cell.py` | 17907 | `a34bb1ad688182db5bc3e186d8ee13d9104e2a9e162b45c7be475352755d0359` |
| `_fact_evidence_closure.py` | 24838 | `9f030b03cedfc82dfe614047cd6d1e54dd960ca0235cb663d6ee61aa93abd04b` |
| `_fact_evidence_values.py` | 5940 | `98e70d07cebd2cba7f731177462e04a56f73d00436a1668cba5e3fd1ccbceff9` |
| `test_boundaries.py` | 9030 | `8bd34a4584d3622160edb290cdc1d0410b4c2a4240601d56361e61fc3820ed94` |
| `test_fact_evidence_closure.py` | 27595 | `b85d38746a5f6511e7c7ac69b160b44685f1f6f6c4d3beadb20848e47ff580aa` |

表中短路径位于 `plugins/review-attention/src/veritrail_review/` 或
`plugins/review-attention/tests/` 对应目录。该读回只证明公开 exact bytes 与 Git tree 相同；合同、审计、测试、
打包与完整门禁共同承担实现资格，HTTP 成功本身不等于正确性。

## 10. 本候选自己的最后门

本文与入口索引完成后，当前状态只能是 implementation freeze candidate。本文必须重新完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、敏感模式、生成物与 `git diff --check` 成立；
3. Fact/Evidence closure + boundary 27 项在 CPython 3.10/3.13 normal/`-O` 下成立；
4. 原始 PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_FACT_EVIDENCE_CLOSURE_FROZEN`。

任一门失败，保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、把 PR #140 或旧合同门
继承为本文证据，也不得开始 output publisher、真实 parser、Provider SPI、Relation、conflict/UNKNOWN、Slice、
Coverage 或完整 Derivation Manifest。

## 11. 下一门与 Fresh-Agent 交接

当前 fresh Agent 的唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，
仍须从新的 exact main 创建独立最终冻结发布；只有该发布完成自身门禁、合入与匿名读回以后，才允许重新审计
下一个最小合同闭环。

后继具体选择不得由本文预先承诺。可以比较：

```text
diagnostic publisher/output coordinate
real parser/provider boundary
multi-Provider Fact/conflict/UNKNOWN boundary
RelationSet boundary
```

但必须先做系统审计，再冻结一个最小合同；不得因本闭环拥有 FactSet bytes 或 Evidence projection 就直接发布
Artifact，更不得同时开始 Relation、Slice、Coverage 或完整 Derivation 实现。
