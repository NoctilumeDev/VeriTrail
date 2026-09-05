# P1 Structured GitHub API Collector 施工合同 0.1

> 状态：`P1_CONTRACT_CANDIDATE / IMPLEMENTATION_NOT_STARTED`
>
> 精确主线基线：`d693f9eb5bdc899d3cb3a5bdd99792e60d2c7617`
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM`
>
> 本页只冻结 P1 的施工与验收边界；没有 Collector、网络 probe、插件版本、标签或 Release

## 1. 本轮裁决

PC2 已冻结通用 `AcceptancePlan -> Evidence -> AcceptanceBundle` 语义，因此 P0 的 Core 兼容阻断已经
关闭。P1 可以进入施工合同阶段，但实现仍须停在本合同之后：先把唯一纵向切片、包边界、网络预算、
身份模型、错误语义和验收矩阵冻结，再创建插件代码。

P1 只回答一个问题：

> 能否从 sealed AcceptancePlan 机械派生一个有界、只读的 GitHub REST 观察请求，并把结构化平台事实
> 规范化为 Core 可独立读取和裁决的标准 Evidence？

它不回答公开网页最终渲染是否正确，不负责替 Core 给出 Verdict，也不发布插件。

## 2. 分层与唯一所有权

```text
sealed AcceptancePlan
        │  owns expectations and applicable observations
        ▼
Plan-to-request derivation 0.1
        │  derives coordinates, never invents expected values
        ▼
GitHub Observation Request 0.1
        │  binds spec + plan + policy, does not prove collection happened
        ▼
Collection Session
        │  owns one bounded serial execution and probe provenance
        ▼
GitHub REST Collector
        │  observes and normalizes, never judges
        ▼
Evidence 0.1 · platform.github.api.snapshot
        │
        ▼
VeriTrail Acceptance Core
             owns binding, rule evaluation and Verdict derivation
```

| 对象 | 唯一权威 | 明确不得拥有 |
| --- | --- | --- |
| sealed AcceptancePlan | 期望值、required set、观察规格与 Seal 决定 | 采集结果、GitHub 平台状态 |
| derivation contract | Plan 字段到 request 字段的机械映射 | 新期望、自由文本推断、网络行为 |
| Collector Policy | 超时、分页、重试、API 版本和资源上限 | 验收条件、通过/失败规则 |
| request | “去哪里看、看什么”的可重放声明 | `expected.*`、采集成功声明、事实身份 |
| collection session | 一次实际执行及其 probe 顺序/窗口 | 事实语义、可信时间、跨次观察合并 |
| Collector | HTTP 观察、解析、规范化与来源记录 | Verdict、Plan 改写、平台写操作 |
| Acceptance Core | Evidence 绑定、完整性/充分性/断言与 Verdict | GitHub 私有语义、网络调用 |

必须保持：

```text
Same Fact != Same Observation != Same Request
Fact Identity != Evidence Artifact Identity != Execution Identity
```

## 3. 包与依赖边界

P1 实现只能新增独立包：

```text
plugins/github-evidence/
  pyproject.toml
  src/veritrail_github/
  tests/
  examples/
```

允许依赖：

- Python 标准库；
- VeriTrail 已公开的 AcceptancePlan canonicalization、seal 验证和 Evidence 0.1 合同；
- 测试中的内存 transport / fixture server；
- 实际采集中的 `https://api.github.com`。

禁止：

- 把插件放进 `src/veritrail`；
- Core 导入 `veritrail_github`；
- 插件导入以下划线开头的 Core 私有符号或复制 Core validator；
- monkey-patch、动态覆盖 Core 行为或把 GitHub 条件塞进 Core；
- Workbench、Starter、Authoring Skill、既有 M/E 轨代码为 P1 改语义；
- 浏览器、GraphQL、GitHub Enterprise、自定义 host、webhook、定时器、组织全量扫描；
- POST、PUT、PATCH、DELETE 或任何平台修复、合并、发布、部署动作。

插件卸载后，既有 Core、旧 Bundle 和已经落盘的标准 Evidence 必须仍可验证、读取与拒绝未知输入。

## 4. Plan-to-request derivation 0.1

P1 只接受已由 Core 公共 validator 验证、且 seal 可重算一致的 `AcceptancePlan 0.1`。适用的
`observation_specs[]` 必须声明：

```json
{
  "contract": {"id": "github-observation-request", "version": "0.1"},
  "evidence_type": "platform.github.api.snapshot",
  "coordinates": {},
  "projections": [],
  "canonicalization_profile": "veritrail-json-c14n/1"
}
```

### 4.1 坐标

`coordinates` 的 P1 允许集为：

| 字段 | 必需性 | 语义 |
| --- | --- | --- |
| `owner` | 必需 | 精确 GitHub owner；不接受通配符 |
| `repository` | 必需 | 精确 repository；不接受 `.git` URL 或任意 host |
| `target_commit_sha` | 必需 | 40 位小写 commit SHA；不得用 branch/tag 名代替 |
| `pull_request_number` | 投影需要时必需 | 与目标提交关联的精确 PR 编号 |
| `release_tag` | 投影需要时必需 | 精确 tag 名；必须继续解引用，不能只信 `target_commitish` |
| `branch` | 可选 | 显式目标分支；缺省时只能使用 repository 返回的 default branch |

坐标不得包含 token、URL、文件路径、`expected.*`、自由文本 Shell、组织级范围或任何验收布尔值。

### 4.2 投影

`projections` 是去重、有序无关的能力集合；P1 允许：

```text
repository.identity
repository.default_branch
commit.identity
pull_request.merge
rules.required_checks
checks.observed_runs
release.identity
release.assets
tag.peeled_commit
pages.metadata
```

derivation 必须：

1. 从实际 sealed Plan 重新计算 `plan_digest`；
2. 从 observation spec 精确计算 `observation_spec_digest`；
3. 对投影进行词典序规范化后生成 request；
4. 拒绝未知字段、未知投影、缺少条件坐标和与 Plan 不同的复制值；
5. 在任何网络 I/O 之前完成以上步骤。

两个 Plan revision 若机械派生出相同 observation spec，spec identity 可以相同；Plan binding 与 request
identity 仍必须不同。Plan 是唯一期望权威，request 绝不复制独立的验收答案。

## 5. Request、Policy 与摘要

### 5.1 GitHub Observation Request 0.1

request envelope 最少包含：

```text
schema_version
request_id
plan_digest
derivation_contract { id, version }
observation_spec
observation_spec_digest
collector_policy
collector_policy_digest
canonicalization_profile
seal { algorithm, digest }
```

`request_id` 标识请求实例；`seal.digest` 摘要排除 `seal` 的整个 envelope。修改 request ID、Plan binding
或 Policy 都会产生新的 request seal，但不得因此改变 observation spec 或 fact identity。

### 5.2 Collector Policy 0.1

P1 默认 Policy 冻结为：

| 字段 | 值 |
| --- | --- |
| API origin | `https://api.github.com` |
| API version | `2026-03-10` |
| Accept | `application/vnd.github+json` |
| User-Agent | `veritrail-github-evidence/0.1` |
| conditional GET | 禁用；不发送 `If-None-Match` / `If-Modified-Since` |
| execution | 严格串行；并发数 `1` |
| `per_page` | `100` |
| `max_pages_per_probe` | `5` |
| `max_total_requests` | `24` |
| `connect_timeout_ms` | `5000` |
| `read_timeout_ms` | `15000` |
| `total_collection_timeout_ms` | `60000` |
| `max_attempts_per_request` | `3` |
| retry schedule | `1000 ms`、`3000 ms`；平台 `Retry-After` 优先但不得突破总窗口 |
| redirects | 只跟随最终仍为 `https://api.github.com` 的有限重定向 |

GitHub 当前要求显式 `X-GitHub-Api-Version`，并建议 `application/vnd.github+json`；版本变化属于 Policy
和 provenance，只有规范化含义变化才升级 `normalization_semantics_version`。GitHub 也建议串行请求、
遵守 `Retry-After` / rate-limit headers，并通过 `Link` header 分页。因此实现不能自行扩大并发、无限等待
或猜测下一页。参考：[API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)、
[REST best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)、
[pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) 与
[rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)。

### 5.3 四种身份

```text
observation_spec_digest
  = canonical(spec contract + evidence type + coordinates + sorted projections + profile)

collector_policy_digest
  = canonical(policy 0.1)

facts_digest
  = canonical(observation_spec_digest + normalization_semantics_version + normalized facts)

Evidence artifact SHA-256
  = canonical(whole Evidence document)
```

`facts_digest` 不得包含 request ID、Plan digest、collection session、墙钟时间、timeout/retry、access mode、
API/client/parser 实现版本或 ETag。后者属于具体 Evidence 的 provenance，因此两次独立采集可得到相同
`facts_digest` 和不同 Evidence SHA-256。

所有摘要只允许 `veritrail-json-c14n/1` 支持的 string、boolean、null、integer、array 和 object。未知
profile、float、NaN、无穷或摘要测试向量不匹配，必须在联网前拒绝。

## 6. 只读访问与秘密边界

P1 默认 `ANONYMOUS`。可选 token 只能通过运行时内存注入，并且只用于明确需要的 read-only probe。
它不得出现在：

- CLI 参数、URL、request/Policy 文件；
- 日志、异常、fixture、Evidence、Bundle、截图；
- Git diff、环境快照或原始 headers/body 留存。

Evidence 只保留：

```text
access_mode = ANONYMOUS | AUTHENTICATED_READ_ONLY
visibility = PUBLIC | PRIVATE_OR_RESTRICTED | UNKNOWN
permission_observation = SUFFICIENT | INSUFFICIENT | UNKNOWN
```

匿名与认证下的同一可见平台事实可以拥有相同 `facts_digest`，但具体 Evidence provenance 和 SHA 不同。
`404` 可能是不存在，也可能是不可见；P1 不把它直接规范化为“不存在”。

## 7. Probe 图与规范化边界

Collector 只执行投影所需 probe，并按下列固定依赖顺序串行运行：

1. repository：`GET /repos/{owner}/{repository}`；
2. exact commit：`GET /repos/{owner}/{repository}/commits/{target_commit_sha}`；
3. PR（适用时）：`GET /repos/{owner}/{repository}/pulls/{pull_request_number}`；
4. active branch rules（适用时）：`GET /repos/{owner}/{repository}/rules/branches/{branch}`；
5. required status protection fallback（仅需解释旧式 protection 且权限允许时）；
6. check runs：`GET /repos/{owner}/{repository}/commits/{target_commit_sha}/check-runs?filter=all`；
7. combined commit statuses：读取 exact SHA 的 status contexts；
8. Release（适用时）：按 exact tag 获取 Release；
9. tag ref 与 bounded peel（适用时）：读取 `refs/tags/{release_tag}`，最多解引用 `5` 层；
10. Pages metadata（适用时）：`GET /repos/{owner}/{repository}/pages`。

Rules API 返回对分支生效的 active rules，包括仓库或组织层规则；它与 observed check runs 是两类事实，
不能互相替代。官方文档同时表明 required check 可以携带 integration/app identity，而 check runs 也带
app identity；因此显示名只用于展示，不能作为唯一匹配键。参考：[repository rules](https://docs.github.com/en/rest/repos/rules)、
[protected branch checks](https://docs.github.com/en/rest/branches/branch-protection) 与
[check runs](https://docs.github.com/en/rest/checks/runs)。

每个 probe 必须保留：

```text
sequence
probe_id
observed_at
method = GET
actual_path_and_safe_query
actual_operands
http_status
returned_identifiers
etag_if_available
github_request_id_if_available
rate_limit_metadata_if_available
page_count
attempt_count
elapsed_ms_monotonic
outcome
```

不得保留 Authorization、Cookie、全部 request headers 或原始 response body。多次 API 调用组合成的是
一个有界采集窗口，不是 GitHub 的原子快照；墙钟只记录观察时间，窗口限制只使用 monotonic elapsed。

## 8. 规范化事实

P1 Evidence 的 `facts` 只保存计划投影需要的字段，并至少按以下分区：

```text
repository
commit
pull_request
required_checks
observed_checks
release
tag
pages
conflicts
```

关键规则：

- commit 事实必须回显 GitHub 返回的 exact SHA；请求路径中的 SHA 不能替代响应事实；
- PR 分开保存 `head.sha`、`base.sha`、`merged`、`merge_commit_sha`；合并前的 test merge SHA 不得冒充
  最终主线提交；
- required check identity 至少保存 `context`、source kind 和可得的 integration/app identity；
- observed check identity 至少保存 name/context、app id/slug、suite/run id、status、conclusion 与 head SHA；
- 同名异源保持多条；身份不足时写显式 ambiguity/conflict，不静默去重；
- tag 分开保存 `ref_target_sha`、`object_type`、完整 bounded peel chain 与 `peeled_commit_sha`；
- lightweight 与 annotated tag 可得到相同 `peeled_commit_sha`，但 provenance 不同；
- Release 保存 release id、tag name、`target_commitish`、draft/prerelease/immutable、published time 和
  规范化 asset identity；`target_commitish` 不能代替 tag peel；
- Pages 只保存 API 可见的 site/build/source metadata；P1 不声称公开页面内容已经更新。

GitHub 官方说明 PR 的 `merge_commit_sha` 会随未合并、merge、squash、rebase 状态改变，因此它必须和
`merged`、head/base 坐标一起解释；Release 的 `target_commitish` 也只是创建时的 commitish，不能代替
真实 tag ref。参考：[pull requests](https://docs.github.com/en/rest/pulls/pulls)、
[releases](https://docs.github.com/en/rest/releases/releases)、[Git tags](https://docs.github.com/en/rest/git/tags)
和 [GitHub Pages](https://docs.github.com/en/rest/pages)。

## 9. Evidence 0.1 映射

输出 `evidence_type` 固定为 `platform.github.api.snapshot`。`metadata.veritrail_observation` 必须完整写入
Core 已冻结的十个字段：

```text
schema_version = 0.1
canonicalization_profile = veritrail-json-c14n/1
plan_digest
observation_spec_digest
request_seal_digest
collection_session_id
collector_role = github-api
coverage
normalization_semantics_version = github-rest-facts/0.1
facts_digest
```

`coverage` 只能是 `COMPLETE | PARTIAL | ERROR | NOT_APPLICABLE`。它描述投影覆盖，不是 Verdict；Collector
不得生成 `all_required_checks_passed`、`release_is_correct`、`merged_to_expected_sha` 等结论字段。

具体 Evidence 另保留 request/policy identity、access mode、安全的 collector/parser/API provenance、
probe records、collection elapsed 和错误列表。Core 只按公开 Evidence 合同导入，并从 Plan assertions
直接读取规范化事实。

## 10. 错误与停止语义

| 条件 | Collector 结果 | 禁止推断 |
| --- | --- | --- |
| Plan/request/policy/seal 不一致 | 联网前拒绝，不生成伪 Evidence | 不能相信外带 digest |
| 未知投影/profile/float | 联网前拒绝 | 不得降级猜测 |
| `401` | `ERROR` + auth category | 不等于资源不存在 |
| `403` 且 rate limit 明确 | `ERROR` + bounded rate-limit provenance | 不得无限重试 |
| `403` 权限不足 | `PARTIAL` 或 `ERROR` | 不等于规则不存在 |
| 歧义 `404` | `PARTIAL`/`ERROR` + visibility unknown | 不等于不存在 |
| `429` | 遵守 bounded Retry-After；越过总窗口后 `ERROR` | 不得绕过平台建议 |
| `304` | `ERROR` | P1 无精确旧证据绑定，不能重建当前事实 |
| `5xx`/timeout/network error | 有界重试后 `ERROR` | 不得用最近成功结果代替 |
| JSON/字段语义异常 | `ERROR` + parser category | 不得静默丢字段 |
| 分页/请求/peel 上限到达 | `PARTIAL` + truncation reason | 不得标记 COMPLETE |
| 平台在窗口内变化 | 保留 probe 冲突和时间 | 不得称为原子快照 |

若发生进程取消或异常，已生成但未完成校验的 staging 文件必须清理；最终 Evidence 采用 create-new +
atomic publish，不覆盖既有产物。P1 不拥有远端资源，因此没有远端 cleanup 动作。

## 11. P1 验收矩阵

每个负例只改变一个预注册变量。P1 实现候选必须串行完成：

### 11.1 纯离线合同

1. `veritrail-json-c14n/1` 四个冻结向量在 Python 3.10/3.13 逐字节一致；
2. request 可从同一 sealed Plan 确定性派生；未知/重复/缺条件字段在 I/O 前拒绝；
3. request 出现 `expected.*`、token、URL 或自由文本命令时拒绝；
4. Plan 无关 revision 变化：spec/fact identity 不变，request/Evidence identity 改变；
5. Policy 改变：policy/request/Evidence identity 改变，spec/fact identity 不变；
6. 同 request 重放：新 session、相同 facts 可同 digest、Evidence SHA 必须不同；
7. normalization semantics version 单独变化：facts digest 必须变化；
8. API/client/parser 实现 version 单独变化：facts digest 不变，Evidence SHA 变化。

### 11.2 内存 transport / fixture server

9. repository + exact commit 正链；请求 SHA 与响应 SHA 不同负链；
10. PR 未合并、已合并 merge、squash、rebase 坐标分别保留；
11. active rules required set 与 exact SHA observed set 分开输出；
12. 同 display name、不同 app/source 不被去重；身份不足形成 ambiguity；
13. commit status 与 check run 同名但来源不同不被错误合并；
14. lightweight/annotated tag 指向同一 commit 得到同 peeled SHA 和不同 provenance；
15. tag 错目标、非 commit、循环/超过 peel 上限分别可辨；
16. Release tag 正确/错误、asset 缺失/重复、`target_commitish` 歧义分别保留；
17. Pages present/not applicable/permission ambiguous 分开；
18. `401/403/404/429/5xx/timeout/损坏 JSON/分页上限/意外 304` 分别 fail closed；
19. 合成 wall-clock 跳变不影响 monotonic 最大窗口；
20. token、Cookie、Authorization、个人路径和原始 body 对日志/Evidence/Git diff 为零。

### 11.3 Core 与旧消费者

21. 当前 Acceptance Core 可直接对 commit/ref、merge、required/observed checks、tag/release 的原始规范化
    字段断言，不需要插件 Verdict-like boolean；
22. metadata 畸形、spec digest 不符、facts digest 不符与 session 绑定错误保持 `INCONCLUSIVE`；
23. Core 全量普通/`-O`、Starter/Skill、Workbench、Browser Smoke 与历史 digest 回归不漂移；
24. Comparison、Pairing、Batch、Workbench 等旧消费者继续保持 PC2 冻结的显式隔离。

### 11.4 真实 GitHub 只读纵向切片

25. 对一个公开固定仓库、exact SHA 和 sealed Plan，匿名模式完成一次严格串行 API Evidence；
26. 对同一坐标重复采集，事实未变时得到相同 facts digest、不同 session 与 Evidence SHA；
27. 使用只读 token 重复可见事实，Evidence 只改变安全 provenance，不泄漏 token；
28. 至少一个单变量远端负链由 Core 直接得到预期非 PASS 结果；
29. wheel clean install 从 `site-packages` 运行，不从 checkout 偷导入；
30. 真实响应只在内存解析，最终保留文件可按 manifest 逐项重算，staging 和临时凭据为零。

真实 GitHub 测试不得依赖“永远会变化”的外部公开仓库作为唯一 CI 成功条件。CI 主门禁使用冻结、脱敏
fixture；真实 live probe 是人工触发、只读、有精确坐标和证据留存的候选冻结门。

## 12. P1 出口与停止线

P1 实现只有在以下条件全部满足后才能标记 `P1_FROZEN`：

1. 本合同先经受保护主线合入与公开渲染读回；
2. 插件代码从该精确主线基线另起工作树；
3. 第 11 节全部适用矩阵有可复现证据；
4. Python 3.10/3.13、普通/优化模式、wheel clean install 和 Core 全回归通过；
5. 候选经独立 PR、required checks、受保护主线合入；
6. 最终 README 与 P1 事实文档在未登录 GitHub 页面真实读回；
7. 最终状态仍明确没有 P2 浏览器、P3 Core handoff、P4 发布。

本合同合入只允许把状态升级为 `P1_CONTRACT_FROZEN / IMPLEMENTATION_NOT_STARTED`。在那之前不得创建
`plugins/github-evidence`；在 P1 冻结前不得进入：

- P2 公开渲染采集；
- API/Render 双源关系；
- P3 自动 handoff 或完整 Verdict pipeline；
- P4 插件版本、tag、Release、Pages 发布；
- GitHub 之外的真实性锚点或“终极真相”声明。

它验证的是已声明坐标之后的平台事实一致性与交付漂移，不证明封存之前的事实真实，也不裁定提出者的
观点终极正确。未知仍是未知，冲突仍保留冲突：**它防的是漂移，不是阴谋；它负责裁决纪律，不替现实
补答案。**
