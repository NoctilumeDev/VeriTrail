# R1 Fact → Coverage same-attempt handoff 最小合同 0.1

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_CANDIDATE`。
>
> 基线：`main@ec0f7e08f45be57754e0cfe86f000de7ac045e4b`；tree
> `42654472044c4b64fb8c6607cc560f69ab9222e4`。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结 private same-attempt Fact-stage history 的
> 一次性交接语义；不创建 runtime、Schema、public carrier、persistence 或 Coverage。

## 1. CONTROL LOOP 与 qualified upstream

[文档 258](258-r1-fact-to-coverage-same-attempt-handoff-current-state-audit.md)已经完成自己的资格链。PR #297
final head `f6dd90cc4b50b0891b8a0ceb759ea8047999f2e2` 由 ordinary merge 合入本基线；candidate/merge tree
均为 `42654472044c4b64fb8c6607cc560f69ab9222e4`。original Public CI `38322762959` 与 exact-main
Public CI `38325172987` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38325172966` attempt 1 / 1/1 SUCCESS。

fresh README/doc258/milestones installed-product observations 各自 P1/P2 COMPLETE、Core PASS；independent
reconciliation attempt 1 的 `KeyError: publication_world` 作为 proof-facility failure 保留，最小修正只把上游 closeout
key 改为实际的 `target_commit_sha`。attempt 2 reconciliation
`97056811f6e0146cb36aeec710a9c1a0a0b4d2e3d07c3b5497b56d7d3b5b47ad` PASS，136-artifact
closeout 为 `353f00e0818e4d9fa72863fc19a5e2a48e17f959d7f5afb5482bc6e692bb1e87`。因此本轮消费：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
```

重新核对本基线、open PR、doc252、doc257、doc258、current private object graph 与 Coverage 0.1 vocabulary，未发现
需要重开 Fact contract/runtime、先选 persistence 或先实现 Coverage 的新事实。并行 open PR 仍只有旧 Dependabot 更新。
所以当前最小合法问题是 handoff contract，不是 handoff runtime 或 seven-stage composition。

## 2. 本合同解决的问题

frozen `OwnedProductFactClosure` 及其 live parent graph 已经保留：

```text
complete Parse partition
complete Fact obligation universe U
representable expected semantics E
projection blockers and mapping history
complete applicable Provider responsibility
child lifecycle / execution / terminal history
FactSet or explicit absence
original attempt / BudgetContext authority
```

但 current `ClaimedProductFactContinuation` 只暴露 FactSet copy 与原 BudgetContext。它不能交出完整责任历史，且 zero
denominator、all rejected、unrepresentable U、required Provider failure 与 unsafe/interrupted world 都不能取得 normal
continuation。于是：

```text
authoritative Fact history retained
    != downstream authority to consume that history

FactSet / digest / current normal continuation
    != Fact-stage handoff
```

本合同只定义第二条边界：谁可以从 exact frozen Fact history 取得一次 private、same-attempt、one-shot handoff，以及
handoff 必须保留哪些语义。它不把 handoff 解释成 Coverage stage、Coverage status、CoverageLedger 或 public closure。

## 3. authority topology

首版 authority topology 冻结为：

| 对象 / 决定 | authority owner | 明确没有 authority 的主体 |
| --- | --- | --- |
| exact source / Policy / Profile / Parse history | frozen upstream owned object graph | caller、Coverage assembler、digest holder |
| Fact obligation universe `U` 与 representable expectation `E` | frozen Fact projection function + application | Provider output、FactSet members、Coverage schema |
| applicable Provider responsibility / requiredness | frozen application applicability and Fact closure | Provider self-report、successful subset |
| Fact terminal history | exact owned Fact closure/parent history | FactSet、normal continuation、replayed document |
| handoff semantic projection | 本合同的 application-owned function | caller-supplied stage、Provider、future publisher |
| live handoff claim | original live Fact attempt through application | equal bytes、equal limits、foreign attempt、digest knowledge |
| FACT_DERIVATION stage mapping and Coverage disposition | future Coverage qualification contract | 本 handoff、Fact closure、public Schema alone |
| publication / Verdict | future public authority | handoff consumer |

核心分离为：

```text
Fact semantic closure
    != live handoff authority
    != Coverage item mapping
    != Coverage qualification
    != public closure
```

## 4. semantic function 与 exact input identity

首版 handoff semantic function identity 冻结为：

```text
r1-fact-to-coverage-handoff/0.1
```

其完整 semantic input 必须共同绑定：

```text
exact DerivationInputSet / Language Support / Parse attempt identity
exact Parse denominator and accepted/rejected partition
exact Fact consumer function and consumer attempt identity
complete U / E / blocker / mapping history
complete applicable Provider descriptor, requiredness and child history
exact terminal/frame/execution provenance
FactSet semantic identity or exact absence
original BudgetContext object / deadline / stop state
handoff function identity
```

任一 digest、FactSet、ProviderRun 列表、closure document、normal continuation 或 caller stage 都不是完整 input identity。
semantic handoff projection 可以是可复算的 derived value；live claim 仍必须来自原 owned object graph，并重新验证对象身份、
完整历史、original BudgetContext 与当前 stop state。

## 5. total handoff branches

handoff function 必须对已冻结的 Fact-stage terminal worlds 作 total classification。以下名称描述规范语义分支，**不是**
预选 public enum、Schema 字段或 Python 类名：

| semantic branch | 必须保留 | 禁止推导 |
| --- | --- | --- |
| normal fulfilled | complete U/E、FactSet、all required Provider fulfillment、optional gaps、all child history | optional gap 不存在；all Providers fulfilled |
| zero Parse denominator | `0/0/0` Parse partition、U/E 为空、无 child、无 FactSet | 与 all rejected 相同；empty FactSet fulfilled |
| all Parse rejected | non-zero Parse denominator、accepted=0、完整 rejected history、U/E 为空、无 child、无 FactSet | 与 zero denominator 相同；Fact Provider 已执行 |
| projection blocked | complete constructible U、representable E 子集、每个 blocker 与 mapping history、无 ordinary child/FactSet | 用 E 或 actual output 缩小 U；把 blocker 改写成 Provider failure |
| required Provider non-success | complete U/E、全部 applicable responsibility、真实 completed/non-success child history、无 normal FactSet | U/E 可复算等于 fulfillment；successful subset 可发布 |
| interrupted / unsafe attempt | 原 stop/release/retained-observation history与已知 U/E 边界；无 normal claim | 用 partial prefix、普通 optional gap 或 fabricated closure 恢复 normal authority |

普通 optional Provider non-success 属于 normal fulfilled branch 的显式 gap：只要所有 required Provider 独立 fulfilled，
FactSet 可以成立；但 `all_provider_fulfilled` 不成立，optional identity/lifecycle 不能从 Fact provenance 数量反推或删除。

interrupted / unsafe world 若当前 private values 无法形成可独立验证的 terminal source，handoff qualification 必须 fail
closed，且不得启动 Coverage。实现可行性审计必须判断能否只从 frozen parent/observation/stop history形成该输入；不能为补齐
handoff 而倒写 Fact outcome、制造 normal closure 或放宽 release/budget 语义。

## 6. denominator 与 obligation-slot identity

FACT_DERIVATION denominator 的 authority source 是完整 `U`，不是 FactSet、`E`、reported IDs 或 successful Provider output。
每个 U slot 至少绑定：

```text
subject_key_digest
product subject / semantic identity
node path / alias ordinal
source anchor identity
Fact projection function identity
```

对 representable slot，handoff 同时保留 U→E→actual Fact 的精确对应。对 unrepresentable slot，U 仍存在，但没有合法
expected Fact / Fact ID。handoff 必须保留该 slot 与 blocker，不能：

- 丢弃它后把剩余 E/FactSet 当作完整 denominator；
- 借用另一个 Fact ID、subject digest 或任意 semantic digest 冒充 public `FACT` item；
- 临时改写成 `DERIVATION_ERROR`、`UPSTREAM_DENOMINATOR_UNKNOWN` 或 Parse rejection；
- 因现有 Coverage 0.1 `CoverageItemRef` 只有 `FACT` digest 形状，就让 Schema 反向定义 U。

因此本合同冻结的是**无损 private obligation-slot handoff**。U slot 到 future Coverage item/disposition 的映射仍是后继
Coverage qualification 问题；若现有 vocabulary 无法表达，必须停下来审查最小 successor/Schema，不能在 runtime 中
静默压缩。

## 7. responsibility 与 terminal partition

handoff 必须按 application-owned complete applicability 保留每个 Provider 的：

```text
descriptor / binding / requiredness
provider-bound claim and child attempt
request / assigned product set
lifecycle / execution / terminal identity
reported Fact IDs
fulfillment and provenance reconciliation result
```

required、optional、ordinary failure、unavailable、unsafe release 与 shared stop 必须保持区别。两个 partial Provider outputs
的 union 不能修复各自未履责；FactSet provenance 也不能证明没有未报告或失败的 applicable Provider。

handoff 只交出 frozen Fact-stage partition facts：U/E/blockers、actual completed Fact 对应、per-Provider terminal history 与
whole-attempt safety state。它不把这些 facts 预先填入 Coverage 0.1 的 `completed / execution_failed / unsupported` 字段，
也不预选 denominator `UNKNOWN` 或 coverage status；该映射由 future Coverage contract 独立拥有。

## 8. one-shot claim、revalidation 与 revocation

application 只能从 exact upstream owned history 发出一个 handoff claim。claim 至少绑定：

```text
original Fact parent / closure or qualified terminal source object identity
original consumer attempt and claimed upstream Parse authority
original BudgetContext object / deadline / stop latch
complete semantic projection bytes
handoff function identity
consumer identity
claim nonce / one-shot state
```

claim 前必须重新验证 source object、terminal history、child authority、FactSet/absence、input seal 与 remaining live authority。
claim 一旦成功领取、验证失败、竞争失败或原 attempt 停止，就不能重放。相同 U/E、FactSet、closure bytes、digest、limits
或重新构造的 Context 都不继承 authority。

handoff 的 copy-owned semantic input 可以在 claim 后供同一 authorized downstream consumer 使用；它不能携带 mutable
repository handle、lazy loader、重新执行 Provider/Parse 的能力或修改上游 history 的引用。若下游需要重新观察源码或执行
Provider，必须另立新 attempt，不能冒充本 handoff 的延续。

## 9. consumer boundary 与 authority ceiling

首版只允许 application-owned future Coverage composition consumer 领取 handoff。caller 不能提交自造 stage，Provider 不能
自证履责，public publisher 不能凭 serialized bytes 取得 live claim。

handoff 成功只证明：

> 在一个 exact live attempt 中，完整 Fact-stage authoritative history 已按本合同无损交给一个受约束 downstream
> consumer。

它不证明：

```text
FACT_DERIVATION Coverage stage is valid
seven-stage joins are qualified
Coverage status is COMPLETE / PARTIAL / UNKNOWN
ReviewSliceSet is admitted
public Schema can represent every slot
Bundle is self-contained
repository semantics are complete
```

handoff consumer 不得修改 U/E、重跑 observation、选择性忽略 negative branch、定义自己的 denominator，或把“收到输入”
写成“Coverage 已完成”。

## 10. persistence、carrier 与版本停止线

本合同选择 same-attempt private handoff，不选择 persistence Route A/B。live owned graph 足以定义 authority；这不证明离线
或 public consumer 能重建同一 history。serialized projection 即使逐字节相同，也只保存 semantics，不自动保存 live claim。

具体 private class、method、field、exception、digest document 与 storage carrier 是 implementation non-decision。以下任一条件
出现时必须停在 feasibility/implementation boundary：

- 只能通过修改 frozen Fact U/E、consumer status 或 child lifecycle 才能形成 handoff；
- 需要重新 parse、重新执行 Provider、刷新 BudgetContext 或恢复已停止 attempt；
- 需要让 public Coverage 0.1 把 unrepresentable U slot 伪装成现有 `FACT` item；
- 需要先选择 persistence、Evidence、Manifest、Bundle 或 publisher；
- 需要把 normal continuation 扩权成 negative-history carrier；
- 需要让 handoff 自己决定 seven-stage status/join。

若 private lower-level identity/provenance primitive 可以复用，必须先证明共同不变量；不得因字段看起来相似就创建通用
ObservationLedger 或改写既有 private closure。

## 11. normative falsifier obligations

以下是后继 feasibility / implementation 必须攻击的 contract worlds，不冒充本轮已实现测试：

| ID | 单变量 world | 必须拒绝的结论 |
| --- | --- | --- |
| `FCHC-000` | Fact IDs/bytes 相同，all complete 与 optional failure 的 responsibility 不同 | Fact content identity 证明 all Providers fulfilled |
| `FCHC-001` | zero denominator 与 all rejected 都无 FactSet | empty output 定义同一 terminal history |
| `FCHC-002` | U=3、E=2、FactSet absent | E/Fact IDs 是完整 denominator；未知 slot 可丢弃 |
| `FCHC-003` | U/E 完整，required Provider failure | universe construction 等于 fulfillment |
| `FCHC-004` | unsafe release/interruption 后有 partial completed observation | partial prefix 可恢复 normal handoff |
| `FCHC-005` | caller 持有 exact closure bytes/digest，但没有 owned source | semantic knowledge 等于 live claim |
| `FCHC-006` | fresh equal-limits Context 或 foreign consumer attempt | equivalent environment 继承 same-attempt authority |
| `FCHC-007` | normal continuation 给出 FactSet/context，未给 responsibility | downstream 可以从 provenance 反推完整 history |
| `FCHC-008` | duplicate/replayed handoff claim | same source 可被两个 Coverage consumers 重复领取 |
| `FCHC-009` | Provider order 变化，semantic projection相同 | execution order 改写 responsibility 或 canonical handoff bytes |
| `FCHC-010` | Coverage 0.1 用 arbitrary digest 给 unrepresentable U slot 造 `FACT` ref | schema-valid shape 证明合法 item identity |
| `FCHC-011` | handoff semantic input完整 | handoff 自己有资格发布 FACT stage/overall Coverage status |

`FCH-000..007` 的 qualified audit history继续是 contract motivation；本合同新增 one-shot、unsafe-interruption、canonical
ordering、unrepresentable mapping 与 authority-ceiling falsifiers。后继必须分别证明，不能用单个 happy-path continuation 代替。

## 12. 本候选自己的资格门

tracked scope 只允许 README、AGENTS、milestones 与本文。doc252–258、runtime、tests、workflows、Schema、Profile、
Policy、fixtures、identity vectors 与架构资产保持基线字节。

final bytes 的本地门至少包括：UTF-8 without BOM、LF/final LF、links/fences/headings、状态 marker、scope 与全部其他
tracked bytes continuity；unchanged Fact fulfillment、Parse→Fact consumer、Coverage schema semantic checks 与 docs/hygiene
回归按声明矩阵运行。测试只作 witness，不将 existing Coverage fixture 升格为本合同实现。

首个 CPython 3.10 normal 调用在前三个模块分别通过 `28 (skipped=1) / 34 (skipped=1) / 22` 后，因直接执行
`tests/test_hygiene.py` 时 `PYTHONPATH` 只含插件源码而不能导入仓库 `scripts`，以 `ModuleNotFoundError` 终止。该身份为
`LOCAL_TEST_INVOCATION_SETUP_ERROR`；不改产品、测试、预算或断言，只在 fresh cell 同时加入仓库根与插件源码。

修正调用环境后的 CPython 3.10.6 / 3.13.13、normal / `-O` 四个 fresh cells 各自：Fact fulfillment
`28 reported / 27 passed / 1 skipped`、Parse→Fact consumer `34 / 33 / 1`、Coverage schema semantics `22 / 22 / 0`、
hygiene `5 / 5 / 0`，合计 `89 reported / 87 passed / 2 skipped`。两个 skip 均为需要显式 reference runtime 与 Windows
cell 的 actual-child witness，不能写成实际通过。字节、scope 与 markdown gates 的最终结果另由 qualification artifact
封存；本节不替代 original PR 或 exact-main gates。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / this contract / milestones installed-product observations
    -> independent Core, source-byte and retained-history reconciliation
    -> qualified contract candidate history
    -> separate docs-only freeze publication with its own complete qualification chain
    -> CONTRACT_FROZEN
    -> return CONTROL LOOP / feasibility and explicit implementation authorization
```

最后门闭合前只允许：

```text
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

即使合同以后冻结，也不自动获得 handoff implementation authority 或 Coverage contract authority。下一步仍由新证据和
CONTROL LOOP 决定；不得按文档编号自动进入 runtime、Schema、persistence、ReviewSliceSet/Coverage、Evidence/Bundle/
publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。
