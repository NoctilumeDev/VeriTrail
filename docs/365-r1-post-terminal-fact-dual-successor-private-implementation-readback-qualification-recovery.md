# R1 post-terminal Fact dual-successor 私有实现读回资格恢复 0.1

日期：2026-11-06

> 候选状态：
> `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_READBACK_QUALIFICATION_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@e0ab9d0679f1706cdde3103ef0e1076baa681b59`，tree
> `9dbd55b4180eee32abd9cee3fd2533763008e962`。
>
> 条件化目标：本文自己的全部资格门闭合后，PR #398 / doc346 最多升级为
> `IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。
>
> 影响：`L0_DOCUMENTATION / READBACK_TARGET_QUALIFICATION_RECOVERY_ONLY`。本文不修改private runtime、tests、workflow、
> Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、projection 0.3 semantic bytes或任何
> frozen contract。

## 1. CONTROL LOOP 输入：实现本身未漂移，旧读回仍不资格化

[私有实现候选](346-r1-post-terminal-fact-dual-successor-private-implementation-candidate.md)由PR #398以exact
`base=aa0cd335a98269dcdb843645f9643c0e7982a5c8 / head=c1952d76f82808d2c9c7ccca719d32db20364000 /
tree=81790b398fb3d07ed53d67269b80d99d94675807`进入受保护主线，普通merge为
`6a30957429c7b6a815608e8355893deb35873f24`。original Public CI `41893051274`、exact-main Public CI
`41898679833`与Browser Smoke `41898679711`均为attempt 1 SUCCESS（11/11、11/11、1/1）。

fresh README、doc345、doc346 formal各取得唯一PASS；milestones diagnostic观察到526260 UTF-8 bytes，超过frozen
524288-byte Public Render上限1972 bytes，正确终结为`PARTIAL / CONTENT_TRUNCATED`，formal没有运行。failure-boundary与
failed-readback closeout SHA-256继续固定为：

```text
0c3b6aebd225dae14b39cf069dfaf400e1f800b54aff5d15c224c758e5e2cc4d
1b3c3a64bace28e5eab3bb2e6674823ed4f5edaf9adc1c5943b8e90d118a91ff
```

因此旧world始终是：

```text
MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN
```

不得重跑milestones diagnostic、事后运行其formal、提高P2上限，或把三个旧PASS与新的target拼接成资格。

## 2. projection 0.3 已冻结，但不自动回填 #398

[projection 0.3 contract](363-r1-public-project-state-projection-recovery-successor-0.3-contract.md)与
[freeze publication](364-r1-public-project-state-projection-0.3-freeze-publication.md)已经完成独立链。PR #416精确
`base=e5af3a0eecf8ef5b3a439bfe7f5948610c3834e6 / head=af353d0dff3823f3b82594658a8869a2b91d3172 /
tree=9dbd55b4180eee32abd9cee3fd2533763008e962`合入本构造坐标。original Public CI `42170247609`、exact-main
Public CI `42173888920`与Browser Smoke `42173888925`均为attempt 1 SUCCESS。

第四个fresh root中的README、project-state、doc363、doc364各有唯一formal PASS；AGENTS/milestones raw、API与exact Git
逐字节一致。独立reconciliation、136-artifact closeout、stdout self-capture mismatch与finite integrity为：

```text
caa8a5d564007fd011cfa3fbe050129dfc50062dae38ca1247aac90f14dcda40
f702c537777d8867906b374bcb583065e22539be3dbff755054dc61e66bea6a3
ab21a304dacd4f41267907ccfefb5301bc5919b34cffedf36073835ddb8c4537
8790db05d542f01399aacaab0703c795ccbde7acb936117bcea561ae22b2355f
```

前三个fresh root中的两次anonymous API exhaustion与一次Public Render network error，以及全部Plan-ID、PowerShell、bootstrap和
proof-facility setup error继续保留。后继PASS不解释其`UNKNOWN`。因此
`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN`与
`R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_FROZEN`已经生效，但它们只提供有界reader target；不会
自动改写#398的readback资格。

## 3. exact implementation 与上游语义连续性

从#398 merge到本构造坐标，`plugins/review-attention`没有tracked diff。五个implementation/test blob逐字节保持：

| path | blob SHA-1 |
| --- | --- |
| `_fact_fulfillment.py` | `cb8e25c7a2a93fac6f038c52cc62ac8019c6c2fe` |
| `_fact_relation_transition.py` | `57e672eeadb6741cc43f5478026bb76a98cd3aca` |
| `_fact_to_coverage_exact_input_handoff.py` | `241bc177247d4343e59001cef461710e3d61d475` |
| `_post_terminal_fact_dual_successor.py` | `68cbb622dbc9d33d0c88e6954f9db77ee16438ce` |
| `test_post_terminal_fact_dual_successor.py` | `3778f3c1c9b7bcbe8852ff0b5f35f0c615467215` |

doc340、doc341、doc342、doc345与doc346也与#398 merge world保持相同blob。该连续性只证明当前main仍承载同一实现候选，不能替代
fresh product observation或把测试升级为authority。

## 4. 最小恢复边界：只version readback target

旧doc346把无界`docs/milestones.md`预注册为formal Render target。该目标已被真实容量反例击穿；frozen projection 0.3现在提供
小于65536 bytes、明确不拥有事实/qualification/scheduler authority的有界读者投影。0.1 recovery只把本次资格义务版本化为：

| target | fresh obligation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal |
| `docs/project-state.md` | anonymous Public Render diagnostic + unique formal；作为milestones Render的有界替代，不替代完整历史 |
| doc345 | anonymous Public Render diagnostic + unique formal；复核authorization语义仍公开可见 |
| doc346 | anonymous Public Render diagnostic + unique formal；复核implementation candidate语义仍公开可见 |
| doc364 | anonymous Public Render diagnostic + unique formal；复核projection freeze publication公开可见 |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致；raw bytes不冒充Render COMPLETE |

每个formal都必须使用新的Plan/session/Evidence；不得复用#398、#415或#416 PASS。产品调用必须清除GitHub token、`NO_PROXY`、
`PYTHONPATH`与`PYTHONHOME`，代理只按命令注入。任何non-success按原identity保留并停止。

## 5. 本candidate自己的资格链

tracked scope只能是：

```text
README.md
AGENTS.md
docs/365-r1-post-terminal-fact-dual-successor-private-implementation-readback-qualification-recovery.md
docs/milestones.md
```

local qualification必须重核exact scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
`git diff --check`、global/local hygiene、primary audit continuity、五个implementation/test blob与五个upstream semantic doc blob continuity，
并在Python 3.10.6/3.13.13 × normal/`-O`下运行focused unchanged-runtime witness。

```text
final docs-only bytes + declared local gates
  -> original PR required gates (attempt 1; no rerun laundering)
  -> protected exact-head merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh six-target anonymous formal readback + two raw-byte observations
  -> independent reconciliation + finite closeout
  -> #398/doc346 becomes IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
  -> return CONTROL LOOP
```

independent reconciliation必须同时绑定本candidate base/head/tree、#398 original/exact-main gate identity、旧milestones truncation failure、
#399 original gate failure、#416 projection freeze closeout、implementation/upstream blob continuity、全部fresh observation与primary audit hash。

## 6. 停止线与后继责任

在本文自己的完整资格链闭合以前只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_READBACK_QUALIFICATION_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门成立后也只恢复`READBACK_QUALIFIED / NOT_FROZEN`。该新有效事实会使projection 0.3成为历史投影；下一CONTROL LOOP必须先
version/rebind当前project-state projection，再独立判断implementation freeze publication是否仍是最小seam。不得从本文直接冻结实现、
恢复global composition authority，或启动manifest、Evidence、persistence、public Review、R2–R6。
