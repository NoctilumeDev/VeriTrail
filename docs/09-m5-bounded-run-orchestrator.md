# 09. M5 有界运行编排与静态目标生命周期

## 状态与认识边界

`PLANNED（仅合同；尚无 M5 实现、自动化或真实运行结论）`。前置 M0–M4 已分别达到
`FROZEN`，M4 冻结标签为 `m4-v0.5.0`。

本文件预注册 M5 的问题、范围、安全边界、控制变量、失败语义和退出条件。文档合并只表示
允许开始实现，不表示 Plan 0.4、运行编排、静态目标服务、证据或清理已经成立。实现后的事实
若反驳这里的设计，必须保留失败 Run，并以新合同版本修正；不得回写标准制造通过。

## 目标问题

M5 只回答一个问题：

> 一个封存的 ExperimentPlan 能否通过单一 `run` 入口，在启动前预检通过后，由 VeriTrail
> 启动一个受限的只读静态回环目标，串行采集真实 Chromium 证据，确定性生成不可变 Bundle，
> 并在成功、失败和异常路径上证明目标、浏览器、线程、端口与 staging 已清理？

当前 `browser-capture` 已能对“外部已启动”的回环站点执行预检、浏览器采集和裁决，但目标
启动/就绪/停止仍由用户手工完成。M5 的增量不是重写 M0–M4，而是把这一段缺失的生命周期纳入
封存计划和证据链。

M5 不回答：

- 任意项目命令是否安全执行；
- npm、Maven、Docker、数据库或中间件能否由 VeriTrail 管理；
- UI 是否可以编辑计划、启动 Run 或展示实时进度；
- 两个 Run 是否可以自动比较、选基线或生成趋势；
- v0 完整自举或跨项目证明是否已经完成。

## 前置门禁

- M4 合同：`b86760c6ba028f63da17f09d76f51477ddba0bd8`；
- M4 实现：`ddcfa314b40bf9ba3332fec1e190e6335a4c1502`；
- M4 冻结：`d0950579ed2fefb28bee4e76bf1de88d24b0fe69`（tag `m4-v0.5.0`）；
- M4 主分支与标签已从 GitHub 远端读回，工作区在 M5 规划前为干净状态。

若实现期间发现必须修改 M0 Verdict 优先级、M1 资源决策、M2 浏览器事实语义、M3 Bundle
Loader 或 M4 Catalog 权威边界，视为范围上浮；停止实现并重新评审消费者矩阵。

## 影响层级、所有者与消费者

- 声明层级：`L2_CONTRACT`；
- 所有者：Python Core / Bounded Orchestrator；
- 新契约候选：ExperimentPlan 0.4、`runtime.orchestration` Evidence、`run` CLI；
- 直接消费者：Plan 校验/Seal、编排器、Evidence 校验器、Verdict、Report/Manifest、CLI；
- 兼容消费者：M0–M4 CLI、Catalog 校验、Vue Workbench 通用 Evidence 账册、既有 Plan 0.1–0.3；
- 后续消费者：计划编辑器、跨 Run 比较、更多显式目标适配器与完整自举；
- 数据所有权：封存 Plan 决定运行政策；Evidence 记录事实；Report/Verdict 仍由确定性规则生成；
  编排器不得直接写最终 `PASS/FAIL`。

## 控制变量设计

### 基线

基线是 M2 的外部目标模式：固定 Plan、静态文件、浏览器版本、视口、步骤、资源预算和断言，
目标站点已由外部步骤启动，`browser-capture` 只负责预检、采集与 Bundle。

### 唯一主要变量

`target_lifecycle_mode`：

- 基线值：`externally_managed_loopback`；
- M5 处理值：`veritrail_managed_static_http`。

### 受控变量

- 同一静态目录字节与目录指纹；
- 同一 Chromium 引擎、浏览器政策、视口和步骤；
- 同一资源预检政策、Artifact 上限、Run ID 规则和 Verdict 规则；
- 固定回环地址、显式端口、单目标、单浏览器、串行执行；
- 相同代码提交、依赖锁、随机种子和清理断言。

### 干扰与观察者效应

- Windows 调度、杀毒扫描、浏览器冷启动和端口释放延迟；
- VeriTrail 内置 HTTP 线程、就绪轮询和请求审计的内存/时间开销；
- Codex 内置浏览器宿主自身的遥测或网络噪声，不得混入被测页面事实。

这些事实只能进入适用边界，不能在观察结果后改成第二个主要变量。

## M5 最小纵向范围

1. 新增向后兼容的 ExperimentPlan 0.4；
2. Plan 0.4 在 Plan 0.3 的 `preflight` 与 `browser` 上增加一个 `target` 对象；
3. 新增 `veritrail run --plan ... --subject-root ... --run-id ... --output ...`；
4. `run` 只接受 Plan 0.4 和 `STATIC_HTTP` 适配器；
5. 编排顺序固定为：校验/Seal → 预检 → 目标校验与启动 → 就绪探测 → 浏览器采集 →
   目标停止 → 端口/线程清理核验 → Verdict → 原子 Bundle；
6. 生成严格校验的 `runtime.orchestration` Evidence；
7. 任何已创建的 Run 目录不可覆盖；失败和异常尽量形成可审计 Bundle，而不是只留下终端文本；
8. M4 Catalog 和 M3 Workbench 只能按既有通用接口读取新 Bundle，不为 M5 增加特殊 Verdict。

### 明确不做

- Shell 字符串、`cmd /c`、PowerShell 命令、管道、重定向、变量展开或命令替换；
- 任意可执行文件、脚本、Python `-c/-m`、npm/Maven/Gradle、Docker 或服务控制；
- 在线 API 写入、后台队列、文件监视器、实时进度 WebSocket/SSE；
- 多目标、多进程、多端口、并行浏览器 Context、远程 URL、TLS、认证或浏览器 Profile；
- 目录列表、上传、写文件、删除/移动输入、修改防火墙/代理/路由；
- 计划编辑、基线自动选择、跨 Run 差异、趋势、报告发布和 AI 裁决。

## ExperimentPlan 0.4 候选合同

Plan 0.4 保留 Plan 0.3 全部字段和语义，只新增必填 `target`：

```json
{
  "target": {
    "adapter": "STATIC_HTTP",
    "root": "examples/browser/site",
    "port": 18769,
    "ready_path": "/",
    "startup_timeout_ms": 5000,
    "shutdown_timeout_ms": 5000,
    "max_files": 256,
    "max_file_bytes": 10485760,
    "max_total_bytes": 67108864
  }
}
```

约束：

- `root` 必须是 1–8 段、只含小写字母/数字/`._-` 的相对 POSIX 路径；禁止绝对路径、盘符、
  反斜杠、空段、`.`、`..`、控制字符和 URL 编码绕过；
- `subject-root` 只由 CLI 显式提供，不写入 Plan、Evidence、Report 或 stdout；
- `target.root` 解析后必须留在 `subject-root` 内，路径链和服务文件不得包含 symlink、junction、
  reparse point 或硬链接混淆；
- `port` 必须是显式回环端口，并在 `preflight.ports` 中声明为 `FREE`；
- `browser.start_url` 与所有 `allowed_origins/goto` 必须精确使用该端口；
- `ready_path` 只允许安全的绝对 URL path，不含 query、fragment、反斜杠或点段；
- 限额必须满足：`max_files` 1–1000，单文件 1 B–10 MiB，总量 1 B–64 MiB，且单文件上限
  不得大于总量上限；
- Plan 0.4 必须要求 `runtime.preflight`、`runtime.orchestration` 与 `browser.session`，并至少对
  编排清理和浏览器事实定义决定性断言；
- 0.4 Seal 覆盖完整 target 政策。修改端口、根、限额、超时或就绪路径必须产生新 Plan 哈希。

Plan 0.1–0.3 的哈希、校验、命令行为和既有示例必须保持字节级兼容。

## 静态目标与请求边界

- 只绑定 `127.0.0.1:<port>`，不监听 `0.0.0.0`、IPv6 或局域网地址；
- 启动前离线扫描并冻结允许文件集合和 SHA-256 目录指纹；服务期间不跟随新增文件；
- 仅允许 `GET`/`HEAD`，其他方法返回 405；不提供目录列表、Range、CORS 或写接口；
- 请求 Host 必须与当前回环端口一致；路径解码后必须落在冻结文件集合；
- 默认文档只解析 `index.html`；文件类型使用固定允许列表，不按用户输入执行内容；
- 每次响应前复核当前普通文件、大小和 SHA-256；源文件丢失或改变即拒绝，不返回旧可信内容；
- 记录有界请求事实：顺序、方法、脱敏 path、状态、字节数；不记录请求/响应头、Cookie、正文、
  query 值、个人路径或客户端网络标识；
- 请求事件最多 1000 条，超限形成稳定 collection error，不无界增长内存。

## 编排状态机与失败语义

```text
VALIDATE
  -> PREFLIGHT
      -> ABORTED/PENDING                 (ABORT)
      -> COMPLETED/PENDING               (STOP_ESCALATION)
      -> STARTING                        (PROCEED)
          -> READY -> BROWSER -> CLEANUP -> EVALUATE -> BUNDLE
          -> ERROR -> CLEANUP -> EVALUATE -> BUNDLE
```

- 计划/路径/安全校验失败：命令退出 2，不启动目标，不创建 Run；
- 输出已存在：命令退出 2，不覆盖；
- 预检 `ABORT`：不启动目标，输出 `ABORTED / PENDING` Bundle；
- 预检 `STOP_ESCALATION`：不启动目标，输出 `COMPLETED / PENDING` Bundle；
- 启动、就绪、服务或浏览器异常：先清理，再以 `ERROR` 形成可审计 Bundle；只有独立的决定性
  事实失败时才允许 Verdict 为 `FAIL`，否则保持 `PENDING`/`INCONCLUSIVE`；
- 清理失败：不得 `PASS`；写入稳定编排事实并保持端口/线程残留可见；
- Bundle 写入仍使用 staging + 原子 rename；写入失败清除 staging，但不覆盖已有输出。

## `runtime.orchestration` Evidence 0.1

严格字段至少包括：

- collector/version、target policy SHA-256、静态目录指纹和文件/字节计数；
- started/ready/stopped/cleanup timestamps 与有界 elapsed；
- 目标 origin（规范化为 localhost）、就绪探测次数和最终状态；
- 生命周期事件时间线与稳定 error type，不持久化原始异常文本；
- 请求计数、GET/HEAD/拒绝数、状态分布和有界请求事件；
- `server_started`、`ready`、`server_stopped`、`thread_stopped`、`port_released`、
  `cleanup_complete`；
- collection errors、observer RSS before/peak/delta 与最大活动线程数；
- 元数据明确 `shell_used=false`、`external_process_started=false`、`writes_allowed=false`、
  `network_scope=loopback-only`。

Evidence 校验器必须拒绝缺字段、额外字段、计数不一致、非回环 origin、未脱敏路径、政策哈希
错误和自相矛盾的完成状态。Verdict 必须检查单 Run 最多一份编排证据、政策与 Plan 一致，且
`cleanup_complete=false` 时阻止 `PASS`。

## 控制组与证伪矩阵

| 组 | 唯一变化 | 预期事实 |
| --- | --- | --- |
| 正向 | 合法静态目录 | `COMPLETED/PASS`，浏览器和清理证据齐全 |
| 预检中止 | 硬内存线高于现实余量 | `ABORTED/PENDING`，目标从未启动 |
| 停止升压 | 软线触发、硬线未触发 | `COMPLETED/PENDING`，目标从未启动 |
| 空/缺入口 | 静态目录不可服务 | 校验失败或 `ERROR`，不得留下监听 |
| 路径穿越 | root/ready/request 含点段或编码绕过 | 拒绝且不泄露路径 |
| 链接混淆 | root 链或文件为 symlink/junction/reparse/hardlink | 启动前拒绝 |
| 源变化 | 索引后同尺寸修改或删除 | 服务拒绝，浏览器/编排事实可见，不能返回旧内容 |
| 端口竞争 | 预检后、绑定前被占用 | `ERROR/PENDING` 或独立断言结果，且不停止外部占用者 |
| 浏览器失败 | 确定性选择器失败 | 失败 Run 保留，目标仍必须清理 |
| 方法/Host | POST、Range、错误 Host | 405/400，0 写入、0 CORS |
| 重复 Run | 同 output 或 Run ID 再执行 | 拒绝覆盖原 Bundle |

正向通过不能替代负向；负向失败不能通过删除证据或放宽断言修正。

## 自动化门槛

- Plan 0.4 Schema、Seal、篡改、版本兼容和敏感值拒绝；
- 静态根路径、普通文件、链接/硬链接、限额、MIME、Host、方法、Range、穿越和源变化；
- 编排顺序、预检三决策、启动失败、就绪超时、浏览器异常、清理和原子输出；
- `runtime.orchestration` 严格字段、计数、哈希、政策漂移、重复证据和 Verdict；
- CLI stdout/stderr、退出码、拒绝覆盖和不泄露绝对路径；
- M0–M4 全量回归、Catalog 接纳 Plan 0.4 Bundle、Workbench 通用读取；
- Python 3.10/3.13；前端 lint、测试和生产构建；worker 上限遵守 16 GB 资源策略。

自动化通过最多推进到 `AUTOMATED`，不能替代真实运行。

## 真实运行退出条件

1. 从干净实现提交和唯一 Plan 0.4 运行正向 `run`，没有预启动目标；
2. 命令自行启动静态目标、完成桌面/移动 Chromium、生成 Bundle 并释放目标；
3. Bundle 可由 M4 Catalog 建索引，并由 Workbench 读回 Plan 0.4、三类 Evidence、断言、截图和
   `COMPLETED/PASS`，不增加特殊前端裁决；
4. 真实运行预检 `ABORT`、`STOP_ESCALATION`、浏览器失败、源变化或端口竞争等适用控制组；
5. Codex 内置浏览器完成用户可见主链，检查 Console、Network、同源、桌面/移动、历史和失败态；
6. 两套 Python、全部自动化、生产构建、依赖审计和敏感扫描通过；
7. 结束后 Chromium、HTTP server、线程、端口、对象 URL、SQLite sidecar 与 staging 全部释放；
8. Git 工作区只含预期提交，冻结提交与 `m5-v0.6.0` 可从 GitHub 远端读回。

只有全部成立，M5 才能依次推进为 `IMPLEMENTED`、`AUTOMATED`、`RUNTIME_VALIDATED`、
`FROZEN`。任一事实未成立时必须报告真实中间状态。

## 合同记录

- 合同版本：M5 Bounded Run Orchestrator Contract 0.1；
- 目标 Plan：ExperimentPlan 0.4；
- 目标 Evidence：`runtime.orchestration` 0.1；
- 目标 CLI：`run`；
- 目标版本：Python Core `0.6.0.dev1`，Workbench `0.6.0-dev.1`；
- 当前里程碑状态：`PLANNED`；
- 未产生的结论：实现正确性、目标服务安全性、异常清理、资源适用性和完整自举。
