# R1 SourceSnapshot 测试环境模拟修正实现冻结发布

日期：2026-11-23

> 条件化状态目标：
> `R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@72b9936c4cd2c0463401a19fc629babed5068a27`，tree
> `80a9d812e3d967bae851cb3e22c41aec10f09d78`。
>
> 上游：[测试支撑构造拓扑修正](452-r1-review-derivation-manifest-0-2-test-support-construction-topology-correction-publication.md)与
> [SourceSnapshot 测试环境模拟机制反例及授权](453-r1-source-snapshot-test-environment-patch-correction-publication.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改runtime、workflow、Schema、fixture、oracle、Manifest产品、
> global composition、public Review或R2–R6；只在自己的完整资格链闭合后发布PR #517中同一单文件test-support修正的
> `FROZEN`状态。

## 1. CONTROL LOOP 与本publication的唯一职责

doc453的docs-only publication已经完成自己的local/original PR/protected merge/new exact-main双门、fresh installed-product
readback、independent reconciliation与finite closeout，因此只允许独立后继修改：

```text
plugins/review-attention/tests/test_source_snapshot_contracts.py
```

PR #517随后把该修正精确合入：

```text
base                 = 6668b45403b885d30ffe52cfc17ad1cb25ae1518
head                 = fa8d688baa41724373e96333e4e2511e5b070af3
candidate/merge tree = 80a9d812e3d967bae851cb3e22c41aec10f09d78
ordinary merge       = 72b9936c4cd2c0463401a19fc629babed5068a27
diff                 = 1 commit / 1 file / +17 -3
```

三个远端门只认各自original attempt，没有rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #517 original Public CI | `45036838130` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `45040921719` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `45040921668` | 1 | 1/1 SUCCESS |

original qualification、protected merge与exact-main gate seal SHA-256分别为：

```text
78601cb494c7d043c3747f52e8add5c80304095138739d34119732778c5e836e
4e1aa57c3c8df8d35f461f41b817de19b340acc7a9d27e28295ba6086fd6f13e
42540f0814e42fd22ef7f1da2064a8b1a82e7b569dc0d498450b798751cab4bf
```

fresh detached world只认`72b9936...`。README、doc452、doc453各有唯一qualifying Render formal，均为HTTP 200、
API/Render `COMPLETE`、marker唯一与Core `PASS`；AGENTS与milestones各有唯一anonymous raw/API/exact-Git byte PASS。
independent reconciliation、163-artifact finite closeout与post-closeout integrity SHA-256依次为：

```text
39dc58d48e6ca48c423bb7e3e7cb614f6d5b65131b98552384dff953488b38c2
1e181cc6bcb418a9b6c934172c0f1118c5731c31257e3a357e13cf1301979fb7
d69b118f157aa467a0e911393349b777c8be7a6b9168de9c3a42f42f2f3f7a8c
```

所以当前最多是：

```text
IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
```

fresh CONTROL LOOP没有发现需要扩大修正边界的反例。下一最小合法seam只是以新的docs-only完整资格链发布同一实现的
`FROZEN`状态；不得顺带重建Manifest successor。

## 2. 本publication冻结的exact对象

本文若完成自己的资格链，只冻结以下test-support行为：

1. 合同测试继续使用原`inherited`字典、blocked-key denominator、safe values与全部断言；
2. `_controlled_git_environment()`调用期间，测试把`veritrail_review.git_objects.os.environ`临时指向独立Python mapping，
   不再通过`mock.patch.dict`写入真实进程环境；
3. context退出时恢复Python object reference，不对宿主OS environment执行set/delete；
4. 同一Python进程中的后继真实裸`git init`必须成功；
5. SourceSnapshot runtime、Git采集逻辑、workflow、Schema、fixture、oracle、Manifest产品与八world denominator保持不变。

qualified exact main中的修正文件SHA-256为：

```text
plugins/review-attention/tests/test_source_snapshot_contracts.py
c4a56c3be8d51862441d84516d976999a519f20b71deefa49771eaa0e83bd3be
```

本地qualification中，direct legacy/isolated falsifier、same-process contracts-to-runtime、focused四格与full Review Attention
四格全部成立；full matrix四格各`694/694 PASS`，semantic summary与local qualification SHA-256分别为：

```text
6ec7a304a3ac8c8f52b7ff9676f4a1075cb09b825ca6969cdb2febdd6cc088d1
32e20ca794b11a7902fa875fd53110f3cb15aae88e06387426009f947ab28602
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

- 旧Manifest successor formal full matrix四格失败、3.10 normal serial v2二十个repo setup errors与control-loop cancellation；
- PR #517资格化以前的wrong-worktree、empty stdout、local composer、schema assumption与其他proof-facility setup errors；
- fresh readback首次README formal的gate-schema mismatch setup error；
- doc452 formal observation1的anonymous GitHub API rate exhaustion `ERROR / UNKNOWN`；
- dynamic setup-history被旧adapter freeze误当成不可变代码的preemptive proof-facility review finding；
- 全部更早的FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`。

doc452 successor formal observation2只建立自己的PASS；它不回填observation1，也不把匿名额度耗尽解释成产品失败。formal adapter
v5与raw adapter v2只分离稳定代码字节和append-only history，SHA-256分别为：

```text
429018e24f5cd4f69bb7b1b6afefb419b6dd989a281d0ec994c69b7a77c5695e
dc9f10ea322c49aebcc21bb170b3bbc6781b9d851f6fcf099536b155409f6924
```

## 4. 本publication自己的资格责任

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc452/453、修正test文件、runtime、
workflow、Schema、fixture、oracle、Manifest产品与primary `audit.json`必须保持base不变。

本层local gates重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. PR #517 exact base/head/tree/one-file diff、local/original/protected/exact-main gate evidence与fresh readback continuity；
3. Python 3.10.6 / 3.13.13 × normal / `-O` 的SourceSnapshot contracts-to-runtime bounded witness；
4. read-only global/local hygiene、`git diff --check`与primary `audit.json` continuity；
5. original publication PR gate只认本candidate exact head/tree/attempt；
6. protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
7. fresh anonymous installed-product README/doc453/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
8. independent correction-source/retained-failure/readback reconciliation与finite closeout。

PR #517 full matrix属于已经资格化的exact source world；本文不以docs-only diff伪造新的runtime语义。任何non-success必须保留原identity
并停止；不得rerun until PASS、弱化oracle、修改doc453或复用旧PASS。

## 5. Candidate qualification pipeline

```text
publication final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original publication PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc453 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observation
  -> independent correction-source / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> target CORRECTION_IMPLEMENTATION_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的Plan/session/Evidence不可复用#517 world；diagnostic不计入资格。worktree alignment与cleanup只属于housekeeping。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_TEST_SUPPORT_CONSTRUCTION_TOPOLOGY_CORRECTION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_STOPPED_PRE_COMMIT_FULL_MATRIX_FAILED_NOT_QUALIFIED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_ALLOWED
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_SOURCE_SNAPSHOT_TEST_ENVIRONMENT_PATCH_CORRECTION_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`CORRECTION_IMPLEMENTATION_FROZEN` target成为事实。随后必须从新的exact main返回CONTROL LOOP，
重新审计并重建Manifest 0.2 implementation successor；不得复用已停止候选的qualification，不得恢复global composition或启动public
Review/R2–R6。R1完成后由人类与AI共同进行的全项目检查继续是独立后续目标。
