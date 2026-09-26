# R1 Language Support Qualification codec-conformance 修正合同 0.2

日期：2026-09-26

> 状态目标（仅[独立冻结发布](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)最后门闭合后生效）：
> `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 候选基线：`main@41bd7cd3d6d486c780aeda91b86ae8845ef90ae7`
>
> 本文是语义合同；冻结状态仅在文档 203 的最后门闭合后生效。本文不是 classifier、carrier、Schema、测试、fixture 或 runtime 实现。

## 1. 目的与停止线

[文档 198](198-r1-language-support-qualification-contract.md)冻结的
`r1-python-language-support/0.1` 要求在 Profile accepted-set membership 以前，对任意 frozen-known codec
执行 whole-source decode。[文档 200](200-r1-language-support-private-implementation-feasibility-audit.md)证明：当前
最小 private implementation boundary 不拥有完整 CPython 3.10.6 decoder surface，也没有逐输入证明宿主 decoder
等价的 authority。[文档 201](201-r1-language-support-codec-conformance-correction-precontract-audit.md)进一步完成
四类世界 partition，选择显式 function version bump：对当前只接受 `UTF-8 / UTF-8-SIG` 的 frozen Profile，
non-accepted whole-source decode 不改变 Language Support terminal projection，因此不应扩张最小实现面。

本文只冻结一个新的确定性 qualification function：

```text
r1-python-language-support/0.2
```

它保持 0.1 的 denominator、predicate applicability、complete reason composition、exactly-one closure、stage ownership、
semantic-result / live-authority separation 与 eligible-only Parse boundary；只修正 versioned function identity、适用的
Profile compatibility domain 与 source-encoding pipeline。

本文不修改 0.1 历史字节，不选择 persistence，不创建 public object，也不授权实现。即使本候选以后冻结，代码施工
仍须从新的 exact main 重新进入 CONTROL LOOP，不能从合同文字自动取得资格。

## 2. 与 frozen 0.1 的规范关系

### 2.1 0.1 保持历史身份

0.1 的规范正文继续固定为：

```text
path       = docs/198-r1-language-support-qualification-contract.md
git blob   = 5a0145629edf427cd873f525e75f486218d6896e
sha256     = e4b70878359d1b9ffae9f82884eddd67981d4bded9b1bdadba58a3ea04a8bede
function   = r1-python-language-support/0.1
state      = FROZEN historical identity
```

本文不得被解释为：

```text
0.1 的 normative order 从未存在
0.1 已被实现
0.1 的历史 classification 自动继承给 0.2
```

### 2.2 0.2 是有界 delta contract

0.2 继承 0.1 中下列语义：

```text
denominator authority and exact history binding
canonical subject payload fields, except function identity
predicate applicability outside the encoding algorithm
complete canonical failed-reason composition
exactly-one denominator closure
stage-reason ownership
semantic result != live continuation authority
eligible-only Parse consumer boundary
persistence as a non-decision
```

本文第 3–7 节替换 0.1 的：

```text
function identity
function/Profile compatibility
accepted UTF-8 equivalence resolver
source-encoding pipeline order
whole-source decode applicability
```

只有上述显式 delta 具有优先级。本文没有重复写出的 0.1 语义不得被实现者重新解释；若 delta 与 inherited semantics
出现无法机械消解的冲突，0.2 qualification 不成立，不能由调用者选择“看起来更方便”的解释。

## 3. authority 与 compatibility domain

### 3.1 Profile authority

Profile 继续拥有：

```text
language
language_semantics
supported_entry_kinds
accepted_source_encodings
normalization_rules.path
```

它不拥有 cookie/BOM detection algorithm、alias resolution implementation、host codec registry 或 decoder behavior。

### 3.2 0.2 function authority

0.2 function 拥有：

```text
Python 3.10 cookie/BOM detection semantics
accepted UTF-8 equivalence resolver
BOM/cookie conflict rule
whole-source decode applicability
canonical UTF-8 / UTF-8-SIG result
source-encoding predicate terminal result
```

Provider 与宿主 Python 只提供执行能力，不能改变这些规则。

### 3.3 exact compatibility predicate

0.2 只适用于同时满足以下条件的 Profile：

```text
language == PYTHON
language_semantics == PYTHON_3_10
canonical accepted_source_encodings == {UTF-8, UTF-8-SIG}
```

accepted set 的顺序或重复不改变 canonical set；任何额外、缺失或无法 canonicalize 的 encoding 都使
function/Profile compatibility 失败。compatibility failure 使**整个 Language Support qualification 不成立**，不得：

```text
把所有 subject 标为 unsupported
把新增 encoding 交给 ambient codec registry
静默回退到 0.1
由 Provider 自选另一个 function
```

未来 Profile 若接受新的 codec，必须取得新的 compatibility authority；0.2 不自动扩张。

## 4. semantic identity

0.2 沿用 0.1 第 4 节的 subject payload 含义，只把：

```text
language_support_function = r1-python-language-support/0.1
```

替换为：

```text
language_support_function = r1-python-language-support/0.2
```

因此：

```text
same exact subject + same terminal disposition + same reasons
    under 0.1 and 0.2
    != same semantic classification identity
```

完整 Snapshot / Policy / Profile history binding 仍须逐次核账。function identity 不包含 attempt、BudgetContext、deadline
或 live continuation；相同 0.2 semantic result 也不继承另一 attempt 的执行权。

## 5. versioned accepted UTF-8 resolver

### 5.1 规范来源

0.2 继续使用 Python 3.10 encoding declarations 与 PEP 263 作为语言语义来源，并把 CPython 3.10.6 的：

```text
Lib/tokenize.py
Lib/encodings/__init__.py
Lib/encodings/aliases.py
Lib/encodings/utf_8.py
```

作为 cookie placement、`_get_normal_name()`、name normalization、alias resolution 与 UTF-8 behavior 的
conformance reference。它们是 versioned rule source，不是“调用当前宿主 API 即合格”的许可。

locale、平台默认编码、当前解释器 patch version、Provider tolerance 与 ambient codec registry 都不得改变结果。

### 5.2 detection projection

对 encoding predicate 适用的 exact blob bytes，0.2 必须保持 CPython 3.10.6 的：

1. UTF-8 BOM detection；
2. first physical line cookie placement；
3. 只有第一行满足 blank/comment-only 条件时才检查第二行；
4. coding token grammar；
5. `_get_normal_name()` special normalization；
6. BOM/cookie conflict 判断。

普通代码后的第二行 cookie 不生效。无 BOM、无有效 declaration 时，effective encoding 是 `UTF-8`。检测失败形成
source-encoding predicate failure，不获得 Parse authority。

### 5.3 closed accepted-equivalence resolution

无 BOM 且存在 declaration 时，0.2 只回答一个有界问题：

> 该 token 在 CPython 3.10.6 的规范路径下，是否属于 canonical `utf_8` accepted class？

resolver 必须保持以下顺序与差异：

```text
token
    -> CPython 3.10.6 _get_normal_name()
    -> CPython 3.10.6 encodings.normalize_encoding()
    -> ASCII lowercase codec search key
    -> exact alias key lookup
    -> alias dotted-fallback lookup
    -> direct canonical module check without dotted fallback
    -> accepted UTF-8 class or non-accepted
```

对当前 closed class，该顺序等价冻结为：

```text
name = _get_normal_name(token)
key = ascii_lower(encodings.normalize_encoding(name))
alias_target = aliases.get(key) or aliases.get(key.replace('.', '_'))
resolved_module = alias_target if alias_target exists else key

accepted iff resolved_module == utf_8
             and resolved_module contains no dot
```

这里的 `aliases` 是 CPython 3.10.6 frozen alias table；application 不导入或探测任何其他 codec module。

它可以用 frozen table、等价纯函数或其他可复核实现，但不能调用 ambient `codecs.lookup()` 后把成功当作 authority。
至少必须保持：

```text
no BOM + cp65001       -> accepted UTF-8 alias
no BOM + CP65001       -> accepted UTF-8 alias after search-key case fold
no BOM + u8            -> accepted UTF-8 alias
no BOM + utf           -> accepted UTF-8 alias
no BOM + utf8          -> accepted UTF-8 alias
no BOM + UTF8          -> accepted UTF-8 alias after search-key case fold
no BOM + utf8_ucs2     -> accepted UTF-8 alias
no BOM + utf8_ucs4     -> accepted UTF-8 alias
no BOM + utf-8-sig     -> _get_normal_name == utf-8
                       -> accepted UTF-8
no BOM + utf.8         -> non-accepted
```

`utf.8` 不能通过 `norm.replace('.', '_') == utf_8` 获得 direct-module success；CPython 3.10.6 的 dotted fallback
只用于 alias key lookup。

### 5.4 BOM conflict identity

有 BOM 且存在 declaration 时，consistency 使用 CPython 3.10.6 `_get_normal_name()` result，不使用
`CodecInfo.name` 或后继 alias target。因此：

```text
BOM + cp65001     -> conflict / unsupported
BOM + utf8        -> conflict / unsupported
BOM + utf-8-sig   -> _get_normal_name == utf-8
                  -> consistent UTF-8-SIG
```

有 BOM 且无 cookie，或 cookie 在该规则下与 BOM 一致时，canonical effective encoding 是 `UTF-8-SIG`；BOM 必须由
strict decoder 消费，不能作为 source character 交给 Parse。

## 6. corrected total pipeline

当 source-encoding predicate 适用时，0.2 必须按以下顺序处理：

```text
1. validate exact function/Profile compatibility
2. verify exact owned blob bytes against inventory identity, size and hash
3. detect BOM and Python 3.10 first/second-line declaration
4. reject detection failure or BOM/cookie conflict
5. resolve only membership in the versioned accepted UTF-8 equivalence class
6. reject non-accepted declaration without ambient lookup or whole-source decode
7. choose canonical UTF-8 or UTF-8-SIG effective encoding
8. strict-decode the whole source with the selected accepted decoder
9. emit the encoding predicate result
10. compose it with every other applicable Language Support predicate
```

Accepted whole-source decode 固定为：

```text
UTF-8
    -> strict UTF-8 decode of all exact blob bytes

UTF-8-SIG
    -> require the detected BOM
    -> consume that BOM
    -> strict UTF-8 decode of all remaining exact blob bytes
```

strict decode failure 贡献 `UNSUPPORTED_SOURCE_ENCODING`。non-accepted token 不需要判断它在宿主上“known/unknown”，
也不执行对应 decoder；known、unknown、decoder-would-pass 与 decoder-would-fail 在当前 compatibility domain 都投影为
同一 failed encoding predicate。

## 7. terminal equivalence 与 version distinction

在第 3.3 节 compatibility domain 内，对任意 bounded exact blob bytes，0.1 与 0.2 的 Language Support terminal
projection 可分为四类：

| world | 0.1 | 0.2 | terminal relation |
| --- | --- | --- | --- |
| detection failure | unsupported | unsupported | equal |
| BOM/cookie conflict | unsupported | unsupported | equal |
| effective encoding non-accepted | decode 后仍 unsupported | 不 decode，直接 unsupported | equal |
| accepted UTF-8 / UTF-8-SIG | strict whole-source decode | 同一 strict decode | equal |

该 partition 是 correction direction 的全称语义依据。文档 201 的 136,228-world 四格 report 只提供 falsifier witness，
不能替代这项 partition，也不能把 finite corpus 变成规范来源。

同时必须保持：

```text
terminal projection equality
    != algorithm identity equality
    != contract identity equality
    != historical authority inheritance
```

0.2 不是“更宽松的 0.1 实现”；它是显式改变 normative order 的新函数版本。

## 8. inherited composition 与 closure

0.2 完整继承 0.1 的 applicability graph 与 reason rank：

```text
UNCLASSIFIED_SOURCE
UNSUPPORTED_ENTRY_KIND
UNSUPPORTED_LANGUAGE
UNSUPPORTED_SOURCE_ENCODING
```

source-encoding predicate 仍只在 entry-kind predicate 与 language/path predicate 通过时适用；source-class failure
不短路其他独立 applicable predicates。所有 applicable 且失败的 reasons 必须完整保存并按 frozen rank canonicalize，
不能把 0.2 的 pipeline order误作 first-failure precedence。

每个 denominator member 仍必须恰好进入：

```text
eligible

or

unsupported(reason_codes = complete canonical failed reasons)
```

并机械证明：

```text
denominator = eligible U unsupported
eligible intersection unsupported = empty
```

compatibility、input identity、integrity binding 或 function identity 不成立时，整个 qualification 失败；不得新增
per-subject `unknown / unseen / not_run`，也不得把 infrastructure failure 改写为 `unsupported`。

## 9. stage ownership 与 Parse boundary

0.2 不改变 reason owner：

| Reason | Owner stage |
| --- | --- |
| `POLICY_EXCLUDED` | `POLICY_SCOPE` |
| `UNCLASSIFIED_SOURCE` | `LANGUAGE_SUPPORT` |
| `UNSUPPORTED_ENTRY_KIND` | `LANGUAGE_SUPPORT` |
| `UNSUPPORTED_LANGUAGE` | `LANGUAGE_SUPPORT` |
| `UNSUPPORTED_SOURCE_ENCODING` | `LANGUAGE_SUPPORT` |
| `UNSUPPORTED_SYNTAX_VERSION` | `PARSE` |
| `PARSE_ERROR` | `PARSE` |

Language Support 不运行 parser、不生成 AST、不解释 syntax failure。Parse 只能消费当前 exact 0.2 qualification 的
eligible members，并须另外证明同一 exact history、同一 function identity 与当前 attempt 的独占 live continuation。

```text
0.2 eligible
    != parse success
    != another attempt's continuation authority
```

## 10. persistence 保持 non-decision

0.2 classification 仍是 deterministic derived fact。本文不在下列路线中作选择：

```text
Route A
    exact live inputs + 0.2 function
    -> same-attempt recomputation

Route B
    canonical derived projection
    -> historical/offline consumption
```

Bundle consumer 是否拥有 exact Git object reacquisition authority、是否需要 self-contained projection，以及 derived
bytes 是否进入 future public Schema，均不由本合同决定。

## 11. falsifier matrix

| ID | world | 必须拒绝的错误推理 |
| --- | --- | --- |
| `LSC2-000` | 0.1 与 0.2 terminal bytes 相同 | 可以静默修改 0.1 或继承其历史 authority |
| `LSC2-001` | `windows-31j` 在宿主版本间 lookup 漂移 | ambient registry 可拥有 0.2 resolver authority |
| `LSC2-002` | `utf.8` 经 naive dotted replacement 变成 `utf_8` | 字符串接近等于 CPython 3.10 direct module success |
| `LSC2-003` | no-BOM `cp65001 / CP65001 / UTF8` accepted | accepted alias 必须依赖全 codec decoder surface，或可省略 search-key case fold |
| `LSC2-004` | BOM `cp65001` / `utf8` conflict | `CodecInfo.name == utf-8` 足以证明 BOM consistency |
| `LSC2-005` | non-accepted bytes 在某宿主可成功 decode | decoder success 可扩大 Profile accepted set |
| `LSC2-006` | accepted UTF-8 body 含 invalid trailing bytes | cookie detection success 等于 whole-source eligibility |
| `LSC2-007` | Profile 新增 accepted codec | 0.2 可静默扩张 compatibility domain |
| `LSC2-008` | compatibility/input integrity failure | 可把所有 member 标成 unsupported 后继续 |
| `LSC2-009` | same 0.2 classification in two attempts | semantic equality 可继承 BudgetContext / Parse authority |
| `LSC2-010` | finite corpus 零 mismatch | corpus 已证明所有 bounded byte worlds |
| `LSC2-011` | 0.2 eligible member | Language Support 已证明 parser success |

这些 falsifiers 冻结拒绝边界，不预造 public enum、test class、carrier 或 persistence format。

## 12. 明确 non-decisions

本文不决定或授权：

```text
private classifier / carrier class shape
request projection or ProviderRun changes
persistence Route A/B
public Schema / corpus / identity-vector changes
historical/offline blob reacquisition
real parser / AST / Fact Provider
Parse or Fact fulfillment contracts
shared receipt / ledger
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
Attention / CLI / Workbench / Core / Q / O / T
```

## 13. 后继实现边界

本候选冻结以前不授权代码。若独立 freeze publication 最终成立，后继仍须从新的 exact main 重新审计最小 private
implementation boundary；最多可以重新考虑：

```text
exact input/history validation
0.2 compatibility gate
versioned accepted UTF-8 resolver
strict accepted-source decoder
complete per-subject composition
exactly-one closure validation
private same-attempt Parse gate proof
LSC2-000..011 hardening
```

该列表不是施工授权。若 private proof 必须先选择 persistence、修改 public identity、运行 real parser，或取得
Fact/Coverage authority 才能成立，必须停止并把反例反馈给对应最小边界。

## 14. 候选历史与冻结门

### 14.1 候选资格历史

本候选只允许修改：

```text
this contract candidate
README navigation / current projection
AGENTS exact boundary
milestones history
```

最终字节已经通过本层声明的 docs/link/boundary gates、PR #214 original required checks、受保护主线合入、
new exact-main Public CI / Browser Smoke，以及 README、本文与 milestones 的 fresh installed-product public
readback 和 independent byte/state reconciliation。因此：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_CANDIDATE
```

已成为 qualified history。精确坐标、Plan/session 与 manifest 摘要由
[独立冻结发布](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)保存；candidate qualification
仍不等于 frozen。

### 14.2 独立 freeze publication

candidate-qualified 以后，仍须由[独立 docs-only freeze publication](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)：

1. 保存 0.1 frozen identity 与本文 candidate qualification；
2. 明确发布 `r1-python-language-support/0.2`，不倒写 0.1；
3. 通过自己的 original PR gates、受保护合入与 new exact-main 双门；
4. 重新完成 fresh installed-product public readback 与独立 byte/state reconciliation。

最后一门以前，不得发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
```

也不得启动实现。

## 15. 合同原则

本合同把修正原则压成：

> A versioned qualification function should own only the semantic distinctions its stage can observe and is
> authorized to decide; changing the normative path requires a new identity even when terminal projections agree.

中文：**版本化资格函数只应拥有本 stage 可观察且有权裁决的语义区分；即使终态投影一致，修改规范路径也必须取得
新的身份。**
