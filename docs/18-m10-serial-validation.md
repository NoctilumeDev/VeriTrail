# M10 第一轮严格串行完整复验

> 状态：`RUNNING`
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

## 3. 运行记录

尚未开始。只有实际命令、退出码、运行时长、残留复核和适用的浏览器事实完成后，才能填写本节并
改变状态。定义、计划或开发期回归不能预填 `PASS`。
