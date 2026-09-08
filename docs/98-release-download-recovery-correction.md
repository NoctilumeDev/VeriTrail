# Release 资产下载恢复策略修正

状态：`IMPLEMENTATION_CANDIDATE`

变更级别：`L1_COMPONENT_INTERNAL`

本修正只处理 Public CI 对既有不可变 Release 资产的下载恢复策略，不改变 P4 合同、标签、Release、
资产名称、冻结 SHA-256、验收阈值或 Core/插件公共语义。

## 1. 触发事实与证据上限

P4 合同冻结候选 PR #72 的原始 Public CI run
[`34241218820`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34241218820) 在 Python 3.10
下载 `authoring-skill-v0.1.0/SHA256SUMS-authoring-skill.txt` 时连续四次收到 HTTP 500；同一工作流的
Python 3.13 路径完成了该步骤。后继匿名下载得到 `302 -> 200`、205 字节，SHA-256 为
`20684909030aa104cb3faadcb1707edcefa16be2b2832808ccd887996a8debfb`，与冻结值一致。该失败已在
[文档 97](97-p4-github-evidence-release-contract-freeze.md) 保留，PR #72 没有重跑或合入。

P4 合同冻结合入后的 `main@12130378febde2075d4cb9924628a07f9f26cb1e` 又在原始 Public CI run
[`34244325251`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34244325251) 的 E3 0.2 下载门
停止：`starter-v0.2.0/veritrail_starter-0.2.0.tar.gz` 连续四次收到 HTTP 500。后继匿名下载得到
`302 -> 200`、24910 字节，SHA-256 为
`d86b836cad6f5b0bf2fbe17ce3d86fb309fa1fb1f2e592b757ef4b0f5f48188d`，同样与冻结值一致。

两次失败发生在不同资产和不同门禁路径。既有策略使用固定 2 秒间隔与三次重试，因此全部重试等待
被压缩在约 6 秒量级；实际总耗时还包含各次 HTTP 请求。现有证据只支持以下边界：

```text
transient external failure duration
>
current recovery window
```

这些事实不证明 GitHub 内部根因、代理故障、仓库缺陷或资产漂移。GitHub Status 当时没有公开未解决
事故，也不能反向证明单次 Release 下载路径没有短暂失败。

## 2. 修正边界

四处重复下载统一委托给仓库内 CI 工具 `scripts/download_release_asset.py`。它只拥有下载、恢复、摘要
校验和目标文件发布责任：

1. 初次请求和所有重试共同消费一个 monotonic 绝对恢复预算，默认 60 秒；
2. 单次请求最多消费 15 秒，但不得刷新总预算；
3. 暂时性 HTTP `408 / 429 / 500 / 502 / 503 / 504` 与明确的 timeout、connection reset 等传输失败
   可按 `2 / 4 / 8 / 16` 秒有界退避；
4. `404`、证书验证失败、非法 URL、错误摘要、错误资产或已存在目标不因重试而被接受；
5. 每次尝试只写同目录内的独立 owned partial，失败即清理；
6. 只有完整流式读取后的 SHA-256 与冻结值相等，才以不覆盖语义发布目标文件；
7. 诊断只报告 attempt、失败类别、HTTP 状态、剩余预算和退避，不记录凭据。

因此：

```text
availability recovery
!=
integrity relaxation
```

## 3. 必需证据

本候选至少必须证明：

- `500 -> 503 -> success` 使用 `2 / 4` 秒退避并发布精确字节；
- `404` 立即失败，不重试；
- SHA-256 不一致立即失败，不重试；
- connection reset 与 timeout 可以在同一绝对预算内恢复；
- 多次请求和 sleep 共同消费一个 deadline，后续请求只取得剩余时间；
- 已存在目标在联网前拒绝；
- 部分响应、重试与最终失败后没有 owned partial 残留；
- 两套 Python 的普通与 `-O` 路径、既有 Core/Starter/Authoring/GitHub 插件回归和远端原始 Public CI
  保持成立。

在独立修正合入并从新 exact main 取得门禁事实前，P4 Release 实现继续暂停；旧失败不通过 rerun 洗白。

## 4. 本地候选证据

从 `main@12130378febde2075d4cb9924628a07f9f26cb1e` 创建的独立工作树中，本候选已取得：

- 下载状态机定向测试 11 项，在 Python 3.10/3.13 的普通与 `-O` 四组均通过；
- Core 403 项在同一四组均通过；
- Starter 24 项、Authoring Skill 24 项、GitHub Evidence Plugin 180 项分别在同一四组均通过；
- Workbench 173/173、lint、production build 与 `npm audit --audit-level=moderate` 通过，报告 0 个漏洞；
- Authoring Skill 的 `single-webapp` 与 `static-site` 真实 DRAFT 链在双 Python 上均为 `PASS`，并保持
  `NOT_RUN / NOT_SEALED / NO_VERDICT`；
- Core、Starter 与 GitHub Evidence Plugin wheel 在双 Python 上构建成功，Starter sdist 构建成功；逐个
  wheel 读回均未包含本 CI 下载脚本，产品包边界未扩张；
- fresh anonymous E1 真实公开下载与 clean-install readback 在 Python 3.10.6/3.13.13 上为 `PASS`，
  七项 Release 资产及 Core wheel 的下载摘要全部与冻结坐标一致；
- fresh anonymous E3 真实公开下载与 clean-install readback 在相同双 Python 上为 `PASS`，两个 preset、
  七项 Release 资产及 Core wheel 均成立，summary 与 draft 事实保持 `BYTE_IDENTICAL`；
- 两次真实探针产生的外部临时目录均已清理。

首次 Core 3.10 普通回归没有绑定当前工作树 `src`，测试源来自本候选，但 Python 实际从旧
`veritrail-r0-review-plugin` editable install 导入生产模块；该 337 项运行产生 2 个失败与 9 个导入错误，
只证明 execution provenance 错配，不能归因给当前补丁，也不构成通过证据。随后显式读回 3.10/3.13 的
`veritrail.__file__` 均指向当前工作树，再从头取得上述 403 × 4 有效结果。旧无效运行没有被后继绿灯
改写成产品失败或成功。

以上仍是本地候选事实。只有独立 PR 的原始远端门禁、受保护主线合入和新 exact main 的后继读回成立后，
本恢复策略才可成为后续 P4 发布实施的地基。
