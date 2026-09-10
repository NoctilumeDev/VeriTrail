# R1 Schema 与规范身份合同冻结发布

## 1. 文档身份

> 状态目标：`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 冻结对象：[文档 120](120-r1-schema-and-canonical-identity-contract.md)
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`
>
> 后继状态：payload preflight 在写入第一份 Schema 前发现新的 identity 反例，修正边界见
> [文档 123](123-r1-schema-payload-preflight-correction.md)，重新冻结发布见
> [文档 124](124-r1-schema-payload-preflight-refreeze-publication.md)。本文继续保存第一次冻结发布曾经成立的
> 历史事实，不把后继修正写回旧合同的起点。

本文外部绑定 R1 Schema 合同候选已经取得的仓库、门禁与匿名产品读回事实，并保留首次冻结发布被
既有 M10 测试夹具否决、独立修正后从新 exact main 重建发布的完整因果链。它不修改文档 120 在候选
时点记录的状态，也不创建 JSON Schema、兼容向量、源码包、CLI、Provider、运行 CI、标签或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、合入后 exact-main 门禁和三次 fresh anonymous 产品
读回；只有最后门全部成立，状态目标才成为当前主线事实。

## 2. 候选身份与受保护主线合入

候选从精确基线 `main@35774838b3e9aeb5f062cfb101e96d76cea0e8ac` 建立，形成两个职责连续但
身份独立的提交：

| 提交 | 作用 |
| --- | --- |
| `1d2ac0b2b021257b19d9df890ef8843265879d00` | 建立 Schema、规范字节、身份投影与兼容向量合同 |
| `73bb087f9e9ffd8bbfd769f854088057de3efd8d` | 收紧分析根、Coverage、policy identity、subject slot 与 module mapping 边界 |

[PR #99 `docs: define R1 schema identity contract`](https://github.com/NoctilumeDev/VeriTrail/pull/99)
的最终 head 为 `73bb087f9e9ffd8bbfd769f854088057de3efd8d`。最终候选的原始
[Public CI run 34467096319](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34467096319)
在 attempt 1 取得 `11/11 SUCCESS`，随后于 `2026-09-10T10:49:04Z` 通过受保护主线合入：

```text
merge commit:
49a2d69d44cca21024808fe5c298db8bac7f64c4

tree:
be425ec78f00ac3c8226afe24ecf0f9163188dbf

parents:
35774838b3e9aeb5f062cfb101e96d76cea0e8ac
73bb087f9e9ffd8bbfd769f854088057de3efd8d
```

首个提交触发的旧 head run 因第二个提交推送而被平台取消；它不属于最终候选证据，也没有被当作成功
运行复用。

## 3. 候选合入后的 exact-main 门禁

候选合入后只接受精确 `main@49a2d69d44cca21024808fe5c298db8bac7f64c4` 上由 push 事件创建的
原始运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34468036396`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34468036396) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34468036355`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34468036355) | 1 | `1/1 SUCCESS` |

Public CI 在 `2026-09-10T10:58:38Z` 完成，Browser Smoke 在 `2026-09-10T10:50:01Z` 完成。没有失败
job 被 rerun 覆盖，也没有用 PR head、旧 main 或本地四矩阵替代合入后的主线事实。

这些门禁证明候选合入后的仓库回归成立；它们不能替代匿名公开渲染，也不能把 docs-only 合同变成
运行能力。

## 4. 候选的匿名产品读回

候选读回从隔离 Python 3.13 环境执行。Core 与 GitHub Evidence Plugin 直接使用公开 Release 资产，
并绑定已发布摘要：

| 组件 | 版本 | 公开 wheel SHA-256 |
| --- | --- | --- |
| VeriTrail Core | `0.13.0` | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence Plugin | `0.1.0` | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

浏览器依赖为 Playwright `1.62.0` 与 matching Chromium。环境中没有提供 `GITHUB_TOKEN`、`GH_TOKEN`
或 `VERITRAIL_GITHUB_TOKEN`，`PYTHONPATH` 也没有指向源码 checkout。每一页使用独立 sealed Plan 和
独立 paired session，固定执行：

```text
github-api
-> github-public-render
-> exact snapshot handoff
-> Acceptance Core
```

三次读回均绑定 exact candidate merge commit，并分别取得 `PUBLISHED / COMPLETE / PASS`：

| Target | Viewport | Plan digest | Session | Evidence SHA-256（API / Render） | Core report digest |
| --- | --- | --- | --- | --- | --- |
| `README.md` | desktop | `b024f39bf8ff52bd94238c1e64261773baa8579263415920913ea4388290729f` | `github-paired-c7ceb98113e5432397b91bc2f8f80e82` | `d54c0e000107d4aec367c76e2641feb6870cbf8b7bf2abadb6de510bc0b80bad` / `5aba84f23677ba6f42dd8fd386ac438213b4ea03b77b99bbcbe4fb07c0b14922` | `fe16051ffe8a3e6006260e3f25563eb48173dc9201656b55b091abaf5bd414ec` |
| `docs/120-r1-schema-and-canonical-identity-contract.md` | narrow | `4a739b3d31fa66c77970f19060bb3e7846da50528df9ff2f637093760076173b` | `github-paired-e84b1b85c2e6496f9d1632cbc0c76adf` | `d9a03ad857e05840ae957f72fb0cf673ee7e8357a7054d867b7629ceb41af449` / `26a65a423058ba781c4b4af152723e45178986968274d6f0dbb463690662710c` | `e03a12c52bbd9d41250063ab76df74d15a49f86f7ddea4de19e4a18a742ecfdc` |
| `docs/milestones.md` | narrow | `b69472d73cea47a17be4731e192ace0651caae11af6ac5c5b76aae52c2f1a1a7` | `github-paired-fd1027091646424ea910b9af674204b3` | `78c279db6ee1ec768d04d0c0f9d0539c8a72ab29f41d439f365e77e058b5573d` / `78c5775134c5db9604c0231a234b182484fa9e761a51c76e8cc00ed895767913` | `b97babc71c617c40dd31a5d2185cd58c980595fe09ed9a6529f4783ffac80ba9` |

汇总摘要为：

```text
b33614fd15fb4d4fbb4f1386ccc19c24ee56afc22b72d0202070822af7710033
```

三页的 requested URL 与 final URL 保持 exact SHA 和同一路径；标记
`R1_SCHEMA_CONTRACT_CANDIDATE` 均至少出现一次。每页的三个规范化样本摘要完全一致，active stream
为零，且 `errors / conflicts / cleanup_errors / coverage_reasons` 为空。每个 pair 内 P1 与 P2 共享
session 但保持独立 request seal；三个 session 不是 GitHub 原子快照，也不被描述成三个独立信任域。

## 5. 首次冻结发布被否决与独立修正

首次冻结发布 [PR #100](https://github.com/NoctilumeDev/VeriTrail/pull/100) 的 final head 为
`6cccd8c74490335fe470450dfdcf689fd7447fd5`。其原始
[Public CI run 34471577377](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34471577377)
在 Python 3.10 `-O` 的
`test_same_sealed_authorities_repeat_without_residual_contamination` 停止；PR #100 没有 rerun，也没有
合入，于 `2026-09-10T12:06:42Z` 关闭。失败记录为：

```text
browser_capture_complete = true
browser_completed        = true
services_ready           = true
cleanup_complete         = true
stop_reason              = LIFECYCLE_TIMEOUT
execution_status         = ABORTED
verdict                  = PENDING
```

该测试共享的 M10 公共自举正向夹具把规范 120000 ms 外层 fail-safe 覆盖成未预注册的 15000 ms 性能门。
产品生命周期忠实执行该输入；失败没有证明 R1 Schema 合同或 Core 生命周期错误。独立
[文档 122](122-m10-public-bootstrap-positive-fixture-budget-alignment.md)与
[PR #101](https://github.com/NoctilumeDev/VeriTrail/pull/101) 只移除该无所有者覆盖，并增加确定性预算守卫：

```text
positive functional fail-safe
!=
performance acceptance threshold
```

修正 head `7f9883e4cbaaf7a2c26a1e2593111e13043a6820` 的原始
[Public CI run 34474857428](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34474857428)
在 attempt 1 取得 `11/11 SUCCESS`，并于 `2026-09-10T12:17:24Z` 合入：

```text
main@8aa70807c0de9c0f50ad977575d81f2a1d635a91
```

新 exact main 随后取得：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34475893962`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34475893962) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34475894056`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34475894056) | 1 | `1/1 SUCCESS` |

Public CI 在 `2026-09-10T12:26:59Z` 完成，Browser Smoke 在 `2026-09-10T12:18:30Z` 完成。随后使用
同一公开 Core/插件与 matching Chromium、无 token、无源码 `PYTHONPATH`，对 exact SHA 上的文档 122
执行匿名产品链，取得：

| Fact | Value |
| --- | --- |
| Plan digest | `5dfebfb65b137591ccb552d436f7a11568a1fe6175f6292db423fb5ae6e46839` |
| Paired session | `github-paired-2937f078d2fa4b62902f3a3d458a03d4` |
| API Evidence SHA-256 | `df8e4ce32805542c0d1dbef1716af9790dd9be11947a3e045954a27bc3dcb8f3` |
| Render Evidence SHA-256 | `d0975039519f85f40ae77cf488a7663a06278382c708c2a7fbbfb99d7d215a4e` |
| Handoff digest | `2e007ffec45656f01b886c3bb61985767bd35c0d5c8220dc00250cca53afe2fb` |
| Core report digest | `ac0a713b0089bb65d5be6f1c40f5e865f0e44147059c5860f5eea3610e8bc44b` |
| Verdict | `PASS` |

requested/final URL 均绑定 exact SHA 与文档 122；标记 `R1_SCHEMA_FREEZE_PUBLICATION_BLOCKED` 出现一次，
三次规范化样本摘要均为
`b1fc660bce91b446aca8b088e6e52ceb6aeee51d0f4222bae501e22c2bb4b6a9`。P1/P2 均为
`PUBLISHED / COMPLETE`，active stream 为零，且没有 error、conflict、cleanup error 或 coverage reason。

这些事实只修复冻结发布依赖的既有测试证据边界。它们不改变文档 120 的任何字段、身份或兼容义务；
新的冻结发布必须从 `main@8aa70807...` 重建，不能把 PR #100 的内容或失败运行重新命名为成功。

## 6. 冻结对象

冻结对象是文档 120 定义的 R1 0.1 Schema 与规范身份语义，而不是实际 Schema payload。主要包括：

- `veritrail-json-c14n/1` 规范 JSON 文件字节及 domain-separated semantic digest；
- Git tree 原始 path bytes 的可逆小写 hex 表示、显式 repository-root 对象与完整 terminal entry inventory；
- `commit_oid / commit_tree_oid / analysis_tree_oid`、source coordinate/content/snapshot digest 的独立身份；
- 一次安全读取形成同一 owned snapshot，再供验证与消费，禁止 `verify(path) -> reread(path)`；
- `ReviewPolicy / DerivationProfile / FactSet / RelationSet / ReviewSliceSet / CoverageLedger /
  DerivationEvidence / Manifest` 的字段与依赖方向；
- Python 3.10 首版编码、module mapping、raw blob 半开 byte anchor、稳定 subject slot 与冲突语义；
- 规范 BFS、稳定 tie-break、inclusive budget、atomic edge-plus-target inclusion 与 frontier truncation；
- `analysis_scope_digest / slice_policy_digest / policy_digest` 的职责分离及 staged Coverage 分母；
- `COMPLETE / DIAGNOSTIC` 固定 Artifact 布局、20 个纯数据兼容向量义务，以及
  `RA-003 / RA-004 / RA-008 / RA-023` 的追溯关系。

文档 120 首屏继续保留其候选时点，不被本文改写成“它从一开始就已冻结”。当前事实由本状态发布外部
绑定，保持：

```text
Contract History != Current State Publication
```

## 7. 当前未产生的能力

截至本状态发布基线，以下事实仍然不存在：

```text
no versioned R1 JSON Schema payloads
no executable compatibility corpus
no frozen canonical-byte or digest vector files
no SourceSnapshot importer
no Python parser / compiler adapter
no CodeFact or Relation graph runtime
no ReviewSlice derivation
no CoverageLedger producer
no R1 CLI or runtime CI
no Analyzer / AI / ranking Provider
no R1 tag or Release
```

`R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED` 只允许下一阶段从新 exact main 创建版本化 JSON Schema、纯数据
兼容 corpus、规范字节/摘要向量和 Schema/conformance tests。它不允许创建 runtime importer、parser、
relation/slice engine、CLI 或 Provider，也不等于 `R1_IMPLEMENTED`。

## 8. 本状态发布的最后门

本补丁只允许本文、README、AGENTS、R 轨 Plan、能力地图与 milestones 变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1 均在原始 attempt 1 成功；
5. 从该 exact main 使用公开 Core `0.13.0` 与 GitHub Evidence Plugin `0.1.0` 的产品链，fresh anonymous
   读取 README、本文和 milestones；
6. 三页均须保持 exact-SHA URL、HTTP 200、唯一 usable scope、`COMPLETE`、三样本稳定、指定 marker
   存在，且没有 error、conflict 或 cleanup error；
7. 确认 diff 中仍无实际 Schema、兼容向量、源码包、CLI、Provider、运行 CI、标签或 Release。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED
R1_IMPLEMENTATION_NOT_STARTED
```

任一新反例都会否决本次状态发布。后继不得从本分支直接叠加 Schema payload 或实现，必须从完成读回后的
新 exact main 重新建立独立施工坐标。
