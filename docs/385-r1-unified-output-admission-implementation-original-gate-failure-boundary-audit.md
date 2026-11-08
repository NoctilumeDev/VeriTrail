# R1 unified Review / Coverage output admission implementation original-gate failure-boundary audit

日期：2026-11-08

> 候选状态：`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@5742c979e671e65067085e0303caf9d3506b7d42`，tree
> `e0a6db65861e19166968b6491f9153ba041eb933`。
>
> 失败对象：PR #436，`base=5742c979e671e65067085e0303caf9d3506b7d42 /`
> `head=1caba94e903ea6151225e96b8ce5dc9d58192be6 / tree=907c4dba7a9eae764627f5484a980fd07ad4dd06`。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只保存并归层一次原始required gate失败；不修改
> runtime、tests、workflow、下载器、恢复预算、Release资产、selector、Fact/Relation/Slice/Coverage、CoverageLedger、
> manifest、Evidence、persistence、public Review、Core Verdict或R2–R6。

## 1. authorization已经独立生效

[文档383](383-r1-application-level-unified-review-coverage-output-admission-private-implementation-authorization-publication.md)
由PR #435以candidate `40a2f537e016477afea16eb2a2d84603692faa0f`精确合入
`main@5742c979e671e65067085e0303caf9d3506b7d42`。original Public CI `42428584420`、exact-main Public CI
`42431241189`与Browser Smoke `42431241097`均attempt 1 SUCCESS（11/11、11/11、1/1），没有rerun。fresh
README/doc382/doc383 Render、AGENTS/milestones raw-byte observation、independent reconciliation与finite closeout全部成立。

```text
independent reconciliation  5f89cf9ba6698cfb99954658e75e1d75a804964198819bb57b0298ca95d60b58
finite closeout              c0276e9bf3b4479a8ff722dfbc7f1645614cd8ad67b939d875ccf8d89f67c17a
finite integrity             4e544e5014694daf2349781f1f7a2f2211eabfde09f046805c4b65271af8f446
```

因此bounded A–J `PRIVATE_IMPLEMENTATION_ALLOWED`是当前exact-main可消费authority。它只授权施工，不证明runtime已存在、正确、
资格化、合入或冻结。`proof_is_not_problem_solving = true`继续把original engineering problem、current proof obligation与
applicability world分离。

## 2. failed candidate与本地证据上限

fresh CONTROL LOOP从该exact main建立PR #436：

| identity | value |
| --- | --- |
| base | `5742c979e671e65067085e0303caf9d3506b7d42` |
| head | `1caba94e903ea6151225e96b8ce5dc9d58192be6` |
| tree | `907c4dba7a9eae764627f5484a980fd07ad4dd06` |
| scope | 1 commit / 10 files |
| original Public CI | run `42468088782` / attempt 1 / `FAILURE` |
| PR disposition | `CLOSED / UNMERGED / NOT_QUALIFIED` |

candidate实现一个versioned private application admission owner、两类exact nominal result的窄live-coordinate hook、独立route/result/
root-chain重验与one-shot commit；public exports、producer semantics、CoverageLedger、manifest、Evidence、persistence、public Review与
R2–R6保持不变。final local witness包括：

- UAO四格各27/27 PASS，matrix SHA-256 `85c72f1991df29a5b0971056ffa57f1afc9302ea34b73e8ce18c5b047997e39c`；
- focused四格各286 reported / 285 passed / 1 skipped，matrix SHA-256
  `70d7e831e1036a9439e31057ab4afe85e1731182c99ba9ecc1f7a133a6bdf3b5`；
- full四格各648 reported，Python 3.10为645 passed / 3 skipped，Python 3.13为646 passed / 2 skipped，matrix
  SHA-256 `57d8a5ed101f4409cd878adb104dc49a3d9d38e4d1f389434736a3aa325d8f88`；
- semantic四格逐字节一致，canonical SHA-256
  `a543fa16316ed9570c467451f66c322f063c6665e06b0ddfd58ebf144af599e1`；
- compile、global/local hygiene、Markdown、exact scope、public exports与primary audit continuity全部PASS；
- 233-artifact post-commit seal SHA-256
  `f158f5e91fe6caf6b7d761328a9567504aaaf1f2bbd144fbe118dd072605f2ec`。

这些只证明local candidate world没有被声明反例击穿。它们不能替代original required gate，也不能与另一attempt或后继candidate拼接。

## 3. original gate的精确失败

run `42468088782` attempt 1绑定exact candidate head `1caba94e…`。终态如下：

| job | identity | conclusion | observed boundary |
| --- | --- | --- | --- |
| Python 3.10 on Windows | `128692177097` | `CANCELLED` | required run已经失败后的原始取消身份；不得改写为PASS或产品失败 |
| Workbench tests, lint, build, and audit | `128692177253` | `SUCCESS` | 只属于同一attempt的成功上下文，不能回填required run |
| E3 0.2 release download acceptance | `128692177263` | `FAILURE` | Core 0.12.0 wheel最终成功；后继E3 immutable asset在显式120秒预算内持续HTTP 504并fail closed |
| Python 3.13 on Windows | `128692177310` | `FAILURE` | Core 0.12.2 immutable wheel在默认60秒预算内持续HTTP 504并fail closed |
| downstream matrices | run-owned identities | `SKIPPED` | required predecessors未成功；不得冒充未执行的PASS |

下载失败均终结为：

```text
release asset recovery budget cannot fund the next bounded retry
after retryable_http status=504
```

failure capture、failed log、failure boundary与248-artifact boundary seal SHA-256为：

```text
66de41a7a3671b6ac6c15d958ede7f9e4a1a350042d97683203331690a2460b7
01581b75c139cfa34062ab3c8047e9fd731beb82738360651610a7a329aa63e5
6c3a8a04b56fbbe103aeab8168649bea9b403777e93696d34714ede9975ef662
2e599f998ba615b4c7dc43a893b4c4191ef33e756a791ab1d29fd0d85c9d0715
```

run、失败job、取消job、跳过job、setup errors、完整日志和`UNKNOWN`归因全部保留；没有rerun。

## 4. 归层与归因上限

当前证据只允许：

```text
required original gate failure                    ESTABLISHED
classification                                    RELEASE_ASSET_HTTP_504_RECOVERY_BUDGET_EXHAUSTED
release asset HTTP 504 recovery budget exhaustion ESTABLISHED
download tool fail-closed behavior                 CONFORMING
asset digest mismatch                              NOT_OBSERVED
candidate regression                               NOT_ESTABLISHED
subject failure                                    NOT_ESTABLISHED
workflow/runtime/test/oracle drift                 NOT_ESTABLISHED
underlying GitHub/proxy/shared-egress/network cause UNKNOWN
```

[冻结恢复策略](98-release-download-recovery-correction.md)要求有限绝对deadline、窄重试集合、owned partial清理、摘要相等后才发布；
[multi-asset lane修正](357-release-download-multi-asset-lane-budget-correction.md)明确说明120秒不保证覆盖未来任意外部中断。当前日志没有显示
错误字节被接受、digest mismatch被忽略、partial被发布或deadline owner失效。因此本观察击穿#436 qualification，不足以击穿下载器
fail-closed语义或授权扩大为无限重试。

不得把“后继时间点可能恢复”写成当前attempt PASS；也不得把“外部失败”写成required gate可跳过。资格失败与产品回归是两个不同身份。

## 5. 最小边界与禁止事项

本候选只允许：

```text
README.md
AGENTS.md
docs/385-r1-unified-output-admission-implementation-original-gate-failure-boundary-audit.md
docs/milestones.md
```

明确禁止：

- 修改#436 candidate、runtime、tests、workflow或下载器；
- 修改60/120秒预算、重试集合、Release URL/asset name/frozen SHA-256或required gate；
- rerun/reopen/merge #436，或把后继PASS回填其original run；
- cherry-pick旧candidate并继承local/original qualification；
- 删除、覆盖或重命名FAILURE/CANCELLED/SKIPPED/setup/UNKNOWN identity；
- 修改primary `audit.json`；
- 启动manifest、same-attempt Evidence continuity、persistence、public Review、Core Verdict或R2–R6。

## 6. 本audit自己的资格链

final bytes必须复核exact four-file scope、UTF-8/LF/final LF、links/fences/headings、required markers、`git diff --check`、
global/local hygiene、focused四格、#435 authority chain、#436 original failure identity、frozen download-recovery bytes、open PR/remote main、
primary audit continuity与全部retained non-success。

当前local candidate已经取得：

- Python 3.10.6 / 3.13.13 × normal / `-O` focused四格各259 reported / 258 passed / 1 skipped，matrix
  SHA-256 `6a0eed4b824a4ef14227c3bd90489ad83aa1d6a8fb166beb3a0c8f8a0a713a68`；
- global/local hygiene 8/8 PASS，matrix SHA-256
  `b8dd56dc5e0b0f26c932c78472b5a52a6667092f632651dc35fe659e3c08b7de`；
- four-file Markdown/scope/frozen-byte/failure-identity/primary-audit validation PASS，851个local links；attempt 1因正文未使用
  canonical classification token而停止，按proof-target setup error保留；正文只补入同一分类token，没有修改产品、oracle或归因。

这些仍是local candidate witness，不是original PR、protected merge、exact-main或readback资格。

```text
final four-file audit bytes / declared local gates
    -> original PR required gates (new attempt identity; no rerun of #436)
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent source/failure/problem-identity reconciliation
    -> finite closeout/integrity
    -> ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

README/本文使用fresh Render diagnostic+formal；AGENTS/milestones使用anonymous raw/Contents API/exact-Git全字节对账，不把超过Render
window的完整milestones注册为Render target。任何non-success保留原identity并停止，不重复已有PASS。

## 7. 当前状态与后继停止线

本文全部最后门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_CANDIDATE_PR436_CLOSED_UNMERGED_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`ORIGINAL_GATE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。#436继续保持closed/unmerged/not-qualified；
authorization继续有效，但没有runtime主线事实。随后必须返回CONTROL LOOP，从新的exact main机械重建implementation candidate bytes并取得
新的local/original/merge/exact-main/readback/reconciliation资格。后继candidate可以重现相同语义，但不能继承#436的attempt、PASS或FAIL。

`proof_is_not_problem_solving = true`：失败归层不是实现完成，后继门全绿也不能回填旧失败；只有新的exact-main runtime与产品读回
闭合以后，原工程问题才可能进入已解决状态。
