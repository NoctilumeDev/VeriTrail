# 12. M8 预注册全因子批次矩阵与固定种子扰动

## 状态

`CORE / WORKBENCH IMPLEMENTED / AUTOMATED`。实现前独立合同已经落地为四个公共 Schema、
Python Core、`seal-batch` / `analyze-batch` CLI、脱敏 2×2 示例、自动化反例，以及只读
BatchAnalysis 四文件 Loader 与矩阵/wave 视图；真实 M5 批次、真实浏览器链路和最终冻结仍为
`PENDING`，因此本里程碑不是 `FROZEN`。前置语义基线是 M7 冻结提交
`e5c6e271423d4359fc63e542c95093b823404de8` 与标签 `m7-v0.8.0`；其后的
`c616974` 只修正 M7 跨文档状态不一致，没有改变代码或公共契约。

本合同已先成为可寻址提交 `b1ca45b`，随后才进入实现。实现结果若反驳合同假设，必须保留
失败证据、修订合同并重新评审，不能倒改运行事实或放宽门槛制造通过。

## 目标问题

> 能否在不削弱单变量计划、不执行任意项目命令的前提下，预注册一个有界全因子 Profile
> 矩阵，先完成确定性串行覆盖，再按固定种子生成不改变成员集合的扰动顺序；最后用全部不可变
> Run 证明覆盖是否完整、受控条件是否一致、预注册交互假设是否被支持，同时保留每个来源
> Run 的 ExecutionStatus 与 Verdict？

M7 回答固定四角色的单一处理效果是否出现、撤销并避开负对照；M8 回答多个明确 Profile 是否
全部覆盖，以及组合 Profile 的预注册结果是否在确定性与扰动阶段保持一致。M8 的 Profile
作为一个有结构映射的分类主要变量，不把 Profile 内多个组件分别宣称为已独立归因。

## 为什么现在做矩阵，而不是项目执行器

当前冻结基线已经具备单变量 Run、资源预检、真实浏览器、只读 Workbench、Run Catalog、
有界静态目标生命周期、同计划复跑比较和四角色反事实分析，但仍缺少产品方法中的两项：

1. 所有声明组合必须先进入确定性覆盖矩阵；
2. 随机顺序只能在确定性覆盖之后寻找偶发问题，并保存可跨实现复建的种子。

直接进入 npm/Maven/Docker、真实中间件或通用项目命令，会同时扩大进程权限、环境传递、进程树
清理、数据副作用和跨项目适配器边界。M8 先冻结调度与分析语义，未来执行器只能消费它，不能
自行删减 Profile、重排不利 Run 或把资源不足包装成覆盖完成。

## 不在 M8 范围

- 不执行 Shell、npm、Maven、Docker、数据库、中间件或用户项目命令；
- 不启动、停止或并行运行来源 Run；批次 wave 只是封存的计划边界，不证明真实时间重叠；
- 不修改 ExperimentPlan 0.1–0.4、Run Bundle、Verdict、Comparison 或 PairedAnalysis 语义；
- 不从任意历史 Run 自动挑选“最好”的 Profile 结果，不删除失败、异常或中止 Run；
- 不把随机扰动代替确定性全覆盖，不因同一种子偶然通过而补写缺失单元格；
- 不做统计显著性、方差、置信区间、性能趋势或任意多变量因果归因；
- 不把组合 Profile 的结果写成来源 Run 的 `PASS/FAIL`；
- 不把 BatchAnalysis 写入 M4 Run-only Catalog；
- 不实现计划编辑器、在线写、完整自举、第二项目证明或 AI 裁决。

## 前置门禁

- M7 合同：`7daf3b4`；
- M7 实现：`9046f25`；
- M7 浏览器导入修复：`c726fe8`；
- M7 冻结：`e5c6e27`（tag `m7-v0.8.0`）；
- M7 状态一致性修复：`c616974`；
- M7 冻结提交与标签已从远端读回；M8 合同提交 `b1ca45b` 已推送，未回写或移动
  `m7-v0.8.0` 标签。

若 M8 实现必须改变 M0 Verdict 优先级、M4 Catalog 权威边界、M6 Comparison、M7 四角色语义、
现有 Plan seal 或 Bundle 哈希，视为范围上浮；停止实现并重新评审全部消费者。

## 影响层级、所有者与消费者

- 声明层级：`L2_CONTRACT`；
- 所有者：Python Batch Matrix Core / CLI / Vue Workbench；
- 新公共契约：BatchPlan 0.1、RunAssignment 0.1、BatchAnalysis 0.1、
  BatchAnalysis Manifest 0.1；
- 直接消费者：`seal-batch`、`analyze-batch`、Batch Loader/View、Python/TypeScript 契约测试；
- 兼容消费者：M0–M7 Plan/Evidence/Report/Bundle/Comparison/PairedAnalysis/Catalog/API/CLI/
  Workbench；
- 后续消费者：有界项目执行器、真实微并行调度、完整自举、第二项目证明与实验矩阵目录；
- 数据所有权：来源 Run 继续拥有执行事实与 Verdict；BatchAnalysis 是可删除、可重建的派生包。

## 控制变量设计

### 基线

基线是 M7：预注册计划只接受固定四角色和唯一主要变量，来源 Run 必须完整、不可变、可追溯，
分析状态不改写 Run Verdict。

### 唯一主要变化

`analysis_design`：

- 基线值：`four_role_paired_counterfactual`；
- M8 实现值：`bounded_full_factorial_batch_matrix`。

### 受控条件

- M0–M7 公共 Schema、canonical JSON、SHA-256、脱敏、不可覆盖与 staging 清理语义；
- 来源 Bundle 完整性校验、Report/Verdict 权威边界和 Catalog Run-only 边界；
- 同一 Batch 内 Subject、Baseline、断言、负载、资源政策、随机种子来源和受控变量投影；
- Workbench 只读验真、同源网络、宫墙朱状态语义与本地文件不上传边界；
- Python 3.10/3.13、Node worker 上限和 16 GB 主机的串行/最多二路微并行策略。

## BatchPlan 0.1

BatchPlan 是独立封存契约，不扩展或放宽 ExperimentPlan 的 `SINGLE_VARIABLE` 约束。它至少包含：

- `batch_id`、版本、问题、Profile 主要变量名称与来源；
- 2–4 个有序维度，每个维度 2–4 个有序 level；
- 维度笛卡尔积形成的 4–16 个 Profile，每个单元格必须恰好出现一次；
- 每个 Profile 的稳定 ID、维度值映射、sealed ExperimentPlan SHA-256、固定实现映射、预计
  静态目标 fingerprint 与预计内存；
- 确定性覆盖阶段、固定种子扰动阶段、资源 envelope、预注册 outcome 与边界；
- reproduction、cleanup、大小/数量限制和 canonical SHA-256 seal。

每个来源 ExperimentPlan 必须保持为已冻结的 0.4 `SINGLE_VARIABLE + STATIC_HTTP`：唯一主要
变量必须等于 BatchPlan 声明的 Profile 变量，值必须等于对应 Profile ID。维度值是该分类值的
结构化解释；M8 可以验证“A+B Profile 与 A、B、基线不同”，但不能据此宣称 A 或 B 已分别
获得多变量因果归因。

Profile 不能只换标签。BatchPlan 必须预注册其固定实现映射，M8 0.1 只允许
`subject.version`、`subject.source_ref`、`target.root` 与 `baseline.fingerprint` 随 Profile
变化，并要求每个 Profile 声明预计 `static_root_fingerprint`。第四个字段来自实现前合同与 M5
真实裁决代码的交叉检查：静态内容改变后若 `baseline.fingerprint` 不同步，M5 必然产生
`STATIC_ROOT_FINGERPRINT_DRIFT`。因此来源 Plan 的 `baseline.fingerprint`、Profile 预注册值与
`runtime.orchestration` 实际 fingerprint 必须三方相等；不匹配即为实现漂移。除这四个固定字段、
Plan `version`、主要变量 `value` 与 seal 外，其余 Plan 投影必须逐项相同。M8 不提供用户自定义
JSON Pointer 白名单。

### 全因子覆盖

- Profile 集合必须等于声明维度的完整笛卡尔积，禁止遗漏、不重复、也不能增加隐藏 Profile；
- `coverage` 阶段严格串行，按维度和 level 的声明顺序生成 canonical 顺序；
- 每个 Profile 在 coverage 阶段恰好一个 slot；
- coverage 未完成时，后续扰动事实可以保留，但不能把矩阵写成完整或支持交互假设。

### 固定种子扰动

- `perturbation` 阶段在 coverage 之后，重复次数为 1–4；
- 每次重复必须包含同一完整 Profile 集合，种子只改变顺序，不能改变成员、次数或 outcome；
- 算法固定为 `SHA256_RANK_V1`：对 canonical JSON `[seed, repetition, profile_id]` 计算
  SHA-256，按 digest、再按 Profile ID 升序；不依赖 Python、JavaScript 或平台 RNG 实现；
- 相同 Plan 与种子必须逐字节重建同一顺序；不同种子可以产生相同偶然排列，但不能被强制
  声称一定不同；
- 随机扰动不是随机抽样，不允许跳过 Profile。

### 资源与 wave

- coverage 每个 wave 只能包含一个 slot；
- perturbation 的 `max_parallel` 只能为 1 或 2，所有 wave 的 slot 数不得超过该值；
- 每个 Profile 声明预计内存，每个 wave 的总预计内存不得超过封存 budget；
- wave 之间必须有 preflight/cleanup 边界，上一 wave 残留会使后续分析不可归因；
- M8 只验证计划、来源顺序和资源 envelope，不执行并行，也不把同 wave 的分组冒充真实重叠；
- 未来执行器必须另行证明进程、时间线、内存、端口和清理事实。

### 预注册 outcome 与交互假设

BatchPlan 为每个 assertion ID 声明每个 Profile 的 `expected_actual`。对于 coverage 和每次
perturbation，来源 Run 的对应 actual 都必须保留：

- 基线、单组件和组合 Profile 全部按预期出现，才支持预注册 Profile 级交互假设；
- 确定性阶段完整且控制条件一致，但实际与预期稳定冲突，结论为 `CONTRADICTED`；
- 偶发不一致、只在扰动顺序出现的变化、残留、顺序错误或控制漂移进入 `INCONCLUSIVE`；
- 任何来源 `FAIL` 都继续显示。若某个组合 Profile 预期就是硬不变量失败，来源 `FAIL` 与
  Batch 假设 `SUPPORTED` 可以同时存在，二者不能压成同一状态。

## 来源 Run 与 Assignment

`analyze-batch` 使用一个严格的 RunAssignment 0.1 和显式 `--runs-root`：

- Assignment 只保存 `slot_id ->` 安全相对 Bundle 目录，不保存绝对路径；
- 路径必须留在显式根内，拒绝绝对路径、反斜杠、点段、隐藏节点、链接与重复目标；
- 每个 Run 必须通过 Bundle 0.1 完整性、文件集合、大小、SHA-256、交叉引用和 sealed Plan 校验；
- 每个 Run 必须保留 Plan 0.4 所需的 `runtime.preflight`、`runtime.orchestration` 与
  `browser.session`；wave 边界的 preflight 和 cleanup 事实不能由 Assignment 手工声明；
- Run ID 必须唯一，禁止同一 Run 复用到多个 slot；
- source Plan digest、Profile 主要变量值与 BatchPlan 三方一致；
- 来源 Plan `baseline.fingerprint` 与实际 `static_root_fingerprint` 必须同时等于 Profile
  预注册值，不能只依赖 Plan 标签推断实际实现；
- 除固定的 `subject.version`、`subject.source_ref`、`target.root`、`baseline.fingerprint` 实现
  映射，以及 Plan `version`、Profile 主要变量 `value` 与 seal 外，控制投影必须相同；
- coverage 与 perturbation 的 phase/wave 先后关系必须与来源时间事实一致；同 wave 内不声明
  全序，也不从时间戳自动推断真实并行；
- 缺少合法 slot 生成可审计的 `INCOMPLETE` 分析；损坏、不安全或超限来源直接拒绝，且不创建
  部分可信输出。

Assignment 是运行时定位输入，不进入 BatchAnalysis Bundle。输出只持久化 slot、Profile、
Run ID、Bundle digest、Plan digest、ExecutionStatus、Verdict、时间与 outcome 投影。

## BatchAnalysis 0.1

BatchAnalysis 分开记录两个维度，避免“矩阵跑全了”被误写成“系统通过”：

### CoverageStatus

- `COMPLETE`：所有 coverage 与 perturbation slot 均有唯一、完整、顺序合法且控制一致的 Run；
- `INCOMPLETE`：一个或多个计划内 slot 缺失或没有达到计划要求的执行事实；
- `INCONCLUSIVE`：Run 复用、顺序/seed 不符、受控投影漂移、残留、来源时间冲突或其他污染
  使覆盖无法可信归因。

### HypothesisStatus

- `SUPPORTED`：CoverageStatus 为 `COMPLETE`，全部预注册 Profile outcome 在确定性与扰动阶段
  匹配，且没有未计划差异；
- `CONTRADICTED`：CoverageStatus 为 `COMPLETE`、控制条件与重复结果稳定，但至少一个
  预注册 outcome 被一致事实反驳；
- `INCONCLUSIVE`：覆盖不足、污染、偶发/顺序相关差异、恢复不一致或证据不足。

CoverageStatus 和 HypothesisStatus 都不是 Run Verdict。BatchAnalysis 必须逐 slot 展示来源
ExecutionStatus/Verdict，不能自动选择成功 Run、平均掉失败或使用多数票覆盖偶发硬失败。

## 输出与确定性

成功分析只生成四个文件：

1. `sealed-batch-plan.json`；
2. `batch-analysis.json`；
3. `batch-analysis.md`；
4. `batch-analysis-manifest.json`。

- `analysis_id` 由 BatchPlan digest 与 slot 顺序中的 Bundle digest 或 canonical `MISSING` 标记
  生成，因此缺格分析仍可稳定寻址；
- JSON 使用 canonical 序列化；Markdown 是同一模型的稳定投影；
- Manifest 精确列出另外三个文件的相对路径、大小与 SHA-256，不包含自己；
- 相同 Plan、Assignment 与来源必须逐字节相同；时间不能使用分析执行时钟制造漂移；
- 输出存在时拒绝覆盖；所有异常先清理 staging，再返回脱敏稳定错误；
- 不持久化绝对路径、环境变量值、命令行、Cookie、令牌、公网/局域网地址或原始业务正文。

## CLI

```powershell
.\.venv\Scripts\veritrail.exe seal-batch `
  --plan .\examples\batch\batch-plan.json `
  --output .\artifacts\m8-sealed-batch-plan.json

.\.venv\Scripts\veritrail.exe analyze-batch `
  --plan .\artifacts\m8-sealed-batch-plan.json `
  --assignment .\artifacts\m8-run-assignment.json `
  --runs-root .\artifacts `
  --output .\artifacts\m8-batch-analysis
```

CLI 只读取既有 Run；它不调用 `run`、不启动 Profile、不执行清理命令，也不自动搜索历史目录。

## Workbench

Workbench 已增加本地 BatchAnalysis 四文件入口。根据 M7 的真实目录选择器反例，M8 从一开始就
使用显式多文件选择，不依赖 `webkitdirectory`。Loader 必须：

- 在显示前核对 Manifest 文件集合、路径、大小、SHA-256 与 BatchPlan seal；
- 重算 analysis ID、完整矩阵、canonical/seed 顺序、slot/Profile/Run 引用和状态 reason；
- 展示维度矩阵、coverage/perturbation phase、wave 预算、来源 Verdict 与 outcome；
- 分开显示 CoverageStatus、HypothesisStatus 和 Run Verdict；
- 明示“wave 只是计划边界，不证明真实并行”和“Profile 信号不等于统计显著性”；
- 损坏、缺失或交叉引用失败时清空部分可信 Batch View，可显式返回正向 Run；
- 刷新后要求重新选择本地文件，history 不持久化 File 对象；
- 延续纯 CSS 故宫主题，不增加贴图、CDN、远程字体、遥测或第二套状态颜色。

## 自动化矩阵

### BatchPlan

1. 2×2、2×3、3×2 全因子矩阵接受，Profile 集合和 canonical coverage 顺序稳定；
2. 缺格、重复格、隐藏额外 Profile、维度/level 重复、超过 16 格拒绝；
3. source Plan digest、Profile ID、维度映射、固定实现映射和主要变量三方不一致进入污染结论；
4. 只改 Profile 标签但 target fingerprint 不变/不符，或试图放宽固定实现字段集合时拒绝；
5. coverage 非串行、seed 顺序伪造、随机阶段漏格或随机替代 coverage 拒绝；
6. wave 超过二路或预算、缺少 wave 间清理边界拒绝；
7. seal 改一字节拒绝，旧 ExperimentPlan 与 M7 PairingPlan hash 保持兼容。

### Assignment 与 Analysis

1. 完整稳定矩阵 -> `COMPLETE/SUPPORTED`；
2. 完整且稳定反驳预期 -> `COMPLETE/CONTRADICTED`；
3. 缺 slot -> `INCOMPLETE/INCONCLUSIVE`，已有不利 Run 仍保留；
4. Run 复用、时间顺序错误、控制漂移、偶发扰动差异 -> `INCONCLUSIVE/INCONCLUSIVE`；
5. 来源 Run `FAIL` 不被 Batch 状态覆盖，也不阻止一个预期失败 Profile 支持假设；
6. 不安全相对路径、链接、损坏 Bundle/Plan/输出拒绝且无半成品；
7. 相同输入逐字节复建，改变种子只改变合法扰动顺序和由此派生的标识；
8. BatchAnalysis 放入 M4 Catalog 时 `run_count=0`。

### 兼容与前端

- Python 3.10/3.13 全回归包括 M0–M7 冻结哈希与失败反例；
- Loader 覆盖四文件完整性、矩阵/seed 重算、三类状态、错误恢复和对象释放；
- Workbench 覆盖桌面/移动、键盘、history、零横向溢出与状态非颜色唯一表达；
- lint、type-check、Vitest 与生产构建串行通过。

自动化最多支持 `AUTOMATED`，不能替代真实 Run、浏览器和清理终验。

## 真实运行退出条件

在干净实现提交和当前 16 GB Windows 主机上串行完成：

1. 启动前重新检查内存、磁盘、计划端口和 staging；不启动 Docker 或无关中间件；
2. 封存一个 2×2 矩阵：基线、A、B、A+B；四个 Profile 使用四份有界静态实现，来源 Plan
   只在固定实现映射和 Profile 主要值上变化，coverage 四个 slot 严格串行；
3. 用固定种子生成至少一轮完整 perturbation，并按 wave 边界创建新的、互不复用的真实 Run；
4. 所有 Run 由已有 M5 `run` 产生，不手工拼 Report；每个 Run 都保留真实 preflight、静态目标
   生命周期、实际静态目标 fingerprint、Chromium 与 cleanup 事实；保存一个组合 Profile 的
   真实 `FAIL`，证明完整覆盖不会覆盖来源失败；
5. 生成 `COMPLETE/SUPPORTED`、`COMPLETE/CONTRADICTED`、`INCOMPLETE/INCONCLUSIVE` 与
   控制漂移/顺序污染 `INCONCLUSIVE/INCONCLUSIVE`；
6. 相同输入第二次生成四文件逐字节相同；改变 seed 后成员集合、次数和 coverage 不变；
7. 运行缺格、复用、错误顺序、损坏来源、损坏输出、覆盖拒绝和 Catalog 隔离反例；
8. 生产 Workbench 与 Codex 内置浏览器完成桌面/移动、四文件导入、矩阵/阶段/wave、三态、
   损坏重试、刷新/返回、键盘和零横向溢出；
9. 检查 Console、Network、同源资源、状态码、外部/写请求和未解释异常；
10. 两套 Python、前端全回归、依赖健康、生产审计与敏感扫描通过；
11. 最终没有预览进程、监听端口、对象 URL、临时上传文件或 `.veritrail-*` staging 残留，
    Git 只包含预期源码与文档；
12. 冻结提交和 `m8-v0.9.0` 标签从 GitHub 远端读回后，才允许后继实现。

若 M8 没有实际执行 wave 内的 Run 重叠，报告必须明确写“调度与 Assignment 验证完成，未证明
真实微并行”。这不阻止 M8 验证当前合同，但不能被后继文档偷换为并行执行能力。

## 退出结论边界

M8 最多可以证明：一个有界全因子 Profile 集合先完成确定性覆盖，再按可复建种子扰动顺序；
全部不可变 Run 被保留，覆盖、假设和来源 Verdict 分层明确，缺格、污染与偶发差异不会被随机
顺序或多数结果掩盖。

M8 不能证明：组件级多变量因果、统计交互、真实并行、任意项目命令、服务/中间件生命周期、
生产容量、完整自举或跨项目通用性。组合 Profile 发现异常后，应回到单变量或 M7 四角色计划
定位原因，而不是从矩阵相关性直接宣布根因。

## 当前实现证据与剩余门禁

- 已实现 BatchPlan 0.1、RunAssignment 0.1、BatchAnalysis 0.1 与 BatchAnalysis Manifest 0.1；
- Python Core 已验证完整笛卡尔积、canonical coverage、`SHA256_RANK_V1`、一/二路 wave 预算、
  seal、Assignment 安全相对目录、M5 Bundle 完整性、四字段固定实现映射、三方 fingerprint、
  phase/wave 时间、来源 Run 不复用、控制投影与稳定/偶发 outcome；
- CLI 已实现 `seal-batch` 与只读 `analyze-batch`，输出四文件、canonical JSON、Manifest、
  不可覆盖和失败 staging 清理；
- 脱敏 2×2 自动化覆盖 `COMPLETE/SUPPORTED`、`COMPLETE/CONTRADICTED`、
  `INCOMPLETE/INCONCLUSIVE`、顺序污染 `INCONCLUSIVE/INCONCLUSIVE`、来源 `FAIL` 保留、
  逐字节复建、损坏来源、路径拒绝和 Catalog Run-only 隔离；
- Workbench `0.9.0-dev.1` 已实现显式四文件选择、Manifest 路径/大小/SHA-256、BatchPlan seal、
  完整笛卡尔积、canonical coverage、`SHA256_RANK_V1`、wave 预算、Analysis ID、slot/Profile/Run
  引用、Profile 计数、reason 与双状态重算；只读视图分开呈现 CoverageStatus、HypothesisStatus、
  来源 ExecutionStatus/Verdict、outcome、矩阵、phase/wave 和“未证明真实并行”边界；
- 前端自动化覆盖四类状态组合、来源 `FAIL` 保留、缺格、未声明漂移、来源证据不足、Plan seal、
  伪造 seed 顺序、额外文件和状态冲突；类型检查、53 项 Vitest、lint 与生产构建通过；
- Python 3.10.6 与 3.13.13 各 108 项全回归通过，M0–M7 冻结消费者未因本次 Workbench 扩展改变；
- `scripts/m8_batch_acceptance.py` 已在 16 GB Windows 主机上执行真实 2×2 批次：先封存
  BatchPlan，再按 coverage 与固定种子 perturbation 顺序串行创建 8 个互不复用的 M5 `run`；
  每个 Run 均完成资源预检、内置静态目标、Chromium 双视口和 cleanup；
- 组合 Profile 在桌面视口产生一次预注册 Console 错误，两次来源 Run 均保持
  `COMPLETED/FAIL`；BatchAnalysis 没有覆盖来源失败，同时得到 `COMPLETE/SUPPORTED`、
  `COMPLETE/CONTRADICTED`、`INCOMPLETE/INCONCLUSIVE` 与顺序污染
  `INCONCLUSIVE/INCONCLUSIVE`；
- 相同输入四文件逐字节复建一致；只改变 seed 时成员、次数和 coverage 不变而 perturbation
  顺序改变；缺格、Run/Bundle 复用、错误顺序、不安全路径、损坏来源、损坏输出、覆盖拒绝和
  Catalog 隔离均已执行；验收结束后计划端口释放且无 `.veritrail-*` staging；
- 本次 wave 成员仍由脚本串行执行，`runtime_overlap_claim=NOT_PROVEN`；它证明调度与 Assignment，
  不证明真实微并行；
- 生产 Workbench 的 Codex 内置浏览器桌面/移动、Console/Network、损坏恢复、history 与最终
  清理终验尚未执行，因此 M8 仍不能冻结。

## 合同记录

- 合同版本：M8 Preregistered Full-factorial Batch Matrix Contract 0.1；
- 前置基线：`m7-v0.8.0` + 文档一致性提交 `c616974`；
- 当前版本：Python Core `0.9.0.dev1`；Workbench `0.9.0-dev.1`；
- 已实现 Schema：BatchPlan / RunAssignment / BatchAnalysis / BatchAnalysis Manifest 0.1；
- 已实现 CLI：`seal-batch`、`analyze-batch`；
- 当前里程碑状态：`REAL SOURCE BATCH VALIDATED`；内置浏览器终验与冻结仍为 `PENDING`。
