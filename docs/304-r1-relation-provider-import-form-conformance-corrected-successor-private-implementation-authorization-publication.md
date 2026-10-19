# R1 Relation Provider import-form conformance corrected successor 私有实现授权发布候选

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@0f0c93a7b0fc2d33572dbb284ab7e54a997ea88b`，tree
> `72c9e720edc3099e0d60c74821d41db0b9de8f2c`。
>
> 上游：[correction contract](299-r1-relation-provider-import-form-conformance-correction-contract.md)、
> [独立冻结发布](300-r1-relation-provider-import-form-conformance-correction-contract-freeze-publication.md)、
> [exact-main qualification failure boundary](302-r1-relation-provider-import-form-successor-feasibility-exact-main-qualification-failure-boundary-audit.md)与
> [feasibility recovery](303-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-recovery.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只发布一份条件化的bounded private implementation
> authority；不修改runtime、tests、workflows、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage或
> public Review产品。本文自己的完整资格链闭合以前，`ALLOWED`不生效。

## 1. publication输入已经取得资格

文档303由PR #348 final head `68e206ca8a7f22ba63b3e6672f23039446a4a796`从
`main@869e8190d4fcc6f3c046bb1661d6d27f1da36283`建立；candidate与merge tree均为
`72c9e720edc3099e0d60c74821d41db0b9de8f2c`，受保护合入后的exact main为
`0f0c93a7b0fc2d33572dbb284ab7e54a997ea88b`。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #348 original Public CI | `39336445825` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `39340041479` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `39340041520` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc303与milestones各有唯一`FORMAL_READBACK_PASS`；三份观察的P1/P2 coverage均为
`COMPLETE`，Core均为`PASS`，Plan、collection session、handoff与output identity互不复用。independent reconciliation与
132-artifact closeout分别为：

```text
4e03b11727cca784a0797bdbaeb9d66fb44be886e8c4072b077c0395a534e430
bbc6f3b018da7591737526a767b5c98fd7b64feda33b132d6ca880c3235ff8e1
```

因此文档303现在是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。文档301仍是merged but not-qualified；#346的
`net::ERR_NO_BUFFER_SPACE`失败、Artifact与`UNKNOWN`底层根因保持原身份。文档302继续只证明failure boundary；任何后继PASS都没有
回填或解释旧world。

readback设施还保留三项setup/operator错误：本地尚未fetch新merge object便执行`git show`、假设固定Python 3.13安装路径、以及把
render-only diagnostic误当成会产生formal summary。三者均在formal观察以前或之外被归为`qualification_effect = NONE`；后继使用
fresh identity并验证真实diagnostic边界，没有删改原记录。

## 2. 授权对象是bounded A–J，不是开放式Relation重写

本文条件化授权的唯一施工面是文档299合同与文档303 qualified feasibility共同限定的private successor A–J：

| 项 | 最小施工责任 |
| --- | --- |
| A | 绑定同一attempt的完整Fact handoff、完整FactSet、sealed Policy/Profile与application-owned assignment；先复核claim仍live。 |
| B | 新建versioned private Provider/descriptor identity；旧identity不得静默扩大import-form语义。 |
| C | 从accepted product/path source bytes完整枚举CPython 3.10.6 `Import` / `ImportFrom` occurrence，包括multi-alias、relative、star、nested与multi-path。 |
| D | authoritative `IMPORT_DECLARATION` Facts与source occurrences双向一一exact binding；missing、duplicate、extra、semantic drift与cross-path均拒绝。 |
| E | 按accepted product/path建立MODULE closure；IMPORT只能绑定同path MODULE，不允许跨path交换parent。 |
| F | 保留legacy top-level single-alias `ast.Import`的body ordinal与candidate/outcome bytes；expanded forms使用确定、无碰撞的extension ordinal。 |
| G | 只执行application已经分配的完整obligation universe；每项恰有一个terminal outcome，foreign、遗漏、重复或partial assignment均不得qualification。 |
| H | 复用既有request validation、canonicalization、ProviderRun qualification与RelationSet admission；不得创建第二套authority或由actual output反推denominator。 |
| I | 保持same-attempt BudgetContext、deadline、stop、revocation与continuation ceiling；digest holder不能恢复已失效authority。 |
| J | 以`RPIF-000..015`和四格Python 3.10 / 3.13 × normal / `-O`为最低falsifier面，并保留#346失败、doc302 closeout与doc303资格链。 |

完整FactSet与Policy bytes/digest始终保持。applicability projection只回答本stage应承担哪些requirement；obligation projection只构造
完整适用义务，不替换Fact truth。Provider算法不拥有stage applicability、denominator、assignment、qualification、admission或
continuation authority。

## 3. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded private Provider successor A–J
+ 增加对应private tests / audit fixtures
+ 运行既有qualification/admission链与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改public Schema、Policy/Profile、Fact truth或FactSet identity
过滤完整FactSet以适配Relation
把one MODULE粗放改成n MODULE而不做per-path closure
恢复或消费旧composition authorization
选择或实现manifest successor
选择persistence
启动Coverage、public Review、post-R1 Benchmark或R2-R6
发布tag / Release
```

`ALLOWED`也不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。实现必须拥有新的source、branch、candidate
head/tree、原始PR门、protected merge、exact-main双门、fresh installed-product readback与independent reconciliation；真实反例出现时
立即停止当前施工，只重开被击穿的最小边界。

## 4. 历史authority不能被偷换成当前授权

此前`R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED`仍是历史事实，
同时继续受`STOP_CONDITION_TRIGGERED`约束。本文发布的是更窄的新authority：只允许import-form conformance corrected Provider
successor A–J。

因此不得推导：

```text
old allowed history == current consumable authority
Provider successor allowed == composition allowed
Provider successor implemented == composition recovered
same semantic digest == same attempt authority
doc303 qualified == this publication effective
```

后继Provider实现若取得资格，也只能回到CONTROL LOOP重新审计Fact handoff → Relation composition的共同exact-input world；不能自动恢复
composition、manifest或Coverage施工。

## 5. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/304-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-authorization-publication.md
docs/milestones.md
```

doc290–303、runtime、tests、workflows、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage与post-R1计划必须保持
`0f0c93a…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
`git diff --check`、read-only hygiene、doc303全文件SHA、132-artifact closeout、三份formal identities、#346 retained failure与doc302
qualified history。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc303 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure / qualified-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用本publication的
original PR green、相同tree、相同semantic digest或后继PASS替代任何一门。

## 6. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`...PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持`...NOT_STARTED`。随后返回CONTROL LOOP，才允许在本文
ceiling内开始新的private implementation candidate；不得把authority publication本身算作实现证据。
