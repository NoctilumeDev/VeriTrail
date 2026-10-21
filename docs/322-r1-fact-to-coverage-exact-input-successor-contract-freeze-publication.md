# R1 Fact → Coverage exact-input handoff successor 合同冻结发布

日期：2026-10-21

> 条件化状态目标：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@9727dc3ab536ba05ab3bfc0baf9186057fc3e73c`；tree
> `0c24c45fb52e5f29fc539d96762a31c0e3d0c899`。
>
> 上游：[successor可行性审计](320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)与
> [0.2最小合同候选](321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只发布文档321限定的Fact→Coverage exact-input handoff successor 0.2合同已经完成本地、original PR、protected merge、
exact-main双门、fresh anonymous installed-product readback与independent reconciliation资格。doc321当前状态精确为
`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`。冻结对象是：

```text
contract function  = r1-fact-to-coverage-exact-input-handoff-successor/0.2
claim purpose      = FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2
private consumer   = r1-negative-world-coverage-exact-input-consumer/0.1
private carrier    = r1-terminal-validated-original-derivation-input-carrier/0.1
audited primitive  = TERMINAL_VALIDATED_ORIGINAL_DERIVATION_INPUT_SET_REFERENCE
```

0.1 bytes、API与历史保持不变。0.2只在parent完成terminal validation以后，以shared one-shot claim交付bound original
`DerivationInputSet`、original live `BudgetContext`与validated terminal source；required-provider-failure不得复活execution
eligibility。五个terminal branches与三个zero-Parse denominator worlds保持total且可区分，equal foreign inputs、late stop、
mutation、cross-attempt、foreign context、duplicate replay与unknown-version fallback全部fail closed。

本文不创建runtime、test、Schema、fixture、Coverage producer、manifest producer、Evidence、persistence、publisher、public API、
CLI、Workbench、public Review product、Benchmark、R2–R6、tag或Release，也不修改Policy/Profile、CoverageLedger、composition、
既有Fact truth或冻结历史。

## 2. Qualified contract candidate identity

```text
PR                   = #368
base                 = b8a1ecd6e01d711f380d0774e7a6920aad005fc8
head                 = 1c2d82b6502053ed2c1b751568d8ed71a6c58196
ordinary merge       = 9727dc3ab536ba05ab3bfc0baf9186057fc3e73c
candidate/merge tree = 0c24c45fb52e5f29fc539d96762a31c0e3d0c899
diff                 = 1 commit / 4 files
```

[PR #368](https://github.com/NoctilumeDev/VeriTrail/pull/368)的original Public CI
[39564224949](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39564224949) attempt 1为11/11 SUCCESS。
exact-main Public CI [39567939524](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39567939524) attempt 1为
11/11 SUCCESS；Browser Smoke [39567939496](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39567939496)
attempt 1为1/1 SUCCESS。merge parents精确为上述base/head，merge tree等于受审candidate tree。

static contract validation在Python 3.10.6/3.13.13 × normal/`-O`四格均PASS；每格复核1,761个local links、七条
immutable upstream/runtime path与`FCXI-000..019`合同marker。focused regression四格各99/99 PASS，global/local hygiene
四格均PASS。local qualification、69-artifact local seal、
original PR qualification、protected merge与candidate exact-main dual gate的SHA-256分别为：

```text
905647477d80e7ddc9f7cd77dade03850aba25b0bbdab173b6f804196cebf3ec
c47ffcff129e551d3e60db1deb2a2a398ea5f8901e9e8b7f26cd09a186899b3c
5cccc45fba7051914cd0510b43878e06bf01516b768ba4579cd58a49299322cc
1cad02b8f2757a24fb01eb7b9db80a4a12c7a26ac47868b10ae6e3afe1d958fd
30df17bf72c74b53303d1fa4fe71068f68d120b9f5a3f1a38fa3bd081a1462b6
```

## 3. Fresh installed-product readback

在detached exact `main@9727dc3…`上建立fresh CPython 3.13 venv，安装冻结Core 0.13.0、GitHub Evidence 0.1.0、
Playwright 1.62.0与matching Chromium。公开wheel只复用重新校验的既有Release字节；匿名观察清空GitHub token、
`PYTHONPATH`、`PYTHONHOME`与`NO_PROXY`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `fcxi-ct-formal-readme-1-9727dc3` | `github-paired-93f95e395f524c0eadc9263f3a1efba2` | `e517d5d0c4948b971980e4a335e0da986e396b1e531c5b5d1574c5337e3cc3a2` |
| doc320 | `fcxi-ct-formal-doc320-2-9727dc3` | `github-paired-b96d4282dfbb43adbda77c1232ac1de9` | `31abf40ddff5048386ee3ae567d1cdfd1edce126f1266ced0804d2cff0d5853d` |
| doc321 | `fcxi-ct-formal-doc321-1-9727dc3` | `github-paired-f3c6352017804bd0ad72a1ad42ce60ac` | `8aff4fc2599d0c216e249b124dab16a1f468891beeb8ca9acc755a26f7476b40` |
| milestones | `fcxi-ct-formal-milestones-1-9727dc3` | `github-paired-11fb3a0d1179485dad64250bc2b5e2f8` | `265885889c8a33ea02bdb117ad7ecaaf0f2cd74f8fb6f85df7f097ea16305f91` |

四个qualifying PASS均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零conflict/coverage reason/
cleanup error/active stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core并逐项等于producer report；四份public
raw bytes逐字节等于同一exact main的Git blobs。

formal history还保留`fcxi-ct-formal-doc320-1-9727dc3`的`FORMAL_READBACK_ERROR`：public render已经COMPLETE且HTTP 200，
但P1 commit probe因匿名GitHub额度remaining=0而失败。reset response epoch为`1792574972`，精确更低层原因仍为UNKNOWN。
后继doc320 #2 PASS拥有新Plan/session/output identity，不覆盖该ERROR。四个diagnostic、两次pip安装以及全部setup errors同样保留，
但不参与资格。

independent reconciliation与176-artifact finite closeout的SHA-256为：

```text
e8f98083143bc6be3f326414f9c65f84461b2e73dd820cf03ee1b23de584a71e
3b1f1ae300ecbfc26637c6298956d2cb838b05366cf2fd5cc5aa371a7e3be209
```

## 4. 保留错误与证明边界

以下身份继续保留，后继PASS不把它们改写成未发生：

- readback中的两次PowerShell `foreach` pipe parser error与一次`rg` quoting/module setup error；
- environment preparation attempt 1只安装Core/plugin wheels、遗漏optional Playwright依赖，attempt 2才形成新环境身份；
- 上述doc320 formal #1匿名额度错误与UNKNOWN底层原因；
- 所有更早FAIL、ERROR、CANCELLED、setup failure与UNKNOWN。

本结果证明fixed contract bytes与声明的有限positive/negative universe取得资格。它不证明实现存在、Oracle绝对正确、future
Coverage denominator/fulfillment完整、manifest/Evidence continuity已取得authority，或0.2可以通过修改0.1、复活Provider、fallback、
placeholder或缩小分母来实现。expected results仍必须独立于被测实现枚举。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc319/doc320/doc321、private runtime、
tests、workflows、Schema、fixtures、Policy/Profile、CoverageLedger、composition、manifest、Evidence、persistence与全部历史合同必须
保持base bytes。

本层final-byte local gates只重核publication自己的docs边界：exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、
balanced fences、unique headings、条件marker、doc321与candidate closeout/reconciliation continuity、`git diff --check`及read-only
global/local hygiene。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc321 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / candidate-history reconciliation
    -> target CONTRACT_FROZEN becomes effective
    -> pause at PR #369 closeout
```

本门闭合前，branch中的`FROZEN`只是条件target。candidate readback不能替代本publication的fresh Plan/session/Evidence；
diagnostic不计入资格，任何formal non-success必须保留原identity，N从history机械导出。

## 6. 生效后的停止线

最后门闭合后，本文最多让0.2 successor contract成为`FROZEN`。按当前人类明确停止线，PR #369及其exact-main readback、
independent reconciliation与finite closeout闭合后立即暂停；不创建#370，不启动implementation feasibility、runtime、Coverage
producer、manifest、Evidence、persistence、public Review、post-R1 Benchmark或R2–R6。

后续若由人类重新授权，仍必须从新的exact main返回CONTROL LOOP；本publication不会预授任何后继施工权。

## 7. 当前publication target

本文进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AUDITED_BLOCKED_BY_FACT_TO_COVERAGE_HANDOFF_0_1_INPUT_AUTHORITY_GAP
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合以后，本文开头的`CONTRACT_FROZEN` target才成为事实；随后立即暂停。
