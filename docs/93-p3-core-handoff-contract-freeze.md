# P3 Core Handoff 合同冻结事实

> 后继状态：本文记录的冻结曾真实成立；P3-A 本地候选实现的组合审查又发现 handoff 核验与 Core 路径
> 重读之间无法证明同一快照。当前合同已按
> [第 13.1 节](92-p3-core-handoff-contract.md#131-连续安全读取不等于同一快照)只重开该边界，状态为
> `P3_CORE_HANDOFF_CONTRACT_0.1_REOPENED / P3_IMPLEMENTATION_PAUSED`。本文不因后继反例而改写历史证据。

> 状态发布目标：`P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`
>
> 状态发布重建基线：`main@befee158da6153ad2774aae7b8772ee3677133d0`
>
> 本文只记录已经发生的合同、门禁与公开读回事实；本补丁自己的远端门禁、受保护主线合入和合入后
> 精确匿名读回全部成立后，状态发布才生效。

## 1. 冻结对象

冻结对象是 [P3 Core Handoff 与真实正负链合同 0.1](92-p3-core-handoff-contract.md)，不是 P3 实现。
它只允许下一阶段从新的 exact main 串行开始：

```text
P3-A  manifest contract + canonical identity
```

冻结不会创建 manifest Schema、publisher、reference lab、示例 Plan 或 AcceptanceBundle，也不授权 P4、
Review Attention R1、Codex Security 深扫或任何 GitHub 写能力。

## 2. 候选与语义修正链

1. 合同候选由 PR #55 的原始 11 项公共门禁通过后，以 merge commit
   `ea6723a224b5430095c25398d872caf025210c99` 合入受保护主线；
2. 从该 exact main 运行产品 `PublicRenderCollector` 时，README 与合同正文均得到 `COMPLETE`；P 轨路线图
   因 GitHub Mermaid 子框架导航得到 `PARTIAL`；
3. 第一份路线图请求因 projections 非规范顺序在联网前被拒绝，没有创建浏览器或网络观察；该无效请求
   没有被包装成产品失败，也没有进入冻结证据；
4. 随后的 desktop 与 narrow 两次有效观察均确认：主文档 HTTP 200、requested/final URL 相同、作用域
   唯一可用、三样本稳定、无 truncation、marker 存在、collector errors 为空；唯一影响 coverage 的
   conflict 都是
   `NETWORK_POLICY_BOUNDARY / UNEXPECTED_PAGE_NAVIGATION / viewscreen.githubusercontent.com/markdown/mermaid`；
5. 因此“路线图必须 COMPLETE”的旧冻结假设被反例否决。PR #56 只修正文档观察边界，不删除 Mermaid、
   不放宽 P2、也不把 `PARTIAL` 升级成 `COMPLETE`；其原始 11 项门禁全部通过，并以 merge commit
   `9eb630c1c502cbae0f76c3e783084c412792bba1` 合入受保护主线。
6. 第一份状态发布 PR #57 的原始 Python 3.10 门禁在下载冻结 E1 Release 资产时遇到
   `curl (35) Recv failure: Connection was reset`。前序资产与同轮 Python 3.13 均成功，但后续依赖作业未
   运行；#57 因而关闭且未合并，没有用 rerun 或旧绿灯覆盖该失败；
7. 该失败不改变 P3 合同，但暴露了既有冻结资产下载只写 `--retry 3`、未把连接重置纳入有界恢复的 CI
   债务。独立 PR #58 为四个同类 Release 下载入口加入
   `--retry-all-errors --retry-delay 2 --retry-max-time 60`，保留全部 SHA-256 与 clean-install 验收；其原始
   11 项门禁全部通过，并以 merge commit `befee158da6153ad2774aae7b8772ee3677133d0` 合入主线；
8. 本状态发布从新的 exact main 重建，不复活 #57，也不把 CI 传输修复冒充 P3 合同或实现证据。

候选 merge `ea6723a...` 上保留的产品观察摘要为：

| 页面 | 结果 | Artifact SHA-256 | 关键事实 |
| --- | --- | --- | --- |
| README | `COMPLETE` | `f9ad236af2de78f40fbe94be261d1e51d9e076ede406e1eb5fee020ebb3ef4f4` | marker 2 次 |
| P3 合同 | `COMPLETE` | `a1842b56ef8af934f9778a7d7b64102285b5091ee8fcf54adef83b302b2d2564` | marker 1 次 |
| P 轨路线图 desktop | `PARTIAL` | `cdb15537e78540ded1c590c96d856812f6f4cc7ee7c846670b9b5b180edace3d` | Mermaid conflict；其余冻结条件成立 |
| P 轨路线图 narrow | `PARTIAL` | `155ff00f13c9fa3d9e6ad6b739eb96b3fa92d318766392d163883fff87569670` | 同一精确 Mermaid conflict；其余冻结条件成立 |

这些 Artifact 只记录候选期观察，不因后续成功而被改写或冒充新的 main 事实。

## 3. 修正后 exact-main 匿名读回

从 `main@9eb630c1c502cbae0f76c3e783084c412792bba1` 建立 detached worktree，并用该坐标内的 Core 与
GitHub Evidence Plugin 产品代码、fresh anonymous Chromium 串行读取三个精确 Markdown 坐标：

| 页面 | Coverage | Artifact SHA-256 | 读回摘要 |
| --- | --- | --- | --- |
| `README.md` | `COMPLETE` | `de0503c05f614d51c935a0503d742a46bb224c8cd7ff509433d6fd2817c2dce6` | HTTP 200；URL 不漂移；唯一作用域；三样本稳定；无 truncation/error/conflict；marker 2 次 |
| `docs/92-p3-core-handoff-contract.md` | `COMPLETE` | `c47e4e54112ef0591384b278f9269db7b2b0b9eafaf0ea9600b3770879b1e1c9` | HTTP 200；URL 不漂移；唯一作用域；三样本稳定；无 truncation/error/conflict；marker 1 次 |
| `docs/77-post-core-platform-plugin-plan.md` | `PARTIAL` | `75ad20fd66b19a51f90bd22be56b98266035c2bb88478894eb2e572490294308` | HTTP 200；URL 不漂移；唯一作用域；三样本稳定；无 truncation/error；marker 1 次；唯一 coverage conflict 为 Mermaid 子框架导航 |

路线图的网络摘要只包含一个影响 coverage 的
`UNEXPECTED_PAGE_NAVIGATION` 和一个不影响 coverage 的只读策略 `METHOD_NOT_ALLOWED`；没有额外错误、
额外冲突或不稳定。这个 `PARTIAL` 只满足合同冻结页的有界公开读回门，不进入 P3 reference slice 的正式
Acceptance Evidence，也不证明页面 `COMPLETE`。

同一 exact 坐标的补充产品读回 Artifact
`d42691984ab8d4c3a1bb6569426928f3724eea6f98b00f1eddb055fd84464c1f` 显式复核
`coverage_reasons = [FACT_CONFLICTS_RETAINED, NETWORK_POLICY_AFFECTED_COVERAGE]`，collector errors 为空，
唯一 conflict 仍为上述 Mermaid 子框架导航。此前一份缺少必需 HARD assertion 的临时 Plan 被公共
validator 在浏览器创建前拒绝，没有产生网络观察，也没有被算作页面失败。

## 4. 边界裁决

本轮冻结确认：

```text
Manifest = exact artifact selection + bounded handoff provenance
Manifest != semantic prevalidation
```

handoff 层只能验证闭合 Schema、role、显式 path、文件 SHA-256 和公共 Evidence importer；Plan/spec
binding、session integrity、coverage sufficiency、assertion 与四态 Verdict 全部留给 Core。路径逃逸、
摘要漂移或不可导入文件是 pre-Core handoff failure；语义不一致只有在可信 Evidence 已精确交接后才由
Core 裁决。

因此本合同冻结不会把：

```text
artifact selection
evidence interpretation
deterministic judgment
```

压成同一层，也不会让插件以“提前拒绝”吞掉 Core 本应保留的 `INCONCLUSIVE` 或 `PENDING`。

## 5. 本状态发布的最后门

本补丁只允许文档与索引变化。它必须独立完成：

1. 原始远端门禁全部通过，不以 rerun 覆盖红灯；
2. 受保护主线 merge；
3. fetch 新的 exact `origin/main`；
4. 从该 exact main 再次运行产品 Collector：README 与 P3 合同必须 `COMPLETE`；P 轨路线图必须
   `COMPLETE`，或只保留合同第 13 节规定的精确 Mermaid `PARTIAL` 闭集；
5. 确认仓库仍不存在 P3 manifest Schema、publisher、reference lab、示例 Plan 或 AcceptanceBundle 实现。

任一新反例都否决冻结资格。只有上述事实全部成立，以下状态才成为当前主线事实：

```text
P2_FROZEN
P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN
P3_IMPLEMENTATION_NOT_STARTED
P4_NOT_STARTED
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```
