# R1 SourceSnapshot 首个运行切片合同 0.1

> 状态：`R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_CANDIDATE /
> R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`
>
> 影响层级：`L2_CONTRACT`
>
> 基线：`main@1409bea0cd75664df181319348e1ca87e643e743`
>
> 后继状态：[文档 128](128-r1-source-snapshot-runtime-contract-freeze-publication.md)完成独立状态发布后，
> 当前主线为 `R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN /
> R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED / R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED`；本文继续保留
> 合同候选自身的历史状态。
>
> 本文只冻结 SourceSnapshot acquisition、身份连续性、资源停止线和单 Artifact 发布边界；不创建源码包、
> CLI、运行 CI、Provider、标签或 Release。

## 1. 为什么先停在合同

R1 Schema payload 冻结以后，首个运行切片原计划为：

```text
exact Git commit / tree / analysis root
        -> bounded binary-safe acquisition
        -> complete terminal inventory
        -> SourceSnapshot 0.1
        -> create-new immutable publication
```

实现前审计发现两个不能交给代码自行解释的接缝：

1. 文档 120 曾把单文件 SourceSnapshot 切片写成 `canonical artifact + manifest`，但冻结的
   `R1_DERIVATION` Manifest 只允许 COMPLETE 八文件或 DIAGNOSTIC 四文件闭环；
2. `ReviewPolicy.execution_budget` 在 SourceSnapshot 之后才存在，不能反向拥有 Git acquisition 的运行
   安全边界。

因此本文只恢复已经存在的对象边界：

```text
Artifact publication != Derivation closure
Safety budget controls existence, not identity
Repository location identifies where to read; owned object bytes determine what was observed
```

十个已冻结 Schema、十九个 compatibility/canonical corpus 文件及其摘要投影均不修改。

## 2. 本切片交付什么

本切片只允许建立一个独立 Review Attention 产品边界内的最小库能力：

```text
exact local Git object database
        +
caller-declared repository_id
        +
full commit OID
        +
GitPathRef analysis root
        +
non-semantic acquisition budget
        ↓
owned and verified commit/tree/blob bytes
        ↓
complete terminal inventory
        ↓
frozen Schema + conformance validation
        ↓
canonical source-snapshot.json
        ↓
atomic create-new publication
```

成功只证明：在声明的本地 Git object database 中，给定 exact commit 与 analysis root 对应的完整
SourceSnapshot 已按冻结规则建立并发布。它不证明仓库真实、代码正确、Python 可解析、Repository 已被
理解，亦不产生 Fact、Relation、ReviewSlice、Coverage、AttentionProposal、HumanDisposition 或 Core
Verdict。

首版不提供 CLI，不解析 branch/tag/`HEAD`，不读取 dirty worktree/index/untracked 文件，不 checkout，
不执行或 import 待审代码，不访问网络，也不建立完整 `R1_DERIVATION` Bundle。

## 3. 权威与输入分层

### 3.1 语义输入

只有以下值决定成功 SourceSnapshot 的语义身份：

```text
repository_id
exact commit_oid
exact commit_tree_oid
exact analysis_tree_oid
analysis_root
complete terminal inventory
frozen canonicalization and digest rules
```

`repository_id` 由 Seal authority 选择并由调用方原样提供；实现不得从 remote URL、目录名、GitHub slug
或本机路径猜测。
`commit_oid` 必须是当前 object format 下完整的 40 位 SHA-1 或 64 位 SHA-256 小写 hex；首版拒绝 ref
name、缩写 OID、reflog expression 与 revision expression。`analysis_root` 只接受冻结的
`GitPathRef`：仓库根使用 `REPOSITORY_ROOT`，非根路径使用 raw Git bytes 的小写 hex。

### 3.2 操作输入

以下值只决定本次尝试在哪里、以什么资源上限执行，不进入 SourceSnapshot canonical bytes 或任何四个
语义摘要：

```text
local repository location
final output directory
acquisition safety budget
Git executable location/version
attempt identity and retry history
wall-clock timestamps and local diagnostics
```

因此，只要两个不同 safety budget 都足以完成同一语义输入：

```text
B1 != B2
Complete(B1) and Complete(B2)
    -> canonical_bytes(S1) == canonical_bytes(S2)
    -> source_snapshot_digest(S1) == source_snapshot_digest(S2)
```

首版没有 checkpoint/resume。失败后重试必须使用新的 ephemeral construction state；过去失败、attempt
number 与最终采用的 budget 不得进入 SourceSnapshot identity。

Git executable 由受信任的运行环境预置，不能由待审仓库、SourceSnapshot request 或仓库内文件选择；实现
不得优先发现仓库目录中的同名可执行文件。首版记录 executable 的解析后路径与版本作为运行 provenance，
但不声称仅凭版本文本认证该二进制。受信任工具链本身属于当前 trust boundary，不由 SourceSnapshot
证明。

## 4. Git acquisition 边界

### 4.1 本地、只读、无解释器

实现只能以参数数组直接调用 Git plumbing，不经 Shell，不执行 hook、filter、smudge、checkout、用户
代码或项目构建。整个 acquisition 必须：

- 禁用 replace-object 解释，exact OID 不得被 `refs/replace` 改写；
- 禁用 partial-clone lazy fetch，缺失 promised object 必须在本地 fail closed；
- 禁止可选写锁，不刷新 index，不修改 refs、object database、worktree 或 Git 配置；
- 清理可能改变 object source/namespace 的继承环境变量，只保留显式受控的 Git 运行环境；
- 在开始时固定一个本地 repository location，后继不重新发现另一个仓库；
- 记录实际 Git/OS/Python 版本为测试或调用层 provenance，但不写入 SourceSnapshot。

首个可宣称运行基线仅为 Windows 11、CPython 3.10/3.13 与候选验收时记录的 Git for Windows。Artifact
格式本身不绑定平台；Linux/macOS 和其他 Git 版本只有通过独立兼容证据后才能加入支持范围。

### 4.2 读取 object bytes，而不是宿主文件路径

实现不得用 checkout path、`Path.read_bytes()`、Git 的人类可读 quoted path 或宿主字符串 pathspec 建立
inventory。固定流程为：

1. 按完整 OID 读取 commit object 的 type、size 与 raw bytes；
2. 复算 `hash("commit " + size + NUL + bytes)`，确认返回对象正是请求 OID；
3. 从已验证 commit bytes 取得唯一顶层 tree OID，再读取并复核该 tree；
4. 对非根 `analysis_root`，按 `git_path_hex` 解码出的 raw components 逐层匹配 tree entry；不把 raw
   bytes 先解码成 Unicode 或交给 OS path API；
5. 从 exact analysis tree 递归读取 raw tree objects，保留 terminal mode/type/OID/path；
6. 对每个 BLOB OID 读取一次 exact bytes，先依据 object header 执行单对象 budget gate，再复算 Git OID、
   SHA-256 与 byte length；同一 OID 的 owned immutable bytes 可在一次尝试内复用；
7. GITLINK 只保留 commit OID，不跟随、不要求 superproject object database 含有该 commit；
8. 所有 terminal entry 关闭并按 raw repository-relative Git path bytes 排序后，才建立 inventory 与四个
   SourceSnapshot digest。

Git object OID 的复算使用 repository object format 对 `type + SP + decimal-size + NUL + bytes` 计算。
SHA-1 仓库仍额外对每个 blob exact bytes 计算冻结 Schema 要求的 SHA-256 content identity。任何 OID、
type、declared size、actual size、tree grammar 或 content digest 不一致都使本次 acquisition 失败。

### 4.3 原始路径与树结构

tree parser 必须从 raw bytes 工作。每个 entry name 禁止空值、NUL、`/`、`.` 与 `..`；同一 tree 内 raw
name 必须唯一。目录 entry 继续递归但不进入 terminal inventory；symlink 只读取其 blob 中的 link-target
bytes 而不跟随；submodule 只成为 `GITLINK`；未知 terminal mode/type 必须按冻结规则保留为
`OTHER_TRACKED_ENTRY`，不能静默丢弃或伪装成普通文件。

同一 tree OID 可以出现在多个合法 path 下：object bytes 可以复用，但每个展开 path 都是独立 inventory
coordinate，并共同消费 traversal budget。实现不得把 Git tree 自身的排序、宿主 locale、Unicode
normalization 或大小写折叠当作最终 inventory 顺序。

## 5. Snapshot acquisition safety budget

首版使用独立 `SnapshotAcquisitionBudget`，与 `ReviewPolicy.execution_budget` 没有继承、复制或默认绑定
关系。它至少同时限制：

```text
one absolute wall-clock deadline
maximum bytes for the commit object
maximum tree depth
maximum unique tree objects read
maximum expanded tree-entry occurrences
maximum bytes for one tree object
maximum total unique tree-object bytes
maximum terminal inventory entries
maximum bytes for one blob
maximum total unique blob bytes owned
maximum canonical artifact bytes
```

首个公开实现固定使用以下操作 Profile；它只约束一次 acquisition attempt，不进入 SourceSnapshot
canonical bytes、digest 或 semantic identity：

```text
profile_id                       = snapshot-acquisition/windows-reference/0.1
wall_clock_ms                    = 30000
max_commit_bytes                 = 8388608
max_tree_depth                   = 128
max_unique_tree_objects          = 8192
max_expanded_tree_entries        = 65536
max_single_tree_bytes            = 8388608
max_total_unique_tree_bytes      = 67108864
max_terminal_inventory_entries   = 32768
max_single_blob_bytes            = 16777216
max_total_unique_blob_bytes      = 268435456
max_canonical_artifact_bytes     = 67108864
```

首个公开实现不提供调用方放宽这些上限的入口。测试可以注入更小但足以完成夹具的预算，以确定性触发
边界；未来若要公开可配置 Profile，必须先建立独立合同与版本身份，不能把一次调用参数写进
SourceSnapshot。

所有数量上限都是包含式最大值；commit、tree、blob、inventory、canonicalization 与 validation 只能消费
同一个绝对 deadline 与同一组累计计数，不能在子阶段之间刷新完整预算。实现必须在读取已知 object body、
扩大 traversal 或开始下一个有界工作单元之前检查其 header/候选加入与剩余时间；不能先把无限内容读入
内存再宣布超限。可取消的 Git 子进程 I/O 必须只获得剩余 deadline，CPU/文件系统原语则必须由上述独立
字节/数量上限约束，并在每个不可再分的有界工作单元前后重新检查时间。因此 `wall_clock_ms` 是停止接纳
后续工作的绝对 safety deadline，不冒充宿主调度器或文件系统提供的 hard real-time 完成保证。

发布的不可逆提交点不刷新也不继续消费 acquisition budget：producer 在 budget 尚未耗尽且规范 bytes 已
全部验证、写入 staging、关闭文件并完成落盘 bytes 复核后，才允许尝试一次 atomic no-replace
publication。原子发布成功返回
即定义本次完成；失败则不重试为覆盖式发布。不得在原子提交成功以后因为重新读取时钟而删除或降格已经
发布的 Artifact。

预算是运行保护策略，不是源码选择器。它只能产生两种结果：

```text
all construction and validation complete within budget -> allow one publication commit
any budget exhausted                                -> fail, publish no SourceSnapshot
```

禁止发布截断 inventory、`PARTIAL SourceSnapshot` 或带正式 `source_snapshot_digest` 的临时对象。该固定
Profile 必须同时满足 16 GB 主机边界与文档 113 的 22 文件、259553-byte Reference Lab。若现实反例证明
它不适用，必须回到合同建立新 Profile/version；不得根据运行结果静默放宽。

## 6. Owned snapshot 与连续性

运行中只在完整读取和验证以后形成一个 owned snapshot value：

```text
verified commit/tree/blob bytes
        +
complete normalized inventory records
        +
canonical SourceSnapshot document/bytes
```

所有 mutable builders 在交付 producer validator 前必须被 copy-owned/frozen；验证与发布消费同一份
canonical bytes，不允许 `verify(path) -> reread(path)`。首切片完成后无需把源 blob bytes 复制进 Artifact，
但后继 parser 只能：

1. 在同一进程中消费 acquisition 已拥有的 exact bytes；或
2. 按 Snapshot 中的 exact object OID 从内容寻址 object store 重新取得，并同时复核 Git OID、SHA-256 与
   size 后消费。

后继不得读取 worktree path，也不得重新解析 branch alias。独立发布的 SourceSnapshot 进入完整
derivation 时，importer 必须安全读取一次 `source-snapshot.json`、验证 exact canonical bytes、Schema、
四个摘要与全部 inventory invariants，再把同一 imported document 放入新的完整 Bundle staging；不能修改
原 Artifact，亦不能重新生成一份语义上“应该相同”的替代品。

## 7. 规范化、验证与依赖边界

成功文档固定使用已冻结的 `review-source-snapshot-0.1.schema.json`、`veritrail-json-c14n/1`、四个
domain-separated digest 投影和唯一结尾 LF。producer 必须在发布前完成：

```text
closed-shape validation
GitPathRef reversibility and raw-byte ordering
mode / object_type / entry_kind / content compatibility
full inventory uniqueness and completeness
four semantic digest recomputations
canonical round-trip and exact-byte check
```

首切片位于未来的 `plugins/review-attention` 独立产品目录；候选 import namespace 固定为
`veritrail_review`。它不得进入 `src/veritrail`，不得导入 Core/P/Q 私有实现，也不得使 Core、GitHub
Evidence 或 Workbench 增加默认安装/运行负担。

首切片生产路径只允许 Python 标准库与显式本地 Git executable。它必须独立实现 canonicalization、digest
和 create-new publication，并以公共 corpus 证明与冻结规范一致；不得导入 `veritrail.canonical`、
`veritrail.atomic_publish` 或测试模块。`jsonschema==4.25.1` 继续只用于仓库 conformance gate，不成为
Core 或 Review Attention 的 base runtime dependency。distribution version、wheel、CLI、entry point、
标签与 Release 留给后继打包合同，本文不借目录名宣布发布事实。

## 8. 发布协议

首切片发布的是一个独立 SourceSnapshot Artifact 目录，而不是 R1 Derivation Bundle：

```text
<caller-selected-new-output>/
  source-snapshot.json
```

最终 output 必须在调用前不存在。producer 在同一 parent 下创建唯一 staging directory，只写一个规范
`source-snapshot.json`；完成 frozen Schema/conformance、exact bytes、size 与 digest 复核后，使用当前平台
能够保证 atomic no-replace 的 primitive 一次发布整个目录。output 已存在、同名竞争者先成功、staging
跨 volume 或平台无法保证 no-replace 时都必须失败，不能覆盖、合并或就地补写。

失败必须 best-effort 清理 owned staging；最终路径不得留下空目录、临时文件、半个 JSON 或可被误读为
成功的 sentinel。Windows 11 的 no-replace backend 必须由真实双发布者竞争测试证明；其他平台不能从
Windows 结果继承支持声明。

该目录不含 `manifest.json`。冻结的 Manifest 继续专属于：

```text
R1_DERIVATION / COMPLETE   -> exact eight artifact files
R1_DERIVATION / DIAGNOSTIC -> exact Snapshot + Policy + Profile + Evidence files
```

不得为单文件切片增加第三个 outcome、缩短 files 集合、伪造占位 Artifact 或把 Manifest 降格成通用文件
索引。单文件 Artifact 的 exact 落盘字节可由调用方 SHA-256 绑定；它的语义身份仍由
`source_snapshot_digest` 表示。

## 9. 失败模型

失败尝试可以返回或记录 typed invocation diagnostics，但它们不是 R1 Artifact，不进入 SourceSnapshot，
也不能冒充 DerivationEvidence。首版至少区分：

```text
INVALID_REQUEST
REPOSITORY_UNAVAILABLE
UNSUPPORTED_OBJECT_FORMAT
SOURCE_OBJECT_MISSING
SOURCE_OBJECT_TYPE_MISMATCH
SOURCE_CONTENT_MISMATCH
MALFORMED_TREE
ANALYSIS_ROOT_NOT_TREE
SAFETY_BUDGET_EXHAUSTED
NONCONFORMANT_SNAPSHOT
OUTPUT_ALREADY_EXISTS
OUTPUT_PUBLICATION_FAILED
INTERNAL_ACQUISITION_ERROR
```

错误文本、stack trace、本机绝对路径与 locale 文本不得进入任何规范 Artifact。即使已经读取部分对象或
计算临时摘要，失败仍满足：

```text
not InventoryComplete -> not Published(SourceSnapshot)
Published(SourceSnapshot) -> InventoryComplete and Conformant
```

## 10. 反例与验收矩阵

实现候选至少要有以下单变量证据；测试数量不能代替格子完整性。

| # | 反例 / 正例 | 必须证明 |
| --- | --- | --- |
| 1 | exact SHA-1 commit + repository root | 产生完整、规范、可复算 Snapshot |
| 2 | exact SHA-256 object-format repository | OID 长度/算法不被写死为 SHA-1 |
| 3 | branch/tag/`HEAD`/缩写/revision expression | 在任何 object read 前拒绝 |
| 4 | analysis root 为 raw non-UTF-8 path | 不经 Unicode/OS path 仍可精确遍历 |
| 5 | root 缺失、指向 blob、含 `.`/`..`/空 component | fail closed，不发布 |
| 6 | regular/executable/symlink/gitlink/unknown terminal | mode/type/kind 与 content 规则准确；不跟随 link/submodule |
| 7 | dirty worktree/index/untracked 在 acquisition 前后变化 | Snapshot bytes/digest 不变 |
| 8 | replace ref 指向另一个 commit | replace semantics 不得改写 exact requested object |
| 9 | promised object 本地缺失 | 不访问网络，返回 missing/unavailable 且无 Artifact |
| 10 | commit/tree/blob OID、type、declared size 或 bytes 被污染 | 检测不一致并拒绝 |
| 11 | raw path 的 locale/case/Unicode 排序诱饵 | 只按 unsigned raw bytes 排序 |
| 12 | 两个不同但充分的 acquisition budgets | 规范 bytes 与全部语义摘要相同 |
| 13 | 任一 budget 正好等于上限 | inclusive 成功；再增加一个原子单位则失败且无输出 |
| 14 | deadline 在 commit/tree/blob/canonicalization/validation 阶段耗尽 | 共用绝对 deadline，不刷新预算，不发布半成品；原子发布是单一提交点 |
| 15 | output 预存在或两个 publisher 竞争同一路径 | 不覆盖；最多一个完整 winner |
| 16 | validation/digest/publication 注入失败 | staging 清理，final path 不可见 |
| 17 | 同一输入重复执行到不同新 output | `source-snapshot.json` 逐字节一致 |
| 18 | CPython 3.10/3.13 normal/`-O` | 相同语义输入产生相同 canonical bytes/digests |
| 19 | 文档 113 exact Reference Lab | 22 个 ordinary Python blob、259553 bytes 与冻结 coordinate 一致 |
| 20 | standalone Snapshot 导入后进入完整 Bundle staging | 同一 exact bytes 被验证和消费，无重新生成/重读漂移 |

第 20 格只可先用 importer contract fixture 证明边界，不能冒充完整 derivation 已实现。真实 Reference Lab
不访问网络、不执行仓库代码，并记录 Git/Python/OS 与 acquisition budget provenance。

## 11. 实现切片与停止线

合同冻结后，首个 implementation candidate 只允许创建：

```text
plugins/review-attention/src/veritrail_review/
  SourceSnapshot request/value and typed failures
  read-only Git object acquisition
  independent canonicalization/digest conformance
  SourceSnapshot producer validator
  atomic create-new single-artifact publisher

plugins/review-attention/tests/
  synthetic Git object fixtures
  frozen corpus conformance
  exact Reference Lab
  publication and budget counterexamples
```

候选不得加入：

```text
branch/tag resolver
Python parser or module mapper
ReviewPolicy authoring
Fact / Relation / Slice / Coverage producer
Provider SPI
CLI / Workbench / Core handoff
AI proposal / ranking / HumanDisposition
Q scheduler / cache / lane
wheel / tag / Release
```

若实现证明 raw-path traversal、object verification、bounded acquisition safety budget 或 atomic no-replace publication
无法按本文兑现，必须停回合同层；不得用 UTF-8 替代路径、post-hoc budget、截断 inventory、普通覆盖式
rename 或半目录“近似实现”。

## 12. 候选最后门

本文只有满足以下条件后才有资格冻结：

1. 文档 120 的 manifest 残留语句完成最小一致性修正，十个 Schema 与十九个 corpus 文件逐字节不变；
2. README、AGENTS、milestones、能力地图和 R1 合同对首切片状态、范围与非声明没有竞争定义；
3. Git object、raw path、budget、owned bytes、validation、publication 与 failure authority 可逐层解释；
4. diff 仅包含 docs-only L2 合同和状态入口，不出现 `plugins/review-attention` 源码、测试、CLI、CI、依赖、
   tag 或 Release；
5. Markdown/link/diff 检查与既有双 Python normal/`-O` 全仓门禁保持成立；
6. 候选经受保护主线合入，并从新 exact main 完成 README、本文与文档 120 的匿名公开读回；
7. 后继独立 docs-only 状态发布完成自己的原始门禁、合入和读回后，才允许写：

```text
R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_FROZEN
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_ALLOWED
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED
```

任一新反例均可否决候选。候选文字、Schema payload 绿灯或历史 R1 合同冻结都不能自动授予运行代码施工
资格。

## 13. 当前候选裁决

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_FROZEN
R1_SOURCE_SNAPSHOT_RUNTIME_CONTRACT_CANDIDATE
R1_SOURCE_SNAPSHOT_IMPLEMENTATION_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文不改变 Core/P/Q、既有 Schema payload、Pattern Corpus 或发布坐标。它只把第一条运行切片在写代码前
需要拥有的最小闭环钉清，并保留实现反例继续否决合同的权力。
