# R1 Language Support eligible operation projection / same-attempt gate 合同冻结发布

日期：2026-09-27

## 1. 发布对象与生效条件

本文只发布[文档 208](208-r1-language-support-eligible-operation-projection-contract.md)的 private
eligible-operation projection / same-attempt gate 合同 `0.1`。本文自己的 final bytes、original PR 门、受保护合入、
new exact-main Public CI / Browser Smoke、fresh anonymous installed-product readback 与 independent reconciliation
全部成立后，以下目标才成为当前事实：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_ALLOWED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文最后门闭合以前，当前有效资格仍是
`R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_CANDIDATE`，runtime 仍为
`IMPLEMENTATION_NOT_AUTHORIZED`。把 frozen / allowed marker 写入条件化发布字节，不等于这些状态已经生效。

| 坐标 | 值 |
| --- | --- |
| 合同前置审计 | `main@940b6fc9ad974c4e4afb4f6f3e2f635efe780e1c` |
| 合同候选 | [文档 208](208-r1-language-support-eligible-operation-projection-contract.md) |
| 候选 PR | [#221](https://github.com/NoctilumeDev/VeriTrail/pull/221) |
| 候选 base | `940b6fc9ad974c4e4afb4f6f3e2f635efe780e1c` |
| 候选 head | `63e05d4b8d2715d91d78c1cf2487449c5e70b142` |
| 候选 merge | `f4d531bd49de330bd7a186633699262997e949f4` |
| 候选 head / merge tree | `74726f76aa0952af65c656de7441bab8c95296c4` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

本文不新增 doc208 之外的合同语义。冻结范围只有：

```text
r1-python-language-support/0.2 exact eligible upper bound
    -> provider-bound stage operation projection
    -> original live BudgetContext / parent eligibility
    -> distinct one-shot child claims
    -> exact Provider-visible source bodies
```

由此发布以下边界：

1. classifier 拥有 deterministic eligibility；Provider 不拥有 eligibility 或 denominator；
2. application 从 frozen FactSet/domain/assignment 机械导出 Fact、Relation derivation、Relation observation
   各自的 exact operation set；
3. Provider-visible source-body map 必须与该 operation set **恰好相等**，而不只是它的 eligible subset；
4. semantic classification / projection equality 不继承原 `BudgetContext`、parent/child `AttemptEligibility`、
   one-shot claim 或 ProviderRun authority；
5. 多个合法 child 各自 claim，不把整次 attempt 压成一个 global one-shot；
6. filtered request 必须在 encoding 前构造；omitted bytes 不得通过全量 frame、side channel 或 fallback 进入 Provider；
7. Fact wire `0.2`、Relation derivation wire `0.3`、Relation observation wire `0.4` 与 operands
   `0.4/0.5/0.6` 是新候选 identity；历史 wire / operands 继续只读；
8. applicable child 在 empty projection 时仍真实运行 exact empty-body request，但不因此取得 Parse、Fact 或 Coverage
   fulfillment authority。

以下不等式继续成立：

```text
eligible upper bound != operation fulfillment
semantic result equality != attempt authority
empty operation set != higher-stage closure
contract frozen != implementation complete
implementation allowed != implementation started
Language Support eligible != parser success
```

persistence 继续 OPEN。本文不选择 live recomputation 或 canonical derived projection，不创建 public carrier、Schema、
receipt、ledger 或 Bundle。

## 3. 候选 source qualification

候选最终字节只改变 AGENTS、README、文档 208 与 milestones；runtime、tests、Schema、Profile、Policy、corpus、
identity vectors、Provider、protocol implementation 与 architecture DOT/SVG 均未修改。

| 门 | Run | Source | 结果 |
| --- | --- | --- | --- |
| PR #221 Public CI | `36280563559` | `63e05d4b...` | attempt 1，`11/11 SUCCESS` |
| exact-main Public CI | `36281621834` | `f4d531bd...` | attempt 1，`11/11 SUCCESS` |
| exact-main Browser Smoke | `36281621765` | `f4d531bd...` | attempt 1，`1/1 SUCCESS` |

候选本地最终字节完成 CPython 3.10.6 / 3.13.13 normal / `-O` 的 40/40 Markdown / Schema 四格、
497 个 relative links、UTF-8 without BOM、LF/final LF、balanced fences、exact scope、唯一 candidate marker 与
`git diff --check`。文档 207 六-world audit 的四车道输出继续是 3072 bytes，SHA-256 均为
`fec549e3181d02c0ef200c0d3ddc91ebec5d32866519ea0de6f6b9e3d2737ca0`，并逐字节等于已资格化 reference。

候选施工期的无效 `PYTHONPATH` test setup、literal wildcard hash、3073-byte extra-LF writer、3074-byte
double-escaped CRLF writer、PowerShell 单一 hash 字符索引误判，以及 JavaScript command-construction syntax error
均继续保留原身份；最终 PASS 不把它们倒写成未发生。

## 4. 候选 fresh installed-product readback

readback 从 detached exact `main@f4d531bd...` 建立 fresh CPython 3.13.13 venv，并安装 Core `0.13.0`、
GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件均从 venv `site-packages`
导入；`GH_TOKEN`、`GITHUB_TOKEN` 与 `PYTHONPATH` 均清空。

三个正式观察在 observation 前保存独立 sealed Plan，并使用互不复用的 Plan ID、session 与 output root：

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-lspg-contract-readme` | `github-paired-5e87892714b74a908149a60c76864a8e` | `4073773cc4e2cf3432fc09c90225ed06e2bb3c5cab0c8654ab3c506d3e974a1e` |
| 文档 208 | `r1-lspg-contract-doc208` | `github-paired-71f86df484804552bb7f1d810d111673` | `570b198081e2b1046740af6963e883d2a9d602d874be0d4f630b62865b31978c` |
| milestones | `r1-lspg-contract-milestones` | `github-paired-a521e3b9dbb446419ea7686a37bdbc20` | `c041a14ca7f3b9da7ef08b03ed905786b779861b87e68ab6d4fac68b4f354e8f` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 candidate marker、零 conflict、coverage
reason、cleanup error 与 active stream，Core 均为 `PASS`。

开始正式观察前，指定 preflight User-Agent 所在匿名 egress 首先两次返回明确的 HTTP 403 `rate limit exceeded`；
默认 curl User-Agent 当时落到另一个有余额的匿名池，但因消费路径不等价而未被用于替代。精确路径在已声明的
reset 之后取得 HTTP 200，才开始正式 Plan/session。三次 preflight 过程均在 Playwright 正常结果写入或失败退出后
打印 `TargetClosedError` shutdown warning；这些 warning 没有正式 Plan/session 身份并继续保留为 setup history。

独立 reconciliation 的首次 invocation 又因保存的 CI JSON 漏掉 `databaseId`，在 Core 复算前以 `KeyError`
停止；一次用于补齐元数据的 PowerShell 复合命令随后在解析阶段失败，没有子命令运行。三份缺字段 JSON 被保留，
后继只重读相同 immutable run identity 的完整元数据，并重新启动 reconciliation；没有重跑或修改正式 observations。

## 5. 独立复算与 source-byte 核账

联合 verifier 独立验证三个 sealed Plan、P1/P2 Evidence、handoff、report 与 summary digest，重新 import handoff 后
调用已安装 Core 复算 adjudication fields。它还核对：

- 三组 Plan ID、Plan digest、session 与 output 不复用；
- PR #221、candidate head、ordinary merge parents/tree 与四文件 candidate scope；
- PR、exact-main Public CI 与 Browser Smoke 均绑定预期 SHA、attempt 1 且所有 jobs 成功；
- installed wheel identity 与 architecture asset byte continuity；
- AGENTS、README、文档 208、milestones 四份匿名 raw bytes 等于 exact Git blobs。

canonical reconciliation manifest 位于仓库外，其摘要为：

```text
sha256_json  = dfa90985976a28e9b5f821b49d80ee2ab1bafa98f0e2db726b302ed94b19bf4e
sha256_bytes = de204fc9df0d53e49d0c91c42f646e86a79fb395617c3ba6cec69d2cac8b5b32
```

该 manifest 属于本地证据链；摘要不使 Artifact 自动成为远端文件，也不替代本冻结发布自己的门。

## 6. 本发布自己的最后门

本发布只允许修改 AGENTS、README、文档 208、milestones，并新增本文。doc208 第 2–14 节语义、上游 frozen
documents、architecture DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus、identity vectors、Provider 与
wire implementation 必须保持原字节。

提交前须完成适用 Markdown/Schema regression 的双 Python normal/`-O` 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff scope、合同语义 continuity 与 `git diff --check`。这些本地门
不能替代本发布自己的 original required checks。

本发布候选施工中，第一次四格命令误写了仓库不存在的 `tests.test_schema`；四条 lane 都在已完成 4 项 Markdown
测试后以 `ModuleNotFoundError` 停止。最终字节第一次复跑又漏掉 command-local `PYTHONPATH=src`；四条 lane
各自完成 37 项 Schema 测试后，`tests.test_markdown` 因不能导入 `veritrail` 停止。这些结果属于 test-selection /
source-path setup failure，不是产品、合同或文档失败。后继使用 command-local source path 与实际存在的
`tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`，在 CPython
3.10.6 / 3.13.13 normal / `-O` 四条 lane 分别取得 40/40 PASS。

第一次静态检查又错误要求五个发布文件都各自只出现一次同一 frozen marker；文档 208 按既有 publication 结构在
顶部条件状态与后文 future target 中合法重复该词，因此该检查属于 over-constrained harness false positive。后继没有
修改合同字节来迎合错误规则。一次用于联合重跑四格与静态门的 JavaScript 编排又因内嵌 Markdown fence token
未转义而在解析阶段失败，没有子测试或检查启动。后继恢复 per-target marker 检查并正确转义 command source，取得
507 个含图片资源的 relative links、UTF-8 without BOM、
LF/final LF、balanced fences、exact five-file scope、无敏感本机路径与 `git diff --check` PASS。文档 208 第 2–14 节
继续逐字节等于候选 exact main，SHA-256 为
`80b028830684815dc8f39daef1dbbf67038c6187f37734e068a77be01b9bb046`。上述 setup / harness failures 均保留原身份；
后继 PASS 不把它们倒写成未发生。

```text
publication final bytes
    -> original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 文档 208 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen / implementation-allowed state takes effect
```

任一非成功观察保留原身份；诊断不计入资格，后继成功不改写旧 observation。不得复用候选 Evidence、拿 PR #221
或 `main@f4d531bd...` 的绿灯替代本发布门，也不得在结果出现后修改验收标准。

## 7. 后继停止线

本文最后门全部成立后，先回到 CONTROL LOOP，从新的 exact main 重新判断 A 是否仍是最小合法问题。
`IMPLEMENTATION_ALLOWED` 只授权 doc208 第 14 节 A–G 按停止线严格串行；它不表示任何实现已开始，也不允许按
文档编号自动施工。

persistence、真实 parser/AST、Parse terminal、Fact fulfillment、public carrier/Schema、shared receipt/ledger、
ReviewSliceSet/Coverage、Evidence、Manifest、publisher、Bundle、CLI、Workbench 与其他顶层轨均不由本文开始。

冻结原则为：**确定性 eligibility 只决定 exact source-body operation 的上界；每个实际 operation 仍必须证明自己的
purpose、same-attempt authority、one-shot claim 与 exact Provider-visible body set。**
