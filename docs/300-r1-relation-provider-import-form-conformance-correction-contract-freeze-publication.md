# R1 Relation Provider import-form conformance 修正合同冻结发布

日期：2026-10-20

## 1. 发布对象与条件状态

本文只发布[文档 299](299-r1-relation-provider-import-form-conformance-correction-contract.md)定义的
`r1-relation-provider-import-form-conformance-correction/0.1`最小语义合同。文档 299 的已资格化完整字节保持不变；
其中的`CONTRACT_CANDIDATE` marker保存候选历史，本发布自己的最后门全部闭合后才由本文承担当前冻结状态。

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED

R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_AUTHORIZED

R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

这些字节目前只表达publication target。本文自己的final-byte local gates、original PR qualification、连续授权的
exact-head protected merge、new exact-main Public CI与Browser Smoke、fresh anonymous installed-product readback及
independent reconciliation全部闭合以前，事实仍是qualified contract candidate。合同冻结不授权corrected Provider successor
implementation，也不恢复旧composition，不选择manifest successor、persistence或public Review产品。

| 坐标 | 值 |
| --- | --- |
| correction feasibility qualified history | [文档 298](298-r1-relation-provider-import-form-conformance-correction-feasibility-audit.md) |
| semantic contract candidate | [文档 299](299-r1-relation-provider-import-form-conformance-correction-contract.md) |
| candidate PR | [#344](https://github.com/NoctilumeDev/VeriTrail/pull/344) |
| candidate base | `85bb22896b978b6f9480b58681c69c5b5ac10c55` |
| candidate final head | `fbf4975202327ed22b7fd2ab02de0bd33f5b751c` |
| candidate merge / publication construction base | `79be6a2af95a51e01318acc7f41b38100e658197` |
| candidate head / merge tree | `dcf629073890844f99f60d1167e1d17c51871c16` |
| publication impact | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范函数、authority owner、falsifier与停止线仍全部由文档 299 定义。本文不新增或修改Python class、field、private carrier、
public Schema、manifest、Profile、Policy、Relation family、Provider responsibility或Coverage semantics。冻结范围只有：

```text
complete authoritative FactSet F
    + complete accepted product/path source bytes
    + unchanged Fact identity and digest

versioned CPython 3.10.6 alias-occurrence projection X
    + Import / ImportFrom
    + multiple aliases / relative / star / nested / multi-path

bidirectional exact binding
    F_R <-> X
    no missing / duplicate / extra / cross-path / semantic drift

application-owned complete assignment A_p
    + exactly one terminal outcome per assigned obligation
    + no foreign or omitted outcome

legacy narrow-world byte compatibility
    + collision-free extension ordinal space
    + new private Provider algorithm / descriptor identity

same-attempt Fact handoff claim
    + original BudgetContext / deadline / stop / revocation state
    + application qualification and admission authority
```

完整FactSet与sealed Policy始终保持；Provider只消费application已经分配的obligations，不拥有applicability、denominator、
qualification或admission。source occurrence与authoritative Fact必须双向、一一对应；只证明emitted occurrence可追溯，或只证明
Fact有匹配项，都不足以证明完整性。Provider `COMPLETED`、candidate数量正确或某个relation family成功，也不能自行证明
complete assignment execution。

legacy top-level single-alias `ast.Import`继续保留既有`body_ordinal`与canonical candidate/outcome bytes。expanded forms使用
独立extension ordinal space和新的private Provider identity；不能closest-version fallback，也不能在旧identity下静默扩大语义。
相同source、FactSet digest、semantic result或limits均不继承另一个attempt的claim、ProviderRun、terminal history、admission或
continuation。

## 3. 合同候选 source 与资格链

PR #344最终只有一个commit、四个docs-only文件：

```text
README.md
AGENTS.md
docs/299-r1-relation-provider-import-form-conformance-correction-contract.md
docs/milestones.md
```

受审head与merge tree完全相同；merge parents依次为candidate base与final head。公开门均为原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #344 original Public CI | [39293777777](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39293777777) | 1 | 11/11 SUCCESS |
| exact-main Public CI | [39297621450](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39297621450) | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | [39297621269](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39297621269) | 1 | 1/1 SUCCESS |

候选local qualification绑定四文件终态、Markdown/link/hygiene及Python 3.10 / 3.13 × normal / `-O` focused regression；
每格均为`61/61 PASS`。exact main随后对README、doc299与milestones各取得一份fresh installed-product
`FORMAL_READBACK_PASS`；三者均为P1/P2 `COMPLETE`、Core `PASS`，Plan、session、handoff与output identities互不复用。

readback facility setup 1未取得本地merge object且PowerShell wildcard / reserved variable使用错误，作为独立setup failure保留。
setup 2在pre-observation adapter freeze以后发现setup history尚未初始化；该设施首败、两份已经产生但未能自动登记的diagnostic
identity、随后fresh anonymous rate exhaustion与全部后继诊断均保留。正式产品观察直到fresh exact-commit preflight可用以后才开始，
没有在已知额度耗尽时制造formal ERROR。

independent reconciliation attempt 1使用readback summary中不存在的`final_report_verdict`字段，终结为
`RECONCILIATION_PROOF_FACILITY_SCHEMA_KEY_ERROR`。attempt 2只把metadata读取修正为实际发出的`verdict`字段；新的harness与输入
在运行前独立冻结，没有改动产品oracle、三份formal observation、target、marker、预算、断言或状态规则。attempt 2重新验证Core、
Git/public bytes、Bundle、三份formal identity、候选source/PR资格、doc298的142项qualified history和全部保留setup/diagnostic history：

```text
independent reconciliation attempt 2
fdc062209a0943c884bca364ebe38dcc020a6a450159dc54c44b56d4d67be207

153-path closeout index
4ad67ab029611b00432addbb727523565c116ad0bcdc8d4816560d95fc5f2455

doc299 full-file SHA256
3ac477d8f5278983a5b4b0d672772d23cf356d102f6c1ffa4419ae608db42fb6
```

本publication本地复算该closeout index时发现一项proof-facility self-capture：索引创建时把仍为空的
`create-closeout-attempt-1.stdout.txt`记为empty digest，wrapper随后向同一文件写入121 bytes终态回显；其余152项逐项一致。
该stdout只回显closeout自身的result、count与hash，不是independent reconciliation输入。因此候选资格继续由先前完成的
reconciliation、三份formal PASS与152项稳定artifact支撑；本文保留该finding，不把153-path index叙述为153项全部终态封存。

因此文档 299 只是qualified contract candidate；这些证据不替代本publication自己的资格链。

## 4. 保留失败与边界

修正可行性审计、合同候选及其readback继续保留下列不同身份：

- 文档298的candidate source attempt 1 setup error、README marker selection setup error与doc298 anonymous API
  rate-exhaustion formal ERROR；
- PR #343 original Public CI中因GitHub官方incident延迟的同一attempt jobs；没有创建替代run identity；
- 合同候选readback setup 1的local object、PowerShell wildcard与reserved variable bootstrap errors；
- setup 2的setup-history initialization error、已经生成但自动登记失败的两个diagnostics，以及fresh rate-exhaustion diagnostics；
- independent reconciliation attempt 1的summary metadata key错误；attempt 2保留其identity后才PASS。
- candidate closeout index纳入仍由wrapper写入的stdout，造成一项self-capture digest失配；其余152项终态一致。

后来的PASS不覆盖、解释或重命名这些事实。diagnostic不替代formal qualification；setup/operator/proof-facility failure不被提升为
产品FAIL。完整Policy、FactSet、doc290–299与candidate history不因publication而重写。

## 5. 本publication自己的资格链

本发布的tracked scope只允许：

```text
README.md
AGENTS.md
docs/300-r1-relation-provider-import-form-conformance-correction-contract-freeze-publication.md
docs/milestones.md
```

文档175、290–299、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与post-R1计划必须保持
`79be6a2…` base bytes。local gates至少包括：

1. 四文件scope、UTF-8 without BOM、LF/final LF、live links、balanced fences、unique headings、条件marker与
   `git diff --check`；
2. doc299完整SHA、candidate closeout/reconciliation、PR/exact-main gates、全部历史failure与引用seal的重新核验；
3. 声明的Markdown/baseline regression、focused four-cell regression复核与只读repository hygiene。

这些只作publication本地witness，不替代original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR required gates
    -> continuously authorized exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc299 / 本文 / milestones observations
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback必须为publication merge exact main创建新的Plan/session/output identity，不能复用#344 candidate observations。
doc299 unchanged full-file bytes必须在独立对账中复核，不改它的历史candidate marker。每个required target恰好选择一份
qualifying PASS；formal non-success数量从完整历史机械导出，不预设N。

## 6. 生效后的停止线

合同冻结只形成private Provider conformance correction semantic authority。下一次必须从新的exact main重新进入CONTROL LOOP，
审查corrected successor feasibility是否仍是最小合法问题；即使可行，也必须另行取得明确implementation authority。

```text
corrected Provider successor feasibility = NOT_STARTED
corrected Provider successor runtime     = NOT_STARTED / NOT_AUTHORIZED
old corrected-successor authorization    = ALLOWED_HISTORY_PRESERVED / NOT_CONSUMABLE
old composition implementation           = STOP_CONDITION_TRIGGERED
manifest successor                       = NOT_SELECTED / NOT_AUTHORIZED
persistence                              = OPEN / NOT_SELECTED
public Review product                    = NOT_STARTED
```

本文不启动runtime、tests、Schema、RelationSet admission、Slice closure、ReviewSliceSet/Coverage composition、manifest
successor、Evidence/Bundle/publisher、CLI/Workbench/Core、post-R1 Benchmark、R2–R6、CLAIM_FIDELITY、tag或Release，也不把
合同扩张成repository truth completeness、semantic completeness、bug completeness或全仓审查完成声明。

## 7. 当前publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_AUTHORIZED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合以后，本文第1节的`CONTRACT_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
