# R1 ReviewSliceSet / Coverage root binding correction 最小合同冻结发布

日期：2026-10-17

## 1. 发布对象与条件状态

本文只发布[文档 281](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)定义的最小语义合同
`r1-review-coverage-root-binding-correction/0.1`。文档 281 的已资格化字节保持不变；其中的 candidate marker 保存候选
历史，本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_PRECONTRACT_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

这些字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、单独批准的
exact-head protected merge、new exact-main 双门、fresh anonymous installed-product observations 与 independent
reconciliation 全部闭合以前，事实仍是 qualified contract candidate。合同冻结不授予 Schema implementation、composition
feasibility / runtime、manifest successor、public `ReviewSliceSet` / `CoverageLedger` 或 persistence authority。

| 坐标 | 值 |
| --- | --- |
| root-binding current-state audit | [文档 279](279-r1-review-slice-set-coverage-schema-root-binding-current-state-audit.md) |
| correction precontract audit | [文档 280](280-r1-review-slice-set-coverage-root-binding-correction-precontract-audit.md) |
| 语义合同候选 | [文档 281](281-r1-review-slice-set-coverage-root-binding-correction-contract.md) |
| 候选 PR | [#323](https://github.com/NoctilumeDev/VeriTrail/pull/323) |
| 候选 base | `b2725e5069cfca0dde1e120192eb03d47fba8ff9` |
| 候选 final head | `32de8a67a547f521d9272755c5c447e70830ec10` |
| 候选 merge / 本发布施工 base | `e0de7556f4075068dcaaa74fba85dcd756540fa6` |
| 候选 head / merge tree | `4acb6ef897ecd988224fd73078d7b3496fc8c0c2` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义、total branches、authority ceiling 与停止线仍全部由文档 281 定义。本文不增删 successor identity、binding
state、terminal-history projection、root-chain order、digest domain、conformance obligation、manifest compatibility 或
version stop。冻结范围为：

```text
CoverageLedger successor   = review-coverage-ledger-0.3
root binding domain        = veritrail.review.coverage-root-binding/0.1
root chain domain          = veritrail.review.coverage-root-chain/0.1
terminal history domain    = veritrail.review.coverage-root-terminal-history/0.1
conformance identity       = r1-review-coverage-ledger-conformance/0.3
binding states             = ARTIFACT_PRESENT
                           | QUALIFIED_ABSENT
                           | QUALIFIED_UNKNOWN
ordered chain              = FACT_SET -> RELATION_SET -> REVIEW_SLICE_SET
historical 0.1 / 0.2       = immutable
manifest 0.1 negative path = not qualified; successor remains separate
```

Root state不拥有seven-stage denominator、stage status或overall join authority。admitted branch-empty仍是present artifact；
qualified absence不是empty artifact；qualified unknown不能被downstream提升成present或absence。相同semantic bytes、digest或
terminal projection不继承另一个attempt的live claim、one-shot composition或continuation authority。

Schema-valid继续只是必要条件。Schema、manifest、Provider、publisher、caller和digest holder都不能生成root truth；只有
application-owned same-attempt composition可以消费frozen Fact / Relation / Slice terminal history并机械形成ordered root chain。
本发布不证明0.3 Schema、conformance/runtime、manifest successor、negative-world public Bundle或public product已经存在。

## 3. 候选 source 与远端资格

PR #323 最终只有一个 commit、四个文件：

```text
README.md
AGENTS.md
docs/281-r1-review-slice-set-coverage-root-binding-correction-contract.md
docs/milestones.md
```

受审 head 与 merge tree完全相同。merge parents依次为：

```text
b2725e5069cfca0dde1e120192eb03d47fba8ff9
32de8a67a547f521d9272755c5c447e70830ec10
```

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #323 original Public CI | [39036786001](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39036786001) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [39039139791](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39039139791) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [39039139694](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39039139694) | 1 | `1/1 SUCCESS` |

候选 mechanical audit 的 fresh attempt 3在 CPython 3.10.6/3.13.13、normal/`-O`四格全部PASS，canonical report
逐字节一致：

```text
ea4674a6bab1b6b43315fb3ab680d6aa28da18cd5f3913be9ac15eaab39dd269
```

attempt 1使用Python `assert`表达规范检查，`-O`移除了证明义务；attempt 2又只对opaque terminal-history label做
digest。两者分别以`OPTIMIZATION_ASSERTION_PROOF_GAP`和`TERMINAL_HISTORY_PROJECTION_PROOF_GAP`保留，fresh attempt 3
只修证明设施，没有改合同oracle。候选source、final local qualification与original PR qualification的SHA-256依次为：

```text
6262373d6915ef7e7560b3841071c3d622146625627e2843fd4a55b117e4ded2
865ee6ad049bff316b53bb5cb389c015de550b7210d213d311fd0d7c7f290491
5c11599008bce567e5868619caed4b9b71820955d0977198fd1b377be786f3c9
```

文档 281 的qualified full-file SHA-256必须继续等于：

```text
241dc7b5922c981aabb61a1a6a765ed224bdf7ac47a588274a20a9bb3e311eaf
```

## 4. 候选 fresh product observation 与保留历史

候选最终读回只绑定`main@e0de7556f4075068dcaaa74fba85dcd756540fa6`。fresh CPython 3.13 venv从
`site-packages`使用released Core `0.13.0`、GitHub Evidence `0.1.0`与Playwright `1.62.0` / matching cached
Chromium；公开wheels只复用封存下载字节，不冒充新下载。

README、doc281、milestones在fresh setup 2各自取得一份独立qualifying PASS；P1/P2均`COMPLETE`、Core `PASS`，
公开raw bytes逐字节等于同一exact main的Git blobs。setup 1的README diagnostic与formal observation都看到P1/P2完成、
HTTP 200，却因所选marker落在public-render observation window外而得到0次rendered occurrence。该formal identity继续以
`FORMAL_READBACK_ERROR / READBACK_MARKER_SELECTION_SETUP_ERROR`保留，setup 2的三份PASS不覆盖它。

independent reconciliation attempt 1发现上游precontract closeout在枚举artifact时，wrapper stdout仍是空文件；wrapper随后
写入最终JSON，使该stdout成为post-seal mutation。其余181项上游artifact全部匹配，wrapper payload也匹配closeout结论。
该身份以`UPSTREAM_PROOF_FACILITY_POSTSEAL_OUTPUT_MUTATION`保留。fresh reconciliation v2在运行前固定完整输入，只修证明设施，
没有改产品观察、合同oracle或上游语义，并取得PASS：

```text
independent reconciliation = 04045abb14705435747630c0e3095aea2318be8cbf8b6f07d59f4229e155ed4a
188-artifact closeout       = 08f337f9544b732a7221047f313961c2bc254e2763553ca50a3e8c7cfa9a843d
superseded setup 1 seal     = 061adb112664bce302c9e397be949ab81bd1be9a8a4e08aa665a8506d5d95904
```

因此doc281已成为qualified contract candidate。candidate marker、两个mechanical-audit proof gaps、setup 1 formal ERROR、
reconciliation attempt 1 finding与全部上游首败继续保持原identity；本地checkout对齐不是事后新增的qualification gate。

## 5. 本发布自己的资格门

本轮只允许修改README、AGENTS、milestones并新增本文。doc281、doc259–280、全部旧合同、runtime、tests、workflows、
Schema、manifest、fixtures、Profile、Policy、vectors、corpus与架构资产必须保持本发布base字节。

final publication bytes提交前至少必须取得：

1. 本层声明的R1 Schema、handoff、Slice join、Markdown与hygiene regression matrix；保留实际counts / skips；
2. exact four-file scope、其余tracked bytes与doc281 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件marker、禁止越权状态与`git diff --check`；
3. 候选188-artifact closeout、independent reconciliation、PR/exact-main terminal gates、setup 1 ERROR、proof-facility findings与
   引用seals的重新核验；只读repository hygiene，不删除历史证据。

这些是publication的本地witness，不替代original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc281 / 本文 / milestones observations
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback必须为publication merge exact main创建新的Plan/session/output identity，不能复用doc281 candidate observations。
doc281 unchanged full-file bytes在独立对账中复核，不改它的historical candidate marker，也不以raw download替代P1/P2 formal
observation。每个required target恰好选择一份qualifying PASS；formal non-success数量从历史机械导出，不预设N。

## 6. 生效后的停止线

合同冻结只形成root-binding correction semantic authority。下一次必须从新的exact main重新进入CONTROL LOOP，分别审查：

1. 有限CoverageLedger 0.3 child Schema/conformance feasibility是否仍为最早合法seam；
2. manifest negative-world topology是否需要独立successor，且不得与child Schema合并授权；
3. composition runtime是否仍能在现有private history和runtime primitives上无损实现。

```text
CoverageLedger 0.3 Schema implementation = NOT_STARTED / NOT_AUTHORIZED
composition private feasibility           = NOT_STARTED
composition implementation                = NOT_STARTED / NOT_AUTHORIZED
manifest successor                        = NOT_SELECTED / NOT_AUTHORIZED
Language Support persistence              = OPEN / NOT_SELECTED
```

本文不启动runtime、tests、Schema implementation、composition feasibility、manifest successor、public carrier、
`ReviewSliceSet` / `CoverageLedger` assembler、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、其他顶层轨、
CLAIM_FIDELITY、tag或Release，也不把合同扩张成repository truth completeness、semantic completeness、bug completeness或
全仓审查完成声明。

## 7. 当前 publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

最后门闭合以后，本文第1节的`CONTRACT_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
