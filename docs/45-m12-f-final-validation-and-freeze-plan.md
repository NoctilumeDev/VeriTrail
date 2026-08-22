# M12-F 总体验收与冻结计划 0.1

> 状态：`M12_F_VALIDATED / FREEZE_CANDIDATE_NOT_COMMITTED`
>
> 日期：2026-08-22
>
> 父合同：[M12 宫阙验迹表现系统重构设计计划 0.1](28-m12-palace-workbench-design-plan.md)
>
> 前置事实：M12-B/C、D1/D2/D3、R1/R2 与 [M12-E Browser Evidence 与全局状态运行事实](44-m12-e-browser-evidence-and-global-state-facts.md)
>
> 功能控制组：`m11-v0.12.0` @ `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40`
>
> 预期影响：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`；禁止越界 `L2_CONTRACT / L3_SYSTEM`

> 2026-08-15 历史阻断：用户在真实浏览器中否决了当时的 M12 Catalog 表现候选。该否决不影响
> M0-M11 的功能事实，也不构成 M12-F 的失败运行；但它使本计划的候选前提不成立。M12-F
> 不得继续启动或形成冻结候选，直到 [M12-R3 参考图优先的 Catalog 重建合同](49-m12-r3-reference-first-catalog-rebuild.md)
> 取得新的用户视觉确认与适用浏览器事实。

> 2026-08-22 收口更新：R3 重建后的 Catalog、Run、Comparison、Pairing 与 Batch 已取得用户逐页视觉和
> 交互确认；M12-F 常规与 `python -O` 总体验收均通过。完整门禁、失败保留和清理事实见
> [M12-F 总体验收与冻结候选运行事实](51-m12-f-final-validation-facts.md)。当前只剩候选提交、tag 与 GitHub
> 精确读回，故 M12 仍不得写成 `FROZEN`。

## 1. 目标、唯一变量与非目标

M12-F 不增加新页面、分析能力、状态、数据或主题选项。它只回答一个问题：

> 当 M12-A 至 E 的表现改动组合在同一生产 Workbench 中，并输入真实 M11、M2、M6、M7、M8 的既有事实时，证据语义、只读边界、键盘链路、响应式和“宫阙验迹”的信息空间是否仍同时成立？

本轮唯一主要变量为：

```text
workbench_presentation_system = palace_evidence_m12_integrated_candidate
```

冻结的受控条件包括：M11 功能控制组、既有脱敏输入、Python Core、Catalog/API、Bundle/Manifest 校验、
Verdict、浏览器采集器、项目依赖锁定、生产构建过程、回环只读服务、串行资源策略和验收矩阵。发现的环境漂移、
输入缺失或越界 diff 必须记录并停止冻结，不能用“视觉工作不影响后端”跳过。

本计划不实施 M13 审查、不发布 GitHub Release、不调整版本语义、不修改 Python/Schema/Catalog/API/Loader、
不添加视觉回归像素门禁，也不因为终验方便而创建新 M11 Run。M12 的 milestone tag 只可能在全部事实成立、
候选提交已形成并完成远端读回后创建；它不是 M14 的发布或 Release。

## 2. 候选与输入预注册

实际验收前先记录候选 `HEAD`、工作树状态、所有 M12 文件所有者、`git diff --check`、生产构建 asset 名称/哈希，
并拒绝未解释的 domain、Core、Schema、Catalog/API、共享状态 token 或 `StatusBadge.vue` 变更。若为修复终验问题
而改变产品代码，原候选失效：保留失败输出，重新记录候选并从本计划的前置门禁完整再跑，不能只补跑失败页面。

生产输入只读使用已在前序事实中审计过的材料：

| 领域 | 固定材料 | 必须保留 |
| --- | --- | --- |
| Runs / Browser | M11 Gate B v2 四个 Catalog Run 与 M2 正、负、损坏 Bundle | `PASS / FAIL / PENDING / PASS`、真实 Console/Network 失败、无 Browser 不等于通过、损坏不展示部分可信内容 |
| Comparison | M11 正向恢复 `MATCH / 0 differences` 与 D1 已有 `DRIFT`、`INCONCLUSIVE` 文件 | Comparison 不借用来源 Run Verdict，也不选择性隐藏不利差异 |
| Pairing | M7 的三态四文件分析包 | 四角色顺序、来源 authority、损坏拒绝、刷新重选 |
| Batch | M8 的四态四文件分析包 | 双状态、固定 slot、来源 `FAIL`、矩阵局部滚动、刷新重选 |

验收器在显示任何内容前验证每个输入存在性、清单、大小和 SHA；不能用 Vue 组件合成对象替代实际 Bundle。输入不成立时，
本轮为 `PENDING` 或 `ERROR`，不是“略过后仍可冻结”。

## 3. 总体验收覆盖矩阵

本计划不把“全部视图 x 全部状态 x 全部视口”伪装成可执行的无界组合。每条硬语义至少有一次完整真实链路，
每种空间压力至少有一次针对性视口；完整矩阵、随机种子和各项实际输入由 M12-F 验收输出记录。

| 代表链路 | 最低真实事实 | 主要视口/交互压力 |
| --- | --- | --- |
| 四轴公共导航与历史 | Pairing / Runs / Batch / Comparison 固定同轴，方向键、`Home/End`、Back/Forward 与目标标题焦点 | `1440x960`、`1024x768`、`390x844` |
| Runs 主链 | Catalog 四个 M11 Run；进入 `PASS`、`FAIL`、`ABORTED / PENDING` 后返回原目录记录 | `1440x960`、`360x800`、长 Run ID |
| Comparison | `MATCH / 0 differences`、`DRIFT`、`INCONCLUSIVE` 与本地文件刷新重选 | `1440x960`、`390x844`、长差异文字 |
| Pairing | 固定四角色顺序、代表性三态、四文件导入/损坏/刷新重选 | `1280x800`、`390x844` |
| Batch | 四种 coverage/hypothesis 组合、来源 `FAIL`、缺格、16 格矩阵、wave/slot、原生 details | `1280x800`、`360x800`，仅具名 matrix region 横滚 |
| Browser 与状态院落 | M2 负向 steps/Console/Network/截图、dialog、M11 no-browser、invalid、operational error、privacy reselect | `1440x960`、`390x844`、`360x800` |
| 可访问性与内容压力 | 长 SHA/URL/错误文字、`ABORTED + PENDING`、reduced motion、forced colors、浏览器实际 200% 缩放 | 桌面、移动与 200% 实际会话 |

根页面在每个矩阵单元必须满足 `scrollWidth - clientWidth = 0`。只有已命名、可聚焦且有语义的 tablist 或 matrix
region 可以局部横滚；任何状态、标题、按钮、焦点环、dialog close button 或证据文字被遮挡、重叠或静默裁断，都是失败。

## 4. 严格执行顺序

所有重任务严格串行。每次 Python、Node、Chromium 或回环服务启动前，重新读取机器档案并检查当前内存、磁盘、端口、
现有监听与 Git 状态；不启动 Docker、中间件、其他项目服务或第二个 Chromium 任务。资源不足时停止本轮、保存现场，
并把 M12 保持为 `IMPLEMENTING`。

1. **候选与所有权预检**：执行第 2 节输入审计，核验 M12 实际 diff 未越过 L0/bounded L1；扫描远程字体、CDN、遥测、
   `.env`、凭据和不应提交的生成物。预检不通过不启动浏览器。
2. **全量静态回归**：串行执行 Workbench test、lint（零 warning）、type-check、production build、`git diff --check`、
   Python 3.10 与项目既有第二解释器的完整 Core 回归；审计锁文件和生产依赖。不得通过删除测试、降低 warning 门槛或
   修改 Core 来使表现层验收变绿。
3. **独立生产 Chromium**：新建专属、不可覆盖的 M12-F 验收脚本；它只服务当前 `web/dist`、冻结 Catalog/Run 和第 2 节输入，
   使用显式空闲回环端口。常规 Python 与 `python -O` 各跑一次；所有硬条件用显式 `require()`，禁止依赖内建 `assert`。
4. **CDP/网络与清理门禁**：记录 Console、page error、request failure、请求方法、origin、状态码、重复请求、根/局部溢出、
   截图摘要及资源快照。只允许同源 `GET/HEAD` 和本地 blob；外部 origin、写请求、未解释 HTTP `4xx/5xx`、Console warning/error、
   page error 或 request failure 均阻止冻结。每轮确认服务线程、端口、进程、临时输出和 SQLite sidecar 全部释放。
5. **Codex 内置浏览器**：使用独立的、由本轮启动的生产预览重新跑矩阵的可见链路。内置浏览器记录真实页面、URL/history、
   原生 file chooser、可见失败、焦点、局部滚动和无障碍交互；response Network/Console 的完整结论仍以第 4 步 CDP 输出为准。
6. **用户物理验收与审美否决**：用户以物理键盘完成十字导航、目录选择/返回、Browser tab/dialog、Pairing/Batch 局部交互，
   并在 200% 缩放下确认 reflow。若 Windows High Contrast 可用，再作人工检视；若不可用，不伪造人工事实，保留自动 forced-colors
   证据。用户同时检查信息检索、结构朱与失败朱区分、院落留白、内部张力和非雾化气韵。
7. **结果分类与冻结候选**：先输出矩阵、失败和清理事实，再按第 5 节分类问题。只有 `Blocker = 0`、`Must Fix = 0`、所有门禁通过
   且用户不否决视觉后，才允许准备 M12 实现提交、重新记录精确候选、创建 `m12-v0.13.0` 并从 GitHub 读回 `main` 与 tag 指向。
   无 GitHub Release；M13 仍保持 `PLANNED`。

## 5. 缺陷分级与停止规则

| 级别 | 定义 | 处理 |
| --- | --- | --- |
| `BLOCKER` | 证据语义、信任/只读边界、状态区分、键盘/焦点、对话框、文件隐私、根溢出、Console/Network、清理或 L2/L3 漂移失败 | 立即停止冻结；保留输出；以新修复切片或本计划新版本处理，再从第 1 步完整重跑 |
| `MUST_FIX` | 不越过契约，但真实内容扫描、响应式、色彩语义、院落结构或用户效率明显违背 M12 父合同 | 记录所有者和复现条件；修复后完整重跑，不能留给 M13 |
| `DEFERRED` | 不影响本合同、不掩盖证据、也不需要改变现有行为的新增想法或偏好 | 写入后续 backlog；不在 M12-F 顺手实现 |

“零 warning、零 smell”不是本轮目标，也不能成为全仓重构理由。反过来，主题好看、截图漂亮或用户主观喜欢，
也不能豁免任一 Blocker 或 Must Fix。计划外的新能力自动归为 `DEFERRED`，除非用户另行开启里程碑。

## 6. 退出条件与非结论

M12-F 可形成运行事实的前提是：

- 所有第 3 节代表链路、状态、视口与人工路径有可追溯输出；
- 两套 Python、Workbench 静态门禁、生产 Chromium 常规/优化模式、内置浏览器与资源/安全/清理全部通过；
- 输入、候选、端口、构建物和网络边界已记录，历史失败不被覆盖；
- 无未解释的 L2/L3 漂移、Blocker 或 Must Fix；
- 用户确认整体是信息由证据关系组织的 VeriTrail 故宫空间，而非泛化雾化东方皮肤、墨叙/暗室藏书复用或普通后台换色；
- 冻结提交、`m12-v0.13.0`、远端 `main` 和 tag 的精确读回均已完成。

M12 冻结仍只证明 M0-M11 已有事实在声明的 Windows 11、16 GB、单机回环、只读输入和实际浏览器边界内保持正确表现。
它不证明 M13 分层代码质量已审查、M14 发布已完成、跨平台、生产容量、后端一致性或任何新产品能力。

## 7. 审阅门禁

- [x] M12 父合同、B/C、D1/D2/D3、R1/R2 与 E 的运行事实已只读审计；
- [x] 唯一变量、固定输入、覆盖矩阵、资源边界、人工与自动化分工已预注册；
- [x] 用户审阅并确认本计划 0.1；
- [x] M12-F 候选、输入与资源预检已经开始；
- [x] M12-F 已形成运行事实；
- [ ] M12 已冻结。

本文件仍是 M12-F 的执行合同；验收事实由文档 51 承担。计划和本地通过不能替代候选提交、标签、
GitHub 精确读回或发布事实。
