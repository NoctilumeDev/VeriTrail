# Review Attention Pattern Ledger 0.1

## 1. 状态与用途

- 状态：`LEDGER_SCHEMA_CANDIDATE / SEED_SET_CANDIDATE`；
- 冻结策略：R0 冻结记录格式与首批种子；P2–P4 期间 Ledger 保持 append-only/open；
- 目的：把真实工程中发现的认知陷阱沉淀为可复核的审查模式，而不是把一次 bug 修复包装成通用真理；
- 非目标：本账册不确认缺陷、不生成 Core Verdict、不授权自动修复，也不是机器学习训练集承诺。

## 2. 为什么 Ledger 必须与 R0 宪法分离

权威、依赖方向、Artifact 身份和 AI 不得裁决等原则应稳定冻结；现实反例则会随着 P2–P4 继续增加。
若每个新反例都重开 R0，主干会持续漂移；若 R0 一次冻结全部规则，又会把尚未观察的世界假装完整。

因此：

```text
R0 Constitution   stable/frozen
Pattern Ledger    append-only/open
Corpus Snapshot   selected and frozen before R1
```

## 3. Pattern Record Schema

每条记录至少包含：

| 字段 | 含义 |
| --- | --- |
| `pattern_id` | 稳定标识，不因标题润色变化 |
| `status` | `OBSERVED / GENERALIZED / CONTRACT_CANDIDATE / FROZEN_PATTERN / REJECTED` |
| `source_coordinate` | 仓库、精确提交/PR/文档/外部资料坐标 |
| `problem_layer` | Premise / Plan / Authority / Identity / Execution / Observation / Verdict / Delivery / Presentation |
| `suspicious_structure` | 代码或设计中值得人确认的结构 |
| `possible_interpretations` | 至少列出替代、优先、覆盖、叠加等可能语义 |
| `required_evidence` | 需要哪些代码、合同、运行或外部平台语义才能裁决 |
| `minimal_counterexample` | 能推翻当前模型的最小情形 |
| `false_positive_conditions` | 哪些条件成立时该结构其实合理 |
| `detectable_cues` | 将来工具可用于定位的信号，不等于结论 |
| `non_claim` | 本记录明确没有证明什么 |
| `provenance` | 谁在何时基于何证据记录/修订 |

状态只描述模式成熟度，不描述代码缺陷真值。`FROZEN_PATTERN` 表示该模式进入某个精确 Corpus 快照，
不是“所有命中都是 bug”。

## 4. 首批种子模式

| ID | 层 | 可疑结构 | 最小反例 / 人工问题 |
| --- | --- | --- | --- |
| RA-001 | Authority | 两个角色最终写入同一事实 | 谁拥有最终状态？Reporter 是否被误当 authority？ |
| RA-002 | Identity | request/fact/evidence/run 共用摘要或 ID | 同一事实两次独立采集是否被误当同一 Evidence？ |
| RA-003 | Observation | 一个来源成功后跳过其他适用来源 | 现实究竟是 `OR`、优先级，还是 `A + B`？ |
| RA-004 | Observation | 首个成功、exit 0 或 HTTP 200 被推导为完整 | 未支持/未观察范围在哪里？ |
| RA-005 | Observation | 多次 API 读取被描述成原子快照 | 组合事实是否曾在同一时刻成立？ |
| RA-006 | Verdict | Provider 输出 `*_ok` / `passed` 并被直接消费 | sealed 条件与 Core 是否被绕过？ |
| RA-007 | Evidence | 本地时间或不可信时间戳决定事实顺序 | 是否有可信顺序来源或只能保留未知？ |
| RA-008 | Evidence | cache/latest/HEAD 替代精确坐标 | 源已漂移时旧结论为何仍成立？ |
| RA-009 | Pairing | 不同 session/source 的产物被隐式配对 | 它们是否来自同一次有界观察？ |
| RA-010 | Premise | 内部自洽被当作源头前提正确 | 有没有与 sealed premise 冲突的外部事实？ |
| RA-011 | Dependency | “有接口”被当作插件解耦证明 | Core 是否仍认识实现类型或共享其状态？ |
| RA-012 | Presentation | 红黄绿或高分让提案看起来像结论 | 用户能否一眼分清机器提案、严重度与人工决定？ |
| RA-013 | Retry | retry 穿过副作用边界 | 重试是否产生重复写、重复通知或双重结算？ |
| RA-014 | Coverage | 空结果被解释为没有风险 | Provider 是完整执行、部分执行、失败还是不支持？ |
| RA-015 | Policy | AI confidence 被直接映射为审查优先级 | 项目风险政策和模型自信是否被混为一谈？ |
| RA-016 | Instruction | 被审查源码/注释改变了工具行为或权限 | 数据是否被错误提升为控制指令？ |

## 5. 完整样例：Fallback 与 Layering

```yaml
pattern_id: RA-003
status: GENERALIZED
problem_layer: Observation
suspicious_structure: >
  当来源 A 成功或返回空集合时，不再读取来源 B；代码把 B 命名为 fallback。
possible_interpretations:
  - A 与 B 互斥
  - A 优先、B 只在 A 不可用时生效
  - A 覆盖 B
  - A 与 B 同时适用并叠加
required_evidence:
  - 外部系统的官方组合语义
  - 真实 coexistence fixture
  - 空 A + 非空 B fixture
  - 重复要求的来源 provenance 与归一化规则
minimal_counterexample: >
  A 要求 check-a，B 要求 check-b，平台实际同时执行二者；Collector 只保留 check-a。
false_positive_conditions:
  - 合同或平台明确保证 A 与 B 互斥
  - 已证明 A 完整覆盖 B 且保留覆盖来源
detectable_cues:
  - fallback / first-success / else-if / coalesce
  - successful empty collection short-circuits another provider
non_claim: >
  命中结构不自动证明代码错误；它只要求确认外部现实中的组合关系。
provenance: >
  VeriTrail P1 Freeze 前 required checks 的 Rulesets + classic branch protection 反例。
```

## 6. Intake 与提升规则

1. 新发现先以 `OBSERVED` 追加，必须绑定精确来源，不能只写口头印象；
2. 能跨越单个实现、写出最小反例与误报条件后才可升为 `GENERALIZED`；
3. 拟进入未来合同或自动检测前必须升为 `CONTRACT_CANDIDATE` 并完成反向找茬；
4. P4 后选择进入 R1 的条目，以 manifest + digest 形成 `FROZEN_PATTERN` corpus；
5. 被证伪或范围不成立的模式标记 `REJECTED`，保留原因，不删除历史；
6. 任何自动化只输出命中 Evidence/Proposal，不能因为模式已冻结就自动确认缺陷。

## 7. P2–P4 重点收集面

| P 阶段 | 重点反例方向 |
| --- | --- |
| P2 Public Render | API != Render、redirect/navigation、stale page、session correlation、browser provenance、observer effect |
| P3 Core handoff | pairing authority、sufficiency、跨 Evidence 关系、Verdict leakage、错误压平 |
| P4 Plugin release | 安装/卸载边界、发布物 != 工作树、tag/release/assets/public readback、冻结坐标 |

这些方向是观察清单，不是预判 P2–P4 一定存在缺陷。新 Evidence 可以更新模式状态，但不能为了丰富
Ledger 而制造问题或扩大 P 轨范围。
