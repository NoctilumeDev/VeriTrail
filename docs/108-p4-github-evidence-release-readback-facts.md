# P4 GitHub Evidence Plugin 发布与公开读回事实

> 状态发布目标：`P4_GITHUB_EVIDENCE_0.1.0_RELEASED / P4_FROZEN / R1_BLOCKED_UNTIL_PATTERN_CORPUS_FREEZE`
>
> 发布源码坐标：`main@548b17ccb1f20d55a9f9beef6666e913af5f65d9`
>
> 影响层级：`L0_PRESENTATION + L2_PUBLIC_DISTRIBUTION_STATUS`；只记录已经发生的插件发行、公开字节与
> 读回事实，不修改 P1/P2 Collector、P3 handoff、Acceptance Core、Evidence、Verdict 或 P4 合同语义
>
> 本文自己的原始门禁、受保护主线合入与合入后 exact-main 匿名读回全部成立后，P4 才最终冻结。

## 1. 最终结论与坐标

- distribution / import / version：`veritrail-github-evidence / veritrail_github / 0.1.0`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.0>；
- Release ID：`385275245`；
- 发布时间：`2026-09-09T06:38:22Z`；
- 注释标签：`github-evidence-v0.1.0`，tag object
  `bdc417058622732a00571eb4c39dc6a758d37b72`；
- 标签解引用提交：`548b17ccb1f20d55a9f9beef6666e913af5f65d9`；
- 源码 tree：`6b0aa67040c914aa49aa4d3ae8db33425415aca1`；
- merge parents：`ab874d3cfd9ac140654e35d84b0025c2503e10cd` 与
  `ad773fbc1e13bd62ba0dcd825906939df2d5d9d6`；
- Release `target_commitish=main`；最终源码身份以受保护注释标签的解引用提交为准；
- Release 为非 draft、非 prerelease，GitHub API 如实返回 `immutable=false`；
- 插件 Release 显式保持 non-Latest；匿名 Latest API 仍返回 Core `v0.13.0`，Release ID
  `385190618`；
- P4 没有发布到 PyPI，也没有移动或重制 Core、Starter、Authoring Skill、M/E/P 历史标签或资产。

标签创建前已启用 tag ruleset `22613490`（`Protect GitHub Evidence release tags`）：target 为 tag，
include 为 `refs/tags/github-evidence-v*`，无 bypass，并禁止删除与 non-fast-forward 更新。该 ruleset、
annotated tag、GitHub Release 与下载摘要分别承担治理、Git 对象、平台发布面与字节身份，不能相互替代。

## 2. 精确主线与门禁

发布恢复提交 `ad773fbc1e13bd62ba0dcd825906939df2d5d9d6` 经
[PR #83](https://github.com/NoctilumeDev/VeriTrail/pull/83) 的原始
[Public CI run 34314354578](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34314354578)
在 attempt 1 上取得 11/11 `SUCCESS`，随后合入上述 exact main。该主线自己的公共门禁为：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 34315174017](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34315174017) | attempt 1，`11/11 SUCCESS`，`headSha` 为发布源码提交 |
| [Browser Smoke 34315174037](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34315174037) | attempt 1，`1/1 SUCCESS`，`headSha` 为发布源码提交 |

最终字节没有复用[文档 107](107-p4-github-evidence-release-resume-candidate.md)的本地候选，而是从 clean
detached exact main 重新构建。Core 416 项与插件 180 项在 CPython 3.10/3.13 的 normal 和 `-O` 四组
全部通过；最终 wheel/sdist 的 base、sdist、render、真实 Chromium、producer-side 8/32 MiB 预算、
插件卸载后 Core-only 复算与真实 GitHub 正向链也分别成立。

## 3. 固定公开资产与摘要

| 资产 | 字节数 | SHA-256 | GitHub asset ID |
| --- | ---: | --- | ---: |
| `veritrail_github_evidence-0.1.0-py3-none-any.whl` | 69,024 | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` | `552169516` |
| `veritrail_github_evidence-0.1.0.tar.gz` | 78,467 | `10212c34f82a320b0eed23f5b101459cc6d0519a220a66e5519e787a0b7c2c7d` | `552169518` |
| `github-evidence-v0.1.0-validation-summary.json` | 2,730 | `a6a04da7cd7e768d868cb724e47f6b5afd4d7d5b3e3abfea7b26b23fdb75bb76` | `552169521` |
| `SHA256SUMS-github-evidence.txt` | 333 | `f324f03c8e27053c90a097dfa5bb3b92e90698d3cc24352fd53d4d8a036b94ce` | `552169519` |

Release API 对四项资产均返回 `state=uploaded`，大小与 `sha256:` digest 和上表一致。匿名下载副本与
上传前 final staging 也逐项同大小、同 SHA-256。checksum manifest 只覆盖 wheel、sdist 与 validation
summary；它自己的摘要由外部发布事实与匿名下载读回固定，因此没有摘要自指。

Validation summary 继续准确保留生成时切片：`RELEASE_CANDIDATE / PUBLIC_GATES_GREEN / PRE_TAG /
NO_PUBLIC_DOWNLOAD_CLAIM`。发布后没有重制它来伪装成事后事实；tag、Release、checksum 自身与匿名下载
结果只记录在本文这类后继事实中。

## 4. 匿名下载后的仓库外复验

四项资产均从公开 Release URL 在未提供 GitHub token 的环境中下载，第一次 attempt 即成功；成功字节
只有在 SHA-256 匹配后才被暴露为可消费文件。随后对公开下载的 wheel 和 sdist 串行执行：

| 输入 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| base wheel + 公开 Core 0.13.0 | metadata、仓库外 `site-packages`、P1/P3、`pip check` 通过 | 同左 |
| wheel + 显式 render capability | Playwright 1.62.0、matching Chromium 151.0.7922.34、真实启动与预算测试通过 | 同左 |
| normalized sdist build/install | metadata、base 能力与 `pip check` 通过 | 同左 |
| plugin uninstall 后 Core-only | 标准 Evidence/handoff 复算为 `PASS` | 同左 |

公开插件运行的两条预封存真实 GitHub `P1 -> P2 -> P3` 链共享 Plan digest
`ed49d9c5592258eb2171c2de3a7f8047cae439f4cef85a81159481404d1e9e17`，但使用独立 request、session、
Evidence、handoff 与 Core report：

| Python | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report digest | Verdict |
| --- | --- | --- | --- | --- | --- |
| 3.10 | `github-paired-915dd09e96264f26b0cfc794d4a32374` | `247c972554e58d9f4ac1b7198ea801053f4bdbd7c82315329fdd2f4addbbdb26` | `b92622c83887d238110b9c0655d7c933867878247f55645c5616a055c3cf3c91` / `02d7fe43ba043bddc58c63ce7c167c00b22d3b98423b3a8963dd8e7b946f1751` | `1191b98123fadf40c15da07a02efec6db2f68e87b40df5e6559d48404faf8e13` | `PASS` |
| 3.13 | `github-paired-623520c6f0c74399aedc1c18c241176` | `b98682746ae304276509bdc6d40ef4a0c9c8baf07356b08be231bc6ba9e13e6e` | `f13d5b40dee6c829e5431273b6144e74bb0f8e8a1bff9f351851efea412ae802` / `ca6a09d4b332d428ab91143d38a6bb169b7d8d18de79a9022039bbe392a1af13` | `459f381eabe714c98370e93658989691d5578ef4807822d7ccc5e0e5cc146122` | `PASS` |

两条链都精确指向 `main@548b17...`，安装版本为 Core/plugin `0.13.0 / 0.1.0`，且没有把相同 Plan
解释成相同执行身份。结束时 owned browser/node 进程和 `.veritrail-*` staging 均为 0。

## 5. 匿名 Release 页面与 API 读回

公开 wheel 的 P2 Public Render Collector 在 fresh anonymous Chromium context 中读取插件 Release：

- requested/final path 均为
  `/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.0`，HTTP 200；
- 初态为 fresh anonymous context；固定 Release body scope 唯一且 usable；
- 三次 sample digest 均为
  `c80c3c9f2cfada8ca9d91ba860ed916041daec770ed72a9cb602db48bd94b89a`；
- 正文标记 `GitHub-only release of the independently bounded VeriTrail GitHub Evidence Plugin 0.1.0.`
  出现 1 次；
- 94 个请求中 2 个写请求被只读策略阻断；它们保留为 observer-induced facts，不影响 coverage；
- response body active streams 为 0；`errors / conflicts / cleanup_errors` 均为空；
- Evidence SHA-256 为
  `6a211612bbd8e7b2f2a37450f392f7df24aed42de6591d3c95a06db2366e76ea`，facts digest 为
  `5f60008cdea50f57ca0b602f29be1a100ba6df1084027e7147a361fdebf81dc5`。

第一次页面探针选中了已经执行“卸载插件后 Core-only 复算”的旧环境，在启动 Chromium 前以
`ModuleNotFoundError: veritrail_github` 停止；它只证明环境坐标选错，未产生页面 Evidence。后继在独立
clean environment 中从公开 Core/plugin wheel 安装成功并发布上述标准 Evidence；随后终端摘要把
`ImportedEvidence` 错当成 mapping，产生 `TypeError`。该包装层错误发生在 Evidence 已关闭之后，没有
重跑网络来覆盖；本节直接从已发布标准 Evidence 读回事实。

匿名 API 同时确认 ruleset、tag、Release flags、non-Latest、四项资产与 digest。API 和 Public Render
仍是同一 GitHub 信任域的两个观察面，不是两个独立真实性权威，也不构成平台原子快照。内置浏览器控制
通道在本轮无法建立可信 Node bridge，因此没有产生 UI 自动化结论；它没有替代、否决或增强上述产品 P2
真实 Chromium Evidence。

## 6. 冻结边界与剩余阻断

- P4 只发布 GitHub Evidence Plugin 0.1.0；Core 0.13.0 继续拥有 Latest 身份；
- Release 平台面仍可变，`immutable=false` 被如实保留；长期源码身份靠受保护注释标签，公开字节身份靠
  asset digest、非自指 checksum 与匿名下载读回；
- 两个既有 Dependabot PR #16/#67 仍是独立外部队列，没有进入 P4 因果链；
- Codex Security 深扫、GitHub 之外的真实性锚、PyPI、macOS/Linux 与长期网络可用性没有因 P4 获得证明；
- P4 冻结只解除 Review Attention R1 的第一个前置条件；Pattern Ledger 仍须选择 exact commit，生成
  manifest digest，并逐项绑定 `pattern_id + selected_record_digest`。在此之前 R1 继续阻断。

P4 的结论是一个状态迁移，不是成功检查的加总：source、distribution、asset、tag/Release、公开下载、
安装/runtime 与最终状态发布各有独立身份。历史 HTTP 500、错误环境坐标和包装层错误继续保留，后继成功
不把它们改写成“从未发生”。

## 7. 本状态发布的最后门

本补丁只允许本文、README、插件 README、AGENTS 与里程碑索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 用产品 P1/P2 Collector、fresh anonymous Chromium 读取 README 与本文；
5. 两页均须 `PUBLISHED / COMPLETE`，URL 与 SHA 不漂移，三样本稳定，指定 marker 存在，Core 为
   `PASS`，且没有额外 error/conflict/cleanup error。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
P1_FROZEN
P2_FROZEN
P3_FROZEN
P4_GITHUB_EVIDENCE_0.1.0_RELEASED
P4_FROZEN
R1_BLOCKED_UNTIL_PATTERN_CORPUS_FREEZE
```

唯一允许的后继主干是冻结精确 Pattern Corpus，再单独判断是否启动 R1；不得把 P4 发布自动解释为 R1
已经开始。
