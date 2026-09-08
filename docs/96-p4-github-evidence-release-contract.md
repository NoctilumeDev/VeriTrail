# P4 GitHub Evidence Plugin 独立发布合同 0.1

> 候选状态：`P4_CONTRACT_0.1_CANDIDATE / RELEASE_NOT_STARTED`
>
> 精确设计基线：`main@9c58b7367712ae726b826b54115766b81444cdf1`
>
> 前置事实：[P3 最终冻结状态发布](95-p3-core-handoff-freeze-publication.md)
>
> 影响层级：`L2_PUBLIC_DISTRIBUTION_CONTRACT + BOUNDED_L3_RELEASE_GOVERNANCE`
>
> 本文只冻结独立插件的发布、标签、资产和公开读回边界；不修改 Core、P1/P2 Collector、P3
> handoff、Evidence、AcceptancePlan、Verdict、Workbench 或 Review Attention R0。

## 1. 目标

P4 只把 P1–P3 已冻结的 GitHub Evidence Plugin `0.1.0` 变成一个可寻址、可下载、可校验、可在
干净环境安装并可被 Core 独立卸载的公开产品坐标：

```text
exact protected main
    -> clean release build
    -> exact candidate bytes
    -> protected annotated tag
    -> non-Latest GitHub Release
    -> anonymous public download
    -> digest + clean-install + real-slice readback
    -> P4 freeze facts
```

P4 不增加 Collector 能力，不重新解释 P1/P2 facts，不改变 P3 handoff 或 Core Verdict。发布工程
发现产品语义缺口时必须停止，并把修正拆到独立补丁；不能借“只是打包”把实现变化混入发布提交。

## 2. 五类身份不得互相替代

| 身份 | 回答的问题 | 最低绑定 | 不能证明 |
| --- | --- | --- | --- |
| Source identity | 从哪一份源码构建 | exact commit、tree、clean worktree | 产物字节已经公开 |
| Distribution identity | 这是哪个 Python 产品版本 | distribution/import name、version、METADATA、dependency/extra | tag 或 Release 已存在 |
| Asset identity | 具体发布了哪些字节 | filename、size、SHA-256、固定资产集合 | GitHub Release 页面正确或下载可达 |
| Tag / Release identity | 哪个 Git 对象和 GitHub 发布页承载该版本 | protected annotated tag object、peeled commit、Release ID/tag/flags | Release 资产平台级不可变 |
| Public-download observation | 匿名用户实际取回了什么 | requested/final URL、HTTP 状态、观察时间、size、SHA-256 | 封存前事实真实或第三方独立见证 |

必须保持：

```text
Build success
    != Tag exists
    != Release exists
    != Asset uploaded
    != Anonymous download returns the same bytes
    != Installed capability works
```

GitHub Release 当前是平台可变表面。若 API 返回 `immutable=false`，P4 必须如实记录；即使未来平台
提供更强不可变能力，源码身份仍由受保护 tag 的解引用提交表达，字节身份仍由摘要和公开下载读回表达。

## 3. 产品与版本坐标

首个稳定插件坐标固定为：

| 字段 | 值 |
| --- | --- |
| Python distribution | `veritrail-github-evidence` |
| Import package | `veritrail_github` |
| Version | `0.1.0` |
| Annotated tag | `github-evidence-v0.1.0` |
| GitHub Release name | `VeriTrail GitHub Evidence Plugin 0.1.0` |
| Core dependency | `veritrail==0.12.2` |
| Python declaration | `>=3.10` |
| Verified Python series | CPython `3.10` 与 `3.13` |
| Distribution channel | GitHub Release only；P4 不发布 PyPI |

源码中的 `pyproject.toml`、wheel/sdist metadata、`importlib.metadata.version()` 与
`veritrail_github.__version__` 必须共同读回 `0.1.0`。任何一处漂移都停止发布，不能在构建脚本里
覆盖版本来“对齐”。

`render` 是同一 distribution 的显式 optional extra，不是第二个版本或第二个 wheel：

```text
base install
    -> P1 + P3 offline handoff
    -> no Playwright import or dependency

[render] extra
    -> playwright==1.62.0
    -> operator explicitly installs matching bundled Chromium
    -> P2 capability becomes available
```

P4 不把 Chromium 二进制、浏览器 Profile、认证材料或系统浏览器打入插件资产，也不允许 Collector
在运行时自动下载浏览器。

## 4. 标签治理必须先于标签创建

当前已有 tag ruleset 只保护：

```text
refs/tags/v*
refs/tags/m*
refs/tags/starter-v*
refs/tags/authoring-skill-v*
```

它们不覆盖 `github-evidence-v*`。因此在创建候选 tag 前，必须新增独立、active 的仓库 tag ruleset：

```text
Name: Protect GitHub Evidence release tags
Target: tag
Include: refs/tags/github-evidence-v*
Rules:
  - deletion prohibited
  - non-fast-forward update prohibited
Bypass actors: none
```

ruleset 的 ID、名称、include pattern、enforcement、rules、bypass 集合和观察时间进入发布事实。保护规则
未生效时不得先推 tag 再补保护。

`github-evidence-v0.1.0` 必须是 annotated tag。发布事实分别保存：

```text
tag name
tag object SHA
tag object type
tag message / tagger timestamp
ref target SHA
peeled commit SHA
```

tagger 信息只属于 Git provenance，不冒充现实身份认证或可信时间戳。GitHub Release 的
`target_commitish` 也不能代替 tag peeling。tag 一经推送不得移动、删除或重建；若源码必须变化，使用
新的 patch version 与新 tag。

P4 前后还必须读回并确认 Core、里程碑、Starter 与 Authoring Skill 的历史 tag 坐标没有变化。

## 5. 固定发布资产

GitHub Release 的上传资产集合必须精确为：

```text
veritrail_github_evidence-0.1.0-py3-none-any.whl
veritrail_github_evidence-0.1.0.tar.gz
github-evidence-v0.1.0-validation-summary.json
SHA256SUMS-github-evidence.txt
```

`SHA256SUMS-github-evidence.txt` 使用非自指约定，只覆盖前三个 payload。GitHub 自动生成的 source
archive 链接不是上传资产，不进入固定资产集合，也不获得 byte-for-byte reproducibility 声明。

同一 filename 在以下位置必须逐字节一致：

```text
final candidate directory
    == draft upload reported digest
    == published Release asset digest
    == anonymous public download digest
```

P4 不发布单独的 render wheel，不在 sdist/wheel 中夹带 Playwright/Chromium，不上传本地日志、HAR、
trace、Cookie、token、绝对路径、临时目录或未经脱敏的真实 Evidence。

## 6. 候选构建与 validation summary

最终资产只能从通过受保护主线门禁后的 exact main，在新建的 clean detached worktree 和仓库外临时
输出目录中构建。不得复用 PR artifact、editable install、旧 staging 或先前提交生成的 wheel。

构建过程必须记录：

- exact commit、tree、提交时间与工作树 clean 状态；
- CPython、pip、setuptools、wheel/build backend 的精确版本；
- distribution/import/version/Core dependency/render extra；
- 每个 payload 的 filename、size 与 SHA-256；
- 两个独立构建目录的包内容/metadata 比较结果；
- 若观察到逐字节可复现，可以记录该事实；未证明时不得把内容等价扩张为字节可复现；
- 全部候选门禁、失败保留与范围外声明。

`github-evidence-v0.1.0-validation-summary.json` 在 tag 创建前生成，状态必须保持：

```text
RELEASE_CANDIDATE
PUBLIC_GATES_GREEN
PRE_TAG
NO_PUBLIC_DOWNLOAD_CLAIM
```

它可以记录当时的 candidate bytes 和 Latest Core 坐标，但不能预写尚未发生的 tag object、Release ID、
匿名下载、最终 Verdict 或 `P4_FROZEN`。发布后的事实另写文档，不事后重制 validation summary 擦除
时间顺序。

## 7. 发布候选门禁

创建 tag 前必须严格串行满足：

1. P4 合同已经自己的 PR 门禁、受保护主线合入和 exact-main 匿名公开读回冻结；
2. 发布准备只包含 P4 所需的打包/验证/说明，不改变 P1–P3 公共语义；
3. 发布准备 PR 的原始 Public CI 11 个 job 全部成功，且 branch ruleset 声明的 7 项 required checks
   全部满足；不以 rerun 覆盖红灯；
4. 合入后的 exact main 再取得该 SHA 的 Public CI 与 Browser Smoke 成功事实；
5. Core 及插件完整普通/`-O` 回归在 CPython 3.10/3.13 全部通过；
6. base wheel 在两套 clean venv 中安装，环境中没有 Playwright，`pip check`、P1 CLI/import 与 P3
   AcceptanceBundle/卸载后 Core-only 复算通过；
7. sdist 在两套 clean venv 中构建安装，版本、入口、dependency、optional extra metadata 与 base
   能力读回一致；
8. wheel 的 `[render]` extra 在两套 Python 中只通过显式安装取得 `playwright==1.62.0`，matching bundled
   Chromium 由操作员预装，P2 synthetic real-Chromium 纵向链、清理与无残留通过；
9. 候选 wheel 在真实 GitHub exact-main 坐标上完成 P1 -> P2 -> P3 正向链，Core 得到预封存 Plan 的
   `PASS`；该事实不重写 P3 历史，也不证明 GitHub 之外的现实真相；
10. tag ruleset 已按第 4 节生效，候选 tag 与 Release 均不存在，Core `v0.12.2` 仍为 Latest；
11. 固定资产集合、摘要、文档和验证产物通过路径、秘密、残留与范围检查。

构建验证使用仓库外临时目录；失败产物不得提交。16 GiB Windows 主机默认串行，浏览器与 clean venv
在每个矩阵单元后清理，不用并行换取速度。

## 8. 固定发布顺序

P4 的顺序固定为：

```text
P4 docs-only contract candidate
    -> original required checks
    -> protected-main merge
    -> exact-main anonymous contract readback
    -> independent contract freeze publication

release-preparation candidate
    -> local matrix
    -> PR original required checks
    -> protected-main merge
    -> exact-main Public CI + Browser Smoke

active github-evidence-v* tag protection
    -> rebuild final bytes from exact main
    -> final local asset matrix
    -> create and push annotated tag
    -> create non-Latest draft Release
    -> upload exact fixed assets
    -> authenticated metadata/digest/asset-set check
    -> publish as non-draft, non-prerelease, non-Latest
    -> anonymous Release page and asset download readback
    -> downloaded-asset clean-install/runtime matrix
    -> docs-only release facts and final state publication
    -> its own gates, merge and exact-main public readback
    -> P4_FROZEN
```

Release 创建与发布必须显式使用 non-Latest 语义；发布前后均通过 GitHub `releases/latest` 读回
`v0.12.2`。插件 Release 不能取代 Core Latest，也不能通过 prerelease 标志伪装这一边界。

上述顺序是带前置条件和历史坐标的状态迁移，不是若干成功检查的加总。每一步只能消费已经记录且
仍然成立的前序状态；后继成功不能补写被跳过的前置事实，也不能覆盖先前失败。需要恢复时，只能从
第 9 节允许的当前状态继续，并保留原 attempt 的因果记录。

Release operator 使用的 GitHub 写权限只服务于 ruleset、annotated tag 与 Release 发布；它不进入插件
runtime，不写入 Evidence，也不改变 GitHub Evidence Plugin 的只读产品权限。

## 9. Draft、失败与恢复语义

发布链必须按失败发生的位置处理：

| 失败位置 | 状态 | 允许动作 | 禁止动作 |
| --- | --- | --- | --- |
| tag 之前 | `RELEASE_NOT_STARTED / CANDIDATE_FAILED` | 保留失败事实，修正后从新 exact main 重建 | 创建 tag、用旧绿灯发布 |
| tag 已推、Release 未公开 | `TAGGED / RELEASE_PENDING` | 若源码和 candidate bytes 均未改变，可从相同 tag/bytes 恢复 draft/upload；记录每次 attempt | 移动 tag、用新源码覆盖同版本 |
| draft 资产或 metadata 错误 | `DRAFT_FAILED` | 记录 Release ID/原因；只有相同 source 与已验证 bytes 可重试传输 | 把不同 bytes 冒充同一候选 |
| Release 已公开但读回失败 | `RELEASE_FAILED / NOT_FROZEN` | 在 Release 正文显式标记问题；修复使用新 patch version/tag | 静默替换/删除公开资产、移动/重建 tag、宣布 P4 完成 |
| Latest 被改变 | `RELEASE_FAILED / LATEST_DRIFT` | 立即停止冻结并恢复 Core Latest 展示；保留漂移事实 | 把插件当作 Core Latest |

若 public asset 曾对匿名用户可见，就不能通过删除后重传同名文件来制造“从未失败”。GitHub Release
正文可以追加纠错/指向后继版本，但 tag、已公开资产和历史失败不得被静默重写。

## 10. 匿名公共读回

发布后必须在不提供 GitHub token、Authorization、登录 Cookie 或本地构建目录的环境中读取：

- tag ref、annotated tag object、peeled commit 与 tag ruleset；
- Release ID、name、tag、draft/prerelease/immutable 状态与公开 URL；
- 精确上传资产集合、asset ID、content type、size 与 GitHub `sha256:` digest；
- Core Latest 仍为 `v0.12.2`；
- 每个资产 requested URL、final URL、HTTP 200、下载 size 与 SHA-256；
- 下载后的 checksum manifest 对前三个 payload 的独立复算；
- 下载 wheel/sdist 的双 Python clean install、base/render 分层、真实 P1 -> P2 -> P3 正向链；
- 插件卸载后 Core 对保留 Evidence/AcceptanceBundle 的独立读取与复算；
- Release 页面、README、插件 README、本文和最终事实文档的公开渲染与版本口径。

GitHub API 与公开页面/下载仍属于同一平台信任域；两者的结果分别保留，但不能描述为独立第三方见证。
匿名下载成功也只证明观察时刻该 URL 返回了对应 bytes，不证明封存前输入真实或未来永不变化。

## 11. 范围外

P4 明确不包含：

- PyPI 发布、自动更新器、安装器、Homebrew、容器镜像或浏览器二进制分发；
- GitHub Enterprise、私有仓库、登录态浏览器、GraphQL、webhook 或定时监控；
- Core `0.12.x`、Starter、Authoring Skill、M/P 历史 tag 或 Release 的移动与重制；
- P1/P2 Collector、P3 handoff、Schema、Evidence、Assertion 或 Verdict 的新语义；
- Review Attention R1、Pattern Corpus 选择、审查 Provider 或 HumanDisposition；
- GitHub 之外的真实性锚、签名身份、可信时间戳或 Codex Security 深扫。

## 12. P4 停止线与出口

任一条件成立时立即停止：

- candidate source 不是新的 exact protected main，或工作树/构建输出混入未声明内容；
- `github-evidence-v0.1.0` 已存在、tag protection 未生效或 tag peeling 不指向 candidate commit；
- version、METADATA、dependency、optional extra 或固定资产集合不一致；
- 任一 required gate、clean install、real Chromium、real GitHub、卸载或清理门失败；
- Release 不是 non-draft/non-prerelease/non-Latest，或 Core Latest 漂移；
- GitHub asset digest、checksum manifest、本地 candidate 与匿名下载副本不一致；
- 出现新的产品语义反例，需要改变 P1–P3 合同或实现。

P4 只有在受保护 tag、独立 Release、四项资产、匿名下载、双 Python、base/render、真实纵向链、
Core-only 卸载复算、公共展示与最终 docs-only 状态发布全部闭合后，才能标记：

```text
P4_FROZEN
GITHUB_EVIDENCE_PLUGIN_0.1.0_RELEASED
PUBLIC_DOWNLOAD_READBACK_PASS
```

该出口只解除 R1 的“等待 P4”一半阻断。Review Attention R1 仍必须等待 Pattern Ledger 选出
`exact commit + corpus manifest digest + pattern_id/selected_record_digest` 的精确 Corpus 并独立冻结；
P4 不得顺手完成该工作。

## 13. 本合同候选自身的冻结门

本文当前只是一份 docs-only 候选，不授权立即创建 ruleset、tag、draft Release 或上传资产。它必须先：

1. 原始 Public CI 11 个 job 全部成功，且 branch ruleset 声明的 7 项 required checks 全部满足；
2. 合入受保护 `main`；
3. fetch 并确认新的 exact main、tree 与 merge parents；
4. 由产品 P1/P2 Collector 在 fresh anonymous Chromium 中读回 README 与本文；
5. 保留 requested/final coordinate、coverage、三样本、cleanup 与 Core Verdict；
6. 通过独立 docs-only freeze publication 把状态推进为
   `P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`。

在这条链完整成立前，P4 的下一项工作只能修订合同，不能进入发布实现。
