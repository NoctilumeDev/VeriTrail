# R1 manifest carrier successor original-gate 失败边界审计

日期：2026-11-15

> 状态：`R1_MANIFEST_CARRIER_SUCCESSOR_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 坐标：`main@ce4fe48356a088bee2d2cd12cc0bbaf590980925`，tree
> `cd395c903b2e9b96d480d7361d035f700023d0d9`。
>
> 受审对象：PR #476 的 original Public CI attempt 1 failure；PR 已关闭且未合并。
>
> 影响：`L3_SYSTEM_DESIGN + L0_DOCUMENTATION`。本文只保存失败 identity、资格影响、未决归因和最小重开边界；
> 不修改 M10 runtime、tests、fixtures、Browser/Bootstrap oracle、workflow、Schema、DerivationEvidence、carrier、Manifest、
> Verdict、persistence 或 public Review，也不把失败候选升级为 qualified history。

## 1. CONTROL LOOP 进入点

[文档 414](414-r1-same-attempt-derivation-evidence-manifest-carrier-successor-precontract-audit.md) 的候选由 PR #475 从
`base=af39730a4527157cc820d23ad40557f5d2c3de30`、
`head=101fffa801df1eb6dcd556323b0ca7469987a317`、
`tree=cd395c903b2e9b96d480d7361d035f700023d0d9` 精确合入当前 main。original Public CI
`43715023036` 与 exact-main Public CI `43717832528` 均为 15/15 SUCCESS，Browser Smoke `43717832351`
为 1/1 SUCCESS；fresh readback、independent reconciliation 与 finite closeout 全部闭合。因此 doc414 已成为
`PRECONTRACT_AUDITED / QUALIFIED_HISTORY`。

fresh CONTROL LOOP 随后只建立 docs-only successor contract candidate。它在独立分支中写入
`docs/415-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract.md`，没有创建 Schema、runtime、
carrier、Manifest 或 persistence，也没有取得任何 implementation authority。

## 2. PR #476 的精确候选身份

PR #476 的 immutable candidate identity 为：

```text
base  = ce4fe48356a088bee2d2cd12cc0bbaf590980925
head  = 4226e51c92adcfdc166e7c5563cc69c35907fa50
tree  = a4016d4294def799bac99103d9062f846dbc172b
scope = README.md
        AGENTS.md
        docs/415-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract.md
        docs/milestones.md
commits = 1
files   = 4
```

候选本地 semantic audit 在 Python 3.10.6 / 3.13.13 × normal / `-O` 四格得到逐字节相同结果；focused
regression 四格各 131/131 PASS，global/local hygiene 8/8 PASS，local validation 通过 2260 条相对链接。
这些 local witness 的主要身份为：

```text
semantic canonical SHA256 = 0f2e1586fbe77c7c186a7d73a66d3b5a19f7bd951d5706ef7991fccfaddd0cc7
focused matrix SHA256      = 787df154cdc101e0008413bf159500304412a52d1297fb593170d420abe36ca5
local qualification SHA256 = d2c3fcd0cb030985751fa7f2d0fb2bc0c4855d92d2d0182edbc6cdf028fba749
pre-PR evidence seal SHA256 = 1dd6680e1660b65ec96f6c99bb6b73a765b40a05200f209950b82cd5892ff8c4
post-commit seal SHA256     = 20fd5d51e0b5c964547ff46646f3809b13a3afd12aadf1ca1d8a0bd09ace32b8
```

local PASS 只说明候选字节在预注册 local witness 中成立，不替代 original PR required gate。

## 3. original Public CI 的直接失败事实

PR #476 的 original Public CI `43728958491` attempt 1 精确绑定上述 head。实际 run graph 有 12 个 job：

- Review Attention 四格、Workbench、E3 release download acceptance 与 Python 3.13 均 SUCCESS；
- Python 3.10 on Windows job `132864515924` 在 `Run Core regression tests` FAIL；
- 失败后四个下游 job SKIPPED；
- 没有 rerun。

唯一 unittest failure 为：

```text
tests.test_bootstrap_run_cli.BootstrapRunCliTests.
test_subject_drift_is_preserved_and_makes_public_verdict_inconclusive

expected contamination = {BOOTSTRAP_SUBJECT_DRIFT}
observed extra item     = BROWSER_STATUS_CONFLICT

Ran 497 tests in 128.218s
FAILED (failures=1, skipped=1)
```

原始 failed job log SHA256 为
`d4d685f33dc0b470341803471c8ce3cbcb01440faf9c36f343e46303d1a18469`；结构化 original-gate
failure record SHA256 为
`8d54f5f0c2c2b46fdd48e8d02468df0be435c52d5cbbe673e216e0e64c36ad7c`。因此 PR #476 已关闭且未合并，状态固定为：

```text
ORIGINAL_PUBLIC_CI_FAILED
CLOSED_UNMERGED
NOT_QUALIFIED
```

doc415 没有进入 main；它的 candidate head/tree、local evidence 与失败 run identity必须保留，但不得被任何后继 PASS 回填。

## 4. 取证与 diagnostic 的 retained errors

第一次 failure capture 错把 run graph 预期为 15 job，而实际为 12；该 proof-target setup error 已保留为：

```text
ORIGINAL_GATE_FAILURE_CAPTURE_ATTEMPT1_JOB_COUNT_PROOF_TARGET_SETUP_ERROR
SHA256 = 09646bff2667f10dfde4a2ecb6ee3e3ce979e7c364b6bca444aa0c8293fefa52
effect = NONE
```

第一次 local diagnostic 又清除了 `PYTHONPATH`，四格均在产品测试前以
`ModuleNotFoundError: No module named 'veritrail'` 终止；它已保留为：

```text
ORIGINAL_FAILURE_LOCAL_DIAGNOSTIC_ATTEMPT1_IMPORT_SETUP_ERROR
SHA256 = c2e8e4ee23559039f5646d8ad53aeb1be00541e1b623cbc293795cf5dce31f78
effect = NONE
```

修正 harness 后，只运行精确失败 test 的 Python 3.10.6 / 3.13.13 × normal / `-O` 四格均 1/1 PASS；summary
SHA256 为 `04780ffb8e9b98dbab1e57c9d9ab29751c90c31af6f212e36115fc89ee9cb5b2`。该结果只能分类为
`NON_QUALIFYING_DIAGNOSTIC`：它证明失败没有稳定复现，不解释原失败，也不能补写 original gate。

本审计 worktree 的侧栏登记又因本聊天累计超过 100 个 attachment identity 失败；首次 tree probe 也因 PowerShell 对
`HEAD^{tree}` 的解析产生 operator setup error。两个身份均只影响取证设施，不影响 exact checkout，并在本审计 evidence root
中单独保留。

## 5. 当前证据能证明什么

失败时 runtime 的既有 contamination oracle 在 `browser.session.capture_complete=false`、Run
`execution_status=COMPLETED` 且不属于允许的 sealed business failure 时加入 `BROWSER_STATUS_CONFLICT`。同一 Bundle 又因
bootstrap `stop.reason=SUBJECT_DRIFT` 加入 `BOOTSTRAP_SUBJECT_DRIFT`。因此 observed set 与当前 runtime 规则一致：

```text
subject drift observed                 = TRUE
browser capture incomplete             = TRUE in original attempt
conservative contamination projection  = OPERATED_AS_IMPLEMENTED
precise lower cause                     = UNKNOWN
stable local reproduction               = NOT_OBSERVED
doc415 content counterexample           = NOT_ESTABLISHED
runtime semantic defect                 = NOT_ESTABLISHED
Subject failure                         = NOT_ESTABLISHED
```

PR #476 的 patch 只改四份文档，M10 runtime/test/workflow bytes与 exact base相同。这使“doc415直接改变了该测试行为”不成立；但 scope
disjoint 不能免除 required gate，也不能把 UNKNOWN 自动改名为平台偶发。

## 6. 历史相似事实不能冒充同一根因

[M10 bounded bootstrap 合同与实施记录](15-m10-bounded-project-bootstrap.md) 已保存过一次 Python 3.13 full-suite
正向公共 Run 的 `browser_completed=false`：隔离用例、连续三次串行重复及后续 full rerun 均 PASS，当时只分类为未稳定复现的
Browser/timing observation，不修改裁决合同。[M10 第一轮串行复验](18-m10-serial-validation.md) 则明确要求 subject drift world
保持 `COMPLETED/INCONCLUSIVE`。

这些历史事实说明“full-suite load 下 Browser observation 曾出现过未稳定复现的差异”不是全新类别；但它们来自不同提交、运行时、
attempt 与观察 world，不能证明 PR #476 的 `BROWSER_STATUS_CONFLICT` 具有同一个根因。历史记录只作分层证据，不拼接成因果证明。

## 7. 没有理由弱化 oracle

`BROWSER_STATUS_CONFLICT` 保留的是“已完成 Run 却含不完整 Browser capture”的冲突事实。删除该 contamination、把 exact-set
assertion改成忽略额外污染、把 capture incomplete 当作成功，都会让真实未完成观察更容易消失，而不会解释 original failure。

当前最小重开对象因此不是 Verdict 语义，也不是整个 M10 frozen baseline，而是：

```text
M10 subject-drift fixture / browser-capture stability under full-suite load
plus the exact-set test proof target that assumes no independent capture contamination
```

该边界目前只允许 audit。现有证据尚不能决定后继修正应落在 deterministic fixture、Browser timing/stop coordination、测试输出保留，
还是更窄的 proof target；在新的 feasibility audit 建立可重复证据以前，runtime 与 test 均不得修改。

## 8. 禁止的伪恢复

以下动作都不能使 PR #476 或 doc415 取得资格：

```text
rerun Public CI 43728958491
retry until PASS
用 Python 3.13 SUCCESS 或其他 job SUCCESS替代Python 3.10 required failure
用四格隔离 PASS覆盖 full-suite failure
删除、忽略或重命名 BROWSER_STATUS_CONFLICT
把 exact contamination assertion 静默改成 subset assertion
增加 timeout、跳过 Browser、降低 required gate或修改 workflow condition
把历史 M10 偶发直接宣称为本次已知根因
把后继 candidate 的绿灯回填到 PR #476
直接重建并合并 doc415，而不先闭合被重开的基础边界
```

## 9. 最小合法后继 seam

恢复必须串行进行：

1. 本 docs-only failure-boundary audit 先通过自己的完整资格链，只冻结 original failure identity、`UNKNOWN` 与 authority ceiling；
2. 返回 fresh CONTROL LOOP，建立独立 read-only feasibility audit，专门判断 M10 subject-drift fixture / Browser capture在 current exact
   world与 full-suite load 下的稳定性，并改进失败现场保留；
3. 只有该基础边界以自己的新 candidate和完整资格链闭合后，才可从新的 exact main重建 manifest-carrier successor contract；
4. successor contract必须取得新的 base/head/tree、local evidence与original attempt，不能复用 doc415 head/tree或资格。

如果本审计自己的 original gate再次出现同类失败，必须保留新identity并把重复反例纳入同一最小基础边界；不得把重复失败解释为
放宽oracle的理由。

## 10. 当前状态与 authority ceiling

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_FEASIBILITY_RECOVERY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY

R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_SUCCESSOR_ORIGINAL_GATE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_M10_SUBJECT_DRIFT_BROWSER_CAPTURE_STABILITY_BOUNDARY_REOPENED_AUDIT_ONLY

R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

doc414 qualified history与全部 frozen runtime不被改写。本文也不授权任何 Schema、carrier/runtime、Manifest、persistence、global
composition、public Review或R2–R6施工。

## 11. 本审计自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/416-r1-manifest-carrier-successor-original-gate-failure-boundary-audit.md
docs/milestones.md
```

doc414、Core/Workbench runtime、tests、fixtures、workflows、Schema、Evidence、carrier、Manifest与persistence必须保持
`ce4fe483…` base bytes。final bytes至少通过 exact scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required
markers、retained failure hashes、source/test/verdict/history continuity、`git diff --check`、read-only hygiene与primary
`audit.json` continuity。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR required Public CI
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc414 / 本文 / milestones readback
    -> exact-Git/source/test/verdict/retained-failure observations
    -> independent reconciliation
    -> finite closeout
    -> FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是 candidate。闭合后也只允许进入独立基础边界 feasibility audit；不得自动修 test、重建 doc415、启动
runtime或恢复 global composition。`proof_is_not_problem_solving = true`、`local_not_global = true`；R1完成后仍必须由人类+AI共同执行
独立全项目检查。
