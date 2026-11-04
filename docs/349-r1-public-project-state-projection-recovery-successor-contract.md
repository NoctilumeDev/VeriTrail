# R1 public project-state projection recovery successor 0.2 contract

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@34de9427d64ba8a3c77ac38eefe146fa8d2e2d77`，tree
> `f6edc136e2bd156409fad553c6453ceee73ccd97`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改 P2 Collector、
> 524288-byte Render oracle、runtime、tests、workflow、Schema、Fact/Relation/Coverage semantics、Verdict 或任何
> frozen contract。

## 1. CONTROL LOOP 输入与 retained failure

[文档346](346-r1-post-terminal-fact-dual-successor-private-implementation-candidate.md)由 PR #398 合入
`main@6a30957429c7b6a815608e8355893deb35873f24`。其 original Public CI `41893051274`、exact-main Public CI
`41898679833` 与 Browser Smoke `41898679711` 均为 attempt 1 SUCCESS；fresh README、doc345、doc346 formal
readback 也各有唯一 PASS。milestones 首次且唯一 diagnostic 则观察到 526260 UTF-8 bytes，超过 frozen
524288-byte Public Render 上限 1972 bytes，正确终结为 `PARTIAL / CONTENT_TRUNCATED`，formal 没有运行。

因此 #398 继续只能是：

```text
MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN
```

failure-boundary 与 failed-readback closeout SHA-256 分别为：

```text
0c3b6aebd225dae14b39cf069dfaf400e1f800b54aff5d15c224c758e5e2cc4d
1b3c3a64bace28e5eab3bb2e6674823ed4f5edaf9adc1c5943b8e90d118a91ff
```

第一次 recovery 使用 doc347 身份。PR #399 精确
`base=6a30957429c7b6a815608e8355893deb35873f24 / head=42df6f6c7f5da44640b47009e942390d55345565 /
tree=1136377bebfd3a9d935024160b84c05377a28300`；original Public CI `41908195831` attempt 1 在 required
Python 3.13 job 中因 fixture `git cat-file` 耗尽剩余 `3.1687451000000237` 秒 acquisition budget 而 FAIL，产品正确
映射 `SAFETY_BUDGET_EXHAUSTED`。该 run 没有 rerun，PR 已关闭且未合并；candidate regression 与 product defect 均未建立，
runner/subprocess stall 的 lower resource cause 保持 `UNKNOWN`。doc347 与其 `docs/project-state.md` bytes 只属于 failed head，
不得继承资格。

独立[文档348](348-r1-public-state-projection-recovery-gate-failure-boundary-audit.md)由 PR #400 以 exact
`base=6a30957429c7b6a815608e8355893deb35873f24 / head=e9d593173aa6ff29ab67d01f595f0ca8d3eb9924 /
tree=f6edc136e2bd156409fad553c6453ceee73ccd97`合入本合同构造坐标。original Public CI `41917042638`、
exact-main Public CI `41921759669` 与 Browser Smoke `41921759657` 均为 attempt 1 SUCCESS。fresh README/doc348
Public Render formal readback与 AGENTS/milestones exact-commit public/API raw-byte observation各有唯一 PASS；raw bytes没有被
冒充为 Render COMPLETE。independent reconciliation、186-artifact closeout、stdout self-capture mismatch 与 finite integrity 为：

```text
fb4dd585026bc0f03ef3a6e9180b1874786f856b864c856dfb3612a140946c17
cc7c6da94ef73715bf39d0291bc62eff08b200a16eb6c4ebb21285767a96bd2f
35fdef9373f6c96f6db4ad225ad2e3e0e6340d90b6872faa6edafbfc7a6af229
d1c660f86636465498300261284de9165bd7eb9eb26a39e977918c5821fd4fe5
```

README formal #1 marker drift ERROR、doc348 diagnostic #1 multiplicity、worktree/bootstrap/PowerShell/public-bytes proof-target
setup errors与全部既有 FAIL/ERROR/UNKNOWN 按原 identity 保留。因此 doc348 现在是
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`，但它不创建 project-state product，也不使 #398/#399 qualified。

## 2. 最小 reopen：有界展示投影，不是事实或裁决权威

current exact base 的 `docs/milestones.md` 继续拥有完整 append-only 工程历史、失败 provenance 与链接索引责任。其 exact bytes
固定为：

```text
source_milestones_bytes = 568856
source_milestones_sha256 = d468191fcfbbaa8df31f592db35e494a8363ddd4f9c1c735dec26ab41a495ccf
source_milestones_blob_sha1 = 18645a09f3a1f11406b4c54f501dd265eb44c072
```

本候选保持这些 bytes 不变。新增[当前项目状态公开投影](project-state.md)只提供 bounded current-state 阅读面；它不是 source of
truth、状态机、roadmap scheduler、qualification record 或施工授权。

权威边界固定为：

| 对象 | 拥有 | 不拥有 |
| --- | --- | --- |
| `docs/milestones.md` | 完整 append-only 历史、链接与 provenance | 必须落入 Public Render 524288-byte window 的义务 |
| `docs/project-state.md` | 当前 exact source world 的有界公开阅读投影 | 历史事实、状态升级、证据充分性或下一步授权 |
| frozen contracts / retained evidence | 各自 exact world 的语义与资格事实 | 被投影重写或压缩后的替代身份 |
| P2 Public Render Collector | frozen cap 内的页面观察与显式 truncation | 提高上限或把 PARTIAL 冒充 COMPLETE |
| exact-commit public/API raw observation | 完整公开文件 bytes 与 digest observation | rendered semantic completeness |
| independent reconciliation | candidate/merge/gates/readback/source binding 一致性 | 创造缺失事实或覆盖 prior failure |

## 3. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2`

successor 0.2 固定以下合同：

1. `docs/project-state.md` 必须小于 65536 UTF-8 bytes，不得嵌入完整 milestones 或把摘要冒充完整历史；
2. 投影必须记录唯一 source exact base/tree、`source_milestones_bytes`、`source_milestones_sha256`、当前有效事实、retained
   failures、停止线与自身候选状态；
3. README/AGENTS 可以把投影作为短入口，但必须继续链接完整 milestones，并明确投影没有事实、qualification 或 scheduler authority；
4. 本候选的 `docs/milestones.md` 必须 byte-for-byte 等于 exact base；
5. 本候选不复用 doc347 或 failed-head project-state bytes；相同结构、措辞或 semantic result 不能继承 failed head 的资格；
6. qualification 时 README、project-state、本文各自先运行 fresh anonymous diagnostic，再运行唯一一次 formal；每项必须
   `COMPLETE / FORMAL_READBACK_PASS`；
7. changed AGENTS 与 unchanged milestones 必须分别通过 anonymous exact-commit raw.githubusercontent + GitHub Contents API
   全字节观察，并与 exact Git bytes、SHA-256、blob SHA-1 对账；raw observation 不等于 Render COMPLETE；
8. independent reconciliation 必须核对 base/head/tree、protected merge、新 exact-main gates、三项唯一 Render PASS、两项唯一 raw
   PASS、projection source binding、doc348 closeout、#398/#399 failure identities与 primary audit continuity；
9. 任一 non-success 保留原身份并停止，不得以另一个 target、world、attempt、same semantic result 或认证访问替代；
10. 每当完整 milestones bytes 或 current effective state 改变，投影必须在独立 publication 中 version/rebind；旧投影只保留其
    exact world 历史，不静默追写；
11. 本合同只 version bump public projection/readback target boundary，不重开 P2、private runtime、frozen upstream 或 public Review。

## 4. tracked scope 与资格链

tracked scope 只能是：

```text
README.md
AGENTS.md
docs/349-r1-public-project-state-projection-recovery-successor-contract.md
docs/project-state.md
```

`docs/milestones.md` 必须保持 exact-base SHA。最终 bytes 必须完成：

```text
exact scope / milestones byte continuity / links / markdown / global+local hygiene
    -> Python 3.10.6 / 3.13.13 × normal / -O focused unchanged-runtime witness
    -> original PR required gates（attempt 1；任一 non-success 保留并停止）
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / project-state / doc349 Public Render
    -> fresh anonymous exact-commit AGENTS / milestones public+API raw-byte observation
    -> independent reconciliation + finite closeout
```

全部成立后，本文最多成为：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_QUALIFIED_CANDIDATE_NOT_FROZEN
```

## 5. 停止线

合同与投影冻结必须由后继独立 docs-only publication 取得自己的完整资格链。在那以前：

- `docs/project-state.md` 只是 candidate，不是当前 frozen qualification target；
- PR #398 继续 `READBACK_NOT_QUALIFIED / NOT_FROZEN`；
- PR #399/doc347 继续失败、关闭、未合并、未资格化；
- 不得建立 private implementation freeze publication；
- 不得恢复 global composition authority；
- 不得启动 manifest、Evidence、persistence、public Review 或 R2–R6。

本文形成任何新事实以后必须返回 CONTROL LOOP。文档编号、短投影和绿色 CI 都不是调度器。
