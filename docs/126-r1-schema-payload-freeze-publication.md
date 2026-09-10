# Review Attention R1 Schema payload 冻结发布

## 1. 文档身份

> 状态目标：`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_FROZEN /
> R1_IMPLEMENTATION_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[文档 125](125-r1-schema-payload-freeze-candidate.md)
>
> payload 合入基线：`main@4a25ef3d4009395f3510e847909f1efbaa29c5ac`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文发布 R1 Schema payload 已经完成候选原始门禁、受保护主线合入、exact-main 门禁、匿名原始字节
读回和已发布产品链读回的事实。本文不修改十个 Schema、compatibility corpus、identity vectors、
conformance tests、Core、P/Q 合同或任何运行语义，也不创建 R1 importer、Git reader、Python parser、
Fact/Relation/Slice/Coverage producer、CLI、Provider、标签或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有最后门全部
成立，状态目标才成为当前主线事实；在此之前不能把本文分支或候选文字当成运行实现授权。

## 2. payload 候选与受保护主线

payload 从精确 `main@4ef8b6434597b6557d6306100b91aebd9c1b3ecd` 建立，最终候选提交为：

```text
88ece8443904c83cc74b6ee3608d84e03e4951af
```

[PR #105 `feat(review): add R1 schema payload candidate`](https://github.com/NoctilumeDev/VeriTrail/pull/105)
的原始 [Public CI run 34510523050](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34510523050)
在 attempt 1 取得 `11/11 SUCCESS`。PR 随后于 `2026-09-10T17:59:38Z` 通过受保护主线合入：

```text
merge commit:
4a25ef3d4009395f3510e847909f1efbaa29c5ac

tree:
c4d88a4ad81c9dde877c3dc7be178aeeec7f6c25

parents:
4ef8b6434597b6557d6306100b91aebd9c1b3ecd
88ece8443904c83cc74b6ee3608d84e03e4951af
```

候选只新增十个公共 JSON Schema、十九个 corpus 文件、Schema/conformance tests 与候选说明，并只将
`jsonschema==4.25.1` 加入测试 extra 和 Public CI 的测试安装。Core base wheel 没有获得该运行依赖。
并行 Dependabot PR #16/#67 未被合入、关闭或带入候选因果链。

## 3. exact-main 门禁

候选合入后只接受精确 `main@4a25ef3d4009395f3510e847909f1efbaa29c5ac` 上由 push 事件创建的
原始运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34511582632](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34511582632) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34511582729](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34511582729) | 1 | `1/1 SUCCESS` |

Public CI 在 `2026-09-10T18:09:57Z` 完成，Browser Smoke 在 `2026-09-10T18:00:46Z` 完成。没有失败
job 被 rerun 覆盖，也没有用 PR head、本地矩阵或旧 main 替代合入后的主线事实。

## 4. 匿名逐字节读回

在未提供 GitHub token 的环境中，读回程序从 `raw.githubusercontent.com` 的 exact commit 坐标读取全部
十个 Schema 与十九个 corpus 文件，并与合入候选逐字节比较。二十九项全部相等；下面的 byte length 与
SHA-256 同时绑定公开字节：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `schemas/review-coverage-ledger-0.1.schema.json` | 11623 | `e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545` |
| `schemas/review-derivation-evidence-0.1.schema.json` | 6756 | `2efbd1d4f73f20fb045c2110136e7f3089e07408b9d496f59c30492a2c3666e7` |
| `schemas/review-derivation-manifest-0.1.schema.json` | 4659 | `69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91` |
| `schemas/review-derivation-profile-0.1.schema.json` | 2983 | `cd2995c30ce2529ae60a2673c366411d91cb08e0753a6a19a89f74cca6159dce` |
| `schemas/review-fact-set-0.1.schema.json` | 7681 | `e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1` |
| `schemas/review-policy-0.1.schema.json` | 5776 | `101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f` |
| `schemas/review-r1-common-0.1.schema.json` | 5283 | `e36f0d4ba494645bc991736b780c2c5354be13789466ab82d72b4963c674da4a` |
| `schemas/review-relation-set-0.1.schema.json` | 6232 | `397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744` |
| `schemas/review-slice-set-0.1.schema.json` | 4476 | `7d9eaba8978776d679e785ed3246a155bd7f78e3f5442219879fb3f80d80b851` |
| `schemas/review-source-snapshot-0.1.schema.json` | 6241 | `f806e52d1f38d850003a85644d1380c00c8129a76720b9d4e96310d06a236518` |
| `tests/fixtures/review-r1-schema-0.1/README.md` | 1106 | `3990bc0664461d049e5684dee8b32c1342901d4fafbb345aa8d7c802fd968e89` |
| `tests/fixtures/review-r1-schema-0.1/compatibility-cases.json` | 7023 | `5cb46458ddf23673fcf0a2fef197637074e7dda16a538bace0b4d95b5d1bb696` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-00-07.json` | 15204 | `00b0cdfaf2754da5bed506fd215d52e27f3a8a1bfbd6cc0811d85208b7effca8` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-08-14.json` | 13214 | `c4acb39a568b50c49b2910b68a2815afd0f7a5eecdb6980ac71baf9bb16def42` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-15-22.json` | 20918 | `d23078ad43183bc237f0c4b8a5a77f4fb2ef870d94498b08c7878b9e0b81940b` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-23-29.json` | 5910 | `9d3712f44a074fdb9b6570e096aac035afcc0e987c394ca924a74c2645a1e2d5` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-30.json` | 18199 | `4449f0b43ec38ca3abfcdfbe8b6969c5b7e265fbfabc471356a97a16aa194e34` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-31.json` | 5741 | `a5f66942a218870d7b4a236244e768ae234a00c5b3cb4c1c1ae3810395cecd48` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/identity-vectors-conflicts.json` | 2293 | `664469a017a128b1a6a24c13c0a83227b89070456cc50cdbf2b467d691b58fef` |
| `tests/fixtures/review-r1-schema-0.1/identity-vectors/raw-sha256-vectors.json` | 4683 | `bfebba3823d4afbaa1d1805ad9f25109787c4352b212d877f49b0e072d0320a1` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/coverage-ledger.json` | 6013 | `256b529b0aaf1405c5020c5f3ffc5296ca769d95c1d6c85854369e79edae3a0a` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-evidence.json` | 1859 | `563664e5675cb861c7c22d4017c97d186a7e370bca4851dbf7bb09df49afb555` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/derivation-profile.json` | 971 | `29ed3bed4caf4bd2d7dbae0d54166796fac2148eb483067809700aa953df95e2` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/fact-set.json` | 2042 | `63c77b77b31eb4e4f127f8bd5eeb77a4aa50d4791f556f1f325da9c32fb355e5` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/manifest.json` | 2018 | `ddccc2f4ed298f93c242a7004d361ca9af2d81574350a4035684aeb29bf2efe1` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/relation-set.json` | 1959 | `739e2f1eac4844346779a0953add1c1e09b3adcefbacd657c8716d89f00ab67c` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/review-policy.json` | 1581 | `b97bbbb7b41addcaf728fb5361aab33d9e801661f7c50c6a07c6228ae8872bc2` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/review-slices.json` | 2207 | `81e1aa631a9817c56b57dfe24a9a4ce8d38e11080fa4d6cc6e85f6825f9cb4a4` |
| `tests/fixtures/review-r1-schema-0.1/valid-complete/source-snapshot.json` | 1187 | `ef07cdd90aa89dc630e9d21f7cc18ed65888f0a989b8b06eb61cbdda25045fce` |

按 Git path 排序后连接上述二十九个小写 SHA-256 文本并再次计算 SHA-256，得到：

```text
afd3fcca87e873a4a797ff8fd8ffd053d826969202a2ec1da643882e339a8796
```

该摘要只是一项读回汇总，不替代每个文件自己的字节身份，也不写入任何自指 payload。

## 5. 已发布产品链读回

公开读回使用隔离 CPython 3.13 环境；Core 与 GitHub Evidence Plugin 均直接安装自公开 Release URL，
`direct_url.json` 记录的摘要为：

| Component | Version | Public wheel SHA-256 |
| --- | --- | --- |
| VeriTrail Core | `0.13.0` | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence Plugin | `0.1.0` | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

浏览器能力为 Playwright `1.62.0` 与 matching Chromium。环境未提供 `GITHUB_TOKEN`、`GH_TOKEN`、
`VERITRAIL_GITHUB_TOKEN` 或源码 `PYTHONPATH`。每个页面使用独立 sealed Plan 与独立 paired session，
固定执行 `github-api -> github-public-render -> exact snapshot handoff -> Acceptance Core`：

| Target | Viewport | Plan digest | Session | Evidence SHA-256（API / Render） | Core report digest |
| --- | --- | --- | --- | --- | --- |
| `README.md` | desktop | `9cef10f45f94bb4a2c205d5b387f7b723796e3bd2c9c02ee787b3d13f300f7e3` | `github-paired-81ffe6ead87442489be3bb4407f06d18` | `390db19a0f36a02c91136645a1b7c18e61d1af65427267603307bbcb17953040` / `172f29fe8f8168badae1c250dfb19629e0f07c760f4b19a75fd037b52477639f` | `04c865a27028daf58cc24597bbd178facb2e31c86e8670015e9566a2ce012555` |
| `docs/125-r1-schema-payload-freeze-candidate.md` | narrow | `9f3c5b895d2edd5ccb30379019944e9e35e5ed5c64a8f355cc0e20ea63af3e44` | `github-paired-325e0b61d86e4303904fa94d8c0f743d` | `f036815fae6302cf9236678afeb6badeed7c09053503ed3da57374abf11aeaca` / `485bef5c022c7eab9c7dde5c5851e2ad8e525369a5f28524cdfb89c2e7fb5bf4` | `8b8bc40873453e34823bf7c448796175d770d8efa55707075e7297b26d04ab93` |

两次读回均取得 `PUBLISHED / COMPLETE / PASS`。requested URL 与 final URL 保持 exact SHA 和同一路径；
HTTP 为 200，scope 唯一可用，三个规范化样本一致，active stream 为零，且
`errors / conflicts / cleanup_errors / coverage_reasons` 均为空。规范 summary digest 为：

```text
1513f6b4df79116cc1eb75243ed44fc725cdc10c6cbda883db84e427cf206a93
```

两个 pair 属于同一 GitHub trust domain，但 session 相互独立；每个 pair 内严格串行且不是 GitHub 原子
快照。这些事实证明公开坐标与声明可被产品链观察，不证明 GitHub 之外的来源真实性。

## 6. 保留的候选证据边界

文档 125 保留 payload 本地施工的完整事实：focused 22 项、Core 441 项、GitHub Evidence 180 项、
Authoring Skill 24 项均在 Python 3.10/3.13 的 normal/`-O` 四矩阵通过；Workbench 173 项、lint、type-check、
production build 与 audit 通过；Core base wheel 的 clean environment 不包含 `jsonschema`。

第一次最终 Core 矩阵曾因宿主机接近 M10 资源停止线而在三条真实 Chromium 用例得到
`RESOURCE_MEMORY_SOFT_LIMIT`。该事实没有被后续绿灯删除或改名；关闭用户 Browser 与腾讯视频、恢复可用
内存后，候选从第一项重跑完整 441 项四矩阵并全部通过。冻结对象因此仍受已声明宿主资源边界约束，
不能把环境停止写成 payload 正确或错误。

## 7. 冻结对象与运行入口

本状态发布冻结的是可寻址、可复算的 R1 Schema payload 0.1：

```text
ten Draft 2020-12 schemas
nineteen data-only corpus files
twenty compatibility obligations
twenty-four semantic identity domains / thirty-four vectors
one raw SHA-256 vector
one nine-file synthetic COMPLETE bundle
test-only jsonschema dependency boundary
```

JSON Schema 只证明局部结构；conformance tests 继续负责跨对象、身份投影、排序、预算、Coverage 方程与
Manifest 绑定。`Schema-valid != R1-conformant != repository understood` 仍是冻结边界。

最后门成立后，`R1_IMPLEMENTATION_ENTRY_UNBLOCKED` 只允许从新的 exact main 建立独立运行实现合同或
首个最小纵向切片：

```text
exact Git commit / tree / analysis root
        -> one bounded safe read
        -> owned SourceSnapshot bytes
        -> frozen Schema + conformance validation
        -> create-new immutable output
```

它不表示运行实现已经开始，也不允许一次性扩张到 Python Facts、Relations、Slices、Coverage、AI proposal、
ranking、HumanDisposition、Core Verdict、Q scheduling、标签或 Release。新实现不得与本状态发布共用分支，
必须重新接受自己的合同、反例和证据门。

## 8. 本状态发布的最后门

本补丁只能更新本文、README、AGENTS、R 轨 Plan、能力地图、候选后继指针与 milestones，并必须独立完成：

1. docs-only scope、Markdown links、敏感信息与 `git diff --check`；
2. 双 Python 3.10/3.13 的 normal/`-O` 完整本地门禁；
3. 原始远端 Public CI 11/11 成功，不以 rerun 覆盖失败；
4. 通过受保护主线合入；
5. 新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1 在 attempt 1 成功；
6. 从新 exact main 使用公开产品链 fresh anonymous 读取 README、本文和 milestones，取得
   `PUBLISHED / COMPLETE / PASS`；
7. 确认十个 Schema、十九个 corpus 文件及其摘要未漂移，且仓库仍无 R1 runtime、CLI、Provider、标签或
   Release。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_IMPLEMENTATION_ENTRY_UNBLOCKED
R1_IMPLEMENTATION_NOT_STARTED
```

任一新反例仍可否决本次状态发布。后继不得从 payload 候选分支续写，也不得把本文记录的候选绿灯继承为
运行实现证据；必须从本发布完成读回后的新 exact main 建立新的单一意图坐标。
