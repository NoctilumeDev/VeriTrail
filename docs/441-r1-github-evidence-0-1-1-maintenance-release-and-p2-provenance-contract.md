# R1 GitHub Evidence 0.1.1 维护发行与 P2 provenance 对齐合同

日期：2026-11-20

> 当前状态：
> `GITHUB_EVIDENCE_0_1_1_MAINTENANCE_RELEASE_AND_P2_PROVENANCE_ALIGNMENT_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 精确基线：`main@75dd9a5a77fc171420d78f2a90c86ecc3bfebc88`，tree
> `427c4400dd0e65d1e65fb38f3e2b6093a5be85f6`。
>
> 上游：[P2 合同](89-p2-public-render-collector-contract.md)、[0.1.0 发行合同](96-p4-github-evidence-release-contract.md)、
> [0.1.0 公开读回事实](108-p4-github-evidence-release-readback-facts.md)、
> [owned-browser 生命周期修正合同](438-r1-public-render-owned-browser-lifecycle-correction-contract.md)、
> [实现候选](439-r1-public-render-owned-browser-lifecycle-correction-implementation-candidate.md)与
> [source 冻结发布](440-r1-public-render-owned-browser-lifecycle-correction-implementation-freeze-publication.md)。
>
> 影响层级：`L2_PUBLIC_DISTRIBUTION_CONTRACT + BOUNDED_L1_PROVENANCE_ALIGNMENT_CONTRACT`。
> 本文是 docs-only 合同；它不修改 runtime、tests、Schema、fact/coverage/Core/P3/R1 语义，不创建 tag、Release
> 或资产，也不恢复 doc437、Manifest 0.2、global composition 或 R2–R6 authority。

## 1. CONTROL LOOP 为什么不能直接重做 doc437

PR #502 已把 doc440 以如下身份精确合入：

```text
base                 = 36edc5119a41573be95cc3fd7c4fd0e8ff307cc7
head                 = 824e8bccc310b1a02d2b887aba8a12d0a157a688
candidate/merge tree = 427c4400dd0e65d1e65fb38f3e2b6093a5be85f6
ordinary merge       = 75dd9a5a77fc171420d78f2a90c86ecc3bfebc88
diff                 = 1 commit / 4 files
```

原始与 exact-main 门均只认 attempt 1：

| 门 | Run | 结果 |
| --- | ---: | --- |
| #502 original Public CI | `44618225861` | 15/15 SUCCESS |
| exact-main Public CI | `44625769930` | 15/15 SUCCESS |
| exact-main Browser Smoke | `44625769739` | 1/1 SUCCESS |

fresh detached exact-main world 从 source 重建 Core 0.13.0 与 GitHub Evidence 0.1.1.dev0 wheel。唯一 negative
lifecycle formal 在 5.029 秒内返回；driver terminal、owned process residue 为空，预期 transport-close failures 与
`playwright-driver:deadline-terminated` 保持可见，且没有声称 Render 内容成功。P1 API 及
README/doc437/doc438/doc439/doc440/milestones raw/API/exact-Git bytes 各有唯一 PASS。independent
reconciliation、59-artifact finite closeout 与 post-closeout integrity SHA-256 依次为：

```text
5a0334b0a742b302815dd0dd54096f482ab38363a4466009434b2a296e8834bd
4b07b2930e53ff1a3699e9aef3ca155e1adab3d52b97c9566120358c47f3e8d5
4a59af90de34e82082ea908680b206f3dce5d61b6a9be7939165aec993fe3ce0
```

因此只有 source 状态已经生效：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
```

公开 `github-evidence-v0.1.0` wheel/sdist 仍是不可移动的旧产品字节，不含该修正。doc437 的失败 formal
消费的是公开 installed product；exact-source PASS 不能替代 public distribution identity。直接重做 doc437 会把两个
world 拼接起来，直接进入 Manifest 0.2 又会把尚未恢复的产品观察面当成已恢复前提。

所以当前最小合法 seam 只能先冻结 0.1.1 维护发行及其 provenance 对齐合同。合同闭合仍不等于发行完成；发行完成也
不等于 doc437 已经通过自己的 fresh Plan/session/readback。

## 2. 当前公开坐标与不可移动历史

2026-11-20 的新鲜 GitHub API 观察确认：

- `github-evidence-v0.1.0` 仍是 annotated tag，tag object
  `bdc417058622732a00571eb4c39dc6a758d37b72`；
- Release `385275245` 仍是 non-draft、non-prerelease，`immutable=false`，四项资产及 digest 与
  [文档108](108-p4-github-evidence-release-readback-facts.md)一致；
- ruleset `22613490` 仍 active，include 为 `refs/tags/github-evidence-v*`，禁止 deletion 与
  non-fast-forward，无 bypass；
- `github-evidence-v0.1.1` tag 与 Release 均不存在；
- `releases/latest` 仍指向 Core `v0.13.0`，Release ID `385190618`。

这些是当前外部观察，不是未来发行资格。创建 0.1.1 tag 前必须重新观察全部坐标；任何漂移先保留并停止，不能把本文
的观察当成永久承诺。0.1.0 tag、Release、四项资产、validation summary、checksum 与历史读回不得移动、删除、替换或重制。

## 3. 发行前发现的 P2 provenance 缺口

P0/P2 冻结边界明确区分 facts identity 与 Evidence provenance：实现版本改变但规范化含义不变时，
`facts_digest` 可以保持，具体 Evidence 必须通过 provenance 继续可区分。P2 合同还把浏览器/API/解析器版本列为
provenance，并要求浏览器实现版本变化不得污染 facts digest。

当前 exact source 同时存在：

```text
distribution version                              = 0.1.1.dev0
veritrail_github.__version__                      = 0.1.1.dev0
GitHub API COLLECTOR_IMPLEMENTATION_VERSION       = 0.1.1.dev0
P2 PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION = 0.1.0
```

owned-browser lifecycle 已改变 P2 production implementation，但新 Evidence 仍把 P2 `collector_version` 写成 `0.1.0`。
这不是 normalization semantics 变化，也不推翻已证明的 cleanup 行为；它是发行前必须显式处理的 provenance identity
缺口。若直接发布 0.1.1，修正前后的 P2 implementation 不能由该字段区分，会违反已冻结的 provenance/fact 分离原则。

本文不静默改源码，也不把缺口扩大成 P1/P2 facts、Schema 或 Core 缺陷。后继 release-preparation 只允许把最终
distribution/import/API/P2 implementation provenance 同步为 `0.1.1`，并新增直接测试证明：

```text
implementation version change -> Evidence artifact identity may change
implementation version change -/-> facts_digest change
normalization_semantics_version remains github-public-render-facts/0.1
```

若实现审查证明上述对齐需要改变 facts、coverage、normalization、request、P3 handoff 或 Core Verdict，立即停止并重新进入
CONTROL LOOP；本文不授权这种扩张。

## 4. 0.1.1 固定产品坐标

后继发行准备只能形成：

| 字段 | 固定值 |
| --- | --- |
| Python distribution | `veritrail-github-evidence` |
| Import package | `veritrail_github` |
| Final version | `0.1.1` |
| Annotated tag | `github-evidence-v0.1.1` |
| GitHub Release name | `VeriTrail GitHub Evidence Plugin 0.1.1` |
| Core dependency | `veritrail==0.13.0` |
| Python declaration | `>=3.10` |
| Verified Python series | CPython `3.10` 与 `3.13` |
| Render extra | `playwright==1.62.0`，matching bundled Chromium 由 operator 显式安装 |
| Channel | GitHub Release only；不发布 PyPI |
| Latest policy | non-Latest；Core `v0.13.0` 的 Latest 身份不得漂移 |

`pyproject.toml`、`veritrail_github.__version__`、API/P2 implementation provenance、wheel/sdist METADATA 与
`importlib.metadata.version()` 必须共同读回 `0.1.1`。source/fact Schema、Evidence type、normalization semantics、P3
handoff 与 Core dependency 不随 patch release 改变。

允许的 release-preparation source surface 只限：

1. 上述 final version/provenance 常量及相应直接回归测试；
2. 既有 `github_evidence_release_assets.py` 与真实 P4 acceptance 工具从 0.1.0 泛化/升级到 0.1.1；
3. plugin README、release candidate/facts 文档及固定资产生成所需的窄发布元数据；
4. 不改变 doc438/439/440 冻结 blob 所证明的 browser lifecycle 行为。

若需要修改 `public_render_browser.py` 的生命周期逻辑、45 秒窗口、5 秒 release envelope、network/body budget 或任何
frozen semantic byte，release-preparation 必须停止；不能把产品修正伪装成打包工作。

## 5. 固定资产与非自指顺序

0.1.1 Release 上传资产精确为：

```text
veritrail_github_evidence-0.1.1-py3-none-any.whl
veritrail_github_evidence-0.1.1.tar.gz
github-evidence-v0.1.1-validation-summary.json
SHA256SUMS-github-evidence.txt
```

固定顺序继续沿用已冻结的非自指规则：

```text
wheel + sdist
    -> validation summary
    -> SHA256SUMS (wheel + sdist + summary)
    -> external release facts bind all four asset digests
```

validation summary 必须在 tag 前关闭，只能声明
`RELEASE_CANDIDATE / PUBLIC_GATES_GREEN / PRE_TAG / NO_PUBLIC_DOWNLOAD_CLAIM`；不得包含自身 size/digest、未来 tag
object、Release ID、匿名下载或最终冻结状态。checksum 不列自身摘要。最终公开事实由后继 docs-only publication 保存，不得
事后重制 summary 洗掉时间顺序。

候选与最终资产都必须从各自 exact clean detached main 重建。PR artifact、doc440 readback wheel、旧 0.1.0 staging 与任何
本地候选字节都不得复用为最终公开资产。

## 6. 发行准备、发布与 installed-product 门

合同闭合后，release-preparation candidate 仍须从新的 exact main 独立取得：

1. exact final source scope、version/provenance 对齐测试与 frozen lifecycle blob continuity；
2. Core 与插件在 Python 3.10.6 / 3.13.13 × normal / `-O` 的声明矩阵；
3. 两次独立 wheel/sdist 构建与内容/metadata 比较；若不能证明逐字节相同，只能报告 content-equivalent；
4. base wheel、sdist、render extra、matching Chromium、`pip check` 与 plugin uninstall 后 Core-only 复算；
5. 正常 P1 -> P2 -> P3 真实 GitHub 链，以及冻结的 blocked-cleanup negative lifecycle：deadline 后 bounded return、
   driver terminal、owned process-tree 零残留、cleanup errors 全部可见且不冒充内容成功；
6. original PR attempt、protected exact-head merge 与新 exact-main Public CI + Browser Smoke；
7. tag/ruleset/Latest/0.1.0 immutable history 的 fresh pre-tag 核账。

只有 release-preparation exact-main 门成立后，才可从该新 exact main 重建最终四项资产，随后严格串行：

```text
recheck active github-evidence-v* protection
  -> create protected annotated github-evidence-v0.1.1 tag
  -> create non-Latest draft Release
  -> upload exact fixed asset set
  -> authenticated metadata/digest/asset-set check
  -> publish non-draft / non-prerelease / non-Latest
  -> fresh anonymous Release/API/asset download readback
  -> downloaded wheel/sdist dual-Python clean-install/runtime/uninstall matrix
  -> docs-only release facts publication
  -> its own gates / protected merge / exact-main readback
```

任何公开失败沿用文档96的恢复语义：tag 不移动；已公开资产不静默覆盖/删除；必要修复使用新 patch version。GitHub
API、Release 页面与下载仍在同一平台信任域，不得描述为独立真实性权威。

下载产品必须证明 `collector_version=0.1.1` 只改变 Evidence provenance、不改变同事实的 `facts_digest`。同时必须在
fresh anonymous product world 重现正常 P2 与 blocked-cleanup negative lifecycle。该发行读回只资格化 0.1.1 产品坐标，不能复用为
doc437 的 Plan/session/formal；doc437 recovery 必须在发行闭合后从新的 CONTROL LOOP 另建唯一 fresh formal。

## 7. 保留的失败与停止线

以下 identity 永久保留：

- PR #498 picomatch required audit FAILURE、dependent SKIPPED、closed/unmerged/no-rerun world；
- doc437 P1 COMPLETE 后 P2 navigation ERROR、45 秒后长期 cleanup 阻塞、外部 containment 与 lower cause `UNKNOWN`；
- doc439 wheel probe `poll()` proof-facility ERROR 与过窄 cleanup oracle FAIL；
- doc440/#502 全部 setup/capture errors，包括 first fresh root、PowerShell tree/path/filename/quoting、exec-wrapper stdout
  capture missing；
- 0.1.0 immutable public history、早期 P4 HTTP 500/timeout、环境坐标与包装层 errors；
- 所有更早 FAIL、ERROR、CANCELLED、setup failure 与 `UNKNOWN`。

任一条件触发即停止：

- candidate 不再绑定新的 protected exact main，或混入无关 Dependabot/其他 PR；
- provenance 对齐需要改变事实或 normalization semantics；
- `github-evidence-v0.1.1` 已意外存在、ruleset 失效或 tag 不能 peel 到唯一发布提交；
- version、dependency、asset set、summary/checksum 顺序或 non-Latest 约束漂移；
- 任一 required gate、真实 Chromium、negative lifecycle、clean install、uninstall 或 residue 门失败；
- public asset digest 与 final staging/anonymous download 不同；
- 尝试以发行 PASS 回填 doc437、#498、Manifest 0.2 或 global composition。

## 8. 本 docs-only 合同自己的资格链

本 patch 只允许修改 `README.md`、`AGENTS.md`、`docs/milestones.md` 并新增本文。runtime、tests、workflow、lock、
release scripts、Schema、Collector、public export 与全部 frozen semantic bytes保持 base 不变。

本层 local gates 必须重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings 与 required markers；
2. doc89/doc96/doc108/doc437–440、#498–#502、source-freeze evidence 与 live public identity continuity；
3. Python 3.10.6 / 3.13.13 × normal / `-O` documentation/Markdown/hygiene bounded witness；
4. `git diff --check`、global/local hygiene、forbidden source/public export change 与 primary `audit.json` continuity；
5. original contract PR 只认本 candidate exact base/head/tree/attempt；
6. protected merge 后只认新 merge SHA 与 new exact-main Public CI 15/15 + Browser Smoke 1/1；
7. fresh installed P1 API 与 README/doc440/本文/milestones raw/API/exact-Git byte observations；公开 0.1.0 的未修正
   P2 不能冒充本合同完整性门；
8. independent source/public-coordinate/readback/retained-history reconciliation 与 finite closeout。

任何 non-success 保留原 identity 并停止；不得 rerun until PASS、弱化 oracle、修改 frozen history 或复用旧 PASS。

全部门闭合后最多生效：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_RELEASE_AND_P2_PROVENANCE_ALIGNMENT_CONTRACT_0_1_FROZEN
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_ALLOWED_NOT_STARTED
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回 CONTROL LOOP，从新的 exact main 重建 release-preparation candidate；不得在本合同 PR 中顺带改版本、脚本、
runtime 或创建 tag/Release。`proof_is_not_problem_solving = true`、`local_not_global = true`；R1 完成后的 human + AI
全项目检查仍是独立后续目标。
