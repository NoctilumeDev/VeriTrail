# VeriTrail Starter 0.1 十分钟 PASS/FAIL 黄金路径

> 状态：`S1_COMPLETE / SOURCE_ONLY / NOT_RELEASED`
>
> 基线：`VeriTrail Core 0.12.0`，Starter `single-webapp-0.1`

这条路径不是“再跑一次绿色测试”。它用同一份 sealed Profile、同一份 sealed Plan 和两个隔离的
Subject，分别保存一个 `PASS` 与一个故意保留的 `FAIL`。

```text
Starter Answers 0.1
  -> doctor
  -> init / validate / review / handoff（DRAFT / NOT_SEALED）
  -> Core seal
  -> 每个 Subject 分别生成并批准 Preview
  -> COMPLETED / PASS Bundle
  -> COMPLETED / FAIL Bundle
  -> Catalog（2 Runs / 0 issues）
  -> production Workbench desktop + mobile readback
```

## 1. 唯一业务事实变化

固定 Subject 位于 `examples/starter/single-webapp`。验收器把它复制到两个新目录：

| Subject | `app/fact.json` | 页面事实 | 预期 Verdict |
| --- | --- | --- | --- |
| PASS | `{"status":"ready"}` | `evidence ready: starter-demo` | `PASS` |
| FAIL | `{"status":"blocked"}` | `evidence blocked: starter-demo` | `FAIL` |

预注册断言始终要求 `evidence ready: starter-demo`。失败后不修改 Plan，不降低断言，也不删除反例。
两次 Run 是独立验收对；这里只证明相同标准能保留正反结果，不创建 M6 Comparison，也不声称因果。

## 2. 从源码运行

在 Windows 11 PowerShell 中，从仓库根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --editable ".[browser,command-windows]"
.\.venv\Scripts\python.exe -m pip install --editable .\starter
.\.venv\Scripts\python.exe -m playwright install chromium

Set-Location web
npm ci
npm run build
Set-Location ..

.\.venv\Scripts\python.exe scripts\starter_single_webapp_acceptance.py `
  --output artifacts\starter-single-webapp-s1
```

输出目录必须尚不存在；验收器拒绝覆盖旧证据。成功时 stdout 是一份 JSON 摘要，至少满足：

```text
execution_status = COMPLETED
verdict = PASS
runs.starter-s1-pass = COMPLETED / PASS
runs.starter-s1-fail = COMPLETED / FAIL
catalog.run_count = 2
catalog.issue_count = 0
workbench.console_error_count = 0
cleanup.application_port_released = true
cleanup.catalog_port_released = true
```

## 3. 为什么 FAIL 会出现三项失败断言

根业务失败只有一个：浏览器最终观察到 `blocked`，而 sealed Plan 预期 `ready`。Browser Adapter 在
关键步骤停止后，`all_steps_passed` 为 false，同时完整 capture 与最终 screenshot coverage 也不能成立。
因此报告包含三项 HARD 失败：

```text
starter-browser-business-steps-passed
starter-browser-capture-complete
starter-browser-screenshot-coverage
```

这不是三个相互独立的产品缺陷，而是一个根事实沿通用完整性门禁产生的三个确定性结果。Workbench
必须如实展示它们；教程不能把它们压缩成“只有一个断言失败”。

## 4. 人工权威边界

验收器用于持续证明整条产品链，因此会逐条调用真实 CLI。普通项目接入时，Starter 的边界不变：

1. `doctor` 只报告环境；
2. `init` 只生成 DRAFT；
3. `review` 由人确认显式事实；
4. `handoff.ps1` 只打印 Core 命令；
5. 用户自行 seal，并批准当前 Subject 的精确 Preview 摘要；
6. Core 根据 sealed 合同和证据给出 Verdict。

AI、Starter 和验收脚本都不能在观察结果后修改 sealed Plan，也不能替 Core 宣布 `PASS`。

## 5. 已验证出口

本地 S1 冻结轮取得：

- Profile SHA-256：`68a18c971a2066901e3421c2ba9b4bc6a97c5385473b3709844e0f5022cd6c59`；
- Plan SHA-256：`31973b67edc7bee9438bf127fabe6c39d009c24951b9236c04d99cdf11883fc2`；
- 2 个可验证 Bundle，Catalog `2 Runs / 0 issues`；
- 1440×960 与 390×844 的目录、PASS 详情、FAIL 详情；
- 0 Console error、0 page error、0 request failure、0 HTTP error、0 横向溢出；
- 应用与 Catalog 固定端口释放，owned 临时 workspace 残留为 0；
- Bundle 与公开 acceptance 摘要中无 Subject、输出目录或仓库绝对路径。

真实浏览器步骤采用有界的 10 秒单操作上限，与仓库其他真实浏览器样例一致。这个上限给 hosted
Windows runner 的 Chromium 冷启动留出确定性窗口；它不是失败重试，也不会在观察到业务结果后
放宽断言。若裁决漂移，验收器会打印实际 ExecutionStatus、Verdict、浏览器完整性与失败断言，公共
CI 只在失败时短期保留完整验收目录供复核。

这些摘要是一次可复核冻结事实，不替代未来 clean install、Release 和下载资产读回。

### Public CI 事实链

S1 的公共 CI 没有只保留最终绿色结果：

- 首轮 Public CI `32657949654`（提交 `a87d17f`）如实失败：Python 3.10 的一次 Core repeat
  出现 `COMPLETED -> ERROR` 瞬态；Python 3.13 在构建 Starter sdist 时缺少显式
  `setuptools` 构建后端。Workbench 任务通过，真实 PASS/FAIL golden path 因上游失败未运行；
- 修复提交 `ae91b9e` 固定 `setuptools==80.9.0`、更新 Starter license 元数据，并让 repeat
  断言在失败时输出完整 payload；本地同一 repeat 用 Python 3.10 与 3.13 各运行 10 次，合计
  `20/20` 通过，未复现瞬态；
- 后续 Public CI `32658836061` 在同一提交上完整通过：Python 3.10、Python 3.13、Workbench、
  Core regression、Starter normal/`-O`、Core wheel、Starter wheel、Starter sdist，以及真实
  Starter PASS/FAIL golden path 全部为 `success`。

首轮失败仍保留在 GitHub Actions 历史中；后续绿色运行是对显式修复的复核，不把已发现问题
改写成“从未发生”。
