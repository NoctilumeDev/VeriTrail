# R1 Relation Derivation 实现冻结发布

## 1. 文档身份与条件状态

> 状态目标：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[Relation Derivation Authority / Operand Continuity 合同冻结发布](170-r1-relation-derivation-contract-freeze-publication.md)
>
> 实现候选：[Relation Derivation 实现冻结候选](171-r1-relation-derivation-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@eb75d360b828fd45007be9f94892e4101af27e50`
>
> 候选合入 Tree：`d03e60fb7557a1d86e876a18c6b40c55ee574823`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 170 冻结的 private Relation derivation seam 已按文档 171 完成实现、候选门禁、受保护
主线合入、新 exact-main 双门和 fresh anonymous installed-product readback 的事实。本文不创建或修改
源码、测试、Schema、identity vector、corpus、依赖、CI、Provider/parser、RelationSet、publisher、Slice、
Coverage、Manifest、CLI、Workbench、Core、P/Q/D/Cu、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，
以及针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为
当前主线事实；在此以前，本分支文字不授权任何后继实现。

## 2. 本次冻结的最小对象

本次只冻结一个 private、closed-fixture、non-published Relation production closure：

```text
Fact ProviderRuns terminal
        ↓
private Fact-stage join
        ↓
exact composed FactSet
        ↓
provider-operands/0.2 + fact_set_digest
        ↓
conservative Relation eligibility gate
        ↓
distinct Relation ProviderRun / execution cell
        ↓
real fixed Python 3.10 grammar parser
        ↓
private canonical Relation candidate history
        ↓
Relation terminal + release
        ↓
final private execution-status projection
```

Fact phase 与 Relation phase 共享同一个 live `BudgetContext`、absolute deadline、stop latch 与 parent attempt；
第二阶段不能重新发放预算。Relation run 只消费 copy-owned exact FactSet operand，Fact Provider 不回填 Relation
报告，application 也不自造 Relation target、candidate 或 provenance。

该对象没有 public Provider authorization/discovery、完整 import resolution、RelationSet admission、
RelationConflict ledger、Artifact writer、publisher 或 final Evidence authority。private candidate 的存在不等于它
已经被 admitted、published、覆盖完整或取得 Verdict 权。

## 3. 实现候选的精确链

实现从已冻结合同基线独立建立：

```text
contract freeze main = 04cdc6bd3aa33ee77819af9e5764591d3469004c
implementation head  = db6148020b3333104a93ec602c7a7c1c5a5e3ab6
implementation merge = 122d0c6b9d3c7a4518f12aec2f503f8979018dda
implementation tree  = 5db4e21a7fceda54eab184b0fea498d365da1fee
```

[PR #156](https://github.com/NoctilumeDev/VeriTrail/pull/156) 的原始 Public CI run
`35512727369` 为 pull_request / attempt 1 / 11/11 SUCCESS。实现以普通 merge commit 合入受保护主线；
`main@122d0c6...` 的新门为：

```text
Public CI      run 35513598312  push / attempt 1  11/11 SUCCESS
Browser Smoke run 35513598411  push / attempt 1   1/1 SUCCESS
```

全部十一份变更文件又从 implementation exact SHA 完成无 token raw-byte 读回，逐项与 Git tree 同大小、同
SHA-256 和同 blob identity；规范行摘要为：

```text
52510795bf4a479d3f6b58cd1aaa643eb0560d6f764f726b89ee0c9e37b8ea4f
```

文档 171 的 docs-only 候选链为：

```text
base    = 122d0c6b9d3c7a4518f12aec2f503f8979018dda
head    = b07018c62aa8cb9fb6c7cd134d1af7b61d4d6e9d
merge   = eb75d360b828fd45007be9f94892e4101af27e50
parents = 122d0c6b9d3c7a4518f12aec2f503f8979018dda
          b07018c62aa8cb9fb6c7cd134d1af7b61d4d6e9d
tree    = d03e60fb7557a1d86e876a18c6b40c55ee574823
```

[PR #157](https://github.com/NoctilumeDev/VeriTrail/pull/157) 的原始 Public CI run
`35514936331` 为 pull_request / attempt 1 / 11/11 SUCCESS。候选 exact main 的新门为：

```text
Public CI      run 35515864709  push / attempt 1  11/11 SUCCESS
Browser Smoke run 35515864729  push / attempt 1   1/1 SUCCESS
```

## 4. 候选 fresh anonymous installed-product readback

读回从 exact `main@eb75d36...` 的 detached worktree 取得 orchestration probe，在 fresh venv 中匿名下载并
复算固定 Release wheel SHA-256：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

两项下载均为 HTTP 200，导入路径位于该 fresh venv 的 `site-packages`。清空 `GH_TOKEN`、`GITHUB_TOKEN`、
`VERITRAIL_GITHUB_TOKEN` 后，针对 exact `eb75d36...` 建立三次互不复用的
`P1 API -> P2 Render -> P3 handoff -> Core` 正式 session：

| Target | Session | Plan | Handoff | P1 Evidence | P2 Evidence | Report |
| --- | --- | --- | --- | --- | --- | --- |
| README | `github-paired-80fefaaa667a4dde8453567ad7bfd9aa` | `a82c24418738411738a52ea8345dd90052c000c67451bea6b629450807dd79e0` | `a57826997c93e17eea72c24a126d89ae46280ab2f762133585e5a680a106e7a7` | `147223c193b97f6e1656ce3e78459a56bdd943515ba10c7ba9f7ccba37b26d2f` | `fafbecaa7f4839bfe84538aa85c0bccdc3514047a9f99f26cd2b3373953e5de3` | `0bd8017e201a6e777f078b5cbbbbb4fd1e9b5e0b7f01fbb9af9208b427d7bdb2` |
| Document 171 | `github-paired-97cf7e4e6d064c6bbd001b975079e4fd` | `eef78625f588708590cdd0af6c00010aed889ee152a7e215e93a625c4ba05eca` | `b3ea7fa9bd9075e8f72945aeb8631d9e6d2852070987574cdc13f5c238e02292` | `9b70c3a9e7e3c1dcf5cd7bf5468364a2af8546fa21613d3015e1c052b4d39c43` | `0f4045c133ace05bbb381fdf88c1b0e7873bf288ab6b62d0bb46503450cb9309` | `58a28289c4fbf8b50457efdca748fcc507d0c58a01ba96271eac2337f7e70f4c` |
| Milestones | `github-paired-430672ffe402418f95850e848604dfdc` | `e2f104caeb78a4dbed45741a2c434655f63dbbe2ed0721c07e6b3896823f04bb` | `02e901a5b7451683efaf2859fc6ce40e4d8798eed5dd524a82de229f8f7f329b` | `b3e51eb88fb1f13d861f94576d4ab8f79bb3148fc6315991eb1781cda417abc6` | `2913c3d618956b7720ffdc35aba0c3467613238488ed5ee20ca658dddcf32654` | `118a944c6c405897b43facc1569d7c7b2ec31416f6e380719deab2f85fbcd0da` |

三次均为 HTTP 200、requested/final exact-SHA path 相同、P1/P2 coverage `COMPLETE`、唯一固定作用域、
三个样本稳定、marker 恰好一次、零 conflict/error/coverage reason/cleanup error、零 active stream，Core
`PASS`。固定 manifest 将页面标签、repository path、marker、完整 summary、Render facts digest 与 sample
digest 按 README、文档 171、milestones 顺序做 canonical `sha256_json`，结果为：

```text
8cd8efe6499cd754ab2668e87e8534c26858a178fd65da55141ae8a1761746d2
```

## 5. 保留的首次 README 失败与归因边界

正式成功前的第一条 README session `github-paired-79f112178b8a48829710e7d47aaec085` 必须继续保留为不合格
事实。该 session 的 P1 为 `PUBLISHED / COMPLETE`；P2 观察到 HTTP 200、唯一作用域、三个稳定样本、正确
marker 与干净 cleanup，但 response-body snapshot 为：

```text
request_count                    154
allowed / blocked               152 / 2
blocked_write / affects_coverage 2 / 0
completed / closed responses    151 / 151
response_error_reason_counts    BlockedByClient: 2
failure                         PublicRenderNetworkError
coverage                        ERROR
```

源码与合同复核证明预期 telemetry write 的 `BlockedByClient` 已由 body controller 显式保持中性；后继诊断与
正式成功 session 仍有相同的 `154 / 152 / 2` network counts 和两个 coverage-neutral blocked writes。因此不能把
首败归因为 blocked write 的二次计罪。

首败的 `final-health` 已成功，异常只在 cleanup/snapshot 之前进入；Public Render Evidence 0.1 只持久化异常
类名，没有足够安全诊断字段从该不可变 Artifact 恢复具体 response-stage 原因。独立诊断 session
`github-paired-dac4b80cf52d4f6fa230de2aa96e8ff5` 使用旁路观察器且没有复现异常；因为它改变了观察环境，明确
不进入本冻结门。现有证据只能保持根因 `UNKNOWN`，不能进一步声称 teardown race、代理、GitHub 页面或某个
具体响应是单一原因。

新的正式 README session 使用新 sealed Plan execution、collection session 与输出根取得资格，不重写首败，也
不把未复现解释成已经修复。0.1 的安全 diagnostic provenance 粒度可作为 future maintenance candidate；它没有
阻塞本次 Relation 事实闭环，也不授权在本文修改 P2 Schema、collector 或 coverage 语义。

## 6. 已冻结不变量

1. Relation 输入绑定 exact composed FactSet 与 `fact_set_digest`；旧 run 不能自然迁移到另一 operand universe。
2. Relation 是独立 ProviderRun / execution cell；Fact Provider、application 与 publisher 都不能冒充 producer。
3. Fact/Relation 两阶段共享一个 live BudgetContext、absolute deadline 与 stop latch，不刷新资源合同。
4. FactConflict、optional gap、required non-success、whole-attempt stop 或 absent normal FactSet 均不启动 Relation。
5. 成功空集合必须来自真实 start、terminal 与 residue-free release；`NOT_STARTED` 不能冒充 empty success。
6. parser identity 只在 Provider 真实使用固定 parser 后报告；identity 字段不能替代实际执行。
7. deadline、cancel、memory、unavailable、failed、nonconformant 与 release failure 保持 typed 区分；失败后不保留
   prefix candidate。
8. private Relation candidate、canonical bytes 与 Provider confidence 都没有 RelationSet admission、publication、
   Coverage 或 Verdict authority。

## 7. 明确未冻结与下一停止线

本次没有冻结、实现或授权：

- fixture-bounded proof 之外的完整 Relation algorithm 或真实 import zero/one/many resolution；
- RelationSet composition/admission、multi-Provider Relation merge、RelationConflict 或 UNKNOWN 扩展资格；
- conflict-bearing FactSet 或 optional-gap 已知前缀的局部派生；
- public Provider SPI/registry/discovery、caller-selected Provider、publisher、Manifest 或 output coordinate；
- ReviewSliceSet、CoverageLedger、Coverage UNKNOWN denominator 或 Attention Proposal；
- CLI、Workbench、Core 新判断、Q runtime、D、Cu、JPyxis adapter、tag 或 Release。

本文最后门全部成立后，唯一合法下一步是从新的 exact main 重新做 Relation post-freeze system audit。内部
Evidence、仓库历史与本地 falsifier 优先；只有审计提出了具体经验缺口，才按 failure family 选择性查询外部生产
案例。公开案例只能产生 hypothesis，不能直接成为 R 合同或施工授权。

## 8. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须
通过适用的 focused 四格回归、完整 Review Attention 回归、root Schema 回归、Markdown relative links、
fence/heading、状态 marker、敏感模式、exact diff scope 与 `git diff --check`。这些本地结果不替代本发布
自己的远端 required checks。

本文 worktree 串行执行 Relation 与 broad boundary 两个 focused suite；每格分别为 15 与 9 项：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `15 + 9 tests / 38.119s + 0.118s / OK` |
| CPython 3.10.6 `-O` | `15 + 9 tests / 38.751s + 0.116s / OK` |
| CPython 3.13.13 normal | `15 + 9 tests / 39.071s + 0.155s / OK` |
| CPython 3.13.13 `-O` | `15 + 9 tests / 37.465s + 0.142s / OK` |

同一 worktree 的完整 CPython 3.13 normal Review Attention 回归为 `178 tests / 373.949s / OK`；root
Schema 回归在 CPython 3.10.6 为 `27 tests / 0.482s / OK`，CPython 3.13.13 为
`27 tests / 0.269s / OK`。全部测试串行运行，未用并发负载缩短 Windows lifecycle 与 cleanup 观察窗口。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_RELATION_DERIVATION_FROZEN 成为当前主线事实
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用 PR #156、PR #157、candidate exact-main 门或
candidate readback 替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
