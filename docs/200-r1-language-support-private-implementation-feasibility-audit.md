# R1 Language Support Qualification private implementation 可行性审计

日期：2026-09-26

## 1. 审计对象与结论

本文从：

```text
main = 791fb093e19165808243258abdad4a1e208dcb70
tree = 5c612426fc616ecff03d240c6da418c8a1037657
```

重新读取[文档 198](198-r1-language-support-qualification-contract.md)第 13 节。该 source state 已满足：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
```

本文不把合同冻结自动升级为实现授权。审计结论是：exact input validation、denominator construction、complete
reason composition、exactly-one closure 与 same-attempt gate 在现有 private architecture 中均有可实现路径；但是
0.1 encoding pipeline 在 accepted-set rejection 以前要求对任意 frozen-known codec 完成 whole-source decode，并要求
宿主 decoder 对当前输入证明与冻结语义等价。当前仓库没有拥有这项证明的 versioned decoder substrate。

因此本文**不授权 private classifier implementation**。下一合法问题只到 codec-conformance 最小合同修正审计：

```text
frozen contract 0.1
    remains historical and authoritative for its exact publication

private implementation
    NOT AUTHORIZED

next legal seam
    versioned codec-conformance / pipeline-order correction audit
```

这不是 persistence、Parse、Fact 或 Coverage 问题；这些边界继续保持未授权。

## 2. exact-main 前态

本轮基准不是聊天摘要。合同发布 `main@cf1b37ab3dfa3bd0569223bb7d59ee94ecf8fc20` 已完成文档 199
声明的 original PR、受保护合入、exact-main Public CI / Browser Smoke、fresh installed-product readback 与独立
reconciliation，因此 `CONTRACT_FROZEN` 已经生效。本地主仓 fast-forward 只属于 housekeeping，不是追加冻结门。

随后 PR #211 只把[证据反馈工作法](working-method.md)接入 always-read `AGENTS.md`；它不修改文档 198 或 R1
runtime。PR #211 original Public CI `36239489966` attempt 1 11/11、受保护合入与本轮 base exact main 的：

```text
Browser Smoke 36240656866 attempt 1 = 1/1 SUCCESS
Public CI     36240656834 attempt 1 = 11/11 SUCCESS
```

均成立。于是本文必须从 `791fb093...` 重新问“最小 private implementation 是否仍是下一合法问题”，不能从
`cf1b37ab...` 的旧判断直接开工。

## 3. 已有结构中可以成立的部分

### 3.1 exact semantic world

`DerivationInputSet` 已 copy-own：

```text
SourceSnapshot canonical bytes
ReviewPolicy canonical bytes
DerivationProfile canonical bytes
verified blob bytes by object identity
five exact digests
```

对象本身不携带 `BudgetContext`、attempt、ProviderRun、continuation 或 mutable repository path。因此同一 immutable
world 可以用于重新计算 semantic classification，而不继承另一次 qualification authority。

### 3.2 denominator 与 composition

现有 validators 已能重新 parse / validate Snapshot、Policy、Profile 与 cross-artifact binding。Language Support
denominator 可以按冻结合同从 terminal inventory 与 exactly-one `IN_SCOPE` Policy decision 构造；四类 predicate 的
applicability、complete failed-reason set、canonical rank 与 exactly-one terminal composition 都可以在 private value
中实现，不需要 public Schema 或 persistence 选择。

### 3.3 live authority

现有 `BudgetContext` 与 `AttemptEligibility` 已提供 controller-owned、不可逆的 live attempt boundary。一个新的
Language Support claim 可以在同一 live attempt 内 one-shot 消费，并把 semantic result 与 continuation authority
分开；相同 classification 不会因此继承另一个 attempt 的 Parse 权力。

这些只是 structural feasibility，不是施工授权。

## 4. current request 不是 Language Support proof

当前 `_execution_cell_application._validate_source_blobs()` 只在：

```text
entry_kind in supported_entry_kinds
and raw_path endswith b".py"
```

时把 path 放入 `supported_paths`。它没有执行 Policy source-class、language semantics、codec resolution 或 whole-source
decode。`build_request_document()` 又把 Snapshot 中每个 blob 的 bytes 都放进 operation request。

因此未来即使增加 classification，也不能只把 eligible path 写进另一个集合，同时继续把所有 bytes 暴露给 Parse
Provider。合同第 10 节要求 Parse 只消费 eligible members；按本项目既有纪律：

```text
available input != authorized input
```

后继若最终获得实现权，必须形成 eligible-only private operation projection，或者同强度地证明 Provider 无法消费
unsupported bytes。它不能靠 Provider 自律或 output filtering 补做 authority boundary。本文不修改现有 frozen
Execution Cell protocol，也不提前选择新 private request shape。

## 5. concrete host lookup drift

审计在本机 CPython 3.10.6 与 Python 3.13.13 上运行同一个 exact world：

```python
# coding: windows-31j
x = "あ"  # body encoded as cp932
```

结果是：

| host | `encodings.aliases['windows_31j']` | detection / decode |
| --- | --- | --- |
| CPython 3.10.6 | absent | `SyntaxError: unknown encoding: windows-31j` |
| Python 3.13.13 | `cp932` | detection and strict decode succeed |

两份 audit-only report 的 SHA-256 为：

```text
3.10 = cdf2c81e5838533ed895e557f05eaac07f5c3bc6a92358d29de6874f274139a3
3.13 = 1d7a75616838a384baff2f9bc8157fa13ed89206c30c903fefeaac4565e60f06
```

该 world 不击穿 0.1：冻结 resolver 应按 CPython 3.10.6 将它分类为 unknown codec，最终贡献
`UNSUPPORTED_SOURCE_ENCODING`。它击穿的是下面这个实现捷径：

```text
call host tokenize.detect_encoding / codecs.lookup
    -> therefore frozen 0.1 lookup was executed
```

宿主 API 只有 capability，没有 rule authority。

## 6. terminal-equivalent reduction 不是合同实现

### 6.1 audit-only reducer

另一个 audit-only function 固定 CPython 3.10 cookie/BOM placement、`_get_normal_name` 与已知 UTF-8 alias subset；
当 token 不可能 canonicalize 为 Profile 接受的 `UTF-8 / UTF-8-SIG` 时，它直接返回
`UNSUPPORTED_SOURCE_ENCODING`，只对可能 eligible 的 UTF-8 world 做 strict whole-source decode。

固定 100,000 个 bounded byte worlds 在：

```text
Python 3.10 normal
Python 3.10 -O
Python 3.13 normal
Python 3.13 -O
```

得到逐字节相同 report：

```text
report sha256       = e96dc9dadb2afd896439d103788a541dece8cfbac2fcacde45a8b6c70769cf0d
corpus count        = 100000
terminal digest     = 60e31791e21cd9d1d889c6cb24c97c59ee4ee6a55cff2139a92acfac92015d3d
mismatch count      = 0
ELIGIBLE_UTF-8      = 716
ELIGIBLE_UTF-8-SIG  = 703
UNSUPPORTED         = 98581
```

### 6.2 它只能证明什么

该结果只证明：在这份 corpus 上，下面两个函数的**终态投影**一致：

```text
0.1 host reference execution
reduced accepted-encoding projection
```

它不能证明 reducer 实现了合同 0.1。reducer 对 non-accepted known codec 没有执行文档 198 §5.2 step 7；而 §5.3
明确禁止因为 public reason 较粗就跳过 whole-source decode。因此：

```text
same terminal classification
    != same frozen algorithm
    != implementation conformance
```

若现在把 reducer 写进 runtime，等于在没有 version bump 的情况下静默修改合同。

## 7. decoder sampling 也不是 total proof

审计还从两个宿主各取 101 个可 lookup codec，每个 codec 使用 2,000 个固定随机 bounded byte strings 比较 strict
decode 的 success/error shape 与 decoded text；本次 common set 未出现差异。

```text
3.10 report sha256 = 59d4d6390129dfa109ad00d23fbf287cedecffcdfdffd391c8aa9e86114d9a51
3.13 report sha256 = 0fc80231821b47ef623632dd4a81d57a2e2db4c74eaacd5095ad6a71e22326eb
common codecs       = 101
sample differences  = 0
```

这项观察只说明 sampled worlds 没有给出 decoder drift 反例。它不能证明：

```text
all frozen-known codecs
x all bounded byte strings
x every supported host
    -> decoder behavior equivalent to the required frozen semantics
```

因此“3.10/3.13 corpus 暂时一致”不能取得文档 198 §5.2 要求的 per-input equivalence authority，更不能把 CI
解释成 codec specification。

### 7.1 frozen 3.10 surface 是有限的，但不是最小的

审计继续枚举本机 CPython 3.10.6 `encodings` package 的 ordinary modules。120 个 module name 均可 lookup；其中：

```text
24 = C-backed MultibyteCodec decoders
 7 = lookupable but non-text codecs
 1 = Windows mbcs platform-bound decoder
```

完整 inventory report：

```text
sha256 = c183cec34c92eef1200fa6ca8d9c8c97e8af879d8be990e7b2864c65323f6437
```

因此把该 surface 叫作“无限 codec universe”并不准确；它是有限集合。但它包含 stateful / multibyte C decoder、
bytes-to-bytes codec，以及 `mbcs` 这类依赖 Windows ANSI code page 的实现。当前 Windows 3.10.6 host 的
preferred encoding 是 `cp936`，`encodings.mbcs` 直接委托 `codecs.mbcs_decode`；对应 audit report：

```text
sha256 = 9147c437aaf8feeb930d7d0ce64db8220e57aed97bc5c5bc4b544f4436bf3904
```

这证明的是 conformance surface 广且异质，并包含平台语义；它仍没有证明两个已采样宿主的 common text decoder
已经实际漂移。

## 8. hidden authority expansion

0.1 的 Profile 只接受 `UTF-8 / UTF-8-SIG`，但 frozen order 是：

```text
resolve every known declaration
    -> whole-source decode with that encoding
    -> accepted-set membership
```

于是一个看似只需要 UTF-8 qualification 的 private classifier，必须额外拥有整个有限但广泛的 frozen-known codec
decoder surface，或者对每一个 exact input 证明宿主 decoder 等价。当前仓库冻结的是 3.10.6 normalization/lookup reference；
没有 frozen decoder table、vendored 3.10 runtime、cross-host per-input oracle 或可由产品独立核验的 decoder identity。

这不是“多写几个 alias”可以解决的问题。直接使用 host decoder 会让 ambient runtime 获得隐藏 authority；vendoring
完整 decoder substrate 又会把本轮从 minimal qualification function 扩张成新的执行依赖。两者都不能由 §13 的
“最多可以考虑”列表自动取得资格。

所以三态问题在当前 exact source 上可以收敛为：

```text
absolute implementability of contract 0.1
    not disproved; a broad version-bound decoder substrate may be possible

minimal private implementation under current §13 boundary
    NO

contract correction route
    OPEN; must be audited separately
```

这里的 `NO` 只否定“在当前最小施工面直接实现完整 0.1 classifier”，不宣称 0.1 在任何未来 runtime 中都不可能实现。

## 9. 两条候选路线，当前均未授权

### Route A：保持 0.1 原顺序

若保持 0.1，后继必须先定义并证明：

```text
version-bound codec lookup
version-bound whole-source decoder semantics
per-input conformance across supported hosts
infrastructure failure != per-subject unsupported
```

可能的实现包括 frozen decoder substrate 或等价的可信执行依赖，但当前合同与仓库没有选择它们。

### Route B：显式发布新函数版本

另一候选是新版本先按 frozen lookup canonicalize effective encoding，再执行：

```text
unknown / BOM conflict
    -> unsupported

known but Profile-nonaccepted encoding
    -> unsupported

accepted UTF-8 / UTF-8-SIG
    -> strict whole-source decode
    -> eligible or unsupported
```

该路线只需要为可能 eligible 的 decoder 绑定精确行为，并与 0.1 coarse terminal classification 保持一致。但它改变
了 §5.2 的 normative order，必须拥有新的 function identity、合同修正与完整资格链；本审计没有授予这些权力。

本文不在 A/B 之间作决定。它只证明：直接开始 0.1 private implementation 不是当前最小合法动作。

## 10. falsifier matrix

| ID | world | 拒绝的错误推理 |
| --- | --- | --- |
| `LSI-000` | `windows-31j` 在 3.10 unknown、3.13 解析为 `cp932` | host lookup success 等于 frozen resolver result |
| `LSI-001` | 100,000 worlds 的 reduced terminal projection 全相同 | terminal equality 等于 frozen algorithm conformance |
| `LSI-002` | sampled text decoders 未发现 3.10/3.13 差异 | finite corpus 等于 total per-input equivalence proof |
| `LSI-003` | non-accepted codec 在 membership 前被 whole-source decode | UTF-8-only accepted set 自动缩小 decoder authority surface |
| `LSI-004` | reducer 先做 accepted-set rejection | 可以不 version-bump 地重排 frozen pipeline |
| `LSI-005` | eligible path 被筛出，但 request 仍携带所有 blob bytes | output filtering 等于 Parse input authority |
| `LSI-006` | host codec 缺失或 decoder failure | infrastructure/integrity failure 可以伪装 per-item unsupported |

## 11. stop line

本文自己的 original PR、受保护合入与 new exact-main Public CI / Browser Smoke 成立后，最多发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只能从新的 exact main 审计最小 codec-conformance / pipeline-order correction。不得在本 PR 中：

```text
modify contract 0.1
publish contract 0.2
implement classifier or carrier
choose persistence Route A/B
run real parser or AST / Fact Provider
change public Schema / corpus / identity vectors
add shared receipt / ledger
start ReviewSliceSet / Coverage
change Evidence / Manifest / publisher / Bundle
```

若后继选择 version bump，0.1 仍是已冻结的历史合同；新版本不能倒写成“0.1 从未成立”。

## 12. 本候选的资格门

本候选只允许修改：

```text
this audit document
README navigation / current projection
AGENTS exact boundary
milestones history
```

必须重新通过本层声明的 docs/link/boundary gates 与 Public CI。受保护合入以后还必须由新的 exact main 自己通过
Public CI 与 Browser Smoke；在此以前，本文只是 audit candidate，不得宣称上述 audited / not-authorized target state
已经生效。
