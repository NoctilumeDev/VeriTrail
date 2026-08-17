# M12-D2 Pairing 运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
>
> 前置合同：[M12-D2 Pairing 四角色有向序列表现计划 0.1](39-m12-d2-pairing-presentation-plan.md)
>
> 前置事实：[M12-D1 Comparison 运行事实](35-m12-d1-comparison-facts.md)、[M12-R2 Runs 主链表现运行事实](38-m12-r2-runs-presentation-facts.md)
>
> 影响：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`；未触及 `L2_CONTRACT / L3_SYSTEM`

## 1. 已实现的表现关系

`PairedAnalysisView.vue` 已从 `comparison-*` 视觉容器中分离，使用仅属 Pairing 的 `.paired-*` court、状态门、
四角色廊道、连续来源账册、outcome 应验册与后方边界。它没有改写 Loader、Plan seal、四文件集合、roles 常量、
AnalysisStatus、来源 Run Verdict、URL/history、文件 input 或共享 `StatusBadge.vue`。

三层事实保持分离：

1. `SUPPORTED / CONTRADICTED / INCONCLUSIVE` 由独立 AnalysisStatus 门表达；
2. 四个来源 Run 固定按 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL` 输出；
3. 每个预注册 outcome 在同一顺序下显示 Expected、Actual 与明确的“吻合/不符”。

桌面以连续四列和细线表达顺序，`920px` 以下转两列，`720px` 以下转单列；来源账册、AnalysisStatus、边界和
outcome 同步收束。长 Run ID、SHA 和 JSON 只在具名局部换行，根页面不横向溢出。

## 2. 固定输入与反例

生产验收只读取现有、Git 忽略的 M7 历史材料，不复制或包装为 M11 新运行：

| AnalysisStatus | 输入目录 | 必须保持的反例 |
| --- | --- | --- |
| `SUPPORTED` | `m7-paired-supported-20260809` | `TREATMENT` 来源 Verdict 为 `FAIL`，而 AnalysisStatus 为 `SUPPORTED` |
| `CONTRADICTED` | `m7-paired-contradicted-20260809` | `TREATMENT` 来源 Verdict 为 `PASS`，但每个对应 outcome 都明确为“不符” |
| `INCONCLUSIVE` | `m7-paired-inconclusive-20260809` | `NEGATIVE_CONTROL` 来源 Verdict 为 `FAIL` 且每个对应 outcome 都明确为“不符” |

这三种输入证明分析结论没有吞并来源 Verdict，也没有把负对照从其固定位置移走。

## 3. 自动化与生产 Chromium

| 门禁 | 结果 | 事实 |
| --- | --- | --- |
| Pairing 局部回归 | `6/6 PASS` | 三态、顺序、来源 Verdict、负对照不符、长 Run ID 与损坏拒绝 |
| Workbench 回归 | `66/66 PASS` | 全量组件/Loader/App 回归 |
| lint / type-check / production build | `PASS` | 零 warning；生产 CSS/JS 构建成功 |
| `m12_d2_pairing_acceptance.py` | `8/8 PASS` | 桌面、390、360px；三态、历史、损坏拒绝、显式恢复、刷新重选、溢出、Console/Network 与清理 |
| 同一脚本 `python -O` | `8/8 PASS` | 所有硬门禁使用显式 `require()`，不依赖优化模式会移除的内建 `assert` |

生产脚本复用 M11 Gate B 的只读 Catalog 服务，在独立回环端口运行。常规与优化模式各记录 `16` 个请求，
全部是同源 `GET` 成功响应：外部请求、写请求、HTTP error、Console warning/error、page error 与 request failure 都为 `0`。
两轮结束后端口释放、服务线程停止，Catalog 无 SQLite `-wal/-shm` sidecar。

首两次脚本运行分别把多个 outcome 误视作一条角色序列、把同一角色的多个 outcome 节点当作单节点；均在未出现
浏览器/网络异常时被脚本自身拦下。失败输出保留在 Git 忽略的本地 artifacts 中；脚本随后改为逐个 outcome 验证完整
四角色顺序，并验证对应角色在每个 outcome 中都有“不符”文字和 `is-mismatch` 边界后通过。它们是验收脚本粒度缺陷，
不是产品状态或布局失败。

## 4. Codex 内置浏览器

用户在运行中的 `http://127.0.0.1:18778/?fixture=pairing` 页面真实选择了 `SUPPORTED` 的四个本地文件。页面实际显示：

- `AnalysisStatus = SUPPORTED`，并明确写有“独立于 Run Verdict”；
- `TREATMENT` 来源仍为 `COMPLETED / FAIL`；
- 两个 outcome 都按 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL` 输出；
- 当前桌面根横向溢出为 `0px`，文件 input 保有原生可访问名称。

内置浏览器只作为真实可见导入和内容关系证据；Console/response Network 结论只来自可重复的生产 Chromium/CDP 运行，
没有把内置浏览器冒充为 F12 抓包。

## 5. 范围与下一入口

本切片不证明科学效度、统计显著性、真实多次 Pairing、M11 中存在四角色 Pairing、Batch、Browser Evidence 终稿、
全局 loading/error、forced-colors、200% zoom、色觉差异矩阵或 M12 冻结。没有修改 Core、Schema、Catalog/API、
Comparison、Batch、状态机、裁决或安全边界。

D2 已关闭。M12 仍是 `IMPLEMENTING / NOT_FROZEN`，唯一下一实现入口是 D3 Batch；只有 D3 自身完成计划、实现和
独立运行事实后，才可进入 M12-E，不能借 D2 的通过提前开始 Browser Evidence 终稿或 M12 冻结。
