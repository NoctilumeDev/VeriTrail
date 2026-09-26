# R1 Language Support Qualification codec-conformance 修正合同 0.2 冻结发布

日期：2026-09-26

## 1. 发布对象与生效条件

本文只发布[文档 202](202-r1-language-support-codec-conformance-correction-contract.md)的
`r1-python-language-support/0.2` 修正合同。本文自身的 original PR 门、受保护合入、exact-main Public CI /
Browser Smoke 与 fresh anonymous installed-product readback 全部成立后，以下发布目标才成为有效状态：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文最后门闭合以前，最后已取得的资格仍是 `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_CANDIDATE`；
写出 frozen marker 不代替该门。0.2 冻结也不授予 classifier、carrier、Schema 或 runtime 实现授权。

| 坐标 | 值 |
| --- | --- |
| 0.1 frozen identity | `r1-python-language-support/0.1`，文档 198 Git blob `5a0145629edf427cd873f525e75f486218d6896e` |
| 0.2 candidate | [文档 202](202-r1-language-support-codec-conformance-correction-contract.md) |
| 候选 PR | [#214](https://github.com/NoctilumeDev/VeriTrail/pull/214) |
| 候选 base | `41bd7cd3d6d486c780aeda91b86ae8845ef90ae7` |
| 候选 head | `10f4a6e22afa8931b29cec79134216521861cd80` |
| 候选 merge | `936e6037deef899da9403988bb86f5fc8f6ddc10` |
| 候选 head / merge tree | `107c6ef7c931a40c6e2661369eef18afbabd3233` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

0.1 继续保持 frozen historical identity；本文不倒写它的规范路径、历史资格或 Git bytes。0.2 只在 exact
Profile compatibility 为 `PYTHON / PYTHON_3_10 / {UTF-8, UTF-8-SIG}` 时发布以下 delta：

```text
Python 3.10 cookie / BOM placement
    + versioned accepted UTF-8 closed resolver
    + BOM consistency by _get_normal_name result
    + non-accepted early rejection without ambient lookup / decoder
    + strict whole-source UTF-8 / UTF-8-SIG decode for possibly eligible inputs
        -> r1-python-language-support/0.2
```

0.2 继承 0.1 的 denominator、exact semantic input binding、predicate applicability、complete reason composition、
exactly-one closure、stage ownership、semantic-result / live-authority separation 与 eligible-only Parse boundary。
terminal projection equality 不等于 contract identity equality；0.1 与 0.2 不得互相继承历史 qualification、
attempt identity、`BudgetContext` 或 continuation authority。

以下停止线继续成立：

```text
accepted-source resolution != ambient codec registry
terminal projection equality != normative-path identity
semantic classification equality != attempt authority
contract frozen != implementation authorized
Language Support eligible != parser success
```

persistence 继续是 non-decision：Route A live recomputation 与 Route B canonical derived projection 都未被选择。
public/offline blob reacquisition、self-contained verification 与 public carrier 仍须由后继消费边界审议。

## 3. 候选 source qualification

候选最终字节只改变 AGENTS、README、文档 202 与 milestones；runtime、tests、Schema、Profile、Policy、corpus、
identity vectors、architecture DOT/SVG 与文档 198 frozen bytes 均未修改。

候选原始 CI、受保护合入与 exact-main 双门均在 attempt 1 成立：

| 门 | Run | Source | 结果 |
| --- | --- | --- | --- |
| PR #214 Public CI | `36248704418` | candidate head | `11/11 SUCCESS` |
| exact-main Public CI | `36249925950` | candidate merge | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36249925954` | candidate merge | `1/1 SUCCESS` |

候选最终字节在 CPython 3.10.6 与 3.13.13 上分别通过 14 项相关测试，以及 UTF-8/LF/final-LF、Markdown
links、边界 marker、exact diff scope 与 `git diff --check`。第一次本地 unit-test 入口没有设置
`PYTHONPATH=src`，Schema tests 已运行但 `test_core_version_contract` 在 collection 阶段以
`ModuleNotFoundError: veritrail` 停止；这属于 local setup failure，不是 runtime 首败。修正 source-root 后才取得
上述合格结果。

special-case oracle 的首次脚本又因外层 JavaScript 模板提前展开 bytes literal 中的 `\n` 而在 parse 前失败；
它没有形成 codec observation。初版 boundary checker 还要求候选字节中存在一个实际不存在的多行短语，因此产生
checker false negative；后继只修正 checker assertion。最终 reverse review 发现
`encodings.normalize_encoding()` 不负责 lowercase，候选因而显式冻结 ASCII lowercase search key 后才形成最终
head。三类记录均保留，不倒填成产品或合同失败。

## 4. Fresh installed-product public readback

readback 使用 fresh CPython 3.13.13 venv、已安装 Core `0.13.0`、GitHub Evidence `0.1.0` 与 matching
Playwright `1.62.0` / Chromium。`GH_TOKEN`、`GITHUB_TOKEN`、enterprise token 与 `PYTHONPATH` 均清空，Core
及插件 import 均来自该 fresh venv 的 `site-packages`。开始正式观察前，匿名 exact-SHA API diagnostic 返回
HTTP 200；该 diagnostic 不计入资格。

环境准备时，主机默认 `python` 指向 3.10，第一次创建的 `venv` 因而是未使用的 3.10 setup artifact；它没有
启动 Plan、session、Evidence 或 product observation。随后另建 `venv313`，并只从该环境开始正式读回。

三个正式观察均在 observation 前保存独立 sealed Plan，并使用全新的 Plan ID、session 与 output：

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-ls02-cand-readme` | `github-paired-e9ba8c808be44d08a5dae4f341cbc371` | `6a415fb81c08c623e2db0eadb31e8538015bb3fd8f04e72271a16f5e74e000cc` |
| 文档 202 | `r1-ls02-cand-doc202` | `github-paired-a4449afae05242e69b7b14ab468a8de0` | `5b1017b46a18777dd7a7fda8aa9630d67a6aec77a3724a6cf8c6c597a5a46de5` |
| milestones | `r1-ls02-cand-milestones` | `github-paired-c277ecdbf2bc4c6a8b66aa5bdd8c04e1` | `23beeb79132156a28e99ac99a3012b7804494dbf17ad2391a18f474f0d887c96` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 marker、零 conflict / coverage reason /
cleanup error / active stream，Core 为 `PASS`。doc202 的中文 marker 在终端 PTY 输出中显示乱码；直接读取 canonical
summary 并按 Unicode code point 比较后，stored marker 与预期逐字符相等，因此该显示问题不改变 Artifact bytes。

## 5. 独立复算与 source-byte 核账

联合 verifier 独立验证三个 sealed Plan、Evidence、handoff 与 report digest，重新 import handoff 后调用已安装
Core 复算全部 adjudication fields；同时检查 Plan/session/digest 不复用、merge ancestry/tree、三条 CI source
identity、wheel identity、changed-file scope 与 architecture asset continuity。

AGENTS、README、文档 202 与 milestones 另做匿名 exact-SHA raw-source 下载，四份文件均逐字节等于 Git blob。
raw-source check 只用于 byte reconciliation，不冒充 P1/P2 Evidence 或替代特定消费路径。两类核查共同形成
本地 canonical manifest：

```text
sha256_json  = f93564b0d0b57560a2ad63c2c37148165958b8e6f8566e002abdb1227b25626d
sha256_bytes = 98aea23cfacec530e1acfa0891fc8c03347e08c6f1a5f65aae80241f0c4a41eb
```

该 manifest 属于本地证据链；摘要不使本地 Artifact 自动成为远端可取得文件。候选资格也不能替代本发布
自己的门。

## 6. 本发布自己的最后门

本发布只修改 AGENTS、README、文档 202 与 milestones 的状态/导航，并新增本文。文档 202 第 1–13 节语义、
文档 198 全文、architecture DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 均须
保持原字节。

提交前必须完成适用 Schema/Markdown regression 的双 Python normal/`-O` 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff scope、候选语义 byte continuity 与 `git diff --check`。
这些本地门不能替代本发布自己的 original required checks。

```text
publication original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 文档 202 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后续成功不改写先前观察。不得修改结果标准、复用候选
Evidence、拿 PR #214 的绿灯替代本发布门，或把相同语义内容解释成 qualification-path equivalence。

## 7. 后继停止线

本发布最后门全部成立后，下一步也不是直接实现。必须回到 CONTROL LOOP，从新的 exact main 重新审计：

> 当前最小 private implementation boundary 是否仍然有资格开始，以及它能否在不选择 persistence、不修改
> public identity、不运行 real parser、不借用 Fact/Coverage authority 的前提下形成 private proof。

classifier、carrier、persistence Route A/B、真实 Parse/AST、Fact、shared receipt、ReviewSliceSet、Coverage、Schema、
Evidence、Manifest、publisher、Bundle、CLI、Workbench 与其他顶层轨均不由本文开始。

冻结原则为：**版本化资格函数只拥有本 stage 可观察且有权裁决的语义区分；终态投影相同不消除规范路径的新身份。**
