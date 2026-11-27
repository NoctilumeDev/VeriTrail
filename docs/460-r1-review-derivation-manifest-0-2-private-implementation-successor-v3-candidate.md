# R1 Review Derivation Manifest 0.2 private implementation successor v3候选

日期：2026-11-27

> 候选状态：
> `R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_V3_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造基线：`main@5c784b0994db00b9ee9e4807855f4c05a9e5fee6`，tree
> `b774532bba933b5000cce3ecc429eeb38e172c70`。
>
> 上游：[Manifest 0.2冻结合同](316-r1-review-derivation-manifest-negative-world-successor-contract.md)、
> [private implementation授权](448-r1-review-derivation-manifest-0-2-private-implementation-authorization-publication.md)、
> [PR #519失败边界](456-r1-review-derivation-manifest-0-2-core-regression-binding-failure-boundary.md)与
> [versioned schema roster binding修正实现冻结发布](459-r1-review-derivation-manifest-0-2-versioned-schema-roster-binding-correction-implementation-freeze-publication.md)。
>
> 影响：`L2_BOUNDED_PRIVATE_IMPLEMENTATION / SCHEMA / FIXTURE / TESTS / CANDIDATE_DOCUMENTATION`。本文不创建public
> Bundle、Evidence、CLI、Workbench route、tag、Release、Core Verdict、HumanDisposition、persistence Route A/B或global
> composition authority，也不启动public Review或R2–R6。

## 1. CONTROL LOOP、精确世界与不继承资格

PR #524已经把doc459精确合入当前构造基线；original Public CI `45960488588`、exact-main Public CI
`45966330464`与Browser Smoke `45966330476`均为attempt 1 SUCCESS（15/15、15/15、1/1）。fresh
README/doc458/doc459/AGENTS/milestones各有唯一qualifying PASS；independent reconciliation、143-artifact closeout与finite
integrity SHA-256依次为：

```text
291758c7f00dddf195f67fcfd4a44e79891f2b9265caf238ded8b2c322f75ed7
b43fc6e1b4110213109512e3db51227c06ae72f99baf3f102c6d13541b862d00
4104dd1c337ce5da3e162dc1c4c005c69922df72a56d71cc8085b813dc8f4347
```

因此`R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_FROZEN`已经生效。
fresh CONTROL LOOP从该exact main重新读取doc316、doc448、doc459、carrier/source、Schema roster与保留失败，只允许在doc448
bounded A–J ceiling内重建Manifest 0.2 private implementation successor。

本候选机械重建PR #519未合并产品字节并加入已经冻结的versioned roster test-support修正，但不继承PR #519、PR #523或PR #524的
qualification。PR #519仍绑定：

```text
base = 9d2a76e6edb3237946dd56806602a894fc70e028
head = f5eff36f3a0d37a97b0d0d1e8a39f64cce76d2d6
tree = 36620b3471acb72a224321af83d2ee5496697380
run  = 45068502183 / attempt 1 / required FAILURE / closed / unmerged / no rerun
```

两个required Python jobs中相同的RAE-017 roster失败、后继SKIPPED与关闭未合并identity永久保留。v3的重新构造记录PASS SHA-256为
`f4417d8101bb6e5646b2b0be57ac690207996eaf86074b6a2f346312cd7db3cf`，但机械同字节只建立来源连续性，qualification effect为
`NONE`。

## 2. 候选exact scope与bounded实现

候选只允许以下11-file scope：

```text
README.md
AGENTS.md
docs/460-r1-review-derivation-manifest-0-2-private-implementation-successor-v3-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_review_derivation_manifest_0_2.py
plugins/review-attention/src/veritrail_review/_review_derivation_manifest_0_2_conformance.py
plugins/review-attention/tests/test_review_derivation_manifest_0_2.py
schemas/review-derivation-manifest-0.2.schema.json
tests/fixtures/review-derivation-manifest-0.2/compatibility-cases.json
tests/test_review_derivation_manifest_0_2.py
tests/test_review_r1_schema_payload.py
```

`tests/test_review_r1_admission_evidence_schema.py`已经在base中冻结，本候选不得再次修改。产品与focused witness的final SHA-256为：

| 对象 | bytes | SHA-256 |
| --- | ---: | --- |
| private producer / one-shot admission | 21771 | `2960da3f6dd511d8da8aed1629a40dcea36adc4de8e461e83292e341b1db1985` |
| independent conformance | 31221 | `a059f1967c9ae08854523f9d0d6b2d2a26799dbb43d00e7fc309fe9ed01b6cec` |
| plugin focused tests | 33845 | `cabe5a7ffc4288124cf3ca9fdf67b501aad03895649eb595037189a8a8a1bad8` |
| Manifest 0.2 Schema | 8839 | `fd37bc4085999dea64715fb7e72073c20d08c3c7ce14b9c2e3fd04895b7a4fa7` |
| compatibility fixture | 4062 | `477d838d06839400f29c1c6c6bf6d088f9bb7245326072c688ba9f8939a17ad7` |
| root Schema tests | 7762 | `231bdc51a9a9391d899a1b464f3d1a07c5a90d0b1da1565fdb268fffcd2e84b5` |
| R1 payload roster witness | 48059 | `1a2d1e1d0137cb2e0f5226264d9f19f6c12058b6e16c44ca965fbea45d76e5b1` |

实现保持doc448 A–J：exact 0.2 dispatch；copy-owned same-attempt carrier snapshot；五到八项有序role/path/raw digest/size/semantic
identity；CoverageLedger 0.3恰为末项；absence/unknown不造placeholder；独立conformance不导入producer projector；validation与private
staging共用one-shot claim；success/failure/replay/foreign context/late mutation/race全部fail closed；八个live worlds、compatibility positive
universe与`RDMC-000..013`均有独立witness。Manifest 0.1 bytes、carrier frozen bytes、既有Provider、public/default composition与
Core Verdict均不变。

## 3. prequalification反例与最小修正

formal qualification以前的完整diff review没有把最初21/21 PASS当成充分证明，而是得到三个真实反例：

1. `PREQUAL-MANIFEST-001`：validation report中的`derivation_evidence_digest`没有绑定实际`DERIVATION_EVIDENCE`字节；
   attempt 1错误接受，SHA-256 `6cfa5ea7e538a1bd3d406fe0850da0ccb04ca2b0b2422ba006d294ede0c48875`；最小修正后
   attempt 2拒绝，SHA-256 `c0f3f8377962489d2b2caae509cf244852f8c6133263cafe16a1b3f919f963e9`。
2. `PREQUAL-MANIFEST-002`：CoverageLedger 0.3只做root/topology检查，没有独立执行closed child shape；attempt 1错误接受，
   SHA-256 `66c21214f35676cedd19de55b9f118e3b04594f5b870b763fa6e1ed0d1ac2641`；最小closed-shape修正后attempt 2拒绝，
   SHA-256 `975eca2814f55d8c95b35564be45a870e34e23cfd62f16cf57f1a68f47545bb6`。
3. `PREQUAL-MANIFEST-003`：SourceSnapshot、ReviewPolicy与DerivationProfile的内部digest没有独立复算；attempt 1错误接受，
   SHA-256 `c47eca8ec5299737cce2e941ef382fa11f1a9272791d1073f614b694bdfffefd`；复用各artifact现有private validator并绑定
   Evidence input digests后attempt 2拒绝，SHA-256 `f27ac6aa064fff9029e7b62f5f7cb38e4ddc90d94c60febc096b03b9f19fa774`。

最后的窄审查还把Evidence `coverage_ledger_digest`与`root_chain_digest`绑定实际Ledger值；既有`RDMC-012`内新增正反向subtests，
没有扩大frozen denominator。targeted final binding witness 2/2 PASS，result/log SHA-256分别为
`2f37bed1a5397297bbd48d0d5e68d113ee2324e1c089529f426dc22c012c2154`与
`3f5ff895cf38e690b8a6188c92484eb6302fe5a45dbab73ac57bad1f6cd2732a`。

这些反例都在formal attempt 3 seal以前发现并保留，没有失败的正式产品run可被后继PASS覆盖。修正后的prequalification 21/21 PASS，
result/log SHA-256为`b762248286fc4b1f99bcae2a7fa61daf7595c0d5e67831fb170168c1249908e0`与
`363c39daec30215a4c9ab337c685c81239be19bcb0879ba5544408b3b3274efc`；qualification effect仍为`NONE`。

## 4. final local qualification attempt 3

formal attempt 3只认输入seal
`f1465e847f99f56afc15005cdf2f87fe270be6e08f5228655ae3143f113b436e`。CPython 3.10.6 / 3.13.13 × normal /
`-O`的final结果如下：

| 门 | 每格结果 | summary SHA-256 |
| --- | --- | --- |
| compile | 4/4 PASS | `1fa426f2b62fae7c0cffab06ff47fb7e0831753ff62fe5c86f51e0a36a6e731e` |
| Core versioned roster | 9/9 PASS | `56af65941956d9e2f33c04eb79b4f835076619c3971b28fba5b476282c77ddb1` |
| root/payload | 27/27 PASS | `2bc778a58bbb91260fb0405a9650d9733f120745fbfbf04cc9162b1f649376f0` |
| focused Manifest | 26/26 PASS | `c19d44549a835b22955848efef13466751a68c85465905de7836ed54da8bbf6c` |
| full Review Attention | 715 reported；3.10为712 passed/3 skipped；3.13为713 passed/2 skipped | `b461f868fd62c3376d77079daf05d8be2412969e5274797dbbcb7f8d3858945a` |

四格full matrix分别用时约2124、2128、1730与1724秒。PASS只证明这组final bytes没有被声明的witness击穿，不把candidate升级为
qualified/frozen，也不证明global composition或最终用户工程问题已经解决。

```text
proof_is_not_problem_solving           = true
local_not_global                       = true
post_r1_human_ai_global_check_required = true
global_composition_authority_restored  = false
```

## 5. 必须继续保留的non-success

后继PASS不得删除、覆盖、改名或解释以下identity：

- PR #519 run `45068502183` attempt 1的两个required Core regression FAILURE、四个downstream SKIPPED、closed/unmerged/no-rerun；
- prequalification三个真实反例的attempt 1错误接受与attempt 2拒绝；
- formal full matrix attempt 1在结果形成前取消，cancellation SHA-256
  `b32867ac748e90964ad3ba42556c6896a1f208b668d1c4bb942a7088ea048613`；
- formal full matrix attempt 2在第二个真实反例出现后取消，cancellation SHA-256
  `0732cf2e01209a627bab1d8677366dcc91fb1be00f3c40cbd17e89fa8e769d21`；
- managed worktree注册与Codex侧栏挂载超过100个attachment identity的两个setup error；
- `apply_patch`相对cwd误投、Windows absolute wildcard error 123、PowerShell hash ParserError与doc316错误文件名查询setup errors；
- #524及全部更早的FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`。

误投到另一checkout的六个未跟踪副本只在确认没有proof owner且exact bytes已经进入本候选后删除；正式evidence root、#519失败root与全部
身份记录继续保留。primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 6. 本候选的完整资格责任

本候选尚未取得PR或exact-main资格。最终文档字节形成后必须重新执行exact 11-file scope、UTF-8 without BOM、LF/final LF、links、
fences/headings、required markers、product SHA、formal seal continuity、`git diff --check`、global/local hygiene与primary audit continuity；
随后形成不可变单一commit与PR body seal。

```text
candidate final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original PR Public CI 15/15 attempt 1 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / 本文 / milestones readback
  -> fresh AGENTS raw/API/exact-Git byte observation where declared
  -> independent source / contract / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
  -> return CONTROL LOOP
```

每个formal identity只运行一次；已PASS目标不得重复。fresh product readback必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。任何non-success保留原identity并停止，不得rerun until PASS、弱化Oracle、
拼接不同world或用后继PASS回填首败。

## 7. authority ceiling与当前停止线

本候选进入仓库、local PASS或PR绿灯都不使实现冻结。自己的完整资格链闭合以后也最多只能成为：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_VERSIONED_SCHEMA_ROSTER_BINDING_CORRECTION_IMPLEMENTATION_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_SUCCESSOR_V3_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回CONTROL LOOP，建立独立docs-only implementation freeze publication并完成其local/original PR/protected merge/new exact-main
双门/fresh installed-product readback/independent reconciliation/finite closeout。该独立publication全部门闭合后，才可使
`R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FROZEN`生效；然后再次返回CONTROL LOOP审计global composition的下一最小
合法seam。本文不授权直接恢复global composition、启动public Review、R2–R6或R1完成后的human+AI全项目检查。
