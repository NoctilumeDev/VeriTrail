# P4 GitHub Evidence Plugin 独立发布合同冻结事实

> 后继事实：本页只证明当时的合同冻结过程，不证明其 `veritrail==0.12.2` 依赖可由公开资产满足。
> final exact-main clean install 的反例与停止线见
> [文档 100](100-core-v0.13.0-acceptance-api-release-contract.md)；P4 当前为 `BLOCKED`。

> 状态发布目标：`P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`
>
> 合同冻结候选基线：`main@eb4dcb60230a516503bf80ce26e13b25cd9b9d97`
>
> 精确合同：[文档 96](96-p4-github-evidence-release-contract.md)
>
> 影响层级：`L1_DOCUMENTATION`；不修改 Core、Plugin、Schema、Collector、Handoff、Verdict、
> tag ruleset、tag、Release 或公开资产

## 1. 冻结裁决

P4 合同已把 source、distribution、asset、tag/Release 与 public-download observation 五类身份分开，
并固定 `0.1.0` 版本、四项上传资产、base/render 安装边界、受保护 annotated tag、non-Latest Release、
匿名下载与失败恢复顺序。冻结前的身份核账又消除了 validation summary 对自身摘要的隐式要求，形成：

```text
wheel + sdist
    -> validation summary
    -> SHA256SUMS (wheel + sdist + summary)
    -> external release facts bind all four asset digests
```

本文只发布合同已经完成设计门禁的事实，不创建发布物。本文自身仍须经过原始远端门禁、受保护主线
合入和合入后 exact-main 匿名产品读回；只有该链全部成立，合同冻结状态才成为当前主线事实。任何新
反例仍可否决冻结，发布实现不得提前消费候选状态。

## 2. 候选、反例与最小修正

1. PR #68 的原始门禁暴露既有 M11 CLI 聚合 `ERROR`，因此停止且未合入；后继成功不覆盖这次失败；
2. PR #69 只增加分层失败诊断，以原始 11/11 门禁合入
   `main@f30647577e6de68c4d40a96f4f9b223fb24140bb`，没有把未复现解释为已知根因；
3. docs-only 候选提交 `ba5b384a8690b06b9236cc627b690ba7ca094a3b` 经
   [PR #70](https://github.com/NoctilumeDev/VeriTrail/pull/70) 的
   [Public CI run 34224420554](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34224420554)
   在原始 attempt 1 上取得 11/11 `SUCCESS`，随后合入
   `main@f27507c3735a68134fa428344f63265601c93715`；
4. 合入后的冻结前核账发现 validation summary 若被要求记录“每个 payload”的摘要，就必须声明自身
   摘要；该自指无法由有限 JSON 产物兑现，因此合同保持候选，且没有创建 tag ruleset、tag、Release
   或资产；
5. 最小非自指修正提交 `35206c8feb6e84c93dc73cf50d048440eff7e8ff` 经
   [PR #71](https://github.com/NoctilumeDev/VeriTrail/pull/71) 的
   [Public CI run 34229473365](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34229473365)
   在原始 attempt 1 上取得 11/11 `SUCCESS`，并合入本次冻结候选主线；
6. 精确 `origin/main` 读回为 `eb4dcb60230a516503bf80ce26e13b25cd9b9d97`，tree 为
   `0829c6ad561032acd0afc3e50e04993dd525e6d5`，merge parents 为
   `f27507c3735a68134fa428344f63265601c93715` 与
   `35206c8feb6e84c93dc73cf50d048440eff7e8ff`；
7. 该 exact main 的
   [Public CI run 34230665610](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34230665610)
   在 attempt 1 上取得 11/11 `SUCCESS`，同一 SHA 的
   [Browser Smoke run 34230665518](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34230665518)
   取得 1/1 `SUCCESS`；
8. 首次状态发布候选提交 `5120841fc824496e3c2af51f6626388cf195285e` 在
   [PR #72](https://github.com/NoctilumeDev/VeriTrail/pull/72) 的原始
   [Public CI run 34241218820](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34241218820)
   attempt 1 上停止：Python 3.10 job 下载既有
   `authoring-skill-v0.1.0/SHA256SUMS-authoring-skill.txt` 时，GitHub Release 连续四次返回
   HTTP 500；同一工作流的 Python 3.13 job 完成了同一下载步骤。后续匿名本机读取
   得到 `302 -> 200`、205 字节，SHA-256 为
   `20684909030aa104cb3faadcb1707edcefa16be2b2832808ccd887996a8debfb`，与冻结值一致。
   该事实只把异常分类为原始门禁中的外部下载失败，不证明仓库缺陷或单一网络根因；
   PR #72 因此未合入、未 rerun，并已关闭。

这条历史把“候选门禁通过”和“合同语义完整”保持为两类事实。PR #70 的绿灯没有阻止后继反例否决
冻结；PR #71 也只修正摘要生成顺序，没有扩张 P1–P3 或 Core 语义。PR #72 的外部下载失败同样
不被后继读回洗掉，但也不被外推成未经证明的产品或代理故障。

## 3. exact-main 匿名产品读回

从 `main@eb4dcb60230a516503bf80ce26e13b25cd9b9d97` 的 clean detached worktree，在未提供
`GITHUB_TOKEN`、`GH_TOKEN` 或 `VERITRAIL_GITHUB_TOKEN` 的环境中，固定执行
`github-api -> github-public-render`。README 使用 `DESKTOP_1365X768`，文档 96 使用
`NARROW_390X844`；两页分别使用独立 sealed Plan 和独立 paired session。

| 页面 | Plan digest | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report canonical digest | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| exact README | `d03b035c389a4e09f0a8a6bf2c478841f8c354e8f534c936b68f1129ebfd0add` | `github-paired-ebb32b886b414a648b9e45f868b93b8d` | `2c04b4c6a3382ef7187018e707f5d93f8e7d90080b90e1e67a9f5dfb6fc22a46` | `57bc647ee806155eda0d6e89196bccb0986ef4c7c2779de2eb9bfc58ef583c5b` / `c591b6c10bf3532bc1e291ebe2612ec87546437472f1a17de22a01f6d00fcdad` | `6dae7ac2a55f294ff2440367173fe3e0257a1ca60f4edc56eacdcdc8ef9d1582` | `PASS` |
| exact 文档 96 | `536509a2c2f2d38f88b234b7b3af3b62cee48429c3694b9c654b0be926d34655` | `github-paired-0ddceb54e6ef4e698d4b6c1ccb4cdb1e` | `0cc1a4f029f46970d48a1e832a2eedc56cf57d969088e1acbe86aafaea27547d` | `9429ea27955ff1733461ee505fec21e6ddd1a083af62be849231213ecf318b67` / `392ce573d23f78f95d627ce2aa65df310b5f91a5b8bcef0b34cd9b13c9208af0` | `66f1a3d390a41100c77225c99f82032407ede92b48a09b962a0bed90c9cf72d8` | `PASS` |

两条链均满足：

- P1/P2 产物均为 `PUBLISHED / COMPLETE`；
- P1 精确读回的 commit SHA 与候选主线一致；
- requested URL 与 final URL 均保持相同 GitHub exact-SHA Markdown 坐标，无 redirect coordinate 漂移；
- 同一 pair 内 collection session 一致，P1/P2 request seal 保持不同；
- README marker `P4_CONTRACT_0.1_CANDIDATE` 与文档 marker
  `P4 GitHub Evidence Plugin 独立发布合同 0.1` 均出现 1 次；
- 两页各自三个 sample digest 完全相同，`samples_stable=true`；
- 结束时 `active_streams=0`，`errors / facts.conflicts / cleanup_errors / coverage_reasons` 均为空；
- Core 只消费 handoff 指定的同一 imported Evidence snapshot，并分别得到 `PASS`。

本轮规范 summary canonical digest 为
`ffb2ca6a4821ff7efef7cf6cccad2b95d647860e8e0659863710db873699246d`；全部运行产物留在仓库外，
不把本机路径、浏览器数据或临时 Evidence 提交为产品事实。

## 4. 不进入冻结裁决的旧读回

在旧候选 `main@f27507c3735a68134fa428344f63265601c93715` 上，第一次 paired 读回遇到匿名 GitHub API
配额耗尽：P1 repository probe 为 `NETWORK_ERROR / ERROR`，同次 README P2 Render 虽为
`COMPLETE`，仍不足以形成 paired Core `PASS`。另一条只读文档 96 的窄屏预检已发布 Render
Evidence，但 response-body controller 报告 `PublicRenderNetworkError`，coverage 为 `ERROR`；稳定 DOM、
marker 和干净 cleanup 不能替代网络观察完整性。

这两次产物继续保留在仓库外，但不进入第 3 节裁决。后继更换网络出口后，从新的 exact main、新 Plan、
新 request、新 session 和新输出根重新执行并通过；该成功只证明新一轮闭环成立，不把旧异常追认成
单一、已证明的代理根因，也不擦除旧失败。

## 5. 冻结边界

合同冻结只确认：

- P4 的版本、身份、资产、保护、发布、下载和失败恢复规则已经形成可执行施工边界；
- validation summary、checksum manifest 与发布事实之间不存在摘要自指；
- P4 发布实现必须从本状态发布闭环后的新 exact main 重建，不能复用当前读回产物或旧候选字节；
- `github-evidence-v*` tag protection 必须先于首个 tag，插件 Release 必须保持 non-Latest；
- Core `v0.12.2`、历史 M/E/P 标签与既有 Release 继续只读；
- R1 仍须等待 P4 最终冻结与 Pattern Corpus 的精确选择和冻结。

它不确认 tag ruleset、`github-evidence-v0.1.0`、Release、四项资产或匿名下载已经存在，也不确认
插件已发布。GitHub 之外的真实性锚、可信时间戳和 Codex Security 深扫仍在范围外。

## 6. 本状态发布的最后门

本补丁只允许文档与索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 用产品 P1/P2 Collector、fresh anonymous Chromium 读取 README 与本文；
5. 两个页面均须 `PUBLISHED / COMPLETE`，URL 与 SHA 不漂移，三样本稳定，指定 marker 存在，Core 为
   `PASS`，且没有额外 error/conflict/cleanup error。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
P1_FROZEN
P2_FROZEN
P3_FROZEN
P4_CONTRACT_0.1_FROZEN
P4_RELEASE_NOT_STARTED
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```
