# R1 Fact → Coverage same-attempt handoff 私有实现授权发布

日期：2026-10-15

> 发布基线：`main@b6268103dc838706a8d2e8c9a2d4711a7d37a4d6`，tree
> `0400e15e8056d1bd7cd3e4773072652e81cf0439`。
> 影响：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L0_DOCUMENTATION`；docs-only。
> `PRIVATE_IMPLEMENTATION_ALLOWED` 仅为条件目标，本文最后门全部闭合以前不生效；handoff runtime 仍未开始。
> persistence OPEN，ReviewSliceSet / Coverage NOT_STARTED；doc259/doc261 的既有字节保持不变。

## 1. CONTROL LOOP 与本轮 authority

[doc259](259-r1-fact-to-coverage-same-attempt-handoff-contract.md) 已由
[doc260](260-r1-fact-to-coverage-handoff-contract-freeze-publication.md) 的独立资格链冻结。
[doc261](261-r1-fact-to-coverage-handoff-private-implementation-feasibility-audit.md) 随后完成自己的 docs-only
可行性资格链；它没有自动授权 runtime。

本轮重新核对 remote exact main、主仓、本轮 detached readback、三个 unrelated Dependabot PR、current private Fact
object graph、Coverage 0.1 vocabulary 与 retained counterexamples。PR #301 只修改 README、AGENTS、milestones 与
doc261；doc259/doc260、runtime、tests、Schema、Profile、Policy 和 fixtures 没有发生语义变化。主仓仍保留用户拥有的
untracked `audit.json`，本轮不读取、覆盖或纳入提交。

没有发现击穿 doc259/doc261 前提的新证据，也没有发现必须先选择 persistence、修改 Coverage vocabulary 或建立 public
carrier 才能实现 bounded private handoff 的更早 seam。因此当前最小候选仍是 doc261 §10 的 A–J private
implementation。本文只条件化发布这项有限 authority；自己的最后门闭合以前，runtime 继续
`NOT_STARTED / NOT_AUTHORIZED`。

## 2. feasibility audit 的资格身份

[PR #301](https://github.com/NoctilumeDev/VeriTrail/pull/301) 的坐标为：

```text
base  = bf6bedb002c1a9a4ade7e64b385be742dcf012fd
head  = 03c8df45d74ffbf3990dbb851d80f6b0a25784cd
merge = b6268103dc838706a8d2e8c9a2d4711a7d37a4d6
tree  = 0400e15e8056d1bd7cd3e4773072652e81cf0439
```

一个 commit、四个文件；受审 head tree 与 merge tree 相同。原始 PR Public CI `38647492297`、exact-main Public CI
`38650640469` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38650640457` attempt 1 / 1/1 SUCCESS。
exact-main 原始日志中的 Review Attention 四格各为 `501 reported / 498 passed / 3 skipped`；skip 不算实际执行通过。

三个 fresh anonymous installed-product observations 均绑定同一个 exact main，P1/P2 COMPLETE、Core PASS：

| Target | Plan identity |
| --- | --- |
| README | `r1-fch-feasibility-formal-readme-1-b626810` |
| doc261 | `r1-fch-feasibility-formal-doc261-1-b626810` |
| milestones | `r1-fch-feasibility-formal-milestones-1-b626810` |

independent reconciliation SHA-256 为
`98860543daa467c235ce25acd69e414a0e350ca6354282fe32ead71b7e576188`；audit closeout 为
`da2ee0a7f2f12a0dc388cb207a2d89abfb604a72aee2f8f496b57f188da99640`，封存 135 份 terminal artifacts。
formal history 为 3 PASS / 0 non-success；三个 render diagnostics 与三个 setup observations 保持非资格化。正式观察前的
Plan ID prefix correction 只修正证明设施长度约束，没有修改产品 oracle、三个 target 或正式 observation identity。

因此 `R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED` 已是 qualified history。
doc261 的 candidate header 保留原字节；状态生效依据它声明的完整资格链与 retained evidence，不靠倒改历史文档。

## 3. current exact-main continuity

本轮重新取得的关键 frozen/current SHA-256 为：

```text
afc40f1226325ac97297863bc99df4f837a37b1617d1c51e5c038cc0f9f39524  doc259 contract
f81062f62a0de1a174d5f96df9ccd9c5ae7f272b55c7e9585f3cfb27140e731f  doc260 freeze publication
d2da6ab903516b2ae2ad81715e6cc4d3529b8e79c82e42e68db53cefe5b76821  doc261 feasibility audit

669411b659ac62836d0b308f008731e4f26b9df68e5cb8a9357a04f5cf1ae3d2  _fact_fulfillment.py
2c4c24d5fd1e9bf521056b3df9e9eb03f69a4ba690af13422219d2d3e46c5651  _fact_fulfillment_projection.py
e4a85d17b5701c14d5481d4fabb10ee0380d2bc201735a43408164c6b27318c0  _fact_fulfillment_binding.py
3c185099c113a18f6ba76cfd0ad3356ae5ab4bd27c3f9d4d5da6fade7a92d674  _multi_provider_fact_composition.py
e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545  review-coverage-ledger-0.1.schema.json
```

这些摘要只证明本轮 CONTROL LOOP 使用的 exact bytes。授权生效后的 implementation branch 仍须从新的 exact main
重新读取 source 与 frozen contracts；相同内容或摘要不继承 live claim、attempt 或 continuation authority。

## 4. 条件化的最小施工面

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，单用途 implementation branch 最多实现 doc261 §10 的：

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

实现必须继续满足：

1. 全部新对象、projection、claim 与 validation 留在 `veritrail_review` private；不新增 public export/SPI。
2. semantic input 只能来自 exact owned Fact parent/closure/history；不得重新读取 source、重跑 Parse/Provider、补写 expected
   answers 或从 document copy 自领 live authority。
3. handoff function identity 固定为 `r1-fact-to-coverage-handoff/0.1`；Parse partition、完整 U/E/blockers、Provider
   requiredness/lifecycle、terminal/frame/execution observations、FactSet/absence 与 whole-attempt safety state 全部保留。
4. normal 与 safe-negative 使用 handoff-specific source qualification；unsafe/interrupted 只允许 no-claim fail closed，不能把
   partial required prefix 包装成 normal source。
5. new handoff 与 legacy FactSet-only continuation 必须共享 closure-level mutually-exclusive one-shot state；成功、验证失败、
   竞争失败或 stop/revocation 不能恢复或复制 authority。
6. 必须绑定 original parent、consumer、attempt 与 `BudgetContext` 对象；fresh equal-limits Context、foreign history、digest
   equality 或 serialized bytes 不继承资格。
7. semantic value 必须 copy-owned、canonical 且无 rerun/mutation/lazy-loader 能力；caller 不能自造 consumer identity、
   denominator 或 completion claim。
8. zero denominator、all rejected、projection blocked、required failure、optional gap 与 unsafe release 保持不同 history；
   zero accepted 不产生 FactSet、Coverage item、Coverage status 或 normal continuation。
9. unrepresentable U slot 保留在 private handoff；不得伪造 `FACT.item_id`、任意 digest 或现有 Coverage reason。
10. FCHC-000..011 必须成为直接实现 falsifiers；旧 Fact fulfillment、Parse → Fact consumer 与 Coverage Schema regressions
    必须保持成立。测试只作 witness，不扩大合同。

该 authority 只允许开始 bounded private implementation，不预先证明实现正确、完成、merged、exact-main verified 或
FROZEN。

## 5. 明确不授权

```text
persistence Route A/B
public Schema / carrier / corpus
Coverage item identity / disposition mapping
FACT_DERIVATION stage status or seven-stage join
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / Bundle
CLI / Workbench / Core / other top-level tracks
CLAIM_FIDELITY
tag / Release
```

尤其：

```text
PRIVATE_IMPLEMENTATION_ALLOWED
    != implementation started
    != handoff constructed
    != Coverage authorized
    != persistence selected
    != public product published
```

若 implementation 证明 frozen boundary 无法在上述范围内成立，必须保留反例、停止施工，并只显式 reopen/version 被击穿的
最小边界；不得因为本文已授权而改写 U/E、Provider history、Budget/release semantics、旧 continuation 或 Coverage 0.1。

## 6. 本 publication 的资格门

本 publication 只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。doc259/doc260/doc261、
runtime、tests、workflows、Schema、Profile、Policy、fixtures、identity vectors 与架构资产必须保持基线字节。

final-byte local gates 至少包括：本轮人工 scope 与上游 terminal seals 重核；docs/Schema regressions；relative links；UTF-8
without BOM、LF/final LF、balanced fences、unique headings、条件 marker、禁止越权状态、敏感路径、exact diff scope、
其余 tracked bytes continuity、`git diff --check` 与只读 hygiene。实际 counts、skips、resource samples 与 outcomes 另存
qualification Artifact；本节是预先声明的门，不冒充已执行 PASS。

```text
final docs-only authorization bytes / declared local gates
    -> original PR qualification
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc261 / this publication / milestones readback
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP on current exact main
```

四个 target 各选一份 qualifying PASS，Plan/session/handoff identity 独立且全部绑定同一个 publication merge SHA。
diagnostic 不替代正式观察；全部 formal non-success 与 setup/diagnostic history 从 evidence 机械枚举，N 不写死。前一轮
PASS 不替代本轮 fresh readback，后来的 PASS 不覆盖 ERROR/FAIL/CANCELLED/UNKNOWN。

## 7. 生效前后与实现自己的门

条件化 target markers：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本文第 6 节最后门闭合以前，actual implementation authority 仍 `NOT_AUTHORIZED`；不能从已提交 marker、可行性审计、
PR CI 或相同 runtime bytes 借权开工。最后门闭合以后也只是 `ALLOWED / NOT_STARTED`；必须重新绑定新的 exact main、
复核并行事实并确认 A–J 仍是最小合法 seam，才可创建 implementation branch。

实现最终字节仍须独立取得本层声明的 local gates、original PR、protected merge、new exact-main gates、fresh product
observation、independent reconciliation 与 implementation fact publication。本文不固定后继文件布局、类名、test count、
private carrier shape 或 publication 形式，也不替后继 qualification、冻结或 Coverage 预先授权。

## 8. stop line

```text
before publication qualification:
    feasibility audit = AUDITED
    implementation authority = NOT_AUTHORIZED
    implementation = NOT_STARTED

after publication qualification:
    feasibility audit = AUDITED
    private implementation = ALLOWED
    implementation = NOT_STARTED
```

当前授权原则候选冻结为：

> The Fact-to-Coverage same-attempt handoff may enter private implementation only through doc261's bounded A–J
> successor; that authority does not establish implementation, persistence, Coverage semantics or publication.

中文：**Fact → Coverage same-attempt handoff 只能在 doc261 已审计的 A–J private successor 边界内进入实现；这项授权
不证明实现已经发生，也不建立 persistence、Coverage 语义或发布事实。**
