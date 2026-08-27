# 从这里开始使用 VeriTrail

> 当前稳定内核：[`VeriTrail Core 0.12.2`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.2)
>
> Core `0.12.2` 只修复 demo Catalog 的最终位置绑定；受保护标签、五项 Release 资产、公开下载摘要、
> 双 Python wheel、sdist 和搬移负对照均已读回。边界与精确事实见
> [文档 74](docs/74-core-demo-catalog-binding-maintenance-contract.md)与
> [0.12.2 Release Notes](docs/75-v0.12.2-release-notes.md)，以及
> [0.12.2 发布与公开读回事实](docs/76-core-v0.12.2-release-readback-facts.md)。
>
> 当前稳定入口层：[`VeriTrail Starter 0.2.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0)
> 与 [`VeriTrail Authoring Skill 0.2.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0)。
> 两个带注释标签共同钉在提交 `c9592e1`；七个 GitHub 下载资产已通过 Python 3.10.6/3.13.13、
> 双 Preset、官方 Skill 结构校验和 DRAFT 逐字节等价门禁。历史 `0.1.0` Release 继续保留。

VeriTrail（验迹）不是“再点一次绿色测试按钮”。它把一次软件验收拆成预先冻结的计划、真实运行、
结构化证据、确定性裁决、不可变证据包和可比较的复跑结果。

最重要的区别是：

```text
程序能启动
  != 断言成立
  != 证据完整
  != 整个 Run 一定 PASS
```

## 选择入口

### 第一次认识 VeriTrail

先走[十分钟 PASS/FAIL 黄金路径](docs/61-starter-single-webapp-golden-path.md)。它包含一次明确的
`PASS` 和一次故意制造的 `FAIL`，让你看到同一份预注册标准如何保留成功与反例。两次 Run 使用
同一 Profile、同一 Plan，只改变一个受控业务事实；它们是独立验收对，不冒充因果 Comparison。

如果已经**克隆了本仓库**，并且只想先认识 Core 的 Plan、Evidence、Verdict 与 Bundle，可以运行
最小证据示例：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install `
  "https://github.com/NoctilumeDev/VeriTrail/releases/download/v0.12.2/veritrail-0.12.2-py3-none-any.whl"

.\.venv\Scripts\veritrail.exe seal `
  --plan examples\minimal\plan.json `
  --output artifacts\m0-sealed-plan.json

.\.venv\Scripts\veritrail.exe evaluate `
  --plan artifacts\m0-sealed-plan.json `
  --evidence examples\minimal\evidence-pass.json `
  --run-id my-first-run `
  --output artifacts\my-first-run
```

上面命令里的 `examples\minimal` 属于 Git 仓库，并不包含在 `v0.12.2` wheel 中。只下载 wheel、
没有 clone 仓库的用户，不能把这组命令当成自包含首跑。这个示例只解释 Plan、Evidence、Verdict
与 Bundle，不代表完整项目自举已经发生。

只安装 Core `0.12.2` wheel、没有 clone 仓库时，使用自包含首跑命令：

```powershell
.\.venv\Scripts\veritrail.exe demo --output artifacts\first-run-demo
```

它从同一份内置 sealed Plan 生成一个 `PASS` Bundle、一个故意制造的 `FAIL` Bundle，并建立只读
Catalog。输出始终带有 `SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE` 边界标记：它演示确定性 Core
链，不证明用户自己的项目，也不会探测启动命令、端口或验收标准。精确边界与门禁见
[Core 无 checkout 首跑维护合同](docs/71-core-first-run-maintenance-contract.md)；0.12.1 建立该入口的
历史事实见[0.12.1 Release Notes](docs/72-v0.12.1-release-notes.md)与
[0.12.1 发布读回事实](docs/73-core-v0.12.1-release-readback-facts.md)。0.12.2 保持同一合成边界并修复
最终位置绑定，见[维护合同](docs/74-core-demo-catalog-binding-maintenance-contract.md)、
[0.12.2 Release Notes](docs/75-v0.12.2-release-notes.md)和
[0.12.2 发布读回事实](docs/76-core-v0.12.2-release-readback-facts.md)。

### 已有一个本地 Web 项目

稳定发布的 Starter 0.2 支持两个有限预设：

- `single-webapp`：Windows 11、C1 进程冷状态、一个可信本地应用进程、固定回环端口、HTTP 就绪
  探针和必需的真实 Chromium 证据；
- `static-site`：显式 CPython console executable、现存普通 `.html/.htm`、固定回环地址、无需构建、
  无需远程资源和显式双视口检查。

它会询问并保存这些显式答案：

- 项目根目录；
- 可信可执行文件和参数数组；
- 工作目录；
- 固定回环端口与健康检查路径；
- 浏览器入口和允许的同源地址；
- 必须成立的业务事实；
- 资源预算和清理边界。

它只生成名称明确的 `*.draft.json`、本机 ToolBindings、答案快照和复核说明。生成物保持
`DRAFT / NOT SEALED`；用户完成复核后，才把它们交给 Core 的 `seal`、`bootstrap-preview` 和
`run`。

如果项目包含多个服务、Docker Compose、远程数据库、登录凭据、非回环网络、来源不明的既有进程、
构建型静态站点或无法确定的资源所有权，Starter 0.2 会返回 `UNSUPPORTED`，不会猜测一个“看起来能跑”
的方案。

### 静态站点入口

Starter/Authoring Skill 0.2 的 `static-site` 只接受现存普通 `.html/.htm`、显式
CPython console executable、固定回环地址、`requires_build = false` 与
`requires_remote_assets = false`。它不运行 npm、构建脚本、包管理器、Shell 或远程资源，也不封存、
不运行、不裁决。

它已经包含在稳定 0.2.0 下载入口中。合同、权限和双 Python clean-install 事实见
[Starter 0.2 合同](docs/66-starter-static-site-contract.md)、
[Authoring Skill 0.2 合同](docs/67-authoring-skill-0.2-contract.md)与
[E2 实现事实](docs/68-entry-layer-e2-static-site-facts.md)；公开资产与读回事实见
[E3 0.2.0 发布说明](docs/70-entry-layer-e3-0.2-release-notes.md)。

### 已经理解完整合同

高级用户可以直接使用 Core CLI 和冻结 Schema。请先阅读：

- [产品定义](docs/00-product-brief.md)
- [证据与实验模型](docs/01-evidence-model.md)
- [架构与安全边界](docs/02-architecture.md)
- [验收标准](docs/03-acceptance.md)
- [M10 有界完整项目自举合同](docs/15-m10-bounded-project-bootstrap.md)
- [M11 单应用真实项目合同](docs/23-m11-single-node-real-project-contract.md)

## 三条不会改变的规则

1. Starter 和 AI 都只能生成草案，不能自动封存合同。
2. 观察到失败后不能降低断言、改写停止线或删除反例。
3. Verdict 只由 VeriTrail Core 根据 sealed 合同和证据确定。

AI 可以帮助阅读仓库、推荐最接近的有限预设、解释字段和整理缺失信息。AI 不能充当裁决器。完整
权限边界见 [VeriTrail Authoring Skill 合同](docs/60-authoring-skill-contract.md)，已实现门禁与验收见
[A0 冻结事实](docs/62-authoring-skill-a0-facts.md)。独立发布坐标、资产集合和公开读回停止线见
[E1 发布合同](docs/63-entry-layer-e1-release-contract.md)与
[E1 0.1.0 发布说明](docs/64-entry-layer-e1-release-notes.md)。0.2 权限增量、不变停止线与公开读回另见
[Authoring Skill 0.2 合同](docs/67-authoring-skill-0.2-contract.md)和
[E3 0.2.0 发布说明](docs/70-entry-layer-e3-0.2-release-notes.md)。

## 当前支持边界

Core 0.12.2 继承 0.12.0 已冻结的 Windows 11、C1、本地受控进程、真实 Chromium、不可变 Bundle、Catalog、
Comparison、Paired Analysis 和 Batch Analysis。它没有证明通用项目探测、自动安装、C2/C3、Docker、
跨平台、多服务编排、恶意代码隔离或生产容量。

遇到边界外项目时，正确结果是 `NOT_PROVEN` 或 `UNSUPPORTED`，不是自动修环境后继续宣布通过。
