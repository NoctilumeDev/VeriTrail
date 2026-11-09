# R1 same-attempt DerivationEvidence continuity audit original-gate failure boundary

日期：2026-11-10

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@03f3f03b6ad116ccf345041cec6ba393a385cd62`，tree
> `cf250d51b1fb5767d2ff648b4d61f4f65b56f73a`。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只保存PR #453 original Public CI失败、检查被击穿的资格前提并限定最小恢复
> 边界；不资格化失败candidate、不改workflow/oracle、不rerun、不实现Evidence runtime，也不授权manifest、persistence、public Review或R2–R6。

## 1. CONTROL LOOP 与失败坐标

PR #453绑定：

```text
base  = 03f3f03b6ad116ccf345041cec6ba393a385cd62
head  = 948ba1d80c0da1aabb891efd19b7ebc55d12ae24
tree  = af62c70b00ac18ce8b8fc1d2cb4182edfc696148
scope = 1 commit / 4 docs files
run   = 42666764972 / attempt 1 / pull_request
```

original Public CI在run终态由GitHub Actions记录为`completed / failure`。该run没有rerun；PR #453已经关闭、未合并，remote main继续是
`03f3f03…`。primary `audit.json`继续保持
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

失败run、PR/commit/file identity、check suite、全部job metadata、全job log、空`--log-failed`输出、artifact listing与8个下载artifact file
已经封存。failure classification与original failure seal SHA-256为：

```text
30c7c3512afae63fd4d16ba9c23e542708f5e2c3790cc74b22d22fa5378b5ae2
052373a1b96764a1789e10f855db3e68954dc00ae1ca4b3285ef9f367ac3eccb
```

## 2. 反例处理方法

本失败采用以下控制原则：

> 理论遇到反例，先检查前提、适用域和观察是否成立；只有确认反例落在原适用域内，才重开理论本身。不得用不断增加例外来保护一个
> 已经失真的前提。

它在本次的机械含义是：

1. 不把“已实例化的9个job全部成功”改写成“9/9已经足够”；required workflow仍应完整形成11个job；
2. 不rerun直到PASS，也不让另一个PR的PASS回填本run；
3. 不因candidate只改docs就假设gate必然成功；先核对workflow identity、job graph、run/check suite与缺失job；
4. 不因run总结FAILURE就反向宣称semantic feasibility结论错误；先判断失败是否观察到candidate assertion或产品回归；
5. lower cause无法由现有证据唯一确定时保持`UNKNOWN`，不以“GitHub偶发”或“runner问题”替代证据。

这不是给资格链增加例外，而是拒绝改变资格定义来保护candidate。

## 3. Exact failure observation

同一`.github/workflows/ci.yml`在上游PR #452 original run `42639396145` attempt 1与merge后exact-main run `42647202547`
attempt 1都形成11个job，11/11 SUCCESS。PR #453没有修改workflow；其四个paths严格是README、AGENTS、doc394与milestones。

失败run只实例化以下9个job，而且9个全部`SUCCESS`：

```text
Python 3.10 on Windows
Python 3.13 on Windows
Wheel-only first run on Python 3.10
Wheel-only first run on Python 3.13
GitHub Evidence wheel-only on Python 3.10
GitHub Evidence wheel-only on Python 3.13
Acceptance Core freeze on Python 3.13
E3 0.2 release download acceptance
Workbench tests, lint, build, and audit
```

两个expected job没有形成job/check-run identity：

```text
Acceptance Core freeze on Python 3.10
Starter PASS/FAIL golden path
```

因此不存在可下载的failed step log；`gh run view --log-failed`为空。check suite与workflow run仍共同记录`failure`。不能把“没有failed
step”解释为PASS，也不能为缺失job虚构失败步骤、runner或产品输出。

机械failure-boundary audit SHA-256为：

```text
dd7e6621b5a77ed301473869acc189b80abc42a757fd750c5e2531377dbbf580
```

## 4. Failure classification 与non-findings

唯一有证据支持的failure identity是：

```text
PUBLIC_CI_WORKFLOW_RUN_CONCLUSION_FAILURE_WITH_TWO_EXPECTED_JOBS_NOT_INSTANTIATED
lower cause                    = UNKNOWN
candidate regression           = NOT_ESTABLISHED
Subject failure                = NOT_ESTABLISHED
product assertion failure      = NOT_ESTABLISHED
workflow byte change           = false
failed candidate qualification = NOT_QUALIFIED
```

这次反例击穿的是“该original PR attempt完整通过required gate”的资格前提。它没有观察到doc394内容的semantic counterexample，也没有
资格化doc394的feasibility结论。两者必须同时保持：semantic conclusion没有被本run反驳；candidate也绝不能因本地证据或9个job成功
而获得资格。

## 5. 对PR #453与doc394 bytes的影响

PR #453保持：

```text
CLOSED / UNMERGED
ORIGINAL_PUBLIC_CI_ATTEMPT_1_FAILED
NOT_QUALIFIED
NOT_MAINLINE
NO_READBACK
NO_RECONCILIATION
NO_CLOSEOUT
```

其commit、tree、local evidence与失败run永久可引用，但不得作为下一candidate的资格输入。后继即使文字相同，也必须从新的exact main
重新构造bytes、commit、tree、original attempt与完整资格链。不得cherry-pick失败commit后宣称资格连续，也不得删除失败evidence后冒充
第一次成功。

## 6. 最小恢复边界

本反例只重开：

```text
ORIGINAL_GATE_QUALIFICATION_ONLY
```

当前证据不授权修改workflow、required job count、timeout、oracle、semantic source audit、Evidence 0.2或frozen output admission。最小
恢复顺序必须是：

1. 本failure-boundary audit自己的docs-only candidate取得完整资格；
2. 返回fresh CONTROL LOOP，重新检查相同original engineering problem、proof obligation与applicability world；
3. 若没有新反例，从当时的新exact main独立重建same-attempt Evidence feasibility audit；
4. 新candidate仍必须取得自己的original 11/11、protected merge、exact-main双门、fresh readback、independent reconciliation与finite
   closeout；
5. 任何后继PASS只证明新world成立，不解释、覆盖或回填run `42666764972`。

若本failure-boundary audit自己的original gate再次以相同“expected job未实例化”身份失败，才累计第二次相同blocking condition；仍不得
弱化required gate。若出现不同failure identity，必须另行归层。

## 7. Authority ceiling

本文最多支持：

```text
failure boundary                         = audited history only
PR #453 feasibility candidate            = not qualified
same-attempt Evidence feasibility        = not yet qualified
versioned Evidence continuity contract   = not started / not authorized
Evidence runtime                         = not started / not authorized
manifest successor                       = not started / not authorized
global composition authority             = not restored / not authorized
persistence / public Review / R2-R6       = not started
```

## 8. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/395-r1-same-attempt-derivation-evidence-continuity-audit-original-gate-failure-boundary.md
docs/milestones.md
```

`docs/project-state.md`、doc318、doc377–394、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与
全部frozen semantic bytes必须保持base bytes。

## 9. Qualification pipeline

本文final bytes必须完成exact scope、UTF-8/LF/final-LF、links/fences/headings、failed run/artifact seal、upstream 11-job comparison、
unchanged workflow、remote main、primary audit、`git diff --check`与read-only global/local hygiene。

```text
final failure-boundary docs bytes / local gates
    -> original PR required 11/11 gate
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent run/job/workflow/source-byte/problem-identity reconciliation
    -> finite closeout
    -> FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

不得复用PR #453的9个successful jobs，也不得把本candidate的后继PASS写成对#453的解释。

## 10. 当前状态与下一合法边界

在本文自己的全部最后门闭合以前，只允许：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_FEASIBILITY_AUDIT_PR453_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_AUDIT_ORIGINAL_GATE_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文完整资格链闭合后最多成为`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；不得从失败边界直接施工
Evidence、重建candidate、修改workflow、启动manifest/persistence/public Review或进入R2–R6。
