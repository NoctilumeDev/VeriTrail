# R1 Parse product → Fact consumer correction 最小合同 0.1

日期：2026-10-10

> 状态目标：`R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_CANDIDATE`
>
> 上游冻结事实：[Parse fulfillment 最小合同](217-r1-parse-fulfillment-contract.md)、
> [Parse private implementation 最终冻结发布](244-r1-parse-private-implementation-freeze-publication.md)
>
> 前置问题历史：[consumer projection 前置资格审计](215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)、
> [product / consumer binding 前合同审计](216-r1-parse-product-fact-consumer-binding-precontract-audit.md)
>
> 候选基线：`main@b166dee05fe995b17b2f3bb557d75c2feb4f5493`
>
> 影响等级：`L1_DOCUMENTATION / CONTRACT_CANDIDATE_ONLY`

本文冻结候选只定义 admitted Parse product 成为 private Fact consumer input 时的最小 authority、membership、
product-use、multi-Provider、zero-accepted 与 output/continuation binding 语义。本文不修改 runtime、tests、Schema、
Profile、Policy、Fact semantics、Fact obligation universe、Fact fulfillment、Coverage、persistence、public Artifact、
Evidence、Manifest、publisher、Bundle、CLI、Workbench 或 Core。

本文不是实现授权。本文自己的 original PR、受保护主线合入、new exact-main gates、fresh installed-product
readback、independent reconciliation 与后继独立 freeze publication 全部闭合以前，candidate marker 只表示发布目标。

## 1. 目的与停止线

Parse private implementation 已经形成：

```text
complete exact Parse denominator reconciliation
    -> application-owned admitted Parse product set
    -> same-attempt one-shot Parse continuation
```

current Fact runtime 仍然形成：

```text
Language Support ELIGIBLE upper bound
    -> private-source-operation-projection/0.1
    -> source body request / derivation-cell/0.2
    -> Fact Provider reads raw source
```

因此当前缺口不是 Parse 结果是否存在，而是：

> 哪个 application-owned、attempt-bound consumer boundary 有资格把同一 admitted Parse product 交给每个 Fact
> Provider，并机械证明 rejected / missing / non-success source 没有通过 raw-body side channel 重新进入 derivation。

本文只冻结这一接缝。本文不回答：

```text
一个 Parse product 应派生哪些 Fact
Fact candidate universe 是否完整
Provider 是否履行全部 Fact obligation
empty FactSet 怎样形成
Fact Coverage 或 seven-stage Coverage 怎样 closure
Parse product / classification 是否持久化
```

## 2. authority topology

首版 authority topology 冻结为：

| 对象 / 决定 | authority owner | 明确没有 authority 的主体 |
| --- | --- | --- |
| exact source / Policy / Profile world | frozen DerivationInputSet | caller subset、Fact Provider |
| Language Support eligible denominator | frozen classifier / application | parser、Fact output |
| Parse denominator、semantic result、product / product set | frozen Parse contract + application reconciliation | Fact Provider、consumer terminal |
| live Parse continuation | original Parse attempt | equal product bytes、fresh BudgetContext |
| applicable Fact Provider bindings | existing frozen applicability / application | arbitrary caller、Provider self-registration |
| per-Provider consumer membership | 本合同的 application function | Provider output、reported Fact paths |
| product-use authority | provider-bound one-shot consumer claim | raw source、path、digest echo |
| zero-accepted scheduling | 本合同的 explicit blocking rule | current empty-body runtime history |
| Fact candidate production | claimed Fact Provider using admitted products | Parse terminal、consumer projection |
| Fact obligation / fulfillment / Coverage | future contract | 本合同、Fact Provider self-report |

核心分离为：

```text
Parse product-set semantics
    != Fact consumer membership authority
    != per-Provider child claim
    != proof that a product was used
    != Fact fulfillment
```

## 3. semantic function 与 exact input identity

首版 consumer qualification function identity 冻结为：

```text
r1-parse-product-fact-consumer/0.1
```

它的 semantic input 必须共同绑定：

```text
exact DerivationInputSet identity
exact LanguageSupportClassificationSet identity
exact Parse denominator and complete reconciliation identity
exact admitted Parse product-set semantic identity
exact Parse parent attempt and claimed continuation
exact applicable Fact Provider descriptor / binding
consumer function identity
```

path、accepted subject ID 列表、product-set digest、Provider descriptor 或 parent attempt 中任一单项都不是完整 input
identity。相同-looking inputs、相同 accepted membership 或逐字节相同 product-set semantics 不继承另一 attempt 的
consumer claim。

semantic consumer projection 可以是 attempt-neutral derived value；claim 与 continuation 必须是 attempt-bound、
one-shot authority。具体 private class、field、digest domain、protocol number 与 carrier 是实现 non-decision，但历史
`private-source-operation-projection/0.1` 和 `veritrail-review-derivation-cell/0.2` 不得被增加字段后静默改义。

## 4. consumer membership

### 4.1 唯一 membership source

normal consumer membership 只能由 application 从**完成对账的 admitted Parse product set**机械导出：

```text
consumer members
    = exact ordered ACCEPTED products in the reconciled Parse product set
```

顺序继承 frozen Parse product set 的 exact subject order。caller 不得传入 accepted subset；Provider output、Fact path、
terminal success 或 current source-operation projection 都不得反向定义 membership。

### 4.2 四类 world

| Parse world | normal candidate membership | consumer qualification |
| --- | --- | --- |
| full accepted | 全部 admitted products | 可继续进入 per-Provider claim |
| partial accepted | 仅 admitted ACCEPTED products | 可继续；rejected raw body 不可见 |
| zero denominator / all rejected complete | exact known-empty product set | 按 section 9 显式阻断 normal Fact launch |
| missing / duplicate / dangling / foreign / lifecycle non-success | 不存在合格 normal product set | fail closed，不得伪装 known-empty |

zero denominator 与 all rejected 可以都得到空 membership，但其 denominator、partition、product-set identity 与历史不得
折叠。missing 或 non-success 也不得仅凭 empty accepted list 混入这两个 world。

### 4.3 Provider-specific projection

每个由 existing applicability rules admitted 的 Fact Provider 都从同一个 application-owned product set 导出自己的
consumer projection。首版不授权 Provider-specific source/product subset：每个 applicable Provider 的 candidate
membership 都是 section 4.1 的完整 ordered admitted product set。

Provider 可以在合法执行后报告零个 Fact；这不允许它在执行前缩小 input denominator，也不证明 Fact obligation 已履行。

## 5. product-use boundary

### 5.1 admitted product 是唯一 derivation-capable input

首版选择 **product-only derivation authority**：Fact Provider 能用于产生 Fact 的 source semantics 只能来自本次
provider-bound claim 交付的 immutable / copy-owned admitted Parse product。

normal consumer request、worker document、shared map、lookup handle、lazy loader 或环境路径不得向 Provider 暴露：

```text
rejected subject raw body
missing / lifecycle non-success subject raw body
accepted subject raw body as an alternative derivation authority
mutable repository path or filesystem reread capability
```

subject/path/blob identity 可以作为 provenance metadata 存在，但不得解析为 source content。若未来 Fact 算法确实需要
accepted raw text 作为独立 operand，必须显式 reopen/version 本合同并冻结其最小 authority；不得先把 raw body 留在
request 中，再用 product digest echo 声称 product 被消费。

### 5.2 禁止 reparse 与 echo proof

Provider 不得：

- 根据 raw bytes、path 或 repository 重新运行 parser；
- 自己创建、替换或修改 Parse product；
- 只回显 product / product-set digest 后声称已使用 product；
- 用同语义 tree、同 Fact 或同 terminal 继承另一 attempt 的 Parse authority。

application 必须能机械验证：child claim 交付的 product view 与 upstream admitted product 是同一 owned semantic value，
且 Provider 的 candidate output 只引用自己被分配的 product subjects。

## 6. per-Provider one-shot claim

每个 applicable Fact Provider 必须拥有独立的 one-shot consumer claim。claim 至少绑定：

```text
original live BudgetContext / parent eligibility
claimed Parse continuation
exact reconciled product-set identity
Provider descriptor / binding
Provider-specific complete consumer projection
consumer function identity
child attempt / request identity
```

claim 在成功领取、validation failure 或竞争失败后的状态转换必须 fail closed；具体 enum 与 exception 是实现
non-decision。同一 Provider 不能重复领取；不同 Providers 不能共享 child claim；一个 Provider 的 terminal 不能替另一个
Provider 完成领取或 execution。

## 7. multi-Provider sharing

多个合法 Fact Providers 共享**一份** upstream Parse truth：

```text
one application-owned reconciled Parse product set
    -> Provider A projection + one-shot claim
    -> Provider B projection + one-shot claim
    -> optional Provider projection + one-shot claim
```

不得按 Provider 数量重新 parse、复制 admission history 或各自建立 product-set authority。每个 child claim 的 descriptor、
attempt、request、terminal 与 lifecycle 独立；所有 child projections 必须共同绑定同一个 upstream product-set semantic
identity 和同一个 parent Parse continuation history。

Provider A 的 completion、failure、timeout 或 output 不修改 upstream product set，也不使 Provider B 自动成功、失败或
取得 claim。

## 8. Fact output 与 continuation binding

每个 normal Fact child terminal 必须绑定：

```text
provider descriptor / child attempt identity
consumer function and projection identity
exact upstream product-set identity
exact assigned product subjects / products
Fact candidate output provenance
execution lifecycle
```

每个 reported Fact 的 source provenance 必须解析到该 Provider 被分配的 exact product subject。rejected、missing、
non-success 或 foreign product subject 的 Fact candidate 使 normal child invalid；application 不得丢弃非法 candidate 后把
其余部分当作合格 terminal。

本合同只要求 output history 证明“这些 candidate 来自本次 product-bound child”。它不规定每个 product 必须产生哪些
Fact，也不以 candidate 数量或 terminal completion 证明 Fact fulfillment。

只有所有 required consumer children 都按既有 Provider requiredness 与 lifecycle 规则形成合格 terminal，application 才能
把 normal continuation 绑定到同一 parent attempt 与同一 product set。具体 Fact composition/admission 继续使用其既有
合同；本合同不扩大其 public semantics，也不把 current historical identities 倒改为新协议。

## 9. zero-accepted scheduling 停止线

首版对 zero denominator 与 all-rejected complete 选择**显式阻断**，不启动 normal Fact consumer child，也不形成
empty-product Provider request：

```text
known-empty admitted Parse product set
    -> preserve exact zero-denominator or all-rejected identity
    -> no normal Fact child claim
    -> no Fact terminal / FactSet / normal Fact continuation
    -> return control to a future Fact zero-member contract
```

该阻断是一个 total consumer scheduling rule，不是 UNKNOWN，也不是 current empty-body history 的继承。它只说明本合同
0.1 不拥有 zero-member Fact closure authority。

因此本合同明确不推出：

```text
empty FactSet
required Provider fulfilled without execution
Fact obligation universe closed
Fact Coverage complete
ReviewSliceSet / seven-stage Coverage CLOSED_EMPTY
```

未来若要启动 exact empty-product child，必须通过 version bump 或独立后继合同说明 required-provider closure、terminal 与
FactSet authority；不得在实现阶段把阻断静默改成 empty success。

## 10. execution、failure 与 attempt authority

consumer execution 继续受 original parent attempt 的 live BudgetContext、deadline、memory/resource ownership、stop latch 与
eligibility 约束。实现不得创建相同 limits 的 fresh context、重置 deadline 或以 retry 生成第二个 normal claim。

以下 world 没有正常 Fact output / continuation 资格：

```text
Parse continuation already claimed or invalid
consumer projection / product-set binding drift
claim duplicate or foreign attempt
Provider launch unavailable
timeout / resource stop / interruption
worker or transport failure
terminal malformed or provenance mismatch
Fact references unassigned product subject
```

diagnostic retry 若未来存在，必须使用独立 identity，不能覆盖原 normal observation。execution completed 也不自动等于
Fact fulfillment。

## 11. persistence 与 public surface 是 non-decision

本合同只要求 same-attempt private product access 与 consumer proof。以下仍保持 OPEN / NOT AUTHORIZED：

```text
Parse product / Language Support classification persistence
offline product reacquisition
public product or consumer Schema
Evidence / Manifest / Bundle role
publisher / output root
historical Fact re-materialization
```

实现可以在 live attempt 内使用 immutable/copy-owned values；不能据此把 Route A 升格为永久 persistence 选择。若未来
offline consumer 无法从现有 authority 自包含验证，必须另开消费边界，而不是由本合同顺手增加 public carrier。

## 12. 资格否定矩阵

文档 215 的 `PFC-000..008`、文档 216 的 `PFCB-000..009` 与文档 217 的 `PFCT-011..016` 继续是本合同的
inherited falsifiers。至少必须机械拒绝：

| ID | world | 必须拒绝的结论 |
| --- | --- | --- |
| `PFC-C-000` | Language Support eligible upper bound 含 Parse-rejected source | upper bound 等于 post-Parse consumer membership |
| `PFC-C-001` | caller 传入 accepted subject subset | caller 拥有 membership authority |
| `PFC-C-002` | accepted IDs 相同、product semantics 不同 | consumer input 相同 |
| `PFC-C-003` | product digest 出现在 raw-source request / terminal | Provider 已消费 admitted product |
| `PFC-C-004` | rejected body 仍可从 side channel 读取 | accepted membership 字段已建立 least authority |
| `PFC-C-005` | Provider reparse 得到同 tree / Fact | 新 observation 继承 upstream Parse authority |
| `PFC-C-006` | 两个 attempts 的 product-set bytes 相同 | live consumer claim 可转移 |
| `PFC-C-007` | 多个 Providers 需要相同 products | 每个 Provider 可创建自己的 Parse truth 或共享 child claim |
| `PFC-C-008` | 一个 Provider completion | 其他 Provider child 已完成或 product set 可被修改 |
| `PFC-C-009` | all rejected complete | empty FactSet / Fact fulfillment / Coverage 已成立 |
| `PFC-C-010` | accepted list 为空但 reconciliation missing | 可以使用 zero-accepted blocking identity |
| `PFC-C-011` | current empty-body tests 全绿 | post-Parse zero-member scheduling 已冻结 |
| `PFC-C-012` | Fact terminal COMPLETED | product-use proof 或 Fact fulfillment 自动成立 |
| `PFC-C-013` | application 丢弃 foreign/rejected candidate 后保留其余输出 | normal child terminal 仍合格 |
| `PFC-C-014` | current projection `/0.1` / wire `/0.2` tests 全绿 | 历史 identity 可静默承载本合同 |

## 13. 后继 private implementation 最大边界

本候选冻结以前不授权代码。若独立 freeze publication 最终成立，后继仍须返回 CONTROL LOOP，并最多审计以下 private
implementation：

```text
exact upstream Parse product-set / continuation revalidation
versioned successor private consumer projection identity
per-Provider complete membership derivation
provider-bound one-shot claim
product-only immutable/copy-owned worker input
raw-source side-channel exclusion
Fact candidate provenance / product-set binding
same-attempt multi-Provider reconciliation and continuation
zero-accepted explicit blocking
PFC / PFCB / PFC-C falsifier hardening
```

该列表不是实现授权。尤其不得直接开始：

```text
Fact obligation-universe enumeration
Fact fulfillment / exact completeness proof
zero-member FactSet or Coverage closure
persistence Route selection
public Schema / carrier / Evidence / Manifest / publisher / Bundle
ReviewSliceSet / CoverageLedger
CLI / Workbench / Core / other top-level tracks
DECLARED_CLAIM_FIDELITY
```

若 private proof 必须暴露 raw source、依赖 public persistence、让 Provider 自证 product use，或先定义 Fact obligation
universe 才能成立，必须停止并重开被击穿的最小边界。

## 14. current-state re-audit evidence

CONTROL LOOP 从 exact `main@b166dee05fe995b17b2f3bb557d75c2feb4f5493` 重建状态。远端没有并行 human
semantic PR；三条 open Dependabot PR 不拥有本合同 authority。

仓库外 audit-only script 位于：

```text
<local-workspace>/tmp/parse-fact-consumer-current-state-audit-b166dee/current_state_audit.py
```

第一次 `py310-normal` audit attempt 使用 `def rejected(:`，而复用的 frozen helper 只把 `def bad(:` 构造成
REJECTED world。审计因此实际形成两个 ACCEPTED outcomes，并在自己的 accepted-count guard 停止。该身份保存为：

```text
INVALID_AUDIT_FIXTURE_SETUP
AUDIT_FIXTURE_DID_NOT_ESTABLISH_DECLARED_WORLD
product_observation = false
```

修正 fixture 后使用全新 attempt 2。CPython 3.10.6 / 3.13.13、normal / `-O` 四格均产生 2528-byte 相同 report：

```text
file SHA-256     = 33b403f1ad93695c9750328fe696d79a8316ae3abe67704ddb4f848a1420b510
semantic SHA-256 = 86b436119ee7159b414de19c1e1f0d6a0fa9e0acb64296c4962898b33ad7554e
```

report 机械确认：

```text
Parse denominator = 2
ACCEPTED = 1
REJECTED = 1
missing reconciliation rejected
zero denominator != all rejected
same-attempt product access exists

current Fact request paths = valid + Parse-rejected source
current Provider reports a Fact from rejected raw source
request / builder / multi-Provider state has no Parse product set or continuation
current projection domain = private-source-operation-projection/0.1
current wire protocol = derivation-cell/0.2
```

与 source claims 直接相关的五个 existing test modules 在同一四格各 86 项：

```text
CPython 3.10.6 normal  = OK, skipped=1
CPython 3.10.6 -O      = OK, skipped=1
CPython 3.13.13 normal = OK
CPython 3.13.13 -O     = OK
```

这些 tests 只证明 frozen Parse product authority 与 historical raw-source Fact chain 同时稳定存在；它们不把旧 Fact chain
解释成 post-Parse integration，也不拥有本合同 authority。canonical audit summary：

```text
<local-workspace>/tmp/parse-fact-consumer-current-state-audit-b166dee/audit-summary.json
SHA-256 = 9cdbec6bddd3dee187ade8e551ebc083a8d2d4568d55468f67dd19c9f5f366e4
```

## 15. 本地候选资格

本轮保留两项没有形成合同语义或产品 observation 的施工设施问题：

1. 第一次组合状态补丁使用的 AGENTS 尾段 anchor 与 exact bytes 不一致，`apply_patch` 在写入前整体拒绝；doc245
   已由此前独立补丁创建，其他四个状态文件没有形成部分修改。后继按 exact file tail 拆分补丁；
2. 第一次 docs/Schema 3.10 normal harness 没有把 exact checkout `src` 放入 `PYTHONPATH`，`test_markdown` 在 import
   阶段停止。该次保留为 `TEST_HARNESS_IMPORT_SETUP_ERROR / product_observation=false`；fresh attempt 2 显式绑定
   exact repository source。

最终四文件候选通过：

```text
changed scope 4/4                         PASS
relative Markdown links                  PASS
UTF-8 without BOM / LF / final LF        PASS
balanced fences                          PASS
candidate markers                        PASS
sensitive absolute paths                 0
git diff --check                         PASS
```

绑定 exact checkout source paths 后，docs/Schema suite 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格各
`40/40 PASS`：

```text
tests.test_markdown
tests.test_review_r1_admission_evidence_schema
tests.test_review_r1_derivation_evidence_schema_correction
tests.test_review_r1_schema_payload
```

与本文 source claims 直接相关的 Parse / source-operation / Fact wire / controller / multi-Provider suite 在最终候选
字节下为：

```text
CPython 3.10.6 normal  = 86 OK / skipped=1
CPython 3.10.6 -O      = 86 OK / skipped=1
CPython 3.13.13 normal = 86/86 PASS
CPython 3.13.13 -O     = 86/86 PASS
```

这些结果只使 docs-only contract candidate 具备提交资格，不替代 original PR、exact-main gates、installed-product
readback、independent reconciliation 或独立 freeze publication，也不授予 runtime authority。

## 16. candidate qualification gates

本候选只有在以下链条完整成立后，才可成为 qualified contract candidate：

1. 文档 215、216、217、244 的既有 claims 保持 qualified/frozen，且没有被扩大或倒改；
2. exact current source 继续证明 Parse product authority 已存在、Fact runtime 仍是 historical raw-source authority；
3. section 3–11 的 identity、membership、product-use、multi-Provider、zero-accepted 与 output binding 可以独立复核；
4. `PFC-*`、`PFCB-*`、`PFCT-011..016` 与 `PFC-C-000..014` 的拒绝边界保持成立；
5. diff 只包含本文与 README / AGENTS / milestones 条件状态同步；文档 216 的 qualified historical bytes
   保持不变，当前 CONTROL LOOP 重入事实由本文拥有；
6. Markdown links、UTF-8、LF/final-LF、fence/heading、敏感路径、marker 与 `git diff --check` 成立；
7. 与 source claims 直接相关的 Parse / source-operation / Fact wire / controller / multi-Provider tests 在本层声明的 Python
   normal / `-O` 矩阵中不被击穿；
8. candidate PR original required checks 全部成功并经受保护主线合入；
9. candidate exact main 的 Public CI 与 Browser Smoke 成立；
10. README、本文与 milestones 的 fresh anonymous installed-product public readback 与 independent reconciliation 成立；
11. 独立 docs-only freeze publication 自己的 original PR 门、受保护合入、new exact-main gates 与 fresh readback 再次成立。

第 11 项以前，本合同只能是 candidate，不能自称 frozen，也不能授权 runtime。任一新反例都可否决冻结或只重开被
击穿的最小条款。

当前原则候选冻结为：

> A Fact consumer may derive only from the exact admitted Parse products assigned by the application; equal semantics,
> echoed identities, or raw-source access never transfer product-use authority.

中文：**Fact consumer 只能从 application 分配的 exact admitted Parse products 派生；相同语义、identity 回显或 raw
source 访问都不能转移 product-use authority。**
