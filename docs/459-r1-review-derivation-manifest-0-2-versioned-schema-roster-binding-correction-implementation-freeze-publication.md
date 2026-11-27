# R1 Review Derivation Manifest 0.2 versioned schema roster binding修正实现冻结发布

日期：2026-11-27

> 条件化状态目标：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@9e7f998899cd5c7e87ad201c7a41047a66fc8dc3`，tree
> `ee1fc82c69bafb0e92f3fff5de9ff8f593c2c642`。
>
> 上游：[versioned schema roster binding可行性审计](457-r1-review-derivation-manifest-0-2-versioned-schema-roster-binding-feasibility-audit.md)与
> [修正发布](458-r1-review-derivation-manifest-0-2-versioned-schema-roster-binding-correction-publication.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改test、runtime、workflow、Schema、fixture、oracle、Manifest产品、
> global composition、public Review或R2–R6；只在自己的完整资格链闭合后发布PR #523中同一单文件test-support修正的`FROZEN`状态。

## 1. CONTROL LOOP 与本publication的唯一职责

doc458的docs-only publication已经完成自己的local/original PR/protected merge/new exact-main双门、fresh installed-product readback、
independent reconciliation与finite closeout，因此只允许独立后继修改：

```text
tests/test_review_r1_admission_evidence_schema.py
```

PR #523随后把该修正精确合入：

```text
base                 = 21b4f1be3181452c7d6f54d1e99ea619093cd30f
head                 = 3d14566214687a51dbd76134ce379dbb01e2094e
candidate/merge tree = ee1fc82c69bafb0e92f3fff5de9ff8f593c2c642
ordinary merge       = 9e7f998899cd5c7e87ad201c7a41047a66fc8dc3
diff                 = 1 commit / 1 file
```

三个远端门只认各自original attempt，没有rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #523 original Public CI | `45112680888` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `45116529682` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `45116529681` | 1 | 1/1 SUCCESS |

original qualification与protected merge identity SHA-256分别为：

```text
08fd6433024bbbd265ae456cfd5e173d781459adc5c42167a103925ceb234853
12a221eb816f7a9feed45a747b70e4caa0faea1dfc5187da220aea24370523ba
```

fresh detached world只认`9e7f998...`。README、doc457、doc458各有唯一qualifying Render formal，均为HTTP 200、API/Render
`COMPLETE`、marker唯一与Core `PASS`；AGENTS与milestones各有唯一qualifying anonymous raw/API/exact-Git byte PASS。AGENTS raw
formal #1的anonymous API rate exhaustion、`KeyError('content')`与`ERROR / UNKNOWN`永久保留，formal #2才是PASS。independent
reconciliation、150-artifact finite closeout与post-closeout integrity SHA-256依次为：

```text
10ac5223835205fb87acf307d9ece12d65572034258dd5c4a1f8ec95efb7a996
9d1ac33ac45d54f3126f59462c5c2f28dd31944a97a9835065491394bc26c3fa
71751db84135e1269646c8de30dcb225c7a8a691e295dcca84d00f19f846d45a
```

所以当前最多是：

```text
IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
```

fresh CONTROL LOOP没有发现需要扩大修正边界的反例。下一最小合法seam只是以新的docs-only完整资格链发布同一实现的`FROZEN`
状态；不得顺带重建Manifest successor。

## 2. 本publication冻结的exact对象

本文若完成自己的资格链，只冻结以下test-support行为：

1. historical Manifest 0.1 SHA-256 guard无条件继续复算；
2. Schema roster只允许`[manifest-0.1]`或`[manifest-0.1, manifest-0.2]`；
3. Manifest 0.2存在时，必须核对doc316冻结的`schema_version = 0.2`、`bundle_kind = R1_DERIVATION`与closed shape；
4. `[0.2]`、`[0.1,0.3]`、`[0.1,0.2,0.3]`及任意额外版本继续拒绝；
5. Manifest 0.1产品字节、runtime、workflow、Schema、fixture、oracle与Manifest 0.2产品实现保持不变。

qualified exact main中的修正文件身份为：

```text
tests/test_review_r1_admission_evidence_schema.py
bytes  = 22012
sha256 = 802e716225c6e09824e824e10c89fb401a3eac913a243edc65c8a5c020c31c0f
```

本地qualification中，focused四格与full Review Attention四格全部PASS；full Core第一次四格因继承的无效
`GIT_CONFIG_VALUE_0`产生503/504项setup/test-support failure，保留后由独立Core recovery四格全部PASS。focused、Core recovery、
hygiene与local qualification SHA-256分别为：

```text
cbfd12ecb0f5db0a9e4773e27702e4b964fa2942fbbc4ecf56feafffe5a0ec88
29389a7241d62416737af7015cf0d4c42eb04c08edb648037c0786b1374a71e2
d4b2d3369553e6bddeb890553866da431d6cbb393db468b93b4ef1bde0262b5a
46011c2cfbc0aeb73718d2292d9ffa2f8939c194c11d3509a92d93772a963f1e
```

这些witness只证明声明的test-support边界，没有把测试升级为产品authority，也没有证明Manifest/global composition或整个工程问题
已经解决。

```text
proof_is_not_problem_solving                = true
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
global_composition_authority_restored       = false
```

## 3. 必须继续保留的non-success

后继PASS不得删除、覆盖、改名或解释以下identity：

- PR #519 original required Python 3.10/3.13 Core regression失败与所有后继SKIPPED；
- PR #523 local full Core attempt1继承无效Git config后的四格setup/test-support failure；
- fresh worktree侧栏注册超过100个attachment identity的setup error；
- public wheel首次使用PowerShell `-LiteralPath` wildcard导致的copy setup error；
- anonymous rate diagnostic/preflight的remaining 0与403记录；
- AGENTS raw formal #1的rate-limit response、`KeyError('content')`、`ERROR / UNKNOWN`；
- 全部更早的FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`。

AGENTS formal #2只建立自己的PASS；它不回填formal #1，也不把共享轮换代理出口解释成产品失败。formal #1同一次保存的raw bytes
虽与exact Git同SHA-256，但API交叉观察失败，因此不能被拼成PASS。

## 4. 本publication自己的资格责任

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc457/458、修正test文件、runtime、workflow、
Schema、fixture、oracle、Manifest产品与primary `audit.json`必须保持base不变。

本层local gates重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. PR #523 exact base/head/tree/one-file diff、local/original/protected/exact-main gate evidence与fresh readback continuity；
3. Python 3.10.6 / 3.13.13 × normal / `-O` 的versioned roster bounded witness；
4. read-only global/local hygiene、`git diff --check`与primary `audit.json` continuity；
5. original publication PR gate只认本candidate exact head/tree/attempt；
6. protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
7. fresh anonymous installed-product README/doc458/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
8. independent correction-source/retained-failure/readback reconciliation与finite closeout。

PR #523 full matrix属于已经资格化的exact source world；本文不以docs-only diff伪造新的runtime语义。任何non-success必须保留原identity
并停止；不得rerun until PASS、弱化oracle、修改doc458或复用旧PASS。

## 5. Candidate qualification pipeline

```text
publication final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original publication PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc458 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observation
  -> independent correction-source / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> target CORRECTION_IMPLEMENTATION_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的Plan/session/Evidence不可复用#523 world；diagnostic不计入资格。worktree alignment与cleanup只属于housekeeping。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_NOT_REBUILT
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`CORRECTION_IMPLEMENTATION_FROZEN` target成为事实。随后必须从新的exact main返回CONTROL LOOP，
重新审计并重建Manifest 0.2 implementation successor；不得复用#519或#523 qualification，不得恢复global composition或启动public
Review/R2–R6。R1完成后由人类与AI共同进行的全项目检查继续是独立后续目标。
