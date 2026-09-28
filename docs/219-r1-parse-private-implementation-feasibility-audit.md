# R1 Parse fulfillment private implementation 可行性审计

日期：2026-09-28

> 当前条件状态：
> `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@bb912680d55ca8c96df4d5b9ded88187bbaf42ef`，Git tree
> `a38418c758f8376aa48d1c1b71b70e5540fb03e4`
>
> 冻结合同：[Parse fulfillment 最小合同 0.1](217-r1-parse-fulfillment-contract.md)
>
> 冻结发布：[Parse fulfillment 合同冻结发布](218-r1-parse-fulfillment-contract-freeze-publication.md)
>
> 影响层级：`L2_IMPLEMENTATION_FEASIBILITY_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本文不修改
> runtime、tests、Schema、Profile、Policy、corpus、identity vector、Provider、Fact/Relation/Slice/Coverage、
> Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 问题与结论

文档 218 的全部冻结门已经闭合，因此 `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN` 是当前事实；合同冻结本身没有
授予实现权。本文重新进入 CONTROL LOOP，只问：

> 能否在不选择 persistence、不修改 public identity、不改 current Fact wire、不借用 Fact output authority，且不把
> 宿主 Python 冒充 CPython 3.10.6 reference 的前提下，形成完整的 private Parse fulfillment closure？

结论是：**可行，但只在显式 exact-reference-runtime boundary 下可行。** 最小闭包为：

```text
exact inputs + frozen Language Support classification + original live attempt
    -> exact ELIGIBLE denominator
    -> per-subject one-shot child claim
    -> explicitly selected CPython 3.10.6 reference worker
    -> candidate ACCEPTED(product) | REJECTED(PARSE_ERROR)
    -> application-owned lifecycle validation and complete reconciliation
    -> private admitted product / product-set semantic value
    -> separate one-shot same-attempt continuation
```

当前 `_windows_execution_cell.py` 已允许 controller 以一个显式绝对 executable 路径在同一 `BudgetContext` 下运行隔离
child；当前 source gate 又已经证明 fresh context、equal classification、equal inputs 与 equal projection 都不能替换
原对象身份。审计 probe 进一步证明 exact CPython 3.10.6 worker 可以由 3.10.6 或 3.13.13 parent 启动，并在四格中
产生逐字节相同的 private product projection。

这不授权直接使用 ambient `sys.executable`、`py -3.10`、PATH 搜索、descriptor 自报或 3.13
`feature_version=(3, 10)`。若 exact reference runtime 不存在、版本不符、worker 失败、超时或资源停止，只能形成
lifecycle non-success；不得伪装 `PARSE_ERROR`。

本文仍只是 docs-only candidate。它自己的资格链闭合以前，runtime 继续 `NOT_STARTED / NOT_AUTHORIZED`。

## 2. exact source state 与冻结资格

冻结候选 PR #240 与独立发布 PR #241 的坐标为：

```text
contract candidate
base  = 63daada4157e0068bb2a1333953f821f56f61894
head  = cf26f4224ef17549d5e086bfcd599de3163358d4
merge = 446604ffc437ff710faf524c1634839dc1a0ddd7
tree  = aa9099f6c4667c39c7493743245a523ca9626351

freeze publication
base  = 446604ffc437ff710faf524c1634839dc1a0ddd7
head  = 562744ac6d01787470069c28a0d21fdc3655136f
merge = bb912680d55ca8c96df4d5b9ded88187bbaf42ef
tree  = a38418c758f8376aa48d1c1b71b70e5540fb03e4
```

PR #241 original Public CI `36430339164` attempt 1 为 11/11 SUCCESS；exact-main Public CI
`36433373130` attempt 1 为 11/11 SUCCESS，Browser Smoke `36433373070` attempt 1 为 1/1 SUCCESS。

final installed-product readback 中 README、doc217、doc218 与 milestones 使用四个 fresh Plan/session 取得 PASS。
milestones 第一次正式 observation 的 API projection 完成，但 render projection 以
`RENDER_NAVIGATION_FAILED / NAVIGATION_NOT_OBSERVED / NAVIGATION_PROJECTION_MISSING` 结束；139 个 request、101 个
完整 response body、零 request failure、零 active stream、零 cleanup/page/conflict error，精确根因保持
`UNKNOWN`。该 observation 永久保持 `ERROR / NON_QUALIFYING`，后继 fresh milestones #2 PASS 不覆盖它。

independent verifier 同时核对候选期保留的 README 匿名 API rate-limit ERROR、上述 final milestones ERROR、四份 fresh
qualifying readback、PR/merge/tree/CI identities、五份 raw source bytes 与安装版 Core 复算，最终 manifest 为：

```text
sha256_json  = 318b2a3ab2700faf2e8dfe481e3a7969ce3c084dee9a96a05e3dd306c471d638
sha256_bytes = 64fa5d2cf7135d6a4ee1cca8ce792f199bda4298ad60667b1607abc242b30381
```

formal observation 前的 managed-worktree `Not a git repository` 与 Playwright preflight shutdown
`TargetClosedError` 均保留为 setup/preflight history；它们没有 Plan/session/product output，不计入资格。上述门已经
满足文档 218 预先声明的标准；本审计不追加事后冻结条件。

## 3. current public projection 的一处矛盾

exact main 的 README 顶部状态、AGENTS 与 milestones 已声明 Parse contract frozen，但 README“系统家族与未来边界”
表格仍写着：

```text
Parse fulfillment authority problem boundary 已 qualified，最小合同前置审计处于 candidate；
Parse contract/runtime ... 仍未开始
```

该行是从早期 source state 留下的 current-summary prose，不是历史记录。它与同一 README 顶部
`R1_PARSE_FULFILLMENT_CONTRACT_FROZEN` 矛盾。本文同步把它更正为：

```text
Parse fulfillment contract 已冻结；private implementation 仍未开始；
当前只处于 implementation feasibility audit candidate。
```

这项修正不重开 doc217，不改变冻结资格，也不把审计结果提前写成 implementation fact。历史章节中的
`CONTRACT_CANDIDATE` 与失败身份继续原样保留。

## 4. current implementation topology

### 4.1 可以复用的 exact-world 与 live-authority 边界

当前代码已经提供：

- `DerivationInputSet` copy-own Snapshot / Policy / Profile canonical bytes 与 verified Git blob bytes；
- `OwnedLanguageSupportClassification` 0.2 copy-own完整 denominator、eligible/unsupported partition、exact subject
  semantic input 与 effective encoding；
- `OwnedSourceOperationAttemptGate` 将 exact inputs、classification、original `BudgetContext` 与 parent
  `AttemptEligibility` 按对象身份绑定，并给每个 child 发放 one-shot claim；
- `_windows_execution_cell.run_windows_execution_cell()` 在 process resume 前完成 containment 与 eligibility
  admission，并把 stop/release facts交还 application；
- current multi-provider controllers 证明同一 live context 可以顺序完成多个 child phase，而 parent authority 不在
  第一个正常 child 后自动终结。

这些结构不自动等于 Parse closure，但足以说明 Parse 不需要新建第二套 budget primitive，也不需要从 Fact output
反向恢复 authority。

### 4.2 current Fact source operation 不能静默升级

`private-source-operation-projection/0.1` 与 Fact wire `/0.2` 当前仍把 Language Support eligible source bodies 作为
authority object；request、terminal 与 source gate 都没有 Parse product、Parse result 或 complete Parse
reconciliation 输入。它们可以继续解释历史 pre-Parse wire，但不能通过增加一个 digest 字段静默成为 post-Parse
consumer boundary。

因此本轮实现若以后获准，只能停在 application-owned admitted Parse product set 与 private continuation。它不能在
同一分支修改 Fact request/projection、启动 Provider、决定 zero-accepted scheduling 或声称 product-use proof。

## 5. exact reference runtime boundary

### 5.1 ambient host 没有 parser authority

文档 214 已证明较新宿主的 `ast.parse(feature_version=(3, 10))` 只是 best-effort；同一 function/class source 在
3.13 AST 中出现 3.10 没有的 `type_params` fields。文档 217 又记录同一 NUL input 在 3.10.6 reference 与 3.13.13
host 中分别产生 `ValueError` 与 `SyntaxError`。终态都可归一为 `PARSE_ERROR`，但 host AST shape 与 exception class
都不能拥有 0.1 语义。

private implementation 因此必须把 reference runtime 作为显式 controller-owned capability：

```text
trusted explicit absolute executable selection
    -> bind executable identity for this prepared attempt
    -> launch the same executable through the contained cell
    -> worker requires CPython 3.10.6 exactly
    -> no PATH / py launcher / ambient interpreter fallback
```

worker 的 version response 只作一致性检查，不能单独从自报 metadata 创造 authority。controller 对 trusted runtime
selection 的权限模型与恶意 host binary attestation 不在本合同内；若未来需要跨机器供应、下载、签名或远程证明，必须
另开 deployment/security seam。当前 private implementation 不得自动下载 runtime 或修改系统安装。

### 5.2 exact runtime absence 是 lifecycle fact

若 executable 不存在、不是 CPython 3.10.6、process 无法启动、worker 非零退出、terminal malformed、资源停止或
release 失败，application 不得制造 per-subject semantic result。完整 denominator reconciliation 随后失败；该 world
没有 normal product set 与 continuation。

这允许 package 继续在 Python 3.13 host 上运行，同时不把 3.13 host parser 当成 reference。可用的 3.10.6 runtime
是 Parse capability 的运行前提，不是整个 VeriTrail package import 的前提。

## 6. private product 可以有界且 copy-owned

audit worker 只在 exact 3.10.6 中调用 frozen invocation，并将返回的 `ast.Module` 投影为私有 canonical tree：

```text
every AST node type
+ every `_fields` member recursively
+ every present `_attributes` member recursively
+ ordered list membership
+ explicit scalar encoding
```

scalar witness 覆盖 `None / bool / int / str / bytes / float / complex / Ellipsis`；float/complex 使用 exact hex text，
bytes 使用 Base64。locations、type comments、operator/context singleton nodes 与 `type_ignores` 都保留。该 projection
由 reference worker 产生，3.13 parent 只验证 canonical shape、binding 与 digest，不重新 parse，也不依赖 3.13 AST
classes。

这证明首版可以使用 **private same-attempt canonical copy-owned value** 作为 admitted product，而不创建 public AST
Schema、Bundle file 或历史 persistence promise。terminal 超限、unsupported scalar 或 projection failure 都是 lifecycle /
internal non-success，不得降格为 semantic rejection。

## 7. authority topology

| Authority | Owner | 明确不拥有 |
| --- | --- | --- |
| Parse denominator | application 从 exact Language Support `ELIGIBLE` subjects 导出 | parser、Fact Provider、caller subset |
| exact decoded input | application 重验 exact blob 与 effective encoding | worker tolerance、locale、fallback decode |
| parser function | frozen 0.1 + controller-owned exact reference runtime boundary | ambient host、descriptor/version string |
| per-subject observation | one admitted contained reference worker execution | worker 不拥有 denominator complete claim |
| semantic result candidate | reference worker terminal under exact invocation | lifecycle failure 不得生成 `PARSE_ERROR` |
| admission / reconciliation | application 对完整 denominator 机械核账 | Provider output、accepted list、first-success selection |
| product / product-set semantic identity | application-owned private canonical values | subject IDs、reported Fact、bare digest echo |
| live continuation | original context + parent attempt + one-shot Parse claims + complete reconciliation | equal bytes/digest/result from another attempt |

semantic product identity 不包含 executable path、deadline、`BudgetContext` 或 claim handle；prepared attempt binding 必须
另行绑定 exact runtime selection 与 live objects。相同 product bytes 可以跨 attempts 复算，但不能继承 live claim。

## 8. 最小实现面

本文自己的全部资格门与后继独立授权发布闭合后，下一分支最多实现以下 private stages：

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

实现必须继续满足：

1. 全部新对象与函数保持 `veritrail_review` private，不进入顶层 exports、CLI、entry point 或 plugin discovery；
2. 不重新读取 repository path，不重新运行 encoding detection，不允许 rejected/unsupported raw body 进入后继 consumer；
3. 每个 exact subject / parent attempt 只有一个共享 obligation；worker 或未来 Fact Provider 数量不复制 Parse truth；
4. application 必须收齐并核对完整 denominator 后才形成 product set；不得 first-success、best-effort subset 或自动 retry；
5. zero denominator 与 all-rejected complete 可以形成语义不同的 known-empty product sets；missing/non-success 不得伪装
   empty closure；
6. private canonical bytes/digest 只作 semantic identity，不是 public Artifact、Evidence、Coverage denominator 或 persistence
   决策；
7. 任何正常 continuation 必须 one-shot 绑定原 `BudgetContext`、parent eligibility、exact classification、所有 Parse
   claims、complete reconciliation 与本次 product-set binding；
8. current Fact projection/request/wire、Provider scheduling 与 product-use enforcement 保持原字节。

## 9. 必须拒绝的实现推理

| ID | 已知 world | 必须拒绝的结论 |
| --- | --- | --- |
| `PFI-000` | Language Support subject 为 `ELIGIBLE` | 已取得 Parse semantic result |
| `PFI-001` | `sys.executable` 可执行 `feature_version=(3,10)` | ambient runtime 拥有 0.1 function authority |
| `PFI-002` | worker 自报 `CPython 3.10.6` | metadata 本身建立 trusted runtime selection |
| `PFI-003` | exact runtime unavailable | 可回退 ambient parser 或声明 `PARSE_ERROR` |
| `PFI-004` | exact AST product 由 reference worker产生 | 3.13 parent 可重新 parse 并替换 product |
| `PFI-005` | source grammar reject | 可声明 `UNSUPPORTED_SYNTAX_VERSION` |
| `PFI-006` | top-level `return` 形成 product | source compile-valid 或 executable |
| `PFI-007` | NUL 在不同宿主抛不同异常 | exception class拥有不同 canonical reason |
| `PFI-008` | 多个 future Fact Providers 需要同一 source | Parse obligation / product 按 Provider 数量复制 |
| `PFI-009` | 一个 child 正常完成 | parent context 或 denominator 已全部关闭 |
| `PFI-010` | missing / duplicate / dangling / foreign/cross-world result | application 可择一或按 accepted subset继续 |
| `PFI-011` | accepted subject IDs 相同 | exact products / product-set identity 相同 |
| `PFI-012` | product-set bytes相同 | 另一 attempt 可继承 continuation |
| `PFI-013` | zero denominator 或 all rejected | Fact/Coverage 自动 `CLOSED_EMPTY` |
| `PFI-014` | current Fact wire 可接收 eligible raw bytes | post-Parse product-use boundary 已成立 |
| `PFI-015` | audit corpus与四格全绿 | 已证明全部 Python grammar 或恶意 runtime authenticity |
| `PFI-016` | frozen contract 存在 | runtime 可在本文资格链前开始施工 |

这些 falsifiers 是实现边界；测试只能成为 witness，不能扩大它们。

## 10. audit-only probes

仓库外审计目录：

```text
<local-workspace>/tmp/parse-implementation-feasibility-audit/
```

脚本 SHA-256：

```text
4e129e42039c0ed5f0170828a9d038ac941e7289a072b4d211c0c4081018bb7f  parse_reference_worker.py
6b6957d7506441735ed87fe41547c7f3e63fed6b78a869fd9dbfe56a79f42fa5  feasibility_matrix.py
2980ce3c1ca935514c9713a3fbf57b2efd67b03c326347df0a46c6127d211872  cell_probe.py
```

本机 explicit reference executable 为 CPython 3.10.6，probe 记录其文件 SHA-256：

```text
32ce1d2650ea8b9d394f5b8f94677d27888dccdc3713365bf903a8c465c9d776
```

`feasibility_matrix.py` 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格均生成 11229-byte canonical report，
逐字节相同：

```text
f7c84c90534a464d87ffa62562f8fcca8ee76acd4d714a5ac0a27ae1041897ee
```

它验证：valid function/literals/match/top-level return 均 accepted；`except*`、ordinary invalid 与 NUL 均只形成
canonical `PARSE_ERROR`；3.13 executable 被 worker 明确投影为 `REFERENCE_RUNTIME_UNAVAILABLE` 且没有 semantic
result；missing、duplicate、dangling、foreign-attempt、cross-world 与 lifecycle non-success 均被 reconciliation 拒绝；
两次 attempts 可产生相同 product-set digest，但 continuation 不继承；zero denominator 与 all-rejected complete 的
product-set digests 不同。

`cell_probe.py` 使用仓库当前 Windows execution cell，在 3.10.6 / 3.13.13、normal / `-O` 四格各生成
2004-byte canonical report并逐字节相同：

```text
dd35740dababf2a8113b4d788f28129584934603b0e5795ae119b45edff8aa8e
```

同一个 original `BudgetContext` 先后运行两个 exact reference children；两次 admission callback 各一次，child
eligibility 均为 `ADMITTED`，resources 全部关闭、exit code 0、无 stop trigger，accepted 与 rejected terminal 都能
完成 phase commit，context 在第二项以后仍为 `RUNNING`。这只证明现有 containment/budget shape 可承载多
obligation；它不是最终 runtime实现或全部 grammar conformance Evidence。

施工时第一次尝试把本节状态同步到 `AGENTS.md`，因补丁预期锚点与 actual final bytes 不一致而在应用前失败；没有
文件发生 mutation。随后重新读取 exact bytes，再使用实际锚点完成修改。该事件保持为 operator/patch-setup history，
不是 product、contract、probe 或 qualification failure。

final static checker 的第一次工具编排也在 shell 启动前被拒绝：外层 JavaScript template literal 与待检查的 Markdown
fence 字符冲突，形成 `SyntaxError: Invalid or unexpected token`。没有命令执行或文件 mutation；后继使用无该歧义的
PowerShell checker 重新开始。该事件同样只保留为 tool-wrapper/setup history，不计入产品资格。

candidate commit 已成功创建后，同一施工命令末尾第一次查询 Git tree 时未引用 PowerShell 中的 `HEAD^{tree}`，
metadata query 被 shell 错误解释并失败；commit 已存在，失败查询没有再修改内容或 index。后继以 quoted revspec
重新读取 tree。该事件保持 operator/shell-setup identity，不改变 candidate qualification。

## 11. 本文明确不决定

```text
public Parse Schema / corpus / identity vectors
historical/offline product persistence Route B
Bundle self-contained parser/product verification
runtime download / installation / signing / remote attestation
Fact consumer correction projection, request or wire
Fact Provider scheduling and product-use enforcement
zero-accepted required-provider behavior
Fact obligation-universe derivation / fulfillment
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root
Attention / CLI / Workbench / Core / Q / O / T
```

private in-memory canonical product 只实现合同允许的 same-attempt Route A；它不把 persistence 的未来选择关闭。

## 12. 本候选的资格门

本 docs-only 候选只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。doc217/218、runtime、
tests、Schema、Profile、Policy、corpus、architecture DOT/SVG 与 identity vectors 必须保持原字节。

提交前必须通过适用双 Python normal/`-O` docs/Schema regressions、relative links、UTF-8/LF/final-LF、
heading/fence、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与 `git diff --check`。随后必须完成：

当前 final candidate bytes 已完成本地资格：CPython 3.10.6 / 3.13.13、normal / `-O` 四格的适用
docs/Schema suite 均为 40/40 PASS；改动范围精确为 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
relative links、UTF-8 without BOM、LF/final-LF、heading/fence、状态 marker、敏感路径与 `git diff --check` 均通过。
冻结 doc217 / doc218 的 Git blob 继续分别为 `0032f6c3c4b90f78f714920982fa373bbb5cb13d` 与
`9fa5e1884a3edcb614d3bf9f1218c57acfc36a36`。

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> feasibility audit becomes qualified history
    -> return to CONTROL LOOP
    -> independent docs-only implementation authorization publication
```

任一非成功观察都保留原身份；后继 PASS 不覆盖首败。audit probe、绿色 CI、合同冻结与本文编号都不能使 runtime
提前开始。README current-summary correction 与本审计共享同一 candidate identity；若本文不取得资格，该更正仍只是
未合入 candidate bytes。

## 13. 后继停止线

本文最后门闭合后，下一步也不是直接写 parser。必须先重新绑定新的 exact main，确认 reference-runtime boundary、
public projection 与上述 falsifiers 没有被新证据击穿，再以独立 docs-only publication 明确发布：

```text
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

只有该 publication 的自身门闭合，private A–H implementation 才可创建。若后继证明 exact 3.10.6 runtime 无法在不
新增 deployment/public authority 的情况下提供，或 private product 无法在不选择 persistence 的情况下供 same-attempt
consumer 使用，则停止并只重开被击穿的最小边界。

原则保持：**exact parser observation 可以生成 semantic product；只有完整 application reconciliation 与原 live
attempt 才能把它升级为可继续消费的 admitted product set。**
