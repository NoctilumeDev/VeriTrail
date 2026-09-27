# R1 Language Support eligible operation projection / same-attempt gate 实现冻结发布

日期：2026-09-28

## 1. 文档身份与条件状态

> 状态目标：`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 208](208-r1-language-support-eligible-operation-projection-contract.md)
>
> 合同冻结发布：[文档 209](209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)
>
> 实现冻结候选：[文档 210](210-r1-language-support-eligible-operation-projection-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@e69ff64333300fc01bd89eb3dfbe69f447048b40`
>
> 候选合入 Tree：`cbf4e9597e1e719f7388080d788c5e40afc0f8e9`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 208 A–G private implementation 已完成施工、逐 stage 进入受保护 main、候选资格化，并且
候选自己的 new exact-main 双门、fresh anonymous installed-product readback 与 independent reconciliation 已经成立。
本文不创建或修改 runtime、tests、Schema、Profile、Policy、corpus、identity vector、wire、operands、request、
controller、Provider、Parse、AST、Fact、Relation、ReviewSliceSet、Coverage、Evidence、Manifest、publisher、Bundle、
CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文自身仍须完成 final bytes local gates、original PR required checks、受保护主线合入、新 exact-main Public CI /
Browser Smoke，以及针对本文合入坐标的 fresh anonymous installed-product readback 与 independent reconciliation。
只有这些最后门全部成立，状态目标才成为当前主线事实；在此以前，本分支中的 frozen marker 只是 publication
target，不授权后继施工。

## 2. 本次冻结的最小对象

本次只冻结以下 private、attempt-bound、non-published input-authority closure 的实现事实：

```text
copy-owned exact DerivationInputSet
        ↓
r1-language-support-parse-operation-projection/0.1
attempt-neutral eligible-only operation projection
        ↓
original BudgetContext + parent AttemptEligibility
        ↓
one-shot child eligibility / same-attempt claim
        ↓
Fact 0.2 / operands 0.4
Relation derivation 0.3 / operands 0.5
Relation observation 0.4 / operands 0.6
        ↓
three controller integrations
        ↓
downstream exact-history revalidation
        ↓
LSPC-000..018 hardening
```

Provider-visible source bodies 必须与 stage operation set 恰好相等；unsupported、out-of-scope 与 mixed-world
body 必须在 encoding 前被排除。旧 wire 不得 fallback，新 wire identity 不得伪装旧历史。相同 semantic
projection、相同 classification、相同 budget limits 或相同-looking request 都不继承另一次 attempt authority。

合法 empty projection 只证明该 stage 没有 Provider-visible body；既有 applicability 仍须运行真实 empty-body
child。该 world 不生成 Parse terminal、Fact fulfillment、Coverage、`CLOSED_EMPTY` 或 public closure。

## 3. Implementation 与候选精确链

文档 208 A–G implementation 由 PR #223–#229 串行形成。每个 stage 都以独立 implementation commit、original
Public CI、ordinary merge 与 new exact-main Public CI / Browser Smoke 取得自己的资格；没有 stage 继承前一 stage
的绿色。最终实现坐标是：

```text
implementation exact main = b69527ec3a4c3037be730144c29b0ce2468940fc
implementation tree       = 03e564bd0aef728d023ad0b93d539067c7ac8ac7
```

完整 A–G implementation diff 相对合同冻结主线只触及 28 个 Review Attention private runtime/test 文件，
`8365 insertions / 83 deletions`；没有 public export、Schema、Profile、Policy、corpus、architecture asset、publisher、
Bundle 或 Workbench 变化。G exact-main 的四格都取得 G direct `20/20`、A–G focused `100/100`、related matrix
`182/182` 与 full Review Attention `417/417`。canonical hardening report 四格 SHA-256 均为：

```text
dc6ef339570c83af99e7882c3de703ea51e9df91c5b0fd9265bc1b65cbc9ca22
```

文档 210 候选精确链为：

```text
candidate base  = b69527ec3a4c3037be730144c29b0ce2468940fc
candidate head  = 91cda857de363ea82b5866d9870f49cc8e58ab46
candidate merge = e69ff64333300fc01bd89eb3dfbe69f447048b40
candidate tree  = cbf4e9597e1e719f7388080d788c5e40afc0f8e9
merge parents   = b69527ec3a4c3037be730144c29b0ce2468940fc
                  91cda857de363ea82b5866d9870f49cc8e58ab46
```

[PR #230](https://github.com/NoctilumeDev/VeriTrail/pull/230) 只有一个 commit、四个文件，`349 insertions /
6 deletions`；original [Public CI run 36334206045](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36334206045)
在 attempt 1 取得 11/11 SUCCESS，没有 rerun 或后继 push。候选以 ordinary merge commit 合入受保护 main，
candidate 与 merge tree 相同。该 exact candidate main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| Public CI | [36335678882](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36335678882) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [36335678884](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36335678884) | 1 | `1/1 SUCCESS` |

## 4. 候选 fresh anonymous installed-product readback

读回从 detached exact `main@e69ff64...` 建立 source coordinate，并在 fresh CPython 3.13.13 venv 中安装固定
Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件均从该
venv 的 `site-packages` 导入；`GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 均清空。

三个正式观察在 observation 前保存独立 sealed Plan，并使用互不复用的 Plan ID、session 与 output root：

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-lspg-impl-cand-readme` | `github-paired-c3159a5dff05418d98283f9db0a103c5` | `fab28ab5780e571d8f526178dd24f919f620d10e293da6a02bfc03402d8ed120` |
| 文档 210 | `r1-lspg-impl-cand-doc210` | `github-paired-a40f33144f654f4d80f3e1f404559409` | `d8a3fc792f470cf3a53fd1ed79b9cf90368cb8ed7e15a796c11bd641578674ec` |
| milestones | `r1-lspg-impl-cand-milestones` | `github-paired-592f73ec7bc9412fbeb9187293b6b60f` | `b17b15f2a97c0cd931906ba36abf5a6ef6f16f0fc71b57d32a394ddc7f487a69` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、预注册 marker 恰好一次、零 error/conflict/
coverage reason/cleanup error/active stream，Core 为 `PASS`。文档 210 的中文 marker 在 PTY 中显示乱码；runner 与
independent verifier 直接读取 canonical JSON 并按 Unicode code point 比较，stored marker 与预期相同，因此该
显示现象不改变 Artifact bytes 或 Verdict。

AGENTS、README、文档 210 与 milestones 又做 anonymous exact-SHA raw-source 下载，四份文件均逐字节等于 exact
Git blobs。raw-source check 只作 byte reconciliation，不冒充 P1/P2 Evidence 或替代指定消费路径。

## 5. 独立 reconciliation 与保留的 setup observation

联合 verifier 独立验证三个 sealed Plan、P1/P2 Evidence、handoff、report 与摘要 digest，并重新 import handoff 后
调用已安装 Core 复算 adjudication fields。它同时核对：

- 三组 Plan/session/output identity 不复用；
- PR #230、candidate head、ordinary merge parents/tree 与四文件 scope；
- PR、exact-main Public CI 与 Browser Smoke 都绑定预期 source SHA、attempt 1 且全部 jobs 成功；
- installed wheel identity 与 architecture asset byte continuity；
- 四份公开 raw bytes 等于 exact Git blobs。

canonical reconciliation manifest 位于仓库外，其摘要为：

```text
sha256_json  = dafb28072bd4d1e7e0969c2a19734101ccd3177d5fd186dd75f41c4d132a32fc
sha256_bytes = d6a8b6eb33ed053144a9d3563615d91edeea56772ff4ae732006e228b1fee5aa
```

正式观察开始前，installed-environment 与 anonymous exact-SHA API preflight 已成功写出且 HTTP 200；Playwright
在解释器 shutdown 时留下 pending-task / `TargetClosedError` warning。该 warning 没有正式 Plan/session/Evidence/
output identity，被保留为 setup history，不是 product observation，也没有被后继 PASS 改写成“没有发生”。

## 6. 已冻结不变量与未授权能力

本次冻结后，以下边界成立：

1. Language Support classification 与 operation projection 都必须从 copy-owned exact inputs 独立重算，caller
   dataclass/type/digest 不能替代 canonical revalidation；
2. classification/projection 是 attempt-neutral semantic fact；它们不拥有 live continuation authority；
3. same-attempt claim 必须绑定 original `BudgetContext` object identity 与 parent/child eligibility，并 exactly once；
4. Provider-visible body set 必须与 operation set 完全相等，且 filter-before-encode；omitted body 不能通过 wire、
   operands、report 或 admission side channel 重现；
5. Fact、Relation derivation、Relation observation 的 corrected wire/operands identity 必须 fail closed，旧 wire 不
   fallback，downstream 必须从 exact history 重算；
6. cancellation、budget exhaustion 与 concurrent claim 保持 fail closed；相同 limits 或相同 semantic result 不
   继承 attempt；
7. private proof 不产生 public carrier、Schema、Evidence、Coverage、publisher 或 Bundle authority。

以下能力继续未授权：

```text
Language Support persistence Route A or B
real parser / AST execution
per-unit Parse terminal fulfillment
Fact projection-universe derivation / fulfillment
shared observation receipt or ledger
public Language Support / Parse / Fact carrier or Schema
ReviewSliceSet / Coverage
Evidence / publisher / Bundle
CLI / Workbench
```

## 7. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 208、209、
210 的规范/历史字节，runtime、tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture DOT/SVG
均须保持原字节。

提交前必须完成本层声明的双 Python normal/`-O` G direct、A–G focused、related matrix、完整 Review Attention 与
docs/Schema regressions，以及 Markdown relative links、fence/heading、状态 marker、UTF-8/LF/final-LF、敏感路径、
exact diff scope、frozen byte continuity 与 `git diff --check`。这些本地门不能替代本发布自己的 original required
checks。

最终 publication worktree 在未改动的 runtime/test bytes 上严格串行完成以下矩阵；记录证据数字后，受文档文字影响的
docs/Schema 与静态门又在最终文档字节上重跑：

| Lane | G direct | A–G focused | Related | Full Review Attention | docs / Schema |
| --- | --- | --- | --- | --- | --- |
| CPython 3.10.6 normal | `20/20` / 46.483s / PASS | `100/100` / 58.342s / PASS | `182/182` / 300.747s / PASS | `417/417` / 568.310s / PASS | `40/40` / PASS |
| CPython 3.10.6 `-O` | `20/20` / 46.438s / PASS | `100/100` / 57.057s / PASS | `182/182` / 296.771s / PASS | `417/417` / 570.234s / PASS | `40/40` / PASS |
| CPython 3.13.13 normal | `20/20` / 47.963s / PASS | `100/100` / 58.555s / PASS | `182/182` / 297.040s / PASS | `417/417` / 562.389s / PASS | `40/40` / PASS |
| CPython 3.13.13 `-O` | `20/20` / 46.790s / PASS | `100/100` / 57.424s / PASS | `182/182` / 298.197s / PASS | `417/417` / 559.748s / PASS | `40/40` / PASS |

四格必须严格串行，且不得修改 timeout、budget、fixture 或 expected result。每个 lane 只证明自己的解释器与
optimization coordinate；这些本地结果仍不替代远端 required checks 或公开读回。

最终静态门还须确认 exact four-file scope、全仓 prose relative links 零断链、四份变更文件 UTF-8 without BOM、LF /
final LF、Markdown fences 平衡、本文 heading 唯一、无敏感本机路径；文档 208/209/210、architecture DOT/SVG、
runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 保持原字节，`git diff --check` 成立。

```text
publication final bytes
    -> original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后继成功不改写先前观察。不得复用候选 Evidence、拿 #223–#230
的绿灯替代本发布门，或把内容相同解释成 qualification-path equivalence。

## 8. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新读取 frozen truth，再判断 Parse
fulfillment prerequisite 是否仍是当前最小合法问题。文档编号、implementation frozen 或绿色 CI 都不能自动授予
Parse、Fact、persistence、Coverage 或 public carrier 施工权。

若新的 readback、reconciliation 或系统审计击穿当前 closure，只重开被击穿的最小 seam 并重新取得资格。不得按
原路线机械进入下一阶段。
