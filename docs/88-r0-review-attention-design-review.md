# R0 Review Attention 架构评审与冻结事实

## 1. 评审身份

- 评审对象：文档 85–87 与 README/AGENTS/milestones 入口；
- 分支基线：`origin/main@e539ad1129d66aac41a03f09222ac3dc42d4d764`；
- 设计候选合入：`main@411a43814632df8a5dc5ae4a9d4e66b11ab7aed1`；
- 影响等级：`L2_CONTRACT + L3_SYSTEM / DESIGN_ONLY`；
- 当前结论：`R0_ARCHITECTURE_FROZEN / PATTERN_LEDGER_OPEN / DESIGN_ONLY`；
- 保持状态：`P1_FROZEN / P2_NOT_STARTED`。

本文记录本地设计复核、远端门禁、受保护主线合入和公开读回；没有发生的 R1/P2 实现仍明确保持
未开始。

## 2. 草稿归纳结果

输入草稿覆盖了 AI 代码吞吐与人工理解吞吐失衡、审查注意力分配、人机责任、紫色提案语义、现实
模型反例以及“一切皆插件”等多个方向。本轮没有原样粘贴草稿，而是按四条稳定主线重组：

1. **Authority**：人拥有 Policy 与处置；Provider 拥有有界输出；Core 拥有 Verdict；Reality 拥有真相；
2. **Artifact**：事实、Evidence、Attention Proposal、Attention Map、HumanDisposition 和 Verdict 分离；
3. **Plugin boundary**：可替换能力全部走 Provider SPI，薄内核只保留合同、身份、状态和发现机制；
4. **Counterexample learning**：R0 宪法稳定，真实反例进入追加式 Ledger，P4 后再冻结 corpus snapshot。

## 3. 外部读者复核

| 读者问题 | 文档是否直接回答 | 位置 |
| --- | --- | --- |
| 这是什么？ | 是：帮助分配代码审查注意力的独立插件轨 | Plan 2–3 节、README 入口 |
| 它会替人找出并确认 bug 吗？ | 否：只产生关注提案，人作出处置 | Contract 2、5、11 节 |
| 为什么不直接放进 Core？ | Core 只拥有确定性 Verdict，R 是可卸载能力 | Plan 3、5 节 |
| “一切皆插件”会不会拆成很多服务？ | 否：允许同进程高内聚，禁止共享权威和实现依赖 | Plan 5 节 |
| 什么时候写代码？ | P4 与 Pattern Corpus 冻结之后才进 R1 | Plan 6、9 节；Contract 12 节 |
| 现在已有运行能力吗？ | 没有，状态始终标记 DESIGN_ONLY | 三份文档与 README |
| 新反例会不会反复打碎 R0？ | 不会；Ledger 开放，R0 宪法不随条目漂移 | Plan 7 节、Ledger 2 节 |

外部读者可以在 README 第一层得到正确心智模型，再按 Plan → Contract → Ledger 逐层进入；不需要先读
P1 实现历史才能理解 R 轨。

## 4. 语义现实反例复核

| 攻击问题 | 设计回答 | 结论 |
| --- | --- | --- |
| AI 和人同时能确认缺陷吗？ | AI 只有 AttentionProposal；确认属于 HumanDisposition | 边界闭合 |
| HumanDisposition 会不会冒充 Core Verdict？ | 两者身份、状态和 authority 分离；handoff 需独立 AcceptancePlan | 边界闭合 |
| 一个 Provider 成功会不会被当作完整审查？ | coverage、skipped、unsupported、failed 必须显式；success != completeness | 边界闭合 |
| 空提案是否会显示“没有问题”？ | 只能描述 observed scope 中没有 proposal，不能描述无问题 | 边界闭合 |
| 两个 Analyzer 是 fallback 还是 layering？ | 必须先确认替代/优先/覆盖/叠加语义并保留 provenance | 边界闭合 |
| 同一事实两次观察会不会被错误去重？ | Fact/Evidence/Proposal/Disposition/Run identity 分离 | 边界闭合 |
| 源码变化后旧行号会不会漂到新代码？ | 源码锚绑定 SourceSnapshot，变化后必须 STALE 或显式重映射 | 边界闭合 |
| AI confidence 会不会支配项目优先级？ | confidence 与 sealed ReviewPolicy priority 分开 | 边界闭合 |
| 第二个模型同意是否变成“独立证实”？ | 仍只是另一个 ProposalProvider 输出 | 边界闭合 |
| 插件目录分开但实际共享状态怎么办？ | 共享权威/可变状态/实现类型即判定为假分层 | 边界闭合 |
| 受审代码能否通过注释改写工具指令？ | 源码与相关文本是数据，不能改变 Policy、权限和命令 | 边界闭合 |
| R 轨会不会拖动 P2–P4 施工？ | 只追加 Ledger；R1 明确阻塞到 P4 与 corpus freeze | 边界闭合 |

## 5. 本轮反向修正

评审没有把第一稿默认当成完成，已在候选内修正四处：

1. `RiskProposal` 改为 `AttentionProposal`，避免命名先行宣布风险成立；
2. 增加 `AttentionStrategyProvider`，不把排序、聚合和去重启发式藏进 application；
3. 明确薄内核只含 Contract、identity、lifecycle、manifest validation 与 capability discovery；
4. 增加 Provider 误报/漏报/不支持范围的 corpus 责任，避免用“人最终负责”替插件免责。

这些修正没有扩大 R0 为实现阶段。

## 6. 分层闭环裁决

当前组合已经形成闭环，但不是把所有能力堆进一个进程的闭环：

```text
ReviewPolicy authority
    -> exact source
    -> bounded provider artifacts
    -> attention proposal/map
    -> human disposition
    -> immutable review bundle
    -> optional independent Core acceptance
```

每个箭头跨越的是版本化 Artifact，不是共享控制流。证据不足可以回到 Provider 补证；驳回不会删除
历史；插件卸载不破坏 Core；R 轨失败也不能改变 P 轨或既有 Verdict。因此它既保持功能闭环，也保持
组间边界。

## 7. 明确延期，不是假装完成

以下问题只有进入对应阶段才可冻结，本轮只给出边界：

- R1：SourceSnapshot/semantic inventory 的具体 Schema、语言支持与 coverage 算法；
- R2：Analyzer SPI、工具沙箱、执行环境与 corpus 测量；
- R3：模型 Provider、提案归一化、排序策略和 UI；
- R4：HumanDisposition 工作流、补证循环与并发处置；
- R5：ReviewBundle 到 AcceptancePlan 的精确映射；
- R6：安装、卸载、版本、标签、Release 与公开读回。

这些不是 R0 漏项；若现在提前冻结字段或实现，会把尚未获得的 P2–P4 反例排除在设计之外。

## 8. Freeze Gate

### 8.1 本地执行事实

本轮没有用后一次成功覆盖前一次环境问题：

1. 首次 `python -m unittest -q` 从另一 checkout 的旧 editable 安装导入 `veritrail`，缺少当前主线已有的
   Acceptance Core 模块；136 项中 37 项在 collection/import 阶段失败。该轮属于环境坐标错误，不能
   证明候选代码失败或通过；
2. 将 Core editable 安装显式绑定到当前 worktree 后，全量常规回归在 244 秒本地命令上限内无失败
   输出但未完成，因此记为 `INCONCLUSIVE_TIMEOUT`，不记 PASS；
3. 当前 worktree 上与插件边界直接相关的 AcceptancePlan/evaluation/reporting：常规 35/35、
   `python -O` 35/35；
4. GitHub Evidence 插件首次因本地包未安装在 import 阶段停止；绑定当前 worktree 插件后，常规
   57/57、`python -O` 57/57；
5. Markdown 相对链接、`git diff --check`、变更路径和非 Markdown R 轨实现文件检查均通过。

完整 Core、Starter、Authoring Skill、双 Python、wheel-only 和公开门禁仍必须由既有远端 CI 从干净
环境执行；本地定向通过不能替代远端完整矩阵。

| Gate | 当前事实 |
| --- | --- |
| 草稿已归纳而非原样堆叠 | `PASS_LOCAL_REVIEW` |
| 外部读者入口与层级 | `PASS_LOCAL_REVIEW` |
| Authority / Artifact / Dependency / Failure 反例 | `PASS_LOCAL_REVIEW` |
| 文档相对链接 | `PASS_LOCAL_CHECK` |
| 非 Markdown R 轨实现文件 | `NONE` |
| `P2_NOT_STARTED` | `CONFIRMED_IN_WORKTREE` |
| 远端 PR 门禁 | `PR #34 / 11 OF 11 SUCCESS` |
| 受保护主线合入 | `PR #34 MERGED` |
| 精确 main SHA 读回 | `411a43814632df8a5dc5ae4a9d4e66b11ab7aed1` |
| 未登录 README/Plan/Contract/Ledger/Review HTML 读回 | `PASS` |

### 8.2 远端与公开读回事实

1. 设计候选提交 `f221639cd14051f983fe46da5802b90d2c053b88` 从精确
   `main@e539ad1129d66aac41a03f09222ac3dc42d4d764` 起步；
2. [PR #34](https://github.com/NoctilumeDev/VeriTrail/pull/34) 的
   [Public CI run 33979104271](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33979104271)
   最终 11 个 job 全部 `SUCCESS`，包括双 Python、普通/优化 Core、Acceptance Core freeze、两套
   wheel-only、GitHub Evidence、Starter 黄金路径、Workbench 与 E3 下载复验；
3. PR #34 以 merge commit `411a43814632df8a5dc5ae4a9d4e66b11ab7aed1` 合入受保护 `main`，
   随后 `origin/main` 与匿名 `ls-remote refs/heads/main` 精确读回同一 SHA；
4. 内置浏览器两次在 GitHub 导航阶段超时，均未产生页面事实；公开网页读取器又返回仍处于 P1 候选的
   陈旧缓存副本。这三次失败没有被冒充为成功；
5. 最终改用无 Authorization/Cookie 的直接 HTTPS，读取 GitHub `blob/main` 与精确 commit HTML，
   [README](https://github.com/NoctilumeDev/VeriTrail/blob/main/README.md)、
   [Plan](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/85-post-core-review-attention-plugin-plan.md)、
   [Contract](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/86-review-attention-r0-contract.md)、
   [Ledger](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/87-review-pattern-ledger.md)与
   [本文](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/88-r0-review-attention-design-review.md)
   均实际返回 GitHub `Sign in` 匿名界面及各自 R0 标记；README 的 `blob/main` 与精确 commit 页面同时
   命中，证明这次不是 raw/API 替代，也不是只读到分支旧副本。

R0 停止线至此满足，状态升级为：

```text
R0_ARCHITECTURE_FROZEN
PATTERN_LEDGER_OPEN
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
P2_NOT_STARTED
```
