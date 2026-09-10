# Review Attention R1 Schema 与规范身份合同 0.1

> 状态：`R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE / R1_SCHEMA_PAYLOAD_BLOCKED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 修正基线：`main@824d50617320d3fe1aecd1e752e4c4f9224257c2`
>
> 上游合同：[R1 确定性语义切片合同 0.1](113-r1-deterministic-semantic-slice-contract.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；本文只冻结候选 Schema 词汇、规范字节、身份投影、
> 可逆路径、源码锚、遍历端点、结构预算和 Artifact 布局，不创建 JSON Schema、源码包、CLI、Provider、
> 运行 CI、标签、Release 或空实现骨架

## 1. 目的与停止线

R1 语义合同已经冻结，但实现仍不能替以下问题作决定：

```text
Git path 怎样无损进入 JSON？
一个源码锚的起点和终点到底指向哪组字节？
Fact identity、Evidence identity 与文件 identity 怎样分开？
重叠 Slice 按什么顺序扩展，预算在哪个端点停止？
Coverage 的分母怎样证明，而不是只给一个百分比？
一次完成产物由哪些不可变文件组成？
```

本文给出 R1 0.1 的候选答案。当前只允许讨论、反证和冻结 Schema 合同；仓库中仍不得出现
`schemas/review-*.schema.json`、R 轨运行代码、解析器、CLI 或测试实现。只有本文完成自己的受保护主线
合入、exact-main 门禁、匿名公开读回和后继状态发布后，才允许从新的 exact main 创建实际 JSON Schema
与数据型兼容向量。

R1 0.1 继续只处理：

```text
Exact SourceSnapshot
    -> deterministic CodeFacts
    -> typed structural Relations
    -> bounded overlapping ReviewSlices
    -> staged CoverageLedger
```

Artifact 依赖保持单向：

```text
SourceSnapshot      DerivationProfile
       \                 /
        \               /
             ReviewPolicy
                  |
          +-------+--------+
          |                |
       FactSet      DerivationEvidence
          |
      RelationSet
          |
    ReviewSliceSet
          |
    CoverageLedger
          |
   fixed thin Manifest
```

图表示语义依赖，不表示必须拆成多个进程或微服务。R1 Provider 内部可以高内聚；跨 Artifact 只通过版本化
身份和不可变文件组合，任何下游对象都不能反向改写上游状态。

本文不扩大为 AI 审查、缺陷判断、动态调用图、跨语言语义、change blast radius 或 Core Verdict。

## 2. Schema 能证明什么

JSON Schema 只负责结构边界：字段、类型、闭集枚举、必填项、禁止的额外字段和局部数值范围。以下性质
必须由后继 conformance validator 与数据型向量复算，不能因为文档通过 JSON Schema 就宣称成立：

- 摘要是否与规范投影一致；
- 数组是否按规范顺序排列；
- Git path hex 是否可逆且满足路径约束；
- commit、tree、blob 与 SHA-256 是否对应同一组字节；
- coverage 各集合是否互斥、完备并与分母一致；
- Fact、Relation、Slice 引用是否存在且属于同一 Snapshot/Profile；
- Manifest 是否绑定实际读取的同一文件快照；
- ReviewSlice 是否严格按规范遍历、inclusive budget 与 frontier 规则产生。

因此：

```text
Schema-valid != Semantically conformant
Semantically conformant != Defect truth
Artifact bytes identity != Semantic content identity
```

## 3. 规范 JSON 与三类摘要

### 3.1 `veritrail-json-c14n/1`

R1 复用 Core 已公开的 `veritrail-json-c14n/1`：

```text
UTF-8
no BOM
JSON object keys sorted by Unicode code point
compact separators: comma and colon, no insignificant whitespace
ensure_ascii = false
NaN / Infinity forbidden
JSON number limited to integers in R1 identity-bearing fields
```

规范 JSON 值的字节等于现有公共 `canonical_json_bytes(value)`。每个落盘 JSON Artifact 必须是：

```text
canonical_json_bytes(document) + LF
```

文件只允许一个结尾 LF；不允许 BOM、CRLF、缩进、尾随空格或第二个换行。

### 3.2 语义摘要

每一种语义身份使用独立 domain，统一计算：

```text
identity_envelope = {
  "domain": <closed versioned identity domain>,
  "payload": <the exact identity projection>
}

semantic_digest = sha256(canonical_json_bytes(identity_envelope))
```

摘要文本始终是 64 位小写十六进制，不带 `sha256:` 前缀。domain 至少冻结为：

```text
veritrail.review.source-coordinate/0.1
veritrail.review.source-inventory/0.1
veritrail.review.source-content/0.1
veritrail.review.source-snapshot/0.1
veritrail.review.derivation-profile/0.1
veritrail.review.analysis-scope/0.1
veritrail.review.slice-policy/0.1
veritrail.review.review-policy/0.1
veritrail.review.fact-subject/0.1
veritrail.review.code-fact/0.1
veritrail.review.fact-set/0.1
veritrail.review.fact-conflict/0.1
veritrail.review.relation-subject/0.1
veritrail.review.structural-relation/0.1
veritrail.review.relation-set/0.1
veritrail.review.relation-conflict/0.1
veritrail.review.slice-spec/0.1
veritrail.review.review-slice/0.1
veritrail.review.slice-set/0.1
veritrail.review.coverage-denominator/0.1
veritrail.review.coverage-ledger/0.1
veritrail.review.provider-operands/0.1
veritrail.review.provider-run/0.1
veritrail.review.derivation-evidence/0.1
```

domain 必须进入被哈希字节；不同 Artifact 即使 payload 恰好相同，也不能共享身份。

本文摘要公式中的 `A + B + C` 表示一个使用各字段原名的 JSON object，不表示文本拼接、数组拼接或
二进制 concatenation。后继兼容向量必须展开完整 JSON identity envelope 与 expected canonical bytes，
不允许实现自行选择分隔符。

每个文档的 self-digest 字段都从自己的 identity projection 删除；其他已经计算完成、作为依赖引用的摘要
仍保留。例如 `fact_set_digest` 不覆盖自身字段，但必须覆盖 `source_snapshot_digest` 与
`derivation_profile_digest`。禁止用反复迭代直到摘要“稳定”的方式处理自引用。

### 3.3 文件摘要与 Evidence 摘要

Manifest 中的 `sha256` 对**完整落盘字节**计算，包含唯一结尾 LF。它回答“是不是同一个文件”。语义摘要
只覆盖各节明确列出的 identity projection，回答“是不是同一个语义对象”。

Provider、时间、运行环境与 request instance 不进入 Fact/Relation content identity，但进入
`DerivationEvidence` 及具体 Artifact 文件身份。因此允许：

```text
same fact_id
same fact_set_digest
different derivation_evidence_digest
different file sha256
```

这表示两次独立执行报告了相同规范事实，而不是两份 Evidence 被错误合并。

### 3.4 禁止隐式默认值

所有进入 identity projection 的选项必须显式出现。`missing`、`null`、空数组和默认值不是同义词。Schema
不得依赖实现语言的 enum ordinal、对象 `repr`、集合迭代顺序、本机路径、locale、时区或随机哈希。

### 3.5 公共 Schema 原子

后继 Schema 不得自行发明字段类型。R1 0.1 的公共原子固定为：

```text
schema_version            string, exact "0.1"
canonicalization_profile  string, exact "veritrail-json-c14n/1"
Sha256Hex                 string, 64 lower-case hex
SemanticDigest            Sha256Hex carrying a domain-separated semantic identity
NonEmptyText              JSON string, at least one Unicode code point
NonNegativeInteger        JSON integer >= 0
PositiveInteger           JSON integer >= 1
UtcTimestamp              RFC 3339 UTC string ending in "Z"
```

`repository_id / policy_id / profile_id / derivation_id / capability_id / provider_id / parser_id / runtime_id`
及对应 version/ref 字段均为逐 code point 比较的 `NonEmptyText`；R1 不替所有者做 Unicode normalization、
URL canonicalization 或大小写折叠。`policy.version` 是 `PositiveInteger`；`profile_version` 及 Provider、
parser、runtime、resolver version 是 `NonEmptyText`。所有数组都必须显式存在；是否允许空数组由各节决定。

Seal 固定为：

```json
{"algorithm":"sha256","digest":"<Sha256Hex>"}
```

`seal.digest` 仍按对应章节定义的无 `seal` 文档投影计算；Schema 只能验证形状，不能证明摘要正确。

## 4. Git 路径的可逆表示

### 4.1 `GitPathRef`

R1 不把 Git path 直接存成 JSON Unicode 字符串。规范表示只有两种：

```json
{"path_kind":"REPOSITORY_ROOT"}
```

或：

```json
{"git_path_hex":"706c7567696e732f6769746875622d65766964656e6365","path_kind":"GIT_PATH"}
```

`git_path_hex` 是 repository-relative Git path 原始字节的小写十六进制，每个字节固定两位。它不是宿主
文件系统路径，也不经过 UTF-8 解码、Unicode normalization、大小写折叠、URL decode 或路径分隔符替换。

`GIT_PATH` 解码后必须满足：

- 至少一个字节；
- 不以 `/` 开头或结尾；
- 不含 NUL；
- 不含空段；
- 任一段都不等于 ASCII `.` 或 `..`；
- `/` 只表示 Git tree component separator。

repository root 只能使用 `REPOSITORY_ROOT`，不能用空字符串、`00`、`.`、`/` 或缺字段替代。inventory entry
只能使用 `GIT_PATH`。

### 4.2 排序与显示

Git path 的规范顺序是解码后的完整原始字节按 unsigned byte lexicographic order。小写定长 hex 的字典序
与该顺序一致，但 validator 仍须按解码字节定义判断。

R1 0.1 identity Artifact 不保存 `display_path`。Workbench 或后继展示层可以从原始字节安全转义生成显示
文本，但显示文本不进入任何 R1 身份，也不能被再次解析回路径。

这与 Git 的原始路径观察边界一致：`git ls-tree -z` 用 NUL 分隔并原样输出 path；Git 的 canonical path
禁止空段、首尾 `/`、`.`、`..` 与 NUL。实现必须使用等价的二进制安全读取，不能解析 Git 的人类可读
quoted output。

## 5. SourceSnapshot 0.1

### 5.1 固定字段

`source-snapshot.json` 的顶层字段固定为：

```text
artifact_kind = SOURCE_SNAPSHOT
schema_version = 0.1
canonicalization_profile = veritrail-json-c14n/1
repository_id
source_coordinate
inventory
inventory_digest
source_coordinate_digest
source_content_digest
source_snapshot_digest
```

`repository_id` 是 Seal authority 选择的精确 UTF-8 subject identifier；R1 不从本地 remote 名称猜测、
重写或认证它。字符串逐 code point 比较，不做 URL canonicalization。

`source_coordinate` 固定包含：

```text
commit_oid:        {algorithm: SHA1 | SHA256, hex: ...}
commit_tree_oid:   {algorithm: SHA1 | SHA256, hex: ...}
analysis_tree_oid: {algorithm: SHA1 | SHA256, hex: ...}
analysis_root: GitPathRef
```

OID 必须是完整摘要；`SHA1` 对应 40 位小写 hex，`SHA256` 对应 64 位。branch、tag、`HEAD`、worktree
路径和 abbreviated hash 不得进入该对象；它们只可留在 DerivationEvidence 的 request provenance。
`commit_tree_oid` 是 commit 直接引用的 repository root tree；`analysis_tree_oid` 是 analysis root 解析到的
exact subtree，repository root 时两者相等。R1 0.1 的 analysis root 必须解析为 tree，不接受单文件 root。

### 5.2 Inventory

`inventory` 是 analysis root 下全部递归 terminal tracked entry 的数组，不另列中间 directory。每项字段：

```text
git_path: GitPathRef(path_kind = GIT_PATH)
git_mode
git_object: {algorithm, hex, object_type}
entry_kind
content: {sha256, size_bytes} | absent
```

闭集枚举：

```text
object_type = BLOB / COMMIT / OTHER

entry_kind =
  REGULAR_BLOB
  EXECUTABLE_BLOB
  SYMLINK_BLOB
  GITLINK
  OTHER_TRACKED_ENTRY
```

三个 blob kind 必须有 `content`；`content.sha256` 对读取到的 exact blob bytes 计算，`size_bytes` 是同一
字节串长度。`GITLINK` 的 Git object type 是 `COMMIT` 且没有 `content`；它不会被跟随。未知/特殊 mode
必须成为 `OTHER_TRACKED_ENTRY`，不能静默删除或伪装成普通文件。

`git_mode` 的规范 JSON 表示是恰好六位 ASCII 八进制字符串。Git tree 中不足六位的 mode 在解析后左侧
补 `0`，因此 tree directory 的规范形式是 `040000`，但 directory 本身不进入 terminal inventory。已知
映射固定为：

```text
100644 + BLOB   -> REGULAR_BLOB
100755 + BLOB   -> EXECUTABLE_BLOB
120000 + BLOB   -> SYMLINK_BLOB
160000 + COMMIT -> GITLINK
```

其他 terminal mode 必须是 `OTHER_TRACKED_ENTRY`。只要 `git_object.object_type = BLOB`，无论 entry kind
为何，都必须保存 `content`；非 BLOB 不得保存 `content`。`git_object.algorithm/hex` 继续遵守完整 Git
object ID 规则，`content.sha256` 使用 `Sha256Hex` 形状，`size_bytes` 是 `NonNegativeInteger`。

数组按 raw Git path bytes 排序且 path 唯一。目录拓扑由 path 与 exact root tree 决定；不把工作目录、
ignored file、untracked file、index-only change、`__pycache__` 或构建产物混入 inventory。

### 5.3 四个摘要投影

```text
inventory_digest
  payload = inventory

source_coordinate_digest
  payload = repository_id + commit_oid + commit_tree_oid + analysis_tree_oid + analysis_root

source_content_digest
  payload = analysis_tree_oid + analysis_root + inventory_digest

source_snapshot_digest
  payload = source_coordinate_digest + source_content_digest
```

因此两个 commit 可以拥有相同 `source_content_digest`，但必须拥有不同 `source_coordinate_digest` 与
`source_snapshot_digest`。两个 commits 若只在 analysis root 外发生变化，该 root 的 content digest 不变，
但仍由 commit coordinate 区分。Fact 绑定 `source_snapshot_digest`；不得把“字节相同”改写为“交付坐标相同”。

### 5.4 快照连续性

SourceSnapshot 记录的是已经读取并复核的 byte identity。派生阶段必须继续消费同一 owned bytes，或按
`git_object + content.sha256` 从具有独立不可变性保证的内容寻址存储重新取得并复核；禁止重新读取
worktree path 或再次解析 branch alias。

R1 完成 Bundle 不强制复制所有源码字节，但实现必须证明：被 hash 的 Snapshot bytes 正是 parser 和
anchor mapper 消费的 bytes。路径只负责定位，快照负责身份。

## 6. ReviewPolicy 与 DerivationProfile

### 6.1 `review-policy.json`

ReviewPolicy 是 human Seal authority 的输入，不是 Provider 配置回执。固定字段：

```text
artifact_kind = REVIEW_POLICY
schema_version
canonicalization_profile
policy_id
version
source_snapshot_digest
derivation_profile_digest
scope_decisions[]
provider_requirements[]
python_module_mapping
slice_policy
execution_budget
governance
analysis_scope_digest
slice_policy_digest
policy_digest
seal
```

`scope_decisions` 必须对 SourceSnapshot 的每个 terminal entry 恰好给出一次决定，按 Git path 排序：

```text
git_path: GitPathRef(path_kind = GIT_PATH)
disposition = IN_SCOPE / OUT_OF_SCOPE
source_class = FIRST_PARTY / GENERATED / VENDORED / UNCLASSIFIED
reason_code
```

没有命中的 path 不能默认为 first-party 或 in-scope。generated/vendor 不是文件名启发式真值；只能由
sealed policy 显式分类，`UNCLASSIFIED` 必须保持可见。
`reason_code = POLICY_INCLUDED / POLICY_EXCLUDED`，且必须与 disposition 对应；source class 不改变
in/out-of-scope 权威。

`provider_requirements` 以 capability identity 排序，每项显式给出：

```text
capability_id
required = true | false
composition_mode = CUMULATIVE
```

R1 0.1 只冻结 `CUMULATIVE`：所有适用且 required 的来源都必须被观察；某来源成功或返回空集合不能取消
其他来源。替代、优先和互斥语义留给后继 Profile，不能由运行时 `first-success` 偷偷实现。

`scope_decisions` 以 `git_path` 唯一定位 inventory item；没有该字段的 decision 无法证明覆盖哪个条目，必须
拒绝。`provider_requirements` 中 `(capability_id)` 唯一；数组分别按 raw Git path bytes 和
`capability_id` 的 Unicode code-point 顺序排列。`required` 是 JSON boolean，首版
`composition_mode` 只能是 `CUMULATIVE`。

`python_module_mapping` 不从 `sys.path`、editable install 或当前虚拟环境猜测 import namespace。首版固定：

```text
module_root: GitPathRef
package_prefix[]
```

`module_root` 必须等于或位于 analysis root 内；`package_prefix` 是 Seal authority 显式给出的
Python-normalized identifier 序列。module root 下 `__init__.py` 映射为 prefix 本身，`x.py` 映射为
`prefix + x`，`x/__init__.py` 映射为 `prefix + x`。其他 `.py` 路径按相同 component 规则映射。不能解码为
UTF-8、不能成为 Python identifier、产生两个候选或越过 module root 的路径必须显式
`UNSUPPORTED/CONFLICT/EXTERNAL_TO_SNAPSHOT`，不能依赖宿主 import machinery 任选结果。

identifier normalization 使用 Python 3.10 标识符规则的 NFKC 结果，Artifact 只保存规范结果；若两个不同
raw Git path 归一到同一 module key，必须是 `CONFLICT`，不能因为 normalized name 相同而合并路径身份。
文件名去掉最后一个 ASCII `.py` 后必须恰好是一个合法、非关键字 identifier；额外的点号、空名和关键字
路径不由首版推测修复。

`python_module_mapping` 是单个对象而不是候选数组；`package_prefix` 是允许为空、保持声明顺序且元素唯一的
Python-normalized identifier 数组。`slice_policy.anchor_fact_kinds` 必须非空、唯一并按 Profile fact-kind
rank 排序；`allowed_relations` 可以为空，每个 `(relation_kind, direction)` 唯一，先按 Profile relation-kind
rank、再按 `OUTBOUND < INBOUND < BOTH` 排序。所有 relation/fact kind 必须属于 Profile 闭集。

`slice_policy` 固定：

```text
anchor_fact_kinds[]
allowed_relations[]: {relation_kind, direction}
max_depth
max_symbols
max_files
max_relations
```

`direction = OUTBOUND / INBOUND / BOTH`。`execution_budget` 只保存 wall-clock、memory 等安全上限，不进入
SliceSpec；它不能改变正常完成时的成员身份。`governance` 与 AcceptancePlan 同样区分
`claim_owner_ref / drafter_ref / seal_authority_ref / seal_decision=CONFIRMED`。

`execution_budget` 的首版字段恰为 `wall_clock_ms / memory_bytes / artifact_bytes`，均为正整数。它们共同
约束一次 derivation 的安全边界；子阶段只能消费同一个绝对预算，不能各自刷新完整 timeout 或容量。

三个摘要职责固定：

```text
analysis_scope_digest
  payload = source_snapshot_digest + derivation_profile_digest
          + scope_decisions + provider_requirements + python_module_mapping

slice_policy_digest
  payload = analysis_scope_digest + slice_policy

policy_digest
  payload = 删除 analysis_scope_digest / slice_policy_digest / policy_digest / seal 后的完整 Policy
```

`policy_digest` 包含 execution budget 与 governance，表示这份完整 sealed Policy；
`analysis_scope_digest/slice_policy_digest` 只表示正常结构派生语义。`seal.digest` 对删除整个 `seal` 后的完整
文档计算，因此会绑定三个已复算摘要。调整 wall-clock、memory 或 drafter metadata 可以改变
`policy_digest` 与具体 Evidence，却不得改变正常 Fact/Relation/Slice content identity。

### 6.2 `derivation-profile.json`

Profile 是版本化语义，不是某个 parser wheel 的版本。固定字段：

```text
artifact_kind = DERIVATION_PROFILE
schema_version
canonicalization_profile
profile_id
profile_version
language = PYTHON
language_semantics = PYTHON_3_10
accepted_source_encodings[]
supported_entry_kinds[]
fact_kinds[]
relation_kinds[]
normalization_rules
traversal_rules
profile_digest
```

首个 Profile 只接受 `UTF-8` 与 `UTF-8-SIG`；其他合法 Python coding declaration 在 R1 0.1 中是
`UNSUPPORTED_SOURCE_ENCODING`，不是 `PARSE_FAILED`。支持条目只有 `REGULAR_BLOB` 与
`EXECUTABLE_BLOB`，且 raw path 以 ASCII `.py` 结尾；symlink 不跟随，gitlink 与其他条目不解析。

闭集顺序同时是规范 rank：

```text
fact_kinds =
  MODULE
  CLASS_DECLARATION
  FUNCTION_DECLARATION
  METHOD_DECLARATION
  IMPORT_DECLARATION

relation_kinds =
  LEXICAL_CONTAINS
  IMPORT_TARGET_LITERAL
```

CPython、parser package 与运行解释器版本属于 DerivationEvidence。只有上述语义投影或规则变化才升级
Profile；不能因为在 CPython 3.13 上运行就接受 3.13-only syntax。

首个固定值为：

```text
profile_id = veritrail-python-source-3.10
profile_version = 0.1
accepted_source_encodings = [UTF-8, UTF-8-SIG]
supported_entry_kinds = [REGULAR_BLOB, EXECUTABLE_BLOB]

normalization_rules = {
  path: git-path-hex/1,
  anchor: raw-blob-half-open/1,
  identifier: python-3.10-nfkc/1,
  fact_projection: r1-python-facts/0.1,
  import_projection: r1-python-import-literal/0.1
}

traversal_rules = {
  algorithm: breadth-first/1,
  budget: inclusive-atomic-edge/1,
  tie_break: r1-relation-rank/0.1,
  cycle_identity: fact-and-relation-digest/1
}
```

`profile_digest` 对删除自身字段后的完整 Profile 计算。上述字符串是语义版本，不是实现 package 名。

## 7. SourceAnchor 与 Python 3.10 投影

### 7.1 Anchor 端点

每个 Fact 使用：

```text
source_anchor = {
  git_path: GitPathRef(GIT_PATH),
  start_byte,
  end_byte
}
```

端点是 exact raw blob bytes 上的零基、半开区间 `[start_byte, end_byte)`：

```text
0 <= start_byte <= end_byte <= content.size_bytes
```

`MODULE` 锚固定为 `[0, size_bytes)`。声明与 import 使用 Python 3.10 AST 节点从第一个语法 token 到
`end_*` 指示的最后 token 后一位；decorator 不因属于 `decorator_list` 就自动并入 class/function anchor。

Python AST 的列坐标是 parser 使用的 UTF-8 byte offset，且 `end_col_offset` 是末端之后的位置。实现必须
按 Python 3.10 encoding detection 解码 UTF-8/UTF-8-SIG，并把 `(lineno, col_offset)` 映射回 exact raw
blob byte offset；必须保留 CRLF、LF、CR 和 UTF-8 BOM 在原始字节中的实际宽度，不能先统一换行再把偏移
误写成 raw anchor。

行列号可以作为后继展示投影，但不进入 Fact identity。缺失或无法无歧义映射的 AST end position 必须使
该文件的 Fact Derivation 有类型失败，不能猜测到下一行或文件末尾。

### 7.2 Fact 粒度

`Fact` 固定字段：

```text
fact_id
subject_key_digest
subject_space
fact_kind
source_snapshot_digest
derivation_profile_digest
source_anchor
local_ordinal
semantic_attributes
provenance_refs[]
```

`subject_space` 闭集是 `MODULE_ENTITY / DECLARATION_NODE / IMPORT_ALIAS`。`subject_key_digest` 只覆盖
Snapshot、Profile、path、anchor、subject space 与 `local_ordinal`；`fact_id` 再加入 `fact_kind` 与
`semantic_attributes`。kind 不进入 subject key，否则两个 Provider 对同一声明是 METHOD 还是 FUNCTION
的分歧会被错误拆成两个无关 subject。相同 subject 出现不兼容 kind/属性时产生不同 `fact_id`，并由
FactSet 冲突组关联。
`provenance_refs` 不进入两者，按 provider-run identity 排序。

上段的“path”就是 `source_anchor.git_path`，不得在 identity envelope 中再复制第二份路径。精确投影为：

```text
subject_key_digest
  domain  = veritrail.review.fact-subject/0.1
  payload = {
    source_snapshot_digest,
    derivation_profile_digest,
    source_anchor,
    subject_space,
    local_ordinal
  }

fact_id
  domain  = veritrail.review.code-fact/0.1
  payload = {subject_key_digest, fact_kind, semantic_attributes}
```

`local_ordinal` 是 `NonNegativeInteger`。`provenance_refs` 是至少一个、排序且唯一的
`provider_run_id`（`SemanticDigest`）数组；每个引用都必须出现在同一 Bundle 的
DerivationEvidence。Schema 只验证摘要形状与非空，存在性由 conformance validator 验证。

kind/space 组合固定：`MODULE -> MODULE_ENTITY`，class/function/method declaration ->
`DECLARATION_NODE`，`IMPORT_DECLARATION -> IMPORT_ALIAS`。MODULE 与 declaration 的
`local_ordinal=0`；只有同一 import statement anchor 下的 alias 使用源码顺序 ordinal。

声明属性闭集：

```text
MODULE:
  module_key_parts[] | null; exact Git path remains the module entity identity

CLASS_DECLARATION:
  declared_name

FUNCTION_DECLARATION / METHOD_DECLARATION:
  declared_name
  function_form = SYNC / ASYNC

IMPORT_DECLARATION:
  import_form = IMPORT / FROM_IMPORT
  relative_level
  module_parts[]
  imported_name | null
  alias_name | null
```

直接位于 class body 的 `FunctionDef/AsyncFunctionDef` 是 `METHOD_DECLARATION`；其他位置的函数声明是
`FUNCTION_DECLARATION`。多个 alias 共用一个 import statement anchor，但每个 alias 产生一个 Fact，
`local_ordinal` 按源码 alias 顺序从 0 开始，避免同锚身份碰撞；MODULE 与普通 declaration 固定为 0。
`module_parts` 和名称使用 Python 3.10 parser-normalized identifier，不声称保留原 token 拼写；exact source
spelling 仍由 source anchor 定位。

`LEXICAL_CONTAINS` 只表达直接语法包含：module 包含其 body 的直接声明/import，class 包含直接 class body
成员，function/method 包含其直接 body 中的嵌套声明/import；它不跨过中间 container 建立传递边。除
`MODULE` 外，每个 Fact 必须恰有一个直接 lexical parent。条件、循环、异常和 with body 不创建新的
CodeFact container，位于其中的声明仍由最近的 module/class/function/method Fact 直接包含。

`module_key_parts` 只由 sealed `python_module_mapping` 与 exact Git path 机械派生；无法唯一映射时为
`null` 并进入 Coverage 的 typed gap。它不是通过实际 `import` 获得的运行时模块名。

`semantic_attributes` 必须按 `fact_kind` 使用以下 exact object，全部拒绝额外字段：

```text
MODULE:
  {module_key_parts: [PythonIdentifier, ...] | null}

CLASS_DECLARATION:
  {declared_name: PythonIdentifier}

FUNCTION_DECLARATION / METHOD_DECLARATION:
  {declared_name: PythonIdentifier, function_form: SYNC | ASYNC}

IMPORT_DECLARATION:
  {
    import_form: IMPORT | FROM_IMPORT,
    relative_level: NonNegativeInteger,
    module_parts: [PythonIdentifier, ...],
    imported_name: PythonIdentifier | "*" | null,
    alias_name: PythonIdentifier | null
  }
```

`PythonIdentifier` 是已经按 Python 3.10 规则 NFKC 规范化、合法且非关键字的非空字符串。
`IMPORT` 必须有 `relative_level=0`、非空 `module_parts`，且 `imported_name` 必须为 `null`；`FROM_IMPORT` 可有空
`module_parts`（例如 `from . import x`），但 `imported_name` 必须是 `PythonIdentifier` 或 exact `"*"`。wildcard
import 的 `alias_name` 必须为 `null`；其他 alias 未声明时也必须显式为 `null`。

### 7.3 FactSet

`fact-set.json` 固定字段：

```text
artifact_kind = FACT_SET
schema_version
canonicalization_profile
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
facts[]
conflicts[]
fact_set_digest
```

`facts` 按 `fact_id` 排序；相同 `fact_id` 只出现一次并汇总 provenance。`conflicts` 按 `conflict_id` 排序，
每项固定包含 `conflict_id / subject_key_digest / candidate_fact_ids[] / provenance_refs[]`，并绑定至少两个
不兼容 `fact_id`。`conflict_id` 覆盖 subject 与排序后的 candidate IDs，不覆盖 provenance；
`fact_set_digest` 覆盖 Snapshot、Profile、analysis scope、去除 provenance 后的规范 facts 与 conflict
semantic records；它不覆盖完整 `policy_digest`。Manifest 文件摘要继续覆盖完整 provenance 与 Policy
引用。

精确摘要投影固定为：

```text
conflict_id
  domain  = veritrail.review.fact-conflict/0.1
  payload = {subject_key_digest, candidate_fact_ids}

fact_set_digest
  domain  = veritrail.review.fact-set/0.1
  payload = {
    source_snapshot_digest,
    analysis_scope_digest,
    derivation_profile_digest,
    facts: facts with provenance_refs removed,
    conflicts: conflicts with provenance_refs removed
  }
```

`candidate_fact_ids` 必须至少两个、排序且唯一；冲突级 `provenance_refs` 是所有候选来源的排序唯一并集。
`policy_digest` 保留在文件中用于交付绑定，但不进入 `fact_set_digest`。

## 8. RelationSet 0.1

`Relation` 固定字段：

```text
relation_id
relation_subject_digest
relation_space
relation_kind
source_fact_id
local_ordinal
target
semantic_attributes
provenance_refs[]
```

`LEXICAL_CONTAINS.target` 必须是 `{target_kind: FACT, fact_id: ...}`。

`IMPORT_TARGET_LITERAL.target` 必须是：

```text
target_kind = IMPORT_LITERAL
relative_level
module_parts[]
imported_name: PythonIdentifier | "*" | null
resolution_status
topology_status
resolved_fact_ids[]
```

闭集：

```text
resolution_status = RESOLVED / UNRESOLVED / UNSUPPORTED / CONFLICT
topology_status = IN_SNAPSHOT / EXTERNAL_TO_SNAPSHOT / UNKNOWN
```

这两个维度正交。`UNRESOLVED + UNKNOWN` 可表示绝对 import 可能来自外部环境；相对引用越过 analysis root
可以是 `UNRESOLVED + EXTERNAL_TO_SNAPSHOT`；多个确定性候选必须是 `CONFLICT`，不能任选一个。
`resolved_fact_ids` 只有 `RESOLVED/CONFLICT` 可非空，且只引用 Snapshot 中的 `MODULE` Fact。

`import x.y` 尝试解析完整 `x.y` module key；`from x.y import z` 只解析 base module `x.y`，不声称 `z`
一定是子模块、属性或运行时对象；`from . import z` 只解析相对 base package。`imported_name` 始终保留为
声明事实，不因 base module 可解析就获得运行时绑定语义。

`relation_space = CHILD_EDGE / IMPORT_EDGE`。`relation_subject_digest` 覆盖 relation space、source fact 与
`local_ordinal`；`relation_id` 再加入 relation kind、target 与 semantic attributes。relation kind 不进入
subject key，使同一 edge slot 的 kind/target 分歧可以形成 conflict。`LEXICAL_CONTAINS` 的 ordinal 按
parent 直接语法子项顺序，`IMPORT_TARGET_LITERAL` 在每个 import Fact 下固定为 0。Provider provenance
不进入 content identity。

R1 0.1 的 Relation 没有第三类扩展属性；`semantic_attributes` 必须是 exact empty object `{}`。新增可参与
Relation identity 的属性必须升级 Profile/Schema，不能通过开放 JSON object 偷渡。精确投影为：

```text
relation_subject_digest
  domain  = veritrail.review.relation-subject/0.1
  payload = {
    source_snapshot_digest,
    derivation_profile_digest,
    relation_space,
    source_fact_id,
    local_ordinal
  }

relation_id
  domain  = veritrail.review.structural-relation/0.1
  payload = {relation_subject_digest, relation_kind, target, semantic_attributes}
```

`local_ordinal` 是 `NonNegativeInteger`；`provenance_refs` 与 Fact 使用同一 provider-run 引用规则。
`resolved_fact_ids` 排序且唯一：`RESOLVED` 必须恰有一个，`CONFLICT` 必须至少两个，
`UNRESOLVED/UNSUPPORTED` 必须为空。`LEXICAL_CONTAINS` 必须使用 `CHILD_EDGE`；
`IMPORT_TARGET_LITERAL` 必须使用 `IMPORT_EDGE`。

IMPORT target 的 `relative_level/module_parts/imported_name` 必须逐项等于 source import Fact 的同名属性；
`module_parts` 使用 `PythonIdentifier` 且允许为空。`RESOLVED/CONFLICT` 的 `topology_status` 必须是
`IN_SNAPSHOT`；`UNRESOLVED/UNSUPPORTED` 的 topology 只能是 `EXTERNAL_TO_SNAPSHOT/UNKNOWN`。
`EXTERNAL_TO_SNAPSHOT/UNKNOWN` 不得携带 resolved Fact ID。

`relation-set.json` 固定：

```text
artifact_kind = RELATION_SET
schema_version
canonicalization_profile
source_snapshot_digest
policy_digest
analysis_scope_digest
derivation_profile_digest
fact_set_digest
relations[]
conflicts[]
relation_set_digest
```

排序、去重、冲突和摘要规则与 FactSet 同构；`relation_set_digest` 绑定 analysis scope，不绑定会随非语义
预算变化的完整 Policy。Relation conflict 同样保存
`conflict_id / relation_subject_digest / candidate_relation_ids[] / provenance_refs[]`，语义摘要不覆盖
provenance。空来源不取消其他来源。

精确摘要投影固定为：

```text
conflict_id
  domain  = veritrail.review.relation-conflict/0.1
  payload = {relation_subject_digest, candidate_relation_ids}

relation_set_digest
  domain  = veritrail.review.relation-set/0.1
  payload = {
    source_snapshot_digest,
    analysis_scope_digest,
    derivation_profile_digest,
    fact_set_digest,
    relations: relations with provenance_refs removed,
    conflicts: conflicts with provenance_refs removed
  }
```

`candidate_relation_ids` 必须至少两个、排序且唯一；冲突 provenance 使用候选来源的排序唯一并集。
`policy_digest` 留在文件中但不进入 `relation_set_digest`。

## 9. ReviewSliceSpec 与规范遍历

### 9.1 Spec

每个机械实例化的 `ReviewSliceSpec` 固定：

```text
source_snapshot_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
fact_set_digest
relation_set_digest
anchor_fact_id
allowed_relations[]
max_depth
max_symbols
max_files
max_relations
slice_spec_digest
```

它只能复制 sealed Policy 允许的关系与不超过 Policy 的结构预算。CLI/request 不得覆盖。最小值：

```text
max_depth >= 0
max_symbols >= 1
max_files >= 1
max_relations >= 0
```

`allowed_relations` 的元素、唯一性与排序沿用 Policy 规则。Spec 中四个 budget 是
`NonNegativeInteger`，其中 symbol/file 的最小值仍为 1。精确摘要投影为：

```text
slice_spec_digest
  domain  = veritrail.review.slice-spec/0.1
  payload = ReviewSliceSpec with slice_spec_digest removed
```

### 9.2 Inclusive budget

R1 0.1 不解释 Provider conflict。若 FactSet 或 RelationSet 的 `conflicts` 非空，ReviewSliceSet 必须使用
`slices=[]`，不得把任一 candidate 当成 canonical anchor/edge，也不得同时遍历所有候选后冒充单一语义图。
Coverage 的 `SLICE_DERIVATION` denominator 为 `UNKNOWN`，保留 `PROVIDER_CONFLICT /
UPSTREAM_DENOMINATOR_UNKNOWN` 与已知上游 item；这仍可
形成协议 `COMPLETE` 的 Bundle，但不形成 normal ReviewSlice。后继若要对不受冲突影响的连通分量做局部切片，
必须先定义可复算的 conflict isolation 合同。

anchor 位于 depth 0，同时计为第 1 个 symbol 和其源码 path 的第 1 个 file。四个 budget 都是**包含式最大
值**：加入候选后必须继续满足 `count <= max_*`。`max_depth=0` 只保留 anchor；`max_relations=0` 不加入边。

候选 relation 是一个原子加入单元：

- 若遍历方向另一端是尚未包含的 Fact，加入 relation 与该 Fact 后必须同时满足
  depth/symbol/file/relation；
- 若另一端 Fact 已在切片中，只增加 relation count；
- literal target 不增加 symbol/file，但 relation hop 仍受 depth 与 relation budget；
- 任一限制会被越过时，relation 与新 target 都不加入，frontier 记录全部适用停止原因；
- 不允许先加入 edge、再因 target 超限留下悬空半结果。

### 9.3 遍历顺序与 tie-break

采用 deterministic breadth-first traversal。queue 先按 `(depth, fact_id)` 排序；对同一 Fact 的候选关系
按以下 tuple 升序：

```text
(relation_kind_rank, direction_rank, relation_id)
```

`relation_kind_rank` 使用 Profile 冻结顺序；`OUTBOUND < INBOUND`，`BOTH` 展开为两个明确方向后去重。
Fact 以 `fact_id` 去重，Relation 以 `relation_id` 去重。循环不会刷新 depth 或重新入队；更短路径先发现，
同深度由上述 tie-break 决定。

任何候选因 `DEPTH_LIMIT / SYMBOL_LIMIT / FILE_LIMIT / RELATION_LIMIT` 被拒绝，都进入 frontier。多个原因
按上述固定 reason rank 排序。只要 frontier 因结构预算非空，Slice coverage 就是 `PARTIAL`；遍历完整
只表示“相对于当前 Snapshot/Profile/RelationSet/Spec 未再发现 eligible edge”，不表示完整程序语义。

每个 Slice frontier item 的 exact shape 固定为：

```text
from_fact_id
relation_id
direction = OUTBOUND / INBOUND
candidate_fact_id: SemanticDigest | null
candidate_depth: NonNegativeInteger
reason_codes[]: non-empty subset of
  DEPTH_LIMIT / SYMBOL_LIMIT / FILE_LIMIT / RELATION_LIMIT
```

`from_fact_id` 是本次展开队列中的 Fact；`relation_id` 必须来自同一 RelationSet；若候选另一端是 Fact，
`candidate_fact_id` 保存其 ID，否则 literal target 显式为 `null`。`candidate_depth` 是该 relation hop 若被
接受时的深度。frontier 按规范遍历中候选被拒绝的 encounter order 保存；相同
`(from_fact_id, relation_id, direction)` 只出现一次，`reason_codes` 按
`DEPTH_LIMIT < SYMBOL_LIMIT < FILE_LIMIT < RELATION_LIMIT` 排序且保存全部适用原因。

### 9.4 Slice Artifact

`review-slices.json` 固定字段：

```text
artifact_kind = REVIEW_SLICE_SET
schema_version
canonicalization_profile
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
fact_set_digest
relation_set_digest
slices[]
slice_set_digest
```

每个 Slice 固定：

```text
slice_id
slice_spec
included_fact_ids[]
included_relation_ids[]
frontier[]
coverage_status = COMPLETE / PARTIAL / UNKNOWN
```

Slice 数组按 `slice_id` 排序，成员 ID 去重排序。`slice_id` 覆盖 spec、成员与 frontier；同成员但不同 spec
仍是不同 Slice。CoverageLedger 不进入 Slice identity，避免循环。

精确投影固定为：

```text
slice_id
  domain  = veritrail.review.review-slice/0.1
  payload = {
    slice_spec_digest,
    included_fact_ids,
    included_relation_ids,
    frontier
  }

slice_set_digest
  domain  = veritrail.review.slice-set/0.1
  payload = {
    source_snapshot_digest,
    analysis_scope_digest,
    slice_policy_digest,
    derivation_profile_digest,
    fact_set_digest,
    relation_set_digest,
    slices
  }
```

`slice_spec` 必须包含与 `slice_spec_digest` 一致的完整 ReviewSliceSpec。`coverage_status` 是 frontier 与上游
可用性的机械派生字段：上游集合无法建立为 `UNKNOWN`；否则 frontier 非空为 `PARTIAL`；否则为
`COMPLETE`。它进入 `slice_set_digest`，但不重复进入 `slice_id`。

## 10. CoverageLedger 0.1

### 10.1 固定阶段

`coverage-ledger.json` 的 `stages` 必须按以下顺序恰好出现一次：

```text
SNAPSHOT_INVENTORY
POLICY_SCOPE
LANGUAGE_SUPPORT
PARSE
FACT_DERIVATION
RELATION_DERIVATION
SLICE_DERIVATION
```

每阶段固定：

```text
stage
upstream_stage | null
denominator
eligible[]: CoverageItemRef
completed[]: CoverageItemRef
out_of_scope[]: CoverageDisposition
unsupported[]: CoverageDisposition
unresolved[]: CoverageDisposition
conflicts[]: CoverageDisposition
parse_failed[]: CoverageDisposition
execution_failed[]: CoverageDisposition
truncated[]: CoverageDisposition
frontier[]
coverage_status
reason_codes[]
```

所有集合元素使用结构化 `CoverageItemRef`：

```text
item_kind = INVENTORY_ENTRY / PARSE_UNIT / FACT / RELATION / REVIEW_SLICE
item_id
```

不同 kind 的相同文本 ID 不是同一 item。

`item_id` 不是 Provider 自由生成的标签，映射固定为：

```text
INVENTORY_ENTRY -> inventory entry 的 git_path.git_path_hex
PARSE_UNIT      -> 对应 inventory entry 的 git_path.git_path_hex
FACT            -> candidate subject_key_digest
RELATION        -> candidate relation_subject_digest
REVIEW_SLICE    -> candidate slice_spec_digest
```

因此 path-backed ID 是非空小写偶数位 hex，subject-backed ID 是 `SemanticDigest`。Ledger 顶层已经绑定
Snapshot/Profile/Policy，`item_id` 不再复制这些上下文。输出 `fact_id / relation_id / slice_id` 必须能从同一
candidate subject 追溯，但不能替换上述 denominator identity。

`CoverageDisposition` 固定为：

```text
item_ref: CoverageItemRef
reason_codes[]
```

`reason_codes` 必须非空、唯一并按本节闭集 rank 排序。同一 `CoverageItemRef` 在同一 stage 的同一数组只出现
一次。

`eligible` 是通过当前 stage 入口判断的中间集合，不是与 `completed` 并列的最终 disposition。对已知分母：

```text
denominator
  = eligible U out_of_scope U unsupported

eligible
  = completed U unresolved U conflicts U parse_failed U execution_failed U truncated
```

两条等式右侧各集合分别互斥，所有比较都按 `CoverageItemRef` 身份进行。某 stage 不适用的分类必须为空，
不能省略字段或把同一 item 同时写进两个终态。

各 stage 的分母来源固定，不能由 Provider 为了提高覆盖率改小：

| Stage | Denominator source | Item kind |
| --- | --- | --- |
| `SNAPSHOT_INVENTORY` | exact analysis tree 的全部 terminal tracked entries | `INVENTORY_ENTRY` |
| `POLICY_SCOPE` | SourceSnapshot inventory | `INVENTORY_ENTRY` |
| `LANGUAGE_SUPPORT` | Policy 的 `IN_SCOPE` entries | `PARSE_UNIT` |
| `PARSE` | 当前 Profile 声明 supported 的 parse units | `PARSE_UNIT` |
| `FACT_DERIVATION` | 成功解析 AST 中按闭集可枚举的 Fact candidates | `FACT` |
| `RELATION_DERIVATION` | 规范 facts 中按闭集可枚举的 direct relation candidates | `RELATION` |
| `SLICE_DERIVATION` | Policy 机械选择出的 anchor/spec pairs | `REVIEW_SLICE` |

若任一上游失败使候选全集无法建立，下游 denominator 必须是 `UNKNOWN`；不得只用成功解析或已经派生出的
子集重新定义全局分母。`FACT/RELATION/REVIEW_SLICE` 的 denominator ID 是候选 subject identity，输出
Artifact ID 另由完整语义计算；二者必须通过 conformance 规则可追溯。

### 10.2 分母

已知分母：

```text
denominator = {
  state: KNOWN,
  source_digest,
  item_refs[]
}
```

未知分母：

```text
denominator = {
  state: UNKNOWN,
  source_digest | null,
  known_item_refs[],
  reason_codes[]
}
```

KNOWN denominator 的 `source_digest` 精确计算为：

```text
domain  = veritrail.review.coverage-denominator/0.1
payload = {stage, item_refs}
```

其中 `item_refs` 排序且唯一，并与 `denominator.item_refs` 逐项相同。R1 0.1 的 UNKNOWN denominator 必须
使用 `source_digest = null`；`known_item_refs` 只是排序唯一的已观察前缀。后继版本若要绑定独立的部分分母
证明，必须增加新字段或升级 Schema，不能让非空 `source_digest` 看起来像完整 denominator。

`UNKNOWN` 的 known items 只是已观察前缀，不能被重命名为全局分母。R1 0.1 不存百分比和冗余 count；
Workbench 从 exact item sets 计算显示值。对 `UNKNOWN`，上述集合关系只适用于 `known_item_refs`，同时
必须保留导致全局分母未知的原因；已知前缀完整不改变 overall UNKNOWN。

闭集 coverage reason：

```text
POLICY_EXCLUDED
UNCLASSIFIED_SOURCE
UNSUPPORTED_ENTRY_KIND
UNSUPPORTED_LANGUAGE
UNSUPPORTED_SOURCE_ENCODING
UNSUPPORTED_SYNTAX_VERSION
PARSE_ERROR
PROVIDER_UNAVAILABLE
PROVIDER_CONFLICT
TARGET_UNRESOLVED
TARGET_EXTERNAL_TO_SNAPSHOT
UPSTREAM_DENOMINATOR_UNKNOWN
DEPTH_LIMIT
SYMBOL_LIMIT
FILE_LIMIT
RELATION_LIMIT
DERIVATION_ERROR
```

reason 与 disposition 的合法映射固定为：

| Disposition / location | Allowed reason codes |
| --- | --- |
| `out_of_scope` | `POLICY_EXCLUDED` |
| `unsupported` | `UNCLASSIFIED_SOURCE / UNSUPPORTED_ENTRY_KIND / UNSUPPORTED_LANGUAGE / UNSUPPORTED_SOURCE_ENCODING / UNSUPPORTED_SYNTAX_VERSION` |
| `unresolved` | `TARGET_UNRESOLVED / TARGET_EXTERNAL_TO_SNAPSHOT` |
| `conflicts` | `PROVIDER_CONFLICT` |
| `parse_failed` | `PARSE_ERROR` |
| `execution_failed` | `PROVIDER_UNAVAILABLE / DERIVATION_ERROR` |
| `truncated` and Slice frontier | `DEPTH_LIMIT / SYMBOL_LIMIT / FILE_LIMIT / RELATION_LIMIT` |
| UNKNOWN denominator/stage reason | `UPSTREAM_DENOMINATOR_UNKNOWN` plus any already observed typed reason above |

不适用于该分类的 reason 必须拒绝；不能把未知原因塞入“最接近”的数组。

`coverage_status = COMPLETE / PARTIAL / UNKNOWN`。Python Profile 的 COMPLETE 不能显示成 repository
complete；混合语言与 Policy 排除仍须在前序 stage 分母可见。

stage-level `frontier` 只在 `SLICE_DERIVATION` 使用，其他六个 stage 必须为空。每项固定为：

```text
slice_id
frontier_item: exact Slice frontier item
```

数组按 `(slice_id, frontier encounter order)` 排列，且必须等于所有 normal ReviewSlice 的 frontier 并集；
它保留每个停止点属于哪个 Slice，不能只汇总 reason。`truncated` 则按 `REVIEW_SLICE + slice_spec_digest`
标识受边界影响的 candidate slice，并保存该 Slice frontier 的 reason union；两者一个回答“哪个候选未完整”，
一个回答“具体在哪条 edge 停止”，不能相互替代。

stage `reason_codes` 是该 stage 所有 disposition 与 frontier reason 的排序唯一并集。若 denominator 为
UNKNOWN，stage 状态必须是 `UNKNOWN`；否则任一非 completed terminal disposition 或非空 frontier 使状态为
`PARTIAL`；其余才是 `COMPLETE`。`eligible` 仍只是中间集合，不单独降低状态。

### 10.3 Ledger 身份

顶层固定：

```text
artifact_kind = COVERAGE_LEDGER
schema_version
canonicalization_profile
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
fact_set_digest
relation_set_digest
slice_set_digest
stages[]
overall_coverage_status
coverage_ledger_digest
```

摘要覆盖完整分母、分类、frontier 与状态，不覆盖 UI 派生百分比。`overall_coverage_status` 是固定 stage
状态的保守机械汇合：任一 UNKNOWN -> UNKNOWN；否则任一 PARTIAL -> PARTIAL；否则 COMPLETE。它不是
缺陷、质量或 Core Verdict。

精确摘要投影为：

```text
coverage_ledger_digest
  domain  = veritrail.review.coverage-ledger/0.1
  payload = CoverageLedger with coverage_ledger_digest removed
```

这会覆盖完整 `policy_digest`、七个 stage、每个 denominator、分类、frontier、reason 与最终机械汇合状态。

## 11. DerivationEvidence 与多来源组合

`derivation-evidence.json` 固定字段：

```text
artifact_kind = DERIVATION_EVIDENCE
schema_version
canonicalization_profile
derivation_id
request_provenance
source_snapshot_digest
policy_digest
analysis_scope_digest
slice_policy_digest
derivation_profile_digest
provider_runs[]
overall_execution_status
started_at
finished_at
diagnostics[]
derivation_evidence_digest
```

执行闭集：

```text
COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE
```

每个 Provider run 保存 capability、provider implementation/version、parser/runtime identity、实际操作数
摘要、起止、状态、reported fact/relation IDs 与 typed diagnostics。`provider_runs` 按 provider-run identity
排序，不能按完成先后排序。

`request_provenance` 固定：

```text
requested_repository_id
requested_ref
resolver_id
resolver_version
resolved_at
```

它记录 friendly coordinate 怎样被解析，不参加 SourceSnapshot content identity。

每个 Provider run 固定：

```text
provider_run_id
capability_id
provider_id
provider_version
parser_id
parser_version
runtime_id
runtime_version
operands_digest
started_at
finished_at
execution_status
reported_fact_ids[]
reported_relation_ids[]
diagnostics[]
```

`operands_digest` 不是无法复算的 Provider 私有 hash。精确投影为：

```text
domain  = veritrail.review.provider-operands/0.1
payload = {
  source_snapshot_digest,
  policy_digest,
  analysis_scope_digest,
  slice_policy_digest,
  derivation_profile_digest,
  capability_id,
  provider_id,
  provider_version,
  parser_id,
  parser_version,
  runtime_id,
  runtime_version
}
```

R1 0.1 不允许未封存的 Provider 参数影响正常派生。未来若 Provider 需要额外 execution operands，必须先把
它们加入版本化 Profile/Policy 或独立 Manifest 并升级本合同，不能只提交一个无法验证来源的摘要。

`provider_run_id` 精确计算为：

```text
domain  = veritrail.review.provider-run/0.1
payload = {derivation_id, capability_id, provider_id, operands_digest}
```

`derivation_id` 是调用方在 create-new output namespace 中生成的 opaque request-instance identity；不同
derivation 不得复用，同一次失败重试若重新发布新 Bundle 也必须获得新 ID。它不宣称是语义内容摘要。
同一 derivation 中 `(capability_id, provider_id)` 必须唯一；一次 Provider 只产生一个 run record，不用重试
次数刷新身份。内部重试属于该 run 的执行细节，不能伪装成多个独立来源。`execution_status` 使用与顶层相同
的 `COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE` 闭集；reported IDs 排序且唯一，成功空来源使用空数组。

每个 diagnostic 固定为 `diagnostic_code / subject_ref | null`。人类可变错误文本、本机绝对路径、stack
trace 和 locale 文本不进入 R1 0.1 规范 Artifact；如未来需要诊断 attachment，必须另开合同定义身份与
Manifest 布局，不能在首版塞入未绑定文件。

`subject_ref` 不是开放字符串，exact union 为：

```text
{ref_kind: ARTIFACT,
 artifact_role: SOURCE_SNAPSHOT / REVIEW_POLICY / DERIVATION_PROFILE,
 semantic_digest: SemanticDigest}

{ref_kind: PROVIDER_RUN,
 provider_run_id: SemanticDigest}

{ref_kind: COVERAGE_ITEM,
 item_ref: CoverageItemRef}
```

无法可靠绑定 subject 时必须显式为 `null`。diagnostics 按
`(diagnostic_code, canonical_json_bytes(subject_ref))` 排序且去重；Provider run 内的 diagnostics 必须能
绑定该 run 或其观察到的 item，顶层 diagnostics 可以汇总但不能添加自由文本。

diagnostic code 首版闭集：

```text
SOURCE_OBJECT_MISSING
SOURCE_CONTENT_MISMATCH
PROVIDER_UNAVAILABLE
PROVIDER_FAILED
NONCONFORMANT_PROVIDER_OUTPUT
EXECUTION_DEADLINE
EXECUTION_CANCELLED
INTERNAL_DERIVATION_ERROR
```

`overall_execution_status` 机械汇合：若整个操作因 deadline/cancellation 停止则 `INTERRUPTED`；否则任一
required Provider 执行或输出验证失败为 `FAILED`；否则任一 required Provider 不可用为 `UNAVAILABLE`；
其余为 `COMPLETED`。optional Provider 的失败仍保留 Evidence/Coverage，但不单独把整体改成
`UNAVAILABLE`；一旦其已报告内容与其他适用来源冲突，冲突不能因它 optional 而被删除。

`request_provenance` 可以保存最初 branch/tag alias 与解析时间，但后继所有语义 Artifact 只绑定 exact
Snapshot。时间使用 UTC RFC 3339；它属于该次 Evidence identity，不进入 Fact/Relation/Profile identity。

required source 的空输出是一个成功但为空的来源事实；required source 不可观察则
`overall_execution_status` 不能冒充完整成功，Coverage 也必须保留 UNKNOWN。多个 Provider 报告同一
`fact_id/relation_id` 时合并 content identity 并保留全部 provenance；同 subject 的不兼容内容进入 conflict，
不能 last-write-wins。

wall-clock timeout 产生 `INTERRUPTED`。此时不得发布普通完成态 FactSet、RelationSet、ReviewSliceSet 或
CoverageLedger；已观察前缀只能留在 typed diagnostics/Evidence 中，不能获得正常派生产物身份。

`request_provenance` 的五个字符串字段均为 `NonEmptyText`，`resolved_at` 与所有起止时间为
`UtcTimestamp`。`resolved_at <= started_at <= finished_at`；每个 Provider run 的 start/end 也有序并落在
该次 derivation 的起止区间内。
`provider_runs` 按 `provider_run_id` 排序；diagnostics 使用上述规范顺序。精确 Evidence 摘要为：

```text
derivation_evidence_digest
  domain  = veritrail.review.derivation-evidence/0.1
  payload = DerivationEvidence with derivation_evidence_digest removed
```

## 12. Artifact 布局与 Manifest

R1 产物是一个 create-new-only 目录。文件名固定，不接受 Manifest 提供任意相对路径：

```text
r1-artifact/
  manifest.json
  source-snapshot.json
  review-policy.json
  derivation-profile.json
  derivation-evidence.json
  fact-set.json
  relation-set.json
  review-slices.json
  coverage-ledger.json
```

### 12.1 公共 JSON Schema 文件集

Schema payload 使用 JSON Schema Draft 2020-12，文件集固定为：

```text
schemas/review-r1-common-0.1.schema.json
schemas/review-source-snapshot-0.1.schema.json
schemas/review-policy-0.1.schema.json
schemas/review-derivation-profile-0.1.schema.json
schemas/review-derivation-evidence-0.1.schema.json
schemas/review-fact-set-0.1.schema.json
schemas/review-relation-set-0.1.schema.json
schemas/review-slice-set-0.1.schema.json
schemas/review-coverage-ledger-0.1.schema.json
schemas/review-derivation-manifest-0.1.schema.json
```

九个 Artifact/Manifest root Schema 只能通过相对 `$ref` 消费同目录 common definitions，不得引用网络资源或
运行时包。每个 root Schema 的 `$id` 使用仓库公共 URL 与自身文件名，`additionalProperties: false` 递归应用
到所有闭合对象。common Schema 只提供已在本文冻结的结构原子，不能把跨文件引用、摘要复算、数组排序、
路径可逆性或 Coverage 集合方程伪装成 JSON Schema 已证明。

`manifest.json` 顶层固定：

```text
bundle_kind = R1_DERIVATION
schema_version = 0.1
canonicalization_profile = veritrail-json-c14n/1
outcome_kind = COMPLETE / DIAGNOSTIC
files[]
```

每项固定：

```text
role
path
sha256
size_bytes
semantic_digest
```

role 与 path 是闭合一一映射；数组按以下 rank 排序：

```text
SOURCE_SNAPSHOT      -> source-snapshot.json
REVIEW_POLICY        -> review-policy.json
DERIVATION_PROFILE   -> derivation-profile.json
DERIVATION_EVIDENCE  -> derivation-evidence.json
FACT_SET             -> fact-set.json
RELATION_SET         -> relation-set.json
REVIEW_SLICE_SET     -> review-slices.json
COVERAGE_LEDGER      -> coverage-ledger.json
```

`semantic_digest` 分别绑定各文件的
`source_snapshot_digest / policy_digest / profile_digest / derivation_evidence_digest /
fact_set_digest / relation_set_digest / slice_set_digest / coverage_ledger_digest`，不能用文件 SHA-256 代替。
Manifest importer 必须先安全读取一次文件、验证 exact bytes 与 semantic digest，再把同一已读取文档交给
后继消费者；禁止 `verify(path) -> reread(path)`。

`COMPLETE` 必须包含八个 role，且 Evidence execution 是 `COMPLETED`；parse failure、unsupported entry 或
结构预算截断仍可产生 COMPLETE bundle，但 Coverage 必须诚实为 PARTIAL/UNKNOWN。这里的 COMPLETE 只指
派生协议完整结束，不是 coverage complete 或 Core PASS。

`DIAGNOSTIC` 必须包含 Snapshot、Policy、Profile 与 Evidence；Policy 已绑定 Snapshot，因此缺少
Snapshot 的目录本身无效。它禁止包含正常态 Fact/Relation/Slice/Coverage 文件。
`INTERRUPTED / FAILED / UNAVAILABLE` 只能发布 DIAGNOSTIC；若连 SourceSnapshot 都不能完整建立，R1
derivation 尚未取得合法输入，不发布伪造的 R1 Bundle，只保留调用层诊断。

Manifest 自身不包含自摘要；调用方以 exact `manifest.json` 文件 SHA-256 绑定 Bundle。发布必须先在隔离
staging 中完成所有文件写入、复算与 cross-reference 校验，再原子 create-new 到最终目录；失败不能留下
可被误读为完整 Bundle 的半目录。

## 13. 兼容向量矩阵

后继实际 Schema payload 必须同时提交纯数据向量及 expected canonical bytes/digests。至少覆盖：

1. repository root 只接受专用对象，空字符串、`.`、`/` 均拒绝；
2. NFC/NFD、大小写不同与 invalid UTF-8 Git path 的 hex round-trip 保持不同身份；
3. path 中 LF 可逆，NUL、空段、`.`、`..`、首尾 `/` 拒绝；
4. 两个 commit 指向同一 tree：content digest 相同，coordinate/snapshot digest 不同；
5. branch alias 在 resolve 后移动，不改变已建 Snapshot；
6. mutable path 在 hash 后替换，派生仍消费已核验 bytes 或明确失败；
7. UTF-8、UTF-8-SIG、LF/CRLF/CR、多字节 identifier 的 raw byte anchor；
8. 非 UTF-8 coding declaration 进入 UNSUPPORTED，不冒充 PARSE_FAILED；
9. Python 3.13-only syntax 在 PYTHON_3_10 Profile 下有类型拒绝；
10. 一个 import statement 的多个 alias 通过 ordinal 得到不同 Fact；
11. Provider A/B 各报告不同事实时累计；A 为空不取消 B；同一事实汇总 provenance；
12. 同 subject 不兼容 facts/relations 形成 conflict，不 last-write-wins；
13. BFS 在 cycle、同深度多边和不同输入顺序下输出相同成员与摘要；
14. depth/symbol/file/relation 每个预算分别命中端点，并保留完整 frontier；
15. overlap Slice 以唯一 ID 计 coverage，不按出现次数重复计数；
16. parse failure、unsupported language、unknown denominator 与 deterministic truncation 保持不同状态；
17. `INTERRUPTED` 不能携带完成态派生文件；
18. Manifest 缺文件、多文件、错 role/path、摘要不符、非规范字节或半发布目录全部拒绝；
19. 同一向量在 CPython 3.10/3.13、normal/`-O` 下得到逐字节相同规范 Artifact 与语义摘要；
20. 冻结 reference lab 的 22 个普通 Python blob 与 259,553 bytes 能由 Snapshot inventory 重新复算。

向量必须共享事实，不共享实现：未来任意兼容 Provider/validator 都读取同一 corpus。不得把 expected digest
在被测实现运行后动态生成；expected bytes 与摘要必须作为审查过的不可变 fixture 提交。

冻结 Corpus 的追溯关系固定为：

| Pattern | 本合同约束 | 主要向量 |
| --- | --- | --- |
| `RA-003` | required sources 累计、空来源不抵消、冲突和 provenance 保留 | 11–12 |
| `RA-004` | denominator 不缩小、inclusive budget、frontier、PARTIAL/UNKNOWN | 13–16 |
| `RA-008` | alias 只解析一次，后继只绑定 exact coordinate/Snapshot | 4–5 |
| `RA-023` | verified bytes 与 parser/consumer bytes 连续，Manifest 单次安全读取 | 6、18 |

## 14. 首个实现切片仍未开始

本文冻结后，下一阶段仍只允许先创建：

```text
versioned JSON Schemas
data-only compatibility corpus
canonical-byte and digest vectors
schema/conformance validation tests
```

该阶段不得顺手加入 Git reader、SourceSnapshot importer、Python parser、Fact mapper、Slice engine 或 CLI。
实际 R1 运行实现必须等待 Schema payload 自身完成门禁、受保护主线合入、exact-main 复算、匿名读回与后继
状态发布。

未来运行实现的第一条 vertical slice 才是：

```text
exact Git commit/tree/root
    -> binary-safe terminal inventory
    -> verified SourceSnapshot 0.1
    -> canonical artifact + manifest
```

它只证明快照身份和连续性，不提前宣称 Python Facts、Relations、Slices 或 Coverage 已实现。

## 15. 候选验收门

本文只有满足以下条件后才有资格冻结：

1. 与文档 113、R0、Corpus、README、AGENTS、R 轨 Plan 和 milestones 不存在竞争语义；
2. 路径、锚、事实、关系、切片、coverage、Evidence 与 Bundle 身份均能独立解释；
3. `Same Path / Snapshot / Fact / Evidence / File` 没有被折叠为一个摘要；
4. JSON Schema 能力上限与后继 conformance validator 职责明确分开；
5. 结构预算 inclusive 规则、BFS tie-break、cycle 去重与 frontier 端点没有实现自由度；
6. Python 3.10 Profile 不随宿主解释器、source encoding 或混合语言仓库偷偷扩大；
7. 兼容向量覆盖冻结 Pattern `RA-003 / RA-004 / RA-008 / RA-023` 的反例；
8. diff 只包含本文与状态入口文档，不出现实际 Schema、源码、CLI、Provider、运行 CI、标签或 Release；
9. 候选经原始远端门禁、受保护主线合入、exact-main 门禁及 README/本文/milestones 匿名读回；
10. 后继独立 docs-only 状态发布完成同样闭环后，才允许写：

```text
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED
R1_IMPLEMENTATION_NOT_STARTED
```

若 Schema 审查发现本文与已冻结 R1 合同冲突，必须停止并只重开被反例击穿的边界。门禁全绿不能覆盖
语义反例。

## 16. 当前修正候选事实

Schema payload preflight 从已发布的 `main@824d50617320d3fe1aecd1e752e4c4f9224257c2` 发现：原合同虽已列出
顶层字段，但 `scope_decisions` 的 path key、Coverage item/denominator identity、Slice/Coverage frontier、
Provider run provenance、typed diagnostic reference 及若干 semantic digest 精确投影仍需由实现猜测。
因此 payload 分支保持零改动，本补丁只重开这些被反例击穿的 Schema/identity 边界。

它没有生成可被程序导入的 Schema，没有修改 Core/P/Q，没有开始 R1 运行实现，也没有把未来兼容向量写成
已经通过的证据。

当前状态保持：

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE
R1_SCHEMA_PAYLOAD_BLOCKED
R1_IMPLEMENTATION_NOT_STARTED
```

## 17. 规范依据

- [Git `ls-tree`](https://git-scm.com/docs/git-ls-tree.html)：`-z` 以 NUL 分隔并原样输出 path；
- [Git `fast-import`](https://git-scm.com/docs/git-fast-import.html)：canonical path、原始字节、根路径与 NUL
  约束；
- [Python 3.10 `ast`](https://docs.python.org/3.10/library/ast.html)：AST 行列与 UTF-8 byte offset 端点；
- [Python 3.10 lexical analysis](https://docs.python.org/3.10/reference/lexical_analysis.html)：source encoding、
  BOM 与物理换行语义。

这些外部文档限制 R1 对 Git/Python 的观察模型，但不替代本合同的项目身份与停止线。
