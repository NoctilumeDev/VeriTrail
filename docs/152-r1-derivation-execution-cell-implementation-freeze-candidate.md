# R1 Derivation Execution Cell 实现冻结候选

> 候选记录状态：`R1_DERIVATION_EXECUTION_CELL_IMPLEMENTED /
> R1_DERIVATION_EXECUTION_CELL_FREEZE_CANDIDATE /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`3c89f8eb94333986fc4901b9a1b91edf47d0059f`
>
> 实现提交：`02e4d05dcfc7c062c97ecfa21c00b26f601b9140`
>
> 受保护主线实现基线：`8b77305cea3a95690660adcb25f76d2b42c6e5e1`
>
> 主线 Tree：`d7f502908c4a1361f8756d15f238fd05a1864b04`
>
> 实际影响层级：`L1_COMPONENT_INTERNAL + L3_SYSTEM`

## 1. 当前裁决

[文档 150](150-r1-derivation-execution-cell-terminal-envelope-contract.md)与
[文档 151](151-r1-derivation-execution-cell-contract-freeze-publication.md)冻结并授权的首个 execution-cell
切片已经实现并合入受保护主线。实现只证明以下命题：

> 一次 closed test Provider 执行可以在同一个 absolute budget、hard-contained Windows process cell、
> bounded single-terminal transport、不可恢复 attempt eligibility 与 controller-owned terminal mapping 下
> 完成或失败，并且只返回 copy-owned、尚未发布的 Fact phase value。

本实现没有创建真实 Python parser、公共 Provider SPI、FactSet、DerivationEvidence runtime publication、
Relation、conflict/UNKNOWN 传播、Slice、Coverage、完整 R1 Manifest、CLI 或 Workbench 能力，也没有修改
Core Verdict。本文只是 docs-only implementation freeze candidate；它自己的门禁、受保护主线合入、
exact-main 复验、匿名产品读回与后继独立最终状态发布尚未发生，因此当前不得写成
`R1_DERIVATION_EXECUTION_CELL_FROZEN`，也不解除下一个 provenance runtime 的实现停止线。

## 2. 实现边界

实现新增私有模块：

```text
plugins/review-attention/src/veritrail_review/
  _execution_cell.py
  _execution_cell_application.py
  _execution_cell_binding.py
  _execution_cell_protocol.py
  _execution_cell_values.py
  _execution_cell_worker.py
  _windows_execution_cell.py
```

并新增两组 execution-cell 测试，扩充公共边界与 Budget Primitive 回归。所有 execution-cell 模块保持私有；
`veritrail_review.__init__` 不导出 controller、binding、transport、worker、terminal value 或 Windows cell。

包与运行边界保持如下：

- base package 不因本切片新增运行时依赖；Windows capability 继续由既有 `budget-windows` extra 与 exact
  `pywin32==312` 提供；
- controller 只接受 product-owned closed allow-list 中的 test launch key，不接受 module string、entry point、
  pickle、ambient Provider discovery 或调用者 `sys.path` 选择；
- worker 使用当前 Python 的 exact executable，在 `-I` 下直接启动 product-owned worker file；它只定位同一
  product package，不能把测试 Provider 变成公共插件发现协议；
- request/result 各使用一条 application-owned 单向 pipe；frame 固定为
  `8-byte unsigned big-endian length + canonical JSON payload + EOF`；
- request payload 上限为 64 MiB，terminal payload 上限为 16 MiB；它们只控制本次执行资格，不进入 Fact identity；
- Windows worker 以 suspended-create、assign-to-owned-Job、final checkpoint、attempt admission、resume 的顺序
  启动，避免 Provider 在 containment 或 admission 以前运行。

## 3. Authority、identity 与 publication

### 3.1 三层 authority 没有压扁

```text
trusted controller
  owns admission / clock / stop latch / transport validation / release / phase commit

contained application worker
  owns request validation / candidate conformance / canonical Fact identity / terminal summary

closed test Provider
  owns bounded observation only
```

Provider 不能自报 `fact_id`、执行状态、时间、diagnostic 或 reported IDs。application worker 对候选执行固定
shape、scope、anchor、semantic attributes 与 identity projection 校验；controller 不把 frame 可解析误写成
Fact 合法，也不把 child exit code、OOM text、active hard limit 或 stderr 提升为 terminal cause。

### 3.2 attempt eligibility 不可恢复

`AttemptEligibility` 只有：

```text
PROVISIONAL -> ADMITTED
PROVISIONAL / ADMITTED -> REVOKED
```

primitive、protocol、terminal conformance、non-success 或 cleanup failure 一旦 revoke，后到的成功 terminal、
cleanup success 或底层仍为 `RUNNING` 的 BudgetContext 都不能恢复 phase commit 资格。pre-admission preparation
失败不生成 ProviderRun 或 phase result；admission 后 resume/pipe/worker 失败则保留已开始 run 的不归因失败。

### 3.3 路径、terminal 与被消费对象连续

controller 只把通过 `validate_terminal_document` 的 terminal 提升为 trusted terminal；验证失败的 untrusted
document 不能提供 `provider_run_id`。最终 run identity 始终由 controller 对 frozen operands 复算，而不是从
rejected terminal 复制。

success 还必须同时满足：

```text
valid terminal
+ attempt eligibility still ADMITTED
+ no stop latch won the race
+ process tree zero
+ handles and channel threads released
+ BudgetContext phase commit succeeds inside the same deadline
```

任何一项不成立都不会留下 canonical Fact bytes。返回的 `OwnedExecutionCellPhaseResult` 深拷贝并保存 canonical
bytes，但它没有输出路径、Manifest、Artifact publication 或顶层公共 API，因此：

```text
candidate Fact generated != FactSet published
phase result returned      != Derivation closure
```

## 4. Terminal mapping 与认识论上限

实现保持冻结的正向 warrant：

| 正向观察 | terminal mapping |
| --- | --- |
| deadline latch | `INTERRUPTED / EXECUTION_DEADLINE` |
| caller cancellation latch | `INTERRUPTED / EXECUTION_CANCELLED` |
| owned Job memory-limit event | `INTERRUPTED / EXECUTION_MEMORY_BUDGET` |
| valid Provider exception terminal | `FAILED / PROVIDER_FAILED` |
| valid Provider unavailable terminal | `UNAVAILABLE / PROVIDER_UNAVAILABLE` |
| application rejects candidate | `FAILED / NONCONFORMANT_PROVIDER_OUTPUT` |
| no valid continuity and no narrower warrant | `FAILED / INTERNAL_DERIVATION_ERROR` |

`INTERNAL_DERIVATION_ERROR` 不声称 Provider、application、transport、OS 或 memory 是根因。`DerivationEvidence
0.1.1` Schema 与 corpus 因此没有升级；pre-admission runtime capability loss 通过调用层 typed
`DERIVATION_RUNTIME_UNAVAILABLE` 表达，不伪造一个不存在的 ProviderRun。

## 5. `EC-001..024` 合同映射

| 合同族 | 已实现的证明义务 |
| --- | --- |
| EC-001..004 | t0 包含 preparation；具体 cell 在 admission 前保持 inactive；assign-before-resume；失败无伪 run |
| EC-005..007 | admission 后 resume failure 保留 run；request cap 与 closed binding fail closed |
| EC-008..012 | 可替换 test Provider 的 provenance-free Fact identity、合法 empty、Provider fail/unavailable 与 bad candidate |
| EC-013..015 | no-envelope、abnormal exit、partial/duplicate/trailing/noncanonical terminal 均不产生 Fact |
| EC-016..020 | terminal 后仍等待 owned release；deadline/cancel/memory race、primitive revoke 与共享 release deadline 不允许成功复活 |
| EC-021..024 | Provider 自报 authority 被拒绝；充分 budget/transport 不污染 Fact ID；non-success IDs 为空；retry 建立新 attempt |

`test_execution_cell_protocol.py` 的 7 个测试与 `test_execution_cell.py` 的 22 个测试共同覆盖上述 29 个
运行/协议义务。表格是合同到证据的索引，不把 unittest 方法名或 closed test Provider 写成公共产品语义。

## 6. 实现后系统审计

本轮没有按 finding 数量凑审计 KPI。只有会击穿冻结不变量或污染证据链的问题进入实现提交；其余后继问题
继续保持延期。

### 6.1 已在实现提交内修正

1. **rejected terminal 不能泄漏 run identity**：早期路径会在 terminal continuity 校验失败后保留 untrusted
   document，并可能继续读取其中的 `provider_run_id`。最终实现先隔离 `untrusted_terminal`，只有验证成功才
   赋给 trusted terminal；phase result 永远使用 controller 复算的 expected run ID；
2. **primitive commit failure 必须 revoke**：`try_complete_phase` 抛出 `BudgetPrimitiveError` 时，最终实现
   显式撤销 eligibility、清空 Facts，并映射为 stop 或不归因 internal failure；
3. **preparation 期间 runtime loss 不能泄漏底层异常**：concrete cell 二次 capability 检查失败经
   `CellRuntimeUnavailableError` 映射为 pre-admission typed error，没有 ProviderRun；
4. **release failure 不能冒充 phase result**：cleanup 未在共享 release deadline 闭合时抛出 typed
   `RELEASE_FAILED`，不返回带 `release_outcome=RELEASED` 的普通 value；
5. **late stop 能否决 early terminal**：terminal bytes 先到并不立即提交；process/handles/channels 与 final
   BudgetContext commit 仍处于同一资格边界。

### 6.2 作废并重建的本地证据

第一次 BP-014 clean-wheel probe 在父进程 `PYTHONPATH` 绑定当前 plugin source、且 source 含 editable
metadata 时，fresh venv 的 pip 把 ambient source 误认为已经安装；随后 `-I` child 正确地无法导入 package。
该结果不能证明当前 wheel 边界，已明确作废。

最终测试没有使用 `--force-reinstall` 掩盖来源问题，而是在 probe subprocess/venv 中移除父进程
`PYTHONPATH`，再由新构建 wheel 建立唯一安装坐标。这个修正证明：

```text
test source coordinate
!= ambient package metadata
!= fresh-interpreter import coordinate
```

### 6.3 明确延期，不在本候选解决

- real Python parser、encoding/anchor 与 partial AST；
- canonical FactSet admission、跨 Provider conflict/UNKNOWN 与 DerivationEvidence publication；
- application worker 的第三方信任、hostile Provider sandbox 与 cross-platform cell；
- RelationSet、ReviewSlice、CoverageLedger 与 COMPLETE/DIAGNOSTIC Manifest；
- Q scheduling/cache、D product shell、JPyxis adapter 或 AI Execution OS。

这些问题可能成为后继合同的真实输入，但不反向扩大本实现切片。

## 7. 本地实现证据

最终实现 head 的 Review Attention 完整矩阵为：

| 门 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| Review Attention normal | `113/113` | `113/113` |
| Review Attention `-O` | `113/113` | `113/113` |

本文 docs-only 候选又从 exact-main worktree 串行重跑定向门；每一格的导入路径都明确指向当前 worktree，
`pywin32` 均为 312：

| 门 | CPython 3.10 | CPython 3.10 `-O` | CPython 3.13 | CPython 3.13 `-O` |
| --- | ---: | ---: | ---: | ---: |
| Execution Cell | `29/29` | `29/29` | `29/29` | `29/29` |
| Budget Primitive | `21/21` | `21/21` | `21/21` | `21/21` |
| Public boundary | `7/7` | `7/7` | `7/7` | `7/7` |

冻结 R1 Schema/payload 消费回归在实现 head 的两套 Python normal/`-O` 四格均为 `27/27`。额外边界证据包括：

- base wheel 在无 `pywin32` 的 clean venv 可导入；新私有模块存在于 site-packages，顶层没有 execution-cell
  public export；
- Python 3.10/3.13 `compileall`、`git diff --check`、production `assert` 扫描、禁止后继对象扫描与敏感模式
  扫描通过；
- 全部 owned worker、Job handle、pipe thread 与测试 staging 完成清理，没有 execution-cell 进程残留。

完整仓库、发布资产、Workbench 与既有消费者不能由这些本地结果继承，仍由远端 required checks 单独建立。

## 8. PR #132 与 exact-main 事实

实现 PR 的精确因果链为：

```text
base = 3c89f8eb94333986fc4901b9a1b91edf47d0059f
head = 02e4d05dcfc7c062c97ecfa21c00b26f601b9140
merge = 8b77305cea3a95690660adcb25f76d2b42c6e5e1
parents = 3c89f8eb94333986fc4901b9a1b91edf47d0059f
          02e4d05dcfc7c062c97ecfa21c00b26f601b9140
tree = d7f502908c4a1361f8756d15f238fd05a1864b04
```

1. [PR #132](https://github.com/NoctilumeDev/VeriTrail/pull/132) 的原始
   [Public CI run 34765917607](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34765917607) 为 attempt 1、
   11/11 success，没有 rerun；
2. PR 以 merge commit `8b77305cea3a95690660adcb25f76d2b42c6e5e1` 合入受保护 `main`；
3. exact-main [Public CI run 34766798266](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34766798266)
   为 attempt 1、11/11 success；
4. exact-main [Browser Smoke run 34766798162](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34766798162)
   为 attempt 1、1/1 success。

这些事实证明 implementation head 与完整仓库门禁可以共同成立；它们不证明本文 docs-only candidate 已通过
自己的门，也不把 closed test Provider 外推为真实 parser 或公共 Provider capability。

## 9. 匿名 exact-SHA 字节读回

在未设置 `GH_TOKEN` / `GITHUB_TOKEN` 的 fresh HTTP client 中，从 `raw.githubusercontent.com` 对 exact
`8b77305cea3a95690660adcb25f76d2b42c6e5e1` 读取本实现的全部 12 个变更文件。远端 bytes 与本地 exact-main
worktree 均逐项同大小、同 SHA-256：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `_execution_cell.py` | 14266 | `56d058938905fe567c3b8f8a5f664fdf494c39ee3e7e4cd44d26e25343b91548` |
| `_execution_cell_application.py` | 26395 | `6f5536b60276ce4d3221ad0c0142ee47d970b89e43fd076be5f2686c893752d0` |
| `_execution_cell_binding.py` | 3313 | `6e93cf95e1e425864704cece60f2e2c4e3a92b60a87109609a10d9f9d1c83946` |
| `_execution_cell_protocol.py` | 4922 | `c97226a42fad4b42854dad9616dbd6e063d5c134417604f8aeff828b0b876266` |
| `_execution_cell_values.py` | 2039 | `d742fd5c48a250948031ee27610b9960510b7d89530ac48b3f3bb8f40711879e` |
| `_execution_cell_worker.py` | 2949 | `c99dadb275e938dcc6642546b627afec4f488373f7e1438a60872504ab02a634` |
| `_windows_execution_cell.py` | 18934 | `c90412ec2218110350dc7fef87ad8292113ffc550ec770eddb9ea46bae852af3` |
| `errors.py` | 10109 | `dd9bd3e31bec915d862bcaef1f6d31b0e35d414558517a5919dc9253d5c87919` |
| `test_boundaries.py` | 7034 | `42496f855bd959a1e1d0a4bb2e7bffef40a20b7d8f07d9a64127148ce0c0f8d0` |
| `test_budget_primitive.py` | 22976 | `43c177796fc2be6b3f87017e0a7643c91a2039f30924565fa6dbf9461d506893` |
| `test_execution_cell.py` | 23645 | `1a8447d359073dfcaed64ce9f1416bdac89caec473e4920de2b0e77a303f4ae5` |
| `test_execution_cell_protocol.py` | 4595 | `8e45db9d81fd68204a99811be08350da330f5a9631a69d6a5ad78f9d106e9e0c` |

表中短路径均位于 `plugins/review-attention/src/veritrail_review/` 或
`plugins/review-attention/tests/` 的对应目录。该读回只证明公开 exact bytes 可取得且与 Git tree 相同，不把
HTTP 成功提升为代码正确性；冻结合同、实现审计、conformance 与完整门禁共同承担后者。

## 10. 本候选自己的最后门

本文与入口索引完成后，当前状态只能是 implementation freeze candidate。本文必须重新完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、`git diff --check`、状态 marker、敏感模式与生成物检查通过；
3. Execution Cell + Budget + Boundary focused regression 在 CPython 3.10/3.13 normal/`-O` 下通过；
4. 原始 PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_DERIVATION_EXECUTION_CELL_FROZEN`。

任一门失败，保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、把 PR #132 或旧合同门
继承为本文证据，也不得开始真实 parser、FactSet/DerivationEvidence publication、Relation、Slice、Coverage
或完整 Derivation。

## 11. 下一门与 Fresh-Agent 交接

当前 fresh Agent 的唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，
仍须从新的 exact main 创建独立最终冻结发布；只有该发布完成自身门禁、合入与匿名读回以后，才允许重新审计：

```text
Provider Run
  -> candidate Fact provenance
  -> canonical Fact admission
  -> FactSet / DerivationEvidence closure eligibility
```

该后继仍必须先审计、再冻结最小合同，不得直接实现真实 parser，更不得越级进入 Relation、conflict/UNKNOWN、
Slice、Coverage 或完整 Manifest。
