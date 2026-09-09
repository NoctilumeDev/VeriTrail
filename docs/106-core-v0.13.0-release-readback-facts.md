# Core 0.13.0 发布与公开读回事实

> 状态发布目标：`CORE_0.13.0_RELEASED / MAINTENANCE_FROZEN / C3_CLOSED / P4_RELEASE_NOT_STARTED`
>
> 发布源码坐标：`main@cd6f85246c0a789a3117861144af95deeb1b7077`
>
> 影响层级：`L0_PRESENTATION + L2_CONTRACT`；只记录已经发生的 Core 发行身份、公开字节与
> 兼容边界，不修改 Core、Acceptance、P1–P3、Verdict 或 GitHub Evidence Plugin 的运行语义
>
> 本文自己的原始门禁、受保护主线合入与合入后 exact-main 匿名读回全部成立后，C3 才关闭，
> P4 的 Core 发行阻断才解除。

## 1. 最终结论与坐标

- 版本：`0.13.0`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.13.0>；
- Release ID：`385190618`；
- 发布时间：`2026-09-09T02:44:29Z`；
- 注释标签：`v0.13.0`，tag object
  `a03c7a1fbcff88291c8cb86f2718c8d76d1ed709`；
- 标签解引用提交：`cd6f85246c0a789a3117861144af95deeb1b7077`；
- 源码 tree：`cf9e996426535eb2131d1ed988a3bfdb03d70a62`；
- Release `targetCommitish` 字段：`main`；最终代码身份以受保护注释标签的解引用提交为准；
- Release 为非 draft、非 prerelease；匿名 API 读回的 Latest Core 为 `v0.13.0`；
- 历史 `v0.12.0`、`v0.12.1`、`v0.12.2` 标签、Release 与资产未移动或重制。

本文闭合[文档 100](100-core-v0.13.0-acceptance-api-release-contract.md)定义的 C2/C3 出口、
[文档 102](102-core-v0.13.0-release-candidate-plan.md)的最终资产停止线，以及
[0.13.0 Release Notes](103-v0.13.0-release-notes.md)的公开读回。0.13.0 只为已经冻结的
AcceptancePlan、四 Verdict、Acceptance Bundle 与 imported-snapshot 公共入口建立新的公开 Core
身份；它不新增 Acceptance 语义，也不把 GitHub Evidence Plugin 并入 Core。

## 2. 精确主线、构建与门禁

C2 没有复用 C1 候选字节。最终资产从干净 detached worktree 的 exact
`main@cd6f85246c0a789a3117861144af95deeb1b7077` 重新导出并构建：542 个 tracked 文件与 542 个
导出文件一一对应，源归档 SHA-256 为
`2ced5389a08fbae888602c4d63e3f66135a60a4026d8f5aebc975c9bbeee1f9d`。

该 exact main 的公共门禁为：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 34300831769](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34300831769) | attempt 1，`11/11 SUCCESS`，`headSha` 为发布源码提交 |
| [Browser Smoke 34300831740](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34300831740) | attempt 1，`1/1 SUCCESS`，`headSha` 为发布源码提交 |

其中 Core 在 Python 3.10/3.13 的 normal 与 `-O` 四组均为 `416/416`；Authoring Skill 每组
`24/24`，GitHub Evidence 每组 `180/180`，Starter/Authoring 的历史 Core 0.12.2 通道每组
`24/24`。Workbench `173/173`、lint、type-check、生产构建与依赖审计全部通过，依赖审计为零漏洞。

PR #79 候选、PR #80 M11 夹具修正与 PR #81 修正闭环的原始门禁和因果顺序继续保留；尤其
`Public CI 34295582018` 的既有 Python 3.13 `-O` 失败没有被本次发行绿灯删除、改名或解释成从未发生。

## 3. 最终公开资产与摘要

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.13.0-py3-none-any.whl` | 220,194 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| `veritrail-0.13.0.tar.gz` | 338,737 | `14cd126a1c3cf4a6de17fbcd2b4654d420d94be2d986033661630daa7079e89c` |
| `veritrail-workbench-0.13.0.zip` | 7,779,858 | `326f2fd4666e437175a10b693d9c642b0d854a6071d2234f2af5733ae12d9219` |
| `core-v0.13.0-validation-summary.json` | 8,452 | `2b3c18bcbdbd8f6950588dc7cf4f31aee4dda1cb3325b365235bc72e9ad3d5f0` |
| `SHA256SUMS.txt` | 390 | `328aa6c0aeb64a7ae80cbd5065eebb8ef5b3482e18a460a1d173ffc0897097cd` |

GitHub API 为五项 asset 返回的 `state=uploaded`、大小和 digest 与上表逐项一致。匿名下载副本也与
上传前 final staging 的大小和 SHA-256 逐项一致。

`SHA256SUMS.txt` 遵循冻结的非自指顺序，只覆盖 wheel、sdist、Workbench ZIP 与 validation summary；
它自己的摘要由外部发布事实和匿名下载读回固定。Validation summary 在 tag 创建前生成，因而其中
`C2_LOCAL_ASSETS_VERIFIED / PRE_TAG`、`release_tag_exists_at_generation=false` 和“不作公开下载声明”
是准确的时间切片；发布后没有重制该文件来擦除顺序。

wheel 含 48 个条目，sdist 含 116 个条目；二者均无重复或不安全归档路径，metadata 版本为
`0.13.0`。Workbench ZIP 的根级 `index.html` 唯一，63 个文件与生产 `web/dist` 内容逐项一致，
无重复或不安全条目。Workbench 源码版本仍为 `0.12.0`；ZIP 的 0.13.0 名称只表示随本次 Core
发行复验并分发的伴随生产构建，不冒充 Workbench 独立语义版本升级。

## 4. 匿名下载后的仓库外复验

五项资产均通过无 GitHub token 的公开 URL 下载；每项在第一次 attempt 成功，并在摘要匹配后才作为
可消费文件暴露。下载恢复工具没有放宽资产身份或摘要规则，历史 HTTP 500 反例也没有被本轮成功覆盖。

| 输入 | 环境 | 结果 |
| --- | --- | --- |
| wheel | Python 3.10.6 clean venv | 版本/仓库外 `site-packages` 来源、`pip check`、四 Verdict 与 imported snapshot 全部通过 |
| wheel | Python 3.13.13 clean venv | 同上，全部通过 |
| sdist | Python 3.10.6 clean build/install | 版本/来源、`pip check`、normal/`-O` 四 Verdict 与 imported snapshot 全部通过 |
| sdist | Python 3.13.13 clean build/install | 同上，全部通过 |
| Workbench ZIP | 独立解压与真实 Chromium | `5/5 PASS`，102 个请求、零 HTTP error、服务端口最终释放 |

公开 wheel 在两套 Python 中都独立复算 `PASS / FAIL / INCONCLUSIVE / PENDING`，并通过同一
`ImportedEvidence` snapshot 入口；这正面关闭了公开 `v0.12.2` wheel 缺少 Acceptance API 的发行身份
缺口。它不改变 Starter 0.2.0 与 Authoring Skill 0.2.0 的 `>=0.12,<0.13` 冻结兼容边界；二者的正向
真实链继续使用公开 Core 0.12.2。GitHub Evidence 的 distribution 依赖仍未在本轮修改，必须由 P4
使用独立新版本坐标处理。

## 5. 匿名 Release 页面与 API 读回

产品 P2 Public Render Collector 在 fresh anonymous Chromium context 中读取公开 Release 页面：

- requested/final path 均为 `/NoctilumeDev/VeriTrail/releases/tag/v0.13.0`，HTTP 200；
- 初态 `cookies=0 / origins=0`；固定 Release body scope 唯一；
- 三次规范化样本稳定；`VeriTrail 0.13.0 Release Notes` 出现一次；
- 92 个网络请求；coverage conflict、Collector error 与 cleanup error 均为零；
- facts digest：`e1e8366c7312832669d46834b5df6188ce0a76a82fbcee2ebd6c1ee0431ed649`。

第一次探针使用页面外层标题 `VeriTrail Core 0.13.0` 作为 body-scope marker，得到 occurrence 0；该输出
被保留为“页面标题不属于固定 Release body scope”的边界校准，没有通过改 Collector 或放宽 scope
把它洗成成功。后继探针使用正文标题后得到上述完整读回。

匿名 API 同时确认 Release 非 draft、非 prerelease、五项资产均已上传，`v0.13.0` 为当前 Latest，
受保护注释标签仍解引用到发布源码提交。API 与公开 Render 是同一 GitHub 信任域的两个观察面，
本轮没有把它们表述成两个独立真实性权威或平台原子快照。

## 6. 治理边界与 C3 出口

- main ruleset `21436452` 继续要求 Pull Request 与七项 required checks，并禁止删除与强制更新；
- Core tag ruleset `21437132` 继续覆盖 `refs/tags/v*`，无 bypass，禁止删除与 non-fast-forward 更新；
- 两个既有 Dependabot PR #16/#67 仍是独立外部队列，未进入本次发布或状态补丁；
- Release 本身不被描述为平台级不可变对象；长期源码身份由受保护注释标签固定，公开字节身份由
  asset digest、非自指 checksum 与匿名下载读回共同约束；
- 本轮没有运行 Codex Security 深度扫描、攻击路径验证或极端攻击工作流；这些工作按既定范围继续
  不作声称，普通 CI、浏览器与发布读回不得冒充对应证据；
- macOS、Linux、C0/C2/C3、Docker、多服务、恶意代码隔离和通用项目自动探测不因本发行新增证明。

当且仅当本文状态补丁自己的原始门禁、受保护主线合入与合入后 exact-main README/本文匿名公开读回
全部成立，状态才推进为：

```text
CORE_0.13.0_RELEASED
CORE_0.13.0_PUBLIC_READBACK_COMPLETE
CORE_0.13.0_MAINTENANCE_FROZEN
C3_CLOSED
P4_RELEASE_NOT_STARTED
```

这只解除 P4 的 Core 公开发行阻断。P4 下一步仍须从新的 exact main 单独重开插件 distribution
依赖坐标、保护 `github-evidence-v*` 标签、重建最终插件资产并完成其自身的公开读回；不得复用旧 P4
候选字节，也不得把 Core 0.13.0 的成功继承为插件 Release 证据。Review Attention R1 仍等待 P4 与
精确 Pattern Corpus 双冻结。
