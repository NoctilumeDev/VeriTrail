# M12-D3 Batch 双状态矩阵与 Wave 账册表现计划 0.1

> 状态：`COMPLETE / USER_CONFIRMED / RUNTIME_VALIDATED / M12_NOT_FROZEN`
>
> 日期：2026-08-14
>
> 前置事实：[M12-D1 Comparison 运行事实](35-m12-d1-comparison-facts.md)、[M12-D2 Pairing 运行事实](40-m12-d2-pairing-facts.md)
>
> 当前代码基线：D2 已闭环的工作树
>
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
>
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 问题、目标与单一变量

当前 Batch 仍借用 `comparison-court`、`comparison-court__heading` 与 `comparison-boundary`；CoverageStatus、
HypothesisStatus、Profile 矩阵、wave/slot 来源账册和原因区虽然功能正确，但视觉上仍是同一类卡片、
连线和状态色的堆叠。它容易让人误读为：

- `COMPLETE` 等于 `SUPPORTED`；
- `CONTRADICTED` 等于来源 Run `FAIL`；
- 同一个 wave 的 slot 已证明真实并行；
- 缺格或污染只是较淡的“普通状态”。

本切片唯一主要变量是：

```text
batch_analysis_presentation = matrix_and_wave_ledger_m12
```

目标是让现有、可信的 BatchAnalysis 表达其原有关系：

```text
CoverageStatus       HypothesisStatus
矩阵是否完整可信  ->  预注册结果是否被支持
        |                       |
Profile matrix              wave / slot ledger
        \                     /
         来源 Run ExecutionStatus / Verdict
```

上图是信息依赖和阅读次序，不是 Coverage 导致 Hypothesis 的因果箭头，也不等于来源 Run 的 Verdict。D3 不增加
矩阵、wave、统计、调度、执行、导入或状态能力。

## 2. 固定输入与反例

生产验收固定使用 M8 已完成的真实运行材料，不新建 M8/M11 Batch，不修改或提交历史 artifact：

| 状态组合 | 目录 | 必须保留的事实 |
| --- | --- | --- |
| `COMPLETE / SUPPORTED` | `artifacts/m8-batch-runtime-v3-20260811/analyses/supported` | `combined` Profile 的来源 Run 有 `FAIL`，而 HypothesisStatus 仍为 `SUPPORTED` |
| `COMPLETE / CONTRADICTED` | `artifacts/m8-batch-runtime-v3-20260811/analyses/contradicted` | 覆盖完整，但预注册 outcome 稳定不符 |
| `INCOMPLETE / INCONCLUSIVE` | `artifacts/m8-batch-runtime-v3-20260811/analyses/incomplete` | 固定 slot 缺失，来源 Run 未提供 |
| `INCONCLUSIVE / INCONCLUSIVE` | `artifacts/m8-batch-runtime-v3-20260811/analyses/inconclusive` | `WAVE_ORDER_MISMATCH` 仍可见，不能被矩阵计数掩盖 |

每个目录必须只通过既有四文件入口读取：`batch-analysis-manifest.json`、`sealed-batch-plan.json`、
`batch-analysis.json`、`batch-analysis.md`。损坏 `batch-analysis.json` 一字节后必须拒绝，页面不显示部分可信
Batch；重新选择完整 `SUPPORTED` 四文件才可恢复。

## 3. 不变量、所有权与停止线

### 3.1 必须保持不变

- `web/src/domain/batch.ts`、`web/src/domain/types.ts`、BatchPlan seal、Manifest/SHA、Analysis ID、
  `SHA256_RANK_V1`、矩阵/slot/wave 权威顺序、coverage/hypothesis 规则和本地 File 生命周期；
- `App.vue` 的公共视图、URL/history、Loader、错误/重选、文件 input、焦点入口与可访问名称；
- Profile、slot、wave、reason、limit、ExecutionStatus、Verdict、outcome、文字语义与 `data-testid`；
- `StatusBadge.vue`、所有 token、Comparison、Pairing、Runs、Browser Evidence、Core、Catalog/API、Schema 与安全边界；
- `role="region"`、`aria-label="全因子 Profile 矩阵"`、`tabindex="0"` 的局部矩阵滚动合同，以及原生 `details/summary`。

### 3.2 允许所有者

| 文件/区域 | 允许工作 | 明确禁止 |
| --- | --- | --- |
| `web/src/components/BatchAnalysisView.vue` | 仅私有表现分组、class、`data-batch-*` 与标题/账册组合 | 改写 loaded 数据、status/slot/wave 算法、roles、导入或文件输入流程 |
| `web/src/styles/components.css` 中 `.batch-*` | 新建 Batch 私有 court、双状态门、矩阵、wave、原因、边界与响应式规则；删除被本切片替代的旧 `.batch-*` | 改 `.comparison-*`、`.paired-*`、`.status-badge` 或 token 语义 |
| `web/tests/batch.test.ts` | 四种状态组合、矩阵/slot 顺序、缺格、来源 FAIL、原因和长内容的局部回归 | 改 Loader/domain 断言以迁就表现 |
| `scripts/m12_d3_batch_acceptance.py` | 独立生产 Chromium、Network、清理和输出事实 | 改产品代码或覆写 M8 脚本 |

若为了布局需要改 App、共享状态组件、domain、Core、Schema、Catalog/API 或 CSS token，立即停止；这将自动升级为
`L2/L3`，本计划不授权继续实施。D3 不得用追加全局 override、`!important`、新的视觉库、图片、CDN、远程字体、
图标库或遥测来绕过局部所有权。

## 4. 空间、状态与响应式合同

### 4.1 双状态门：同殿不同职

CoverageStatus 与 HypothesisStatus 是并列、但职责不同的两扇门：

- 每扇门都保留状态文字、中文职责、图形标记和简短的可审计事实；
- `COMPLETE` 只表示覆盖完整可信，`SUPPORTED` 只表示预注册结果被支持；二者不得共用 PASS 语义或相同徽章；
- `INCOMPLETE` 必须明确“缺”，`INCONCLUSIVE` 必须明确“疑”；它们不使用来源 `PENDING/FAIL` 的颜色或词义；
- `CONTRADICTED` 使用分析专属金赭，来源 `FAIL` 继续由原生 Verdict Badge 表达；
- 双门之间只能用中轴、间距和层级表达前置关系，不能画成“覆盖完整必然支持假设”的强因果箭头。

桌面可同列呈现两门；窄屏按 `CoverageStatus -> HypothesisStatus` 纵向展开。文字、位置、边界和固定标题必须在
颜色失效时仍表达双状态。

### 4.2 格局：矩阵是主体，不是卡片附件

Profile matrix 是 Batch 的主体。它保留真正的 `table`、`scope`、具名可聚焦滚动 region 和最小表宽：

- 桌面将 matrix 放在状态门后、wave 前，用台基、细边界和列标题形成格局；不在表外增加四宫格摘要卡；
- `mismatch_count > 0` 保留数字、表格位置和可见边界，不能只换背景色；
- 在 `390 x 844` 和 `360 x 800`，表格只允许在 `.batch-matrix-scroll` 内横向滚动，根页面始终为 `0px` 横向溢出；
- 不通过缩小文字到不可读、裁剪列或把 table 改成无语义 div 网格来避免滚动；
- 从本地四文件 input 按真实 `Tab` 前进，矩阵 region 仍是确定且可见的焦点目标。

### 4.3 行次：wave 只是封存账册

wave 使用连续账册而不是一叠同等卡片：phase/repetition/wave 是行次标题，slot 保持现有 loaded 顺序。每个 slot 仍显示
position、Profile、slot ID、来源 Run、Bundle 摘要、ExecutionStatus、Verdict 和原生 `details` outcome：

- `MISSING` 永远留在其预注册 slot 位置，并同时显示文字和缺口边界；
- `FAIL` 来源 Run 不可被 `COMPLETE/SUPPORTED` 遮蔽；
- `details/summary` 保持原生交互和焦点，不做无法键盘操作的伪折叠面板；
- `WAVE_ORDER_MISMATCH` 等 reason 在“判词”段独立出现；
- 页面必须继续显式写出“wave 不证明真实并行”和“Profile 信号不是统计显著性”。

### 4.4 故宫气韵与色彩边界

空白由双门、矩阵台基、wave 行与后方边界共同界定，不使用雾化、柔焦、渐变光斑、龙纹、屋檐、圆形徽章或红金大面积铺陈。
石青、玉色、金赭、青灰与墨形成内部张力；结构朱只保留既有固定空间用途，真实 FAIL/ERROR 的状态语义优先。

## 5. 精确 DOM 与局部自动化退出条件

实现可增加 Batch 私有 class 或 `data-batch-phase`/`data-batch-wave`，但必须满足：

1. `Batch Analysis` 继续是公共 H2；只有应用名称是 H1；`local-batch-input` 继续由唯一、原生、可访问的 label/input 拥有；
2. `batch-coverage-status` 与 `batch-hypothesis-status` 始终同时存在，且所有状态文字、`aria-label` 与值不变；
3. `batch-profile-matrix` 保持 Profile 和 dimensions 的权威行/列顺序；每个 wave 的 slot DOM 顺序等于 `analysis.slots`；
4. `batch-wave-list` 中保留来源 Execution/Verdict，`batch-reasons` 中保留 status reason，`batch-boundary` 中保留非并行/非统计边界；
5. `COMPLETE/SUPPORTED` 中来源 `FAIL` 可见；`COMPLETE/CONTRADICTED` 的不符 count/reason 可见；
   `INCOMPLETE/INCONCLUSIVE` 的 `MISSING` 不换位；`INCONCLUSIVE/INCONCLUSIVE` 的 `WAVE_ORDER_MISMATCH` 可见；
6. 长 Profile ID、Run ID、SHA、reason 和 JSON 内容不撑破根页面；局部 code 可换行，matrix 只在具名 region 滚动；
7. 损坏输入没有 Batch View，显式重选才恢复；刷新和 Back/Forward 不持久化 File；十字东向进入仍将焦点置于 `view-batch-title`。

局部测试先写入四种状态、双状态独立、矩阵/slot 顺序、来源 FAIL、缺格、不符 reason、长内容和 native details 的断言，
再改私有 DOM/CSS。不得删除既有 M8 Loader 负向测试或把真实状态替换为截图比较。

## 6. 严格实施与验收顺序

不启动 Docker、中间件、第二项目栈或任何 M8 新运行；全部工作在当前 16 GB 主机上串行进行。

1. **局部回归先行**：扩展 `batch.test.ts` 的合同断言，审查已触及文件只属于本计划所有者；
2. **私有表现实现**：重组 `BatchAnalysisView.vue`，以 `.batch-*` 完整取代其 `comparison-*` 外壳依赖；只在 `.batch-*`
   区域替换 CSS，并实现桌面、920px、720px 的局部规则；
3. **静态门禁**：串行运行完整 `npm test`、lint 零 warning、type-check 和 production build；`git diff --check` 必须通过；
4. **独立生产 Chromium**：新增 `scripts/m12_d3_batch_acceptance.py`，复用 M11 Gate B 的只读 Catalog 服务和第 2 节四份
   M8 Batch 输入。显式回环端口、输出拒绝覆盖、无 Docker；常规与 `python -O` 各独立运行一次，脚本只能使用显式
   `require()`，不得依赖内建 `assert`；
5. **生产浏览器断言**：验证四种状态、双状态和来源 Verdict 分离、matrix/slot/wave 顺序、`MISSING`、
   `WAVE_ORDER_MISMATCH`、native details、损坏拒绝/恢复、刷新重选、Back/Forward、1440/390/360px、局部矩阵滚动、
   根溢出、Console、page error、request failure、同源 `GET/HEAD`、端口/线程/SQLite sidecar 清理；
6. **Codex 内置浏览器**：从东向进入，真实选择 `SUPPORTED` 四文件，核对 Coverage/Hypothesis 与来源 FAIL 的分离；
   使用系统 `Tab` 进入 matrix region、实际横向滚动该局部区域、展开一个原生 outcome `details`，再验证刷新后重选。
   再按可用时间导入其余三种状态，确认缺格、稳定不符和 wave order 污染没有视觉吞并；内置浏览器只记录真实交互、
   焦点和可见内容，Network response/Console 结论仍由 Chromium/CDP 记录；
7. **事实归档**：所有门禁通过后才写 D3 运行事实、更新 README/`milestones.md`/`AGENTS.md`/D 状态；再决定是否进入 M12-E。

任何失败先保留本地忽略输出，定位唯一当前变量，修复后使用新输出目录复跑；不得临时换成较短矩阵、较少状态或更容易的
历史包。

## 7. 非目标与交接

D3 不证明 Batch 的统计效度、真实微并行、M11 中真实 Batch、Browser Evidence 终稿、全局 loading/error、
forced-colors、200% zoom、色觉差异、M12 冻结、版本标签或发布。它不重开 M8，也不把 `runtime_overlap_claim=NOT_PROVEN`
改写为已证明。

- [x] D1、D2 已形成独立运行事实；
- [x] M8 四态真实输入、矩阵局部滚动与失败反例已审计；
- [x] 所有者、单一变量、前端/生产/内置浏览器/清理门禁已预注册；
- [x] 用户审阅并确认本计划 0.1；
- [x] Batch 私有表现、局部自动化、生产 Chromium、优化模式、内置浏览器与清理门禁已完成；事实见
  [M12-D3 Batch 运行事实](42-m12-d3-batch-facts.md)。

D3 已闭环。M12 仍是 `IMPLEMENTING / NOT_FROZEN`；下一入口只能是独立计划后的 M12-E，不能借 D3 的通过
提前宣称 Browser Evidence 终稿、全局状态收束或 M12 冻结。

本文件是 D3 的设计与验收合同，不是实现或运行事实。
