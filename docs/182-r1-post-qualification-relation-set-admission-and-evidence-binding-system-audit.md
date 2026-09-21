# R1 RelationSet Admission / Qualification Evidence Binding 系统审计

> 状态：`R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_SYSTEM_AUDIT_CANDIDATE /
> R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@de0fdc6f01e1c99ae74259abd77640ad39d28038`
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

Final Evidence / complete Bundle
    -> which admitted identities and qualification history a third party can verify
```

前三层已在 private closed proof 中冻结。后两层尚未实现。继续成立：

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
加字段。

### 3.3 Manifest 0.1

`Manifest 0.1` 的 `COMPLETE` file set 固定为八个角色。它绑定每个 Artifact 的 exact file bytes 与 semantic
identity，但不替子 Artifact 决定自己的 Schema patch version。既有 Evidence `0.1 -> 0.1.1` 修正已经冻结：

```text
Artifact Schema version != Manifest Schema version
Schema validity         != cross-object derivation conformance
```

因此“需要公开 qualification”不自动推出第九种 Artifact role 或 Manifest shape 升级。

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

### 4.2 结果

Q 与 U 的 raw phase candidate/conflict canonical projection 完全相同：

```text
candidate projection SHA-256:
8180ec9d8a0fc48636d0ac68f36645ec22e097165a1ced28a6b9c98b78709f30

relation IDs:
4e42c7e39960bd9e247da522260afbcd36aa9df49e5d4ac5f9fad6d927df02d2
9872c294f8e9c15128867029ec9fd5845b3ce6cc1220aa8f5cc036605abccdc1
```

Q：

```text
qualification_digest = 8c5fb7b038980920a2fedcf1010c8fc1cb9e8b6103486d308584075b6f173faa
status               = QUALIFIED / COMPLETE / CONSISTENT
```

U：

```text
qualification_digest = 5fdbe8ea510bf428131eead3a47a4d337b32d95f6fee321c533fca8643c503e0
status               = NOT_QUALIFIED / INCOMPLETE / NOT_COMPOSED
merged candidates    = []
reason codes         = OBSERVATION_OUTCOME_MISSING / UNEXPECTED_RELATION_CANDIDATE
```

如果一个未来 assembler 错误绕过 U 的 qualification status，直接从 raw phase candidates 构造
`RelationSet 0.1`，现有 Schema 会接受该文档：

```text
relation_set_digest = 9be261a89ffa32d328357590567cdc1050b9158979b81f2a24f2c3fe6c5c4749
canonical JSON SHA-256 = 7fc3fbad405051b17fab90fad7f0160c9fbf295ba6bf2dffd9f858489cc3e9c4
Schema validation = ACCEPT
```

这不授权 U admission，也不声称当前代码存在该 assembler。它只证明：

> current public RelationSet shape cannot distinguish a qualified projection from the same candidate content copied
> around qualification.

### 4.3 绑定能力 probe

在内存副本上追加单一候选绑定，当前 closed Schema 均 fail closed：

| Probe | 当前结果 |
| --- | --- |
| `RelationSet 0.1 + qualification_digest` | root additional property，reject |
| `DerivationEvidence 0.1.1 + relation_qualification_digest` | root additional property，reject |
| `COMPLETE Manifest 0.1 + ninth RELATION_QUALIFICATION file` | exact eight-file/closed role，reject |

这只证明当前版本不能原位承载绑定；它不预先选择字段名、Semantic Digest 投影或第九文件方案。

### 4.4 跨运行时复算

CPython 3.10 与 3.13 对上述完整审计报告产生相同 2753 bytes：

```text
sha256_json = d798d8df88d6a6b3ebfbcc6fe14ef0edb3a36d699f0df0538a41fa884416fd5a
```

本地输出位于仓库外临时审计目录，不是产品 Artifact、冻结 corpus 或发布 Evidence。

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
private qualification can authorize admission
but
current public complete Bundle cannot expose and bind that authorization
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
| 新增 standalone qualification Artifact | 可保存 domain/receipts/qualification | 至少新增公共 Schema、Manifest role/file set 与跨对象绑定；attempt Evidence 中仍已有 ProviderRun owner | 可行但当前非最小 |
| **RelationSet admission + attempt-level qualification Evidence closure** | 同时关闭 private admission 与完整 Bundle 的公开履责证明；可复用既有 Evidence owner 与八文件角色 | 必须版本化 Evidence、定义跨对象 conformance；具体 shape 尚未冻结 | **下一问题面** |
| 把 RelationSet 降格为 observed prefix | 可保存诊断性候选 | 不解锁 normal Slice/Coverage；当前冻结合同禁止把偶然/中断 prefix 当普通完成态 RelationSet | 延期为独立 diagnostic 问题 |
| 直接开始 Slice/Coverage | 消费既有 relation-set shape | 会把不可证明的 admission 当稳定图或分母 | 过早 |

“attempt-level Evidence closure”描述 authority owner，不等于已经选择把全部 private receipt 原样内联，也不
冻结 `0.1.2` 版本号。下一合同必须用最小 Schema feasibility 和 identity dependency graph 决定公开投影。

## 7. 当前最小方向与保持不动的 identity

本轮只选择下一问题面：

> **RelationSet Admission / Qualification Evidence Binding**

候选形状为：

```text
exact QUALIFIED private result
    -> independent membership / conflict / provenance conformance
    -> private admitted RelationSet value

same attempt ProviderRuns + public qualification projection
    -> versioned DerivationEvidence candidate

admitted RelationSet + corrected Evidence + existing complete file roles
    -> cross-object qualification/admission closure
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
5. public Evidence 最少公开 domain、responsibility、terminal、receipt、closure、composition 与 qualification 中的
   哪个可复算投影；
6. public qualification 怎样绑定 exact ProviderRuns、FactSet、admitted Relation IDs/conflict IDs 与 final
   Evidence reported arrays；
7. corrected Evidence 的 Artifact Schema version、semantic domain/projection、历史 byte guard 与 correction corpus；
8. Manifest 0.1 是否只需继续绑定 corrected Evidence bytes，还是有独立反例要求升级 role/file set；
9. qualification 成功后 admission/release/staging 失败时，哪些 private history 保留、哪些 final reported IDs 必须清空；
10. private admitted value、public Evidence construction 与 actual file publication 是否需要分阶段授权。

## 9. 后继最小 falsifier 矩阵

| ID | 单变量世界 | 必须禁止或保留 |
| --- | --- | --- |
| `RAE-000` | Q/U raw candidates 相同，U 缺一个合法 outcome | U 不得形成 admitted RelationSet 或 normal final Evidence |
| `RAE-001` | QUALIFIED / CONSISTENT，成员精确相等 | 只取得 admission eligibility，不自动取得 publication |
| `RAE-002` | qualification digest/domain 与 ProviderRuns 不匹配 | cross-object reject |
| `RAE-003` | RelationSet 少一个或多一个 qualified candidate | admission reject，不缩放分母 |
| `RAE-004` | Relation provenance 指向不存在或错误 attempt 的 run | admission/Evidence closure reject |
| `RAE-005` | QUALIFIED / CONFLICTING | 若合同允许 admission，必须保留全部 candidates/conflict 且无 winner；Slice 继续为空 |
| `RAE-006` | historical Evidence 0.1/0.1.1 与新 RelationSet 组合 | 不得冒充带 qualification 的新 complete runtime Evidence |
| `RAE-007` | overall non-COMPLETED 或 staging/release failure | final reported IDs 为空，不能发布 normal RelationSet |
| `RAE-008` | RelationSet Schema-valid 但没有可复算 qualification binding | complete-bundle conformance reject |
| `RAE-009` | 同一 Relation semantics 来自两个独立合法 attempts | content identity 可稳定；attempt Evidence 必须各自可复算 |

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

在本文自己的 docs-only 门、原始远端门、受保护主线合入、新 exact-main 门与公开读回全部成立以前，状态只能是：

```text
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_SYSTEM_AUDIT_CANDIDATE
R1_RELATION_SET_ADMISSION_EVIDENCE_BINDING_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

闭环后，本文最多发布：

```text
R1_POST_QUALIFICATION_RELATION_SET_ADMISSION_EVIDENCE_BINDING_PRECONTRACT_AUDITED
```

唯一合法下一步是从届时新的 exact main 起草 docs-only RelationSet Admission / Qualification Evidence Binding
最小合同候选。不得由本文直接开始：

- RelationSet / corrected Evidence Schema 或 runtime；
- standalone qualification Artifact 或 Manifest file-set 扩张；
- full import resolution、public Provider SPI/registry/discovery；
- Slice、Coverage、Attention、publisher、CLI 或 Workbench；
- P/Q/D/Cu/O/T、Core、tag 或 Release。

任何新反例只重开被打穿的最小条款，不改写文档 165/172/175/179 已冻结的运行事实。
