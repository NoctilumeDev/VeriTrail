# R1 global composition authority当前状态审计

日期：2026-11-28

> 当前候选状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_CURRENT_STATE_AUDIT_CANDIDATE_NOT_QUALIFIED`。
> 本文自己的完整资格链闭合以前，不得把审计内容记为qualified history。
>
> 审计基线：`main@f0d7651ff1f03330a5d058c3ea2fa535369c5c36`，tree
> `c9da1e9453fcb05b41f415eed20c99f14ead1571`。
>
> 上游：[Manifest 0.2 private implementation successor v3候选](460-r1-review-derivation-manifest-0-2-private-implementation-successor-v3-candidate.md)与
> [Manifest 0.2 private implementation冻结发布](461-r1-review-derivation-manifest-0-2-private-implementation-freeze-publication.md)。
>
> 影响：`L0_DOCUMENTATION / CURRENT_STATE_AUDIT_ONLY`。本文不新增或修改runtime、Schema、fixture、test、workflow、
> public export、CLI、publisher、Core Verdict、persistence、HumanDisposition或任何公开产品面；它只核对当前exact world中已经冻结的
> private组件能否机械组合，以及谁拥有把它们组织成一次应用级Review的权力。

## 1. CONTROL LOOP恢复与精确世界

PR #526已经把doc461精确合入：

```text
base                 = 8b6be3a51a6ff35da9239906297be34696fce47a
head                 = 4cf12505ee6a7b7ec3661d3174141628e5f148ec
candidate/merge tree = c9da1e9453fcb05b41f415eed20c99f14ead1571
ordinary merge       = f0d7651ff1f03330a5d058c3ea2fa535369c5c36
diff                 = 1 commit / 4 files
```

三个远端门都只认original attempt，没有rerun：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #526 original Public CI | `46019810121` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `46027836695` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `46027836748` | 1 | 1/1 SUCCESS |

fresh installed-product world只认`f0d7651...`。README、doc460与doc461各有唯一qualifying anonymous Render formal；AGENTS与
milestones各有唯一qualifying anonymous raw/API/exact-Git byte observation。independent reconciliation、125-artifact finite closeout与
post-closeout integrity SHA-256依次为：

```text
589965decf5e8e4e738e3da9abb09225a872798caa56837c30fa87dc0839816f
641c7f60b6afd72c5851e57f97e61538b95e4e6e8c343c31156c83fbb3dc399e
43fae87a7f17a9cfbd75ca7ffa9bdcfd7b972db6a1071527625656ed4e5225f6
```

因此`R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FROZEN`已经生效。该事实只冻结Manifest 0.2的bounded
private producer、independent conformance、one-shot validation/admission与private staging；doc461明确没有恢复global composition
authority，也没有创建public Review产品面。本文从这个新exact main重新执行外层CONTROL LOOP，不继承“下一编号”的施工权。

## 2. 当前已冻结的局部能力

本审计重新核对以下已经各自在自己的冻结边界内成立的private能力：

1. SourceSnapshot及冻结输入digest；
2. post-terminal Fact dual-successor与normal/negative world分派；
3. typed Relation、bounded overlapping ReviewSlice与CoverageLedger；
4. application-level unified Review/Coverage output admission；
5. same-attempt DerivationEvidence continuity；
6. DerivationEvidence manifest carrier；
7. Manifest 0.2的有序role/path/raw digest/size/semantic identity、独立conformance、one-shot admission与private staging。

这些状态说明局部对象有可检验的合同和交接边界；它们不自动指定谁负责选择Provider、建立一次全局attempt、按同一world顺序调用这些
组件、封存最终应用级Artifact，或把结果公开给用户。局部冻结不是全局授权：

```text
local_components_frozen          = true
local_private_chain_composable   = true
global_application_owner_present = false
global_composition_authority     = false
public_review_product_present    = false
```

## 3. 八个live worlds的机械组合审计

审计facility在同一exact source中构造八个live worlds，并把每个world依次送入既有continuity、carrier、Manifest 0.2 candidate、
independent validation、admission与private staging。它没有新增产品入口，也没有把test helper记作authority。

| world | qualification | handoff | continuity |
| --- | --- | --- | --- |
| `NORMAL_CONSISTENT` | `NORMAL_FULFILLED` | `RELATION_HANDOFF` | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `NORMAL_BRANCH_EMPTY` | `NORMAL_FULFILLED` | `RELATION_HANDOFF` | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `NORMAL_SLICE_PARTIAL` | `NORMAL_FULFILLED` | `RELATION_HANDOFF` | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `NORMAL_RELATION_CONFLICT` | `NORMAL_FULFILLED` | `RELATION_HANDOFF` | `NORMAL_REVIEW_SLICE_COVERAGE_CONTINUITY` |
| `ZERO_PARSE_DENOMINATOR` | `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `ALL_PARSE_REJECTED` | `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `PROJECTION_BLOCKED` | `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | `NEGATIVE_WORLD_COVERAGE_CONTINUITY` |

normal world得到八项有序role；qualified negative world只得到SourceSnapshot、ReviewPolicy、DerivationProfile、
DerivationEvidence与终端CoverageLedger五项role，不伪造Fact/Relation/Slice placeholder。每个Manifest都以CoverageLedger为末项，
private staging只允许同一已验证对象使用一次。

fail-closed探针保持以下精确reason：

| 反例族 | reason |
| --- | --- |
| carrier replay | `MANIFEST_0_2_CONSTRUCTION_OPPORTUNITY_CONSUMED` |
| candidate mutation | `MANIFEST_0_2_SNAPSHOT_MUTATION_REJECTED` |
| admitted copy | `MANIFEST_0_2_ADMISSION_REJECTED` |
| unknown version | `UNKNOWN_SCHEMA_VERSION` |
| staging replay | `MANIFEST_0_2_PRIVATE_STAGING_ALREADY_USED` |

final audit script SHA-256为
`cce023e78b50ec3539652bb51f12efe26f448b3e22b78105b37c23d497c9098e`。CPython 3.10.6 / 3.13.13 × normal / `-O`
四格均exit 0，四格共同的deterministic semantic projection SHA-256为
`501fb8d39b2b4857f7c3eed5a618823d47dcf90118c1b5210a71b1e3b2d46146`。raw report SHA-256依次为：

```text
3.10 normal = 0e370d6a3d3ea8345cd0d699025e9ef51bbb51ebb9a435399fa86041f666bef2
3.10 -O     = 31a0bf620f49c68ec15aabc9f2883c801cbfc27ebe21c3d57c9b27b054e34b64
3.13 normal = 70234d78316ca24ea523fb30070af887251308a8cdf0a7f856c696e181f74c5a
3.13 -O     = f5f7c5067dacd712178d25b826e1b89116e5f2dbdb1057426d80ed51577bc2b1
```

这些witness只证明当前private bytes能够被外部审计facility按既有合同机械串接；它们不把facility本身提升为production owner。

## 4. 缺失的全局authority与产品面

exact source的静态核对得到：

- `plugins/review-attention/src/veritrail_review/__init__.py`没有公开private composition chain；
- plugin `pyproject.toml`没有声明应用级`[project.scripts]`入口；
- 当前publisher只发布SourceSnapshot，不发布Manifest 0.2或统一Review Artifact；
- production module没有一个同时导入并拥有完整private chain；完整串接只存在于bounded witness；
- 既有authority ceiling仍明确记录`global_composition_authority: false`；
- 没有公开Review命令、持久化Route或用户可消费的应用级Review结果。

因此当前真实finding是：

```text
LOCAL_PRIVATE_COMPONENTS_ARE_MECHANICALLY_COMPOSABLE_BUT_NO_GLOBAL_APPLICATION_OWNER_OR_AUTHORITY_EXISTS
```

这不是“代码已经写好，只差导出”的结论。若没有先冻结owner、输入/输出、world、停止线、失败传播、persistence与public边界，直接把
private模块接到CLI或publisher会让组合层成为新的隐性裁决器。特别是组合层可以选择Provider与采集顺序，但不能自行改变sealed proof
obligation、把证据充分性改写为PASS或生成Core Verdict。

## 5. 下一最小合法seam

本审计支持的下一最小seam仅为：

```text
DOCS_ONLY_VERSIONED_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT
```

该后继合同至少必须显式冻结：

1. 唯一global application owner及其版本化identity；
2. owner可消费的exact frozen private inputs与禁止消费的public/default旧入口；
3. normal和qualified negative world的同attempt顺序、一次性资源与failure propagation；
4. Provider选择、任务编排与Core充分性/Verdict之间的权威隔离；
5. application-level Artifact、Manifest、Coverage、provenance与persistence的exact handoff；
6. public Review尚未开始时的export/CLI/publisher停止线；
7. composition replay、cross-world splice、partial success、late mutation、foreign context、unknown version与resource cleanup反例；
8. 后继private implementation的最小授权、资格门与不得自动进入public product的停止线。

本文不预写该合同的最终字段，不授权实现，也不把“全局最优产品愿景”当成当前施工authority。后继必须从本文资格化后的新exact main
重新执行CONTROL LOOP并建立独立docs-only candidate。

## 6. 必须保留的non-success

本轮后继PASS不得删除、覆盖、改名或重解释：

- audit attempt 1中mutation probe错误地修改已验证对象，normal cells得到`AssertionError`；同一script使用Python `assert`，使两个
  `-O` cells形成false-PASS-shaped输出。script SHA-256为
  `6a5b928fb5fd7aaf31ed3349178d7e9307f8cbede7d00a94937c9ed74849539f`；四格全部`NON_QUALIFYING / EFFECT_NONE`；
- audit attempt 2四格均PASS，但报告只含attempt-local raw digest，没有建立跨Python/optimization共同semantic projection；script
  SHA-256为`ed0869ae524938ae90a6317bb93f48d6e5e878019378757c850fdf105ac55ad9`，只作proof-target gap历史；
- managed worktree已经按exact ref创建，但Codex侧栏注册因thread超过100个attachment identity失败；checkout本身有效；
- 首次exact-coordinate PowerShell命令未引用`HEAD^{tree}`、Windows `rg` wildcard、PowerShell `$f:`插值三个setup error；
- doc461及此前全部FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`，尤其PR #519 original required failure、PR #525第一套
  readback topology错误与PR #526闭合期间保留的所有non-success。

attempt 1/2不能由attempt 3倒推为PASS。它们没有建立产品失败，也没有修改exact source world。primary
`C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 7. 本candidate的资格责任

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc460/461、runtime、Schema、fixture、
test、workflow、oracle、public export、CLI、publisher与primary `audit.json`必须保持base不变。

本层local gates至少重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. exact base/head/tree、PR #526 original/protected/exact-main gate与fresh readback continuity；
3. audit attempt 1/2/3 identities、script hashes、四格semantic projection、八world与五类fail-closed reason；
4. public export、entry point、publisher、production import graph与authority ceiling静态断言；
5. Python 3.10.6 / 3.13.13 × normal / `-O`的bounded docs/roster witness；
6. `git diff --check`、global/local hygiene与primary `audit.json` continuity；
7. original audit PR gate只认本candidate exact head/tree/attempt；
8. protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
9. fresh anonymous installed-product README/doc461/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
10. independent source/finding/retained-failure/readback reconciliation与finite closeout。

任何non-success必须保留原identity并停止；不得rerun until PASS、弱化oracle、修改冻结历史或复用旧world的PASS。

## 8. Candidate qualification pipeline与停止线

```text
audit final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original audit PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc461 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observation
  -> independent source / finding / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> target CURRENT_STATE_AUDITED / QUALIFIED_HISTORY becomes effective
  -> return CONTROL LOOP for a separate versioned global composition authority contract
```

本文进入仓库不等于审计资格成立。在自己的完整资格链闭合以前只能记录：

```text
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_CURRENT_STATE_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文成为`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。随后必须从新的exact main返回CONTROL LOOP，另建docs-only
versioned global composition authority contract；不得直接修改runtime、公开private模块、启动public Review、R2–R6或R1后的human+AI
全项目检查。
