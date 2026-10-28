# R1 negative-world Coverage authority recovery 私有实现授权发布候选

日期：2026-10-28

> 状态：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@91a7e6ba466b375ff6e4568ccc3a57ddd60ca044`，tree
> `47d6bfdad66f022bf386b5c1e2bf2b2d2f9a2171`。
>
> 上游：[0.1合同](332-r1-negative-world-coverage-authority-recovery-contract.md)、
> [合同独立冻结发布](333-r1-negative-world-coverage-authority-recovery-contract-freeze-publication.md)与
> [private implementation feasibility audit](334-r1-negative-world-coverage-authority-recovery-private-implementation-feasibility-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只发布一份条件化的bounded private implementation
> authority；不修改runtime、tests、workflows、fixtures、CoverageLedger 0.3、positive composition、Fact terminal、manifest、
> Evidence、persistence或public Review。本文自己的完整资格链闭合以前，`ALLOWED`不生效。

## 1. publication输入已经取得资格

文档334由PR #385 final head `aaf5980b6721dfa34001b0554d34b6416253b7a9`从
`main@637c51079151860e2634c1e7cdc60655ebf9ca45`建立；candidate与merge tree均为
`47d6bfdad66f022bf386b5c1e2bf2b2d2f9a2171`，受保护合入后的exact main为
`91a7e6ba466b375ff6e4568ccc3a57ddd60ca044`。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #385 original Public CI | `40691909691` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `40695985547` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `40695985611` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc333、doc334与milestones各有唯一`FORMAL_READBACK_PASS`。independent
reconciliation、272-artifact versioned successor closeout、保留的stdout self-capture mismatch与finite integrity分别为：

```text
81ba15df22399af8de1378a3dc159b70652f4f8be918237eca3307a465af084b
0ff6fbf2c6c6f20435a0ae04a08c3f14f279184b94cc1fcd47faae3d3c835438
9914883f492792ea91ab7c3cc28322d615617905b99268f50f29c750ab4479e7
c115f28ecbd8e0327314f33d4c7ddcb56264fb802f85068a108325519b085eb9
```

doc334 full-file SHA-256为：

```text
6a6710dee095c3f9c52989906b84336a99f06fb46228c78bb319559a8a7347dc
```

因此文档334现在是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。合同保持`FROZEN`；runtime implementation在本文最后门
闭合以前仍是`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 保留失败不被授权发布重解释

以下身份继续按原样保留：

- setup1创建长路径detached worktree时命中Windows path-length错误；setup3短根只证明同一exact commit可被重新观察；
- setup2 README formal #1在写AcceptanceBundle时命中path-length ERROR；它不是PASS，也没有被setup3回填；
- setup3 README formal #2与后继diagnostic观察到public-render navigation ERROR，P1 COMPLETE但P2未完成，根因保持UNKNOWN；
- 第一个closeout后完整性checker使用了错误stdout文件名；第一个recovery checker又正确发现setup history在closeout后新增记录导致
  原closeout有两项漂移；两次都不取得资格；
- versioned successor closeout只冻结新的closeout identity与正确的stdout identity。原closeout SHA-256
  `19c1647f04cca11a2be91e94eda71a1dcfda1c641ea0f49446586da2dd1644c5`、filename错误记录
  `e7db8120b8ed6d2e3609f71af767b603b218debd5301c25a846d42130479203e`与history-drift记录
  `761cefb5f062c5ddf30933f87ad8f45c071bf2ebebd6dc14068415e1c1c4af99`均继续存在。

这些事实证明“proof facility可以被版本化修正”，不证明旧观察没有发生，也不扩大runtime authority。

## 3. 授权对象是bounded A–J

本文最后门闭合、返回CONTROL LOOP且前提仍成立以后，唯一允许的private implementation scope如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 消费同一live 0.2 exact-input carrier；绑定原始Snapshot、Policy、Language、Parse、Fact、blob map、五digest、`BudgetContext`与Fact terminal source，并先重验claim仍live。 |
| B | 新建versioned private producer / independent-validator / admission identity；旧Fact handoff、CoverageLedger 0.3与positive composition identity保持不变。 |
| C | producer从original carrier完整构造七个live denominator world的CoverageLedger 0.3 candidate，保留branch-specific absent roots、stage history与Provider outcome。 |
| D | validator不调用producer的denominator、root、stage或branch helper；它从同一original carrier独立枚举完整分母并生成自己的conformance source。 |
| E | empty、unsupported-only与policy-excluded-only即使共享`ZERO_PARSE_DENOMINATOR`也分别得到COMPLETE/PARTIAL/PARTIAL；all-rejected、projection-blocked、Provider failed/unavailable保持各自terminal语义。 |
| F | 既有0.3 validation-only conformance只比较validator独立构造的source与candidate；不得把producer source或caller缩小后的输入作为expected。 |
| G | admission绑定同一live carrier、同一`BudgetContext`对象、candidate digest、validation result与same-attempt claim；只允许exactly-once phase commit。 |
| H | 直接拒绝self-consistent denominator shrink、branch rewrite与fixture-without-live-admission；agreement不能替代original-input completeness。 |
| I | 保持deadline、stop、revocation、resource closure与shared one-shot ceiling；foreign context、late stop、replay或revoked upstream不得恢复authority。 |
| J | 增加对应private tests与audit fixtures，运行Python 3.10.6/3.13.13 × normal/`-O`及focused falsifiers，并证明旧public/default composition字节与行为不变。 |

类名、方法名、锁与retention布局仍由实现候选决定。实现可以复用canonical serializer、frozen enums、0.3 conformance与phase-commit
primitive；不得让producer与oracle共享被测试的关键denominator/root/stage projector。

## 4. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded private producer / independent validator / admission A–J
+ 增加对应private tests / audit fixtures
+ 运行既有Fact terminal、CoverageLedger 0.3 conformance与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改CoverageLedger 0.3 Schema、reason order或positive composition
修改Fact terminal、0.2 carrier identity或public method list
从actual output、producer source或caller-supplied projection反推denominator
恢复或消费旧composition authorization
选择或实现manifest successor / same-attempt Evidence continuity
选择persistence
启动public Review、post-R1 Benchmark或R2–R6
发布tag / Release
```

`ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。runtime patch必须拥有新的source、
branch、candidate head/tree、原始PR门、protected merge、exact-main双门、fresh installed-product readback与independent reconciliation；
真实反例出现时停止当前施工，只重开被击穿的最小边界。

## 5. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止：

1. original carrier不能独立恢复七个world所需的完整Snapshot/Policy/Language/Parse/Fact denominator；
2. Provider responsibility或Fact terminal branch必须由caller或producer自行选择；
3. producer与validator只能共享同一个关键denominator/root/stage projector；
4. one-shot admission要求修改0.2 identity、public method list或恢复revoked upstream eligibility；
5. 0.3 conformance、positive composition或frozen fixtures必须被弱化才能通过；
6. negative result必须先取得manifest、Evidence、persistence或public authority才能存在；
7. phase commit无法绑定同一live carrier/context/candidate/result，或resource closure无法在commit前机械证明。

授权已经生效也不能成为修改oracle、扩大scope或静默reopen frozen contract的理由。

## 6. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/335-r1-negative-world-coverage-authority-recovery-private-implementation-authorization-publication.md
docs/milestones.md
```

doc332–334、runtime、tests、workflows、fixtures、CoverageLedger 0.3、positive composition、Fact terminal、manifest、Evidence、
persistence与public产品必须保持`91a7e6b…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、
links/fences/headings、required markers、`git diff --check`、read-only global/local hygiene、doc334 full-file SHA、#385
original/exact-main双门、四份formal identity、全部retained non-success、independent reconciliation、successor closeout与finite integrity、
primary `audit.json` continuity。focused matrix与read-only feasibility audit必须从当前base fresh复算；它们只作witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc334 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用本publication的
original PR green、相同tree、相同semantic digest或后继PASS替代任何一门。

## 7. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内开始新的private implementation
candidate；不得把authority publication本身算作runtime证据。
