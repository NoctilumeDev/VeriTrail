# R1 Schema payload 前置审计与合同修正候选

> 状态：`R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE / R1_SCHEMA_PAYLOAD_BLOCKED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@824d50617320d3fe1aecd1e752e4c4f9224257c2`
>
> 规范对象：[R1 Schema 与规范身份合同 0.1](120-r1-schema-and-canonical-identity-contract.md)
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；不创建 JSON Schema、compatibility corpus、运行源码、
> CLI、Provider、标签或 Release

## 1. 为什么 payload 没有开始

文档 121 已经合法发布 `R1_SCHEMA_CONTRACT_FROZEN / R1_SCHEMA_PAYLOAD_DRAFTING_ALLOWED`。后继从该 exact
main 创建了独立 payload worktree，但在第一份 Schema 写入前先执行了一个更窄的问题：

> 一个不知道实现代码的 Schema 作者，能否只靠冻结合同唯一写出所有闭合对象、引用和摘要投影？

答案是否定的。原合同正确区分了 Artifact、身份域、canonical bytes 与 conformance 职责，但若干嵌套对象
只列出了名字，没有冻结“它如何指认对象”或“它究竟被 hash 成什么”。继续施工会使 Schema 作者获得未被
授权的语义决定权。

因此原 payload branch 保持零改动。当前不是运行实现失败，而是 payload preflight 发现合同不足：

```text
Schema contract published
        ↓
payload preflight
        ↓
field vocabulary exists
but several identities are not uniquely constructible
        ↓
STOP payload
        ↓
reopen only the underspecified schema/identity boundary
```

## 2. 最小反例

### 2.1 Scope decision 没有 item key

原合同要求 `scope_decisions` 对每个 terminal inventory entry 恰好出现一次，却只列：

```text
disposition
source_class
reason_code
```

两条不同路径可以产生完全相同的三个值。没有 `git_path`，validator 无法证明某个 decision 属于哪个 entry，
也无法证明分母没有漏项或重复。

### 2.2 Coverage item 只有名字，没有跨阶段身份规则

`CoverageItemRef` 有 `item_kind / item_id`，但原合同没有规定 inventory、parse unit、Fact candidate、Relation
candidate 与 Slice candidate 各自如何得到 `item_id`。两个实现可以分别使用 path、artifact ID 或随机 UUID，
并都声称满足字段形状。这样 Coverage denominator 无法跨实现复算。

### 2.3 Frontier 能被写成互不兼容的对象

原合同要求所有预算停止点进入 `frontier[]`，却没有给出 frontier item 的字段。只保留 reason、只保留
relation ID 或复制整条 relation 都符合原文字面，但三者拥有不同 canonical bytes 和 Slice identity。

### 2.4 Provenance 引用没有被引用对象身份

Fact/Relation 使用 `provenance_refs[]`，DerivationEvidence 使用 `provider_run_id`，但原合同没有定义 run ID
投影。若 ID 由完成时间、数组序号或 Provider 自报字符串决定，相同运行语义会产生不可比较 provenance；
若多个 run 复用一个 ID，又会把独立来源错误合并。

### 2.5 Digest 说明仍不足以生成兼容向量

原合同已经描述 Fact/Relation/Slice/Set/Evidence digest 的职责，但部分位置没有给出完整 payload object。
兼容向量若由 payload 作者自行选择冗余字段、provenance 或 derived status 是否入 hash，会把“expected digest”
变成某个实现的私有答案。

### 2.6 Conflict 被保存了，但没有遍历边界

FactSet/RelationSet 能表达 conflict，原合同却没有说明冲突 candidate 是否可成为 Slice anchor/edge。跳过、
任选一个或遍历全部都会产生不同 Slice。首版采用保守规则：保留冲突事实，不解释冲突图，Slice stage 保持
UNKNOWN；后继局部 conflict isolation 必须另开合同。

## 3. 本修正只补什么

文档 120 的修正候选只增加以下确定性：

1. 公共 JSON scalar、版本、时间与 Seal 形状；
2. `git_mode` 的规范表示、已知 mode 映射与 BLOB content 条件；
3. `scope_decisions.git_path` 及 Policy 内数组唯一性/排序；
4. Fact/Relation 的 exact attributes、subject/content digest projection 与 provenance reference；
5. ReviewSliceSpec、Slice frontier、Slice/SliceSet digest projection；
6. Coverage item identity、known denominator digest、typed disposition/reason、stage frontier 与 Ledger digest；
7. Provider operands、provider-run identity、typed diagnostic subject reference 与 Evidence digest；
8. 十个固定、可离线解析的 Draft 2020-12 Schema 文件坐标。

这些都是原有对象成为可编码合同所必需的形状或身份，不增加新的产品能力。

## 4. 明确不补什么

```text
no Git reader
no SourceSnapshot importer
no Python parser or AST mapper
no Fact/Relation producer
no BFS or Slice engine
no Coverage producer
no runtime conformance validator
no CLI or Provider discovery
no AI proposal, ranking, HumanDisposition or Core Verdict
no tag or Release
```

compatibility corpus、canonical byte vector 和 Schema tests 也不属于本补丁。它们继续被阻塞，直到修正合同
重新完成受保护主线、exact-main 门禁、匿名公开读回与独立状态发布。

## 5. Authority 没有变化

```text
Human Seal authority
    owns ReviewPolicy and scope decisions

Schema
    constrains document shape

Conformance validator (future)
    recomputes ordering, identity, references and set equations

Provider runtime (future)
    reports deterministic candidates and provenance

Review Attention Core (future)
    composes artifacts without producing human disposition
```

Schema 仍不能证明路径可逆、摘要正确、遍历完整、Coverage 分母真实或源码没有缺陷。修正没有把
`Schema-valid` 偷换成 `semantically conformant`。

## 6. 候选验收门

本修正只有满足以下条件才可合入：

1. 所有改动均为文档，原 payload branch 保持零改动；
2. 每个新增字段或 domain 都能追溯到一个已存在但不可编码的 R1 对象；
3. 文档 113 的 SourceSnapshot -> Facts -> Relations -> Slices -> Coverage 单向关系不变；
4. Pattern Corpus、P/Q/Core 合同、Verdict 与 Human authority 不变；
5. `git diff --check`、链接、敏感信息和完整双 Python normal/`-O` 门禁通过；
6. 候选经原始 Public CI、受保护主线合入与 exact-main gates；
7. README、文档 120、本文和 milestones 完成匿名 exact-SHA public render readback；
8. 后继独立 docs-only 状态发布再次完成同样闭环后，才恢复 payload drafting authorization。

任何新反例都可否决本次修正。已有 PR #102、exact-main 全绿和匿名读回证明的是上一版合同确实被发布，
不能证明它已经足以唯一生成 Schema payload。

## 7. 本地候选证据

第一次 Python 3.10 normal 回归只把 Core `src` 放入 import coordinate，漏掉当前 worktree 的
`plugins/github-evidence/src`。测试源来自本 worktree，但 P4 辅助模块无法导入；该次在 409 项后以
`ModuleNotFoundError` 停止，只证明测试环境绑定错误，不构成产品失败或成功证据。

重新把 Core、GitHub plugin 与 test root 全部绑定到同一 worktree 后，候选完成：

```text
Python 3.10 normal  419/419
Python 3.10 -O      419/419
Python 3.13 normal  419/419
Python 3.13 -O      419/419
```

`git diff --check`、changed/untracked Markdown links、敏感信息扫描和 docs-only scope 也通过。以上仍只是本地
候选证据，不能替代原始远端门禁、受保护主线合入、exact-main 复验或匿名公开读回。

## 8. 当前裁决

```text
R1_CONTRACT_FROZEN
R1_SCHEMA_CONTRACT_CORRECTION_CANDIDATE
R1_SCHEMA_PAYLOAD_BLOCKED
R1_IMPLEMENTATION_NOT_STARTED
```

这不是撤销文档 121 的历史事实。文档 121 仍诚实记录上一版冻结曾经成立；本文记录后继 preflight 用新
反例更新了当前结论。冻结不是免检权，payload 也不能用实现便利覆盖合同缺口。
