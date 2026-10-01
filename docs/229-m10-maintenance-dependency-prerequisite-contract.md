# M10 0.12 maintenance dependency prerequisite 最小合同

日期：2026-10-01

> 状态：`CONTRACT_CANDIDATE`。本文只冻结 0.12 maintenance dependency prerequisite 的 source、构造、
> review、dispatch witness、受保护合入、exact-tip reconciliation 与失败语义。本文不是 dependency candidate，
> 不创建 branch / PR，不运行 workflow，不修改 maintenance line，也不授权 workflow bootstrap、phase two、
> 0.12.3 backport / release、consumer migration 或 Parse。

## 1. 合格输入与合同问题

[文档 228](228-m10-maintenance-dependency-prerequisite-precontract-audit.md)已经完成自己的资格链：

| gate | identity | result |
| --- | --- | --- |
| candidate PR | `#255`，head `3b885a7230e1af37a00dcd8db5fed6faefbc4dd4` | exact 4-file docs-only diff |
| original Public CI | `36786553995`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `1227d41ff3c0d052f6b9e90f8be55ae89b2912fc` | merged |
| exact-main Browser Smoke | `36789112562`，attempt 1 | `1/1 SUCCESS` |
| exact-main Public CI | `36789112514`，attempt 1 | `11/11 SUCCESS` |

因此 precontract boundary 已成为 qualified history。当前最小合同问题是：

> 怎样只改变 exact 0.12 maintenance source 的一个 lockfile，以不可借用的 exact-head / exact-tip
> `workflow_dispatch` observations 证明当前 dependency qualification，同时仍由 phase-one ruleset 保证
> maintenance tip 只能经 PR 改变？

合同只接受以下顺序：

```text
exact protected maintenance tip
    -> fresh one-file dependency topic candidate
    -> bounded local construction and review
    -> protected PR identity
    -> exact candidate-head Public CI + Browser Smoke dispatch witnesses
    -> unchanged PR/ruleset reconciliation
    -> ordinary merge commit
    -> exact maintenance-tip Public CI + Browser Smoke dispatch witnesses
    -> return to CONTROL LOOP
```

## 2. 冻结的 source 与治理输入

dependency candidate 开始以前必须重新读回并精确匹配：

| coordinate | frozen value |
| --- | --- |
| maintenance ref | `refs/heads/core-0.12-maintenance` |
| maintenance base commit | `f961930ae1e69d7d88849fa2b0d40befb3e94c89 = v0.12.2^{}` |
| maintenance base tree | `e0ded371266ac80b936fcbf5e00515a75dbf0950` |
| `web/package.json` Git blob | `b38efdf88c439528a5b8af799e7ab8935037b3fc` |
| base `web/package-lock.json` Git blob | `b52f8900b3c44ec978d358a5fff9e7fb852fbf34` |
| base lock SHA-256 | `FD50366E34F3FECE0CD661A18989A6BC41217B1AD92BFD3E4C79D15002CD20D1` |
| phase-one ruleset | `24216773`，active |
| ruleset target | `refs/heads/core-0.12-maintenance` |
| bypass actors | empty |
| protected operations | deletion / non-fast-forward denied；PR required |
| required checks | none |

若 maintenance ref、base tree、package input blob 或 ruleset 任一不匹配，当前合同实例不得继续。必须保留新观察并
返回 CONTROL LOOP；不得把 drift 当成“同一 0.12 line”继续施工。

ruleset 只拥有 merge governance。它没有 required checks，因此不能证明 dependency candidate 合格；后文的 manual
dispatch runs 是独立 observation witnesses，也不得冒充 branch protection required checks 或 original PR checks。

## 3. 唯一允许的 dependency construction

从第 2 节 exact maintenance base 创建一个新的、此前未用于 #252 或其他候选的 topic identity。构造工具与输入固定为：

```text
npm version
    11.19.1

registry
    https://registry.npmjs.org

command, from web/
    npm update undici brace-expansion
        --package-lock-only
        --ignore-scripts
        --registry=https://registry.npmjs.org
```

`web/package.json` 必须保持第 2 节 blob 不变。构造完成后，working tree 只允许修改：

```text
web/package-lock.json
```

允许改变的 package-lock entries、最终值、resolved URL 与 integrity 只有：

| entry | version | resolved | integrity |
| --- | --- | --- | --- |
| `node_modules/brace-expansion` | `5.0.12` | `https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.12.tgz` | `sha512-YovQ3rzhaLMIrDjNDMkNS01tea93qhEhG5xy8f6+R0l+dw3Ki+5sCoIoI942iuLZTHWogWktgwVDhU09iNEimQ==` |
| `node_modules/editorconfig/node_modules/brace-expansion` | `2.1.7` | `https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.1.7.tgz` | `sha512-uZbew1NqdmPDTMJ8ah1y+b+9QEJrfkXFk3RcTQw3X0jW/xRUvFKsg1CfQdSYGdTbXZWExtU3J3ccxtnfw1Fi0g==` |
| `node_modules/glob/node_modules/brace-expansion` | `2.1.7` | `https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.1.7.tgz` | `sha512-uZbew1NqdmPDTMJ8ah1y+b+9QEJrfkXFk3RcTQw3X0jW/xRUvFKsg1CfQdSYGdTbXZWExtU3J3ccxtnfw1Fi0g==` |
| `node_modules/undici` | `7.30.0` | `https://registry.npmjs.org/undici/-/undici-7.30.0.tgz` | `sha512-dkrQXeHSaoamnItlYbmzG0wFYrM0ZwDxCIg0A7aKjTyyhh9svRzCNFEzV+Vm05/yehjCzjDZ31KXfGEjYSztDQ==` |

最终 lock SHA-256 必须为：

```text
6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E
```

除上述四个 entry 的 `version / resolved / integrity` 变化外，不允许新增、删除或重排其他 lock semantics。
最终 diff 预期为 `12 insertions / 12 deletions`；行数只作辅助 witness，one-file exact diff 与最终 SHA-256 才是
内容 identity。candidate bytes 与 current main lock 相同不转移 main 的 qualification authority。

## 4. Local construction / review gates

candidate commit 以前必须在 fresh dependency installation 上串行完成并保留命令、工具版本、开始/结束时间、exit code
与输出：

1. `npm 11.19.1` + frozen registry 的 fresh `npm ci --ignore-scripts`；
2. Workbench regression：14 files / 172 tests 全部 PASS；
3. lint PASS；
4. type-check + production build PASS；
5. `npm audit --audit-level=moderate` exit 0；
6. dependency tree 只解析出 `brace-expansion 5.0.12 / 2.1.7` 与 `undici 7.30.0`；
7. package-lock JSON 可解析，四个 allowed entries 的 version / resolved / integrity 精确匹配；
8. `git diff --check` PASS；
9. exact diff 只包含 `web/package-lock.json`。

`npm audit` 是带 observation time 的 registry/advisory observation，不是 lock bytes 的永久“安全证明”。必须记录 UTC
时间、registry、npm version、exit code 与摘要；后继 exact-head / exact-tip workflow 各自仍须重新观察。后来的 advisory
不能改写旧 observation，但新的失败也不能因旧 PASS 被忽略。

文档 228 保留的本机 Python 四格 `6 / 6 / 7 / 7` 与 3.10 normal `10` 个 memory-soft-stop failure 不是本合同的
local PASS。不得调大冻结预算、删测试或把 #252 的远端 Python PASS 借给 candidate。本合同以第 6 / 9 节的完整
remote dispatch workflow 作为 exact-head / exact-tip Python 与 Browser witnesses。

## 5. Candidate commit 与 PR identity

local gates 成立后只允许产生一个 one-file candidate commit。push 前后必须保存：

- fresh topic ref 名称与 exact commit SHA / tree；
- commit parent 精确等于第 2 节 maintenance base；
- `web/package-lock.json` Git blob 与 SHA-256；
- `git diff --name-status / --stat / --check` 与完整 patch；
- topic ref 的 Git 与 GitHub REST 双读回；
- source repository / owner / base repository identity。

随后打开一个 base 为 `core-0.12-maintenance` 的 PR。PR 打开后必须独立读回：

```text
state = OPEN
draft = false
base SHA = f961930ae1e69d7d88849fa2b0d40befb3e94c89
head SHA = exact candidate commit
commits = 1
changed files = 1
diff = web/package-lock.json only
```

PR review/merge authority 与 candidate qualification 分离。PR 本身不因 old workflow filters 自动产生 required checks；
下一节 manual dispatch 仍不得命名为 original PR CI。

## 6. Exact candidate-head dispatch qualification

candidate topic ref 必须保持不变，并从 GitHub Actions 产生两个新的 run identity：

### 6.1 Public CI

| field | required value |
| --- | --- |
| workflow path | `.github/workflows/ci.yml` |
| workflow name | `Public CI` |
| workflow Git blob at candidate | `c094d2cb84a2147e2b8bba1a7e76f140905d1a4d` |
| event | `workflow_dispatch` |
| run attempt | `1` |
| head branch | exact candidate topic ref |
| head SHA | exact unchanged candidate commit |
| conclusion | `success` |

完整 job denominator 必须是七项且全部成功：

```text
Python 3.10 on Windows
Python 3.13 on Windows
Wheel-only first run on Python 3.10
Wheel-only first run on Python 3.13
E3 0.2 release download acceptance
Workbench tests, lint, build, and audit
Starter PASS/FAIL golden path
```

### 6.2 Browser Smoke

| field | required value |
| --- | --- |
| workflow path | `.github/workflows/browser-smoke.yml` |
| workflow name | `Browser Smoke` |
| workflow Git blob at candidate | `413f35ad9f768eb323d0058b82bdd8eaca177be1` |
| event | `workflow_dispatch` |
| run attempt | `1` |
| head branch | exact candidate topic ref |
| head SHA | exact unchanged candidate commit |
| job denominator | `Production Workbench smoke` only |
| conclusion | `success` |

每次 dispatch 前、触发后和 run 终结后均需重新读回 topic ref；run API 的 `head_sha` 必须精确等于 candidate SHA。
必须保存 run ID / URL、workflow identity、event、head branch、head SHA、attempt、job IDs / names、status、
conclusion、created/started/completed timestamps 与可取得日志/Artifact metadata。

一个 workflow 的 PASS 不能替代另一个；相同 branch 名、最近绿色 run、schedule/push run 或 attempt > 1 均不满足本门。

## 7. Merge 前 reconciliation

两条 candidate dispatch 都成功以后，merge 前必须 fresh 读回并同时确认：

- PR 仍 OPEN、非 draft、exact head / base 未变、1 commit / 1 file；
- topic ref 仍指向 exact candidate SHA；
- one-file patch 与 final lock SHA-256 未变；
- `core-0.12-maintenance` 仍指向第 2 节 base；
- ruleset `24216773` 仍 active、无 bypass、禁止删除/non-fast-forward、要求 PR、required checks 为空；
- review threads 已解决，PR 可合入；
- candidate runs 仍为各自原始 run identity / attempt 1 / success。

若 PR head、base、diff、topic ref、maintenance tip 或 ruleset 任一漂移，当前 merge authority 失效。不得“顺手 rebase”后
借用旧 dispatch；新 exact head 必须作为新 candidate 重新经过第 4–7 节。

## 8. Protected merge identity

本合同只允许 ordinary merge commit；不得 squash 或 rebase merge。合入后必须读取并保存：

- merge commit SHA 与 tree；
- first parent = exact pre-merge maintenance tip；
- second parent = exact candidate head；
- `refs/heads/core-0.12-maintenance` = exact merge commit；
- merge tree 中 package-lock SHA-256 = 第 3 节 final hash；
- parent1..merge diff 仍只修改 `web/package-lock.json`；
- ruleset readback 与 merge API / PR terminal state。

若 base 在 merge 前移动、GitHub 产生的 commit topology 不符合上述关系、出现冲突解决字节或 merge tree 漂移，则不得
把该 tip 称为本合同的 qualified dependency prerequisite。保留写观察并返回 CONTROL LOOP。

## 9. Exact maintenance-tip dispatch qualification

merge 后不得复用第 6 节 candidate runs。必须对 `core-0.12-maintenance` 创建两条 fresh run identity，并在每次
dispatch 前后及终结后读回 maintenance ref。

两条 run 分别使用第 6 节同一 workflow path / name / Git blob / job denominator，并且必须满足：

```text
event       = workflow_dispatch
run_attempt = 1
head_branch = core-0.12-maintenance
head_sha    = exact merge commit
conclusion  = success
```

Public CI 七项 jobs 与 Browser Smoke 一项 job 必须分别全成功。maintenance ref 在两条 dispatch 之间或终结前后发生
任何移动时，旧 merge commit 的 runs 仍保留为历史 observation，但不能资格化新的 branch tip；必须停止并重新绑定
当前 exact tip。

## 10. Failure / cancellation / drift semantics

| observation | retained identity | required action |
| --- | --- | --- |
| local construction / review non-zero | `LOCAL_GATE_FAILURE` 或精确 setup/resource 分类 | 保留输出；归层后重新决定，不弱化门 |
| topic/PR head drift | old runs remain bound to old head | 新 head 重新走 candidate gates；不借用旧 PASS |
| dispatch cannot start / API error | `DISPATCH_ERROR`，root cause only if proven | 不伪造 run，不用 push/schedule run替代 |
| run `failure` | `FAILURE` | 保留 run/log/Artifact；不 rerun 洗白 |
| run `cancelled` | `CANCELLED` | 保留；不是 PASS，也不自动解释为产品失败 |
| run attempt > 1 PASS | diagnostic / non-qualifying | 不能替代所需 fresh attempt-1 run |
| job denominator missing / skipped | incomplete qualification | 不把“workflow success-like”缩成部分分母 |
| ruleset/base/merge topology drift | merge authority invalid | 停止并返回 CONTROL LOOP |
| exact-tip run head SHA != branch tip | observation belongs to another coordinate | 不资格化当前 tip |
| advisory later changes | new timed observation | 不改写旧 PASS；当前 seam 重新判断是否仍可继续 |

任何后来成功都不能删除或重新解释 #252、文档 228 的本机 resource failures 或本合同产生的首个非成功 observation。

## 11. Retained evidence 与发布权

每个阶段至少保留：

1. exact source commit/tree/blob identities 与 ref REST/Git readback；
2. ruleset JSON bytes、读取时间与关键字段 projection；
3. npm / Node version、registry、构造命令与 local gate logs；
4. base/final package-lock bytes、SHA-256、Git blob、parsed four-entry projection 与 exact patch；
5. PR REST/GraphQL bytes、diff/commits/files、head/base 与 review/mergeability readback；
6. 四条 dispatch run 的 API bytes、job lists、attempt、timestamps、conclusions、logs/Artifact metadata；
7. merge response、merge commit parents/tree、protected ref 与 post-merge ruleset readback；
8. 所有 ERROR / FAILURE / CANCELLED / setup / resource-stop identities；
9. 一份只做 reconciliation 的 canonical manifest，把 candidate 与 tip 两套 evidence 分开列出。

dependency producer、PR、workflow run 与 npm registry 都无权自行发布“qualified tip”。只有合同声明的所有 gate 对同一
exact identities 完成 reconciliation 后，才可在后继独立状态 publication 中条件化发布结果。

## 12. 闭合后的 continuation

第 9–11 节全部成立只证明：

```text
exact core-0.12-maintenance tip
    has a qualified dependency prerequisite
```

它不自动授权 workflow bootstrap。闭合后必须返回 CONTROL LOOP，重新核对 exact maintenance tip、ruleset、并行 PR、
advisory surface 与文档 223/224 的停止线。只有该复核仍支持原问题，才允许从新 tip 建立一个全新的 workflow-only
candidate；#252 永久保持关闭/未合并/失败身份，不能 reopen、rerun 或改写。

## 13. 明确禁止的扩张

本文不得被解释为授权：

- 当前就创建/push dependency topic、PR 或 dispatch runs；
- 修改 `core-0.12-maintenance`、ruleset、workflow、runtime、tests、timeouts、retry 或 budgets；
- 把 lockfile 重新塞进 workflow-only PR；
- 重开、改 head、rerun、合并或删除 #252；
- 关闭、忽略或降低 `npm audit`；
- phase-two ruleset、host-socket backport、version bump、tag、Release、asset 或 public readback；
- current main required-lane migration、public 0.13 repair 或 Starter compatibility change；
- R1 Parse implementation authorization，或修改 frozen R1 contract / Schema / publisher / Bundle。

## 14. 合同候选资格与冻结停止线

本文当前只条件化发布：

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

合同候选必须先完成 final-byte local documentation gates、original PR Public CI、受保护 main 合入、new exact-main
Public CI + Browser Smoke、fresh README / doc228 / 本文 / milestones installed-product readback 与 independent
source-byte reconciliation，才可成为 qualified contract candidate。

之后仍须使用独立 docs-only freeze publication 重新发布合同 target state。该 publication 自己的 final bytes、original
PR gates、protected merge、new exact-main dual gates、fresh installed-product readback 与 independent reconciliation
全部闭合后，合同才可标为 `FROZEN`。冻结以前不得执行第 3–12 节的任何 dependency write / dispatch 动作。

合同冻结也不自动开始实现；必须返回 CONTROL LOOP，从新的 exact main 重新确认 one-file dependency prerequisite
仍是当前最小合法问题。

停止原则为：**相同 lock bytes 可以出现在 main 与 maintenance 两个 source world 中，但构造、review、manual
dispatch、protected merge 与 exact-tip qualification 必须在 maintenance world 内重新取得；任何内容相等都不继承
authority。**
