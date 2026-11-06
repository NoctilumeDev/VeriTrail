# VeriTrail 当前项目状态公开投影

> 本页是bounded current-state阅读投影，不是事实权威、状态机、roadmap scheduler、qualification record或施工授权。
> 完整append-only工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始PR attempt、exact-main gates、Artifact、
> fresh installed-product readback与independent reconciliation继续拥有各自事实。

## 投影身份

```text
projection_contract_candidate: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3
projection_status: CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
construction_exact_base: e5e8c8895e811f858850ae5f5094f7595eac9120
construction_tree: 8848573c63db3561f9e23662a4524f360c0d4480
source_binding_kind: FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes: 599729
source_milestones_sha256: 4ad66def6e220eca45c334f65222022f5d5ace0ea5ad458873082acd0bd85fec
source_milestones_blob_sha1: b2b983cacde0a6990d394a1087d92a3b78c83291
```

这些坐标和摘要只声明本candidate由哪组不可变输入起草。milestones不保存自己的摘要，因而没有自引用；protected merge后的
exact commit/tree、公开可观察性与资格只能由外部完整资格链绑定。本文不能给自己升级状态。

## 当前有效事实

- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；
- `R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`；
- PR #398 private implementation已经合入，original/exact-main双门成立，但fresh milestones Render正确返回
  `PARTIAL / CONTENT_TRUNCATED`，所以仍是`MERGED / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #399 original Public CI真实失败，未rerun、已关闭且未合并，lower resource cause保持`UNKNOWN`；
- PR #400/doc348 gate failure-boundary audit已经完成自身完整资格链，是qualified history；
- PR #401已合入project-state 0.2 candidate并通过exact gates，但唯一README formal发生source/render marker drift，故0.2仍
  `MERGED / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #402/doc350 exact gates通过，但唯一README formal在Acceptance Bundle持久化时触发`FileNotFoundError`，Verdict未创建；
- PR #403/doc351把该bundle-persistence failure boundary资格化，底层文件系统机制继续`UNKNOWN`；
- PR #404的doc350 recovery 0.1 original gate在35分钟outer containment budget下`CANCELLED`，已关闭、未合并、未rerun；
- PR #405/#406分别保留doc353 marker drift与doc354 anonymous API exhaustion；旧formal和未运行目标没有重跑或拼接；
- PR #407/#408在不同required lane、不同Release asset上各自耗尽60秒HTTP 504恢复预算，均关闭、未合并、未rerun；
- PR #409只把两个被击中的multi-asset lane显式改为120秒，已完整资格化为
  `RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN`；
- PR #410 unique README formal在Render COMPLETE时遭遇anonymous API额度耗尽，Core Verdict未创建；
- PR #411/doc359、#412/doc360、#413/doc361分别完成自己的failure-boundary/recovery资格链，不回填旧world；
- PR #414/doc362已完成original/exact-main双门、fresh README/doc350/doc361/doc362 formal、AGENTS/milestones raw观察、
  independent reconciliation与finite closeout，因此doc362是qualified history；
- [文档363](363-r1-public-project-state-projection-recovery-successor-0.3-contract.md)与本页是从新的exact base重建的0.3
  candidate；public project-state projection仍未生效。

## 必须继续可见的failure boundary

### #398 / #399入口失败

#398 milestones diagnostic观察到526260 UTF-8 bytes，超过frozen 524288-byte Public Render上限1972 bytes，故coverage为
`PARTIAL / CONTENT_TRUNCATED`；#399 required Python 3.13 fixture `git cat-file`在剩余acquisition budget内超时并正确映射
`SAFETY_BUDGET_EXHAUSTED`。两者不是同一world，也不能由后继PASS覆盖。

### #401 / #402公开投影读回失败

#401 README exact source marker一次、fresh rendered text零次；产品fail closed。#402的新world中marker稳定出现、API/Render
均COMPLETE且cleanup完成，但Acceptance Core在Verdict前持久化Evidence时对271字符本地目标触发`FileNotFoundError`。legacy
Windows `MAX_PATH`只保留为hypothesis，底层机制为`UNKNOWN`。0.3不得把这些失败改写成从未发生。

### #404–#410后继失败链

#404 cancellation、#405 marker drift、#406/#410 anonymous API exhaustion以及#407/#408 HTTP 504预算耗尽均保留原run/head/job/
target identity。#409 maintenance只证明被击中的两个lane在自己的新world资格化；doc359–doc362只证明各自publication。

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
- 恢复global composition authority，或启动manifest、Evidence、persistence、public Review、R2–R6。

## 本candidate的生效条件

只有[successor 0.3 contract](363-r1-public-project-state-projection-recovery-successor-0.3-contract.md)自己的local qualification、
original PR gates、protected exact-head merge、新exact-main Public CI与Browser Smoke、fresh anonymous installed-product
README/本页/doc349/doc350/doc362/doc363 Public Render、AGENTS/milestones public+API raw-byte observations、candidate milestones
binding复算、independent reconciliation与finite closeout全部成立后，本页才可成为
`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_QUALIFIED_CANDIDATE_NOT_FROZEN`。

即使这些门全部成立，后继仍须独立docs-only freeze publication；本页不是scheduler。
