# M10 有界完整项目自举合同

> 状态：`CONTRACT_DRAFT 0.1 / PLANNING`
> 影响层级：`L3_SYSTEM`（项目 Profile、长运行进程、就绪状态机、所有权与逆序清理）
> 前置基线：`m9-v0.10.0` @ `3181d69`
> 首个证明范围：Windows 11 / `C1 PROCESS_COLD` / 宿主机本地可信进程 / 严格串行
> 目标版本：Python Core `0.11.0.dev1`，Workbench `0.11.0-dev.1`
> 目标冻结标签：`m10-v0.11.0`
> 实施门禁：本合同冻结前不得新增 Plan 0.6、ProjectProfile、服务执行器或运行代码

## 1. M10 只回答一个问题

> VeriTrail 能否在一个预先声明、资源有界的 Windows C1 冷状态中，按依赖顺序启动一个本地依赖
> 进程和一个应用进程，证明它们真实就绪并可被浏览器使用，然后在成功、失败或中止后按逆序恢复
> 到可解释的清洁状态？

这里的“完整”只表示**声明范围内的生命周期闭环完整**。M10 不是系统安装器、包管理器、通用
服务管理器、容器编排器或不可信代码沙箱。

控制变量固定为：

- M9 已证明可信 `ONESHOT` 的结构化预览、审批、Job Object 所有权和证据链；
- M10 唯一主要增量是两个**长运行、Run-owned、本地进程**的依赖顺序、就绪和逆序回收；
- 不同时引入 C2 依赖恢复、Docker、第二平台、真实项目或新前端控制台。

## 2. 已冻结事实与不可改写边界

M10 消费但不重解释：

- M0 的 sealed Plan、Evidence、Report、Manifest、ExecutionStatus 与 Verdict；
- M1 的资源预检和 `PROCEED / STOP_ESCALATION / ABORT`；
- M2 的有界回环 Chromium 与浏览器证据；
- M4 的 Bundle 权威、可重建 Catalog 和固定回环只读 API；
- M5 的异常路径清理原则；
- M6–M8 的 Comparison、Pairing 与 Batch 独立派生边界；
- M9 的普通 `.exe`、无 Shell、无 stdin/TTY、ToolBindings 0.1、暂停后分配 Job、进程树回收、
  输出脱敏和“不可信代码不受支持”边界。

M10 不得把 M9 `command.adapter=TRUSTED_PROCESS_ONESHOT` 改成长运行模式，也不得改变 Plan 0.5
的命令顺序或冻结语义。服务生命周期必须拥有独立的新合同和证据类型；旧 Plan 0.1–0.5、Bundle、
Catalog、Workbench、Comparison、Pairing 与 Batch 消费者继续兼容。

若实现要求修改 M9 的信任模型、公共 ExecutionStatus/Verdict、旧 Evidence 含义或冻结标签，停止
M10 并上浮合同，不得以“复用代码”为名静默改写基线。

## 3. 最大声明与非目标

### 3.1 冻结后允许作出的最大声明

只有全部出口通过后，M10 最多声明：

> 在本次 Windows 11、C1、16 GB 主机和封存 Profile 边界内，VeriTrail 能管理一个可信依赖进程
> 与一个可信应用进程的启动、owned readiness、浏览器 exercise、逆序强制回收、证据封存和残留
> 检查；成功、启动失败、就绪超时、用户中止和端口竞争均保持可解释状态。

### 3.2 明确不证明

- C0 既有服务接管、C2 锁文件依赖恢复或 C3 主机安装；
- Linux、macOS、WSL、Docker、Windows 服务或远程主机；
- npm、Maven、pip、conda 等包管理器生命周期；
- 数据库事务安全、服务优雅停机、数据迁移或崩溃一致性；
- 文件系统隔离、网络隔离、TOCTOU containment 或恶意代码 containment；
- 任意依赖图、动态服务发现、真实重叠并行或生产容量；
- 不同类型真实项目的通用适配性；该结论属于 M11。

## 4. 冷状态合同

| 级别 | 定义 | M10 0.1 行为 |
| --- | --- | --- |
| `C0 RUNNING` | Profile 声明的服务或端口已经存在 | `NOT_PROVEN`；拒绝接管，不停止外部资源 |
| `C1 PROCESS_COLD` | 合格运行时与项目依赖已存在，声明服务未运行 | 唯一冻结目标 |
| `C2 WORKSPACE_COLD` | 运行时存在，但项目依赖尚未按锁文件恢复 | `NOT_SUPPORTED`；不运行安装命令 |
| `C3 HOST_COLD` | 运行时、系统工具或中间件缺失 | `NOT_SUPPORTED`；不修改主机 |

一次有效 C1 起点必须同时满足：

1. sealed Profile、sealed ExperimentPlan、subject root 和本地 ToolBindings 全部可解析且相互绑定；
2. 两个可执行文件均通过 M9 同级别的普通 `.exe`、文件身份与允许列表核验；
3. 项目依赖已经存在，M10 不执行恢复、安装或升级；
4. 两个声明端口均为 `127.0.0.1` IPv4、互不重复、预检为 FREE；
5. 没有证据表明声明服务已在运行；仅凭名称相同不构成接管权；
6. 可用内存、磁盘、输出目录和工具自身预算满足 sealed 停止线；
7. 上一 Run 的 owned 进程、端口、工作目录或 staging 残留为 0。

任一条件不成立时不进入进程创建。资源、版本、端口或冷状态门禁导致的停止使用
`ABORTED/PENDING`；发现主体或 Profile 漂移时使用 `INCONCLUSIVE`，不能自动修复环境后继续。

## 5. 公共合同候选

M10 0.1 计划新增以下独立、版本化合同；字段在合同冻结前仍是提案，不是代码事实。

### 5.1 `ProjectProfile 0.1`

ProjectProfile 是服务拓扑的权威声明，使用规范 JSON、内容哈希和独立 seal。它不保存本机绝对
路径或秘密。首片固定：

- 一个稳定 `profile_id` 与版本；
- `platform=WINDOWS_11`、`cold_state=C1_PROCESS_COLD`；
- 恰好两个节点：一个 `DEPENDENCY`、一个 `APPLICATION`；
- 依赖节点 `depends_on=[]`，应用节点只依赖该依赖节点；禁止环和隐式依赖；
- 每个节点固定 `adapter=TRUSTED_PROCESS_SERVICE`、tool binding、结构化参数、工作目录、环境名称、
  单一回环端口、输出/进程上限、就绪策略与回收策略；
- 应用节点声明唯一 browser origin；它必须与应用端口一致；
- 全局启动顺序、逆序清理、资源预算、subject watch roots 和残留检查策略。

Profile 的自动发现只能生成候选事实，不能修改或替代 sealed Profile。观察到的版本、端口或路径与
Profile 不一致时停止；不得自动选择“看起来能用”的另一套 Python/Node。

### 5.2 `ExperimentPlan 0.6`

Plan 0.6 绑定 `profile_id + profile_sha256`，而不复制 Profile 内容。它继续拥有问题、基线、唯一
主要变量、资源停止线、浏览器步骤、断言、必需证据、复现与清理语义，并要求：

- `runtime.preflight`、`runtime.bootstrap` 与 `browser.session` 各恰好一份；
- 至少一个 HARD/DEGRADATION 断言消费 `runtime.bootstrap`；
- browser URL 的 origin 必须等于 Profile 的应用 origin；
- Profile 与 Plan 都必须在首次运行前封存；任何语义变化生成新版本；
- Plan 0.6 不要求也不隐式执行 Plan 0.5 的 `command` 或 M5 `STATIC_HTTP`。

### 5.3 复用 `ToolBindings 0.1`

本机可执行路径仍通过 M9 的 ToolBindings 0.1 提供，值不进入 Plan、Profile、Preview 或 Bundle。
每个节点引用稳定 binding ID；运行时必须重新核对 basename、大小、SHA-256、普通文件、非链接/
reparse point 和普通 `.exe`。绑定缺失或变化时 Preview 失效，禁止运行。

### 5.4 `BootstrapPreview 0.1`

执行前生成只读 Preview，至少封存：

- Plan/Profile seal 与政策哈希；
- subject/working directory 身份摘要；
- 两个 executable 身份、结构化参数和环境名称投影；
- 确定性启动顺序与逆序清理顺序；
- 两个回环端口、就绪 URL、浏览器 origin 与超时；
- 每节点 Job/输出/进程上限和全局资源停止线；
- 文件系统、网络、优雅停机、不可信代码与其他平台的 `NOT_PROVEN/NOT_SUPPORTED` claims；
- `preview_sha256`。

`run` 必须接收用户批准的精确 Preview digest，并在进程创建前重新构建 live Preview；任何差异都
拒绝运行。Preview 只展示路径身份摘要与 executable basename，不持久化个人绝对路径。

### 5.5 CLI 入口候选

```text
bootstrap-profile-seal --profile <draft> --output <sealed>
bootstrap-preview --plan <sealed> --profile <sealed> --subject-root <root> --tool-bindings <local>
run --plan <sealed> --profile <sealed> --subject-root <root> --tool-bindings <local>
    --approve-bootstrap-preview-sha256 <digest> --run-id <id> --output <new-directory>
```

不增加在线编辑、Shell 字符串、后台守护进程、全局服务注册或“自动修复”命令。

## 6. 生命周期状态机

这些是 `runtime.bootstrap` 内部阶段，不新增公共 ExecutionStatus：

```text
DISCOVERED
  -> PREFLIGHTED
  -> PREPARED
  -> DEPENDENCY_STARTING -> DEPENDENCY_READY
  -> APPLICATION_STARTING -> APPLICATION_READY
  -> SERVICES_READY
  -> EXERCISED
  -> EVIDENCE_FINALIZED
  -> TEARDOWN_APPLICATION
  -> TEARDOWN_DEPENDENCY
  -> TEARDOWN_COMPLETE
```

从 `PREPARED` 之后任一阶段均可进入：

```text
ABORTING -> EVIDENCE_FINALIZED -> TEARDOWN_APPLICATION? -> TEARDOWN_DEPENDENCY? -> TEARDOWN_COMPLETE
```

问号只表示该节点可能尚未创建，不表示可以跳过已创建节点。所有阶段转换追加时间线，不能覆盖旧
事件；同一节点不能二次 START，重复启动必须成为编排错误而不是新服务。

`EVIDENCE_FINALIZED` 在本合同中表示：所有 teardown 前事实已经复制到 Run-owned staging，之后
不再执行被测用户步骤。它不是最终 Bundle 已落盘；最终 `runtime.bootstrap` 在 teardown 事实齐全
后一次性生成并进入不可变清单。即使 staging 或 Evidence 生成失败，`finally` 清理也必须运行；
验收器保留该失败与残留事实，不能因为无法写 Bundle 就跳过回收。

## 7. 进程所有权与启动

- 每个节点使用**独立** Windows Job Object；依赖与应用不能共用一个只能整体关闭的 Job；
- 复用 M9 的 `CREATE_SUSPENDED -> AssignProcessToJobObject -> ResumeThread` 顺序，先拥有再执行；
- 每个 Job 设置 `KILL_ON_JOB_CLOSE` 与 sealed active-process limit，不允许 breakaway；
- Job handle、根进程 handle、输出 reader 和运行目录都归当前 Run 所有，直到对应节点完成 teardown；
- 子进程默认继承 Job；Job process list 用于 owned listener 交叉核验；
- 启动严格串行：依赖 READY 前不得创建应用；应用 READY 前不得执行浏览器；
- 根进程启动后提前退出、Job 分配/恢复失败或 active-process limit 触发都进入结构化节点事实；
- 不按进程名、映像名、模糊命令行或端口号终止进程；这些只能用于诊断，不能建立所有权；
- 只清理当前 Run 持有 Job 的进程树和明确创建的 Run work/staging；不回滚 subject 文件，也不删除
  Profile 之外的文件。

## 8. 就绪与 exercise

首片只支持一种探针：`HTTP_GET_LOOPBACK_OWNED_PID`。

一次 READY 必须同时满足：

1. 直接绕过代理访问 sealed `http://127.0.0.1:<port>/<safe-path>`；
2. 不发送认证材料，不跟随重定向，不接受 query/fragment；
3. 在单次超时、总超时、最大响应字节和固定间隔内返回 sealed 允许状态码，首片固定 200；
4. Windows TCP listener 的 owner PID 属于该节点实时 Job process list；
5. Job 仍有活动进程，根/后代未出现未解释退出；
6. 成功事实至少连续取得两次，避免一次瞬时响应冒充稳定就绪。

仅“进程存在”、仅“端口 LISTEN”或仅“HTTP 200”都不能单独成为 READY。owner PID 查询失败、
响应来自外部 PID 或端口在启动竞态中被其他进程占用时，探针失败并进入 ABORTING；绝不停止该
外部进程。

`EXERCISED` 由现有 M2 Browser Adapter 对应用 origin 完成 sealed 桌面/移动步骤后产生。M10 不
新增浏览器控制语义；Console、Network、截图、失败请求和溢出继续进入 `browser.session`，最终
Verdict 仍由 sealed assertions 决定。

## 9. 逆序回收与清洁状态

首片回收策略固定为 `JOB_TERMINATE_AFTER_CAPTURE`，不声明优雅停机：

1. 停止新增浏览器/探针/被测步骤并封存 teardown 前事实；
2. 关闭浏览器 Context；
3. 终止应用 Job，等待 Job active process 为 0，关闭其进程/线程/管道/Job handles；
4. 确认应用端口释放；
5. 终止依赖 Job并执行同样检查；
6. 确认依赖端口释放；
7. 结束输出 reader，落盘脱敏附件，删除 owned staging/work；
8. 复查两个端口、两个 Job、owned 进程、线程、handles 和临时目录；
9. 对 subject watch roots 做最终指纹比较。

回收某一步失败不能阻止后续 best-effort 清理。`cleanup_complete=true` 只有全部适用条件为真；
超时或残留必须保留具体节点、阶段、计数和错误类型。下一 Run 在残留解释并清除前不得开始。

## 10. 写入、环境、网络与秘密边界

- 服务仍只接受用户信任的本地代码；Job Object 不是安全沙箱；
- 继承环境默认只允许 `SYSTEMROOT/WINDIR`，runner 注入独立 TEMP/TMP 与 Run work；
- Profile 只允许固定非秘密 runner 变量名或 typed 参数占位，不接受 `.env`、任意秘密值或 PATH；
- stdout/stderr 并发有界读取，内存与落盘两次脱敏，原始 canary 不进入 Bundle；
- subject watch roots 运行前后比较；变化不自动回滚，运行进入 `INCONCLUSIVE` 并保留差异摘要；
- 本合同只约束 VeriTrail 自身的 readiness/browser 请求为回环；它不阻止可信服务自行联网，网络
  隔离保持 `NOT_PROVEN`；
- 不采集请求/响应头、Cookie、正文、个人绝对路径、账号、公网 IP 或 ToolBindings 值；
- Run work、日志、截图和 staging 默认进入 Git 忽略目录，且路径必须由本轮创建并核验所有权。

## 11. `runtime.bootstrap` Evidence 0.1

单一 Evidence 至少包含：

- Plan/Profile/Preview/Tool policy 哈希与 collector 版本；
- 声明/观察的 OS、冷状态、启动顺序、回收顺序和资源起点；
- 每节点 executable 身份摘要、Job backend、active-process 上限和安全 claims；
- 每阶段时间线、根进程退出、Job active-process 采样和输出摘要；
- readiness 每次尝试的时间、结果类别、HTTP 状态、listener owner 是否属于 Job；
- browser exercise 是否开始/完成及其 Evidence 引用；
- ABORT/ERROR 原因、用户取消和停止线；
- teardown 顺序、Job/handles/readers/ports/work/staging/subject 最终事实；
- 脱敏计数、附件哈希、观察者资源和 `cleanup_complete`。

Evidence 不保存 PID 的长期身份主张；PID 只作为同一运行时间线内的短期诊断事实，持久化时可用
Run-local ordinal/摘要表达。它不保存原始绝对路径、环境值、响应正文或完整命令行。

## 12. ExecutionStatus 与 Verdict 映射

| 场景 | ExecutionStatus | 默认 Verdict 上界 |
| --- | --- | --- |
| 两节点 READY、browser 完成、清理完成 | `COMPLETED` | 由 assertions 决定，可为 `PASS` |
| 可信节点启动后提前退出且形成完整负向证据 | `COMPLETED` | HARD readiness 失败可为 `FAIL` |
| 资源预检、端口竞争、版本/C1 缺口 | `ABORTED` | 无独立 HARD 失败时 `PENDING` |
| readiness 总超时或用户中止 | `ABORTED` | 无独立 HARD 失败时 `PENDING` |
| subject/Profile/Preview 漂移 | 依执行完整度决定 | `INCONCLUSIVE` |
| Job/collector/证据系统非预期错误 | `ERROR` | `PENDING` 或已有 HARD `FAIL` |
| 任一 owned 残留或逆序清理失败 | `ERROR` | cleanup HARD 断言为 `FAIL` |

退出码、HTTP 200、Job 清空或浏览器成功都只是事实；任何一个都不能单独把整个 Run 提升为 PASS。

## 13. 资源合同

- 16 GB 主机严格串行；同时最多存在一个依赖节点、一个应用节点和一个 Chromium Context；
- 不启动 Docker、WSL 中间件、数据库或其他完整项目栈；
- 每次 Preview 和 Run 重新采样内存、C/D 磁盘、两个端口与适配器版本；
- Core、两个节点与 Chromium 分开记账；
- Profile 声明每节点 process/output/time 限额和全局软/硬内存停止线；
- 软阈值停止进入下一阶段，硬阈值立即 ABORT、保存现场并逆序清理；
- 不以机器档案快照代替当前事实，不因 16 GB 降低清理、安全或一致性断言。

## 14. 首个真实纵向切片

首片使用仓库内两个独立、脱敏、无包管理器的轻量可信 Subject：

- dependency：普通 Python `.exe` 直接启动的回环 HTTP 进程；
- application：另一个 Python `.exe` 回环 HTTP 进程，启动后访问 dependency，并向 Chromium 展示
  dependency 事实；
- 两者只写各自 Run work，不读取 `.env`，不依赖 Docker/数据库/代理/公网；
- 应用的页面由现有 Browser Adapter 在桌面和移动视口真实操作；
- 该夹具只证明生命周期 Core，不构成第二种真实项目证明。

所有 Profile、Plan、断言、端口、故障点和退出条件在首个 Run 前一次性封存。失败后修改标准必须
生成新版本和新目录，不覆盖旧事实。

## 15. 自动化与真实验收矩阵

### 15.1 合同与组件自动化

- Profile/Plan/Preview 严格字段、seal、哈希和交叉引用；
- 依赖图固定两节点、无环、顺序/逆序确定性；
- executable/working directory/typed 参数/环境/端口/URL 安全边界；
- Preview live rebuild 与审批 digest 不一致拒绝；
- Job 创建、暂停分配、恢复、active-process list、输出和 handle 清理；
- readiness 200 但 listener 不属于 Job 时拒绝；
- 旧 Plan 0.1–0.5、Bundle、Catalog、Comparison、Pairing、Batch 与 Workbench 回归。

### 15.2 必须真实串行完成的运行

1. C1 成功：dependency -> application -> browser -> application cleanup -> dependency cleanup；
2. 完全相同 sealed Plan/Profile 第二次复跑，证明第一次无污染；
3. dependency 提前退出，application 从未创建，已创建资源仍清理；
4. application readiness 超时，dependency 与 application 均逆序清理；
5. browser exercise 失败，两个服务仍逆序清理并形成负向证据；
6. 用户在 application READY 后中止，形成 `ABORTED/PENDING` 与完整清理；
7. dependency 或 application 端口被外部进程占用：不创建/不接管/不终止外部进程；
8. listener owner 与 Job 不匹配：不得误判 READY，不误杀外部进程；
9. subject 最终状态漂移：不回滚，Verdict 为 `INCONCLUSIVE`；
10. cleanup 注入失败：继续 best-effort 回收，状态不得伪装为 clean；
11. Evidence staging 注入失败：仍执行逆序清理并由验收器保留失败事实；
12. Catalog 接纳最终 Bundle，现有 Workbench 通用账册读回 `runtime.bootstrap`。

### 15.3 浏览器、资源、安全与清理终验

- 真实 Chromium 和 Codex 内置浏览器完成正向、负向、刷新/返回、桌面/移动、键盘；
- DevTools Console/Network 无未解释异常，页面请求全部属于声明的回环 origin；
- 双 Python 兼容回归、前端 test/lint/type-check/build、依赖审计通过；
- Profile/Plan/Bundle/日志/附件无真实秘密、个人绝对路径、账号或公网 IP；
- 最终两个端口、两个 Job、M10 Python/Node 进程、Chromium、reader、Run work、staging 和临时目录
  残留均为 0；工作区干净；
- GitHub 远端读回冻结提交与 `m10-v0.11.0` 标签后才可标记 `FROZEN`。

## 16. 停止条件

出现以下任一情况立即停止实施或运行：

- 需要 Shell、包管理器、Docker、C2/C3、系统服务、管理员权限或修改 PATH/代理/防火墙；
- 无法在进程执行前建立 Job 所有权；
- 无法把 listener owner 与当前节点 Job 建立可靠交叉核验；
- 只能通过进程名/PID/端口猜测并终止资源；
- 必须扩大为任意依赖图、动态端口、优雅停机协议或第二平台才能通过；
- Evidence 失败会绕过清理，或清理失败仍会生成 clean/PASS；
- 需要修改 M0–M9 冻结语义或删除不利失败事实；
- 当前可用内存、磁盘或端口不满足 sealed 硬门槛。

## 17. 合同冻结前的设计验证项

本 0.1 草案还不能授权实现。首次只读设计核验形成以下候选决策：

1. **listener owner 后端**：本机锁定的 `pywin32==312` 提供
   `JobObjectBasicProcessIdList`，但没有 `win32iphlpapi` 模块或 `GetExtendedTcpTable` binding。
   草案选择一个 M10-only、窄封装的标准库 `ctypes` IP Helper 适配器读取
   `TCP_TABLE_OWNER_PID_LISTENER`；M9 Job 后端继续固定 pywin32，不降级为 ctypes。禁止新增 Shell、
   `netstat` 或 PowerShell 文本解析。合同冻结前仍需核对结构大小、IPv4 字节序、缓冲区重试、
   权限失败与 PID race 的负向设计；
2. **Job 生命周期复用边界**：M9 `run_owned_process` 当前把 start、wait、terminate 和 close 固定在
   一次函数内，不能被长运行服务直接调用。M10 必须增加独立的 long-lived owned-service session；
   不改变 `run_owned_process` 的签名、返回值或 Plan 0.5 Evidence 映射。若抽取内部低层 helper，
   必须使用单独提交和 M9 characterization/full regression 证明行为未变；
3. **Plan 0.6 消费者矩阵**：冻结候选如下，任何实现 diff 越界都回到合同评审。

| Consumer | Plan/Profile 0.1/0.6 rule |
| --- | --- |
| profile sealer | 只封存 ProjectProfile 0.1；拒绝绝对路径、秘密、未知字段和非两节点图 |
| plan sealer/validator | 识别 Plan 0.6 并绑定 Profile SHA；旧 Plan 0.1–0.5 行为不变 |
| `bootstrap-preview` | 只读解析 sealed Plan/Profile/ToolBindings，生成 Preview，不启动进程 |
| `run` | Plan 0.6 必须提供 Profile、ToolBindings 与精确 approval digest；旧版本不要求新参数 |
| evidence/verdict | 严格校验唯一 `runtime.bootstrap` 与政策哈希；不改写公共状态枚举 |
| report/manifest | 透传 Plan 0.6 与新 Evidence，继续执行哈希、脱敏和不可覆盖规则 |
| Catalog | 接纳通过现有 Bundle 验真的 Plan 0.6 Run；SQLite 仍是可重建派生索引 |
| Workbench | 先只通过通用 Evidence 账册读回；M10 不增加执行按钮或前端新裁决 |
| Comparison | 允许两个同 sealed Plan/Profile 的 M10 Run 使用既有三态比较，Profile SHA 纳入可比性 |
| Pairing/Batch | M10 不扩张其语义；在专门兼容合同出现前对 Plan 0.6 显式拒绝，不能部分解析 |

上述候选决策、字段表与负向矩阵逐条复核后，合同才可升级为 `CONTRACT_FROZEN`。定义、草案或单元
测试都不能替代真实运行；M10 只有全部退出门禁、清理和远端标签读回完成后才能标记 `FROZEN`。

## 18. 设计依据

- [Microsoft：Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Microsoft：AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [Microsoft：JOBOBJECT_BASIC_PROCESS_ID_LIST](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list)
- [Microsoft：GetExtendedTcpTable](https://learn.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getextendedtcptable)

这些来源只证明 Windows API 能力存在，不证明 VeriTrail 已正确实现、正确归属 listener 或完成
清理；代码自动化、真实失败注入、浏览器和无残留验收仍不可替代。
