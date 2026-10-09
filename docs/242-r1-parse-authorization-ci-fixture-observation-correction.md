# R1 Parse authorization exact-main CI 夹具观察修正

> 状态：`L0_TEST_FIXTURE_CORRECTION_CANDIDATE`
>
> 基线：`main@bf1b3f570b84aecf8d9ca789314471592aa84127`
>
> 影响层级：`L0_TEST_FIXTURE`；不修改 Core runtime、Windows Job/readiness/cleanup 合同、公共 Evidence、
> R1 Parse 合同、授权 publication、产品 timeout 或任何 Parse 实现

## 1. 正式首败

R1 Parse private implementation authorization publication PR #277 的 head
`39886d09fd8e888c4cb92edb25ad11ae8bccc665` 与 merge commit `bf1b3f570b84aecf8d9ca789314471592aa84127`
具有相同 tree `6086c3e3f8b3490ed2d1c59f4a82df30a2352c41`。

资格链保留以下事实：

```text
PR Public CI 37924644574 attempt 1
  11/11 SUCCESS

exact-main Browser Smoke 37926907552 attempt 1
  1/1 SUCCESS

exact-main Public CI 37926907456 attempt 1
  FAILURE
```

失败发生在 Python 3.10 job `113807919575` 的 Core `python -O` step。normal step 已成功；optimized 日志停在：

```text
test_early_exit_and_never_ready_are_distinct
  ...
Process completed with exit code 1
```

日志没有 traceback、assertion failure 或 unittest summary。因此只能确定进程在该 test method 执行期间退出；
不能确定失败属于 early-exit world、never-ready world，也不能确定发生在 start、readiness 或 teardown。根因保持
`UNKNOWN`，不得改写成 Core/runtime defect、Windows Job defect、runner 抖动或网络问题。

该 formal first failure 永久保留。后继成功不得覆盖或重新解释它。

## 2. 独立成立的测试观察缺口

旧测试把两个独立世界放在同一个 test method：

1. child 以 code `23` 提前退出，应得到 `NODE_EARLY_EXIT`；
2. child 保持存活但不建立 listener，应得到 `READINESS_TIMEOUT`。

每个世界又依次经过 start、readiness 与 teardown。verbose unittest 输出只能给出整个 method 名称，硬退出时没有
能力分辨上述 world 或 substep。

此外，旧测试在两次成功 start 后都没有立即注册幂等 unconditional cleanup。任意中间 assertion、Python 异常或
硬退出都会让测试缺少一个由 unittest 管理的 cleanup obligation。相邻的正向 lifecycle test 已经使用
`addCleanup(session.terminate)`，并在 readiness 不符合预期时保存 exact observation 与 bounded streams；旧负向测试
没有同等级观察面。

这些是源码可直接证明的 test-fixture observation gap，与 formal first failure 的唯一根因无关。

## 3. 最小修正

本候选只做以下修改：

```text
combined method
  -> early-exit 独立 method
  -> never-ready 独立 method

successful start
  -> immediately addCleanup(session.terminate)

test-owned temporary directory
  -> register cleanup before start
  -> unittest LIFO cleanup terminates the session before removing the directory

unexpected readiness
  -> exact readiness observation
  -> bounded stdout/stderr

explicit teardown
  -> preserve full teardown observation in assertion message

early-exit
  -> verify root_exit_code == 23

both worlds
  -> flushed test-only phase markers around start/readiness/teardown
```

phase marker 只进入测试日志，用来在 Python 没来得及产生 failure object 时保存最后完成的 test phase。它不是产品
Evidence，也不进入任何 public Schema、Bundle、Core verdict 或 runtime API。

上述 cleanup 顺序只约束 unittest 能够执行 Python cleanup 的正常结束与异常路径；解释器硬退出时不保证 cleanup
callback 会运行，此时仍以最后一个 flushed phase marker 作为主要诊断面。

## 4. 非资格诊断

同一旧 exact tree 上，本机 CPython 3.10.6 取得：

```text
targeted optimized method, fresh process x20
  20/20 PASS

full normal suite
  469/469 PASS

then full optimized suite in a fresh interpreter
  469/469 PASS
```

修正后的最终测试字节又在 CPython 3.10.6 / 3.13 的 normal / `-O` 四格中各取得定向两用例 `2/2 PASS`，
并在四格完整 Core 中分别取得 `Ran 470 tests / OK`。这些都是
non-qualifying local diagnostics：它们证明修正没有稳定破坏被测语义，也反驳“normal 先运行必然污染 optimized”
这一强假设；它们不否定 exact-main formal first failure，也不证明其根因。

## 5. 明确禁止

本候选不得：

- 修改 `OwnedServiceSession`、Job Object、readiness 或 teardown runtime；
- 放宽任何产品或测试 timeout；
- 增加 retry；
- 修改 frozen Parse contract 或授权 publication bytes；
- 启动 formal readback、reconciliation 或 Parse implementation；
- 把该修正描述为已经修复 formal first failure 的唯一根因。

## 6. 资格与后继停止线

本候选只有在最终字节完成本地相关门、原始 PR Public CI、受保护主线合入以及新 exact-main Public CI 与
Browser Smoke 后，才能成为 qualified maintenance history。

即使 maintenance exact-main 双门闭合，也只能重新进入 CONTROL LOOP，并从新的 exact main 进行 fresh installed-
product readback 与 independent reconciliation。只有授权 publication 自己预先声明的剩余门全部成立后，
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED` 才能生效。

在此以前继续保持：

```text
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```
