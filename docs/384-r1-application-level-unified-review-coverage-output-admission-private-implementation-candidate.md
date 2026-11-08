# R1 application-level unified Review / Coverage output admission 私有实现候选

日期：2026-11-08

> 状态：`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_CANDIDATE`。
>
> exact base：`main@5742c979e671e65067085e0303caf9d3506b7d42`，tree
> `e0a6db65861e19166968b6491f9153ba041eb933`。
>
> 权威来源：[冻结合同](380-r1-application-level-unified-review-coverage-output-admission-contract.md)、
> [合同冻结发布](381-r1-application-level-unified-review-coverage-output-admission-contract-freeze-publication.md)、
> [private implementation feasibility audit](382-r1-application-level-unified-review-coverage-output-admission-private-implementation-feasibility-audit.md)与
> [private implementation authorization publication](383-r1-application-level-unified-review-coverage-output-admission-private-implementation-authorization-publication.md)。
>
> 影响：`L2_PRIVATE_RUNTIME / BOUNDED_IMPLEMENTATION_CANDIDATE_ONLY`。本文不冻结实现、不创建public
> Schema/export、manifest、Evidence、persistence、public Review、Core Verdict或R2–R6能力。

## 1. 实现入口来自已经闭合的独立授权链

doc383由PR #435精确合入当前exact main。original Public CI `42428584420`、exact-main Public CI
`42431241189`与Browser Smoke `42431241097`均为attempt 1 SUCCESS，分别11/11、11/11与1/1；没有rerun。
fresh installed-product README/doc382/doc383 Render formal与AGENTS/milestones raw/API/exact-Git观察、independent
reconciliation、finite closeout及finite integrity全部闭合。关键identity为：

```text
5f89cf9ba6698cfb99954658e75e1d75a804964198819bb57b0298ca95d60b58
c0276e9bf3b4479a8ff722dfbc7f1645614cd8ad67b939d875ccf8d89f67c17a
4e544e5014694daf2349781f1f7a2f2211eabfde09f046805c4b65271af8f446
```

README与raw AGENTS的anonymous rate non-success、worktree attachment cap、recursive-delete policy、PowerShell/Windows
`rg`、reconciliation marker-cardinality与successor proof-facility setup failures继续按原identity保留。后继PASS不回填它们。
因此`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效；它只授权
doc383 A–J，不等于实现已经资格化、合入或冻结。

## 2. 原工程问题、当前证明义务与适用世界

原工程问题保持为：

```text
为Review/Coverage normal与negative结果建立同一个application-level
可判别、one-shot、authority-preserving output admission边界。
```

本文当前证明义务只是在exact base上形成doc380/doc383允许的bounded private runtime candidate，并让它经过自己的完整资格链。
适用世界仍只包含Python 3.10结构语义、冻结的post-terminal selector、两类private downstream result与当前声明矩阵；不包含public
Review、manifest、same-attempt DerivationEvidence continuity、持久化、多语言或真实人类审查收益。

候选显式固定：

```text
proof_is_not_problem_solving      = true
qualification_inheritance_allowed = false
original engineering problem solved = false
```

形式矩阵全绿只能证明该exact applicability world中的候选没有被声明反例击穿，不能把证明对象漂移成“测试通过即问题解决”。

## 3. bounded private implementation

候选新增private module `_unified_review_coverage_output_admission.py`，并只在四个既有private seam增加窄live-coordinate hook：

1. application owner只能在downstream消费以前绑定一个exact selector route claim；第二个owner、late bind、copy、replay或失败
   fallback都会撤销同一route authority；
2. application module独立拥有五分支映射，保持`NORMAL_FULFILLED -> RELATION_HANDOFF`及四类negative
   `-> FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`，不调用selector的被测branch projector；
3. normal path只接受exact nominal `OwnedReviewSliceCoverageComposition`，逐项重验claim id、Fact consumer attempt、五个input
   digest、original inputs、live context、bridge request、committed phase、CoverageLedger conformance source与composition identity；
4. negative path只接受exact nominal `AdmittedNegativeWorldCoverage`，逐项重验carrier、claim id、original closure/attempt、validation、
   candidate bytes、live context、CoverageLedger conformance source与admitted candidate identity；
5. application owner对两条路径都独立调用冻结的`validate_review_coverage_ledger`，不信任downstream曾经成功，也不从result shape
   反推route；
6. one-shot submit通过同一live `BudgetContext`提交private canonical admission proof；state只允许
   `ROUTE_BOUND_NOT_ADMITTED -> ADMITTED_NORMAL | ADMITTED_NEGATIVE`，任何失败进入`REVOKED`；
7. admitted object只暴露exact route判别、result kind与对应variant accessor；每次读取继续重验exact object graph、context、phase、
   ledger/root chain与authority ceiling；wrong accessor、copy、pickle、JSON或mutation均fail closed；
8. 九类private failure family逐字保持doc380 vocabulary，不写入既有Fact/Relation/Slice/Coverage reason或Core Verdict；
9. 旧direct exact-input carrier继续服务旧consumer，但因为缺少selector-origin callback不能冒充新application route；
10. `veritrail_review.__init__`、public Schema、既有producer语义、CoverageLedger reason/order、manifest/Evidence/persistence/public
    Review与R2–R6均保持base行为。

## 4. prequalification findings与保留身份

formal qualification以前发现的边界与证明目标问题都保留原identity；它们没有被后继PASS删除：

| 身份 | 首次观察 | 最小处置 |
| --- | --- | --- |
| `PREQUAL-UAO019-PROOF-TARGET` | 测试错误假设独立negative attempt的`coverage_ledger_digest`应相等；实际root chain正确绑定attempt identity | 改为比较等价semantic projection，同时要求digest不同并拒绝foreign attempt；不修改产品oracle |
| `PREQUAL-FOCUSED-MIXED-WORKTREE` | source correction发生在首次focused四格运行期间，matrix被主动CANCELLED | 保留取消identity；只在稳定字节上重建新matrix |
| `PREQUAL-NORMAL-ELIGIBILITY-LAYER-IDENTITY` | 测试把Fact parent eligibility与downstream Relation transition eligibility误认成同一对象 | 分层重验各自live authority，再以claim/attempt/input identity机械桥接 |
| `PREQUAL-DIRECT-CARRIER-FIXTURE` | direct-carrier负例使用了没有exact-input authority的Relation-only closure | 改用既有exact-input fixture；产品代码与oracle不变 |
| `PREQUAL-ADDITIONAL-PROOF-TARGETS` | review要求显式证明成功后read仍发现result mutation，以及copy未提交owner会撤销route | 在同一private test module增加两个反例；无产品失败、无scope扩张 |

Codex attachment cap、PowerShell tree表达式、Windows `rg` wildcard、错误Python/pytest入口、black不可用与wrong unittest target均作为
setup error保存在evidence root，effect为`NONE`。修正前focused日志、UAO019 failure、eligibility failure与direct-carrier fixture error
均不得作为final qualification。

稳定修正前字节上的prequalification witness为：focused四格各284项、1 skipped、PASS；full Review Attention四格各646项，
Python 3.10为643 passed/3 skipped，Python 3.13为644 passed/2 skipped；global/local hygiene 8/8 PASS。对应matrix SHA-256为：

```text
7821fd885b30202ded1a9479759e672c59d00d5b0037609d1242195986f5a981
4959beee0e3329d245fa8e6f5be8472916913269e3ad71efa9478a88db475722
d63cd3c7da57f81b9798ec13b69a772086e2d8a244401b32459d173c8c2bfa87
```

semantic prequalification四格逐字节一致，canonical report SHA-256为
`e2c476a7c254a4710953656dad247b0b1c0c9e11f8582a866183389c31da4a0b`，matrix SHA-256为
`b1c4907101506bdc4207c3b5f370d8d4805252ab0c7090ee1d9e2cd2bd00a87a`。这些都只作prequalification witness；新增
proof target以后必须从final bytes重新运行。

## 5. final witness matrix

新增proof target后的最终源码与test字节已经从头完成四组产品witness：

| witness | Python 3.10.6 normal / `-O` | Python 3.13.13 normal / `-O` | evidence SHA-256 |
| --- | --- | --- | --- |
| private UAO suite | 各27/27 PASS | 各27/27 PASS | `85c72f1991df29a5b0971056ffa57f1afc9302ea34b73e8ce18c5b047997e39c` |
| focused Review Attention | 各286 reported / 285 passed / 1 skipped | 各286 reported / 285 passed / 1 skipped | `70d7e831e1036a9439e31057ab4afe85e1731182c99ba9ecc1f7a133a6bdf3b5` |
| full Review Attention | 各648 reported / 645 passed / 3 skipped | 各648 reported / 646 passed / 2 skipped | `57d8a5ed101f4409cd878adb104dc49a3d9d38e4d1f389434736a3aa325d8f88` |
| semantic comparison | 四格逐字节一致 | 四格逐字节一致 | canonical `a543fa16316ed9570c467451f66c322f063c6665e06b0ddfd58ebf144af599e1`; matrix `223bc74a2ed76936a9745a1229f012d02578280bb7b78fec6335c262fe7d2a24` |

final十文件还完成Python 3.10.6/3.13.13 × normal/`-O`四格compile、global/local hygiene 8/8、四份Markdown与850个
local link、staged/unstaged diff、exact scope、UTF-8/LF、public export与primary audit continuity。local aggregation attempt 1/2先后因把
UAO与focused matrix的实际`result/rows` schema误读成`all_pass/cells`而产生`KeyError`；两个proof-facility error均保留为
`NON_QUALIFYING / NONE`，后继只纠正validator的schema读取，没有重跑或修改产品witness。最终corrected validation在同一final十文件
字节上PASS。这些PASS只证明private implementation在已声明world中的机械性质，不宣称原工程问题已经解决，也不授予merge、exact-main、
readback或freeze资格。

## 6. candidate scope与剩余资格链

tracked scope只能是：

```text
README.md
AGENTS.md
docs/384-r1-application-level-unified-review-coverage-output-admission-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_fact_to_coverage_exact_input_handoff.py
plugins/review-attention/src/veritrail_review/_negative_world_coverage_authority_recovery.py
plugins/review-attention/src/veritrail_review/_post_terminal_fact_dual_successor.py
plugins/review-attention/src/veritrail_review/_relation_transition_slice_composition.py
plugins/review-attention/src/veritrail_review/_unified_review_coverage_output_admission.py
plugins/review-attention/tests/test_unified_review_coverage_output_admission.py
```

提交前还必须以最终十文件字节完成本层全部local gates并形成有限local evidence seal。之后资格链仍是：

```text
single candidate commit / exact base-head-tree
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc383 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> implementation candidate becomes EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
```

任何non-success都保留原identity；不得rerun洗白，不得用相同semantic digest、另一个world或后继PASS替代本candidate的一门。

## 7. 当前状态与停止线

在本文自己的完整资格链闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_CANDIDATE
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_NOT_MERGED_NOT_EXACT_MAIN_VERIFIED_NOT_READBACK_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整链闭合后最多把本candidate升级为`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。实现冻结必须由
新的docs-only publication从新exact main独立发布并完成自己的资格链；不得从本文直接选择manifest/Evidence/persistence、启动
public Review或R2–R6。原工程问题仍须由该完整链与后继CONTROL LOOP检验，不能由形式PASS自行宣告解决。
