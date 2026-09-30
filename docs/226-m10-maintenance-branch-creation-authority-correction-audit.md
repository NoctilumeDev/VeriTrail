# M10 0.12 maintenance branch 创建 authority 更正审计

日期：2026-09-30

## 1. 更正结论

[文档 225](225-m10-maintenance-bootstrap-governance-counterexample-audit.md)保存的现场观察继续成立：

```text
phase-one ruleset 24216773
    = active / no bypass / PR required

first REST create-reference observation
    = HTTP 404 / Not Found

refs/heads/core-0.12-maintenance
    = absent
```

但文档 225 形成 qualified history 后，后继只读核账发现：执行第一次创建请求的 GitHub OAuth token 没有
`workflow` scope，而目标 `v0.12.2^{}` 所含旧 `.github/workflows/ci.yml` 在任何当前远端 branch tip 上都没有
同路径、同内容副本。GitHub 官方 OAuth 文档明确把 `workflow` scope 定义为新增或更新 GitHub Actions workflow
文件所需能力，并且只在相同路径、相同内容已存在于另一 branch 时给出免该 scope 的例外。

因此，第一次 404 发生时，branch-creation credential authority 并未取得资格。当前证据没有资格把该 404
归因为 phase-one ruleset / governance 语义反例，也没有资格继续声称“明显 token scope 缺失已经排除”。

精确根因仍为 `UNKNOWN`：

```text
observed REST 404
    = preserved

missing workflow scope
+ old ci.yml has no same-path/same-content branch-tip copy
    = material unqualified precondition

missing workflow scope caused this exact 404
    = NOT PROVEN

phase-one ruleset rejected exact branch creation
    = NOT PROVEN
```

当前状态更正为：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CURRENT_SOURCE_EXACT_MAIN_VERIFIED
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_NOT_CREATED
M0_BRANCH_CREATION_AUTHORITY_UNQUALIFIED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

`M0_MAINTENANCE_BOOTSTRAP_BLOCKED` 仍是操作状态；它现在表示 branch 尚未创建且合法创建权未资格化，不再表示
ruleset-specific governance counterexample 已成立。

## 2. 被保留的历史身份

文档 225 已经完成自己的资格链：

| 坐标 | 值 |
| --- | --- |
| PR | [#250](https://github.com/NoctilumeDev/VeriTrail/pull/250) |
| candidate head | `7cd2533255e59aac12fe91520c9fa64a1dc9f918` |
| original Public CI | `36643281071`，attempt 1，`11/11 SUCCESS` |
| merge / exact main | `bbf019f983677650ac28237d70a6218d6448d866` |
| exact-main tree | `889e3652481a18c42484b726b9f731a74fcf525f` |
| exact-main Public CI | `36645504643`，attempt 1，`11/11 SUCCESS` |
| exact-main Browser Smoke | `36645504461`，attempt 1，`1/1 SUCCESS` |

这些门证明文档 225 的字节和当时的审计判断成为 qualified history；它们不保证后继不会发现击穿该判断前提的
新证据。本文不改写、删除或回填文档 225，也不把第一次 REST 404 重分类为“没有发生”。

更正只作用于 404 的归因强度：

```text
old qualified claim
    active ruleset + REST 404
    -> preregistered governance counterexample

new evidence
    credential lacks workflow scope
    + documented exception fails for old ci.yml

corrected claim
    active ruleset + REST 404 + absent branch
    -> branch creation failed under an unqualified credential precondition
```

## 3. credential scope 只读核账

第一次 branch-creation 使用的当前 GitHub CLI OAuth credential 读回 scope 为：

```text
delete_repo
gist
read:org
repo
```

其中没有 `workflow`。`repo` 能解释 repository `admin/push` 和 ordinary contents write，但 GitHub 官方 OAuth
scope 文档单独定义了 `workflow`：它授予新增、更新 GitHub Actions workflow 文件的能力。只有当同一路径、同一
内容已经存在于该 repository 的另一 branch 时，workflow 文件才可以在没有该 scope 的情况下提交。

官方 REST create-reference 文档同时把 fine-grained credential 的适用权限列为：

```text
Contents: write

or

Contents: write + Workflows: write
```

该文档为成功创建列出的状态是 `201`，并列出 `409` / `422`；它没有为 Create a reference 列出 `404`。
这进一步说明 404 不能仅凭状态码被解释成已命中冻结的 ruleset 拒绝语义，但仍不足以独立证明 GitHub 实际采用的
内部拒绝原因。

参考：

- [GitHub OAuth app scopes](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps)
- [GitHub REST API: Create a reference](https://docs.github.com/en/rest/git/refs#create-a-reference)

## 4. 同路径、同内容例外复算

从精确 maintenance base：

```text
v0.12.2^{} = f961930ae1e69d7d88849fa2b0d40befb3e94c89
```

读取两个 workflow blob，并与当前所有 `refs/remotes/origin/*` branch tip 的同路径 blob 比较：

| path | v0.12.2 blob | 当前 branch-tip 同内容数 |
| --- | --- | ---: |
| `.github/workflows/ci.yml` | `c094d2cb84a2147e2b8bba1a7e76f140905d1a4d` | `0` |
| `.github/workflows/browser-smoke.yml` | `413f35ad9f768eb323d0058b82bdd8eaca177be1` | `11` |

例外要求目标 branch 中的 workflow 文件都满足同路径、同内容条件；旧 `ci.yml` 的计数为零，已经足以证明该例外
不能覆盖这次 exact ref creation。`browser-smoke.yml` 的匹配不能替代 `ci.yml` 的缺失。

该复算只说明 credential prerequisite 没有闭合，不把 branch tip 列表、Git object equality 或 OAuth 文档升级为对
GitHub 内部鉴权路径的证明。

## 5. ruleset 与 branch 当前事实

本文施工前重新只读读取控制面：

```text
ruleset id                     = 24216773
enforcement                    = active
target                         = refs/heads/core-0.12-maintenance
bypass actors                  = []
current_user_can_bypass        = never
rules                          = deletion / non-fast-forward / pull request
required status checks         = none
matching maintenance refs      = []
```

所以 ruleset 已存在、branch 不存在仍然成立。本文没有修改 ruleset，也没有创建 branch。

文档 225 曾把 `do_not_enforce_on_create` 作为待审候选。官方 rules API 把该字段放在
`required_status_checks` / `workflows` rule 的参数中；当前 phase-one ruleset 没有这两类 rule。它不能修复未资格化的
OAuth workflow authority，也不是当前下一步。

参考：[GitHub REST API: Rules](https://docs.github.com/en/rest/repos/rules)

## 6. 当前最小问题

当前问题不是“怎样绕过 ruleset 创建 branch”，而是：

> 在任何新的写观察以前，怎样取得并独立读回足以携带目标 workflow bytes 的 credential authority，然后在
> phase-one ruleset 保持 active、无 bypass、无未保护窗口的条件下，对同一个 exact ref creation 做一次新的、
> 独立身份观察？

本文只把该问题登记为下一次 CONTROL LOOP 的候选，不授权解决方案。特别是，本文不授权：

- 运行 `gh auth refresh` 或扩大 OAuth scope；
- 重试 REST create-reference；
- 改用实际 `git push`；
- disable、evaluate、删除或修改 ruleset `24216773`；
- 增加 bypass actor；
- 先创建未保护 branch；
- 创建 workflow-only PR、phase two ruleset、0.12.3 backport 或 Release；
- 修改 runtime、tests、workflow、version、Starter consumer 或 Parse 状态。

如果 credential scope 扩张以后再次观察，必须使用新身份并同时保留第一次 404。后继成功不能证明第一次失败的
根因，也不能把第一次观察改写成 ruleset PASS / FAIL。

## 7. 本审计的资格与停止线

本文只追加更正历史、同步当前 project projection，并收回过强归因。它不修改文档 223/224/225、ruleset、branch、
runtime、tests、workflow、version、tag、Release、asset、Schema 或 frozen R1 合同。

本文与 README、AGENTS、milestones 的最终字节须完成适用 Markdown/Schema 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff 与 `git diff --check`。然后仍须经过本文自己的 original PR 门、
受保护 main 合入与 new exact-main 双门。只有这些门闭合，更正状态才成为 qualified history；它仍不自动授权
credential scope 扩张或新的 ref creation。

停止原则为：**先前 404 是事实，但“它证明了 ruleset/governance 反例”不再有资格成立。先补齐 credential
authority，再决定是否进行一项新的写观察；在此以前，所有控制面保持不变。**
