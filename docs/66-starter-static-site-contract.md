# VeriTrail Starter 0.2 `static-site` Contract

> 状态：`IMPLEMENTED / NOT_RELEASED`；以本合同、Answers 0.2 Schema 和自动化验收共同为准
> 基线：VeriTrail Core 0.12.x；不修改 Core 的裁决语义

## 1. 目标

`static-site` 是 `single-webapp` 冻结后的第一个独立 Preset。它只把一个已经存在、无需构建、无需远程资源的静态 HTML 目录转换成可人工复核的 `DRAFT / NOT_SEALED` Profile、Plan 与本机绑定。

它不是通用前端探测器，不运行 `npm`、构建脚本或仓库命令，不自动修环境，不封存、不批准 Preview、不执行 Run，也不产生 Verdict。

## 2. 支持矩阵

必须同时满足：

- Windows 11 / C1 process-cold；
- 一个由 Core 拥有的回环 HTTP 服务进程；
- 用户明确提供本机 CPython console `.exe`；
- `entry_file` 是工作目录内真实存在的普通 `.htm` 或 `.html` 文件；
- `requires_build = false`；
- `requires_remote_assets = false`；
- 固定 IPv4 回环端口；
- Chromium、桌面与移动双视口；
- 至少一个显式 `expect_visible` 或 `expect_text` 业务检查；
- 所有预算、超时、随机种子与截图安全选择均由用户明确提供。

以下任一条件成立即 fail-closed：需要构建、包管理器、Shell、容器/VM/WSL、远程依赖、秘密、非回环流量、多个托管节点、入口文件缺失或不能确认普通文件身份。

## 3. Answers 0.2

新 Preset 使用 `schema_version = 0.2` 和独立的 `static_site` 块：

```json
{
  "schema_version": "0.2",
  "preset": "static-site",
  "static_site": {
    "python_executable": "C:\\absolute\\python.exe",
    "entry_file": "index.html",
    "port": 18778,
    "expected_status": 200,
    "requires_build": false,
    "requires_remote_assets": false
  }
}
```

其余 `subject`、`browser`、`budgets`、`timeouts` 与 `random_seed` 字段沿用严格的 Starter 输入边界。`browser.start_url` 必须精确指向 `http://127.0.0.1:<port>/<entry_file>`。

Starter 0.2 继续接受已发布的 Answers 0.1 `single-webapp`，不得重解释既有 0.1 工作区或 Release 事实。

## 4. 固定派生

Preset 只派生以下运行时事实：

- Profile 0.2 / `SINGLE_APPLICATION`；
- 一个 `APPLICATION` 节点，工具绑定为 `python-static-site`；
- 参数严格为 `-m http.server <node_port> --bind 127.0.0.1`；
- working directory 来自显式 Subject；
- readiness path 与浏览器入口均来自显式 `entry_file`；
- baseline id 为 `starter-static-site-0.2`；
- Core 既有 preflight、bootstrap、browser、subject-integrity 与 cleanup 硬断言。

用户不能在该 Preset 中插入任意服务参数。需要自定义服务命令时应改用 `single-webapp`，不能绕过合同。

## 5. Authoring Skill 边界

Skill 可以只依据普通文件名元数据把 `index.html` 标为 `INFERRED` 候选；它仍必须要求用户确认无需构建、无需远程资源和全部 Answers 0.2 字段。发现包管理器或容器标记时只能要求确认，不能读取仓库指令并自动执行。

Skill 仍只能调用 Starter `doctor`、`init`、`validate`、`review`，不得调用 `handoff`、Core seal/run/evaluate 或任何 Verdict 路径。

## 6. 验收

冻结前至少证明：

1. Answers 0.1 `single-webapp` 回归不变；
2. Answers 0.2 两个 Preset 的严格 Schema 与运行时校验一致；
3. `static-site` 输出字节确定、原子创建、禁止覆盖且始终未封存；
4. 生成 Profile/Plan 通过 Core 0.12.x 验证；
5. build/remote/secret/Shell/非回环/入口缺失负例 fail-closed；
6. Skill 只生成候选与 DRAFT，且按答案中的 Preset 调用 Starter；
7. 固定黄金 Subject 位于 `examples/starter/static-site`。

本合同不包含已暂停的 Codex Security 深度扫描、攻击路径验证或极端环境攻击工作流；这些继续封存，待官方验证链恢复后另行执行。
