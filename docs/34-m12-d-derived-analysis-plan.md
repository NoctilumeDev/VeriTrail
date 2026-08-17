# M12-D 派生分析视图计划 0.1

> 状态：`IMPLEMENTING / D1_COMPLETE / D2_COMPLETE / D3_COMPLETE / M12_NOT_FROZEN`
> 日期：2026-08-14
> 前置事实：[M12-C 空间令牌与 Runs 主链运行事实](33-m12-c-run-mainline-facts.md)
> 当前提交基线：`0a6f789`（R2 Runs 主链事实已闭环）
> 影响声明：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 禁止越界：`L2_CONTRACT / L3_SYSTEM`

## 1. 目的和单一变量

M12-D 只迁移三类已经存在、由 Core 确定性生成的派生分析视图：Comparison、PairedAnalysis 与
BatchAnalysis。唯一主要变量是：

```text
derived_analysis_presentation = palace_evidence_m12
```

它不增加分析能力，不改变分析结论，也不把来源 Run 的 execution status、Verdict、Bundle hash 或
Plan authority 改写为新的前端事实。目标是让不同证据关系本身决定空间，而不是把 Runs 的详情模板
复制三遍。

M12-D 的固定顺序是：`Comparison -> Pairing -> Batch`。每一类完成其正常、负向或不完整状态与移动
端事实后，才允许迁移下一类；不得把三类 CSS、DOM、状态文案和响应式规则混为一次不可归因的大改。

## 2. 所有权和不变量

| 范围 | 允许的表现所有者 | 禁止触及的事实所有者 |
| --- | --- | --- |
| Comparison | `ComparisonView.vue`、其 `.comparison-*` 样式与目标测试 | `web/src/domain/comparison.ts`、Comparison Bundle、来源 Run、ComparisonStatus 规则 |
| Pairing | `PairedAnalysisView.vue`、其 `.paired-*` 样式与目标测试 | `web/src/domain/pairing.ts`、PairingPlan、四角色顺序、AnalysisStatus 规则 |
| Batch | `BatchAnalysisView.vue`、其 `.batch-*` 样式与目标测试 | `web/src/domain/batch.ts`、BatchPlan、slot/wave、coverage/hypothesis 规则 |
| 公共外壳 | `components.css` 中有明确所有者的局部规则；必要时只增加私有 DOM 分组 | `App.vue` Loader 流程、URL/import 语义、`web/src/domain/` 公共类型、Core/API/Schema |

以下不变量在每一小节和最终回归中必须保持：

- Comparison 的 `MATCH / DRIFT / INCONCLUSIVE` 始终独立于来源 Run Verdict；
- Pairing 的 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL` 顺序不可被视觉重排；
- Batch 的 coverage、hypothesis 与来源 Run status 三层不互相覆盖，wave 也不被误写成真实并行；
- 既有 `data-testid`、可访问名称、本地文件导入、损坏隔离、对象 URL 回收、URL/history 与焦点合同不变；
- 不增加图片、纹理、远程字体、CDN、图标库、遥测、路由库、状态库或主题切换器；
- 不用红金装饰掩盖警示，分析状态必须同时由文字、位置、边界或形状表达。

实际 diff 若触及任一 Loader、domain 类型、裁决文本、API 或 Core，立即停止并按 L2/L3 重新审查；本计划
不能为这类变化背书。

## 3. 三段空间章法

### 3.1 Comparison: 南轴的镜像对照

- 共同的 ComparisonStatus 位于两份来源之间的中轴，不复用 PASS/FAIL 的组件或色彩语义；
- `BASELINE` 与 `REPEAT` 在桌面保持可比较的左右镜像，来源 Run 的 execution 与 Verdict 仍在各自侧边；
- `MATCH / 0 differences` 要安静但不是空白，`DRIFT` 必须把差异路径、baseline/repeat 的值和不相同的原因
  带到前景，`INCONCLUSIVE` 必须明确不可比较而不伪装成无差异；
- 窄屏按 `BASELINE -> REPEAT -> ComparisonStatus -> differences` 的明确阅读顺序纵向展开，避免靠左右滚动
  才能理解对照；长 SHA、Run ID 与 JSON 值只在具名的局部区域换行或滚动，根页面不溢出。

### 3.2 Pairing: 四角色的有向序列

- 顶部四角色顺序是证据关系，不是四张可随意调换的装饰卡；用 CSS 轴线、序号和角色文字保持方向；
- `BASELINE` 与 `RESTORED_BASELINE` 可以形成视觉呼应，但不得暗示它们在实际值或 Verdict 上必然相同；
- `TREATMENT` 与 `NEGATIVE_CONTROL` 必须保留其不同职责，`SUPPORTED / CONTRADICTED / INCONCLUSIVE` 独立于
  来源 Run Verdict；
- outcome 区在桌面显示相同的角色列序，在移动按该顺序分段；不符项必须有文字和边界，不能只换色。

### 3.3 Batch: 格局、波次和三层状态

- 先呈现 coverage 与 hypothesis 的双状态门，再呈现封存 policy、Profile 矩阵、wave ledger、原因和边界；
- Profile 矩阵是主体。小视口保留现有具名 `role=region` 与键盘焦点的局部横向滚动，禁止让根页面横向滚动；
- `INCOMPLETE` 缺格、`INCONCLUSIVE` 污染、`CONTRADICTED` 与来源 `FAIL` 都必须同时可见且不发生语义吞并；
- wave 只表示封存资源预算与次序。页面必须继续可见“不证明真实并行”的边界，不能用宫阙层级制造
  性能或因果的夸大暗示。

## 4. 实施切片与退出条件

### D1: Comparison

1. 仅重组/替换 `ComparisonView.vue` 的私有 DOM 分组和 `.comparison-*` 样式，移除已迁移范围的旧规则；
2. 测试 `MATCH`、`DRIFT`、`INCONCLUSIVE`、长哈希和差异 JSON；
3. 用真实 M11 正向恢复 Comparison 验证 `MATCH / 0 differences`，再用既有脱敏夹具验证 DRIFT/不可比较；
4. 完成桌面、390、360 px、返回/前进、根溢出、Console 和同源只读 Network 回归后，才进入 D2。

### D2: Pairing

1. 只迁移 `PairedAnalysisView.vue` 和 `.paired-*` 规则，保留 roles 常量及其给定顺序；
2. 测试 `SUPPORTED`、`CONTRADICTED`、`INCONCLUSIVE`，包括负对照不符、长 primary variable 和 outcome；
3. 用四文件本地导入证明来源权威、刷新重选和损坏拒绝未漂移；
4. 完成桌面、390、360 px、顺序、无溢出、Console 和同源只读 Network 回归后，才进入 D3。

### D3: Batch

1. 只迁移 `BatchAnalysisView.vue` 和 `.batch-*` 规则，保留 matrix region、表格语义、details 和 wave/slot 顺序；
2. 测试 `COMPLETE + SUPPORTED`、`COMPLETE + CONTRADICTED`、`INCOMPLETE`、`INCONCLUSIVE`、缺格和 4--16 格
   矩阵；
3. 验证局部矩阵滚动可用、Tab 可进入/离开、根页面无溢出，长 slot ID/Run ID/SHA 不撑破内容；
4. 完成桌面、390、360 px、Console、同源只读 Network 与导入负向后，M12-D 才能形成运行事实。

## 5. 预注册验收矩阵

所有门禁严格串行，不启动 Docker、中间件或第二个项目栈。实现每个子切片后先运行其局部测试，再运行
以下回归；不能把一次全量绿色代替中间切片事实。

| 层级 | 共同门禁 | 每类额外门禁 |
| --- | --- | --- |
| 代码/静态 | `npm test`、lint `--max-warnings=0`、`vue-tsc`、Node `tsc`、production build | 目标组件的三态/负态、稳定来源顺序与局部滚动断言 |
| Chromium | 同一 M11 Gate B Catalog、正向恢复 Comparison、Console/Network、只读 HTTP 负向合同 | Comparison 的 MATCH/DRIFT/INCONCLUSIVE；Pairing 的三态和四文件导入；Batch 的四态、矩阵和 wave |
| 内置浏览器 | 十字进入视图、真实本地导入、焦点、刷新/返回、桌面与 390/360 px、Console | Comparison 镜像/差异；Pairing 角色方向；Batch region 滚动、details、缺格 |
| 边界 | 根溢出为 `0 px`、长内容、文字/形状/位置不只依赖颜色 | 状态词、source authority、边界文字均仍可见 |
| 清理 | 测试服务、端口、SQLite sidecar、对象 URL 与临时输出按本切片复核 | 本地文件导入不持久化、损坏候选不污染有效分析 |

M12-D 的运行事实必须明确区分自动化、真实 Chromium 与内置浏览器。生产 Chromium 的 response 观察是
Network/CDP 事实；内置浏览器负责真实可见操作、焦点、历史与响应式，若其控制接口不能提供 response
事件，不得伪称其为 F12 Network 抓包。

D1 的已取得事实见 [M12-D1 Comparison 运行事实](35-m12-d1-comparison-facts.md)。D2 的独立计划与运行事实见
[M12-D2 Pairing 四角色有向序列表现计划 0.1](39-m12-d2-pairing-presentation-plan.md) 与
[M12-D2 Pairing 运行事实](40-m12-d2-pairing-facts.md)。D3 已按其独立计划
[M12-D3 Batch 双状态矩阵与 Wave 账册表现计划 0.1](41-m12-d3-batch-presentation-plan.md) 完成，事实见
[M12-D3 Batch 运行事实](42-m12-d3-batch-facts.md)。这些事实只关闭 M12-D；不为后续 M12-E 预先提供完成结论。

## 6. 非目标与交接

- Browser Evidence、loading/empty/error/invalid 全局收束、200% zoom、完整 forced-colors 与色觉差异矩阵
  属于 M12-E/F；D 中发现其阻断性缺陷只能记录和停止，不能偷偷实施 E；
- 本文不是 M12-D 的运行事实，不提高版本，不创建 M12 标签，也不允许把 M12 标成 `FROZEN`；
- D3 已形成独立事实文档、更新阶段记录并复核 diff/资源边界；下一入口才是单独计划的 M12-E。
