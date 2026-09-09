# Q0 Quick Verification Scheduling 蓝图冻结状态发布

> 状态发布目标：`Q0_BLUEPRINT_FROZEN / Q_IMPLEMENTATION_NOT_STARTED / NO_GATE_SKIP_AUTHORITY`
>
> 候选蓝图：[文档 116](116-q0-quick-verification-scheduling-blueprint.md)
>
> 候选闭环基线：`main@ca1ce9fbf0dafab74a681fe761b1cee07d4b5269`
>
> 影响层级：`L0_DOCUMENTATION + L2_CONTRACT_STATUS`；本文只发布已经发生的蓝图候选、反例修正、
> 远端门禁、受保护主线合入与匿名产品读回事实，不创建 Q Schema、源码、CLI、缓存、调度器、执行 Lane、
> CI 修改、标签、Release 或空插件目录

## 1. 发布裁决

Q0 已把 Verification Scheduling 从 Review Attention、Platform Evidence 和 Core Verdict 中分离出来，
并冻结候选能力的身份、权威、依赖方向、反例、实现前置门与拒绝边界：

```text
Q = Quick / Verification Scheduling

can:
    plan bounded verification work
    bind exact reusable Evidence candidates
    arrange isolated execution lanes
    retain deterministic join provenance

cannot:
    output SAFE_TO_SKIP
    weaken or redefine a Gate
    redefine Evidence
    produce PASS or Core Verdict
    require Review Attention R1 to become a diff engine
```

`Quick` 只表示减少无效重算与可解除的串行等待，不是性能承诺，也不授予减少证明义务的权力。Q 缺失、
失败或卸载时，完整串行验证与 Core 判断语义必须保持成立。

候选蓝图已经完成原始远端门禁和受保护主线合入。第一次 exact-main 产品读回又发现能力地图依赖 GitHub
Mermaid 子资源，严格只读 P2 Collector 因此正确保留 `PARTIAL`，冻结没有继续。后继单文件修正只把关系图
改为等价静态文本，再次通过原始远端门禁、受保护主线合入、合入后 exact-main 门禁和三次 fresh
anonymous 产品读回。本文发布这条包含失败与修正的完整因果链，不把后续成功写成第一次就已成立。

本文自身仍须完成原始远端门禁、受保护主线合入和合入后 exact-main 产品读回；只有最后门全部成立，
状态发布目标才成为当前主线事实。任一新反例仍可否决冻结资格。

## 2. 蓝图候选身份

| Identity | Exact value |
| --- | --- |
| Candidate base | `5807c53e87ea385d7a1c9de2bc32a64faeafc00e` |
| Candidate commit | `a5688558aca92b30e17e4bf041e2dc8ded759a48` |
| Candidate tree | `1e82af8398e9a6cfd0c8176b0b5e4fa371dacec7` |
| Pull request | [#91 `docs: define Q0 verification scheduling blueprint`](https://github.com/NoctilumeDev/VeriTrail/pull/91) |
| Merge commit | `f713cf5eeb4e88f2a759082c49a1eb973f634982` |
| Merge parents | `5807c53e87ea385d7a1c9de2bc32a64faeafc00e` + `a5688558aca92b30e17e4bf041e2dc8ded759a48` |
| Merge tree | `1e82af8398e9a6cfd0c8176b0b5e4fa371dacec7` |

PR #91 只修改 `AGENTS.md`、`README.md`、R 轨 Plan、里程碑索引并新增文档 114、116；没有 Schema、
源码、CLI、缓存、调度器、执行 Lane、workflow、标签或 Release。它于 `2026-09-09T23:11:35Z`
通过正常受保护分支流程合入，候选 tree 与 merge tree 一致，没有在合入时改写候选 payload。

## 3. 蓝图候选原始门禁

PR #91 的 Public CI run
[`34414889151`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34414889151) 在 attempt 1
生成并完成 11 个 job，全部为 `SUCCESS`：

1. Workbench tests, lint, build, and audit；
2. Python 3.10 on Windows；
3. Python 3.13 on Windows；
4. E3 0.2 release download acceptance；
5. Wheel-only first run on Python 3.10；
6. Wheel-only first run on Python 3.13；
7. GitHub Evidence wheel-only on Python 3.10；
8. GitHub Evidence wheel-only on Python 3.13；
9. Acceptance Core freeze on Python 3.10；
10. Acceptance Core freeze on Python 3.13；
11. Starter PASS/FAIL golden path。

没有失败 job 被 rerun 覆盖，也没有用其他 PR 或旧 main 的绿灯替代候选 head。

候选合入后的 `main@f713cf5eeb4e88f2a759082c49a1eb973f634982` 还完成了：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34415808732`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34415808732) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34415808763`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34415808763) | 1 | `1/1 SUCCESS` |

这些绿灯证明候选在主线门禁中成立，但不能替代公开渲染读回。

## 4. 公开读回反例与单文件修正

第一次从 `main@f713cf5eeb4e88f2a759082c49a1eb973f634982` 使用公开 Core `0.13.0` 与
GitHub Evidence Plugin `0.1.0` 读回时，出现了两个不同问题：

1. README 首次 Plan 请求了源码并未声明的 `Q0_BLUEPRINT_CANDIDATE` 字面标记，Collector 忠实记录
   occurrence 为 0；该 Plan 没有被改写成成功。随后以 README 实际公开口号为预声明标记的新 session
   才取得 `PASS`。
2. 能力地图正文、三样本和 `Q0_BLUEPRINT_CANDIDATE` 标记均稳定，但 GitHub Mermaid 渲染触发
   `viewscreen.githubusercontent.com/markdown/mermaid` 子资源。P2 的只读导航边界保留
   `NETWORK_POLICY_BOUNDARY / UNEXPECTED_PAGE_NAVIGATION`，coverage 为 `PARTIAL`，因此没有取得冻结资格。

第二个问题说明“页面正文可见”不等于“严格公共读回已经完整”。修正 PR 只更改展示机制：

| Identity | Exact value |
| --- | --- |
| Correction base | `f713cf5eeb4e88f2a759082c49a1eb973f634982` |
| Correction commit | `3f34f971b97d65cb3f5440ca7354bbd36c58e37b` |
| Correction tree | `67185359fd2a26ca2148ba4b380196673f9f200e` |
| Pull request | [#92 `docs: make Q0 system map self-contained`](https://github.com/NoctilumeDev/VeriTrail/pull/92) |
| Merge commit | `ca1ce9fbf0dafab74a681fe761b1cee07d4b5269` |
| Merge parents | `f713cf5eeb4e88f2a759082c49a1eb973f634982` + `3f34f971b97d65cb3f5440ca7354bbd36c58e37b` |
| Merge tree | `67185359fd2a26ca2148ba4b380196673f9f200e` |

PR #92 把文档 114 中唯一的 Mermaid 图替换为等价静态文本关系图，没有改变任何权威、依赖、状态或
路线语义。其 Public CI run
[`34416475469`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34416475469) 在 attempt 1
完成 `11/11 SUCCESS`，并于 `2026-09-09T23:30:32Z` 通过受保护主线合入。修正 tree 与 merge tree
一致。首次 `PARTIAL` 保留为反例，不被后续 `PASS` 覆盖。

## 5. 修正后 exact-main 门禁

只接受精确 `main@ca1ce9fbf0dafab74a681fe761b1cee07d4b5269` 上由 push 事件产生的运行：

| Workflow | Run | Attempt | Result |
| --- | ---: | ---: | --- |
| Public CI | [`34417241951`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34417241951) | 1 | `11/11 SUCCESS` |
| Browser Smoke | [`34417242011`](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34417242011) | 1 | `1/1 SUCCESS` |

该事实只证明修正后的主线门禁成立；它不单独证明匿名公共页面，也不产生 Q 运行能力。

## 6. 修正后匿名产品读回

读回使用公开发布的 Core `0.13.0` 与 GitHub Evidence Plugin `0.1.0`，均从隔离环境的
`site-packages` 导入；没有提供 `GITHUB_TOKEN` 或 `GH_TOKEN`，浏览器使用插件要求的 matching Chromium。
三次 P1 API -> P2 Public Render -> Core 配对 session 均绑定 exact main，并分别取得 `COMPLETE / PASS`：

| Target | Required marker | API Evidence SHA-256 | Render Evidence SHA-256 | Acceptance report SHA-256 |
| --- | --- | --- | --- | --- |
| `README.md` | `Prove no less. Repeat no more.` | `5baec3efb92c7cc0525f11b32abec29be24c43dc3be5d098308239033b81fccf` | `1409b93bf0a98ced00f3696262c8d6b15b5dda98e7d9750d85c3c063d486cc73` | `f450e79aaaadcd1446f6ec381c7c4d00259ca04f382220fea1d2b120ec666ed6` |
| `docs/114-capability-boundary-and-system-map.md` | `Q0_BLUEPRINT_CANDIDATE` | `d5b36577ecd4e8ba131d350d7ad7b6ce4097bfd5aece6c0ab04e40abdf72b073` | `dd3b31f6b2c0a710c47e5084c6b9ad475ee057f0590c9394aed308e94077e991` | `b051670952c7e14c0dc7312bca4daa89e2548fa1c5635e924a3ddf56aa83f32c` |
| `docs/116-q0-quick-verification-scheduling-blueprint.md` | `Q0_BLUEPRINT_CANDIDATE` | `ecbb6a4cfeb6c8232c76a72b95c87a7e2517fd5c1c1f80bb2f7e522f62b6722d` | `bb344083b8b6ed2fd820526d14f6c33b30c601ba10d463706930bfdafc922c86` | `fe79d9f1a01c7b844a53550bda00596c2beb1cbbc96e86f69c87ba725a86faa7` |

三次 session ID 分别为：

```text
github-paired-6c6fedac49fb4c619c0b7a832bab9c9b
github-paired-dffcdfcd02754f0daf581a85732220f3
github-paired-ca8deadd10894c61aa96846ee93ecc5e
```

每个 session 都保持固定的 P1 -> P2 顺序、独立 request seal、同一 Plan binding 与非原子观察声明。
三次 session 不构成同一 GitHub 原子快照，也不被描述成三个独立信任域。

在额度重置前还出现过一次匿名 API `remaining=0 / HTTP 403`；Collector 将其保留为
`COLLECTION_BUDGET_EXHAUSTED / ERROR`，没有复用该 session。额度按平台声明时间重置后，新 session 才从头
采集并取得上表结果。这证明匿名可用性与仓库语义仍是两类事实。

## 7. 冻结对象

冻结对象是文档 116 中的 Q0 蓝图语义，包括：

- `Q = Quick`，正式能力名为 Verification Scheduling Plugin；
- `Prove no less. Repeat no more. / 验证不减，重复不做。`；
- Q、R、P 与 Core 之间独立的 authority、lifecycle、Artifact identity 和卸载边界；
- `Dependency != Ownership`、`Consumption != Succession`、`Composition != Integration`；
- Gate input closure、Evidence reuse/freshness、绝对预算、隔离 Lane、deterministic join 与 snapshot continuity
  的候选问题边界；
- Q 只能生成未来 Schedule、reuse binding 和 Lane/join provenance，不能产生 `SAFE_TO_SKIP`、PASS 或 Verdict；
- Q 不得反向扩大 R1，不得把文件扩展名、旧绿灯、cache hit 或单个成功结果当成 impact proof；
- Q 不可用时完整串行验证保持成立，只允许 wall-clock 退化；
- 实现入口必须另行获得 exact ChangeSet、Gate closure、freshness、真实 Profile、资源隔离和 reference lab
  等证据与独立合同；
- Q0 不预编 Q1–Qn，也不承诺 Q 一定进入实现。

文档 116 首屏继续保留候选时点与设计基线，不批量改写成“它从一开始就已冻结”。当前状态由本文外部
绑定，保持 `Blueprint History != Current State Publication`。

## 8. 未产生的能力

截至候选闭环基线，以下事实仍然不存在：

```text
no Q Schema or canonical-byte vector
no ChangeSet or Gate-closure runtime
no Evidence cache or reuse engine
no VerificationSchedule producer
no isolated Lane scheduler
no deterministic runtime join implementation
no Q CLI or workflow integration
no Q package directory
no Q tag or Release
no SAFE_TO_SKIP authority
```

`Q0_BLUEPRINT_FROZEN` 只说明验证调度问题已经被放入独立、受约束的语义边界。它不表示 Q 已经实现，
也不表示任何现有 Gate 可以少跑、跳过或被历史 Evidence 自动满足。

## 9. 返回 Review Attention R1 Schema

Q0 是 R1 Schema 之前的短暂 docs-only 支线，不是 R1 的后继或上级。Q0 最后门成立后，当前施工入口返回：

```text
Review Attention R1
    contract: FROZEN
    schema: DRAFTING ALLOWED
    implementation: NOT STARTED
```

下一阶段只能从新的 exact main 独立起草 R1 Schema、canonical bytes 与兼容向量。不得在本分支加入 R1
运行实现，也不得为了未来 Q 的 impact facts 扩大 R1 0.1 的单快照结构语义。

## 10. 本状态发布的最后门

本补丁只允许本文、README、AGENTS、R 轨 Plan、能力地图和里程碑索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 使用公开 Core `0.13.0` 与 GitHub Evidence Plugin `0.1.0` 的产品链，fresh anonymous
   读取 README、本文和里程碑索引；
5. 三页均须保持 exact-SHA URL、HTTP 200、唯一 usable scope、`COMPLETE`、三样本稳定、指定 marker
   存在，且没有 error、conflict 或 cleanup error；
6. 确认 diff 中仍无 Schema、源码包、CLI、缓存、调度器、执行 Lane、workflow、标签、Release 或空插件目录。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
Q0_BLUEPRINT_FROZEN
Q_IMPLEMENTATION_NOT_STARTED
NO_GATE_SKIP_AUTHORITY
```

后继不得从本分支叠加 README 骨架、SVG、Q 实现或 R1 Schema。每一项都必须从完成本状态发布读回后的新
exact main 建立自己的施工坐标。
