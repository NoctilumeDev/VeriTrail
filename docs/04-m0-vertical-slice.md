# 04. M0 纵向切片

## 状态

`AUTOMATED`。实现与自动化证据已经存在；提交后的干净工作区尚需再次完成真实 CLI 运行、
证据包核验和残留检查，之后才能更新为 `RUNTIME_VALIDATED` 或 `FROZEN`。

## 影响层级

- 声明层级：`L2_CONTRACT`；
- 所有者：VeriTrail Core；
- 直接消费者：CLI、JSON 报告导出器、Markdown 报告导出器和后续 UI；
- 预期爆炸半径：`ExperimentPlan 0.1`、`Evidence 0.1`、`Report 0.1`；
- 不在范围：SQLite、资源采样、浏览器采集、组合矩阵、Vue 和任意命令执行。

## 用户闭环

M0 只证明一件事：一个封存的单变量计划，可以导入结构化证据，在不执行项目命令的前提下
生成可追溯的确定性裁决包。

```text
plan.json
  -> validate
  -> canonicalize + SHA-256 seal
  -> redact and import evidence JSON
  -> evaluate assertions and variable drift
  -> PASS / FAIL / INCONCLUSIVE / PENDING
  -> report.json + report.md + manifests
```

CLI 只有两个动作：

```text
veritrail seal --plan PLAN --output NEW_FILE
veritrail evaluate --plan PLAN --evidence EVIDENCE --run-id RUN --output NEW_DIRECTORY
```

`--evidence` 可以重复，也可以不提供以形成真实的 `PENDING`。输出文件和运行目录一旦存在就
拒绝覆盖。Run ID 由调用者显式提供，使复跑创建新 Run，而不是覆盖旧事实。

## M0 裁决优先级

1. 已有硬性或降级边界断言失败：`FAIL`；即使执行状态为 `ABORTED` 也保留已证明的失败。
2. 基线过期、变量漂移、未知变量、证据冲突或规则类型错误：`INCONCLUSIVE`。
3. 执行未完成、必需证据缺失或决定性断言无法求值：`PENDING`。
4. 必需证据齐全、无污染且全部决定性断言通过：`PASS`。

体验目标与观察项不会抵消硬性事实。规则只读取已脱敏的持久化内容，因此报告使用的值与
证据包中的值一致。

## 安全与资源边界

- M0 只读取用户明确传入的 JSON，不执行其中的命令、HTML 或脚本；
- 证据在落盘前递归脱敏认证字段、常见令牌、私钥文本和用户目录；
- 单证据大小受计划中的 `max_artifact_bytes` 限制；
- 输出使用临时目录组装，成功后一次性改名；失败时不留下半成品；
- 证据文件名由序号、受限类型和内容哈希生成，输入文件名不能控制输出路径；
- 清单只写相对路径，避免把本机用户名或临时目录写进证据包。

## 退出条件

- 计划封存稳定，修改后校验失败；
- `PASS / FAIL / INCONCLUSIVE / PENDING` 均有确定性测试；
- `ABORTED + FAIL` 与 `ABORTED + PENDING` 均有测试；
- 敏感字段在持久化前被替换；
- 每个持久化证据和报告文件的清单哈希与实际字节一致；
- JSON 与 Markdown 报告 Verdict 一致；
- 已有输出不会被覆盖，重复证据不会生成重复副本；
- 使用仓库样例完成一次真实 CLI 运行，并确认输出目录可安全清理。
