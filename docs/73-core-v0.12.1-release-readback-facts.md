# Core 0.12.1 发布与公开读回事实

## 1. 最终结论与坐标

- 状态：`RELEASED / MAINTENANCE FROZEN`；
- 版本：`0.12.1`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.1>；
- 发布时间：`2026-08-25T16:57:36Z`；
- 注释标签：`v0.12.1`，tag object
  `0bdedebd27d35c093b6bfba575e1b81305375a10`；
- 标签解引用提交：`1d3e5a053dfca26837ec4293b11a17f016973413`；
- Release `targetCommitish` 字段：`main`；最终代码坐标以受保护注释标签解引用结果为准；
- 历史稳定标签 `v0.12.0` 未移动，Core `v*` 标签规则禁止删除和改写。

本文是[文档 71](71-core-first-run-maintenance-contract.md)停止线的执行事实，也是
[0.12.1 Release Notes](72-v0.12.1-release-notes.md)的公开读回闭环。它不重开 M0–M14，不扩张
Starter／Authoring Skill 权限，也不把合成 demo 冒充项目验收。

## 2. 精确合并后门禁

发布候选 PR #9 合并为 `81b9625d1246a352287256ff8cb1c3cc3b66de40` 后，
[Public CI 32863463458](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32863463458)
如实暴露 Starter S1 在 hosted Windows 上把 Chromium 冷启动限制为 3 秒的瞬态 FAIL。整改
[PR #10](https://github.com/NoctilumeDev/VeriTrail/pull/10)没有加入 retry，也没有降低断言；它只把
单次浏览器操作恢复为仓库其他真实浏览器样例使用的有界 10 秒，并增加实际裁决、失败断言与短期
artifact 诊断。

最终合并提交 `1d3e5a053dfca26837ec4293b11a17f016973413` 的精确 post-merge 门禁为：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 32872266734](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32872266734) | `SUCCESS`；Python 3.10／3.13 全矩阵、双 Python 无 checkout wheel-only、Starter 真实 PASS／故意 FAIL 链全部通过 |
| [Browser Smoke 32872266093](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32872266093) | `SUCCESS`；真实浏览器门禁通过 |

两个 run 的 `headSha` 均为上述最终合并提交，不以分支最新状态或其他提交的绿灯替代精确候选事实。

## 3. 发布资产与摘要

五个公开资产均从最终合并提交重新构建，没有复用旧 Release 资产：

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.12.1-py3-none-any.whl` | 197,553 | `6de3fb2ae4cd946a64872a05fbb845434ef627d2927585b8e4100bff4720ddd9` |
| `veritrail-0.12.1.tar.gz` | 279,360 | `dcdadf9a7c88ee7f72f6dd527a9f7497bd4af7e44f140f97f849cc273fce69cf` |
| `veritrail-workbench-0.12.1.zip` | 7,779,810 | `0d3b05ff8ff6849074bf4e0b7f0a5803bd13b7f46bc6ad63d15ff71c8c87e2a3` |
| `core-v0.12.1-validation-summary.json` | 5,407 | `5609cb22b2dbcad8f25c85b082c44d2166c346048187b590d55062e8215f4036` |
| `SHA256SUMS.txt` | 390 | `b034c7f160c0454c8080bc752782c9ad7694f61e8a2a6fd6b7b6c6b1df7975fe` |

`SHA256SUMS.txt` 使用非自指约定，覆盖前四个 payload；其自身由上传副本与公开下载副本逐字节比较。
GitHub 为五个 asset 返回的 `digest` 与上表逐项一致，公开下载后的本机文件大小和 SHA-256 也逐项
一致。

Workbench ZIP 与最终生产 `web/dist` 按内容逐文件比较为 `63/63` 一致；ZIP 中另有 4 个目录条目，
不是额外 payload。Core 维护版没有改变 Workbench 独立源码包版本，因此其内部
`web/package.json` 仍准确保持 `0.12.0`；`veritrail-workbench-0.12.1.zip` 表示它是随 Core 0.12.1
Release 重新验证并分发的伴随资产，不冒充 Workbench 独立语义版本升级。

## 4. 公开下载后独立复验

所有测试均使用 GitHub Release 公开下载副本，而不是构建 staging 中的原文件：

| 输入 | 环境 | 结果 |
| --- | --- | --- |
| wheel | Python 3.10.6 clean venv | 安装、`pip check`、`veritrail demo` 的 PASS／故意 FAIL、两 Run／零 issue Catalog 与边界标记全部通过 |
| wheel | Python 3.13.13 clean venv | 同上，全部通过 |
| sdist | Python 3.10.6 clean venv | 从 sdist 构建、安装、`pip check` 与完整 demo 通过 |
| Workbench ZIP | 独立解压与生产 `dist` 比较 | 63 个文件逐内容一致 |

生成的 JSON／Markdown 不含构建 staging 或本机绝对路径；demo 仍精确标记
`SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE`。这证明的是 Core wheel 的合成首跑合同，不证明
任何外部项目已经通过验收。

## 5. 边界与关闭条件

- 本次维护没有运行 Codex Security 深度扫描、攻击路径验证或极端环境攻击工作流；这些敏感工作流
  不属于本次有界发布停止线，也没有被绿灯暗示为已完成。
- macOS、Linux、C0/C2/C3、Docker、多服务、恶意代码隔离和通用项目自动探测仍不在证明范围内。
- GitHub Release 页面本身仍是平台允许维护正文的普通 Release；不可移动性由受保护注释标签、资产
  digest、下载读回和本文共同提供，不能把 `isImmutable: false` 误写成平台级不可变 Release。
- Starter 与 Authoring Skill 仍只生成 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`，不能 Seal、Run
  或裁决。

文档 71 的全部发布停止线已经满足。Core 0.12.1 因此可以准确描述为已发布、已公开读回并完成维护
冻结；后续修改必须使用新的提交与版本坐标，不能移动 `v0.12.1`。
