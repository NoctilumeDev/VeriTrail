# R1 Language Support Qualification 合同冻结发布

日期：2026-09-26

## 1. 发布对象与生效条件

本文只发布[文档 198](198-r1-language-support-qualification-contract.md)的 Language Support Qualification
最小语义合同 0.1。本文自身的 original PR 门、受保护合入、exact-main Public CI / Browser Smoke 与 fresh
anonymous installed-product readback 全部成立后，以下发布目标才成为有效状态：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文最后门闭合以前，最后已取得的资格仍是合同候选；写出 frozen marker 不代替该门。合同冻结也不授予
classifier、carrier 或 runtime 实现授权。

| 坐标 | 值 |
| --- | --- |
| 前置审计 | [文档 197](197-r1-language-support-qualification-precontract-audit.md)，`PRECONTRACT_AUDITED` |
| 候选 PR | [#209](https://github.com/NoctilumeDev/VeriTrail/pull/209) |
| 候选 base | `de4eee7e953a0b95d52b973bee35a033e3901254` |
| 候选 head | `8ce697cc2e60e3b784d69dd213c3bfc4e1ea2971` |
| 候选 merge | `78014cd32cf539c3141ae066f6a7c40c0ac707ab` |
| 候选 head / merge tree | `cda0ee14fcc64349c634e4bba83c79cdce1df15c` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

冻结对象为 `r1-python-language-support/0.1` 的确定性资格语义：

```text
exact terminal Snapshot inventory + sealed Policy IN_SCOPE join
    -> authoritative denominator
relevant inventory / Policy / Profile semantics + versioned function
    -> exact semantic input identity
all applicable predicates
    -> complete canonical failed-reason set
    -> exactly one eligible / unsupported disposition per member
```

Python 3.10 encoding pipeline、predicate applicability、reason rank、stage ownership、input/integrity rejection
与 Parse consumer boundary 均沿用文档 198；本文不修改这些语义。Provider 不获得 qualification authority，
Language Support 不执行 parser 或解释 AST。

以下边界继续成立：

```text
encoding declaration detected != whole source qualified
complete applicable failed reasons != first failure
semantic classification equality != attempt or continuation authority
contract frozen != implementation authorized
```

persistence 继续是 non-decision：Route A live recomputation 与 Route B canonical derived projection 均未被选择。
public/offline blob reacquisition 与 self-contained verification 仍须由后继消费边界审议。

## 3. 候选 source qualification

候选原始 CI、受保护合入与 exact-main 双门均在 attempt 1 成立：

| 门 | Run | Source | 结果 |
| --- | --- | --- | --- |
| PR #209 Public CI | `36195619550` | candidate head | `11/11 SUCCESS` |
| exact-main Public CI | `36197451442` | candidate merge | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36197451327` | candidate merge | `1/1 SUCCESS` |

候选只改变 AGENTS、README、文档 197、文档 198 与 milestones。architecture DOT/SVG Git blob identity 未变，
runtime、tests、Schema、Profile、Policy 与 fixture 未改。

候选最终字节完成 CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `40/40` Schema/Markdown regression。
第一次 local gate 的 37 项 Schema tests 已通过，但 Markdown module 因缺 `PYTHONPATH=src` 未启动；
该记录保留为 local setup failure，不写成已经执行的 Markdown 测试或产品首败。修正 source-root 后的四格
属于同一最终 source 的独立本地资格。

候选静态门检查五份文档、449 个 relative links、87 个 headings 与六个 required markers；UTF-8 无 BOM、
fence/heading、敏感路径、exact diff scope 与 `git diff --check` 均成立。

## 4. 首次正式读回 ERROR 与后续资格观察

首次 README 正式观察必须保留：

```text
Plan ID  r1-ls-contract-readme
session  github-paired-6b600bac30084f06a5c87737722ac3e3
Plan     db1cc8b32c7d728e53013b7e80035ee90a82b3199be9d7db579c635ec84b3e6e
P1       ERROR / HTTP 403 / COLLECTION_BUDGET_EXHAUSTED
P2       COMPLETE / HTTP 200
```

GitHub 明确返回匿名 core limit 60、used 60、remaining 0。该观察是正式 readback ERROR；未生成 handoff
或 Core report，因此它不是 Core FAIL、合同 FAIL 或 public bytes mismatch。额度由谁消耗没有被归因。
原 runner 在形成 Bundle 时才保存独立 sealed Plan 文件；本次错误只在两份 Evidence 内保留 Plan digest，
不得事后宣称首轮已持久化完整 Plan 文件。

其后 API 可用性、显式代理与公开 raw-source 核查均为 `DIAGNOSTIC_ONLY_NON_QUALIFYING`。多个 reset 时间
经过后仍观察到额度耗尽，证明“已过 reset”不能代替当前可用性检查。新网络条件下 API 返回 200 后，才
启动新的正式身份。旧 ERROR 输出没有删除、覆盖或复用。

三个后继正式观察来自 fresh CPython 3.13 venv 中的已安装产品：Core `0.13.0`、GitHub Evidence `0.1.0` 与
matching Playwright `1.62.0` / Chromium。token 环境清空，import 来源为 site-packages。公开 wheels 的 SHA-256：

```text
Core
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04
GitHub Evidence
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README #2 | `r1-ls-contract-readme-02` | `github-paired-a92c317f34e74d18a165333cc9aebfa7` | `a0663b45ef4fab49dfe2e2ccfeb3bc067af37450adb53d96f5e3b2ef64afe9b3` |
| 文档 198 | `r1-ls-contract-doc198` | `github-paired-f173778dad2447238d68a027d1aee233` | `c83dad9e8c5f618e3699392ac66e551718de0263fa3ffab259852cc48c812c7a` |
| milestones | `r1-ls-contract-milestones` | `github-paired-3b67318bb5cd4c6aad26a29e252550e7` | `5fef86d47cb25f5032f12c44ad92440b0d031d817f0ba0e8e72bfc9ff2accc1d` |

这三个新观察均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 marker、零 conflict / coverage
reason / cleanup error / active stream，Core 为 `PASS`。历史形状仍是 **README #1 ERROR + 三个后继正式 PASS**，
不能描述成读回从无失败。

## 5. 独立复算与 source-byte 核账

联合 verifier 独立复核 sealed Plans、Evidence、handoff 与 report digest，重新 import handoff 后调用已安装
Core 复算全部 adjudication fields，并检查 Plan/session 不复用、merge ancestry/tree、记录的 CI source identity、
wheel identity 与 architecture asset continuity。首轮 ERROR 两份 Evidence 的 SHA-256 也重新核对，字节未变。

五份候选变更文档另做匿名 exact-SHA raw-source 下载，均逐字节等于 Git blob。该核查单独保存，不冒充 P1/P2
Evidence 或替代特定消费路径。两类核查共同进入本地 canonical reconciliation manifest：

```text
sha256_json  = 285d72da03869e77e850a752912629acaa3455d56f200231946ed1c1970260f1
sha256_bytes = 19ecf8e0fcf607f16d42703ca23f96f7698c9c3f0c5e4c0a9b41fed0e13cf25c
```

这个 manifest 属于本地证据链；摘要不使本地 Artifact 自动成为远端可取得文件。候选资格不代替本发布自己的门。

## 6. 本发布自己的最后门

本发布只修改 AGENTS、README、文档 198 与 milestones 的状态/导航，并新增本文。文档 198 第 1–12 节语义
保持原字节；architecture DOT/SVG、runtime、tests、Schema、Profile、Policy、corpus 与 identity vectors 不变。

提交前必须完成适用 Schema/Markdown regression 的双 Python normal/`-O` 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff scope、合同语义 byte continuity 与 `git diff --check`。
这些本地门不能代替本发布自己的 original required checks。

本发布最终字节的 CPython 3.10.6 / 3.13.13、normal / `-O` 四格 Schema/Markdown regression 各为 `40/40 / OK`。
静态门检查五份文档、454 个 relative links 与 74 个 headings，零断链；UTF-8 无 BOM、LF、fence/heading、
敏感路径与状态 markers 均成立。exact diff scope、合同第 1–12 节原字节与 architecture DOT/SVG byte continuity
也独立通过。

```text
publication original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后续成功不改写先前观察。不得修改结果标准、复用旧 Evidence、
拿 PR #209 的绿灯替代本发布门，或把相同语义内容解释成 qualification-path equivalence。

## 7. 后继停止线

本发布最后门全部成立后，下一步仍只是从新 exact main 重读文档 198 第 13 节，独立审计最小 private
implementation 面与停止线。若该审计需要 implementation authorization，必须另行明确；本文不先授予。

classifier、carrier、persistence Route A/B、真实 Parse/AST、Fact、shared receipt、ReviewSliceSet、Coverage、
Schema、Evidence、Manifest、publisher、Bundle、CLI、Workbench 与其他顶层轨均不由本文开始。

冻结原则为：**Language Support 是对 exact semantic world 的确定性资格分类；语义结果可以复用，执行权必须
逐次取得。**
