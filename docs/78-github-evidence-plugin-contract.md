# VeriTrail GitHub Evidence Plugin 0.1 合同

> 状态：`P0_CONTRACT_FROZEN / IMPLEMENTATION_NOT_STARTED`
>
> 产品：独立平台证据插件；候选包名 `veritrail-github-evidence`
>
> 影响层级：插件内部 `L2_CONTRACT`；VeriTrail Core 为只读消费者

## 1. 问题与首个边界

本插件解决一个有界问题：从 GitHub 读取指定仓库和指定坐标的外部平台事实，并把它们规范化为
VeriTrail 可验证的 Evidence。它用于发现“本地、分支、PR、主线、Release 与公开页面不是同一层”
产生的展示或交付漂移。

首个版本不是 GitHub 管理机器人、部署器、合并器、通用爬虫、持续监控服务或 Verdict 引擎。它不
替用户修仓库，也不根据“最新”自动选择应被证明的提交。

## 2. 不变量

1. **Read only**：所有 GitHub 与浏览器操作均为只读；插件不存在远端写入口。
2. **Exact coordinates**：owner、repository、ref、commit、PR、tag、release 或页面期望必须来自已封存
   请求或 Plan，不能从执行结果倒推。
3. **API is not rendering**：REST API 成功不能证明用户看到的页面已经更新。
4. **Observation is not verdict**：插件只产生事实和采集状态，不产生 `PASS / FAIL / INCONCLUSIVE /
   PENDING`。
5. **One source, one record**：API、公开浏览器和用户提供的本地事实分别记录来源，不合并成不可追溯
   的布尔值。
6. **Fail closed on ambiguity**：无权限、限流、超时或来源冲突不得被当作“目标不存在”或“验收通过”。
7. **No secret persistence**：令牌、Cookie、Authorization、响应体、私人路径和账号环境值不进入
   Evidence、日志、截图或测试夹具。
8. **Core owns semantics**：插件升级、失败或卸载不能改变 Core 的裁决规则。

## 3. 请求合同

P1 实现前必须把输入冻结为版本化 `github-observation-request 0.1`。最低字段为：

```text
schema_version
request_id
repository.owner
repository.name
expected.commit_sha
probes[]
captured_policy.api_version
captured_policy.public_mode
timeouts
```

每个 probe 还必须声明自己的精确坐标和期望，例如 PR number、required check name、tag、Release ID、
Pages URL 或公开页面的有限可见标记。请求封存后计算 canonical SHA-256；改变仓库、提交、检查集合、
页面或期望值必须创建新请求，不能回写旧请求。

默认拒绝：

- 任意 URL、任意 Host、IP 字面量和 URL 中的凭据；
- 缺失 `expected.commit_sha` 的“检查最新状态”；
- 通配符仓库、组织全量扫描和无限分页；
- 页面脚本、自由文本 Shell、任意文件读取和响应体持久化。

P1 的固定网络目标仅为 `https://api.github.com`；P2 才允许由请求中 owner/repository 推导的
`https://github.com` 公共页面与已验证的 GitHub Pages 最终跳转。GitHub Enterprise 留给后继合同。

## 4. 采集器分层

### 4.1 Structured API Collector

负责白名单 REST `GET` 请求和字段规范化：

- repository identity、visibility、default branch；
- commit/ref；
- pull request state、head/base SHA、merged 状态与 merge commit；
- required rules/check names 与指定 commit 的 check runs/statuses；
- tag、release、asset name/size/digest when available；
- Pages configuration/deployment metadata when applicable。

它不下载任意 Release 资产，不解析 README 视觉结果，也不推断浏览器是否已经获得最新内容。

### 4.2 Public Render Collector

P2 使用全新、未登录、无持久 Profile 的浏览器 Context，只负责用户可见结果：

- requested URL 与 final URL；
- HTTP/导航结果；
- 页面类型与可见标记；
- 目标链接 href；
- 规范化可见文本签名；
- 视口、浏览器版本与采集时间；
- 必要时的脱敏截图附件哈希。

浏览器不读取开发者已登录 Session，不继承本机 Cookie，不把 DOM 全文、HAR 全量响应或屏幕上的私人
信息持久化。截图默认是本地运行附件并被 Git 忽略；只有合成、脱敏、合同所需的最小夹具才可入库。

## 5. Evidence 0.1 映射

两个 Collector 分别输出现有通用 Evidence 0.1 外壳，禁止先合成一份“万能 GitHub 状态”：

```json
{
  "schema_version": "0.1",
  "evidence_type": "platform.github.api.snapshot",
  "source": "veritrail-github-evidence",
  "captured_at": "<RFC3339 UTC>",
  "facts": {},
  "observed_variables": {},
  "metadata": {}
}
```

Public Render Collector 使用独立 `platform.github.public-render`，并引用同一 sealed request digest。
Core 通过 Plan 关联两份 Evidence；插件不得把 API 与浏览器结果预先压成一个跨源布尔值。P0 不修改
Core Schema。P1 必须先证明通用 Evidence 外壳足以严格校验插件事实；如果需要改变 Core 公共
Schema，必须停止 P1，另开 Core 兼容合同，不能把字段校验塞进私有导入。

API Evidence 的 `facts` 至少保留：

```text
request_identity
repository
commit
pull_request
required_checks
observed_checks
release
pages
request_alignment
coverage
collection_errors
```

Render Evidence 独立保留 request identity、requested/final URL、navigation、visible markers、links、
content signature、viewport、coverage 与 collection errors。`request_alignment` 只能比较这份来源和
sealed request，例如 `main_sha_matches_expected`；必须同时保留两个操作数和推导规则版本。跨 API /
浏览器一致性只由 Core 的 sealed assertion 计算。所有 alignment 都只是事实，不是断言状态，更不是
Verdict。

采集状态只允许：

| 状态 | 含义 |
| --- | --- |
| `COMPLETE` | 请求的 probe 都取得可用来源事实 |
| `PARTIAL` | 一部分 probe 有事实，另一部分缺失或不可判 |
| `ERROR` | 采集器未能形成该 probe 的可信事实 |
| `NOT_APPLICABLE` | 请求明确声明该 probe 不适用 |

这些词只描述采集覆盖，不映射到 Core `ExecutionStatus` 或 `Verdict`。

## 6. 规范化与确定性

- 响应只保留合同白名单字段；未知新增字段默认忽略并记录解析器版本。
- 列表使用稳定业务键排序；重复项不得静默覆盖。
- volatile headers、请求耗时、采集时间和速率窗口进入 metadata，不参与 canonical fact digest。
- canonical fact digest 必须包含请求摘要、API 版本、插件版本、来源坐标和规范化 facts。
- 同一封存请求与同一来源快照应生成相同 canonical facts；时间与 request ID 的差异不能制造事实漂移。
- GitHub API 版本升级、字段语义变化或规范化规则变化必须产生新插件合同/解析器版本。

## 7. 权限、凭据与网络

默认模式匿名读取公开资源。GitHub 文档说明公开资源的部分检查接口可不认证读取；需要认证时，只接受
运行时进程环境或调用方内存传入的可选 token，优先 fine-grained token，并限制到实际 probe 所需的
只读权限。token 不得出现在 CLI 参数、URL、配置文件、Bundle、异常文本或测试快照中。

实现必须：

- 设置 `Accept`、稳定 `User-Agent` 与显式 `X-GitHub-Api-Version`；
- 串行、有界请求，不做组织级并发扫库；
- 使用条件请求与缓存标识降低重复读取；
- 遵守 `retry-after`、`x-ratelimit-remaining` 和 `x-ratelimit-reset`，有界退避后停止；
- 区分 `401`、权限不足、主/次限流、网络超时、服务器错误和数据校验错误；
- 不把 GitHub request headers、token 或原始响应 body 写入持久产物。

官方依据：

- [REST API 最佳实践](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)
- [REST API 限流](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
- [REST API 故障排查](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api)
- [REST API 认证](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api)
- [REST API 版本](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
- [Check runs](https://docs.github.com/en/rest/checks/runs)
- [Pull requests](https://docs.github.com/en/rest/pulls/pulls)
- [Repository rules](https://docs.github.com/en/rest/repos/rules)
- [Releases](https://docs.github.com/en/rest/releases/releases)
- [GitHub Pages](https://docs.github.com/en/rest/pages/pages)

## 8. 故障语义

| 观察 | 插件记录 | Core 可得出的最大结论 |
| --- | --- | --- |
| 明确取得 wrong SHA / failed required check / wrong tag target | 有来源的反例事实 | sealed assertion 可 `FAIL` |
| timeout / DNS / GitHub 5xx | `ERROR`，无目标事实 | 通常 `PENDING`；不能宣称目标失败 |
| rate limit `403/429` | 限流类别、可公开的 reset 信息 | `PENDING`，不得无限重试 |
| private resource 未授权时 `404` | `PARTIAL` + authority ambiguity | `INCONCLUSIVE` 或 `PENDING`，不得当作不存在 |
| API 与公开页面坐标冲突 | 两份独立事实及冲突 | `INCONCLUSIVE` |
| 页面有效显示旧内容 | public render 反例 | 若 Plan 要求当前渲染，可 `FAIL` |
| probe 未在请求中声明 | `NOT_APPLICABLE` 或不输出 | 不得补做、不得扩大验收范围 |

GitHub 官方说明某些私有资源在授权不足时会返回 `404`；因此 `404` 只有在请求权威和可见性已经独立
确认时，才能作为“资源不存在”的事实。

## 9. 首个验收矩阵

P1–P3 至少逐项建立独立夹具或真实证据：

1. exact commit、required checks、merge、release 与 public render 全部一致；
2. 本地提交存在但远端分支没有该 SHA；
3. check run 成功，但不是规则要求的 context；
4. PR 已通过检查但没有合入；
5. PR 已合入，但 main SHA 不是期望 SHA；
6. tag/Release 存在，但 tag 指向错误提交或资产集合不符；
7. Pages deployment 完成，但发布源或公开内容仍旧；
8. API 中 README 已更新，公开渲染缺少期望标记；
9. API 与浏览器事实冲突；
10. `401`、权限不足 `403`、歧义 `404`、限流、超时、损坏 JSON 和分页上限；
11. 相同来源快照重复规范化，canonical facts 与 digest 相同；
12. token、Cookie、私有路径和原始响应体在日志、Evidence、Bundle、截图与 Git diff 中均不存在；
13. Core 0.12.2 全量回归、Starter/Skill、Workbench 与 Browser Smoke 不受影响。

每个负例只改变一个预注册变量；不能用同一份混合失败同时证明多个边界。

## 10. 未来包边界

P1 经批准后可采用：

```text
plugins/github-evidence/
  pyproject.toml
  src/veritrail_github/
  tests/
  examples/
```

目录只是候选，不在 P0 创建。包不得放入 `src/veritrail`，不得 monkey-patch Core，不得依赖 Core 私有
符号。Core 通过文件或公开 API 消费标准 Evidence；插件卸载后既有 Bundle 仍可验证和阅读。

## 11. 明确延期

首个版本不包含 GitHub Enterprise、自定义 Host、GraphQL、webhook server、GitHub App 安装流程、
自动定时器、组织级仪表盘、仓库修复、PR 合并、规则集修改、Release 发布、Pages 部署、跨平台统一
SPI 或通用网页爬虫。需要其中任何一项时必须先写新合同。
