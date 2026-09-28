# M10 Browser 主机 socket 分类修正与发行消费合同

日期：2026-09-29

> 当前条件状态：
> `M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_CONTRACT_CANDIDATE /
> M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_IMPLEMENTATION_NOT_STARTED /
> CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED`
>
> 精确基线：`main@fc2be4009989c3ddc0ff71fc5f0a54c02290751a`，Git tree
> `ba5715e5800d1b74cf733826b2e9da3d6e0aefd4`
>
> 影响层级：`L2_CONTRACT + L2_DISTRIBUTION_IDENTITY + L0_DOCUMENTATION`。本文只冻结后继修正、
> maintenance 发行和 required-lane 消费迁移的最小权责与顺序；当前候选不修改 runtime、tests、workflow、
> version、branch、ruleset、tag、Release、asset、Schema、Parse 合同或 persistence。

## 1. 合格输入与合同问题

[文档 222](222-m10-browser-host-socket-classification-correction-release-consumer-precontract-audit.md)
经 [PR #245](https://github.com/NoctilumeDev/VeriTrail/pull/245) original Public CI
`36466022463` attempt 1 的 11/11、ordinary merge、new exact-main Public CI `36469016262`
attempt 1 的 11/11 与 Browser Smoke `36469016158` attempt 1 的 1/1 后，README、doc222 与
milestones 三份 fresh anonymous installed-product readback 均为 `COMPLETED / PASS`。六份匿名 public
raw bytes 与 exact Git blobs 一致；independent reconciliation manifest 为：

```text
sha256_json  = 0ec68ad5805535e9a06676eb403f4a6b3298765258d1bfcde5f2b8f96c3bf1dd
sha256_bytes = 8a5506d1f79b96fdd17486aa7919575677892a0c7a20d01ecbb9dde6d0721b05
```

正式 Plan 产生以前有两项 setup observation：托管 worktree 工具从 workspace parent 调用时返回
`Not a git repository`；installed-product preflight 成功后，Playwright executable-path 探针关闭时打印
`TargetClosed` pending-task warning。两者都没有创建正式 Plan、session、Evidence 或产品观察，保持
`NON_QUALIFYING`；后继三份 PASS 不覆盖它们。

因此 doc222 已成为 qualified precontract audit。本合同只回答：

> 怎样把已证明的精确 Browser 分类缺口，分别修正到 current source 与不可移动的 0.12 历史发行线，
> 再让 required Starter lane 消费一个真正合格的公开产品，同时不改写任何既有失败或发行身份？

## 2. 冻结的分类语义

### 2.1 精确匹配

Browser request-failure collector 取得 Playwright failure value 后，必须先形成既有 raw failure text。只有：

```text
raw_failure_text.strip() == "net::ERR_NO_BUFFER_SPACE"
```

才增加 private collector classification：

```text
collector  = network:<viewport>
error_type = HostSocketNoBufferSpace
```

匹配不得扩张为子串、前缀、后缀、大小写不敏感、正则族或“所有 socket 错误”。
`net::ERR_CONNECTION_RESET`、`net::ERR_INSUFFICIENT_RESOURCES`、未知 failure 与空 failure 继续按既有
Browser 合同处理，不能被本合同推断成 `HostSocketNoBufferSpace`。

### 2.2 raw Network fact 保留

分类只增加 collector projection，不能删除、替换、规范化或伪造原始 Network request failure：

```text
Network request record.failure = original raw failure text
collector error                = network:<viewport> / HostSocketNoBufferSpace
```

因此同一 Artifact 同时保留“浏览器实际报告了什么”和“该精确失败由哪一侧负责”。private error type
不得进入用户可控 URL、selector、response body 或 Subject 输出，也不得把敏感本机路径写入公共 Artifact。

### 2.3 lifecycle 与 Verdict

一旦上述 collector error 进入 Browser collection，既有 M10 fail-closed 语义必须得到：

```text
stop_reason      = COLLECTOR_ERROR
execution_status = ERROR
verdict          = PENDING
responsibility   = observer / collector side
```

它不得成为：

```text
BROWSER_HARD_FAILURE / COMPLETED / FAIL / SUBJECT
```

预注册 selector、fill、click 或业务断言真正失败时，既有
`BROWSER_HARD_FAILURE / COMPLETED / FAIL` 语义不得被本映射吞掉。分类表不拥有重试、扩大 timeout、
忽略 Network failure、把 collector failure 降格成 warning 或替 Subject 生成 PASS 的 authority。

## 3. 三条独立 source / distribution identity

本合同冻结三条不能互相继承资格的轨：

| 轨 | source identity | 可获得的最强结论 | 不能获得的结论 |
| --- | --- | --- | --- |
| C：current source | 后继 main 上自己的 correction PR / merge | current source 已包含分类修正 | public `v0.13.0` wheel 已修复 |
| M：0.12 maintenance | `v0.12.2^{}` 精确谱系上的 protected maintenance tip | 新 `v0.12.3` 候选/发行包含 backport | current main 或 public 0.13 line 已修复 |
| W：required consumer | 后继 main workflow 中固定的 public 0.12.3 URL、SHA-256 与 version check | required lane 消费了合格 0.12.3 | workflow 自己创造 compatibility 或修正语义 |

相同 patch、相同测试输出、相同 wheel version string 或相同 terminal classification 都不能让一条轨继承另一条轨的
source、attempt、tag、asset 或 readback qualification。

## 4. C：current-main 修正

合同冻结后，C 阶段只允许在新的 main-based PR 中：

1. 实现第 2 节的封闭分类；
2. 增加精确匹配、near-miss、raw fact 保留与 lifecycle 归因回归；
3. 保持当前 Core source version 为 `0.13.0`，不移动或重制 public `v0.13.0`；
4. 不修改 Starter compatibility、required-lane URL、timeout、retry、Parse 或任何发行资产。

候选必须通过两套 Python 的适用 normal / `-O` 全回归、Browser/bootstrap/CLI 定向矩阵、original PR
required checks、受保护 main 合入以及 new exact-main Public CI / Browser Smoke。current-main PASS 只证明
current source；它既不发布 0.13 patch，也不授权进入 Parse。

## 5. M0：maintenance branch 治理 bootstrap

### 5.1 不可移动谱系与固定分支

0.12 maintenance 的唯一根为：

```text
annotated tag object = 2177bb2cc02d9ef9068e7b7132983c5edb82be6c
v0.12.2^{}          = f961930ae1e69d7d88849fa2b0d40befb3e94c89
maintenance branch  = core-0.12-maintenance
```

不得从 current main、`v0.13.0`、诊断 worktree 或重新打出的 0.12.2 source archive 创建该分支。

### 5.2 为什么需要两阶段 ruleset

`v0.12.2` 的 Public CI 与 Browser Smoke workflow 只监听 `main`。若新分支从创建时就要求这些远端
checks，首个 workflow-enablement PR 将没有资格产生 required check，治理会自锁。该事实不授权 direct push
产品代码，也不授权临时 bypass。

合同只允许以下一次性 bootstrap：

```text
phase-one active ruleset created before branch
  target = refs/heads/core-0.12-maintenance
  bypass = none
  deny deletion
  deny non-fast-forward
  require pull request
  required status checks = none
        ↓
create branch exactly at v0.12.2^{}
        ↓
bootstrap PR changes only the two workflow branch filters
        ↓
ordinary merge through the phase-one PR rule
        ↓
new maintenance exact-tip Public CI + Browser Smoke
        ↓
upgrade the same ruleset to phase two
```

如果 GitHub 在 active phase-one ruleset 下拒绝创建这个只指向既有可达 commit 的 exact branch ref，该观察就是
`MAINTENANCE_BOOTSTRAP_CONTRACT_COUNTEREXAMPLE`。此时必须停止并最小重开治理 seam，不得通过临时 disable、
bypass、direct push 或先创建未保护 branch 来让原合同“看起来可行”。

bootstrap PR 只允许：

- `.github/workflows/ci.yml` 的 `push` / `pull_request` target 增加
  `core-0.12-maintenance`；
- `.github/workflows/browser-smoke.yml` 的 `push` target 增加
  `core-0.12-maintenance`；
- 不修改 job、step、action pin、timeout、test command、runtime、version 或发布文件。

bootstrap PR 在 merge 前必须通过 exact-diff、YAML/static、两套 Python normal / `-O` 和既有 Browser
acceptance 的本地 final-byte witness。由于 base workflow 尚不监听该 branch，不得伪造“original remote required
checks”；merge 后 push 产生的 exact-tip Public CI 与 Browser Smoke 才是该 bootstrap 的远端产品观察。
任一 exact-tip 门失败时，保持 branch 与失败身份，停止 phase-two ruleset 和全部产品 backport。

### 5.3 phase-two ruleset

bootstrap exact-tip 双门成功后，ruleset 必须保持 active、无 bypass、禁止删除与 non-fast-forward、要求 PR，
并增加 strict required checks：

```text
Python 3.10 on Windows
Python 3.13 on Windows
Wheel-only first run on Python 3.10
Wheel-only first run on Python 3.13
E3 0.2 release download acceptance
Workbench tests, lint, build, and audit
Starter PASS/FAIL golden path
```

`strict_required_status_checks_policy = true`，`do_not_enforce_on_create = false`。ruleset identity、target、
enforcement、rules、bypass 与观察时间必须进入后继事实。GitHub ruleset 是外部控制面；更新它不因此获得修改
source branch 的 authority。GitHub 关于 ruleset 创建、状态检查与 rule layering 的当前语义见
[Creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)、
[Available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
与 [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)。

## 6. M1：0.12.3 backport 与 release candidate

只有 phase-two ruleset 读回成立后，新的 topic branch 才能从 maintenance tip 创建产品 PR。该 PR 只允许：

- 第 2 节的 Browser classification backport；
- 与该语义直接对应的 Browser/bootstrap/CLI 回归；
- `pyproject.toml` 与 `veritrail.__version__` 从 `0.12.2` 升为 `0.12.3`；
- 0.12.3 release notes、validation summary 构建入口与本合同授权的最小发布文件。

它不得带入 Acceptance API、P1–P4、R1、current-main-only maintenance、其他 0.13 增量或无关依赖更新。
历史 branch 与 topic branch 的 diff 必须证明新增生产语义只属于精确 host-socket 分类。

验收至少包括：

1. 两套 Python normal / `-O` 的完整 0.12-line Core、Starter 与 Authoring Skill 回归；
2. exact failure、near-miss、raw Network fact、两类 viewport collector identity 与 exactly-once error projection；
3. deterministic bootstrap/CLI world 证明 exact failure 为 `COLLECTOR_ERROR / ERROR / PENDING`；
4. 既有 selector/business failure 仍为 `BROWSER_HARD_FAILURE / COMPLETED / FAIL`；
5. wheel 与 sdist 的无 checkout clean install；
6. unchanged public Starter 0.2.0 wheel 的 compatibility、doctor 与真实 PASS/故意 FAIL 链；
7. Catalog 两 Run/零 issue、Workbench 零 console/http/page/request error，以及端口、进程、SQLite sidecar 与
   owned staging 零残留；
8. phase-two ruleset 的 original PR required checks、ordinary merge 与 new maintenance exact-tip Public CI /
   Browser Smoke。

诊断中第一次 patched Python 3.13 normal 的 7/58 failure 保持 `UNKNOWN`；后继全绿不能把它改名为
transient，也不能删掉失败记录。正式 candidate 任一同型失败都必须保 Artifact 并重新归因。

## 7. M2：Core 0.12.3 create-new publication

产品 PR 与 maintenance exact-tip 双门成功后，最终资产必须从该 exact tip 的 clean detached checkout 重新构建；
不得复用诊断 wheel 或 PR staging bytes。固定上传集合为：

```text
veritrail-0.12.3-py3-none-any.whl
veritrail-0.12.3.tar.gz
core-v0.12.3-validation-summary.json
SHA256SUMS.txt
```

0.12.3 不重新分发未变化的 Workbench ZIP；`v0.12.2` / `v0.13.0` 的既有 Workbench assets 保持原身份。
`SHA256SUMS.txt` 使用非自指约定，只覆盖前三个 payload；其自身以 final staging bytes、GitHub asset digest 与
匿名下载 bytes 三方对账。

发布顺序固定为：

```text
final staging + local verification
    -> existing Core tag ruleset 21437132 readback
    -> protected annotated tag v0.12.3
    -> non-Latest draft Release
    -> upload four create-new assets
    -> verify asset names / sizes / GitHub sha256 digests
    -> publish non-Latest, non-prerelease Release
    -> anonymous public readback
```

现有 Core tag ruleset 覆盖 `refs/tags/v*`、无 bypass、禁止删除与 non-fast-forward；它必须在 tag 创建前重新
读回。`v0.12.3` 不得成为 Latest，当前 Latest `v0.13.0` 必须保持不变。

公开读回至少重做：

- tag object、peeled commit、Release flags、固定四资产与摘要；
- Python 3.10 / 3.13 wheel clean install、版本、`pip check` 与分类/Bootstrap 纵向门；
- Python 3.10 / 3.13 sdist clean build/install 与相同适用门；
- 匿名下载并核验 public Starter 0.2.0 wheel 后，与 public Core 0.12.3 wheel 完成真实 PASS/FAIL、Catalog、
  Workbench 与 cleanup 链；
- 发布输入、输出、日志与摘要的敏感路径扫描。

## 8. W：required lane 的单独消费迁移

public 0.12.3 readback 与独立 release-facts publication 闭合以前，不得修改 main 的 required Starter lane。
随后只能用单独 workflow PR 把：

```text
fixed public URL
fixed SHA-256
expected installed version
```

从 0.12.2 更新到已读回的 0.12.3。该 PR 不得同时修改 runtime、tests、timeout、retry、job 名、required-check
集合或 Starter compatibility。original PR 必须实际运行 public 0.12.3 的 real Starter PASS/FAIL chain；合入后
new exact-main Public CI 与 Browser Smoke 必须再次成功。workflow migration 的成功只能证明 consumer 选择与
end-to-end gate，不替代 Core 0.12.3 自己的发行资格。

## 9. public 0.13 与 Parse authorization

C 阶段修正 current source 后，public `v0.13.0` tag、Release 与五项 assets 仍保持未修复的历史身份，不得重制。
未来 public 0.13.x 修复必须使用新的合同、版本、tag、Release、asset bytes 与公开读回；本合同不选择版本号，
也不授权该发行。

public 0.13.x 新发行不是重新审查 Parse private implementation authorization 的前置条件。只有以下事实全部成立后，
才允许回到 CONTROL LOOP 重新审查 Parse authorization：

```text
current-main classification correction exact-main qualified
+ public Core 0.12.3 release/readback qualified
+ required Starter lane migrated to exact public 0.12.3 coordinate
+ migrated main exact-main Public CI / Browser Smoke qualified
+ all prior failures and UNKNOWN causes preserved
```

这只恢复“重新审查资格”，不自动重新发布 PR #243，不自动授权 parser，也不选择 persistence。

## 10. 失败与恢复语义

| 失败位置 | 状态 | 唯一允许的后继动作 | 禁止动作 |
| --- | --- | --- | --- |
| C correction PR / exact main | `CURRENT_SOURCE_CORRECTION_FAILED` | 保留原 attempt，归因后用新 candidate 取得自己的资格 | 把 maintenance PASS 借给 main |
| branch/ruleset bootstrap | `MAINTENANCE_BOOTSTRAP_BLOCKED` | 保留 ruleset/ref/PR/CI identity，修订合同时只重开治理 seam | disable/bypass ruleset 后直接推产品代码 |
| M1 PR / exact tip | `MAINTENANCE_CANDIDATE_FAILED` | 保留 Artifact，归因后从同一 protected line 建新 candidate | 移动 v0.12.2 或用 current main 重建 0.12.3 |
| tag 前 | `RELEASE_NOT_STARTED / CANDIDATE_FAILED` | 从新的 qualified maintenance tip 重建全部 final assets | 用旧绿灯或诊断 wheel 发布 |
| tag 已推、Release 未公开 | `TAGGED / RELEASE_PENDING` | source/tag/bytes 未变时恢复同一 draft/upload，逐次记录 attempt | 移动 tag、覆盖同名 asset、换源码保留版本号 |
| Release 已公开但读回失败 | `RELEASE_FAILED / NOT_FROZEN` | 明示失败，修复使用新的 patch version/tag | 删除重传、静默改写、迁移 required lane |
| workflow migration | `CONSUMER_MIGRATION_FAILED` | 保留 PR/run，从仍消费 0.12.2 的合格 main 重新归因 | retry 到绿、取消 required lane、宣布 Parse authorized |

如果任何 asset 曾向匿名用户可见，就不得通过删除后重传同名文件制造“从未失败”。后来的 PASS 可以建立新资格，
不能覆盖旧 ERROR/FAIL/UNKNOWN。

## 11. 明确禁止的扩张

本合同不得：

- rerun、重开或改写 PR #243；
- 移动、删除、重制或补传 `v0.12.2`、`v0.13.0`、`starter-v0.2.0` 的 tag / Release / assets；
- retry `ERR_NO_BUFFER_SPACE`、扩大产品 timeout 或把 collector failure 当成 Subject failure；
- 让 workflow、Starter 或 Release Notes 拥有 Browser classification authority；
- 在 phase-one ruleset 下合入 runtime/version，或在 phase-two ruleset 生效前创建产品 PR；
- 从 current main 构建 0.12.3，或把 0.13 增量伪装成 patch maintenance；
- 用 source Starter、诊断 wheel、本地 editable install 或 compatibility metadata 替代 public product readback；
- 在同一 PR 中实现 Parse、修改 Fact/Relation/Slice/Coverage、选择 persistence 或重开 frozen R1 合同；
- 把 0.12.3 的资格扩张成 public 0.13、macOS/Linux、恶意代码隔离、Docker 或生产容量证明。

## 12. 串行施工与每阶段停止线

合同冻结以后仍必须严格按：

```text
C1  current-main correction
    -> original PR gates
    -> protected main merge
    -> exact-main Public CI + Browser Smoke

M0  maintenance governance bootstrap
    -> phase-one ruleset
    -> exact v0.12.2 branch
    -> workflow-only PR
    -> maintenance exact-tip dual gates
    -> phase-two strict ruleset readback

M1  0.12.3 correction/release candidate PR
    -> required checks
    -> protected merge
    -> maintenance exact-tip dual gates

M2  tag / Release / four assets
    -> anonymous download and dual-Python product readback
    -> independent release-facts publication

W1  main workflow-only consumer migration
    -> original PR public 0.12.3 Starter chain
    -> protected merge
    -> new exact-main dual gates
    -> fresh status readback / reconciliation

CONTROL LOOP
    -> only then re-audit Parse private implementation authorization
```

前一阶段未闭合，后一阶段不得开工。各阶段只继承明确列出的合格 source fact，不继承 attempt、continuation、
release 或 observation authority。

## 13. 本候选停止线与资格链

本文只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_CONTRACT_CANDIDATE
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_IMPLEMENTATION_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

候选只能修改 AGENTS、README、milestones 与本文四个文档文件。它必须完成 final-byte local gates、original
PR required checks、受保护 main 合入、new exact-main Public CI / Browser Smoke、fresh README / doc223 /
milestones installed-product readback 与 independent reconciliation，才可成为 qualified contract candidate。

qualified candidate 仍不是 frozen contract。它必须再经过独立 docs-only freeze publication、该 publication
自己的 original PR / merge / exact-main 双门与 fresh final readback，目标状态才可生效。冻结以前不得创建
`core-0.12-maintenance`、ruleset、runtime patch、version、tag、Release 或 workflow migration。

## 14. 当前 final-byte 本地证据

候选四文件字节完成以下 Markdown / Schema 四格：

| Python | mode | result |
| --- | --- | --- |
| CPython 3.10.6 | normal | `40/40 PASS` |
| CPython 3.10.6 | `-O` | `40/40 PASS` |
| CPython 3.13.13 | normal | `40/40 PASS` |
| CPython 3.13.13 | `-O` | `40/40 PASS` |

每格运行 `tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`。独立只读 checker
确认：

```text
changed scope                         4/4 PASS
relative Markdown links              554 / zero broken
UTF-8 without BOM / LF / final LF    PASS
changed-file fences / headings       PASS
candidate markers                    PASS
sensitive local paths                zero
frozen docs / architecture blobs     unchanged
git diff --check                     PASS
```

冻结输入的 Git blobs 继续为：

```text
doc217 = 0032f6c3c4b90f78f714920982fa373bbb5cb13d
doc218 = 9fa5e1884a3edcb614d3bf9f1218c57acfc36a36
doc219 = 02e886ce87a865db602ff63a9a4d187c5994fc67
doc221 = 4c4c9d9eaf2a620373e267e3664c28a2a34a1e4d
doc222 = 849da7f9bcda0d992eab5aa44a25d137e6eb0566
```

这些 witness 只使 docs-only candidate 具备提交资格；它们不替代 original PR、merge、exact-main、fresh
installed-product readback、independent reconciliation 或后继 freeze publication。
