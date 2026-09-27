# R1 Language Support eligible operation projection / same-attempt gate 实现冻结候选

日期：2026-09-28

## 1. 当前裁决

> 条件化状态目标：`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED /
> R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FREEZE_CANDIDATE /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 208](208-r1-language-support-eligible-operation-projection-contract.md)
>
> 合同冻结发布：[文档 209](209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)
>
> 实现 PR：[#223](https://github.com/NoctilumeDev/VeriTrail/pull/223) 至
> [#229](https://github.com/NoctilumeDev/VeriTrail/pull/229)
>
> 最终实现 exact main：`b69527ec3a4c3037be730144c29b0ce2468940fc`

文档 209 的最后门闭合后，CONTROL LOOP 重新确认文档 208 第 14 节 A–G 仍是最小合法施工面。七个
stage 随后按停止线串行进入受保护 main；每一刀都使用独立 PR、original required checks、ordinary merge 与
new exact-main Public CI / Browser Smoke，未把前一 stage 的绿色继承给后一 stage。

本文只记录 A–G private implementation 的 exact identity、合同闭合、测试 witness 与冻结候选资格。本文自己的
远端门、受保护合入、新 exact-main 双门、fresh anonymous installed-product readback 与后继独立最终状态发布全部
成立前，不得写成
`R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN`。persistence、真实 parser / AST、
Parse terminal、Fact fulfillment、public carrier / Schema、ReviewSliceSet / Coverage 与发布能力均没有从本实现取得
authority。

## 2. 实现边界

本次 private implementation 只物化以下链条：

```text
frozen Language Support classification
        -> attempt-neutral stage operation projection
        -> original BudgetContext / parent AttemptEligibility
        -> distinct one-shot child claims
        -> filtered request encoded after projection
        -> exact Provider-visible body equality
        -> corrected Fact / Relation derivation / Relation observation wires
        -> controller integration and downstream history revalidation
        -> LSPC-000..018 direct hardening
```

application 拥有 projection construction 与 exact-history revalidation；Provider 不拥有 eligibility、operation
denominator、projection、attempt 或 fulfillment authority。相同 semantic input / classification / projection bytes
可以复算相同结果，但不能继承原 `BudgetContext`、parent/child `AttemptEligibility`、one-shot prepared frame 或
ProviderRun identity。

empty denominator、all-unsupported world 与 applicable child 的 later-empty assignment 保持不同 identity。
applicable empty child 仍真实运行 exact empty-body request，但它的 terminal 不生成 Parse、Fact 或 Coverage
fulfillment，也不形成更高阶 closure。

## 3. A–G exact implementation chain

合同冻结后的实现起点为 `main@e0997266bb485b3f49bf1076d4fda6b9dbd46dc7`。七个 stage 的 identity
如下；每个 PR 均只有一个实现 commit，original Public CI 均为 attempt 1、11/11 success。

| Stage | 对象 | PR head | Merge / exact main | PR Public CI | Exact-main Public CI | Browser Smoke |
| --- | --- | --- | --- | ---: | ---: | ---: |
| A | private operation projection | `1484420de9461a0360b754e80f16d17c9e6c162a` | `aaad8ea2808513b268e8d39cad0f82c370b29fde` | `36289355151` | `36290394026` | `36290394010` |
| B | same-attempt gate / child claims | `0934dec2bb2f767864b73def39ae2de3f3cd9dd4` | `e81ddbbdad6b436e3edf5e9e7dbbc36b6bbb2caf` | `36294946569` | `36296004496` | `36296004471` |
| C | Fact wire `0.2` / operands `0.4` | `ab5e2884be8d1dddf9b3bec50d0dba72454f6ee6` | `82d1887b1b413ebd9a2179240f78e6e8749b4a94` | `36300898706` | `36301942808` | `36301942810` |
| D | Relation derivation wire `0.3` / operands `0.5` | `5a92458407b0a20c256aa7528a94c728d228f8f6` | `b0a5a035ec1401c346850d2b00d54b156a23545e` | `36304549283` | `36305623390` | `36305623405` |
| E | Relation observation wire `0.4` / operands `0.6` | `03d23aa5df51c82bbde344e8985b8173c2da23f3` | `07116fc4d9830470b6adf9c534222ee1b1feecee` | `36308341038` | `36309512627` | `36309512693` |
| F | controller integration / history revalidation | `b5fc19500836b65d1812945988a9872467b5ef7d` | `7658db401d1a78ff324c3c1776013c1f9ce22ffa` | `36317868121` | `36319123131` | `36319123124` |
| G | `LSPC-000..018` hardening | `0d9319a1906c5ab5a7ccc3639f4b48944cb3cd79` | `b69527ec3a4c3037be730144c29b0ce2468940fc` | `36328081523` | `36329453405` | `36329453485` |

所有表中 run 都是 attempt 1、completed / success；没有 rerun。每个 merge 都是 ordinary two-parent merge，第一
parent 为前一 stage exact main，第二 parent 为表中 PR head。最终 exact main tree 为
`03e564bd0aef728d023ad0b93d539067c7ac8ac7`。

从合同冻结 main 到 G exact main 的累计 Review Attention diff 为 28 个文件、`8365 insertions / 83 deletions`。
变更只位于 private runtime 与 tests；顶层 `veritrail_review` 没有新增 public export，公共 Schema、Profile、Policy、
Evidence、Manifest、publisher、Bundle、CLI、Workbench、architecture DOT / SVG 与其他顶层轨均未改变。

## 4. Stage closure

### A. Attempt-neutral projection

`source-operation-projection/0.1` 绑定 exact classifier result、Provider descriptor、下游 FactSet / domain /
assignment coordinate、完整 eligible upper bound 与 stage-specific operation set。caller 不能提交 path set；值中没有
source body、attempt、budget、continuation、claim、Evidence 或 publication authority。

### B. Same-attempt gate

controller-owned gate 绑定 original `DerivationInputSet`、`BudgetContext`、parent eligibility、classification、
projection、prepared frame、transport limits 与 distinct child eligibility。claim concurrency-safe、one-shot，并在
validation failure 或 parent/context stop 后失效。limits 相同的新 context 与同字节 classification/projection 都不能
替代原 authority。

### C–E. Corrected private wires

Fact、Relation derivation 与 Relation observation 分别使用新 wire `0.2 / 0.3 / 0.4` 与 operands
`0.4 / 0.5 / 0.6`。旧 wire / operands 保持只读；没有 fallback。worker 独立重验 exact world，并只接收当前
operation set 所需的 bodies / Facts。request 仍携带独立验证需要的完整 semantic identity，但不携带 omitted bodies。

### F. Controller integration

三个现有 controller 接入 projection/gate/claim/new-wire 链。RelationSet admission 又从 exact inputs 机械重建并重验
classification / projection history，不能只信下游 terminal 或 operands digest。合法 empty worlds 仍运行适用 child，
并产生 terminal、released outcome；semantic RelationSet 内容不因 authority correction 被改写。

### G. Hardening

`LSPC-000..018` 均有直接 falsifier，覆盖：mixed/unsupported/out-of-scope exposure、exact Fact/Relation operation
set、attempt / budget identity、new wire identity、concurrent one-shot、cancellation、filter-before-encode、三类 empty
world、worker exact-byte reconciliation、omitted-body side channel、cross-attempt splice，以及 Parse/Fact/Coverage
authority boundary。

canonical hardening report 在 CPython 3.10.6 / 3.13.13 normal / `-O` 四格中逐字节一致，SHA-256 为：

```text
dc6ef339570c83af99e7882c3de703ea51e9df91c5b0fd9265bc1b65cbc9ca22
```

## 5. Final-byte local qualification

G exact-main runtime / test bytes已在最终 stage 上严格串行完成以下矩阵：

| Lane | G direct | A–G focused | Related Language Support / controller / Relation | Full Review Attention |
| --- | ---: | ---: | ---: | ---: |
| CPython 3.10.6 normal | `20/20` | `100/100` | `182/182` | `417/417 / 533.140s` |
| CPython 3.10.6 `-O` | `20/20` | `100/100` | `182/182` | `417/417 / 545.505s` |
| CPython 3.13.13 normal | `20/20` | `100/100` | `182/182` | `417/417 / 531.212s` |
| CPython 3.13.13 `-O` | `20/20` | `100/100` | `182/182` | `417/417 / 528.883s` |

G test module最终 SHA-256 为
`8071843b3101454f2917381c4d44adec0803dddbe8eb154f630ad35d7280c81c`。Python 3.10/3.13 compilation、UTF-8
without BOM、LF/final LF、added-line width 与 `git diff --check` 均成立。

本 docs-only candidate 又在未修改的 runtime / test bytes 上严格串行重跑 full Review Attention：

| Lane | Result |
| --- | ---: |
| CPython 3.10.6 normal | `417/417 / 564.844s / PASS` |
| CPython 3.10.6 `-O` | `417/417 / 572.200s / PASS` |
| CPython 3.13.13 normal | `417/417 / 557.563s / PASS` |
| CPython 3.13.13 `-O` | `417/417 / 560.945s / PASS` |

四格没有并发执行，也没有修改 timeout、budget、fixture 或 expected result。记录上述数字后，只受文档内容影响的
docs / Schema regression 在四格中均为 `40/40 PASS`。写入这些结果后，docs / Schema / static gates 又在最终
文档字节上重跑；这些本地 witness 不替代本候选自己的 original PR、exact-main 或 public readback。

最终 static gate 确认 exact four-file scope、全仓 prose 中 1010 个 relative links 且零断链；四份变更文件均为
UTF-8 without BOM、LF/final LF，Markdown fences 平衡，本文 heading 唯一，无敏感本机路径。文档 208 / 209、
runtime、tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture DOT / SVG 保持原字节，
`git diff --check` 成立。

## 6. Preserved construction observations

实现期以下非成功观察继续保留原身份：

- A 的第一次 targeted command 使用错误 `PYTHONPATH`，discovery 在产品代码运行前停止；一次新增 assertion 的 test
  variable 又被放入前一 test 并触发 `NameError`；
- B 的早期 falsifier 证明 swapped eligibility failure 只撤销 replacement、一个 child eligibility 可支撑两个 claims；
  两个真实 authority defects 在最终字节前修正；
- C 的首个候选缺少 distinct worker boundary；自审拒绝该候选后才补齐 worker 与 direct boundary tests；
- D 的首个 fixture 使用 Fact-only Policy，被 Relation requirement validator 正确拒绝；首个 non-empty probe 又把
  trailing LF 算入 AST span，Provider 正确返回无匹配；
- E 的 positive worker roundtrip 在最终矩阵前从 B-only 加强为 A/B 独立覆盖；
- F 首先暴露 historical operands reconciliation、empty Fact helper 索引首 path，以及 RelationSet admission 重算旧
  observation operands 三处真实 integration gap；均在最终矩阵前修正；
- G 的 expected digest placeholder 首跑失败；LSPC-005 两个不合格 fixture 与 LSPC-017 的双成功 world 又在审计中被
  拒绝，最终测试分别改为 frozen-profile 内 exact assignment rejection 与旧失败/新成功 cross-attempt splice。

这些记录分别属于 invalid local setup、fixture refinement、自审停止或真实 implementation counterexample。后继绿色不把
它们倒写成未发生，也不把 setup/fixture 问题升级成 runtime defect。

G 合入后的首次只读 run 查询又因 PowerShell string construction 把 SHA 作为 `gh` 子命令，返回
`unknown command <sha>`；显式使用 `--commit` 后才读到 exact-main runs。该观察没有修改远端或产品字节。

## 7. Scope reconciliation

本实现没有选择 Language Support persistence Route A/B，也没有创建 public classification/projection carrier、Schema、
Evidence、receipt、ledger 或 Bundle。以下能力继续未授权：

```text
real parser / AST execution
Parse per-unit terminal fulfillment
Fact obligation-universe derivation / fulfillment
public Language Support or operation-projection Artifact
shared observation receipt / ledger
ReviewSliceSet / Coverage
publisher / Bundle / CLI / Workbench
other top-level tracks
```

以下不等式继续成立：

```text
eligible upper bound != operation fulfillment
operation terminal != Parse / Fact / Coverage fulfillment
semantic equality != attempt authority
same limits != original BudgetContext
exact empty request != higher-stage closure
implementation exact-main verified != implementation frozen
```

## 8. 本候选自己的最后门

本文与状态入口只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 208 / 209、
runtime、tests、Schema、Profile、Policy、corpus、identity vectors 与 architecture DOT / SVG 必须保持原字节。

提交前必须完成：

1. applicable docs / Schema regressions 的 CPython 3.10.6 / 3.13.13 normal / `-O` 四格；
2. exact scope、relative links、Markdown fence / heading、状态 marker、UTF-8/LF/final-LF、敏感/本机路径、frozen-byte
   continuity 与 `git diff --check`；
3. original PR required checks 全部成功；
4. 受保护主线合入且 merge parents / tree 可复核；
5. new exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
6. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
7. independent Core / source-byte reconciliation；
8. 后继独立状态发布完成自己的同等级 final bytes、original PR、merge、exact-main 双门与 fresh
   readback/reconciliation，才允许发布
   `R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN`。

任一非成功观察都保留原身份并停止；诊断不计入资格，后继 PASS 不覆盖首败。本文 target marker 在最后门以前只表示
publication target，不授权 Parse/Fact/Coverage 施工。

## 9. 下一停止线

当前唯一合法动作是完成本 docs-only candidate 的证据闭环。候选取得资格后，仍须从新的 exact main 建立独立最终
冻结发布；最终冻结发布闭合以后再返回 CONTROL LOOP，重新判断 Parse fulfillment prerequisite 是否仍是当前最小合法
问题。

不得从 A–G 绿色自动选择 persistence、创建通用 receipt/ledger、运行真实 parser、开始 Fact fulfillment 或恢复
ReviewSliceSet/Coverage。若新的 readback、reconciliation 或系统审计击穿当前 closure，只重开被击穿的最小 seam。
