# 10. M6 同计划复跑确定性比较

## 状态

`FROZEN（实现提交 1a5eeaa6b5516c5b53248411e1284f6a2568e5e2）`。本文件先作为候选
合同独立提交，随后 Comparison Core/CLI、两个 Schema、Workbench Loader/View 与验收脚本
实现；Python 3.10/3.13、前端自动化、真实正/负 Run、逐字节复建、生产浏览器、Codex 内置
浏览器、安全、资源和清理门槛均由实际结果满足。定义、自动化与真实运行的证据仍在下文分层
记录，没有用合同文字代替运行事实。

前置基线是 M5 冻结提交 `d3b9cd72967aff02dc40d730640e30fea30de2d9` 与标签
`m5-v0.6.0`。M5 已真实证明一个 sealed Plan 可以通过单一 `run` 入口生成不可变 Run Bundle；
M6 只在该事实之上增加复跑比较，不回写已有 Run，也不改变其 Verdict。

## 目标问题

> 两个由同一 sealed Plan 和同一种子产生、Run ID 不同的不可变 Run Bundle，能否在不读取原始
> 项目、不重新执行断言、不忽略失败 Run 的前提下，生成可复验、可视、不可覆盖的确定性比较包？

这是 v0 完整闭环第 9 步的最小纵向切片。M6 判断的是“同计划复跑的已裁决语义是否一致”，
不是“处理变量是否造成因果效果”。两个 `FAIL` Run 可以稳定 `MATCH`；两个 `PASS` Run 也可能
因为断言实际值不同而 `DRIFT`。比较结论不得替代任一来源 Run 的 Verdict。

## 不在 M6 范围

- 不比较不同 Plan、不同种子、不同基线或不同主要变量的因果效果；
- 不表达 `BASELINE / TREATMENT / RESTORED_BASELINE / NEGATIVE_CONTROL` 配对实验；
- 不自动选择“最近一次成功 Run”，不删除、覆盖或挑选最优结果；
- 不比较任意原始 Evidence 正文、时间戳、随机路径或 SHA-256，从而把正常采集差异误报为漂移；
- 不把 Comparison 写入 M4 的 Run-only Catalog，不修改 SQLite/API 0.1；
- 不执行项目命令，不启动目标或中间件，不引入 Docker、云服务或 AI 裁决；
- 不实现计划编辑、趋势统计、性能显著性分析、任意后端编排或完整自举。

## 影响层级、所有者与消费者

- 声明层级：`L2_CONTRACT`；新增 Comparison 0.1 公共只读契约与 UI 消费者；
- 所有者：Python Comparison Core / CLI / Vue Workbench；
- 权威输入：两个已通过现有 Bundle 0.1 完整性校验的不可变 Run Bundle；
- 新输出：`comparison.json`、`comparison.md`、`comparison-manifest.json`；
- 直接消费者：`compare` CLI、Comparison Loader、Comparison View、Python/TypeScript 契约测试；
- 兼容消费者：M0–M5 Plan、Evidence、Report、Bundle、Catalog、API、CLI 与 Run Workbench；
- 后续消费者：配对/反事实实验、Comparison Catalog、完整轻量自举；
- 数据所有权：来源 Run 继续拥有事实和 Verdict；Comparison 是可删除、可重建的派生证据包。

实际 diff 若修改既有 Plan/Evidence/Report/Bundle 0.1、Verdict 优先级、Catalog 数据库/API、M5
运行生命周期或允许执行任意命令，视为范围漂移，M6 合同不能继续沿用。

## 控制变量设计

M6 自身的主要变量是：

```text
PRIMARY: repeat_outcome_semantics = identical | changed
```

受控条件：同一 Plan SHA-256、Plan ID/version、随机种子、Subject/Baseline、变量、断言和规则；
同一 Comparison 规则版本；固定的 baseline → repeat 顺序。Run ID 必须不同。

允许变化且不进入语义漂移：Run ID、Run 创建时间、Evidence `captured_at`、Evidence/附件文件名、
Evidence SHA-256 和 Bundle SHA-256。这些事实仍分别保留在来源引用中，不会伪装成相同文件。

M6 比较的冻结语义投影包括：

- `execution_status`、`verdict` 与有序 reason code；
- 按断言 ID 排序后的 `severity/status/operator/path/evidence_type/expected/actual`；
- 排序后的 `missing_evidence`；
- 去除 `evidence_sha256` 后的 contamination 结构；
- Evidence 类型、来源、解析器/脱敏规则/保留策略、脱敏计数、摘要与附件逻辑形态。

断言的 `explanation` 和证据哈希不进入结果投影；前者是呈现文案，后者会被采集时间等允许差异
改变。M6 不读取原始 Evidence `facts` 做新的业务判断；未被 sealed assertion 或上述形态表达的
业务事实，不能由 M6 宣称“相同”。

## Comparison 0.1 契约

### 输入门禁

每个来源必须：

1. 是普通本地目录，且现有 Bundle 0.1 路径、文件集合、大小、哈希与交叉引用全部有效；
2. 声明并包含 `sealed-plan.json`，其 seal 自身有效且 digest 等于 Report 的 Plan SHA-256；
3. 没有符号链接、reparse point、硬链接、目录逃逸、未声明文件或不受支持版本；
4. 在比较期间未发生索引后变化；
5. 只通过显式 `--baseline` 与 `--repeat` 路径读取，绝不扫描用户目录或持久化绝对路径。

来源包损坏属于不可信输入：命令失败且不产生 Comparison 输出。来源完整但不可比较时，应产生
`INCONCLUSIVE` Comparison，保留原因，而不是静默拒绝或硬凑差异结论。

### 三态结果

| `comparison_status` | 条件 | 含义 |
| --- | --- | --- |
| `MATCH` | 不同 Run ID、同 Plan SHA、均 `COMPLETED`，且语义投影相同 | 这次复跑在 M6 投影内一致 |
| `DRIFT` | 满足可比较门禁，但语义投影至少一处不同 | 复跑结果发生确定性漂移 |
| `INCONCLUSIVE` | 同 Run 被复用、Plan/种子不一致或任一 Run 未完成 | 当前输入不能支持复跑一致性判断 |

优先级为 `INCONCLUSIVE > DRIFT > MATCH`。结果必须包含稳定 reason code 和逐字段 differences；
`MATCH` 也必须明确声明两侧原 Verdict，防止被误读为“产品通过”。

### 不可变输出

- `comparison_id` 由规则版本和有序的 baseline/repeat Bundle SHA-256 生成；
- `comparison.json` 记录规则版本、结果、来源引用、语义摘要、差异和适用边界；
- `comparison.md` 是同一对象的确定性可读投影；
- `comparison-manifest.json` 固定列出前两文件的相对路径、大小和 SHA-256；
- 相同输入必须逐字节产生相同三文件，输出不写生成时间、绝对路径或主机身份；
- 已存在输出目录一律拒绝覆盖，失败 staging 必须清理。

## CLI 与 Workbench 候选链路

```powershell
.\.venv\Scripts\veritrail.exe compare `
  --baseline .\artifacts\baseline-run `
  --repeat .\artifacts\repeat-run `
  --output .\artifacts\comparison-baseline-repeat
```

Workbench 增加“选择复跑比较包”入口，仅在浏览器内存中读取本地目录。它必须先校验
Comparison Manifest 的文件集合、路径、大小与 SHA-256，再交叉核对 `comparison_id`、来源角色、
状态、reason 和 difference；失败时不展示部分可信比较。页面展示：

- `MATCH / DRIFT / INCONCLUSIVE`，且不复用 Run `PASS/FAIL` 的视觉语义；
- baseline/repeat 的 Run ID、ExecutionStatus、Verdict、Plan 与 Bundle 摘要；
- 差异字段、左右值、语义投影摘要和“不等于因果结论”的边界；
- 完整性文件计数与本地只读说明；
- 键盘可达、状态不只依赖颜色、桌面与移动无横向溢出。

浏览器刷新或 history 返回本地比较 URL 时必须要求重新选择目录，不持久化文件对象。

## 预注册反例

必须至少保留并验证以下路径：

1. 同一 sealed Plan 的两个独立 `PASS` Run → `MATCH`；
2. 同一 sealed Plan 的 `PASS` 与硬断言 `FAIL` Run → `DRIFT`；
3. 两个不同 Plan 或种子的完整 Run → `INCONCLUSIVE`；
4. 同一 Run/复制包被同时作为两侧 → `INCONCLUSIVE`；
5. `ABORTED/PENDING` 与完整 Run → `INCONCLUSIVE`；
6. 任一来源或 Comparison 文件被改一字节 → 拒绝，且不留下输出/部分可信 UI；
7. 相同输入两次生成 → 三个文件的 SHA-256 全部相同；
8. Comparison 输出不被 M4 Catalog 误收录为 Run；其使用独立输出根或显式排除边界。

## 自动化与真实验收门槛

### Python

- Python 3.10 与 3.13 串行执行全套测试；
- 覆盖投影稳定排序、允许差异、嵌套值差异、结果优先级、计划封存交叉验证；
- 覆盖损坏/缺失/额外文件、路径穿越、链接、超限、不可覆盖和 staging 清理；
- CLI stdout/stderr、退出码和错误文本稳定，不泄露来源绝对路径。

### 前端

- TypeScript 校验器覆盖正向、三态、哈希变化、额外/缺失文件和引用不一致；
- 组件覆盖状态语义、左右来源、差异、无差异、错误、重新选择与释放；
- `lint`、`type-check`、Vitest 和生产构建串行通过。

### 真实链路

- 先用 `run` 或 `evaluate` 生成两个新的独立 Run，不复用手工拼装报告；
- 用 `compare` 生成正向 `MATCH` 与负向 `DRIFT/INCONCLUSIVE` Comparison；
- 使用 Workbench 生产构建真实导入，并在 Codex 内置浏览器完成桌面与移动关键链路；
- 检查 Console、Network、键盘、history/刷新、横向溢出和未解释 4xx/5xx；
- 记录峰值内存、磁盘增量、端口/进程/临时目录释放与敏感扫描；
- 真实结果反驳候选定义时保留失败 Artifact，创建合同修订，不倒改本文件的原始门槛。

## 退出条件

只有下列事实同时成立，M6 才能标记 `FROZEN`：

- M5 冻结基线没有被回写，M0–M5 兼容回归通过；
- Comparison 0.1、CLI、Workbench 在全部已知消费者中一致；
- 正向、漂移、不可比较和损坏输入均取得真实证据；
- 相同输入输出逐字节稳定，所有输出可追溯到两个来源 Bundle digest；
- 内置浏览器桌面/移动、Console/Network 与错误恢复完成；
- 没有秘密、个人路径、后台进程、监听端口或 staging 残留；
- 文档只声明同 Plan 复跑比较，不冒充因果配对、趋势或完整 v0 自举。

## 合同记录

- 合同版本：M6 Deterministic Rerun Comparison Contract 0.1；
- 前置基线：`m5-v0.6.0`；
- 目标版本：Python Core `0.7.0.dev1`，Workbench `0.7.0-dev.1`；
- 目标 CLI：`compare`；
- 当前里程碑状态：`FROZEN`；
- 冻结标签：`m6-v0.7.0`。

## 实际实现与自动化事实

M6 合同提交为 `4b0fb76588e56fe0198ade2a95f09bfc5816af08`，实现提交为
`1a5eeaa6b5516c5b53248411e1284f6a2568e5e2`。实际 diff 保持在预注册的 `L2_CONTRACT`
范围：新增 `comparison.py`、`compare` CLI、Comparison/Manifest 0.1 Schema、Vue Loader/View、
测试与有界浏览器验收脚本；没有修改 Plan/Evidence/Report/Bundle 0.1、Verdict、Catalog SQLite/API
或 M5 编排语义。

冻结实现的自动化结果：

- Python 3.10.6：94/94；Python 3.13：94/94；
- Workbench：lint、type-check、生产构建通过，Vitest 39/39；
- M6 新增 Python 8 项，覆盖三态结果、Plan 不同、同 Run 复用、未完成 Run、损坏来源、
  逐字节稳定、Manifest、不可覆盖与 CLI 脱敏错误；
- 前端新增 Loader/View/App 测试，覆盖三态显示、来源角色、差异、完整性、额外/缺失/变化文件、
  状态冲突和真实目录输入事件；
- 首次 3.13/npm 批处理因 3.13 未安装 editable 包且 npm 工作目录错误，分别得到 import 与
  `package.json` 入口错误；这不是 VeriTrail Run。修正为临时 `PYTHONPATH=src` 和 `web/` 工作目录
  后完整复跑通过，原始失败没有被当作产品通过证据。

## 真实 Run 与 Comparison 事实

### MATCH：同 Plan 的两次完整 M5 Run

在实时可用内存约 6.74 GiB、磁盘约 147 GiB、18769 无监听时，严格串行运行同一
`examples/orchestration/plan.json`：

- baseline：`m6-rerun-baseline-20260809`；
- repeat：`m6-rerun-repeat-20260809`；
- 两侧 Plan SHA-256：
  `658955b08cd56902e376e4db7d5716572374b1cb0a21283b1cc55ac8a0efc10a`；
- 两侧均为 `PROCEED`、目标已启动/READY、`COMPLETED/PASS`、`cleanup_complete=true`；
- 两次之间与结束后 18769 监听数均为 0；
- Bundle SHA-256 分别为
  `7aadc6d13383c382c8c4d60c39f57573aba0ce29dffc0e4dd8340ae8e5637b78` 与
  `fc6375061370574ebcf88ab6b3d60cab35534cd1864881b4c0714341a7dcef3c`，证明它们不是同一个
  文件副本；两侧 semantic SHA-256 均为
  `9ee206252c8f5b9cdcd82e7e805a7f3b602c652eef4b3e7331b86920655ce13b`。

生成 Comparison `cmp_f3d21253b674318c1f0fee7d`，结果 `MATCH`、`comparable=true`、0 差异。
来源 Run 的 `PASS` 仍作为左右事实展示，没有被 Comparison 改写。

同一对来源第二次生成到新目录，三个文件逐字节相同：

| 文件 | SHA-256 |
| --- | --- |
| `comparison.json` | `7b8a527d46cb273e3c901d9ec1abb0d82cac9bf54ecd9a4ca14a9eac05da0d9c` |
| `comparison.md` | `f75b2609cd1885cd8721f1ad8d58c2041b54d9fddd0f7f09c99c8c3a916d2edd` |
| `comparison-manifest.json` | `e2e65b4632e86131b0821576063d5b9761e8c9e06efcf7806c4dc0252c6fad9f` |

### DRIFT 与 INCONCLUSIVE

用同一 sealed M0 Plan 生成新的真实 Bundle：

- `m6-minimal-pass-20260809`：`COMPLETED/PASS`；
- `m6-minimal-fail-20260809`：`COMPLETED/FAIL`；
- `m6-minimal-aborted-20260809`：`ABORTED/PENDING`。

`PASS → FAIL` 生成 `cmp_b360d395a4e2a592761f22d4`：`DRIFT`、可比较、7 处差异；差异明确
落在断言 actual/status、Evidence 形态、reason code 与 Verdict。`COMPLETED → ABORTED` 生成
`cmp_8c546ae7b25cbeea72c42edb`：`INCONCLUSIVE`、不可比较、原因包含
`RUN_NOT_COMPLETED`；已有 3 处投影差异仍被展示，但没有越过门禁写成 `DRIFT`。

## 真实浏览器与用户链路

生产构建的有界 Playwright 验收输出为 `m6-comparison-browser-20260809`：

- 桌面真实导入 `MATCH / DRIFT / INCONCLUSIVE`；
- 故意改变 `comparison.json` 后命中 `COMPARISON_SIZE_MISMATCH`，未展示部分 Comparison，
  可显式返回正向 Run；
- 刷新 `?fixture=comparison` 命中 `COMPARISON_RESELECT_REQUIRED`，history 返回正向入口；
- 移动 390×844 的 `MATCH` 可读且横向溢出为 0；
- 6 个检查全部完成，48 个请求、0 HTTP error、0 外部请求、0 写请求、0 Console/Page/Request
  异常；
- 桌面截图 SHA-256：
  `f2da94036eedc26c5ab9606b112c206c1ea9c52e11c73af47e6e64e06e1ac285`；移动截图：
  `b8dcd34ea4894367f0391fcbe8c54650fde299f56124b60d03e91b50dd1ff770`。

Codex 内置浏览器再次独立验收：

- 1280×720 导入真实 MATCH，显示两侧不同 Bundle digest、相同 semantic digest、0 差异与三条
  边界；导入真实 DRIFT 后展示 7 条左右差异；
- 改动 Comparison Markdown 一字节后命中 `COMPARISON_SIZE_MISMATCH`，Comparison View 数量为
  0，返回正向入口后恢复 `COMPLETED/PASS`；
- 刷新后要求重新选择目录，后退回 `?fixture=positive`；
- 390×844 再次导入 MATCH，来源可读、横向溢出为 0；
- Console warning/error 为 0；页面观察到 12 项资源，全部来自 `127.0.0.1:18769`。网络状态码
  的完整断言由上一条生产 Playwright 证据给出，不用资源清单冒充状态码证据。

## 安全、资源与清理事实

- 两套 Python `pip check` 均无破损依赖；npm 官方 registry 的生产依赖审计为 0 vulnerabilities；
- M6 Artifact 文本未命中个人绝对路径、GitHub 邮箱、私钥或 GitHub token 形态；11 个运行与
  失败 Artifact 目录全部被 Git 忽略，Git 工作区在写冻结文档前为空；
- 真实浏览器开始前可用内存约 6.65 GiB，终验后约 6.62 GiB，磁盘仍约 147 GiB；没有超过
  Plan 的 4/2 GiB 软/硬停止线；
- 生产验收脚本自行释放 18769。内置浏览器预览的终端父会话退出后，首次残留检查捕获到本轮
  Vite Node 子进程仍占用 18769；按端口所有权和启动时间只停止该 PID 后重新检查为 0。这个
  清理反例被保留在验收记录中，没有把“父会话已退出”冒充“端口已释放”；
- 最终 18765–18770 监听数均为 0，Vite preview 进程为 0，`.veritrail-*` staging 为 0；临时
  移动视口已复原，内置浏览器验收页已关闭。

## 冻结结论与边界

这些事实支持冻结 M6“同计划复跑确定性比较”：两个不同 Run ID、同 sealed Plan、完整执行的
不可变 Bundle 可以产生确定性的 `MATCH/DRIFT`，不满足门禁的输入保留为 `INCONCLUSIVE`；输出
可逐字节复建，Workbench 在展示前独立验真。

它们不证明不同 Plan 的处理组因果、恢复基线/负对照配对、趋势统计、Comparison Catalog、计划
编辑、任意项目命令、真实后端/中间件编排或完整 v0 自举。M4 Catalog 仍只扫描显式指定的 Run
Artifact 根；本轮 Comparison 均保留在该根之外的忽略目录，没有改写 Run-only Catalog 语义。
