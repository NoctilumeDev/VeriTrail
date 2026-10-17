# R1 ReviewSliceSet / Coverage Schema correction 最小合同冻结发布

日期：2026-10-17

## 1. 发布对象与条件状态

本文只发布[文档 273](273-r1-review-slice-set-coverage-schema-correction-contract.md)定义的最小语义合同
`r1-review-slice-coverage-schema-correction/0.1`。文档 273 的已资格化字节保持不变；其中的 candidate marker 保存候选
历史，本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

这些字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、protected merge、
new exact-main 双门、fresh anonymous installed-product observations 与 independent reconciliation 全部闭合以前，事实仍是
qualified contract candidate。合同冻结不授予 Schema implementation、composition feasibility / implementation、public
`ReviewSliceSet` / `CoverageLedger` assembler 或 persistence authority。

| 坐标 | 值 |
| --- | --- |
| Schema correction 可行性审计 | [文档 272](272-r1-review-slice-set-coverage-schema-correction-feasibility-audit.md) |
| 语义合同候选 | [文档 273](273-r1-review-slice-set-coverage-schema-correction-contract.md) |
| 候选 PR | [#315](https://github.com/NoctilumeDev/VeriTrail/pull/315) |
| 候选 base | `406aa8ee9440db8738ee2bd3a35aae558dc105c6` |
| 候选 final head | `37af11f8a4efeef1b34ff7a403e55fb924f70303` |
| 候选 merge / 本发布施工 base | `356b930a039783417f8dcd698e7ae49c25fb4615` |
| 候选 head / merge tree | `eaaea3e40a9bf0d9d8fb2a7934f6035a7b555495` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义、total branches、authority ceiling 与停止线仍全部由文档 273 定义。本文不增删 successor identity、字段、
terminal class、disposition family、reason、applicability、denominator owner、stage join、admission、continuation 或 version
stop。冻结范围为：

```text
CoverageLedger child identity = review-coverage-ledger-0.2
blocked carrier               = exact member identity
                              + SEMANTIC_PROJECTION_BLOCKER
                              + UNREPRESENTABLE_EXPECTED_FACT
                              + exact subject / blocker / same-attempt provenance
conformance identity          = r1-review-coverage-ledger-conformance/0.2
manifest role/path            = COVERAGE_LEDGER / coverage-ledger.json
Coverage 0.1                  = immutable historical identity
```

Schema-valid 继续只是必要条件，不拥有 same-attempt provenance、cross-field exclusivity、transition reconciliation 或
admission。manifest 0.1 继续只绑定 exact child bytes/digest，不拥有 child version dispatch 或 semantic admission；unknown
child version 必须 fail closed。`BLOCKED` 仍只承载已资格化 semantic projection blocker，execution failure、missing、unknown
与 out-of-scope 不得被改名为该状态。

Coverage 0.1 Schema、fixtures、vectors、digest domain、历史 Bundle 与 consumer interpretation 继续 immutable。文档 273
选择的 0.2 child identity、文件名、字段和 conformance boundary 不等于对应 Schema、validator、fixture、consumer、manifest
或产品已经存在；本发布也不把 0.2 扩张为 common Schema 或 manifest 的版本声明。

## 3. 候选 source 与远端资格

PR #315 最终只有一个 commit、四个文件：

```text
README.md
AGENTS.md
docs/273-r1-review-slice-set-coverage-schema-correction-contract.md
docs/milestones.md
```

受审 head 与 merge tree 完全相同。merge parents 依次为：

```text
406aa8ee9440db8738ee2bd3a35aae558dc105c6
37af11f8a4efeef1b34ff7a403e55fb924f70303
```

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #315 original Public CI | [38973694059](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38973694059) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [38976364225](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38976364225) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [38976364071](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38976364071) | 1 | `1/1 SUCCESS` |

exact-main Public CI 的 Review Attention 四格均为 `513 reported / 510 passed / 3 skipped`；不能写成 513 项全部实际
通过。这些门只证明 candidate source 与声明矩阵，没有实现 CoverageLedger 0.2 Schema、composition runtime 或 public
product。

候选 local qualification 在 CPython 3.10/3.13、normal/`-O` 四格各为 `45/45 PASS`。semantic witness attempt 1
虽然四格 PASS 且逐字节一致，但未显式覆盖文档 273 声明的全部 corpus identity，因此以
`SEMANTIC_WITNESS_COVERAGE_INCOMPLETE` 保留；fresh attempt 2 只补 proof-facility witness，未修改合同或产品 oracle。

候选 local qualification、original PR qualification 与 terminal seal 的 SHA-256 分别为：

```text
a14e3f3d14f9dec88f93c9b8ba5e8843d1a734f2fbf72aef0bc6c23ff002fd9c
152010510977bd2559281e7c006a7e3b1a7f73c1225349caf3dd0075466f11a2
03814bcdf08b0c229ec6a4f970bd9fd5d7a97a5803d1c69074e82e317ad830a6
```

文档 273 的 qualified full-file SHA-256 必须继续等于：

```text
0fe8f2714333c5802ffaa83b867a5f687d80abbfe78b5351dc7a39d11d41f8ec
```

## 4. 候选 fresh product observation 与保留历史

候选最终读回只绑定 `main@356b930a039783417f8dcd698e7ae49c25fb4615`。fresh CPython 3.13 venv 从
`site-packages` 使用 released Core `0.13.0`、GitHub Evidence `0.1.0` 与 Playwright `1.62.0` / matching cached
Chromium；公开 wheels 只复用封存下载字节，不冒充新下载：

| Wheel | SHA-256 |
| --- | --- |
| Core 0.13.0 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence 0.1.0 | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

README、doc273、milestones 各自取得一份独立 qualifying PASS；P1/P2 均 `COMPLETE`、Core `PASS`，公开 raw bytes
逐字节等于同一 exact main 的 Git blobs。正式 history 为 `3 PASS / 0 ERROR`，但这不删除 diagnostic、setup 与
proof-facility 首败。

只读坐标检查中未引用的 `HEAD^{tree}` 被 PowerShell 误解析、`py_compile` 接收 Windows 不会展开的 `*.py` 字面量，
分别按 `NON_QUALIFYING_OPERATOR_SETUP_ERROR` 保留；两者均发生在产品观察以前，没有修改 repository、adapter 或 oracle。
三个 render diagnostic 与匿名 API preflight 也只拥有 `NON_QUALIFYING` 身份。

independent reconciliation 重新复算 installed Core verdict、Git/public bytes、Bundle、Plan/session/handoff、全部 formal /
diagnostic / setup identities、#315 candidate/local/original/exact-main gates、semantic witness 首败与 119 项 upstream
closeout，并取得 PASS：

```text
independent reconciliation = a4e3ca83e6b298646f789ac1113930f6cc87a1eed5dbbd46fe0e3755b4addb89
120-artifact closeout       = 692a6fda883c37021a90e09da82b93dd356fef58d87489018ee15e11bdde9552
post-closeout terminal seal = 7185e12331f38247bac4c196fd15773326a9d63d803d7bec24cf0877c4db8d4c
```

因此 doc273 已成为 qualified contract candidate。candidate marker、proof-facility / setup errors 与所有上游首败保持
自己的原 identity；本地 checkout 对齐不是事后新增的 qualification gate。

## 5. 本发布自己的资格门

本轮只允许修改 README、AGENTS、milestones 并新增本文。doc273、Coverage 0.1、全部旧合同、runtime、tests、workflows、
Schema、manifest、fixtures、Profile、Policy、identity vectors、corpus 与架构资产必须保持本发布 base 字节。

final publication bytes 提交前至少必须取得：

1. 本层声明的 R1 Schema、handoff、Slice join、Markdown 与 hygiene regression matrix；保留实际 counts / skips；
2. exact four-file scope、其余 tracked bytes 与 doc273 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件 marker、禁止越权状态与 `git diff --check`；
3. 候选 closeout、independent reconciliation、PR/exact-main terminal gates、全部 retained setup / proof-facility errors 与
   引用 seals 的重新核验；只读 repository hygiene，不删除历史证据。

这些是 publication 的本地 witness，不替代 original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc274 / milestones observations
    -> independent Core, source-byte and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback 必须为 publication merge exact main 创建新的 Plan/session/output identity，不能复用 doc273 candidate
observations。doc273 unchanged full-file bytes在独立对账中复核，不改它的 historical candidate marker，也不以 raw
download替代 P1/P2 formal observation。每个 required target 恰好选择一份 qualifying PASS；formal non-success 数量从历史
机械导出，不预设 N。

## 6. 生效后的停止线

合同冻结只形成 Schema correction semantic authority。下一次必须从新的 exact main 重新进入 CONTROL LOOP，分别审查：

1. 有限 CoverageLedger 0.2 Schema implementation 是否仍为最早合法 seam；
2. implementation 能否保持 Coverage 0.1 immutable、完整 blocker tuple、versioned conformance 与 consumer fail-closed；
3. Schema correction 完成自己的独立资格链以后，private composition feasibility 是否仍能在既有 runtime primitives 上无损实现。

```text
CoverageLedger 0.2 Schema implementation = NOT_STARTED / NOT_AUTHORIZED
composition private feasibility           = NOT_STARTED
composition implementation                = NOT_STARTED / NOT_AUTHORIZED
Language Support persistence              = OPEN / NOT_SELECTED
```

本文不启动 runtime、tests、Schema implementation、composition feasibility、public carrier、`ReviewSliceSet` /
`CoverageLedger` assembler、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、其他顶层轨、CLAIM_FIDELITY、tag 或
Release，也不把合同扩张成 repository truth completeness、semantic completeness、bug completeness 或全仓审查完成声明。

## 7. 当前 publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

最后门闭合以后，本文第 1 节的 `CONTRACT_FROZEN` target 才成为事实；随后只允许返回 CONTROL LOOP。
