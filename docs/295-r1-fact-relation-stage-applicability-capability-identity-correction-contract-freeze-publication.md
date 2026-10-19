# R1 Fact / Relation stage applicability capability identity 修正合同冻结发布

日期：2026-10-19

## 1. 发布对象与条件状态

本文只发布[文档294](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)定义的
`r1-fact-handoff-relation-interoperability-correction/0.2`与
`r1-fact-relation-stage-applicability/0.2`最小语义合同。文档294的已资格化完整字节保持不变；其中的
`CONTRACT_CANDIDATE` marker保存候选历史，本发布自己的最后门全部闭合后才由本文承担当前冻结状态。

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_QUALIFIED_HISTORY
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

这些字节目前只表达publication target。本文自己的final-byte local gates、original PR qualification、单独批准的
exact-head protected merge、new exact-main Public CI与Browser Smoke、fresh anonymous installed-product readback及
independent reconciliation全部闭合以前，事实仍是qualified contract candidate。合同冻结不授权corrected successor
implementation，也不恢复旧composition A–J，不选择manifest successor、persistence或public Review产品。

| 坐标 | 值 |
| --- | --- |
| correction audit qualified history | [文档293](293-r1-fact-relation-stage-applicability-capability-identity-correction-audit.md) |
| semantic contract candidate | [文档294](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md) |
| candidate PR | [#339](https://github.com/NoctilumeDev/VeriTrail/pull/339) |
| candidate base | `0dd06e0e236a56472925bd6f29fc053b49727958` |
| candidate final head | `e5ba262b602c86a9390d763c048a6eb31954af45` |
| candidate merge / publication construction base | `289b496282adaa20a582ef5ffb93a6a3476d4d6a` |
| candidate head / merge tree | `4c7c8f74a27b003e233f920a31f6876b766340c0` |
| publication impact | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范函数、authority owner、falsifier与停止线仍全部由文档294定义。本文不增删successor object、private carrier、Schema、
manifest、serialization、Provider algorithm、Relation families或Coverage semantics。冻结范围只有：

```text
complete sealed Policy P
    + exact bounded capability identities
    + exact requiredness / composition mode

Owner_0.2(P)
    FACT iff capability_id in {python-ast, python-ast-advisory}
    RELATION iff capability_id == review-relation-derivation

A_FACT_0.2(P) / A_RELATION_0.2(P)
    total + disjoint + exactly-once ownership
    applicable side + non-applicable side preserve complete Policy identity

complete authoritative FactSet F
    + unchanged per-product/path MODULE closure
    + unchanged total Fact partition
    + complete Relation obligation projection
    + expected/emitted bidirectional reconciliation

same-attempt Fact handoff claim
    + original BudgetContext / deadline / stop / revocation state
    + versioned successor boundary
```

Fact stage的required owner是`python-ast`，存在时optional owner是`python-ast-advisory`；Relation stage的required owner是
`review-relation-derivation`。`review-fact-derivation`仍是不存在的unknown capability，不能被别名化或规范化。
超出本文bounded universe的capability不能由任一stage静默认领；结果最多是该version下的
`UNKNOWN / NO_QUALIFIED_CONSTRUCTION`或明确input rejection，除非完整bounded候选空间已有机械不可满足性证明。

applicability只投影stage responsibility，不投影或替换完整Policy/Fact truth。完整Policy bytes/digest、完整FactSet
bytes/digest、non-applicable side、per-product/path closure、obligation denominator与terminal history必须保持。每个Policy row
在两个stage间恰好拥有一个owner；overlap、gap、duplicate、missing required row、错误requiredness与unknown row均不得取得
successor continuation。

`O_emitted`必须与从完整`F / P / R / C_H(F)`独立重算的`O_expected`双向相等、基数相等且每个identity恰好一次。
只证明emitted rows可追溯不构成完整性。相同semantic result、digest、limits或Relation outputs均不继承另一个attempt的
claim、ProviderRun、receipt、admission、continuation或BudgetContext。

## 3. 合同候选 source 与资格链

PR #339最终只有一个commit、四个docs-only文件：

```text
README.md
AGENTS.md
docs/294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md
docs/milestones.md
```

受审head与merge tree完全相同；merge parents依次为candidate base与final head。公开门均为原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #339 original Public CI | [39206452352](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39206452352) | 1 | 11/11 SUCCESS |
| exact-main Public CI | [39213475131](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39213475131) | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | [39213475022](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39213475022) | 1 | 1/1 SUCCESS |

候选local qualification绑定19项终态证据，authority ceiling为`CONTRACT_CANDIDATE_ONLY`；pure semantic model在
CPython 3.10.6 / 3.13.13、normal / `-O`四格逐字节一致：

```text
candidate local seal
02c3120e516ed24a8f0d8e89a5f1cf52a0da9418a8051983447038a6575b185c

semantic report SHA256
a1201a99ea6cc28edcbae973d69d550aa6c1e2c607d77dc1530622c4d2864e7d

semantic digest
74f5f8bef3edc46278bb927c967976a159f3d991a7390e999123909482fa2809
```

同一四格分别运行现有Fact fulfillment、Relation derivation、Relation observation qualification与RelationSet admission窄基线；
每格均为`Ran 77 tests / OK (skipped=1)`。该model与回归只证明合同区分可机械表达且未观察到既有产品回归，不是runtime
implementation或产品资格证据。

exact main随后对README、doc294与milestones各取得一份fresh installed-product `FORMAL_READBACK_PASS`；三者均为P1/P2
`COMPLETE`、Core `PASS`，Plan、session、handoff与output identities互不复用。独立对账重新验证Core、Git/public bytes、
Bundle、三份formal identity、19项候选证据、doc293的132项qualified history与全部保留setup/diagnostic history：

```text
independent reconciliation
19fd667cb7fd5ff13e31932a49429dcffa218760d06ee13366a2a3a1dbd23bc2

130-path closeout index
20a28872176ed644163ab485c9aef36ac9473f0c97e6b32a5c5150ab4d6e7dc3

upstream doc293 closeout
54231fcfb88109112115ac5c5b08e1ad088d8269c266b9221885442b37b70cdf

doc294 full-file SHA256
1ef2ddeb2c8fd87c9053138e38a509e73bb6d5a99a53ba0ecb1916d14eaebece
```

因此文档294只是qualified contract candidate；这些证据不替代本publication自己的资格链。

本publication本地复算该closeout index时发现一个proof-facility self-capture缺陷：索引把执行时仍为空的
`create-closeout-attempt-1.stdout.txt`记为empty digest，closeout script返回后wrapper又向同一文件写入277 bytes终态输出。
其余129项逐项与索引一致；该stdout只回显closeout本身的result、count、hash、remote main与ceiling，不是reconciliation输入。
因此候选资格继续由先前完成的independent reconciliation、三份formal PASS与129项稳定artifact支撑；本文保留该finding，
不把130-path index误述为130项全部终态封存，也不反写历史文件。

## 4. 保留失败与边界

修正审计、合同候选与readback继续保留下列不同身份：

- 文档293 attempt 1手写64 MiB transport limit触发的`AUDIT_HARNESS_SETUP_ERROR`；
- 本候选proof facility建立前未显式代理的`git fetch` DNS失败，归为`NETWORK_PROXY_SETUP_ERROR`；
- readback setup 1错误选择README marker，形成独立`READBACK_MARKER_SELECTION_SETUP_ERROR`与正式non-qualifying历史；
- readback setup 2的README正式观察以P1 `COMPLETE`、P2 navigation `ERROR`终结，底层原因保持`UNKNOWN`；
- setup 2随后复用既有Plan identity prefix，归为独立Plan construction setup error；
- setup 3使用新的prefix、Plan/session/output取得三份PASS并完成对账。
- candidate closeout index纳入仍由wrapper写入的stdout，造成一项self-capture digest失配；其余129项终态一致。

后来的PASS不覆盖、解释或重命名这些事实。diagnostic不替代formal qualification；setup/operator failure不被提升为产品FAIL。
完整Policy、FactSet、doc290–294与candidate history不因publication而重写。

## 5. 本publication自己的资格链

本发布的tracked scope只允许：

```text
README.md
AGENTS.md
docs/295-r1-fact-relation-stage-applicability-capability-identity-correction-contract-freeze-publication.md
docs/milestones.md
```

文档290–294、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与post-R1计划必须保持
`289b4962…` base bytes。local gates至少包括：

1. 四文件scope、UTF-8 without BOM、LF/final LF、live links、balanced fences、unique headings、条件marker与
   `git diff --check`；
2. doc290–294完整SHA、候选closeout/reconciliation、PR/exact-main gates、全部历史failure与引用seal的重新核验；
3. 声明的Markdown/baseline regression、四格audit report复核与只读repository hygiene。

这些只作publication本地witness，不替代original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR required gates
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc294 / 本文 / milestones observations
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback必须为publication merge exact main创建新的Plan/session/output identity，不能复用#339 candidate observations。
doc294 unchanged full-file bytes必须在独立对账中复核，不改它的历史candidate marker。每个required target恰好选择一份
qualifying PASS；formal non-success数量从完整历史机械导出，不预设N。

## 6. 生效后的停止线

合同冻结只形成private corrected successor semantic authority。下一次必须从新的exact main重新进入CONTROL LOOP，审查
corrected successor feasibility是否仍是最小合法问题；即使可行，也必须另行取得明确implementation authority。

```text
corrected successor feasibility       = NOT_STARTED
correction implementation             = NOT_STARTED / NOT_AUTHORIZED
old composition authorization history = PRESERVED / NOT CONSUMABLE
old composition implementation        = STOP_CONDITION_TRIGGERED
manifest successor                    = NOT_SELECTED / NOT_AUTHORIZED
persistence                           = OPEN / NOT_SELECTED
public Review product                 = NOT_STARTED
```

本文不启动runtime、tests、Schema、RelationSet admission、Slice closure、ReviewSliceSet/Coverage composition、manifest
successor、Evidence/Bundle/publisher、CLI/Workbench/Core、post-R1 Benchmark、R2/R3、CLAIM_FIDELITY、tag或Release，也不把
合同扩张成repository truth completeness、semantic completeness、bug completeness或全仓审查完成声明。

## 7. 当前publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_QUALIFIED_HISTORY
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

最后门闭合以后，本文第1节的`CONTRACT_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
