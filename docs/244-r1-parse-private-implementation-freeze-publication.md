# R1 Parse fulfillment private implementation 最终冻结发布

日期：2026-10-10

## 1. 文档身份与条件状态

> 状态目标：`R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_IMPLEMENTED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_STAGES_A_B_C_D_E_F_G_H_EXACT_MAIN_VERIFIED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 217](217-r1-parse-fulfillment-contract.md)
>
> 合同冻结发布：[文档 218](218-r1-parse-fulfillment-contract-freeze-publication.md)
>
> 实现可行性审计：[文档 219](219-r1-parse-private-implementation-feasibility-audit.md)
>
> 实现授权发布：[文档 241](241-r1-parse-private-implementation-authorization-publication.md)
>
> 实现冻结候选：[文档 243](243-r1-parse-private-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@cd4aabb38e0352a7df9e5222606dbb96f65135e5`
>
> 候选合入 Tree：`35a92b37dae5571a77178d4945c626d66ff17f95`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 217 / 219 限定的 private A–H 已完成施工、进入受保护 main、通过候选资格链，并且候选自己的
fresh anonymous installed-product readback 与 independent reconciliation 已经成立。本文不创建或修改 runtime、tests、
Schema、Profile、Policy、corpus、identity vector、wire、Provider、Parse semantics、AST semantics、Fact、Relation、
ReviewSliceSet、Coverage、Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文自身仍须完成 final bytes local gates、original PR required checks、受保护主线合入、新 exact-main Public CI /
Browser Smoke，以及针对本文合入坐标的 fresh anonymous installed-product readback 与 independent reconciliation。
只有这些最后门全部成立，状态目标才成为当前主线事实；在此以前，本分支中的 frozen marker 只是 publication target。

## 2. 本次冻结的最小对象

本次只冻结以下 private、attempt-bound、non-published Parse fulfillment closure：

```text
copy-owned exact DerivationInputSet + LanguageSupportClassificationSet
        ↓
exact Git object bytes / classification history revalidation
        ↓
ELIGIBLE Parse denominator
        ↓
explicit exact CPython 3.10.6 runtime capability
        ↓
per-subject one-shot claim under one parent attempt
        ↓
contained worker + canonical private Parse product
        ↓
semantic terminal separated from lifecycle outcome
        ↓
complete denominator reconciliation
        ↓
application-owned Parse product set
        ↓
same-attempt one-shot continuation
```

accepted product 保存 frozen canonical AST fields、attributes、list order、type ignores 与 source locations；bytes 使用
base64，float/complex 使用稳定十六进制，`Ellipsis` 使用显式 scalar identity。syntax rejection 只形成 canonical
`PARSE_ERROR`；reference runtime unavailable、timeout、resource、release、interruption 与 infrastructure failure 均不
伪装 semantic result。

missing、duplicate、dangling、foreign-attempt、cross-world、post-construction mutation 与 lifecycle non-success 全部
fail closed。相同 product/product-set digest、相同 budget limits 或相同-looking input 不继承另一次 attempt authority。

## 3. Implementation 与候选精确链

private A–H implementation 由 PR #279 一次性物化：

```text
implementation base  = 026fabd74d7cc3fb9be1300e66f22fb8fd38fe7b
implementation head  = 2965fcfa1908d2e73e1600118493b69d5e37646a
implementation merge = 26f21b5049dc87c889862fbcef2a12e76aed697e
implementation tree  = 3d6cd1b783f7919ef3657e391d7d8c4de9f85fa5
```

PR #279 只触及五个 private runtime/test files，`2162 insertions / 0 deletions`。original Public CI
`37966413820` attempt 1 为 11/11 SUCCESS；implementation exact-main Public CI `37969385811` attempt 1 为
11/11 SUCCESS，Browser Smoke `37969385827` attempt 1 为 1/1 SUCCESS。五份匿名 exact-SHA source bytes 等于
Git blobs；canonical manifest SHA-256 为
`d7fbe6441f095595ebf471319d85f0609321d5d70311f520625625c0cb0dcf2f`。

文档 243 freeze candidate 的精确链为：

```text
candidate base  = 26f21b5049dc87c889862fbcef2a12e76aed697e
candidate head  = a230c61493c09e4d258adbf95f1056940ebda24c
candidate merge = cd4aabb38e0352a7df9e5222606dbb96f65135e5
candidate tree  = 35a92b37dae5571a77178d4945c626d66ff17f95
merge parents   = 26f21b5049dc87c889862fbcef2a12e76aed697e
                  a230c61493c09e4d258adbf95f1056940ebda24c
```

[PR #280](https://github.com/NoctilumeDev/VeriTrail/pull/280) 只有一个 commit、四个文档/状态文件，`432
insertions / 21 deletions`。original [Public CI run 37977436359](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37977436359)
在 attempt 1 取得 11/11 SUCCESS；candidate 与 ordinary merge tree 相同。该 exact candidate main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| Public CI | [37980410283](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37980410283) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [37980410250](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37980410250) | 1 | `1/1 SUCCESS` |

## 4. 候选 fresh anonymous installed-product readback

读回从 detached exact `main@cd4aabb...` 建立 source coordinate，并在 fresh CPython 3.13.13 venv 中安装固定
Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件均从该
venv 的 `site-packages` 导入；`GH_TOKEN`、`GITHUB_TOKEN`、`PYTHONPATH` 与 `PYTHONHOME` 均清空。

三个正式观察在 observation 前保存独立 sealed Plan，并使用互不复用的 Plan ID、session 与 output root：

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `parse-impl-freeze-candidate-readme-cd4aabb` | `github-paired-ddd369d3acae4d1e9b2a6a3c61d4c9ca` | `450fecabbfbaa7302fb59a76d1ec13816b080b373eec52c2176f239e58a5a11e` |
| 文档 243 | `parse-impl-freeze-candidate-doc243-cd4aabb` | `github-paired-c416c3ccbc824b81b632c11d18d04fa2` | `91e1909ef63424a80a675949a66917d948a8d120397a81acd296c7b1f5d2529c` |
| milestones | `parse-impl-freeze-candidate-milestone-cd4aabb` | `github-paired-112e04eaed8f48d7b33a56a812500cc0` | `c60e91fba386c37c1adac442574109910839c0152e50bddfc4ea0002adef533f` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、预注册 marker 恰好一次、零 error/conflict/
coverage reason/cleanup error/active stream，Core 为 `PASS`。README、文档 243 与 milestones 的匿名 raw-source
bytes 又逐字节等于 exact Git blobs；raw-source check 只作 byte reconciliation，不替代 P1/P2 Evidence。

## 5. 候选 independent reconciliation 与保留观察

独立 verifier 重新核对三个 sealed Plan、P1/P2 Evidence、handoff、report 与摘要 digest，验证 exact commit/tree /
merge-parent identity、三个互不复用的 Plan/session/handoff、外部/Bundle Evidence byte equality 与三份 exact Git bytes。
canonical reconciliation SHA-256 为：

```text
877ca46b98703994402bd0ab7e6f9a1789aa079b51e30ab12fad0f50eee87721
```

正式观察开始前，installed-environment 与 anonymous API preflight 已成功写出；Playwright 在解释器 shutdown 时留下
pending-task / `TargetClosedError` warning。该 warning 没有正式 Plan/session/Evidence/output identity，保留为
`NON_QUALIFYING_SETUP_WARNING`；三个后继 PASS 不把它改写成未发生。

更早的 #277 exact-main Windows 硬退出仍保持 `FAILURE / ROOT_CAUSE_UNKNOWN`。实现 final-byte attempt 1 的
CPython 3.10.6 `-O` full suite 在 unchanged Relation `RD-016` 得到 `INTERRUPTED`，仍保持
`FAIL / ROOT_CAUSE_UNKNOWN`；isolated 与 instrumented PASS 只作 diagnostics。后继绿色不解释这两个首败。

## 6. 已冻结不变量与未授权能力

本次冻结后，以下边界成立：

1. exact input、classification、blob bytes、runtime capability 与 denominator 必须由 application 从 sealed history
   重新验证；caller type/digest 不能替代 canonical validation；
2. Parse subject claim 必须绑定 original parent attempt，per subject exactly once；一个 child 终结不关闭 parent；
3. CPython 3.10.6 reference runtime 必须显式传入并由 worker/version/hash 绑定；ambient Python 不能冒充；
4. semantic `ACCEPTED / REJECTED` 与 lifecycle/infrastructure outcome 严格分离；
5. application 必须对完整 ELIGIBLE denominator reconcile，missing/duplicate/dangling/foreign/cross-world 均拒绝；
6. product/product-set digest 只表达 private semantic identity，不拥有 continuation 或 public authority；
7. continuation 必须绑定 original BudgetContext object、parent、全部 claims、reconciliation 与 product-set object，
   exactly once；
8. private proof 不产生 public carrier、Schema、Evidence、Coverage、publisher 或 Bundle authority。

以下能力继续未授权：

```text
current Fact projection/request/wire changes
Fact Provider scheduling or Parse product-use enforcement
Parse -> Fact consumer correction contract or runtime
historical/offline Parse product persistence Route B
public Parse Schema / carrier / corpus / identity vectors
runtime download / installation / signing / attestation
Fact obligation-universe derivation / fulfillment
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root / Bundle
CLI / Workbench / Core / Q / O / T runtime
DECLARED_CLAIM_FIDELITY / objective-obligation-inference drift
tag / Release
```

## 7. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 217/218/
219/241/242/243、implementation runtime/tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture
DOT/SVG 均须保持原字节。

最终 publication worktree 在未改动的 runtime/test bytes 上严格串行完成四格 full Review Attention 与 docs/Schema
regressions；记录结果后，docs/Schema 与静态门在最终文档字节上重跑：

<!-- FINAL_MATRIX_START -->

| Lane | Full Review Attention | Duration | Log SHA-256 | docs / Schema |
| --- | --- | ---: | --- | --- |
| CPython 3.10.6 normal | `439 OK / skipped=1` | `526.357s` | `80306de809b63c7b8748137d9045ac75022c8e791e6babc69f04537129268fc8` | `40/40 PASS` |
| CPython 3.10.6 `-O` | `439 OK / skipped=1` | `524.788s` | `87abc64cde3f107bb5304a07d4375322524ee8783b6c40ace9a003e3a87f07fd` | `40/40 PASS` |
| CPython 3.13.13 normal | `439/439 PASS` | `517.508s` | `0117497a9e8844ff420c254558a7f0956f29517d4e407b18d69cb118b4ccecfe` | `40/40 PASS` |
| CPython 3.13.13 `-O` | `439/439 PASS` | `519.223s` | `cfa45ffbdf46beda1f62f4e330191b33e4779fcfcb128cff4f23d91921402491` | `40/40 PASS` |

<!-- FINAL_MATRIX_END -->

第一次 local qualification attempt 在 CPython 3.10.6 normal 的 docs/Schema test import 阶段停止：36 项已通过，
`tests.test_markdown` 因临时解释器没有绑定 repository `src` 而得到
`ModuleNotFoundError: No module named 'veritrail'`。该 setup failure 的日志 SHA-256 为
`2ec95487c063e8dca835353afbce82882ff43d3c9bd83a5f11ce310537d4e9c9`；它没有修改 repo bytes，也没有进入
product runtime。fresh attempt 2 显式绑定当前 exact worktree `src` 后从四格第一项重新开始；后继 PASS 不把
attempt 1 写成未发生。

四格必须严格串行，且不得修改 timeout、budget、fixture 或 expected result。每个 lane 只证明自己的解释器与
optimization coordinate；本地结果不替代远端 required checks 或公开读回。

最终静态门还须确认 exact four-file scope、全仓 prose relative links 零断链、四份变更文件 UTF-8 without BOM、LF /
final LF、Markdown fences 平衡、本文 heading 唯一、无敏感本机路径；文档 217/218/219/241/242/243、architecture
DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 保持原字节，`git diff --check` 成立。

```text
publication final bytes
    -> original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后继成功不改写先前观察。不得复用候选 Evidence、拿 #279/#280
的绿灯替代本发布门，或把内容相同解释成 qualification-path equivalence。

## 8. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新读取 frozen truth，再判断 Parse -> Fact
consumer correction contract 是否仍是当前最小合法问题。文档编号、implementation frozen 或绿色 CI 都不能自动
授予 Fact wire、Provider scheduling、persistence、Fact fulfillment、Coverage 或 public carrier 施工权。

若新的 readback、reconciliation 或系统审计击穿当前 closure，只重开被击穿的最小 seam 并重新取得资格。不得按
原路线机械进入下一阶段。
