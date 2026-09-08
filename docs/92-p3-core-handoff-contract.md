# P3 Core Handoff 与真实正负链合同 0.1

> 当前状态：`P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_FROZEN / P4_CONTRACT_0.1_FROZEN / P4_RELEASE_NOT_STARTED`
>
> 历史冻结事实：[文档 93](93-p3-core-handoff-contract-freeze.md)。P3-A 本地候选实现审查发现“连续两次安全读取
> 不等于同一快照”的组合反例；第 13.1 节只重开 handoff 到 Core 的快照连续性。
> 后继实现与冻结候选事实：[文档 94](94-p3-core-handoff-implementation-freeze-candidate.md)。本文后文保留
> 合同冻结时的 `P3_IMPLEMENTATION_NOT_STARTED` 历史，不批量改写成当时已经实现。
> 最终冻结状态发布：[文档 95](95-p3-core-handoff-freeze-publication.md)。P4 当前边界见
> [合同冻结事实](97-p4-github-evidence-release-contract-freeze.md)。
>
> 精确设计基线：`3e785d197c8040c8baa4120fc63301eb347e5bc8`
>
> 本次重开重建基线：`main@6e48b5d109d0dd0e6c7b1b0fbe723cf1b792f852`
>
> 依赖状态：`P1_FROZEN / P2_FROZEN / Acceptance Core PC2_FROZEN`
>
> 影响等级：`L2_CONTRACT + L3_SYSTEM`；候选阶段只修改文档、索引与仓库协作说明

第一次 docs-only 修正 PR #60 从 `main@294ebf7...` 建立，但其原始 Python 3.13 `-O` 门禁复现了既有
Browser 停止竞态：Run 已保留 `USER_CANCELLED`，事件队列中的 route 回调仍与关闭中的 Playwright
driver 竞争并泄漏第二个 listener 异常。#60 因而关闭且未合并；独立 PR #61 只收窄停止后的路由解析
边界，原始 11 项门禁全绿后合入上述新主线，并完成匿名 exact-SHA 源码与 `RA-020` Ledger 读回。
本候选从该 exact main 重建，不以重跑洗白 #60，也不把 Browser 地基修复冒充 P3 合同或实现证据。

## 1. 本轮裁决

P3 不再观察 GitHub API、公共页面、Chromium、网络或 DOM。P1 与 P2 已分别把开放世界压缩成两份
标准 `Evidence 0.1`；P3 只建立从这些不可变产物到现有 Acceptance Core 的显式交接，并证明 Core
可以在一个 sealed `AcceptancePlan 0.1` 下形成可复算的四态 Verdict。

```text
sealed AcceptancePlan 0.1
        |
        +-- P1 GitHub API Evidence 0.1
        +-- P2 Public Render Evidence 0.1
        |
        v
exact-digest handoff
        |
        v
Acceptance Core PC2
        |
        v
AcceptanceBundle 0.1
```

P3 不新增 GitHub 真值，不把两个观察面说成独立权威，也不把同一 session 说成平台原子快照。它只
证明：给定事先封存的条件和两份明确来源的 Evidence，Core 能按已经冻结的规则区分 `PASS`、`FAIL`、
`INCONCLUSIVE` 与 `PENDING`。

## 2. 权威与责任

| 组件 | 拥有什么 | 明确不拥有什么 |
| --- | --- | --- |
| sealed AcceptancePlan | 观察规格、Evidence 要求、充分性、完整性与断言 | 外部事实、采集结果、Verdict |
| P1/P2 Collector | 各自来源事实、provenance、coverage 与 Evidence 产物 | 跨源匹配、充分性、最终结论 |
| PairedCollectionCoordinator | 一次串行 P1 -> P2 执行、共同 session 与两侧发布结果 | 合并 facts、原子快照、Core Verdict |
| P3 handoff | 明确列出两侧结果并绑定实际 Evidence 文件摘要 | 复制 Plan/session 语义、选择“最好”的事实、判断 coverage、执行 assertion |
| Acceptance Core | Evidence binding、cardinality、规则求值与四态 Verdict | GitHub/浏览器私有语义、现实真相 |
| Human Seal authority | 前提、目标、验收条件与是否 Seal | 改写已经发生的外部事实 |

调用 Core 的动作可以由 reference lab 编排，但 Verdict 只能由 Core 公共 evaluator 产生。命令输出位于
插件仓库、脚本由插件发起或报告最终由插件 README 展示，都不能转移这项权威。

## 3. P3 交接单位

### 3.1 标准输入保持不变

Core 的语义输入仍然只有：

```text
sealed AcceptancePlan 0.1
zero or more imported standard Evidence 0.1 snapshots
execution_status
```

P3 不修改 `AcceptancePlan`、`Evidence`、`AcceptanceReport` 或 `AcceptanceBundle` Schema，不增加 GitHub
专用 operator，也不要求 Core 导入 `veritrail_github`。Core 现有路径入口继续存在；为避免 handoff 核验与
Core 导入之间再次打开可变路径，P3 只允许增加一个通用的、接受已由 Core 公共 importer 形成之
`ImportedEvidence` 快照的 Bundle 入口，路径入口必须先导入再委托给同一实现。

### 3.2 GitHubEvidenceHandoff 0.1

为避免用同目录、文件名排序、mtime 或“最近一次”隐式选择 Evidence，P3 reference lab 必须由插件原子
发布一个极薄的 `GitHubEvidenceHandoff 0.1` manifest。它是插件侧交接清单，不是 Evidence，不进入
Core rule evaluator，也不能单独支持 Verdict。

冻结字段为：

```text
schema_version              = "0.1"
manifest_kind               = "GITHUB_EVIDENCE_HANDOFF"
collection_order            = ["github-api", "github-public-render"]
sides[]
  collector_role            = "github-api" | "github-public-render"
  state                     = "PUBLISHED" | "COLLECTED_NOT_PUBLISHED" | "MISSING"
  evidence_path             = safe relative filename | null
  evidence_sha256           = lowercase SHA-256 | null
  error_code                = bounded operational code | null
```

约束如下：

- manifest 恰好有两个不同 role，并按冻结顺序排列；
- `evidence_path` 只能是 manifest 同目录下的普通相对文件名，禁止绝对路径、父目录、空段、符号链接逃逸
  和隐式 glob；
- side 字段组合必须满足下表，不能用任意字符串或半套字段制造第四种状态；
- manifest 不复制 `plan_digest`、`collection_session_id`、facts、coverage、captured time、assertion result
  或 Verdict-like boolean；Plan binding、session integrity 与 coverage sufficiency 只由 Core 从标准 Evidence
  求值；
- 一个 side 缺失时必须保留其 state/error，不能从清单删除后把一侧集合称为完整；
- manifest 文件使用 create-new + staging + atomic rename 发布，拒绝覆盖；其规范 JSON 文件摘要形成该次
  handoff 的产物身份，但不替代 Evidence 自身摘要。

| state | evidence_path | evidence_sha256 | error_code |
| --- | --- | --- | --- |
| `PUBLISHED` | 必须存在 | 必须存在 | `null` |
| `COLLECTED_NOT_PUBLISHED` | `null` | 必须存在 | `PUBLISH_ERROR` |
| `MISSING` | `null` | `null` | `COLLECTOR_FACTORY_ERROR`、`COLLECTION_ERROR`、`ARTIFACT_CONFORMANCE_ERROR` 或 `SESSION_MISMATCH` |

该闭集与 P2 已冻结的 `PairedSideOutcome` 对齐；P3 不重新解释或扩张错误类别。

### 3.3 handoff 验证

reference lab 在调用 Core 前必须：

1. 验证 manifest 的闭合集合、字段、路径和摘要格式；
2. 对每个 `PUBLISHED` 路径只做一次有界、身份稳定的普通文件读取，并由 Core 公共 Evidence importer
   在该次读取拥有的字节快照上形成标准 `ImportedEvidence`；
3. 以 importer 计算的规范 Evidence SHA-256 与 manifest 精确比较；不得用包含文件尾换行的原始文件
   字节摘要替代 Evidence 产物身份；
4. 验证已导入 Evidence 的 `collector_role` 对应 manifest side；
5. 将同一批已验证的 `ImportedEvidence` 对象直接交给 Core 通用公共入口。Core 必须在求值前再次执行
   `verify_imported_evidence`，但不得为本次 handoff 再次打开原路径；
6. Evidence 的 Plan/spec binding、跨源 session integrity、coverage sufficiency 与缺失 side 继续由
   sealed Plan 和 Core 保持可见。

这里的 snapshot ownership 不等于“相信同一个 Python 对象永远不会变化”。Core importer 必须拥有递归
复制后的 document/attachment 内容，不得继续引用调用者提供的可变映射；交接后任何对象内 mutation 都
必须因消费前规范摘要复算而失败。0.1 不引入新的 persistent immutable container，也不允许插件修改
`ImportedEvidence` 后重签摘要。

handoff 验证不得读取业务 facts、Plan/spec binding、session 或 coverage 来决定是否传递，也不得因 coverage
为 `PARTIAL/ERROR` 就丢弃 Evidence。结构/摘要/路径不可信时必须在 Core 调用前失败并保留 typed handoff
error；不能虚构一份 Error Evidence，也不能把“未形成 Acceptance Run”冒充 Core `INCONCLUSIVE`。

这条边界保证：

```text
Handoff failure
    = 无法可信确定要交给 Core 的不可变文件

Core INCONCLUSIVE / PENDING / FAIL / PASS
    = 文件已被精确交接后，按 sealed Plan 对 Evidence 语义进行裁决
```

因此本阶段冻结：

```text
Manifest = exact artifact selection + bounded handoff provenance
Manifest != semantic prevalidation
```

`state/error_code` 只解释某一侧是否形成可交接文件，不获得解释 Evidence 内容的权力。

## 4. 首个 reference vertical slice

首片固定为公开、匿名、CPU-only、串行执行：

```text
Host repository:       NoctilumeDev/VeriTrail
Target:                one exact immutable commit
Render surface:        exact-commit README Markdown
P1 access mode:        ANONYMOUS
P2 access mode:        ANONYMOUS_FRESH_CONTEXT
Collection order:      P1 API -> P2 Render
Evidence cardinality:  EXACTLY_ONE per observation spec
Core:                  public Acceptance Core PC2 API/CLI
Output:                create-new AcceptanceBundle 0.1
```

实现时新增一个完整 sealed 示例 Plan。它必须使用两个不同 observation spec 与 requirement：

```text
github-api
  -> platform.github.api.snapshot

github-public-render
  -> platform.github.public-render
```

首片至少声明：

- 两侧 coverage 必须为 `COMPLETE`；
- 两份 Evidence 的 `collection_session_id` 必须相同；
- P1 `/facts/commit/sha` 必须等于 P2
  `/facts/target/source_coordinates/target_commit_sha`；
- API commit SHA、Render requested URL 与一个预先声明的 README literal marker 必须满足 Plan；
- 同一 session 只表示有序相关窗口；AcceptanceBundle 保留的两份 Evidence 必须继续携带
  `atomic_snapshot_claimed = false`，报告不得把它扩张为原子快照。

首片不要求 branch head 在未来一直等于该 exact commit；可变 `main` 只用于交付读回，不能替代 Plan 内
冻结的 immutable target。

## 5. P3 reference lab 边界

P3 实现允许新增一个仓库内 reference lab，用于串联公开 API：

```text
load exact sealed Plan
derive and validate both requests offline
run PairedCollectionCoordinator
publish handoff manifest
verify exact handoff files
call Core with the same imported Evidence snapshots
independently recompute and read report
```

reference lab 不是安装后的长期调度器，也不是新的 Core 入口。首版不提供“一键接受 GitHub 结果”的插件
CLI，不 monkey-patch Core，不调用 Core 私有符号，不写 GitHub，不自动 Seal，不自动重试 Verdict，也不
在失败后替用户修改 Plan。

## 6. 四态正负链

每条负链只改变一个预注册变量；旧 Evidence、旧 Plan 和旧 Bundle 保持不可变。

### 6.1 PASS

- 两个 spec 各精确绑定一份标准 Evidence；
- 两侧 coverage、session integrity、cross-Evidence coordinate 与全部 HARD assertion 成立；
- execution status 为 `COMPLETED`；
- Core 产生 `PASS`，独立复算得到相同结果。

### 6.2 FAIL

- Evidence 结构、摘要、Plan binding、cardinality 与 integrity 全部成立；
- 另一个事先封存的 Plan 把一个可观察 marker 或精确事实声明为错误期望；
- Collector 仍忠实保留现实事实，Core 因 decisive assertion false 得到 `FAIL`；
- 不允许在采集后修改 Plan 制造 FAIL。

### 6.3 INCONCLUSIVE

至少覆盖：

- 从两次独立 collection session 交叉选择 P1/P2 Evidence，跨源 session integrity false；
- 精确交接已经成立，但 Evidence 的 Plan/spec binding、cardinality 或 Core integrity rule 不成立；
- integrity false 与 assertion false 同时出现时，仍由冻结优先级得到 `INCONCLUSIVE`。

路径逃逸、manifest/Evidence 摘要漂移或 Evidence 文件无法通过公共 importer 时尚未形成可信 Core 输入，
属于 handoff failure，不得借用 `INCONCLUSIVE`；只有精确文件已可信交接后的语义不一致才进入 Core 四态。

### 6.4 PENDING

至少覆盖：

- Plan 要求两侧 Evidence，但 Core 只收到其中一侧；
- 一侧合法 Evidence 的 coverage 为 `PARTIAL` 或 `ERROR`，sufficiency 未满足；
- execution status 不是 `COMPLETED`；
- 缺证据不得被插件补成空对象，也不得自动转为 `FAIL`。

### 6.5 优先级复验

P3 必须直接复验 PC2 已冻结的顺序，不在插件内复制另一份规则：

```text
binding/cardinality/metadata/rule/integrity error -> INCONCLUSIVE
else decisive assertion false                    -> FAIL
else missing/incomplete/not-evaluated             -> PENDING
else                                               -> PASS
```

## 7. 身份、顺序与可复算性

必须保持：

```text
Plan identity
!= Observation Spec identity
!= Request instance identity
!= Fact identity
!= Evidence artifact identity
!= Handoff manifest identity
!= Acceptance Run identity
!= AcceptanceBundle identity
```

两次采集看到相同 facts 可以拥有相同 `facts_digest`，但 Evidence、handoff 与 Core Run 仍必须不同。
Evidence 参数顺序不得改变 binding 或 Verdict；显式 requirement/spec/digest 才拥有身份。P3 禁止通过：

```text
latest
glob first match
directory order
mtime
same filename
same request id
same facts digest
```

选择或配对产物。

## 8. 故障与恢复

- 两个 request 在任何网络/浏览器创建前共同完成离线验证；
- P1 失败不取消安全可执行的 P2，P2 失败也不改写已发布 P1；
- 已发布 Evidence 不得在后续 side、manifest 或 Core 失败时删除或覆盖；
- manifest 发布失败时不调用 Core，并保留两份已发布 Evidence 供诊断；
- Core Bundle 发布失败不得反向修改 manifest/Evidence；重试必须使用新的 output 与新的 Acceptance Run ID；
- 所有临时目录、浏览器进程和 staging 均须清理；失败证据不得泄漏 token、Cookie、绝对私有路径或原始
  页面/响应体。

## 9. 安装与解耦

P3 不改变 P1/P2 可选依赖边界：

- base plugin 未安装 Playwright 时，P1 与 handoff manifest 的离线校验仍可导入；
- P2 只有显式安装 `render` extra 和 matching bundled Chromium 才可运行；
- Core wheel 不依赖 GitHub plugin；插件卸载后，已经生成的 AcceptanceBundle 仍可由 Core 读取和复算；
- reference lab 必须从当前 exact worktree/wheel 导入，测试源码坐标与实际模块坐标不一致时证据作废。

## 10. 验收矩阵

P3 合同冻结后，实现至少建立以下证据格：

1. handoff manifest 的规范正向向量与稳定摘要；
2. 未知字段、缺 role、重复 role、错误顺序、非法路径、绝对路径与父目录逃逸拒绝；
3. `PUBLISHED` 缺 path/digest、非 Published 伪装 artifact、文件缺失、摘要漂移和符号链接逃逸拒绝；
4. manifest 不含 Plan/session、facts、coverage、Verdict-like boolean 或私有绝对路径；
5. 两侧 COMPLETE、同 session、同 exact coordinate 的 synthetic 全链得到 `PASS`；
6. sealed wrong-expectation Plan 在完整 Evidence 下得到 `FAIL`；
7. 错误 Plan/spec binding 或不同 session 的两侧 Evidence 不被 handoff 层过滤，并由 Core 得到
   `INCONCLUSIVE`；
8. 缺 Render、coverage `PARTIAL/ERROR`、execution incomplete 分别得到 `PENDING`；
9. integrity false + decisive false 得到 `INCONCLUSIVE`，decisive false + 无关缺证据仍按 Core 冻结规则裁决；
10. Evidence 输入顺序变化不改变 Verdict，重复/额外 candidate 不被顺序掩盖；
11. handoff 摘要验证发生在 Core 调用前，失败不会创建半个 Bundle；
12. Bundle 使用 create-new 原子发布，拒绝覆盖，报告/manifest/Evidence SHA 可独立复算；
13. base wheel 无 Playwright 时 P1/handoff 可用，render wheel 能启动 matching Chromium；
14. plugin 卸载后 Core 可读取并复算既有 AcceptanceBundle；
15. 真实 GitHub exact-commit positive slice 得到 `PASS`；另一个预先 sealed 的单变量错误期望真实链得到
    `FAIL`，不得在观察后改 Plan；
16. 真实链报告明确同一 GitHub trust domain、同一相关 session、非原子快照，不扩张为来源真实性或
    世界真相；
17. handoff 核验后替换原路径的确定性负例证明 Core 仍消费核验时的同一 `ImportedEvidence` 快照，不会
    把 manifest 绑定的 A 与随后路径中的 B 混成一次合法 Run；
18. 旧的 path-based Core 公共入口与新的 imported-snapshot 入口对同一输入产生同一 Bundle/Verdict；
19. importer 不共享调用者的输入映射；导入后修改原映射不改变快照，直接修改快照则在 Core 消费前因
    摘要复算被拒绝；
20. Core、Starter/Skill、Workbench、P1、P2 与双 Python `normal/-O` 回归不受影响；
21. 远端门禁、受保护主线、exact-main、匿名 README/合同/事实文档读回分别成立。

测试数量不是出口；每个合同命题必须指向独立自动化证据或明确的真实外部读回。

## 11. 实现批次

合同冻结后只允许串行施工：

```text
P3-A  manifest contract + canonical identity
P3-B  create-new publisher + exact-file verifier
P3-C  combined sealed Plan + synthetic four-verdict lab
P3-D  wheel/uninstall/regression boundaries
P3-E  real GitHub PASS/FAIL slice
P3-F  remote gates + freeze closure
```

每批独立验证后再进入下一批。第 13.1 节只允许增加通用 imported-snapshot Bundle 入口并让旧路径入口
委托它；若实现需要修改 Acceptance Core Schema/evaluator、P1/P2 fact semantics、Collector coverage
或 Verdict 优先级，立即停止并重开相应合同，不能在 P3 内兼容掉矛盾。

## 12. 明确延期

P3 不包含：

- P4 插件版本、tag、Release、公开下载与稳定安装坐标；
- 登录态/私有 GitHub、GitHub Enterprise、GraphQL、webhook、scheduler 或组织级扫描；
- Workbench 新规则、长期 dashboard、自动修仓库、自动合并或写 GitHub；
- Review Attention R1 代码、Pattern Corpus 冻结或 AI 自动处置；
- GitHub 之外的真实性锚点、可信时间服务或“事实终极为真”声明；
- Codex Security 深扫、攻击路径或安全认证。

## 13. 合同冻结门

候选经 PR #55 合入 `main@ea6723a224b5430095c25398d872caf025210c99` 后，真实匿名读回暴露了
冻结门自身的一条错误假设：本文与 README 不含嵌入式 Mermaid，均可得到 `COMPLETE`；P 轨 Plan
`docs/77-post-core-platform-plugin-plan.md` 含 Mermaid，GitHub 会导航到
`viewscreen.githubusercontent.com/markdown/mermaid` 子框架，而 P2 冻结策略会把任何非主文档导航保留为
`UNEXPECTED_PAGE_NAVIGATION`。desktop 与 narrow 两次独立观察都因此正确得到 `PARTIAL`，不是主页面、
作用域、样本或标记失败。

P3 不重开 P2，也不删除 Mermaid 来迫使现实迎合观察器。这里把“公共读回存在”与“整页观察
`COMPLETE`”拆开：Plan 页的有界 `PARTIAL` 只证明指定标记在一个明确受限的公开观察中存在，绝不升级为
`COMPLETE`，也不进入 P3 reference slice 的正式 Acceptance Evidence。

本候选只有在以下事实全部成立后才能进入 `P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN`：

1. 本文与 P0/P1/P2、PC2 合同逐项复核，不改写既有冻结语义；
2. 文档候选通过原始远端门禁并由受保护主线合入；
3. 合入后读取新的 exact `origin/main`；
4. 使用 fresh anonymous P2 Collector 读取 README 与本文，确认 HTTP 200、requested/final URL 相同、
   唯一作用域、三样本稳定、指定标记存在且 coverage 为 `COMPLETE`；
5. 使用同一产品 Collector 读取更新后的 P 轨 Plan。`COMPLETE` 可直接满足；若因嵌入式 Mermaid 得到
   `PARTIAL`，只允许以下精确闭集同时成立：HTTP 200、requested/final URL 相同、作用域唯一可用、三样本
   稳定、无 truncation、指定标记至少出现一次、collector errors 为空，coverage reasons 恰为
   `FACT_CONFLICTS_RETAINED + NETWORK_POLICY_AFFECTED_COVERAGE`，唯一影响 coverage 的 conflict 恰为
   `NETWORK_POLICY_BOUNDARY / UNEXPECTED_PAGE_NAVIGATION / viewscreen.githubusercontent.com/markdown/mermaid`；
   任何额外 reason、error、conflict 或不稳定都否决冻结；
6. 另一个 docs-only closure 只记录候选、修正、首次失败观察与最终有界读回已经发生的事实，再次通过
   门禁、合入和匿名读回；
7. 仓库中仍不存在 P3 manifest Schema、publisher、reference lab、示例 Plan 或 AcceptanceBundle 产物。

候选、语义修正与修正后 exact-main 读回当时已经完成；精确坐标、失败观察和产品 Artifact 摘要由
[文档 93](93-p3-core-handoff-contract-freeze.md)保留。在文档 93 的状态发布闭环完成前，当时状态保持：

```text
P2_FROZEN
P3_CORE_HANDOFF_CONTRACT_0.1_CANDIDATE
P3_IMPLEMENTATION_NOT_STARTED
P4_NOT_STARTED
R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE
```

任何新反例都可以否决冻结资格。文档 93 的最后门随后全部成立，合同曾进入
`P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`；该冻结只允许后续从新的 exact
main 开始 P3-A，没有自动授权 P4 或 R1。第 13.1 节记录的后继反例现已再次否决该冻结资格。

### 13.1 连续安全读取不等于同一快照

P3-A 已在独立本地候选实现中完成 manifest 纯合同和规范身份的定向验证，但进入 P3-B 前审计 Core 公共
入口时发现：

```text
handoff verifier reads path -> Evidence A -> digest matches manifest
path changes from A to B
Core path entry reads path   -> Evidence B -> each individual read is safe
```

`read_stable_bytes` 能证明一次打开期间普通文件身份和内容没有变化，却不能把两个先后发生的打开变成同一
快照。原合同要求 handoff 先导入核验、随后把路径交给 Core 重读，因此可能让 manifest 绑定 A、Core
裁决 B。两次局部安全不能推出组合身份连续：

```text
StableRead(A) + StableRead(B) != SameSnapshot(A, B)
```

这不改变 manifest、Evidence 或 Verdict 语义，只纠正交接载体。修正后的唯一合法链为：

```text
one stable bounded file read
    -> Core public Evidence import
    -> manifest digest and collector_role verification
    -> same ImportedEvidence objects
    -> Core generic imported-snapshot bundle entry
    -> Core verify_imported_evidence
    -> deterministic evaluation and Bundle publication
```

Core 旧路径入口继续兼容既有调用者，但必须先导入路径并委托同一个通用实现。P3 插件不得复制 importer、
不得把 GitHub 类型引入 Core、不得用文件锁或“调用足够快”冒充身份连续，也不得在 handoff 后再次打开
Evidence 路径。该修正只补通用 API 组合边界，不修改 Schema、operator、binding、coverage 或 Verdict
优先级。现有 importer 已经为 dict/list 建立递归 owned copy，现有 Core verifier 也会在消费前复算摘要；
实现只需保持并验证这两条性质，不为“绝对不可变”另造一套容器系统。

因此 P3-B 及后续施工当时暂停；旧 P3-A 候选不具备继续施工资格，也不得被当作新合同实现证据。

### 13.2 快照交接修正重新冻结

第一次修正 PR #60 的原始 Python 3.13 `-O` 门禁复现了既有 Browser 停止后 route 回调与 driver 关闭竞态，
因此关闭且未合并，没有以 rerun 或旧绿灯覆盖失败。独立 PR #61 只修复该地基，并经原始 11 项门禁合入
`main@6e48b5d109d0dd0e6c7b1b0fbe723cf1b792f852`；该修复没有被解释成 P3 合同或实现证据。

快照修正随后从该 exact main 重建，由 PR #62 的原始 11 项门禁通过后，以 merge commit
`5d4e7bbbf706d92c98cf36418d6f86b5caf2d3d8` 合入受保护主线。从该 exact main 运行产品
`PublicRenderCollector`，README 与本文均确认 HTTP 200、requested/final URL 相同、唯一可用作用域、
三样本稳定、指定标记存在、coverage 为 `COMPLETE`，且没有 conflict、collector error 或 cleanup error。
精确 Artifact 摘要由[文档 93](93-p3-core-handoff-contract-freeze.md)保留。

独立 docs-only closure 的原始门禁、受保护主线合入和合入后 exact-main 产品读回全部成立后，本合同重新
进入 `P3_CORE_HANDOFF_CONTRACT_0.1_FROZEN / P3_IMPLEMENTATION_NOT_STARTED`。冻结只允许从新的
exact main 重建 P3-A，再串行进入 P3-B；P4 与 Review Attention R1 仍未获得启动资格。任何后继反例仍可
再次否决受影响边界的冻结资格。
