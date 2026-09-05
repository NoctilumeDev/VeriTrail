# PC2 Acceptance Core 兼容与冻结事实 0.1

> 状态：`PC2_FROZEN / P1_NOT_STARTED`
>
> 主线基线：`78dc2c3c5bfdc95bfc8ef1cd5fbf8529d430c211`
>
> 最后一个 Core 运行语义提交：`ee6896ec7f6d969eefca4700f46a92f4e0144189`
>
> 完整本地候选提交：`91004e99aaf4d3fb5cbae29d00057eff00f0b68a`
>
> 受保护主线实现基线：`fa8a5acac753456d37325bb0d9fac1b85add912b`
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM`；只冻结并列 Acceptance 路径与旧消费者边界

## 1. 本轮结论

PC2 已完成合同要求的完整兼容、运行与交付验证。`AcceptancePlan -> AcceptanceReport ->
AcceptanceBundle` 仍与既有 `ExperimentPlan -> Report -> Bundle` 并列；没有 GitHub Collector、网络
probe、凭据、动态插件注册中心或 P1 代码。

本轮候选已通过远端 PR checks、受保护主线合入和公开文档读回，PC2 因而标记 `FROZEN`。这只解除
P1 的 Core 兼容前置阻断，不表示 P1 已经开始，也不把 Acceptance Core 扩张成已发布能力。

## 2. 冻结前发现并修复的语义缺口

反向审查发现：同一 Evidence 输入集合若同时包含一份合法同类型 Evidence 和一份 Core-owned
observation metadata 畸形的同类型 Evidence，PC1 会绑定合法件并忽略畸形件，可能得到表面 `PASS`。
这与“metadata 合同错误是 integrity blocker”的既有合同不一致。

`ee6896e` 只修正这一处：任何所需 evidence type 中出现 metadata 畸形候选，都以
`OBSERVATION_METADATA_INVALID` / `METADATA_INVALID` 阻断为 `INCONCLUSIVE`；合法件不能掩盖畸形件。
新增反例只改变“是否额外提供一份畸形同类型 Evidence”这一项，没有改变 Plan、合法 Evidence 或
其他规则。

## 3. 旧消费者矩阵

| 消费者 | PC2 结果 | 边界证据 |
| --- | --- | --- |
| ExperimentPlan 0.1–0.7 | 原语义保留 | validator、seal、代表 digest 随 Core 全量回归通过 |
| Comparison | 明确拒绝 | `UNSUPPORTED_BUNDLE_KIND`，不生成输出 |
| Pairing | 明确拒绝 | `UNSUPPORTED_BUNDLE_KIND`，不生成输出 |
| Batch | 明确拒绝 | `UNSUPPORTED_BUNDLE_KIND`，不生成输出 |
| Preflight / Browser / Command / Bootstrap run | 明确拒绝 AcceptancePlan | 在采集、读 ToolBindings 或启动 subject 前因 `plan_kind` 失败 |
| Catalog | 标记不支持 | 零 Run、一个 `UNSUPPORTED_BUNDLE_KIND` issue |
| Workbench | 明确拒绝 | `UNSUPPORTED_BUNDLE_KIND`，不按旧 Report 解释 |

识别逻辑没有复制到每个分析器。Python 消费者继续汇入既有受限 Bundle validator；Workbench 只在旧
manifest 缺失且新 Acceptance manifest 明确存在时返回稳定边界错误。普通缺文件、旧 Bundle 和历史
派生分析的路径均未改写。

## 4. 新 Acceptance 正负闭环

新增 `scripts/pc2_acceptance_core_freeze.py`，在 wheel clean install 中通过显式 CLI：

1. 封存一个平台无关、CPU-only、无网络的 AcceptancePlan；
2. PASS 与 FAIL 使用同一 sealed Plan、同一 collection session 和相同 coverage；
3. FAIL 只把 Render Evidence 的 `commit_sha` 从 `candidate-001` 改为 `other-visible-commit`；
4. 两包均逐文件重算大小和 SHA-256，独立重算 Plan、facts 与 Evidence identity；
5. 从封存文件重新导入 Evidence，再调用 Core 重算 derivation，并逐字段比对 JSON Report；
6. 检查跨 Evidence 两侧原值及各自 Evidence SHA，同时核对 Markdown；
7. 确认没有旧 Bundle 根文件名、原始敏感 canary 或 staging 残留。

Python 3.10 与 3.13 均从临时 venv 的 `site-packages` 导入构建 wheel，而不是从 checkout 的 `src`
目录导入；两边均得到 `PASS / FAIL` 和 `PC2_ACCEPTANCE_CORE_FREEZE_NOT_P1` 边界标记。Public CI 新增的
同名门禁也设置 `max-parallel: 1`，按 3.10、3.13 顺序消费对应 wheel artifact。

## 5. 本地串行验证事实

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| 全 Core 普通模式 | `383/383` | `383/383` |
| 全 Core `-O` 模式 | `383/383` | `383/383` |
| Starter 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring Skill 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| 两个 Authoring DRAFT preset | `PASS` / `PASS` | `PASS` / `PASS` |
| wheel clean install + 双 Acceptance Bundle | `PASS` | `PASS` |

Workbench 在实际 Node 依赖安装后完成 `173/173`、零警告 lint、type-check、生产 build 和 moderate
依赖审计零漏洞。所有本轮生成的 venv、wheel、npm 依赖、生产构建、缓存和临时 Bundle 已在取证后
清理；Git diff 敏感模式扫描没有发现凭据、个人路径或原始响应体。

Codex Security 深扫、攻击路径分析和极端环境攻击按既有范围继续不执行；本轮普通质量门不得冒充这些
安全能力。

## 6. 远端门禁、主线与公开读回事实

- [PR #26](https://github.com/NoctilumeDev/VeriTrail/pull/26) 从精确基线
  `78dc2c3c5bfdc95bfc8ef1cd5fbf8529d430c211` 审查候选
  `c0a7aa1de7aa8fb492db6e4187c0a1f5cd5becd3`，合并前状态为 `CLEAN / MERGEABLE`。
- [Public CI 运行 33962872171](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33962872171)
  的九项可见检查全部 `SUCCESS`：双 Python Core、E3 下载验收、Workbench、双 Python wheel-only、
  双 Python Acceptance Core freeze 与 Starter PASS/FAIL golden path。
- PR 于 `2026-09-05` 合入受保护 `main`，合并提交为
  `fa8a5acac753456d37325bb0d9fac1b85add912b`；随后远端 `refs/heads/main` 读回同一 SHA。
- 真实 GitHub 渲染页随后读回
  [README](https://github.com/NoctilumeDev/VeriTrail/blob/main/README.md) 与
  [本文](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/82-pc2-acceptance-core-freeze-candidate.md)：
  本文标题、候选阶段状态与 `P1_NOT_STARTED` 停止线均可见，README 的两处文档 82 链接均指向
  `main` 上的同一文件。公开渲染没有被 Git/API 结果代替。

以上事实关闭 PC2 的候选停止线。P1 当前仍为 `P1_NOT_STARTED`；是否开启 P1 必须另作明确施工决定。
本轮不创建 GitHub Collector，不决定 Core 新版本、标签或 Release。
