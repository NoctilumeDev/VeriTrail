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

### RA-018 rev2：跨抽象边界刷新预算与中断后继续观察

PR #51 在发布 `P2_FROZEN` 前再次击穿同一公共生命周期上限，证明 rev1 只修正 cleanup 内部两个等待
还不够：外层同步关闭与资源 observer 的释放等待仍可能各自取得时间。该 revision 扩大的是已观察模式的
适用边界，不把 P2 Collector 实现误判为失败，也不覆盖 rev1。`record_digest` 对删除该字段后的完整 JSON
按 `veritrail-json-c14n/1` 计算：

```json
{
  "pattern_id": "RA-018",
  "record_revision": 2,
  "supersedes_digest": "sha256:ab4863cb5fad5d25e970d530f63df2b3332058dafa41bba24b3260c4d8994e11",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:2caba65e9842c38378bcf0f9bac2a49ac01cd228016e7aa9d28215d6fd3b70fe",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail PR #51 head@1829738683b4ce1fb1c59bb2a8928a1ddac2c453 / Public CI run 34035125337 / Python 3.10 -O",
    "VeriTrail main@2d3877df41d7ec5a3b7b932404f6b622f06862a8",
    "VeriTrail correction candidate@4316897 src/veritrail/browser.py",
    "VeriTrail correction candidate@4316897 src/veritrail/bootstrap_browser.py"
  ],
  "problem_layer": "Execution",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "BudgetSemantics",
  "suspicious_structure": "An outer lifecycle deadline is checked before teardown, but synchronous close operations run outside the resource owner's absolute release deadline; after owned termination, finally blocks may also continue observing resources that no longer exist.",
  "possible_interpretations": [
    "Synchronous close is guaranteed to be bounded by the already-expired outer lifecycle deadline.",
    "Context, browser, driver and owned-process release intentionally have separate budgets and the public bound includes their sum.",
    "The resource owner must interrupt first and all later cleanup must consume one inherited absolute deadline.",
    "Post-interruption observer calls are safe because the observed transport remains valid after process termination."
  ],
  "required_evidence": [
    "A monotonic end-to-end timeline from lifecycle creation through final observable completion.",
    "The owner, start, end and inherited deadline of context close, browser close, driver stop and process release.",
    "A loaded real-browser run at the exact public failure coordinate without weakening the elapsed-time assertion.",
    "A deterministic fixture proving escalation cannot create a fresh release budget.",
    "A fixture proving owned interruption precedes potentially blocking close calls and prevents later checkpoint observation."
  ],
  "minimal_counterexample": "A 5 s lifecycle expires, context/browser/driver synchronous shutdown consumes about 5 s outside the observer budget, then process release receives another 3 s; the public less-than-9 s invariant completes in 13.688 s.",
  "false_positive_conditions": [
    "Every teardown primitive is proven to inherit one immutable outer deadline and cannot block beyond it.",
    "The contract explicitly defines separate teardown budgets and the public end-to-end limit includes all of them.",
    "The later observer reads an independently valid immutable snapshot rather than a transport destroyed by interruption."
  ],
  "detectable_cues": [
    "check_deadline(); context.close(); browser.close(); new_release_deadline()",
    "A resource observer creates its absolute deadline only after an unbounded owner-level close returns",
    "Job or process termination is followed by CDP checkpoint or live-resource sampling in finally",
    "Nested modules each satisfy local timeout tests while the public operation exceeds their declared total"
  ],
  "non_claim": "This pattern does not invalidate the merged P2 implementation evidence and does not prove every synchronous close must be skipped; it requires one explicit owner for the public end-to-end interruption budget and forbids post-termination observation from being reported as an external collection failure.",
  "provenance": "Observed on 2026-09-06 when docs-only PR #51 independently reproduced 13.688 s on Python 3.10 -O. The PR was closed unmerged; correction candidate 4316897 terminates and confirms the owned Playwright/Chromium Job on the inherited lifecycle coordinate, skips potentially blocking context/browser closes after accepted interruption, and suppresses checkpoints against the destroyed CDP session."
}
```

rev2 的关键不是“再缩短一个 timeout”，而是把控制变量重新放回总操作：

```text
lifecycle expiry
→ owner accepts interruption
→ owned Job termination and release confirmation share the inherited deadline
→ no live-resource observation after termination
→ local Playwright control object may then stop without refreshing browser cleanup authority
```

该 revision 仍未进入 Pattern Corpus，也没有启动 R1。

### RA-020 rev1：停止权威成立后，延迟回调仍竞争已关闭的控制通道

这条记录来自 P3 合同修正 PR 的既有 Core 门禁。Run 已正确保留 `USER_CANCELLED`，但 Playwright
事件队列中的 HTTP route 回调同时撞上 driver 关闭，并从 listener 泄漏第二个异常。它要求区分
“正常路径错误仍须可见”和“停止权威成立后的路由解析只能尽力完成”。`record_digest` 对删除该字段后的
完整 JSON 按 `veritrail-json-c14n/1` 计算：

```json
{
  "pattern_id": "RA-020",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:56e6cc68a3d3834caa89efda92d1504351cbe5594a9095e0fe0a7c1441c2ccff",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail PR #60 head@dcb46b6 / Public CI run 34050007876 / Python 3.13 -O",
    "VeriTrail main@294ebf7dd11db34d5f9ff99a8b879e81cb9b1c8d",
    "VeriTrail correction candidate@e4e341a src/veritrail/browser.py",
    "VeriTrail correction candidate@e4e341a tests/test_browser_evidence.py"
  ],
  "problem_layer": "Execution",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "LifecycleAuthority",
  "suspicious_structure": "An asynchronous callback recognizes an authoritative stop and then performs a route-resolution command through a driver transport that owner-level teardown may already be closing.",
  "possible_interpretations": [
    "The driver remains valid until every queued callback has resolved its route.",
    "Route resolution is best-effort after the owning thread has accepted the stop reason.",
    "The failure happened before stop ownership was established and must remain observable.",
    "The event system forwards callback failures to the lifecycle owner without leaking an independent listener error."
  ],
  "required_evidence": [
    "The exact point at which stop reason ownership becomes authoritative.",
    "A deterministic callback action that raises after the driver transport closes.",
    "Repeated real-Chromium cancellation runs that capture listener stderr and verify cleanup.",
    "A change-surface audit proving normal allow, block and connect operations do not use the best-effort stop path."
  ],
  "minimal_counterexample": "User cancellation starts Playwright teardown while a queued HTTP route callback catches the same stop; route.abort then raises Connection closed while reading from the driver and Playwright leaks Error occurred in event listener even though the owning Run preserves USER_CANCELLED.",
  "false_positive_conditions": [
    "The runtime serializes callback drainage before driver teardown and proves the route transport remains valid.",
    "The callback failure is delivered to the lifecycle owner and cannot create a second competing failure fact.",
    "The failing route operation runs before stop acceptance, where normal error visibility still applies."
  ],
  "detectable_cues": [
    "except StopRequested followed by route.abort, route.close or another driver command",
    "queued event callbacks use a transport destroyed concurrently by owner cleanup",
    "the test verdict is correct but stderr contains Error occurred in event listener",
    "an accepted stop reason is followed by a second callback-level transport failure"
  ],
  "non_claim": "This pattern does not authorize suppressing ordinary route or browser errors. Only route resolution after authoritative stop acceptance is best-effort; failures on normal routing paths must remain visible.",
  "provenance": "Observed on 2026-09-06 when docs-only PR #60 reproduced the Playwright listener race on Python 3.13 -O. The exact local test reproduced it on attempt 3 of 5; correction candidate e4e341a then passed 20 consecutive Python 3.13 -O real-Chromium repetitions and the 388-test Core suite across both Python versions in normal and optimized modes without listener stderr."
}
```

该记录不重开 R0，也不进入 Pattern Corpus。它只保留一个可复用的审查问题：异步回调已经观察到
权威停止后，后续动作是在完成必要语义，还是在竞争一个已被 owner 撤销的控制通道？

## 10. P3 闭环期间追加记录

### RA-021 rev1：合成夹具与生产 Evidence 结构漂移

这条记录来自 P3 第一条真实 GitHub 纵向链。Synthetic reference lab、sealed Plan 与四态测试彼此一致，
但它们使用了生产 P2 Collector 从未输出的简化字段路径。它要求区分“Core 语义夹具可用”与“产品
Adapter 事实结构相容”，不否定有边界的合成测试。`record_digest` 对删除该字段后的完整 JSON 按
`veritrail-json-c14n/1` 计算：

```json
{
  "pattern_id": "RA-021",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:c728324a2335f1e88cc93a9909e62be86bf47d1ad26dfe82e8d3210811fc134b",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail contract main@589bbad docs/92-p3-core-handoff-contract.md",
    "VeriTrail synthetic reference lab candidate@86d44d8",
    "VeriTrail first local P3-E run against GitHub exact commit 589bbad",
    "VeriTrail correction commit@7e10e7a",
    "VeriTrail implementation main@c0bce6cb7a3c9f3684d1845beda355084f232d0a"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SyntheticFixtureDrift",
  "suspicious_structure": "A hand-built synthetic Evidence fixture uses a simplified field path or shape that the frozen production Collector never emits, so the reference lab proves Verdict behavior against a different observation model than the real handoff.",
  "possible_interpretations": [
    "The fixture intentionally tests only generic Core semantics and is not claimed to represent a product adapter.",
    "The production Evidence schema evolved while the synthetic fixture retained an older or invented shape.",
    "The test reimplemented normalized facts instead of consuming an adapter conformance vector.",
    "The sealed Plan and fixture agree with each other but not with the actual Collector output."
  ],
  "required_evidence": [
    "The exact frozen contract pointer for every rule operand.",
    "One standard Evidence artifact emitted by the real Collector at an immutable coordinate.",
    "A byte- or pointer-level comparison between synthetic fixture paths and production facts.",
    "A full vertical slice that feeds real Evidence through the same handoff and Core boundary."
  ],
  "minimal_counterexample": "A synthetic render fixture stores target_commit_sha at /facts/navigation/target_commit_sha, so four Verdict tests pass; real P2 Evidence stores it at /facts/target/source_coordinates/target_commit_sha, making the same-target integrity operand unresolved and the real P3 slice INCONCLUSIVE.",
  "false_positive_conditions": [
    "The fixture is explicitly generic, is not described as adapter-compatible and no product acceptance conclusion depends on it.",
    "A shared data-only conformance vector proves the synthetic and production shapes expose every referenced pointer with identical semantics.",
    "The synthetic artifact is generated by the frozen production normalizer rather than reconstructed by the test."
  ],
  "detectable_cues": [
    "Tests hand-build nested facts dictionaries that resemble but do not originate from the production adapter",
    "A JSON pointer used by the sealed Plan is absent from a real standard Evidence artifact",
    "Synthetic four-Verdict tests are green while the first real vertical slice yields a missing operand or INCONCLUSIVE",
    "Fixture schema has no conformance assertion against one immutable production Evidence sample"
  ],
  "non_claim": "This pattern does not make synthetic fixtures invalid or require every unit test to call a live service. It requires product-level claims to prove that synthetic fact paths and semantics match the frozen adapter contract before using those fixtures as vertical-slice evidence.",
  "provenance": "Observed 2026-09-06 when the first P3-E real GitHub run stopped after handoff publication: the frozen P3 contract named the correct P2 target path, but the synthetic C lab and its sealed Plans used a simplified navigation path. The old output was retained outside the repository, C was corrected without changing P2, and the real PASS/FAIL slice was rerun twice before P3 freeze closure."
}
```

该记录不把“synthetic”染成缺陷，也不要求单元测试联网。它只要求产品级结论在冻结前至少有一条真实
标准 Evidence 贯穿同一 handoff/Core 边界，并明确证明所有 Plan pointer 都能在生产 Artifact 中解析。
RA-021 尚未进入 Pattern Corpus，Review Attention R1 仍被 P4 与 corpus freeze 阻断。

## 11. P2–P4 冻结后补账记录

以下六条记录来自已经保留在 P2、P3、P4 与 Core 0.13.0 事实文档中的真实反例。它们在 P4 最终冻结后
按既有 Schema 物化，用来补齐 Ledger，不把后见总结伪装成当时已经存在的记录，也不自动进入 Pattern
Corpus。

### RA-022 rev1：观察者制造的失败被归因给外部系统

```json
{
  "pattern_id": "RA-022",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:879d1fd06991d5aa24ddd660b413a364bfb5cc6ed1213422176df475f6904f59",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail P2 contract main@c0ec6e29ee9f43e69846535af8b2e79be52a4fc1 docs/89-p2-public-render-collector-contract.md",
    "VeriTrail P2 implementation main@ca6b8aaa33bc06795c96610b9e9085506efef9a0",
    "VeriTrail P4 release facts main@548b17ccb1f20d55a9f9beef6666e913af5f65d9 docs/108-p4-github-evidence-release-readback-facts.md"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "ObserverEffectAttribution",
  "suspicious_structure": "A read-only observer intentionally blocks or rewrites an operation, then reports the resulting runtime error as a failure of the external system being observed.",
  "possible_interpretations": [
    "The failure was produced by the external platform or transport.",
    "The observer's declared policy deliberately produced the failure.",
    "The observer effect is expected but still makes the requested observation incomplete.",
    "The runtime cannot distinguish policy-generated and external failures at the available boundary."
  ],
  "required_evidence": [
    "The exact observer policy and action that accepted, blocked or rewrote the operation.",
    "Runtime error class and timing correlated with that policy decision.",
    "Independent page or artifact health facts after the observer-induced event.",
    "Coverage rules stating whether the induced event affects the requested observation."
  ],
  "minimal_counterexample": "A read-only browser route intentionally aborts a telemetry POST, Chromium reports BlockedByClient, and the Collector labels the public GitHub page failed even though the requested body scope is complete and stable.",
  "false_positive_conditions": [
    "The blocked operation is itself part of the sealed observation and its absence makes coverage incomplete.",
    "The external system independently failed before the observer policy acted.",
    "The runtime proves the same error class cannot be generated by the observer's own control path."
  ],
  "detectable_cues": [
    "route.abort or policy deny immediately precedes an external-failure classification",
    "BlockedByClient is grouped with DNS, TLS or remote HTTP failures",
    "test harness, mock or timeout wrapper effects are attributed to the subject",
    "the requested content is usable while a policy-blocked side channel is reported as page failure"
  ],
  "non_claim": "This pattern does not make observer effects harmless. It requires provenance and coverage to distinguish what the observer caused from what the external system did.",
  "provenance": "Observed during P2 real-Chromium integration when the GET/HEAD-only policy blocked GitHub telemetry writes. Materialized on 2026-09-09 after P4 freeze from the retained contract, implementation and release-readback facts."
}
```

### RA-023 rev1：核验路径与被裁决快照失去连续性

```json
{
  "pattern_id": "RA-023",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:b4cc563222decfaa02c5d84e0ab5d9a239f586399ef8e048eff14dd97b8b9458",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail P3 contract main@589bbad7261cceda1aa3a6412278a48473a9b1b7 docs/92-p3-core-handoff-contract.md",
    "VeriTrail snapshot correction main@5d4e7bbbf706d92c98cf36418d6f86b5caf2d3d8",
    "VeriTrail P3 implementation main@c0bce6cb7a3c9f3684d1845beda355084f232d0a"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SnapshotContinuity",
  "suspicious_structure": "One layer safely reads and verifies a file by path, but a later layer receives only that path and independently rereads it before judgment.",
  "possible_interpretations": [
    "The path names an immutable artifact and both reads are equivalent.",
    "The path is only a locator and its contents may change between reads.",
    "The first layer verified bytes while the second layer consumes a mutable decoded object.",
    "A trusted storage boundary provides snapshot semantics that are not expressed in the API."
  ],
  "required_evidence": [
    "The exact bytes and digest produced by the verifying read.",
    "A deterministic replacement between verification and consumption.",
    "The ownership and mutability contract of the imported Evidence object.",
    "Proof that the Core consumes the same imported snapshot without path reread or caller mutation."
  ],
  "minimal_counterexample": "The handoff verifies Evidence A at path p, p is replaced with valid Evidence B, and the Core path API rereads B while the run is described as having judged verified A.",
  "false_positive_conditions": [
    "The path belongs to an immutable content-addressed store and immutability is independently enforced.",
    "The later layer receives and verifies its own exact artifact identity rather than relying on the earlier check.",
    "The same owned immutable snapshot object is passed across the boundary and its digest is rechecked before use."
  ],
  "detectable_cues": [
    "verify(path) followed by evaluate(path)",
    "a digest check returns only a filename or locator",
    "multiple safe reads are treated as proof of one snapshot",
    "an imported mapping remains shared with mutable caller state"
  ],
  "non_claim": "This pattern does not prohibit path-based APIs. It requires the artifact snapshot that was verified to remain the artifact snapshot that is judged.",
  "provenance": "Observed before P3-B when the frozen handoff sequence composed a verifier read with the Core path importer read. Materialized on 2026-09-09 from the retained P3 contract correction and implementation facts."
}
```

### RA-024 rev1：摘要产物被要求声明自身摘要

```json
{
  "pattern_id": "RA-024",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:c868140a0ffe033a04fc258b82473d6671002bbe7355eec300e3dd3fd3c743b4",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail P4 contract candidate main@f27507c3735a68134fa428344f63265601c93715 docs/96-p4-github-evidence-release-contract.md",
    "VeriTrail PR #71 correction@35206c8feb6e84c93dc73cf50d048440eff7e8ff",
    "VeriTrail corrected contract main@eb4dcb60230a516503bf80ce26e13b25cd9b9d97 docs/97-p4-github-evidence-release-contract-freeze.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "DigestSelfReference",
  "suspicious_structure": "A finite manifest or validation summary is required to include the digest or size of every payload while that same document is itself one of the payloads.",
  "possible_interpretations": [
    "The document is intentionally excluded from its own digest domain.",
    "An external envelope or later manifest binds the completed document.",
    "A fixed-point digest construction is explicitly specified and implementable.",
    "The contract accidentally creates a nonterminating identity definition."
  ],
  "required_evidence": [
    "The exact canonical byte domain for every digest field.",
    "The generation and closure order of payload, summary and checksum artifacts.",
    "A recomputation vector proving each identity without mutable placeholders.",
    "The external artifact that binds the final summary and checksum bytes."
  ],
  "minimal_counterexample": "A validation-summary JSON must contain its own SHA-256; adding the digest changes the JSON bytes and therefore changes the digest again.",
  "false_positive_conditions": [
    "The self field is excluded by an explicit canonicalization rule and consumers enforce that rule.",
    "The summary is not in the payload set it describes and is bound by a later immutable manifest.",
    "The system uses a formally specified construction whose fixed point and verification procedure are actually proven."
  ],
  "detectable_cues": [
    "manifest says every payload while listing itself as a payload",
    "a file records its own full-file SHA-256 or byte size",
    "build scripts patch a digest placeholder inside the hashed file",
    "checksum manifests include their own checksum without an exclusion rule"
  ],
  "non_claim": "This pattern does not forbid nested or chained manifests. It requires an acyclic identity construction or a fully specified verifiable alternative.",
  "provenance": "Observed after the first P4 contract candidate merged, before any plugin tag or Release existed. Materialized on 2026-09-09 from the preserved non-self-referential contract correction."
}
```

### RA-025 rev1：短固定重试窗口被当作充分恢复能力

```json
{
  "pattern_id": "RA-025",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:012555e96104ba08f998df5d42b7154069b8a76c8f11352e0b9743b641c83993",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail PR #72 Public CI run 34241218820",
    "VeriTrail main@12130378febde2075d4cb9924628a07f9f26cb1e Public CI run 34244325251",
    "VeriTrail release download correction main@d23916735c7ac4d7e4a706d8edc5b106046b93c8 docs/98-release-download-recovery-correction.md"
  ],
  "problem_layer": "Execution",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "RecoveryBudget",
  "suspicious_structure": "Retry count and a short fixed delay are treated as sufficient recovery without an explicit end-to-end availability budget, error taxonomy or partial-artifact publication rule.",
  "possible_interpretations": [
    "The external service contract guarantees recovery inside the short retry window.",
    "Only a best-effort probe is intended and immediate failure is acceptable.",
    "Transient failures may outlive the retry window and require bounded backoff.",
    "Repeated retries are masking a permanent coordinate or integrity failure."
  ],
  "required_evidence": [
    "Attempt-level HTTP or transport failure classes and monotonic timing.",
    "An absolute recovery deadline shared by requests and sleeps.",
    "Permanent-error and integrity-failure no-retry fixtures.",
    "Proof that partial downloads are cleaned and only digest-verified bytes are atomically published."
  ],
  "minimal_counterexample": "Two immutable Release assets independently return four HTTP 500 responses inside a fixed approximately six-second retry-wait window, then later download anonymously with the frozen SHA-256 intact.",
  "false_positive_conditions": [
    "The declared operation intentionally has a short fail-fast availability objective and does not claim resilient recovery.",
    "An outer orchestrator owns a larger explicit recovery budget and safely retries the whole idempotent operation.",
    "The failure is permanent or the downloaded bytes fail integrity validation, so retry must not produce acceptance."
  ],
  "detectable_cues": [
    "fixed retry count and delay with no monotonic deadline",
    "retry-all-errors mixes 404, digest mismatch and HTTP 500",
    "each attempt receives a fresh full timeout",
    "partial files share the final artifact name before digest verification"
  ],
  "non_claim": "This pattern does not require long or unlimited retries and does not relax checksum validation. Availability recovery and integrity acceptance remain separate authorities.",
  "provenance": "Observed twice during P4 contract closure on different frozen Release assets. Materialized on 2026-09-09 from the retained failed runs and bounded-recovery correction; no GitHub internal root cause is claimed."
}
```

### RA-026 rev1：同版本源码产物代替公开分发产物

```json
{
  "pattern_id": "RA-026",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:a43a34bdb8ac01aaf72d35b41b90930b11d61bccbdc6b5a49627b904b6726a60",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail public tag v0.12.2 peeled commit@f961930ae1e69d7d88849fa2b0d40befb3e94c89",
    "VeriTrail first Acceptance Core commit@0e01dbf3c31631bc62993944d39fbccd79303555",
    "VeriTrail discovery main@8e51a03113a54230c5120d7bf5084035c78fe63e docs/100-core-v0.13.0-acceptance-api-release-contract.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "DistributionIdentity",
  "suspicious_structure": "A clean-install or compatibility claim uses a wheel built from current source because it declares the same version as an older public Release asset.",
  "possible_interpretations": [
    "Version equality guarantees byte and capability equality for the distribution.",
    "The current-source wheel is a development candidate and cannot represent the public coordinate.",
    "A public artifact was rebuilt or replaced under an unchanged version.",
    "The acceptance claim is source compatibility only and never claimed public reproducibility."
  ],
  "required_evidence": [
    "Public tag, asset URL and downloaded SHA-256.",
    "The exact source commit used to build each local and public distribution.",
    "Public API inventory from clean installation outside the repository.",
    "A versioning decision when the required public capability did not exist in the released artifact."
  ],
  "minimal_counterexample": "The public veritrail 0.12.2 wheel lacks Acceptance APIs, while a current-main wheel still labeled 0.12.2 contains them; local clean install passes and is incorrectly used to claim the public plugin is reproducible.",
  "false_positive_conditions": [
    "The claim is explicitly limited to the current source candidate and retains its exact commit and digest.",
    "The locally tested bytes are independently proven identical to the public asset bytes.",
    "The public coordinate is intentionally mutable and the contract does not claim immutable reproducibility."
  ],
  "detectable_cues": [
    "package version matches a Release while git commit is newer than the release tag",
    "clean-install uses dist built from the working tree instead of anonymous public download",
    "public wheel API inventory differs from local wheel inventory",
    "rebuilding an old version is proposed instead of publishing a new capability version"
  ],
  "non_claim": "This pattern does not make local wheels invalid for development. It prevents current-source bytes from standing in for an immutable public distribution claim without identity proof.",
  "provenance": "Observed at the P4 final clean-install gate before the GitHub Evidence Plugin Release. Materialized on 2026-09-09 from the retained publication mismatch and Core 0.13.0 corrective release contract."
}
```

### RA-027 rev1：功能正向测试暗带无权威性能阈值

```json
{
  "pattern_id": "RA-027",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:8cf2e2947c75c604a7ccd5409a7c0db66370ea61fe22f625be43118c9d339cb2",
  "status": "GENERALIZED",
  "source_coordinate": [
    "VeriTrail Core 0.13.0 candidate main@a5ba0e1bd8f181851db83de611981524da1da8f5",
    "VeriTrail Public CI run 34295582018 / Python 3.13 -O",
    "VeriTrail correction main@43c8e9105adf84641d203514594d3e0c5a1251e8 docs/104-core-v0.13.0-m11-positive-fixture-budget-correction.md"
  ],
  "problem_layer": "Plan",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "AssertionScope",
  "suspicious_structure": "A positive functional test narrows an outer fail-safe timeout below the sum of valid bounded work and then treats timeout as evidence that the function is incorrect.",
  "possible_interpretations": [
    "The timeout is a declared performance acceptance threshold owned by the test plan.",
    "The timeout is only a deadlock fail-safe and must allow all contract-valid work.",
    "Inner operation limits imply an unstated end-to-end latency objective.",
    "The implementation regressed even though no performance contract exists."
  ],
  "required_evidence": [
    "The positive test's declared functional claim and any separately sealed performance claim.",
    "Per-operation limits, operation count and outer lifecycle budget.",
    "A phase timeline showing functional completion, timeout observation and cleanup.",
    "Dedicated deadline/cancellation tests that remain unchanged when the positive fail-safe is corrected."
  ],
  "minimal_counterexample": "A positive M11 test serially performs two browser viewports with 10-second per-operation limits under an unowned 15-second outer lifecycle; valid work completes at 18.125 seconds and Core correctly returns ABORTED/PENDING instead of the expected functional PASS.",
  "false_positive_conditions": [
    "The end-to-end latency threshold is explicitly sealed as part of the acceptance claim.",
    "The test subject guarantees a tighter total bound than the sum of inner limits and the fixture measures that contract.",
    "The outer deadline is intentionally the behavior under test rather than a positive-path fail-safe."
  ],
  "detectable_cues": [
    "positive functional fixture overrides a shared lifecycle timeout with a smaller unexplained number",
    "test name asserts correctness while failure condition is only elapsed wall-clock time",
    "multiple bounded operations fit individually but not inside the outer fixture budget",
    "fix proposals widen product deadlines instead of separating functional and performance assertions"
  ],
  "non_claim": "This pattern does not remove bounded execution or weaken dedicated timeout tests. It requires performance thresholds to have an explicit owner instead of hiding inside a functional positive fixture.",
  "provenance": "Observed on 2026-09-08 after Core 0.13.0 candidate merge when the original Python 3.13 -O exact-main gate stopped at 18.125 seconds. Materialized on 2026-09-09 from the retained L0 test-fixture correction facts."
}
```

这六条均保持 `GENERALIZED`，没有因为“值得进入候选集”就提前写成 `CONTRACT_CANDIDATE` 或
`FROZEN_PATTERN`。Pattern Corpus 的选择、状态提升、manifest 与 exact source commit 必须继续按独立合同
串行完成。

## 12. 首个 Pattern Corpus 的候选 revisions

以下四条 revision 只把首个 R1 Corpus 的最小候选物化为完整记录。它们分别约束来源组合、覆盖声明、
精确源码坐标与已核验快照连续性；状态仍是 `CONTRACT_CANDIDATE`，尚未进入 Corpus。

### RA-003 rev1：适用来源被错误建模为 fallback

```json
{
  "pattern_id": "RA-003",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:98ba9abb407347ce5f8721644aaf75cb9b126a6fb695cd2a8edb2eb21603f60a",
  "status": "CONTRACT_CANDIDATE",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail P1 implementation main@9b45bd635dedd132dc8333c105c04723991c2670 plugins/github-evidence/src/veritrail_github/collector.py",
    "VeriTrail required-check layering correction@7bd800fd9962fa4b4baa7a849128f373d7fa294a and merged main@5b363637f59be9786d58eed61a14e3bd663dd6d8 docs/83-p1-structured-github-api-collector-contract.md"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SourceComposition",
  "suspicious_structure": "One relation or fact source succeeds or returns an empty collection, so other independently applicable sources are skipped as fallbacks.",
  "possible_interpretations": [
    "The sources are mutually exclusive.",
    "One source has precedence and the others apply only when it is unavailable.",
    "One source completely covers the others.",
    "The sources are independently applicable and their facts must be layered."
  ],
  "required_evidence": [
    "The contract or external semantics defining whether sources are exclusive, ordered, covering or cumulative.",
    "A coexistence fixture in which two sources contribute different valid relations.",
    "An empty-first-source fixture in which another applicable source remains non-empty.",
    "Normalization rules that retain source provenance while deduplicating semantically identical relations."
  ],
  "minimal_counterexample": "Source A derives a call relation and Source B derives an ownership relation for the same SourceSnapshot; A succeeds, B is skipped as fallback, and the resulting semantic inventory is described as complete.",
  "false_positive_conditions": [
    "The contract proves the sources are mutually exclusive.",
    "The preferred source is proven to cover every fact domain of the skipped source and retains that coverage provenance.",
    "The output is explicitly partial and records every skipped applicable source."
  ],
  "detectable_cues": [
    "fallback, first-success, else-if or coalesce around fact providers",
    "a successful empty result short-circuits another provider",
    "multiple relation providers feed one inventory but only the first successful result is retained",
    "deduplication removes the contributing-source identities"
  ],
  "non_claim": "A fallback structure is not automatically wrong. This candidate only requires R1 to make source composition explicit and to preserve partial or conflicting facts when cumulative applicability cannot be disproved.",
  "provenance": "The seed was frozen in R0 and grounded by the P1 Rulesets plus classic branch-protection counterexample. It was materialized as an R1 contract candidate from exact baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a after Pattern Corpus contract 0.1 froze."
}
```

### RA-004 rev1：有界成功被描述成完整覆盖

```json
{
  "pattern_id": "RA-004",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:6485945ad3280e33b79c94619323c16e5503544a73ccfbd694a940e81ee5c3c8",
  "status": "CONTRACT_CANDIDATE",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail R1 Semantic Review Slice design@846d392145703f2406cc244cc1fdc0e573202e21 docs/85-post-core-review-attention-plugin-plan.md",
    "VeriTrail P2 implementation main@ca6b8aaa33bc06795c96610b9e9085506efef9a0 docs/90-p2-public-render-collector-freeze-candidate.md"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "Coverage",
  "suspicious_structure": "A bounded traversal, parser or provider exits successfully and that local success is promoted to complete semantic or repository coverage without a coverage and truncation ledger.",
  "possible_interpretations": [
    "Successful completion means the declared finite scope was fully covered.",
    "The mechanism reached a symbol, file, depth or time limit and only produced a partial view.",
    "Unsupported syntax or provider failure omitted part of the source graph.",
    "The result is intentionally a bounded sample and does not claim completeness."
  ],
  "required_evidence": [
    "The declared source scope and deterministic inventory denominator.",
    "Visited, emitted, skipped, unsupported and failed item counts with identities.",
    "Every slice expansion limit, stop condition and truncation reason.",
    "A fixture where a valid downstream relation exists just beyond one configured boundary."
  ],
  "minimal_counterexample": "A call-path slice reaches max_symbols before one downstream call edge, returns exit 0 and is published as a complete call chain without PARTIAL coverage or a truncation reason.",
  "false_positive_conditions": [
    "The finite scope and denominator are sealed and every member is accounted for.",
    "The result is explicitly partial and retains the exact boundary and omitted inventory.",
    "A separate complete provider proves the same declared coverage and the bounded result is not used as its substitute."
  ],
  "detectable_cues": [
    "exit 0, non-empty output or first match directly sets coverage to COMPLETE",
    "max_depth, max_symbols, max_files or timeout without a truncation field",
    "unsupported files disappear from the inventory denominator",
    "empty proposal or analyzer output is described as no issue"
  ],
  "non_claim": "This candidate does not require unbounded graph traversal or claim that every partial result is unusable. It requires bounded R1 views to expose exactly what was covered and why expansion stopped.",
  "provenance": "The seed was frozen in R0 and materialized for the R1 bounded-slice and coverage-ledger boundary from exact baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a; no R1 implementation defect is claimed."
}
```

### RA-008 rev1：可变源码别名替代精确快照坐标

```json
{
  "pattern_id": "RA-008",
  "record_revision": 1,
  "supersedes_digest": null,
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:49fcdc03c92734c0caf980a9ac37d8724868e94a9263f5da610d96065d6790c1",
  "status": "CONTRACT_CANDIDATE",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail R1 Semantic Review Slice design@846d392145703f2406cc244cc1fdc0e573202e21 docs/85-post-core-review-attention-plugin-plan.md",
    "VeriTrail P1 corrected contract main@5b363637f59be9786d58eed61a14e3bd663dd6d8 docs/83-p1-structured-github-api-collector-contract.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "CoordinateStaleness",
  "suspicious_structure": "A mutable alias such as HEAD, latest, a branch name or an unbound working directory is used as the identity of the source from which inventories, relations and slices are derived.",
  "possible_interpretations": [
    "The alias is resolved once to an immutable commit and every artifact retains that resolution.",
    "Different pipeline stages resolve the alias at different times.",
    "The working tree is intentionally the subject and its full dirty-state identity is retained.",
    "The result is exploratory and makes no reproducibility or continuity claim."
  ],
  "required_evidence": [
    "The exact commit/tree or complete working-tree content identity used for the SourceSnapshot.",
    "The resolution time and resolver provenance for any mutable input alias.",
    "A rerun after the alias moves while the original snapshot remains addressable.",
    "Bindings from every CodeFact, relation, slice and coverage entry back to one SourceSnapshot identity."
  ],
  "minimal_counterexample": "Inventory resolves branch main to commit A, main moves to B before slice derivation, and both outputs are labeled as one SourceSnapshot because each stage only records the branch name.",
  "false_positive_conditions": [
    "The alias is resolved exactly once and the immutable resolved coordinate is propagated to every consumer.",
    "The subject is an intentionally mutable working tree whose file set, content digests and dirty state are captured atomically enough for the declared claim.",
    "The output is clearly marked exploratory and is not used as reproducible review evidence."
  ],
  "detectable_cues": [
    "HEAD, latest or branch names appear where an immutable source identity is required",
    "separate stages call rev-parse independently",
    "artifacts record repository URL and branch but no commit/tree or content digest",
    "dirty files are parsed without entering SourceSnapshot identity"
  ],
  "non_claim": "This candidate does not forbid friendly aliases at user entry. It requires R1 to resolve them once and bind all derived artifacts to the resulting exact SourceSnapshot or to retain an explicitly bounded working-tree identity.",
  "provenance": "The seed was frozen in R0 and materialized as the direct SourceSnapshot identity candidate from exact baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a after P1/P2 demonstrated that friendly coordinates and exact observed coordinates are different identities."
}
```

### RA-023 rev2：核验快照必须继续成为消费快照

```json
{
  "pattern_id": "RA-023",
  "record_revision": 2,
  "supersedes_digest": "sha256:b4cc563222decfaa02c5d84e0ab5d9a239f586399ef8e048eff14dd97b8b9458",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:cd9f19656476803f5c49138f5269bed3856705e5f3e98d900d631de08ae97d35",
  "status": "CONTRACT_CANDIDATE",
  "source_coordinate": [
    "VeriTrail P3 contract main@589bbad7261cceda1aa3a6412278a48473a9b1b7 docs/92-p3-core-handoff-contract.md",
    "VeriTrail snapshot correction main@5d4e7bbbf706d92c98cf36418d6f86b5caf2d3d8",
    "VeriTrail P3 implementation main@c0bce6cb7a3c9f3684d1845beda355084f232d0a",
    "VeriTrail Pattern Corpus contract baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a docs/109-review-attention-pattern-corpus-freeze-contract.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SnapshotContinuity",
  "suspicious_structure": "One layer safely reads and verifies source bytes or an imported artifact, but later derivation receives only the locator or a caller-owned mutable object and independently reconstructs what it consumes.",
  "possible_interpretations": [
    "The locator names an immutable content-addressed snapshot and every read is equivalent.",
    "The locator is mutable and can identify different bytes between verification and derivation.",
    "The verifier owns a stable copy but later code consumes a shared mutable decoded object.",
    "A storage or language-service boundary provides snapshot semantics that are not expressed in the API."
  ],
  "required_evidence": [
    "The exact source bytes or canonical imported snapshot and its digest.",
    "A deterministic replacement or mutation between verification and semantic consumption.",
    "The ownership and mutability contract of SourceSnapshot and every derived input object.",
    "Proof that inventory, relation and slice derivation consume the same verified snapshot without locator reread or caller mutation."
  ],
  "minimal_counterexample": "R1 verifies source archive A at path p, p is replaced with valid archive B, and a SemanticMapper rereads p while the resulting CodeFacts are described as derived from verified A.",
  "false_positive_conditions": [
    "The locator belongs to an independently enforced immutable content-addressed store.",
    "The later layer verifies and owns its own exact snapshot identity rather than relying on the earlier check.",
    "The same owned immutable snapshot object is passed across the boundary and its digest is rechecked before use."
  ],
  "detectable_cues": [
    "verify(path) followed by parse(path) or derive(path)",
    "a digest check returns only a filename or locator",
    "multiple safe reads are treated as proof of one snapshot",
    "an imported mapping or source buffer remains shared with mutable caller state"
  ],
  "non_claim": "This candidate does not prohibit path-based entry APIs or repeated reads from proven immutable storage. It requires the SourceSnapshot verified at the R1 boundary to remain the snapshot consumed by deterministic derivation.",
  "provenance": "RA-023 rev1 was materialized from the P3 handoff TOCTOU correction. Rev2 preserves that failure mechanism and narrows its direct R1 application from exact baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a; it does not claim an R1 implementation already exists or is defective."
}
```

这四条只完成候选提升。任何摘要不符、链断裂、重复 successor 或选择审查缺口都会阻止后继
`FROZEN_PATTERN` revision 与 manifest；R1 继续保持 `BLOCKED`。

## 13. 首个 Pattern Corpus 的冻结 revisions

候选 revision 经逐条最小性审议与独立摘要复算后，只有以下四条形成线性 successor。这里的
`FROZEN_PATTERN` 只表示该 revision 可被首个 R1 Corpus manifest 精确选择；不表示命中即缺陷、自动
Verdict 或 HumanDisposition，也不关闭其余开放 Ledger。

### RA-003 rev2：适用来源被错误建模为 fallback

```json
{
  "pattern_id": "RA-003",
  "record_revision": 2,
  "supersedes_digest": "sha256:98ba9abb407347ce5f8721644aaf75cb9b126a6fb695cd2a8edb2eb21603f60a",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:1e20737718ec5e4056dc39d91f750e81c0ccbfefa965b72c1d918bd679f669f7",
  "status": "FROZEN_PATTERN",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail P1 implementation main@9b45bd635dedd132dc8333c105c04723991c2670 plugins/github-evidence/src/veritrail_github/collector.py",
    "VeriTrail required-check layering correction@7bd800fd9962fa4b4baa7a849128f373d7fa294a and merged main@5b363637f59be9786d58eed61a14e3bd663dd6d8 docs/83-p1-structured-github-api-collector-contract.md"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SourceComposition",
  "suspicious_structure": "One relation or fact source succeeds or returns an empty collection, so other independently applicable sources are skipped as fallbacks.",
  "possible_interpretations": [
    "The sources are mutually exclusive.",
    "One source has precedence and the others apply only when it is unavailable.",
    "One source completely covers the others.",
    "The sources are independently applicable and their facts must be layered."
  ],
  "required_evidence": [
    "The contract or external semantics defining whether sources are exclusive, ordered, covering or cumulative.",
    "A coexistence fixture in which two sources contribute different valid relations.",
    "An empty-first-source fixture in which another applicable source remains non-empty.",
    "Normalization rules that retain source provenance while deduplicating semantically identical relations."
  ],
  "minimal_counterexample": "Source A derives a call relation and Source B derives an ownership relation for the same SourceSnapshot; A succeeds, B is skipped as fallback, and the resulting semantic inventory is described as complete.",
  "false_positive_conditions": [
    "The contract proves the sources are mutually exclusive.",
    "The preferred source is proven to cover every fact domain of the skipped source and retains that coverage provenance.",
    "The output is explicitly partial and records every skipped applicable source."
  ],
  "detectable_cues": [
    "fallback, first-success, else-if or coalesce around fact providers",
    "a successful empty result short-circuits another provider",
    "multiple relation providers feed one inventory but only the first successful result is retained",
    "deduplication removes the contributing-source identities"
  ],
  "non_claim": "A fallback structure is not automatically wrong. This pattern only requires R1 to make source composition explicit and to preserve partial or conflicting facts when cumulative applicability cannot be disproved.",
  "provenance": "RA-003 rev1 was independently recomputed and selected only for R1 relation-source composition. Rev2 freezes the same semantics for the first bounded Corpus payload; it does not declare any reviewed code defective."
}
```

### RA-004 rev2：有界成功被描述成完整覆盖

```json
{
  "pattern_id": "RA-004",
  "record_revision": 2,
  "supersedes_digest": "sha256:6485945ad3280e33b79c94619323c16e5503544a73ccfbd694a940e81ee5c3c8",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:1915e4aba5b7604ed417c640ff54494c720cc2bb72c815bf4305f65f4d439077",
  "status": "FROZEN_PATTERN",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail R1 Semantic Review Slice design@846d392145703f2406cc244cc1fdc0e573202e21 docs/85-post-core-review-attention-plugin-plan.md",
    "VeriTrail P2 implementation main@ca6b8aaa33bc06795c96610b9e9085506efef9a0 docs/90-p2-public-render-collector-freeze-candidate.md"
  ],
  "problem_layer": "Observation",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "Coverage",
  "suspicious_structure": "A bounded traversal, parser or provider exits successfully and that local success is promoted to complete semantic or repository coverage without a coverage and truncation ledger.",
  "possible_interpretations": [
    "Successful completion means the declared finite scope was fully covered.",
    "The mechanism reached a symbol, file, depth or time limit and only produced a partial view.",
    "Unsupported syntax or provider failure omitted part of the source graph.",
    "The result is intentionally a bounded sample and does not claim completeness."
  ],
  "required_evidence": [
    "The declared source scope and deterministic inventory denominator.",
    "Visited, emitted, skipped, unsupported and failed item counts with identities.",
    "Every slice expansion limit, stop condition and truncation reason.",
    "A fixture where a valid downstream relation exists just beyond one configured boundary."
  ],
  "minimal_counterexample": "A call-path slice reaches max_symbols before one downstream call edge, returns exit 0 and is published as a complete call chain without PARTIAL coverage or a truncation reason.",
  "false_positive_conditions": [
    "The finite scope and denominator are sealed and every member is accounted for.",
    "The result is explicitly partial and retains the exact boundary and omitted inventory.",
    "A separate complete provider proves the same declared coverage and the bounded result is not used as its substitute."
  ],
  "detectable_cues": [
    "exit 0, non-empty output or first match directly sets coverage to COMPLETE",
    "max_depth, max_symbols, max_files or timeout without a truncation field",
    "unsupported files disappear from the inventory denominator",
    "empty proposal or analyzer output is described as no issue"
  ],
  "non_claim": "This pattern does not require unbounded graph traversal or claim that every partial result is unusable. It requires bounded R1 views to expose exactly what was covered and why expansion stopped.",
  "provenance": "RA-004 rev1 was independently recomputed and selected only for R1 bounded coverage and truncation semantics. Rev2 freezes the same semantics for the first Corpus payload; it does not create an unbounded-analysis requirement."
}
```

### RA-008 rev2：可变源码别名替代精确快照坐标

```json
{
  "pattern_id": "RA-008",
  "record_revision": 2,
  "supersedes_digest": "sha256:49fcdc03c92734c0caf980a9ac37d8724868e94a9263f5da610d96065d6790c1",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:194cd1eae23cf3d063a41a9f0b5b3f664a19b3b4b283034acaee07bbddb2198f",
  "status": "FROZEN_PATTERN",
  "source_coordinate": [
    "VeriTrail R0 seed set main@fd944621ef9de7c4f377fa5bd91759f3f900c9a3 docs/87-review-pattern-ledger.md",
    "VeriTrail R1 Semantic Review Slice design@846d392145703f2406cc244cc1fdc0e573202e21 docs/85-post-core-review-attention-plugin-plan.md",
    "VeriTrail P1 corrected contract main@5b363637f59be9786d58eed61a14e3bd663dd6d8 docs/83-p1-structured-github-api-collector-contract.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "CoordinateStaleness",
  "suspicious_structure": "A mutable alias such as HEAD, latest, a branch name or an unbound working directory is used as the identity of the source from which inventories, relations and slices are derived.",
  "possible_interpretations": [
    "The alias is resolved once to an immutable commit and every artifact retains that resolution.",
    "Different pipeline stages resolve the alias at different times.",
    "The working tree is intentionally the subject and its full dirty-state identity is retained.",
    "The result is exploratory and makes no reproducibility or continuity claim."
  ],
  "required_evidence": [
    "The exact commit/tree or complete working-tree content identity used for the SourceSnapshot.",
    "The resolution time and resolver provenance for any mutable input alias.",
    "A rerun after the alias moves while the original snapshot remains addressable.",
    "Bindings from every CodeFact, relation, slice and coverage entry back to one SourceSnapshot identity."
  ],
  "minimal_counterexample": "Inventory resolves branch main to commit A, main moves to B before slice derivation, and both outputs are labeled as one SourceSnapshot because each stage only records the branch name.",
  "false_positive_conditions": [
    "The alias is resolved exactly once and the immutable resolved coordinate is propagated to every consumer.",
    "The subject is an intentionally mutable working tree whose file set, content digests and dirty state are captured atomically enough for the declared claim.",
    "The output is clearly marked exploratory and is not used as reproducible review evidence."
  ],
  "detectable_cues": [
    "HEAD, latest or branch names appear where an immutable source identity is required",
    "separate stages call rev-parse independently",
    "artifacts record repository URL and branch but no commit/tree or content digest",
    "dirty files are parsed without entering SourceSnapshot identity"
  ],
  "non_claim": "This pattern does not forbid friendly aliases at user entry. It requires R1 to resolve them once and bind all derived artifacts to the resulting exact SourceSnapshot or to retain an explicitly bounded working-tree identity.",
  "provenance": "RA-008 rev1 was independently recomputed and selected only for R1 SourceSnapshot coordinate identity. Rev2 freezes the same semantics for the first Corpus payload without forbidding friendly input aliases."
}
```

### RA-023 rev3：核验快照必须继续成为消费快照

```json
{
  "pattern_id": "RA-023",
  "record_revision": 3,
  "supersedes_digest": "sha256:cd9f19656476803f5c49138f5269bed3856705e5f3e98d900d631de08ae97d35",
  "record_canonicalization": "veritrail-json-c14n/1",
  "record_digest": "sha256:fcf5d2a2364aa89413ae6d9884380cf7a3ff3f43a309970230d3e204d91b538b",
  "status": "FROZEN_PATTERN",
  "source_coordinate": [
    "VeriTrail P3 contract main@589bbad7261cceda1aa3a6412278a48473a9b1b7 docs/92-p3-core-handoff-contract.md",
    "VeriTrail snapshot correction main@5d4e7bbbf706d92c98cf36418d6f86b5caf2d3d8",
    "VeriTrail P3 implementation main@c0bce6cb7a3c9f3684d1845beda355084f232d0a",
    "VeriTrail Pattern Corpus contract baseline main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a docs/109-review-attention-pattern-corpus-freeze-contract.md"
  ],
  "problem_layer": "Identity",
  "taxonomy_version": "review-attention-taxonomy/1",
  "pattern_class": "SnapshotContinuity",
  "suspicious_structure": "One layer safely reads and verifies source bytes or an imported artifact, but later derivation receives only the locator or a caller-owned mutable object and independently reconstructs what it consumes.",
  "possible_interpretations": [
    "The locator names an immutable content-addressed snapshot and every read is equivalent.",
    "The locator is mutable and can identify different bytes between verification and derivation.",
    "The verifier owns a stable copy but later code consumes a shared mutable decoded object.",
    "A storage or language-service boundary provides snapshot semantics that are not expressed in the API."
  ],
  "required_evidence": [
    "The exact source bytes or canonical imported snapshot and its digest.",
    "A deterministic replacement or mutation between verification and semantic consumption.",
    "The ownership and mutability contract of SourceSnapshot and every derived input object.",
    "Proof that inventory, relation and slice derivation consume the same verified snapshot without locator reread or caller mutation."
  ],
  "minimal_counterexample": "R1 verifies source archive A at path p, p is replaced with valid archive B, and a SemanticMapper rereads p while the resulting CodeFacts are described as derived from verified A.",
  "false_positive_conditions": [
    "The locator belongs to an independently enforced immutable content-addressed store.",
    "The later layer verifies and owns its own exact snapshot identity rather than relying on the earlier check.",
    "The same owned immutable snapshot object is passed across the boundary and its digest is rechecked before use."
  ],
  "detectable_cues": [
    "verify(path) followed by parse(path) or derive(path)",
    "a digest check returns only a filename or locator",
    "multiple safe reads are treated as proof of one snapshot",
    "an imported mapping or source buffer remains shared with mutable caller state"
  ],
  "non_claim": "This pattern does not prohibit path-based entry APIs or repeated reads from proven immutable storage. It requires the SourceSnapshot verified at the R1 boundary to remain the snapshot consumed by deterministic derivation.",
  "provenance": "RA-023 rev2 was independently recomputed and selected only for R1 SourceSnapshot continuity. Rev3 freezes the same semantics for the first Corpus payload without transferring source-state authority to the review plugin."
}
```

最终 Corpus 仍由独立 manifest 以这四条 frozen revision 的精确 digest 选择。Ledger 中未选记录没有被
删除、降级或判错；后续 closure 尚未绑定 payload 的 exact merged source commit，R1 仍保持 `BLOCKED`。
