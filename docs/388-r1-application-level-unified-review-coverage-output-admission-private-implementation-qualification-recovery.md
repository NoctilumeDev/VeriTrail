# R1 application-level unified Review / Coverage output admission 私有实现资格恢复 0.1

日期：2026-11-09

> 候选状态：
> `R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_EXACT_MAIN_QUALIFICATION_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@6da3fdd10e28162e05a518663b0553fcd11afe00`，tree
> `212d3d953fe9c88ac70bb2ab643af9956b64d507`。
>
> 条件化目标：本文自己的全部资格门闭合后，[文档387](387-r1-application-level-unified-review-coverage-output-admission-private-implementation-successor-candidate.md)
> 所绑定的六个implementation/test blob最多升级为
> `IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。
>
> 影响：`L0_DOCUMENTATION / IMPLEMENTATION_QUALIFICATION_RECOVERY_ONLY`。本文不修改private runtime、tests、workflow、
> required lane、inner timeout、oracle、Schema、Provider、Collector、Coverage reason、public export、manifest、Evidence、
> persistence、Core Verdict或R2–R6能力。

## 1. CONTROL LOOP 输入：实现已合入，资格链没有闭合

[successor implementation candidate](387-r1-application-level-unified-review-coverage-output-admission-private-implementation-successor-candidate.md)
由PR #439以exact
`base=ce9fa08aa62b0ffd3a87c8e4d8f61b9e49ce3d5e / head=d6a40b5c7fc79f3f420aaa6625c5903face76bc2 /
tree=a9c3c9676b45f30aeb9ad38d482616ad1394852b`进入受保护主线，ordinary merge为
`1b7350ee0adbd028c97954372e9795d98ffbd487`。original Public CI `42502371306` attempt 1为11/11 SUCCESS，
Browser Smoke `42505545660` attempt 1为1/1 SUCCESS。

但exact-main Public CI `42505545592` attempt 1终态为`CANCELLED`。required Python 3.10 job `128807254935`在固定35分钟
outer containment内运行，Core、Authoring、GitHub Evidence与Review Attention normal步骤均已成功；终止发生在assertions-disabled
Review Attention步骤，日志没有产品assertion failure。该run没有rerun，readback与reconciliation没有启动。取消capture、run、job
log、annotations、failed closeout与finite integrity SHA-256为：

```text
7d1f71d14f45e921bb2caa7f3cadd30b4fbeecbe722598a9a432f91848ae83e9
b1fdfd2d9f709d0a3e2a66e5d47ece90185b149747eeac0a72418da1ac79710f
daeaeba3486fc642606235161873e14d3ed4b3823eae140f54b859793af57ee8
f8b1eef39b4b81e1d8d0423b470dd9c5ac248d942aa86f637b3e7bf719bc0af3
03426d3f83ecb3173ec33ba25b9b5d4de6e700804530b508486d83bed447a7cc
09c01809dfce7f91ac713fae1ff548b093451e5b9fd7482b0ac73b1753146056
```

因此#439保留：

```text
RUNNER_JOB_TIMEOUT_BUDGET_EXHAUSTED           = ESTABLISHED
workflow recovery-headroom invariant          = NOT_MAINTAINED
product assertion failure                     = NOT_OBSERVED
candidate semantic regression / Subject failure = NOT_ESTABLISHED
lower resource cause                          = UNKNOWN
qualification                                 = NOT_ESTABLISHED
```

original success、Browser success与相同tree不能拼接成exact-main Public CI PASS，也不能把`CANCELLED`重解释为产品PASS。

## 2. 两个maintenance world必须分别保留

第一次独立maintenance PR #440只把`.github/workflows/ci.yml`中Python aggregate outer timeout从35提高到45分钟，没有修改
产品、测试、命令、inner timeout、required lane或oracle。其original Public CI `42510104584` attempt 1真实FAILURE（10/11）：
两个长Python job都成功，但required Starter job在正确产品runs之后的Catalog→run-detail浏览器观察超时。Artifact
`13630875034` archive SHA-256为
`4b6410400840042bd30ff221f1b19db8b5ade28a35c18d4d15b49376b2ce8a15`。PR #440已关闭、未合并、未rerun；
底层原因仍为`UNKNOWN`，maintenance regression、Starter Subject failure与Workbench regression均未建立。classification、
failed closeout与finite integrity SHA-256为：

```text
e038892e1e5140a456681eeba9d4e2efe91d0c76a382546b6c43a3b93eeec688
21296c63df92ea89b66edbb542c33fc854203f805d6756fdbe875d55ec7bbe28
f91640fa0f51287f9d0e799931d851f8464afabde18b78af76adb6e983128b66
```

独立successor maintenance PR #441使用新的head、PR与attempt，只保留同一行35→45分钟变更：

```text
base = 1b7350ee0adbd028c97954372e9795d98ffbd487
head = d7c676ceecbe748d35d871ebcd1a8ae9e5ca3678
tree = 212d3d953fe9c88ac70bb2ab643af9956b64d507
```

original Public CI `42514455000` attempt 1为11/11 SUCCESS；Python 3.10自然运行42分41秒，直接证明35分钟不足、45分钟
有界完成。protected merge形成当前构造坐标；new exact-main Public CI `42518266450` attempt 1为11/11 SUCCESS，Browser Smoke
`42518266390` attempt 1为1/1 SUCCESS，Python 3.10又自然运行35分45秒。fresh anonymous exact-SHA workflow raw bytes与local
Git blob逐字相等，只含唯一45分钟值。original qualification、protected merge、exact-main gates、workflow readback、independent
reconciliation、70-artifact closeout与finite integrity SHA-256为：

```text
d1c2edbbafea9d4dfb39a40b906735467364e3b086e55a6a235c287680898fc7
e9f49c1dc5e9379e9891de0473b589f2f5b1abb087c29fededac6525d8818c59
4cb294acb2b5bd0180f7c5c88f11b6678e55e947dfc1b3541eda318686f034da
f067ac4dbd89bb135acc7e66f051016ccc93209c5d732f8a04827561b6be8101
928086797899a4d5cd67676d5825ff144633a5518c38028316ae5decfaff74c4
4ef5222a10fb1cc121da5a58d3ff3e1a919a2961f1a18752ea6e65409c1d6986
74f9e04e7f127532d31230010a2fba2e171a9bb71e14d33139a8e5d144c52613
```

这些事实只资格化CI containment maintenance。它们不回填#439或#440，不解释两个`UNKNOWN`，也不自动资格化语义实现。

## 3. exact implementation 与合同字节连续性

从#439 merge到当前构造坐标，tracked diff只有`.github/workflows/ci.yml`。六个implementation/test blob逐一保持：

| path | blob SHA-1 |
| --- | --- |
| `_fact_to_coverage_exact_input_handoff.py` | `1a645c33931b94c657939457379e89900daa357b` |
| `_negative_world_coverage_authority_recovery.py` | `2385cfdbedfc5126ff2510c09c013424328065f9` |
| `_post_terminal_fact_dual_successor.py` | `3dcd4bba30a5a6437ef019e6e7cea4258bdf9797` |
| `_relation_transition_slice_composition.py` | `9235bc5e801f3d83b4d2e70334721bd08749c01a` |
| `_unified_review_coverage_output_admission.py` | `0fcc7ba32617a05d0cda895f0e69f2addb95b716` |
| `test_unified_review_coverage_output_admission.py` | `9340a522a6aef62511375196472f2d97ca84933a` |

doc380–383、doc386与doc387也与#439 merge world保持相同blob。该连续性只证明当前main仍承载同一实现与权威边界；它不能
继承#439的attempt、qualification、admission或closure authority。

## 4. 原工程问题、当前证明义务与适用世界

原工程问题仍是：

```text
为Review/Coverage normal与negative结果建立同一个application-level
可判别、one-shot、authority-preserving output admission边界。
```

本文当前证明义务只是：在qualified outer-containment maintenance之后，重新绑定当前exact main，证明上述不变的六个blob在本层
完整local witness、自己的original PR、protected merge、new exact-main双门与fresh installed-product observation中仍成立。

适用世界仍只包含Python 3.10结构语义、冻结post-terminal selector、两类private downstream result、CoverageLedger 0.3 root chain与
当前资格矩阵；不包含manifest、same-attempt DerivationEvidence continuity、persistence、多语言、public Review或真实人类审查收益。

```text
proof_is_not_problem_solving          = true
qualification_inheritance_allowed    = false
old_cancelled_attempt_rewritten       = false
original_engineering_problem_claimed_solved = false
```

## 5. 本candidate新增的资格责任

本文不是#439 rerun、空提交或把#441绿灯贴到旧实现上。它增加以下独立责任：

1. 用新的docs-only final bytes、base/head/tree、PR与attempt显式承担#439/#440/#441完整history；
2. 在当前exact main重新运行private UAO、focused、full Review Attention、semantic四格、compile/hygiene/scope/audit continuity；
3. 独立证明runtime/test、doc380–383、doc386/doc387与public export在#439 merge至当前base间保持不变；
4. 自己的original PR与new exact-main required gates必须分别完成，任何non-success保留原identity且不得rerun洗白；
5. fresh product observation只能在自己的exact-main双门闭合后启动；
6. independent reconciliation必须同时绑定实现bytes、三个失败/维护world与本candidate自己的全部新identity；
7. target只恢复`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`，冻结必须另行发布。

## 6. Exact scope 与local qualification

tracked scope只能是：

```text
README.md
AGENTS.md
docs/388-r1-application-level-unified-review-coverage-output-admission-private-implementation-qualification-recovery.md
docs/milestones.md
```

private runtime、tests、workflow、doc380–387、`docs/project-state.md`、Schema、Provider、Collector、Coverage、public export、manifest、
Evidence、persistence与Core oracle必须保持base bytes。final bytes至少完成exact scope、UTF-8 without BOM、LF/final LF、links/fences/
headings、required markers、blob/history continuity、`git diff --check`、global/local hygiene、primary audit continuity，以及Python
3.10.6/3.13.13 × normal/`-O`的private UAO、focused、full与semantic witness。

当前exact base上的四格local witness已经分别完成：private UAO每格27/27 PASS；focused每格286 reported / 285 passed /
1 skipped；full每格648 reported，Python 3.10.6为645 passed / 3 skipped，Python 3.13.13为646 passed / 2 skipped；
semantic report四格逐字节一致。对应UAO、focused、full、semantic canonical report、semantic matrix与六个implementation/test
blob continuity evidence SHA-256为：

```text
bc77fc6c45df21a28ce1933726e2e3b893846d8fb321b138fbfd1283beb65261
c224554c91ba4e0c5f23db9e4f48e562fd6787abeab27865fad4fa6f93c96cbd
d31e49fb183ad477bded848dbe8c1a47b887a0fefd028a29653ef047ba267149
1ae2da5ceda24ac65ccc33b4fe84c2e3615c4a37b3ab181f3b9f41fe9a0d5a85
3ead274aad632ab73dec052f2c9acd0e4c3af4869f04c97619131d943c3d02af
23bf3c5f46878cc81bd0bde1218b3f8e3044a73a4b23395388089eb3200ed9a2
```

这些结果只证明当前local candidate world中的既定witness成立；它们不继承#439的exact-main资格，也不把#440/#441的
maintenance facts转换成implementation qualification，更不证明原工程问题已经解决。

## 7. Candidate qualification pipeline

```text
final docs-only recovery bytes + declared local gates
  -> original PR required gates (attempt 1; no rerun laundering)
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc386 / doc387 / 本文 Render readback
  -> fresh anonymous exact-commit AGENTS / milestones raw + API + exact-Git byte observations
  -> independent reconciliation + finite closeout
  -> implementation bytes become IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
  -> return CONTROL LOOP
```

任何formal non-success必须保留原identity并停止；不同target、session、attempt或world不能拼接。产品调用必须清除全部GitHub token、
`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令注入。

## 8. 当前状态与停止线

本文全部门闭合以前只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_ALLOWED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_CANDIDATE_PR436_CLOSED_UNMERGED_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_PR439_MERGED_EXACT_MAIN_PUBLIC_CI_CANCELLED_NOT_READBACK_QUALIFIED_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CI_HEADROOM_MAINTENANCE_PR440_FAILED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CI_HEADROOM_MAINTENANCE_SUCCESSOR_PR441_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_EXACT_MAIN_QUALIFICATION_RECOVERY_0_1_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后也只恢复bounded private implementation的资格，不自动冻结，不恢复global composition authority，也不选择manifest、
Evidence、persistence或public Review。新事实必须返回CONTROL LOOP；只有前提与原工程问题仍一致时，才可建立独立docs-only
implementation freeze publication。
