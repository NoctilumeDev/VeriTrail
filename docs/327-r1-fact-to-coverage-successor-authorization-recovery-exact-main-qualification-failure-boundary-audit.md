# R1 Fact→Coverage successor 授权恢复 exact-main 资格失败边界审计

日期：2026-10-27

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE`。
>
> 坐标：`main@310285aba4d2175164b53c4f68087817491df8bd`，tree
> `f04a7870f31aa6c02cf7419f7af1c3e5229bdc33`。
>
> 受审对象：[文档 326](326-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-publication.md)
> 的 exact-main qualification failure。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只冻结失败 identity、qualification effect 与最小 recovery seam；
> 不修改 Workbench、Starter、Core、runtime、tests、fixtures、workflow、required lane、timeout、oracle、0.2合同、Coverage、
> manifest、Evidence、persistence或public Review产品，也不把文档326升级为qualified authority publication。

## 1. CONTROL LOOP触发事实

文档326的docs-only authorization recovery candidate由PR #377从exact base
`ebeb890da1936cc15bcefe7e23c9bd532efd4787`提交：

```text
head  = 7c9ba8bf990622b19abd35d2bbad860138ced11a
tree  = f04a7870f31aa6c02cf7419f7af1c3e5229bdc33
scope = README.md
        AGENTS.md
        docs/326-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-publication.md
        docs/milestones.md
```

original Public CI `40506198552` attempt 1为11/11 SUCCESS。protected exact-head merge形成：

```text
merge   = 310285aba4d2175164b53c4f68087817491df8bd
tree    = f04a7870f31aa6c02cf7419f7af1c3e5229bdc33
parents = ebeb890da1936cc15bcefe7e23c9bd532efd4787
          7c9ba8bf990622b19abd35d2bbad860138ced11a
```

new exact-main Browser Smoke `40510081338` attempt 1为1/1 SUCCESS；new exact-main Public CI `40510081408`
attempt 1为10/11，required `Starter PASS/FAIL golden path` job `122222945703` FAIL。该run没有rerun，fresh
installed-product readback、independent reconciliation与finite closeout没有启动。

因此文档326声明的资格链在new exact-main Public CI处终止：

```text
authorization recovery publication = MERGED / NOT_QUALIFIED
PRIVATE_IMPLEMENTATION_ALLOWED      = NOT_EFFECTIVE
private implementation              = NOT_STARTED / NOT_AUTHORIZED
```

original PR的绿灯只属于head world；即使merge tree相同，也不能穿过失败的merge attempt取得exact-main authority。

## 2. failed job与Artifact的直接事实

failed-evidence Artifact为：

```text
name           = starter-single-webapp-s1-failure-40510081408-1
artifact id    = 12737259914
archive SHA256 = 33ef978964918c30870010fcc56082c7e5d29edc9778c72c0147108bfa6de4bb
```

job log与Artifact共同支持以下直接事实：

- Starter正向run的Bundle verdict为`PASS`，其声明assertions全部PASS；
- intentional negative run的Bundle verdict为`FAIL`，两viewport的`expect_text`均按预期观察到业务不匹配；
- Workbench生成并保留desktop/mobile的catalog、pass detail与fail detail六张截图；
- 最终WorkBench验真阶段累计到desktop console error：
  `Failed to load resource: net::ERR_NO_BUFFER_SPACE`；
- 既有oracle在全部声明交互与截图完成后正确拒绝该console error；
- cleanup完成，失败没有被静默改名或忽略。

失败输出没有保留触发console error的精确resource URL/request identity，也没有保留更底层的runner资源诊断。因此证据上限是：

```text
raw console failure                    = net::ERR_NO_BUFFER_SPACE
observed viewport                      = desktop
oracle behavior                        = CORRECTLY_REJECTED_CONSOLE_ERROR
exact failed resource identity         = UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT
exact underlying host resource cause   = UNKNOWN
subject failure                        = NOT_ESTABLISHED
docs-only candidate regression         = NOT_ESTABLISHED
```

失败分类文件SHA-256为：

```text
6a4feec11380f4c18a2897fb2f365786f156d5b5aeac3d7042fee1ce12383430
```

## 3. qualification failure与semantic defect分离

该失败足以否定文档326在`310285…`世界的exact-main资格，但不足以推翻文档320的feasibility witness、文档321–322的
frozen 0.2 contract、文档324–325的maintenance历史或文档326的bounded A–I设计内容。必须保留两种不同结论：

```text
semantic continuity result
    candidate在构造world中没有观察到新的0.2合同反例

qualification result
    merged publication没有通过自己预注册的exact-main required gates
```

前者不能覆盖后者；后者也不能在缺乏新证据时被扩大为Fact truth、Coverage semantics、0.2 handoff、Starter business
assertion或Workbench oracle的缺陷。PR #377只改四份文档，original head的同一required lane也已PASS；这些事实使
`docs-only candidate regression`保持`NOT_ESTABLISHED`，但不能产生qualification exemption。

## 4. 现有oracle边界没有被击穿

本次失败显示现有Workbench会在业务Bundle与交互截图都完成以后，仍独立检查浏览器console错误。这里没有出现：

```text
console error被忽略
collector failure被冒充Subject failure
业务PASS覆盖环境错误
cleanup缺失
required Starter lane被静默降级
```

因此当前证据没有资格修改console-error policy、Browser/Workbench分类、timeout、required lane、workflow success condition、
screenshot要求或cleanup oracle。把`net::ERR_NO_BUFFER_SPACE`加入忽略列表、增加retry或只看Bundle verdict，都会让失败更容易
消失，却不能证明文档326曾在原合同下通过。

## 5. 禁止的伪恢复

以下动作均不能让PR #377或文档326取得资格：

```text
rerun Public CI 40510081408
retry until PASS
用original PR 11/11或Browser Smoke 1/1替代exact-main 10/11
用相同tree推导qualification继承
把unknown host/resource cause伪装成Subject或候选回归
忽略console error、增加timeout或放宽required Starter lane
在exact-main gate失败后启动installed-product readback
提交空提交或无语义状态抖动后借用新绿灯
把后继candidate PASS回填成PR #377 PASS
直接启动private implementation
```

run `40510081408`、job `122222945703`、Artifact `12737259914`、raw console error、分类与两个UNKNOWN必须永久
保持原identity。

## 6. 最小合法qualification-recovery seam

当前最小合法问题不是“怎样让同一检查再跑一次”，而是：

> 怎样先让本次qualification failure成为有界、可复算的qualified history，再由fresh CONTROL LOOP判断是否存在一份承担
> 新失败历史与新资格责任的authorization recovery successor？

恢复必须串行分成两层：

1. 本docs-only failure-boundary audit先通过自己的完整资格链，只证明失败identity、UNKNOWN边界、authority ceiling与合法
   recovery seam；
2. 本审计资格化以后，fresh CONTROL LOOP才能判断是否存在一份新的authorization recovery candidate。后继必须拥有新
   base/head/tree、新original attempt，并明确承担PR #377失败与本文资格历史的独立对账责任；它不能是空提交、PR #377的
   重放或“平台这次也许正常”的裸重试。

如果本审计自己的required Starter lane再次失败，就保留新identity并重新判断最小test-support/environment边界；不得把重复失败
当作弱化oracle的理由。任何后继success只属于其新world，不解释也不回填`310285…`。

## 7. 当前状态与authority ceiling

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN

R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_MERGED_NOT_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_PUBLIC_CI_FAILED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED

R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

既有frozen contract、feasibility与maintenance history不被改写；但它们不能穿过失败的authorization publication取得
implementation authority。本文不授权runtime施工、Coverage producer、manifest、Evidence、persistence、public Review、
post-R1 Benchmark或R2–R6。

## 8. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/327-r1-fact-to-coverage-successor-authorization-recovery-exact-main-qualification-failure-boundary-audit.md
docs/milestones.md
```

文档326、runtime、tests、fixtures、workflows、Schema、Profile、Policy、Coverage、manifest、Evidence、persistence与public产品必须
保持`310285…` base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、
required markers、失败分类identity、`git diff --check`、read-only hygiene与primary `audit.json` continuity。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required gates
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc326 / 本文 / milestones readback
    -> independent source-byte / Bundle / identity / retained-failure reconciliation
    -> FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是candidate。闭合后也只允许返回CONTROL LOOP判断是否存在具有新事实与新资格责任的authorization
recovery successor；不得直接重建authority、施工runtime或进入后续阶段。
