# R1 Language Support Qualification Authority 问题审计

> 状态（候选）：`R1_LANGUAGE_SUPPORT_QUALIFICATION_AUTHORITY_PROBLEM_AUDIT_CANDIDATE /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_NOT_STARTED /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@2ce608ce80a39a3bbd3dd15bdab60d3940a1c21d`
>
> 上游审计：[Language Support / Parse / Fact Fulfillment 问题边界审计](195-r1-language-support-parse-fact-fulfillment-problem-boundary-audit.md)
>
> 影响层级：`L3_SYSTEM_AUDIT + L2_CONTRACT_PROBLEM_BOUNDARY + L0_DOCUMENTATION`；本文只判断
> `LANGUAGE_SUPPORT` 的 denominator、规则 authority、classification construction 与最小待证事实，不选择
> terminal enum、receipt、Schema、runtime、parser、Provider、Coverage publisher 或共同 carrier。

## 1. 审计问题与停止线

文档 195 已经证明：

```text
candidate path entered current request
    != language-support qualification fulfilled
```

本轮把问题严格拆成两层：

```text
A. qualification function 是否已经由 frozen inputs 完整定义？
B. 若 function 完整且可复算，qualification result 是否仍须作为历史事实持久化？
```

只有 A 成立后才有资格讨论 B。不能因为 current runtime 没有逐项 outcome，就先假定必须新增 receipt；也不能
因为 exact inputs 已经保存，就假定当前合同已经定义了唯一结果。

本文不进入 Parse 或 Fact。即使某个 source 满足 Language Support，也不能据此声称 parser 已运行、syntax 被
接受、AST 已形成或 Fact projection 已履责。

## 2. Denominator 不是单一 Artifact 独占

文档 120 冻结：`LANGUAGE_SUPPORT` denominator 是 Policy 的全部 `IN_SCOPE` entries，item identity 是对应 raw
Git path 的 `PARSE_UNIT`。该集合不是由 Profile、Provider 或 Coverage consumer 任意选择：

```text
SourceSnapshot terminal inventory
    -> exact subject identity / path / entry kind / content identity

ReviewPolicy scope_decisions
    -> every inventory item receives exactly one IN_SCOPE / OUT_OF_SCOPE decision
    -> source_class is sealed policy input

LANGUAGE_SUPPORT denominator
    -> exactly the IN_SCOPE join result
```

因此：

```text
Profile declares support rules
    != Profile owns denominator membership

Policy declares scope
    != Policy invents source bytes or entry kind

Provider receives candidates
    != Provider may shrink the denominator
```

denominator 可以在任何 Provider 执行前由 exact Snapshot + Policy 机械建立。Profile 只参与随后对每个 denominator
member 的资格判断。

## 3. 资格判断所需事实已经存在，但完整函数尚未冻结

首个 Profile 已固定：

```text
language                  = PYTHON
language_semantics        = PYTHON_3_10
accepted_source_encodings = [UTF-8, UTF-8-SIG]
supported_entry_kinds     = [REGULAR_BLOB, EXECUTABLE_BLOB]
raw path suffix           = ASCII .py
```

Policy 另提供 `source_class`；Derivation Input Binding 已经把 exact Snapshot、Policy、Profile 与每个 blob 的 Git
object bytes 闭合，且不允许从 mutable path 重新读取。因此 Language Support 的判断不需要 Provider 产生新的外部
事实。它可以是一项对已冻结输入的纯资格计算：

```text
semantic rule authority
    = sealed Policy + frozen Profile

subject / byte authority
    = exact SourceSnapshot + verified Git object bytes

classification construction
    = deterministic application applying those rules

Provider authority
    = none for deciding Language Support
```

这里的 application 只执行既有规则，不能自行新增支持语言、扩大 accepted encoding、改写 source class 或删除
denominator member。

因此，对“current live DerivationInputSet 的数据是否足够”的回答是 **是**：不需要 Provider 再观察外部世界。
对“qualification function 是否已完整定义”的回答仍是 **否**。现有冻结材料还不足以直接授权实现一个 total
classifier：

1. Profile 给出了接受集合，却没有把 coding-declaration detection 固定为一个独立于宿主解释器的规范算法；
2. public Coverage Schema 允许 `UNCLASSIFIED_SOURCE / UNSUPPORTED_ENTRY_KIND / UNSUPPORTED_LANGUAGE /
   UNSUPPORTED_SOURCE_ENCODING / UNSUPPORTED_SYNTAX_VERSION` 出现在通用 `unsupported` disposition，却没有限制
   每个 reason 属于哪个 stage；
3. 同一 item 同时不满足 source class、entry kind、path/language 与 encoding 时，尚未冻结“记录全部适用 reason”
   还是“按固定优先级形成一个 terminal reason”；
4. 是否需要逐项 canonical result、若需要其 exact-input binding 是什么，以及后继 same-attempt continuation 怎样
   消费它，尚未定义。

因此：

```text
inputs are sufficient for a deterministic classification
    != the total classification contract already exists

total classification can be recomputed
    != its result must be persisted as execution evidence
```

Language Support 与 Parse 因此进一步分叉：前者目前更像 deterministic derived qualification；后者必须证明真实
parse execution 已经发生。本文不把前者重新命名为 observation fulfillment。

## 4. Current runtime 实际做了什么

`_execution_cell_application._validate_source_blobs()` 当前验证全部 BLOB request bytes 与 Snapshot 的 path、size 和
SHA-256 一致，然后只用两个结构条件形成 `ValidatedRequest.supported_paths`：

```text
entry_kind in profile.supported_entry_kinds
and raw_path.endswith(b".py")
```

它不读取 `source_class`，不检测 Python coding declaration，不验证 exact bytes 是否能按 accepted encoding 解码，
也不形成 denominator 中每个 item 的 qualification projection。Fact admission 与 multi-Provider composition 后面仍只
重复 entry-kind、scope 与 `.py` path eligibility；它们不补 Language Support 事实。

这符合现有 mechanism-test Provider 合同，不是 runtime defect。更重要的是，exact Snapshot/Policy/Profile digests
已经保留“输入 world 不同”这一 identity 事实，live DerivationInputSet 还 copy-own verified blob bodies；缺少显式
projection 不等于 same-attempt 数据不足。另一方面，public SourceSnapshot inventory 只保存 Git/content identity、
size 与 hash，不内嵌 blob body；只有历史 Bundle 的第三方未必能离线重算。`supported_paths` 只是一个消费方便的
positive structural projection，既不能单独充当 denominator，也不能被升级为完整 qualification history。

## 5. 六个 exact-input world

审计在仓库外临时目录中复用 current SourceSnapshot、Derivation Input、request validator 与真实 closed
multi-Provider composition entry。审计 oracle 只读取 exact path/kind/source-class/blob bytes，并用当前解释器的
`tokenize.detect_encoding` 帮助区分测试 world；它不进入产品 runtime，也不取得未来 classifier 或 Coverage
authority。

前五个 world 只改变 `pkg/regular.py` 的 bytes 或其 sealed `source_class`；第六个只改变同一 entry 的 scope
disposition，用于验证 denominator 边界。当前 Schema 中 `UNCLASSIFIED` 是 `source_class`，不是
`scope_decisions.disposition`；一个 entry 可以同时是 `IN_SCOPE + UNCLASSIFIED`，因此它仍属于 Language Support
denominator。

| World | denominator member | authoritative input facts | `supported_paths` 是否单独区分 |
| --- | --- | --- | --- |
| `UTF8` | 是 | UTF-8 可解码且在 Profile 接受集合 | 否；只投影为 present |
| `UTF8_SIG` | 是 | UTF-8-SIG 可解码且在 Profile 接受集合 | 否；只投影为 present |
| `LATIN1_DECLARATION` | 是 | 可按 ISO-8859-1 解码，但不在 Profile 接受集合 | 否；仍 present |
| `INVALID_UTF8` | 是 | accepted encoding 不成立 | 否；仍 present |
| `UNCLASSIFIED_UTF8` | 是 | encoding accepted；sealed source class 是 `UNCLASSIFIED`，其 stage effect 尚待 total function | 否；仍 present |
| `OUT_OF_SCOPE_UTF8` | 否 | encoding accepted；Policy disposition 是 `OUT_OF_SCOPE` | `supported_paths` 仍 present；必须与 `in_scope_paths` join 才排除 |

前五个 in-scope world 都得到：

```text
in-scope entries                = 7
current request candidates      = 4
required ProviderRun statuses   = [COMPLETED, COMPLETED]
Provider diagnostic counts      = [0, 0]
overall execution               = COMPLETED
normal continuation at terminal = true
reported Fact kinds             = [MODULE]
per-item Language Support carrier = absent
```

`OUT_OF_SCOPE_UTF8` 的 `in_scope_count = 6`，`regular.py` 仍在 `supported_paths`，但不在
`in_scope_paths ∩ supported_paths`。这证明 denominator 必须来自 Snapshot/Policy join，不能从字段名为
`supported_paths` 的正集合反推。

因此以下 world 在 `supported_paths` 这个 projection 上不可区分：

```text
accepted UTF-8
accepted UTF-8-SIG
non-accepted legal coding declaration
invalid source bytes
Policy IN_SCOPE + UNCLASSIFIED source
```

它们在 exact current inputs 中仍然可区分；一旦 total function 被合同冻结，持有 verified blob bodies 的
same-attempt application 原则上可以重新计算。只持有 public Snapshot/Policy/Profile 的第三方则只有 body identity，
没有 body bytes，不能据此自动离线重算。这次反例只否定 `supported_paths` 作为完整 qualification history，不证明
必须或不必新增持久化 outcome。

审计还复核同一 Snapshot 的七个 entry：symlink、unknown-mode blob 与 gitlink 没有进入 `supported_paths`；三个正常
`.py` entry 与一个 raw path 不能按 UTF-8 解码的 `b"\xff.py"` 都进入。前者只证明结构过滤发生过，后者证明
`.py` suffix 也不能替代完整 language/path qualification。current carrier 没有保存每项为什么进入或未进入。

## 6. 当前能裁决的最小 authority 形状

本轮事实支持以下分权：

### 6.1 规则定义权

- Human-sealed Policy 决定 scope 与 source class；
- frozen Profile 决定语言语义、支持的 entry kinds 与 accepted encodings；
- runtime、Provider 与 Coverage consumer 均不能改变这些集合。

### 6.2 资格构造权

- total function 一旦冻结，deterministic application 可以从 exact owned inputs 机械形成 classification；
- 它必须消费 verified blob bytes，不能重读 mutable filesystem path；
- 它不能借宿主 Python 版本、locale、默认 encoding 或 ambient package 扩大 Profile；
- classifier failure 不能被伪装成某个“最接近”的 unsupported reason。

### 6.3 Result persistence 仍是开放问题

当前不能从“没有 outcome carrier”直接推出“必须新增 execution receipt”。至少存在两个仍待比较的合法候选：

```text
Route A
    same-attempt consumer 从 live exact inputs 按 versioned total function 重新计算
    -> result 是可复算 derived fact

Route B
    application 同时保存 canonical derived projection
    -> 用于免重算、跨生命周期绑定或 public offline 核账
    -> 仍不是 Provider observation evidence
```

若 Route B 最终有必要，持久化对象也不能因此获得新的规则 authority；它只是 frozen inputs 与 versioned function
的派生结果。是否要求 self-contained public verification、是否允许按 exact Git object 重新取 bytes，以及
reacquisition authority/availability 怎样表达，都会影响选择。本文不选择 Route A 或 B。

### 6.4 Provider 与后继层的禁止项

- Provider 不拥有 Language Support denominator 或 terminal classification；
- Provider `COMPLETED`、空 candidates 或已有 Facts 都不能补写 support outcome；
- Parse 只能消费已经合法 qualified 的 parse-unit domain，不能回头重定义它；
- Coverage application 只能核账与绑定，不能 post-hoc 重新检测后宣称原 attempt 已经履责。

## 7. 还必须冻结的最小问题

下一份 precontract 以前至少要回答：

1. exact `IN_SCOPE` item 到 Language Support subject 的 canonical identity；
2. coding declaration、BOM、invalid bytes 与 raw non-UTF-8 path 的版本化判断算法；
3. source class、entry kind、language/path 与 encoding 多条件失败时的 total classification rule；
4. reason 的 stage ownership，尤其不得让 `UNSUPPORTED_SYNTAX_VERSION` 把 Parse 偷进 Language Support；
5. qualification 是否只需在 live attempt 内按需重算，还是 public/offline verifier 构成必须持久化 canonical
   projection 的独立理由；
6. semantic classification identity 是否可跨 attempt 重算复用，以及 live continuation 怎样仍只属于当前 attempt；
7. application 怎样证明 denominator 每一项恰好有一个 terminal disposition，且不能遗漏、重复或越界；
8. 后继 Parse 怎样消费 eligible set，而不把 support success 偷换成 parse success。

这些问题没有答案以前，不命名 terminal enum，不选择 receipt/envelope，不改 public Schema，也不实现 classifier。

## 8. 资格否定矩阵

| ID | 已知世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `LSQ-000` | Policy 有 7 个 `IN_SCOPE` entries，current `supported_paths` 只列 4 个 paths | positive structural projection 是 Language Support denominator |
| `LSQ-001` | Latin-1 declaration 或 invalid UTF-8 的 `.py` 仍进入 current request | request candidate 等于 accepted encoding |
| `LSQ-002` | `UNCLASSIFIED` 的 valid UTF-8 `.py` 仍进入 current request | accepted bytes 足以形成 eligible parse unit |
| `LSQ-003` | UTF-8 与 UTF-8-SIG 均满足 Profile，但无逐项 result projection | projection absent 自动证明 inputs 不足，或自动证明必须新增 execution receipt |
| `LSQ-004` | valid UTF-8 entry 被 Policy 改为 `OUT_OF_SCOPE`，仍在 `supported_paths` | structural projection 拥有 scope authority |
| `LSQ-005` | 一个 item 同时不满足多项支持条件 | Schema 允许多个 reason 就等于 reason composition 已冻结 |
| `LSQ-006` | Coverage consumer 对相同 bytes 重新得到正确 classification | post-hoc recomputation 自动继承原 attempt continuation authority |

本文实际构造 `LSQ-000..004`；`LSQ-005/006` 是下一轮必须解决的合同 falsifier，不冒充已运行产品测试。

## 9. 四格与代码边界复核

Python 3.10.6 / 3.13.13、normal / `-O` 四次独立运行的 canonical report 逐字节相同：

```text
sha256 = 168401b563292ab157db02b648787657b7cdc4788c07636d8ba5a9a0e0999498
bytes  = 23888
```

四格一致只证明本次 falsifier projection 稳定；因为 audit oracle 使用宿主 `tokenize.detect_encoding`，它不把该
函数升级成产品规范。最终 diff 不包含审计脚本或 report，也不修改 runtime、tests、fixture、Schema、Profile、
Policy、Coverage 或 frozen history。

## 10. 当前允许与禁止

本候选最多允许发布：

```text
Language Support denominator is the exact IN_SCOPE inventory join
Language Support has enough exact data for mechanical classification
classification rule authority and construction authority are distinct
the total function is not yet frozen
persistence of a derived result has not been selected
```

仍然禁止：

```text
Language Support precontract / contract selection
terminal enum / receipt / shared envelope implementation
Parse / AST / Fact projection work
ReviewSliceSet / CoverageLedger public runtime
Schema / corpus / identity-vector changes
Evidence / Manifest / publisher / Bundle changes
Attention / CLI / Workbench
```

## 11. 候选闭环门

本文只有在以下条件全部成立后，才有资格成为 Language Support problem-audit history：

1. `LSQ-000..004` 可从本基线 current-source fixture 与正式 private entry 独立复算；
2. Python 3.10 / 3.13、normal / `-O` canonical reports 一致；
3. 文档 120/132/137/155/160/175/194/195 的 authority claim 没有被扩大或推翻；
4. README、AGENTS 与 milestones 只同步候选问题边界，不发布合同或实现状态；
5. diff 只包含本文与三处导航/状态同步，链接、敏感路径、UTF-8 与 `git diff --check` 成立；
6. 候选 PR original required checks 全部成功并经受保护主线合入；
7. 新 exact main Public CI 与 Browser Smoke 成立。

在第 6–7 项完成以前，当前公开主线状态不变。即使本候选闭合，下一步也只能从新的 exact main 做 Language
Support precontract audit；不得直接实现 classifier、Parse、Fact、ReviewSliceSet、Coverage 或共同 Ledger。
