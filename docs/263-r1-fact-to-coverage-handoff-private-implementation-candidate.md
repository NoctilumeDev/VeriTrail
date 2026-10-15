# R1 Fact → Coverage same-attempt handoff 私有实现候选

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_CANDIDATE`。
>
> 施工基线：`main@a174ee739a39a8dda956ff9a8ea899c569a78cf3`。
>
> 本文认领 doc262 A–J 的 bounded private implementation；不发布 exact-main verified / frozen，不建立 Coverage 语义。

## 1. CONTROL LOOP 与当前授权

[最小合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)、
[合同冻结发布](260-r1-fact-to-coverage-handoff-contract-freeze-publication.md)与
[私有实现可行性审计](261-r1-fact-to-coverage-handoff-private-implementation-feasibility-audit.md)保持原字节。
[授权发布](262-r1-fact-to-coverage-handoff-private-implementation-authorization-publication.md)由 PR #302 final head
`8582a5e2d0d2261f18ce746f470211159120a13e` 合入本基线；final original Public CI `38657864511` attempt 1
为 11/11 SUCCESS，较早的 concurrency-cancelled run `38657826171` 保留原身份。exact-main Public CI
`38660718150` attempt 1 为 11/11 SUCCESS，Browser Smoke `38660717996` attempt 1 为 1/1 SUCCESS。

四份 fresh README/doc261/doc262/milestones installed-product observations 分别取得 qualifying PASS，两个 formal ERROR
保持原 identity；independent reconciliation
`e5f41ff354a491d7927703d16d021e0add5ddcb3f7bb1519dbf58e15668fd269` PASS，216-artifact closeout 为
`a69cf12295b3018042e100321a9c6f1305ef5fec7a14973907d89272c96d3009`。因此 `ALLOWED` 已生效。

fresh CONTROL LOOP 重新核对 remote main、基线、并行 PR、frozen docs、source 与 retained counterexamples；没有发现更早
blocker，A–J 仍是最小合法施工面。该判断不是由文档编号或绿色 CI 自动推出。

## 2. 私有实现与 authority topology

新增 private function `r1-fact-to-coverage-handoff/0.1` 与固定 application-owned consumer
`veritrail-review-private-coverage-composition/0.1`。入口只接受 exact `OwnedProductFactClosure`；serialized bytes、digest、
FactSet、foreign equal world 或 caller-supplied consumer identity 均不能领取 live handoff。

```text
exact owned Fact parent / closure / history
    -> claim-time full revalidation
    -> one closure-level mutually-exclusive source claim
    -> total Fact-stage semantic projection
    -> copy-owned private handoff value
    -> fixed future Coverage-composition consumer boundary
```

handoff 与 legacy FactSet-only continuation 共用同一个 one-shot source state。任一合法 winner 取得 source 后，另一路只能失败；
validation failure、replay、fresh equal-limits Context、late budget stop、foreign history 或 source mutation不能恢复或复制 authority。
handoff value保留 original `BudgetContext` 对象并在每次读取时检查其 live state；它没有重新执行 Parse/Provider、读取仓库、
修改上游 history 或发布 Coverage 的能力。

## 3. A–J 实现对应

| 阶段 | 本候选实际机制 |
| --- | --- |
| A | 重新绑定并核验 exact Fact parent、closure、DerivationInputSet、Language Support classification、Parse product set、Fact projection、child history 与 original BudgetContext |
| B | `r1-fact-to-coverage-handoff/0.1` 对全部 safe branches 建立 total semantic projection |
| C | Parse partition、完整 U/E/blockers、Provider descriptor/requiredness/history 与 observations 使用 application-owned canonical ordering |
| D | normal fulfilled、optional gap、zero denominator、all rejected、projection blocked 与 required Provider non-success 保持不同 branch；unsafe/interrupted 没有 claim |
| E | handoff 与 legacy continuation 在 closure 上共享互斥 one-shot source；竞争 loser 不获得第二份 authority |
| F | consumer identity 固定在 private application code，caller 无参数可改 |
| G | handoff bytes canonical、copy-owned；public surface 只有只读 `document_copy()`，没有 rerun、loader、stage 或 publication method |
| H | release failed / interrupted history fail closed；已完成 partial prefix 不能包装成 safe handoff |
| I | original attempt/context、late stop、foreign equal world、replay、source mutation 与并发竞争均有直接 hardening |
| J | FCHC-000..011 与 replay/source-mutation falsifier，外加 unchanged Fact/Parse upstream 和 Coverage Schema regressions |

safe-negative handoff 只保存 Fact-stage history。zero denominator / all rejected 没有 child、FactSet 或 Coverage item；projection
blocked 保留完整 constructible U、representable E 与 blocker；required failure 保留完整 responsibility 和实际 non-success history。
unrepresentable U slot不会被伪造成 `FACT.item_id`、任意 digest 或现有 Coverage reason。

## 4. semantic projection 与 proof strength

每份 started Provider history 保留 exact request、execution、terminal、terminal frame 与 canonical Fact bytes；not-started responsibility
保留显式 `NOT_STARTED`。跨 runtime 比较不把 nonce-bound claim/run/attempt identity或 monotonic clock要求为相同，而是独立断言
exact observation bytes存在，再比较去 provenance 的 semantic projection。

六个固定世界为：normal、optional gap、zero denominator、all rejected、projection blocked、required failure。CPython 3.10.6 / 3.13.13
normal / `-O` 四格得到相同 canonical semantics，common SHA256 为
`182a1b233f5bdc4df3638b1e38c5ab38724931768f3c0999398cb15d25fa3a49`。

这只证明 bounded private handoff 在该 corpus 与 frozen upstream semantics 下稳定，不证明 public Coverage item mapping、
FACT_DERIVATION status、seven-stage join、persistence 或任意第三方 consumer 安全性。测试是 witness，不是 authority。

## 5. 首败与 retained history

首个 targeted attempt 为 12 reported / 10 passed / 2 failed：

1. FCHC-000 错把含独立 Provider provenance 的完整 FactSet bytes 当作跨 world semantic equality，归为
   `TEST_ASSERTION_TARGET_SETUP_ERROR`；修正为比较去 provenance 的 Fact semantics，不改产品 Fact identity。
2. FCHC-009 的初始实现把 reconciliation caller order误当 canonical Provider order，归为
   `NEW_PRIVATE_IMPLEMENTATION_DEFECT`；改为按 binding identity验证完整成员、按 frozen binding order投影。

该 attempt 的 source patch与失败记录保留；记录 SHA256 为
`bf05fedffb0287892c9147c48b8db10e6b377b5012d660482048529db929a931`。

后继 hardening 又发现两项独立问题：竞争 loser在 source 已被另一 claimant合法领取后错误撤销 parent，归为
`NEW_PRIVATE_IMPLEMENTATION_DEFECT`；`copy.deepcopy(bytes)` 返回同一 immutable bytes对象，未真正构造 mutation，归为
`TEST_MUTATION_SETUP_ERROR`。原 source/failure record 保留，SHA256 为
`8607f4ed2cee51da1cec49bb1d73abe7ecc709e52b90eb186cef8009b6a98557`。修正后 loser只失去自己的 claim，不能撤销 winner；
mutation witness改为经 `bytearray` 构造不同 bytes identity。

final-byte完整Review Attention 3.10 normal attempt 1为513 reported / 510 passed / 1 skipped / 2 errors；两个错误均来自
既有Slice H falsifier在full discovery中的`CONTINUATION_UNAVAILABLE`。fresh单测2/2与完整Slice join模块85/85均PASS，
handoff targeted 12/12 PASS；当前最窄身份是
`FULL_DISCOVERY_CROSS_MODULE_CONTINUATION_UNAVAILABLE / ROOT_CAUSE_UNKNOWN`，不归为handoff产品或合同失败，也不称为
flaky。原513项日志与source patch保留。未改oracle、timeout或测试顺序的fresh full attempt 2通过。

最终文档字节的31项窄回归首次从插件目录调用仓库级测试，四格均在discovery阶段以`ModuleNotFoundError`停止；该次归为
`TEST_INVOCATION_WORKDIR_SETUP_ERROR`，没有执行产品断言。原四格日志保留。fresh attempt 2从仓库根绑定Core与插件`src`后，
四格各31/31 PASS；后继PASS不改写首个setup failure。

后来的 PASS 不覆盖以上身份，也不重写 doc259–262 或上游 Fact 历史。

## 6. 本地验证

最终 private source的 targeted handoff suite四格各为 12/12 PASS。handoff + Fact fulfillment + Parse→Fact consumer + Parse
fulfillment 的上游组合四格各为 95 reported；3.10 normal / `-O` 各 94 passed / 1 skipped，3.13 normal / `-O`
各 95 passed / 0 skipped。skip只表示 exact reference runtime所在格不重复启动同一 reference witness。

完整 Review Attention 回归四格各为 513 reported：

| Cell | Result | Duration |
| --- | --- | --- |
| CPython 3.10.6 normal, fresh attempt 2 | 512 passed / 1 skipped | 697.294 s |
| CPython 3.10.6 `-O` | 512 passed / 1 skipped | 673.993 s |
| CPython 3.13.13 normal | 513 passed / 0 skipped | 643.926 s |
| CPython 3.13.13 `-O` | 513 passed / 0 skipped | 642.023 s |

Coverage Schema 22项、Markdown 4项与 hygiene 5项组成的31项窄回归在fresh attempt 2四格均 PASS；private boundary、compile、
public-export absence、forbidden Coverage/persistence surface、relative links、UTF-8/LF/final LF、`git diff --check` 与只读
hygiene仍须针对最终 PR bytes重核。所有原始日志与 matrix artifacts留在仓库外 qualification root，不进入产品包。

## 7. 本候选自己的资格门

最终 bytes必须完成 final local gates、original PR required checks、单独批准 exact-head protected merge、新 exact-main Public CI +
Browser Smoke、fresh installed-product README/本文/milestones observations与 independent Core/source-byte/Bundle/retained-history
reconciliation。formal non-success保留原 identity，后继 PASS不覆盖；每个 observation只属于同一个 implementation world。

这些门闭合最多建立 `IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED` 的 source/readback qualification。`FROZEN` 仍须独立
implementation fact publication及其自己的完整资格链。本地 checkout alignment与清理只是 housekeeping，不追加语义门。

## 8. 当前状态与停止线

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本候选不是 merged、exact-main verified 或 frozen。禁止选择 persistence Route A/B、定义 Coverage item identity/disposition、
FACT_DERIVATION stage status、seven-stage join、ReviewSliceSet/CoverageLedger、public Schema/carrier、Evidence/Manifest/Bundle/
publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag或Release。若反例要求这些能力，必须保留现场并只重开被击穿的最小边界。
