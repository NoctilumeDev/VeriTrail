# R1 Public CI Review Attention topology containment maintenance

> 日期：2026-11-15  
> 状态：`MAINTENANCE_CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`  
> exact base：`272d581cd8fb5e652ee6cd5d1077c45aaf1d442d`  
> base tree：`4afa14e2364ace0d4740278383686bf901e5eeb4`  
> 影响：`L1_CI_TEST_TOPOLOGY_ONLY`。本文与同一candidate中的workflow patch只重建Public CI如何承载既有
> Review Attention full-suite oracle；不修改runtime、tests、Schema、合同、产品timeout、public Review或Core Verdict。

## 1. CONTROL LOOP 输入不是“再加一次时间”

[文档407](407-r1-same-attempt-continuity-original-public-ci-timeout-failure-boundary-audit.md)已经以PR #466自己的完整资格链成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`：

```text
candidate base / head / tree = a41b8ba... / 04c2a25... / 4afa14e...
original Public CI           = 43614699493 / attempt 1 / 11 of 11 SUCCESS
protected merge              = 272d581cd8fb5e652ee6cd5d1077c45aaf1d442d
exact-main Public CI         = 43618842277 / attempt 1 / 11 of 11 SUCCESS
exact-main Browser Smoke     = 43618842284 / attempt 1 / 1 of 1 SUCCESS
fresh reconciliation         = d0483ec482252357e682a986d44c561e99fd8e85f1882a6edf3374b7c74ba309
116-artifact closeout        = bd62d911997b28a40c64d136ab1bf550c8cf5847f256a6b8dc39c4076a8aba42
finite integrity             = 1e8671cd8799306925224fa2abcdce8f92908b97a3b46a5034f8de6c9451c7ed
```

这只资格化失败边界。PR #465的Python 3.10 job仍是`CANCELLED`，lower slowdown cause仍是`UNKNOWN`，doc405仍是
`MERGED / PUBLIC_CI_PASS / BROWSER_SMOKE_FAILED / NOT_QUALIFIED / NOT_FROZEN`。本文不回填这些身份。

当前真正被反例击穿的前提是：一个固定上限的Windows job可以长期串行承载全部Core、entry/plugin、两个完整Review Attention模式、
发行下载、构建和artifact发布，同时始终为hosted-runner variance保留恢复余量。workflow历史已经多次只扩大同一aggregate budget：

| commit | 变化 |
| --- | --- |
| `2b51cb607588bf220e19cf23715210324584d028` | 15 -> 20分钟 |
| `9e0a032699ccf298e5e556a3f10f2cf824d5932f` | 20 -> 25分钟 |
| `48b2f0c308959a447beb2fb7de529b3b4c5fd640` | 25 -> 30分钟 |
| `113862ec60027b537c6c86855477098719facd98` | 30 -> 35分钟 |
| `00754c2890b6aeabce0720ecf157d8f5ab3b550a` / successor | 35 -> 45分钟 |
| `50586d3917373acda0f607892f7dd7929e22ff1f` | 45 -> 55分钟 |

PR #465在55分钟再次触顶后，继续把55替换成另一个任意数字只是在保留已失败的模型。理论遇到反例时，本轮先检查前提，不把新上限当作
下层性能根因或长期正确性的证明。

## 2. 事实分层与不允许的推断

PR #465建立：

```text
configured 55-minute aggregate timeout reached = ESTABLISHED
normal Review Attention 1463s / SUCCESS          = ESTABLISHED
optimized Review Attention 1451s / CANCELLED     = ESTABLISHED
lower slowdown cause                              = UNKNOWN
candidate product regression                      = NOT_ESTABLISHED
cancelled step product result                      = NOT_ESTABLISHED
```

PR #466与其exact-main gate提供的新world成功时长，包括最慢已观察成功Python 3.10 aggregate job 2819秒；它距55分钟只剩481秒。后继
成功证明相同bytes有时可以在旧预算内完成，不恢复“始终保留恢复余量”的前提，也不覆盖PR #465。

因此本文不：

1. 删减normal或`-O`；
2. 缩小test discovery root、改test bytes、改变fail-fast或接受部分PASS；
3. 通过并发运行两个完整suite于同一runner来把资源竞争隐藏成优化；
4. 修改产品内层budget或timeout；
5. 修改branch ruleset、required check名字或把新非required job当作独立保护；
6. 宣称结构维护定位了lower slowdown cause。

## 3. 当前保护面与 skipped-check 风险

2026-11-15的authenticated GitHub ruleset readback显示，active main ruleset `21436452`与0.12 maintenance ruleset `24216773`都要求：

```text
Python 3.10 on Windows
Python 3.13 on Windows
Wheel-only first run on Python 3.10
Wheel-only first run on Python 3.13
E3 0.2 release download acceptance
Workbench tests, lint, build, and audit
Starter PASS/FAIL golden path
```

Review Attention尚无独立required context。GitHub官方说明：依赖失败而被条件跳过的required job可能以`skipped`报告并不阻止合并；需要用
[`always()`与显式结果检查](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks)
让required job真实运行并失败。只添加`needs`而允许既有Python required checks被跳过，不是fail-closed方案。

## 4. 最小结构维护

本candidate执行一个拓扑修正：

```text
Review Attention 3.10 normal     --\
Review Attention 3.10 optimized  ----> existing required Python 3.10 / 3.13 barriers
Review Attention 3.13 normal     ----> remaining product/release gates + artifact producers
Review Attention 3.13 optimized  --/
```

机械边界如下：

1. 新`review-attention` matrix有Python 3.10/3.13 × normal/optimized四个独立Windows cells；
2. 每个cell继续运行原命令的精确语义：`python`或`python -O`加同一`unittest discover` root；
3. 每个cell在fresh checkout与editable exact candidate上运行，安装既有Core schema/browser/Windows能力及Review Attention Windows budget能力；
4. 每个cell拥有45分钟outer containment budget；已观察最慢单mode 1463秒，与旧aggregate的两个mode串行相分离；
5. 既有`python` job删除那两个重复命令，但保留所有其他tests、release acceptance、build与artifact producers；
6. 既有required check display names保持逐字节不变，ruleset不修改；
7. 既有`python` job使用`needs: [review-attention]`与job-level `always()`，第一步机械要求
   `needs.review-attention.result == success`；failure/cancelled/skipped均使required Python contexts真实FAIL，而不是被跳过；
8. wheel-only、GitHub Evidence wheel-only、Acceptance Core与Starter下游仍依赖既有`python` job，因此artifact与保护关系不漂移；
9. 55分钟只继续约束移除Review Attention后的其余Python product/release lane，不被提高，也不解释PR #465。

该结构把“完整oracle是否通过”与“所有测试必须挤进同一累计墙钟”分开。它没有让测试变少，只让两个长mode不再共享同一aggregate deadline。

## 5. 精确范围

本candidate只允许：

```text
.github/workflows/ci.yml
README.md
AGENTS.md
docs/408-r1-public-ci-review-attention-topology-containment-maintenance.md
docs/milestones.md
```

所有runtime/test bytes、fixtures、Schema、doc397、doc405、doc407、`docs/project-state.md`与primary `audit.json`必须保持base bytes。GitHub
ruleset也不得在本candidate中修改。

## 6. Local qualification

final bytes必须证明：

- exact five-file scope、UTF-8/LF/final-LF、links/fences/headings与`git diff --check`；
- workflow可解析，只有一个full Review Attention discovery command，matrix精确为四个Python/mode cells；
- 既有两个required Python display names、所有其他job names、下游`needs`与artifact producer/consumer names不漂移；
- `always()`加显式success assertion存在，不能由dependency skip冒充required PASS；
- runtime/test bytes相对base完全不变；
- Python 3.10.6/3.13.13 × normal/`-O`的focused same-attempt continuity witness全部PASS；
- global/local hygiene、remote main与primary audit continuity PASS；
- doc407 closeout、PR #465 retained failure与ruleset snapshot可复算。

本地PASS只证明final candidate bytes可送原始远端门，不自行冻结maintenance。

## 7. Qualification pipeline

```text
final five-file maintenance bytes / declared local gates
    -> original PR Public CI: 15 of 15 jobs, including four isolated Review Attention cells
    -> existing seven required contexts PASS; no ruleset mutation
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc407 / 本文 / milestones readback
    -> fresh anonymous exact-commit AGENTS / workflow raw-byte observation
    -> independent topology / ruleset / PR465 retained-history reconciliation
    -> finite closeout
    -> CI_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN at most
    -> return CONTROL LOOP
```

任何non-success保留自己的attempt与原始身份，不rerun。后继PASS不能回填PR #465或PR #464 Browser setup failure。

## 8. 状态上限与后继停止线

在本文自己的全部最后门闭合以前，只允许：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_PR464_MERGED_EXACT_MAIN_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_EXACT_MAIN_BROWSER_FAILURE_BOUNDARY_AUDIT_PR465_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_TIMEOUT_CANCELLED_NOT_QUALIFIED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_ORIGINAL_PUBLIC_CI_TIMEOUT_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门成立后，只把本maintenance升级为`R1_PUBLIC_CI_REVIEW_ATTENTION_TOPOLOGY_CONTAINMENT_MAINTENANCE_FROZEN`。doc405仍不因此
`QUALIFIED`或`FROZEN`；fresh CONTROL LOOP必须从新的exact main独立重建doc406 failure-boundary recovery。本文不授权manifest、public
Review、R2–R6或global composition。`local_not_global = true`与`post_r1_global_check_required = true`继续成立。
