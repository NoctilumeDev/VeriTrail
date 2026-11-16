# R1 M10 repeatability failure-observation correction 0.1 authorization publication

日期：2026-11-16

> 候选状态：`R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_AUTHORIZATION_PUBLICATION_0_1_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@c76fc0dd71de281b21a4486bd68b2aebd3375c70`，tree
> `8c0422d4c888659516d652d8c240401bf3dffce5`。
>
> 上游：[repeatability exact-main failure-boundary audit](421-r1-m10-repeatability-exact-main-failure-boundary-audit.md)与
> [failure-observation feasibility audit](422-r1-m10-repeatability-failure-observation-feasibility-audit.md)。
>
> 影响：`L0_DOCUMENTATION / VERSIONED_TEST_PROOF_FACILITY_AUTHORITY_PUBLICATION_ONLY`。本文只条件化发布
> bounded test-only correction authority；不修改runtime、tests、fixture、Browser collector、timeout、retry、workflow、Schema、
> Verdict、doc420、carrier、Manifest、persistence、public Review或R2–R6。本文自己的完整资格链闭合以前，
> `R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED`不生效。

## 1. publication输入已经取得资格

PR #484把doc422 candidate

```text
base = 5b15c715f6da16153a37025d5477bcf53b4b4c8c
head = c4bdd43aa6afc2507c8ba7e85c17780855e88e7e
tree = 8c0422d4c888659516d652d8c240401bf3dffce5
```

精确合入`main@c76fc0dd71de281b21a4486bd68b2aebd3375c70`。original Public CI `43803646543`、exact-main
Public CI `43806889221`与Browser Smoke `43806889217`均为attempt 1 SUCCESS，分别15/15、15/15与1/1；没有rerun。

fresh detached exact-main world只认`c76fc0d… / 8c0422d…`。README、doc421与doc422各自唯一Render diagnostic为
`COMPLETE`，各自唯一formal为`COMPLETE / PASS`；AGENTS与milestones各自唯一anonymous raw/Contents API/exact-Git
全字节一致PASS。reset前anonymous rate diagnostic #1观察到`remaining=0`，没有启动已知不可用的preflight或readback；reset后
diagnostic #2与preflight #1才分别观察到`remaining=55`与HTTP 200。independent reconciliation、125-artifact finite closeout、
expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
ef88665edccb4066afd1ccddb41f61c77c3d7313360839ba7c50f62758112602
f50f9b65d509514d7e9eff8944484ee0be1748918b719fef0673446a17c5ff59
e896da496bc07224469fd9144c1e021f12d1ac3f2a06bc53832e25b80eb21376
2e44bcb2f4b2fc48616df8c086731f8644143eb48a501a89a9cf1c9aa043b083
```

doc422 full-file SHA-256为
`8eff5d8f9e1c76fb067187c2a715f10aa5d6f5f8854d28cdcf2e80ed78f35472`。因此doc422现在是
`M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDITED / QUALIFIED_HISTORY`；doc421继续是qualified history，doc420、
run `43783429314`与lower cause `UNKNOWN`仍保持原identity。该事实只解除本authorization publication的阶段阻断；correction仍为
`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 原工程问题、当前证明义务与适用世界

```text
original engineering problem
    future Review derivation Manifest需要same-attempt DerivationEvidence与
    private copy-owned exact snapshot carrier边界

current proof obligation
    只发布doc422 qualified feasibility允许的versioned test-only correction authority；
    不把授权、测试或未来diagnostic解释为old failure根因、runtime修复或原工程问题解决

applicability world
    exact main c76fc0d source + qualified doc421/doc422 history
    + retained PR #481 exact-main failure and UNKNOWN lower cause

proof_is_not_problem_solving  = true
local_not_global              = true
post_r1_global_check_required = true
```

授权只是允许在下面的窄边界内施工。它不证明correction已经存在、下次failure一定出现、old attempt可以事后补证、完整R1
composition已经正确，或最终用户目标已经完成。

## 3. 授权对象是test-only correction 0.1 A–J

本文最后门闭合、返回CONTROL LOOP且前提仍成立以后，唯一允许的施工scope如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 只修改`tests/test_bootstrap_run_cli.py`中的private test proof facility；不得修改`src/`、public Schema/export或workflow。 |
| B | 在`test_same_sealed_authorities_repeat_without_residual_contamination`原exact-set assertion以前，透明包住导入到`veritrail.cli.run_bootstrap_bundle`的symbol且每个original run只包一次。 |
| C | original返回时保存同一个`BootstrapPublicRunResult`的bounded projection并返回同一对象；original抛异常时保存test-boundary exception type/message并重抛同一异常。 |
| D | projection只允许携带public execution/verdict、observed lifecycle event/node result、resource/subject completion、workspace release、Browser Evidence completion/error type与既有Browser private exception trace。 |
| E | projection必须确定性、有界、可安全格式化；不得新增runtime字段、回读临时目录、外部文件、clock、network或第二次产品执行。 |
| F | projection只进入失败assertion diagnostics；不得改变exact expected set、branch、status、Verdict、cleanup要求、测试成功条件或原异常控制流。 |
| G | controlled witnesses分别覆盖success透明、Browser private exception、Browser formed failure facts与resource sampling incomplete，并证明同一result/exception保持不变。 |
| H | 既有真实Chromium subject-drift witness与repeatability witness必须保留；synthetic witness不能替代、skip、缩小或重分类它们。 |
| I | wrapper重复调用、foreign result、result/exception替换、无界projection、post-attempt reread或diagnostic自身失败必须fail closed，不能变成PASS或retry。 |
| J | 运行CPython 3.10.6/3.13.13 × normal/`-O` focused/full regression、compile、global/local hygiene、scope与primary audit continuity，并形成独立test-only implementation candidate。 |

class、helper名与局部字段布局由后继candidate决定，但不得把test expected value变成product authority。`BootstrapPublicRunResult.observed`
只提供同一attempt已经存在的事实；test projection可以改善失败可诊断性，不能创造未观察事实。

## 4. authority ceiling

本文最后门闭合后只允许：

```text
实现 test-only correction 0.1 A–J
+ 增加同文件bounded controlled witnesses
+ 保留并运行真实repeatability / subject-drift witnesses
+ 形成独立test-only implementation candidate
```

它不允许：

```text
修改runtime、CLI payload、Browser collector、resource monitor或lifecycle语义
增加timeout、retry、rerun、skip、subset assertion或workflow relaxation
把old run 43783429314归因为Browser、resource、service、runner或environment
回填doc420资格、重建doc415/carrier、恢复global composition authority
启动public Review、language-support persistence、R2–R6、tag或Release
```

`...CORRECTION_0_1_ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。后继patch必须
拥有新的source、branch、candidate head/tree、original PR门、protected merge、exact-main双门、fresh installed-product readback与
independent reconciliation。

## 5. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止：

1. 保存lower facts必须修改`src/`、public payload、Schema、runtime event或Collector；
2. wrapper不能保证original result identity、exception identity或exactly-once调用；
3. deterministic projection必须读取attempt结束后的临时目录、clock、network、log或其他外部状态；
4. assertion只有放宽expected set、改变status/Verdict、增加timeout/retry/rerun或skip才能通过；
5. synthetic witness必须替代真实Chromium或repeatability witness；
6. old failure只能通过猜测、拼接different attempts/worlds或删除`UNKNOWN`才能获得解释；
7. correction需要创建manifest/carrier、修改doc420或消费尚未恢复的global composition authority；
8. four-grid/full regression暴露真实反例，而不是proof-facility setup error。

理论遇到反例先检查前提、适用域和模型；不得通过不断增加例外保护一个已经失效的局部理论。

## 6. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/423-r1-m10-repeatability-failure-observation-correction-authorization-publication.md
docs/milestones.md
```

doc420–422、`docs/project-state.md`、runtime、tests、workflows、fixtures、Schema、Provider、Collector、oracle、Verdict与全部frozen semantic
bytes必须保持`c76fc0d…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required
markers、`git diff --check`、global/local hygiene、doc421/doc422/project-state full-file SHA、PR #484 original/exact-main gates、fresh
readback histories、retained failure、independent reconciliation、finite closeout/integrity与primary `audit.json` continuity。focused matrix与
doc422 controlled probe只作witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original creation-event Public CI 15/15, attempt 1, no rerun
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc421 / doc422 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> finite closeout and integrity
    -> R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED becomes effective
    -> return CONTROL LOOP
```

产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用`http://127.0.0.1:7897`。任何non-success
保留原identity；不得rerun洗白、重复已有PASS或拼接不同world。PR title、body与base metadata必须在创建前完成，original creation gate
终态前禁止edit。

## 7. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_PROOF_FACILITY_CORRECTION_PR481_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_M10_REPEATABILITY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_AUTHORIZATION_PUBLICATION_0_1_CANDIDATE_NOT_QUALIFIED
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_NOT_STARTED_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_ALLOWED`变成当前事实，同时保持
`...CORRECTION_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内开始新的test-only implementation
candidate；不得把authority publication、doc422 probe或绿色CI算作correction已经存在。

`proof_is_not_problem_solving = true`，`local_not_global = true`；R1结束后的human+AI全项目检查继续是独立义务。
