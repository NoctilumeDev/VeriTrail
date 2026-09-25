# R1 Language Support Qualification 最小合同前置审计

> 状态：`R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_CANDIDATE /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 基线：`main@26b235cda3ba220e7de222a8e8ab8d2effedb5f4`
>
> 审计闭合基线：`main@de4eee7e953a0b95d52b973bee35a033e3901254`
>
> 上游审计：[Language Support Qualification Authority 问题审计](196-r1-language-support-qualification-authority-problem-audit.md)
>
> 后继候选：[Language Support Qualification 最小合同](198-r1-language-support-qualification-contract.md)

本文只把文档 196 留下的八个问题压成下一份最小合同必须覆盖的语义面。它不发布合同，不命名 public
Artifact，不选择持久化路线，也不实现 classifier、Parse、Fact、Coverage 或共同 carrier。

## 1. 本轮问题

文档 196 已经证明：

```text
Language Support denominator
    = exact SourceSnapshot terminal inventory
    + sealed Policy IN_SCOPE join

rule authority
    = sealed Policy + frozen DerivationProfile

classification construction
    = deterministic application

Provider authority
    = none
```

但这还没有定义一个 total qualification function。当前 frozen materials 没有唯一回答：

```text
同一路径在不同 exact source world 中是否还是同一个 qualification subject？
encoding detection 与整份源码 decode 怎样组合？
多个失败条件是只保留第一个，还是保留全部适用理由？
UNSUPPORTED_SYNTAX_VERSION 属于 Language Support 还是 Parse？
每个 denominator member 怎样证明恰好闭合一次？
可复算 semantic result 是否携带原 attempt 的 continuation authority？
```

因此本轮审计的目标不是设计 outcome 对象，而是确定下一合同的最小语义表面与禁止项。

## 2. 停止线

本文不修改：

```text
runtime / tests / fixtures
SourceSnapshot / ReviewPolicy / DerivationProfile
public Schema / compatibility corpus / identity vectors
CoverageLedger / Evidence / Manifest / publisher / Bundle
Parse / AST / Fact / Relation / Slice
```

本文不会把宿主 Python 的 `tokenize.detect_encoding()` 直接升级成产品合同，也不会因为当前 public Schema 能接受
某种 reason placement，就反推该 placement 已获语义授权。

## 3. authoritative subject 与 semantic input identity

### 3.1 path-only 只够做局部 item reference

文档 120 冻结 `PARSE_UNIT.item_id = git_path_hex`，同时要求 Ledger 顶层绑定 Snapshot/Profile/Policy。该 path-only
reference 可以在一个已绑定的 Ledger 内定位成员，却不能独立承担 Language Support classification identity。

本轮构造两个 exact worlds：同一 `pkg/regular.py` 的 `CoverageItemRef` 完全相同，但 blob bytes、
`source_snapshot_digest` 与 `analysis_scope_digest` 均不同；一个 world 是 accepted UTF-8，另一个是合法但 Profile
不接受的 Latin-1。于是：

```text
same PARSE_UNIT path ref
    !=
same Language Support semantic input
```

### 3.2 下一合同必须绑定的最小语义

一个 classification subject 至少由以下 authoritative inputs 共同决定：

```text
exact inventory item
    raw Git path identity
    entry kind
    exact content/object identity and bytes

exact matching Policy decision
    disposition == IN_SCOPE
    source_class

exact Profile support semantics
    language / language_semantics
    supported_entry_kinds
    accepted_source_encodings
    normalization rules relevant to this stage

versioned Language Support function identity
```

`policy_digest` 还绑定 execution budget 与 governance，过宽；现有 `analysis_scope_digest` 又同时绑定 Provider
requirements 与 module mapping。下一合同可以引用现有 broader digest 作为外层历史坐标，但不能在没有说明的
情况下把这些无关变化变成 Language Support semantic identity。本文不预造新 digest 字段；它只要求合同明确
选择 canonical payload，不能让 path-only、whole Policy 或 Provider identity 暗中代替。

## 4. versioned encoding qualification semantics

Python 3.10 的语言参考明确规定：源码 encoding declaration 只在第一或第二行的特定位置生效；无 declaration
时默认 UTF-8；UTF-8 BOM 声明 UTF-8；无法解码的源码抛出 `SyntaxError`。PEP 263 还规定 BOM 与非 UTF-8
cookie 冲突必须失败，整份源码使用单一 encoding。参见 [Python 3.10 encoding declarations](https://docs.python.org/3.10/reference/lexical_analysis.html#encoding-declarations)
与 [PEP 263](https://peps.python.org/pep-0263/)。CPython 3.10 的
[`tokenize.detect_encoding`](https://github.com/python/cpython/blob/3.10/Lib/tokenize.py) 是本轮 audit oracle 的实现
参照，不自动成为 VeriTrail 产品规范。

下一合同至少要冻结以下顺序：

```text
exact blob bytes
    ↓
Python 3.10-compatible BOM / first-two-line declaration detection
    ↓
canonical encoding-name normalization
    ↓
known codec and BOM/cookie consistency check
    ↓
whole-source decode using the detected encoding
    ↓
Profile accepted_source_encodings membership
```

检测成功不等于整份源码 decode 成功。反例中 `# coding: utf-8` 可以被正确检测，但后续 body 仍含非法字节；
这必须被判为 source encoding 不合格，不能被推迟成 parser syntax failure。

首个 Profile 的 accepted set 仍只有：

```text
UTF-8
UTF-8-SIG
```

因此：

- 无 declaration 且整份 bytes 可按 UTF-8 解码，属于 `UTF-8`；
- UTF-8 aliases 必须按冻结规则 canonicalize，而不是依赖宿主 codec 名称字符串；
- BOM 成立且 cookie 与 UTF-8 一致，属于 `UTF-8-SIG`；
- 合法 `ascii`、Latin-1 或其他 coding declaration 即使恰好能表示当前文本，也不属于首个 Profile accepted set；
- unknown codec、BOM/cookie 冲突、detection failure 与 whole-source decode failure 都终结为 source-encoding
  不合格；它们不因此成为 Parse outcome；
- coding declaration 只有在 Python 3.10 规定的位置才生效；普通代码后的第二行 cookie 不得改变 encoding。

这是一条版本化产品语义；未来 Profile 若接受更多 encoding，必须形成新的 Profile/function identity，不能由宿主
Python、locale 或 Provider 自行扩大。

## 5. total classification composition

### 5.1 四类 Language Support predicates

对 denominator 中每个 `IN_SCOPE` subject，下一合同至少需要四类判断：

| Predicate | Authority | 适用条件 | 失败 reason |
| --- | --- | --- | --- |
| source class | sealed Policy | 始终 | `UNCLASSIFIED_SOURCE` |
| entry kind | frozen Profile | 始终 | `UNSUPPORTED_ENTRY_KIND` |
| language/path | frozen Profile + raw Git path | 始终 | `UNSUPPORTED_LANGUAGE` |
| source encoding | frozen Profile + exact blob bytes | entry kind 可提供 blob bytes，且 language/path 已识别为当前 Python source candidate | `UNSUPPORTED_SOURCE_ENCODING` |

`source_class` 不改变 Policy 的 `IN_SCOPE` 决定，但 `UNCLASSIFIED` 仍会阻止该 subject 进入 Parse eligibility。
`OUT_OF_SCOPE` 根本不进入本 stage denominator，因此不能在 Language Support 内再次产生 `POLICY_EXCLUDED`。

### 5.2 reason composition 不能依赖执行顺序

现有 Schema 同时接受以下两份输出：

```text
all applicable failed reasons

和

only the first failed reason
```

二者都可以保持 digest 与 stage partition 自洽。因此 Schema 不能替合同选择语义。

本轮审计选择下一合同必须采用：

> 对每个 subject，计算所有**适用且失败**的 Language Support predicates；若集合非空，按 frozen reason rank
> 输出完整且唯一的 reason set。不得由检查顺序、短路位置或 Provider 选择“第一个理由”。

“所有”不等于对无意义的 predicate 强行求值。gitlink 等 unsupported entry kind 没有 blob body，不能再编造
encoding 结果；encoding predicate 只在上表条件成立时适用。该 applicability graph 必须和 reason completeness
一起冻结，否则 complete set 仍会因实现路径不同而漂移。

### 5.3 terminal composition

对已知 denominator 的单个 subject：

```text
applicable_failed_reasons == []
    -> eligible for Parse input

applicable_failed_reasons != []
    -> unsupported with the complete canonical reason set
```

Language Support 没有第三种“未观察”终态：当 exact inputs 与 versioned function 都成立时，它是 deterministic
derivation。若 exact blob bytes、Profile 或 Policy binding 缺失，整个 qualification 没有资格形成；application
不能把 infrastructure/input failure 伪装成 `UNSUPPORTED_SOURCE_ENCODING`。

## 6. stage-reason ownership

本轮实际证明 current public Schema 会同时接受：

```text
UNSUPPORTED_SYNTAX_VERSION at LANGUAGE_SUPPORT
UNSUPPORTED_SYNTAX_VERSION at PARSE
```

但 Language Support 的职责只到“这个 exact source 是否具有进入 Parse domain 的资格”。Python 3.13-only syntax
与普通 invalid syntax 在 Python 3.10 parser 下都可能只表现为 `SyntaxError`；Language Support 没有 AST/grammar
execution authority，也没有资格解释两者。

因此下一合同的 stage ownership 必须固定为：

| Reason | Owner stage | 说明 |
| --- | --- | --- |
| `POLICY_EXCLUDED` | `POLICY_SCOPE` | `OUT_OF_SCOPE` 不进入 Language Support denominator |
| `UNCLASSIFIED_SOURCE` | `LANGUAGE_SUPPORT` | 来自 sealed Policy source class |
| `UNSUPPORTED_ENTRY_KIND` | `LANGUAGE_SUPPORT` | 来自 frozen Profile entry-kind rule |
| `UNSUPPORTED_LANGUAGE` | `LANGUAGE_SUPPORT` | 来自 frozen Profile language/raw-path rule |
| `UNSUPPORTED_SOURCE_ENCODING` | `LANGUAGE_SUPPORT` | 来自 exact bytes 与 frozen encoding semantics |
| `UNSUPPORTED_SYNTAX_VERSION` | `PARSE` | 只有 parser/version discrimination contract 才能解释 |
| `PARSE_ERROR` | `PARSE` | 来自实际 parser execution |

本文不替 Parse 解决 `UNSUPPORTED_SYNTAX_VERSION` 与普通 `PARSE_ERROR` 怎样机械区分；它只禁止 Language
Support 提前拥有该结论。现有 Schema 的跨 stage 宽松接受是待后继合同/Schema 修正的边界，不是当前实现许可。

## 7. exactly-one terminal disposition proof

下一合同必须让 application 对 exact denominator 机械复核：

```text
denominator members
    = eligible members U unsupported members

eligible ∩ unsupported
    = empty
```

并且：

- 每个 denominator member 恰好出现一次；
- 任何遗漏、重复、额外 path 或跨 exact-world transplant 都必须拒绝；
- 每个 unsupported member 的 reason set 必须非空、唯一、按 frozen rank 排序且等于全部适用失败理由；
- eligible member 不得携带 unsupported reason；
- `OUT_OF_SCOPE` item 不得借 path 相同混入本 stage；
- path ref 必须回连同一个 exact inventory item、Policy decision、Profile 与 function identity。

这是一份 composition proof，不是 Provider receipt。application 可以复算并核账，但不能修改 denominator、补猜
失败理由或把缺失 item 默认为 eligible。

## 8. semantic reuse 与 attempt authority

相同 authoritative semantic inputs 与相同 versioned function 可以在不同 attempt 中机械得到相同 classification。
这允许 semantic result 复算或内容去重，却不产生 continuation authority：

```text
same classification semantics
    !=
same attempt

same canonical result bytes
    !=
right to continue a previous BudgetContext
```

若未来 live pipeline 需要从 Language Support 进入 Parse，continuation 必须继续绑定当前 attempt 的原始 live
authority；另一次 attempt、相同 limits 的新 BudgetContext 或历史 projection 都不能替代。下一合同必须分别定义
semantic binding 与 live continuation binding，不能用一个 digest 同时承担两种职责。

## 9. persistence route 仍然开放

本轮没有发现 execution-time observation 才能决定 Language Support 的事实。于是同一 live attempt 内，exact
bytes + frozen Policy/Profile + versioned total function 足以重算 classification。

但 public SourceSnapshot 只保存 identity/size/hash，不内嵌 blob body。离线 Bundle consumer 是否被保证可以重新
取得 exact Git object bytes，仍然没有合同。因此：

```text
Route A
    live exact inputs + versioned function
    -> on-demand recomputation

Route B
    canonical derived projection
    -> self-contained historical/offline verification
```

两条路线都仍然合法。选择依据必须是 public consumer 的 self-contained verification 与 reacquisition contract，
不能因为工程方便、已有 Schema 形状或“留证据比较安心”就提前选择。即使选择 Route B，projection 也只是
deterministic derived fact，不是 Provider observation receipt。

## 10. Parse consumer boundary

Parse 只能消费当前 exact qualification 中的 `eligible` members，并验证它们仍绑定同一个 exact source world 与
current-attempt continuation。Parse 不得：

- 把 Language Support eligible 偷换成 parse success；
- 回头把 unsupported subject 改成 eligible；
- 重新定义 Language Support denominator 或 reason set；
- 用 parser 能容忍某 encoding 的事实扩大 Profile accepted set；
- 把 `SyntaxError` 反填为 Language Support failure。

反过来，Language Support 也不得运行 parser 来证明 AST、grammar 或 syntax-version compatibility。

## 11. 资格否定矩阵

| ID | 已知世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `LSP-000` | 同一 path ref 在 UTF-8 与 Latin-1 exact worlds 中相同 | path-only 是完整 classification identity |
| `LSP-001` | encoding cookie 检测成功，但 body 含该 codec 下非法 bytes | detection success 等于 whole-source qualification |
| `LSP-002` | `ascii` declaration 合法且当前 bytes 也可按 UTF-8 解码 | decodable 等于 declared encoding 属于 Profile accepted set |
| `LSP-003` | BOM 与 non-UTF-8 cookie 冲突，或 codec unknown | detection error 可以推迟成 Parse failure |
| `LSP-004` | source class、entry kind、language 与 encoding 可同时失败 | Schema-valid first reason 等于完整 classification |
| `LSP-005` | unsupported entry kind 没有可读 blob body | complete reason set 要求对不适用 encoding predicate 编造结果 |
| `LSP-006` | Python 3.13-only syntax与普通 invalid syntax在 Python 3.10 parser 下都失败 | Language Support 有资格声明 `UNSUPPORTED_SYNTAX_VERSION` |
| `LSP-007` | 同一 semantic classification 在另一 attempt 被复算 | semantic equality 继承 live continuation authority |
| `LSP-008` | live exact inputs 足以重算 | public/offline consumer 必然拥有 exact blob reacquisition authority |

## 12. 审计实证

仓库外 audit-only script 在 Python 3.10.6 / 3.13.13、normal / `-O` 四个独立进程中生成逐字节相同的 canonical
report：

```text
sha256 = 5666fcda8e61e16664cc46f01e12778499c56b8d56f4638e32dd08e3acc6615c
bytes  = 4404
```

报告覆盖：

- default UTF-8、UTF-8 cookie/alias、UTF-8 BOM 与 BOM/cookie 一致；
- explicit ASCII、Latin-1、第二行有效/无效 cookie；
- invalid UTF-8 body、检测成功后 full decode failure、unknown codec 与 BOM/cookie conflict；
- Python 3.13-only syntax 与普通 invalid syntax 的同类 parse failure；
- complete reason set、first-only reason、syntax reason 两种 stage placement 均 Schema-valid；
- same path ref 跨不同 exact source/policy worlds 保持相同。

四格一致只证明本次 falsifier projection 稳定，不发布产品 classifier。audit script 与 reports 保留在仓库外，
最终 diff 不包含临时 Artifact。

## 13. 下一合同的最小边界

本审计允许下一份 docs-only contract 只冻结：

```text
Language Support semantic input identity
versioned Python 3.10 encoding qualification algorithm
predicate applicability graph
complete canonical reason composition
stage-reason ownership
exactly-one terminal composition proof
semantic result / live continuation separation
Parse consumer boundary
```

合同仍须把 persistence route 保持为显式决策点；若 public/offline self-contained verification 尚未定义，不能顺手
新增 public carrier。

仍然禁止：

```text
classifier / parser / AST / Fact runtime
shared ObservationReceipt / FulfillmentLedger
public Schema / compatibility corpus / identity-vector changes
ReviewSliceSet / CoverageLedger runtime
Evidence / Manifest / publisher / Bundle
Attention / CLI / Workbench
```

## 14. 候选闭环门

本文只有在以下条件全部成立后，才有资格成为 precontract-audit history：

1. `LSP-000..008` 可由本基线 frozen materials、current Schema 与 audit-only worlds 独立复核；
2. Python 3.10 / 3.13、normal / `-O` canonical reports 逐字节一致；
3. 官方 Python 3.10 encoding semantics 与宿主 audit oracle 的角色已明确分开；
4. 文档 120/132/137/155/160/175/190/194/195/196 的 authority claim 没有被扩大或推翻；
5. README、AGENTS 与 milestones 只同步候选 precontract boundary，不发布合同或实现状态；
6. diff 只包含本文与三处导航/状态同步，链接、敏感路径、UTF-8 与 `git diff --check` 成立；
7. 候选 PR original required checks 全部成功并经受保护主线合入；
8. 新 exact main Public CI 与 Browser Smoke 成立。

第 7–8 项完成以前，当前公开主线状态不变。即使本候选闭合，下一步也只能从新的 exact main 起草 Language
Support 最小合同；不得直接实现 classifier、Parse、Fact、ReviewSliceSet、Coverage、publisher 或 Bundle。

上述条件现已闭合。PR #206 保留 original Python 3.10 正式失败；独立 PR #207 只修复 test-support 重复 acquisition
拓扑，不放宽产品 30 秒预算，也不共享 attempt authority。语义补丁随后从 maintenance-qualified
`main@36c82c9c5445b83c33e714c1288d79d27e1fe2bb` 以相同 patch-id 重建为 PR #208，并取得：

```text
PR #208 Public CI     36190024077  pull_request / attempt 1  11/11 SUCCESS
candidate merge      de4eee7e953a0b95d52b973bee35a033e3901254
Public CI             36192106963  push / attempt 1          11/11 SUCCESS
Browser Smoke         36192106965  push / attempt 1           1/1 SUCCESS
```

因此本文现在是 `PRECONTRACT_AUDITED` 历史，只授权文档 198 的 docs-only semantic contract candidate。旧失败、
maintenance 与新候选资格仍是三条独立事实链；本文不因此授权 classifier、Parse、Fact、Coverage、Schema、
publisher 或 Bundle。
