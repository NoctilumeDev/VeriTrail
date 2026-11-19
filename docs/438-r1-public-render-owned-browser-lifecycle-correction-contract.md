# R1 Public Render owned-browser 生命周期修正合同 0.2

> 状态：`CONTRACT_CANDIDATE / NOT_QUALIFIED / IMPLEMENTATION_NOT_AUTHORIZED`
>
> 基线：`main@24d728065b1d165eb3e241c872606c8356fabd10 / tree=2a0b7933849d8f6be99abac307d9ad463a78fb66`
>
> 影响层级：`L2_CONTRACT`；只显式 reopen P2 Public Render 的 owned-browser 生命周期与 cleanup
> 边界。GitHub observation/fact Schema、coverage 含义、Core Verdict、R1 Manifest 语义以及已发布
> `github-evidence-v0.1.0` 字节均不改变。

## 1. 触发事实不是 doc437 内容错误

[文档437](437-r1-picomatch-advisory-withdrawal-and-workbench-audit-recovery.md) 的候选已经由 PR #499
以 `base=8a9233582a519760e2c3008e6d8e1324442ba687 / head=f22824a552161a8e5162dca9f4977de0324e4691 /
tree=2a0b7933849d8f6be99abac307d9ad463a78fb66` 合入当前精确主线。original Public CI
`44539372086`、exact-main Public CI `44549026856` 与 Browser Smoke `44549026705` 均为 attempt 1
SUCCESS（15/15、15/15、1/1）。这些门只证明候选及主线门成立，不替代 fresh installed-product
readback。

fresh readback identity `r1d437-formal-doc437-1-24d7280` 使用公开 GitHub Evidence `0.1.0`：

1. P1 API 已形成 `COMPLETE` Evidence；
2. P2 navigation 在约 `30,007 ms` 以 ERROR 终结；
3. frozen `max_elapsed_ms=45,000` 到期后，cleanup 仍阻塞；
4. 观察在 `1,512,992 ms` 时仍没有 terminal event；
5. 先外部终止 owned Chromium root 后，超过 60 秒仍未释放；只有再终止本 session 的 owned
   Playwright driver，原调用才在 `1,640,992 ms` 形成 terminal ERROR；
6. 终态保留 `CLEANUP_FAILED / COLLECTION_WINDOW_EXCEEDED / NAVIGATION_NOT_OBSERVED /
   NAVIGATION_PROJECTION_MISSING / RENDER_NAVIGATION_FAILED / RESPONSE_BODY_OBSERVATION_FAILED`，
   Core Verdict 未创建，lower external trigger 保持 `UNKNOWN`。

原始记录没有被覆盖：

| identity | SHA-256 | 说明 |
| --- | --- | --- |
| pre-containment | `24de3f51ac99c5dcf2e4c8c67313efbcc7c00bf2e640f80edeb25c56b407522b` | 首次封存 STILL_RUNNING；其中 process-tree 字段受已保留的 PowerShell 参数解析缺陷影响而不完整 |
| containment | `e30e87eafa76585c355f9e58ca50dcb9c79bf31419671a57ddb5c8909b43d399` | owned Chromium 与 Playwright driver 的外部 containment、最终产品 ERROR |
| product render | `999b8e115dbc8d8417e69527f0954a715af055febc622dbb3f18e88a699d3154` | 产品形成的 P2 ERROR Evidence |
| setup-error successor | `e32e102eb8aa2ebdedc1a3c9bcab3e5d0e6b72ec33b89f41ff190d39575c15a4` | 补充 probe 与 unittest 启动证明设施错误，不改写前三项 |

因此 doc437 当前只能是：

```text
MERGED
EXACT_MAIN_DUAL_GATES_PASS
READBACK_NOT_QUALIFIED
NOT_QUALIFIED_HISTORY
```

后继不得重跑该 formal、把 P1 COMPLETE 拼成整体 PASS、改 marker、缩短正文或用后来的成功覆盖这次
产品 ERROR。

## 2. 被击穿的 frozen 前提与最小 reopen

[P2 合同](89-p2-public-render-collector-contract.md)冻结的是一次 bounded browser execution、单一
`max_elapsed_ms=45000` 绝对采集窗口、异常后零 owned residue，以及 failure 后保留 ERROR 而非猜测成功。
当前实现把 page/navigation timeout 绑定到该 deadline，却让以下同步 cleanup 调用依次直接运行：

```text
response-body controller close
  -> CDP detach
  -> BrowserContext close
  -> browser close
  -> Playwright stop
```

这些调用没有共同的外部 interrupt owner。某一步阻塞时，后续 cleanup 与 terminal publication 都不会发生。
所以被击穿的是：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_AND_CLEANUP
```

不是以下边界：

- GitHub 页面、API 或 advisory 的真实性；
- `github-public-render-facts/0.1` 的 fact identity；
- `COMPLETE / PARTIAL / ERROR / NOT_APPLICABLE` 的含义；
- response-body `8/32 MiB`、512 requests、零重试、匿名只读或 URL allowlist；
- Core evidence sufficiency、Verdict priority、P3 handoff；
- Review Attention R1 Manifest、Evidence carrier 或 global composition authority。

## 3. 修正合同

### 3.1 一个绝对采集 deadline，一个 owned interrupt owner

每个 production `RenderBrowserSession` 必须在启动锁定的 Playwright `1.62.0` 后机械取得本 session 自己的
Playwright driver process identity，并建立一个只绑定现有绝对 collection deadline 的 guard：

1. deadline 前正常关闭时，guard 必须被取消且不得终止 driver；
2. deadline 到达而 session 仍未关闭时，guard 只能终止该 session 自己的 driver；
3. driver identity 缺失、无效或不属于当前 session 时，必须在正式采集前 fail closed；
4. termination 失败必须显式进入 cleanup error，不能被吞掉；
5. driver termination 只提供本地 containment，不把 navigation/body/network failure 改名为 deadline success；
6. termination 后的 Evidence 仍必须是 `ERROR`，并保留原 phase、coverage reasons、cleanup errors 与
   active-stream facts。

guard 不获得远端 cleanup、GitHub write、process discovery、任意 PID kill 或跨 session authority。它也不能用
sleep/poll 刷新 deadline，不能在 cleanup 开始时再取得一份新的相对预算。

### 3.2 bounded release envelope

`max_elapsed_ms=45,000` 继续是语义采集窗口，不提高、不刷新。deadline 触发后的本地 owned process-tree
release 允许最多 `5,000 ms` 的 cleanup-only envelope；因此外部生命周期验收上限为：

```text
max_elapsed_ms + 5,000 ms
```

这个 envelope 只允许释放本 session 的 driver/Chromium descendants 与关闭本地资源，不能继续导航、采样、
采集 body、构造新事实或恢复 attempt。超过该 envelope、仍有 residue 或 guard thread 未退出都必须失败。

### 3.3 版本与 distribution 边界

当前源码 distribution 已因既有 state-bound authority maintenance 使用 `0.1.1.dev0`；本修正只能进入该
未发布 source successor。不可移动的 `github-evidence-v0.1.0` tag、Release、wheel、sdist、summary 与
checksum 保持原字节和历史资格，且不得声称已含本修正。

在 repaired source exact-main 资格成立以前，公开 `0.1.0` 的 P2 path 不再拥有新的 bounded formal
qualification authority；P1 Structured API 与 raw exact-Git observation 不受影响。修正实现闭合后必须返回
CONTROL LOOP，独立决定 GitHub Evidence `0.1.1` release contract；没有公开 successor Release 时，不得把
exact-source PASS 写成公开 installed-product 已恢复。

## 4. 已完成的 feasibility 只作 witness

隔离 probe 对锁定 Playwright `1.62.0` 启动真实 Chromium，在一个阻塞的同步 Playwright call 中于 deadline
终止 owned driver。调用返回、Node 与全部 Chromium descendants 释放、无 residue；记录 SHA-256 为：

```text
19ebf6fcea883871f173ce49d4b37b737df1174d0b3e9d5e120286543ecdce47
```

另一个隔离工作树存在未提交 exact-source 草案，Python 3.10/3.13 的 unit 与真实 Chromium focused
witness 已通过。它们只证明修正路径可行：没有 commit、PR、original gate、protected merge、exact-main gate、
fresh repaired-product readback 或 release identity，因此当前仍是：

```text
NON_QUALIFYING_FEASIBILITY_DRAFT_EXISTS
IMPLEMENTATION_NOT_AUTHORIZED
```

## 5. implementation acceptance matrix

合同冻结后重建的实现候选必须至少证明：

1. normal Browser/Context/CDP/body-controller cleanup 在 deadline 前完成且不触发 driver termination；
2. response-body cleanup、CDP detach、context close、browser close 或 Playwright stop 任一同步调用阻塞时，
   同一个绝对 deadline 能释放调用并继续 terminal publication；
3. 真实 Playwright + matching Chromium 的 5 秒测试窗口在总计 10 秒内返回、记录 deadline termination 且
   owned process-tree/staging residue 为零；
4. driver identity 缺失/无效、termination failure 与 guard-thread residue 全部 fail closed；
5. navigation timeout、body over-limit、aborted navigation、HTTP 404/500、正常 COMPLETE、P1→P2 paired
   collection 与 P3 handoff 既有结果不漂移；
6. ERROR path 不创建 Core PASS，不把 cleanup-only envelope 算作 collection success；
7. Python 3.10/3.13 × normal/`-O` 的 GitHub Evidence full suite、wheel-only install、Core-only imported Evidence、
   Public CI、Browser Smoke 与 Workbench audit 通过；
8. exact-source repaired wheel 的 fresh anonymous negative lifecycle readback 在 frozen 外部窗口内终结，随后
   README/doc437/本文的 P1/API raw identity 与 public bytes 独立对账；
9. primary `audit.json` SHA-256 继续为
   `4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`；
10. 失败 identity、setup errors 与旧 public `0.1.0` 资产全部保留。

## 6. 本 docs-only candidate 的资格链

本文候选只允许修改 `README.md / AGENTS.md / docs/438... / docs/milestones.md`。它自己的资格链必须是：

```text
final docs-only bytes
  -> link / marker / exact scope / audit continuity
  -> original PR Public CI attempt 1
  -> protected exact-head merge
  -> new exact-main Public CI + Browser Smoke
  -> fresh anonymous installed P1 API + exact-Git byte observations
     for README / doc437 / doc438 / milestones
  -> independent reconciliation
  -> finite closeout
```

P2 是本次被 reopen 的对象，不能在修正以前又充当本合同的完整性证明。这里显式使用已发布产品的 P1
Structured API 与 exact-Git raw bytes；不得把它写成 P2 Render PASS，也不得降低后继修正实现自己的真实
Chromium 门。

全部门闭合后，最多生效：

```text
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_CONTRACT_0_2_FROZEN
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_ALLOWED
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回 CONTROL LOOP，从新的 exact main 重建 implementation candidate。实现闭合后仍须重新判断
source freeze、public `0.1.1` release、doc437 successor readback 与 Manifest 0.2 feasibility 的顺序，不能按本文
编号自动前进。`proof_is_not_problem_solving = true`、`local_not_global = true`；R1 完成后的 human + AI
全项目复核继续是独立后续目标。
