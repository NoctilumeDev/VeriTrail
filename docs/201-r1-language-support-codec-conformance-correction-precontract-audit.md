# R1 Language Support codec-conformance 修正前置审计

日期：2026-09-26

## 1. 审计对象与结论

本文从：

```text
main = 943300a4d6b3d708be8f4196cc0ee67a86eee64b
tree = 1eee915760809d9bc07ee06938d01bc3ab139863
```

重新读取[文档 198](198-r1-language-support-qualification-contract.md)第 5、13 节与
[文档 200](200-r1-language-support-private-implementation-feasibility-audit.md)的两条候选路线。

文档 200 已证明：保持 `r1-python-language-support/0.1` 的 frozen order，需要拥有 CPython 3.10.6
整个 frozen-known codec decoder surface，或者对每一个 exact input 独立证明宿主 decoder 等价；当前最小
private implementation boundary 没有这项 authority。

本轮进一步证明：对当前 frozen Profile 的 exact accepted set：

```text
{UTF-8, UTF-8-SIG}
```

non-accepted codec 的 whole-source decode 不改变 Language Support 0.1 的 terminal disposition 或 canonical reason。
因此保留完整 decoder surface 没有为本 stage 增加可观察区分力，却扩张了 implementation authority。

本审计选择文档 200 的 Route B：后继应以**新 function identity**起草最小修正合同，把 accepted-set rejection
放在 non-accepted whole-source decode 之前。`0.1` 继续作为已冻结历史合同存在，不能倒写；新合同尚未起草，
classifier、carrier 与 runtime 仍未获授权。

```text
contract 0.1
    FROZEN historical identity
    NOT silently modified

correction direction
    explicit function version bump
    AUTHORIZED TO DRAFT

contract 0.2 candidate
    NOT STARTED

implementation
    NOT STARTED / NOT AUTHORIZED
```

## 2. exact-main 前态

文档 200 的 PR #212 original Public CI、受保护合入与 new exact-main gates 已闭合：

```text
Public CI     36243585555 attempt 1 = 11/11 SUCCESS
Browser Smoke 36243585552 attempt 1 =  1/1  SUCCESS
```

所以本轮不是继续候选分支上的旧推理，而是从新的 qualified exact main 重新执行控制回路。当前公开事实仍是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_NOT_STARTED
```

三个开放 Dependabot PR 不拥有本 seam 的合同 authority，也没有改变 exact main。

## 3. 先分开三种 authority

### 3.1 Profile authority

Profile 拥有：

```text
accepted_source_encodings = {UTF-8, UTF-8-SIG}
language_semantics = PYTHON_3_10
```

它不拥有 detection algorithm、codec lookup implementation 或 host decoder registry。

### 3.2 function authority

versioned Language Support function 拥有：

```text
cookie / BOM detection semantics
accepted encoding equivalence
whole-source decode rule for possibly eligible inputs
terminal classification composition
```

如果 normative pipeline order 改变，必须改变 function identity；相同 coarse reason 不能掩盖算法版本变化。

### 3.3 host capability

宿主 Python 可以提供执行能力，但：

```text
host lookup success
    != frozen lookup authority

host decoder availability
    != right to expand the accepted semantic surface
```

`windows-31j` 已证明 ambient registry 会漂移。新修正不能重新把宿主 registry 当成规范来源。

## 4. 为什么 Route A 不再是最小路线

`0.1` 对 source-encoding predicate 的所有内部失败统一贡献：

```text
UNSUPPORTED_SOURCE_ENCODING
```

其中包括：

```text
declaration detection failure
unknown codec
BOM / cookie conflict
whole-source decode failure
accepted-set miss
```

对任意 denominator member，令 `E` 为 effective encoding，`S` 为 Profile accepted set。`0.1` 的 terminal
classification 可以按四类世界拆开：

1. detection 失败：`unsupported`；
2. BOM / cookie conflict：`unsupported`；
3. `E` 不属于 `S`：无论 decode 成功或失败，最终仍是 `unsupported`；
4. `E` 属于 `S`：只有 strict whole-source decode 成功才 `eligible`。

Route A 在第 3 类世界继续执行 non-accepted decoder，但 decoder 的成功、失败与 decoded text 都不会改变本 stage 的
terminal result。要让这条不可观察路径跨 3.10/3.13 host 合格，反而需要：

```text
full version-bound lookup
full version-bound decoder substrate
platform-dependent codec handling
per-input conformance proof
```

这不是说不可观察内部路径永远不应冻结；若它承担 side-effect、security、resource 或下游语义，仍可能是必要合同。
但当前 stage 禁止把 decoded non-accepted text 交给 Parse，也不公开内部 failure shape。Route A 因此不是当前最小
authority surface。

## 5. Route B 的全称终态等价

新版本必须先保留与 `0.1` 相同的 Python 3.10 detection 与 BOM-conflict 语义，再只判断 declaration 是否属于
当前 accepted UTF-8 等价类：

```text
detection failure
    -> unsupported

BOM conflict under Python 3.10 token normalization
    -> unsupported

effective encoding outside accepted UTF-8 equivalence class
    -> unsupported without whole-source decode

effective encoding inside accepted UTF-8 equivalence class
    -> strict UTF-8 / UTF-8-SIG whole-source decode
    -> eligible or unsupported
```

因此四类世界逐一保持 `0.1` terminal projection：

| world | 0.1 | corrected version | relation |
| --- | --- | --- | --- |
| detection failure | unsupported | unsupported | same |
| BOM conflict | unsupported | unsupported | same |
| non-accepted effective encoding | decode 后仍 unsupported | 直接 unsupported | same terminal result |
| accepted UTF-8 effective encoding | strict decode | 同一 strict decode | same |

这个证明依赖当前 exact accepted set 与 coarse reason semantics。未来 Profile 若接受新的 codec，不能自动复用该函数；
必须取得新的 function/Profile compatibility authority。

```text
same terminal classification
    != same algorithm identity

total terminal equivalence
    + explicit version bump
    -> correction route may be drafted
```

## 6. accepted UTF-8 闭集仍需精确版本化

修正不需要模拟整个 CPython codec universe，但也不能把字符串看起来像 UTF-8 当作资格。

CPython 3.10.6 的 relevant surface 包括：

1. `tokenize.cookie_re / blank_re` 的 first/second physical-line placement；
2. `_get_normal_name()` 的 first-12-character special normalization；
3. `encodings.normalize_encoding()`；
4. canonical module `utf_8`；
5. 3.10.6 alias keys `cp65001 / u8 / utf / utf8 / utf8_ucs2 / utf8_ucs4`；
6. alias lookup 的 dotted fallback 与 direct module lookup 的不同顺序；
7. BOM conflict 使用 `_get_normal_name()` 的 result，而不是 `CodecInfo.name`。

所以：

```text
no BOM + cp65001
    -> accepted UTF-8 alias

BOM + cp65001
    -> conflict / unsupported

BOM + utf8
    -> conflict / unsupported

BOM + utf-8-sig
    -> _get_normal_name == utf-8
    -> accepted UTF-8-SIG

utf.8
    -> unsupported
```

`utf.8` 是本轮实际打出的反例。naive resolver 若把 `norm.replace('.', '_') == utf_8` 当成 direct module success，
会错误接受它；CPython 只对 alias table 做 dotted fallback，不能用该 fallback 直接导入 canonical module。

## 7. 审计执行与首败保留

### 7.1 invalid harness observation

第一次 136,228-world audit 把 Python raw regex 中的 `\t / \f / \w` 又多转义了一层，cookie 没有按 CPython
规则匹配，产生 20,270 个 mismatch，其中 `BOM + utf8 / cp65001` 被错误走到 default `UTF-8-SIG`。

```text
3.10 report sha256 = 4149452217c93ee35077a61f2cb284c635113a9bb5bcbac5be342d8889489d80
3.13 report sha256 = 83164cd33d5b13c37dd4a81d57a2e2db4c74eaacd50935ad35c9561a535c1fa
classification      = INVALID_AUDIT_HARNESS
```

该 observation 不是产品或合同反例，也不能被后继 PASS 改写成“从未失败”。

### 7.2 valid harness 打出的 resolver counterexample

修正 regex 后，第二次观察仍有 10 个 mismatch，全部来自 `utf.8` 的 accepted-alias 错误。这个失败属于拟议
resolver semantics；它使 naive closed-set algorithm 失去资格，随后只修正 alias/direct-module lookup 顺序。

```text
3.10 report sha256 = 236f91b2bb5aba1025c68514b0bd20bffc6e5d170025bb3375f66fae3664b759
3.13 report sha256 = 25349c6fd83a89ca9513d9132b712480a1c4fd8f05717b241ae011b27d88edf7
mismatch_count      = 10
classification      = VALID_COUNTEREXAMPLE
```

### 7.3 corrected witness

最终 audit-only resolver 固定上述 3.10.6 accepted UTF-8 surface。136,228 个 byte worlds 在：

```text
Python 3.10 normal
Python 3.10 -O
Python 3.13 normal
Python 3.13 -O
```

得到逐字节相同 canonical report：

```text
report sha256              = 03b540bcbf2cccd2f2d43f6b8287e2821168337503405d09abf7a0935a8cdc03
terminal digest            = b7ec84502db8e2f506c866748f85a4d3c0f8fb974116736f738c27cddfbe3f7a
worlds                     = 136228
reference mismatch count   = 0
ELIGIBLE_UTF-8             = 7217
ELIGIBLE_UTF-8-SIG         = 26
UNSUPPORTED                = 128985
```

该 corpus 仍只是 witness，不是全称证明。Route B 的 authority 来自第 5 节的 case partition；corpus 用于打实现草案
反例并证明四格 determinism，不能取代合同论证。

## 8. 后继修正合同的最小面

后继可以起草一个新的 Language Support function version，但合同面最多包括：

```text
new function identity
exact compatibility with accepted set {UTF-8, UTF-8-SIG}
Python 3.10 cookie/BOM placement
versioned accepted UTF-8 equivalence resolver
exact BOM conflict semantics
strict whole-source UTF-8 / UTF-8-SIG decode for possibly eligible inputs
same complete reason composition
same exactly-one denominator closure
same semantic-result / live-authority separation
same eligible-only Parse consumer boundary
```

必须明确：

- non-accepted declaration 不调用 ambient lookup 或 decoder；
- accepted UTF-8 resolver 是 versioned rule，不是 host `codecs.lookup()` 成功；
- accepted set 与函数 compatibility 不成立时，整个 qualification 不成立，不能把它改写成 per-subject unsupported；
- `0.1` 与新版本拥有不同 semantic identity，即使某些输出字节相同也不能互相继承历史 authority。

## 9. 本轮没有决定的事情

本文不决定：

```text
private classifier / carrier class shape
persistence Route A/B
public Schema or new fields
historical/offline blob reacquisition
Parse execution / outcome
Fact universe / fulfillment
shared receipt / ledger
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
```

它也不发布 `0.2` 合同正文。下一步只有在本文自己的资格链闭合后，才能从新的 exact main 起草最小 contract
correction candidate。

## 10. falsifier matrix

| ID | world | 拒绝的错误推理 |
| --- | --- | --- |
| `LSC-000` | regex 被双重转义，20,270 mismatches | audit harness 输出天然拥有产品 authority |
| `LSC-001` | `utf.8` 被 naive dotted fallback 接受 | normalized spelling 接近等于 CPython 3.10 lookup success |
| `LSC-002` | no-BOM `cp65001` accepted，BOM `cp65001` conflict | `CodecInfo.name == utf-8` 足以决定 BOM consistency |
| `LSC-003` | `windows-31j` host lookup 漂移但始终 non-accepted | ambient registry 可拥有 correction rule authority |
| `LSC-004` | non-accepted decoder success/failure 都投影为同一 reason | 不可观察 decoder path 自动值得扩张最小实现面 |
| `LSC-005` | 136,228 worlds 四格零 mismatch | finite corpus 等于全称终态证明 |
| `LSC-006` | function identity 改变但 terminal bytes 相同 | terminal equality 允许静默改写 0.1 |
| `LSC-007` | future Profile 接受新 codec | 当前 UTF-8-only function 可自动扩张 compatibility |

## 11. stop line

本文自己的 original PR、受保护合入与 new exact-main Public CI / Browser Smoke 成立后，最多发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步最多起草最小 `r1-python-language-support/0.2` correction contract candidate。不得在本 PR 中：

```text
modify contract 0.1 bytes or historical identity
publish or freeze contract 0.2
implement classifier / carrier / request projection
choose persistence
run Parse / AST / Fact Provider
change public Schema / corpus / identity vectors
add shared receipt / ledger
start ReviewSliceSet / Coverage
change Evidence / Manifest / publisher / Bundle
```

## 12. 本候选的资格门

本候选只允许修改：

```text
this audit document
README navigation / current projection
AGENTS exact boundary
milestones history
```

最终字节必须重新通过 docs/link/boundary gates 与 Public CI。受保护合入后，new exact main 还必须独立通过
Public CI 与 Browser Smoke；在此以前，Route B 只是 audit candidate，不能声称 precontract audited，更不能开始
0.2 contract 或 runtime。
