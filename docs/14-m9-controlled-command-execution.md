# M9 受控项目命令执行合同

> 状态：`IMPLEMENTING / CONTRACT_FROZEN / RUNTIME_BROWSER_VALIDATED / KEYBOARD_PENDING`
> 影响层级：`L3_SYSTEM`（外部进程、信任边界、公共 Plan/Evidence 合同）
> 前置基线：`m8-v0.9.0` 与 `post-m8-plan-v1`
> 实施门禁：实现只能遵循本合同 0.2；改变公共字段、状态、所有权、安全边界或验收矩阵时必须
> 先形成新合同版本并重新冻结

## 1. 目标问题

M9 只回答一个问题：

> 一个封存的 ExperimentPlan 能否在资源预检通过后，解析并展示一个用户明确批准的可信
> `ONESHOT` 进程，以结构化参数直接启动，在有界时间、输出和进程树内完成，生成脱敏且不可变的
> `runtime.command` 证据，证明清理、受监测范围的最终状态漂移及未证明的写活动边界，然后继续
> 消费 M5 已冻结的静态目标、浏览器、裁决和 Bundle 链路？

M9 的增量是“可信一次性进程进入证据链”，不是“任意代码获得安全沙箱”。

M9 不回答：

- 长运行服务、多个进程步骤、依赖图或完整项目自举是否成立；
- npm/Maven/Gradle、`.cmd/.bat`、Docker、中间件或系统服务能否安全编排；
- 不可信仓库、恶意可执行文件或供应链攻击能否被隔离；
- 文件系统、注册表、网络、系统调用或凭据访问是否被操作系统级阻断；
- C2 工作区依赖恢复、C3 主机依赖安装或 Linux/macOS 是否受支持；
- UI 是否可以编辑计划、批准命令、启动/停止 Run 或显示实时终端；
- 计划编辑、在线写、报告发布、远程执行、并行命令或 AI 裁决。

## 2. 前置门禁与范围上浮

- M8 冻结：`m8-v0.9.0`；
- Post-M8 规划冻结：`post-m8-plan-v1`；
- M5 `STATIC_HTTP`、Plan 0.4、`runtime.orchestration` 与 `run` CLI 保持冻结；
- M0–M8 的 Plan、Evidence、Report、Manifest、Catalog、Comparison、Pairing 和 Batch 消费者
  必须保持兼容。

若实现 M9 必须修改以下任何事实，立即停止并回到合同评审：

- M0 Verdict 优先级或 ExecutionStatus/Verdict 分离；
- M1 `PROCEED / STOP_ESCALATION / ABORT` 资源语义；
- M2 浏览器证据或 M5 `STATIC_HTTP` 生命周期语义；
- M4 Bundle 权威、Catalog 派生索引或 M3/M6–M8 只读消费者边界；
- Post-M8 Plan v1 的 `ONESHOT`、Windows-first、C1 或无自由 Shell 边界；
- 从“可信本地进程”扩大为“对恶意代码提供隔离”。

## 3. 影响层级、所有者与消费者

- 声明层级：`L3_SYSTEM`；
- 所有者：Python Core / Trusted Process Runner；
- 冻结合同：ExperimentPlan 0.5、ToolBindings 0.1、CommandPreview 0.1、
  `runtime.command` Evidence 0.1；
- 冻结 CLI：新增 `command-preview`，扩展既有 `run` 接受 Plan 0.5；
- 直接消费者：Plan 校验/Seal、预检、命令审批、进程执行、Evidence 校验、Verdict、Report、
  Manifest 与 CLI；
- 兼容消费者：M0–M8 CLI、M4 Catalog、Vue Workbench 通用 Evidence 账册、Plan 0.1–0.4；
- 后继消费者：M10 本地长运行进程适配器与有界完整项目自举；
- 数据所有权：Plan 决定政策，ToolBindings 只解析本机工具，Preview 绑定本次解析事实，Evidence
  记录观察，规则计算 Verdict；执行器不得直接写 `PASS / FAIL`。

## 4. 威胁模型与诚实声明

### 4.1 M9 防护的风险

- Shell 拼接、隐式变量展开、管道、重定向和命令替换；
- Plan 已封存但运行时解析到另一份可执行文件；
- 参数、工作目录、环境投影或执行政策在预览后漂移；
- 命令无限运行、输出无限增长、等待交互输入或遗留子进程；
- stdout/stderr、错误信息或证据中持久化秘密与个人绝对路径；
- 受监测项目文件的最终状态发生未声明漂移；
- 资源停止、命令失败和业务 Verdict 被压扁成同一状态。

### 4.2 M9 不防护的风险

结构化参数只能证明 VeriTrail 没有调用 Shell 解释这些参数，不能证明目标程序不会把参数当成
自己的脚本、插件、表达式或代码。一个可信解释器、测试框架或构建工具仍可能：

- 读取当前用户有权访问的任意文件或环境；
- 访问网络、注册表、系统 API 或其他进程；
- 在受监测范围外写文件；
- 自行启动未被可靠纳入所有权后端的进程；
- 在输出脱敏前把秘密发送到外部系统。

下表定义 M9 完成全部真实验收后允许作出的**最大声明**，不是当前实现事实：

| 能力 | M9 声明 |
| --- | --- |
| VeriTrail 调用层的 Shell 注入防护 | 真实证明后可 `SUPPORTED` |
| sealed policy 与本机解析漂移检测 | 真实证明后可 `SUPPORTED` |
| 有界 stdout/stderr 与持久化前脱敏 | 真实证明后可 `SUPPORTED` |
| Windows 进程树所有权与清理 | 必须真实证明后才可 `SUPPORTED` |
| Job 活动进程上限强制执行 | 必须真实证明后才可 `SUPPORTED` |
| 每次被 Job 拒绝的进程创建尝试均被 runner 观测 | `NOT_PROVEN` |
| 声明范围内最终状态漂移检测 | 必须真实证明后才可 `SUPPORTED` |
| 命令全程写活动检测 | `NOT_PROVEN` |
| 对手并发替换可执行文件的 TOCTOU containment | `NOT_PROVEN` |
| 文件系统隔离 | `NOT_PROVEN` |
| 网络隔离 | `NOT_PROVEN` |
| 恶意代码 containment | `NOT_SUPPORTED` |
| Linux/macOS 进程控制 | `NOT_PROVEN` |

M9 只能用于用户已经信任并明确批准的本地项目命令。仓库来源、依赖或可执行文件不可信时必须
在进程创建前拒绝，不能把“有结构化参数”描述成“可以安全运行恶意代码”。

## 5. 控制变量设计

### 5.1 基线

基线是 M5 Plan 0.4：预检通过后，不启动外部进程，直接验证并启动内置 `STATIC_HTTP`，完成
真实 Chromium、裁决、Bundle 与清理。

### 5.2 唯一主要变量

`pre_target_command_mode`：

- 基线值：`none`；
- M9 处理值：`veritrail_managed_trusted_process_oneshot`。

### 5.3 受控变量

- 同一代码提交、静态目标字节、浏览器版本、视口和步骤；
- 同一 M1 资源政策、M5 目标政策、断言、Artifact 上限和 Verdict 规则；
- 固定 Windows 11、C1、单命令、单目标、单浏览器链、串行执行；
- 相同 ToolBindings、解析后可执行文件摘要、参数、工作目录、环境名称、环境投影摘要和审批摘要；
- 相同受监测根、文件/字节上限、输出上限、超时和清理断言。

### 5.4 干扰与观察者效应

- Windows 调度、杀毒扫描、文件索引、运行时冷启动和进程退出延迟；
- 命令输出捕获线程、进程树监测、文件指纹与脱敏的 CPU/内存/磁盘开销；
- 工具运行时自己的缓存、临时文件和已安装依赖状态；
- ToolBindings 指向的本机可执行文件更新时间或安全软件注入。

这些事实进入 EnvironmentSnapshot 和适用边界，不能观察后改成第二个主要变量。

## 6. M9 最小纵向范围

1. 新增向后兼容的 ExperimentPlan 0.5；
2. Plan 0.5 在完整 Plan 0.4 上新增**恰好一个** `command`；
3. 新增只读 `command-preview`：校验/Seal Plan、读取 ToolBindings、解析可执行文件并生成审批摘要，
   但不创建目标进程；
4. Plan 0.5 的 `run` 必须接收与实时解析完全一致的审批摘要；
5. 预检只有 `PROCEED` 才能进入命令执行；
6. 命令为 `TRUSTED_PROCESS_ONESHOT`、无 stdin、无 TTY、无 Shell、单工作目录；
7. 命令正常完成且没有阻断性污染后，继续走 M5 `STATIC_HTTP -> browser -> evaluate -> Bundle`；
8. 非零退出、超时、中止、输出超限、污染或清理异常都形成 `runtime.command` 证据；
9. 进程树、捕获线程、临时工作区和 staging 必须按所有权清理；用户项目文件不得自动回滚或删除；
10. Catalog 与 Workbench 只通过现有通用接口读回 Plan 0.5 Bundle，不增加 M9 特殊裁决或控制台。

### 明确不做

- 多命令序列、DAG、并行、重试、长运行服务、就绪探针和多端口生命周期；
- `cmd.exe`、PowerShell/pwsh、`sh/bash/zsh`、WSL 或自由 Shell 字符串；
- Python `-c`、Node `-e/--eval` 及其他内联代码入口；
- `.cmd/.bat`、npm、Maven、Gradle、Docker、Git hook、系统服务或提权工具；
- 自动安装/升级依赖、修改 PATH/代理/注册表/防火墙/系统服务或全局包；
- 自动撤销项目文件变化、全局杀进程、全局端口清理或删除来源不明的资源；
- 将结构化 runner 宣称为文件系统/网络/恶意代码沙箱；
- M10、M11、前端终稿或最终系统审查能力。

## 7. ExperimentPlan 0.5 冻结合同

Plan 0.5 保留 Plan 0.4 全部字段与语义，只新增必填 `command`。冻结形状：

```json
{
  "schema_version": "0.5",
  "command": {
    "adapter": "TRUSTED_PROCESS_ONESHOT",
    "command_id": "python-unit-check",
    "purpose": "run the sealed Python unit-test entry point",
    "project_profile_id": "veritrail-self-check",
    "tool_binding": "python",
    "arguments": [
      { "literal": "-m" },
      { "literal": "unittest" },
      { "literal": "discover" },
      { "literal": "-s" },
      { "literal": "tests" }
    ],
    "working_directory": ".",
    "environment": {
      "inherit": ["SYSTEMROOT", "WINDIR"],
      "set": { "PYTHONDONTWRITEBYTECODE": "1" }
    },
    "stdin": "CLOSED",
    "timeout_ms": 300000,
    "descendant_exit_grace_ms": 2000,
    "expected_exit_codes": [0],
    "max_stdout_bytes": 1048576,
    "max_stderr_bytes": 1048576,
    "max_processes": 16,
    "write_policy": "RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES",
    "subject_watch_roots": ["src", "tests"],
    "max_watch_files": 2000,
    "max_watch_total_bytes": 67108864,
    "network_policy": "NOT_REQUIRED_NOT_ENFORCED"
  }
}
```

### 7.1 通用约束

- `command_id`、`project_profile_id`、`tool_binding` 使用稳定小写标识，不包含路径、账号或机器名；
- `purpose` 是有界非秘密说明；`project_profile_id` 在 M9 只绑定当前 Subject 与命令政策，不引入
  M10 的工具/端口/服务生命周期 Profile；
- M9 每个 Plan 只能有一个 command，`adapter` 只能是 `TRUSTED_PROCESS_ONESHOT`；
- `working_directory` 是 subject-root 下安全的相对 POSIX 路径；允许精确的 `.` 表示 subject-root，
  其他路径禁止绝对路径、盘符、反斜杠、空段、`.`/`..` 段、symlink、junction 和 reparse point；
- `arguments` 1–128 项，每项只能是 `literal` 或受限的 `run_work_path`，不能同时包含两者；
- `literal` 是单个 argv 元素，不做 glob、变量、引号、转义或 Shell 解释；控制字符、NUL、秘密、
  账号/机器标识和个人绝对路径拒绝；
- `run_work_path` 只允许 1–8 段安全相对路径，由 runner 转换为当前 Run 临时工作区内的绝对路径；
- Plan、Preview、Evidence 和终端 JSON 不持久化该绝对路径；
- stdin 固定关闭，不支持交互确认、密码输入、TTY 或继承控制台输入；
- timeout 1–900 秒；后代正常退出窗口 0.1–10 秒；stdout/stderr 各 1 B–1 MiB；
- 允许退出码是唯一、排序的 0–255 整数；process 上限 1–32；
- 监测根 1–8 个，均在 subject-root 内且互不重叠；单 Run 指纹上限 2000 文件、64 MiB；
- 0.5 Seal 覆盖完整 command 政策。任何参数、环境、上限、监测根或期望退出码变化都产生新
  Plan 哈希。

### 7.2 环境边界

- 子进程从最小环境开始，只继承 Plan 明确列出的非秘密变量；
- M9 首片允许继承名固定为 `SYSTEMROOT` 与 `WINDIR`，键按 Windows 大小写不敏感语义规范化并
  拒绝重复；`TEMP`/`TMP` 由 runner 指向 Run work，不继承用户路径；
- 后续扩充允许集合必须先证明必要性；名称含 token、secret、password、key、credential、cookie、
  auth、proxy 等敏感含义的变量一律拒绝；
- `environment.set` 不接受任意键值。M9 首片固定只允许
  `PYTHONDONTWRITEBYTECODE=1`；Node 正向 Plan 使用空 `set`。解释器加载路径、启动选项、代理、凭据、
  动态库和用户目录相关变量均拒绝；扩表必须修改并重新冻结合同；
- Post-M8 Plan v1 提到的秘密值透传是后继上界，不是 M9 首片义务；M9 0.2 明确不接受秘密环境值，
  将来若需要必须另立秘密来源、单向注入、预览和脱敏合同；
- Preview 与 Run 都从当前父进程解析允许继承变量的**实际值**，对规范化后的完整环境投影计算
  SHA-256；Approval 必须绑定该摘要，Run 前漂移即拒绝 spawn；
- 环境投影按键排序，区分 inherited/set/runner 三类；inherited 与 set 绑定传给子进程的实际值，
  runner 路径值规范为稳定的 `<RUN_WORK>` 语义占位符；
- CommandPreview、Evidence 与日志只保存环境变量名称和投影摘要，不保存环境原值；SHA-256 不等于
  脱敏，低熵个人值仍可能被猜测，因此 M9 必须先用上述固定集合排除账号、个人路径与秘密，而不是
  依赖哈希掩盖它们；
- runner 注入的实际绝对路径不进入 Plan、Preview、Evidence 或日志；
- 不默认继承完整父进程环境，不读取或解析 `.env`；
- 子进程继承环境值无法构成恶意程序隔离；M9 仍只接受可信命令。

### 7.3 required_evidence 与断言

Plan 0.5 必须要求且各只允许一份：

- `runtime.preflight`；
- `runtime.command`；
- `runtime.orchestration`；
- `browser.session`。

Plan 必须至少定义一个针对 `runtime.command` 的 `HARD` 或 `DEGRADATION_BOUNDARY` 断言，并继续
满足 Plan 0.4 的 preflight、orchestration 和 browser 断言。退出码、输出、清理和最终状态漂移事实由
断言解释；runner 不直接写 Verdict。

Plan 0.1–0.4 的 Schema、Seal、CLI 行为和冻结示例必须保持兼容。

## 8. ToolBindings 0.1 与本机解析

Plan 只保存逻辑 `tool_binding`，不保存个人绝对路径。调用者通过本地、Git 忽略的 ToolBindings
文件声明具体可执行文件；冻结形状：

```json
{
  "schema_version": "0.1",
  "bindings": {
    "python": {
      "executable": "<local absolute path>"
    }
  }
}
```

约束：

- ToolBindings 是本机输入，不进入 Bundle、Artifact、Git 或普通报告；
- M9 Windows 首片只接受普通 `.exe`，拒绝 `.cmd/.bat`、目录、链接、reparse point 和设备路径；
- 可执行文件解析后记录 basename、大小、SHA-256 和脱敏路径摘要，不记录原绝对路径；
- Preview 与 Run 都重新打开并计算身份；摘要不一致时在 spawn 前拒绝；
- Run 在进程结束后再次核对可执行文件身份；发生变化时结果为 `INCONCLUSIVE`，不能 `PASS`；
- ToolBindings 不提供信任证明。用户仍负责确认工具来源；哈希只提供采样时点的身份稳定性，不能
  排除校验与创建进程之间的对手并发替换，也不能构成 TOCTOU containment。

## 9. CommandPreview 0.1 与显式批准

冻结 CLI：

```powershell
veritrail command-preview `
  --plan <plan-0.5.json> `
  --subject-root <project-root> `
  --tool-bindings <local-bindings.json>

veritrail run `
  --plan <plan-0.5.json> `
  --subject-root <project-root> `
  --tool-bindings <local-bindings.json> `
  --approve-command <preview-sha256> `
  --run-id <unique-id> `
  --output <new-output>
```

Preview 必须：

- 只读校验/Seal Plan，解析工作目录、ToolBindings、参数和监测范围；
- 不创建目标进程，不执行 `--version`，不写项目和 Artifact；
- 展示命令 ID、脱敏可执行文件身份、argv 边界、相对工作目录、环境变量名称、环境投影摘要、
  上限、写策略、未证明的隔离边界和预计副作用；
- 生成规范化 CommandPreview 与 SHA-256；
- Approval 摘要覆盖 Plan seal、完整 command policy、解析后可执行文件身份、规范工作目录、环境
  名称、环境投影摘要和监测范围，但不包含原绝对路径或环境原值；
- stdout 只输出结构化、脱敏 JSON，stderr 不输出 traceback 或个人路径。

`run` 必须实时重建相同 Preview。缺少批准、摘要不匹配、工具身份漂移、环境投影漂移或政策漂移
时，命令退出 2，不启动子进程、不创建 Run Bundle、不改动项目。

批准只确认“按屏幕所示运行这一个可信命令”，不表示用户授权任意后继进程、系统修改或未声明
副作用。

## 10. 执行顺序与状态语义

```text
VALIDATE / SEAL
  -> PREFLIGHT
      -> ABORTED/PENDING                  (ABORT)
      -> COMPLETED/PENDING                (STOP_ESCALATION)
      -> RESOLVE / REBUILD PREVIEW        (PROCEED)
          -> APPROVAL MISMATCH             (reject before Run)
          -> SUBJECT SNAPSHOT
          -> SPAWN / CAPTURE / REAP
              -> ACCEPTED EXIT -> SUBJECT DIFF -> M5 TARGET / BROWSER
              -> UNEXPECTED EXIT -> SUBJECT DIFF -> EVALUATE / BUNDLE
              -> TIMEOUT/CANCEL/LIMIT -> TERMINATE JOB -> SUBJECT DIFF -> EVALUATE / BUNDLE
              -> SPAWN ERROR -> CLEANUP -> EVALUATE / BUNDLE
          -> ARTIFACT FINALIZE / EVALUATE / ATOMIC BUNDLE
```

上述是内部编排阶段，不替代公共 ExecutionStatus。

- Plan、ToolBindings、路径或审批校验失败：CLI 退出 2，不创建进程或 Run；
- 预检 `ABORT`：`ABORTED/PENDING`，没有 `runtime.command`，进程从未启动；
- 预检 `STOP_ESCALATION`：`COMPLETED/PENDING`，没有 `runtime.command`，进程从未启动；
- 进程按允许退出码结束且所有清理/最终状态门通过：继续 M5 链，最终 Verdict 由全部断言决定；
- 进程正常退出但退出码不在允许集合：ExecutionStatus 可以是 `COMPLETED`；命令硬断言可以形成
  `FAIL`，不能把项目测试失败误记为 runner `ERROR`；
- spawn 或所有权后端异常：`ERROR/PENDING`，除非已有独立硬失败证据；
- 用户取消、超时、输出硬限或已被 collector 观察到的资源硬限触发：ExecutionStatus 为
  `ABORTED`；无独立硬失败证据时
  Verdict 为 `PENDING`；
- 根进程以允许退出码结束，但已拥有后代未在 `descendant_exit_grace_ms` 内自行退出：终止本 Run
  Job；ExecutionStatus 保持 `COMPLETED`，`oneshot_quiescent` 硬断言形成 `FAIL`；
  `cleanup_complete` 可在 Job 回收成功后为 true，但不能抹掉命令遗留后代的事实；
- 监测范围最终状态漂移、可执行文件后验身份变化或无法解释的运行后环境漂移：`INCONCLUSIVE`，不得自动回滚
  或删除用户文件；
- 进程树、捕获线程、临时工作区或 staging 清理失败：不得 `PASS`，残留必须可见；
- Bundle 继续使用 staging + 原子 rename，已有 output/Run ID 永不覆盖。

## 11. Windows 进程所有权与清理 ADR-0001

冻结决策是使用 Windows Job Object 作为 M9 的进程所有权边界，调用层锁定为项目虚拟环境内的
`pywin32==312`。依赖与后端的当前实施事实只以第 19 节记录为准；能力缺失时必须关闭失败。

### 11.1 依赖决策

- 实现阶段在 `pyproject.toml` 新增 Windows 专用可选依赖组
  `command-windows = ["pywin32==312; sys_platform == 'win32'"]`；既有 core/browser 安装与 M0–M8
  行为不得被迫引入它；
- `command-preview` 与 Plan 0.5 `run` 缺少该依赖时必须在创建目标前给出稳定 capability error，
  不自动安装、不降级为 `ctypes`/普通 `Popen`，Plan 0.1–0.4 保持可用；
- 只安装在分别对应 Python 3.10/3.13 的 Git 忽略项目虚拟环境，不执行 `pywin32_postinstall`，
  不写全局 Python、注册表或 System32；
- PyPI 312 提供本机 CPython 3.10/3.13 Windows AMD64 wheel；实施验收必须再次从索引读取文件名、
  大小和 SHA-256，并与下表冻结值一致，否则停止实施并重新审查依赖：

| Python | wheel | bytes | SHA-256 |
| --- | --- | ---: | --- |
| 3.10 | `pywin32-312-cp310-cp310-win_amd64.whl` | 6926780 | `5dbc35d2b5320dc07f25fa31269cfb767471002b17de5eb067d03da68c7cb2db` |
| 3.13 | `pywin32-312-cp313-cp313-win_amd64.whl` | 6914298 | `c53e878d15a1c44788082bfe712a905433473aa38f86375b7cf8b45e3acbaaf9` |

PyPI 将该发行版标记为 Python Software Foundation License；VeriTrail 不复制或修改 pywin32
源码。发行元数据或许可证事实变化时停止实施并重新审查，不能自动换版本。

### 11.2 必须成立的创建顺序

1. 创建本 Run 独占的 Job Object；
2. 在 Job 上设置 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`、`JOB_OBJECT_LIMIT_ACTIVE_PROCESS` 和
   sealed `max_processes`，不允许 breakaway；
3. 直接以 `CREATE_SUSPENDED` 创建目标 `.exe`，保留 process/thread handles；
4. 在首线程执行任何目标代码前把进程分配给 Job；分配失败时终止仍暂停的目标并关闭所有句柄，
   记录 `process_created=true`、`target_resumed=false` 与稳定错误，形成 `ERROR/PENDING`，禁止无 Job
   降级运行；
5. 分配成功后才 `ResumeThread`，并发排空 stdout/stderr；
6. 根进程正常退出后，在 `descendant_exit_grace_ms` 内等待已拥有后代自行结束；仍有存活成员时
   终止整个 Job；
7. 超时、取消、输出硬限或 collector 已观察到的资源硬限触发时直接终止本 Run 的 Job，再等待并证明成员、管道线程
   与句柄全部释放；
8. 最后关闭 Job handle；`KILL_ON_JOB_CLOSE` 是异常路径的最后所有权保险，不是唯一清理步骤。

先普通 `Popen`、后补分配 Job 存在目标进程先行执行/派生的竞态，不满足 M9。M9 也不使用
`CREATE_BREAKAWAY_FROM_JOB`。Windows 普通控制台进程没有统一、可靠且不波及外部进程的温和终止
协议，因此 M9 不承诺泛化的“先发优雅信号”；有界 grace 只用于根进程正常退出后的已拥有后代。

### 11.3 嵌套 Job 与本机预检

Windows 8 及以后允许满足约束的嵌套 Job，但 Codex/PowerShell 宿主自身可能已经在 Job 中。
2026-08-11 实施前只读探针曾观察到宿主差异；实施后两个项目虚拟环境均已用锁定 wheel 完成真实
暂停创建、Job 分配、恢复与清理自动化。该结果只证明当前 Windows 主机上的后端切片，不替代
Plan 0.5 `run` 或完整真实命令验收。

实现必须在目标执行前：

- 调用 `IsProcessInJob` 记录当前进程是否已有上层 Job；
- 创建本 Run Job 并验证必要 limit 能设置；嵌套兼容性的决定性检查仍是按 11.2 把暂停目标分配
  进去；
- 将嵌套/分配不兼容作为稳定 ownership error，保持 `ERROR/PENDING`，证明目标代码从未恢复执行；
- 不以普通 `Popen`、PID 轮询、进程名匹配或全局端口清理作为回退。

### 11.4 所有权验收能力

后端必须能够：

- 直接创建目标进程而不经过 Shell；
- 在目标执行用户权限内运行，不请求管理员/UAC 提权；
- 把目标及其后代纳入本 Run 的所有权范围；
- 同时排空 stdout/stderr，避免管道背压死锁；
- 正常结束后等待全部已拥有后代退出；
- 超时/取消/硬限制时只终止本 Run 的 Job；
- 不按名称、模糊命令行或全局端口杀进程；
- 记录已启动/观察/终止/残留数量，但不持久化个人命令行或不必要 PID；
- 最终证明捕获线程、句柄、临时目录、staging 和已拥有进程树清理。

是否“纯标准库”不是冻结标准；可靠所有权、可证伪失败和不产生 jobless 竞态才是标准。

`JOB_OBJECT_LIMIT_ACTIVE_PROCESS` 负责强制“同时活跃进程不超过 `max_processes`”。M9 使用 Job
accounting 记录累计分配数和最终查询时的活动数，但不引入 completion port，也不把采样冒充精确
峰值，因此不能声称看见目标程序每一次被 Windows 拒绝的创建尝试。Evidence 必须分开记录
`active_process_limit_enforced` 与 `process_limit_attempt_observation=NOT_PROVEN`。前者只有在 limit
设置成功并读回一致后才能为 true；不得把前者扩张成后者。

## 12. 项目最终状态漂移与副作用边界

M9 不具备 OS 文件系统沙箱。首个切片使用“声明 + 检测 + 阻止结论扩张”：

- 运行前对每个 `subject_watch_root` 做普通文件、链接、大小和 SHA-256 有界快照；
- 运行后用同一规则复算，报告最终新增、删除、修改、链接变化和无法读取；
- 快照超限或采集失败时不启动进程；
- `RUN_WORK_ONLY_DETECT_SUBJECT_CHANGES` 表示命令应只写 Run 临时区，但这是合同要求，不是内核
  强制；
- 监测根最终状态发生漂移时记录污染并阻止因果 `PASS`；VeriTrail 不替用户删除、覆盖或回滚文件；
- 前后指纹只证明采样时点的最终状态差异，不能证明命令没有“写入后恢复”的瞬时写活动；
- 未列入监测根的 subject 路径、subject-root 外部、NTFS Alternate Data Streams 及文件系统元数据均
  明确为未观测；Evidence 固定记录 `write_activity=NOT_PROVEN`；
- Run 临时区必须由 VeriTrail 创建、确认所有权并在证据附件转存后清理；
- 计划要求的构建产物只能写到 typed `run_work_path`；M9 不把产物复制回项目；
- 如果真实命令不能在这个边界内运行，应留给 M10/C2 的隔离工作区合同，不能放宽 M9。

## 13. 输出、脱敏与 Evidence 0.1

stdout 和 stderr 分开捕获为有界附件；不合并顺序，也不把终端彩色控制序列、退格或伪造日志行
直接当作可信结构化事实。持久化前执行流式/最终双重脱敏；原始未脱敏输出不得落盘。

任一流读到超过 sealed 上限的第一个字节时立即终止本 Run Job，形成 `ABORTED/PENDING`。附件最多
保存脱敏后的上限内前缀；`observed_bytes_lower_bound` 记录终止前已读数量，不能冒充完整原始输出
大小。正常退出后遗留后代则按第 10 节形成 `COMPLETED/FAIL`，与输出超限分开。

`runtime.command` 0.1 至少记录：

- collector/version、Plan seal、command policy SHA-256、Preview SHA-256；
- command ID、adapter、tool binding ID、可执行 basename/size/SHA-256 与脱敏身份摘要；
- argv 个数与规范化参数摘要；敏感值和运行时绝对路径不重复保存；
- 相对工作目录、继承/设置的环境变量**名称**、`environment_projection_sha256`、stdin/TTY/Shell
  事实；
- started/ended/elapsed、process_created、target_assigned、target_resumed、exit_code、exit_expected、
  termination_reason；
- stdout/stderr `observed_bytes_lower_bound`、stream_complete、持久化字节计数、截断/超限、脱敏计数
  和附件哈希；只有 stream_complete=true 时观察计数才可解释为完整输出大小；
- 进程所有权后端、观察进程数、正常/强制终止数、tree_released；
- active process limit、total assigned processes、final active processes、`active_process_limit_enforced`、
  `process_limit_attempt_observation=NOT_PROVEN`；
- subject snapshot policy/fingerprint、差异计数、`final_state_drift_detected`、snapshot_complete、
  `write_activity=NOT_PROVEN`；
- run work 创建/释放、捕获线程停止、句柄释放、cleanup_complete；
- collector RSS before/peak/delta、资源/观察者错误和稳定 error type；
- 明确元数据：`shell_used=false`、`structured_arguments=true`、
  `filesystem_isolation=NOT_PROVEN`、`network_isolation=NOT_PROVEN`、
  `executable_toctou_containment=NOT_PROVEN`、`untrusted_code_containment=NOT_SUPPORTED`。

Evidence 校验器必须拒绝缺字段、额外字段、政策哈希错误、Preview 漂移、计数/附件不一致、原绝对
路径、未脱敏秘密、自相矛盾状态和重复 `runtime.command`。`cleanup_complete=false`、未解释最终漂移
或身份漂移必须阻止 `PASS`。

## 14. 控制组与证伪矩阵

| 组 | 唯一变化 | 预期事实 |
| --- | --- | --- |
| M5 基线 | 无 command | 既有 Plan 0.4 字节/行为兼容 |
| Python 正向 | 可信 Python module ONESHOT | 允许退出、最终状态无漂移、继续 M5 链 |
| Node 正向 | 可信 node.exe script ONESHOT | 独立 Run 证明第二命令家族 |
| 缺少批准 | 无/错误 Preview SHA | spawn 前拒绝、0 Run |
| 工具漂移 | Preview 后替换绑定身份 | spawn 前拒绝；后验漂移为 `INCONCLUSIVE` |
| Shell/内联代码 | shell、`.cmd/.bat`、`-c/-e` | Plan/Preview 拒绝 |
| 非零退出 | 退出码不在允许集合 | `COMPLETED` 与命令断言 `FAIL` 可并存 |
| spawn 失败 | 文件不存在/不可执行 | `ERROR/PENDING`，形成有界证据 |
| 超时 | 超过 sealed timeout | `ABORTED/PENDING`，进程树回收 |
| 用户取消 | 执行中取消 | `ABORTED/PENDING`，证据与清理保留 |
| 输出超限 | stdout 或 stderr 首次超过 sealed 上限 | `ABORTED/PENDING`、终止 Job、有界脱敏前缀 |
| 秘密 canary | 输出含测试秘密/路径 | 原值不落盘，脱敏事实可见 |
| subject 最终漂移 | 修改受监测普通文件且保留变化 | `INCONCLUSIVE`，不回滚用户文件 |
| 瞬时写后恢复 | 修改后恢复原字节与类型 | 最终指纹可相同；`write_activity=NOT_PROVEN`，不得声称无写入 |
| 正常退出后代残留 | helper 根进程允许退出、后代超过 grace | Job 回收成功仍为 `COMPLETED/FAIL` |
| Job 回收失败 | helper 创建长存后代且回收失败 | 不得 `PASS`，残留事实可见 |
| 活动进程上限 | helper 尝试超过 sealed cap | cap 强制成立；不声称观测每次被拒绝尝试 |
| 外部同名进程 | 预先存在同名程序 | 不接管、不停止、不计入本 Run |
| 预检 ABORT/STOP | 只改变资源阈值 | 0 spawn，无 `runtime.command` |
| 重复 Run | output 或 Run ID 已存在 | 拒绝覆盖原 Bundle |

正向不能替代负向，模拟 helper 不能替代至少两种真实工具，自动化进程树不能替代 Windows 真实
残留核验。

## 15. 自动化门槛

- Plan 0.5 Schema、Seal、篡改、unknown field、Plan 0.1–0.4 字节兼容；
- ToolBindings 路径类型、普通 `.exe`、链接/reparse、身份摘要和 Preview/Run 漂移；
- 参数边界、typed run path、工作目录、环境投影摘要、秘密拒绝、漂移拒绝和审批摘要确定性；
- shell/`.cmd/.bat`/inline code、stdin/TTY、超时、输出、进程数和监测上限；
- 正常/非零/spawn error/timeout/cancel/output overflow 的状态与 Verdict 分离；
- stdout/stderr 并发排空、脱敏、控制字符、有界附件、哈希和 Manifest；
- suspended 分配、嵌套 Job、子进程树正常退出、Job 强制回收、外部同名进程保护和清理失败；
- subject 前后快照、最终状态漂移、瞬时写未证明、快照超限、Run work 与 staging 清理；
- `runtime.command` 严格校验、重复证据、政策/Preview 漂移和 Verdict；
- M0–M8 全量回归、Catalog 接纳 Plan 0.5、Workbench 通用读回；
- 两套 Python、前端 lint/test/build、依赖与敏感扫描；worker 数遵守 16 GB 资源策略。

自动化通过最多推进到 `AUTOMATED`，不能替代真实进程、浏览器或清理证据。

## 16. 真实运行退出条件

实现阶段开始前必须从本机机器档案和实时状态确定工具路径、版本、资源和端口。真实运行串行完成：

1. 在 Windows 11/C1 上用两个独立 Plan/Run 分别执行可信 Python module 与直接 `node.exe`
   script；不使用 npm、`.cmd`、Shell 或内联代码；
2. 每个正向 Run 都完成 preflight、审批一致性、ONESHOT、subject 最终状态无漂移、M5 静态目标、桌面/移动
   Chromium、Verdict、Bundle 和清理；
3. 真实运行非零退出、超时/取消、秘密 canary、受监测文件变化和长存子进程等适用负向；
4. Bundle 由 Catalog 建索引并被现有 Workbench 通用读回，不增加 M9 特殊 UI；
5. Codex 内置浏览器检查正/负/损坏恢复、桌面/移动、键盘、Console/Network、Evidence 与状态分维；
6. 重复正向 Run 生成可比较证据；只有语义适用时才使用 Comparison，不强制 Pairing/Batch；
7. 两套 Python、全部自动化、前端生产构建、依赖审计和敏感扫描通过；
8. 结束后所有 M9 子进程、捕获线程、句柄、临时工作区、Chromium、端口和 staging 全部释放；
9. 记录 VeriTrail 与命令进程的资源事实，超过停止线保持 `PENDING`，不降低清理/安全标准；
10. 冻结提交和 tag `m9-v0.10.0` 从 GitHub 远端读回，工作区只含预期忽略证据。

两种工具只证明 M9 合同对这两个真实命令家族成立，不自动证明 npm、Maven、Docker、其他平台或
不可信代码。任何必需真实链无法完成时，M9 保持真实中间状态，不得标记 `FROZEN`。

## 17. 合同冻结审查结论

0.2 冻结审查已经确认：

- 可信命令与恶意代码边界没有使用“沙箱”式夸大表述；
- Plan 0.5 只有一个 ONESHOT，不侵入 M10 长运行生命周期；
- ToolBindings、Preview 和 Approval 能固定采样时点的本机解析与环境投影，而不持久化个人路径或
  环境原值，也不夸大为 TOCTOU containment；
- Windows Job Object + `pywin32==312` 后端有无 jobless 竞态的创建顺序、嵌套预检、锁定 wheel
  和可证伪失败语义；
- 项目副作用采用 Run work + 最终状态监测 + 漂移阻断，不把前后指纹夸大成全程写活动证明，
  不自动删除用户文件；
- ExecutionStatus 与 Verdict 在全部异常路径上保持分离；
- M5 `STATIC_HTTP`、浏览器、Bundle 和旧消费者保持兼容；
- 自动化矩阵与真实运行矩阵都包含正向、失败、中止、最终状态漂移、清理和秘密 canary；
- M9 没有借“通用命令”加入 Shell、包管理器、Docker、服务、自举或前端控制台；
- 16 GB 主机保持串行，资源不足只能形成 `PENDING`。

本合同冻结只允许 M9 进入实现，不代表任何代码、依赖安装、运行或安全主张已经成立。

## 18. 冻结依据

- [Microsoft：Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Microsoft：AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [Microsoft：Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)
- [Microsoft：Process Creation Flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags)
- [pywin32：win32process.CreateProcess](https://mhammond.github.io/pywin32/win32process__CreateProcess_meth.html)
- [pywin32：win32job](https://mhammond.github.io/pywin32/win32job.html)
- [PyPI：pywin32](https://pypi.org/project/pywin32/)

这些来源只证明 API/分发事实存在，不证明 VeriTrail 已正确调用，也不替代本机负向运行与残留核验。

## 19. 合同记录

- 合同版本：M9 Controlled Project Command Execution Contract 0.2；
- 目标 Plan：ExperimentPlan 0.5；
- 目标本机输入：ToolBindings 0.1；
- 目标 Preview：CommandPreview 0.1；
- 目标 Evidence：`runtime.command` 0.1；
- 目标 CLI：`command-preview` 与扩展 `run`；
- 目标版本：Python Core `0.10.0.dev1`，Workbench `0.10.0-dev.1`；
- 目标冻结标签：`m9-v0.10.0`；
- 当前里程碑状态：`IMPLEMENTING / RUNTIME_BROWSER_VALIDATED / KEYBOARD_PENDING`；
- 当前合同状态：`CONTRACT_FROZEN`；
- 当前实现事实：`4d2bc84` 已完成 Plan 0.5、ToolBindings 0.1、CommandPreview 0.1 与只读
  `command-preview` CLI；`9f979c8` 已完成 `pywin32==312` Windows Job Object 后端、暂停分配、
  直接无 Shell 启动、并发有界输出、超时/取消/输出超限/后代 grace 清理和活动进程上限读回；
  `fa27b51` 已完成审批一致的 Plan 0.5 `run`、运行前后 subject 有界快照、owned Run work、双重
  输出脱敏、严格 `runtime.command`、状态/Verdict 分离，以及 Bundle、Catalog、只读 API 与
  Workbench 通用 Evidence 读回自动化；`9031719` 已增加两个独立轻量 Subject 和串行真实验收器，
  不扩张为包管理器、服务或完整自举；
- 当前隔离边界：锁定版本的 pywin32 `STARTUPINFO` 不提供 `STARTUPINFOEX` 句柄白名单，重定向标准
  句柄仍需 Windows 句柄继承；因此该后端不声明通用句柄能力隔离，仍只允许用户已信任的命令；
- 当前自动化事实：CPython 3.10.6 与 3.13.13 各有 150 项测试通过；因单次执行器约 30 秒截止，
  每个解释器都按固定的 65 + 63 + 22 三片串行执行同一全集。Windows helper 与 Plan 0.5 CLI
  覆盖正常退出、非零退出、spawn error、超时、取消、输出超限、subject 漂移、秘密 canary、
  typed Run work、分配/恢复失败、活动进程上限、后代回收和外部同名进程保护；Workbench 54 项
  测试、lint、type-check 与生产构建通过；两套 Python `pip check` 通过，生产依赖 `npm audit`
  通过；测试后 helper、约定端口和仓库顶层 VeriTrail 临时目录残留均为 0；
- 当前真实运行事实：2026-08-11 的最终 `r4` 矩阵在 Windows 11/C1 上串行完成 8 个 Run。Python 与
  Node 两个独立正向 Plan 均为 `COMPLETED/PASS` 并完成 M5 静态目标、1280×720/390×844 Chromium、
  四层 Evidence、Bundle 与清理；同 sealed Python Plan 复跑生成 `MATCH`。非零为
  `COMPLETED/FAIL`，超时为 `ABORTED/PENDING`，最终状态漂移为
  `COMPLETED/INCONCLUSIVE` 且未回滚项目文件，长存后代在 grace 后被 Job 回收并保持
  `COMPLETED/FAIL`；秘密 canary 原值未进入 Bundle，stdout 记录一次脱敏；
- 当前 Catalog/Workbench 事实：最终 `r4` Catalog 接纳 8/8 Bundle、0 issue、0 duplicate；Codex
  内置浏览器已读回最终 r4 的 Python 正向与超时 Run，并在同一构建上检查 Node 正向、漂移、损坏
  包隔离/恢复、桌面与 390×844 移动视口。页面 Console 为 0；已观察资源全部属于
  `http://127.0.0.1:18770`，包含 `runtime.command`；HTTP 补证为 Catalog GET/HEAD 200、POST 405、
  未知查询 400、命令文本附件 GET 200；桌面/移动文档横向溢出均为 0；
- 当前资源与回归事实：`r4` 的两个 sealed target 端口、owned process、Run work 与 staging 残留均
  为 0；CPython 3.10.6 与 3.13.13 再次各以 65 + 63 + 22 三片通过 150 项，Workbench 54 项、lint、
  type-check、生产构建、两套 `pip check` 与官方 npm registry audit 均通过。敏感候选复核只有真实
  canary 夹具及其 `[REDACTED]` 断言，不含真实秘密、个人绝对路径或账号；
- 保留的失败事实：实现期间自动化曾暴露根进程或后代退出与输出超限观察之间的两条竞态，修复后
  已加入回归；本轮 `r1` 因验收器错误要求连非秘密 Authorization 字段名也消失而停止，`r2` 因读取
  Comparison 的字段名错误而停止，均保留且由全新目录完整复跑修正。首次通过控制台入口启动浏览器
  验收服务器时，终端中断只结束 Windows launcher、遗留精确可识别的 Python 子进程；该进程已按
  PID 与完整任务命令双重核验后停止，最终服务改用直接 `python -m veritrail`，不得把启动器退出
  冒充端口已释放；
- 当前未完成事实：Codex 内置浏览器的合成与系统 `Tab/Enter` 没有移动或激活当前焦点，不能冒充
  物理键盘通过；最终浏览器服务仍为这项人工检查有意保留。人工键盘后还需释放服务、复核全部端口/
  进程/临时目录，提交本文档并从 GitHub 远端读回冻结提交与 `m9-v0.10.0` 标签；
- 当前运行结论：M9 已取得真实命令、真实 Chromium、Catalog/Workbench 与适用负向证据，但物理
  键盘、最终清理和远端冻结门禁未闭合；状态保持 `KEYBOARD_PENDING`，不构成 `FROZEN` 或超出合同
  两个可信命令家族的通用 `SUPPORTED` 声明。
