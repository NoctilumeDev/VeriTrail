# M10 Browser 主机 socket 分类修正与发行消费合同冻结发布

日期：2026-09-29

## 1. 发布对象与生效条件

本文只发布[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)的
M10 Browser 主机 socket 分类修正与发行消费合同。本文自身的 final bytes、original PR 门、受保护合入、
new exact-main Public CI / Browser Smoke、fresh anonymous installed-product readback 与 independent
reconciliation 全部成立后，以下目标才成为当前事实：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_CONTRACT_FROZEN
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_IMPLEMENTATION_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

本文最后门闭合以前，current fact 仍是 qualified contract candidate。把 frozen marker 写入条件化发布字节不替代
该门，也不创建 maintenance branch、ruleset、runtime patch、version、tag、Release、asset 或 workflow
migration。

| 坐标 | 值 |
| --- | --- |
| 边界审计 | [文档 221](221-m10-browser-host-socket-release-consumer-boundary-audit.md)，qualified history |
| 前合同审计 | [文档 222](222-m10-browser-host-socket-classification-correction-release-consumer-precontract-audit.md)，qualified history |
| 合同候选 | [文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md) |
| 候选 PR | [#246](https://github.com/NoctilumeDev/VeriTrail/pull/246) |
| 候选 base | `fc2be4009989c3ddc0ff71fc5f0a54c02290751a` |
| 候选 head | `0b07eec8bffc0aa77b215e87dd249c1fd4d097d6` |
| 候选 merge | `5703ac4126e9645569b4631b4cc359ebca70e6d9` |
| 候选 head / merge tree | `9b49eb0ac776afebe92a04f72b37467ec96905e8` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

本文不新增文档 223 之外的合同语义。冻结对象只有三条不能互相继承资格的轨及其串行顺序：

```text
C  current-main narrow classification correction
   -> current source exact-main qualification

M0 protected core-0.12-maintenance governance bootstrap
   -> workflow-only PR
   -> maintenance exact-tip dual gates
   -> strict phase-two ruleset

M1/M2 exact v0.12.2-line backport and new public Core 0.12.3
      -> create-new non-Latest release
      -> anonymous dual-Python / Starter product readback

W  separate main required-lane consumer migration
   -> exact public 0.12.3 URL / SHA-256 / version
   -> migrated exact-main dual gates
```

分类语义继续严格限定为：仅当既有 raw failure text 满足
`raw_failure_text.strip() == "net::ERR_NO_BUFFER_SPACE"` 时，增加 private
`network:<viewport> / HostSocketNoBufferSpace` collector projection；原始 Network failure 保留，lifecycle 为
`COLLECTOR_ERROR / ERROR / PENDING`。near-miss 与真实 selector/business failure 继续走既有合同。

以下边界继续成立：

```text
same patch or terminal classification != qualification inheritance
current source corrected != public v0.13.0 corrected
maintenance release qualified != main consumer migrated
contract frozen != implementation already started
consumer lane PASS != Parse implementation authorized
```

public 0.13.x 仍是独立未来发行义务，不是重新审查 Parse authorization 的前置门。本文不修改文档 223
第 1–12 节，不重新解释任何失败，也不放宽两阶段 maintenance governance 的 counterexample stop line。

## 3. 候选 source qualification

候选只改变 AGENTS、README、文档 223 与 milestones。architecture DOT/SVG、runtime、tests、workflow、
version、branch、ruleset、tag、Release、asset、Schema 与 frozen R1 合同均未修改。

| 门 | Run | Source | 结果 |
| --- | --- | --- | --- |
| PR #246 Public CI | `36473865925` | `0b07eec...` | attempt 1，`11/11 SUCCESS` |
| exact-main Public CI | `36476517678` | `5703ac4...` | attempt 1，`11/11 SUCCESS` |
| exact-main Browser Smoke | `36476517518` | `5703ac4...` | attempt 1，`1/1 SUCCESS` |

候选最终字节完成 CPython 3.10.6 / 3.13.13 normal / `-O` 的 Markdown / Schema 四格各
`40/40 PASS`。四文件 scope、554 个 relative links、UTF-8 without BOM、LF/final LF、balanced
fences/headings、状态 markers、敏感路径、frozen input blob continuity 与 `git diff --check` 均成立。

候选提交前的两个只读 setup command failure 继续保留：一次 `git hash-object` 使用了不存在的文档 218
短文件名；一次 `gh release view --json isLatest` 请求了该 CLI 版本不支持的字段。它们没有修改 source、
远端状态、Plan、Evidence 或产品观察，不属于合同/产品失败。

## 4. 候选 fresh installed-product readback

readback 从 detached exact `main@5703ac4...` 建立 fresh CPython 3.13.13 venv，安装 public Core `0.13.0`、
GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。Core 与插件都从该 venv 的
`site-packages` 导入；`GH_TOKEN`、`GITHUB_TOKEN`、`PYTHONPATH` 与 `PYTHONHOME` 均清空。冻结 wheels 的
SHA-256：

```text
Core
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04
GitHub Evidence
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

匿名 preflight 精确命中 `5703ac4...`、HTTP 200，并报告 core rate remaining 58/60。正式观察为：

| 正式观察 | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `m10-socket-contract-readme-5703ac4` | `github-paired-e96e064f61634277b5cceed630965051` | `7f490fb46d61baa25865787a6d1eeefde0b2e666746c5f384ee2098001395a35` |
| 文档 223 | `m10-socket-contract-doc223-5703ac4` | `github-paired-d2e335fa263d4ddfa1a44e8f64febfde` | `431e595ee0db00f2cd6e7fc69eb3b191b34575380bdc39a487230babc8dd2502` |
| milestones | `m10-socket-contract-milestones-5703ac4` | `github-paired-4097a595f78e496e998422de3fbee0b3` | `4edcf0ac91f332de060c6b9cddb5f4c328388b827a84183241f8f309b4a8887c` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 marker、零 conflict / coverage reason /
cleanup error / active stream，安装版 Core 均为 `COMPLETED / PASS`。

正式 Plan 产生以前的三项 setup observation 单独保留且不计入资格：PowerShell here-string 解析拒绝、Windows
`rg *.py` positional glob 调用错误，以及 preflight 结束时 Playwright 打印的 pending-task `TargetClosed`
cleanup warning。三者都没有创建正式 Plan、session、Evidence 或产品 observation；后继 PASS 不把它们改写成
未发生。

## 5. 独立复算与 source-byte 核账

联合 verifier 独立验证三份 sealed Plan、P1/P2 Evidence、handoff、report 与 summary digest，重新 import
handoff 后调用安装版 Core 复算 adjudication fields。它还核对：

- PR #246、candidate head、ordinary merge parents/tree 与 exact four-file scope；
- PR、exact-main Public CI 与 Browser Smoke 均绑定预期 SHA、attempt 1 且所有 jobs 成功；
- 三个 Plan ID、Plan digest、session 与 output root 互不复用；
- public wheel identity、先前 doc222 manifest、architecture asset continuity 与 clean detached worktree；
- AGENTS、README、文档 219、221、222、223 与 milestones 七份 anonymous raw bytes 等于 exact Git blobs。

canonical reconciliation manifest 为：

```text
sha256_json  = 37c1fb9620a4d1524188903b9ee34fb3f293a96a9847764ffc605ece2fb9f7b0
sha256_bytes = 6b38ee7a7931d60b4a7880652db8d7f851e8efaff6b96c8377fbc4fbd8be4d6c
```

该 manifest 属于本地证据链；摘要不使本地 Artifact 自动成为远端可取得文件，也不替代本冻结发布自己的门。

## 6. 本发布自己的最后门

本发布只允许修改 AGENTS、README、文档 223、milestones，并新增本文。文档 223 第 1–12 节、上游 frozen
documents、architecture DOT/SVG、runtime、tests、workflow、version、branch、ruleset、tag、Release、asset、
Schema 与 persistence 必须保持原字节。

提交前须完成适用 Markdown/Schema regression 的双 Python normal / `-O` 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff scope、文档 223 第 1–12 节语义 continuity 与
`git diff --check`。本地门不能替代本发布自己的 original required checks。

本发布的 final-byte candidate 已完成以下本地门：

- CPython 3.10.6 / 3.13.13 normal / `-O` 四格分别 `40/40 PASS`；
- exact 五文件 scope，1097 个 repo-relative file-link occurrence 全部可解析；
- 五文件均为 UTF-8 without BOM、LF/final LF，fence/heading、状态 marker、敏感路径与 README 索引检查通过；
- 文档 217、218、219、221、222 与 architecture assets 保持 HEAD 原字节；
- 文档 223 第 1–12 节保持原字节，其 SHA-256 为
  `04de5a290581192e785f6b598de72d62c35e90d6df0b237719e0ab93234dd300`；
- `git diff --check` 通过。

本地资格形成以前的 setup observations 继续保留且不计入资格：首次四格启动没有注入当前仓库 `src`，
Markdown module 因而 import 失败；第二次误用了当前 tree 不存在的旧 `packages/core/src` 路径。两次均在
test import/setup 边界失败，其余 37 条 Schema tests 当次通过，不能据此把整格写成 PASS。静态 checker 也曾
依次把 fenced regex 误识别为 Markdown link、产生 Windows 路径字面量语法错误，并使用错误的 frozen document
文件名。修正的是 checker/setup，不是产品、合同、预算或 final bytes；这些调用没有产生产品 observation。

```text
publication final bytes
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 文档 223 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察保留原身份；诊断不计入资格，后继成功不改写旧 observation。不得复用候选 Evidence、拿 PR
#246 或 `main@5703ac4...` 的绿灯替代本发布门，也不得在结果出现后修改验收标准。

## 7. 后继停止线

本文最后门全部成立后，必须先回到 CONTROL LOOP，从新的 exact main 重新审查 C：current-main classification
correction 是否仍是最小合法问题、现有 runtime seam 是否与冻结合同一致，以及这一次实现允许触及的精确文件与
测试面。`CONTRACT_FROZEN` 不自动等于 implementation 已经开始。

在该复核完成以前，不得创建 `core-0.12-maintenance`、ruleset、runtime patch、version、tag、Release、asset 或
workflow migration，也不得重发 Parse private implementation authorization。

冻结原则为：**同一精确主机 socket 失败可以在多个 source/distribution world 中得到相同分类，但每个 world 的
修正、发行与消费资格必须分别取得。**
