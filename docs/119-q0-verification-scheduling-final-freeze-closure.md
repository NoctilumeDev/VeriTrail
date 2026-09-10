# Q0 Quick Verification Scheduling 最终冻结闭环

> 状态发布目标：`Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY`
>
> 修复后基线：`main@c2f488e8274b43dea6ad39402a94c3f6a1ee7753`

本闭环不重新设计 Q0，也不实现 Q。它只把蓝图候选、公开展示反例、冻结发布失败、独立地基修正与新
exact-main 证据组织成一条可审计因果链，然后恢复此前被停止的 Q0 冻结资格。

## 1. 冻结对象

Q0 冻结对象仍然只有[文档 116](116-q0-quick-verification-scheduling-blueprint.md)定义的候选语义：

```text
Q = Quick / Verification Scheduling Plugin

goal:
reduce redundant recomputation and removable serialization

not authority:
no SAFE_TO_SKIP
no gate weakening
no Evidence redefinition
no Core Verdict
```

Q 与 Review Attention R 仍是不同顶层轨道；Q 不反向要求 R1 增加 base/head diff、change blast radius 或
Attention ranking。`Prove no less. Repeat no more.` 是设计约束，不是当前已实现能力。

## 2. 候选与展示修正

Q0 候选提交 `a5688558aca92b30e17e4bf041e2dc8ded759a48` 经 PR #91 原始 Public CI 11/11 合入
`main@f713cf5eeb4e88f2a759082c49a1eb973f634982`。首次严格匿名读回随后发现
[能力地图](114-capability-boundary-and-system-map.md)中的 Mermaid 需要额外 GitHub 渲染子资源，P2 因
`UNEXPECTED_PAGE_NAVIGATION` 保持 `PARTIAL`；该 session 没有被接受为冻结证据。

PR #92 只把 Mermaid 改为等价静态文本，没有改变能力关系。其原始 Public CI 11/11 后合入
`main@ca1ce9fbf0dafab74a681fe761b1cee07d4b5269`；该 exact main 的 Public CI、Browser Smoke 与
README、文档 114、文档 116 的三次匿名产品读回均成立。

这些事实已经由[文档 117](117-q0-verification-scheduling-freeze-publication.md)记录，旧 `PARTIAL` 不被
后继成功覆盖或删除。

## 3. 第一次冻结发布为何没有生效

文档 117 的状态提交 `a32f98a903f5befa27d03e422662da3cbb5051b7` 经 PR #93 原始 Public CI 11/11
合入 `main@39b5eb37ebd8f2e502925f2a026be2ccf4c25101`。从该 exact main 对 README、文档 117 与
milestones 的三次匿名产品读回均为 `COMPLETE / PASS`，Browser Smoke 也为 1/1 `SUCCESS`。

但是同一 SHA 的原始 Public CI run
[34419511498](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34419511498) 只有 10/11；E3 0.2
Release 下载验收连续五次收到 HTTP 500，并在约 31 秒后退出，而 60 秒绝对恢复预算仍剩约 29 秒。

因此：

```text
anonymous readback PASS
+ Browser Smoke PASS
+ 10 other Public CI jobs PASS
!=
required exact-main gate complete
```

Q0 当时只能保持 `Q0_FREEZE_CLOSURE_HELD`。PR #93 的绿灯和读回不能替代失败的 exact-main gate，原始
run 没有 rerun。

## 4. 独立地基修正

[文档 118](118-release-download-recovery-deadline-correction.md)把问题收敛为：有限退避表被旧实现误作
最大尝试数，形成了一个比绝对恢复 deadline 更短的隐式停止条件。

独立提交 `0c83cf0237f6ddfc3f25adcb1da09f5a23416009` 只让最后一个正退避阶段成为等待上限，使所有后继尝试
继续消费同一个 monotonic deadline。它没有修改 Q0/P4、Release 坐标、冻结 SHA-256、验收阈值、永久错误
分类、摘要校验或不覆盖发布语义。

该提交经 [PR #94](https://github.com/NoctilumeDev/VeriTrail/pull/94) 的原始
[Public CI run 34422552275](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34422552275) 在 attempt 1
取得 11/11 `SUCCESS`，随后以 merge commit
`c2f488e8274b43dea6ad39402a94c3f6a1ee7753` 合入受保护 `main`：

```text
tree:
b4c560a969e3839d574483a939a5ce0edfc69b47

parents:
39b5eb37ebd8f2e502925f2a026be2ccf4c25101
0c83cf0237f6ddfc3f25adcb1da09f5a23416009
```

修复后的 exact main 又在原始 attempt 1 上取得：

| Gate | Run | Result |
| --- | --- | --- |
| Public CI | [34423412884](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34423412884) | 11/11 `SUCCESS` |
| Browser Smoke | [34423412894](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34423412894) | 1/1 `SUCCESS` |

PR 与主线门禁是两组独立事实；其中 E3 下载门在两组中均重新执行，没有用本地探针或前序 run 替代。

## 5. 修复后 exact-main 匿名产品读回

从 detached `main@c2f488e8274b43dea6ad39402a94c3f6a1ee7753`，在无 `GITHUB_TOKEN`、`GH_TOKEN` 或
`VERITRAIL_GITHUB_TOKEN` 的环境中，固定执行：

```text
github-api
-> github-public-render
-> exact snapshot handoff
-> Acceptance Core
```

三页使用独立 sealed Plan 与独立 paired session：

| 页面 | Viewport | Plan digest | Session | Evidence SHA-256（API / Render） | Core report digest | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| README | desktop | `b2f52111ed23e59baf7b87c69323150f339a192fad909fcf0396e6a41746247c` | `github-paired-822b05723a6e4b448526698ec0ecc8c9` | `98d1fdeacf81a8848f6db5e1ce988f50f48cb13d7d7c635c82cc20cbb8e568d5` / `46c70f64bc0f637a8445697839b0d14b44437e3f9ae80f8baeda68b1fe325d54` | `11d44ad1c2e4f2f5904858ff41d1e3c87fdb3782583e34dac9364a00a70506a9` | `PASS` |
| 文档 118 | narrow | `ec08acff9c1fe64bdf17acf0a7278766398b833df8fba43afe07d547d8163157` | `github-paired-84ae32c9c70e495cbe261775135b0739` | `de640420e1a7f48069afd1e1e778cbe40e42f418247e259061eecc3258bec3a0` / `a2cf9876f4f11a8273e7940b4c20aa1842d6b53bfa1e01d3f1c19486cf2deed2` | `65b3b690cc2cbc1d7c90d6ea543bafa55bf4ebbc1c090375df77c28c2a5025ae` | `PASS` |
| milestones | narrow | `a87133bdb15ec1455d9b6240b55034469849959b5c528740805d9b7d3c949a9a` | `github-paired-c1838e5abee74b32854692dd7fda4a00` | `72d424abd304409831489c073b99a2dbb0db48b411341253966cc02ec4df7d30` / `8d8ae2b2c9ec1514872a645801334c3cd055a808092141e03f9c663868e71b75` | `9ccdf54e0d80a4ad0d85e9c494d0b8850acae322c6a585aa462952c2e9c364d7` | `PASS` |

汇总摘要为：

```text
db09606083909386d769969ae9b1a5fd0177921682a59b4f78cf4135f43494d3
```

三条链均满足 P1/P2 `PUBLISHED / COMPLETE`、固定 P1 -> P2 顺序、同 pair session、独立 request seal、
exact commit、requested/final URL 一致、三样本稳定、active streams 为零，以及空
`errors / conflicts / cleanup_errors / coverage_reasons`。README 与 milestones 的
`Q0_FREEZE_CLOSURE_HELD`、文档 118 的 `attempt limit` 均至少出现一次。

## 6. 当前未实现边界

本闭环仍然没有创建：

```text
Q Schema
Q source package
Q CLI
impact planner
Evidence reuse cache
isolated execution lanes
deterministic join runtime
Q workflow / tag / Release
SAFE_TO_SKIP authority
```

README 读者骨架和 SVG 属于后继独立展示施工，R1 Schema 属于 Review Attention 主线；二者均不构成 Q0
冻结证据，也不能叠加到本 closure 提交。

## 7. 本状态发布的最后门

本次只允许 AGENTS、README、milestones 与本文变化。它自身仍须完成：

1. docs-only PR 原始 Public CI 11/11；
2. 受保护主线合入；
3. 新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1；
4. 从该 exact main 对 README、本文和 milestones 的 fresh anonymous 产品读回。

只有以上事实全部成立，当前状态才是：

```text
Q0_BLUEPRINT_FROZEN
Q_IMPLEMENTATION_NOT_STARTED
NO_GATE_SKIP_AUTHORITY
README_RESTRUCTURE_ALLOWED
R1_SCHEMA_NOT_RESUMED
```

下一步只能从新的 exact main 独立重构 README 读者骨架；SVG 必须等文字骨架稳定后再单独施工。两项展示
闭环完成以后，才返回 Review Attention R1 Schema。
