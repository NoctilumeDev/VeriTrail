# VeriTrail 项目指令

## 当前阶段

- 当前阶段是 `v0 Implementation`。M0 已在提交 `64497779add1351014d802b38d46f73a4ce394ac`
  上冻结；M1 已在提交 `21d555cf1a8d5b4f3bc9430b4241c3f70ff0d48f` 上通过两套 Python、
  M0 兼容、三类真实预检、证据包哈希、敏感扫描和残留检查并标记 `FROZEN`；M2 已在提交
  `3db07aa284e16db2afe3b84136371f35ec2091fc` 上通过两套 Python、真实 Chromium 正/负链路、
  Codex 内置浏览器、附件哈希、敏感扫描和残留检查并标记 `FROZEN`；M3 已在提交
  `ef2a8d64f781ba61bf7fbd9c1511a3419a6cfbaa` 上完成只读 Vue 工作台，并通过前端自动化、两套
  Python 兼容回归、真实 Chromium、Codex 内置浏览器、同源网络、依赖审计和残留检查，标记
  `FROZEN`。M4“本地 Run 目录与轻量自举”已在实现提交
  `ddcfa314b40bf9ba3332fec1e190e6335a4c1502` 上完成离线 Bundle 校验、SQLite 派生索引、固定
  回环只读 API、Catalog UI 和两阶段轻量自举，并通过双 Python、真实 Chromium、Codex 内置
  浏览器、敏感与残留复核，标记 `FROZEN`。Plan v1 的选择器歧义失败 Run 必须继续保留。
  M5“有界运行编排与静态目标生命周期”已在实现提交
  `98d3b69798e278da7603ea0ce04c39607e3a6407` 上完成 Plan 0.4、内置只读 `STATIC_HTTP`、
  `runtime.orchestration` 与 `run` CLI，并通过双 Python、真实正/负 Chromium、ABORT/STOP、
  端口竞争、源变化、Catalog/Workbench、Codex 内置浏览器、敏感与残留复核，标记 `FROZEN`。
  首个查询参数 400 失败 Run 必须继续保留。M6“同计划复跑确定性比较”已在实现提交
  `1a5eeaa6b5516c5b53248411e1284f6a2568e5e2` 上完成 Core/CLI、Comparison 0.1 与
  Workbench，并通过双 Python、真实三态 Comparison、逐字节复建、生产与 Codex 内置浏览器、
  资源、安全和清理终验，标记 `FROZEN`。损坏 Comparison 与预览端口残留反例必须继续保留。
  M7“预注册四角色配对反事实分析”已在合同提交 `7daf3b4`、实现提交 `9046f25` 与本地文件
  导入修复 `c726fe8` 上完成 PairingPlan/PairedAnalysis、CLI 与 Workbench，并通过双 Python、
  真实四角色三态、逐字节复建、来源损坏拒绝、Catalog 隔离、生产与 Codex 内置浏览器、资源、
  安全和清理终验，标记 `FROZEN`。目录选择器在内置浏览器中不触发导入的失败事实与改成显式
  四文件导入的修复必须继续保留。计划编辑、任意项目命令和完整自举仍未实现。
  M8“预注册全因子批次矩阵与固定种子扰动”已在合同 `b1ca45b`、Core `0510915`、Workbench
  `a067f4c`、真实批次 `5caee26` 与浏览器终验 `ba77feb` 上完成四个公共 Schema、两个 CLI、
  BatchAnalysis 四文件 Loader 和只读矩阵/wave 视图，并通过双 Python、8 个独立 M5 Run、四类
  分析、确定性/反例、生产及 Codex 内置浏览器、人工系统键盘、资源、安全和清理终验，标记
  `FROZEN`。裸静态服务的 Catalog 404 失败事实、内置浏览器合成 `Tab` 限制、真实 Chromium
  自动化补证与内置浏览器人工 `Tab` 通过事实必须继续保留。
- Post-M8 收束路线 Plan v1 位于 `docs/13-post-m8-roadmap.md`，已以 `post-m8-plan-v1` 冻结为
  规划基线。M10、M11、M12、M13 已冻结；M13 独立终审计划 0.1 位于
  `docs/52-m13-system-and-layered-code-quality-audit-plan.md`，事实位于
  `docs/53-m13-system-and-layered-code-quality-audit-facts.md`；M14 合同、整改、最终事实与 Release
  说明位于 `docs/54-m14-final-validation-and-release-contract.md` 至
  `docs/57-v0.12.0-release-notes.md`，当前为 `FROZEN / RELEASED`，稳定标签为 `v0.12.0`。
- `v0.12.0` 之后的当前主线是独立入口层 E0/S0/S1/A0/E1/E2/E3，计划、合同与事实位于
  `docs/58-post-core-entry-layer-plan.md` 至 `docs/70-entry-layer-e3-0.2-release-notes.md`。E1 已将
  Starter/Authoring Skill `0.1.0` 独立发布并固定到提交 `c7d3c8d`；E2 在源码中实现 Starter/Skill
  `0.2.0` 与第二个有限 Preset `static-site`；E3 已将两个 `0.2.0` 带注释标签固定到提交 `c9592e1`，
  完成两个非 Latest Release、七个资产、双 Python 公共下载读回与 GitHub 展示收口。`single-webapp`
  0.1 合同与标签事实不被重解释；`static-site` 只允许显式 CPython、
  现存普通 HTML、固定回环、无需构建和无需远程资源。Starter/Skill 仍不得自动 seal、run、批准
  Preview、handoff 或修改 Verdict，亦不得把入口层能力回填成 Core 0.12.0 已证明事实。Codex Security
  深度扫描、攻击路径验证和极端环境攻击继续封存，普通质量审查不得冒充这些安全工作流。Core
  `0.12.1` 已按 `docs/71-core-first-run-maintenance-contract.md` 至
  `docs/73-core-v0.12.1-release-readback-facts.md` 完成有界维护发布；它不重开 M0–M14，也不改写
  `v0.12.0` 冻结基线。归档审查随后证明 `demo` 在 staging 内生成的 Catalog 会在整目录改名后失去
  Artifact root 绑定；`docs/74-core-demo-catalog-binding-maintenance-contract.md` 至
  `docs/76-core-v0.12.2-release-readback-facts.md` 已完成最小 producer 修复、受保护标签、五项 Release
  资产、公开下载、双 Python wheel、sdist 与搬移负对照的闭环。Core `0.12.2` 是不可移动的历史维护
  Release，状态为 `RELEASED / MAINTENANCE FROZEN`；当前 Latest Core 已由后述 0.13.0 发布闭环更新。
  `v0.12.0`、`v0.12.1`、`v0.12.2`、`v0.13.0` 与 E1/E3 的所有已发布标签和资产均不得移动或静默改写。
- `docs/77-post-core-platform-plugin-plan.md` 至 `docs/79-p0-github-plugin-design-review.md` 新开独立
  平台插件 `P` 轨。P0 当前为 `FROZEN / DESIGN_ONLY`：它只冻结 GitHub Evidence Plugin 的权威、
  依赖、权限、数据、失败和后继验收边界，不是 M15 或 E4，也没有创建可运行插件、Schema、CLI、
  CI、标签或 Release。Core 0.12.2 离线探针曾证明：单源字面断言可以执行，但未观察 PRIMARY 仍可
  `PASS`，跨 Evidence session 也无法由当时的 Assertion 比较；这些缺口触发了后续兼容桥，不能被
  插件布尔值、虚构实验字段或私有比较器绕过。
  `docs/80-p0-core-compatibility-contract.md` 已定义临时、串行的 `PC0 -> PC1 -> PC2` Core 兼容桥：PC0
  冻结独立 AcceptancePlan、跨 Evidence 关系和旧消费者隔离语义；`docs/81-pc1-acceptance-core-implementation.md`
  已实现平台无关的 PC1 Core；`docs/82-pc2-acceptance-core-freeze-candidate.md` 已从精确候选
  `91004e99aaf4d3fb5cbae29d00057eff00f0b68a` 完成双 Python、普通/优化、旧消费者、Workbench、正负
  Bundle 独立复算、wheel clean install、敏感与清理本地门禁，并经 PR #26 九项远端检查、受保护
  `main` 合入及真实 GitHub 渲染读回固定在实现基线
  `fa8a5acac753456d37325bb0d9fac1b85add912b`。PC2 当前为 `FROZEN`。P1 合同随后经 PR #28 冻结，
  独立 Structured API Collector 经 PR #30 合入 `main@9b45bd635dedd132dc8333c105c04723991c2670`。
  冻结事实 PR #31 在合入前因 required-check 来源 layering 反例关闭且未合并；0.2 修正经 PR #32 的
  11 项门禁后，以 `main@5b363637f59be9786d58eed61a14e3bd663dd6d8` 合入，并完成精确主线与匿名
  README/事实文档读回。P1 当前为 `P1_FROZEN`；P2 合同从精确主线
  `cdc2c250f21b37a0be9f815295f7b7c3c5081d0d` 起步，经 PR #38 的最终 11 项门禁、受保护主线合入与
  exact-SHA 匿名 Render 读回固定在 `main@8c624ec3aa83fe462e3578d8aa215e8ef9908332`。当前为
  `P2_CONTRACT_0.1_FROZEN`。默认 Pages 根坐标反例随后经 PR #40 docs-only 修正为
  `pages_path = ""` 的唯一表示，并在 11 项门禁、受保护主线与 exact-SHA 匿名 Render 读回后重新冻结；
  其后的 implementation feasibility 又证明 completion-time Network 计数不能冒充 response-body 硬截断，
  并曾只重开计量字段、Chromium Fetch 流控制和 producer-side 中断证据；该修正与 append-only
  `RA-017` 已经 PR #42 的 11 项门禁、受保护主线与 exact-SHA 匿名 README/合同/Ledger 读回重新冻结；合同位于
  `docs/89-p2-public-render-collector-contract.md`。P2 实现已从冻结后的 exact main 独立施工，经 PR #49
  的 11 项门禁合入 `main@ca6b8aaa33bc06795c96610b9e9085506efef9a0`，并从该 exact main 完成产品
  Collector 的 desktop/narrow 匿名 README 读回；实现与本地/远端证据见
  `docs/90-p2-public-render-collector-freeze-candidate.md`。docs-only closure 又经 PR #50 的 11 项门禁合入
  `main@2d3877df41d7ec5a3b7b932404f6b622f06862a8`，并从该 exact main 对 README/事实文档完成
  desktop/narrow 匿名读回。最终冻结发布 PR #51 的原始门禁随后重新打出 Python 3.10 `-O` 的
  M10 生命周期反例（`13.688s > 9s`），因此被关闭且未合并；P2 实现证据保持成立，冻结资格没有成立。
  独立 PR #52 沿完整中断链统一生命周期与 Chromium 释放预算，并阻止 owned termination 后的失效观察，
  其原始 11 项门禁全绿后合入 `main@bb8f2d44c0c681862a5e63506ae57d4b4a8d7947`。修正后的 exact main
  已由产品 Collector 完成匿名 README desktop 与 `RA-018 rev2` Ledger narrow 读回。本状态发布以自身
  11 项门禁、受保护主线合入和合入后匿名读回为生效条件；该链成立后状态为
  `P2_FROZEN / P3_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`。P3 合同冻结只在
  `docs/93-p3-core-handoff-contract-freeze.md` 自身的门禁、合入和合入后读回全部成立后生效；不得把 P2
  冻结或 P3 合同冻结自动解释为已创建 handoff、P4 发布、定时监控或
  Review Attention R1。
  第一次 docs-only closure PR #43 因重复的 M10 Chromium cleanup timing failure 被否决并关闭，未合入；
  独立 PR #44 以单一绝对清理 deadline 修复并经 11 项门禁合入
  `main@25ff62f50a01fddc086c41740af802d9c2df0495`。后继 closure 没有 rerun 洗白 #43，也没有把 M10 修复
  解释成 P2 Collector 实现证据；PR #51/#52 同样保留“发布失败、地基修复、重新发布”三条独立事实链。
  插件只能产生只读事实，不能写 GitHub，不能生成或覆盖 Core Verdict。Codex Security 深度扫描与攻击
  路径验证继续不在当前工作范围内。GitHub API 与公开页面是同一信任域的两个观察面，不是两个独立
  权威；P 轨不得把承诺后完整性扩张为首次封存前的来源真实性或现实真实性，也不建设 GitHub 之外
  的独立见证或可信锚点。P 轨也不得裁定提出者的观点是否正确；它只检查 sealed 条件与 Evidence 的
  关系，未知、冲突、缺证据和不可归因必须继续可见。Agent 发现与前提冲突的事实时必须报告并把
  Seal 决定权交还给人，不得以“人负责前提”为由沉默，也不得自行改写目标。
  `docs/92-p3-core-handoff-contract.md` 与 `docs/93-p3-core-handoff-contract-freeze.md` 曾冻结 P3 0.1
  施工边界：P3 不新增观察面，只把 P1/P2 标准 Evidence 通过显式 role/path/digest handoff 交给现有
  Acceptance Core。handoff manifest 是插件侧极薄交接清单，不是 Evidence，不复制
  plan/session/facts/coverage，不进入 rule evaluator，也不产生 Verdict；Plan binding 与 session integrity
  仍只由 Core 裁决。P3-A 本地候选实现审查随后证明：handoff 先核验一次路径、Core 再读同一路径会让
  manifest 绑定的 Evidence A 与 Core 实际裁决的 Evidence B 发生快照漂移；两次各自安全的读取不能证明
  同一快照。修正边界只允许 Core 增加通用 imported-snapshot Bundle 入口，并让既有 path 入口先导入后
  委托它；不得修改 Schema、evaluator、P1/P2 fact semantics、coverage 或 Verdict 优先级。第一次修正
  PR #60 的原始 Python 3.13 `-O` 门禁复现既有 Browser route 回调与 driver 关闭竞态，因此关闭且未合并；
  独立 PR #61 只修复该停止边界，经 11 项门禁合入
  `main@6e48b5d109d0dd0e6c7b1b0fbe723cf1b792f852` 并完成匿名 exact-SHA 源码/Ledger 读回。合同修正随后
  从该新主线重建，由 PR #62 的原始 11 项门禁通过后合入
  `main@5d4e7bbbf706d92c98cf36418d6f86b5caf2d3d8`；从该 exact main 运行产品 Collector 对 README 与
  P3 合同完成 `COMPLETE` 匿名读回。独立 docs-only closure 的门禁、合入和合入后读回全部成立后，状态
  恢复为 `P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`。只能从新的 exact
  main 重建 P3-A，再串行继续 P3-B；不得复用旧候选、rerun 洗白旧失败，或把 Browser 地基修复算作 P3
  证据。P4 与 Review Attention R1 仍不得启动。
  P3 后继实现已从冻结后的 `main@589bbad7261cceda1aa3a6412278a48473a9b1b7` 严格串行完成 A–E；
  [PR #64](https://github.com/NoctilumeDev/VeriTrail/pull/64) 的原始 11 项门禁把完整候选
  `fa26dda516c354a5ddd08335202d3fd1cf5dbabb` 合入
  `main@c0bce6cb7a3c9f3684d1845beda355084f232d0a`，随后 README 与 P3 合同完成 exact-main 匿名产品读回。
  候选阶段状态为 `P3_IMPLEMENTED / FREEZE_CANDIDATE / P4_NOT_STARTED`，事实见
  `docs/94-p3-core-handoff-implementation-freeze-candidate.md`。第一次真实 E 暴露的 synthetic P2 fact path
  漂移已由 `7e10e7a` 最小修正，并以 append-only `RA-021 rev1` 保留；不得把旧失败输出删除后冒充从未
  发生，也不得把合成夹具的全绿替代真实标准 Evidence。P3 只有在 docs-only closure、主线合入与合入后
  匿名读回全部成立后才可标记 `P3_FROZEN`；在此之前 P4 与 Review Attention R1 仍不得启动。
  后继 docs-only 候选由 PR #65 的原始 11 项门禁合入
  `main@ec5ac70dcfa72b1b9859602af62cc3c9344389de`，并从该 exact main 对 README 与文档 94 完成 fresh
  anonymous P1/P2 产品读回，Core 均为 `PASS`。最终状态发布见
  `docs/95-p3-core-handoff-freeze-publication.md`；其自身门禁、合入与合入后读回全部成立后，当前状态为
  `P3_FROZEN / P4_NOT_STARTED`。这只解除 P4 的阶段阻断，不代表 P4 已开始；Review Attention R1 仍须
  等待 P4 与精确 Pattern Corpus 一并冻结。
  P4 docs-only 合同从 `main@f30647577e6de68c4d40a96f4f9b223fb24140bb` 重建，精确边界位于
  `docs/96-p4-github-evidence-release-contract.md`，冻结事实位于
  `docs/97-p4-github-evidence-release-contract-freeze.md`。该状态发布自身的门禁、受保护主线合入与合入后
  exact-main 匿名产品读回成立后，当前状态为
  `P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`。不得把合同冻结解释为已经创建
  `github-evidence-v0.1.0`、Release、公开资产或 `github-evidence-v*` ruleset。P4 必须区分
  source、distribution、asset、tag/Release 与 public-download
  observation identity；当前 tag ruleset 不覆盖插件标签，这是 tag 创建前的硬门。插件 Release 必须
  显式 non-Latest；P4 合同冻结时的 Latest 是 Core `v0.12.2`，后继受控 Core 0.13.0 发布已将 Latest
  合法更新为 `v0.13.0`，P4 恢复后不得让插件 Release 覆盖该身份。R1 继续等待 P4 与 Pattern Corpus
  双冻结。
  先前 PR #68 的原始门禁暴露既有 M11 CLI 聚合 `ERROR` 后已停止且未合入；PR #69 只增加分层诊断并以
  原始 11/11 门禁合入当前基线。后继绿灯不覆盖 #68，也不把其未复现解释为已知根因。
  PR #70 合入后的冻结前身份核账又发现 validation summary 不能把自身摘要写入自身；PR #71 只把顺序
  修正为 `wheel/sdist -> summary -> checksum -> external release facts`，经原始 11/11 门禁合入
  `main@eb4dcb60230a516503bf80ce26e13b25cd9b9d97`。该 exact main 的 Public CI、Browser Smoke 以及
  README desktop / 文档 96 narrow 的 fresh anonymous P1/P2 产品读回均成立，Core 两次为 `PASS`。
  这些事实只冻结发布合同，仍不授权提前创建 tag ruleset、tag、Release 或公开资产。
  后继 PR #72 与 `main@12130378febde2075d4cb9924628a07f9f26cb1e` 的原始 Public CI 分别在不同
  既有 Release 资产上连续收到 HTTP 500；后续匿名下载的字节与冻结 SHA-256 均成立，因此现有证据只支持
  瞬时外部失败超出旧短恢复窗口，不证明 GitHub、代理、仓库或资产的单一根因。独立 PR #74 只把四处
  固定短重试收敛为共享绝对截止时间、窄重试集合、owned partial、摘要校验后不覆盖发布的 CI 工具；其
  原始 11/11 门禁合入 `main@d23916735c7ac4d7e4a706d8edc5b106046b93c8`，该 exact main 的 Public CI
  11/11、Browser Smoke 1/1 以及 README desktop / 文档 98 narrow 的 fresh anonymous P1/P2 产品
  读回均成立，Core 两次为 `PASS`。精确事实见
  `docs/98-release-download-recovery-correction.md`；其 docs-only 状态发布自身的门禁、受保护主线合入与
  合入后读回全部成立后，状态为
  `RELEASE_DOWNLOAD_RECOVERY_FROZEN / P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`。
  该修正不得被解释为 P4 已创建 tag ruleset、tag、Release 或资产；P4 只能从状态发布后的新 exact main
  继续，R1 仍等待 P4 与 Pattern Corpus 双冻结。
  后继发布准备已经从 `main@b6ddb5c8a704b464dc9b4d07a0f43b7b93a64a71` 建立候选：内部工具固定
  wheel/sdist、非自指 summary/checksum 顺序与 independent verify；双 Python 的 base、sdist、render、
  plugin uninstall/Core-only 复算及预封存真实 GitHub P1 -> P2 -> P3 正向链均已形成本地证据，精确事实见
  `docs/99-p4-github-evidence-release-preparation-candidate.md`。当前状态只能记为
  `P4_RELEASE_PREPARATION_CANDIDATE / NO_TAG / NO_RELEASE`；只有该候选自己的原始远端门禁、受保护主线
  合入与新 exact main 门成立后，才允许重建最终字节并创建 tag protection。当前候选字节不得复用为最终
  Release 资产，R1 仍等待 P4 与 Pattern Corpus 双冻结。
  该候选合入后的 final exact-main clean-install 门随后证明：公开 `v0.12.2` wheel 不含 P3 所需的
  Acceptance API，而准备矩阵使用了同版本号的当前源码本地 wheel。该事实属于公开发行身份错配，不是
  下载失败或插件回归；P4 已停止为 `BLOCKED`，插件 tag ruleset、tag、Release、validation summary 与
  checksum 均不得创建。后继只能先按
  `docs/100-core-v0.13.0-acceptance-api-release-contract.md` 为既有冻结 Acceptance 能力建立独立 Core
  `0.13.0` 公开坐标；`v0.12.2` 标签与资产继续只读，R1 仍等待 P4 与 Pattern Corpus 双冻结。
  该合同候选经 PR #77 原始 11/11 门禁合入 `main@5b28ac3076ff4a08added47cbfc66c960c3dbdea`；
  exact-main 11/11、Browser Smoke 1/1 及 README/合同正文的两个独立匿名产品读回均已成立，冻结事实见
  `docs/101-core-v0.13.0-acceptance-api-contract-freeze.md`。该状态发布自身的门禁、受保护主线合入与
  合入后 exact-main 读回全部成立后，状态为
  `CORE_0.13.0_CONTRACT_FROZEN / P4_BLOCKED`。C1 随后从 exact
  `main@e69f3844254947f795564cb845056652f2dcf3ac` 进入
  `docs/102-core-v0.13.0-release-candidate-plan.md`；该阶段源码发行身份为 `0.13.0 / RELEASE CANDIDATE /
  PENDING PUBLIC READBACK`，历史过程见 `docs/103-v0.13.0-release-notes.md`。必须分开 Starter 0.2.0 的
  `>=0.12,<0.13` 冻结兼容边界、继承该边界的 Authoring Skill 真实 DRAFT 链、GitHub Evidence 的源码
  前向兼容、distribution 声明兼容与公开 clean install；不得让依赖解析把 Core 候选静默替换为
  0.12.2，也不能创建插件 tag ruleset、tag、Release、validation summary 或 checksum。
  候选 PR #79 原始 11/11 已成立并合入 `main@a5ba0e1bd8f181851db83de611981524da1da8f5`，但该
  exact main 的首轮 Public CI 在 Python 3.13 `-O` 暴露 M11 正向夹具预算不自洽；修正边界见
  `docs/104-core-v0.13.0-m11-positive-fixture-budget-correction.md`。独立 PR #80 与修正后的 exact main
  已分别取得 11/11，Browser Smoke 1/1 与 README/文档 104 匿名公开读回也已成立；闭环状态发布见
  `docs/105-core-v0.13.0-m11-positive-fixture-budget-closure.md`。该发布最后门成立前 C2 继续停止；其后只
  恢复 C2 施工资格，P4 仍等待 Core 0.13.0 公开发行闭环。
  C2 后继已经从 exact `main@cd6f85246c0a789a3117861144af95deeb1b7077` 重建五项最终资产，创建受保护
  注释标签 `v0.13.0` 与非 draft、非 prerelease 的 Latest Core Release，并完成五项匿名下载摘要、双
  Python wheel/sdist clean install、四 Verdict/imported snapshot、Workbench 真实 Chromium 与匿名
  Release body 读回。精确事实见 `docs/106-core-v0.13.0-release-readback-facts.md`；该状态补丁自己的
  原始门禁、受保护主线合入与合入后 exact-main README/文档 106 匿名读回全部成立后，状态才是
  `CORE_0.13.0_RELEASED / MAINTENANCE_FROZEN / C3_CLOSED / P4_RELEASE_NOT_STARTED`。这只解除 P4 的
  Core 发行阻断；P4 必须从新的 exact main 单独修正插件 distribution 依赖至 `veritrail==0.13.0`、
  保护 `github-evidence-v*` 标签并重建自身最终资产，不得复用旧候选字节或把 Core Release 继承为
  插件发布证据。R1 仍等待 P4 与精确 Pattern Corpus 双冻结。
  P4 已从后继 `main@ab874d3cfd9ac140654e35d84b0025c2503e10cd` 建立新的发布恢复候选，分发
  绑定提交为 `beaf006574e23d3d3f0c3541d9ea0708d23fa097`，精确事实见
  `docs/107-p4-github-evidence-release-resume-candidate.md`。当前只允许记为
  `P4_RELEASE_PREPARATION_CANDIDATE / CORE_0.13.0_BOUND / NO_TAG / NO_RELEASE / NO_PUBLIC_DOWNLOAD_CLAIM`。
  旧 `00130c0...` 候选已经作废；当前本地候选字节也不得作为最终资产。下一步只能推送候选、等待原始
  远端门禁并合入受保护主线，再从新的 exact main 重建最终四项资产；tag ruleset 必须先于 tag，插件
  Release 必须保持 non-Latest，Dependabot #16/#67 不得混入该因果链。
  后继 PR #83 已以原始 11/11 门禁合入
  `main@548b17ccb1f20d55a9f9beef6666e913af5f65d9`；该 exact main 的 Public CI 11/11 与 Browser Smoke
  1/1 均在 attempt 1 成立。P4 已从该提交重新构建最终四项资产，先启用 ruleset `22613490`，再创建
  受保护注释标签 `github-evidence-v0.1.0` 与 non-Latest Release `385275245`。四项匿名下载摘要、双
  Python clean install/runtime/uninstall、真实 GitHub 正向链与匿名 Release body 读回事实见
  `docs/108-p4-github-evidence-release-readback-facts.md`。该状态发布自己的原始门禁、受保护主线合入和
  合入后 exact-main 匿名读回全部成立后，当前状态为
  `P4_GITHUB_EVIDENCE_0.1.0_RELEASED / P4_FROZEN / R1_BLOCKED_UNTIL_PATTERN_CORPUS_FREEZE`。
  P4 冻结只解除 R1 的第一个前置条件；Pattern Corpus 未按 exact commit、manifest digest 与
  `pattern_id + selected_record_digest` 冻结前，不得启动 R1。
  P1 起不得在 observation request 中另造 `expected.*` 权威：观察坐标只能由 sealed Plan 机械派生并
  绑定 `plan_digest` 和派生规则版本；独立 Collector Policy 只提供 API 版本、超时和重试等运行边界，
  不得携带验收语义。Plan drafter 不因起草获得 Seal 权，Plan digest
  也不冒充身份认证。observation spec、Collector Policy 和 request envelope 摘要不得混用；
  observation spec digest 只能绑定自身语义版本、规范化坐标与投影；`plan_digest` 和 derivation version
  只进入 request binding/envelope，不得污染 observation/fact identity。`facts_digest` 只绑定 observation
  spec、规范化事实及 `normalization_semantics_version`，不得绑定
  request ID、本地时间、ETag、采集实现版本或非语义运行策略。具体 Evidence 身份沿用 Core 对完整
  EvidenceArtifact 计算的 SHA-256，不得在文件内创建自引用摘要，也不得与 fact/request/Core Run identity
  混用。API/客户端/解析器实现版本属于 provenance；只有规范化含义变化才升级语义版本。required
  check 不得仅按显示名合并，必须保留可取得的 producer/app/workflow/source identity；多次 GitHub
  调用必须记录 probe 级
  `observed_at`、实际操作数与总采集窗口，并明确整份 Evidence 不是平台原子快照。
  sealed request 不等于一次观察；每次实际执行必须建立新的 `collection_session_id`，跨 session 的
  API/Render 产物不得冒充同一次观察，最大窗口只使用 monotonic `collection_elapsed_ms`。P1 写代码前
  必须分别证明 ExperimentPlan 字段按原语义可承载 GitHub 坐标，以及 Core assertion algebra 能直接
  裁决规范化事实；禁止为 Schema 通过虚构实验字段，也禁止插件输出 Verdict-like boolean 绕过表达
  缺口。插件摘要固定 `veritrail-json-c14n/1` 与冻结测试向量，不重算历史 Core digest。P1 0.1 禁用
  conditional GET；tag 必须解引用到 `peeled_commit_sha`；Evidence 只保存匿名/只读认证 access mode，
  不保存凭据。required checks 的 ruleset 与 classic branch protection 是独立适用来源：必须分别采集
  并聚合；同一有效要求只保留一个 item，同时保留全部来源 provenance；任一来源不可观察时不得以
  另一来源的成功冒充完整。该变化升级 `normalization_semantics_version`，不重算历史 Core digest。
  P1 已冻结；后续新反例只能显式重开受影响的语义边界，不得借修补之名静默扩张 P2/P3/P4。
- `docs/85-post-core-review-attention-plugin-plan.md` 至 `docs/88-r0-review-attention-design-review.md` 新开独立顶层
  Review Attention `R` 轨。`R = Review`，不表示 Risk；它与历史 `M12-R1/R2/R3` 无关，文档、未来
  包与发布坐标必须使用完整名称，禁止裸 `r*` 标签。R0 已经冻结为
  `R0_ARCHITECTURE_FROZEN / PATTERN_LEDGER_OPEN / DESIGN_ONLY`：权威、Artifact、依赖、失败、视觉语义、
  阶段门和 Pattern Ledger Schema 已固定；不得创建源码包、Schema、CLI、CI、标签、Release 或空实现骨架。
  R 轨必须保持事实、Analyzer Evidence、机器 Proposal、Attention Map、Human Disposition 与 Core
  Verdict 分离。机器只能提出需要关注的位置，不能确认缺陷；只有经过身份确认的人类 authority 可以
  创建 HumanDisposition，已封存 ReviewPolicy 只能机械约束范围、优先级与必审项。Provider 成功不等于覆盖完整，空提案
  不得写成“无问题”。AI confidence 与 ReviewPolicy priority 必须分离；紫色仅表示机器提案来源，
  界面还必须使用标签、图标/边框和文字，不得只靠颜色或把红黄绿结论语义借给提案。
  可替换能力通过窄 Provider SPI 接入；同进程部署不等于共享权威，Core、P 插件和 Provider 实现不得
  相互导入或共享可变控制状态。`docs/87-review-pattern-ledger.md` 在 R0 后继续 append-only/open；
  `problem_layer` 与 `pattern_class` 必须正交，状态提升必须追加带 `record_revision / supersedes_digest /
  record_digest` 的不可变 revision。P2–P4 的新反例只能按 Schema 追加，不得反向改写 R0 或改变 P 轨
  范围。R1 必须等 P4 冻结并选定 exact commit + manifest digest，且逐项绑定
  `pattern_id + selected_record_digest` 的 Pattern Corpus 后才能启动。P4 已冻结；Ledger 已在独立 docs-only
  候选中把保留的 P2–P4 反例物化至 `RA-027`，并新增 Corpus 选择/manifest/非自指 closure 合同。该候选
  经 PR #85 原始 11/11 门禁合入 `main@8526c5551cce3a9a9e916917381e0e0463a082f0`，合入后 exact-main
  Public CI、Browser Smoke、README 与合同正文的匿名产品读回均已成立。最终状态发布见
  `docs/110-review-attention-pattern-corpus-contract-freeze.md`；其自身门禁、合入和合入后读回全部成立后，
  合同状态为 `CORPUS_CONTRACT_0.1_FROZEN / LEDGER_OPEN`。后继 payload 候选见
  `docs/111-review-attention-pattern-corpus-selection-candidate.md` 与
  `docs/review-attention-pattern-corpus-0.1.json`：只选择 `RA-003 / RA-004 / RA-008 / RA-023` 的精确
  `FROZEN_PATTERN` successor。Payload 经 PR #87 原始 11/11 门禁合入
  `main@9bdcef30517309bbc87ed7fdb0fec395197ef58a`，其 exact-main Public CI、Browser Smoke、四组独立复算、
  README/文档 111 匿名产品读回和 manifest 匿名原始字节读回均已成立。最终状态发布见
  `docs/112-review-attention-pattern-corpus-freeze-closure.md`，外部绑定 source commit 与 manifest digest
  `sha256:ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`；其自身门禁、受保护主线合入与
  合入后 exact-main 匿名读回全部成立后，状态为
  `PATTERN_CORPUS_0.1_FROZEN / LEDGER_OPEN / R1_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`。这只解除
  R1 入口停止线；R1 必须从新的 exact main 另开合同，不得在 Corpus closure 中顺带实现。
  后继 `docs/113-r1-deterministic-semantic-slice-contract.md` 已从
  `main@9ab64121350b69ce81e6be79961ad426026bbc39` 建立 docs-only 候选；PR #89 原始 11/11 门禁已把它合入
  `main@617e99ddd8217fbcaf26037c0f9ac15014795f15`，该 exact main 的 Public CI、Browser Smoke 与三次匿名
  产品读回均成立。后继 `docs/115-r1-contract-freeze-publication.md` 自身的门禁、受保护主线合入与合入后
  exact-main 匿名读回全部成立后，状态才是
  `R1_CONTRACT_FROZEN / R1_SCHEMA_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。R1 0.1 的范围必须保持为
  `SourceSnapshot -> CodeFacts -> typed structural Relations -> bounded overlapping ReviewSlices ->
  CoverageLedger`；首个 Profile 只支持 Python 3.10 结构语义，不得外推为整个多语言仓库已被理解。
  `R1_SCHEMA_DRAFTING_ALLOWED` 只允许从新的 exact main 独立起草版本化 Schema 与兼容向量，不表示 Schema
  已存在或已冻结；R1 源码包、CLI、运行 CI、Provider、标签和 Release 继续禁止，直到后继实现入口独立闭合。
  README 读者骨架与对称 SVG 已经在独立受保护主线闭环后退出；后继
  `docs/120-r1-schema-and-canonical-identity-contract.md` 从
  `main@35774838b3e9aeb5f062cfb101e96d76cea0e8ac` 建立 docs-only Schema 合同候选，只定义字段词汇、
  规范字节、可逆 Git path、raw byte anchor、身份投影、BFS tie-break、inclusive budget、Coverage 分母与
  固定 Artifact 布局。候选经 PR #99 原始 11/11 门禁合入
  `main@49a2d69d44cca21024808fe5c298db8bac7f64c4`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
  与 README/文档 120/milestones 三次匿名产品读回均已成立。首次 docs-only 冻结发布 PR #100 的原始
  Python 3.10 `-O` 门禁随后复现 M10 公共自举正向夹具的隐藏 15000 ms lifecycle SLO；PR #100 没有
  rerun 或合入，已关闭。独立 `docs/122-m10-public-bootstrap-positive-fixture-budget-alignment.md` 与 PR #101
  只修正该测试证据边界；PR #101 原始 11/11 门禁合入
  `main@8aa70807c0de9c0f50ad977575d81f2a1d635a91` 后，新 exact main 的 Public CI 11/11、Browser Smoke
  1/1 与文档 122 匿名产品读回均已成立。后继
  `docs/121-r1-schema-contract-freeze-publication.md` 从该新 exact main 重建冻结发布并保留完整失败链；其
  自身门禁、受保护主线合入与合入后 exact-main 匿名读回全部成立后，状态才是
  `R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。
  后继 payload preflight 从该 exact main 发现 item key、frontier、Coverage 与 provenance identity 仍不足以
  唯一生成 Schema；`docs/123-r1-schema-payload-preflight-correction.md` 只重开被反例击穿的边界。修正候选
  `19a923cae37b057879ae9879296e789c6e348cf2` 经 PR #103 原始 11/11 门禁合入
  `main@839877ca38489d0518a5b67d5956c7907152529c`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1
  与 README、合同、修正文档、milestones 四次匿名产品读回均成立。后继
  `docs/124-r1-schema-payload-preflight-refreeze-publication.md` 只发布该修正闭环；其自身门禁、受保护主线
  合入与合入后 exact-main 匿名读回全部成立后，状态才恢复为
  `R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED / R1_IMPLEMENTATION_NOT_STARTED`。
  该资格只允许从新的 exact main 创建版本化 JSON Schema、纯数据兼容 corpus、规范字节/摘要向量与
  Schema/conformance tests；runtime importer、parser、relation/slice engine、CLI、Provider、标签和
  Release 继续禁止。
- 后继 `docs/125-r1-schema-payload-freeze-candidate.md` 已从 exact
  `main@4ef8b6434597b6557d6306100b91aebd9c1b3ecd` 创建十个固定 JSON Schema、纯数据 compatibility corpus、
  canonical byte/digest vectors 与 Schema/conformance tests；`jsonschema==4.25.1` 只能作为测试 extra，
  不得成为 Core base runtime dependency。当前状态为
  `R1_SCHEMA_PAYLOAD_CANDIDATE / R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED / R1_IMPLEMENTATION_NOT_STARTED`。
  候选自身原始远端门、受保护主线合入、exact-main 门与匿名公开读回全部成立前，不得写 payload frozen，
  不得创建 R1 runtime importer、parser、Fact/Relation/Slice/Coverage producer、CLI、Provider、标签或
  Release。
- 候选提交 `88ece8443904c83cc74b6ee3608d84e03e4951af` 经 PR #105 原始 11/11 门禁合入
  `main@4a25ef3d4009395f3510e847909f1efbaa29c5ac`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1、
  十个 Schema 与十九个 corpus 文件匿名逐字节读回以及 README/文档 125 的公开产品链读回均成立。后继
  `docs/126-r1-schema-payload-freeze-publication.md` 只发布该闭环；其自身门禁、受保护主线合入与合入后
  exact-main 匿名读回全部成立后，状态为
  `R1_SCHEMA_PAYLOAD_FROZEN / R1_IMPLEMENTATION_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`。
  该入口只允许从新的 exact main 建立独立运行实现合同或首个最小切片；不得从 payload 分支续写，不得
  继承 payload 绿灯为运行证据，也不得提前创建完整 Facts/Relations/Slices/Coverage、AI/排序、CLI、
  Provider、标签或 Release。
- 后继 `docs/127-r1-source-snapshot-runtime-contract.md` 从 exact
  `main@1409bea0cd75664df181319348e1ca87e643e743` 开始首个运行切片的 docs-only 合同审计。审计确认单文件
  `source-snapshot.json` 不是 `R1_DERIVATION` closure，冻结 Manifest 不能用占位 Artifact 或第三种
  outcome 缩短；Snapshot acquisition 另用不进入语义身份的 safety budget，预算耗尽不得发布截断
  inventory。当前只能写
  `R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_CANDIDATE / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`；候选完成
  自己的受保护主线闭环和独立冻结发布前，不得创建 `plugins/review-attention` runtime、测试、CLI、CI、
  Provider、标签或 Release。
- 候选提交 `ac3d4169732529ad7662672222156c7e140d0fc8` 经 PR #107 原始 11/11 门禁合入 exact
  `main@def98c6a116b50fc9c0e7c849dd9118b70285eba`；该 main 的 Public CI 11/11、Browser Smoke 1/1 与
  README、文档 120/127 的匿名 Public Render 读回均成立。后继
  `docs/128-r1-source-snapshot-runtime-contract-freeze-publication.md` 只发布该闭环；其自身门禁、受保护
  主线合入、exact-main 门与匿名读回全部成立后，状态才是
  `R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED /
  R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`。授权仅覆盖 SourceSnapshot 最小实现；Fact、Relation、
  Slice、Coverage、完整 Derivation Manifest、CLI、Provider、标签与 Release 继续禁止。
- SourceSnapshot 最小实现从 exact `main@24c41c0ac9221ba4d8ae642c08ca5cdc08587b20` 独立施工。
  PR #109 的第一次 head `0f7ba6d84e09187f918f3c855c7c43e47b0415d4` 在 Python 3.10/3.13 的 exact
  Reference Lab 同时因 Actions shallow checkout 缺少冻结 commit 而 fail closed；该 run 没有 rerun。
  独立提交 `c4dff3a7d0a6b5b58160da2b3d73151654161a2f` 只让 Python CI checkout 物化完整本地
  object history，不允许 SourceSnapshot 联网或 lazy fetch。修正 head 原始 11/11 门禁通过后，PR #109
  以 merge commit `4f5c41a9f163056ed4c2d2cfd686d321ecba5605` 合入；该 exact main 的 Public CI
  11/11、Browser Smoke 1/1 与 Reference Lab 双版本读回均成立。在冻结候选发布前只能写
  `R1_SOURCE_SNAPSHOT_IMPLEMENTED / FREEZE_CANDIDATE /
  R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。冻结候选见
  `docs/129-r1-source-snapshot-implementation-freeze-candidate.md`；其自身门禁、合入、公开读回与后继独立
  状态发布完成前，不得写 `R1_SOURCE_SNAPSHOT_FROZEN`，也不得启动后继 R1 对象。
- docs-only PR #110 将 SourceSnapshot 实现、二十格合同映射与失败链记录为冻结候选；其 head
  `e406884a7ead6dcb3498f48af26783e6519f7c32` 的原始 Public CI attempt 1 为 11/11，随后以
  `main@ee249d35e1000d3f15f0a0b4e1ef9eb66a425b32` 合入。该 exact main 的 Public CI 11/11、
  Browser Smoke 1/1，以及 README/文档 129 的 fresh anonymous P2 Collector 三样本与 marker 读回均
  成立。最终状态发布见 `docs/130-r1-source-snapshot-freeze-publication.md`；它自身完成原始门禁、受保护
  主线合入、新 exact-main 门禁与匿名读回后，状态为 `R1_SOURCE_SNAPSHOT_FROZEN /
  R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结不授权直接施工后继对象；下一步
  只能从新 exact main 审计并冻结下一个最小合同闭环。
- 后继 `docs/131-r1-post-snapshot-derivation-input-audit.md` 从 exact
  `main@b1a58143ae2fd359b885a575587aa4682aef8a04` 审计 Snapshot 之后的接缝。审计确认 FactSet 的
  provenance 与冻结 Manifest file set 不允许 Fact-only 发布，并选择不产生公共 Artifact 的
  `Derivation Input Binding` 作为下一最小边界。`docs/132-r1-derivation-input-binding-contract.md` 的候选经
  PR #112 原始 11/11 门禁合入 `main@b807ee095630c14edd73621c43943437b6cdddff`，该 exact main 的 Public CI
  11/11、Browser Smoke 1/1 与 README/合同/milestones 三次 fresh anonymous P2 Collector 读回均成立。
  `docs/133-r1-derivation-input-binding-contract-freeze-publication.md` 只发布该闭环；其自身门禁、受保护主线
  合入、exact-main 门与匿名读回全部成立后，状态才是
  `R1_DERIVATION_INPUT_BINDING_CONTRACT_FROZEN / R1_DERIVATION_INPUT_IMPLEMENTATION_ALLOWED /
  R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED / R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。
  授权仅覆盖 input binder；parser、Fact、Evidence、Relation、Slice、Coverage 或完整 Derivation runtime
  继续禁止。
- Derivation Input runtime 从 exact `main@84512755b6475cfa40ca352f43e4cb7be953a761` 独立施工。
  PR #114 head `5447a0c0947c44cbbd80af6e90f74438b9950d1f` 的原始 Public CI 11/11 后，以
  `main@46bb81625b9f2dcb4fa1284bd75344e89ed4be5f` 合入；该 exact main 的 Public CI 11/11 与
  Browser Smoke 1/1 均为 attempt 1 success。实现只建立四路径有界读取、三 Artifact conformance、
  exact Git byte reacquisition 与 copy-owned `DerivationInputSet`，不发布 Artifact。当前状态为
  `R1_DERIVATION_INPUT_IMPLEMENTED / FREEZE_CANDIDATE /
  R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`，候选见
  `docs/134-r1-derivation-input-implementation-freeze-candidate.md`。候选自己的远端门、合入、exact-main 门、
  匿名读回与后继独立最终状态发布完成前，不得写 `R1_DERIVATION_INPUT_FROZEN`，也不得启动 parser、Fact、
  Relation、Slice、Coverage、conflict/UNKNOWN 传播或完整 Derivation runtime。
- docs-only PR #115 将 Derivation Input 实现、二十二格合同矩阵与反例链记录为冻结候选；其 head
  `170edd2dd9569da7c70a219ae11e850ff96aad12` 的原始 Public CI attempt 1 为 11/11，随后以
  `main@aa7ff1140aa8c988e84b38808cb8cb1eebe3fbf3` 合入。该 exact main 的 Public CI 11/11、
  Browser Smoke 1/1，以及 README/文档 134 的 fresh anonymous P2 Collector 三样本与 marker 读回均
  成立。最终状态发布见 `docs/135-r1-derivation-input-freeze-publication.md`；它自身完成原始门禁、受保护
  主线合入、新 exact-main 门禁与匿名读回后，状态为 `R1_DERIVATION_INPUT_FROZEN /
  R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只覆盖 Input Binding runtime；下一步
  仍只能从新的 exact main 审计并冻结下一个最小合同闭环。
- 后继 `docs/136-r1-derivation-attempt-and-fact-provenance-audit.md` 从 exact
  `main@7e0950ba2544476049e6defe1545f786971a89bd` 审计 attempt、Provider applicability、budget 与 Fact
  provenance 接缝；`docs/137-r1-derivation-attempt-and-fact-provenance-contract.md` 只建立 docs-only 合同
  候选。候选经 PR #117 原始 Public CI 11/11、受保护主线合入、exact-main Public CI 11/11、Browser Smoke
  1/1 与已安装产品匿名 exact-SHA 读回后，由
  `docs/138-r1-derivation-provenance-contract-freeze-publication.md` 独立发布冻结事实。当前状态为
  `R1_DERIVATION_PROVENANCE_CONTRACT_FROZEN /
  R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_REQUIRED /
  R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结最多只允许后继先修正 Evidence typed budget
  diagnostics 与非成功 reported IDs；Schema/corpus 修正独立冻结、budget primitive feasibility 与明确
  runtime 授权成立前，不得创建真实 parser、Provider runtime、FactSet/DerivationEvidence Artifact、
  Relation、Slice、Coverage、Manifest、CLI 或 Workbench。
- 后继 `docs/139-r1-derivation-evidence-schema-correction-audit.md` 从 exact
  `main@f69f2818d06834da0d9e8e95288f6f72aada6beb` 复现旧 Evidence Schema 会接受 non-COMPLETED
  run/overall 携带 reported IDs，同时拒绝必要的 memory/artifact budget diagnostic。审计确认文档 126 已
  逐字节冻结的 `review-derivation-evidence-0.1.schema.json` 不能在相同 path/`$id` 下原位改写；
  `docs/140-r1-derivation-evidence-schema-correction-contract.md` 只建立自描述的 DerivationEvidence `0.1.1`
  补丁合同，保留旧 Schema/corpus/vector 原字节，不升级其他 R1 Artifact、Manifest 或 digest projection。
  候选经 PR #119 原始 Public CI 11/11、受保护主线合入、exact-main Public CI 11/11、Browser Smoke 1/1 与
  已安装产品匿名 exact-SHA 读回后，由
  `docs/141-r1-derivation-evidence-schema-correction-contract-freeze-publication.md` 独立发布冻结事实。当前状态为
  `R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_CONTRACT_FROZEN /
  R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTATION_ALLOWED /
  R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_NOT_STARTED /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只允许物化文档 140 限定的 `0.1.1`
  Schema/corpus/test；其独立冻结完成以后仍须先证明 budget primitive feasibility 并取得明确 runtime 授权。
  request provenance 的 exact-only 约束继续属于首个 runtime conformance，不能借本修正永久收窄通用
  alias-aware Schema。
- DerivationEvidence `0.1.1` correction payload 随后从 exact
  `main@19cb4ff4300e6c7aeb08aa315802abb29e183d60` 物化；PR #121 原始 Public CI 11/11 后合入
  `main@99826ec1564e8447524c477ff9f271fa5d062ea6`，并完成 exact-main Public CI 11/11、Browser Smoke 1/1
  与匿名公开字节读回。实现冻结候选见
  `docs/142-r1-derivation-evidence-schema-correction-implementation-freeze-candidate.md`；其 PR #122 原始
  Public CI 11/11 后合入 `main@a940259a4c286f64d39a92854397eea25c442e0f`，该 exact main 的 Public CI
  11/11、Browser Smoke 1/1 与 README/文档 142/milestones 三次已安装产品匿名读回均成立。最终状态发布见
  `docs/143-r1-derivation-evidence-schema-correction-freeze-publication.md`；它自身的门禁、合入与合入后读回
  全部成立后，状态为 `R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。唯一下一步是独立 budget primitive feasibility；
  它不是 runtime authorization，Provider/parser/Fact、Relation、Slice、Coverage 与完整 Derivation 仍禁止。
- 后继 budget primitive 审计从 exact
  `main@3a1374c2e7c5861ab9746052dceb8f50a1544d3e` 开始，只使用仓库外一次性 Windows Job/staging 探针，
  没有写 runtime。`docs/144-r1-derivation-budget-primitive-precontract-audit.md` 证明 hard memory
  containment 与 terminal attribution 不能压成一个事实：只有正向 Job memory-limit event 才能授权
  `EXECUTION_MEMORY_BUDGET`，OOM/exit code/已配置上限均不得反推；它还把 absolute monotonic deadline
  收窄为结果资格边界，要求 normal result 与 phase-owned resources 在 deadline 前一起闭合，
  并仅为 terminal-stop 后的 process-tree/staging cleanup 建立一次性共享 release envelope。
  `docs/145-r1-derivation-budget-primitive-contract.md` 的候选经 PR #124 原始 Public CI 11/11 合入
  `main@9a969af10f705abe66ac7816bc27e9369ea7206a`；该 exact main 的 Public CI 11/11、Browser Smoke 1/1、
  匿名 raw bytes 与 README/文档 145/milestones 三次已安装产品读回均成立。第二轮系统俯瞰又修正了
  `COMPLETED_FOR_PHASE` 被误作 BudgetContext terminal state 以及 normal completion check/stop latch
  竞态两个 Freeze blocker；其余发现分别归为实现门、延期接缝或仅观察事实，不因审计 KPI 自动修改。
  最终状态发布见 `docs/146-r1-derivation-budget-primitive-contract-freeze-publication.md`；它自身的门禁、
  合入、exact-main 门与最终匿名读回全部成立后，状态为
  `R1_DERIVATION_BUDGET_PRIMITIVE_CONTRACT_FROZEN /
  R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_ALLOWED /
  R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTATION_NOT_STARTED /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该冻结只允许实现文档 145 的 primitive 与
  `BP-001..016`；Provider/parser/Fact 必须等待该实现自身冻结及后继明确授权，Relation、Slice、Coverage、
  conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。
- Derivation Budget Primitive 后继实现由 PR #126 从冻结合同基线
  `4c4d81bfeed7bea9d159a58bb91097f8d98fb0c8` 建立。主实现提交为
  `998b6ef52665bcafc0e7f9b6b8f2cbc0bedb2341`；其第一次 Public CI 在双 Python 的 BP-014 同时暴露
  `pip wheel --no-build-isolation` 对 ambient build backend 的错误测试假设，该失败没有 rerun。独立修正
  `b23488e7f12b719c6fc331af31ff9bb9032659ca` 让 base-wheel 负向门真正使用 isolated build environment；
  新 head 的原始 11/11 门禁合入
  `main@8f8af815d1a566bbf35096e318d209bdc17bf7b3`，该 exact main 的 Public CI 11/11、Browser Smoke 1/1
  与四项匿名 exact-SHA bytes 读回均成立。实现后系统审计修正 local cleanup 冒充 global release、expired
  context 仍可 resume worker，以及内部 attribution state 顶层导出；Provider 异常后的 context discard 与
  非抢占文件系统 cleanup 继续留给后继合同，不能由 primitive 猜测。实现冻结候选见
  `docs/147-r1-derivation-budget-primitive-implementation-freeze-candidate.md`；当前只能记为
  `R1_DERIVATION_BUDGET_PRIMITIVE_IMPLEMENTED /
  R1_DERIVATION_BUDGET_PRIMITIVE_FREEZE_CANDIDATE /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。文档 147 自身的门、主线合入、exact-main 门、
  匿名产品读回与后继独立状态发布成立前不得写成 frozen；Provider/parser/Fact、Relation、Slice、Coverage、
  conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。
- `docs/148-r1-derivation-budget-primitive-freeze-publication.md` 从候选合入基线
  `main@571139df5db94159f5e439619176f17a02f86f94` 独立发布最终冻结事实。PR #127 的第一个 docs-only head
  曾以 `startup_failure` 结束且没有实例化 jobs/check-runs；该 run 未 rerun，后继新 head 原始 Public CI
  11/11、受保护主线合入、新 exact-main Public CI 11/11、Browser Smoke 1/1 与三次匿名已安装产品 PASS
  均成立。本文自身的原始门、合入、新 exact-main 门和针对本文坐标的 fresh anonymous 读回全部完成后，
  状态才为 `R1_DERIVATION_BUDGET_PRIMITIVE_FROZEN /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。唯一下一步是重新审计 Derivation Attempt / Provider
  Run / Fact provenance 接缝；审计不授权实现。Provider/parser/Fact、Relation、Slice、Coverage、
  conflict/UNKNOWN 与完整 Derivation/Manifest 继续禁止。
  docs-only Q0 支线的蓝图、展示反例修正、失败冻结发布、独立地基修正与新 exact-main 复验已经完成：
  `Q = Quick`，正式能力名为 `Verification Scheduling Plugin`。旧状态发布合入后的 exact-main Public CI
  曾在 E3 0.2 Release 下载门停止，证明旧实现把四级退避表误作五次尝试上限，在 60 秒绝对恢复预算仍有约
  29 秒时提前退出；该失败没有 rerun。独立 PR #94 只修正预算所有权，其原始 11/11 门禁合入
  `main@c2f488e8274b43dea6ad39402a94c3f6a1ee7753`，新 exact main 的 Public CI 11/11、Browser Smoke 1/1 与
  三次匿名产品读回均成立。本状态发布自己的门禁、合入与合入后读回全部成立后，状态为
  `Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY`。蓝图见
  `docs/116-q0-quick-verification-scheduling-blueprint.md`，状态发布见
  `docs/117-q0-verification-scheduling-freeze-publication.md`，最小修正与最终闭环见
  `docs/118-release-download-recovery-deadline-correction.md` 和
  `docs/119-q0-verification-scheduling-final-freeze-closure.md`。Q0 仍只冻结该候选插件的身份、权威、分层、反例
  与实现前置门；没有创建 Schema、源码包、CLI、缓存、
  调度器、执行 Lane、CI 修改、标签、Release 或空插件
  目录，也没有预编 Q1–Qn。Q 与 R 是不同顶层语义：R 优化 Human Attention，Q 优化既定证明义务的
  wall-clock/recompute；Q 不得要求 R1 增加 diff/change blast radius，不得把 AttentionProposal 当 impact fact，
  也不得导入 R/P 实现或 Core 私有 API。Q 未来最多形成可审计 Schedule、Evidence reuse binding 与 Lane/join
  provenance；不能输出 `SAFE_TO_SKIP`、PASS、削弱 Gate、重定义 Evidence 或产生 Verdict。Q 缺失、失败或
  卸载时，完整串行验证与 Core 语义必须保持成立。下一步只允许从完成本状态发布读回后的新 exact main 独立
  重构 README 读者骨架；文字骨架闭环后才允许单独增加 SVG，R1 Schema 必须等两项展示施工闭环后恢复，新的
  Q 施工仍未授权。
  仓库前缀必须按层级和全名解释：`M/E/P/R/Q` 是长期或候选顶层轨道，`S/A` 是 E 轨内部产品阶段，`PC/C`
  是已关闭的一次性桥/发布状态机，`RA/CAP/AUTH/L*` 是 Artifact 或治理编号。字母多不构成问题；禁止脱离
  全名复用裸前缀，或把依赖误写成 ownership、消费误写成 succession、组合误写成 integration。
  文档 91 已把 P1/P2 的开放世界观察经验归纳为非合同方法，并在 R 轨 Plan 中补充 R1 的未来
  Semantic Review Slice 边界：slice 由精确 SourceSnapshot 的确定性关系图派生，可以重叠但必须
  有界、可追溯并保留 coverage/truncation；slice derivation、analysis 与 attention ranking 不得合并。
  该补充不新增 R0 Artifact、不冻结 Slice Schema，也不解除 R1 前置阻断。
- `docs/149-r1-derivation-execution-cell-system-audit.md` 从 exact
  `main@c33aeac9fa198bd8a0b9b5dc8340372757ba04b7` 审计 Budget Primitive 与后继 Provider/Fact phase 的组合
  接缝。审计确认 execution-cell memory 覆盖与 application canonicalization、bounded terminal envelope、
  primitive failure 后 context invalidation、concrete cell preparation/admission 原子边界及未归因 worker
  termination 的公共表达尚未闭合。当前状态为
  `R1_DERIVATION_EXECUTION_CELL_PRECONTRACT_AUDITED /
  R1_DERIVATION_EXECUTION_CELL_CONTRACT_NOT_STARTED /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只允许从新 exact main 起草 docs-only
  Execution Cell / Terminal Envelope 合同；不得创建 transport、Provider、parser、Fact、Schema revision、
  Relation、Slice、Coverage、Manifest、CLI 或 Workbench 实现。
- `docs/150-r1-derivation-execution-cell-terminal-envelope-contract.md` 从 exact
  `main@2de46c21997d85a437820decfeb2bd8bb7b69ee1` 起草审计 149 选定的 docs-only 最小合同。它把 trusted
  controller、contained application worker 与 Provider authority 分层，冻结 preflight/t0/inactive-cell/
  attempt/run-start 顺序、8-byte length-prefixed single-terminal canonical JSON framing、closed test launch
  binding、controller-owned terminal mapping，以及 primitive/protocol/cleanup failure 后不可恢复的 attempt
  eligibility revocation。当前状态为 `R1_DERIVATION_EXECUTION_CELL_CONTRACT_CANDIDATE /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该候选裁决现有 `INTERNAL_DERIVATION_ERROR` 足以作为
  不声明平台/Provider 根因的 epistemic fallback，因此不修改 `DerivationEvidence 0.1.1` Schema/corpus。候选
  自身的远端门、主线合入、exact-main 门、匿名读回与独立冻结发布成立以前，不得写 execution-cell transport、
  test Provider、Fact phase 或任何后继对象。
- `docs/151-r1-derivation-execution-cell-contract-freeze-publication.md` 外部绑定文档 150 候选的本地组合审计、
  PR #130 原始 Public CI attempt 1 的 11/11、受保护主线 `e1f91a94afb3e3afd4e85d3605240b77d379f57a`、
  exact-main Public CI 11/11、Browser Smoke 1/1 与 README/文档 150/milestones 三次 fresh anonymous
  installed-product Core PASS。其自身最后门全部成立后，状态为
  `R1_DERIVATION_EXECUTION_CELL_CONTRACT_FROZEN /
  R1_DERIVATION_EXECUTION_CELL_IMPLEMENTATION_ALLOWED /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。该授权只允许文档 150 的 closed test Provider、
  bounded transport、attempt eligibility 与 non-published Fact phase result；真实 parser、FactSet/Evidence
  publication、Relation、conflict/UNKNOWN、Slice、Coverage 与完整 Manifest 继续禁止。本状态发布自己的
  PR/合入/exact-main/匿名读回完成前，分支文字仍不授权实现。
- Execution Cell 实现已由 PR #132 从冻结合同基线
  `3c89f8eb94333986fc4901b9a1b91edf47d0059f` 建立；实现提交
  `02e4d05dcfc7c062c97ecfa21c00b26f601b9140` 经原始 Public CI attempt 1 的 11/11 后，以 merge commit
  `8b77305cea3a95690660adcb25f76d2b42c6e5e1` 合入受保护主线。该 exact main 的 Public CI 11/11、
  Browser Smoke 1/1 与全部十二个变更文件的 fresh anonymous exact-SHA bytes 读回均成立。实现只新增
  private closed test Provider binding、bounded single-terminal transport、hard-contained Windows application
  worker、不可恢复 attempt eligibility、controller-owned terminal mapping 与 copy-owned non-published Fact
  phase result；顶层包没有导出 execution-cell API。实施中修正了 rejected terminal run identity 泄漏、
  primitive commit failure 未显式 revoke、pre-admission runtime loss 异常泄漏、release failure 被误作普通
  phase result 与 late stop/early terminal 竞态，并作废父进程 `PYTHONPATH` 污染的第一次 BP-014 clean-wheel
  证据后在 fresh interpreter 世界重建。精确事实见
  `docs/152-r1-derivation-execution-cell-implementation-freeze-candidate.md`。当前只能记为
  `R1_DERIVATION_EXECUTION_CELL_IMPLEMENTED /
  R1_DERIVATION_EXECUTION_CELL_FREEZE_CANDIDATE /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。文档 152 自身的门、受保护主线合入、exact-main
  门、匿名产品读回与后继独立最终状态发布成立前，不得写成 frozen，也不得审计或实现真实 parser、
  FactSet/DerivationEvidence publication、Relation、conflict/UNKNOWN、Slice、Coverage 或完整 Manifest。
- 文档 152 的实现冻结候选已由 PR #133 从 exact `main@8b77305cea3a95690660adcb25f76d2b42c6e5e1`
  建立；候选提交 `84a986010c42ef43f785e3725ea6d65b87d3b063` 的原始 Public CI attempt 1 为
  11/11 SUCCESS，并以 merge commit `c2349b2a7c4d9ed002311d46f7212cb35856caf6`、tree
  `63239304e6d32479a888ebf1e5a077a4143292bb` 合入受保护主线。该 exact main 的 Public CI
  `34770503241` 为 11/11、Browser Smoke `34770503260` 为 1/1，均是 attempt 1。fresh CPython 3.13.13
  已安装产品环境在无 GitHub token、无 `PYTHONPATH` 下对 README、文档 152 与 milestones 建立三次独立
  `P1 API -> P2 Render` session；三者均 HTTP 200、requested/final 相同、三样本稳定、active streams 为 0、
  无 cleanup/coverage error 且 Core Verdict 为 PASS，summary digest 为
  `94654f6f58fcf82a2a6230521164e8f98176dff1ab40e97d2c695a67d8c98045`。最终状态发布见
  `docs/153-r1-derivation-execution-cell-freeze-publication.md`。该文档自己的门禁、合入、exact-main 门与匿名
  读回全部成立后，状态才是 `R1_DERIVATION_EXECUTION_CELL_FROZEN /
  R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只允许先审计 Provider Run、candidate Fact
  provenance、canonical Fact admission 与 FactSet/DerivationEvidence closure eligibility；不得直接实现真实
  parser、publication、Relation、conflict/UNKNOWN、Slice、Coverage 或完整 Manifest。
- `docs/154-r1-fact-evidence-closure-system-audit.md` 已从 exact
  `main@a96912fa3f141a783e728f95e0feb26341197a32` 完成上述前合同系统审计。审计拆开 Provider candidate、
  application-canonical Fact、FactSet admission 与公共 Artifact membership，确认 phase reported IDs 不能
  原样复制为 final Evidence reported IDs；COMPLETE Manifest 仍禁止 Fact/Evidence standalone publication。
  审计还以三个均被 `DerivationEvidence 0.1.1` Schema 接受但 digest 不同的 `PROVIDER_FAILED` 单变量向量证明
  non-budget diagnostic placement 尚未冻结，并确认 terminal stop 后 cleanup-only permission 与 DIAGNOSTIC
  publication/artifact budget 之间缺少明确 authority。当前状态为
  `R1_FACT_EVIDENCE_CLOSURE_PRECONTRACT_AUDITED /
  R1_FACT_EVIDENCE_CLOSURE_CONTRACT_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只能从新 exact main 起草 docs-only Fact
  Admission / DerivationEvidence Closure 合同；不得创建 parser、Provider SPI、FactSet/Evidence publisher、
  Relation、conflict/UNKNOWN、Slice、Coverage 或完整 Manifest 实现。
- `docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md` 已从 exact
  `main@0b2ca79191adc3743b2cf4663cd0cda7574a7912` 起草上述 docs-only 最小合同候选。它把 Provider
  candidate、application-canonical Fact、FactSet membership 与 published member 分为四层；成功 path 只建立
  owned non-published FactSet construction state，不提前构造 final COMPLETED Evidence。首个 single-Provider
  terminal diagnostic 固定为 run/top-level 同 tuple，artifact-budget 固定 top-only/null；有合法 phase result、
  且没有预算 stop 的 execution-cell non-success，只有在 release 成功、原 BudgetContext 仍 RUNNING、无 stop 且
  artifact reservation 为零时，才获得
  一次性 future DIAGNOSTIC closure eligibility。deadline/cancel/memory/artifact stop 与 RELEASE_FAILED 均不得
  发布 R1 Artifact。当前状态只能是 `R1_FACT_EVIDENCE_CLOSURE_CONTRACT_CANDIDATE /
  R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。候选自身的远端门、受保护主线合入、exact-main 门、
  匿名产品读回与后继独立冻结发布完成前，不得实现 integrated controller、Fact admission、Evidence projection，
  也不得创建 output path/publisher、real parser、Provider SPI、Relation、conflict/UNKNOWN、Slice、Coverage、
  COMPLETE Manifest、CLI 或 Workbench。
- `docs/156-r1-fact-evidence-closure-contract-freeze-publication.md` 从候选合入基线
  `main@3c237555b4924f08b7e82c523f675fbd28512e3c` 独立发布冻结事实。PR #136 的原始 Public CI 为
  11/11 SUCCESS；候选合入后的 exact-main Public CI 为 11/11、Browser Smoke 为 1/1，README、文档 155 与
  milestones 的三次 fresh anonymous installed-product readback 均由 Core 判为 PASS。冻结前第二轮系统审计
  又用 8 个 in-memory terminal projection 证明现有 `DerivationEvidence 0.1.1` Schema、固定 status、diagnostic
  placement/cardinality、空 reported IDs 与 digest 复算可同时成立，未发现新 blocker。本文自己的门禁、合入、
  新 exact-main 双门与匿名读回全部成立后，状态才是
  `R1_FACT_EVIDENCE_CLOSURE_CONTRACT_FROZEN /
  R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_ALLOWED /
  R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。授权只覆盖 private integrated controller、owned
  non-published Fact admission/Evidence projection 与 FA-001..024；output path/publisher、real parser、Provider SPI、
  Relation、conflict/UNKNOWN、Slice、Coverage、完整 Manifest、CLI 与 Workbench 继续禁止。
- `docs/157-r1-fact-evidence-closure-implementation-freeze-candidate.md` 记录上述窄实现已经由 PR #140 合入
  `main@86b62464b9eef00a5e9da8d0549f093767be27e2`。实现只新增 private integrated controller、owned
  non-published FactSet construction state、non-success Evidence projection 与 one-shot diagnostic eligibility；
  FA-001..024 focused gate 在 CPython 3.10/3.13 normal/`-O` 四格均为 27/27，完整 Review Attention 回归四格
  均为 133/133。PR 首次 pre-rebase run 因既有 aggregated Python job 的 15 分钟 outer timeout 被取消；该事实
  保留，独立 PR #141 只把 CI containment 调整为 20 分钟并完成自己的 11/11、exact-main 双门与匿名 workflow
  byte readback。实现 patch-id 不变地 rebase 后，PR #140 的有效原始门为 11/11；实现 exact main 的 Public CI
  为 11/11、Browser Smoke 为 1/1。本文状态只能是 `R1_FACT_EVIDENCE_CLOSURE_IMPLEMENTED /
  R1_FACT_EVIDENCE_CLOSURE_FREEZE_CANDIDATE /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。候选自己的门、合入、exact-main 门、匿名产品读回
  与后继独立最终状态发布完成前，不得写成 frozen，也不得开始 output publisher、真实 parser、Provider SPI、
  Relation、conflict/UNKNOWN、Slice、Coverage 或完整 Manifest。
- `docs/158-r1-fact-evidence-closure-freeze-publication.md` 从候选合入基线
  `main@a4c63607d8a586a5ec19eae1cdc4279cda1ffa88` 独立发布实现冻结事实。PR #142 原始 Public CI 为
  11/11 SUCCESS；候选 exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。README、文档 157 与
  milestones 的三次 fresh anonymous installed-product readback 均使用 R1 专属 sealed Plan、acceptance ID、
  summary kind 与 boundary，由 Core 判为 PASS；最初复用 P4 release-candidate label 的三份运行因 evidence
  identity 不匹配已作废，未进入联合摘要。本文自己的门禁、合入、新 exact-main 双门与匿名读回全部成立后，
  状态才是 `R1_FACT_EVIDENCE_CLOSURE_FROZEN /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步必须先从新 exact main 做系统级审计，再
  选择一个最小合同；不得预先承诺或直接实现 output publisher、真实 parser、multi-Provider Fact、Relation、
  conflict/UNKNOWN、Slice、Coverage 或完整 Manifest。
- `docs/159-r1-post-fact-evidence-next-closure-system-audit.md` 从 exact
  `main@7141999383489f51cf6f87806d2d271496499584` 比较 DIAGNOSTIC publisher、真实 parser、
  multi-Provider Fact composition、Relation、Slice、Coverage 与 COMPLETE publisher。审计确认完整发布必须等待
  八文件闭环，DIAGNOSTIC publisher 是正交失败留档能力，real parser 不能先替合同决定 Provider applicability；
  `provider_requirements -> exact Provider descriptor set`、共享 BudgetContext、required/optional join、same-ID
  provenance merge 与 same-subject conflict 同时约束 FactSet、Evidence、Relation 入口、Slice conflict gate 与
  Coverage UNKNOWN，因此选择 multi-Provider applicability / Fact composition 作为下一份最小 docs-only 合同。
  本文自己的远端门、合入、exact-main 双门与 R1 专属匿名读回全部成立后，状态才是
  `R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED /
  R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。不得因审计选择而直接开始实现，也不得创建 real
  parser、public Provider SPI/discovery、publisher、Relation、Slice、Coverage、CLI、Workbench 或 COMPLETE
  Manifest。
- `docs/160-r1-multi-provider-applicability-and-fact-composition-contract.md` 从 exact
  `main@22df05698f05380e910ac8a4e0cc6ba1276842e7` 起草下一份 docs-only 合同候选。它把 requirement、
  applicability、descriptor、binding 与 ProviderRun 分开，以合同定义的 private conformance table 导出 exact binding
  tuple；requiredness 由 capability requirement 继承，所有 Provider 串行消费同一 BudgetContext。run-local
  conformance 先闭合，之后才允许 same-ID semantic merge、provenance union 与 same-subject FactConflict；required/
  optional terminal join、diagnostic placement 与 final reported-ID 清空保持机械。当前状态只能是
  `R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_CANDIDATE /
  R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。候选自己的远端门、主线合入、exact-main 双门、匿名
  产品读回与后继独立冻结发布成立前，不得实现；real parser、public Provider authorization/SPI/discovery、
  publisher、Relation、Slice、Coverage、Manifest、CLI 与 Workbench 继续禁止。
- `docs/161-r1-multi-provider-fact-composition-contract-freeze-publication.md` 从候选合入基线
  `main@9c336e02318791b411c9abfa8cf662fb97f61f47` 独立发布合同冻结事实。PR #145 原始 Public CI 为
  attempt 1、11/11 SUCCESS；candidate exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。README、
  文档 160 与 milestones 的三次 fresh anonymous installed-product readback 均使用 R1 专属 acceptance identity，
  P1/P2 coverage COMPLETE、三样本稳定、Core PASS，canonical summary 联合 SHA-256 为
  `82a160f94a5e8f5bc8adfaf836e886c6b70f3c7f28cf31e2131b1813a4ff0905`。本文自己的门禁、合入、新
  exact-main 双门与匿名读回全部成立后，状态才是
  `R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_FROZEN /
  R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_ALLOWED /
  R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。授权只覆盖 private closed applicability table、共享
  BudgetContext 下串行 single-Provider child cells、run-local conformance、same-ID merge、same-subject conflict、
  terminal join 与 `MP-001..028`；real parser、public Provider authorization/SPI/discovery、publisher、Relation、
  Slice、Coverage、Manifest、CLI 与 Workbench 继续禁止。本状态发布自己的最后门成立前，分支文字不授权实现。
- `docs/162-r1-multi-provider-fact-composition-implementation-freeze-candidate.md` 记录上述 private 实现已经由
  PR #147 合入 `main@590df332fbd60bdfc857a4ea3f3c35937ce03d8a`。实现只新增 application-owned closed
  applicability table、共享 BudgetContext 下的串行 child cells、run-local conformance、same-ID merge、
  same-subject FactConflict、required/optional terminal join 与 private FactSet/Evidence projection；没有真实 parser、
  public Provider SPI/discovery、publisher、Relation、Slice、Coverage 或 Manifest。PR 原始 Public CI 与实现
  exact-main Public CI 均为 attempt 1、11/11，exact-main Browser Smoke 为 1/1，七个变更文件匿名 raw-byte
  readback 与 Git tree 一致。当前状态只能是 `R1_MULTI_PROVIDER_FACT_COMPOSITION_IMPLEMENTED /
  R1_MULTI_PROVIDER_FACT_COMPOSITION_FREEZE_CANDIDATE /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。本文候选自己的门、合入、exact-main 双门、匿名产品
  读回与后继独立最终状态发布完成前，不得写成 frozen，也不得开始任何延期能力。
- `docs/163-r1-multi-provider-fact-composition-freeze-publication.md` 从候选合入基线
  `main@66b2252c5261387e1d1b40899f3e009e6ed6cecf` 独立发布实现冻结事实。PR #148 原始 Public CI 为
  attempt 1、11/11 SUCCESS；候选 exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。README、文档
  162 与 milestones 的三次 fresh anonymous installed-product readback 均使用新的 R1 implementation-candidate
  acceptance identity，P1/P2 coverage COMPLETE、三样本稳定、Core PASS，联合 summary SHA-256 为
  `c098ffeefea338b9ab220bca0e2c521ec5d0faaae9970699367c20deab8fa7da`。第一次 README 工具尝试因
  `plan_id` 超过 Core 长度上限在采集前失败，未产生输出；修正后从新目录建立有效 evidence。本文自己的门、
  合入、新 exact-main 双门与匿名读回全部成立后，状态才是
  `R1_MULTI_PROVIDER_FACT_COMPOSITION_FROZEN /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步必须先从新 exact main 做系统级审计，再选择
  一个最小合同；不得直接开始 parser、publisher、Relation、Slice、Coverage 或完整 Manifest。
- `docs/164-r1-post-composition-next-closure-system-audit.md` 从 exact
  `main@3575cc90faffd41c7172339f461c583e748f2215` 比较 DIAGNOSTIC publisher、real parser/public Provider
  boundary、Relation derivation、Slice、Coverage 与 COMPLETE publisher。审计确认当前 worker/phase 只产生
  Facts、`reported_relation_ids=[]`，而完整 fixture 让 ProviderRun 背书 Relations；同时
  `IMPORT_TARGET_LITERAL` 的 final resolution 必须消费 multi-Provider composition 后的 exact FactSet，现有
  Provider operands 又不绑定 `fact_set_digest`。因此下一最小合同只选择 Relation derivation authority、exact
  FactSet operand continuity、provenance/reporting 与 minimum upstream eligibility gate，不预选 Provider 二阶段
  或 application derivation 模型，也不把完整 Relation 算法、conflict/UNKNOWN 账册或 admission 打包进来。
  facts-only real parser 可以是独立后继，但不得借机固定 Relation authority。本文自己的远端门、合入、
  exact-main 双门与 R1 专属匿名读回全部成立后，状态才是
  `R1_RELATION_DERIVATION_PRECONTRACT_AUDITED /
  R1_RELATION_DERIVATION_CONTRACT_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。不得因审计选择直接修改 Schema 或实现 Relation；
  public Provider SPI/discovery、完整 RelationSet composition/admission、publisher、Slice、Coverage、Manifest、CLI
  与 Workbench 继续禁止；real parser 若先行也只能是独立 facts-only 合同，不得与本审计自动捆绑。
- `docs/165-r1-relation-derivation-authority-and-operand-continuity-contract.md` 从文档 164 收口后的 exact
  `main@41a398783d5eaf25e15574df5beafb8465d0a91e` 独立起草 docs-only 合同候选。文档 164 的 PR #150
  head 原始 11 项 required checks 全绿；exact-main Public CI run `34930110622` attempt 1 保留 10/11
  FAILURE（E3 Release 资产六次 HTTP 500），failed-jobs rerun 的 attempt 2 组合 11/11 SUCCESS 中只有 E3
  新执行，其余十项继承 attempt 1 成功事实；Browser Smoke run `34930110603` attempt 1 为 1/1 SUCCESS。
  README、文档 164、milestones 的三个新 anonymous installed-product P1→P2→P3→Core session 均 PASS，
  联合 summary SHA-256 为 `9fd68f63fc6ce3ea60f1d3aea014b8c61018b8f9adadd9637ad9bc79cbed08bf`。
  §4.1 反证复核未发现能推翻选题的新证据。候选选择 composed FactSet 后一个由 newly sealed requirement
  支持的 distinct closed Relation ProviderRun，而不回填 Fact Provider 报告或让 application 自造来源；
  relation-only operands 必须以版本化投影绑定 `fact_set_digest`；新 profile 的 Fact-stage private join 先构造
  FactSet，Relation terminal 后才能投影 final overall，避免 required Relation run / FactSet 循环等待。
  同一次 execution 保持 live shared BudgetContext。首版 FactConflict、optional-source gap 和 absent normal FactSet 只保留 upstream truth，
  不启动 Relation run。当前分支只能是 `R1_RELATION_DERIVATION_CONTRACT_CANDIDATE /
  R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。候选自己的原始门、受保护主线合入、新 exact-main
  双门、专属匿名产品读回与后继独立冻结发布成立前不得写成 FROZEN；现有 Fact cell wire、Schema、identity
  vectors、runtime、real parser/public SPI、完整 RelationSet admission、publisher、Slice 与 Coverage 继续未授权。
- `docs/170-r1-relation-derivation-contract-freeze-publication.md` 独立发布文档 165 的最小合同，不实现
  Relation。它绑定候选 PR #151 的 base/head/merge/tree、保留 Public CI 首次 10/11 与 failed-jobs rerun 的
  部分重跑事实，并以同一 head 的新鲜 11/11、候选 exact-main 双门和三次专属匿名产品读回支撑冻结判断。
  文档 168/169 只收紧后续 source-state 与 GitHub workflow/attempt authority，不回填或改写 R1 历史。本文
  自己的原始远端门、受保护合入、新 exact-main 双门与三次 fresh anonymous installed-product readback
  全部成立后，状态才是 `R1_RELATION_DERIVATION_CONTRACT_FROZEN /
  R1_RELATION_DERIVATION_IMPLEMENTATION_ALLOWED /
  R1_RELATION_DERIVATION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。授权只覆盖 relation-only `/0.2` identity/vector、
  固定 phase join、distinct relation-only cell、保守 upstream gate、原 live `BudgetContext` 与 `RD-001..017`
  的 private closed implementation。真实 parser identity 必须实际使用；否则先独立审议最小 Evidence 修正，
  不得虚填。完整 Relation 算法、RelationSet composition/admission、public Provider、publisher、Slice、Coverage、
  CLI、Workbench、D、Cu 与 Q 继续未授权。
- `docs/171-r1-relation-derivation-implementation-freeze-candidate.md` 记录上述 private closed 实现已经由 PR #156
  合入 `main@122d0c6b9d3c7a4518f12aec2f503f8979018dda`。实现新增 relation-only `/0.2` identity/vector、固定
  Fact/Relation phase join、distinct Relation cell、保守 upstream gate、同一个 live `BudgetContext` 与真实使用
  Python 3.10 grammar 的 closed parser/provider；没有完整 import resolution、RelationSet、publisher、Slice、
  Coverage 或公共 API。PR 与实现 exact-main Public CI 均为 attempt 1、11/11，exact-main Browser Smoke 为
  1/1；十一份变更文件匿名 raw-byte readback 与 Git tree 一致。当前状态只能是
  `R1_RELATION_DERIVATION_IMPLEMENTED / R1_RELATION_DERIVATION_FREEZE_CANDIDATE /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。本文自己的门、合入、exact-main 双门、匿名产品
  读回与后继独立最终状态发布完成前不得写成 frozen，也不得开始延期能力。
- `docs/172-r1-relation-derivation-freeze-publication.md` 从候选合入基线
  `main@eb75d360b828fd45007be9f94892e4101af27e50` 独立发布实现冻结事实。PR #157 原始 Public CI 为
  attempt 1、11/11 SUCCESS；candidate exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。README、文档
  171 与 milestones 的三次正式 anonymous installed-product session 均为 P1/P2 COMPLETE、稳定样本、唯一
  marker 与 Core PASS，联合 manifest SHA-256 为
  `8cd8efe6499cd754ab2668e87e8534c26858a178fd65da55141ae8a1761746d2`。第一条 README session 的
  late `PublicRenderNetworkError / ERROR` 继续保留，根因为 `UNKNOWN`；coverage-neutral telemetry write 不是
  已证原因，旁路诊断 session 不进入门禁。本文自己的原始远端门、受保护合入、新 exact-main 双门与三次 fresh
  anonymous installed-product readback 全部成立后，状态才是 `R1_RELATION_DERIVATION_FROZEN /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。完整 Relation algorithm/import resolution、
  RelationSet、conflict/UNKNOWN、publisher、Slice、Coverage、CLI 与 Workbench 继续未授权；下一步必须先做
  post-freeze system audit，不得直接施工。
- `docs/173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md` 从 Relation Derivation
  冻结 exact `main@d54ee43170779f54ec88b9839ad80d48056aa033` 独立审计下一闭环。exact-main 本地反例证明
  Relation ProviderRun 可以 `COMPLETED` 且只报告 `LEXICAL_CONTAINS`，同时冻结 Profile 仍列有
  `IMPORT_TARGET_LITERAL`；因此 provider terminal、source-local output closure、required source-set terminal、
  bounded observation-domain qualification、RelationSet admission 与 final publication 不能合并。下一问题面识别为
  declared Relation observation domain / composition qualification，只允许后继独立 docs-only 合同审议 source
  responsibility、successful-empty 边界、required/optional observation、multi-source merge/conflict 与 qualification
  identity。当前分支只能是 `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_SYSTEM_AUDIT_CANDIDATE /
  R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_NOT_STARTED`；本文自己的原始远端门、受保护主线合入、
  新 exact-main 双门与专属匿名读回全部成立后，才提升为 `PRECONTRACT_AUDITED`。完整 Relation algorithm/import
  resolution、RelationSet admission、final Evidence、public Provider、publisher、Slice、Coverage、CLI、Workbench、
  D、Cu 与 Q 继续未授权；本地事实已足以选择问题面，因此本轮不以外部 production case 替代本地反例。
- `docs/174-m10-listener-owner-mismatch-fixture-timing-correction.md` 记录 PR #160 原始 Public CI 在 Python 3.13
  真正执行 450 tests 后暴露的既有 listener-owner-mismatch 测试时序缺口。正式首败保持成立；诊断只把归因
  收窄为夹具从过早坐标开始计算 `1.5s` 外部 listener 寿命。把寿命延长到 `30s` 的本地候选又合法触发
  `CLEANUP_ERROR`，因此被反例否决；最小修正只在 disputed node 进入既有 readiness adapter 时建立原
  `1.5s` external owner，继续同时证明 no-kill 与 cleanup release。该维护自己的原始远端门、受保护合入与
  新 exact-main Public CI / Browser Smoke 全部成立前，PR #160 保持停止；随后必须吸收新 main、形成新 head
  SHA 并重新取得完整门禁，不得用维护绿色或旧 head rerun 覆盖 #160 attempt 1。source-root `PYTHONPATH`
  四包组合只证明 current-source regression，不等同 installed-product/CI topology。
- M9 独立合同 0.2 位于 `docs/14-m9-controlled-command-execution.md`，已在 `290b618` 进入
  `IMPLEMENTING`；`4d2bc84` 完成 Plan 0.5、ToolBindings 0.1、CommandPreview 0.1 与
  `command-preview` CLI，`9f979c8` 完成锁定 `pywin32==312` 的 Windows Job Object 所有权后端和
  真实 helper 自动化，`fa27b51` 完成 Plan 0.5 `run` 与严格 `runtime.command`，`9031719` 新增
  两个独立轻量 Subject 和真实 Python/Node 正负矩阵。冻结提交 `3181d69` 已通过真实命令、重复 Run、
  适用负向、双视口 Chromium、Catalog/Workbench、Console/Network、内置浏览器物理键盘、双 Python/
  前端回归与最终清理，并已从 GitHub 读回 `main` 和 `m9-v0.10.0` 标签，状态为 `FROZEN`。M9 仍只
  允许一个可信、直接启动、无 Shell、无 stdin/TTY 的 `ONESHOT` 进程；不得顺手加入服务、
  自举、包管理器或前端控制台，也不得把结构化 runner 描述成文件系统、网络、TOCTOU 或恶意代码沙箱。目标
  标签 `m9-v0.10.0` 必须继续指向 `3181d69`；越过合同边界时必须开启后继里程碑而不是改写该基线。
- M10 独立 Contract 0.2 位于 `docs/15-m10-bounded-project-bootstrap.md`。冻结提交
  `008444319a4af54de3291fe5c0ab602001c30754` 已完成公共退出矩阵、M0–M10 地基与安全审查、严格
  串行、双 Python 228/228、Workbench 58/58、16 GB 有界压力、Codex 内置浏览器与零残留复验；
  冻结读回时 GitHub `main` 和 `m10-v0.11.0^{}` 均指向该提交。冻结后地基纠偏已在实现提交
  `f4efdd25c50b19077c61994bce3e2aca5244d5ec` 完成双 Python 262/262、Workbench 59/59、公共出口、
  16 GB 有界压力、生产浏览器与清理复验；首次补丁冻结读回时，GitHub `main` 与
  `m10-v0.11.1^{}` 均指向该提交，当前 M10 地基状态为 `FROZEN`。`m10-v0.11.0` 和
  `m10-v0.11.1` 均不得移动。M10 只证明 Windows 11、
  `C1 PROCESS_COLD`、一个 Run-owned dependency、一个 application、
  `HTTP_GET_LOOPBACK_OWNED_PID` readiness、既有 Browser Adapter 与逆序 Job 清理；C0 接管、
  C2/C3、Docker、跨平台、包管理器、第二类真实项目、不可信代码隔离和优雅停机均未证明。不得把
  M10 冻结解释为允许跳过后继合同。
- M11 只读候选盘点与探索探针位于 `docs/22-m11-real-project-suitability-and-contract-draft.md`。探针已
  证明现有候选不能直接装入 M10 两节点边界，并证明 InkNarratives 原始目录的单节点 HTTP/代表页
  浏览器形态真实可运行。用户已确认 `OPTION_B`、精确 ref、Gate A -> Gate B 严格串行和不适用项；
  `docs/23-m11-single-node-real-project-contract.md` 的 0.2 已在 `eb39c0a` 留下历史，Contract 0.3
  纠正 Plan/Profile 一对一权威绑定，当前 Contract 0.4 只版本化 Gate B 的响应式交互纠偏。Gate A 已完成 Profile 0.2、Plan 0.7、单 APPLICATION、
  collector 0.3、双 Python、真实 Chromium、13 个预注册出口、Catalog/Comparison、资源、安全、
  清理与 Workbench 验证，事实见 `docs/25-m11-gate-a-validation.md`。Gate B Plan v1 已在预注册提交
  `2c14393` 后启动；首个正向 Run 因移动视口长卷导航隐藏而
  得到 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`，失败目录
  `tmp/m11-gateb-contract03-20260814-160143` 必须保留，后续三个 v1 Run 未启动。Contract 0.4 将两个
  Gate B Plan 升为 version 2、保留 Profile v1 与全部资源/裁决边界，并使用新 Run ID；v2 已严格串行
  取得 `PASS / FAIL / PENDING / PASS`、Comparison `MATCH`、Catalog/Workbench、内置浏览器物理键盘、
  双 Python 277/277 与零残留事实。系统审查修复了 Workbench 验收脚本在 `python -O` 下会移除关键
  `assert` 的门禁缺陷；优化模式完整 Workbench 复跑通过。冻结提交
  `b13e2fb20a3aa670d8daba1ea78b5f9f0f7bac40` 已推送；冻结读回时远端 `main` 和
  `m11-v0.12.0^{}` 均精确指向该提交，M11 状态为 `FROZEN`。事实见文档 26、27；M12 已以
  `m12-v0.13.0` @ `5f32c33` 冻结；M13 已按文档 52 完成系统与 L0–L3 终审，事实见文档 53，
  M14 已按文档 54–57 完成安全整改、双目标严格串行终验、稳定 `0.12.0` 与首个最终 Release，
  当前为 `FROZEN / RELEASED`。
- M11 入口治理与 M0-M10 当前复验位于 `docs/24-m11-entry-governance.md`。它保留首次 Python 3.10
  Chromium 瞬态失败以及后续双解释器完整全绿事实，只允许继续入口枝叶整理；它不证明 M11 已实现。
- M12 表现系统重构设计计划 0.1 位于 `docs/28-m12-palace-workbench-design-plan.md`。M12-A 控制组审计已在
  `docs/29-m12-a-control-baseline-audit.md` 闭环；M12-B 已在提交 `7b8b72d` 完成四向公共视图、十字中轴导航、
  URL/history、焦点与移动几何，事实见文档 30、31。M12-C 已实现语义 token、十字的 token-bound 视觉迁移、
  Catalog 行式目录与 Runs 主链，并通过 64/64 前端、真实 Gate B 生产 Chromium、优化模式门禁与 Codex 内置浏览器
  桌面/390/360 px 的真实交互补证，事实见文档 33。M12-D 派生分析视图计划 0.1 位于文档 34；D1 Comparison
  已在文档 35 形成真实 M11 MATCH、脱敏 DRIFT/INCONCLUSIVE、生产 Chromium、优化模式与内置浏览器事实；D2 Pairing
  已在文档 40 形成 M7 三态、四文件导入、生产 Chromium 常规/优化模式、内置浏览器和清理事实；D3 Batch 已在文档 42
  形成 M8 四态、矩阵/slot 顺序、局部滚动、原生 details、损坏恢复、刷新隐私、生产 Chromium 常规/优化模式、用户物理键盘
  和清理事实。M12-B/C 空间收束与 Runs 目录整改计划 0.1 已在
  `docs/36-m12-bc-spatial-recomposition-plan.md` 确认：R1 公共外壳（Header、十字中枢与过门）与 R2 Runs
  主链均已在文档 37、38 通过生产 Chromium、内置浏览器和清理事实。D2 Pairing 的计划 0.1 位于文档 39、事实位于
  文档 40；D3 Batch 计划 0.1 位于文档 41、事实位于文档 42，已在其 `L0_PRESENTATION + BOUNDED_L1_COMPONENT`
  边界内闭环。M12-E Browser Evidence 与全局状态计划 0.1 位于文档 43、运行事实位于文档 44，已在
  `L0_PRESENTATION + BOUNDED_L1_COMPONENT` 边界内通过 70/70 Workbench、生产 Chromium 常规/优化模式、
  360/390px、forced-colors、内置浏览器、物理键盘和清理门禁；`StatusBadge.vue` 仍未被用作局部整改的全局入口。
  M12-F 总体验收与冻结计划 0.1 位于文档 45，最终事实位于文档 51；Workbench 156/156、双 Python
  各 278/278、D1/D2/D3、常规与优化生产 Chromium、内置浏览器、用户逐页确认及零残留均已通过。
  冻结读回时远端 `main` 与 `m12-v0.13.0^{}` 均精确指向
  `5f32c33ab3dac076151a4fcd9a93a74ccafcfaa9`；M12 状态为 `FROZEN`。M13 已在文档 52 边界内完成，
  关闭优化模式验收 fail-open、安全说明漂移、Catalog 旧空态和公共文档本机路径四项问题；双 Python
  279/279、Workbench 156/156、常规/优化生产总验收、安全、依赖、浏览器与清理事实见文档 53。
  M13 状态为 `FROZEN`；M14 已按文档 54–57 完成并以 `v0.12.0` 冻结。后续入口层或新能力不能
  静默改写该基线，也不能把 M13/M14 定向证据继承为新能力的产品证明。
- 开始工作前依次阅读 `README.md`、`docs/00-product-brief.md`、`docs/01-evidence-model.md`、`docs/02-architecture.md` 和 `docs/03-acceptance.md`。
- 产品事实与代码不一致时先停止并指出冲突；不得静默降低方法论或安全边界。

## 核心原则

- 控制变量法是产品核心：一个可归因实验只能有一个主要变量。其他变量必须冻结、记录为受控变量，或明确列为干扰/未知变量。
- 单变量证明因果，组合批次验证交互，固定种子随机扰动寻找偶发故障，代表性全链路形成系统级结论。
- 运行状态与验收结论分离。资源中止使用 `ABORTED`；证据不足使用 `PENDING`；变量污染或无法归因使用 `INCONCLUSIVE`；不得借硬件限制伪造 `PASS/FAIL`。
- 吞吐目标可以受资源限制，一致性、安全和其他硬性不变量不能降级。
- 实验开始前冻结计划、断言、停止线和裁决规则。观察结果后若需修改，创建新计划版本并保留旧运行，不得移动原实验的判定标准。
- 重要结论应支持重复、配对或反事实复跑；验迹自身的 CPU、内存、连接和采样开销与被测对象分开记录。

## 开发与资源边界

- 优先建立最小纵向闭环，再扩展适配器；不要先堆积导入器、仪表盘或中间件集成。
- 16 GB Windows 主机默认串行或受限微并行。测试必须有启动前资源预检、软/硬停止线、现场保存和批次清理确认。
- v0 架构规划使用 Python Core、SQLite、Vue Workbench 和 Playwright/CDP；当前冻结基线已包含
  Python Core、可重建 SQLite Catalog、固定回环只读 API、Vue Workbench 与 Playwright/CDP。
  不要求 Docker、MQ、搜索或外部云服务。
- M3 Workbench 只读消费 Report/Evidence/Manifest 和浏览器附件，不在前端重新裁决，不修改
  M0–M2 Schema；M3 本身不包含 SQLite、本地 API 或自举闭环，这些由 M4 独立合同交付。
  不能把 M3/M4 的只读 UI 与轻量自举当成计划编辑或执行编排已经完成。
- M4 必须保持 Bundle 为权威事实、SQLite 为可重建派生索引、服务为固定回环只读
  API；不得在该里程碑加入在线写、文件监视、跨 Run 差异、任意命令或被测对象生命周期管理。
- M5 冻结基线只允许 Core 内置的 `STATIC_HTTP` 目标适配器；不得扩大为任意 Shell、外部
  可执行文件、npm/Maven、Docker、中间件或项目服务生命周期管理。Plan 0.4 必须向后兼容，
  所有异常路径先清理再形成证据，定义和自动化都不得冒充真实运行。
- M6 冻结合同只比较两个不同 Run ID、同 sealed Plan 的不可变 Bundle，生成独立 Comparison
  Bundle；不得修改来源 Verdict、自动挑选成功 Run、把 Comparison 写进 M4 Run-only Catalog，
  或把同计划复跑一致性扩张为处理组因果结论。
- M7 冻结合同固定 `BASELINE -> TREATMENT -> RESTORED_BASELINE -> NEGATIVE_CONTROL` 四角色，
  新增独立 PairingPlan/PairedAnalysis；不得修改 M0–M6 契约、删减不利角色、把配对结果写成
  来源 `PASS/FAIL`，或扩大为统计显著性、组合变量与任意执行器。
- M8 冻结合同使用独立 BatchPlan/BatchAnalysis 表达 4–16 格全因子 Profile；确定性 coverage
  必须先完成，seed 只能改变 perturbation 顺序，不能改变成员或补写缺格。M8 不执行来源 Run、
  不证明真实并行，不把 Profile 信号写成组件级因果或来源 `PASS/FAIL`。
- v0 不接受任意 Shell 字符串执行。若未来引入命令执行，必须采用结构化参数、显式预览、最小权限和可审计允许列表。
- M9 Windows 进程后端锁定为项目虚拟环境内的 `pywin32==312` 可选依赖；只能在实施时显式安装到
  Git 忽略的项目虚拟环境，不得自动安装、全局安装、运行 `pywin32_postinstall`，也不得在缺失时
  降级为 `ctypes`、普通 `Popen` 或 PID/进程名轮询。
- 不记录或提交 `.env` 值、令牌、Cookie、Authorization 头、私钥、个人路径或原始敏感业务数据。采集器必须默认脱敏。

## 分层审查与里程碑门禁

- 变更开始前必须声明影响层级：`L0 表现层`、`L1 组件内部`、`L2 公共契约`、`L3 系统级`。实际 diff 越界时立即升级审查与验收范围。
- 局部需求不得顺手修改全局序列化、共享配置、公共 Schema、通用中间件、状态机、安全或数据所有权。确需修改时，列出全部消费者、兼容策略和回归矩阵。
- 审查先确定所有者、调用者、数据流、失败边界和爆炸半径，再讨论实现细节；避免用全局改动解决局部问题。
- 里程碑可以提前规划，但前一里程碑没有完成代码事实、自动化证据、真实运行证据并冻结为可寻址基线前，不得开始下一里程碑的实现。
- 资源不足导致前一里程碑最终验收 `PENDING` 时，下一里程碑继续保持 `PLANNED`；不得把未闭环问题向后传递。
- 代码、配置、依赖、数据或拓扑越过基线容差后，旧结论标记过期并重新验收；不得把历史 `PASS` 自动继承给新版本。

## 验收门槛

- 单元测试、静态检查和 Mock 只算自动化证据，不能替代真实浏览器与真实运行证据。
- 浏览器能力必须检查 Console、Network、关键交互、失败重试、桌面/移动视口和未解释的 4xx/5xx。
- 涉及多实例、幂等、消息、缓存或最终一致性时，必须核对权威事实、重复副作用、故障恢复和退出条件。
- 每个证据文件都应进入清单并计算哈希；报告必须能追溯到代码版本、环境快照、实验计划和随机种子。
- 无法完成最终验收时，明确标记 `PENDING`，不要用“实现完成”冒充“产品完成”。

## Git 与文档

- 保持提交单一意图，提交前检查 `git diff --check`、敏感信息和生成物。
- `artifacts/`、本地数据库、浏览器 trace/HAR、截图和运行日志默认不提交；只有经过脱敏的最小夹具可进入仓库。
- 修改模型或结论语义时同步更新全部相关文档，并写明迁移或兼容边界。
