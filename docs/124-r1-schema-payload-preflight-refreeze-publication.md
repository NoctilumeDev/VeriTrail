# R1 Schema payload 前置修正重新冻结发布

## 1. 文档身份

> 状态目标：`R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 冻结对象：[R1 Schema 与规范身份合同 0.1](120-r1-schema-and-canonical-identity-contract.md)
>
> 修正说明：[R1 Schema payload 前置审计与合同修正候选](123-r1-schema-payload-preflight-correction.md)
>
> 修正合入基线：`main@839877ca38489d0518a5b67d5956c7907152529c`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文发布 payload preflight 发现的 Schema identity 缺口已经被最小修正并完成受保护主线、exact-main
门禁与匿名产品读回的事实。本文不创建 JSON Schema、compatibility corpus、canonical byte/digest vector、
运行源码、CLI、Provider、运行 CI、标签或 Release。

本文不抹去文档 121 曾经合法冻结上一版合同，也不把旧全绿解释成新反例从未存在：

```text
previous Schema contract freeze
        -> payload drafting allowed
        -> zero-change payload preflight
        -> identity vocabulary found insufficient
        -> payload stopped
        -> corrected contract candidate
        -> protected-main evidence
        -> this independent state publication
```

## 2. 为什么必须重新冻结

上一轮冻结证明合同候选被完整发布，却不能证明一个不知道实现代码的 Schema 作者已经能够唯一生成所有
对象、引用和摘要投影。preflight 在第一份 payload 写入前证明至少以下身份仍需由实现者猜测：

```text
scope decision -> inventory item binding
coverage item -> stable cross-stage identity
slice frontier -> exact item shape and ordering
provider provenance -> exact run/reference identity
fact/relation/slice/set/evidence -> complete digest projection
provider conflict -> conservative traversal boundary
git mode / BLOB content -> exact representation and condition
public Schema family -> fixed offline file set
```

这些不是新产品能力，而是既有合同对象成为可编码 payload 的必要条件。文档 123 因而只重开该语义边界，
保持 R1 上位合同、Pattern Corpus、Core/P/Q 权威与 human Seal authority 不变。

## 3. 修正候选的受保护主线事实

修正候选提交为：

```text
19a923cae37b057879ae9879296e789c6e348cf2
```

[PR #103](https://github.com/NoctilumeDev/VeriTrail/pull/103) 的原始 Public CI 为：

```text
run id:     34486903233
event:      pull_request
attempt:    1
head SHA:   19a923cae37b057879ae9879296e789c6e348cf2
result:     11 / 11 SUCCESS
```

该 PR 以 merge commit 合入受保护主线：

```text
main:       839877ca38489d0518a5b67d5956c7907152529c
tree:       d970f42f9621760ad986293f314cda4fd9135a77
parent 1:   824d50617320d3fe1aecd1e752e4c4f9224257c2
parent 2:   19a923cae37b057879ae9879296e789c6e348cf2
```

相对 parent 1 只有以下八个文档文件变化：

```text
AGENTS.md
README.md
docs/85-post-core-review-attention-plugin-plan.md
docs/114-capability-boundary-and-system-map.md
docs/120-r1-schema-and-canonical-identity-contract.md
docs/121-r1-schema-contract-freeze-publication.md
docs/123-r1-schema-payload-preflight-correction.md
docs/milestones.md
```

没有 Schema、corpus/vector、源码、测试、插件、脚本或 workflow 混入修正候选。

## 4. exact-main 门禁

合入后的 exact main 没有复用 PR head 的结果：

| Gate | Run | Event | Attempt | Result |
| --- | --- | --- | --- | --- |
| Public CI | [34488281264](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34488281264) | `push` | 1 | `11 / 11 SUCCESS` |
| Browser Smoke | [34488281191](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34488281191) | `push` | 1 | `1 / 1 SUCCESS` |

两条 run 的 `headSha` 均为
`839877ca38489d0518a5b67d5956c7907152529c`。没有 rerun 覆盖失败，也没有把 PR 事件结果冒充主线结果。

## 5. fresh anonymous 产品读回

使用公开 Core `0.13.0`、GitHub Evidence Plugin `0.1.0`、Playwright `1.62.0` 与 matching Chromium，
在无 GitHub token、无 `PYTHONPATH` 的已安装 `site-packages` 环境中，对 exact main 建立四个独立
`P1 API -> P2 Render -> P3/Core` 会话：

| Case | Path | Viewport | Marker | Occurrences | Verdict |
| --- | --- | --- | --- | ---: | --- |
| README | `README.md` | `DESKTOP_1365X768` | `R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE` | 1 | `PASS` |
| Schema contract | `docs/120-r1-schema-and-canonical-identity-contract.md` | `NARROW_390X844` | `R1_SCHEMA_PAYLOAD_BLOCKED` | 2 | `PASS` |
| Preflight correction | `docs/123-r1-schema-payload-preflight-correction.md` | `NARROW_390X844` | `R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE` | 2 | `PASS` |
| Milestones | `docs/milestones.md` | `NARROW_390X844` | `R1_SCHEMA_PAYLOAD_BLOCKED` | 1 | `PASS` |

四个会话均满足：

```text
collector state       PUBLISHED
coverage              COMPLETE
collection order      github-api -> github-public-render
top-level HTTP         200
requested/final path  exact SHA, same repository path
scope                  unique and usable
samples                3, normalized digests identical
errors                 []
conflicts              []
cleanup_errors         []
coverage_reasons       []
active streams         0
Core verdict           PASS
```

本轮规范 summary digest 为：

```text
sha256:3a77672fd78a8f893117f9f5bfe440496f2b9305528f992d0e4e080b301606f6
```

四个 pair 属于同一 GitHub trust domain，但 session 相互独立；每个 pair 内严格串行且不是平台原子快照。
这些事实证明 exact main 的声明能够被产品链观察，不证明 GitHub 之外的真实性。

## 6. 被保留的无效读回尝试

第一次本地读回脚本先成功采集 README，随后第二个 case 在联网前被 Core validator 拒绝：构造的
`plan_id` 超过 64 字符。该目录只包含一个已完成 case，不能冒充四坐标 closure。

后继只缩短 request-instance 标识，并把脚本改为在任何网络访问前先构造、Seal 并验证全部四个 Plan；随后
使用新的 `-v2` 输出坐标完成第 5 节读回。没有放宽 marker、coverage、稳定性、错误或 Verdict 条件。

## 7. 重新冻结的精确边界

重新冻结后，文档 120/123 已经足以唯一指导下一阶段创建：

```text
ten fixed Draft 2020-12 JSON Schema files
data-only positive and negative compatibility corpus
canonical-byte vectors
domain-separated digest vectors
Schema and conformance tests
```

获准施工不等于这些 payload 已经存在。以下能力仍未开始：

```text
SourceSnapshot importer
Git reader
Python parser / compiler adapter
CodeFact / Relation producer
ReviewSlice traversal engine
CoverageLedger producer
runtime conformance importer
R1 CLI
Provider discovery
AI proposal / ranking
HumanDisposition
Core Verdict integration
R1 tag or Release
```

## 8. 本状态发布候选的本地证据

候选把 Core `src`、GitHub plugin `src` 与 test root 绑定到同一 worktree 后，完成：

```text
Python 3.10 normal  419 / 419 PASS
Python 3.10 -O      419 / 419 PASS
Python 3.13 normal  419 / 419 PASS
Python 3.13 -O      419 / 419 PASS
```

9 个变更文件全部为 Markdown；changed/untracked Markdown links 解析为 0 个断链，敏感信息扫描为空，
`git diff --check` 通过。以上只是候选本地证据，不能替代本状态发布自己的远端门禁、合入或公开读回。

## 9. 本状态发布的最后门

本补丁只能更新本文、README、AGENTS、R 轨 Plan、能力地图、历史状态指针与 milestones。它必须独立完成：

1. docs-only scope、Markdown 链接、敏感信息和 `git diff --check`；
2. 双 Python 3.10/3.13 的 normal/`-O` 完整本地门禁；
3. 原始远端 Public CI 11/11 成功，不以 rerun 覆盖失败；
4. 通过受保护主线合入；
5. 新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1 在原始 attempt 1 成功；
6. 从新的 exact main fresh anonymous 读取 README、本文和 milestones，并取得
   `PUBLISHED / COMPLETE / PASS`；
7. 确认仓库仍无实际 R1 Schema payload、runtime importer、parser、slice engine、CLI、Provider、标签或
   Release。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED
R1_IMPLEMENTATION_NOT_STARTED
```

后继不得从旧的零改动 payload branch 直接续写，也不得在本状态发布分支叠加 payload。必须从本发布完成
读回后的新 exact main 建立独立施工坐标。任一新反例仍可否决 payload 资格。
