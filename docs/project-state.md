# VeriTrail 当前项目状态公开投影

> 本页是bounded current-state阅读投影，不是事实权威、状态机、roadmap scheduler、qualification record或施工授权。
> 完整append-only工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始PR attempt、exact-main gates、Artifact、
> fresh installed-product readback与independent reconciliation继续拥有各自事实。

## 投影身份

```text
projection_contract_candidate: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4
projection_status: CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
construction_exact_base: 27f0b93eeb5ace7b5428ebc0c07cb1ebe4199f25
construction_tree: f96b396e7bbdb42af9f4f6a75bbc8d730eede7af
source_binding_kind: FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes: 609477
source_milestones_sha256: dd815b3a598e781debbb5eb6291dc3d8032e8d374b1c852c40da953fae6011c7
source_milestones_blob_sha1: b250410a9641ecd13e7ff7fe2804b66a683433fe
```

这些坐标和摘要只声明本candidate由哪组不可变输入起草。milestones不保存自己的摘要，因而没有自引用；protected merge后的
exact commit/tree、公开可观察性与资格只能由外部完整资格链绑定。本文不能给自己升级状态。

## 当前有效事实

- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；
- `R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`；
- PR #398 private implementation已经合入，original/exact-main双门成立；旧milestones Render正确返回
  `PARTIAL / CONTENT_TRUNCATED`，该旧readback world仍保持`READBACK_NOT_QUALIFIED`；
- PR #399 original Public CI真实失败，未rerun、已关闭且未合并，lower resource cause保持`UNKNOWN`；
- PR #400–#414的公开投影failure-boundary、证明设施修正、维护与恢复publication均按各自exact world保留；后继PASS不回填旧失败；
- PR #415使projection 0.3成为qualified candidate，PR #416又完成独立freeze publication，因此
  `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN`已经生效；
- PR #417/doc365完成local、original PR、protected merge、exact-main双门、fresh六目标formal、两项raw-byte observation、
  independent reconciliation与finite closeout；因此#398/doc346现在是
  `IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`；
- #417第一个fresh root的README formal发生anonymous API budget exhaustion，第二个fresh root发生reader-visible marker target
  selection failure；两次Core Verdict均未创建，后继PASS不覆盖它们，底层原因保持`UNKNOWN`；
- 本页与[文档366](366-r1-public-project-state-projection-successor-0.4-contract.md)是从新的exact base重建的0.4 candidate；
  projection 0.3现在只承担冻结历史身份，0.4尚未资格化或冻结；
- Review derivation manifest negative-world successor、same-attempt derivation Evidence continuity、language-support persistence与
  public Review产品继续`NOT_STARTED / NOT_AUTHORIZED / OPEN`；R2–R6继续未启动。

## 必须继续可见的failure boundary

### #398 / #399入口失败

#398 milestones diagnostic观察到526260 UTF-8 bytes，超过frozen 524288-byte Public Render上限1972 bytes，故coverage为
`PARTIAL / CONTENT_TRUNCATED`；#399 required Python 3.13 fixture `git cat-file`在剩余acquisition budget内超时并正确映射
`SAFETY_BUDGET_EXHAUSTED`。两者不是同一world，也不能由#417 PASS覆盖。

### #401–#414公开投影恢复链

#401 marker drift、#402 Evidence持久化`FileNotFoundError`、#404 cancellation、#405 marker drift、#406/#410 anonymous API
exhaustion与#407/#408 HTTP 504预算耗尽继续保留各自run/head/job/target identity。后继failure-boundary audit、release-download
maintenance与recovery publication只证明自己的exact world，不重写首败或`UNKNOWN`。

### #417读回资格恢复的两个non-success world

第一次fresh root中README formal的anonymous API首个repository probe为`403 / COLLECTION_BUDGET_EXHAUSTED / remaining=0`，
Render仍`COMPLETE / 200`，Core Verdict未创建。第二次fresh root中API/Render均`COMPLETE / 200`，但选择的旧README
marker在source中一次、rendered text中零次，产品以`Render Evidence marker drifted`停止；这是readback target selection defect，
不是subject或candidate regression。第三个fresh root使用新的reader-visible marker取得独立PASS，不删除、不解释前两次失败。

## 权威边界

| 主体 | 权威 | 明确不拥有 |
| --- | --- | --- |
| Reality | 现实事实 | 被文档、测试或Verdict创造 |
| 用户/人类授权者 | 目标、验收前提与必要Seal决定 | 被Business Layer或Core替代 |
| Provider | 自己实际观察到的事实及来源 | 全局事实或裁决权 |
| R/Q/O/T | 各自合同规定的分析、观察和调度职责 | 越界扩张或共享隐性权威 |
| Business Layer | 业务流程组织、能力选择、补证请求 | 证据充分性裁决或PASS宣布 |
| Core | 证据完整性、绑定、充分性及确定性裁决 | 现实事实的超级所有权 |
| `docs/milestones.md` | 完整append-only工程历史、链接与provenance | 必须落入Public Render窗口 |
| 本页 | 当前candidate world的有界公开阅读投影 | source of truth、scheduler、qualification或施工授权 |

验迹内部可以有很多插件、Provider、分析器和调度器，但最终优化目标始终是用户提出的工程问题，而不是插件自身的存在价值。

## 本页不能做什么

本页不能：

- 替代、裁剪、重写或删除`docs/milestones.md`；
- 把短投影冒充完整历史已经被Public Render观察；
- 修改P2 oracle、Collector coverage或Core充分性规则；
- 把任何旧FAIL/ERROR/CANCELLED/UNKNOWN升级为PASS；
- 决定证据充分性、qualification、state transition或下一合法seam；
- 冻结#398 private implementation、恢复global composition authority，或启动manifest、Evidence、persistence、public Review、R2–R6。

## 本candidate的生效条件

只有[successor 0.4 contract](366-r1-public-project-state-projection-successor-0.4-contract.md)自己的local qualification、
original PR gates、protected exact-head merge、新exact-main Public CI与Browser Smoke、fresh anonymous installed-product
README/本页/doc346/doc364/doc365/doc366 Public Render、AGENTS/milestones public+API raw-byte observations、candidate milestones
binding复算、independent reconciliation与finite closeout全部成立后，本页才可成为
`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_QUALIFIED_CANDIDATE_NOT_FROZEN`。

即使这些门全部成立，后继仍须独立docs-only freeze publication；本页不是scheduler。
