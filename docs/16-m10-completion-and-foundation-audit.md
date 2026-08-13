# M10 完成、地基审查与双轮冻结计划

> 状态：`FROZEN_EXECUTION_PLAN / STRESS_AUDITED`
> 计划版本：`M10 Completion and Foundation Audit Plan 0.1`
> 影响层级：`L3_SYSTEM`
> 依赖合同：[M10 Bounded Project Bootstrap Contract 0.2](15-m10-bounded-project-bootstrap.md)
> 目标冻结标签：`m10-v0.11.0`

## 1. 为什么增加这道计划门

M0–M9 的主要事实可以在封存文件、一次性命令和派生分析中静态复核；M10 首次把长运行进程、端口、
owned readiness、浏览器 exercise、取消、失败封存与逆序清理放入同一个动态生命周期。M10 又是
M11 真实项目、M12 前端终稿、M13 系统/代码终审和 M14 发布收束共同依赖的执行地基，因此不能把
“已有若干绿色切片”写成“动态地基已完成”。

本计划只增加 M10 的完成顺序、基础层审查和冻结前验证纪律，不扩大 Contract 0.2 的最大能力声明：

- Windows 11、`C1 PROCESS_COLD`、两个本地可信节点仍是唯一支持范围；
- 单个 Run 内仍严格串行，一个 dependency、一个 application、一个 Chromium Context；
- C2/C3、Docker、Linux/macOS、任意依赖图和生产容量仍为 `NOT_SUPPORTED / NOT_PROVEN`；
- 第二种不同类型真实项目的通用性证明仍属于 M11，不作为 M10 偷渡的新变量；
- 压力轮属于诊断性地基审计，通过不能把“真实并行”改写成正式支持能力。

## 2. 状态必须分开

M10 依次经过以下状态，禁止跳级：

```text
IMPLEMENTING
  -> FEATURE_COMPLETE
  -> FOUNDATION_REVIEWED
  -> SERIAL_VALIDATED
  -> STRESS_AUDITED
  -> RELEASE_GATES_PASSED
  -> FROZEN
```

- 开发期定向测试和全量回归只证明当前切片没有已知回归，不等于 `SERIAL_VALIDATED`；
- 功能未闭环时不得开始最终串行轮或压力轮；
- 审查发现问题后先整改，再重跑受影响自动化；不能带着已知问题进入第一轮；
- 第一轮未完全通过时，第二轮不得启动；
- 资源停止是有效边界事实，但不能掩盖安全、所有权、证据、裁决或清理失败。

## 3. 阶段 A：完成 M10 功能闭环

Contract 0.2 第 15 节的公共退出矩阵必须逐项实现并保留真实证据：

1. C1 正向成功，并用同一 sealed Plan/Profile 再次运行，证明无残留污染；
2. dependency 提前退出，application 从未创建；
3. application readiness 超时，两个节点逆序清理；
4. browser sealed HARD 业务步骤失败，仍生成有效负向 Evidence；
5. preflight `STOP_ESCALATION` 与硬 `ABORT`，零 bootstrap、零 browser；
6. application READY 后用户取消，形成 `USER_CANCELLED / ABORTED/PENDING`；
7. dependency/application 外部端口竞争，不接管、不误杀外部进程；
8. listener owner 与当前 Job 不匹配，不误判 READY、不误杀外部进程；
9. subject 最终状态漂移，不回滚并裁决为 `INCONCLUSIVE`；
10. cleanup 注入失败，继续 best-effort 回收且不得伪装 clean；
11. Evidence staging 注入失败，仍逆序清理并保留可解释失败事实；
12. Catalog 独立接纳或隔离每类 Bundle，Workbench 通过通用账册真实读回适用 Evidence。

每完成一个切片，可以运行定向自动化、兼容回归和残留检查；这些属于开发证据。只有以上矩阵全部
闭环，M10 才能标记 `FEATURE_COMPLETE`。

## 4. 阶段 B：M0–M10 地基系统审查

该审查在 M10 功能完成后、最终测试前执行，只审查 M0–M10 的静态到动态接缝，不替代 M13 在
M12 之后进行的全项目终审。

### 4.1 系统思维审查

逐层核对：

1. **权威与所有权**：Plan、Profile、Preview、ToolBindings、Evidence、Report、Manifest、Catalog、
   Workbench 各自只有一个事实所有者；派生消费者不能反写裁决；
2. **状态机**：每个阶段、停止原因、ExecutionStatus 与 Verdict 的组合可解释，无跳阶段、双启动、
   失败后继续执行或 `ABORTED` 机械映射；
3. **动态资源**：Job、进程树、listener、reader、Chromium、work、staging 和输出目录的创建、使用、
   封存、逆序清理与残留检查形成闭环；
4. **失败与恢复**：成功、业务失败、采集失败、证据失败、清理失败、取消、超时、竞争和漂移保持
   不同语义，不用一个异常捕获掩平；
5. **消费者兼容**：M0–M9 Bundle、CLI、Catalog、Comparison、Pairing、Batch 和 Workbench 的冻结
   行为不被 Plan 0.6 静默改写；
6. **安全与隐私**：无 Shell 绕过、外部进程误杀、路径逃逸、reparse/hardlink 绕过、秘密/绝对路径/
   PID 身份泄漏或代理污染；
7. **资源与观察者效应**：Core、两个节点、Browser 分账，采样不完整或观察开销超限时不能生成
   无条件性能结论；
8. **爆炸半径**：局部修复不能借机重写公共 Schema、全局状态机或 M0–M9 冻结语义。

### 4.2 分层代码质量审查

- `L0`：Workbench 展示、可访问性和错误状态是否只读且不重新裁决；
- `L1`：每个模块职责、资源句柄生命周期、异常边界、超时、命名、重复代码和可测试性；
- `L2`：Profile/Plan/Preview/Evidence/Bundle/CLI 的全部消费者、严格验证、兼容与负向回归；
- `L3`：跨模块状态机、所有权、竞态、失败封存、逆序清理、安全和恢复路径；
- 检查过长函数、隐式共享状态、宽泛异常、布尔语义混用、重复状态映射和测试只覆盖成功路径；
- 审查意见按严重度、证据、影响范围和整改结果归档；未整改的阻断项不得带入最终测试。

## 5. 阶段 C：第一轮——严格串行完整复验

第一轮只在 `FEATURE_COMPLETE` 且基础审查阻断项清零后开始。它是确定性基线轮：

1. 从实时资源、端口、进程和 staging 清洁状态开始；
2. 按第 3 节顺序逐项运行，每次只运行一个 M10 Run；
3. 每项结束立即验证 Bundle/Catalog/Verdict、端口、进程、Job、reader、Chromium、work/staging；
4. 同一 sealed Plan/Profile 至少完成两次正向运行，比较结果并证明第一次未污染第二次；
5. Python 3.10 与 3.13 全量回归严格串行；
6. 前端 test、lint、type-check、production build 与依赖审计严格串行；
7. 真实 Chromium 完成正/负、桌面/移动链路；Codex 内置浏览器完成刷新/返回、失败恢复、物理键盘，
   并检查 Console/Network；
8. 敏感信息、绝对路径、生成物和最终残留均为零。

任一功能、裁决、安全或清理不变量失败，第一轮立即停止，保存事实并回到整改；不得挑选其余绿色
结果拼成通过。全部通过后才可标记 `SERIAL_VALIDATED`。

## 6. 阶段 D：第二轮——16 GB 边界内的受控压力审计

第二轮不是把所有东西无限并行，而是一次只改变一个压力变量，并冻结随机种子、批次、端口、输出
目录、资源软/硬停止线和预期退出条件。

### 6.1 Run 竞争与微并行

- **同 Profile/同端口竞争启动**：验证竞争者只能取得可解释结果，不能双重拥有 listener、误杀外部/
  同伴进程、生成相互污染的 Bundle 或留下残留；不要求所有竞争 Run 成功；
- **独立 Profile/独立端口/独立输出**：并发度按 `1 -> 2 -> 3` 阶梯，只在上一阶资源、证据、清理
  全部满足时升阶；16 GB 主机不继续扩大 Run 实例数；
- **取消与清理交错**：使用固定种子扰动取消点和启动顺序，失败必须可复现；
- 每一 wave 结束后必须回到零 owned 进程、零约定端口、零 staging，再开始下一 wave。

### 6.2 请求并发

“1000”固定表示**一轮总请求数**，不是 1000 个浏览器、1000 个同时自举实例或 1000 RPS。对已就绪
的轻量回环 application，连接复用并按 `1 -> 10 -> 50 -> 100` 个最大在途请求阶梯发送总计 1000 次
请求，分别记录完成数、错误类型、P95/P99、Core/节点/Browser 内存、连接状态和最终清理。请求负载
不能替代 Browser 用户链，也不能把夹具吞吐写成 VeriTrail 的生产容量。

### 6.3 资源与退出规则

- 每轮启动前重新采样；可用内存软停止线初始为 3 GB、硬中止线为 2 GB，正式运行前随同压力计划
  一次性封存，只能调高保护余量，不能观察结果后放宽；
- 发现持续资源软越界、动态端口异常、连接失败、采样不完整或上一 wave 残留时停止升压；
- 触发硬线、失去进程所有权、Evidence 无法解释、清理失败或系统不稳定时立即中止并保存现场；
- 资源停止线按预期触发是边界事实；安全、所有权、证据、裁决或清理不变量失败则阻断 M10；
- 压力轮通过只标记 `STRESS_AUDITED`，Contract 0.2 的“真实重叠运行 `NOT_PROVEN`”声明保持不变。

## 7. 最终冻结门禁

只有以下事实全部成立，才能创建并远端读回 `m10-v0.11.0`：

- 功能矩阵全部完成并有不可变证据；
- 地基系统审查和分层代码质量审查的阻断项已整改并复验；
- 第一轮严格串行完整通过；
- 第二轮在封存停止线内完成，所有不变量成立或按计划安全停止；
- Codex 内置浏览器、Console/Network、双运行时、前端、依赖、安全和清理门禁通过；
- 发布安全扫描的 Report/Verdict 权威、进程/路径身份、浏览器网络、隐私、Markdown、前端语义上界
  和 M10 内存硬限制阻断项全部整改，并按
  [M10 发布安全整改与冻结复验](20-m10-release-security-remediation.md) 从新候选重新验证；
- 工作区干净，本地、`origin/main` 与 GitHub 远端提交一致；
- README、验收文档、里程碑历史和 Contract 0.2 使用同一完成口径。

M10 未冻结前，M11–M14 只能保持 `PLANNED`；不能先进入后继实现，再回来补动态地基。

## 8. 实施记录

- 2026-08-13：计划 0.1 冻结并进入实施；同步纠正“第二类真实项目属于 M10 门禁”的旧进度口径，
  该证明保持归属 M11；
- 2026-08-13：阶段 A 第 6 项完成开发切片。application READY 后 cooperative user cancel 形成
  `USER_CANCELLED / ABORTED/PENDING` 公共 Bundle，CLI Ctrl+C/Ctrl+Break 只请求取消并等待 Evidence/
  逆序清理，Catalog、四流附件、端口与 staging 验真通过；双 Python 开发回归均为 206/206；
- 2026-08-13：阶段 A 第 7 项完成定向开发切片。live Preview 通过后分别抢占 dependency/application
  端口，两条公共链路均在 preflight 安全停止为 `ABORTED/PENDING`；observed runner 未调用，外部
  listener 保持存活，Bundle 仅含 preflight，Catalog 可验真且 attachments/staging 为零；双 Python
  开发回归均为 207/207；
- 2026-08-13：阶段 A 第 8 项完成定向开发切片。dependency/application 的外部 listener 均被 owned
  readiness 识别为不属于当前 Job，拒绝 READY 且不误杀；外部进程按计划自然退出后，owned Job 完成
  适用逆序清理，公共 Bundle 为 `LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL`、零 Browser、四流附件，
  Catalog 与无残留检查通过；双 Python 开发回归均为 208/208；
- 2026-08-13：阶段 A 第 1 项的重复 Run 门禁完成定向开发切片。完全相同的 sealed Plan/Profile 连续
  两次公共正向运行均为 `COMPLETED/PASS`，权威与 Preview 一致，首份 Bundle 未被覆盖；两轮均独立
  Catalog 验真、轮间无残留，M6 Comparison 为 `MATCH`、0 differences；双 Python 开发回归均为
  209/209；
- 2026-08-13：阶段 A 第 9 项完成定向开发切片。watch root 漂移被保留且不回滚，公共测试发现旧
  Verdict 未消费 `SUBJECT_DRIFT` 而错误 PASS；增加 Plan 0.6 专属 `BOOTSTRAP_SUBJECT_DRIFT` 后形成
  `COMPLETED/INCONCLUSIVE`，真实 Browser、Catalog、逆序清理与无残留均通过；双 Python 开发回归均
  为 210/210；
- 2026-08-13：阶段 A 第 10 项完成定向开发切片。应用 cleanup 注入失败后仍继续依赖回收，适用
  attempted/completed 顺序保持 application→dependency；公共 Bundle 以 HARD cleanup 断言形成
  `CLEANUP_ERROR / ERROR/FAIL`，Catalog 复算一致，独立残留检查为零；Python 3.10 首轮全量曾无诊断
  非零退出，受影响 34 项、3.10 完整复跑与 3.13 完整回归随后通过，完整回归均为 211/211；
- 2026-08-13：阶段 A 第 11 项完成定向开发切片。部分 staging 写入失败在 teardown 前固定记录
  `EVIDENCE_STAGING_FAILED`，随后完整逆序清理；受限 fallback Evidence 形成
  `EVIDENCE_ERROR / ERROR/PENDING` 公共 Bundle 并由 Catalog 验真，未知 callback 错误反例被拒绝；
  双 Python 开发回归均为 213/213；
- 2026-08-13：阶段 A 第 12 项完成。真实 `COMPLETED/PASS` 与预检 `ABORTED/PENDING` M10 Bundle
  在同一 Catalog 中被接纳，损坏副本以稳定问题码隔离；生产 Workbench 由 Codex 内置浏览器通过只读
  API 读回 `runtime.bootstrap`，刷新后裁决与完整性不变，Console/Warning 为零且 Catalog/15 个 Bundle
  文件请求均被观察。双 Python 开发回归为 214/214，前端 55/55、lint、type-check、build 与本地
  服务/端口/进程/临时目录清理通过；
- 阶段 A 全部完成，M10 当前为 `FEATURE_COMPLETE`。下一步只能进入阶段 B 地基系统/代码审查；阶段 B
  阻断项清零前不得启动最终串行轮，第一轮通过前不得启动压力轮；
- 2026-08-13：阶段 B 完成。系统/代码审查发现并修复 Plan 0.6 Catalog 未完整重推导 Report、HTTP
  READY 响应后的 listener ownership 竞态、只读 API 校验后重开文件的 verify/use 竞态，并同步
  Workbench M10 版本。整改中一次 `bundle_file` 返回形状回归由 Python 3.10 全量测试以 215/216 拦截，
  恢复兼容后 Python 3.10/3.13 均为 216/216，前端 55/55、lint、type-check、build、依赖审计、
  compileall 和 diff 门禁通过；当前状态为 `FOUNDATION_REVIEWED`。完整审查记录见
  [M10 动态地基系统与代码质量审查](17-m10-foundation-review.md)。下一步进入阶段 C；阶段 C 尚未开始，
  不得把本次整改回归写成 `SERIAL_VALIDATED`；
- 2026-08-13：阶段 C 完成。13 个预注册 method 严格串行覆盖十二类公共退出，批间残留为零；首次
  Python 3.13 在收集阶段因 editable binding 丢失而 35 errors/0 产品测试，本轮按规则停止。修复两个
  venv 的本仓库 binding 后从 Python 3.10 重启全序列，双运行时均为 216/216；前端 55/55、lint、
  type-check、build、依赖审计与 compileall 通过。Codex 内置浏览器真实读回正向 PASS 与业务失败
  FAIL Bundle，刷新/返回、真实键盘、移动视口、Console 与页面资源账册成立；服务、端口、staging 与
  TEMP 最终清零。当前状态为 `SERIAL_VALIDATED`，完整记录见
  [M10 第一轮严格串行完整复验](18-m10-serial-validation.md)；
- 2026-08-13：阶段 D 完成。压力 harness 的前三个候选分别暴露“至多一个 PASS”误写成“必须一个
  PASS”、竞争者仍占声明端口时 owned cleanup 与全局 port-free 混淆，以及 Windows venv launcher
  PID 不能证明真实 listener 所有权三项验收器问题；每次均先修正门禁并从 Wave A 全量重跑，不拼接
  局部绿色。首次完整通过后，发布审查又补强硬停止/超时 worker 子树回收并由双 Python 真实进程树
  测试证明；最终候选 `88d083a` 再次从头完成同端口竞争、独立度 1/2/3、READY 后取消交错与 1000 总
  请求；6 个独立 Run PASS、3 个取消 Run 为 `ABORTED/PENDING`、2 个竞争 Run 安全 FAIL，11 个 Bundle
  与 Catalog 独立验真，最低可用内存 7323 MiB，最终端口、进程和 staging 为零。当前状态为
  `STRESS_AUDITED`，完整记录见
  [M10 第二轮 16 GB 有界压力审计](19-m10-bounded-stress-audit.md)。下一步只能进入阶段 E 发布门禁；
  在最终候选回归、代码质量/安全复核、内置浏览器与 GitHub/tag 读回全部成立前不得标记 `FROZEN`。
- 2026-08-13：阶段 E 安全扫描形成 2 个 medium、9 个 low 和 1 个 M10 资源合同阻断项；整改计划、
  爆炸半径与重新验证顺序已固化到
  [M10 发布安全整改与冻结复验](20-m10-release-security-remediation.md)。实现候选已封闭权威重推导、
  稳定单次读取、进程/目录 identity pin、WebSocket/Service Worker、凭据脱敏、截图确认、Markdown、
  Workbench 权威标签/语义上界和 Job memory limit；最终双运行时、压力、内置浏览器与复扫仍须完成。
- 2026-08-13：阶段 E 实现与本地发布验收完成。整改中先后由严格串行、Python 3.13、Workbench
  type-check 和最终代码复审暴露 browser cleanup 二次等待、Chromium sandbox Job 竞争、派生包权威
  标签遗漏、pinned handle 二次打开及 abort handle 释放问题；每次均修复后从受影响门禁起点重跑。
  最终候选严格串行 13/13，Python 3.10/3.13 均 228/228，Workbench 58/58 与全部门禁通过；最终
  压力轮 11 Runs/0 issues，最低可用内存 6770 MiB，三取消、同端口竞争和 1000 请求均符合预注册
  结果。Codex 内置浏览器又真实完成 PASS/PENDING/FAIL、刷新/返回、键盘、资源账册、移动视口和
  Console 0 复验；最终端口、server/helper、Chromium 与 staging 为零。详细失败事实和安全矩阵见
  [M10 发布安全整改与冻结复验](20-m10-release-security-remediation.md)。当前为
  `VERIFIED / FREEZE_PENDING`；只剩 GitHub 冻结候选与 `m10-v0.11.0` 标签读回，M11 仍不得开始。
