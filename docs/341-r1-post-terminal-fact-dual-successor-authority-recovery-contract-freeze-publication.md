# R1 post-terminal Fact dual-successor authority recovery 合同冻结发布

日期：2026-10-29

> 条件化状态目标：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@c819dd1cca35a96efc22908cce546fad8185d9d8`；tree
> `a80eb8913f225a8494bc50cd09e9a6edb35df0a6`。
>
> 上游：[合同候选](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)与
> [current-state audit](339-r1-review-coverage-composition-authority-recovery-current-state-audit.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改runtime、tests、workflow、Schema、Fact/Relation/Coverage
> semantics、manifest、Evidence、persistence或public Review surface。

## 1. CONTROL LOOP 与本publication的唯一职责

文档340已经完成自己的final bytes、local gates、original PR gate、protected exact-head merge、新exact-main双门、fresh anonymous
installed-product readback、independent reconciliation与finite closeout。因此它现在是：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified candidate不等于frozen contract。fresh CONTROL LOOP重新核对doc339证明的最小缺口仍是post-terminal、branch-qualified、
shared-one-shot的dual-successor authority；doc340冻结的five-branch total/disjoint partition、same-object terminal source重验、wrong-route
永久撤销、fail-then-fallback禁止与claim-specific independence仍是最小边界。没有新证据授权扩大到runtime、union output、manifest、
Evidence、persistence或public Review。

因此本文只承担一个职责：在自己的完整资格链成立以后，把固定doc340 semantic bytes从qualified candidate发布为frozen contract。

## 2. Exact contract candidate qualification

```text
PR                   = #392
base                 = 328ba21aa885a51f99c234ed90bee7056e8a320f
head                 = fe0d1c9ba6a967142542fe4606a70f3a91bb5475
ordinary merge       = c819dd1cca35a96efc22908cce546fad8185d9d8
candidate/merge tree = a80eb8913f225a8494bc50cd09e9a6edb35df0a6
diff                 = 1 commit / 4 docs files
```

original Public CI `40821427690`、exact-main Public CI `40825476221`与Browser Smoke `40825476284`均为attempt 1
SUCCESS，分别11/11、11/11与1/1。candidate-local semantic audit在Python 3.10.6/3.13.13 × normal/`-O`四格逐字节一致，
report SHA-256为`254cac8a3d722d8e5cc95f0c89859689ea4da411e768463aa75ecf38f13b9dae`；focused matrix四格各214
reported / 213 passed / 1 skipped。49-artifact local closeout与post-commit seal SHA-256为：

```text
d07144079b6c814772e81f391041b9297a52ed255a8c3322b51c5338b99d569c
dee9e4c8e8972037e908c2064469be8a19c3ba6c617aecfd0de7b3de8f25239a
```

assertion/fragment、incomplete falsifier coverage与focused runner syntax setup errors全部保留，effect为`NONE`；later PASS不把它们
改写成未发生。

## 3. Fresh exact-main installed-product readback

在detached exact `main@c819dd1…`上建立fresh CPython 3.13 venv，安装冻结Core 0.13.0、GitHub Evidence 0.1.0、
Playwright 1.62.0与matching Chromium。公开wheel只复用重新校验的immutable Release bytes；匿名产品观察清除token、
`PYTHONPATH`、`PYTHONHOME`与`NO_PROXY`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-ptds-contract-formal-readme-1-c819dd1` | `github-paired-e8c5a2db0106419a805ac3fdcc49b2ca` | `d0962d6268ccd244dd56d677e1a9006b8768f956719cf2951756fd4099e8cea0` |
| doc340 | `r1-ptds-contract-formal-doc340-1-c819dd1` | `github-paired-cee0b37b888c4a9fbe623bc1d4122fdb` | `a014896ce0da79f0bcba078710bfcd5f2ed57a24bacfa369fcddfea2aa9ff0de` |
| milestones | `r1-ptds-contract-formal-milestones-1-c819dd1` | `github-paired-f2078339bf594aaf8e1ee782063e6567` | `5bef4f0813e7db88d5c61dfbdb6502a9391b156b6d087aad557cfd8ed1fbfef5` |

三者均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零conflict、coverage reason、cleanup error与active
stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core并逐项等于producer report；public raw bytes逐字节等于同一
exact main的Git blobs。

pre-observation adapter、independent reconciliation、140-artifact finite closeout、保留的stdout self-capture mismatch与finite
integrity SHA-256为：

```text
8855346ee466702055504759bb5c8a95ec92feb3367ec927a8d021c29ab9d503
44462f6dc318aadc2931c252d5c8f5586dd8de10db2377ac11368cfc9d253c40
379234bcd445d25059e5008b90299cc0d2963eea8b49e1ccfac23fca319240f8
6c7d0a427d5ce6f62a9c9b91e92abc4b57c6fa7519fc5fd89119875d0fa3e6ff
f348f7a17348549752c0f681e3400e362258d6872b5963b897471f3064f954a5
```

milestones diagnostic #1的public-render response-body observation终结为`ERROR / UNKNOWN`，但它是明确
`DIAGNOSTIC_ONLY_NON_QUALIFYING`且完整保留。formal milestones使用新的Plan/session并唯一PASS；它不覆盖或解释diagnostic。
reconciliation attempt 1因proof script误读candidate setup-error schema而失败；attempt 2修正证明设施后PASS。两个operator path setup
error与closeout stdout self-capture mismatch也以effect `NONE`保留。

## 4. 冻结对象与不变量

本文发布的唯一semantic对象仍是doc340定义的：

```text
contract function              r1-post-terminal-fact-dual-successor-authority-recovery/0.1
Fact consumer handoff domain   POST_TERMINAL_DUAL_SUCCESSOR_0_1
route-selection function       r1-post-terminal-fact-route-selection/0.1
shared claim function          r1-post-terminal-fact-dual-successor-claim/0.1
```

冻结以后仍必须保持：

- pre-terminal successor只绑定完整world，不签发route；
- complete original Fact terminal source经过独立重验以后，`NORMAL_FULFILLED`只可签发Relation handoff；
- 四类negative terminal branch只可签发exact-input successor 0.2；
- 两条route共享一个不可复制consume slot；pre-terminal、wrong-route、fallback、replay、copy-equal、branch rewrite、denominator
  shrink与shared-projector common-mode都fail closed；
- Fact truth、既有Relation/negative Coverage algorithms、positive/negative qualification/admission、CoverageLedger 0.3与全部历史
  contract bytes不因本publication改变。

`CONTRACT_FROZEN`只解除private implementation feasibility的阶段阻断；它不证明可实现、不授权施工，也不恢复旧global composition
authority为可消费状态。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc340、runtime、tests、workflows、
Schema、Policy/Profile、Fact/Relation/Coverage semantics、manifest、Evidence、persistence与public Review bytes必须保持base不变。

本层local gates只重核publication边界：exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique
headings、条件marker、doc339/doc340资格与candidate evidence continuity、`git diff --check`、read-only global/local hygiene及primary
`audit.json` continuity。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc340 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP for private implementation feasibility
```

publication自己的fresh Plan/session/Evidence不可由doc340 readback复用；diagnostic不计入资格，所有formal non-success保留原identity，
N从history机械导出。本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 6. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_COVERAGE_COMPOSITION_AUTHORITY_RECOVERY_CURRENT_STATE_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合以后，本文开头的`CONTRACT_FROZEN` target才成为事实。随后必须从新的exact main返回CONTROL LOOP，独立审计private
implementation feasibility；不得把合同冻结解释为runtime已经开始、恢复global composition authority、选择manifest/Evidence/
persistence或启动public Review/R2–R6。
