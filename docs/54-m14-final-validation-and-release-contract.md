# M14 整改后终局复验与发布收束合同 0.1

## 1. 状态与权限

本文在 2026-08-22 冻结 M14 的执行边界。冻结后，M14 状态为
`CONTRACT_FROZEN / VALIDATING`；它不是功能开发里程碑，也不授权借终验之名改变已经冻结的
Schema、裁决语义、命令信任模型、Catalog/API 或 Workbench 信息架构。

M14 只允许：

- 为终验增加独立、可重复、拒绝覆盖的验收编排与脱敏摘要；
- 修复终验真实暴露且仍属于原所有者的缺陷，并完整复跑受影响消费者；
- 更新安装、使用、安全、限制、故障排查、里程碑历史、版本和发布元数据；
- 在全部硬门禁通过后构建、校验、签署校验和、打不可移动标签并创建首个最终 GitHub Release。

任何 L2/L3 语义变化、新平台、新冷状态、新目标适配器、新产品能力或无关全仓重写都必须停止
M14，回到独立合同。必需链路因资源、权限、网络或外部状态无法完成时，M14 保持 `PENDING`，
不得用局部测试、历史日志或 M13 证据代替。

## 2. 分层声明

| 层级 | M14 允许范围 | 禁止事项 |
| --- | --- | --- |
| L0 | 文档、发布说明、校验和清单、脱敏事实摘要 | 夸大证据范围或删除历史失败事实 |
| bounded L1 | M14 专属验收器、只读浏览器复验、临时目标检出与清理 | 改写 M11/M12 冻结验收器，或让测试替代真实页面/F12 检查 |
| L2 | 最终包版本、Workbench 版本、构建与 Release 元数据 | 修改冻结 Schema、Loader、Catalog/API 或裁决规则 |
| L3 | 不授权 | 进程所有权、信任边界、状态机或证据权威关系重构 |

若候选差异触及 L2 产品语义或 L3，必须把受影响基线标记为失效并停止发布；不能用 CSS、测试
夹具或后置文档掩盖。

## 3. 候选坐标与版本策略

### 3.1 入口候选

- VeriTrail 仓库：`https://github.com/NoctilumeDev/VeriTrail.git`；
- M14 合同起草入口：`a9308c1987497dc308855cbb32ab28007c7efd85`；
- 入口要求：本地 `main`、`origin/main` 与入口提交一致，工作树干净；
- M12 冻结标签 `m12-v0.13.0` 继续不可移动并精确指向
  `5f32c33ab3dac076151a4fcd9a93a74ccafcfaa9`；
- M11 GitHub 预发布与全部历史里程碑标签只读保留。

入口提交只用于说明合同从何处开始，不预先等于最终 Release 提交。最终候选必须在事实文档中
记录完整 SHA，并从 GitHub 重新读回。

### 3.2 最终版本坐标

M14 预注册的稳定版本为：

- Python 包：`0.12.0.dev1` -> `0.12.0`；
- Workbench：`0.12.0-dev.1` -> `0.12.0`；
- 最终 Git 标签与 GitHub Release：`v0.12.0`。

理由：`m11-v0.12.0` 是不可移动的里程碑标签，而 M11 GitHub 预发布已明确绑定
`0.12.0.dev1`，并把首个最终 Release 权限保留给 M14；`m12-v0.13.0` 是表现层里程碑寻址坐标，
从未把 Python/Workbench 包版本升到 `0.13.0`。因此 M14 将已有开发候选收束为同一语义版本的
稳定 `0.12.0`，不改写 M12 标签，也不伪造未存在的 `0.13.0` 包演进。

版本只在候选全链路第一次通过后修改；修改后必须重新运行静态、双 Python、前端、构建安装、
浏览器和安全门禁。任一门禁失败时不得创建 `v0.12.0` 或最终 Release。

## 4. 双目标冻结

### 4.1 自身目标

自身目标使用 M11 Gate A 已冻结的单 application helper 和 13 个公共出口。M14 不修改该冻结
合同，只以当前候选重新执行：

- 正向、选择器负向、资源 STOP/ABORT、端口竞争；
- dependency/application 提前退出、readiness 超时、user cancel；
- subject/staging 漂移、重复与受控微并行；
- Bundle 重建、哈希、Catalog 和正向恢复 Comparison。

### 4.2 不同类型真实目标

真实目标冻结为 InkNarratives 公共远端 `main`：

- 仓库：`https://github.com/NoctilumeDev/InkNarratives.git`；
- 精确提交：`076be2f92194b90e31535d4583ac4d5e72922794`；
- 目标类型：零生产依赖的多页面静态叙事站点；
- 目标原生门禁：`node scripts/verify-repository.mjs`；
- 稳定入口：`/`、`/works/darkroom/`、`/works/liuyong/`、`/works/sushi/`、
  `/works/wangwei/`、`/works/night-voyage/`；
- 首页代表性断言：`h1` 为“墨叙”、`#works` / `#works-title` 可见，五个 `data-work` 条目与
  对应 `data-work-link` 可访问；代表作品页必须有可见主标题、返回画廊入口和目标自己的既定交互。

本机现有 InkNarratives 工作副本当前位于已删除上游分支，且包含三项用户未提交修改。该目录
只读保留，绝不能 reset、checkout、stash、clean、提交或作为发布证据。
M14 只在唯一、可删除的临时独立 clone 中检出上述精确提交；验收前后记录 ref、clean 状态与原生
门禁，完成后按已解析绝对路径清理临时 clone。

M14 为新精确 ref 建立专属真实目标验收器，不改写 M11 Gate B 冻结脚本。预注册顺序为：

1. positive：`COMPLETED / PASS`；
2. browser-negative：`COMPLETED / FAIL`；
3. port-conflict：`ABORTED / PENDING`；
4. recovery-positive：`COMPLETED / PASS`；
5. 两个正向 Run 的 Comparison：`MATCH`，0 项语义差异。

任何观察结果都不能反向修改上述出口；需要纠正断言时必须升验收计划版本并保留旧失败事实。

## 5. 资源、串行与残留门禁

本机只有 16 GB 内存，M14 全程严格串行；一次只允许运行一个重型 Python/Node/Chromium 波次。
除 Gate A 已预注册的受控微并行外，不证明通用并行或生产容量。

- 启动 Chromium 前可用物理内存必须 >= 4096 MiB；
- 可用内存 < 3072 MiB 时软停止，不开启新重型波次；
- 可用内存 < 2048 MiB 时硬中止当前 M14 波次并封存 `PENDING`；
- 每一波使用独立固定回环端口、输出目录、临时 clone 和 staging；
- 输出目录必须不存在，验收器拒绝覆盖；
- 波次结束后端口、owned process、Chromium、线程、SQLite sidecar、staging 和临时目标必须为 0；
- 不启动 Docker、数据库、中间件或与合同无关的后台服务。

证据目录只能保存脱敏 Bundle、Catalog、浏览器摘要、资源曲线、命令退出码和 SHA-256；不得保存
凭据、环境变量、Authorization、真实个人路径、完整代理配置或未审查截图。

## 6. 终局执行矩阵

### 6.1 候选与依赖

1. 工作树、分支、远端、历史标签和合同 SHA 精确读回；
2. `git diff --check`、敏感/绝对路径/旧临时端口/历史空态残留扫描；
3. Python 3.10 与 3.13 全量测试，均不得跳过适用测试；
4. Workbench `test`、`lint`、`type-check`、生产 `build`；
5. Python `pip check`、锁定依赖核验，前端 `npm audit --omit=dev` 与完整 audit；
6. 当前工作树安全差异扫描；候选固定后再做一次标准全仓安全扫描；
7. InkNarratives 临时 clone 的精确 ref、clean 状态和原生门禁。

### 6.2 真实链路

按“自身目标 -> 清理 -> InkNarratives -> 清理”的顺序执行，禁止交错。两者均必须覆盖冷启动、
正向、适用负向、失败恢复、Bundle 逐字节重建、Manifest/附件哈希、Catalog 重建与只读消费。
适用的重复、超时、中止、资源停止、端口竞争、受控微并行和多实例只在对应冻结合同内复验。

### 6.3 派生分析

- 自身目标正向重复与 InkNarratives positive/recovery 分别运行适用的 Comparison；
- Comparison、PairedAnalysis、BatchAnalysis 的既有兼容回归夹具必须全部重跑；
- 真实目标不凭路径或视觉相似性强行运行 Pairing/Batch；只有另行预注册且具备因果/维度语义时
  才适用，本合同中二者对真实目标记为 `NOT_APPLICABLE`；
- 来源损坏、Plan 不同、变量污染和证据不足必须继续得到既定拒绝或三态结论。

### 6.4 用户可见浏览器

自动化与人工验收必须同时覆盖：

- 1440×960 桌面、390×844 与 360×800 移动视口；
- Runs、详情、Comparison、Pairing、Batch、Browser Evidence、空态、损坏恢复；
- 键盘焦点、展开/收回闭环、返回目录/history、长文本和多行边界；
- Console 无未知 error，Network 无外网、写请求和未知 4xx/5xx；
- 普通与 `python -O` 验收均使用显式硬门禁；
- 最后在 Codex 内置浏览器逐页检查真实呈现、交互和 F12 事实，不能只看测试或日志。

## 7. 构建、安装与 Release 资产

最终版本提交通过第 6 节后，从同一个干净提交构建：

- `veritrail-0.12.0-py3-none-any.whl`；
- `veritrail-0.12.0.tar.gz`；
- `veritrail-workbench-0.12.0.zip`（生产 `web/dist`，不得包含源码缓存或本机路径）；
- `m14-validation-summary.json`（脱敏、机器可读的门禁与环境摘要）；
- `SHA256SUMS.txt`（覆盖全部发布资产）。

Wheel 与 sdist 必须分别在新的临时虚拟环境安装，验证 import、CLI `--help`、版本读回和一条最小
封存/裁决链；Workbench zip 解包后必须与候选 `dist` 文件清单及 SHA-256 一致，并以独立只读
回环服务通过桌面/移动 smoke。构建目录、压缩包和校验和均不得手工修改。

Release 说明必须列出：支持矩阵、安装与最小使用、双目标事实、已知限制、安全边界、失败恢复、
M0–M14 历史、M11 预发布关系和资产校验方法。Release 不是生产容量、跨平台、C2/C3、Docker、
恶意代码隔离或 AI 裁决声明。

## 8. 状态机与不可回退规则

M14 只允许以下前进路径：

```text
PLANNED
  -> CONTRACT_FROZEN / VALIDATING
  -> CANDIDATE_VALIDATED
  -> VERSION_FROZEN
  -> RELEASED / FROZEN
```

- 合同提交必须先推送并从远端读回，才可运行终局矩阵；
- 首次候选通过后才能提交稳定版本；稳定版本提交后必须重跑全部受影响门禁；
- 最终标签只能是 annotated tag，且创建后不得移动；
- GitHub Release 必须是非 draft、非 prerelease，资产逐项读回 SHA-256；
- Public CI 与 Browser Smoke 必须对最终提交全绿；
- 远端 `main`、`v0.12.0^{}`、Release targetCommitish 与事实文档记录必须精确一致；
- 任一硬门禁失败时状态退回 `VALIDATING` 或保持 `PENDING`，不删除失败事实，不创建成功标签。

最终事实另立后继文档，记录每条命令、输出目录、SHA、资源峰值、浏览器证据、残留、Release URL
与远端读回；本文只冻结规则，不预写结果。
