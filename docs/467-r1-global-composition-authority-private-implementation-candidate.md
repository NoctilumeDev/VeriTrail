# R1 global composition authority private implementation候选

日期：2026-11-28

> 候选状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造基线：`main@fc3345f032aa4df558cdb86b39284c22b5d99505`，tree
> `79b0507047bd74d53cc23bae93767b55ad7ad591`。
>
> 上游：[versioned contract](463-r1-versioned-global-composition-authority-contract.md)、
> [contract freeze](464-r1-global-composition-authority-contract-freeze-publication.md)、
> [feasibility audit](465-r1-global-composition-authority-private-implementation-feasibility-audit.md)与
> [private implementation authorization](466-r1-global-composition-authority-private-implementation-authorization-publication.md)。
>
> 影响：`L2_BOUNDED_PRIVATE_IMPLEMENTATION / FOCUSED_TESTS / CANDIDATE_DOCUMENTATION`。本文不新增public
> export、Schema、CLI、publisher、persistence、Core Verdict、Workbench route或公开Review产品，也不启动外部开源系统集成、
> R2–R6或R1后的human+AI全项目检查。

## 1. CONTROL LOOP、精确授权与不继承资格

PR #531已经把doc466从base `47dde07519034191ba1cf7f1f7f36eeae1ee362f`、head
`16c3a655c774ffc1cffaf74947559e3557f80316`精确合入当前基线。original Public CI `46125384012`、exact-main
Public CI `46128932412`与Browser Smoke `46128932318`均为attempt 1 SUCCESS（15/15、15/15、1/1）。fresh
README/doc465/doc466 Render与AGENTS/milestones raw-byte observations各有唯一qualifying PASS；independent reconciliation、
135-artifact finite closeout与post-closeout integrity SHA-256为：

```text
94d54677edff3a9ac3efddbf3539c7714506d856c23c41e9d06dc6a54f2f0e52
e1195beb605e0ec8dbcf65a720ccad5676b70ebd19c6217878c1498a2e981d48
3267403443ba5bc190a7355d73e142dc6a04645455d5701b6e49cfd1f90fe904
```

因此`R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_ALLOWED`已经生效，同时implementation在该publication闭合时仍为
`NOT_STARTED`。fresh CONTROL LOOP从新的exact main重读三份控制文件、doc463–466、冻结private chain、PR #531完整证据与全部
保留失败，没有发现击穿A–J授权的新反例；当前最小合法seam只是一个private owner模块、一个focused test模块及其候选事实投影。

本候选不继承doc465 feasibility witness或doc466授权publication的qualification。相同设计、摘要或测试语义也不能替代本候选自己的
local/original PR/protected merge/new exact-main/readback/reconciliation链。

## 2. exact scope与bounded实现

候选只允许以下六文件scope：

```text
README.md
AGENTS.md
docs/467-r1-global-composition-authority-private-implementation-candidate.md
docs/milestones.md
plugins/review-attention/src/veritrail_review/_global_review_composition_authority.py
plugins/review-attention/tests/test_global_review_composition_authority.py
```

两份产品/focused witness final bytes为：

| 对象 | SHA-256 |
| --- | --- |
| private global composition owner / independent admission / one-shot result | `ed2cb31b5186aa71bb0da0fc6f02fc4d20e90888ae81376cc4e3a036ccccc9bf` |
| focused eight-world and falsifier witness | `1a70d1fc6b1a4a0911390766871ddb19adc21ab09177d7e2c2c7f5a3d6686352` |

实现只创建private identity `R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1`、versioned owner/binding/composition/admission/result、一个
live `BudgetContext`和一个same-attempt capture slot。四个normal world只走`RELATION_HANDOFF`，四个qualified negative只走
`FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2`。完整Fact、Relation、Slice/Coverage、continuity、Carrier、Manifest 0.2、private
staging、cleanup与terminal phase均在独立global admission中按copy-owned exact material重算。

owner传播最早底层failure；unknown保持`UNKNOWN`；partial、late mutation、foreign attempt/context、roster drift、cross-world splice、
Manifest staging replay、cleanup failure和并发双消费全部typed fail closed。qualified negative world是完整成功结果，interrupt、unsafe、
partial或cleanup-failed attempt不得借negative vocabulary冒充成功。result不可复制、pickle、JSON恢复或重复领取；它不是Artifact、
Evidence、Manifest替代品或Core Verdict。

`veritrail_review.__init__`、`pyproject.toml`、publisher、public/default composition、冻结private successor、Core、persistence、Schema、
fixture、workflow与primary audit均未修改。

## 3. formal以前的反例与最小修正

完整diff review在formal qualification以前发现并修正四类产品边界：

1. `PREQUAL-REVIEW-001`：并发consumer会让失败的replay consumer撤销唯一active validator，使两个consumer都失败；最小修正让只有
   active validator拥有成功/失败状态转换权，保留第一次Python 3.13 normal失败run。
2. `PREQUAL-REVIEW-002`：independent admission最初没有独立重算完整downstream digest；修正后不再依赖producer expected projector。
3. `PREQUAL-REVIEW-003`：Carrier future-consumption envelope的identity、validation与authority ceiling绑定不完整；修正后逐项重验。
4. `PREQUAL-REVIEW-004`：continuity、cleanup、terminal phase与最终result admission的独立重算不完整；修正后全部绑定实际快照。

这些反例都发生在final byte seal以前。targeted attempt 5中新加test-only coherent mutation缺少`hashlib`产生proof-facility
`NameError`，GCA-007在同run通过；修正test import后只以新identity重跑GCA-002。错误worktree/provider lookup、wrong document name、
CoverageLedger shape/stage假设、missing helper、lost process handle、patch syntax、tool invocation、Windows wildcard与broad lookup truncation
等setup failures均按原identity保留，不能被后继PASS解释成从未发生。

## 4. final fixed-byte local qualification

final focused matrix在CPython 3.10.6 / 3.13.13 × normal / `-O`四格各运行10 tests并全部PASS：

| cell | elapsed | log SHA-256 |
| --- | ---: | --- |
| Python 3.10 normal | 370.689s | `087ffcb422861dac3b2dd87f622845dc6801999d316b602f302a4bb2dc5d056e` |
| Python 3.10 `-O` | 360.126s | `55ec2c4dbfb7cd0aafbac073a92d990680af4baf77b3bcc5ccbccc2bdec8c3e6` |
| Python 3.13 normal | 226.185s | `befce0929f8225d220494074ba056afd7450ede91710f931e13c340a12bc5a5d` |
| Python 3.13 `-O` | 237.192s | `1a7a0c29e8d7d4a6214e84a6f48a25ee9d3ccbad572ad21cdb39357cb7063da4` |

full Review Attention matrix四格各reported 725 tests：Python 3.10为722 passed / 3 skipped，Python 3.13为723 passed / 2 skipped。
四格日志SHA-256依次为：

```text
6c89d183f8a51acbb5d6d49c52eb3fdcc7440586ed114b3e35c4d6c1d9431e82
8d7a4671f440d565afd5340d58d141c6f35175fd0b55ce494aaf62770032a194
f94e087f3603416ca14060a3f069afc6bda4b26b085a24416dc1e239ab5e8088
19a0ff3af0f588acf5059b17304e69982bb8e23f95fa8ec7063bc776edcd6dee
```

semantic projection attempt 1把每次重新取得attempt/ProviderRun identity的`DERIVATION_EVIDENCE`与`COVERAGE_LEDGER`
file semantic digest误当成跨run稳定值，四格产品执行都exit 0但得到四个不同投影摘要；矩阵以SHA-256
`3c0a81931a0027692dde611609ac8f7cdfb0d00403bcd652e68d9457c283987b`永久保留为
`SEMANTIC_PROJECTION_BOUNDARY_OVERCLAIM_NON_SUCCESS / NON_QUALIFYING_NONE`。

attempt 2没有弱化单次run的独立admission：每格仍复算exact Carrier、Manifest、cleanup与result binding；跨run只比较version、八个
world、route、root topology、Manifest role topology/digest shape、cleanup、authority ceiling与typed fail-closed families。四格共同
semantic projection SHA-256为`953f762c737f7ea5edc661953a08ddc1134fb241e21c664c8cef5e208e530b8c`，矩阵SHA-256为
`da1576c53185427f3824b9c3e5f2a1610d5f12742484d25317d820aed22c99b7`。

compile 4/4、global/local hygiene 8/8、UTF-8/LF/final-LF、exact status、public surface absence、产品无`assert`与primary audit continuity
全部PASS；pre-document static qualification SHA-256为
`9298e6e71448a763afade79b52cd7da89803aa523e68395556d440e1a10d1337`。这些都只作local witness，不使candidate qualified或frozen。

## 5. 必须继续保留的non-success

后继PASS不得删除、覆盖、改名或解释：

- 本候选`PREQUAL-REVIEW-001..004`、targeted proof-facility import error与全部15项setup/lost-handle/UNKNOWN identity；
- semantic projection attempt 1四个不同摘要与总矩阵`NON_SUCCESS`；
- doc462 audit attempt 1/2、PR #527 README anonymous rate ERROR、PR #529 HTTP 503/PARTIAL/ERROR/UNKNOWN、doc465错误test-root、
  PR #530/#531 proof-facility与sidebar attachment cap setup failures；
- PR #519、#498及更早全部FAIL、ERROR、CANCELLED、setup failure、fixture failure与`UNKNOWN`。

primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须继续保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 6. 本候选的完整资格责任

最终六文件字节形成后必须重新执行exact scope、UTF-8 without BOM、LF/final LF、links/fences/headings/required markers、产品SHA、
semantic attempt 2 seal continuity、`git diff --check`、global/local hygiene与primary audit continuity；随后形成不可变单一commit与PR body
seal。

```text
candidate final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original PR Public CI 15/15 attempt 1 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc466 / 本文 / milestones readback
  -> fresh AGENTS raw/API/exact-Git byte observation where declared
  -> independent source / contract / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
  -> return CONTROL LOOP
```

每个formal identity只运行一次；已PASS目标不得重复。fresh product readback必须清除GitHub token、`NO_PROXY`、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令使用`http://127.0.0.1:7897`。任何non-success保留原identity并停止，不得rerun until PASS、弱化oracle、
拼接不同world或用后继PASS回填首败。

## 7. authority ceiling与当前停止线

本文自己的完整资格链闭合以后最多只能成为：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

随后必须返回CONTROL LOOP，另建独立docs-only implementation freeze publication并完成自己的local/original PR/protected merge/new
exact-main双门/fresh installed-product readback/independent reconciliation/finite closeout。只有该publication全部门成立，才可使
`R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_FROZEN`生效；本文不授权直接启动public Review、外部开源系统集成、
R2–R6或R1后的human+AI全项目检查。
