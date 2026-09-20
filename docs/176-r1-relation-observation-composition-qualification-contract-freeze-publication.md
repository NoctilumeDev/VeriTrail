# R1 Declared Relation Observation Domain / Composition Qualification 合同冻结发布

日期：2026-09-21

## 1. 发布对象、输入与条件状态

本文只发布[文档 175](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
已经审议的最小合同，不实现 runtime，也不把 private qualification 提前解释为 RelationSet 或公开事实。

| 坐标 | 值 |
| --- | --- |
| 上游冻结状态 | `R1_RELATION_DERIVATION_FROZEN` |
| 前置系统审计 | [文档 173](173-r1-declared-relation-observation-domain-and-composition-qualification-system-audit.md) |
| 合同候选 | [文档 175](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md) |
| 候选 PR | `#160` |
| 最初语义起点 | `main@559bf9b9a052f0b542227b1cea069dd15c696cc8` |
| maintenance-qualified base | `main@962251d91bc2695afe984ee47845ac4fe1a80f7e` |
| 候选 head / merge / tree | `fde8df8279c27b5a222d58d2b0a5fd73c261a54f` / `bc495eb92c70f85566505d51d00677ac14f38ff2` / `a60677888f76de6a108bf13c13fa9c73b9485c83` |
| 影响层级 | `L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

本文分支、原始远端门、受保护主线合入、合入后 exact-main Public CI / Browser Smoke 与本文专属 fresh
anonymous installed-product readback **全部成立以后**，目标状态才是：

```text
R1_RELATION_DERIVATION_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_PRECONTRACT_AUDITED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_ALLOWED
R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

在最后一项门禁成立前，这些只是本发布的条件目标；文档 175 的 `CONTRACT_CANDIDATE` 仍是当前已证事实。

## 2. 本次冻结的最小对象

冻结对象是 **exact FactSet 上预先声明的 bounded Relation observation responsibility，以及逐 item 履责、
候选对账和多来源 composition qualification 的 private contract**。它只包含以下相互不可分的边界：

1. Profile vocabulary、Policy requiredness 与 private observation profile 分离；Profile 列出的 relation kinds
   不自动成为已观察分母；
2. application 在任何 Relation Provider 运行前，从 exact copy-owned FactSet 机械建立 Fact-backed observation
   items，并用冻结的 family、negative policy 与 Provider responsibility semantics 固定 domain identity；
3. 首个 closed proof 只有两个 exact required sources：A 负责全部 `LEXICAL_CONTAINS` items，B 负责全部
   `LEXICAL_CONTAINS` 与 `IMPORT_TARGET_LITERAL` items；缺失、额外、重复或漂移 binding 在执行前拒绝；
4. relation-only `provider-operands/0.3` 与 private relation-cell `/0.2` 分别绑定 exact domain、assigned item IDs、
   terminal outcomes 与 candidates，不改写历史 `/0.2` operands 或 `/0.1` wire；
5. Provider 必须为每个 assigned item 在真实 bounded operation 后报告显式 outcome；application 只能做
   outcome/candidate 双向机械对账，不能从 candidate absence 补 negative；
6. Provider terminal、required source-set terminal closure、required observation closure、candidate composition
   与 qualification status 分别保存；定义 responsibility 不等于已经履责；
7. same-ID candidates 只合并 provenance，same-subject incompatible candidates 保留 private conflict；
   `QUALIFIED` 可以与 `CONFLICTING` 同时成立，但两者都没有 admission 或 Verdict authority；
8. complete-empty 只在 assigned items 为空、Provider 真实启动并 `COMPLETED`、outcomes/candidates 为空且
   residue-free release 时成立；non-empty responsibility 上的空输出不能冒充 closed negative；
9. 当前公共 RelationSet 0.1 与 DerivationEvidence 0.1.1 不足以让第三方复算 qualification，因此首个实现
   只能返回 private owned result，不写 Artifact、Manifest、RelationSet 或 final Evidence。

该冻结只回答：在本合同声明的 bounded observation domain 内，哪些责任被预先定义，哪些履责记录能够经过
机械对账，以及多来源 candidates 是否完成一致或冲突的 private composition。它不证明 Provider 内部认知过程、
candidate 真实性、完整 Python Relation universe、缺陷存在、Coverage 完整或任何 Core Verdict。

## 3. 原始首败、独立维护与重新资格化

PR #160 原始 head `44caffaa08ab67bcb83760d86bdbad7e30081b6f` 的 Public CI run
`35530411983` attempt 1 真正执行 450 tests 后，在 Python 3.13 暴露既有 listener-owner-mismatch fixture
时序缺口并得到正式 `FAILURE`。该首败不被后继绿灯、旧 head rerun 或归因修正覆盖。

[文档 174](174-m10-listener-owner-mismatch-fixture-timing-correction.md)与独立 PR #161 只修测试夹具的注入
时间坐标：external owner 在 disputed node 真正进入冻结 readiness adapter 时建立，仍保持原 `1.5s` 自然退出，
同时证明系统不杀 external owner 且端口会在 cleanup deadline 内释放。被反例否决的 `30s` lifetime 候选合法
产生 `CLEANUP_ERROR`，因此没有进入最终修复。维护链为：

```text
PR #161 Public CI 35532371731  pull_request / attempt 1  11/11 SUCCESS
maintenance merge 962251d91bc2695afe984ee47845ac4fe1a80f7e
Public CI          35533373276  push / attempt 1          11/11 SUCCESS
Browser Smoke      35533373269  push / attempt 1           1/1 SUCCESS
```

本地显式绑定四个 source roots 的 450-test 四格只证明 current-source composition regression，不冒充
installed-product/CI topology；PR #161 自己的远端门和 exact-main 门提供后一层资格。合同语义没有由 maintenance
改写。

PR #160 随后从 maintenance-qualified exact main 重建 source state，形成新 head
`fde8df8279c27b5a222d58d2b0a5fd73c261a54f`。更新 PR body 触发的同 head workflow
`35534733454` 被 concurrency 行政取消，未形成完整测试结论；有效资格 run 为：

```text
PR #160 Public CI 35534770529  pull_request / attempt 1  11/11 SUCCESS
candidate merge   bc495eb92c70f85566505d51d00677ac14f38ff2
Public CI         35535740629  push / attempt 1          11/11 SUCCESS
Browser Smoke     35535740617  push / attempt 1           1/1 SUCCESS
```

因此历史同时保留：原 head 的正式产品相关首败、独立测试维护、一次没有测试结论的行政取消，以及新 source
snapshot 上的完整资格。maintenance 的绿没有替合同背书；重新资格化的绿也没有把旧失败改成“从未发生”。

## 4. 候选 exact-main 匿名产品读回

读回从 detached exact `main@bc495eb...` 取得 orchestration probe，并在全新 CPython 3.13 venv 中安装冻结
Release wheels：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

导入路径均位于该 fresh venv 的 `site-packages`；没有使用 repository `PYTHONPATH`。清空 `GH_TOKEN`、
`GITHUB_TOKEN` 与 `VERITRAIL_GITHUB_TOKEN` 后，对 README、文档 175 与 milestones 建立三个互不复用的
sealed Plan、collection session 与 output root：

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-275b94cda1ec4c17be3becaf7f21d83f` | `340a9cfef9b82c8804a4e0a59f674fdef45d981b31ea9fdfd36a6f7250df78a6` | `bae9d50d48c4884b973ed5c5b2fe39934a6548e6e12b264a614cba064326592b` | `02bcd4c89170506330a0ebea230847d68754332d0f1c8ca16ea74e0438e8061a` | `e4e644626d1d374246479732a4d544e082ac3edaef3626fea5a0e0e2a8a0c9ed` | `684b6591c0822c1493331264bfc4a497e13ae1b61295a85f5a9e4bfe9e7224ed` |
| Document 175 | `github-paired-79eaa25f9a46491ea9ffb08d2a47dccc` | `2ff733351b2a134a03d7de58fca365ef8c210e00d03f7d75ea81216766d71a0e` | `f31770705cceed384cc42a0a06a8cb61f73f01950f71de31ebdb661c744b65c7` | `a8550fa1e608b593aeba47ef732bd1056fc80d35c8ff2f20192e0f8dad0362c4` | `0a670ce0fe1f020ee25e3ba367c1cf6de3113d8344d23f4dfb8e6fd22252b903` | `3f31a7075eb6fb63461347710277f70dc157af5f19130b9e909c192c75687845` |
| Milestones | `github-paired-9a888f0244b049b09087633b2c5788c9` | `28dbe4cedbea05b353ce5fe0acc966a37aee300fa380a5125903c72d0489d45c` | `65e9ba69e034bf41bdd3b3c93d5ae614a64e99be96da46fafb83de805a2f9ee4` | `5df7f0ec466c7fd49e9170f10226167d80d5409664019b05de287ee6ea904f6f` | `91dae7af5171c036ae0799f51fe8e8a08bfa4c161a5ee1fe71aa02c83eab9cb4` | `d3052ca023bcf73d72f8fcbdc1683a53d9aa8835f495a93d75c1aac1e1126c29` |

三次均为 HTTP 200、requested/final exact-SHA path 一致、P1/P2 coverage `COMPLETE`、唯一固定 scope、
三个样本稳定、marker 恰好一次、零 conflict/error/coverage reason/cleanup error、零 active stream，Core
`PASS`。canonical manifest 重新校验 sealed Plan、报告、Evidence digests、逐响应字节账与三组 identity 的
独立性，得到：

```text
sha256_json = 0df7a15fb0193f2d86d26b07fc96991cdada73d28058e5edb6e7cbf426bc194c
```

这只证明候选 exact commit 的公开内容、安装产品与 Core 验收闭包，不替代本文 publication 自己的最后门。

## 5. 已冻结不变量

1. responsibility 必须在 Provider 执行前由 exact FactSet 与冻结 responsibility semantics 决定，不能从实际
   candidates 反向构造 denominator；
2. `responsibility defined != responsibility discharged`；ProviderRun `COMPLETED` 不能自动升级成逐 item closure；
3. Profile vocabulary、capability requiredness、Provider responsibility、outcome、receipt 与 qualification identity
   分离，任一层不能替另一层背书；
4. 每个 assigned item 必须有一个合法显式 outcome；candidate absence 不产生 negative，application 不替 Provider
   补履责记录；
5. outcome 与 candidates 必须双向闭合；missing、unexpected、duplicate、dangling、mismatched 与 unreferenced
   分别保留，不能靠删除 source 或缩小 domain 修复；
6. terminal closure 只说明 required runs 都到达真实终态；observation closure 另要求每个 required source
   `COMPLETED`、residue-free release 且逐 item 对账完整；
7. empty domain 的 complete-empty 不等于源码没有 Relation；non-empty domain 的 `COMPLETED + []` 在当前
   total-obligation profile 上永远不能 qualification；
8. same-ID union 与 same-subject conflict 分离；observation `COMPLETE` 可以与 composition `CONFLICTING` 同时
   成立，冲突不被选择 winner 或压成 qualification failure；
9. `QUALIFIED` 只表示 bounded obligations 有显式履责记录并完成机械 composition，不等于 candidate true、
   admitted、published、Coverage complete 或 Verdict；
10. A/B Relation sources 继续共享原 live `BudgetContext`、absolute deadline 与 stop latch；普通 source failure
    不刷新预算，也不在 context 安全时阻止观察剩余 required source；
11. 现有 RelationSet/Evidence shape 不能凭字段存在证明 qualification；Schema-valid 不等于 authoritative；
12. private outcome/receipt/qualification 不写文件、不进入 Manifest，也不成为新事实 owner。

## 6. 冻结后的有限实现授权

最后门全部成立后，下一分支只可从新的 exact main 严格串行物化文档 175 第 14 节的 A–H：

```text
A. private observation profile + exact A/B responsibility/binding admission
B. FactSet-derived observation items + domain identity
C. relation-only provider-operands/0.3 + relation-cell/0.2
D. shared-budget serial A/B execution + Provider-owned per-item outcomes
E. application outcome/candidate reconciliation + source-local receipts
F. same-ID union / same-subject private conflict / qualification projection
G. immutable OwnedRelationCompositionQualificationResult
H. RQ-001..028 hardening
```

每一步都是停止线。实现只能形成 private construction state，并必须继续通过 `RO-000..007` 与
`RQ-001..028` 的单变量反例。若 FactSet 不能机械建立 denominator、parser identity 无法诚实绑定、历史
identity/wire 不能保持兼容，或 qualification 必须提前进入公共 Artifact，必须停下并重开最小合同，不能在
runtime 中缩分母或扩 authority。

## 7. 明确未授权

本冻结不授权：

- fixture-bounded proof 之外的完整 Relation algorithm 或真实 import zero/one/many resolution；
- public Provider SPI、registry、discovery、ambient Provider 或 caller-selected responsibility；
- 公共 Schema correction、RelationSet admission、final Evidence、Manifest、publisher 或 output coordinate；
- 把 private conflict 解析成 winner，或把 `QUALIFIED` 当成真值、缺陷、Coverage、Attention 或 Verdict；
- conflict-bearing FactSet、optional Fact-source gap 或 optional Relation source 的扩展资格；
- ReviewSliceSet、CoverageLedger、Coverage UNKNOWN denominator 或 Attention Proposal；
- CLI、Workbench、Core 新判断、Q runtime、D、Cu、JPyxis adapter、tag 或 Release；
- 对历史 Artifact、失败 attempt、`provider-operands/0.2`、relation-cell `/0.1` 或旧 ProviderRun 的重写。

## 8. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须
通过适用的 focused 双 Python normal/`-O` 回归、Markdown relative links、fence/heading、状态 marker、敏感模式、
本机路径、exact diff scope 与 `git diff --check`。这些本地结果只证明 publication 没有暗改冻结 runtime，不替代
本文自己的远端 required checks。

本 publication worktree 的本地门如下：

```text
exact diff scope
  PASS: README.md / AGENTS.md / docs/milestones.md / this document only

Markdown/static
  PASS: git diff --check
  PASS: 340 relative links, zero broken links, balanced fences, unique headings
  PASS: no tabs, local absolute paths or sensitive token values
  PASS: tests.test_markdown, CPython 3.10.6, 4/4
  PASS: tests.test_markdown, CPython 3.13.13, 4/4

focused frozen-runtime regression
  PASS: CPython 3.10.6 normal, 24/24, 37.201s
  PASS: CPython 3.10.6 -O,     24/24, 38.385s
  PASS: CPython 3.13.13 normal, 24/24, 37.216s
  PASS: CPython 3.13.13 -O,     24/24, 37.405s
```

四个 focused 门均串行运行 `test_relation_derivation + test_boundaries`，并在测试前用 `__file__` 证明
`veritrail_review` 来自本 publication worktree。没有使用并发负载缩短 Windows deadline、terminal、release
或 cleanup 观察窗口。任何后继 command-construction 或不完整环境失败仍必须按其真实层级记录，不能伪装成
runtime 反证，也不能从最终表中抹掉已经形成正式 observation identity 的失败。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_CONTRACT_FROZEN
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用 PR #160、PR #161、candidate exact-main 门或
candidate readback 替代本文自己的最后门；在这条链成立前不得写 runtime。
