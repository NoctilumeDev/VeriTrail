# R1 Fact projection fulfillment 当前状态再审计

> 当前状态：`R1_FACT_PROJECTION_FULFILLMENT_CURRENT_STATE_AUDIT_CANDIDATE`。
> 本文只认领 docs-only current-state re-audit；不冻结 Fact 合同，不授权 runtime。
> 剩余 R1 是条件化目标，本文后面的依赖计划不预授后继 authority。

## 1. exact 坐标与上游闭环

本轮重新绑定 `main@f35d69b337b1961c9e9b54243097250cb962a582`，tree
`8dfa3799881c0323d483326e852e82037f248e70`。本地主仓与 origin 相同；主仓未跟踪文件保持原样，施工使用独立
worktree。并行 open PR 只有旧 Dependabot #164、#163、#16，没有新 semantic PR 改写本 seam。

[PR #288](https://github.com/NoctilumeDev/VeriTrail/pull/288) original Public CI `38151322948` attempt 1 为
11/11 SUCCESS；publication merge 为上述 main。exact-main Public CI `38153642974` attempt 1 为 11/11 SUCCESS，
Browser Smoke `38153642954` attempt 1 为 1/1 SUCCESS。

[doc250](250-r1-parse-to-fact-consumer-private-implementation-freeze-publication.md)自己的最后门已闭合：README #2、
doc250 #1、milestones #1 三份 fresh anonymous installed-product observations 均 P1/P2 COMPLETE、Core PASS；
independent Core/source-byte reconciliation SHA-256 为
`e92e0bf7afd9d5acb184016f751d5288a56e901e67e292c1629f99d8e6b9bfe4`。

README #1 是正式 ERROR：Plan marker 在默认折叠的 details 内不可见，P2 正确使用可见 innerText；不归因于产品
失败。新观察前显式修订 marker selection 并使用全新 Plan/session，旧 Plan/Evidence/output 保留。六份 render
diagnostics、两份 DOM diagnostics、匿名 API 403 与 setup warning 均不计入正式资格。closeout SHA-256 为
`d433fe23d717a5110b291bf088145af91084a012e09dd4fa2040bbe598af5d13`。

因此本轮消费的上游是已生效的 private Parse fulfillment 与 Parse → Fact consumer A–J freeze，不是候选 target。
它们证明 product、claim、candidate provenance 与 child lifecycle；不证明完整 Fact 正确性或 fulfillment。

## 2. 当前问题与历史 claim domain

[doc195](195-r1-language-support-parse-fact-fulfillment-problem-boundary-audit.md)在旧 world 中没有 application-owned
AST carrier。这个事实继续作为历史保留，但不能继续作为当前阻塞理由。现在 admitted canonical Parse product、
完整 reconciliation、same-attempt continuation 与 product-only child 都已经存在。

当前最小问题变成：**已有上游能否支持完整 Fact 候选枚举；谁拥有枚举的 authority；现有 history 能否证明该全集
逐项履责，而不由 Provider 从实际输出倒定义 denominator？**

[doc245 §8–9](245-r1-parse-to-fact-consumer-correction-contract.md)明确没有承诺 per-product Fact completeness，并且
zero-accepted 时阻断 normal Fact child。不能因为下游需要更多证明，就把当前实现认定为违约。

## 3. 冻结规则与当前结构

当前 Profile 固定 `PYTHON_3_10`，包含五种 Fact：MODULE、CLASS_DECLARATION、FUNCTION_DECLARATION、
METHOD_DECLARATION、IMPORT_DECLARATION；`fact_projection=r1-python-facts/0.1`，
`import_projection=r1-python-import-literal/0.1`。reference Profile digest 为
`e8bbe54140ff2a082b69d6b6967d8630a423abd135ac6e7be0badc1fe053125b`。

[doc120 §6–7](120-r1-schema-and-canonical-identity-contract.md)已经规定 Fact 粒度、属性与身份：

- 每个 module entity 有 MODULE，anchor 是 `[0, size_bytes)`；空 source 不取消 MODULE；
- ClassDef、FunctionDef、AsyncFunctionDef 保留声明；只有直接 ClassDef.body 中的函数属于 METHOD，其余是 FUNCTION；
- 每个 import alias 是一个 Fact，共用 statement anchor，以源码 alias 顺序给 local ordinal；
- 条件、循环、try/with 不增加 CodeFact container；nearest lexical parent 与直接 class-body 方法分类是不同判断；
- MODULE.module_key_parts 由 sealed Policy.python_module_mapping 与 exact Git path 派生，不能从 AST 或实际 import 获得；
- identity/anchor 继续依赖 exact Snapshot/Profile/path/raw-byte history，provenance 不进入 Fact content identity。

当前源码链是：

```text
explicit CPython 3.10.6 Parse worker
    -> all AST fields / present attributes as canonical data
    -> admitted OwnedParseProductSet + claimed original continuation
    -> application exact-byte anchor mapping
    -> complete accepted-product projection for each applicable Provider
    -> fixed MODULE/CLASS-only conformance worker
    -> per-record product/node/run admission
    -> child lifecycle / reported-Fact composition / original-attempt continuation
```

源码入口：[Parse worker](../plugins/review-attention/src/veritrail_review/_parse_fulfillment_worker.py)、
[product values](../plugins/review-attention/src/veritrail_review/_parse_fulfillment_values.py)、
[consumer](../plugins/review-attention/src/veritrail_review/_parse_product_fact_consumer.py)、
[protocol/admission](../plugins/review-attention/src/veritrail_review/_parse_product_fact_protocol.py)、
[anchor translation](../plugins/review-attention/src/veritrail_review/_parse_product_fact_anchors.py)。

## 4. 九个 world 与 witness 边界

审计计划在观察前固定。仓库外 helper 复用现有 synthetic exact-input fixtures；每个 world 重新取得 Parse attempt、
BudgetContext、eligibility 与 child claims，真实运行 reference Parse 与固定 product-only workers。未在宿主 reparse，
未把审计枚举器放进 runtime。预算使用现有 test helper 的 testing admission：60s / 512 MiB / 64 MiB；不声称它是
sealed production Policy budget 的资格。四格严格串行，终止点立即固定 live state，不延迟到后续 world 才读。

“结构槽位”只用于对照冻结规则和夹具，不是 normative denominator。下表中的候选数量预先手工确定。

| World | Parse denominator / accepted / rejected | 审计结构槽位 | 每个真实 child 报告 | Child 数 / 状态 |
| --- | --- | --- | --- | --- |
| rich | 1 / 1 / 0 | MODULE 1、CLASS 1、FUNCTION 3、METHOD 2、IMPORT 3 = 10 | MODULE 1、CLASS 1 | 2 / COMPLETED |
| empty-source | 1 / 1 / 0 | MODULE 1 | MODULE 1 | 2 / COMPLETED |
| nested | 1 / 1 / 0 | MODULE 1、CLASS 3、FUNCTION 3、METHOD 2 = 9 | MODULE 1、CLASS 3 | 2 / COMPLETED |
| imports | 1 / 1 / 0 | MODULE 1、IMPORT 5 = 6 | MODULE 1 | 2 / COMPLETED |
| two-accepted | 2 / 2 / 0 | rich + empty module = 11 | MODULE 2、CLASS 1 | 2 / COMPLETED |
| all-rejected | 1 / 0 / 1 | 不枚举 | 无 child / FactSet | 0 / BLOCKED_NO_ACCEPTED_PRODUCTS |
| zero-parse-denominator | 0 / 0 / 0 | 不枚举 | 无 child / FactSet | 0 / BLOCKED_NO_ACCEPTED_PRODUCTS |
| policy-variant | 1 / 1 / 0 | rich = 10；仅 sealed module prefix 改变 | MODULE 1、CLASS 1 | 2 / COMPLETED |
| advisory | 1 / 1 / 0 | rich = 10 | 三个 child 各 MODULE 1、CLASS 1 | 3 / COMPLETED |

Python 3.10.6 / 3.13.13 normal / `-O` 四份独立 reduced report 为逐字节相同的 86,947 bytes，SHA-256：

```text
eead1af820adb0fe3968a44a3c0f4a4fe90e1d44b9212633c45849d6be4633f9
```

九个 world × 四格，实际执行每格 9 个 Parse children 和 15 个 consumer children。每个 raw request、terminal/frame、
Parse product、consumer closure 和终止点资源/authority 记录分别保留。reduced report 排除随机 attempt/run identity，
字节一致只证明 semantic projection；不使四格共享 execution authority。

另有两类明确不同的 witness：

1. 每个非空 request 的 modeled COMPLETED terminal 使用空 records，现有 admission 返回零 Facts；移除 CLASS records
   也仍被接纳。它只证明 current predicate 不要求完整 candidate universe，不声称真实固定 worker 产生该输出。
2. 对 retained rich request 作只读 admission replay：具有真实 FunctionDef node/anchor 的 FUNCTION candidate 被拒绝；
   将 MODULE null 属性改为本 world 的 Policy 映射属性也被拒绝。两项都来自 current closed candidate comparison，
   不是 foreign product。result SHA-256 为
   `d4ab21e96ca9264a404a0fee3865511af669af15b097faba75a06054b124a4f0`。

第二类说明：后继不仅缺 completeness proof，还需要完整 Fact 投影可进入的受审 admission 语义。不能把新类型塞进
当前 `r1-parse-product-fact-consumer/0.1`，再声称继承了原冻结资格。具体 successor/version 范围仍是后继合同问题。

## 5. 六个问题的裁决

| 问题 | 当前可成立事实 | 尚未取得的资格 |
| --- | --- | --- |
| Profile kinds / responsibility | 五种 Fact 的结构规则已有冻结文本；当前闭合 worker 只有 MODULE/CLASS | 五种完整投影的 executable universe / fulfillment admission |
| Parse product 足够吗 | 九个 world 的 canonical AST 保留声明、direct-body 关系、alias、relative level、位置；无需宿主 reparse 即可检查 | 有限 witness 不证明通用枚举本身 complete；完整属性还需要 Policy mapping 与 exact anchor history |
| denominator owner | Human Seal/Policy/Profile 拥有语义；Parse product 提供已资格化结构；application 执行已冻结机械规则 | 当前没有 admitted 全集构造结果/规则执行证明；Provider 和实际输出不得反向定义全集 |
| multi-Provider 责任 | 每个 applicable child 收完整 accepted set；独立 claim/run/lifecycle；封闭三 Provider 的 semantic output 重复 | CUMULATIVE 只证明 applicability/lifecycle，不决定逐 kind/node 的重复、分区或异构履责；重复输出不是独立 Parse witness |
| negative / zero output | empty source 仍有 MODULE；空 terminal 可合法 admission；rich child 可正常完成而不报告函数/import | current carrier 不能认证“该种类确实不存在”与“未履行相应责任”的区别；absence 需从独立枚举规则得到 |
| all-rejected / zero accepted | 两种 world 的 upstream identity 不同，consumer 都显式阻断且无 FactSet/normal Fact continuation | 未决定 zero-member Fact-stage closure，更不推出 empty FactSet、Fact fulfillment 或 Coverage CLOSED_EMPTY |

Policy variant 在相同 AST 结构下改变 module mapping，但当前 worker 两次都报告 module_key_parts=null，request 只携带
policy digest，未交付 mapping payload。doc245 没承诺完整 MODULE 属性派生，因此这不是当前 runtime defect；它证明
不能把“Profile + products”写成完整 Fact semantic input，也不能把 candidate provenance admission 写成一般 Fact 正确性。

## 6. 收窄后的后继问题

Fact seam 已经具备 qualified 上游，不再缺 AST carrier。最小候选应先明确：

```text
admitted Parse products + relevant sealed Policy/Profile + exact identity/anchor history
    -> versioned, mechanically checkable complete projection universe
    -> explicit per-Provider responsibility and applicable membership
    -> per-obligation fulfillment / justified absence
    -> same-world reconciliation and original-attempt continuation
```

这里每个箭头仍待合同审查。不能先命名通用 ObservationReceipt/Ledger，不能从 reported Facts 倒构造全集；不能只加
count 并把 conformance MODULE/CLASS admission 解释成五种完整投影。MODULE mapping、函数/方法分界、import alias
ordinal、重复责任与 zero-member disposition 都必须能被反例攻击。

既有 Parse/consumer freeze 不重开；如果完整投影需要改变 frozen function/projection/admission，必须显式划出最小
successor 或 reopen/version 边界再资格化。当前不决定类名、字段、状态枚举或 persistence。

## 7. 剩余 R1 的条件化依赖计划

长期目标是让源码语义到有限 public closure 可核验；阶段顺序由新证据修正，不由文档编号调度。

| 候选阶段 | 进入前必须重新确认 | 最多形成的新事实 | 当前 authority |
| --- | --- | --- | --- |
| Fact projection / fulfillment | 本审计取得自己的资格；完整输入、全集构造与 consumer admission 断口仍是最小问题 | 先最小合同，再独立可行性/施工资格；最后才有实现与冻结 | 仅本轮 current-state audit |
| Fact → Coverage history handoff | authoritative Fact universe / fulfillment 已成为 qualified upstream，且确有消费缺口 | 同 attempt 的 history/denominator 交接合同与 qualification | 未授权；可能与前阶段共享边界，但不能预定 |
| ReviewSliceSet / seven-stage Coverage | 各阶段 denominator、履责、unknown/negative world 与 same-world binding 均可核账 | composition-level qualification、有限 closure 与跨 stage reconciliation | 未授权；不能把 seven sets 方程当真实性 |
| finite public projection / Bundle | private qualified history 足够，public consumer 的自包含/重取输入责任已经明确 | 有限 public claim、serialization/publisher/readback 的独立闭环 | 未授权；不自动进入 R2–R6 |
| persistence 分支 | 现实 consumer 必须离线/历史重算，且 live recomputation 或合法 reacquisition 不足 | 最小 persistence authority；其余保持 OPEN | OPEN；不先选 Route A/B，也不保证永远可延期 |

上述是 dependency candidates，不是一次性实现授权。每段仍须回到 CONTROL LOOP，遇到反例先归层，必要时退回被击穿
的最小 seam。`CLAIM_FIDELITY`、AI proposal、human disposition、Core handoff、release/tag 不借本计划获得资格。

## 8. 本层资格门与停止线

本层 patch 限于本文、README、AGENTS 与 milestones；doc195、doc245、doc247、doc249、doc250、全部 runtime/tests/
Schema/fixtures/identity vectors 与架构资产保持原字节。现有 Parse/product-consumer/source-operation/multi-Provider
窄测试四格各报告 128 项 OK：3.10.6 两格各实际通过 127、跳过 1（ambient host 就是 reference runtime），3.13.13
两格各实际通过 128、无跳过；不把跳过写成实际执行 PASS。最终字节通过本层 docs/Schema regressions、four-file scope、links、
UTF-8 without BOM、LF/final-LF、fences/headings、敏感路径、target marker、字节连续性、diff check 与只读 hygiene。

```text
current-state audit / final-byte local gates
    -> original PR required gates
    -> protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc251 / milestones observations
    -> independent Core and source-byte reconciliation
    -> qualified current-state audit history
```

闭合前只有 candidate；闭合后也不是 Fact contract frozen 或 implementation allowed。readback 的 non-success 完整枚举，
数量从 history 导出；诊断不替代正式产品路径；后来的 PASS 不覆盖旧身份。记录额外 housekeeping 不追加为生效门。

本轮 setup 中 optional psutil probe 不可用，只改用仓库外 OS 内存测量，无安装、产品观察或预算变更。所有正式
audit world 的首个 attempt 都通过；旧 timing failure、Windows UNKNOWN、doc248 六个 ERROR、doc250 README 首败
与其他历史身份保持原样。本地 readback 原始 Artifact 不进入 Git，本文摘要也不冒充外部独立复算。

最后门成立后重新绑定 current main，检查是否出现更早的输入/authority seam。若上述断口仍成立，下一候选才是
**docs-only Fact projection universe / fulfillment 最小合同审查**。不得先修改 worker/admission、Fact consumer、公共
Schema/carrier、persistence、Evidence/Bundle、Coverage、CLI、Workbench 或 Core。
