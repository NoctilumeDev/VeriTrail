# R1 Fact→Coverage exact-input successor 私有实现授权恢复发布候选

日期：2026-10-27

> 状态：`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@ebeb890da1936cc15bcefe7e23c9bd532efd4787`，tree
> `8b14018edf7f77b6bc5eb540204e8e084243c43b`。
>
> 上游：[private implementation feasibility audit](320-r1-fact-to-coverage-exact-input-successor-private-implementation-feasibility-audit.md)、
> [0.2 contract](321-r1-fact-to-coverage-exact-input-handoff-successor-contract.md)、
> [contract freeze publication](322-r1-fact-to-coverage-exact-input-successor-contract-freeze-publication.md)、
> [maintenance failure boundary](324-r1-workbench-vitest-undici-maintenance-exact-main-qualification-failure-boundary-audit.md)与
> [maintenance qualification recovery](325-r1-workbench-vitest-undici-maintenance-qualification-recovery.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只发布一份条件化的bounded private implementation
> authority；不修改runtime、tests、workflows、fixtures、Schema、Profile、Policy、Coverage、manifest、Evidence、persistence或
> public Review产品。本文自己的完整资格链闭合以前，`ALLOWED`不生效。

## 1. publication输入已经取得资格

文档320已由PR #367完成自己的original/exact-main双门、fresh anonymous installed-product
README/doc319/doc320/milestones读回、independent reconciliation与finite closeout，成为
`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。对应reconciliation与closeout SHA-256为：

```text
2959c0b5288abd97e15e00547a6845327f8ee64849e095831d33d0314877beb5
7d235b233a27878dfe8e6150a6eaf0d0485ccfe024b78e8cfcc4de621e96e9a0
```

文档321随后由PR #368完成资格链，成为`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`；文档322由PR #369完成自己的
original/exact-main双门、fresh readback、independent reconciliation与finite closeout。因此：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
```

第一次authorization PR #372在original Public CI `40470062665` attempt 1命中Vitest 4.1.11与undici 7.30.0的五个
advisory，关闭且未合并，永久保持`CLOSED / UNMERGED / NOT_QUALIFIED`。独立maintenance PR #373把Vitest/
`@vitest/mocker`更新到4.1.12、undici更新到7.30.1；其original门成立，但merge `5aeb53e…`的exact-main Public CI
`40478059827` attempt 1在既有Python 3.10 M10正向fixture中观察到expected `PASS`、actual `FAIL`。由于日志没有保留
decisive assertion与临时Bundle，precise cause保持`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，没有rerun或installed-product readback。

文档324经PR #375建立qualified failure-boundary history；第一次original run的concurrency cancellation和milestones formal #1
匿名额度ERROR均永久保留，后继PASS不覆盖它们。其independent reconciliation与151-artifact closeout为：

```text
ebe07c9fd593d1f0c5d50d90677f6499352ad50c0169a14ee8f891f2b7d8915c
9bc218b6f52b6758f0b53dbb76ee0d063bc247254aedc8614894861fe59b05f2
```

文档325随后由PR #376以exact head `01267dc…`合入`main@ebeb890da1936cc15bcefe7e23c9bd532efd4787`；original Public CI
`40495667837`、exact-main Public CI `40499231916`与Browser Smoke `40499231632`均为attempt 1 SUCCESS。fresh anonymous
README/doc324/doc325/milestones 4/4取得唯一`FORMAL_READBACK_PASS`，P1/P2 coverage均为`COMPLETE`，Core均为`PASS`。
independent reconciliation与167-artifact closeout分别为：

```text
5f514c9fbcb24e1a89154632dc79cfe2407f8bd3293b0243f7bbd6082ab5b559
31c83dc18a5b19b98d95779b61dfa6895a00205d7b9ca56a2fe39d09457488a0
```

`--no-index`误把两份public product wheel目录当作完整dependency wheelhouse、以及首次Plan id前缀超过64字符的两个本轮
readback setup ERROR均按原身份保留，qualification effect为NONE。因此maintenance recovery现为
`AUDITED / QUALIFIED_HISTORY`，但#372/#373没有被回填，implementation仍未授权。

## 2. fresh continuity audit没有发现新的反例

本文施工前从exact main `ebeb890…`运行了独立read-only continuity audit。它没有复用文档320或文档325的结论来替代当前世界，而是重新检查：

- 文档320已审的四个关键private source文件从`9701b192…`到当前HEAD无字节漂移；
- 文档320、321、322、324、325字节与feasibility、contract freeze、maintenance recovery的reconciliation/closeout身份保持精确；
- PR #372的closed/unmerged/not-qualified身份与PR #373的`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`保持原样；
- `r1-fact-to-coverage-exact-input-handoff-successor/0.2`、
  `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`、
  `r1-negative-world-coverage-exact-input-consumer/0.1`、
  `r1-terminal-validated-original-derivation-input-carrier/0.1`与
  `TERMINAL_VALIDATED_ORIGINAL_DERIVATION_INPUT_SET_REFERENCE`仍是冻结身份；
- 五个终态world与三个zero-Parse denominator world重新成立；
- equal-bytes/equal-digests foreign `DerivationInputSet`仍不能冒充原始对象；
- shared one-shot replay、late stop与required-provider-failure后的普通live accessor仍fail closed；
- Python 3.10.6 / 3.13 × normal / `-O`四格语义报告一致；相关focused suite每格99/99 PASS。

continuity qualification SHA-256为：

```text
a6aa4f4fa8ee63431cfb89b10867d66fa78ff39304ee610c7bc5983b5f00a588
```

Codex worktree工具因当前app工作目录不是Git仓库而返回`Not a git repository`；该setup ERROR已经保留且明确
`qualification_effect = NONE`。后继从显式VeriTrail仓库与exact commit建立隔离worktree；错误不属于产品或审计证据。

## 3. 授权对象是bounded A–I，不是开放式Coverage重写

本文最后一门闭合后，唯一允许的private implementation scope如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 增加冻结的0.2 handoff function、claim purpose、private consumer与private carrier identity；旧0.1 identity、bytes和入口保持不变。 |
| B | 在Fact parent内部增加parent-only terminal accessor；它必须先完整执行既有`_handoff_source_document(closure)`验证，并在同一同步调用内原子返回source、原始`BudgetContext`与parent-bound原始`DerivationInputSet`。 |
| C | 新0.2 claim必须与legacy continuation、Coverage 0.1和Relation handoff共享closure级`__claimed` one-shot slot；不得创建第二个可重放claim域。 |
| D | carrier绑定原始inputs对象身份、input-state seal、三份canonical bytes、verified blob key/bytes、五个digest、live context identity与私有构造token；equal foreign reconstruction一律拒绝。 |
| E | required-provider-failure branch只消费terminal validation已证明的bound original inputs；不得调用会因parent eligibility为`REVOKED`而失败的普通live `_inputs_ref()`，更不得恢复eligibility。 |
| F | carrier每次读取都重新检查live context、deadline/stop、input seal、source/input五digest、对象图和claim token；晚到stop、reseal drift、foreign context或重放均fail closed。 |
| G | 覆盖`NORMAL_FULFILLED`、`ZERO_PARSE_DENOMINATOR`、`ALL_PARSE_REJECTED`、`PROJECTION_BLOCKED`、`REQUIRED_PROVIDER_NON_SUCCESS`五world，以及empty inventory、unsupported-only、policy-excluded-only三分母world。 |
| H | carrier只允许copy-owned SourceSnapshot、ReviewPolicy、DerivationProfile、verified blob identity/bytes、五digest、0.1 Fact终态与same-object-graph proof；不得创建Coverage obligation/item/status/ledger。 |
| I | 增加对应private tests与audit fixtures并运行四格falsifiers；旧Provider/public export/default composition、0.1 handoff、Relation路径、Schema、Profile与Policy保持不变。 |

上述scope实现的是“把已经通过Fact终态验证的原始输入对象安全交给后继private consumer”。它不实现Coverage producer，不选择Coverage
obligation projection，不生成manifest role，不构造same-attempt Evidence，也不授予状态完成权。

## 4. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded private exact-input successor A–I
+ 增加对应private tests / audit fixtures
+ 运行既有Fact终态验证、shared one-shot与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改public Schema、Policy/Profile、Fact truth或FactSet identity
过滤、重建或用equal foreign input替代原始DerivationInputSet
恢复parent/child eligibility或跨attempt拼接authority
创建Coverage obligation/item/status/ledger
恢复或消费旧composition authorization
实现manifest 0.2 successor或same-attempt Evidence continuity
选择persistence
启动public Review、post-R1 Benchmark或R2-R6
发布tag / Release
```

`ALLOWED`也不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。实现必须拥有新的source、branch、candidate
head/tree、原始PR门、protected merge、exact-main双门、fresh installed-product readback与independent reconciliation；真实反例出现时
立即停止当前施工，只重开被击穿的最小边界。

## 5. 历史authority和后继阶段不能被偷换

以下推导继续禁止：

```text
doc320 feasible == implementation authorized
contract frozen == implementation started
same bytes/digest == same object identity或same attempt authority
terminal validation == Coverage producer authority
exact-input carrier implemented == Coverage obligations complete
后继PASS == 覆盖任何先前FAIL/ERROR/UNKNOWN
```

实现候选即使取得资格，也只能返回CONTROL LOOP，分别审计Coverage producer、manifest 0.2 successor与same-attempt Evidence continuity所需的
新authority；不得顺序继承。

## 6. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/326-r1-fact-to-coverage-exact-input-successor-private-implementation-authorization-recovery-publication.md
docs/milestones.md
```

doc320–325、runtime、tests、workflows、fixtures、Schema、Profile、Policy、Coverage、manifest、Evidence、persistence与public产品必须保持
`ebeb890…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
`git diff --check`、read-only hygiene、0.2 continuity qualification、feasibility/contract/failure-boundary/maintenance-recovery
reconciliation与closeout、#372/#373全部保留的FAIL/ERROR/setup/UNKNOWN历史及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc321 / doc322 / doc324 / doc325 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用本publication的
original PR green、相同tree、相同semantic digest或后继PASS替代任何一门。

## 7. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_CONTRACT_FROZEN
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_AUTHORIZATION_RECOVERY_PUBLICATION_CANDIDATE
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_CONTRACT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内开始新的private implementation
candidate；不得把authority publication本身算作实现证据。
