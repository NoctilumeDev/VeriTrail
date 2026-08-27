# Core 0.12.2 发布与公开读回事实

## 1. 最终结论与坐标

- 状态：`RELEASED / MAINTENANCE FROZEN`；
- 版本：`0.12.2`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2>；
- 发布时间：`2026-08-27T21:02:03Z`；
- 注释标签：`v0.12.2`，tag object
  `2177bb2cc02d9ef9068e7b7132983c5edb82be6c`；
- 标签解引用提交：`f961930ae1e69d7d88849fa2b0d40befb3e94c89`；
- Release `targetCommitish` 字段：`main`；最终代码身份以受保护注释标签的解引用提交为准；
- 历史标签 `v0.12.0`、`v0.12.1` 未移动；Core `v*` 标签规则禁止删除与非快进更新。

本文是[文档 74](74-core-demo-catalog-binding-maintenance-contract.md)停止线的执行事实，也是
[0.12.2 Release Notes](75-v0.12.2-release-notes.md)的公开读回闭环。它只关闭 demo producer 的
最终 Artifact root 绑定缺口，不重开 M0–M14，不修改 Catalog Schema、`catalog_id`、Run identity、
Verdict、公共 `build_catalog()` 语义或 Workbench，也不放宽 `catalog-serve` 的 fail-closed 校验。

## 2. 受保护 PR 与精确合并后门禁

发布准备提交 `9be06a52db740b85920e75c0f4cd5a0c3e5afdbe` 经
[PR #14](https://github.com/NoctilumeDev/VeriTrail/pull/14) 的七项 required checks 全部通过，合并为
`f961930ae1e69d7d88849fa2b0d40befb3e94c89`。最终合并提交的精确 post-merge 门禁为：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 33114343509](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33114343509) | `SUCCESS`；`headSha` 为最终合并提交 |
| [Browser Smoke 33114343542](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33114343542) | `SUCCESS`；`headSha` 为最终合并提交 |

Public CI 的精确矩阵为：

- Core Python 3.10 普通／`-O` 各 `347/347`；Python 3.13 普通／`-O` 各 `347/347`；
- Starter 两套 Python 普通／`-O` 每组 `24/24`；Authoring Skill 同样每组 `24/24`；
- Workbench `172/172`、lint、type-check、生产构建与依赖审计通过，依赖审计为零漏洞；
- 无 checkout candidate wheel 在 Python 3.10／3.13 均通过；
- Starter 真实 PASS／故意 FAIL 黄金路径一次通过、无 retry，job `98666631419` 用时 `2m5s`。

Browser Smoke 读回五项真实浏览器检查，结果为 `COMPLETED / PASS`，HTTP error 为零、网络请求
102 个、端口最终释放。PR 绿灯与 post-merge 绿灯分别证明不同提交阶段，本文不以其中一者替代另一者。

## 3. 发布资产与摘要

五个公开资产均从最终合并提交的干净 detached worktree 重新构建，没有复用早期 staging 字节：

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.12.2-py3-none-any.whl` | 198,729 | `3a42f28db6f4ed12351dade3fbb6f57fa1d5aa3fdd6d28210492f676bc1562de` |
| `veritrail-0.12.2.tar.gz` | 281,151 | `290a4238ef25e9daba68ea02e6e66c9acf1673df2b2dd27aaa0e8e7928e46708` |
| `veritrail-workbench-0.12.2.zip` | 7,779,810 | `3b5a851813f1b23faa0aa3ed1822e8f8066b8640ab92dc414a9fd9e4111b8082` |
| `core-v0.12.2-validation-summary.json` | 6,451 | `e7802ed78778eeca1f757359acc4d566b3b447b14c99bba06e245e961725190d` |
| `SHA256SUMS.txt` | 390 | `358d7f7ab4df33d0defd0f53a1f595f615b71f917e92be4ef7468d20fb371fd8` |

`SHA256SUMS.txt` 使用非自指约定，只覆盖前四个 payload；其自身由冻结上传副本与公开下载副本逐字节
比较。GitHub 为五个 asset 返回的 `digest`、公开下载后的文件大小与本机 SHA-256 均与上表逐项一致。
公开下载的 `SHA256SUMS.txt` 四行也对全部 payload 重新验真通过。

Workbench ZIP 包含 63 个文件与 4 个目录条目；63 个文件与最终提交的生产 `web/dist` 按内容
`63/63` 一致。Workbench 源坐标仍为 `0.12.0`，ZIP 名称中的 `0.12.2` 表示随 Core 0.12.2 Release
重新验证和分发的伴随资产，不冒充 Workbench 独立语义版本升级。

验证摘要在创建标签前生成，因此其中
`RELEASE_CANDIDATE / PUBLIC_GATES_GREEN / PRE_TAG` 与“当时稳定版仍为 0.12.1”是准确的时间切片，
不是发布后状态漂移，也不得事后重制该摘要来擦除证据顺序。

## 4. 公开下载后的仓库外复验

下列复验在发布后由受控 16 GiB Windows 主机从匿名公开 URL 下载资产，并在仓库外执行；它不使用
本地构建 staging。该轮没有 GitHub-hosted post-release execution log，因此本文记录的是公开资产的
本机下载与运行读回，不把它扩张为第三方托管执行或社区独立复现。

| 输入 | 环境 | 结果 |
| --- | --- | --- |
| wheel | Python 3.10.6 clean venv | 版本 0.12.2、`pip check`、PASS／故意 FAIL demo、Catalog READY、两 Run／零 issue、PASS Bundle 读回、搬移负对照全部通过 |
| wheel | Python 3.13.13 clean venv | 同上，全部通过 |
| sdist | Python 3.10.6 clean venv | 从公开 sdist 构建安装后重复适用完整链，全部通过 |
| Workbench ZIP | 独立解压 | 63 个文件、根级 `index.html` 与生产构建内容一致 |

每条 Core 链都保留 `SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE`，完整搬移已经发布的 demo 后，
`catalog-serve` 仍精确拒绝 `ARTIFACT_ROOT_MISMATCH`。这同时证明 producer 组合链恢复、verifier
没有被削弱；它不证明 VeriTrail 自身或任何外部项目已经通过业务验收。

公开复验生成的 JSON／Markdown 中，构建路径或验收机绝对路径命中数为零。测试结束后，owned
服务进程、监听端口、SQLite sidecar、demo／Catalog staging 残留均为零。

## 5. 治理事实与边界

- `main` ruleset `21436452` 要求 Pull Request 与七项 strict required checks，并禁止删除与
  non-fast-forward 更新；
- Core 标签 ruleset `21437132` 保护 `refs/tags/v*`，禁止删除与 non-fast-forward 更新；
- `v0.12.0` tag object `e252d8b5a8857ff6b7f2acf0a6b501adc85465c9` 仍解引用到
  `3216f5494db76939d94f2c76db096851a05e9b4c`；
- `v0.12.1` tag object `0bdedebd27d35c093b6bfba575e1b81305375a10` 仍解引用到
  `1d3e5a053dfca26837ec4293b11a17f016973413`；
- GitHub Latest Release 已读回为 `v0.12.2`；Release 非 draft、非 prerelease；
- GitHub API 对该 Release 返回 `isImmutable: false`。因此不能声称平台级不可变 Release；长期身份由
  受保护注释标签，字节身份由 asset digest、公开下载摘要和本文共同约束；
- 本轮没有运行 Codex Security 深度扫描、攻击路径验证或极端攻击工作流。它们按既定决定继续封存，
  普通 CI、浏览器和发布读回不得冒充这些安全证据；
- macOS、Linux、C0/C2/C3、Docker、多服务、恶意代码隔离和通用项目自动探测仍不在本维护版的新增
  证明范围内；
- Starter 与 Authoring Skill 仍只生成 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`，不能 Seal、Run
  或裁决。

文档 74 的全部停止线已经满足。Core 0.12.2 因此可以准确描述为已发布、已公开读回并完成有界维护
冻结；后续 Core payload 修改必须使用新的提交、合同与版本坐标，不能移动或重制 `v0.12.2`。
