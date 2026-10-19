# R1 Relation Provider import-form conformance corrected successor 私有实现可行性审计

日期：2026-10-20

> 状态：`R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
>
> 坐标：`main@68e6fa0245161dd75b9d7750d3320158bebfa315`，tree
> `68e84bebf1d69a0ccbfca95eeb85c87e45fcf6a5`。
>
> 上游：[import-form conformance correction contract](299-r1-relation-provider-import-form-conformance-correction-contract.md)
> 与[独立冻结发布](300-r1-relation-provider-import-form-conformance-correction-contract-freeze-publication.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只审计冻结合同能否由一个有限、可区分的 private Provider
> successor 施工；不修改 runtime、tests、fixtures、Schema、Profile、Policy、manifest、persistence、Coverage 或 public
> Review 产品，也不授权实现。

## 1. CONTROL LOOP 与 qualified upstream

文档 300 由 PR #345 final head `9bca8018cea834507bd2c5ae0bed51ba312260f9` 合入本 exact main。PR original
Public CI `39305312371`、exact-main Public CI `39309834623` 与 Browser Smoke `39309834678` 均为 attempt 1
SUCCESS，分别为 11/11、11/11 与 1/1。fresh anonymous installed-product README、doc299、doc300、milestones
为 4/4 qualifying PASS；independent reconciliation 与 150-artifact closeout 分别为：

```text
4e4a50b33d5ab07acaa4c54f643023f359603b5460605a162d4e9039663d7866
44c856882e33510288570883e49ca0b351e145d07e616c416a8c7d75e3950e43
```

因此以下事实已经生效：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_STARTED
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_NOT_AUTHORIZED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORITY_ALLOWED_HISTORY_PRESERVED
R1_FACT_HANDOFF_RELATION_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_STOP_CONDITION_TRIGGERED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
```

fresh CONTROL LOOP 重新核对 remote main、open PR、doc290 / 294 / 299、Fact handoff、current Relation request / Provider /
canonicalizer / qualification / admission source 与相关 tests。open PR 只有依赖更新，没有并行 semantic PR 已经实现本 seam；没有新证据
要求重开 Fact truth、stage applicability、per-product closure、obligation projection、Relation candidate semantics 或 doc299。

## 2. 当前 private primitive 足以承载有限 successor

current `ValidatedRelationObservationRequest` 已 copy-own：

```text
descriptor
provider_run_id
assigned observation item ids
facts_by_id
observation_items_by_id
source_blobs_by_path_hex
```

现有 canonicalizer、Provider outcome builder、terminal validation、qualification 与 RelationSet admission 已把 candidate semantics、
assigned responsibility、run identity和下游 admission分开。审计 witness 在不修改这些 frozen primitives 的条件下，用新的 audit-only
algorithm identity消费完整 FactSet与明确 assignment，并把结果交给现有 canonicalizer / outcome validator。

因此需要增加的是：

```text
new private descriptor / algorithm identity
+ bounded import occurrence discovery
+ exact Fact binding
+ legacy-compatible child ordinal projection
```

而不是新的 public Provider SPI、Schema、manifest、persistence或第二套 qualification framework。

## 3. frozen input 与 occurrence universe 可机械构造

successor 对每个 accepted product/path 的 exact source bytes，以 CPython 3.10 grammar projection递归枚举
`ast.Import` / `ast.ImportFrom` 的每个 alias occurrence。每个 occurrence至少绑定：

```text
path
byte_start / byte_end
import_form
relative_level
module_parts
imported_name
alias_name
alias_ordinal
```

它与 authoritative `IMPORT_DECLARATION` Fact 做双向 exact matching：

```text
every applicable Fact has exactly one source occurrence
every source occurrence has exactly one authoritative Fact
```

完整 FactSet bytes、digest与所有 MODULE / CLASS / FUNCTION / METHOD / IMPORT_DECLARATION identity保持不变。occurrence
projection只为 Provider执行冻结 assignment提供 observation view，不成为新的 Fact truth，也不能生成或缩小 obligation denominator。

## 4. legacy compatibility 与 deterministic extension identity

legacy top-level single-alias `ast.Import` world继续使用原 `tree.body` ordinal，因此现有 candidate/outcome canonical bytes保持不变。
extra alias、`ImportFrom`与nested occurrence按 path内 lexical byte span、form、alias ordinal与canonical attributes排序，从
`len(tree.body)`开始分配 extension ordinal。

机械 witness同时证明：

- legacy plain import与`pass`后的plain import均保持 exact candidate bytes；
- extension ordinal不与 legacy top-level ordinal碰撞；
- multi-path world的 MODULE parent与import occurrence按 exact path闭合；
- 不同 path不能交换 MODULE、Fact或ordinal取得通过；
- host 3.13行为不取得 authority，四格均按3.10 projection生成相同 semantic report。

该规则是可行性 witness。最终 class、field、suffix与encoding仍由后继实现合同边界内选择，不能从本文反推 public shape。

## 5. complete assignment 与 terminal closure

application仍独立拥有 expected obligation universe和per-Provider assignment。successor只能遍历 request中已分配的
`observation_item_id`，不能自己选择 eligible subset。每个 assigned item必须恰好产生一个 terminal outcome；candidate仍由现有
canonicalizer复核 relation family、source/target Fact、path、ordinal与semantic attributes。

所以施工不需要让 Provider拥有以下权力：

```text
stage applicability
denominator construction
Provider requiredness
qualification
RelationSet admission
continuation issuance
```

missing / duplicate / foreign assignment或terminal history仍由 application-owned reconciliation拒绝。successor完成进程不等于
Provider已履责；只有 expected、assigned、terminal与admitted candidate的双向核账全部成立，same-attempt continuation才可能继续。

## 6. 规范 world 与 direct falsifier 可表达

fresh audit在完整 Fact truth上执行七组positive/control world：

| world | current legacy Provider | audit-only successor |
| --- | --- | --- |
| top-level single-alias plain import | COMPLETE | COMPLETE，candidate bytes相同 |
| `pass`后的legacy import | COMPLETE | COMPLETE，body ordinal与bytes相同 |
| `import a, b` | REJECTED | 两个alias obligation complete |
| `from pkg import a, b` | REJECTED | 两个alias obligation complete |
| relative与star import | REJECTED | complete |
| function/class/branch nested imports | REJECTED | complete |
| multi-path mixed forms | REJECTED | per-path complete |

每个world对两个现有Relation Provider responsibility分别执行；successor共完成14个Provider run。审计同时直接拒绝：

- authoritative import Fact missing；
- duplicate authoritative import Fact；
- semantic attributes drift；
- per-path MODULE closure非exact；
- candidate未覆盖全部assignment。

这些 witness直接覆盖 doc299 `RPIF-000..009`与`RPIF-014`的核心构造。`RPIF-010..012`使用现有
assignment/outcome/qualification primitives继续保留为后继实现必须直接攻击的negative worlds；`RPIF-013`由3.10 projection与四格
canonical report equality约束；`RPIF-015`继续由上游one-shot claim、original BudgetContext与same-attempt continuation约束。
可行性不把尚未施工的完整falsifier矩阵冒充已经实现。

## 7. upstream composition continuity仍成立

独立 continuity audit在本 exact main重新运行doc296的read-only construction，确认：

- exact immutable `DerivationInputSet`与claimed Fact handoff仍能按完整坐标join；
- foreign-policy world仍被拒绝；
-完整Policy的Fact / Relation stage ownership仍total、disjoint、exactly-once；
-完整five-kind single-path / two-path FactSet仍可建立per-product closure与complete obligation projection；
-current legacy domain/request仍不足以表达corrected successor；
-manifest、persistence与public Schema仍不是private successor blocker。

因此doc299补上的Provider conformance semantics可以作为doc296 A–J的有限新前置层；它不需要重开Fact handoff、stage ownership或
RelationSet admission，也不能直接恢复旧composition authorization。

## 8. bounded private implementation A–J

若本候选最终取得资格，后继独立授权最多可以覆盖以下施工面；本文不实施：

### A. exact upstream revalidation

绑定本 exact main、doc290 / 294 / 299 frozen bytes、claimed handoff、original BudgetContext、exact input与current private
Relation primitives；任何foreign world、consumed claim或digest-only holder停止。

### B. versioned private binding

新增可区分的private descriptor / binding / launch identity；legacy descriptor、allow-list与provider bytes保持不变。

### C. bounded occurrence projection

以显式CPython 3.10 projection递归枚举完整Import / ImportFrom alias occurrence；unsupported parser/runtime world fail closed。

### D. bidirectional Fact binding

按doc299完整键做AST occurrence与authoritative Fact双向exact match；missing、duplicate、drift与foreign path全部停止。

### E. deterministic child identity

保持legacy body ordinal与candidate bytes；只为non-legacy occurrence构造collision-free extension ordinal并直接攻击排序碰撞。

### F. complete assigned execution

只执行application分配的完整obligations；每项恰好一个terminal outcome，不由actual output反推denominator。

### G. existing canonicalization / qualification integration

复用现有candidate canonicalization、terminal validation、qualification与admission，增加version-aware allow-list；Provider不自证履责。

### H. same-attempt lifecycle

在doc296限定的同一composition attempt、同一original BudgetContext与同一claimed handoff内运行，不创建第二claim或重跑Fact。

### I. normative falsifiers

直接固化`RPIF-000..015`，包括assignment/terminal missing、duplicate、foreign attempt、host parser drift与identity collision。

### J. byte guards与continuation ceiling

保护legacy source/contract/vector bytes；只有完整required reconciliation后才能签发同attempt continuation，且不取得manifest、
persistence、Coverage、public Review、R2或R3 authority。

## 9. mechanical audit 与保留边界

audit root：

```text
C:\Users\lenovo\Desktop\GitHubProjects\tmp\relation-provider-import-form-successor-feasibility-68e6fa0
```

两组read-only audit均在Python 3.10.6 / 3.13.13、normal / `-O`四格产生相同canonical semantic digest：

```text
provider successor semantic report
915d0243222b18600911a63732c07ac06085e7be585f2f64a54e55ef30188c15

upstream corrected-successor continuity report
187680159640a6c1df6c2a3b20cee4635f7be05ccc34f9bf989a6867b36eb5c3
```

四格focused regression各为：

```text
Ran 77 tests
OK (skipped=1)
```

即每格76 passed、1个explicit reference runtime/Windows skip。测试与audit witness只证明在声明世界中没有观察到阻断，不拥有
合同扩张、实现授权、资格升级或未来continuation authority。

doc299 freeze readback bootstrap中的wheel wildcard与PowerShell reserved variable setup errors继续按原identity保留；它们没有产生
formal product observation。candidate history的reconciliation schema-key error与closeout self-capture mismatch同样不被本轮PASS覆盖。

## 10. feasibility stop conditions

后继若出现以下任一条件，必须保留反例并只重开被击穿边界：

- exact source occurrence与authoritative Fact不能双向、无歧义绑定；
- 3.10 projection不能在受支持runtime中稳定复算，或host parser必须成为authority；
- legacy bytes只能通过改写旧Provider identity、ordinal或candidate semantics保持；
- complete assignment只能通过过滤FactSet、缩小obligation universe或让Provider选择subset完成；
- 必须修改public Schema、manifest、persistence、Coverage或Policy/Profile才能运行private successor；
- version-aware binding / qualification不能与current allow-list、terminal history或admission安全共存；
- 必须创建第二个Fact claimant、新BudgetContext、跨attempt复用result或重跑Fact；
- direct falsifier只有弱化oracle、删除negative history或移动成功条件才能PASS。

## 11. 当前裁决

| 问题 | 裁决 |
| --- | --- |
| import-form correction contract是否frozen | **是** |
| current legacy Provider是否覆盖完整import-form universe | **否，且保持immutable** |
| current private request/canonicalizer能否承载有限versioned Provider successor | **是** |
| occurrence与authoritative Fact能否双向exact binding | **是，audit witness** |
| legacy narrow-world bytes能否保持 | **是，audit witness** |
|完整assignment/terminal/admission是否仍由application拥有 | **是** |
|需要过滤FactSet、重跑Fact或新增public Schema | **否，且禁止** |
| bounded A–J private implementation是否可行 | **是** |
|实现是否已授权或开始 | **否** |

本候选没有发现需要重开doc299或更早frozen truth的反例。它只把下一合法问题收紧为独立docs-only implementation authorization
publication；不证明runtime已经存在，也不恢复旧composition。

## 12. 本候选资格门与停止线

tracked scope只允许：

```text
README.md
AGENTS.md
docs/301-r1-relation-provider-import-form-conformance-corrected-successor-private-implementation-feasibility-audit.md
docs/milestones.md
```

doc290–300、runtime、tests、workflows、Schema、manifest、fixtures、Profile、Policy、Provider、vectors、corpus与post-R1计划必须保持
`68e6fa0…` base bytes。final bytes至少完成四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、marker、上游byte
continuity、`git diff --check`、read-only hygiene、两组机械audit与声明的focused regression；测试只作witness。

```text
final docs-only audit bytes / declared local gates
    -> original PR required gates
    -> continuously authorized exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> FEASIBILITY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前只能写：

```text
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTION_CONTRACT_FROZEN
R1_RELATION_PROVIDER_IMPORT_FORM_CONFORMANCE_CORRECTED_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE
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

若本候选最终取得资格，它最多成为qualified feasibility history。随后必须从新 exact main返回CONTROL LOOP，单独判断docs-only
implementation authorization publication是否仍是下一最小合法seam；不得自动修改runtime、恢复旧composition、选择manifest /
persistence或启动Coverage、public Review、R2–R6或post-R1 Benchmark。
