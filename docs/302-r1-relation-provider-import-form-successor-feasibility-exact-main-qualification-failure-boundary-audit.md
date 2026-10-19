# R1 Relation Provider successor feasibility exact-main 资格失败边界审计

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_FEASIBILITY_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE`。
>
> 坐标：`main@bd0cb9838545de0dd3a2e26486c6fa90df765962`，tree
> `a651589a7879c213a0e54f035e442e1780263074`。
>
> 受审对象：[文档 301](301-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-audit.md)
> 的 exact-main qualification failure。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结失败身份、资格影响与后继恢复边界；不修改
> Browser 分类、timeout、required Starter lane、workflow、runtime、tests、fixtures、Schema、Provider、Policy、Profile、
> manifest、persistence、Coverage 或 public Review 产品，也不把失败候选升级为 qualified history。

## 1. CONTROL LOOP 触发事实

文档 301 的 docs-only candidate 由 PR #346 final head
`df6955d59a485027fbc2429090d35d43b52ca3ed` 从 base
`68e6fa0245161dd75b9d7750d3320158bebfa315` 提交；candidate tree为
`a651589a7879c213a0e54f035e442e1780263074`。original Public CI `39317208755` attempt 1 为 11/11
SUCCESS，随后 protected merge 形成：

```text
merge = bd0cb9838545de0dd3a2e26486c6fa90df765962
tree  = a651589a7879c213a0e54f035e442e1780263074
parents = 68e6fa0245161dd75b9d7750d3320158bebfa315
          df6955d59a485027fbc2429090d35d43b52ca3ed
```

new exact-main Browser Smoke `39321768185` attempt 1 为 1/1 SUCCESS；new exact-main Public CI
`39321768248` attempt 1 为 10/11，required `Starter PASS/FAIL golden path` job `118308355830` FAIL。该 run
没有 rerun，也不能用 original PR SUCCESS 或 Browser Smoke SUCCESS替代。

因此文档 301 §12 声明的资格链在 exact-main Public CI 处终止。README/doc301/milestones fresh installed-product
readback没有启动，independent reconciliation没有启动，`FEASIBILITY_AUDITED`没有生效。

## 2. 失败 Artifact 的直接事实

failed-evidence Artifact：

```text
name = starter-single-webapp-s1-failure-39321768248-1
artifact id = 12221668728
archive SHA256 = 9a4975a882784ca91266c21a2a27ded4cc6232b3f5b4cdfabb57596db8c1fa1c
```

Artifact 与 failed job log 给出的直接事实是：

- desktop viewport完成全部声明步骤；
- mobile viewport的首个loopback document请求报告精确 raw failure
  `net::ERR_NO_BUFFER_SPACE`；
-产品按冻结规则将其映射为 `network:mobile / HostSocketNoBufferSpace`；
- Browser capture以`capture_complete=false`、`all_steps_passed=false`终结；
- Browser与bootstrap cleanup均完成，bootstrap以`COLLECTOR_ERROR / ERROR`终结；
- failed assertions对应capture incomplete、all steps not passed、1个failed request与1/2 screenshots。

这些事实只支持：required product collection在该 exact attempt中未完成，而且既有分类器正确保留了精确host/client collector
failure。它们不支持把失败改名为 Subject failure，也不支持断言某个更具体的socket、端口、内存或runner资源根因。

```text
exact underlying host resource cause = UNKNOWN
subject failure                       = NOT_ESTABLISHED
doc-only candidate regression         = NOT_ESTABLISHED
product classification defect         = NOT_OBSERVED
```

## 3. qualification failure 与 semantic defect 分离

该失败足以否定本 candidate 的 exact-main资格，但不足以推翻文档 301 的read-only feasibility witness或文档 299的frozen
contract。必须同时保留两组不同结论：

```text
semantic audit result
    candidate bytes提出的bounded successor在声明world中未观察到阻断

qualification result
    merged candidate没有通过自己预注册的exact-main required gates
```

前者不能覆盖后者；后者也不能在没有新证据时被扩大成Provider算法、Fact truth、Relation semantics或Browser分类的缺陷。
绿色的original PR run只属于PR head world，不能穿过失败的merge attempt取得exact-main authority。

## 4. 冻结的 HostSocketNoBufferSpace 边界没有被击穿

[文档 221](221-m10-browser-host-socket-release-consumer-boundary-audit.md)至
[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)以及
[文档 240](240-m10-required-starter-lane-migration-qualification-publication.md)已经冻结以下分层：

```text
raw Network failure
    -> exact private classification
    -> collector failure identity
    -> required lane qualification effect
```

本次产品恰好遵守该分层：raw bytes仍是`net::ERR_NO_BUFFER_SPACE`，private classification恰好是
`HostSocketNoBufferSpace`，Subject没有被误归因，cleanup没有被省略，required lane也没有被静默放宽。因此当前证据没有资格重开：

- exact matcher或private error type；
- Browser/Bootstrap stop category；
- required Starter lane、job name或success condition；
- timeout、retry、screenshot count或cleanup oracle；
- public Core/Starter release identity。

修改这些边界只会让失败更容易消失，不会证明文档 301 的candidate曾在原合同下通过。

## 5. 禁止的伪恢复

以下动作均不能产生文档 301 的资格：

```text
rerun Public CI 39321768248
retry until PASS
提交空提交或无语义状态抖动后借用新绿灯
删除/降级required Starter lane
增加timeout或放宽capture/assertion
把collector failure改名为Subject failure
用original PR 11/11替代exact-main 10/11
在双门未闭合时启动installed-product readback
把后继candidate PASS回填成旧candidate PASS
```

失败 run、job、Artifact、raw log、classification与`UNKNOWN`根因必须保持原 identity。任何后继成功只能建立新 candidate 的
资格，不能重写`bd0cb983…`世界。

## 6. 最小合法 qualification-recovery seam

当前最小合法问题不是“怎样让同一检查再跑一次”，而是：

> 在不改 required product oracle、不伪造根因、也不借用旧绿灯的前提下，怎样让后继 feasibility candidate 对失败历史承担
> 明确责任并取得自己的完整资格？

答案必须是一份新的、可区分的candidate，而不是重放文档 301。它至少需要：

1. 绑定新的 exact base/head/tree 与新 original-PR attempt；
2. 明确枚举并保留本次 exact-main failure及其Artifact identity；
3. 说明相对于失败candidate新增了什么可审查的工程事实或资格责任，禁止空提交；
4. 保持文档299、300与既有runtime/tests/workflow/oracle字节，除非新证据先合法重开其最小边界；
5. 从头通过original PR、protected merge、new exact-main双门、fresh installed-product readback与independent reconciliation；
6. 即使取得资格，也只成为新的feasibility history，不自动取得implementation authority。

本文不预先指定新candidate的文档号、类名或实现形状。后继CONTROL LOOP必须从当时exact main复核是否存在足够的新事实；如果只有
“平台这次也许会正常”，合法结果仍是`UNKNOWN / NO QUALIFICATION CANDIDATE`，而不是重试。

## 7. 当前状态与 authority ceiling

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_CANDIDATE_MERGED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_EXACT_MAIN_PUBLIC_CI_FAILED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_NOT_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED

R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

历史`ALLOWED`、frozen contract与audit witness均不被改写；但它们不能被当前失败candidate消费。本文也不授予corrected successor、
旧composition恢复、manifest、persistence、Coverage、public Review或R2–R6施工权。

## 8. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/302-r1-relation-provider-import-form-successor-feasibility-exact-main-qualification-failure-boundary-audit.md
docs/milestones.md
```

文档301、runtime、tests、workflows、Schema、Provider、fixtures、Profile、Policy、manifest、persistence与post-R1计划必须保持
`bd0cb983…` base bytes。final bytes至少完成四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required
markers、上游byte continuity、`git diff --check`与read-only hygiene。失败Artifact只用于复算身份和分层，不作为新产品PASS。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required gates
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure reconciliation
    -> FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是failure-boundary audit candidate。闭合后也只允许返回CONTROL LOOP，判断是否存在一份具有新事实与新
责任的feasibility successor candidate；不得自动重试文档301、启动runtime、恢复composition或进入后续阶段。
