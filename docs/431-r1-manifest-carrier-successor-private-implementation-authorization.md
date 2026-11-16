# R1 DerivationEvidence manifest carrier successor 私有实现授权发布

日期：2026-11-17

> 候选状态：`R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@2b747deb7fdf4edc51668e02365da817e55c5e60`，tree
> `f1189b0eb018cea4de8643c557980d705644ba97`。
>
> 上游：[最小合同 0.1](426-r1-same-attempt-derivation-evidence-manifest-carrier-successor-contract-recovery.md)、
> [合同冻结发布](429-r1-manifest-carrier-successor-contract-recovery-freeze-publication.md)与
> [private implementation feasibility audit](430-r1-manifest-carrier-successor-private-implementation-feasibility-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只发布一份条件化 bounded private implementation
> authority；不修改 runtime、tests、workflows、fixtures、Schema、carrier、Manifest、persistence、Provider、public Review、Core
> Verdict、global composition authority 或 R2–R6。本文自己的完整资格链闭合以前，`PRIVATE_IMPLEMENTATION_ALLOWED`不生效。

## 1. publication 输入已经取得资格

PR #492 已把 doc430 candidate
`base=adb1fe7e454c7538ed828a12fe79aa4b43441207 / head=391528c611ea83ffb0a78263e247cf7c973f9a4d /
tree=f1189b0eb018cea4de8643c557980d705644ba97`精确合入
`main@2b747deb7fdf4edc51668e02365da817e55c5e60`。original Public CI `43956270989`、exact-main Public CI
`43962198744`与 Browser Smoke `43962198868`均为 attempt 1 SUCCESS，分别 15/15、15/15 与 1/1；没有 rerun。

fresh detached exact-main world 只认`2b747de… / f1189b0…`。README、doc426、doc429、doc430 各有唯一 Render diagnostic
和唯一 formal PASS；AGENTS、milestones、legacy Evidence 0.2 Schema、legacy Manifest 0.1 Schema、continuity runtime 与 unified
admission runtime 各有唯一 anonymous raw/Contents API/exact-Git 全字节一致 PASS。independent reconciliation、185-artifact finite
closeout、expected stdout self-capture mismatch 与 finite integrity SHA-256 为：

```text
e4038eedd5a020f3e098a51b050626d15fdcde48da3843a5f45b6ef74439e2db
c6175dced041de46b8383d91f165474b6025cf5beac2928c1f2b84331f8458a6
da7d855bd88aa2580a39b9e0ef903196aa178d63337a819644b6751e2422735f
71d481cbd7408aa969e9ca735ebb07d273bd2a9ee44a28716b16c23487f7b862
```

doc430 full-file SHA-256 为：

```text
090c18e917b09029486d47c77bc797076182efc8a586dc02b7f4dc0517d4d834
```

因此 doc430 现在是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`；doc426 的 PR #488 失败 world 与 doc429 的合同冻结历史继续保持各自
原 identity。这些事实只解除独立 implementation authorization publication 的阶段阻断；runtime 在本文最后门闭合以前仍是
`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 保留的 non-success 与证明设施修正

doc430 形成和资格化过程中所有 non-success 均继续保留，不被后继 PASS 回填：

1. feasibility 长进程 session 丢失、Manifest Schema `$defs`误判、semantic comparator 过度投影 fresh attempt identities、PowerShell
   pipeline、Windows glob、pytest availability probe 与 evidence hash capture 均按原 identity 保留；
2. readback facility inspection 的 Windows glob、组合 regex 与 wrong-worktree marker inspection 错误均没有执行产品观察；
3. anonymous rate diagnostic 与 API preflight 是 non-qualifying setup observations，formal observations 使用独立 Plan/session identity；
4. independent reconciliation attempt 1 把 append-only setup history 误要求为“等于初始 setup 记录数”，在 rate diagnostic 与 preflight
   合法追加后 fail closed；versioned v2 只改为“历史是初始记录的超集且逐项保留”，没有重跑任何产品观察；
5. attempt 1 proof-facility error、v2 freeze 与 adapter freeze SHA-256 分别为：

```text
900fbd4049d1e189dd1ee583770857ab652419af989a60da8fac337c178256c8
6514efc8252a0a9be873eee92514e3bf46eae9d18cd9c8e508fb80565a1cc9cf
d7f9402705abffb9a2d94a6c85124f369f170827fa630461f9db01664dea68bb
```

当前 authorization worktree 的首次受管创建又命中 Windows 长路径 setup error；短路径 successor 从同一 exact SHA 建立成功。该错误只属于
worktree setup，未生成 candidate bytes、未修改仓库，也不改变 doc430 qualification。

## 3. 原工程问题、当前证明义务与适用世界

```text
original engineering problem
    为 future Review derivation Manifest 建立 same-attempt、copy-owned、
    可独立验真的 DerivationEvidence carrier

current proof obligation
    只发布 frozen doc426/doc429 + qualified doc430 允许的 bounded private implementation authority；
    不把授权、测试或未来 candidate 解释为 runtime 已存在或原工程问题已解决

applicability world
    exact main 2b747de source + frozen doc426/doc429 contract world
    + qualified doc430 eight-live-world feasibility world + 全部 retained non-success

proof_is_not_problem_solving = true
local_not_global             = true
post_r1_global_check_required = true
```

若原工程问题、证明义务或适用世界漂移，即使本文本地或远端门仍绿也必须停止。授权只说明指定边界内可以施工；它不证明施工已经发生、
结果正确、用户问题已经解决或 global composition 已成立。

## 4. 授权对象是 bounded A–J

本文最后门闭合、返回 CONTROL LOOP 且前提仍成立以后，唯一允许的 private implementation scope 如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 新增显式 `review-derivation-evidence-0.3` Schema 与 exact-version dispatch；Evidence 0.2 与 Manifest 0.1 bytes、role/path、consumer 保持逐字节不变，unknown/closest version 无 fallback。 |
| B | continuity owner 只增加一个窄 private coordinate，返回它已 copy-own 的 inputs、transition、result、application admission、attempt/context 与 lifecycle binding；不得暴露 mutable state。 |
| C | 新建 versioned private projection claim 与 Evidence 0.3 projector，只从 B 的 exact material 和 frozen rules 形成 canonical bytes；不得回读 path、重调 Provider 或从 expected result 反推 route。 |
| D | 新建不可 public 构造、不可 copy/pickle/JSON 恢复的 one-shot exact snapshot carrier；copy-own exact Evidence、present child、Ledger、role/path、raw SHA、size、semantic digest、root topology 与 qualified absence/unknown proof。 |
| E | 新建独立 conformance owner；不得调用 producer 的 expected-document projector，必须从 copy-owned raw bytes 与独立冻结向量复算 Schema、branch/route/variant、Ledger/root-chain、topology、child binding、attempt/context 与 lifecycle。 |
| F | 正例分母固定为 doc426 的八个 live worlds；branch-empty/closed-empty/partial 保持 present，relation-conflict 保持 Slice qualified unknown，四个 negative world 不制造 placeholder；compatibility-only fixture 不能冒充 live route。 |
| G | 第一次 validation 成功或失败都永久消费 candidate validation opportunity；成功只能签发 exact private admission。admitted carrier 只暴露 future Manifest producer 的 one-shot consumption protocol，不在本阶段创建 Manifest runtime。 |
| H | wrong version/type/branch/route/variant、subclass/proxy/copy、foreign attempt/context、mutation、role/path swap、digest drift、common-mode oracle、replay、late stop 与 concurrent second use 全部以 doc426 typed private failure family fail closed；未知 lower cause 保持 `UNKNOWN`。 |
| I | Evidence 0.3、carrier、conformance 与 consumption protocol 不取得 Reality、Provider、stage truth、evidence sufficiency、Core Verdict、Manifest transport 或 global composition authority；public export 只限 frozen Schema resource。 |
| J | 把 `DEMC-000..019`、八个 live worlds、legacy compatibility、copy isolation 与 one-shot races 转成 focused tests；运行 CPython 3.10.6/3.13.13 × normal/`-O`、legacy/full regression、compile、hygiene、scope 与 audit continuity，形成独立 implementation candidate。 |

class、method、field、lock、retention 与文件布局仍由后继 implementation candidate 决定。测试只作 witness；expected version、route、topology、
role/path 与 digest rules 必须来自独立冻结向量，不能由被测 producer 生成。

## 5. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded A–J
+ 增加 Evidence 0.3 Schema 与对应 private modules
+ 增加 private tests / audit fixtures
+ 运行 DEMC、八个 live worlds、legacy/full 与四格 falsifiers
+ 形成独立 implementation candidate
```

它不允许：

```text
修改 Evidence 0.2 / Manifest 0.1 bytes、role/path或legacy consumer
让 producer 自验、回读 mutable path、重调 Provider或伪造fixture-only live world
让 carrier/Evidence/Manifest 宣布truth、sufficiency或Verdict
实现 Manifest 0.2 runtime、publisher、Bundle或persistence Route A/B
恢复global composition authority或关闭language-support persistence
启动public Review、post-R1全局优化、R2–R6、tag或Release
```

`PRIVATE_IMPLEMENTATION_ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。runtime patch 必须拥有
新的 source、branch、candidate head/tree、原始 PR 门、protected merge、exact-main 双门、fresh installed-product readback 与 independent
reconciliation；真实反例出现时必须停止当前施工，只重开被击穿的最小边界。

## 6. implementation stop conditions

后继施工出现以下任一条件时必须保留反例并停止：

1. Evidence 0.3 不能在不修改 0.2 bytes/semantics 下显式 dispatch；
2. current continuity/application admission 不能无损提供第4节 B/C 所需 exact material；
3. carrier 必须回读 path、重调 Provider、依赖 mutable shared projector 或接受 caller-selected item replacement；
4. live relation-conflict、四个 negative topology 或 compatibility-only world 无法由 Ledger 与 current route 机械区分；
5. independent conformance 只能调用 producer expected projector，或 producer/validator 必须共享被测试的关键 projector state；
6. one-shot validation/admission/consumption 不能绑定 same attempt/context/root chain，或失败后 equal bytes/new wrapper 可恢复 authority；
7. bounded patch 必须同时实现 Manifest 0.2、persistence、public Review、Core Verdict 或 global composition；
8. `DEMC-000..019`只能通过弱化 oracle、删除首败、拼接不同 world、增加例外或重解释冻结历史才能通过。

授权已经生效也不能成为扩大 scope、静默 reopen 合同或把局部 PASS 外推为全局正确的理由。理论遇到反例先检查前提和适用域，不不断增加例外。

## 7. 本 publication 自己的资格链

tracked scope 只允许：

```text
README.md
AGENTS.md
docs/431-r1-manifest-carrier-successor-private-implementation-authorization.md
docs/milestones.md
```

doc426、doc429、doc430、`docs/project-state.md`、runtime、tests、fixtures、workflows、Schema、carrier、Manifest、persistence、Provider 与全部
frozen semantic bytes 必须保持`2b747de…` base 不变。local gates 至少复算四文件 scope、UTF-8 without BOM、LF/final LF、links/fences/
headings、required markers、`git diff --check`、global/local hygiene、doc426/doc429/doc430 full-file SHA、PR #492 原始/exact-main 双门、
4+6 fresh observations、retained non-success、independent reconciliation、finite closeout/integrity 与 primary `audit.json` continuity。
focused matrix 与 read-only feasibility audit 必须从当前 base fresh 复算；它们只作 witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 15/15 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc430 / 本文 Render readback
    -> fresh anonymous exact-commit AGENTS / milestones raw-byte observation
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

README、doc430、本文各运行唯一 Render diagnostic+formal；AGENTS、milestones 各运行唯一 anonymous raw+Contents API+exact-Git 全字节
对账。产品调用必须清除 GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按命令使用
`http://127.0.0.1:7897`。任何 non-success 保留原 identity；不得 rerun 洗白、重复已有 PASS 或拼接不同 world。

## 8. 当前 publication target 与停止线

全部门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_CONTRACT_FROZEN
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把
`R1_DERIVATION_EVIDENCE_MANIFEST_CARRIER_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回 CONTROL LOOP，才允许在本文 ceiling 内开始新的 private implementation candidate；
不得把 authority publication、形式矩阵或 doc430 qualified feasibility history 算作 runtime 证据。
