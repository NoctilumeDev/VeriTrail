# Design QA — Rerun Comparison 数据页

## 对照依据

- 用户标注：中轴标签与勘合图案归入上半区正中央，四项判定数据留在下半区中轴。
- 实现实页：`?fixture=comparison&sample=drift`，1115 × 898 视口。
- 并排证据：`artifacts/design-audit/comparison-misalignment/07-vertical-center-comparison.png`
- 最终实页：`artifacts/design-audit/comparison-misalignment/06-centered-axis.png`

## 本轮核对

- [x] `CORE JUDGMENT · 中轴` 与勘合图案作为一个整体置于上半区正中央；水平偏差 0px，垂直偏差 0px。
- [x] 核心判定、适用性、差异统计、比较文件留在下半区中轴，轴线贯穿上下两区。
- [x] 基线／中轴／复跑与差异／判定／边界共用同一套三列网格。
- [x] 外层纹样框、内层细框与内容之间保留等量留白，四边没有重叠。
- [x] “类型／影响／路径／基线／重复”表头完整可见；类型与影响不换行。
- [x] 长路径只在单元格内省略，并保留 `title` 查看全值。
- [x] 桌面视口 `clientWidth` 与 `scrollWidth` 均为 1100px，无横向溢出。
- [x] 浏览器 console 无 error / warning。
- [x] `npm run build` 通过。
- [x] `npm test -- --run tests/comparison.test.ts tests/app.test.ts`：30 / 30 通过。

## 结论

中轴的图案、标签与数据已形成一根连续的视觉柱，左右两份 Run 信息保持镜像秩序；用户标注中的最后一处归位已完成。

final result: passed

---

# Design QA — Batch Analysis 数据页收尾

## 对照依据

- 用户标注：取消工作台黄色下划线与批次院落顶部青线；为 `Outcome N 项不符` 补充首次可见的展开提示。
- 实现实页：`?fixture=batch&sample=supported`。
- 顶部实页：`artifacts/design-audit/batch-final-polish/01-batch-court-top.png`
- 展开实页：`artifacts/design-audit/batch-final-polish/02-outcome-disclosure.png`

## 本轮核对

- [x] 工作台导航不再显示黄色下划线，计算样式 `border-bottom-width: 0px`。
- [x] 批次主院落顶部不再显示额外青色粗杠；顶边与底边使用相同的外框重量，且 `box-shadow: none`。
- [x] Outcome 使用原生 `details/summary` 披露控件，并显示随开合变化的三角标识。
- [x] 浏览器实测可展开、可再次收起，开合状态闭环。
- [x] `npm run build` 通过。
- [x] `tests/batch.test.ts` 与 `tests/app.test.ts`：34 / 34 通过。

## 结论

批次数据页最后三处视觉与发现性问题已经消除，没有引入额外脚本状态或伪造交互图标。

final result: passed
