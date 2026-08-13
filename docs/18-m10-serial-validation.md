# M10 第一轮严格串行完整复验

> 状态：`SERIAL_VALIDATED`
> 预注册日期：2026-08-13
> 实现候选：`c3118d8`（`fix(m10): harden dynamic foundation`）
> 执行依据：[M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md) 第 5 节
> 前置审查：[M10 动态地基系统与代码质量审查](17-m10-foundation-review.md)

## 1. 运行纪律

- 十二类公共退出严格按第 2 节顺序执行；每条命令只运行一个 test method，不并行；
- 每个 method 都通过真实公共 `run`、Windows Job、回环 listener、适用的真实 Chromium、Bundle、
  Catalog/Verdict 和清理断言验证自身场景；
- 任一 case 出现功能、裁决、安全、所有权、Evidence 或清理失败，立即停止本轮并保留失败；
- 十二类出口全绿后，才依次运行 Python 3.10 全量、Python 3.13 全量、前端 test/lint/type-check/build、
  依赖与静态门禁；
- 自动化全绿后仍需 Codex 内置浏览器执行正/负、刷新/返回、物理键盘并检查 Console/Network；
- 本轮不得启动阶段 D 微并行或 1000 请求压力审计。

预检快照：Windows 11，物理内存 15.78 GB、可用内存 8.72 GB，C 盘可用 139.47 GB；18770–18789
未发现 listener，仓库 `.veritrail/staging` 不存在。该快照只用于本轮起点，不替代运行中的停止线。

## 2. 预注册公共退出顺序

统一命令前缀：

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

| 序号 | 公共退出 | test method | 预期 |
| --- | --- | --- | --- |
| 1 | C1 正向成功与同权威重复运行 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_same_sealed_authorities_repeat_without_residual_contamination` | 两次 `COMPLETED/PASS`、Comparison `MATCH`、轮间无残留 |
| 2 | dependency 提前退出 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_dependency_early_exit_creates_completed_fail_bundle_without_browser` | `NODE_EARLY_EXIT / COMPLETED/FAIL`，application/browser 未创建 |
| 3 | application readiness 超时 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_application_readiness_timeout_creates_aborted_fail_bundle_without_browser` | `READINESS_TIMEOUT / ABORTED/FAIL`，双节点逆序清理 |
| 4 | Browser sealed HARD 业务失败 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_browser_business_failure_is_completed_fail_not_contamination` | 有效 browser Evidence，`COMPLETED/FAIL` |
| 5a | preflight `STOP_ESCALATION` | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_preflight_stop_creates_pending_bundle_without_starting_processes` | 零 bootstrap/browser，`ABORTED/PENDING` |
| 5b | preflight `ABORT` | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_preflight_abort_creates_pending_bundle_without_starting_processes` | 零 bootstrap/browser，`ABORTED/PENDING` |
| 6 | application READY 后用户取消 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_user_cancel_after_services_ready_creates_aborted_pending_bundle` | `USER_CANCELLED / ABORTED/PENDING`，完整逆序清理 |
| 7 | dependency/application 外部端口竞争 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_port_conflict_after_live_preview_aborts_without_touching_external_owner` | 不接管、不误杀、只含 preflight |
| 8 | dependency/application listener owner mismatch | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_listener_owner_mismatch_aborts_without_killing_external_listener` | 不误判 READY、不误杀外部进程 |
| 9 | subject 最终状态漂移 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_subject_drift_is_preserved_and_makes_public_verdict_inconclusive` | 不回滚，`COMPLETED/INCONCLUSIVE` |
| 10 | cleanup 注入失败 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_cleanup_failure_is_public_and_does_not_skip_remaining_teardown` | `CLEANUP_ERROR / ERROR/FAIL`，继续 best-effort 回收 |
| 11 | Evidence staging 注入失败 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_staging_failure_creates_public_error_bundle_after_reverse_cleanup` | `EVIDENCE_ERROR / ERROR/PENDING`，先清理再封存失败 |
| 12 | Catalog 组合接纳与损坏隔离 | `tests.test_bootstrap_run_cli.BootstrapRunCliTests.test_catalog_accepts_public_m10_outcomes_and_isolates_a_corrupt_copy` | 正向/停止 Bundle 独立接纳，损坏副本隔离 |

## 3. 公共退出运行记录

十二类公共退出按预注册顺序逐 method 串行执行，没有重排、跳项或把后续绿色结果补给前项。第 5 类
含两个独立 preflight 决策，因此实际执行 13 个 method：

| 序号 | 结果 | unittest 实际用时 |
| --- | --- | --- |
| 1 | `PASS` | 6.070 s |
| 2 | `PASS` | 1.487 s |
| 3 | `PASS` | 2.017 s |
| 4 | `PASS` | 4.484 s |
| 5a | `PASS` | 1.064 s |
| 5b | `PASS` | 1.045 s |
| 6 | `PASS` | 1.753 s |
| 7 | `PASS` | 1.633 s |
| 8 | `PASS` | 5.706 s |
| 9 | `PASS` | 2.794 s |
| 10 | `PASS` | 2.796 s |
| 11 | `PASS` | 2.818 s |
| 12 | `PASS` | 3.373 s |

第 4、9、10、11 项的 `FAIL / INCONCLUSIVE / ERROR` 是各自预注册的业务/系统退出事实；method 的
`PASS` 表示系统没有把这些负向出口错误改写成正向，并且 Evidence、Verdict 与清理符合预期。

第 1–4 项、第 5a–7 项和第 8–12 项之后分别检查 helper、约定端口和 repository staging，均为零；
最后一项后工作区仍干净，可用内存 8.68 GB。

## 4. 双运行时、前端与依赖门禁

第一次冻结候选双运行时序列中，Python 3.10 为 216/216（95.426 s）；随后 Python 3.13 在测试收集
阶段产生 35 个 `ModuleNotFoundError: veritrail`，实际产品测试为 0。按停止规则，本轮立即停止，没有
提前运行前端或浏览器，也没有用以前的 216/216 覆盖该失败。

诊断确认 `.venv313` 的 Python 3.13.13、Playwright 和 pywin32 均存在，但 VeriTrail editable binding
丢失；同时 `.venv` 虽可导入源码，pip metadata 仍停留在 `0.6.0.dev1`。这属于验收环境漂移。两个既有
虚拟环境随后只执行本仓库 `pip install --no-deps --editable .`，没有升级第三方依赖或修改产品文件；
二者均读回 `veritrail 0.11.0.dev1` 且 `pip check` 通过。

按不可拼接原则，双运行时门禁从 Python 3.10 重新开始：

| 门禁 | 最终同序列结果 |
| --- | --- |
| Python 3.10.6 全量 | `216/216 PASS`，96.804 s |
| Python 3.13.13 全量 | `216/216 PASS`，94.520 s |
| Workbench Vitest | `55/55 PASS`，8 files，2 workers 上限 |
| Workbench lint | `PASS`，0 warnings |
| Workbench type-check | `PASS` |
| Workbench production build | `PASS`，JS 167.26 kB / CSS 40.16 kB |
| Python 3.10 / 3.13 `pip check` | 均为 `No broken requirements found` |
| npm production/full audit | 官方 registry 两次均为 0 vulnerabilities |
| Python 3.10 / 3.13 compileall | 均为 `PASS` |
| repository integrity / diff | `git fsck --no-dangling`、`git diff --check` 均通过 |

环境失败、修复动作和修复后的完整重跑都保留；最终绿色不能改写成“第一次 3.13 就通过”。

## 5. Codex 内置浏览器真实链路

在系统 TEMP 中临时生成两份真实公共 Plan 0.6 Bundle：

- `m10-stage-c-positive`：`COMPLETED/PASS`，15 个 Bundle 文件；
- `m10-stage-c-browser-failure`：`COMPLETED/FAIL`，13 个 Bundle 文件，业务步骤失败保持有效
  `browser.session`。

两份 Run 独立 `validate_bundle` 后构建同一只读 Catalog，`run_count=2`、`issue_count=0`、
`duplicate_count=0`；生产 Workbench 由内置浏览器从 `127.0.0.1:18772` 真实加载：

- 目录同时呈现 PASS/FAIL，没有把有效负向包隔离成损坏；
- 正向详情为 `COMPLETED/PASS`、完整性已核验、14 个 manifest entries，Evidence Ledger 同时包含
  `runtime.preflight`、`runtime.bootstrap` 与 `browser.session`；13 个确定性断言全部 PASS；
- 真实键盘 `Tab` 后焦点环可见；正向详情刷新后 URL、裁决与完整性保持；返回目录后加载失败 Run；
- 失败详情为 `COMPLETED/FAIL`、完整性已核验、12 个 manifest entries，3 个 HARD assertion 明确
  FAIL，Console/page/failed-request 断言没有被业务步骤失败伪造为基础设施异常；
- 页面资源账册观察到生产 JS/CSS、Catalog、两份 Bundle 的 manifest、Report、Plan/Profile、
  `runtime.bootstrap`、`browser.session` 和适用附件请求；
- 移动视口 390×844 下失败裁决与 bootstrap Evidence 仍可读，`scrollWidth == clientWidth == 375`；
- 浏览器开发日志中的 warning/error 为 0。临时视口已恢复默认值。

## 6. 安全、远端与最终残留

- tracked 文本扫描没有发现本机用户绝对路径、邮箱、私钥头或真实 GitHub token；命中的
  `ghp_123...` 仅是 M9 脱敏自动化专用假 canary，并有“不进入持久化输出”的对应断言；
- 浏览器验收标签已关闭；owned Catalog server PID 身份核对后停止，18772 已释放；
- 系统 TEMP 下 Stage C 目录及其中两份临时 Bundle/Catalog 已删除。它们是可重建的本轮验收数据，
  删除不可恢复，但不包含用户项目数据；
- 最终 M10 helper=0、Catalog server=0、18770–18789 listener=0、repository staging 不存在、Stage C
  TEMP 目录=0；可用内存 8.30 GB；
- 运行完成时工作区干净，本地与 `origin/main` 均为 `b29960a0f2d6071f1fd7328dc93843175f96d5b1`。

## 7. 结论与下一门

阶段 C 已满足本计划的严格串行退出条件，M10 推进为 `SERIAL_VALIDATED`。这不等于 M10 已冻结：
阶段 D 的独立 Profile 微并行、竞争/取消交错与 1000 总请求压力审计仍未执行；最终发布、安全、远端
和标签门禁也仍未完成。下一步只能先预注册并执行阶段 D，不能跳到 M11。
