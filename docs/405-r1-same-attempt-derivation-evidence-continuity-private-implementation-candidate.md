# R1 same-attempt DerivationEvidence continuity private implementation 候选

日期：2026-11-11

> 状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_FROZEN`。
>
> 施工基线：`main@b5ff07e03630d57060384883d28a49dc57bdf0df`，tree
> `a1147c811133f9834bf587c5245189f773c474cd`。
>
> 授权来源：[最小合同 0.1](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [可行性审计](403-r1-same-attempt-derivation-evidence-continuity-private-implementation-feasibility.md)与
> [private implementation 授权发布](404-r1-same-attempt-derivation-evidence-continuity-private-implementation-authorization-publication.md)。
>
> 影响：`L3_PRIVATE_RUNTIME_AND_TESTS / NO_PUBLIC_EXPORT`。本文不发布merged、exact-main verified、readback qualified或frozen状态，不恢复
> global composition authority，不创建Schema、manifest、persistence、public Review、Core Verdict、标签、Release或R2–R6能力。

## 1. CONTROL LOOP 与已生效授权

PR #463把doc404 candidate
`base=ffe57f80d3c0eef85dcb5ad39753a0d7a1abbb11 / head=445e014708a78c16b362951133480193575fc8cf /
tree=a1147c811133f9834bf587c5245189f773c474cd`精确合入
`main@b5ff07e03630d57060384883d28a49dc57bdf0df`。三个远端门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #463 original Public CI | `42981105555` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `42986054505` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `42986054537` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc397、doc402、doc403与doc404各有唯一qualifying readback；AGENTS与milestones的raw、Contents
API与exact Git bytes一致，independent reconciliation与finite closeout也全部成立。因此：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
```

fresh CONTROL LOOP重新核对remote main、exact base、冻结合同、PR #453/#457/#459及fresh formal failures、旧Evidence 0.2、现有
Fact/Relation/Slice/Coverage/admission authority与primary `audit.json`。没有反例要求重开doc397或扩大doc404；当前最小合法施工面仍是
bounded private A–J。global composition authority保持`NOT_RESTORED / NOT_AUTHORIZED`。

## 2. versioned private identity 与 authority ceiling

本候选新增且只在private模块内可见：

```text
contract function             r1-same-attempt-derivation-evidence-continuity/0.1
private continuity domain     SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_0_1
controller capture function   r1-derivation-evidence-controller-capture/0.1
branch projection function    r1-derivation-evidence-continuity-branch-projection/0.1
independent reconciliation    r1-derivation-evidence-continuity-reconciliation/0.1
binding identity              r1-same-attempt-derivation-evidence-continuity-binding/0.1
profile identity              r1-same-attempt-derivation-evidence-continuity-profile/0.1
wire identity                 r1-same-attempt-derivation-evidence-continuity-wire/0.1
```

`veritrail_review.__init__`没有新增export。private value只允许声明same-attempt continuity、exact discriminated one-shot branch与原执行期
controller timing；legacy Evidence 0.2、public Schema、manifest、persistence、public Review、Core Verdict、global composition authority与
R2–R6全部为false。

## 3. bounded A–J 实现映射

| ID | 本候选实现 |
| --- | --- |
| A | 新建versioned private capture slot与committed value；构造token、owner、result和encoded bytes均为exact identity，copy/pickle/JSON/duck type不能恢复authority。 |
| B | slot绑定同一`OwnedProductFactConsumer`、原始attempt、`DerivationInputSet`、live `BudgetContext`、eligibility、selector与terminal source；equal bytes/digest或同字符串ID不能替代对象authority。 |
| C | Fact controller在真实claim执行前后copy-own attempt/provider/phase UTC wall time；Provider output中的自报时间不进入capture。 |
| D | normal route在one-shot transition continuation消费前copy-own完整transition admission bytes；late capture、missing capture与recovered authority均拒绝。 |
| E | Relation controller在真实ProviderRun执行期copy-ownrun与phase timing，并逐项绑定transition的完整`provider_run_ids`与lineage denominator。 |
| F | normal branch绑定exact `ReviewSliceSet`/CoverageLedger/root chain/application admission；Relation conflict且Slice null继续是normal qualified unknown。 |
| G | 四类negative branch绑定exact qualified Coverage与Fact/Relation/Slice缺席；`NOT_STARTED`不能伪造timing，实际started Provider必须保留controller timing。 |
| H | foreign attempt、copy-equal authority、wrong route/result、unknown branch、replay、并发第二commit、mutation、late stop与cleanup failure均fail closed并永久revoke。 |
| I | owner与独立reconciler分别投影五类route；reconciler重新核对terminal source、application admission、Coverage/root chain与authority ceiling，不共享关键route projector。 |
| J | 新private suite把doc397的`DEC-000`至`DEC-029`变成direct falsifiers，并与旧selector、Fact、Relation、Coverage、legacy boundary与unified admission回归共同执行。 |

## 4. one-shot lifecycle 与五类route

slot生命周期为：

```text
PROVISIONAL
  -> CAPTURING_FACT
  -> FACT_CLOSED
  -> CAPTURING_NORMAL | CAPTURING_NEGATIVE
  -> OUTPUT_ADMITTED
  -> COMMITTED

any invalid transition -> REVOKED
```

normal只接受`RELATION_HANDOFF`与`NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY`；四类negative只接受
`FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`与`NEGATIVE_WORLD_COVERAGE_CONTINUITY`：

```text
ZERO_PARSE_DENOMINATOR
ALL_PARSE_REJECTED
PROJECTION_BLOCKED
REQUIRED_PROVIDER_NON_SUCCESS
```

unknown branch没有negative catch-all。negative output继续是qualified Coverage结果，不被重写为`FAILED`或`UNAVAILABLE`；normal
Relation conflict也不被重分类为negative。

## 5. 原执行期 controller capture

Fact capture为每个expected claim保留descriptor、launch key、lifecycle、provider start/finish与phase finish，并绑定attempt start和Fact
phase finish。Relation capture绑定完整transition `provider_run_ids`顺序、provider lineage cardinality、descriptor、run status、release
outcome、phase status及每条time chain。全部UTC wall time必须是canonical microsecond `...Z`，并满足单调顺序。

commit后每次读取都重新核对：

1. live context与原context identity；
2. 当前input digests与原始capture；
3. 当前Fact与Relation capture document与committed bytes；
4. 当前result live API、CoverageLedger、root chain与application admission；
5. fresh independent reconciliation与committed reconciliation逐字节一致。

因此绑定后的capture、input、result或ledger发生变异时，不能继续读取旧continuity值，也不能从equal bytes恢复authority。

## 6. direct falsifiers 与已有边界回归

新private suite共26项测试，直接覆盖`DEC-000`至`DEC-029`。其中一项可以同时覆盖多个紧密相连的falsifier，但每个ID都在测试方法或
断言中有机械marker。新增的直接反例包括：

- Provider自报controller timing、Fact或Relation capture缺项；
- negative `NOT_STARTED` fabricated timing、started Provider缺finish、placeholder injection；
- normal/negative wrong-result双向提交与unknown bound branch；
- negative语义重写、legacy projector alias与authority ceiling扩张；
- context stop、cleanup incomplete、committed capture/input/result mutation；
- replay、并发commit、copy/pickle/JSON与qualification inheritance。

既有post-terminal selector与unified output admission 48项回归在修正后单独PASS；它们不替代新continuity suite，也不被新suite替代。

## 7. final candidate source/test bytes

六个private implementation source/test文件的冻结本地候选SHA-256为：

| Path | SHA-256 |
| --- | --- |
| `_fact_fulfillment.py` | `f2dad4e394edff4323d26eedf0647ade7a0d48f2e7f425ba63ee21e5313742cb` |
| `_fact_relation_transition.py` | `e6ce67331b7055623971f1edb3a9830b89e0c2fb47020ea67093714538eeaa8d` |
| `_post_terminal_fact_dual_successor.py` | `d7f19f631f4527278f4f660a2aa7a57b661ced0ec51a2a5cffa954b15e2e0742` |
| `_unified_review_coverage_output_admission.py` | `5194c7431429a9181c8e2a744fe419816699be835a05b54b831c806d05b5be51` |
| `_same_attempt_derivation_evidence_continuity.py` | `dc42d38c68ed6cc96dc072f5d51a5289b67648f4252e29af7a1c3d2b2a759a42` |
| `test_same_attempt_derivation_evidence_continuity.py` | `4ada737c77b7e7a0c033a18c59f9ca837f11b9e5586cbcde69241da0e3c5ba11` |

formal runner在执行前机械比较这六个hash；任何漂移先停止，不产生新PASS。

## 8. final local qualification

semantic runner在每格真实构造normal与四类negative路径，删除随机ID和clock value，只保留identity、capture shape、five-route语义、
reconciliation、authority ceiling、falsifier marker与source hashes。Python 3.10.6/3.13.13 × normal/`-O`四格全部PASS且逐字节一致：

```text
canonical semantic SHA-256  dfba622dd81e3b13938c0f4b71b7354a0b3708b5cb4ac420b76b04274a002bd3
semantic matrix SHA-256     885e9ba58c25559d6f7c3ea7e115defc10af58314ece40f304955283c5aa03f9
```

focused matrix包含七个既有关键测试文件与新continuity suite：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 152/152 PASS |
| 3.10.6 | `-O` | 152/152 PASS |
| 3.13.13 | normal | 152/152 PASS |
| 3.13.13 | `-O` | 152/152 PASS |

focused matrix SHA-256为`8848acfeeb0bcb4ac59ffa73efd7bb2bea3484b1c216108599b314f97e35f327`。

完整Review Attention discover matrix使用相同candidate source/test bytes：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 674/674 PASS |
| 3.10.6 | `-O` | 674/674 PASS |
| 3.13.13 | normal | 674/674 PASS |
| 3.13.13 | `-O` | 674/674 PASS |

full matrix SHA-256为`70157b6fe04e51093bef60d7eaabbcfd9d5edf31b7230917b66ecf18b7b27ab5`。两套Python compile、
`git diff --check`、global/local hygiene、forbidden public export guard与primary audit continuity也PASS。测试只作当前candidate witness，
不替代original PR、protected merge、exact-main gates或installed-product readback。

## 9. retained prequalification 与setup history

正式矩阵以前发现并修正的private implementation缺陷全部保留：

1. legacy relation path capture-order regression；
2. qualified `REQUIRED_PROVIDER_NON_SUCCESS`被过早revoke；
3. Relation capture没有证明完整ProviderRun denominator；
4. committed value读取未重新绑定Fact capture、input digest、result与ledger mutation。

测试/证明设施历史也保持原identity：

1. DEC-004在错误外层期待exception；
2. 混合working bytes的focused run被主动`CANCELLED`，没有输出可用于资格；
3. DEC-012错误要求私有异常穿透typed outer boundary；
4. DEC-021/022先后复用了已消费fixture并向每个Fact claim注入cleanup failure；
5. system Python无pytest与Codex attachment cap只构成setup error。
6. local validation的首个PowerShell source-hash display命令在执行检查前发生parser setup error。

prequalification findings、setup history与source identity SHA-256分别为：

```text
aa6be2a0957cb81efabc427c2c9c5dee8d53e61eb74cef2ef845105ba64811bd
abdc76f1a97817f53eec61cc4555e412d397214bc61a37f5233efda3764b0e0b
135816d90044c68e684123fbff71368ec6b1effe1b7cd8e2086d802975da0226
```

后继PASS不覆盖任何FAIL、ERROR、CANCELLED、setup failure或UNKNOWN，也不把测试设施失败冒充产品失败。

## 10. tracked scope 与资格链

本候选预期tracked scope只允许：

```text
README.md
AGENTS.md
docs/405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_fact_fulfillment.py
plugins/review-attention/src/veritrail_review/_fact_relation_transition.py
plugins/review-attention/src/veritrail_review/_post_terminal_fact_dual_successor.py
plugins/review-attention/src/veritrail_review/_same_attempt_derivation_evidence_continuity.py
plugins/review-attention/src/veritrail_review/_unified_review_coverage_output_admission.py
plugins/review-attention/tests/test_same_attempt_derivation_evidence_continuity.py
```

doc397–404、`docs/project-state.md`、public exports、Schema、workflow、fixtures、manifest、persistence、public Review、Core Verdict与R2–R6
必须保持base bytes。完整资格链为：

```text
final implementation candidate bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent source-byte / five-route / capture-owner / retained-history reconciliation
    -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
    -> return CONTROL LOOP
    -> separate docs-only implementation freeze publication
    -> FROZEN only after that publication's full qualification chain
```

相同source hash、semantic digest、local PASS或上游doc404 readback都不能继承任一后继门的资格。

## 11. 当前状态与 stop line

本文只发布：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_MERGED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文不宣称implementation已经合入、exact-main verified、readback qualified或frozen。候选完成自己的资格链后仍必须返回CONTROL LOOP，
重新审计manifest successor与剩余R1的全部前提；文档编号、绿色CI或局部矩阵都不是调度器。`local_not_global = true`，即使本候选未来
冻结，也不能冒充整个R1或最终产品已经全局可组合。R1完整闭合后，必须由人类与AI共同执行独立全项目检查。
