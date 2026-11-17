# R1 DerivationEvidence manifest carrier successor 私有实现候选

日期：2026-11-17

> 当前状态：`R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NOT_FROZEN`。
>
> 施工基线：`main@cc8097eb2c71981802ad987f75ce07e1c3bc2d30`，tree
> `992bc9c85f90a7aeaddffa39925d14f049f52772`。
>
> 授权来源：[合同恢复](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)、
> [合同冻结发布](429-r1-manifest-carrier-successor-contract-recovery-freeze-publication.md)、
> [private implementation feasibility audit](430-r1-manifest-carrier-successor-private-implementation-feasibility-audit.md)、
> [original-gate cancellation boundary](432-r1-manifest-carrier-authorization-original-gate-cancellation-boundary.md)与
> [authorization successor](433-r1-manifest-carrier-successor-private-implementation-authorization-successor.md)。
>
> 影响：`L3_PRIVATE_RUNTIME_AND_TESTS / ONE_PUBLIC_SCHEMA_RESOURCE / NO_MANIFEST_RUNTIME`。本文只形成 bounded A–J
> implementation candidate；不声明 merged、exact-main verified、readback qualified 或 frozen，不恢复 global composition authority，
> 不创建 Manifest runtime、persistence、public Review、Core Verdict、标签、Release 或 R2–R6 能力。

## 1. CONTROL LOOP 与已生效授权

PR #495 把 doc433 candidate 精确合入：

```text
base   f21f310c1e99d5e7fa8b4f944d545f3163c9d627
head   f95b1276b3f3ebae4910c3fabc4eb84f83d851b1
tree   992bc9c85f90a7aeaddffa39925d14f049f52772
merge  cc8097eb2c71981802ad987f75ce07e1c3bc2d30
```

三个远端门均为原始 attempt，没有 rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #495 original Public CI | `43995899179` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `44000762240` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `44000762356` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc430、doc432、doc433 Render 与 AGENTS、milestones、Public CI workflow raw-byte
observations 各有唯一 qualifying PASS。fresh worktree missing-object 与 Codex attachment-cap setup errors、anonymous diagnostic/preflight
记录、reconciliation attempt 1 的 doc433 alignment whitespace proof-target error，以及 expected stdout self-capture mismatch 均按原 identity
保留；没有用后继 PASS 覆盖或重复产品观察。最终 independent reconciliation、160-artifact closeout、self-capture mismatch 与
166-artifact finite integrity SHA-256 依次为：

```text
c33ccdf6d5015c5c1795a538329dec0fa8bb669989306e79370e3adb41c3a712
349ebd00e89d9fecfa436bf22d8a0767b305d2b036f4cb12012d616def0420c1
d5445572cdb982ee56b7d2833f49309b98828903c486dd9eef5f9c7779daeebe
3ad1757ed9124974ba4586be09afe917199d5fde658e6c13e01a41d3b1888b99
```

因此以下 authority 已经生效：

```text
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
```

fresh CONTROL LOOP 重新核对 exact main、doc426/doc429 冻结合同、doc430/doc432 qualified history、doc433 authority ceiling、旧 Evidence
0.2 / Manifest 0.1、PR #493 retained CANCELLED/FAILURE world 与 primary `audit.json`。没有反例要求重开冻结合同，也没有理由扩大
doc433。最小合法施工面仍是 bounded A–J；`proof_is_not_problem_solving = true`、`local_not_global = true`。

## 2. Evidence 0.3 与 exact-version isolation

本候选新增公开 Schema resource `review-derivation-evidence-0.3.schema.json`，固定：

- closed `DERIVATION_EVIDENCE / 0.3` object 与 `veritrail-json-c14n/1`；
- exact source/request provenance、五个 input digest、terminal branch、selector route、continuity variant、application admission、
  CoverageLedger/root-chain 与 evidence identity；
- `NORMAL_FULFILLED`只能对应`RELATION_HANDOFF / NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY`；四类 negative branch 只能对应
  `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2 / NEGATIVE_WORLD_COVERAGE_CONTINUITY`；
- request provenance 只能是 exact owned snapshot OID projection；unknown、closest、Evidence 0.2 或 Manifest 0.1 不得 fallback 为 0.3。

`tests/test_review_r1_schema_payload.py`只把新 Schema 加入显式授权资源集合。旧 Evidence 0.2、Manifest 0.1 Schema bytes、role/path、
consumer 与 default composition 均保持 base 不变。

## 3. same-attempt private coordinate

既有 continuity owner 只增加一个 sibling-private coordinate：

```text
continuity bytes
source snapshot / ReviewPolicy / DerivationProfile bytes
exact request provenance bytes
terminal source / optional transition / exact result bytes
application admission bytes
attempt binding bytes
CoverageLedger conformance source
result kind
```

coordinate 每次读取前重新执行既有 committed-value validation，并逐项核 exact result/application admission、inputs、live context、
conformance source 与 normal/negative exact object identity。negative worlds 在原 Fact attempt 边界 copy-own request provenance，不借用不存在的
Relation request。attempt binding 是 closed shape，绑定原 fact attempt、selector claim、derivation、canonical context identity、positive finite
budget、`RUNNING / ADMITTED / COMMITTED` lifecycle；它不是新的 observation、truth 或 global authority。

## 4. private projection、carrier 与 one-shot lifecycle

新 private producer：

1. 从 exact continuity coordinate 形成 canonical Evidence 0.3；
2. 机械投影固定 role/path 顺序、raw SHA-256、size、semantic digest 与 CoverageLedger root topology；
3. copy-own source/policy/profile/evidence、present Fact/Relation/Slice 以及 CoverageLedger bytes；
4. normal branch保留 present Fact/Relation，Slice conflict保留`QUALIFIED_UNKNOWN`；四类negative保留三个`QUALIFIED_ABSENT`，不制造
   placeholder file；
5. 把 claim、candidate、admitted carrier 与 future-consumption snapshot 各自绑定 owned snapshot seal。

候选生命周期为：

```text
PENDING -> VALIDATING -> VALIDATED -> ADMITTED
any invalid edge -> REVOKED
```

第一次 validation 成功或失败都永久消费 validation opportunity；并发 validation 只能有一个 winner。admitted carrier 只签发
`r1-future-manifest-carrier-consumption-input/0.1` one-shot private input；future consumption 同样只能有一个 winner。copy、deepcopy、pickle、
JSON-like restoration、foreign attempt/context、mutation、replay、late stop、wrong branch/route/variant、role/path swap、digest drift 与 authority
ceiling expansion 均 typed fail closed。本文不实现 Manifest producer 或 transport。

## 5. independent conformance owner

`_derivation_evidence_manifest_carrier_conformance.py`不 import producer projector，也不读取 path 或重调 Provider。它从 copy-owned raw bytes
独立复算：

- Evidence 0.3 closed keys、canonical bytes、request provenance 与 evidence digest；
- attempt/context binding、input/application/continuity cross-binding；
- fixed role/path order、raw hash、size、semantic digest 与 legacy isolation；
- CoverageLedger conformance、Fact/Relation/Slice present/absent/unknown topology 与 root-chain digest；
- normal/negative branch、route、variant、result kind 与 authority ceiling。

producer projection function 与 independent conformance function 必须不同，`shared_expected_projector_state`必须为 false。测试不能用 producer
expected document 替代 oracle；形式自洽不冒充原工程问题已经解决。

## 6. 八个 live worlds 与 DEMC falsifiers

focused suite 覆盖 doc426 的四个 normal 与四个 negative live worlds：

```text
normal:    branch empty / closed empty / partial / relation conflict
negative:  ZERO_PARSE_DENOMINATOR / ALL_PARSE_REJECTED /
           PROJECTION_BLOCKED / REQUIRED_PROVIDER_NON_SUCCESS
```

`DEMC-000..019`直接覆盖八世界 admission、exact 0.3 dispatch、branch/route/variant、ledger/root drift、foreign attempt、owned snapshot
mutation、present/absent topology、relation conflict qualified unknown、legacy alias、role/path order、raw/semantic binding、common-mode oracle、
no-path/no-Provider validation、late stop、validation race、future-consumption race、authority ceiling 与 immutable legacy bytes。

## 7. final source/test identity

七个 implementation/test blob 的本地候选 SHA-256 为：

| Path | SHA-256 |
| --- | --- |
| `_same_attempt_derivation_evidence_continuity.py` | `6c11b5e04c16a86157fd69c74b7bf1c308861ac6e5f5351cbbc00e5b6d2c8d3c` |
| `_derivation_evidence_manifest_carrier_conformance.py` | `8a8208895617a8f13ff33e262e38ddf7497511c777501f616932c3cd69dc4800` |
| `_derivation_evidence_manifest_carrier_successor.py` | `276d9a3b001d9ce616b1b138395187cd5813969b5137cd71bae26d2327e11a7c` |
| `test_derivation_evidence_manifest_carrier_successor.py` | `3ed552e44e538b1eb0254bb24fcc55de9f85ada3ad2ec51606501534d7873be8` |
| `review-derivation-evidence-0.3.schema.json` | `23d664d09dcf59f795030c87651a32ecd8b59f636419dfd8ed4a2638bc18325e` |
| `test_review_r1_derivation_evidence_0_3.py` | `b6cb83f9732ee7aef4eb25a85150b1fe5ab75a881ce3ac2a185d495e424f59f7` |
| `test_review_r1_schema_payload.py` | `04e1a31763b9cbfd2a523a766ac552a48ecbae502865bbd658876270a2dd4a39` |

## 8. final local qualification

final focused matrix：

| Python | mode | 结果 | log SHA-256 |
| --- | --- | --- | --- |
| 3.10.6 | normal | 20/20 PASS | `8ecd2627989d2fc11a7a7639e0a03f0b7536105302f14146d3ab1302eaf6c8f5` |
| 3.10.6 | `-O` | 20/20 PASS | `bcb3d35e8448884df7564b319407a685c0d65533545f466b0366760e6074ee16` |
| 3.13.13 | normal | 20/20 PASS | `f861275548b1d764ec2e322c3becd1d30cc507df6897c76ca60963a8674f6f5a` |
| 3.13.13 | `-O` | 20/20 PASS | `3dbb9509d60dfb923afc88760492af257731aacc3502658d786c1cb48f076b16` |

完整 Review Attention discover matrix使用去重后的 694 个 unique tests：

| Python | mode | 结果 | log SHA-256 |
| --- | --- | --- | --- |
| 3.10.6 | normal | 691 passed / 3 skipped | `ee7ffdc9f765ed262f129238c2ba9a878c7dc13f1490b751a0866f95541bba75` |
| 3.10.6 | `-O` | 691 passed / 3 skipped | `67cba4a1b21b8961d5b6dcbefabfbbbfbb173a964a0cc1d2a6fc28e2beed1891` |
| 3.13.13 | normal | 692 passed / 2 skipped | `e314a70499959e1a65187c8e97071c7952a1696434e63ab27fb70734f994067b` |
| 3.13.13 | `-O` | 692 passed / 2 skipped | `36ba400d36cf899b9a8846e2245f4dc57a5fbaa87c4f47118aa6e05ddd9e5b50` |

Schema/payload matrix每格26/26 PASS；四格日志 SHA-256 依次为：

```text
57a140c6c391301deef7548a23a821e10cca46b849a72c5cc0cd47af9e4604f3
bb5b60a0907928de81d7207169a6d2f2764158a0af9ec1a2b2c12e85d8d7ab21
d3dc7a63fc726447ce737eeb0be2535ad7943e9fe1bd27b15502497305b7c114
1fa92511b21af806179b91a09742da615496264e9d9bba03e5e6caf704cc0efc
```

双 Python compile、hygiene unittest、global/local hygiene、`git diff --check`、forbidden public export guard 与 primary audit continuity
均 PASS。final local qualification SHA-256 为`0af06bcd0ed4ee4a35f1ec43cfcacb1822e921b9de610ab93ac3752c3567ae50`；
48-artifact local evidence root 的 seal 文件 SHA-256 为
`a626aca4a4df63079dd67254c6f49c8c97d2731a2e1fca7e7c7aeff805322f3e`，其排除自身的 47-artifact mapping SHA-256 为
`0b08d8c63a28b15a764653952949bb7a68bde514d1aaef812e54a6502c86fd76`。这些只作 local candidate witness。

## 9. retained prequalification 与 setup history

formal qualification前发现并修正两类边界：

1. `DEMC-005`首个测试只重新构造了同值 tuple，没有实际变异 owned snapshot；该 proof-target failure 保留，后继测试直接变异
   claim/candidate bytes并增加嵌套snapshot seal；
2. prequalification review发现 independent conformance 对 attempt binding、context identity 与 exact normal/negative object binding 仍不够
   closed；修正为 closed field set、positive finite budget、独立 context digest 与 exact object identity后，才运行 final sealed matrix。

另外，首个 full discovery因测试模块直接 import support `TestCase`而重复发现26项；该 proof-facility identity保留，正式矩阵使用694个
unique tests。wrong worktree、managed-worktree long path、attachment cap、PowerShell parser/pipeline、Windows wildcard、direct hygiene import、
blocked cleanup command与aggregate seal direct-output truncation等 setup errors全部保留。两个被策略阻止的清理命令没有文件系统效果；随后只对
四个明确的 ignored `__pycache__`路径运行`git clean -ndX` dry-run和 exact `git clean -fdX`，不删除产品证据或用户文件。

后继 PASS 不覆盖任何 FAIL、ERROR、CANCELLED、setup failure 或 UNKNOWN，也不把 proof-facility failure冒充产品失败。

## 10. tracked scope 与后继资格链

本候选 tracked scope 只允许：

```text
README.md
AGENTS.md
docs/434-r1-manifest-carrier-successor-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_same_attempt_derivation_evidence_continuity.py
plugins/review-attention/src/veritrail_review/_derivation_evidence_manifest_carrier_conformance.py
plugins/review-attention/src/veritrail_review/_derivation_evidence_manifest_carrier_successor.py
plugins/review-attention/tests/test_derivation_evidence_manifest_carrier_successor.py
schemas/review-derivation-evidence-0.3.schema.json
tests/test_review_r1_derivation_evidence_0_3.py
tests/test_review_r1_schema_payload.py
```

doc426–433、`docs/project-state.md`、workflow、legacy Schema、public exports、Provider、Manifest、persistence、public Review、Core Verdict 与
R2–R6必须保持 base bytes。完整资格链为：

```text
final implementation candidate bytes / declared local gates
    -> immutable pre-created PR body seal
    -> original PR required 15/15 gate without metadata edit or rerun
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / eight-world / conformance / retained-history reconciliation
    -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
    -> return CONTROL LOOP
    -> separate docs-only implementation freeze publication
    -> FROZEN only after that publication's complete qualification chain
```

相同 source hash、local PASS、测试摘要或 doc433 authority不能继承任一后继门资格。

## 11. 当前状态与 stop line

本文只发布：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_AUTHORIZATION_PR493_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_CANCELLED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_AUTHORIZATION_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

original PR、protected merge、new exact-main dual gates、fresh anonymous installed-product readback、independent reconciliation与finite closeout
全部闭合前，不得升级本文状态。闭合后也必须返回 CONTROL LOOP另建 docs-only freeze publication；不能按文档编号直接创建 Manifest、恢复
global composition authority或启动R2–R6。R1完成后仍须由人类与AI共同执行独立全项目检查。
