# R1 ReviewSliceSet / Coverage composition qualification 最小合同冻结发布

日期：2026-10-16

## 1. 发布对象与条件状态

本文只发布[文档 267](267-r1-review-slice-set-coverage-composition-qualification-contract.md)定义的最小语义合同
`r1-review-slice-coverage-composition-qualification/0.1`。文档 267 的已资格化字节保持不变；其中的 candidate marker
保存候选历史，本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

这些字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、protected merge、
new exact-main 双门、fresh anonymous installed-product observations 与 independent reconciliation 全部闭合以前，事实仍是
qualified contract candidate。合同冻结不授予 Coverage vocabulary correction、composition implementation、
`ReviewSliceSet` / `CoverageLedger` assembler 或 publication authority。

| 坐标 | 值 |
| --- | --- |
| current-state audit | [文档 265](265-r1-review-slice-set-coverage-composition-current-state-audit.md) |
| precontract audit | [文档 266](266-r1-review-slice-set-coverage-composition-precontract-audit.md) |
| 语义合同候选 | [文档 267](267-r1-review-slice-set-coverage-composition-qualification-contract.md) |
| 候选 PR | [#309](https://github.com/NoctilumeDev/VeriTrail/pull/309) |
| 候选 base | `becf49db117be20ecdb4d860c1763ad7bc0eaae7` |
| 候选 final head | `b86db5ee3bfae6c341a9a5d4634836b2c2dbb77a` |
| 候选 merge / 本发布施工 base | `4280355c6ec4d1ade9cceedf8a47853d1a93ea16` |
| 候选 head / merge tree | `bfa13c8e514a203b71e3869a5188c491ff466e23` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义、total branches、authority ceiling 与停止线仍全部由文档 267 定义。本文不增删 stage、predicate、reason、
transition、admission、branch、denominator owner 或 continuation rule。冻结范围为：

```text
attempt-neutral immutable DerivationInputSet
    + original one-shot Fact handoff / BudgetContext / attempt
    -> one application-owned composition attempt
    -> successor Relation responsibility / qualification / admission
    -> private Slice obligation closure
    -> ReviewSliceSet semantic projection + independent admission
    -> seven-stage Coverage qualification
    -> complete transition / terminal / branch reconciliation
    -> only then same-attempt continuation eligibility
```

每个 stage 必须先形成 authoritative subject universe 与 applicability partition；只有 applicable members 进入
qualification denominator，not-applicable history 仍完整保留。Coverage 只拥有 qualification，不拥有考试范围；actual
output、representability、Schema shape、UI、R3 priority 或 successful Provider subset 都不能缩小 upstream universe。

每个 next-stage subject 必须有 predecessor witness；每个应流转的 predecessor 必须有 successor 或 exact typed blocker。
silent disappearance、foreign reappearance、digest-only history transplant 与 local-equation false COMPLETE 一律拒绝。
ReviewSliceSet 必须先按 exact Slice obligation history独立 admit；相同 members、empty bytes 或
`slice_set_digest` 不继承 closure branch 或 admission authority。Coverage 只能在同一 composition attempt、同一 admitted set
及完整 history 上做保守汇合，不能反向改变 Slice admission。

`COVERED / MISSING / BLOCKED / UNKNOWN` 是 denominator 内的 qualification semantics；not-applicable 在 denominator 外保留。
任一 required universe、transition、attempt、history 或 upstream admission authority 不足时，对应 stage 必须为 `UNKNOWN`；
任一 `UNKNOWN` 使 overall 为 `UNKNOWN`，否则任一 `PARTIAL` 才使 overall 为 `PARTIAL`，其余才可能 `COMPLETE`。

U=3/E=2 projection-blocked world 的 blocker slot 继续使用 frozen `FACT` subject identity。Coverage 0.1 vocabulary 没有
`UNREPRESENTABLE_EXPECTED_FACT` 的无损 reason，因此 successor assembler/runtime 前必须先完成独立、最小、versioned
vocabulary correction。本文不选择版本号、Schema 文件、迁移策略、carrier 或 persistence Route A/B。

## 3. 候选 source 与远端资格

PR #309 最终只有一个 commit、四个文件：

```text
README.md
AGENTS.md
docs/267-r1-review-slice-set-coverage-composition-qualification-contract.md
docs/milestones.md
```

受审 head 与 merge tree 完全相同。merge parents 依次为：

```text
becf49db117be20ecdb4d860c1763ad7bc0eaae7
b86db5ee3bfae6c341a9a5d4634836b2c2dbb77a
```

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #309 original Public CI | [38836722757](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38836722757) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [38852540587](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38852540587) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [38852540955](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38852540955) | 1 | `1/1 SUCCESS` |

exact-main Public CI 的 Review Attention 四格均为 `513 reported / 510 passed / 3 skipped`；不能写成 513 项全部实际
通过。这些门只证明 candidate source 与声明矩阵，没有实现 Coverage vocabulary correction 或 composition runtime。

候选 final local qualification 绑定四格各 `128 reported / 128 passed` 的 declared narrow matrix；四份 mechanical audit
report 逐字节相同。其 qualification record SHA-256 为：

```text
1b049ff07d6cffbf9bb645228f828b52d89f1ae1a2efc03fdcd70b1e9d32ac1a
```

文档 267 的 qualified full-file SHA-256 必须继续等于：

```text
598ad8069df115a49baf35c7b62d43e286abe39096b4dc62ced23321d6024aa6
```

## 4. 候选 fresh product observation 与保留历史

候选最终读回只绑定 `main@4280355c6ec4d1ade9cceedf8a47853d1a93ea16`。fresh CPython 3.13 venv 从
`site-packages` 使用 released Core `0.13.0`、GitHub Evidence `0.1.0` 与 Playwright `1.62.0` / matching cached
Chromium；公开 wheels 只复用封存下载字节，不冒充新下载：

| Wheel | SHA-256 |
| --- | --- |
| Core 0.13.0 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence 0.1.0 | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

README、doc267、milestones 各自取得一份独立 qualifying PASS；P1/P2 均 `COMPLETE`、Core `PASS`，公开 raw bytes
逐字节等于同一 exact main 的 Git blobs。正式 history 为 `3 PASS / 1 ERROR`：doc267 formal observation #1 的 P2
`COMPLETE / HTTP 200`，P1 repository probe 则明确返回 `403 / remaining=0 / COLLECTION_BUDGET_EXHAUSTED`；后继
fresh readiness 与 doc267 observation #2 PASS 不覆盖该 ERROR。额度突发耗尽的外部原因保持 `UNKNOWN`。

两个 setup/operator error 也分别保留：首次 PowerShell `-LiteralPath` wheel copy 不展开通配符；首次 venv install command
遗漏单独需要的 Playwright。后继修正只完成 setup，没有把两者改写成产品失败。全部 render diagnostics、anonymous
rate/preflight/paired diagnostics 与 setup findings均为 `NON_QUALIFYING`。

independent reconciliation attempt 1 重新复算 installed Core verdict、Git/public bytes、Bundle、Plan/session/handoff、全部
formal/non-success/diagnostic/setup identities、#309 candidate/local/original/exact-main gates 与上游 127 项 closeout，并取得
PASS：

```text
independent reconciliation = 6fb87a704792b7f94c415f44765b059eb51057bafe1bc88f2383225c8b85f4a6
135-artifact closeout       = 76fa18bc8e868e7fe4d5cf4a197fe6b4ec9f7a5aa6c09efe7ba5d3592e8fe818
```

因此 doc267 已成为 qualified contract candidate。candidate marker、formal ERROR、setup errors 与所有上游首败保持自己的
原 identity；本地 checkout 对齐与侧栏 artifact hygiene 不是事后新增的 qualification gate。

## 5. 本发布自己的资格门

本轮只允许修改 README、AGENTS、milestones 并新增本文。doc267、全部旧合同、runtime、tests、workflows、Schema、
fixtures、Profile、Policy、identity vectors、corpus 与架构资产必须保持本发布 base 字节。

final publication bytes 提交前至少必须取得：

1. 本层声明的 R1 Schema、handoff、Slice join、Markdown 与 hygiene regression matrix；保留实际 counts / skips；
2. exact four-file scope、其余 tracked bytes与 doc267 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件 marker、禁止越权状态与 `git diff --check`；
3. 候选 closeout、independent reconciliation、PR/exact-main terminal gates、formal ERROR 与全部引用 seals 的重新核验；
   只读 repository hygiene，不删除历史证据。

这些是 publication 的本地 witness，不替代 original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc268 / milestones observations
    -> independent Core, source-byte and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback 必须为 publication merge exact main 创建新的 Plan/session/output identity，不能复用 doc267 candidate
observations。doc267 unchanged full-file bytes在独立对账中复核，不改它的历史 candidate marker，也不以 raw download 替代
P1/P2 formal observation。每个 required target 恰好选择一份 qualifying PASS；formal non-success 数量从历史机械导出，
不预设 N。

## 6. 生效后的停止线

合同冻结只形成 private composition qualification semantic authority。下一次必须从新的 exact main重新进入
CONTROL LOOP，分别审查：

1. mandatory Coverage vocabulary version correction 是否仍是最早合法 seam；
2. correction 只需修 `UNREPRESENTABLE_EXPECTED_FACT` reason/disposition boundary，还是现有 0.1 carrier 还有更早反例；
3. correction 资格化以后，private composition feasibility 是否仍能在现有 runtime primitives 上无损实现。

```text
Coverage vocabulary correction = NOT_STARTED / NOT_AUTHORIZED
composition private feasibility = NOT_STARTED
composition implementation      = NOT_STARTED / NOT_AUTHORIZED
Language Support persistence     = OPEN / NOT_SELECTED
```

本文不启动 runtime、tests、Schema correction、public carrier、`ReviewSliceSet` / `CoverageLedger` assembler、
Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、其他顶层轨、CLAIM_FIDELITY、tag 或 Release，也不把合同扩张成
repository truth completeness、semantic completeness、bug completeness 或全仓审查完成声明。

## 7. 当前 publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

最后门闭合以后，本文第 1 节的 `CONTRACT_FROZEN` target 才成为事实；随后只允许返回 CONTROL LOOP。
