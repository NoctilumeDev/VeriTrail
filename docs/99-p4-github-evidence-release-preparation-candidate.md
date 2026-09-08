# P4 GitHub Evidence Plugin 发布准备候选事实 0.1

> 后继事实：本页的 clean-install 使用当前源码本地构建、版本仍为 `0.12.2` 的 Core wheel；最终
> exact-main 门改用公开 `v0.12.2` wheel 后确认其不含 P3 所需 Acceptance API。因此本页仍是历史候选
> 证据，不再支持进入 tag/Release；修正合同见
> [文档 100](100-core-v0.13.0-acceptance-api-release-contract.md)。

> 当前状态：`P4_RELEASE_PREPARATION_CANDIDATE / NO_TAG / NO_RELEASE`
>
> 精确施工基线：`b6ddb5c8a704b464dc9b4d07a0f43b7b93a64a71`
>
> 发布资产工具提交：`e62836bd8981f78df28c6f3e2067ef396f41121a`
>
> 真实 GitHub 候选门提交：`fe1f01249365a91e29becbef08b62aa6624c9481`
>
> 影响层级：`L1_COMPONENT_INTERNAL`；只增加发布资产构建/核验工具、真实候选验收探针与测试，
> 不修改 P1–P3、Acceptance Core、Evidence、Verdict 或 P4 已冻结的公开发布合同

## 1. 当前裁决

P4 发布准备已形成可提交候选，但尚未取得发布资格。当前代码能够从精确、干净源码构建固定 wheel 与
sdist，核验候选 metadata、归档边界、双构建一致性和非自指摘要顺序；候选 wheel 又在两套 Python 的
独立安装环境中完成 base、sdist、render、卸载与真实 GitHub 正向链。

这些事实只支持：

```text
P4_RELEASE_PREPARATION_CANDIDATE
NO_TAG
NO_RELEASE
NO_PUBLIC_DOWNLOAD_CLAIM
```

它们不支持提前生成 validation summary，不支持复用本地候选字节作为最终 Release 资产，也不支持
`P4_FROZEN`。发布准备 PR 必须先取得自己的原始远端门禁并合入受保护主线；最终字节只能从合入后的
新 exact main 在新 clean detached worktree 中重建。

## 2. 薄工具边界

`scripts/github_evidence_release_assets.py` 只拥有候选资产的构建、规范化、核验和关闭责任：

```text
exact clean source
    -> two independent builds
    -> deterministic sdist normalization
    -> byte/content/metadata comparison
    -> external build facts
    -> exact validation facts
    -> pre-tag validation summary
    -> checksum manifest
    -> independent verification
```

工具不调用 GitHub API，不创建 ruleset、tag 或 Release，不上传资产，不产生 Core Verdict。validation
summary 只白名单复制冻结字段；本地路径、日志、token 和未知扩展字段不能进入公开候选摘要。成功文件
只在完整校验后以 create-new 语义生成，不能覆盖已经关闭的同名产物。

`scripts/p4_real_github_acceptance.py` 只建立一个预封存真实候选 Plan，并从已安装 Core/plugin 运行：

```text
P1 anonymous API
    -> P2 fresh anonymous Chromium
    -> exact two-Evidence handoff
    -> Acceptance Core
    -> PASS
```

它拒绝从 checkout 导入产品模块，不参与构建、发布或 GitHub 写操作，输出也明确标记
`RELEASE_CANDIDATE_NOT_PUBLIC_DOWNLOAD_EVIDENCE`。

## 3. 候选资产构建事实

从提交 `e62836bd8981f78df28c6f3e2067ef396f41121a` 的独立源码副本进行两次构建。该提交之后新增的真实
验收脚本和测试位于仓库根，不进入插件 wheel/sdist；它们只验证候选，不改变 distribution 内容。两次
构建经 sdist 规范化后逐字节一致：

| 资产 | Size | SHA-256 | 双构建 |
| --- | ---: | --- | --- |
| `veritrail_github_evidence-0.1.0-py3-none-any.whl` | 69026 | `142b6e33200cca501f1873c8d24244f53ecc86fd808661a700011814b7b054d0` | `BYTE_IDENTICAL` |
| `veritrail_github_evidence-0.1.0.tar.gz` | 78467 | `f9613f23465a6e2407d6c89c205bd83aa4317ef233ac93bb4a93a5f78e71f11b` | `BYTE_IDENTICAL` |

构建同时确认：distribution/import/version 为
`veritrail-github-evidence / veritrail_github / 0.1.0`，Core dependency 精确为
`veritrail==0.12.2`，render extra 只增加 `playwright==1.62.0`；归档没有绝对路径、路径穿越、重复
member、symlink/hardlink 或 Chromium/browser payload。

这两项只是本地候选字节。`github-evidence-v0.1.0-validation-summary.json` 与
`SHA256SUMS-github-evidence.txt` 尚未生成；它们必须等待发布准备 PR 的 Public CI 与新 exact main
事实成立后才能关闭。

## 4. 本地串行矩阵

所有源码回归均显式绑定当前 worktree 的 `src`、插件 `src` 与测试根；clean-install 门只从独立 venv
的 `site-packages` 读取候选：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| 发布资产/真实 Plan 定向，普通 / `-O` | `11/11` / `11/11` | `11/11` / `11/11` |
| Core 全量，普通 / `-O` | `414/414` / `414/414` | `414/414` / `414/414` |
| GitHub Evidence 全量，普通 / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| base wheel，无 Playwright | `PASS` | `PASS` |
| normalized sdist 安装 | `PASS` | `PASS` |
| render extra + matching Chromium | `3/3` | `3/3` |
| plugin uninstall 后 Core-only P3 复算 | `PASS` | `PASS` |

两套 Python 的 base 环境均确认 P1 import/CLI/Collector 不触发 Playwright；render 环境则只在显式安装
extra 后取得 Playwright 1.62.0 与 matching bundled Chromium。卸载插件后，Core 仍可读取已经形成的
标准 Evidence/AcceptanceBundle，插件能力没有倒灌 Core 完整性。

## 5. 真实 GitHub 候选链

候选 wheel 从独立 3.10/3.13 render venv 读取，在未提供 `GITHUB_TOKEN`、`GH_TOKEN` 或
`VERITRAIL_GITHUB_TOKEN` 的条件下，分别对以下预声明坐标运行：

```text
NoctilumeDev/VeriTrail
README.md
commit b6ddb5c8a704b464dc9b4d07a0f43b7b93a64a71
marker VeriTrail
```

两次运行使用同一个预封存 Plan digest
`79f41394f46019320b3cb214d639ee98b8cd1778d5f308fa30606f4b74c56607`，但建立独立 request、session、
Evidence 与 Core Run：

| Python | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report digest | Verdict |
| --- | --- | --- | --- | --- | --- |
| 3.10 | `github-paired-bfdfae9b870148129da41a5cc4a69945` | `062de38582140d08dc7f26012523378ad7e37a00cb20bb180c25f0be8f3c2c62` | `c7def4798725b9ac89f79af9119a668a3182d5d4c30ada479e18e4509645a32e` / `8fc218fcbda5ab37d5466d5ecf7d140e41b7ee9651b5b8b041fbb363e740a201` | `1bd6a0bcc79900bfe8c01d95f487e44853554ac854197369adbd38b1b23b65fa` | `PASS` |
| 3.13 | `github-paired-1e6428459ffd45228cecafc128cfe4fc` | `68080a7fdf93090a85f9f7f5c87ef65e8edc958877d5b975ef3803b8f71281e3` | `d5971c4d2c34e31957563b087e953483c1419c70fc49ae6df730d3c630934728` / `6d857aa32abe576b32652bb898e112d8c8218e383e438d7817957139200cef55` | `bbf2e9547fc36ffbd32b224620a600164102e7956b4ba6e9455a7ea4f8fcb106` | `PASS` |

两条链均满足：

- API 为 `ANONYMOUS / COMPLETE`，Render 为 `ANONYMOUS_FRESH_CONTEXT / COMPLETE`；
- P1 与 P2 严格按 `github-api -> github-public-render` 串行，同一 pair 内 session 一致；
- requested/final URL 均保持同一 exact-SHA README 坐标，HTTP 200；
- 三次样本摘要均为
  `85be0a364ee00dfa4425e5a3fc106712d8f55c2b9b29aa90f75461586b927df2`，marker 出现 23 次；
- response-body active streams 为 0，errors、conflicts、coverage reasons 与 cleanup errors 均为空；
- handoff 只把同一 imported Evidence snapshots 交给 Core，全部规则为 `PASS`。

这两次成功只说明当前网络路径与 GitHub 在对应观察窗口内支持候选链，不证明代理或 GitHub 长期稳定，
也不把 GitHub API 与公开页面描述为独立第三方权威。

## 6. 被保留但不进入通过结论的执行事实

- 第一次新增测试未设置当前 worktree 的 `PYTHONPATH`：3.10 从旧 Review Attention worktree 导入 Core，
  3.13 找不到插件包。该结果只证明 import coordinate 错配，随后显式读回模块路径并从头重跑；
- 第一次 Core 全量组的外层 shell 总预算只有 120 秒，而有效运行约需 130 秒，因执行器超时被中断；
  中断后确认无 Python/Chromium 残留，再以 300 秒外层预算重跑同一 3.10 普通组并通过 414/414；
- sdist clean-install 的一次 PowerShell inline Python 引号错误，以及 render 测试的一次 discovery 根目录
  错误，都在同一 venv 中按正确坐标重跑；两者不归因给 package，也不被改写成产品通过证据。

这些失败与后继通过分别保留，后继绿灯不声称旧运行“其实成功”。

## 7. 远端门与停止线

当前尚未发生：

```text
release-preparation PR
original Public CI 11/11
protected-main merge
new exact-main Public CI + Browser Smoke
github-evidence-v* tag ruleset
github-evidence-v0.1.0 tag
GitHub Release
public assets / anonymous downloads
```

因此下一步只能推送本候选并等待原始门禁。任何红灯先按其事实层分类；不能通过 rerun、放宽摘要、
复用当前候选字节或混入 Dependabot 变更取得发布资格。候选合入后还必须从新的 exact main 重建全部
最终字节、重跑最终本地矩阵，再按“tag 保护先于 tag”的顺序进入公开发布。

R1 继续等待 P4 最终冻结与 Pattern Corpus 精确冻结，本候选不解除该阻断。
