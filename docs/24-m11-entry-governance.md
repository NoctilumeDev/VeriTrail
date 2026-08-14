# M11 入口治理与 M0-M10 当前复验

> 状态：`ENTRY_GOVERNANCE_COMPLETE / IMPLEMENTATION_NOT_STARTED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`（只复核冻结地基、当前回归与入口文档；不修改代码、Schema 或标签）
> M10 基线：`m10-v0.11.1` @ `f4efdd25c50b19077c61994bce3e2aca5244d5ec`
> M11 合同：Contract 0.2 首次冻结于 `eb39c0aaaaa3fb878899ab2c8685b0dae4d303de`
> 里程碑状态：M11 继续为 `PLANNED`

## 1. 目的

本轮只回答：在开始 M11 Gate A 实现前，M0-M10 冻结地基、M11 合同入口和当前开发环境是否仍可
消费？计划文字、历史标签和一次局部通过都不能单独回答这个问题。

本轮不重新移动 M0-M10 标签，不实现 Profile 0.2、Plan 0.7 或单 application 生命周期，也不生成
M11 Run/Bundle。M10 已完成的 16 GB 压力、内置浏览器物理键盘和完整公共退出矩阵仍由冻结文档承担；
当前代码树若未漂移，不为制造新数字无意义重跑压力矩阵。

## 2. 冻结基线与代码漂移

- `m10-v0.11.0` 和 `m10-v0.11.1` 标签仍存在，后者解引用到固定补丁提交 `f4efdd25...`；
- 当前 `main` 相对 `m10-v0.11.1` 的变更只涉及 README、治理指令和 docs；
- `src/`、`schemas/`、`tests/`、`web/`、`pyproject.toml` 与依赖声明没有实现差异；
- `git fsck --full --no-dangling` 通过；
- M11 Contract 0.2 已从 GitHub 公开读回 `eb39c0a...`，状态为
  `CONTRACT_FROZEN / TARGET_SELECTED / IMPLEMENTATION_NOT_STARTED`，README 的 M11 仍是 `PLANNED`。

因此本轮是在同一 M10 实现上重新检查当前环境与公共回归，不是创建新 M10 能力基线。

## 3. 当前资源起点

启动前只读采样约有 6.3 GiB 可用物理内存，C/D 盘分别约有 140/189 GiB 可用；Docker Desktop 与
`vmmemWSL` 未运行。测试严格串行，不启动 MySQL、Redis、RabbitMQ、Docker 或其他项目技术栈。

## 4. 自动化事实

| Gate | Current result |
| --- | --- |
| Python 3.10.6 full suite, retained first run | `260/262`；2 个 Chromium 生命周期失败，见第 5 节 |
| Python 3.10.6 focused reproduction | 单例 2/2、相关类 11/11、同进程重复负向与 Catalog 6/6 均 PASS |
| Python 3.10.6 full suite rerun 1 | `262/262 PASS`，126.697 s |
| Python 3.13.13 full suite | `262/262 PASS`，125.522 s |
| Python 3.10.6 full suite rerun 2 | `262/262 PASS`，128.473 s |
| 双 Python compileall / pip check | PASS / `No broken requirements found` |
| 双 Python editable metadata | 均为 `0.11.1.dev1`，指向当前仓库 |
| Workbench tests | `59/59 PASS`，2 workers |
| Workbench lint / type-check / production build | 全部 PASS；lint 0 warnings |
| npm audit（官方 registry） | production 0、完整依赖 0 vulnerabilities |
| production Workbench Chromium | `5/5 PASS`；66 请求，0 HTTP 错误，18777 已释放 |

production Workbench 使用当前 `web/dist`、仓库内脱敏 Bundle 和只读空 Catalog 兼容入口，覆盖桌面、
移动、本地包导入、损坏包拒绝、Console/Network 与同源路径。它是当前构建物的自动 Chromium 复验；
M10 已冻结的 Codex 内置浏览器物理键盘事实没有因文档变更失效，也没有被本轮自动化冒充重做。

## 5. 必须保留的不利事实

Python 3.10 首次全仓运行出现：

1. Browser 硬失败负向的 `result.browser` 意外为 `None`；
2. 一个公共 Catalog 正向 Run 的 Verdict 仍为 `PASS`，但 stderr 出现 Playwright pending task 与
   `TargetClosedError` 警告，因此测试按合同失败。

两条用例单独重跑、相关类顺序重跑、同一进程 5 次 Browser 负向加 Catalog 重跑均未复现；随后同
解释器两次完整全仓和 Python 3.13 一次完整全仓全部通过，结束后没有 Chromium、Python helper、
测试端口或 `.veritrail-*` staging 残留。本轮将其分类为
`TRANSIENT_NOT_REPRODUCED / RETAINED_DIAGNOSTIC`，不修改产品代码，也不把首次失败从记录中删除。

npm 首次使用当前 npmmirror 配置执行 audit 时，镜像返回 security endpoint 未实现；该次不产生漏洞
结论。随后只对当前命令指定官方 registry，production 与完整依赖均返回 0 vulnerabilities，没有修改
用户或项目的持久 npm 配置。

## 6. 清理与残留边界

- 18765-18891 当前无本轮 owned listener；没有本轮 Chromium、Python helper、Catalog 或 Workbench
  服务残留；仓库没有 `.veritrail-*` staging；
- production Workbench 自动验收生成的 3 个可重建文件保留在 OS TEMP 的
  `veritrail-m11-preentry-browser-20260814` 目录；删除命令被当前执行策略阻止，没有绕过；
- 这 3 个文件是明确具名的 acceptance JSON 与桌面/移动截图，不是运行服务、端口、用户数据或 Git
  产物。后续可以按授权清理，但本轮不能写成“临时输出为零”；
- M10 文档 21 已登记的历史诊断目录边界保持不变，本轮没有擅自清理用户缓存或历史证据。

## 7. 入口结论

M0-M10 当前实现没有相对冻结标签发生代码漂移，双 Python、Workbench、依赖与 production Browser
门禁在当前环境重新成立；首次 Chromium 瞬态和未删除临时输出均已显式保留。没有发现需要反向移动
M10 标签或先修改产品代码的稳定阻断项。

因此允许先完成 README、个人主页和方法论文档等入口枝叶整理；这些整理公开读回后，才按 Contract
0.2 从 Gate A 开始 M11 实现。直到 Gate A 代码提交真正出现，M11 必须保持
`PLANNED / IMPLEMENTATION_NOT_STARTED`，本文件不得被引用为 M11 功能通过。

## 8. 入口后的合同纠偏

Gate A 编码开始后的严格 validator 测试证明，Contract 0.2 第 8.1 节让一个 sealed Plan 同时绑定四个
不同 sealed Profile，与既有 `bootstrap_profile.profile_sha256` 权威关系矛盾。当前 Contract 0.3 已在
任何 Gate A Run 之前把 early-exit、readiness-timeout 和 owner-mismatch Profile 分别绑定到独立 Plan；
13 个出口、资源预算、裁决和 Gate A -> Gate B 门禁不变。本入口治理文档继续只证明进入 Gate A 时的
M0-M10 状态，不证明纠偏后的实现或运行已经通过。

## 9. 后继事实索引

Gate A 后续已完成 Profile 0.2、Plan 0.7、Preview 0.2、单 APPLICATION 生命周期、collector 0.3 和
全部公共消费者实现，并从 Run 1 重新完成 13 个预注册出口。该事实不回写本文件的历史入口结论；
准确自动化、运行、失败候选、资源、安全与边界见
[M11 Gate A 单应用能力验证](25-m11-gate-a-validation.md)。M11 仍为 `PLANNED`，Gate B 尚未开始。
