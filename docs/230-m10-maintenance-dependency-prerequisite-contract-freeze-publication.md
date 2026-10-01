# M10 0.12 maintenance dependency prerequisite 合同冻结发布

日期：2026-10-01

## 1. 发布对象与生效条件

本文只发布[文档 229](229-m10-maintenance-dependency-prerequisite-contract.md)的 maintenance dependency
prerequisite 最小合同。本文自身的 final-byte local gates、original PR 门、受保护合入、new exact-main Public CI /
Browser Smoke、fresh anonymous installed-product readback 与 independent reconciliation 全部成立后，以下目标状态才生效：

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

本文最后门闭合以前，最后合格事实仍是 `CONTRACT_CANDIDATE`。写出 frozen marker 只是条件化 target state，
不代替 publication qualification。合同冻结也不自动授权 dependency write、dispatch 或 workflow bootstrap。

| 坐标 | 值 |
| --- | --- |
| 前置审计 | [文档 228](228-m10-maintenance-dependency-prerequisite-precontract-audit.md)，qualified precontract history |
| 合同候选 PR | [#256](https://github.com/NoctilumeDev/VeriTrail/pull/256) |
| 候选 base | `1227d41ff3c0d052f6b9e90f8be55ae89b2912fc` |
| 候选 head | `c5e10ebd215d168293713714ef189742ff64d806` |
| 候选 merge | `be1db09637b8b499269b6281c5ab744ddf27db02` |
| 候选 head / merge tree | `3a6332d75d225bd5263852ce4c4b734e34e800ca` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

冻结对象仍是文档 229 的 exact 0.12 maintenance dependency prerequisite：

```text
exact v0.12.2 maintenance source + phase-one ruleset
    -> fresh one-file dependency topic candidate
npm 11.19.1 + public registry + frozen targeted command
    -> exact four-entry lock update
local Workbench gates + protected PR identity
    -> exact candidate-head dispatch witnesses
ordinary merge identity
    -> exact maintenance-tip dispatch witnesses
all identities reconciled
    -> qualified dependency prerequisite
```

本文不修改 source、npm/registry/command、四个 lock entries、final lock SHA-256、one-file scope、local gates、
PR/ruleset/merge topology、dispatch denominator、失败语义或 retained-evidence 规则。manual `workflow_dispatch`
仍只是 exact-ref observation witness，不是 original PR check 或 ruleset required check。

以下边界继续成立：

```text
same lock bytes != same source world or inherited qualification
dispatch success != required check
candidate-head qualification != merge-tip qualification
contract frozen != dependency implementation authorized
```

## 3. 合同候选 source qualification

候选最终字节只改变 AGENTS、README、文档 229 与 milestones；runtime、tests、workflow、ruleset、maintenance
branch、dependency bytes、Schema、publisher、Bundle 与 architecture DOT/SVG 均未改。其本地 documentation gates
在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格各为 `13/13`，并通过 exact four-file scope、relative links、
UTF-8 无 BOM、LF/final LF、fence、required marker、sensitive-path 与 `git diff --check`。

| 门 | Run / identity | Source | 结果 |
| --- | --- | --- | --- |
| PR #256 original Public CI | `36792226029`，attempt 1 | `c5e10ebd215d168293713714ef189742ff64d806` | `11/11 SUCCESS` |
| protected merge | `be1db09637b8b499269b6281c5ab744ddf27db02` | parents `1227d41...` + `c5e10eb...` | ordinary merge |
| exact-main Public CI | `36794128077`，attempt 1 | `be1db09637b8b499269b6281c5ab744ddf27db02` | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36794127955`，attempt 1 | `be1db09637b8b499269b6281c5ab744ddf27db02` | `1/1 SUCCESS` |

这些门只使文档 229 成为 qualified contract candidate；它们不能替代本 publication 自己的资格链。

## 4. Fresh installed-product readback

候选读回来自 fresh CPython 3.13 venv 中的已安装 public artifacts：Core `0.13.0`、GitHub Evidence
`0.1.0`、Playwright `1.62.0` 与 matching Chromium。`GH_TOKEN / GITHUB_TOKEN / PYTHONPATH / PYTHONHOME /
VERITRAIL_SOURCE_ROOT` 均清空；Core 与 plugin import 来自该 venv 的 site-packages。public wheel SHA-256：

```text
Core
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04
GitHub Evidence
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

正式观察以前的五条 setup 记录永久保留且不计入资格：一次 PowerShell read-only 参数引用错误、一次
`source.json` 路径转义错误、一次 Playwright preflight teardown warning，以及两次不存在 probe 位置的
`FileNotFoundError`。五次都没有 sealed Plan、collection session、Evidence 或 product output；随后 repository
search 确认 exact-main probe 为 `scripts/p4_real_github_acceptance.py`。这些记录不是产品、合同或 Core failure。

四个后继正式观察使用全新的 Plan、session 与 output：

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `m10-dep-contract-readme3-be1db09` | `github-paired-7822aaeac91d485988228f9710fec30e` | `2e00cef2759c7d7fd5158e56ce88e0616d646b010bfbfa8904338346fd6c17b1` |
| 文档 228 | `m10-dep-contract-doc228-be1db09` | `github-paired-4c89c583b2a141899ebe2e2d1adc6d8c` | `69ecdcb7e92cae3592b5e408f012b16898c1e3463028233635cb77bb7ae67a40` |
| 文档 229 | `m10-dep-contract-doc229-be1db09` | `github-paired-64a8f3eca8ec4179b6615c0b4d6b0874` | `6ba0778e519bcffcfba4574b37b6aa0b195ed9ffc6eb0dc2d09f9a92cd8e7983` |
| milestones | `m10-dep-contract-milestones-be1db09` | `github-paired-3fab7db16a7641c1ab1c0ff80164a09f` | `d138b44c0d1bea2a3ab070ee65c0e31e9e3bec5a7283788cbf807fcbff3f612c` |

四份观察均绑定 exact merge SHA，匿名 API 与 public render 为 `COMPLETE`、HTTP 200、三样本稳定、唯一 marker、
零 conflict / coverage reason / cleanup error / active stream，installed Core 独立裁决为 `PASS`。

## 5. Independent reconciliation 与 source bytes

联合 verifier 验证四份 sealed Plan、Evidence、handoff、report 与 summary digest；重新 import handoff 后调用安装产品
Core 复算所有 adjudication fields，并证明 Plan ID、Plan digest 与 collection session 未复用。它还核对 PR #256
base/head/commit/file scope、original CI、ordinary merge 双亲/tree、exact-main 双门、clean local checkout 与五条 setup
记录的非资格身份。

AGENTS、README、文档 228、文档 229 与 milestones 另做匿名 exact-SHA raw-source 下载，`5/5` 逐字节等于
对应 Git blob。该 byte check 不冒充 API/render Evidence，也不替代 installed-product path。canonical reconciliation
manifest：

```text
sha256_json  = dfd697f9544b5629adc86c83d3cb3e511942e0350a7c064a026564e9618c3942
sha256_bytes = a890203ae0a468c811446fd97826a55bf9dbaf6a4150b0d422e11f405eb3a01a
```

该 manifest 是本地 retained evidence；摘要不使本地 Artifact 自动变成远端可取得文件，也不替代本 publication
自己的门。

## 6. 本发布自己的最后门

本发布只修改 AGENTS、README、文档 229 与 milestones 的状态/导航，并新增本文。文档 229 第 1–13 节语义、
architecture DOT/SVG、runtime、tests、workflow、ruleset、maintenance branch 与 dependency bytes 保持不变。

提交前必须重新运行适用于最终字节的双 Python normal/`-O` documentation regression、relative links、UTF-8、
fence/heading、required markers、sensitive paths、exact diff scope、文档 229 semantic byte continuity、architecture
asset continuity 与 `git diff --check`。这些本地门不能代替 publication original PR checks。

本发布最终字节的 CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `tests.test_markdown` 各为 `4/4 / OK`。
静态门检查五份文档、584 个 relative links 与 125 个 headings，零断链；UTF-8 无 BOM、LF/final LF、
fence、required markers、sensitive paths、exact five-file scope 与 `git diff --check` 均成立。文档 229 第 1–13 节
逐字节等于 publication base，architecture DOT/SVG Git blob identity 未变。

```text
publication original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / doc229 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后续成功不改写先前 observation。不得修改结果标准、复用本次
候选 Evidence、拿 PR #256 绿灯替代本 publication 门，或把相同文案解释成 qualification-path equivalence。

## 7. 后继停止线

本发布最后门全部成立后，必须回到 CONTROL LOOP，从新的 exact main 重新核对 maintenance ref/tip、phase-one
ruleset、并行 PR、current advisory surface 与文档 223/224 停止线。只有复核仍证明 one-file dependency
prerequisite 是最小合法问题，才可建立全新 dependency candidate identity。

#252 永久保持关闭、未合并和原始失败身份；不得 reopen、rerun、改 head 或借用。workflow bootstrap、phase two、
0.12.3 backport/release、consumer migration、current-main repair 与 R1 Parse 均不由本文开始。

冻结原则为：**相同 lock 内容不能跨 source world 继承 authority；合同、实现、candidate-head qualification、
merge-tip qualification 与后继 workflow bootstrap 必须分别取得资格。**
