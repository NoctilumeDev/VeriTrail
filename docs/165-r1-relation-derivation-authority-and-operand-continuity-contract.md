# R1 Relation Derivation Authority / Operand Continuity 最小合同 0.1 候选

> 状态：`R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN /
> R1_RELATION_DERIVATION_PRECONTRACT_AUDITED /
> R1_RELATION_DERIVATION_CONTRACT_CANDIDATE /
> R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@41a398783d5eaf25e15574df5beafb8465d0a91e`
>
> 前置审计：[composition 冻结后下一闭环系统审计](164-r1-post-composition-next-closure-system-audit.md)
>
> 冻结输入：[确定性语义切片合同](113-r1-deterministic-semantic-slice-contract.md)、
> [Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [Execution Cell 合同](150-r1-derivation-execution-cell-terminal-envelope-contract.md)、
> [Fact/Evidence Closure 合同](155-r1-fact-admission-and-derivation-evidence-closure-contract.md)、
> [multi-Provider Fact 合同](160-r1-multi-provider-applicability-and-fact-composition-contract.md)与
> [composition 冻结发布](163-r1-multi-provider-fact-composition-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本候选只改变文档；不修改
> Schema、corpus、identity vector、源码、测试、依赖、CI、Provider、parser、publisher、Manifest、CLI、
> Workbench、Core、P/Q/D、tag 或 Release。

## 1. 目的与停止线

当前 private composition 可以在同一个共享 BudgetContext 中让多个 Fact Provider 终态、合并 Facts 并构造
copy-owned FactSet state。它不生产 Relation：Fact child 的 `reported_relation_ids=[]`，现有 Provider operands
投影也不绑定组合后的 `fact_set_digest`。完整 fixture 中的 Relation 与 ProviderRun 只能证明公共 shape 可表达
一个完整 Bundle，不能授权当前 Fact child 或 application 声称它已报告 Relation。

本合同候选只关闭下面的先后与权威接缝：

```text
newly sealed Policy + exact applicable bindings
  -> one admitted derivation and one live BudgetContext
  -> all Fact children terminal + exact composed FactSet
  -> conservative Relation input gate
  -> distinct bounded Relation capability / ProviderRun
  -> private relation candidate and terminal history
```

即使以后冻结，这一闭环最多允许 closed deterministic Relation execution proof 与 private、copy-owned、
non-published continuation。它不授予完整 Relation algorithm、import zero/one/many resolution、RelationSet
composition/admission、RelationConflict、Coverage UNKNOWN denominator、Slice、publisher 或完整 Derivation 的
施工权。当前 `veritrail-review-derivation-cell/0.1` 仍是 Fact-only；不得把它改名后声称可以运输 Relations。

## 2. 先复核审计的反证条件

本候选从本页所列 exact main 重新读了文档 113、120、150、155、160、163、164、公共 Schema、完整
fixture 与当前 private runtime。文档 164 第 4.1 节的五种失效条件均未得到新证据：

| 反证方向 | 本次实际核对 | 裁决 |
| --- | --- | --- |
| 冻结合同已唯一指定 composition 后的 Relation producer | 文档 120 冻结 shape/identity，文档 160 和 runtime 的 Fact children 只报告 Facts | 未找到唯一 producer |
| application 可纯机械派生且有独立诚实 provenance | Relation 要求非空 ProviderRun 引用；复制或回填 Fact run 会虚构其报告 | blocker 仍成立 |
| private proof 必须先取得 public Provider authorization | 文档 150/160 已区分 closed test 与 future public authorization | 未找到此强制前置 |
| conflict-bearing FactSet 必须先有独立 eligibility 合同 | 文档 160 只保留 conflict state，未唯一决定 Relation 启动/局部派生；本合同第 6 节采用首版保守 gate | 未证明可先独立闭环 |
| Relation 不再被后继消费 | 文档 113/120 的 Slice、Coverage 与 final Bundle 仍消费 RelationSet | 未找到绕过路径 |

这些是当前 source-of-truth 范围内的反查结果，不把“未找到”解释为未来模型不可改变。若后续 proof
击穿任一行，先沿文档 164 第 4.1 节修正审计、README、AGENTS、milestones 与本合同，再继续合同闭环。

## 3. 候选模型与 authority 分工

### 3.1 首个 closed proof 选择独立 Relation capability

本候选选择 **组合后的独立 Relation ProviderRun**，不让 Fact Provider 在首次 terminal 中报告最终 Relations，
也不让 application 凭可复算算法直接成为 Relation 事实来源。选择理由是：

1. Fact child 不拥有其他来源终态后的完整 module Fact universe；其第一次 terminal 不能最终证明
   `IMPORT_TARGET_LITERAL` 的 resolved target。
2. Relation 的 `provenance_refs` 必须解析到实际报告该 Relation 的 ProviderRun；application 不得回填早已
   terminal 的 Fact run，也不得提交空 provenance。
3. distinct capability 让同一实现可以有两次真实执行、两个不同 operand/time boundary，而不复用相同
   `(capability_id, provider_id)` identity。
4. replaceable Relation semantics 留在 bounded Provider；application 只执行 sealed applicability、copy-own、
   schema/identity conformance 和后继 admission，不硬编码可替换的 import/edge 算法。

首个 proof 使用一个新封存 Policy profile：Fact requirements 保持其原有 requiredness 与 `CUMULATIVE`
语义，另增加 exact `review-relation-derivation` requirement，`required=true`、
`composition_mode=CUMULATIVE`。这是**新请求封存的 Policy**，不是对既有 sealed Policy、文档 160 的首个
Fact-only private profile 或历史 Bundle 的修改。公共 Policy 0.1 schema 可表达另一个 capability requirement；
但当前 private composition entry 不接受此新 profile，不能直接复用它完成 Relation proof。新 profile 的
closed table 必须把 `python-ast`/`python-ast-advisory` 明确归为 Fact stage，把
`review-relation-derivation` 明确归为 Relation stage；phase classification 是合同固定值，不由
caller、ambient Provider 或 hash iteration 推断。Policy 仍一次封存全部 requirements 和预算。

文档 160 的首个 Fact-only profile 在**其全部 applicable runs** terminal-success 后才构造 private FactSet。
若新 profile 直接把 required Relation run 算进这次 join，就会形成循环：Relation 等 FactSet，FactSet 等
Relation。新 integrated parent 因此必须区分：

```text
fact_stage_status
  = 只汇合 sealed Fact-stage requirements，沿用文档 160 的 required/optional 规则
  -> COMPLETED 才可构造 copy-owned FactSet；这不是 final DerivationEvidence COMPLETED

relation_stage_status
  = distinct Relation requirement 的真实启动、terminal、cleanup 或 upstream hold

final_derivation_status
  = 两阶段都得到合法终态后才按 frozen overall priority 投影；
    upstream hold 不伪造 Relation run，也不冒充 COMPLETED
```

这是**候选版本化 phase-join 扩展**，不改变文档 160 的旧 Fact-only profile 或历史 overall status。
首次 Relation proof 前须独立验证 stage classification、FactSet-before-final-overall 的 private 身份与
final reported-ID 清空；当前代码和冻结 vector 尚未证明它。

Relation closed conformance table 必须在任何 Provider code 运行前固定并校验 exact descriptor、handle、
requiredness 与排序。首个表只允许：

```text
capability_id    = review-relation-derivation
provider_id      = closed-relation-provider-a
provider_version = 0.1-test
parser_id        = closed-deterministic-test-parser
parser_version   = 0.1-test
runtime_id       = veritrail-review-test-runtime
runtime_version  = 0.1-test
```

这里的 `parser_id` 必须是该 Relation Provider **实际使用**的 parser identity；若 proof 只读 FactSet 而没有
parser，就不能为满足现有 ProviderRun shape 虚填这个值，应重新评估最小 Evidence 字段/版本边界。
该 closed table 不是公共 SPI、registry、安装扫描或 caller 选 Provider 的授权。真实 parser/public Provider
须由独立后继合同审议。

### 3.2 四个 owner 不能混同

| owner | 本候选拥有的步骤 | 不拥有的步骤 |
| --- | --- | --- |
| Human Seal authority | 新 Policy 的 capability、requiredness、Profile 与预算 | run-local 事实或后处理回填 |
| Fact Provider / composition controller | 原有 Fact terminal、merge/conflict 与 exact FactSet construction | Relation candidate 或 Relation Provider 报告 |
| Relation Provider | 在 exact copied operand 上 bounded 生成自己的 Relation candidates、真实 terminal 与实现身份 | FactSet 改写、其他 Provider 的事实、publication |
| application canonicalizer | 验证 descriptor/operand echo、字段、引用、identity、run-local candidate/report 双向闭包 | 自造 Relation target、任选 conflict winner、把 candidate 当 final RelationSet |

后继 RelationSet admission、final Evidence projection、Slice 与 Coverage 各属于后续独立闭环；本合同只为它们
保留可验证的 private 输入历史，不提前执行这些步骤。

## 4. exact FactSet operand continuity

### 4.1 Relation Provider 的 owned 输入

composition controller 必须先 terminal 全部 admitted Fact children、完成 required/optional join、same-ID
merge、FactConflict construction、双向 provenance 与文档 120 的 `fact_set_digest` 复算。只有第 6 节 gate
允许后，Relation execution 才能启动。Relation request 的 copy-owned 语义输入固定为：

```text
exact SourceSnapshot / sealed Policy / DerivationProfile coordinates
exact analysis scope and original shared BudgetContext
composed FactSet semantic projection:
  source_snapshot_digest, analysis_scope_digest, derivation_profile_digest,
  facts and conflicts with provenance_refs removed
computed fact_set_digest over that exact projection
```

application 保留完整 FactSet 的 Policy、Fact provenance、Fact child terminal、optional gap 与 conflict state；
Relation Provider 不得重写它们。`fact_set_digest` 是冻结的**语义摘要**，不等于文件 SHA-256，也不声称
ProviderRun provenance 相同。Provider 用于生成 Relation 的 copied canonical Fact projection 必须逐项复算到
request 中的 `fact_set_digest`；单独传一个摘要、再从 ambient checkout 读取另一份 Facts 不成立。

### 4.2 旧 operands 公式不能冒充新绑定

文档 120 的 `veritrail.review.provider-operands/0.1` 投影只有 Snapshot、Policy、scope、Slice Policy、
Profile 与 descriptor；FactSet 交换而其他坐标相同时，它仍相同。因此本候选提出 **relation-only** 的
版本化投影，供下一合同/identity correction 精确审议：

```text
domain  = veritrail.review.provider-operands/0.2  [候选，尚未冻结]
payload = frozen provider-operands/0.1 payload + {fact_set_digest}
```

所有原有 Fact runs 继续使用 `/0.1`；不能修改历史 operands digest、ProviderRun 或冻结 vector。Relation
run 的 `provider_run_id` 仍由 frozen `veritrail.review.provider-run/0.1` 的
`{derivation_id, capability_id, provider_id, operands_digest}` 公式计算。新 capability 与新 operands digest
共同区分两段运行；时间和 terminal 边界仍须真实记录，不允许隐藏 resume 或共用一个 run ID。

公共 Evidence 0.1.1 的字段形状能存 `operands_digest`、distinct ProviderRuns 与
`reported_relation_ids`；RelationSet 0.1 能存 `fact_set_digest` 与独立 run provenance。然而形状本身不
升级文档 120 已冻结的通用 `/0.1` 投影或 verifier/corpus。首次合法 Relation run 以前，必须通过一个
只针对 relation-only projection、dispatch 与 identity vector 的版本化合同/校验修正证明外部可复算。
若 exact capability dispatch 无法在 0.1.1 Evidence 下无歧义表达，再只增加被证明必需的最小
Evidence 字段/版本；本候选不预先改 Schema payload 或重算旧 bytes。

### 4.3 一个 live context，不能在 Fact result 返回后重启

Relation child 与全部 Fact children 必须属于同一个 derivation、同一个 absolute monotonic deadline 和
BudgetContext。当前 Fact composition entry 返回的是终态 private result，不能从另一个 standalone 调用
重建“同一次”共享预算。未来 closed proof 必须由一个 integrated parent controller 在 Fact terminal 后、
Relation start 前仍真实持有 original live context，并复验剩余 deadline、memory、artifact permission 与
residue-free release。该 parent 只在 Fact-stage join `COMPLETED` 后形成 private FactSet，不在 Relation
终态前形成 final `DerivationEvidence.overall_execution_status=COMPLETED`。Relation 不刷新预算，不并行
运行，也不能复用 Fact cell 的 Fact-only wire terminal。

## 5. Relation run、candidate 与 provenance

首个 relation-only execution 必须有独立的 versioned request/terminal protocol。它沿用文档 150 的
one-request/at-most-one-terminal、exact echo、bounded read、cleanup-only after stop、no partial candidate
admission 原则，但当前 `veritrail-review-derivation-cell/0.1` 的 `canonical_facts` 和固定空 relation IDs
不是 Relation terminal shape。本合同候选只固定语义 terminal，尚不授权改 Fact wire bytes。

| terminal | private phase history | normal candidate eligibility |
| --- | --- | --- |
| `COMPLETED` + canonical candidates | one truthful Relation run；包括成功空集合 | 仅在全部 conformance 与 release 成功后保留 |
| `FAILED` / nonconformant output | run-local typed diagnostic；不得保留 prefix candidates | 撤销 |
| `UNAVAILABLE` | 合法开始后的 run 与 unavailable diagnostic；不伪造未启动 run | 撤销 |
| deadline/cancel/memory stop | `INTERRUPTED`，原 context cleanup-only；不发布 prefix | 永久撤销 |
| release/shared-context/identity failure | typed whole-attempt non-success；不能任选无责 Fact run 背书 | 永久撤销 |

Relation Provider 返回的 candidate identity 与其真实 run ID 先在 private state 中双向闭合：每个 candidate
的 `provenance_refs` 恰为该 run，run-local candidate ID 集恰为该 run 真正报告的排序唯一全集。
application 复算 frozen `relation_subject_digest/relation_id`、Fact 引用、target 字段与 canonical arrays；
不得通过修改 target、补 edge、挑 conflict winner 或回填 Fact run 使输出“通过”。一个 relation run 内的
同 subject 不兼容 candidate 是 nonconformant output；跨 relation runs 的 merge/RelationConflict 尚未授权。

这些是 **private phase IDs**，不是可发布 DerivationEvidence 的 final `reported_relation_ids`。只有后继
RelationSet admission 与完整 normal Bundle 同时成功，final Evidence 才可把被 admission 的 Relation IDs
投影到该 Relation run，并检查 Relation/run 双向 provenance。任一下游失败或 DIAGNOSTIC closure，全部
final reported Fact/Relation IDs 仍按文档 155/160 清空；历史 `COMPLETED` run status 不被改写。

## 6. 首版 upstream gate 与未知状态

第一个 closed execution proof 使用保守、不可回填的 gate。这只决定本 proof 能否**开始** Relation run，
不声称冻结所有未来 Relation conflict-isolation 或 Coverage 算法：

| composed input | 首版 Relation start | 必须保留的 private truth |
| --- | --- | --- |
| normal FactSet；所有 applicable Fact sources `COMPLETED`；无 FactConflict | 允许，包括合法空 FactSet | exact FactSet 与 source terminal 全集 |
| FactSet 有 FactConflict | 不启动 | 全部 Fact candidates/conflicts；不选 winner，不写 `relations=[]` 为 known empty |
| 任一 optional Fact source `FAILED/UNAVAILABLE` | 不启动 | 已构造 FactSet 与 optional gap；不得把成功前缀改为全局 KNOWN |
| required source non-success、whole-attempt stop 或无 normal FactSet | 不启动 | 原 terminal/cleanup 与 no-FactSet 原因；不构造较小 normal Relation world |

optional gap 与 FactConflict 即使同时存在也分别保留，不压成一个 `has_conflict`。没有 start 的状态不是
Relation Provider `UNAVAILABLE`，不得伪造 ProviderRun、Relation failure diagnostic、empty-success 或
RelationSet，也不得把未执行的 required Relation stage 投影成 final `COMPLETED` Evidence。它只是一份
private upstream-hold construction history；未来 DIAGNOSTIC/public disposition 须由独立合同授权。
未来若证明对 conflict-free component 或 optional-gap 已知前缀可以安全派生，必须另开
conflict/UNKNOWN 资格合同，显式绑定 candidate universe；不能从本首版 gate 的保守停止推导永久禁止。

首版 run 成功空 candidate 时，必须实际 terminal 并 release，且与“不启动”、`UNAVAILABLE`、失败和
upstream UNKNOWN 不同。`IMPORT_TARGET_LITERAL` 的 `UNRESOLVED/UNSUPPORTED/CONFLICT`、
RelationConflict、FactConflict 与 Coverage denominator 又是不同维度；本合同不使用一个空数组或 boolean
代替其 typed history。完整 import zero/one/many 与 Relation admission 留在后继合同。

## 7. 最小反例与后继证明义务

| ID | 单变量反例 | 本候选必须拒绝的推理 |
| --- | --- | --- |
| `RD-001` | Fact Provider A terminal 后，B 才提交 target MODULE Fact | A 已能最终解析 import |
| `RD-002` | 交换 composed FactSet，其他 Provider operands 相同 | 旧 `/0.1` digest 已证明同一 Relation 输入 |
| `RD-003` | application 生成 Relation，再回填 A 的 reported IDs | A 实际报告该 Relation |
| `RD-004` | application 生成 Relation，provenance 为空 | deterministic 可替代来源 |
| `RD-005` | 同 capability/provider 两次运行使用同 run ID | 同一实现就是同一 terminal |
| `RD-006` | Policy 无 Relation requirement，caller 临时传 descriptor | ambient callable 等于 sealed authority |
| `RD-007` | FactConflict 存在，Relation 任选一个 candidate | 建图可以顺便裁决 Fact 冲突 |
| `RD-008` | optional Fact source 不可用，另一来源成功 | 已知前缀等于完整候选全集 |
| `RD-009` | required source 失败，另一来源成功 | 可以创建较小 normal FactSet/RelationSet |
| `RD-010` | 成功空 Relation run 与 Relation run 未启动 | 两者都只有 `relations=[]`，所以相同 |
| `RD-011` | Relation deadline 命中并留有 prefix candidate | prefix 可 normal admission 或刷新预算 |
| `RD-012` | Relation candidate provenance 指向 Fact run | Schema 接受引用就证明该 run 报告 Relation |
| `RD-013` | relation-only `/0.2` proposal 还未版本化验证 | Evidence 0.1.1 有 string 字段就已经冻结新公式 |
| `RD-014` | 同一 import 有两个 module target | 任选排序首项或将 target conflict 当 RelationConflict |
| `RD-015` | Relation phase 成功、下游 admission 失败 | final Evidence 仍可保留非空 reported IDs |
| `RD-016` | 在 Fact composition 返回后另开 Relation 调用 | 两次独立预算可声称为同一 context |
| `RD-017` | required Relation requirement 计入 Fact-stage overall join | FactSet 可等所有 runs 完成，而 Relation 同时等 FactSet |

`RD-014` 只锁定不得丢失分歧，**不**把完整 import resolution 算法收入本合同。
后继独立 proof 还须决定：Relation candidate 的 closed algorithm 与 exact source bytes；relation-only
request/terminal wire bytes；`provider-operands/0.2` identity dispatch 与 vector；RelationSet run-local
admission、跨来源 merge/RelationConflict；optional gap 与 conflict-bearing FactSet 的扩展资格；final Evidence、
Coverage UNKNOWN 与完整 publisher。stage-scoped join 与 final overall 的 versioned extension 也须先以
`RD-017` 的单变量 vector 证明，不能复用旧 Fact-only all-runs join。只有某项被证明与本
authority/operand 闭环不可分，才最小重开本合同。

## 8. 候选事实、本地门与最后停止线

本候选基线是 PR #150 合入后的 exact main。PR head 的原始 11 项 Public CI check 均成功；合入后 Public CI
run `34930110622` attempt 1 保留为 10/11 `FAILURE`，E3 Release asset 六次 HTTP 500 后按 60 秒预算停止。
failed-jobs rerun 的 attempt 2 组合结果是 11/11 `SUCCESS`：只有 E3 在第二次窗口重新执行并成功，其余十项
继承首次成功事实。Browser Smoke run `34930110603` attempt 1 为 1/1 `SUCCESS`。README、文档 164、
milestones 的三次新匿名 installed-product P1→P2→P3→Core 读回均为 PASS，三份 canonical summary 的
联合 SHA-256 为 `9fd68f63fc6ce3ea60f1d3aea014b8c61018b8f9adadd9637ad9bc79cbed08bf`。
这些事实只解除**起草**本合同的入口，不是本合同自己的冻结门。

本 docs-only 候选提交前必须通过 Markdown relative links、fence/heading、状态 marker、敏感/本机路径、
exact diff scope、`git diff --check` 与绑定当前 worktree 的适用 focused regression。即使本地、原始
remote checks、受保护合入、新 exact-main Public CI/Browser Smoke 与本候选专属 fresh anonymous
installed-product readback 后续全部成立，候选也只达到待独立冻结发布的合同事实；不得在本分支直接
实现 Relation runtime、Schema correction 或完整 RelationSet。

当前分支只能写：

```text
R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN
R1_RELATION_DERIVATION_PRECONTRACT_AUDITED
R1_RELATION_DERIVATION_CONTRACT_CANDIDATE
R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

若本候选的 `/0.2` operand proposal、parser identity 或 Relation terminal shape 在 review 中不能同时保持
truthful provenance 与最小性，先收窄/修正合同；不能为通过现有 vector 回填 Fact Provider 报告、偷改
冻结 Schema bytes 或让薄 application 获得事实生产权。
