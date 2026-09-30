# M10 0.12 maintenance dependency prerequisite 最小前合同审计

日期：2026-10-01

## 1. 审计结论

[文档 227](227-m10-maintenance-workflow-bootstrap-ordering-counterexample-audit.md)成为 qualified history 后，当前最小问题仍然是：

> 在 phase-one ruleset 保持 active、无 bypass、无未保护窗口，且后继 workflow-only PR 继续保持精确两文件
> scope 的条件下，怎样先让 exact 0.12 maintenance line 取得当前 Workbench dependency qualification？

本审计证明一条窄路线具有合同化资格：

```text
exact maintenance tip
    -> one lockfile-only prerequisite candidate
    -> exact-head workflow_dispatch witnesses
    -> protected PR merge
    -> exact maintenance-tip workflow_dispatch witnesses
    -> fresh workflow-only bootstrap candidate
```

其中 `workflow_dispatch` run 是独立的 exact-ref witness，不是 original PR check。候选内容、PR merge authority、
dispatch observation 与 maintenance-tip qualification 必须分别绑定；相同 lock bytes、相同版本或 current-main PASS
都不能继承另一条线的 authority。

本审计只授权起草 dependency prerequisite 的最小合同。它不授权创建 dependency topic branch / PR、运行
`workflow_dispatch`、修改 maintenance branch、重开 #252、开始 workflow migration、phase two、backport、version、
Release、consumer migration 或 Parse。

当前状态为：

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_PRECONTRACT_AUDIT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_NOT_STARTED
M0_MAINTENANCE_DEPENDENCY_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

## 2. Exact source 与治理坐标

本轮重新读回的坐标为：

| 坐标 | 值 |
| --- | --- |
| current main | `b1053e483982e3fe9c22cdc15a27c2c8c2b60468` |
| current-main tree | `4bb1340807adb65b568bcb10bde3ff21b85701d5` |
| maintenance ref | `refs/heads/core-0.12-maintenance` |
| maintenance commit | `f961930ae1e69d7d88849fa2b0d40befb3e94c89 = v0.12.2^{}` |
| maintenance tree | `e0ded371266ac80b936fcbf5e00515a75dbf0950` |
| phase-one ruleset | `24216773`，active |
| bypass actors | empty |
| current user bypass | `never` |
| rules | deletion / non-fast-forward / pull request |
| required checks | none |

当前三个 open Dependabot PR 均以 `main` 为 base，没有并行 PR 指向 `core-0.12-maintenance`。因此本审计没有把
main 的依赖更新、Dependabot candidate 或任何并行 maintenance head 当作当前输入。

ruleset 只证明 maintenance tip 必须经 PR 改变；它没有 required checks，不能自己证明候选经过了适当验证。
后继合同必须另外定义 exact-head 与 exact-tip witness，同时不得把这些 witness 伪称为 branch protection 的 required
checks。

## 3. Lockfile-only 候选的有界构造

在 detached exact maintenance commit 上，以 npm `11.19.1`、公开 registry 与现有 `web/package.json` 范围执行：

```text
npm update undici brace-expansion
    --package-lock-only
    --ignore-scripts
    --registry=https://registry.npmjs.org
```

得到的候选只修改 `web/package-lock.json` 四个 lock entry：

| entry | before | candidate |
| --- | --- | --- |
| root `brace-expansion` | `5.0.9` | `5.0.12` |
| `editorconfig` nested `brace-expansion` | `2.1.4` | `2.1.7` |
| `glob` nested `brace-expansion` | `2.1.4` | `2.1.7` |
| `undici` | `7.29.0` | `7.30.0` |

字节坐标为：

```text
base lock SHA-256
FD50366E34F3FECE0CD661A18989A6BC41217B1AD92BFD3E4C79D15002CD20D1

candidate lock SHA-256
6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E
```

candidate lock 与 current main 经 PR #248 / #253 形成的当前 lock file 逐字节相同。这只说明相同 exact package
inputs 与有界更新得到同一组 bytes；它不把 main 的 PR、CI、merge、exact-main 或 continuation authority 转移给
maintenance line。

候选没有修改 `web/package.json`、workflow、runtime、tests、Python dependency、version、tag、Release 或 asset。
因此最小 dependency prerequisite 的 candidate scope 可以收缩到一个 lockfile，但该 scope 仍需合同冻结后才能
成为实际施工权。

## 4. 本地诊断 witness 与保留失败

候选 lock bytes 上完成了新的 Workbench 安装与验证：

| witness | 结果 |
| --- | --- |
| npm `11.19.1` fresh `npm ci --ignore-scripts` | 252 packages added；253 audited；0 vulnerabilities |
| Workbench regression | 14 files；172/172 PASS |
| lint | PASS |
| type-check + production build | PASS |
| full audit，`--audit-level=moderate` | 0 vulnerabilities |
| dependency tree | `brace-expansion 5.0.12 / 2.1.7`；`undici 7.30.0` |
| exact diff | `web/package-lock.json` only；12 insertions / 12 deletions |
| `git diff --check` | PASS |

本轮还曾把 CPython 3.10 / 3.13 normal / `-O` 四个完整 `347` 测试套件错误地放在同一宿主并发运行。四格分别
留下 `6 / 6 / 7 / 7` 个失败，主要终态为 `RESOURCE_MEMORY_SOFT_LIMIT`；随后立即进行的 3.10 normal 顺序重跑
仍在 Chromium / service 启动后跌破冻结的 `4096 MB` 可用内存软线，最终 `10` 个失败。该观察必须保留为：

```text
local diagnostic
    = FAIL-CLOSED under insufficient host-memory headroom
    != dependency semantic regression proven
    != Python matrix PASS
```

PR #252 在未修改 lock 的相同 maintenance source 上，原始远端 Python 3.10 / 3.13 jobs 已经 PASS；这帮助定位
本轮本机观察的环境形状，但不能替当前 lock candidate 取得资格。因此本审计没有调大预算、删除 Browser 用例、
继续串行消耗宿主资源或把失败改写成 PASS；后继合同必须把完整远端 Public CI / Browser Smoke exact-head 与
exact-tip observation 作为必需 witness。

## 5. `workflow_dispatch` 的可用语义

exact v0.12.2 的 `.github/workflows/ci.yml` 与 `.github/workflows/browser-smoke.yml` 都已声明
`workflow_dispatch`；同路径 workflow 也存在于 default branch 并处于 active 状态。GitHub 官方文档明确：

- 手动运行可通过 CLI / REST 指定 branch 或 tag `ref`；
- `workflow_dispatch` 的 `GITHUB_SHA` 是被 dispatch 的 `GITHUB_REF` branch / tag 的最后提交；
- workflow run 读接口可返回 `event`、`head_branch`、`head_sha`、`run_attempt`、`status` 与 `conclusion`，并按
  `head_sha` 过滤。

参见：

- [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [Events that trigger workflows: workflow_dispatch](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch)
- [REST API endpoints for workflow runs](https://docs.github.com/en/rest/actions/workflow-runs)

因此可以在不先修改 workflow filters 的条件下，对 dependency topic ref 和合入后的 maintenance ref 分别建立远端
observation。但 dispatch 接受的是可移动 ref，不是 immutable commit 参数；后继合同必须在触发前后独立读回 ref，
并只接纳 `head_sha` 精确等于候选 / merge commit 的 run。只凭 branch 名、最近一次绿色 run 或相同 output 都不够。

## 6. Authority 分离

最小合同必须至少分开：

| authority | owner / source | 禁止偷换 |
| --- | --- | --- |
| source identity | exact maintenance tip + one-file final diff | current main 或 v0.12.2 tag 不能替候选 head |
| dependency construction | frozen package inputs、npm version、registry、targeted update procedure | current-main version 不能直接授予 selection authority |
| content review | exact PR head、lock diff、hash、resolved URL / integrity | 0 vulnerabilities 不能替代 source review |
| merge authority | ruleset-protected PR into `core-0.12-maintenance` | dispatch success 不能直接写 branch |
| candidate qualification | exact-head Public CI + Browser Smoke dispatch runs | 不是 original PR checks，不得这样命名 |
| tip qualification | exact merged maintenance SHA 的两条 fresh dispatch runs | candidate run 不能继承给 merge SHA |
| bootstrap continuation | 由新 exact tip 重新返回 CONTROL LOOP | dependency PASS 不自动授权 workflow / phase two |

dependency candidate 可以使用与 main 相同的最终 lock bytes，但必须在 maintenance source 上重新构造、评审、运行并
取得自己的 exact-head / exact-tip observations。

## 7. 待冻结的最小串行资格链

后继合同若继续选择本审计证明可行的路线，必须把下列关系冻结为串行、不可借用的阶段：

```text
A. bind current exact maintenance tip and active phase-one ruleset

B. create one fresh topic identity from that tip
   -> change only web/package-lock.json
   -> freeze tool / registry / targeted-update inputs and final lock hash

C. complete declared local Workbench gates
   -> preserve any resource stop or setup failure

D. open one PR into core-0.12-maintenance
   -> independently read exact PR head and one-file diff

E. dispatch Public CI and Browser Smoke against the topic ref
   -> event = workflow_dispatch
   -> attempt = 1
   -> head_sha = exact unchanged PR head
   -> full declared jobs PASS

F. re-read PR head, base, diff and ruleset
   -> merge only if they still match D/E

G. read exact protected maintenance merge tip

H. dispatch Public CI and Browser Smoke against core-0.12-maintenance
   -> attempt = 1
   -> head_sha = exact merge tip
   -> full declared jobs PASS

I. return to CONTROL LOOP
   -> create a fresh workflow-only candidate from the qualified tip
   -> never reopen or rewrite #252
```

阶段 E/H 的 run 必须保存 workflow identity、event、head branch、head SHA、attempt、job matrix、conclusion 与时间。
一个 workflow run 不得替代另一 workflow；candidate exact-head 成功不得替代 merge exact-tip 成功。

## 8. 最小合同仍需作出的决定

本审计没有直接冻结实现。下一份合同必须明确：

1. targeted update 的 npm 版本、registry、命令输入、允许改变的 lock entries 与 final hash；
2. advisory 读取时间与 `npm audit --audit-level=moderate` 的资格身份；
3. exact-head / exact-tip 两次 dispatch 的 ref 前后读回和 `head_sha` reconciliation；
4. Public CI 的完整 job denominator 与 Browser Smoke 的独立身份；
5. PR head 在 dispatch 后变化、run CANCELLED / ERROR / FAILURE 或 branch tip 漂移时怎样停止；
6. merge method、merge SHA 与 maintenance tree 怎样保存；
7. dependency prerequisite 闭合后，workflow-only bootstrap 怎样以全新 candidate identity 重建；
8. 哪些 Artifact / API bytes 构成 retained evidence，以及谁有资格发布状态。

合同不得把 registry 当前响应、main 绿灯、branch 名或“版本看起来一样”当成 immutable authority。

## 9. 明确未授权

本文不授权：

- 创建、push 或删除 dependency topic branch；
- 创建 dependency PR，或直接修改 `core-0.12-maintenance`；
- 运行、rerun 或取消任一 `workflow_dispatch`；
- 重开、rerun、更新或合入 PR #252；
- 把 lockfile 加入 workflow-only PR，或把 workflow filters 加入 dependency candidate；
- 修改、disable、evaluate 或升级 ruleset `24216773`，或增加 bypass / required checks；
- 弱化 `npm audit`、改 audit level、忽略 advisory、调大产品预算或删除失败测试；
- 把本机资源停止写成 Python / Browser PASS；
- 开始 phase two、Browser classification backport、`0.12.3` version / tag / Release / assets；
- 开始 Starter consumer migration、Parse / Fact / Coverage 或重发 Parse authorization。

## 10. 本审计的资格与停止线

本文只证明 lockfile-only prerequisite 与 exact-ref dispatch 组合具有合同化资格，并列出下一合同必须冻结的 source、
scope、selection、PR、merge、exact-head、exact-tip 与 continuation identity。它不修改文档 223–227、maintenance
branch、ruleset、workflow、runtime、tests、dependencies、version、Release、Schema 或 frozen R1 contracts。

本文与 README、AGENTS、milestones 的最终字节须完成适用 Markdown/Schema 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff 与 `git diff --check`，再经过本文自己的 original PR 门、受保护
main 合入与 new exact-main 双门。只有这些门闭合，本前合同问题边界才成为 qualified history；它仍不自动授权
dependency contract 或 source write。

停止原则为：**先冻结 lockfile-only prerequisite 的 exact input、one-file scope、manual-dispatch identity、protected
merge 与 exact-tip reconciliation；合同闭合以前不创建实际 dependency candidate。dependency prerequisite 闭合后也必须
返回 CONTROL LOOP，以全新 identity 重做 workflow-only bootstrap，不能把依赖绿灯直接升级为 phase two。**
