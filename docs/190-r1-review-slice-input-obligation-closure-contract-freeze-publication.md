# R1 ReviewSlice Input / Obligation Closure 合同冻结发布

日期：2026-09-23

## 1. 发布对象与条件状态

本文只发布[文档 189](189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md)已经审议的
最小合同，不实现 BFS、ReviewSlice、ReviewSliceSet、CoverageLedger、Schema、publisher 或公共 Bundle。

| 坐标 | 值 |
| --- | --- |
| 上游冻结状态 | `R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN` |
| 前置审计 | [文档 188](188-r1-post-admission-review-slice-input-obligation-closure-system-audit.md) |
| 合同 | [文档 189](189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md) |
| 候选 PR | `#179` |
| 候选 base / head | `0c2ab31671a89b7c96fb5a44c390c85e7820c8c5` / `c73f4007e6a7ffd8dffa0ba1a0d1d58167c85a9e` |
| 候选 merge / tree | `adbf2e50ee4cadb2b94e2b79e297c60f1c40a28b` / `dc05964476fbd856d1f26e0ea9f71fddeda50da2` |
| 影响层级 | `L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

本文分支、原始远端门、受保护主线合入、合入后 exact-main Public CI / Browser Smoke 与本文专属 fresh
anonymous installed-product readback **全部成立以后**，目标状态才是：

```text
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN
R1_POST_ADMISSION_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_PRECONTRACT_AUDITED
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_FROZEN
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

在本文最后一项门成立前，文档 189 的 `CONTRACT_CANDIDATE` 仍是最后已证事实。本文不能因为写出了目标
状态而提前授权 runtime。

## 2. 冻结的最小对象

冻结对象是 **admitted-graph input continuity、authoritative anchor/spec obligation domain 与逐项履责闭合的
最小合同**：

```text
exact DerivationInputSet
+ exact owned qualification history
+ exact OwnedRelationSetAdmissionState
+ same-attempt live continuation
    -> deterministic input join
    -> exact FactSet + Policy/Profile reconstruction
    -> conflict gate
    -> authoritative anchor/spec obligation domain
    -> exactly-once assignment/outcome accounting
    -> private reconciliation and closure receipt
```

该合同把以下层保持独立：

```text
RelationSet admitted
    != Slice execution eligible
responsibility enumerated
    != responsibility fulfilled
self-consistent denominator
    != authoritative denominator
semantic Slice identity
    != attempt-bound execution authority
```

raw RelationSet、digest-only、caller witness、caller boolean 与 fresh BudgetContext 都不能替代 join。application
只能重建并验账，不能从 candidate absence、Coverage 或成功 terminal 猜 negative、gap 或 complete。

## 3. 冻结的不变量

1. normal Slice phase 只能消费同一合法 attempt 连续传递的 exact inputs、owned qualification/admission history 与
   live continuation；同 limits 的新 BudgetContext 仍是新 authority；
2. obligation domain 由 sealed Policy/Profile 与 exact FactSet 机械产生，不由 provider、caller、Slice output 或
   Coverage denominator 自报；
3. `CONFLICTING` admitted graph 保持 denominator `UNKNOWN` 并阻止 normal traversal；只有 exact FactSet 确实没有
   eligible anchor 时，空 domain 才是 `KNOWN CLOSED_EMPTY`；
4. 每个 eligible anchor 精确产生一个完整 `ReviewSliceSpec`；assignment、outcome、Slice candidate 与 domain 必须
   双向闭合，不得漏项、重复、跨 domain 或跨 attempt 引用；
5. normal outcome 只允许 `NORMAL_COMPLETE / NORMAL_PARTIAL`；partial 必须保存结构 frontier，timeout/cancel/
   unavailable/failed 不得留下 normal Slice authority；
6. semantic domain 与未来 Slice content identity 可以由两个合法 attempt 独立得到相同 bytes；closure receipt
   必须逐 attempt 建立，不能因 content digest 相同而继承；
7. `QUALIFIED` 只证明本合同责任域闭合，不等于 ReviewSliceSet admitted、Coverage complete、Attention correct、
   finding true 或 final Evidence；
8. 现有 public Schema 若没有新反例证明不足就保持不变；private proof 不得为了方便提前创建 public Artifact。

## 4. 合同候选的本地与远端资格

文档 189 的最终字节在同一 source state 上完成 Review Attention full regression：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `210/210 / 407.476s / OK` |
| CPython 3.10.6 `-O` | `210/210 / 396.149s / OK` |
| CPython 3.13.13 normal | `210/210 / 397.976s / OK` |
| CPython 3.13.13 `-O` | `210/210 / 392.202s / OK` |

Core version-contract gate 在正确的 CI source-root topology 下完成双 Python normal/`-O` 四格 `5/5`。第一次
本地命令没有设置 `PYTHONPATH=src`，在 import `veritrail` 时停止，任何被声明测试都没有启动；该记录只属于
local gate setup failure，不能伪装成产品首败或被后继 `5/5` 改写成已经执行。

Markdown/static 门检查 421 个 relative links，`git diff --check`、UTF-8/LF、无 BOM、fence/heading、状态 marker、
本机路径与敏感模式均通过。`docs/assets/veritrail-architecture.dot/.svg` 相对 base 保持 Git blob identity，因为本
合同没有改变能力拓扑。

候选随后以 ordinary merge commit 进入受保护 main：

```text
PR #179 Public CI   35818391398  pull_request / attempt 1  11/11 SUCCESS
candidate merge    adbf2e50ee4cadb2b94e2b79e297c60f1c40a28b
Public CI           35819851821  push / attempt 1          11/11 SUCCESS
Browser Smoke       35819851827  push / attempt 1           1/1 SUCCESS
```

PR head、push run 与三个 readback 都绑定同一候选树 `dc05964476fbd856d1f26e0ea9f71fddeda50da2`；PR
只修改 `AGENTS.md`、`README.md`、文档 189 与 `docs/milestones.md`。

## 5. 候选 exact-main 匿名产品读回

读回从 detached exact `main@adbf2e50...` 取得 orchestration probe，在 fresh CPython 3.13 venv 中只安装固定
公开 wheel 与 matching Playwright/Chromium：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

GitHub token 环境被清空；README、文档 189 与 milestones 分别使用不同 Plan ID、Plan digest、collection
session 与 output root：

| Target | Session | Plan digest | Handoff | Report |
| --- | --- | --- | --- | --- |
| README | `github-paired-662dcade34c34fd6adfa933dfd2f76ef` | `41447453ffc6a18cf5650649e17dfac4906ef1508343c229c1457d7a1fbf1e36` | `22c99c8af5184028a9d39a2537a25e1d70252cd6c1b612a67aee220723280687` | `21bc37591b57a0b97c35a2c0f872c062c585078b7e2e75de8981361f5ea9746e` |
| Document 189 | `github-paired-bc78db97ea8e4bec8804adb4a09bb6da` | `fe508ea9cbcc80ade4888121bbaf3295dc2e7ac6c549af4a9ab4e63c8f4ad50d` | `08225d8587c69d7b149ad4e2ab56d5a328a10b5c52a53033c5488ec12688dbdb` | `0591d1d767e25e272b252aed8c3478ab7a48eecca54ea10817ff57e22a0c161c` |
| Milestones | `github-paired-29b15c4dd54b4a0c88a531209d0290e9` | `6cd9f08522a0407bdc037b9f71d591df1f41d47dc7a6ad315c02eaa2c7591b5d` | `99a5d3ecd1f7c1a7356288e9474301556b3d662d886bd2a58532823a68111fad` | `5a8d9d3d93f346f077de2274d8a0538eddb513fc7a3b5ccbbc7be7cbf2c88166` |

三次均为 HTTP 200、requested/final exact-SHA path 相同、P1/P2 coverage `COMPLETE`、三样本稳定、唯一 marker、
零 conflict/error/coverage reason/cleanup error、零 active stream，Core verdict `PASS`。三个 canonical summary
按 README / 文档 189 / milestones 顺序连接后的 SHA-256 为：

```text
170f3a6015af99381f4eb0d7b3d7b7ba29b4e860686bead4a3ab3a338fc59721
```

联合 verifier 又复算 sealed Plans、Evidence、handoff、reports、session/Plan 不复用、四份变更文件的 Git
byte identity、merge ancestry、tree、wheel 与 architecture asset continuity。canonical manifest 为：

```text
sha256_json  = 780beec326fdc9f9fbb934229af8a5550426558ec46139e54f100dd4ac34031e
sha256_bytes = c18e26f824275ad231bb9075f788c5c7030d2cbe9d6d5e459e0489f450530845
```

这些事实只使候选有资格进入本文，不能替代本文自己的最后门。

## 6. 有限实现授权与停止线

本文最后门全部成立后，下一分支只能从新的 exact main 严格串行实现文档 189 第 11 节 A–H：

```text
A. same-attempt continuation and admitted-graph input join
B. exact FactSet reconstruction + Policy/Profile/admission cross-validation
C. conflict gate + deterministic anchor/spec obligation domain
D. private obligation assignment and deterministic traversal boundary
E. normal COMPLETE/PARTIAL outcome + structural frontier proof
F. missing/duplicate/dangling/cross-attempt reconciliation
G. zero-anchor closed-empty + conflict/upstream-unknown negative worlds
H. RS-000..016 hardening and cross-runtime byte proof
```

A–H 只能形成 private values 与测试。不得写 output root，不得创建公共 ReviewSliceSet/CoverageLedger/Evidence/
Manifest，不得修改 Schema/corpus/identity vector，不得开始 Attention ranking、human disposition、CLI、Workbench、
D、Cu、Q、O 或 T runtime。

如果实现要求 publisher、公共 Bundle、Schema patch、独立 Slice Provider 或 fresh BudgetContext 才能成立，必须
停下，以新反例重开被击穿的最小边界；不能把本文的合同冻结解释成对该扩张的授权。

## 7. 本状态发布自己的最后门

本 docs-only publication 只允许同步 `AGENTS.md`、`README.md`、文档 189、`docs/milestones.md` 并新增本文；
architecture DOT/SVG 因拓扑未变而必须保持字节不变。提交前必须通过适用双 Python normal/`-O` regression、
Markdown relative links、fence/heading、状态 marker、敏感模式、本机路径、exact diff scope 与
`git diff --check`。本地结果不能替代本文自己的远端 required checks。

本 publication worktree 先串行运行 `test_relation_set_admission + test_boundaries`，把首轮计时写入本文；
证据文字写定后，最终字节又完整重复同一四格并保持每格 `24/24 / OK`：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `24 tests / 29.741s / OK` |
| CPython 3.10.6 `-O` | `24 tests / 29.552s / OK` |
| CPython 3.13.13 normal | `24 tests / 29.648s / OK` |
| CPython 3.13.13 `-O` | `24 tests / 31.294s / OK` |

Markdown runtime regression 在 CPython 3.10.6/3.13.13 下各为 `4/4`。最终静态门精确读取五份 docs-only
文件，检查 428 个 relative links 且零断链；UTF-8 无 BOM、LF-only、fence 平衡、heading 无重复、五份文件
均包含目标 frozen marker、无 tab、本机绝对路径或敏感 token-like value。exact diff scope、
`git diff --check` 与 architecture DOT/SVG byte continuity 均成立。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_FROZEN
```

任一新反例都可否决冻结或只重开被击穿的边界。不得用 PR #179、candidate exact-main 门或 candidate
readback 替代本文自己的最后门；在完整链成立前不得写 runtime。

当前原则冻结为：

> Responsibility enumerated is not responsibility fulfilled; a complete-looking denominator is not authoritative
> until its exact obligation world and attempt-bound closure are independently established.

中文：**责任被枚举不等于责任已履行；看起来完整的分母，只有在精确责任世界与 attempt-bound 闭合都独立成立
以后，才有资格成为权威分母。**
