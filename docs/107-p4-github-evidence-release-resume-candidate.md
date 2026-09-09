# P4 GitHub Evidence Plugin 发布恢复候选事实 0.1

> 当前状态：`P4_RELEASE_PREPARATION_CANDIDATE / CORE_0.13.0_BOUND / NO_TAG / NO_RELEASE / NO_PUBLIC_DOWNLOAD_CLAIM`
>
> 精确起始主线：`ab874d3cfd9ac140654e35d84b0025c2503e10cd`
>
> 分发绑定提交：`beaf006574e23d3d3f0c3541d9ea0708d23fa097`
>
> 分发源码树：`e511bdb2c8fc4108437de042a73314ed38252f02`
>
> 影响层级：`L2_PUBLIC_DISTRIBUTION_CONTRACT`；只把 GitHub Evidence Plugin 0.1.0 的公开 Core
> 依赖与发布核验固定到 `veritrail==0.13.0`，不修改 P1–P3 Collector、Evidence、handoff、Acceptance
> Core 或 Verdict 语义

## 1. 当前裁决

Core 0.13.0 的独立发布与公开读回已经解除 P4 的发行阻断。P4 随后从新的 exact main 重新开始，只修改
GitHub Evidence Plugin 0.1.0 的 distribution 依赖及对应发布核验，不复用文档 99 中绑定本地 Core
0.12.2 的历史候选。

当前候选已经完成本地源码矩阵、可复现 wheel/sdist 构建、公开 Core 0.13.0 的双 Python clean install、
显式 render extra、插件卸载后的 Core-only 复算，以及预封存真实 GitHub P1 -> P2 -> P3 正向链。
这些事实只支持：

```text
P4_RELEASE_PREPARATION_CANDIDATE
CORE_0.13.0_BOUND
NO_TAG
NO_RELEASE
NO_PUBLIC_DOWNLOAD_CLAIM
```

它们不表示 tag ruleset、annotated tag、GitHub Release、validation summary、checksum 或公开下载已经
发生。当前候选字节不得作为最终 Release 资产；候选必须先取得自己的原始远端门禁并合入受保护主线，
最终四项资产只能从合入后的新 exact main 重建。

## 2. 恢复策略没有被重开

本轮按真实反例重新审计了 `scripts/download_release_asset.py`。现有组件已经具备：

```text
one absolute recovery deadline
    -> narrow retryable transport/server failures
    -> bounded 2s / 4s / 8s / 16s backoff
    -> per-attempt unique partial file
    -> SHA-256 verification
    -> no-overwrite atomic publication
```

HTTP 404、摘要不一致、错误资产或语义核验失败不会因重试被放过；每次尝试只消费同一绝对截止时间的
剩余预算。成功文件只在摘要匹配后发布。因此本轮没有把一份草稿建议机械转成第二套下载器，也没有修改
P4 已冻结的资产身份、checksum 或 Release 坐标。

公开 Core wheel 通过该组件在第一次尝试完成匿名下载：

| 资产 | Size | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.13.0-py3-none-any.whl` | 220194 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |

这次成功只证明对应观察窗口内的下载成立，不覆盖文档 98 保留的历史 HTTP 500 反例，也不证明 GitHub 或
当前代理路径长期稳定。

## 3. 候选资产构建事实

从分发绑定提交 `beaf006574e23d3d3f0c3541d9ea0708d23fa097` 的干净源码建立两次独立构建。构建
环境为 CPython 3.13.13、`build 1.3.0`、`setuptools 80.9.0` 与 `wheel 0.45.1`。sdist 规范化后，
两次构建逐字节一致：

| 资产 | Size | SHA-256 | 双构建 |
| --- | ---: | --- | --- |
| `veritrail_github_evidence-0.1.0-py3-none-any.whl` | 69024 | `54bc460abd075633c9b453a7a921a0db6019c05d7225071cdb00e717745c6a9a` | `BYTE_IDENTICAL` |
| `veritrail_github_evidence-0.1.0.tar.gz` | 78465 | `a0ae8702d613f39c3e1556a8996ff6d7201f16c4ea1fc323da2f6b9a3a884468` | `BYTE_IDENTICAL` |

构建同时确认：distribution/import/version 为
`veritrail-github-evidence / veritrail_github / 0.1.0`，Core dependency 精确为
`veritrail==0.13.0`，render extra 仍只增加 `playwright==1.62.0`。这两项仍是本地候选字节；最终
validation summary 与非自指 checksum 必须等待新 exact main 重建。

## 4. 本地串行矩阵

源码回归显式绑定当前 worktree 的 Core `src`、插件 `src` 与测试根；clean-install 只从独立环境的
`site-packages` 读取公开 Core 0.13.0 与候选插件分发：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| Core 全量，普通 / `-O` | `416/416` / `416/416` | `416/416` / `416/416` |
| GitHub Evidence 全量，普通 / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| base wheel，无 Playwright | `PASS` | `PASS` |
| normalized sdist 安装 | `PASS` | `PASS` |
| render extra + matching Chromium | `3/3` | `3/3` |
| plugin uninstall 后 Core-only P3 复算 | `PASS` | `PASS` |

两套 base 环境均确认 P1 import、Collector 与 CLI 不依赖 Playwright；sdist metadata 同时确认精确
`veritrail==0.13.0` 与 render extra。render 环境显式安装 Playwright 1.62.0 和 matching bundled
Chromium 151.0.7922.34，并完成一次真实启动及 producer-side 8/32 MiB 两条硬上限测试。卸载插件后，
Core 0.13.0 仍能独立读取已形成的标准 Evidence 与 handoff；插件能力没有倒灌 Core 完整性。

## 5. 真实 GitHub 候选链

候选 wheel 从独立 3.10/3.13 render 环境运行，未提供 GitHub token，预先封存的目标为：

```text
NoctilumeDev/VeriTrail
README.md
commit ab874d3cfd9ac140654e35d84b0025c2503e10cd
marker VeriTrail
```

两次运行共享 Plan digest
`d0168892510c7beeb889a8804f08a1890884504d582942e503d48315361b7271`，但各自建立独立 session、
Evidence、handoff 与 Core report：

| Python | Session | Handoff digest | Evidence SHA-256（API / Render） | Core report digest | Verdict |
| --- | --- | --- | --- | --- | --- |
| 3.10 | `github-paired-668658268e87498fa8e6575ab53ca08f` | `948526ccfd16cf0baa7552947cc2940a0358266a2b0a13d7093c01dd1837de08` | `a97959a594b08637d8212e2fa6957209d9a03ea20f3cca2c402efdaadf55d89b` / `1e4607e524b2c2596de445350186aa079fb5b4aa093cd05864494e25c270b362` | `04a4c67444b900677f901dbfb9a49f9256820c4dc7b192d76e98a2de91a99ba0` | `PASS` |
| 3.13 | `github-paired-ce08dfa983b446daa73f1ff353241176` | `8cca60016b3ed0282fc39f016bd14cafd5d2dac46d01be3bcebafb60de89b17a` | `18160963baf8ef4a60705a91fbae975b7272ff87741aca2b5016a35aa6dae82e` / `20e5497e04eff38dbb2196d731876cf5a19915493e10d5b566b769b77b2cc493` | `3134883e7a53cdf629715b60df449838a24d58b9c8eaf2cdf04f15a1c523a230` | `PASS` |

两条链均确认：

- Core / plugin 安装版本为 `0.13.0 / 0.1.0`；
- P2 coverage 为 `COMPLETE`，HTTP 200，requested/final exact-SHA 路径一致；
- 三次规范化样本摘要均为
  `88d4c5481c96fd1c5aed03571e5b6e1b2c68f10b46cd4c153f76ccdd507b5431`，marker 为 24 次；
- P2 facts digest 为 `c8887af5c022e92214c648b9e14b161fb196ae092b42235eea8023d657ad089a`；
- 输出明确标记 `RELEASE_CANDIDATE_NOT_PUBLIC_DOWNLOAD_EVIDENCE`。

它们证明候选与当前公开 GitHub 现实相容，但不冒充插件 Release 的匿名下载证据。

## 6. 保留的失败与作废候选

- 从早期候选提交首次构建时，所选 Python 3.13 环境缺少 `build`，在生成资产前失败；随后建立显式、
  独立的构建工具环境，没有把本机偶然已安装工具当作项目事实；
- 第一轮完整插件回归为 `179/180`：`test_optional_render_boundary.py` 仍把 exact Core dependency 写成
  `0.12.2`。该门禁发现了真实漏改，修正后从头重建并重跑矩阵；
- 由旧提交 `00130c0...` 构建的本地候选因此作废。它没有进入仓库、tag、Release 或公开下载，也不得
  作为当前候选或最终资产复用；
- 两条真实 GitHub 链成功后，PowerShell 的摘要选择器使用了错误字段名，只使终端摘要显示为空；原始
  JSON 已保留正确 `PASS`、安装版本与精确摘要。该显示错误不被归因成 Collector 失败，也没有靠重复
  网络执行覆盖。

后继通过不会把这些历史执行改写成成功。它们分别约束工具链、测试完整性、候选身份和观察层归因。

## 7. 远端门与下一步

当前尚未发生：

```text
release-resume PR
original Public CI 11/11
protected-main merge
new exact-main final asset rebuild
github-evidence-v* tag ruleset
github-evidence-v0.1.0 annotated tag
non-Latest GitHub Release
public assets / anonymous downloads
P4 freeze publication
```

下一步只能推送当前候选并等待它自己的原始远端门禁。任何红灯必须按其事实层分类，不能通过重复运行、
放宽摘要、延长无界超时或混入 Dependabot 变更取得资格。候选合入后，从新的 exact main 重新建立最终
四项资产；tag ruleset 必须先于首个插件 tag 生效，插件 Release 必须保持 non-Latest，Core v0.13.0
继续拥有 Latest 身份。

R1 继续等待 P4 最终冻结与 Pattern Corpus 精确冻结，本候选不解除该阻断。
