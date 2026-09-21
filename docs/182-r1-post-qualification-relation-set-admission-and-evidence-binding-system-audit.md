# R1 RelationSet Admission / Qualification Evidence Binding 系统审计

> 状态：`R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_CANDIDATE /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@de0fdc6f01e1c99ae74259abd77640ad39d28038`
>
> 审计闭合基线：`main@1ffc4494dbbb61a056dcc8beed2530e7313f6116`
>
> 后继候选：[RelationSet Admission / Explicit Admission Witness / Public Qualification Binding 最小合同](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
>
> 冻结输入：[Relation Observation / Composition Qualification 实现冻结发布](179-r1-relation-observation-composition-qualification-freeze-publication.md)
>
> 影响层级：`L0_DOCUMENTATION / SYSTEM_AUDIT_ONLY`；本文不创建或修改 Schema、corpus、identity vector、
> runtime、测试、Provider、parser、RelationSet、DerivationEvidence、Manifest、publisher、Slice、Coverage、
> CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. 审计问题与停止线

文档 179 已冻结 private Relation observation/composition qualification，并明确要求从新的 exact main 先做
系统审计。本文只回答：

> private qualification 已经能够证明 bounded observation obligations 闭合以后，哪一条尚未闭合的 authority
> seam 会阻止 Relation candidates 成为可由完整 Bundle 对外复核的 RelationSet？

本轮不按路线图直接实现 RelationSet，也不因为公共 Schema 已有 `relation-set.json` shape 就补写文件。
`Slice / Coverage / Attention` 继续位于停止线之外。

## 2. 已冻结事实重新分层

当前运行时与公共合同共同给出以下五层：

```text
Relation ProviderRun terminal
    -> run-local execution fact

ObservationOutcome / Receipt
    -> per-item responsibility fulfillment accounting

Composition Qualification
    -> exact bounded obligations closed + deterministic candidate composition

RelationSet admission
    -> which qualified candidates/conflicts become stable Artifact members

Admission witness / public qualification binding
    -> which exact qualification history authorized which admitted RelationSet

Final Evidence / complete Bundle
    -> where that witness is represented and which exact public bytes a third party can verify
```

前三层已在 private closed proof 中冻结。后三层尚未实现。继续成立：

```text
Provider COMPLETED       != observation closure
Qualification QUALIFIED  != RelationSet admission
Schema-valid RelationSet != qualified bounded Relation view
RelationSet membership   != final Evidence/publication authority
```

## 3. 公共对象当前能证明到哪里

### 3.1 RelationSet 0.1

`RelationSet 0.1` 保存 exact input digests、Relations、conflicts、provenance refs 与
`relation_set_digest`。该 semantic digest 有意排除 Provider provenance；同一结构语义可由不同合法来源观察，
不应仅因运行历史不同就获得不同 content identity。

它不保存：

```text
observation_domain_digest
provider responsibility table
per-item ObservationOutcome / Receipt
required observation closure
qualification_status / qualification_digest
```

### 3.2 DerivationEvidence 0.1.1

`DerivationEvidence 0.1.1` 保存 attempt、ProviderRuns、terminal status、reported Fact/Relation IDs 与 typed
诊断。它不能重建 observation obligations、receipts 或 qualification。历史 `0.1.1` bytes 已冻结，不能原位
加字段。Evidence 已持有 attempt facts，不等于它天然拥有 RelationSet admission authority；存放或绑定
admission witness 的位置，与定义 witness 证明什么，是两个独立问题。

### 3.3 Manifest 0.1

`Manifest 0.1` 的 `COMPLETE` file set 固定为八个角色。它绑定每个 Artifact 的 exact file bytes 与 semantic
identity，但不替子 Artifact 决定自己的 Schema patch version，也不裁决子 Artifact 是否满足 admission 条件。
既有 Evidence `0.1 -> 0.1.1` 修正已经冻结：

```text
Artifact Schema version != Manifest Schema version
Schema validity         != cross-object derivation conformance
```

因此“需要公开 qualification”不自动推出第九种 Artifact role 或 Manifest shape 升级。

### 3.4 下游只继承 RelationSet identity

`ReviewSliceSet 0.1` 与 `CoverageLedger 0.1` 都直接引用 `relation_set_digest`，没有独立的 qualification /
admission binding。总合同又已禁止把 timeout、缺少必需 Provider 或未知上游分母产生的偶然 prefix 发布成
正常完成的 FactSet、RelationSet、ReviewSlice 或 CoverageLedger。因此 admission gap 不能留给 Slice 或
Coverage 补救：一旦未取得资格的 set 被当成稳定上游，下游只会继承它的 content identity，看不到缺失的
authority history。

## 4. exact-main 本地最小反例

### 4.1 反例构造

审计在仓库外的临时脚本中只读复用当前 closed fixture、Provider 与 application；没有修改仓库源码或测试。
两次运行使用同一 exact inputs 与同一 `derivation_id = rq-positive`：

```text
Q: A/B outcomes 完整
   -> observation closure COMPLETE
   -> composition CONSISTENT
   -> qualification QUALIFIED

U: 只从 Provider B terminal 删除一个 ObservationOutcome
   -> 原 canonical Relation candidates 保持不变
   -> observation closure INCOMPLETE
   -> composition NOT_COMPOSED
   -> qualification NOT_QUALIFIED
```

该 mutation 是未来 admission 的单变量 falsifier，不是当前产品缺陷。现有 application 正确地保留 U 的
run-local candidate history，同时把 `merged_candidates` 清空并拒绝 qualification。

### 4.2 H1 / H2 / H3 identity matrix

为避免把“相同语义”误写成“相同文件”，审计又在同一 frozen inputs 上加入第二个独立合格 attempt：

```text
H1: rq-positive
    QUALIFIED

H2: rq-independent-qualified
    QUALIFIED
    与 H1 使用不同 derivation / ProviderRun / receipt / qualification identity

H3: rq-positive
    删除一个 Provider B outcome
    NOT_QUALIFIED
    raw phase candidates 保持不变
```

CPython 3.10 与 3.13 得到相同 identity matrix：

当前没有 RelationSet assembler；下表涉及 RelationSet 文件的比较均由仓库外审计脚本按现有 Schema identity
规则构造，是 counterfactual projection，不是 runtime 已生成或发布的 Artifact。

| 比较 | 结果 | 解释 |
| --- | --- | --- |
| H1 / H2 Relation IDs | 相同 | relation semantic identity 稳定 |
| H1 / H2 semantic candidate projection | 相同 | 排除 `provenance_refs` 后语义相同 |
| H1 / H2 `relation_set_digest` | 相同 | content identity 不因合法运行历史改变 |
| H1 / H2 counterfactual RelationSet canonical file bytes | **不同** | `provenance_refs` 保留各自 ProviderRun identity |
| H1 / H3 raw phase projection | 相同 | outcome omission 没有改变 Provider 原始 candidates |
| H1 / H3 counterfactual RelationSet bytes | **相同** | 只有错误 assembler 绕过 H3 qualification 时才可能形成 |

共同 semantic projection SHA-256：

```text
1676d64f480d304e2f7b114fdd4914c97982a4e487ddad28d8f57227033a2f4b
```

共同 `relation_set_digest`：

```text
9be261a89ffa32d328357590567cdc1050b9158979b81f2a24f2c3fe6c5c4749
```

H1 / H3 counterfactual canonical RelationSet JSON SHA-256：

```text
7fc3fbad405051b17fab90fad7f0160c9fbf295ba6bf2dffd9f858489cc3e9c4
```

H2 canonical RelationSet JSON SHA-256：

```text
b9681ebe3acf0e0a3b264935afb702df077aa17a0740cd07061b6a28c28ecab4
```

因此草稿命题必须收紧为：

> same semantic RelationSet does not inherit admission authority; independent qualified attempts may share content
> identity while retaining different provenance bytes, and a bad assembler can still make a qualified and an
> unqualified history project to identical Schema-valid RelationSet bytes.

### 4.3 qualification 单变量结果

H1 与 H3 的 raw phase candidate/conflict canonical projection 完全相同：

```text
candidate projection SHA-256:
8180ec9d8a0fc48636d0ac68f36645ec22e097165a1ced28a6b9c98b78709f30

relation IDs:
4e42c7e39960bd9e247da522260afbcd36aa9df49e5d4ac5f9fad6d927df02d2
9872c294f8e9c15128867029ec9fd5845b3ce6cc1220aa8f5cc036605abccdc1
```

H1：

```text
qualification_digest = 8c5fb7b038980920a2fedcf1010c8fc1cb9e8b6103486d308584075b6f173faa
status               = QUALIFIED / COMPLETE / CONSISTENT
```

H3：

```text
qualification_digest = 5fdbe8ea510bf428131eead3a47a4d337b32d95f6fee321c533fca8643c503e0
status               = NOT_QUALIFIED / INCOMPLETE / NOT_COMPOSED
merged candidates    = []
reason codes         = OBSERVATION_OUTCOME_MISSING / UNEXPECTED_RELATION_CANDIDATE
```

如果一个未来 assembler 错误绕过 H3 的 qualification status，直接从 raw phase candidates 构造
`RelationSet 0.1`，现有 Schema 会接受该文档：

```text
relation_set_digest = 9be261a89ffa32d328357590567cdc1050b9158979b81f2a24f2c3fe6c5c4749
canonical JSON SHA-256 = 7fc3fbad405051b17fab90fad7f0160c9fbf295ba6bf2dffd9f858489cc3e9c4
Schema validation = ACCEPT
```

这不授权 H3 admission，也不声称当前代码存在该 assembler。它只证明：

> current public RelationSet shape cannot distinguish a qualified projection from the same candidate content copied
> around qualification.

### 4.4 绑定能力 probe

在内存副本上追加单一候选绑定，当前 closed Schema 均 fail closed：

| Probe | 当前结果 |
| --- | --- |
| `RelationSet 0.1 + qualification_digest` | root additional property，reject |
| `DerivationEvidence 0.1.1 + relation_qualification_digest` | root additional property，reject |
| `COMPLETE Manifest 0.1 + ninth RELATION_QUALIFICATION file` | exact eight-file/closed role，reject |

这只证明当前版本不能原位承载绑定；它不预先选择字段名、Semantic Digest 投影或第九文件方案。尤其是，
“Evidence 增加一个 qualification digest”只提供存储位置候选，不会自动定义 admission witness 的语义、
构造权与跨对象验证规则。

### 4.5 跨运行时复算

CPython 3.10 与 3.13 对上述完整审计报告产生相同 2753 bytes：

```text
sha256_json = d798d8df88d6a6b3ebfbcc6fe14ef0edb3a36d699f0df0538a41fa884416fd5a
```

本地输出位于仓库外临时审计目录，不是产品 Artifact、冻结 corpus 或发布 Evidence。

H1/H2/H3 identity matrix 在 CPython 3.10 与 3.13 也逐字节相同：

```text
sha256_json = c1c310834ba98947269c637ac83852633a9c2c77372d89850bb47d78f776d3d8
```

与反例直接相关的 `test_relation_observation_qualification.py + test_review_r1_schema_payload.py` 在同一
候选字节上完成四格复核：

| Python | normal | `-O` |
| --- | ---: | ---: |
| CPython 3.10 | `39/39` | `39/39` |
| CPython 3.13 | `39/39` | `39/39` |

该结果证明冻结 qualification 与公共 Schema 地基仍按现有合同工作；它不把审计候选升级成合同或实现。

## 5. 反例打穿的 authority gap

反例不是 ordinary hash collision。`relation_set_digest` 对 content semantics 保持稳定是现有冻结设计的一部分。
真正缺口是：

```text
qualification proves bounded obligations closed
admission rules decide exact Artifact membership
admission witness binds that decision to one exact qualified history
but
current public complete Bundle cannot expose and verify that witness
```

因此下一闭环必须同时守住两个方向：

```text
QUALIFIED result
    -> may become eligible for independent RelationSet membership checks

normal RelationSet in COMPLETE Bundle
    -> must have one externally verifiable qualification history
```

只做前者会留下不可外部复核的普通 Artifact；只做后者而没有 admission rules，会让 Evidence 为一个任意
candidate bag 背书。

## 6. 后继候选比较

| 候选 | 能关闭什么 | 代价 / 未关闭项 | 本轮裁决 |
| --- | --- | --- | --- |
| 直接 private RelationSet admission | 内部成员、排序、identity 与 provenance 闭包 | 完整 Bundle 仍不能证明 admission 的 qualification 来源 | 单独不足 |
| 只给 Evidence 增加 `qualification_digest` | 能携带一个 attempt-level reference | reference 本身不定义 admission witness、成员闭包或谁有资格构造该声明 | 单独不足 |
| 新增 standalone qualification/admission Artifact | 可显式保存 witness、domain/receipts/qualification | 至少新增公共 Schema、Manifest role/file set 与跨对象绑定 | 可行；当前未证明最小 |
| **RelationSet admission + explicit admission witness + public binding** | 同时关闭 private admission 与完整 Bundle 的公开履责证明 | witness 的 authority relation、identity 与 public encoding 尚未冻结；可编码在 corrected Evidence 或独立 Artifact | **下一问题面** |
| 把 RelationSet 降格为 observed prefix | 可保存诊断性候选 | 不解锁 normal Slice/Coverage；当前冻结合同禁止把偶然/中断 prefix 当普通完成态 RelationSet | 延期为独立 diagnostic 问题 |
| 直接开始 Slice/Coverage | 消费既有 relation-set shape | 会把不可证明的 admission 当稳定图或分母 | 过早 |

`DerivationEvidence` 当前只是一个可能的 public encoding/binding locus，不是由现有字段自然推导出的 admission
authority owner。下一合同必须先定义 witness 证明什么、依赖哪些 exact identities、由哪条 deterministic
application rule 形成；之后再用最小 Schema feasibility 与 identity dependency graph 决定它是 corrected
Evidence 的版本化投影，还是独立 Artifact。本文不冻结 `0.1.2` 版本号或第九文件。

## 7. 当前最小方向与保持不动的 identity

本轮只选择下一问题面：

> **RelationSet Admission / Qualification Evidence Binding**

候选形状为：

```text
exact QUALIFIED private result
    -> admission eligibility only

independent membership / conflict / provenance conformance
    -> private admitted RelationSet value

exact qualification history + admitted RelationSet
    -> explicit admission witness

admission witness
    -> public representation candidate
       (corrected Evidence binding OR standalone Artifact; unresolved)

Manifest
    -> bind selected public bytes and identities
    -> does not judge admission eligibility
```

当前证据**没有**要求修改 `relation_set_digest`。qualification 是 attempt/admission provenance；把它加入
RelationSet content identity 会让相同结构语义仅因合法运行历史不同而改变 identity，必须由额外反例证明，
不能作为默认修法。

同样，本文不授权原位修改 `DerivationEvidence 0.1.1`。若后继选择 additive patch root，历史 `0.1/0.1.1`
Schema、corpus、documents 与 digests 必须逐字节保留。

## 8. 下一合同必须裁决的问题

下一份 docs-only 最小合同至少要回答：

1. 哪个 exact private result 才有 admission eligibility；`NOT_QUALIFIED/INTEGRITY_FAILED` 怎样 fail closed；
2. RelationSet membership 如何等于 qualified merged candidates/conflicts，禁止遗漏、额外成员与 winner selection；
3. same-ID provenance union、same-subject conflict 与 provider-run reverse closure 怎样重新验证；
4. conflict-bearing `QUALIFIED` 是否 admission，以及怎样继续触发 frozen empty-Slice / Coverage UNKNOWN 语义；
5. admission witness 的最小 claim、identity、构造规则与 fail-closed 边界是什么；它怎样区别“记录运行”与
   “授权这一个 RelationSet membership”；
6. public binding 最少公开 domain、responsibility、terminal、receipt、closure、composition 与 qualification 中的
   哪个可复算投影；
7. witness 怎样绑定 exact ProviderRuns、FactSet、admitted Relation IDs/conflict IDs 与 final Evidence reported arrays；
8. witness 应编码在 corrected Evidence 还是 standalone Artifact；选择前者时怎样避免把 Evidence presence 当
   admission authority，选择后者时怎样证明新增角色确有必要；
9. 若选择 corrected Evidence，其 Artifact Schema version、semantic domain/projection、历史 byte guard 与
   correction corpus是什么；
10. Manifest 0.1 是否只需继续绑定 selected public bytes，还是有独立反例要求升级 role/file set；
11. qualification 成功后 admission/release/staging 失败时，哪些 private history 保留、哪些 final reported IDs 必须清空；
12. private admitted value、witness construction、public representation 与 actual file publication 是否需要分阶段授权。

## 9. 后继最小 falsifier 矩阵

| ID | 单变量世界 | 必须禁止或保留 |
| --- | --- | --- |
| `RAE-000` | H1/H3 raw candidates 相同，H3 缺一个合法 outcome | H3 不得形成 admitted RelationSet 或 normal final Evidence |
| `RAE-001` | QUALIFIED / CONSISTENT，成员精确相等 | 只取得 admission eligibility，不自动取得 publication |
| `RAE-002` | witness 只携带 qualification digest，但未闭合 admitted membership / ProviderRuns | cross-object reject |
| `RAE-003` | RelationSet 少一个或多一个 qualified candidate | admission reject，不缩放分母 |
| `RAE-004` | Relation provenance 指向不存在或错误 attempt 的 run | admission/Evidence closure reject |
| `RAE-005` | QUALIFIED / CONFLICTING | 若合同允许 admission，必须保留全部 candidates/conflict 且无 winner；Slice 继续为空 |
| `RAE-006` | historical Evidence 0.1/0.1.1 与新 RelationSet 组合 | 不得冒充带 qualification 的新 complete runtime Evidence |
| `RAE-007` | overall non-COMPLETED 或 staging/release failure | final reported IDs 为空，不能发布 normal RelationSet |
| `RAE-008` | RelationSet Schema-valid 但没有可复算 admission witness/public binding | complete-bundle conformance reject |
| `RAE-009` | 同一 Relation semantics 来自两个独立合法 attempts | `relation_set_digest` 可稳定；provenance file bytes、witness 与 attempt Evidence 必须各自可复算 |
| `RAE-010` | Manifest 精确绑定 RelationSet/Evidence bytes，但 witness 不成立 | Manifest 不得替子 Artifact 判定 admission eligible |

该矩阵是下一合同的否定边界，不是实现测试清单，也不授权任何 Schema 或 runtime 文件。

## 10. 外部案例插入判断

本轮不启动外部大厂 failure-shape survey。当前 exact-main Schema、private runtime 与本地单变量反例已经回答：

- 问题真实存在于哪个 authority seam；
- 当前哪三个公共对象不能承载绑定；
- 哪条最小方向能避免先扩 Manifest role；
- 哪些 identity 不应因方便而默认改写。

如果下一合同在“公开 receipt 的最小可复算字段”或“跨工具生态怎样携带 qualification”上仍出现具体经验缺口，
再按该 failure family 查公开一手材料。公司名不成为目录，外部做法也不直接产生合同 authority。

## 11. 状态与唯一下一步

本文起草时，在自己的 docs-only 门、原始远端门、受保护主线合入、新 exact-main 门与公开读回成立以前，
历史状态只能是：

```text
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_SYSTEM_AUDIT_CANDIDATE
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

闭环后，本文最多发布：

```text
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED
```

该闭环现已成立：PR #170 合入 `main@1ffc4494dbbb61a056dcc8beed2530e7313f6116`；该 exact main 的
Public CI attempt 1 为 11/11，Browser Smoke attempt 1 为 1/1。README、本文、能力地图与 milestones
使用四组不同 Plan/session/output root 完成 fresh anonymous API + render paired readback，均为 HTTP 200、
P1/P2 `COMPLETE`、三样本稳定、唯一 marker 与零 cleanup residue；canonical readback manifest
`sha256_json=d4ec2504e8bd2176d76eb6cda46fb44f6edda9dacc8c61c056c0a2a833535ad1`，combined summary
SHA-256 为 `e6c6d1a50d1f9269453cfb978b18cd5d6658f901d6510536fc38869bf69bd0aa`。因此当前状态是
`R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED`；早先
`SYSTEM_AUDIT_CANDIDATE` 是可追溯历史，不被改写成当时已经闭合。

唯一合法下一步已从该 exact main 以[文档 183](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)
起草 docs-only RelationSet Admission / Explicit Admission Witness / Public Qualification Binding 最小合同候选。
本文仍不得直接开始：

- RelationSet / corrected Evidence Schema 或 runtime；
- standalone qualification Artifact 或 Manifest file-set 扩张；
- full import resolution、public Provider SPI/registry/discovery；
- Slice、Coverage、Attention、publisher、CLI 或 Workbench；
- P/Q/D/Cu/O/T、Core、tag 或 Release。

任何新反例只重开被打穿的最小条款，不改写文档 165/172/175/179 已冻结的运行事实。
