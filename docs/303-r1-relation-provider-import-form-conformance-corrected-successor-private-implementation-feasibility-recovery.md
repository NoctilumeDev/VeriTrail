# R1 Relation Provider import-form conformance corrected successor 私有实现可行性恢复候选

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_RECOVERY_CANDIDATE`。
>
> 坐标：`main@869e8190d4fcc6f3c046bb1661d6d27f1da36283`，tree
> `915f2559184c9bec00c8a3593b6a59e0e524254c`。
>
> 上游：[import-form conformance correction contract](299-r1-relation-provider-import-form-conformance-correction-contract.md)、
> [独立冻结发布](300-r1-relation-provider-import-form-conformance-correction-contract-freeze-publication.md)与
> [exact-main qualification failure boundary audit](302-r1-relation-provider-import-form-successor-feasibility-exact-main-qualification-failure-boundary-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文建立一份对既有失败历史承担新增责任的独立 feasibility
> candidate；不修改 runtime、tests、workflows、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage
> 或 public Review 产品，也不把文档301或其失败 world补写成通过。

## 1. CONTROL LOOP 与新增事实

文档301由PR #346合入`main@bd0cb9838545de0dd3a2e26486c6fa90df765962`。它的original Public CI
`39317208755` attempt 1为11/11 SUCCESS，Browser Smoke `39321768185` attempt 1为1/1 SUCCESS；但new
exact-main Public CI `39321768248` attempt 1为10/11，required Starter job `118308355830`在mobile首个loopback
document请求命中`net::ERR_NO_BUFFER_SPACE`并失败。该run没有rerun，fresh README/doc301/milestones readback没有启动，
文档301保持merged but not-qualified，`FEASIBILITY_AUDITED`没有生效。

文档302随后只审计该失败边界。PR #347 final head
`1586d096f6d51e9b54350e4b14324daaf2c3732c`从失败world的merge建立，candidate与merge tree均为
`915f2559184c9bec00c8a3593b6a59e0e524254c`；它只修改README、AGENTS、文档302与milestones，保持runtime、tests、
workflow、Browser分类、required lane、timeout和oracle字节不变。其original Public CI `39327705063`、new exact-main
Public CI `39330968073`与Browser Smoke `39330968165`均为attempt 1 SUCCESS，分别11/11、11/11与1/1。

fresh anonymous installed-product README、doc302、milestones为3/3 qualifying PASS；independent reconciliation与
131-artifact closeout分别为：

```text
071427e5656dbc65d9b4ea18ce148a02d490c363d4761199891b10c20bc68339
92d671cf074919a2116043bfa509a4e571dec2499ba4c80d27af0b66dc568a5a
```

因此failure boundary现为qualified history。这里出现了文档302 §6要求的两项新增事实与责任：

1. 同一冻结product lane在保持workflow/runtime/tests/oracle不变的后继docs-only world中完成，证明不需要通过弱化产品门来恢复；
2. 后继feasibility必须把#346 exact-main失败、Artifact、`UNKNOWN`根因与doc302 closeout作为自己的输入历史并独立对账，不能只重放文档301。

后继成功不解释#346为什么失败，也不把#347 PASS回填#346。它只使一份新的、有不同字节与责任的feasibility candidate成为合法。

## 2. failure identity 与恢复资格严格分离

#346 failed-evidence Artifact继续固定为：

```text
run = 39321768248 attempt 1
job = 118308355830
artifact id = 12221668728
archive SHA256 = 9a4975a882784ca91266c21a2a27ded4cc6232b3f5b4cdfabb57596db8c1fa1c
raw failure = net::ERR_NO_BUFFER_SPACE
classification = network:mobile / HostSocketNoBufferSpace
subject failure = NOT_ESTABLISHED
candidate regression = NOT_ESTABLISHED
underlying host resource cause = UNKNOWN
```

本文不尝试把`UNKNOWN`升级成资源根因，也不借后继PASS证明旧attempt“本应通过”。恢复的是**新candidate取得资格的可能性**，不是
旧candidate的资格。以后任何reconciliation必须同时保留：

```text
#346 exact-main failure world
+ doc302 qualified failure-boundary history
+ current candidate own world
```

三者不能合并成一个attempt，也不能以相同source/runtime bytes推导相同authority。

## 3. semantic feasibility在当前 exact main重新复算

fresh audit使用新的audit-only identity
`r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-recovery/0.1`，在完整FactSet与
application-owned assignment上重新执行：

- CPython 3.10 Import / ImportFrom alias occurrence递归枚举；
- AST occurrence与authoritative `IMPORT_DECLARATION` Fact双向exact matching；
- per-product/path MODULE closure；
- legacy body ordinal与candidate/outcome bytes保持；
- non-legacy extension ordinal的稳定、无碰撞构造；
- complete assigned execution与exact terminal outcome；
- 既有canonicalization、qualification与RelationSet admission复用；
- foreign path、missing、duplicate、semantic drift与不完整assignment拒绝。

Python 3.10.6 / 3.13.13 × normal / `-O`四格分别得到相同semantic digest：

```text
provider successor feasibility recovery
a06190284adcef005010a3ceb069161f2f6528d6111abe5c90596723b5fbeb82

upstream corrected-successor continuity
0caf68d7a78b8ab1279399d5f3b0e258818010f366c2cac6816c7b0a1ef0474b
```

focused regression每格`Ran 77 tests / OK (skipped=1)`，即76 passed、1个explicit reference runtime/Windows skip。
这些结果只作本candidate的fresh witness，不继承文档301资格，也不拥有状态升级或实现授权。

## 4. bounded successor语义没有扩大

当前审计仍只支持文档301 §8的bounded A–J：exact upstream revalidation、versioned private binding、bounded occurrence
projection、bidirectional Fact binding、deterministic child identity、complete assigned execution、既有qualification/admission集成、
same-attempt lifecycle、`RPIF-000..015` falsifiers及continuation ceiling。

完整FactSet bytes/digest、sealed Policy、stage ownership、application-owned obligation universe与Provider responsibility均保持。Provider
仍不能自行选择eligible subset，不能由actual output反推denominator，也不能自证履责。本文没有创建新的public SPI、Schema、
manifest、persistence、Coverage或第二套qualification framework。

## 5. 新candidate承担的 qualification responsibilities

相对于文档301，本candidate新增的不是算法功能，而是资格责任：

1. source、local evidence与最终readback都绑定`869e819…`以后形成的独立exact world；
2. 本地与独立对账必须复算#346 failed run/job/Artifact/classification及其`UNKNOWN`边界；
3. 必须复算doc302的original/exact-main门、3/3 fresh readback、reconciliation与closeout；
4. 必须证明doc299/doc300、runtime/tests/workflow/oracle从当前base保持连续；
5. 自己的original PR与new exact-main required gates必须各自通过，任何non-success保留原身份；
6. fresh installed-product观察只在自己的exact-main双门闭合后启动；
7. 后继PASS只能支持本文，不得回填文档301或消除#346失败。

这使当前变更具有独立可审查语义，而不是空提交或平台重试载体。

## 6. 禁止的推论

即使本文最终取得资格，也不能推出：

```text
#346其实PASS
HostSocketNoBufferSpace根因已经确定
required Starter lane可选
corrected Provider runtime已经实现或授权
旧composition authorization恢复可消费
manifest successor已经选择
persistence已经选择
Coverage或public Review已经启动
R2-R6已经启动
```

如果本文自己的required gate再次失败，必须保留新world并重新执行CONTROL LOOP；不得以本文已有failure-history责任为由自动创建第三个
candidate。

## 7. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| import-form correction contract是否frozen | **是** |
| #346 exact-main failure是否永久保留 | **是** |
| doc302 failure boundary是否qualified | **是** |
| required product oracle是否需要修改 | **否** |
| semantic feasibility是否在current exact main重新成立 | **是，fresh audit witness** |
| 当前candidate是否相对#346增加资格责任 | **是** |
| bounded private implementation是否已授权或开始 | **否** |

因此当前存在一份合法的新feasibility candidate；它不重试文档301，而是以qualified failure history为新增输入，重新承担完整资格链。

## 8. 当前状态与 authority ceiling

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_EXACT_MAIN_FAILURE_BOUNDARY_AUDITED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_RECOVERY_CANDIDATE
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_NOT_AUDITED
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

## 9. 本candidate资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/303-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-recovery.md
docs/milestones.md
```

doc290–302、runtime、tests、workflows、fixtures、Schema、Profile、Policy、Provider、manifest、persistence、Coverage与post-R1计划必须保持
`869e819…` base bytes。final bytes至少完成四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
上游byte continuity、`git diff --check`、read-only hygiene、两组fresh audit与四格focused regression。

```text
final docs-only recovery candidate bytes / declared local gates
    -> original PR required gates
    -> continuously authorized exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-failure / failure-boundary reconciliation
    -> FEASIBILITY_AUDITED becomes qualified history for this candidate only
    -> return CONTROL LOOP
```

全部门闭合以前只能写candidate状态。闭合后最多允许fresh CONTROL LOOP判断独立docs-only implementation authorization publication；
不得自动修改runtime、恢复旧composition、选择manifest/persistence或启动Coverage、public Review、R2–R6或post-R1 Benchmark。
