# R1 Review Derivation Manifest 0.2 私有实现候选

日期：2026-11-22

> 当前状态：`R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NOT_FROZEN`。
>
> 施工基线：`main@50819b8ab16800a415439285dc9fcf909d5b435a`，tree
> `42f4337bb1b49957929c15fedf207e1aecfa5c06`。
>
> 授权来源：[Manifest 0.2合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)、
> [合同冻结](317-r1-review-derivation-manifest-negative-world-successor-contract-freeze-publication.md)、
> [carrier实现冻结](435-r1-manifest-carrier-successor-private-implementation-freeze-publication.md)、
> [feasibility successor审计](447-r1-review-derivation-manifest-0-2-private-implementation-feasibility-successor-audit.md)与
> [private implementation授权发布](448-r1-review-derivation-manifest-0-2-private-implementation-authorization-publication.md)。
>
> 影响：`L3_PRIVATE_RUNTIME_AND_TESTS / ONE_PUBLIC_SCHEMA_RESOURCE / ONE_COMPATIBILITY_FIXTURE / NO_DEFAULT_COMPOSITION`。
> 本文只形成bounded A–J implementation candidate；不声明merged、exact-main verified、readback qualified或frozen，不恢复
> global composition authority，不创建public Review、Core Verdict、标签、Release或R2–R6能力。

## 1. CONTROL LOOP 与已生效授权

PR #511把doc448 candidate精确合入：

```text
base   f2394bdbb2910d5cc14bd1296d7ef503d2b60e66
head   59c05a002562fa77c887c81dab49302f5efb04dc
tree   42f4337bb1b49957929c15fedf207e1aecfa5c06
merge  50819b8ab16800a415439285dc9fcf909d5b435a
```

三个远端门均为原始attempt，没有rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #511 original Public CI | `44905508551` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `44909682401` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `44909682395` | 1 | 1/1 SUCCESS |

fresh anonymous public Core 0.13.0与GitHub Evidence 0.1.1 installed-product formal中，attempt 1 adapter error与attempt 2
readback error继续保持原identity；唯一qualifying attempt 3为`FORMAL_P1_P2_READBACK_PASS`，其API Evidence、Render Evidence与
formal record SHA-256分别为：

```text
5882d5745f867079ae977c1bca569c256d54c43f48b0169215ae915ccb0370bb
a62d0f1c778661b4dcb9ba78dfb1b16208cabb981b54271dff6475f5fd5734e2
d918d0b518f0dec7eadd0893f01548f8285962bc216af36ff770918ad3d2909b
```

README、doc316、doc317、doc435、doc447、doc448与milestones各自唯一raw-byte readback也全部PASS。independent
reconciliation、110-artifact finite closeout与post-closeout integrity SHA-256依次为：

```text
3319c08176043834c7bc081d963ddd626a1311002f1ab0abded18fc432584dfc
e8cf4086eee0331775ebecb7ae93c602f0de30688085d24688166066812947eb
007f077e4577040b7b98bd060319dcae657a5edf36d1c58f7b7db4837dd91dd9
```

因此以下authority已经生效：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
```

fresh CONTROL LOOP重新核对exact main、doc316/doc317冻结合同、doc435 carrier freeze、doc447 qualified history、doc448 authority
ceiling、Manifest 0.1 bytes、PR #498与doc437保留失败，以及primary `audit.json`。没有反例要求重开冻结边界。最小合法施工面仍是
doc448 bounded A–J；`proof_is_not_problem_solving = true`、`local_not_global = true`。

## 2. Schema 0.2 与兼容向量

本候选新增公开resource `schemas/review-derivation-manifest-0.2.schema.json`，固定closed
`R1_DERIVATION / 0.2 / veritrail-json-c14n/1` document：

- `COMPLETE / DIAGNOSTIC / COVERAGE`三类outcome分别拥有闭合的role/path结构；
- CoverageLedger始终是最后一个record，所有present child都必须与carrier record、set entry、raw SHA-256、size与semantic digest
  精确绑定；
- optional relation/slice topology只从冻结CoverageLedger事实机械派生，不用placeholder冒充absence或unknown；
- unknown version、closest version、旧Manifest 0.1或错误conformance identity不得fallback为0.2。

`tests/fixtures/review-derivation-manifest-0.2/compatibility-cases.json`固定positive branches、八个live worlds、relation-conflict
roles和`RDMC-000..013` falsifier denominator。旧Manifest 0.1 Schema bytes保持base不变。

## 3. 私有projector、candidate与exact authority

`_review_derivation_manifest_0_2.py`只接受冻结carrier的一次性copy-owned consumption input，并机械投影：

1. 固定prefix role/path顺序与CoverageLedger末位；
2. 逐项保留raw SHA-256、size、semantic digest、carrier record和root topology；
3. 根据CoverageLedger投影present/absent/unknown child，不重读路径、不重调Provider；
4. 形成exact 0.2 canonical bytes与input snapshot digest；
5. 把construction、validation、admission、consumption与private staging分别绑定到同一候选identity。

candidate construction、validation与private staging都是one-shot。成功、失败、并发race、late replay、copy/deepcopy、snapshot mutation、
role/path swap、foreign producer、wrong ledger prior conformance或authority ceiling expansion全部typed fail closed。candidate构造需要私有
`_CANDIDATE_TOKEN`，只有`build_review_derivation_manifest_0_2_candidate()`能够发放；直接调用class constructor不能绕过carrier
one-shot claim。private staging只返回caller-owned bytes与receipt，不写文件系统、不进入default composition。

## 4. 独立conformance owner

`_review_derivation_manifest_0_2_conformance.py`不import producer projector，不读取path，也不调用Provider。它独立复算：

- exact producer/conformance identity、closed snapshot shape与authority ceiling；
- fixed role/path order、raw hash、size、semantic digest与Manifest 0.1 isolation；
- carrier proof、CoverageLedger entries/prior conformance、root binding与root-chain topology；
- outcome kind、present child topology和完整canonical document。

producer function与conformance function不同，测试通过AST检查可执行imports/calls而不是扫描注释或docstring。producer与validator共同
接受一个document只证明有界conformance，不冒充现实问题、全局组合或公开Review已经成立。

## 5. 八个live worlds 与 RDMC falsifiers

focused suite从冻结carrier真实构造下列八个world：

```text
NORMAL_CONSISTENT
NORMAL_BRANCH_EMPTY
NORMAL_SLICE_PARTIAL
NORMAL_RELATION_CONFLICT
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

`RDMC-000..013`覆盖legacy不变性、unknown version、Coverage缺Ledger、duplicate role/path、role/path swap与traversal、Ledger非末位、
absent/unknown placeholder、present root缺carrier、set/root artifact digest漂移、raw hash、size、Ledger entry digest、prior conformance及
foreign/unsafe/interrupted publication。额外witness覆盖direct-constructor bypass、construction/validation/staging失败消耗、并发winner、
snapshot mutation、replay/copy与独立owner无path/Provider access。

## 6. final source/test identity

七个implementation/test blob的final candidate SHA-256为：

| Path | SHA-256 |
| --- | --- |
| `schemas/review-derivation-manifest-0.2.schema.json` | `fd37bc4085999dea64715fb7e72073c20d08c3c7ce14b9c2e3fd04895b7a4fa7` |
| `tests/fixtures/review-derivation-manifest-0.2/compatibility-cases.json` | `477d838d06839400f29c1c6c6bf6d088f9bb7245326072c688ba9f8939a17ad7` |
| `_review_derivation_manifest_0_2.py` | `2960da3f6dd511d8da8aed1629a40dcea36adc4de8e461e83292e341b1db1985` |
| `_review_derivation_manifest_0_2_conformance.py` | `13e112b429acf4989452612416276b895af9d3b7d1f5d5d5172471d87101ed65` |
| `test_review_derivation_manifest_0_2.py`（plugin） | `512f4d26ea1e649f087fd2c5652b630668b7e7253e9d6cce65cef803e260c680` |
| `test_review_derivation_manifest_0_2.py`（root） | `231bdc51a9a9391d899a1b464f3d1a07c5a90d0b1da1565fdb268fffcd2e84b5` |
| `test_review_r1_schema_payload.py` | `1a2d1e1d0137cb2e0f5226264d9f19f6c12058b6e16c44ca965fbea45d76e5b1` |

Manifest 0.1 SHA-256保持`69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91`。
formal v4 input seal SHA-256为`26ac3f6971a6fcd0261aa7c300fa28714c3a5528d1272d1a07bd65877b4a619a`。

## 7. final local qualification

final focused matrix每格26/26 PASS：

| Python | mode | log SHA-256 |
| --- | --- | --- |
| 3.10.6 | normal | `1e54c0f87853705b94ed1128144c09b42dcbd3c305b82ab4dcc20ee51ba25b3d` |
| 3.10.6 | `-O` | `1e4c6aa0d4aaa18d6c45e67f2952fe51279afc3255e907cf24d5b0eb19c91dd1` |
| 3.13.13 | normal | `8b6b1769264f5eb411c5d60c13deba3b50d6e661beb08d1506a321e89821b95b` |
| 3.13.13 | `-O` | `d948dee74bdbd13cd94effd5664d7ab3ae2d9c82434173127e5b55de270393f0` |

完整Review Attention discover matrix每格715 reported：

| Python | mode | 结果 | log SHA-256 |
| --- | --- | --- | --- |
| 3.10.6 | normal | 712 passed / 3 skipped | `fc56fd5084f5589cb9ab8ce96446c45a85fc830e325aee8e30fa951439c12ce7` |
| 3.10.6 | `-O` | 712 passed / 3 skipped | `d85f3dd2fe9d0b1def47c73eb13862ed7e5322dd804c217afbb5fc6f5263ca96` |
| 3.13.13 | normal | 713 passed / 2 skipped | `5441425cf107984b7b35a16d708f0793f1efbfcb55258136301e87b1aa4c14ec` |
| 3.13.13 | `-O` | 713 passed / 2 skipped | `b6432aba7be87004202ff3ab7de00566a6668f48f7009b2e471f75e2d484831d` |

root Schema/payload matrix每格27/27 PASS；四格日志SHA-256依次为：

```text
9e362d038d87d2acc0707becff4fd6902e43a07cd58b68998b6fc3e2dcc2fbf0
69abbe2b9e0244b3a6959b4af2a4b9714a7042a5d6a418e31239c46ae5f103b6
8ba8602ad2d6b8100496ef102628f9bcdd40f60f1b1df344c1767758803ea98f
2c5fd5d64a36f003747ae3d74b2ebceb1b4326d9426d19575d9be6811fd8f4f7
```

双Python normal/`-O` static parse、global/local hygiene、`git diff --check`、forbidden external runtime reference guard、
Manifest 0.1不变性与primary audit continuity均PASS。以上只作local candidate witness。

## 8. retained failure 与 setup history

formal qualification前的review保留三项发现：

1. `PREQUAL-REVIEW-001`：首个independence proof错误扫描注释/docstring并命中`Provider`，属于proof-target false positive；修正为
   AST executable import/call检查；
2. `PREQUAL-REVIEW-002`：foreign producer identity可被独立conformance判为QUALIFIED，属于private implementation defect；修正为
   conformance owner独立冻结exact producer identity与closed snapshot；
3. `PREQUAL-REVIEW-003`：failed construction/validation/staging、staging race及0.2改写0.1 fallback的proof denominator不完整；已补充
   witnesses后才进入formal matrix。

正式矩阵后又发现`POST-FORMAL-REVIEW-001`真实合同阻断反例：caller可绕过factory，直接从同一carrier material构造并admit两个
candidate，两个admission digest相同。原counterexample日志SHA-256为
`796786da719b1d986470a95ae5b11377a312add57c3fe23f59681ac926b57c2d`。最小修正只增加private construction token与直接构造
拒绝test；Python 3.13 targeted correction为21/21 PASS，日志SHA-256
`99e636421b1245183f18cec418815f30a388637c57c924fb13a7beb48a728ec8`。修正前PASS继续是真实旧bytes观察，但不得资格化final v4
bytes；因此本节第7节所有矩阵均在修正后重新执行。

早期focused/full/root-payload矩阵、foreign-producer probes、wrong-path、hygiene log identity collision、PowerShell parser/pipeline、
tool orchestration syntax、以及Python 3.10 `-O` full product PASS后的`Tee-Object -LiteralPath -Append` post-terminal wrapper error全部按
原identity保留。wrapper error没有改变product log或terminal result，不重跑同一product identity。后继PASS不覆盖任何FAIL、ERROR、
CANCELLED、setup failure或UNKNOWN，也不把proof-facility failure冒充产品失败。

## 9. tracked scope 与资格链

本候选tracked scope只允许：

```text
README.md
AGENTS.md
docs/449-r1-review-derivation-manifest-0-2-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_review_derivation_manifest_0_2.py
plugins/review-attention/src/veritrail_review/_review_derivation_manifest_0_2_conformance.py
plugins/review-attention/tests/test_review_derivation_manifest_0_2.py
schemas/review-derivation-manifest-0.2.schema.json
tests/fixtures/review-derivation-manifest-0.2/compatibility-cases.json
tests/test_review_derivation_manifest_0_2.py
tests/test_review_r1_schema_payload.py
```

doc316–448、`docs/project-state.md`、workflow、Manifest 0.1、public exports、Provider、default composition、persistence、public Review、Core
Verdict与R2–R6必须保持base bytes。完整资格链为：

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

相同source hash、local PASS、测试摘要或doc448 authority不能继承任一后继门资格。

## 10. 当前状态与 stop line

本文只发布：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FEASIBILITY_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_ALLOWED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

original PR、protected merge、new exact-main dual gates、fresh anonymous installed-product readback、independent reconciliation与finite
closeout全部闭合前，不得升级本文状态。闭合后也必须返回CONTROL LOOP另建docs-only freeze publication；不能按文档编号恢复global
composition authority、启动public Review或R2–R6。R1完成后仍须由人类与AI共同执行独立全项目检查；未来开源能力组合不得反向充当本候选
资格或改变R1 stop line。
