# 从这里开始使用 VeriTrail

> 当前稳定内核：`VeriTrail Core 0.12.0`
>
> 当前入口层状态：`VeriTrail Starter 0.1` 的 S0 确定性 DRAFT 链与 S1 真实 PASS/FAIL 黄金路径
> 以及 `VeriTrail Authoring Skill 0.1` 的 A0 DRAFT-only 包装已在源码中完成；独立发布仍未完成，
> 因此它们还不是开箱即用正式版。

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

在 Starter 发布前，可以先运行 Core 的最小证据示例：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install `
  "https://github.com/NoctilumeDev/VeriTrail/releases/download/v0.12.0/veritrail-0.12.0-py3-none-any.whl"

.\.venv\Scripts\veritrail.exe seal `
  --plan examples\minimal\plan.json `
  --output artifacts\m0-sealed-plan.json

.\.venv\Scripts\veritrail.exe evaluate `
  --plan artifacts\m0-sealed-plan.json `
  --evidence examples\minimal\evidence-pass.json `
  --run-id my-first-run `
  --output artifacts\my-first-run
```

这个示例只解释 Plan、Evidence、Verdict 与 Bundle，不代表完整项目自举已经发生。

### 已有一个本地 Web 项目

Starter 0.1 只支持一个有限预设：`single-webapp`。它面向 Windows 11、C1 进程冷状态、一个可信本地
应用进程、固定回环端口、HTTP 就绪探针和必需的真实 Chromium 证据。

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

如果项目包含多个服务、Docker Compose、远程数据库、登录凭据、非回环网络、来源不明的既有进程
或无法确定的资源所有权，Starter 0.1 会返回 `UNSUPPORTED`，不会猜测一个“看起来能跑”的方案。

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
[A0 冻结事实](docs/62-authoring-skill-a0-facts.md)。

## 当前支持边界

Core 0.12.0 已证明 Windows 11、C1、本地受控进程、真实 Chromium、不可变 Bundle、Catalog、
Comparison、Paired Analysis 和 Batch Analysis。它没有证明通用项目探测、自动安装、C2/C3、Docker、
跨平台、多服务编排、恶意代码隔离或生产容量。

遇到边界外项目时，正确结果是 `NOT_PROVEN` 或 `UNSUPPORTED`，不是自动修环境后继续宣布通过。
