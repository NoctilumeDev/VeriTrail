# R1 public project-state projection doc350 readback recovery publication 0.1

日期：2026-11-05

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@da6a6b3e692bf2486ca428dd5ed9c2068918e982`，tree
> `102b1e3e5f6844b278edee3caa83d10dc6dc8179`。
>
> 受审对象：doc350 failure-boundary audit 在新的 exact world 中的公开可观察性与资格恢复。
>
> 影响：`L0_DOCUMENTATION + L3_QUALIFICATION_RECOVERY + PROOF_FACILITY_PATH_BUDGET`。本文不修改doc350、doc351、
> doc349、`docs/project-state.md`、runtime、tests、workflow、Schema、Provider、Collector、P2 oracle、Core evaluator、
> Fact/Relation/Coverage semantics、Verdict或任何frozen contract。

## 1. CONTROL LOOP 输入：两个失败世界与一个 qualified boundary

[文档350](350-r1-public-state-projection-successor-readback-failure-boundary-audit.md)由PR #402合入
`main@4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea`。它自己的original/exact-main双门均PASS，但fresh README formal在
API/Render `COMPLETE`、marker一次、samples稳定、cleanup complete之后，于Acceptance Core创建Verdict以前持久化Evidence时对
271字符本地目标路径触发`FileNotFoundError [Errno 2]`。该formal保持：

```text
identity = r1-psp-v2-readback-fb-audit-formal-readme-1-4fd9a78
classification = FORMAL_READBACK_ERROR
Core verdict = NOT_CREATED
proof-facility local output failure = ESTABLISHED
legacy Windows MAX_PATH causality = HYPOTHESIS / NOT_ESTABLISHED
underlying local filesystem cause = UNKNOWN
```

doc350 formal、AGENTS与milestones raw-byte observation均保持`NOT_RUN`；本publication不得用新world的后继观察回填这些身份。

failure-boundary、93-artifact failed closeout与finite integrity分别为：

```text
6e33bedd7228ac7f080f9209374b9fa3671d8e12e6fb318832e943477e90e397
87592d66e1c3d3eed5e2ea5b73a60f3bbd90047c15416318a3b18ee04e31dd7e
35ea330b2d05646fbef5b7693fc78fa417526e1130419ed5b61f0d960396f6a6
```

独立[文档351](351-r1-public-state-projection-audit-readback-bundle-persistence-failure-boundary.md)由PR #403以exact
`base=4fd9a78ab994475b05a2cb5bc1f2d6108a9572ea / head=d6ee533e9751380d4e981204c1d5c6e95fc26762 /
tree=102b1e3e5f6844b278edee3caa83d10dc6dc8179`合入本构造坐标。original Public CI `41968023423`、exact-main
Public CI `41971091826`与Browser Smoke `41971091790`均为attempt 1 SUCCESS。fresh README/doc351 formal与
AGENTS/milestones exact-commit raw-byte observation各有唯一PASS；reconciliation与finite closeout identity为：

```text
independent reconciliation = 972b9fa8c37c90f6a214128cae28e60d1647662ae1808040c96efa074673d24f
147-artifact closeout      = 45f26afccb77ea779bf0ed47b8780779129c22f7e17af27f802b518b8b00452f
self-capture mismatch      = 0de80aa38eb2f223591e5d37f1214f33d3ada6d5044848f2433afafd180a8172
finite integrity           = 1b2243f5ec2a008c3145baed9398dfae69db0a1ecaebaaaf9facbd6653d3b70f
```

gate capture attempt 1的stale parents、attempt 2的stale PR identity、anonymous rate exhaustion与closeout stdout
self-capture mismatch均按原identity保留。doc351现在是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`；它只证明恢复可在不弱化
oracle的短路径world完成，不回填#402，也不解释底层文件系统`UNKNOWN`。

## 2. versioned recovery 的最小边界

本publication不重跑#402 formal，也不把`C:\vt351e`的PASS改写成#402的PASS。它建立新的candidate、merge、attempt、
collection session与Bundle identity，并固定：

1. doc350/doc351/doc349/project-state bytes不变；
2. readback必须使用新的短evidence root，formal前记录最坏case acceptance-bundle target字符数与声明上限；
3. proof-facility path budget只约束本publication的本地输出拓扑，不升级Core或产品语义；
4. #402的271字符失败路径、stderr、partial Bundle、failed closeout、MAX_PATH hypothesis与`UNKNOWN`原因永久保留；
5. 新formal必须继续要求API/Render `COMPLETE`、marker可见、Bundle完整持久化、Core Verdict `PASS`与cleanup complete；
6. 任一non-success按自己的identity保留并停止，不得换目录、重复target或借旧PASS拼接。

因此新的PASS若成立，只能证明doc350内容在本publication exact world重新取得资格；不能证明#402从未失败，也不能把短路径
提升成产品运行时合同。

## 3. tracked scope 与公开观察面

tracked scope只能是：

```text
README.md
AGENTS.md
docs/352-r1-public-state-projection-doc350-readback-recovery-publication.md
docs/milestones.md
```

合入后必须取得：

| target | fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal；marker=`doc350 readback recovery publication 0.1` |
| doc350 | anonymous Public Render diagnostic + unique formal；重新证明被恢复审计正文可见 |
| doc351 | anonymous Public Render diagnostic + unique formal；绑定qualified upstream boundary |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致；不把raw bytes冒充Render COMPLETE |

所有render target与raw target必须各有且只有一个qualifying PASS。independent reconciliation还必须核对
base/head/tree、四文件scope、#401 marker failure、#402 persistence failure、#403 qualified history、primary audit continuity、
path-budget preflight与全部setup/non-success identity。

## 4. 本publication的资格链

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、`git diff --check`、
global/local hygiene、primary audit continuity，以及Python 3.10.6 / 3.13.13 × normal/`-O` focused unchanged-runtime witness。

```text
final docs-only bytes / local gates / predeclared readback path budget
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh six-target anonymous installed-product observations
    -> independent reconciliation + finite closeout
    -> DOC350 READBACK_RECOVERED / FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

全部成立以前，本文只是一份candidate，doc350继续`READBACK_NOT_QUALIFIED / NOT_FROZEN`。

## 5. 状态上限与停止线

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_2_READBACK_FAILURE_BOUNDARY_AUDIT_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PUBLIC_PROJECT_STATE_PROJECTION_AUDIT_READBACK_BUNDLE_PERSISTENCE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_1_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_2_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_2_MERGED_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本publication闭合后也必须返回CONTROL LOOP，重新检查projection successor是否仍是最小合法seam。不得把doc350恢复自动解释成
doc349/projection 0.2已资格化、private implementation已冻结、global composition authority已恢复，或runtime/manifest/Evidence/
persistence/public Review/R2–R6已获授权。
