# R1 Post-Slice-Input Closure / Slice-Coverage Qualification 系统审计

> 状态（本文最后门全部成立后）：`R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_PRIVATE_IMPLEMENTATION_EXACT_MAIN_VERIFIED /
> R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_PRECONTRACT_AUDITED /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@1ca6a4740f13cbb9cb70eb0836dbbabf81c076d0`，Git tree
> `eb3ea2f62a00e4a0e93da5b0be94f6b75828823f`
>
> 上游冻结合同：[ReviewSlice Admitted-Graph Input / Anchor-Spec Obligation Closure 合同](189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md)
>
> 上游实现事实：文档 189 A–H private implementation 已 merged 并在 exact main 完成 Public CI 与
> Browser Smoke；A–H 没有独立 `FROZEN` claim
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不创建或修改 Schema、
> corpus、identity vector、runtime、测试、依赖、CI、Provider、parser、publisher、Manifest、公共
> ReviewSliceSet、CoverageLedger、Evidence、Bundle、Attention、CLI、Workbench、Core、P/Q/D/Cu/O/T、
> tag 或 Release

## 1. 审计问题与停止线

文档 189 A–H 已经能够在一个 exact admitted graph、同一 live attempt 与共享预算内形成：

```text
exact admitted graph input
    -> authoritative anchor/spec obligation domain
    -> attempt-bound traversal assignments
    -> deterministic BFS outcomes
    -> normal / empty / blocked reconciliation
    -> private obligation closure or typed negative receipt
```

这条链只证明 private obligation fulfillment。本文只问：

> private Slice obligations 已闭合以后，系统还缺哪一层资格，才允许把语义 Slice 投影成公共
> `ReviewSliceSet`，把七个 Coverage stages 组成一份权威 `CoverageLedger`，并让第三方确认这些公共
> bytes 来自这一次合法履责历史，而不是 caller 拼装、自洽缩分母或跨 attempt 移植？

本文不预选 Evidence 字段、独立 receipt、第九 Manifest role、Schema version、publisher 或 output root。
系统审计只识别下一条 blocking seam；后继合同必须从新的 exact main 独立起草。

## 2. 当前系统实际拥有的四层

### 2.1 private Slice obligation closure

`OwnedReviewSliceObligationClosure` copy-own exact assignments、outcomes、normal Slice candidates、phase commit
与 attempt-bound closure identity。其验证链还能向上追到 exact cross-validated Snapshot、Policy、Profile、
FactSet、RelationSet 与 relation admission witness。

它明确不拥有公共 SliceSet、Coverage 或 publication authority。继续成立：

```text
obligation domain defined       != obligations discharged
obligations discharged          != ReviewSliceSet admitted
ReviewSliceSet admitted         != seven-stage Coverage qualified
Coverage qualified              != bytes published
```

### 2.2 ReviewSliceSet 0.1 是语义内容

`ReviewSliceSet 0.1` 保存 exact semantic input digests、排序后的 `slices[]` 与 `slice_set_digest`。它不保存
`derivation_id`、relation admission witness、Slice obligation domain 或 closure receipt。

这一点本身不是 Schema 缺陷。两个独立合法 attempts 可以得到相同的 Slice 语义与相同
`slice_set_digest`。不能自动复用的是本次 attempt 的 admission、履责和 publication authority。

### 2.3 CoverageLedger 0.1 是七阶段语义账册

`CoverageLedger 0.1` 能表达七个 stage 的 denominator、partition、typed gaps、frontier 与保守状态汇合。
它的字段足以表达 normal complete、normal partial、known empty 与 upstream unknown。

但 Ledger 是责任履行账册，不是 denominator 的所有者。Schema 与单 stage 集合方程只能证明它在自己声明的
分母下自洽，不能证明：

```text
SNAPSHOT_INVENTORY denominator came from exact Snapshot
POLICY_SCOPE denominator came from exact Policy world
FACT / RELATION denominators came from authorized derivation history
SLICE_DERIVATION denominator came from the private obligation domain
all seven stages belong to one exact attempt history
```

### 2.4 当前公共 carrier 只到 Relation admission

`DerivationEvidence 0.2` 的 non-null `relation_admission` 能绑定 exact RelationSet admission history；它没有
Slice obligation closure 或 Slice/Coverage qualification binding。历史八文件 `valid-complete` corpus 仍使用
`DerivationEvidence 0.1`，这是受 byte guard 保护的历史样本，不能原位改写成 admission-capable Bundle。

`Manifest 0.1` 仍是八文件 exact-byte binder。它不能从文件 presence、SHA-256 或 semantic digest 推出
Slice/Coverage qualification，也不能被提升成 judge。

## 3. exact-main 本地最小反例

以下反例均在仓库外临时进程中只读复用 current test helper、Schema 与 fixture；没有修改源码、测试、
fixture 或 Artifact。Python 3.10.6 与 3.13.13 的 canonical reports 逐字节相同。

### 3.1 `SCQ-000`：相同 Slice semantics，不同履责历史

审计从同一 exact inputs 启动两个独立合法 attempts：

```text
H1 derivation_id = post-closure-audit-h1
H2 derivation_id = post-closure-audit-h2
```

两者都完成 relation admission、Slice obligation enumeration、deterministic traversal 与 normal closure。
结果为：

```text
same Slice candidates       = true
same slice_id               = 7723d6179b1fdc7c833e6a380665a95c7778230529e1e1a461c1ba4fd17656bf
same slice_set_digest       = 882e75aa343b30b3d8227fe32d5225b030a5544b81d619ce12f137c3320f936c

H1 admission witness       = bceaf3117b43041cef1d4b29a1255b7b57544deae8f7af78be510b3d9240eed2
H2 admission witness       = e755678ab123316375a18d3e435e7bb7a53507e05cfcdf59f603ce014d215886

H1 closure digest          = 7121d0969f69854e37863ec0a46940f7b8130d3f903eb22e1af925393ad8d024
H2 closure digest          = ef14c165d400ee83b75e6959e7a7921b28d800cf42c3b70bd4e81ce2a4846d23

H1 closure bytes SHA-256   = 046f5eda49a32907de5519e955c44c7d0d9b87ef7abd88d96e3f7f8a78f57750
H2 closure bytes SHA-256   = 9ddfd596b9948cd06c5b62b647cc51798658ced19f959d53e72a3708e8352c75
```

因此：

```text
same semantic SliceSet
    != same relation admission history
    != same Slice obligation fulfillment history
    != reusable publication authority
```

后继不能把 attempt receipt 加进 `slice_id` 或 `slice_set_digest`，否则会污染 content identity；也不能因为
公共 SliceSet bytes 相同就继承另一个 attempt 的 closure。

### 3.2 `SCQ-001`：Schema-valid 且 stage-self-consistent 的假 Coverage

审计从 frozen `valid-complete` Bundle 只修改 `SNAPSHOT_INVENTORY` stage：

1. exact SourceSnapshot 保持一个 tracked terminal entry；
2. 首阶段 denominator、eligible 与 completed 改成 KNOWN empty；
3. 按 frozen domain 重算 empty denominator digest；
4. 按 frozen projection 重算 `coverage_ledger_digest`；
5. 后续 `POLICY_SCOPE` stage 仍保留原来的一个 entry。

结果：

```text
Coverage Schema valid                    = true
stage partition equation conformant      = true
overall_coverage_status                  = COMPLETE
SourceSnapshot inventory count           = 1
SNAPSHOT_INVENTORY denominator count     = 0
POLICY_SCOPE denominator count           = 1
coverage_ledger_digest                   = 8dda8565035886d57f3765a564e44269d7d83bd13573bc3284433c28c138c721
```

这份 Ledger 同时声称“首阶段已知为空”和“下一阶段出现一项”，与 exact Snapshot 明显矛盾，却仍能通过
Schema、digest 和当前逐 stage partition predicate。它不是当前 runtime defect，因为公共 Coverage producer
尚未实现；它证明下一层不能只做：

```text
caller stages[]
    -> validate each stage
    -> hash
    -> CoverageLedger
```

必须由 application 从 exact owned history 重建每个 stage 的 authoritative denominator、terminal partition 与
跨 stage continuity，再决定完整 Ledger 是否 qualified。

### 3.3 `SCQ-002`：当前公共格式没有 Slice closure binding 通道

当前 positive `DerivationEvidence 0.2` 在没有任何 Slice closure binding 时合法；closed Schema 会拒绝直接追加
`slice_obligation_closure` 字段。`Manifest 0.1` 的八个 role 也会拒绝直接追加第九个
`SLICE_OBLIGATION_RECEIPT` role。

这不自动证明“必须新增 Evidence 0.3”，也不自动证明“必须新增第九个文件”。它只证明：

> 当前公共格式没有已经获得授权的 attempt-bound Slice fulfillment carrier；后继若需要公开这项 claim，必须
> 先定义 witness 的 owner、claim、identity 与 cross-object conformance，再选择版本化存放位置。

### 3.4 `SCQ-003`：相同空 Slice bytes 可以来自不同世界

下列世界都可以投影成 `slices=[]`：

```text
known zero-anchor domain, CLOSED_EMPTY
relation conflict, normal Slice input blocked
unknown upstream denominator
caller omitted every obligation
traversal never started
```

现有 `ReviewSliceSet 0.1` 与 `CoverageLedger 0.1` 足以分别表达 empty content 和 KNOWN/UNKNOWN Coverage；
但只有 private empty closure / blocked receipt 能证明是哪一个世界。后继必须保留：

```text
empty semantic content
    != closed-empty fulfillment
    != blocked / unknown
    != work never performed
```

## 4. 真正缺失的层

反例把下一条 blocking seam 压成三项连续资格，而不是一个“写 JSON 文件”的动作：

```text
private Slice obligation closure / negative receipt
    -> ReviewSliceSet semantic projection eligibility
    -> seven-stage Coverage composition qualification
    -> explicit public closure binding
```

### 4.1 ReviewSliceSet semantic projection eligibility

application 必须从 exact owned closure/receipt 决定：

- 哪些 normal candidates 可以成为 SliceSet members；
- zero-anchor 是否形成合法 empty SliceSet；
- conflict/upstream-unknown 是否允许 empty semantic SliceSet，同时怎样阻止它伪装成 closed empty；
- member ordering、`slice_id`、frontier 与 `slice_set_digest` 是否全部可复算；
- same semantics / different attempts 怎样共享 content identity而不共享 eligibility。

### 4.2 seven-stage Coverage composition qualification

Coverage application 必须从同一 exact owned history 机械建立七个 stages，而不是接受 caller 自报的分母和
disposition。至少需要证明：

- 每个 denominator 来自文档 120 冻结的 exact source；
- 每个 stage 的 terminal partition 双向闭合；
- stage N 到 N+1 没有凭空消失或重新出现的 item；
- Fact、Relation、Slice denominator subject identity 可追到 exact artifacts/obligations；
- Slice normal/partial/frontier 与 Ledger 完全一致；
- conflict、unknown、empty 与 interruption 不互相冒充；
- overall status 是七阶段保守机械汇合。

### 4.3 explicit public closure binding

第三方只拿完整 Bundle 时，必须能区分：

```text
semantic artifacts are internally valid
from
this exact attempt was eligible to publish those artifacts
```

后继合同必须先定义 application-owned witness/receipt claim，再决定它由 versioned Evidence 携带、由既有对象的
组合 conformance 复算，还是需要其他不破坏八文件布局的表达。禁止：

- SliceSet 自报 `admitted=true`；
- CoverageLedger 用 `COMPLETE` 证明自己的 denominator 有权威；
- Evidence 从 SliceSet/Coverage presence 反向签发 closure；
- Manifest 因为绑定 exact bytes 就升级为 judge；
- caller 直接提交 closure digest 或 stages 数组获得 publication authority。

## 5. 下一合同必须回答的问题

下一份 docs-only contract 至少要冻结：

1. **owned input join**：哪一个 private application value 同时拥有 exact admitted graph history、Slice closure/
   negative receipt 与后继一次性 continuation？
2. **SliceSet admission rule**：normal、empty、blocked/unknown 各自允许形成什么语义对象？
3. **Coverage responsibility**：谁拥有七个 denominator，谁逐项形成 terminal disposition，谁做跨 stage join？
4. **qualification result**：SliceSet 与 Coverage 是分别 qualification 后再 join，还是由一个共同 composition
   qualification 一次闭合？
5. **public witness**：什么最小 claim 能绑定 exact attempt、relation admission、Slice obligation closure、
   SliceSet 与 Coverage，同时不污染 content identity？
6. **carrier/versioning**：既有 Evidence、Manifest 与历史 corpus 怎样保持 byte compatibility？
7. **negative worlds**：known empty、conflict blocked、upstream unknown、interruption 与 caller omission 怎样被
   第三方区分？
8. **stop line**：何时必须因 Schema/carrier 不足重新审计，而不是在 runtime 中暗加字段？

## 6. 最小资格否定矩阵

| ID | 单变量世界 | 必须拒绝的结论 |
| --- | --- | --- |
| `SCQ-000` | H1/H2 semantics 相同、attempt closure 不同 | content identity 自动继承 fulfillment authority |
| `SCQ-001` | 首阶段缩空、下一阶段重新出现 item，Ledger 自洽 | Schema/digest/partition 足以证明 authoritative Coverage |
| `SCQ-002` | Evidence 0.2 只有 relation admission | complete Bundle 已公开绑定 Slice closure |
| `SCQ-003` | `slices=[]`，没有 typed closure/receipt | empty content 就是 closed empty |
| `SCQ-004` | Slice members 正确，Coverage denominator 少一个 obligation | SliceSet correctness 补足 Coverage completeness |
| `SCQ-005` | Coverage completed 引用均存在，但 SliceSet 少一个合法 obligation | completed refs 反向定义完整 denominator |
| `SCQ-006` | caller 提交正确 closure digest，未持有 owned closure | digest knowledge 等于 construction authority |
| `SCQ-007` | Manifest 精确绑定全部 bytes，但 witness/conformance 无效 | byte binding 修复 qualification |

本文只实际构造 `SCQ-000..003`；`SCQ-004..007` 是下一合同必须固化的资格反例，不冒充当前已运行测试。

## 7. 审计结论与后继停止线

本轮没有得到“现有 Schema 必须修改”的结论，也没有得到“现有 Schema 已足够完成 public binding”的结论。
得到的是一个更窄的事实：

> A–H 已经证明一组 Slice obligations 可以在正确的 attempt、输入与预算下诚实闭合；它还没有证明这些
> private results 何时有资格成为公共 ReviewSliceSet、何时七阶段 Coverage 可以整体成立，以及完整 Bundle
> 怎样证明这两项公共内容来自同一次合法履责历史。

因此下一条 seam 识别为：

```text
ReviewSliceSet / Coverage Composition Qualification
and Public Closure Binding
```

合法下一步只有：从本文闭合后的新 exact main 起草独立 docs-only 最小合同，并用 `SCQ-000..007` 审查。
在合同冻结前继续禁止：

```text
public ReviewSliceSet / CoverageLedger runtime
Schema / corpus / identity-vector changes
Evidence or Manifest version changes
publisher / output root / public Bundle
Attention / CLI / Workbench
```

外部大厂案例仍不需要进入问题选择：当前内部代码、历史合同与本地反例已经给出真实 blocking seam。

