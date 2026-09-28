# M10 Browser 主机 socket 分类修正与发行消费最小前合同审计

日期：2026-09-29

> 当前条件状态：
> `M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_PRECONTRACT_AUDIT_CANDIDATE /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED`
>
> 精确基线：`main@02ba60fd4f2e78f273485ba84110540cef209509`，Git tree
> `b71eb3d710c5dddfc76ae99dc07a4546e0d1d0f5`
>
> 影响层级：`L2_CONTRACT_AUDIT + L2_DISTRIBUTION_IDENTITY_AUDIT + L0_DOCUMENTATION`。本文不修改
> Core runtime、tests、workflow、Starter、version、tag、Release、timeout、retry、Schema 或 Parse 合同；不创建
> maintenance branch、ruleset、release candidate 或任何发行资产。

## 1. 已取得资格的问题边界

[文档 221](221-m10-browser-host-socket-release-consumer-boundary-audit.md)经 PR
[#244](https://github.com/NoctilumeDev/VeriTrail/pull/244) original Public CI `36454917831` attempt 1
十一项全绿后，ordinary merge 为：

```text
main = 02ba60fd4f2e78f273485ba84110540cef209509
tree = b71eb3d710c5dddfc76ae99dc07a4546e0d1d0f5
```

该 exact main 的 Public CI `36457785860` attempt 1 为 `11/11 SUCCESS`，Browser Smoke
`36457786007` attempt 1 为 `1/1 SUCCESS`。README、doc221 与 milestones 三份 fresh anonymous
installed-product readback 均得到 P1/P2 `COMPLETE` 与 Core `PASS`；AGENTS、README、doc219、doc221、
milestones 五份匿名 public raw bytes 等于 exact Git blobs。independent reconciliation manifest 为：

```text
sha256_json  = 0333b6ddf4489fcd2d4ac8d64ba47b122f76106dc9c2b10e57d805a2f8997a74
sha256_bytes = 1f45742e782e15ec95306b5a3619d11127bc61f42d7012babe9820aa1e46eede
```

readback 前的匿名 API / Playwright preflight 已成功返回精确 SHA 与公开页面，随后进程在 async shutdown
打印 warning。它发生在正式 Plan/session 以前，保留为 setup observation，不进入三份正式产品裁决。由此，
doc221 已成为 qualified problem boundary；该结论只授权本次最小前合同审计，不直接授权 runtime 或发行。

## 2. 本轮必须同时满足的三个事实

当前问题不能压成“在 `browser.py` 加一条映射”。至少有三项独立事实：

```text
classification semantics
    exact net::ERR_NO_BUFFER_SPACE is a host/client-side collector failure,
    not evidence that the Subject returned an incorrect business result

released consumer identity
    required Starter lane consumes the immutable public Core v0.12.2 wheel

current source identity
    main and the public Latest Core line are 0.13.0
```

因此：

```text
same semantic correction
    != same source history
    != same distribution bytes
    != same release qualification

fixing the required 0.12 lane
    != repairing public v0.13.0

fixing current source
    != repairing the immutable v0.12.2 wheel
```

任何后继合同若只证明其中一条，均不得借另一条的结果扩大 claim。

## 3. Authority owner 分离

后继合同必须保持以下权责：

| 问题 | authority owner | 不拥有该 authority 的对象 |
| --- | --- | --- |
| `net::ERR_NO_BUFFER_SPACE` 的 Browser/M10 分类 | Core Browser/M10 合同与对应实现 | Starter、workflow、失败 Subject |
| 某个 Core distribution 是否包含修正 | 该版本自己的 source commit、tag、Release、asset bytes 与公开读回 | 相同 patch、另一个 Core 版本、current checkout |
| Starter 0.2.0 接受哪些 Core | Starter 0.2.0 已冻结 metadata 与 doctor | CI workflow、Core release notes |
| required lane 实际消费哪个产品 | workflow 中固定的公开 URL、SHA-256、版本检查与 clean install | 本地 source import、editable Core、诊断 wheel |
| 历史失败身份 | PR #243 original run 与 Artifact | 后继 PASS、重跑、版本迁移 |

workflow 可以在合同闭合后选择新的 qualified consumer，但不能凭修改 URL 或 expected version 创造
compatibility，也不能证明被选择的 wheel 已经修复。Starter metadata 可以接受 `0.12.3`，却不证明该发行存在或
合格。Core patch 可以实现相同分类，却不能自行修改 Starter 的兼容合同。

## 4. 最小 required-lane 发行坐标

公开 Starter 0.2.0 冻结依赖为 `veritrail>=0.12,<0.13`。因此，在不扩大 Starter 合同、不创建新 Starter
版本的前提下，能够承载 required lane 修正的最小 Core 坐标是：

```text
Core 0.12.3 maintenance release
```

但 `0.12.3` 不能从 current main 构建。current main 已包含作为 minor release 发布的 Acceptance API 与其他
0.13 增量；把它们包装成 0.12.3 会违反
[Core 0.13.0 Acceptance API 发布补全合同](100-core-v0.13.0-acceptance-api-release-contract.md)已经冻结的
版本语义。合法候选必须：

1. 以 immutable `v0.12.2` 解引用提交
   `f961930ae1e69d7d88849fa2b0d40befb3e94c89` 为精确谱系起点；
2. 只包含封闭的 host-socket classification backport、对应回归、`0.12.3` version/release bytes 与后继合同明确
   授权的发布文件；
3. 在单独受治理且受保护的 maintenance branch 或等价历史发行坐标上，经自己的 PR、required checks、
   merge 与 exact-tip 资格链形成候选；
4. 以新的 annotated tag、GitHub Release 与 create-new assets 发布，不移动、不覆盖、不补传 `v0.12.2`；
5. 完成公开下载摘要、双 Python clean install、Browser/M10 分类负例以及公开 Starter 0.2.0 wheel 的真实
   PASS/FAIL chain；
6. 只有上述事实闭合后，才允许另一个 workflow PR 把 required lane 从固定 0.12.2 URL/SHA/version check
   迁移到固定 0.12.3 public coordinate。

branch 名称、ruleset、required-check 集、tag policy、资产集合、validation summary 及发布失败恢复规则都属于
后继合同面。本文不创建或替它们选定具体值。

## 5. current 0.13 source 与公开发行的独立义务

current main 的 `browser.py` 存在同一分类缺口，因此后继合同还必须允许在 current source 上独立实施相同的
封闭语义修正，并用 current-main 自己的完整回归与 Browser gate 取得资格。该 source correction 不继承
0.12.3 backport 的实现资格，反之亦然。

同时必须继续区分：

```text
corrected current source declaring 0.13.0
    != immutable public v0.13.0 wheel repaired
```

公开 `v0.13.0` tag 与 assets 保持只读。若未来要声明公开 0.13 Core 已修复，必须使用新的版本坐标、候选、
tag、Release、asset digest 与公开读回；预期可以是 0.13.x patch，但具体版本与发布范围不由本文决定。

对当前 R1 Parse authorization 来说，最小前提是：

```text
current source classification correction qualified
+
required Starter lane consumes a qualified public 0.12.3 distribution
+
the migrated exact main passes its own Public CI and Browser Smoke
```

公开 0.13.x 新发行是否必须先于 Parse authorization 完成，仍是后继合同必须显式裁决的独立问题；不得默认为
“修了 current source，所以 public 0.13.0 也修了”。

## 6. 诊断性可行性证据

本审计没有只凭版本号推断 0.12.3 可行。仓库外 diagnostic worktree 从精确 v0.12.2 release commit 起步，
只加入：

```text
closed exact mapping:
  net::ERR_NO_BUFFER_SPACE -> HostSocketNoBufferSpace

Network fact:
  retain original raw failure text

collector projection:
  network:<viewport> / HostSocketNoBufferSpace

version:
  0.12.2 -> 0.12.3
```

诊断 patch 与 wheel 身份为：

```text
v0.12.2 classification patch sha256 = bd5fb0a501fcff118ddea3039751098b5b716cdaacfddcd647c7683695418977
v0.12.3 coordinate patch sha256     = 9475099eaa74b2c1e240b7de42bde10be63485df6c025483f67d5db29a308efb
diagnostic wheel bytes              = 198965
diagnostic wheel sha256             = 68e84aee7dbc3adbdee7504fb4435c581805e5e7e051c99434637b0913f112ad
```

同一 patched source 的 focused Browser/bootstrap/CLI/Starter 相关矩阵得到：

| Python | mode/world | observation |
| --- | --- | --- |
| 3.10.6 | normal | `58/58 PASS` |
| 3.10.6 | `-O` | `58/58 PASS` |
| 3.13.13 | first patched normal | `7 failures / 58`, cause `UNKNOWN`, preserved |
| 3.13.13 | unmodified v0.12.2 control normal | `57/57 PASS` |
| 3.13.13 | fresh later patched normal | `58/58 PASS` |
| 3.13.13 | patched `-O` | `58/58 PASS` |

第一次 3.13 normal 的七个失败包含 Browser result 缺失、cleanup/cancel thread 未终结与 CLI stderr thread
exception。后继 control/PASS 不能覆盖首败，也不足以把它命名为 transient 或 patch regression；精确根因保持
`UNKNOWN`。该观察要求真实 Browser gate 与失败 Artifact 继续作为发布门，而不是要求扩大 timeout 或忽略失败。

诊断 wheel 随后与 source Starter 0.2.0 完成 24/24 normal、24/24 `-O` 合同测试和真实链。更强的独立观察
使用匿名下载并核验的公开 Starter wheel：

```text
tag                = starter-v0.2.0
asset              = veritrail_starter-0.2.0-py3-none-any.whl
public sha256       = ce6e9ea0730adc891aba97f8148fdb861fffdd5164989c980b5cbbaaa950771f
diagnostic Core     = veritrail-0.12.3-py3-none-any.whl
```

clean venv 中 `pip check`、Starter doctor 与兼容检查通过；真实 PASS/FAIL chain 得到：

```text
overall verdict        = PASS
intended PASS run      = COMPLETED / PASS
intended FAIL run      = COMPLETED / FAIL
Catalog                = COMPLETED / two runs / zero issues
Workbench              = zero console/http/page/request errors
cleanup                = both ports released / zero owned residue
acceptance.json sha256 = 570a853ac5f6b544e8d48168afb533a22cce739f7b39dcf94b39701dbe37faa6
```

完整仓库外 diagnostic summary SHA-256 为：

```text
8ae85fa25c96b037ec8666a9a9c0a24d612b4398c0b5461f93e7839b765e3d7e
```

第一次 build 尝试所在 venv 没有 `build` 模块，在产生 wheel 以前退出，保留为
`SETUP_FAILURE_NO_PRODUCT_CREATED`。随后使用独立 build venv，不能倒写前一次尝试为成功。

上述全部是 `DIAGNOSTIC_ONLY_NON_QUALIFYING`：没有 commit、candidate、tag、Release 或 public Core 0.12.3
asset。它们只证明“0.12.3 + unchanged public Starter 0.2.0”是有限且实际可运行的合同候选，不证明发布已经发生。

## 7. 明确拒绝的路径

后继合同不得：

- rerun、改写或重开 PR #243 original failure；
- retry `ERR_NO_BUFFER_SPACE` 直到 Subject PASS，扩大 timeout，或移除 required Starter lane；
- 移动、重制、覆盖或补传 v0.12.2、v0.13.0、starter-v0.2.0 的 tag / Release / assets；
- 从 current main 构建 0.12.3，或把 0.13 能力伪装成 0.12 maintenance patch；
- 以 current-source tests、source Starter、diagnostic wheel 或 compatibility range 替代公开产品资格；
- 仅修改 workflow URL/version check，然后声称新 consumer 已修复；
- 把 0.12.3 的合格结论扩张成 public v0.13.0 已修复；
- 在同一 PR 中顺手重发 Parse implementation authorization、实现 parser、选择 persistence 或修改 Fact wire。

## 8. 后继最小合同必须冻结的面

本文若取得资格，只授权起草一份 correction / release-consumer contract。该合同至少必须冻结：

1. 精确分类语义与 raw Network fact 保留规则；
2. current-main correction 与 v0.12.2-line backport 的独立 source identities；
3. maintenance branch / ruleset / merge / exact-tip gate authority；
4. 0.12.3 version、tag、Release、asset set、摘要与 create-new publication；
5. 双 Python normal / `-O`、Browser/M10 分类、wheel/sdist clean install 与真实公开 Starter wheel 验收；
6. public 0.12.3 readback 完成后 required lane 的单独 migration PR 与固定 URL/SHA/version check；
7. workflow migration 后 new exact-main Public CI / Browser Smoke 和失败 Artifact 保留；
8. public v0.13.x claim 是独立 publication obligation，不能从 current source 或 0.12.3 继承；
9. 何时才允许重新审查 Parse private implementation authorization。

具体 Python symbol、test helper、branch 名、release notes 文件名、0.13.x 版本号与发布日不在本文冻结。

## 9. 本候选停止线与资格链

本文只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_CORRECTION_RELEASE_CONSUMER_PRECONTRACT_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

本候选只允许 AGENTS、README、milestones 与本文四个文档文件。它必须完成 final-byte local gates、original PR
required checks、受保护合入、new exact-main Public CI / Browser Smoke、fresh README / doc222 / milestones
installed-product readback 与 independent reconciliation，才可成为 qualified precontract audit。

闭合以后仍须返回 CONTROL LOOP。唯一得到的下一阶段资格是审查并起草上述最小 correction /
release-consumer contract；runtime、tests、workflow、version、maintenance branch、ruleset、tag、Release、asset 与
Parse authorization 仍未开始。任何新反例若击穿 0.12.3 路线、branch governance 或两条发行线的独立性，应把本候选
打回，不得因诊断 PASS 强行推进。

## 10. 当前 final-byte 本地证据

最终四文件字节上的 Markdown/Schema suite 为：

| Python | mode | result |
| --- | --- | --- |
| CPython 3.10.6 | normal | `40/40 PASS` |
| CPython 3.10.6 | `-O` | `40/40 PASS` |
| CPython 3.13.13 | normal | `40/40 PASS` |
| CPython 3.13.13 | `-O` | `40/40 PASS` |

独立 static checker 的第一次运行对完整 `git status --short` 输出调用 `.strip()`，吃掉首行 tracked change 的前导
空格，随后把 `AGENTS.md` 误读成 `GENTS.md`，以 scope false positive 停止。第二次运行又把“候选文件 heading
唯一”错误扩大成“全仓所有 Markdown heading 唯一”，命中未修改的 `design-qa.md` 既有重复标题。两次均未修改
候选字节；收回 checker 自己的 observation scope 后，最终结果为：

```text
changed scope                         4/4 PASS
relative Markdown links              1098 / zero broken
UTF-8 without BOM / LF / final LF    PASS
changed-file fences / headings       PASS
candidate markers                    PASS
sensitive local paths                zero
frozen doc217 / doc218 blobs         unchanged
git diff --check                     PASS
```

这些本地 witness 只使 docs-only candidate 具备提交资格；它们不替代 original PR、exact-main、fresh
installed-product readback 或 independent reconciliation，也不把诊断 Core 0.12.3 变成 release candidate。
