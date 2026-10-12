# R1 Fact → Coverage same-attempt handoff 当前状态审计

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDIT_CANDIDATE`。
>
> 基线：`main@50ab803671674b8a88245480aae06b5ba8fec526`；tree
> `9369f3b43c9f08bf6ea43557794ea8dc14c51ea0`。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只审计 frozen Fact history 到未来 Coverage
> qualification 的 same-attempt handoff seam；不创建合同、runtime、Schema、public carrier 或 Coverage。

## 1. CONTROL LOOP 与上游事实

[Fact projection / fulfillment 合同](252-r1-fact-projection-universe-and-fulfillment-contract.md)、
[私有实现候选](256-r1-fact-projection-fulfillment-private-implementation-candidate.md)与
[独立冻结发布](257-r1-fact-projection-fulfillment-private-implementation-freeze-publication.md)已经完成各自资格链。
[PR #296](https://github.com/NoctilumeDev/VeriTrail/pull/296) final head
`cd3001a3f9acaf0c70941aee04e90363e99099aa` 由 ordinary merge 合入本基线；candidate/merge tree 均为
`9369f3b43c9f08bf6ea43557794ea8dc14c51ea0`。original Public CI `38285546808` 与 exact-main
Public CI `38316924237` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38316924154` attempt 1 / 1/1 SUCCESS。

fresh README/doc257/milestones installed-product observations 各自 P1/P2 COMPLETE、Core PASS；independent
reconciliation `ee148157be125b140dc0f6a8918977f93227dd14e4afbd875a2f8a415e62dbed` PASS，120-artifact
closeout `6d80880795b216d1cefce5dcead550ebe98b3f24bf0d8a2da864e28b9e7ecf1d`。setup1 adapter identity
错误与 post-reconciliation PowerShell 调用错误仍保留原身份，不改变冻结资格。

因此本轮消费的是已经生效的：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
```

当前 remote main、隔离 worktree 与本基线一致；并行 open PR 只有旧 Dependabot 更新，没有 semantic PR 改写本 seam。
主仓用户未跟踪文件没有进入审计或候选。

## 2. 本轮问题不是 Coverage 本身

[doc194](194-r1-fact-parse-observation-fulfillment-coverage-prerequisite-system-audit.md) 曾证明 full seven-stage
Coverage 缺少 Parse / Fact obligation universe 与逐项 fulfillment history。现在 Parse 与 Fact 的对应 private truth
已经冻结，旧 blocker 不能继续原样复用。

本轮只问：

> frozen Fact closure 是否已经保留足够的 authoritative history，使后继能够在原 attempt 中取得 denominator、
> responsibility、terminal partition 与 negative world；如果足够，当前又缺少哪一条合法消费边界？

这不等于问：

```text
CoverageLedger 0.1 怎样填七个 stages
ReviewSliceSet 怎样公开
Fact history 是否必须持久化
public Bundle 怎样携带 closure witness
```

这些仍属于后继合同或更晚阶段。

## 3. 当前 closure 保留什么，continuation 暴露什么

`OwnedProductFactClosure` 的 canonical document 已保留：

```text
consumer_function / consumer_status
product_set_digest / consumer_attempt_id
complete parse_partition
complete application_projection (U / E / blockers / mapping history)
per-Provider child request / lifecycle / execution / reported IDs
terminal and frame digests
FactSet or explicit absence
```

closure object 还持有原 parent 与 observation objects；observation 自身继续验证 exact terminal/frame bytes 和 child
authority。parent 则绑定原 Parse continuation、DerivationInputSet、BudgetContext 对象、deadline、eligibility、
qualification 与 claims。因此同一 live object graph 中没有发现必须先选择 persistence 才能表达的 history 缺口。

但 `ClaimedProductFactContinuation` 当前只提供：

```text
_fact_set_copy()
_context_ref()
```

它不提供 application projection、parse partition、child responsibility/lifecycle 或 negative closure。normal closure 才能
claim 这个 continuation；zero denominator、all rejected、unrepresentable U 与 required Provider failure 都没有 normal
continuation。现状因此是：

```text
authoritative history retained by closure
    != authorized downstream handoff projection

FactSet + BudgetContext access
    != Fact-stage responsibility closure access
```

这不是 Fact implementation defect。doc252 §10 与 doc257 §6 本来就明确没有授予 Fact→Coverage handoff API。

## 4. 六个独立 world

审计脚本只读复用 current exact-input/test helpers 与产品 validators。每个 world 都重新构造 attempt、BudgetContext、
eligibility、claims 与 closure；Fact child 使用 current protocol 的受控 test cell，不把这些 world 冒充真实 external
Provider 或 public Evidence。

| World | Parse denominator / accepted / rejected | U / E / Fact | child lifecycle | normal continuation |
| --- | --- | --- | --- | --- |
| all Providers complete | 1 / 1 / 0 | 14 / 14 / 14 | COMPLETED × 3 | yes |
| optional Provider failure | 1 / 1 / 0 | 14 / 14 / 14 | COMPLETED × 2 + FAILED × 1 | yes |
| zero Parse denominator | 0 / 0 / 0 | 0 / 0 / 0 | no child | no |
| all rejected | 1 / 0 / 1 | 0 / 0 / 0 | no child | no |
| unrepresentable U | 1 / 1 / 0 | 3 / 2 / 0 | no child | no |
| required Provider failure | 1 / 1 / 0 | 14 / 14 / 0 | FAILED + COMPLETED | no |

前两个 world 的 Fact IDs 与 semantic content 相同；完整 world 每 Fact 有 3 个真实 source provenance refs，optional
failure world 每 Fact 有 2 个。即使 downstream 看见 FactSet provenance 数量，也不能从中恢复 complete applicability、
失败 Provider identity 与未履责原因。必须消费 closure-owned responsibility history，不能用结果集合反推责任全集。

zero denominator 与 all rejected 最终都没有 FactSet/normal continuation，但 parse partition 分别为 `0/0/0` 与
`1/0/1`。empty result 本身不能区分“数学分母为空”和“上游逐项拒绝”。required failure 则保留完整 U/E 与两项
child history，却没有正常 FactSet；U/E 存在也不能冒充履责成功。

unrepresentable world 的 U 有 3 个 obligation slots，只有 2 个可构造 Fact IDs。它证明后继不能总把 FactSet members
或 expected Fact IDs 当作完整 FACT_DERIVATION denominator。

## 5. 当前可以成立的裁决

| 问题 | 裁决 | 边界 |
| --- | --- | --- |
| frozen Fact history 是否足够成为后继合同的上游 | **是** | closure/object graph 已保留 U/E、partition、责任、terminal、FactSet/absence 与原 attempt authority |
| current normal continuation 是否已经是 Coverage handoff | **否** | 它只暴露 FactSet 与 context；negative worlds 无 normal continuation |
| 是否需要重开 Fact projection / fulfillment | **否** | 没有发现 Fact contract/runtime 反例；缺口是尚未授权的 consumer seam |
| 是否已能冻结 seven-stage Coverage contract | **否** | handoff qualification、item/disposition mapping 与 cross-stage join 尚未定义 |
| 是否必须先选择 persistence | **否** | live private object graph 足以继续合同审查；offline/public consumer responsibility 仍未裁决 |
| current public Schema 是否已被证明足够或不足 | **均否** | 已发现 vocabulary seam，但尚未证明必须改 Schema，也未证明可以无损映射 |

因此新的最小 blocking seam 是：

```text
frozen OwnedProductFactClosure
    -> application-owned same-attempt handoff qualification
    -> exact Fact-stage denominator / terminal partition input
    -> future seven-stage Coverage composition qualification
```

本审计不把第三个箭头倒推成当前已拥有 Coverage authority。

## 6. 后继合同必须裁决的最小问题

如果本 current-state audit 取得自己的资格，后继最多有资格重新审查一份 docs-only minimal handoff contract。它至少要回答：

1. **claim owner**：谁从 exact `OwnedProductFactClosure` 取得一次性 handoff；caller/digest/FactSet 不得自领资格；
2. **same-attempt continuity**：怎样绑定原 BudgetContext 对象、consumer attempt、Parse partition、U/E/function 与
   child history，不接受 fresh equal-limits context 或 foreign closure；
3. **normal responsibility**：如何同时传递 Fact content、完整 applicable Provider membership、required/optional/safety
   lifecycle 与 provenance reconciliation；
4. **negative worlds**：zero denominator、all rejected、unrepresentable U、required failure 与 interruption 分别交出什么
   typed input，并且谁都不能伪装成 empty fulfilled FactSet；
5. **denominator identity**：representable U/E 怎样映射到 `FACT` item refs；不得由 actual FactSet 缩小 denominator；
6. **unrepresentable slots**：没有 total Fact ID 的已知 U slot 怎样进入或阻断 Coverage；不能临时借用
   `DERIVATION_ERROR`、`UPSTREAM_DENOMINATOR_UNKNOWN` 或任意 digest 掩盖语义缺口；
7. **one-shot / reuse**：semantic content 可以复算，但 live handoff authority 怎样 one-shot、撤销并阻止跨 attempt 移植；
8. **authority ceiling**：handoff 只提供 frozen Fact-stage history，不能拥有 seven-stage join、Coverage status、public
   Verdict、ReviewSliceSet admission 或 publication authority；
9. **version / carrier stop line**：若现有 private values 或 Coverage 0.1 vocabulary 无法表达，何时必须停下来审查最小
   successor/Schema，而不是在 runtime 暗加字段。

这些问题目前没有预选类名、字段、receipt、ledger 或 persistence route。

## 7. 最小资格否定矩阵

| ID | 单变量 world | 必须拒绝的结论 |
| --- | --- | --- |
| `FCH-000` | Fact IDs 相同，all complete 与 optional failure 的 responsibility history 不同 | Fact content identity 证明 all Providers fulfilled |
| `FCH-001` | zero denominator 与 all rejected 都没有 FactSet/continuation | empty output 足以证明同一种 closed-empty history |
| `FCH-002` | U 有 3 slots，只有 2 个可表示 Fact IDs | expected/actual Fact IDs 定义完整 denominator |
| `FCH-003` | U/E 完整，required Provider failure，FactSet 缺失 | universe 可复算等于 execution fulfilled |
| `FCH-004` | caller 提交正确 closure bytes/digest，但不持有 owned closure | digest knowledge 等于 handoff authority |
| `FCH-005` | fresh equal-limits context 或 foreign consumer attempt | semantic equality 继承 live continuation |
| `FCH-006` | Coverage assembler 只收到 FactSet 与 context | downstream 可自行补回 Provider/negative history |
| `FCH-007` | Schema-valid FACT stage 用 output members 作 denominator | schema/digest/集合方程证明 authoritative stage history |

本文实际运行 `FCH-000..003` 的六个 world，并从 current method surface 直接观察 `FCH-006`；`FCH-004/005/007`
是后继合同必须固化的 falsifier，不冒充本轮已运行测试。

## 8. Witness 与稳定性

六个 world 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四个 fresh cells 中均 PASS。去除 fresh attempt-derived
provenance identity 后，四份 semantic report 各 20,353 bytes，逐字节一致，SHA-256：

```text
14110c2180d6067ed9f0d8d74aba1c8f82f944d140db15233c7bc6c1c82c212a
```

current `test_fact_fulfillment.py` 四格各报告 28 项、实际通过 27、跳过 1；跳过的是需要显式 reference runtime/Windows
环境的 actual-child witness，不能写成 28 项全部实际通过。其余 tests 均 OK。audit semantic report 与 test logs 的
exact SHA、七份 frozen source bytes 和 setup history 由 repo 外 qualification record 绑定；它们是本候选 local witness，
不冒充 installed-product readback。

首个 audit attempt 错读不存在的 `parse_partition.eligible`；第二个 fresh attempt 错把
`provider_descriptor` 放在 request root。两者均为 audit fixture shape error，stdout/stderr 原样保留。第三个诊断虽 PASS，
但含 fresh attempt-derived IDs，不能作为四格 byte oracle；后继 qualification 才改为比较 semantic IDs 与 provenance
cardinality。外层 test batch wait timeout、被文件锁阻止的重复启动、managed-worktree/path/source-search setup errors
同样保留，均未修改产品、预算、oracle 或 frozen bytes。

## 9. 当前允许与禁止

本文候选最多发布：

```text
Fact fulfillment frozen upstream is sufficient for a handoff contract audit
current Fact continuation is not that handoff
Fact → Coverage handoff contract is still NOT_STARTED
seven-stage Coverage qualification remains NOT_STARTED
```

继续禁止：

```text
Fact → Coverage handoff runtime
ReviewSliceSet / CoverageLedger runtime or contract
zero-member FactSet / Fact-stage closure invention
public Schema / carrier / Evidence / Manifest / publisher / Bundle
persistence Route A/B selection
Relation / Slice public assembler
CLI / Workbench / Core / CLAIM_FIDELITY / tag / Release
```

Fact contract与 implementation 均不重开。真实反例若击穿 frozen conclusion，必须显式 reopen/version 最小边界；不能用
本审计的后继需求倒写上游违约。

## 10. 本候选自己的资格门

tracked scope 只允许 README、AGENTS、milestones 与本文。doc252–257、runtime、tests、workflows、Schema、Profile、
Policy、fixtures、identity vectors 与架构资产保持基线字节。

final bytes 的 local docs/Schema gates 在 CPython 3.10.6 / 3.13.13 normal / `-O` 四格各运行 13 项并全部
PASS；candidate scope/UTF-8/LF/fence/heading/marker/frozen-byte validator 与 read-only hygiene 四格均 PASS。
本结果不替代 original PR 或 exact-main 完整 CI，也不把 skipped actual-child witness 补算成通过。

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / doc258 / milestones installed-product observations
    -> independent Core, source-byte and retained-history reconciliation
    -> qualified current-state audit history
    -> return CONTROL LOOP
```

最后门闭合前只有 `CURRENT_STATE_AUDIT_CANDIDATE`。闭合后也不自动创建 handoff contract；必须重新绑定新 exact
main，并检查本 seam 是否仍是最小合法问题。formal non-success 保留原身份，数量从 history 机械导出；diagnostic 不替代
正式产品路径，本地 checkout/hygiene 只是 housekeeping。
