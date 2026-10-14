# R1 Fact → Coverage same-attempt handoff 最小合同冻结发布

日期：2026-10-15

## 1. 发布对象与条件状态

本文只发布[文档 259](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)定义的最小语义合同
`r1-fact-to-coverage-handoff/0.1`。文档 259 的已资格化字节保持不变；其中的 candidate marker 保存候选历史，
本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

这些字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、protected merge、
new exact-main 双门、fresh anonymous installed-product observations 与 independent reconciliation 全部闭合以前，事实仍是
qualified contract candidate。合同冻结不授予 handoff implementation 或 Coverage authority。

| 坐标 | 值 |
| --- | --- |
| current-state audit | [文档 258](258-r1-fact-to-coverage-same-attempt-handoff-current-state-audit.md) |
| 语义合同候选 | [文档 259](259-r1-fact-to-coverage-same-attempt-handoff-contract.md) |
| 候选 PR | [#298](https://github.com/NoctilumeDev/VeriTrail/pull/298) |
| 候选 base | `ec0f7e08f45be57754e0cfe86f000de7ac045e4b` |
| 候选 final head | `fae10532d7781adb556956724ef6c532b2f74b66` |
| 候选 merge / qualified exact main | `2a97b5cd6cdf0598db07a26d3640e4408f84713b` |
| 候选 head / merge tree | `f3f05d9c9f3059407ee2c06693b8e15051846046` |
| 本发布施工 base | `06f13d9d035702281862ae59a2f84e656ccee795` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义与 `FCHC-000..011` 反例义务仍全部由文档 259 定义。本文不增删 handoff predicate、semantic branch、
obligation-slot identity、Provider responsibility、one-shot rule 或 Coverage authority ceiling。冻结范围为：

```text
exact owned Fact-stage history
    + complete Parse partition / U / E / blockers / mapping
    + complete Provider responsibility / lifecycle / terminal history
    + FactSet or exact absence
    + original attempt / BudgetContext / whole-attempt safety state
    -> application-owned one-shot claim
    -> copy-owned private semantic handoff
```

合同对 normal fulfilled、optional gap、zero denominator、all rejected、projection blocked、required Provider
non-success 与 interrupted/unsafe worlds 作 total classification。FACT_DERIVATION denominator 的 authority source 是完整
`U`；unrepresentable U slot 即使没有合法 Fact ID 也不能消失、借用 arbitrary digest，或被现有 Coverage reason 偷换。

semantic projection 可以复算，live claim authority 不能由相同 bytes、digest、FactSet、limits、fresh Context 或 foreign
attempt 继承。handoff 成功只证明完整 Fact-stage history 被无损交给受约束 downstream consumer，不证明 Coverage item、
stage disposition、seven-stage join、ReviewSliceSet、Verdict 或 publication 已成立。

本发布不选择 persistence Route A/B，不选择 public Schema/carrier，也不决定 U slot 到 Coverage vocabulary 的映射。
若后继实现只能修改 frozen Fact history、恢复 stopped attempt、重跑 Parse/Provider，或让 handoff 自己裁定 Coverage，必须
fail closed 并返回 CONTROL LOOP。

## 3. 候选 source 与远端资格

PR #298 最终只有一个 commit、四个文件，`+395 / -4`：

```text
README.md
AGENTS.md
docs/259-r1-fact-to-coverage-same-attempt-handoff-contract.md
docs/milestones.md
```

受审 head 与 merge tree 完全相同。merge parents 依次为：

```text
ec0f7e08f45be57754e0cfe86f000de7ac045e4b
fae10532d7781adb556956724ef6c532b2f74b66
```

| 门 | 原始 Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #298 Public CI | [38344285489](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38344285489) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [38626280347](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38626280347) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [38626280577](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38626280577) | 1 | `1/1 SUCCESS` |

两个 Public CI run 的 Review Attention 四格各为 `501 reported / 498 passed / 3 skipped`，不能写成 501 项全部实际通过。
这些门只证明 candidate 与 candidate exact-main 的声明矩阵，没有把 existing Coverage fixtures 升格成 handoff runtime。

候选以后，PR #299 只向仓库增加一份 `RESEARCH_NOTE / NON_NORMATIVE / NO_R1_STATE_CHANGE` 文档；它没有修改
doc259、runtime、tests、Schema、Profile、Policy 或 milestones。PR #299 original Public CI
`38631990832` attempt 1 为 11/11 SUCCESS；ordinary merge
`main@06f13d9d035702281862ae59a2f84e656ccee795` 的 Public CI `38635767457` attempt 1 为 11/11 SUCCESS，
Browser Smoke `38635767688` attempt 1 为 1/1 SUCCESS。因此本发布的 source state 已取得自己的 exact-main
qualification，没有从 PR #299 原始门或内容等价继承资格。

## 4. 候选 fresh product observation 与保留历史

候选最终读回只绑定 `main@2a97b5cd6cdf0598db07a26d3640e4408f84713b`。fresh CPython 3.13.13 venv 从
`site-packages` 使用 released Core `0.13.0`、GitHub Evidence `0.1.0` 与 Playwright `1.62.0` / matching Chromium；
公开 wheel 复用封存下载字节，不冒充新下载。

README、doc259、milestones 三份正式观察使用独立 Plan/session/output，均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、
Core `PASS`，且 raw Markdown bytes 等于 exact Git blobs。本 world 的正式历史为 `3 PASS / 0 formal non-success`；
三个 target-specific readiness diagnostics 均为 `DIAGNOSTIC_ONLY_NON_QUALIFYING`。

independent reconciliation attempt 1 把 live PR metadata 误读为固定 `changedFiles` shape，以
`KeyError: changedFiles` 终止，身份保持 `PROOF_FACILITY_ERROR`。最小修正只适配实际 metadata shape；原 Plan、session、
product outputs 与三份 formal observations 不变。attempt 2 PASS：

```text
9f346117c05bdffd031092ddc689ecabfa8a7446701fa8122fbcf18f29949395
```

候选 qualification closeout 绑定 150 份 terminal artifacts，candidate qualification SHA-256 为：

```text
3109b2a6a446ed6323db67df40b2579205bc7763bfc55d7cd4e1ec1eb6af297b
```

文档 259 的 qualified full-file SHA-256 必须继续等于：

```text
afc40f1226325ac97297863bc99df4f837a37b1617d1c51e5c038cc0f9f39524
```

上游 doc258 reconciliation / closeout、候选 local/original/exact-main gates、全部 diagnostics、setup findings 与
reconciliation 首败均保持自己的原 identity。新 PASS 不覆盖旧失败。本地 checkout 对齐和只读 hygiene 只是 housekeeping，
不是事后增加的冻结门。

## 5. 本发布自己的资格门

本轮只允许修改 README、AGENTS、milestones 并新增本文。doc259、全部旧合同、runtime、tests、workflows、Schema、
fixtures、Profile、Policy、identity vectors 与架构资产必须保持本发布 base 字节。

final publication bytes 提交前必须取得：

1. Fact fulfillment、Parse→Fact consumer、Coverage Schema semantics 与 hygiene 的 CPython 3.10.6 / 3.13.13、normal /
   `-O` 四格串行回归；保留实际 counts / skips，不能把 skipped witness 写成通过；
2. exact four-file scope、其余 tracked bytes与 doc259 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件 marker、禁止越权状态与 `git diff --check`；
3. 候选 closeout、independent reconciliation、PR/exact-main terminal gates 与其引用 seals 的重新核验；只读 repository
   hygiene，不删历史证据。

final bytes 的四格串行回归已经执行：CPython 3.10.6 / 3.13.13、normal / `-O` 各
`89 reported / 87 passed / 2 skipped`。两个 skip 均为既有显式 reference runtime / Windows actual-child witness，不能
写成实际通过。`scripts/check_hygiene.py` 报告 `Residual Hygiene: PASS`；独立 byte audit 证明 exact four-file scope、
UTF-8 without BOM、LF/final LF、链接/fence/heading 与 doc259 SHA-256 continuity，`git diff --check` 通过。

这些是 publication 的本地 witness，不替代 original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc260 / milestones observations
    -> independent Core, source-byte and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback 必须为 publication merge exact main 创建新的 Plan/session/output identity，不复用 candidate observations。
README 观察可见的当前成熟度边界；doc260 与 milestones 观察 frozen target marker。doc259 的 unchanged full-file bytes在
独立对账中复核，不改它的历史 candidate marker，也不以 raw download 替代 P1/P2 formal observation。

最终核账要求每个 required target 恰好选择一份 qualifying PASS，并机械枚举全部 retained formal observations、diagnostics
与 setup findings；formal non-success 数量从历史导出，不预设 N。任何后继观察都须使用独立身份。新 main 若被其他 PR
推进，本发布继续在自己的 merge world 闭合，不拼接不同 SHA；随后再回外环绑定 current main。

## 6. 生效后的停止线

合同冻结只形成 handoff semantic authority。下一次必须从新的 exact main 重新读取文档 259 第 10–12 节、current runtime、
Coverage 0.1 vocabulary 与 retained counterexamples，判断 private feasibility 是否仍是最小合法问题。

```text
Fact → Coverage handoff implementation = NOT_STARTED / NOT_AUTHORIZED
Language Support / Parse / Fact persistence = OPEN / NOT_SELECTED
ReviewSliceSet / Coverage contract = NOT_STARTED
```

本文不启动 runtime、tests、Schema、public carrier、Coverage item/disposition mapping、seven-stage join、ReviewSliceSet、
Evidence/Bundle/publisher、CLI/Workbench/Core、其他顶层轨、CLAIM_FIDELITY、tag 或 Release，也不把 handoff contract
扩张成 truth completeness、semantic completeness、bug completeness 或全仓审查完成声明。
