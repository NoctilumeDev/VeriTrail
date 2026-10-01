# M10 0.12 maintenance dependency prerequisite 资格发布

日期：2026-10-01

## 1. 发布结论

[文档 229](229-m10-maintenance-dependency-prerequisite-contract.md)与
[文档 230](230-m10-maintenance-dependency-prerequisite-contract-freeze-publication.md)冻结的最小合同已经完成自己的候选、冻结与公开读回资格链。随后，exact Core 0.12 maintenance line 按该合同建立 one-file dependency candidate、两组不可借用的 manual-dispatch observations、ordinary merge 与 independent reconciliation。

本 publication 自己的 final bytes、original PR Public CI、受保护 `main` 合入、new exact-main Public CI + Browser Smoke、fresh README / doc229 / doc230 / 本文 / milestones installed-product readback 与 independent reconciliation 全部闭合后，以下目标状态才生效：

```text
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

该状态只说明 exact maintenance tip 已取得当前 dependency prerequisite。它不自动授权 workflow-only bootstrap、phase two、host-socket backport、0.12.3 version/tag/Release、consumer migration 或 Parse。

## 2. 冻结合同的资格历史

文档 229 的合同候选已经完成：

| gate | identity | result |
| --- | --- | --- |
| candidate PR | `#256`，head `c5e10ebd215d168293713714ef189742ff64d806` | exact 4-file docs-only diff |
| original Public CI | `36792226029`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `be1db09637b8b499269b6281c5ab744ddf27db02` | ordinary merge |
| exact-main Public CI | `36794128077`，attempt 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36794127955`，attempt 1 | `1/1 SUCCESS` |
| fresh installed-product readback | README / doc228 / doc229 / milestones | 4 independent `PASS` |

候选 canonical manifest：

```text
sha256_json  = dfd697f9544b5629adc86c83d3cb3e511942e0350a7c064a026564e9618c3942
sha256_bytes = a890203ae0a468c811446fd97826a55bf9dbaf6a4150b0d422e11f405eb3a01a
```

文档 230 的独立冻结发布已经完成：

| gate | identity | result |
| --- | --- | --- |
| freeze PR | `#257`，head `fc8d259570789c7c56f6e0a5c45bfbdecd2ed2a5` | exact 5-file docs-only diff |
| original Public CI | `36797434149`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `8099d162db78862beccdd84e88c22bec21b0e8b1` | ordinary merge |
| exact-main Public CI | `36799448250`，attempt 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36799448440`，attempt 1 | `1/1 SUCCESS` |
| fresh installed-product readback | README / doc229 / doc230 / milestones | 4 independent `PASS` |

冻结 readback 同时保留第一份 README formal observation 的错误 marker Plan，并使用新的 Plan/session 取得合格 PASS。独立核账证明该首败是 Plan literal 与 exact source 不匹配，不是 collector、Core 或 source-byte failure。最终 canonical manifest：

```text
sha256_json  = 1dcd412b0f298ad7a90d779b0d16bd5b5102f0f892838cb4c9f9484d3d4cf1a7
sha256_bytes = ff10d51d8aef37e10fb88b70759bf99c02f43d5e649b5b3ae8ddaf0017e35652
```

因此 `M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN` 已经是当前事实；合同冻结没有自动开始实现，后继仍从新的 exact main 重新经过 CONTROL LOOP 才取得最小施工权。

## 3. Exact implementation source 与 local gates

控制回路重新确认：

| coordinate | value |
| --- | --- |
| maintenance base | `f961930ae1e69d7d88849fa2b0d40befb3e94c89 = v0.12.2^{}` |
| base tree | `e0ded371266ac80b936fcbf5e00515a75dbf0950` |
| base `web/package.json` blob | `b38efdf88c439528a5b8af799e7ab8935037b3fc` |
| base `web/package-lock.json` blob | `b52f8900b3c44ec978d358a5fff9e7fb852fbf34` |
| phase-one ruleset | `24216773`，active，无 bypass，current user `never` |
| parallel maintenance PR | none |

fresh topic `chore/m10-maintenance-dependency-prerequisite` 使用 npm `11.19.1`、registry `https://registry.npmjs.org` 与合同冻结的 targeted update。最终只修改 `web/package-lock.json`：

```text
brace-expansion = 5.0.12 / 2.1.7
undici           = 7.30.0
lock SHA-256     = 6a6f5d09c97b7c01501d04705575cda11155840cf715ee88817711062a7ea01e
diff             = 12 insertions / 12 deletions
```

串行 local gates：

| gate | result |
| --- | --- |
| fresh `npm ci --ignore-scripts` | PASS |
| Workbench regression | 14 files / 172 tests PASS |
| lint | PASS |
| type-check + production build | PASS |
| timed `npm audit --audit-level=moderate` | exit 0；0 vulnerabilities |
| dependency tree / four-entry projection | exact match |
| exact one-file diff / `git diff --check` | PASS |

Dependabot Alerts API 明确返回仓库未启用；该外部能力错误被保留，但没有替代合同指定的 timed `npm audit` witness。

## 4. Candidate identity 与 exact-head qualification

candidate commit：

```text
head   = 823add7850867754db1fea5b484c083678be0873
tree   = 42732643af743ca4aa9e801d61e5b49a04c4f54f
parent = f961930ae1e69d7d88849fa2b0d40befb3e94c89
blob   = 3b37cc4f29a74a370cd15e778953aedd372283b7
```

PR [#258](https://github.com/NoctilumeDev/VeriTrail/pull/258) 的 base/head、1 commit、1 file 与 lock bytes 独立读回一致。该 PR 没有 original required checks；合同要求的 manual-dispatch observations 是：

| workflow | run | event / attempt | exact head | denominator | result |
| --- | --- | --- | --- | --- | --- |
| Public CI | `36803540792` | `workflow_dispatch` / 1 | `823add7850867754db1fea5b484c083678be0873` | 7/7 | SUCCESS |
| Browser Smoke | `36803550201` | `workflow_dispatch` / 1 | `823add7850867754db1fea5b484c083678be0873` | 1/1 | SUCCESS |

两条 run 前后 topic ref 均绑定 exact candidate head；logs 与 Artifact metadata 已保留。它们是 candidate-head witnesses，不是 original PR CI，也不转移给 merge tip。

## 5. Protected merge 与 exact-tip qualification

fresh pre-merge reconciliation 再次确认 PR `OPEN / CLEAN / MERGEABLE`、0 review threads、exact base/head、one-file scope、maintenance base 与 ruleset 未漂移。PR #258 以 ordinary merge 形成：

```text
merge   = 6ed18ae8b3d8b98b6e5be7af709aa868590ee914
tree    = 42732643af743ca4aa9e801d61e5b49a04c4f54f
parent1 = f961930ae1e69d7d88849fa2b0d40befb3e94c89
parent2 = 823add7850867754db1fea5b484c083678be0873
```

GitHub 自动删除了 merged topic ref；文档 229 第 8 节没有把 post-merge topic-ref retention 设为门。protected maintenance ref 精确指向 merge commit，tree 与 lock bytes 未变。merge 后新建的 exact-tip observations 为：

| workflow | run | event / attempt | exact head | denominator | result |
| --- | --- | --- | --- | --- | --- |
| Public CI | `36804634994` | `workflow_dispatch` / 1 | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` | 7/7 | SUCCESS |
| Browser Smoke | `36804645585` | `workflow_dispatch` / 1 | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` | 1/1 | SUCCESS |

maintenance ref 在两次 dispatch 前后和终结后均保持 exact merge SHA。candidate 与 tip 四条 run ID 互不复用，Public CI logs 各自重新观察到 0 vulnerabilities。

## 6. 独立 reconciliation 与保留失败

独立 verifier 同时核对冻结合同 manifest、local gates、candidate commit/ref/PR、ruleset、ordinary merge topology、四条 workflow runs、完整 job denominator、logs / Artifact metadata、maintenance ref 与最终 lock bytes。normal / `-O` 生成同一 canonical manifest：

```text
sha256_json  = 6ca3a967ed8b39f0aabd88fcf2553f2d4d774c4769663d53c4ae53bce0b5742c
sha256_bytes = 43f47d29a15275fa2bd6110973e5eb14379247e1929b2f34f8b9e755b1d91d4c
```

以下非资格观察保持原身份：

- Dependabot Alerts API disabled；
- 首次 worktree tree probe 的 PowerShell brace quoting error；
- Codex PR Artifact attachment 超过 100 identities；
- 首次 pre-merge PowerShell helper 的 argument binding error；
- 首次 post-merge verifier 错误增加 topic-ref retention 门。

后续成功没有把这些事件改写成“未发生”，也没有借它们改变产品 gate。

## 7. 本 publication 的 final-byte local gates

本 publication 只修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 229 / 230、
architecture DOT/SVG、runtime、tests、workflow、ruleset、maintenance ref 与 dependency bytes 保持不变。

最终字节在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格执行只读 documentation gate，结果一致：

```text
tests.test_markdown = 4/4 OK
files               = 4
headings            = 109
relative links      = 586
```

UTF-8 无 BOM、LF/final LF、balanced fences、duplicate headings、required markers、relative links、sensitive
paths、exact four-file scope、frozen contract/architecture continuity 与 `git diff --check` 均成立。

第一次 PowerShell 调用因 quoted executable 缺少调用运算符而在 shell parse 阶段终止；第一次 Markdown test
调用因未设置源码树 `PYTHONPATH` 而在 test import 前终止。两次均作为 operator/test-startup error 保留；随后按仓库
源码布局设置 process-local `PYTHONPATH=src`，没有改变测试、产品或合同标准，四格均取得上述结果。

## 8. Publication gate 与下一停止线

本文只发布已经闭合的 dependency prerequisite。本文自己的资格链闭合以前，公开状态仍停在：

```text
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_PREREQUISITE_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_BOOTSTRAP_BLOCKED
```

本文最后门闭合后，下一动作也不是自动修改 workflow。必须返回 CONTROL LOOP，从 exact maintenance tip `6ed18ae8...` 重新读取 ruleset、并行 PR、advisory surface 与文档 223/224/225–227 的停止线；只有原 workflow-only bootstrap 问题仍成立，才允许使用全新 branch/PR identity 起草候选。PR #252 永久保持关闭、未合入、失败身份，不得 reopen、rerun、改 head 或借用。

本文不授权 phase-two ruleset、host-socket backport、version/tag/Release、asset、public consumer migration、main required lanes、Parse / Fact / Coverage、Schema、publisher 或 Bundle。
