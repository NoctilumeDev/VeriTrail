# M11 Gate B 真实项目验证

> 状态：`GATE_B_VALIDATED / M11_FROZEN`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`
> Gate B harness：`da6390eeccb806cd8975103220d625488b293673`
> 目标：`InkNarratives @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`
> 最终自动轮：`tmp/m11-gateb-contract04-20260814-161647`

## 1. 结论

Contract 0.4 / Plan v2 的 Gate B 严格串行矩阵已经按预注册顺序真实完成：正向为
`COMPLETED / PASS`，Browser 负向为 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`，端口竞争为
`ABORTED / PENDING`，外部 owner 结束后的恢复正向再次为 `COMPLETED / PASS`。两次正向 Comparison
为 `MATCH` 且差异数为 0；Catalog 接纳四个有效 Run，并把一个故意损坏副本隔离为
`COMPLETED_WITH_ISSUES`。

这证明 M11 的单 application 真实项目链路在当前 Windows 11 / C1 process-cold / 16 GB 边界内成立。
生产 Workbench、双 Python 全量回归、M0-M11 系统审查与代码质量审查随后也已独立完成；最终前端、
依赖、安全、残留和远端标签门禁也已关闭。冻结来自完整运行事实，不来自计划文字或局部通过。

## 2. 冻结 authority 与串行结果

| Authority / Run | SHA-256 或结果 |
| --- | --- |
| Profile | `a9385a78a282e485d0cd7aa6f2970d51cf240ea3bc41324276ab5d59960fd7f4` |
| Positive Plan v2 | `8300700074b8d8f520ccf21fd2369b5607881eb96b7a1e62c7a18d91ba200841` |
| Browser-negative Plan v2 | `47bb71543916929652139e20b85ee2587c3a7847e7b92659822aeaa3c662eddb` |
| `m11-gateb-v2-ink-positive-01` | `NONE / COMPLETED / PASS` |
| `m11-gateb-v2-ink-browser-negative-01` | `BROWSER_HARD_FAILURE / COMPLETED / FAIL` |
| `m11-gateb-v2-ink-port-conflict-01` | preflight-only / `ABORTED / PENDING` |
| `m11-gateb-v2-ink-recovery-positive-02` | `NONE / COMPLETED / PASS` |
| 正向恢复 Comparison | `MATCH`，`0` differences |
| Catalog | `4` Runs，损坏副本已隔离，`COMPLETED_WITH_ISSUES` |

端口竞争 Run 保留外部 owner，独立恢复后才启动第四个 Run。四个 Bundle 均绑定固定 ref，Subject 前后
工作区干净、无 `.env`，没有把失败结果改写成通过，也没有把不同轮次拼接成一轮。

## 3. 自动 Browser 与资源事实

- positive 与 recovery-positive 均完成五页、桌面 `1440x960` 和移动 `390x844` 的固定步骤；
- 页面文档、同源资源与固定交互均由自动 Browser Evidence 封存，目标请求为 HTTP 200；
- Browser-negative 使用预注册不存在 selector，按合同形成真实 `COMPLETED / FAIL`；
- readiness 响应为 31,741 字节；三条 application Run 峰值约 30.875-30.918 MiB；
- Browser 进程树峰值约 534.977-1,192.090 MiB，Core 峰值约 46.125-52.527 MiB；
- 最低宿主机可用内存约 5,389.930 MiB，未触及资源停止线；
- 51 个持久化文本文件敏感扫描 0 命中；
- 自动轮结束后 18775、owned staging、run-work、application 与 Browser owned 进程均归零。

Pairing、Batch、数据库、中间件、业务写入、多角色、多实例和最终一致性在本目标均为
`NOT_APPLICABLE`，不得从单节点静态项目外推这些能力。

## 4. 内置浏览器独立补验

自动 Run teardown 后，另以 Python 3.10.6、InkNarratives 原始目录和专用回环端口 18776 启动独立
owned `http.server`。该补验没有修改或倒填任一 Gate B Bundle。

已完成的用户可见事实：

- 五个 HTML 页面在内置浏览器中完成桌面浏览与代表性交互；
- 完成刷新、后退与前进；
- 长卷页初始 `Tab` 聚焦“空山之后”，`Enter` 打开阅读层，`Esc` 可以关闭；关闭后再次按
  `Tab` 到达下一册“江流有声”，证明焦点先归还“空山之后”触发按钮，再按原生顺序前进；
- 用户以物理键盘实际完成 `Tab -> Enter -> Esc -> Tab`，并当场确认上述焦点顺序和视觉反馈无异常；
- 工具在用户切回对话后只读观察到阅读层 `aria-hidden=true`、`display=none`，页面横向溢出为 0，
  开发者日志 warning/error 为 0；此时页面焦点已回落到 `BODY`，因此事后工具读回只承担关闭状态、
  溢出和日志事实，焦点归还结论由用户当场的物理键盘顺序承担；
- 自动 Bundle 已独立承担固定 `1440x960`、`390x844` 的完整步骤、Network 200 和截图事实。

补验结束前再次核对 PID、Python 路径和命令行，只停止本轮 owned PID `32864`。停止后 PID 不存在，
18776 已释放；没有使用进程名匹配、全局 `taskkill` 或关闭无关 listener。

## 5. 生产 Workbench 独立读回

当前源代码先用 Node 24.14.0 重新执行 type-check 与 production build，构建通过。随后新增的
`scripts/m11_gateb_workbench_acceptance.py` 只读消费最终 Gate B 目录，不重新裁决、不修改 Catalog、
Bundle 或 Comparison。独立自动 Chromium 结果保存在
`tmp/m11-gateb-workbench-contract04-20260814-physical01`：

- 桌面 `1440x960` 逐个读回四个 Run，状态与最终 acceptance 完全一致；
- Catalog 显示 4 Runs、1 个隔离问题，损坏副本没有进入有效 Run 集合；
- 正向与恢复正向均显示 `Core 裁决 / 已核验`，端口竞争明确只含 preflight、Browser 不适用；
- 真实 Comparison 为 `MATCH`、0 differences，并显示两个不同 Run 与相同 positive Plan SHA-256；
- 移动 `390x844` 读回真实负向与 Comparison，两个状态均无横向溢出；
- 共完成 9 项浏览器检查、113 个页面请求；Console warning/error、page error、request failure、
  HTTP 4xx/5xx、外部 origin 和写请求均为 0；
- 自动验收结束后 18778 释放，Catalog SQLite sidecar 为 0。

同一 production build 随后由 Codex 内置浏览器独立打开。内置浏览器在实际 `692x898` 页面中读回
4 Runs、1 个 `BUNDLE_SIZE_MISMATCH` 隔离问题、正向 `COMPLETED/PASS`、预注册 Browser 负向
`COMPLETED/FAIL`、端口竞争 `ABORTED/PENDING` 及真实 Comparison `MATCH`、0 differences；根级横向
溢出为 0，开发者日志为空。页面资源账册共观察到 40 项，均来自 `127.0.0.1:18778`，包含生产
JS/CSS、Catalog API、三类已打开 Bundle 的 Manifest/Report/Plan/Profile/Evidence/附件与截图；
Comparison 由本地目录只读导入，不产生上传或写请求。

验收后按启动时记录的三层 owned 进程链逐个核对身份并从叶到根停止；最终 owned 进程、18778 和
SQLite sidecar 均为 0。自动固定移动视口与内置浏览器实际窗口是两项独立事实，不能把 692px 窗口
伪写为 390px。

## 6. 必须保留的不利事实

以下事实不得被最终成功轮覆盖：

1. `tmp/m11-gateb-contract03-20260814-160143`：Plan v1 在移动长卷页引用隐藏导航，正向真实 FAIL；
2. `tmp/m11-gateb-contract04-20260814-161147`：验收器曾错误要求 Catalog 为纯 `COMPLETED`，没有接受
   隔离损坏副本后的 `COMPLETED_WITH_ISSUES`；
3. `tmp/m11-gateb-contract04-20260814-161439`：acceptance metadata 曾仍写 Contract 0.3；
4. 内置浏览器约 1280px 宽时，长卷页出现约 13px 根级测量溢出；固定 1440 和 390 视口均为 0。
   独立复测证明阅读层打开前、打开后和关闭后均为 13px，来源是目标页多个超宽装饰层；
   `body overflow-x:hidden` 隐藏滚动条但没有消除 `scrollWidth`。它归为 InkNarratives 的
   `DEFERRED_TARGET_L0`，不修改 M11 固定 ref，也不倒填为预注册视口失败。

前三个失败候选均保留在独立目录中，不删除、不覆盖，也不抽取其中局部通过项拼接最终轮。

## 7. M0-M11 系统与代码质量审查

审查按 Profile/Plan/Preview -> lifecycle -> staging/Evidence -> Bundle/Verdict -> Catalog/Comparison ->
Pairing/Batch -> CLI -> Workbench -> Gate A/B harness 顺序完成。Profile 0.1/0.2、Plan 0.6/0.7、Preview
0.1/0.2 与 collector 0.1/0.2/0.3 均使用显式版本分派；Plan 0.7 只能绑定 Profile 0.2，单节点只生成
两个 application 流附件，Catalog 从 sealed authority 和 Evidence 重推导，Comparison 只接受同 Plan/
Profile，Pairing/Batch 明确拒绝 0.7。没有发现 Core、Schema、状态归因、所有权或旧版本兼容阻断项。

审查分类如下：

| Class | Fact | Decision |
| --- | --- | --- |
| `MUST_FIX` | Workbench 验收脚本用 Python `assert` 承担关键门禁，`python -O` 可将其移除 | 改为始终执行的 `require`，补齐服务线程退出门禁，并在 `PYTHONOPTIMIZE=1` 下完整复跑通过 |
| `DEFERRED_RUNTIME` | Python 3.13 首次全仓出现一次 Playwright 1.62 关闭阶段 `TargetClosedError` warning | 单例 5/5、相关类 4/4 与后续完整 277/277 均未复现；保留首次失败，不加 sleep、不放宽 stderr |
| `DEFERRED_TARGET_L0` | 长卷页约 1280px 的 13px 根级测量溢出 | 归属固定 Subject 的装饰层；预注册 1440/390 与用户实际 692px 均为 0，留给 InkNarratives 独立版本处理 |
| `STRUCTURAL_DEBT` | `bootstrap_evidence.py`、`bootstrap_run.py` 与两个 M11 harness 体量较大 | M13 再按所有权拆分评估；M11 合同稳定期不做无证据重构 |

## 8. 冻结回归与发布门禁

- Python 3.10.6：`277/277 PASS`，128.667 s；
- Python 3.13.13：`277/277 PASS`，127.660 s；
- Python 3.13 高风险单例额外连续 `5/5 PASS`；
- Workbench 优化模式生产验收：9 项、113 个同源只读请求，Console/Network/HTTP/写请求异常均为 0，
  server thread、18778 与 SQLite sidecar 均归零。

- [x] Gate B v2 四 Run 严格串行矩阵与真实裁决；
- [x] 正向恢复 Comparison 与 Catalog 独立验真；
- [x] 内置浏览器目标项目补验、物理键盘、日志和 owned 清理；
- [x] 生产 Workbench 读取最终 Catalog、四个 Bundle 与 Comparison；
- [x] Workbench 桌面/移动完整链路与 Console/Network；
- [x] Python 3.10.6 与当前 Python 双运行时全量回归；
- [x] Workbench 60/60、lint、type-check、production build 与两类 npm audit；
- [x] M0-M11 系统思维审查与代码质量审查；
- [x] 资源、敏感扫描、端口、owned 进程、staging/run-work、SQLite sidecar 与目标状态最终读回；
- [x] 候选提交前 VeriTrail 远端基线无漂移；固定 Subject 的本地 HEAD 与远端 `main` 精确一致；
- [x] Python/Workbench 版本更新为 `0.12.0.dev1` / `0.12.0-dev.1`；
- [x] 候选提交 `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40` 已推送；注释标签
  `m11-v0.12.0` 已创建；冻结读回时远端 `main` 与 `m11-v0.12.0^{}` 均精确指向该提交。

因此 M11 已在 Contract 0.4 声明的 Windows 11 / C1 / 16 GB / 固定 InkNarratives ref 边界内标记
`FROZEN`。M12–M14 继续保持 `PLANNED`，本次冻结不外推未证明能力。
