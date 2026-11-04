# VeriTrail 当前项目状态公开投影

> 本页是 bounded current-state 阅读投影，不是事实权威、状态机、roadmap scheduler、qualification record 或施工授权。
> 完整 append-only 工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始 PR attempt、exact-main gates、Artifact、
> fresh installed-product readback 与 independent reconciliation 继续拥有各自事实。

## 投影身份

```text
projection_contract_candidate: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2
projection_status: CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
source_exact_base: 34de9427d64ba8a3c77ac38eefe146fa8d2e2d77
source_tree: f6edc136e2bd156409fad553c6453ceee73ccd97
source_milestones_bytes: 568856
source_milestones_sha256: d468191fcfbbaa8df31f592db35e494a8363ddd4f9c1c735dec26ab41a495ccf
source_milestones_blob_sha1: 18645a09f3a1f11406b4c54f501dd265eb44c072
```

这些坐标只说明本候选由哪组不可变输入起草。候选合入后的 commit/tree 只能由 protected merge 与外部资格证据绑定；本文不创建
自引用摘要，也不能给自己升级状态。

## 当前有效事实

- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；
- `R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`；
- PR #398 的 private implementation 已合入 `main@6a30957429c7b6a815608e8355893deb35873f24`，且 original/exact-main
  Public CI 与 Browser Smoke 均为 attempt 1 SUCCESS；
- PR #398 的 fresh README/doc345/doc346 formal readback 各有唯一 PASS，但 milestones diagnostic 正确返回
  `PARTIAL / CONTENT_TRUNCATED`，所以 #398 继续为 `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED /
  NOT_FROZEN`；
- PR #399 original Public CI `41908195831` attempt 1 真实 FAILURE，PR 没有 rerun、已关闭且未合并；
- PR #400 已把两条失败链的边界审计合入 `main@34de9427d64ba8a3c77ac38eefe146fa8d2e2d77`，并完成自己的
  original/exact-main gates、fresh changed-target observations、independent reconciliation 与 finite closeout；doc348 现为
  `FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
- 本页与 doc349 是新 exact main 上的独立 successor 0.2 candidate；public project-state projection 仍未生效。

## 必须继续可见的 failure boundary

### #398 readback boundary

milestones diagnostic 观察到 526260 UTF-8 bytes，超过 frozen 524288-byte Public Render 上限 1972 bytes，故 coverage 为
`PARTIAL / CONTENT_TRUNCATED`，formal 没有运行。Collector behavior 符合 frozen P2 contract；Collector regression 与 private
runtime semantic regression 均未建立。后继不能提高上限、把 PARTIAL 改名为 COMPLETE、补跑该 formal 或拼接三个已有 PASS。

### #399 original gate boundary

required Python 3.13 job 中 fixture `git cat-file` 在剩余 `3.1687451000000237` 秒 acquisition budget 内超时，产品正确映射
`SAFETY_BUDGET_EXHAUSTED`。candidate regression 与 product defect 未建立；runner/subprocess stall 已观察，lower resource cause
保持 `UNKNOWN`。same-run Python 3.10 PASS 与 prior exact-base Python 3.13 PASS 不能拼成 #399 资格；failed-head doc347 和
project-state bytes 不在 main 中复用。

### #400 proof-facility history

README formal #1 marker drift ERROR、doc348 diagnostic #1 marker multiplicity、worktree/bootstrap/PowerShell/public-bytes setup errors与
stdout self-capture mismatch继续按原 identity 保留；后继 PASS 不覆盖它们。

## 本投影不拥有的权力

本页不能：

- 替代、裁剪、重写或删除 `docs/milestones.md`；
- 把短投影冒充完整历史已被 Public Render 观察；
- 修改 P2 oracle、Collector coverage 或 Core 充分性规则；
- 把 #398 升级为 readback qualified/frozen，或把 #399 恢复为 qualified；
- 决定证据充分性、qualification、state transition 或下一合法 seam；
- 恢复 global composition authority，或启动 manifest、Evidence、persistence、public Review、R2–R6。

## 本候选的生效条件

只有[successor 0.2 contract](349-r1-public-project-state-projection-recovery-successor-contract.md)自己的 local qualification、
original PR gates、protected merge、新 exact-main Public CI 与 Browser Smoke、fresh anonymous installed-product
README/本文/contract Public Render、AGENTS/milestones public+API raw-byte observations、independent reconciliation 与 finite closeout
全部成立后，本投影才可成为 `QUALIFIED_PROJECTION_CANDIDATE / NOT_FROZEN`。

即使这些门全部成立，后继仍须独立 docs-only freeze publication；本文不是 scheduler。
