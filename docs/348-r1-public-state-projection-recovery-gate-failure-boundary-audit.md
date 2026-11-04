# R1 public project-state projection recovery gate failure-boundary audit

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@6a30957429c7b6a815608e8355893deb35873f24`，tree
> `81790b398fb3d07ed53d67269b80d99d94675807`。
>
> 受审对象：PR #398 合入后的 milestones public-render truncation 与 PR #399 original required Public CI
> failure 两条独立失败链。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_BOUNDARY`。本文只冻结失败身份、资格影响、公开投影容量边界与后继
> 恢复责任；不修改 runtime、tests、workflow、Schema、Provider、Collector、P2 512 KiB oracle、Fact/Relation/Coverage
> semantics 或任何 public product surface。

## 1. CONTROL LOOP 输入：#398 merged world 没有取得 readback qualification

[文档346](346-r1-post-terminal-fact-dual-successor-private-implementation-candidate.md)的implementation candidate以
exact base `aa0cd335a98269dcdb843645f9643c0e7982a5c8`、head
`c1952d76f82808d2c9c7ccca719d32db20364000`、tree
`81790b398fb3d07ed53d67269b80d99d94675807`进入PR #398；scope为README、AGENTS、doc346、milestones、
四个private relation modules与一个private test module。original Public CI `41893051274` attempt 1为11/11 SUCCESS，
protected merge形成current exact main：

```text
merge = 6a30957429c7b6a815608e8355893deb35873f24
tree = 81790b398fb3d07ed53d67269b80d99d94675807
parents = aa0cd335a98269dcdb843645f9643c0e7982a5c8
          c1952d76f82808d2c9c7ccca719d32db20364000
```

new exact-main Public CI `41898679833` attempt 1为11/11 SUCCESS，Browser Smoke `41898679711` attempt 1为
1/1 SUCCESS。fresh anonymous installed-product README、doc345与doc346 formal readback各有唯一PASS；milestones
diagnostic则观察到526260 UTF-8 bytes，而frozen P2 Public Render硬上限为524288 bytes，超出1972 bytes，故正确终结为：

```text
coverage = PARTIAL
coverage_reason = CONTENT_TRUNCATED
formal milestones readback = NOT_RUN
implementation candidate readback qualification = FAILED / NOT_QUALIFIED
```

failure-boundary record SHA-256为
`0c3b6aebd225dae14b39cf069dfaf400e1f800b54aff5d15c224c758e5e2cc4d`；failed-readback finite closeout
SHA-256为`1b3c3a64bace28e5eab3bb2e6674823ed4f5edaf9adc1c5943b8e90d118a91ff`。因此#398当前只能是：

```text
MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN
```

README/doc345/doc346的三个PASS继续保留，但不能与PARTIAL milestones拼成四目标PASS。该事实击穿的是public project-state
projection/readback target boundary，不是P2 truncation oracle；不得提高上限、把PARTIAL改名为COMPLETE、运行正式milestones
readback或把已通过目标重复执行到另一个world。

## 2. #399 failed candidate 的 exact identity

fresh CONTROL LOOP随后建立docs-only public project-state projection recovery candidate。它没有修改原milestones bytes，而尝试以
bounded public state projection解除未来公开读回对无界历史索引的依赖。PR #399精确身份为：

```text
base = 6a30957429c7b6a815608e8355893deb35873f24
head = 42df6f6c7f5da44640b47009e942390d55345565
tree = 1136377bebfd3a9d935024160b84c05377a28300
commit count = 1
scope = README.md
        AGENTS.md
        docs/347-r1-public-project-state-projection-recovery-contract.md
        docs/project-state.md
```

original Public CI `41908195831` attempt 1真实结束为FAILURE。required Python 3.13 job `126848392933`在
`Run Review Attention contract tests`步骤运行
`test_derivation_input_binding.DerivationInputBindingContractMatrixTests.test_row_20_public_result_is_independent_of_assert_optimization`
时，materialize tiny fixture SourceSnapshot所需的：

```text
git cat-file -t 79c53955ef856f16f2107446bc721c8879a1bd2e
```

在剩余固定30秒acquisition budget中的`3.1687451000000237`秒超时；`subprocess.TimeoutExpired`被产品映射为
`SourceSnapshotError: SAFETY_BUDGET_EXHAUSTED`。suite以
`Ran 621 tests in 520.445s / FAILED (errors=1, skipped=3)`终结。run没有rerun；PR #399已关闭且未合并，remote
main保持`6a309574…`。

原始Python 3.13 job log SHA-256为
`789ab4717ff1b200822dfd6efc55439fbf46df6b5973bb2f83127781f5a592ee`；同run Python 3.10 job log
SHA-256为`ecc6b5029a0b6f0911920d6840f7da4d2408456c400dd0474ed928e4fd4deb03`；terminal run record
SHA-256为`6ee1e008b3f96c3ec53236386094d1b463b4848731ca33db794ea327bdbd5309`。failure-boundary record
SHA-256为`fd7131e454301589e521c7078ac92f63fdb9dbcaa10af6c15ceb0c5af6ccca5e`；44-artifact closeout与
finite integrity分别为：

```text
4b4dcd0dd01cc09c244e7ded476bf77978a3569bd06129f428a394bb6b7ef20c
c28e9c631e80cfd97cbe0de2d909acc8ad787708f517f344d135fe9afd0374b4
```

## 3. 失败归层：gate failure成立，candidate regression与product defect未建立

#399只改四个docs文件，required Review Attention runtime、tests、workflow、30秒总acquisition budget和
`SAFETY_BUDGET_EXHAUSTED`映射均与exact base相同。失败attempt中的产品按冻结规则fail closed。只能成立：

```text
PR #399 original required gate failure = TRUE
product fail-closed behavior = CONFORMING
runner/subprocess stall = OBSERVED
exact lower-level resource cause = UNKNOWN
candidate regression = NOT_ESTABLISHED
product defect = NOT_ESTABLISHED
```

同一run的Python 3.10 normal/`-O` Review Attention steps成功；更早的exact-base Public CI `41898679833` attempt 1
也在相同runtime bytes上完成Python 3.13 normal/`-O`。这些只是不拼接world的failure-boundary context：它们不能替代#399
Python 3.13 failed job，也不能给#399取得资格或解释本次stall根因。

#399 head上的doc347与`docs/project-state.md`只属于失败、关闭、未合并的candidate。相同文字、摘要或投影结构不能脱离该
exact head继承资格；main不得复用doc347编号冒充它已经通过。后继若仍有合法public projection seam，必须从本审计闭合后的新
exact main建立独立、versioned candidate。

## 4. 两条失败链不能相互覆盖

必须同时保存：

```text
#398 exact-main gate result
    = PASS
#398 installed-product readback result
    = NOT_QUALIFIED because milestones Public Render is PARTIAL / CONTENT_TRUNCATED

#399 original PR gate result
    = FAIL because required Python 3.13 hit SAFETY_BUDGET_EXHAUSTED
#399 merge/exact-main/readback
    = NOT_STARTED / NOT_AUTHORIZED
```

#399 failed gate不能反向解释#398 milestones容量边界；#398 exact-main绿灯也不能替代#399 original gate。P2 collector正确保留
truncation，SourceSnapshot正确保留budget exhaustion；任何后继PASS都不能把这两个原始non-success改写成从未发生。

## 5. 禁止的伪恢复

以下动作都不能产生public project-state projection recovery资格：

```text
rerun Public CI 41908195831 或 retry until PASS
reopen / merge PR #399
复用 doc347 或 failed-head docs/project-state.md 作为 qualified bytes
用 same-run Python 3.10 PASS 拼接 failed Python 3.13 world
用 prior exact-base Public CI 41898679833 回填 #399
提高或绕过 frozen 524288-byte Public Render上限
把 milestones PARTIAL 改名为 COMPLETE 或事后运行其formal readback
把 runner/subprocess stall 猜测成单一host、Git、磁盘、进程或产品根因
用本failure-boundary audit本身授权implementation freeze、manifest、Evidence或public Review
```

## 6. 本审计的最小职责与公开观察面

本文只把两条已发生失败放入同一不可混淆的项目状态记录，并冻结后继恢复责任。tracked scope只允许：

```text
README.md
AGENTS.md
docs/348-r1-public-state-projection-recovery-gate-failure-boundary-audit.md
docs/milestones.md
```

runtime、tests、workflows、Schema、doc346、frozen contracts、milestones既有历史、failed-head doc347与
`docs/project-state.md`必须保持各自原identity；本candidate不创建新的bounded project-state product bytes。

由于`docs/milestones.md`已被真实证明超过frozen Public Render容量，本审计不能预注册一条必然把PARTIAL伪装成PASS的readback。
自己的fresh installed-product observation必须机械区分：

| changed target | required fresh observation |
| --- | --- |
| `README.md` | anonymous P2 Public Render diagnostic + unique formal readback |
| 本文 | anonymous P2 Public Render diagnostic + unique formal readback |
| `AGENTS.md` | anonymous exact-commit public/API raw-byte observation，核对完整bytes与SHA-256 |
| `docs/milestones.md` | anonymous exact-commit public/API raw-byte observation，核对完整bytes与SHA-256；另行保留P2 Render仍会PARTIAL的已知边界，不把raw bytes冒充render COMPLETE |

raw/API bytes只证明该exact commit公开了完整changed bytes，不替代P2 render语义，也不授予未来无界文档reader。independent
reconciliation必须同时核对candidate/base/head/tree、changed-file hashes、原始#398/#399 failure identities、Public Render容量边界、
primary audit continuity与四个changed targets的fresh observation。

## 7. 本审计自己的资格链

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、`git diff --check`、
global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O`下与#399失败测试类相关的focused
Review Attention witness。该witness只审当前candidate没有改动runtime语义，不能回填#399。

```text
final docs-only bytes / declared local gates
    -> original PR required gates（attempt 1，禁止rerun洗白）
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product observations per §6
    -> independent reconciliation + finite closeout
    -> R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_GATE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任一门non-success都保留原身份并停止。本审计全部门闭合后也只成为qualified history；它不使#398 readback qualified、#399
qualified或public projection effective。

## 8. 当前状态与后继停止线

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_MERGED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_EXACT_MAIN_DUAL_GATES_PASS
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_PR_399_FAILED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_NOT_EFFECTIVE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

完整资格链闭合后必须返回CONTROL LOOP；若没有新反例，下一最小seam才是从新的exact main建立独立docs-only、versioned public
project-state projection recovery candidate（新文档号不得复用doc347）。不得从本文直接冻结#398 implementation、恢复#399、启动
runtime/manifest/Evidence/persistence/public Review或R2–R6。
