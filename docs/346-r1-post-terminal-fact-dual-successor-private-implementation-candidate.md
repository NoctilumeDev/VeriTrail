# R1 post-terminal Fact dual-successor 私有实现候选

日期：2026-11-05

> 状态：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_CANDIDATE`。
>
> exact base：`main@aa0cd335a98269dcdb843645f9643c0e7982a5c8`，tree
> `eb4a9529867169f0ef695609c6cd8265d161df4e`。
>
> 权威来源：[冻结合同](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)、
> [合同冻结发布](341-r1-post-terminal-fact-dual-successor-authority-recovery-contract-freeze-publication.md)、
> [可行性审计](342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md)与
> [versioned implementation authorization successor 0.2](345-r1-post-terminal-fact-dual-successor-private-implementation-authorization-successor-publication.md)。
>
> 影响：`L2_PRIVATE_RUNTIME / BOUNDED_IMPLEMENTATION_CANDIDATE_ONLY`。本文不冻结实现、不恢复global
> composition authority，也不创建manifest、Evidence、persistence、public Review或R2–R6能力。

## 1. 实现入口来自已经闭合的独立授权链

doc345由PR #397以
`base=a1899bc857d7933833b4b2393ae1bd7a71af2e14 / head=ab1e5f37b18e96e676da5aa05641f0a987ec15f2 /
tree=eb4a9529867169f0ef695609c6cd8265d161df4e`受保护合入当前exact main
`aa0cd335a98269dcdb843645f9643c0e7982a5c8`。original Public CI `41849292451`、exact-main Public CI
`41854217488`与Browser Smoke `41854217661`均为attempt 1 SUCCESS，分别为11/11、11/11与1/1。

fresh anonymous installed-product README、doc342、doc344、doc345与milestones各取得唯一qualifying PASS；independent
reconciliation、189-artifact finite closeout、保留的stdout self-capture mismatch与finite integrity分别为：

```text
cb652ab7de58b7480252af142ffddd38ca5bfb4949dbaffe335e6e1f7b6c1572
855d9ab3f5d6af5680712ae2155cc56004db5d27334d9e5e16a238705e3000b3
356acb5a49c9c0848367d8c2322d234fb65133abd19bc672aaac789b396eabf3
dc813b3051db9099aba33c7827044ca8edfeac3265acb4e28d0625e69c941615
```

首次README marker-window formal ERROR、修正边界
`ee2ae06…`及retained history `cf2af86…`继续按原identity保留，后继PASS不回填。因此
`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效；它只授权
doc345 A–J，不等于实现已经合入或冻结。

## 2. bounded private implementation

候选新增private module `_post_terminal_fact_dual_successor.py`，并只在三个既有private seam中增加可选、默认不启用的
适配入口：

1. `POST_TERMINAL_DUAL_SUCCESSOR_0_1` factory在Fact pre-terminal阶段绑定original consumer、inputs、Policy/Profile、
   provider assignment、qualification、live `BudgetContext`与一个shared slot；初态只能是`SEALED_NOT_ROUTABLE`；
2. original Fact owner完成closure以后，selector从同一consumer重新取得terminal source，独立验证exact五分支，并机械映射
   `NORMAL_FULFILLED -> RELATION_HANDOFF`、四类negative -> `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`；
3. shared slot只允许一次`TERMINAL_READY -> CLAIMED_RELATION | CLAIMED_EXACT_INPUT`；pre-terminal、wrong route、copy、
   replay、version mismatch、same-attempt漂移、late stop或并发loss都会永久`REVOKED`，没有fallback；
4. normal route产生non-serializable private Relation claimed-source carrier，随后委托既有Relation transition同一执行体；existing
   entry仍沿原路径进入该执行体；
5. negative route把同一terminal source、original inputs/blob maps、五digest与live context交给现有exact-input 0.2 carrier；
   既有negative producer、validator与admission继续负责自己的冻结语义；
6. Relation admission与exact-input每次读取都回到route carrier重验source bytes、object identity、context、input seal、claim与
   consume state；新route上的copy/replay同时撤销shared authority；
7. 八类private failure family逐字保持合同 vocabulary，不写入既有Fact/Relation/Coverage reason enum；
8. 默认参数保持`LEGACY`、`RELATION_TRANSITION`与exact-input 0.2旧调用路径不变；新module没有加入public package exports。

候选没有获得RelationSet、ReviewSliceSet、CoverageLedger、global composition、manifest、Evidence、persistence、public Review或
R2–R6 authority。

## 3. prequalification review findings与保留身份

formal qualification以前的两项真实实现边界缺陷已经在同一未提交工作树内修正，但原失败日志永久保留：

| 身份 | 首次观察 | 最小修正 |
| --- | --- | --- |
| `PREQUAL-IMPLEMENTATION-001` | `implementation-test-attempt1-failure.txt`中required-provider terminal source未能完成新route验证；12项得到2 failures/4 errors | terminal branch验证改为接受冻结required-provider failure生命周期，同时保持Fact truth与parent revocation约束 |
| `PREQUAL-IMPLEMENTATION-002` | `implementation-test-attempt2-failure.txt`中terminal replay泄漏既有`ProductFactConsumerError`，没有投影为新private typed family；12项得到1 error | selector在terminal boundary统一投影为`DUAL_SUCCESSOR_TERMINAL_SOURCE_REJECTED`并撤销shared slot |

`implementation-test-attempt3.log`随后12/12 PASS。其后的expanded attempt 1/2为20/20 PASS，expanded attempt 3在加入
existing negative producer end-to-end witness后为21/21 PASS。

wrong document filename、Windows rg glob、初始wrong-worktree apply/inverse patch、wrong Python path、PowerShell heredoc、focused
matrix summary filename、authorization successor filename、unquoted tree revision与首次doc346 patch格式错误均保存在
`setup-errors.txt`，effect全部为`NONE`。这些错误、两项prequalification defect及修正前日志都不被后继PASS删除或改写。

第一次九文件local validation在`git diff --check`观察到milestones新增了一个terminal blank line并以exit 2停止；该
`LOCAL-VALIDATION-001 / CANDIDATE_DOCUMENT_HYGIENE_DEFECT`及validator traceback永久保留。最小修正只移除该空行，未修改
runtime、test oracle或冻结合同；后继PASS不能回填attempt 1。

首次pre-PR暂存又证明普通`git diff --check`不检查untracked doc346；staged门因此发现本文自己的terminal blank line。
先前local-validation PASS与146-artifact seal被保留为`NON_QUALIFYING / PROOF_FACILITY_SURFACE_INCOMPLETE`。最小修正只移除该
空行；后继validator必须同时检查staged与unstaged diff surface。

## 4. final witness matrix

最终工作字节上的focused矩阵在Python 3.10.6/3.13.13 × normal/`-O`四格各运行174项，均为173 passed / 1 skipped。
其中显式覆盖`PTDS-000`至`PTDS-017`、new Relation claimed-source到existing executor、new negative claim到existing
producer/validator/admission，以及old Relation identity/public exports不变。

full Review Attention矩阵四格各运行621项并全部PASS：

| Python | 模式 | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 618 passed / 3 skipped |
| 3.10.6 | `-O` | 618 passed / 3 skipped |
| 3.13.13 | normal | 619 passed / 2 skipped |
| 3.13.13 | `-O` | 619 passed / 2 skipped |

semantic audit四格逐字节一致，canonical report SHA-256为：

```text
638b370d5cca5f3d8e854513386664de6e5ce33c5cea3796e29c8e2a48b69b16
```

该report机械固定exact base/tree、private domain/function identities、五分支total route、五个state、八类failure family、
existing Relation/exact-input identity、18项falsifier与authority ceiling；测试只是witness，不授予额外authority。

## 5. candidate scope与剩余资格链

tracked scope只能是：

```text
README.md
AGENTS.md
docs/346-r1-post-terminal-fact-dual-successor-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_fact_fulfillment.py
plugins/review-attention/src/veritrail_review/_fact_relation_transition.py
plugins/review-attention/src/veritrail_review/_fact_to_coverage_exact_input_handoff.py
plugins/review-attention/src/veritrail_review/_post_terminal_fact_dual_successor.py
plugins/review-attention/tests/test_post_terminal_fact_dual_successor.py
```

提交前还必须以最终九文件字节完成compile、diff、global/local hygiene、Markdown、exact scope、public export与primary audit
continuity复算并形成有限local evidence seal。之后资格链仍是：

```text
single candidate commit / exact base-head-tree
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc345 / 本文 / milestones readback
    -> independent reconciliation + finite closeout
    -> implementation candidate becomes EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
```

任何non-success都保留原identity；不得rerun洗白，不得用相同semantic digest、另一个world或后继PASS替代本candidate的一门。

## 6. 当前状态与停止线

在本文自己的完整资格链闭合以前只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_MERGED_NOT_EXACT_MAIN_VERIFIED_NOT_READBACK_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整链闭合后最多把本candidate升级为`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。实现冻结必须由
新的docs-only publication从新exact main独立发布并完成自己的资格链；不得从本文直接恢复global composition、选择manifest/Evidence/
persistence、启动public Review或R2–R6。
