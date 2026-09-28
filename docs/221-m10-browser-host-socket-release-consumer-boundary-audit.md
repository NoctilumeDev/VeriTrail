# M10 Browser 主机 socket 分类与发行消费边界审计

日期：2026-09-29

> 当前条件状态：
> `M10_BROWSER_HOST_SOCKET_CLASSIFICATION_RELEASE_CONSUMER_BOUNDARY_AUDIT_CANDIDATE /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED`
>
> 精确基线：`main@23f9825e61791a78056d5154e4dfd3626a1167b1`，Git tree
> `ae1496ba1978ddb40b3a74e414b4e6f58f9bddd5`
>
> 影响层级：`L3_SYSTEM_AUDIT + L2_DISTRIBUTION_IDENTITY_AUDIT + L0_DOCUMENTATION`。本文不修改
> Core runtime、tests、workflow、Starter、timeout、retry、Schema、public Evidence、tag、Release 或 R1 Parse
> 合同，也不授权新的 Core / Starter 版本、兼容范围迁移或 parser runtime。

## 1. 触发事实与首败身份

[文档 219](219-r1-parse-private-implementation-feasibility-audit.md)已经完成自身候选、受保护合入、new exact-main
双门、fresh installed-product readback 与 independent reconciliation，因此其 feasibility 结论是 qualified history。
后继 docs-only Parse private implementation authorization PR
[#243](https://github.com/NoctilumeDev/VeriTrail/pull/243) 没有取得同样资格。

PR #243 的 base、head 与 original Public CI 分别为：

```text
base = 23f9825e61791a78056d5154e4dfd3626a1167b1
head = c28860fb2b3acd21c15216e3c7a69e3b3e573f16
run  = 36449716998 / attempt 1
```

十一项检查中十项成功，唯一失败是 `Starter PASS/FAIL golden path` job `109027269096`。原 workflow 没有
rerun，candidate head 没有改写；PR #243 已关闭且未合入。因此：

```text
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
    = qualified history

R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED
    = did not take effect

R1_PARSE_FULFILLMENT_IMPLEMENTATION
    = NOT_STARTED / NOT_AUTHORIZED
```

后继观察、维护或重新发布都不得把 run `36449716998` 改写为通过。

## 2. Artifact 恢复出的精确失败世界

失败 job 上传了 `starter-single-webapp-s1-failure-36449716998-1`：

```text
artifact id            = 10982779354
archive sha256         = b43c8c284924ca03c3a50f78ae724e309ac2b14cbef272887684269fc4c62e10
browser Evidence sha256= de9f7c8c3174ae4eee6bc51c7cd61b4f8e394276726181484356e8a79d06542d
```

Starter PASS world 最终得到 `COMPLETED / FAIL`。桌面 viewport 的 document 导航为 `200`，标题、输入与点击步骤
通过；点击触发的第一个 loopback `/data.json` fetch 随后失败：

```text
failure    = net::ERR_NO_BUFFER_SPACE
status     = null
finished   = false
page error = Failed to fetch
```

`expect_text` 因而在既有 10 秒操作边界内失败。紧随其后的移动 viewport 在同一服务、同一端口和同一 Plan 下
重新导航并请求同一个 `/data.json`，两次均为 `200`，全部业务步骤与 screenshot 成功。与此同时：

```text
application readiness      = READY
subject changed            = false
resource sampling complete = true
cleanup complete           = true
host available memory min  = 13278.883 MiB
browser peak RSS           = 211.285 MiB
collection_errors          = []
```

前一份 exact-main Public CI run `36443544885` 的同一 Starter lane 使用相同 runner image、Python 3.13.15、
Playwright 1.62.0、Chromium 151.0.7922.34、Node 22.23.2、Plan 与 Profile，并取得完整 PASS。该对照只排除
docs patch 或已记录依赖版本变化足以解释失败；它不覆盖本次首败，也不证明底层原因可复现。

## 3. 已知分类矛盾与仍未知的根因

Microsoft 将 `WSAENOBUFS / 10055` 定义为本机无法完成 socket 操作，因为没有足够 buffer space 或相关队列
已满；Chromium 在 Windows 上把该错误映射为 `ERR_NO_BUFFER_SPACE`。因此该精确 error code 支持：

```text
Browser host/client-side transport resource failure occurred
```

它不支持：

```text
the observed application returned an incorrect business result
```

当前 Browser Adapter 会把 failure 保存进 Network 事实，却不会把该 host-local error 放进
`collection_errors`。M10 后继逻辑于是只看到：

```text
collection_errors = []
all_steps_passed  = false
capture_complete  = false
```

并形成：

```text
BROWSER_HARD_FAILURE / COMPLETED / FAIL / SUBJECT
```

既有 M10 边界要求 Browser / observer / collector 自身的非预期失败 fail closed 为 `COLLECTOR_ERROR`，不能冒充
Subject business failure。因此这里存在真实的 classification defect。能够唯一确定的是 host-local socket failure
发生且被归入了 Subject；到底是 buffer、queue、临时端口、runner 上其他资源压力还是它们的组合，现有 Artifact
不足以恢复，精确底层根因保持 `UNKNOWN`。

外部语义依据：

- [Microsoft Windows Sockets error codes](https://learn.microsoft.com/windows/win32/winsock/windows-sockets-error-codes-2)
- [Chromium: WSAENOBUFS -> ERR_NO_BUFFER_SPACE](https://chromium.googlesource.com/chromium/src/net/+/285728c206d899dd545dbe0b77d473594bce51f7%5E%21/)

## 4. 门禁实际消费的不是 current main

进一步核账证明，失败的 Starter lane 不运行 PR checkout 中的 Core runtime。workflow 会匿名下载并校验：

```text
Core distribution = v0.12.2 release wheel
wheel sha256       = 3a42f28db6f4ed12351dade3fbb6f57fa1d5aa3fdd6d28210492f676bc1562de
Starter source     = checkout editable Starter 0.2.0
declared dependency= veritrail>=0.12,<0.13
```

job 还显式验证 `veritrail.__version__ == 0.12.2` 且 Core module 不在 checkout。当前 source 与 Latest Core Release
则是 `0.13.0`；Starter 0.2.0 的 runtime doctor 会拒绝 Core 0.13。由此得到：

```text
current-main source correction
    != correction of the product identity that failed #243

same browser.py defect in current source
    != authority to rewrite v0.12.2 release bytes

same semantic fix candidate
    != same distribution qualification
```

[Core 0.12.2 发布与公开读回事实](76-core-v0.12.2-release-readback-facts.md)明确规定，后继 payload 修改必须使用
新的提交、合同与版本坐标，不能移动或重制 `v0.12.2`。[Core 0.13.0 发布补全合同](100-core-v0.13.0-acceptance-api-release-contract.md)
也只授权当时已经冻结的 0.13.0 增量，并保持历史 Release 只读。当前没有合同授权：

```text
Core 0.12.x new maintenance release
Core 0.13.x patch release
Starter compatibility range expansion
new Starter release
Starter lane distribution migration
release asset replacement
```

因此本次不能把一个只改 current source 的补丁描述成“修复了 #243 的实际产品”。

## 5. 诊断性实现与 setup 观察的资格

审计期间曾在未提交 worktree 中为精确字符串 `net::ERR_NO_BUFFER_SPACE` 草拟封闭映射，使原始 Network
failure 继续保留，同时增加 `network:<viewport> / HostSocketNoBufferSpace` collector error。相关 Browser、bootstrap、
CLI 与 Starter source-level tests 在 Python 3.10.6 / 3.13.13 normal / `-O` 四格各 `58/58 PASS`。

该 patch 没有 commit、没有 push，已经从候选 worktree 撤回；诊断副本仅保留在仓库外，SHA-256 为：

```text
edefcdca449a4572a8b7a26a2a5f0d021cf20a76263fb7ec896aba10746491ac
```

这些结果只证明 current source 存在一个窄实现候选；它们不证明 v0.12.2 release wheel 已改变，也不证明 Starter
真实门会消费该候选。

另一次尝试用 current source 直接运行真实 Starter chain，在正式产品 lifecycle 前被
`veritrail-starter doctor` 以 Core 0.13 不满足 `>=0.12,<0.13` 拒绝。该观察属于 setup / product-identity
precondition failure，没有创建 M10 Plan/session/Evidence，不能冒充修正后的 Starter product run。

## 6. 当前问题边界

现在有两个同时成立、不能互相替代的缺口：

```text
runtime semantic defect
    exact host-local request failure can be misclassified as SUBJECT

distribution consumer boundary
    the required Starter lane consumes immutable Core v0.12.2,
    while current main is Core 0.13.0 and Starter 0.2 rejects it
```

因此当前最小合法问题不是“把一行映射提交到 main”，而是：

> 在不移动历史资产、不放宽 required gate、不加入 retry/timeout 规避、且不把 source test 当作 released-product
> 证据的前提下，哪个新的 Core / Starter / CI 消费坐标有资格承载这项 classification correction？

以下方案都只是待审解空间，不是本文的决定：

```text
new bounded Core maintenance release
new Core patch coordinate plus compatible Starter release
Starter consumer migration to an already compatible released Core
separate correction contract spanning runtime and distribution identity
```

本文也不证明每一种方案都可行。尤其禁止：

```text
rerun #243
rewrite or reopen #243 head
retry ERR_NO_BUFFER_SPACE until PASS
increase timeout or remove Starter required gate
move v0.12.2 / v0.13.0 tags or replace assets
claim current-source PASS repaired the released v0.12.2 product
```

## 7. 本候选的停止线与资格

本文只条件化发布：

```text
M10_BROWSER_HOST_SOCKET_CLASSIFICATION_RELEASE_CONSUMER_BOUNDARY_AUDIT_CANDIDATE
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

本候选只能修改 AGENTS、README、milestones 与本文。它必须完成 final docs/static gates、original PR required
checks、受保护合入、new exact-main Public CI / Browser Smoke、fresh README / doc221 / milestones installed-product
readback 与 independent reconciliation，才可成为 qualified problem boundary。

闭合以后仍须返回 CONTROL LOOP。唯一可重新审计的下一问题是最小 correction / release-consumer precontract；
在它自己取得 authority 以前，不得提交 runtime/test/workflow/Starter/version 变更，也不得重建 Parse implementation
authorization。Parse contract 与 feasibility history 不因本次失败失效；失效的是 #243 的 qualification 与由它条件化
发布的 implementation authority。

## 8. 当前本地候选证据

第一次四格命令没有为新 worktree 绑定 `src`，四条 lane 都完成 37 个不依赖 Core import 的测试后，以
`ModuleNotFoundError: veritrail` 拒绝 `tests.test_markdown`。该观察属于 test setup failure，没有形成 40-test
suite 结果。使用 command-local `PYTHONPATH=<worktree>/src` 绑定 exact checkout source 后，最终四文件字节得到：

| Python | mode | result |
| --- | --- | --- |
| CPython 3.10.6 | normal | `40/40 PASS` |
| CPython 3.10.6 | `-O` | `40/40 PASS` |
| CPython 3.13.13 | normal | `40/40 PASS` |
| CPython 3.13.13 | `-O` | `40/40 PASS` |

独立 static checker 的第一次运行把文档 89 中 Markdown code block 内的正则片段
`(?:[A-Za-z0-9-]{0,38})` 误识别为 relative link，因此以 checker false positive 停止；它没有修改候选字节。
只收窄 checker 的 Markdown-link 识别后，最终结果为：

```text
changed scope                         4/4 PASS
relative Markdown links              1053 / zero broken
UTF-8 without BOM / LF / final LF    PASS
balanced fences / unique headings    PASS
candidate markers                    PASS
sensitive local paths                zero
git diff --check                     PASS
```

冻结 doc217 / doc218 的 Git blob 继续分别为
`0032f6c3c4b90f78f714920982fa373bbb5cb13d` 与
`9fa5e1884a3edcb614d3bf9f1218c57acfc36a36`。这些本地结果只使 docs-only candidate 具备提交资格；
它们不替代 original PR、exact-main、installed-product readback 或 independent reconciliation，也不授权
runtime/distribution correction。
