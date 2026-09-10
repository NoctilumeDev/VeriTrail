# R1 SourceSnapshot 首个运行切片合同冻结发布

## 1. 文档身份

> 状态目标：`R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN /
> R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[文档 127](127-r1-source-snapshot-runtime-contract.md)
>
> 候选合入基线：`main@def98c6a116b50fc9c0e7c849dd9118b70285eba`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 SourceSnapshot 运行合同候选已经完成原始远端门禁、受保护主线合入、exact-main 门禁与匿名
公共渲染读回的事实。本文不修改 R1 Schema/corpus、Git acquisition 语义、运行预算数值、Core/P/Q，
也不创建 Review Attention 源码、测试、CLI、CI、Provider、依赖、标签或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有最后门全部
成立，状态目标才成为当前主线事实；在此之前不能把本分支或本文文字当成实现授权。

## 2. 被冻结的最小边界

本次冻结只覆盖：

```text
exact local Git object database
        +
Seal-authority-selected repository_id
        +
full commit OID and GitPathRef analysis root
        ↓
bounded raw-byte object acquisition
        ↓
complete terminal inventory
        ↓
owned canonical SourceSnapshot bytes
        ↓
one atomic create-new source-snapshot.json publication
```

其中：

```text
Artifact publication != R1_DERIVATION closure
Safety budget controls existence, not SourceSnapshot identity
Repository path locates input; verified owned bytes determine the observed snapshot
```

单文件切片不产生 `manifest.json`。冻结的 `R1_DERIVATION` Manifest 继续只描述 COMPLETE 八文件或
DIAGNOSTIC 四文件闭环，不增加第三种 outcome，也不接受占位 Policy/Profile/Evidence。独立 acquisition
safety Profile 是运行保护，不读取后继 `ReviewPolicy.execution_budget`，不进入 SourceSnapshot 的规范字节
或四个语义摘要；预算耗尽、inventory 未关闭或验证失败时不发布部分 Snapshot。

## 3. 候选、PR 与受保护主线

合同候选从精确 `main@1409bea0cd75664df181319348e1ca87e643e743` 建立，候选提交为：

```text
ac3d4169732529ad7662672222156c7e140d0fc8
```

[PR #107 `docs: define R1 SourceSnapshot runtime contract`](https://github.com/NoctilumeDev/VeriTrail/pull/107)
只修改六个 Markdown 文件。其原始
[Public CI run 34521283464](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34521283464)
在 attempt 1 取得 `11/11 SUCCESS`，没有失败 job 被 rerun 覆盖。PR 随后于
`2026-09-10T19:46:31Z` 通过受保护主线合入：

```text
merge commit:
def98c6a116b50fc9c0e7c849dd9118b70285eba

tree:
c3fab1012586f07dcf221d6a7550993524d228f4

parents:
1409bea0cd75664df181319348e1ca87e643e743
ac3d4169732529ad7662672222156c7e140d0fc8
```

冻结的十个 Schema 与十九个 compatibility/canonical corpus 文件没有进入候选 diff。并行 Dependabot
PR #16/#67 未被合入、关闭或带入这条因果链。

## 4. exact-main 门禁

候选合入后，只接受精确 `main@def98c6a116b50fc9c0e7c849dd9118b70285eba` 上由 push 事件创建的原始
运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34522392153](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34522392153) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34522392123](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34522392123) | 1 | `1/1 SUCCESS` |

Public CI 在 `2026-09-10T19:55:39Z` 完成，Browser Smoke 在 `2026-09-10T19:47:31Z` 完成。PR head 的
绿灯、本地矩阵和旧 main 均未替代这两个 exact merge-commit 事实。

## 5. 匿名公共渲染读回

读回环境未提供 `VERITRAIL_GITHUB_TOKEN`。每个 target 使用独立 sealed AcceptancePlan、fresh anonymous
Chromium context 与 P2 Public Render Collector，固定观察 exact commit Markdown 坐标、HTTP status、唯一
scope、三样本稳定窗口和预先声明的 literal marker：

| Target | Marker | Coverage / HTTP / stable | Render Evidence SHA-256 |
| --- | --- | --- | --- |
| `README.md` | `R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_CANDIDATE`（1 次） | `COMPLETE / 200 / true` | `862756639c94b1b4c5a13e124a3a21fe0d1454e6393318651f5dffa972a9e7e3` |
| `docs/120-r1-schema-and-canonical-identity-contract.md` | `one canonical create-new SourceSnapshot artifact`（1 次） | `COMPLETE / 200 / true` | `fffe3ac47898c6217ed464905cef5c66b618e7d1398fba4a617982ee9ec08309` |
| `docs/127-r1-source-snapshot-runtime-contract.md` | 标题、`Safety budget controls existence, not identity`（各 1 次） | `COMPLETE / 200 / true` | `dbc4ae5ac15b636e55fe0d0e7ac771324d76c6b530e4853c58e878a75e7a21a3` |

三项 requested URL 与 final URL 均保持 exact SHA 与原 repository path；每项保留的 navigation chain
均只有同一坐标的最终 `200` 响应。固定 scope 均为 `observed_count = 1 / usable = true`，三个规范化样本
摘要均一致。这里不把 `redirect_chain` 字段名机械解释成“必须为空”：P2 Collector 在该字段中保留最终
主文档响应，坐标是否漂移由 requested/final 与链中安全坐标共同判断。该读回证明公开 GitHub 渲染在
采集时可观察到候选内容，不证明 GitHub 之外的来源真实性，也不把同一平台的 API/Render 观察冒充独立
trust domain。

## 6. 保留的本地证据边界

候选本地定向门在 CPython 3.10/3.13 的 normal/`-O` 四矩阵分别取得 26/26；绑定当前 worktree 的 Core、
GitHub Evidence Plugin 与 Starter 源码后，全仓四矩阵分别取得 441/441。Reference Lab 从 exact commit
`9ab64121350b69ce81e6be79961ad426026bbc39` 的
`plugins/github-evidence/src/veritrail_github` 读取到 22 个普通 Python blob、259553 bytes；本地工具链为
Git for Windows `2.55.0.windows.2`。

第一次本地全仓运行只把 Core `src` 加入 `PYTHONPATH`，GitHub Plugin 实际解析到当前 worktree 之外，因
缺少 `veritrail_github.handoff` 在 collection 阶段失败。该结果被明确作废；没有用其余成功用例证明当前
候选。后续四组结果只在三套 production module 的 `__file__` 均验证位于 exact worktree 后重新建立。

Reference Lab 的快速成功只说明当前样本落在固定 acquisition Profile 内，不证明所有仓库都适用；未来
Profile 放宽或公开可配置必须先建立独立合同/version，不能静默改变本文冻结边界。

## 7. 下一步允许什么

本状态发布自己的最后门成立后，只允许从新的 exact main 建立 SourceSnapshot 最小实现候选：

```text
read-only exact Git object acquisition
raw Git path traversal
bounded independent acquisition safety budget
owned SourceSnapshot construction and validation
atomic create-new single-artifact publication
synthetic Git fixtures + exact Reference Lab
```

仍然禁止：

```text
branch/tag/HEAD resolver
Python parser or module mapper
ReviewPolicy authoring
FactSet / RelationSet
ReviewSliceSet / CoverageLedger
conflict or UNKNOWN propagation implementation
complete R1_DERIVATION Manifest publication
Provider SPI / CLI / Workbench / Core handoff
AI proposal / ranking / HumanDisposition
Q scheduling / cache / lane
wheel / tag / Release
```

这些后续对象必须各自以最小可验证闭环推进。SourceSnapshot 绿灯不能继承为它们的合同或实现证据。

## 8. 当前状态目标与停止线

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文若不能完成自己的原始远端门禁、受保护主线合入、exact-main 门禁和匿名公开读回，上述状态只能是
目标，不能成为事实。任何新反例都可以阻止冻结；状态发布本身没有免检权。
