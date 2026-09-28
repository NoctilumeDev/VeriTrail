# R1 Parse fulfillment 最小合同冻结发布

日期：2026-09-28

## 1. 发布对象与生效条件

本文只发布[文档 217](217-r1-parse-fulfillment-contract.md)的 Parse fulfillment 最小合同 `0.1`。本文自己的
final bytes、original PR 门、受保护合入、new exact-main Public CI / Browser Smoke、fresh anonymous
installed-product readback 与 independent reconciliation 全部成立后，以下目标才成为当前事实：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED
R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDITED
R1_PARSE_PRODUCT_FACT_CONSUMER_BINDING_PRECONTRACT_AUDITED
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文最后门闭合以前，current fact 仍为 `R1_PARSE_FULFILLMENT_CONTRACT_CANDIDATE`。把 frozen marker 写入
条件化发布字节不替代该门，也不授予 parser、AST、product carrier、Fact consumer 或其他 runtime authority。

| 坐标 | 值 |
| --- | --- |
| 问题审计 | [文档 213](213-r1-parse-fulfillment-authority-problem-audit.md)，qualified history |
| 前合同审计 | [文档 214](214-r1-parse-fulfillment-precontract-audit.md)，`PRECONTRACT_AUDITED` |
| consumer 前置审计 | [文档 215](215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)，qualified history |
| consumer binding 前合同审计 | [文档 216](216-r1-parse-product-fact-consumer-binding-precontract-audit.md)，`PRECONTRACT_AUDITED` |
| 合同候选 | [文档 217](217-r1-parse-fulfillment-contract.md) |
| 候选 PR | [#240](https://github.com/NoctilumeDev/VeriTrail/pull/240) |
| 候选 base | `63daada4157e0068bb2a1333953f821f56f61894` |
| 候选 head | `cf26f4224ef17549d5e086bfcd599de3163358d4` |
| 候选 merge | `446604ffc437ff710faf524c1634839dc1a0ddd7` |
| 候选 head / merge tree | `aa9099f6c4667c39c7493743245a523ca9626351` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

本文不新增文档 217 之外的合同语义。冻结范围只有：

```text
exact Language Support ELIGIBLE denominator
    -> one shared Parse obligation per subject / parent attempt
r1-python-parse/0.1 + CPython 3.10.6 reference semantics
    -> grammar-only ACCEPTED(product) / REJECTED(PARSE_ERROR)
all per-subject semantic results + lifecycle evidence
    -> complete exact denominator reconciliation
    -> application-owned admitted product-set identity
same-attempt immutable/copy-owned access
    -> product may be consumed without transferring live authority
```

由此只发布以下边界：

1. denominator 来自 exact Language Support `ELIGIBLE` 结果；Provider 不定义 denominator；
2. 同一 parent attempt、同一 subject 只有一个共享 Parse obligation，不按下游 Provider 数量复制；
3. `r1-python-parse/0.1` 的目标语义固定为 CPython 3.10.6 reference grammar；宿主版本不是 authority；
4. Parse semantic terminal 只有 grammar-only accepted product 或 canonical `PARSE_ERROR` rejection；
5. semantic result、execution lifecycle 与 domain reconciliation 是不同事实；
6. accepted result 必须携带 application-owned admitted product；裸 subject ID 或 digest 回显不足以证明消费；
7. complete reconciliation 必须覆盖 exact denominator，不能把 missing / error 伪装成 rejected 或 empty；
8. semantic product equality、product-set equality与重新计算都不继承 attempt、BudgetContext、claim 或 continuation。

以下继续是 non-decision / not authorized：

```text
product carrier / digest algorithm / persistence route
parser / AST runtime implementation
Fact Provider product-use enforcement
zero-accepted scheduling
new Fact wire or Fact fulfillment
public Schema / Evidence / Manifest / Bundle / publisher
ReviewSliceSet / Coverage
```

## 3. 候选 source qualification

候选只改变 AGENTS、README、文档 216、文档 217 与 milestones。architecture DOT/SVG、runtime、tests、Schema、
Profile、Policy、corpus、identity vectors、Provider 与 wire implementation 均未修改。

| 门 | Run | Source | 结果 |
| --- | --- | --- | --- |
| PR #240 Public CI | `36422575750` | `cf26f422...` | attempt 1，`11/11 SUCCESS` |
| exact-main Public CI | `36425303909` | `446604f...` | attempt 1，`11/11 SUCCESS` |
| exact-main Browser Smoke | `36425303740` | `446604f...` | attempt 1，`1/1 SUCCESS` |

候选最终字节完成 CPython 3.10.6 / 3.13.13 normal / `-O` 的 Markdown / Schema 四格各 `40/40 PASS`，
与 source claims 直接相关的 source-operation gate、Fact wire、controller integration 与 multi-Provider suite 四格各
`67/67 PASS`。五文件 scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、marker、敏感路径、
audit script identity 与 `git diff --check` 均成立。

候选施工期的 managed-worktree calling root、PowerShell heredoc、patch anchor 与 marker checker expectation 等 setup
failure 均保留原身份；它们没有形成 product observation。后继 PASS 不把这些记录倒写成未发生。

## 4. 候选 fresh installed-product readback

readback 从 detached exact `main@446604f...` 建立 fresh CPython 3.13.13 venv，安装 Core `0.13.0`、GitHub
Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件都从该 venv 的 `site-packages`
导入；`GITHUB_TOKEN`、`GH_TOKEN`、`PYTHONPATH` 与 `VERITRAIL_SOURCE_ROOT` 均清空。冻结 wheels 的 SHA-256：

```text
Core
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04
GitHub Evidence
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

首次 README 正式观察必须保留：

```text
Plan ID  r1-parse-contract-readme
session  github-paired-9f6eba497a094517b190d2ad5c9a1d18
Plan     0fe5b90a25d7ec11f17fbd5a848b488da47dcbd1027b453811731aeb227292f4
P1       ERROR / HTTP 403 / COLLECTION_BUDGET_EXHAUSTED / remaining 0
P2       COMPLETE / HTTP 200
```

该 observation 已在执行前保存 sealed Plan，且 API / render 绑定同一 Plan digest 与 session。它没有生成 handoff、
AcceptanceBundle 或 Core report，因此不是 Core FAIL、合同 FAIL 或 public byte mismatch。GitHub 返回的失败原因是匿名
core rate exhaustion；为什么 preflight 所见可用 bucket 与正式请求 bucket 不同没有被归因。旧 output 没有删除、
覆盖或复用，后继成功也不改变它的 ERROR identity。

reset 以后才使用全新身份启动第二次 README 正式观察。三个 qualifying observations 为：

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README #2 | `r1-parse-contract-readme-2` | `github-paired-0fbfc7f841454c4eba3f1718d0498346` | `b9d2085b2c1458b20888cd7630034ecf49289db9e1d44086885d2dcbe17fa4df` |
| 文档 217 | `r1-parse-contract-doc217` | `github-paired-d66acf929e83441caecada8ac4e70794` | `3ded8cbe0ca90d39983a9fa2c55842875dfb67e2dad80189f2b18cbe41db8b89` |
| milestones | `r1-parse-contract-milestones` | `github-paired-5eb5629512064766b263758afa193ce9` | `9079df0d1d1c6c41596d5a9d10be63610b568110969ca923af54c3bd23ebf70c` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 marker、零 conflict / coverage reason /
cleanup error / active stream，Core 均为 `PASS`。历史形状是 **README #1 ERROR + 三个后继正式 PASS**，不能写成
“读回全程无失败”。

正式 observation 前的 installed-environment preflight 成功写入环境与匿名 API HTTP 200 Artifact，但 Playwright 在
进程退出时打印内部 pending-connection `TargetClosedError` warning。它没有 Plan/session/product output，被保留为
setup/preflight warning，不计入资格。五份 anonymous raw-source bytes 另行逐字节等于 exact Git blobs；该核查不是
P1/P2 Evidence，也不替代特定消费路径。

## 5. 独立复算与 source-byte 核账

联合 verifier 独立验证三个 qualifying sealed Plan、P1/P2 Evidence、handoff、report 与 summary digest，重新 import
handoff 后调用安装版 Core 复算 adjudication fields。它还验证并永久保留第一次 README ERROR 的 Plan/API/render
identity、403 rate metadata 与无 handoff/report 形状，并核对：

- qualifying Plan ID、Plan digest、session 与 output root 互不复用；
- PR #240、candidate head、ordinary merge parents/tree 与 exact five-file candidate scope；
- PR、exact-main Public CI 与 Browser Smoke 均绑定预期 SHA、attempt 1 且所有 jobs 成功；
- installed wheel identity、architecture asset continuity 与 exact Git blob bytes；
- AGENTS、README、文档 216、文档 217、milestones 五份 anonymous raw bytes 等于 exact Git blobs。

verifier 在 normal / `-O` 下生成相同 canonical reconciliation manifest：

```text
sha256_json  = f76d687ab15a06a5e20172429176774c2c65ecc82616b2628dfcf043bcb3a292
sha256_bytes = 78bddb62cf980afb79fca85d8cd201b6fda3bca6e7ca426bb73280da51e6d76b
```

该 manifest 属于本地证据链；摘要不让本地 Artifact 自动成为远端可取得文件，也不替代本冻结发布自己的门。

## 6. 本发布自己的最后门

本发布只允许修改 AGENTS、README、文档 217、milestones，并新增本文。doc217 第 1–15 节语义、上游 frozen
documents、architecture DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus、identity vectors、Provider 与
wire implementation 必须保持原字节。

提交前须完成适用 Markdown/Schema regression 的双 Python normal / `-O` 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff scope、合同语义 continuity 与 `git diff --check`。本地门不能
替代本发布自己的 original required checks。

```text
publication final bytes
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 文档 217 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察保留原身份；诊断不计入资格，后继成功不改写旧 observation。不得复用候选 Evidence、拿 PR #240
或 `main@446604f...` 的绿灯替代本发布门，也不得在结果出现后修改验收标准。

本发布施工开始前还保留两项 operator/setup history：一次 `git ls-remote` 漏注入 command-local proxy 后 DNS
失败；一次 worktree clean checker 误把 PowerShell `$null -ne ''` 判为 dirty。显式代理与 porcelain line-count
只修复命令设置，没有修改候选 source 或产品 observation。

本发布最终字节复核期间，一次未加引号的 PowerShell `git rev-parse <sha>^{tree}` invocation 又把 revision
表达式重写为无效参数并返回 `fatal: ambiguous argument`。后继只以 quoted revision 重新读取既有 commit/tree；该
setup failure 没有修改 source、合同或产品 observation，也不计入资格。

## 7. 后继停止线

本文最后门全部成立后，必须先回到 CONTROL LOOP，从新的 exact main 重新审计最小 private implementation 的
feasibility、authority owners 与停止线。`CONTRACT_FROZEN` 不自动产生 `IMPLEMENTATION_ALLOWED`。

product carrier、digest、persistence Route A/B、真实 parser/AST、Fact Provider product-use proof、zero-accepted
scheduling、new wire、Fact fulfillment、public Schema/Evidence/Manifest/Bundle/publisher、ReviewSliceSet/Coverage、
CLI、Workbench 与其他顶层轨均不由本文开始。

冻结原则为：**Parse 履责属于完整 exact denominator 的机械对账；接受结果必须携带 admitted product，而相同
product 语义永远不能转移 live execution authority。**
