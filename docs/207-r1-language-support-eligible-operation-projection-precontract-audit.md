# R1 Language Support eligible-only operation projection / same-attempt gate 前合同审计

日期：2026-09-27

## 1. 文档身份与条件状态

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@476fa8c1740e96be80e068265a9af210f860f420`，Git tree
> `adc6fbf93620f24dbff2d90ef5d65540e7d2d768`
>
> 上游冻结发布：[文档 206](206-r1-language-support-private-classifier-implementation-freeze-publication.md)
>
> 影响层级：`L2_PRECONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改 runtime、tests、
> Schema、Profile、Policy、corpus、identity vector、execution-cell request/protocol、Provider、parser、AST、Fact、
> Relation、Slice、Coverage、Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或
> Release。

本文只重新执行 classifier 冻结后的 CONTROL LOOP，回答：

> eligible-only source-body operation projection 与 same-attempt gate 是否仍是当前最小合法问题；若是，现有
> execution-cell / relation-cell 私有协议能否直接承载，还是必须先形成 versioned private correction contract？

本文不是 Parse fulfillment 合同，不运行真实 parser，不解释 syntax outcome，也不授权代码施工。本文中的
`PRECONTRACT_AUDITED` 只允许后继从新的 exact main 起草一个 docs-only 最小合同；它不等于 contract frozen、
implementation allowed、Parse started 或 Fact/Coverage ready。

## 2. 审计结论

结论分成四层：

```text
private classifier 0.2
    -> frozen and effective

eligible-only source-body authority
    -> still the next minimal seam

current source-body-carrying request protocols
    -> cannot express that seam without changing frozen semantics

same-attempt substrate
    -> structurally available
    -> no qualified projection claim / binding exists yet
```

因此下一份最小合同必须同时冻结：

1. controller-owned Language Support classification 怎样约束 source-body operation projection；
2. projection 怎样绑定原始 exact inputs、`r1-python-language-support/0.2` 与原 live attempt；
3. Fact、Relation derivation 与 Relation observation 三类 source-body-carrying request 怎样服从同一 eligible 上界；
4. request / operands identity 怎样区分不同 function 或 projection world；
5. zero-eligible、deadline、cancellation、integrity failure 与 one-shot consumption 怎样 fail closed；
6. frozen protocol identity 怎样显式 version，而不是静默改变 `source_blobs` cardinality。

该合同仍不得选择 persistence、创建 public carrier、运行真实 parser、定义 Parse terminal outcomes、改变 Fact/Relation
语义，或开始 ReviewSliceSet/Coverage。

## 3. classifier freeze 已成为当前事实

[文档 206](206-r1-language-support-private-classifier-implementation-freeze-publication.md)的最后门已闭合。最终发布
PR #219 的 head 为 `a857597a7691aaedca68fa8457dd00143d4f85e5`，以 merge commit
`476fa8c1740e96be80e068265a9af210f860f420` 合入受保护 main；merge tree 与 candidate tree 都是
`adc6fbf93620f24dbff2d90ef5d65540e7d2d768`。

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| PR #219 Public CI | `36273175628` | 1 | `11/11 SUCCESS` |
| exact-main Public CI | `36274415270` | 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36274415265` | 1 | `1/1 SUCCESS` |

README、文档 206 与 milestones 又从该 exact main 完成三个互不复用的 fresh anonymous installed-product
observations；P1/P2 均 `COMPLETE`、Core 均 `PASS`。四份 public raw bytes 与 exact Git blobs 一致。最终
reconciliation manifest 摘要为：

```text
sha256_json  = 50ca3ac1f7e03ba1ef93d6d7c7903165954b1c973c3de3b2246446f2c9ae21a9
sha256_bytes = 8df9dbd272e0569dd97c822d04ee16e2bb09bca073fe5de50709f0110ea6ee58
```

因此本文消费的是已经生效的：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
```

本文不追加 classifier freeze 的事后条件，也不重解释其历史 setup observations。

## 4. authority owner 重新核账

当前 seam 必须先区分四类 authority：

| 对象 | owner | 不是 owner 的对象 |
| --- | --- | --- |
| exact source world | copy-owned `DerivationInputSet` 经 canonical history / Git object byte revalidation | path、digest 字符串、Provider report |
| Language Support eligibility | frozen `r1-python-language-support/0.2` deterministic application | Provider、parser tolerance、current `supported_paths` |
| live attempt / stop boundary | controller-owned original `BudgetContext` 与不可逆 `AttemptEligibility` | classification digest、caller boolean、同 limits 的新 context |
| source-body operation projection | application/controller 在 Provider admission 前形成的 qualified request projection | Provider 自行忽略、terminal filter、FactSet reconciliation |

由此得到：

```text
available exact bytes
    != Provider-authorized operation bytes

same classification bytes
    != same live attempt

Provider did not report a Fact
    != Provider never received the bytes
```

Provider 可以消费 projection，却不能定义 eligibility、扩大 projection、补做 admission 或用 terminal output 反向证明
input authority。

## 5. 六个 concrete worlds

审计从 exact main 的 current-source modules 构造六个单变量/组合世界。审计脚本与四份 canonical report 位于仓库外：

```text
<local-workspace>/tmp/
  veritrail-r1-language-support-parse-gate-audit-476fa8c/
```

它们不是仓库 Artifact、Evidence 或后继 implementation input。脚本 SHA-256 为：

```text
103611f30be851ed56c1f128a941879be348916f199c6bcf960418b55ebb1817
```

CPython 3.10.6 / 3.13.13 normal/`-O` 四格严格串行运行，四份 3072-byte canonical JSON report 逐字节相同：

```text
fec549e3181d02c0ef200c0d3ddc91ebec5d32866519ea0de6f6b9e3d2737ca0
```

| World | classifier | current request body | current closed cell |
| --- | --- | --- | --- |
| eligible-only | `1 ELIGIBLE` | 只含 eligible path | `COMPLETED`，Fact 锚在 eligible path |
| mixed encoding | `1 ELIGIBLE + 1 UNSUPPORTED_SOURCE_ENCODING` | 两份 bytes 都进入 | `COMPLETED`，Fact 锚在 rejected Latin-1 path |
| all unsupported encoding | `1 UNSUPPORTED_SOURCE_ENCODING` | rejected bytes 进入 | `COMPLETED`，Fact 锚在 rejected path |
| unclassified valid Python | `1 UNCLASSIFIED_SOURCE` | rejected bytes 进入 | `COMPLETED`，Fact 锚在 rejected path |
| out-of-scope valid Python | denominator empty | excluded bytes 进入 | 后段才成为 `NONCONFORMANT_PROVIDER_OUTPUT` |
| in-scope non-Python | `1 UNSUPPORTED_LANGUAGE` | rejected bytes 进入 | 后段才成为 `INTERNAL_DERIVATION_ERROR` |

混合编码 world 又进入 current private Fact/Evidence closure：

```text
classifier eligible     = pkg/z_good.py
classifier unsupported  = pkg/a_bad.py
FactSet fact path       = pkg/a_bad.py
normal continuation     = permitted
```

这证明 current downstream admission 与 live continuation 不会自动修复 upstream projection 缺口。该观察不把旧 runtime
倒填成 defect：execution-cell / FactSet 正在履行各自既有冻结合同，而这些旧合同早于 Language Support classifier，且
从未声称自己实现了 eligible-only gate。新事实只切断以下错误推理：

```text
classifier exists
    -> current Provider input is already qualified        [false]

terminal output was rejected or empty
    -> unauthorized bytes were never exposed              [false]

FactSet closure and continuation exist
    -> Language Support gate must have been satisfied      [false]
```

## 6. 缺口覆盖三个 source-body-carrying protocol

### 6.1 Derivation Fact cell

`veritrail-review-derivation-cell/0.1` 的 `build_request_document()` 枚举 Snapshot 中每个 BLOB，把全部
`content_base64` 写入 request。worker 的 `_validate_source_blobs()` 又要求 request body 数量等于全部 BLOB inventory，
并只按 entry kind + `.py` suffix 形成 `supported_paths`。

`ValidatedRequest.document` 保留完整 request，因此 Provider 即使没有专门的 bytes field，也可以读取完整
`source_blobs`。current terminal/candidate validator 只在 Provider 已收到 request 后运行。

### 6.2 Relation derivation cell

`veritrail-review-relation-cell/0.1` 重新调用 `_owned_source_blobs(inputs, snapshot)`，把全部 Snapshot BLOB bytes
写入 relation request。worker validation 解码完整 map，`_copy_relation_request_for_provider()` 又把整份
`source_blobs_by_path_hex` copy 给 Relation Provider。

Relation Provider 当前只按 Fact paths 读取 bytes，是 closed implementation behavior，不是 authority boundary；Provider
拥有完整 map 后，“它现在没有访问其他 key”不能证明那些 key 没有被授权暴露。

### 6.3 Relation observation cell

`veritrail-review-relation-cell/0.2` 同样重新携带全部 source blobs，并把完整 map copy 给 observation Provider。它的
operation paths 虽由 FactSet / assigned domain 收窄，available bytes 仍比 operation-required bytes 大。

因此最小合同不能只修改第一个 Fact request，也不能只依赖 FactSet 不再产生 unsupported facts。Language Support
eligible set 必须成为同一 derivation attempt 中所有 source-body-carrying Provider request 的共同上界；后继 request
可以继续按自己的 Fact/domain obligations 取更小交集，但不能越过该上界。

## 7. current 0.1/0.1/0.2 不能静默承载

三个协议都冻结了 exact request keys 与全量 `source_blobs` continuity。共享 `_validate_source_blobs()` 明确要求：

```text
len(request source_blobs)
    == len(all Snapshot BLOB inventory entries)
```

而新的 authority 需要至少满足：

```text
Provider-visible source-body paths
    subset of exact classifier eligible paths

Provider-visible source-body paths
    contain no OUT_OF_SCOPE or unsupported subject
```

二者在 mixed / empty / all-unsupported worlds 中不能同时成立。旁路增加 `eligible_paths` 而保留全量 bodies、先把 bytes
交给 Provider 再要求忽略、或只过滤 terminal output，都不满足 input authority。

因此后继合同必须显式处理 protocol compatibility/versioning。本文不预选一个共享 protocol 版本号，也不要求三种
request 使用同一 document shape；但它禁止用同一 frozen identity 静默改变 cardinality 和 validation semantics。

## 8. same-attempt substrate 存在，但 claim 尚未存在

current controller 的顺序是：

```text
admit original BudgetContext
    -> build request document
    -> encode immutable request frame
    -> final controller checkpoint
    -> create one-shot prepared attempt
    -> create suspended Provider process / containment
    -> AttemptEligibility.admit()
    -> resume process and write frame
```

这提供了一个有界窗口：controller 可以在原 budget admission 之后、Provider process admission 之前，对 exact
copy-owned inputs 运行/复核 classifier，形成 projection，并在 deadline/cancellation checkpoint 下编码 request。现有
prepared attempts 已是 one-shot；multi-provider / Relation controllers 也已经共享原 `BudgetContext`，没有必要为 gate
新建 limits 相同的第二个 context。

但 current code 尚不存在：

```text
original live attempt
    + exact classifier function/result
    + eligible source-body projection
    + one-shot request construction
    + all child request binding
```

classification value 本身故意不携带 context、attempt 或 continuation。调用者传入 digest、path set、boolean 或另一个
attempt 的同字节 classification 都不能补出 live authority。后继合同必须冻结 claim/consumption 的语义不变量，但不必
在本审计中命名 class、token 或 API。

## 9. request identity 也必须绑定 projection authority

current provider operands digests 绑定 Snapshot、Policy、Profile 与 Provider；Relation 变体另外绑定 FactSet/domain。
它们没有显式绑定 Language Support function identity 或 eligible operation projection。

如果 function/version 或 eligible set 改变，而 provider-run identity 仍保持原值，就可能出现：

```text
different authorized operation input
    -> same provider operands / run identity
```

因此后继合同必须要求 request/operands identity 对 exact Language Support function 与 exact projected subject set 有
机械绑定。本文不预决定必须新增 `classification_digest` 字段；它只否定“现有 input digests 自动证明任意未来
classifier version/projection”的推理。

## 10. trusted application validator 与 Provider view 必须分开

过滤 unsupported bodies 以后，Provider worker 不再拥有那些 exact bytes，因此不能在 Provider-visible request 中重新
执行完整 classifier。后继合同必须明确：

```text
controller classifier authority
    -> constructs qualified projection

application-owned request validator
    -> validates projection identity and included-byte continuity

Provider-visible request
    -> receives only authorized operation bodies
```

这不是允许 worker 盲信 caller set。合同仍须定义 controller result、function identity、exact history 与 request projection
怎样绑定，以及 worker/application validator 能机械检查到什么。Provider 不能成为 omission authority，也不能因缺少
unsupported bytes 而自证“它们确实 unsupported”。

## 11. zero-eligible world 不能被偷偷解释

至少必须区分：

```text
Language Support denominator empty
non-empty denominator but all subjects unsupported
eligible subjects exist but a later operation has no assigned path
```

这三类 world 都可能没有 Provider-visible source body，却不具有相同语义。后继合同必须定义 gate 的 terminal/private
disposition 与 revocation behavior；它不得：

- 启动只携带 unsupported bytes 的 source-consuming Provider；
- 把“不启动 Provider”自动写成 Parse `COMPLETE`、`CLOSED_EMPTY` 或 Fact/Coverage fulfillment；
- 把 all-unsupported 偷换成 denominator empty；
- 用 Provider internal error 代替 upstream gate result。

本文不命名 zero-operation result type，也不决定它是否成为 future evidence。

## 12. 下一份最小合同面

本文最后门闭合后，只允许起草一个 docs-only contract，至少回答：

1. **semantic binding**：exact Snapshot/Policy/Profile history、classifier function 与 result 怎样绑定；
2. **eligible upper bound**：所有 Provider-visible source-body paths 怎样证明是 exact eligible set 的子集；
3. **operation projection**：Fact / Relation / observation request 怎样声明并验证各自所需的更小 operation set；
4. **same-attempt ownership**：原 `BudgetContext`、parent/child `AttemptEligibility` 与 one-shot prepared request 怎样继续；
5. **identity binding**：provider operands/run identity 怎样区分不同 function/projection world；
6. **validator boundary**：controller、application validator 与 Provider 各自可以看到什么、证明什么；
7. **zero-operation semantics**：empty denominator、all unsupported 与 later empty assignment 怎样分开；
8. **failure semantics**：integrity failure、deadline、cancellation、transport insufficiency 与 concurrent/double claim 怎样 fail closed；
9. **protocol versioning**：三个 frozen request identities 怎样显式 correction；
10. **scope closure**：所有 source-body-carrying child requests 怎样证明没有遗漏旁路。

这些问题闭合以前，不得修改 `source_blobs` cardinality、operands digest、worker/provider request type 或 execution-cell
builders。

## 13. 必须面对的 falsifiers

| ID | world | 必须拒绝的错误推理 |
| --- | --- | --- |
| `LSPG-000` | mixed eligible/unsupported bytes，旧 cell 在 unsupported path 上完成 Fact | terminal success 证明 input authorized |
| `LSPG-001` | all subjects unsupported，旧 cell 仍完成 Fact | non-empty old `supported_paths` 等于 classifier eligible |
| `LSPG-002` | OUT_OF_SCOPE bytes 进入 request，后段才失败 | later candidate rejection 撤销先前 bytes exposure |
| `LSPG-003` | relation request 的 Fact paths 都 eligible，但 Provider copy 仍含其他 bytes | operation subset 使 full request automatically least-authority |
| `LSPG-004` | 同 classification bytes 来自另一个 attempt | semantic equality 恢复 continuation |
| `LSPG-005` | 新建 limits 相同的 `BudgetContext` | equal limits 等于 original attempt |
| `LSPG-006` | caller 传入 eligible path set / boolean / digest | caller assertion 拥有 projection authority |
| `LSPG-007` | Provider 收到全量 bytes 后自行忽略 unsupported | Provider self-restraint 是 input boundary |
| `LSPG-008` | output/FactSet filter 删除 unsupported result | output reconciliation 可以倒置 input authority |
| `LSPG-009` | zero eligible | Parse/Fact/Coverage 自动 `CLOSED_EMPTY` |
| `LSPG-010` | classifier function 改变但 old operands digest 不变 | exact inputs alone bind every future qualification function |
| `LSPG-011` | 只修 Fact request，Relation/observation request 仍携带全量 bytes | first gate 已覆盖全部 source-consuming cells |
| `LSPG-012` | double/concurrent claim 同一 prepared projection | 两个 child execution 都继承同一 one-shot authority |
| `LSPG-013` | classification/projection 后 deadline 或 cancellation latch | stale frame 仍可启动 Provider |
| `LSPG-014` | request payload limit 只够 filtered frame | 先构造全量 frame 再过滤仍符合 admission |
| `LSPG-015` | finite six-world / four-lane audit 全绿 | sampled worlds 已证明 total protocol contract |

测试只能 witness 这些边界，不拥有 contract wording、protocol version、reason、state 或 implementation authority。

## 14. 明确 non-decisions

本文不决定或授权：

```text
exact request field names or protocol version numbers
shared carrier/class hierarchy
public Language Support carrier / Schema / Evidence
persistence Route A or B
historical/offline blob reacquisition
real parser / AST / syntax-version discrimination
Parse terminal outcome or fulfillment contract
Fact projection / fulfillment correction
Relation semantic changes
shared receipt / ledger
ReviewSliceSet / Coverage
Manifest / publisher / Bundle
CLI / Workbench / Core / Q / O / T
```

三个 request protocol 以后可以共享 lower-level helper，但只有各自 owner、identity、validation 与 failure semantics 先
独立闭合，才能证明该抽象不会混淆 authority。本审计不预造一个通用 `OperationLedger` 或 `ObservationReceipt`。

## 15. 后继停止线

本文自己的最终字节、local docs/Schema/static gates、original PR required checks、受保护主线合入、新 exact-main
Public CI / Browser Smoke，以及 fresh installed-product readback/reconciliation 全部成立后，才允许从新的 exact main
起草第 12 节的最小合同。

在此以前：

```text
contract drafting      NOT STARTED
runtime implementation NOT AUTHORIZED
Parse fulfillment      NOT STARTED
```

合同候选形成以后仍须走自己的冻结链；contract frozen 也不能自动授权 runtime。任何新反例若击穿 classifier 0.2、
execution-cell/Relation frozen semantics 或本文的 scope closure，只显式重开被击穿的最小边界。

## 16. 本审计自己的最后门

本 docs-only 候选只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档
198/202/203/204/205/206、runtime、tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture DOT/SVG
必须保持原字节。

提交前必须完成适用双 Python normal/`-O` docs/Schema regressions、Markdown relative links、UTF-8/LF/final-LF、
fence/heading、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与 `git diff --check`。本文中的六世界
audit 必须从未修改的 exact-main runtime 重新运行，并保持四格逐字节一致。

最终四文件字节已经通过本地候选门：

| Lane | docs / Schema 结果 |
| --- | --- |
| CPython 3.10.6 normal | `40/40 PASS` |
| CPython 3.10.6 `-O` | `40/40 PASS` |
| CPython 3.13.13 normal | `40/40 PASS` |
| CPython 3.13.13 `-O` | `40/40 PASS` |

每格运行 `tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`。六世界 audit 又从
未修改 runtime 严格串行重跑，四格仍分别为 3072 bytes，SHA-256 都是
`fec549e3181d02c0ef200c0d3ddc91ebec5d32866519ea0de6f6b9e3d2737ca0`。

独立只读 checker 确认：exact status scope 恰好是 `AGENTS.md`、`README.md`、`docs/milestones.md` 与新增本文；
488 个相对链接可解析；三枚条件状态 marker 在四个文件中各恰好出现一次；UTF-8 无 BOM、LF、final-LF、fence、
敏感本机路径与 `git diff --check` 均成立。第一次只读行尾检查命令因 PowerShell 管道语法错误以 `ParserError`
停止，没有读取结果或修改仓库；修正命令随后通过。该 setup failure 保留原身份，不记作产品、合同或文档失败。

这些结果只使本地候选可提交；测试与 sampled worlds 仍不拥有 contract wording、protocol version、状态生效或后继
implementation authority。

随后必须完成：

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> conditional precontract-audited state takes effect
```

任一 FAIL/ERROR/CANCELLED/setup failure 保留原身份；后继 PASS 不覆盖首败。本文 target marker 在最后门以前只是
publication target，不授权后继合同分支提前开始。
