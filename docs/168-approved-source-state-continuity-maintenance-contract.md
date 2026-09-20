# Core 获批源码状态连续性维护合同

> 身份：`CORE_MAINTENANCE_CONTRACT / IMPLEMENTED_ON_FIX_BRANCH / NOT_A_RELEASE_CLAIM`。
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM`。本修正只穿透 Approved Preview、Run-start
> source identity 与同计划复跑 Comparison；不授权 Git 身份、formatter/codegen、可变执行器、
> transformation lineage、GitHub Evidence Plugin 或 Review Attention R 的扩展。

## 真实反例

维护前，两个 Run 可以在不同起始源码状态上各自稳定执行并得到 `PASS`。只要 sealed Plan、Profile、
随机种子和冻结语义投影相同，Comparison 仍可能给出 `MATCH`。现有 `before_fingerprint ==
after_fingerprint` 只能证明单个 Run 期间没有漂移，不能证明 Run 开始时仍是操作者批准的 Preview
所对应状态。

维护过程中还观察到一次验收环境错绑：Python editable install 指向另一个 worktree，使测试显示绿色，
但实际没有执行待验补丁。它不作为本合同新增能力，却再次证明 source identity 与 execution identity
不能由报告中的路径或口头声明代替。

## 三道门

1. **Approval continuity**：M9 CommandPreview 与 M10/M11 BootstrapPreview 记录
   `policy_version + watch_roots + fingerprint`。同一 sealed Plan 可以在不同源码状态上生成并批准新的
   Preview；旧 Preview 的批准不能漂移到新状态。
2. **Run-start eligibility**：创建 verifier 进程、服务或运行工作区之前，重新捕获相同受保护表面的
   source snapshot。实际 fingerprint 不等于获批 Preview 时，拒绝启动，不生成伪装成正常 Run 的
   Evidence。
3. **Comparison eligibility**：Comparison 0.2 只有在两侧获批 source snapshot identity 完全相同，
   或该判据对旧 Plan 类型明确不适用时，才继续比较冻结语义投影。不同 identity 返回
   `INCONCLUSIVE / SOURCE_STATE_MISMATCH`；没有新保证的历史运行返回
   `INCONCLUSIVE / SOURCE_STATE_UNQUALIFIED`。两者都不计算普通 differences。

现有运行期只读连续性保持不变：成功通过起点门后，`runtime.before == runtime.after` 才能支持正常
结论；运行期修改仍以既有 contamination / subject drift 语义保留。

## 身份与版本

获批 source snapshot identity 由以下三项共同组成，不能只比较裸 digest：

```text
subject-tree-sha256/0.1
+ ordered subject_watch_roots
+ snapshot fingerprint
```

新增版本是 additive correction：CommandPreview `0.1.1`、BootstrapPreview `0.1.1 / 0.2.1`、
trusted-command collector `0.2`、bootstrap-lifecycle collector `0.2.1 / 0.3.1`、Comparison
`0.2` 与规则 `rerun-semantic/0.2`。旧 Preview Schema、Evidence 和 Comparison 0.1 保留可读；
可读不表示它们被追溯性证明拥有 approved-source continuity。

## Run-start 的有限定义

本合同中的 Run start 是：在创建 verifier 进程或 bootstrap 工作区之前完成受保护源码快照并核对
Approved Preview。它不声称提供不可变文件系统，也不声称消除快照检查与目标进程首次读取之间的全部
TOCTOU 窗口。当前边界由启动前核对与既有 before/after 运行期连续性共同组成；没有新的真实反例时，
不扩张为通用 snapshot filesystem。

## 必须保留的反证验收

- 同一 Plan 在 source X 与 Y 上各自 `PASS`：Comparison 不得 `MATCH`，必须保持零 semantic
  differences 并返回 `SOURCE_STATE_MISMATCH`。
- Preview 在 X 获批、Run 前改为 Y：必须在 verifier 未启动、工作区未创建时拒绝。
- Run 从 X 启动、运行中变为 Y：既有 source drift / contamination 证据继续成立。
- 历史 Bundle 与 Comparison 0.1：继续可读取，但不得自动获得新版 continuity qualification。

核心表述：**运行期间稳定，不等于运行起点获批；两次各自有效的运行，也不等于彼此可比。**
