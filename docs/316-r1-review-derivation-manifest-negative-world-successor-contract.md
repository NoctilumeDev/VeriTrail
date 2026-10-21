# R1 Review derivation manifest negative-world successor 最小合同候选

日期：2026-10-21

> 候选状态：`R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_CANDIDATE`。
> 本文自己的资格链与后继独立冻结发布全部闭合以前，本文不是 frozen contract，也不授权 Schema、fixture、
> producer、consumer、publisher、persistence 或 public Review 产品施工。
>
> 合同基线：`main@a4fb97ea1a98dbe3014bbae17635396e2d676c85`；tree
> `8b810bd2acb89bb0865ace2a92521e36617dcd6d`。
>
> 上游：[negative-world successor 可行性审计](315-r1-review-derivation-manifest-negative-world-successor-feasibility-audit.md)、
> [root binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)、
> [CoverageLedger 0.3 私有实现冻结](286-r1-review-coverage-ledger-0-3-schema-conformance-implementation-freeze-publication.md)与
> [composition 私有实现冻结](314-r1-review-slice-set-coverage-composition-private-implementation-freeze-publication.md)。
>
> 影响层级：`L0_DOCUMENTATION / CONTRACT_CANDIDATE_ONLY`。

## 1. CONTROL LOOP 与已资格化前提

文档315已由PR #362从
`base=add5a8c7359cf9f0a678ea2bf947ef3a9791f94d / head=b8dd91645faaa1ac46bf3206165376bd1d0af638 /
tree=8b810bd2acb89bb0865ace2a92521e36617dcd6d`受保护合入本合同基线。original Public CI
`39512467514`、exact-main Public CI `39515876073`与Browser Smoke `39515876085`均为attempt 1
SUCCESS，分别为11/11、11/11与1/1。

fresh anonymous installed-product readback对doc315、milestones与README各保留一份qualifying
`COMPLETE / PASS`。README第一次formal观察使用的长尾marker存在于exact Git/raw bytes，但不在当前稳定渲染窗口，
因此以`FORMAL_READBACK_ERROR`保留；versioned marker successor没有重跑前两个PASS，也没有覆盖该失败。
independent reconciliation、184-artifact finite closeout与独立完整性复核均为PASS：

```text
reconciliation = cefd7f3f37130cada58135060cfca5bde2afd0e6c94e49bb282914d015cda0a3
closeout       = f821a4ed7f94bfdedfc171806dd8b2f192e151652047e2efceca66a2af2d4470
integrity      = 184 / 184, mismatch = 0
```

因此本合同只消费以下已资格化事实：

```text
composition implementation = FROZEN
manifest successor feasibility = AUDITED / QUALIFIED_HISTORY
manifest successor contract = NOT_YET_FROZEN
manifest successor implementation = NOT_STARTED / NOT_AUTHORIZED
persistence = OPEN / NOT_SELECTED
public Review = NOT_STARTED
R2-R6 = NOT_STARTED
```

## 2. 被冻结的版本与职责

### 2.1 immutable 0.1

`schemas/review-derivation-manifest-0.1.schema.json`保持逐字节immutable；其SHA-256继续为：

```text
69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
```

0.1 transport合同只接受8项`COMPLETE`与4项`DIAGNOSTIC`。0.1 Schema的`schema_version`引用共享字面格式，
所以version dispatcher必须先于structural validator精确选择Schema；任何0.2文件都不得被路由到0.1 validator。任何consumer也不得把
未知version回退到0.1、按相似字段猜测版本，或把0.1 COMPLETE/DIAGNOSTIC历史重解释成negative-world transport。

### 2.2 successor identity

本合同选择唯一后继身份：

```text
file                    = schemas/review-derivation-manifest-0.2.schema.json
$id                     = https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-manifest-0.2.schema.json
title                   = VeriTrail Review R1 Derivation Manifest 0.2
bundle_kind             = R1_DERIVATION
schema_version          = 0.2
canonicalization        = veritrail-json-c14n/1
new outcome_kind        = COVERAGE
cross-artifact identity = r1-review-derivation-manifest-coverage-topology/0.1
```

`COVERAGE`表示“实际存在的set carriers与最后一份CoverageLedger共同构成transport”，不是PASS、COMPLETE、
publication authority或live continuation。root truth仍只由已验证CoverageLedger 0.3拥有；manifest不得复制
`ARTIFACT_PRESENT / QUALIFIED_ABSENT / QUALIFIED_UNKNOWN`字段。

## 3. 0.2结构合同

0.2继续使用0.1的五字段对象边界：

```text
bundle_kind
schema_version
canonicalization_profile
outcome_kind
files
```

`additionalProperties=false`。0.2 Schema必须继续接受0.2的`COMPLETE`与`DIAGNOSTIC`分支，其role/path/order与0.1
完全相同；新`COVERAGE`分支只允许：

```text
SOURCE_SNAPSHOT      source-snapshot.json
REVIEW_POLICY       review-policy.json
DERIVATION_PROFILE  derivation-profile.json
DERIVATION_EVIDENCE derivation-evidence.json
[FACT_SET            fact-set.json]
[RELATION_SET        relation-set.json]
[REVIEW_SLICE_SET    review-slices.json]
COVERAGE_LEDGER      coverage-ledger.json
```

方括号表示carrier可不存在，不表示Schema自行决定存在性。固定前缀为4项，Ledger必须最后；三个set role最多各一项且只能按
Fact、Relation、Slice顺序出现。总数为5–8。每个file entry继续只含：

```text
role
path
sha256
size_bytes
semantic_digest
```

role/path必须一一对应；路径不得自定义、绝对化、含`..`、别名或重复。Schema不增加root state、reason、terminal history、
attempt、authority或placeholder字段。

## 4. cross-artifact conformance合同

Schema structural validation不能证明`files`与Ledger root truth一致。0.2资格必须另外运行
`r1-review-derivation-manifest-coverage-topology/0.1`，且只在以下前提满足后返回PASS：

1. exact version dispatch已选择0.2；0.1、未知version与fallback均不能进入本conformance；
2. `coverage-ledger.json`实际存在，先通过CoverageLedger 0.3 JSON Schema与
   `r1-review-coverage-ledger-root-binding/0.1`；
3. manifest中每个role唯一、role/path严格对应、顺序符合第3节、Ledger entry恰为最后一项；
4. 每个entry的`sha256`与`size_bytes`从对应实际carrier raw bytes复算；
5. 每个set carrier的semantic digest由其自身既有digest字段取得，并与entry完全相等；
6. 对每个`ARTIFACT_PRESENT` root，恰有一份对应set carrier，且entry semantic digest等于
   root `artifact_digest`；
7. 对每个`QUALIFIED_ABSENT`或`QUALIFIED_UNKNOWN` root，对应set carrier必须不存在；
8. Ledger entry semantic digest等于已验证Ledger的`coverage_ledger_digest`；
9. source/policy/profile/evidence前缀的既有digest binding继续成立；
10. unsafe、interrupted、foreign-attempt或未完成composition world没有调用producer/publisher的authority。

conformance只验证给定manifest与实际文件集合，不创建缺失文件、不修正Ledger、不推断root state、不授予publication或
same-attempt live authority。

## 5. compatibility corpus与falsifier分母

后继实现若获授权，必须新增独立fixture：

```text
tests/fixtures/review-derivation-manifest-0.2/compatibility-cases.json
```

其qualified positive universe必须恰好覆盖已冻结CoverageLedger 0.3八个world：

| world | set carrier projection | outcome |
| --- | --- | --- |
| normal | Fact + Relation + Slice | COVERAGE |
| branch-empty | Fact + Relation + Slice | COVERAGE |
| slice-partial | Fact + Relation + Slice | COVERAGE |
| zero parse denominator | none | COVERAGE |
| all parse rejected | none | COVERAGE |
| projection blocked | none | COVERAGE |
| required Provider non-success | none | COVERAGE |
| qualified unknown | Fact only | COVERAGE |

前三个world仍可另外证明0.1 COMPLETE兼容，但不得因此省略0.2 COVERAGE正例。0.1 DIAGNOSTIC继续是独立历史，不承担Ledger
transport。

最小负例分母冻结为：

| ID | 必须拒绝 |
| --- | --- |
| `RDMC-000` | 0.1 bytes被改写或0.2回退到0.1 |
| `RDMC-001` | 未知schema version或conformance identity |
| `RDMC-002` | COVERAGE缺少Ledger |
| `RDMC-003` | 重复role或重复path |
| `RDMC-004` | role/path交换、自定义路径或越界路径 |
| `RDMC-005` | Ledger不是最后一项 |
| `RDMC-006` | 为absence/unknown创建empty、synthetic或placeholder set |
| `RDMC-007` | present root缺少对应set carrier |
| `RDMC-008` | set entry digest与root artifact digest不一致 |
| `RDMC-009` | raw byte SHA-256不一致 |
| `RDMC-010` | size_bytes不一致 |
| `RDMC-011` | Ledger entry digest与coverage_ledger_digest不一致 |
| `RDMC-012` | 未先通过0.3 Schema/conformance |
| `RDMC-013` | foreign-attempt、unsafe或interrupted world尝试发布 |

测试不得通过调用被测producer来生成expected拓扑；expected files、role/path与root projection必须从冻结合同/corpus独立枚举，
并至少包含漏项、重复、混入、placeholder与版本fallback mutation。

## 6. producer、consumer与authority ceiling

本合同只选择Schema/conformance/fixture identities，不选择实现入口。后继implementation feasibility必须重新核对：

- 现有0.1 producer/consumer与version dispatch能否在不改0.1 bytes的前提下扩展；
- 实际carrier raw bytes与semantic digest的单一读取/快照边界；
- CoverageLedger 0.3 conformance结果如何作为前置条件输入，而不是由manifest producer自我认证；
- negative world是否有qualified publication authority；
- expected topology是否独立于被测producer生成。

本文不授权：

```text
review-derivation-manifest-0.2 Schema or fixture creation
0.2 validator / conformance / producer / consumer / publisher
negative-world public Bundle
persistence Route A/B
public Review product
Evidence / CLI / Workbench / Core integration
post-R1 Benchmark or R2-R6
```

## 7. 停止线

命中任一条件必须停止当前施工，只重开最小合同边界：

- 需要修改0.1 bytes、扩大0.1 enum或让0.1接受0.2；
- 需要把absence/unknown编码成artifact、空集合、synthetic carrier或placeholder digest；
- manifest必须拥有或推断root truth，或能把unknown提升为present/complete；
- Schema alone被当作cross-artifact conformance；
- producer与Oracle共用同一未独立核对的presence projector；
- conformance必须重新读取可漂移路径，导致manifest绑定A而验证B；
- 需要把serialized Ledger恢复成same-attempt live authority；
- 需要同时选择persistence或public product才能实现本合同。

## 8. 后继资格顺序

本文tracked scope只允许`README.md`、`AGENTS.md`、`docs/milestones.md`与新增本文。Schema、fixtures、runtime、tests、
workflows、0.1 bytes、CoverageLedger 0.3、composition、persistence和public产品保持base bytes。

本文须先完成local exact scope、links、UTF-8/LF/final LF、fences/headings、`git diff --check`、global/local hygiene、
primary `audit.json` continuity、四格read-only contract audit与focused regression；再依次完成：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc315 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / feasibility-history reconciliation
    -> qualified contract candidate
    -> return CONTROL LOOP
```

即使全部闭合，本文也只升级为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。必须由独立docs-only freeze publication
完成自己的完整资格链后，`R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN`才可生效。
之后仍须返回CONTROL LOOP，独立判断implementation feasibility；不得从合同直接施工。

## 9. 状态上限

本候选当前只允许：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_FEASIBILITY_AUDITED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_CANDIDATE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文自己的资格链闭合后最多变为：

```text
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
```
