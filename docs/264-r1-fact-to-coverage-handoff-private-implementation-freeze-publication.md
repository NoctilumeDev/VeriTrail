# R1 Fact → Coverage same-attempt handoff 私有实现冻结发布

日期：2026-10-15

> 条件化状态目标：`R1_FACT_TO_COVERAGE_HANDOFF_PRIVATE_IMPLEMENTATION_FROZEN`。本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@83ad8f10b68f1d085b83310613c6f5cc06292d28`；tree `9ab55471f81711fdb80ab6de638c2f504f5ce9b1`。
>
> 上游：[冻结合同](259-r1-fact-to-coverage-same-attempt-handoff-contract.md)、
> [合同冻结发布](260-r1-fact-to-coverage-handoff-contract-freeze-publication.md)、
> [可行性审计](261-r1-fact-to-coverage-handoff-private-implementation-feasibility-audit.md)、
> [实现授权发布](262-r1-fact-to-coverage-handoff-private-implementation-authorization-publication.md)、
> [实现候选](263-r1-fact-to-coverage-handoff-private-implementation-candidate.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只发布 doc259–263 限定的 bounded private A–J 已完成施工、进入受保护 main，并取得候选自己的
local/original PR/exact-main/fresh installed-product/independent reconciliation 资格。它不修改 runtime、tests、Schema、
Profile、Policy、fixtures、corpus、public carrier、Evidence、Bundle、publisher、CLI、Workbench、Core、tag 或 Release。

冻结对象仍是 private、attempt-bound、non-published Fact-stage history handoff。application 只从 exact owned
`OwnedProductFactClosure` 领取 source；claim 时重验 Fact parent、input、Language Support、Parse products、U/E/blockers、
Provider responsibility、observations、FactSet-or-absence、original BudgetContext 与 whole-attempt history。normal 与
safe-negative branches形成 total semantic projection；unsafe/interrupted不能取得 claim。

handoff 与 legacy FactSet-only continuation共享 closure-level one-shot source；固定 application-owned consumer取得
copy-owned、只读 value，不能重跑上游、读取 repository、修改 history 或发布 Coverage。zero denominator、all rejected、
projection blocked、required Provider failure 保持不同 terminal history；unrepresentable U slot不会被伪造成 Fact identity、
任意 digest 或现有 Coverage reason。

## 2. Exact implementation qualification

```text
PR                   = #303
base                 = a174ee739a39a8dda956ff9a8ea899c569a78cf3
head                 = f585cffe54f7949859d3adf76833500f2aa9c76a
ordinary merge       = 83ad8f10b68f1d085b83310613c6f5cc06292d28
candidate/merge tree = 9ab55471f81711fdb80ab6de638c2f504f5ce9b1
diff                 = 1 commit / 7 files / +939 / -9
```

[PR #303](https://github.com/NoctilumeDev/VeriTrail/pull/303) 的 original Public CI
[38702235329](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38702235329) attempt 1 为 11/11 SUCCESS。
exact-main Public CI [38705035837](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38705035837) attempt 1 为
11/11 SUCCESS；Browser Smoke [38705035878](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38705035878)
attempt 1 为 1/1 SUCCESS。ordinary merge parents精确为上述 base/head，merge tree等于受审 candidate tree。

最终 private source的 targeted handoff suite四格各12/12 PASS；handoff + Fact fulfillment + Parse→Fact consumer + Parse
fulfillment组合四格各95 reported，CPython 3.10.6 normal/`-O`各94 passed / 1 skipped，CPython 3.13.13 normal/`-O`
各95 passed / 0 skipped。完整 Review Attention四格各513 reported：3.10两格各512 passed / 1 skipped，3.13两格各
513 passed / 0 skipped。Coverage Schema、Markdown与hygiene窄回归四格各31/31 PASS。

六个固定semantic worlds为normal、optional gap、zero denominator、all rejected、projection blocked与required failure；四格
去provenance canonical semantics一致，SHA-256为：

```text
182a1b233f5bdc4df3638b1e38c5ab38724931768f3c0999398cb15d25fa3a49
```

exact request/execution/terminal/frame bytes另行验证存在；semantic equality不继承nonce-bound claim、run、attempt、
BudgetContext或continuation authority。

## 3. Candidate fresh installed-product readback

在 detached exact `main@83ad8f10...` 上建立 fresh CPython 3.13.13 venv，安装冻结 Core 0.13.0、GitHub Evidence
0.1.0、Playwright 1.62.0 与 matching cached Chromium。公开 wheel只复用重新校验的既有 Release 字节，不声称本轮
fresh download；匿名产品观察清空token、`PYTHONPATH`、`PYTHONHOME`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| doc263 | `r1-fch-implementation-candidate-formal-doc263-1-83ad8f1` | `github-paired-6f7837cdc55f41c48be629c49b7674e6` | `1b3a982185458bdb04f81be586b2f70ed3f79a07eebbc8cc47690430ea7da7d1` |
| milestones | `r1-fch-implementation-candidate-formal-milestones-1-83ad8f1` | `github-paired-47e07f4b40b84772acc9114b708d930a` | `89f436b487a4ebb3c95c825884610ab207576ef88a2ca9595fa02875e166b3b1` |
| README | `r1-fch-implementation-candidate-formal-readme-1-83ad8f1` | `github-paired-ab121fe0adc440918f16b9fca2d20a8f` | `33ae72347a7efad268b0c1607e1ecc0c7e16ac3467013197e9f89f54176994fd` |

三者均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零 conflict/coverage reason/cleanup error/active
stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core，逐项等于producer report；三份public raw bytes
逐字节等于同一exact main的Git blobs。raw-byte check不替代正式产品路径。

candidate independent reconciliation attempt 1 因proof facility把真实祖先文件
`feasibility-audit-closeout.json`错误写成`audit-closeout.json`而失败，保留为
`RECONCILIATION_ANCESTOR_CLOSEOUT_FILENAME_SETUP_ERROR`。版本化attempt 2只修正该path owner并冻结新adapter；三个产品
Plan/session/Evidence/report、oracle、budgets与doc263字节未改变。attempt 2 PASS，SHA-256为：

```text
fa37b88dfc1007bb6eee8494ef5a372c3ab50564f78734ca7234e13f32d5da96
```

144-artifact finite closeout SHA-256：

```text
d69d906750712846a82246ff09050e4a869ed95adc4db6c9760f95727816c767
```

正式history为3 PASS / 0 non-success。三个render diagnostics、anonymous rate/preflight diagnostics、adapter derivation
setup error与两次reconciliation facility observations全部保留且不参与资格。

## 4. Proof strength 与保留历史

本结果只证明fixed audited closed application consumer与private same-attempt handoff。普通Python进程仍具有宿主能力；
固定consumer没有因此变成任意第三方consumer sandbox。handoff不拥有Coverage denominator、item identity、disposition、
FACT_DERIVATION status、seven-stage join或public publication authority。

以下身份继续保留，later PASS不把它们改写成未发生：

- targeted attempt中FCHC-000的`TEST_ASSERTION_TARGET_SETUP_ERROR`与FCHC-009的`NEW_PRIVATE_IMPLEMENTATION_DEFECT`；
- hardening中竞争loser错误撤销winner parent的`NEW_PRIVATE_IMPLEMENTATION_DEFECT`与immutable bytes mutation的`TEST_MUTATION_SETUP_ERROR`；
- first full 3.10 normal在两个既有Slice H falsifier上的`FULL_DISCOVERY_CROSS_MODULE_CONTINUATION_UNAVAILABLE / ROOT_CAUSE_UNKNOWN`；
- 文档窄回归从错误工作目录触发的`TEST_INVOCATION_WORKDIR_SETUP_ERROR`；
- candidate readback adapter derivation setup error、匿名rate/preflight diagnostics与reconciliation attempt 1 proof-facility path error；
- 本 publication 首个四格窄测试调用未安装也未绑定仓库 `src`，22项Schema与5项hygiene已通过，但Markdown模块在导入阶段以
  `ModuleNotFoundError: veritrail`停止，保留为`LOCAL_TEST_INVOCATION_IMPORT_PATH_SETUP_ERROR`；fresh attempt 2只绑定exact
  repository `src`到`PYTHONPATH`，不改测试、产品、文档语义或oracle，四格各31/31 PASS；publication最终字节仍须按§5
  重新取得独立local qualification；
- doc262及更早的FAIL、ERROR、CANCELLED、setup failure、fixture failure与UNKNOWN历史。

safe-negative handoff仍只保存Fact-stage history。zero denominator/all rejected不生成child、FactSet或Coverage item；projection
blocked保留完整constructible U、representable E与blocker；required failure保留完整responsibility和真实non-success history。

doc259–263全文件SHA-256保持：

```text
doc259 = afc40f1226325ac97297863bc99df4f837a37b1617d1c51e5c038cc0f9f39524
doc260 = f81062f62a0de1a174d5f96df9ccd9c5ae7f272b55c7e9585f3cfb27140e731f
doc261 = d2da6ab903516b2ae2ad81715e6cc4d3529b8e79c82e42e68db53cefe5b76821
doc262 = 6ba553ee1f1d6b820aebb458ce34108819c639745c9d7092c837aa603bb54635
doc263 = 012b195db360a61b67cdfb11a117f36b52aa2846be1e7fc9b877f0bc3c0c8806
```

## 5. 本发布自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc259–263、private
modules、`test_fact_to_coverage_handoff.py`、其他runtime/tests/workflows/Schema/Profile/Policy与全部历史合同保持原字节。

本层final-byte local gates只重核publication自己的docs/Schema边界：CPython 3.10.6/3.13.13 normal/`-O`的
docs/Schema regressions、exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences/unique
headings、条件marker、敏感字面量、上述冻结字节连续性、`git diff --check`与read-only hygiene。implementation full runtime
matrix属于已经资格化的candidate tree；publication不重新解释它。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> target PRIVATE_IMPLEMENTATION_FROZEN becomes effective
    -> return CONTROL LOOP
```

本门闭合前，branch中的`FROZEN`只是条件target。candidate readback不能替代本publication的fresh Plan/session/Evidence；
diagnostic不计入资格，所有formal non-success必须保留原身份，N从history机械导出。本地checkout alignment与cleanup是
housekeeping，不追加语义门。

## 6. 后继停止线

本发布不授权persistence Route A/B、Coverage applicability/denominator/item identity/disposition、FACT_DERIVATION status、
Relation/Slice public assembler、ReviewSliceSet/seven-stage Coverage、public Schema/carrier、Evidence/Bundle/publisher、
CLI/Workbench/Core、CLAIM_FIDELITY、tag或Release。

最后门闭合后必须返回[CONTROL LOOP](working-method.md)，重新绑定current main、冻结上游、并行PR与反例。private handoff
implementation frozen不自动授权下一seam；只有现实证明最小问题仍成立，才可另行审计Coverage contract边界。R1完成以前，
外部related-work只留在研究账本，不改变当前合同、实现或调度。
