# R1 public project-state projection 0.8 original-gate failure-boundary audit

日期：2026-11-09

> 候选状态：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@f2ab7b78f86a057431cf5c8f4cbc3b0337338118`，tree
> `280cbc4f54427b86b81854892af8a490559fed7d`。
>
> 受审对象：PR #447及其未合入的
> `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8` candidate original-gate failure。
>
> 影响：`L0_DOCUMENTATION / ORIGINAL_PR_QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只保存#447自己的失败identity、
> qualification effect、authority ceiling与最小后继责任；不修改`docs/project-state.md`、runtime、tests、fixtures、workflow、
> download recovery tool、60/120秒预算、Release资产、Schema、Provider、Collector、P2/Core oracle、Verdict、既有frozen
> semantic bytes、manifest、Evidence、persistence、public Review或R2–R6。

## 1. CONTROL LOOP触发事实

PR #446已经把[文档390](390-r1-application-level-unified-review-coverage-output-admission-private-implementation-freeze-qualification-recovery.md)
精确合入本次base。其original Public CI `42557756555`、exact-main Public CI `42560991201`与Browser Smoke
`42560991124`均attempt 1 SUCCESS（11/11、11/11、1/1）；fresh README/doc389/doc390 Render、AGENTS/milestones raw-byte
observation、independent reconciliation与finite closeout全部成立。因此bounded application output admission private
implementation已经在自己的声明world中`FROZEN`；这项上游事实不恢复global composition authority，也不授权manifest、Evidence、
persistence、public Review或R2–R6。

fresh CONTROL LOOP随后从相同exact main建立projection 0.8 candidate：

```text
base         = f2ab7b78f86a057431cf5c8f4cbc3b0337338118
base tree    = 280cbc4f54427b86b81854892af8a490559fed7d
head         = 1e554754d43e3b2bf0d6e7780852537857399797
candidate tree = 521c75df9908a7c6d1b30836da8d4c23f22d2801
scope        = AGENTS.md
               README.md
               docs/391-r1-public-project-state-projection-successor-0.8-contract.md
               docs/milestones.md
               docs/project-state.md
```

candidate local qualification、final diff review与post-commit seal SHA-256分别为：

```text
1dfab31fa35e94c28a911d3662f608b00c38ed577afaaec99b682b7236d95069
4dd33d4784d718d9ef17fd4bc87301a9d6c9cd73f5ea6331d801e0c426891e2e
7b712e8bc87aba274fa60ca537027585c73e6470450e0c427e61706e326a495d
```

这些只证明local final bytes。PR #447 original Public CI `42568657029` attempt 1以`FAILURE`终结；没有rerun。PR已关闭、
没有合入，remote main继续是`f2ab7b78…`。fresh installed-product readback、independent reconciliation与qualifying closeout没有
启动。因此：

```text
doc391 / projection 0.8 bytes = CLOSED PR-ONLY HISTORY / NOT MAINLINE
PR #447 candidate             = CLOSED / UNMERGED / NOT_QUALIFIED / NOT_FROZEN
projection 0.7                = FROZEN CURRENT MAINLINE PROJECTION
```

相同local PASS、内容摘要或未来successor不能继承#447的original-gate qualification。

## 2. 三个required job的直接失败事实

### 2.1 E3 0.2 release download acceptance

```text
run         = 42568657029 / attempt 1
job         = E3 0.2 release download acceptance / 129000700153
failed step = Download and verify the frozen Core and E3 release assets
```

Core 0.12.0 wheel与Starter 0.2.0 wheel均已下载并通过摘要验证。随后Starter 0.2.0 sdist
`veritrail_starter-0.2.0.tar.gz`连续七次得到retryable HTTP 504；bounded backoff与请求耗时消耗120秒共享恢复预算后，下载器在预算
无法承担下一次bounded retry时fail closed。clean-install acceptance因此SKIPPED。

### 2.2 Python 3.13 on Windows

```text
run         = 42568657029 / attempt 1
job         = Python 3.13 on Windows / 129000700027
failed step = Run Starter and Authoring Skill 0.2.0 on their declared Core 0.12.2 lane
```

Core、GitHub Evidence与Review Attention的normal/`-O`测试均SUCCESS。随后冻结Core
`veritrail-0.12.2-py3-none-any.whl`连续五次得到retryable HTTP 504；60秒恢复预算不能承担下一次bounded retry，下载器fail
closed。后继build、Artifact upload与release checks均SKIPPED。

### 2.3 Python 3.10 on Windows

```text
run         = 42568657029 / attempt 1
job         = Python 3.10 on Windows / 129000700095
failed step = Run Starter and Authoring Skill 0.2.0 on their declared Core 0.12.2 lane
```

同一产品测试边界全部SUCCESS。冻结Core 0.12.2 wheel随后连续四次得到retryable HTTP 504；60秒恢复预算不能承担下一次
bounded retry，下载器fail closed。后继build、Artifact upload与release checks均SKIPPED。

Workbench job `129000700069` SUCCESS；四个依赖job group因required predecessor未全部成功而SKIPPED。成功job、不同Python lane与
不同asset不能拼接成original Public CI通过。

三个failed log与failure capture SHA-256为：

```text
E3 log      acd6bb21ac909cb33c69baedf3debf0f508721086fa0be25f6cff03835efd109
E3 capture  3079ca5aeb8e592a5b30d2bd6fc400bdd4b3775367aa3a5cc2d63163e8351336
Py3.13 log  2e4a4047ee131853811c9667507c11bf3eae6cea68a0abb3fd3f54b0d486e3c0
Py3.13 cap  01bc04b9bb8da442732523977e5f4016b5369af5ca90ee349a689692dd50ee35
Py3.10 log  9d7d10b7b73a581e6fca2058e8e72f2acce9354b442385dfc09a819f9ec6ba28
Py3.10 cap  bc700e80e200bc152ee956b2590864402aa5c2fb3d7719c9b04cd244c19df276
terminal    d6d4956530e7bd208a0ea8318598e8f7ebe35da1fe3cc434c50ed6cddaf96393
post-close  f5877883ea5723ff3068f43963cdbcd2786e888b9475c124ebf728d52c9af8df
```

remote pre-push TLS EOF、三个`gh run view` API EOF、REST summary EOF、Python 3.10 monitor/log retrieval EOF与terminal capture
boolean-name proof-facility error均按原identity保留，effect `NON_QUALIFYING_NONE`。

## 3. 归层、资格与原工程问题分离

当前证据只允许：

```text
original required gate failure             ESTABLISHED
observed failure layer                     FROZEN_RELEASE_ASSET_DELIVERY_PATH
HTTP response status                       504 / RETRYABLE
bounded recovery exhaustion                ESTABLISHED
download tool fail-closed behavior         CONFORMING
wrong bytes accepted                       NOT_OBSERVED
asset digest mismatch                      NOT_OBSERVED
candidate semantic regression              NOT_ESTABLISHED
Subject failure                            NOT_ESTABLISHED
workflow/runtime/test/oracle defect         NOT_ESTABLISHED
shared root cause across three jobs        NOT_ESTABLISHED
GitHub/proxy/shared-egress/network cause    UNKNOWN
```

候选只修改五份文档；三条失败lane在下载前已经完成各自的相关产品或资产检查。这个disjoint scope与前置SUCCESS支持
`candidate regression = NOT_ESTABLISHED`，但它们不产生docs-only exemption，也不能把失败run改写成PASS。

原工程问题、当前证明义务与适用世界继续机械分开：

```text
original engineering problem = 保持准确、自洽、可公开观察且不越权的bounded current-state projection
current proof obligation      = 只资格化#447 original-gate failure identity、effect与最小后继责任
applicability world           = f2ab7b78 exact main + run 42568657029 attempt 1 + 本audit自己的final bytes/资格链
proof_is_not_problem_solving  = true
```

形式上说明“为什么不能合并0.8”不等于0.8已经正确；本audit将来qualified也不等于project-state projection已经更新。

## 4. frozen recovery oracle没有被击穿

[release download recovery](98-release-download-recovery-correction.md)与
[multi-asset lane correction](357-release-download-multi-asset-lane-budget-correction.md)要求有限deadline、窄retry集合、owned partial清理与
摘要相等后才接受资产。本run没有观察到错误字节被接受、digest mismatch被忽略、partial被发布、deadline失效或required gate被绕过。

因此本失败不授权：

```text
扩大60/120秒预算
无限重试或retry-until-PASS
rerun 42568657029
删除、降级或skip required lane
移动或重制冻结Release资产
修改frozen digest或asset name
把不同job的PASS借给失败job
把三个HTTP 504命名成已证明的单一GitHub、代理、网络或runner根因
```

后继时间点若成功，只能证明自己的新world跨过相同门；它不能解释或回填run `42568657029`。

## 5. 最小合法recovery seam

当前最小合法问题是：

> 怎样先让#447的original-gate failure成为有界、可复算的qualified history，再从新exact main判断project-state projection是否仍需
> version successor？

恢复必须串行：

1. 本docs-only audit先取得自己的local、original PR、protected merge、new exact-main双门、fresh readback与independent
   reconciliation，只把#447失败identity、qualification effect与authority ceiling升级为qualified history；
2. 如果本audit的unchanged required lane完成，只证明恢复无需弱化门，不解释也不回填#447；
3. publication形成新事实后返回CONTROL LOOP，复核projection 0.7、#446 frozen implementation、#447 retained failure、当前main与公开
   projection lag；
4. 只有仍需0.8且没有新runtime/test/oracle反例时，才从新的exact main重新构造versioned projection successor final bytes，取得新的
   base/head/tree、milestones binding、original attempt、exact-main gates与fresh readback；
5. doc391与旧project-state 0.8 bytes不得cherry-pick、空提交重放或继承资格；只能作失败world provenance输入；
6. 如果本audit自己的required lane再次失败，保留新identity并重新判断最小failure/proof-facility边界，不能弱化oracle。

本文不预先授权projection 0.8 successor、freeze publication、runtime maintenance、budget correction、manifest、Evidence、persistence、
public Review或R2–R6。

## 6. 本audit自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/392-r1-public-project-state-projection-0.8-original-gate-failure-boundary-audit.md
docs/milestones.md
```

`docs/project-state.md`、doc375–390、runtime、tests、fixtures、workflows、download policy、Release assets、Schema、Provider、Collector、
P2/Core oracle、Verdict与全部frozen semantic bytes必须保持`f2ab7b78…` base bytes。final bytes至少通过exact四文件scope、UTF-8 without
BOM、LF/final LF、links/fences/headings、required markers、#447 failure identity与log digest复算、`git diff --check`、global/local
hygiene、focused Python 3.10.6 / 3.13.13 × normal / `-O`四格及primary `audit.json` continuity。

本候选的首轮local witness为：

- exact四文件scope、Markdown、873个local links、#447 identity、retained failure摘要、7/5/4次HTTP 504计数、
  `docs/project-state.md`不变、remote main与primary audit continuity全部PASS；
- Python 3.10.6 / 3.13.13 × normal / `-O` focused四格各22/22 PASS；
- global/local hygiene 8/8 PASS；
- local qualification、final diff review与retained-failure validation SHA-256分别为：

```text
e8ca36b4a96fbf933bad26b314cb4ed99165838d2218101aa0fae29713a1d3aa
d0aba4cc5eee3316a9ce473998cd6226f0b624a7364ae92bbc72ed22d14c930d
acd3542cef58974f3e8712f05cd1402e6518b7b8553d21d7879d1f123d662e80
```

这些identity属于写入本段以前的pre-record bytes。本文加入witness记录以后，final bytes必须重新运行相同local gates并由外部
evidence seal固定；不得用上述pre-record PASS冒充final-byte qualification。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required gates (new attempt; no rerun of #447)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source / failure / problem-identity reconciliation
    -> finite closeout / integrity
    -> ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止，不重复已有PASS。

## 7. 当前状态与停止线

全部最后门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_8_PR447_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_NOT_MAINLINE_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。projection 0.7继续是current frozen
mainline projection；PR #447/doc391/0.8 candidate继续closed/unmerged/not-qualified/not-frozen；三个job failure、所有setup error与lower
`UNKNOWN`均不回填。随后必须返回CONTROL LOOP，不能按文档编号自动重建projection或启动任何runtime seam。
