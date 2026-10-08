# M10 0.12 maintenance dependency drift 反例审计

日期：2026-10-08

## 1. 审计结论

[文档 231](231-m10-maintenance-dependency-prerequisite-qualification-publication.md)证明：在它记录的 exact source、
exact lock bytes 与 2026-10-01 advisory observation 下，`core-0.12-maintenance@6ed18ae8...` 曾取得
dependency prerequisite qualification。该历史事实继续成立。

重新进入 CONTROL LOOP 后，workflow-only PR [#264](https://github.com/NoctilumeDev/VeriTrail/pull/264)
在同一 maintenance tip 上形成了新的 timed registry observation。原始 Public CI
[`37795167502`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/37795167502) attempt 1 的 Python、E3 与
wheel-only jobs 成功，Workbench tests、lint 与 build 也成功；随后 `npm audit --audit-level=moderate` 对精确 lock
报告 `1 moderate / 3 high`，Workbench job 与整条 run 因此为 `FAILURE`，Starter golden path 被跳过。

#264 已关闭、未合入、未 rerun、未改写 head。maintenance ref 仍为：

```text
core-0.12-maintenance
    = 6ed18ae8b3d8b98b6e5be7af709aa868590ee914
```

因此：

```text
old timed qualification
    remains historical fact

new timed advisory observation
    proves current dependency drift

current dependency drift
    blocks workflow-only bootstrap
```

文档 229 冻结的旧 dependency contract 不能直接消费这组新 advisory：它绑定旧 base、旧构造命令、四个允许
lock entry 与旧 final hash。current main 的 PR #262 只提供候选修复字节，不能向 maintenance line 转移 source、
construction、PR、attempt、merge 或 exact-tip authority。

本文只条件化发布：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

## 2. Exact source 与治理坐标

本轮重新读回：

| coordinate | exact value |
| --- | --- |
| current main | `9d311c640ff0ac2528e7b0da98c8dd01c9cabfdf` |
| maintenance ref | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` |
| maintenance tree | `42732643af743ca4aa9e801d61e5b49a04c4f54f` |
| `web/package.json` blob | `b38efdf88c439528a5b8af799e7ab8935037b3fc` |
| `web/package-lock.json` blob | `3b37cc4f29a74a370cd15e778953aedd372283b7` |
| lock SHA-256 | `6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E` |
| Public CI workflow blob | `c094d2cb84a2147e2b8bba1a7e76f140905d1a4d` |
| Browser Smoke workflow blob | `413f35ad9f768eb323d0058b82bdd8eaca177be1` |
| phase-one ruleset | `24216773`，active，no bypass，current user `never` |
| maintenance open PRs | `0` |

ruleset 仍禁止 deletion / non-fast-forward，并要求 PR 与全部 review thread resolved；required checks 仍为空。
这些事实证明治理边界没有漂移。它们不证明当前 dependency bytes 仍合格，也不授权 dependency write。

## 3. PR #264 与原始首败

#264 的精确身份为：

| field | value |
| --- | --- |
| base | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` |
| head | `585f98252d3c18727a0f19cb0eb1a28b362c9dc9` |
| commits | `1` |
| changed files | `.github/workflows/ci.yml`、`.github/workflows/browser-smoke.yml` |
| original Public CI | `37795167502` / attempt 1 / `FAILURE` |
| terminal state | `CLOSED / NOT MERGED` |

原始 run 的 job 结果为：

```text
Python 3.10 on Windows                  SUCCESS
Python 3.13 on Windows                  SUCCESS
E3 0.2 release download acceptance      SUCCESS
Wheel-only first run on Python 3.10     SUCCESS
Wheel-only first run on Python 3.13     SUCCESS
Workbench tests, lint, build, and audit FAILURE
Starter PASS/FAIL golden path           SKIPPED
```

Workbench 失败发生在 tests、lint、type-check/build 全部成功以后。官方 registry audit 报告：

| package | affected range | severity | advisory |
| --- | --- | --- | --- |
| `@vue/server-renderer` | `<3.5.42` | high | `GHSA-g2v6-rqmx-r4w6` |
| `vue` | `3.2.13 - 3.5.41`，经 server renderer | high | 同上 |
| `postcss-selector-parser` | `<7.1.6` | moderate | `GHSA-rj75-hqrm-r3gf` |
| `source-map-js` | `>=1.0.0 <1.2.2` | high | `GHSA-68fv-2mgg-jv7q` |

2026-10-08T15:11Z 的第一次本地 probe 使用 ambient npm registry，实际解析到 `npmmirror.com`；该 mirror 的 audit
endpoint 返回 `HTTP 404 / NOT_IMPLEMENTED`。这是 setup observation，不是零漏洞、产品失败或 registry 结论。随后显式
绑定 `https://registry.npmjs.org` 的 fresh probe 复现同一 `1 moderate / 3 high`，并读回三个 advisory 的 exact
ranges 与 `fixAvailable=true`。

## 4. 旧资格没有被改写

文档 231 保存的四条 exact-head / exact-tip dispatch run 与当时的 0-vulnerability observation 继续属于各自的
source、lock bytes、registry 时点与 run identity。后来出现 advisory 不会把旧 PASS 改写成当时的 FAIL。

反过来也一样：

```text
old audit PASS
    !=
current audit PASS
```

`npm audit` 是带 observation time 的外部 qualification input。#264 的新失败证明当前 workflow-only candidate 不能
取得 original PR qualification；它不证明文档 231 的历史记录虚假，也不证明 workflow filter、Python、Browser、Core
或 Workbench runtime regression。

## 5. 文档 229 的 authority 不能静默扩张

文档 229 的冻结 construction 明确绑定：

```text
base = f961930ae1e69d7d88849fa2b0d40befb3e94c89

npm update undici brace-expansion
    --package-lock-only
    --ignore-scripts
    --registry=https://registry.npmjs.org

allowed entries
    brace-expansion 5.0.12 / 2.1.7 / 2.1.7
    undici 7.30.0

final lock SHA-256
    6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E
```

当前 maintenance source 已移动到 `6ed18ae8...`，而新 advisory 涉及 Vue / server-renderer、
postcss-selector-parser 与 source-map-js。旧合同没有定义这些 entry 的版本选择、package manifest scope、构造命令、
expected patch、candidate identity 或新的 exact-tip qualification。因此不能把“合同曾冻结”解释为“未来任何 npm
advisory 都可在同一合同下顺手修复”。

这次需要重开的只是 dependency drift seam；旧 contract、旧 implementation 与旧 qualification history 保持不可移动。

## 6. current main 只提供候选证据

current main 的 PR [#262](https://github.com/NoctilumeDev/VeriTrail/pull/262) 已把相关解析结果更新为：

```text
vue                         3.5.43
@vue/server-renderer        3.5.43
postcss-selector-parser     7.1.6
source-map-js               1.2.2
```

官方 registry 当前可读回这些 exact versions 与 integrity，且它们位于已知修复范围。但是 #262 同时修改
`web/package.json` 与 `web/package-lock.json`，其 base、source graph、PR、CI、merge 与 exact-main gates 全部属于 main。

所以只能得出：

> 这些版本是 bounded candidate evidence；maintenance 是否需要同样的 manifest / lock scope、同样的构造命令与同样的
> final bytes，仍须由新的 precontract audit 重新证明。

## 7. 下一最小问题

下一刀只允许审计：

> 在 `core-0.12-maintenance@6ed18ae8...`、ruleset `24216773` 与当前官方 registry advisory surface 下，什么是
> 最小、可复算、不会借用 main authority 的 dependency-drift construction 与 qualification chain？

该 precontract audit 至少要回答：

1. exact source / package input / registry / npm identity；
2. direct manifest 与 transitive lock 哪些必须改变、哪些必须保持；
3. version selection 与完整 allowed-entry projection；
4. final-byte local gates、audit 时点与 setup failure 归层；
5. candidate topic、PR、manual dispatch 与 ordinary merge identity；
6. candidate-head 与 maintenance-tip witnesses 是否沿用文档 229 的结构，以及哪些 identity 必须重取；
7. #264 如何永久保留为 failed workflow-only candidate；
8. dependency 重新资格化以后，为什么仍须返回 CONTROL LOOP 才能重做 workflow bootstrap。

本文不选择命令、版本、文件 scope、final hash 或 PR 结构。

## 8. 明确未授权

本文不授权：

- 修改 `core-0.12-maintenance`、dependency bytes、workflow、ruleset、runtime、tests、timeout 或 budget；
- 直接复制、cherry-pick 或 merge PR #262；
- 创建 dependency topic / PR 或运行 `workflow_dispatch`；
- reopen、rerun、改 head、合入或删除 #264；
- 弱化、忽略或降低 `npm audit`；
- 把 dependency bytes 塞入 workflow-only #264；
- phase-two ruleset、host-socket backport、version/tag/Release、asset、public readback 或 consumer migration；
- Parse / Fact / Coverage、Schema、publisher、Bundle 或 `DECLARED_CLAIM_FIDELITY` 施工。

## 9. 本审计资格与停止线

本文与 README、AGENTS、milestones 只发布问题边界，不修改产品、workflow、dependency、ruleset、maintenance ref 或
frozen contracts。最终字节必须完成适用 Markdown/Schema 四格、relative links、UTF-8、fence/heading、required
markers、敏感路径、exact four-file scope 与 `git diff --check`。

当前 final-byte candidate 已完成：

- CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `tests.test_markdown`，各 `4/4 PASS`；
- UTF-8 without BOM、LF/final LF、balanced fences、duplicate heading 与 relative-link 检查；
- exact four-file scope：README、AGENTS、milestones 与本文；
- 108 个 heading、593 个 relative link 的只读结构检查；
- `git diff --check` PASS。

第一次自定义 Python structure-gate invocation 被命令安全策略在进程创建前拒绝，未执行、未改工作树；第一次
PowerShell link checker 又因仓库根文件的 parent path 为空而在首个 README relative link 终止。二者都保留为
audit-harness setup error；只修检查器的 root-path handling 后，同一文档字节完成上述结构门。

随后仍须经过本文自己的 original PR Public CI、受保护 main 合入与 new exact-main Public CI + Browser Smoke。只有
这些门闭合，`M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN` 才成为公开 qualified history，并只授权起草新的最小
dependency-drift precontract audit。

停止原则为：**old timed PASS 与 new timed FAIL 可以同时为真；新的 advisory 只能最小重开 dependency drift seam，
不能改写旧证据，也不能借机合并 workflow、release、consumer 或 Parse 施工。**
