# R1 application-level unified Review / Coverage output admission 合同冻结发布

日期：2026-11-08

> 条件化状态目标：`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，该目标不是生效事实。
>
> 发布基线：`main@c93ca8d8f556a50cc5e1df6928d272e374e6f67c`，tree
> `7205873b2bb57b30356bb180f596eda4da7d5a80`。
>
> 上游：[最小合同0.1](380-r1-application-level-unified-review-coverage-output-admission-contract.md)、
> [current-state audit successor](379-r1-application-level-unified-review-coverage-output-admission-current-state-audit-successor.md)与
> [readback-target correction](378-r1-application-level-unified-output-admission-audit-readback-target-correction.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改runtime、tests、fixtures、workflow、Schema、Provider、
> Collector、P2/Core oracle、Verdict、Fact/Relation/Slice/Coverage semantics、manifest、Evidence、persistence、public Review或
> R2–R6 authority。

## 1. CONTROL LOOP 与本publication的唯一职责

文档380已经完成自己的final bytes、local qualification、original PR gate、protected exact-head merge、新exact-main双门、fresh
anonymous installed-product readback、independent reconciliation与finite closeout。因此它现在是：

```text
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
```

qualified contract candidate不等于frozen contract。fresh CONTROL LOOP重验原工程问题仍是为normal与negative Review/Coverage结果建立
同一个application-level可判别、one-shot、authority-preserving output admission边界；doc380固定的exact selector claim、original
Fact attempt、DerivationInputSet、live BudgetContext、terminal source、exact nominal result与CoverageLedger root chain共同绑定仍是最小
合法语义边界。没有新证据授权扩大到runtime、same-attempt DerivationEvidence continuity、manifest、Evidence、persistence、public
Review或R2–R6。

因此本文只承担一个职责：在自己的完整资格链成立以后，把doc380固定的semantic bytes从qualified contract candidate发布为frozen
contract。本文不会把合同资格化冒充runtime实现，也不会把形式证明冒充原工程问题已经解决。

## 2. Exact contract candidate qualification

```text
PR                   = #432
base                 = 84d987f1c9a164c04f1b692d7e5872ff555ef2da
head                 = 4314d17331c26ef8c4ede550925c95d764aeda5c
ordinary merge       = c93ca8d8f556a50cc5e1df6928d272e374e6f67c
candidate/merge tree = 7205873b2bb57b30356bb180f596eda4da7d5a80
diff                 = 1 commit / 4 docs files
```

original Public CI `42395635894`、exact-main Public CI `42398054530`与Browser Smoke `42398054526`均为attempt 1
SUCCESS，分别11/11、11/11与1/1；没有rerun。candidate-local Python 3.10.6/3.13.13 × normal/`-O` semantic audit
四格逐字节一致，canonical SHA-256为`f435b49f569f0fb8c0c1032ef5b91a09fcfc508cc454cb92903920e8e4c5ff57`；
focused witness四格各90/90 PASS。local qualification、final diff review、65-artifact post-commit evidence seal、original PR
qualification、protected merge与exact-main gate record SHA-256为：

```text
49236cda2c9b605d8cc649a8a462f9bc8068e26373528ad40adec35c24199eaf
794da6b984c35d0e4151413248996701e1c4332d42966b7b0210f6a6015e3c61
1aa54eb002736cee80006b4589e9e13faaeec012a068be0b3aff0d242d04bd7f
f23824653476d3fc9846203fe9683102839d61fccb235673c1e780cc48b431aa
2f9ab5f79420829265f5af48ab2905231fb5069b176b8627ba90152e701077b4
6ee4dfff370a04f2389e21ae92e6b3d0ac55ba107a613915f392064e2e6390c7
```

candidate source-inventory output truncation、Windows `rg` glob、PowerShell tree-expression、pre-PR seal self-capture与Codex
worktree attachment-cap setup errors全部以原identity保留，qualification effect为`NONE`。later PASS不删除、不解释或回填它们。

## 3. Fresh exact-main installed-product readback

fresh detached exact `main@c93ca8d…`上建立显式CPython 3.13.13 venv，安装公开Core 0.13.0与GitHub Evidence 0.1.0
wheel、Playwright 1.62.0与matching Chromium。产品观察清除GitHub token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，代理只按
命令注入。README与doc380各运行唯一diagnostic和唯一formal；AGENTS与milestones各运行唯一anonymous raw/Contents API/exact-Git
全字节对账，没有复用先前PASS。

| Target | Formal identity | Session / byte identity | Result |
| --- | --- | --- | --- |
| README | `r1-uoa-contract-formal-readme-1-c93ca8d` | `github-paired-63065383b1a147a3bc126ca6fc4c6a70` | API/Render COMPLETE、Core PASS |
| doc380 | `r1-uoa-contract-formal-doc380-1-c93ca8d` | `github-paired-fcd1c0dbca58434e987585a7d6721fee` | API/Render COMPLETE、Core PASS |
| AGENTS | `r1-unified-output-admission-contract-raw-agents-1-c93ca8d` | 591406 bytes / `a49e9cdd…b408` | raw = API = exact Git |
| milestones | `r1-unified-output-admission-contract-raw-milestones-1-c93ca8d` | 651444 bytes / `b7c01706…e32c` | raw = API = exact Git |

pre-observation adapter v4、independent reconciliation、106-artifact finite closeout、expected stdout self-capture mismatch与finite
integrity SHA-256为：

```text
c5f3985160a1b8ed96ff8db9f40bda1f746ed3d59e653be84fa930f114c0a33a
c0b02c74bb497770ad6158faa20d5e2d8d74ea21b986d5273a2ec92f02fa8fd1
0dac8c039601144d1522aff386a00e69ca14e3c61085134b6e1a1f0c86205b0c
3bd879ac78d0d53f9864ba4abdb09696528460303eff324eb59f6902315cefe8
9f3651787b39b4ef37879a08c34556e5070509e4d389a6e2536fb1fa15451892
```

preformal attempt 1因proof marker漏掉“最小”而停止在产品run以前，v4只version该proof facility；原错误SHA-256为
`1920f44905a7cb79a08369834cb52a4330ab43e4696ecd7203c311c0ad245bfd`。fresh worktree attachment cap与anonymous rate
diagnostic #1 remaining 0也按原identity保留。rate reset以后diagnostic #2、API preflight与四项唯一qualifying observation才运行；
这些后继观察不覆盖先前setup/diagnostic identity。

## 4. 冻结对象、问题连续性与authority ceiling

本文发布的唯一semantic对象仍是doc380定义的：

```text
contract function                 r1-application-level-unified-review-coverage-output-admission/0.1
private admission domain          APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_0_1
route/result binding function     r1-application-level-review-coverage-route-result-binding/0.1
application reconciliation        r1-application-level-review-coverage-output-reconciliation/0.1
```

冻结以后仍必须保持：

- normal route只接受exact `OwnedReviewSliceCoverageComposition`，四类negative route只接受exact
  `AdmittedNegativeWorldCoverage`；
- exact selector claim、terminal branch、original Fact closure/attempt、DerivationInputSet、live BudgetContext、route-specific
  source、exact result object与CoverageLedger root chain必须属于同一个application attempt；
- subclass、proxy、copy、foreign attempt、replay、ledger swap、selector/result mismatch、late context stop、mutation、serialization、
  fallback与第二次admission全部fail closed；
- normal Relation-conflict即使`review_slice_set = null`仍是normal-route qualified unknown；artifact presence没有classification
  authority；
- Fact truth、selector、positive/negative downstream、CoverageLedger、Core Verdict与全部历史contract bytes不因本publication改变。

本publication机械分开并绑定：

```text
original engineering problem = 为normal/negative Review/Coverage结果建立共同application output admission边界
current proof obligation      = 本freeze publication自己的全部最后门与跨表面状态一致性
applicability world           = 本candidate exact base/head/tree/final bytes/attempt/fresh readback identity
proof_is_not_problem_solving  = true
```

`CONTRACT_FROZEN`只解除private implementation feasibility的阶段阻断；它不证明可实现，不授权runtime施工，不补齐same-attempt
DerivationEvidence continuity，也不创建manifest、Evidence、persistence、public Review、Core Verdict或R2–R6 authority。

## 5. 本publication自己的exact scope与最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc377–380、
`docs/project-state.md`、runtime、tests、fixtures、workflow、Schema、Provider、Collector、P2/Core oracle、Verdict与全部frozen
semantic bytes必须保持base不变。

本层local gates只重核publication边界：exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique
headings、条件marker、doc380资格与evidence continuity、原工程问题/proof obligation/applicability world分离、`git diff --check`、
read-only global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。Public CI仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc380 / 本文 readback
    -> fresh AGENTS / milestones raw+API+exact-Git byte observations
    -> independent Core / source-byte / problem-identity / retained-history reconciliation
    -> conditional target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP for private implementation feasibility
```

publication自己的fresh Plan/session/Evidence不可由doc380 readback复用；diagnostic不计入资格，任何non-success按原identity保留并停止。
本地checkout alignment、worktree侧栏登记与cleanup只属于housekeeping/setup，不追加语义门。

## 6. 条件化target与停止线

本文进入仓库不等于冻结生效。在自己的全部最后门闭合以前，只能记录：

```text
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_7_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CURRENT_STATE_AUDIT_MERGED_READBACK_NOT_QUALIFIED
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_AUDIT_READBACK_TARGET_CORRECTION_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CURRENT_STATE_AUDIT_SUCCESSOR_AUDITED_QUALIFIED_HISTORY
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本文最后门全部闭合以后，开头的conditional target才成为事实。随后必须从新的exact main返回CONTROL LOOP，独立审计private
implementation feasibility；不得把合同冻结解释为runtime已开始，或直接施工manifest、Evidence、persistence、public Review或
R2–R6。
