# VeriTrail Starter 0.1 `single-webapp` Contract

> 状态：`CONTRACT_FROZEN / S0_COMPLETE / S1_COMPLETE`
>
> 消费基线：`VeriTrail Core >=0.12,<0.13`
>
> 影响层级：独立入口包 `L3_SYSTEM`；不修改 Core 公共契约

## 1. 目标

Starter 0.1 把一个明确属于支持矩阵的单节点本地 Web 项目，转换成可人工复核、可由 Core 验证的
Profile/Plan 草案。它解决“怎么正确开始写合同”，不解决“怎么自动证明项目通过”。

## 2. 输入权威

`init` 的唯一权威输入是显式 Answers 0.1 JSON。自动发现只写入 doctor 候选报告，不能静默进入草案。

Answers 采用严格嵌套字段；至少包含：

- `subject.root`：用户选择的项目根目录；
- `application.executable`：可信可执行文件的本机引用；
- `application.arguments`：逐项分隔的结构化参数数组；
- `subject.working_directory`：受 subject root 约束的目录；
- `application.port`、`application.health_path` 和预期 HTTP 状态；
- `browser.start_url` 与 `browser.allowed_origin`；
- `browser.viewports` 中精确的桌面和移动 viewport；
- 至少一个用户确认的业务断言；
- `subject.watch_roots`、输出上限、进程/内存预算和生命周期超时；
- 明确的 `browser.screenshot_safety` 选择。

答案文件不得包含 Token、Cookie、Authorization、私钥、数据库密码或 `.env` 值。需要秘密才能启动的
项目在 0.1 中为 `UNSUPPORTED`。

## 3. Workspace 输出

成功的 `init` 原子创建新目录：

```text
.veritrail/
  starter-manifest.json
  answers.snapshot.json
  profile.draft.json
  plan.draft.json
  tool-bindings.local.json
  REVIEW.md
  handoff.ps1
```

约束：

- `starter-manifest.json` 固定 `authoring_state=DRAFT`、`seal_state=NOT_SEALED`、Preset 版本和输入摘要；
- Profile/Plan 严格符合 Core Schema，但不包含 `seal`；
- ToolBindings 保存本机映射，默认建议加入 `.gitignore`，不得复制到公共 Bundle；
- `answers.snapshot.json` 同样可能包含绝对本机路径；推荐忽略整个 `.veritrail/`，而不是只忽略一个文件；
- `REVIEW.md` 区分 `USER_SUPPLIED`、`DISCOVERED_CANDIDATE`、`DERIVED_FROM_PRESET` 和
  `NOT_PROVEN`；
- `handoff.ps1` 只打印经用户确认后可手工执行的 Core seal/preview/run 命令；它本身不调用 Core，
  也不包含自动批准摘要；
- 相同规范化答案与 Preset 版本产生逐字节稳定输出；时间戳不得污染草案内容；
- 输出目录已存在或任一目标文件冲突时全部拒绝，不覆盖、不合并。

## 4. 命令合同

### `doctor`

只读检查 Python/Core 版本、Windows 平台、项目路径、可执行文件候选、端口可用性、Chromium 可用性和
剩余磁盘/内存。它不安装、不启动、不结束进程。

输出状态：

- `READY`：已提供事实满足当前检查，但不等于 Run 会 PASS；
- `NEEDS_INPUT`：仍需用户选择或确认；
- `UNSUPPORTED`：项目或主机越过 0.1 合同。

### `init`

验证 Answers、Preset 和目标目录后原子生成 workspace。不得根据“常见框架”补写启动命令、端口或
断言。

### `validate`

验证 workspace 完整性、Schema、路径边界、ToolBindings 名称、Profile/Plan 交叉身份、回环 URL、预算
和草案状态。它不得添加 seal。

### `review`

验证并指向 `init` 时逐字节稳定生成的人类复核摘要；该摘要列出全部用户输入、Preset 派生项、环境
候选、未知项、拒绝项和 Core handoff 前停止线。`review` 不原地重写 workspace。

### `handoff`

只有 validate 成功且 manifest 仍为 DRAFT 时输出 Core 命令；`handoff` 不执行这些命令。Core seal
之后的文件保存在独立目录；Starter 不把 workspace 就地改写成 SEALED。

## 5. 固定生成语义

Preset 可以固定生命周期、资源、浏览器完整性和清理断言，但业务断言必须来自用户显式答案。Preset
不得从页面文字、测试名、README 或 AI 推断“真正业务成功”。

Starter 生成的 Core Plan 使用 0.7，Profile 使用 0.2；确切字段必须由 Core 公共 Schema 和验证器复核。
如果 Core 兼容范围或 Schema 变化，Starter 必须拒绝而不是自动迁移。

## 6. Fail-closed 矩阵

以下情况返回 `UNSUPPORTED`，不生成 workspace：

- 非 Windows 11 或不属于已证明的 C1 形态；
- 多于一个需要 Starter 管理的节点；
- Docker、Compose、WSL、虚拟机、远程执行或远程数据库；
- 非 loopback listener、动态端口、来源不明的既有 listener；
- Shell 字符串或 `cmd /c`、PowerShell `-Command`、`bash -c` 等解释器绕过；
- 需要自动安装系统工具、包、浏览器或修改 PATH/代理/注册表；
- 需要秘密值；
- 工作目录或 watch root 越出 subject root；
- 无法声明至少一个业务断言、预算或清理边界。

`NEEDS_INPUT` 只能用于支持矩阵内的缺失答案，不能用来掩盖不支持拓扑。

## 7. 错误与退出

- stdout 只输出一个版本化 JSON 结果；诊断写 stderr；
- 错误码必须稳定区分无效输入、冲突输出、不支持拓扑、Core 不兼容和环境未就绪；
- 任一失败后目标 workspace 不存在，或保持调用前逐字节不变；
- doctor/validate 的成功只表示 authoring 条件成立，不产生 ExecutionStatus 或 Verdict。

## 8. 验收矩阵

自动化：

- 相同答案确定性、不同主变量产生不同摘要；
- 无 seal、无自动审批、无覆盖；
- 路径穿越、symlink/junction 越界、Shell 绕过、秘密字段和非回环拒绝；
- Core 版本上下界、Schema 和 Profile/Plan 身份错误拒绝；
- Python 3.10/3.13、`python -O`、wheel/sdist clean install。

真实运行：

- Windows 11/C1 单节点示例的 doctor/init/validate/review/handoff；
- 人工 seal 与 Preview 批准后的独立 PASS 和 FAIL Run；
- Catalog/Workbench 桌面、390 px、Console/Network；
- 中止、端口竞争、重复 init、半写入故障和最终零残留。

S1 已完成固定合成 Subject 的真实双 Run、Catalog 与生产 Workbench 验收；准确步骤和事实见
[十分钟 PASS/FAIL 黄金路径](61-starter-single-webapp-golden-path.md)。独立安装、Release、公共下载
读回和 A0 Skill 尚未完成，因此 Starter 仍保持 `0.1.0.dev0`，不得写成开箱即用正式版。
