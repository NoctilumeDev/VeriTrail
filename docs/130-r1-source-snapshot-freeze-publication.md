# R1 SourceSnapshot 最小运行切片冻结发布

## 1. 文档身份

> 状态目标：`R1_SOURCE_SNAPSHOT_FROZEN /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[文档 129](129-r1-source-snapshot-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@ee249d35e1000d3f15f0a0b4e1ef9eb66a425b32`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 SourceSnapshot 最小实现已经完成冻结候选自身门禁、受保护主线合入、新 exact-main 门禁与
匿名公共渲染读回的事实。本文不修改 SourceSnapshot、Schema、Core、P/Q、CI、依赖或发布坐标，也不创建
Fact、Relation、ReviewSlice、Coverage、完整 Derivation Manifest、Provider、CLI 或 Workbench 能力。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不能授权后继施工。

## 2. 冻结的最小闭环

本次冻结只覆盖：

```text
caller-owned semantic SourceSnapshotSpec
        ↓
trusted operational runtime configuration
        ↓
one fixed absolute acquisition deadline
        ↓
exact local Git object database / no lazy fetch
        ↓
verified commit, tree and complete raw terminal inventory
        ↓
independent canonical bytes and semantic digests
        ↓
owned immutable SourceSnapshot
        ↓
same-parent staging + validation + atomic no-replace publication
        ↓
exactly one source-snapshot.json
```

其中继续成立：

```text
Artifact publication != R1_DERIVATION closure
Safety budget controls existence, not SourceSnapshot identity
Path locates input; verified owned bytes determine the snapshot
Published(SourceSnapshot) => InventoryComplete
```

单文件切片不生成 `manifest.json`。预算耗尽、object 缺失或损坏、inventory 未关闭、canonicalization 超限、
validation 失败、目标已存在或并发竞争失败时，都不得发布部分 Snapshot。运行预算、attempt、Git executable、
本机路径和工具链版本只属于 operational provenance，不进入 Artifact canonical bytes 或语义摘要。

## 3. 实现候选与原始失败链

SourceSnapshot 从 exact `main@24c41c0ac9221ba4d8ae642c08ca5cdc08587b20` 施工。PR #109 的第一版 head
`0f7ba6d84e09187f918f3c855c7c43e47b0415d4` 在
[Public CI run 34571581284](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34571581284)
的 Python 3.10/3.13 exact Reference Lab 同时 fail closed：Actions shallow checkout 没有冻结 commit object，
而产品按合同拒绝网络与 lazy fetch。该 run 没有 rerun。

独立提交 `c4dff3a7d0a6b5b58160da2b3d73151654161a2f` 只令 Python CI checkout 物化完整本地
history，不修改产品语义。修正 head 的
[Public CI run 34572221064](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34572221064)
在 attempt 1 取得 11/11，PR #109 随后以
`main@4f5c41a9f163056ed4c2d2cfd686d321ecba5605` 合入。该失败与修正的完整语义见文档 129；冻结不会擦除
第一次失败，也不会把 CI fixture preparation 解释成产品联网能力。

## 4. 冻结候选发布与受保护主线

[PR #110 `docs: record SourceSnapshot implementation facts`](https://github.com/NoctilumeDev/VeriTrail/pull/110)
只修改五个 Markdown 文件。其 head 为：

```text
e406884a7ead6dcb3498f48af26783e6519f7c32
```

原始 [Public CI run 34575341242](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34575341242)
在 attempt 1 取得 11/11，没有失败 job 被 rerun 覆盖。PR 于 `2026-09-11T07:50:17Z` 合入：

```text
merge commit:
ee249d35e1000d3f15f0a0b4e1ef9eb66a425b32

tree:
e5bd238d18562329369794910e196f77ce554101

parents:
4f5c41a9f163056ed4c2d2cfd686d321ecba5605
e406884a7ead6dcb3498f48af26783e6519f7c32
```

候选没有修改 SourceSnapshot 源码、Schema、Core evaluator、GitHub Evidence runtime、CI 或发布物。

## 5. exact-main 门禁

候选合入后，只接受 exact `main@ee249d35e1000d3f15f0a0b4e1ef9eb66a425b32` 由 push 事件创建的原始
workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34576265163](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34576265163) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34576265221](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34576265221) | 1 | `1/1 SUCCESS` |

PR head、本地矩阵与旧 main 均未替代这两个 exact merge-commit 事实。

## 6. 匿名产品 Collector 读回

读回使用 exact main 的 P2 Public Render Collector。Collector 未获得 GitHub token 或浏览器会话凭据；每个
target 使用独立 sealed AcceptancePlan、fresh anonymous Chromium context、exact commit Markdown 坐标、
固定正文 scope、三样本稳定窗口与预先声明的 literal markers。

| Target | Coverage / stable / scope | Marker occurrences | Facts digest | Evidence SHA-256 |
| --- | --- | --- | --- | --- |
| `README.md` | `COMPLETE / true / 1 usable` | `R1_SOURCE_SNAPSHOT_IMPLEMENTED`、`FREEZE_CANDIDATE`、`R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED` 各 1 次 | `8bd92473c24899439bce7b6d9a00f3cb4ad7f72b743c89fbd1399abb017b6872` | `400a9ecfd3ed95b1c11739c8956a8b670d72f81745d53985fb93ff3fac4c31c3` |
| `docs/129-r1-source-snapshot-implementation-freeze-candidate.md` | `COMPLETE / true / 1 usable` | 标题、`R1_SOURCE_SNAPSHOT_IMPLEMENTED`、`任何新反例仍可否决冻结` 各 1 次 | `e7297b940c0ec2e596ee9cb10d1a2680a914ea5f9767d2a9bc8e7a6295e54776` | `8ca7d4ec5a6de80d603a042237c498b35c4ef413114f9c60976ae6b0d889ba07` |

两项 requested URL 与 final URL 都保持 exact SHA 和原 repository path。第一次诊断读取误用了 Evidence 字段
路径，因此没有把得到的 `null` 当成 marker 成立；随后按冻结 Schema 从
`facts.content.window.stable_facts.literal_markers` 重新读取并断言所有 occurrence 大于零。两轮规范事实摘要
相同，说明修正的是诊断读取方式，不是页面或 Collector 事实。

该读回只证明采集时 GitHub 公共渲染可观察到候选内容；不证明 GitHub 之外的源头真实性，不把公开 Render
升级成独立 trust domain，也不赋予 Collector Verdict 权。

## 7. 保留边界与下一步

本次没有冻结或启动：

- Python parser、module map、CodeFact、RelationSet、ReviewSliceSet 与 CoverageLedger；
- conflict / UNKNOWN 传播实现或完整 `R1_DERIVATION` Manifest；
- Provider SPI、CLI、Workbench、Core handoff、AI proposal、HumanDisposition 与 Q scheduling；
- branch/tag/HEAD resolver、remote fetch、wheel、版本、tag、Release 或跨平台支持；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门成立后，当前状态为：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN
R1_SOURCE_SNAPSHOT_FROZEN
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步仍不是把剩余 R1 对象一次写完。只能从新的 exact main 选择下一个最小闭环，先审计 RelationSet、
ReviewSliceSet、CoverageLedger、conflict / UNKNOWN 传播与完整 derivation 的合同接缝，再决定哪一段获得施工
授权。SourceSnapshot 的绿灯不能继承为它们的证据。任何新反例仍可阻止本次发布或重开后继合同。
