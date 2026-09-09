# Review Attention Pattern Corpus 冻结合同 0.1

> 状态：`CORPUS_CONTRACT_CANDIDATE / LEDGER_CAUGHT_UP_THROUGH_P4 / CORPUS_NOT_SELECTED / R1_BLOCKED`
>
> 精确基线：`main@b2dae28fea70abe6e1bfa1066dbb1ddc4ff9c292`
>
> 影响层级：`L2_CONTRACT + L0_DOCUMENTATION`；只定义 Ledger 到首个 Corpus 的选择与冻结闭环，不创建
> Review Attention 源码、Schema、CLI、Provider、CI、标签或 Release

## 1. 目的与停止线

P4 已经冻结，只解除 R1 的发布前置门。R1 仍必须等待一个可复算、非自指、按精确记录摘要选择的
Pattern Corpus。Corpus 不是“所有历史坑的集合”，也不是缺陷真值库；它只是 R1 首个确定性语义切片实验
允许引用的有界反例知识快照。

本合同成立前后均保持：

```text
Ledger remains append-only/open
Corpus is an exact selected snapshot
pattern match is not a defect verdict
R1 remains not started until final public readback
```

## 2. 输入边界

候选输入只有 [Review Pattern Ledger 0.2](87-review-pattern-ledger.md) 中满足以下条件的 revision：

1. 是包含完整 Schema 字段的 JSON PatternRecord，不是人类可读 seed 表行；
2. `record_digest` 能以 `veritrail-json-c14n/1` 从删除自身字段后的完整记录复算；
3. revision 链严格递增，`supersedes_digest` 指向唯一前序链头，没有分叉、缺链或重复链头；
4. `problem_layer` 与 `pattern_class` 符合冻结分类边界；
5. `source_coordinate`、最小反例、误报条件、所需证据与 `non_claim` 均非空；
6. 状态是明确提升后的 `CONTRACT_CANDIDATE`；仅 `OBSERVED / GENERALIZED / REJECTED` 的 revision
   不能被最终 manifest 静默选择。

RA-001–RA-016 目前只是冻结 seed 的人类投影。只有实际入选的 seed 才需要先追加完整不可变 revision；
未入选不等于被证伪，也不允许为凑数量机械物化。P2–P4 已经形成完整 revision 的记录与本次补账记录
同样必须逐条经过选择审查，不能因为较新就自动入选。

## 3. 选择标准

首个 Corpus 只选择能够直接约束 R1 四项边界的最小充分集合：

```text
SourceSnapshot identity and provenance
deterministic semantic inventory / relation derivation
bounded overlapping Semantic Review Slices
coverage and truncation ledger
```

选择记录必须同时满足：

- 对上述至少一个边界存在明确适用性；
- 最小反例能转写为未来数据型 conformance fixture 或审查问题；
- 与已选记录相比提供不同的失败机制，不能只换项目名重复同一模式；
- 不要求 R1 引入 AI 推理、风险排序、HumanDisposition、Core handoff、网络访问或自动修复；
- 不把一次环境偶发、外部平台内部根因猜测或未复现印象冻结成通用模式。

数量不是出口。若较小集合已经覆盖 R1 的身份、关系、切片与 coverage 风险，剩余 Ledger 继续开放，不因
未入选而丢失。

## 4. 非自指冻结序列

Corpus 身份必须分两次受保护主线事实建立，禁止让 manifest 或状态页声明自身尚未确定的 commit/digest：

```text
A. candidate revisions
   GENERALIZED/seed projection
       -> append CONTRACT_CANDIDATE successor revisions
       -> independent digest/revision/conformance audit

B. corpus payload
   selected candidates
       -> append FROZEN_PATTERN successor revisions
       -> create corpus manifest selecting exact
          pattern_id + selected_record_digest
       -> protected merge at exact corpus source commit C

C. closure publication
   read C from protected main
       -> recompute manifest digest and every selected record digest
       -> record C + manifest digest in a later status document
       -> protected merge
       -> anonymous exact-SHA README/contract/manifest readback
```

`FROZEN_PATTERN` revision 与 manifest 可以在同一 corpus payload commit 中共同出现；最终身份由后继状态
文档绑定该 payload 合入后的 exact source commit `C`。状态文档自己的 commit 不冒充 Corpus source
commit。

## 5. Manifest 0.1

Manifest 是纯数据 JSON，固定字段为：

```text
schema_version
corpus_id
record_canonicalization
taxonomy_version
selection_policy_version
entries[]
```

`entries` 必须按 `pattern_id` Unicode code-point 升序排列，每项只含：

```text
pattern_id
selected_record_digest
record_revision
problem_layer
pattern_class
```

Manifest 不包含：

```text
manifest_digest
its own git commit
latest ledger head
human verdict
defect truth
provider score
runtime timestamp
```

Manifest SHA-256 以 UTF-8、无 BOM、LF、文件完整字节计算，并由 closure 状态文档外部绑定。Manifest 中的
摘要只定位 PatternRecord，不复制记录正文；阅读者必须在 exact Corpus source commit 中按 digest 解析。

## 6. 必需负例与复算门

冻结前至少证明：

1. 任一 PatternRecord 摘要不符、缺字段、链断裂、revision 倒退或并发 successor 分叉都会拒绝；
2. seed 表行、`GENERALIZED` 记录和 `REJECTED` 记录不能直接进入最终 manifest；
3. 重复 `pattern_id`、重复 digest、未排序 entry、未知 taxonomy/canonicalization 会拒绝；
4. Manifest 不依赖本机绝对路径、采集时间、当前 HEAD 或网络状态；
5. 修改未选 Ledger 记录不会改变既有 Corpus identity；修改已选 revision 任一语义字段必然破坏摘要；
6. 同一 payload 在双 Python normal/`-O` 下得到相同记录摘要、manifest 字节与 manifest 摘要；
7. R1 入口必须读取 closure 中的 exact Corpus source commit 和 manifest digest；缺任一坐标、读回不一致
   或匿名页面未建立证据时继续 `R1_BLOCKED`；
8. 全仓既有 Core、P1–P4 与 Workbench 门禁保持成立，且本合同不新增运行时代码。

## 7. 选择与权威

机器可以生成候选对照表、复算摘要和指出重复/缺口，但不能自行宣布某模式为缺陷，也不能因为命中次数
高就获得选择权。Corpus 选择属于本项目在已冻结 R1 范围内的合同决定；它不等于 HumanDisposition，
更不等于 Core Verdict。

```text
Ledger records what was learned.
Corpus selects what R1 may rely on.
R1 proposes where to look.
Human authority still decides what it means.
```

## 8. 当前候选事实

本补丁只做两件事：

1. 把 P2–P4 已保留但尚未物化的六条真实模式追加为 `RA-022` 至 `RA-027` 的 `GENERALIZED rev1`；
2. 冻结候选选择方法、manifest 语义、非自指提交顺序与 R1 停止线。

它没有选择最终集合，没有追加 `CONTRACT_CANDIDATE/FROZEN_PATTERN` successor，没有生成 manifest，
也没有启动 R1。候选合同自己的原始门禁、受保护主线合入与合入后 exact-main 匿名读回未全部成立前，
不得把 `CORPUS_CONTRACT_CANDIDATE` 提升为冻结事实。
