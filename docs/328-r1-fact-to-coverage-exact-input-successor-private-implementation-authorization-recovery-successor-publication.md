# R1 Fact→Coverage exact-input successor 私有实现授权恢复后继发布候选

日期：2026-10-27

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_SUCCESSOR_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@7a043e8745d76e59a0ef5a3a3c332d7aaa645e57`，tree
> `eb3785ba4c03984b2e7b25cb215e4b61015235a2`。
>
> 上游：[private implementation feasibility audit](320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)、
> [0.2 contract](321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)、
> [contract freeze publication](322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md)、
> [首次授权恢复发布](326-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-publication.md)与
> [exact-main qualification failure boundary](327-r1-fact-to-coverage-successor-authorization-recovery-exact-main-qualification-failure-boundary-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文建立一份对PR #377失败与文档327 qualified history承担新增
> 对账责任的独立publication；不修改runtime、tests、workflows、fixtures、Schema、Profile、Policy、Coverage、manifest、
> Evidence、persistence或public Review产品。本文自己的完整资格链闭合以前，`ALLOWED`不生效。

## 1. failure boundary已经取得自己的资格

首次authorization recovery publication由PR #377提交。original Public CI `40506198552` attempt 1为11/11 SUCCESS，并以
exact head `7c9ba8bf990622b19abd35d2bbad860138ced11a`合入
`main@310285aba4d2175164b53c4f68087817491df8bd`。Browser Smoke `40510081338` attempt 1为1/1 SUCCESS，
但exact-main Public CI `40510081408` attempt 1在required Starter job `122222945703`观察到desktop console
`net::ERR_NO_BUFFER_SPACE`，以10/11 FAILURE终结。

失败Artifact `12737259914`、archive SHA-256
`33ef978964918c30870010fcc56082c7e5d29edc9778c72c0147108bfa6de4bb`与分类
`6a4feec11380f4c18a2897fb2f365786f156d5b5aeac3d7042fee1ce12383430`永久保留。oracle正确拒绝该console error；
精确失败resource identity为`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，底层host resource cause为`UNKNOWN`，Subject failure与
docs-only candidate regression均未建立。该run没有rerun，文档326保持`MERGED / NOT_QUALIFIED`。

文档327随后由PR #378从该失败world建立：

```text
base  = 310285aba4d2175164b53c4f68087817491df8bd
head  = f071608639c6b3462990c7d947f1fbd7bad186b2
tree  = eb3785ba4c03984b2e7b25cb215e4b61015235a2
merge = 7a043e8745d76e59a0ef5a3a3c332d7aaa645e57
```

其original Public CI `40515795532`、exact-main Public CI `40520543941`与Browser Smoke `40520544044`均为attempt 1
SUCCESS，分别11/11、11/11与1/1。fresh anonymous installed-product README、doc326、doc327、milestones各取得唯一
qualifying PASS；README formal #1因匿名API额度耗尽以`FORMAL_READBACK_ERROR`保留，真实reset后以新Plan/session/output形成
formal #2 PASS，没有覆盖首个ERROR。四个qualifying观察的P1/P2 coverage均为`COMPLETE`，Core均为`PASS`。

independent reconciliation与159-artifact finite closeout分别为：

```text
23e7f9f32b1793f74fd3906f33f7f65119a67d489fdf0d20da21bb02f37f1612
b4018ef01507795b95918dc27aaee3f6f3266de7d8b36967fea5fe511f683281
```

因此文档327现在是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。它没有解释或回填#377，只使一份承担新失败历史与新资格责任的
successor publication成为合法候选。

## 2. 本candidate不是空提交或旧publication重放

本文相对文档326新增的不是算法功能，而是资格责任：

1. 绑定新的base/head/tree、original attempt、protected merge、exact-main gates与fresh product observation；
2. 独立复算#377 run/job/Artifact/classification、两个UNKNOWN与`MERGED / NOT_QUALIFIED`状态；
3. 独立复算PR #378双门、四个qualifying PASS、一个formal ERROR、reconciliation与closeout；
4. 保持runtime、tests、workflow、required Starter lane、Workbench console oracle与0.2合同字节不变；
5. 证明任何后继PASS只属于本文的新world，不回填#377，也不把#378 success解释成旧失败根因；
6. 全部门闭合以后才发布bounded private implementation authority，并立即返回CONTROL LOOP。

因此本文不是“平台现在也许正常”的retry载体。它把此前不存在的qualified failure history纳入自己的输入世界，并承担独立
reconciliation责任。

## 3. current exact main continuity重新复算

施工前使用audit-only identity
`r1-fact-to-coverage-exact-input-successor-implementation-authorization-recovery-successor-continuity-audit/0.1`，从clean exact
`main@7a043e8…`重新检查：

- 文档320审计的四个private source文件从feasibility baseline到当前HEAD没有字节漂移；
- 文档320–327、feasibility/contract/maintenance/failure-boundary proof facilities保持精确；
- #377失败classification、Artifact、`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与`UNKNOWN`保持原身份；
- 0.2 handoff、private consumer/carrier、five terminal worlds、three zero-Parse denominator worlds、same-object identity与shared
  one-shot falsifiers重新成立；
- Python 3.10.6 / 3.13 × normal / `-O`四格语义报告完全一致；focused suite每格99/99 PASS。

continuity qualification SHA-256为：

```text
f9c06265447dfc2adae00fe33e35827b00282b5c2f21be52278a30678b04f678
```

该审计只证明当前world仍有资格形成authorization successor candidate；它没有授予implementation authority，也没有把测试结果升级为
合同、Coverage或composition结论。

## 4. 条件化授权对象仍是bounded A–I

本文最后一门闭合后，唯一允许的private implementation scope保持文档326定义的A–I：

| 项 | 最小施工责任 |
| --- | --- |
| A | 增加冻结的0.2 handoff function、claim purpose、private consumer与private carrier identity；旧0.1 identity、bytes和入口保持不变。 |
| B | 在Fact parent内部增加parent-only terminal accessor；先完整执行既有`_handoff_source_document(closure)`验证，再在同一同步调用内原子返回source、原始`BudgetContext`与parent-bound原始`DerivationInputSet`。 |
| C | 新0.2 claim与legacy continuation、Coverage 0.1和Relation handoff共享closure级`__claimed` one-shot slot；不得创建第二个可重放claim域。 |
| D | carrier绑定原始inputs对象身份、input-state seal、三份canonical bytes、verified blob key/bytes、五个digest、live context identity与私有构造token；equal foreign reconstruction一律拒绝。 |
| E | required-provider-failure branch只消费terminal validation已证明的bound original inputs；不得调用会因parent eligibility为`REVOKED`而失败的普通live `_inputs_ref()`，更不得恢复eligibility。 |
| F | carrier每次读取都重新检查live context、deadline/stop、input seal、source/input五digest、对象图和claim token；晚到stop、reseal drift、foreign context或重放均fail closed。 |
| G | 覆盖`NORMAL_FULFILLED`、`ZERO_PARSE_DENOMINATOR`、`ALL_PARSE_REJECTED`、`PROJECTION_BLOCKED`、`REQUIRED_PROVIDER_NON_SUCCESS`五world，以及empty inventory、unsupported-only、policy-excluded-only三分母world。 |
| H | carrier只允许copy-owned SourceSnapshot、ReviewPolicy、DerivationProfile、verified blob identity/bytes、五digest、0.1 Fact终态与same-object-graph proof；不得创建Coverage obligation/item/status/ledger。 |
| I | 增加对应private tests与audit fixtures并运行四格falsifiers；旧Provider/public export/default composition、0.1 handoff、Relation路径、Schema、Profile与Policy保持不变。 |

该scope只把已经通过Fact终态验证的原始输入对象安全交给后继private consumer。它不实现Coverage producer，不选择Coverage obligation
projection，不生成manifest role，不构造same-attempt Evidence，也不授予状态完成权。

## 5. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded private exact-input successor A–I
+ 增加对应private tests / audit fixtures
+ 运行既有Fact终态验证、shared one-shot与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改public Schema、Policy/Profile、Fact truth或FactSet identity
过滤、重建或用equal foreign input替代原始DerivationInputSet
恢复parent/child eligibility或跨attempt拼接authority
创建Coverage obligation/item/status/ledger
恢复或消费旧composition authorization
实现manifest successor或same-attempt Evidence continuity
选择persistence
启动public Review、post-R1 Benchmark或R2-R6
发布tag / Release
```

`ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。implementation必须拥有自己的完整资格链；
真实反例出现时立即停止当前施工，只重开被击穿的最小边界。

## 6. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/328-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-successor-publication.md
docs/milestones.md
```

doc320–327、runtime、tests、workflows、fixtures、Schema、Profile、Policy、Coverage、manifest、Evidence、persistence与public产品必须保持
`7a043e8…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
`git diff --check`、read-only hygiene、continuity四格、99-test四格、#377 retained failure、doc327 qualified history及primary
`audit.json` continuity。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc326 / doc327 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure / qualified-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用original PR green、
相同tree、相同semantic digest或后继PASS替代任何一门。

## 7. 当前target与停止线

全部门闭合以前只能记录：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_MERGED_NOT_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_SUCCESSOR_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内建立新的private implementation
candidate；不得把authority publication本身算作实现证据。
