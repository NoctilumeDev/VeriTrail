# R1 RelationSet Admission / Public Qualification Binding 实现冻结候选

## 1. 当前裁决

> 状态：`R1_RELATION_DERIVATION_FROZEN /
> R1_RELATION_OBSERVATION_COMPOSITION_QUALIFICATION_FROZEN /
> R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_FROZEN /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_IMPLEMENTED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FREEZE_CANDIDATE /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同：[文档 183](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
>
> 合同冻结发布：[文档 185](185-r1-relation-set-admission-and-public-qualification-binding-contract-freeze-publication.md)
>
> 实现 PR：[#174](https://github.com/NoctilumeDev/VeriTrail/pull/174)
>
> 实现 exact main：`dc580e0a23d0141982f09f7c19bb55d61e9a30d8`

文档 183 第 11 节 A–F 已在 private closed proof 中物化。deterministic application 从一个已经成立的
`OwnedRelationCompositionQualificationResult` 重新复核 qualification、FactSet、observation domain、phase、
outcome、candidate、conflict、provenance 与 reverse-run closure，再形成 exact `RelationSet 0.1`、explicit
admission witness 与 copy-owned private admission state。Evidence 0.2 projection 只接受这份已经 admission 的
state，不能从 raw candidates、ProviderRuns、RelationSet presence 或 caller-supplied witness 反向签发资格。

该实现没有创建 publisher、output coordinate、artifact reservation、八文件 Bundle、第九 Manifest role、Slice、
Coverage、Attention、CLI 或 Workbench，也没有修改 Core、GitHub Evidence、Q、D、Cu、O 或 T。本文只记录实现
事实与冻结候选资格；本文自己的远端门、受保护主线合入、新 exact-main 双门、fresh anonymous
installed-product readback 与后继独立最终状态发布全部成立前，不得写成
`R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN`。

## 2. 实现边界与 source state

实现从合同冻结后的 exact `main@f307f2b5d3e2c04b263fdca24cd8bc521979c6bf` 建立，最终候选为：

```text
implementation head  = a454b0d4b7ea9b65c191d3849b73a89b817b7479
implementation merge = dc580e0a23d0141982f09f7c19bb55d61e9a30d8
implementation tree  = b89f4534c0c5cfe87b51ba2cf31f7268728d2dd9
merge parents         = f307f2b5d3e2c04b263fdca24cd8bc521979c6bf
                        a454b0d4b7ea9b65c191d3849b73a89b817b7479
```

candidate 与 merge tree 相同。实现变更严格限于十五份文件、`3953 insertions / 1 deletion`：

```text
plugins/review-attention/src/veritrail_review/
  _relation_set_admission.py
  _relation_set_admission_values.py

plugins/review-attention/tests/
  test_boundaries.py
  test_relation_set_admission.py

schemas/
  review-derivation-evidence-0.2.schema.json

tests/fixtures/review-r1-derivation-evidence-0.2/
  README.md
  compatibility-cases.json
  identity-vectors.json
  valid-consistent/derivation-evidence.json
  valid-consistent/relation-set.json
  valid-conflicting/derivation-evidence.json
  valid-conflicting/relation-set.json
  valid-interrupted-null/derivation-evidence.json

tests/
  test_review_r1_admission_evidence_schema.py
  test_review_r1_schema_payload.py
```

两个 runtime module 保持 private，顶层 `veritrail_review` 没有新增 admission/projection export。boundary test
继续禁止 private admission module 导入 publisher、Artifact budget 或 `ast`。`RelationSet 0.1`、Manifest 0.1、
DerivationEvidence 0.1/0.1.1 与既有 corpus/vector 没有原位改写。

## 3. Admission gate 与 exact RelationSet

唯一 admission 入口为：

```text
admit_relation_set_for_private_closed_proof(
    OwnedRelationCompositionQualificationResult
)
    -> OwnedRelationSetAdmissionState
```

入口不接收 raw candidates、caller-created witness、path、Provider registry 或 ambient discovery。它逐项重新验证：

- `qualification_status=QUALIFIED`、required source/observation closure 为 `COMPLETE`、reason codes 为空；
- exact FactSet、observation domain、Fact/Relation phase 与各 ProviderRun terminal/release 仍闭合；
- observation outcome、candidate、merged candidate、conflict 与 provider-reported IDs 双向一致；
- qualification digest、candidate identity、RelationSet digest 与 admission witness digest 各按自己的 domain 复算；
- import-literal target 的 `relative_level`、`module_parts`、`imported_name`、`UNRESOLVED`、`UNKNOWN` 与空
  `resolved_fact_ids` 和 exact source Fact attributes 一致。

最后一项不是继续相信 qualification 的历史结果。实现期复核构造了一份内部 digest 全部重新闭合、但 import
target 与 source Fact 不一致的伪造 qualification；admission 必须独立拒绝它。输入不支持时整体 fail closed，
不能通过缩小成员、删除 conflict、换 provenance 或选择 winner 获得 admission。

`QUALIFIED / CONFLICTING` 可以形成 admitted RelationSet，但必须保存所有 incompatible candidates 与 exact
conflict records，不得选择 winner，也不得生成空 Slice 或 `UNKNOWN` Coverage。`QUALIFIED`、conflict-free、
RelationSet admission、Slice eligibility 与 final publication 继续是不同状态。

## 4. Explicit witness 与 private state integrity

application 从 exact admission history 形成 witness。witness 绑定完整 observation domain、qualification claim、
ProviderRun terminals/receipts、exact admitted Relation/conflict IDs、RelationSet digest 与 attempt-specific admission
witness digest；它不声明 Relation 是现实真相，也不取得 Slice、Coverage 或 Verdict authority。

private admission state 同时使用三类独立检查：

```text
construction token
  -> 证明对象来自 application-owned constructor

private state seal
  -> 检测构造后的 owned-state 静默变更

public digest and closure recomputation
  -> 证明当前 semantic projection 与 admission contract 相符
```

实现期测试曾证明，只有 construction token 不能阻止 dataclass replacement 改写 Relation target、provenance 或
witness claim，因此加入 `_state_seal` 与独立重算。seal 只证明内部对象完整性，不能替代 qualification、
RelationSet、witness 与 reverse-run conformance，也不能逐渐变成新的 admission authority。

两个独立合法 attempts 可以共享 `relation_set_digest`，但完整 RelationSet bytes、provenance、witness 与 Evidence
必须各自成立。相同 semantic digest 只允许说明 semantic content identity 相同，不授权复用另一次 attempt 的
`relation-set.json` bytes。

## 5. Evidence 0.2 carrier 与 projection boundary

private projection 入口为：

```text
project_private_derivation_evidence_0_2(
    admitted: OwnedRelationSetAdmissionState
)
```

该入口只能序列化已经建立的 witness；没有从 raw candidates、qualification digest、ProviderRuns 或 caller bytes
构造 witness 的参数。projection 再验证 private seal、RelationSet/witness/qualification digest 与 cross-object
closure，然后新建 Evidence 0.2 document。它没有写文件、分配 Artifact budget 或修改 Manifest。

新增的 `review-derivation-evidence-0.2.schema.json` 以冻结 0.1.1 shape 为基线，增加 required
`relation_admission` 与新的 `veritrail.review.derivation-evidence/0.2` identity domain。当前 closed
admission-capable profile 的规则是：

```text
COMPLETED
  -> conformant non-null relation_admission

INTERRUPTED / FAILED / UNAVAILABLE
  -> relation_admission = null
  -> final reported Fact/Relation IDs empty
```

这不是所有未来 R runtime 的普遍定义。若以后出现合法 `COMPLETED` 但 Relation phase 不适用的 profile，必须
以新 version/profile 反例重新审计，不能把本次 closed slice 的条件外推。

独立 corpus 包含 consistent、conflicting 与 interrupted-null 三个正向世界，以及 historical-version、缺 witness、
witness/member/provenance/receipt/digest 漂移、identity cycle 与 Manifest ninth-file shortcut 等负向世界。
RelationSet 0.1 自报 `admission_status` 仍被 closed Schema 拒绝；Manifest 0.1 继续只是八/四文件 binder。

## 6. `RAE-000..017` 与实现期纠偏

十五个 focused test method 覆盖合同 `RAE-000..017`。本轮关键反例包括：

- 非 `QUALIFIED` history 即使 raw candidate projection 相同，也不能形成 RelationSet/witness；
- candidate member 少/多、错误 provenance、dangling reverse-run 或 conflict winner selection 均 reject；
- caller 无法把 witness bytes 直接送入 Evidence projection；
- H1 witness 复制到同 semantic H2 时，run/qualification/provenance closure reject；
- receipt/outcome 修改后只重算外层 Evidence digest 仍 reject；
- historical Evidence 0.1/0.1.1 不能冒充 admission-capable 0.2；
- Manifest 正确绑定 bytes 也不能补一个无效 witness 的 eligibility。

实现期审计还修正了四个未进入最终候选的不足：最初 fact validation 未覆盖全部冻结字段；token-only state 可被
replace 后继续投影；Schema 中空 `reason_codes` 缺少 `items: false`；responsibility order 没有按 descriptor rank
固定。后继 import target source-Fact falsifier又暴露 admission 重验不够深，最终实现已加入第 3 节的 exact
semantic match。这些纠偏不能被描述成“第一次设计就已经具备”。

第一次本地 wheel 命令使用 `python -m build`，在 build module 不存在时停止；它没有执行 package build。
后继 `pip wheel --no-deps` 才形成 clean wheel。另一次手写 unittest method 名错误在 loader 阶段停止，也没有
形成目标测试 observation。这两项属于 local tooling/gate setup failure，不是 runtime 反证，且不被后继绿色
改写为已执行。

## 7. 本地与 package 证据

实现最终字节在 CPython 3.10.6/3.13.13 上完成 full Review Attention normal/`-O` 四格：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `210 tests / 466.167s / OK` |
| CPython 3.10.6 `-O` | `210 tests / 466.205s / OK` |
| CPython 3.13.13 normal | `210 tests / 460.968s / OK` |
| CPython 3.13.13 `-O` | `210 tests / 461.374s / OK` |

admission focused regression 在同一四格均为 `15/15`；Schema/corpus focused regression 为 `12/12`。两套
解释器 `py_compile`、runtime-generated Evidence 0.2 / RelationSet 0.1 Schema validation、敏感/本机路径扫描与
`git diff --check` 均成立。

CPython 3.13 的 clean wheel 为：

```text
name   = veritrail_review_attention-0.1.0.dev0-py3-none-any.whl
bytes  = 124052
sha256 = 342a65a58757f564000f54cb69919b2e15edf1d2af6f05a480f11c48c1bd503a
```

wheel 包含两个 private admission module。candidate 与 merge tree 都是
`b89f4534c0c5cfe87b51ba2cf31f7268728d2dd9`；exact-main Public CI 又在 checkout/install topology 中完成双
Python Review Attention normal/`-O` 与后继 wheel-only/acceptance gates。本地 wheel 身份和远端安装门仍是两种
不同观察，不互相冒充。

固定 identity vectors 为：

```text
relation_set_digest      = 9be261a89ffa32d328357590567cdc1050b9158979b81f2a24f2c3fe6c5c4749
admission_witness_digest = 029865c7abb407a6c6eb147892ce686bcc1d085cdd6c4b9d4a430bec100b3bc3
RelationSet artifact SHA = 8ee1ab118ac2add04e9ce8e55cb1f070df0ad3f8f6cec2a22a9c64a7f3a080d1
```

## 8. 远端实现因果链

PR #174 original head `a454b0d4b7ea9b65c191d3849b73a89b817b7479` 的 Public CI
[run 35676753872](https://github.com/NoctilumeDev/VeriTrail/actions/runs/35676753872) 为
`pull_request / attempt 1 / 11/11 SUCCESS`。没有 rerun 或后继 push。候选随后以普通 merge commit 合入受保护
`main@dc580e0a23d0141982f09f7c19bb55d61e9a30d8`，merge tree 与 candidate tree 相同。

该 exact main 的新门为：

```text
Public CI      run 35677941414  push / attempt 1  11/11 SUCCESS
Browser Smoke run 35677941420  push / attempt 1   1/1 SUCCESS
```

Public CI 两条 Windows 主车道都完成 Review Attention normal/`-O`、package build 与后继 installed/acceptance
gates；11 个 jobs 全部成功。上述绿色证明 exact source state 在声明的门禁中成立，不把本地 setup failure 改写成
产品失败或成功。

## 9. Anonymous exact-SHA source identity readback

清空 GitHub token 环境并显式使用 `127.0.0.1:7897` 代理后，从 `raw.githubusercontent.com` 匿名读取 exact
`dc580e0a...` 的全部十五份实现变更文件。一次正式 session 中，15/15 请求均为 HTTP 200，final URL 与
requested exact-SHA URL 相同；远端 bytes、SHA-256 与 exact merge tree 相等，重新计算的 Git blob SHA-1 也逐项
匹配。

| Path | Bytes | SHA-256 | Git blob |
| --- | ---: | --- | --- |
| `plugins/review-attention/src/veritrail_review/_relation_set_admission.py` | 41048 | `27f33608c6db8725b1c1100154689e75f2b8a04ebde5b1ec2c4de1f382040398` | `0b882070542e89c4a88ed1a54fab4c9b81c89845` |
| `plugins/review-attention/src/veritrail_review/_relation_set_admission_values.py` | 3252 | `b6f71378990f43164205050b4005fb39d463d716bdad6991ae3a8de3a9ece269` | `a83d3aae5f410d44dc9f57f31a91064df04ffb40` |
| `plugins/review-attention/tests/test_boundaries.py` | 12005 | `1c1082b29ec5aa4488334bd01865014bdf6c64711935a94924fd149957b54df3` | `72fa8a84e5f98a93341e4facfb25c5501de5915b` |
| `plugins/review-attention/tests/test_relation_set_admission.py` | 15441 | `2d9c7f1ef72ae7aec492998088472c92c8d871f2507dd76e2cbba95a06070a11` | `dff7c2d8d31cf02c4d35ccd13a023f41929524cc` |
| `schemas/review-derivation-evidence-0.2.schema.json` | 27193 | `66190e12fad8c3bbec3615c25b1bbaf3cfb1ef723267e0e99185dcf05b8238e6` | `dcd72d3f0c6738b9105e84aa3cf70eaad2b83d5f` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/README.md` | 881 | `83883e148ad59c3f00ea2448c999ff73df563d34bfab85fab4083d9b74cf3fc9` | `3fdb414251ab172f80e797d524fe0c5f51e3840e` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/compatibility-cases.json` | 1961 | `74bbab0ac14c26f42fbc17e3d076b3879091dd48c70a72f01f50e7b25f5116c2` | `3e1ff57fa177acc323f0fe73c685742495cee372` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/identity-vectors.json` | 1250 | `dac497cda4e75eb3f205d96dedcd442c42e1c0aa84bd5452f9a3a3f288fa64ce` | `2b79c64e2c6f25c0b1c2fb5a3bf7c106be64d3bf` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/valid-conflicting/derivation-evidence.json` | 19105 | `0d9112707ea6b1db2d4328c6df4606f81fe5f615ccb610924f7822f5d3c04581` | `c05b0dc1c7845f61055b930096b5227c1d68ae9b` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/valid-conflicting/relation-set.json` | 5769 | `9e91a26446577f7803a12fb1b8c6a1a1d8f847624a4f57529f15f89dc1b6e6eb` | `d3cec863097ef3572632973830207fd7d5e24201` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/valid-consistent/derivation-evidence.json` | 14633 | `18a53834c3a7acf90ffe28319bafffada716e151ca8005a126073604f3227a52` | `d1e9251d58554dbf3303863181d77667f5c5c545` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/valid-consistent/relation-set.json` | 2346 | `b54bc9b3dbbe4eb9c4abe446df3e116eb23682436b5cf2cf219186bdadd07175` | `f1d5ebf4abdcc7b98e599de2f7417c1d8b7dd50c` |
| `tests/fixtures/review-r1-derivation-evidence-0.2/valid-interrupted-null/derivation-evidence.json` | 4219 | `752921fe52b23b436e2df58fada6c3fe09474b82171897e0844d81f0f9d69855` | `e1da7edaf8883c1c1292127720941a915f3b625a` |
| `tests/test_review_r1_admission_evidence_schema.py` | 17845 | `40ae75ccd79a07b6bbd1b5a15e47ceaa24462fc3af656a9628b9891572ca78e5` | `2b27414cf33a74b49ede520b285f219d73861405` |
| `tests/test_review_r1_schema_payload.py` | 47733 | `cbeaf4a87e116c266dec5dfdf4ecc56afc773ccbab1989423e957cc4f62b964e` | `7015a3c41784c327b74d38224d2160e462ef017e` |

canonical readback manifest 位于仓库外，SHA-256 为：

```text
faf356c5fd15ccbc2d6788e8c274b922464108257775fd2edb6a1554959d1c9a
```

该 readback 只证明公开 exact bytes 与 Git tree identity 一致；它不证明代码符合合同，也不替代 package 或
installed-product observation。

## 10. 展示面与历史 byte guard

本实现没有改变系统拓扑。`docs/assets/veritrail-architecture.dot`、对应 SVG、
[能力边界与系统认知地图](114-capability-boundary-and-system-map.md)、Manifest 0.1、RelationSet 0.1 与历史
Evidence 0.1/0.1.1 bytes 均不在十五文件 diff 中，因此不为状态文字重新绘图或改写旧 Artifact。README、
AGENTS 与 milestones 只把当前公开导航从 `IMPLEMENTATION_NOT_STARTED` 更新为
`IMPLEMENTED / FREEZE_CANDIDATE`；图中已有的 R/Coverage/authority 关系不因 private admission implementation
获得新权力。

## 11. 本候选自己的最后门

本文与状态入口完成后，当前仍只是 implementation freeze candidate。本文必须独立完成：

1. diff 只含 `AGENTS.md`、`README.md`、`docs/milestones.md` 与本文；
2. relative links、Markdown fence/heading、状态 marker、敏感/本机路径、生成物与 `git diff --check` 成立；
3. admission + boundary focused tests 在 CPython 3.10/3.13 normal/`-O` 下成立；
4. Schema/corpus/payload regression 在两套 Python 下成立；
5. 原始 PR required checks 全部成功；
6. 受保护主线合入且 merge parents/tree 可复核；
7. 新 exact-main Public CI 11/11 与 Browser Smoke 1/1 成功；
8. fresh anonymous installed-product readback 对 README、本文与 milestones 各自 Core PASS；
9. 后继独立状态发布完成自己的同等级门禁，才允许写
   `R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_FROZEN`。

任一门失败，必须保留失败事实并停止。不得 rerun 洗白、降低 test count、放宽 marker、继承 PR #174 或其
exact-main 绿色作为本文证据，也不得开始 publisher、公共 Bundle、Slice、Coverage、Attention、CLI 或
Workbench。

本 docs-only worktree 已在两套解释器上串行运行 admission + boundary focused 四格：

| 门 | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `24 tests / 30.563s / OK` |
| CPython 3.10.6 `-O` | `24 tests / 29.860s / OK` |
| CPython 3.13.13 normal | `24 tests / 30.539s / OK` |
| CPython 3.13.13 `-O` | `24 tests / 30.841s / OK` |

Evidence 0.2 Schema/corpus 与既有 R1 payload regression 在 CPython 3.10.6/3.13.13 normal 下分别为
`31 tests / 0.579s / OK` 与 `31 tests / 0.542s / OK`；Markdown runtime regression 在两套解释器下各为
`4/4`。静态门检查四文件 exact scope、49 个 headings、409 个 relative links、fence、tab、敏感/token-like
模式、本机绝对路径、四份 candidate marker、架构 DOT/SVG/map byte continuity 与 `git diff --check`，结果均
成立。这些本地门不替代本文自己的远端 required checks。

## 12. 下一门与 Fresh-Agent 交接

当前唯一合法动作是完成本文 docs-only candidate 的证据闭环。本文合入和 exact-main 门成立后，必须先对
README、本文与 milestones 建立三个互不复用的 fresh anonymous installed-product session；随后再从新的 exact
main 创建独立最终冻结发布。只有最终发布完成自己的门禁、合入、exact-main 双门与匿名读回以后，才允许重新做
post-admission system audit。

本文不预选下一条 R seam。ReviewSlice、Coverage、Attention、publisher 与完整公共 Bundle 都仍只是待审候选；
外部生产案例只有在内部审计出现具体经验缺口时才作为 hypothesis source 进入，不能从本实现候选自动产生施工
授权。
