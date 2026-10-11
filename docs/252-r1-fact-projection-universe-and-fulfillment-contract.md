# R1 Fact projection universe / fulfillment 最小合同 0.1

> 状态：`R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_CANDIDATE`。
> 基线：`main@07e3e90e6b7976c660ae7643b0cde79cb9b97a8a`。
> 影响：`L2_CONTRACT + L3_SYSTEM_DESIGN + L0_DOCUMENTATION`；只形成语义合同候选，不授权实现。
> Parse / consumer A–J 的冻结历史不重写；persistence OPEN，Coverage 与 public carrier 未授权。

## 1. 本轮问题与已取得的资格

[doc251](251-r1-fact-projection-fulfillment-current-state-audit.md) 经 [PR #289](https://github.com/NoctilumeDev/VeriTrail/pull/289)
进入本基线。final head 为 `d3cb2aadc4885fd21446f4752843351fef754fad`，两个 commits；受审与 merge tree 同为
`ea70122eb45f240c0eb03ca956096385c269f8d6`。original Public CI `38166052364`、exact-main Public CI
`38167806238` 均 attempt 1 / 11 of 11 SUCCESS；Browser Smoke `38167806265` attempt 1 / 1 of 1 SUCCESS。
README/doc251/milestones 三份 fresh anonymous installed-product observations 均 P1/P2 COMPLETE、Core PASS；
independent reconciliation `d788554a27dbeb6f5c0d02fb19938e3c8e228c5b1d2e5084b792d35451677ad2` PASS。

当前问题是：admitted Parse product 与 product-only consumer 已存在，怎样从完整冻结输入机械构造 Fact 全集，
并证明每个 required 来源的输出完整、正确归属，而不是从实际输出倒定义 denominator？

本合同区分三种事实：**全集可独立构造、child 实际执行、输出完整核账**。不新增逐项 execution receipt，也不声称
对账能证明 Provider 的内部算法逐步执行。反例若要求这种更强 claim，必须另审，不能追加到当前 fulfillment 含义。

## 2. Authority topology

| Authority | Owner / 边界 |
| --- | --- |
| scope、Fact kind/属性规则、requiredness | Human Seal / Policy / Profile；Provider 不得解释或扩张 |
| canonical AST 与成功/拒绝 partition | frozen Parse function、admitted product set 与完整 Parse history |
| exact source/path/anchor | frozen Snapshot、copy-owned verified bytes、application 的受审坐标翻译 |
| universe、expected semantic projection | application 执行本合同的版本化机械规则；不消费 Provider outputs 来构造 |
| actual candidates | 各自 product-bound、one-shot、bounded child；不能认证自己 complete |
| fulfillment、provenance 与 continuation | application 逐来源核账，再按冻结 requiredness/lifecycle join |

application 拥有规则执行权，不拥有自由修改规则的权力。Core、caller、publisher、Coverage 不能反向选择 denominator。

## 3. 版本与兼容范围

本合同的资格函数身份为 `r1-fact-projection-fulfillment/0.1`。五种 Fact 的内容语义继续使用
[doc120 §6–7](120-r1-schema-and-canonical-identity-contract.md) 的 `r1-python-facts/0.1`、
`r1-python-import-literal/0.1`、Python 3.10 identifier 规则、既有 subject/fact digest domains 与 Profile rank。
本合同不更改 public Fact identity、Schema、Profile 或 Policy。

未来 private consumer 必须使用显式 successor `r1-parse-product-fact-consumer/0.2`；其 private request/terminal
协议使用独立 `veritrail-review-parse-product-fact-cell/0.2` 身份。新增的 Policy mapping 输入、五类投影与完整输出
admission 不能塞进 frozen `/0.1`，也不能让旧 request、terminal、closure 或资格 token 被自动升级。

首版仅继承 [doc160](160-r1-multi-provider-applicability-and-fact-composition-contract.md) 的 closed capability membership、
descriptor cardinality、requiredness 与串行 lifecycle 规则。successor 的实现 descriptor/handle 必须独立绑定版本和
final bytes，经后继 feasibility/authorization 审查；不静默改旧 closed table，不建立 public Provider SPI/registry。

若五类内容规则本身需要变化，单独提升 consumer version 不够，必须显式 reopen 对应 frozen semantic boundary。

## 4. 完整输入与两种身份

构造函数至少消费并重新验证：

```text
exact Snapshot + sealed Policy + frozen Profile
complete admitted Parse product set / partition / function identity
all and only ACCEPTED subjects and their canonical products
matching exact path, blob identity/size and owned byte-anchor history
relevant Policy scope and python_module_mapping semantics
this versioned projection/fulfillment function
```

不允许单独的 AST、product digest echo、Provider path list 或未封存的 mapping 替代这组输入。完整 Parse denominator
与 accepted/rejected partition 必须已独立 reconciled；missing、duplicate、foreign 或 lifecycle failure 不能变成空集合。

semantic input projection 绑定上述 Fact 相关语义；原始 Snapshot/Profile digest 与已有 Fact identity 的关系保持不变。
budget、governance 与 ProviderRun 不进入单个 Fact 的 content identity，但完整 Policy seal、analysis scope、Parse
admission history、Provider responsibility 与 original attempt 必须在 authority envelope 中独立连续。
不能仅以 full policy digest 相等代替检查 mapping，也不能因 semantic result 相同继承另一 attempt 的 authority。

raw bytes 只由 application 用于已冻结的 integrity/anchor 翻译，来自 verified owned inputs；不重新读 mutable path。
child 的 source semantics 继续来自 assigned products；immutable mapping、path/size 与 anchor metadata 是明确的附加
规则输入，不是重新获取 raw source 的能力。不得交付 source body、lazy loader、repository handle 或预先算好的 expected
Fact 集合作为 child 的答案。expected projection 留在 application 的核账侧。

## 5. Total universe construction 与 normal projection qualification

本节对合格冻结输入给出唯一机械结果；typed negative result 是结果的一部分，不能用成功前缀冒充完整全集。

### 5.1 完整结构枚举

按 exact raw Git path 排序处理全部 ACCEPTED products。每个 product 必须是 frozen Parse 交付的 Module canonical tree。
树中的 AST fields 按规范 field-name 顺序递归，LIST 保留原 item 顺序，scalar/none 为叶；不按宿主 AST API 重建。
所有 fields 都要访问，不能只遍历 body、已知声明或实际输出出现的节点。

| AST position | obligation / expected kind |
| --- | --- |
| 每个 accepted Module | 恰好一个 MODULE，raw anchor `[0, size_bytes)`，ordinal 0；空 source 也存在 |
| 每个 ClassDef | 一个 CLASS_DECLARATION，使用该 node 的 exact anchor，ordinal 0 |
| 每个 FunctionDef / AsyncFunctionDef | 一个声明；直接作为 ClassDef.body 的 LIST item 才是 METHOD，否则 FUNCTION |
| 每个 Import / ImportFrom 的 names item | 一个 IMPORT_DECLARATION；statement anchor 相同，ordinal 按原 alias 顺序从 0 开始 |
| 其他 AST nodes | 不产生 CodeFact，仍递归其 fields；不丢弃内部声明/import |

METHOD 的判断使用**直接结构边**，不使用 nearest lexical container、缩进、同名、anchor 包含或 parent path 前缀猜测。
例如 class 内 if body 的函数是 FUNCTION；直接 class body 的 async 函数是 ASYNC METHOD。条件/循环/try/with
不变成 Fact container；本文不因此生成 Relation。

每个槽位从 Snapshot/Profile、exact raw anchor、subject space 与 local ordinal 复算 doc120 的 `subject_key_digest`。
全集 `U` 是这些 subject identities 的唯一集合，规范顺序按 digest 排序；保留到 product、node position、alias ordinal
的反向关联。两个不同槽位出现同一 subject key 是构造/integrity failure，不能去重后缩小 U。
`fact_id`、Provider output、reported IDs 与 FactSet member count 都不能成为 U 的来源。

枚举必须证明：每个 accepted Module、每个适用声明节点和每个 import alias 被访问并进入 U 恰好一次；无额外槽位；
来源树/fields/LIST 无删减。手工 gold worlds、mutation 与独立 conformance 用于攻击这个函数；测试数量不授予通用完整性。

### 5.2 Expected semantic values

对每个槽位独立构造 provenance-free expected Fact，记为 `E`：

- CLASS 取 reference product 的 parser-normalized name。
- FUNCTION/METHOD 取同一 name，FunctionDef 为 SYNC、AsyncFunctionDef 为 ASYNC。
- Import 每个 alias 的 name 按 ASCII dot 拆为 module_parts，relative_level 为 0，imported_name 为 null；
  ImportFrom 取其 module（None 对应空 parts）、level 与各 alias name；asname 未声明时为 null，wildcard 的 alias 为 null。
- 不重新 normalize 或猜测 source spelling；名称仍须通过 frozen Python 3.10 PythonIdentifier 与 kind/attribute 规则。
- MODULE.module_key_parts 按 5.3 从 sealed mapping 与 exact path 计算，不用 AST/import machinery/环境推断。

所有 anchors 都来自受审 raw-byte 翻译；BOM、CRLF/LF/CR、多字节字符宽度和 AST end position 不得猜测或统一后误报。
doc120 的 digest 函数与排序不变。E 与 U 的 key 必须一一对应；输出普通 FactSet 的前提是每个 expected value 可合法表示。

### 5.3 Module mapping 与 nullable 属性

只按 doc120 的 module_root/package_prefix 规则处理 exact path：按 raw path component 判断是否在 root 内，剥离 root，
去掉末尾 ASCII `.py`；**raw basename 恰为 ASCII `__init__.py`** 才省略其最后 component。其他 component 按 frozen
Python 3.10 NFKC/identifier/非 keyword 规则获得 module parts，再接上已封存 prefix。不得跟随 symlink、case-fold、
查询 sys.path、访问 package 或使用宿主 import resolver。

不能唯一映射的 path 按 frozen nullable 规则形成 module_key_parts=null；对应 mapping limitation 必须可从完整输入
独立复算并保留，不能解释成没有 MODULE。不同 raw paths 映到同一个 normalized module key 时，保留各自 MODULE/path
身份与 collision 关联；不得任选、合并路径或把跨 subject collision 冒充 doc160 的 same-subject FactConflict。
本文不认证 import resolution 或 Coverage typed-gap closure。

### 5.4 可枚举不等于可表示

Parse ACCEPTED 只承诺 grammar product。source 可以出现全角 `ｉｆ` 名称：reference CPython 3.10.6 接受 class/function
声明，AST name 为 `if`；该名称却不满足 doc120 的非 keyword PythonIdentifier。

因此 obligation 存在可以已知，但 expected Fact 不一定可在冻结属性闭集中表示。对于这类 world：

```text
retain complete U and exact incompatible product/slot evidence where identities can be constructed
normal expected projection qualification does not hold
no ordinary Provider assignment / FactSet / normal Fact continuation
```

不能跳过该声明、把它写成“不存在”、修正名称、改归 Parse REJECTED、制造 Provider failure 或缩小全集。如果完整
subject identities 因 input/admission/anchor integrity 无法构造，则连 ordinary U 都不成立；只保留失败现场，不输出较小
KNOWN universe。具体 private status/reason carrier 留给 implementation audit，不扩 public enum。

本候选的 totality 是“完整可表示投影，或明确的 projection/input qualification 阻断”，不是承诺所有 grammar-accepted
输入都能成功生成五类 Fact。若要扩大 Fact 属性表达范围，必须另审 frozen identity/Schema，而非在本实现修复。

## 6. 每个 Provider 的 responsibility

首版选择**每个 existing-applicability admitted Provider 都负责完整 U/E**。required 与 optional 都不能选择 kind、node、
product subset，也不按 caller 配置分区。每个 Provider 收同一完整 accepted product set 与规则输入，取得独立 one-shot
claim、child attempt 与 run；共享一份 Parse truth，不重复 parse 或复制 admission witness。

requiredness 仍在 capability requirement 上继承；optional 不等于没有 obligation。optional 失败不单独使 required join
失败，但其未履责历史必须保留，不能报告“所有 Providers complete”。一个 required 来源填补另一个 required 来源的
遗漏、merged union 恰好等于 E、或者 CUMULATIVE 标记，均不能替代逐来源资格。

heterogeneous/per-kind responsibility 不在 0.1；若现实反例要求它，必须先版本化 applicability/responsibility 规则，
不能用输出分布反推 responsibility。此选择只限 closed private conformance path，不承诺公开通用 Provider 能力。

## 7. Fulfillment predicate 与 admission

对于每个合格的、非空 U/E，Provider fulfillment 必须同时成立：

```text
one exact provider-bound claim consumed in the original live attempt
truthful bounded child start / one terminal / residue-free release
terminal identity, product set, function and operands exact
every record resolves to its assigned product/node/alias and frozen semantic value
application-canonicalized provenance-free output == E, independently recomputed
run/fact provenance closes in both directions
```

比较完整内容与身份，不只比较 count、digest 字符串或 ID 集合。少一个、额外一个、wrong kind/form/attribute、错误
mapping、anchor、ordinal、foreign product/attempt 或不兼容 duplicate 都不能 admission；不得删除错误记录后接纳其余。

沿用 doc155/160 对 byte-identical semantic duplicates 的规范去重，不把重发同一 candidate 解释成额外履责。保留 raw
terminal 历史，canonical E/U 必须唯一；duplicate terminal frames 或 duplicate child history 仍拒绝。这不证明逐项
exactly-once execution。same ID/different bytes 与 same subject/incompatible value 仍按既有 integrity/run-local 规则处理。

E 非空时合法空 terminal、partial output 即使声称 COMPLETED，也不满足 successor admission。source 不含某类声明的
absence 来自完整 U/E 构造；不要求 Provider 对不存在的 item 发 negative receipt。

application 不把 expected values补进实际输出，不补造 ProviderRun、不把 oracle 自己完成投影当作 child 执行。
共享纯函数代码不等于独立软件反证；gold semantics、遗漏/属性 mutation 与 verifier falsifier 必须独立攻击构造和核账。

## 8. Multi-Provider join 与冲突边界

只在所有仍可安全执行的 applicable children 真实终态并 release 后核账。普通 required/optional failure 不获得
first-success/first-failure short-circuit 权；unsafe release、whole-attempt stop 或 shared-context/integrity failure 除外。

逐来源成功必须先通过第 7 节。required source 缺失、non-success 或输出不等于 E，不能形成正常 fulfilled FactSet。
optional non-success 保留 source gap/diagnostic；不提交 partial Facts。所有 required fulfilled 且预算/identity 仍有效时，
按 doc160 合并合法 completed 来源：semantic E 不变，provenance 只汇总真实报告并通过核账的 runs。

本 successor 对同一个确定 E 的错误 candidate 不能借 FactConflict 获得资格；它应在 run-local admission 拒绝。
这不删除或改变 broader frozen FactConflict、Relation 或 Slice 合同。未来真正可合法分歧的 projection 必须另审，
不得给本函数临时选择 winner 或改变 oracle。

FactSet construction、required-provider fulfillment、all-provider fulfillment 与 publication 是不同 claim；optional gap
不能从正常 FactSet 内容中被推成不存在。最终 Evidence reported IDs 的清空/发布规则仍由既有合同与未来 publisher 拥有。

## 9. Zero-member 与 unknown worlds

| World | U / normal authority |
| --- | --- |
| 至少一个 accepted product，包括 empty source | 至少一个 MODULE；U 不会为空 |
| zero Parse denominator、完整 reconciliation | 可机械知道 accepted-derived U 为空；保持 exact upstream 身份与 consumer 阻断 |
| all rejected、完整 reconciliation | 同样可知道 accepted-derived U 为空，但 denominator/rejection/history 与上一行不同 |
| missing / lifecycle non-success / foreign / incomplete reconciliation | 无合格普通 U；不能从空 accepted list 得到 known-empty |
| U 已构造而 E 不可表示 | retain U 与 projection failure；无普通 fulfilled FactSet |

零 accepted 继续遵守 [doc245 §9](245-r1-parse-to-fact-consumer-correction-contract.md)：不启动 normal Fact child，
不形成 empty-product request、Fact terminal、empty FactSet 或 normal Fact continuation。本合同没有选择 zero-member
Fact-stage closure；future empty scheduling/closure 必须显式版本化该边界。知道数学集合为空不是 required Provider 已执行。

partial accepted + reconciled rejected 的 U 是**完整 admitted accepted-domain**投影，不是 Provider 实际成功前缀。完整
Parse partition 与 rejection history 必须绑定；它不自动授予 global seven-stage Coverage KNOWN/COMPLETE，也不解释
doc120 的 upstream-unknown 规则。Coverage consumer 必须以后独立核对 stage denominator/negative semantics。

## 10. Same-attempt closure 与 continuation

所有构造、资格复算、Provider launch/canonicalization、reconciliation 与 join 都消费原 BudgetContext 的剩余资格，
不刷新 timeout、memory、artifact limit。原对象身份、deadline、stop latch、eligibility、Parse continuation 与 product
history 必须连续，参数相等的 fresh Context 不成立。

private closure 至少保有/可验证 exact inputs、U/E/function、每个 obligation 的 product/slot 关联、完整 responsibility、
真实 observations/terminal bytes、逐 Provider 对账、FactSet/provenance 与 projection/mapping/optional/negative history。
这些是证明责任，未选择类名、字段、receipt 或 persistence carrier；内存 owned values 可以作为 same-attempt witness。

同语义 U/E 可以在完整输入与函数相同且 independently validated 时复算；normal continuation 必须重新验证本次所有
required fulfillment 与原 live authority，并 one-shot claim。失败后修 output、重建 Context、换 terminal 或复制 closure
不能恢复 normal eligibility。identity/integrity/budget/unsafe release failure 不获得 partial-prefix continuation。

本合同只形成 private Fact-stage continuation，不授予 Fact→Coverage handoff API、Relation/Slice/public assembler 权限。

## 11. Normative falsifier obligations

以下是后继 conformance 必须攻击的语义世界，**不是本轮已实现测试**。

| ID | World | 唯一约束 |
| --- | --- | --- |
| FPFCT-001 | products/Profile 相同，sealed module mapping 不同 | E 使用各自 mapping；不能只认产品 digest |
| FPFCT-002 | unsealed mapping、foreign path/anchor/product 或 Parse history 不完整 | 无 ordinary qualification，不能缩为成功子集 |
| FPFCT-003 | 同名/嵌套/控制语句内声明 | 所有声明各入 U；不按名称去重；直接 class body 才是 METHOD |
| FPFCT-004 | sync/async 与 conditional class function | form 与 kind 各自独立、唯一 |
| FPFCT-005 | multi-alias、relative/wildcard import、asname | 每 alias 一个 slot，原序 ordinal，exact 属性 |
| FPFCT-006 | empty accepted source | 有 MODULE；空 output 不合格 |
| FPFCT-007 | BOM/CRLF/CR/Unicode/decorators | raw-byte anchor 正确；无 host reparse 或 decorator 扩锚 |
| FPFCT-008 | normalized keyword name、不可表示 attributes | U 保留；E qualification 阻断，不造 Parse rejection/absence |
| FPFCT-009 | no imports/functions after complete traversal | absence 可独立复算；不能仅根据零报告认证 |
| FPFCT-010 | 两个 raw paths 的 normalized module key 相同 | 保留两条 subject 与 collision；不选 winner |
| FPFCT-011 | raw `__init__.py` 与 normalization 后同名 | 特殊 basename 判断在 raw path 上进行 |
| FPFCT-012 | unknown/missing node data 或无合法 end position | fail closed；不猜测或跳过槽位 |
| FPFCT-013 | 构造遗漏节点，Provider 跟着遗漏 | verifier/conformance 必须能击穿共同错误；count 一致不足 |
| FPFCT-014 | required A/B 各报告 U 的一半，union=E | 两个来源都未 fulfilled；不按 aggregate 掩盖 |
| FPFCT-015 | required empty/partial 或 wrong semantic value | successor run-local reject，不能继承 /0.1 conformance PASS |
| FPFCT-016 | identical duplicate / incompatible duplicate / duplicate terminal | 按各自冻结边界去重或拒绝；不新增履责次数 |
| FPFCT-017 | required success + optional failure/partial | optional history 保留；不宣称 all-provider complete |
| FPFCT-018 | Provider 次序变化或 first-success 优化 | applicability/rank/requiredness/逐来源账不变 |
| FPFCT-019 | false product-use echo、oracle output补写、raw-body reparse | 无 product-use/fulfillment qualification |
| FPFCT-020 | same U/E、foreign attempt 或 fresh equal-limits Context | semantic equality 不继承 live authority |
| FPFCT-021 | zero denominator / all rejected / missing | empty-derived / blocked / invalid history 不折叠 |
| FPFCT-022 | deadline/cancel/memory/release failure | 原 stop 保留；无正常 FactSet/continuation |
| FPFCT-023 | digest/ID-only comparison、provenance/run 双向不闭合 | reject；不能以漂亮 count 替代内容 |
| FPFCT-024 | /0.1 request/terminal/closure 混入 /0.2 | 即使相同 Fact 内容也拒绝 authority inheritance |

## 12. 本轮 witness 与验证边界

doc251 的九个 finite worlds/四格和 retained artifacts 继续是已资格化 audit history，不是本函数的实现证明。
本轮另在 exact baseline 进行三个反向世界：ASCII class、normalized-keyword class/function。四格每格实际运行三个
fresh reference Parse children，共 12；没有执行 Fact children。AST 都 admitted ACCEPTED，ASCII name 满足冻结
identifier predicate，两个 normalized keyword names 不满足；CLASS 的 modeled terminal 分别 admission/rejection，
FUNCTION 仍在旧 protocol 的 closed scope 外。reduced report 四格同为 1,456 bytes，SHA-256：

```text
0d219416ae955fd8e29613646861a93247b8ed300d9eca079cd7ec80b57b1e3b
```

首次 direct-reference 诊断不作为 admitted-product witness；正式审计在预先固定的 plan 下独立产生。该反例不证明
parser/consumer defect，只迫使 total projection 保留可枚举与可表示的区别。旧观察、ERROR/CANCELLED/UNKNOWN、
preflight warning 与 live diagnostic-log snapshot correction 都保留原身份，不因本候选被解释或覆盖。

本轮 final bytes 的 gates 限于四文件 scope、UTF-8/LF、links/fences/headings、敏感路径、状态边界、全部其他 tracked
bytes 连续、diff check/只读 hygiene，以及 unchanged Parse/product-consumer/source-operation/multi-Provider 窄回归与
R1 Schema regressions 的 CPython 3.10.6/3.13.13 normal/`-O` 四格。最终结果另记资格 Artifact，不能把本节计划冒充 PASS。

## 13. 候选资格、独立冻结与后继停止线

```text
final semantic candidate bytes / declared local gates
    -> original PR qualification / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / this contract / milestones observations
    -> independent Core and source-byte reconciliation
    -> qualified contract candidate history
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN
    -> return CONTROL LOOP / feasibility and explicit implementation authorization
```

即使合同以后冻结，也不自动获得 implementation authority。feasibility 必须证明完整函数、module/identifier conformance、
所有语义 negative branches、independent universe/output reconciliation 与同 attempt continuation 能在原 primitive 内
闭合，并审 successor descriptor/allow-list/worker-input 边界；做不到就重开最小被击穿的 semantic boundary。

本轮不修改 doc120/160/217/245/247/249/250/251、runtime/tests/workflows/Schema/fixtures/identity vectors 或架构图。
不选择 Fact/Parse/Language Support persistence、public carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、
Fact→Coverage API、ReviewSliceSet/Coverage、其他顶层轨、CLAIM_FIDELITY、tag/Release。serialized history 不获得 live authority。

当前只允许写 `CONTRACT_CANDIDATE / IMPLEMENTATION_NOT_AUTHORIZED`。下一步以新的证据和本层自己的门为准，
不按文档编号调度，也不把本候选的 bounded fulfillment 当成 truth completeness、bug completeness 或全仓审查完成。
