# R1 RelationSet Admission / Public Qualification Binding 合同冻结发布

日期：2026-09-22

## 1. 发布对象与条件状态

本文只发布[文档 183](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)已经审议的
最小合同，不实现 Schema、runtime、publisher、RelationSet 文件、Slice 或 Coverage。

| 坐标 | 值 |
| --- | --- |
| 上游冻结状态 | `R1_RELATION_DERIVATION_FROZEN / R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN` |
| 前置审计 | [文档 182](182-r1-post-qualification-relation-set-admission-and-evidence-binding-system-audit.md) |
| 合同候选 | [文档 183](183-r1-relation-set-admission-and-public-qualification-binding-contract.md) |
| 候选 PR | `#171` |
| maintenance | [文档 184](184-m10-descendant-readiness-fixture-observation-correction.md) / PR `#172` |
| maintenance-qualified base | `main@f4aec949258ed16830b2e8dd828273435498764b` |
| 候选 head / merge / tree | `53d4b9991e0df4a3c0328e7426f9c7de23c31d67` / `9299c24fdde489957cb39dfc687296ea3dc59718` / `3770d2440845e76d65a178c8962fbc4676b889be` |
| 影响层级 | `L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

本文分支、原始远端门、受保护主线合入、合入后 exact-main Public CI / Browser Smoke 与本文专属 fresh
anonymous installed-product readback **全部成立以后**，目标状态才是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_ALLOWED
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

在最后一项门禁成立前，文档 183 的 `CONTRACT_CANDIDATE` 仍是当前已证事实。本文不因自身文字提前授权代码。

## 2. 本次冻结的最小对象

冻结对象是 **private RelationSet admission、explicit admission witness 与 versioned public qualification
binding 的最小合同**：

```text
exact owned QUALIFIED result
    -> deterministic admission eligibility
    -> exact RelationSet membership / provenance / conflict closure
    -> private admitted RelationSet value
    -> explicit admission witness
    -> DerivationEvidence 0.2 public binding shape
```

以下五层继续独立：

```text
Relation semantics
    != provenance bytes
    != composition qualification
    != admission authority
    != publication authority
```

deterministic application 是 admission rule 与 witness construction 的唯一所有者。`RelationSet 0.1` 只保存
语义内容与诚实 provenance，不能自报合法；`DerivationEvidence 0.2` 只承载已成立 witness，不能反向签发；
`Manifest 0.1` 继续绑定八个文件的 bytes/digests，不能从文件存在推出 eligibility。

## 3. 冻结的不变量

1. admission 只能接受 exact、copy-owned、`QUALIFIED` 的 qualification result，并重新复算 terminal、逐项
   observation、candidate composition、release 与 identity closure；raw candidates、`COMPLETED`、Schema-valid
   shape 或 caller digest 不能绕过 gate；
2. RelationSet members 必须恰等于 merged qualified candidates；same-ID provenance、ProviderRun reverse closure、
   same-subject conflicts 与 final reported IDs 必须双向闭合；
3. `QUALIFIED / CONFLICTING` 可以 admission，但必须保留全部 candidates/conflicts、不得选 winner，并阻止 normal
   Slice traversal；qualification 完整不等于 conflict-free；
4. witness 必须绑定 exact FactSet、ObservationDomain、qualification claim、ProviderRun IDs、admitted members、
   conflicts 与 `relation_set_digest`；相同 semantic content 的独立 attempts 必须逐次建立各自 witness；
5. identity dependency 保持单向无环：qualification -> RelationSet -> witness -> Evidence -> Manifest；RelationSet
   不反向引用 witness，witness 不包含 Evidence digest，Manifest 不进入子 Artifact semantic identity；
6. `DerivationEvidence 0.2` 新增 required `relation_admission` carrier 与独立 identity domain；历史 0.1/0.1.1
   Schema、corpus、vectors、bytes 与 domain 均不得改写；
7. `COMPLETED` 需要 conformant non-null witness 与 exact final Relation IDs；其他 terminal 只冻结 future
   `relation_admission=null` 的 fail-closed shape，不由本合同授予 diagnostic publication；
8. qualification 后的 admission、witness、staging、release 或 cleanup 失败不得留下 normal partial Artifact；后继成功
   attempt 不解释或覆盖早先失败。

该合同只证明 bounded admission eligibility 可被机械建立和第三方复算。它不证明 Relation 是现实真相，不授予
Slice/Coverage/Attention/Verdict 权，也不创建公共文件。

## 4. 原始首败、独立维护与重新资格化

PR #171 original head `cffd64d941b76bdae746fab4190d5c56c1d33366` 的 Public CI run
`35629971691` attempt 1 在 Python 3.10 `-O` 的既有 descendant-readiness positive fixture 上正式失败。旧 Artifact
只保留约 `3.045s` 后 `readiness.ready == false`，没有 terminal、attempts 或 bounded streams；精确根因保持
`UNKNOWN`。本机同 source state 的后继成功不能反推旧失败原因。

独立 maintenance PR #172 只修可由源码直接证明的测试观察缺口：为无 3 秒 SLO 的正向 helper 使用 bounded
`10s` observation window，启动后立即注册 idempotent cleanup，并在失败时保存 exact observation/streams。它没有
修改 R runtime、合同、产品 timeout 或负向语义。资格链为：

```text
PR #172 Public CI  35634296113  pull_request / attempt 1  11/11 SUCCESS
maintenance merge f4aec949258ed16830b2e8dd828273435498764b
Public CI          35636414037  push / attempt 1          11/11 SUCCESS
Browser Smoke      35636414038  push / attempt 1           1/1 SUCCESS
```

PR #171 随后从该 maintenance-qualified exact main 重建 source state，形成 head
`53d4b9991e0df4a3c0328e7426f9c7de23c31d67`。其第一条完整新-head run 与 PR body metadata refresh 触发的
第二条同-head required run 都独立成功：

```text
PR #171 Public CI  35639609448  pull_request / attempt 1  11/11 SUCCESS
same-head CI       35641735161  pull_request / attempt 1  11/11 SUCCESS
candidate merge   9299c24fdde489957cb39dfc687296ea3dc59718
Public CI          35643852734  push / attempt 1          11/11 SUCCESS
Browser Smoke      35643852850  push / attempt 1           1/1 SUCCESS
```

第二条 run 只满足 GitHub 在 metadata edit 后重新出现的 required status；它不使同一 source head 获得两份不同
语义，也不覆盖第一条成功。所有绿色只证明各自 source state 的资格，不解释原 head 的 `UNKNOWN` 首败。

## 5. 候选 exact-main 匿名产品读回

读回从 detached exact `main@9299c24...` 取得 orchestration probe，在 fresh CPython 3.13 venv 中只安装公开冻结
wheels：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

导入路径位于 fresh venv 的 `site-packages`，没有使用 repository `PYTHONPATH`。清空 GitHub token 环境后，第一份
README formal session `github-paired-a3adeade779149f489fd67ffae4c80a3` 的 P1 得到匿名 API
`403 / COLLECTION_BUDGET_EXHAUSTED / ERROR`，记录 `limit=60 / used=60 / remaining=0 / reset=1790019794`；
同 session P2 为 exact-SHA、HTTP 200、`COMPLETE`。该 session 不合格且原 output 保留。

quota reset 后使用新的 Plan、session 与 output root，合同要求的三份 paired readback 全部闭合：

| Target | Session | Plan digest | Handoff | Report |
| --- | --- | --- | --- | --- |
| README | `github-paired-98f2cd455d0e44068bc07bb0ccac07cc` | `851bc594f581cbbc0efd29fe90483750220ee46090d4d21ba14a0b204a9dc119` | `f4c54c63746a7b5556ac1264260a27a82dbcfaf01e81d528216b492cd45d9434` | `3d7c8efd124d353e95ed91c6535551e7c70900efb76b0e9ef442f0b58727dfed` |
| Document 183 | `github-paired-c03f16981492450e84d9bb0b4dd7ef46` | `3d74eede56e83afacda6d3ef3cb0681422fedb1f32e16816bc775315e651b24c` | `d73285fdf74349e531279266e6d02f5b01878ae023f1d000ac8660139c089a82` | `cd4ce13969a29d05b99331245bf8e92550d635e3f50c9e1e4ed989fd169233dc` |
| Milestones | `github-paired-7df2145a880d4733ac34fe5ec7948d44` | `7d5e5138262813b881e7e54712736a3f1e2ce4b629a36d6baead08978b1ae05b` | `7e89f917d311fef95879ac15e87f6b04c875e4d305d27a4624e1185c99727522` | `c7830178ac4e972bd69092e8f8f42df9d260c1e4b63ea46f94b70360c0f6284a` |

三次均为 P1/P2 coverage `COMPLETE`、HTTP 200、requested/final exact-SHA path 相同、唯一 marker、三样本稳定、
零 conflict/error/coverage reason/cleanup error、零 active stream，Core `PASS`。能力地图另以独立 render-only Plan
`dcb87de55a293a8220d24ebe955a94e8113ba2cb331406c5bbc2b57434d979f9` 和 session
`github-render-9a25a660bc7e4bfbbccb73d5d53565cd` 取得相同 public-render 闭包；它不消耗或冒充 P1 API coverage。

联合 verifier 还核验 sealed Plans、Evidence、handoff、reports、逐响应字节、session/Plan 不复用、九份公开文件
与 Git tree 的 byte identity，以及 architecture DOT/SVG 相对 maintenance base 未改变。成功 summaries 的连接摘要为：

```text
193f5b0b2bd8c404ef4d495b679bd99c60b203be22f06ad9a8794ae787497ca3
```

包含首败、三份 paired PASS、system-map render PASS、CI 与文件身份的 canonical manifest 为：

```text
sha256_json = f8759f0ec46b79b0a0315180d410f6ec6b43ddd0267b87fa40570ef5d01b9cb8
```

这些事实只使合同候选有资格进入本状态发布，不能替代本 publication 自己的最后门。

## 6. 有限实现授权与停止线

最后门全部成立后，下一分支只能从新的 exact main 严格串行实现文档 183 第 11 节 A–F：

```text
A. private admission gate and exact RelationSet construction state
B. same-ID provenance / conflict / reverse-run conformance
C. private explicit admission witness construction
D. DerivationEvidence 0.2 Schema + independent corpus + identity vectors
E. private non-published Evidence 0.2 projection boundary
F. RAE-000..017 hardening and cross-runtime byte proof
```

A–C 不依赖 public file；D 只能新增版本化 Schema/corpus；E 只能构造 private new-copy projection。任何一步若
要求 publisher、Manifest role 扩张、第九文件、Slice 或 Coverage 才能成立，必须停止并用新反例重开最小合同。

本冻结不授权 output path、artifact writer、八文件 publication、Release、standalone admission Artifact、public
Provider SPI/registry/discovery、完整 import resolution、ReviewSlice traversal、CoverageLedger、Attention ranking、
CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 7. 本状态发布自己的最后门

本 docs-only publication 只允许同步 `AGENTS.md`、`README.md`、文档 114、文档 183、`docs/milestones.md`
并新增本文；architecture DOT/SVG 因拓扑未变而必须保持字节不变。提交前必须通过适用 focused 双 Python
normal/`-O` 回归、Markdown relative links、fence/heading、状态 marker、敏感模式、本机路径、exact diff scope
与 `git diff --check`。这些本地结果不替代本文自己的远端 required checks。

本 publication worktree 的最终 focused 门严格从 `plugins/review-attention` 的真实 source root 串行运行
`test_relation_observation_qualification + test_boundaries`：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `26 tests / 30.882s / OK` |
| CPython 3.10.6 `-O` | `26 tests / 29.987s / OK` |
| CPython 3.13.13 normal | `26 tests / 31.073s / OK` |
| CPython 3.13.13 `-O` | `26 tests / 30.441s / OK` |

第一次命令只把 root `src` 作为 `PYTHONPATH`，在导入 `veritrail_review` 和两个 test modules 时停止，未进入
任何被声明测试；该 source-root/test-discovery setup failure 不伪装成两项产品测试失败，也不被后继 26/26
写成已经执行。两套 Python 的 root Markdown regression 各为 `4/4`。最终静态门精确读取六个 Markdown
变更文件，检查 429 个 relative links 且零断链；UTF-8 无 BOM、LF-only、fence 平衡、heading 唯一、12 个
状态/证据 marker、无 tab、本机绝对路径或敏感 token-like value。`git diff --check` 通过，architecture DOT/SVG
与本分支 base 的 Git blob identity 相同。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> capability map fresh anonymous render-only readback
    -> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用 PR #171、PR #172、candidate exact-main 门或
candidate readback 替代本文自己的最后门；在完整链成立前不得写 runtime。

当前原则冻结为：

> Same semantic content may be re-observed; admission authority must be independently established for each
> admissible publication history.

中文：**内容身份可以复用，来源历史可以不同，但准入资格必须逐次成立，不能因为字节或语义摘要相同而继承。**
