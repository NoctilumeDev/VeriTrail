# R1 Language Support private classifier 实现授权审计

日期：2026-09-27

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTATION_ALLOWED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTATION_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@fa74ae22872691eebf2fe8bdb2209da34b64b56e`，Git tree
> `21d72d18e5d86fd3d3b5aabdf62dac5d7f8fa475`
>
> 冻结合同：[Language Support codec-conformance 修正合同 0.2](202-r1-language-support-codec-conformance-correction-contract.md)
>
> 影响层级：`L2_IMPLEMENTATION_AUTHORIZATION_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改
> runtime、tests、Schema、corpus、identity vector、Profile、Policy、execution-cell protocol、Provider、parser、
> Fact、Relation、Slice、Coverage、Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、
> tag 或 Release。

## 1. 审计问题与结论

[文档 203](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)最后门已经闭合，
`r1-python-language-support/0.2` 是当前 frozen function。合同冻结没有自动授予代码施工权；本文重新执行
CONTROL LOOP，只问：

> 当前最小 private implementation 能否在不选择 persistence、不修改 public identity、不运行 real parser、
> 不改 frozen execution-cell 0.1 request，也不借用 Fact/Coverage authority 的前提下形成可复核闭包？

结论必须拆成两层：

```text
private deterministic classifier
  + exact-history revalidation
  + 0.2 compatibility / encoding function
  + complete per-subject reason composition
  + exactly-one denominator closure
    -> feasible and minimal

eligible-only Parse operation projection
  + same-attempt continuation claim
  + execution-cell request integration
    -> not yet authorized
```

因此本文只条件化授权 **private classifier stage**。它形成私有 semantic result，不形成 live continuation、
Parse request、Provider input、execution receipt 或 public Artifact。Parse gate 必须在 classifier 真实实现、合入并由
新 exact main 重新审计以后另行申请 authority。

## 2. 0.2 冻结事实已经成立

冻结发布 PR #215 的最终 head 为 `969648a04a2d885725faba7f2c10273cdda4cbca`，合入
`main@fa74ae22872691eebf2fe8bdb2209da34b64b56e`。原始与 exact-main 门均在 attempt 1 成立：

| 门 | Run | 结果 |
| --- | --- | --- |
| PR #215 Public CI | `36252309763` | `11/11 SUCCESS` |
| exact-main Public CI | `36253391449` | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36253391478` | `1/1 SUCCESS` |

从该 exact main 建立的 fresh CPython 3.13.13 installed-product readback 对 README、文档 202、文档 203 与
milestones 使用四个独立 Plan/session/output；P1/P2 均 `COMPLETE`，Core 均 `PASS`。五份匿名 raw source bytes
逐字节等于 exact Git blobs。独立 verifier 重新核对 Plan、Evidence、handoff、Core report、source bytes、merge
ancestry/tree 与 CI source identity，最终 canonical manifest 为：

```text
sha256_json  = 4783ae6c0ef3da1abb9a0d2e8cd18038a29c83360dca96c579fee817eb103c9a
sha256_bytes = 7bc122c5f699331be91eab30f6fd041be503cb11126aedc6e72354b13c97074e
```

首次准备脚本的 source-substring assertion failure、Playwright executable-path diagnostic 退出后的 pending-task
warning，以及从非 Git root 调用 `gh` 形成的三个空 setup files 都保留为 setup/diagnostic history；它们没有启动或
替代四份正式 readback。上述最终门闭合后，0.2 frozen target 已经生效；本文不追加新的事后冻结条件。

## 3. exact main 的相关字节

```text
e4b70878359d1b9ffae9f82884eddd67981d4bded9b1bdadba58a3ea04a8bede  docs/198-r1-language-support-qualification-contract.md
1660025c6f090055706807d9b3c5f19f5ed07adb6bec5be6e78cd8d275c5bee5  docs/202-r1-language-support-codec-conformance-correction-contract.md
a1e80646a61f0f638472df578106e7fe4a3186b9bded6e65e862697a14b1e434  docs/203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md

fed71dab3c7bdd99bbb4fe5b2e3b64875a44946b74d3375f4d169cffc4918c98  plugins/review-attention/src/veritrail_review/derivation_input.py
820fcc9da7d87fe60aba6a6876192e222c9d85e5e00c8c07454102ae01917d2f  plugins/review-attention/src/veritrail_review/derivation_input_contracts.py
bd2037368946f2f10ccb462819f7b9c3f4b62fd7a05ad341d772fa7d593008fa  plugins/review-attention/src/veritrail_review/_execution_cell.py
62933f560f2df275bdde5097ba7bc8a292962a7125c6a4f2988fdcda34176559  plugins/review-attention/src/veritrail_review/_execution_cell_application.py
```

文档 198/202/203、runtime、Schema、Profile、Policy 与 architecture assets 在本审计中保持不变。本文读取它们，
不把审计解释成合同 version bump 或实现。

## 4. 当前可复用的结构事实

### 4.1 exact semantic world 已经 copy-owned

`DerivationInputSet` copy-own 三份 canonical input bytes、全部 verified blob bytes 与五个历史 digest；blob mapping
在构造时复制并包成只读 view，不保存 repository path、open handle、ProviderRun、attempt 或 continuation。因此同一
exact semantic world 可以供多个合法 classifier attempts 重新计算，而不继承执行权。

但 `DerivationInputSet` dataclass 的字段可被调用者直接构造，类型存在本身不是 qualification。private classifier
必须重新 parse/validate：

```text
SourceSnapshot canonical bytes and digest
ReviewPolicy canonical bytes, seal and digests
DerivationProfile canonical bytes and digest
cross-artifact Snapshot / Policy / Profile binding
exact verified blob key set, Git object bytes, size and SHA-256
```

只比较五个 digest、相信 caller-supplied object、重新读 mutable path 或遗漏 blob key 都不合格。

### 4.2 0.2 已把 classifier 算法面压成有界闭集

Profile compatibility 只接受 exact：

```text
language = PYTHON
language_semantics = PYTHON_3_10
canonical accepted_source_encodings = {UTF-8, UTF-8-SIG}
```

0.2 只需要 frozen Python 3.10 cookie/BOM placement、closed accepted-UTF-8 resolver、BOM consistency、
non-accepted early rejection 与 possibly-eligible UTF-8/UTF-8-SIG strict whole-source decode。它不再要求实现整个
CPython 3.10 codec decoder universe，也不得回退到 ambient `codecs.lookup()`。

因此文档 200 的 codec-conformance blocker 已被 versioned 0.2 明确消解。没有新反例要求重开 0.2。

### 4.3 denominator 与 exactly-one closure 可以在 private semantic layer 闭合

classifier 可以从 exact Snapshot inventory 与 sealed Policy scope decisions 做唯一 raw-path join，只把 `IN_SCOPE`
members 纳入 denominator，并按 raw Git path bytes 排序。对每个 member 求值全部 applicable predicates，形成 frozen
rank 的完整 reason set，随后机械证明：

```text
denominator = eligible U unsupported
eligible intersection unsupported = empty
every denominator member appears exactly once
no OUT_OF_SCOPE or foreign-world member appears
```

这是一项 deterministic derived fact。它不需要 Provider report、parser outcome、Coverage self-report、public Schema
或持久化选择。

## 5. 当前 Parse gate 仍缺独立 authority seam

当前 `_execution_cell_application.build_request_document()` 把 Snapshot 中每个 blob 的 body 都放入
`source_blobs`。`_validate_source_blobs()` 要求 request body 数量与全部 blob inventory 相等；它产生的
`supported_paths` 只检查 entry kind 与 `.py` suffix，没有执行 Policy source class、0.2 codec qualification 或
whole-source decode。

当前 `_build_prepared_closed_test_execution_attempt()` 又按以下顺序运行：

```text
admit one BudgetContext
    -> build complete request document
    -> encode immutable request frame
    -> final pre-cell checkpoint
    -> create prepared attempt
    -> execution-cell process creation / containment
    -> AttemptEligibility.admit()
    -> resume process and write the already-built request frame
```

这意味着 exact main 上不存在一个可以直接复用的：

```text
same live attempt
    -> qualified eligible set
    -> eligible-only request bytes
    -> existing frozen 0.1 protocol validation
```

接点。把另一个 `eligible_paths` 集合塞进旁路对象、先把所有 bytes 给 Provider 再过滤输出，或在脱离真实 cell 的
测试对象上自称 one-shot gate，都不能建立 Parse input authority。

这不是 classifier blocker，也不是当前 execution-cell runtime defect。它只证明：

```text
classifier implementation
    can proceed privately

request projection / cell integration
    needs a later explicit audit and possibly a versioned private protocol boundary
```

本文不修改 frozen execution-cell 0.1，不预选 0.2 request shape，也不允许 implementation branch 顺手做该扩张。

## 6. 有限实现授权

本文最后门全部成立后，下一分支只允许实现一个 private semantic classifier stage：

```text
A. exact owned input/history revalidation
B. r1-python-language-support/0.2 compatibility and closed UTF-8 resolver
C. deterministic per-subject classification with complete canonical reasons
D. exactly-one denominator closure and immutable private semantic result
```

实现必须满足：

1. 代码保持 `veritrail_review` private，不进入顶层 `__all__`，不新增 CLI、entry point 或 plugin discovery；
2. 不重新读取 repository/path，不调用 ambient codec registry，不运行 `ast` 或 real parser；
3. exact input/history validation 失败、Profile incompatibility 或内部 integrity failure 使整个 classification 不成立，
   不得把所有 subjects 伪装为 unsupported；
4. private result copy-own 规范语义内容，不 copy-own或序列化 `BudgetContext`、attempt、deadline、continuation、
   Provider identity、repository path 或 output coordinate；
5. 可以形成 private canonical bytes/digest 以做确定性比较，但它不是 public Artifact、Evidence、receipt、Coverage
   denominator 或 persistence 决策；
6. implementation tests 必须直接覆盖 `LSC2-000..011` 中适用于 classifier 的拒绝边界，并增加本节第 7 节的
   exact-history/closure falsifiers；
7. 当前 `_execution_cell*`、Provider、Fact/Relation/Slice runtime 不得调用该 classifier。集成只有在后继
   Parse-gate audit 明确授权后才允许。

### 6.1 不授权的邻接能力

```text
live continuation or attempt authority
eligible-only source-body / operation projection
execution-cell request or protocol changes
Provider input filtering or ProviderRun changes
persistence Route A/B selection
public classifier carrier / Schema / corpus / identity-vector changes
real parser / AST / Fact fulfillment
shared receipt / ledger
ReviewSliceSet / Coverage
Evidence / Manifest / publisher / Bundle
CLI / Workbench / Core / Q / O / T runtime
```

因此 `PRIVATE_CLASSIFIER_IMPLEMENTATION_ALLOWED` 不得缩写成“Language Support 已完整实现”或“Parse 已有资格”。

## 7. 实现必须面对的 falsifiers

| ID | world | 必须拒绝的错误推理 |
| --- | --- | --- |
| `LSI2-000` | caller 直接构造字段自洽但 canonical bytes/digest 不匹配的 `DerivationInputSet` | dataclass identity 等于 qualified history |
| `LSI2-001` | 同一 path ref 绑定不同 blob bytes 或 Policy source class | path-only ref 足以缓存 classification |
| `LSI2-002` | Profile compatibility 多/少一个 encoding 或语言语义漂移 | 0.2 可静默扩张或回退 0.1 |
| `LSI2-003` | `utf.8`、`cp65001`、BOM + `utf8` | 字符串相似或 ambient codec success 拥有 resolver authority |
| `LSI2-004` | accepted UTF-8 declaration后存在 invalid trailing bytes | detection success 等于 whole-source qualification |
| `LSI2-005` | source class、entry kind、language/path 中多项同时失败 | first failure 等于完整 canonical reason set |
| `LSI2-006` | unsupported entry kind / non-Python path | 不适用的 encoding predicate也必须编造 reason |
| `LSI2-007` | denominator 为合法空集 | 空集自动获得 Coverage `CLOSED_EMPTY` 或 Parse completion |
| `LSI2-008` | 同 exact inputs 两次复算得到相同 semantic result | semantic equality 继承 attempt/continuation authority |
| `LSI2-009` | current execution-cell request 仍携带 unsupported blob bytes | classifier 通过已经建立 eligible-only Parse boundary |
| `LSI2-010` | caller mutation / `object.__setattr__` 后的 input或 result | frozen dataclass 声明替代 construction-time 与 use-time seal |
| `LSI2-011` | finite test corpus 全绿 | sampled worlds 已证明 total function |

测试是这些边界的 witness，不拥有修改 0.2、授予 Parse gate 或选择 persistence 的 authority。

## 8. 后继停止线

private classifier implementation 只有在自己的最终字节、本层声明的完整 local gates、original PR checks、受保护
合入、新 exact-main Public CI / Browser Smoke 以及所需 fresh observation/reconciliation 全部成立后，才能成为新的
implementation fact。该事实形成后必须返回 CONTROL LOOP，重新问：

> eligible-only operation projection 与 same-attempt Parse gate 是否仍是最小合法问题；若是，现有 execution-cell
> 0.1 能否在不泄露 unsupported bytes 的前提下承载，还是需要一个最小 versioned private protocol correction？

在此以前不得先写 protocol 0.2、改 `source_blobs` cardinality、让 Provider自行忽略 bytes，或把 classifier unit tests
当作 Parse input-boundary proof。

## 9. 本审计自己的最后门

本 docs-only 候选只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 198/202/203、
runtime、tests、Schema、Profile、Policy、corpus、architecture DOT/SVG 与 identity vectors 必须保持原字节。

提交前必须通过适用双 Python normal/`-O` docs/Schema regressions、relative links、UTF-8/LF/final-LF、
heading/fence、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与 `git diff --check`。随后必须完成：

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> conditional authorization state takes effect
```

任一非成功观察都保留原身份；后继 PASS 不覆盖首败。本文的 target marker 在最后门以前只是 publication target，
不授权代码分支提前开始。

### 9.1 本地资格结果

第一次 CPython 3.10 normal invocation 未绑定 current-source `PYTHONPATH`：37 个 Schema tests 已执行，但
`tests.test_markdown` 在 import 阶段以 `ModuleNotFoundError: veritrail` 停止。该次只记为
`INVALID_LOCAL_TEST_SETUP`，没有被后继结果解释成产品或文档失败，也没有以放宽 assertion 或删减 module 修正。

把 exact checkout 的 `src` 与 `plugins/review-attention/src` 显式加入 source topology 后，同一最终文档字节通过：

| Lane | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `40/40 PASS` |
| CPython 3.10.6 `-O` | `40/40 PASS` |
| CPython 3.13.13 normal | `40/40 PASS` |
| CPython 3.13.13 `-O` | `40/40 PASS` |

每格运行 `tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`。独立静态 checker
又确认 exact diff scope 为本文、`README.md`、`AGENTS.md`、`docs/milestones.md` 四个文档文件，relative links、
UTF-8/LF/final-LF、fence、target markers 与 base identity 均成立；文档 198/202/203 和四个相关 runtime 文件的
七份 SHA-256 与第 3 节一致，`git diff --check` 通过。测试仍只是本候选的 witness，不使条件化 target 提前生效。
