# M12-D1 Comparison 运行事实

> 状态：`IMPLEMENTED_WITH_AUTOMATED_AND_IN_APP_BROWSER_EVIDENCE / M12_NOT_FROZEN`
> 日期：2026-08-14
> 前置计划：[M12-D 派生分析视图计划 0.1](34-m12-d-derived-analysis-plan.md)
> 前置事实：[M12-C 空间令牌与 Runs 主链运行事实](33-m12-c-run-mainline-facts.md)
> 影响事实：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
> 未进入：`L2_CONTRACT / L3_SYSTEM`

## 1. D1 已实现的表现事实

Comparison 现在以 `BASELINE -> REPEAT -> ComparisonStatus` 的 DOM 顺序组织来源与结论；桌面 CSS 将
两份来源置于共同中轴两侧，窄屏按该固定顺序纵向展开。`ComparisonStatus` 保持独立于来源 Run 的
execution status 和 Verdict：

- `MATCH` 使用结构玉色与 `comparison-mirror__verdict--match`，明确显示 `0 differences`；
- `DRIFT` 使用结构金色与 `comparison-mirror__verdict--drift`，把路径、BASELINE 值与 REPEAT 值留在
  前景；
- `INCONCLUSIVE` 使用黛色与 `comparison-mirror__verdict--inconclusive`，明确显示不可比较，不伪装成
  无差异。

这三种表现都没有复用来源 Run 的 `PASS/FAIL` token 或改写 Bundle、ComparisonStatus、来源 authority、
Loader、URL/import 语义。`Pairing` 与 `Batch` 继续使用原有共享 `.comparison-*` 基础规则；D1 只新增
Comparison 专属的 `.comparison-mirror*` 与 `.comparison-rerun-*` 私有规则，避免提前迁移 D2/D3。

## 2. 自动化与生产 Chromium 事实

所有命令在 Windows 11、16 GB 主机上严格串行执行；没有启动 Docker、中间件或第二个项目栈。

| 门禁 | 最终事实 |
| --- | --- |
| Comparison component | `5/5` tests passed，覆盖 MATCH、DRIFT、INCONCLUSIVE、固定来源 DOM 顺序与损坏拒绝 |
| Workbench full suite | `9` files、`64/64` tests passed |
| ESLint | `--max-warnings=0` 通过 |
| TypeScript | `vue-tsc` 与 Node `tsc` 通过 |
| Production build | `38` modules；CSS `51.00 kB` / gzip `9.05 kB`；JS `178.14 kB` / gzip `55.05 kB` |
| M11 Gate B Workbench 回归 | `11` checks，`113` Network requests，HTTP error、external origin、write request、Console/page error/request failure 均为 `0`；临时端口、服务线程与 SQLite sidecar 均释放 |
| D1 production acceptance | 常规与 `python -O` 均 `7` checks / `COMPLETED / PASS`；每轮 `12` requests，HTTP error、external origin、write request、Console/page error/request failure 均为 `0`，端口释放 |

新的 `scripts/m12_d1_comparison_acceptance.py` 以真实 M11 Gate B 恢复 Comparison 作为 MATCH 输入，以
已有脱敏 M6 Bundle 作为 DRIFT / INCONCLUSIVE 输入，并验证：

1. 十字从 Comparison 到 Runs 的 Back/Forward 保持 Comparison 入口；
2. 真实 M11 `MATCH / 0 differences` 仍显示两个正确来源；
3. DRIFT 的差异轴保留 BASELINE / REPEAT 与路径；
4. INCONCLUSIVE 保持不可比较；
5. 损坏 Manifest 输入不展示局部可信事实，随后在同一只读入口重新选择 MATCH 成功恢复；
6. 桌面、`390 x 844` 与 `360 x 800` 根级横向溢出均为 `0 px`。

自动化输出位于 Git 忽略目录：

- `artifacts/m12-d1-comparison-production-20260814-2123/acceptance.json`
- `artifacts/m12-d1-comparison-production-optimized-20260814-2123/acceptance.json`
- `artifacts/m12-d1-m11-gateb-regression-20260814-2123/acceptance.json`

旧 `m6_comparison_acceptance.py` 保持未修改。它在 M12-B 后直接从根页寻找旧的 Comparison 输入、并在
Comparison 损坏后假设存在全局“返回正向 Run”按钮，因此不再是当前公共入口的有效 D1 门禁；该脚本的
失败输出保留在 Git 忽略 artifacts 中。D1 使用新的、明确从 `?view=comparison` 进入并按当前“本地重选”
恢复合同工作的验收脚本，而没有篡改 M6 历史门禁或冻结事实。

## 3. Codex 内置浏览器补证

既有只读生产 Workbench `127.0.0.1:18778` 以当前 production build 接受真实本地文件导入。内置浏览器
完成的可见事实如下：

| 视口 | 输入与验证 | 结果 |
| --- | --- | --- |
| Desktop | 真实 M11 恢复 Comparison；两个来源、独立 MATCH、`0 differences`、边界文字 | PASS，根溢出 `0 px`，Console warning/error `0` |
| `390 x 844` | 真实 M11 MATCH；BASELINE 与 REPEAT 纵向进入、运行状态和 Verdict 不合并 | PASS，根溢出 `0 px`，Console warning/error `0` |
| `360 x 800` | 脱敏 DRIFT；多条路径、BASELINE / REPEAT 结构值和 `FAIL` 值仍可读 | PASS，根溢出 `0 px`，Console warning/error `0` |

内置浏览器的 viewport 覆写首次在新页加载前未生效。后续严格按“页面加载后设定视口，再 reload 并重选本地
Comparison”的实际操作取得 `390 x 844` 和 `360 x 800` 的 CSS 视口事实；没有把第一次的默认宽度截图记成
移动端验收。该控制接口未暴露 Network response 事件，因此本节不冒充 F12 Network 抓包；完整 response、
外部 origin 与写请求检查由第 2 节的生产 Chromium/CDP 验收承担。

## 4. 边界、清理与下一步

- 本切片未修改 `web/src/domain/`、Core、Schema、API、Catalog、Comparison Bundle、Analysis ID、裁决文本
  或安全边界；实际 diff 保持在 Comparison 组件、其私有表现样式、目标测试和 D1 浏览器验收脚本。
- 所有 D1 临时服务都绑定显式回环端口并已释放；没有持久化导入文件，也没有将 artifacts 提交到 Git。
- 本文不证明 Pairing、Batch、Browser Evidence、全局 loading/invalid 状态、200% zoom、forced-colors、色觉
  差异、M12-F 终验、M12 标签或 M12 冻结。

D1 已经形成代码、自动化、生产 Chromium 与内置浏览器事实。下一允许入口是 D2 `Pairing`；在 D2 的四角色
顺序、三态、四文件导入、移动端和边界事实独立闭环前，不得迁移 Batch。
