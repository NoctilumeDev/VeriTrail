# M10 动态地基系统与代码质量审查

> 状态：`FOUNDATION_REVIEWED`
> 审查日期：2026-08-13
> 审查范围：M0–M10 静态证据链到 Plan 0.6 动态生命周期的接缝
> 依据计划：[M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md)
> 后续门禁：阶段 C 严格串行完整复验尚未开始

## 1. 结论

M10 的阶段 B 已完成。审查发现的四项阻断/发布一致性问题均已按最小爆炸半径整改，并通过受影响
回归与双 Python 全量回归；当前没有已知阻断项，可以进入阶段 C，但不得据此标记
`SERIAL_VALIDATED`、`STRESS_AUDITED` 或 `FROZEN`。

本次审查只证明：M0–M10 的已实现接缝在当前代码与自动化覆盖范围内没有遗留的已知地基阻断项。
它不替代最终串行真实运行、16 GB 压力审计、内置浏览器终验、安全复核、远端提交/标签读回，也不
替代 M12 之后面向完整产品的 M13 终审。

## 2. 系统思维审查结果

| 维度 | 结论 | 关键事实 |
| --- | --- | --- |
| 权威与所有权 | 通过（整改后） | Catalog 现在对 Plan 0.6 的全部 Evidence 重新执行 Core 确定性裁决，并逐字段比对 Report；派生索引不能接受一份仅同步修改 Report/Manifest 的自洽伪报告 |
| 状态机 | 通过（整改后） | bootstrap 已开始的 Bundle 同时检查 `execution_status` 与 Evidence 推导结果；状态冲突固定拒绝为 `BOOTSTRAP_STATUS_CONFLICT`，派生字段漂移固定拒绝为 `BOOTSTRAP_REPORT_DERIVATION_MISMATCH` |
| 动态资源 | 通过（整改后） | owned readiness 在 HTTP 响应之后再次夹取 Job process set 与 listener owner；响应期间 ownership 变化不能计为成功 |
| 失败与恢复 | 通过 | 既有公共矩阵保持区分预检停止、业务失败、超时、取消、漂移、清理失败和 Evidence staging 失败；本轮未合并这些语义 |
| 消费者兼容 | 通过（发现并修复回归） | Plan 0.1–0.5、CLI、Bundle、Catalog、Comparison、Pairing、Batch 与 Workbench 全量回归通过；本轮曾破坏 `bundle_file` 四元组形状，测试当场拦截并恢复 |
| 安全与隐私 | 通过（整改后） | Bundle/静态文件改为同一 handle 有界读取、身份复核后直接发送已验 bytes，消除“校验一个文件、重新打开另一个文件”的 verify/use 竞态；未发现 Shell/eval、前端原始 HTML 注入或新增秘密持久化路径 |
| 资源与观察者效应 | 通过（边界保持） | 本轮没有扩大并行度、资源声明或采样结论；本地 API 单文件仍有 10/16 MiB 上限，阶段 D 的 16 GB 停止线保持不变 |
| 爆炸半径 | 通过 | 未修改公共 Schema、ExecutionStatus/Verdict 枚举、M0–M9 冻结语义或 M9 Job 后端；所有整改集中于 Plan 0.6 Catalog 验真、M10 readiness 和只读 API 读取接缝 |

## 3. 发现、整改与复验

### FND-M10-001：Plan 0.6 Catalog 未完整重推导 Report（阻断）

**事实**：预检停止 Bundle 会由 Catalog 重新裁决，但 bootstrap 已开始的 Bundle 只核对权威身份、
Evidence 结构和 browser 引用。操作者若同时修改 Report 与 Manifest，Catalog 可能接纳与 Evidence 不
一致的 `execution_status`、Verdict 或派生字段。

**整改**：Catalog 统一加载并严格验证全部 Evidence，调用既有 Core `evaluate` 重新推导
`execution_status`、`verdict`、`reasons`、`assertions`、`missing_evidence` 和 `contamination`；状态冲突
与派生漂移使用稳定问题码拒绝。

**复验**：新增 Report Verdict 篡改和 ExecutionStatus 篡改反例；合法 Plan 0.6、预检停止及旧版本
Bundle 继续通过全量回归。

### FND-M10-002：HTTP READY 响应后的 ownership 竞态（阻断）

**事实**：旧实现只在发出 HTTP 请求前核对 listener owner。若 owned listener 在请求期间退出、外部
进程抢占同一端口并返回 200，响应可能被错误计入连续成功。

**整改**：收到响应后再次执行 `Job set A -> listener -> Job set B` 夹取，并要求 listener PID、预期
owner 和进程集合稳定。listener 改变立即形成 `LISTENER_OWNERSHIP_MISMATCH`；Job 集合变化只记录一次
非成功观察并继续等待稳定状态。

**复验**：新增“响应后 owner 被外部 PID 替换”与“稳定 owned listener”单元测试，并复跑真实公共
成功、owner mismatch、Windows service 和 bootstrap lifecycle 测试。

### FND-M10-003：只读 API 存在校验—使用时间窗（阻断）

**事实**：旧实现先按路径、metadata 和哈希校验 Bundle 文件，HTTP handler 随后再次打开路径发送；
两次打开之间发生替换时，实际响应内容不再是刚验证的 bytes。静态资源也存在同类路径重开窗口。

**整改**：通过单一文件 handle 有界读取，比较读取前、opened handle 与读取后的文件身份，再对内存
bytes 计算 Bundle 哈希；handler 只发送已经验证的 bytes，不再重新打开路径。静态资源读取期间变化
固定返回 `STATIC_CHANGED`。

**复验**：新增“验证后再修改源文件，已返回内容仍为原始已验证 bytes”测试；路径逃逸、源变化、
媒体类型和 API 既有测试继续通过。

### FND-M10-004：Workbench 包版本仍停留在 M9（发布一致性）

**事实**：Python Core 已为 `0.11.0.dev1`，M10 合同也固定 Workbench `0.11.0-dev.1`，但
`package.json` 与 lockfile 根包仍声明 `0.10.0-dev.1`。

**整改**：只同步根包与 lockfile 根包版本为 `0.11.0-dev.1`，不更新依赖树。

**复验**：前端测试、lint、类型检查和 production build 均以新版本通过。

## 4. 分层代码质量审查

### L0 表现层

Workbench 仍只消费 Catalog/Bundle 事实，不增加执行入口、在线写或前端裁决。通用 Evidence loader
对文本输出保持转义；本轮搜索未发现 `v-html`、直接 `innerHTML` 或把红色普通强调与失败语义混用的
新增路径。M12 的完整视觉、响应式和无障碍终审仍按原路线执行。

### L1 组件内部

抽查了命令、自举、readiness、Evidence、Catalog、API、Browser、Job 和清理模块的资源句柄、超时、
异常边界与负向测试。M10 动态函数中存在若干较长函数；它们目前以明确阶段和大量失败分支维持合同
对应关系，且全量回归稳定。仅为缩短行数进行拆分会同时触碰状态机、Evidence 映射与清理路径，因此
登记为非阻断维护债，不在冻结前做无行为收益的大改。

### L2 公共契约

重点复核 Plan/Profile/Preview/Evidence/Report/Manifest/Bundle/Catalog/Comparison/Pairing/Batch/
Workbench 消费矩阵。FND-M10-001 修补了唯一发现的 Plan 0.6 派生权威缺口；公共 Schema 和旧版本
语义未变。`CatalogApplication.bundle_file` 整改时曾从既有四元组缩为三元组，Python 3.10 全量回归
以 215/216 立即失败；随后恢复四元组兼容形状并完成双运行时 216/216。该失败事实保留，不能把最终
绿色写成“第一次就通过”。

### L3 系统级

复核了 Preview 到 preflight 的竞态、Job/listener/HTTP 交叉所有权、Browser 进入条件、取消、失败
封存、subject drift、best-effort 逆序清理、Catalog 独立重验和文件只读供应链。FND-M10-002 与
FND-M10-003 已封闭两个真实竞态窗口；仍按合同明确承认用户态多次采样不是内核原子事务，M10 不宣称
恶意代码隔离或 TOCTOU 已被数学消除。

## 5. 回归与依赖证据

| 门禁 | 结果 |
| --- | --- |
| Python 3.10 全量 | `216/216 PASS` |
| Python 3.13 全量 | `216/216 PASS` |
| Workbench Vitest | `55/55 PASS`，8 files |
| Workbench lint | `PASS`，0 warnings |
| Workbench type-check | `PASS` |
| Workbench production build | `PASS` |
| Python compileall | `PASS` |
| `pip check` | `No broken requirements found` |
| npm production/full audit | 官方 npm registry 一次性审计均为 0 vulnerabilities |
| `git diff --check` | `PASS` |
| 动态残留复核 | 约定端口 18770–18772 无 listener，`.veritrail/staging` 不存在 |

npm 审计第一次从仓库根目录执行，因该目录没有 lockfile 而失败；第二次使用本机默认镜像时，镜像
没有实现 security audit endpoint 并返回 404。随后没有修改持久化 npm 配置，只对该两次审计命令
显式使用官方 registry，生产依赖和完整依赖均得到 0 vulnerabilities。探针失败与有效结论分开保留。

## 6. 已知非阻断项与下一步

- 长函数与重复阶段映射登记为维护债；只有在后续发现可观察行为缺陷，或能建立独立 characterization
  门禁时，才按 L2/L3 变更单独拆分，不能混入最终验收；
- Windows 用户态 ownership 采样只能降低误判窗口，不能升级为恶意对手模型下的原子隔离；
- 本轮自动化是整改回归，不是阶段 C 的冻结候选串行轮；
- 第二项目通用性、前端终稿、全项目终审和终局发布分别仍属于 M11–M14。

下一步严格按计划进入阶段 C：从实时清洁状态开始，逐项串行执行公共退出矩阵、双运行时、前端、
依赖、安全、真实 Chromium 与 Codex 内置浏览器门禁。阶段 C 完整通过前不得开始阶段 D 压力审计。
