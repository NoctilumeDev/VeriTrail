# VeriTrail 项目指令

## 0. 必读工作法

开始任何 VeriTrail 施工、审计、状态判断或“下一步”选择以前，**MUST READ**
[证据反馈工作法](docs/working-method.md)。该文件规定本项目的 `CONTROL LOOP` 与
`QUALIFICATION PIPELINE`；文档编号、README、roadmap 和绿色 CI 均不得替代这两个过程。

最小不变量如下：

- 工作法只规定**怎样判断与施工**，不保存当前项目事实；当前 SHA、状态、authority 与下一合法 seam 必须每次从
  exact main 和保留证据重新构造；
- 用户在聊天中提供的日志、判断与草稿只作线索；material claim 必须回到源码、冻结合同、原始 PR attempt、
  exact-main gates、Artifact 与 fresh product readback 复核；
- 先执行外层证据反馈回路，确认当前问题与最小授权仍成立；之后才允许进入本轮资格链；
- target state 可以条件化写入 publication，但全部冻结门闭合以前不得宣称生效；
- 测试只作 witness，不拥有合同扩张、reason 解释、状态升级或下一阶段授权；
- 相同 patch、内容、摘要或 semantic result 不继承另一个 exact coordinate、attempt 或 continuation 的资格；
- 碰到矛盾先保现场并归层，不能先修、先重跑或把后来的 PASS 用来覆盖先前事实；
- frozen scope 禁止静默修改；真实反例可以显式 reopen/version bump 被击穿的最小边界并重新资格化；
- publication 形成新事实后必须返回外层回路；不得按文档编号自动进入下一阶段。

重大阶段退出或 release closeout 前，**MUST READ**
[仓库遗留物收口门禁](docs/hygiene.md)。该门禁只处理已失去职责的施工残留，不授予产品语义、冻结状态或
下一阶段施工权。R1 合同、审计、首败、fixtures、Schema、readback identity，以及仍承担视觉或运行职责的
资产均有明确 owner；不得因为“旧”“大”或当前入口未直接引用就删除。

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
  identity。PR #159 原始 Public CI 11/11 后合入
  `main@559bf9b9a052f0b542227b1cea069dd15c696cc8`；新 exact main 的 Public CI 11/11、Browser Smoke 1/1
  与 README/文档 173/milestones 三次 fresh anonymous installed-product readback 均成立，联合 manifest
  `sha256_json=6a88636093691394ced966199c153bd9cc95e331fadbcc968aebfd48436c6fe1`。因此当前审计状态已是
  `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED`。完整 Relation algorithm/import
  resolution、RelationSet admission、final Evidence、public Provider、publisher、Slice、Coverage、CLI、Workbench、
  D、Cu 与 Q 继续未授权；本地事实已足以选择问题面，因此本轮不以外部 production case 替代本地反例。
- `docs/174-m10-listener-owner-mismatch-fixture-timing-correction.md` 记录 PR #160 原始 Public CI 在 Python 3.13
  真正执行 450 tests 后暴露的既有 listener-owner-mismatch 测试时序缺口。正式首败保持成立；诊断只把归因
  收窄为夹具从过早坐标开始计算 `1.5s` 外部 listener 寿命。把寿命延长到 `30s` 的本地候选又合法触发
  `CLEANUP_ERROR`，因此被反例否决；最小修正只在 disputed node 进入既有 readiness adapter 时建立原
  `1.5s` external owner，继续同时证明 no-kill 与 cleanup release。维护 PR #161 原始 Public CI run
  `35532371731` attempt 1 为 11/11，随后受保护合入 `main@962251d91bc2695afe984ee47845ac4fe1a80f7e`；该 exact main 的 Public CI
  run `35533373276` attempt 1 为 11/11，Browser Smoke run `35533373269` attempt 1 为 1/1。PR #160
  的正式首败仍保留；合同候选必须吸收该 exact main、形成新 head SHA 并重新取得完整门禁，不得用维护绿色或
  旧 head rerun 覆盖 #160 attempt 1。source-root `PYTHONPATH` 四包组合只证明 current-source regression，
  不等同 installed-product/CI topology。
- `docs/175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md` 的语义最初从审计
  exact `main@559bf9b9a052f0b542227b1cea069dd15c696cc8` 起草。PR #160 原始 head 的 Python 3.13 正式首败由独立文档 174 / PR #161
  维护关闭，首败没有被 rerun 或改写；当前候选从 maintenance-qualified exact `main@962251d91bc2695afe984ee47845ac4fe1a80f7e` 重新绑定
  source state。候选不把 Profile relation-kind 闭集当 required observation；它以 private versioned
  observation profile 将 exact FactSet 机械投影为 Fact-backed items，并在 Provider 执行前把 A/B exact
  responsibilities 固定。A 负责 lexical items，B 同时负责 lexical 与 import-literal items；两者继承 sealed
  required CUMULATIVE requirement、共享原 live `BudgetContext`，并以 relation-only operands `/0.3` 与 private
  relation cell `/0.2` 绑定 exact domain。`observation_profile_digest` 同时绑定 FactSet 以外的 family、negative
  policy 与 Provider responsibility semantics；定义 responsibility 不等于已履责。与每个 terminal run 绑定的
  private relation-cell terminal 必须另报 explicit per-item outcomes，application 对 outcomes 与 candidates 双向
  对账，不能从 candidate absence 补 negative。
  当前 total-obligation families 不允许 non-empty closed negative。Provider terminal、required source-set terminal、
  source-local item closure 与 candidate composition 分开；same-ID 合并 provenance，same-subject incompatibility 保留 private
  conflict，complete-empty 必须有空 assigned items 与真实 start/terminal/release。现有 RelationSet 0.1 与
  Evidence 0.1.1 不能单凭 shape 证明 qualification，因此首个实现即使以后获授权也只能返回 private state，
  不创建 RelationSet 或公共 Artifact。当前状态只能是
  `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_CANDIDATE /
  R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`；候选自己的远端门、受保护合入、exact-main
  双门、专属匿名读回与后继独立冻结发布成立前，不得写 runtime。完整 resolver、public Provider、Schema
  correction、RelationSet admission、final Evidence、publisher、Slice、Coverage、CLI、Workbench、D、Cu 与 Q
  继续未授权。
- `docs/176-r1-relation-observation-composition-qualification-contract-freeze-publication.md` 独立发布文档 175
  的最小合同，不实现 runtime。它保留 PR #160 原始 head 的正式 Python 3.13 首败、独立 PR #161 fixture
  maintenance 与被反例否决的 30s lifetime 候选；重新资格化 head
  `fde8df8279c27b5a222d58d2b0a5fd73c261a54f` 的有效原始 Public CI 11/11 后合入
  `main@bc495eb92c70f85566505d51d00677ac14f38ff2`，该 exact main 的 Public CI 11/11、Browser Smoke 1/1 与
  README/文档 175/milestones 三次 fresh anonymous installed-product readback 均成立，canonical manifest
  `sha256_json=0df7a15fb0193f2d86d26b07fc96991cdada73d28058e5edb6e7cbf426bc194c`。PR body edit 触发的同 head
  run `35534733454` 只形成 concurrency 行政取消，不冒充测试失败或成功。本文自己的原始门、受保护合入、
  新 exact-main 双门与三次 fresh anonymous installed-product readback 全部成立后，状态才是
  `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN /
  R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_ALLOWED /
  R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。授权只覆盖文档 175 A–H 的 private closed proof；
  RelationSet、公共 Schema、publisher、Slice、Coverage、CLI、Workbench、D、Cu 与 Q 继续未授权。
- `docs/177-m10-ci-fixture-observation-correction.md` 记录 private implementation PR #165 原始 Public CI
  run `35569800950` 的两条正式首败：Python 3.13 `-O` 的 emergency-cleanup 测试把已关闭 socket 的空闲端口
  观察误作后继 child 的端口预约；旧 Artifact 没有 child stderr/exit/owner 证据，因此只证明夹具前置条件未
  成立，不恢复该次失败的唯一底层触发。Python 3.10 `-O` 的 repeat 公共 Run 诚实 fail closed 为
  `COLLECTOR_ERROR`，但冻结 Artifact 与 CLI summary 未保存 private collector error type，精确根因保持
  `UNKNOWN`。L0 maintenance 只让 child 在自己的 `listen()` 成功后报告实际 OS-assigned port，并在 repeat
  测试层捕获、记录后立即重抛 `ObservedBrowserCollectionError`；不改 runtime、timeout、公共 Evidence、
  R1 合同或 #165 实现。维护候选自己的原始远端门、受保护合入与新 exact-main 双门成立前，#165 不得 rerun、
  合入或发布 freeze candidate；之后也必须从 maintenance-qualified exact main 形成新 head 并独立重新资格化。
- `docs/178-r1-relation-observation-composition-qualification-implementation-freeze-candidate.md` 记录文档 175 A–H
  已由重新资格化后的 PR #165 实现。原始 head `015bf8f19ca1269933749c53f67eebe33186bc58` 的两条正式首败
  继续保留；独立 PR #166 只修复 CI 夹具前置条件与 test-only 诊断能力，合入
  `main@43fd5d3368f962677722d09d962718bced306449` 后，#165 形成相同 implementation patch 的新 head
  `4bcba01dbdc7fb57c34451d154be8ef8f52bfb87` 并以原始 11/11 门禁合入
  `main@3b4a55cad4e4f093c27dd8e9736d24d3b905dd54`。该 exact main 的 Public CI 11/11、Browser Smoke 1/1
  与十一份变更文件匿名 raw-byte readback 均成立。实现只新增 private observation profile/domain、A/B exact
  responsibility、`provider-operands/0.3`、relation-cell `/0.2`、逐 item outcomes、receipts、candidate
  composition/conflict 与 owned qualification result；没有公共 Schema、RelationSet、final Evidence、publisher、
  Slice、Coverage、CLI 或 Workbench。当前状态只能是
  `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTED /
  R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FREEZE_CANDIDATE /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。本文自己的门、合入、exact-main 双门、三次
  fresh anonymous installed-product readback 与后继独立最终状态发布全部成立前不得写成 frozen。
- `docs/179-r1-relation-observation-composition-qualification-freeze-publication.md` 从候选合入基线
  `main@49b7cbc877049377f78f2c845db75ad89ec189a1` 独立发布实现冻结事实。PR #167 原始 Public CI 为
  attempt 1、11/11 SUCCESS；candidate exact main 的 Public CI 为 11/11、Browser Smoke 为 1/1。README、
  文档 178 与 milestones 三次 fresh anonymous installed-product readback 均使用不同 Plan ID、Plan digest、
  collection session 与输出根，P1/P2 coverage COMPLETE、三样本稳定、唯一 marker 与 Core PASS；canonical
  manifest `sha256_json=8017762ce4e975dea0da8f71fa9c8388176d794a73f3c4bc2cdb1934b4798220`。
  README 的 wrapper 在完整 PASS Artifact 落盘后因旧中间文件名后处理退出 1，未重跑；文档 178 首次正式
  session 因 anonymous API quota exhausted 保留 `API ERROR / Render COMPLETE`，quota reset 后使用新 Plan、
  session 与输出根取得 PASS，后继成功不改写首败。最终发布 head
  `1a27ca44b526372637fb0a7a67a54fa0182c446f` 经 PR #168 原始 Public CI 11/11 合入
  `main@672a1c121aa3f2fb4cd89cb211b9acc7569f479f`；该 exact main 的 Public CI run `35592499950`
  attempt 1 为 11/11、Browser Smoke run `35592499949` attempt 1 为 1/1。README、文档 179 与 milestones
  又以三个新 Plan/session/output root 完成 fresh anonymous installed-product readback，联合 manifest
  `sha256_json=6ab7372006e06752edd925b5461f42e0a9c23aefe3c46ce8cea98d36f134b95b`。当前状态是
  `R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步必须从新 exact main 做 system audit；
  RelationSet、公共 Schema、publisher、Slice、Coverage、CLI 与 Workbench 继续未授权。
- `docs/180-o0-operations-evidence-problem-framing.md` 与
  `docs/181-t0-test-evidence-problem-framing.md` 是 R1 当前冻结闭环后独立形成的 docs-only 候选记忆。
  `O = Operations Evidence` 首先只观察运行事实，不自动拥有 deploy/restart/repair 等动作权；
  `T = Test Evidence` 首先只观察 test discovery/execution/report identity，selection、runner、retry 与 fixture
  authority 仍为 `UNKNOWN`。两者均为 `PRECONSTRUCTION_NOTE / NO_IMPLEMENTATION_AUTHORITY`，不改 Core，
  不创建插件、Provider、Schema、runtime、CLI、CI、标签或 Release。工具 coverage 不得与 R observation
  coverage 混用，test pass 不得直接升级为 Core PASS。本支线关闭后，当前串行施工坐标返回 R post-freeze
  system audit。
- `docs/182-r1-post-qualification-relation-set-admission-and-evidence-binding-system-audit.md` 从 exact
  `main@de0fdc6f01e1c99ae74259abd77640ad39d28038` 审计 private qualification 与公共 RelationSet/Evidence/
  Manifest 之间的下一缝隙。双 Python H1/H2/H3 identity matrix 证明：独立合格 attempts 可具有相同
  `relation_set_digest` 与不同 provenance file bytes；合格与缺一个 outcome 的未合格历史又可以保留完全相同的
  raw candidate projection。现有 application 正确拒绝未合格 composition，但未来 assembler 若绕过该状态，
  `RelationSet 0.1` shape 无法独立识别。审计只选择 RelationSet admission / explicit admission witness / public
  qualification binding 作为下一问题面；Evidence 是候选编码位置而不是自动的 admission authority，Manifest
  只绑定文件而不裁决 eligibility；审计本身不冻结 witness 编码、字段、Schema 版本或实现。PR #170 合入
  `main@1ffc4494dbbb61a056dcc8beed2530e7313f6116` 后，exact-main Public CI 11/11、
  Browser Smoke 1/1 与 README/本文/能力地图/milestones 四份 fresh anonymous paired readback 已闭合，状态为
  `R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED`。早先
  `SYSTEM_AUDIT_CANDIDATE` 仍是历史状态，不被后继闭环改写。
- `docs/183-r1-relation-set-admission-and-public-qualification-binding-contract.md` 从上述 exact main 起草下一份
  docs-only 最小合同。它冻结 deterministic application 所有的 admission gate、RelationSet exact membership/
  provenance/conflict closure、explicit admission witness 与 public cross-object binding；RelationSet 0.1 与八文件
  Manifest 0.1 保持不变，候选选择 versioned DerivationEvidence 0.2 只作为 witness carrier，不把 Evidence 或
  Manifest 升格为 admission authority。文档 185 的独立发布链全部成立后，该合同冻结坐标的阶段状态是
  `R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN /
  R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_ALLOWED /
  R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`；只有文档 183 A–F 的 private closed proof 获得
  有限授权，publisher、Slice、Coverage、CLI 与 Workbench 继续未授权。
- `docs/184-m10-descendant-readiness-fixture-observation-correction.md` 保留后继 docs-only PR #171
  original Public CI run `35629971691` 的 Python 3.10 `-O` 正式首败。失败用例只留下
  `readiness.ready == false`，耗时约 `3.045s`、贴合旧正向夹具 `3000ms` budget，但没有保存 terminal、
  attempts 或 bounded streams，因此精确原因保持 `UNKNOWN`。独立 L0 maintenance 只给该无 3 秒 SLO 的
  positive helper 使用 bounded `10s` observation window，在启动 session 后立即注册 cleanup，并在失败时输出
  exact observation/streams；它不改 runtime、默认 readiness、负向测试、cleanup deadline、R1 合同或产品
  timeout。PR #172 original head `d3342175aa5611ff1d2c6cefeb300137ac0696ef` 的 Public CI run
  `35634296113` attempt 1 为 11/11；合入 `main@f4aec949258ed16830b2e8dd828273435498764b` 后，
  exact-main Public CI run `35636414037` attempt 1 为 11/11，Browser Smoke run `35636414038`
  attempt 1 为 1/1。PR #171 原 head 不 rerun，旧失败仍为 `UNKNOWN`；maintenance 已独立资格化，新 head
  `53d4b999...` 的两次同-head 11/11、合入 `main@9299c24...` 后的 exact-main 11/11、Browser Smoke 1/1
  与 fresh public readback 均已成立。
- `docs/185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md` 独立发布
  文档 183 的最小合同。它保留 #171 的 `UNKNOWN` 首败、#172 maintenance、README 匿名 quota 首败、三份
  paired PASS 与能力地图 render-only PASS；architecture DOT/SVG 因无拓扑变化保持字节不变。冻结只授权
  文档 183 A–F，不能扩张到 publisher、公共 Bundle、Slice、Coverage 或 Attention。
- `docs/186-r1-relation-set-admission-and-public-qualification-binding-implementation-freeze-candidate.md` 记录文档
  183 A–F 已由 PR #174 实现并合入 `main@dc580e0a23d0141982f09f7c19bb55d61e9a30d8`。该 exact
  main 的 Public CI 11/11、Browser Smoke 1/1 与十五份实现文件 anonymous exact-SHA source identity readback
  均成立。实现只新增 private admission/witness state、Evidence 0.2 Schema/corpus/identity vectors 与 private
  projection；Evidence assembler 不能从 raw candidates 或 caller witness 反向签发 admission，`CONFLICTING`
  不选择 winner 或生成 Slice/Coverage。PR #175 的原始 11/11、受保护主线合入、exact-main Public CI
  11/11、Browser Smoke 1/1 与 README/本文/milestones 三次 fresh anonymous installed-product readback
  随后全部成立；候选状态仍作为历史坐标保留，不被最终发布改写。
- `docs/187-r1-relation-set-admission-and-public-qualification-binding-freeze-publication.md` 独立发布文档 186 的
  实现冻结事实。冻结对象只包括 private deterministic admission、explicit witness 与 Evidence 0.2 binding；
  RelationSet 不能自报 admission，Evidence 不能生成 admission，Manifest 不能裁决 admission。该发布自己的
  原始远端门、受保护主线合入、新 exact-main 双门与三次 fresh anonymous installed-product readback 全部成立
  后，当前状态才是
  `R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只能先做 post-admission system audit；
  publisher、公共 Bundle、Manifest role 扩张、Slice、Coverage、Attention、CLI 与 Workbench 继续未授权。
- `docs/188-r1-post-admission-review-slice-input-obligation-closure-system-audit.md` 从上述 exact main 完成
  post-admission system audit。双 Python `RS-000/001` 证明现有 Schema/identity/Manifest/stage partition
  checks 既不能把 Coverage completed 与实际 Slice 双向闭合，也不能阻止 producer 连同 Slice 一起缩小
  Policy+FactSet 已机械定义的 anchor/spec denominator；`RS-002` 又证明相同 semantic RelationSet 可来自不同
  attempt/witness，Slice content identity 与 execution eligibility 必须分离。本文最后门全部成立后，当前状态是
  `R1_POST_ADMISSION_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_PRECONTRACT_AUDITED /
  R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。下一步只能从新 exact main 起草 admitted-graph
  input / anchor-spec obligation closure docs-only 合同；不得直接实现 BFS、SliceSet、Coverage、publisher、
  Schema patch、Attention、CLI 或 Workbench。
- `docs/189-r1-review-slice-admitted-graph-input-and-obligation-closure-contract.md` 从新的 exact
  `main@0c2ab31671a89b7c96fb5a44c390c85e7820c8c5` 起草 docs-only 最小合同。它要求 future Slice
  application 同时闭合 exact `DerivationInputSet`、owned qualification history、
  `OwnedRelationSetAdmissionState` 与原 attempt 的 live continuation；raw RelationSet、digest-only、caller
  witness 或 fresh BudgetContext 都没有启动资格。conflict-free exact FactSet/Policy 机械产生完整
  anchor/spec obligation domain，conflict world 保持 UNKNOWN，真正零 anchor 才是 KNOWN closed empty；每个
  obligation 必须 exactly-once 取得允许 outcome，reconciler 只能验账，不能补造 Slice、negative 或 gap。
  文档 190 的独立发布链全部成立后，当前状态是
  `R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_CONTRACT_FROZEN /
  R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_ALLOWED /
  R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。实现授权只覆盖 A–H 的 private closed proof；
  不得扩张到公共 Schema、ReviewSliceSet、CoverageLedger、publisher、Bundle、Attention、CLI 或 Workbench。
- `docs/190-r1-review-slice-input-obligation-closure-contract-freeze-publication.md` 独立发布文档 189 的最小合同。
  它绑定 PR #179、candidate exact-main 双门、三份 fresh anonymous installed-product readback 与 canonical
  manifest，并要求自身再通过远端门、受保护合入、新 exact-main 双门和 fresh readback。冻结只授权 A–H；
  architecture DOT/SVG 因能力拓扑未变而保持字节不变。
- 文档 189 的 private implementation 已严格按序完成 A、B 两段。A 经 PR #181 合入
  `main@dbe1217f9502dc1f2fbb55da73c2e41845b63439`，该 exact main 的 Public CI attempt 1 与 Browser
  Smoke attempt 1 均通过；B 经 PR #182 合入 `main@6b9de57d1009e486d4bb5e392cc6791ee1811304`，PR 原始
  Public CI 11/11、合入后 exact-main Public CI 11/11 与 Browser Smoke 1/1 均在 attempt 1 通过。当前状态为
  `R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_IN_PROGRESS /
  R1_REVIEW_SLICE_INPUT_STAGES_A_B_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_C_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A/B 没有独立冻结 claim；下一步只有在重新读取
  exact-main 停止线且没有新反例推翻问题选择后，才允许进入 C 的 private conflict gate 与 deterministic
  anchor/spec obligation domain。不得把 A/B 的成功扩张为 obligation domain、BFS、ReviewSliceSet、Coverage、
  publisher、Schema、Attention、CLI 或 Workbench 已开始；能力拓扑未变化，architecture DOT/SVG 保持字节不变。
- 从上述 exact main 继续实现的 C 经 PR #184 合入
  `main@9b9e401d03634dc9dd9afc7365c4a2a01b849fc5`；PR 原始 Public CI run `35914018955` 为 11/11
  PASS，合入后的 exact-main Public CI run `35966286794` attempt 1 为 11/11 PASS，Browser Smoke run
  `35966286690` attempt 1 为 1/1 PASS。C 只形成 private Relation conflict gate 与 deterministic exact
  anchor/spec obligation domain；conflict world 没有 normal domain，zero-anchor world 只有已知空 domain，二者
  都没有被升级为 Slice、Coverage 或 closure。当前状态为
  `R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_IN_PROGRESS /
  R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_D_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A/B/C 均没有独立 frozen claim。重新读取该 exact
  main 后，D 仍是下一条最小候选 seam，但任何实现必须由 domain owner 逐项产生 opaque assignment、继续消费原
  live `BudgetContext`，并停在 private deterministic traversal boundary；caller-supplied spec、fresh budget、
  public ReviewSliceSet/CoverageLedger、publisher、Schema、Attention、CLI 与 Workbench 仍未授权。能力拓扑未变，
  architecture DOT/SVG 保持字节不变。
- D 从状态同步后的 `main@eabce147092799b38fab5e54fd2659db4d3f17b8` 建立 private obligation
  assignment 与 deterministic traversal boundary。PR #186 原始 Public CI run `35979172112` attempt 1 为
  11/11 PASS，并以实现 commit `487df99930eed719753627d00af78e7c0fea0b17` 合入
  `main@a876a1d2616c81786571d295ecd4aa4a98828d97`。该 exact main 的 Browser Smoke run
  `35981417298` attempt 1 为 1/1 PASS；Public CI run `35981417295` 则在 Python 3.10 已通过
  Review Attention normal/`-O`、构建与资产上传后触及既有 20 分钟 aggregated job containment，E1
  clean-install 被取消，七条后继门跳过，因此正式保持 `CANCELLED`，不得写成 PASS 或 rerun 洗白。独立 PR
  #187 只把该 outer containment 从 20 调整到 25 分钟，不修改产品 timeout、测试、验收阈值或 D runtime；其
  原始 Public CI run `35983866207` attempt 1 为 11/11 PASS，随后合入
  `main@eacc1995236fde60b8e838fda1cef8865ba3e0b5`。该 maintenance-qualified exact main 的 Public CI
  run `35986138680` attempt 1 为 11/11 PASS，Browser Smoke run `35986138572` attempt 1 为 1/1 PASS。
  当前状态为
  `R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_IMPLEMENTATION_IN_PROGRESS /
  R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_D_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_E_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A–D 均没有独立 frozen claim。D 只允许 domain
  owner 形成 attempt-bound opaque assignments，并按 domain 顺序一次性给出绑定 exact FactSet、RelationSet 与
  Profile traversal rules 的 private boundary；它没有执行 BFS，也没有 outcome、frontier、Slice、closed-empty、
  publisher 或公共 Schema authority。能力拓扑未变，architecture DOT/SVG 保持字节不变；下一步必须重新读取
  exact-main 停止线后再判断 E，不得因 D 已验证而自动开始 COMPLETE/PARTIAL outcome 或后继 F–H。
- E 从上述状态链继续形成 private deterministic BFS、`NORMAL_COMPLETE / NORMAL_PARTIAL` outcome 与
  structural frontier proof，并经 PR #190 合入
  `main@5493007d15b7895fe0dddfd4c7c617424cd15672`；该 exact main 的 Public CI run
  `36031453261` attempt 1 为 11/11 PASS，Browser Smoke run `36031453255` attempt 1 为 1/1 PASS。
  后继 docs-only 状态发布 PR #191 的原始 Public CI run `36034293834` attempt 1 在 Python 3.13 `-O`
  执行 M10 dependency-early-exit 公共 CLI 用例时，只留下测试 identity 与 step exit code 1，没有 terminal
  unittest outcome、traceback 或 summary；该正式失败保持 `FAILURE / UNKNOWN`，PR 不合并、不 rerun。
  `docs/191-m10-public-cli-host-exit-observation-correction.md` 只修正这个 negative test 的观察边界：由外层
  unittest 启动 exact interpreter 的独立 CLI 子进程，保存 return code/stdout/stderr，同时继续验证原 Bundle、
  cleanup 与 port facts。它不修改 Core runtime、M10 生命周期合同、R1 E、Schema 或 publisher，也不声称已
  解释或修复 #191 的未知根因。当前只能记为
  `M10_PUBLIC_CLI_HOST_EXIT_OBSERVATION_CORRECTION_CANDIDATE /
  R1_E_STATUS_PUBLICATION_REQUALIFICATION_BLOCKED /
  R1_REVIEW_SLICE_INPUT_STAGES_F_H_NOT_STARTED`；维护必须独立通过本地适用门、原始 PR 门、受保护合入与新
  exact-main 双门，E 状态发布再从该新 source identity 重建。能力拓扑未变，architecture DOT/SVG 保持字节
  不变，F 不得启动。
- maintenance PR #192 original head `e7c1bd8e2fe60b648074fae90bda83d2e73331ae` 的 Public CI run
  `36038413885` attempt 1 为 11/11 PASS，随后合入
  `main@89a069277c361a55afdd963f2a1e5e75aee9a39a`；该 exact main 的 Public CI run
  `36041811403` attempt 1 为 11/11 PASS，Browser Smoke run `36041811369` attempt 1 为 1/1 PASS。
  因此状态为
  `M10_PUBLIC_CLI_HOST_EXIT_OBSERVATION_CORRECTION_QUALIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_D_E_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_F_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。PR #191 保持 closed/unmerged，其 original
  `FAILURE / UNKNOWN` 没有被维护绿灯覆盖。E 状态发布必须从该 maintenance-qualified exact main 形成新的
  docs-only source identity，并独立通过自身 PR 与合入后 exact-main 门；A–E 均没有独立 frozen claim。
  E 仍只证明逐项 normal traversal outcome 与 structural frontier，可以在同一 live attempt 中形成多个
  assignment/outcome；它不证明整组 missing/duplicate/dangling/cross-attempt reconciliation、zero-anchor
  closed-empty、conflict/upstream-unknown closure 或 `RS-000..016` hardening。公共 ReviewSliceSet、
  CoverageLedger、publisher、Schema、Attention、CLI 与 Workbench 均未授权；能力拓扑未变，architecture
  DOT/SVG 保持字节不变，F 不得因本状态投影自动开始。
- F 从 E 的 owned normal outcomes 继续完成 non-empty domain 的 private reconciliation：逐项拒绝
  missing、duplicate、dangling 与 cross-attempt outcome，按 authoritative assignment/domain order 重排，
  从 owned traversal boundary 重新推导完整 normal candidate，并通过原 live `BudgetContext` 原子提交
  attempt-bound `NORMAL_CLOSED` receipt。实现 commit
  `74211037af08cc5ce6bf2e851b25864203e82dcf` 经 PR #194 original Public CI run
  `36068162572` attempt 1 的 11/11 PASS 后合入
  `main@28e048777341cfa6c9a6d7b546d75a0dc0eb0d33`；该 exact main 的 Public CI run
  `36070066887` attempt 1 为 11/11 PASS，Browser Smoke run `36070066891` attempt 1 为 1/1 PASS。
  因此当前可投影为
  `R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_D_E_F_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_G_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A–F 仍没有独立 frozen claim。F 没有获得
  zero-anchor `CLOSED_EMPTY`、conflict/upstream-unknown negative closure、`RS-000..016` hardening、公共
  ReviewSliceSet/CoverageLedger、publisher、Schema、Attention、CLI 或 Workbench authority。首次本地
  targeted `61/64` 的三处错误均发生在 F runtime 前的 fixture 构造：两处把 two-import producer 配到
  one-import blob，一处使用 Policy 不允许的空 anchor-kind 列表；改为既有 two-import input world 与有效但
  不存在的 `CLASS_DECLARATION` anchor world 后，runtime 不变，最终 A–F 双 Python normal/`-O` 均为
  `64/64`，完整 Review Attention 四格均为 `274/274`。能力拓扑未变，architecture DOT/SVG 保持字节不变；
  G 不得因本状态投影自动开始。
- G 已把两类可达 negative world 留在独立 private identity 中：`QUALIFIED / CONSISTENT` 且 exact
  obligation domain 真正为零时，domain owner 通过 one-shot empty reconciliation claim 与原 live
  `BudgetContext` 原子提交 attempt-bound `CLOSED_EMPTY` closure；已 admission 的 `QUALIFIED /
  CONFLICTING` graph 则只形成 denominator `UNKNOWN`、固定记录 `PROVIDER_CONFLICT /
  UPSTREAM_DENOMINATOR_UNKNOWN` 且没有 normal Slice candidate 的 blocked-input receipt。更早的
  `NOT_QUALIFIED / NOT_COMPOSED` world 仍停在 qualification，不得借 G 进入 Slice。最终实现 commit
  `fc5fd83bd0dac01dd7b04f89b261411eb9287195` 经 PR #196 original Public CI run
  `36090158284` attempt 1 的 11/11 PASS 后合入
  `main@1efba63d720d8faa39cc5ca3f82433c8b0e14d42`；该 exact main 的 Public CI run
  `36091900312` attempt 1 为 11/11 PASS，Browser Smoke run `36091900308` attempt 1 为 1/1 PASS。
  因此当前可投影为
  `R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGE_H_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A–G 仍没有独立 frozen claim。一次中间实现
  曾原位扩张 F 已验证的 private `obligation-closure/0.1` identity；最终 diff review 拒绝该路径，恢复 F
  文件原字节，并为 G 建立两个独立 private identity 后重跑全部门。首次使用仓库 `.venv` 的完整 suite
  尝试因测试环境缺少 `jsonschema` 在 discovery 阶段形成两处 import error，不构成 qualified full-suite
  observation；依赖完整的 Python 3.10/3.13 normal/`-O` 最终字节上，A–G targeted 四格均为 `77/77`，
  完整 Review Attention 四格均为 `287/287`。G 不形成公共 ReviewSliceSet/CoverageLedger、Schema、
  publisher、output root、Attention、CLI 或 Workbench authority。能力拓扑未变，architecture DOT/SVG
  保持字节不变；H 不得因本状态投影自动开始。
- H 已从重新绑定的 exact main 完成 doc189 最后一组 private hardening。真实反例证明 fresh
  `BudgetContext` 即使 limits 与原 attempt 相同，也不能继承 same-attempt authority；两个 private
  continuation 因此保存并复核原始 context 对象身份。H 又直接固化 `RS-008 / 013 / 014 / 015 / 016`，
  保存 normal partial、normal complete、closed empty 与 conflict blocked 四类 private world 的
  cross-runtime identity，并明确 `RS-000/007` 在当前只能证明 private precursor，不得冒充未来公共
  ReviewSliceSet/CoverageLedger 的 cross-object closure。实现 commit
  `195c52ab2790af5cb987f7b10b73bcafe7516685` 经 PR #198 original Public CI run `36114737357`
  attempt 1 的 11/11 PASS 后合入
  `main@59c2ccfc886a92824abea748ae8f9749330adb67`；该 exact main 的 Public CI run
  `36116922092` attempt 1 为 11/11 PASS，Browser Smoke run `36116922116` attempt 1 为 1/1 PASS。
  因此当前可投影为
  `R1_REVIEW_SLICE_INPUT_OBLIGATION_CLOSURE_PRIVATE_IMPLEMENTATION_EXACT_MAIN_VERIFIED /
  R1_REVIEW_SLICE_INPUT_STAGES_A_B_C_D_E_F_G_H_EXACT_MAIN_VERIFIED /
  R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SYSTEM_AUDIT_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。A–H 仍没有独立 frozen claim。首次本地完整
  suite 尝试因选用的 venv 缺少仓库声明的 `schema-test` 能力，在 243 项执行后留下两个
  `jsonschema` import error；这属于 local gate setup failure，不是 H runtime failure，也不是 qualified
  full-suite result。补齐锁定的 `jsonschema==4.25.1` 后，最终同一 source bytes 上 H focused 四格均为
  `8/8`、A–H join 四格均为 `85/85`、完整 Review Attention 四格均为 `295/295`。能力拓扑未变，
  architecture DOT/SVG 保持字节不变；下一步只能先做 post-closure system audit，不能自动开始公共
  ReviewSliceSet、CoverageLedger、Schema、publisher、output root、Attention、CLI 或 Workbench。
- `docs/192-r1-post-slice-input-closure-slice-coverage-qualification-system-audit.md` 已从
  `main@1ca6a4740f13cbb9cb70eb0836dbbabf81c076d0` 完成 A–H 后的 post-closure system audit。实际
  `SCQ-000` 证明两个独立合法 attempts 可共享 Slice candidates、`slice_id` 与 `slice_set_digest`，同时保留
  不同 admission witness、obligation closure digest 与 closure bytes；content identity 不得继承 fulfillment
  authority。`SCQ-001` 又证明与 exact Snapshot 及相邻 stage 矛盾的 CoverageLedger 仍可保持 Schema-valid、
  stage-partition-self-consistent 与 digest-valid。PR #200 original Public CI 11/11 后合入
  `main@042654e8f9467fbaa8e26cf31690b8f878541eda`；该 exact main 的 Browser Smoke attempt 1 成功，
  Public CI attempt 1 却在 Python 3.13 把预注册 Browser business failure world 从预期
  `BROWSER_HARD_FAILURE` 分类成 `COLLECTOR_ERROR`。原 Artifact 只保留公共 stop reason，精确 private
  error type 与根因保持 `UNKNOWN`；五次 Python 3.13 本地诊断均未稳定复现。当前只能投影为
  `R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_AUDIT_MERGED /
  R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_AUDIT_REQUALIFICATION_BLOCKED /
  R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。`docs/193-m10-browser-business-failure-observation-correction.md`
  只把文档 177 已有的 test-only transparent error-type tracing 接到该 business-failure world；不改 runtime、
  timeout、公共 Evidence、Schema、CI 或 R1 审计结论，也不声称修复旧 `UNKNOWN`。维护自身的新 exact-main
  双门与独立状态发布成立前，不得发布 `...PRECONTRACT_AUDITED`，不得起草后继合同或开始 Schema/runtime。
- maintenance PR #201 original head `657f17c5d312fa239e76b55833c13b9ee01ed97a` 的 Public CI run
  `36133008016` attempt 1 为 11/11 PASS，随后合入
  `main@f9a493b73754b198745f6d92055d85516aa0a7cd`；该 exact main 的 Public CI run
  `36135275911` attempt 1 为 11/11 PASS，Browser Smoke run `36135275948` attempt 1 为 1/1 PASS。
  因此测试观察修正已独立资格化，post-closure audit 可以投影为
  `R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_PRECONTRACT_AUDITED /
  R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
  R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`。PR #200 exact-main Public CI run
  `36128804576` 的 `FAILURE / UNKNOWN` 永久保留；后继绿灯不解释或覆盖它。该状态发布必须独立通过自身
  original PR 门、受保护合入与新 exact-main 双门；在最终门闭合前仍不得起草后继合同或开始 Schema、
  Evidence、Manifest、runtime、publisher、output root、公共 Bundle、Attention、CLI 或 Workbench。
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

## R1 Fact / Parse Coverage 前置审计候选

从 `main@0b2df206756bd07ddd5075fa1bd9b63b656a16dc` 起草的
`docs/194-r1-fact-parse-observation-fulfillment-coverage-prerequisite-system-audit.md` 只审计完整七阶段
Coverage 的上游资格。current closed multi-Provider fixture 实际有四个按 entry-kind 与 `.py` raw-path 后缀进入
`supported_paths` 的 candidate parse-unit paths；该 private 字段不证明 encoding/syntax/parse 已完成。两个 required
ProviderRuns 均 `COMPLETED`、overall `COMPLETED`、FactSet 与 normal continuation 均成立，但只报告一个 path
的一个 Fact。该结果符合文档 137/155/160 的 private mechanism-test 边界，不是 runtime defect；它证明
Fact membership/provenance closure 不能替代 parse-unit / Fact observation fulfillment。

当前候选状态为：

```text
R1_POST_SLICE_INPUT_OBLIGATION_CLOSURE_SLICE_COVERAGE_QUALIFICATION_PRECONTRACT_AUDITED
R1_FACT_PARSE_OBSERVATION_FULFILLMENT_COVERAGE_PREREQUISITE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文不推翻 Relation qualification、RelationSet admission 或 ReviewSlice A–H private closure；它只禁止在没有
Fact/Parse observation domain、逐项 terminal outcome 与 same-attempt fulfillment receipt 时，把
`ProviderRun COMPLETED` 或 FactSet members 升格为 `PARSE / FACT_DERIVATION` authoritative Coverage。
候选自己的原始 PR 门、受保护合入和新 exact-main 双门成立以前，公开主线状态不变。即使候选闭合，下一步
也只能从新 exact main 做 Fact/Parse observation fulfillment precontract audit；不得直接开始完整
ReviewSliceSet/Coverage 合同、real parser、Schema、Evidence/Manifest、publisher、Bundle、Attention、CLI 或
Workbench。

## R1 Language Support / Parse / Fact 履责问题边界审计候选

从 `main@a07266661ec66e79b3658c32da69e79494d8ae0e` 起，
`docs/195-r1-language-support-parse-fact-fulfillment-problem-boundary-audit.md` 不预选通用
`ObservationObligation / ObservationReceipt / FulfillmentLedger`，而是先复核 frozen Coverage 三个上游 stage 的
denominator source。`LANGUAGE_SUPPORT` 的责任域来自 exact Policy `IN_SCOPE` inventory；`PARSE` 的责任域依赖
逐项 support classification；`FACT_DERIVATION` 的候选分母只有在 exact parse result / AST 成立后才可按 frozen
Profile projection 枚举。共享 attempt identity 或 terminal vocabulary 不证明三者共享 domain construction、
authority owner 或一个通用 receipt。

本轮实际运行三个单变量 falsifier：`LPF-000` 证明 raw `.py` request candidate 可以不满足 Profile accepted
encoding；`LPF-001` 证明 accepted UTF-8 request candidate 可以在 Python 3.10 grammar 下 parse failed；
`LPF-002` 证明可成功解析且含 MODULE/import/class/method/function 的 exact AST，current closed Provider 仍可只
报告 MODULE。三个世界中 required ProviderRuns 都保持 `COMPLETED`、diagnostics 为空、overall
`COMPLETED`、normal continuation 成立。该结果符合现有 mechanism-test 合同，不是 runtime defect；它只证明
request enumeration、whole-run completion 与 reported Fact composition 分别不能替代对应的逐项履责事实。
首次并发复跑因仓库外脚本在三个 world 全部结束后才读取首 world 的 live continuation，形成越过 10 秒
budget 的非一致 projection；该 audit-harness timing failure 不计作合格结果。把 projection 移到每个 world
自己的运行终点后，并发四格 canonical report 才逐字节一致；产品 runtime 与预算没有修改。

当前候选状态为：

```text
R1_FACT_PARSE_OBSERVATION_FULFILLMENT_COVERAGE_PREREQUISITE_AUDIT_CANDIDATE
R1_LANGUAGE_PARSE_FACT_FULFILLMENT_PROBLEM_BOUNDARY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文不推翻文档 192 对 private Slice closure 的既有 claim，也不发布 Fact/Parse precontract、真实 parser、AST
carrier、Fact projection runtime、公共 ReviewSliceSet/CoverageLedger、Schema、Evidence、publisher 或 Bundle。
候选自己的原始 PR 门、受保护合入与新 exact-main 双门成立前，公开主线状态不变；即使候选闭合，下一步也只
能从新 exact main 选择并审计最小 contract problem，不能直接实现统一 Ledger 或完整七阶段 Coverage。

## R1 Language Support Qualification Authority 问题审计候选

从 `main@2ce608ce80a39a3bbd3dd15bdab60d3940a1c21d` 起，
`docs/196-r1-language-support-qualification-authority-problem-audit.md` 只审计 `LANGUAGE_SUPPORT`。责任域由 exact
SourceSnapshot terminal inventory 与 sealed Policy `IN_SCOPE` decisions 机械 join；Snapshot 提供 path/kind/content
identity，Policy 提供 scope/source class，Profile 提供 Python 3.10、entry-kind、path 与 accepted-encoding 规则。
Provider 不拥有 denominator 或 classification authority；total function 一旦冻结，deterministic application 可以
执行规则，但不能自行扩张规则。

本轮实际运行 UTF-8、UTF-8-SIG、合法 Latin-1 declaration、invalid UTF-8、Policy `IN_SCOPE + UNCLASSIFIED` 与
`OUT_OF_SCOPE` 六个 exact-input world。前五个 world 都有 7 个 `IN_SCOPE` entries、4 个 current request
candidates、两个 required `COMPLETED` ProviderRuns、零 diagnostics、overall `COMPLETED` 与 terminal-point normal
continuation；current carrier 均没有逐项
Language Support terminal classification。Python 3.10/3.13 normal/`-O` 四格 canonical report 逐字节相同，SHA-256
为 `168401b563292ab157db02b648787657b7cdc4788c07636d8ba5a9a0e0999498`。`OUT_OF_SCOPE` control 的
`regular.py` 仍在 `supported_paths`，但不属于 denominator。

当前候选状态为：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_AUTHORITY_PROBLEM_AUDIT_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该候选不选择 terminal enum、receipt、共同 carrier、Schema 或 runtime，也不预判 derived qualification 是否必须
持久化。live DerivationInputSet copy-own verified blob bodies，但 public SourceSnapshot 只保存 content identity；
same-attempt 可重算不等于 public/offline 可复核。现有 frozen materials 尚未把 coding-declaration detection、
多条件 reason composition、reason 的 stage ownership、canonical classification identity 与 same-attempt continuation
写成 total contract。候选 original PR 门、受保护合入与新 exact-main 双门成立以前，
公开主线状态不变；闭合后下一步也只能做 Language Support precontract audit，不能开始 Parse、Fact、
ReviewSliceSet、CoverageLedger、publisher 或 Bundle。

## R1 Language Support Qualification 最小合同前置审计候选

从 `main@26b235cda3ba220e7de222a8e8ab8d2effedb5f4` 起，
`docs/197-r1-language-support-qualification-precontract-audit.md` 只收敛下一份 Language Support 合同必须冻结的
semantic input identity、Python 3.10 encoding qualification、predicate applicability、complete reason composition、
stage ownership、exactly-one proof 与 Parse consumer boundary。path-only `PARSE_UNIT` ref 只能在 broader-bound
Ledger 内定位成员；它不能脱离 exact inventory bytes、matching Policy decision、Profile 与 versioned function
identity 独立承担 classification identity。

仓库外 audit-only oracle 区分 encoding detection 与 whole-source decode，并覆盖 default UTF-8、cookie/alias、BOM、
explicit ASCII、Latin-1、unknown codec、BOM/cookie conflict、invalid body 与第二行 cookie 边界。current Schema
同时接受 complete multi-reason、first-only reason 与 `UNSUPPORTED_SYNTAX_VERSION` 的 Language Support/Parse 两种
placement，因此 Schema 不能替合同定义 totality 或 stage authority。Python 3.10/3.13 normal/`-O` 四格 canonical
report 逐字节相同：

```text
sha256 = 5666fcda8e61e16664cc46f01e12778499c56b8d56f4638e32dd08e3acc6615c
bytes  = 4404
```

当前候选状态为：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_AUTHORITY_PROBLEM_AUDIT_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDIT_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一合同必须让每个 exact denominator member 恰好形成 `eligible` 或带完整适用失败理由的 `unsupported`，并固定
`POLICY_EXCLUDED -> POLICY_SCOPE`、四个 support reason -> `LANGUAGE_SUPPORT`、
`UNSUPPORTED_SYNTAX_VERSION/PARSE_ERROR -> PARSE`。semantic classification 可以在相同 exact inputs 下复算，
不能继承另一 attempt 的 live continuation。persistence route 继续保持 OPEN；本候选不修改 runtime、tests、
fixture、Schema、Profile、Policy 或 corpus，也不授权 shared receipt、classifier、Parse、Fact、ReviewSliceSet、
CoverageLedger、Evidence、publisher 或 Bundle。其 original PR 门、受保护合入与新 exact-main 双门闭合后，下一步
也只能从新 exact main 起草 Language Support 最小合同。

## R1 Language Support Qualification 最小合同候选

PR #206 的 docs-only semantic candidate 在 Python 3.10 Review Attention 门正式失败；失败发生在 nested test
support 重复 acquisition 同一个 fact-only exact input world，最终由 frozen 30 秒 SourceSnapshot budget 正确
fail closed。该失败没有击穿 Language Support 语义，但候选资格不成立。独立 PR #207 只让测试进程复用
copy-owned、immutable、attempt-neutral `DerivationInputSet`，不共享 `BudgetContext`、ProviderRun、qualification、
admission、continuation 或 terminal receipt，也不放宽产品预算；其 merge
`main@36c82c9c5445b83c33e714c1288d79d27e1fe2bb` 的 Public CI 11/11 与 Browser Smoke 1/1 均在 attempt 1
成立。相同语义 patch 随后以新 source identity 重建为 PR #208，original Public CI 11/11、受保护合入
`main@de4eee7e953a0b95d52b973bee35a033e3901254`、exact-main Public CI 11/11 与 Browser Smoke 1/1 均成立。
PR #206 的失败、PR #207 maintenance 与 PR #208 qualification 必须继续保持独立历史。

从该 exact main 起，[文档 198](docs/198-r1-language-support-qualification-contract.md)只冻结 Language Support
0.1 的 semantic contract：

```text
exact IN_SCOPE inventory world
  + relevant sealed Policy semantics
  + relevant frozen Profile support semantics
  + r1-python-language-support/0.1
    -> all applicable predicates
    -> complete canonical failed-reason set
    -> exactly one eligible / unsupported disposition
```

contract identity 只绑定 exact inventory item、matching `IN_SCOPE` decision、相关 Profile support semantics 与
versioned function；whole `policy_digest` / `analysis_scope_digest` 继续作为历史闭包坐标，不能把 governance、budget、
Provider requirements 或 module mapping 的无关变化塞进 Language Support semantic content。Python 3.10 encoding
qualification 必须依次完成 BOM/前两行 declaration detection、版本化 codec normalization/lookup、BOM/cookie
consistency、whole-source decode 与 Profile accepted-set membership；宿主 Python、locale、ambient codec registry
和 Provider tolerance 没有规则 authority。

所有 applicable 且失败的 reasons 必须按固定 rank
`UNCLASSIFIED_SOURCE / UNSUPPORTED_ENTRY_KIND / UNSUPPORTED_LANGUAGE /
UNSUPPORTED_SOURCE_ENCODING` 完整保存；first-failure 或执行顺序不得改变结果。encoding predicate 只在 entry-kind
和 language/path predicate 通过时适用。`POLICY_EXCLUDED` 属于 `POLICY_SCOPE`；
`UNSUPPORTED_SYNTAX_VERSION / PARSE_ERROR` 只属于 `PARSE`，Language Support 不得运行 parser 或解释 AST。
每个 denominator member 必须恰好进入 eligible 或 unsupported；input/integrity failure 使整个 qualification 不成立，
不得伪装成 per-item unsupported。

候选形成阶段状态为：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

semantic classification 可以在相同 exact inputs 与 function 下复算，但不继承 attempt、`BudgetContext`、deadline、
resource ownership 或 Parse continuation。persistence 明确保留为 non-decision：live recomputation 与 canonical
derived projection 均未被选择。本文不修改 runtime、tests、fixture、Schema、Profile、Policy、corpus 或 identity
vector，也不授权 classifier、carrier、Parse、Fact、shared receipt、ReviewSliceSet、CoverageLedger、Evidence、
publisher 或 Bundle。候选 original PR、受保护合入、candidate exact-main 双门与 fresh public readback 成立后，
仍须独立 freeze publication 自己完成同等级最后门；在 publication 闭合以前不得把合同写成 frozen 或开始代码。

## R1 Language Support Qualification 合同冻结发布

[文档 199](docs/199-r1-language-support-qualification-contract-freeze-publication.md)只发布文档 198 的语义合同，不修改 classification 规则。
PR #209 original Public CI run `36195619550` attempt 1 11/11 成立后，候选合入
`main@78014cd32cf539c3141ae066f6a7c40c0ac707ab`；该 exact main 的 Public CI `36197451442`
attempt 1 11/11 与 Browser Smoke `36197451327` attempt 1 1/1 均成立。

首次 README 正式读回的 P1 为 `ERROR / HTTP 403 / anonymous remaining=0`，P2 为 `COMPLETE`；
它没有 handoff 或 Core report，不能写成 Core FAIL 或合同 FAIL。该 session 与原字节永久保留。
三个后继 fresh installed-product observations 分别独立 PASS，不能倒写成读回从无失败；诊断与 raw-source
byte equality 不替代产品资格路径。联合 verifier 已重新调用安装产品 Core 核账，并将原 ERROR 纳入 manifest。

本发布 original PR 门、受保护合入、new exact-main 双门与 fresh readback 自己全部成立后，当前目标状态才是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

最后门以前，最后合格事实仍是合同候选；不得因 marker 已写入而提前授予实现权。冻结以后也只允许从新
exact main 重读文档 198 第 13 节，做独立 minimal private implementation audit；本文不先授予 classifier、
carrier 或 runtime implementation authority。persistence 继续 OPEN；Parse、Fact、shared receipt、ReviewSliceSet、
Coverage、Schema、Evidence、publisher 与 Bundle 均未获得施工权。architecture DOT/SVG 不因状态发布重画。

## R1 Language Support Qualification private implementation 可行性审计候选

从 `main@791fb093e19165808243258abdad4a1e208dcb70` 起，
[文档 200](docs/200-r1-language-support-private-implementation-feasibility-audit.md)重新读取文档 198 第 13 节。
`DerivationInputSet` 已提供 copy-owned exact world；private denominator、complete reason composition、exactly-one
closure 与 same-attempt claim 都有既有结构可以承载，但这些 structural facts 不自动授予实现权。

审计以 `windows-31j` concrete world 证明 ambient host codec registry 会漂移：CPython 3.10.6 将其拒为 unknown
encoding，Python 3.13.13 则通过 `cp932` alias detection 与 strict decode。冻结 0.1 应取 3.10.6 结果；直接调用 host
`tokenize.detect_encoding / codecs.lookup` 没有 rule authority。

100,000 个固定 byte worlds 的 audit-only reducer 在 Python 3.10/3.13 normal/`-O` 四格取得同一 terminal report：

```text
sha256 = e96dc9dadb2afd896439d103788a541dece8cfbac2fcacde45a8b6c70769cf0d
mismatch_count = 0
```

但 reducer 对 Profile non-accepted codec 在 whole-source decode 前直接返回 unsupported；它只证明 coarse terminal
projection 相同，明确没有实现文档 198 §5.2 的 frozen algorithm。另一个 101 codecs × 2,000 samples 的 3.10/3.13
probe 未发现 decoder 差异，也只是 finite witness，不是 total per-input equivalence proof。

进一步枚举 CPython 3.10.6 `encodings` ordinary modules 得到 120 个 lookupable names，其中 24 个 C-backed
multibyte decoders、7 个 non-text codecs 与 1 个依赖 Windows ANSI code page 的 `mbcs`。该 universe 是有限的，
不能写成“无限 codec 世界”；但它已经超出当前最小 private classifier 的既有 authority surface。审计不宣称 0.1
绝对不可实现，只确认当前 §13 minimal boundary 下不能直接实现完整 0.1 classifier。

因此当前候选 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在候选 original PR、受保护合入与 new exact-main Public CI / Browser Smoke 全部成立后生效。下一步
只能从新的 exact main 审计最小 codec-conformance / pipeline-order correction：保留 0.1 原顺序需要 version-bound
decoder semantics 或同强度 per-input equivalence；把 Profile membership 提到 non-accepted whole-source decode 以前则
必须发布新 function identity。两条路线均未由本文选择或授权。

禁止在本候选中修改合同 0.1、实现 classifier/carrier、选择 persistence、运行 real parser/AST/Fact、修改 public
Schema/corpus、创建 shared receipt、启动 ReviewSliceSet/Coverage 或改变 Evidence/publisher/Bundle。未来即使
classification 成立，Parse operation request 也必须落实 `available input != authorized input`，不能把 unsupported
blob bytes 全部交给 Provider 后只过滤输出。

从 `main@943300a4d6b3d708be8f4196cc0ee67a86eee64b` 起，
[文档 201](docs/201-r1-language-support-codec-conformance-correction-precontract-audit.md)重新审计文档 200 留下的
codec-conformance / pipeline-order seam。文档 200 的 PR #212 original Public CI、受保护合入、exact-main
Public CI `36243585555` attempt 1 11/11 与 Browser Smoke `36243585552` attempt 1 1/1 均已成立。

审计把 `0.1` terminal semantics 按 detection failure、BOM conflict、non-accepted encoding 与 accepted UTF-8
四类世界分解。当前 frozen Profile 只接受 `UTF-8 / UTF-8-SIG`；non-accepted whole-source decoder 的成功、失败
与 decoded text 均不改变 terminal disposition 或 canonical reason，因此完整 3.10 decoder substrate 不是当前最小
authority surface。后继选择显式 function version bump，不静默修改已冻结的 `0.1`。

第一次 136,228-world harness 因 raw regex 多转义一层产生 20,270 mismatches，保留为
`INVALID_AUDIT_HARNESS`。修正后又以 `utf.8` 打出 10 个真实 resolver mismatches：CPython 只对 alias table 做
dotted fallback，不能借此直接导入 canonical `utf_8` module。修正 lookup 顺序后，3.10/3.13 normal/`-O` 四格
得到同一 report：

```text
sha256 = 03b540bcbf2cccd2f2d43f6b8287e2821168337503405d09abf7a0935a8cdc03
worlds = 136228
reference_mismatch_count = 0
```

该 corpus 只作 witness；Route B 的资格来自四类世界的全称 case partition 与显式 version bump。当前候选 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在本候选 original PR、受保护合入与 new exact-main Public CI / Browser Smoke 成立后生效。随后最多
从新的 exact main 起草 `r1-python-language-support/0.2` correction contract candidate；不得修改 0.1 历史字节、
直接实现 classifier/carrier、选择 persistence、运行 Parse/Fact、修改 public Schema/corpus、创建 shared receipt、
启动 ReviewSliceSet/Coverage 或改变 Evidence/publisher/Bundle。

## R1 Language Support Qualification codec-conformance 修正合同 0.2 候选

从 `main@41bd7cd3d6d486c780aeda91b86ae8845ef90ae7` 起，
[文档 202](docs/202-r1-language-support-codec-conformance-correction-contract.md)只起草
`r1-python-language-support/0.2` 的最小语义修正。前态 PR #213 original Public CI `36245636110`
attempt 1 11/11、受保护合入、exact-main Public CI `36246765819` attempt 1 11/11 与 Browser Smoke
`36246765806` attempt 1 1/1 均已成立，因此文档 201 的 precontract audited target 已生效。

0.1 继续绑定 frozen historical bytes 与 `r1-python-language-support/0.1` identity。0.2 只在 exact Profile
compatibility 为 `PYTHON / PYTHON_3_10 / {UTF-8, UTF-8-SIG}` 时适用，并以新 function identity 冻结：

```text
Python 3.10 cookie/BOM placement
versioned accepted UTF-8 closed resolver
BOM conflict by _get_normal_name result
non-accepted early rejection without ambient lookup/decoder
strict whole-source UTF-8 / UTF-8-SIG decode for possibly eligible inputs
```

它继承 0.1 的 denominator、complete reason composition、exactly-one closure、stage ownership、
semantic-result / live-authority separation 与 eligible-only Parse boundary。terminal projection equality 不等于
contract identity equality；0.1 与 0.2 不能互相继承历史 qualification 或 attempt authority。

候选形成阶段的条件化 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在最终字节通过 docs/link/boundary gates、original PR required checks、受保护合入、new exact-main
Public CI / Browser Smoke 与 fresh installed-product public readback 后生效。随后仍须独立 docs-only freeze publication
完成自己的同等级门禁与 readback，才能发布 `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN`。

本文不实现 classifier/carrier/request projection，不选择 persistence，不运行 Parse/Fact，不修改 public Schema/corpus/
identity vector，不创建 shared receipt/ledger，不启动 ReviewSliceSet/Coverage，也不改变 Evidence/Manifest/publisher/Bundle。

## R1 Language Support Qualification codec-conformance 修正合同 0.2 冻结发布

PR #214 的最终 head `10f4a6e22afa8931b29cec79134216521861cd80` 已经以 original Public CI
`36248704418` attempt 1 11/11 合入 `main@936e6037deef899da9403988bb86f5fc8f6ddc10`；该 exact main 的
Public CI `36249925950` attempt 1 11/11 与 Browser Smoke `36249925954` attempt 1 1/1 均成立。README、文档 202
与 milestones 的三个 fresh anonymous installed-product observations 使用独立 Plan/session/output，P1/P2 均
`COMPLETE`、Core 均 `PASS`；联合 verifier 与四份 exact-SHA source-byte 核账也为 `PASS`。因此
`R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_CANDIDATE` 已成为 qualified history。

[文档 203](docs/203-r1-language-support-codec-conformance-contract-0-2-freeze-publication.md)只发布
`r1-python-language-support/0.2`：0.1 historical identity 与文档 198 bytes 不变；0.2 冻结 exact Profile
compatibility、accepted UTF-8 closed resolver、BOM consistency、non-accepted early rejection 与 strict accepted-source
decode，并继承 0.1 的 denominator、reason composition、exactly-one closure、stage ownership 与 attempt-authority
分离。persistence 继续 OPEN。

本发布的条件化 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CODEC_CONFORMANCE_CORRECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 203 最终字节通过 docs/link/boundary gates、original PR required checks、受保护合入、new
exact-main Public CI / Browser Smoke，以及 README、文档 202、文档 203 与 milestones 的 fresh installed-product
public readback 和 independent byte/state reconciliation 后生效。此轮不实现 classifier/carrier，不选择 persistence，
不运行 Parse/Fact，不修改 public Schema/corpus，不创建 shared receipt，也不启动 ReviewSliceSet/Coverage。最后门
闭合后必须先回到 CONTROL LOOP，重新审计 minimal private implementation 是否仍是最小合法问题。

## R1 Language Support Qualification private classifier 实现授权审计候选

文档 203 经 PR #215 final head `969648a04a2d885725faba7f2c10273cdda4cbca` 合入
`main@fa74ae22872691eebf2fe8bdb2209da34b64b56e`。PR Public CI `36252309763` attempt 1 11/11、
exact-main Public CI `36253391449` attempt 1 11/11 与 Browser Smoke `36253391478` attempt 1 1/1 均成立。
README、文档 202、文档 203 与 milestones 四份 fresh installed-product observations 均为 P1/P2 `COMPLETE`
和 Core `PASS`；五份 anonymous raw source bytes 与 exact Git blobs 一致，最终 reconciliation manifest 为：

```text
sha256_json  = 4783ae6c0ef3da1abb9a0d2e8cd18038a29c83360dca96c579fee817eb103c9a
sha256_bytes = 7bc122c5f699331be91eab30f6fd041be503cb11126aedc6e72354b13c97074e
```

因此 `R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN` 已生效。首次准备脚本 assertion failure、
Playwright executable-path diagnostic 的 pending-task warning 与非 Git root `gh` 调用形成的空 setup files 继续
保留原身份；它们没有启动或替代四份正式 readback。

[文档 204](docs/204-r1-language-support-private-classifier-implementation-authorization-audit.md)重新执行 CONTROL LOOP，
只把当前最小施工面限定为 private deterministic classifier：exact input/history revalidation、0.2 compatibility 与
closed UTF-8 resolver、完整 canonical reason composition、exactly-one denominator closure 和 immutable private
semantic result。`DerivationInputSet` 可以 copy-own exact semantic world，但 dataclass/type/digest 本身不是
qualification；实现仍须重新验证 canonical Snapshot/Policy/Profile bytes、cross-artifact binding 与全部 Git object
bytes/size/SHA-256。

当前 execution-cell 0.1 request 会携带 Snapshot 中全部 blob bodies，且 immutable request frame 在最终 cell
admission 前已经构造；所以 classifier 成立不等于 eligible-only Parse operation projection 或 same-attempt
continuation 已成立。文档 204 不授权修改 `_execution_cell*`、request/protocol、Provider input、Parse/AST/Fact、
persistence Route A/B、public Schema/carrier、shared receipt、ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。

本 docs-only 候选的条件化 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTATION_ALLOWED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 204 最终字节通过本层 local gates、original PR checks、受保护合入、new exact-main Public CI /
Browser Smoke，以及 README、文档 204 与 milestones fresh installed-product readback 和 independent reconciliation
以后生效。生效以前不得提前创建 implementation branch；生效以后也只允许实现 private classifier，完成自己的
资格链后必须返回 CONTROL LOOP，另行审计 Parse gate，而不是按文档编号自动施工。

## R1 Language Support Qualification private classifier 实现冻结候选

文档 204 的授权状态已经完成自己的最后门。private classifier 随后从 exact
`main@ad52dbbd361872b2d8de1fbb35d5be152d4e03f1` 建立，只新增 `_language_support.py`、
`_language_support_values.py` 与 `test_language_support.py`。实现 head
`dac2892a173844c4cb288e6381895577e0b46f33` 经 PR #217 original Public CI
`36263694668` attempt 1 的 11/11 SUCCESS 后合入
`main@c3f8a0762e5fecfeb3ed7b6d492d67773a44ab84`；candidate 与 merge tree 均为
`c75855d78ea00d061bac1234533dd536c9e44c33`。该 exact main 的 Public CI
`36264888477` attempt 1 为 11/11 SUCCESS，Browser Smoke `36264888553` attempt 1 为 1/1 SUCCESS。

实现重新验证 canonical Snapshot/Policy/Profile bytes、cross-artifact binding 与全部 exact Git object bytes/size/
SHA-256，再按 `r1-python-language-support/0.2` 形成 complete reason composition、eligible/unsupported exactly-one
closure 与 immutable private semantic result。它不携带 attempt、BudgetContext、continuation、ProviderRun、
admission 或 disposition authority，顶层 package 也没有新增 export。

targeted tests 在 CPython 3.10.6/3.13.13 normal/`-O` 四格均为 20/20，full Review Attention 四格均为
316/316；五个 canonical worlds 逐字节一致。三个 exact-SHA implementation files 的 fresh anonymous raw readback
均为 HTTP 200、无重定向且等于 Git blobs；仓库外 manifest SHA-256 为
`daa0d098b2b3024e5f93945a020704009ac92d8715b8bea38db8d63a2aefb404`。

[文档 205](docs/205-r1-language-support-private-classifier-implementation-freeze-candidate.md)据此只条件化发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_IMPLEMENTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FREEZE_CANDIDATE
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 205 的 docs/link/boundary gates、original PR checks、受保护合入、new exact-main Public CI /
Browser Smoke，以及 README、文档 205 与 milestones 的 fresh anonymous installed-product readback 后生效。随后仍须
独立最终冻结发布完成自己的同等级门禁，才能写成 private classifier `FROZEN`。Parse operation projection、
same-attempt continuation、execution-cell request/protocol correction、Provider filtering、persistence Route A/B、public
carrier/Schema、real parser/AST/Fact、shared receipt、ReviewSliceSet/Coverage、Evidence、publisher 与 Bundle 均未获授权。

## R1 Language Support Qualification private classifier 实现冻结发布

文档 205 的候选随后以 [PR #218](https://github.com/NoctilumeDev/VeriTrail/pull/218) 完成自己的 original
Public CI `36268364383` attempt 1 11/11 SUCCESS，并以 ordinary merge commit
`f79d6d1d470f36b553874492bdd35b53a1b042dd` 合入受保护 main；candidate 与 merge tree 均为
`83d3c74784cf6bc29ee97de478b140477c84e889`。该 exact main 的 Public CI `36269612657` attempt 1 为
11/11 SUCCESS，Browser Smoke `36269612652` attempt 1 为 1/1 SUCCESS。

README、文档 205 与 milestones 三份 fresh anonymous installed-product observations 使用互不复用的 sealed Plan、
session 与 output，均为 P1/P2 `COMPLETE`、三样本稳定、唯一 marker、零 error/conflict/coverage reason/cleanup
error/active stream，Core 为 `PASS`。AGENTS、README、文档 205 与 milestones 的 anonymous raw bytes 又逐字节等于
exact Git blobs。最终 reconciliation manifest 为：

```text
sha256_json  = 2bc041af39faefdf3872397b72f3d18ede5e1364ee4cfc9f92c8a4e10e233384
sha256_bytes = b1bdbb3b79a01b42dee69fe281f87e635b982e9c60254a81100ccdc4e5551a54
```

[文档 206](docs/206-r1-language-support-private-classifier-implementation-freeze-publication.md)据此只条件化发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 206 最终字节完成 local gates、original PR checks、受保护合入、new exact-main Public CI /
Browser Smoke，以及 README、文档 206 与 milestones 的 fresh anonymous installed-product readback 和 independent
reconciliation 后生效。随后必须返回 CONTROL LOOP，重新审计 eligible-only operation projection 与 same-attempt
Parse gate 是否仍是最小合法问题；不得自动开始 Parse。persistence、public carrier/Schema、Fact、Coverage、Evidence、
publisher 与 Bundle 继续未获授权。

## R1 Language Support eligible-only operation projection / same-attempt gate 前合同审计候选

文档 206 的最后门已经闭合，`R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN` 在
`main@476fa8c1740e96be80e068265a9af210f860f420` 成为当前事实。重新执行 CONTROL LOOP 后，
[文档 207](docs/207-r1-language-support-eligible-operation-projection-precontract-audit.md)确认当前最小 seam 不是运行
真实 parser，而是先限制 Provider 可以收到哪些 source bodies，并把该 projection 绑定到原 live attempt。

current Fact execution cell、Relation derivation cell 与 Relation observation cell 都会把 Snapshot 中全部 BLOB bytes
写入 request 或 Provider copy。六个 concrete worlds 在 CPython 3.10.6/3.13.13 normal/`-O` 四格严格串行后形成
逐字节相同的 3072-byte canonical report，SHA-256 为
`fec549e3181d02c0ef200c0d3ddc91ebec5d32866519ea0de6f6b9e3d2737ca0`。mixed world 中，
private classifier 只允许 `pkg/z_good.py`，旧 cell 仍在 rejected `pkg/a_bad.py` 上完成 Fact；该 Fact 又能进入
FactSet，且 normal continuation 仍被允许。这不倒填旧 runtime defect，只证明 terminal/FactSet reconciliation 不能
补做 upstream input authority。

original `BudgetContext`、不可逆 `AttemptEligibility` 与 one-shot prepared request 提供 same-attempt substrate；
classification value、path set、digest、boolean 或 limits 相同的新 context 都不拥有 continuation authority。与此同时，
frozen `veritrail-review-derivation-cell/0.1`、`veritrail-review-relation-cell/0.1` 与
`veritrail-review-relation-cell/0.2` 都要求全量 source-blob continuity，不能在原 identity 下静默改变 cardinality。

本 docs-only 候选只条件化发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 207 的最终字节通过 local docs/Schema/static gates、original PR required checks、受保护合入、
new exact-main Public CI / Browser Smoke，以及 README、文档 207 与 milestones 的 fresh anonymous
installed-product readback 和 independent reconciliation 后生效。生效后最多从新的 exact main 起草 docs-only 最小
合同；不得提前修改 request/protocol/runtime、运行 Parse/Fact、选择 persistence、创建 public carrier/Schema 或 shared
receipt，也不得启动 ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。

## R1 Language Support eligible operation projection / same-attempt gate 合同候选

文档 207 的 source qualification 已由 PR #220 original Public CI `36277119012` attempt 1 的 11/11 SUCCESS、
ordinary merge `main@940b6fc9ad974c4e4afb4f6f3e2f635efe780e1c`、exact-main Public CI
`36278154174` attempt 1 11/11、Browser Smoke `36278154195` attempt 1 1/1，以及 README、文档 207、
milestones 三份 fresh anonymous installed-product readback 闭合。四份 public raw bytes 与 exact Git blobs 一致；
independent reconciliation manifest 为：

```text
sha256_json  = 12e7bf7555c9d088163bb9499435d54aee9d5829cba306d0551f0e703718cf85
sha256_bytes = ea13418d60d2818a9c52b67110e9276e10b28628d141de0a7f7e5d61b4647f5f
```

因此 `PRECONTRACT_AUDITED` 已成为当前事实。重新执行 CONTROL LOOP 后没有出现推翻问题选择的新反例；
[文档 208](docs/208-r1-language-support-eligible-operation-projection-contract.md)只冻结 private source-body input authority：

- `r1-python-language-support/0.2` 拥有 exact eligible subject upper bound；
- application 从 FactSet/domain/assignment 机械建立每个 child 的 exact operation subject set；
- Provider-visible source bodies 必须与 operation set 恰好相等，不能只证明是 eligible subset；
- classification/projection semantic equality 不继承 original `BudgetContext`、parent/child `AttemptEligibility` 或
  one-shot request claim；
- Fact、Relation derivation、Relation observation 分别使用新 versioned wire 与 operands identities，旧
  `0.1/0.1/0.2` wire 及 `0.1/0.2/0.3` operands 继续只读；
- empty projection 按既有 applicable-child contracts 真实运行 empty-body child，但不升级成 Parse/Fact/Coverage
  fulfillment。

本文当前只条件化发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_CANDIDATE
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 208 final bytes、local docs/Schema/static gates、original PR checks、受保护合入、new exact-main
Public CI / Browser Smoke，以及 README、文档 208 与 milestones 的 fresh anonymous installed-product readback 和
independent reconciliation 后生效；随后仍须独立 docs-only freeze publication 完成同等级最后门，才可能授予
文档 208 A–G 的 private implementation。当前不得修改 runtime/protocol、选择 persistence、运行 Parse/Fact、创建
public carrier/Schema/shared receipt、ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。

## R1 Language Support eligible operation projection / same-attempt gate 合同冻结发布

文档 208 候选已完成自己的资格链：PR #221 head
`63e05d4b8d2715d91d78c1cf2487449c5e70b142` 的 original Public CI `36280563559` attempt 1 为
11/11 SUCCESS；ordinary merge `main@f4d531bd49de330bd7a186633699262997e949f4` 的 tree 为
`74726f76aa0952af65c656de7441bab8c95296c4`，exact-main Public CI `36281621834` attempt 1 为
11/11 SUCCESS，Browser Smoke `36281621765` attempt 1 为 1/1 SUCCESS。

README、文档 208 与 milestones 三份 fresh anonymous installed-product observations 使用互不复用的 sealed
Plan/session/output，P1/P2 均 `COMPLETE`、三样本稳定、marker 恰好一次、Core `PASS`。AGENTS、README、
文档 208 与 milestones 四份 anonymous raw bytes 等于 exact Git blobs；independent reconciliation manifest 为：

```text
sha256_json  = dfa90985976a28e9b5f821b49d80ee2ab1bafa98f0e2db726b302ed94b19bf4e
sha256_bytes = de204fc9df0d53e49d0c91c42f646e86a79fb395617c3ba6cec69d2cac8b5b32
```

候选 readback 前置阶段保留两次 exact-User-Agent anonymous API 403、后 reset PASS 及 Playwright shutdown
warning；正式 observations 没有复用这些 diagnostics。独立 reconciliation 首次又因 CI JSON 漏
`databaseId` 在 Core 复算前停止，一次 PowerShell metadata correction command 随后在解析阶段失败；后继只补齐
相同 immutable run metadata 并重新启动 reconciliation，没有重跑正式 observations。后继 PASS 不抹掉这些记录。

[文档 209](docs/209-r1-language-support-eligible-operation-projection-contract-freeze-publication.md)只发布 doc208 已有
input-authority 合同；不新增 classifier、Parse、Fact 或 Coverage 语义。本发布的条件化 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_ALLOWED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 209 final bytes、local docs/Schema/static gates、original PR checks、受保护合入、new
exact-main Public CI / Browser Smoke，以及 README、文档 208、文档 209、milestones 的 fresh installed-product
readback 和 independent reconciliation 后生效。此前当前事实仍是 `CONTRACT_CANDIDATE /
IMPLEMENTATION_NOT_AUTHORIZED`。生效后也必须先回到 CONTROL LOOP；`IMPLEMENTATION_ALLOWED` 只覆盖 doc208
第 14 节 A–G，不选择 persistence，不授权 real parser/AST、Parse/Fact fulfillment、public carrier/Schema、shared
receipt/ledger、ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。

## R1 Language Support eligible operation projection / same-attempt gate 实现冻结候选

文档 209 的最后门闭合后，CONTROL LOOP 重新确认文档 208 A–G 仍是最小合法施工面。A–G 已通过七个独立 PR
#223–#229 串行合入；每个 PR 的 original Public CI 都是 attempt 1、11/11 SUCCESS，每个 merge coordinate 的
Public CI / Browser Smoke 也都是 attempt 1 success。最终实现 exact main 为
`b69527ec3a4c3037be730144c29b0ce2468940fc`。

七个 stage 分别建立：attempt-neutral operation projection；绑定 original `BudgetContext` 与 parent/child
`AttemptEligibility` 的 one-shot same-attempt gate；Fact `0.2/0.4`、Relation derivation `0.3/0.5`、Relation
observation `0.4/0.6` corrected wire/operands；三个 controller 与 downstream admission 的 exact-history
revalidation；以及 `LSPC-000..018` hardening。Provider-visible bodies 必须与 stage operation set 恰好相等，filtered
request 在 encoding 前建立，旧 wire 不 fallback，相同 semantic result 或 limits 不继承 attempt authority。

G exact-main final bytes 在 CPython 3.10.6 / 3.13.13 normal / `-O` 四格中取得 G direct `20/20`、A–G focused
`100/100`、related Language Support/controller/Relation `182/182` 与 full Review Attention `417/417`。canonical
hardening report 四格 SHA-256 均为：

```text
dc6ef339570c83af99e7882c3de703ea51e9df91c5b0fd9265bc1b65cbc9ca22
```

[文档 210](docs/210-r1-language-support-eligible-operation-projection-implementation-freeze-candidate.md)据此只条件化
发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FREEZE_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 210 自己的 final docs/static gates、original PR checks、受保护合入、new exact-main Public CI /
Browser Smoke，以及 README、文档 210、milestones 的 fresh anonymous installed-product readback 与 independent
reconciliation 后生效。后继还必须建立独立最终冻结发布，并完成同等级 final bytes、PR、merge、exact-main 双门与
fresh readback/reconciliation，才允许写
`R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN`。

当前不得自动开始 real parser / AST、Parse terminal、Fact fulfillment、persistence、public carrier/Schema、shared
receipt/ledger、ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。implementation exact-main verified 与
implementation frozen 必须继续分离。

## R1 Language Support eligible operation projection / same-attempt gate 实现冻结发布

文档 210 候选经 PR #230 original Public CI `36334206045` attempt 1、11/11 SUCCESS，ordinary merge
`main@e69ff64333300fc01bd89eb3dfbe69f447048b40`，以及 exact-main Public CI `36335678882` attempt 1、
11/11 SUCCESS 与 Browser Smoke `36335678884` attempt 1、1/1 SUCCESS。candidate / merge tree 均为
`cbf4e9597e1e719f7388080d788c5e40afc0f8e9`。

README、文档 210 与 milestones 三份 fresh anonymous installed-product observations 使用互不复用的 sealed
Plan/session/output，P1/P2 均 `COMPLETE`、三样本稳定、marker 恰好一次、Core `PASS`。AGENTS、README、
文档 210 与 milestones 四份 anonymous raw bytes 等于 exact Git blobs；independent reconciliation manifest 为：

```text
sha256_json  = dafb28072bd4d1e7e0969c2a19734101ccd3177d5fd186dd75f41c4d132a32fc
sha256_bytes = d6a8b6eb33ed053144a9d3563615d91edeea56772ff4ae732006e228b1fee5aa
```

正式观察前的 installed-environment / anonymous API preflight 已 HTTP 200，但 Playwright shutdown 留下 pending-task /
`TargetClosedError` warning；它没有正式 Plan/session/Evidence/output identity，继续保留为 setup history。

[文档 211](docs/211-r1-language-support-eligible-operation-projection-implementation-freeze-publication.md)只发布 A–G
已有 private implementation closure，不新增 wire、runtime、Parse、Fact 或 Coverage 语义。本发布的条件化 target 是：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRECONTRACT_AUDITED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_IMPLEMENTED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_STAGES_A_B_C_D_E_F_G_EXACT_MAIN_VERIFIED
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 target 只有在文档 211 final bytes、local docs/Schema/static gates、original PR checks、受保护合入、new exact-main
Public CI / Browser Smoke，以及 README、文档 211、milestones 的 fresh installed-product readback 与 independent
reconciliation 后生效。生效后必须先返回 CONTROL LOOP；不得由 implementation frozen 自动开始 real parser /
AST、Parse terminal、Fact fulfillment、persistence、public carrier/Schema、shared receipt/ledger、ReviewSliceSet /
Coverage、Evidence、publisher 或 Bundle。

## R1 Language Support eligible operation projection 实现冻结重新资格化

文档 211 的 publication PR #231 original Public CI `36342051676` attempt 1 为 11/11 SUCCESS，并以 ordinary
merge `main@fd5628123e5460de21039c81dc7f9e9ed7ae9772` 合入。该 exact main 的 Browser Smoke
`36343474807` attempt 1 为 1/1 SUCCESS，但 Public CI `36343474761` attempt 1 在 Python 3.10 `-O`
Review Attention 正式失败：`test_d_004_failed_assignment_validation_consumes_the_claim` 在约 `10.085s`
后跨过 sealed 10 秒 wall-clock budget，runtime 正确返回 `ADMISSION_BINDING_REJECTED`。因此文档 211 的
frozen target 没有生效；该 run 永久保持 FAILURE。

独立 PR #232 只修改 Slice-input test-support：保留真实 `BudgetContext`、limits、attempt identity、one-shot claim
与 cancellation semantics，把该 semantic suite 的 attempt-local test clock 固定在 admission 时刻，避免 hosted-runner
scheduling 把 identity / ownership 测试静默变成 deadline 测试。它没有修改 runtime、产品 timeout、budget、合同或
public state。

PR #232 head `f7651732ea419865814bb9e755916795c4cc9fa1` 的 original Public CI `36349719735`
attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 main 为
`df7f3d5a190d317a47c0fc1fb9405419e6b76828`，tree 为
`7bcfa7788ee929e2b60b22246eac01cb977ac0cb`。该 exact main 的 Public CI `36351246640` attempt 1 为
11/11 SUCCESS，Browser Smoke `36351246642` attempt 1 为 1/1 SUCCESS。maintenance 已成为合格 source
state，但不追溯使文档 211 生效。

[文档 212](docs/212-r1-language-support-eligible-operation-projection-implementation-freeze-requalification.md)以新
source identity 重新发布同一 private implementation frozen target。该 target 只有在文档 212 final bytes、local
docs/Schema/static gates、original PR checks、受保护合入、new exact-main Public CI / Browser Smoke，以及 README、
文档 212、milestones 的 fresh anonymous installed-product readback 与 independent reconciliation 后生效。

在此以前 frozen marker 仍只是 publication target。生效后也必须先返回 CONTROL LOOP；不得自动开始 real parser /
AST、Parse terminal、Fact fulfillment、persistence、public carrier/Schema、shared receipt/ledger、ReviewSliceSet /
Coverage、Evidence、publisher 或 Bundle。

文档 212 的 publication PR #233 original Public CI `36353138086` attempt 1 已 11/11 SUCCESS；ordinary merge
`main@0c82c55a521750698c969b26221bf776530aec16` 的 tree 为
`5ca3bb0952360ec05c9c4a3ba1ee8e46cfe6843d`，exact-main Public CI `36354589236` attempt 1 为
11/11 SUCCESS，Browser Smoke `36354589265` attempt 1 为 1/1 SUCCESS。README、文档 212 与 milestones
随后以互不复用的 Plan/session/output 完成 fresh installed-product observations 与 independent reconciliation。

milestones 前两次正式 observations 的 product/Core 均为 `COMPLETED / PASS`，但 runner 在 Windows 长路径
final-summary 写入阶段退出 1，因此两个 identity 永久保持 `ERROR / NON_QUALIFYING`；byte-preserving short-root
copy 后，第三个 fresh identity 才取得 PASS。最终 manifest 为：

```text
sha256_json  = 0354060769104d5647c322838740fc64af0c8e96d333698bdef963345fd16e82
sha256_bytes = 669c4af61877e8c9287a742bacb20b9dfc794ee0c30c4c0cc4f287ca6da00b08
```

因此 `R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN` 已成为事实；本地 checkout
alignment 只是 workspace hygiene，不是新增资格门。

## R1 Parse fulfillment authority 问题审计

[文档 213](docs/213-r1-parse-fulfillment-authority-problem-audit.md)从上述 frozen exact main 重新进入 CONTROL LOOP。
它只条件化发布：

```text
R1_LANGUAGE_SUPPORT_QUALIFICATION_CONTRACT_0_2_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PRIVATE_CLASSIFIER_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_CONTRACT_FROZEN
R1_LANGUAGE_SUPPORT_PARSE_GATE_PROJECTION_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_PRECONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

审计 paired world 保持 path、size、Policy/Profile、Provider set 与 controller 不变，只把 13-byte exact source 从
`def ok():\n 0\n` 改为 `def broken(:\n`。两者分别由独立 Python 3.10 parse oracle 得到 `SUCCESS` 与
`SYNTAX_ERROR`，但 current exact history 对二者都给出两次 ProviderRun `COMPLETED`、无 diagnostic、一个
`MODULE` Fact、overall `COMPLETED` 与 normal continuation。closed Fact Provider 不调用 parser；descriptor 的
`parser_id / parser_version` 只是 identity metadata。CPython 3.10.6 / 3.13.13 normal / `-O` 四格 report 均为
4479 bytes，SHA-256 均为：

```text
a942cf2662706b35a75140c16d5332754e9665ef2ca937068101a60ae61c4ce4
```

因此 eligibility、exact request membership、Provider `COMPLETED`、Fact membership、downstream Relation parse
或 normal continuation 都不能证明逐项 Parse fulfillment。本文只允许 problem-boundary audit；它不是
precontract，不授权 parser/AST、Parse terminal enum/reason、Fact fulfillment、persistence、shared carrier、public
Artifact/Schema、ReviewSliceSet/Coverage、Evidence、publisher 或 Bundle。

文档 213 的 candidate 只有在自己的 final README / AGENTS / milestones / doc bytes、local docs/Schema/static
gates、original PR checks、受保护合入、new exact-main Public CI / Browser Smoke、fresh README / doc213 /
milestones installed-product readback 与 independent reconciliation 全部闭合后才生效。任一失败身份必须保留；
闭合后仍须返回 CONTROL LOOP，重新判断 Parse fulfillment precontract audit 是否仍是最小合法问题。

## R1 Parse fulfillment 最小合同前置审计

文档 213 的重新资格化 PR #236 original Public CI `36362377502` attempt 1 为 11/11 SUCCESS；ordinary merge
后的 exact main 是 `5d0769b8ce9d7823b5a095de3657531085d19e83`，tree 为
`e58017d1fe67a7954486f39b216dc4267fa93d2e`。该 exact main 的 Public CI `36363900026` attempt 1 为
11/11 SUCCESS，Browser Smoke `36363899988` attempt 1 为 1/1 SUCCESS。

README、文档 213 与 milestones 随后以三个 fresh Plan/session 完成 anonymous installed-product readback，均为
HTTP 200、三样本稳定、唯一 marker、`COMPLETE / PASS`。正式观察前 Playwright shutdown warning 与第一次误选
runner 都发生在 Plan/session/Evidence/output lifecycle 之前，分别保留为 `SETUP-PREFLIGHT-001` 与
`SETUP-RUNNER-001`，不是 product observation。独立 verifier 重新核对 original PR、merge parents/tree、
exact-main 双门、Plan-before-observation、Core fields 与四份 exact Git raw bytes；最终 manifest 为：

```text
sha256_json  = 44a1fe0ddc803ea9602882c653418cb94606b24518c264cb6b45ef69cb7e00ab
sha256_bytes = faed852d3373b67e9e8367529ad2ab22d937959171cb598019cfcfce0458bc25
```

因此 `R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED` 已成为 qualified history。重新进入 CONTROL LOOP 后，
Parse precontract audit 仍是最小合法问题，但文档编号不自动授予合同或实现权。

[文档 214](docs/214-r1-parse-fulfillment-precontract-audit.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该审计规定 Parse denominator 只能来自 exact Language Support `ELIGIBLE` subjects；一个 subject 在一次 parent
attempt 中只有一个共享 Parse obligation，Provider duplication 不创建多个 truth。ambient
`ast.parse(feature_version=(3,10))` 是 best-effort witness，不是 CPython 3.10.6 authority；grammar parse success
不承诺 compilation/scoping/execution validity。semantic result、execution lifecycle 与 denominator reconciliation
必须正交，`never attempted` 是 missing obligation，不是 parser terminal。target parser reject 在另一个 frozen
version discriminator 成立前不得写成 `UNSUPPORTED_SYNTAX_VERSION`。

successful terminal bit 也不足以供 Fact 继承：后继 Fact consumer 必须取得同一个 admitted、immutable/copy-owned
parse product 或可验证的 exact product identity；自行 reparse 是新 observation，不能继承 upstream authority。
具体 parser、AST normalization/carrier、enum、receipt、Schema、Fact fulfillment、persistence、公有 Artifact 与
Coverage 都没有获得施工权。

文档 214 只有在自身 final bytes、local docs/Schema/static gates、original PR checks、受保护合入、new exact-main
Public CI / Browser Smoke、fresh README / doc214 / milestones installed-product readback 与 independent
reconciliation 全部闭合后，才可发布 `PRECONTRACT_AUDITED`。闭合后必须返回 CONTROL LOOP；不得自动起草合同
或进入 implementation。

## R1 Parse → Fact consumer projection 前置资格审计

文档 214 候选 PR #237 head `9e76639ed42f69e43d7783180be143dee6acc8af` 的 original Public CI
`36367307721` attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 exact main 是
`5593f48256acafeda6205ffde174441781c87c2e`，tree 为
`c5d9fcc726b3c57019b0857c04c0e445f1e08386`。该 exact main 的 Public CI `36400964690` attempt 1 为
11/11 SUCCESS，Browser Smoke `36400964718` attempt 1 为 1/1 SUCCESS。

README 与文档 214 的 formal readback 直接 `COMPLETE / PASS`。milestones formal #1 使用 Plan
`r1-parse-precontract-milestones` 与 session `github-paired-3dcf5cbcc0cf4a1a93443ab29faa73c9`，在
summary/handoff/Bundle 以前因 anonymous API `HTTP 403 / remaining=0` 保持 `ERROR / NON_QUALIFYING`；P2
public render 独立完成。reset 后的 fresh Plan `r1-parse-precontract-milestones-2` 与 session
`github-paired-2530d43a51d644479ac9ce394874a690` 取得 `COMPLETE / PASS`。独立 reconciliation 同时保存首个
ERROR 与三个 qualifying observations：

```text
sha256_json  = 4c7482a55bbaaf67585568b6e6b84c5cf3d12ec232a5bcbe5d4b85d1d134716b
sha256_bytes = cea42a376fc022da40d3e0b37b2e942475cf1dec25101d0e3ec72706a96b88b0
```

因此 `R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED` 已成为 qualified history。重新进入 CONTROL LOOP 后，
[文档 215](docs/215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)发现更早 prerequisite：文档 208 与
current runtime 都强制 `FACT_DERIVATION operation_subject_ids == eligible_subject_ids`，request/worker 又要求
Provider-visible bodies 与 operation set 恰好相等；controller 没有 Parse result/product 输入。

audit-only paired world 含一个 syntax-valid 与一个 syntax-invalid source，两者都被 Language Support 0.2 判为
`ELIGIBLE`。独立 Parse witness 只接受 valid source；current Fact request 仍携带两份 body，closed Provider 实际对
invalid source 报告 canonical `MODULE` Fact；把 request 收窄到 accepted-only set 会被 current wire 拒绝。
CPython 3.10.6 / 3.13.13 normal / `-O` 四格 1041-byte reports 逐字节一致：

```text
bf42f8051226388e3823b92f572a570071f2ec513c455d7c14685f283260203f
```

本文只条件化发布：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED
R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该 candidate 必须完成自己的 final docs/static gates、original PR checks、受保护合入、new exact-main Public CI /
Browser Smoke、fresh README / doc215 / milestones installed-product readback 与 independent reconciliation 才能成为
qualified history。它不推翻文档 208 在 pre-Parse claim domain 内的历史事实；它只禁止 current Fact projection
静默继承为 post-Parse consumer authority。下一步最多审计 versioned Parse-result → Fact-consumer projection /
request binding；不得直接修改旧合同、实现 parser/AST/new wire/Fact、选择 persistence 或恢复 Coverage。

## R1 Parse product → Fact consumer binding 最小前合同审计

文档 215 候选 PR #238 head `fdc3c3222615cf63eb1d98abf25706295ec25a33` 的 original Public CI
`36406936981` attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 exact main 是
`34b58014b1eadd0b30bc4deb73ab2cc97e2ed675`，tree 为
`37a75ee670d0f1bd288486d351a137c353beaa85`。该 exact main 的 Public CI `36409451476` attempt 1 为
11/11 SUCCESS，Browser Smoke `36409451412` attempt 1 为 1/1 SUCCESS。

README、文档 215 与 milestones 以三个 fresh Plan/session 取得 `COMPLETE / PASS`，四份 public raw bytes 与 exact
Git blobs 相等。独立 verifier 重新核对 original PR、merge/tree、exact-main gates、Plan-before-observation、Core
fields 与 source bytes，final manifest 为：

```text
sha256_json  = 4acc88bb15f35b7b362f9feacd446277547d82625e13f89a207390496f5dab79
sha256_bytes = 12a8004834b3b083f6a25f309666c8852cde7a8d062103907e2545e96ea9e80e
```

因此 `R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDITED` 已成为 qualified history。重新进入
CONTROL LOOP 后，[文档 216](docs/216-r1-parse-product-fact-consumer-binding-precontract-audit.md)把下一 seam
拆为 consumer membership、exact product binding 与 product consumption authority。

accepted IDs 不能区分同一 subject 的不同 Parse products；empty accepted set 不能区分 all-rejected complete 与
missing/non-success；相同 product-set semantics 不继承另一 attempt 的 live claim；request/terminal 回显 product
identity 也不能证明 Provider 实际消费 product。多个 Fact Providers 必须共享一份 application-owned reconciled
product truth，并分别领取 provider-bound child claim，不能按 Provider 数量复制 Parse truth。

仓库外 `consumer_matrix.py` 在 CPython 3.10.6 / 3.13.13 normal / `-O` 四格各产生 1456-byte report，逐字节
相同：

```text
38c4af75a33c7f9718cd980e8e8069a46bd888d311fd35e8500b603f31358f32
```

第一次额外 byte comparison 在 reports 已生成并取得相同 size/hash 后误用 PowerShell `AsSpan()`，保留为
`INVALID_AUDIT_COMPARISON_SETUP`；后继显式 byte-array comparison 只复核既有 outputs，没有覆盖旧 evidence。

本地候选还保留 AGENTS patch anchor miss、`git diff --name-only` 漏掉 untracked doc216 与首次并行测试 wrapper
未保存 final summaries 三个 setup/orchestration 问题；它们都未形成 product observation。最终四文件 scope、
relative links、UTF-8/LF/final-LF、fences、marker、audit hashes 与 `git diff --check` 全部通过。docs/Schema 四格
各 `40/40 PASS`；source-operation gate、Fact wire、controller integration 与 multi-Provider composition 四格各
`67/67 PASS`。这些结果只支持 candidate 提交，不授予 contract/runtime authority。

本文只条件化发布：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED
R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDITED
R1_PARSE_PRODUCT_FACT_CONSUMER_BINDING_PRECONTRACT_AUDITED
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该候选必须完成 final docs/static gates、original PR checks、受保护合入、new exact-main Public CI / Browser Smoke、
fresh README / doc216 / milestones installed-product readback 与 independent reconciliation，才能成为 qualified
history。它不冻结 Parse product、consumer correction 或 zero-accepted scheduling；最后门闭合后必须返回 CONTROL
LOOP，最多重新判断 Parse minimal contract 是否仍是最小合法问题，不得直接实现 parser/AST/product/new wire/Fact、
选择 persistence 或恢复 Coverage。

## R1 Parse fulfillment 最小合同 0.1 候选

文档 216 候选 PR #239 head `ca90402e23e7dcf07f7d085882843eba19dd5dde` 的 original Public CI
`36414215832` attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 exact main 是
`63daada4157e0068bb2a1333953f821f56f61894`，tree 为
`4ff61ed57f6b88c8dfbe4d1adb53c9652eab106a`。该 exact main 的 Public CI `36416676877` attempt 1 为
11/11 SUCCESS，Browser Smoke `36416676883` attempt 1 为 1/1 SUCCESS。

README、文档 216 与 milestones 使用三个 fresh Plan/session 取得 `COMPLETE / PASS`；四份 public raw bytes 与
exact Git blobs 相等。独立 verifier 的 final manifest 为：

```text
sha256_json  = 9b896e85c11efbd90cb4a19c8a12674652de568e80e7ed9619f80aba95649dc2
sha256_bytes = fd04d68753dff54f1b6f6f64d854cf3eb0267ac5b0bc5697286dd31544e22d5
```

因此 `R1_PARSE_PRODUCT_FACT_CONSUMER_BINDING_PRECONTRACT_AUDITED` 已成为 qualified history。重新执行 CONTROL
LOOP 后，没有新反例击穿 Parse contract 的最小边界；[文档 217](docs/217-r1-parse-fulfillment-contract.md)只冻结：

```text
exact Language Support ELIGIBLE denominator
one shared Parse obligation per subject / parent attempt
r1-python-parse/0.1 with CPython 3.10.6 reference semantics
grammar-only ACCEPTED(product) / REJECTED(PARSE_ERROR)
semantic result / execution lifecycle / reconciliation separation
complete denominator closure and admitted product-set identity
same-attempt immutable/copy-owned product access
semantic value != live continuation authority
```

carrier、digest algorithm、persistence、Fact product-use enforcement、zero-accepted scheduling、new wire、Fact
fulfillment 与 Coverage 仍是 non-decision / not authorized。本文是 docs-only contract candidate；它必须完成自己的
original PR、受保护合入、new exact-main gates、fresh public readback 与 independent reconciliation，再由独立 freeze
publication 取得同等级资格，才可成为 `CONTRACT_FROZEN`。在此以前 runtime 继续 `NOT_STARTED`。


## R1 Parse fulfillment 合同冻结发布（条件状态）

文档 217 候选经 PR #240 original Public CI `36422575750` attempt 1 11/11 SUCCESS、ordinary merge
`main@446604ffc437ff710faf524c1634839dc1a0ddd7`、tree
`aa9099f6c4667c39c7493743245a523ca9626351`、new exact-main Public CI `36425303909` attempt 1
11/11 SUCCESS 与 Browser Smoke `36425303740` attempt 1 1/1 SUCCESS 取得 source qualification。

fresh installed-product readback 的 README 正式 observation #1 使用 Plan `r1-parse-contract-readme` 与 session
`github-paired-9f6eba497a094517b190d2ad5c9a1d18`，P1 因匿名 core rate limit remaining 0 返回
`ERROR / HTTP 403 / COLLECTION_BUDGET_EXHAUSTED`，P2 为 COMPLETE；该身份永久保留且不计入资格。reset 后全新
README Plan/session 与 doc217、milestones 两份独立 Plan/session 均取得 `COMPLETE / PASS`。五份 public raw bytes
等于 exact Git blobs；independent reconciliation manifest 为：

```text
sha256_json  = f76d687ab15a06a5e20172429176774c2c65ecc82616b2628dfcf043bcb3a292
sha256_bytes = 78bddb62cf980afb79fca85d8cd201b6fda3bca6e7ca426bb73280da51e6d76b
```

因此 doc217 现在是 qualified contract candidate。[文档 218](docs/218-r1-parse-fulfillment-contract-freeze-publication.md)
只条件化发布以下目标：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

这些 marker 只有在 freeze publication 自己的 final bytes、original PR required checks、受保护合入、new exact-main
Public CI / Browser Smoke、README / doc217 / doc218 / milestones fresh anonymous installed-product readback 与 independent
reconciliation 全部成立后才生效。在此以前 current fact 仍为 contract candidate；不得开始 parser、AST、Parse
product carrier、Fact consumer correction、persistence、Schema、publisher 或 Coverage。最后门闭合后必须返回
CONTROL LOOP，重新判断 implementation feasibility / authorization 是否仍是最小合法问题，不能按文档编号自动施工。

## R1 Parse fulfillment private implementation 可行性审计候选

[文档 219](docs/219-r1-parse-private-implementation-feasibility-audit.md)从
`main@bb912680d55ca8c96df4d5b9ded88187bbaf42ef` 重新执行 CONTROL LOOP。该 exact main 上文档 218 的
冻结门已全部闭合，所以 `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN` 是当前事实；实现仍为 `NOT_STARTED`。

审计确认现有 budget/containment、exact Language Support classification 与 source-gate identity discipline 可以承载
private Parse closure，但 parser authority 必须来自 controller 显式选择的 exact CPython 3.10.6 reference runtime。
ambient `sys.executable`、PATH / `py -3.10` 搜索、descriptor 自报或 3.13 `feature_version=(3,10)` 都不能拥有
`r1-python-parse/0.1` authority；reference runtime absence、worker failure、timeout、resource stop 与 malformed terminal
只能形成 lifecycle/reconciliation non-success，不能伪装 `PARSE_ERROR`。

仓库外 audit-only worker 将 exact 3.10.6 `ast.Module` 的全部 fields、present attributes、ordered lists 与显式 scalar
encoding 投影为 private canonical copy-owned product。feasibility matrix 与真实 Windows execution-cell probe 在
CPython 3.10.6 / 3.13.13、normal / `-O` 四格分别逐字节一致；同一 original `BudgetContext` 可顺序完成 accepted 与
rejected 两个 subject。该 witness 只证明 bounded private implementation shape 可行，不证明全部 grammar、恶意
runtime authenticity、public persistence 或 post-Parse Fact product-use boundary。

当前条件状态为：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文还修正 README“系统家族与未来边界”中遗留的 precontract-candidate current summary；历史章节中的候选与失败
身份不改。本文只允许 AGENTS、README、milestones 与新增 doc219 四个文档文件；runtime、tests、Schema、Profile、
Policy、corpus、architecture assets、Provider 与 wire 必须保持原字节。

候选必须完成 final-byte local gates、original PR checks、受保护合入、new exact-main Public CI / Browser Smoke、
README / doc219 / milestones fresh anonymous installed-product readback 与 independent reconciliation，才能成为
qualified history。随后必须先返回 CONTROL LOOP，并通过独立 docs-only implementation authorization publication；
该 publication 自己的门闭合前，不得创建 parser runtime branch。即使获得授权，下一 implementation 也最多覆盖
doc219 A–H；不得修改 current Fact wire、选择 persistence、启动 Fact fulfillment 或 Coverage。

## M10 Browser 主机 socket 分类与发行消费边界审计（条件状态）

文档 219 候选 PR #242 head `ed3cfa2871df864e84068cc32f52081863de8878` 的 original Public CI
`36440677161` attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 exact main 为
`23f9825e61791a78056d5154e4dfd3626a1167b1`，tree 为
`ae1496ba1978ddb40b3a74e414b4e6f58f9bddd5`。该 exact main 的 Public CI `36443544885`
attempt 1 为 11/11 SUCCESS，Browser Smoke `36443544713` attempt 1 为 1/1 SUCCESS。README、doc219 与
milestones 的 fresh installed-product readback 与 independent reconciliation 也已成立，因此
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED` 是 qualified history。

独立实现授权 PR #243 没有取得资格。其 original Public CI `36449716998` attempt 1 的十项检查成功，
`Starter PASS/FAIL golden path` job `109027269096` 失败。Artifact
`starter-single-webapp-s1-failure-36449716998-1` 保存：桌面 document / title / fill / click 成功后，loopback
`/data.json` fetch 以 `net::ERR_NO_BUFFER_SPACE` 失败；同一服务上的后继 mobile viewport 两次请求 `200` 并
完整通过。M10 没有把这个 Windows host-local socket failure 写入 `collection_errors`，于是错误形成
`BROWSER_HARD_FAILURE / COMPLETED / FAIL / SUBJECT`。精确底层资源原因保持 `UNKNOWN`。

更关键的是，该 required lane 固定下载 SHA-256
`3a42f28db6f4ed12351dade3fbb6f57fa1d5aa3fdd6d28210492f676bc1562de` 的公开 Core v0.12.2 wheel，
并使用只接受 `veritrail>=0.12,<0.13` 的 Starter 0.2.0。current main 与 Latest Core 是 0.13.0；修改 current
source 不能修复 #243 实际消费的 distribution，Starter 0.2 又会拒绝 current Core。历史 v0.12.2 / v0.13.0
tag 与 Release assets 继续只读，当前没有新 maintenance/patch release、Starter compatibility migration 或 CI
consumer migration 的合同 authority。

[文档 221](docs/221-m10-browser-host-socket-release-consumer-boundary-audit.md)只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_RELEASE_CONSUMER_BOUNDARY_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

PR #243 保持 CLOSED / original FAILURE，head 与 run 不 rerun、不改写。doc221 只允许 AGENTS、README、
milestones 与自身四个文档文件；runtime、tests、workflow、Starter、version、tag、Release、timeout 与 retry 都必须
保持原字节。本文自己的 final-byte local gates、original PR checks、受保护合入、new exact-main Public CI / Browser
Smoke、README / doc221 / milestones fresh installed-product readback 与 independent reconciliation 全部成立后，
只获得 qualified problem boundary。后继仍须先返回 CONTROL LOOP，只能重新审计最小 correction /
release-consumer precontract；不得直接重发 Parse implementation authorization 或提交 current-source 映射。

## M10 Browser 主机 socket 分类修正与发行消费最小前合同审计（条件状态）

doc221 已经 PR #244 original Public CI `36454917831` attempt 1 的 11/11、ordinary merge
`main@02ba60fd4f2e78f273485ba84110540cef209509`、new exact-main Public CI `36457785860` attempt 1 的
11/11 与 Browser Smoke `36457786007` attempt 1 的 1/1，以及 README / doc221 / milestones 三份 fresh
installed-product PASS 和 independent reconciliation 成为 qualified problem boundary。final manifest 为：

```text
sha256_json  = 0333b6ddf4489fcd2d4ac8d64ba47b122f76106dc9c2b10e57d805a2f8997a74
sha256_bytes = 1f45742e782e15ec95306b5a3619d11127bc61f42d7012babe9820aa1e46eede
```

[文档 222](docs/222-m10-browser-host-socket-classification-correction-release-consumer-precontract-audit.md)
据此只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_PRECONTRACT_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

该审计把 Browser classification authority、Starter compatibility authority、workflow consumer selection 与每个
Core distribution 自己的发行资格分开。仓库外诊断证明：从精确 v0.12.2 release 谱系加入窄映射并构建的
Core 0.12.3 wheel，可由 SHA-256
`ce6e9ea0730adc891aba97f8148fdb861fffdd5164989c980b5cbbaaa950771f` 的公开 Starter 0.2.0 wheel
接受，并完成真实 PASS/FAIL、Catalog、Workbench 与清理链；acceptance 摘要 SHA-256 为
`570a853ac5f6b544e8d48168afb533a22cce739f7b39dcf94b39701dbe37faa6`。全部结果仍是
`DIAGNOSTIC_ONLY_NON_QUALIFYING`，没有 candidate、tag、Release 或 public 0.12.3。

0.12.3 不得从 current main 构建，必须来自 exact v0.12.2 谱系上的受治理 maintenance coordinate；current
0.13 source correction、public 0.12.3 repair 与任何 future public 0.13.x repair claim 都必须独立取得资格。
doc222 只允许 AGENTS、README、milestones 与自身四个文档文件。它自己的 final-byte local gates、original PR、
受保护合入、new exact-main 双门、fresh README / doc222 / milestones installed-product readback 与 independent
reconciliation 全部闭合后，只授权起草最小 correction / release-consumer contract。runtime、tests、workflow、
version、maintenance branch、ruleset、tag、Release、assets 与 Parse authorization 仍未开始。

## M10 Browser 主机 socket 分类修正与发行消费合同（条件状态）

doc222 经 PR #245 original Public CI `36466022463` attempt 1 的 11/11、ordinary merge
`main@fc2be4009989c3ddc0ff71fc5f0a54c02290751a`、new exact-main Public CI `36469016262`
attempt 1 的 11/11 与 Browser Smoke `36469016158` attempt 1 的 1/1，以及 README / doc222 /
milestones 三份 fresh installed-product PASS 与 independent reconciliation，已经成为 qualified precontract audit。
final manifest 为：

```text
sha256_json  = 0ec68ad5805535e9a06676eb403f4a6b3298765258d1bfcde5f2b8f96c3bf1dd
sha256_bytes = 8a5506d1f79b96fdd17486aa7919575677892a0c7a20d01ecbb9dde6d0721b05
```

[文档 223](docs/223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_CONTRACT_CANDIDATE
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_IMPLEMENTATION_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

合同候选把后继工作串行为 current-main 窄修正、`core-0.12-maintenance` 两阶段 ruleset/bootstrap、精确
v0.12.2 谱系上的 0.12.3 backport 与 non-Latest create-new publication、公开产品读回，以及 main required
Starter lane 的单独消费迁移。phase-one ruleset 只服务 workflow-enablement PR；maintenance exact-tip 双门与
phase-two strict required checks 成立以前，任何 runtime/version backport 均不得开始。public v0.13.x 是独立
发行义务，不是重新审查 Parse authorization 的前置门。

doc223 只允许 AGENTS、README、milestones 与自身四个文档文件。它自己的 final-byte local gates、original
PR、受保护 main 合入、new exact-main 双门、fresh README / doc223 / milestones installed-product readback 与
independent reconciliation 全部闭合后，只成为 qualified contract candidate；仍须独立 freeze publication 才能
生效。冻结以前不得创建 maintenance branch、ruleset、runtime patch、version、tag、Release、asset 或 workflow
migration，也不得重发 Parse implementation authorization。

## M10 Browser 主机 socket 分类修正与发行消费合同冻结发布（条件状态）

doc223 已经 PR #246 original Public CI `36473865925` attempt 1 的 11/11、ordinary merge
`main@5703ac4126e9645569b4631b4cc359ebca70e6d9`、new exact-main Public CI `36476517678`
attempt 1 的 11/11 与 Browser Smoke `36476517518` attempt 1 的 1/1，以及 README / doc223 /
milestones 三份 fresh installed-product PASS、七份 raw public bytes 与 independent reconciliation 成为
qualified contract candidate。manifest 为：

```text
sha256_json  = 37c1fb9620a4d1524188903b9ee34fb3f293a96a9847764ffc605ece2fb9f7b0
sha256_bytes = 6b38ee7a7931d60b4a7880652db8d7f851e8efaff6b96c8377fbc4fbd8be4d6c
```

[文档 224](docs/224-m10-browser-host-socket-classification-correction-release-consumer-contract-freeze-publication.md)
只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_CONTRACT_FROZEN
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_IMPLEMENTATION_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

doc224 只允许 AGENTS、README、doc223、milestones 与自身五个文档文件。它自己的 final-byte local gates、
original PR、受保护 main 合入、new exact-main 双门、fresh README / doc223 / doc224 / milestones installed-product
readback 与 independent reconciliation 全部闭合后，frozen target 才生效。最后门以前不得开始 runtime、
maintenance branch、ruleset、version、tag、Release、asset、workflow migration 或 Parse implementation。

后继 CONTROL LOOP 已完成 C1：PR #249 head `6fec13def5b0e8f66362fbd7b81f191be8e48110` 的 original Public CI
`36637526486` attempt 1 为 11/11，合入 `main@2daf6eaefa20b0bf3f371eed50e74f3d863496b3` 后 exact-main
Public CI `36639973530` attempt 1 为 11/11，Browser Smoke `36639973548` attempt 1 为 1/1。该事实只证明
current source 已修正，不发布新 wheel。M0 随后创建 active、无 bypass 的 phase-one ruleset `24216773`，但
第一次真实 exact branch ref 创建返回 HTTP 404，branch 保持不存在。精确现场见
`docs/225-m10-maintenance-bootstrap-governance-counterexample-audit.md`。后继只读核账又证明：该次 OAuth credential
没有 `workflow` scope，且旧 `.github/workflows/ci.yml` 在当前任何远端 branch tip 上都没有同路径同内容副本，
因此 scope 例外不成立。追加更正位于
`docs/226-m10-maintenance-branch-creation-authority-correction-audit.md`；404 继续保留，但它没有资格证明
ruleset/governance counterexample。当前状态为：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CURRENT_SOURCE_EXACT_MAIN_VERIFIED
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_NOT_CREATED
M0_BRANCH_CREATION_AUTHORITY_UNQUALIFIED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

不得改用实际 git push、disable/evaluate/delete ruleset、增加 bypass、先建未保护 branch、创建 workflow PR 或
开始 runtime/version/backport/release/consumer migration。不得在本审计中运行 `gh auth refresh` 或重试 ref creation。
后继只能先资格化 workflow-bearing branch creation 所需的 credential authority；scope 扩张属于独立授权动作，
新的写观察必须使用新身份且不得覆盖第一次 404。`do_not_enforce_on_create` 不修复 credential 缺权，也不是当前候选。

## M10 0.12 maintenance workflow bootstrap 顺序反例（候选状态）

Human 已明确授权补齐 GitHub OAuth `workflow` scope；新 credential 读回为
`delete_repo / gist / read:org / repo / workflow`。随后只进行一次新的 REST create-reference 写观察，返回
`HTTP 201`。REST 与 Git 双读回确认 `refs/heads/core-0.12-maintenance` 精确指向
`f961930ae1e69d7d88849fa2b0d40befb3e94c89 = v0.12.2^{}`。ruleset `24216773` 保持 active、无 bypass、
禁止删除与 non-fast-forward、要求 PR、required checks 为空。第一次 `HTTP 404 / UNKNOWN` 继续保留；后继 201
不解释旧失败。

workflow-only PR #252 只修改 `.github/workflows/ci.yml` 与 `.github/workflows/browser-smoke.yml` 的 branch
filters。其本地 final-byte 四格和 Browser acceptance 成立，但 original Public CI `36771080921` attempt 1 在
Workbench `npm audit` 因 `brace-expansion` 与 `undici` 两组 high-severity advisory 失败；六个 job 成功，Starter
golden path 因依赖 job 失败而跳过。#252 未 rerun、未改 head、未合入并已关闭。

current main 已通过 PR #248 把 `undici` 锁到 `7.30.0`，并通过 PR #253 把 root / nested
`brace-expansion` 锁到 `5.0.12 / 2.1.7`。#253 original Public CI `36773193271` attempt 1 为 11/11，合入
`main@30d459197c24dabcfd28f9d50f6ed582ee029258` 后 exact-main Public CI `36775834977` attempt 1 为
11/11，Browser Smoke `36775834866` attempt 1 为 1/1。这些门只证明 current main；maintenance branch 仍保留
`undici 7.29.0` 与 `brace-expansion 5.0.9 / 2.1.4 / 2.1.4`。

[文档 227](docs/227-m10-maintenance-workflow-bootstrap-ordering-counterexample-audit.md)只登记：

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_BOOTSTRAP_ORDERING_CORRECTION_REQUIRED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

它只最小重开 exact branch 创建以后、workflow-only PR 以前的 dependency qualification / ordering seam。
在本文自己的 final-byte local gates、original PR、受保护 main 合入与 new exact-main 双门成立以前，这仍是 audit
candidate。不得重开/rerun #252，不得把 lockfile 塞进 workflow-only PR，不得直接修改 maintenance branch、运行
`workflow_dispatch`、创建 dependency PR、弱化 audit、升级 phase two 或开始 backport/release/consumer migration /
Parse。后继只能先审计并冻结 dependency prerequisite 的 source、scope、验证、merge 与 exact-tip 资格链。

## M10 0.12 maintenance dependency prerequisite 最小前合同审计

从 exact maintenance commit `f961930ae1e69d7d88849fa2b0d40befb3e94c89` detached 构造的 bounded candidate
只修改 `web/package-lock.json`：`undici 7.29.0 -> 7.30.0`、root `brace-expansion 5.0.9 -> 5.0.12`、
两处 nested `2.1.4 -> 2.1.7`。base / candidate lock SHA-256 分别为
`FD50366E34F3FECE0CD661A18989A6BC41217B1AD92BFD3E4C79D15002CD20D1` /
`6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E`。candidate 与 current main lock
逐字节相同，但不继承 main qualification。

fresh npm `11.19.1` 安装与 Workbench 14 files / 172 tests、lint、type-check/build、full audit 0 vulnerability、
dependency tree 与 exact one-file diff 成立。错误并发运行的 Python 四格分别留下 `6 / 6 / 7 / 7` 个
`RESOURCE_MEMORY_SOFT_LIMIT` 相关失败；随后 3.10 normal 顺序观察仍在真实 `4096 MB` soft line 下留下 10 个失败。
这些观察保持非资格失败，不得改写成 Python / Browser PASS，也不得通过调大预算解决。

GitHub 官方 `workflow_dispatch` 语义允许对 branch / tag ref 运行 workflow，run 的 `head_sha` 绑定该 ref 的最后
提交。旧 Public CI / Browser Smoke 均已有 `workflow_dispatch`。因此[文档 228](docs/228-m10-maintenance-dependency-prerequisite-precontract-audit.md)
把唯一进入后继合同候选的路线收缩为：one-file topic candidate -> exact-head 两条 dispatch witness -> ruleset-protected
PR merge -> exact maintenance-tip 两条 fresh dispatch witness -> 返回 CONTROL LOOP -> 新 workflow-only candidate。
dispatch witness 不是 original PR check；ref、head SHA、attempt、job denominator、conclusion 与 merge tip 必须独立核账。

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

doc228 已经 PR #255 head `3b885a7230e1af37a00dcd8db5fed6faefbc4dd4` 的 original Public CI
`36786553995` attempt 1 11/11、ordinary merge `main@1227d41ff3c0d052f6b9e90f8be55ae89b2912fc`、
new exact-main Public CI `36789112514` attempt 1 11/11 与 Browser Smoke `36789112562` attempt 1 1/1，
成为 qualified precontract history。它只授权起草最小 dependency prerequisite contract；不授权 dependency write、
dispatch、workflow bootstrap、phase two、release 或 Parse。

## M10 0.12 maintenance dependency prerequisite 合同冻结发布（条件状态）

[文档 229](docs/229-m10-maintenance-dependency-prerequisite-contract.md)只条件化发布：

```text
M0_PHASE_ONE_RULESET_CREATED
M0_MAINTENANCE_BRANCH_CREATED
M0_WORKFLOW_BOOTSTRAP_CANDIDATE_FAILED
M0_MAINTENANCE_DEPENDENCY_QUALIFICATION_GAP_PROVEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

合同候选冻结 exact source / package inputs、npm 11.19.1 targeted update、四个 lock entries 与 final hash、one-file scope、
local Workbench gates、PR/ruleset/ordinary merge identity，以及 topic-head / maintenance-tip 两组不可借用的
Public CI + Browser Smoke `workflow_dispatch` observations。dispatch witness 不是 original PR check 或 required check；
candidate 与 tip 必须各自绑定 ref、head SHA、attempt 1、完整 job denominator 与 conclusion。

文档 229 已经 PR #256 head `c5e10ebd215d168293713714ef189742ff64d806` original Public CI
`36792226029` attempt 1 11/11、ordinary merge `main@be1db09637b8b499269b6281c5ab744ddf27db02`、
new exact-main Public CI `36794128077` attempt 1 11/11 与 Browser Smoke `36794127955` attempt 1 1/1。
README / doc228 / doc229 / milestones 四份 fresh installed-product readback 与 independent reconciliation 均 PASS，
因此文档 229 已是 qualified contract candidate。

[文档 230](docs/230-m10-maintenance-dependency-prerequisite-contract-freeze-publication.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_IMPLEMENTATION_NOT_STARTED
```

文档 230 自己的 final bytes、original PR、受保护 main 合入、new exact-main 双门、fresh README / doc229 /
doc230 / milestones installed-product readback 与 independent reconciliation 已全部闭合。final manifest
`sha256_json=1dcd412b0f298ad7a90d779b0d16bd5b5102f0f892838cb4c9f9484d3d4cf1a7`，因此合同已经
`FROZEN`；冻结没有自动开始实现。

## M10 maintenance dependency prerequisite 资格发布（条件状态）

[文档 231](docs/231-m10-maintenance-dependency-prerequisite-qualification-publication.md)条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

one-file candidate `823add7850867754db1fea5b484c083678be0873` 只修改 `web/package-lock.json`；fresh npm
11.19.1 install、Workbench 14 files / 172 tests、lint、type-check/build、audit 0 vulnerabilities 与 exact lock
projection 成立。PR #258 的 candidate-head manual dispatch 为 Public CI `36803540792` attempt 1 7/7 和 Browser
Smoke `36803550201` attempt 1 1/1；ordinary merge `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` 保持同一
tree/lock bytes，maintenance-tip fresh dispatch 为 Public CI `36804634994` attempt 1 7/7 与 Browser Smoke
`36804645585` attempt 1 1/1。candidate/tip run 不互相借用。independent manifest
`sha256_json=6ca3a967ed8b39f0aabd88fcf2553f2d4d774c4769663d53c4ae53bce0b5742c`。

本文自己的 original PR、受保护 main 合入、new exact-main 双门、fresh README / doc229 / doc230 / doc231 /
milestones installed-product readback 与 independent reconciliation 全部闭合后，qualified target 才生效。最后门以前
仍是 implementation not started / bootstrap blocked。闭合以后必须从 exact maintenance tip 返回 CONTROL LOOP，重新
审查 workflow-only bootstrap；不得重开/rerun/改写 #252，不得自动启动 phase two、backport/release、consumer
migration 或 Parse。

## M10 maintenance dependency drift 反例审计（条件状态）

从 exact maintenance tip `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` 建立的 workflow-only PR #264 保持
两文件 scope；原始 Public CI `37795167502` attempt 1 的 Python、E3、wheel-only 与 Workbench tests/lint/build
成功，随后 official-registry `npm audit` 对 Vue/server-renderer、postcss-selector-parser 与 source-map-js 报告
`1 moderate / 3 high`，因此 Workbench 与整条 run 为 `FAILURE`，Starter golden path 跳过。#264 已关闭、未合入、
未 rerun、未改 head，maintenance ref 未移动。

[文档 233](docs/233-m10-maintenance-dependency-drift-counterexample-audit.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

文档 231 的 timed PASS 继续属于旧 observation；新 advisory 不改写旧历史，但阻断当前 bootstrap。文档 229
冻结的是旧 base、旧四 entry、旧命令和 final hash，不能静默扩张到新 dependency set。main PR #262 只提供候选
版本证据，不转移 maintenance authority。doc233 的 final-byte local gates、original PR、受保护 main 合入与 new
exact-main 双门闭合以前，公开状态仍停在 doc231；闭合后也只授权新的 dependency-drift precontract audit。

不得直接复制 #262、创建 dependency PR、运行 dispatch、修改 maintenance branch/ruleset/workflow、重开 #264、
弱化 audit、启动 phase two/backport/release/consumer migration、Parse / Fact / Coverage 或
`DECLARED_CLAIM_FIDELITY`。

## M10 maintenance dependency drift 最小前合同审计（条件状态）

[文档 234](docs/234-m10-maintenance-dependency-drift-precontract-audit.md)从 qualified doc233 source state 重新绑定
`main@0f2fef265582f9bf80c32e3c08ff1580250d67ef`、maintenance
`6ed18ae8b3d8b98b6e5be7af709aa868590ee914`、ruleset `24216773` 与 PR #264 首败。maintenance manifest
保持 `b38efdf...`；npm `11.19.1`、official registry 与 package-name-only
`vue / postcss-selector-parser / source-map-js` targeted update 两次逐字节重建同一 lock：

```text
candidate lock blob    297be5c0bcc30729c0f4c3f4322be74641b2a916
candidate lock SHA256  D9FBF89CA905EC2602B9956E986E24F74C38AAF4DE3EA960D1DBA3905EBD00A4
tracked scope          web/package-lock.json only
allowed projection     14 package entries
```

fresh install、14 files / 172 tests、lint、type-check/build、moderate audit 0 vulnerabilities 与 installed-tree
projection 成立。exact-version `npm update ...@version` 在写入前以 `EUPDATEARGS` 失败；一次 audit helper 漏传 base path
以 `KeyError` 失败。两者分别保留为 construction syntax 与 audit-harness setup failure，不被后续 PASS 覆盖。

本文只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDIT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_NOT_STARTED
M0_MAINTENANCE_DEPENDENCY_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

doc234 自己的 final-byte local gates、original PR、受保护 main 合入与 new exact-main 双门闭合后，只授权起草
dependency drift 最小合同。不得修改 dependency/maintenance/workflow/ruleset，创建 topic / PR，运行 dispatch，重开
#264，或启动 workflow bootstrap、release、consumer migration、Parse / Fact / Coverage / claim fidelity。

doc234 已经 PR #266 head `0bb60c0b51c1abcaa0877ffda6a62c9216fecc48` original Public CI
`37808837143` attempt 1 11/11、ordinary merge `main@7cf409940339d4068c3effd9e6d4deaca0c7861b`、new exact-main
Public CI `37811755532` attempt 1 11/11 与 Browser Smoke `37811755526` attempt 1 1/1。因此
`M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDITED` 已成为 qualified history。

## M10 maintenance dependency drift 最小合同（条件状态）

[文档 235](docs/235-m10-maintenance-dependency-drift-contract.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_DRIFT_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

合同冻结 exact maintenance tip `6ed18ae8...`、manifest/lock/workflow/ruleset coordinates、npm `11.19.1` + official
registry 的 package-name-only construction、完整 14-entry version/resolved/integrity/dependency-reference projection、
final lock blob/SHA、one-file scope、两次 deterministic reconstruction、local Workbench gates、ordinary PR/merge 与
candidate-head / exact-tip 两轮 `7/7 + 1/1` manual-dispatch witnesses。

本文自己的 final-byte local gates、original PR、受保护 main 合入、new exact-main 双门、fresh README / doc234 /
doc235 / milestones installed-product readback 与 independent source-byte reconciliation 全部闭合后，才是 qualified
contract candidate；随后仍须独立 docs-only freeze publication 完成同层资格链，合同才可标为 `FROZEN`。冻结后也必须
返回 CONTROL LOOP。不得在本文分支修改 dependency、maintenance、workflow、ruleset，创建 topic / PR，运行 dispatch，
重开 #252/#264，或启动 bootstrap、release、consumer migration、Parse / Fact / Coverage / claim fidelity。

doc235 已经 PR #267 head `8ed2f6f0e02e0a7a1e9f0d8006944e02eae1bb75` original Public CI
`37815845110` attempt 1 11/11、ordinary merge `main@933df49e61b8a5d3e3856afa648d27c1c21f5529`、new
exact-main Public CI `37818894300` attempt 1 11/11 与 Browser Smoke `37818894374` attempt 1 1/1。四份 fresh
installed-product readback、五份 public raw bytes 与 independent reconciliation 全部 PASS；manifest
`sha256_json=1bea6a3b59b452d7debda2b4778826a031e0ae2737e6523a19d55b02cac92960 /
sha256_bytes=ddbe3925167ae99b1babcc7ff47dcfbca2560bd3802378b31847f799f63ddda3`。因此 doc235 已成为
qualified contract candidate，仍未冻结。

## M10 maintenance dependency drift 合同冻结发布（条件状态）

[文档 236](docs/236-m10-maintenance-dependency-drift-contract-freeze-publication.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

本文保留候选 authoring transcription failure、readback 前非 Git CWD setup error 与 Playwright teardown warning；
后继 PASS 不覆盖这些身份。文档 235 第 1–11 节必须保持原字节；本发布只更新状态/导航并新增文档 236。

上述 target 只在文档 236 自己的 final-byte local gates、original PR Public CI、受保护 main 合入、new exact-main
Public CI + Browser Smoke、fresh README / doc235 / doc236 / milestones installed-product readback 与 independent
reconciliation 全部闭合后生效。冻结以后必须返回 CONTROL LOOP；dependency implementation、workflow bootstrap、
release、Parse / Fact / Coverage 与 claim fidelity 均未获授权。

doc236 已经 PR #268 head `a55c9bf5c66d8808cb728392b413249e0b158eea` original Public CI
`37823219183` attempt 1 11/11、ordinary merge `main@295afd0637385068e92b581c837249166bcf9919`、new exact-main
Public CI `37826445149` attempt 1 11/11 与 Browser Smoke `37826445084` attempt 1 1/1。四份 fresh installed-product
readback、五份 public raw bytes 与 independent reconciliation 全部 PASS；manifest
`sha256_json=162cabd962e192568c8405f65cb0486e1748038c9047a49858eda72dc97de847 /
sha256_bytes=e20d4e9aa9aacc07fe9b48603c722940ef0b35b37d6bc43388e2ba7fae806eed`。因此 dependency-drift contract 已经
`FROZEN`；implementation 没有由冻结自动开始。

## M10 maintenance dependency drift 资格发布（条件状态）

[文档 237](docs/237-m10-maintenance-dependency-drift-qualification-publication.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

one-file candidate `6efccfb89d362819d6deaaef1616fe221eae52b2` 只修改 `web/package-lock.json`；两个独立
exact-base worktree 逐字节重建同一 `D9FBF89C...00A4` lock，fresh npm 11.19.1 install、Workbench 14 files /
172 tests、lint、type-check/build、audit 0 vulnerabilities 与 exact 14-entry projection 成立。PR #269 的
candidate-head manual dispatch 为 Public CI `37831705180` attempt 1 7/7 和 Browser Smoke `37831710041`
attempt 1 1/1；ordinary merge `685b077203c4c9b74a1ef14649a4ee5f8d16d82c` 保持同一 tree/lock bytes，
maintenance-tip fresh dispatch 为 Public CI `37832912010` attempt 1 7/7 与 Browser Smoke `37832916430`
attempt 1 1/1。candidate/tip run 不互相借用。independent manifest
`sha256_json=105a44f4342f0496e76d4c056fbe7e91cc322a62cdf546e06894f08c5c8ab547 /
sha256_bytes=899b0571ea644ad99441af5ea6c9ebebf4510c187a6f6547b885241f2a8d1523`。

本文自己的 original PR、受保护 main 合入、new exact-main 双门、fresh README / doc235 / doc236 / doc237 /
milestones installed-product readback 与 independent reconciliation 全部闭合后，qualified target 才生效。最后门以前
workflow bootstrap 仍未开始。闭合以后必须从 exact maintenance tip 返回 CONTROL LOOP，重新审查 advisory surface、
并行 PR 与文档 223/224/225–227；不得自动启动 phase two、backport/release、consumer migration、Parse 或 claim fidelity。

## M10 maintenance workflow bootstrap 资格发布（条件状态）

[文档 238](docs/238-m10-maintenance-workflow-bootstrap-qualification-publication.md)只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

fresh workflow-only candidate `4b262eb24e101d8bfc7605b8a7a14ce0b15386fe` 只修改两个 workflow 的
branch filters；本地 static 四格逐字节一致、Python 四格各 347/347、Workbench 172/172 + lint/build/audit 0 与
Browser witness 均 PASS。PR #271 original Public CI `37844968094` attempt 1 为 7/7 SUCCESS；ordinary merge
`ebc5d7f5084b1a4dae3c3a211a4e82e78c6bbc78` 的 parents/tree 精确闭合，maintenance-tip Public CI
`37846426640` attempt 1 为 7/7 SUCCESS，Browser Smoke `37846426876` attempt 1 为 1/1 SUCCESS。

ruleset `24216773` 已独立读回为 active、无 bypass、禁止 deletion / non-fast-forward、要求 PR，并严格要求文档 223
列出的七个 status contexts；`strict=true`、`do_not_enforce_on_create=false`，branch-effective-rules 读回一致。

本文自己的 final-byte local gates、original PR、受保护 main 合入、new exact-main 双门、fresh README / doc223 /
doc237 / doc238 / milestones installed-product readback 与 independent reconciliation 全部闭合后，target 才生效。
闭合以后必须返回 CONTROL LOOP 重审 M1；0.12.3 产品改动、release、consumer migration、Parse 与 claim fidelity
都没有被本文自动启动。

## Core 0.12.3 发布与公开读回事实（条件状态）

[文档 239](docs/239-core-v0.12.3-release-readback-facts.md)只条件化发布：

```text
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_RELEASED
CORE_0_12_3_PUBLIC_READBACK_COMPLETE
CORE_0_12_3_MAINTENANCE_FROZEN
W1_REQUIRED_STARTER_LANE_MIGRATION_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

M1 candidate `4bae52e4127a964985f56a2219fc0c0a002a82b4` 经 PR #273 original Public CI 7/7、ordinary
merge `core-0.12-maintenance@a18da8ce40f7f9113bebef82f7fa5b3fcf334212`、exact-tip Public CI 7/7 与
Browser Smoke 1/1。M2 从该 exact tip 的 clean detached checkout 重建最终字节，创建受保护注释标签
`v0.12.3`，发布四项 create-new 资产，并保持非 Latest；匿名读回完成两套 Python wheel／sdist 四格与
public Starter 0.2.0 双 Python PASS／故意 FAIL、Catalog、Workbench 和 cleanup 链。

第一次敏感路径扫描 `FAILURE`、后继限定 evidence scope 的独立 `PASS`，以及此前所有 harness/setup
observation 均保留。本文自己的 final-byte local gates、original PR Public CI、受保护 main 合入、new
exact-main Public CI + Browser Smoke、fresh README／doc239／milestones／AGENTS installed-product readback 与
independent reconciliation 全部闭合后，target 才生效。

该发布不修改 runtime、workflow、timeout、retry、required-check、Release assets 或 frozen R1 contracts。闭合以后
必须返回 CONTROL LOOP 重审 W1；W1 没有由本文自动开始，Parse / Fact / Coverage、claim fidelity、Schema 与
persistence 继续未获授权。

## M10 required Starter lane 迁移资格发布（条件状态）

[文档 240](docs/240-m10-required-starter-lane-migration-qualification-publication.md)只条件化发布：

```text
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_RELEASED
CORE_0_12_3_PUBLIC_READBACK_COMPLETE
CORE_0_12_3_MAINTENANCE_FROZEN
W1_REQUIRED_STARTER_LANE_MIGRATION_QUALIFIED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

W1 candidate `ecc09bcb1d278a399cdc2685dcdb1f9110122283` 只修改 `.github/workflows/ci.yml` 的独立
`Starter PASS/FAIL golden path`：fixed public Core URL、SHA-256 与 installed version 从 0.12.2 更新到已读回的
0.12.3。Python matrix 中 Starter / Authoring 的 declared Core 0.12.2 compatibility lane 保持原字节；job 名、timeout、
retry、required-check、runtime 与 tests 没有变化。

PR #275 original Public CI `37868238477` attempt 1 为 11/11 SUCCESS。ordinary merge
`594f1b10c2e441b7e73bd607d4d3d2623afd3704` 的 tree 为
`59aa0c140d923160f92104316ef6200e8db4ee9e`；new exact-main Public CI `37870151887` attempt 1 为
11/11 SUCCESS，Browser Smoke `37870151759` attempt 1 为 1/1 SUCCESS。

fresh anonymous status readback 清除了 GitHub token 环境；public workflow raw bytes 与 exact Git blob 的 SHA-256
均为 `ad85f4755d6b5c5605806960a6a12788a403de99a17e13bab1b3a0ce2c6967e7`。PR、两条 run、11/11 job、
Release v0.12.3 与 wheel digest 被独立交叉核账；Python 3.10 / 3.13 normal / `-O` 四格 reconciliation
逐字节一致 PASS，SHA-256 为 `86dc70f0d5a7b31bb5c30a7f13baf163ca3a7f4e44e10ece4cdc7d8b29e8c32a`。

不受支持的 `gh release view --json isLatest` 读取、PR Artifact attachment identity 上限、两次 status
reconciliation setup/tooling error、托管 worktree 的非仓库调用与 unmanaged checkout attachment error 均保持自己的
非产品身份；后继 PASS 不覆盖它们。

本文自己的 final-byte local gates、original PR Public CI、受保护 main 合入、new exact-main Public CI + Browser
Smoke、fresh README / doc223 / doc239 / doc240 / milestones / AGENTS installed-product readback 与 independent
reconciliation 全部闭合后，target qualified state 才生效。

闭合以后必须返回 CONTROL LOOP，重新核对 exact main、并行 PR、文档 223 §9、文档 219–221、frozen Parse
contract 与现存反例，才可以判断 Parse private implementation 是否应获得新的 authorization。本文不自动授权
parser，不重开或复用 PR #243，不选择 persistence，不启动 Fact / Coverage、Schema、publisher 或 Bundle。

## R1 Parse fulfillment private implementation 实现授权发布（条件状态）

W1 资格发布 PR #276 head `4c4d4ceaef6c7e837f4cfd75fa4b7fb007efcd1e` 的 original Public CI
`37872621305` attempt 1 为 11/11 SUCCESS；ordinary merge 后的新 exact main 为
`35502aa2f605e5654327f9df81d9da7fe81f23cf`，tree 为
`98a951f93cf5b084fabc8d5c63b77d63aac3a2f8`。该 exact main 的 Public CI `37874646050`
attempt 1 为 11/11 SUCCESS，Browser Smoke `37874646030` attempt 1 为 1/1 SUCCESS。

README、doc223、doc239、doc240、milestones 与 AGENTS 使用六个 fresh Plan/session 取得 Core PASS；六份匿名 raw
source bytes 等于 exact Git blobs。两个正式 `ERROR` observation 原身份保留：doc223 首次 API
`COLLECTION_BUDGET_EXHAUSTED` / render network error，以及 AGENTS 首次 render network error / root cause
`UNKNOWN`。后继 fresh PASS 没有删除或解释它们。independent reconciliation 为：

```text
sha256_json  = 4cbb0d6454ba266e46635884f1d714980a4e21286006f8ab48f43c164f9694bd
sha256_bytes = 2e4b63e2ac0ba811303cb95ea2a5d50ed27a9766473fa23d9ab198efbb3017b1
```

第一次 Parse authorization 候选 PR #243 仍保持 original Public CI `36449716998` attempt 1 的 required Starter
`FAILURE`、`CLOSED / UNMERGED`，没有 rerun 或 authority 继承。文档 221–240 只闭合外部 consumer prerequisite；
`W1_REQUIRED_STARTER_LANE_MIGRATION_QUALIFIED` 使 CONTROL LOOP 可以从新 source state 重审授权，不自动授权 parser。

fresh audit-only probe 又发现旧 doc219 matrix Artifact 把 source literal `文本` 编码损坏为 `�ı�`。第一次
re-audit attempt 因 stdout UTF-8 decode error 保留为 `EVIDENCE_TOOLING_ERROR`；全新 attempt 固定 UTF-8 后，
CPython 3.10.6 / 3.13.13、normal / `-O` 四格 decision projection 相同，execution-cell canonical report 与旧摘要
逐字节相同。该差异属于 audit Artifact 输出编码，不是 product runtime 或 feasibility claim 反例；旧 digest 不改写。

[文档 241](docs/241-r1-parse-private-implementation-authorization-publication.md)因此只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

`PRIVATE_IMPLEMENTATION_ALLOWED` 只覆盖 doc219 A–H：exact input/classification/history 重验、ELIGIBLE denominator、
显式 exact CPython 3.10.6 runtime、per-subject one-shot child、contained worker/private canonical product、
semantic/lifecycle 分离、完整 reconciliation、application-owned product set 与 same-attempt one-shot continuation。
它不授权 current Fact projection/request/wire、Provider scheduling、persistence、public Schema/carrier、Fact
fulfillment、shared ledger、Coverage、Evidence/publisher/Bundle、CLI、其他顶层轨或 `DECLARED_CLAIM_FIDELITY`。

doc241 只允许 AGENTS、README、milestones 与新增 publication 四个文档文件。其 final-byte local gates、original
PR、受保护合入、new exact-main Public CI / Browser Smoke、fresh README / doc219 / doc241 / milestones
installed-product readback 与 independent reconciliation 全部成立以前，target marker 只是条件目标，runtime 继续
`NOT_STARTED / NOT_AUTHORIZED`。最后门闭合后仍须重新绑定新 exact main 并返回 CONTROL LOOP；不能按文档编号
自动开始实现。

## R1 Parse fulfillment private implementation 实现冻结候选（条件状态）

文档 241 后继 authorization publication 已在 PR #277 exact-main Public CI 的正式硬退出后停止；该 failure 只定位到
Python 3.10 `-O` combined service fixture，根因保持 `UNKNOWN`。文档 242 与 PR #278 独立拆分 test worlds、增加
phase observation 并修正 unittest cleanup 顺序，没有声称解释旧失败。#278 original Public CI、受保护合入、新
exact-main Public CI / Browser Smoke 与 doc241 剩余四份 fresh installed-product readback / reconciliation 闭合后，
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED` 才成为事实。

CONTROL LOOP 随后从 `main@026fabd74d7cc3fb9be1300e66f22fb8fd38fe7b` 重审 doc219 A–H。PR #279
head `2965fcfa1908d2e73e1600118493b69d5e37646a` 只新增 private Parse runtime/tests；ordinary merge
`26f21b5049dc87c889862fbcef2a12e76aed697e` 的 tree 为
`3d6cd1b783f7919ef3657e391d7d8c4de9f85fa5`，与 candidate tree 相同。PR original Public CI
`37966413820` attempt 1 为 11/11 SUCCESS；new exact-main Public CI `37969385811` attempt 1 为 11/11
SUCCESS，Browser Smoke `37969385827` attempt 1 为 1/1 SUCCESS。

实现只物化 exact input/classification/blob history revalidation、exact ELIGIBLE denominator、explicit
CPython 3.10.6 runtime capability、per-subject one-shot claim、contained worker/private canonical AST product、
semantic/lifecycle 分离、complete reconciliation、application-owned product set 与 same-attempt one-shot continuation。
五份匿名 exact-SHA source readback 均等于 Git blobs；manifest SHA-256 为
`d7fbe6441f095595ebf471319d85f0609321d5d70311f520625625c0cb0dcf2f`。

最终实现字节的四格 full Review Attention 为 CPython 3.10.6 normal / `-O` 各 `439 OK / skipped=1`，
CPython 3.13.13 normal / `-O` 各 `439/439 PASS`。第一次 3.10.6 `-O` full-suite observation 在未修改的
Relation `RD-016` 得到 `INTERRUPTED` 而非预期 `COMPLETED`，保持 `FAIL / ROOT_CAUSE_UNKNOWN`；后继 isolated
和 instrumented PASS 只作 diagnostics。attempt 2 被后继 hardening bytes supersede；attempt 3 才绑定最终实现。

[文档 243](docs/243-r1-parse-private-implementation-freeze-candidate.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_IMPLEMENTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_STAGES_A_B_C_D_E_F_G_H_EXACT_MAIN_VERIFIED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FREEZE_CANDIDATE
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

current Fact projection/request/wire、Provider scheduling/product-use enforcement、persistence、public Schema/carrier、
Fact fulfillment、shared ledger、Coverage、Evidence/publisher/Bundle、CLI、其他顶层轨与
`DECLARED_CLAIM_FIDELITY` 均未获授权。doc243 的 final bytes、original PR、受保护合入、新 exact-main 双门、
fresh README / doc243 / milestones installed-product readback、independent reconciliation 与后继独立最终冻结发布
全部闭合前，只能写成 `IMPLEMENTED / EXACT_MAIN_VERIFIED / FREEZE_CANDIDATE`，不能写成 `FROZEN`。

## R1 Parse fulfillment private implementation 最终冻结发布（条件状态）

文档 243 的 freeze candidate 经 PR #280 head `a230c61493c09e4d258adbf95f1056940ebda24c`、ordinary merge
`cd4aabb38e0352a7df9e5222606dbb96f65135e5` 与相同 tree
`35a92b37dae5571a77178d4945c626d66ff17f95` 进入受保护主线。PR original Public CI
`37977436359` attempt 1 为 11/11 SUCCESS；new exact-main Public CI `37980410283` attempt 1 为
11/11 SUCCESS，Browser Smoke `37980410250` attempt 1 为 1/1 SUCCESS。

README、doc243 与 milestones 三份 fresh anonymous installed-product readback 使用独立 Plan/session/output，均为
P1/P2 `COMPLETE`、三样本稳定、零 conflict/coverage reason/cleanup error/active stream，Core `PASS`。三份
anonymous raw source bytes 等于 exact Git blobs；independent reconciliation SHA-256 为：

```text
877ca46b98703994402bd0ab7e6f9a1789aa079b51e30ab12fad0f50eee87721
```

installed-environment preflight 在正式 Plan 创建前出现 Playwright shutdown pending-task warning；该 setup
observation 保留为 `NON_QUALIFYING_SETUP_WARNING`，没有 formal Evidence 或 Verdict 身份，也没有被后继 PASS
改写成未发生。

[文档 244](docs/244-r1-parse-private-implementation-freeze-publication.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_IMPLEMENTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_STAGES_A_B_C_D_E_F_G_H_EXACT_MAIN_VERIFIED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文自己的 final-byte local gates、original PR、受保护合入、new exact-main Public CI / Browser Smoke、fresh
README / doc244 / milestones installed-product readback 与 independent reconciliation 全部闭合前，frozen marker
只是 publication target。闭合以后也必须返回 CONTROL LOOP；Fact consumer correction、Provider scheduling /
product-use enforcement、persistence、public carrier、Fact fulfillment、Coverage 与其他顶层施工不会自动获得授权。

## R1 Parse → Fact consumer correction 最小合同候选（条件状态）

doc244 最后门闭合后，CONTROL LOOP 从 exact `main@b166dee05fe995b17b2f3bb557d75c2feb4f5493` 重建
Parse / Fact seam。fresh audit-only matrix 证明 application-owned Parse product set、complete reconciliation 与
same-attempt product access 已成为 qualified upstream truth；current Fact request 仍携带 Language Support eligible raw
source，并没有 Parse product-set / continuation binding。第一次 fixture 没有构造出声明的 rejected world，保持
`INVALID_AUDIT_FIXTURE_SETUP / product_observation=false`；fresh attempt 2 的四格 report byte-identical，现有五个
相关 test modules 四格各 86 项成立。

[文档 245](docs/245-r1-parse-to-fact-consumer-correction-contract.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_CANDIDATE
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

候选只冻结 post-Parse successor identity、从完整 reconciliation 导出的 ACCEPTED product membership、per-Provider
one-shot claim、product-only derivation authority、raw-source side-channel exclusion、multi-Provider 共享一份 Parse truth、
Fact output/continuation binding，以及 zero-accepted 的显式 normal-launch 阻断。该阻断不生成 empty FactSet、Fact
fulfillment 或 Coverage closure。

doc245 自己的 final bytes、original PR、受保护合入、new exact-main gates、fresh README / doc245 / milestones
installed-product readback、independent reconciliation 与后继独立 freeze publication 全部闭合以前，candidate marker
只是目标。runtime、Fact obligation/fulfillment、persistence、public carrier、Coverage 与 `DECLARED_CLAIM_FIDELITY`
均未获授权。

## R1 Parse → Fact consumer correction 最小合同冻结发布（条件状态）

PR #282 最终 head `56d6438459d4bbb1fad734eb875c85211895f3f5` 有两个 commits，最终 diff 只有
`AGENTS.md`、`README.md`、文档 245 与 milestones；文档 216 不在 diff，qualified historical bytes 保持不变。
edited-triggered workflow `38007576277` attempt 1 被 concurrency 取消并永久保留；fresh independent run
`38007576374` attempt 1 为 11/11 SUCCESS，它不是 cancelled run 的 rerun。

ordinary merge 后的 exact main 为 `3214586645c67156d5c498cbcd2ea5ed1a7d6b43`，tree
`9b25d6bd996a616ca9a9193db1b204ed0d29762e` 与 candidate tree 相同。该 exact main 的 Public CI
`38010089320` attempt 1 为 11/11 SUCCESS，Browser Smoke `38010089337` attempt 1 为 1/1 SUCCESS。

README、doc245 与 milestones 三份 fresh anonymous installed-product readback 使用独立 Plan/session/output，均为
P1/P2 `COMPLETE`、三样本稳定、唯一 candidate marker、零 conflict/coverage reason/cleanup error/active stream，Core
`PASS`。三份 public raw source bytes 等于 exact Git blobs；independent reconciliation SHA-256 为：

```text
db518b6da6d51e00097abb95baaae01081ff0e8694234852f3d6ca00df1e6fcf
```

formal Plan 创建前的 PowerShell wildcard static-check error、fresh venv 未预装 Playwright 的 package-version probe
error 与 Playwright shutdown warning继续作为 non-qualifying setup observations 保留。reconciliation PASS 后，外层首次
读取旧文件名以及未加引号的 `HEAD^{tree}` 又形成两项 non-qualifying operator inspection error；它们没有重跑或修改
reconciliation bytes，也不具有产品或合同失败身份。

[文档 246](docs/246-r1-parse-to-fact-consumer-correction-contract-freeze-publication.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

doc246 自己的 final bytes、original PR required checks、受保护主线合入、new exact-main Public CI / Browser Smoke、
fresh README / doc246 / milestones installed-product readback 与 independent reconciliation 全部闭合以前，frozen marker
只是 publication target。最后门闭合后必须返回 CONTROL LOOP；不得自动修改 Fact wire、启动 Provider child、选择
persistence、定义 Fact fulfillment / Coverage，或进入 `DECLARED_CLAIM_FIDELITY`。

## R1 Parse → Fact consumer correction private implementation 可行性审计（条件状态）

文档 246 的最后门已经闭合：PR #283 original Public CI `38012722163` attempt 1 为 11/11 SUCCESS；ordinary
merge 后的 exact main 为 `54eda4577e64cc3cf80eee464bd0ad116b710548`，tree
`546ef4db989d715572b935c8c631c9db697be969`；new exact-main Public CI `38014271058` attempt 1 为
11/11 SUCCESS，Browser Smoke `38014271039` attempt 1 为 1/1 SUCCESS。README 第一次正式 readback 因匿名
GitHub API `403 / remaining=0` 保持 `ERROR / NON_QUALIFYING`；fresh README #2、doc246 与 milestones 才取得
PASS。independent reconciliation SHA-256 为
`0454c821633ca742dfb9d93f11c62872b490a4b75748c01cf4989c48129d3182`。因此：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
```

均为当前事实。CONTROL LOOP 从该 exact main 重建 current runtime：`OwnedParseProductSet` 与 one-shot
`ClaimedParseContinuation` 已提供 qualified upstream Parse truth；historical Fact projection `/0.1` 与 wire `/0.2`
仍携带 raw `source_blobs`，没有 Parse product-set / continuation / product-use binding。旧 identity 不得增加字段后静默
改义。

[文档 247](docs/247-r1-parse-to-fact-consumer-private-implementation-feasibility-audit.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

审计确认 bounded private successor 可复用 original live `BudgetContext` / eligibility、Provider applicability、contained
execution、Fact canonicalization 与 multi-Provider join，但必须新增 versioned private consumer identity、application-owned
parent、完整 per-Provider membership、独立 one-shot claim、product-only worker request、candidate/product provenance admission、
required-child reconciliation 与 zero-accepted blocking。历史 `/0.1` projection / `/0.2` wire 保持原义。

raw bytes 只允许由 application 在 Provider boundary 以前，把 admitted Parse product source location 转换为 frozen Fact
所需的 exact byte anchor；worker 不得收到 raw body、source text、path loader、lazy handle 或 reparse authority。UTF-8-SIG、
CRLF、多字节 audit world 中，`ClassDef` exact raw byte range 为 `[23, 75)`。

仓库外 probe 四格 report 均为 2639 bytes、逐字节相同：file SHA-256
`c10d3da0e5874e6fdad1803405830aa9acfdfe3e1ba98829bc056a6021a30510`，report SHA-256
`dc0fdc26ddf0b80f0c4247ab9edc4c4eb3f0fb549c86b3bfe0359b34dfe4720b`。probe 证明两个 Providers
可共享一份 product-set semantics 而持有不同 child identity；one-shot concurrency 恰好一胜一拒；foreign candidate 被拒；
两 child 后原 context 仍 `RUNNING`、parent 仍 `ADMITTED`；all-rejected complete 形成
`BLOCKED_NO_ACCEPTED_PRODUCTS`，不产生 Fact terminal / FactSet。

第一次 targeted 3.10 normal command 指向不存在的 `tests.test_multi_provider_applicability`，保持
`TEST_HARNESS_IMPORT_SETUP_ERROR / product_observation=false / NON_QUALIFYING`。fresh attempt 2 的 Parse /
source-operation / Fact wire / controller / multi-Provider suite 四格各 122 项：3.10.6 normal / `-O` 各
`OK, skipped=1`，3.13.13 normal / `-O` 各 `122/122 PASS`。

本文只允许 AGENTS、README、milestones 与新增 doc247 四个文档文件。它自己的 final-byte local gates、original PR、
受保护主线合入、new exact-main Public CI / Browser Smoke、README / doc247 / milestones fresh anonymous
installed-product readback 与 independent reconciliation 全部闭合以前，feasibility 只能是 candidate。闭合后最多成为
`FEASIBILITY_AUDITED` qualified history；runtime 仍继续 `NOT_STARTED / NOT_AUTHORIZED`，并须返回 CONTROL LOOP，
另行决定是否创建独立 docs-only implementation authorization publication。

后继最多审计/授权 doc247 A–J private stages。Fact obligation universe / fulfillment、zero-member FactSet、persistence、
public carrier、Evidence/Bundle、ReviewSliceSet/Coverage、CLI/Workbench/Core 与 `DECLARED_CLAIM_FIDELITY` 均未获
授权。最后门闭合后也必须返回 CONTROL LOOP，不得按文档编号自动开始 runtime。

## R1 Parse → Fact consumer correction private implementation 授权发布（条件状态）

文档 247 已闭合自己的资格链：PR #284 original Public CI `38079982368` attempt 1 为 11/11 SUCCESS；ordinary
merge 后的 exact main 为 `fca688e399af2b24776e23bf490cb6e4b589880f`，tree
`285d2a46776be1f1d380c570b3f83f401819889c`；exact-main Public CI `38081660490` attempt 1 为 11/11
SUCCESS，Browser Smoke `38081660497` attempt 1 为 1/1 SUCCESS。README、doc247 与 milestones 以三个独立
Plan/session/handoff 完成匿名 exact-SHA installed-product readback，P1/P2 均 `COMPLETE`、Core 均 `PASS`；三个
public raw 文件逐字节等于 Git blobs。independent reconciliation SHA-256 为
`4a34719d1a1116760b5fe4fb659b93151848ce7f4a3d5a686d9b011003bfcd19`。

因此 `R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED` 已是 qualified
history，但不是 runtime authority。setup 阶段的 Windows `rg` wildcard、harness replacement、匿名 API 额度耗尽、
direct DNS 与两次 Playwright shutdown warning 共六项 observation 继续保留为 `NON_QUALIFYING`；它们发生在正式
Plan 前，没有被后继 PASS 覆盖或解释成产品失败。

[文档 248](docs/248-r1-parse-to-fact-consumer-private-implementation-authorization-publication.md)只条件化发布：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文自己的 final bytes、original PR、受保护合入、new exact-main gates、README / doc247 / doc248 / milestones
fresh installed-product readback 与 independent reconciliation 全部闭合以前，`PRIVATE_IMPLEMENTATION_ALLOWED` 只是
target marker，runtime 继续 `NOT_STARTED / NOT_AUTHORIZED`。

最后门成立后也只能从新 exact main 返回 CONTROL LOOP，重新确认 doc247 A–J 仍是最小合法问题，才可创建单用途
implementation branch。Fact obligation universe / fulfillment、zero-member FactSet、persistence、public carrier、
Evidence/Bundle、ReviewSliceSet/Coverage、CLI/Workbench/Core 与 `DECLARED_CLAIM_FIDELITY` 继续未授权。

### R1 Parse → Fact consumer correction private implementation 冻结发布（条件状态）

实现 [PR #287](https://github.com/NoctilumeDev/VeriTrail/pull/287) head `ab718cc6b4003a60de2a2707b50f71d0ff942690` 经 ordinary merge 进入
`main@d9e6ce3021c1981c52ddafa5009568ef900dcac6`，tree `db5fe21ab4536ed67df6ed96a739e50610beafaf`。原始 PR Public CI `38116549854` 与 exact-main
Public CI `38149116073` 均 attempt 1 / 11 of 11 SUCCESS；Browser Smoke `38149116151` attempt 1 /
1 of 1 SUCCESS。README/doc249/milestones 三个独立 anonymous installed-product readback 均 PASS，独立 Core/source-byte
reconciliation `b787eba23c6322a910663540fd12f5e102d24f4b53102334f7bde11f8fd5cbf8` PASS。首轮测试定位失败、readback setup 网络错误、全部旧正式 ERROR 保持历史身份。

[文档 250](docs/250-r1-parse-to-fact-consumer-private-implementation-freeze-publication.md)仅条件化发布：

```text
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_IMPLEMENTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_STAGES_A_B_C_D_E_F_G_H_I_J_EXACT_MAIN_VERIFIED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

doc250 的 final-byte local gates、original PR、protected merge、新 exact-main 双门、fresh README/doc250/milestones
product observations 与 independent reconciliation 全部闭合以前，FROZEN 只是 target。固定 closed worker 不等于
第三方 filesystem sandbox；observation 保存 terminal/frame 原字节，closure document 以摘要绑定。historical Fact
controller 仍保持 raw-source wire 原义；Fact fulfillment、persistence、public carrier 与 Coverage 未获施工权。
最后门闭合后必须重新返回 CONTROL LOOP，不能自动开始下一 seam。

### R1 Fact projection fulfillment 当前状态再审计（候选）

doc250 最后门已在 `main@f35d69b337b1961c9e9b54243097250cb962a582` 闭合：exact-main Public CI `38153642974`
attempt 1 为 11/11 SUCCESS，Browser Smoke `38153642954` attempt 1 为 1/1 SUCCESS；三个 fresh installed-product
readback/Core PASS 与 independent reconciliation
`e92e0bf7afd9d5acb184016f751d5288a56e901e67e292c1629f99d8e6b9bfe4` PASS。
README #1 正式 ERROR 保留；后继 fresh Plan 的可见 marker 不覆盖旧观察。private consumer A–J freeze 已生效。

[文档 251](docs/251-r1-fact-projection-fulfillment-current-state-audit.md)仅认领 docs-only current-state audit。doc195 的
“无 AST carrier”继续是旧 world 历史，不能作为当前前提。当前 Profile 五种 Fact 的结构可从 admitted canonical
product 检查，但完整 semantic input 还需要 sealed Policy module mapping 与 exact path/anchor history。
current worker/admission 仅闭合 MODULE/CLASS conformance；合法空报告不证明完整 fulfillment。

```text
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_CURRENT_STATE_AUDIT_CANDIDATE
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_NOT_STARTED
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

文档 251 自己的 local/original PR/protected merge/exact-main dual gates/fresh product readback/independent reconciliation
闭合前不得升级审计状态。其长期依赖计划不授予后继施工权；CUMULATIVE 不决定 per-kind/node fulfillment，Provider
不得从 outputs 倒定义 denominator。后继若改变 frozen projection/admission，须显式限定 successor/version 边界；不在
本轮改 runtime、Schema、persistence、Fact consumer、Coverage、Evidence/Bundle、CLI/Workbench/Core 或 CLAIM_FIDELITY。

### R1 Fact projection universe / fulfillment 最小合同（候选）

doc251 已经通过 [PR #289](https://github.com/NoctilumeDev/VeriTrail/pull/289) 进入
`main@07e3e90e6b7976c660ae7643b0cde79cb9b97a8a`。original Public CI `38166052364` 与 exact-main Public CI
`38167806238` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38167806265` attempt 1 / 1/1 SUCCESS。
三个 fresh README/doc251/milestones product observations 均 PASS，independent reconciliation
`d788554a27dbeb6f5c0d02fb19938e3c8e228c5b1d2e5084b792d35451677ad2` PASS。旧 CANCELLED/ERROR、preflight warning
与 live diagnostic-log snapshot correction 保留；旧候选 marker 不倒改这份 qualified history。

[文档 252](docs/252-r1-fact-projection-universe-and-fulfillment-contract.md)只认领 docs-only 最小语义合同：完整
admitted products、sealed mapping/Profile 与 exact identity/anchor history 形成 application-owned U/E；每个 applicable
closed Provider 负责完整全集，required/optional lifecycle 分开。fulfillment 是真实 child history 与独立 expected/output
对账共同成立，不认证内部逐项执行，不要求逐项 receipt。normalized keyword name 可以 grammar ACCEPTED 但 Fact
属性不可表示；保留 obligation 与 typed projection 阻断，不改 Parse truth 或缩小 denominator。

```text
R1_FACT_PROJECTION_FULFILLMENT_CURRENT_STATE_AUDITED
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_CANDIDATE
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

未来 consumer `/0.2` 与独立 private protocol 必须显式受审；不修改 frozen `/0.1`，不扩大旧证据。zero accepted 继续
阻断 normal Fact child/FactSet/continuation；已知空 U 不等于 Fact-stage closure 或 Coverage。所有旧 runtime/tests/
Schema/fixtures/contracts 与架构资产不变。doc252 的 local/original PR/merge/new-main 双门/fresh product readback/
independent reconciliation 只取得 contract candidate history；还需独立 freeze publication，再回 CONTROL LOOP 审
feasibility/implementation authorization。不得启动 runtime、public carrier、persistence、Coverage 或 CLAIM_FIDELITY。

### R1 Fact projection universe / fulfillment 最小合同独立冻结发布（条件目标）

doc252 候选已由 [PR #290](https://github.com/NoctilumeDev/VeriTrail/pull/290) final head
`63f0f31028416587f7db91358485fae71e6a0af2` 合入 `main@da11ca26eef6739c3fd7560fe29b67e2618f4d1a`；
受审与 merge tree 同为 `05a0ae561ccec269368c1c5b230d03b946816f36`。original Public CI `38172220489` 与
exact-main Public CI `38174088676` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38174088675` attempt 1 /
1/1 SUCCESS。fresh README/doc252/milestones observations 均 Core PASS，independent reconciliation
`ce57ba2d36b88795fb556669a69d438e94b09c910fef262a760e609bc8e0fec3` PASS；候选资格只形成 qualified history。

[文档 253](docs/253-r1-fact-projection-fulfillment-contract-freeze-publication.md)只认领独立 status publication：
保留 doc252 全部字节与候选 marker，不改 frozen projection / Profile / Policy / public identity 或旧 consumer `/0.1`。
自己的 local/original PR/protected merge/new exact-main dual gates/fresh README/doc253/milestones observations /
independent reconciliation 全部闭合后，以下目标才生效：

```text
R1_FACT_PROJECTION_FULFILLMENT_CURRENT_STATE_AUDITED
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

此前仍为 qualified candidate，之后也不自动获得 feasibility 结论或 implementation authority。重新回 CONTROL LOOP
读取 doc252 §13 与 current runtime，只审仍成立的最小后继问题。runtime、Schema、public carrier、persistence、Coverage、
Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag/Release 均不启动。
候选 README marker-selection setup finding、旧 ERROR/CANCELLED/UNKNOWN 与其他失败历史保留；diagnostics 不取得
formal qualification，最终核账机械枚举全部 retained observations，不写死错误数量，不跨 SHA 拼接资格。

### R1 Fact projection / fulfillment 私有实现可行性审计（候选）

doc253 自己的资格链已闭合在 `main@c65a9f7d915ea96b22c3ca4d641c12a09664b7ac`：PR #291 original Public CI
`38177038668`、exact-main Public CI `38191557863` 均 attempt 1 / 11/11 SUCCESS，Browser Smoke `38191557889`
attempt 1 / 1/1 SUCCESS；fresh README/doc253/milestones 均 P1/P2 COMPLETE / Core PASS。independent reconciliation
`ff035c7129dd22d796b321124ad3082bd31ee1304502fe6b9b564eb06dbac22f` PASS，132-artifact closeout
`d416156f4185977ee60d2f788efa48a019a7bb22897a4d35c3d68b111c8e4e29` 保留全部旧诊断与历史身份。

[文档 254](docs/254-r1-fact-projection-fulfillment-private-implementation-feasibility-audit.md)另经人工阶段授权，只审
六条 private feasibility seam。现有 `/0.1` MODULE/CLASS 能力不是完整五类 fulfillment，也不因本审计升级。
final four-cell product corpus 为 9 worlds/cell、44 actual reference Parse children、0 actual Fact children；identifier
corpus 是全部 `0x110000` codepoints 的四类谓词与 11 个 component gold，不是所有字符串/未来宿主的通用证明。

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

首个 product block 的 UNCLASSIFIED-disposition fixture 错误、11 个旧 Parse children 和 52 份 artifacts 保留；新 v2
使用 source_class=UNCLASSIFIED，不改产品。synthetic verifier v1 把 optional unsafe release 错当 ordinary gap；该模型
counterexample 保留，v2 增加 shared safety/any-source unsafe release gate。不能把模型或 stateless validator 变成 live
authority，也不能以旧 `/0.1` 原始证据替新 `/0.2` 实现背书。

本文自己的 local/original PR/protected merge/exact-main dual gates/fresh README/doc254/milestones observations /
independent reconciliation 全部闭合前，feasibility 仍为 candidate。闭合后仍须返回 CONTROL LOOP，单独取得 explicit
implementation authorization；本轮不发布 ALLOWED，不改 runtime/tests/Schema/Profile/Policy/旧合同/架构资产，不选择
persistence，不启动 Fact→Coverage、ReviewSliceSet/Coverage、public carrier、Evidence/Bundle/publisher、CLI/Workbench/
Core、CLAIM_FIDELITY、tag 或 Release。

### R1 Fact projection / fulfillment 私有实现授权发布（条件目标）

doc254 的资格链已在 `main@c9de08409ac0fda9bb1da9638d54077a4914cad0` 闭合：PR #292 head
`816eda40ccef21db510b535d4a2a277addc46271` 与 merge tree 均为 `97ed9b306166f54f88e9f5b3f6096cfad1909a02`。
original Public CI `38200446340`、exact-main Public CI `38201901095` 均 attempt 1 / 11/11 SUCCESS；Browser
Smoke `38201901082` attempt 1 / 1/1 SUCCESS。fresh README/doc254/milestones 各自 P1/P2 COMPLETE、Core PASS，
independent reconciliation `d8ae2060f3a44c9f775a482a8bdca152423b47bf83163faee2961533fd516b5c` PASS；125-artifact
closeout `b6653116656bb0f8e1c2fcce6084ec4f3a13fcc59de318dd92974b028d600ea3` 保留正式/非资格历史。

`FEASIBILITY_AUDITED` 已生效；doc254 的历史 candidate header 不改。本轮另获人工 docs-only 授权，仅由
[文档 255](docs/255-r1-fact-projection-fulfillment-private-implementation-authorization-publication.md)发布条件目标：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

doc255 final local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc254/
doc255/milestones observations/independent reconciliation 全部闭合以前，ALLOWED 仅作 target，实际 authority 仍
NOT_AUTHORIZED。四份观察必须属于本 publication 同一 merge SHA；历史 N 从 retained observations 机械导出。

最后门闭合后仍回 CONTROL LOOP，再判断完整 U/E、独立 `/0.2`、product-only worker、per-Provider claim/lifecycle/
内容与双向 provenance、required/optional/shared safety join、negative blocking 与 same-attempt continuation 是否仍为
最小合法施工面。FPFCT-001–024 必须直接攻击实现；finite model 或旧 `/0.1` PASS 不替代真实 child/fulfillment。
禁止 raw reparse、expected-answer 补写、Provider 自定 denominator、fresh BudgetContext、静默改 frozen identities。
本发布只改四份文档，doc252/doc254 和全部其他 tracked bytes 保留；persistence、zero-member Fact-stage closure、
Fact→Coverage、ReviewSliceSet/Coverage、public carrier/Schema、Evidence/Bundle/publisher、CLI/Workbench/Core、
CLAIM_FIDELITY、tag/Release 均未授权。fixed closed worker 不等于通用 filesystem sandbox，首败与 UNKNOWN 不改写。

### R1 Fact projection / fulfillment 私有实现候选

doc255 在 `main@46eb3ab55bdeea17cd5e6bd2bf614a05b109c0f6` 的最后门已闭合；4 qualifying PASS + 1 formal ERROR
原身份保留，independent reconciliation `ebffc0fcdda1d1072ef7539a9f7413592c5732644ff00924f534057d68413644` PASS，
177-artifact closeout `5d681ade0bbfd1dbf426b8ceebed90dffb209d405b67b0dfc48ad4f3127495c3`。
新的 CONTROL LOOP 与明确阶段确认允许 doc255 A–J 私有实现；当前是
[doc256](docs/256-r1-fact-projection-fulfillment-private-implementation-candidate.md)候选，尚未 exact-main verified/frozen。

独立 `/0.2` 只在私有层构造完整 application-owned U/E、product-only closed worker、每 Provider one-shot/lifecycle/
完整内容与双向 provenance、required/optional/shared-safety reconciliation 和 same-attempt continuation。旧 `/0.1`、
frozen contracts、public exports、Schema/Profile/Policy/workflows 字节不变。FPFCT-001–024 的 gold/mutation 与真实
bounded child 是本实现 witness，不能扩权。初始化首败、mapping fixture 首败及上游 non-success/UNKNOWN 保留。

最终字节须经过 doc256 §6 的完整门；original PR、精确 head 合并、新 exact-main、fresh README/doc256/milestones
读回与独立对账分别取证。FROZEN 仍需独立发布。persistence、zero-member Fact closure、Fact→Coverage、public
ReviewSliceSet/Coverage、Schema/carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag/Release
继续禁止；若反例击穿前提，保现场归层，仅重开最小 seam，不修改 oracle 来获得 PASS。

### R1 Fact projection / fulfillment 私有实现独立冻结发布（条件目标）

doc256 候选已由 [PR #295](https://github.com/NoctilumeDev/VeriTrail/pull/295) final head
`daf11eb76a33b4522da2b2f0fc14f0ec280e5f1f` 合入
`main@b11eb0bd857f87ed7c4da4b9b74b14fcaac884d4`；受审与 merge tree 同为
`6a807fea6ab9eed98320cc92ef73db3dfa4f3271`。original Public CI `38274256272` 与 exact-main Public CI
`38278181528` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke `38278181407` attempt 1 / 1/1 SUCCESS。candidate
fresh README/doc256/milestones observations 均 P1/P2 COMPLETE / Core PASS，independent reconciliation
`47a3069eb291c3cf69f59ce54454310c78d21df0ee20d807b0f0e8408cb4edcd` PASS，finite closeout
`ffb3ad21d42d7b45c84533d40efbe7a26a611243c996a00ab2cd5f5db4c9c137` 保留全部历史身份。

[文档 257](docs/257-r1-fact-projection-fulfillment-private-implementation-freeze-publication.md)只认领独立 docs-only
status publication：保留 doc252–256、六个 private modules、`test_fact_fulfillment.py` 与全部其他 tracked bytes；只在
自己的 final local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc257/
milestones observations/independent reconciliation 全部闭合后发布：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

在最后门闭合前，branch 中的 `FROZEN` 只是条件 target。candidate readback 不能替代本 publication 的 fresh
Plan/session/Evidence，diagnostic 不计入资格，formal non-success 必须保留原 identity，历史 N 从 observations 机械导出。
冻结生效后仍必须返回 CONTROL LOOP；不得自动启动 persistence、zero-member Fact-stage closure、Fact→Coverage handoff、
Relation/Slice public assembler、ReviewSliceSet/seven-stage Coverage、public Schema/carrier、Evidence/Bundle/publisher、
CLI/Workbench/Core、CLAIM_FIDELITY、tag、Release 或任何后继合同/runtime。

### R1 Fact → Coverage same-attempt handoff 当前状态审计（候选）

doc257 的最后门已经在 `main@50ab803671674b8a88245480aae06b5ba8fec526` 闭合。PR #296 original Public CI
`38285546808` 与 exact-main Public CI `38316924237` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38316924154` attempt 1 / 1/1 SUCCESS。fresh README/doc257/milestones 均 P1/P2 COMPLETE、Core PASS，
independent reconciliation `ee148157be125b140dc0f6a8918977f93227dd14e4afbd875a2f8a415e62dbed` PASS；
120-artifact closeout 为 `6d80880795b216d1cefce5dcead550ebe98b3f24bf0d8a2da864e28b9e7ecf1d`。
因此 Fact private implementation FROZEN 已生效；历史条件 header 不修改。

[文档 258](docs/258-r1-fact-to-coverage-same-attempt-handoff-current-state-audit.md)只认领新的 docs-only current-state
audit。六个 finite worlds 证明 closure 已保留 U/E、Parse partition、完整 Provider responsibility/lifecycle、
FactSet/absence 与 negative blockers；但 current normal continuation 只暴露 FactSet 与原 BudgetContext，negative worlds
没有 normal continuation。FactSet/output 不能反推完整责任历史，unrepresentable U 也不能总映成 total Fact IDs。

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

四格 audit semantic report 各 20,353 bytes 且 SHA-256 同为
`14110c2180d6067ed9f0d8d74aba1c8f82f944d140db15233c7bc6c1c82c212a`；current Fact fulfillment tests
四格各 28 reported / 27 passed / 1 skipped，skip 的 actual-child witness 不能写成实际通过。fixture shape 首败、
identity-normalization finding、outer wait/setup errors 均保留原身份，不归为产品失败。

本文自己的 local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc258/
milestones readback/independent reconciliation 闭合以前只保持 candidate。它不授权 handoff 合同/runtime、
ReviewSliceSet/Coverage、zero-member FactSet、Schema/carrier、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、
CLAIM_FIDELITY、tag 或 Release。闭合以后返回 CONTROL LOOP；只有 seam 仍成立时，才可另行审查最小 handoff 合同。

### R1 Fact → Coverage same-attempt handoff 最小合同候选

doc258 的资格链已在 `main@ec0f7e08f45be57754e0cfe86f000de7ac045e4b` 闭合。PR #297 original Public CI
`38322762959` 与 exact-main Public CI `38325172987` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38325172966` attempt 1 / 1/1 SUCCESS。fresh README/doc258/milestones 均 P1/P2 COMPLETE、Core PASS；
independent reconciliation attempt 1 的 proof-facility `KeyError: publication_world` 保留，最小 key correction 后 attempt 2
`97056811f6e0146cb36aeec710a9c1a0a0b4d2e3d07c3b5497b56d7d3b5b47ad` PASS，136-artifact closeout 为
`353f00e0818e4d9fa72863fc19a5e2a48e17f959d7f5afb5482bc6e692bb1e87`。因此 current-state audit 已成为
qualified history；历史 candidate header 不改。

[文档 259](docs/259-r1-fact-to-coverage-same-attempt-handoff-contract.md)只认领 docs-only minimal semantic
contract：handoff function 为 `r1-fact-to-coverage-handoff/0.1`，authority owner 是 exact upstream owned history 上的
application。合同要求 total negative branches、完整 U/E/Provider/lifecycle history、unrepresentable U slot 无损保留、
same-attempt one-shot claim 与严格 authority ceiling。FactSet、digest、normal continuation、fresh equal-limits Context 或
serialized bytes 均不能自领 handoff authority。

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

本合同不把 handoff 解释成 Coverage stage/status。Coverage 0.1 无法直接表达没有合法 Fact ID 的 U slot 时，必须停下来
审查最小 successor/Schema，不得用 arbitrary digest、`DERIVATION_ERROR` 或 `UPSTREAM_DENOMINATOR_UNKNOWN` 掩盖。
interrupted/unsafe world 若不能从 frozen parent/observation/stop history形成可验证 terminal source，同样 fail closed，不得
制造 normal closure。

本文自己的 final local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc259/
milestones readback/independent reconciliation 全部闭合前只保持 contract candidate；之后还需独立 freeze publication。
即使合同冻结，也不自动授权 handoff runtime、persistence、ReviewSliceSet/Coverage、public Schema/carrier、Evidence/
Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。

### R1 Fact → Coverage same-attempt handoff 最小合同独立冻结发布（条件目标）

doc259 已完成候选资格链。PR #298 final head `fae10532d7781adb556956724ef6c532b2f74b66` 的 original Public CI
`38344285489` attempt 1 为 11/11 SUCCESS；ordinary merge `main@2a97b5cd6cdf0598db07a26d3640e4408f84713b`
的 Public CI `38626280347` attempt 1 为 11/11 SUCCESS，Browser Smoke `38626280577` attempt 1 为 1/1 SUCCESS。
fresh README/doc259/milestones 均 P1/P2 COMPLETE、Core PASS。

independent reconciliation attempt 1 的 proof-facility `KeyError: changedFiles` 保留；最小 metadata-shape 修正没有修改
原 Plan/session/product outputs。attempt 2
`9f346117c05bdffd031092ddc689ecabfa8a7446701fa8122fbcf18f29949395` PASS，150-artifact closeout 的
candidate qualification SHA-256 为 `3109b2a6a446ed6323db67df40b2579205bc7763bfc55d7cd4e1ec1eb6af297b`。
doc259 full-file SHA-256 保持 `afc40f1226325ac97297863bc99df4f837a37b1617d1c51e5c038cc0f9f39524`。

[文档 260](docs/260-r1-fact-to-coverage-handoff-contract-freeze-publication.md)只条件化发布：

```text
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_CURRENT_STATE_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

publication tracked scope 只能是 README、AGENTS、milestones 与新增 doc260；doc259、runtime、tests、workflows、Schema、
Profile、Policy、fixtures、identity vectors 与架构资产保持 base 字节。本文的 original PR、单独批准 exact-head merge、
new exact-main dual gates、fresh README/doc260/milestones installed-product observations 与 independent reconciliation 全部
闭合以前，`CONTRACT_FROZEN` 只是 target marker。

最后门闭合后必须返回 CONTROL LOOP，重新审查 handoff private feasibility；不得自动启动 runtime、persistence、
Coverage item/disposition mapping、ReviewSliceSet/Coverage、public carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、
CLAIM_FIDELITY、tag 或 Release。

### R1 Fact → Coverage same-attempt handoff private implementation 可行性审计（条件状态）

doc260 的最后门已经在 `main@bf6bedb002c1a9a4ade7e64b385be742dcf012fd` 闭合。PR #300 original Public CI
`38639738028` 与 exact-main Public CI `38643028967` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38643028948` attempt 1 / 1/1 SUCCESS。fresh README/doc260/milestones 均 P1/P2 COMPLETE、Core PASS；
independent reconciliation `ddf865aac99f1af7cf27dc69f73c04bdc251b88e02e5eb05b0d3fdfbca5358e2` PASS，
149-artifact closeout 为 `604f69a6784b36861507aa2020247dd5f5967b0756553884a662fc44de6be6a9`。因此
handoff contract FROZEN 已生效；proof-facility count/seal 首败保留原身份。

[文档 261](docs/261-r1-fact-to-coverage-handoff-private-implementation-feasibility-audit.md)只认领 docs-only private
feasibility audit。current owned graph 已保留完整 Parse partition、U/E/blockers、Provider requiredness/lifecycle、exact
observations、FactSet/absence、original Context 与 attempt identity；七个 finite worlds 和 reversed/equal-semantics worlds
支持一个独立、copy-owned、same-attempt one-shot handoff successor。legacy FactSet-only continuation 不能扩权；safe negative
terminal eligibility 必须独立受审，unsafe/interrupted只能 no-claim fail closed。

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

最终 v4 matrix 的 CPython 3.10.6 / 3.13.13、normal / `-O` 归一化 bytes 相同，SHA-256 为
`22cc3c8ac29d31a891711fc7b8c49cd5b5c51e8b17805197751243cc7880462e`。首个 matrix 的
`KeyError: provider_descriptor` 保留为 audit read-path setup failure；后续 tuple/member identity 和 pre/post claim
refinement 不改产品或 oracle。unchanged regression 四格各 `89 reported / 87 passed / 2 skipped`，skip 不算实际通过。

本文自己的 final local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc261/
milestones readback/independent reconciliation 全部闭合以前只保持 candidate；闭合后最多成为 `FEASIBILITY_AUDITED`。
随后仍须返回 CONTROL LOOP 并另行取得 explicit implementation authorization。不得在本轮修改 runtime/tests/Schema、
选择 persistence、映射 unrepresentable U 到 Coverage、启动 ReviewSliceSet/seven-stage Coverage、public carrier、
Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。

### R1 Fact → Coverage same-attempt handoff private implementation 授权发布（条件目标）

doc261 已在 `main@b6268103dc838706a8d2e8c9a2d4711a7d37a4d6` 完成自己的资格链。PR #301 original
Public CI `38647492297` 与 exact-main Public CI `38650640469` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38650640457` attempt 1 / 1/1 SUCCESS。fresh README/doc261/milestones 均 P1/P2 COMPLETE、Core PASS；
independent reconciliation
`98860543daa467c235ce25acd69e414a0e350ca6354282fe32ead71b7e576188` PASS，135-artifact closeout 为
`da2ee0a7f2f12a0dc388cb207a2d89abfb604a72aee2f8f496b57f188da99640`。因此 doc261 已成为
`FEASIBILITY_AUDITED` qualified history；它的历史 candidate header 不改。

[文档 262](docs/262-r1-fact-to-coverage-handoff-private-implementation-authorization-publication.md)只条件化发布
doc261 §10 的 A–J private implementation authority：exact owned Fact history revalidation、total semantic
projection、canonical ordering、normal/safe-negative source qualification、与 legacy continuation 互斥的 closure-level
one-shot claim、固定 application-owned consumer、copy-owned value、unsafe/interrupted no-claim、same-attempt hardening
与 FCHC-000..011 direct falsifiers。

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

这些是 publication target。doc262 自己的 final local gates、original PR、单独批准 exact-head merge、new exact-main
Public CI / Browser Smoke、fresh README/doc261/doc262/milestones readback 与 independent reconciliation 全部闭合以前，
`ALLOWED` 不生效，runtime 仍 `NOT_STARTED / NOT_AUTHORIZED`。本发布不修改 runtime/tests/Schema、doc259–261、
Profile/Policy/fixtures，也不选择 persistence、映射 unrepresentable U、启动 Coverage item/disposition、ReviewSliceSet/
seven-stage Coverage、public carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。

授权生效后仍须返回 CONTROL LOOP，重新绑定新 exact main；只有 A–J 仍是最小合法 seam 时才可另建 implementation
branch。`PRIVATE_IMPLEMENTATION_ALLOWED` 不证明实现已经发生、完成、合入、冻结或拥有 Coverage authority。

### R1 Fact → Coverage same-attempt handoff private implementation 候选

doc262 已在 `main@a174ee739a39a8dda956ff9a8ea899c569a78cf3` 完成自己的最后门。PR #302 final original
Public CI `38657864511` 与 exact-main Public CI `38660718150` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38660717996` attempt 1 / 1/1 SUCCESS。较早 concurrency-cancelled run `38657826171` 与两个 formal ERROR 保持原身份；
四份 fresh README/doc261/doc262/milestones 均取得 qualifying PASS。independent reconciliation
`e5f41ff354a491d7927703d16d021e0add5ddcb3f7bb1519dbf58e15668fd269` PASS，216-artifact closeout 为
`a69cf12295b3018042e100321a9c6f1305ef5fec7a14973907d89272c96d3009`。因此 private implementation authority 已生效。

[文档 263](docs/263-r1-fact-to-coverage-handoff-private-implementation-candidate.md)只认领 doc262 A–J 的 bounded
private implementation：exact owned Fact history重验、`r1-fact-to-coverage-handoff/0.1` total projection、canonical
responsibility ordering、normal/safe-negative source qualification、与 legacy continuation互斥的 one-shot source、固定
application consumer、copy-owned value、unsafe/interrupted no-claim与 same-attempt hardening。

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

FCHC-000..011与replay/source-mutation falsifier保留normal、optional gap、zero denominator、all rejected、projection
blocked、required failure、unsafe/interrupted、foreign equal context与并发竞争。四格六世界去provenance semantic bytes
一致，SHA-256为 `182a1b233f5bdc4df3638b1e38c5ab38724931768f3c0999398cb15d25fa3a49`；exact request/
execution/terminal/frame bytes另行验证存在，不由semantic equality替代。

final-byte完整Review Attention的首个3.10 normal attempt在两个既有Slice H falsifier上得到
`CONTINUATION_UNAVAILABLE`；fresh两用例与完整Slice join模块均PASS，未改oracle/timeout/order的fresh full attempt 2亦PASS。
该首败保持`FULL_DISCOVERY_CROSS_MODULE_CONTINUATION_UNAVAILABLE / ROOT_CAUSE_UNKNOWN`，不被后继PASS覆盖，也不据此
宣称handoff产品、合同或既有Slice实现失败。

本文自己的 final local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc263/
milestones readback/independent reconciliation闭合以前只保持 implementation candidate；FROZEN仍须独立发布。不得选择
persistence、定义Coverage item/disposition或FACT_DERIVATION status、启动ReviewSliceSet/seven-stage Coverage、修改public
Schema/carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag或Release。

### R1 Fact → Coverage same-attempt handoff private implementation 冻结发布（条件目标）

doc263 候选已在 `main@83ad8f10b68f1d085b83310613c6f5cc06292d28` 完成自己的资格链。PR #303 original
Public CI `38702235329` 与 exact-main Public CI `38705035837` 均 attempt 1 / 11/11 SUCCESS；Browser Smoke
`38705035878` attempt 1 / 1/1 SUCCESS。fresh README/doc263/milestones 均 P1/P2 COMPLETE、Core PASS，public bytes
等于同一 exact main 的 Git blobs。independent reconciliation attempt 1 的祖先 closeout 文件名假设错误保留为
`RECONCILIATION_ANCESTOR_CLOSEOUT_FILENAME_SETUP_ERROR`；只修 proof-facility path 的版本化 attempt 2 PASS，SHA-256 为
`fa37b88dfc1007bb6eee8494ef5a372c3ab50564f78734ca7234e13f32d5da96`。144-artifact closeout 为
`d69d906750712846a82246ff09050e4a869ed95adc4db6c9760f95727816c767`。正式 observation history 为 3 PASS / 0
non-success；diagnostic 与 setup observations 保持非资格化。因此 doc263 已成为
`CANDIDATE_MERGED_EXACT_MAIN_READBACK_QUALIFIED` history，历史 candidate header 不改。

本 publication 的首个本地四格窄测试调用未绑定 repository `src`，各格均在 Markdown 模块导入时留下
`LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`；已执行的22项Schema与5项hygiene均PASS。fresh attempt 2只修调用方
`PYTHONPATH`，四格各31/31 PASS；测试、产品、文档语义与oracle未修改，首败不被后继PASS覆盖，publication最终字节仍由
自己的local qualification单独受审。

[文档 264](docs/264-r1-fact-to-coverage-handoff-private-implementation-freeze-publication.md)只条件化发布已资格化的 bounded
private implementation，不修改 doc259–263、runtime、tests、Schema、Profile、Policy、fixtures 或 corpus：

```text
R1_FACT_TO_COVERAGE_HANDOFF_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
```

这些是 publication target。doc264 自己的 final-byte local gates、original PR、单独批准 exact-head protected merge、new
exact-main Public CI / Browser Smoke、fresh README/doc264/milestones installed-product observations 与 independent
reconciliation 全部闭合以前，`FROZEN` 不生效。即使最后门闭合，也必须返回 CONTROL LOOP；不得自动选择 persistence、
定义 Coverage item/disposition、FACT_DERIVATION status 或 seven-stage join，不得启动 ReviewSliceSet/CoverageLedger、public
Schema/carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、tag 或 Release。

### R1 ReviewSliceSet / Coverage composition 当前状态审计（候选）

doc264 的最后门已经在 `main@20dd549d3f07f7b9185215eb3c8377dcd0f13a2c` 闭合。PR #304 original
Public CI `38715944983`、exact-main Public CI `38736844425` 与 Browser Smoke `38736844350` 均 attempt 1
SUCCESS，分别 11/11、11/11 与 1/1。fresh README/doc264/milestones 均 P1/P2 COMPLETE、Core PASS；independent
reconciliation `830fa170391e1ae5689538337d4d62ebf47d550b44de5633a175830445b70108` PASS，128-artifact
closeout 为 `a5898cce497e89dbb95e86fd5286a8e39719705273ed9cdc02fe55a499050516`。因此 handoff private
implementation 已是 frozen upstream。

[文档 265](docs/265-r1-review-slice-set-coverage-composition-current-state-audit.md)从该 exact main 复核 public 0.1
identity/vocabulary、current private object graph 与 seven-stage join。current Relation/Slice path 不消费新 handoff，而是在独立
BudgetContext/attempt 中重跑 historical Fact source operations；production source 尚无 handoff downstream consumer。相同
Snapshot/Profile/Policy、Fact semantics 或 digest 不能把两套 histories 拼成一条 authority history。

projection-blocked world 的 U=3/E=2 slot subject digest 可按 doc120 精确复算并通过现有 `FACT CoverageItemRef` shape，
所以 identity 不要求先造新 item kind；但 `UNREPRESENTABLE_EXPECTED_FACT` 不在 Coverage 0.1 reason 闭集，shape-valid ref
不授予 mapping/disposition authority。重跑 `SCQ-001` 仍得到 Snapshot 1项、首 stage 0项、下一 stage 1项、Schema与局部
方程全绿且 overall COMPLETE 的 false ledger。

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

仓库外 audit harness attempts 1/2 分别保留 missing repository `src` 与同名 `support.py` 解析错误；attempt 3 语义断言
PASS 但报告混入 interpreter version，attempt 4 将 runtime identity 移到 manifest 后四格 canonical report 逐字节相同，SHA-256
为 `89498f07c7d5b8cabaecf91e85b02c2484e56e94d871197f9a33c76ffeef5d78`，run manifest 为
`042a95716be695a98dffebd43c2e8e44bdd3cc63e2947c4e661072435a4c49e3`。

本文自己的 local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc265/milestones
readback/independent reconciliation闭合以前只保持candidate。它不授权composition contract、Fact/Relation/Slice successor
runtime、ReviewSliceSet/CoverageLedger、Schema successor、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、
R2/R3、CLAIM_FIDELITY、tag或Release。闭合以后必须返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage composition precontract audit（候选）

doc265 已在 `main@ceaec8fce6b695a35f5eb5ea35847b6f60063b63` 完成自己的资格链。PR #306 first original
Public CI `38751708053` 的 outer-timeout CANCELLED 保留；fresh independent original run `38755858920`、exact-main
Public CI `38759957319` 与 Browser Smoke `38759957354` 均 SUCCESS。fresh README/doc265/milestones qualifying
PASS 与 milestones formal attempt 1 ERROR 同时保留；independent reconciliation 为
`e3961fc50a2317cdca2b36e41eae8bcd42419ef9b8ff48d59f12a912c9d164c8`，修正后的 149-artifact closeout 为
`0c4a89aa1401e215a5d1e1c35e82bd4feef9393ff189178802695be815cebe1f`。

[文档 266](docs/266-r1-review-slice-set-coverage-composition-precontract-audit.md)只审 future composition contract 的最小面。
Fact handoff 保留 original Context/history，但 serialized surface 不含 Relation 所需完整 exact inputs；因此后继必须 join
attempt-neutral immutable `DerivationInputSet` 与 one-shot live handoff，不能按 digest 拼接 histories、复制 claim 或在 fresh
Context 重跑 Fact 后继承旧 authority。

当前唯一未被反例击穿的最小 topology 是一个 application-owned single composition attempt：重验 exact inputs、一次 claim
handoff、顺序形成 successor Relation qualification/admission、Slice closure、ReviewSliceSet admission，再对同一 owned history
做 Coverage qualification。七阶段 denominator 必须分别回到 Snapshot、Policy、Language、Parse、Fact U、Relation domain 与
Slice obligation owners；Coverage 不拥有考试范围。

U=3/E=2 blocker slot 仍可用现有 FACT item identity，但 `UNREPRESENTABLE_EXPECTED_FACT` 不在 Coverage 0.1 vocabulary，
因此 future contract 必须保留最小 version-stop rule，不能改名消除 blocker。四格 audit canonical report 均为 2726 bytes：

```text
report SHA-256 = eafcb77cdf5454f033f0bdbb6e592bedb853507a0af49e3111e1ff3c8b3e36ae
```

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本文自己的 local/original PR/separately approved exact-head merge/new exact-main dual gates/fresh README/doc266/milestones
readback/independent reconciliation闭合以前只保持candidate。它不授权composition contract、successor runtime、
ReviewSliceSet/CoverageLedger、Schema successor、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
CLAIM_FIDELITY、tag或Release。闭合以后必须返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage composition qualification 最小合同候选

doc266 已在 `main@becf49db117be20ecdb4d860c1763ad7bc0eaae7` 完成完整资格链。原 candidate outer-timeout
`CANCELLED`、独立 CI headroom maintenance、final original 11/11、exact-main 11/11 + Browser 1/1、fresh
README/doc266/milestones readback、proof-facility setup failures与后继 reconciliation PASS全部保留。independent
reconciliation为 `09d11235e5a50bb158049c6976e657431d94bf396faaa43befa746985b1895b3`，127-artifact closeout为
`c9b37740eb8665df2cbcafaabbdfaf79608510ce9fd6ffc7fa58abf90c9edf33`。因此 composition precontract audit成为
qualified history；Coverage contract/runtime没有自动开始。

[文档 267](docs/267-r1-review-slice-set-coverage-composition-qualification-contract.md)只冻结最小语义合同：一个
application-owned single composition attempt重验 immutable exact inputs、一次领取 original Fact handoff，再顺序取得
Relation admission、Slice closure、ReviewSliceSet admission与seven-stage Coverage qualification。各stage先区分authoritative
subject universe、applicability与qualification denominator；Coverage只拥有qualification，不能按actual output、
representability、Schema shape或R3 priority缩小考试范围。

相邻stage必须保存predecessor/successor transition proof，拒绝silent disappearance、foreign reappearance与local-equation
false COMPLETE。`slice_set_digest`只拥有semantic content identity；相同members/empty bytes不继承admission authority。
Coverage只有在同一composition history、admitted ReviewSliceSet、完整transition/terminal reconciliation上才能保守汇合。

U=3/E=2 blocker identity仍使用精确`FACT` subject digest；现有Coverage 0.1缺少
`UNREPRESENTABLE_EXPECTED_FACT`无损reason，因此本合同设置mandatory version stop，不选择版本号、Schema文件或迁移策略。

```text
R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRECONTRACT_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

candidate自己的final local/original PR/separately approved exact-head merge/new exact-main双门/fresh README/doc267/
milestones observations/independent reconciliation闭合以前，只保持contract candidate；随后仍需独立freeze publication。
本轮不修改runtime/tests/Schema、doc113/120/175/183/189/192/194/258–266、Profile/Policy/fixtures/corpus，不选择
persistence，不启动composition runtime、ReviewSliceSet/CoverageLedger assembler、Evidence/Bundle/publisher、CLI/
Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。

### R1 ReviewSliceSet / Coverage composition qualification 最小合同独立冻结发布（条件目标）

doc267 已在 `main@4280355c6ec4d1ade9cceedf8a47853d1a93ea16` 完成自己的资格链。PR #309 final head
`b86db5ee3bfae6c341a9a5d4634836b2c2dbb77a` 的 original Public CI `38836722757`、exact-main Public CI
`38852540587` 与 Browser Smoke `38852540955` 均为 attempt 1 SUCCESS，分别 11/11、11/11 与 1/1；Review
Attention 四格各为 `513 reported / 510 passed / 3 skipped`。fresh README/doc267/milestones 各有一份 qualifying
PASS；doc267 formal observation #1 的 P1 匿名 API 额度耗尽 ERROR 与后继 #2 PASS 同时保留。independent
reconciliation 与 135-artifact closeout 分别为：

```text
6fb87a704792b7f94c415f44765b059eb51057bafe1bc88f2383225c8b85f4a6
76fa18bc8e868e7fe4d5cf4a197fe6b4ec9f7a5aa6c09efe7ba5d3592e8fe818
```

[文档 268](docs/268-r1-review-slice-set-coverage-qualification-contract-freeze-publication.md)保留 doc267 已资格化
字节与 candidate marker，只条件化发布 `R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN` target。
本发布自己的 final-byte local gates、original PR、单独批准的 exact-head protected merge、new exact-main Public CI /
Browser Smoke、fresh README/doc268/milestones installed-product observations 与 independent reconciliation 全部闭合
以前，事实仍是 qualified contract candidate，`FROZEN` 不生效。

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许 README、AGENTS、milestones 与 doc268 的 docs-only publication surface。不得修改 doc267、runtime、tests、
Schema、Profile、Policy、fixtures 或 corpus；不得启动 Coverage vocabulary correction、composition feasibility/runtime、
`ReviewSliceSet` / `CoverageLedger` assembler、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
CLAIM_FIDELITY、tag 或 Release。最后门闭合以后只返回 CONTROL LOOP，分别重新审查 mandatory version correction 与
private composition feasibility；不得按文档编号自动施工。

### R1 ReviewSliceSet / Coverage vocabulary correction 当前状态审计与最小合同候选

doc268 已在 `main@13e08177e9353d45ebc2fde1244ac37b2bfea2d6` 完成自己的资格链。PR #310 original
Public CI `38858809608`、exact-main Public CI `38866243713` 与 Browser Smoke `38866243720` 均 attempt 1
SUCCESS，分别 11/11、11/11 与 1/1；fresh README/doc268/milestones 均取得 qualifying PASS。setup 1 的 wildcard、
Playwright、marker 与 derived-summary path errors，以及 setup 2 的 adapter ownership setup error 均保留；setup 2 的
independent reconciliation 与 120-artifact closeout 分别为：

```text
4a3a57357fd6523c872c5f0f326f859c35a960f9ce8021f101ffe442686903a8
5ddce0cd29ec8b5ef6b3150a5b5e752a5e7bd67bb9b12a744ad7f56810341a1b
```

因此 composition qualification 合同已经 frozen；version correction 没有自动开始。[文档 269](docs/269-r1-review-slice-set-coverage-vocabulary-correction-current-state-audit.md)
只审 mandatory vocabulary seam。机械反例证明 Coverage 0.1 不仅缺少 `UNREPRESENTABLE_EXPECTED_FACT` reason，也没有
独立 semantic `BLOCKED` carrier；把 blocker 改名为 `DERIVATION_ERROR` 并放入 `execution_failed` 可以 Schema-valid，
但会把 representation blocker 重解释为 execution failure。现有 `FACT` item identity 足以命名 exact U slot，因此 item-kind
shape 不是当前 blocker。

doc269 随后由 PR #311 final head `984ae8241b8f3513bc74762f23cf5260edbc131a` 的 original Public CI
`38870827554`、exact-main Public CI `38878798937`、Browser Smoke `38878798945`、fresh
README/doc269/milestones readback 与 independent reconciliation闭合为 qualified history。setup 1 的 preparation、parser、
premature freeze与折叠marker错误原样保留；setup 2 的 reconciliation 与117-artifact closeout为：

```text
041aa549bfe396bcdfd1b1ec8b774463eccba2c6585e326b88b525f8d5799a6d
afc10e8932ac94cb2ea5fc1464e152bf07ad6ebcea032c307cc2ab971d1569cd
```

[文档 270](docs/270-r1-review-slice-set-coverage-vocabulary-correction-contract.md)只冻结carrier-neutral
`terminal class / disposition family / exact reason`语义。projection-blocked tuple必须保持
`BLOCKED / SEMANTIC_PROJECTION_BLOCKER / UNREPRESENTABLE_EXPECTED_FACT`；execution failure继续属于独立provenance
family。Coverage 0.1 bytes/semantics immutable；public successor版本、Schema shape、migration、runtime与persistence均未选择。

```text
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

doc270候选自己的local/original PR/separately approved exact-head merge/new exact-main双门/fresh README/doc270/milestones
readback/independent reconciliation闭合以前只保持contract candidate。它不授权独立freeze publication、Schema successor或
feasibility、runtime/tests、composition feasibility/implementation、public ReviewSliceSet/CoverageLedger、persistence、
Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。闭合以后必须返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage vocabulary correction 最小合同独立冻结发布（条件目标）

doc270 已在 `main@b6eee45b87efd4ed850cb4e67f34df728dd47c4d` 完成自己的资格链。PR #312 final head
`e7231d4cd6ac81ae87053a14d3d344c9c342dda1` 的 original Public CI `38884545397`、exact-main Public CI
`38887472152` 与 Browser Smoke `38887472143` 均为 attempt 1 SUCCESS，分别 11/11、11/11 与 1/1；Review
Attention 四格各为 `513 reported / 510 passed / 3 skipped`。fresh README/doc270/milestones 各有一份 qualifying
PASS，正式 history 为 `3 PASS / 0 ERROR`。独立对账 attempt 1–4 的 key path、cell shape、stale public-byte marker 与
historical diagnostic marker errors 全部保留；attempt 5 与 166-artifact closeout 分别为：

```text
ea125d787f1c1b093ddbef3ef81cdb0f2857e289980efeecd0470b831d1008bb
f0b6097a573ccddee1fb0e04f7877fc467fe0cb08159a6e380c67ae94389f6f7
```

[文档 271](docs/271-r1-review-slice-set-coverage-vocabulary-correction-contract-freeze-publication.md)保留 doc270
已资格化字节与 candidate marker，只条件化发布
`R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN` target。本发布自己的 final-byte local
gates、original PR、单独批准的 exact-head protected merge、new exact-main Public CI / Browser Smoke、fresh
README/doc271/milestones installed-product observations 与 independent reconciliation 全部闭合以前，事实仍是 qualified
contract candidate，`FROZEN` 不生效。

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许 README、AGENTS、milestones 与 doc271 的 docs-only publication surface。不得修改 doc270、Coverage 0.1、
runtime、tests、Schema、Profile、Policy、fixtures、vectors 或 corpus；不得启动 successor Schema correction/feasibility、
composition feasibility/runtime、public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、
CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag 或 Release。最后门闭合以后只返回 CONTROL LOOP，重新审查显式
successor identity / Schema correction 是否仍为最小合法 seam；不得按文档编号自动施工。

### R1 ReviewSliceSet / Coverage Schema correction 可行性审计（候选）

文档 271 已在 `main@142bc264bbcddb155e5169fa0fa58659dedfa665` 完成自己的资格链。PR #313 final head
`592ae6dd40b91ea91e4c829d7f6f47cb65c7520a` 的 original Public CI `38894454185`、exact-main Public CI
`38897295769` 与 Browser Smoke `38897295757` 均为 attempt 1 SUCCESS，分别11/11、11/11与1/1；Review
Attention四格各为`513 reported / 510 passed / 3 skipped`。fresh README/doc271/milestones各有一份qualifying
PASS；milestones formal #1 的匿名额度耗尽ERROR与#2 PASS同时保留。independent reconciliation与126-artifact
closeout分别为：

```text
7330df0c1832d5e8601c98a15c91e01a4e6cccd7780fdf6d1242f2da8430d645
97de5369a6bda0a2776859dabd3a92dfa0097210b3f5493c91d50be53f4502a9
```

因此`R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN`已经生效；Schema successor与
composition没有自动开始。[文档 272](docs/272-r1-review-slice-set-coverage-schema-correction-feasibility-audit.md)只审显式
successor identity / Schema correction的有限可行性。仓库内DerivationEvidence precedent与七个mechanical worlds证明：
child successor可继续复用common 0.1基础类型，manifest 0.1可绑定child bytes/digest，但不拥有child version dispatch；
旧Coverage 0.1 validator拒绝successor bytes；JSON Schema单独不能拒绝同一member同时covered/blocked，因此后继必须同时
冻结self-describing child Schema、distinct identity domain、manifest/consumer dispatch与versioned conformance rule。

首次harness因audit-only `$id`改变相对`$ref`基址而以`UNRESOLVABLE_REFERENCE_SETUP_ERROR`停止；fresh attempt只修
proof-facility URI base并把`assert`改为普通/`-O`均执行的显式检查。CPython 3.10.6/3.13.13 normal/`-O`
四格canonical report逐字节一致：

```text
e54642dc26f7a4a9f2e7317c462217eff5375b3c8aaf9e380912ea22661deacc
```

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许README、AGENTS、milestones与新增doc272。不得修改doc267–271、runtime、tests、workflows、Schema、
manifest、fixtures、Profile、Policy、vectors或corpus；不得选择successor版本/文件名/字段名、启动Schema contract或实现、
composition feasibility/runtime、public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、
CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。完成自身完整资格链后只返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage Schema correction 最小合同候选

doc272 已在 `main@406aa8ee9440db8738ee2bd3a35aae558dc105c6` 完成自己的资格链。PR #314 final head
`a2577e1f05f1ebd685a35120181fc2b85bfffa7a` 的 original Public CI `38964769464`、exact-main Public CI
`38967921677` 与 Browser Smoke `38967921685` 均为 attempt 1 SUCCESS，分别11/11、11/11与1/1；Review Attention
四格各为`513 reported / 510 passed / 3 skipped`。setup 1 的证明设施错误与 README formal marker-selection ERROR均按原
identity保留；setup 2的fresh README/doc272/milestones为3/3 qualifying PASS。independent reconciliation与119-artifact
closeout分别为：

```text
d32b662933368546e14fb01d8477b6be5452fa9c5ecafaa695a35aba789d3672
741ed5551b423597bcebda0ee94f6102ffa872160e4cbe6a3649d34eab08a2f8
```

因此Schema correction feasibility audit已经成为qualified history。[文档 273](docs/273-r1-review-slice-set-coverage-schema-correction-contract.md)
只冻结CoverageLedger 0.2 child identity、`blocked`最小carrier、versioned conformance、manifest/consumer dispatch与0.1
immutability。manifest 0.1仍只绑定bytes/digest；unknown child version fail closed；Schema-valid不替代same-attempt provenance
与cross-field conformance。

```text
R1_REVIEW_SLICE_SET_COVERAGE_VOCABULARY_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_FEASIBILITY_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许README、AGENTS、milestones与新增doc273。不得修改doc267–272、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、identity vectors、corpus或架构资产；不得启动独立freeze publication、Schema implementation、
composition feasibility/runtime、public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、
CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。候选完成自己的完整资格链后只返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage Schema correction 最小合同独立冻结发布（条件目标）

doc273 已在 `main@356b930a039783417f8dcd698e7ae49c25fb4615` 完成自己的资格链。PR #315 final head
`37af11f8a4efeef1b34ff7a403e55fb924f70303` 的 original Public CI `38973694059`、exact-main Public CI
`38976364225` 与 Browser Smoke `38976364071` 均为 attempt 1 SUCCESS，分别11/11、11/11与1/1；Review
Attention四格各为`513 reported / 510 passed / 3 skipped`。semantic witness attempt 1因没有显式覆盖全部合同corpus
identity，以`SEMANTIC_WITNESS_COVERAGE_INCOMPLETE`保留；fresh attempt 2只补proof-facility witness。fresh
README/doc273/milestones为3/3 qualifying PASS；readback的两个operator setup error保持NON_QUALIFYING原identity。
independent reconciliation、120-artifact closeout与post-closeout terminal seal分别为：

```text
a4e3ca83e6b298646f789ac1113930f6cc87a1eed5dbbd46fe0e3755b4addb89
692a6fda883c37021a90e09da82b93dd356fef58d87489018ee15e11bdde9552
7185e12331f38247bac4c196fd15773326a9d63d803d7bec24cf0877c4db8d4c
```

[文档274](docs/274-r1-review-slice-set-coverage-schema-correction-contract-freeze-publication.md)保留doc273已资格化字节与
candidate marker，只条件化发布`R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN` target。本发布
自己的final-byte local gates、original PR、单独批准的exact-head protected merge、new exact-main Public CI / Browser
Smoke、fresh README/doc274/milestones installed-product observations与independent reconciliation全部闭合以前，事实仍是
qualified contract candidate，`FROZEN`不生效。

```text
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许README、AGENTS、milestones与doc274的docs-only publication surface。不得修改doc273、Coverage 0.1、
runtime、tests、Schema、manifest、Profile、Policy、fixtures、vectors或corpus；不得启动Schema implementation、composition
feasibility/runtime、public `ReviewSliceSet` / `CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/
Core、R2/R3、CLAIM_FIDELITY、tag或Release。最后门闭合以后只返回CONTROL LOOP，重新审查有限CoverageLedger 0.2
Schema implementation是否仍为最小合法seam；不得按文档编号自动施工。

### M10 public CLI native hard-exit diagnostic maintenance（候选）

R1 root-binding audit PR #317 的 Browser-before-exercise failure 促成独立 fixture maintenance PR #318；#318 final head
`ae59c118971614d99ec26413bc64aa07a5e1ab5a` 的原始 Public CI `39005021790` attempt 1 又在 Python 3.13 normal
暴露 `test_dependency_early_exit_creates_completed_fail_bundle_without_browser` child return code `3221225477 /
0xC0000005`，stdout/stderr 为空。Python 3.10、Workbench、E3 成功；#318 未 rerun、未改 head并已关闭，root cause
保持`UNKNOWN`。

[文档277](docs/277-m10-public-cli-native-hard-exit-diagnostic-maintenance.md)只让既有独立 CLI child 使用`-X faulthandler`，
继续保留normal/`-O`模式、同一公共命令、Bundle与断言；若native fault重现，outer unittest仍保留return code，并可同时
捕获Python fatal stack。exact-main Windows handle ownership源码审查没有证明runtime defect，本轮不修改runtime、资源阈值、
Browser fixture、Schema、Coverage或persistence。

```text
M10_PUBLIC_CLI_NATIVE_HARD_EXIT_DIAGNOSTIC_MAINTENANCE_CANDIDATE
PR_318_ORIGINAL_FAILURE_RETAINED
PR_318_ROOT_CAUSE_UNKNOWN
M10_BROWSER_HARD_FAILURE_FIXTURE_RESOURCE_ISOLATION_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_AUDIT_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本候选完成自己的完整资格链后只返回CONTROL LOOP，从新的exact main重建Browser fixture resource-isolation maintenance；
后者独立资格化以前，不得重建root-binding audit。不得借诊断增强解释#317/#318首败或启动Schema实现、composition
feasibility/runtime、public ReviewSliceSet/CoverageLedger、persistence、Evidence/Bundle/publisher、R2/R3或CLAIM_FIDELITY。

### M10 Browser hard-failure fixture resource isolation maintenance（重新创建候选）

PR #319 的诊断维护已在 `main@a5137525c2348334bf0b79a2e873895a8533e745` 完成 original PR、protected
merge、exact-main双门、fresh README/doc277/milestones读回与independent reconciliation；它只建立更强的native
hard-exit diagnostic source state，#318 root cause仍为`UNKNOWN`。

[文档278](docs/278-m10-browser-hard-failure-fixture-resource-isolation-maintenance.md)从该exact main重新创建独立
fixture maintenance：普通Browser/lifecycle worlds使用test-owned `1 / 1 MiB` host-memory门；两个resource-limit
worlds显式保留`4096 / 2048 MiB`并注入确定性`100 / 3000 MiB`观测；Browser Artifact assertions保留
stop/trigger/resource diagnostics。产品runtime、resource合同、timeout、Schema、Coverage与persistence均不修改。

```text
M10_BROWSER_HARD_FAILURE_FIXTURE_RESOURCE_ISOLATION_MAINTENANCE_CANDIDATE
M10_PUBLIC_CLI_NATIVE_HARD_EXIT_DIAGNOSTIC_MAINTENANCE_QUALIFIED
PR_317_ORIGINAL_FAILURE_RETAINED
PR_317_ROOT_CAUSE_UNKNOWN
PR_318_ORIGINAL_FAILURE_RETAINED
PR_318_ROOT_CAUSE_UNKNOWN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_AUDIT_NOT_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本候选的完整资格链闭合以后只返回CONTROL LOOP，从新exact main重新生成root-binding audit candidate；不得继承
#318资格，不得修改Schema/runtime或启动composition、persistence及public Review产品。

### R1 ReviewSliceSet / Coverage Schema root binding 当前状态审计（重新生成候选）

PR #320 final head `1cba21711bad9b858ac9a89cecb4930a3794dac7` 已合入
`main@5b0ba6d3ebe06c7da3320c18afd47a658aff465e`。original Public CI `39017859822`、exact-main Public CI
`39020304436` 与 Browser Smoke `39020304437` 均为 attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc278/milestones为3/3 qualifying PASS。independent reconciliation与181-artifact closeout分别为：

```text
ce6bb7497d4bce9a204e520894601bfcf751c7e5d2a1020806d6d2a0b90d0746
1d1f731c4d75f1ae191f5d50536caf39716bdc8b2bb478f18302f1f77e5426be
```

因此Browser fixture resource-isolation maintenance已经qualified；#317/#318首败与`UNKNOWN` root cause继续保留。
[文档279](docs/279-r1-review-slice-set-coverage-schema-root-binding-current-state-audit.md)从该新exact main重新执行CONTROL LOOP。
新的read-only四格falsifier仍证明：projection-blocked handoff的U/E/blocker为`3/2/1`且`fact_set=null`，但frozen
CoverageLedger root要求`fact_set_digest`；省略root会被Schema拒绝，未获authority的占位digest只能取得shape。

```text
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本轮只允许README、AGENTS、milestones与新增doc279。不得修改doc267–278、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得起草root-binding correction合同、启动Schema implementation、composition
feasibility/runtime、public`ReviewSliceSet`/`CoverageLedger`、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、
R2/R3、CLAIM_FIDELITY、tag或Release。完成自身完整资格链后只返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage root binding correction 前合同审计候选

PR #321 final head `406923bdfa7e89ff3caaea9d66e402a9075bae03` 已合入
`main@acf248daee9bca362a84df27fb9f7d8c2385b0b9`。original Public CI `39022612920`、exact-main Public CI
`39024355114`与Browser Smoke `39024355171`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc279/milestones为3/3 qualifying PASS。independent reconciliation与173-artifact closeout分别为：

```text
9c78cbe29b76a6780d670f1ea51df825603eedec754f93b6870aeb476a202e3c
c0e886b08e4dcf990ade8f7890e9e6c07a61683e2c09e9e51288f9bac4aec6d4
```

因此doc279已经成为qualified history。fresh CONTROL LOOP创建
[文档280](docs/280-r1-review-slice-set-coverage-root-binding-correction-precontract-audit.md)，只审 root correction的最小问题面。
read-only mechanical audit证明：现有root同时要求Fact/Relation/ReviewSlice三个set digest；五个Fact worlds中只有normal有
FactSet，四个safe-negative worlds保留不同qualified absence；manifest 0.1的COMPLETE/DIAGNOSTIC topology均不能携带
缺少三个normal sets的CoverageLedger。attempt 1的`KeyError('blockers')`按`AUDIT_HARNESS_SETUP_ERROR`保留；fresh
attempt 2四格逐字节一致：

```text
6bfbc73f8ff4cf33fb54570b585789df0dab74c75a012c113ffc66dd010d4f48
```

```text
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_ROOT_BINDING_CURRENT_STATE_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_PRECONTRACT_AUDIT_QUALIFIED_HISTORY
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

doc280 已由 PR #322 final head `9628b9334cad5cfb22327c7e28e833c3999608e5` 合入
`main@b2725e5069cfca0dde1e120192eb03d47fba8ff9`。original Public CI `39027041983`、exact-main Public CI
`39029206479` 与 Browser Smoke `39029206492` 均 attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc280/milestones为3/3 qualifying PASS。independent reconciliation与182-artifact closeout分别为：

```text
ae9eba013266c43e430920754433455444171ac1747202de3ac9ce32b6c98144
4dc81ff765da8dde180dce25e79ec01111e4a6adbdad12f7dfabbc5572acab90
```

首个readback setup的超长Plan ID、fresh setup缺失pip log及宿主策略命令拒绝均按setup/operator事实保留，没有formal
qualification effect。因此doc280已经成为qualified history。fresh CONTROL LOOP创建
[文档281](docs/281-r1-review-slice-set-coverage-root-binding-correction-contract.md)，只冻结CoverageLedger 0.3 ordered root
chain、versioned terminal-history projection、`ARTIFACT_PRESENT / QUALIFIED_ABSENT / QUALIFIED_UNKNOWN`、branch-empty仍属present、0.1/0.2 immutability、
0.3 conformance与manifest compatibility stop。manifest negative-world successor继续是独立问题。

本候选只允许README、AGENTS、milestones与新增doc281。不得修改doc259–280、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得启动Schema implementation、composition feasibility/runtime、manifest successor、
public Review产品、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。
完成自身完整资格链后最多成为qualified contract candidate；随后仍需独立docs-only freeze publication。

### R1 ReviewSliceSet / Coverage root binding correction 最小合同独立冻结发布候选

文档281已由PR #323 final head `32de8a67a547f521d9272755c5c447e70830ec10`合入
`main@e0de7556f4075068dcaaa74fba85dcd756540fa6`。original Public CI `39036786001`、exact-main Public CI
`39039139791`与Browser Smoke `39039139694`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh setup 2的
README/doc281/milestones为3/3 qualifying PASS。independent reconciliation与188-artifact closeout分别为：

```text
04045abb14705435747630c0e3095aea2318be8cbf8b6f07d59f4229e155ed4a
08f337f9544b732a7221047f313961c2bc254e2763553ca50a3e8c7cfa9a843d
```

setup 1的README formal marker-selection ERROR与reconciliation attempt 1的wrapper stdout post-seal mutation继续保留；
后继PASS没有覆盖二者。doc281 full-file SHA-256继续为
`241dc7b5922c981aabb61a1a6a765ed224bdf7ac47a588274a20a9bb3e311eaf`。

[文档282](docs/282-r1-review-slice-set-coverage-root-binding-correction-contract-freeze-publication.md)只发布doc281定义的
0.3 ordered root chain合同。本文档进入仓库不等于冻结生效；自己的final-byte local gates、original PR checks、单独批准
exact-head protected merge、new exact-main Public CI + Browser Smoke、fresh anonymous installed-product
README/doc281/doc282/milestones observations与independent reconciliation全部闭合后，`CONTRACT_FROZEN` target才成为事实。

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本发布只允许README、AGENTS、milestones与新增doc282。不得修改doc259–281、runtime、tests、workflows、Schema、
manifest、fixtures、Profile、Policy、vectors或corpus；不得启动Schema implementation、composition feasibility/runtime、
manifest successor、public Review产品、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
CLAIM_FIDELITY、tag或Release。冻结后也只返回CONTROL LOOP，分别重新审查child Schema/conformance、manifest topology与
composition runtime；三者不得自动合并授权。

### R1 CoverageLedger 0.3 child Schema / conformance 可行性审计候选

PR #324 final head `4874cd21f223ece7f5c17a6369cc512012d23d68` 已合入
`main@6709f5890c6b2cf9bf5acd84d8531af49ac00c76`。original Public CI `39047963366`、exact-main Public CI
`39091698699`与Browser Smoke `39091698666`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc281/doc282/milestones为4/4 qualifying PASS。首个doc282 formal匿名API quota ERROR继续保留。independent
reconciliation与238-artifact closeout分别为：

```text
884d3a4765ca1111e40fa8305159a710c5ba15876a15c5c8a328d5611d4b0ebd
4307edd2c672581a52ccf696528ec97160aabadbbe03022bc30d27d61b92fcb3
```

因此root-binding correction合同已经frozen。[文档283](docs/283-r1-review-coverage-ledger-0-3-schema-conformance-feasibility-audit.md)
从该exact main重新执行CONTROL LOOP，只审finite child Schema/conformance feasibility。read-only audit确认仓库仍只有
CoverageLedger 0.1 Schema，0.2/0.3文件均不存在；Fact handoff、Relation admission及Slice normal/empty/blocked private
history已保留构造versioned terminal-history projection所需材料。audit-only root fragment不是产品Schema，也不证明composition。

八个positive worlds与八类mutation在CPython 3.10.6/3.13.13、normal/`-O`四格全部PASS，canonical report逐字节一致：

```text
06be5d0ac56ff70762bfe6680e1cc137abc288123fe53b8b6a7b68d32c9594b0
```

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本候选只允许README、AGENTS、milestones与新增doc283。不得修改doc259–282、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得启动Schema implementation/authorization、composition、manifest successor、
public Review产品、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。完成
自己的完整资格链后最多成为qualified feasibility history，并返回CONTROL LOOP。

### R1 CoverageLedger 0.3 child Schema / conformance 实现授权发布候选

文档283已由PR #325 final head `734f35a328e706fe843ec6f2f9590c6e2ac90f83`合入
`main@dd4cd19d23623516416c8d0a6803c22d15960e36`。original Public CI `39094291800`、exact-main Public CI
`39095889099`与Browser Smoke `39095889019`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc283/milestones为3/3 qualifying PASS。independent reconciliation与145-artifact closeout分别为：

```text
afb2bf3dfc5054ee0fb8b00504e4a485125d4e8c3552d7eac318c48fcc9b405d
0e26367f1d3614d56e3ddc130f45d41003205818154a433d30ed16cf543c57d2
```

因此doc283已经成为qualified feasibility history。fresh CONTROL LOOP未发现更早prerequisite或击穿上游合同的反例；
0.3 child不需要先物化0.2，也不需要先修改common/manifest、选择persistence或实现composition assembler。

[文档284](docs/284-r1-review-coverage-ledger-0-3-schema-conformance-implementation-authorization-publication.md)只条件化发布
doc283已审计的bounded A–J实现面：exact 0.3 child Schema、versioned conformance、terminal-history/binding/chain/digest复算、
positive/negative fixtures与identity vectors、`RSCSC-000..016` / `RBCC-000..011` direct falsifiers、known-version fail-closed与
0.1/common/manifest全字节守卫。本文进入仓库不等于授权生效；自己的final-byte local gates、original PR checks、单独批准的
exact-head protected merge、new exact-main Public CI + Browser Smoke、fresh anonymous installed-product
README/doc283/doc284/milestones observations与independent reconciliation全部闭合后，`SCHEMA_IMPLEMENTATION_ALLOWED`
target才成为事实。

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_SCHEMA_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本发布只允许README、AGENTS、milestones与新增doc284。不得修改doc259–283、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得启动Schema/conformance implementation candidate本身、composition、manifest
successor、public Review产品、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或
Release。最后门闭合以后也只得到`ALLOWED / NOT_STARTED`，必须返回CONTROL LOOP重新确认A–J仍是最小合法seam。

### R1 CoverageLedger 0.3 child Schema / conformance 私有实现候选

文档284由PR #326合入`main@b4e741bc3b4029257f95cb1bfabbbd0e71c40bd3`。其original PR与exact-main双门均为
attempt 1 SUCCESS；fresh README/doc283/doc284/milestones为4/4 qualifying PASS。independent reconciliation与
149-artifact closeout分别为：

```text
0c9358d34d234c29f4869de1a0b34b04cfb3b9282e10009074b11aacf5f5d19d
eb66acd79603423953c16cf12f25f6f54abf67b637d30e8c9979c0dacb61d027
```

因此`SCHEMA_IMPLEMENTATION_ALLOWED`已生效。fresh CONTROL LOOP确认A–J仍是最小合法seam；当前进入
[文档285](docs/285-r1-review-coverage-ledger-0-3-schema-conformance-implementation-candidate.md)的单用途implementation
candidate。它新增exact 0.3 child Schema、validation-only conformance、closed terminal-history vectors、八个规范world、
`RSCSC-000..016` / `RBCC-000..011` direct falsifiers与0.1/common/manifest/history全字节守卫。

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_ALLOWED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

PR #327 final head `578714adc3ca84552a1aa7e3aa08c79096d3cf5f`已合入
`main@2dc923ba5b070aaa63d6b783c7d21c1135a9f6ca`；original Public CI、exact-main Public CI与Browser Smoke均为
attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh README/doc285/milestones取得3个qualifying PASS；首个milestones
formal匿名API额度耗尽ERROR继续保留。independent reconciliation与148-artifact closeout分别为：

```text
6fe3331f5eb24a5aaf057563c2c398d9c37945bb060388515ee87e04a83aa745
7f0635123b85d83d218c1b17358803e5d1170874f167fb5bf73108bee6767e9a
```

因此doc285已成为qualified implementation candidate，但仍不是frozen，也不拥有composition、manifest successor、persistence、
transport或publication authority。

### R1 CoverageLedger 0.3 child Schema / conformance 私有实现独立冻结发布候选

[文档286](docs/286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)只条件化发布doc285
已资格化的bounded A–J实现。本文进入仓库不等于冻结生效；自己的final-byte local gates、original PR checks、单独批准
exact-head protected merge、new exact-main Public CI + Browser Smoke、fresh anonymous installed-product
README/doc285/doc286/milestones observations与independent reconciliation全部闭合后，`IMPLEMENTATION_FROZEN` target才成为事实。

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_ALLOWED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_CANDIDATE_QUALIFIED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本发布只允许README、AGENTS、milestones与新增doc286。不得修改doc281–285、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得启动composition、manifest successor、public Review产品、persistence、
Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。最后门闭合以后必须返回
CONTROL LOOP，不自动授权下一seam。

### R1 ReviewSliceSet / Coverage composition 私有实现可行性审计候选

文档286由PR #328 final head `f29d170987ffd693d0575c91d0853ad0252038ed`合入
`main@ac41b5c852a7f79607fa3bcc771ea0b7858abeb9`。original Public CI `39108536749`、exact-main Public CI
`39110162970`与Browser Smoke `39110162978`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc285/doc286/milestones为4/4 qualifying PASS。independent reconciliation与165-artifact closeout分别为：

```text
26bc4b18172a0317d5f82d011b56bb0767f1fb35a1b65b24767483740e40b8e3
1c5215761e4524435d0d4cf48fce817d66406b042f977d97275eeae4974b91ba
```

因此CoverageLedger 0.3 child Schema/conformance private implementation已经frozen。fresh CONTROL LOOP创建
[文档287](docs/287-r1-review-slice-set-coverage-composition-private-implementation-feasibility-audit.md)。read-only source audit
确认one-shot Fact handoff及完整terminal history已经存在；legacy high-level Relation qualifier会创建新context并重跑Fact，
legacy Relation admission与Slice entry又绑定旧Fact phase/continuation，因此不能原样接入handoff。现有low-level Relation
domain/cell、Slice normal/empty/blocked closure与validation-only 0.3 conformance足以支撑bounded versioned successor，
不需要重开frozen合同、先选persistence或先解决manifest negative-world publication topology。

四格read-only audit attempt 4在CPython 3.10.6/3.13.13、normal/`-O`全部PASS且canonical report逐字节一致：

```text
14210f1ce528b09f7ab9c5808105637287c1c082175f79a1c1c7b6fb6d03fed3
```

前三次audit harness分别因参数名、调用图层级与过宽filename predicate失败并保留；均不构成产品反例。

```text
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc287。不得修改doc259–286、runtime、tests、workflows、Schema、manifest、
fixtures、Profile、Policy、vectors或corpus；不得启动composition implementation/authorization、manifest successor、
public Review产品、persistence、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、CLAIM_FIDELITY、tag或Release。
完成自己的local/original PR/separately approved exact-head merge/new exact-main双门/fresh README/doc287/milestones
readback/independent reconciliation后，最多成为qualified feasibility history并返回CONTROL LOOP。

### R1 ReviewSliceSet / Coverage composition 私有实现授权发布候选

文档287由PR #329 final head `fd02f92ea1047ac6b246585bb167d4681625bca3`合入
`main@0dc7f832b7f77a1926c6ab7807805f9939e56246`。original Public CI `39113130924`、exact-main Public CI
`39114897070`与Browser Smoke `39114897054`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc287/milestones为3/3 qualifying PASS。independent reconciliation与141-artifact closeout分别为：

```text
07cf069ccc901f30ce8ac28d01623a6b711256e665fa14211a92038a80f657d4
efccb6067ff3e974361e043cfd22bbd27489b5833d638492223740b19a9e51b9
```

因此doc287已成为qualified feasibility history。PR #330随后只修改README读者说明并合入
`main@de21b3a2fadf436b22d91b7d90c218a6c868f77c`；它不拥有R1 authority。fresh CONTROL LOOP已放弃旧基线上的
候选资格并重新绑定该exact main，未发现更早prerequisite或击穿frozen contracts的反例。当前最小合法候选是
[文档288](docs/288-r1-review-slice-set-coverage-composition-private-implementation-authorization-publication.md)，它只条件化
发布doc287 A–J：single composition attempt、handoff重验、post-handoff Relation/RelationSet successor、same-attempt Slice、
ReviewSliceSet projection/admission、seven-stage history、total Coverage qualification、one-shot closure与direct falsifiers。

```text
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本publication自己的final bytes、local gates、original PR qualification、单独批准的exact-head protected merge、new exact-main
Public CI 11/11 + Browser Smoke 1/1、fresh anonymous installed-product README/doc287/doc288/milestones observations与
independent reconciliation全部闭合以前，`COMPOSITION_IMPLEMENTATION_ALLOWED`不生效。它不创建或修改runtime、tests、
Schema、manifest、fixtures、vectors，不选择persistence，也不启动public Review产品；最后门闭合以后也只得到
`ALLOWED / NOT_STARTED`并返回CONTROL LOOP。

### R1 Fact handoff → Relation exact-input interoperability 可行性修正审计候选

文档288的publication最后门后来在`main@3e491558d511f2578a5364d25822d235e91e8a14`闭合。fresh
README/doc287/doc288/milestones为4/4 qualifying PASS；independent reconciliation与156-artifact closeout分别为：

```text
ea069bfc0995a90c40e26cbb282f2420aaa3c8df72d91d094003e1e1931e96c1
892ea5494a0b9ab6785f42e16341b411d26cbc4c6aaed2878a8a303813c6d508
```

因此`COMPOSITION_IMPLEMENTATION_ALLOWED`已成为历史事实，但implementation仍未开始。施工前read-only反例随后触发
doc287 §9 / doc288 §5：current Fact applicability只接受Fact requirements，current Relation domain要求Relation
requirement并只接受single-module MODULE+IMPORT closed shape；完整五类Fact handoff、Fact-only MODULE+IMPORT handoff与
Fact+Relation combined Policy三者分别在Relation domain或Fact consumer边界被拒绝。首轮四格semantic report为：

```text
c01f2c7b46fda251272abea8fad86d76a52ff731b593d4cb55f9bb1cb617bd50
```

[文档289](docs/289-r1-fact-handoff-relation-exact-input-interoperability-feasibility-correction-audit.md)只审同一sealed Policy的
stage-scoped applicability、完整FactSet到Relation-applicable obligation的投影、single-module closed-shape边界与bounded
versioned successor。第二轮四格证明过滤FactSet会改变digest，而current Provider在audit-only validated view后能保留完整
五类或多模块FactSet并完成profile-applicable import obligations；semantic report为：

```text
51c17d6fce90fde5cee9152250ff59eb025eb4f236604db14699ab2e730c726f
```

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc289。不得修改doc175/doc287/doc288、runtime、tests、workflows、
Schema、manifest、fixtures、Profile、Policy、vectors或corpus；不得起草correction contract、实现successor、恢复composition
施工、选择persistence或启动public Review产品。完成自己的local/original PR/separately approved exact-head merge/new
exact-main双门/fresh README/doc289/milestones readback/independent reconciliation后，最多成为qualified correction
feasibility history并返回CONTROL LOOP。

### R1 Fact handoff → Relation exact-input interoperability correction 最小合同候选

文档289后来由PR #332 final head `79027d49c515a249a049e49fd81d273f4f3b1cc5`合入
`main@2f57c71e6e3a9ecb3e2d2da050d331fff7bb004a`。original Public CI `39129451257`、exact-main Public CI
`39131588569`与Browser Smoke `39131588645`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc289/milestones均取得qualifying PASS。首次milestones formal observation的503/PARTIAL保持
`FORMAL_READBACK_ERROR`；independent reconciliation attempt 1的derived marker metadata mismatch保持proof-facility
failure。attempt 2与176-artifact closeout分别为：

```text
7df17cfa65f5ee800c7df52c4c7de80016666198ba7b2726a6c781e43b14a015
56bc8017443700422926336a59993f70b8aa6297df6b2dedcbf9e199cf79f8b8
```

因此doc289已成为qualified feasibility history。[文档290](docs/290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)
只冻结四个semantic functions：same-policy stage applicability、完整FactSet total partition、per accepted product/path MODULE
closure与Relation-profile obligation projection。完整Policy与FactSet始终保留；projection只决定当前stage责任，不能删除或替代
authoritative world。`O_R(F)`还必须与从完整F/P/Profile/closure机械重算的expected universe做双向、基数与唯一性核账；只证明
emitted rows可追溯不足以证明完整。已测试候选全部失败只能停在UNKNOWN，除非对完整限定候选空间给出不可满足性证明。
audit-only attempt 1误删排序后的Relation requirement，保留为`AUDIT_FIXTURE_SETUP_ERROR`；attempt 2
证明核心projection，但合同复读发现其把完整`policy_digest`过度绑定进stage semantic digest。attempt 3只修
semantic/exact binding；其后summary命令的PowerShell scalar/`System.Char`错误保留为`OPERATOR_REPORTING_ERROR`，完整reports
不受影响。“两个适用Import只emitted一个obligation”的新反例随后要求双向、基数与唯一性核账。fresh attempt 4增加该
falsifier、不改产品oracle，并在CPython 3.10.6/3.13.13 normal/`-O`四格逐字节一致：

```text
02f33ff455057ad1010ac392fdc1132b1e33fc9cf6b8e5bc65bc89f273cd7c07
```

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc290。不得修改doc175/doc287/doc288/doc289、runtime、tests、workflows、
Schema、manifest、fixtures、Profile、Policy、vectors或corpus。自己的完整candidate qualification与后继独立freeze publication
全部闭合以前，合同不生效；即使最终FROZEN，也不自动实现successor、恢复composition A–J、选择persistence/manifest或启动
public Review产品。

### R1 Fact handoff → Relation exact-input interoperability correction 合同独立冻结发布候选

文档290后来由PR #333 final head `2763e06bcbcdefeb3f5711f678dd4c22c826793e`合入
`main@33b4aa37d4ce22ebbac93e898e716da4e7053792`。original Public CI `39137995491`、exact-main Public CI
`39139725019`与Browser Smoke `39139725021`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc290/milestones均取得qualifying PASS；doc290 public-render diagnostic #1的`ERROR / UNKNOWN`及多项proof-facility
setup问题继续保留。independent reconciliation与167-artifact closeout分别为：

```text
4d93b5cb4960aac9551e126f13a511f2b27544fd40339ac20db65fb173a2c9c8
30f7cf5eb104b443839bec94f17c442224f374fb058015db9cde353d7c6d4b16
```

因此doc290已成为qualified contract candidate。[文档291](docs/291-r1-fact-handoff-relation-exact-input-interoperability-correction-contract-freeze-publication.md)
只条件化发布该合同，不修改doc290语义、runtime、tests、Schema、manifest、Profile、Policy、fixtures、vectors或corpus。

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_FEASIBILITY_CORRECTION_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本publication自己的final bytes、local gates、original PR qualification、单独批准的exact-head protected merge、new exact-main
Public CI与Browser Smoke、fresh anonymous installed-product README/doc290/doc291/milestones observations及independent
reconciliation全部闭合以前，`CONTRACT_FROZEN`不生效。最后门闭合以后只允许返回CONTROL LOOP；corrected successor
feasibility、implementation authority、旧composition A–J恢复、manifest successor、persistence与public Review产品均未启动。

### R1 Fact handoff → Relation interoperability correction 合同冻结闭合

文档291后来由PR #334 final head `29f7a9348780a1fd819f6ed7db57c2f78a233259`合入
`main@0e32501644d93e33bc0610e1b149c2c33f4be69d`。original Public CI `39144553268`、exact-main Public CI
`39146613986`与Browser Smoke `39146613991`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc290/doc291/milestones最终为4/4 qualifying PASS；milestones formal #1因匿名API额度耗尽成为
`FORMAL_READBACK_ERROR`，fresh #2使用新的Plan/session/output取得PASS，首个ERROR继续保留。independent reconciliation与
171-artifact closeout分别为：

```text
523ebf741b4bfef44bbbe0b7f91f2b693b2ec42ea76dacff5c466594664f56e9
7825232b20f7116a8b0e3aa6cba16fc12af1ab35c03e6176d9f561b35afa7ea1
```

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_FEASIBILITY_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

该冻结只形成private interoperability correction semantic authority。下一步仍须从新exact main返回CONTROL LOOP，判断
corrected successor feasibility是否为最小合法问题；不得从合同冻结直接恢复旧composition A–J或启动implementation。

### Post-R1 外部错题本 Benchmark 与 Oracle 资格计划（延期）

[文档292](docs/292-post-r1-external-counterexample-benchmark-and-oracle-qualification-plan.md)保存 R1 完整闭合后的外部反例
攻击计划。它要求先资格化case与claim，再独立审查Oracle construction，最后才允许把qualified expected universe与DUT
reconciliation；外部程序、冻结摘要或`expected == actual`都不自动证明Oracle正确。DUT与Oracle共享关键projector、denominator、
normalization或identity路径时，必须公开common-mode failure surface并以独立falsifier攻击。

该计划同时保存后续Attention的非线性边界：cause relation、action relation、intervention observation与human-work evaluation
彼此不继承authority；common cause不推出shared resolution，shared resolution也不推出common cause，动作有效更不推出人工省工。

```text
POST_R1_EXTERNAL_COUNTEREXAMPLE_BENCHMARK_PLAN_0_1
    PLANNED / NOT_STARTED

CURRENT R1
    UNCHANGED

R2 / R3 / PUBLIC BENCHMARK PRODUCT
    NOT_STARTED BY DOC292
```

用户已授权在R1终态资格链闭合后执行该方向；届时不重做“是否开始”的概念讨论，但必须从当时exact main重新运行
CONTROL LOOP，确认没有更早反例并为具体case/Oracle/DUT工作取得本阶段资格。文档292是未来方法与启动条件，不是当前事实，
不得按编号自动越过R1、当前correction successor、manifest、persistence或public Review停止线。

### R1 Fact / Relation stage applicability capability identity 修正审计候选

从`main@0a94b32f464f896b86de1cef18dc88dc126225be`重新运行CONTROL LOOP时，[文档293](docs/293-r1-fact-relation-stage-applicability-capability-identity-correction-audit.md)
发现frozen doc290 §5把Fact stage owner requirement identity写成仓库中不存在的`review-fact-derivation`。当前runtime、fixtures与
Provider descriptors实际只承认required `python-ast`与optional `python-ast-advisory`；Relation stage继续拥有
`review-relation-derivation`。因为doc290同时要求stage applicability绑定exact requirement identity，这不是可忽略的别名差异。

独立audit在Python 3.10/3.13 × normal/`-O`四格中得到相同semantic digest
`f2319f6300b878cf2d8dec8c4291bf514c8cc2dd83afa816bc228e7f012412e7`：actual combined Policy可由generic Policy接纳，
current Fact applicability拒绝额外Relation capability，current Relation applicability接纳；literal doc290 identity则被Fact与
Relation双方拒绝。首次3.10 normal audit因手写64 MiB transport limit触发`AUDIT_HARNESS_SETUP_ERROR`，原身份保留；改用仓库
`DEFAULT_TRANSPORT_LIMITS`后以fresh attempt 2重跑。现有Fact/Relation窄基线四格各`Ran 77 tests / OK (skipped=1)`。

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_COUNTEREXAMPLE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc293，保存doc290/doc291已资格化历史字节，不修改runtime、tests、Schema、
Profile、Policy、Provider、manifest或post-R1计划。自己的final-byte门、original PR、单独批准的exact-head merge、new exact-main
双门、fresh README/doc293/milestones读回与独立对账闭合后，最多形成qualified correction audit history并返回CONTROL LOOP；
不得直接改doc290、实现successor、恢复composition A–J、选择manifest/persistence或启动Coverage、public Review、R2/R3。

### R1 Fact / Relation stage applicability capability identity 修正合同候选

文档293由PR #338 final head `7725c637f0a2681a0781f7a2b2ad1f42d4de60a8`合入
`main@0dd06e0e236a56472925bd6f29fc053b49727958`。original Public CI `39193502156`、exact-main Public CI
`39201809502`与Browser Smoke `39201809536`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc293/milestones为3/3 qualifying PASS。independent reconciliation与132-artifact closeout分别为：

```text
f5412f7e32842687ecb5df0162c70e18ae1850f1329ff52292fa5f4f87208529
54231fcfb88109112115ac5c5b08e1ad088d8269c266b9221885442b37b70cdf
```

因此该反例现为qualified history。fresh CONTROL LOOP没有发现并行semantic施工或更早seam；下一最小问题是
[文档294](docs/294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)限定的docs-only修正合同候选。
它将parent contract与stage applicability升级到`/0.2`，把Fact owner冻结为required `python-ast`与存在时optional
`python-ast-advisory`，Relation owner冻结为required `review-relation-derivation`，并要求两个stage对完整Policy形成total、
disjoint、exactly-once ownership。per-product closure与obligation projection仍为原`/0.1`语义，doc290/291历史字节不改。

当前只能记录`R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_CANDIDATE /
NOT_FROZEN`。本候选只允许README、AGENTS、milestones与新增doc294；自己的完整candidate qualification与独立freeze
publication闭合前不得启动runtime、恢复composition A–J、选择manifest/persistence或启动Coverage、public Review、R2/R3。

### R1 Fact / Relation stage applicability capability identity 修正合同冻结发布候选

文档294由PR #339 final head `e5ba262b602c86a9390d763c048a6eb31954af45`合入
`main@289b496282adaa20a582ef5ffb93a6a3476d4d6a`。original Public CI `39206452352`、exact-main Public CI
`39213475131`与Browser Smoke `39213475022`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc294/milestones为3/3 qualifying PASS。independent reconciliation与130-path closeout index分别为：

```text
19fd667cb7fd5ff13e31932a49429dcffa218760d06ee13366a2a3a1dbd23bc2
20a28872176ed644163ab485c9aef36ac9473f0c97e6b32a5c5150ab4d6e7dc3
```

本publication本地复算发现closeout index写入时纳入了仍会被wrapper追加的`create-closeout-attempt-1.stdout.txt`：索引中的
empty digest与终态stdout不一致，其余129项逐项一致。该proof-facility self-capture finding被独立保留；它不改变先于closeout
完成的independent reconciliation与3/3 formal资格，也不能继续把该索引叙述成130项全部终态封存。

因此文档294现为qualified contract candidate；fresh CONTROL LOOP没有发现并行semantic施工或更早seam。当前最小合法问题是
[文档295](docs/295-r1-fact-relation-stage-applicability-capability-identity-correction-contract-freeze-publication.md)
限定的独立docs-only冻结发布。它只发布文档294的`/0.2` bounded owner map、total/disjoint ownership、完整Policy/Fact truth、
per-product closure、obligation completeness与same-attempt authority；不选择successor carrier、Schema、manifest或persistence。

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_QUALIFIED_HISTORY
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

文档295中的`CONTRACT_FROZEN`只是条件目标。它自己的final-byte local gates、original PR、单独批准的exact-head merge、new
exact-main双门、fresh README/doc294/doc295/milestones读回与独立对账全部闭合以后才可生效；随后必须返回CONTROL LOOP，
不能自动启动corrected successor feasibility、恢复旧composition A–J或进入Coverage、public Review、R2/R3。

### R1 Fact handoff → Relation corrected successor 私有实现可行性审计候选

文档295由PR #340 final head `80c299b383d66f442d1710b4502cd9baf23489d2`合入
`main@b293b263c85fec36164830869c76f560cad8cb2d`。original Public CI `39227323668`、exact-main Public CI
`39234418094`与Browser Smoke `39234418220`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；fresh
README/doc294/doc295/milestones为4/4 qualifying PASS。independent reconciliation与147-artifact closeout分别为：

```text
c7f941274b1824948f07c0a55cf22b6508b60a54218df9d03d12c3e01dde72db
a0918ed18de68b5a2352d16a17f5eb9a369f51f26313a51720826bcfd5c0056c
```

因此stage applicability capability identity修正合同现已frozen。fresh CONTROL LOOP没有发现并行semantic施工或更早seam；
当前最小合法问题是
[文档296](docs/296-r1-fact-relation-corrected-successor-private-implementation-feasibility-audit.md)限定的docs-only corrected
successor私有实现可行性审计候选。

read-only audit确认current one-shot Fact handoff可以拥有整个private composition attempt并保留original `BudgetContext`，但
handoff不含Relation需要的source blob bytes，因此application必须显式join exact immutable `DerivationInputSet`与claimed handoff，
并逐项复核同一source/policy/scope/profile/classification/Fact attempt/product world。current Relation domain `/0.1`正确拒绝完整
five-kind与multi-path FactSet，request protocol `/0.2`也没有携带修正后的stage ownership、per-product closure与完整obligation
projection，所以current carrier不能冒充successor。

同一audit在不删除Fact、不改变FactSet identity的audit-only validated view中，复用现有closed Relation Provider algorithms处理
five-kind single-path与five-kind two-path worlds；两个Providers分别完成1/1、2/2与2/2、4/4责任。Python 3.10/3.13 ×
normal/`-O`四格fresh attempt 2 semantic digest均为
`27de95e632aaee5b6ef26ac332846184ac79b5011f319ce4d34152c53e003eaa`；现有Fact/Relation窄基线四格各
`Ran 77 tests / OK (skipped=1)`。attempt 1 nonce canonicalization failure与第一次相对PYTHONPATH invocation error均保留为setup
history，不被后续PASS覆盖。

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc296；不修改doc290–295、runtime、tests、Schema、Profile、Policy、Provider、
manifest、persistence、Coverage或post-R1计划。自己的final-byte门、original PR、单独批准的exact-head merge、new exact-main双门、
fresh README/doc296/milestones读回与独立对账闭合后，最多形成qualified feasibility history并返回CONTROL LOOP；不得自动启动
implementation、恢复旧composition A–J或选择manifest/persistence。

### R1 Fact handoff → Relation corrected successor 私有实现授权发布候选

文档296由PR #341 final head `34fba6ca71122d8a71a55ddf98567486744fa189`合入
`main@e8171b93b526f16ca2dee0c90537780cec91a212`。original Public CI `39241157801`、exact-main Public CI
`39247733436`与Browser Smoke `39247733582`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc296/milestones各有一份qualifying PASS；README formal #1的P2 render timeout保留为ERROR，fresh #2才PASS。
independent reconciliation与142-artifact closeout分别为：

```text
bad8c6125ef0e0432d2d81568c0f41edfed7be1e2732857fd5d356d39ac5340f
5b0861c6b1ee31cf09ff5f907ae52e0f0d4627b31d69544bd052db4ecce8041a
```

因此doc296已成为qualified feasibility history。fresh CONTROL LOOP确认#341只改四份文档，当前main没有并行semantic施工或
更早反例；下一最小合法问题是
[文档297](docs/297-r1-fact-relation-corrected-successor-private-implementation-authorization-publication.md)限定的docs-only授权发布。
它只条件化授权doc296 §7 A–J：exact-input/handoff/context join、`/0.2` stage ownership、完整per-product closure、完整obligation
projection、可区分successor carrier、现有Provider assignment、独立qualification/admission与same-attempt continuation。

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与新增doc297。其final bytes、original PR、单独批准的exact-head merge、new
exact-main双门、fresh README/doc296/doc297/milestones读回与独立对账全部闭合以前，`ALLOWED`不生效。闭合以后也必须返回
CONTROL LOOP；不得自动施工successor、恢复旧composition、选择manifest/persistence或启动Coverage、public Review、R2/R3。

### R1 Relation Provider import-form conformance 修正可行性审计候选

文档297由PR #342 final head `dcc5d2c4bccf6ceb69fb52673075446d983d71d2`合入
`main@cd74cfd8d212d200465a86391d2fdb08c123376c`。其original/exact-main门、fresh
README/doc296/doc297/milestones读回与independent reconciliation均已闭合；200-artifact closeout与reconciliation分别为：

```text
9cdd52106ac942b96a16cf4b5df8d11e14bbf95eaba1d4353846b7d0001fe824
9d59a160a3bdacb166b620f169568de2dbd51e843e56dd18eb7eea28759a4799
```

因此bounded corrected-successor implementation authority已经成为`ALLOWED`历史事实。fresh implementation CONTROL LOOP在任何
runtime diff产生以前构造完整import-form world，证明current Fact stage递归产生`Import` / `ImportFrom`、multiple aliases、
relative/star、nested与multi-path `IMPORT_DECLARATION` Facts，而current closed Relation Provider只遍历`tree.body`、只接受
`ast.Import`并要求单alias。完整14-Fact world中的5个import Facts使Provider A 5/5与Provider B 10/10责任均被拒绝；旧plain-import
控制仍完成。该反例命中doc296 §9与doc297 §5，所以历史授权保留但当前不可消费，implementation仍`NOT_STARTED`。

[文档298](docs/298-r1-relation-provider-import-form-conformance-correction-feasibility-audit.md)限定一个docs-only feasibility
candidate。audit-only bounded successor保持完整FactSet，以recursive alias occurrence和authoritative Fact做双向exact matching，
拒绝missing/duplicate/semantic drift，并在legacy plain worlds保持candidate/outcome bytes；expanded domain必须取得新private Provider
algorithm/descriptor identity。Python 3.10/3.13 × normal/`-O`四格semantic digest均为
`14f5eb624116f5712005e05322e08b734379fcb4891b02289553b4b44177e241`，10-artifact feasibility closeout SHA-256为
`2330d91d16d58f67fd852b4921910a4a91025900ef36f0cda28c94b121c100a3`。

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDIT_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R3_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc298；不修改doc290–297、runtime、tests、fixtures、Schema、Profile、Policy、
Provider、manifest、persistence、Coverage或post-R1计划。自己的final-byte local gates、original PR、单独批准的exact-head merge、
new exact-main双门、fresh README/doc298/milestones读回与independent reconciliation闭合后，最多成为qualified feasibility
history并返回CONTROL LOOP；不得自动起草修正合同、施工Provider successor或恢复任何composition authority。

### R1 Relation Provider import-form conformance 修正最小合同候选

文档298由PR #343 final head `51ca59a5ad1bacc63c9f10aaa4bbad8f16fe1962`合入
`main@85bb22896b978b6f9480b58681c69c5b5ac10c55`；original Public CI `39279104121`、exact-main
Public CI `39286685392`与Browser Smoke `39286685584`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。
fresh README/doc298/milestones各有qualifying PASS。setup1的README marker selection错误、setup2的doc298匿名API额度耗尽
formal ERROR均保留；后继fresh identity取得PASS。independent reconciliation与142-artifact closeout分别为：

```text
58552b25d98294099608e177b7f7e750c1862874393ee9533652ebe6df5e7bb3
f0ff0d0166127aca487a782fc589b00447eb7490cee95f647f6438e1d3bed736
```

因此文档298现为qualified history。fresh CONTROL LOOP重新核对current Provider source与doc175/290/294/296/297，没有发现
需要重开Fact truth、application-owned obligation projection、Relation candidate semantics、Policy/Profile、Schema、manifest或
persistence的更早seam。当前最小合法问题是
[文档299](docs/299-r1-relation-provider-import-form-conformance-correction-contract.md)限定的docs-only semantic contract candidate。

文档299冻结complete `IMPORT_DECLARATION` form universe、versioned CPython 3.10.6 alias-occurrence projection、source
occurrence与authoritative Fact双向exact binding、complete assignment/terminal核账、collision-free child ordinal、legacy
candidate/outcome bytes兼容、新private Provider identity与same-attempt authority ceiling。Provider继续只消费application-owned
assignment，不拥有applicability、denominator、qualification或admission。

```text
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_CONTRACT_FROZEN
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_NOT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R3_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc299；不修改doc290–298、runtime、tests、fixtures、Schema、Profile、Policy、
Provider、manifest、persistence、Coverage或post-R1计划。自己的final-byte local gates、original PR、受保护exact-head merge、
new exact-main双门、fresh README/doc299/milestones读回与independent reconciliation闭合后，最多成为qualified contract
candidate。`FROZEN`仍要求后继独立docs-only freeze publication；不得自动恢复旧授权、施工Provider或composition、选择manifest /
persistence或启动Coverage、public Review、R2/R3。

### R1 Relation Provider import-form conformance 修正合同冻结发布候选

文档299由PR #344 final head `fbf4975202327ed22b7fd2ab02de0bd33f5b751c`合入
`main@79be6a2af95a51e01318acc7f41b38100e658197`；original Public CI `39293777777`、exact-main Public CI
`39297621450`与Browser Smoke `39297621269`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc299/milestones各有唯一qualifying PASS。

readback setup1 bootstrap errors、setup2 history initialization error、fresh anonymous rate-exhaustion diagnostics均保留；
formal observation只在fresh exact-commit preflight可用以后启动。independent reconciliation attempt 1因读取不存在的
`final_report_verdict`字段终结为proof-facility schema-key error；attempt 2只读取产品summary实际发出的`verdict`字段，未修改
oracle、formal observations、target、marker、预算、断言或状态规则。attempt 2 reconciliation与153-path closeout index分别为：

```text
fdc062209a0943c884bca364ebe38dcc020a6a450159dc54c44b56d4d67be207
4ad67ab029611b00432addbb727523565c116ad0bcdc8d4816560d95fc5f2455
```

本publication复算发现closeout index把执行时为空、随后由wrapper写入121 bytes终态回显的
`create-closeout-attempt-1.stdout.txt`记为empty digest；其余152项逐项一致。该self-capture finding独立保留，不能把
153-path index叙述成153项全部终态封存；它不改变先于closeout完成的independent reconciliation与3/3 formal资格。

因此文档299现为qualified contract candidate。fresh CONTROL LOOP确认remote main、上游frozen bytes、current Provider source与
停止线连续，没有并行semantic PR或更早反例；下一最小合法问题是
[文档300](docs/300-r1-relation-provider-import-form-conformance-correction-contract-freeze-publication.md)限定的独立docs-only冻结发布。

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_QUALIFIED_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_AUTHORIZED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

文档300只发布文档299已经资格化的semantic bytes；其`CONTRACT_FROZEN` marker在本publication自己的final-byte local gates、
original PR、连续授权的exact-head protected merge、new exact-main Public CI与Browser Smoke、fresh
README/doc299/doc300/milestones installed-product readback及independent reconciliation全部闭合以前不生效。冻结生效后也只能
返回CONTROL LOOP；不能自动授权corrected Provider successor runtime、恢复旧composition、选择manifest/persistence或启动
Coverage、public Review、R2–R6。

### R1 Relation Provider import-form conformance corrected successor 私有实现可行性审计候选

文档300由PR #345 final head `9bca8018cea834507bd2c5ae0bed51ba312260f9`合入
`main@68e6fa0245161dd75b9d7750d3320158bebfa315`；original Public CI `39305312371`、exact-main Public CI
`39309834623`与Browser Smoke `39309834678`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc299/doc300/milestones为4/4 qualifying PASS；independent reconciliation与150-artifact closeout分别为：

```text
4e4a50b33d5ab07acaa4c54f643023f359603b5460605a162d4e9039663d7866
44c856882e33510288570883e49ca0b351e145d07e616c416a8c7d75e3950e43
```

因此`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN`已经生效。readback bootstrap中的wheel
wildcard与PowerShell reserved variable setup errors按原identity保留，均先于formal observation；它们不被后继PASS覆盖，也不被
提升为产品failure。

fresh CONTROL LOOP确认上游Fact truth、stage applicability、per-product closure、complete obligation projection、doc299与current
Relation request/canonicalizer/qualification/admission连续；open PR只有依赖更新。现有legacy Provider仍保持immutable。下一最小合法问题是
[文档301](docs/301-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-audit.md)
限定的docs-only private implementation feasibility audit。

read-only audit使用新的audit-only Provider identity在完整FactSet与application-owned assignment上实现CPython 3.10 import
occurrence projection、AST occurrence与authoritative Fact双向核账、legacy-compatible extension ordinal与完整terminal outcome。
七组positive/control worlds、negative matcher worlds与upstream corrected-successor continuity在Python 3.10 / 3.13 × normal / `-O`
四格产生稳定semantic report；focused regression每格76 passed、1 skipped。当前只允许：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc301；doc290–300、runtime、tests、fixtures、Schema、Profile、Policy、
Provider、manifest、persistence、Coverage与post-R1计划必须保持`68e6fa0…` base bytes。自己的local gates、original PR、连续授权的
exact-head protected merge、new exact-main双门、fresh README/doc301/milestones读回与independent reconciliation闭合后，最多成为
qualified feasibility history。随后必须返回CONTROL LOOP；不能自动授权或施工corrected Provider successor、恢复旧composition、
选择manifest/persistence或启动Coverage、public Review、R2–R6。

### R1 corrected Provider successor feasibility exact-main 资格失败边界审计候选

文档301由PR #346 final head `df6955d59a485027fbc2429090d35d43b52ca3ed`合入
`main@bd0cb9838545de0dd3a2e26486c6fa90df765962`，merge tree与candidate tree均为
`a651589a7879c213a0e54f035e442e1780263074`。original Public CI `39317208755` attempt 1为11/11 SUCCESS，
Browser Smoke `39321768185` attempt 1为1/1 SUCCESS；但exact-main Public CI `39321768248` attempt 1只有10/11，
required `Starter PASS/FAIL golden path` job `118308355830` FAIL。

失败Artifact保留desktop complete与mobile首个loopback document请求`net::ERR_NO_BUFFER_SPACE`；产品正确分类为
`network:mobile / HostSocketNoBufferSpace`，Browser capture incomplete、cleanup complete，bootstrap以
`COLLECTOR_ERROR / ERROR`终结且cleanup complete。更具体host resource cause保持`UNKNOWN`；Subject failure、doc-only
candidate regression与分类缺陷均未建立。禁止rerun、retry until PASS、弱化required lane/oracle/timeout、启动readback或用original
PR绿灯替代exact-main失败。

[文档302](docs/302-r1-relation-provider-import-form-successor-feasibility-exact-main-qualification-failure-boundary-audit.md)
只把失败identity、资格影响与新candidate恢复纪律形成docs-only audit candidate。文档301保持未资格化，`FEASIBILITY_AUDITED`
未生效，implementation仍NOT_STARTED/NOT_AUTHORIZED。本文自己的local/original PR/protected merge/new exact-main双门、fresh
README/doc302/milestones读回与independent reconciliation闭合以前，failure boundary也尚未成为qualified history；闭合后只能返回
CONTROL LOOP，不能以空提交重试旧candidate，也不能启动runtime、恢复composition或进入后续阶段。
### R1 corrected Provider successor 私有实现可行性恢复候选

文档302由PR #347 final head `1586d096f6d51e9b54350e4b14324daaf2c3732c`合入
`main@869e8190d4fcc6f3c046bb1661d6d27f1da36283`。original Public CI `39327705063`、exact-main Public CI
`39330968073`与Browser Smoke `39330968165`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh anonymous
installed-product README、doc302、milestones为3/3 qualifying PASS；independent reconciliation与131-artifact closeout分别为：

```text
071427e5656dbc65d9b4ea18ce148a02d490c363d4761199891b10c20bc68339
92d671cf074919a2116043bfa509a4e571dec2499ba4c80d27af0b66dc568a5a
```

因此failure boundary现为qualified history。#347只修改docs，required Starter workflow/runtime/tests/oracle保持不变却完成自己的
exact-main门；这证明恢复不需要弱化产品门，但不解释#346的`UNKNOWN`资源根因，也不把PASS回填失败world。

[文档303](docs/303-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-recovery.md)
形成具有新责任的docs-only feasibility recovery candidate：它把#346 failed run/job/Artifact/classification与doc302 qualified
closeout纳入自己的独立对账，并在current exact main用新audit identity重新执行Provider successor与upstream continuity witness。
Python 3.10 / 3.13 × normal / `-O`四格semantic digest分别稳定为：

```text
provider successor feasibility recovery
a06190284adcef005010a3ceb069161f2f6528d6111abe5c90596723b5fbeb82

upstream corrected-successor continuity
0caf68d7a78b8ab1279399d5f3b0e258818010f366c2cac6816c7b0a1ef0474b
```

focused regression每格76 passed、1 skipped。本文只允许README、AGENTS、milestones与新增doc303；doc290–302、runtime、
tests、workflows、Provider、Schema、Policy/Profile、manifest、persistence、Coverage与post-R1计划必须保持base bytes。自己的
local gates、original PR、protected exact-head merge、new exact-main双门、fresh README/doc303/milestones readback与independent
reconciliation闭合后，最多成为qualified feasibility history；在此以前implementation仍NOT_STARTED/NOT_AUTHORIZED，旧composition
authority继续不可消费。

### R1 corrected Provider successor 私有实现授权发布候选

文档303由PR #348 final head `68e206ca8a7f22ba63b3e6672f23039446a4a796`合入
`main@0f0c93a7b0fc2d33572dbb284ab7e54a997ea88b`；candidate与merge tree均为
`72c9e720edc3099e0d60c74821d41db0b9de8f2c`。original Public CI `39336445825`、exact-main Public CI
`39340041479`与Browser Smoke `39340041520`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh anonymous
installed-product README、doc303、milestones为3/3 qualifying PASS；independent reconciliation与132-artifact closeout分别为：

```text
4e03b11727cca784a0797bdbaeb9d66fb44be886e8c4072b077c0395a534e430
bbc6f3b018da7591737526a767b5c98fd7b64feda33b132d6ca880c3235ff8e1
```

因此doc303现为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`；doc301保持merged but not-qualified，#346失败、Artifact与`UNKNOWN`
根因不变。[文档304](docs/304-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-authorization-publication.md)
只条件化发布bounded private Provider successor A–J authority，不修改runtime/tests/workflows/Provider/Schema/Policy/Profile、旧composition、
manifest、persistence、Coverage或public Review。它自己的local/original PR/protected merge/exact-main双门、fresh
README/doc303/doc304/milestones readback与independent reconciliation全部闭合以前，`ALLOWED`不生效；闭合后仍为
implementation NOT_STARTED，并必须返回CONTROL LOOP。

### R1 corrected Provider successor 私有实现候选

文档304由PR #349 final head `b5d66949657449efa5cbfc6315d810696f76e861`合入
`main@4411c02c7278b8ecb4aa36415fdea77e7cb90168`；candidate与merge tree均为
`7e13b5d8acf374c5e9e854554824b28ad606f677`。original Public CI `39344764110`、exact-main Public CI
`39348029772`与Browser Smoke `39348029859`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh anonymous
installed-product README、doc303、doc304、milestones为4/4 qualifying PASS；independent reconciliation与178-artifact closeout分别为：

```text
cbe3144f61e7e68b9bee9af11f463ebc38ec017d50fd98c2a6fde4742dc19d2e
fe760ad7716b0d62ec22b37a906e6031e7ff152bb4838ec5e7114dbb69d815a0
```

因此bounded private Provider successor A–J authority已经生效。[文档305](docs/305-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-candidate.md)
在exact base `4411c02c…`上形成独立implementation candidate：新增versioned private binding/profile/wire与Provider，保持完整FactSet，
枚举CPython 3.10 import-form occurrence，执行双向Fact核账、per-path MODULE closure、完整assignment与legacy-compatible ordinal，并复用
既有qualification/admission/lifecycle。旧Provider/public/default composition不变。

prequalification review在formal qualification以前发现并修正UTF-8-SIG首行BOM byte-offset defect与RPIF-013 proof target过弱；两项
identity及修正前focused日志继续保留。final focused四格均为95 reported / 94 passed / 1 skipped；full Review Attention四格为531
reported，Python 3.10每格528 passed / 3 skipped，Python 3.13每格529 passed / 2 skipped。semantic report attempt 1 method error与
attempt 2 non-semantic timestamp mismatch均保留，attempt 3四格digest一致：

```text
1d663d655365cddbcb00375066fbd523475586cc754ee461be3695628ed06c6c
```

本文仍只是本地candidate。它必须取得自己的original PR gate、protected merge、new exact-main双门、fresh README/doc305/milestones
readback与independent reconciliation；全部闭合最多为`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED`。
`FROZEN`只能由后继独立docs-only publication取得。旧Fact handoff → Relation composition authority继续不可消费，manifest、
persistence、Coverage、public Review与R2–R6均未启动。

### R1 corrected Provider successor 私有实现冻结发布候选

文档305由PR #350 final head `cb46053b9dc73e53b7cea0f37a1ec34baaa8deea`合入
`main@b4438d29cbd856d5ccbc3a4ef9cb0040de13da74`；candidate/merge tree均为
`d05cb480f77288b34ba994eb5a1547261dec80ce`。original Public CI `39361779895`、exact-main Public CI
`39364238110`与Browser Smoke `39364238111`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh anonymous
installed-product README、doc305、milestones为3/3 qualifying PASS；independent reconciliation与133-artifact closeout分别为：

```text
1394b9678ab5abc7b2a141bdb0434dae16770e9ceb2dc08f9cd912437cea109d
addf39c28a3bfe04b63cd739e6d8d5a3956a0684c499c1a2f5e5795304ab7352
```

closeout wrapper的stdout self-capture mismatch已单独保留；其余132项终态一致，semantic与qualification effect均为`NONE`。因此
doc305现为`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。

[文档306](docs/306-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-freeze-publication.md)
只条件化发布private implementation frozen target，tracked scope只允许README、AGENTS、milestones与新增doc306。它不修改runtime、
tests、workflows、Schema、Policy/Profile、旧composition、manifest、persistence、Coverage或public Review。自己的local/original PR/
protected merge/new exact-main双门、fresh README/doc305/doc306/milestones readback与independent reconciliation全部闭合以前，
`FROZEN`不生效。闭合以后必须返回CONTROL LOOP，重新审计Fact handoff → Relation composition authority；旧authorization history
继续`PRESERVED / NOT_CONSUMABLE`，不能由implementation freeze自动恢复。

### R1 Fact handoff → Relation corrected successor authority recovery 当前状态审计候选

文档306由PR #351 final head `5b6ee8bbb3586e89fec3133960265b3f450a26d8`合入
`main@6cbd7ae5088bb232cbb64e51acc7298441272ab6`，tree为
`8026bbab89d5e2856fe8660a9dc36cc016f5ed66`。original Public CI `39368437171`、exact-main Public CI
`39370392129`与Browser Smoke `39370391965`均为attempt 1 SUCCESS；fresh README/doc305/doc306/milestones为4/4
qualifying PASS。independent reconciliation、finite closeout与finite-integrity summary分别为：

```text
43b74760aef0dcb102e0d0d8fcbd6ba068af7e1521f44b53db18f158613dafda
bc0a7f29b80272eb8287598529c1bc9fae0490837645593b522b91af5e165abe
bed71633b03a65bed58ddde4d0476ce3dd0478732ba8a22e40be3347210d2555
```

因此corrected Provider successor private implementation现已frozen。fresh CONTROL LOOP确认新versioned Provider已经在完整
FROM_IMPORT、five-kind、multi-alias与two-path FactSet上解决旧Provider stop condition，但这只取得Provider conformance authority。
current combined-policy Fact entry仍正确fail closed；Fact-only handoff不能与combined-Policy exact input跨world join；high-level
Relation entry仍创建新BudgetContext并重跑Fact；import-form carrier没有handoff claim、original context、stage applicability、
cross-stage ownership、per-product closure、complete obligation projection与expected/assigned obligation identities。因此
Fact handoff-owned Relation transition/admission仍不存在。

[文档307](docs/307-r1-fact-relation-corrected-successor-authority-recovery-current-state-audit.md)只形成current-state audit
candidate。audit在Python 3.10.6 / 3.13.13 × normal / `-O`四格取得同一semantic digest：

```text
a2a96debfb98ddaf176057489493dbc917dcad3a898a295778ea43c7f9b58437
```

fresh focused attempt 2四格各200 reported / 199 passed / 1 skipped；attempt 1的错误module name loader failure保持
`NON_QUALIFYING / NONE`。本candidate只允许README、AGENTS、milestones与新增doc307；doc290–306、runtime、tests、workflows、
Provider、Schema、Policy/Profile、manifest、persistence、Coverage与public Review必须保持base bytes。自己的local/original PR/
protected merge/exact-main双门、fresh README/doc307/milestones readback与independent reconciliation闭合后，最多成为
`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，单独考虑docs-only corrected successor authority
recovery publication；旧authority仍`PRESERVED / NOT_CONSUMABLE`，transition implementation仍`NOT_STARTED / NOT_AUTHORIZED`。

### R1 Fact handoff → Relation corrected successor authority recovery publication candidate

文档307由PR #352 final head `ed5211609271dd522b3ca474201b76cc02748139`合入
`main@2a461ad476aaeed207f4d60bcabd3e235c4aba7e`。original Public CI `39375812065`、exact-main Public CI
`39378248233`与Browser Smoke `39378248142`均attempt 1 SUCCESS。fresh doc307、milestones与README各有唯一qualifying
PASS；README formal #1的P1 API额度耗尽错误完整保留，reset后的fresh formal #2才取得PASS。independent reconciliation、
162-artifact closeout与finite integrity分别为：

```text
e78ebd5296652e0168b73ef73cb1d8dbbd26ae2c7078379a76217e485435ef50
f10c27507f7fa799675525a0e8820dffe0c9aaf25fe27beee2cc1f16634efc27
44a2ca60f68f8fd458f19ad022e6a1c4fbb326af21b8726c208064a247b8ba44
```

因此doc307现在是`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。fresh CONTROL LOOP确认Provider stop condition已由冻结的
versioned import-form Provider解决，但common exact input + live handoff → corrected Relation admission transition仍不存在；旧doc297
authority继续保留历史且不可消费。

[文档308](docs/308-r1-fact-relation-corrected-successor-authority-recovery-publication.md)只条件化恢复一个bounded、private、
versioned、handoff-owned transition A–J：绑定exact input、一次领取的完整Fact handoff与original live BudgetContext，构造冻结的stage
applicability、per-product closure与complete obligation universe，复用已冻结import-form Provider，再独立核对expected/emitted/terminal
partition与same-attempt provenance。它不得过滤FactSet、缩小Policy、新建claim/context、重跑Fact、跨world join、改写legacy/public
bytes或恢复旧ReviewSliceSet/Coverage composition。

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与新增doc308；自己的local/original PR/protected merge/exact-main双门、fresh
README/doc307/doc308/milestones readback与independent reconciliation全部闭合以前，`ALLOWED`不生效。闭合以后也必须返回
CONTROL LOOP，才允许从新exact main创建implementation branch；不得自动启动manifest、persistence、Coverage、public Review或R2–R6。

### R1 Fact handoff → Relation corrected successor 私有 transition 实现候选

文档308由PR #353 final head `fa7eb63aa450ab56925304cc94b7bb736b028f59`合入
`main@aabab17ee183f6eec29b38658b044734016b197f`，candidate/merge tree均为
`2b79c2802e35824284d3862f0f5573192f3c8843`。original Public CI `39384052591`、exact-main Public CI
`39386875212`与Browser Smoke `39386875311`均为attempt 1 SUCCESS；fresh README/doc307/doc308/milestones为4/4
qualifying PASS。independent reconciliation、finite closeout与finite integrity分别为：

```text
38db55054abc1e1a123e9b9d1fc8de5b011240404491a1f1751b3014df41213a
5c671ea25a53bc4e0fae128e5fb4f91b2697be247463bf4af9c9cbf166bcd76f
f25a1d65a624abb7a9c1d1f7c30d779ee783028fd848417cfdafbdd9d79a722c
```

因此`R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。
[文档309](docs/309-r1-fact-handoff-relation-corrected-successor-private-transition-implementation-candidate.md)在该exact main上形成
bounded private transition candidate：它从专用Relation handoff domain一次性领取完整Fact source与original live BudgetContext，
机械复算完整Policy的stage ownership、逐product/path closure、三类total Fact partition与complete successor obligation universe，
复用冻结的import-form Provider并独立核对assignment、emitted/terminal partition、request provenance与same-attempt lineage。carrier
copy-own完整Fact handoff history，admission绑定完整carrier，one-shot continuation的authority ceiling不包含ReviewSliceSet、Coverage、
manifest、persistence或public Review。

prequalification working-byte review保留十六项已修正finding，包括subject/path混用、assignment与terminal假设、Coverage/Relation
handoff串域、Coverage negative path回归、carrier/admission绑定不足、Fact partition遗漏STRUCTURAL_ANCHOR、successor obligation
identity不足、complete Fact history遗漏、doc309 exact base tree误抄、live source/context/provenance未与独立operand重绑定，以及
Provider terminal/receipt/RelationSet未从frozen wire独立重建、第10/11项修正首跑把terminal helper导入错误模块，以及下一run把
carrier helper插入到RelationSet constructor return以前。后续复核又发现provenance校验重造`resolved_at`、attempt/claim/timestamp只在
carrier内部互相引用，以及foreign Policy Provider lineage可自洽地跨入外层exact world；三项均以新direct falsifier实证并修正。
全部发生在commit/PR/formal product identity以前；修正前working logs、第10/11项发现前的四格focused与3.10 normal full成功、
第12项loader failure、第13/14项31-test/18-error run及第15/16项单测failure保持非资格证据，
final bytes必须重新完成Python 3.10/3.13 ×
normal/`-O` focused/full matrix与semantic comparison。现有final focused四格均为108 reported / 107 passed / 1 skipped；
full四格均为564 reported，其中Python 3.10两格为561 passed / 3 skipped，Python 3.13两格为562 passed / 2 skipped。
semantic report 0.1因按attempt-bound obligation identity顺序投影assignment产生139项位置差异，已保留为
`SEMANTIC_REPORT_ASSIGNMENT_ORDER_PROJECTION_ERROR`且未建立产品分歧；versioned 0.2按稳定义务内容排序后，在default、multi-path、
known-empty、optional-advisory与UTF-8-SIG五个world的四格共同digest为
`2bd6c43da6a1a24450031df71638f83533527b93b05fa68076545eafaa9f9193`。compile attempt 1未创建独立pycache根、attempt 2的
镜像目标路径达到277--319字符，两次均只建立proof-facility setup error且没有`SyntaxError`/`IndentationError`；fresh短前缀的
attempt 3在Python 3.10/3.13均exit 0。diff、Markdown/local links、global/local hygiene、private export、exact eight-path scope与
primary audit continuity也已PASS。首个pre-PR commit又证明工作树`git diff --check`遗漏untracked doc309的两处行尾空格；
commit `9896b654…`、exit 2输出与错误local qualification/seal attempt 1保留，最终字节改用base-to-candidate commit-range门并
重新封存。因此当前为`IMPLEMENTATION_CANDIDATE / LOCAL_GATES_PASS / NOT_QUALIFIED / NOT_FROZEN`。

当前状态上限为本地`IMPLEMENTATION_CANDIDATE / LOCAL_GATES_PASS / NOT_QUALIFIED / NOT_FROZEN`。它必须完成自己的single candidate commit、
original PR、protected exact-head merge、new exact-main Public CI与Browser Smoke、fresh README/doc309/milestones installed-product readback、
independent reconciliation与finite closeout；全部闭合也只能取得`EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。冻结必须由
后继独立docs-only publication取得；旧ReviewSliceSet/Coverage composition authority继续不可消费，manifest successor未选择，
persistence保持OPEN，public Review与R2–R6均未启动。

### R1 Fact handoff → Relation corrected successor 私有 transition 实现冻结发布候选

文档309的implementation candidate已由PR #354从exact base
`aabab17ee183f6eec29b38658b044734016b197f`、head `8a41ddeaae9087589d16aec8f5ceb9bffc2fb428`、tree
`9b230e69eca15379da0a75f428767373c9a89946`精确合入`main@eadccc6023196e5b31c3bf312f5de2c4578d2f5d`。
original Public CI `39413230303`与exact-main Public CI `39416474939`均为attempt 1的11/11 SUCCESS，Browser Smoke
`39416474952`为attempt 1的1/1 SUCCESS。fresh README/doc309/milestones各有唯一qualifying PASS，Plan/session/report分别为：

```text
doc309     r1-fr-trans-impl-formal-doc309-1-eadccc6     github-paired-86e6781ed6f94739b4a79f8917464a67     75b4901939c4d481e06b2f700a5170f7a2a87aa84311c777a1ac7dd92cb1a85c
milestones r1-fr-trans-impl-formal-milestones-1-eadccc6 github-paired-60ac576f781647df8954ef2bb582b7d9     e418098209105bb7aa7021872af442820acc9f2ba6c474cad972abc783a121c0
README     r1-fr-trans-impl-formal-readme-1-eadccc6     github-paired-48d1e7a85df44786b1c9bc2072b24922     d9b3cf9d1d130be0015b270887e33e7ba6eb29f384a284834dc4ec8d0c021623
```

independent reconciliation、155-artifact closeout、post-closeout stdout self-capture record与finite integrity的SHA-256分别为：

```text
3fad5d6aed4b0054750207bd527580373e096513eafc9cc2e4be330ed322e938
984beb7124a79b64e5bca446afefe54ff0ba741350891759f78f5ac9bba5d252
9cd19ee0228a7e3ba5e29e296e609e0c519833f8f2d78a50006e15b1c37ff1bc
e750bfec27f1d246ad4d9148259450e294619b4d8a4e6f69c08ddae00f958073
```

milestones diagnostic #1在约30秒navigation后以`PublicRenderNetworkError`终结，底层原因保持`UNKNOWN`；fresh匿名rate/commit
preflight后独立diagnostic #2为COMPLETE。首个ERROR没有被覆盖。closeout wrapper在enumeration前打开自己的stdout，形成唯一
self-capture mismatch；其余154项终态一致，semantic与qualification effect均为`NONE`。因此candidate现在只能记录
`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。

[文档310](docs/310-r1-fact-handoff-relation-corrected-successor-private-transition-implementation-freeze-publication.md)是独立docs-only
conditional freeze publication，只允许README、AGENTS、milestones与新增doc310。它自己的final-byte local gates、original PR、
protected exact-head merge、new exact-main Public CI与Browser Smoke、fresh README/doc309/doc310/milestones installed-product readback、
independent reconciliation与finite closeout全部闭合以后，才允许
`R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN`生效。随后必须返回CONTROL LOOP；旧
ReviewSliceSet/Coverage composition authority不会自动恢复，manifest successor、persistence、Coverage/public Review、post-R1
Benchmark与R2–R6均不得自动启动。

### R1 ReviewSliceSet / Coverage composition authority recovery 当前状态审计候选

文档310由PR #355从base `eadccc6023196e5b31c3bf312f5de2c4578d2f5d`、head
`c2dd1ed7b9b8d2cb6e82a523eadfabbc390ae77b`、tree `43ac035e0cd2e012fac5b390f54244f591551a40`
精确合入`main@e88310ca1c4c5a382d097e8d0b68193b106549c5`。original Public CI `39421644660`、exact-main
Public CI `39425547417`与Browser Smoke `39425547424`均为attempt 1 SUCCESS，分别为11/11、11/11与1/1。fresh
doc309、doc310、milestones与README为4/4 qualifying PASS；independent reconciliation、162-artifact closeout与finite
integrity分别为：

```text
f4fac71760ebb77cc676e2040852be29d6df36ee1da9e0f02e5cad55af5232e5
bd97fe2171315408a2248bcd2e045946d7727865d1aa6b816abb265d72552054
671d65e2680a0c69ef785cbbfe43ef9089f8d907dda71186c678555a9abb5d37
```

因此Fact handoff → Relation corrected successor private implementation现已frozen。fresh CONTROL LOOP不直接恢复旧composition，
而由[文档311](docs/311-r1-review-slice-set-coverage-composition-authority-recovery-current-state-audit.md)重验current authority topology。
新transition admission为`QUALIFIED`，默认world保留14个Facts、10个obligations与10个Relations；one-shot continuation保持同一
`DerivationInputSet`、`BudgetContext`与`AttemptEligibility`。但transition authority ceiling继续令ReviewSliceSet/Coverage为false，
current Slice入口只接受exact `OwnedRelationQualificationContinuation`，并对`OwnedFactRelationTransitionAdmission`与
`ClaimedFactRelationTransitionContinuation`均以`ADMISSION_BINDING_REJECTED` fail closed。源码没有新continuation consumer或
到legacy Slice authority的adapter；相同content、RelationSet、inputs/context/eligibility或digest不能绕过该边界。

read-only audit在Python 3.10.6 / 3.13.13 × normal / `-O`四格取得同一semantic digest：

```text
29a2cc8b30cd43b18cb8be214de88803dfdf9879e0930129a9ed26f7b943608b
```

audit attempt 1的postponed annotation object-identity proof-facility error与focused attempt 1的test-root loader error均保留，
semantic/qualification effect为`NONE`。fresh audit attempt 2四格一致；fresh focused attempt 2四格各`193/193 PASS`，summary为
`770cf74e9a42158ac3637c04d21d40775eb02b1bb67c7b3a9e0b0d8dcbcefaf3`。

当前裁决是Fact → Relation stop condition只解决到Relation admission；旧doc288 composition authorization保持历史但不可直接消费。
文档267/287的versioned Slice successor与A–J semantics仍可作为design basis，下一最小合法seam是一个docs-only composition
authority recovery publication，至多条件化授权application-owned `RELATION_TRANSITION_TO_SLICE_AUTHORITY_BRIDGE`：消费exact
one-shot transition continuation、独立重验admission/history/inputs/context/eligibility，再签发与existing Slice primitives兼容的
successor authority。它不能修改transition ceiling、放宽legacy type gate、伪造legacy qualification、重跑Relation或选择
manifest/persistence。

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_RESOLVED_THROUGH_RELATION_ADMISSION_ONLY
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本候选只允许README、AGENTS、milestones与新增doc311；doc267、doc287–310、runtime、tests、workflows、Schema、Policy/Profile、
manifest、persistence与全部保留evidence必须保持base bytes。自己的final-byte local gates、original PR、protected exact-head merge、
new exact-main双门、fresh README/doc311/milestones readback与independent reconciliation闭合以后，最多成为
`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，单独发布docs-only composition authority recovery；不得从
本审计直接施工bridge、启动ReviewSliceSet/Coverage runtime或选择manifest/persistence/public Review/R2–R6。

### R1 ReviewSliceSet / Coverage composition authority recovery publication candidate

文档311已由PR #356从base `e88310ca1c4c5a382d097e8d0b68193b106549c5`、head
`af9e8c225efe14d5a9a3f5a0fb729f2fb6dbb360`、tree `b2c8e9dfd0cf2adb3e87ffbf8b1b01c9b044f155`
精确合入`main@35e99a872d33234c4fb923a64995ccb148d9e3ba`。original Public CI `39435033981`、exact-main
Public CI `39439635290`与Browser Smoke `39439635449`均为attempt 1 SUCCESS，分别为11/11、11/11与1/1。
fresh README/doc311/milestones各有唯一qualifying PASS；setup1/2 marker投影边界、setup3 README formal #1/#2与
milestones formal #1的non-success全部原样保留。independent reconciliation与230-artifact finite closeout分别为：

```text
71bc49fcb4c6c0b943f5c825cf61d885cd914f54d82253b5345fa607a397ad4f
7a062bb3589d2252b3e999eda48338c5949c18fb3b970affb70efeeb56a432ba
```

因此doc311是`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。fresh CONTROL LOOP选择
[文档312](docs/312-r1-review-slice-set-coverage-composition-authority-recovery-publication.md)作为独立docs-only authority recovery
publication。它不复活doc288 identity，也不修改Fact → Relation transition ceiling或legacy Slice gate；最后门闭合后最多条件化
授权application-owned、versioned、private、one-shot `RELATION_TRANSITION_TO_SLICE_AUTHORITY_BRIDGE`与文档267/287限定的
composition A–J。

新bridge必须消费exact transition continuation并独立重验transition identity/version、qualified admission、complete expected/
emitted/terminal equality、complete RelationSet、same-attempt lineage、original `DerivationInputSet`、live `BudgetContext`与
`AttemptEligibility`。相同bytes、digest、members或semantic result都不是Slice authority。不得放宽legacy exact-type gate、暴露或
复用private token、伪造legacy qualification、创建新claim/context、重跑Relation，或按successful/representable subset缩小Slice/
Coverage denominator。

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc312；doc267、doc281、doc287–311、runtime、tests、workflows、
Schema、Policy/Profile、Fact/Relation transition、legacy Slice、CoverageLedger、manifest、persistence与全部保留evidence必须保持
base bytes。自己的final-byte local gates、original PR、protected exact-head merge、new exact-main双门、fresh README/doc311/
doc312/milestones readback、independent reconciliation与finite closeout全部闭合后，才允许
`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED`生效。随后必须从新exact main返回CONTROL LOOP；
implementation仍为`NOT_STARTED`，不得自动选择manifest/persistence或启动public Review/post-R1 Benchmark/R2–R6。

### R1 ReviewSliceSet / Coverage composition 私有实现候选

文档312已由PR #357 final head `e4503ad0392c762eaf2abeed5597b31c6853934b`从exact base
`35e99a872d33234c4fb923a64995ccb148d9e3ba`受保护合入`main@36333195833a462169e883aab0d36637e2edbdf3`；
candidate/merge tree均为`3731a6211abf976fd98d7e67b7ac315154ef1201`。original Public CI `39455940067`、
exact-main Public CI `39460190492`与Browser Smoke `39460190387`均为attempt 1 SUCCESS；fresh README/doc311/doc312/
milestones 4/4 PASS，independent reconciliation、finite closeout attempt 2与finite-integrity summary分别为：

```text
9a78a3df2dcc9117b49c2dea31cfad62cd3f8d683e64d71caec0371caf825d33
da1855844e36ebcfc32a84873b988b88738e919fbc2c96addd62608005b0bafc
82ea3195bca5e6bfea10c720b37e368df232ff483dd9145b41856f40dc8cccc1
```

closeout attempt 1 stdout self-capture mismatch保持原identity。因此
`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED`已生效。fresh CONTROL LOOP以该exact main建立
[文档313](docs/313-r1-review-slice-set-coverage-composition-private-implementation-candidate.md)及private implementation branch。

本候选新增application-owned、versioned、private、one-shot Relation transition → Slice authority bridge。它只消费exact
`ClaimedFactRelationTransitionContinuation`，在任何Slice work前重新绑定qualified admission、complete Provider lineage/
RelationSet/terminal history、obligation projection、original live `DerivationInputSet`、`BudgetContext`与`AttemptEligibility`。
foreign、consumed、digest-only、fresh-context、resealed identity/history和legacy token必须fail closed；bridge不得改写transition ceiling、
放宽legacy Slice exact-type gate、创建新claim/context或重跑Relation。

Slice obligation producer之后必须由独立validator直接从冻结Policy/Profile、complete FactSet、RelationSet与accepted paths重建完整
denominator；producer与validator共同漏项的falsifier不得通过。multi-path逐path MODULE closure、normal/partial、conflict unknown与valid
closed-empty必须保留不同terminal semantics。private ReviewSliceSet membership与authority分离；missing、duplicate、foreign、mutated或
cross-attempt member不能取得admission。

Coverage只构造七阶段`S/A/N/D`、ordered Fact/Relation/Slice root chain与exactly-once terminal accounting；CoverageLedger 0.3继续只作
validation witness，不生成上游事实、Slice authority、manifest、persistence或publication authority。legacy Slice三个实现文件由exact
SHA guards保护，public/default composition、Schema、Policy/Profile、workflow与R2–R6保持不变。

final focused四格在Python 3.10.6/3.13.13 × normal/`-O`各140/140 PASS。full四格各574 reported；3.10各571 passed/3
skipped，3.13各572 passed/2 skipped。default、multi-path与zero-anchor semantic report四格逐字一致：

```text
ac29917eb0303931abbba15e25499f80fd39782562f0578c021fd119d5717048
```

`py_compile`、diff、Markdown/local links、global/local hygiene、public export/pyproject/workflow guard与primary `audit.json`
continuity必须在final bytes重新闭合。semantic report首次读取不存在的`coverage_ledger_function`，归为proof-facility schema-key
error并保留；修正只改读实际`artifact_kind / schema_version`，未修改产品或oracle。此前obligation/provider-id混淆、zero fixture、
coverage inspection与conflict falsifier findings均为formal前prequalification history，不得覆盖或冒充正式产品失败。

本candidate预期scope只允许README、AGENTS、milestones、doc313、新private composition模块与对应test。doc267、doc281、
doc287–312、legacy Slice、Fact/Relation transition、CoverageLedger conformance、manifest、persistence与全部保留evidence必须保持base
bytes。状态上限为：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

single candidate commit、original PR gates、protected exact-head merge、new exact-main Public CI/Browser Smoke、fresh anonymous
installed-product README/doc313/milestones readback、independent reconciliation与finite closeout全部闭合后，最多升级为
`EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。随后必须返回CONTROL LOOP，另建docs-only freeze publication；不得从
candidate PASS直接选择manifest/persistence或启动public Review/post-R1 Benchmark/R2–R6。

### R1 ReviewSliceSet / Coverage composition 私有实现冻结发布候选

文档313 candidate已由PR #358从base `36333195833a462169e883aab0d36637e2edbdf3`、head
`20789a22440cce40fab1a62c315ba21a11ae6e0e`、tree `4b478f917d21b6bc7f3e91f01c480c21591d0cbf`精确合入
`main@7ae964fd86b45802ed77444bbffcf36caef20796`。original Public CI `39482381263`、exact-main Public CI
`39486901626`与Browser Smoke `39486901758`均为attempt 1 SUCCESS；fresh README/doc313/milestones 3/3 PASS。
independent reconciliation、157-artifact finite closeout与finite integrity分别为：

```text
5112c50336484c7c9a55ef03ac2b077ac232c220f5737dfb10a51f2c646d8ce9
52f89095522a8bf7a89d04bc22ac3e1610c4d84be76fb326853443596e2b380c
33f0b418f84f7be89aca3149513c332f6e4b8409356a3bbc49ecf18e4fd65cd6
```

因此doc313现在是`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。第一次freeze publication
PR #359的original Public CI `39492871239` attempt 1因锁定`vite@8.2.2`命中`GHSA-698v-4r3x-3vcv`而以9 SUCCESS /
1 FAILURE / 1 SKIPPED终结；PR关闭且未合并，永久保持`CLOSED / UNMERGED / NOT_QUALIFIED`。R1 runtime或docs-only
regression未建立，exact registry propagation cause保持`UNKNOWN`，禁止rerun或后继PASS回填。

独立maintenance PR #360仅将`web/package.json`与`web/package-lock.json`中的Vite更新为8.2.4。两次fresh构造、local
Workbench/lint/build/audit、original Public CI `39495044192` 11/11、受保护合入`main@3d2b230d0d00695a10fe2ff2f73d950e1674d2e6`、
exact-main Public CI `39499480536` 11/11、Browser Smoke `39499479537` 1/1、fresh installed Workbench readback与独立reconciliation
均PASS。maintenance reconciliation与66-artifact closeout分别为：

```text
a06b2e9823b1fd4e620de38a0e6f53b9d2df09ce8b13c30e269c33656574b01d
e6316e4db5b8292be1bbaa3c6de7fc56c7bfeb2ce0e88b0fd9ec0e7f31ffece9
```

fresh CONTROL LOOP从该新exact main重建[文档314](docs/314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)
作为新的独立docs-only conditional freeze publication。它只允许修改README、AGENTS、milestones与新增doc314；doc267、doc281、
doc287–313、private runtime、tests、workflows、Schema、Policy/Profile、Fact/Relation/Slice实现、CoverageLedger conformance、manifest、
persistence与全部历史合同保持base bytes。它不复活或回填#359。

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_READBACK_QUALIFIED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication自己的final-byte local gates、original PR、protected exact-head merge、new exact-main Public CI与Browser Smoke、fresh
README/doc313/doc314/milestones installed-product readback、independent reconciliation与finite closeout全部闭合以后，才允许
`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN`生效。随后必须从新exact main返回CONTROL LOOP；不得
自动选择manifest successor、persistence route或启动public Review、post-R1 Benchmark与R2–R6。

### R1 Review derivation manifest negative-world successor 可行性审计候选

文档314已由PR #361从`base=3d2b230d0d00695a10fe2ff2f73d950e1674d2e6`、
`head=accf3c977bdadb88e27e2261bc870fb24e85f6a3`、`tree=4e696754b30dbd5e6f057ca9cc856261cf78bdf1`
精确合入`main@add5a8c7359cf9f0a678ea2bf947ef3a9791f94d`。original Public CI `39504016890`、exact-main Public CI
`39507399748`与Browser Smoke `39507399981`均为attempt 1 SUCCESS；fresh README/doc313/doc314/milestones 4/4 PASS。
independent reconciliation与180-artifact finite closeout分别为：

```text
0d2d26172d0d036ebb4bea2f65fe5432959c3cfb694de67df58c38e874a5d827
8487aef23ff3eef55bfdcc32ad9c2fe77c719964ecd34b0409826d8d1731460d
```

因此private composition implementation已经frozen。fresh CONTROL LOOP建立
[文档315](docs/315-r1-review-derivation-manifest-negative-world-successor-feasibility-audit.md)，只读审计immutable manifest 0.1、
CoverageLedger 0.3八个qualified worlds与bounded presence-projection topology。首轮harness导入根错误保留；fresh attempt 2在
Python 3.10.6/3.13.13 × normal/`-O`四格全部PASS且canonical report SHA-256一致：

```text
834e1cd107c1d9fdad74a611823e5cb10e4b2c91443c354d624457a82ee2f039
```

focused regression四格各46/46 PASS。当前结论只支持bounded versioned successor topology可行；正式version、Schema、
conformance identity与实现authority仍未选择。

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_FEASIBILITY_AUDIT_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc315。自己的local gates、original PR、protected exact-head merge、new
exact-main Public CI与Browser Smoke、fresh README/doc315/milestones installed-product readback与independent reconciliation全部闭合后，
最多成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；不得从审计直接创建successor Schema/runtime、
选择persistence或启动public Review/post-R1 Benchmark/R2–R6。

### R1 Review derivation manifest negative-world successor 最小合同候选

文档315已由PR #362精确合入`main@a4fb97ea1a98dbe3014bbae17635396e2d676c85`，tree
`8b810bd2acb89bb0865ace2a92521e36617dcd6d`。original Public CI `39512467514`、exact-main Public CI
`39515876073`与Browser Smoke `39515876085`均为attempt 1 SUCCESS。fresh doc315/milestones与versioned README marker
successor各有一份qualifying PASS；README第一次formal marker selection ERROR按原identity保留，不回填。independent
reconciliation与184-artifact finite closeout分别为：

```text
cefd7f3f37130cada58135060cfca5bde2afd0e6c94e49bb282914d015cda0a3
f821a4ed7f94bfdedfc171806dd8b2f192e151652047e2efceca66a2af2d4470
```

因此doc315已成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。fresh CONTROL LOOP建立
[文档316](docs/316-r1-review-derivation-manifest-negative-world-successor-contract.md)，选择immutable 0.1的唯一0.2 successor、
新`COVERAGE` outcome、4项固定前缀、按Ledger presence projection出现的Fact/Relation/Slice carriers与最后一份Ledger。
cross-artifact conformance identity固定为`r1-review-derivation-manifest-coverage-topology/0.1`；Schema validation不能替代它，
manifest不复制或推断root truth。

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_FEASIBILITY_AUDITED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_CANDIDATE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本contract candidate只允许README、AGENTS、milestones与新增doc316。自己的完整资格链闭合后最多为
`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`；必须再经独立docs-only freeze publication的完整资格链才允许contract frozen。
随后仍须返回CONTROL LOOP独立审计implementation feasibility；不得直接创建Schema、fixture、runtime、persistence或public产品。

### R1 Review derivation manifest negative-world successor 合同冻结发布候选

文档316已由PR #363从`base=a4fb97ea1a98dbe3014bbae17635396e2d676c85`、`head=18044cdb8b02a01d42c2571af18a4592d6a35e74`、
`tree=7ecf71e1e0d05cd3acf7b4fe9e503085c024c3b6`精确合入`main@a0dd817d4fd1743a2de9d5e040afaee2a65697ed`。
original Public CI `39521206997`、exact-main Public CI `39523916099`与Browser Smoke `39523916109`均attempt 1 SUCCESS；
fresh README/doc315/doc316/milestones 4/4 PASS。independent reconciliation与184-artifact closeout为：

```text
9a046576e8404c4615676be0c1338454b0204053e635554ed12dd1a96add4e29
e45c95c54c0e5bbd768b134cb3ea1acbccb6b547d7eaad2cab525bf34f1b744c
```

因此doc316是`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。fresh CONTROL LOOP建立
[文档317](docs/317-r1-review-derivation-manifest-negative-world-successor-contract-freeze-publication.md)，只条件化发布
`R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN`。它不修改doc316、Schema、fixture、runtime、tests、
workflows、CoverageLedger 0.3、composition或0.1 bytes。

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_FEASIBILITY_AUDITED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与新增doc317。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc316/doc317/milestones readback、independent reconciliation与finite closeout全部闭合以后，才允许contract frozen生效。
随后必须返回CONTROL LOOP独立审计implementation feasibility；不得直接创建Schema、fixture、runtime、persistence或public产品。

PR #364已把doc317精确合入`main@8cdd613c3848476f7c4c0162f42581dc32903a33`；original/exact-main双门、fresh
README/doc316/doc317/milestones、independent reconciliation与174-artifact closeout全部闭合，因此
`R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN`已生效。fresh CONTROL LOOP的
[文档318](docs/318-r1-review-derivation-manifest-negative-world-successor-implementation-feasibility-correction-audit.md)
发现两个正交的unproved upstream seams：四个Fact阻断world只有one-shot handoff与fixture，没有owned Coverage result；corrected
transition/composition没有same-attempt DerivationEvidence carrier，legacy Evidence projection又只接受旧
`OwnedRelationSetAdmissionState`。合同未被击穿，但manifest implementation必须保持`NOT_STARTED / NOT_AUTHORIZED`。

文档318只允许README、AGENTS、milestones与新增doc318。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc317/doc318/milestones readback、independent reconciliation与finite closeout全部闭合以后，最多发布
`IMPLEMENTATION_FEASIBILITY_AUDITED_BLOCKED_BY_UPSTREAM_PRIVATE_AUTHORITY_GAPS` qualified history。随后必须返回CONTROL LOOP，
独立审计`NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY`；不得直接创建manifest 0.2 Schema、fixture、producer、Evidence、persistence或
public Review产品。

### R1 negative-world Coverage authority recovery 修正审计候选

文档318已由PR #365精确合入`main@03b6d49a37a09f0d3cd2cdac4dca29454206e704`，tree
`1abe4a4fcc958ba306f59c420f355718af699922`。original Public CI `39537858764`、exact-main Public CI
`39540823614`与Browser Smoke `39540823601`均attempt 1 SUCCESS；fresh README/doc317/doc318/milestones 4/4 PASS。
independent reconciliation与234-artifact finite closeout为：

```text
3bb7c89c434d526b675430c9539469aca96b307c6eb5119ebfed4f4399602743
048fdd8f0196d90d3d14c8fb103b21bd18bae01f3accc6d783055f2b32a47776
```

因此doc318是qualified correction-audit history；manifest implementation保持`NOT_STARTED / NOT_AUTHORIZED`。fresh CONTROL
LOOP建立[文档319](docs/319-r1-negative-world-coverage-authority-recovery-audit.md)。normal Relation path持有原始
`DerivationInputSet`，但只接受`NORMAL_FULFILLED`。0.1 Fact→Coverage handoff能保留五分支、Fact阶段历史、digest、one-shot与
live BudgetContext，却没有`_inputs_ref`，也不能枚举Snapshot inventory、total Policy classification与blob authority。

empty、unsupported-only与Policy-excluded-only三个world的handoff可见状态均为Parse `0/0/0`、Fact U/E `0/0`、FactSet null，
实际Snapshot/Policy分母却分别为`0/0`、`1/1`、`1/1`。digest identity不能替代成员authority；内容相等的旁路input也不能证明
它属于原始same-attempt object graph。0.1 frozen history没有违约，最小重开边界是versioned Fact→Coverage exact-input handoff
successor feasibility。

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_FEASIBILITY_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc319。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc318/doc319/milestones readback、independent reconciliation与finite closeout全部闭合以后，最多成为
`AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，
独立建立handoff successor feasibility；不得直接创建successor、Coverage producer、manifest、Evidence、persistence或public产品。

### R1 Fact→Coverage exact-input successor 私有实现可行性审计候选

文档319已由PR #366从`base=03b6d49a37a09f0d3cd2cdac4dca29454206e704`、
`head=02271650a83f099a58bd469d466d4c62c097f6c1`、`tree=7615e0d04059f766d103c87383989851b57b7852`
精确合入`main@9701b192b6b60499b70a5e429ecbbb83b1134b70`。original Public CI `39546108067`、exact-main
Public CI `39548733536`与Browser Smoke `39548733661`均为attempt 1 SUCCESS；fresh README/doc318/doc319/milestones
4/4 PASS。independent reconciliation与162-artifact finite closeout分别为：

```text
e4c080206842e189e31de01b900bd37c24c8149f9ab8aab5648855bd93407fb7
fd7c23e7665c42747a774decdf5efccc1f05eb4fe31056142876471e6312269e
```

因此doc319已成为`AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP / QUALIFIED_HISTORY`。
fresh CONTROL LOOP建立[文档320](docs/320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)。
attempt 1证明`parent._inputs_ref()`不是五终态统一解：required Provider non-success会正确把parent eligibility保持为
`REVOKED`，live accessor因而拒绝。原四格失败保留为`FEASIBILITY_DESIGN_COUNTEREXAMPLE`，不重解释、不回填。

attempt 2改审`TERMINAL_VALIDATED_ORIGINAL_DERIVATION_INPUT_SET_REFERENCE`：parent先完成既有terminal handoff validation，
再在同一one-shot closure claim内交付其bound original immutable inputs与BudgetContext。五终态、三个零Parse分母world、
foreign-equal identity、legacy replay与late-stop falsifiers在Python 3.10.6/3.13.13 × normal/`-O`四格均PASS，canonical
report SHA-256一致：

```text
edcc90fdaba37646dc1065c24bb513f79ba2dac17741af0a4bdaef5ef8239a66
```

focused regression四格各99/99 PASS。0.1 function/consumer/document bytes与历史不变；successor只能携带terminal-validated
original inputs，不能复活Provider execution、产生Coverage status或取得manifest/Evidence/persistence/public authority。

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_NOT_STARTED_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc320。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc319/doc320/milestones readback、independent reconciliation与finite closeout全部闭合后，最多成为
`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP独立建立successor contract；不得直接修改runtime、
创建Coverage producer、实现manifest/Evidence、选择persistence或启动public Review/post-R1 Benchmark/R2–R6。

### R1 Fact→Coverage exact-input handoff successor 最小合同候选

文档320已由PR #367从`base=9701b192b6b60499b70a5e429ecbbb83b1134b70`、
`head=89abdf0467aeaa4c2bf7f09e84790ba458976f7c`、`tree=f58e3be4110885ab0760e4faa2d71ff3321e7dbf`
精确合入`main@b8a1ecd6e01d711f380d0774e7a6920aad005fc8`。original Public CI `39555193491`、exact-main
Public CI `39558171201`与Browser Smoke `39558171203`均为attempt 1 SUCCESS；fresh README/doc319/doc320/milestones
4/4 PASS。independent reconciliation与166-artifact finite closeout分别为：

```text
2959c0b5288abd97e15e00547a6845327f8ee64849e095831d33d0314877beb5
7d235b233a27878dfe8e6150a6eaf0d0485ccfe024b78e8cfcc4de621e96e9a0
```

因此doc320已成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。fresh CONTROL LOOP进入
[文档321](docs/321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)，选择
`r1-fact-to-coverage-exact-input-handoff-successor/0.2`、claim purpose
`FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`、private consumer与terminal-validated original-input carrier。

0.2对`NORMAL_FULFILLED / ZERO_PARSE_DENOMINATOR / ALL_PARSE_REJECTED / PROJECTION_BLOCKED /
REQUIRED_PROVIDER_NON_SUCCESS`五终态total；parent必须先完成terminal validation，再在同一同步one-shot claim内交付bound
original `DerivationInputSet`与BudgetContext。legacy continuation、0.1 Coverage、Relation与0.2共享单一claim槽。equal foreign
inputs、late stop、mutation、foreign context/cross-attempt与duplicate replay全部fail closed；required failure不得复活parent eligibility。

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc321。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc320/doc321/milestones readback、independent reconciliation与finite closeout全部闭合后，最多成为
`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。随后必须返回CONTROL LOOP建立独立docs-only freeze publication；不得从本合同
直接修改runtime、创建Coverage producer、实现manifest/Evidence、选择persistence或启动public Review/post-R1 Benchmark/R2–R6。

### R1 Fact→Coverage exact-input handoff successor 合同冻结发布候选

文档321已由PR #368从`base=b8a1ecd6e01d711f380d0774e7a6920aad005fc8`、
`head=1c2d82b6502053ed2c1b751568d8ed71a6c58196`、`tree=0c24c45fb52e5f29fc539d96762a31c0e3d0c899`
精确合入`main@9727dc3ab536ba05ab3bfc0baf9186057fc3e73c`。original Public CI `39564224949`、exact-main
Public CI `39567939524`与Browser Smoke `39567939496`均为attempt 1 SUCCESS；fresh README/doc320/doc321/milestones
4/4取得qualifying PASS。doc320 formal #1匿名额度耗尽ERROR仍保留，后继formal #2 PASS不覆盖它。independent reconciliation
与176-artifact finite closeout分别为：

```text
e8f98083143bc6be3f326414f9c65f84461b2e73dd820cf03ee1b23de584a71e
3b1f1ae300ecbfc26637c6298956d2cb838b05366cf2fd5cc5aa371a7e3be209
```

因此doc321已成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。fresh CONTROL LOOP进入
[文档322](docs/322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md)，只发布0.2合同冻结状态，保持
0.1 bytes/history、runtime、tests、Coverage producer、composition、manifest、Evidence、persistence与public产品不变。

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与新增doc322。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc321/doc322/milestones readback、independent reconciliation与finite closeout全部闭合后，才让`CONTRACT_FROZEN`
生效。按人类停止线，#369闭合后立即暂停，不创建#370或启动implementation feasibility。

### R1 Workbench Vitest/undici maintenance exact-main 资格失败边界审计候选

PR #369已精确合入`main@b2626e8e31c7c2681dc87e74dff799471886648b`，tree
`b757b130c767013a8f2f3db621e83123cf629ee4`。original Public CI `39573932263`、exact-main Public CI
`39578176854`与Browser Smoke `39578176781`均为attempt 1 SUCCESS；fresh README/doc321/doc322/milestones 4/4 PASS。
independent reconciliation与150-artifact finite closeout为：

```text
f1cefeaa6f7d4deb862cc4a5f9a8684774e6d85718587b32ae1a911f2523e050
78bce5110f50afcdb961b48be9369d4b36724d7e7019747f020eb23c4c26d73a
```

因此`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN`已生效。第一次docs-only implementation
authorization PR #372的original Public CI `40470062665` attempt 1因Vitest 4.1.11与undici 7.30.0的五个advisory
以9 SUCCESS / 1 FAILURE / 1 SKIPPED终结；PR关闭且未合并，保持`CLOSED / UNMERGED / NOT_QUALIFIED`。

独立maintenance PR #373只把`web/package.json`与`web/package-lock.json`更新到Vitest/`@vitest/mocker` 4.1.12及
undici 7.30.1。两次fresh构造与本地tests/lint/build/audit全部PASS，original Public CI `40474320234` attempt 1为
11/11 SUCCESS，随后精确合入`main@5aeb53eeb0cca2dc92175fb5dfe4521388dca67a`，tree
`96ff0ce193799760c41676404f1d33af63652ba9`。

new exact-main Browser Smoke `40478059772` attempt 1为1/1 SUCCESS，但Public CI `40478059827` attempt 1为
3 SUCCESS / 1 FAILURE / 4 SKIPPED。Python 3.10 job `122101107016`的Core regression在494项中仅
`test_catalog_accepts_public_m10_outcomes_and_isolates_a_corrupt_copy`失败：expected top-level verdict `PASS`，actual
`FAIL`。日志没有保留该临时Bundle的decisive assertion或attachments，故precise cause只能保持
`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`。同一run的Python 3.13与Workbench job成功；CPython 3.10.6 isolated repeat
PASS只属non-qualifying diagnostic，不解释或回填原失败。maintenance因此保持`MERGED / NOT_QUALIFIED`，installed Workbench
readback没有启动。

fresh CONTROL LOOP建立
[文档324](docs/324-r1-workbench-vitest-undici-maintenance-exact-main-qualification-failure-boundary-audit.md)，只冻结失败identity、
qualification effect与recovery seam。它保持Core/Workbench runtime、tests、fixtures、workflow、required lane、timeout、oracle、
docs/321–322、Schema、Coverage、manifest与persistence为base bytes。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_372_CLOSED_UNMERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_ADVISORY_MAINTENANCE_MERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_PUBLIC_CI_FAILED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc324。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc324/milestones installed-product readback、independent reconciliation与finite closeout全部闭合后，最多成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；只有存在新工程事实与新资格责任时，才允许建立
独立maintenance recovery candidate，再从恢复后的新exact main重建implementation authorization。禁止rerun、retry until PASS、
空提交、回填PR #372/#373或弱化required Core gate。

### R1 Workbench Vitest/undici maintenance 资格恢复候选

文档324已由PR #375从`base=5aeb53eeb0cca2dc92175fb5dfe4521388dca67a`、
`head=3604ef7a6316317212dd026f08e5346fa271357b`、`tree=739c9ed21cb5dcada0a66c6de651edc80665a768`
精确合入`main@c8503321934a8f65fc8744dc503cb1d476ab28a2`。第一次original Public CI `40482098220`
attempt 1的concurrency cancellation永久保留；独立第二次pull_request事件run `40482288836`、exact-main Public CI
`40486037853`与Browser Smoke `40486037792`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。fresh
README/doc324/milestones 3/3取得qualifying PASS；milestones formal #1的匿名额度耗尽ERROR保留，formal #2 PASS不覆盖它。
independent reconciliation与151-artifact finite closeout分别为：

```text
ebe07c9fd593d1f0c5d50d90677f6499352ad50c0169a14ee8f891f2b7d8915c
9bc218b6f52b6758f0b53dbb76ee0d063bc247254aedc8614894861fe59b05f2
```

因此`R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDITED`现为qualified
history；它不解释或回填PR #373。fresh CONTROL LOOP进入
[文档325](docs/325-r1-workbench-vitest-undici-maintenance-qualification-recovery.md)，建立一份具有新exact坐标与新增失败历史
对账责任的maintenance recovery candidate。在`main@c850332…`上的fresh local witness继续观察Vitest/`@vitest/mocker`
4.1.12、undici 7.30.1、Vite 8.2.4、14-file/179-test PASS、lint/build PASS及official npm registry零advisory。
主机默认npmmirror不实现audit API的HTTP 404作为setup ERROR保留；命令级official registry PASS不覆盖它，也没有修改全局配置。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_372_CLOSED_UNMERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_ADVISORY_MAINTENANCE_MERGED_NOT_QUALIFIED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_PUBLIC_CI_FAILED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDITED
R1_WORKBENCH_VITEST_UNDICI_MAINTENANCE_QUALIFICATION_RECOVERY_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc325。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc324/doc325/milestones installed-product readback、independent reconciliation与finite closeout全部闭合后，最多成为
`MAINTENANCE_QUALIFICATION_RECOVERY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，从新的exact main重建独立
implementation authorization；禁止rerun、空提交、回填#372/#373、弱化required Core gate或直接启动runtime/Coverage施工。

### R1 Fact→Coverage exact-input successor 私有实现授权恢复发布候选

文档325已由PR #376从`base=c8503321934a8f65fc8744dc503cb1d476ab28a2`、
`head=01267dc7bcb6d0a752a58bf81721c95ae57d3c19`、`tree=8b14018edf7f77b6bc5eb540204e8e084243c43b`
精确合入`main@ebeb890da1936cc15bcefe7e23c9bd532efd4787`。original Public CI `40495667837`、exact-main
Public CI `40499231916`与Browser Smoke `40499231632`均为attempt 1 SUCCESS；fresh
README/doc324/doc325/milestones 4/4取得唯一qualifying PASS。readback bootstrap的`--no-index` dependency wheelhouse误判与
首次Plan id前缀超长setup ERROR均保留。independent reconciliation与167-artifact finite closeout分别为：

```text
5f514c9fbcb24e1a89154632dc79cfe2407f8bd3293b0243f7bbd6082ab5b559
31c83dc18a5b19b98d95779b61dfa6895a00205d7b9ca56a2fe39d09457488a0
```

因此maintenance recovery现为`AUDITED / QUALIFIED_HISTORY`，但PR #372/#373的失败与UNKNOWN原身份不变。fresh CONTROL
LOOP从`main@ebeb890…`建立[文档326](docs/326-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-publication.md)。
独立continuity audit重新核对四个private source、docs320–325、contract/maintenance资格链、五个terminal world、三个zero-Parse
denominator world、same-object identity与shared one-shot falsifiers；Python 3.10.6/3.13 × normal/`-O`四格语义一致，focused
suite每格99/99 PASS。continuity qualification SHA-256为：

```text
a6aa4f4fa8ee63431cfb89b10867d66fa78ff39304ee610c7bc5983b5f00a588
```

Codex worktree工具因app当前目录不是Git仓库返回的setup ERROR已经保留，qualification effect为NONE；后继从显式VeriTrail
仓库与exact commit建立隔离worktree。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与新增doc326。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc321/doc322/doc324/doc325/doc326/milestones installed-product readback、independent reconciliation与finite closeout
全部闭合后，才让`PRIVATE_IMPLEMENTATION_ALLOWED`生效；implementation仍保持`NOT_STARTED`并返回CONTROL LOOP。禁止回填
#372/#373、弱化required gate、直接创建Coverage producer、消费旧composition authority、选择manifest/persistence或启动R2–R6。

### R1 Fact→Coverage successor 授权恢复 exact-main 资格失败边界审计候选

文档326由PR #377从`base=ebeb890da1936cc15bcefe7e23c9bd532efd4787`、
`head=7c9ba8bf990622b19abd35d2bbad860138ced11a`、`tree=f04a7870f31aa6c02cf7419f7af1c3e5229bdc33`
提交，original Public CI `40506198552` attempt 1为11/11 SUCCESS；protected merge形成
`main@310285aba4d2175164b53c4f68087817491df8bd`。Browser Smoke `40510081338` attempt 1为1/1 SUCCESS，
但exact-main Public CI `40510081408` attempt 1为10/11，required Starter job `122222945703` FAIL。

Artifact `12737259914`（archive SHA-256
`33ef978964918c30870010fcc56082c7e5d29edc9778c72c0147108bfa6de4bb`）证明pass/intentional-fail Bundle、
六张Workbench截图与声明交互均已形成；最终Workbench验真仍观察到desktop console
`Failed to load resource: net::ERR_NO_BUFFER_SPACE`并正确拒绝。精确失败resource identity为
`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，底层host resource cause为`UNKNOWN`；Subject failure与docs-only candidate
regression均未建立。没有rerun，也没有启动installed-product readback。因此文档326保持
`MERGED / NOT_QUALIFIED`，`PRIVATE_IMPLEMENTATION_ALLOWED`未生效。

fresh CONTROL LOOP建立
[文档327](docs/327-r1-fact-to-coverage-successor-authorization-recovery-exact-main-qualification-failure-boundary-audit.md)，
只冻结失败identity、qualification effect、UNKNOWN边界与最小recovery seam。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_MERGED_NOT_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_PUBLIC_CI_FAILED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones与新增doc327。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc326/doc327/milestones installed-product readback、independent reconciliation与finite closeout全部闭合后，最多成为
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP；只有存在具有新失败历史对账责任的新candidate时，
才可重建authorization recovery。禁止rerun、retry until PASS、空提交、回填#377、弱化required Starter/Workbench oracle或直接
启动private implementation。

### R1 Fact→Coverage successor 授权恢复后继发布候选

文档327已经由PR #378以exact head `f071608639c6b3462990c7d947f1fbd7bad186b2`合入
`main@7a043e8745d76e59a0ef5a3a3c332d7aaa645e57`。original Public CI `40515795532`、exact-main Public CI
`40520543941`与Browser Smoke `40520544044`均为attempt 1 SUCCESS；fresh README/doc326/doc327/milestones 4/4取得唯一
qualifying PASS。README formal #1的匿名额度`FORMAL_READBACK_ERROR`永久保留，reset后的formal #2使用新identity通过。
independent reconciliation与159-artifact closeout为：

```text
23e7f9f32b1793f74fd3906f33f7f65119a67d489fdf0d20da21bb02f37f1612
b4018ef01507795b95918dc27aaee3f6f3266de7d8b36967fea5fe511f683281
```

因此failure boundary现为qualified history；#377与文档326仍是`MERGED / NOT_QUALIFIED`，run `40510081408`、Artifact
`12737259914`与两个UNKNOWN不被解释或回填。fresh CONTROL LOOP建立
[文档328](docs/328-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-successor-publication.md)，
以新world独立对账#377失败与文档327 closeout。current exact main的四格continuity audit语义一致，focused suite每格99/99 PASS，
continuity qualification SHA-256为`f9c06265447dfc2adae00fe33e35827b00282b5c2f21be52278a30678b04f678`。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_MERGED_NOT_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_SUCCESSOR_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

文档328完整资格链闭合后，只让bounded A–I private implementation authority生效并保持implementation`NOT_STARTED`；随后必须
返回CONTROL LOOP。禁止把本publication当作实现证据、回填#377、弱化required oracle、创建Coverage producer、消费旧composition
authority、选择manifest/persistence或启动R2–R6。

### R1 Fact→Coverage exact-input successor 私有实现候选

文档328已由PR #379完整闭合并精确形成`main@494fedb1fbae9d5f847cb9f1873e7e13996b893a`，tree
`c60c01e5a1a380fe1aba0c217faa834241bea545`。original Public CI `40531345541`、exact-main Public CI
`40535859530`与Browser Smoke `40535859486`均为attempt 1 SUCCESS；fresh七目标readback取得唯一qualifying PASS。
independent reconciliation、finite closeout与active adapter freeze attempt 2分别为：

```text
8861f480d643904fd75ed61afe09ccd61a4c978a8a3fcb253625d7927e729050
72ae34c8ec41ab963c4dee2a8bc005c131f60d12e69982f521250bfa0d15e382
8799458f7bb570e8291c00f206537ecdf49602ba3b75941d1e7f5e61762cef7c
```

错误upstream coordinate与过早adapter freeze attempt 1保持原identity；#377 exact-main failure、Artifact `12737259914`、
resource `UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与root cause `UNKNOWN`也不被回填。因此
`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。

fresh CONTROL LOOP进入
[文档329](docs/329-r1-fact-to-coverage-exact-input-successor-private-implementation-candidate.md)。本candidate新增versioned private
0.2 carrier：parent-only terminal accessor在完整Fact terminal revalidation以后返回同一source、原始`BudgetContext`与原始
`DerivationInputSet`；successor与legacy continuation、Coverage 0.1及Relation共享one-shot；每次carrier read重验context、stop、
deadline、input seal、三canonical bytes、blob map、五digest、source与claim identity。它保留五terminal branch与三zero-Parse
denominator world，且只返回copy-owned input truth，不产生Coverage outcome、ledger或manifest authority。

source review在formal qualification前发现初版foreign-closure substitution失败路径可能没有撤销原始bound authority；final bytes改为
始终撤销bound closure并增加原eligibility `REVOKED` falsifier。全部旧字节测试观察保持non-qualifying，fresh final focused与full
四格必须独立重跑。semantic attempt 1的null FactSet proof-facility schema error与attempt 2旧字节也保持原identity。

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本candidate只允许README、AGENTS、milestones、doc329、`_fact_fulfillment.py`、新增private carrier module与其private test。
自己的local/original PR/protected merge/exact-main双门、fresh README/doc329/milestones readback、independent reconciliation与finite
closeout全部闭合后，最多成为`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。随后必须
返回CONTROL LOOP建立独立docs-only implementation freeze publication。禁止从本candidate直接创建Coverage producer、消费旧composition
authority、选择manifest/Evidence/persistence、发布public Review或启动R2–R6。

### R1 Fact→Coverage exact-input successor 私有实现冻结发布候选

文档329已由PR #380以exact head `2177ce675c23d1e6793c696f1bfabd67e6702b5d`合入
`main@8f258e3c4fb425af3d057493a63009c3099f03c4`，tree `69f826fd5d82e08ba2cd201b043f473fcc7a722e`。
original Public CI `40551350656`、exact-main Public CI `40556421233`与Browser Smoke `40556420712`均为attempt 1
SUCCESS；fresh README/doc329/milestones 3/3取得唯一qualifying PASS。independent reconciliation与134-artifact finite closeout为：

```text
0852c865880cba6d50caee93920e27e2aa07443fccdcc5b756a4d78cea15bbbb
e18860cf91973a906529274767e817760407c6a1cbe18a425225a6765630e638
```

closeout stdout self-capture mismatch另以`47ed145338746cb9e3008daeee4b1081fe2f59c73f31aed4d53ed4bb43e77b58`
保留，semantic/qualification effect均为`NONE`；其余133项终态一致。因此candidate为
`IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。

fresh CONTROL LOOP建立
[文档330](docs/330-r1-fact-to-coverage-exact-input-successor-private-implementation-freeze-publication.md)，只以docs-only状态发布
条件化冻结已资格化private carrier。当前只能记录：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_READBACK_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication只允许README、AGENTS、milestones与doc330。自己的local/original PR/protected merge/exact-main双门、fresh
README/doc329/doc330/milestones installed-product readback、independent reconciliation与finite closeout全部闭合后，
`PRIVATE_IMPLEMENTATION_FROZEN`才生效。随后必须返回CONTROL LOOP；禁止直接创建Coverage producer、消费旧composition
authority、选择manifest/Evidence/persistence、发布public Review或启动R2–R6。
