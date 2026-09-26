# R1 Language Support private classifier 实现冻结候选

## 1. 当前裁决

> 条件化状态目标：`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FREEZE_CANDIDATE /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 202](202-r1-language-support-codec-conformance-correction-contract.md)
>
> 合同冻结发布：[文档 203](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)
>
> 实现授权：[文档 204](204-r1-language-support-private-classifier-implementation-authorization-audit.md)
>
> 实现 PR：[#217](https://github.com/NoctilumeDev/VeriTrail/pull/217)
>
> 实现 exact main：`c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84`

`r1-python-language-support/0.2` 已按文档 204 的有限授权物化为 private deterministic classifier。application
重新验证 exact Snapshot、Policy、Profile、cross-artifact binding 与全部 copy-owned Git object bytes，再对
authoritative `IN_SCOPE` denominator 形成完整 canonical reason composition、eligible/unsupported exactly-one closure
与 immutable private result。

本文只记录实现事实与冻结候选资格。本文自己的远端门、受保护主线合入、新 exact-main 双门、fresh anonymous
installed-product readback 与后继独立最终状态发布全部成立前，不得写成
`R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN`。Parse operation projection、same-attempt
continuation、persistence、public carrier/Schema、Fact 与 Coverage 均没有从本实现取得 authority。

## 2. Exact implementation identity

实现从授权闭合后的 exact source 建立：

```text
implementation base  = ad52dbbd361872b2d8de1fbb35d5be152d4e03f1
implementation head  = dac2892a173844c4cb288e6381895577e0b46f33
implementation merge = c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84
implementation tree  = c75855d78ea00d061bac1234533dd536c9e44c33
merge parents         = ad52dbbd361872b2d8de1fbb35d5be152d4e03f1
                        dac2892a173844c4cb288e6381895577e0b46f33
```

candidate 与 merge tree 相同。实现 diff 严格限于三个新增文件，`1136 insertions / 0 deletions`：

```text
plugins/review-attention/src/veritrail_review/_language_support.py
plugins/review-attention/src/veritrail_review/_language_support_values.py
plugins/review-attention/tests/test_language_support.py
```

两个 runtime module 保持 private；顶层 `veritrail_review` 没有新增 export。实现没有修改 execution-cell request、
Provider protocol、公共 Schema/corpus/identity vector、Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、
P/Q/D/Cu/O/T、tag 或 Release。

## 3. Exact-history revalidation

唯一入口 `classify_language_support(DerivationInputSet)` 不把 dataclass、type 或 caller-supplied digest 当作资格。
每次调用都会从 copy-owned bytes 重新闭合：

```text
SourceSnapshot canonical bytes + digest
ReviewPolicy canonical bytes + seal/digests
DerivationProfile canonical bytes + digest
cross-artifact binding
exact inventory / IN_SCOPE raw-path join
verified blob key set
Git object OID + size + SHA-256 + bytes
```

它不重新读取 mutable filesystem path，也不依赖临时 Git repository 的存活。相同 exact semantic world 可以被重新
计算；本结果不携带 attempt、BudgetContext、ProviderRun、continuation、admission 或 disposition authority。

## 4. 0.2 qualification semantics

实现只接受冻结 compatibility domain：

```text
language                         = PYTHON
language_semantics               = PYTHON_3_10
canonical accepted encodings     = {UTF-8, UTF-8-SIG}
qualification function identity  = r1-python-language-support/0.2
```

closed resolver 实现 Python 3.10 cookie/BOM placement、accepted UTF-8 alias normalization、BOM/cookie consistency、
non-accepted early rejection，以及 possibly eligible UTF-8/UTF-8-SIG 的 strict whole-source decode。它不调用 ambient
`codecs.lookup()` 来扩张可接受集合，也不实现整个 CPython codec universe。

classification 对全部 applicable predicates 求值，收集完整 failed-reason set，再按冻结 rank canonicalize；结果不受
predicate 执行顺序影响。unsupported entry kind 不会被迫生成不适用的 encoding reason；Parse syntax 也不会被
Language Support 越权解释。

## 5. Denominator closure 与 private result

denominator 由 exact Snapshot terminal inventory 与 sealed Policy `IN_SCOPE` join 建立，并按 raw Git path bytes 排序。
实现机械证明：

```text
denominator = eligible U unsupported
eligible intersection unsupported = empty
every denominator member appears exactly once
no OUT_OF_SCOPE or foreign-world member appears
```

合法空 denominator 只形成已知的 Language Support 空分类；它不创建 Parse completion、Fact fulfillment、Coverage
`CLOSED_EMPTY` 或 ReviewSliceSet closure。private result 保存 canonical semantic bytes 与 digest 以供相同输入和
相同 function identity 的确定性比较；该 digest 不是公共 identity，也不能继承另一 attempt 的权力。

## 6. Local qualification

最终实现字节通过：

```text
targeted Language Support suite
  CPython 3.10.6 normal / -O   20/20 PASS
  CPython 3.13.13 normal / -O  20/20 PASS

full Review Attention suite
  CPython 3.10.6 normal / -O   316/316 PASS
  CPython 3.13.13 normal / -O  316/316 PASS
```

五个 canonical worlds 在 CPython 3.10.6 与 3.13.13、normal 与 `-O` 下逐字节一致，覆盖 ordinary UTF-8、
UTF-8-SIG、Profile 不接受的 Latin-1、invalid UTF-8 与 Policy `UNCLASSIFIED`。`compileall`、exact diff scope、
private export/boundary scan 与 `git diff --check` 均成立。

这些测试是文档 204 `LSI2-000..011` 与合同 0.2 的 witness，不证明 sampled corpus 已穷尽 total function，也不授权
Parse gate 或 persistence。

## 7. PR 与 exact-main gates

PR #217 original head `dac2892a173844c4cb288e6381895577e0b46f33` 的 Public CI
[run 36263694668](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36263694668) 是
`pull_request / attempt 1 / 11/11 SUCCESS`。没有 rerun 或后继 push。候选随后以 ordinary merge commit 合入受保护
`main@c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84`，merge tree 与 candidate tree 相同。

该 exact main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | --- | --- | --- |
| Public CI | [36264888477](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36264888477) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [36264888553](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36264888553) | 1 | `1/1 SUCCESS` |

PR 与 exact-main 绿色分别绑定自己的 source coordinate；它们不互相继承，也不替代本文的 docs-only 资格门。

## 8. Anonymous exact-SHA source readback

清空 `GH_TOKEN` / `GITHUB_TOKEN` 后，从 `raw.githubusercontent.com` 匿名读取 exact merge SHA 上的三个实现文件。
三项均为 HTTP 200、无重定向，且逐字节等于 `git show <merge>:<path>`：

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `_language_support.py` | 15028 | `e774cdba9cc3a2820c58e1806f76ec066558b9b07260f6558a564e91e08ebca5` |
| `_language_support_values.py` | 10737 | `70286924c2590c1acfc494a52bfa800e3777c6cd8f80993045abad90339f5ace` |
| `test_language_support.py` | 19453 | `530aa20427007f1e351fa69424213e3a1b66f5ee516a05e16c091e2d38443292` |

仓库外 canonical readback manifest 的 SHA-256 为：

```text
daa0d098b2b3024e5f93945a020704009ac92d8715b8bea38db8d63a2aefb404
```

该 readback 只证明公开 exact bytes 与 Git tree identity；它不独自证明实现符合合同，不创建 public API、Parse
authority 或 persistence 决策。

## 9. 保留的 setup / operator observations

施工中以下观察保持原身份：

- Windows PowerShell 把 wildcard 作为 literal `rg` path，首次搜索未覆盖预期文件；
- broad docs filter 使用 `/` 而当前输出为 Windows `\`，导致一次 broad read 被截短；
- 一次 malformed regex 和一次 Unix heredoc 语法在 PowerShell 中停止；
- `if (git diff --quiet)` 的 no-output 被误读；
- `git rev-parse HEAD^{tree}` 被 PowerShell 改写为 encoded token，诊断命令失败。

这些都没有修改 repo bytes、实现语义或远端身份。它们不能被后继成功改写为“没有发生”，也不是 classifier
runtime failure。

## 10. Scope reconciliation

本实现没有改变系统能力拓扑。architecture DOT/SVG、文档 198/202/203/204、execution-cell 0.1、公共 Schema、
corpus 与 identity vectors 均保持原字节。README、AGENTS 与 milestones 只把公开状态从
`IMPLEMENTATION_NOT_STARTED` 更新为 `IMPLEMENTED / FREEZE_CANDIDATE`。

明确未授权：

```text
eligible-only Parse operation projection
same-attempt continuation claim
execution-cell request/protocol correction
Provider-side filtering
persistence Route A or B
public Language Support carrier / Schema / Evidence
real parser / AST / Fact fulfillment
shared observation receipt or ledger
ReviewSliceSet / Coverage
publisher / Bundle / CLI / Workbench
```

## 11. 本候选自己的最后门

本文与状态入口完成后仍只是 implementation freeze candidate，必须独立完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、UTF-8/LF/final-LF、敏感/本机路径、frozen byte continuity 与
   `git diff --check` 成立；
3. 本层声明的双 Python normal/`-O` docs/Schema regressions 与 Language Support/full Review Attention tests 成立；
4. original PR required checks 全部成功；
5. 受保护主线合入且 merge parents/tree 可复核；
6. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
7. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
8. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN`。

任一非成功观察都保留原身份并停止；后继 PASS 不覆盖首败。本文的 target marker 在最后门以前只表示 publication
target，不授权 Parse/Fact/Coverage 施工。

## 12. 下一停止线

当前唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，必须先对 README、
本文与 milestones 建立三个互不复用的 fresh anonymous installed-product sessions；随后从新的 exact main 创建独立
最终冻结发布。

只有最终冻结发布完成自己的门禁、受保护合入、新 exact-main 双门与 fresh readback 后，才能回到 CONTROL LOOP，
重新判断 eligible-only operation projection 与 same-attempt Parse gate 是否仍是最小合法问题。该判断不得从本文的
实现成功自动推出。
