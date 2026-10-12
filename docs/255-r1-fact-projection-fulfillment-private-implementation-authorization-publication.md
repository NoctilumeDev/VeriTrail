# R1 Fact projection / fulfillment 私有实现授权发布

日期：2026-10-12

> 发布基线：`main@c9de08409ac0fda9bb1da9638d54077a4914cad0`，tree
> `97ed9b306166f54f88e9f5b3f6096cfad1909a02`。
> 影响：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`；docs-only。
> `PRIVATE_IMPLEMENTATION_ALLOWED` 仅为条件目标，本文最后门全部闭合以前不生效；完整 successor 实现仍未开始。
> persistence OPEN，Coverage NOT_STARTED；doc252/doc254 的已资格化历史字节保持不变。

## 1. CONTROL LOOP 与本轮 authority

[doc252](252-r1-fact-projection-universe-and-fulfillment-contract.md) 已由
[doc253](253-r1-fact-projection-fulfillment-contract-freeze-publication.md) 的独立资格链冻结。
[doc254](254-r1-fact-projection-fulfillment-private-implementation-feasibility-audit.md) 的可行性审计随后取得自己的
qualification；它没有自动授权 successor runtime。

本轮重新核对远端 main、主仓、并行 PR、current runtime 与保留 artifacts。远端与主仓均为本基线；三个 open PR
为 unrelated Dependabot 变更，未参与本候选。主仓用户 untracked 文件保留，单用途分支从本 exact main 创建。
current consumer/protocol `/0.1` 仍只构造 MODULE/CLASS，没有完整五类 U/E successor；这不是旧 runtime 违约。

没有发现击穿 doc252/doc254 前提的新证据。当前最小候选仍是 doc254 §8 的有限 private implementation authority。
人工本次仅批准 docs-only 授权发布候选；精确 head 合并须在最终字节和原始 PR 门闭合后另行确认。
本文不再做一轮 feasibility，不创建 runtime 分支，也不提前授予本发布尚未取得的资格。

## 2. 已闭合的 feasibility 资格身份

[PR #292](https://github.com/NoctilumeDev/VeriTrail/pull/292) 的坐标为：

```text
base  = c65a9f7d915ea96b22c3ca4d641c12a09664b7ac
head  = 816eda40ccef21db510b535d4a2a277addc46271
merge = c9de08409ac0fda9bb1da9638d54077a4914cad0
tree  = 97ed9b306166f54f88e9f5b3f6096cfad1909a02
```

一个 commit、四文件、`+293/-3`；受审 head tree 与 merge tree 相同。原始 PR Public CI `38200446340`、
exact-main Public CI `38201901095` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38201901082` attempt 1 /
1/1 SUCCESS。Review Attention 四格各 `473 reported / 471 passed / 2 skipped`，skip 不算实际执行通过。

三个独立 anonymous installed-product observations 均绑定该 exact main，P1/P2 COMPLETE、Core PASS：

| Target | Plan identity |
| --- | --- |
| README | `r1-fact-feasibility-formal-readme-1-c9de084` |
| doc254 | `r1-fact-feasibility-formal-doc254-1-c9de084` |
| milestones | `r1-fact-feasibility-formal-milestones-1-c9de084` |

independent reconciliation SHA-256 为
`d8ae2060f3a44c9f775a482a8bdca152423b47bf83163faee2961533fd516b5c`；audit closeout 为
`b6653116656bb0f8e1c2fcce6084ec4f3a13fcc59de318dd92974b028d600ea3`，封存 125 份 terminal artifacts。
本轮重核其 seals，以及 candidate local qualification 的 386 份 terminal witnesses。该 world 的 formal history
为 3 PASS / 0 non-success，6 个 render diagnostics 与 3 个 setup entries 均保持非资格化。

因此 `FEASIBILITY_AUDITED` 已是 qualified history。doc254 的 candidate header 仍保留原字节；状态生效依据其
声明的资格链与 retained evidence，不靠倒改历史 header。主仓对齐与 read-only hygiene 是收尾 housekeeping。

## 3. 审计 witness 不预先证明实现

doc254 的 identifier corpus、九个 product worlds 和 23-case synthetic reconciliation 支持有限可行路线，不能
变成 successor fulfillment。最终四格共 44 个实际 reference Parse children、0 个实际 Fact children；synthetic
核账没有实际 Provider histories。真正的 claim、bounded child、terminal、release 与 live continuation 必须由实现
重新建立并直接受审，不能复用模型 PASS 或旧 `/0.1` qualification。

首个 `INVALID_AUDIT_FIXTURE_SETUP` 的 11 个 Parse children 与 52 份 artifacts 保留；v1 model 的
`AUDIT_RECONCILIATION_MODEL_INSUFFICIENCY`、21-case 原 corpus PASS 与独立 v2 23-case 结果各保留原身份。
上游 formal ERROR、CANCELLED、hard-exit UNKNOWN 和网络/setup diagnostics 继续由各自记录拥有，不因本授权改写。

fixed audited closed worker 仍是普通 Python process。本轮不把 product-only input discipline 宣称为任意第三方
Provider filesystem sandbox，也不把码点 corpus 宣称为所有字符串或未来宿主的通用 conformance。

## 4. 条件化的最小施工面

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多落实以下私有边界。
各项继承 doc252 的语义与 doc254 §8 的候选面，不新增语义合同或决定 public carrier。

| 面 | 允许落实的责任 |
| --- | --- |
| A | exact Snapshot/Policy/Profile、完整 Parse partition/product/history、owned anchor inputs 与原 live authority 的重新验证 |
| B | application-owned 完整 U/E、Python 3.10 module/identifier conformance、nullable/collision history 与明确 projection blockers |
| C | 独立 `/0.2` descriptor/allow-list、consumer/protocol validators 与明确 operands；旧 `/0.1` 不变 |
| D | product-only、immutable/copy-owned closed worker input；expected projection 留在 application 核账侧 |
| E | 每个 applicable closed Provider 的完整 U/E 责任、独立 provider-bound one-shot claim 与真实 bounded child lifecycle |
| F | 完整 Fact 内容及 assigned product/node/alias admission；真实 run/fact provenance 双向核账 |
| G | required/optional responsibility 与串行 join；ordinary optional gap、unsafe release、shared stop 分开 |
| H | zero denominator、all rejected、incomplete/unknown 与不可表示 world 的显式阻断和历史保留 |
| I | 完整 qualified reconciliation 后的 same-attempt FactSet 与 one-shot private continuation |
| J | FPFCT-001–024 直接实现 falsifiers、independent gold/mutation 与 verifier 反查 |

实现必须守住这些硬边界：

1. 全部对象、worker、validator、projection 与 controller 留在 `veritrail_review` private；不新增 public export/SPI。
2. U 来自完整 admitted products 与冻结规则；E 不依赖 actual Provider outputs。所有 applicable fields/LIST、声明和
   import alias 完整访问，METHOD 仅按 direct ClassDef.body edge；subject、Fact identity 和属性规则不变。
3. U 已知但 E 不可表示时保留完整可构造的 U 与 exact blocker history；不能把可表示前缀 admission、改名、漏项或
   改归 Parse REJECTED。input/anchor integrity 失效不能形成较小 KNOWN U。
4. module mapping、raw ASCII init 判断、nullable/collision 和 raw-byte anchors 按合同复算；不借宿主 import resolver、
   newer identifier 规则或 mutable path 获取语义。未知宿主或 conformance 无法证明时停止。
5. worker 不得收到 raw source/body、lazy loader、repository handle 或 expected answers；受审 application 只使用
   copy-owned verified bytes 完成原 integrity/anchor 责任，不能新增 raw-source reparse。
6. 每个 required/optional Provider 都承担完整 U/E，独立领取 claim；两个 partial reports 的 union 不能修复各自履责。
   不补造 candidates/ProviderRun，不删错项后 admission。identical semantic duplicate 与 duplicate terminal 分别处理。
7. 原 BudgetContext 对象、deadline、stop latch、eligibility、Parse continuation 与完整 authority history 连续；相同
   limits 的 fresh context、foreign history 或 semantic equality 不继承本次资格，失败后不能刷新预算恢复 continuation。
8. 真实 child start、唯一 terminal、完整 release 与 source provenance 必须直接成立；unsafe release/shared stop
   阻断正常 FactSet/continuation，不能藏进 optional ordinary gap。纯函数核账不拥有 execution authority。
9. zero accepted 不启动 normal Fact child、empty-product request 或 Fact terminal，不形成 empty FactSet/normal
   continuation。known-empty accepted-derived U 不等于 Fact-stage closure；两种 complete negative worlds 不折叠。
10. qualified closure 的 private retention 必须足以重核 inputs/U/E、product-slot 关联、责任、terminal/frame 原字节、
    对账、FactSet/provenance 与 negative/optional history。本文不选类名、字段、receipt 或 persistence 形状。

该 authority 允许施工，不预先证明实现正确、完成、merged、exact-main verified 或 FROZEN。

## 5. 未授予的后继能力

本轮不修改 runtime/tests/workflows/Schema/fixtures/Profile/Policy、doc252/doc254 或其他 frozen 文件。
后继有限实现也不授权 persistence Route A/B、zero-member Fact-stage closure、Fact→Coverage handoff API、
Relation/Slice/public assembler、ReviewSliceSet/Coverage、public Schema/carrier/corpus、Evidence/Manifest/publisher/
Bundle、CLI/Workbench/Core、其他顶层轨、CLAIM_FIDELITY、tag 或 Release。

若实际反例迫使改变 frozen kinds/identities、Provider 自定义 denominator、raw reparse、expected-answer 注入、
放宽预算、共享 attempt authority、改旧版本或扩 public surface，先保现场并归层；只显式 reopen/version 被击穿的
最小边界。授权不能成为扩大实现范围的理由。

## 6. 本 publication 的资格门

本 publication 只改 README、AGENTS、milestones 并新增本文。全部其他 tracked bytes/modes 保持基线，包括
doc252 SHA-256 `074852c5579443fe14af3497cc19ea1c649097cf211258ab3ee0104ecb011d81` 与 doc254 SHA-256
`17042716d144dc24083091066d4fb335c186c16d1b856b2da25582644932e0fe`。

final-byte local gates：重核本轮人工 scope、上游 terminal seals/首败身份；unchanged Parse/product-consumer/
source-operation/multi-Provider 六个窄模块与三个 R1 Schema modules 的 CPython 3.10.6/3.13.13 normal/`-O` 四格；
UTF-8 without BOM、LF/final LF、links/fences/headings、条件 marker、敏感字面量、exact scope/其他字节连续、
diff check 与 read-only hygiene。实际 counts/skips、resource samples 和 outcomes 另存 qualification Artifact；
本节是预先声明的门，不冒充已执行 PASS。harness containment 不修改产品预算。

```text
final docs-only bytes / declared local gates
    -> original PR qualification
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc254 / this publication / milestones readback
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP on current exact main
```

四个目标各选一份 qualifying PASS，Plan/session/handoff 独立，全部绑定本 publication 的同一个 merge SHA。
diagnostic 不替代正式观察；全部 retained formal non-success 与 diagnostics 从历史机械枚举，N 不写死。
前一轮 PASS 不替代本轮 fresh readback，后来的 PASS 不覆盖 ERROR/FAIL/CANCELLED/UNKNOWN。

## 7. 生效前后与实现自己的门

条件化 target markers：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本文第 6 节最后门闭合以前，实际 implementation authority 仍 `NOT_AUTHORIZED`；不能从已提交 target marker、
PR CI 或可行性审计借权开 runtime。最后门闭合以后也只是 `ALLOWED / NOT_STARTED`；从 current exact main 复核
仍为最小合法 seam，才可创建实现分支，不能按本文编号自动开始。

实现最终字节仍须独立取得本层声明的完整 local/original PR/protected merge/new exact-main/fresh product observation/
independent reconciliation 与 implementation fact publication。本文不固定后继文件布局、test count 或发布形状，
也不替后继 qualification、冻结或 Coverage 预先授权。
