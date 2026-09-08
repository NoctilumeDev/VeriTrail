# Core 0.13.0 Acceptance API 合同冻结事实

> 状态发布目标：`CORE_0.13.0_CONTRACT_FROZEN / C1_NOT_STARTED / P4_BLOCKED / NO_TAG / NO_RELEASE`
>
> 状态发布重建基线：`main@5b28ac3076ff4a08added47cbfc66c960c3dbdea`
>
> 本文只记录 [Core 0.13.0 发布补全合同](100-core-v0.13.0-acceptance-api-release-contract.md)已经发生的
> 候选、门禁与公开读回事实；本状态发布自己的原始门禁、受保护主线合入和合入后 exact-main 匿名读回
> 全部成立后，冻结状态才成为当前主线事实。

## 1. 冻结对象

本轮冻结的是 Core `0.13.0` 的发布施工边界，不是 Core 0.13.0 Release。它确认公开 `v0.12.2` wheel
与当前同版本源码 wheel 的 Acceptance API 能力不一致，且该新增公共能力必须通过新的 Core 版本发布。

冻结不会创建 `v0.13.0` tag、Release 或资产，也不修改 AcceptancePlan、四 Verdict、P1/P2 facts、
P3 handoff、历史 Release 或 GitHub Evidence 插件依赖。P4 继续停止；R1 继续等待 P4 与 Pattern Corpus
双冻结。

## 2. 候选与主线门禁

1. 合同候选提交 `2b173ce95791393e92f1f045b4304acbf693ee74` 只修改文档与索引；
2. PR [#77](https://github.com/NoctilumeDev/VeriTrail/pull/77) 的原始
   [Public CI run 34277939214](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34277939214)
   在 attempt 1 完成 11/11 success，没有 rerun；
3. PR #77 经受保护主线合入 merge commit
   `5b28ac3076ff4a08added47cbfc66c960c3dbdea`，tree 为
   `e101ed7c0c119eeeacd930378439c2ac348a73e3`；
4. 合入后的 [Public CI run 34279041454](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34279041454)
   在 exact head `5b28ac3076ff4a08added47cbfc66c960c3dbdea`、attempt 1 完成 11/11 success；
5. 同一 exact head 的
   [Browser Smoke run 34279041516](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34279041516)
   完成 1/1 success。

该链只证明候选与 exact main 门禁成立，不把 CI 构建 wheel 冒充公开 Core 0.13.0 资产。

## 3. exact-main 匿名产品读回

从 `main@5b28ac3076ff4a08added47cbfc66c960c3dbdea` 建立 clean detached worktree，独立构建并安装该
坐标内的 Core 与 GitHub Evidence Plugin。运行时未提供 `GITHUB_TOKEN`、`GH_TOKEN` 或
`VERITRAIL_GITHUB_TOKEN`，固定执行 `github-api -> github-public-render -> exact snapshot handoff -> Core`。
README 与合同正文使用两个独立 sealed Plan、request、session 与输出根。

| 页面 | Plan digest | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report digest | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| exact README | `2d80837a409582599da6cfa9e65d15c711c8a1fcb1c70668177cc60fe711b2a1` | `github-paired-e2083e83a0d14c58a3c7acf71645a38f` | `89d301a8674d5a862caa3bb0ad254dfac788159a7d0f798c79c53615926fadd7` | `3be3a83e333cbc9af27cafcb5ba112c2dbf8d35f065806229d3f661dbfb04c67` / `2ad29a992cdb597fe75c45e31f934c030ad8d62537b3ae1f085c47820a57b2e5` | `e0af98ef9c384ac6f6cfe8b877236ce1742c801e1c7b4d792604288fa62e454f` | `PASS` |
| exact 文档 100 | `fae161cbbbfb0c666127a01f8143526d3e358daa83b3a423a7a580e736656324` | `github-paired-485dff1642a14786814fc6bc2239714c` | `772f4df3d9a67f0fa6d09b922d058fa0bafee8afa25e0db69b192b255cb23811` | `986b9c3a282fa6a96d9b821c39ed73d42461da5a93d455b5f97d0b3dc1a3bbce` / `53997f34cc280faaf89f0be8f033bd4a75790e0a658ff61fdb3b1ae3609a37e3` | `aa8054928a6e3b3e74125be9952edd7f9f78d0ab7f4f80f62ddec08b5c78c782` | `PASS` |

两条链均确认：

- P1 与 P2 均为 `PUBLISHED / COMPLETE`，同一 pair 内 session 一致；
- API commit 与 Render source coordinate 均精确绑定 `5b28ac3076ff4a08added47cbfc66c960c3dbdea`；
- requested URL 与 final URL 保持同一个 GitHub exact-SHA Markdown 坐标，主文档 HTTP 200；
- 固定 Markdown 作用域 `observed_count=1 / usable=true`；
- 三个样本 digest 各自完全相同，`samples_stable=true`，无 truncation 或 conflict；
- README marker `Core 0.13.0 Acceptance API` 出现 2 次，文档 marker
  `PUBLICATION_IDENTITY_MISMATCH` 出现 1 次；
- Core 只消费 handoff 绑定的同一 imported Evidence snapshot，全部规则得到 `PASS`。

本轮生成物保留在仓库外。它们属于 C0 候选公开读回，不是 Core 0.13.0 或 GitHub Evidence 0.1.0
公开下载证据。

## 4. 外部坐标保持未创建

冻结候选读回时：

- `origin/main` 精确为 `5b28ac3076ff4a08added47cbfc66c960c3dbdea`；
- open PR 只有既有 Dependabot #16、#67，不属于 C0/P4 因果链；
- `v0.13.0*` 与 `github-evidence-v0.1.0*` tag 均不存在；
- Latest Release 仍为 Core `v0.12.2`；
- 既有 tag ruleset 只覆盖 `refs/tags/v*` 以及 `m* / starter-v* / authoring-skill-v*`，没有提前创建
  `github-evidence-v*` 保护规则；
- plugin validation summary 与 checksum 仍未生成。

## 5. 冻结边界与下一步

合同冻结只允许下一步从本状态发布闭环后的新 exact main 串行进入 C1：

```text
Core 0.13.0 release candidate
    -> version / release notes / public entry points
    -> 双 Python normal / -O 全回归
    -> wheel + sdist clean install
    -> four-verdict + imported-snapshot 纵向门
    -> Starter / Workbench / Browser Smoke 兼容回归
```

C1 不得新增 Acceptance 语义、改变 P1–P3、把 GitHub 语义倒灌 Core，或创建任何插件发布坐标。
Core 0.13.0 尚未公开发布，P4 仍为 `BLOCKED`。

## 6. 本状态发布的最后门

本补丁只允许文档与索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不用 rerun 覆盖失败；
2. 经受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 用产品 P1/P2 Collector、fresh anonymous Chromium 读取 README 与本文；
5. 两页均须 `PUBLISHED / COMPLETE`，URL 与 SHA 不漂移，三样本稳定，指定 marker 存在，Core 为
   `PASS`，并且没有额外 error、conflict 或 cleanup error。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
CORE_0.13.0_CONTRACT_FROZEN
C1_NOT_STARTED
P4_BLOCKED
NO_CORE_0.13.0_TAG_OR_RELEASE
NO_GITHUB_EVIDENCE_TAG_OR_RELEASE
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```
