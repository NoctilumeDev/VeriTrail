# R1 Review Derivation Manifest 0.2 versioned schema roster binding feasibility audit

日期：2026-11-23

> 当前状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 审计基线：`main@0348f4b42840565538ea831a20d74e4d57e78afd`，tree
> `581f751802601b5309537a99ba90dce939968549`。
>
> 影响：`L0_DOCUMENTATION / TEST_SUPPORT_BINDING_FEASIBILITY_AUDIT_ONLY`。本文只审计旧 `RAE-017`
> historical 0.1 byte guard与doc316 versioned 0.2 identity能否由一个不放宽任意版本的最小test-support表达同时满足；
> 不修改test、runtime、Schema、fixture、workflow、oracle或Manifest产品。

## 1. CONTROL LOOP输入

PR #520已经把[PR #519 original-gate失败边界](456-r1-review-derivation-manifest-0-2-core-regression-binding-failure-boundary.md)
精确合入本基线。original Public CI `45073861962`、exact-main Public CI `45078041431`与Browser Smoke
`45078041397`均为attempt 1 SUCCESS（15/15、15/15、1/1）。fresh README/doc454/doc456 Render与
AGENTS/milestones raw/API/exact-Git byte observations各有唯一PASS；README第一次diagnostic的长尾marker不在有界Render窗口，
以`DIAGNOSTIC_ONLY_NON_QUALIFYING_ERROR`保留，后继reader-visible marker diagnostic没有覆盖它。

独立reconciliation、145-artifact finite closeout与post-closeout integrity为：

```text
reconciliation  931f954bd154548e9a12478a90d4ddee7bb40ac1f86d8a82bdadb155b0213f85
finite closeout  0a5a3930a2d4d2987f9a2b4ba5fd5b186dde45511566e4f18827edee77b25fad
integrity        4a9b3d475734319b029832091696d7dac99b81c3c467c63da9bbe194cb2bd14a
```

因此doc456现在最多是`FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。PR #519仍为closed/unmerged、original required gate
FAILURE、无rerun、not qualified/not frozen；后继任何PASS不得回填它。

## 2. 两项冻结义务

[RelationSet admission合同](183-r1-relation-set-admission-and-public-qualification-binding-contract.md)的`RAE-017`冻结：

```text
historical Manifest 0.1 byte guard rejects an eighth-file -> ninth-file shortcut
```

[Manifest 0.2 successor合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)随后冻结独立版本身份：

```text
review-derivation-manifest-0.1.schema.json  = immutable historical bytes
review-derivation-manifest-0.2.schema.json  = authorized independent versioned successor
schema_version                              = 0.2
```

这两项义务不矛盾。矛盾来自旧Core test把“0.1 bytes/topology不被改写”近似成“目录永远只能含0.1”。

## 3. exact source审计

当前`tests/test_review_r1_admission_evidence_schema.py`已经独立保存0.1 byte guard：

```text
schemas/review-derivation-manifest-0.1.schema.json
sha256:69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91
```

同一test最后另行枚举`review-derivation-manifest-*.schema.json`，并要求结果只等于`[0.1]`。该断言来自早于doc316的
`a454b0d` world。PR #519候选`f5eff36f3a0d37a97b0d0d1e8a39f64cce76d2d6`没有修改0.1；其versioned roster恰为：

```text
review-derivation-manifest-0.1.schema.json
review-derivation-manifest-0.2.schema.json
```

0.2 candidate bytes SHA-256为
`fd37bc4085999dea64715fb7e72073c20d08c3c7ce14b9c2e3fd04895b7a4fa7`，其`$id`、title、
`schema_version=0.2`、`bundle_kind=R1_DERIVATION`与`additionalProperties=false`均与doc316一致。

## 4. 最小可同时满足表达

独立semantic audit没有使用被测producer生成expected roster。唯一允许集合应精确为：

```text
CURRENT_BASE          = [manifest-0.1]
AUTHORIZED_SUCCESSOR = [manifest-0.1, manifest-0.2]
```

机械义务为：

1. 无条件复算0.1历史SHA-256；
2. exact roster只能等于上述两个值之一；
3. 0.2存在时，另行核对冻结的filename、`$id`、title、`schema_version`、`bundle_kind`与closed shape；
4. 只有0.2、0.1+0.3、0.1+0.2+0.3或其他任意文件全部拒绝；
5. 不用glob存在性替代0.1 byte guard，不把0.2产品conformance搬进旧admission test。

这不是删除oracle，也不是把expected list改成任意子集。它把historical byte identity与versioned roster policy拆成两个明确断言。

## 5. 四格审计结果

read-only audit绑定current exact main、PR #519 closed candidate、doc183、doc316、doc456、primary `audit.json`与两份Schema bytes。
Python 3.10/3.13 × normal/`-O`四格逐字节一致：

```text
semantic audit SHA-256 = d790b240bedc199f8cf879dbecaa266e3d99dec4c5b8f98509fa956780215d94
result                 = PASS / PASS / PASS / PASS
```

它只证明单文件test-support correction在现有合同下可表达；不证明具体补丁、PR门、Manifest successor或产品已经合格。
managed worktree attachment cap与第一次schema目录inspection选错root均保留为setup error / effect NONE。

## 6. authority与停止线

当前只重开：

```text
RAE_017_VERSIONED_MANIFEST_SCHEMA_SET_ACCEPTANCE_BINDING
```

不重开0.1 bytes、doc316 contract、Manifest 0.2 Schema/conformance/producer、CoverageLedger、Provider、workflow budget、
global composition、persistence、public Review、Core Verdict、HumanDisposition或R2–R6。

本文全部资格门成立后也最多成为`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。随后必须返回CONTROL LOOP，另建独立docs-only
correction publication；在该publication完整资格化以前，不得修改`tests/test_review_r1_admission_evidence_schema.py`，也不得重建
Manifest successor。

## 7. 本候选资格链

tracked scope只允许README、AGENTS、本文与milestones。local exact scope、links、UTF-8/LF/final LF、Markdown、
`git diff --check`、global/local hygiene、primary audit continuity、四格semantic audit与focused regression成立后，再依次完成：

```text
original PR Public CI 15/15
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc456 / 本文 Render
    -> fresh AGENTS / milestones raw-byte observation
    -> independent reconciliation + finite closeout
    -> FEASIBILITY_AUDITED / QUALIFIED_HISTORY at most
    -> return CONTROL LOOP
```

当前只允许：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PR519_CORE_REGRESSION_BINDING_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_FEASIBILITY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_NOT_REBUILT
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

