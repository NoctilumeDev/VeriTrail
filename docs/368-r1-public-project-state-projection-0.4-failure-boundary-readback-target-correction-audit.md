# R1 public project-state projection 0.4 failure-boundary readback-target correction audit

状态：`AUDIT_CANDIDATE / NOT_QUALIFIED / QUALIFICATION_EFFECT_NONE`

构造坐标：`main@03060eef4f6579c1d187ab2cad9806d2133cfeee`，tree
`962ad5312c92c80e3558f36965b290b1ab664d71`。

> 受审对象：[文档367](367-r1-public-project-state-projection-0.4-exact-main-qualification-failure-boundary-audit.md)
> 自身的 fresh readback target failure，以及它继续承载的 PR #418 exact-main gate failure。
>
> 影响：`L3_QUALIFICATION_BOUNDARY + L0_DOCUMENTATION`。本文只保存两条失败链、证明哪一条 target seam
> 被击穿，并恢复正确的 readback 责任划分；不修改 runtime、tests、fixtures、workflow、Schema、Provider、
> Collector、P2/Core oracle、Verdict、doc366、`docs/project-state.md` 或任何 frozen semantic bytes。

## 1. CONTROL LOOP 输入：#419 双门通过，但自己的 readback 未资格化

文档367候选由 PR #419 以 exact identity：

```text
base = abf06ecfbd01852c202096a7733165f6cb0f0f70
head = f49637a7407953111a89a2290883bab2d51d187d
tree = 962ad5312c92c80e3558f36965b290b1ab664d71
scope = README.md
        AGENTS.md
        docs/367-r1-public-project-state-projection-0.4-exact-main-qualification-failure-boundary-audit.md
        docs/milestones.md
```

进入 original Public CI `42219624414` attempt 1，结果为 11/11 SUCCESS。protected exact-head merge 形成
`main@03060eef4f6579c1d187ab2cad9806d2133cfeee`；该 exact main 的 Public CI `42223794241` attempt 1
为 11/11 SUCCESS，Browser Smoke `42223794592` attempt 1 为 1/1 SUCCESS。没有重跑 PR #418 的失败 run。

这三个门只证明 doc367 candidate 在自己的 original 与 exact-main gate 上完成；它们不能替代 fresh installed-product
readback，也不能回填 PR #418。

## 2. 两个 fresh readback world 必须分别保留

第一个 fresh root 的 README diagnostic 为 `COMPLETE / 200`。README formal 的 API 与 Render 也都完成，但 sealed
marker 在 Markdown source 中包含反引号，GitHub rendered text 正确去除了这些定界符，于是产品以
`Render Evidence marker drifted` fail closed，Core Verdict 未创建。该 world 的 adapter freeze、formal history 与
formal stderr SHA-256 分别为：

```text
fa51e956fbe7dbc8b8419c73cc1c62b24491b1910da1678ccf454dab3c6f0cd0
6d0d19f13103909568975cc2c5322f1ce6bc420087199672b8ebedb9f3fb3e0a
d1e7eea4d8a6210f2c59d9eeeb49890aa2c0ab3c48b8a2c97c03a6d03cd98db3
```

它是 `PROOF_TARGET_SELECTION_ERROR / NON_QUALIFYING / NONE`，不是 subject、candidate 或 Collector regression。

第二个 fresh root 从同一 exact main 重建，并把 README proof target version 为 reader-visible plain phrase。pre-observation
adapter freeze SHA-256 为：

```text
c140c482e382bff3a39084c4b3f75db8bd63f214eac4450f416f8ca7517769c7
```

README 与 doc367 各取得唯一 `FORMAL_READBACK_PASS`，不能重复，也不能与第一个 world 拼接。随后 milestones 的唯一
diagnostic 观察到：

```text
top_level_http_status = 200
literal_marker_occurrences = 1
rendered_text_limit_utf8_bytes = 524288
observed_rendered_text_utf8_bytes = 571604
overage_utf8_bytes = 47316
coverage = PARTIAL
coverage_reason = CONTENT_TRUNCATED
formal milestones readback = NOT_RUN
```

Collector 正确保留三样本稳定的 marker、明确 truncation，并按 frozen P2 合同把 coverage 终结为 `PARTIAL`。这不是
网络、Subject 或 Collector failure；底层原因是已知固定的 512 KiB rendered-text bound。

failure-boundary、118-artifact failed closeout 与 finite integrity SHA-256 为：

```text
89dd99142889d40e753a0edb9950f737ceb22544a3a40eaf0afb543d29160b5c
c328b73d09fd1cd5b070abb4e1533517a516dec1426ebd2e006f151cc36b133d
9bffbf6c77443a710ed900be392e4975d598f2e42bc840accf0e1db4f2e8efee
```

因此 doc367 当前只能是：

```text
MERGED / ORIGINAL_GATE_PASS / EXACT_MAIN_DUAL_GATES_PASS /
READBACK_NOT_QUALIFIED / NOT_QUALIFIED_HISTORY
```

README/doc367 的两个 PASS 继续保留，但不能与 milestones `PARTIAL` 拼成三目标 PASS。

## 3. 被击穿的是 doc367 的 target seam，不是 P2 oracle

这个反例不是新的未知容量问题。冻结边界此前已经明确：

- [projection recovery successor contract](349-r1-public-project-state-projection-recovery-successor-contract.md)
  固定 milestones 只承担完整 append-only 历史，不承担落入 524288-byte Render window 的义务；
- [private implementation readback qualification recovery](365-r1-post-terminal-fact-dual-successor-private-implementation-readback-qualification-recovery.md)
  使用 bounded `docs/project-state.md` 承担读者 Render target，并继续以 raw/API/Git 对账完整 milestones bytes；
- #398 的 milestones `PARTIAL / CONTENT_TRUNCATED` 及其 formal `NOT_RUN` 永久保留，后继 PASS 不回填。

文档367 §7 却重新预注册了：

```text
fresh anonymous installed-product README / doc367 / milestones readback
```

因此直接分类为：

```text
P2 Collector conformance                         = ESTABLISHED
milestones reader-visible marker                 = ESTABLISHED
doc367 readback-target boundary regression       = ESTABLISHED
subject / runtime / Collector regression          = NOT_ESTABLISHED
doc367 exact-main readback qualification          = FAILED
```

## 4. PR #418 failure identity继续不变

PR #418 candidate `bdf5c170817b3b79c4e597d93c76229f36516463`、tree
`e2c98f48cc0071bd1aa85d8134e155ee55fb3e45` 合入 `main@abf06ecfbd01852c202096a7733165f6cb0f0f70` 后，
exact-main Public CI `42211661846` attempt 1 在 required Python 3.10 test
`test_staging_failure_creates_public_error_bundle_after_reverse_cleanup` 真实失败且没有 rerun。产品已观察到
`EVIDENCE_STAGING_FAILED`、`EVIDENCE_ERROR / ERROR` 与 cleanup complete；public verdict 为 `FAIL` 而不是 test 预期的
`PENDING`。failed output 没有保留 decisive assertion 或临时 Bundle，所以 exact assertion 是
`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，lower cause 仍为 `UNKNOWN`。

该 failure evidence seal 与 finite integrity 继续固定为：

```text
ced9138ea87e4bd1c3f06b46bb67cb87a99f4ac957a9a7faae3279919ff3eabc
c663feeac7036c636fe7c2023413584fe9af61dc0a0aadfddec3daae894ed8f7
```

doc367 readback failure不能解释或回填这条 exact-main gate failure；反过来，PR #418 failure也不能把已知 milestones
target regression改写成未知 runtime 原因。

## 5. 禁止的伪恢复

```text
rerun or retry PR #418 exact-main Public CI 42211661846
rerun milestones diagnostic or run its formal readback after PARTIAL
raise, bypass or rename the frozen 524288-byte P2 limit
reuse README/doc367 PASS in this candidate's qualification
use raw bytes to claim Render COMPLETE
silently rewrite doc367 as qualified history
merge the two failed readback worlds or delete either one
modify doc366, project-state, runtime, tests, fixtures, workflow or oracle
start projection successor, maintenance, manifest, Evidence, persistence, public Review or R2-R6 from this candidate
```

## 6. 本 audit candidate 的精确 scope 与正确 readback 责任

tracked scope 只能是：

```text
README.md
AGENTS.md
docs/368-r1-public-project-state-projection-0.4-failure-boundary-readback-target-correction-audit.md
docs/milestones.md
```

doc366、doc367、`docs/project-state.md`、runtime、tests、fixtures、workflows、Schema、Provider、Collector、P2/Core
oracle、Verdict 与 frozen semantic bytes 必须保持 `03060eef…` base bytes。

本 candidate 不再对已知超过 frozen Render window 的 milestones 预注册 formal。它自己的 fresh observation 机械分为：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal readback |
| 本文 | anonymous P2 Public Render diagnostic + unique formal readback |
| `AGENTS.md` | anonymous exact-commit raw.githubusercontent + GitHub Contents API + exact Git 全字节对账 |
| `docs/milestones.md` | anonymous exact-commit raw/API/Git 全字节对账；继续保留既有 Render `PARTIAL`，不冒充 COMPLETE |

## 7. 资格链与生效上限

```text
final docs-only bytes / exact four-file scope / local gates
    -> original PR required gates (attempt 1; any non-success retained and stop)
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh README / doc368 unique formal readbacks
    -> fresh AGENTS / milestones exact-commit public+API+Git raw observations
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_0_4_DUAL_FAILURE_BOUNDARY_READBACK_TARGET_CORRECTION_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合后，本文最多把 PR #418 exact-main gate failure与 PR #419 readback-target failure形成一份 qualified dual-chain
history。它不使 doc366、doc367、projection 0.4 或 PR #418 qualified，也不自动选择 projection successor 或 test/runtime
maintenance。publication 形成新事实后必须返回 CONTROL LOOP，从新的 exact main 重新审计下一最小 seam。

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_MERGED_EXACT_MAIN_PUBLIC_CI_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_EXACT_MAIN_QUALIFICATION_FAILURE_BOUNDARY_AUDIT_MERGED_READBACK_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_0_4_DUAL_FAILURE_BOUNDARY_READBACK_TARGET_CORRECTION_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```
