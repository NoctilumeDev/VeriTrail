# R1 Fact projection / fulfillment 私有实现候选

> 本文认领 doc255 A–J 的私有实现，不重开 doc252，不发布 FROZEN，也不授予后继施工权。

## 1. CONTROL LOOP 与当前授权

本轮从 exact `main@46eb3ab55bdeea17cd5e6bd2bf614a05b109c0f6` 建立独立实现分支。
[doc252](252-r1-fact-projection-universe-and-fulfillment-contract.md) 合同与
[doc254](254-r1-fact-projection-fulfillment-private-implementation-feasibility-audit.md) 字节保留。
[doc255](255-r1-fact-projection-fulfillment-private-implementation-authorization-publication.md) 的授权最后门已经闭合：
四份 fresh README/doc254/doc255/milestones 各 P1/P2 COMPLETE、Core PASS，同一 publication world；
4 qualifying PASS + 1 formal ERROR 原身份保留。independent reconciliation 为
`ebffc0fcdda1d1072ef7539a9f7413592c5732644ff00924f534057d68413644`，177-artifact closeout 为
`5d681ade0bbfd1dbf426b8ceebed90dffb209d405b67b0dfc48ad4f3127495c3`。

新一轮源码、远端 main、并行 PR 与封存产物核对没有发现击穿 A–J 的新事实；用户另行明确切换本轮阶段到 A–J。
这不是由文档编号或 CI 自动调度。旧长目标中的 docs-only current-stage clause 不再代表本轮范围。

## 2. 私有实现边界

新增独立 consumer `r1-parse-product-fact-consumer/0.2` 与 protocol
`veritrail-review-parse-product-fact-cell/0.2`。全部代码位于 `veritrail_review` 私有模块，未改 package exports。
旧 `/0.1` controller/protocol/worker、closed descriptors、历史 tests 和 frozen contracts 保持原字节。

| 阶段 | 本候选实际机制 |
| --- | --- |
| A | 从 owned Parse closure 消耗原 continuation；复算 exact inputs/classification/eligible denominator，验证完整 product-set 与原对象身份 |
| B | application 遍历全部 CPython 3.10 fields/LIST；独立构造完整 U 与 provenance-free E，保留 nullable mapping、collision、unrepresentable blockers |
| C | 独立 `/0.2` closed descriptor/allowlist、projection/request/terminal validators 与 execution digest domains；保留旧 semantic Fact domains |
| D | copy-owned product-only 输入携带 sealed module mapping；不携带 raw body、repository loader、U 或 E；fixed worker 自行遍历产品 |
| E | 每个 admitted required/optional Provider 获得完整产品集合与独立 one-shot claim；复用 Windows bounded child primitive，保存实际启动、终态与释放 witness |
| F | 每个 record 绑定 assigned product/node/alias/run；比对完整 canonical semantic bytes 与 application E；reported IDs 与实际 Facts 双向核账 |
| G | serial join 保留每个来源责任；ordinary required failure 仍执行后续安全来源；optional gap 保留，任何 unsafe release/shared stop 阻断 normal join |
| H | zero denominator 与 all-rejected 保留各自 complete Parse partition；不启动 Fact child，不形成 empty FactSet；unrepresentable U 保留且阻断 assignment |
| I | 完整对账后才形成 FactSet 与 one-shot private continuation；继续绑定原 BudgetContext 对象、deadline、eligibility 与 Parse history |
| J | FPFCT-001–024 直接反例、独立手写 gold、common-mode omission mutant、实际 reference Parse/Fact children 与四格语义字节比较 |

application 的完整 U/E 与 worker 的遍历分开；expected values 不进入请求。MODULE 即使 source 为空也有 obligation；
METHOD 仅由 direct ClassDef.body LIST edge 决定。Parser-normalized keyword 无法表示时不改名、不跳过、不改归 Parse REJECTED。
U 完整但 E 不成立的 world 没有 ordinary claim、FactSet 或 continuation。

MODULE mapping 先检查 raw component 的 3.10 repertoire，再 NFKC 与 frozen identifier/keyword；只有 raw ASCII
`__init__.py` 省略末 component。对当前 conformance 宿主 Unicode 13.0.0/15.1.0 之外的 normalization host 明确拒绝，
不把 finite corpus 证明扩大成任意未来宿主保证。AST field inventory 来自显式 CPython 3.10.6；unknown/missing node fields
或位置 fail closed，不剥除后继 AST fields 来假装兼容。

## 3. 保留面与 proof strength

owned closure 保留 parent/Parse continuation、完整 application projection、child observations 与 copy-owned FactSet。
每份 observation 在产生时立即进入 parent 的 execution history，不能等全部来源结束后才保存；reconciliation 的输入历史另存，
后继 child 异常或 claim 前 shared stop 不抹掉前面已完成的 observation。未知 release 不能作为 optional ordinary gap。
observations 保留 exact terminal/frame bytes 与执行 witness；closure document 记录 request、lifecycle、执行事实、reported IDs
并以摘要绑定原 terminal/frame。失败 reconciliation 的 observations 仍由原 parent 保留，不能只保留最后合并集合。

这仍是 fixed audited closed conformance worker。普通 Python 进程具有宿主能力；本候选不宣称通用第三方 Provider filesystem
sandbox。stateless protocol validator 不拥有 live continuation authority，也不能独立认证任意 Provider 未使用其他宿主输入。

## 4. 直接反例与有限 witness

新增 `test_fact_fulfillment.py` 的 28 个用例覆盖 FPFCT-001–024：mapping 与 input drift、nested/direct method、sync/async、
多 alias/relative/wildcard、空 source MODULE、raw anchors、unrepresentable/absence/collision/raw init、unknown node/end position、
common-mode omission、两个 required 各做一半、partial/wrong/foreign/duplicate output、optional gap、完整 serial responsibility、
product-only/no oracle input、foreign attempt/equal-limits context、zero/missing distinctions、any-source unsafe release/shared stops、
完整内容与双向 provenance、旧 `/0.1` identity、one-shot/copy ownership 和真实 reference Parse/Fact children。
附加直接反例覆盖后继 child 异常/claim 前停止的历史保留、outside-root 与无效 UTF-8 path 的 nullable MODULE；旧 `/0.1`
移植反例使用语义内容完全相同的 MODULE world，仍拒绝跨版本 execution authority。

common-mode mutant 同时删掉 application 与 worker 的 IMPORT，可以形成内部自洽的错误成功；独立预先写定的 14-slot gold
必须拒绝它。这验证的是 gold/falsifier 能发现该 mutant，不是宣称 evaluator 不可能出错。

四格 actual corpus 固定 11 worlds/cell，共 **52 actual reference Parse children / 56 actual bounded Fact children**；
其 U/E、mapping history、negative states 与去 provenance 的 FactSet 语义字节完全相同。nonce-bound terminal、run/attempt
身份不参与跨 world 继承。有限 Unicode corpus 检查全部 `0x110000` codepoints 的四类谓词及 11 个 module component gold，
true counts 为 `131460 / 134415 / 128049 / 130889`，四格 canonical 结果一致；它不证明所有字符串或未来 Unicode 行为。

## 5. 首败与错误身份

- 首轮 `310-normal`：26 reported，33 errors（含 subtests）；新 initializer 在 qualification 赋值前创建 claims。
  归为 `NEW_PRIVATE_IMPLEMENTATION_DEFECT`，修正本候选初始化顺序，原日志/源字节 seal 不覆盖。
- 第二轮：26 reported，1 failure；raw-init 手写 gold 未显式配置 empty package_prefix，而 fixture 封存了 `[pkg]`。
  归为 `TEST_GOLD_MAPPING_SETUP_ERROR`；新身份明确封存该 world 的 empty-prefix rule，不改产品 mapping 算法。
- fresh GraphQL open-PR inspection HTTP 504 属 metadata transport setup；独立 REST 观察成功，不归产品失败。
- 首个完整 `310-normal` local suite 在 600 秒 harness outer containment 终止，缺少 suite terminal count，未取得资格；
  已输出日志未观察到 assertion failure，不能据此宣称产品 PASS。新 local block 独立预声明 1200 秒 outer containment，
  产品 budget/timeout 与 workflow 字节不变。
- source review 发现 serial helper 直到 join 才保存 observations 的 retention 缺口，补 observation-time retention 与直接反例；
  一次证据目录/worktree 路径混淆的 patch 被工具在写入前拒绝，归 operator path setup，不归产品。
- 上游 doc255 formal README ERROR、旧 marker setup、匿名 quota 差异 UNKNOWN、doc254 fixture/model 首败及更早历史身份保留。

后来的 PASS 不改变这些原身份；本候选不重写上游历史文档。

## 6. 本层自己的资格门

最终源字节必须取得：完整 Review Attention 3.10/3.13 normal/`-O`、有关上游 seam 与 Schema checks、上述独立 corpus/identifier
核对、docs/link/boundary/hygiene。然后 original PR gates、单独批准 exact-head protected merge、新 exact-main Public CI +
Browser Smoke、fresh installed-product README/本文/milestones observations 与 independent Core/source-byte/Bundle reconciliation。
每份 observation 属于本实现同一 exact world，任何 non-success 保留原 identity；不借 doc255 的四份 PASS。

这些门闭合才有 implementation candidate 的 source/readback 资格；FROZEN 仍须独立实现事实发布及其自己的完整最后门。
本地 housekeeping 不追加语义门。本文不预写未来 head/merge SHA、workflow run 或尚未完成的 PASS。

## 7. 当前状态与后继停止线

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本候选不是 exact-main verified/frozen。禁止 persistence Route A/B、zero-member Fact-stage closure、Fact→Coverage handoff、
Relation/Slice/public assembler、ReviewSliceSet/seven-stage Coverage、public Schema/carrier、Evidence/Bundle/publisher、
CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。若反例要求这些能力、raw reparse、向 worker 发送 E、改变 frozen Fact
identity 或预算，则保现场并只重开被击穿的最小边界，不顺手实现。
