# M10 0.12 maintenance workflow bootstrap 顺序反例审计

日期：2026-10-01

## 1. 审计结论

[文档 226](226-m10-maintenance-branch-creation-authority-correction-audit.md)形成 qualified history 后，Human
明确授权补齐 GitHub OAuth `workflow` scope。新 credential 读回包含：

```text
delete_repo
gist
read:org
repo
workflow
```

随后只进行一次新的 REST create-reference 写观察。GitHub 返回 `HTTP 201`，并独立通过 REST 与
`git ls-remote` 读回：

```text
refs/heads/core-0.12-maintenance
    = f961930ae1e69d7d88849fa2b0d40befb3e94c89
    = v0.12.2^{}
```

phase-one ruleset `24216773` 在创建前后均保持 active、无 bypass、禁止删除与 non-fast-forward、要求 PR、
required checks 为空。第一次 `HTTP 404 / UNKNOWN` 继续保持原身份；后继 `201` 不证明旧 404 的原因，也不把
旧 observation 改写成 PASS。

branch 创建以后，按[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
第 5.2 节建立 workflow-only PR #252。该候选保持精确两文件 scope，但原始 Public CI
`36771080921` attempt 1 在 Workbench `npm audit` 观察到两组 high-severity advisory，最终为 `FAILURE`。
PR #252 未 rerun、未改写 head、未合入并已关闭。

因此当前被击穿的已经不是 branch-creation authority，而是冻结的 bootstrap 顺序假设：

```text
exact v0.12.2 branch
    -> workflow-only PR
    -> green original Public CI
```

当前 maintenance lock bytes 不能通过当前 advisory database，而 workflow-only PR 没有 authority 修改这些 bytes。
在新的顺序合同取得资格以前，不能重开 #252、不能把 lockfile 塞入 workflow-only PR，也不能弱化 audit gate。

当前状态为：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CURRENT_SOURCE_EXACT_MAIN_VERIFIED
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_BOOTSTRAP_ORDERING_CORRECTION_REQUIRED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

## 2. branch 创建与治理事实

branch 创建使用与第一次 404 相同的 ref / target commit：

```text
ref = refs/heads/core-0.12-maintenance
sha = f961930ae1e69d7d88849fa2b0d40befb3e94c89
```

不同的是 credential scope 已经在写观察以前补齐并独立读回。新请求返回：

```text
HTTP 201 Created
```

当前控制面复算为：

| 字段 | 当前读回 |
| --- | --- |
| branch ref | `f961930ae1e69d7d88849fa2b0d40befb3e94c89` |
| branch tree | `e0ded371266ac80b936fcbf5e00515a75dbf0950` |
| ruleset id | `24216773` |
| enforcement | `active` |
| target | `refs/heads/core-0.12-maintenance` |
| bypass actors | empty |
| current user bypass | `never` |
| rules | deletion / non-fast-forward / pull request |
| required checks | none |

这证明 exact branch 已在 active governance 下建立。它不证明第一次 404 的内部原因，也不授予 workflow、dependency、
runtime、version、phase two、backport 或 Release authority。

## 3. workflow-only 候选与首败

PR #252 的精确坐标为：

| 坐标 | 值 |
| --- | --- |
| base | `f961930ae1e69d7d88849fa2b0d40befb3e94c89` |
| head | `fb77a5483c9d16af1311a53dba64531bc63bada8` |
| commit count | `1` |
| changed files | `.github/workflows/ci.yml`、`.github/workflows/browser-smoke.yml` |
| merge state at closure | `CLOSED / UNMERGED` |
| original Public CI | `36771080921`，attempt 1，`FAILURE` |

候选只把：

```text
.github/workflows/ci.yml
    push / pull_request += core-0.12-maintenance

.github/workflows/browser-smoke.yml
    push += core-0.12-maintenance
```

没有修改 job、step、action pin、timeout、command、runtime、version、release 或 lockfile。其 final bytes 在提交前完成：

- exact workflow-only diff、YAML/static 检查；
- CPython 3.10.6 / 3.13.13 normal / `-O` 四格，各 `347/347 PASS`；
- Browser acceptance 为 `COMPLETED / PASS`，5 checks、102 requests、0 HTTP errors，端口释放；
- `git diff --check`。

这些本地 witness 没有资格覆盖原始远端失败。

原始 run 的七个已产生 job 为：

```text
Python 3.10 on Windows                  SUCCESS
Python 3.13 on Windows                  SUCCESS
E3 0.2 release download acceptance      SUCCESS
Wheel-only first run on Python 3.10     SUCCESS
Wheel-only first run on Python 3.13     SUCCESS
Workbench tests, lint, build, and audit FAILURE
Starter PASS/FAIL golden path           SKIPPED
```

Workbench 先完成 tests、lint 与 build，随后 `npm audit --audit-level=moderate` 报告：

```text
brace-expansion  2.0.0 - 2.1.6 || 4.0.0 - 5.0.11
undici           7.0.0 - 7.29.0

2 high severity vulnerabilities
```

所以这不是 workflow filter 语法失败，也不是 runtime、Browser、Core 或 Python regression。它是当前 advisory
database 对 maintenance branch 精确 lock bytes 的真实不合格观察。

## 4. maintenance 与 main 的 dependency identity

maintenance branch 当前仍持有：

| lock entry | maintenance value |
| --- | --- |
| root `brace-expansion` | `5.0.9` |
| `editorconfig` nested `brace-expansion` | `2.1.4` |
| `glob` nested `brace-expansion` | `2.1.4` |
| `undici` | `7.29.0` |

current main 已经通过两个独立维护 PR 修正相同 advisory surface：

| maintenance | PR / merge | current-main value |
| --- | --- | --- |
| `undici` | PR #248 / `b735758bb07c76bc50bdcebf8dd56d01bd81d6df` | `7.30.0` |
| `brace-expansion` | PR #253 / `30d459197c24dabcfd28f9d50f6ed582ee029258` | root `5.0.12`，nested `2.1.7` |

PR #253 只修改 `web/package-lock.json` 的三处 transitive lock entry；原始 Public CI `36773193271`
attempt 1 为 `11/11 SUCCESS`。合入后 exact-main Public CI `36775834977` attempt 1 为 `11/11 SUCCESS`，
Browser Smoke `36775834866` attempt 1 为 `1/1 SUCCESS`。

这些事实证明 current-main lock maintenance 可以通过当前门；它们不修改 maintenance branch，也不能把 main 的
source、PR、attempt 或 exact-main qualification 借给 0.12 line。相同版本选择只是 bounded candidate evidence，
不是 maintenance backport authority。

## 5. 被击穿的最小冻结假设

文档 223 正确冻结了以下边界：

- phase-one ruleset 只允许受 PR 保护的 bootstrap；
- workflow-only PR 不得混入 runtime、version、dependency 或 release bytes；
- audit failure 不得通过扩大 timeout、删 gate 或改写结果来规避；
- workflow bootstrap 成功以前，不开始产品 backport。

但它还隐含依赖：

> exact historical branch 在只改变 workflow filters 时，仍能通过 workflow 自身的全部当前外部资格条件。

#252 反证了该前提。历史 source 没有变化，但 npm advisory database 是外部、可变化的 qualification input；因此：

```text
workflow semantics unchanged
    !=
workflow-only candidate currently qualifiable
```

这一反例不推翻文档 223 的 Browser 分类、历史谱系、phase-one governance、phase-two、M1/M2/W1 隔离。它只要求
最小重开 M0 中 “exact branch 创建以后、workflow-only PR 以前” 的 dependency qualification / ordering seam。

## 6. 当前最小问题

后继最小问题是：

> 在 phase-one ruleset 保持 active、无 bypass、无未保护窗口，且 workflow-only PR 继续保持精确两文件 scope 的
> 条件下，如何让 maintenance branch 先取得当前 Workbench dependency qualification，并为该前置变更建立不借用
> current main、也不伪造 original PR checks 的充分远端/本地 witness？

当前可见的候选机制包括：

1. 在 workflow-only PR 以前增加独立、lockfile-only maintenance prerequisite PR；
2. 利用旧 workflow 已有的 `workflow_dispatch`，对 exact topic / maintenance ref 取得远端 observation；
3. 只使用冻结合同原有的强本地 final-byte witness；
4. 把 dependency 与 workflow filters 合并在同一 PR；
5. 降低、忽略或删除 `npm audit` gate。

本文不选择任何路线。第 4 项会破坏 workflow-only scope；第 5 项会弱化既有 gate，应保持禁止。第 1–3 项仍需
分别审计：谁拥有 dependency version selection、exact head / exact tip 如何绑定、`workflow_dispatch` 是否提供足够的
candidate identity、合入前后需要哪些门、以及 phase-one 能否承载这类非产品语义的 lock maintenance。

特别是，main 上的 `7.30.0 / 5.0.12 / 2.1.7` 不能直接成为 maintenance 结论。只有新的最小合同明确 source、
scope、验证、merge 与 exact-tip 资格后，这些版本才可作为候选输入被重新验证。

## 7. 明确未授权

本文不授权：

- 重开、rerun、更新或合入 PR #252；
- 直接修改 `core-0.12-maintenance`；
- 创建 dependency topic branch 或 lockfile PR；
- 运行 `workflow_dispatch` 或把本地 witness 写成远端 PASS；
- 把 dependency bytes 加入 workflow-only PR；
- 修改、disable、evaluate 或升级 ruleset `24216773`；
- 弱化 `npm audit`、改 audit level、忽略 advisory 或扩大 timeout；
- 开始 phase two、Browser classification backport、`0.12.3` version/release、Starter consumer migration；
- 修改 Parse / Fact / Coverage 或重发 Parse private implementation authorization。

## 8. 本审计的资格与停止线

本文只保存 branch-creation 后继事实、#252 原始失败、current-main dependency maintenance 与被击穿的顺序前提。
它不修改文档 223/224/225/226、ruleset、maintenance branch、runtime、tests、workflow、dependency、version、tag、
Release、asset、Schema 或 frozen R1 合同。

本文与 README、AGENTS、milestones 的最终字节须完成适用 Markdown/Schema 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff 与 `git diff --check`。然后仍须经过本文自己的 original PR 门、
受保护 main 合入与 new exact-main 双门。只有这些门闭合，本问题边界才成为 qualified history；它仍不自动授权
dependency prerequisite contract 或任何 maintenance source 写入。

当前 final-byte candidate 已完成：

- CPython 3.10.6 / 3.13.13 normal / `-O` 四格，各 `48/48 PASS`；
- exact 四文件 scope，文档 223–226 保持 HEAD 原字节；
- UTF-8 without BOM、LF/final LF、balanced fences、relative links、状态 marker 与敏感路径检查；
- `git diff --cached --check`。

停止原则为：**branch authority 已经闭合，但 workflow-only first 的顺序已被真实 advisory observation 击穿。
先冻结 dependency prerequisite 的最小 authority 与资格链，再以全新 identity 重做 workflow-only bootstrap；不得把
依赖修复、workflow 迁移和产品 backport 揉成一次“顺手修好”。**
