# R1 Relation Derivation Authority / Operand Continuity 合同冻结发布

日期：2026-09-20

## 1. 发布对象、输入与条件状态

本文只发布[文档 165](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)已经审议的最小合同，
不补写新的 Relation 算法，也不把候选事实提前改成实现事实。

| 坐标 | 值 |
| --- | --- |
| 上游冻结状态 | `R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN` |
| 前置系统审计 | [文档 164](164-r1-post-composition-next-closure-system-audit.md) |
| 合同候选 | [文档 165](165-r1-relation-derivation-authority-and-operand-continuity-contract.md) |
| 候选 PR | `#151` |
| 候选 base / head / merge | `41a398783d5eaf25e15574df5beafb8465d0a91e` / `8ccc1066d665d2b7e290f929c2c84f22645def01` / `301f5248b77c67284b5e52bf287c23f286590e6b` |
| 本发布起草基线 | `main@8e5c0007c20b8c495195cdbdbb3a68891d88c3df` |
| 影响层级 | `L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

本文分支、原始远端门、受保护主线合入、合入后 exact-main Public CI / Browser Smoke 与本发布专属 fresh
anonymous installed-product readback **全部成立以后**，目标状态才是：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_PRECONTRACT_AUDITED
R1_RELATION_DERIVATION_CONTRACT_FROZEN
R1_RELATION_DERIVATION_IMPLEMENTATION_ALLOWED
R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

在最后一项成立前，这些只是本发布的条件目标；文档 165 的候选状态仍是当前已证事实。

## 2. 本次冻结的最小对象

冻结对象是 **composed FactSet 之后 Relation 事实生产权与精确 operand 连续性**，只包含下列相互不可分的
边界：

1. 新封存 Policy profile 中一个 phase-classified、required 的 `review-relation-derivation` requirement；
2. Fact-stage applicable runs 先 terminal 并完成 private join，随后才产生 copy-owned composed FactSet；
3. 只有第 6 节的保守 upstream gate 允许时，才启动 distinct Relation ProviderRun；
4. Relation run 的 owned input 绑定原 SourceSnapshot、Policy、scope、Profile、同一个 live
   `BudgetContext` 与 exact `fact_set_digest`；
5. Relation candidate 只能归因于实际报告它的 Relation run；Fact run 不回填 Relation IDs，application
   不自造 Relation target 或 provenance；
6. Relation terminal 后才允许计算 final overall；下游未完成时 private candidate history 不冒充可发布
   `RelationSet` 或 final Evidence；
7. FactConflict、optional-source gap、required-source non-success 与 absent normal FactSet 保留各自 typed
   upstream truth，不伪造 Relation run、empty success 或较小 normal Relation world。

因此冻结的是一个可独立证伪的 authority / continuity seam，不是“Relation 已实现”。

## 3. 冻结后的 authority 与时间顺序

### 3.1 四个 owner 继续分离

| owner | 拥有 | 不拥有 |
| --- | --- | --- |
| Human Seal authority | 新请求的 capability、requiredness、phase classification、Profile 与预算 | run-local 事实、候选回填或事后改写 |
| Fact Provider / composition controller | Fact terminal、same-ID merge/conflict、exact FactSet construction | Relation candidate、Relation 报告或 target 裁决 |
| Relation Provider | 在 exact copied operands 上 bounded 生成候选、真实 terminal 与实现身份 | FactSet 改写、其他 Provider 的事实、publication |
| application canonicalizer | conformance、identity、引用、copy ownership 与后继 admission 的机械校验 | 自造 Relation、任选冲突 winner、把 candidate 当 final RelationSet |

`Capability != Authority` 在这里有具体含义：一个 Provider 可以被发现或调用，不等于它可以修改其他阶段的
事实；application 可以复算 ID，不等于它成为 Relation producer。

### 3.2 phase join 不能形成循环

新 profile 必须把 Fact requirements 与 Relation requirement 分成固定 phase。顺序冻结为：

```text
Fact children terminal
  -> Fact-stage private join
  -> exact composed FactSet
  -> conservative upstream gate
  -> distinct Relation run terminal / cleanup
  -> final derivation status projection
```

required Relation run 不得计入产生其输入 FactSet 的 Fact-stage join。FactSet 构造成功也不等于 final
`DerivationEvidence.overall_execution_status=COMPLETED`。同一次 execution 从 Fact children 到 Relation child
始终持有原 absolute monotonic deadline 与 live shared `BudgetContext`；不能在一个 standalone Fact
composition 返回后，用新预算重启“同一次”Relation 执行。

## 4. exact FactSet operand 与 identity 连续性

文档 120 已冻结的 `veritrail.review.provider-operands/0.1` 不含 `fact_set_digest`，因此不能证明两个 Relation
runs 看见了同一份 composed Fact universe。本冻结确认文档 165 的 relation-only 版本化修正义务：

```text
domain  = veritrail.review.provider-operands/0.2
payload = frozen provider-operands/0.1 payload + {fact_set_digest}
```

这里冻结的是语义投影与兼容边界，不是已存在的 runtime bytes：

- 原有 Fact runs 与历史 Artifact 继续使用 `/0.1`，不得重算或改写；
- Relation request 必须复制完整 canonical Fact projection，并由 Provider 逐项复算 `fact_set_digest`；
- 单独传摘要后再从 ambient checkout 读取另一份 Facts 不成立；
- Relation `provider_run_id` 继续按冻结的 `provider-run/0.1` 公式，由新的 capability 与 operands digest 区分；
- 后继实现必须新增 exact identity vector、dispatch 与外部复算验证；在这些 bytes 存在前，不得声称首个合法
  Relation run 已经产生。

现有 ProviderRun shape 包含 parser identity。后继 closed Provider 必须报告其**真实使用**的 parser；若实现
不使用 parser，就必须先提出最小、版本化且可迁移的 Evidence 修正，不能虚填
`closed-deterministic-test-parser` 只为通过现有 shape。该诚实性要求是实现停止线，不是扩大本次 Schema 授权。

## 5. Relation terminal、provenance 与不可逆 eligibility

当前 `veritrail-review-derivation-cell/0.1` 是 Fact-only wire，固定空 relation IDs，不能改名冒充 Relation
terminal。后继实现只可增加独立 versioned relation request/terminal protocol，并继续满足 one request、
at-most-one terminal、exact echo、bounded read、stop 后 cleanup-only 与 no partial admission。

| 结果 | 必须保留 | candidate eligibility |
| --- | --- | --- |
| `COMPLETED` + canonical candidates | 真实 Relation run，包括成功空集合 | conformance 与 release 全成功后才可保留为 private history |
| `FAILED` / nonconformant | run-local typed diagnostic | 永久撤销，prefix 不保留 |
| `UNAVAILABLE` | 合法启动后的 run 与 unavailable diagnostic | 永久撤销 |
| deadline / cancel / memory stop | `INTERRUPTED` 与原 context cleanup | 永久撤销，不能刷新预算 |
| release / shared-context / identity failure | typed whole-attempt non-success | 永久撤销 |

每个 private Relation candidate 的 `provenance_refs` 必须恰好解析到真实报告它的 Relation run；该 run 的
run-local candidate ID 集也必须恰好等于它实际报告的排序唯一全集。application 只能复算 identity、字段、
Fact 引用与 canonical arrays，不能补 edge、换 target、选 winner 或回填 Fact provenance。

这些仍是 private phase history。只有后继 RelationSet admission 与完整 normal Bundle 同时成功，final Evidence
才可以投影 admitted Relation IDs。任一下游失败或 DIAGNOSTIC closure，final reported Fact / Relation IDs
继续清空；历史 terminal 本身不被改写。

## 6. 首版 upstream gate

首个 closed proof 只冻结保守、不可回填的启动资格：

| composed input | Relation start | 保留的事实 |
| --- | --- | --- |
| normal FactSet；全部 applicable Fact sources `COMPLETED`；无 FactConflict | 允许，包括合法空 FactSet | exact FactSet、source terminals 与 shared context |
| FactSet 含 FactConflict | 不启动 | 全部 candidates/conflicts；不选 winner |
| 任一 optional Fact source `FAILED/UNAVAILABLE` | 不启动 | FactSet 与 optional gap；不把成功前缀写成完整世界 |
| required source non-success、whole-attempt stop 或无 normal FactSet | 不启动 | 原 terminal/cleanup 与 no-FactSet 原因 |

“未启动”不是 Provider `UNAVAILABLE`，成功空集合也不是未启动。optional gap、FactConflict、RelationConflict、
import resolution 的 `UNRESOLVED/UNSUPPORTED/CONFLICT` 与 Coverage UNKNOWN 是不同维度，不能压成一个空数组、
布尔值或通用 confidence。

未来若要对 conflict-free component 或 optional-gap 已知前缀派生，必须另开 eligibility / UNKNOWN 合同并绑定
候选 universe；本首版 gate 既不授权该扩展，也不把保守停止写成永久禁止。

## 7. 候选证据与保留失败

文档 165 候选 PR #151 的 exact identity 为：

```text
base  41a398783d5eaf25e15574df5beafb8465d0a91e
head  8ccc1066d665d2b7e290f929c2c84f22645def01
merge 301f5248b77c67284b5e52bf287c23f286590e6b
tree  c82cb015516e817304e0ea8804dfc9375c9e1627
```

候选 head 的 Public CI run `34953748989` attempt 1 是 10/11：只有 `Wheel-only first run on Python
3.13` 失败。failed-jobs rerun 的 attempt 2 只新执行该失败 job；其组合 11/11 不能描述为十一项全部重跑。
随后同一 head 上一条全新的 Public CI run `34955710084` attempt 1 完成 11/11，才提供完整新鲜的候选门。

候选合入 `main@301f5248b77c67284b5e52bf287c23f286590e6b` 后：

- Public CI run `34957252663` attempt 1：11/11 `SUCCESS`；
- Browser Smoke run `34957252725` attempt 1：1/1 `SUCCESS`。

第一次红灯、部分 rerun 与后来的完整绿灯分别保留；后一个事实不重写前一个事实。

## 8. 候选 exact-main 匿名产品读回

候选 exact main 上对 README、文档 165 与 milestones 建立了三次互不复用的 fresh anonymous
installed-product session：

```text
README     github-paired-ce92921f28f94b1ab242bb963eebcf54
doc 165    github-paired-eda2a00a21ae4a1da5e5fecd4b0baebb
milestones github-paired-f893bb385ad744fdb923b83f25d77461
```

三次均为 HTTP 200、requested/final exact SHA path 一致、P1/P2 coverage `COMPLETE`、三样本稳定、marker
恰好一次、零 conflict/error/coverage reason/cleanup error、Core `PASS`。三份 canonical summary 的联合
SHA-256 为：

```text
b099b3b49b9092f915f684768807896ac4be616e4dd73f0cac9a326547d04b6c
```

该读回证明的是候选 exact commit 的公开 render、内容 marker 与 Core 校验闭包；它不证明某个 workflow
attempt 或 Artifact producer 身份，也不能替代本发布自己的合入后读回。

## 9. 后续维护合同对本冻结的复核

候选合入以后，Core 与 GitHub Evidence 分别增加了[获批源码状态连续性维护合同](168-approved-source-state-continuity-maintenance-contract.md)
和[GitHub Evidence 状态绑定权威维护合同](169-github-evidence-state-bound-authority-maintenance-contract.md)。本发布从
`main@8e5c0007c20b8c495195cdbdbb3a68891d88c3df` 重新核对二者：

- 文档 168 收紧后续受控执行的 run-start source identity 与 comparison eligibility，不回填 R1 候选历史，也不
  改写 R1 的 SourceSnapshot / FactSet / Relation authority；
- 文档 169 区分 PR payload、timeline merged event、Check Run、workflow run、attempt 与 Artifact producer。
  因此第 7 节的 attempt 事实按 attempt-specific jobs 读取，第 8 节不越权声称 workflow provenance；
- 从候选 exact main 到本发布基线，`plugins/review-attention` tree 与文档 165 均未变化；D0、Cu0、Core/P
  维护改动与两份维护合同也没有获得 R 轨的裁决权。

未发现推翻文档 165 选题、authority 分工、operand continuity、phase join 或 upstream gate 的新证据。这里的
“未发现”只支持本次冻结判断，不证明未来反例不存在。

## 10. 冻结后的有限实现授权

最后门全部成立后，下一分支只可从新的 exact main 串行物化以下 private closed proof：

1. relation-only `provider-operands/0.2` canonical projection、digest、dispatch 与 exact identity vector；
2. 新 sealed profile 的固定 phase classification，以及只消费 Fact-stage runs 的 private join；
3. independent relation-only request / terminal protocol 与 copy-owned FactSet operand；
4. 第 6 节保守 upstream gate，并证明 no-start、empty-success、unavailable 与 interrupted 不混同；
5. 持有原 live `BudgetContext` 的 integrated parent controller，FactSet-before-Relation、Relation-before-final；
6. 只服务首个封闭 fixture、真实消费 exact copied operands 的 deterministic candidate producer；
7. truthful parser/runtime/provider identity、candidate/run provenance、conformance 与 residue-free release；
8. `RD-001..017` 的单变量 negative / compatibility vectors。

该授权允许为上述闭环加入被证明必需的 private runtime 与最小版本化 identity/wire correction。若现有公共
Evidence shape 无法诚实表达 parser 或 phase identity，必须停下，先提交独立最小 Schema 合同；不能在实现中
静默改变已冻结 bytes。

## 11. 明确未授权

本冻结不授权：

- fixture-bounded proof 之外的完整 Relation algorithm，或真实 import zero/one/many resolution；
- RelationSet composition/admission、跨 Provider merge 或 RelationConflict；
- conflict-bearing FactSet / optional-gap 的局部派生资格；
- public Provider SPI、registry、安装扫描、真实 parser 产品化或 caller 自选 Provider；
- final COMPLETE / DIAGNOSTIC publisher、完整 Manifest 或 Artifact 发布；
- Slice、Coverage、Coverage UNKNOWN denominator、Attention Proposal；
- CLI、Workbench、D、Cu、Q 或跨系统产品化；
- 对历史 Artifact、`provider-operands/0.1`、既有 ProviderRun 或失败记录的重写。

## 12. 本发布门与最后停止线

本 docs-only publication 提交前必须通过 Markdown relative links、heading/fence、唯一状态 marker、敏感或本机
路径、exact diff scope、`git diff --check` 与绑定当前 worktree 的适用 focused regression。

当前 worktree 的第一次 Python 3.10 normal 尝试使用了主仓既有 `.venv`；它执行 110 项后在 test discovery
报告 2 个 `ModuleNotFoundError: jsonschema`，其余 108 项通过。该环境没有安装完整 schema-test 依赖，因此
这次尝试既不是 runtime assertion failure，也不具备 gate 资格。随后用明确绑定本 worktree `src` 与
`plugins/review-attention/src`、且依赖完整的系统解释器从头执行四个独立门：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | 162 tests / 323.031s / `OK` |
| CPython 3.10.6 `-O` | 162 tests / 312.168s / `OK` |
| CPython 3.13.13 normal | 162 tests / 313.396s / `OK` |
| CPython 3.13.13 `-O` | 162 tests / 310.383s / `OK` |

四个合格门均从当前 worktree 读取 Core 与 Review Attention 源码，串行执行以避免并发负载干扰 Windows
deadline、Job Object、terminal 与 cleanup 反例。它们证明现有冻结 runtime 回归保持成立，不证明本页尚未
实现的 Relation runtime。

之后仍须依次满足：

1. 本发布 PR head 的完整原始 required checks；
2. 受保护主线合入与不可移动 merge identity；
3. 新 exact main 上独立 Public CI 11/11 与 Browser Smoke 1/1；
4. README、本文与 milestones 三次新的 anonymous installed-product readback，覆盖 requested/final exact
   source、P1/P2 completeness、稳定样本、唯一 marker、零 conflict/error/cleanup error 与 Core PASS。

任一项未成立，就保留文档 165 的 `CONTRACT_CANDIDATE / IMPLEMENTATION_NOT_STARTED`。全部成立后，本页只
把合同状态发布为 `FROZEN` 并允许下一份独立 implementation candidate；它本身不证明任何 Relation runtime
已经存在。
