# R1 Fact / Relation stage applicability capability identity 修正合同 0.1

> Status: `CONTRACT_CANDIDATE / NOT_FROZEN`
>
> Exact source world: `main@0dd06e0e236a56472925bd6f29fc053b49727958`
>
> 本文只修正冻结文档 290 §5 的 stage-owner capability identity，并为该修正建立可区分的 versioned semantic
> function。文档 290/291 的历史字节和冻结事实保持不变；runtime、tests、Schema、Profile、Policy、Provider、manifest、
> persistence、Coverage 与 public Review 产品均不在本轮施工范围内。

## 1. CONTROL LOOP 与 qualified upstream

[文档 293](293-r1-fact-relation-stage-applicability-capability-identity-correction-audit.md)由 PR #338 合入
`main@0dd06e0e236a56472925bd6f29fc053b49727958`。其 original Public CI、exact-main Public CI 与 Browser Smoke
均为 attempt 1 SUCCESS，分别为 11/11、11/11 与 1/1。fresh README、doc293、milestones installed-product
readback 为 3/3 `FORMAL_READBACK_PASS`，independent reconciliation 与 132-artifact closeout 分别为：

```text
f5412f7e32842687ecb5df0162c70e18ae1850f1329ff52292fa5f4f87208529
54231fcfb88109112115ac5c5b08e1ad088d8269c266b9221885442b37b70cdf
```

pre-formal verifier attempt 1 把上游 closeout 生成时仍为空、随后才写入终态绑定的 wrapper stdout 当作普通静态
artifact，保留为 `UPSTREAM_CLOSEOUT_STDOUT_SELF_REFERENCE_VERIFICATION_SETUP_ERROR`。fresh attempt 2 同时核验
manifest 中的 pre-print empty identity 与 stdout 对 closeout SHA 的 terminal binding 后 PASS；正式产品观察当时仍为零。

当前 remote main、exact worktree 与本合同 construction base 一致。open PR 只有依赖更新，没有 semantic PR 已经修正本
identity seam。因而下一最小合法问题仍是 docs-only contract correction，不是 successor runtime。

## 2. 被击穿的旧主张与最小 reopen

冻结的 `r1-fact-handoff-relation-interoperability-correction/0.1` 将 Fact stage owner 写成：

```text
review-fact-derivation
```

该 identity 在 exact repository world 中不存在；它不是 Provider descriptor、Policy requirement、Schema value 或 frozen alias。
当前 Fact stage 的实际 capability identities 是 required `python-ast` 与存在时 optional `python-ast-advisory`；Relation stage
拥有 required `review-relation-derivation`。

本合同只 reopen 以下主张：

```text
stage applicability function identity
stage-owned capability identity map
cross-stage ownership completeness / disjointness proof
parent correction contract version
```

文档 290 的完整 Policy、完整 FactSet、per-product closure、total Fact partition、obligation projection、expected/emitted
双向核账、known-empty、same-attempt claim、UNKNOWN/UNSAT boundary 与 authority ceiling均不被本轮反例击穿。

## 3. authority owner 与禁止自证

| 主体 | 拥有 | 不拥有 |
| --- | --- | --- |
| sealed Policy | 完整 requirement rows、requiredness、composition mode、canonical bytes 与 `policy_digest` | stage owner map、履责结果或 live continuation |
| 本合同 | bounded Fact/Relation owner map 与 `/0.2` stage-applicability semantics | 增删 Policy row、Provider terminal、Fact/Relation truth |
| application | 按冻结函数机械构造两个 stage partition并核账 | 猜测 alias、按 Provider 输出反推 owner、忽略未知 capability |
| Fact / Relation Provider | 自己被分配责任的 bounded execution | 声明自己或另一 stage 的 applicability、修改 Policy identity |
| digest/content holder | 对应 immutable bytes | attempt、claim、qualification、admission或 continuation authority |

Provider、caller、Schema、manifest、Coverage 与 publisher均不能定义 owner map。application 只能执行本文冻结的 total
classification；如果输入不在 bounded policy universe 中，必须停止，不能以“最接近的已知 capability”继续。

## 4. versioned normative identities

本合同冻结以下 successor identities：

```text
parent correction function
    r1-fact-handoff-relation-interoperability-correction/0.2

stage applicability function
    r1-fact-relation-stage-applicability/0.2
```

以下文档 290 identities保持原语义，不因本修正重新编号：

```text
per-product closure
    r1-fact-relation-product-closure/0.1

obligation projection
    r1-fact-relation-obligation-projection/0.1
```

`/0.2` 不是 `/0.1` 的 alias、原位勘误或 closest-version fallback。future private carrier/request 必须可区分地绑定
parent `/0.2` 与 stage-applicability `/0.2`；旧 `/0.1` bytes不得被静默当作 `/0.2` 接受。本文不选择 Python class、field、
serialization、public Schema 或 manifest successor。

## 5. bounded capability universe 与 exact requiredness

首个 `/0.2` 只接受以下完整 requirement identities：

```text
python-ast
    required = true
    composition_mode = CUMULATIVE

python-ast-advisory
    required = false
    composition_mode = CUMULATIVE
    presence = optional

review-relation-derivation
    required = true
    composition_mode = CUMULATIVE
```

因此合法 bounded Policy shape 只能是：

```text
{python-ast, review-relation-derivation}

或

{python-ast, python-ast-advisory, review-relation-derivation}
```

集合表示只说明成员关系；canonical Policy bytes仍拥有顺序、重复拒绝、字段和值的完整验证责任。`python-ast-advisory`
缺席不产生一个虚构 row；存在时必须保持 optional requiredness。任一 required row缺失、duplicate、requiredness或
composition mode改变、出现未知 capability，均使 `/0.2` applicability construction fail closed。

特别地，`review-fact-derivation` 必须作为 unknown/nonexistent capability被拒绝，不能映射、规范化或重命名为
`python-ast`。

## 6. total stage ownership 与双层 partition

对完整 sealed Policy `P` 中每个实际 requirement row `r`，规范 owner 函数为：

```text
Owner_0.2(r) = FACT
    iff r.capability_id in {python-ast, python-ast-advisory}

Owner_0.2(r) = RELATION
    iff r.capability_id == review-relation-derivation
```

它必须满足：

```text
FACT_owned(P) union RELATION_owned(P) = requirements(P)
FACT_owned(P) intersect RELATION_owned(P) = empty
count(owner for each exact requirement identity) = 1
```

然后每个 stage `s` 分别构造自己的 total applicability partition：

```text
requirements(P)
    = applicable_requirements(s)
      disjoint-union non_applicable_requirements(s)
```

其中：

```text
applicable_requirements(FACT)     = FACT_owned(P)
applicable_requirements(RELATION) = RELATION_owned(P)
```

另一 stage 的 rows 必须以完整 identity 出现在 `NON_APPLICABLE_TO_STAGE` 一侧。它们不是 optional、fulfilled、deleted、
unknown 或 globally out of scope。两个 stage均无权替另一方签发 fulfillment。

只分别证明“Fact认识自己的 rows”和“Relation认识自己的 rows”仍然不够；`/0.2` 额外要求 cross-stage union、intersection与
每-row唯一 owner核账。这样不能把一个漏归属的 requirement藏在两个局部 PASS 之间。

## 7. exact input、semantic projection 与 live authority

每次 applicability construction必须 copy-own：

```text
complete canonical Policy bytes
policy_digest
stage identity
stage-applicability function identity
applicable side exact requirement identities
non-applicable side exact requirement identities
cross-stage ownership reconciliation identity
```

与 applicability 无关的 execution/governance字段可以不进入 stage semantic result digest，但仍属于 exact Policy world。
两份 Policy 即使得到相同 semantic classification，只要 canonical bytes、digest、attempt或 live state不同，就不能继承另一世界的
qualification、claim、ProviderRun或 continuation。

stage applicability只回答“这一 stage 对哪些 Policy requirements负有责任”。它不证明责任已经履行，也不生成 Fact、Relation、
RelationSet、Coverage 或 public truth。

## 8. 与完整 Fact / Relation algorithm 的组合边界

`/0.2` stage applicability通过后，文档 290 §6–§13 的其余算法才可能继续：

```text
same sealed Policy /0.2 ownership qualification
    -> complete same-attempt Fact handoff claim
    -> unchanged per-product closure /0.1
    -> unchanged total Fact partition
    -> unchanged obligation projection /0.1
    -> unchanged expected/emitted bidirectional reconciliation
    -> frozen Relation observation semantics
```

stage owner修正不允许：

- 过滤或重写完整 FactSet；
- 以 `python-ast` Provider output替代 Policy owner proof；
- 把 Relation requirement交给 Fact stage履责；
- 弱化 per-product MODULE closure；
- 缩小 obligation denominator；
- 复用 foreign attempt、已消费 claim或 digest holder；
- 恢复旧 composition A–J authorization。

如果 feasibility 证明现有 private carrier不能无损绑定 `/0.2` identity与完整 two-stage partition，必须在新的最小 carrier/version
seam停止；不得通过修改 `/0.1` 或省略 non-applicable side规避。

## 9. normative falsifier obligations

后继 feasibility / implementation至少必须攻击：

| ID | 单变量 world | 必须拒绝的错误结论 |
| --- | --- | --- |
| `FRIC-CID-001` | Policy使用 `review-fact-derivation` | 将其别名化为 `python-ast` |
| `FRIC-CID-002` | 缺 required `python-ast` | Relation row存在即可建立完整 ownership |
| `FRIC-CID-003` | 缺 required Relation row | Fact stage成功自动授权 Relation |
| `FRIC-CID-004` | advisory存在但标成 required | capability string相同即可忽略 requiredness |
| `FRIC-CID-005` | duplicate `python-ast` | 两个相同 owner rows可折叠成一个 |
| `FRIC-CID-006` | unknown capability row | 归入两个 stage的 non-applicable side即可继续 |
| `FRIC-CID-007` | 一个 row同时进入两 stage applicable sides | overlap仍可由两个局部 PASS掩盖 |
| `FRIC-CID-008` | 一个 row未进入任一 stage applicable side | gap不影响 downstream completeness |
| `FRIC-CID-009` | stage applicable side正确但 non-applicable side缺 row | subset正确等于 total partition正确 |
| `FRIC-CID-010` | 相同 semantic classification、不同 Policy bytes/digest | semantic equality继承 exact-world authority |
| `FRIC-CID-011` | `/0.1` request携带修正后的 owner rows | 实际内容正确即可忽略 function version |
| `FRIC-CID-012` | `/0.2` request声明旧不存在 owner | version label可以替代 semantic conformance |

文档 290 的 `FRIC-000..018`继续全部适用。本合同没有用新的 owner map删除旧反例。

本合同起草阶段另以 pure semantic model机械执行上述 bounded owner map。CPython 3.10.6 / 3.13.13、normal / `-O`
四格输出逐字节相同；两个 positive Policy worlds建立完整 ownership，八个 negative worlds分别拒绝旧 identity、缺 required
row、错误 advisory requiredness、duplicate、unknown、overlap与gap：

```text
audit script SHA256
27b1369ee094a81543a01c19bffa0484c9bc742da2a18565fbc67cb8c37e53bc

four-cell report SHA256
a1201a99ea6cc28edcbae973d69d550aa6c1e2c607d77dc1530622c4d2864e7d

semantic digest
74f5f8bef3edc46278bb927c967976a159f3d991a7390e999123909482fa2809
```

同一四格还分别运行现有 Fact fulfillment、Relation derivation、Relation observation qualification与RelationSet admission
窄基线；每格均为 `Ran 77 tests / OK (skipped=1)`。该 model与回归只证明合同区分可机械表达且未观察到既有产品回归，
不是 runtime implementation或产品资格证据。

## 10. UNKNOWN、UNSAT 与正确拒绝

若 exact Policy不属于 §5 的 bounded universe，结果是该 contract version下
`UNKNOWN / NO_QUALIFIED_CONSTRUCTION` 或明确的 input rejection；不能自动声称整个系统无解。只有穷尽本文明确限定的完整
候选空间并给出机械不可满足性证明，才可声明该 bounded contract的 `UNSAT / NO_CONSTRUCTION_EXISTS`。

拒绝一个没有完整 owner partition的 Policy world是合同成功履责，不是比错误给出 COMPLETE 更弱的结果。

## 11. 本合同不决定什么

本文明确不决定：

- successor Python对象、private carrier、Schema、manifest或serialization；
- current Fact/Relation runtime如何改造；
- Relation Provider algorithm、new relation families或module resolution；
- RelationSet admission、Slice closure、ReviewSliceSet/Coverage composition；
- persistence Route A/B、cache、Bundle、publisher、CLI、Workbench或Core；
- R2 Evidence、R3 Attention、human disposition或效益测量；
- post-R1 Benchmark是否已经启动；
- successor implementation feasibility或implementation authority。

## 12. candidate qualification 与停止线

本候选 tracked scope只允许：

```text
README.md
AGENTS.md
docs/294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md
docs/milestones.md
```

doc290–293、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、vectors、corpus与post-R1计划必须保持
base bytes。final bytes至少完成四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、marker、上游 byte
continuity、`git diff --check`、read-only hygiene、声明的Markdown/baseline regression与doc293四格证据复核。

```text
final docs-only contract bytes / declared local gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> qualified contract candidate
    -> separate docs-only freeze publication
    -> freeze publication's own original PR / merge / exact-main / readback / reconciliation
    -> corrected CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

当前只能记录：

```text
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_AUDIT_QUALIFIED_HISTORY
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_CANDIDATE
R1_FACT_HANDOFF_RELATION_STAGE_APPLICABILITY_CAPABILITY_IDENTITY_CORRECTION_CONTRACT_NOT_FROZEN
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_FEASIBILITY_STOP_CONDITION_TRIGGERED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_EXACT_INPUT_INTEROPERABILITY_CORRECTION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

即使本合同最终冻结，也只解除 corrected successor feasibility 的合同阻断。它不自动授权 runtime、恢复旧 composition A–J、
选择 manifest/persistence、启动 Coverage/public Review、执行 post-R1 Benchmark 或进入 R2/R3。
