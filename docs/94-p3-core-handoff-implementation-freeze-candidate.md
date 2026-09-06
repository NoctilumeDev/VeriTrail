# P3 Core Handoff 实现与冻结候选事实 0.1

> 候选记录状态：`P3_IMPLEMENTED / FREEZE_CANDIDATE / P4_NOT_STARTED`
>
> 后继冻结状态发布：[文档 95](95-p3-core-handoff-freeze-publication.md)
>
> 精确施工基线：`589bbad7261cceda1aa3a6412278a48473a9b1b7`
>
> 完整实现候选：`fa26dda516c354a5ddd08335202d3fd1cf5dbabb`
>
> 受保护主线实现基线：`c0bce6cb7a3c9f3684d1845beda355084f232d0a`
>
> 主线 Tree：`2ff03343d5d9bb1b1a889d9d22c8713de4a3cd22`
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM`；只增加通用 imported-snapshot Core 入口、独立插件
> handoff/reference lab、测试与 CI，不修改既有 Schema、evaluator、P1/P2 fact semantics 或 Verdict
> 优先级

## 1. 当前裁决

P3 已完成合同内实现并进入冻结候选：P1 API 与 P2 Public Render 的两份标准 Evidence 由极薄 handoff
manifest 精确选择；插件通过 Core 公共 importer 各读取一次，核验 role/path/digest 后，把同一组
`ImportedEvidence` 快照交给通用 Acceptance Core Bundle 入口。manifest 不复制 Plan、session、facts、
coverage 或 Verdict 语义，插件也不预先判断充分性、完整性或最终结论。

Synthetic reference lab 已证明 `PASS / FAIL / INCONCLUSIVE / PENDING` 四态；真实 GitHub 纵向链使用
预先 sealed 的正确 Plan 得到 `PASS`，使用只改变一个 SHA 期望的 Plan 得到 `FAIL`。负链中其余
sufficiency、integrity、requested URL 与 marker 规则仍全部通过，因此不是“顶层碰巧为 FAIL”的多变量
结果。

实现 PR、受保护主线合入和合入后 exact-main 匿名产品读回已经成立。但本文仍只是 docs-only freeze
candidate。只有本候选自己的原始公共门禁、主线合入与合入后匿名 README/本文读回全部成立，才允许
另开最终状态发布，把 P3 标记为 `P3_FROZEN`。P4 与 Review Attention R1 目前均不得启动。

## 2. 实现边界

```text
P1 Evidence path ─┐
                  ├─ handoff manifest: role + relative path + sha256
P2 Evidence path ─┘
                         ↓
              Core safe import exactly once
                         ↓
            verified ImportedEvidence snapshots
                         ↓
         generic Core AcceptanceBundle entry point
                         ↓
       sufficiency / integrity / assertion / Verdict
```

路径只负责定位，快照才负责身份。既有 path API 继续兼容旧调用者，但内部必须先完成安全导入，再委托
同一个 imported-snapshot 实现；handoff verifier 不允许核验路径 A 后让 Core 再读可能已经变成 B 的
同一路径。`ImportedEvidence` 拥有导入后的独立文档副本；调用者后续修改原映射不能改变 Core 消费的
快照，直接篡改 imported snapshot 也会在 Core 消费前由摘要复核拒绝。

插件与 Core 仍保持单向依赖：Core 只认识通用 `ImportedEvidence`，不知道 GitHub、P1、P2、manifest、
collector role 或 collection session。插件卸载后，已经形成的标准 Evidence 与 AcceptanceBundle 仍可
由 Core 独立读取和复算。

## 3. 分阶段实现事实

实现候选由六个单一意图提交组成：

1. `ce08d91`：P3-A handoff manifest 闭集、规范身份与 create-new 发布；
2. `87003a9`：P3-B publisher/verifier 与 Core imported-snapshot Bundle 入口；
3. `86d44d8`：P3-C synthetic four-verdict reference lab；
4. `c615ef1`：P3-D base wheel、render extra、plugin uninstall 与 Core-only 复算门；
5. `7e10e7a`：按冻结 P2 fact schema 修正 synthetic C 与 sealed Plan；
6. `fa26dda`：P3-E 真实 GitHub PASS/FAIL 可重复验收脚本。

P3-A/P3-B 没有把语义预检塞进 manifest；P3-C 直接把 Evidence 交给 PC2 Core；P3-D 不让 Playwright
成为 P1/base wheel 的默认依赖；P3-E 不在观察现实以后再制造错误期望。

## 4. Freeze 前反例与最小修正

第一次真实 P3-E 在两侧 Evidence 与 handoff 已发布后停止：冻结合同要求比较
`/facts/commit/sha` 与 `/facts/target/source_coordinates/target_commit_sha`，但 synthetic C 与其 sealed Plan
错误使用了 `/facts/navigation/target_commit_sha`。合成夹具、Plan、测试和四态结果彼此自洽，却与真实
P2 标准 Evidence 不同；若继续执行，真实链会因 operand unresolved 得到 `INCONCLUSIVE`。

该反例没有被解释成 P2 错误，也没有通过插件侧 fallback 兼容。提交 `7e10e7a` 只修正 C：

- synthetic Evidence 改用真实 P2 target/navigation/content 结构；
- sealed Plan 同时要求 exact target SHA、requested URL 与预声明 README marker；
- 两份提交夹具重新 seal，并由测试逐字节对照生成器；
- Python 3.10/3.13 的普通与 `-O` 定向门均为 `6/6`，完整插件门均为 `180/180`。

原失败产物保留在仓库外，没有被后续成功覆盖。该模式以 append-only `RA-021 rev1` 写入
[Review Pattern Ledger](87-review-pattern-ledger.md)，但不进入 Pattern Corpus，也不启动 R1。

## 5. 本地串行证据

所有门禁均显式绑定当前 worktree 的 Core、插件源码和测试目录，并严格串行运行：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| Core 普通 / `-O` | `392/392` / `392/392` | `392/392` / `392/392` |
| GitHub Evidence 普通 / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| P3 C 定向普通 / `-O` | `6/6` / `6/6` | `6/6` / `6/6` |
| base wheel + plugin uninstall + Core-only 复算 | `PASS` | `PASS` |

wheel-only 探针从 clean venv 安装 Core/plugin wheel，先在没有 Playwright 的 base 环境生成 P3
AcceptanceBundle，再显式安装 `playwright==1.62.0` 与 matching Chromium；卸载 GitHub 插件后，Core
仍从保留的标准 Evidence 独立复算为 `PASS`。这分别证明 capability 可用与 Core 完整性，不把插件
安装状态当成 Evidence 真值。

## 6. 真实 GitHub PASS / FAIL

真实 E 固定公开仓库 `NoctilumeDev/VeriTrail` 与不可变 commit：

```text
589bbad7261cceda1aa3a6412278a48473a9b1b7
```

两份 Plan 在观察前已经提交并 seal。它们只在 `sealed-exact-commit` 的字面期望与派生 Plan identity 上
不同；P1 → P2 每次建立新的 paired session，分别发布两份 `COMPLETE` Evidence，再经 handoff 将同一
imported snapshots 交给 Core。确认复验得到：

| Case | Plan digest | Handoff digest | Core report | Verdict |
| --- | --- | --- | --- | --- |
| 正确期望 | `837bfd793abc6c60ca7ab0737874965010b0d331df502a83bd6f4467abe1584b` | `06fe53eeb77df6b18b0ee85c02d71664d018158ea72416ab18c42a931975759a` | `0b053e907e580755ee5b59905d0bf6aac8cadc76f06307fcc84c55fc1cc1bccf` | `PASS` |
| 单变量错误 SHA | `ae99d59c88d8d3a57aae0119918dd227890c5f76a7228791d0c1946d73c3ac8d` | `8b2275d9a72c93b8b70016dc63a84c80ae89d74eefe12cf3a3f30da5f4374bec` | `701c8ea3cb46a9fde2e89580fb76d28a7a59366e93e8d4d0d84e4db74c8c3661` | `FAIL` |

正链 Evidence SHA 为 API `c2be05c3714ec2221dbef4b410127da1e15585503e62babe5361d6c2521c8649`
与 Render `58c2410e31f5940640dda102f12c3090f82903f6adc09be8cdd7e76aca31eaa2`；负链为 API
`a4b61273f6ff3184b8acd0222a34cc2c689bd6cb8f7b6d46512a5f07ffd23073` 与 Render
`cc14c6516aa2ee65b9683fa9273578609a0203dd49e9e7faf77dce3d58bdf2e9`。两条链都保留固定
`github-api -> github-public-render` 顺序、同 session 相关性、两份不同 request seal，并明确
`atomic_snapshot_claimed=false`。GitHub API 与公开页面仍是同一信任域的两个观察面，不是独立权威。

负链只有 `ASSERTION / sealed-exact-commit` 为 FAIL；两项 coverage、同 session、同 target、requested
URL 与 `VeriTrail` marker 均为 PASS。该证据只证明 Core 忠实执行预封存规则，不证明源头观点或 GitHub
之外的现实为真。

## 7. 远端 implementation PR

1. 完整候选 `fa26dda516c354a5ddd08335202d3fd1cf5dbabb` 从精确
   `main@589bbad7261cceda1aa3a6412278a48473a9b1b7` 起步；
2. [PR #64](https://github.com/NoctilumeDev/VeriTrail/pull/64) 的
   [Public CI run 34058486030](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34058486030)
   原始 attempt 共 11 个 job，全部 `COMPLETED / SUCCESS`，没有 rerun；
3. PR #64 以 merge commit `c0bce6cb7a3c9f3684d1845beda355084f232d0a` 合入受保护 `main`；
4. 合入后 `origin/main` 精确读回同一 SHA，tree 为
   `2ff03343d5d9bb1b1a889d9d22c8713de4a3cd22`，merge parents 为施工基线
   `589bbad7261cceda1aa3a6412278a48473a9b1b7` 与候选
   `fa26dda516c354a5ddd08335202d3fd1cf5dbabb`。

## 8. 合入后 exact-main 匿名产品读回

从 `main@c0bce6cb7a3c9f3684d1845beda355084f232d0a` 使用产品 P1/P2 Collector、fresh anonymous
Chromium、独立 sealed Plan 与新 session 串行读取：

| 页面 | Plan digest | Handoff digest | Marker | Core report | Verdict |
| --- | --- | --- | --- | --- | --- |
| exact README | `b855b5e4143d0578b9f336dd830f2842e3e00105753e3ab82e1fa3f1e144398b` | `de0fe0bc73c696fd96da96b0dbf2a452eedbc2b61fbe9b95c8c8359adb1128f0` | `VeriTrail` 23 次 | `68da82ac613343d095360443f6a088e9d93474b5af7a912feed3b05e13891d68` | `PASS` |
| exact P3 合同 | `01b0aced1f41618e72ad449e1486d2f1cb5ff0142c0f85159741dd53720780e7` | `334979d13d10dab7ec52a891c40b937851627c8fc5fe1e33053e86255e12f909` | `快照连续性` 1 次 | `7a2bf0dc25af8dd97492c5c98636b6ff67edae16fe3e0a21ef2e6eeb504574ae` | `PASS` |

两次 P1/P2 Evidence 均为 `PUBLISHED / COMPLETE`，requested/final exact path 未漂移，三样本稳定，
结束时 active streams 为 0、cleanup errors 为空。两个页面是两次独立观察，不冒充同一平台原子快照；
本地取证 Artifact 未提交仓库。

## 9. 范围外与停止线

本候选没有进入：

- P4 插件版本、tag、Release、下载读回或稳定安装坐标；
- Review Attention R1、Pattern Corpus 冻结、自动风险判断或 HumanDisposition；
- 新 GitHub 写能力、登录态/私有仓库、GitHub Enterprise 或外部真实性锚点；
- Workbench 新规则、远端调度、自动监控或 Codex Security 深扫；
- 对源头命题、GitHub 真实性或世界真相的最终裁定。

本 docs-only candidate 必须继续满足：

```text
候选原始 11 项 required checks 全部成功
    -> exact head 合入受保护 main
    -> 读回新的 exact origin/main
    -> fresh anonymous 产品 Collector 读回 README 与本文
    -> 独立最终状态发布
    -> P3_FROZEN / P4_NOT_STARTED
```

任何新反例仍可否决冻结。P3 冻结以后也只解除 P4 的阶段阻断，不自动发布插件，更不解除
`R1_BLOCKED_UNTIL_P4_AND_CORPUS_FREEZE`。
