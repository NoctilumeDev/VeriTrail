# R1 Relation Observation / Composition Qualification 实现冻结发布

## 1. 文档身份与条件状态

> 状态目标：`R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 最小合同：[文档 175](175-r1-declared-relation-observation-domain-and-composition-qualification-contract.md)
>
> 合同冻结：[文档 176](176-r1-relation-observation-composition-qualification-contract-freeze-publication.md)
>
> 实现候选：[文档 178](178-r1-relation-observation-composition-qualification-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@49b7cbc877049377f78f2c845db75ad89ec189a1`
>
> 候选合入 Tree：`3e7fbcf48995e8443125cabaaec60795a827267d`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 175/176 冻结的 private Relation observation-domain / composition-qualification closure 已按
文档 178 完成实现、重新资格化、实现候选门禁、受保护主线合入、新 exact-main 双门和 fresh anonymous
installed-product readback 的事实。本文不创建或修改源码、测试、公共 Schema、identity vector、corpus、依赖、
CI、RelationSet、final Evidence、publisher、Slice、Coverage、Attention、CLI、Workbench、Core、P/Q/D/Cu、
tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及
针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为
当前主线事实；在此以前，本分支文字不授权任何后继实现。

## 2. 本次冻结的最小对象

本次只冻结一个 private、closed-fixture、non-published observation/composition qualification closure：

```text
exact frozen FactSet + observation profile
        ↓
Fact-backed observation domain
        ↓
fixed A/B exact responsibility assignment
        ↓
distinct Relation source ProviderRuns
        ↓
per-item ObservationOutcome + candidate report
        ↓
source-local receipts and terminal accounting
        ↓
bidirectional outcome/candidate/provenance reconciliation
        ↓
same-ID provenance merge + private same-subject conflict
        ↓
owned private qualification result
```

两个 source 共用 Relation derivation 已冻结的 live `BudgetContext`、absolute deadline 与 stop latch。Provider
只消费 exact FactSet 对应 operation blob；application 只验账，不从 candidate absence、Provider terminal 或公共
Schema shape 补造 negative observation、责任闭合或 Relation truth。

`QUALIFIED` 只证明本次 bounded responsibility 已按合同履行并记账；它可以与 `CONFLICTING` 同时成立。它不
证明完整 Python Relation universe、candidate 真实性、conflict 已解决、RelationSet 已 admission、Coverage 完整、
final Evidence 已发布或任何 Verdict。

## 3. 实现与维护因果链

实现链保持原始首败、独立 maintenance 与重新资格化 head 分离：

```text
contract freeze main = 65bdfa0a05f96693a7df9a1a86e27ecdb503b875
original impl head   = 015bf8f19ca1269933749c53f67eebe33186bc58
maintenance head    = 189abdfdf73a6b5b2f9e462b81f1b19b9fae8f94
maintenance merge   = 43fd5d3368f962677722d09d962718bced306449
requalified head    = 4bcba01dbdc7fb57c34451d154be8ef8f52bfb87
implementation merge= 3b4a55cad4e4f093c27dd8e9736d24d3b905dd54
implementation tree = f2becc7d31f7ca29fc265ea7690be248a48bf05e
stable patch-id     = bfbb87ec732a203bd9e8c321a45b2dc3574aeb5c
```

PR #165 原始 Public CI run `35569800950` 的两条正式首败继续成立。Python 3.13 的旧 listener fixture 把
瞬时空闲端口误作已预约；Python 3.10 的 `COLLECTOR_ERROR` 精确根因保持 `UNKNOWN`。独立 maintenance PR
#166 只修测试前置条件与 test-only diagnostic observation；它没有修改 R runtime、公共 Evidence、timeout 或
#165 implementation patch。

maintenance final-head Public CI run `35573748557` 为 attempt 1、11/11 SUCCESS；maintenance exact main
`43fd5d3...` 的 Public CI run `35575271109` 为 11/11，Browser Smoke run `35575271103` 为 1/1。重新资格化
#165 head 的 Public CI run `35577081157` 为 attempt 1、11/11 SUCCESS；实现合入后 exact main
`3b4a55c...` 的 Public CI run `35578893674` 为 11/11，Browser Smoke run `35578893670` 为 1/1。

这些绿色只证明各自 source state 的资格，不解释或覆盖旧失败。十一份实现文件的匿名 exact-SHA raw-byte
readback 与 Git tree 逐项一致，规范行 SHA-256 为：

```text
9c36591b276df231ee6f03145fb52d683c9c0ce2ca78f4e72ef3c9bb702d3da6
```

## 4. 实现候选的精确链

文档 178 的 docs-only 候选链为：

```text
base    = 3b4a55cad4e4f093c27dd8e9736d24d3b905dd54
head    = 8b9dd79e3397b663b90bafae5119d76462951153
merge   = 49b7cbc877049377f78f2c845db75ad89ec189a1
parents = 3b4a55cad4e4f093c27dd8e9736d24d3b905dd54
          8b9dd79e3397b663b90bafae5119d76462951153
tree    = 3e7fbcf48995e8443125cabaaec60795a827267d
```

[PR #167](https://github.com/NoctilumeDev/VeriTrail/pull/167) 的原始 Public CI run
`35584243147` 为 pull_request / attempt 1 / 11/11 SUCCESS。候选 exact main 的新门为：

```text
Public CI      run 35585937377  push / attempt 1  11/11 SUCCESS
Browser Smoke run 35585937328  push / attempt 1   1/1 SUCCESS
```

## 5. 候选 fresh anonymous installed-product readback

读回从 exact `main@49b7cbc...` 建立 detached source coordinate，在 fresh CPython 3.13 venv 中通过公开
Release URL 匿名下载并复算固定 wheel SHA-256：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

两项安装后都从 fresh venv 的 `site-packages` 导入，并配套 Playwright 1.62.0 与 matching Chromium。清空
GitHub token 环境后，针对 exact `49b7cbc...` 建立三个不同 Plan ID、Plan digest、collection session 与输出根的
`P1 API -> P2 Render -> P3 handoff -> Core` session：

| Target | Plan ID | Session | Plan digest | Handoff | Report |
| --- | --- | --- | --- | --- | --- |
| README | `r1-roq-impl-candidate-readback-readme` | `github-paired-bfbf22ed7e344de6b48f98ef187defaa` | `27560ffdfd63b02b910ca8aa072becabd3a0f9056b6f4b4e4f010c5850e43339` | `bce46d4777707915fd453a4848121f458ea7c8f06f685dd23dd1f35c4104f0f4` | `95e6c43a4c77730f7978c4812972b1d40a87413477e48e2646706596297d56a8` |
| Document 178 | `r1-roq-impl-candidate-readback-doc178-v2` | `github-paired-ce699057ff574be691851733f115344b` | `5baa846d0f08a096fdb7cdb21acfb3f655e49bd8b84e1d49f71b45c668efa423` | `a5bb9eb3d630454a84234d638b5ea46b7e9a0598f0522e8748e6bb22947494fe` | `dfe0a4435c5dd4f44c7cda78c6a3cedda7a88bd4b84d0081f9d11da79ba7219b` |
| Milestones | `r1-roq-impl-candidate-readback-milestones` | `github-paired-5a8fcd7d8cc84d37b663919d7cd25abc` | `e1291513b2b8aeee3efa93d8d62c43763f609a096dea3d7b7bb905eee6093690` | `86fe4e7b66246c77c458c6fa3c6b7b089972f1c793e5e5d5c1e20947868bece2` | `4665ef4cb7d67d5f1d8c9d8df2a08ea5e5e2ff11b610cc615b140938329b91d0` |

三次均为 HTTP 200、requested/final exact-SHA path 相同、P1/P2 coverage `COMPLETE`、唯一固定作用域、三个
样本稳定、marker 恰好一次、零 conflict/error/coverage reason/cleanup error、零 active stream，Core `PASS`。

联合 verifier 还逐项校验 sealed Plan、Evidence、handoff、report、summary、response byte accounting、匿名访问
模式与三组 identity 不复用。三个 canonical summary 按 README、文档 178、milestones 顺序连接后的 SHA-256 为：

```text
de6b6c444a5b0f7b3ecb3770ad2eeaec5b2206bd7d806f47cc698da360be037f
```

包含成功结果、首败和 harness history 的 canonical manifest `sha256_json` 为：

```text
8017762ce4e975dea0da8f71fa9c8388176d794a73f3c4bc2cdb1934b4798220
```

## 6. 保留的 readback 异常与归因边界

README session 的产品观察、sealed acceptance report 与 canonical implementation-candidate summary 已完整落盘，
状态为 `COMPLETED / PASS`。wrapper 随后试图删除一个所选 immutable probe 从未创建的旧中间文件名
`p4-real-github-summary.json`，因 `FileNotFoundError` 退出 1。原 output 未修改且没有重跑；联合 verifier 独立
重验该 session 的 Plan、Evidence、report 与 summary。因此该事实分类为 harness postprocess cleanup filename
mismatch，不是产品 readback failure，也不能从日志中被省略。

文档 178 第一条正式 session `github-paired-fd900203c78547e4917b53a540158190` 使用 Plan ID
`r1-roq-impl-candidate-readback-doc178`。其 anonymous API 第一项 repository probe 返回：

```text
HTTP status  403
outcome      COLLECTION_BUDGET_EXHAUSTED
coverage     ERROR
limit/used   60 / 60
remaining    0
reset epoch  1789986741
```

同一 session 的 public render 为 HTTP 200、coverage `COMPLETE`、稳定样本、marker 一次且 cleanup 干净；它不能
抵消 API ERROR。该失败没有生成 acceptance bundle。quota reset 后先实测 anonymous `remaining > 0`，再使用
新 Plan ID `...doc178-v2`、新 collection session 与新 output root 取得正式 PASS。后继 PASS 不解释、修复或
改写首败；manifest 同时绑定失败 API/render bytes 的 SHA-256 与原 reset metadata。

## 7. 已冻结不变量与未授权能力

本次冻结以下边界：

1. observation domain 由 exact FactSet、冻结 profile/policy 与执行前固定的 responsibility 机械建立；实际输出
   不能反向缩小 denominator。
2. responsibility definition、Provider terminal、逐 item obligation fulfillment、required source-set terminal、
   candidate agreement 与 composition qualification 是独立状态。
3. `ObservationOutcome` 是独立履责通道；candidate absence、`COMPLETED` 或 empty array 都不能冒充 negative
   observation。
4. assigned item、outcome、candidate、terminal reported IDs、canonical bytes 与 provenance 必须双向闭合；
   application 只验账，不补事实。
5. same-ID/same-semantics 只合并 provenance；same-subject 分歧保留 private conflict；same-ID/different-semantics
   是 integrity failure。
6. interruption、deadline、memory、unavailable、failed、nonconformant 与 release failure 保持 typed 区分，
   且不得留下 prefix qualification。
7. `QUALIFIED` 可以与 `CONFLICTING` 同时成立，但没有 RelationSet admission、publication、Coverage 或 Verdict
   authority。

本次没有冻结、实现或授权 RelationSet composition/admission、完整 import resolution、public Provider
SPI/registry/discovery、caller-selected responsibility、公共 Schema correction、final Evidence、publisher、
Manifest、ReviewSliceSet、CoverageLedger、Attention Proposal、CLI、Workbench、Core 新判断、Q runtime、D、Cu、
JPyxis adapter、tag 或 Release。

## 8. 下一停止线

本文最后门全部成立后，唯一合法下一步是从新的 exact main 重新做 post-freeze system audit。审计应先读取内部
Evidence、仓库历史和本地 falsifier，判断冻结后的 qualification closure 实际暴露了什么缝隙；不得因为路线图上
写有 RelationSet、Slice 或 Coverage 就机械开工。

只有内部审计出现具体经验缺口时，才按 failure family 选择性查询外部生产案例。公开案例只能产生 hypothesis，
必须再由本地 falsifier 打穿后才可能影响下一合同；它不能直接成为施工授权。

## 9. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须
通过适用的 qualification + boundary 双 Python normal/`-O` 回归、Markdown relative links、fence/heading、
状态 marker、敏感模式、本机路径、exact diff scope 与 `git diff --check`。这些本地结果不替代本文自己的远端
required checks。

本 publication worktree 在同一最终字节上串行运行
`test_relation_observation_qualification + test_boundaries`：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `26 tests / 35.639s / OK` |
| CPython 3.10.6 `-O` | `26 tests / 33.568s / OK` |
| CPython 3.13.13 normal | `26 tests / 33.888s / OK` |
| CPython 3.13.13 `-O` | `26 tests / 33.550s / OK` |

两套解释器的 Markdown runtime regression 在补足当前 worktree Core `src` root 后各为 `4/4`。第一次两条
Markdown 命令都在 test import 前因 `ModuleNotFoundError: veritrail` 停止，没有形成四项测试 observation；
该 source-root topology setup failure 继续保留，不被后继 4/4 改写为已经执行。

最终静态门逐项读取四个 docs-only 文件，检查 346 个 relative links 且零断链；fence 平衡、heading 唯一、四个
发布 marker 可见、无 tab、无本机绝对路径或敏感 token-like value。exact diff scope 与 `git diff --check` 均
成立。四个 focused runtime 门严格串行，未用并发负载缩短 Windows deadline、terminal、release 或 cleanup
观察窗口。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用 PR #165、PR #166、PR #167、candidate
exact-main 门或 candidate readback 替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
