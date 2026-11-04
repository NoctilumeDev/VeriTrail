# VeriTrail 当前项目状态公开投影

> 本页是有界的公开阅读投影，不是事实权威、状态机、roadmap scheduler 或施工授权。
> 完整 append-only 工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始 PR attempt、
> exact-main gates、Artifact、fresh installed-product readback 与 independent reconciliation 继续拥有各自事实。

## 投影身份

```text
projection_contract_candidate: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_1
projection_status: CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
source_exact_base: 6a30957429c7b6a815608e8355893deb35873f24
source_tree: 81790b398fb3d07ed53d67269b80d99d94675807
source_milestones_sha256: 5c16f46bcd407cd8932a1233c25afe306288f916e04a41c6cf7dcfae77a6c926
source_milestones_bytes: 565121
```

这里记录的 exact base 和 milestones SHA 只说明本候选从哪一组不可变输入起草。候选合入后的 exact-main
commit/tree 由受保护合入与外部资格证据绑定，不能在本文内部创建自引用摘要。

## 当前有效事实

- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；
- `R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`；
- PR #398 的 private implementation 已精确合入 `main@6a30957429c7b6a815608e8355893deb35873f24`，
  original Public CI、exact-main Public CI 与 Browser Smoke 均为 attempt 1 SUCCESS；
- PR #398 的 fresh README、doc345、doc346 formal readback 各有一个保留的 qualifying PASS；
- milestones diagnostic 在同一 exact main 正确返回 `PARTIAL / CONTENT_TRUNCATED`，因此 PR #398 当前只能是
  `MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`。

## 必须继续可见的失败边界

同一安装产品、同一目标路径下，exact base `aa0cd335a98269dcdb843645f9643c0e7982a5c8` 的控制诊断为
`COMPLETE`；PR #398 exact main 的首次且唯一 milestones diagnostic 观察到 526260 UTF-8 bytes，超过冻结的
524288-byte Render 上限 1972 bytes，返回 `PARTIAL / CONTENT_TRUNCATED`。Collector 符合
[P2 Public Render 合同](89-p2-public-render-collector-contract.md)；Collector regression 与 private runtime semantic
regression均未建立。失败 closeout、三项既有 PASS、所有 setup failure 与 UNKNOWN identity 均继续保留，不能被本投影覆盖。

## 本投影不拥有的权力

本页不能：

- 替代、裁剪、重写或删除 `docs/milestones.md`；
- 把自己的简短内容冒充完整历史已经被 Public Render 观察；
- 修改 512 KiB oracle、Collector coverage 或 Core 充分性规则；
- 把 PR #398 升级为 qualified/frozen；
- 恢复 global composition authority，或启动 manifest、Evidence、persistence、public Review、R2–R6。

## 候选生效条件

只有[恢复合同](347-r1-public-project-state-projection-recovery-contract.md)自己的 local qualification、original PR gates、
protected merge、新 exact-main Public CI 与 Browser Smoke、fresh anonymous installed-product README/本文/合同正文 readback、
完整 milestones public raw bytes SHA 对账、independent reconciliation 与 finite closeout 全部成立后，本投影才可升级为
`QUALIFIED_PROJECTION_CANDIDATE / NOT_FROZEN`。后继仍须独立 docs-only freeze publication；文档编号不自动授权下一步。
