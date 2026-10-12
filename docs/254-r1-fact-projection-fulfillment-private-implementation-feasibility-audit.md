# R1 Fact projection / fulfillment 私有实现可行性审计

> 状态：`R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
> 基线：`main@c65a9f7d915ea96b22c3ca4d641c12a09664b7ac`。
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`；docs-only，不授予 implementation authority。
> 合同已冻结；successor runtime / Schema / persistence / Coverage 均未启动。

## 1. 外环重新绑定与本轮认领

[doc253](253-r1-fact-projection-fulfillment-contract-freeze-publication.md) 的独立发布由
[PR #291](https://github.com/NoctilumeDev/VeriTrail/pull/291) 合入本基线。final head 为
`5a4c640fe64235979e08dac40af125236c5086d4`；candidate/merge tree 同为
`ebf859bcb732bbd5b3611e79aa8d8b89c3c5bf40`。
original Public CI `38177038668` 与 exact-main Public CI `38191557863` 均 attempt 1 / 11/11 SUCCESS；
Browser Smoke `38191557889` attempt 1 / 1/1 SUCCESS。Review Attention 各格为
`473 reported / 471 passed / 2 skipped`，不把 skip 算作实际通过。

fresh README/doc253/milestones 均 P1/P2 COMPLETE、Core PASS；independent reconciliation
`ff035c7129dd22d796b321124ad3082bd31ee1304502fe6b9b564eb06dbac22f` PASS，closeout
`d416156f4185977ee60d2f788efa48a019a7bb22897a4d35c3d68b111c8e4e29` 封存 132 份 terminal artifacts。
本轮已重核这些 seals。该链使合同 FROZEN 生效，不自动形成 feasibility 或实现授权。

远端与主仓均为本基线，只有旧 Dependabot PR；用户 untracked 状态未参与候选。独立阶段授权只认领：
完整投影、3.10 conformance、successor 边界、逐 Provider 核账、同 attempt lifecycle 与零成员阻断六个问题。

当前 `_parse_product_fact_protocol.py` 的 `/0.1` 只构造 MODULE/CLASS；MODULE mapping 为 null。
`admit_terminal()` 逐条核验已报告 records，`OwnedProductFactConsumer.reconcile()` 复核各来源终态并合并。
这些实现不承诺 [doc252](252-r1-fact-projection-universe-and-fulfillment-contract.md) 的完整五类 U/E；本轮没有把
已声明的旧能力边界归为 runtime defect，也没有修改旧合同、测试或 `/0.1` bytes。

## 2. 审计方法与证据强度

审计计划在观察前固定；各 block 另封存脚本与 gold。四格是 CPython 3.10.6 / 3.13.13 normal / `-O`，串行执行。
实际 Parse 固定使用显式 CPython 3.10.6 executable，其 SHA-256：

```text
32ce1d2650ea8b9d394f5b8f94677d27888dccdc3713365bf903a8c465c9d776
```

| Evidence | 实际证明范围 | 不能提升成的 claim |
| --- | --- | --- |
| reference Parse products | 真实 bounded Parse children、admitted canonical trees 与 partition | successor Fact child 已执行 |
| 独立五类 gold、raw-anchor gold | 有限 U/E 模型与手写语义/字节跨度相符 | 任意输入的通用完整性或真实 Provider fulfillment |
| identifier/component corpus | 声明 corpus 的跨宿主字节一致性与 reference predicates | 任意字符串、安全隔离或所有未来宿主已通过 |
| synthetic reconciliation model | 固定反例中的内容、身份、requiredness 与 safety 判据 | 实际 ProviderRun、one-shot token 或 live continuation |
| unchanged runtime regression | 当前已冻结 primitive 的原声明与真实 reference/worker witness | `/0.2` 已实现或旧资格自动继承 |

有限模型使用预先声明的 expected values 来构造 synthetic reports，只是在反查核账谓词。真实 child 不得接收
这些 oracle answers；没有把模型输出补写成 Provider Evidence。

## 3. 完整投影可以留在 application 私有层

版本化构造消费完整 admitted products、sealed mapping/Profile 与 owned exact anchor history。现有
`walk_product()` 已递归排序后的全部 AST fields 与有序 LIST，`product_byte_anchors()` 可翻译所有有位置的节点，
不是只支持 CLASS。generic Fact canonicalizer 已识别五类 kind/space/属性及既有 identity domains。

audit-only walker 保留直接结构边：仅 ClassDef.body 的直接 LIST item 是 METHOD；class 内条件块中的函数是
FUNCTION。每个 import alias 使用 statement anchor 与原 alias ordinal。MODULE 保留完整 raw-byte anchor，包括
empty accepted source。U 从完整槽位建立，E 再作属性资格；不从 actual candidates 或实际 Fact IDs 倒定义 U。

九个预注册 world 的最终四格结果如下：

| World | Parse accepted / rejected | U | 可表示的 E | normal projection blocker |
| --- | --- | --- | --- | --- |
| nested five-kind / multi-alias / direct method | 1 / 0 | 12 | 12 | 0 |
| BOM / CRLF / multibyte raw anchors | 1 / 0 | 4 | 4 | 0 |
| empty accepted source | 1 / 0 | 1 | 1 | 0 |
| normalized keyword class/function | 2 / 0 | 4 | 2 | 2 |
| nullable module mapping | 1 / 0 | 1 | 1 | 0 |
| normalized module-key collision | 2 / 0 | 2 | 2 | 0 |
| raw ASCII init 与 normalized init spelling | 2 / 0 | 2 | 2 | 0 |
| all rejected | 0 / 1 | 0 | 0 | 0 |
| zero Parse-eligible denominator | 0 / 0 | 0 | 0 | 0 |

normalized keyword world 的 E=2 只是模型保留的可表示前缀，不是普通 qualified E；完整 U=4 且两个槽位不可表示，
因此未来 normal assignment / FactSet / continuation 必须阻断。不能把前缀发布为完整结果。

zero denominator world 使用 IN_SCOPE + source_class=UNCLASSIFIED，Language Support denominator 仍有成员，
Parse eligibility 为零；它与 all rejected 保留不同的 inputs、partition 和 history，不取得 Fact-stage closure。

四格共 36 个 world、44 个实际 reference Parse children，实际 Fact children 为 0。canonical reduced result SHA-256：

```text
b5235912fe2cc4b3130337f7d830b3bf7ee79504bc05150ce3c8fee3163011ea
```

nullable/collision worlds 保存 exact inputs、distinct subject identities 与模型的映射结果。它们没有实现 public
limitation carrier、import resolution 或 Coverage typed-gap closure；具体 private retention surface 仍由后继实现受审。

## 4. Python 3.10 module / identifier conformance

模块 component 必须先检查 raw spelling 的 Python 3.10 start/continue 资格，再 NFKC，最后检查 canonical identifier
及 frozen keyword 集。不能先用新宿主把原本未获 3.10 资格的字符归一成旧字符。仅 raw basename 为 ASCII
`__init__.py` 才省略最后 component；`__ｉｎｉｔ__.py` 保留 normalized `__init__` component。

现有 post-3.10 start/continue range guard 可作为有限机制的基础。对全部 `0x110000` 个码点分别检查 raw start、
`a + character` continuation、canonical Fact 单字符和 canonical Fact `a + character`，reference 3.10.6 独立 built-ins
也逐点复算。这是包含 surrogate 在内的码点 corpus，不声称每项均为 Unicode scalar。

四格的四类 true counts 同为 `131460 / 134415 / 128049 / 130889`；11 个 component gold 还包括 keyword、点号、
fullwidth、micro sign、较新 compatibility character 与空名。四格 canonical result SHA-256：

```text
caa0629e50ec8507fe554bfb807c94b526e6b1d2a694baaf39f851d7b065c34e
```

该 corpus 的 raw masks 与允许字符 NFKC fingerprint 相等。跨字符规范化的机制前提另来自
[Unicode UAX #15 revision 57 §3](https://www.unicode.org/reports/tr15/tr15-57.html#Versioning_and_Stability)：
Unicode 4.1 后的过程稳定性以两个版本中字符均已分配为条件；未分配字符不能直接获得该保证。这是外部规范参照，
不是本项目测试出的结论，也不授予新宿主资格。

有限可行路线是先限制到 reference 3.10 repertoire，再执行受支持宿主的 NFKC 与冻结 keyword/identifier 判据。
实现必须绑定受审 ranges、runtime/Unicode boundary 与 final bytes；未知宿主、guard drift 或无法证明 conformance
时停止，不能把宿主库当隐式 oracle。该路线没有要求 vendor 整个 codec universe，也不修改 doc120 的内容语义。

## 5. Successor descriptor 与 worker input 边界

现有 `ProviderDescriptor/ProviderBinding` 是私有不可变值；closed applicability/cardinality 与 descriptor table 是
consumer 层规则。`run_windows_execution_cell()` 接收 original BudgetContext、AttemptEligibility、executable、arguments
与 request frame，并不拥有旧 descriptor table。因而可在新的私有层声明独立 `/0.2` table、factory 和 request/terminal
validator，再复用原 bounded Windows primitive；不能调用旧 allow-list 并假装它已经认领新版本。

对保留 request 的 stateless checks 已确认：旧 request 仅作为数据可验证；successor consumer projection、successor
terminal 和改版 descriptor 均被旧 validator/table 拒绝。此检查没有重建任何 live token，也没有新 successor admission。

future worker operands 只允许 copy-owned canonical products、sealed mapping/support 规则、exact path/size/anchor metadata
及 provider-bound identity envelope。raw body、lazy loader、repository handle 和 expected answers 留在禁止项；expected
projection 留在 application。明确新增输入与独立版本，不编辑 frozen `/0.1` keys/table 或自动升级旧 history。

fixed audited closed worker 仍是普通 Python process；本审计不证明任意第三方 Provider 的 filesystem sandbox。
product-only 的证明依赖受审 worker 与 input boundary，不借这些结果宣称通用安全隔离。

## 6. 核账、生命周期与反查 verifier

有限内容模型检查完整结果、合法 identical duplicate、遗漏、额外 item、same ID/wrong bytes 与 incompatible duplicate。
每个 required Provider 独立对 E 核账，不能靠两个 partial reports 的 union 修复各自未履责。optional ordinary failure
可留下 gap，但不得变成 all-provider complete。真实 child start、one terminal、完整 release 与实际 run provenance
还必须独立成立；纯函数 oracle 本身不能拥有 execution authority。

synthetic identity/lifecycle model 的最终 23 个 case 对四份稳定 semantic inputs 同得预注册结果，SHA-256：

```text
51359b7f5c10301714c24dfcb9d2fe66aedfa90712cd75675e839fa268ba7163
```

这是一个 audit host 对四份 inputs 的模型核账，不是四格实际 Provider execution。其 case 包括 required missing/
duplicate/partial、union repair、foreign attempt/product/run、双向 reported IDs、duplicate terminal、release failure、
self-report without completion、optional ordinary failure、fresh equal-limits context、旧版本、raw/oracle leakage 与零 E。

反查 v1 model 时，optional unsafe release 返回 `(required=true, all=false)`，与 doc252 §8 不符。该首个观察归为
`AUDIT_RECONCILIATION_MODEL_INSUFFICIENCY`，不是 runtime/contract counterexample。v1 的 21-case PASS 仅保留原
corpus 身份；新 v2 增加 whole-attempt/shared safety state 和 any-source unsafe-release gate，并独立检查两个新增 case。
旧模型、计划、结果与 finding 未修改。ordinary optional gap 与 unsafe release / shared stop 必须分离。

真正的 one-shot、original BudgetContext object、foreign history 和 residue-free child/lifecycle 仍以既有 private primitive
及 unchanged regression 的原范围为 witness；本模型没有产生这些 live authority。successor 必须重新落实并被直接反证。

## 7. 首败、未知与证据归属

首个 product block 的 3.10 normal 在第九个 world 停止：fixture 把 UNCLASSIFIED 写成 scope disposition，触发冻结
Policy validator 的 INPUT_REVALIDATION_REJECTED。正确字段是 source_class，scope 仍为 IN_SCOPE。
身份为 `INVALID_AUDIT_FIXTURE_SETUP`；前八个 world 的 11 个实际 Parse children 与 52 份 immutable artifacts 保留。

v2 只改 audit fixture，另建 plan 与全新 attempt 2，全部九个 world 重做四格。该新 PASS 不覆盖首败；44 个最终 Parse
children 不包含首败的 11 个。追溯总数为 55，不能把 55 写成最终合格矩阵的规模。

doc253 的匿名额度耗尽、直连 DNS、HTML Accept header、read-path setup 等诊断继续非资格化；最终 formal history 为
3 PASS / 0 formal non-success，不能把这些 diagnostics 改写成正式 ERROR。旧 formal ERROR、CANCELLED、hard-exit
UNKNOWN 及上游证据仍由各自 owner 保存。文件检索的 operator path/glob 错误不作产品失败。

## 8. 最小实现候选面与硬停止线

本轮没有发现必须扩 public Schema、persistence 或 Coverage 才能表达的机制；有限模型与现有 primitive 支持继续
审查 private feasibility。但“没有发现反例”不等于 successor 实现成立，完整施工权仍须独立授权。

后继候选面只可能包括：exact upstream revalidation；完整 U/E 与 typed projection blocker；独立 `/0.2` descriptor/
allow-list/operands；product-only worker；per-Provider one-shot child；完整内容和双向 provenance admission；required/
optional/safety join；zero/unknown 阻断；same-attempt FactSet/continuation；FPFCT-001–024 的直接实现反证。

如果需要 raw-source reparse、Provider 自定 denominator、expected-answer 补写、改 frozen kind/identity/nullable rule、
把 unsupported world 改归 Parse REJECTED、放宽 Budget、共享 attempt authority、改旧 `/0.1` 或扩 public surface，必须停。
真实语义反例才显式 reopen 被击穿的最小 frozen boundary；不能为工程便利静默改合同。

## 9. 本候选自己的资格门与后继授权

本轮 tracked scope 只有 README、AGENTS、milestones 与本文。所有 runtime/tests/workflows/Schema/fixtures/Profile/
Policy、doc120/160/217/245/247/249/250/251/252/253 及架构资产保持基线字节。

final bytes 的本地门为：上述 sealed audit blocks 与保留首败核账；unchanged Parse/product-consumer/source-operation/
multi-Provider 六个窄模块和三个 R1 Schema modules 的声明四格；UTF-8 without BOM、LF/final LF、scope、其他 tracked
bytes continuity、links/fences/headings、敏感字面量、diff check 与只读 hygiene。harness resource samples/outer timeout
不修改产品预算。实际 counts/skips 和结果另记 final qualification Artifact，本节不冒充已执行 PASS。

```text
final docs-only candidate / declared local gates
    -> original PR qualification
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / this audit / milestones installed-product observations
    -> independent Core, source-byte and retained-history reconciliation
    -> FEASIBILITY_AUDITED
    -> return CONTROL LOOP
    -> separate explicit implementation authorization, if still the minimal legal seam
```

own chain 闭合以前只保留 FEASIBILITY_AUDIT_CANDIDATE；其后也没有 PRIVATE_IMPLEMENTATION_ALLOWED。
本轮不发布 implementation authorization，不启动 successor runtime、Schema、public carrier、persistence、Fact→Coverage、
ReviewSliceSet/Coverage、Evidence/Bundle/publisher、CLI/Workbench/Core、其他顶层轨、CLAIM_FIDELITY、tag 或 Release。
