# M10 公共 CLI 宿主硬退出观察修正

> 状态：`M10_PUBLIC_CLI_HOST_EXIT_OBSERVATION_CORRECTION_QUALIFIED`
>
> 精确基线：`main@5493007d15b7895fe0dddfd4c7c617424cd15672`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core runtime、M10 生命周期合同、R1 E 实现、公共 Evidence、Schema 或 publisher

## 1. 触发事实与首败身份

R1 ReviewSlice input 阶段 E 的 docs-only 状态发布 PR
[#191](https://github.com/NoctilumeDev/VeriTrail/pull/191) 原始 head 为
`a19a06431799e05482df7dbb5944ada429389d1f`，base 为上述 exact main。该 head 只修改
`README.md`、`AGENTS.md` 与 `docs/milestones.md`，没有修改 Core、测试、CI 或 R1 runtime。原始 Public CI
[run 36034293834](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36034293834) attempt 1 保留下列正式失败：

```text
Python 3.13 / -O
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_dependency_early_exit_creates_completed_fail_bundle_without_browser

last observed unittest output:
  <test identity> ...

no terminal unittest outcome
no traceback
no failure/error summary
step exit code = 1
```

同一 run 的 Python 3.13 normal Core 回归、完整 Python 3.10 job、E3 release-download acceptance 与
Workbench 均成功；依赖双 Python job 的七个后继门被跳过。PR #191 不合并、不 rerun；任何后继绿色都不能
把该原始 attempt 改写成成功。

## 2. 已知事实与未知根因

紧邻的 E exact-main Public CI
[run 36031453261](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36031453261) 使用相同
`windows-2025-vs2026@20260907.229.1` runner image，并在同一 Core/test tree 上让 Python 3.13 normal 与
`-O` 两次执行该用例成功。PR #191 的差异又只有 Markdown。因此原始失败没有证据支持“E runtime 回归”或
“状态文案改变了 Core 行为”。

相同 PR head 的本地 Python 3.13 `-O` 诊断中：

- 精确目标用例独立执行 `20/20 PASS`；
- 前一 alphabetic 用例 `test_cleanup_failure_is_public_and_does_not_skip_remaining_teardown` 与目标用例成对执行
  `10/10 PASS`；
- 一次更广的 Core 顺序执行也让目标用例取得 terminal `ok`。

这些观察只能证明首败没有稳定复现。它们不能证明首败没有发生，不能把原因写成 runner 抖动，也不能证明
某个 `TerminateProcess`、Job、浏览器清理或端口竞争假说为真。精确根因保持 `UNKNOWN`。

## 3. 已证实的测试观察缺口

旧用例通过测试进程内直接调用 `veritrail.cli.main(...)` 来执行公共 Run：

```text
unittest host
  -> in-process CLI main
     -> owned service lifecycle
```

如果被测路径让宿主解释器在 Python 异常机制之外硬退出，测试 harness 与被测 CLI 共享同一进程，无法保留
return code、stdout、stderr、断言失败或 suite summary。原始 Artifact 正好只留下测试 identity 与 step-level
exit code。这证明旧夹具有一个独立于底层触发原因的观察缺口：**被测宿主硬退出时，裁判也随之消失。**

这个缺口不等于 Core runtime 已被证明会主动杀死自己；它只说明当前测试拓扑没有资格区分这种世界与其他
无 traceback 的宿主终止。

## 4. 最小修正

只把该 negative public-CLI 用例改为由 unittest 父进程启动同一解释器的独立 CLI 子进程：

```text
unittest observer
  -> exact sys.executable
  -> preserve current normal / -O optimization mode
  -> python -m veritrail run <same sealed inputs>
  -> capture return code + stdout + stderr
  -> continue validating the same Bundle, Evidence, cleanup and port facts
```

正常路径的产品命令、sealed Plan/Profile、preview approval、run id、输出 Bundle 与后继断言均不改变。若 CLI
子进程再次硬退出，外层 unittest 仍存活并把 return code 与捕获流写进失败诊断；它不会把 nonzero exit
转换成 PASS，也不会重试。

一个临时 hard-exit mutation 把 CLI 子进程替换为 `os._exit(1)`。外层测试稳定存活并报告
`returncode == 1`，证明新边界观察的是宿主硬退出，而不是只把调用方式换了一遍。mutation 随即撤销，不进入
候选字节。

## 5. 非声明与停止线

本修正不声明：

```text
isolated child PASS
=> 原始首败已解释

future CI PASS
=> 原始首败是偶发

captured return code
=> 已知道谁终止了进程

test topology correction
=> Core runtime 被修复
```

在本维护自己的本地四格、原始 PR 门、受保护合入与新 exact-main 双门成立以前，状态只能是：

```text
M10_PUBLIC_CLI_HOST_EXIT_OBSERVATION_CORRECTION_CANDIDATE
R1_E_STATUS_PUBLICATION_REQUALIFICATION_BLOCKED
R1_REVIEW_SLICE_INPUT_STAGES_F_H_NOT_STARTED
```

维护闭合以后，PR #191 的原始失败仍保持 `FAILURE / UNKNOWN`。E 状态发布必须从 maintenance-qualified
exact main 建立新的 source identity，再独立接受完整门禁；不得在原 head 上 rerun 洗白。F 仍不得启动。

## 6. 当前候选证据

目标用例在同一候选字节上通过双 Python normal/`-O` 四格；完整 `test_bootstrap_run_cli` 也通过四格：

| gate | Python 3.10 | Python 3.13 |
| --- | --- | --- |
| target normal | `1/1 PASS` | `1/1 PASS` |
| target `-O` | `1/1 PASS` | `1/1 PASS` |
| module normal | `24/24 PASS` | `24/24 PASS` |
| module `-O` | `24/24 PASS` | `24/24 PASS` |
| hard-exit mutation | — | outer harness survived and reported `returncode == 1` |

另一次 Python 3.10 source-root `python -m unittest -q` 尝试没有形成完整 Core 资格观察：测试发现缺少
`veritrail_github`，真实浏览器用例又因当前本机资源状态在目标生命周期事件前触发
`RESOURCE_MEMORY_SOFT_LIMIT`。该命令既没有复刻 Public CI 先安装 Core extras、GitHub Evidence 与 Review
Attention 的环境，也没有取得预期的完整 suite 终态，因此只保留为本地 gate setup / environment mismatch，
不计作候选 PASS 或产品回归 FAIL。

完整 Core installed-topology 四格、维护 PR 与远端资格仍待闭合，因此当前仍只是 correction candidate。维护
PR 的干净 Windows runner 必须独立执行仓库原有完整门；后继远端成功也只证明修正候选在该新观察中通过，
不会解释 PR #191 的原始失败。

## 7. 远端资格与后继状态发布

maintenance PR [#192](https://github.com/NoctilumeDev/VeriTrail/pull/192) 的 original head
`e7c1bd8e2fe60b648074fae90bda83d2e73331ae` 在 Public CI
[run 36038413885](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36038413885) attempt 1 取得
11/11 PASS；双 Python 聚合车道均完整通过 normal/`-O` Core、各消费者回归、构建与 clean-install。该 PR
随后受保护合入 `main@89a069277c361a55afdd963f2a1e5e75aee9a39a`；该 exact main 的 Public CI
[run 36041811403](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36041811403) attempt 1 为
11/11 PASS，Browser Smoke
[run 36041811369](https://github.com/NoctilumeDev/VeriTrail/actions/runs/36041811369) attempt 1 为
1/1 PASS。因此测试观察修正已独立资格化：

```text
M10_PUBLIC_CLI_HOST_EXIT_OBSERVATION_CORRECTION_QUALIFIED
R1_E_STATUS_PUBLICATION_REQUALIFICATION_IN_PROGRESS
R1_REVIEW_SLICE_INPUT_STAGES_F_H_NOT_STARTED
```

PR #191 仍保持 closed、unmerged，其 original Public CI `FAILURE / UNKNOWN` 没有被 #192 或新 exact-main
绿灯覆盖。E 状态发布只能从上述 maintenance-qualified exact main 建立新的 source identity，再独立接受
docs-only PR 与合入后 exact-main 门；该链闭合前不得启动 F。
