# VeriTrail GitHub Evidence Plugin 0.1 合同

> 后继状态：`P1_CONTRACT_FROZEN / IMPLEMENTATION_NOT_STARTED`。PC2 已关闭本合同记录的 Core
> 兼容阻断；P1 的精确施工与验收边界见
> [文档 83](83-p1-structured-github-api-collector-contract.md)。下文保留 P0 冻结时的探针与停止事实，
> 不把历史未通过状态改写成已经存在 Collector；文档 83 的实现前合同现已冻结。

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
2. **Exact coordinates**：owner、repository、ref、commit、PR、tag、release 或页面观察选择器必须从
   sealed Plan 按版本化规则派生，不能由插件选择，也不能从执行结果倒推。
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
11. **Plan owns expectations**：sealed Plan 是验收期望的唯一权威；observation request 只能机械派生
    并携带观察坐标，不能另造 `expected.*` 或独立通过语义。
12. **Identity beats display name**：required check 的显示名不等于事实身份；可取得的 producer、app、
    workflow、job 与来源类型必须保留，歧义不能静默折叠。
13. **Collection is not an atomic snapshot**：精确 SHA 不能把多次平台调用变成同一时刻的世界；每个
    probe 的观察时间、实际操作数和总采集窗口必须可见。
14. **Request identity is not fact identity**：request ID、Plan revision、采集时间或非语义运行策略可以
    标识一次请求或执行，不能让语义相同的观察规格与相同来源事实产生不同 `facts_digest`。
15. **Fact identity is not Evidence identity**：`facts_digest` 只标识规范化事实内容；现有
    EvidenceArtifact SHA-256 标识一份包含 provenance 的具体证据文件。二者不能互相替代，也不能与
    Core Run/Execution identity 混用。
16. **Request is not observation**：sealed request 可以重放；每次实际采集必须建立新的 Collection
    Session。同一 request、同一 facts 不等于同一次观察，跨 session 产物不得静默配对。
17. **Core retains verdict authority**：Plan 与 Core assertion algebra 必须能直接基于原始规范化事实表达
    所需规则；插件不得输出 `*_passed`、`*_match`、`*_is_correct` 等 Verdict-like boolean 规避表达缺口。
18. **Schema validity is not semantic compatibility**：能通过 ExperimentPlan Schema 不等于按字段原意
    建模；不得虚构 PRIMARY variable、baseline、load model 或其他实验事实来适配插件。
19. **Canonical bytes are versioned**：SHA-256 只在 canonicalization profile 与输入投影同时明确时有
    可复核语义；未知 profile、非有限 JSON 或未冻结数字规则必须 fail closed。
20. **Cache response is not current fact**：`304 Not Modified` 没有当前表示正文；除非与精确旧 Evidence、
    facts、资源坐标和 validator 绑定，否则不能重建当前事实。
21. **Reference identity is not commit identity**：lightweight tag ref、annotated tag object、Release
    metadata 与最终 commit 是不同坐标；比较提交时必须使用有来源的 `peeled_commit_sha`。

## 3. 请求合同

P1 实现前必须把输入冻结为版本化 `github-observation-request 0.1`。最低字段为：

```text
schema_version
request_id
canonicalization_profile
plan_digest
derivation.version
observation_spec.version
observation_spec_digest
repository.owner
repository.name
target.commit_sha
probes[].type
probes[].coordinates
captured_policy.policy_id
captured_policy.version
captured_policy.digest
captured_policy.api_version
captured_policy.public_mode
captured_policy.timeouts
seal.algorithm
seal.digest
```

请求由两个权威不同的输入确定性组装：验收范围与观察坐标从 sealed Plan 机械派生，并以 `plan_digest`
绑定；API 版本、公开模式、超时和重试预算来自只含运行约束的 versioned Collector Policy，并以独立
digest 绑定。Collector Policy 不能包含 required set、期望值或 assertion，也不能改变相同 Evidence
在 Core 中的 Verdict。

`plan_digest` 本身只说明引用对象，不能单独证明派生正确；插件必须按版本化的 `derivation.version`
从实际 sealed Plan 重算 repository、target 与 probes，并在联网前逐字段比对。请求只回答“去哪里观察、
采集哪些字段”，不回答“观察到什么算满足”。每个 probe 只声明精确资源坐标和有限投影，例如
PR number、target commit、check source coordinate、tag、Release ID、Pages URL 或公开页面观察选择器；
Plan 才拥有 required set、期望值和 assertion。请求的 `seal.digest` 对排除 `seal` 字段自身后的 canonical
unsigned envelope 计算 SHA-256；不得手工编辑。坐标、投影或适用 probe 变化时必须从新版本 Plan 重新
派生，不能让 request 成为第二份期望权威。

P1 兼容 Core 0.12.2 时，`request.plan_digest` 必须满足：

```text
request.plan_digest
== verified sealed Plan.seal.digest
== SHA256(veritrail-json-c14n/1(unsigned Plan excluding seal))
```

这里的最后一项是对 Core 0.12.2 现有实现行为的具名冻结，不给历史 Plan 新增字段，也不重算既有
Bundle。整个 sealed Plan 文件（含 `seal`）的文件 SHA-256 不是 `plan_digest`。

`observation_spec_digest` 只标识“观察什么”，必须由 `observation_spec.version`、规范化资源坐标、probe
类型与有限投影计算；它不包含整个 `plan_digest` 或 `derivation.version`。后两者仍由 request envelope
绑定，用来证明“这份观察规格从哪份 Plan、按哪条规则产生”。否则 Plan 中与观察规格无关的说明或
assertion 变化也会污染事实身份。两个 Plan revision 若机械派生出完全相同的观察规格，其
`observation_spec_digest` 可以相同，但 request seal 与后续 Evidence artifact identity 必须继续可区分。

三个摘要用途不能混用：

```text
observation_spec_digest  c14n profile + spec version + normalized coordinates/probes/projections (excluding digest)
collector_policy.digest c14n profile + API version + public mode + timeout/retry/resource bounds (excluding digest)
request seal digest      canonical unsigned envelope, including request/Plan/derivation/spec/policy (excluding seal)
```

前两者分别标识“观察什么”和“怎样有界采集”，最后一个只封存这次请求实例。`plan_digest`、
`derivation.version`、`request_id`、本地时间和非语义运行策略不进入 `observation_spec_digest`；任何摘要
都不等于批准者身份、可信时间或事实真实。
这些都是请求侧身份，不是 `facts_digest` 或现有 EvidenceArtifact SHA-256 的别名。

### 3.1 Canonicalization Profile

P1 所有插件侧 JSON 摘要固定声明 `canonicalization_profile=veritrail-json-c14n/1`。Profile 1 精确复用
Core 0.12.2 的 `canonical_json_bytes`：UTF-8、无 BOM、对象键按 Unicode code point 升序、分隔符固定为
`,` 与 `:` 且不插入空白、非 ASCII 字符保持 UTF-8，仅按 JSON 要求转义控制字符/引号/反斜线，并拒绝
`NaN` 与正负无穷。字段 absent 与显式 `null` 是不同输入。

为避免不同运行时的浮点打印规则进入首片身份，P1 digest 投影只允许 string、boolean、null、整数、
array 和 object；时间使用 RFC3339 string，耗时/大小/计数使用具名整数单位。需要浮点事实时必须先为
其十进制/单位规范化另立 profile 版本，不能直接依赖语言默认序列化。

冻结测试向量如下；哈希均对表中 canonical UTF-8 字节计算 SHA-256：

| 输入语义 | Canonical JSON | SHA-256 |
| --- | --- | --- |
| empty object | `{}` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |
| key ordering | `{"a":1,"b":2}` | `43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777` |
| Unicode / bool / null | `{"enabled":true,"label":"验迹","value":null}` | `8e7d13a7fc5609925598e1f5a9b8db749a4c54a49c4bea2acda36adf1418c270` |
| nested array/object | `{"items":[3,2,1],"nested":{"a":"A","z":0}}` | `3ec5a09f647d26013353111c8569e41444237e1c517fd481658b3587f03b0f30` |

未知 profile、非有限值、未声明浮点规范化、测试向量不匹配或请求/Policy/profile 身份不一致时，必须
在联网前拒绝。Profile 变更不会追溯改变 Core 历史 Plan、Evidence 或 Bundle；需要兼容新 Core 时另立
映射合同。

现有 ExperimentPlan Schema 允许通用 variables、required evidence 与 assertions，但没有命名的 GitHub
坐标字段。P0 不预判这些通用字段一定足以形成无歧义映射。P1 的第一项设计证据必须冻结
Plan-to-request derivation map，并用合成 Plan 证明可重复派生；如果只能依赖自由文本、未声明私有字段
或修改 Core 公共 Schema，必须停止 Collector 施工并另开兼容合同。

通过 derivation map 只是第一道门。P1 还必须用当前 Core 的真实 Plan 校验器与 Verdict evaluator 证明：

- GitHub 坐标使用 variables、baseline、load model 等字段时符合这些字段本来的实验语义，不是为了
  Schema 通过而编造占位事实；
- commit/ref、merge、required check identity/set、tag/release 等首片断言可以直接读取规范化事实；
- 插件不需要先计算 `all_required_checks_passed=true`、`release_is_correct=true` 或同类结论；
- 需要的集合包含、跨 Evidence 关系或动态值比较若超出现有 assertion algebra，必须停止并另开 Core
  兼容合同，而不是把关系判断藏进 Collector。

因此：**能被 Schema 塞进去，不等于语义兼容；能被 Core 比较，不等于裁决权没有泄漏。**

P0 已对 Core 0.12.2 做离线兼容探针，得到两条必须保留的负事实：

1. 合成 GitHub Plan 可以通过 validator，并在三个 API 字段字面断言通过时得到 `PASS`；即使 Evidence
   完全没有 `observed_variables`，声明的 PRIMARY 也不会因此缺证据。这只证明结构接受，不证明
   `SINGLE_VARIABLE`、baseline 与 load model 被按原义使用。
2. API Evidence 的 `collection_session_id=session-A`、Render Evidence 的
   `collection_session_id=session-B` 时，分别对两个字段做 `exists` 断言仍会得到 `PASS`。当前 Assertion
   只比较“一个 evidence type 的一个 JSON Pointer”与 literal expected，不能表达跨 Evidence 动态相等。

所以当前兼容门的裁决是 **未通过**，而不是“以后再测”。`P1_NOT_STARTED` 保持有效；下一项允许工作
仅为独立 Core 兼容合同。该合同必须先解决非因果平台验收计划的真实字段语义，以及由 Core 判断的跨
Evidence 关系，再决定是否需要公共 Schema/规则演进。插件不得利用 `observed_variables` 的偶然冲突
检测、占位 NUISANCE 值或预计算布尔值冒充正式关系合同。

[Post-P0 Core 兼容桥合同 0.1](80-p0-core-compatibility-contract.md) 已把这项裁决具体化为独立
`AcceptancePlan 0.1`、公共 Evidence requirement/binding 和跨 Evidence operand。它不修改本合同的
GitHub 采集语义，也不让 Core 认识 GitHub；只有通用 Core 实现、旧行为兼容和运行证据在 PC1/PC2
完成冻结后，本合同的 P1 Collector 才可施工。

默认拒绝：

- 任意 URL、任意 Host、IP 字面量和 URL 中的凭据；
- 缺失或未知 canonicalization profile，缺失 `plan_digest`、派生规则版本、observation spec
  version/digest、Collector Policy digest、无法证明机械派生关系，或缺失 `target.commit_sha` 的“检查
  最新状态”；
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
- required rules/check identities 与指定 commit 的 check runs/statuses；身份至少区分显示名、来源类型，
  并保留 API 可提供的 producer/app、workflow/job、外部标识与来源 URL；
- tag ref target、object type、bounded peel chain、最终 `peeled_commit_sha`、release metadata、asset
  name/size/digest when available；lightweight ref 与 annotated tag object 分开记录；
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
目标合同要求 Core 通过 Plan 关联两份 Evidence；插件不得把 API 与浏览器结果预先压成一个跨源布尔
值。P0 不修改 Core Schema，而本轮探针已经确认 Core 0.12.2 不能表达该跨源动态关系。因此必须先另开
Core 兼容合同；在合同及其后继实现通过前，P1 Collector 不启动，也不能把字段或关系校验塞进私有导入。

后继通用 Core 不从 `facts` 中猜绑定。插件 Evidence 必须在现有开放 `metadata` 中写入
`metadata.veritrail_observation`，并显式绑定 `plan_digest`、`observation_spec_digest`、
`collection_session_id`、collector role 和 normalization/profile identity；Core 只验证这份公共
metadata 子合同。下列更丰富的 GitHub request、session、policy 与平台 provenance 仍保留在本合同定义的
事实/元数据中，但不得形成第二套与公共 binding 竞争的权威字段。

API Evidence 的 `facts` 至少保留：

```text
request_identity
collection_session_identity
observation_spec_identity
collector_policy_identity
canonicalization_profile
normalization_semantics_version
facts_digest
repository
commit
pull_request
required_checks
observed_checks
release
pages
request_binding
collection_window
probe_observations
source_provenance
access_mode
coverage
collection_errors
```

Render Evidence 独立保留 request identity、collection session identity、observation spec identity、
Collector Policy identity、canonicalization profile、`normalization_semantics_version`、`facts_digest`、
requested/final URL、navigation、visible markers、links、content signature、viewport、provenance、access
mode、coverage、collection window 与 collection errors。两个 Evidence
类型各自对自己的语义投影计算 `facts_digest`；不得复用另一 Collector 的 fact identity，也不得因为引用
同一 request 就合并成一份事实。`request_binding` 只
证明响应资源与请求坐标相符，例如“响应 commit SHA 等于本次 target commit”；它必须保留两个操作数
和推导规则版本，不能使用 `*_matches_expected` 一类暗示验收的名字。Evidence 是否满足 Plan 只能由
Core 的 sealed assertion 计算；跨 API / 浏览器一致性也只能在 Core 内推导。所有 binding 都只是
采集正确性事实，不是断言状态，更不是 Verdict。

`collection_session_id` 在每次实际采集执行开始、任何 probe 之前创建；同一 sealed request 重放必须
获得新 ID。它与 request seal、collector 类型和 session 内产物引用共同形成 provenance/correlation，
不进入 observation spec 或 `facts_digest`，也不证明来源、时间或执行真实性。只有同一协调执行明确
生成且携带同一 session identity 的 API/Render Evidence，才可称为同一次观察的多个产物；不同 session
不得因 request 相同而混合。P2/P3 若无法由 Core 或单独兼容合同验证该关系，必须停止 handoff，不能
由插件自行挑选后生成 `api_render_match=true`。

每份产物至少保存以下 session 投影；session manifest 或 handoff 若引用多个产物，还必须绑定其精确
EvidenceArtifact SHA-256，不接受“同目录”“最近一次”或仅 request 相同的隐式配对：

```text
collection_session_identity.session_id
collection_session_identity.request_seal_digest
collection_session_identity.collector_role
collection_session_identity.collection_started_at
collection_session_identity.collection_completed_at
collection_session_identity.collection_elapsed_ms
```

采集状态只允许：

| 状态 | 含义 |
| --- | --- |
| `COMPLETE` | 请求的 probe 都取得可用来源事实 |
| `PARTIAL` | 一部分 probe 有事实，另一部分缺失或不可判 |
| `ERROR` | 采集器未能形成该 probe 的可信事实 |
| `NOT_APPLICABLE` | 请求明确声明该 probe 不适用 |

这些词只描述采集覆盖，不映射到 Core `ExecutionStatus` 或 `Verdict`。

## 6. 规范化与确定性

- 响应只保留合同白名单字段；未知新增字段默认忽略。原始 API 版本、客户端版本、解析器实现版本和
  采集器版本进入 provenance，不凭版本号变化自动制造新的事实身份。
- 列表使用稳定事实身份排序；重复项不得静默覆盖。两个同名 check 若 producer、app、workflow、job
  或来源类型不同，必须保留为两个观察；若平台没有暴露足够身份，必须显式记录歧义，不能只按名称合并。
- volatile headers、ETag、请求耗时、采集时间、速率窗口、request identity、collection session identity、
  access mode 与 Collector Policy 进入 provenance 或 metadata，不参与 `facts_digest`。
- `facts_digest` 必须只对如下语义投影计算 canonical SHA-256：

  ```text
  canonicalization_profile
  observation_spec_digest
  normalization_semantics_version
  normalized source coordinates
  normalized fact values
  ```

  该投影排除 `facts_digest` 字段自身、request envelope seal、request ID、collection session ID、采集
  时间、ETag、原始采集机制版本以及 timeout/retry 等运行策略，避免循环摘要和实例噪音。
  `facts_digest` 相等只说明这份语义投影
  相同，不证明采集完整、来源真实、Evidence 相同或 Plan 已满足；coverage、errors 与冲突仍须独立保留。
- `normalization_semantics_version` 属于事实身份。若字段含义、缺省规则、单位、排序身份、冲突折叠或
  规范化投影改变，必须升级该版本；仅 API、客户端或解析器实现升级，而规范化含义与输出事实未变时，
  不得仅凭实现版本改变 `facts_digest`。若上游 API 语义变化影响规范化含义，则必须同时升级
  `normalization_semantics_version`。
- 相同 observation spec 与同一来源快照应生成相同 canonical facts；不同请求实例、时间或非语义
  Collector Policy 不能制造事实漂移。Policy 若导致覆盖不同，应由 coverage / errors 表达，而不是
  改写已经取得的同一来源事实。
- 现有 Core 已对脱敏后的完整 Evidence 0.1 文档计算 `ImportedEvidence.sha256`，并以 `sha256` 写入
  Evidence manifest/report；P 轨沿用它作为 Evidence artifact identity，不在 Evidence 文件内部再造一个
  自引用 `evidence_digest`。请求实例、Collector Policy、`captured_at`、source metadata 和 provenance
  只要被完整保留在 Evidence 文档中，就会使两次独立采集产生不同 artifact SHA-256；Bundle manifest
  另行封存 Evidence、附件和清单文件。

因此允许且预期：

```text
same facts_digest + different Evidence artifact SHA-256
same request instance + multiple Collection Sessions
same Collection Session + one or more explicitly bound Evidence artifacts
same fact identity + different Core Run / execution identity
```

这三种关系不能被去重逻辑、缓存或报告层压成一条记录。简写为：

```text
Same Fact != Same Observation != Same Request
Fact Identity != Evidence Artifact Identity != Execution Identity
```

身份对照如下；任一行的相等都不能替代下一行的证明：

| 身份 | 规范输入或现有坐标 | 相等最多说明 | 不能推出 |
| --- | --- | --- | --- |
| Observation spec | spec version、规范化坐标、probe 与投影 | 观察的问题相同 | 来自同一 Plan 或 request |
| Collector Policy | API/public mode、timeout、retry 与资源边界 | 有界采集策略相同 | 事实相同或验收通过 |
| Request instance | 排除 seal 自身的完整 request envelope | 同一封存请求字节 | 同一次观察或执行 |
| Collection session | 新 session ID、request seal 与本次协调执行上下文 | 同一次实际采集会话 | 事实相同、可信时间或 Plan 满足 |
| Fact | observation spec、规范化语义版本与规范化事实 | 语义事实投影相同 | Evidence 完整、来源真实或 Plan 满足 |
| Evidence artifact | Core 现有的脱敏完整 Evidence 文档 SHA-256 | 保留的具体 Evidence 字节相同 | 采集前事实真实或外部时间可信 |
| Execution | Core Run identity 与对应 Bundle 上下文 | 同一运行坐标 | request、fact 或 Evidence 可互换 |

每个 probe attempt 还必须记录稳定递增的采集序号、自己的 `observed_at`、实际请求操作数、返回资源
标识，以及 API 可用时的 ETag 或等价来源标识；Evidence 外壳记录 `collection_started_at` 与
`collection_completed_at`，并使用同一进程内的 monotonic clock 记录非负整数
`collection_elapsed_ms`。墙钟字段只说明采集器何时观察，不是 GitHub 事件发生时间、可信时间戳或
外部真实性锚，也不参与事实摘要；最大采集窗口只能比较 `collection_elapsed_ms`，不能用两个 wall
clock timestamp 相减。多次调用或有界重试之间若资源发生变化，必须保留每次观察及冲突；不得只保存
“最后一次”，也不得拼成一个从未同时存在过的“GitHub 原子快照”。即使 Plan 的窗口约束满足，Core
仍不能宣称平台提供了原子读。

## 7. 权限、凭据与网络

默认模式匿名读取公开资源。GitHub 文档说明公开资源的部分检查接口可不认证读取；需要认证时，只接受
运行时进程环境或调用方内存传入的可选 token，优先 fine-grained token，并限制到实际 probe 所需的
只读权限。token 不得出现在 CLI 参数、URL、配置文件、Bundle、异常文本或测试快照中。Evidence 必须
记录 `access_mode=ANONYMOUS|AUTHENTICATED_READ_ONLY`，并在端点能安全判断时记录可见性/权限类别；
不得记录 token、Authorization 值、账号秘密或可用于重放认证的信息。`404` 的解释必须关联本次 access
mode，不能脱离认证上下文宣称资源不存在。

实现必须：

- 设置 `Accept`、稳定 `User-Agent` 与显式 `X-GitHub-Api-Version`；
- 串行、有界请求，不做组织级并发扫库；
- P1 0.1 首片禁用 conditional GET，不发送 `If-None-Match` / `If-Modified-Since`，也不把本地缓存当事实；
- 遵守 `retry-after`、`x-ratelimit-remaining` 和 `x-ratelimit-reset`，有界退避后停止；
- 区分 `401`、权限不足、主/次限流、网络超时、服务器错误和数据校验错误；
- 不把 GitHub request headers、token 或原始响应 body 写入持久产物。

### 7.1 `304 Not Modified` 与旧证据

`304` 只表示请求表示相对于所带 validator 未变化，本身没有可重新规范化的当前 response body。
因此 P1 0.1 选择禁用条件请求，以最小请求量换取来源清楚的 `200` 事实。若后继版本启用缓存，必须先
另立合同并同时绑定：完全相同的资源坐标与请求参数、matching ETag/Last-Modified、精确旧
EvidenceArtifact SHA-256、旧 `facts_digest`、旧 normalization/profile identity，以及本次 `304` 的
probe provenance；任一项缺失只能形成缺证据/采集错误，不能重建当前事实。意外收到 `304` 时 fail
closed，不沿用“最近一次”缓存。

### 7.2 Tag 与 Release 解引用

`refs/tags/<name>` 可能直接指向 commit（lightweight tag），也可能指向 annotated tag object。Collector
必须保存 `ref_target_sha`、每一步 `object_type/object_sha`、有界 peel chain 和最终
`peeled_commit_sha`。首片只接受最终解引用为 commit 的目标；循环、超过上限、tree/blob 或无法读取的
对象记录为歧义/错误，不把 tag object SHA 与预期 commit 直接比较。Release 的 `target_commitish` 是
平台 metadata，不替代 tag ref 与最终 commit 的实际解引用结果。

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
- sealed Plan 固定验收期望；由它派生的 request 固定观察坐标。两者都不是其内容诚实的证明，request
  也不能成为第二份期望权威。
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
| 人的前提或目标存在歧义、遗漏或后续争议 | Claim owner / Seal authority | 版本化保存声明、反例、未决项与确认过程 | 代替提出者裁定观点终极正确 |
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
- Human / AI Plan drafter 只负责把目标起草成可评审合同并暴露未决项；起草身份不自动获得 Seal 权，
  也不能把自己的推断写成已经被 claim owner 确认的前提；
- 现实拥有最终真相，且现实可能模糊、不完整、随时间变化、相互冲突或当前不可判；
- VeriTrail 拥有声明、证据来源、验收过程、规则版本和 Verdict 推导的完整性，不拥有世界真相；
- 插件只观察声明范围内的平台事实，不能评价人的想法，也不能扩大或重写其验收目标；
- AI 或执行 Agent 负责在授权边界内忠实质疑、规划和执行；发现与前提冲突的证据时必须报告，却
  不能擅自改写人的目标、扩大现实权限或把自己的世界模型冒充最终真值。

0.1 不建立身份认证或电子签名系统。角色分离首先是权限与流程纪律：Plan 的 SHA-256 seal 证明内容
未变，不证明某个现实身份亲自批准。P1 若不能在不修改 Core 公共 Schema 的前提下保存 drafter、确认
过程与 Seal authority 的可区分审计引用，必须停止并另开兼容合同；不得把一个自由文本姓名或 request
字段冒充已认证授权。

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
Plan drafter owns draft fidelity, not Seal authority
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
| request 的 `plan_digest` 不匹配或无法证明机械派生 | 网络前预检错误，不启动 probe | `PENDING` 或 `INCONCLUSIVE`；不得选择任一份期望继续 |
| 两个 check 显示名相同但 producer/workflow 不同 | 分别保留身份与来源；身份不足时记录歧义 | 不能仅按名称判定 required check 已满足 |
| 采集窗口内平台状态发生变化 | probe 级时间、操作数、来源标识与冲突 | 不能把组合 Evidence 描述为原子快照 |
| API 与 Render 来自不同 collection session | 分别保留 session identity，拒绝冒充同一次观察 | 不得生成跨源一致性结论 |
| wall clock 在采集中跳变 | 保留墙钟事实；窗口只使用 monotonic `collection_elapsed_ms` | 不得用墙钟差值制造超时或通过 |
| Plan/Assertion 只能靠插件预计算布尔值才能表达 | 兼容门失败，不启动 Collector | 保持 `P1_NOT_STARTED`，另立 Core 兼容合同 |
| canonicalization profile 未知或测试向量不匹配 | 联网前预检错误 | 不得计算或比较摘要 |
| 首片意外收到 `304` | `ERROR`/缺事实，并保留无秘密 provenance | 不得从未绑定缓存重建当前事实 |
| annotated tag object SHA 与 commit SHA 不同 | 保存 ref/object/peel chain，比较 `peeled_commit_sha` | 不得把 object SHA 差异直接判为 wrong tag |
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
19. observation request 含与 Plan 重复或冲突的 `expected.*` 时必须拒绝；正确请求必须分别绑定
    `plan_digest`、派生规则版本与 Collector Policy digest，且由实际 sealed Plan 可确定性重新派生
    相同观察坐标；只有 digest 字符串相同而重算结果不同也必须在联网前拒绝。Collector Policy 改变
    运行边界时生成新 request envelope seal，但不得改变 observation spec digest 或相同 Evidence 的
    验收语义。
20. AI 或另一位 Human 起草 Plan 的案例中，drafter 未取得明确 Seal authority 时不能封存或启动采集；
    起草者身份、确认者与最终 Seal 决定必须可区分。
21. 两个 display name 相同但 producer/app/workflow/source identity 不同的 check 必须保持两个事实；
    身份字段不足时得到显式歧义，而不是错误满足 required set。
22. 一个采集窗口内 main、PR、Release 或 Pages 发生变化的夹具，必须保留 probe 级 `observed_at`、
    实际操作数、来源标识与窗口；报告不得声称这些结果构成同一时刻的平台原子快照，也不得把本地
    `observed_at` 表述为可信时间戳或平台事件时间。
23. 对同一 observation spec 独立采集两次且规范化事实相同的夹具，必须得到相同 `facts_digest` 和不同
    Evidence artifact SHA-256；两份 Evidence 与两个 Core Run 不得被去重。
24. 只改变 API/客户端/解析器实现版本、保持语义版本与规范化事实不变时，`facts_digest` 必须不变，
    provenance 与 Evidence artifact SHA-256 必须变化。
25. 只改变 `normalization_semantics_version` 时，`facts_digest` 必须变化，即使输出字段的表面 JSON 值
    恰好相同。
26. 只改变 Plan 中与观察规格无关的 revision 内容、并机械派生出完全相同 observation spec 时，
    `observation_spec_digest` 与同来源的 `facts_digest` 必须不变；request seal、Plan binding 与 Evidence
    artifact SHA-256 必须变化。
27. 同一 sealed request 重放两次时必须产生两个 `collection_session_id`；若规范化事实相同，
    `facts_digest` 可相同，但 session identity 与 Evidence artifact SHA-256 必须不同。
28. API Evidence A 与 Render Evidence B 的 request 相同但 collection session 不同时，不得被称为同一次
    观察或生成跨源匹配结果；同一协调执行的多个产物则必须携带相同 session identity。
29. 合成 wall clock 前跳/后跳时，`observed_at` 保留实际观察值，最大窗口只依据 monotonic
    `collection_elapsed_ms`；时钟跳变不得制造窗口 `PASS/FAIL`。
30. 使用当前 Plan validator 与 Verdict evaluator 的首片夹具必须直接对规范化 commit/ref、merge、
    required check、tag/release 事实形成断言；若必须由插件输出 Verdict-like boolean，兼容门失败。
31. GitHub Plan 夹具必须按 PRIMARY variable、baseline、load model 等字段原义成立；仅为 Schema 通过而
    编造占位实验事实时，兼容门失败并保持 `P1_NOT_STARTED`。
32. `veritrail-json-c14n/1` 的四个冻结向量必须在受支持 Python 上逐字节与 SHA-256 一致；未知 profile、
    `NaN`/无穷或首片浮点投影必须在联网前拒绝。sealed Plan 的 `plan_digest` 必须等于排除 `seal` 的
    canonical 内容摘要，而不是整个 Plan 文件摘要。
33. P1 首片不得发送 conditional GET；意外 `304` 或只有 validator 而没有精确旧 Evidence SHA、旧
    `facts_digest` 和同坐标绑定时，必须缺证据/fail closed，不能复用最近缓存。
34. lightweight tag 与 annotated tag 指向同一 commit 的夹具必须得到相同 `peeled_commit_sha`，同时保留
    不同 ref/object provenance；错误目标、非 commit 目标和超过 peel 上限必须保持可区分。
35. 匿名与只读认证采集必须分别保留 `access_mode`，同一可见事实可规范化为相同 `facts_digest`，具体
    Evidence provenance/SHA 不同；token、Authorization 和可重放账号秘密必须为零，歧义 `404` 不得当作
    不存在。

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
conditional GET/旧 Evidence 缓存复用、自动定时器、组织级仪表盘、仓库修复、PR 合并、规则集修改、
Release 发布、Pages 部署、跨平台统一 SPI 或通用网页爬虫。后述 GitHub 平台能力需要新合同；外部见证
不因新合同自动进入本产品路线。
