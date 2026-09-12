# R1 Derivation Input Binding 合同冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_INPUT_BINDING_CONTRACT_FROZEN /
> R1_DERIVATION_INPUT_IMPLEMENTATION_ALLOWED /
> R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[R1 Derivation Input Binding 最小运行合同 0.1](132-r1-derivation-input-binding-contract.md)
>
> 候选合入基线：`main@b807ee095630c14edd73621c43943437b6cdddff`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只发布 Derivation Input Binding 合同候选已经完成审计、本地复验、原始 PR 门禁、受保护主线合入、
新 exact-main 门禁与匿名公共渲染读回的事实。本文不修改 R1 Schema/corpus、SourceSnapshot runtime、Core、
P/Q、CI、依赖或发布坐标，也不创建 input binder、parser、Fact、Evidence、Relation、ReviewSlice、Coverage、
完整 Derivation Manifest、Provider、CLI 或 Workbench 能力。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不能授权实现。

## 2. 审计裁决

[前置审计](131-r1-post-snapshot-derivation-input-audit.md)没有把 SourceSnapshot 的绿灯直接继承给后继对象。
它确认：

```text
FactSet provenance requires DerivationEvidence
        +
frozen Manifest permits only COMPLETE eight-file
or DIAGNOSTIC four-file closure
        ↓
Fact-only publication is not a legal closed outcome
```

因此下一步没有直接施工 Fact、Relation、Slice、Coverage 或完整 Derivation，而是选择一个不产生新公共
Artifact 的最小接缝：

```text
published canonical SourceSnapshot
        +
human-sealed canonical ReviewPolicy
        +
fixed canonical DerivationProfile
        +
exact local Git source bytes
        ↓
bounded independent validation and cross-binding
        ↓
one copy-owned DerivationInputSet runtime value
```

`DerivationInputSet` 没有独立 schema、semantic digest、Manifest role 或发布生命周期。路径只负责定位；
被验证且 copy-owned 的 bytes 才决定后继允许消费什么。

## 3. 冻结的合同边界

合同 0.1 冻结以下最小语义：

- 四个 caller-owned absolute Windows path 只作为操作坐标，不进入 Artifact 或后继事实身份；
- 三份 Artifact 分别以单一 handle 有界读取一次，验证规范 bytes、冻结 Schema、摘要、Policy Seal 与闭集；
- Policy 必须按 digest 精确绑定 imported Snapshot/Profile，scope decisions 与 terminal inventory 构成 raw-path
  双射，module root 以 raw Git component 判断 containment；
- exact Git object 必须在本地重新取得并复核 OID、type、size、SHA-256、inventory 与重构 Snapshot 的逐字节
  身份；worktree、index、untracked 与 ref movement 不能进入输入；
- Input Binding 使用独立且不进入语义身份的 acquisition safety profile。它成功返回后该 deadline 结束；
  `ReviewPolicy.execution_budget` 只由后继完整 derivation runtime 合同决定开始点，并在其全部子阶段共享；
- 成功只返回不可由调用方就地修改的 owned value，不写 Artifact、Manifest 或 partial output；失败使用闭集
  typed code，并区分请求、Artifact、repository、受信 runtime、单 Artifact conformance、cross-binding、
  reacquisition 与 safety budget；
- 不同但充分的收紧安全预算、不同合法 absolute paths 与 CPython normal/`-O` 不能改变 owned semantic
  inputs。

其中继续成立：

```text
Input binding != semantic derivation
Owned runtime value != Public Artifact
Artifact publication != Derivation closure
Safety budget controls existence, not semantic identity
Verified bytes == bytes later permitted for consumption
```

## 4. 本地候选证据

候选从 exact `main@b1a58143ae2fd359b885a575587aa4682aef8a04` 建立两笔独立提交：

```text
a6f22f4d0fea85b01e534619ebd8698c8a0e2ab1
  docs: audit R1 derivation input boundary

8706a8ecd9978c28615d2d686cbc7ce2727d7c64
  docs: define R1 derivation input binding contract
```

本地先完成 Markdown link、敏感模式、diff scope 与 `git diff --check`。随后显式把当前 worktree 的 Core、
GitHub Evidence、Review Attention、Starter 与 Authoring Skill source roots 绑定到 CPython 3.10/3.13，分别
运行 normal/`-O` 四条 lane。第一次 verbose 运行全部进程退出成功，但汇总输出被调用工具截断，不能独立
显示四条 lane 的终态；因此没有拿该显示结果直接宣称四矩阵通过，而是用同样 suite 做一次静默复验，只
输出退出码。复验结果为：

| Lane | Core + GitHub Evidence + Review Attention + Authoring Skill |
| --- | --- |
| CPython 3.10 normal | `ALL_SUITES_OK` |
| CPython 3.10 `-O` | `ALL_SUITES_OK` |
| CPython 3.13 normal | `ALL_SUITES_OK` |
| CPython 3.13 `-O` | `ALL_SUITES_OK` |

测试坐标与 imported production module 均绑定当前候选 worktree；没有以其他 editable install 的结果替代。

## 5. PR 候选与受保护主线

[PR #112 `docs: define R1 derivation input binding contract`](https://github.com/NoctilumeDev/VeriTrail/pull/112)
的 base 为 `b1a58143ae2fd359b885a575587aa4682aef8a04`，head 为：

```text
8706a8ecd9978c28615d2d686cbc7ce2727d7c64
```

原始 [Public CI run 34677960571](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34677960571)
在 attempt 1 取得 11/11；没有失败 job 被 rerun，也没有在门禁运行期间追加提交。PR 于
`2026-09-12T06:32:45Z` 合入：

```text
merge commit:
b807ee095630c14edd73621c43943437b6cdddff

tree:
5eaf839e2462916b596651bb67afeab6908555b7

parents:
b1a58143ae2fd359b885a575587aa4682aef8a04
8706a8ecd9978c28615d2d686cbc7ce2727d7c64
```

候选只修改 `AGENTS.md`、`README.md` 与五个 `docs/*.md` 文件，没有修改源码、Schema/corpus、测试、CI、
依赖、tag 或 Release。

## 6. exact-main 门禁

候选合入后，只接受 exact `main@b807ee095630c14edd73621c43943437b6cdddff` 由 push 事件创建的原始
workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34678408822](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34678408822) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34678408819](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34678408819) | 1 | `1/1 SUCCESS` |

PR head、本地矩阵、旧 main 与 Browser Smoke 单项均未替代 exact-main Public CI 的完整结果。

## 7. 匿名产品 Collector 读回

读回使用 exact-main worktree 的 P2 Public Render Collector；环境移除 `GITHUB_TOKEN`、`GH_TOKEN` 与
`VERITRAIL_GITHUB_TOKEN`。每个 target 使用独立 sealed AcceptancePlan、fresh anonymous Chromium context、
exact commit Markdown 坐标、固定正文 scope、三样本稳定窗口与预先声明的单一 literal marker。

| Target | Coverage / HTTP / stable / scope | Marker occurrences | Facts digest | Evidence SHA-256 |
| --- | --- | ---: | --- | --- |
| `README.md` | `COMPLETE / 200 / true / 1 usable` | `R1_DERIVATION_INPUT_BINDING_CONTRACT_CANDIDATE`：1 | `2d783a3c31a39d9eeac7ce5da5ca1decc569d0f7ee8c29693caf6fc6c5d62b67` | `7e23ef34eaeba6833c1d5a53f6d7213df8c8e1e5c61dada25953cae1d6f4dcaa` |
| `docs/132-r1-derivation-input-binding-contract.md` | `COMPLETE / 200 / true / 1 usable` | 标题：1 | `c79de9aef08bc522c17eb3260d5cf128ac63c88dae51edea72f674de26f619b1` | `fbf251c8472a474a165264ecf7f1941ed37c8d1a5e5317f4fe8558f24a9eb2c2` |
| `docs/milestones.md` | `COMPLETE / 200 / true / 1 usable` | `R1 SourceSnapshot 后继最小闭环审计`：1 | `333d4bfa9b94fd93aa5dbff99efe24c70bb268c01b6ad22b6bb15762429ed0c4` | `bad11e2a94acf1965f5458501c817ff990dd8bf9692de3b570823903547fa10e` |

三项 `access_mode` 都是 `ANONYMOUS_FRESH_CONTEXT`，collection errors 与 cleanup errors 均为 0；requested
URL 与 final URL 都保持 exact SHA 和原 repository path。

第一次诊断采集已经完成，但本地结果读取脚本误取不存在的 `final_status`，在解释 Evidence 时以 `KeyError`
停止。该错误没有被归因给 GitHub 或 Collector，也没有把已采结果补写成成功；修正为合同字段
`top_level_http_status` 后，三个 target 全部从 fresh context 重新采集。该读回只证明采集时 GitHub 公共
渲染可观察到候选内容，不证明 GitHub 之外的源头真实性，也不赋予 Collector Verdict 权。

## 8. 保留边界与下一步

本次没有冻结或启动：

- Input Binding runtime、ReviewPolicy authoring、默认 Policy 或自动 Seal；
- Python decoding/parser、module-key production、CodeFact、FactSet 与 DerivationEvidence；
- Provider execution/composition、RelationSet、conflict / UNKNOWN 传播、ReviewSliceSet 与 CoverageLedger；
- COMPLETE/DIAGNOSTIC `R1_DERIVATION` Manifest、Artifact 目录发布、CLI、Workbench 或 Core handoff；
- AI proposal、HumanDisposition、Q scheduling、cache、lane 或 gate reuse；
- remote fetch、branch/tag/HEAD resolver、wheel、版本、tag、Release 或跨平台支持；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文自己的最后门成立后，当前状态为：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN
R1_SOURCE_SNAPSHOT_FROZEN
R1_DERIVATION_INPUT_BINDING_CONTRACT_FROZEN
R1_DERIVATION_INPUT_IMPLEMENTATION_ALLOWED
R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

下一步只允许从新的 exact main 建立 Input Binding runtime 与合同 0.1 的二十二格证据，不得在同一分支
顺带实现 parser、Fact、Evidence、Relation、Slice、Coverage 或完整 Derivation。候选、SourceSnapshot 与
本状态发布的绿灯都不能继承为 runtime 证据；任何新反例仍可否决实现或重开被击穿的最小合同边界。
