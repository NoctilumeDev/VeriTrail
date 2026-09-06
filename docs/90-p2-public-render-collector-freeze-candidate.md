# P2 Public Render Collector 实现与冻结闭环候选事实 0.1

> 状态：`P2_IMPLEMENTED / FREEZE_CLOSURE_CANDIDATE / P3_NOT_STARTED`
>
> 精确实现基线：`cacb08539a9c2835320410ade03e68502ca5de6c`
>
> 完整实现候选：`3b1f2703ee3b70d23146c592bc4af2ca7a058a72`
>
> 受保护主线实现基线：`ca6b8aaa33bc06795c96610b9e9085506efef9a0`
>
> 主线 Tree：`4c45191a6fac4f4848883be94d0c646076716e56`
>
> 本文影响层级：`L0_DOCUMENTATION_ONLY`；只记录已发生的 P2 实现与验收事实，不修改运行代码

## 1. 当前裁决

P2 已完成合同内的 Public Render Collector 实现，并形成从 sealed `AcceptancePlan` 到 fresh anonymous
Chromium、固定公开作用域、三样本内容观察、标准 `Evidence 0.1` 以及 P1 API → P2 Render 同会话串行
协调的可运行纵向切片。Collector 只保存它实际观察到的事实；Evidence 的充分性、跨 Evidence 关系、
assertion 与最终 Verdict 仍由 Core 拥有。

当前还不是 `P2_FROZEN`。实现 PR、公共门禁、受保护主线合入和 exact-main 真实读回已经完成；本
docs-only 闭环候选仍须通过自己的完整门禁、受保护主线合入和合入后匿名公开读回。任何新反例都可以
否决冻结，既有 11/11、测试数量或真实浏览器成功不能覆盖新证据。

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

## 7. 范围外与冻结停止线

本候选没有进入：

- P3 正式 Core handoff、AcceptanceBundle、完整 PASS/FAIL/INCONCLUSIVE/PENDING 正负链；
- P4 插件版本、标签、Release、下载读回或稳定安装坐标；
- 登录态/私有仓库、GitHub Enterprise、custom Pages domain、任意脚本执行或远端写操作；
- Review Attention R1、Pattern Corpus 冻结或自动 HumanDisposition；
- GitHub 之外的真实性锚点、Codex Security 深扫或“已经证明安全/真实”的声明。

冻结剩余步骤严格串行：

```text
本文与状态索引形成 docs-only 候选
    -> 候选自己的 11 项 required checks
    -> 合入受保护 main
    -> 读回新的 exact origin/main SHA
    -> fresh anonymous Chromium 读回 README 与本文
    -> 最小状态事实补丁记录上述闭环
    -> P2_FROZEN / P3_NOT_STARTED
```

在最后一步成立前，准确状态始终是
`P2_IMPLEMENTED / FREEZE_CLOSURE_CANDIDATE / P3_NOT_STARTED`。全绿不是冻结资格；任何新反例拥有
否决权。
