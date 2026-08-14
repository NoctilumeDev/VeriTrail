# M11 Gate A 单应用能力验证

> 状态：`GATE_A_VALIDATED / M11_PLANNED / GATE_B_NOT_STARTED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`
> 合同：`docs/23-m11-single-node-real-project-contract.md` Contract 0.3
> 运行环境：Windows 11 / Python 3.10.6 / C1 process-cold / 16 GB host

## 1. 结论

Gate A 已以目标无关 helper 完成代码、自动化、真实 Chromium、13 个预注册公共出口、Catalog、
Comparison、失败恢复、资源、安全、清理和 Workbench 单节点消费验证。它证明 VeriTrail 能在现有
Windows/C1 边界内管理一个 owned `APPLICATION`，且不会伪造 dependency 节点或附件。

这不是 M11 冻结事实。InkNarratives Gate B 尚未开始，README 中 M11 继续为 `PLANNED`；M12 也不得
提前实施。Gate B 开始前还必须把本轮固定实现提交推送到 GitHub，并从公开远端精确读回该提交。

## 2. 实现与兼容边界

- 新增 ProjectProfile 0.2、ExperimentPlan 0.7、BootstrapPreview 0.2；
- Profile 0.2 固定 `SINGLE_APPLICATION`，只有一个 `APPLICATION`，启动和清理顺序均只有该节点；
- Plan 0.7 只绑定 Profile 0.2，唯一 PRIMARY 为 `project_bootstrap_topology`；
- `runtime.bootstrap` 使用 `VeriTrail bootstrap-lifecycle/0.3`，恰好两个 application 文本附件，
  `dependency_peak_rss_mb` 固定为 `null`；
- Profile 0.1、Plan 0.6、Preview 0.1 和 collector 0.1/0.2 的双节点语义保持不变；
- Comparison 接受相同 Plan 0.7/Profile 0.2 的独立复跑；Pairing 与 Batch 均以
  `SOURCE_PLAN_VERSION_UNSUPPORTED` 显式拒绝 Plan 0.7；
- Workbench 生产代码保持通用只读消费，仅新增 Plan 0.7 / collector 0.3 单节点 Bundle 测试夹具。

## 3. 自动化门禁

| Gate | Result |
| --- | --- |
| Gate A dedicated tests | `10/10 PASS` |
| 旧/新消费者定向回归 | `135/135 PASS` |
| Python 3.10.6 full suite | `272/272 PASS` |
| Python 3.13.13 full suite | `272/272 PASS` |
| 双 Python `compileall` / `pip check` | PASS / `No broken requirements found` |
| Workbench tests | `60/60 PASS`，2 workers；新增 1 个单应用 Bundle 测试 |
| Workbench lint / type-check / production build | 全部 PASS；lint 0 warnings |
| Codex 内置浏览器补充复核 | 桌面/移动真实交互 PASS；Console/Warning 0；18774 已释放 |

新增 Workbench 测试直接读取同一份已验哈希 Bundle，核对 sealed Plan 的 schema 版本、Report PRIMARY、
collector source、单节点、启动/清理顺序、资源字段和两附件；没有通过 UI 文案推断缺失 dependency。

最终收尾第一次误用未安装 editable 包的系统 `python`，两个测试模块在收集期以
`ModuleNotFoundError: veritrail` 退出，实际执行 0 个测试；改用项目 `.venv` 后同一 Gate A 定向命令
`10/10 PASS`。该事实是命令环境选择错误，不改写产品结论，也不从记录中删除。

## 4. 真实 Gate A 严格串行轮

成功候选从第一个场景重新开始，保存在本地
`tmp/m11-gatea-contract03-20260814-151258`。13 个出口按合同原顺序全部符合预注册结果：

| # | Run | Stop reason | ExecutionStatus / Verdict |
| ---: | --- | --- | --- |
| 1 | `m11-gatea-positive-01` | `NONE` | `COMPLETED / PASS` |
| 2 | `m11-gatea-positive-02` | `NONE` | `COMPLETED / PASS` |
| 3 | `m11-gatea-early-exit-01` | `NODE_EARLY_EXIT` | `COMPLETED / FAIL` |
| 4 | `m11-gatea-readiness-timeout-01` | `READINESS_TIMEOUT` | `ABORTED / FAIL` |
| 5 | `m11-gatea-owner-mismatch-01` | `LISTENER_OWNERSHIP_MISMATCH` | `ABORTED / FAIL` |
| 6 | `m11-gatea-port-conflict-01` | preflight stop | `ABORTED / PENDING` |
| 7 | `m11-gatea-user-cancel-ready-01` | `USER_CANCELLED` | `ABORTED / PENDING` |
| 8 | `m11-gatea-browser-negative-01` | `BROWSER_HARD_FAILURE` | `COMPLETED / FAIL` |
| 9 | `m11-gatea-browser-collector-error-01` | `COLLECTOR_ERROR` | `ERROR / PENDING` |
| 10 | `m11-gatea-subject-drift-01` | `SUBJECT_DRIFT` | `COMPLETED / INCONCLUSIVE` |
| 11 | `m11-gatea-cleanup-failure-01` | `CLEANUP_ERROR` | `ERROR / FAIL` |
| 12 | `m11-gatea-staging-failure-01` | `EVIDENCE_ERROR` | `ERROR / PENDING` |
| 13 | `m11-gatea-memory-stop-01` | `RESOURCE_MEMORY_SOFT_LIMIT` | `ABORTED / PENDING` |

两个正向 Run 使用同一 sealed Plan/Profile，Bundle 不同且语义 Comparison 为 `MATCH`、0 differences。
Catalog 独立验真 13 个 Run，`run_count=13`、`issue_count=0`。每个存在 bootstrap Evidence 的 Run 均为
一个 APPLICATION、两个 application stream 附件；preflight port conflict 不伪造 bootstrap Evidence。

## 5. 保留的失败事实

以下失败候选继续保留，不删除、不与成功轮拼接：

| Retained run | Harness defect exposed | Resolution |
| --- | --- | --- |
| `tmp/m11-gatea-contract03-20260814-150720` | 外部 owner 观察窗口过短 | 延长有界观察并等待可判定状态 |
| `tmp/m11-gatea-contract03-20260814-150851` | owned teardown 时外部 owner 仍占用同端口 | 把外部 owner 生命周期纳入独立恢复顺序 |
| `tmp/m11-gatea-contract03-20260814-151119` | 验收器读取内部 lifecycle reason，而非公共 Bundle stop reason | 改为只从公共 `runtime.bootstrap` / Report 验证 |

这些是验收器缺陷，不是被测实现的通过事实；修复后成功轮从 Run 1 全量重跑。

## 6. 资源、安全与恢复

- 成功轮起点可用内存约 `5934 MB`；真实运行最低点约 `5649.617 MB`；
- memory-stop 使用注入值 `3500 MB` 验证停止线，该值不是宿主机真实低水位；
- application 峰值约 20.590-31.109 MB，真实 Chromium 峰值约 216.516-221.461 MB；
- 133 个文本文件敏感扫描 0 命中；未持久化绝对路径、PID、环境值、原始响应正文或凭据；
- 18774 最终可重新独占绑定，owned staging 数为 0；
- Codex 内置浏览器在 `1440x960` 与 `390x844` 分别完成输入、请求和结果列表链路，状态均到达
  `evidence ready`，无横向溢出，Console/Warning 为 0；Network 结论仍取自已封存的自动 Chromium
  Evidence，不把人工补充观察倒填进 Bundle；
- owner mismatch 与 port conflict 均保留外部 owner，并在独立恢复后回到起点；
- subject drift 保留失败 Evidence，由验收器独立恢复目标，再允许下一 Run；
- 未启动 Docker、MySQL、Redis、RabbitMQ 或其他项目技术栈。

## 7. 系统与代码质量审查

本轮按 Profile/Plan/Preview -> lifecycle -> Evidence -> Bundle/Verdict -> Catalog/Comparison ->
Pairing/Batch -> Workbench 顺序复核所有公共消费者。版本分派、authority 重推导、Browser reference、
附件 cardinality、状态归因和旧 0.6 兼容均有自动化覆盖；`git diff --check` 通过。

`bootstrap_evidence.py` 与 `bootstrap_run.py` 体量较大，登记为后续分层审查的结构性债务，不在合同稳定
阶段无依据重构。当前未发现阻断 Gate A 的稳定代码缺陷；该结论不扩张为跨平台、Docker、C2/C3、
不可信代码、任意包管理器、优雅停机或第二类真实项目能力。

## 8. 后继门禁

Gate A 固定提交完成并从 GitHub 读回后，才允许按 Contract 0.3 起草并执行 Gate B 的精确运行清单。
Gate B 必须使用预注册的 InkNarratives ref，不得修改 Gate A Core、Schema、collector、状态机或裁决来
迎合目标。Gate A 和 Gate B 全部事实闭环前，不创建 M11 标签，不进入 M12。
