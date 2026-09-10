# R1 Schema 与规范身份合同冻结发布

## 1. 文档身份

> 状态目标：`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 冻结对象：[文档 120](120-r1-schema-and-canonical-identity-contract.md)
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文外部绑定 R1 Schema 合同候选已经取得的仓库、门禁与匿名产品读回事实。它不修改文档 120
在候选时点记录的状态，也不创建 JSON Schema、兼容向量、源码包、CLI、Provider、运行 CI、标签或
Release。

候选合同已经完成原始远端门禁、受保护主线合入、合入后 exact-main 门禁和三次 fresh anonymous
产品读回。本文自身仍须完成同样的远端闭环；只有最后门全部成立，状态目标才成为当前主线事实。

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

首个提交触发的旧 head run 因第二个提交推送而被平台取消；它不属于最终候选证据，也没有被当作
成功运行复用。

## 3. 合入后 exact-main 门禁

合入后只接受精确 `main@49a2d69d44cca21024808fe5c298db8bac7f64c4` 上由 push 事件创建的
原始运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34468036396`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34468036396) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34468036355`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34468036355) | 1 | `1/1 SUCCESS` |

Public CI 在 `2026-09-10T10:58:38Z` 完成，Browser Smoke 在 `2026-09-10T10:50:01Z` 完成。没有
失败 job 被 rerun 覆盖，也没有用 PR head、旧 main 或本地四矩阵替代合入后的主线事实。

这些门禁证明合入后的仓库回归成立；它们不能替代匿名公开渲染，也不能把 docs-only 合同变成运行能力。

## 4. 匿名产品读回

读回从新的隔离 Python 3.13 环境执行。Core 与 GitHub Evidence Plugin 直接从公开 Release URL 安装，
并由 pip 的 URL hash 约束到已发布摘要：

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

三次读回均绑定 exact merge commit，并分别取得 `PUBLISHED / COMPLETE / PASS`：

| Target | Viewport | Plan digest | Session | Evidence SHA-256（API / Render） | Core report digest |
| --- | --- | --- | --- | --- | --- |
| `README.md` | desktop | `b024f39bf8ff52bd94238c1e64261773baa8579263415920913ea4388290729f` | `github-paired-c7ceb98113e5432397b91bc2f8f80e82` | `d54c0e000107d4aec367c76e2641feb6870cbf8b7bf2abadb6de510bc0b80bad` / `5aba84f23677ba6f42dd8fd386ac438213b4ea03b77b99bbcbe4fb07c0b14922` | `fe16051ffe8a3e6006260e3f25563eb48173dc9201656b55b091abaf5bd414ec` |
| `docs/120-r1-schema-and-canonical-identity-contract.md` | narrow | `4a739b3d31fa66c77970f19060bb3e7846da50528df9ff2f637093760076173b` | `github-paired-e84b1b85c2e6496f9d1632cbc0c76adf` | `d9a03ad857e05840ae957f72fb0cf673ee7e8357a7054d867b7629ceb41af449` / `26a65a423058ba781c4b4af152723e45178986968274d6f0dbb463690662710c` | `e03a12c52bbd9d41250063ab76df74d15a49f86f7ddea4de19e4a18a742ecfdc` |
| `docs/milestones.md` | narrow | `b69472d73cea47a17be4731e192ace0651caae11af6ac5c5b76aae52c2f1a1a7` | `github-paired-fd1027091646424ea910b9af674204b3` | `78c279db6ee1ec768d04d0c0f9d0539c8a72ab29f41d439f365e77e058b5573d` / `78c5775134c5db9604c0231a234b182484fa9e761a51c76e8cc00ed895767913` | `b97babc71c617c40dd31a5d2185cd58c980595fe09ed9a6529f4783ffac80ba9` |

汇总摘要为：

```text
b33614fd15fb4d4fbb4f1386ccc19c24ee56afc22b72d0202070822af7710033
```

三页的 requested URL 与 final URL 保持 exact SHA 和同一路径；要求标记
`R1_SCHEMA_CONTRACT_CANDIDATE` 均至少出现一次。每页的三个规范化样本摘要完全一致，active stream
为零，且 `errors / conflicts / cleanup_errors / coverage_reasons` 为空。

每个 pair 内 P1 与 P2 共享 session 但保持独立 request seal。三个 session 不是 GitHub 原子快照，也不被
描述成三个独立信任域。

## 5. 冻结对象

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

## 6. 当前未产生的能力

截至候选合入基线，以下事实仍然不存在：

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

## 7. 本状态发布的最后门

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
