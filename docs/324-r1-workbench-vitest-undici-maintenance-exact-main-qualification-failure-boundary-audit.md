# R1 Workbench Vitest/undici maintenance exact-main 资格失败边界审计

日期：2026-10-27

> 状态：`R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE`。
>
> 坐标：`main@5aeb53eeb0cca2dc92175fb5dfe4521388dca67a`，tree
> `96ff0ce193799760c41676404f1d33af63652ba9`。
>
> 受审对象：PR #373 Workbench Vitest/undici advisory maintenance 的 exact-main qualification failure。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结失败 identity、qualification effect 与合法 recovery seam；
> 不修改 Core/Workbench runtime、tests、fixtures、workflow、required lane、timeout、oracle、Schema 或 R1 合同，也不把
> maintenance 升级为 qualified。

## 1. 上游 R1 状态与第一次 authorization 失败

[文档 322](322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md) 已由 PR #369 精确合入
`main@b2626e8e31c7c2681dc87e74dff799471886648b`，tree
`b757b130c767013a8f2f3db621e83123cf629ee4`。original Public CI `39573932263`、exact-main Public CI
`39578176854` 与 Browser Smoke `39578176781` 均为 attempt 1 SUCCESS；fresh README/doc321/doc322/milestones
4/4 PASS。independent reconciliation 与 150-artifact finite closeout 分别为：

```text
f1cefeaa6f7d4deb862cc4a5f9a8684774e6d85718587b32ae1a911f2523e050
78bce5110f50afcdb961b48be9369d4b36724d7e7019747f020eb23c4c26d73a
```

因此 `R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN` 已生效。它只冻结 0.2 合同，尚未授权
private implementation。

第一次 docs-only implementation authorization candidate PR #372 绑定
`base=b2626e8e31c7c2681dc87e74dff799471886648b`、
`head=51528c7178c9d329c03daa39dda5951a827e3dca`、
`tree=a3316a6184cd13d4dd93a1d6accba056323fcd01`。original Public CI `40470062665` attempt 1 在
`Audit Workbench dependencies` 观察到 Vitest 4.1.11 与 undici 7.30.0 的五个 advisory，以 9 SUCCESS / 1 FAILURE /
1 SKIPPED 终结。PR #372 已关闭且未合并，保持 `CLOSED / UNMERGED / NOT_QUALIFIED`；其后任何 PASS 都不得回填该世界。

## 2. 独立 maintenance candidate 与 protected merge

PR #373 不修改 PR #372 或 R1 文档，只从同一 frozen main 建立独立 maintenance：

```text
base  = b2626e8e31c7c2681dc87e74dff799471886648b
head  = 4101357f138e90c9f1e69ccc0ca74ebd748d87c8
tree  = 96ff0ce193799760c41676404f1d33af63652ba9
scope = web/package.json
        web/package-lock.json
```

两次 fresh official-registry construction 得到相同 final bytes：Vitest 与 `@vitest/mocker` 为 4.1.12，undici 为
7.30.1，Vite 保持 8.2.4。本地 fresh `npm ci`、14-file/179-test Workbench regression、lint、build、`npm audit`
零漏洞、dependency tree 与 hygiene 均 PASS。original Public CI `40474320234` attempt 1 为 11/11 SUCCESS。

protected merge 形成：

```text
merge   = 5aeb53eeb0cca2dc92175fb5dfe4521388dca67a
tree    = 96ff0ce193799760c41676404f1d33af63652ba9
parents = b2626e8e31c7c2681dc87e74dff799471886648b
          4101357f138e90c9f1e69ccc0ca74ebd748d87c8
```

original PR 的绿灯只属于 head world。protected merge 以后仍必须通过新的 exact-main gates，不能因为 tree 与 PR head
一致就继承资格。

## 3. exact-main required Core gate 的直接失败事实

exact-main Browser Smoke `40478059772` attempt 1 为 1/1 SUCCESS。exact-main Public CI `40478059827`
attempt 1 以 FAILURE 终结：

```text
3 SUCCESS / 1 FAILURE / 4 SKIPPED

failed job  = Python 3.10 on Windows
job id      = 122101107016
failed step = Run Core regression tests
```

Python 3.10 job 的安装、exact editable Core coordinate、Starter/Core 边界、GitHub Evidence、Review Attention 与 frozen
Chromium 安装步骤全部成功。Core regression 共运行 494 项，得到 1 failure / 1 skipped：

```text
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_catalog_accepts_public_m10_outcomes_and_isolates_a_corrupt_copy

expected = (0, "", "PASS")
actual   = (0, "", "FAIL")
```

同一 run 的 Python 3.13 aggregated job SUCCESS；Workbench job的tests、lint、build与dependency audit全部SUCCESS。
Python 3.10 required Core job失败后，四个下游 job按workflow条件SKIPPED。这是完整的原始 attempt 1 拓扑，不是 11-job
成功矩阵。

## 4. 当前证据能证明什么，不能证明什么

失败测试只把 top-level `payload["verdict"]` 与 `PASS` 比较，没有把该次临时 Bundle 的 decisive assertion、Browser
attachments 或 report bytes 输出到 Actions log；`TemporaryDirectory` 在失败 unwind 后也没有被作为 Artifact 保留。因此直接证据只支持：

```text
positive M10 catalog fixture produced a public FAIL verdict
precise decisive assertion = UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT
```

它不支持进一步声称根因是 Subject、Chromium、socket、port、resource、fixture、timing 或 Core runtime。CPython 3.10.6
上的 fresh isolated repeat PASS，只是新的 non-qualifying diagnostic：它证明失败没有稳定复现，不解释原失败，也不能覆盖 required
gate。

maintenance 自身的 exact-main Workbench job与dependency audit均SUCCESS，而且 patch只修改两份web dependency manifest/lock
文件；Core runtime/test/workflow bytes未改变。由此可以排除“依赖 advisory 仍未修复”，但不能由 scope disjoint 自动推出整个
exact-main qualification成立：

```text
dependency correction effectiveness = OBSERVED_IN_WORKBENCH_JOB
maintenance regression              = NOT_ESTABLISHED
precise Core failure cause           = UNKNOWN
exact-main qualification             = FAILED
```

## 5. 禁止的伪恢复

以下动作均不能让 PR #373 取得资格：

```text
rerun Public CI 40478059827
retry until PASS
用 original PR 11/11 替代 exact-main failure
用 Python 3.13 SUCCESS 或 Browser Smoke SUCCESS替代Python 3.10 required failure
用隔离复跑PASS解释或覆盖原失败
把scope disjoint解释成qualification exemption
删除、skip或放宽该M10 test
改写expected PASS、timeout、required lane或workflow condition
在exact-main gate失败后启动installed Workbench readback
把后继candidate PASS回填PR #372或PR #373
```

run `40478059827`、job `122101107016`、failed log与`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`必须永久保持原
identity。

## 6. 最小合法 recovery seam

当前最小合法问题不是“再跑一次相同检查”，而是：

> 怎样在不弱化 Core oracle、不伪造失败根因、也不借用旧绿灯的前提下，先限定本次 qualification failure，再让一份新的
> maintenance recovery candidate承担完整证明责任？

恢复必须串行分成三项：

1. 本 docs-only failure-boundary audit 先取得自己的完整资格，只证明失败identity与authority ceiling；
2. 只有本审计自己的 unchanged required gates 成立后，fresh CONTROL LOOP 才能建立一份新的 maintenance recovery candidate，
   重新核验当前main上的Vitest/undici exact bytes、零advisory与完整资格链；它必须绑定新base/head/tree和新original attempt，不能是
   空提交或PR #373的重放；
3. maintenance recovery完成以后，再从新的exact main重建Fact→Coverage implementation authorization publication；旧PR #372
   永久保持closed/unmerged/not-qualified。

如果本审计自己的required Core gate再次出现同类失败，就保留新identity并重新判断test-support/runtime边界；不得把重复失败当作
放宽oracle的理由。

## 7. 当前状态与 authority ceiling

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN

R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_372_CLOSED_UNMERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_ADVISORY_MAINTENANCE_MERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_PUBLIC_CI_FAILED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE

R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

冻结合同、feasibility history与既有R1历史不被改写；但它们不能穿过失败的maintenance qualification取得implementation authority。
本文不授权runtime施工、Coverage producer、manifest、Evidence、persistence、public Review、post-R1 Benchmark或R2–R6。

## 8. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/324-r1-workbench-vitest-undici-maintenance-exact-main-qualification-failure-boundary-audit.md
docs/milestones.md
```

`web/package.json`、`web/package-lock.json`、docs/321–322、Core/Workbench runtime、tests、fixtures、workflows、Schema、
Policy/Profile、Coverage、manifest与persistence必须保持`5aeb53e…` base bytes。final bytes至少通过exact四文件scope、UTF-8
without BOM、LF/final LF、links/fences/headings、required markers、upstream failure identity、`git diff --check`、read-only hygiene
与primary `audit.json` continuity。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required gates
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc324 / milestones readback
    -> independent source-byte / Bundle / identity / retained-failure reconciliation
    -> FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是candidate。闭合后也只允许返回CONTROL LOOP判断是否存在具有新事实与新责任的maintenance recovery；
不得直接重建authorization、施工runtime或进入后续阶段。
