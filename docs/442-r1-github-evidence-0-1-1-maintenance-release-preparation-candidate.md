# R1 GitHub Evidence 0.1.1 维护发行准备候选

日期：2026-11-20

> 当前状态：
> `GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_FINAL_SUCCESSOR_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NO_TAG_NO_RELEASE`。
>
> 精确基线：`main@8493c6240fda4c6435198fe37d39ab51a56a95cd`，tree
> `33eb2966daf2f65272be964b4bb5ddf51eb35689`。
>
> 冻结上游：[维护发行与 P2 provenance 对齐合同](441-r1-github-evidence-0-1-1-maintenance-release-and-p2-provenance-contract.md)、
> [owned-browser 生命周期实现冻结发布](440-r1-public-render-owned-browser-lifecycle-correction-implementation-freeze-publication.md)、
> [P2 合同](89-p2-public-render-collector-contract.md)与
> [0.1.0 公开读回事实](108-p4-github-evidence-release-readback-facts.md)。
>
> 影响层级：`BOUNDED_L1_PROVENANCE_ALIGNMENT_IMPLEMENTATION + L2_RELEASE_PREPARATION_CANDIDATE`。
> 本候选不创建 tag、Release 或公开资产，不恢复 doc437、Manifest 0.2、global composition 或 R2–R6 authority。

## 1. CONTROL LOOP 输入与最小授权

PR #503 把 doc441 以如下身份精确合入：

```text
base                 = 75dd9a5a77fc171420d78f2a90c86ecc3bfebc88
head                 = 4cb0c760a1b607fa6067291ff8cd7fa9852b1fc5
candidate/merge tree = 33eb2966daf2f65272be964b4bb5ddf51eb35689
ordinary merge       = 8493c6240fda4c6435198fe37d39ab51a56a95cd
diff                 = 1 commit / 4 files
```

原始与 exact-main 门只认各自 attempt 1：

| 门 | Run | 结果 |
| --- | ---: | --- |
| #503 original Public CI | `44638243231` | 15/15 SUCCESS |
| exact-main Public CI | `44643445192` | 15/15 SUCCESS |
| exact-main Browser Smoke | `44643445263` | 1/1 SUCCESS |

fresh detached exact-main world 从 exact source 构建 Core 0.13.0 与 GitHub Evidence 0.1.1.dev0 wheel。installed P1 API
以及 README/doc440/doc441/milestones raw/API/exact-Git bytes 各有唯一 PASS。anonymous rate/preflight 的不同代理出口配额
视图与两个本轮 PowerShell proof-facility setup error均按原 identity 保留；没有 formal 被覆盖或重复。independent reconciliation、
62-artifact finite closeout 与 post-closeout integrity SHA-256 依次为：

```text
7251cc136abe593792068974b1a2d7bfdfc324cf2ea5b500a3ebe16b4314f2d0
a46b59e2e1a116c18eb52f085e7fbb260495cf86ccc106b3d48ca86f8643b7d4
82eb2ffa5934ffe5d8626fd5f385cce133487cfab8d53e85d03218589f74dbb8
```

因此现在生效的是：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_RELEASE_AND_P2_PROVENANCE_ALIGNMENT_CONTRACT_0_1_FROZEN
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_ALLOWED
```

授权只覆盖新的 release-preparation candidate。合同冻结不是 public Release；public 0.1.0 仍是不含 lifecycle 修正的不可移动
历史产品，doc437 的 installed-product failure 也仍未恢复。

### 1.1 PR #504 原始门失败与最小 successor

首次候选固定为：

```text
base = 8493c6240fda4c6435198fe37d39ab51a56a95cd
head = e3eb07ab67e047939be5f3d01ea711f4f458f44f
tree = 51f878fb7771120144a4f8405c2885227b52134a
diff = 1 commit / 15 files
```

PR #504 original Public CI `44674570733` attempt 1 的13个job成功，但Python 3.10与3.13两个
`GitHub Evidence wheel-only` job失败。两条链都成功构建并安装
`veritrail_github_evidence-0.1.1-py3-none-any.whl`，随后被`.github/workflows/ci.yml`中仍要求
`__version__ == '0.1.1.dev0'`的旧exact acceptance binding拒绝。失败job为`136098185965`与
`136098186028`，原始日志SHA-256依次为：

```text
a292a91cf502cdd10b7678a1801f04eb1c54a77579efbf8f80475831e3cf9912
e84c4768735da63333a791f00c650a894473b247a039434bb3f042b3970d147a
```

这是真实的candidate scope completeness / CI acceptance binding缺陷，不是wheel下载、Python兼容或runtime行为反例。
#504已经关闭且未合并，禁止rerun洗白。successor仍从同一exact main重建，只新增把wheel-only exact import-version
oracle同步为`0.1.1`及其直接回归；不得把oracle泛化为仅比较两个动态来源相等，也不得扩张任何frozen semantic边界。

### 1.2 首个本地 successor 的发行门基数反例

首个本地 successor 已固定为：

```text
base = 8493c6240fda4c6435198fe37d39ab51a56a95cd
head = 2f61c0051c3a87320bd6804ebf62e17502fc9b3d
tree = 77b20b8d7c9d736742fe1f378fecd0084f39fa52
diff = 1 commit / 16 files
```

该候选的双 Python source matrix、双构建、base/sdist/render与blocked-cleanup负链已经形成PASS witness；匿名formal开始前的
独立合同复核又发现`github_evidence_release_assets.py`仍把validation facts中的Public CI job数固定为历史`11`，而doc441、
本文件及当前workflow都要求new exact-main Public CI `15/15`。因此一个真实15-job PASS会在最终资产finalize时被拒绝。
这是pre-PR release-tool gate-cardinality binding defect；`2f61c005...`没有推送、没有PR且不具资格，既有PASS只属于该失败候选。

final successor仍从同一exact main重建，只把validator与测试fixture同步为精确`15`，并增加旧`11`必须被拒绝的回归。不得把job数
检查改为动态或宽松比较；final successor必须重做全部local、original PR、protected merge、new exact-main与fresh product资格链。

## 2. 候选改动的有界范围

基线中四个实现/发行坐标并不一致：

```text
distribution version                              = 0.1.1.dev0
veritrail_github.__version__                      = 0.1.1.dev0
GitHub API COLLECTOR_IMPLEMENTATION_VERSION       = 0.1.1.dev0
P2 PUBLIC_RENDER_COLLECTOR_IMPLEMENTATION_VERSION = 0.1.0
```

本successor只把它们同步为 `0.1.1`，并把既有 P4 发行工具的固定版本、wheel/sdist/summary 名称、wheel-only CI exact
import-version oracle与真实 acceptance installed-product version同步到相同坐标。直接回归向量分别对 P1 与 P2 证明：同一 observation spec、source coordinates 与
facts 下，`collector_version` 从 0.1.0 变为 0.1.1 时 Evidence artifact SHA 必须改变，而 `facts_digest` 与
`normalization_semantics_version` 必须保持不变。

候选明确保持：

```text
P1 normalization = github-rest-facts/0.3
P2 normalization = github-public-render-facts/0.1
Core dependency  = veritrail==0.13.0
render extra     = playwright==1.62.0
Python floor     = >=3.10
```

`public_render_browser.py`、45 秒采集窗口、5 秒 cleanup-only release envelope、network/body budget、facts、coverage、
P3 handoff 与 Core Verdict priority均不修改。若最终 diff 需要改变任一上述边界，候选立即停止并返回 CONTROL LOOP。

## 3. 固定候选资产与非自指顺序

release-preparation 工具只允许生成以下四项候选资产：

```text
veritrail_github_evidence-0.1.1-py3-none-any.whl
veritrail_github_evidence-0.1.1.tar.gz
github-evidence-v0.1.1-validation-summary.json
SHA256SUMS-github-evidence.txt
```

顺序保持：

```text
wheel + sdist
  -> validation summary
  -> SHA256SUMS (wheel + sdist + summary)
  -> external release facts bind all four assets
```

candidate validation summary只能写 `RELEASE_CANDIDATE / PUBLIC_GATES_GREEN / PRE_TAG / NO_PUBLIC_DOWNLOAD_CLAIM`，不得包含
自身 digest、未来 tag object、Release ID或匿名下载结论。候选字节只作候选资格，合入后必须从新的 exact main 重建最终资产，
不得复用本地或 PR artifact。

## 4. 本地资格矩阵

final bytes 至少必须重新执行：

1. Python 3.10.6 / 3.13.13 × normal / `-O` 的 Core 与 GitHub Evidence full suite；
2. direct provenance/facts identity vectors及 release-asset fail-closed vectors；
3. 两次独立 wheel/sdist build、metadata/content比较与非自指 summary/checksum verify；
4. base wheel、sdist、`render` extra、matching Chromium、`pip check`、plugin uninstall 后 Core-only复算；
5. 真实 GitHub P1 -> P2 -> P3 正向链；
6. blocked-cleanup negative lifecycle：deadline 后 bounded return、driver terminal、owned process tree零残留、cleanup errors可见且
   不冒充内容成功；
7. frozen browser lifecycle blobs、source/fact Schema、public exports与 primary `audit.json` continuity；
8. wheel-only CI exact import-version oracle为`0.1.1`且旧`0.1.1.dev0`绑定不存在；
9. `git diff --check`、global/local hygiene、Markdown链接/格式与精确 scope。

测试只作 candidate witness；它们不创建 tag、Release或public installed-product事实。

## 5. PR、exact-main 与发行前门

候选必须以单一 exact head 完成 original PR required gate、protected merge、新 exact-main Public CI 15/15 与 Browser Smoke
1/1。合入后还要从该新 exact main：

1. fresh 重建并复核候选产品矩阵；
2. 重新核对 `github-evidence-v0.1.0` immutable history、active `github-evidence-v*` tag ruleset、Core `v0.13.0`
   Latest身份以及 `github-evidence-v0.1.1` tag/Release不存在；
3. 关闭 final staging identity，才允许进入最终发布串行链。

任一门失败必须保留原 identity；禁止 rerun 洗白。source candidate PASS 不能冒充 public download或doc437 recovery。

## 6. 候选闭合后的唯一后继

全部 release-preparation candidate 门闭合后最多得到：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_CANDIDATE_EXACT_MAIN_VERIFIED
GITHUB_EVIDENCE_0_1_1_FINAL_ASSET_REBUILD_AND_PROTECTED_PUBLICATION_ALLOWED
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
```

随后必须从新的 exact main 重建最终四项资产，严格串行执行 ruleset核对、protected annotated tag、non-Latest draft Release、
上传、authenticated核账、发布、fresh anonymous API/Release/asset download、双Python installed-product正负链与独立 docs-only
release-facts publication。任何公开失败沿用冻结的tag不可移动、asset不可静默覆盖语义；必要修复必须使用新 patch version。

发行闭合后仍须返回 CONTROL LOOP，为 doc437 建立自己的 fresh Plan/session/formal。doc437 recovery、Manifest 0.2、global
composition、public Review与R2–R6都不能继承本候选 PASS。

## 7. 当前停止线

当前只能声明：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_RELEASE_AND_P2_PROVENANCE_ALIGNMENT_CONTRACT_0_1_FROZEN
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_ORIGINAL_PR_504_FAILED_CLOSED_UNMERGED
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_LOCAL_SUCCESSOR_2F61_STOPPED_PRE_PR_NOT_QUALIFIED
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_FINAL_SUCCESSOR_CANDIDATE_NOT_MERGED_NOT_QUALIFIED_NO_TAG_NO_RELEASE
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`proof_is_not_problem_solving = true`、`local_not_global = true`；R1完成后的human + AI全项目检查仍是独立后续目标。
