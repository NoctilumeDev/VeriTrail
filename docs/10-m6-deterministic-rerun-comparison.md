# 10. M6 同计划复跑确定性比较

## 状态

`AUTOMATED`。本文件先作为候选合同独立提交，随后 Comparison Core/CLI、两个 Schema、
Workbench Loader/View 与验收脚本已实现；Python 3.10/3.13 各 94 项测试、前端 39 项测试、
lint/type-check/生产构建均通过。定义、自动化与真实运行不是同一层证据；M6 仍须取得本文件
预注册的真实正/负 Run、Comparison、浏览器、安全、资源和清理事实后才能进入 `FROZEN`。

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
- 当前里程碑状态：`AUTOMATED`，真实运行与最终冻结待执行；
- 预期冻结标签：`m6-v0.7.0`。
