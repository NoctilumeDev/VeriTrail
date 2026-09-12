# R1 Derivation Input Binding 最小运行切片冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_INPUT_FROZEN /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[文档 134](134-r1-derivation-input-implementation-freeze-candidate.md)
>
> 候选合入基线：`main@aa7ff1140aa8c988e84b38808cb8cb1eebe3fbf3`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 Derivation Input Binding 最小 runtime 已经完成 implementation candidate 自身门禁、受保护主线
合入、新 exact-main 门禁与匿名公共渲染读回的事实。本文不修改 Input Binding runtime、SourceSnapshot、
Schema、Core、P/Q、CI、依赖或发布坐标，也不创建 parser、Fact、Evidence、Relation、ReviewSlice、
Coverage、完整 Derivation Manifest、Provider、CLI 或 Workbench 能力。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不能授权后继施工。

## 2. 冻结的最小闭环

本次冻结只覆盖：

```text
three caller-located canonical Artifacts
    source-snapshot.json
    review-policy.json
    derivation-profile.json
exact local Git repository
        ↓
one-handle bounded reads / one fixed absolute acquisition deadline
        ↓
independent canonical validation and digest / Seal recomputation
        ↓
cross-Artifact binding, scope bijection and raw module-root containment
        ↓
frozen Python 3.10 policy vocabulary
        ↓
exact local Git object reacquisition
        ↓
byte-for-byte SourceSnapshot continuity
        ↓
copy-owned immutable DerivationInputSet
        ↓
return runtime value / publish nothing
```

其中继续成立：

```text
Path locates input; owned bytes determine what was validated and consumed
Locally valid Artifacts != Valid cross-Artifact binding
Host runtime vocabulary != Frozen language semantics
Owned runtime value != Public Artifact
Input binding != Derivation
```

路径、deadline、Git executable、attempt、读取时间与失败历史不进入成功 value。安全预算耗尽、Artifact
不规范、digest/Seal 不匹配、scope 不是双射、module root 越界、Profile 词汇错误、Git object 缺失/损坏或
exact bytes 不连续时，均不得返回 partial value，也不得发布 Artifact 或 Manifest。

## 3. 实现与反例

实现从 exact `main@84512755b6475cfa40ca352f43e4cb7be953a761` 开始。冻结合同的二十二格全部建立了
自动化证据，最终 Review Attention suite 在 CPython 3.10/3.13 的 normal/`-O` 四矩阵均为 `61/61`；Core、
GitHub Evidence 与 Authoring Skill 全仓回归也在对应四矩阵成立。

最重要的实现期反例来自语言词汇：宿主 CPython 3.13 的 `str.isidentifier()` 会接受 Python 3.10 尚未拥有的
Unicode code point。若直接复用宿主 helper，冻结的 `PYTHON_3_10` Profile 会随运行宿主改变。实现因此固定
Python 3.10 keyword/identifier 语义，并以 `U+0870` 负例、合法 Unicode 正例与完整 start/continue truth-set
摘要复验，没有把当前 Python、parser wheel 或 Provider 版本加入 Profile identity。

两个测试自身的反例也被保留：ASCII path 不能替代 raw unsigned-byte ordering，调用产品前 `.resolve()`
也不能抹掉待测 symlink 身份。首次全仓回归还发现测试文件来自当前 worktree，而 editable import 指向另一
worktree；该证据被作废并以 exact source roots 重跑。具体矩阵、摘要与停止线见文档 134。

## 4. Implementation PR 与受保护主线

[PR #114 `feat(review): bind exact R1 derivation inputs`](https://github.com/NoctilumeDev/VeriTrail/pull/114)
的 head 为：

```text
5447a0c0947c44cbbd80af6e90f74438b9950d1f
```

原始 [Public CI run 34684659163](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34684659163)
在 attempt 1 取得 11/11 success。PR 随后合入：

```text
merge commit:
46bb81625b9f2dcb4fa1284bd75344e89ed4be5f

tree:
10815dbc9c3e9deacab651dda21589986de25527

parents:
84512755b6475cfa40ca352f43e4cb7be953a761
5447a0c0947c44cbbd80af6e90f74438b9950d1f
```

该 implementation exact main 的 Public CI run `34685266682` 为 attempt 1、11/11 success；Browser Smoke
run `34685266683` 为 attempt 1、1/1 success。

## 5. 冻结候选发布与 exact-main 门禁

[PR #115 `docs: record Derivation Input implementation facts`](https://github.com/NoctilumeDev/VeriTrail/pull/115)
只修改六个 Markdown 文件。其 head 为：

```text
170edd2dd9569da7c70a219ae11e850ff96aad12
```

原始 [Public CI run 34686289898](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34686289898)
在 attempt 1 取得 11/11 success，没有失败 job 被 rerun 覆盖。PR 于 `2026-09-12T09:50:39Z` 合入：

```text
merge commit:
aa7ff1140aa8c988e84b38808cb8cb1eebe3fbf3

tree:
706083da0e36e3481dcd6d3d7263e1cccd3f0eba

parents:
46bb81625b9f2dcb4fa1284bd75344e89ed4be5f
170edd2dd9569da7c70a219ae11e850ff96aad12
```

候选合入后，只接受 exact `main@aa7ff1140aa8c988e84b38808cb8cb1eebe3fbf3` 由 push 事件创建的原始
workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34686899049](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34686899049) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34686899041](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34686899041) | 1 | `1/1 SUCCESS` |

PR head、implementation main 与旧 main 均未替代这两个 exact candidate merge-commit 事实。

## 6. 匿名产品 Collector 读回

读回使用 clean environment 中已安装的 `veritrail 0.13.0`、`veritrail-github-evidence 0.1.0` 与
`playwright 1.62.0`，没有绑定候选 worktree production source。GitHub token 变量被清除；每个 target
使用独立 sealed AcceptancePlan、fresh anonymous Chromium context、exact commit Markdown 坐标、固定正文
scope、三样本稳定窗口与预先声明的 literal markers。

| Target | Coverage / stable / scope | Marker occurrences | Facts digest | Evidence SHA-256 |
| --- | --- | --- | --- | --- |
| `README.md` | `COMPLETE / true / 1` | 三个状态 marker 各 1 次 | `e6ac4068a3bc0128e589f88f2f594a3007c635ac766efeae409585c5b5aa8778` | `3263405656319786e4f7c41b99f797541822d3398f1ebe34ffa0b0f2df25ca8b` |
| `docs/134-r1-derivation-input-implementation-freeze-candidate.md` | `COMPLETE / true / 1` | 标题、候选状态、停止线 marker 各 1 次 | `fb04646cd692d9bb99f257310002590c6dca860612af79da1930336ccce18871` | `a59596905b093bf13fcd353aa7784bd0f6a268eb91a7b65e470c4b2686c81bd7` |

两项 requested/final coordinate 都保持 exact SHA、`github.com` origin 与原 repository path，无 query 或
fragment。第一次诊断脚本把规范化 `requested_url` 对象误当成字符串，并且 sealed Plan 中也使用了过强的
字符串断言；它在读取层停止，没有被当成产品失败或完成证据。后继读回改用冻结 Schema 的
`/facts/navigation/requested_url/path` 断言和完整 coordinate object 诊断，并以两个全新 context 重新采集。
修正的是读回模型，不是页面或 Collector 事实。

该读回只证明采集时 GitHub 公共渲染可观察到候选内容；不证明 GitHub 之外的源头真实性，不把公开 Render
升级成独立 trust domain，也不赋予 Collector Verdict 权。

## 7. 保留边界与下一步

本次没有冻结或启动：

- Python decoding/parser、module-key production、CodeFact、FactSet 或 DerivationEvidence；
- Provider execution/composition、RelationSet、ReviewSliceSet、CoverageLedger 与 conflict/UNKNOWN 传播；
- 完整 `R1_DERIVATION` Manifest、Artifact directory、CLI、Workbench 或 Core handoff；
- AI proposal、HumanDisposition、Q scheduling/cache/lane/gate reuse、Agent 或 IDE integration；
- wheel、版本、tag、Release、Linux/macOS、network share 或恶意本地管理员 sandbox；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门成立后，当前状态为：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_SOURCE_SNAPSHOT_FROZEN
R1_DERIVATION_INPUT_FROZEN
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步仍不是把剩余 R1 对象一次写完。只能从新的 exact main 审计并冻结下一个最小合同闭环；Input Binding
的绿灯不能继承为 parser、Fact、Relation、Slice、Coverage、conflict/UNKNOWN 或完整 derivation 的证据。
任何新反例仍可阻止本次发布或重开后继合同。
