# R1 DerivationEvidence Schema 0.1.1 实现冻结发布

## 1. 文档身份

> 状态目标：`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结候选：[R1 DerivationEvidence Schema 0.1.1 实现冻结候选](142-r1-derivation-evidence-schema-correction-implementation-freeze-candidate.md)
>
> 冻结合同：[R1 DerivationEvidence Schema 0.1.1 修正合同](140-r1-derivation-evidence-schema-correction-contract.md)
>
> 候选合入基线：`main@a940259a4c286f64d39a92854397eea25c442e0f`
>
> 影响等级：`L1_DOCUMENTATION / STATUS_PUBLICATION_ONLY`

本文只在 AGENTS、README、milestones 与本状态文档中发布 `DerivationEvidence 0.1.1` correction payload
已完成合同限定实现、本地矩阵、原始 PR 门禁、受保护主线合入、新 exact-main 门禁、匿名公共字节读回与
已安装产品公共渲染读回的事实。本文不创建或修改
Schema、corpus、identity vector、测试、runtime、Provider、parser、Fact、Relation、Slice、Coverage、Manifest、
CLI、Workbench、Core、P/Q、CI、依赖、tag 或 Release。

本文自身仍须完成原始远端门禁、受保护主线合入、新 exact-main 门禁与匿名公开读回。只有这些最后门全部
成立，状态目标才成为当前主线事实；在此之前，本分支文字不授权 budget primitive 或 provenance runtime。

## 2. 冻结对象与语义边界

修正 payload 的公共 root 是：

```text
schemas/review-derivation-evidence-0.1.1.schema.json

$id:
https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.1.1.schema.json
```

冻结实现只增加：

```text
EXECUTION_MEMORY_BUDGET
EXECUTION_ARTIFACT_BUDGET
```

并固定以下约束：

- non-`COMPLETED` ProviderRun 不得报告 canonical Fact/Relation identity；
- overall Evidence 非 `COMPLETED` 时，每个 ProviderRun 的 reported-ID 数组均为空；
- memory diagnostic 绑定 active `PROVIDER_RUN`，run-local 与 top-level typed tuple 指向同一 run；
- artifact diagnostic 只允许作为 `subject_ref = null` 的 top-level stop fact，不反写已完成 run；
- document Schema identity 升为 `0.1.1`，semantic digest domain、Manifest `0.1`、其他 R1 Artifact 与
  `RequestProvenance` 语义不变；
- 历史 `0.1` root、十九个 corpus 文件与三十四个 identity vector 继续保持原字节和原解释。

因此继续成立：

```text
Additive corrected Schema != In-place rewrite
Schema validity != Cross-object derivation conformance
Availability diagnostic != Partial canonical Fact authority
Correction payload frozen != Provider runtime authorized
```

## 3. 实现与本地证据

实现从冻结合同基线 `19cb4ff4300e6c7aeb08aa315802abb29e183d60` 建立：

```text
implementation commit:
4a2be77be6cbde6684aa7580b936eaba3c2147a5

implementation tree:
a060ed65177b516f4fe054d212f255cc1baf2f49

protected-main implementation baseline:
99826ec1564e8447524c477ff9f271fa5d062ea6
```

提交只修改合同允许的五个路径：一个新 Schema、一个独立 corpus README、一个
`R1-DE-CV-001..010` compatibility corpus、一个 correction 测试，以及历史 Schema payload 测试中的
additive root 集合。旧十个 Schema 与十九个 corpus 文件由二十九项固定 SHA-256 逐字节守卫。

有效本地矩阵显式绑定同一 implementation worktree 的 Core、GitHub Evidence、Review Attention 与 test root：

| 门 | CPython 3.10 normal / `-O` | CPython 3.13 normal / `-O` |
| --- | ---: | ---: |
| correction + historical Schema focused | `27/27` / `27/27` | `27/27` / `27/27` |
| Core | `446/446` / `446/446` | `446/446` / `446/446` |
| GitHub Evidence | `180/180` / `180/180` | `180/180` / `180/180` |
| Review Attention | `61/61` / `61/61` | `61/61` / `61/61` |
| Authoring Skill | `24/24` / `24/24` | `24/24` / `24/24` |

Workbench `173/173`、lint、type-check/build 与 dependency audit 全部通过，Core wheel/sdist 可构建；
`jsonschema` 仍只属于 `schema-test` optional extra。第一次 Core 全仓运行因测试与 imported plugin source
不在同一 worktree 而留下一个 loader error；该结果被判为 provenance 无效并保留，最终矩阵没有用后续成功
把它改名为未发生。

## 4. 实现 PR 与公开字节读回

[PR #121](https://github.com/NoctilumeDev/VeriTrail/pull/121) 的 base 为冻结合同基线，head 为 implementation
commit，只含上述五个允许路径。原始
[Public CI run 34707150563](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707150563)
在 attempt 1 取得 11/11，没有 rerun。PR 以 merge commit
`99826ec1564e8447524c477ff9f271fa5d062ea6` 合入，merge tree 与 implementation tree 相同。

该 exact main 的 [Public CI run 34707869618](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707869618)
为 attempt 1、11/11；[Browser Smoke run 34707869586](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707869586)
为 attempt 1、1/1。

没有 GitHub token 的 exact-SHA raw readback 取得以下公开字节，并与 merge tree 相等：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `schemas/review-derivation-evidence-0.1.1.schema.json` | 9671 | `a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045` |
| `tests/fixtures/review-r1-derivation-evidence-0.1.1/README.md` | 888 | `16168eeab31757daa5a8b8b66165a2a00916b78517b6fa630938b9e33f5878ef` |
| `tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json` | 20266 | `b202f0063b1d94a6edc7bf5c9e8aa30e24a76ff6584638bf416c7739ce1283df` |

raw transport success 只证明公开 exact bytes 可取得；Schema correctness 仍由合同、corpus、conformance 与
回归矩阵共同承担。

## 5. 冻结候选 PR 与 exact-main 门禁

[PR #122](https://github.com/NoctilumeDev/VeriTrail/pull/122) 从 implementation main 建立 docs-only 候选：

```text
base:
99826ec1564e8447524c477ff9f271fa5d062ea6

candidate commit:
90f4f31e6e44fbe2df359633fde19e4ab11acff9

candidate / merge tree:
8369260aa9f5729e8380ac4963b0ad4a6524a4b6
```

候选只修改 README、milestones 并新增文档 142。其本地合同索引/corpus/历史 payload 定向检查在
CPython 3.10 / 3.13 的 normal 与 `-O` 四条 lane 均为 `35/35`。

原始 [Public CI run 34708925152](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34708925152)
为 attempt 1、11/11 success，没有 rerun。PR 于 `2026-09-13` 合入：

```text
merge commit:
a940259a4c286f64d39a92854397eea25c442e0f

parents:
99826ec1564e8447524c477ff9f271fa5d062ea6
90f4f31e6e44fbe2df359633fde19e4ab11acff9
```

合入后只接受 exact `main@a940259a4c286f64d39a92854397eea25c442e0f` 的 push workflow：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [34709579700](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34709579700) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [34709579608](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34709579608) | 1 | `1/1 SUCCESS` |

## 6. 匿名已安装产品读回

读回在新建 CPython 3.13 venv 中安装已冻结 Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0`
与 matching Chromium。两份本地缓存的公开 Release wheel 在安装前重新核对为：

```text
Core:
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence:
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

三个 import 坐标均来自该新 venv 的 `site-packages`，不是 checkout、`PYTHONPATH` 或 editable install；环境
移除 GitHub token。每个 target 使用独立 sealed AcceptancePlan、独立 paired session、固定
`P1 API -> P2 Render` 顺序、fresh anonymous Chromium context、exact commit Markdown 坐标、三样本稳定
窗口与预先声明 marker。

| Target | Coverage / HTTP / samples / scope | Marker | Facts digest | Render Evidence SHA-256 | Report SHA-256 |
| --- | --- | ---: | --- | --- | --- |
| `README.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `657c67c1036b578c2e68c976fb1f1ac1e462707ee29063f75a13ea77de5fd3e5` | `39ed0c06763eb5ae9727558b1a9b3c3535859ed5659182aa7e23c7867a5e1fd4` | `15c4cad14a01833827290a1bcd428dc98d3fdcd3670abbac77edea706adf4a60` |
| `docs/142-r1-derivation-evidence-schema-correction-implementation-freeze-candidate.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `48f76014e6c1da171eec49feed6f3e330a38bd33f90c9a3f15bf53984ee5a7f9` | `b666ad866fb2bc0d356586566a98dc0ee20fcec474e69a02c2d48a75c80f3942` | `c03a298bb3a769d2be70df3c8305c443aceabf826a72b9a74695c8f6fa0db6af` |
| `docs/milestones.md` | `COMPLETE / 200 / 3 stable / 1 usable` | 1 | `100d514b1c22f1f3536f3d3634a709b95e0021244f4fa729aadc37d4ef6835f8` | `44d4e5b7d74a101279e8f127b66ca21d33a656f3be66aad1a2162a8efb913a28` | `18c24f6b1adfc0b3ef33e4169e1c8f2d6ca289e84ba865f97a3e624eee8e6a15` |

三项 Core Verdict 均为 `PASS`，marker 均为
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FREEZE_CANDIDATE`；`access_mode` 均为
`ANONYMOUS_FRESH_CONTEXT`。collection errors、coverage conflicts、cleanup errors 与 active streams 都为
0；requested URL 与 final URL 保持 exact SHA 和原 repository path。summary digest 为
`fe26a87a1440bbb37c98f4603f6902dcab59bb7591b0f921f4cfe906a3f552bb`。

该读回只证明采集时 GitHub 公共渲染可观察到候选内容，并证明已发布产品能完成该次 observation 与 Core
验收；它不证明 GitHub 之外的源头真实性，也不赋予 Collector、本文或模型现实真值裁决权。

## 7. 保留边界与唯一下一步

本次没有冻结、实现或授权：

- wall/memory/artifact budget runtime primitive；
- Provider-binding/attempt kernel、真实 Provider execution、Python parser 或 ambient discovery；
- canonical Fact production、FactSet 或 DerivationEvidence runtime publication；
- RelationSet、conflict / UNKNOWN 传播、ReviewSliceSet、CoverageLedger 或完整 Derivation Manifest；
- CLI、Workbench、Core handoff、Q implementation、D product shell、JPyxis 或 AI Execution OS；
- tag、Release、Linux/macOS、Server/Cloud、并发或分布式能力；
- 对源码正确性、缺陷真值、用户前提或现实真相的最终判断。

本 docs-only 状态发布只修改 AGENTS、README、milestones 并新增本文；`git diff --check` 通过。合同索引、
correction corpus 与历史 Schema payload 组成的定向检查在 CPython 3.10 / 3.13 的 normal 与 `-O` 四条
lane 均为 `35/35`。该结果不替代本发布自己的完整远端 required checks。

本文自己的最后门全部成立后，当前状态为：

```text
R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN
R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

唯一下一步是从新的 exact main 建立独立、非实现承诺的 budget primitive feasibility。它必须先证明一个
absolute monotonic deadline、pre-start process-tree memory containment、artifact staging stop、取消/清理与
zero residue 在当前 16GB Windows reference host 上真实可行。feasibility 不是 runtime authorization；只有它
独立冻结且后继明确发布实现授权，才可进入文档 137 的 Provider/Fact phase。

Relation、Slice、Coverage、conflict/UNKNOWN 与完整 Derivation 继续没有施工资格。任何新反例仍可否决后继
施工，或只重开被击穿的最小合同边界。
