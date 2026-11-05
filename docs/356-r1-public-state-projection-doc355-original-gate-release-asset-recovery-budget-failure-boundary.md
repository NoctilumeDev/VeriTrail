# R1 public project-state projection doc355 original-gate Release asset recovery-budget failure boundary

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC355_ORIGINAL_GATE_RELEASE_ASSET_RECOVERY_BUDGET_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@95add9053c2984c0efe0cb87d1a4b64812215683`，tree
> `3619ceeba79145ebfe3af230e4ba22c89798c306`。
>
> 受审失败：PR #407 original Public CI attempt 1 的 frozen E1 Release asset HTTP 504 recovery-budget exhaustion。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只冻结失败identity、同run上下文、未开始目标、
> fail-closed归层与后继责任；不修改workflow、runtime、tests、Schema、Provider、Collector、下载恢复工具、P2 oracle、
> Core evaluator、Fact/Relation/Coverage semantics、Verdict、doc355、doc354、doc353、doc350、`docs/project-state.md`
> 或任何frozen contract。

## 1. CONTROL LOOP输入：#406不被回填，#407形成独立失败world

[文档354](354-r1-public-state-projection-doc353-readback-marker-drift-failure-boundary.md)由PR #406以exact：

```text
base = 6af0dac952ec2bd3e015bc827b2b709908282036
head = a5dd28fa8b24b5517a09e5be9733e7e479658746
tree = 3619ceeba79145ebfe3af230e4ba22c89798c306
original Public CI = 42003156856 / attempt 1 / 11 of 11 SUCCESS
exact-main Public CI = 42007684666 / attempt 1 / 11 of 11 SUCCESS
Browser Smoke = 42007684466 / attempt 1 / 1 of 1 SUCCESS
protected merge = 95add9053c2984c0efe0cb87d1a4b64812215683
```

进入main。fresh README formal的API anonymous 403 `COLLECTION_BUDGET_EXHAUSTED`与Render COMPLETE发生在同一
collection session，但不能拼成PASS；Core Verdict未创建，doc354继续是`MERGED / EXACT_MAIN_DUAL_GATES_PASS /
READBACK_NOT_QUALIFIED / NOT_FROZEN`。#407的后继失败不回填该identity，也不解释其shared-egress rate cause `UNKNOWN`。

doc355 audit candidate从未改变的exact main独立构造：

```text
base = 95add9053c2984c0efe0cb87d1a4b64812215683
head = ade665c3b4e760a57c2d2de4fb1c92fcd21d1b98
candidate tree = 66dad764b58927a29e0d7e3aeafb6f237f165510
commit count = 1
scope = README.md
        AGENTS.md
        docs/355-r1-public-state-projection-doc354-readback-anonymous-rate-exhaustion-failure-boundary.md
        docs/milestones.md
```

local qualification、pre-PR evidence seal与post-commit evidence seal均成立：

```text
local qualification = 40647f5df425eecdeeafdbc2c8b1d585e8fde3704cac6095092c69108faf7f28
pre-PR evidence seal = 63b079f0ace129d3592d1e068624b75a2361601aa1e6af38773bba14d7de1475
post-commit evidence seal = 2b8b13b1c11841ec46792960217c5a4e2905c202da8d2515e1b203c4e1e45fb4
```

pre-PR staged-diff review发现doc355多一个EOF空行；它在formal local qualification之前被修复，旧工作字节、旧资格输出与
finding identity全部保留。最终字节重新跑完整local matrix并形成上述三个seal。该prequalification finding不等于产品失败。

## 2. original Public CI真实失败

PR #407 original Public CI只有一个attempt，禁止rerun：

```text
run = 42037283423
attempt = 1
run conclusion = FAILURE
required failing job = 127278597232 / Python 3.10 on Windows
job started = 2026-11-05T13:36:40Z
job completed = 2026-11-05T14:08:56Z
failed step = 31 / Download the frozen E1 entry-layer release assets
failed step interval = 2026-11-05T14:07:04Z .. 2026-11-05T14:08:51Z
```

该job的steps 1–30全部SUCCESS，包括Core normal/`-O`、Authoring normal/`-O`、GitHub Evidence normal/`-O`、
Review Attention normal/`-O`、Starter/Skill、wheel/sdist/plugin build与frozen Core wheel下载。step 31中：

```text
preceding assets successful = 5
failed asset position = 6
failed asset = authoring-skill-e1-validation-summary.json
initial status = HTTP 504
retry attempts observed = 5
recovery budget = 60 seconds
terminal reason = release asset recovery budget cannot fund the next bounded retry
                  after retryable_http status=504
following assets not attempted = 1
E1 clean install = SKIPPED
```

下载工具在既有绝对deadline与窄重试集合内停止，没有覆盖partial或摘要校验结果；其fail-closed行为符合冻结边界。

## 3. 同run上下文不是可拼接资格

同一run的八个job结论为：

```text
SUCCESS = Python 3.13 on Windows
          E3 0.2 release download acceptance
          Workbench tests, lint, build, and audit
FAILURE = Python 3.10 on Windows
SKIPPED = Wheel-only first run on Python matrix
          GitHub Evidence wheel-only on Python matrix
          Starter PASS/FAIL golden path
          Acceptance Core freeze on Python matrix
```

Python 3.13成功最多说明另一个runner/job在自己的window完成；它不能替代Python 3.10 required job，也不能与E3、Workbench或
此前local PASS拼成11/11。四个downstream required jobs因依赖失败而SKIPPED，保持原结论。

## 4. 失败归层与归因上限

当前证据只允许：

```text
original PR gate = FAILURE / NOT_QUALIFIED
classification = RELEASE_ASSET_HTTP_504_RECOVERY_BUDGET_EXHAUSTED
download-tool fail-closed behavior = CONFORMING
candidate workflow/runtime/tests/oracle changes = false
candidate semantic regression = NOT_ESTABLISHED
candidate docs content failure = NOT_ESTABLISHED
underlying GitHub/proxy/shared-egress/network cause = UNKNOWN
rerun = NOT_REQUESTED
```

HTTP 504与固定60秒预算耗尽都是真实事实；但当前证据不支持从GitHub、代理、共享出口、runner网络、资产本身或瞬时外部状态中
选一个作为单一根因。不能用同run Python 3.13成功把它改名为偶发噪声，也不能直接把一次预算耗尽解释为预算必然过小。

raw capture、完整job log、failed-step log、run logs zip与failure-boundary SHA-256为：

```text
3b376279543da71acf14e4bec364dc5215b764d0d727927ed6d5637d5c4a7a76
09707a4184e2d8133983b53344b8d236c846936bf77fd22833a7fd15138cf472
3536d47d20934f0dbc2fb13163abcb9a4605bc01b28845be6a91789f766e101a
fcb2368a58c6787499aebc929df3958edb24024ddf7e27290b141c6ed93aaa86
48c43a66843c6fdf010650b186c6b82e3773a79fe641e2b59cbb2aaf3cf3323e
```

run仍可下载时保存的八个Artifact seal为
`d17fbf95321ec695fc12dd0e546fbcbe4ccd4d69a060c590f2a55376a04bf39c`；它包含双Python Core wheel/sdist、
双Python GitHub Evidence wheel与双Python P3 probe，不把这些成功产物升级为整run资格。

## 5. PR关闭、未开始目标与失败closeout

PR #407未rerun，已关闭且未合并：

```text
PR state = CLOSED
merged = false
closed PR raw SHA-256 = 54fe100840144d4c4068c86099b204b8a29f2a0688d57fce02a8acc96126d63e
close capture SHA-256 = 47a8209574ed74171b7a507d656a64a8a3c980349576facbebf9a66719ab69ce
remote main = 95add9053c2984c0efe0cb87d1a4b64812215683
new exact-main gates = NOT_STARTED / NOT_AUTHORIZED
fresh installed-product readback = NOT_STARTED / NOT_AUTHORIZED
```

123-artifact failed-candidate closeout与finite integrity分别为：

```text
c01e86ea670dc0a2d0de9bdfb1c7d2145fe8c0185c7590f595d6198baa7ef896
b010e77087f24330a168e48023b3708005bd163503bdb29d701ef8696bb5607c
```

PowerShell rev-parse braces、`rg` Windows glob、monitor yield/parser、local watch cancellation、wrong closeout template name等setup
failure均按原identity保留，semantic effect为`NONE`。它们不覆盖original gate product failure，也不被本审计删除。

## 6. retained history不被回填

- PR #402/doc350仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #403/doc351仍是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；
- PR #404/doc352仍是`CANCELLED / CLOSED / UNMERGED / NOT_QUALIFIED`，duration variance仍为`UNKNOWN`；
- PR #405/doc353仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #406/doc354仍是`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #407/doc355是`FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED`；
- projection 0.2、private implementation与global composition authority均没有因此冻结或恢复；manifest、Evidence、persistence、
  public Review与R2–R6仍未授权。

## 7. 禁止的伪恢复

```text
rerun #407或retry until PASS
增加Release下载恢复预算后冒充同一候选已通过
把Python 3.13、E3、Workbench、local PASS或下载Artifacts拼成original gate PASS
把HTTP 504猜成GitHub、代理、shared egress、runner网络或资产的已知单一根因
删除失败run/log/Artifact/setup failure或把SKIPPED改名为NOT_APPLICABLE
复用doc355 candidate bytes而不从新的exact main重新取得资格
从本审计直接冻结doc354/doc355、恢复projection或启动后续runtime seam
```

## 8. 本审计的最小职责与公开观察面

tracked scope只能是：

```text
README.md
AGENTS.md
docs/356-r1-public-state-projection-doc355-original-gate-release-asset-recovery-budget-failure-boundary.md
docs/milestones.md
```

本文自己的合入后observation必须机械区分：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal；sealed literal是reader-visible的`PR #407 的原始门下载恢复预算失败已按原身份保留` |
| 本文 | anonymous P2 Public Render diagnostic + unique formal |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整bytes与digest |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation；raw bytes不冒充Render COMPLETE |

independent reconciliation必须核对base/head/tree、四文件scope、#405/#406/#407 retained failures、#407 original run/job/step、
全部setup identity、raw capture/log/Artifact/failure-boundary/PR-close/failed-closeout/finite-integrity、doc351 qualified history、
primary audit continuity与四个fresh observations。

## 9. 本审计自己的资格链

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、`git diff --check`、
global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O` focused unchanged-runtime witness。

```text
final docs-only bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per section 8
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC355_ORIGINAL_GATE_RELEASE_ASSET_RECOVERY_BUDGET_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一non-success都保留原identity并停止。全部门闭合后本文也只成为qualified history；它不使doc355、doc354、doc350、
projection 0.2或private implementation qualified/frozen。

## 10. 当前状态与后继停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_PR_404_CANCELLED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_RECOVERY_ORIGINAL_GATE_CANCELLATION_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC353_READBACK_MARKER_DRIFT_FAILURE_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC354_READBACK_ANONYMOUS_RATE_EXHAUSTION_FAILURE_BOUNDARY_AUDIT_PR_407_FAILED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC355_ORIGINAL_GATE_RELEASE_ASSET_RECOVERY_BUDGET_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文形成新事实后必须返回CONTROL LOOP。只有从新的exact main重建证据后，才能判断Release下载恢复maintenance是否仍是最小
合法seam；不得从单次HTTP 504直接增加60秒预算、复用#407 attempt、重新推送doc355或启动manifest/Evidence/persistence/
public Review/R2–R6。
