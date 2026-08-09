# 11. M7 预注册四角色配对反事实分析

## 状态

`PLANNED`。本文件是实现前独立冻结的候选合同；定义、自动化与真实运行均不能代替彼此。
前置基线是 M6 冻结提交 `807ef1eafae6249c88c68ab90d0be1e0d1eccf99` 与标签
`m6-v0.7.0`。只有本合同先成为可寻址提交，M7 才能进入实现。

## 目标问题

> 四个由预注册计划明确指定、按固定顺序产生的不可变 Run Bundle，能否证明处理效果随唯一
> 主要变量出现、在恢复基线后消失，且不会在负对照中出现，同时保留完整来源 Verdict 与边界？

M6 只回答同一 sealed Plan 复跑是否稳定；M7 回答不同 sealed Plan 之间的单变量配对是否支持
预注册因果解释。M7 不从任意两个 Run 自动推断因果，也不把配对结果写回来源 Report。

## 不在 M7 范围

- 不自动挑选最近、成功、最优或有利的 Run；
- 不支持缺少恢复基线或负对照的简化组，不允许运行后补选角色；
- 不做统计显著性、置信区间、趋势、性能分布或多次重复聚合；
- 不支持组合变量、多个主要变量、动态基线、跨 Subject 或跨随机种子分析；
- 不执行项目命令、Docker、中间件或外部服务，不扩张 M5 的静态目标边界；
- 不修改 ExperimentPlan 0.1–0.4、Evidence、Report、Bundle、Comparison、Catalog 或 Verdict；
- 不把配对包写入 M4 Run-only Catalog，不实现在线写、计划编辑或完整自举。

## 影响层级、所有者与消费者

- 声明层级：`L2_CONTRACT`；新增 PairingPlan 0.1 与 PairedAnalysis 0.1 公共只读契约；
- 所有者：Python Pairing Core / CLI / Vue Workbench；
- 权威输入：一个 sealed PairingPlan 与四个已通过 Bundle 0.1 完整性校验的不可变 Run；
- 新输出：`sealed-pairing-plan.json`、`paired-analysis.json`、`paired-analysis.md`、
  `paired-analysis-manifest.json`；
- 直接消费者：`seal-pairing`、`pair` CLI、Pairing Loader/View、Python/TypeScript 契约测试；
- 兼容消费者：M0–M6 Plan/Evidence/Report/Bundle/Comparison/Catalog/API/CLI/Workbench；
- 后续消费者：重复组统计、实验矩阵、完整轻量自举和复杂项目适配器；
- 数据所有权：来源 Run 继续拥有事实与 Verdict；PairedAnalysis 是可删除、可重建的派生包。

实际 diff 若修改来源 Run、既有 Schema、Verdict 优先级、M4 Catalog、M5 生命周期或任意命令
执行边界，视为范围漂移，必须停止并修订合同。

## PairingPlan 0.1

### 固定四角色

首版固定且只接受以下顺序：

```text
BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL
```

每个角色恰好一个 Run；四个 Run ID 和 Bundle digest 必须互不相同。`RESTORED_BASELINE` 必须
引用与 `BASELINE` 完全相同的 sealed ExperimentPlan digest。首版预热策略固定记录为
`NONE / 0 iterations`，避免声明尚未采集的预热行为。

PairingPlan 至少封存：

- `pairing_id`、版本、问题与四角色固定顺序；
- 唯一主要变量名称、来源及每个角色的预期结构化值；
- 四个角色各自准确的 sealed ExperimentPlan SHA-256；
- 一个或多个 outcome assertion ID；
- 每个 outcome 在四角色中的预期 `actual` 值；
- `NONE` 预热事实、适用边界、复现与清理步骤；
- PairingPlan 自身的 canonical SHA-256 seal。

处理组主要变量值必须不同于基线；恢复基线值必须等于基线；负对照值必须区别于基线与处理。
至少一个 outcome 的处理组预期值必须不同于基线；每个 outcome 的恢复基线与负对照预期值必须
等于基线，从合同层明确“处理效果出现、撤销后消失、负对照不复制效果”。

### 跨 Plan 控制投影

四个 ExperimentPlan 都必须是 `SINGLE_VARIABLE`，具有同一 `plan_id`、同一主要变量名称、角色、
来源与单位。比较时只允许以下差异：

1. `version`；
2. 唯一 `PRIMARY` 变量的 `value`；
3. 由内容变化必然产生的 `seal`。

`subject`、`question`、`baseline`、全部受控/干扰变量、required evidence、断言定义、随机种子、
资源预算、负载、影响层级、复现/清理、preflight、browser 与 target 必须逐字节规范化相同。
PairingPlan 只能收紧这些条件，不能提供任意 JSON Pointer 白名单绕过控制变量检查。

### Outcome 与非目标漂移

Outcome 只读取来源 Report 中同 ID 断言的已裁决 `actual`，不重新解释原始 Evidence。四个 Plan
中该断言的严重性、证据类型、路径、操作符和 Plan expected 必须相同。

未列入 outcome 的断言，其 `severity/status/operator/path/evidence_type/expected/actual` 在处理、
恢复和负对照中必须与基线相同；任何变化都是未声明结果漂移并使分析 `INCONCLUSIVE`。来源
Verdict、reason 与 Evidence 仍展示但不会被配对器覆盖。

## 输入门禁

1. PairingPlan seal 有效、结构完整、无敏感值且未超限；
2. 每个来源都是普通本地目录，Bundle 路径、集合、大小、哈希与交叉引用全部有效；
3. 每个来源包含有效 sealed ExperimentPlan，digest 与 Report、PairingPlan 三方一致；
4. 无符号链接、reparse point、硬链接、目录逃逸、额外文件或不支持版本；
5. 四个 Run 均为 `COMPLETED`，创建时间严格符合预注册角色顺序；
6. 四个 Run、Bundle、角色绑定唯一，随机种子相同，跨 Plan 控制投影成立；
7. outcome 存在且断言定义一致，非 outcome 没有未声明漂移。

损坏或不可信文件导致命令失败且不产生输出。来源完整但执行未完成、顺序错误、控制污染、
恢复失败或负对照出现处理效果时，保留 `INCONCLUSIVE` 包，而不是丢弃不利事实。

## PairedAnalysis 0.1 结果

| `analysis_status` | 条件 | 含义 |
| --- | --- | --- |
| `SUPPORTED` | 全部门禁成立，四角色 outcome 均命中预注册值 | 当前四 Run 支持声明的单变量解释 |
| `CONTRADICTED` | 基线、恢复、负对照成立，但处理组未命中预注册处理值 | 本轮完整证据没有观察到声明的处理效果 |
| `INCONCLUSIVE` | 执行、顺序、控制、恢复、负对照或非目标漂移破坏归因 | 当前输入不足以支持或反驳处理解释 |

优先级为 `INCONCLUSIVE > CONTRADICTED > SUPPORTED`。`SUPPORTED` 不是来源 Run 的 `PASS`；一个
有意故障处理组可以是 `FAIL`，同时配对分析因准确出现预注册效果而为 `SUPPORTED`。

每个结果必须包含稳定 reason code、四角色来源摘要、主要变量值、outcome 预期/实际、非目标
漂移、控制投影摘要和适用边界。不得生成 `PASS/FAIL` 字段或改写任一来源 Verdict。

## 不可变输出

- `analysis_id` 由 PairingPlan digest 与四个有序 Bundle digest 生成；
- 输出复制 canonical 的 sealed PairingPlan，并写入确定性的 JSON 与 Markdown 投影；
- Manifest 固定列出前三个文件的路径、大小和 SHA-256；
- 相同输入必须逐字节生成相同四文件，不写生成时间、绝对路径、账号或主机身份；
- 已存在输出目录一律拒绝覆盖，任意失败 staging 必须清理；
- 来源引用只保留角色、Run ID、Plan SHA、Bundle SHA、ExecutionStatus、Verdict 和创建时间。

## CLI 与 Workbench 候选链路

```powershell
.\.venv\Scripts\veritrail.exe seal-pairing `
  --plan .\examples\pairing\pairing-plan.json `
  --output .\artifacts\m7-sealed-pairing-plan.json

.\.venv\Scripts\veritrail.exe pair `
  --plan .\artifacts\m7-sealed-pairing-plan.json `
  --baseline .\artifacts\m7-baseline `
  --treatment .\artifacts\m7-treatment `
  --restored-baseline .\artifacts\m7-restored `
  --negative-control .\artifacts\m7-negative-control `
  --output .\artifacts\m7-paired-analysis
```

Workbench 增加本地 Pairing 目录入口，只在浏览器内存中读取。它必须先校验 Manifest 的文件集合、
路径、大小、SHA-256 与 PairingPlan seal，再核对 analysis ID、角色、状态、reason 和 outcome；
失败时不展示部分可信内容。页面必须明确显示来源 Verdict 与 analysis status 是不同维度，并支持
键盘、错误重试、history/刷新重新选择、桌面/移动无横向溢出。

## 预注册反例

必须至少保留并验证：

1. `PASS -> FAIL -> PASS -> PASS` 且 outcome 全部命中预期 -> `SUPPORTED`；
2. 处理组仍为基线 outcome，而其他三角色成立 -> `CONTRADICTED`；
3. 恢复基线未恢复或负对照复制处理效果 -> `INCONCLUSIVE`；
4. 任一 Run 未完成、角色复用、实际时间顺序错误 -> `INCONCLUSIVE`；
5. Plan 在主变量之外漂移、Plan digest/种子/断言定义不一致 -> `INCONCLUSIVE`；
6. PairingPlan、来源 Bundle 或输出文件改一字节 -> 拒绝且不显示部分可信内容；
7. 相同输入两次生成 -> 四个文件 SHA-256 全部相同；
8. 配对包不会被 M4 Run Catalog 当作 Run Bundle。

## 自动化与真实验收门槛

### Python

- Python 3.10 与 3.13 串行执行全套测试；
- 覆盖 Plan seal、四角色唯一性、控制投影、outcome、三态优先级、时间顺序与确定性；
- 覆盖损坏/缺失/额外文件、链接、超限、不可覆盖、staging 清理与脱敏错误；
- CLI 退出码和错误文本稳定，stdout/stderr 不泄露绝对路径。

### 前端

- TypeScript 校验器覆盖正向、三态、seal/hash、额外/缺失/变化文件和交叉引用；
- 组件覆盖四角色、来源 Verdict、outcome、原因、边界、错误与重新选择；
- `lint`、`type-check`、Vitest 与生产构建串行通过。

### 真实链路

- 先用现有 `evaluate` 或 `run` 依次生成四个新 Run，不手工拼 Report；
- 生成真实 `SUPPORTED / CONTRADICTED / INCONCLUSIVE` 与损坏包反例；
- Workbench 生产构建和 Codex 内置浏览器完成桌面/移动、本地导入、错误恢复与 history；
- 检查 Console、Network、键盘、横向溢出、未解释 4xx/5xx、外部/写请求；
- 记录内存、磁盘、端口/进程/临时目录释放与敏感扫描；
- 实际事实反驳本合同时保留失败 Artifact，修订合同，不倒改验收门槛。

## 退出条件

- M6 冻结基线未被回写，M0–M6 全部兼容回归通过；
- PairingPlan/PairedAnalysis/Manifest、CLI 与 Workbench 在已知消费者中一致；
- 四角色正向、处理反例、恢复/负对照反例、污染和损坏输入均取得真实证据；
- 相同输入输出逐字节稳定，全部来源可追溯但不持久化绝对路径；
- 内置浏览器桌面/移动、Console/Network、错误恢复和隐私 history 完成；
- 无秘密、个人路径、后台进程、监听端口或 staging 残留；
- 文档不冒充统计因果、组合实验、通用执行器、真实中间件或完整 v0 自举。

## 合同记录

- 合同版本：M7 Preregistered Paired Counterfactual Analysis Contract 0.1；
- 前置基线：`m6-v0.7.0`；
- 目标版本：Python Core `0.8.0.dev1`，Workbench `0.8.0-dev.1`；
- 目标 CLI：`seal-pairing`、`pair`；
- 当前里程碑状态：`PLANNED`。
