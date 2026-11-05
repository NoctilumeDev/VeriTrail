# R1 public project-state projection failure-chain audit readback rate-exhaustion failure-boundary

日期：2026-11-06

> 候选状态：
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RATE_EXHAUSTION_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@c613129814cec4812066d747e34ebdb40e44fa03`，tree
> `fcce220c39605f316ad917e0457a072675901895`。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只发布PR #410 fresh readback的新失败事实；不修改
> [文档358](358-r1-public-state-projection-failure-chain-audit.md)、workflow、runtime、tests、Schema、Provider、Collector、
> P2 oracle、Core evaluator、Fact/Relation/Coverage semantics、Verdict或任何frozen contract。

## 1. CONTROL LOOP结论

PR #410完成了自己的local、original PR gate、protected merge与new exact-main双门，但fresh installed-product observation是
独立资格层。该层的唯一README formal发生anonymous API rate exhaustion，因此doc358仍是`MERGED / NOT_QUALIFIED`；
不能从此前绿灯继承readback qualification，也不能把同session的Render COMPLETE与API ERROR拼成PASS。

新的最小责任是保存这次failure identity、未运行目标与归因上限。它不授权重跑同一formal，也不授权跳到projection recovery、
runtime、manifest、persistence、public Review或R2–R6。

## 2. #410 exact identity与既有门

```text
candidate base = fa26311fb156d2e07a79ecc76c8d8b5169f64891
candidate head = 9f7e0071178e0c9a9f5e62ac4c745a5d1cc2e47d
candidate tree = fcce220c39605f316ad917e0457a072675901895
original Public CI = 42084370751 / attempt 1 / 11 of 11 SUCCESS
protected merge = c613129814cec4812066d747e34ebdb40e44fa03
exact-main Public CI = 42090149115 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42090149265 / attempt 1 / 1 of 1 SUCCESS
```

这些门只证明doc358 exact world的声明链；它们没有提前证明fresh public presentation。

## 3. Fresh环境与pre-formal observation

fresh detached worktree固定到merge/tree且保持clean。public Core `0.13.0`与GitHub Evidence `0.1.0` immutable wheel
字节仅作输入复用，安装到fresh Python 3.13.13 venv；模块路径、Playwright 1.62.0、matching Chromium、token/source-path
清理与primary audit continuity均已验证。pre-observation adapter freeze与pre-formal validation SHA-256为：

```text
d0b1e9391d4a5cc99d09ce02c735751535d1a8199b2a796b1e37ce83f85b5e61
ec2443bfe49a643067ab3f82405612acea3d0a0451a3ad63ea483080240f3def
```

README与doc358各自fresh Public Render diagnostic均为`COMPLETE / HTTP 200`。它们只确认render路径当时可观察，
`DIAGNOSTIC_ONLY_NON_QUALIFYING`身份不产生formal authority。

formal以前的两个anonymous API观察为：

| observation | time (UTC) | remaining | reset epoch | authority |
| --- | --- | ---: | ---: | --- |
| rate diagnostic #1 | `2026-11-05T19:50:14.272823Z` | 17 | 1793909598 | NON_QUALIFYING / NONE |
| API preflight #1 | `2026-11-05T19:50:21.268204Z` | 16 | 1793909598 | NON_QUALIFYING / NONE |

两者只提供运行前上下文，不预付formal budget，也不拥有qualification。

## 4. 唯一README formal non-success

formal identity为`r1-projection-failure-chain-formal-readme-1-c613129`。在
`collection_session_id=github-paired-9c3f38486a6e478db2802fecd4b60f1e`中，两个观察面得到：

```text
API repository probe = HTTP 403 / COLLECTION_BUDGET_EXHAUSTED
API rate metadata = limit 60 / used 60 / remaining 0 / reset 1793909526
API coverage = ERROR
Render coverage = COMPLETE
Render navigation = HTTP 200 / requested equals final
Render content = marker once / three stable samples
Render cleanup = active streams 0 / cleanup errors 0
Core Verdict = NOT_CREATED
formal classification = FORMAL_READBACK_ERROR
```

formal API probe发生在`2026-11-05T19:50:58.260974Z`，距preflight约43秒。formal返回的reset epoch还与
preflight metadata不同。现有证据只证明：unique formal执行时anonymous API budget为0；它不证明哪一个外部消费者消耗了
额度，也不证明三次请求必然由同一个稳定shared-egress bucket服务。因此底层consumer/egress allocation原因保持`UNKNOWN`。
candidate semantic regression与Collector regression均未建立；Collector按合同fail closed。

## 5. 停止与保留

README unique formal失败后，资格链立即停止：

```text
doc358 formal = NOT_RUN
AGENTS raw/API/exact-Git observation = NOT_RUN
milestones raw/API/exact-Git observation = NOT_RUN
independent success reconciliation = NOT_RUN
successful closeout = NOT_RUN
rerun / retry until PASS = NOT_REQUESTED
```

failure-boundary、62-artifact failed closeout与failure-preservation finite integrity SHA-256为：

```text
0d5cb71ca998418f286fb68607f650387f1b6fa1cee7459dfc65c2bb12996262
2531254a857f1be4bd4c1ee9b44cb1b6fc2fc93c86e7967afd549b4f4f465143
ac8707c94a8248dcea037953e17d387daeace9be7f8cfc98d97b31e8aa04c612
```

proof-facility compile预检第一次把PowerShell未展开的`*.py`传给Python并得到`Errno 22`；该setup error已经以
`f6185df292c609d290fabdddb733f677d652897bd19e645c9d43c799b8b4e7a3`保留，effect为NONE。随后逐文件AST parse
PASS不删除前者。

## 6. 归因上限与状态

```text
#410 original/exact-main gates = PASS
#410 fresh README formal = ERROR / NOT_QUALIFIED
anonymous API exhaustion during formal = ESTABLISHED
same-session Render COMPLETE = ESTABLISHED
Core Verdict = NOT_CREATED
underlying consumer/egress allocation cause = UNKNOWN
doc358 = MERGED / READBACK_NOT_QUALIFIED
failure-chain audit = NOT_QUALIFIED
release multi-asset lane recovery 0.2 = FROZEN
public project-state projection 0.2 = NOT_FROZEN
```

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RATE_EXHAUSTION_FAILURE_BOUNDARY_CANDIDATE_NOT_QUALIFIED
RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本失败与#406的API exhaustion分类相似，但commit、session、formal identity、preflight metadata与publication责任不同；不得将两次
失败合并成同一个attempt，也不得用#409或后继PASS解释二者的`UNKNOWN`。

## 7. 本failure-boundary candidate的资格链

tracked scope只能是：

```text
README.md
AGENTS.md
docs/359-r1-public-state-projection-failure-chain-audit-readback-rate-exhaustion-failure-boundary.md
docs/milestones.md
```

本candidate必须独立完成local gates、original PR required gates、protected exact-head merge、新exact-main Public CI与Browser
Smoke、fresh README/本文 Public Render formal、AGENTS/milestones raw-byte observation、independent reconciliation与finite
closeout。任一non-success继续保留并停止。

全部闭合后只允许形成：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_FAILURE_CHAIN_AUDIT_READBACK_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
```

然后返回CONTROL LOOP，从新的exact main建立独立versioned doc358 readback recovery publication。不得重跑#410 formal、继续
未运行目标后拼接资格、使用认证观察替代匿名读回、弱化marker/API/Render/Core oracle、回填doc358、直接恢复projection/private
implementation，或启动manifest/Evidence/persistence/public Review/R2–R6。
