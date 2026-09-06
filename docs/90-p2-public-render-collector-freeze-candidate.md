# P2 Public Render Collector 实现与冻结事实 0.1

> 状态：`P2_FROZEN / P3_NOT_STARTED`
>
> 精确实现基线：`cacb08539a9c2835320410ade03e68502ca5de6c`
>
> 完整实现候选：`3b1f2703ee3b70d23146c592bc4af2ca7a058a72`
>
> 受保护主线实现基线：`ca6b8aaa33bc06795c96610b9e9085506efef9a0`
>
> 主线 Tree：`4c45191a6fac4f4848883be94d0c646076716e56`
>
> 冻结闭环主线：`2d3877df41d7ec5a3b7b932404f6b622f06862a8`
>
> 本文影响层级：`L0_DOCUMENTATION_ONLY`；只记录已发生的 P2 实现与验收事实，不修改运行代码

## 1. 当前裁决

P2 已完成合同内的 Public Render Collector 实现，并形成从 sealed `AcceptancePlan` 到 fresh anonymous
Chromium、固定公开作用域、三样本内容观察、标准 `Evidence 0.1` 以及 P1 API → P2 Render 同会话串行
协调的可运行纵向切片。Collector 只保存它实际观察到的事实；Evidence 的充分性、跨 Evidence 关系、
assertion 与最终 Verdict 仍由 Core 拥有。

实现 PR、公共门禁、受保护主线合入、exact-main 真实读回，以及独立 docs-only closure 自身的 11 项
门禁、主线合入和合入后匿名公开读回均已完成，因此 P2 在本文边界内冻结为 `P2_FROZEN`。任何后继
反例仍可显式重开受影响边界；冻结不会把既有绿灯升级为对未知现实的永久保证。

## 2. 实现边界

P2 代码只增加在独立 `plugins/github-evidence` 包内，并按职责拆成：

```text
structured request / coordinates / URL
    -> runtime preflight
    -> fresh anonymous BrowserContext
    -> navigation and read-only route policy
    -> response-body budget controller
    -> fixed content scope and three-sample observation
    -> normalized facts and Evidence assembly
    -> optional P1 API -> P2 Render coordinator
```

`public_render_contracts.py` 只负责请求校验、规范身份与 URL 派生，不拥有浏览器、网络、DOM 或 Evidence
职责。P1 与 P2 不共享私有 validator 实现；两者消费同一份数据型 GitHub coordinate conformance corpus，
以“共享事实向量，不共享实现”限制语义漂移和跨层耦合。

Playwright 只位于插件的 `render` optional extra。基础 wheel 不安装、不导入 Playwright，P1 Collector 与
CLI 继续独立可用；P2 也不自动下载浏览器，只接受锁定 `playwright==1.62.0` 所匹配且已经存在的
Chromium。内部 `route.fulfill(...)` synthetic seam 只能由测试子类使用，request、CLI 和外部调用者均
不能选择它；生产默认仍为只读 `route.continue_()`。

## 3. 合同内能力

实现已覆盖：

- repository Markdown、exact commit Markdown、Release Markdown 与默认 GitHub Pages 的唯一 HTTPS
  坐标派生，包括 `pages_path = ""` 的站点根表示；
- fresh、匿名、non-persistent context，固定 viewport、同源 redirect、GET/HEAD-only 与写请求阻断；
- 主文档 `8 MiB`、全页 `32 MiB` response-body 硬预算、45 秒生命周期、512 请求和零重试；
- response-stage Fetch stream 的 producer-side 中断、受控响应回放、policy block 与外部失败分离；
- 固定 DOM scope、一次求值形成一个 sample、三次规范化结果全等、末次 health barrier；
- rendered text、heading、link、literal marker 与 initial-viewport 投影，以及版本化 `facts_digest`；
- `COMPLETE / PARTIAL / ERROR` coverage、conflict、provenance、原子 Evidence 发布与失败清理；
- P1 API → P2 Render 的固定串行协调、同一 plugin-created session 和两份独立 request/Evidence 身份。

浏览器导航 200、DOM 可见、三样本稳定、异步采集健康与页面事实完整仍是不同命题。Synthetic 页面只
证明机制；GitHub API 与公开页面仍是同一平台的两个观察面，不是两个独立权威，也不是平台原子快照。

## 4. 本地串行证据

所有门禁均从实现候选的同一 worktree 绑定 Core、插件源码和测试目录后串行执行；未把其他 editable
checkout 的导入结果计入证据。

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| GitHub Evidence 插件普通 / `-O` | `162/162` / `162/162` | `162/162` / `162/162` |
| Core 普通 / `-O` | `385/385` / `385/385` | `385/385` / `385/385` |
| Starter 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring Skill 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring 两条真实 DRAFT 链 | `PASS / PASS` | `PASS / PASS` |
| Core wheel-only | `PASS` | `PASS` |
| PC2 wheel-only | `PASS` | `PASS` |
| GitHub Evidence wheel-only | `PASS` | `PASS` |
| E3 公共冻结资产读回 | `PASS` | `PASS` |

Authoring 输出继续保持 `NOT_SEALED / NOT_RUN / NO_VERDICT`。Workbench 完成 `173/173`、零警告 lint、
type-check、生产 build 与 moderate 级依赖审计零漏洞；Starter PASS/FAIL golden path、桌面/移动 Workbench、
Console/network 与端口/SQLite/staging 清理均通过。

GitHub Evidence wheel-only 门从空 venv 与无 checkout 工作区安装 Core wheel 和插件 wheel，分别证明：

1. base wheel 中没有 Playwright，P1 import、Collector 与 CLI 正常；
2. 显式安装 `render` 依赖并预置 matching Chromium 后，P2 从 `site-packages` 完成 preflight；
3. 卸载 GitHub 插件后，Core 仍能独立读取 P1/P2 标准 Evidence。

真实 Chromium synthetic 纵向门不是组件拼接假设，而是完整运行 request → browser → route policy →
body budget → DOM scope → three samples → Evidence → cleanup；它在双 Python、普通/`-O` 四条路径均
通过。HTTP 404/500 仍保留为 `COMPLETE` 导航事实；无响应路径 fail closed 为 `ERROR`；popup/download
被主动阻止并保留 conflict。事实摘要还分别证明 viewport profile 与 normalization semantic version 的
变化会改变 `facts_digest`。

## 5. 远端门禁与受保护主线

1. 完整实现候选 `3b1f2703ee3b70d23146c592bc4af2ca7a058a72` 从精确
   `main@cacb08539a9c2835320410ade03e68502ca5de6c` 起步；
2. [PR #49](https://github.com/NoctilumeDev/VeriTrail/pull/49) 的
   [Public CI run 34032911537](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34032911537)
   共 11 个 job，全部 `COMPLETED / SUCCESS`，没有以局部测试替代公共门禁；
3. PR #49 以 merge commit `ca6b8aaa33bc06795c96610b9e9085506efef9a0` 合入受保护 `main`；
4. 合入后 `origin/main` 精确读回同一 SHA，tree 为
   `4c45191a6fac4f4848883be94d0c646076716e56`，merge parents 为旧主线
   `cacb08539a9c2835320410ade03e68502ca5de6c` 与候选
   `3b1f2703ee3b70d23146c592bc4af2ca7a058a72`。

## 6. Exact-main 真实 GitHub Render 读回

从 `main@ca6b8aaa33bc06795c96610b9e9085506efef9a0` 建立无分支、无本地修改的 exact-main checkout，使用
产品 `PublicRenderCollector`、锁定 Playwright 1.62.0 与 matching Chromium，对 exact commit README
分别执行 desktop 与 narrow 两次串行观察。每次都建立独立 sealed Plan、request 和 collection session；
没有把两次观察冒充原子配对，也没有把取证 Evidence 写入仓库。

两次观察共同得到：

- coverage `COMPLETE`、主文档 HTTP 200；
- requested/final path 均为 exact commit README，坐标未漂移；
- 固定 scope 恰好 1 个，三样本全等且末次 health barrier 通过；
- headings 19、links 151、字面 `VeriTrail` 命中 23；
- coverage conflicts 0、结束时 active body streams 0、cleanup errors 为空。

desktop 观察到 150 个请求和 `7,624,936` response-body bytes；narrow 观察到 149 个请求和
`7,623,809` bytes。差异保留为两个实际观察，不被抹平成“相同网络世界”。两次 context 均在关闭后
没有遗留项目拥有的 Playwright/Chromium 进程。

## 7. 范围外与后继停止线

本候选没有进入：

- P3 正式 Core handoff、AcceptanceBundle、完整 PASS/FAIL/INCONCLUSIVE/PENDING 正负链；
- P4 插件版本、标签、Release、下载读回或稳定安装坐标；
- 登录态/私有仓库、GitHub Enterprise、custom Pages domain、任意脚本执行或远端写操作；
- Review Attention R1、Pattern Corpus 冻结或自动 HumanDisposition；
- GitHub 之外的真实性锚点、Codex Security 深扫或“已经证明安全/真实”的声明。

P2 冻结只解除 P3 的阶段阻断，不自动启动 P3。后继仍须严格串行：

```text
P2_FROZEN
    -> 从新的 exact main 单独定义 P3 合同与验收矩阵
    -> 合同冻结后才可实现正式 Core handoff
    -> P3 完整正负 Verdict 链冻结后才可进入 P4
```

P3、P4 与 Review Attention R1 当前仍未开始。不得把 P2 的配对 coordinator、标准 Evidence 或
synthetic 纵向门冒充 P3 的正式 AcceptanceBundle/Verdict 闭环。

## 8. Docs-only 冻结闭环事实

1. docs-only 候选 `55977b79f9c681cf81508c1c2ab61b8fc860f963` 从精确实现主线
   `ca6b8aaa33bc06795c96610b9e9085506efef9a0` 起步，只改 README、AGENTS、P 轨状态/索引与本文；
2. [PR #50](https://github.com/NoctilumeDev/VeriTrail/pull/50) 的
   [Public CI run 34034165712](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34034165712)
   原始 attempt 共 11 个 job，全部 `COMPLETED / SUCCESS`，没有 rerun；
3. PR #50 以 merge commit `2d3877df41d7ec5a3b7b932404f6b622f06862a8` 合入受保护 `main`；
   合入后 `origin/main` 精确读回同一 SHA，tree 为
   `6c5e7ddf5d9dd0fea8a8eb36aeda220c796a710c`，merge parents 为此前实现主线
   `ca6b8aaa33bc06795c96610b9e9085506efef9a0` 与候选
   `55977b79f9c681cf81508c1c2ab61b8fc860f963`；
4. 从该 exact main 使用产品 `PublicRenderCollector`、锁定 Playwright 1.62.0 与 matching Chromium，
   分别为 README 和本文建立 fresh anonymous desktop/narrow context；四次观察均返回 HTTP 200、
   requested/final path 相同、唯一 usable scope、三样本全等、coverage `COMPLETE`；
5. README 两个视口均观察到 19 个 heading 与 154 个 link；三样本摘要均为
   `7dbd0eee60018535ebf95e6b618498e607a0afc2bf9be6fd1e1260a9f2e0980b`，并实际命中
   `P2_IMPLEMENTED`、`FREEZE_CLOSURE_CANDIDATE` 与 `P3_NOT_STARTED`；desktop/narrow 分别记录
   150/149 个请求与 `7,628,534 / 7,627,358` response-body bytes；
6. 本文两个视口均观察到 8 个 heading 与 10 个 link，候选状态标记分别命中 2/2/3 次；desktop/narrow
   的三样本摘要分别为 `7be2398a17b21396ea45579fa97fa9c77121167aa8ca9a2f1835e13d3e40e881` 与
   `7b6f80cc42ab8854277a69880419347e25bc18eddf9043345a99d4a3dadaeced`，记录 141/140 个请求与
   `7,316,980 / 7,315,812` response-body bytes；
7. 四次观察的 policy-blocked writes 分别为 3/3/2/2，但影响 coverage 的网络冲突均为 0；body failure
   均为 `null`，结束时 active streams 为 0，cleanup errors 为空。视口间差异作为真实观察保留，没有
   被抹平成原子快照或相同网络世界。

P2 至此冻结。下一阶段若启动，只能从新的 exact main 另行定义并评审 P3；当前准确状态为
`P2_FROZEN / P3_NOT_STARTED`。
