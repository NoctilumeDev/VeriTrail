# M10 0.12 maintenance dependency drift 合同冻结发布

日期：2026-10-09

## 1. 发布对象与生效条件

本文只发布[文档 235](235-m10-maintenance-dependency-drift-contract.md)的 dependency drift 最小合同。
本文自身的 final-byte local gates、original PR Public CI、受保护 `main` 合入、new exact-main Public CI /
Browser Smoke、fresh anonymous installed-product readback 与 independent reconciliation 全部成立后，以下目标才成为
有效状态：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

本文最后门闭合以前，当前事实仍是 qualified contract candidate。写出 frozen marker 不代替这些门；合同冻结也不
自动授权 dependency implementation、workflow bootstrap 或 release。

## 2. 合同候选 source qualification

文档 235 的候选链已经对同一 exact source 完成：

| gate | identity | result |
| --- | --- | --- |
| candidate base | `main@7cf409940339d4068c3effd9e6d4deaca0c7861b` | qualified doc234 source state |
| candidate PR | [#267](https://github.com/NoctilumeDev/VeriTrail/pull/267)，head `8ed2f6f0e02e0a7a1e9f0d8006944e02eae1bb75` | 1 commit / 4 files |
| original Public CI | `37815845110`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `933df49e61b8a5d3e3856afa648d27c1c21f5529` | ordinary merge |
| merge tree | `b4a06c0a5937f8738d2315acaa36fead1721620b` | parents = base + candidate head |
| exact-main Public CI | `37818894300`，attempt 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `37818894374`，attempt 1 | `1/1 SUCCESS` |

候选只修改 AGENTS、README、文档 235 与 milestones。maintenance branch、dependency bytes、workflow、ruleset、runtime、
tests、Schema 与 R1 frozen surfaces 均未改变。

候选 final bytes 已完成 CPython 3.10 / 3.13、normal / `-O` 四格 Markdown regression，各格 `4/4 PASS`；
relative links、UTF-8 无 BOM、LF/final LF、fence/heading、required markers、敏感路径、exact four-file scope 与
`git diff --check` 均通过。合同表另与 candidate lock 做机械核账：14/14 projection rows、Vue peer dependency、root
projection、Git blob 与 SHA-256 一致。

## 3. Fresh installed-product readback 与独立复算

从 detached `main@933df49...` 建立 fresh CPython 3.13 venv，安装 public VeriTrail Core `0.13.0`、GitHub
Evidence `0.1.0`、Playwright `1.62.0` 与 matching Chromium。token 与 source-path 环境清空；import 来源为
venv `site-packages`。

四份正式 readback 使用互不复用的 sealed Plan、session、Evidence 与 output：

| target | Plan ID | session | Core report SHA-256 | result |
| --- | --- | --- | --- | --- |
| README | `m10-drift-ctr-readme-933df49` | `github-paired-347066c2ddaf419bbf5a9995352d9096` | `e8181386a068e44b647baee19918fabc7f799772e1878f7a447b0c947a0a710d` | `PASS` |
| doc234 | `m10-drift-ctr-doc234-933df49` | `github-paired-8350f4b284284d078e166fc95d27bd79` | `62482e10f4c70a857717fccb2b99a6292be99630d94b3cb28f79d24afd6a4a7a` | `PASS` |
| doc235 | `m10-drift-ctr-doc235-933df49` | `github-paired-377aab4c3a154827ab57d822701d3923` | `23bef516d985d7f873c8f0e50bb93f46b4c657ebd4dcfaa8249895ceb7b218da` | `PASS` |
| milestones | `m10-drift-ctr-milestones-933df49` | `github-paired-bdba41c1e9434f65a82c88205d08e1d6` | `bc10ff771e4404bd41b7a95aa0c86266e6f28193c378c0a36719d35e1d34b150` | `PASS` |

每次正式观察均为 exact-SHA HTTP 200、API/render `COMPLETE`、三样本稳定、唯一 marker、零 conflict / coverage
reason / cleanup error / active stream。installed Core 独立重算为 `PASS`。AGENTS、README、doc234、doc235 与
milestones 五份 anonymous exact-SHA raw bytes 另与 Git blob 做逐字节核账，结果 `5/5 MATCH`；该 raw-byte
核查不冒充 installed-product Evidence。

canonical reconciliation manifest：

```text
sha256_json  = 1bea6a3b59b452d7debda2b4778826a031e0ae2737e6523a19d55b02cac92960
sha256_bytes = ddbe3925167ae99b1babcc7ff47dcfbca2560bd3802378b31847f799f63ddda3
```

独立 verifier 还复核了 PR/base/head、CI denominators、merge ancestry/tree、detached worktree cleanliness、exact
four-file scope、Plan/session identity、public bytes 与 Core recomputation。manifest 属于本地证据链；摘要不使本地
Artifact 自动成为远端可取得文件。

## 4. 保留的非成功与 setup 观察

候选写作阶段的第一次机械核账发现 `@vue/reactivity` dependencies 被误写为 `{}`，而 exact lock 是
`{"@vue/shared":"3.5.43"}`。该 authoring transcription failure 在 commit 前修正；它不成为产品失败，也不从历史中
删除。

正式 readback lifecycle 开始以前还保留两项 setup observation：

1. 第一次 remote snapshot capture 从非 Git working directory 运行 `gh pr/run view`，四条命令均因无法推断 repository
   失败；未创建 Plan、session、Evidence 或 formal output。
2. 后继匿名 API/environment preflight 成功，但 Playwright teardown 输出一次 `TargetClosed` warning；未进入正式
   Plan/session，因此不计入产品 readback 或 qualification。

两项 setup observation 的后继成功只证明新的正确 setup 可工作，不改写原观察。PR #264、exact-version
`EUPDATEARGS`、projection-helper `KeyError`、doc228 resource stops 与其他上游失败身份继续原样保留。

## 5. 冻结范围与字节连续性

本文冻结文档 235 第 1–11 节的语义与原字节：exact maintenance tip、manifest/lock/workflow/ruleset coordinates、
package-name-only construction、完整 14-entry projection、one-file lock identity、两次 reconstruction、local gates、
ordinary PR/merge、candidate-head / exact-tip 两轮 `7/7 + 1/1` manual-dispatch witnesses、failure semantics、retained
evidence 与 continuation stop line 均不修改。

本发布只允许：

- 更新文档 235 第 12 节的 candidate qualification 与 freeze-publication 指针；
- 更新 README、AGENTS 与 milestones 的状态/导航；
- 新增本文。

因此 exact scope 是五份 Markdown。dependency、maintenance ref、workflow、ruleset、runtime、tests、timeout、retry、
budgets、Schema、publisher 与 Bundle 不得改变。

## 6. 本发布自己的资格门

提交前必须在最终字节上完成本层适用的双 Python normal/`-O` Markdown regression、relative links、UTF-8、
fence/heading、required markers、敏感路径、exact five-file scope、文档 235 第 1–11 节 byte continuity 与
`git diff --check`。本地门不能替代 original PR checks。

本发布最终五文件字节已完成 CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `tests.test_markdown`，各格
`4/4 PASS`。静态门检查五份 Markdown、606 个 relative links 与 125 个 headings；UTF-8 无 BOM、LF/final LF、
fence/heading、required markers、敏感路径与 exact scope 均成立。文档 235 第 1–11 节前缀长度 `18212` bytes，
SHA-256 `0a140c15ece04d5a841a2db0cd8b73a4b18f8a62048fbc0ec71f63a7b39fa6c7`，与 qualified candidate 逐字节相同；
`git diff --check` 通过。

```text
final-byte local documentation gates
    -> original PR Public CI
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback:
         README / doc235 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都必须保存原 identity。不得 rerun 洗白、复用 doc235 的 Evidence、拿相同内容或 digest 继承资格，
也不得在观察以后修改发布标准。

## 7. 后继停止线

最后门闭合后必须返回 CONTROL LOOP，从新的 exact main 重新核对 maintenance tip、ruleset、并行 PR、advisory
surface 与文档 223/224 的停止线。只有新的证据仍证明 one-file dependency correction 是当前最小合法问题，才可另行
审计 implementation authority。

本文不授权创建 dependency topic / PR、运行 dispatch、修改 maintenance branch、重开 #252/#264、workflow
bootstrap、phase two、0.12.3 backport/release、consumer migration、R1 Parse / Fact / Coverage、
`DECLARED_CLAIM_FIDELITY` 或其他顶层轨。

冻结原则为：**相同 package 名、版本、patch、projection 或 terminal PASS 都不继承另一个 exact coordinate 的
authority；合同冻结只固定施工与证明边界，不替代后继实现自己的完整资格链。**
