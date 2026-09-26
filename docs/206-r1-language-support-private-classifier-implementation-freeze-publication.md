# R1 Language Support private classifier 实现冻结发布

日期：2026-09-27

## 1. 文档身份与条件状态

> 状态目标：`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 202](202-r1-language-support-codec-conformance-correction-contract.md)
>
> 合同冻结：[文档 203](203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)
>
> 实现授权：[文档 204](204-r1-language-support-private-classifier-implementation-authorization-audit.md)
>
> 实现候选：[文档 205](205-r1-language-support-private-classifier-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@f79d6d1d470f36b553874492bdd35b53a1b042dd`
>
> 候选合入 Tree：`83d3c74784cf6bc29ee97de478b140477c84e889`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 `r1-python-language-support/0.2` private deterministic classifier 已完成实现、候选资格、受保护
主线合入、new exact-main 双门、fresh anonymous installed-product readback 与独立 reconciliation 的事实。本文
不创建或修改 runtime、tests、Schema、Profile、Policy、corpus、identity vector、execution-cell request/protocol、
Provider、Parse、AST、Fact、ReviewSliceSet、Coverage、Evidence、Manifest、publisher、Bundle、CLI、Workbench、
Core、P/Q/D/Cu/O/T、tag 或 Release。

本文自身仍须完成 original PR required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及
针对本文合入坐标的 fresh anonymous installed-product readback 与 reconciliation。只有这些最后门全部成立，
状态目标才成为当前主线事实；在此以前，本分支中的 frozen marker 只是 publication target，不授权后继施工。

## 2. 本次冻结的最小对象

本次只冻结一个 private、deterministic、non-published classification closure：

```text
copy-owned exact DerivationInputSet
        ↓
canonical Snapshot / Policy / Profile revalidation
        ↓
cross-artifact binding + exact Git object byte closure
        ↓
authoritative IN_SCOPE denominator
        ↓
r1-python-language-support/0.2
closed Python 3.10 UTF-8 / UTF-8-SIG qualification
        ↓
complete canonical failed-reason composition
        ↓
eligible / unsupported exactly-one closure
        ↓
immutable private semantic result
```

该结果不携带 attempt、`BudgetContext`、ProviderRun、continuation、admission 或 disposition authority。相同 exact
semantic world 与相同 function identity 可以得到相同 classification bytes；这不使两次 computation 成为同一
attempt，也不允许任何消费者继承另一次执行权。

合法空 denominator 只证明 Language Support 阶段已知为空，不证明 Parse、Fact 或 Coverage 已履责，不生成
`CLOSED_EMPTY`、ReviewSliceSet 或 public closure。private canonical bytes/digest 只用于当前边界内的确定性比较，
不是公共 identity、Evidence 或 publication coordinate。

## 3. Implementation 与候选精确链

实现链为：

```text
implementation base  = ad52dbbd361872b2d8de1fbb35d5be152d4e03f1
implementation head  = dac2892a173844c4cb288e6381895577e0b46f33
implementation merge = c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84
implementation tree  = c75855d78ea00d061bac1234533dd536c9e44c33
```

[PR #217](https://github.com/NoctilumeDev/VeriTrail/pull/217) original Public CI run
[36263694668](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36263694668) 为
`pull_request / attempt 1 / 11/11 SUCCESS`。implementation merge 的 exact-main Public CI run
[36264888477](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36264888477) 为 attempt 1、11/11 success；
Browser Smoke run [36264888553](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36264888553) 为 attempt 1、
1/1 success。

实现 diff 严格限于两个 private runtime modules 与一个 test module，共 `1136 insertions / 0 deletions`。最终
Language Support targeted suite 在 CPython 3.10.6/3.13.13 normal/`-O` 四格均为 `20/20 PASS`，完整 Review
Attention suite 四格均为 `316/316 PASS`。五个 canonical worlds 在四格中逐字节一致。三个实现文件的匿名
exact-SHA raw-source readback 均为 HTTP 200、无重定向并等于 Git blobs；仓库外 manifest SHA-256 为：

```text
daa0d098b2b3024e5f93945a020704009ac92d8715b8bea38db8d63a2aefb404
```

文档 205 的候选精确链为：

```text
candidate base  = c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84
candidate head  = 8c6dc1e1e5227fff5d50e80de0711b8ad3a52bbc
candidate merge = f79d6d1d470f36b553874492bdd35b53a1b042dd
candidate tree  = 83d3c74784cf6bc29ee97de478b140477c84e889
merge parents   = c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84
                  8c6dc1e1e5227fff5d50e80de0711b8ad3a52bbc
```

[PR #218](https://github.com/NoctilumeDev/VeriTrail/pull/218) 只有一个 commit、四个文件；original
[Public CI run 36268364383](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36268364383) 在 attempt 1
取得 11/11 success，没有 rerun 或后继 push。候选以 ordinary merge commit 合入受保护 main，candidate 与 merge
tree 相同。该 exact candidate main 的独立门为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| Public CI | [36269612657](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36269612657) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [36269612652](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36269612652) | 1 | `1/1 SUCCESS` |

## 4. 候选 fresh anonymous installed-product readback

读回从 exact `main@f79d6d1...` 建立 detached source coordinate，并在 fresh CPython 3.13.13 venv 中安装固定
Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件均从该
venv 的 `site-packages` 导入；`GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 均清空。

三个正式观察在 observation 前保存独立 sealed Plan，并使用互不复用的 Plan ID、session 与 output root：

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-ls-cls-cand-readme` | `github-paired-8ed994d0734642eea04b6b958e161d46` | `5f69e3e4ebdc380e3802ad72898687a2fb8e4591a443bc4630dfccf39670da6e` |
| 文档 205 | `r1-ls-cls-cand-doc205` | `github-paired-f751d018aa804931afc34d8ebd4ec777` | `376e55e1debd4ae450eb55ca9b12342df412b30da272c1b4cb0de2d2a753a76e` |
| milestones | `r1-ls-cls-cand-milestones` | `github-paired-c3bd5f8213464c45b60f49fbb55854cf` | `d94ac87f7c55ffd81e1976228ed7e17dad0d04f6c52a3b2aa6cc3c28247e1558` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、预注册 marker 恰好一次、零 error/conflict/
coverage reason/cleanup error/active stream，Core 为 `PASS`。文档 205 与 milestones 的中文 marker 在 PTY 中显示
乱码；independent verifier 直接读取 canonical JSON 并按 Unicode code point 比较，stored marker 与预期相同，因此
该显示现象不改变 Artifact bytes 或 Verdict。

AGENTS、README、文档 205 与 milestones 又做匿名 exact-SHA raw-source 下载，四份文件均逐字节等于 exact Git
blobs。raw-source check 只作 byte reconciliation，不冒充 P1/P2 Evidence 或替代指定消费路径。

## 5. 独立 reconciliation

联合 verifier 独立验证三个 sealed Plan、P1/P2 Evidence、handoff、report 与摘要 digest，并重新 import handoff
后调用已安装 Core 复算 adjudication fields。它同时核对：

- 三组 Plan/session/output identity 不复用；
- PR #218、candidate head、ordinary merge parents/tree 与四文件 scope；
- PR、exact-main Public CI 与 Browser Smoke 都绑定预期 source SHA 且为 attempt 1；
- installed wheel identity 与 architecture asset byte continuity；
- 四份公开 raw bytes 等于 exact Git blobs。

canonical reconciliation manifest 位于仓库外，其摘要为：

```text
sha256_json  = 2bc041af39faefdf3872397b72f3d18ede5e1364ee4cfc9f92c8a4e10e233384
sha256_bytes = b1bdbb3b79a01b42dee69fe281f87e635b982e9c60254a81100ccdc4e5551a54
```

该 manifest 属于本地证据链；摘要不使本地 Artifact 自动成为远端可取得文件，也不替代本发布自己的门。

## 6. 保留的 setup / operator observations

候选读回准备阶段保留三项 setup observation：

1. PowerShell 对 `HEAD^{tree}` 的解析使一次诊断命令失败；后继使用 `git show -s --format=%T` 取得 tree；
2. Windows `rg` 把 `*.py` 当作 literal path；后继改用显式文件路径；
3. 正式观察开始前的匿名 Render diagnostic 已成功退出并写出结果，但 Playwright shutdown 后出现
   `TargetClosedError` warning。

这三项发生时均没有对应的正式 Plan/session/Evidence/output，或没有改变任何正式观察身份。它们不是 classifier
runtime failure，也不能被后继成功改写成“没有发生”。

本发布的首次全仓 relative-link checker 又把文档 89 代码片段中的 regex character class 与 group 误识别为
Markdown link，产生 checker false positive。后继检查器只收集 fenced/inline code 之外的 Markdown links；它不修改
旧文档、链接目标或产品字节。该误报保留为 publication validation-harness observation。

## 7. 已冻结不变量与未授权能力

本次冻结后，以下边界成立：

1. classifier 必须从 copy-owned exact bytes 重新验证 Snapshot、Policy、Profile、cross-artifact binding 与 Git
   object continuity，dataclass/type/caller digest 不是资格；
2. denominator 由 exact terminal inventory 与 sealed Policy `IN_SCOPE` join 拥有，Provider 不拥有 denominator 或
   classification authority；
3. 0.2 closed resolver 只处理冻结的 Python 3.10、UTF-8/UTF-8-SIG compatibility domain，不借 ambient codec
   registry 扩张 authority；
4. complete failed-reason set 按冻结 applicability 与 rank canonicalize，不能用 first-failure 执行顺序替代；
5. `eligible / unsupported` 对 denominator 形成 exactly-one closure，但不生成 Parse、Fact 或 Coverage fulfillment；
6. semantic result identity 与 attempt/live continuation authority 分离；相同 classification 不继承执行权；
7. private result 没有 public carrier、Schema、Evidence、publisher 或 Bundle authority。

以下能力继续未授权：

```text
eligible-only Parse operation projection
same-attempt continuation claim
execution-cell request / protocol correction
Provider-side filtering
persistence Route A or B
public Language Support carrier / Schema / Evidence
real parser / AST / Fact fulfillment
shared observation receipt or ledger
ReviewSliceSet / Coverage
publisher / Bundle / CLI / Workbench
```

## 8. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 198、
202、203、204、205 的规范/历史字节，runtime、tests、Schema、Profile、Policy、corpus、identity vectors 与
architecture DOT/SVG 均须保持原字节。

提交前必须完成本层声明的双 Python normal/`-O` Language Support targeted、完整 Review Attention 与
docs/Schema regressions，以及 Markdown relative links、fence/heading、状态 marker、UTF-8/LF/final-LF、敏感路径、
exact diff scope、frozen byte continuity 与 `git diff --check`。这些本地门不能替代本发布自己的 original required
checks。

最终 publication worktree 在未改动的 runtime/test bytes 上严格串行完成以下矩阵；记录证据数字后，受文档文字影响的
docs/Schema 与静态门又在最终文档字节上重跑：

| Lane | Language Support targeted | Full Review Attention | docs / Schema regression |
| --- | --- | --- | --- |
| CPython 3.10.6 normal | `20/20 / 0.108s / PASS` | `316/316 / 434.984s / PASS` | `53/53 / PASS` |
| CPython 3.10.6 `-O` | `20/20 / 0.110s / PASS` | `316/316 / 440.712s / PASS` | `53/53 / PASS` |
| CPython 3.13.13 normal | `20/20 / 0.112s / PASS` | `316/316 / 436.510s / PASS` | `53/53 / PASS` |
| CPython 3.13.13 `-O` | `20/20 / 0.112s / PASS` | `316/316 / 433.606s / PASS` | `53/53 / PASS` |

四格没有并发执行，也没有修改 timeout、budget、fixture 或 expected result。每个 lane 只证明自己的解释器与
optimization coordinate；这些本地结果仍不替代远端 required checks 或公开读回。

最终静态门确认 exact 四文件 scope，检查全仓 prose 中 926 个 relative links 且零断链；四份变更文件均为 UTF-8
无 BOM、LF、final LF，fence 平衡、heading 无重复、无本机绝对路径。文档 198/202/203/204/205、architecture
DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 保持原字节，`git diff --check`
成立。

```text
publication original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后继成功不改写先前观察。不得复用候选 Evidence、拿 PR #217 / #218
的绿灯替代本发布门，或把内容相同解释成 qualification-path equivalence。

## 9. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新审计：

> eligible-only operation projection 与 same-attempt Parse gate 是否仍然是当前最小合法问题，以及它们能否在不选择
> persistence、不创建 public carrier、不运行真实 parser、不借用 Fact/Coverage authority 的前提下形成 private proof。

本文不授权自动开始 Parse。若新证据击穿 classifier closure、消费边界或既有合同，只重开被击穿的最小 seam 并重新
取得资格；不得按文档编号进入下一阶段。
