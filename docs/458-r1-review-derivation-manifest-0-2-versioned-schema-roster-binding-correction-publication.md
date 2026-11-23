# R1 Review Derivation Manifest 0.2 versioned schema roster binding修正发布

日期：2026-11-23

> 候选状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@982a269e5bcd54733e0960d065f46d852aeb5aa9`，tree
> `186f62cad00fadfb58386d5c647e868794df87f8`。
>
> 影响：`L0_DOCUMENTATION / CONDITIONAL_SINGLE_TEST_SUPPORT_CORRECTION_PUBLICATION_ONLY`。本文不修改test、runtime、
> Schema、fixture、workflow、oracle或Manifest产品；只有自己的完整资格链闭合后，才为一个独立单文件test-support
> implementation candidate条件化冻结修正边界。

## 1. CONTROL LOOP输入

PR #521已经把
[versioned schema roster binding feasibility audit](457-r1-review-derivation-manifest-0-2-versioned-schema-roster-binding-feasibility-audit.md)
精确合入本基线：

```text
candidate base          0348f4b42840565538ea831a20d74e4d57e78afd
candidate head          cd8cd7a7c33559a1efb3b0f4a8126cb0c1b1679e
candidate tree          186f62cad00fadfb58386d5c647e868794df87f8
original Public CI      45084517912 / attempt 1 / 15 of 15 SUCCESS
protected merge         982a269e5bcd54733e0960d065f46d852aeb5aa9
exact-main Public CI    45088700138 / attempt 1 / 15 of 15 SUCCESS
exact-main Browser      45088700115 / attempt 1 / 1 of 1 SUCCESS
```

fresh README/doc456/doc457 Render与AGENTS/milestones raw/API/exact-Git byte observations各有唯一qualifying PASS。README
formal observation #1在Public Render `COMPLETE`后收到GitHub API `403 / remaining 0`，以
`FORMAL_READBACK_ERROR / ANONYMOUS_RATE_LIMIT_EXHAUSTED`永久保留；reset后的新Plan与新collection session #2才为PASS，
没有覆盖#1。最终身份为：

```text
independent reconciliation   5ba6bb2f1613ff4a8d367cca108edd6f015c3baed38dda426e1ed463769ab704
148-artifact finite closeout  4862f6288a7ccdb0d9a4e74d8434a9e9db23783b51cc7cb1e276d1d736d3091e
post-closeout integrity       54834c680107d7c37bbd5b7a1f373ccbe169add38d82c7bea6357088b6d4132c
```

因此doc457现在最多是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。它证明一个不弱化oracle的最小表达存在；它没有修改测试，
也没有给Manifest successor续期。

## 2. 必须同时保持的证明义务

后继test-support correction必须同时机械保持：

```text
historical 0.1 bytes SHA-256 = 69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
CURRENT_BASE roster          = [review-derivation-manifest-0.1.schema.json]
AUTHORIZED_SUCCESSOR roster = [review-derivation-manifest-0.1.schema.json,
                               review-derivation-manifest-0.2.schema.json]
```

允许versioned successor不等于允许任意glob成员。`0.2`不得取代`0.1`，也不得把historical byte guard降级为文件存在性检查。

## 3. 条件化冻结的唯一实现边界

本文全部资格门闭合后，后继implementation candidate只允许修改：

```text
tests/test_review_r1_admission_evidence_schema.py
```

该文件中的`RAE-016/017`测试只能作以下最小修正：

1. 每次仍无条件复算Manifest 0.1文件的冻结SHA-256；
2. 实际`review-derivation-manifest-*.schema.json` roster只能精确等于`CURRENT_BASE`或`AUTHORIZED_SUCCESSOR`；
3. 当且仅当0.2文件存在时，另行核对冻结filename、`$id`、title、`schema_version=0.2`、
   `bundle_kind=R1_DERIVATION`与`additionalProperties=false`；
4. 显式证明只有0.2、0.1+0.3、0.1+0.2+0.3及其他额外/未知版本均不在允许集合；
5. 不把Manifest 0.2产品conformance、fixture或producer逻辑搬进旧admission test，不改变`RAE-016` identity-cycle oracle。

允许把historical byte identity与versioned roster policy拆成两个具名断言或窄helper；不得用任意子集、前缀、排序后截断、
“至少含0.1”或动态发现后自我接受替代精确集合。

## 4. 实现候选的独立资格要求

后继implementation不能与本文同commit，也不能复用PR #519的head、tree、original run或本地qualification。它必须从本文资格化后的
新exact main建立单一test-file candidate，并至少独立证明：

- current base `[0.1]`保持PASS，0.1 byte hash继续逐字节成立；
- policy vectors精确接受`[0.1]`与`[0.1,0.2]`；
- policy vectors拒绝`[0.2]`、`[0.1,0.3]`、`[0.1,0.2,0.3]`与任意额外成员；
- 使用doc316冻结的0.2 identity/closed shape时通过，任何一项identity或closed-shape漂移时失败；
- 双Python normal/`-O` focused与完整Core/Review Attention witness、scope/hygiene、primary audit continuity均成立。

implementation自己的original PR gate、protected exact-head merge、new exact-main双门、fresh installed-product readback、独立
reconciliation与后继docs-only freeze publication仍须全部完成；只有实现冻结后才可返回CONTROL LOOP重建Manifest successor。

## 5. 保留的历史与禁止扩张

PR #519继续是closed/unmerged、original required gate FAILURE、no rerun、not qualified/not frozen；后继PASS不得回填。doc456的
`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`与doc457的`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`均保持原身份。

本文不重开或修改：

- Manifest 0.1历史bytes；
- doc316的Manifest 0.2 Schema/conformance/producer合同与candidate bytes；
- CoverageLedger、Fact/Relation/Slice Provider、workflow budget、default/global composition与persistence；
- Core Verdict、HumanDisposition、public Review或R2–R6；
- primary `audit.json`或任何既有FAIL/ERROR/CANCELLED/setup failure/UNKNOWN。

如果单文件修正不能在不删除oracle、不放宽版本集合且不修改产品字节的条件下通过，它必须停止并只重开被真实反例击穿的最小边界。

## 6. Exact docs-only scope

本candidate只允许：

```text
README.md
AGENTS.md
docs/458-r1-review-derivation-manifest-0-2-versioned-schema-roster-binding-correction-publication.md
docs/milestones.md
```

runtime、tests、Schema、fixture、workflow、doc183/doc316/doc456/doc457、`docs/project-state.md`与primary `audit.json`必须保持
`982a269…` base bytes。local gates至少复算exact scope、UTF-8/LF/final-LF、links/fences/headings、required markers、
`git diff --check`、global/local hygiene、doc457 qualified-history evidence、PR #519 retained failure、remote main与primary audit continuity。

## 7. Qualification pipeline

```text
final docs-only publication bytes / declared local gates
    -> immutable PR body seal
    -> original PR Public CI 15 of 15 / attempt 1 / no rerun
    -> protected exact-head merge
    -> new exact-main Public CI 15 of 15 + Browser Smoke 1 of 1
    -> fresh anonymous installed-product README / doc457 / 本文 formal
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent retained-failure / feasibility / correction-boundary reconciliation
    -> finite closeout + post-closeout integrity
    -> VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_FROZEN
    -> return CONTROL LOOP
```

每个formal identity只运行一次；任何non-success保留原identity。产品调用必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。

## 8. 当前状态与生效条件

本文自己的最后门闭合以前只允许：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_NOT_REBUILT
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后才条件化变为：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_ALLOWED
```

随后必须返回CONTROL LOOP，从新的exact main建立独立单文件implementation candidate。本文不让PR #519续期，不宣称测试已修改或
Manifest 0.2已经实现，也不恢复global composition或启动public Review/R2–R6。`proof_is_not_problem_solving = true`、
`local_not_global = true`、`target_continuity_over_local_correction = true`继续成立。
