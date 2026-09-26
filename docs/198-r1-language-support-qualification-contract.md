# R1 Language Support Qualification 最小合同 0.1

> 状态目标（仅[独立冻结发布](199-r1-language-support-qualification-contract-freeze-publication.md)最后门闭合后生效）：`R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@de4eee7e953a0b95d52b973bee35a033e3901254`
>
> 前置审计：[Language Support Qualification 最小合同前置审计](197-r1-language-support-qualification-precontract-audit.md)
>
> 冻结输入：[Schema 与规范身份合同](120-r1-schema-and-canonical-identity-contract.md)、
> [SourceSnapshot runtime 合同](127-r1-source-snapshot-runtime-contract.md)、
> [Derivation Input Binding 合同](132-r1-derivation-input-binding-contract.md)与
> [Derivation Attempt / Fact Provenance 合同](137-r1-derivation-attempt-and-fact-provenance-contract.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本候选只冻结 Language Support
> qualification 的语义输入、版本化 Python 3.10 资格函数、predicate applicability、完整 reason composition、
> stage ownership、exactly-one terminal closure、attempt authority 分离与 Parse consumer boundary。它不创建或修改
> Schema、corpus、identity vector、runtime、classifier、parser、Fact、Coverage、carrier、Evidence、Manifest、
> publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 目的与停止线

文档 196 已证明 Language Support denominator 来自 exact SourceSnapshot terminal inventory 与 sealed Policy
`IN_SCOPE` join，Profile 只拥有支持规则，Provider 不拥有分类 authority。文档 197 又证明：现有
`supported_paths` 只是 positive structural projection；path-only item ref、encoding declaration detection、Schema-valid
first reason 或 ProviderRun terminal 都不能证明一个 total qualification 已经成立。

本合同只关闭以下语义接缝：

```text
exact SourceSnapshot inventory
    + sealed Policy IN_SCOPE decisions
    + frozen Profile support semantics
    + exact owned blob bytes
    + versioned Language Support function
        ↓
deterministic per-subject classification
        ↓
complete canonical failed-reason set
        ↓
exactly one eligible / unsupported disposition
        ↓
private semantic qualification eligible for a future Parse gate
```

它不选择 derived result 的持久化路线，不设计 public object，不运行 parser，也不证明 Parse、Fact 或七阶段 Coverage
闭合。即使本候选以后冻结，任何代码施工仍须由独立状态发布明确授权；本合同文字本身不授予实现资格。

## 2. authority 分工

Language Support 0.1 的 authority 固定为：

```text
SourceSnapshot
  拥有 terminal inventory、raw Git path、entry kind、Git/content identity 与 exact blob bytes binding

sealed Policy
  拥有每个 inventory member 的 IN_SCOPE / OUT_OF_SCOPE 与 source_class

frozen DerivationProfile
  拥有 language、language_semantics、supported_entry_kinds 与 accepted_source_encodings

deterministic application
  拥有 versioned qualification function、applicability、reason composition 与 exactly-one proof

Provider
  不拥有 Language Support denominator、classification、reason 或 completion authority

Parse
  只能消费已合格 eligible subjects；不拥有 Language Support 的回写或扩张权
```

因此：

```text
Policy IN_SCOPE                         != Language Support eligible
Profile allows UTF-8                    != exact bytes decode as UTF-8
path ends in .py                        != source qualified
encoding declaration detected           != whole source decoded
all ProviderRuns COMPLETED               != Language Support closed
same semantic result                     != same attempt authority
classification recomputable              != classification must be persisted
```

## 3. authoritative denominator

### 3.1 唯一 denominator

Language Support denominator 必须由 application 对以下 exact inputs 机械 join：

```text
all SourceSnapshot terminal inventory members
    INNER JOIN
exactly one matching sealed Policy scope_decision by raw Git path
    WHERE
scope_decision.disposition == IN_SCOPE
```

结果按 raw Git path bytes 排序且唯一。`OUT_OF_SCOPE` member 在 `POLICY_SCOPE` 终结，不进入本 stage，也不得在
Language Support 内再次产生 `POLICY_EXCLUDED`。缺失、重复、额外 Policy decision，Policy/Snapshot binding 不一致，
或 inventory bytes 无法复核，都使整个 qualification 没有资格形成；application 不得缩小 denominator 或把 input
failure 改写成 per-subject unsupported。

### 3.2 item reference 不是完整 subject identity

`PARSE_UNIT.item_id = git_path_hex` 只在已绑定同一个 exact world 的集合内定位成员。它不独立证明：

```text
which inventory object and bytes
which sealed Policy decision
which Profile support semantics
which qualification function version
```

同一路径在两个 exact source worlds 中可以拥有不同 classification。任何 path-only cache、caller-supplied disposition
或跨 world transplant 都必须拒绝。

## 4. semantic input identity

### 4.1 exact history binding 与 semantic content 分开

一次 qualification 必须先验证完整历史坐标：

```text
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
exact verified blob bytes by inventory object/content identity
```

这些坐标证明当前 application 正在消费哪一份 frozen history，却不全部进入 Language Support semantic content。
`policy_digest` 还绑定 governance、budget、Provider requirements、module mapping 与 Slice policy；
`analysis_scope_digest` 还绑定 Provider requirements 与 module mapping。无关字段变化不得暗中改变 Language Support
classification identity。

### 4.2 canonical semantic payload

单个 subject 的规范语义投影固定为以下**含义**：

```text
language_support_function = r1-python-language-support/0.1

inventory_item =
  git_path
  git_mode
  git_object
  entry_kind
  content identity when the entry is a blob

scope_semantics =
  disposition = IN_SCOPE
  source_class

profile_support_semantics =
  language
  language_semantics
  supported_entry_kinds
  accepted_source_encodings
  normalization_rules.path
```

本合同冻结 payload 的语义边界，不新增 digest 字段或 public Artifact。未来实现可以形成 private canonical bytes，
但不得把 raw blob body、whole Policy、whole Profile、Provider identity、BudgetContext 或 path-only ref 冒充该
payload。exact owned blob bytes 是 function input：application 必须按 inventory 的 Git object、`content.sha256` 与
`size_bytes` 复核后消费，但不需要把潜在大字节串复制进 semantic identity。相同 payload 与相同 verified bytes
可以跨合法 attempts 产生相同 semantic classification；完整历史 binding 仍须逐次验证。

## 5. versioned Python 3.10 encoding qualification

### 5.1 function identity 与规范来源

首个函数 identity 固定为：

```text
r1-python-language-support/0.1
```

它以 `language = PYTHON`、`language_semantics = PYTHON_3_10` 为唯一首版语言世界。Python 3.10
[encoding declarations](https://docs.python.org/3.10/reference/lexical_analysis.html#encoding-declarations) 与
[PEP 263](https://peps.python.org/pep-0263/) 是语义来源；CPython 3.10.6 的
[`tokenize.detect_encoding`](https://github.com/python/cpython/blob/v3.10.6/Lib/tokenize.py) 与
[`encodings.aliases`](https://github.com/python/cpython/blob/v3.10.6/Lib/encodings/aliases.py) 固定首版
normalization/lookup 的 conformance reference，不是宿主运行时 authority。locale、平台默认编码、当前解释器版本、
Provider tolerance 与 ambient codec registry 都不得改变结果。

### 5.2 total pipeline

当 encoding predicate 适用时，函数必须按以下顺序处理 exact blob bytes：

```text
1. detect UTF-8 BOM
2. inspect Python 3.10-defined first/second physical-line coding declaration positions
3. extract the declaration token without decoding the whole source
4. resolve it through the function's Python 3.10-versioned codec normalization/lookup semantics
5. reject unknown codec or BOM/non-UTF-8 declaration conflict
6. choose the effective encoding
7. decode the whole source with that effective encoding
8. canonicalize the effective encoding to the Profile vocabulary
9. test membership in accepted_source_encodings
```

第二行 declaration 只有在第一行满足 Python 3.10 对 blank/comment-only line 的条件时才生效。普通代码后的
第二行 cookie 不得改变 encoding。无 BOM、无有效 declaration 时 effective encoding 是 `UTF-8`。有 BOM 且没有
冲突时 canonical result 是 `UTF-8-SIG`；BOM 由 decoder 消费，不能作为源码字符传给后继 Parse。

codec token normalization 与 lookup 属于 `r1-python-language-support/0.1`，并固定到上一节给出的 CPython 3.10.6
conformance reference；不得跟随宿主 patch version 或未绑定版本的 codec registry 漂移。未来实现若复用宿主 API，
必须证明其 lookup、alias normalization 与 decoder behavior 对当前输入等价；宿主 API 的成功本身不是 authority。

### 5.3 accepted set 与 failure

首个 frozen Profile 只接受：

```text
UTF-8
UTF-8-SIG
```

因此：

- default UTF-8、合法 UTF-8 cookie/alias 与整份 UTF-8 bytes 可以合格；
- UTF-8 BOM 与一致的 UTF-8 cookie 可以合格为 `UTF-8-SIG`；
- 合法 ASCII、Latin-1 或其他非 accepted declaration 仍不合格；
- unknown codec、BOM/cookie conflict、declaration detection failure、whole-source decode failure 与 accepted-set
  miss 都使 encoding predicate 失败；
- 上述内部失败形状在 0.1 中统一贡献 `UNSUPPORTED_SOURCE_ENCODING`，不得伪装成 `PARSE_ERROR`，也不得
  因当前 public reason 较粗而跳过检测或整份 decode。

检测成功不等于 decode 成功；decode 成功也不等于 Profile 接受。函数必须对任意 bounded byte string 终结为确定
结果或使整个 qualification 因 input/infrastructure integrity failure 不成立，不能悬空等待 Provider 解释。

## 6. predicate applicability graph

对 denominator 中每个 subject，四类 predicate 与适用条件固定为：

| Predicate | Authority | Applicability | Failed reason |
| --- | --- | --- | --- |
| source class | sealed Policy | 始终 | `UNCLASSIFIED_SOURCE` |
| entry kind | frozen Profile | 始终 | `UNSUPPORTED_ENTRY_KIND` |
| language/path | frozen Profile + raw Git path | 始终 | `UNSUPPORTED_LANGUAGE` |
| source encoding | exact blob bytes + frozen Profile/function | entry kind predicate 通过，且 language/path predicate 通过 | `UNSUPPORTED_SOURCE_ENCODING` |

predicate 结果固定为：

```text
source class passes
  iff source_class in {FIRST_PARTY, GENERATED, VENDORED}

entry kind passes
  iff inventory_item.entry_kind is in supported_entry_kinds

language/path passes
  iff Profile language is PYTHON
  and raw Git path bytes end with exact ASCII bytes ".py"

source encoding passes
  iff section 5 produces a canonical encoding
  and that value is in accepted_source_encodings
```

raw Git path 不经过 Unicode decode、NFKC、大小写折叠、URL decode、宿主路径 separator 替换或 locale 解释。
`.PY`、`.pyw`、无 `.py` suffix 的文件在 0.1 中不属于 Python source candidate。

applicability 不是短路顺序。source class 失败不阻止 entry-kind 与 language/path predicate 求值；只有表中明确依赖
前态的 source-encoding predicate 可以不适用。unsupported entry kind 或非 Python path 不得被强行读取/解码并
编造 encoding reason。

## 7. complete canonical reason composition

### 7.1 完整集合

application 必须对每个 subject 求值全部 applicable predicates，收集所有 applicable 且失败的 reasons，去重并按
固定 rank 排序：

```text
UNCLASSIFIED_SOURCE
UNSUPPORTED_ENTRY_KIND
UNSUPPORTED_LANGUAGE
UNSUPPORTED_SOURCE_ENCODING
```

该顺序只定义 canonical representation，不定义 first-failure winner。检查顺序、并行调度、短路位置或 Provider
报告不得改变 reason set。

### 7.2 exactly-one disposition

单个 subject 的 terminal composition 固定为：

```text
failed_reasons == []
    -> eligible

failed_reasons != []
    -> unsupported(reason_codes = complete canonical failed_reasons)
```

Language Support 没有第三个 per-subject `unseen`、`unknown` 或 `not_run` terminal。exact inputs、函数 identity 或
integrity binding 缺失时，整个 qualification 不成立；application 不得把 infrastructure failure 塞入最接近的
unsupported reason，也不得把缺失 subject 默认为 eligible。

### 7.3 denominator closure proof

application 必须机械证明：

```text
denominator = eligible U unsupported
eligible ∩ unsupported = empty
```

并同时验证：

1. 每个 denominator member 恰好出现一次；
2. 没有额外 path、重复 member 或跨 exact-world transplant；
3. 每个 unsupported reason set 非空、唯一、有序并等于所有 applicable failed predicates；
4. eligible member 不携带 unsupported reason；
5. `OUT_OF_SCOPE` item 不进入本 stage；
6. 每个 item ref 能回连同一个 exact inventory item、Policy decision、Profile semantics 与 function identity。

这是一份 deterministic composition proof，不是 Provider receipt、parser outcome 或 Coverage self-report。

## 8. stage-reason ownership

stage ownership 固定为：

| Reason | Owner stage | Boundary |
| --- | --- | --- |
| `POLICY_EXCLUDED` | `POLICY_SCOPE` | `OUT_OF_SCOPE` 不进入 Language Support denominator |
| `UNCLASSIFIED_SOURCE` | `LANGUAGE_SUPPORT` | sealed Policy source class 不具备 Parse eligibility |
| `UNSUPPORTED_ENTRY_KIND` | `LANGUAGE_SUPPORT` | entry kind 不在 frozen Profile accepted set |
| `UNSUPPORTED_LANGUAGE` | `LANGUAGE_SUPPORT` | frozen language/raw-path rule 不成立 |
| `UNSUPPORTED_SOURCE_ENCODING` | `LANGUAGE_SUPPORT` | exact bytes 未通过 section 5 |
| `UNSUPPORTED_SYNTAX_VERSION` | `PARSE` | 只有后继 parser/version discrimination contract 可以解释 |
| `PARSE_ERROR` | `PARSE` | 来自实际 parser execution |

current Schema 能接受某 reason 的多个 placement，不构成语义授权。Language Support 不运行 parser，不生成 AST，
不解释 `SyntaxError`，也不区分 Python 3.13-only syntax 与普通 invalid syntax。`UNSUPPORTED_SYNTAX_VERSION` 在本
合同中被明确赶出 Language Support；Parse 如何区分它与 `PARSE_ERROR` 仍未决定。

## 9. semantic result 与 live continuation

相同 canonical semantic payload 与相同 function identity 可以在不同合法 attempts 中复算出相同 classification。
这只允许内容复用或一致性比较：

```text
same semantic inputs + same function
    -> same semantic classification

same semantic classification
    != same attempt
    != same BudgetContext
    != same deadline/resource ownership
    != right to continue into Parse
```

未来 same-attempt pipeline 必须另外持有并独占 claim 原始 live continuation。新建一个 limits 相同的
`BudgetContext`、读取历史 projection、传入 caller boolean 或比较 classification digest 都不能恢复该 authority。
semantic identity 不得包含 live handle；live handle 也不得成为 semantic result 内容。

本合同不命名 continuation class、claim API 或 private carrier。它只冻结两种 authority 必须分离。

## 10. Parse consumer boundary

Parse 只能消费当前 exact qualification 的 eligible members，并在执行前重新验证：

```text
same exact SourceSnapshot / Policy / Profile history binding
same Language Support function identity
subject remains in the exact eligible set
original current-attempt continuation remains live and exclusively claimable
```

Parse 不得：

- 把 Language Support eligible 偷换成 parse success；
- 接受 unsupported member 或回写其 reason；
- 重新定义 Language Support denominator、applicability 或 accepted encoding set；
- 用 parser 对某 encoding 的容忍扩大 Profile；
- 用 `SyntaxError` 反填 `UNSUPPORTED_SOURCE_ENCODING`；
- 从另一次 attempt 的同字节 classification 借 continuation。

Language Support 也不得读取 AST、执行 grammar discrimination、形成 Fact candidate，或从“parser 以后可能成功”
反推当前 qualification。

## 11. persistence 是显式 non-decision

本合同同时允许两个尚未选择的后继方向：

```text
Route A: live recomputation
  exact owned inputs + versioned function
      -> same-attempt deterministic classification

Route B: canonical derived projection
  frozen inputs + function identity
      -> self-contained historical/offline classification material
```

选择只能由未来消费边界决定：public/offline verifier 是否被保证能重新取得并复核 exact blob bytes，以及 Bundle 是否
要求 self-contained verification。工程便利、现有 Schema 形状或“多留证据”不能代替该判断。

无论选择哪条路线，classification 都是 deterministic derived fact：

```text
not Provider observation evidence
not execution receipt
not parser outcome
not Coverage authority
```

本合同不新增 public carrier、digest、Schema role、Manifest entry、Evidence field 或 Bundle file。

## 12. 资格否定矩阵

| ID | 已知世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `LSC-000` | 同一 path ref 指向不同 exact bytes/policy worlds | path-only ref 是完整 semantic identity |
| `LSC-001` | UTF-8 cookie 检测成功，body 后部含非法 UTF-8 bytes | declaration detection 等于 whole-source qualification |
| `LSC-002` | 合法 ASCII/Latin-1 declaration 与可解码 body | Python 可解码等于 Profile accepted |
| `LSC-003` | UTF-8 BOM 与 non-UTF-8 cookie 冲突 | conflict 可以推迟给 Parse |
| `LSC-004` | unknown codec 或 host-only codec alias | ambient codec registry 有资格改变 0.1 result |
| `LSC-005` | source class、entry kind、language、encoding 中多个 applicable predicates 同时失败 | first failure 是完整 classification |
| `LSC-006` | unsupported entry kind 或非-Python path 使 encoding predicate 不适用 | complete reason set 要求编造 encoding failure |
| `LSC-007` | Python 3.13-only syntax与普通 invalid syntax在 Python 3.10 parser 下都失败 | Language Support 有资格声明 syntax version outcome |
| `LSC-008` | denominator 中一个 member 被遗漏、重复或同时 eligible/unsupported | Schema-valid remaining members 足以证明 closure |
| `LSC-009` | 同一 classification 在另一个 attempt 被复算 | semantic equality 继承 live continuation |
| `LSC-010` | live exact inputs 足以重算 | public/offline consumer 必然拥有 blob reacquisition authority |
| `LSC-011` | ProviderRun `COMPLETED` 且 `supported_paths` 非空 | Provider output 已证明 total Language Support qualification |

这些 falsifiers 冻结语义拒绝边界，不预造测试类、public error enum 或 carrier。

## 13. 后继实现边界

本候选冻结以前不授权代码。若独立 freeze publication 最终成立，后继仍须从新的 exact main 重新审计最小实现面；
最多可以考虑：

```text
exact input/history validation
deterministic private qualification function
complete per-subject composition
exactly-one closure validation
private same-attempt Parse gate proof
LSC-000..011 hardening
```

该列表不是当前施工授权。尤其不得从本合同直接开始：

```text
public Schema / corpus / identity-vector change
public classification carrier or new Bundle file
persistence Route A/B selection
real parser / AST / Fact Provider
Parse fulfillment contract or implementation
shared ObservationReceipt / FulfillmentLedger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root
Attention / CLI / Workbench / Core / Q / O / T
```

若 private proof 必须先选择 persistence、修改 public identity 或借用 Parse/Fact authority 才能成立，必须停止并用
新反例重开对应最小边界。

## 14. 候选冻结门

本节保留合同候选的冻结门。[独立冻结发布](199-r1-language-support-qualification-contract-freeze-publication.md)
记录候选资格与发布目标；只有以下链条完整成立后，合同状态才可生效为
`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN`：

1. `LSC-000..011` 能从 frozen inputs、文档 197 反例与本合同独立复核；
2. Python 3.10 encoding function、applicability、reason rank、stage ownership 与 total closure 没有依赖宿主环境或
   Provider 自报；
3. persistence 明确保留为 non-decision；
4. 文档 120/127/132/137/194/195/196/197 的 authority claim 没有被扩大或推翻；
5. diff 只包含本文、文档 197 状态闭合与三处公开导航/状态同步；
6. Markdown links、UTF-8、fence/heading、敏感路径、状态 marker 与 `git diff --check` 成立；
7. 候选 PR original required checks 全部成功并经受保护主线合入；
8. 候选 exact main 的 Public CI 与 Browser Smoke 成立；
9. README、本文与 milestones 的 fresh public readback 证明公开内容与 exact Git bytes 一致；
10. 独立 freeze publication 自己的 original PR 门、受保护合入、exact-main 双门与 fresh readback 再次成立。

第 10 项以前，本合同不能自称 frozen，也不能授权 runtime。任何新反例都可否决冻结或只重开被击穿的最小条款。

当前原则候选冻结为：

> Language Support is a deterministic qualification over an exact semantic world; semantic equality may be
> reused, but execution authority must be reacquired for every attempt.

中文：**Language Support 是对 exact semantic world 的确定性资格分类；语义结果可以复用，执行权必须逐次取得。**
