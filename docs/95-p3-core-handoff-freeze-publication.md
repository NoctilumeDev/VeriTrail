# P3 Core Handoff 最终冻结状态发布

> 状态发布目标：`P3_FROZEN / P4_NOT_STARTED`
>
> 冻结候选基线：`ec5ac70dcfa72b1b9859602af62cc3c9344389de`
>
> 候选事实：[文档 94](94-p3-core-handoff-implementation-freeze-candidate.md)
>
> 影响层级：`L1_DOCUMENTATION`；不修改 Core、Plugin、Schema、Evaluator、P1/P2 Evidence 或 Verdict

## 1. 发布裁决

P3 A–E 的实现、synthetic four-verdict lab、wheel/uninstall、真实 GitHub PASS/FAIL、受保护主线实现合入
与实现后产品读回已经由文档 94 固定。后继 docs-only 候选又独立完成原始 11 项远端门禁、主线合入，
并从新的 exact main 使用产品 P1/P2 Collector 对 README 与文档 94 完成匿名读回。

本文只发布这一已闭合事实，不增加实现。本文自身仍须经过原始远端门禁、受保护主线合入和合入后匿名
产品读回；只有该链全部成立，`P3_FROZEN` 才成为当前主线事实。任何新反例仍可否决发布，P4 与 Review
Attention R1 在此之前都不得启动。

## 2. 冻结候选 closure

1. docs-only 候选提交 `f9f85693b879643b038a9fc29f8c331d2119671b` 只修改文档、索引和 append-only
   `RA-021 rev1`；
2. [PR #65](https://github.com/NoctilumeDev/VeriTrail/pull/65) 的
   [Public CI run 34059620615](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34059620615)
   在原始 attempt 1 上生成 11 个 job，全部 `COMPLETED / SUCCESS`，没有 rerun；
3. PR #65 以 merge commit `ec5ac70dcfa72b1b9859602af62cc3c9344389de` 合入受保护 `main`；
4. 合入后精确读回 `origin/main` 为同一 SHA，tree 为
   `8f316b2131994db79635b2d35ce76871080ab88d`，merge parents 为实现主线
   `c0bce6cb7a3c9f3684d1845beda355084f232d0a` 与候选
   `f9f85693b879643b038a9fc29f8c331d2119671b`。

这条 closure 只证明候选经过了自己的门禁和交付链；它不拿 PR #64 的旧绿灯替代 #65，也不把 GitHub
API、Git commit 存在性或本地 Markdown 文件替代公开渲染。

## 3. exact-main 匿名产品读回

从 `main@ec5ac70dcfa72b1b9859602af62cc3c9344389de`，在未提供 GitHub token 的 fresh anonymous
Chromium 中固定执行 `github-api -> github-public-render`，分别读取两个不可变 Markdown 坐标。两次
观察使用独立 sealed Plan 和独立 paired session：

| 页面 | Plan digest | Handoff digest | Evidence SHA-256（API / Render） | Marker | Core report | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| exact README | `101f280635557025306c3e868f063bdacff696dbb577223780e2786680be4399` | `c599d73585abebddff6943e68431770577e07c317230a842e68b4757e373d9e9` | `b33a1965788a243db7eac1d5e0706d1d5b0dfb34aec1db32362e4eb6e13b751d` / `ab2837ab28c025a5fd428cee6ff5642562bec9910ed4e6c3f00ebd228ad5449b` | `VeriTrail` 23 次 | `0a113ed450c9b6cd3661c518a1f2cf41713f671d54ad0484c7ef2a0f9da529c3` | `PASS` |
| exact 文档 94 | `e3e3d6e9d3ca2dda0b43727a3e7f3ee062f87817835cb23606bd0a2ce7057cfc` | `9fd61eef4204c1101d2cd92c6757fb9f76dd7d7a8a8165851c69c01a3e6b5638` | `45d2d4b3b6ca8a8db04470ee3492cd93adc2db02265a8783cab686f259cceb9d` / `303716ae79dbbee122bb532878fa5e1b27b7e80880e5cc4f6c54def9e63a71c0` | `P3_IMPLEMENTED` 1 次 | `3fe2856eb2eb605814b3f28d995e7f666866703a83b9b924a06e4c4a9e758c03` | `PASS` |

两条链的 P1/P2 Evidence 均为 `PUBLISHED / COMPLETE`，requested URL、repository path 与 exact target SHA
未漂移，P1/P2 request seal 保持不同，同一 pair 内 session 一致，Render 仍明确
`atomic_snapshot_claimed=false`。规范 summary SHA-256 为
`c05e495f174e9549f7caa878a576f3ddff2616fe0ab367b1749645fc5b7d1f02`；取证 Artifact 保留在仓库外。

两份 Render Evidence 的三个 sample digest 各自完全相同，`samples_stable=true`，结束时
`active_streams=0`，`errors / facts.conflicts / cleanup_errors / coverage_reasons` 均为空。只读策略分别阻断
两个 telemetry 写请求，并以 `METHOD_NOT_ALLOWED / BlockedByClient` 保留 observer effect；它们不影响
coverage，也没有被解释成 GitHub 页面故障。

## 4. 不进入裁决的失联产物

第一次读回被外层执行器错误设置的 10 秒上限终止，控制通道没有返回 Collector completion 或 Verdict。
外层退出以后，临时目录中虽出现了完整文件，但此时已经失去“哪个进程在何种控制边界内完成”的连续
provenance，因此这些产物不进入冻结裁决，也不被事后解释成一次成功。

确认没有相关活进程后，读回使用新的输出根、Plan、request、session、Evidence 与 Handoff 从头执行；
第 3 节只记录这次 fresh observation。由此保持：

```text
Artifact appeared after control loss
    !=
Observed successful execution
```

## 5. 冻结后的边界

P3 冻结只确认：

- 极薄 manifest 只绑定 role/path/digest，不复制 Plan/session/facts/coverage/Verdict；
- 一次安全导入形成的同一 `ImportedEvidence` 快照同时被验证和交给 Core；
- 四态 synthetic lab 与真实 GitHub 单变量 PASS/FAIL 均由现有 Core 裁决；
- base wheel、render extra、plugin uninstall 与 Core-only 复算边界成立；
- API 与公开页面只是同一 GitHub 信任域的两个串行观察面，不是平台原子快照或外部真相锚点。

它不确认 P4 版本、tag、Release、下载坐标或长期兼容承诺，也不冻结 Review Attention Pattern Corpus。
`RA-021` 仍只是开放 Ledger revision；R1 继续受 `P4_AND_CORPUS_FREEZE` 阻断。

## 6. 本状态发布的最后门

本补丁只允许文档与索引变化，并必须独立完成：

1. 原始远端 11 项 required checks 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 parents；
4. 从该 exact main 用产品 P1/P2 Collector、fresh anonymous Chromium 读取 README 与本文；
5. 两个页面均须 `PUBLISHED / COMPLETE`，URL 与 SHA 不漂移，三样本稳定，指定 marker 存在，Core 为
   `PASS`，且没有额外 error/conflict/cleanup error。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
P1_FROZEN
P2_FROZEN
P3_FROZEN
P4_NOT_STARTED
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```
