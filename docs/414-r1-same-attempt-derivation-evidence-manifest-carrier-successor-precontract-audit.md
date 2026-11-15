# R1 same-attempt DerivationEvidence manifest carrier successor precontract audit

日期：2026-11-15

> 候选状态：
> `R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDIT_CANDIDATE_NOT_QUALIFIED`。
> 本文自己的完整资格链闭合以前，不是qualified history，不选择successor版本号，不授权创建Schema、fixture、validator、carrier、
> producer、consumer、Manifest、publisher、persistence、global composition或public Review产品。
>
> 审计基线：`main@af39730a4527157cc820d23ad40557f5d2c3de30`；tree
> `01844ea351abc59b655305f9fc79a0d4b74c83b7`。
>
> 上游：[manifest 0.2冻结合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)、
> [same-attempt continuity合同](397-r1-same-attempt-derivation-evidence-continuity-contract.md)、
> [private implementation冻结发布](411-r1-same-attempt-derivation-evidence-continuity-private-implementation-freeze-publication.md)、
> [前提当前状态审计](412-r1-review-derivation-manifest-successor-prerequisite-current-state-audit.md)与
> [implementation feasibility recovery audit](413-r1-review-derivation-manifest-successor-implementation-feasibility-recovery-audit.md)。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION / READ_ONLY_PRECONTRACT_AUDIT`。本文不修改runtime、tests、fixtures、workflow、
> Schema、Provider、Collector、P2/Core oracle、Verdict或任何frozen semantic bytes。

## 1. CONTROL LOOP：doc413资格化以后仍须重审下一seam

PR #474把doc413 candidate
`base=b596776cc9e8782ca491f98de0fec8568fecb8b9 / head=f35ae3966c9850b5859cf017e662d9fb0d864005 /
tree=01844ea351abc59b655305f9fc79a0d4b74c83b7`精确合入本审计基线。original Public CI `43704551763`与
exact-main Public CI `43707526555`均attempt 1 15/15 SUCCESS；Browser Smoke `43707526538`为attempt 1 1/1 SUCCESS。
fresh README/doc316/doc397/doc412/doc413各有唯一qualifying formal PASS，AGENTS/milestones与三个private source-test target各有唯一
raw/API/exact-Git全字节一致PASS。README diagnostic #1的marker selection failure按原identity保留，formal没有重跑。

independent reconciliation、175-artifact closeout与finite integrity分别为：

```text
079559aee40ab9bcbe9c7a68fc03065309550a0e831eb92d22419a74c8109096
0d6302cf034efe8b7d7ed1622b1e7b17808a2d380dfdf9c3ac2a8d4323002236
7656cab2e882ef9a08b2545c62fae64ae99d847655555a1bcc001110e085e0d4
```

所以doc413现在是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。它允许fresh CONTROL LOOP审计successor seam，但不把
`UNPROVED_VERSIONED_EVIDENCE_SUCCESSOR_CARRIER_SEAM`自动变成已选合同或runtime authority。本轮必须先回答一个更具体的问题：

```text
versioned Evidence claim建立以后，future manifest producer从哪里取得同一快照的全部actual child bytes？
```

如果答案仍是“回到private object逐项读取”或“从路径重新读取”，那么manifest绑定的Evidence A与实际消费的children B仍可能不是同一
快照。对Evidence shape的局部修复不能证明完整manifest composition安全。

## 2. 当前五路对象图证明Evidence successor单独不足

read-only semantic audit从exact base在Python 3.10.6 / 3.13.13 × normal / `-O`四格重建五条live route。去除运行时和真实时钟
provenance后，四格authority、topology、availability与ceiling projection逐字节一致：

```text
canonical semantic SHA-256 = a0b33faaef0a3fb838528ec5c20f7a6d0d9c2306aec83dfeefe0e53ad90c4297
matrix SHA-256             = edf9a0dd79ac2b7f4c4d7b2ce2fb9b1917a7e67f967a0978325747eb1c7173e6
```

当前actual document availability是：

| live route | Source / Policy / Profile | Fact | Relation | Slice | Ledger | successor Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `NORMAL_FULFILLED` | present | present | present | present | present | absent |
| `ZERO_PARSE_DENOMINATOR` | present | qualified absent | qualified absent | qualified absent | present | absent |
| `ALL_PARSE_REJECTED` | present | qualified absent | qualified absent | qualified absent | present | absent |
| `PROJECTION_BLOCKED` | present | qualified absent | qualified absent | qualified absent | present | absent |
| `REQUIRED_PROVIDER_NON_SUCCESS` | present | qualified absent | qualified absent | qualified absent | present | absent |

normal route中Fact/Relation由transition document owner持有，Slice/Ledger由composition result持有，Source/Policy/Profile由exact input owner
持有；四条negative route没有也不得伪造Fact/Relation/Slice document。当前private continuity能够绑定这些owners与application admission，
但authority ceiling仍明确是：

```text
legacy_evidence_0_2          = false
public_evidence_schema       = false
manifest                     = false
persistence                  = false
global_composition_authority = false
```

因此“创建一个successor Evidence JSON”只能解决claim shape；它不会自动把分散在同一个one-shot private graph中的actual bytes变成安全的
manifest input。最小缺口必须同时包含版本化claim与精确快照交接。

## 3. 权威分层：carrier不拥有现实事实

未来最小边界必须保持下列authority，不得为了组合方便把Core、Evidence或Manifest变成超级事实源：

| owner | 仍然拥有的权威 |
| --- | --- |
| Source/Policy/Profile与各stage owner | 自己创建、校验与admit的exact document bytes及stage语义 |
| `CoverageLedger` root bindings | Fact/Relation/Slice的`ARTIFACT_PRESENT`、`QUALIFIED_ABSENT`或`QUALIFIED_UNKNOWN` topology |
| unified application admission | 五路exact discriminated result、same-attempt application admission与one-shot消费资格 |
| private continuity owner | 已提交attempt内的input、transition、application admission、controller provenance与result binding |
| future successor projector | 只从已提交continuity和admitted owners形成versioned claim及copy-owned carrier candidate |
| independent carrier validator/admission | 不共享producer projector地复算bytes、digests、topology、attempt与one-shot资格 |
| future Manifest producer | 只消费已admit carrier一次，机械写role/path/digest；不判断stage充分性或现实真假 |
| Core | 既有Plan/session integrity、证据绑定、充分性与Verdict；本文不修改它 |

carrier不是Evidence Artifact，不是Manifest，不是public Schema，不是persistence，也不是新的stage admission。它不因为copy-own bytes就取得
这些bytes所表达事实的权威；它只阻止后继重新读取或拼接不同快照。

## 4. private copy-owned exact snapshot carrier的最小职责

本文不选择类名、Schema版本或序列化格式。后继合同若被授权，至少必须让一个private immutable carrier candidate copy-own：

1. `SourceSnapshot`、`ReviewPolicy`、`DerivationProfile` exact bytes；
2. versioned DerivationEvidence successor exact bytes；
3. 仅在Ledger root为`ARTIFACT_PRESENT`时存在的`FactSet`、`RelationSet`、`ReviewSliceSet` exact bytes；
4. `CoverageLedger` exact bytes；
5. 每个actual manifest child role/path的raw SHA-256、byte size与既有semantic digest；
6. Ledger `root_chain_digest`、每个`binding_digest`及present/absent/unknown topology proof；
7. exact attempt、continuity、transition/application admission与one-shot lifecycle bindings；
8. 明确的optional-child absence，不使用placeholder、空对象或按字段presence猜测。

这些职责不要求修改doc316冻结的role/path：`DERIVATION_EVIDENCE -> derivation-evidence.json`仍可承载显式dispatch的successor版本；
manifest 0.1与legacy DerivationEvidence 0.2 bytes继续immutable。

## 5. live topology必须由Ledger决定

后继不得把“normal”简化成所有children必然present，也不得把所有unknown都解释为negative branch：

- normal consistent、branch-empty与slice-partial：Fact/Relation/Slice均present；
- normal relation-conflict：Fact/Relation present，Slice是`QUALIFIED_UNKNOWN`；DEC-013现有focused witness必须保留；
- 四条negative route：Fact/Relation/Slice均`QUALIFIED_ABSENT`，只交接Source/Policy/Profile/Evidence/Ledger actual files；
- 冻结compatibility fixture中的Fact-present、Relation/Slice qualified-unknown只属于fixture，不得被live producer编造。

Evidence successor需要一个显式、discriminated application-output admission binding，而不能继续假设legacy 0.2的
`relation_admission`必然non-null。exact字段名、版本号与public shape尚未选择；无论如何，CoverageLedger root chain和stage owners仍是
topology authority，Evidence不得反向改写它们。

## 6. one-shot sequence与独立conformance

唯一允许继续审计的sequence是：

```text
committed same-attempt continuity
  -> successor projection claim
  -> copy-owned exact snapshot carrier candidate
  -> independent carrier validation/admission
  -> future Manifest producer consumes admitted carrier exactly once
```

producer与validator不能调用同一个“生成expected document”的projector后再比较，否则两边会共享同一个错误。independent validator至少要从
raw bytes与既有frozen rules复算：JSON canonicality/Schema dispatch、role/path、SHA-256/size/semantic digest、Ledger root topology、
application admission、continuity/attempt binding及one-shot lifecycle。测试只作witness，不授予authority。

## 7. 必须fail closed的反例

任何后继合同若不能机械停止下列情形，本seam即不成立：

1. replay、foreign attempt、已消费continuation或重复Manifest消费；
2. carrier形成前后任一owned bytes mutation；
3. context stop、deadline stop、unsafe、interrupted或incomplete chain；
4. Ledger root与actual file presence不一致；
5. qualified absence被placeholder/empty document冒充，或qualified unknown被折叠为absence/present；
6. relation-conflict被错误归入negative route，或fixture-only topology被伪造为live；
7. producer与validator共享projector/expected bytes，形成common-mode oracle；
8. manifest producer回读mutable path/private internals而不是只消费admitted carrier；
9. legacy 0.2 fallback接受unknown successor，或successor重算/改写legacy identity；
10. Evidence、carrier或Manifest替代stage owner/Core宣布事实充分或Verdict。

## 8. classification与下一合法seam

当前结论是：

```text
classification = BOUNDED_VERSIONED_EVIDENCE_AND_PRIVATE_SNAPSHOT_CARRIER_PRECONTRACT_SEAM
versioned_derivation_evidence_successor_required = true
copy_owned_manifest_carrier_snapshot_required = true
independent_successor_conformance_required = true
manifest_role_or_path_change_required = false
direct_private_continuity_serialization_allowed = false
direct_manifest_runtime_authority = false
```

这不是doc413的反例；它把doc413已经资格化的“carrier seam”拆成claim与snapshot handoff两个不可互换的责任。本文资格化以后，下一次
CONTROL LOOP最多允许选择独立docs-only最小successor contract；不能跳过合同/冻结/feasibility/authorization直接施工runtime。

## 9. retained evidence与setup/proof-facility failures

保留证据根：

```text
C:\Users\lenovo\Desktop\GitHubProjects\tmp\r1-manifest-carrier-precontract-audit-af39730
```

audit source与semantic matrix SHA-256分别为：

```text
0b45349adbd69ae49a9c8ea21cb34b5fc6f0e713fa6c50627d5a0ec42b4c00f6
edf9a0dd79ac2b7f4c4d7b2ce2fb9b1917a7e67f967a0978325747eb1c7173e6
```

下列non-qualifying setup/proof-facility identity全部保留，不被attempt 2 PASS覆盖：

1. managed worktree创建成功但Codex thread attachment identity超过100，侧栏注册失败；
2. audit attempt1错误地把normal semantic clock patch为零，产品正确fail closed为`DERIVATION_ADMISSION_DEADLINE`；
3. positive composition source首次假设了不存在的`_review_slice_coverage_composition.py`，真实文件是
   `_relation_transition_slice_composition.py`；
4. Python interpreter inventory首次使用无效PowerShell `foreach` pipeline；
5. control re-read首次把`HEAD^{tree}`交给PowerShell/git后发生revision argument编码错误；
6. doc413读取脚本首次猜错文件名，真实tracked path由`rg`恢复。

这些错误没有修改产品、合同或candidate repo bytes，qualification effect与semantic effect均为`NONE`。primary
`C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`仍保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 10. candidate scope、资格链与状态上限

本docs-only candidate只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc316、doc397、doc411、doc412、
doc413、private runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle与全部frozen semantic bytes保持base不变。

local gates至少重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、required markers、
legacy Schema/manifest immutable hashes、successor/manifest runtime absence、四格semantic/focused witness、`git diff --check`、read-only
global/local hygiene与primary `audit.json` continuity。随后依次：

```text
final docs-only audit bytes / declared local gates
  -> original audit PR Public CI 15/15
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc316 / doc397 / doc413 / 本文 Public Render
  -> fresh AGENTS / milestones / exact private source-test raw+API+exact-Git byte observations
  -> independent source-byte / five-route / relation-conflict / topology / authority-ceiling / retained-history reconciliation
  -> PRECONTRACT_AUDITED / QUALIFIED_HISTORY
  -> return CONTROL LOOP
```

所有产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用
`http://127.0.0.1:7897`。任何non-success保留原identity并停止；不得重复已有PASS、拼接different worlds或用后继成功覆盖失败。

本文自己的最后门闭合以前，只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_NOT_SELECTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

局部precontract audit不等于完整R1或用户工程问题已经解决：

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
```
