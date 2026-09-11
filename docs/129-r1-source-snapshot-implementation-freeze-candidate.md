# R1 SourceSnapshot 实现与冻结候选事实 0.1

> 候选记录状态：`R1_SOURCE_SNAPSHOT_IMPLEMENTED / FREEZE_CANDIDATE /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 精确施工基线：`24c41c0ac9221ba4d8ae642c08ca5cdc08587b20`
>
> 完整实现 head：`c4dff3a7d0a6b5b58160da2b3d73151654161a2f`
>
> 受保护主线实现基线：`4f5c41a9f163056ed4c2d2cfd686d321ecba5605`
>
> 主线 Tree：`53d5dd167fb437095fa8a43f99f9a6130d5f9488`
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM`；只实现冻结的 SourceSnapshot acquisition、
> canonical identity、typed failure、owned bytes 与单 Artifact 原子发布，并把对应测试加入既有 CI

## 1. 当前裁决

SourceSnapshot 首个最小运行切片已经实现并合入受保护主线。它从调用方声明的 repository identity、完整
commit OID 与 raw Git analysis root 出发，只读本地 Git object database，建立完整 terminal inventory，
复核 Git object identity，计算冻结的四层语义摘要，并以 create-new 方式发布唯一
`source-snapshot.json`。

实现没有解析 Python、推导 Fact/Relation、建立 ReviewSlice/Coverage、发布完整 Derivation Manifest，
也没有增加 CLI、Provider、Workbench、Core handoff、Q 调度或分发坐标。运行安全预算、Git executable、
工具链版本、attempt 与本机路径属于 operational provenance，不进入 Snapshot canonical bytes 或语义身份。

本文仍只是 docs-only freeze candidate。只有本文自己的原始远端门禁、受保护主线合入、exact-main 门禁与
匿名公共读回全部成立，再由后继独立状态发布记录这些事实以后，才允许写
`R1_SOURCE_SNAPSHOT_FROZEN`。实现 PR 和当前主线绿灯不能替代该最后门。

## 2. 最小实现边界

```text
caller-owned SourceSnapshotSpec
    repository_id + exact commit OID + raw analysis root
                            ↓
trusted runtime config selects Git executable
                            ↓
one fixed absolute acquisition deadline
                            ↓
local read-only Git plumbing / no shell / no lazy fetch
                            ↓
verified commit -> tree -> raw terminal inventory
                            ↓
independent canonical bytes + four semantic digests
                            ↓
owned immutable SourceSnapshot snapshot
                            ↓
same-parent staging + validation + atomic no-replace rename
                            ↓
exactly one source-snapshot.json
```

实现维持以下边界：

- `SourceSnapshotSpec` 只拥有语义坐标；repository path、output path 与 Git executable 不进入 Artifact；
- public request 不能选择 safety budget，测试只能通过非顶层内部入口收紧冻结 Profile；
- wall-clock deadline 在尝试开始时创建一次，Git 读取、建模、canonicalization、validation、staging 与
  publication 共同消费同一绝对预算；
- raw path 不经过 Unicode/locale/case normalization，inventory 只按 unsigned raw full path bytes 排序；
- symlink 只保留 link-target blob bytes，gitlink 不跟随，未知 terminal mode/type 不丢弃；
- output 已存在或并发竞争时绝不覆盖，失败只清理自己拥有的 staging；
- 单文件切片不创建 `manifest.json`，也不伪装成 `R1_DERIVATION` COMPLETE/DIAGNOSTIC closure。

## 3. 合同矩阵证据

文档 127 的二十格不是由“38 个测试很多”代替，而是逐格映射：

| # | 合同义务 | 证据 |
| ---: | --- | --- |
| 1–2 | exact SHA-1/SHA-256 repository-root snapshot | 双 object-format synthetic repositories |
| 3 | ref/缩写/revision expression 在仓库访问前拒绝 | invalid-ref pre-access case |
| 4–5 | raw non-root analysis root；missing/non-tree fail closed | raw byte root 与负向 root cases |
| 6 | regular/executable/symlink/gitlink/unknown mode/type | 单一 raw tree fixture 全量核对 |
| 7 | worktree、index、untracked 噪声不改变 bytes | 同一 object DB 前后加入三类噪声复验 |
| 8 | replace ref 不改写 exact requested object | replacement commit counterexample |
| 9–10 | missing/corrupt/type/size/OID/body mismatch | loose object 与独立 object verifier 反例 |
| 11 | raw locale/case/Unicode 排序 | non-UTF-8 与 raw byte ordering fixture |
| 12 | 不同但充分的 budget 不改变 identity | 两个 tightened test profiles 字节相等 |
| 13–14 | inclusive count/byte/depth 与单一 absolute deadline | exact-limit / one-less 与 fake-clock stages |
| 15 | pre-existing output / concurrent publishers | Windows 真实双线程只有一个完整 winner |
| 16 | validation/digest/publication 注入失败 | typed failure、无 final、无 staging residue |
| 17–18 | 重复与跨 Python/`-O` 确定性 | exact canonical bytes/digest 常量与四矩阵 |
| 19 | 文档 113 exact Reference Lab | 22 blobs / 259553 bytes / frozen coordinate |
| 20 | 后继 importer snapshot continuity | same owned exact bytes fixture；不冒充完整 derivation |

## 4. Freeze 前反例与最小修正

实现期间发现并修正了四个局部接缝，没有重开冻结合同：

1. Git executable 最初误放在 request；最终移入 trusted operational runtime config，调用方不能让待审仓库
   选择工具链；
2. acquisition 与 modeling 最初可能各自建立 deadline；最终改为整个 attempt 共享一个绝对 deadline；
3. canonical artifact size 最初可能在完整 materialization 后检查；最终采用 incremental canonical chunks，
   超限前不继续积累正式 Artifact；
4. 非根 analysis root 的 tree depth 最初可能从零重新计数；最终深度从 repository root 连续计算，避免把
   analysis root 选择变成 budget reset。

源码审计还补出一个 typed-failure 接缝：外层 request 类型正确但内部 spec 类型错误时必须稳定得到
`INVALID_REQUEST`，不能落成 `INTERNAL_ACQUISITION_ERROR`。合同第 7 格也从仅有 untracked 噪声，补成
worktree、index 与 untracked 三类事实均被证明不进入 exact object identity。

## 5. PR #109 首次远端失败

第一版候选 `0f7ba6d84e09187f918f3c855c7c43e47b0415d4` 本地四矩阵成立，但 PR #109 的原始
[Public CI run 34571581284](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34571581284)
在 Python 3.10 与 3.13 的 SourceSnapshot normal step 同时停止：

```text
exact Reference Lab requests 9ab64121350b69ce81e6be79961ad426026bbc39
        ↓
actions/checkout shallow object database does not contain that commit
        ↓
SourceSnapshot refuses network and lazy fetch
        ↓
SOURCE_OBJECT_MISSING
```

这不是产品应当“自动恢复”的错误。SourceSnapshot 的本地只读边界正确地 fail closed；缺口在于 CI 没有
建立 Reference Lab 的本地 object precondition。失败 run 没有 rerun，也没有通过 skip、改用 HEAD、放宽
expected digest 或让 Collector 联网来消除。

独立提交 `c4dff3a7d0a6b5b58160da2b3d73151654161a2f` 只把 Python job 的
`actions/checkout` 设为 `fetch-depth: 0`。网络只属于 CI fixture preparation；产品调用发生时所需对象已经
在本地，运行实现继续保留 `GIT_NO_LAZY_FETCH=1`、完整 OID 与只读 Git plumbing。修正 head 的
[Public CI run 34572221064](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34572221064)
为原始 attempt 1，11/11 全部成功。

## 6. 本地串行证据

所有本地门均显式绑定当前 worktree 的 Core、GitHub Evidence Plugin、Starter 与 Review Attention source
root，避免 editable-install provenance 漂移：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| SourceSnapshot normal / `-O` | `38/38` / `38/38` | `38/38` / `38/38` |
| Core 全仓 normal / `-O` | `441/441` / `441/441` | `441/441` / `441/441` |
| GitHub Evidence normal / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| compileall / diff check | `PASS` | `PASS` |

Reference Lab 固定：

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
```

Artifact 为 10611 bytes，并通过冻结 Draft 2020-12 Schema 与产品 validator。CPython 3.10 normal 与
3.13 `-O` 又在 detached exact-main worktree 上独立复验该 Reference Lab。

## 7. 受保护主线事实

1. PR #109 修正 head 为 `c4dff3a7d0a6b5b58160da2b3d73151654161a2f`；
2. 修正 head 的原始 Public CI attempt 1 为 11/11 success；
3. PR #109 以 merge commit `4f5c41a9f163056ed4c2d2cfd686d321ecba5605` 合入受保护 `main`；
4. merge parents 为施工基线 `24c41c0ac9221ba4d8ae642c08ca5cdc08587b20` 与修正 head；
5. exact-main [Public CI run 34573104009](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34573104009)
   为 attempt 1、11/11 success；
6. exact-main [Browser Smoke run 34573104052](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34573104052)
   为 attempt 1、1/1 success。

这些事实证明实现与现有仓库门禁可以共同成立；不证明本文 docs-only 候选已经闭环，也不把 Windows 结果
外推为 Linux/macOS 支持。

## 8. 范围外与停止线

本候选没有进入：

- branch/tag/HEAD resolver 或 remote fetch capability；
- Python parser、module map、CodeFact、RelationSet、ReviewSliceSet 或 CoverageLedger；
- conflict / UNKNOWN 传播实现或完整 `R1_DERIVATION` Manifest；
- Provider SPI、CLI、Workbench、Core handoff、AI proposal、HumanDisposition 或 Q scheduling；
- wheel、版本、tag、Release、Linux/macOS 支持或恶意本地 object database sandbox；
- 对代码正确性、缺陷真值、用户前提或现实真相的最终判断。

本文必须继续满足：

```text
docs-only candidate 原始 required checks 全部成功
    -> exact candidate 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README 与本文
    -> 后继独立最终状态发布
    -> R1_SOURCE_SNAPSHOT_FROZEN
```

任何新反例仍可否决冻结。最后门成立前，下一步只能完成本候选的证据闭环；不得开始 Fact、Relation、
Slice、Coverage 或完整 derivation。
