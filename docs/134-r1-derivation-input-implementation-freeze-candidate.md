# R1 Derivation Input Binding 实现与冻结候选事实 0.1

> 候选记录状态：`R1_DERIVATION_INPUT_IMPLEMENTED / FREEZE_CANDIDATE /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 精确施工基线：`84512755b6475cfa40ca352f43e4cb7be953a761`
>
> 完整实现 head：`5447a0c0947c44cbbd80af6e90f74438b9950d1f`
>
> 受保护主线实现基线：`46bb81625b9f2dcb4fa1284bd75344e89ed4be5f`
>
> 主线 Tree：`10815dbc9c3e9deacab651dda21589986de25527`
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM`；只实现冻结的 Derivation Input acquisition、
> cross-Artifact binding、exact Git byte reacquisition、owned runtime value 与 typed failure，
> 并把二十二格合同矩阵加入既有 CI

## 1. 当前裁决

Derivation Input Binding 最小运行切片已经实现并合入受保护主线。它从调用方提供的三份 canonical
Artifact 路径与本地 Git repository 路径出发，各读取一次并 copy-own exact bytes，独立验证 Snapshot、
sealed Policy 与 Profile，复算全部摘要与 Seal，验证 scope 双射、module-root containment 与冻结词汇，
再从 exact local Git object database 复获并核对同一批源码 bytes，最终返回一个不发布的
`DerivationInputSet`。

实现没有解码或解析 Python，没有生成 CodeFact、DerivationEvidence、Relation、ReviewSlice、Coverage 或
Manifest，也没有增加 CLI、Provider、Workbench、Core handoff、Q 调度或分发坐标。路径、deadline、Git
executable、attempt 与失败历史只属于 operational provenance，不进入成功 value 的语义身份。

本文仍只是 docs-only freeze candidate。只有本文自己的原始远端门禁、受保护主线合入、候选 exact-main
门禁与匿名公共读回全部成立，再由后继独立状态发布记录这些事实以后，才允许写
`R1_DERIVATION_INPUT_FROZEN`。实现 PR、当前主线绿灯或本文尚未合入的文字都不能替代最后门。

## 2. 最小实现边界

```text
source-snapshot.json
review-policy.json
derivation-profile.json
exact local Git repository
        ↓
one-handle bounded reads / one absolute acquisition deadline
        ↓
canonical bytes + schema-shaped product validation
        ↓
digest / Seal / scope / module-root / vocabulary binding
        ↓
exact Git object reacquisition / byte-for-byte Snapshot continuity
        ↓
copy-owned immutable DerivationInputSet
        ↓
return runtime value / publish nothing
```

实现维持以下边界：

- public request 只接受四个绝对 Windows path，不能选择安全预算、Git executable、输出目录或派生参数；
- Artifact 以单一 handle 有界读取一次；后续只消费 owned canonical bytes，不重新打开路径；
- 三份 Artifact 局部合法仍不足以成功，Policy 必须绑定 exact Snapshot/Profile，scope 必须与 inventory 双射；
- module-root containment 使用 raw Git path component，不使用字符串前缀、宿主大小写或 Unicode 归一化；
- imported Snapshot 与 exact local object database 重构出的 canonical Snapshot 必须逐字节相等；
- 相同 object OID 只 copy-own 一份 blob body，但多个 inventory path 的身份不会被合并；
- 成功 value 不拥有 Artifact、Schema、Manifest role 或独立生命周期，失败也不产生 partial value；
- `jsonschema` 继续只属于仓库 Schema gate，Review Attention base runtime 没有因此增加默认依赖。

## 3. 合同矩阵证据

文档 132 的二十二格由可定位测试逐格覆盖，不用总测试数量替代合同义务：

| # | 合同义务 | 自动化证据 |
| ---: | --- | --- |
| 1–3 | 正向 owned value；Snapshot/Profile digest mismatch | exact Reference Lab 与两个 typed binding 反例 |
| 4–5 | scope 双射；module root component containment | missing/duplicate/extra 与 `pkg`/`pkg2` 单变量组合 |
| 6–8 | 三类 canonical Artifact；availability/runtime；特殊文件 | noncanonical/digest/Seal、缺失坐标、symlink/directory/hard-link cases |
| 9–11 | 单次读取 owned continuity；object mismatch；工作世界噪声 | path replacement、Git corruption、worktree/index/ref movement |
| 12–14 | budget/path 不进 identity；全阶段单一 deadline | 双安全 Profile、异路径同 bytes、fake-clock phase exhaustion |
| 15–16 | inclusive byte limits；object body 去重而路径不合并 | exact-limit/one-over 与 shared-object fixture |
| 17–18 | raw path identity；root/non-root containment | non-UTF-8/NFC-NFD/case 与 `REPOSITORY_ROOT` cases |
| 19 | 合法 Slice/Relation Policy 只被验证 | 零 parser、零 Fact/Relation/Slice 执行边界测试 |
| 20 | Python 3.10/3.13、normal/`-O` 语义一致 | 四矩阵、全 identifier 真值集摘要与 public boundary 扫描 |
| 21 | exact R1 Reference Lab | 22 blobs / 259553 bytes 与全部冻结摘要 |
| 22 | 无派生输出能力 | public API 无 output 参数，文件系统零 Fact/Evidence/Manifest |

public boundary 另行证明顶层包不导出默认安全 Profile、测试 override 或内部 binder，也不导入任何下游
Fact/Relation/Slice/Coverage 模块。16 个冻结失败码全部使用固定、不泄露路径与源码的说明；已知失败不会被
压成 generic internal error。

## 4. Freeze 前反例与最小修正

### 4.1 宿主解释器词汇不能改写冻结 Python 3.10 Profile

第一版实现借用了宿主 `str.isidentifier()`。审计发现 CPython 3.13 接受一批 Python 3.10 尚未拥有的 Unicode
identifier code point；例如 `U+0870` 在 3.13 宿主可被接受，却不能进入冻结的
`veritrail-python-source-3.10` 词汇。若保留该实现，同一 Policy 会随运行宿主改变 conformance 结果：

```text
frozen language semantics = Python 3.10
host helper semantics      = current CPython
        ↓
host runtime identity leaks into contract meaning
```

最终实现把 Python 3.10 keyword 与 identifier 语义固定在产品 validator 内，不允许当前宿主扩大 Profile。
测试不仅保留 `变量` 正例与 `U+0870` 负例，还遍历完整 Unicode code-point 空间，并固定 start/continue 真值集
SHA-256：

```text
identifier start:
086ba2039596f4e84ca79818a445e195d71d9ee46fe52ea4cda47e541865f994

identifier continue with prefix "a":
e3c579def9a076edb3e5bb842a10a6d85c2a0c4f0062c2d61b0897590b8413ff
```

这项修正没有把 parser 或当前 Python runtime identity 加入 Profile；它只阻止 host vocabulary drift。

### 4.2 测试模型与执行坐标

两个早期负例分别错误假设 ASCII `zz` 会排在已有 raw `0xff` path 之后，以及在调用产品前对 symlink path
执行 `.resolve()`、从而抹掉待测 symlink 身份。二者都修正测试模型，没有修改产品排序或文件安全语义。

第一次 Core 全仓回归还从其他 editable worktree 导入 GitHub Evidence 生产模块，测试源码与实现坐标不一致；
该结果立即作废，随后显式绑定当前 worktree 的 Core、P、Entry 与 R source root 后重跑。实现证据不继承
污染运行。

### 4.3 PR rollup 不能替代 exact-main run

实现合入后的一次监控误用 `gh pr view 114`，读到 PR head 的 11 项成功并暂时将其口头解释为 exact-main
结果。后续直接读取 push run 时发现坐标不同，旧结论立即作废；当时尚未创建或修改本文。最终只接受：

```text
PR head run:    34684659163
exact-main run: 34685266682
```

这说明 `same checks`、`same PR` 与 `same repository` 都不能替代 exact execution coordinate。

## 5. Reference Lab

Reference Lab 固定在实现运行以前已经存在的 exact inputs：

```text
source commit:
9ab64121350b69ce81e6be79961ad426026bbc39

analysis root:
plugins/github-evidence/src/veritrail_github

inventory:
22 ordinary Python blobs / 259553 bytes

source_snapshot_digest:
08d32840ef56f0c7c0edd6e51d1c64e40b8f476af9330961d1b10c0916b9aaaa

source-snapshot.json SHA-256:
e2e79a9e21da9c2484b885033cd75503501ec94476539ad575bb8161dd304083

derivation_profile_digest:
e8bbe54140ff2a082b69d6b6967d8630a423abd135ac6e7be0badc1fe053125b

derivation-profile.json SHA-256:
29ed3bed4caf4bd2d7dbae0d54166796fac2148eb483067809700aa953df95e2

analysis_scope_digest:
f56b78795614457eda36e55aec034b558aca4825ebe01e158ea55d547114583e

slice_policy_digest:
bc137efdb676a81d321b797679b44cedc46ee9863e50f4637277a1d7dd77ee81

review_policy_digest:
83e21d837b65b01eeedffe1702f4a576a71f27037708c0f6ae825d704bb2b7b9

review_policy seal:
b5c634a2192552ac6c1ae08ca917af947ce613c5ceb15e6a91ed7cadcdcff8f8

review-policy.json SHA-256:
9e3979f66403bbe814964170d23cc0be99768b6e63f5a4477bd29f67df2ac7aa
```

fixture 还固定 `analysis_scope_digest`、`slice_policy_digest` 与三份输入文件 SHA-256。运行只验证并绑定
Policy 内的 Slice/Relation 配置，不执行它们。Reference Lab 证明 input continuity，不证明任何 Python
Fact、代码正确性、repository coverage、缺陷真值或跨平台行为。

## 6. 本地串行证据

最终本地门禁显式绑定当前 implementation worktree：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| Review Attention normal / `-O` | `61/61` / `61/61` | `61/61` / `61/61` |
| Core 全仓 normal / `-O` | `441/441` / `441/441` | `441/441` / `441/441` |
| GitHub Evidence normal / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| Authoring Skill normal / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| compileall / diff / staged-scope audit | `PASS` | `PASS` |

完整 identifier truth-set、Reference Lab、public exports、零派生产物与 typed failure 又以聚焦测试在四矩阵
独立复验。提交前变更范围固定为 Review Attention runtime/tests/fixtures 与两个既有 CI step 名称；没有修改
Core evaluator、P/Q、Workbench、Schema、release asset 或依赖。

## 7. 受保护主线事实

1. PR #114 head 为 `5447a0c0947c44cbbd80af6e90f74438b9950d1f`；
2. 原始 [Public CI run 34684659163](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34684659163)
   为 attempt 1、11/11 success；
3. PR #114 以 merge commit `46bb81625b9f2dcb4fa1284bd75344e89ed4be5f` 合入受保护 `main`；
4. merge parents 为施工基线 `84512755b6475cfa40ca352f43e4cb7be953a761` 与实现 head；
5. exact-main [Public CI run 34685266682](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34685266682)
   为 attempt 1、11/11 success；
6. exact-main [Browser Smoke run 34685266683](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34685266683)
   为 attempt 1、1/1 success。

这些事实证明实现与现有仓库门禁可以共同成立；不证明本文 docs-only 候选已经闭环，也不把 Windows 结果
外推为 Linux/macOS 支持。

## 8. 范围外与停止线

本候选没有进入：

- Python decoding/parser、module-key production、CodeFact、FactSet 或 DerivationEvidence；
- Provider execution/composition、RelationSet、ReviewSliceSet、CoverageLedger 或 conflict/UNKNOWN 传播；
- 完整 `R1_DERIVATION` Manifest、Artifact directory、CLI、Workbench 或 Core handoff；
- AI proposal、HumanDisposition、Q scheduling/cache/lane/gate reuse 或 Agent/IDE integration；
- wheel、版本、tag、Release、Linux/macOS、network share 或恶意本地管理员 sandbox；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文必须继续满足：

```text
docs-only candidate 原始 required checks 全部成功
    -> exact candidate 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README 与本文
    -> 后继独立最终状态发布
    -> R1_DERIVATION_INPUT_FROZEN
```

任何新反例仍可否决冻结。最后门成立前，下一步只能完成本候选的证据闭环；不得开始 parser、Fact、
Relation、Slice、Coverage、conflict/UNKNOWN 传播或完整 derivation。
