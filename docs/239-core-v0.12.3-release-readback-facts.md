# Core 0.12.3 发布与公开读回事实

> 状态发布目标：
> `CORE_0_12_3_RELEASED / CORE_0_12_3_PUBLIC_READBACK_COMPLETE /
> CORE_0_12_3_MAINTENANCE_FROZEN /
> W1_REQUIRED_STARTER_LANE_MIGRATION_NOT_STARTED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED`
>
> 状态发布基线：`main@95a48f3dc283419bdc3de879360288de477a0995`
>
> 发行源码：`core-0.12-maintenance@a18da8ce40f7f9113bebef82f7fa5b3fcf334212`，
> Git tree `89adec5db40b6784d0a833f073010a81e261fe4b`
>
> 影响层级：`L0_DOCUMENTATION + L2_DISTRIBUTION_IDENTITY`。本文只发布已经形成的 maintenance
> source、tag、Release、公开资产与匿名产品读回事实；不修改 runtime、tests、workflow、timeout、retry、
> required-check、Schema、Parse 合同或任何历史 Release 字节。

本文是[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
第 6–8 节中 M1/M2 出口的独立 release-facts publication。本文自己的 final-byte local gates、original PR
Public CI、受保护 `main` 合入、new exact-main Public CI + Browser Smoke，以及合入后的 fresh
README／本文／milestones／AGENTS installed-product readback 与 independent source-byte reconciliation
全部成立以后，上述 target state 才生效。

## 1. M1：精确 maintenance backport 与合入后资格

M0 workflow bootstrap 已由[文档 238](238-m10-maintenance-workflow-bootstrap-qualification-publication.md)
闭合；phase-two ruleset `24216773` 当前仍为 active、无 bypass、禁止删除与 non-fast-forward、要求 PR，
并严格要求文档 223 所列七个 status contexts，`strict=true`、`do_not_enforce_on_create=false`。

M1 候选 `4bae52e4127a964985f56a2219fc0c0a002a82b4` 从 exact maintenance source 构造，只包含：

- `net::ERR_NO_BUFFER_SPACE` 的精确 `HostSocketNoBufferSpace` collector 分类；
- raw Network failure 保留、near-miss、两类 viewport、exactly-once error projection 与 business-failure
  非回归；
- Core 版本 `0.12.2 -> 0.12.3`、0.12.3 Release Notes 与 source-side installed-distribution probe；
- 不带入 Acceptance API、P1–P4、R1 或其他 0.13-only 增量。

[PR #273](https://github.com/NoctilumeDev/VeriTrail/pull/273) 的 original Public CI
[`37857066281`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37857066281) attempt 1 为
`7/7 SUCCESS`。ordinary merge `a18da8ce40f7f9113bebef82f7fa5b3fcf334212` 保持 candidate tree；
maintenance exact-tip Public CI
[`37857936597`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37857936597) attempt 1 为
`7/7 SUCCESS`，Browser Smoke
[`37857936668`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37857936668) attempt 1 为
`1/1 SUCCESS`。candidate 与 exact-tip run 身份没有复用。

M1 最终字节还通过：

- Python 3.10／3.13 normal 与 `-O` 的 Core `352/352` 四格；
- Starter 与 Authoring Skill `24/24` 四格及 Authoring 真实 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`；
- wheel／sdist clean install、public Starter 0.2.0 兼容链；
- Workbench `172/172`、lint、type-check/build、audit 0 vulnerabilities；
- Browser Smoke `5/5`、102 个请求、零 HTTP error 和零残留。

这些事实证明 M1 backport 已合入并绑定 exact maintenance tip；它们不替代 M2 公开发行或 W1 consumer
迁移资格。

## 2. M2：受保护标签与非 Latest Release

发布资产从上述 exact-tip 的 clean detached checkout 重新构建，没有复用诊断 wheel、PR staging 或历史
Release 字节。创建标签前，Core tag ruleset `21437132` 已读回为 active、无 bypass、覆盖
`refs/tags/v*`，禁止删除与 non-fast-forward。

最终公开坐标为：

- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.3>；
- Release ID：`407348784`；
- 发布时间：`2026-10-08T23:44:52Z`；
- 注释标签：`v0.12.3`，tag object `244cc76b1c19cefd8a70b0da367b5bf0cfd97146`；
- 标签解引用提交：`a18da8ce40f7f9113bebef82f7fa5b3fcf334212`；
- Release `target_commitish` 字段为 `main`；最终源码身份只由受保护注释标签的解引用结果决定；
- Release 非 draft、非 prerelease、非 Latest；当前 Latest 仍为 `v0.13.0`。

四项 create-new 公开资产为：

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.12.3-py3-none-any.whl` | 199,301 | `360add853dbaf3bbd18b51d21b494b20891010c6f1bc4b122b9e87d77ce53308` |
| `veritrail-0.12.3.tar.gz` | 283,730 | `4270f8f81262180a71d2084c85793be4d459bd1ced3f46a264adf55772af7de2` |
| `core-v0.12.3-validation-summary.json` | 9,452 | `2e08390e2b7e35d824c41c5b5418c40e4264079a096e44864e571f69859168c2` |
| `SHA256SUMS.txt` | 293 | `ebcea39b44e6e3c4f0106fc552293c5391d36c0a2a206a3e35212a59e68bfe79` |

`SHA256SUMS.txt` 使用非自指约定，只覆盖 wheel、sdist 与 validation summary；其自身由 final staging、
GitHub asset digest 和匿名下载副本三方固定。0.12.3 不重新分发未变化的 Workbench ZIP；历史
`v0.12.2`／`v0.13.0` Workbench 资产保持原身份。

## 3. 匿名公开读回

fresh readback 清除了 GitHub token 环境，并从公开 Release 重新下载四项资产。API、tag ref 与下载副本共同确认：

- tag object、peeled commit、Release flags 与四项 asset membership 精确一致；
- GitHub 返回的 size／SHA-256 digest 与上表一致；四个下载文件也与 final staging 逐字节一致；
- public `SHA256SUMS.txt` 精确覆盖三个 payload；`v0.13.0` 仍为 Latest。

公开 Core wheel／sdist 随后在四个 fresh venv 中独立消费：

| 输入 | Python | 结果 |
| --- | --- | --- |
| wheel | 3.13 | 版本／site-packages／`pip check`、normal／`-O` 字节一致、两条纵向门 `2/2 PASS` |
| sdist | 3.13 | 同上，全部通过 |
| wheel | 3.10 | 同上，全部通过 |
| sdist | 3.10 | 同上，全部通过 |

四格 probe 摘要相同；精确 host-socket world 为 `COLLECTOR_ERROR / ERROR / PENDING`，既有业务失败仍为
`BROWSER_HARD_FAILURE / COMPLETED / FAIL`。

public Starter 0.2.0 wheel 又以新的匿名下载身份取得 SHA-256
`ce6e9ea0730adc891aba97f8148fdb861fffdd5164989c980b5cbbaaa950771f`。它分别与 public Core
0.12.3 wheel 在 Python 3.13 与 3.10 完成：

- Starter doctor `READY`；
- 真实 PASS 与故意 FAIL 各一条；
- Catalog 两 Run／零 issue；
- Workbench desktop／mobile 双视口、每格六张截图、console/http/page/request failure 均为零；
- application／Catalog 端口释放，owned workspace residue 为零。

Workbench 来自 exact tagged source；`package-lock.json` SHA-256 为
`d9fbf89ca905ec2602b9956e986e24f74c38aaf4de3ea960d1dba3905ebd00a4`，production `dist`
为 63 个文件，canonical tree SHA-256 为
`b7853502e1b14bc54630d3e103ec986654055d01e865ee5c66f3acb4d8ad280e`。

independent anonymous reconciliation 为 `PASS`：

```text
sha256_json  = fa4c471ddc038008b084bc097203d8b9cdd31901121b6cdf2994088658ac0405
sha256_bytes = fbceac57f4c19a95c92b2b3718a2db7cab9736f01962a6d6bc74574ed9ae3d6c
```

## 4. 首败、setup error 与敏感路径边界

M2 没有把后继 PASS 倒写为“从未失败”。外部 observation history 保留九项身份，SHA-256 为
`2e085be3b9e788f23a3a8c37501c5b07baad2ba07e8289c38ef0f7b39561b3b8`，包括：

1. 首个 formal wheel verifier 漏装声明的 browser extra，业务 world 在真实浏览器语义以前落到
   `COLLECTOR_ERROR`；归因为 verification-harness setup error，不证明产品缺陷；
2. 第二次 orchestration 漏传 probe 必需的 `--output`，没有形成产品 probe；
3. Starter Python 3.13 产品链已经 PASS 后，wrapper 误认 canonical summary 文件名；保留 3.13 产品输出，
   Python 3.10 使用 fresh recovery identity；
4. 首个 artifact audit 无授权地要求 source-only probe 必须进入 sdist；最终资产字节未改变；
5. 两次 pre-tag `ls-remote` 分别暴露 per-command proxy 遗漏与 PowerShell peeled-ref 解析错误；均未形成远端
   mutation；
6. 首个匿名敏感路径扫描把本地 bootstrap 输入混入 publication evidence，且原日志脱敏未覆盖 JSON 转义路径，
   对 134 个文件得到 12 项命中，状态保持 `FAILURE`；
7. 后继扫描不修改原始观察，只生成独立脱敏日志，并明确排除 venv 实现树与六份 machine-local
   subject/bootstrap 输入；129 个证据文件、34,224,950 字节为零命中，独立 `PASS`；
8. reconciliation 前的一次 PowerShell 只读汇总命令有 empty-pipe setup error；没有产生结果或修改证据。

第一次敏感扫描报告没有被删除或重写。后继 PASS 证明的是经过明确 owner/consumer 划分后的 publication
evidence scope，不把本地 executable/root binding 伪装成可公开事实，也不把红灯解释成产品 defect。

validation summary 是 tag 前生成并上传的冻结字节；它不能包含发布后才发生的 readback observation。完整 M2
construction/readback 历史由上述外部 history 与 reconciliation 补充，不能重制 public summary 去擦除时间顺序。

## 5. Hygiene 与证明边界

完成 public readback 后，exact detached checkout 再次经过 `git clean -fdX`；最终仍精确位于上述 commit/tree，
tracked status 与 ignored status 都为零。public tag、Release assets、外部 observation history 与 readback manifests
各自仍有发行或证明 owner，不属于清理候选。

本轮没有运行 Codex Security 深度扫描、攻击路径验证或极端环境攻击工作流；普通 CI、Browser 与发行读回不得
冒充这些证据。macOS、Linux、C0/C2/C3、Docker、多服务、恶意代码隔离和通用项目自动探测不因本发行新增证明。

本次状态发布不得：

- 修改或重制 `v0.12.0`、`v0.12.1`、`v0.12.2`、`v0.12.3` 或 `v0.13.0`；
- 把相同 patch／classification／测试输出解释成 current main、maintenance 与 public distribution 之间的资格继承；
- 修改 required Starter lane 的 URL、SHA-256、version、timeout、retry、job 名或 required-check 集合；
- 启动 Parse／Fact／Coverage、`DECLARED_CLAIM_FIDELITY`、Schema 或 persistence。

## 6. 状态生效与下一停止线

本 publication 的施工历史还保留两项非产品 observation：首次 CPython 四格直接从 src-layout checkout
调用测试，因没有加入 process-local `PYTHONPATH=src` 而四格均得到 `ModuleNotFoundError`；源码、测试和 staged
bytes 没有被修改。后继 fresh attempt 只补齐该 source-test import path。首个静态 helper 已通过 UTF-8、LF、
fence、marker、敏感路径、scope 与 diff 检查，但只统计了全量 relative links，没有逐项验证目标，因此只记为
`LIMITED_PASS`；后继 fresh helper 必须使用仓库既有规范化 link parser 对全部 Markdown 目标重新核账。

最终四文件字节必须完成两套 Python normal／`-O` 的 Markdown + Hygiene 四格、全量 Markdown link、UTF-8 无
BOM、LF/final LF、balanced fences、required markers、敏感路径、exact four-file scope、`git diff --check` 与
`scripts/check_hygiene.py --local`。这些本地门只证明 publication bytes，不能替代 original PR 或 exact-main
产品门。

当且仅当本文自己的 original PR Public CI、受保护 `main` 合入、new exact-main Public CI + Browser Smoke，以及
fresh README／本文／milestones／AGENTS installed-product readback 与 independent source-byte reconciliation
全部成立，公开状态才推进为：

```text
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_RELEASED
CORE_0_12_3_PUBLIC_READBACK_COMPLETE
CORE_0_12_3_MAINTENANCE_FROZEN
W1_REQUIRED_STARTER_LANE_MIGRATION_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

该闭合只把 0.12.3 的 release/readback 事实发布回主线。之后必须返回 CONTROL LOOP，重新核对新的 exact main、
public asset coordinate、并行 PR 与文档 223 第 8–9 节，才可以判断 W1 是否仍是最小合法 seam。即使 W1 后续
取得资格，也只允许把 required Starter lane 的 fixed public URL、SHA-256 与 expected version 从 0.12.2 更新到
0.12.3；Parse 仍须等待 W1 自己的 original PR、protected merge、exact-main 双门与读回闭合后重新申请授权。
