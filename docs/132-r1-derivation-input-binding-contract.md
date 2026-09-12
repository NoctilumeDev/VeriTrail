# R1 Derivation Input Binding 最小运行合同 0.1

> 状态：`R1_DERIVATION_INPUT_BINDING_CONTRACT_CANDIDATE /
> R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED /
> R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 精确起草基线：`main@b1a58143ae2fd359b885a575587aa4682aef8a04`
>
> 前置审计：[R1 SourceSnapshot 后继最小闭环审计](131-r1-post-snapshot-derivation-input-audit.md)
>
> 上游冻结事实：[R1 SourceSnapshot 最小运行切片冻结发布](130-r1-source-snapshot-freeze-publication.md)
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM_DESIGN`；本候选只冻结输入 acquisition、身份连续性、
> cross-Artifact conformance、owned value 与失败边界，不修改 Schema/corpus、SourceSnapshot runtime、
> Core、P/Q、CI 或发布坐标，也不创建任何运行源码

## 1. 目的与停止线

SourceSnapshot 已经证明 exact Git object 可以形成单一规范 Artifact；它没有把源码正文复制进
`source-snapshot.json`，也没有定义后继 parser 怎样同时绑定 Snapshot、ReviewPolicy、DerivationProfile
与同一批源码 bytes。

本合同只关闭这个接缝：

```text
published source-snapshot.json
canonical sealed review-policy.json
canonical derivation-profile.json
exact local Git object database
        ↓
bounded acquisition and independent validation
        ↓
cross-Artifact conformance and exact byte reacquisition
        ↓
one owned DerivationInputSet value
```

它不解析 Python，不产生 Fact/Relation，不做来源 composition，不传播 conflict/UNKNOWN，不建立 Slice 或
Coverage，也不发布 `R1_DERIVATION` Manifest。合同候选完成本地或远端门禁仍不构成冻结；只有后继独立
docs-only 状态发布完成自己的合入、exact-main 门与匿名读回，才允许开始该边界的实现。

## 2. 为什么这是下一个最小闭环

`FactSet` 的每个 `provenance_refs` 必须绑定 `DerivationEvidence.provider_run_id`；冻结 Manifest 又只允许
COMPLETE 八文件或 DIAGNOSTIC 四文件。直接实现 Fact-only 发布会制造 dangling provenance、占位下游
Artifact 或第三种未授权 outcome。

Input Binding 不产生新的语义 Artifact。它只把已经存在的三个 Artifact 与已经被 Snapshot 绑定的源码
bytes 变成一个不可变运行时拥有关系，因此既能单独验证，又不借用完整 derivation：

```text
Input binding != Fact derivation
Owned runtime value != Public Artifact
Validation authority != Authoring authority
```

## 3. 输入、权威与请求边界

### 3.1 四个调用输入

首版调用只接受四个 caller-owned absolute Windows path：

```text
source_snapshot_path
review_policy_path
derivation_profile_path
repository_path
```

前三者定位普通文件，第四项定位只读本地 Git repository。相对路径、当前工作目录推导与运行中再次发现
repository 一律拒绝。四个路径是操作坐标，不进入 Snapshot、Policy、Profile 或后继 Fact identity。
public request 不接受 branch、tag、`HEAD`、缩写 OID、remote URL、output directory、Provider 参数、parser
参数、执行预算覆盖或 Manifest path。

`repository_path` 只用于按 imported Snapshot 中的完整 OID 复获 object bytes；它不能提供新的
`repository_id`，也不能从 remote、lazy fetch、replace refs、worktree 内容或调用方注入的 alternate-object
环境补全缺失 object。repository 自身已经配置且可在本地只读访问的 object source 继续遵守冻结的
SourceSnapshot acquisition 语义；本合同不暗中收窄或扩张该语义。

### 3.2 三个语义所有者

```text
SourceSnapshot
  owns the exact observed source world

DerivationProfile
  owns Python 3.10 semantic vocabulary and normalization rules

ReviewPolicy
  owns human-sealed scope, capability requirements, module mapping,
  slice policy, governance and derivation execution budget
```

Input Binding 只能验证和持有这些值，不能生成、补写或选择它们。尤其：

- 不根据文件扩展名自动把 entry 设为 `IN_SCOPE`；
- 不从 `sys.path`、editable install 或当前 venv 推测 `python_module_mapping`；
- 不把 Provider 运行版本写回 DerivationProfile；
- 不因某个 scope decision “看起来不合理”而改写 Human Seal；
- 不把 `slice_policy` 或 Provider requirement 当成本切片的执行授权。

### 3.3 caller-owned request 与 trusted runtime

调用方拥有四个路径值；trusted runtime 只拥有固定 Git executable 与本合同的 acquisition safety profile。
待审 Artifact、仓库内容或 public request 都不能选择 Git executable、扩大安全预算或关闭验证步骤。

## 4. Derivation input acquisition safety profile

首版冻结独立运行保护：

```text
profile_id                         = derivation-input/windows-reference/0.1
wall_clock_ms                      = 30000
max_source_snapshot_file_bytes     = 67108864
max_review_policy_file_bytes       = 16777216
max_derivation_profile_file_bytes  = 65536
max_total_unique_blob_bytes        = 268435456
```

Git commit/tree/blob acquisition 的其他 count、depth、single-object 与 cumulative 限制不得比
`snapshot-acquisition/windows-reference/0.1` 更宽。一个 attempt 在 public boundary 入口创建一次绝对
deadline；文件读取、解析、规范验证、摘要/Seal 复算、cross-reference 验证、Git reacquisition、exact-byte
比较与 owned copy 共同消费它。子阶段不能刷新完整 30 秒。

安全 Profile 不进入任何 Artifact bytes、语义摘要或 owned input identity。不同但充分的测试收紧值必须
得到逐字节相同的三个 canonical Artifact 与相同源码 blob bytes；预算不足只使本次 attempt 失败：

```text
Safety budget controls existence, not semantic identity.
```

`ReviewPolicy.execution_budget` 不能保护对尚未验证 Policy 的首次读取。本切片也不开始或消费后继
derivation execution budget。Input Binding 成功返回 owned value 后，本次 acquisition deadline 随即结束；
后继 derivation 何时建立自己的单一绝对 deadline，必须由完整 derivation runtime 合同另行冻结。该合同
必须保证所有 derivation 子阶段共同消费同一份 Policy budget，不能让任何子阶段刷新完整预算，也不能让
本 acquisition budget 被解释为额外的 derivation 时间。

## 5. 三个 Artifact 的安全读取

每个输入 Artifact 必须：

1. 是调用开始时可定位的普通文件；目录、symlink、junction/reparse point 与可检测 hard link 拒绝；
2. 在对应 byte cap 内以单一已打开 handle 有界读取一次；不能先整文件无界读入再检查大小；
3. copy-own exact bytes，以严格 UTF-8、无 BOM、无 CR、恰好一个结尾 LF 的规范 JSON 解析；
4. 拒绝重复 key、额外字段、隐式默认值与非规范字节；
5. 通过冻结 Schema 形状与本合同要求的 runtime conformance；
6. 在后继步骤中只消费 owned bytes/document，不重新打开路径。

路径在读取后被替换、删除或修改，不得改变已经建立的 owned value。读取过程中无法取得一份满足规范的
完整 byte sequence 时 fail closed；“两次读取结果相同”不能替代一次读取后的 owned continuity。

首版只声明 Windows 11 ordinary local filesystem。网络共享、Linux/macOS、不可检测 hard-link filesystem、
恶意本地管理员与底层存储欺骗不在本合同证明范围内。

## 6. 单 Artifact conformance

### 6.1 SourceSnapshot

importer 必须复算并验证：

```text
closed document shape
GitPathRef reversibility and raw-byte ordering
mode / object_type / entry_kind / content compatibility
inventory uniqueness
inventory_digest
source_coordinate_digest
source_content_digest
source_snapshot_digest
exact canonical bytes
```

它消费已发布 Artifact 的 exact canonical bytes，不能重新生成一份替代 Snapshot 后丢弃原输入身份。

### 6.2 DerivationProfile

首版只接受冻结的：

```text
profile_id       = veritrail-python-source-3.10
profile_version  = 0.1
language         = PYTHON
language_semantics = PYTHON_3_10
```

accepted encodings、entry/fact/relation 闭集、normalization 与 traversal rules 必须与文档 120 和公共 Schema
完全一致；`profile_digest` 对删除自身字段后的完整规范文档复算。Provider、parser wheel、宿主 CPython 与
运行环境不进入 Profile，也不能通过“当前解释器支持”扩大它。

### 6.3 ReviewPolicy

importer 必须复算：

```text
analysis_scope_digest
slice_policy_digest
policy_digest
seal.digest
```

并验证所有数组的冻结 rank、唯一性、字段闭集、governance 与 `seal_decision = CONFIRMED`。Seal 只证明这份
Policy 的规范 bytes 被声明为已确认，不证明声明者身份、意图或世界真相。

Input Binding 不提供 ReviewPolicy authoring、默认 Policy、自动 scope classifier 或人工确认 UI。测试与
Reference Lab 必须使用在运行前已经固定 exact bytes 与 expected digest 的 Policy fixture。

## 7. Cross-Artifact conformance

三个 Artifact 局部合法仍不足以形成 DerivationInputSet。必须额外满足：

### 7.1 摘要绑定

```text
policy.source_snapshot_digest == snapshot.source_snapshot_digest
policy.derivation_profile_digest == profile.profile_digest
```

比较使用完整小写 SHA-256 文本。任何 mismatch 都是 typed binding failure；不得用 repository path、文件名、
profile ID 或“内容看起来相同”替代。

### 7.2 Scope 双射

`scope_decisions` 必须与 SourceSnapshot 的 terminal `inventory` 以 exact raw Git path 构成双射：

```text
every inventory path has exactly one decision
every decision path names exactly one inventory entry
no duplicate, missing or extra path
```

排序按 unsigned raw full-path bytes。`OUT_OF_SCOPE` 仍是完整决定，不从分母中消失；source class 不改变
in/out-of-scope authority。本切片只验证决定完整性，不把 disposition 解释成 Python eligibility 或 Coverage。

### 7.3 Module-root containment

`python_module_mapping.module_root` 必须等于 analysis root 或位于其下。containment 按 raw Git path component
判断，不使用字符串前缀、宿主路径大小写或 Unicode 归一化：

```text
analysis root pkg     contains pkg and pkg/sub
analysis root pkg     does not contain pkg2
non-root analysis     does not contain REPOSITORY_ROOT
REPOSITORY_ROOT       contains every valid GitPathRef
```

package prefix 只验证为冻结的 Python-normalized identifier sequence；本切片不实际生成 module key。

### 7.4 Policy/Profile 词汇闭集

Policy 的 `anchor_fact_kinds` 与 `allowed_relations` 必须来自 imported Profile 闭集并按 Profile rank 排序。
provider requirements 继续只允许 `CUMULATIVE`，按 capability identity 排序且唯一。Input Binding 不判断
某个 Provider 是否已安装，也不把 required source 的缺失转换成 Coverage 或 Evidence。Policy 使用
Profile 外词汇、错误 rank 或非法 composition 时归入 `NONCONFORMANT_REVIEW_POLICY`，不能等到后继派生再
猜测或静默过滤。

## 8. Exact Git object reacquisition

通过 Artifact conformance 后，运行必须使用 imported Snapshot 的完整 commit OID 与 analysis root，从
`repository_path` 的本地 object database 重新执行一次有界只读 acquisition：

```text
GIT_NO_LAZY_FETCH = 1
no remote access
no branch/tag/HEAD resolution
no abbreviated OID
no replace-ref interpretation
no worktree/index/untracked traversal
```

reacquisition 必须验证 commit/tree/object types、raw terminal inventory、Git object identity、blob SHA-256、
size 与全部 SourceSnapshot 规范摘要。重新构造的 canonical SourceSnapshot bytes 必须与 imported
`source-snapshot.json` **逐字节相等**；只比较 `source_snapshot_digest` 不足以替代 exact-byte continuity。

成功后保留 imported Snapshot canonical bytes，并把本次复获且核验的全部 blob body copy-own 到运行时
value。worktree/index/ref 随后变化不能影响它；object 缺失、损坏、类型错误、bytes/size/digest 或完整
Snapshot bytes 不等时全部 fail closed。

这一步不把本地 object database 宣称为外部真实性锚点。它只证明后继将消费的 bytes 与已声明 Snapshot
一致。

## 9. Owned DerivationInputSet

成功返回值至少拥有：

```text
source_snapshot_canonical_bytes
review_policy_canonical_bytes
derivation_profile_canonical_bytes
verified_blob_bytes_by_object_identity
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
```

所有 bytes 必须 copy-owned；映射与序列不可由调用方就地修改。document view 每次从 owned canonical bytes
产生独立 copy，或以等价不可变结构暴露。后继消费者只能接收这个 value 或其明确 copy-owned 派生，不接收
原输入路径。

`DerivationInputSet`：

- 不是 JSON Artifact；
- 没有 `artifact_kind`、schema、semantic digest、Manifest role 或独立生命周期；
- 不保存输入路径、budget、attempt、Git executable、wall-clock 或失败历史；
- 不证明 Fact/Relation/Slice/Coverage 已经产生；
- 不证明 ReviewPolicy 的目标正确或 SourceSnapshot 的源头真实。

它只是一个运行时连续性保证：

```text
Path locates input; owned bytes determine what was validated and may be consumed.
```

## 10. 失败模型

首版失败码闭集：

```text
INVALID_DERIVATION_INPUT_REQUEST
INPUT_ARTIFACT_UNAVAILABLE
INPUT_ARTIFACT_NOT_ORDINARY_FILE
INPUT_ARTIFACT_TOO_LARGE
INPUT_REPOSITORY_UNAVAILABLE
INPUT_RUNTIME_UNAVAILABLE
NONCONFORMANT_SOURCE_SNAPSHOT
NONCONFORMANT_REVIEW_POLICY
NONCONFORMANT_DERIVATION_PROFILE
POLICY_SNAPSHOT_MISMATCH
POLICY_PROFILE_MISMATCH
POLICY_SCOPE_MISMATCH
MODULE_ROOT_OUTSIDE_ANALYSIS_ROOT
SOURCE_REACQUISITION_MISMATCH
INPUT_SAFETY_BUDGET_EXHAUSTED
INTERNAL_INPUT_BINDING_ERROR
```

相对路径、禁止的请求字段与错误调用形状使用 `INVALID_DERIVATION_INPUT_REQUEST`；输入文件与本地 repository
不可用必须分别使用 `INPUT_ARTIFACT_UNAVAILABLE` 和 `INPUT_REPOSITORY_UNAVAILABLE`；固定 Git executable
或受信运行前提不可用使用 `INPUT_RUNTIME_UNAVAILABLE`。已打开 Artifact 的非规范内容不降格成 unavailable，
Git object 缺失、损坏、类型、bytes 或重构 Snapshot 不一致统一使用 `SOURCE_REACQUISITION_MISMATCH`。

错误对象只暴露稳定 code 与不含路径、源码、stack trace、locale 文本的固定说明。已知验证错误不能降格为
`INTERNAL_INPUT_BINDING_ERROR`；未知异常也不能泄露本机路径或 Artifact 内容。

失败不发布 Artifact、Manifest、诊断 Bundle 或 partial DerivationInputSet。临时 buffers 只属于 attempt；
重试重新读取三份输入并重新取得 object bytes，前一次部分状态不能暗中续用。重试 history 属于调用方运行
provenance，不进入成功 value。

## 11. 合同矩阵

后继实现至少逐格提供自动化证据：

| # | 单变量义务 | 预期 |
| ---: | --- | --- |
| 1 | 三份规范 Artifact + matching local object database | 返回一个 owned value，不写文件 |
| 2 | Policy 绑定错误 Snapshot digest | `POLICY_SNAPSHOT_MISMATCH` |
| 3 | Policy 绑定错误 Profile digest | `POLICY_PROFILE_MISMATCH` |
| 4 | scope missing / duplicate / extra path | `POLICY_SCOPE_MISMATCH` |
| 5 | module root 等于、位于、字符串前缀伪装在 analysis root | 前两者接受，`pkg2` 反例拒绝 |
| 6 | 三类 Artifact 分别出现非规范 JSON、错摘要或错 Seal | 对应 typed nonconformance |
| 7 | 任一相对 path、缺失 Artifact、缺失 repository、受信 Git runtime 不可用 | 四类请求/availability 错误精确区分 |
| 8 | symlink/reparse point、directory、可检测 hard link | 读取前拒绝 |
| 9 | Artifact path 在读取后替换或删除 | owned bytes 不变，后继不重读 path |
| 10 | exact Git object 缺失、损坏、类型或 body mismatch | `SOURCE_REACQUISITION_MISMATCH` |
| 11 | worktree、index、untracked 与 ref movement | owned inputs 不变 |
| 12 | 两个不同但充分的收紧安全预算 | 三 Artifact bytes 与 blob map 相同 |
| 13 | 相同 Artifact bytes 位于不同合法 absolute paths | owned canonical bytes/digests 相同；路径不进入 value |
| 14 | deadline 在 read / validate / cross-bind / Git / own-copy 各阶段耗尽 | typed stop；没有 partial value |
| 15 | source/profile/policy size gate 的 exact limit 与 one-byte-over | exact limit 进入内容验证；超限在解析前拒绝 |
| 16 | 同一 object OID 被多个 path 引用 | blob body 只拥有一次，inventory identity 不合并 |
| 17 | raw non-UTF-8、NFC/NFD、大小写不同路径 | scope 双射保持 raw identity |
| 18 | `REPOSITORY_ROOT` 与非根 analysis/module root 组合 | raw-component containment 正确 |
| 19 | Policy 含合法 Slice/Relation 配置 | 只验证并保留；零 Slice/Relation 执行 |
| 20 | CPython 3.10/3.13、normal/`-O` | owned canonical bytes/digests 一致 |
| 21 | exact R1 Reference Lab | 全部 22 blob / 259553 bytes 连续绑定 |
| 22 | 输出目录、Fact/Evidence/Manifest 探针 | public API 无此参数且零派生产物 |

测试必须绑定 exact current worktree 的 production module；`Test Source != Imported Production Module` 的结果
一律作废。fake clock 可证明预算所有权，但不能替代 Windows local object reacquisition 与真实文件替换负例。

## 12. Reference Lab

Reference Lab 继续使用：

```text
repository: NoctilumeDev/VeriTrail
commit:     9ab64121350b69ce81e6be79961ad426026bbc39
root:       plugins/github-evidence/src/veritrail_github
tracked ordinary Python blobs: 22
total blob bytes:              259553
source_snapshot_digest:
  08d32840ef56f0c7c0edd6e51d1c64e40b8f476af9330961d1b10c0916b9aaaa
```

后继实现开始前必须提交一份 human-sealed、逐条覆盖该 Snapshot inventory 的 canonical ReviewPolicy fixture，
并固定它、首个 DerivationProfile 与 expected digests 的 exact bytes。expected 值必须在被测 importer 之外
预先复算和审查，不能由被测实现运行后动态回填。

Reference Lab 只证明 input continuity。它不 import/execute 待审 Python，不证明 Python facts、repository
coverage、代码正确性、缺陷真值或跨平台行为。

## 13. 包、依赖与状态边界

后继实现只能位于 `plugins/review-attention`，不得进入 Core、GitHub Evidence Plugin 或 Workbench。它可以
复用同一 R 产品边界内已冻结的 SourceSnapshot canonical/Git object primitives，但不能导入 Core/P/Q 私有
实现或测试模块。

`jsonschema==4.25.1` 继续只属于仓库 Schema gate；Review Attention base runtime 必须用独立、闭合的产品
validator 实现本合同，不能因为方便让 Core 或 P 增加默认依赖。没有 CLI、entry point、wheel、tag 或
Release；包目录存在也不表示分发能力已成立。

## 14. 明确不进入本合同

```text
no ReviewPolicy authoring or automatic Seal
no branch/tag/HEAD resolver or remote fetch
no Python decoding, parsing, AST mapping or module-key production
no CodeFact, FactSet or DerivationEvidence production
no Provider execution, composition or provenance merge
no RelationSet or import target resolution
no conflict / UNKNOWN propagation
no ReviewSliceSpec, ReviewSliceSet or CoverageLedger
no R1_DERIVATION Manifest or Artifact directory publication
no CLI, Workbench, Core handoff, AI proposal or HumanDisposition
no Q scheduling, cache, lane or gate reuse
no wheel, version, tag, Release or cross-platform claim
```

## 15. 候选验收与冻结序列

本合同只有满足以下条件后才有资格进入冻结发布：

1. 文档 113、120、127–131、十个 Schema/corpus、README、AGENTS、R 轨 Plan 与 milestones 没有竞争语义；
2. FactSet provenance、Manifest file-set 与 Input Binding 的边界可分别解释；
3. path、canonical bytes、semantic digest、owned input 与 runtime provenance 没有折叠；
4. input safety budget 与 ReviewPolicy execution budget 没有形成双 authority 或跨阶段 budget refresh；
5. scope 双射、module-root containment、Profile/Policy/Snapshot binding 与 reacquisition continuity 没有实现自由度；
6. diff 只包含 Markdown，不修改 Schema/corpus、源码、测试、CI、依赖、标签或 Release；
7. 本地 docs、链接、敏感、双 Python normal/`-O` 与适用全仓门禁通过；
8. 候选提交经原始 Public CI、受保护主线合入与新 exact-main Public CI / Browser Smoke；
9. 从新 exact main 使用 fresh anonymous P2 Collector 读回 README、本文与 milestones；
10. 后继独立 docs-only 状态发布再完成相同最后门。

只有第 10 项完成后，才允许写：

```text
R1_DERIVATION_INPUT_BINDING_CONTRACT_FROZEN
R1_DERIVATION_INPUT_IMPLEMENTATION_ALLOWED
R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

该授权只覆盖 Input Binding runtime 与合同矩阵，不向 parser、Fact、Relation、Slice、Coverage 或完整
Derivation 传播。SourceSnapshot 与本合同候选的绿灯也不能继承为后继实现证据。

## 16. 当前候选裁决

```text
R1_SOURCE_SNAPSHOT_FROZEN
R1_DERIVATION_INPUT_PRECONTRACT_AUDITED
R1_DERIVATION_INPUT_BINDING_CONTRACT_CANDIDATE
R1_DERIVATION_INPUT_IMPLEMENTATION_NOT_STARTED
R1_FACT_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

本文件没有写运行代码，也没有把未来实现 API 名、类布局或分发形态冻结为公共承诺。任何新反例仍可在
冻结前否决本候选；修正必须重开被击穿的最小边界，不能用兼容分支同时接受两套语义。
