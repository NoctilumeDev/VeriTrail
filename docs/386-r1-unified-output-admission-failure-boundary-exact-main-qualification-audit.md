# R1 unified Review / Coverage output admission failure-boundary exact-main qualification audit

日期：2026-11-08

> 候选状态：`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_FAILURE_BOUNDARY_EXACT_MAIN_QUALIFICATION_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@e3c3281cb00f4bcef54ea9512e49d38064305fe6`，tree
> `a9488dcf7feebe158f4571cdc7778c96ef5df754`。
>
> 受审对象：[文档385](385-r1-unified-output-admission-implementation-original-gate-failure-boundary-audit.md)及PR #437的
> exact-main qualification failure。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只保存doc385自己的required gate失败、资格影响、
> `UNKNOWN`上限与最小后继责任；不修改runtime、tests、workflow、下载器、恢复预算、Release资产、selector、
> Fact/Relation/Slice/Coverage、CoverageLedger、manifest、Evidence、persistence、public Review、Core Verdict或R2–R6。

## 1. CONTROL LOOP触发事实

PR #437绑定下列docs-only candidate：

```text
base   = 5742c979e671e65067085e0303caf9d3506b7d42
head   = 997b2bfde1e3d6c9da1cb4ad3ddbab0a5a90343f
tree   = a9488dcf7feebe158f4571cdc7778c96ef5df754
scope  = AGENTS.md
         README.md
         docs/385-r1-unified-output-admission-implementation-original-gate-failure-boundary-audit.md
         docs/milestones.md
```

original Public CI `42473232190` attempt 1为11/11 SUCCESS。受保护exact-head merge形成：

```text
merge   = e3c3281cb00f4bcef54ea9512e49d38064305fe6
tree    = a9488dcf7feebe158f4571cdc7778c96ef5df754
parents = 5742c979e671e65067085e0303caf9d3506b7d42
          997b2bfde1e3d6c9da1cb4ad3ddbab0a5a90343f
```

new exact-main Browser Smoke `42475745159` attempt 1为1/1 SUCCESS；new exact-main Public CI `42475745171`
attempt 1以FAILURE终结，没有rerun。fresh installed-product readback、independent reconciliation与finite qualifying closeout没有启动。

因此doc385的资格链在new exact-main required gate处停止：

```text
doc385 publication    = MERGED / NOT_QUALIFIED
failure-boundary state = NOT_EFFECTIVE_AS_QUALIFIED_HISTORY
implementation         = NO_MAINLINE_RUNTIME_FACT
```

original PR绿灯与Browser Smoke成功都不能替代失败的exact-main Public CI；相同tree也不产生qualification继承。

## 2. required Python 3.10失败的直接事实

失败坐标：

```text
run         = 42475745171 / attempt 1
job         = Python 3.10 on Windows / 128716605284
failed step = Run Starter and Authoring Skill 0.2.0 on their declared Core 0.12.2 lane
asset       = veritrail-0.12.2-py3-none-any.whl
frozen sha  = 3a42f28db6f4ed12351dade3fbb6f57fa1d5aa3fdd6d28210492f676bc1562de
```

该job在失败以前已经完成Core normal/`-O`、Authoring Skill、GitHub Evidence与Review Attention normal/`-O`门。随后冻结
Core wheel下载依次得到三次15秒`TimeoutError`：

```text
attempt 1 -> next delay 2s / remaining budget 44.985s
attempt 2 -> next delay 4s / remaining budget 27.969s
attempt 3 -> next delay 8s / remaining budget 8.953s
terminal  -> release asset recovery budget cannot fund the next bounded retry
```

下载器以exit code 1 fail closed；wheel build、sdist、Artifact upload与后继E1步骤在该job中SKIPPED。Python 3.13同一完整lane
SUCCESS，Workbench SUCCESS，E3 0.2 release download acceptance SUCCESS；四个依赖job group因required predecessor未全部成功而
SKIPPED。这些成功上下文不能改写required run失败，也不能与另一Python lane拼接成11/11。

run JSON、failed log、failure capture与142-artifact failure closeout seal SHA-256为：

```text
2bc11476ca2fbc50f9295c893243c47d2a0691af0cdab14cb5278b94121a459d
5a440d55deabeb3da2d7d0656d5803dd055b1c8c172133557dffd04542180290
41ba940d0870b6015d630f033aac6e6c31559f90b90e759457adf78be74987dd
7e7f1388f64f487248efe93678826a5ae5510a2337974c100390640048a2489a
```

两个GitHub API EOF、closeout Python path、capture boolean与closeout schema proof-facility setup errors均按原identity保留，effect
`NON_QUALIFYING_NONE`。

## 3. 归层、资格与工程问题分离

当前证据只允许：

```text
required exact-main gate failure                    ESTABLISHED
classification                                      RELEASE_ASSET_TIMEOUT_RECOVERY_BUDGET_EXHAUSTED
download tool fail-closed behavior                  CONFORMING
asset digest mismatch                               NOT_OBSERVED
doc385 semantic contradiction                       NOT_ESTABLISHED
docs-only candidate regression                      NOT_ESTABLISHED
subject failure                                     NOT_ESTABLISHED
workflow/runtime/test/oracle defect                  NOT_ESTABLISHED
underlying GitHub/proxy/shared-egress/network cause UNKNOWN
```

PR #437只改四份文档，original head的同一required lane通过，exact-main Python 3.13、Workbench与E3 lanes也通过。这些事实使
candidate regression与Subject failure保持`NOT_ESTABLISHED`，却不能产生docs-only exemption或把doc385升级为qualified history。

doc385对PR #436的`HTTP 504`失败归层内容没有被本次`TimeoutError`反例推翻；被击穿的是doc385自己预注册的资格链。两次失败拥有
不同candidate、attempt、status observation与world，必须并列保留，不能合并成一个“网络已知根因”。

`proof_is_not_problem_solving = true`：形式上写对失败边界，不等于该边界已经资格化；资格化失败边界也不等于application runtime
已经解决原工程问题。

## 4. frozen download oracle没有被击穿

[冻结恢复策略](98-release-download-recovery-correction.md)与
[multi-asset lane修正](357-release-download-multi-asset-lane-budget-correction.md)要求有限deadline、窄重试集合、owned partial清理与摘要
相等后发布。本run没有观察到错误字节被接受、digest mismatch被忽略、partial被发布、deadline失效或required gate被绕过。

因此本次failure不授权：

```text
扩大60/120秒预算
无限重试或retry-until-PASS
删除或降级required lane
改写Release URL、asset name或frozen digest
把另一lane的PASS借给失败lane
把TimeoutError命名成已证明的GitHub、代理或网络根因
```

后继时间点若成功，只能证明自己的新world跨过同一门，不能解释或回填run `42475745171`。

## 5. 最小合法recovery seam

当前最小合法问题是：

> 怎样先让doc385自己的exact-main qualification failure成为有界、可复算的qualified history，再从新exact main机械重建
> application output admission implementation candidate？

恢复必须串行：

1. 本docs-only审计先取得自己的local、original PR、protected merge、new exact-main双门、fresh readback与independent
   reconciliation，只把#437失败identity、qualification effect与authority ceiling升级为qualified history；
2. 如果本审计的unchanged required lane完成，只证明恢复无需弱化门，不解释也不回填#437；
3. publication形成新事实后返回CONTROL LOOP，复核冻结合同、authorization、当前runtime source与两个保留失败world；
4. 只有没有新的runtime/test/oracle反例时，才从新的exact main重建implementation candidate final bytes，取得新base/head/tree、
   新local witness与新original/exact-main/readback/reconciliation资格；
5. 如果本审计自己的required lane再次失败，保留新identity并重新判断最小proof-facility/environment边界，不把重复失败当作
   弱化oracle的理由。

本文不预先授权runtime maintenance、download-budget correction、manifest、same-attempt Evidence、persistence、public Review或
R2–R6。

## 6. 本audit自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/386-r1-unified-output-admission-failure-boundary-exact-main-qualification-audit.md
docs/milestones.md
```

doc385、runtime、tests、fixtures、workflows、download policy、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen
semantic bytes必须保持`e3c3281…` base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、
links/fences/headings、required markers、failure identity复算、`git diff --check`、global/local hygiene、focused四格与primary
`audit.json` continuity。

本候选的首轮local witness为：

- four-file Markdown/scope/frozen-byte/failure-identity/primary-audit validation PASS，855个local links，SHA-256
  `b09ce66a0e2ec774ab03e1bcdfd10d75ca9d9c34dc1d9c4d38f633412ecd40da`；
- Python 3.10.6 / 3.13.13 × normal / `-O` focused四格各259 reported / 258 passed / 1 skipped，matrix SHA-256
  `91f394c59a45e09e02ffdddbf8001ba1b07a2b05421bfe0002461bfe08c88e8b`；
- global/local hygiene 8/8 PASS，matrix SHA-256
  `0e5908890c79c7cf031274da1a2c1cb53a17e9140636e1dfbd3891754e9f4f00`。

worktree registration因本聊天累计attachment identity超过100失败，按setup error保留；它不改变Git、GitHub或产品观察面。本文加入
这些witness identity以后，final bytes仍必须重新运行相同local gates并由外部evidence seal固定，不能把pre-record bytes冒充final。

```text
final docs-only exact-main failure-boundary bytes / declared local gates
    -> original PR required gates (new attempt; no rerun of #437)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc385 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source/failure/problem-identity reconciliation
    -> finite closeout/integrity
    -> EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止，不重复已有PASS。

## 7. 当前状态与停止线

全部最后门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_CANDIDATE_PR436_CLOSED_UNMERGED_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_MERGED_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_FAILURE_BOUNDARY_EXACT_MAIN_QUALIFICATION_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。doc385继续保持
`MERGED / NOT_QUALIFIED`，#436继续保持closed/unmerged/not-qualified；两个failed attempt与lower `UNKNOWN`均不回填。随后必须返回
CONTROL LOOP，不能按文档编号自动进入runtime施工。
