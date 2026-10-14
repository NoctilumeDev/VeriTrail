# R1 Fact → Coverage same-attempt handoff 私有实现可行性审计

日期：2026-10-15

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 基线：`main@bf6bedb002c1a9a4ade7e64b385be742dcf012fd`；tree
> `6f6b5ca7c60c8982967536a98111eb81cdc55187`。
>
> 影响：`L2_IMPLEMENTATION_FEASIBILITY_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本文只审查
> [文档 259](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)的 private implementation shape；不修改
> runtime、tests、Schema、Profile、Policy 或 frozen contracts，也不授予 implementation authority。

## 1. CONTROL LOOP 重新绑定与结论

[文档 260](260-r1-fact-to-coverage-handoff-contract-freeze-publication.md)已经完成自己的资格链。PR #300 final head
`28f5fdcc11589b177e7005bb536a39da9e27cc15` 由 ordinary merge 合入本基线；merge tree 为
`6f6b5ca7c60c8982967536a98111eb81cdc55187`。original Public CI `38639738028` 与 exact-main Public CI
`38643028967` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38643028948` attempt 1 / 1/1 SUCCESS。

fresh README/doc260/milestones installed-product observations各自 P1/P2 COMPLETE、Core PASS；independent
reconciliation：

```text
ddf865aac99f1af7cf27dc69f73c04bdc251b88e02e5eb05b0d3fdfbca5358e2
```

149-artifact closeout：

```text
604f69a6784b36861507aa2020247dd5f5967b0756553884a662fc44de6be6a9
```

exact-main 原始日志的 Review Attention 四格实际各为 `501 reported / 498 passed / 3 skipped`。第一次 count extractor
仍按旧预期断言而失败，第一次 gate seal 随后因 count file 缺失而失败；最小 proof-facility 修正后 fresh extractor 与
seal 通过。没有 rerun CI，也没有修改产品、合同或 oracle。上述历史使：

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
```

成为当前事实；它没有自动授权实现。重新 fetch 后远端、本 worktree 与 `origin/main` 均为本基线，语义并行 PR 不存在，
只有旧 Dependabot PR。因此本轮只问：

> 能否在不修改 frozen Fact U/E、Provider lifecycle、Coverage 0.1、persistence 或 public surface 的前提下，用现有
> private owned graph 实现文档 259 的 total semantic projection 与 same-attempt one-shot handoff？

结论是：**有限 private successor boundary 内可行。** 现有对象图已经保存所需事实和 live identity；缺的是独立于
`ClaimedProductFactContinuation` 的 handoff-specific projection、互斥 one-shot claim 与 safe terminal-source
qualification。它们可以在 private application 层增加，不需要重跑 Parse/Provider、恢复 stopped attempt、选择
persistence 或让 Coverage Schema 反向定义 Fact denominator。

本文仍只是 docs-only candidate。自己的完整资格链闭合后最多成为 `FEASIBILITY_AUDITED` history；runtime 在独立
implementation authorization 生效前继续 `NOT_STARTED / NOT_AUTHORIZED`。

## 2. 审计方法与证明强度

本轮直接读取 frozen source、doc259 §10–12、Coverage 0.1 vocabulary 与 retained counterexamples，并在仓库外构造
七个单变量 world：

```text
normal fulfilled
optional Provider ordinary failure
zero Parse denominator
all Parse rejected
projection blocked with U=3 / E=2
required Provider failure
optional Provider unsafe release after completed required children
```

audit matrix 只调用 current private factories、closed bindings 与 test cell witness；没有修改 repository tracked bytes，
没有创建 handoff 类，也没有把 audit projection 当作实现。另有 reversed-binding 与 equal-semantics/foreign-attempt world
分别检查 canonical Provider order 与 authority identity。

| Evidence | 实际证明范围 | 不能提升成的 claim |
| --- | --- | --- |
| current object-graph inspection | required inputs、owned refs、locks 与 exact observations 已存在 | handoff runtime 已实现 |
| seven-world matrix | 当前 worlds 可机械区分，negative history没有被 FactSet 压平 | 任意未来 Fact world 已穷尽 |
| reversed binding world | application normalization 不依赖 caller execution order | arbitrary third-party Provider ordering 已受支持 |
| equal-semantics world | 相同 qualification 不继承 Context、consumer 或 claim identity | identity primitive 可跨 attempt 复用 |
| Coverage 0.1 source inspection | 当前 vocabulary 不能合法表达无 Fact ID 的 U slot | 已选择 successor Schema 或 disposition |
| unchanged four-cell regression | frozen upstream 仍满足自己的原声明 | handoff/Coverage authority 已取得 |

最终 matrix script SHA-256：

```text
6598543d15e6fbd927a335771c3419ceb632e202fda937e8360613b10582834e
```

CPython 3.10.6 / 3.13.13、normal / `-O` 四格去除 interpreter identity 后逐字节一致，canonical SHA-256：

```text
22cc3c8ac29d31a891711fc7b8c49cd5b5c51e8b17805197751243cc7880462e
```

## 3. current private object graph 已经保存完整输入

`OwnedProductFactConsumer` 当前仍拥有并绑定：

```text
original ClaimedParseContinuation / Parse attempt
exact DerivationInputSet and input seal
original BudgetContext object and budget identity
original AttemptEligibility
OwnedParseProductSet and Language Support classification
application qualification bytes with U / E / blockers / mapping history
complete normalized Provider bindings and requiredness
all Provider claims, execution history and reconciliation history
```

`OwnedProductFactClosure.document_copy()` 已保留 Parse partition、application projection、consumer status、ordered child
requests/lifecycle/execution、reported Fact IDs、terminal/frame digest 与 FactSet/absence。活的 closure 另外仍持有同一批 sealed
`OwnedProductFactObservation` 成员；每个 observation 保存 exact terminal bytes、terminal frame bytes、execution bytes 与
canonical Fact bytes。closure 与 parent 使用不同 tuple 容器，但成员逐项保持对象 identity；实现不需要从文档摘要反推
原始 observation。

因此 handoff semantic input 可以从 exact owned graph copy 出来。它不需要 repository handle、lazy loader、source reread、
Provider rerun 或 public Artifact。`document_copy()` 本身仍不是 live authority；完整 bytes/digest 的持有者也不能绕过
source object、Context 和 claim state。

## 4. total branches 的可区分性

最终四格得到相同的规范投影：

| branch | Parse denominator / accepted / rejected | U / E / blockers | child lifecycle | FactSet | pre-claim authority |
| --- | --- | --- | --- | --- | --- |
| normal fulfilled | `1 / 1 / 0` | `14 / 14 / 0` | `COMPLETED, COMPLETED` | present | Context RUNNING / parent ADMITTED |
| optional gap | `1 / 1 / 0` | `14 / 14 / 0` | `COMPLETED, COMPLETED, FAILED` | present | Context RUNNING / parent ADMITTED |
| zero denominator | `0 / 0 / 0` | `0 / 0 / 0` | none | absent | Context RUNNING / parent ADMITTED |
| all rejected | `1 / 0 / 1` | `0 / 0 / 0` | none | absent | Context RUNNING / parent ADMITTED |
| projection blocked | `1 / 1 / 0` | `3 / 2 / 1` | none | absent | Context RUNNING / parent ADMITTED |
| required failure | `1 / 1 / 0` | `14 / 14 / 0` | `FAILED, FAILED` | absent | Context RUNNING / parent REVOKED |
| unsafe release | `1 / 1 / 0` | qualification retained | `COMPLETED, COMPLETED, RELEASE_FAILED` | no normal closure | parent REVOKED |

zero denominator 与 all rejected 的 `consumer_status` 都是 `BLOCKED_NO_ACCEPTED_PRODUCTS`，但 exact Parse partition 不同；
handoff 不能只看 status 或 empty output。normal 与 optional gap 的 Fact content可以相同，但 requiredness 和完整 child history
不同；FactSet 不能证明 all Providers fulfilled。projection-blocked world 保留完整 U=3、representable E=2 和 blocker，不能
用 E 缩小 denominator。

矩阵故意调用旧 `claim_continuation()` 后，三个 safe negative closure 都 fail closed 并撤销 parent eligibility；调用前它们
仍是 ADMITTED。该差异证明 observer/claim order 是 authority 的一部分：handoff 必须直接领取自己的 mutually-exclusive
claim，不能先探测 legacy continuation 再尝试恢复 authority。

## 5. normal continuation 不能充当 handoff

current `OwnedProductFactClosure` 已有 lock 与单次 `__claimed` 状态，但 `claim_continuation()` 只接受
`consumer_status == COMPLETED`，并只暴露 FactSet copy 与 original Context。因此：

```text
legacy normal continuation
    != complete Fact-stage history
    != negative terminal source
    != handoff claim
```

后继实现可以复用同一个 closure-level claim mutex，使 legacy continuation 与 new handoff 互斥；不能另建两个彼此不知道的
one-shot flag。handoff成功、legacy claim 成功、验证失败或竞争失败中的任一项都必须永久消费或撤销该 source。equal
qualification world 已证明两个 independently created consumers 的 Context、consumer 与 claim objects 全部不同；fresh
equal-limits Context 或 foreign attempt 不能继承 authority。

normal/optional branch 的 handoff eligibility 必须要求 original parent ADMITTED、Context RUNNING、无 stop latch，并重新验证
closure、observations、qualification、FactSet 与 exact inputs。safe negative terminal branch 不能调用
`_authorize_continuation()`；它需要 handoff-specific terminal eligibility，显式接受合同允许的 terminal state并仍要求 original
Context RUNNING、无 stop latch、完整 sealed history。仓库已有 `_DiagnosticClosureEligibility` 的“revoked parent + live safe
Context + one-shot”模式可作机制参照，但其 token、purpose 和 semantics 不能被直接冒充为本 handoff，也没有理由抽象成
通用 ObservationLedger。

## 6. unsafe / interrupted 是 fail-closed branch

unsafe-release world 中，current `reconcile()` 保留三个 exact observations并拒绝 join，`__closure` 仍为 `None`。这不是缺少
normal closure 的 bug；它防止 partial prefix 取得 continuation。

首版 handoff实现可在 application reconciliation boundary 对 retained observations逐项验证并形成不可领取的 terminal
qualification result，或者直接返回 path-free handoff rejection。它不得：

- 把已完成的 required prefix 包装成 normal handoff；
- 因 Context仍显示 RUNNING 而忽略 release failure；
- 创建 FactSet、Coverage item 或 unknown denominator 来掩盖没有 safe terminal source；
- 恢复 parent eligibility、刷新 BudgetContext 或重跑缺失 child。

如果实现无法在异常返回前形成 sealed、可独立复核的 terminal-source state，就必须维持 no-claim 并停止 Coverage。本审计
没有选择 public failure carrier；它只证明 current exact observations足以让 application deterministic fail closed。

## 7. canonical semantic projection 与 copy ownership

current applicability 会按 descriptor rank 规范化 caller提交的 bindings。反向提交三个 bindings仍得到：

```text
closed-fact-fulfill-a
closed-fact-fulfill-b
closed-fact-fulfill-advisory
```

reconciliation 也按 canonical claim order 重排 observations。因此 handoff bytes 可以用 frozen U/E ordering、Parse partition
ordering 与 canonical Provider order 构造，不受 child completion order影响。

copy-owned handoff input 至少需要：

```text
handoff function identity
exact upstream identities and input seals
Parse denominator / accepted / rejected partition
complete U / E / blockers / mapping history
Provider descriptor / requiredness / claim / request / lifecycle / execution history
exact terminal / frame / canonical Fact bytes or their owned validated value
FactSet bytes or exact absence
whole-attempt safety state
consumer identity and one-shot claim identity
```

projection不得携带 mutable parent、repository handle、lazy bytes loader 或重新执行能力。live claim对象可以短暂引用原 owned
source来验证 authority；领取后交给 downstream 的 semantic value必须 copy-owned。serialized equality只证明 semantics，
不保存 live claim。

## 8. Coverage 0.1 仍是明确停止线

Coverage 0.1 的 `CoverageItemRef` 对 `FACT` 要求一个 semantic digest；它没有 obligation-slot item kind。unrepresentable U slot
只有自己的 subject/product/node/anchor identity，没有合法 Fact ID。把 subject digest 填进 `FACT.item_id` 虽可能通过 shape，
仍是 semantic forgery。

因此 handoff private implementation只交付 U slot 与 blocker；它不能决定：

```text
U slot -> Coverage item identity
blocker -> DERIVATION_ERROR / UNKNOWN / another disposition
FACT_DERIVATION stage status
seven-stage joins or overall coverage
```

source scan也确认 current `_fact_fulfillment.py` 不导入 Coverage runtime或 public Coverage Schema。实现若需要修改
`review-coverage-ledger-0.1.schema.json`、伪造 Fact ID 或预先选择 disposition，必须停下并返回 CONTROL LOOP；这不是
handoff feasibility 的一部分。

## 9. FCHC falsifier 到实现责任的映射

| contract falsifier | 可行机制 / 必须直接证明的事实 |
| --- | --- |
| `FCHC-000` | semantic projection保存 requiredness与全部 child history，不以 Fact bytes推断 responsibility |
| `FCHC-001` | Parse partition进入 projection，zero denominator与all rejected保持不同 bytes |
| `FCHC-002` | denominator取完整 U；E=2、U=3 时 blocker和第三个 slot仍存在 |
| `FCHC-003` | required failure保留 U/E但没有 FactSet；terminal eligibility不把 construction 当 fulfillment |
| `FCHC-004` | unsafe/interrupted只产生 no-claim terminal decision；partial prefix不能领取 |
| `FCHC-005` | claim验证 owned closure/parent identity；serialized copy没有 construction token |
| `FCHC-006` | 绑定 original Context object、attempt、consumer和stop state；equal limits无效 |
| `FCHC-007` | handoff不消费现有 FactSet-only continuation，直接从 complete owned history构造 |
| `FCHC-008` | handoff与legacy continuation共享一个 mutually-exclusive source claim state |
| `FCHC-009` | U/E和Provider descriptor按 frozen rank canonicalize，不用 completion order |
| `FCHC-010` | unrepresentable slot留在 private U；不生成 `FACT` ref |
| `FCHC-011` | consumer只取得 Fact-stage input；API没有 Coverage status/join/publish 方法 |

这些仍是 future implementation必须新增的直接 tests；本轮 matrix只证明现有 source足以构造它们，不冒充 tests已存在。

## 10. 最小 private implementation 候选面

若本审计最终取得资格，后继 implementation authorization 最多只能覆盖：

```text
A. exact Fact parent / closure / input / BudgetContext revalidation
B. r1-fact-to-coverage-handoff/0.1 total semantic projection
C. canonical Parse / U / E / blocker / Provider / observation ordering
D. normal and safe-negative handoff-specific source qualification
E. closure-level mutually-exclusive one-shot claim shared with legacy continuation
F. fixed application-owned Coverage-composition consumer identity
G. copy-owned private handoff value with no rerun or mutation capability
H. unsafe/interrupted no-claim fail-closed path
I. same-attempt revocation, replay, foreign-context and competition hardening
J. FCHC-000..011 direct implementation falsifiers and unchanged upstream regression
```

具体 module/class/method/field 名称仍是 implementation non-decision。最小实现可以向 current private Fact module增加窄
validation/handoff入口，也可以新增一个 private successor module；它不能修改 frozen U/E算法、FactSet、Provider lifecycle、
old protocol bytes或 public package API。

以下任一需要都立即停止：

- 重新读取 source、重跑 Parse/Provider、补写 expected answers；
- 恢复 stopped attempt、替换 Context、放宽 Budget/release semantics；
- 改写 requiredness、child lifecycle、U/E/blocker 或旧 Fact closure bytes；
- 选择 persistence、public Schema/carrier、Coverage vocabulary/status/join；
- 让 caller自造 consumer identity、denominator或 completion claim；
- 为复用字段而建立通用 ObservationLedger。

## 11. 首败、审计修正与 retained history

首个 Python 3.10 normal audit matrix 在读取 Provider order 时错误假定 descriptor位于
`request.provider_descriptor`；current wire实际是 `request.projection.provider_descriptor`。attempt 1 以
`KeyError: provider_descriptor` 保留为 `AUDIT_PROJECTION_ASSUMPTION_ERROR`，没有形成产品/合同结论。

fresh attempt 2修正 read path后通过。后续输出显示 closure 与 parent history 的 tuple容器不同；审计随后同时记录 container
identity与逐成员 object identity，避免把容器不同误报成 observation丢失。再一次 refinement把 negative world的
pre-claim state与故意调用 legacy continuation后的 revoked state分开，避免审计动作污染原状态。全部旧脚本和输出保留，
最终 v4四格没有覆盖 attempt 1。

unchanged regression 的四个 cells 各为：

```text
Fact fulfillment                 28 reported / 27 passed / 1 skipped
Parse -> Fact consumer           34 reported / 33 passed / 1 skipped
Coverage Schema semantics        22 reported / 22 passed / 0 skipped
hygiene                           5 reported /  5 passed / 0 skipped
total                            89 reported / 87 passed / 2 skipped
```

两个 skip仍是需要 explicit reference runtime / Windows actual-child witness，不能写成实际通过。测试只证明 frozen upstream
continuity，不证明 handoff runtime。

## 12. 本候选自己的资格门与停止线

tracked scope只允许 README、AGENTS、milestones与本文。doc259/doc260、runtime、tests、workflows、Schema、Profile、
Policy、fixtures、identity vectors与架构资产保持基线字节。

final bytes本地门至少包括：

1. final v4 matrix四格 byte reconciliation、attempt 1与中间 refinements完整保留；
2. 上述四模块 CPython 3.10.6 / 3.13.13、normal / `-O` 回归；
3. exact four-file scope、其余 tracked bytes continuity、doc259/doc260/source hashes、UTF-8 without BOM、LF/final LF、
   relative links、balanced fences、unique headings、状态 marker、禁止越权状态、`git diff --check` 与只读 hygiene。

完整资格链为：

```text
final docs-only feasibility bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / this audit / milestones installed-product observations
    -> independent Core, source-byte and retained-history reconciliation
    -> FEASIBILITY_AUDITED
    -> return CONTROL LOOP
    -> separate explicit implementation authorization, if still minimal
```

own chain闭合以前只允许：

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本文不发布 `FEASIBILITY_AUDITED` 生效事实，不发布 implementation authorization，不改 runtime/tests/Schema，不选择
persistence，也不启动 Coverage item mapping、ReviewSliceSet/seven-stage Coverage、Evidence/Bundle/publisher、
CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。
