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
9. **Trust ceiling is explicit**：本链只能检查支持范围内的证据一致性与承诺后完整性，不能仅凭内部
   自洽证明信任锚建立前的事实真实。
10. **Epistemic ceiling is explicit**：VeriTrail 不拥有被声明观点的终极真值，只负责保留声明、证据
    来源、验收过程、规则与 Verdict 的可追溯关系，并忠实保存未知、冲突和不可判。

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

## 8. 信任上限与共同故障域

### 8.1 三种不能混用的结论

```text
Consistency   证据、坐标与规则之间是否自洽
Authenticity  来源身份与制品归属是否得到额外可信机制支持
Truth         最初的源码、数据、实验或现实事件是否真实
```

本插件与 Core 首先检查 `Consistency`。在精确坐标和规则封存、Evidence 被采集并进入不可变 Bundle 后，
它们可以发现支持范围内的错绑、漏证、漂移和内容变化，即“承诺后的完整性”。它们不从内部自洽自动
推出 `Authenticity`，更不能推出 `Truth`。

例如，一套在首次封存前已被人为构造、但源码、数据、运行结果、Commit、PR、Checks、Release、Pages
和 sealed Plan 彼此一致的材料，可能满足全部预注册断言。此时 Core 最多能裁决“声明的 GitHub 平台
证据满足 sealed Plan”，不能把该 `PASS` 解释为上游数据或现实命题真实。

### 8.2 共同信任域

- GitHub REST API 与 GitHub 公开页面是不同交付面，可以互相暴露缓存、部署或链接漂移；它们仍由
  GitHub 同一平台权威提供，不是两个独立见证人。
- GitHub Evidence Plugin 是观察者，不是被观察事实的独立来源；插件正确运行不能证明 GitHub 本身
  没有平台级故障、受控管理员变更或共同失陷。
- VeriTrail Core 是规则裁决者，不是事实创造者；确定性裁决只能说明现有 Evidence 是否满足 sealed
  Plan，不能补出 Evidence 没有携带的现实真实性。
- sealed request / Plan 固定的是“准备相信和检查什么”，不是其内容诚实的证明。
- Bundle 哈希证明采集后字节和清单的对应关系，不证明采集前事实、采集者身份或声明时间真实。

因此，GitHub、插件与 Core 不是三个相互独立的真相来源。它们组成一条职责分离的工程证据链，但仍有
共同信任根；GitHub 全局不可用或同一权威提供一致但错误的状态时，本链不能凭自身完成外部反证。

### 8.3 可支持与不可支持的表述

| 可支持 | 不可仅凭本链支持 |
| --- | --- |
| 指定 Commit、PR、Check、Tag、Release、Pages 和公开标记在采集时是否对齐 | 原始源码、业务数据或实验输入在首次封存前没有被伪造 |
| Check 是否绑定错误 SHA，PR 是否未合入，Tag/Release 是否漂移 | GitHub 平台、仓库管理员或凭据从未失陷 |
| API 与公开渲染是否冲突，重复采集是否发生变化 | 平台账号等同于现实身份，或签名内容必然真实 |
| Evidence 进入 Bundle 后是否被静默修改 | 一个内部完全自洽的历史必然对应真实世界 |

允许的结论语言应带适用边界，例如：

> 在声明的 GitHub 信任域、采集时间和 sealed Plan 下，指定平台坐标与所需证据一致。

禁止把它缩写成“来源已被证明真实”“不存在事前造假”或“GitHub 不可能出错”。

工程俗语可概括为：**防君子，不防小人**。这里不是对使用者作道德判断，而是说明产品只提高误操作、
事后漂移、选择性遗漏与低成本篡改的发现成本；它不与能够在信任锚建立前共同控制源码、数据、结果、
平台坐标和 sealed Plan 的蓄意造假者对抗。

> **它防的是漂移，不是阴谋。**

### 8.4 外部锚是产品非目标

VeriTrail 与本插件不建设、托管或裁决 GitHub 之外的第三方签名见证、透明日志、可信时间戳、硬件
证明、仪器来源证明或多方见证网络。这些机制会引入新的身份、密钥、可用性与权威问题，不属于 P0–P4，
也不进入当前产品路线。

高风险场景若需要更高保证，应由使用方在 VeriTrail 之外选择和治理独立来源，再把“存在何种外部
保证”作为适用边界说明；Core 不得因看到一个签名或摘要就推断内容真实。任何未来的定位变化都必须
另立产品提案，不能作为 GitHub 插件的顺手扩展，也不能倒写 0.1 已经具备外部见证。

## 9. 认识论上限（Epistemic Ceiling）

### 9.1 两个上限下的三条风险路径

| 风险路径 | 主要来源 | VeriTrail 能做什么 | 不能承诺什么 |
| --- | --- | --- | --- |
| 封存前有意构造一套自洽材料 | 能共同控制源码、数据、结果与平台坐标的主体 | 声明信任域，保留采集后完整性并发现后续漂移 | 仅靠内部证据识别源头造假 |
| 人的前提或目标存在歧义、遗漏或后续争议 | Claim owner / Plan author | 版本化保存声明、反例、未决项与确认过程 | 代替提出者裁定观点终极正确 |
| Agent 诚实地理解了另一个问题 | AI / 执行 Agent | 限制权限与爆炸半径，要求报告冲突并验证是否偏离 sealed Plan | 从内部自洽自动发现未声明的真实意图 |

三条路径都可能留下“Plan、实现、测试、Evidence 与 Verdict 完全一致”的外观，但动机、权威和治理
动作不同，不能压成同一种风险。VeriTrail 只能辅助发现矛盾、保存边界并定位应回查的层级；当所有
输入从起点就内部一致时，它不能根治问题，也不能凭空制造外部真相。

### 9.2 验证正确不等于命题正确

```text
Verification Correctness != Specification Correctness
Claim Ownership          != Truth Ownership
```

VeriTrail 回答的是“这次执行是否满足 sealed Plan”，不回答“sealed Plan 表达的观点在终极意义上是否
正确”。一个 Plan、实现、测试、Evidence 与 Verdict 可以完全一致，却未必对应提出者真正想解决的
问题，也未必覆盖现实中的全部前提；内部没有矛盾时，VeriTrail 不能凭空发现一个未被声明的目标。

这类风险对 AI Agent 尤其重要：模型可能并无欺骗意图，只是理解了不同的问题，随后诚实地把与提出者
意图不一致的方向做成完整闭环。此时 `PASS` 只表示封存条件被保留证据满足，不得扩张为“用户真实
目标已被证明达成”。

> VeriTrail 不裁定一个被声明的观点在终极意义上是否正确，只裁定其预先声明的验收条件是否被现有
> 证据满足。

### 9.3 权威与职责

- 提出者拥有自己的 claim、问题定义与封存选择，承担前提与验收目标的最终决定责任，但这不等于
  拥有现实真相；
- 现实拥有最终真相，且现实可能模糊、不完整、随时间变化、相互冲突或当前不可判；
- VeriTrail 拥有声明、证据来源、验收过程、规则版本和 Verdict 推导的完整性，不拥有世界真相；
- 插件只观察声明范围内的平台事实，不能评价人的想法，也不能扩大或重写其验收目标；
- AI 或执行 Agent 负责在授权边界内忠实质疑、规划和执行；发现与前提冲突的证据时必须报告，却
  不能擅自改写人的目标、扩大现实权限或把自己的世界模型冒充最终真值。

这不是“输入错了不管”。更准确的纪律是：

```text
Not responsible for Truth != Not responsible for Uncertainty
```

不拥有真理裁决权，反而意味着必须忠实保存不知道：`UNKNOWN` 仍是未知，来源冲突仍保留冲突，缺失
必需证据仍按既有规则得到 `PENDING`，不可归因仍得到 `INCONCLUSIVE`；任何一层都不能为了形成漂亮
闭环而补写、压平或升级成 `PASS / FAIL`。

### 9.4 人机责任链与失败归因

```text
Human       owns premise authority and the Seal decision
Agent       owns faithful challenge and authorized execution
VeriTrail   owns judgment discipline
Reality     owns truth
```

“人的前提由人决定”不能被 Agent 当成忽略明显反证的免责条款。Agent 若观察到“声明文件不存在，但
仓库中实际存在”之类的冲突，应把证据和影响交还提出者确认；在决定前不得继续扩大动作，在决定后也
只能执行被重新确认或新版本封存的目标。

VeriTrail 通过 Plan、权限边界、提交/封存屏障（commit barrier）、Evidence 与独立裁决，把推理错误
和现实副作用隔开：

```text
Reasoning Error   != Unbounded Real-World Effect
Premise Error     != Plan Error
Plan Error        != Execution Error
Execution Error   != Observation Error
Observation Error != Verdict Error
```

它不保证项目必然正确，而是让失败后能够判断应回查前提、规格、执行、证据还是裁决，避免模型同时
解释目标、修改目标、执行并自证成功。

反向排查顺序应遵循现有证据，而不是默认回到代码层强改：

```text
unexpected outcome
  -> verdict derivation
  -> evidence completeness and conflicts
  -> platform observation / delivery
  -> execution versus sealed Plan
  -> Plan versus declared intent
  -> premise review by its owner
```

若执行与 Evidence 已证明没有偏离，就回查 Plan 或前提；若 API 与公开页面冲突，就定位到平台渲染或
交付层。系统不得在问题已被定位到上游层后继续用重构代码制造“完成感”。

### 9.5 Seal 前只能降风险

Authoring 或人工流程可以在 Seal 前增加 premise review、反例、独立 challenge，以及由提出者或领域
责任人确认“系统理解的是不是准备验收的问题”。这些步骤降低误解概率，却不证明命题终极正确；两个
模型也可能共享同一错误先验。

此类审查不属于 GitHub Collector 的职责，不能让插件获得 Plan 修改权或 Verdict 权。若未来提供辅助
入口，它只能把问题、分歧、未决前提与确认者记录为声明事实；未决项必须继续可见。

> **现实拥有真相，VeriTrail 只拥有裁决纪律。**

## 10. 故障语义

| 观察 | 插件记录 | Core 可得出的最大结论 |
| --- | --- | --- |
| 明确取得 wrong SHA / failed required check / wrong tag target | 有来源的反例事实 | sealed assertion 可 `FAIL` |
| timeout / DNS / GitHub 5xx | `ERROR`，无目标事实 | 通常 `PENDING`；不能宣称目标失败 |
| rate limit `403/429` | 限流类别、可公开的 reset 信息 | `PENDING`，不得无限重试 |
| private resource 未授权时 `404` | `PARTIAL` + authority ambiguity | `INCONCLUSIVE` 或 `PENDING`，不得当作不存在 |
| API 与公开页面坐标冲突 | 两份独立事实及冲突 | `INCONCLUSIVE` |
| 页面有效显示旧内容 | public render 反例 | 若 Plan 要求当前渲染，可 `FAIL` |
| API 与页面在共同信任域内返回一致但错误或预先构造的状态 | 按来源记录所见事实与已声明信任域 | 最多判断与 Plan 一致；不得升级为来源真实性或现实真实性 |
| probe 未在请求中声明 | `NOT_APPLICABLE` 或不输出 | 不得补做、不得扩大验收范围 |

GitHub 官方说明某些私有资源在授权不足时会返回 `404`；因此 `404` 只有在请求权威和可见性已经独立
确认时，才能作为“资源不存在”的事实。

## 11. 首个验收矩阵

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
14. 一套内部自洽的合成材料只能得到带 GitHub 信任域限定的结果，报告不得生成“上游事实真实”或
    “不存在事前造假”的扩张性表述；
15. GitHub API 与公开页面共同不可用或共同返回无法外部反证的状态时，Evidence 必须保留共同故障域，
    不得把两个观察面计成两个独立权威。
16. 一套 Plan、实现、测试与 Evidence 内部一致但未覆盖某个未声明真实目标的合成案例，只能证明 sealed
    条件被满足，报告不得宣称观点终极正确或用户真实目标已经得到证明；
17. 未知前提、来源冲突和缺失必需证据分别保持可见，并按既有 Core 规则进入 `INCONCLUSIVE` 或
    `PENDING`，不得由插件、AI 或展示层补写成确定结论。
18. Agent 观察到与人类前提冲突的仓库事实时必须保留并上报冲突；不得以“前提由人负责”为由忽略，
    也不得在未经重新确认或新版本 Seal 的情况下自行改写目标继续执行。

每个负例只改变一个预注册变量；不能用同一份混合失败同时证明多个边界。

## 12. 未来包边界

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

## 13. 明确延期

本产品不包含 GitHub 之外的独立见证、可信时间锚或来源真实性网络。首个版本也不包含 GitHub
Enterprise、自定义 Host、GraphQL、webhook server、GitHub App 安装流程、
自动定时器、组织级仪表盘、仓库修复、PR 合并、规则集修改、Release 发布、Pages 部署、跨平台统一
SPI 或通用网页爬虫。后述 GitHub 平台能力需要新合同；外部见证不因新合同自动进入本产品路线。
