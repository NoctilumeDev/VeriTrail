# R1 ReviewSliceSet / Coverage composition 私有实现候选

日期：2026-10-21

> 状态：`IMPLEMENTATION_CANDIDATE / LOCAL_GATES_PASS / NOT_QUALIFIED / NOT_FROZEN`。
>
> 施工基线：`main@36333195833a462169e883aab0d36637e2edbdf3`，tree
> `3731a6211abf976fd98d7e67b7ac315154ef1201`。
>
> 本文认领[文档312](312-r1-review-slice-set-coverage-composition-authority-recovery-publication.md)已经生效的
> bounded private implementation A–J。本文只记录Relation transition → Slice authority bridge、private ReviewSliceSet successor
> 与CoverageLedger 0.3 validation witness；不发布merged、exact-main verified、readback qualified或frozen状态，不选择manifest
> successor或persistence，不启动public Review产品、post-R1 Benchmark或R2–R6。

## 1. CONTROL LOOP 与已生效authority

文档312由PR #357 final head `e4503ad0392c762eaf2abeed5597b31c6853934b`从
`main@35e99a872d33234c4fb923a64995ccb148d9e3ba`建立，受保护合入后的exact main为本施工基线。candidate与merge tree均为
`3731a6211abf976fd98d7e67b7ac315154ef1201`。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #357 original Public CI | `39455940067` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39460190492` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39460190387` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc311、doc312与milestones为4/4 qualifying PASS。independent reconciliation、
finite closeout attempt 2与finite-integrity summary分别为：

```text
9a78a3df2dcc9117b49c2dea31cfad62cd3f8d683e64d71caec0371caf825d33
da1855844e36ebcfc32a84873b988b88738e919fbc2c96addd62608005b0bafc
82ea3195bca5e6bfea10c720b37e368df232ff483dd9145b41856f40dc8cccc1
```

closeout attempt 1的stdout self-capture mismatch保持原identity，semantic effect为`NONE`。因此
`R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。fresh CONTROL LOOP重新核对exact
main、doc267/281/287/310/311/312、legacy Slice字节、CoverageLedger 0.3 conformance、#346 retained failure与primary
`audit.json`；没有更早反例要求重开已冻结边界。当前最小合法施工面仍是文档312限定的private A–J。

## 2. versioned private identities

本候选新增一组显式、可区分且未公开导出的private identity：

```text
r1-relation-transition-to-slice-authority-bridge/0.1
r1-relation-transition-to-slice-authority-request/0.1
r1-relation-transition-to-slice-authority-admission/0.1
r1-review-slice-set-coverage-composition/0.1
r1-review-slice-set-successor-admission/0.1
r1-review-slice-set-successor/0.1
```

入口只接受exact `ClaimedFactRelationTransitionContinuation`。bridge admission、bridge continuation与最终composition result都由
private constructor token创建并copy-own canonical bytes；claim与continuation分别one-shot。legacy
`OwnedRelationQualificationContinuation`入口、constructor/token、Slice wire和默认composition保持不变，新旧authority不能互换。

本候选未修改`__init__.py`、`pyproject.toml`、workflow、public Schema、Policy/Profile、Fact/Relation实现或任何legacy Slice文件。

## 3. exact transition bridge

bridge在任何Slice work以前重新验证：

- original live `DerivationInputSet`、`BudgetContext`与`AttemptEligibility`仍为同一对象且处于可继续状态；
- transition function/version、qualified admission、handoff claim、attempt与request provenance仍与original carrier一致；
- complete Provider lineage重新组合出的Relation members/conflicts与sealed RelationSet逐字相等；
- complete obligation projection与Provider observation assignment双向、唯一、无遗漏地闭合；
- transition ceiling仍未取得ReviewSliceSet、Coverage、manifest、persistence或public Review authority。

相同bytes、digest、members、limits或semantic output都不能替代live continuation。foreign object、已经消费的claim、digest-only
holder、fresh context、resealed attempt/history漂移与legacy token全部fail closed。bridge admission成功只签发下一条private edge，
不会把transition本身改写成Slice authority，也不会重跑Relation。

## 4. complete Slice denominator 与common-mode falsifier

consumption成功以后，candidate先通过既有pure Slice primitive从complete FactSet、RelationSet、sealed Policy/Profile构造
`slice_obligation_domain`。随后新的independent validator不信任该producer：它直接从冻结Policy/Profile、完整Fact kinds、每个accepted
path及Relation membership重新推导expected Slice obligation universe，并对全部spec、anchor、path、closure与domain digest做双向比较。

因此以下common-mode failure被直接拒绝：

```text
producer 漏掉一个 obligation
    + 重封 domain digest
    + downstream 只核 produced domain
```

测试会故意把普通producer结果缩成空集合并重封digest；independent validator仍以冻结规则推导出的完整集合拒绝该候选。Slice
denominator不能由actual output、representable subset、successful subset、UI convenience或caller bool反推。

multi-path world对每个path保留唯一same-path MODULE anchor；obligation集合与Slice集合按完整digest集合核对，而不是依赖producer
顺序。valid zero-anchor world得到真实空domain与`CLOSED_EMPTY`，不会把unknown或blocked冒充empty。

## 5. ReviewSliceSet successor 与terminal preservation

每个obligation使用existing private assignment、traversal与normal Slice validator生成candidate；所有candidate重新验证后才进入新的
private `ReviewSliceSet / 0.1` successor。SliceSet绑定source/policy/scope/profile、FactSet、RelationSet、完整member identity与集合digest。

normal world保留当前traversal的`NORMAL_PARTIAL`，并产生一个或多个exact Slice member；zero-anchor world产生空members但保留
`CLOSED_EMPTY`资格。存在真实Relation conflict时不构造Slice domain或SliceSet，admission为`PREDECESSOR_UNKNOWN`；Relation stage
保持`PARTIAL`，Slice stage与overall Coverage保持`UNKNOWN`。这三个branch互不继承authority。

missing、duplicate、foreign或mutated Slice member不能进入集合。相同members或相同digest也不能从另一个attempt继承closure、
admission或composition authority。

## 6. seven-stage Coverage与root chain

本候选从exact upstream history与Slice terminal branch构造七阶段`S/A/N/D`投影：

```text
SNAPSHOT_INVENTORY
POLICY_SCOPE
LANGUAGE_SUPPORT
PARSE
FACT_DERIVATION
RELATION_DERIVATION
SLICE_DERIVATION
```

每个stage明确记录coverage status、expected/emitted/terminal refs、frontier与predecessor proof。FactSet、RelationSet与
ReviewSliceSet组成ordered root chain；每个root保存artifact digest、terminal branch、terminal-history digest、predecessor binding与
closure。complete normal world得到前六阶段`COMPLETE`、Slice `PARTIAL`、overall `PARTIAL`；conflict world保持Relation
`PARTIAL`、Slice `UNKNOWN`、overall `UNKNOWN`。

`CoverageLedger 0.3`只由现有validation-only conformance source核对这些projection。它不生成Fact、Relation、Slice authority，
不改变terminal state，也不选择manifest successor、persistence或publication。

## 7. direct falsifiers 与legacy byte guards

新增10项direct tests：

1. exact default world闭合complete Fact/Relation、SliceSet、seven-stage ledger与authority ceiling；
2. multi-path保持逐path MODULE closure与完整Slice denominator；
3. zero-anchor只在已证明空domain上取得`CLOSED_EMPTY`；
4. 真实Relation conflict保持`PARTIAL / UNKNOWN`，不制造Slice；
5. transition claim与bridge continuation均one-shot；
6. foreign、digest-only与legacy authority不能越界；
7. producer与validator共因漏项被independent denominator reconstruction拒绝；
8. mutated Slice candidate不能进入SliceSet；
9. resealed transition terminal history不能跨bridge；
10. 三个legacy Slice实现文件保持exact SHA-256。

legacy guards为：

```text
_review_slice_input.py        185ab7adb57b13ffc29a14bf20411702c316000b0c6733a45f7135f8db3ca307
_review_slice_input_values.py 21a58d679018bc45131d8e4a3909d1f14a7491085106f422e18d64d9f5048bb3
_review_slice_traversal.py    263bfc8adeac96a1181afdbaa526aac3452523a240f699d23f2a948529a6b784
```

## 8. final local qualification

focused matrix由Fact→Relation transition、legacy Slice join、Fact→Coverage handoff与本候选10项tests组成。四格均使用当前final
runtime/test bytes：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 140 / 140 PASS |
| 3.10.6 | `-O` | 140 / 140 PASS |
| 3.13.13 | normal | 140 / 140 PASS |
| 3.13.13 | `-O` | 140 / 140 PASS |

完整Review Attention suite也在同一final bytes闭合：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 574 reported / 571 passed / 3 skipped |
| 3.10.6 | `-O` | 574 reported / 571 passed / 3 skipped |
| 3.13.13 | normal | 574 reported / 572 passed / 2 skipped |
| 3.13.13 | `-O` | 574 reported / 572 passed / 2 skipped |

独立semantic report对default normal、multi-path与zero-anchor三个world投影稳定Fact/Relation/Slice/Coverage语义，删除attempt-local
identity后四格逐字一致：

```text
ac29917eb0303931abbba15e25499f80fd39782562f0578c021fd119d5717048
```

Python 3.10/3.13 `py_compile`、`git diff --check`、global/local hygiene、public export/pyproject/workflow guard与primary
`audit.json` continuity均PASS。实现文件与测试文件当前SHA-256分别为：

```text
9e1331596705f911a58e2867bf1643ff2f7e9e90649e79a717ca560eb4d3404a
8e6c8922695b9b2ae0d4665e299a8318f02d399d6d548195b29226a483e9952f
```

这些测试只是candidate witness，不替代original PR、protected merge、exact-main gates、installed-product readback或independent
reconciliation。

## 9. retained prequalification与proof-facility history

formal qualification以前保留的implementation findings包括：首版bridge把successor `obligation_id`与Provider
`observation_item_id`直接比较，现改为冻结的`provider_observation_item_id`映射；初版coverage inspection读取不存在的
`stage_records`；zero-anchor fixture与eligibility assertion选错对象；conflict falsifier先后误用了legacy validator、immutable tuple和
不合法的双Relation terminal。它们均在formal matrix以前修正，没有产生可覆盖的正式产品失败。

semantic report attempt 1读取不存在的`coverage_ledger_function`，四格在已经完成产品构造后于proof projection阶段同样
`KeyError`；归为`SEMANTIC_REPORT_PROOF_FACILITY_SCHEMA_KEY_ERROR`。attempt 2只改读实际冻结的`artifact_kind / schema_version`
后四格逐字PASS，没有修改产品、tests或oracle。初始source路径、PowerShell/JavaScript quoting、文档名猜测和Windows glob也作为
setup history保留。final Python 3.13 compile proof attempt 1还因工具参数名误写为`workdir:`而从父目录启动，产生relative-path
`FileNotFoundError`；fresh attempt 2从exact worktree执行并以空stdout/stderr PASS。全部设施错误的qualification effect均为`NONE`。
local qualification汇总设施attempt 1还对整个`git status --short`输出使用`strip()`，删除首行状态左空格并误报scope drift；
attempt 2只去除尾部换行后按六文件exact scope PASS。该错误同样没有修改candidate bytes。

## 10. tracked scope 与资格链

本候选的预期tracked scope只允许：

```text
README.md
AGENTS.md
docs/313-r1-review-slice-set-coverage-composition-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_relation_transition_slice_composition.py
plugins/review-attention/tests/test_relation_transition_slice_composition.py
```

doc267、doc281、doc287–312、legacy Slice、Fact/Relation transition、CoverageLedger conformance、public Schema、Policy/Profile、
workflows、manifest、persistence、public Review与post-R1计划必须保持base bytes。完整资格链为：

```text
final implementation bytes / declared local gates
    -> single candidate commit
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
    -> return CONTROL LOOP
```

任何non-success必须保留原identity并停止当前资格链。相同tree、semantic digest、旧composition成功或后继PASS不能替代任一门。
`FROZEN`必须由后继独立docs-only publication完成自己的完整资格链以后才能生效。

## 11. 当前状态与stop line

本文只发布：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本候选不能因为local PASS宣称merged、exact-main verified、readback qualified或frozen。若任何门揭示bridge不能保持complete
denominator、same-attempt authority、terminal history、legacy bytes或Coverage validation-only边界，必须保留首个反例并只重开被击穿的
最小边界。全部candidate资格门闭合后仍须返回CONTROL LOOP，单独建立docs-only implementation freeze publication；本文不自动选择
manifest successor、persistence route或public Review product。
