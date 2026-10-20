# R1 Relation Provider import-form conformance corrected successor 私有实现候选

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE`。
>
> 施工基线：`main@4411c02c7278b8ecb4aa36415fdea77e7cb90168`，tree
> `7e13b5d8acf374c5e9e854554824b28ad606f677`。
>
> 本文认领[文档304](304-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-authorization-publication.md)
> 已生效的bounded private implementation A–J；不发布merged、exact-main verified、readback qualified或frozen状态，不恢复旧composition
> authority，不选择manifest successor或persistence，也不启动Coverage、public Review产品或R2–R6。

## 1. CONTROL LOOP 与已生效授权

文档304由PR #349 final head `b5d66949657449efa5cbfc6315d810696f76e861`从
`main@0f0c93a7b0fc2d33572dbb284ab7e54a997ea88b`建立；candidate与merge tree均为
`7e13b5d8acf374c5e9e854554824b28ad606f677`，受保护合入后的exact main为
`4411c02c7278b8ecb4aa36415fdea77e7cb90168`。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #349 original Public CI | `39344764110` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39348029772` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39348029859` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc303、doc304与milestones为4/4 qualifying PASS；independent reconciliation与
178-artifact closeout分别为：

```text
cbe3144f61e7e68b9bee9af11f463ebc38ec017d50fd98c2a6fde4742dc19d2e
fe760ad7716b0d62ec22b37a906e6031e7ff152bb4838ec5e7114dbb69d815a0
```

closeout stdout self-capture mismatch保持原身份，semantic effect为`NONE`。因此
`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效。
fresh CONTROL LOOP重新核对remote main、exact base、冻结合同、#346 retained failure、doc302 failure boundary、doc303 qualified
feasibility、旧Provider/public/default composition与primary `audit.json`；没有更早反例要求重开文档299/300或文档304 authority。当前最小
合法施工面仍是private Provider successor A–J。

## 2. versioned private identity 与旧世界隔离

本候选新增一组显式private successor identity：

```text
launch keys
  import-form-observation-a
  import-form-observation-b

provider ids
  relation-import-form-provider-a
  relation-import-form-provider-b

parser
  cpython-3.10.6-import-alias-occurrence-parser / 0.1-test

observation profile
  closed-python-import-form-observation / 0.1-test

source-operation wire
  veritrail-review-relation-cell/0.5
  veritrail.review.provider-operands/0.7
```

旧`observation-a/b`、closed Provider descriptors、legacy profile与`0.4 / 0.6` wire bytes保持原语义。binding family按完整exact
descriptor解析；old/new混用、用old wire承载successor request、用successor wire承载old request均fail closed。public exports、默认
composition入口、workflows、Schema、Policy/Profile与Fact truth未被改写。

## 3. A–J 实现映射

| ID | 本候选实现 |
| --- | --- |
| A | 通过既有`DerivationInputSet`、完整FactSet、sealed Policy/Profile、Fact handoff source与application assignment进入同一attempt；不从Provider output恢复authority。 |
| B | 新增exact private descriptor/binding/profile/wire identities；旧identity与默认composition保持不变。 |
| C | 以`ast.parse(..., feature_version=(3, 10))`完整枚举accepted product/path的`Import`与`ImportFrom` alias occurrence，覆盖multi-alias、relative、star、nested与multi-path。 |
| D | 以path、raw byte span、alias ordinal与完整semantic attributes双向核对occurrence与authoritative `IMPORT_DECLARATION` Facts；missing、duplicate、extra、semantic drift与cross-path均拒绝。 |
| E | 对每个accepted path要求恰有一个MODULE；IMPORT只能绑定同path MODULE，path集合不闭合或parent交换均拒绝。 |
| F | legacy top-level single-alias `ast.Import`保留原body ordinal；其余form按冻结rank从`len(tree.body)`之后分配确定、无碰撞extension ordinal。 |
| G | Provider只执行application分配的完整obligation universe；foreign、遗漏、重复、partial assignment或terminal partition不闭合均不能qualification。 |
| H | 复用既有request validation、canonicalization、ProviderRun qualification与RelationSet admission；不创建第二套denominator或admission authority。 |
| I | 复用same-attempt `BudgetContext`、deadline、stop、revocation、run lifecycle与one-shot admission；相同bytes或digest不恢复continuation。 |
| J | 直接实现`RPIF-000..015`、UTF-8-SIG与qualification/admission集成falsifiers，并在Python 3.10 / 3.13 × normal / `-O`四格执行同一final bytes。 |

完整FactSet从未被过滤成MODULE+IMPORT视图；successor domain只从完整truth构造适用obligation。unrelated Fact kinds仍保留原identity，
Relation Provider只取得被分配义务的execution responsibility，不取得stage applicability、denominator、qualification、admission或
continuation authority。

## 4. occurrence / Fact exact binding

每个source path先从原始bytes建立完整occurrence universe。UTF-8与UTF-8-SIG均严格解码；AST line/column span转换回raw byte
offset。UTF-8-SIG首行坐标显式加回三字节BOM前缀，避免解析文本坐标与authoritative Fact anchor位于不同byte world。

双向核账键为：

```text
git_path_hex
+ start_byte / end_byte
+ alias_ordinal == Fact local_ordinal
+ canonical import-form semantic attributes
```

`Import`记录完整module parts与alias；`ImportFrom`记录relative level、module parts、imported name与alias，star作为普通冻结
`imported_name`参与精确比较。expected occurrence keys与actual Fact keys必须集合相等；任一侧遗漏、重复或额外成员都会拒绝整个Provider
run，不能通过缩小分母制造成功。

## 5. 完整assignment与per-path closure

successor domain允许完整FactSet、多path与任意非Relation-applicable Fact kinds，但对每个出现source bytes的path必须存在且只存在一个
MODULE。`LEXICAL_CONTAINS` candidate从该path MODULE指向对应Import Fact；`IMPORT_TARGET_LITERAL`从同一Import Fact指向完整literal
target。不同path不能交换MODULE parent。

Provider A的完整assignment是每个Import Fact的`LEXICAL_CONTAINS`；Provider B的完整assignment是每个Import Fact的
`LEXICAL_CONTAINS + IMPORT_TARGET_LITERAL`。actual assignment必须与这两个闭集之一精确相等；每个assigned item必须产生恰一个
candidate与一个terminal outcome。candidate bytes与outcome partition随后由既有qualification和admission重新构造，而不是信任
Provider自报。

## 6. legacy兼容与确定extension ordinal

对legacy top-level single-alias `ast.Import`，`LEXICAL_CONTAINS.local_ordinal`继续等于其`tree.body`位置，所以历史candidate/outcome
bytes不变。multi-alias、`ImportFrom`与nested imports进入extension集合，按raw span、form、alias ordinal与canonical attributes排序，
从`len(tree.body)`开始编号。rank重复或任何最终ordinal碰撞都fail closed。

这不是把旧ordinal规则静默扩成另一种算法。legacy子域保持原值；新增form只在versioned private successor identity下使用可区分的
extension ordinal。

## 7. direct falsifiers

final private suite含18项测试：

```text
RPIF-000..015
+ UTF-8-SIG end-to-end Fact binding
+ successor qualification / RelationSet admission integration
```

它们直接覆盖legacy bytes/ordinal、multi-alias `Import`与`ImportFrom`、relative/star、nested extension ordinal、multi-path parent、
missing/duplicate/drift Fact、partial/duplicate assignment、missing/duplicate/foreign terminal partition、CPython 3.10.6 occurrence reference
vector、extension-rank collision、相同bytes不同run identity、old/new双向wire rejection与BOM raw offsets。

`RPIF-013`除断言`feature_version=(3, 10)`外，还把完整occurrence projection与显式CPython 3.10.6 reference vector比较；参数本身
不被冒充为版本语义证明。

## 8. final local qualification

修正后的focused matrix由18项new-provider tests与77项既有Relation/qualification/admission regressions组成。四格均使用当前final
runtime/test bytes：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 95 reported / 94 passed / 1 skipped |
| 3.10.6 | `-O` | 95 reported / 94 passed / 1 skipped |
| 3.13.13 | normal | 95 reported / 94 passed / 1 skipped |
| 3.13.13 | `-O` | 95 reported / 94 passed / 1 skipped |

完整Review Attention suite也在同一final implementation bytes完成：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 531 reported / 528 passed / 3 skipped |
| 3.10.6 | `-O` | 531 reported / 528 passed / 3 skipped |
| 3.13.13 | normal | 531 reported / 529 passed / 2 skipped |
| 3.13.13 | `-O` | 531 reported / 529 passed / 2 skipped |

独立semantic projection删除run timestamps后，四格逐语义一致：

```text
1d663d655365cddbcb00375066fbd523475586cc754ee461be3695628ed06c6c
```

comparison evidence SHA-256为：

```text
5126bdfd509e75cc3097fe298a410bd556599c9f8dcfd2da13a2bbae2d2d4616
```

Python 3.10/3.13 compileall、`git diff --check`、global/local hygiene、public export/pyproject/workflow diff guard与primary
`audit.json` continuity均PASS。测试是当前candidate witness，不会预先替代original PR、exact-main或installed-product门。

## 9. retained prequalification / proof-facility history

两项source review finding在任何formal qualification以前被发现并修正：

1. `PREQUAL-REVIEW-001`：UTF-8-SIG首行span未加回BOM三字节，属于private implementation defect；修正raw byte映射并增加
   end-to-end test。
2. `PREQUAL-REVIEW-002`：原`RPIF-013`只检查`feature_version`，proof target过弱；增加显式3.10.6 occurrence vector与old/new
   reverse wire rejection。

finding记录SHA-256为：

```text
9349962fa1f71081a5a9a88e8f10fdc9ed4221fe90100a04156d897260d607f2
```

修正前四格focused 94-test日志保留，但不得作为final qualification。semantic report proof facility attempt 1调用不存在的
`provider_runs_copy`，归为`SEMANTIC_REPORT_PROOF_FACILITY_SCHEMA_METHOD_ERROR`；attempt 2把`started_at / finished_at`纳入
semantic projection，四格digest不一致，归为`SEMANTIC_REPORT_PROJECTION_INCLUDED_NON_SEMANTIC_TIMESTAMPS`，记录SHA-256：

```text
a75d721b56c58f1a8bb864b575824942868410920b55afde6ea459534259a2cf
```

attempt 3只从projection去除非语义timestamps后PASS。三个attempt全部保留，未修改产品oracle、candidate bytes或任何正式历史。

final local validation attempt 1在读取`git status --porcelain`时对整个stdout使用`strip()`，导致首行前导状态空格被删并把
`AGENTS.md`误读为`GENTS.md`；它被归为`LOCAL_VALIDATION_PROOF_FACILITY_LEADING_WHITESPACE_TRIM_ERROR`并保留。fresh attempt 2
只把读取改为去除尾部换行后在当时bytes上PASS；本文补记该历史后，attempt 3再对final bytes执行同一检查并PASS。candidate scope与
产品字节未因该设施错误改变。

Markdown structure checker的首份PASS报告还因PowerShell console redirection把非ASCII heading保存为mojibake；原报告保持，fresh
attempt改由proof facility直接写UTF-8后再次PASS。该输出编码损失没有改变被检查的Markdown bytes、link/headings verdict或资格结论。

## 10. tracked scope 与资格链

本候选的预期tracked scope只允许：

```text
README.md
AGENTS.md
docs/305-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_relation_import_form_provider.py
plugins/review-attention/src/veritrail_review/_relation_observation_binding.py
plugins/review-attention/src/veritrail_review/_relation_observation_domain.py
plugins/review-attention/src/veritrail_review/_relation_observation_qualification.py
plugins/review-attention/src/veritrail_review/_relation_set_admission.py
plugins/review-attention/src/veritrail_review/_source_operation_relation_observation_application.py
plugins/review-attention/src/veritrail_review/_source_operation_relation_observation_worker.py
plugins/review-attention/tests/test_relation_import_form_provider.py
```

doc290–304、public Schema、Policy/Profile、fixtures、workflows、manifest、persistence、Coverage、public Review与post-R1计划必须保持
base bytes。完整资格链为：

```text
final implementation bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
    -> return CONTROL LOOP
```

本候选不得借用文档304 readback、相同semantic digest、旧Provider success或后继PASS替代任一门。只有独立docs-only freeze
publication完成自己的资格链以后，`FROZEN`才可能生效。

## 11. 当前状态与 stop line

本文只发布：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文不宣称implementation已经合入、exact-main verified、readback qualified或frozen。Provider successor即使完成全部candidate资格，也只会
形成新的CONTROL LOOP输入；旧Fact handoff → Relation composition authority继续不可消费，必须独立重审共同exact-input world、
same-attempt claim、manifest与剩余R1边界。
