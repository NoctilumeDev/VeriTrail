# Review Attention Pattern Ledger 0.2

## 1. 状态与用途

- 状态：`LEDGER_SCHEMA_FROZEN / SEED_SET_FROZEN / LEDGER_OPEN`；
- 冻结策略：R0 冻结记录格式与首批种子；P2–P4 期间 Ledger 保持 append-only/open；
- 目的：把真实工程中发现的认知陷阱沉淀为可复核的审查模式，而不是把一次 bug 修复包装成通用真理；
- 非目标：本账册不确认缺陷、不生成 Core Verdict、不授权自动修复，也不是机器学习训练集承诺。

0.1 的矛盾版本仍可由 Git 历史在 `main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3` 精确读回；0.2 是在
P2 尚未开始、尚无后继 PatternRecord 的零迁移窗口中完成的显式 Schema 修正，不声称 0.1 从未存在。
0.2 重新冻结后，append-only 规则适用于所有物化 revision。

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
| `record_revision` | 同一 `pattern_id` 下从 1 开始、严格递增的不可变记录版本 |
| `supersedes_digest` | 上一 revision 的 `record_digest`；首个 revision 为 `null` |
| `record_canonicalization` | 摘要规范化语义；0.2 固定为 `veritrail-json-c14n/1`，实现须通过其冻结向量但不得导入 Core 实现 |
| `record_digest` | 当前不可变记录的 SHA-256；规范化输入包含其余完整记录并排除 `record_digest` 自身，避免自引用 |
| `status` | `OBSERVED / GENERALIZED / CONTRACT_CANDIDATE / FROZEN_PATTERN / REJECTED` |
| `source_coordinate` | 仓库、精确提交/PR/文档/外部资料坐标 |
| `problem_layer` | Premise / Plan / Authority / Identity / Execution / Observation / Verdict / Delivery / Presentation |
| `taxonomy_version` | `problem_layer` 与 `pattern_class` 的分类语义版本 |
| `pattern_class` | 正交的机制/陷阱类别，例如 Pairing / Dependency / Retry / Coverage / Policy / Instruction；开放但受 `taxonomy_version` 约束 |
| `suspicious_structure` | 代码或设计中值得人确认的结构 |
| `possible_interpretations` | 至少列出替代、优先、覆盖、叠加等可能语义 |
| `required_evidence` | 需要哪些代码、合同、运行或外部平台语义才能裁决 |
| `minimal_counterexample` | 能推翻当前模型的最小情形 |
| `false_positive_conditions` | 哪些条件成立时该结构其实合理 |
| `detectable_cues` | 将来工具可用于定位的信号，不等于结论 |
| `non_claim` | 本记录明确没有证明什么 |
| `provenance` | 谁在何时基于何证据记录/修订 |

`problem_layer` 回答“问题发生在哪一层”，`pattern_class` 回答“它是哪类机制或陷阱”，两者不得混用。
状态只描述该 revision 的模式成熟度，不描述代码缺陷真值。`FROZEN_PATTERN` 表示该 revision 被选入某个
精确 Corpus 快照，不是“所有命中都是 bug”。

任何状态提升、证伪或内容修订都必须追加新 revision，并令 `supersedes_digest` 指向当时唯一链头；不得
原地修改旧 revision。第二个并发 successor 不得被静默选为“当前状态”：若 Git 合并形成分叉，Ledger
必须显式报告冲突，相关模式在修复前不得进入 Corpus。Corpus Manifest 必须绑定精确仓库提交、manifest
digest，以及每个条目的 `pattern_id + selected_record_digest`：

```text
Ledger History != Corpus Selection
```

## 4. 首批种子模式

下表是 Seed Set 的人类可读投影，不冒充未来序列化的 PatternRecord；机器化时每个 seed 必须物化为包含
全部 Schema 字段的 revision。表内“层”严格使用 `problem_layer` 枚举，“模式类”单独表达机制：

| ID | 层 | 模式类 | 可疑结构 | 最小反例 / 人工问题 |
| --- | --- | --- | --- | --- |
| RA-001 | Authority | Ownership | 两个角色最终写入同一事实 | 谁拥有最终状态？Reporter 是否被误当 authority？ |
| RA-002 | Identity | IdentityCollapse | request/fact/evidence/run 共用摘要或 ID | 同一事实两次独立采集是否被误当同一 Evidence？ |
| RA-003 | Observation | SourceComposition | 一个来源成功后跳过其他适用来源 | 现实究竟是 `OR`、优先级，还是 `A + B`？ |
| RA-004 | Observation | Coverage | 首个成功、exit 0 或 HTTP 200 被推导为完整 | 未支持/未观察范围在哪里？ |
| RA-005 | Observation | Atomicity | 多次 API 读取被描述成原子快照 | 组合事实是否曾在同一时刻成立？ |
| RA-006 | Verdict | VerdictLeakage | Provider 输出 `*_ok` / `passed` 并被直接消费 | sealed 条件与 Core 是否被绕过？ |
| RA-007 | Observation | TemporalOrdering | 本地时间或不可信时间戳决定事实顺序 | 是否有可信顺序来源或只能保留未知？ |
| RA-008 | Identity | CoordinateStaleness | cache/latest/HEAD 替代精确坐标 | 源已漂移时旧结论为何仍成立？ |
| RA-009 | Identity | Pairing | 不同 session/source 的产物被隐式配对 | 它们是否来自同一次有界观察？ |
| RA-010 | Premise | PremiseValidity | 内部自洽被当作源头前提正确 | 有没有与 sealed premise 冲突的外部事实？ |
| RA-011 | Authority | Dependency | “有接口”被当作插件解耦证明 | Core 是否仍认识实现类型或共享其状态？ |
| RA-012 | Presentation | ConclusionSignaling | 红黄绿或高分让提案看起来像结论 | 用户能否一眼分清机器提案、严重度与人工决定？ |
| RA-013 | Execution | Retry | retry 穿过副作用边界 | 重试是否产生重复写、重复通知或双重结算？ |
| RA-014 | Observation | Coverage | 空结果被解释为没有风险 | Provider 是完整执行、部分执行、失败还是不支持？ |
| RA-015 | Authority | Policy | AI confidence 被直接映射为审查优先级 | 项目风险政策和模型自信是否被混为一谈？ |
| RA-016 | Execution | Instruction | 被审查源码/注释改变了工具行为或权限 | 数据是否被错误提升为控制指令？ |

## 5. 完整样例：Fallback 与 Layering

```yaml
pattern_id: RA-003
record_revision: 1
supersedes_digest: null
record_canonicalization: veritrail-json-c14n/1
record_digest: <sha256 of the canonical record excluding record_digest>
status: GENERALIZED
problem_layer: Observation
taxonomy_version: review-attention-taxonomy/1
pattern_class: SourceComposition
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

1. 新发现先以 `OBSERVED` rev1 追加，必须绑定精确来源，不能只写口头印象；
2. 能跨越单个实现、写出最小反例与误报条件后，追加 `GENERALIZED` revision；
3. 拟进入未来合同或自动检测前，追加 `CONTRACT_CANDIDATE` revision 并完成反向找茬；
4. P4 后以 manifest 选择 `pattern_id + selected_record_digest`，形成 `FROZEN_PATTERN` corpus；
5. 被证伪或范围不成立时追加 `REJECTED` revision，保留完整前序链；
6. revision 必须严格引用唯一前序 digest；缺链、分叉、摘要不符或 revision 倒退均不得静默选入 Corpus；
7. 任何自动化只输出命中 Evidence/Proposal，不能因为模式已冻结就自动确认缺陷。

## 7. P2–P4 重点收集面

| P 阶段 | 重点反例方向 |
| --- | --- |
| P2 Public Render | API != Render、redirect/navigation、stale page、session correlation、browser provenance、observer effect |
| P3 Core handoff | pairing authority、sufficiency、跨 Evidence 关系、Verdict leakage、错误压平 |
| P4 Plugin release | 安装/卸载边界、发布物 != 工作树、tag/release/assets/public readback、冻结坐标 |

这些方向是观察清单，不是预判 P2–P4 一定存在缺陷。新 Evidence 可以更新模式状态，但不能为了丰富
Ledger 而制造问题或扩大 P 轨范围。

## 8. P2 追加记录

### RA-017 rev1：完成时计量冒充实时硬上限

以下记录在 P2 Collector 编写前由真实 Chromium、慢速本地生产端与服务端完成/断开 oracle 共同触发。
它不把某个 CDP API 宣布为“不可靠”，只要求硬限制必须证明自己真的在被测响应完成前取得控制权。
`record_digest` 对删除该字段后的完整 JSON 按 `veritrail-json-c14n/1` 计算：

```json
{
  "pattern_id": "RA-017",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:6ff5bd94dd858d9d0a3d6e25ea8e40cb19efb7e3d3fd72c28bd048e95ae10a2e",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail contract correction candidate@91bdce6 docs/89-p2-public-render-collector-contract.md",
    "https://chromedevtools.github.io/devtools-protocol/tot/Network/",
    "https://chromedevtools.github.io/devtools-protocol/tot/Fetch/",
    "https://chromedevtools.github.io/devtools-protocol/tot/IO/"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "CapabilitySemantics",
  "suspicious_structure": "A hard limit is specified, but implementation measures a completion-time or delayed observation event without proving upstream interruption.",
  "possible_interpretations": [
    "The event is a real-time enforcement primitive.",
    "The event is delayed or completion-time observation only.",
    "The measured unit is response body payload rather than encoded wire transfer.",
    "A passive observer must be replaced by an active bounded interception primitive."
  ],
  "required_evidence": [
    "A slow streaming producer with sent, completed and disconnected state.",
    "Separate oversized main-document and subresource fixtures.",
    "The exact runtime/protocol primitive and measurement unit.",
    "Proof that threshold crossing occurs before the producer completes."
  ],
  "minimal_counterexample": "A 40 MiB script under a 32 MiB total cap completes at the server before Network.dataReceived exposes enough bytes to trip the cap.",
  "false_positive_conditions": [
    "The runtime primitive guarantees sufficiently incremental delivery and that guarantee is verified against a producer-side completion oracle.",
    "An independently enforced lower-layer transport quota bounds the same byte domain before the observer."
  ],
  "detectable_cues": [
    "Network.loadingFinished or response.body used as the only size gate",
    "Threshold checked only after complete body materialization",
    "Tests assert a local counter but not producer sent/completed/disconnected state",
    "Metric name says encoded transfer while code counts decoded body characters or payload bytes"
  ],
  "non_claim": "This pattern does not prove Chromium cannot enforce a hard response-body budget; P2 feasibility demonstrated Fetch.takeResponseBodyAsStream plus IO.read can interrupt the producer before completion.",
  "provenance": "Observed 2026-09-06 during P2 8 MiB/32 MiB feasibility before Collector implementation; retained as a contract-model correction, not a defect verdict."
}
```

该记录的解决方向不是“把超时或阈值调大”，而是先拆清计量对象，再选能在响应完成前主动中断的原语。
P2 当前采用 identity response-body stream 作为有界对象，同时明确不声称测得 HTTP/TLS 线速字节。

## 9. P2 闭环期间追加记录

### RA-018 rev1：升级阶段重复刷新总预算

这条记录来自 P2 文档闭环门禁连续两次暴露的 M10 时序债务。它关注的是预算所有权，不把“每阶段都
有 timeout”直接判成错误。`record_digest` 对删除该字段后的完整 JSON 按
`veritrail-json-c14n/1` 计算：

```json
{
  "pattern_id": "RA-018",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:ab4863cb5fad5d25e970d530f63df2b3332058dafa41bba24b3260c4d8994e11",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail PR #43 head@0950cf8 / Public CI run 34016126981 / Python 3.10 -O",
    "VeriTrail correction candidate@b043ef8 src/veritrail/bootstrap_browser.py",
    "VeriTrail correction candidate@b043ef8 tests/test_bootstrap_browser.py"
  ],
  "problem_layer": "Execution",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "BudgetSemantics",
  "suspicious_structure": "One bounded operation gives each graceful, escalation and post-escalation phase a fresh relative timeout even though policy names one overall cleanup budget.",
  "possible_interpretations": [
    "Each phase intentionally owns an independent budget and the declared upper bound is their sum.",
    "The operation owns one end-to-end budget that every phase must share.",
    "Escalation needs a reserved part of the total budget to confirm cleanup.",
    "The repeated relative timeout is harmless because every phase is independently bounded by another outer deadline."
  ],
  "required_evidence": [
    "The policy owner and exact scope of the timeout.",
    "Monotonic timestamps at graceful wait, escalation and cleanup confirmation boundaries.",
    "A deterministic fake-clock fixture in which owned processes remain live.",
    "A real loaded-runtime run that verifies stop reason, elapsed time and owned-resource release."
  ],
  "minimal_counterexample": "A 5 s lifecycle deadline enters browser cleanup; graceful release waits 3 s, forced Job termination then receives a fresh 3 s wait, so the same operation can exceed a less-than-9 s public bound.",
  "false_positive_conditions": [
    "The contract explicitly defines independent per-phase budgets and the public end-to-end bound includes their sum.",
    "A separate immutable outer deadline prevents every inner reset from extending the operation.",
    "The second timeout protects a different operation with a distinct authority and observable result."
  ],
  "detectable_cues": [
    "deadline = monotonic() + timeout repeated after escalation",
    "wait(T); force_terminate(); wait(T)",
    "retry or cleanup phases accept relative timeouts but no shared absolute deadline",
    "A public end-to-end timeout is smaller than the sum of nested phase budgets"
  ],
  "non_claim": "This pattern does not prove per-phase timeouts are inherently wrong; it asks whether timeout ownership and the externally claimed upper bound are the same operation.",
  "provenance": "Observed twice on 2026-09-06 in Python 3.10 -O Public CI while closing the P2 contract; a fake clock reproduced 6.02 s of cleanup budget before the shared-deadline correction."
}
```

### RA-019 rev1：测试与实现来源坐标错配

这条记录保留一次被主动作废的本地测试结果：测试文件来自当前 worktree，但两个解释器通过各自的
editable 安装导入了其他 checkout 的生产模块。它要求先证明“测的是谁”，不把所有跨目录导入都
视为污染：

```json
{
  "pattern_id": "RA-019",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:89682dc8f8548c0b9b0ede38598aebaf143b803061ca946d9d20a87dba8b2fc2",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail local P2 worktree based on main@55babcf",
    "Python 3.10 import probe resolved a sibling R0 review worktree",
    "Python 3.13 import probe resolved the primary VeriTrail checkout",
    "VeriTrail correction candidate@b043ef8"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "EnvironmentProvenance",
  "suspicious_structure": "Tests are selected from the current checkout while the implementation package is imported through stale editable metadata or path precedence from another checkout.",
  "possible_interpretations": [
    "The test deliberately compares two declared immutable coordinates.",
    "An editable installation still points to an older worktree.",
    "PYTHONPATH, current directory and package metadata resolve different source roots.",
    "The imported artifact is intentionally external but its coordinate was omitted from the evidence."
  ],
  "required_evidence": [
    "The resolved test-file path and imported module __file__.",
    "Interpreter identity, sys.path order and editable-install metadata.",
    "Exact repository/worktree SHA for both test and implementation sources.",
    "A rerun with import resolution explicitly bound to the intended source root or immutable wheel."
  ],
  "minimal_counterexample": "Production code is modified in checkout A and tests are read from A, but Python imports the production module from editable checkout B; the result is then attributed to A.",
  "false_positive_conditions": [
    "Cross-coordinate testing is predeclared and both immutable coordinates are retained.",
    "The imported wheel or source tree digest is exact and is the intended subject.",
    "The resolved module path is outside the test checkout by design and the acceptance rule evaluates that explicit pairing."
  ],
  "detectable_cues": [
    "module.__file__ is outside the current checkout",
    "Multiple worktrees or editable installs of the same distribution are present",
    "Test changes affect discovery but production changes do not affect behavior",
    "Different interpreters resolve the same package to different source roots"
  ],
  "non_claim": "A path mismatch does not by itself prove the tested implementation is wrong; it makes the evidence attribution invalid until both coordinates are declared and intentionally paired.",
  "provenance": "Observed 2026-09-06 while validating the M10 cleanup correction: the first local result mixed the current test file with production modules from two other checkouts and was discarded before rerunning with the current worktree src explicitly bound."
}
```

这两条模式均未进入 Pattern Corpus，也没有启动 R1。前者要求确认预算的单一 authority，后者要求先
对齐执行证据的源码身份；二者都只缩小误归因空间，不承诺自动判断现实语义。
