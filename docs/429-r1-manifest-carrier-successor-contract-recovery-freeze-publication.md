# R1 same-attempt DerivationEvidence manifest carrier successor合同恢复冻结发布

日期：2026-11-17

> 条件化状态目标：
> `R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@4b507edad080334a3958b1fc0f156f6ddd036d99`，tree
> `6bc307922a1f9b7d408d71e8d4631f3defb9089f`。
>
> 冻结对象：[文档426](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)中SHA-256
> `93e7033276e35890b8a390ec041e6bb64cc770ba0e3684900ee08f5d6a260800`的不变合同语义。
>
> 恢复边界：[reader-visible failure-boundary audit](427-r1-manifest-carrier-contract-recovery-reader-visible-failure-boundary-audit.md)与
> [public-projection correction](428-r1-manifest-carrier-contract-recovery-reader-visible-public-projection-correction.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改doc426、Schema、fixture、runtime、tests、workflow、Manifest、
> publisher、persistence、Provider、Collector、Core oracle、Verdict、global composition authority或任何frozen semantic bytes。

## 1. CONTROL LOOP与本publication的唯一职责

PR #488把doc426合入`main@72b5e95…`后，original与exact-main双门全部成功，但fresh README diagnostic发现预注册状态只在默认
折叠的`<details>`内，reader-visible marker为0。该world在formal与其余target启动前fail closed，source/readback contradiction与
64-artifact failed closeout永久保留。因此doc426的PR #488 world只能是：

```text
MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_FROZEN
```

doc427随后只资格化该失败边界，doc428只资格化最小reader-visible public projection。两者都明确禁止回填doc426或借公开投影
直接冻结合同。PR #490完成后fresh CONTROL LOOP重新核对remote exact main、开放PR、doc426–428、保留首败、全部合同输入、public
projection、authority ceiling与primary `audit.json`，没有发现击穿doc426合同语义的新反例；从doc426构造base到当前main也没有任何
`src/`、Schema、fixture、test或workflow变化。

因此当前最小合法seam不是重写doc426历史，也不是重建另一份合同内容，而是建立独立docs-only freeze publication：以doc426不变
语义bytes为冻结对象，从当前exact world重新取得本publication自己的完整资格。若最后门成立，冻结事实由本文链产生；它不把
PR #488改写成曾经资格化。

## 2. doc426失败world与doc427/428恢复world保持分离

doc426的PR #488坐标与失败identity为：

```text
base  = 663ca58054f56e8e3eada7ee2347225d0e9484e7
head  = c0fe7a218d1f60be9a1075c5837785b4ed1465db
tree  = 7f87e0e0624328168363db105237f0e84a27cad6
merge = 72b5e95ae30933d139967c94dc50f5c11c6c8a5b

source/readback contradiction = cb5a22d7a970f2a5bde22b2f9b21808cfd0a814092956a0e9f465bd158668991
failed closeout               = bccf9b2ba20793628b3d583ea135538a5c14a55302029a1b85ab3d6882035ef6
```

后继PASS只能证明自己的exact world。本文必须同时保留下列不同事实：

```text
doc426 PR #488 world = READBACK_NOT_QUALIFIED / NOT_FROZEN
doc427                = READER_VISIBLE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
doc428                = PUBLIC_PROJECTION_CORRECTION / QUALIFIED_HISTORY
doc429                = FREEZE_PUBLICATION_CANDIDATE / NOT_QUALIFIED / NOT_FROZEN
```

“doc426文档world未资格化”与“同一不变合同语义以后由doc429独立链冻结”不是同一claim。前者是不可改写历史；后者只有本文完整
资格链闭合以后才可能成为新事实。

## 3. doc428 qualification与当前exact起点

PR #490 exact identity为：

```text
base    = a8e7b096ac1820b254706ffd649957c10bdbcb27
head    = bf78c8f983f3d8b2040623e63ee0db16eff2cab6
tree    = 6bc307922a1f9b7d408d71e8d4631f3defb9089f
merge   = 4b507edad080334a3958b1fc0f156f6ddd036d99
parents = a8e7b096ac1820b254706ffd649957c10bdbcb27,
          bf78c8f983f3d8b2040623e63ee0db16eff2cab6
```

original Public CI `43909428334`、exact-main Public CI `43915289318`与Browser Smoke `43915289124`均attempt 1 SUCCESS，分别
15/15、15/15与1/1，没有rerun。original qualification、protected merge与exact-main gate seal SHA-256为：

```text
887835006b452ed0cebedeaa24587047933f5199237f14908872ad011f4452d7
36ae94e6a69fb8f3a79656a5210ae9f1333a5a57b096e87fb20c6137ece284f1
f7d25d2eb20e91e202ec4a1b207d6bcead708ef5ceb2c08ada89c5188fc073ca
```

fresh README/doc426/doc427/doc428各自唯一diagnostic为`DIAGNOSTIC_ONLY_NON_QUALIFYING / Render COMPLETE / HTTP 200 /
marker=1`，各自唯一formal为`FORMAL_READBACK_PASS / API+Render COMPLETE / HTTP 200 / marker=1 / Core PASS`。AGENTS与
milestones各自唯一raw-byte formal证明raw.githubusercontent、Contents API与exact Git逐字节一致。没有重复任何PASS。

preformal三次schema/world proof-target setup error分别以SHA-256
`9255c2af41a29b98cea7cdceae7659320bb5efbb9baec5b5362531424c3d7bcd`、
`13f836630e24362d96444e71feb3c06024a4e434e59092d6b682b89ea3507cd6`与
`45f1b948dda331b4f7e920439cee1f141993f603fb7d01b9d90581658b617622`永久保留；它们均发生在产品观察前，effect为`NONE`。
最终preformal validation、pre-observation adapter freeze与reconciliation facility freeze SHA-256为：

```text
734101cde2a45f46003408804f432e35bcee724f3e7eaaa18974e0fbd8eb8260
e8562058edb439c6d2d760d69b20d3bab807d8aa93a3c70d7d664726df21213c
cf47f247a3ab388896f674e5980d12a3cdfe834a2011c26b239847e517a17d2e
```

independent reconciliation、176-artifact closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
9adfb9752cbd34435b9e0e60ab178b07882b076dd20a535b18fe5ac42daecc80
a4570eef406f66292cb6fff910c2e63c65868cb49d06541c408f6fa8c77ad36f
6b0c09b610486e6cbe04e830ce1b25ea5a55f933371fbd9ce5d1863314aca007
6987bbce27205e698a354f8b55c6173743f266ea3831664cc528532c67a718c0
```

所以doc428现在是qualified history；本文仍须建立自己的final bytes、Plan/session/Evidence与全部门，不能继承PR #490资格。

## 4. 冻结对象与proof strength

本文若完成自己的资格链，只冻结doc426第2–12节定义的bounded successor contract：

1. `r1-derivation-evidence-manifest-carrier-successor/0.1`与public `DERIVATION_EVIDENCE / schema_version 0.3`的显式版本身份；
2. Evidence 0.3对same-attempt continuity、exact unified application admission、terminal branch与exact root binding的机械绑定；
3. `r1-derivation-manifest-snapshot-carrier/0.1` copy-owned exact snapshot、独立conformance、private admission与one-shot consumption；
4. legacy Evidence 0.2与Manifest 0.1 bytes、role/path、旧consumer与旧canonical identity保持不可重解释；
5. 五条live terminal route、negative-world qualified absence、conflict/UNKNOWN及authority ceiling保持显式；
6. producer、conformance、admission与future Manifest consumer authority继续分离。

doc426 full-file SHA-256固定为：

```text
93e7033276e35890b8a390ec041e6bb64cc770ba0e3684900ee08f5d6a260800
```

本冻结不创建`review-derivation-evidence-0.3.schema.json`、carrier runtime、Manifest 0.2、publisher、persistence、Bundle或public Review，
不恢复global composition authority，也不证明完整R1或用户工程问题已经解决。

```text
proof_is_not_problem_solving                = true
original_engineering_problem_claimed_solved = false
local_not_global                            = true
post_r1_human_ai_global_check_required      = true
global_composition_authority_restored       = false
```

## 5. 必须继续保留的non-success、setup failure与UNKNOWN

后继PASS不得删除、改名、回填或解释：

- PR #476 original Public CI failure、closed/unmerged candidate与未资格化doc415；
- PR #481 exact-main Public CI failure、0 failed Evidence Artifact与lower cause `UNKNOWN`；
- doc426 README diagnostic 0命中、contradiction、failed closeout及其未启动targets；
- doc427/428全部worktree attachment cap、PowerShell revision、Windows glob、proof-target与anonymous rate exhaustion identity；
- doc428 semantic comparator attempt 1 fail-closed记录与未重复运行的后继v2 projection；
- 本publication已经保留的control-read/reference-measure PowerShell parser、marker search Windows glob、doc426 path-search shell quoting、
  PR490 record-hash parser、wrong-worktree docs patch、proof-script replacement与worktree registration attachment-cap setup errors；
- 所有更早FAIL、ERROR、CANCELLED、setup failure与UNKNOWN。

这些identity分别属于自己的exact coordinate。相同bytes、后继PASS或同一工程目标不能把它们拼接成另一world的qualification。

## 6. 本publication的精确scope与local gates

tracked scope只允许：

```text
README.md
AGENTS.md
docs/429-r1-manifest-carrier-successor-contract-recovery-freeze-publication.md
docs/milestones.md
```

doc426–428、Schema、fixtures、runtime、tests、workflow、Provider、Collector、Core oracle、Verdict、carrier、Manifest、persistence与全部
frozen semantic bytes必须保持`4b507edad…` base bytes。

local gates至少重核exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、unique reader-visible marker、doc426
full-file hash、doc427/428 qualification hashes、PR #488 failed-world identity、successor Schema/carrier仍不存在、immutable legacy Schema/runtime
hashes、primary `audit.json` continuity与`git diff --check`。Python 3.10.6/3.13.13 × normal/`-O`必须重新执行：

- 五条live route与contract input semantic audit，四格semantic projection逐字节一致；
- doc426声明的bounded focused unchanged-runtime witness；
- read-only global/local hygiene。

测试只作witness，不能授予合同扩张、状态升级或runtime authority。

本candidate四个semantic cell均成功，versioned projection比较逐字节一致；canonical semantic SHA-256为
`0f2e1586fbe77c7c186a7d73a66d3b5a19f7bd951d5706ef7991fccfaddd0cc7`。focused四格各131/131 PASS，global/local hygiene
8/8 PASS；semantic、focused与hygiene matrix SHA-256分别为：

```text
42cafbe5682a2fccf6c8f74d408764fd0639be9c75eb2fe2a2f23f3e3a4f5615
1d7231c99cff380d5c52601e2f3d7bdce2f2521ddf2c926598d4d702f52f0563
a114ad7a1aa70ef1780e462cc6787c7e49aeaee60020d6c3d0dc9c57247f1553
```

这些只证明当前exact source没有被声明的反例击穿；仍须绑定本文final bytes、original PR与后继全部门。

## 7. 本publication自己的qualification pipeline

```text
final docs-only freeze publication bytes / declared local gates
  -> original publication PR Public CI 15/15, attempt 1, no rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc316 / doc397 / doc414 / doc419 / doc425 / doc426 / doc427 / doc428 / 本文 Render
  -> fresh AGENTS / milestones / exact legacy Schema / continuity runtime / unified admission runtime raw+API+exact-Git byte observations
  -> independent source-byte / live-route / topology / authority-ceiling / failed-world / public-projection reconciliation
  -> finite closeout and integrity
  -> target R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication的fresh Plan/session/Evidence不可复用doc426或doc428 world；diagnostic不计入资格，任何non-success必须保留原identity并停止。
产品readback必须清除全部GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令使用
`http://127.0.0.1:7897`。不得重复已有PASS或把不同world拼成一条成功链。

## 8. 当前candidate状态与停止线

本文自己的完整资格链闭合以前，只能记录：

```text
R1_M10_REPEATABILITY_FAILURE_OBSERVATION_CORRECTION_0_1_IMPLEMENTATION_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRECONTRACT_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_PR476_CLOSED_UNMERGED_ORIGINAL_PUBLIC_CI_FAILED_NOT_QUALIFIED
R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
R1_MANIFEST_CARRIER_CONTRACT_RECOVERY_READER_VISIBLE_PUBLIC_PROJECTION_CORRECTION_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_RECOVERY_PR488_WORLD_READBACK_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FREEZE_PUBLICATION_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`...CONTRACT_FROZEN` target成为新事实；doc426 PR #488失败world仍不改写。随后必须从新的exact main
返回CONTROL LOOP，独立审计private implementation feasibility、language-support persistence与剩余R1；不得按文档编号自动创建Schema、
carrier、Manifest runtime或启动R2–R6。R1完成以后必须由人类与AI共同执行独立全项目检查。
