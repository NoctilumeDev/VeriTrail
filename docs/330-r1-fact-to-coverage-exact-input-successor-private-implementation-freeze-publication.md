# R1 Fact→Coverage exact-input successor 私有实现冻结发布

日期：2026-10-28

> 条件化状态目标：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@8f258e3c4fb425af3d057493a63009c3099f03c4`；tree
> `69f826fd5d82e08ba2cd201b043f473fcc7a722e`。
>
> 上游：[可行性审计](320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)、
> [0.2合同](321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)、
> [合同冻结发布](322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md)、
> [授权恢复后继发布](328-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-successor-publication.md)、
> [实现候选](329-r1-fact-to-coverage-exact-input-successor-private-implementation-candidate.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只发布文档320–329限定的bounded private exact-input carrier A–I已经完成施工、进入受保护main，并取得candidate自己的
local/original PR/exact-main/fresh installed-product/independent reconciliation资格。本文不修改runtime、tests、workflows、
public exports、Schema、Policy/Profile、Coverage producer、manifest、persistence、public Review产品、CLI、Workbench、Core、tag或
Release。

冻结对象是versioned、private、attempt-bound、non-published Fact→Coverage exact-input successor。parent-only accessor在完整Fact
terminal revalidation以后返回同一terminal source、原始`BudgetContext`与原始`DerivationInputSet`；successor与legacy continuation、
Coverage 0.1及Relation共享one-shot；carrier每次读取都重验live context、input seal、canonical bytes、blob map、五digest、source与
claim identity，并只返回copy-owned input truth。

实现冻结不创建Coverage outcome、obligation universe、ledger、manifest或public authority；也不恢复旧composition authorization为
可消费authority。它只证明固定candidate在声明世界内取得资格。

## 2. Exact implementation qualification

```text
PR                   = #380
base                 = 494fedb1fbae9d5f847cb9f1873e7e13996b893a
head                 = 2177ce675c23d1e6793c696f1bfabd67e6702b5d
ordinary merge       = 8f258e3c4fb425af3d057493a63009c3099f03c4
candidate/merge tree = 69f826fd5d82e08ba2cd201b043f473fcc7a722e
diff                 = 1 commit / 7 files
```

[PR #380](https://github.com/NoctilumeDev/VeriTrail/pull/380)的original Public CI
[40551350656](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40551350656) attempt 1为11/11 SUCCESS。
exact-main Public CI [40556421233](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40556421233) attempt 1为
11/11 SUCCESS；Browser Smoke [40556420712](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40556420712)
attempt 1为1/1 SUCCESS。merge parents精确为上述base/head，merge tree等于受审candidate tree。

final focused四格各运行139项：Python 3.10.6/3.13.13的normal与`-O`均为138 passed / 1 skipped。完整Review
Attention四格各运行586项：Python 3.10.6两格均为583 passed / 3 skipped，Python 3.13.13两格均为584 passed /
2 skipped。独立semantic projection四格一致：

```text
a6866781bd574b7f899c7127d241bcca1eb290696d081a45401f8fb413391c7f
```

local qualification、43-artifact seal、original PR qualification与protected merge records的SHA-256分别为：

```text
38fd07d739acc6c145feb6974102fedcdc1df2b375ff232fbb6762bc830cb489
ccef481cc8a5c0187b0ea369ac36add2740a7ae7327089027a38ce03f2a437a7
230e80ea138300a322293f0437f499b5a5fc9997f32ecb82c5d8b94c2ba2de30
f1456d918e15784c2c4834c1c2f7527544e7232c6cee14a239109f2907c84b3d
```

## 3. Candidate fresh installed-product readback

在detached exact `main@8f258e3…`上建立fresh CPython 3.13 venv，安装冻结Core 0.13.0、GitHub Evidence
0.1.0、Playwright 1.62.0与matching Chromium。公开wheel只复用重新校验的既有Release字节；匿名产品观察清空token、
`PYTHONPATH`与`PYTHONHOME`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| doc329 | `r1-f2c-exact-impl-formal-doc329-1-8f258e3` | `github-paired-6bd4a27d28f245f087041c0cd42ae52d` | `6b4e975ddca8b9ca0e0b532dea7b39cbce28f02c1a6341fd021036c2cc1fcc66` |
| milestones | `r1-f2c-exact-impl-formal-milestones-1-8f258e3` | `github-paired-752555b3d9144456b023169256871a29` | `72ed1b3fedbdb298a4801af50fb7257d09f30d6b0e3d36984792988d20875a9b` |
| README | `r1-f2c-exact-impl-formal-readme-1-8f258e3` | `github-paired-c42a82ca802249699701d02c3839c55e` | `8a461ac520cddb2c96aa4e32327360ecd1d478f19465b74d4af616582c3119ee` |

三者均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零conflict/coverage reason/cleanup error/active
stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core并逐项等于producer report；三份public raw bytes逐字节等于
同一exact main的Git blobs。raw-byte check不替代正式产品路径。

independent reconciliation与134-artifact finite closeout的SHA-256为：

```text
0852c865880cba6d50caee93920e27e2aa07443fccdcc5b756a4d78cea15bbbb
e18860cf91973a906529274767e817760407c6a1cbe18a425225a6765630e638
```

closeout wrapper在enumeration前打开`create-closeout-attempt-1.stdout.txt`，索引因此记录empty digest；wrapper随后把terminal
JSON写入该文件。其余133项逐项终态一致。post-closeout record与finite integrity summary的SHA-256分别为：

```text
47ed145338746cb9e3008daeee4b1081fe2f59c73f31aed4d53ed4bb43e77b58
8b6f5c53c5a26d98be1f524e4b9d36f417fda84e1fb422ab3e252ad52af66ba1
```

该self-capture只涉及closeout stdout本身，semantic effect与qualification effect均为`NONE`；closeout字节保持不变。

## 4. Proof strength 与保留历史

本结果只证明fixed audited private carrier与既有Fact terminal validation、same-attempt input identity及shared one-shot的组合。普通
Python进程仍具宿主能力；private identity不等于第三方sandbox，也不产生Coverage、Schema或publication authority。

以下身份继续保留，later PASS不把它们改写成未发生：

- #377 exact-main Public CI `40510081408` attempt 1的required Starter失败、Artifact `12737259914`、archive
  `33ef978964918c30870010fcc56082c7e5d29edc9778c72c0147108bfa6de4bb`、resource
  `UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与host cause `UNKNOWN`；文档326保持merged but not-qualified；
- source review发现并修复初版foreign-closure substitution未必撤销原始bound authority的private defect；全部旧字节测试保持
  non-qualifying；
- Relation fixture capability、empty fixture root、丢失focused output、semantic report null FactSet、Core Markdown import path、首次
  push workdir等setup/proof-facility observations；它们不改写产品oracle或formal product history；
- 文档328 readback的错误upstream coordinate与过早adapter freeze attempt 1；
- 本candidate closeout的stdout self-capture mismatch及更早合同、可行性、授权、FAIL、ERROR、CANCELLED与UNKNOWN历史。

正式candidate readback history为3 PASS / 0 formal non-success；三个diagnostic与四个setup events全部保留但不参与资格。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc320–329、private runtime、
`test_fact_to_coverage_exact_input_handoff.py`、其他tests/workflows/Schema/Profile/Policy与全部历史合同必须保持base bytes。

本层final-byte local gates只重核publication自己的docs边界：exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、
balanced fences、unique headings、条件marker、doc329与candidate closeout/reconciliation/failure-history continuity、`git diff --check`及
read-only global/local hygiene。implementation full runtime matrix属于已经资格化的candidate tree；publication不重新解释它。
Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc329 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / candidate-history reconciliation
    -> target PRIVATE_IMPLEMENTATION_FROZEN becomes effective
    -> return CONTROL LOOP
```

本门闭合前，branch中的`FROZEN`只是条件target。candidate readback不能替代本publication的fresh Plan/session/Evidence；
diagnostic不计入资格，所有formal non-success必须保留原身份，N从history机械导出。本地checkout alignment与cleanup只属于
housekeeping，不追加语义门。

## 6. 生效后的停止线

最后门闭合后，本文最多让Fact→Coverage exact-input successor private implementation成为`FROZEN`。随后必须从新的exact main返回
CONTROL LOOP，重新审计Coverage producer与现有frozen composition之间的applicability、obligation universe、same-attempt input、
transition proof、assignment与admission authority。旧composition authorization只保留历史，不因本实现冻结自动恢复为可消费authority。

本文不授权Coverage runtime、manifest successor、persistence、public Review、post-R1 Benchmark、R2–R6、CLAIM_FIDELITY、tag或
Release，也不把有限exact-input carrier扩张成repository truth、semantic、bug或全仓审查完整性。

## 7. 当前publication target

本文进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_READBACK_QUALIFIED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_PRIVATE_IMPLEMENTATION_FROZEN
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合以后，本文开头的`PRIVATE_IMPLEMENTATION_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
