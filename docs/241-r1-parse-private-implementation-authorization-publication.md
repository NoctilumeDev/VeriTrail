# R1 Parse fulfillment private implementation 实现授权发布

日期：2026-10-09

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 发布基线：`main@35502aa2f605e5654327f9df81d9da7fe81f23cf`，Git tree
> `98a951f93cf5b084fabc8d5c63b77d63aac3a2f8`
>
> 冻结合同：[Parse fulfillment 最小合同 0.1](217-r1-parse-fulfillment-contract.md)
>
> 冻结发布：[Parse fulfillment 合同冻结发布](218-r1-parse-fulfillment-contract-freeze-publication.md)
>
> 可行性审计：[Parse private implementation 可行性审计](219-r1-parse-private-implementation-feasibility-audit.md)
>
> required consumer 修正合同：[M10 Browser 主机 socket 分类修正与发行消费合同](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
>
> required lane 资格发布：[M10 required Starter lane 迁移资格发布](240-m10-required-starter-lane-migration-qualification-publication.md)
>
> 影响层级：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本轮不修改
> runtime、tests、Schema、Profile、Policy、corpus、identity vector、Provider、Fact/Relation/Slice/Coverage、
> Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. CONTROL LOOP 结论

文档 219 已经完成其原始 PR、受保护合入、新 exact-main 双门、fresh installed-product readback 与 independent
reconciliation，因此 `R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED` 仍是 qualified history。
第一次授权候选 PR #243 的 required Starter gate 在公开 Core 0.12.2 consumer 上暴露 host socket 分类缺口；该 PR
保持 `FAILURE / CLOSED / UNMERGED`，没有 rerun，也没有获得 implementation authority。

文档 221–240 随后只闭合该外部 prerequisite：区分 current source、发行与 consumer identity，建立并冻结 M10
correction contract，创建受治理的 `core-0.12-maintenance`，发布并匿名读回 Core 0.12.3，最后把 main required
Starter lane 迁移到该已读回产品。文档 240 的最后门已经闭合，因此
`W1_REQUIRED_STARTER_LANE_MIGRATION_QUALIFIED` 是当前事实；它只恢复重新审查 Parse authorization 的资格。

本轮重新绑定 `main@35502aa2f605e5654327f9df81d9da7fe81f23cf`，复核 frozen Parse contract、文档
219–223、current runtime bytes、并行 PR 与 retained counterexamples。current Review Attention runtime/tests 与文档
219 审计基线保持相同字节，没有出现 exact runtime、denominator、private product、complete reconciliation、
same-attempt continuation 或 Fact-wire stop line 的产品反例。

重新运行 audit-only probes 时发现一项证明设施缺口：文档 219 保存的 matrix Artifact 把 source literal `文本`
损坏为 `�ı�`。fresh probe 固定 stdout 为 UTF-8 后恢复 exact literal；四格 decision projection 与文档 219 声称的
accepted/rejected、canonical reason、runtime rejection、falsifier、closure 和 attempt isolation 全部相同，execution-cell
canonical report 也与旧摘要逐字节相同。该差异归类为 `OUTPUT_ENCODING_CORRUPTION / EVIDENCE_TOOLING_ERROR`，
不改写旧 Artifact，不冒充复现旧 matrix digest，也不构成 product runtime 或 feasibility claim 反例。

因此当前最小合法下一刀仍是文档 219 第 8 节的 private A–H implementation。合同冻结、可行性审计、W1 资格与
本轮 re-audit 都不自动授予施工权；本文只条件化发布这一项有限 authority。本文自己的最后门闭合以前，runtime
继续 `NOT_STARTED / NOT_AUTHORIZED`。

## 2. 首次授权候选与 prerequisite 修正历史

第一次授权候选 PR #243 的身份固定为：

```text
base = 23f9825e61791a78056d5154e4dfd3626a1167b1
head = c28860fb2b3acd21c15216e3c7a69e3b3e573f16
state = CLOSED / UNMERGED
Public CI 36449716998 attempt 1 = 10/11 SUCCESS + 1 FAILURE
failed job = Starter PASS/FAIL golden path
```

该失败不能由本候选重开、rerun 或解释成 PASS。文档 221 的边界审计证明 required gate 消费的是冻结的 public
Core v0.12.2 wheel，current-source narrow fix 不能修复该世界；因此 #243 的 authorization target 没有生效。

后继 M10 链没有修改 Parse contract/runtime。最终 W1 资格发布 PR #276 的 exact coordinates 为：

```text
base  = 594f1b10c2e441b7e73bd607d4d3d2623afd3704
head  = 4c4d4ceaef6c7e837f4cfd75fa4b7fb007efcd1e
merge = 35502aa2f605e5654327f9df81d9da7fe81f23cf
tree  = 98a951f93cf5b084fabc8d5c63b77d63aac3a2f8
```

原始与 exact-main 门均在 attempt 1 成立：

| 门 | Run | 结果 |
| --- | --- | --- |
| PR #276 Public CI | `37872621305` | `11/11 SUCCESS` |
| exact-main Public CI | `37874646050` | `11/11 SUCCESS` |
| exact-main Browser Smoke | `37874646030` | `1/1 SUCCESS` |

README、doc223、doc239、doc240、milestones 与 AGENTS 使用六个 fresh Plan/session/output 取得 Core `PASS`；六份
anonymous raw source bytes 逐字节等于 exact Git blobs。独立 normal / `-O` reconciliation 逐字节相同：

```text
sha256_json  = 4cbb0d6454ba266e46635884f1d714980a4e21286006f8ab48f43c164f9694bd
sha256_bytes = 2e4b63e2ac0ba811303cb95ea2a5d50ed27a9766473fa23d9ab198efbb3017b1
```

doc223 第一次正式 readback 的匿名 API `COLLECTION_BUDGET_EXHAUSTED` 与 render network error，以及 AGENTS 第一次
正式 readback 的 render network error / root cause `UNKNOWN`，均永久保留为 nonqualifying `ERROR`；后继 fresh
PASS 没有删除、覆盖或解释它们。

## 3. current exact-main re-audit

current exact main 的相关 frozen docs/runtime bytes 与文档 219 基线一致：

```text
eb16303547bad45eb3f22b8209c0e6b46c681495f42bb0c8810666787235264f  docs/217-r1-parse-fulfillment-contract.md
a977cb22e73c812c5e081180f811d740de0a8b874a7239c82c201ab720f42b9a  docs/218-r1-parse-fulfillment-contract-freeze-publication.md
8fcecd73274e0c1d54021a7862e8d34ad68ceb6ae4f5f697e6c2fb17135bf774  docs/219-r1-parse-private-implementation-feasibility-audit.md

7705ba4b4a9d91697ba9a5c5e31d868b88fb22d9b4ba37fdb7ee8e188081c259  plugins/review-attention/src/veritrail_review/_source_operation_gate.py
c90412ec2218110350dc7fef87ad8292113ffc550ec770eddb9ea46bae852af3  plugins/review-attention/src/veritrail_review/_windows_execution_cell.py
e774cdba9cc3a2820c58e1806f76ec066558b9b07260f6558a564e91e08ebca5  plugins/review-attention/src/veritrail_review/_language_support.py
70286924c2590c1acfc494a52bfa800e3777c6cd8f80993045abad90339f5ace  plugins/review-attention/src/veritrail_review/_language_support_values.py
eeb82823563aeb7460cd06eec4cec08091e7342fdc74d251ed5f2a35234e0dbd  plugins/review-attention/src/veritrail_review/_source_operation_fact_application.py
252f8018404c294daffecedb74519203dce33fb6b734ce99cd9405db0b82b4f9  plugins/review-attention/src/veritrail_review/_source_operation_fact_worker.py
```

audit-only scripts 仍为文档 219 的 exact bytes：

```text
4e129e42039c0ed5f0170828a9d038ac941e7289a072b4d211c0c4081018bb7f  parse_reference_worker.py
6b6957d7506441735ed87fe41547c7f3e63fed6b78a869fd9dbfe56a79f42fa5  feasibility_matrix.py
2980ce3c1ca935514c9713a3fbf57b2efd67b03c326347df0a46c6127d211872  cell_probe.py
```

explicit reference executable 仍为 CPython 3.10.6，SHA-256 为
`32ce1d2650ea8b9d394f5b8f94677d27888dccdc3713365bf903a8c465c9d776`；另一格为 CPython 3.13.13。

第一次 re-audit attempt 在 product mutation 前以
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xce in position 6702` 停止。它保留为
`EVIDENCE_TOOLING_ERROR`，部分输出不复用。全新 attempt 2 清理 `PYTHONPATH/PYTHONHOME` 并显式设置
`PYTHONIOENCODING=utf-8 / PYTHONUTF8=1`；CPython 3.10.6 / 3.13.13、normal / `-O` 四格结果为：

```text
matrix canonical bytes = 11227
matrix sha256          = 69f02e873765c2e30fe88c3b77119628554718df245f99f283b06b3a726f3477

cell canonical bytes   = 2004
cell sha256            = dd35740dababf2a8113b4d788f28129584934603b0e5795ae119b45edff8aa8e
```

四格各自逐字节一致。与旧 matrix 比较仅有一个 structural difference：accepted literal 从旧 Artifact 的 `�ı�`
恢复为 exact `文本`；文档 219 的 decision-claim projection 完全相同，projection SHA-256 为
`873987b227771c67119bc100e95708793db9523ec1c56eed0ebe88597d3082fe`。保留的本地审计 Artifact：

```text
comparison.json          745478e5e23654c50def476d57be35f2eba311c6d788a012df4ac9b9ed346dc5
attempt2-manifest.json    1cecf765d3f4679bf41165d39420bdbad1a6513d89bc71aa1cc6e61b9632a17b
observation-history.json  a0b147fb4c11f6035ecbbe62786fcff73f03be101903b12febba67a70424534c
```

本节只重新资格化文档 219 已声明的 feasibility claims。它没有把 audit-only corpus 提升为 public conformance
suite，也没有授权修改 probe、runtime 或 frozen contract 来追求旧错误 digest。

## 4. 发布的有限 authority

本文最后门全部成立后，下一分支只允许实现文档 219 第 8 节已经审计的 private stages：

```text
A. exact input / classification / blob-history revalidation
B. exact ELIGIBLE denominator + frozen decode construction
C. explicit CPython 3.10.6 runtime capability and per-subject one-shot claims
D. contained reference worker request / terminal and private canonical product
E. semantic result / lifecycle / infrastructure failure separation
F. missing / duplicate / dangling / foreign-attempt / cross-world reconciliation
G. application-owned admitted product / product-set semantic identity and copy-owned access
H. attempt-bound one-shot continuation + PFCT-000..016 hardening
```

实现 authority 继续受以下约束：

1. 新对象与函数保持 `veritrail_review` private，不进入顶层 exports、CLI、entry point 或 plugin discovery；
2. denominator 只能来自 exact Language Support `ELIGIBLE` subjects；parser、Provider 与 caller subset 不拥有分母；
3. reference runtime 必须由 controller 以显式绝对路径选择并绑定本次 prepared attempt；不得使用 ambient
   `sys.executable`、PATH、`py` launcher、host feature emulation 或自动下载；
4. worker 必须要求 exact CPython 3.10.6，并只产生 candidate semantic result；version/descriptor 自报不能单独建立
   trusted runtime authority；
5. application 必须独立验证 lifecycle、terminal、binding 与完整 denominator，之后才能 admission product set；
6. reference runtime absence、启动/worker/terminal/release/timeout/resource failure 不得伪装 `PARSE_ERROR` 或空闭包；
7. private canonical product/product-set 可以形成 same-attempt semantic identity，但不是 public Artifact、Evidence、
   receipt、Coverage denominator 或 historical persistence；
8. continuation 必须 one-shot 绑定原 `BudgetContext`、parent eligibility、exact classification、全部 child claims、
   complete reconciliation 与本次 product-set binding；
9. current Fact projection/request/wire、Provider scheduling 与 product-use enforcement 保持原字节。

这项 authority 只允许开始实现，不预先声明实现正确、完成、合入、exact-main verified 或 frozen。

## 5. 不授权的邻接能力

```text
current Fact projection/request/wire changes
Fact Provider scheduling or Parse product-use enforcement
zero-accepted required-provider behavior
historical/offline product persistence Route B
public Parse Schema / carrier / corpus / identity vectors
runtime download / installation / signing / attestation
Fact fulfillment or obligation-universe derivation
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root / Bundle
CLI / Workbench / Core / Q / O / T runtime
DECLARED_CLAIM_FIDELITY / objective-obligation-inference drift
tag / Release
```

尤其：

```text
PRIVATE_IMPLEMENTATION_ALLOWED
    != implementation started
    != parser integration completed
    != current Fact consumer corrected
    != persistence selected
    != Coverage authorized
```

## 6. 实现必须继续面对的反证

文档 219 的 `PFI-000..016` 全部继续约束 implementation。至少必须直接证明：

- equal exact inputs、classification 或 product bytes 不继承另一 attempt 的 claim/continuation；
- runtime unavailable 与 lifecycle failure 不生成 semantic result；
- one child completion 不关闭 parent denominator；
- missing、duplicate、dangling、foreign-attempt、cross-world 与 post-construction mutation fail closed；
- zero denominator 与 all-rejected complete identity 不同，且二者都不自动形成 Fact/Coverage closure；
- current Fact wire 能接收 eligible raw bytes 不证明它有权消费 Parse product；
- finite corpus、descriptor/version response 与 hash equality 都不能替代 owner-side validation。

若 implementation 审计发现 frozen semantics 不能在上述有限边界内成立，必须停止，保留反例，并只显式 reopen/version
被击穿的最小边界；不得以“publication 已授权”为由扩大实现。

## 7. implementation 的后继资格链

implementation 分支形成最终字节以后，仍必须独立经过：

```text
implementation final bytes
    -> implementation layer declared local gates
    -> original PR required checks
    -> protected main merge
    -> new exact-main Public CI + Browser Smoke
    -> required fresh product observation / reconciliation
    -> implementation fact publication
    -> return to CONTROL LOOP
```

本文不预先决定 implementation 的文件布局、private class 名称、test count、public readback surface 或后继 publication
形状。测试是 witness，不拥有扩张 A–H、修改 contract、选择 persistence 或启动 Fact/Coverage 的 authority。

## 8. 本 publication 的最后门

本 docs-only publication 只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。
doc217/218/219、docs 221–240、runtime、tests、Schema、Profile、Policy、corpus、architecture DOT/SVG 与 identity
vectors 必须保持原字节。

提交前必须通过本层声明的双 Python normal/`-O` docs/Schema regressions、relative links、UTF-8 without BOM、
LF/final-LF、heading/fence、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与
`git diff --check`。随后必须完成：

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / doc219 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> conditional authorization state takes effect
```

任一非成功观察都保留原身份；后继 PASS 不覆盖首败。本文中的
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED` 在最后门闭合以前只是一项 target marker，不能授权
runtime branch 提前开始。最后门闭合后也必须先重新绑定新的 exact main 并再次执行 CONTROL LOOP；只有最小
A–H implementation 仍成立时，才可创建 implementation branch。

### 8.1 本地资格结果

第一次 local test invocation 按 installed-product readback 习惯清除了 `PYTHONPATH`；但本层运行的是 source-tree
regression，`tests.test_markdown` 因无法导入仓库内 `veritrail` 在 test module import 阶段停止。其余 37 项虽然执行，
该格保持 `SETUP_FAILURE / NON_QUALIFYING`；它没有产品或文档 mutation，也没有被写成部分 PASS。

全新 attempt 显式把仓库 `src` 与 `plugins/review-attention/src` 绑定为 current-source test roots，并清理
`PYTHONHOME`。candidate bytes 首轮通过：

| Lane | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `40/40 PASS` |
| CPython 3.10.6 `-O` | `40/40 PASS` |
| CPython 3.13.13 normal | `40/40 PASS` |
| CPython 3.13.13 `-O` | `40/40 PASS` |

每格运行 `tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`。independent static
checker 又确认 exact diff scope 为 AGENTS、README、milestones 与 doc241，doc217/218/219 与六个相关 runtime 文件的
九份 SHA-256 连续，relative links、UTF-8 without BOM、LF/final-LF、heading/fence、target markers、敏感路径与
`git diff --check` 均成立。

本节写入后必须从新的 final bytes 重跑同一四格与 static gate；首轮 PASS、后继 final-byte PASS 与 static PASS
各自只作本 candidate 的 witness。
