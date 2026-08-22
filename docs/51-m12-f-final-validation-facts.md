# M12-F 总体验收与冻结候选运行事实 0.1

> 状态：`VALIDATED_FREEZE_CANDIDATE / NOT_FROZEN`
>
> 日期：2026-08-22
>
> 影响层级：`L0_PRESENTATION + BOUNDED_L1_COMPONENT`
>
> 候选基线：`HEAD ecc2d09` 加本文件记录的 M12 工作树；提交后必须重新记录候选 SHA

## 1. 结论

M12 宫阙验迹表现候选已通过静态、双 Python、三个派生页独立生产验收、M12-F 常规/优化生产验收、
Codex 内置浏览器与用户逐页审美确认。没有发现 L2/L3 合同、裁决、Catalog/API 或安全边界漂移。

本结论只形成“可提交的冻结候选”，不等于 M12 已冻结。候选提交、`m12-v0.13.0`、远端 `main` 与 tag
精确读回尚未执行；因此没有 GitHub Release，也没有提前进入 M13。

## 2. 输入与环境

- Windows 11 单机，16 GB 内存；重任务严格串行，Chromium 启动前可用内存均高于 7.8 GiB。
- 生产 Workbench：`web/dist`，Vite 生产构建。
- M11 Gate-B 控制事实：`artifacts/m12-f-relocated-gateb-input-20260822`。
- Comparison：M11 `MATCH` 与既有 `DRIFT / INCONCLUSIVE`；Pairing：M7 三态；Batch：M8 四态。
- 只允许同源 `GET/HEAD` 与本地文件/blob；不启动 Docker、中间件或第二个并行浏览器任务。

旧 `tmp/m11-gateb-contract04-20260814-161647` 的 Catalog 绑定原绝对证据根目录。仓库迁移后，首次 M12-F
运行以 `ARTIFACT_ROOT_MISMATCH` 正确拒绝，输出保留在 `artifacts/m12-f-final-acceptance`。没有改写旧快照；
后续使用重新生成根绑定、内容集合不变的脱敏重定位输入完成验收。

## 3. 静态与全量回归

| 门禁 | 结果 |
| --- | --- |
| Workbench `npm test` | `156 / 156` 通过 |
| Workbench lint | 通过，0 warning |
| TypeScript + Vite production build | 通过 |
| Python 3.10 | `278 / 278` 通过 |
| Python 3.13 | `278 / 278` 通过 |
| `git diff --check` | 通过；仅有 Git 的 CRLF/LF 提示，无空白错误 |

Python 3.13 回归曾打印 Playwright 关闭阶段的异步清理提示，但最终退出码为 0；随后各独立/集成验收均确认
浏览器关闭、服务线程停止、端口释放且无 SQLite sidecar，因此未发现持续资源泄漏。

## 4. 独立派生页验收

| 页面 | 输出 | 结果 |
| --- | --- | --- |
| D1 Rerun Comparison | `artifacts/m12-d1-comparison-acceptance-closeout-fixed` | 7 组检查，`PASS` |
| D2 Paired Analysis | `artifacts/m12-d2-pairing-acceptance-closeout-fixed2` | 8 组检查，`PASS` |
| D3 Batch Analysis | `artifacts/m12-d3-batch-acceptance-closeout-fixed` | 9 组检查，`PASS` |

独立验收首先暴露了验收器自身仍等待旧折叠菜单、数据态仍寻找旧入口及移动批次连续换样例的问题。失败输出
没有覆盖；D1/D2/D3 当前验收器已统一到固定四轴导航和“回入口再选择”的现行交互闭环。M11 与 R1 的历史
里程碑脚本保持原样，避免用新 UI 篡改历史验收定义。

## 5. M12-F 生产总验收

最终候选输出：

- 常规：`artifacts/m12-f-final-acceptance-closeout-final`
- 优化：`artifacts/m12-f-final-acceptance-closeout-final-optimized`

两轮均为：

- `execution_status = COMPLETED`，`verdict = PASS`；
- 13 组集成检查；
- 636 个网络请求；外部 origin 0、写请求 0、HTTP 错误 0；
- Console warning/error 0、page error 0、request failure 0；
- 根页面横向溢出 0；只在具名局部矩阵保留可聚焦滚动；
- 端口释放、服务线程停止、SQLite sidecar 不存在。

## 6. 真实浏览器与用户确认

Codex 内置浏览器逐一复核 16 个主路由、数据态与二级页；桌面、390 px、360 px 代表链路根溢出均为 0。
损坏包提示和 Batch Outcome 均可展开、再次收回；返回目录、历史、标题焦点与数据重选闭环成立。浏览器 Console
未出现 warning/error。Comparison 与 Batch 最终页面已按用户标注完成逐项收口；用户于本轮明确确认“没有问题，
可以收尾”。

## 7. 边界与下一门禁

- 没有修改 Python Core、Schema、Verdict、Catalog/API、Bundle 或确定性裁决。
- bounded L1 只增加同源脱敏 Batch 审阅夹具读取和 `sample=supported` 路由；数据仍经既有 manifest/size/SHA
  校验器读取，不以组件内对象伪造事实。
- `Blocker = 0`，`Must Fix = 0`；M13 建议不混入本候选。
- 下一步只允许：复核最终 diff，形成单一 M12 候选提交，推送并读回，再创建并读回 `m12-v0.13.0`。
