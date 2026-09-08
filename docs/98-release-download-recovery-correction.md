# Release 资产下载恢复策略修正

状态发布目标：`RELEASE_DOWNLOAD_RECOVERY_FROZEN / P4_RELEASE_NOT_STARTED`

变更级别：`L1_COMPONENT_INTERNAL`

本修正只处理 Public CI 对既有不可变 Release 资产的下载恢复策略，不改变 P4 合同、标签、Release、
资产名称、冻结 SHA-256、验收阈值或 Core/插件公共语义。

## 1. 触发事实与证据上限

P4 合同冻结候选 PR #72 的原始 Public CI run
[`34241218820`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34241218820) 在 Python 3.10
下载 `authoring-skill-v0.1.0/SHA256SUMS-authoring-skill.txt` 时连续四次收到 HTTP 500；同一工作流的
Python 3.13 路径完成了该步骤。后继匿名下载得到 `302 -> 200`、205 字节，SHA-256 为
`20684909030aa104cb3faadcb1707edcefa16be2b2832808ccd887996a8debfb`，与冻结值一致。该失败已在
[文档 97](97-p4-github-evidence-release-contract-freeze.md) 保留，PR #72 没有重跑或合入。

P4 合同冻结合入后的 `main@12130378febde2075d4cb9924628a07f9f26cb1e` 又在原始 Public CI run
[`34244325251`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34244325251) 的 E3 0.2 下载门
停止：`starter-v0.2.0/veritrail_starter-0.2.0.tar.gz` 连续四次收到 HTTP 500。后继匿名下载得到
`302 -> 200`、24910 字节，SHA-256 为
`d86b836cad6f5b0bf2fbe17ce3d86fb309fa1fb1f2e592b757ef4b0f5f48188d`，同样与冻结值一致。

两次失败发生在不同资产和不同门禁路径。既有策略使用固定 2 秒间隔与三次重试，因此全部重试等待
被压缩在约 6 秒量级；实际总耗时还包含各次 HTTP 请求。现有证据只支持以下边界：

```text
transient external failure duration
>
current recovery window
```

这些事实不证明 GitHub 内部根因、代理故障、仓库缺陷或资产漂移。GitHub Status 当时没有公开未解决
事故，也不能反向证明单次 Release 下载路径没有短暂失败。

## 2. 修正边界

四处重复下载统一委托给仓库内 CI 工具 `scripts/download_release_asset.py`。它只拥有下载、恢复、摘要
校验和目标文件发布责任：

1. 初次请求和所有重试共同消费一个 monotonic 绝对恢复预算，默认 60 秒；
2. 单次请求最多消费 15 秒，但不得刷新总预算；
3. 暂时性 HTTP `408 / 429 / 500 / 502 / 503 / 504` 与明确的 timeout、connection reset 等传输失败
   可按 `2 / 4 / 8 / 16` 秒有界退避；
4. `404 / 403` 等声明为永久响应的 HTTP 结果、证书验证失败、非法 URL、摘要不一致或已存在目标不因
   重试而被接受；下载工具不判断标签或资产为何不存在，坐标含义仍由上层解释；
5. 每次尝试只写同目录内的独立 owned partial，失败即清理；
6. 只有完整流式读取后的 SHA-256 与冻结值相等，才以不覆盖语义发布目标文件；
7. 诊断只报告 attempt、失败类别、HTTP 状态、剩余预算和退避，不记录凭据。

因此：

```text
availability recovery
!=
integrity relaxation
```

## 3. 必需证据

本候选至少必须证明：

- `500 -> 503 -> success` 使用 `2 / 4` 秒退避并发布精确字节；
- `404` 立即失败，不重试；
- SHA-256 不一致立即失败，不重试；
- connection reset 与 timeout 可以在同一绝对预算内恢复；
- 多次请求和 sleep 共同消费一个 deadline，后续请求只取得剩余时间；
- 已存在目标在联网前拒绝；
- 部分响应、重试与最终失败后没有 owned partial 残留；
- 两套 Python 的普通与 `-O` 路径、既有 Core/Starter/Authoring/GitHub 插件回归和远端原始 Public CI
  保持成立。

在独立修正合入并从新 exact main 取得门禁事实前，P4 Release 实现继续暂停；旧失败不通过 rerun 洗白。

## 4. 本地候选证据

从 `main@12130378febde2075d4cb9924628a07f9f26cb1e` 创建的独立工作树中，本候选已取得：

- 下载状态机定向测试 11 项，在 Python 3.10/3.13 的普通与 `-O` 四组均通过；
- Core 403 项在同一四组均通过；
- Starter 24 项、Authoring Skill 24 项、GitHub Evidence Plugin 180 项分别在同一四组均通过；
- Workbench 173/173、lint、production build 与 `npm audit --audit-level=moderate` 通过，报告 0 个漏洞；
- Authoring Skill 的 `single-webapp` 与 `static-site` 真实 DRAFT 链在双 Python 上均为 `PASS`，并保持
  `NOT_RUN / NOT_SEALED / NO_VERDICT`；
- Core、Starter 与 GitHub Evidence Plugin wheel 在双 Python 上构建成功，Starter sdist 构建成功；逐个
  wheel 读回均未包含本 CI 下载脚本，产品包边界未扩张；
- fresh anonymous E1 真实公开下载与 clean-install readback 在 Python 3.10.6/3.13.13 上为 `PASS`，
  七项 Release 资产及 Core wheel 的下载摘要全部与冻结坐标一致；
- fresh anonymous E3 真实公开下载与 clean-install readback 在相同双 Python 上为 `PASS`，两个 preset、
  七项 Release 资产及 Core wheel 均成立，summary 与 draft 事实保持 `BYTE_IDENTICAL`；
- 两次真实探针产生的外部临时目录均已清理。

首次 Core 3.10 普通回归没有绑定当前工作树 `src`，测试源来自本候选，但 Python 实际从旧
`veritrail-r0-review-plugin` editable install 导入生产模块；该 337 项运行产生 2 个失败与 9 个导入错误，
只证明 execution provenance 错配，不能归因给当前补丁，也不构成通过证据。随后显式读回 3.10/3.13 的
`veritrail.__file__` 均指向当前工作树，再从头取得上述 403 × 4 有效结果。旧无效运行没有被后继绿灯
改写成产品失败或成功。

以上仍是本地候选事实。只有独立 PR 的原始远端门禁、受保护主线合入和新 exact main 的后继读回成立后，
本恢复策略才可成为后续 P4 发布实施的地基。

## 5. 远端合入与主线门禁

实现提交 `24b2126907d9e0c60faa7d8ce10b13decb11b52f` 经
[PR #74](https://github.com/NoctilumeDev/VeriTrail/pull/74) 的原始
[Public CI run 34256599627](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34256599627)
在 attempt 1 上取得 11/11 `SUCCESS`，没有 rerun。PR 随后以 merge commit
`d23916735c7ac4d7e4a706d8edc5b106046b93c8` 合入受保护 `main`；精确读回得到：

```text
tree:
f1cb8c67ace4d3a69eeb0006ad9f37a675144e93

parents:
12130378febde2075d4cb9924628a07f9f26cb1e
24b2126907d9e0c60faa7d8ce10b13decb11b52f
```

该 exact main 的
[Public CI run 34257876815](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34257876815)
在原始 attempt 1 上取得 11/11 `SUCCESS`；同一 SHA 的
[Browser Smoke run 34257876863](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34257876863)
在原始 attempt 1 上取得 1/1 `SUCCESS`。PR 事实和主线事实分别成立，没有互相替代。

## 6. exact-main 匿名产品读回

从 clean detached `main@d23916735c7ac4d7e4a706d8edc5b106046b93c8`，在未提供
`GITHUB_TOKEN`、`GH_TOKEN` 或 `VERITRAIL_GITHUB_TOKEN` 的环境中，固定执行
`github-api -> github-public-render -> handoff -> Acceptance Core`。README 使用
`DESKTOP_1365X768`，本文使用 `NARROW_390X844`；两页使用独立 sealed Plan 与独立 paired session。

| 页面 | Plan digest | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report canonical digest | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| exact README | `2c1b0c61692e741eea27965fff210e8a2747a4c4f1877a57a621a73b8ea144f8` | `github-paired-5683636f032b4db79091cbd300b002c0` | `80b45b72c0d995592bc2ce7eb02b52272826b3d6391065be3c3e0caa44096759` | `10c8b859219f2d006414162c938f3c3fd6c8ee6a7b0128b9d32c0eebd9c6a2ad` / `c8afb46ee71dc442d8634f44a0d3898fd4be569ce08ab9046e43304109259671` | `c010d93d8421129b5a0fa944053c59e5f3b0d3d7f986b2a9e0bb990133525827` | `PASS` |
| exact 文档 98 | `930b9d98aef0b783187f5e965bf49aec895ff871e461d0ac70cb52e841b452ce` | `github-paired-4ac2e1eb86ff477bae122c48a72dd8c4` | `98c3c34bd6f2f3d62c16cc850f3c6c643e869bdc27a4344192382a43003d2975` | `cda35518a5b44533c91014ea21d2e1de8b24eb5e798550f5f501f2f56d664335` / `0ec470000a3260b9fe8445e8c9c5f26261a8b10142b274750967b9fe82cd5031` | `ee9b64b95337b4ef1d444a19c941aa93b853f0870f4f6660c2c137437d7b7d10` | `PASS` |

两条链均满足：

- P1/P2 为 `PUBLISHED / COMPLETE`，P1 精确 commit 与候选主线一致；
- requested/final URL 均保持相同 GitHub exact-SHA Markdown 坐标；
- 同一 pair 内 session 一致，P1/P2 Evidence 与 request seal 仍保持独立；
- README marker `P4_RELEASE_NOT_STARTED` 出现 2 次，本文 marker `availability recovery` 出现 1 次；
- 两页各自三个 sample digest 完全相同，`samples_stable=true`；
- `errors / conflicts / cleanup_errors / coverage_reasons` 均为空；
- Core 只消费 handoff 指定的 imported Evidence snapshot，并分别得到 `PASS`。

README 链完成标准 Evidence、handoff 与 Acceptance Bundle 后，第一版仓库外摘要包装器错误假定报告顶层
存在 `canonical_digest` 字段并退出。该错误发生在摘要整理层，不改变已经落盘的标准产物和 Core `PASS`；
后继步骤直接读取公共报告并以 `sha256_json(report)` 计算规范摘要，没有重跑 README 网络观察，也没有把
包装层错误改写成 Collector 成功或失败。全部运行产物继续留在仓库外。

## 7. 状态发布的最后门

本次收口只允许文档与索引变化。它自身仍须完成原始远端 Public CI 11 项、受保护主线合入，以及从新
exact main 对 README/本文的匿名产品读回。只有该链全部成立，以下状态才成为后续 P4 施工可消费的主线
事实：

```text
RELEASE_DOWNLOAD_RECOVERY_FROZEN
P4_CONTRACT_0.1_FROZEN
P4_RELEASE_NOT_STARTED
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```

该状态不创建 `github-evidence-v*` ruleset、tag、Release 或资产，不改变 Core `v0.12.2` 的 Latest 身份，
也不把外部传输恢复能力扩张成资产完整性或 GitHub 内部根因证明。
