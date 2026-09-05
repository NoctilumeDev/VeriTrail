# P0 GitHub Evidence Plugin 架构评审与冻结事实

> 状态：`FROZEN / DESIGN_ONLY / NO_RUNTIME_CLAIM`
>
> 日期：`2026-09-05`
>
> 审查对象：文档 77–79；未创建插件实现、Schema、CLI、CI、标签或 Release

## 1. 评审问题

P0 只回答：GitHub 外部平台事实能否作为独立插件被采集，并在不重开 Core、不污染入口层、不让采集器
获得裁决权的前提下，进入 VeriTrail 的现有证据链。

结论为 **可以进入 P1 施工准备，但不能把 P0 描述为插件已经可用**。

## 2. 分轨裁决

| 候选 | 裁决 | 原因 |
| --- | --- | --- |
| 继续命名 M15 | 拒绝 | 会重开 M0–M14 冻结历史，并把平台适配误写为 Core 能力 |
| 并入 E4 | 拒绝 | Starter/Skill 负责合同入口，不拥有远端平台观察 |
| 建第十个独立仓库 | 当前拒绝 | 首片规模不足以抵消治理、版本与展示成本；独立包已足够隔离 |
| 在 VeriTrail 内开 P 轨独立插件 | 接受 | 方法、证据与裁决可复用，同时版本、目录和所有权仍能分离 |

P0 因此冻结为 `P` 轨起点。它与 M14、E3 并列存在，不是任何一条历史线的后继状态。

## 3. 架构一致性审查

### 3.1 权威边界

- GitHub 拥有其平台对外暴露的远端状态；
- 插件拥有采集过程、规范化事实和来源说明；
- Claim owner / Seal authority 拥有最终 Seal 决定；Human / AI Plan drafter 只拥有草稿忠实性；
- sealed Plan 是期望值、required set 与适用 probe 的唯一权威；它派生 request 的观察坐标；
- versioned Collector Policy 只拥有 API 版本、超时和重试等运行边界；request 分别绑定 Plan 与 Policy，
  Policy 不得携带验收语义；
- Core 拥有 ExecutionStatus、Assertion 与 Verdict；
- Workbench 只读。

没有两个组件共同拥有同一最终事实。插件可以生成 derived alignment fact，但没有 `PASS/FAIL` 写权。

### 3.2 依赖边界

```text
GitHub API / public browser
              |
              v
     GitHub Evidence Plugin
              |
       Evidence 0.1 file
              |
              v
       VeriTrail public Core
              |
              v
      Read-only Workbench
```

Core 不反向依赖插件；插件不导入 Core 私有实现；API Collector 与 Browser Collector 也不共享登录态
或隐式全局缓存。组内允许围绕单一职责高内聚，组间只通过版本化请求和 Evidence 连接。

### 3.3 状态边界

以下状态保持分离：

```text
collector coverage: COMPLETE / PARTIAL / ERROR / NOT_APPLICABLE
Core execution:      PLANNED / RUNNING / COMPLETED / ABORTED / ERROR
Core verdict:        PASS / FAIL / INCONCLUSIVE / PENDING
```

不存在从 collector coverage 到 Verdict 的固定映射。尤其 `ERROR` 不等于 `FAIL`，API success 也不等于
public render success。

### 3.4 信任边界

P0 明确区分 `Consistency / Authenticity / Truth`。API Collector 与 Public Render Collector 虽然独立
采集、独立成证，但都观察 GitHub 同一平台权威；它们是两个观察面，不是两个独立信任根。插件是
观察者，Core 是裁决者，sealed Plan 是预期坐标的所有者；三者均不能证明首次封存前的上游事实未被
伪造，也不能把 GitHub 平台级共同故障转化成外部反证。

因此 0.1 的最大正向表述是：在声明的 GitHub 信任域、采集时间和 sealed Plan 下，指定平台坐标与
所需证据一致。任何“来源真实”“现实命题真实”“不存在事前造假”的结论都越过 P0 合同。评审收束语
为：**它防的是漂移，不是阴谋。**

### 3.5 认识论边界

P0 进一步区分 Verification Correctness 与 Specification Correctness。sealed Plan 拥有被检查的声明
和验收条件，不拥有观点的终极真值；Core 可以确定性回答 Evidence 是否满足这些条件，却不能证明
Plan 理解了提出者真正的问题或覆盖了现实的全部前提。

提出者拥有 claim，现实拥有真相，VeriTrail 只拥有裁决纪律。这里“不拥有真相”不等于“不负责
不确定性”：未知、冲突、缺证据与不可归因必须原样保留，不能被插件、AI、Core 或 Workbench 压成
确定答案。Agent 仍须报告它发现的前提冲突，但只能把决定权交还提出者，不能借此改写目标。Seal 前
的人工确认、反例或独立 challenge 只能降低理解偏差，不能获得真理裁决权。

评审没有把人为蓄意构造、人的前提选择或歧义和 Agent 诚实误解混成同一条：前者属于信任上限，
后两者属于认识论与规格边界。它们可以呈现相同的“内部全绿”外观，但需要不同的责任回查。P0 只
承诺保存差异、暴露冲突并把失败定位到 Premise / Plan / Execution / Observation / Verdict 之一，
不承诺根治源头问题。

## 4. 与既有基线的兼容审查

- 现有 `evidence.schema.json` 允许版本化通用 `evidence_type` 与 facts；P0 只设计相互独立的
  `platform.github.api.snapshot` 与 `platform.github.public-render`，没有修改 Schema。
- `docs/01-evidence-model.md` 已要求证据、执行状态和裁决分离；插件合同没有另造裁决体系。
- `docs/02-architecture.md` 已把技术栈差异交给适配器，并规定适配器失败不能修改 Core 裁决语义；P 轨
  把该原则落实为独立产品边界。
- `docs/65-github-public-presentation-facts.md` 是一次性公共展示收束事实，不是可复用插件证明；P0 没有
  倒写该历史。
- M0–M14、E0–E3、Core `v0.12.0`/`v0.12.1`/`v0.12.2` 与入口层全部标签保持不可移动。

若 P1 证明通用 Evidence 不能严格承载插件事实，必须停止并另开 Core 兼容合同；不能在插件里静默
放宽 Schema 或复制 Core 验证器。

## 5. 风险与预先裁决

| 风险 | P0 裁决 |
| --- | --- |
| 采集器顺手修 GitHub | 只读接口；没有写 token、写 endpoint 或 mutation |
| Plan 与 request 同时持有期望 | Plan 是唯一期望权威；request 绑定 `plan_digest` 和派生规则版本，联网前从实际 Plan 重算，只携带观察坐标 |
| 整个 Plan digest 污染 observation/fact identity | observation spec 只摘要自身版本、规范化坐标与投影；Plan 与 derivation 只进入 request binding/envelope |
| Collector Policy 偷带通过条件 | Policy 只拥有 API 版本、超时、重试等运行边界，并独立绑定 digest；不能改变 Core assertion |
| 现有 Plan 无法无歧义表达 GitHub 坐标 | P1 先冻结 Plan-to-request 映射夹具；若需自由文本私约或 Core Schema 变更，停止并另立兼容合同 |
| request ID 或超时策略制造“事实漂移” | observation spec、Collector Policy 与 request envelope 三种摘要分开；`facts_digest` 不绑定实例噪音 |
| `facts_digest` 与 Evidence 文件摘要混用 | 事实语义投影使用独立 `facts_digest`；具体证据产物沿用 Core 的 EvidenceArtifact SHA-256，禁止文件内自引用摘要 |
| 所有版本号都被塞进事实身份 | API/客户端/解析器实现版本属于 provenance；只有规范化含义变化才升级 `normalization_semantics_version` |
| 两次采集看到同一事实就被错误去重 | 允许 facts digest 相同而 Evidence artifact SHA-256、request 与 Core Run 不同；报告必须保留每次观察 |
| Plan drafter 自动获得 Seal 权 | claim owner / Seal authority 与 Human/AI drafter 分列；起草不能代替确认 |
| “最新”发生 TOCTOU | 请求固定 target SHA 与 probe 坐标；所有来源回传实际操作数 |
| 多次 API 调用拼成不存在的同刻状态 | 保留 probe 级 `observed_at`、来源标识和 collection window；明确不是平台原子快照 |
| 本地观察时间或 Plan digest 被包装成更强证明 | `observed_at` 只描述采集器窗口；digest 只证明内容绑定，不证明可信时间或现实身份 |
| `404` 被误判为不存在 | 保留可见性/授权歧义，默认缺证据而非反例 |
| 绿色检查绑错提交、错 context 或同名异源 | required set、observed set、head SHA 与 producer/app/workflow/source identity 分开保存；显示名不作为唯一身份 |
| API 更新但页面缓存/部署仍旧 | P2 使用未登录真实浏览器形成独立 render evidence |
| 插件状态污染 Verdict | 三套状态命名与所有权分开，无自动映射 |
| token 或私人会话泄漏 | 匿名优先；内存 token；fresh browser context；字段白名单 |
| GitHub API 演进破坏解析 | 固定 API 版本、解析器版本和兼容矩阵 |
| API 与公开页面被误当成两个独立权威 | 明确同属 GitHub 共同信任域；双源只增加漂移可见性，不增加独立见证 |
| 首次封存前的内部自洽造假被误写为真实 | 正向结论必须带信任域；Core 只裁决一致性，不推断来源或现实真实性 |
| GitHub 平台级共同故障或失陷 | 保留共同故障域；本链不声称能内部反证，外部锚由使用方在产品之外治理 |
| AI 诚实地把误解的问题做成完整闭环 | 区分验证与规格正确性；`PASS` 只绑定 sealed 条件，不声明用户真实目标已被证明达成 |
| “人负责前提”被 Agent 当成沉默免责 | 发现冲突必须报告；人决定是否重写并重新 Seal，Agent 不忽略也不越权改题 |
| 系统为避免“不知道”而补写答案 | UNKNOWN、冲突、缺证据与不可归因保持可见，沿用 Core 的 PENDING/INCONCLUSIVE 规则 |
| 证据已定位到 Plan/交付层却继续强改代码 | 按 Verdict→Observation→Execution→Plan→Premise 反向排查，不跨层制造修复 |
| 插件耦合 Core 私有实现 | 独立包、公开 Evidence handoff、Core 无插件导入 |
| 为插件移动 Core 发布坐标 | 独立版本/标签，Core 历史只读 |

## 6. P0 验收事实

P0 已在文档层完成：

- 明确 `P` 轨与 M/E 两轨的关系；
- 固定 P0–P4 的串行阶段和跨级施工停止线；
- 给出 authority、dependency、data、permission、failure 和 cleanup 边界；
- 固定 API Collector 与 Public Render Collector 的双源证据模型；
- 固定 Plan 单一期望权威、Collector Policy 运行边界、三层请求摘要、Evidence 外壳、采集覆盖状态、
  规范化与 digest 规则；
- 固定 `facts_digest` 与现有 EvidenceArtifact SHA-256 的不同所有权，区分语义规范化版本与采集实现
  provenance，并拒绝自引用摘要和跨身份去重；
- 固定 drafter / Seal authority 分离、check identity 与非原子采集窗口；
- 明确承诺后完整性与承诺前真实性的分界，以及 API/公开页面的共同信任域；
- 将“防君子，不防小人”限定为工程信任模型，并把 GitHub 之外的外部锚列为产品非目标；
- 明确观点真值不属于 VeriTrail 权威，并要求未知、冲突与不可判保持可见；
- 覆盖二十六类正负验收场景：既约束信任与认识论上限，也专门防止双重期望权威、drafter 越权、
  同名 check 误合并、多次调用伪装成原子快照和事实/证据身份混用；
- 引用 GitHub 官方 REST API、认证、版本、限流和各资源接口文档；
- 明确 Codex Security 深扫与攻击路径分析不在本阶段范围内。

P0 没有可运行能力，因此没有宣称单元测试、网络采集、真实浏览器、性能、兼容性或发布通过。合入前
只执行文档链接、`git diff --check`、敏感信息、历史坐标和无运行代码变化检查；受保护主线与公开
README 读回是最后的冻结证据。

## 7. P1 进入门

P1 开始前必须重新确认：

1. P0 文档已在受保护 `main` 可公开读回；
2. 工作树从最新 `origin/main` 创建，且没有继承历史本地补丁；
3. 只实现 API Collector，不提前进入浏览器、Core handoff 或发布；
4. 先冻结 Plan-to-request derivation map，证明现有 Plan 可无歧义派生；再提交独立包的 request/facts
   schema、Collector Policy、解析器与合成正负夹具，最后才接真实 GitHub；
5. 真实请求严格串行、总量有界，默认匿名，凭据只用于明确需要的只读 probe；
6. 输出与示例只使用带 GitHub 信任域的结论语言，不把双观察面包装成双权威；
7. 插件与示例不得评价提出者观点，只能报告 sealed 条件与 Evidence 的关系，并保留不确定性；
8. request schema 不含独立 `expected.*`，必须绑定 `plan_digest`、派生规则与 Collector Policy digest；
   坐标可从实际 sealed Plan 确定性派生，Policy 不含验收语义；
9. Plan drafter 与 Seal authority 可区分，未获 Seal 的草稿不能启动采集；现有 seal 不冒充身份认证；
10. check identity 不以显示名为唯一键；probe 级时间、操作数和 collection window 必须保留；
11. observation spec、Collector Policy 与 request envelope 摘要职责分开；spec digest 不包含整个 Plan
    或派生规则身份；`facts_digest`、现有 EvidenceArtifact SHA-256 与 Core Run identity 也分别拥有事实
    语义、具体证据产物与执行身份；
12. `normalization_semantics_version` 与 API/客户端/解析器实现 provenance 分开，且同事实的独立采集
    不得被去重；
13. Core 0.12.2 全量回归和秘密/路径零泄漏作为 P1 硬门禁。

违反任一项时保持 `P1_NOT_STARTED`，回到合同评审，不以临时代码绕过。

## 8. 受保护主线与公开读回闭环

首轮 P0 文档经 [PR #21](https://github.com/NoctilumeDev/VeriTrail/pull/21) 受保护合入，merge commit 为
`8944549a080e331a7021337e40de5c8accc49649`。随后在真实 GitHub 公开渲染页逐项读回：

- README 的 P0 入口、Trust Ceiling、Epistemic Ceiling 与 `P1_NOT_STARTED` 停止线；
- 文档 78 的第 8、9 节、三条风险路径、人机责任链和外部锚产品非目标；
- 本评审页的认识论边界、P0 非运行声明和 P1 进入门。

这次读回使用最终网页渲染而非 API 内容代替，因此关闭了 P0 的最后展示层门禁；它不改变“API 与公开
页面同属 GitHub 共同信任域”的结论，也不等于 P1 已经开始。
