# R1 Fact / Parse Observation Fulfillment / Coverage Prerequisite 系统审计

> 状态（候选）：`R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_FACT_PARSE_OBSERVATION_FULFILLMENT_COVERAGE_PREREQUISITE_AUDIT_CANDIDATE /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@0b2df206756bd07ddd5075fa1bd9b63b656a16dc`
>
> 上游审计：[Post-Slice-Input Closure / Slice-Coverage Qualification 系统审计](192-r1-post-slice-input-closure-slice-coverage-qualification-system-audit.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本文只审计七阶段
> Coverage 的前置事实资格，不创建或修改 Schema、corpus、identity vector、runtime、测试、Provider、
> parser、FactSet、RelationSet、ReviewSliceSet、CoverageLedger、Evidence、Manifest、publisher、Bundle、
> Attention、CLI、Workbench、Core、P/Q/D/Cu/O/T、依赖、CI、tag 或 Release

## 1. 审计问题与停止线

文档 192 已经用真实反例识别出三项后继资格：

```text
private Slice obligation closure / typed negative receipt
    -> ReviewSliceSet semantic projection eligibility
    -> seven-stage Coverage composition qualification
    -> explicit public closure binding
```

但“需要一个七阶段 Coverage qualification”不等于“七个阶段所需的权威履责历史已经存在”。起草下一份
public-boundary 合同以前，必须先回答：

> 当前 exact owned history 是否真的足以机械重建文档 120 冻结的全部七个 Coverage stages，尤其是
> `LANGUAGE_SUPPORT / PARSE / FACT_DERIVATION` 的 denominator 与逐项 terminal disposition？

如果答案是否定的，就不能通过读取现有 FactSet、相信 `ProviderRun = COMPLETED`、重跑一个未获授权的 parser，
或给缺失事实填入看起来保守的 `UNKNOWN` 来继续 public contract。本文只定位这一前置条件，不选择实现。

## 2. 七阶段当前真实资格

| Stage | 当前 exact source | 当前能证明的上限 | 缺失事实 |
| --- | --- | --- | --- |
| `SNAPSHOT_INVENTORY` | exact SourceSnapshot inventory | denominator 可从已验证 exact analysis tree 复算 | 后继仍须机械生成 partition，不能接受 caller stages |
| `POLICY_SCOPE` | exact Policy `scope_decisions` 与 Snapshot inventory 一一闭合 | denominator 与 in/out-of-scope 可复算 | 无 |
| `LANGUAGE_SUPPORT` | exact Policy、Profile、inventory 与 blob bytes | Policy `IN_SCOPE` denominator 与 entry kind/path 的结构条件可复算 | 每项 source language / encoding support 的 terminal classification 未保存 |
| `PARSE` | Profile 声明支持的 parse units | denominator 形状可枚举 | 没有 real Fact parser，也没有每个 parse unit 的 terminal outcome |
| `FACT_DERIVATION` | Provider candidate reports 与 admitted FactSet | 已报告 Fact 的 canonical identity、provenance 与跨 Provider composition 成立 | 没有 Fact observation domain / per-item outcome，不能证明未报告 subject 被观察 |
| `RELATION_DERIVATION` | declared Relation ObservationDomain、ObservationOutcome 与 qualification | 对 exact admitted FactSet 的 Relation responsibility closure 成立 | 不能反向修复 FactSet 上游 completeness |
| `SLICE_DERIVATION` | exact anchor/spec domain、assignment、outcome 与 private terminal closure/receipt | 对 exact admitted graph 的 Slice obligation fulfillment 成立 | 尚无 public projection/qualification/binding |

因此当前不是“最后两个 public JSON 尚未生成”。当前事实是：

```text
Slice obligation fulfillment exists
Relation observation fulfillment exists for the admitted FactSet
Fact membership/provenance closure exists

but

Fact membership/provenance closure
    != Fact observation-domain closure
    != Parse-unit fulfillment
    != authoritative FACT/PARSE Coverage
```

## 3. 冻结合同已经留下的边界

文档 137 第 8.2 节已经明确：application 只负责 candidate conformance 与 canonical identity，不是第二个事实
观察者。第 8.3 节又明确首切片不实现真实 parser，并把以下问题留给后继合同：

```text
parse failure / unsupported entry 怎样成为后继 Coverage 输入
accepted encoding 怎样与 raw byte anchor 共存
parser diagnostics 怎样保持 typed 且不泄露源码
一个 file 的部分 AST 是否有资格产生 canonical Fact
```

文档 155/160 随后只关闭了：

```text
Provider reported candidates
    -> application canonical Fact identity
    -> FactSet membership / conflict / provenance reconciliation
```

其中 `completed empty source` 是“该 Provider 报告了空集合”的真实来源事实；它没有额外证明 Provider 已对
所有 parse units、所有 AST nodes 或所有 Fact subjects 履行穷尽观察。文档 175 之所以为 Relation 新增
ObservationDomain 与逐项 ObservationOutcome，正是因为：

```text
ProviderRun COMPLETED
    != observation responsibility fulfilled
```

这条纪律不能在 Coverage 前又对 Fact 阶段失效。

## 4. exact-main 实际反例

### 4.1 `FPQ-000`：四个 candidate parse-unit paths、两个 COMPLETED runs、一个 Fact

审计在仓库外临时进程中只读复用 current `test_multi_provider_fact_composition` fixture、正式 input binding、
closed applicability table 与真实 multi-Provider composition entry；没有修改源码、测试、fixture 或 Artifact。

同一 exact Snapshot / Policy / Profile 下，application 按当前 request validator 的 entry-kind 与 `.py` raw-path
后缀规则，把四个 path 放进 `supported_paths`。这里的名字是现有 private request 字段；它不证明编码、语法或
真实 parse 已经完成。四个 candidate parse-unit paths 是：

```text
pkg/nested/mod.py
pkg/regular.py
pkg/run.py
pkg/<raw-byte-name>.py
```

实际运行结果为：

```text
snapshot_inventory_count          = 7
request_supported_paths_count     = 4
required ProviderRun statuses  = [COMPLETED, COMPLETED]
overall_execution_status       = COMPLETED
FactSet constructed            = true
normal continuation permitted  = true
reported Fact count            = 1
reported Fact paths            = [pkg/nested/mod.py]
```

Python 3.10.6 与 3.13.13 的 normal / `-O` 四次独立只读复算生成逐字节相同的上述 canonical report；报告不含
wall-clock 或临时目录坐标。

这不是当前 runtime bug。两个 closed Provider 的冻结用途本来就是证明替换、预算、terminal、identity、
composition 与 provenance 机制；它们不是 Python 3.10 parser。当前 Provider implementation 明确只选择排序后的
首个 supported path 并报告一个 `MODULE` candidate。

该世界却足以反证以下推导：

```text
all required ProviderRuns COMPLETED
    -> all supported parse units were parsed
    -> all Fact candidates were observed
    -> FACT_DERIVATION denominator is KNOWN
```

现有 FactSet 能诚实证明“哪些 candidates 被报告、接纳并形成 provenance”，不能证明“哪些应报告 candidates
不存在”。因此把 FactSet 的 `subject_key_digest` 集合直接复制成 Fact denominator，会让 producer output
自己定义考试范围。

### 4.2 反例身份

`FPQ-000` 是 contract/prerequisite falsifier，不是产品失败或正式 Evidence readback。它使用已授权 private
conformance lab，暴露的是现有 authority 上限：

```text
candidate set closed under reported IDs
    != candidate universe observed
```

它不推翻已经成立的 Fact identity、multi-Provider provenance、Relation qualification、RelationSet admission 或
Slice A–H private closure。那些结论都继续对各自的 exact admitted inputs 成立；它只禁止把这些局部闭环扩大为
全源码 Fact/Parse Coverage。

## 5. 对文档 192 结论的精确修正

文档 192 识别出的 public seam 仍然真实：ReviewSliceSet admission、Coverage qualification 与 public closure
binding 都缺失。需要修正的是施工顺序，而不是删除该 seam。

文档 192 第 4.2 节要求：

> Coverage application 必须从同一 exact owned history 机械建立七个 stages。

当前审计证明，这项要求的前提尚未成立：exact owned history 没有 `PARSE / FACT_DERIVATION` 的逐项履责
记录。于是：

```text
public Slice/Coverage seam identified
    != full seven-stage input history available
    != public qualification contract ready to freeze
```

不得用以下任一种方式越过：

- 把 `ProviderRun = COMPLETED` 升格为 parse/fact observation closure；
- 把 FactSet members 当作 FACT denominator 的所有成员；
- 让 Coverage assembler 自己运行一个未封存的 parser 后补写历史；
- 用 Relation/Slice 的后继成功反向证明 Fact 阶段完整；
- 把无法解释的缺口塞入不匹配的 `DERIVATION_ERROR` 或 `UPSTREAM_DENOMINATOR_UNKNOWN`；
- 只实现 `SLICE_DERIVATION`，再用七阶段 Schema 的其他空数组冒充完整 Ledger。

## 6. 新的最小 blocking seam

真正需要先审计和冻结的是：

```text
Fact / Parse Observation Domain
and Fulfillment Qualification
```

它至少必须回答：

1. **parse-unit domain**：exact Snapshot、Policy 与 Profile 如何机械定义本次必须观察的 parse units？
2. **parser authority**：哪个 fixed/versioned parser 有资格形成 parse outcome，真实 parser 怎样进入 public
   Evidence，而不把 private test descriptor 改名对外？
3. **per-unit outcome**：每个 parse unit 怎样留下 `PARSED / UNSUPPORTED / PARSE_FAILED / EXECUTION_FAILED`
   等与现有 Coverage 闭集一致的 terminal receipt？
4. **Fact responsibility**：成功 AST 中哪些 Fact subjects 构成不可缩小的 observation domain，谁负责枚举？
5. **fulfillment proof**：没有 candidate 时，怎样区分 closed negative 与漏观察？
6. **multi-Provider responsibility**：同一 capability 的多个 applicable Provider 是重复观察、分片责任还是不同
   语义来源；requiredness 怎样传播？
7. **same-attempt continuity**：parse/fact outcomes 怎样继续使用原始 exact inputs、BudgetContext 与 attempt
   authority，不在 Coverage 阶段重开一轮观察？
8. **Coverage handoff**：哪个 application-owned receipt 只证明 parse/fact responsibility closure，并把 exact
   denominator/terminal partitions交给后继 Coverage qualification，而不拥有 public Verdict？

这八项没有答案时，不应先决定 ObservationOutcome Schema、Evidence carrier、public Provider registry 或真实
parser 实现。

## 7. 后继资格否定矩阵

| ID | 单变量世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `FPQ-000` | 四个 request-supported candidate parse-unit paths；required runs 全 COMPLETED；只报告一个 path 的 Fact | Provider completion 证明 parse/fact domain closure |
| `FPQ-001` | non-empty parse domain；没有逐项 parse outcome | `PARSE` stage 可以是 COMPLETE |
| `FPQ-002` | Fact candidates 只覆盖部分成功 AST；reported-ID 双向闭合 | FactSet membership closure 证明 FACT denominator complete |
| `FPQ-003` | Provider 返回空 candidate；domain 非空；无 negative receipt | empty report 证明没有 Fact |
| `FPQ-004` | Coverage assembler 观察结果后另启 parser 重建 denominator | post-hoc second observation 继承原 attempt authority |
| `FPQ-005` | Relation/Slice 对 admitted FactSet 均 qualified | downstream closure 修复 upstream Fact omission |
| `FPQ-006` | caller 给出正确 parse/fact denominator digest | digest knowledge 等于 observation authority |
| `FPQ-007` | public Ledger 使用 UNKNOWN，但没有合法 typed cause/receipt | conservative label 补足缺失历史 |

本文只实际构造 `FPQ-000`；`FPQ-001..007` 是后继 precontract/contract 必须逐项裁决的反例，不冒充已运行
测试。

## 8. 当前允许与禁止

本文候选成立时，只允许发布以下窄结论：

```text
post-Slice public qualification seam remains real
full seven-stage Coverage contract has an unmet Fact/Parse prerequisite
next contract selection must return to Fact/Parse observation fulfillment
```

仍然禁止：

```text
ReviewSliceSet / CoverageLedger public runtime
full Slice/Coverage composition qualification contract
real Fact parser implementation
Fact/Parse ObservationOutcome implementation
Schema / corpus / identity-vector changes
Evidence / Manifest version changes
publisher / output root / public Bundle
Attention / CLI / Workbench
```

单独的 semantic ReviewSliceSet projection虽可从 private closure 复算，但当前不预选为绕行施工：它不能形成
COMPLETE Bundle，也不能解决 public witness 与 Coverage binding。若未来要拆出该支线，必须另做价值与停止线
审计，不能把“可计算”写成“应当先实现”。

## 9. 下一步顺序

```text
本审计候选自己的门 / merge / exact-main qualification
    -> Fact/Parse observation fulfillment precontract audit
    -> minimal contract candidate
    -> contract freeze
    -> private proof
    -> post-prerequisite system audit
    -> re-evaluate ReviewSliceSet / seven-stage Coverage qualification
```

任何一步都不自动授权下一步。尤其本审计不把文档 137 的 real-parser 未决问题改写成已解决，也不把后继
Fact/Parse 合同预先限定成 Relation ObservationDomain 的字段复制版。

## 10. 候选闭环门

本审计候选只有在以下条件全部成立后，才有资格发布为当前 system-audit fact：

1. `FPQ-000` 的 source/input/run/fact 数量可由 current exact main 独立复算；
2. 文档 120/137/155/160/175/189/192 的 authority 边界没有被重解释；
3. README、AGENTS 与 milestones 同步表达“public seam 仍在，但 full Coverage contract 前置条件不足”；
4. diff 只包含本文与三处状态/导航同步；
5. Markdown 链接、状态 token、敏感路径、`git diff --check` 与 docs scope gate 成立；
6. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
7. 新 exact main Public CI 与 Browser Smoke 成立；
8. 后继独立状态发布若被当前流程要求，必须使用新的 source state 与独立证据，不得让本候选自封冻结。

在第 6–7 项完成以前，当前公开状态仍是文档 192/193 与 PR #201/#202 已资格化的
`...PRECONTRACT_AUDITED / CONTRACT_NOT_STARTED`；本文只是候选，不改写历史状态。
