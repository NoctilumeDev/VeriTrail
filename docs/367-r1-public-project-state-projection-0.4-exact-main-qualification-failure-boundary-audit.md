# R1 public project-state projection 0.4 exact-main 资格失败边界审计

日期：2026-11-06

> 状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 坐标：`main@abf06ecfbd01852c202096a7733165f6cb0f0f70`，tree
> `e2c98f48cc0071bd1aa85d8134e155ee55fb3e45`。
>
> 受审对象：[文档366](366-r1-public-project-state-projection-successor-0.4-contract.md)与
> `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4` candidate的exact-main qualification failure。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只保存失败identity、qualification effect与最小后继责任；不修改
> doc366、`docs/project-state.md`、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict
> 或任何frozen semantic bytes，也不把0.4升级为qualified candidate。

## 1. CONTROL LOOP 触发事实

PR #418绑定下列candidate：

```text
base   = 27f0b93eeb5ace7b5428ebc0c07cb1ebe4199f25
head   = bdf5c170817b3b79c4e597d93c76229f36516463
tree   = e2c98f48cc0071bd1aa85d8134e155ee55fb3e45
scope  = AGENTS.md
         README.md
         docs/366-r1-public-project-state-projection-successor-0.4-contract.md
         docs/milestones.md
         docs/project-state.md
```

original Public CI `42207330233` attempt 1为11/11 SUCCESS。protected exact-head merge形成：

```text
merge   = abf06ecfbd01852c202096a7733165f6cb0f0f70
tree    = e2c98f48cc0071bd1aa85d8134e155ee55fb3e45
parents = 27f0b93eeb5ace7b5428ebc0c07cb1ebe4199f25
          bdf5c170817b3b79c4e597d93c76229f36516463
```

new exact-main Browser Smoke `42211661825` attempt 1为1/1 SUCCESS；new exact-main Public CI
`42211661846` attempt 1以FAILURE终结，没有rerun。required Python 3.10 job失败后，四个依赖job group按workflow条件
SKIPPED。original PR的11/11与Browser Smoke的1/1都不能替代失败的exact-main required gate。

因此doc366 §8声明的资格链在new exact-main Public CI处终止。README/project-state/doc346/doc364/doc365/doc366 fresh
installed-product readback没有启动，AGENTS/milestones raw observation没有启动，independent reconciliation没有启动；0.4
contract与projection均未取得qualification或freeze authority。

## 2. required Python 3.10失败的直接事实

失败坐标：

```text
run         = 42211661846 / attempt 1
job         = Python 3.10 on Windows / 127871513134
failed step = Run Core regression tests / step 12
suite       = 496 reported / 1 failure / 1 skipped
test        = tests.test_bootstrap_run_cli.BootstrapRunCliTests.
              test_staging_failure_creates_public_error_bundle_after_reverse_cleanup
source      = tests/test_bootstrap_run_cli.py:1683
expected    = PENDING
actual      = FAIL
```

test在失败assertion前已经观察到：

- injected staging writer写入17 bytes后抛出`OSError("injected staging failure")`；
- public runner保留`EVIDENCE_STAGING_FAILED`；
- lifecycle trigger/stop reason均为`EVIDENCE_ERROR`；
- actual teardown顺序为`application -> dependency`；
- lifecycle cleanup为complete；
- report execution status为`ERROR`。

随后`result.report["verdict"]`实际为`FAIL`而不是预期`PENDING`，test立即停止。它没有把临时Bundle、decisive assertion列表、
Browser attachments或report JSON输出到Actions log，也没有为失败job上传Artifact。因此直接证据只支持：

```text
execution status                         = ERROR
public verdict                           = FAIL
at least one decisive assertion failed  = PROVEN_BY_VERDICT_RULE
precise decisive assertion              = UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT
```

现有`verdict.evaluate`顺序会先处理decisive `FAIL`，再处理`execution_status != COMPLETED`；所以`ERROR / FAIL`在规则上可形成，
但日志不足以确定究竟是哪个Browser或其他decisive fact失败。不得从`FAIL`反推具体Subject、Chromium、socket、port、resource、
fixture或timing根因。

## 3. Artifact与source-scope边界

该run只上传了successful Python 3.13 lane的四个Artifact：

```text
13500631599  core-wheel-3.13
13500527316  p3-wheel-probe-3.13
13500477691  core-sdist-3.13
13499459353  github-evidence-wheel-3.13
```

这些Artifact已在过期前下载并逐文件固定，但它们不包含失败job的临时Bundle，不能解释或复现Python 3.10失败。failure evidence
seal与finite integrity SHA-256为：

```text
ced9138ea87e4bd1c3f06b46bb67cb87a99f4ac957a9a7faae3279919ff3eabc
c663feeac7036c636fe7c2023413584fe9af61dc0a0aadfddec3daae894ed8f7
```

PR #418从base到merge只修改五个docs surface；`src/`、`tests/`、`web/`、`.github/`、`pyproject.toml`、plugins、starter与
authoring均无diff。相同tree的original PR Python 3.10 lane通过，而exact-main attempt失败。这足以排除“candidate修改了失败test或
runtime”的直接因果链，但scope disjoint不能替代qualification，也不能证明环境或fixture根因。

```text
candidate semantic regression    = NOT_ESTABLISHED
subject failure                  = NOT_ESTABLISHED
test/runtime defect              = NOT_ESTABLISHED
environment/resource cause       = NOT_ESTABLISHED
lower cause                      = UNKNOWN
exact-main qualification         = FAILED
```

## 4. 0.4资格与上游有效事实分离

PR #417/doc365已经独立使#398/doc346成为
`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`，该事实不被本次失败改写。projection 0.3也继续承担
`FROZEN_HISTORICAL`身份。

但doc366/0.4必须通过自己的完整资格链，不能继承#417或original PR #418的绿灯：

```text
upstream private implementation readback qualification = EFFECTIVE
projection 0.3 frozen historical identity              = EFFECTIVE
projection 0.4 candidate content                       = MERGED
projection 0.4 exact-main qualification                = FAILED
projection 0.4 installed-product readback              = NOT_STARTED
projection 0.4 qualified/frozen status                 = NOT_QUALIFIED / NOT_FROZEN
```

`docs/project-state.md`中的candidate声明属于#418 final bytes；它不能通过描述自己而升级，也不能被本文静默改写成PASS。

## 5. 禁止的伪恢复

以下动作均不能让PR #418或doc366取得资格：

```text
rerun Public CI 42211661846
retry until PASS
用original PR 11/11或Browser Smoke 1/1替代exact-main failure
用Python 3.13 SUCCESS替代Python 3.10 required failure
把docs-only scope解释成qualification exemption
删除、skip、放宽或重写该M10 test和PENDING oracle
把ERROR / FAIL无证据改名为Subject、Chromium或resource根因
在exact-main gate失败后启动fresh readback或reconciliation
把后继candidate PASS回填成#418 PASS
```

run、job、failed log、skipped topology、successful-lane Artifact、`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与`UNKNOWN` lower cause
必须保持原identity。任何后继成功只能证明自己的新exact world。

## 6. 最小合法 recovery seam

当前最小合法问题不是“再跑同一检查”，而是：

> 怎样在不弱化Core oracle、不伪造下层根因、也不借用旧绿灯的前提下，先限定0.4的qualification failure，再判断需要
> versioned projection successor还是独立test/runtime maintenance？

恢复必须串行：

1. 本docs-only failure-boundary audit先取得自己的local、original PR、protected merge、new exact-main双门、fresh readback与
   independent reconciliation，只把失败identity与authority ceiling升级为qualified history；
2. publication形成新事实后返回CONTROL LOOP，重新审计该required test、当前main与保留失败；
3. 如果出现可证实的runtime/test反例，只reopen/version最小地基边界并独立资格化，不能借projection candidate顺带修复；
4. 如果审计自己的unchanged required lane完成且仍没有下层反例，后继projection successor也必须绑定新base/head/tree与新
   original attempt，显式承担#418失败历史和新资格责任；不能是空提交或#418重放；
5. 无论哪条路径，都要从头通过自己的完整资格链；后继PASS不解释、不覆盖本次attempt 1。

本文不预先授权0.5、runtime patch或freeze publication。只有后继CONTROL LOOP能根据新exact事实选择最小seam。

## 7. 当前状态与authority ceiling

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_IMPLEMENTED_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN_HISTORICAL

R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED

R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文不冻结#398 private implementation，不恢复global composition authority，也不授权manifest、Evidence、persistence、public
Review或R2–R6。

## 8. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/367-r1-public-project-state-projection-0.4-exact-main-qualification-failure-boundary-audit.md
docs/milestones.md
```

doc366、`docs/project-state.md`、runtime、tests、fixtures、workflows、Schema、Provider、Collector、P2/Core oracle、Verdict及全部
frozen semantic bytes必须保持`abf06ec…` base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、
links/fences/headings、required markers、failure log/Artifact/source identity复算、`git diff --check`、read-only hygiene与primary
`audit.json` continuity。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required gates
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc367 / milestones readback
    -> independent source-byte / Bundle / identity / retained-failure reconciliation
    -> FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是candidate。闭合后也只能返回CONTROL LOOP；不得直接重建projection、冻结private implementation或启动
后续runtime seam。
