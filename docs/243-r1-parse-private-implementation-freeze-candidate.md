# R1 Parse fulfillment private implementation 实现冻结候选

日期：2026-10-10

## 1. 当前裁决

> 条件化状态目标：`R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_IMPLEMENTED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_STAGES_A_B_C_D_E_F_G_H_EXACT_MAIN_VERIFIED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FREEZE_CANDIDATE /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 217](217-r1-parse-fulfillment-contract.md)
>
> 合同冻结发布：[文档 218](218-r1-parse-fulfillment-contract-freeze-publication.md)
>
> 可行性审计：[文档 219](219-r1-parse-private-implementation-feasibility-audit.md)
>
> 实现授权发布：[文档 241](241-r1-parse-private-implementation-authorization-publication.md)
>
> CI 夹具观察修正：[文档 242](242-r1-parse-authorization-ci-fixture-observation-correction.md)
>
> 实现 PR：[#279](https://github.com/NoctilumeDev/VeriTrail/pull/279)
>
> 实现 exact main：`26f21b5049dc87c889862fbcef2a12e76aed697e`

文档 241 的最后门闭合后，CONTROL LOOP 从新的 exact main 重新核对 frozen contract、文档 219 的 A–H、current
runtime、open PR 与 retained counterexamples。没有新事实击穿 exact input、ELIGIBLE denominator、explicit
CPython 3.10.6 reference runtime、one-shot claims、contained worker、complete reconciliation、private product set 或
same-attempt continuation 的有限实现前提。

PR #279 因此只在 `veritrail_review` private boundary 内物化 doc219 A–H。本文记录实现 identity、合同闭合、local/remote
witness 与冻结候选资格。本文自己的 final bytes、original PR、受保护合入、新 exact-main 双门、fresh anonymous
installed-product readback、independent reconciliation 与后继独立最终状态发布全部成立前，不得写成
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN`。

## 2. Exact implementation identity

实现从授权闭合后的 exact source 建立：

```text
implementation base  = 026fabd74d7cc3fb9be1300e66f22fb8fd38fe7b
implementation head  = 2965fcfa1908d2e73e1600118493b69d5e37646a
implementation merge = 26f21b5049dc87c889862fbcef2a12e76aed697e
implementation tree  = 3d6cd1b783f7919ef3657e391d7d8c4de9f85fa5
merge parents         = 026fabd74d7cc3fb9be1300e66f22fb8fd38fe7b
                        2965fcfa1908d2e73e1600118493b69d5e37646a
```

candidate 与 merge tree 相同。实现 diff 严格限于 5 个文件，`2162 insertions / 0 deletions`：

```text
plugins/review-attention/src/veritrail_review/_parse_fulfillment.py
plugins/review-attention/src/veritrail_review/_parse_fulfillment_values.py
plugins/review-attention/src/veritrail_review/_parse_fulfillment_worker.py
plugins/review-attention/tests/test_parse_fulfillment.py
plugins/review-attention/tests/test_boundaries.py
```

三个 runtime module 保持 private；顶层 `veritrail_review` 没有新增 export。实现没有修改 current Fact
projection/request/wire、Provider scheduling、公共 Schema/corpus/identity vector、Evidence、Manifest、publisher、
Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 3. A–H private closure

### A. Exact input history

application 从 copy-owned exact inputs 重新验证 SourceSnapshot、ReviewPolicy、DerivationProfile、cross-artifact binding、
Language Support classification 与全部 verified Git object bytes。它不重新读取 mutable repository path，也不把 dataclass、
caller digest 或历史 classification 当作当前资格。

### B. Exact denominator

Parse denominator 只能由 frozen Language Support classification 中的全部 `ELIGIBLE` subjects 形成，并按 canonical
subject identity 排序。rejected/unsupported/out-of-scope body 不进入 worker。zero denominator 与 all-rejected complete
形成不同 semantic product-set identity；二者都不自动形成 Fact 或 Coverage closure。

### C. Runtime capability 与 one-shot claims

controller 只接受显式绝对路径选择的 CPython 3.10.6 executable，并绑定 caller-observed executable SHA-256；worker 又在
受约束 execution cell 中确认 exact runtime version。ambient `sys.executable`、PATH、`py` launcher、feature emulation、
自动下载与 worker self-report 都不能单独建立 runtime authority。

每个 exact denominator subject 对应一个 parent-attempt-bound child claim。claim concurrency-safe、one-shot；相同 limits、
相同 source/classification/product bytes 或另一 attempt 的 child eligibility 都不能替代原 live authority。

### D. Contained worker 与 canonical product

private worker protocol `veritrail-r1-parse-worker/0.1` 在 exact CPython 3.10.6 中执行：

```text
ast.parse(
    exact_decoded_source,
    filename="<veritrail-r1-parse>",
    mode="exec",
    type_comments=False,
    feature_version=(3, 10),
)
```

accepted result 保存 canonical AST fields、attributes、list order、type ignores 与 source locations；bytes 使用 base64，
float/complex 使用稳定十六进制表示，`Ellipsis` 使用显式 scalar identity。parent 不在 ambient runtime 中重新 parse 或替换
reference product。syntax rejection 统一形成 canonical `PARSE_ERROR`；它不被 Language Support reason 或
`UNSUPPORTED_SYNTAX_VERSION` 重新解释。

### E. Semantic 与 lifecycle 分离

`ACCEPTED` / `REJECTED` 是 worker semantic terminal。reference runtime unavailable、start/readiness、worker protocol、
timeout、resource、release、interruption 与 infrastructure failure 都保留为 lifecycle/infrastructure outcome，没有 semantic
result；它们不得伪装 `PARSE_ERROR`、known-empty denominator 或正常 completion。

### F. Complete reconciliation

application 必须收齐并验证 exact denominator。missing、duplicate、dangling、foreign-attempt、cross-world、post-construction
mutation 与 lifecycle non-success 全部 fail closed；不能 first-success、best-effort subset、自动 retry 或从已返回结果反向
缩小 denominator。一个 child 正常结束也不关闭 parent attempt。

### G. Admitted private product set

只有 complete reconciliation 才能创建 application-owned `OwnedParseProductSet`。canonical product/product-set bytes 与
digest 只表达 semantic identity，并提供 copy-owned access；它们不是 public Artifact、Evidence、receipt、Coverage
denominator、historical persistence 或 executable authority。

### H. Same-attempt continuation 与 hardening

normal continuation one-shot 绑定原 `BudgetContext`、parent eligibility、exact inputs/classification/runtime、全部 claims、
complete reconciliation 与本次 product-set object binding。相同 product-set digest 的另一 attempt 不能继承 continuation。
`PFI-000..016` 的主要反推理均由 21 项 Parse direct tests 与 private-boundary tests 提供 witness；测试仍不拥有合同扩张
或下一阶段授权。

## 4. Final implementation-byte qualification

最终实现字节的 canonical manifest SHA-256 为：

```text
a1b371cb91c15d0c754352bb3c8404bf718d8d3015ad6987b4fdd7b62a230e1f
```

Parse direct suite 在四格各运行 21 项；CPython 3.10.6 因宿主本身就是 reference runtime，ambient-runtime impersonation
负向用例按预期 skip，CPython 3.13.13 则实际执行该用例。最终 full Review Attention matrix 为：

| Lane | Result | Duration | Log SHA-256 |
| --- | --- | ---: | --- |
| CPython 3.10.6 normal | `439 OK / skipped=1` | `529.905s` | `8b3ec798b9580f303154ec30c60cd56d7d887d8b854314eb16e160cd81458ca9` |
| CPython 3.10.6 `-O` | `439 OK / skipped=1` | `525.997s` | `235df528ed7298f887070f92d1037d971c80b1fbb89d1058c5a2e3367253112b` |
| CPython 3.13.13 normal | `439/439 PASS` | `513.402s` | `c090beeb0d7bf9e27e66819fecb466aea309fd7e6e505ca0b202f71ebf76ab0d` |
| CPython 3.13.13 `-O` | `439/439 PASS` | `523.344s` | `b8e6c6fabaef17af719dc1760367d7d1f4a6555f737609d8e1648d91e769f1aa` |

fresh wheel build 生成 `veritrail_review_attention-0.1.0.dev0-py3-none-any.whl`：

```text
bytes   = 206883
sha256  = bd9c69d737a8a75f6dbc1a8f980faa5e11c4a7fa9f9e93104267034307c3c6b3
```

wheel 在 fresh venv 安装后，三个 private runtime modules 与 source tree 逐字节相同，worker 被正确打包，顶层没有新增
authority export。installed-package readback manifest SHA-256 为：

```text
a939cdc74d732d05406fc682aa476af06d73393c5a27d99bfc81bf6aff0b1f3b
```

这些 witness 绑定 implementation final bytes；它们不替代 PR/exact-main gates，也不把 sampled tests 升级为全部 Python
grammar、恶意 runtime authenticity 或未来 Fact consumer correctness 的证明。

## 5. PR 与 exact-main gates

PR #279 original head `2965fcfa1908d2e73e1600118493b69d5e37646a` 的 Public CI
[run 37966413820](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37966413820) 是
`pull_request / attempt 1 / 11/11 SUCCESS`。没有 rerun 或后继 push。候选随后以 ordinary merge commit 合入受保护
`main@26f21b5049dc87c889862fbcef2a12e76aed697e`，merge tree 与 candidate tree 相同。

该 exact main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | --- | --- | --- |
| Public CI | [37969385811](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37969385811) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [37969385827](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37969385827) | 1 | `1/1 SUCCESS` |

PR 与 exact-main 绿色分别绑定自己的 source coordinate；它们不互相继承，也不替代本文的 docs-only 资格门。

## 6. Anonymous exact-SHA source readback

清空 `GH_TOKEN` / `GITHUB_TOKEN` / `PYTHONPATH` 后，从 `raw.githubusercontent.com` 匿名读取 exact merge SHA 上的
5 个 implementation files。五项均为 HTTP 200、无重定向，且逐字节等于 exact Git blobs：

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `_parse_fulfillment.py` | 31912 | `2c845899213b81c5cee32017ec889d1c304199e02df636bfb026a1f17b6a0f3a` |
| `_parse_fulfillment_values.py` | 21201 | `5d5f5125ddebeb934712e793e081cf0e191a8a193962afd028b30659df3afda2` |
| `_parse_fulfillment_worker.py` | 4795 | `e54f8da698efd3811dc5cf4b499238dd0d29132815d5ba16881e7e2e6d024ac8` |
| `test_parse_fulfillment.py` | 23074 | `0da41d30cff5904f7ae9493cd31f78afa2db9581211def54bed8aadcb5206240` |
| `test_boundaries.py` | 14113 | `e2e3a9170c0361e67f00e09e4dd7c80e406ae8199796b82c0d0f2862b17b559b` |

canonical source-readback manifest SHA-256 为：

```text
d7fbe6441f095595ebf471319d85f0609321d5d70311f520625625c0cb0dcf2f
```

该 readback 只证明公开 exact bytes 与 Git tree identity；它不独自证明 contract conformance，也不创建 public Parse
Artifact、Fact consumer authority 或 persistence 决策。

## 7. 保留的失败与施工观察

### 7.1 授权 publication 的 formal exact-main failure

PR #277 的 original 11/11 与 exact-main Browser 1/1 成立，但 exact-main Public CI `37926907456` 在 Python 3.10
`-O` 的 combined service fixture 期间硬退出。日志没有 traceback、assertion 或 unittest summary；正式身份保持
`FAILURE / ROOT_CAUSE_UNKNOWN`。文档 242 与 PR #278 只拆分测试 world、补观察阶段并保证 session 在临时目录前清理；
它们没有声称解释或修复唯一根因。#278 与后继 exact-main 双门建立的是新 source state qualification，不覆盖 #277。

### 7.2 Implementation local qualification first failure

implementation final-byte local qualification attempt 1 的 CPython 3.10.6 `-O` full Review Attention suite 在未修改的
Relation `RD-016` 得到 `INTERRUPTED`，而测试预期 `COMPLETED`。该格保持 `FAIL / ROOT_CAUSE_UNKNOWN`；Relation
runtime、timeout、fixture 与 expected result 没有因此修改。后继同 world isolated PASS、instrumented full-suite PASS
都只作 non-qualifying diagnostics，不能把首败解释成 flake。

attempt 2 的四格虽全部成功，但其字节随后被 Parse hardening 扩充，因此保持 superseded identity；attempt 3 才是本候选
第 4 节绑定的最终实现字节。

### 7.3 Setup / tooling history

- 首次 targeted module command 使用错误 module invocation，在 product code 前以 `ModuleNotFoundError` 停止；
- build frontend 不存在，随后使用 clean `pip wheel` 路径；
- 一次递归清理/构建组合命令在 shell 执行前被安全层拒绝，没有文件 mutation；
- 首次 push 因 DNS failure 停止，后继只对单条命令注入代理后成功；
- PR artifact attachment 因 identity 数量上限失败，没有作为资格门重试；
- pre-merge tree query 的 unquoted `HEAD^{tree}` 被 PowerShell 错误解释，后继只读查询改用 `git show -s --format=%T`。

这些观察保持 setup/tooling/network 身份，不是 Parse semantic failure；后继成功不把它们倒写成未发生。

## 8. Scope reconciliation

本实现只建立 same-attempt、private、in-memory Parse fulfillment closure。以下能力继续未授权：

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

以下不等式继续成立：

```text
ELIGIBLE != Parse fulfilled
worker terminal != admitted product set
semantic result != lifecycle success
product-set equality != attempt authority
implementation exact-main verified != implementation frozen
private Parse closure != Fact consumer correction
```

## 9. 本候选自己的最后门

本文与状态入口只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。doc217/218/219/241/242、
implementation runtime/tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture DOT/SVG 必须保持原字节。

提交前必须完成：

1. applicable docs / Schema regressions 与 full Review Attention suite 的 CPython 3.10.6 / 3.13.13 normal / `-O` 四格；
2. exact scope、relative links、Markdown fence/heading、状态 marker、UTF-8 without BOM、LF/final-LF、敏感/本机路径、
   frozen-byte continuity 与 `git diff --check`；
3. original PR required checks 全部成功；
4. 受保护主线合入且 merge parents/tree 可复核；
5. new exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
6. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
7. independent Core/source-byte reconciliation；
8. 后继独立状态发布完成自己的同等级 final bytes、original PR、merge、exact-main 双门与 fresh
   readback/reconciliation，才允许发布 `R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN`。

任一非成功观察都保留原 identity 并停止；诊断不计入资格，后继 PASS 不覆盖首败。本文 target markers 在最后门以前
只表示 publication target，不授权 Fact consumer、persistence、Coverage 或其他顶层施工。

## 10. 下一停止线

当前唯一合法动作是完成本 docs-only candidate 的资格闭环。候选取得资格后，仍须从新的 exact main 建立独立最终
冻结发布；最终冻结发布闭合以后再返回 CONTROL LOOP，重新判断 Parse -> Fact consumer correction contract 是否仍是
当前最小合法问题。

不得从 A–H 绿色自动修改 current Fact wire、选择 persistence、创建通用 receipt/ledger、开始 Fact fulfillment 或恢复
ReviewSliceSet/Coverage。若新的 readback、reconciliation 或系统审计击穿当前 closure，只重开被击穿的最小 seam。
