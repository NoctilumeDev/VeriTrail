# M10 0.12 maintenance dependency drift 最小前合同审计

日期：2026-10-09

## 1. 审计结论

[文档 233](233-m10-maintenance-dependency-drift-counterexample-audit.md)成为 qualified history 后，本轮从新的
exact main 重新绑定 maintenance source、ruleset、PR #264 首败与官方 registry。当前最小问题仍然是：

> 在 `core-0.12-maintenance@6ed18ae8...` 不移动、PR #264 永久保持关闭/未合入/首败不变的条件下，能否形成一条
> 最小、可复算、不会借用 current main authority 的 dependency-drift construction 与 qualification chain？

本审计证明一条窄路线具有合同化资格：

```text
exact maintenance tip
    -> one lockfile-only drift candidate
    -> bounded deterministic reconstruction
    -> local Workbench qualification
    -> exact candidate-head workflow_dispatch witnesses
    -> protected ordinary PR merge
    -> exact maintenance-tip workflow_dispatch witnesses
    -> return to CONTROL LOOP
```

`web/package.json` 不需要改变。以 npm `11.19.1`、官方 registry 与三个 package-name 输入进行 targeted
lock update，可以从 exact base 两次逐字节构造同一 lock：只有 14 个 package-lock entry 改变，最终 SHA-256 为
`D9FBF89C...00A4`。fresh install、172 项 Workbench regression、lint、type-check/build 与 moderate audit 均通过。

这些事实只授权起草 dependency drift 最小合同。本文不授权修改 dependency bytes、创建 maintenance topic / PR、
运行 dispatch、重做 workflow bootstrap、发布 0.12.3，或开始 Parse / Fact / Coverage / claim fidelity 施工。

本文只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDIT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_NOT_STARTED
M0_MAINTENANCE_DEPENDENCY_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

## 2. Exact source 与治理坐标

本轮重新读回：

| coordinate | exact value |
| --- | --- |
| current main | `0f2fef265582f9bf80c32e3c08ff1580250d67ef` |
| current-main tree | `677ede377b446261abe11a3a078bacbc35b00120` |
| maintenance ref | `refs/heads/core-0.12-maintenance` |
| maintenance commit | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` |
| maintenance tree | `42732643af743ca4aa9e801d61e5b49a04c4f54f` |
| `web/package.json` blob | `b38efdf88c439528a5b8af799e7ab8935037b3fc` |
| base `web/package-lock.json` blob | `3b37cc4f29a74a370cd15e778953aedd372283b7` |
| base lock SHA-256 | `6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E` |
| Public CI workflow blob | `c094d2cb84a2147e2b8bba1a7e76f140905d1a4d` |
| Browser Smoke workflow blob | `413f35ad9f768eb323d0058b82bdd8eaca177be1` |
| phase-one ruleset | `24216773`，active，no bypass，current user `never` |
| maintenance open PRs | `0` |

ruleset 继续禁止 deletion / non-fast-forward，并要求 PR 与全部 review thread resolved；required checks 仍为空。
因此 merge governance 与 dependency qualification 必须分开：ruleset 能阻止直接写 branch，不能替代 candidate-head / exact-tip
workflow witnesses。

PR #264 仍是：

```text
base    6ed18ae8b3d8b98b6e5be7af709aa868590ee914
head    585f98252d3c18727a0f19cb0eb1a28b362c9dc9
state   CLOSED / NOT MERGED
run     37795167502 / attempt 1 / FAILURE
scope   two workflow files only
```

它没有 rerun、head rewrite 或 merge。本文不重解释它的 original failure。

## 3. 最小可复算构造

### 3.1 固定输入

从第 2 节 exact maintenance commit 的 detached worktree 开始，固定：

```text
node
    v24.14.0

npm
    11.19.1

registry
    https://registry.npmjs.org

command, from web/
    npm update vue postcss-selector-parser source-map-js
        --package-lock-only
        --ignore-scripts
        --registry=https://registry.npmjs.org
```

`web/package.json` 的 direct Vue range 已是 `^3.5.41`，因此解析到 `3.5.43` 不需要 manifest write。三个命令输入是
selection seed；完整合格输出是 lock closure，而不是只允许三个同名 entry 改变。

第一次尝试把 exact versions 写进 `npm update` 参数：

```text
npm update vue@3.5.43 postcss-selector-parser@7.1.6 source-map-js@1.2.2 ...
```

npm `11.19.1` 在写入前以 `EUPDATEARGS` 拒绝：update arguments must only contain package names。工作树未产生 diff。
该结果是 construction-command setup failure；它证明这条语法不能进入后继合同，不能被后来的成功覆盖。

### 3.2 确定性复算

支持的 package-name-only 命令先从 base 构造候选，再 `git restore` 回 exact base 并 fresh 重跑。两次都得到：

```text
candidate package-lock Git blob
    297be5c0bcc30729c0f4c3f4322be74641b2a916

candidate package-lock SHA-256
    D9FBF89CA905EC2602B9956E986E24F74C38AAF4DE3EA960D1DBA3905EBD00A4

package.json Git blob
    b38efdf88c439528a5b8af799e7ab8935037b3fc

tracked diff
    web/package-lock.json only
    68 insertions / 68 deletions
```

所以当前 candidate construction 是 deterministic byte reconstruction，不只是“第二次也审计为零漏洞”。

## 4. 完整 allowed-entry projection

base 与 candidate 的 `packages` map 恰有 14 个 entry 不同；root manifest projection 不变：

| entry | before | candidate |
| --- | --- | --- |
| `node_modules/@vue/compiler-core` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/compiler-dom` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/compiler-sfc` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/compiler-ssr` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/reactivity` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/runtime-core` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/runtime-dom` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/server-renderer` | `3.5.41` | `3.5.43` |
| `node_modules/@vue/shared` | `3.5.41` | `3.5.43` |
| `node_modules/nanoid` | `3.3.18` | `3.3.20` |
| `node_modules/postcss` | `8.5.26` | `8.5.29` |
| `node_modules/postcss-selector-parser` | `7.1.5` | `7.1.6` |
| `node_modules/source-map-js` | `1.2.1` | `1.2.2` |
| `node_modules/vue` | `3.5.41` | `3.5.43` |

后继合同必须冻结这 14 个 entry 的 version、resolved URL、integrity 与内部 dependency reference 的完整 canonical
projection，而不能只冻结四个 advisory package 名。Vue 子包必须保持同版闭包；PostCSS 的 Nano ID 与 Source Map
依赖也是实际解析结果，不能被称为“无关变化”后漏出 denominator。

current main lock 的 blob / SHA-256 分别是 `5c33c3c0...` / `E94FE29F...8C6F`，与本轮 maintenance candidate
并不逐字节相同。main PR #262 的相同修复范围只提供 bounded candidate evidence；maintenance candidate 的 package
manifest scope、base、构造命令、final hash、PR、dispatch、merge 与 exact-tip authority 都必须独立取得。

## 5. 本地资格 witness 与观察归层

candidate bytes 上串行完成：

| witness | result |
| --- | --- |
| npm `11.19.1` fresh `npm ci --ignore-scripts` | 252 packages added；253 audited；0 vulnerabilities |
| Workbench regression | 14 files；172/172 PASS |
| lint | PASS |
| type-check + production build | PASS |
| `npm audit --audit-level=moderate` | exit 0；0 vulnerabilities |
| installed tree | Vue family `3.5.43`；selector parser `7.1.6`；source-map-js `1.2.2`；PostCSS `8.5.29`；Nano ID `3.3.20` |
| exact tracked diff | `web/package-lock.json` only |
| `git diff --check` | PASS |

本次 audit observation 使用 official registry；结束时点为 `2026-10-08T16:21:21Z`。它是 timed registry/advisory
observation，不是 lock bytes 的永久安全证明。candidate-head 与 maintenance-tip Public CI 必须各自重新观察。

第一次 package projection 辅助脚本漏传临时 base-lock path 环境变量，在读取 JSON 前以 `KeyError` 终止；候选字节未变。
这属于 audit-harness setup error。只修传参后，脚本机械得到 14-entry projection 与 root manifest unchanged。该错误不计为
dependency candidate failure，也不从历史删除。

文档 228 保留的本地 Python resource-stop observations 继续属于原身份。本审计没有调大预算，也没有把 Workbench-only
local PASS 冒充完整 Python / Browser qualification；后继合同仍须用远端 exact-head / exact-tip workflow denominators。

## 6. Authority 分离

| authority | owner / source | 禁止偷换 |
| --- | --- | --- |
| base source | exact maintenance commit、tree、manifest/lock blobs | branch 名或 current main 不能替代 exact bytes |
| selection construction | npm `11.19.1`、official registry、三个 package-name seed、完整 14-entry closure | advisory package 名不等于完整 allowed projection |
| deterministic content | final lock blob / SHA-256、one-file exact diff、fresh reconstruction | 0 vulnerabilities 不证明字节 identity |
| local behavior | fresh install、tests、lint、build、timed audit | 本地 Workbench PASS 不证明 Python / Browser |
| merge governance | active ruleset + ordinary PR into maintenance | dispatch success 不能直接写 branch |
| candidate qualification | exact candidate-head Public CI + Browser Smoke dispatch | 不是 original PR checks 或 required checks |
| tip qualification | exact merged maintenance-tip fresh Public CI + Browser Smoke dispatch | candidate runs 不能继承给 merge SHA |
| bootstrap continuation | qualified new tip 返回 CONTROL LOOP | dependency PASS 不自动复活 #264 或授权 workflow write |

## 7. 待冻结的最小串行资格链

后继合同若沿用本审计证明可行的路线，必须冻结：

```text
A. bind exact maintenance tip, package inputs, workflows and ruleset

B. create one fresh topic from that exact tip
   -> run the frozen package-name-only construction
   -> permit web/package-lock.json only
   -> reconcile the complete 14-entry projection and final hash

C. complete declared local Workbench gates
   -> preserve setup, registry, resource or product failures by identity

D. open one ordinary PR into core-0.12-maintenance
   -> fresh read exact base/head, one commit, one file and one-file diff

E. dispatch Public CI and Browser Smoke against the unchanged topic ref
   -> event = workflow_dispatch
   -> attempt = 1
   -> head_sha = exact PR head
   -> Public CI 7/7 and Browser Smoke 1/1 PASS

F. fresh re-read PR, topic ref, ruleset, diff, hash and original dispatch identities
   -> stop on any drift

G. merge through the protected PR path
   -> read exact maintenance merge SHA / tree / lock bytes

H. dispatch fresh Public CI and Browser Smoke against core-0.12-maintenance
   -> event = workflow_dispatch
   -> attempt = 1
   -> head_sha = exact new maintenance tip
   -> Public CI 7/7 and Browser Smoke 1/1 PASS

I. independently reconcile retained evidence
   -> return to CONTROL LOOP
   -> decide whether a new workflow-only candidate is still the smallest legal seam
```

Public CI 的七项 denominator 继续是 Python 3.10、Python 3.13、两个 wheel-only、E3 download acceptance、
Workbench 与 Starter golden path；Browser Smoke denominator 继续是独立的 Production Workbench smoke。workflow blob、
event、head branch、head SHA、attempt、job names / IDs、conclusion 与 timestamps 都须保存。

topic ref 是可移动名称。每次 dispatch 前、触发后和终结后都要 fresh 读回 ref，并只接纳 run API 返回的 exact
`head_sha`。一个 workflow 的 PASS、旧 run、attempt > 1 或最近绿色 run 都不能替代另一个必需 identity。

## 8. 下一合同必须作出的决定

下一份最小合同至少要冻结：

1. exact base source、package blobs、workflow blobs、ruleset 与无并行 maintenance PR 前提；
2. npm / Node / registry identity、package-name-only command 与禁止 exact-version `update` 语法；
3. 14 个 allowed entries 的完整 version / resolved / integrity / dependency-reference projection；
4. candidate lock blob / SHA-256、one-file scope 与确定性 fresh reconstruction；
5. local Workbench gates、audit observation time 与 setup / registry / resource failure 分类；
6. topic、PR、base/head、manual dispatch、ordinary merge 与 maintenance-tip identity；
7. candidate-head 与 exact-tip 两轮 7/7 + 1/1 witness，及 ref/head reconciliation；
8. #264 永久保持关闭、未合入、首败不变；
9. retained evidence 的最小集合与状态发布 authority；
10. qualification 闭合后强制返回 CONTROL LOOP，而不是自动启动 workflow bootstrap。

## 9. 明确未授权

本文不授权：

- 修改 `core-0.12-maintenance`、dependency、workflow、runtime、tests、timeout、budget 或 ruleset；
- 创建/push/delete dependency topic，创建 PR，或运行/rerun/cancel `workflow_dispatch`；
- 直接复制、merge 或 cherry-pick PR #262；
- 重开、rerun、改 head、合入、删除或重新解释 PR #264；
- 弱化 audit level、忽略 advisory、使用 ambient mirror 代替 frozen registry；
- 把 workflow files 塞入 dependency candidate，或把 dependency bytes 塞回旧 workflow candidate；
- phase two、host-socket backport、version/tag/Release/assets/public readback 或 consumer migration；
- Parse / Fact / Coverage、Schema、publisher、Bundle 或 `DECLARED_CLAIM_FIDELITY` 施工；
- 创建共享 dependency abstraction 或把一次 timed audit 提升成永久安全结论。

## 10. 本审计资格与停止线

本文与 README、AGENTS、milestones 只发布 precontract 问题边界，不修改 maintenance ref、dependency、workflow、
ruleset、runtime、frozen contracts 或 releases。最终字节必须完成适用 Markdown/Schema 四格、relative links、UTF-8、
fence/heading、required markers、敏感路径、exact four-file scope 与 `git diff --check`，再经过本文自己的 original PR
Public CI、受保护 main 合入与 new exact-main Public CI + Browser Smoke。

当前 final-byte candidate 已完成：

- CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `tests.test_markdown`，各 `4/4 PASS`；
- UTF-8 without BOM、LF/final LF、balanced fences、duplicate heading、relative-link 与敏感绝对路径检查；
- exact four-file scope：README、AGENTS、milestones 与本文；
- 113 个 heading、595 个 relative link 的只读结构检查；
- required marker 与 `git diff --check` PASS。

第一次四格 invocation 未设置源码 worktree 的 `PYTHONPATH=src`，四次均在 test collection 时以
`ModuleNotFoundError: veritrail` 终止，未执行测试、未改最终字节。该结果保留为 local test-harness setup failure；显式
绑定仓库源码 import path 后，同一候选字节完成上述四格。它不是 Markdown failure，也没有被后来的 PASS 改写。

只有这些门闭合，`M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDITED` 才成为 qualified history，并只授权起草
dependency drift 最小合同。dependency source write、topic / PR / dispatch / merge、workflow bootstrap 与 release 继续
未开始。

停止原则为：**先冻结 exact source、package-name-only construction、完整 14-entry closure、one-file identity、两轮
manual-dispatch witness、受保护合入与失败保留；合同闭合以前不创建 dependency candidate。dependency qualification
闭合以后仍须返回 CONTROL LOOP，不能把绿色 audit 自动升级为 workflow 或 release authority。**
