# R1 Parse → Fact Consumer 私有实现候选

> 状态：`PRIVATE_IMPLEMENTATION_CANDIDATE`。本文不声明 merged、exact-main verified 或 frozen。
>
> 施工基线：`main@935adbfd55b974d7fa50535da2ea0c95a90b4f99`。
>
> 上游 authority：[冻结合同](245-r1-parse-to-fact-consumer-correction-contract.md)、
> [A–J feasibility](247-r1-parse-to-fact-consumer-private-implementation-feasibility-audit.md)、
> [独立授权发布](248-r1-parse-to-fact-consumer-private-implementation-authorization-publication.md)。

## 1. 输入边界

历史 Fact wire `/0.2` 消费 source bodies；本候选在独立私有入口消费已完成 reconciliation 的 Parse products。
旧 source-operation projection `/0.1`、旧 wire `/0.2` 及其历史 controller 保持原义。

```text
OwnedParseFulfillmentClosure
    -> one-shot Parse continuation
    -> exact input / classification / product history revalidation
    -> existing application-owned Provider applicability
    -> complete ACCEPTED membership for each Provider
    -> provider-bound one-shot child request
    -> fixed product-only worker
    -> assigned-product candidate admission
    -> complete requiredness / lifecycle reconciliation
    -> same original attempt continuation
```

请求只有 canonical AST product、subject/product identity、Git path identity、source size 和 application-owned
node byte anchors。它没有 raw bytes、source text、repository path、loader 或重新 parse 的入口。
application 只为定位换算使用已有 exact blobs，不把这些 blobs 交给 worker。

## 2. A–J 对应

| Stage | 私有实现 |
| --- | --- |
| A | 领取原 Parse continuation；重验 exact inputs、Language Support classification、完整 ELIGIBLE denominator 和 product coordinates |
| B | `r1-parse-product-fact-consumer/0.1`；新 projection/wire identity，完整 ordered ACCEPTED membership |
| C | 每个 Provider 独立 one-shot claim；绑定原 BudgetContext/parent eligibility，不创建或续发 budget |
| D | copy-owned canonical request；strict keys；固定 worker，不提供 raw-source alternative authority |
| E | application 从 AST UTF-8 byte columns 映射 exact raw offsets，处理 BOM、CRLF/CR 和 multibyte boundaries |
| F | 每个 candidate 绑定 assigned subject/product、node path、child run、exact anchor 和 product-derived attributes；一个非法 row 拒绝整个 child |
| G | 复用 frozen Provider applicability、requiredness、Fact canonicalization 和 multi-Provider join；child lifecycle 各自独立 |
| H | zero denominator 与 all-rejected 保持不同 upstream identity，均阻断 child/terminal/FactSet/continuation |
| I | 只在完整合格 reconciliation 后领取 continuation；再次检查 original live authority 和 child eligibility |
| J | 直接 PFC-I-001..018 及继承 PFC/PFCB/PFC-C 反例；mutation、late revocation、budget stop、真实 Windows cell witness |

完整失败 child history 保留 exact request、原 terminal frame 和摘要；不会把非法 candidate 过滤以后保留其他 Facts。
缺失、重复、foreign attempt 的 observations 使 reconciliation fail closed，并消费这一次 join。

## 3. Product-use proof 的范围

proof 由 application 交付的 exact product view、固定受控 worker 的 product-only 执行、Windows cell lifecycle 和
逐 candidate 的 product/node admission 共同成立。terminal 的 `COMPLETED` 或 digest echo 单独不成立。

首版只为既有 closed Provider bindings 物化 MODULE/CLASS_DECLARATION conformance projection。它不是任意第三方
Provider 的沙箱证明，不证明任意 Python 代码无法访问宿主文件系统，也不声明通用 Fact projection 已实现。
worker 不读取 Git path metadata 所指对象，也不调用 parser；改变该受控边界需要重新审查。

合同允许合法 product-bound child 报告零个 Fact：这不缩小请求 membership，也不证明 Fact fulfillment。
这种 normal nonempty-input world 与 zero-accepted 阻断不同，不能相互替代。

## 4. 测试与保留失败

新增测试在 `test_parse_product_fact_consumer.py`，不依赖其他 test class 的初始化顺序。
每个 attempt 独立建立 BudgetContext、Parse reconciliation、consumer claims 和 child history。

首个 CPython 3.10.6 normal targeted attempt：27 项中 26 通过、1 失败。
失败的 PFC-I-017 断言读了历史 `/0.1` application，却要求其中存在 `/0.2` 标记；实际 `/0.2` owner 是
`_source_operation_fact_application.py`。该失败归为 `TEST_ASSERTION_TARGET_SETUP_ERROR`，不是产品协议改义。
只修正测试定位，原日志与当时源码摘要保留在仓库外 qualification artifacts。后续 PASS 不覆盖该身份。

最终资格面：

```text
CPython 3.10.6 normal / -O
CPython 3.13.13 normal / -O

new consumer targeted suite
full Review Attention regression suite
real explicit CPython 3.10.6 Parse -> two product-only Windows workers
four golden semantic worlds: mixed / two accepted / all rejected / zero denominator
historical byte continuity / private boundary / links / encoding / hygiene
```

golden 比较只比较 semantic product/projection/Fact 值；不会把包含独立 attempt/run provenance 的完整 closure
字节要求为相同。最终运行数量、skips、日志与 byte hashes 由本候选 PR 的 validation 记录，不从中间字节继承。

## 5. 停止线

本候选不修改 Fact obligation universe/fulfillment、Coverage、persistence、public Schema/carrier、Evidence/Bundle、
publisher、CLI、Workbench 或 Core。它不把既有 public/historical Fact controller 自动接到此私有入口。

若后继必须重新交付 raw source、允许 Provider 自证 product use、改变历史协议、增加 public persistence 或先定义
Fact universe，必须停止并回到 [CONTROL LOOP](working-method.md)，只重开被击穿的最小边界。

PR 门只资格化 implementation candidate。合入、new exact-main gates、后继独立状态发布及其声明的读回门仍须各自
取得证据；本文件不据此授予冻结状态或下一 seam 的施工权。
