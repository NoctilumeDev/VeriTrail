# R1 RelationSet Admission / Public Qualification Binding 实现冻结发布

## 1. 文档身份与条件状态

> 状态目标：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN /
> R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 最小合同：[文档 183](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
>
> 合同冻结：[文档 185](185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)
>
> 实现候选：[文档 186](186-r1-relation-set-admission-and-public-qualification-binding-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@bf1d94104283573394db76939051a06da972cd12`
>
> 候选合入 Tree：`a334ee8bcf37b48033197e1ffe0f47e4764edb37`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布文档 183/185 冻结的 RelationSet admission、explicit admission witness 与 public qualification
binding 已按文档 186 完成 private closed implementation、实现门禁、受保护主线合入、新 exact-main 双门和
fresh anonymous installed-product readback 的事实。本文不新增或修改源码、测试、公共 Schema、identity
vector、corpus、依赖、CI、publisher、Manifest role、公共 Bundle、Slice、Coverage、Attention、CLI、
Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

本文自身仍须完成原始远端 required checks、受保护主线合入、新 exact-main Public CI / Browser Smoke，以及
针对本文合入坐标的 fresh anonymous installed-product readback。只有这些最后门全部成立，状态目标才成为
当前主线事实；在此以前，本分支文字不授权 post-admission audit 或任何后继实现。

## 2. 本次冻结的最小对象

本次只冻结以下 private、closed-fixture、non-published closure：

```text
exact owned QUALIFIED composition result
        ↓
deterministic application admission gate
        ↓
exact RelationSet 0.1 semantic membership
        ↓
same-ID provenance + conflict + reverse-run closure
        ↓
explicit admission witness
        ↓
copy-owned private admission state
        ↓
DerivationEvidence 0.2 public binding projection
```

application 必须重新验证 qualification、FactSet、observation domain、phase、outcome、candidate、source Fact、
conflict、provenance 与 reverse-run closure；它不能把 `QUALIFIED`、candidate presence、RelationSet shape、
caller witness 或 private state seal 单独当成 admission authority。Evidence projection 只能接受已经 admission 的
owned state，不能从 raw candidates、ProviderRuns、qualification digest 或 caller bytes 反向签发 witness。

`QUALIFIED / CONFLICTING` 可以形成保留全部 candidates/conflicts 的 RelationSet，但不会选择 winner，也不会
产生 Slice、Coverage、Attention 或 Verdict。RelationSet 0.1 semantic digest 可以在不同合法 attempts 间相同；
完整 RelationSet bytes、provenance、witness、Evidence 与 admission authority 必须逐次成立，不能按 semantic
digest 继承。

## 3. 实现因果链

合同冻结后的 exact source 为 `main@f307f2b5d3e2c04b263fdca24cd8bc521979c6bf`。实现链为：

```text
implementation head  = a454b0d4b7ea9b65c191d3849b73a89b817b7479
implementation merge = dc580e0a23d0141982f09f7c19bb55d61e9a30d8
implementation tree  = b89f4534c0c5cfe87b51ba2cf31f7268728d2dd9
```

[PR #174](https://github.com/NoctilumeDev/VeriTrail/pull/174) 原始 Public CI run
`35676753872` 为 `pull_request / attempt 1 / 11/11 SUCCESS`；没有 rerun 或后继 push。实现合入后的 exact-main
Public CI run `35677941414` 为 `push / attempt 1 / 11/11 SUCCESS`，Browser Smoke run `35677941420`
为 `push / attempt 1 / 1/1 SUCCESS`。

实现最终字节在 CPython 3.10.6/3.13.13 的 Review Attention full normal/`-O` 四格均为 `210/210`；
admission focused 四格均为 `15/15`，Schema/corpus focused 为 `12/12`。clean wheel
`veritrail_review_attention-0.1.0.dev0-py3-none-any.whl` 为 `124052` bytes，SHA-256 为：

```text
342a65a58757f564000f54cb69919b2e15edf1d2af6f05a480f11c48c1bd503a
```

十五份实现文件又在一个匿名 exact-SHA source identity session 中逐项满足 HTTP 200、final URL、远端 bytes、
SHA-256 与 Git blob identity；manifest 原始 canonical bytes 的 SHA-256 为：

```text
faf356c5fd15ccbc2d6788e8c274b922464108257775fd2edb6a1554959d1c9a
```

该 source readback 只证明公开 exact bytes 与 Git tree 一致；它不替代实现测试、package observation 或本文的
installed-product readback。

## 4. 实现候选的精确链

文档 186 的 docs-only candidate 链为：

```text
base    = dc580e0a23d0141982f09f7c19bb55d61e9a30d8
head    = f4cf6fd64f544b970d0b03a8b573432051f53087
merge   = bf1d94104283573394db76939051a06da972cd12
parents = dc580e0a23d0141982f09f7c19bb55d61e9a30d8
          f4cf6fd64f544b970d0b03a8b573432051f53087
tree    = a334ee8bcf37b48033197e1ffe0f47e4764edb37
```

[PR #175](https://github.com/NoctilumeDev/VeriTrail/pull/175) 的原始 Public CI run
`35680541051` 为 `pull_request / attempt 1 / 11/11 SUCCESS`；没有 rerun 或后继 push。候选以 ordinary merge
commit 合入受保护 main，candidate 与 merge tree 相同。新 exact main 的门为：

```text
Public CI      run 35681782493  push / attempt 1  11/11 SUCCESS
Browser Smoke run 35681782555  push / attempt 1   1/1 SUCCESS
```

文档 186 分支自身的 admission + boundary focused 回归在 CPython 3.10.6/3.13.13 normal/`-O` 四格均为
`24/24`；Schema/corpus/payload regression 在两套 Python 下均为 `31/31`，Markdown runtime regression 各为
`4/4`。静态门证明 exact 四文件范围、heading/link/fence/status marker、敏感与本机路径、架构资产连续性及
`git diff --check` 成立。这些本地门与远端门分别证明自己的执行拓扑，不互相冒充。

## 5. 候选 fresh anonymous installed-product readback

readback 从 exact `main@bf1d941...` 建立 detached source coordinate，并在 fresh CPython 3.13 venv 中只安装固定
Core 0.13.0 与 GitHub Evidence 0.1.0 wheel，再显式加入 Playwright 1.62.0 与 matching Chromium。wheel
SHA-256 为：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

清空 GitHub token 环境并显式使用 `127.0.0.1:7897` 代理后，针对 exact `bf1d941...` 建立三个不同 Plan ID、
Plan digest、collection session 与 output root 的 `P1 API -> P2 Render -> P3 handoff -> Core` session：

| Target | Plan ID | Session | Plan digest | Handoff | Report |
| --- | --- | --- | --- | --- | --- |
| README | `r1-admission-implementation-candidate-readback-readme` | `github-paired-8db5d7d152234feb93a0da2ee8bfa018` | `9c82bc424fbfbc8dd5bdd3f2a34bf1cef7bcf8ccc862bed671a486f749a3af16` | `d1ac43ccdfef759e73415da8b66238dd06d04f3e20ba0dd3b6556fefc1ac2ef4` | `5cd7e31e83d1bf9264e9d392d9d4ff39a53e595b576352443e45f77d413904d8` |
| Document 186 | `r1-admission-implementation-candidate-readback-doc186` | `github-paired-34c2f1206afe4330b1eb7438e39d0423` | `345278e3ea2c41138509b8297c8315a16ab21fb530fc5aad19187426f9e30589` | `900cecd120864c3b079b4af600ad132bdf1ba42e4cc1d39cc4090687fe5891f2` | `8096bd4e1adf39ee9d395b91c6f9678b47809afae84f5f304a5beef2745d9b38` |
| Milestones | `r1-admission-implementation-candidate-readback-milestones` | `github-paired-6d29597f174e4c25a98aabcb2d05cf59` | `f567b4e0788cf150eb0b6fd13ed3049aaee73251fb84561eff4c7a775bc1ebd2` | `18ec74882cb9ac0ae39b192b673cb38e6fb89edf227abf793d95a387d9bc5389` | `35a0adde3538dae593ebd1e30f55abf0715641eedacd0e618d772f83dd0154cc` |

三次均为 HTTP 200、requested/final exact-SHA path 相同、P1/P2 coverage `COMPLETE`、唯一固定作用域、三个
样本稳定、marker 恰好一次、零 conflict/error/coverage reason/cleanup error、零 active stream，Core `PASS`。

联合 verifier 逐项复算 sealed Plan、API/Render Evidence、handoff、report、summary、response byte accounting、
匿名访问模式、Git merge/tree/四文件 scope、公开 wheel identity、implementation source manifest 与三组 identity
不复用。三个 canonical summary 按 README、文档 186、milestones 顺序连接后的 SHA-256 为：

```text
02b1ee821cb16682021bbe376ed92f5bb770f629fc2d54d8115fc87f53dc7710
```

canonical manifest `sha256_json` 为：

```text
dfb4d386143a96df3071d8a2e4fa37e0ad69ba9d42a2783454619578b8bfddf9
```

## 6. 保留的 harness / setup 事实

fresh venv 第一次只安装两个公开 wheel 后，预检发现 Playwright package 不存在。两个 wheel 已正确从 fresh
`site-packages` 导入，但浏览器能力尚未完成安装；此时没有 Plan、collection session、Evidence、acceptance
bundle 或 output root，因此它是 environment setup failure，不是正式 readback 首败。后继显式安装冻结的
Playwright 1.62.0 与 matching Chromium 后才开始 README attempt。

三份 readback 全部完成后，联合 verifier 第一次运行在写 manifest 以前停止，因为它错误要求旧 implementation
source manifest 使用 `canonical_json_bytes + LF`。该历史文件实际是无尾随 LF 的 canonical bytes，其原始
SHA-256 与 `sha256_json` 均为 `faf356c...`。verifier 只把历史格式检查修正为 exact canonical bytes；三份 Plan、
session、Evidence、report、summary 与 output root 均未重跑或修改，随后独立复算并生成上述 manifest。

## 7. 已冻结不变量与未授权能力

本次冻结以下边界：

1. qualification、RelationSet semantics、provenance bytes、admission authority 与 public carrier 是不同身份；
2. admission 只接受 exact owned `QUALIFIED` result，并重验完整 membership、source Fact、conflict、provenance 与
   reverse-run closure；
3. RelationSet 不能自报 admission，Evidence 不能生成 admission，Manifest 不能裁决 admission；
4. explicit witness 必须绑定 exact qualification、FactSet、observation domain、admitted semantic RelationSet、
   full RelationSet artifact 与 execution/provenance closure；
5. `QUALIFIED / CONFLICTING` 可以被 admission，但 conflict 不被解析、降权或选出 winner；
6. private construction token 与 state seal 只保护 owned object integrity，不取得 admission authority；
7. Evidence 0.2 的 `COMPLETED -> non-null relation_admission` 只属于当前 frozen closed profile，不外推为所有未来
   R runtime 的普遍规则。

本次没有冻结、实现或授权 publisher、Artifact reservation、公共 Bundle 写入、第九 Manifest role、完整 import
resolution、public Provider SPI、ReviewSliceSet、CoverageLedger、Attention Proposal、CLI、Workbench、Core
新判断、Q runtime、D、Cu、O、T、tag 或 Release。

## 8. 下一停止线

本文最后门全部成立后，唯一合法下一步是从新的 exact main 做 post-admission system audit。审计必须先读取内部
Evidence、仓库历史与本地 falsifier，再判断 frozen admission closure 实际暴露了什么缝隙；不得因为路线图上写有
RelationSet、Slice 或 Coverage 就机械开工。

只有内部审计出现具体经验缺口时，才按 failure family 选择性查询外部生产案例。公开案例只能产生 hypothesis，
必须再由本地 falsifier 打穿后才可能影响下一合同；它不能直接成为施工授权。

## 9. 本状态发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。提交前必须通过
适用的 admission + boundary 双 Python normal/`-O` 回归、Schema/corpus/payload 回归、Markdown relative
links、fence/heading、状态 marker、敏感模式、本机路径、architecture byte continuity、exact diff scope 与
`git diff --check`。这些本地结果不替代本文自己的远端 required checks。

本 publication worktree 在同一最终字节上串行运行
`test_relation_set_admission + test_boundaries`：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `24 tests / 33.579s / OK` |
| CPython 3.10.6 `-O` | `24 tests / 34.025s / OK` |
| CPython 3.13.13 normal | `24 tests / 33.341s / OK` |
| CPython 3.13.13 `-O` | `24 tests / 32.038s / OK` |

Evidence 0.2 Schema/corpus 与既有 R1 payload regression 在 CPython 3.10.6/3.13.13 normal 下分别为
`31 tests / 0.723s / OK` 与 `31 tests / 0.371s / OK`；Markdown runtime regression 在两套解释器下各为
`4/4`。四个 focused runtime 门严格串行，未用并发负载改变 Windows deadline、terminal、release 或 cleanup
观察窗口。

最终静态门逐项读取四个 docs-only 文件，检查 412 个 relative links 且零断链；fence 平衡、heading 无重复、
四个展示文件均包含目标 frozen marker、无 tab、无本机绝对路径或敏感 token-like value。exact diff scope、
`git diff --check` 与 architecture DOT/SVG byte continuity 均成立；本轮没有拓扑变化，因此不重绘图片或修改
能力地图。

最终状态只在以下链条完整成立后生效：

```text
本文原始 required checks 全部成功
    -> exact head 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN
```

任一新反例都可否决冻结或只重开被击穿的最小边界。不得用 PR #174、PR #175、candidate exact-main 门或
candidate readback 替代本文自己的最后门，也不得因为本文是 docs-only 就跳过完整门禁。
