# R1 post-terminal Fact dual-successor 私有实现可行性审计

日期：2026-10-29

> 候选状态：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDIT_CANDIDATE`。
> 本文自己的资格链闭合以前，本文不是qualified history，也不授权runtime施工。
>
> 审计基线：`main@99244df24360787b5f1b97a1cad89dc26d8aefe0`；tree
> `f398de23047a8ca6ecd5822e204d50abfc40b8c7`。
>
> 上游：[0.1合同](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)、
> [合同独立冻结发布](341-r1-post-terminal-fact-dual-successor-authority-recovery-contract-freeze-publication.md)。
>
> 影响层级：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_IMPLEMENTATION_FEASIBILITY_AUDIT`。

## 1. CONTROL LOOP与qualified起点

文档341由PR #393以
`base=c819dd1cca35a96efc22908cce546fad8185d9d8 / head=c49f8f1327ad6f528a10eadcb6f25eec9cf8009a /
tree=f398de23047a8ca6ecd5822e204d50abfc40b8c7`受保护合入本审计基线。original Public CI
`40830900921`、exact-main Public CI `40834389932`与Browser Smoke `40834389934`均为attempt 1 SUCCESS，
分别11/11、11/11与1/1。

fresh anonymous installed-product readback对README、doc340、doc341与milestones各取得唯一
`FORMAL_READBACK_PASS`。首次fresh root误选Python 3.10、public-bytes `FileNotFoundError`、anonymous rate exhaustion、
README formal generation 1 marker drift、generation 2 zero-rendered marker、pre-formal active-pointer collision与reconciliation
attempt 1 staged proof-history extension错误均按原identity保留，后继PASS不回填。independent reconciliation、226-artifact finite
closeout、保留的stdout self-capture mismatch与finite integrity的SHA-256为：

```text
4463042f2452fc5b3f8c9920eb1a0b472bb3bbd9fe699d6fcc8db44fd08e78fe
e501f171f09cb569dc21cd1d4b1854e56993988b032a98d94546f2ff3cf906b7
907b5638bf444528a627cd78a7863ae3b6bcfb7a9b17b87776e48663196aa1a8
8db5b5693695ba85ce5f4f100116d4b4b57e2804d43b441ebf02cafaa7f59be1
```

因此本轮qualified起点是：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

fresh CONTROL LOOP只问：冻结的`POST_TERMINAL_DUAL_SUCCESSOR_0_1`能否在不改变既有Fact、Relation、Coverage与public
边界的前提下，由一个bounded private patch实现并独立反证。合同冻结不自动产生implementation authority。

## 2. 当前源码已经拥有的四个primitive

read-only审计确认当前source已经分离四项必要primitive：

1. `_handoff_source_document()`从original Fact consumer、complete closure、same-object inputs/context、Policy/Profile、
   Provider history与child lifecycle重验terminal source，并只从这些事实机械得到五个terminal branch；
2. `OwnedProductFactClosure`只有一个`__claimed`、一个`__claim_purpose`与一个lock；legacy continuation、Coverage 0.1、
   Relation handoff及exact-input successor 0.2已经证明共享同一不可复制consume slot；
3. `/0.2` Fact-stage applicability对完整Policy建立`union_complete / intersection_empty / owner_count_per_requirement=1`，
   caller不能缩小Fact Provider responsibility；
4. positive Relation transition与negative exact-input successor已经各自从private closure claim取得完整source，并由自己的
   downstream owner继续验证；negative producer、independent validator与same-attempt admission也保持分离。

这些primitive属于当前frozen实现，不等于新domain已经存在。exact base的runtime与public package export都不包含
`POST_TERMINAL_DUAL_SUCCESSOR_0_1`。

## 3. bounded private construction

冻结合同可以由以下有限实现面承载：

```text
new private post-terminal selector / claimed-route carrier
    +
one exact Fact consumer factory for POST_TERMINAL_DUAL_SUCCESSOR_0_1
    +
shared-slot branch-checked claim hooks in _fact_fulfillment.py
    +
one private claimed-Relation-source adapter preserving the legacy transition entrypoint
    +
one focused private test module and status documentation
```

successor在Fact执行前与new-domain consumer一起创建，只绑定original inputs/context、完整Policy/Profile、Fact assignment与一个shared
slot；没有complete closure时任何route claim都永久revoke。Fact reconciliation完成后，selector重用original terminal-source
revalidation，normal branch只签发Relation claimed-source carrier，四类negative branch只签发现有0.2 exact-input carrier。

Relation claimed-source adapter只把当前`run_fact_handoff_relation_transition()`开头已经分离的claim acquisition与后续transition
execution显式分开；旧closure entrypoint仍可先claim再委托同一执行体。它不修改Relation Provider、obligation projector、assignment、
qualification或admission。negative route继续委托现有exact-input carrier，后继producer/validator/admission无需修改。

具体class、method、field与locking布局仍是implementation non-decision；可行性只证明上述有限解空间存在。

## 4. branch independence与shared-slot可构造性

selector不需要读取Relation/Coverage candidate来决定route。它可以复用Fact owner已经独立形成的terminal source，同时再次验证：

```text
five known branches exactly
same closure / consumer / inputs / context object graph
complete Policy and Fact truth
branch-specific Provider history and child lifecycle
live BudgetContext and unchanged input seal
```

claim开始时先占用当前closure唯一slot，再验证new exact domain与branch-route mapping。这样wrong-route、pre-terminal、validation failure、
copy-equal、replay与concurrent loss都进入同一永久revoke路径，不能在失败后fallback。normal和negative下游仍各自验证source，不共享
selector的“期望输出反推branch”错误路径。

## 5. 不需要修改的frozen surface

bounded construction不要求修改：

- Fact terminal branch、FactSet、Provider history或Fact failure family；
- corrected Fact→Relation Provider、assignment、qualification与admission；
- Fact→Coverage exact-input successor 0.2 identity、carrier truth与negative-world producer；
- CoverageLedger Schema、reason order、positive/negative composition result；
- legacy `LEGACY`或`RELATION_TRANSITION`consumer的domain identity与history bytes；
- package public exports、manifest、Evidence、persistence、CLI、Workbench或public Review。

旧entrypoint可以通过内部委托保持行为兼容；新selector与claimed carrier保持private、attempt-bound、non-serializable且不可copy。

## 6. read-only机械结果

审计identity为：

```text
r1-post-terminal-fact-dual-successor-private-implementation-feasibility/0.1
```

Python 3.10.6 / 3.13.13 × normal / `-O`四格均PASS，canonical report逐字节一致：

```text
7bbc3762c1f28dfa6b6889e45da00c45353d411b079ab4a663545ed4b7113a6a
631d58e078ff4f8fcf2d8ba94085429da616d4d812a4d46e434733e545aae68c
```

focused witness覆盖Language Support、Fact fulfillment、positive/negative handoff、Fact→Relation、ReviewSlice composition与negative-world
recovery；四格各为`214 tests / 213 passed / 1 skipped`，matrix SHA-256为
`048a0a143bacca5bdb5f00139f3e500025b9e950a1ec14a14556602705b00a77`。首次embedded dataclass audit因proof module未注册到`sys.modules`而ERROR，
其stdout/stderr/result保持原identity，effect为`NONE`；修正后的attempt 2才构成本审计local semantic witness。测试只证明current
base与本审计判断稳定，不创建runtime或implementation authority。

## 7. 状态上限与下一合法seam

本审计自己的完整资格链闭合以后，最多支持：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
```

下一seam只能是独立docs-only `PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION`。该publication必须重新绑定本审计的exact
资格历史并条件化授权bounded private patch；本文自身不能被runtime消费。

## 8. stop conditions

以下任一事实出现时停止当前施工，只重开被击穿的最小边界：

- complete terminal branch必须由requester或downstream candidate选择；
- normal/negative route需要两个独立claim slot或失败后fallback；
- new domain只能alias `LEGACY`或`RELATION_TRANSITION`才能工作；
- Relation claimed-source adapter无法保留完整Policy/Fact truth或必须弱化existing transition；
- exact-input route必须改变0.2 identity、carrier truth或negative producer oracle；
- producer与selector只能共享同一个关键branch/denominator projector；
- bounded patch必须扩大public Schema、manifest、Evidence、persistence或global composition authority。

这些反例属于implementation/admission无资格，不能用`UNKNOWN`产品或绿色测试掩盖。

## 9. 本candidate资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md
docs/milestones.md
```

final bytes至少复核exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences、unique headings、
状态markers、upstream frozen hashes、`git diff --check`、read-only global/local hygiene与primary `audit.json` continuity。随后依次：

```text
original PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc341 / 本文 / milestones readback
    -> independent source-byte / Core / Bundle / frozen-history reconciliation
    -> FEASIBILITY_AUDITED qualified history
    -> return CONTROL LOOP
```

任何FAIL、ERROR、CANCELLED、setup failure、rate-limit或UNKNOWN保持原identity；不得rerun until PASS或把后继PASS回填旧world。
本文完整资格链闭合以前，开头的candidate marker不升级。闭合以后仍不得直接施工runtime、消费旧global composition authority、实现
manifest/Evidence、选择persistence、发布public Review或启动post-R1 Benchmark/R2–R6。
