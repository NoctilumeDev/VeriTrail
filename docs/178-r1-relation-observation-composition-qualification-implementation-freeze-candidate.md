# R1 Relation Observation / Composition Qualification 实现冻结候选

## 1. 当前裁决

> 状态：`R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTED /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FREEZE_CANDIDATE /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 175](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
>
> 合同冻结发布：[文档 176](176-r1-relation-observation-composition-qualification-contract-freeze-publication.md)
>
> CI 地基修正：[文档 177](177-m10-ci-fixture-observation-correction.md)
>
> 实现 PR：[#165](https://github.com/NoctilumeDev/VeriTrail/pull/165)
>
> 实现 exact main：`3b4a55cad4e4f093c27dd8e9736d24d3b905dd54`

文档 175 第 14 节 A–H 已在 private closed proof 中物化。实现从 exact FactSet 与冻结 observation profile
机械建立责任域，让两个固定 required Relation sources 分别报告逐 item `ObservationOutcome`，再由 application
对 outcome、candidate、terminal 与 provenance 做机械对账并生成 private owned qualification result。

该实现没有创建或修改公共 Schema、RelationSet、DerivationEvidence、Manifest、publisher、output coordinate、
CLI、Workbench、Slice 或 Coverage。`QUALIFIED` 只证明本次 bounded responsibility 已闭合；它不证明 candidate
真实性、完整 Python Relation universe、conflict 已解决、RelationSet 已 admission、Coverage 完整或任何 Verdict。

本文记录实现事实与资格证据，不发布最终冻结。本文自己的原始远端门、受保护主线合入、新 exact-main 双门、
fresh anonymous installed-product readback，以及后继独立最终状态发布全部成立前，不得写
`R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN`。

## 2. 实现边界

实现变更严格限于 `plugins/review-attention` 的九个 private runtime module、一个新回归 module 与既有 boundary
test：

```text
_relation_observation_application.py
_relation_observation_binding.py
_relation_observation_cell.py
_relation_observation_cell_values.py
_relation_observation_cell_worker.py
_relation_observation_domain.py
_relation_observation_provider.py
_relation_observation_qualification.py
_relation_observation_qualification_values.py
tests/test_relation_observation_qualification.py
tests/test_boundaries.py
```

精确实现 diff 为 `3812 insertions / 12 deletions`。顶层 `veritrail_review` 没有导出
`run_closed_test_relation_observation_qualification`；private cell 不导入 publisher、Artifact budget 或 `ast`，
只有实际使用固定 parser 的 private Provider 导入 `ast`。变更没有触及 `schemas/`、公共 `__init__.py`、Core、
GitHub Evidence、Workbench 或 workflow。

## 3. Observation domain、责任与 identity

`observation_profile_document()` 固定 `closed-python-import-observation / 0.1-test`，只接受已冻结 Python 3.10
Profile 的 `LEXICAL_CONTAINS` 与 `IMPORT_TARGET_LITERAL`，以及 required `CUMULATIVE`
`review-relation-derivation` Policy requirement。两个 responsibility 在 Provider 启动前固定：

- `closed-relation-provider-a` required，只负责 `LEXICAL_CONTAINS`；
- `closed-relation-provider-b` required，负责 `LEXICAL_CONTAINS` 与 `IMPORT_TARGET_LITERAL`。

domain builder 从 exact FactSet 机械生成 Fact-backed observation items，并同时复核 frozen input digests、FactSet
identity、唯一 `MODULE` anchor、`IMPORT_DECLARATION` shape 与 import ordinal。输入不支持时整体 fail closed；不得
通过删 item、换责任或从实际 candidate 反向构造 denominator 获得资格。

`observation_domain_digest` 绑定 exact FactSet、observation profile 与 A/B responsibility；relation-only operands
另起 `veritrail.review.provider-operands/0.3`，cell wire 另起 `veritrail-review-relation-cell/0.2`。历史
`provider-operands/0.2` 与 relation-cell `/0.1` 没有原位改写。

## 4. Provider 履责与共享预算

两个 Relation sources 继续使用同一个 live `BudgetContext`、absolute deadline 与 stop latch 串行执行。后继 source
不会获得第二份预算；interruption、memory、deadline、unavailable、failed、nonconformant 与 release failure 保持
typed 区分，停止后不保留 prefix output，也不启动尚未开始的后继 source。

Provider 只消费 request 中与 exact FactSet operation 对应的 blob，不读取 Snapshot 其他文件来扩大权限。它实际
运行固定 Python 3.10 grammar parser 后才报告 parser identity，并为每个 assigned item 独立返回
`ObservationOutcome`。当前两个 total-obligation family 都要求 `EXACTLY_ONE` candidate 且不允许 negative
outcome；candidate 缺席不能由 application 补成“未发现 Relation”。

`ProviderRun COMPLETED`、source-local terminal、required source-set terminal、required observation closure 与
candidate composition 是五个独立状态。non-empty responsibility 上的 `COMPLETED + []` 仍不闭合；complete-empty
只允许 assigned item 集本来为空、Provider 真实 start/terminal、outcome/candidate 均为空且 release 无残留。

## 5. Reconciliation、composition 与 private result

application 对每个 source 建立 private receipt，并双向复核：

- assigned item 必须恰好有一个可归属 outcome；missing、duplicate、unassigned 与 identity mismatch 都保留为失败；
- candidate 必须映射到 assigned item，`candidate_ids` 与 outcome、terminal reported IDs、canonical bytes 相互一致；
- same-ID 且相同 semantics 的 candidate 只合并 provenance，不折叠各 source receipt；
- same subject 的不兼容 candidate 保留 private conflict，不选择 winner；
- same relation ID 但 semantics 不同属于 integrity failure，不降格为普通 conflict。

因此 `qualification_status=QUALIFIED` 可以与 `candidate_composition_status=CONFLICTING` 同时成立：前者只表示该看
的责任均有合格记账，后者表示看全后仍有分歧。`OwnedRelationCompositionQualificationResult` copy-own domain、
Fact/Relation phase results、ProviderRun、receipts、merged candidates、private conflicts、reason codes 与
qualification digest；它只存在于内存，不写 Artifact、Manifest 或公共 RelationSet。

## 6. `RQ-001..028` 合同映射

| 合同面 | 当前实现与反例 |
| --- | --- |
| `RQ-001..004` | exact preflight 拒绝 required source 缺失、额外 source、descriptor drift 与 optional requiredness |
| `RQ-005..007` | Fact-backed domain、真实空责任与 unsupported Fact 不缩 denominator |
| `RQ-008..009` | identity 同时绑定 FactSet、domain 与 exact assignment |
| `RQ-010..013`、`RQ-021` | Provider terminal 与 observation closure 分开；非空责任的零/部分 outcome 不闭合 |
| `RQ-014..017` | negative、duplicate、missing、unassigned、candidate/outcome mismatch 与 dangling ref fail closed |
| `RQ-018..020` | same-ID provenance union、qualified conflict 无 winner、identity collision 属 integrity failure |
| `RQ-022` | interruption 与 release failure 阻止后继、丢弃 prefix result且不能 qualification |
| `RQ-023` | A/B 共享原 live budget，不刷新 deadline、memory 或 artifact accounting |
| `RQ-024..025` | import literal 保守解析，parser identity 只有真实 parser 使用后才报告 |
| `RQ-026..027` | owned result private、unpublished、无顶层 export，不取得 RelationSet/Evidence authority |
| `RQ-028` | 双 Python normal/`-O` 的 golden identities 与 canonical projections 一致 |

新回归 module 以十七个 test method 覆盖全部 `RQ-001..028`，boundary test 又约束 private/nonpublishing surface。
测试数量只是观察范围，不把 Provider 自述变成独立事实权威。

## 7. 实现后系统复核

实现复核没有发现必须重开文档 175/176 的 blocker：

1. obligation enumeration 与 fulfillment 由 domain 和逐 item outcome 分开承载；
2. application 只验账，不从 candidate absence、Provider terminal 或 public Schema shape 补事实；
3. A/B 都是实际执行的 responsibility，没有不执行却进入 submitted responsibility table 的 ghost source；
4. domain 完整性错误整体 fail closed，不允许静默缩小分母后仍 `QUALIFIED`；
5. conflict、integrity failure、interruption、missing outcome 与 release failure 没有被统一压成空数组；
6. `QUALIFIED`、`CONFLICTING`、RelationSet admission 与 final Evidence authority 保持正交。

该复核只支持“文档 175 A–H 的 private closed proof 已实现”。它不支持完整 Relation algorithm、真实 import
zero/one/many resolution、public Provider SPI、caller-selected responsibility、公共 Schema correction、RelationSet、
publisher、Slice、Coverage、Attention、CLI、Workbench、D、Cu 或 Q。

## 8. 本地、打包与远端证据

本文起草 worktree 从 implementation exact main 串行运行完整 Review Attention 双 Python normal/`-O` 四格；
最终结果在本候选提交前固定：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `195 tests / 418.853s / OK` |
| CPython 3.10.6 `-O` | `195 tests / 403.760s / OK` |
| CPython 3.13.13 normal | `195 tests / 395.920s / OK` |
| CPython 3.13.13 `-O` | `195 tests / 391.564s / OK` |

同一最终 worktree 的 focused `test_relation_observation_qualification + test_boundaries` 四格为：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `26 tests / 32.958s / OK` |
| CPython 3.10.6 `-O` | `26 tests / 32.291s / OK` |
| CPython 3.13.13 normal | `26 tests / 33.006s / OK` |
| CPython 3.13.13 `-O` | `26 tests / 33.079s / OK` |

root Schema/payload 与 Evidence 0.1.1 消费回归在 CPython 3.10/3.13 normal 下各为 `27/27`；两套解释器
都对十一份实现变更 Python 文件完成 `py_compile`。Markdown runtime regression 在双 Python 下各为 `4/4`；
docs scope、relative links、fence、candidate marker、敏感/本机路径扫描与 `git diff --check` 均成立。

clean wheel 从 CPython 3.13 worktree 构建为
`veritrail_review_attention-0.1.0.dev0-py3-none-any.whl`：

```text
bytes  = 115343
sha256 = 16ca9a267186dd5f396e132f0043699f0188a926538867b0ebf1f8d5d7583d0c
```

该 wheel 安装到 fresh venv 后，九个 private observation/qualification module 全部来自 isolated
`site-packages`；顶层 package 仍没有导出 `run_closed_test_relation_observation_qualification`。

第一次 Markdown 命令漏掉 Core `src` root，在导入 `veritrail` 前失败，没有进入四项测试；补足实际 source-root
topology 后才形成上述双 Python `4/4`。随后第一次自写 docs scanner 又因 Python subprocess 使用 Windows 默认
GBK 解码含中文的 `git diff` 而停止；固定 UTF-8 后，才完成上述静态门。这两项均属于 local gate setup/tooling
failure，不是 runtime 或文档内容反证，也没有被后继成功改写为已经执行。

## 9. 远端实现因果链

实现与地基修正必须保持为两条链：

```text
contract freeze main = 65bdfa0a05f96693a7df9a1a86e27ecdb503b875
original impl head   = 015bf8f19ca1269933749c53f67eebe33186bc58
maintenance head    = 189abdfdf73a6b5b2f9e462b81f1b19b9fae8f94
maintenance merge   = 43fd5d3368f962677722d09d962718bced306449
requalified head    = 4bcba01dbdc7fb57c34451d154be8ef8f52bfb87
implementation merge= 3b4a55cad4e4f093c27dd8e9736d24d3b905dd54
implementation tree = f2becc7d31f7ca29fc265ea7690be248a48bf05e
stable patch-id     = bfbb87ec732a203bd9e8c321a45b2dc3574aeb5c
```

PR #165 原始 Public CI [run 35569800950](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35569800950)
在真正执行测试后保留 Python 3.13 emergency-cleanup fixture precondition failure 与 Python 3.10
`COLLECTOR_ERROR`。前者只证实旧夹具没有资格把瞬时空闲端口当作预约，原 Artifact 不足以恢复唯一底层触发；
后者精确根因继续是 `UNKNOWN`。后继绿色不得解释或覆盖这两条首败。

独立 maintenance PR #166 的 final-head Public CI
[run 35573748557](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35573748557) 为 11/11 SUCCESS；此前同
PR 的 run `35573699381` 因后继 push 被 concurrency 取消，不形成测试成功或失败结论。maintenance 合入后，
`main@43fd5d3...` 的 Public CI
[run 35575271109](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35575271109) 为 attempt 1、11/11，
Browser Smoke [run 35575271103](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35575271103) 为 attempt 1、1/1。

#165 随后从该 maintenance-qualified exact main 形成新 head；old/new implementation patch-id 与
`plugins/review-attention` diff 均相同。新 head 的 Public CI
[run 35577081157](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35577081157) 为 attempt 1、11/11 SUCCESS，
再以普通 merge commit 合入受保护 `main`。merge parents 为 `43fd5d3...` 与 `4bcba01...`，candidate head 与
merge tree 相同。

新 exact `main@3b4a55c...` 的 Public CI
[run 35578893674](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35578893674) 为 attempt 1、11/11
SUCCESS；Browser Smoke
[run 35578893670](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35578893670) 为 attempt 1、1/1 SUCCESS。
这些门证明新 source state 的运行资格，不反推旧 `COLLECTOR_ERROR` 的原因。

## 10. 匿名 exact-SHA 源码读回

清空 GitHub token 后，从 `raw.githubusercontent.com` 匿名读取 exact
`3b4a55cad4e4f093c27dd8e9736d24d3b905dd54` 的全部十一份实现变更文件。每次请求均为 HTTP 200、final URL
未漂移；远端 bytes 与 exact merge tree 逐项同大小、同 SHA-256，重新计算的 Git blob identity 也逐项匹配。

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `_relation_observation_application.py` | 27007 | `426bcaa8eb7386d4b405a648235679f7561c979deb1b349ac8863661b9418d1b` |
| `_relation_observation_binding.py` | 2400 | `55d14975adf34a083d083f8954fbf6132778613dacd8351834acb6f63d7ea97a` |
| `_relation_observation_cell.py` | 13919 | `87e3ede3bdb20d52d0f828bbb0a2b2eef92e7b1a9662789bb2644f491e921266` |
| `_relation_observation_cell_values.py` | 1737 | `39abd2648d60169c3ad7cb8ea95e453ebb5425adfd1c867a92598972f1561b88` |
| `_relation_observation_cell_worker.py` | 3077 | `a6f5569696b966e72ea4d2ad1d73c547dcb3460cabdbbbe3ac0758787292e2ba` |
| `_relation_observation_domain.py` | 12762 | `a539b3bdc8f0e39799753bf2973250c3c5d0ce1e1a7ade27c3ab3d47b1f57098` |
| `_relation_observation_provider.py` | 7567 | `f1754aa66196534c35bb44dad390a2791916e6e7fd78dd43033c9a3d2664c6a4` |
| `_relation_observation_qualification.py` | 41245 | `3376ea81d8fad565afef0d0079f2f33089664e052abd0cf43afc339dd56d86b1` |
| `_relation_observation_qualification_values.py` | 2176 | `6079407d42a52eb184cf2b70835465520171ff7f8b0c1bc3f5fd125d9bae2a3f` |
| `tests/test_boundaries.py` | 11632 | `edddfd8105cc8b1c085769c0dea03ae78d53d118e9905e2ebacac1e0cd8576df` |
| `tests/test_relation_observation_qualification.py` | 33404 | `7238261a8fb03bb72bd4ba833efaec9fd5f451b3c82f2a157f339dd330305f44` |

短路径位于 `plugins/review-attention/src/veritrail_review/` 或 `plugins/review-attention/tests/`。按完整
`path<TAB>bytes<TAB>sha256`、LF join 形成的规范行 SHA-256 为：

```text
9c36591b276df231ee6f03145fb52d683c9c0ce2ca78f4e72ef3c9bb702d3da6
```

匿名 readback 只证明公开 exact bytes 与 Git tree identity 一致；它不证明代码符合合同。

## 11. 本候选自己的最后门

本文与状态入口完成后，当前状态仍只能是 implementation freeze candidate。本文必须独立完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、敏感/本机路径、生成物与 `git diff --check` 成立；
3. qualification + boundary focused tests 在 CPython 3.10/3.13 normal/`-O` 下成立；
4. 原始 PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN`。

任一门失败，必须保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、继承 PR #165 或其
exact-main 绿色作为本文证据，也不得开始 RelationSet、公共 Schema、publisher、Slice、Coverage、CLI 或
Workbench。

## 12. 下一门与 Fresh-Agent 交接

当前唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，必须先对
README、本文与 milestones 建立三个互不复用的 fresh anonymous installed-product session；随后再从新的 exact
main 创建独立最终冻结发布。只有最终发布完成自己的门禁、合入、exact-main 双门与匿名读回以后，才允许重新做
post-freeze system audit。

本文不预选下一条 R seam。RelationSet admission、multi-Provider conflict/UNKNOWN、Slice、Coverage、Attention
与 publisher 仍只是待审候选；外部生产案例只有在内部审计出现具体经验缺口时才作为 hypothesis source 进入，
不能从本实现候选自动产生施工授权。
