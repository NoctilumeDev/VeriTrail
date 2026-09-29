# M10 0.12 maintenance bootstrap 治理反例审计

日期：2026-09-30

## 1. 审计结论

[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)的 C1 已经完成自己的
original PR、受保护 main 合入与 new exact-main 双门。current source 因而已经包含精确
`net::ERR_NO_BUFFER_SPACE` 分类修正；这不发布新的 Core wheel，也不改写 public `v0.13.0`。

M0 随后按冻结顺序创建 phase-one ruleset，再尝试从精确 `v0.12.2^{}` 创建
`core-0.12-maintenance`。ruleset 创建与读回成功，但第一次真实 Git reference 创建返回 HTTP 404，branch
保持不存在。该观察命中文档 223 第 5.2 节预注册的
`MAINTENANCE_BOOTSTRAP_CONTRACT_COUNTEREXAMPLE`：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CURRENT_SOURCE_EXACT_MAIN_VERIFIED
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_NOT_CREATED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

精确拒绝原因保持 `UNKNOWN`。本审计不把 REST 404 单独解释为 GitHub ruleset 的确定错误，也不把后继
`git push --dry-run` 的可行输出升级为真实 branch-creation PASS。

## 2. C1 current-main 资格

| 坐标 | 值 |
| --- | --- |
| C1 base | `b735758bb07c76bc50bdcebf8dd56d01bd81d6df` |
| C1 head | `6fec13def5b0e8f66362fbd7b81f191be8e48110` |
| C1 PR | [#249](https://github.com/NoctilumeDev/VeriTrail/pull/249) |
| C1 original Public CI | `36637526486`，attempt 1，`11/11 SUCCESS` |
| C1 merge / exact main | `2daf6eaefa20b0bf3f371eed50e74f3d863496b3` |
| exact-main tree | `edb39f90306c85299094442c5d9a5dd410f53b41` |
| exact-main Public CI | `36639973530`，attempt 1，`11/11 SUCCESS` |
| exact-main Browser Smoke | `36639973548`，attempt 1，`1/1 SUCCESS` |

C1 只修改 `src/veritrail/browser.py`、`src/veritrail/verdict.py` 与三个对应测试文件。它保持 raw Network
failure，增加精确 private collector projection，并只在 raw fact 与 collector projection 互相印证、没有混入其他
collection error 时，把 Browser success assertions 投影为 `NOT_EVALUATED`；cleanup assertion 继续适用。真实
business/selector failure 仍为 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`，没有扩大 timeout、retry、版本、
Starter compatibility 或 Parse authority。

候选阶段首次完整 lifecycle 回归曾得到 `COLLECTOR_ERROR / ERROR / FAIL`：三个 Browser HARD assertions
仍在错误地评价 collection-error world。该反例推动了 applicability 修正；它继续保留，后继 PASS 不把它写成
未发生。其余 import path、invalid Evidence fixture、PowerShell ref 转义与 attachment identity 超限均保持各自的
setup / external-artifact 身份，不冒充产品失败。

## 3. phase-one ruleset 事实

创建前只读核账确认：

```text
annotated tag object = 2177bb2cc02d9ef9068e7b7132983c5edb82be6c
v0.12.2^{}          = f961930ae1e69d7d88849fa2b0d40befb3e94c89
target branch        = absent
target ruleset       = absent
```

随后创建并独立读回：

| 字段 | 读回值 |
| --- | --- |
| ruleset id | `24216773` |
| name | `Protect Core 0.12 maintenance branch` |
| target | `branch` / `refs/heads/core-0.12-maintenance` |
| enforcement | `active` |
| bypass | empty，`current_user_can_bypass = never` |
| deletion | denied |
| non-fast-forward | denied |
| pull request | required |
| required status checks | none |

该 ruleset 当前继续保持 active。保留它不创建 source branch，也不授予 phase two、workflow、runtime、version、
backport 或 release 权力。

## 4. branch 创建首败与归因边界

第一次真实 branch 创建使用 GitHub REST `POST /repos/NoctilumeDev/VeriTrail/git/refs`，请求的 ref 与 SHA 为：

```text
ref = refs/heads/core-0.12-maintenance
sha = f961930ae1e69d7d88849fa2b0d40befb3e94c89
```

GitHub 返回：

```text
HTTP 404
message = Not Found
```

后继只读归因确认：

- 同一凭据可以读取现有 `refs/heads/main`，并拥有仓库 `admin/push` 权限；
- classic token 具有 `repo` scope；
- phase-one ruleset 仍为 active 且无 bypass；
- Git API `matching-refs/heads/core-0.12-maintenance` 返回空数组；
- `git ls-remote --heads` 也没有该 branch；
- exact peeled commit 仍可从 current main 到达；
- `git push --dry-run` 只证明 refspec 与对象可构造，不执行远端 ref 更新，也不能证明 ruleset 会接受真实 push。

因此已确定的是“真实 REST branch creation 没有成立”；尚未确定的是 GitHub 为什么用 404 拒绝。不得把
`UNKNOWN` 擅自改写成 token 缺权、ruleset bug、临时网络错误或产品错误。

## 5. 最小重开问题

冻结合同原先假设：active phase-one PR ruleset 可以先存在，然后 exact branch ref 可以在无 bypass、无未保护窗口的
条件下创建。当前观察击穿的只有这个治理可行性假设。

官方 GitHub ruleset 文档还提供 `do_not_enforce_on_create`，用于允许 branch creation 避免 required-check 自锁；
但它属于什么 rule、能否与本合同的 PR rule 共同形成无 bypass 的精确一次性 bootstrap、以及更新现有 ruleset 后
哪一种 readback 足以证明没有扩大权限，目前都未冻结。它只是待审候选，不是现场修复许可证。

后继最小问题是：

> 如何在 branch 建立前保持 active governance，同时只允许精确 `v0.12.2^{}` 创建
> `core-0.12-maintenance`，并在无 bypass、无未保护窗口、无产品代码 direct push 的条件下进入
> workflow-only PR？

在该问题形成新合同并取得自己的资格以前，禁止：

- 实际 `git push` 作为第二条 branch 创建路径；
- disable、evaluate 或删除 ruleset `24216773`；
- 增加 bypass actor；
- 先创建未保护 branch，再补 ruleset；
- 创建 workflow-only PR、phase-two ruleset 或产品 backport；
- 修改 runtime、version、tag、Release、asset、Starter consumer 或 Parse 状态。

## 6. 本审计的资格与停止线

本文只保存已经发生的控制面事实、失败身份和最小问题边界。它不修改文档 223/224、runtime、tests、workflow、
version、branch、ruleset、tag、Release、asset、Schema 或 frozen R1 合同。

本文与 README、AGENTS、milestones 的最终字节须完成适用 Markdown/Schema 四格、relative links、UTF-8、
fence/heading、状态 marker、敏感路径、exact diff 与 `git diff --check`。然后仍须经过本文自己的 original PR 门、
受保护 main 合入与 new exact-main 双门。只有这些门闭合，审计状态才成为 qualified history；它仍不自动授权
下一份治理合同或任何控制面修改。

冻结原则为：**治理设施可以先于 source branch 存在，但第一次真实 ref 创建失败以后，不能用另一条写路径把
预注册反例变成“其实可行”。先保存失败，再重新证明一条无 bypass、无未保护窗口的创建语义。**
