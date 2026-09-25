# R1 Language Support / Parse / Fact Fulfillment 问题边界审计

> 状态（候选）：`R1_FACT_PARSE_OBSERVATION_FULFILLMENT_COVERAGE_PREREQUISITE_AUDIT_CANDIDATE /
> R1_LANGUAGE_PARSE_FACT_FULFILLMENT_PROBLEM_BOUNDARY_AUDIT_CANDIDATE /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@a07266661ec66e79b3658c32da69e79494d8ae0e`
>
> 上游审计：[Fact / Parse Observation Fulfillment / Coverage Prerequisite 系统审计](194-r1-fact-parse-observation-fulfillment-coverage-prerequisite-system-audit.md)
>
> 影响层级：`L3_SYSTEM_AUDIT + L2_CONTRACT_PROBLEM_BOUNDARY + L0_DOCUMENTATION`；本文只判断
> `LANGUAGE_SUPPORT / PARSE / FACT_DERIVATION` 的缺口是否属于同一种责任语义，不选择合同、Schema、
> Provider、parser、AST carrier、ObservationOutcome、receipt、Ledger、runtime、publisher 或 public Artifact

## 1. 审计问题与停止线

文档 194 已经证明：current Fact composition history 不足以授权完整七阶段 Coverage。下一步不能因为三个
stage 都缺 fulfillment evidence，就先发明一个通用 `ObservationObligation / ObservationReceipt /
FulfillmentLedger`。本文只问：

```text
LANGUAGE_SUPPORT 缺的是什么？
PARSE 缺的是什么？
FACT_DERIVATION 缺的是什么？

它们的 denominator 何时可知？
谁有资格形成 terminal fact？
后继 application 能验证什么，而不会重做观察？
```

若三者的 domain source、形成时刻或 authority owner 不同，就必须保持分层；共享 attempt identity、terminal
outcome 或 reconciliation shape，不足以证明它们应共享一个 primitive。

## 2. 冻结 Coverage 已经规定了三个不同 denominator

文档 120 冻结的 denominator source 是：

| Stage | Denominator source | 何时可以知道 |
| --- | --- | --- |
| `LANGUAGE_SUPPORT` | Policy 的全部 `IN_SCOPE` inventory entries | exact Snapshot + Policy 已知后即可枚举 |
| `PARSE` | 当前 Profile 真正支持的 parse units | 每项 language / entry-kind / encoding support 得到合法分类后 |
| `FACT_DERIVATION` | 成功解析 AST 中按 Profile 闭集可枚举的 Fact candidates | exact parse result 已经成立后 |

因此三者从一开始就不是同一张静态清单：

```text
IN_SCOPE inventory entries
    -> language/support classification
    -> supported parse units
    -> parse terminal outcomes
    -> successful exact AST results
    -> profile-governed Fact candidate enumeration
```

当前 private request validator 的 `supported_paths` 只检查 Profile `supported_entry_kinds` 与 raw path 的 ASCII
`.py` 后缀。它不读取 Python coding declaration，不验证 accepted encoding，不执行 Python 3.10 parse，也不
枚举 AST Fact candidates。该字段只能描述 current test-provider request 的结构候选，不是
`LANGUAGE_SUPPORT` 或 `PARSE` Coverage outcome。

## 3. 当前 carrier 能证明什么

`OwnedExecutionCellPhaseResult` 当前保存：

```text
exact input digests
Provider descriptor / operands / run identity
ProviderRun and phase terminal status
diagnostic_code
canonical Fact bytes
reported Fact / Relation IDs
release outcome
```

multi-Provider composition 随后验证 reported candidates、canonical identity、FactSet membership、conflict 与
provenance。它没有保存：

```text
per-IN_SCOPE-entry language/support classification
per-supported-parse-unit parse terminal outcome
exact parse-result / AST identity
Fact projection responsibility domain
per-unit Fact enumeration closure
```

这与既有冻结合同一致。closed Provider 是 mechanism-test Provider，不是真实 Python parser；缺少上述字段不是
当前 runtime defect。

## 4. 三个独立反例

审计在仓库外临时目录中只读复用 current SourceSnapshot、Derivation Input、closed applicability table 与真实
multi-Provider composition entry。审计 oracle 只用于证明夹具世界：accepted encoding 使用 exact bytes 解码；
syntax/AST 使用 `ast.parse(..., feature_version=(3, 10))`；它不进入产品 runtime，也不取得 Provider 或 Coverage
authority。

Python 3.10.6 与 3.13.13 的 normal / `-O` 四次独立运行产生逐字节相同的 canonical report。

首次并发四格复跑时，仓库外审计脚本直到三个 world 全部运行完才回头读取第一个 world 的 live
`normal_continuation_permitted()`；host contention 使三份首 world projection 越过 10 秒 budget，而另一份尚未
越过，因而没有形成一致报告。该尝试是 audit-harness observation-timing failure，不是合格反例结果。脚本随后
只把每个 world 的 projection 移到其自身运行结束点，没有修改仓库或产品预算；并发四格重新得到逐字节相同
报告。原不一致尝试不计作 PASS，也不解释为 runtime defect。

### 4.1 `LPF-000`：request candidate 不等于 language-supported

单变量只把 `pkg/regular.py` 的 blob 改为不能按 `UTF-8` 或 `UTF-8-SIG` 解码的 bytes；entry kind 与 `.py`
raw-path 后缀保持满足 current request validator。另一个排序更早的合法 path 仍供 closed Provider 产生其既有
`MODULE` Fact。

结果：

```text
independent Profile encoding check = REJECTED
required ProviderRun statuses       = [COMPLETED, COMPLETED]
Provider diagnostics                = [0, 0]
overall execution                   = COMPLETED
normal continuation                 = true
reported Fact kinds                 = [MODULE]
```

该世界证明：

```text
path entered current supported_paths
    != accepted source encoding established
    != LANGUAGE_SUPPORT terminal classification exists
```

它不证明 current Provider 错误读取了该 blob；恰恰相反，现有 history 无法说明这个 entry 是否被 support
classifier 观察。

### 4.2 `LPF-001`：language-supported 不等于 parse outcome exists

单变量只把 `pkg/regular.py` 改为合法 UTF-8、但在 Python 3.10 grammar 下必然 `SyntaxError` 的 bytes；其他条件
与 `LPF-000` 相同。

结果：

```text
independent Python 3.10 parse       = FAILED
required ProviderRun statuses       = [COMPLETED, COMPLETED]
Provider diagnostics                = [0, 0]
overall execution                   = COMPLETED
normal continuation                 = true
reported Fact kinds                 = [MODULE]
```

该世界证明：

```text
encoding accepted + request candidate enumerated
    != parse attempted
    != parse terminal outcome retained
```

即使未来 `LANGUAGE_SUPPORT` 已闭合，`PARSE` 仍须拥有自己的 execution-derived terminal fact；不能从前一阶段
或 whole-run `COMPLETED` 推导。

### 4.3 `LPF-002`：parseable AST 不等于 Fact projection fulfilled

单变量只把排序最早、实际承载 reported `MODULE` 的 `pkg/nested/mod.py` 变为合法 Python 3.10 source：

```python
import os
class A:
    def m(self):
        pass
def f():
    pass
```

按文档 120 的冻结 Fact kind 与 direct-body 规则，该 exact AST 中可枚举：

```text
MODULE
IMPORT_DECLARATION
CLASS_DECLARATION
METHOD_DECLARATION
FUNCTION_DECLARATION
```

current closed Provider 对同一个 path 仍只报告 `MODULE`；两个 required runs 继续 `COMPLETED`，diagnostics 为空，
FactSet 与 normal continuation 成立。

该世界证明：

```text
parse result can be successful
    != all profile-governed Fact candidates were enumerated
    != FACT_DERIVATION denominator is authoritative
```

这不是要求 current test Provider 立刻实现真实 parser。它只证明：即使 Parse receipt 将来存在，Fact projection
fulfillment 仍是一项独立义务。

## 5. 三者不能先压成一个 domain primitive

反例支持的最小分层是：

### 5.1 Language-support classification

- responsibility domain 在执行前可由 exact `IN_SCOPE` inventory 枚举；
- terminal fact 是每项是否满足 language、entry-kind、path 与 source-encoding support；
- 它不能由名为 `supported_paths` 的未执行结构筛选字段代替；
- 谁拥有 classification algorithm、coding-declaration 语义和 typed reasons，仍待后继选择。

### 5.2 Parse fulfillment

- responsibility domain 依赖合法 language-support terminal outcomes；
- item identity 仍是 exact path-backed parse unit；
- terminal fact 来自 fixed/versioned parser 的真实执行；
- success、unsupported syntax、parse failure、provider unavailable 与 execution failure 必须保留区别；
- parse outcome 必须绑定 exact blob bytes、Profile semantics、parser identity 与 attempt。

### 5.3 Fact projection fulfillment

- denominator 不能仅从 path domain 预先枚举；它依赖成功 parse result 中的 exact AST structure；
- application 当前没有 AST carrier，不能在不重做 parse/inference 的情况下独立重建候选全集；
- Provider 自报 Fact list 又不能自动成为自己的完整性证明；
- 后继必须决定 exact parse-result identity、Fact projection owner，以及 application 如何验账而不补事实。

因此：

```text
shared lifecycle vocabulary
    may exist

but

shared lifecycle vocabulary
    != shared domain construction
    != shared authority owner
    != one universal observation receipt
```

本文不禁止未来使用一个小型共同 envelope；它只禁止在 owner 与 domain semantics 尚未闭合时，先用统一字段
掩盖三类不同义务。

## 6. 下一轮必须先裁决的问题

后继仍是问题定界，不是 precontract implementation。至少要逐项回答：

1. `LANGUAGE_SUPPORT` classification 能否由 application 从 exact bytes 与 frozen Profile 完全机械形成，还是需要
   独立 classifier/provider？
2. parse success 的最小可绑定结果是什么：只保存 terminal receipt 是否足够，还是必须有可复算的 normalized
   parse-result / AST identity？
3. Fact denominator 由谁枚举：parser、Fact Provider、application，还是一个受版本约束的投影器？
4. 如果 domain owner 与 candidate producer 相同，什么独立 conformance 能阻止它缩小自己的考试范围？
5. 一个 parse unit 的 Fact projection 是一项整体 obligation，还是按 AST subject 拆成多项；negative 怎样证明？
6. multi-Provider 是重复观察、分片责任还是不同语义来源；同一 parse result 怎样避免重复定义 domain？
7. 哪些信息只属于 private same-attempt receipt，哪些最终必须进入 public Coverage binding？

这些问题没有答案以前，不命名最小合同，也不预选 `ObservationDomain`、`ObservationOutcome`、AST Artifact、
Evidence 版本或 public file topology。

## 7. 后继资格否定矩阵

| ID | 单变量世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `LPF-000` | 非 accepted encoding 的 `.py` blob 进入 current `supported_paths`；runs COMPLETED | request candidate 等于 language-supported |
| `LPF-001` | accepted encoding、syntax invalid；runs COMPLETED 且无 per-unit outcome | Provider completion 证明 parse closure |
| `LPF-002` | successful rich AST；reported Fact 仅 MODULE | parse success 证明 Fact projection closure |
| `LPF-003` | Provider 自报 domain 与 candidates 双向一致，但 domain 漏掉 AST subject | self-consistent producer domain 是 authoritative denominator |
| `LPF-004` | Coverage 阶段重新 parse 相同 bytes 并得到正确全集 | post-hoc observation 自动继承原 attempt authority |
| `LPF-005` | 两个 Providers 都声称观察全部 domain，但用不同 parser/result identity | COMPLETED runs 自动可比较或可合并 |
| `LPF-006` | parse receipt 完整，Fact projection receipt 缺失 | upstream success 补足 downstream fulfillment |
| `LPF-007` | Fact projection receipt 完整，原 parse result identity 缺失 | downstream self-consistency 修复 upstream identity gap |

本文只实际构造 `LPF-000..002`；其余是下一轮必须审计的 candidate falsifiers，不冒充已运行测试。

## 8. 当前允许与禁止

本候选最多允许发布：

```text
LANGUAGE_SUPPORT, PARSE, FACT_DERIVATION have distinct responsibility semantics
no universal obligation primitive has been selected
full ReviewSliceSet / seven-stage Coverage contract remains not started
```

仍然禁止：

```text
Fact/Parse precontract or contract selection
real parser / AST carrier / Fact projection runtime
ObservationDomain / ObservationOutcome implementation
ReviewSliceSet / CoverageLedger public runtime
Schema / corpus / identity-vector changes
Evidence / Manifest / publisher / Bundle changes
Attention / CLI / Workbench
```

## 9. 候选闭环门

本文只有在以下条件全部成立后，才有资格作为 problem-boundary audit history：

1. `LPF-000..002` 可从本基线的 current-source fixture 与正式 private entry 独立复算；
2. Python 3.10 / 3.13、normal / `-O` canonical reports 一致；
3. 文档 120/137/155/160/175/194 的 authority claim 没有被扩大或推翻；
4. README、AGENTS 与 milestones 只同步候选问题边界，不发布合同或实现状态；
5. diff 只包含本文与三处导航/状态同步，链接、敏感路径、UTF-8 与 `git diff --check` 成立；
6. 候选 PR 原始 required checks 全部成功并经受保护主线合入；
7. 新 exact main Public CI 与 Browser Smoke 成立。

在第 6–7 项完成以前，当前公开状态不变。即使本候选闭合，下一步也只是从新的 exact main 选择并审计最小
contract problem；不得直接实现统一 Ledger、真实 parser、ReviewSliceSet 或 Coverage。
