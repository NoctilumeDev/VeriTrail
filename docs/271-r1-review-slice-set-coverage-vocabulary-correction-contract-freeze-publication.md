# R1 ReviewSliceSet / Coverage vocabulary correction 最小合同冻结发布

日期：2026-10-16

## 1. 发布对象与条件状态

本文只发布[文档 270](270-r1-review-slice-set-coverage-vocabulary-correction-contract.md)定义的最小语义合同
`r1-review-slice-coverage-vocabulary-correction/0.1`。文档 270 的已资格化字节保持不变；其中的 candidate marker保存候选
历史，本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

这些字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、protected merge、
new exact-main 双门、fresh anonymous installed-product observations 与 independent reconciliation 全部闭合以前，事实仍是
qualified contract candidate。合同冻结不授予 public successor、Schema correction、composition implementation、
`ReviewSliceSet` / `CoverageLedger` assembler 或 persistence authority。

| 坐标 | 值 |
| --- | --- |
| vocabulary correction current-state audit | [文档 269](269-r1-review-slice-set-coverage-vocabulary-correction-current-state-audit.md) |
| 语义合同候选 | [文档 270](270-r1-review-slice-set-coverage-vocabulary-correction-contract.md) |
| 候选 PR | [#312](https://github.com/NoctilumeDev/VeriTrail/pull/312) |
| 候选 base | `5ea7b001380e27c3e3a1e54d1675064f8d16b5a0` |
| 候选 final head | `e7231d4cd6ac81ae87053a14d3d344c9c342dda1` |
| 候选 merge / 本发布施工 base | `b6eee45b87efd4ed850cb4e67f34df728dd47c4d` |
| 候选 head / merge tree | `8b1545457067f0c228586655c810785811411409` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义、total branches、authority ceiling 与停止线仍全部由文档 270 定义。本文不增删 terminal class、disposition
family、reason、applicability、denominator owner、stage join、admission、continuation 或 version stop。冻结范围为：

```text
qualified projection-blocked Fact slot
    -> BLOCKED
    -> SEMANTIC_PROJECTION_BLOCKER
    -> UNREPRESENTABLE_EXPECTED_FACT
    -> exact subject / blocker / same-attempt provenance
```

execution failure 继续属于独立 provenance family，不能被改名为 semantic blocker；`NOT_APPLICABLE` 继续位于 denominator
外，`COVERED / MISSING / BLOCKED / UNKNOWN` 继续组成 denominator 内的 qualification semantics。Coverage 只能验证并
无损映射 qualified upstream reason，不能发明、删除、重命名或重解释 blocker，也不能因为 reason 已知而补造 downstream
universe。

Coverage 0.1 Schema、fixtures、vectors、digest domain、历史 Bundle 与 consumer interpretation继续 immutable。文档 270
只冻结 carrier-neutral semantic tuple与显式 successor version stop，不选择 successor version、文件名、Schema shape、
migration、class、runtime 或 persistence Route A/B；“需要不同 identity”不等于 public successor 已设计或存在。

## 3. 候选 source 与远端资格

PR #312 最终只有一个 commit、四个文件：

```text
README.md
AGENTS.md
docs/270-r1-review-slice-set-coverage-vocabulary-correction-contract.md
docs/milestones.md
```

受审 head 与 merge tree 完全相同。merge parents 依次为：

```text
5ea7b001380e27c3e3a1e54d1675064f8d16b5a0
e7231d4cd6ac81ae87053a14d3d344c9c342dda1
```

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #312 original Public CI | [38884545397](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38884545397) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [38887472152](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38887472152) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [38887472143](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38887472143) | 1 | `1/1 SUCCESS` |

exact-main Public CI 的 Review Attention 四格均为 `513 reported / 510 passed / 3 skipped`；不能写成 513 项全部实际
通过。这些门只证明 candidate source 与声明矩阵，没有实现 successor Schema、composition runtime 或 public product。

候选 final local qualification 在 CPython 3.10/3.13、normal/`-O` 四格各为 `36/36 PASS`；11-world carrier-neutral
semantic report 在四格逐字节一致，其 SHA-256 为：

```text
6132507ebe296ce23d6648268038c15ce3cdfe9ed672a6dd3d4f27b882ab4131
```

候选 qualification record SHA-256 为：

```text
15fcc24997c1c7bf533df3c690e2b03ad26ce6c25ec28c4b9761ec14b8b3c41c
```

文档 270 的 qualified full-file SHA-256 必须继续等于：

```text
f205c6dca120d5951565b43c317d8906c9d113bb03fb520b9d9480f0f0e4f7a4
```

## 4. 候选 fresh product observation 与保留历史

候选最终读回只绑定 `main@b6eee45b87efd4ed850cb4e67f34df728dd47c4d`。fresh CPython 3.13 venv 从
`site-packages` 使用 released Core `0.13.0`、GitHub Evidence `0.1.0` 与 Playwright `1.62.0` / matching cached
Chromium；公开 wheels只复用封存下载字节，不冒充新下载：

| Wheel | SHA-256 |
| --- | --- |
| Core 0.13.0 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence 0.1.0 | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

README、doc270、milestones 各自取得一份独立 qualifying PASS；P1/P2 均 `COMPLETE`、Core `PASS`，公开 raw bytes
逐字节等于同一 exact main 的 Git blobs。正式 history 为 `3 PASS / 0 ERROR`，但这不删除 setup 与 proof-facility 首败。

wheel copy、CI watch network、hash expectation、premature adapter freeze 与 README marker selection 的 setup/proof-facility
errors继续保留。独立对账 attempt 1–4 分别保留 key path、cell shape、stale public-byte marker 与 historical diagnostic
marker errors；修正只作用于 proof facility，三个正式 Plan/session/output 与产品产物均未重跑。attempt 5重新复算 installed
Core verdict、Git/public bytes、Bundle、Plan/session/handoff、全部 formal/diagnostic/setup identities、#312 candidate/local/
original/exact-main gates 与上游 117 项 closeout，并取得 PASS：

```text
independent reconciliation = ea125d787f1c1b093ddbef3ef81cdb0f2857e289980efeecd0470b831d1008bb
166-artifact closeout       = f0b6097a573ccddee1fb0e04f7877fc467fe0cb08159a6e380c67ae94389f6f7
```

因此 doc270 已成为 qualified contract candidate。candidate marker、setup/proof-facility errors 与所有上游首败保持自己的
原 identity；本地 checkout 对齐不是事后新增的 qualification gate。

## 5. 本发布自己的资格门

本轮只允许修改 README、AGENTS、milestones 并新增本文。doc270、Coverage 0.1、全部旧合同、runtime、tests、workflows、
Schema、fixtures、Profile、Policy、identity vectors、corpus 与架构资产必须保持本发布 base 字节。

final publication bytes 提交前至少必须取得：

1. 本层声明的 R1 Schema、handoff、Slice join、Markdown 与 hygiene regression matrix；保留实际 counts / skips；
2. exact four-file scope、其余 tracked bytes与 doc270 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件 marker、禁止越权状态与 `git diff --check`；
3. 候选 closeout、independent reconciliation、PR/exact-main terminal gates、全部 retained proof-facility errors 与引用 seals
   的重新核验；只读 repository hygiene，不删除历史证据。

这些是 publication 的本地 witness，不替代 original PR checks。完整资格链为：

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> separately approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc271 / milestones observations
    -> independent Core, source-byte and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback 必须为 publication merge exact main 创建新的 Plan/session/output identity，不能复用 doc270 candidate
observations。doc270 unchanged full-file bytes在独立对账中复核，不改它的 historical candidate marker，也不以 raw
download替代 P1/P2 formal observation。每个 required target恰好选择一份 qualifying PASS；formal non-success 数量从历史
机械导出，不预设 N。

## 6. 生效后的停止线

合同冻结只形成 vocabulary correction semantic authority。下一次必须从新的 exact main重新进入 CONTROL LOOP，分别审查：

1. 显式 successor identity / Schema correction 是否仍为最早合法 seam；
2. successor 是否能够保持 Coverage 0.1 immutable、完整 blocker tuple、four-way terminal semantics与 conservative join；
3. Schema correction完成自己的资格链以后，private composition feasibility 是否仍能在现有 runtime primitives上无损实现。

```text
Coverage successor Schema correction = NOT_STARTED / NOT_AUTHORIZED
composition private feasibility       = NOT_STARTED
composition implementation            = NOT_STARTED / NOT_AUTHORIZED
Language Support persistence          = OPEN / NOT_SELECTED
```

本文不启动 runtime、tests、Schema correction、public carrier、`ReviewSliceSet` / `CoverageLedger` assembler、
Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、其他顶层轨、CLAIM_FIDELITY、tag 或 Release，也不把合同扩张成
repository truth completeness、semantic completeness、bug completeness 或全仓审查完成声明。

## 7. 当前 publication target

本文件进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

最后门闭合以后，本文第 1 节的 `CONTRACT_FROZEN` target才成为事实；随后只允许返回 CONTROL LOOP。
