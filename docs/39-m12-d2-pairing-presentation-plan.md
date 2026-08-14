# M12-D2 Pairing 四角色有向序列表现计划 0.1

> 状态：`DESIGN_DRAFT / NOT_IMPLEMENTED`
> 日期：2026-08-14
> 前置事实：[M12-R2 Runs 主链表现运行事实](38-m12-r2-runs-presentation-facts.md)、[M12-D1 Comparison 运行事实](35-m12-d1-comparison-facts.md)
> 当前代码基线：`0a6f789`
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 问题、目标与单一变量

Pairing 当前复用了 `comparison-court`、`comparison-verdict` 与四等分小卡片的表现语言。功能正确，但这会把有
方向、有角色职责的四角色反事实链压成可互换的后台卡片：来源 Verdict、配对结论和 outcome 不符项容易在视觉上
混成一层。

本切片唯一主要变量是：

```text
paired_analysis_presentation = directed_four_role_court_m12
```

目标不是增加配对能力，也不是“给四个卡片换颜色”。它要让以下关系按阅读顺序可见：

```text
BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL
     source Run facts              paired AnalysisStatus              preregistered outcomes
```

Pairing 是一个有向的、预注册的四角色序列；`SUPPORTED / CONTRADICTED / INCONCLUSIVE` 是独立分析结论，
不能被来源 Run 的 `PASS / FAIL` 覆盖，也不能把来源 Verdict 改写成配对结果。

## 2. 控制内容与不变量

### 2.1 固定输入

本切片不伪造“已有 M11 Pairing”。M11 Gate B 的 Catalog 只提供当前生产 Workbench 的只读根环境；Pairing 内容
固定使用 M7 已生成、互不覆盖的三份四文件 PairedAnalysis：

| 状态 | 目录 | 必须保留的反例 |
| --- | --- | --- |
| `SUPPORTED` | `artifacts/m7-paired-supported-20260809` | TREATMENT 的来源 Verdict 为 `FAIL`，但四角色预注册 outcome 支持效果 |
| `CONTRADICTED` | `artifacts/m7-paired-contradicted-20260809` | TREATMENT 来源 Verdict 为 `PASS`，但其预期/实际不符，配对结论仍为 `CONTRADICTED` |
| `INCONCLUSIVE` | `artifacts/m7-paired-inconclusive-20260809` | NEGATIVE_CONTROL 出现效果且来源 Verdict 为 `FAIL`，`attributable=false` |

这三种内容压力证明分析结论和来源 Verdict 没有视觉吞并。目录是 Git 忽略的历史运行材料；计划只引用其已存在
事实，不复制、修改、提交或将其包装为新的 M11 运行。

### 2.2 保持不变

- `web/src/domain/pairing.ts`、`web/src/domain/types.ts`、PairingPlan seal、四文件集合、Manifest/SHA 校验、
  分析状态规则与本地临时导入生命周期；
- 角色常量和每个 `analysis.sequence` 的权威顺序：`BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL`；
- `App.vue` 的公共视图选择、URL/history、Loader、错误/重选、文件 input 的标签与可访问名称；
- 来源 Run 的 execution status、Verdict、Plan/Bundle SHA、outcome actual/matches、limits、`data-testid` 与所有
  对外可观察的文字语义；
- Comparison、Batch、Runs、Browser Evidence、全局 `StatusBadge.vue` 和所有 L2/L3 数据、安全、裁决边界。

### 2.3 允许所有者

| 文件/区域 | 允许工作 | 明确禁止 |
| --- | --- | --- |
| `web/src/components/PairedAnalysisView.vue` | 私有表现分组、私有 class/data 属性、标题层级内的结构组合 | 改写 loaded 数据、role 常量、状态词或输入流程 |
| `web/src/styles/components.css` 的 `.paired-*` | 新建 Pairing 私有 court、序列、来源账册、outcome 与响应式规则；删除不再使用的旧 `.paired-*` | 修改 `.comparison-*`、`.batch-*`、全局 `.status-badge` 或 token 语义 |
| `web/tests/pairing.test.ts` | 固定三态、四角色 DOM 顺序、来源状态与不符项的局部回归 | 修改 loader/domain 断言来适配表现 |
| `scripts/m12_d2_pairing_acceptance.py` | 新的生产 Chromium 事实、清理和 Network 门禁 | 修改产品运行逻辑或覆写历史 M7 脚本 |

`PairedAnalysisView.vue` 不再依附 `comparison-*` 容器类。D2 会为它建立只属于 Pairing 的私有外壳；D1 的
Comparison CSS 与事实不回改。若为方便布局而需要改 App、共享状态组件或 domain，立即停止，按 L2 重新审查。

## 3. 空间与状态合同

### 3.1 四角色廊道

桌面按权威顺序形成一条连续廊道，而不是四张等权卡。每个角色保留：序号、角色名、主变量值和明确的前后关系；
连接线、边界和空白只说明顺序，不能把线画成“因果已被证明”的装饰。`BASELINE` 与 `RESTORED_BASELINE` 可以
形成视觉呼应，但不得通过同色或镜像暗示它们的实际值、来源 Verdict 或 Bundle 一定相同。

移动端按相同顺序纵向展开，每一段仍显示序号和角色名；禁止重排为两列、手风琴或需横向滚动才能读完的四宫格。

### 3.2 三层事实不得合并

1. **AnalysisStatus 门**：`SUPPORTED`、`CONTRADICTED`、`INCONCLUSIVE` 只属于 PairedAnalysis。始终同时显示
   状态文字、是否可归因、理由和 outcome 数；`SUPPORTED` 不借用 PASS，`CONTRADICTED` 不借用 FAIL。
2. **来源账册**：四个角色按同一顺序显示其 Run ID、主变量、execution、Verdict、Plan 与 Bundle 摘要。原生
   `StatusBadge` 可以原样使用，但只由 `.paired-*` 父级界定其位置，不能改共享组件。
3. **预注册 outcome**：每项 outcome 仍按四角色顺序显示 Expected / Actual / 吻合或不符。`不符` 必须有文字和
   边界，不只换颜色；负对照的不符必须保持在 NEGATIVE_CONTROL 位置。

建议的语义色彩是：`SUPPORTED` 为分析专用玉色，`CONTRADICTED` 为分析专用金赭，`INCONCLUSIVE` 为独立黛青。
它们不等同于 Run 的绿色 PASS、警示朱 FAIL 或灰色 PENDING。色彩失效时，文字、图形、层级、边界和固定位置
仍能表达三层事实。

### 3.3 疏密与边界

- AnalysisStatus 是“正殿”，四角色廊道是方向骨架，来源账册为连续档案，outcome 为高密度应验册，limits 为
  后方边界；不让所有段落采用同一种卡片框。
- 只使用细线、局部台基、背景微差、间距和局部状态色；禁止完整粗框、阴影、圆形徽章、卡片套卡片、红金大面积
  铺陈和全局 `!important` 覆盖。
- 长 Run ID、SHA、主变量、Expected/Actual JSON 仅在具名局部自然换行或局部滚动；根页面任何视口不得横向溢出。
- 不增加“屋檐、四象、徽章”图案解释故宫；`四象殿` 仅为次级 kicker，功能名称与证据关系优先。

## 4. 精确 DOM 与交互退出条件

实现可以增加私有分组或 `data-pairing-role` 以便验收，但必须保持下列阅读和焦点关系：

1. `paired-sequence`、来源账册和每个 outcome 的角色子项都严格输出四角色权威顺序；桌面 CSS 可以排成四列，
   DOM 不得按视觉便利重排；
2. `Paired Analysis` 仍是公共视图 H2，只有应用名称是 H1；本地四文件导入继续是拥有明确可访问名称的原生
   label/input，不加入第二个上传控件；
3. 从十字西向进入时，焦点继续落到 `view-pairing-title`；刷新后必须要求重新选择本地文件，Back/Forward
   不得把临时文件持久化或把旧分析冒充仍可信；
4. 损坏 Manifest/PairingPlan/文件大小输入只显示拒绝状态，不展示局部可信 Pairing；显式重选后才能恢复；
5. `390 x 844`、`360 x 800`、`1440 x 960` 均无根横向溢出；移动端保留四角色方向、AnalysisStatus 与不符项；
6. `prefers-reduced-motion` 不制造必要动效；Console、page error、request failure 必须为零，Network 只允许同源
   `GET/HEAD` 成功响应。

## 5. 预注册实施与验收顺序

所有步骤严格串行，不启动 Docker、中间件或第二个项目栈。

1. **组件局部测试**：先建立三态下四角色 DOM 顺序、来源 Verdict 与 AnalysisStatus 独立、不符项位置和长内容
   换行的断言；再实施私有 DOM/CSS。不得先改视觉再放宽测试。
2. **静态门禁**：完整 `npm test`、lint 零 warning、type-check 与 production build。此时检查 diff 仅包含 2.3
   所列所有者；共享 `StatusBadge.vue`、App、domain、Comparison/Batch diff 直接失败。
3. **新的生产 Chromium 验收**：新增 `scripts/m12_d2_pairing_acceptance.py`，复用 M11 Gate B 的只读 Catalog 服务，
   从当前 Pairing 公共入口加载三份 M7 四文件分析。脚本必须使用自己的 `require()`，不得使用会被 `python -O`
   删除的内建 `assert`；输出拒绝覆盖，使用显式回环端口，常规和优化模式各独立运行一次。
4. **生产浏览器断言**：依次验证 `SUPPORTED`、`CONTRADICTED`、`INCONCLUSIVE` 的三层状态，四角色 DOM 顺序，
   `CONTRADICTED` 的 Treatment 不符，`INCONCLUSIVE` 的 Negative Control 不符，损坏拒绝/显式恢复，刷新重选、
   Back/Forward、桌面/390/360 根溢出、Console/Network、端口/线程/SQLite sidecar 清理。
5. **Codex 内置浏览器**：真实进入西向、使用本地四文件导入、检查角色方向和状态分离、刷新/返回与 Console；
   固定 390/360 的 Network 结论只由可重复 Chromium/CDP 记录，内置浏览器不冒充 F12 response 采集。
6. **事实归档**：全部通过后才写 D2 运行事实、更新 README/`milestones.md`/`AGENTS.md` 和 D 的状态；再决定是否
   进入 D3 Batch。任何失败先保留输出、定位当前单变量，再修复并重跑，不允许临时换一个更容易通过的分析包。

## 6. 完成边界与确认门禁

D2 不证明 Pairing 的科学效度、统计显著性、真实多次运行、M11 中存在真实四角色 Pairing、Batch、Browser Evidence
终稿、全局 loading/error/forced-colors/200% zoom，或 M12 冻结。它只证明现有可信 PairedAnalysis 的表现层能够
在真实内容和真实浏览器中保留其关系、边界和交互。

- [x] R1、R2 与 D1 已各自闭环，D2 是唯一下一入口；
- [x] 四角色常量、来源/状态三层、历史 M7 三态输入和现有消费者已审计；
- [x] 已明确 D2 不把历史 M7 材料表述成新的 M11 Pairing；
- [x] 已明确生产验收不能复用带优化模式缺口的旧 M7 脚本；
- [ ] 用户审阅并确认本计划 0.1；
- [ ] 未确认前不修改 Pairing 生产代码、不启动 D2 生产验收、不进入 D3。

本文件是 D2 的设计与验收合同，不是实现或运行事实。
