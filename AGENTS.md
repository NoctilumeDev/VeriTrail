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
  `pattern_id + selected_record_digest` 的 Pattern Corpus 后才能启动。当前仍为
  `R0_ARCHITECTURE_FROZEN / DESIGN_ONLY`；P2 的新反例可以按 Ledger Schema 追加，但不得借此启动 R1。
  文档 91 已把 P1/P2 的开放世界观察经验归纳为非合同方法，并在 R 轨 Plan 中补充 R1 的未来
  Semantic Review Slice 边界：slice 由精确 SourceSnapshot 的确定性关系图派生，可以重叠但必须
  有界、可追溯并保留 coverage/truncation；slice derivation、analysis 与 attention ranking 不得合并。
  该补充不新增 R0 Artifact、不冻结 Slice Schema，也不解除 R1 前置阻断。
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
