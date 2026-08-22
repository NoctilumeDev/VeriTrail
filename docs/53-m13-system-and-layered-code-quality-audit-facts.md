# M13 系统思维与分层代码质量终审事实 0.1

> 状态：`M13_FROZEN / M14_ENTRY_OPEN`
>
> 日期：2026-08-22
>
> 审查范围：`L0 / L1 / L2 / L3`
>
> 冻结能力基线：`m12-v0.13.0^{}` @ `5f32c33ab3dac076151a4fcd9a93a74ccafcfaa9`
>
> 审查计划：`bbab1d3`；有界整改：`a3ba23f`、`63e6354`
>
> 审查后实现坐标：`63e6354fe12782372704c8ad08bc765d84276445`

## 1. 结论

M13 已完成仓库、系统权威链、消费者、状态机、安全、资源、恢复以及 L0–L3 代码质量终审。
审查没有发现需要改变冻结 Schema、Verdict、ExecutionStatus、命令信任模型、Catalog/API 权限或
支持矩阵的 L2/L3 语义缺陷。四项可观察问题均在原所有者内最小修复，最终为：

- `BLOCKER = 0`；
- `MUST_FIX = 0`；
- `DEFERRED = 2`，均有所有者、边界和重新触发条件；
- M12 标签、包版本和公共格式均未移动；
- M14 入口开放，但 M14 仍须另立终局复验合同，不能把本次定向证据冒充最终 Release 证据。

## 2. 仓库与版本基线

审查入口盘点 361 个 tracked 文件，主要分布为 `web 125 / docs 61 / tests 47 / examples 37 /
src 34 / schemas 25 / scripts 19 / .github 3`。大文件热点集中在 Evidence、自举、Plan、Batch、CLI、
Catalog、Windows Job 和 Verdict；体量只作为变更风险提示，没有被单独定性为缺陷。

- Python 包版本保持 `0.12.0.dev1`；Workbench 保持 `0.12.0-dev.1`。
- Python 实测为 3.10.6 与 3.13.13；Node 为 24.14.0，npm 为 11.9.0。
- `m12-v0.13.0^{}` 保持指向 `5f32c33`，M13 没有移动历史标签或改写历史失败 Run。
- 审查实现提交 `a3ba23f` 与 `63e6354` 已逐个推送并从 `origin/main` 读回。

## 3. 系统权威与消费者矩阵

| 事实 | 唯一所有者 | 主要消费者 | 已核对的禁止动作 |
| --- | --- | --- | --- |
| Profile / sealed Plan / Preview | `plan.py`、对应 Schema 与版本分派 | preflight、run、bootstrap、CLI | UI 或执行器不得回写 seal、规则和输入身份 |
| ExecutionStatus 与运行生命周期 | orchestration / command / bootstrap 运行状态机 | Evidence、Report、Catalog、Workbench | Verdict 不得伪造执行完成；清理失败不得被压成成功 |
| Evidence 与附件 | `evidence.py`、`bootstrap_evidence.py` | evaluate、Bundle、Browser Evidence | 先脱敏后哈希；不得信任未校验附件或越界路径 |
| Verdict | `verdict.evaluate` | Report、Bundle validator、Catalog、派生分析 | Report、Catalog、API、UI 均不得产生第二套裁决 |
| Manifest / Bundle | Bundle 构造与 `validate_bundle` | Catalog、Comparison、Pairing、Batch、API | 必须复核 containment、size、SHA、权威文件和重新裁决 |
| Catalog | `catalog.py` 从 Bundle 重建的 SQLite 派生索引 | loopback API、Workbench | 不信任 Report 自报，不反写 Bundle，不把索引当权威 |
| Comparison | `comparison.py` | CLI、Workbench | 只比较通过来源校验的同计划 Run，不替代来源 Verdict |
| PairedAnalysis | `pairing.py` | CLI、Workbench | 固定角色和预注册 outcome，不自动扩大因果范围 |
| BatchAnalysis | `batching.py` | CLI、Workbench | 固定 seed、Profile 与 slot，不把串行 wave 宣称为真实并行 |
| loopback API | `local_api.py` | Workbench | 只允许 GET/HEAD；严格 Host、路径、query、body 与安全响应头 |
| Workbench | Vue 组件、domain loader/validator 与页面状态 | 本地用户 | 只显示并校验输入，不拥有 Verdict、Bundle 或派生分析事实 |

源到汇追踪确认：sealed authority 先进入执行/采集状态机，再形成不可变 Evidence、确定性 Verdict、
Bundle、可重建 Catalog、三类派生分析、只读 API，最后才进入 Workbench。没有发现 UI 反向成为权威、
Catalog 信任自报 Verdict、派生页绕过来源校验或 API 获得写权限的路径。

## 4. 状态、失败与恢复矩阵

| 条件 | ExecutionStatus | Verdict | 恢复与证据要求 |
| --- | --- | --- | --- |
| 所有决定性断言通过且证据完整 | `COMPLETED` | `PASS` | 封存全部权威与附件，清理 owned 资源 |
| 决定性断言有可证明反例 | `COMPLETED` | `FAIL` | 保留不利 Evidence，不允许重写规则或删除失败 Run |
| 变量污染、无法归因或来源互相矛盾 | 通常 `COMPLETED` | `INCONCLUSIVE` | 保留污染/边界事实，不伪装成业务失败 |
| 中止、未完成、证据缺失或未求值 | `ABORTED` 或非完成态 | `PENDING` | 封存已有事实，逆序清理，不能猜测 PASS/FAIL |
| Core/Subject/Browser 或 staging/cleanup 异常 | 对应错误/中止态 | 不得自动 PASS | 分层记录问题码、资源账册和最终清理状态 |

命令、自举与 Browser 链路均继续使用显式 argv/cwd/environment、owned PID/Job、readiness、逆序清理、
对象 URL 释放和端口/SQLite sidecar 回零。外部进程不在 owned 集合时不会被误杀；用户态 TOCTOU、
恶意代码隔离、跨平台和生产容量仍明确属于未证明能力。

## 5. 已关闭发现

### FND-M13-001：优化模式会移除历史验收关键断言

- 分类：`MUST_FIX / L1`。
- 事实：M3、M4、M6、M7 的历史验收脚本使用裸 `assert` 作为通过门禁；`python -O` 会删除这些条件，
  可能让验收器 fail-open。
- 修复：提交 `a3ba23f` 将关键断言改为显式 `require`，并在
  `tests/test_browser_acceptance_metrics.py` 增加 AST 回归，禁止这些脚本重新引入裸断言。
- 结果：普通与 `python -O` 的 M3 定向验收均通过；最新 HEAD 的 M12-F 常规与优化总验收也均通过。

### FND-M13-002：公共安全边界文档落后于冻结能力

- 分类：`MUST_FIX / L1`。
- 事实：`SECURITY.md` 仍停留在 M10/M3，且把 Browser 附件边界写成仅 PNG/JPEG，无法准确描述 M11/M12
  的单 application、自举、文本附件和只读 Workbench 边界。
- 修复：提交 `a3ba23f` 同步 M12/M11 冻结坐标、支持矩阵、文本附件、信任边界和未证明能力。
- 结果：安全说明与产品、架构、验收、冻结标签一致，没有扩大能力声明。

### FND-M13-003：Catalog 空集合仍使用旧的“贴卡片”视觉

- 分类：`MUST_FIX / L0`。
- 事实：有效 Catalog 但 0 Run 时仍由全局 `components.css` 提供虚线、米黄色不透明卡片，和当前连续纸面、
  页面所有权及用户已确认的 M12 视觉语法冲突。
- 修复：提交 `63e6354` 删除全局遗留样式，改由 `catalog-reference.css` 拥有透明连续纸面空态；增加
  style-ownership 回归，禁止虚线、阴影和旧卡片重新进入全局层。
- 结果：桌面 1600×1000 与移动 390×844 真实浏览器均无根横向溢出，Console warning/error 为 0；
  用户发现的“漏网之鱼”已关闭。

### FND-M13-004：历史计划公开写死本机用户名路径

- 分类：`MUST_FIX / L0_DOCUMENTATION`。
- 事实：文档 43 把机器画像入口写成具体用户目录，既不便迁移，也泄漏与产品合同无关的本机用户名。
- 修复：M13 事实收口将其改成 `%USERPROFILE%\\.codex\\machine-profile.md`；内容语义和 M12 历史结论不变。
- 结果：tracked 文件不再包含该本机绝对路径。凭据形状扫描剩余命中均为脱敏负向测试使用的明确假数据，
  这些样本必须保留，不能为了“扫描零命中”削弱安全回归。

## 6. 延期维护债

### DEFERRED-M13-001：Evidence / bootstrap Evidence 的受控局部导入接缝

- 所有者：Evidence 与 bootstrap Evidence 层。
- 当前判断：局部导入用于避免共享封存逻辑形成模块初始化环，现有调用路径、异常和负向测试完整；没有
  发现第二套 Evidence 权威、运行时递归或资源泄漏。
- 重新触发：新增第三类 Evidence 构造器、共享函数开始拥有状态，或局部导入导致初始化顺序/测试隔离缺陷时，
  先补 characterization，再提取无状态的独立封存模块。

### DEFERRED-M13-002：Workbench domain validators 的状态字面量重复

- 所有者：`web/src/domain` 的 Bundle、Catalog、Comparison、Pairing、Batch 输入校验器。
- 当前判断：重复只承担消费者侧拒绝未知值，不产生 Verdict，也没有出现不同页面解释同一冻结状态的事实。
- 重新触发：公共状态集合改变、增加新派生分析消费者，或任意两个 validator 对同一输入给出不同结果时，
  在 domain 层提取共享只读枚举；不得从 UI 反向成为 Python 裁决权威。

## 7. 安全审查

Codex Security 标准单轮仓库扫描以 M13 计划基线 `bbab1d3` 运行，scan ID 为
`ec501b47-e23f-4a03-8ed1-d45b9c80b4ae`。Threat modeling 与 finding discovery 覆盖均为 `6/6`，
没有形成可报告漏洞或候选攻击路径。

补充事实：

- `npm audit --registry=https://registry.npmjs.org` 为 0 vulnerability；国内镜像不实现 audit 接口的失败
  单独记录为 registry 能力问题，没有伪装成依赖安全通过；
- Python 3.10/3.13 两个环境的 `pip check` 均为 0 broken requirement；本机未安装 `pip-audit`，因此没有
  把 `pip check` 外推成完整 CVE 数据库审计；
- 扫描器 Python 3.10 预检因缺少 `tomllib` 停止后，改用项目已验证的 Python 3.13 完成；
- 未认证 TAC advisory 查询不可用，已作为外部情报限制披露；不影响本地静态来源到汇结论。

本次安全扫描实测消耗：总 token `7,135,147`，输入 `7,119,539`（其中 cached `6,976,256`），输出
`15,608`，reasoning `2,685`，thread count `1`。

## 8. 回归与真实运行证据

| 门禁 | 结果 |
| --- | --- |
| Python 3.10 全量 | `279 / 279` 通过 |
| Python 3.13 全量 | `279 / 279` 通过 |
| Workbench 全量 | 13 个测试文件、`156 / 156` 通过 |
| Workbench lint / TypeScript / Vite production build | 全部通过 |
| 两个 Python 环境 `pip check` | 0 broken requirement |
| npm 官方 registry audit | 0 vulnerability |
| M3 `python -O` 定向验收 | 5 组检查、102 请求、0 错误、`PASS` |
| M12-F 最新 HEAD 常规总验收 | 13 组检查、636 请求、`PASS` |
| M12-F 最新 HEAD `python -O` 总验收 | 13 组检查、636 请求、`PASS` |
| 两轮 M12-F 网络边界 | 外部 origin 0、写请求 0、HTTP 错误 0 |
| 两轮 M12-F 最终清理 | 端口释放、线程停止、SQLite sidecar 0 |
| Catalog 0 Run 真实浏览器 | 桌面/移动无根溢出，Console warning/error 0 |
| 敏感与绝对路径复核 | 无真实凭据；本机用户名路径已移除 |

M12-F 首次直接消费旧 `tmp` Gate-B 输入时以 `ARTIFACT_ROOT_MISMATCH`/“Artifact 根目录与 Catalog
快照不匹配”在 0 检查处拒绝，并释放端口、停止线程、保持 sidecar 为 0。这是冻结输入仍绑定迁移前绝对
证据根的既有负向事实。随后使用文档 51 登记的、内容集合不变且重建根绑定的脱敏冻结输入，常规和优化
两轮完整通过。失败没有被覆盖，也没有为了变绿而改写旧 Catalog。

全量 Python 3.13 曾在 Playwright 关闭阶段打印一次异步清理诊断，但退出码与 279 项均通过；后续两个
生产总验收均再次证明 Browser、服务线程、端口和 SQLite sidecar 回零，未观察到持续泄漏。全局
`py -3.13` 指向另一套缺少项目绑定/pywin32 的环境，其失败按环境不满足前置条件记录，没有混入产品结论。

## 9. 出口与 M14 边界

M13 出口门禁已经满足：权威链、消费者、状态/失败/恢复矩阵、L0–L3、依赖、安全、真实 Browser、
残留与远端读回均有事实；全部 Must Fix 已关闭，两个延期项均没有当前可达缺陷。

M14 可以开始独立合同，但只能执行整改后终局复验、归档和发布收束。它仍须覆盖两个真实目标、支持矩阵内
完整链路、桌面/移动/键盘、负向恢复、资源清理、双 Python、依赖/安全、公共文档、GitHub 与最终 Release
读回。M13 不证明生产容量、C2/C3、Docker、跨平台、恶意代码隔离、wave 真实并行、统计显著性或 AI 裁决。
