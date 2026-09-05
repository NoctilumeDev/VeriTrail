# PC1 通用 Acceptance Core 实现与候选事实 0.1

> 状态：`PC1_IMPLEMENTED / NOT_FROZEN / PC2_NOT_STARTED / P1_NOT_STARTED`
>
> 合同来源：[Post-P0 Core 兼容桥合同 0.1](80-p0-core-compatibility-contract.md)
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM`；新增并列路径，不改写既有 Experiment Core

## 1. 本阶段解决什么

PC1 把 PC0 已冻结的非因果验收语义实现为平台无关 Core：一个 sealed `AcceptancePlan` 声明观察
规格、Evidence 要求和有限规则；Core 精确绑定已有 Evidence、解析跨 Evidence operand，并独立产生
`PASS / FAIL / INCONCLUSIVE / PENDING`。它不认识 GitHub、PR、Release、Pages 或任何平台私有字段。

新增公共产品彼此独立：

```text
AcceptancePlan 0.1
  -> exact Evidence binding
  -> sufficiency / integrity / assertion evaluation
  -> AcceptanceReport 0.1
  -> AcceptanceBundle 0.1
```

原有 `ExperimentPlan -> Report -> Bundle` 路径没有被改成联合类型，也没有获得 `plan_kind` 默认值。

## 2. 实现边界

本阶段新增：

- `AcceptancePlan 0.1`、`AcceptanceReport 0.1`、Acceptance Evidence Manifest 0.1 与
  Acceptance Bundle Manifest 0.1 Schema；
- 独立 validator、canonical seal 与 observation spec digest；
- Evidence 0.1 开放 metadata 中 `veritrail_observation` 子合同的严格验证；
- `EXACTLY_ONE` 精确绑定、artifact 复用冲突和绑定歧义检测；
- RFC 6901 operand 解析，以及合同限定的十个 operator；
- sufficiency、integrity 与 assertion 分层裁决和四态 Verdict；
- `acceptance-seal` 与 `acceptance-evaluate` 显式 CLI；
- 原子 AcceptanceBundle 发布、文件摘要、大小/文件数边界和拒绝覆盖。

本阶段明确没有：

- GitHub Collector、浏览器采集、网络访问或凭据处理；
- 通用插件注册中心或动态插件加载；
- Catalog、Workbench、Starter、Comparison、Pairing、Batch 对 Acceptance 产品的支持；
- 旧 Plan/Report/Evidence 顶层 Schema 修改；
- 新版本号、标签、Release 或 P1 启动声明。

## 3. 权威与失败语义

sealed Plan 是期望的唯一权威。Evidence 只提供观察事实和来源；插件式字段即使名为 `passed` 或
`match`，也不能覆盖 Core 规则。Core 使用 `evidence_type + plan_digest + observation_spec_digest`
绑定 Evidence，并在 Report 中保留解析值与具体 Evidence SHA-256。

裁决优先级固定为：

1. 绑定歧义、cardinality 冲突、artifact 复用、metadata 合同错误、规则类型错误或 integrity 失败
   得到 `INCONCLUSIVE`；
2. 其余 decisive assertion 为假得到 `FAIL`；
3. Evidence 缺失、coverage 不完整、sufficiency 不满足、decisive rule 未求值或执行未完成得到
   `PENDING`；
4. 只有前述条件均不存在时得到 `PASS`。

因此，确定的反证不会被无关缺证据降格为 `PENDING`，而完整性错误也不会被表面上的 decisive false
伪装成可信 `FAIL`。

## 4. 身份分层

PC1 保持以下身份互不替代：

```text
Plan identity
!= Observation spec identity
!= Normalized fact identity
!= Evidence artifact identity
!= Evaluation identity
```

Core 验证并保留 adapter 提供的 `facts_digest`，但不知道领域规范化语义时不擅自重算。可选摘要只有
满足小写 SHA-256 语法才进入 Acceptance manifest；畸形 metadata 仍由 evaluator 明确裁决，而不会把
非法摘要复制成新产物的结构性噪声。

## 5. 当前验证事实

PC1 定向合同套件覆盖：

- Acceptance 与 Experiment 双向拒绝、旧 0.1–0.7 代表 Plan digest 不变；
- spec digest 的语义包含项与非语义排除项；
- 未知但结构合法的 adapter contract 可封存，畸形 contract/pointer/浮点/个人路径拒绝；
- exact binding、错误 Plan/spec digest、cardinality、复用与 metadata 负例；
- 跨 Evidence 比较、十个有限 operator、严格类型、缺路径和 `exists` 的差异；
- 四态 Verdict 优先级、OBJECTIVE 不覆盖 decisive 结果、Verdict-like Evidence 字段不受信任；
- 独立 Bundle 文件名、逐文件摘要、拒绝覆盖、显式 CLI 与旧入口拒绝；
- 旧 Catalog 不误收 AcceptanceBundle，而是按旧语义留下不支持问题。

本地候选已按串行顺序完成：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| 全 Core 普通模式 | `380/380` | `380/380` |
| 全 Core `-O` 模式 | `380/380` | `380/380` |
| Starter 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring Skill 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring DRAFT 真实链 | 两个 preset `PASS` | 两个 preset `PASS` |

其中 PC1 定向合同测试为 `32/32`。四份 JSON Schema 已通过 Draft 2020-12 meta-schema 检查，实际生成
的 sealed Plan、Report、Evidence Manifest 与 Bundle Manifest 也逐份通过对应 Schema。双 Python
wheel 构建成功并确认包含三个 PC1 runtime module。Workbench 保持 `172/172`、零警告 lint、类型检查
与生产构建通过，依赖审计为零漏洞。

这些仍是 PC1 工作树上的实现候选证据，不是 PC2 对精确提交完成的全消费者、正负 Bundle 独立复算、
干净安装和远端冻结证据。

## 6. 停止线

PC1 完成后停止扩张。下一项只能是 PC2：从一个精确可寻址的 PC1 提交，串行完成双 Python、普通与
优化模式、全 Core 与既有消费者回归、新 Acceptance 正负 Bundle 复算、敏感信息和清理门禁，再决定
是否冻结或发布。

在 PC2 达到 `FROZEN` 前：

- P1 必须保持 `P1_NOT_STARTED`；
- 不得创建 GitHub Collector 或联网探针；
- 不得让插件导入 Core 私有符号；
- 不得把本实现候选描述成已发布、已兼容或生产可用能力。
