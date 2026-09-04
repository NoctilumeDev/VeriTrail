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

- GitHub 拥有远端平台原始状态；
- 插件拥有采集过程、规范化事实和来源说明；
- sealed Plan 拥有期望值与适用 probe；
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
| “最新”发生 TOCTOU | 请求固定 expected SHA 与 probe 坐标；所有来源回传实际操作数 |
| `404` 被误判为不存在 | 保留可见性/授权歧义，默认缺证据而非反例 |
| 绿色检查绑错提交或错 context | required set、observed set 与 head SHA 分开保存 |
| API 更新但页面缓存/部署仍旧 | P2 使用未登录真实浏览器形成独立 render evidence |
| 插件状态污染 Verdict | 三套状态命名与所有权分开，无自动映射 |
| token 或私人会话泄漏 | 匿名优先；内存 token；fresh browser context；字段白名单 |
| GitHub API 演进破坏解析 | 固定 API 版本、解析器版本和兼容矩阵 |
| 插件耦合 Core 私有实现 | 独立包、公开 Evidence handoff、Core 无插件导入 |
| 为插件移动 Core 发布坐标 | 独立版本/标签，Core 历史只读 |

## 6. P0 验收事实

P0 已在文档层完成：

- 明确 `P` 轨与 M/E 两轨的关系；
- 固定 P0–P4 的串行阶段和跨级施工停止线；
- 给出 authority、dependency、data、permission、failure 和 cleanup 边界；
- 固定 API Collector 与 Public Render Collector 的双源证据模型；
- 固定请求身份、Evidence 外壳、采集覆盖状态、规范化与 digest 规则；
- 覆盖十三类正负验收场景；
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
4. 先提交独立包的 request/facts schema、解析器与合成正负夹具，再接真实 GitHub；
5. 真实请求严格串行、总量有界，默认匿名，凭据只用于明确需要的只读 probe；
6. Core 0.12.2 全量回归和秘密/路径零泄漏作为 P1 硬门禁。

违反任一项时保持 `P1_NOT_STARTED`，回到合同评审，不以临时代码绕过。
