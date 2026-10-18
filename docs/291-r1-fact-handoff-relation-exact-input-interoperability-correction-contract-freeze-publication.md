# R1 Fact handoff → Relation exact-input interoperability correction 最小合同冻结发布

日期：2026-10-19

## 1. 发布对象与条件状态

本文只发布[文档 290](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)定义的
`r1-fact-relation-interoperability-correction/0.1`最小语义合同。文档 290 的已资格化完整字节保持不变；其中的
`CONTRACT_CANDIDATE` marker保存候选历史，本发布自己的最后门全部闭合后才由本文承担当前冻结状态。

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED

R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED

R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

这些字节目前只表达publication target。本文自己的final-byte local gates、original PR qualification、单独批准的
exact-head protected merge、new exact-main Public CI与Browser Smoke、fresh anonymous installed-product readback及
independent reconciliation全部闭合以前，事实仍是qualified contract candidate。合同冻结不恢复旧composition施工，
也不授予successor implementation、manifest successor、persistence或public Review产品authority。

| 坐标 | 值 |
| --- | --- |
| correction feasibility qualified history | [文档 289](289-r1-fact-handoff-relation-exact-input-interoperability-feasibility-correction-audit.md) |
| semantic contract candidate | [文档 290](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md) |
| candidate PR | [#333](https://github.com/NoctilumeDev/VeriTrail/pull/333) |
| candidate base | `2f57c71e6e3a9ecb3e2d2da050d331fff7bb004a` |
| candidate final head | `2763e06bcbcdefeb3f5711f678dd4c22c826793e` |
| candidate merge / publication construction base | `33b4aa37d4ce22ebbac93e898e716da4e7053792` |
| candidate head / merge tree | `cc261643c65cfca879968d993816cabc8e427314` |
| publication impact | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范函数、authority owner、falsifier与停止线仍全部由文档 290 定义。本文不增删successor identity、Python class、field、
serialization、public Schema、manifest、Provider algorithm、Relation families或Coverage semantics。冻结范围只有：

```text
complete sealed Policy P
    + same-policy stage applicability A_s(P)

complete authoritative FactSet F
    + per accepted product/path MODULE closure C_H(F)
    + total Fact partition T_R(F)

Relation profile R
    + complete obligation projection O_R(F)
    + expected/emitted bidirectional, cardinality and uniqueness reconciliation

same-attempt Fact handoff claim
    + original BudgetContext / deadline / stop / revocation state
    + versioned successor boundary
```

`A_s(P)`只决定当前stage拥有的责任，不替换完整Policy；`T_R(F)`与`O_R(F)`不替换、过滤或重写完整FactSet。
non-applicable Facts继续保留在authoritative history。每个accepted product/path必须有恰好一个same-product MODULE anchor；
cross-path、foreign-product、missing、duplicate或filtered worlds均不能取得successor continuation。

`O_emitted`必须与从完整`F / P / R / C_H(F)`独立重算的`O_expected`双向相等、基数相等且每个identity恰好一次。
只证明emitted rows可追溯不构成完整性。known empty仍要求完整上游truth、完整partition与frozen required empty Provider
execution；它不等于FactSet missing、handoff未claim、unknown或无需执行。

相同semantic bytes、digest、equal limits或相同Relation outputs均不继承另一个attempt的claim、ProviderRun、receipt、
admission、continuation或BudgetContext。当前尝试过的所有candidate structures失败只能得到
`UNKNOWN / NO_QUALIFIED_CONSTRUCTION`；只有对合同明确限定的完整候选空间给出机械不可满足性证明，才可声明
`UNSAT / NO_CONSTRUCTION_EXISTS`。

## 3. 合同候选 source 与资格链

PR #333最终只有一个commit、四个docs-only文件：

```text
README.md
AGENTS.md
docs/290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md
docs/milestones.md
```

受审head与merge tree完全相同；merge parents依次为candidate base与final head。公开门均为原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #333 original Public CI | [39137995491](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39137995491) | 1 | 11/11 SUCCESS |
| exact-main Public CI | [39139725019](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39139725019) | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | [39139725021](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39139725021) | 1 | 1/1 SUCCESS |

候选local qualification绑定29项终态证据，authority ceiling为`CONTRACT_CANDIDATE_ONLY`；attempt 4在
CPython 3.10.6 / 3.13.13、normal / `-O`四格逐字节一致：

```text
semantic report digest
02f33ff455057ad1010ac392fdc1132b1e33fc9cf6b8e5bc65bc89f273cd7c07

local candidate closeout
a3a41da13fbf23d989bf1c7a6f075b535aab333d69ef75710bdc70054ebdda14
```

exact main随后对README、doc290与milestones各取得一份fresh installed-product
`FORMAL_READBACK_PASS`；三者均为P1/P2 `COMPLETE`、Core `PASS`，Plan、session、handoff与output identities互不复用。
独立对账重新验证Core、Git/public bytes、Bundle、三份formal identity、29项候选证据、doc289的176项qualified history与
全部保留setup/diagnostic history：

```text
independent reconciliation
4d93b5cb4960aac9551e126f13a511f2b27544fd40339ac20db65fb173a2c9c8

167-artifact closeout
30f7cf5eb104b443839bec94f17c442224f374fb058015db9cde353d7c6d4b16

doc290 full-file SHA256
a3e995085d8a13f4131b5a8f16eed72201edde21e1bed7182d84d3a8a1b08818
```

因此文档 290 只是qualified contract candidate；这些证据不替代本publication自己的资格链。

## 4. 保留失败与边界

合同候选及其readback继续保留下列不同身份：

- audit fixture误删Relation requirement的`AUDIT_FIXTURE_SETUP_ERROR`；
- candidate validation选择过宽、PowerShell scalar展示与local closeout base-tree错误；
- proof facility首次复制wheel wildcard、上游closeout目标文件名与dynamic-history freeze topology错误；
- 第二个proof facility把freeze wrapper自身stdout纳入静态集合，首次target diagnostic在产品Plan前被拒绝；
- doc290 public-render diagnostic #1终结为`ERROR / UNKNOWN`，fresh #2才取得`COMPLETE`；
- closeout attempt 1把仍会写入的wrapper stdout映射为空文件，作为独立setup错误保留；最终closeout直接运行同一冻结脚本。

后来的PASS不覆盖、解释或重命名这些事实。diagnostic不替代formal qualification；setup/operator failure不被提升为产品FAIL。
完整Policy、FactSet与candidate history不因publication而重写。

## 5. 本publication自己的资格链

本发布的tracked scope只允许：

```text
README.md
AGENTS.md
docs/291-r1-fact-handoff-relation-exact-input-interoperability-correction-contract-freeze-publication.md
docs/milestones.md
```

文档175、287–290、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors与corpus必须保持
`33b4aa37…` base bytes。local gates至少包括：

1. 四文件scope、UTF-8 without BOM、LF/final LF、live links、balanced fences、unique headings、条件marker与
   `git diff --check`；
2. doc290完整SHA、候选closeout/reconciliation、PR/exact-main gates、全部历史failure与引用seal的重新核验；
3. 声明的Markdown/baseline regression、四格audit report复核与只读repository hygiene。

这些只作publication本地witness，不替代original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR required gates
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc290 / doc291 / milestones observations
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback必须为publication merge exact main创建新的Plan/session/output identity，不能复用#333 candidate observations。
doc290 unchanged full-file bytes必须在独立对账中复核，不改它的历史candidate marker。每个required target恰好选择一份
qualifying PASS；formal non-success数量从完整历史机械导出，不预设N。

## 6. 生效后的停止线

合同冻结只形成private interoperability correction semantic authority。下一次必须从新的exact main重新进入CONTROL LOOP，
审查corrected successor feasibility是否仍是最小合法问题；即使可行，也必须另行取得明确implementation authority。

```text
correction implementation feasibility = NOT_STARTED
correction implementation             = NOT_STARTED / NOT_AUTHORIZED
old composition implementation        = STOP_CONDITION_TRIGGERED
manifest successor                    = NOT_SELECTED / NOT_AUTHORIZED
persistence                           = OPEN / NOT_SELECTED
public Review product                 = NOT_STARTED
```

本文不启动runtime、tests、Schema、RelationSet admission、Slice closure、ReviewSliceSet/Coverage composition、manifest
successor、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release，也不把合同扩张成
repository truth completeness、semantic completeness、bug completeness或全仓审查完成声明。

## 7. 当前publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

最后门闭合以后，本文第1节的`CONTRACT_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
