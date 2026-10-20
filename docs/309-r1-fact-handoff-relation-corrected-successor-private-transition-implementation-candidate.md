# R1 Fact handoff → Relation corrected successor 私有 transition 实现候选

> 状态：`IMPLEMENTATION_CANDIDATE / LOCAL_GATES_PASS / NOT_QUALIFIED / NOT_FROZEN`
> 日期：2026-10-20
> 前置：[互操作修正合同](290-r1-fact-handoff-relation-exact-input-interoperability-correction-contract.md)、
> [stage applicability capability identity 修正合同](294-r1-fact-relation-stage-applicability-capability-identity-correction-contract.md)、
> [corrected Provider 私有实现冻结发布](306-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-freeze-publication.md)、
> [authority recovery 当前状态审计](307-r1-fact-relation-corrected-successor-authority-recovery-current-state-audit.md)与
> [authority recovery publication](308-r1-fact-relation-corrected-successor-authority-recovery-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L2_PRIVATE_RUNTIME + L1_TESTS + L0_DOCUMENTATION`。本文只记录 bounded、private、
> handoff-owned Fact → Relation transition 候选；不恢复旧 ReviewSliceSet / Coverage composition，不选择 manifest successor，
> 不启动 persistence、public Review product 或 R2–R6。

## 1. exact base 与 authority

本候选从以下唯一 base 建立：

```text
commit = aabab17ee183f6eec29b38658b044734016b197f
tree   = 2b79c2802e35824284d3862f0f5573192f3c8843
```

该 base 是文档 308 最后门闭合后的 exact main。其 original Public CI、new exact-main Public CI、Browser Smoke、fresh
README/doc307/doc308/milestones anonymous installed-product readback与independent reconciliation均已完成；因此
`R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。

本文只消费这段新 authority。doc297旧授权仍为`PRESERVED / NOT_CONSUMABLE`，#346 exact-main Public CI
`39321768248` attempt 1的required Starter `net::ERR_NO_BUFFER_SPACE`失败、Artifact `12221668728`与底层原因
`UNKNOWN`继续保留，不被本候选或任何后继PASS回填。

## 2. 候选实现面

候选增加一个可区分的private transition：

```text
r1-fact-handoff-relation-transition/0.1
r1-fact-relation-handoff-claim/0.1
r1-fact-relation-stage-applicability/0.2
r1-fact-relation-product-closure/0.1
r1-fact-relation-obligation-projection/0.1
r1-fact-relation-transition-admission/0.1
```

施工面由三部分组成：

1. Fact consumer增加内部handoff domain。legacy consumer只能签发legacy continuation或Coverage handoff；Relation
   transition必须从专用combined-policy Fact consumer取得一次性handoff。两个domain不能交叉消费；
2. application从同一sealed Policy构造Fact / Relation stage applicability，从完整authoritative FactSet与完整Fact handoff
   history构造逐accepted product/path closure、三类total Fact partition与完整Relation obligation universe；
3. transition复用文档306冻结的corrected import-form Provider、原BudgetContext、deadline、stop/revocation与request
   provenance，独立核对expected / assigned / emitted / terminal后才签发private admission与one-shot continuation。

旧Provider、旧wire、public/default composition、Schema、Profile、Policy与已有Fact truth bytes不变。

## 3. 完整Policy与stage ownership

`/0.2` applicability只接受两个bounded Policy shapes：

```text
{python-ast, review-relation-derivation}

{python-ast, python-ast-advisory, review-relation-derivation}
```

`python-ast`与可选的`python-ast-advisory`归FACT；`review-relation-derivation`归RELATION。每个stage同时
copy-own applicable与non-applicable两侧，cross-stage reconciliation机械证明union完整、intersection为空且每个row只有一个
owner。unknown、missing、duplicate、requiredness或composition-mode drift均fail closed。完整Policy canonical bytes与
`policy_digest`继续绑定exact world；相同semantic projection不能继承另一份Policy的attempt或authority。

## 4. complete Fact truth 与per-product closure

Relation transition一次性领取完整Fact handoff source。carrier copy-own：

```text
parse partition
Fact projection U / E / blockers
complete Provider terminal history
complete authoritative FactSet
whole-attempt BudgetContext snapshot
```

并记录完整source canonical SHA-256。FactSet不被过滤或替换。每个accepted product的closure同时绑定：

```text
accepted product identity
parse obligation identity
product semantic digest
exact git path
exact source object / bytes / sha256
exactly one same-product MODULE fact
all same-product Facts and provenance refs
```

所有product Fact集合两两不交且并集等于完整FactSet。path string本身不取得product authority；foreign path、重复MODULE、
dangling Fact、overlap或FactSet filter均停止。

total Fact partition为：

```text
STRUCTURAL_ANCHOR       = per-product MODULE
APPLICABLE_SUBJECT      = IMPORT_DECLARATION
PROFILE_NON_APPLICABLE  = remaining complete Facts
```

三类互斥且并集等于完整FactSet。`CLASS / FUNCTION / METHOD`等non-applicable Facts保留原identity、provenance与handoff
history，不被重写成缺失或已履责。

## 5. successor obligation 与frozen Provider assignment

每个current import obligation使用新的private `obligation_id`，至少绑定：

```text
complete fact_set_digest
sealed policy_digest
Relation profile identity / version / digest
complete product_closure_digest
accepted product identity and exact path
same-product MODULE fact identity
relation family / kind and subject role
subject Fact identity
obligation projection function identity
exact legacy-compatible Provider observation_item_id
```

因此successor obligation identity与Provider现有observation item identity明确分层：前者承担handoff-owned transition证明，
后者保持已冻结Provider wire与算法不变。application从完整obligation universe生成逐Provider assignment；Provider只执行分配的
legacy-compatible observation items，不能从candidate、actual output或成功项反推denominator。

每个assigned Provider-obligation pair必须恰有一个terminal outcome。expected / assigned / emitted进行双向、基数、唯一性、
Provider requiredness、request provenance、attempt-start与exact coordinates核对；遗漏、重复、foreign、partial assignment或
terminal partition不完整均不能取得admission。

known-empty只在完整Policy、Fact handoff、FactSet、per-product closure、total partition与projection全部成立时存在；两个required
Provider仍必须真实执行、`COMPLETED`并residue-free release。empty不等于Fact missing、handoff未claim或无需执行。

## 6. carrier、admission 与authority ceiling

private carrier同时绑定完整Fact handoff source、stage ownership、product closure、Fact partition、successor obligations、frozen
Provider domain、request/terminal/receipt lineage、RelationSet与original same-attempt context。`carrier_digest`覆盖完整carrier，
`admission_digest`再绑定所有admission pointers。live validation会从authoritative operands重算applicability、closure、partition、
projection与Provider domain，并核对nested digests和cross-document links；只重算外层digest不能掩盖内部漂移。

continuation ceiling固定为：

```text
private Relation transition = true
ReviewSliceSet              = false
Coverage                    = false
manifest                    = false
persistence                 = false
public Review               = false
```

相同bytes、digest、limits或semantic output都不能恢复已消费、失败、revoked或foreign attempt的claim。

## 7. prequalification findings

正式资格化前的working-byte review保留十六项修正：subject identity/path混用、独立assignment order与terminal multiplicity
过度假设、Coverage/Relation handoff authority串域、首版domain guard对required-non-success Coverage路径的回归、admission未绑定
完整carrier、Fact partition缺失STRUCTURAL_ANCHOR、successor obligation identity未绑定profile/product/MODULE，以及carrier未
copy-own完整Fact handoff history；doc309初稿还把正确commit旁的base tree误抄成了近似字符串，现已用`git rev-parse
HEAD^{tree}`得到的exact tree替换。最后两项是live validation未把carrier source/context/provenance与独立持有的live operands
重新绑定，以及只核request/terminal摘要、未从frozen wire重建receipt与RelationSet；现已增加外部source bytes绑定、whole-attempt
context/provenance复算、逐Provider request/terminal validation与terminal-driven RelationSet recomposition。

第10/11项修正后的首次transition suite在import阶段失败：request validator位于source-operation application，而terminal
constructor/validator属于relation-observation application，首稿错误地从同一模块导入三者。该1-test loader failure作为
`PREQUAL-REVIEW-012`保留；导入所有权已纠正，必须以新run identity复验。

导入修正后的下一run执行31 tests并产生18 errors：新增carrier-composition helper被插入到既有RelationSet constructor的return
以前，使所有正常RelationSet构造返回`None`。该`PREQUAL-REVIEW-013` run保持原身份；constructor return已恢复到helper定义以前。

return恢复后的下一run仍为31 tests / 18 errors：live validator再次调用带当前时间的provenance constructor，导致original
`resolved_at`必然不等于fresh timestamp。该`PREQUAL-REVIEW-014` run原样保留；实现改为在carrier外绑定original provenance
canonical bytes，只从exact inputs复算稳定repository/ref/resolver坐标。

后续direct reseal证明，handoff claim id、transition attempt id、attempt timestamp及admission pointers若一起改写，内部引用与摘要仍
可自洽；这是`PREQUAL-REVIEW-015`。实现现把三项original transition identity作为carrier外operand绑定。另一反例把不同sealed
Policy下完整合法的Provider request/terminal lineage拼入原carrier，并共享同一request provenance；内部request验证仍可通过。
`PREQUAL-REVIEW-016`据此要求每个Provider request的source、Policy、analysis scope、slice policy与profile digest直接重绑外层live
`DerivationInputSet`。两项单测首败及各自修正后的PASS均保留独立身份。

这些finding均在commit、PR、formal product run与readback identity产生以前修正；没有可覆盖的正式失败。修正前working logs继续
保留且不得作为final qualification。final bytes必须重新完成全部测试与semantic matrix。

## 8. direct falsifiers 与当前本地见证

新增private transition tests直接覆盖：完整five-kind world、multi-path、known-empty required execution、filtered FactSet、duplicate
MODULE、foreign path、one-shot claim、fresh equal-world attempt、legacy/Relation handoff domain隔离、CID-001..012、carrier/admission
resealed tamper、external attempt identity、foreign exact-input lineage、Provider family narrowing/drift、missing/duplicate/foreign
terminal与complete handoff history。冻结Provider的
`RPIF-000..015`继续覆盖import-form occurrence、same-path parent、complete assignment、terminal partition、legacy ordinal与
CPython 3.10 projection。

当前working-byte witness包括：

```text
latest post-fix transition suite: 33 / 33 PASS
latest post-fix combined focused: 108 reported / 107 passed / 1 skipped
final focused Python 3.10 normal / -O: each 108 reported / 107 passed / 1 skipped
final focused Python 3.13 normal / -O: each 108 reported / 107 passed / 1 skipped
final full Python 3.10 normal / -O:    each 564 reported / 561 passed / 3 skipped
final full Python 3.13 normal / -O:    each 564 reported / 562 passed / 2 skipped
final five-world semantic digest:     2bd6c43da6a1a24450031df71638f83533527b93b05fa68076545eafaa9f9193
```

第一次标记为final的focused四格曾各取得101 reported / 100 passed / 1 skipped，随后Python 3.10 normal full取得
557 reported / 554 passed / 3 skipped；但第10/11项finding在该full格运行期间被发现，因此五份成功日志均改名为
`pre-fix-010-011-nonqualifying`并永久保留，qualification effect为`NONE`。修正后的final matrix已经从零重跑，未消费这些旧日志。

第一次final semantic comparison没有PASS：报告设施按attempt-bound `obligation_id`的顺序投影assigned obligations，使同一稳定
assignment在不同attempt / `-O`格产生139个列表位置差异。该
`SEMANTIC_REPORT_ASSIGNMENT_ORDER_PROJECTION_ERROR`、四份0.1报告与差异诊断保持原身份；机械分类确认全部差异路径只位于
`provider_assignments[*].assigned_obligations[*]`，未建立产品语义分歧。versioned 0.2设施改为按完整稳定义务内容排序，同时继续保留
原始`assigned_observation_item_ids`、完整义务语义和Provider descriptor。新四格对default、multi-path、known-empty、optional-advisory
与UTF-8-SIG五个world逐字相等，得到上列共同digest；四个stderr均为空。

compile proof facility的前两次运行也完整保留。attempt 1指定独立`PYTHONPYCACHEPREFIX`但没有先创建根目录，Python
3.10 / 3.13各产生108项`FileNotFoundError`；机械分类为`COMPILEALL_PYCACHE_PREFIX_ROOT_SETUP_ERROR`。attempt 2先创建根目录，
但长证据路径镜像后的目标达到277--319字符，再次各产生108项`FileNotFoundError`；机械分类为
`COMPILEALL_PYCACHE_PREFIX_PATH_LENGTH_ERROR`。两次记录均没有`SyntaxError`或`IndentationError`，不能建立产品编译失败。
attempt 3使用fresh短隔离前缀`C:\\vt310a3`与`C:\\vt313a3`，两格`compileall -q`均exit 0且stderr/stdout为空；两个空日志
SHA-256均为`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

首个pre-PR commit暴露了另一项证明设施scope错误：工作树上的`git diff --check`不会枚举untracked doc309，因而此前空日志
没有覆盖本文头部两处Markdown hard-break行尾空格。commit-range check在commit `9896b654…`上首次看见这两项并以exit 2
停止；该commit、失败输出及错误的local qualification attempt 1 / evidence seal attempt 1全部保留为
`UNTRACKED_FILE_EXCLUDED_FROM_PRECOMMIT_DIFF_CHECK`，qualification effect为`NONE`。最终字节移除行尾空格，改用
exact base-to-candidate commit-range检查并重新生成本地资格与seal。

final focused/full、canonical semantic comparison、compile、`git diff --check`、Markdown/local links、global/local hygiene、
forbidden public export、exact eight-path scope与primary `audit.json` continuity均已闭合。本地结果只使候选取得
`LOCAL_GATES_PASS`；在single candidate commit、original PR、protected merge、exact-main gates、fresh installed-product readback、
independent reconciliation与finite closeout完成以前，仍为`NOT_QUALIFIED / NOT_FROZEN`。

## 9. qualification gates 与状态上限

候选必须依次完成：

1. Python 3.10.6 / 3.13.13 × normal / `-O` final focused与full Review Attention matrix；
2. 四格canonical semantic projection一致；
3. compile、`git diff --check`、Markdown/local links、global/local hygiene、private export、exact scope与primary audit continuity；
4. 单一candidate commit与original PR Public CI；
5. protected exact-head merge；
6. new exact-main Public CI与Browser Smoke；
7. fresh anonymous installed-product README/doc309/milestones diagnostic/formal readback；
8. independent reconciliation与finite closeout。

任一non-success保留原身份并停止当前资格链。全部闭合后状态最多为：

```text
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_EXACT_MAIN_VERIFIED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_READBACK_QUALIFIED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`FROZEN`必须由后继独立docs-only publication及其完整资格链发布。冻结以后仍须返回CONTROL LOOP，重新审计旧
ReviewSliceSet / Coverage composition是否获得新的可消费authority；本文不自动恢复它。
