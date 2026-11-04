# R1 post-terminal Fact dual-successor 私有实现授权 successor 0.2 发布候选

日期：2026-11-04

> 状态：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_SUCCESSOR_0_2_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@a1899bc857d7933833b4b2393ae1bd7a71af2e14`，tree
> `19a897fcba6fed897c2fd8d51beff65a668d8876`。
>
> 上游：[0.1合同](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)、
> [合同独立冻结发布](341-r1-post-terminal-fact-dual-successor-authority-recovery-contract-freeze-publication.md)、
> [private implementation feasibility audit](342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md)与
> [Workbench dependency audit recovery](344-r1-workbench-dependency-audit-recovery.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文是失败的doc343 / PR #395之后从新exact main
> 重建的versioned successor，只发布一份条件化bounded private implementation authority；不修改runtime、tests、workflows、
> fixtures、Fact/Relation/Coverage Schema、manifest、Evidence、persistence或public Review。本文自己的完整资格链闭合以前，
> `ALLOWED`不生效。

## 1. publication输入与恢复地基已经分别取得资格

文档342由PR #394以
`base=99244df24360787b5f1b97a1cad89dc26d8aefe0 / head=3abf3afc56f9e00622e34f9e320ae16ae2f75d47 /
tree=be764de0a27d1b61cc1f0d51f14a29ad3894ce58`受保护合入`main@2e9e5fbb56c84152de6a90be535345666becb733`。
original Public CI `40848292961`、exact-main Public CI `40853811383`与Browser Smoke `40853811154`均为attempt 1
SUCCESS；fresh README/doc341/doc342/milestones、independent reconciliation与finite closeout已经闭合。因此doc342保持
`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`，合同保持`FROZEN`。

第一次authorization publication的doc343 / PR #395没有取得资格。required Workbench job在original Public CI
`41811545926` attempt 1观察到16个moderate advisory；该PR没有rerun，已经关闭且未合并。clean exact base对同一lock
复现相同live audit，因此只能成立：原required gate真实失败，authorization content failure与candidate regression没有建立，
external advisory activation根因保持`UNKNOWN`。doc343、head `a9824e8451cc61242884cefb23b6c772aba07bee`与tree
`0725a796cbecda85397969c4762ce6d488b11a64`继续只属于失败world，不被本文复用。

fresh CONTROL LOOP建立的doc344 maintenance只收敛Workbench dev dependency graph，保持原required audit oracle、workflow、
Workbench source/tests与R1 semantics不变。PR #396的exact资格链为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #396 original Public CI | `41819486547` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `41824009644` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `41824009444` | 1 | 1/1 SUCCESS |

protected merge为`main@a1899bc857d7933833b4b2393ae1bd7a71af2e14`，tree
`19a897fcba6fed897c2fd8d51beff65a668d8876`。fresh anonymous installed-product README、doc342、doc344与milestones
各有唯一qualifying PASS。independent reconciliation、218-artifact finite closeout、保留的stdout self-capture mismatch与finite
integrity分别为：

```text
8f4d91fb0f25bd305fd3bce951c7363ef91addf18adaca5eaede708295ae6566
843f1986666c9b568e6e088a51dc986a38807a998023a95651677ef375781069
ed74a25cc5702ef18e66d2320ce8f8f08b1556f77e2d77f1586ec8ee230fcd4e
c48361e22262e5a9c9f380b6297cbdb17e9e8734834f69743da8a0c3c07af944
```

因此doc344现在是`R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`。这项新事实只解除后继候选再次面对同一
required Workbench audit的地基阻断；它不回填#395，不把dependency maintenance算作R1语义证据，也不自动授予runtime authority。

## 2. 保留的non-success不被successor重解释

以下身份继续按原样保留：

- #395 original Public CI失败、关闭且未合并；doc343及其base/head/tree永不升级为qualified publication；
- exact-base复现16个moderate advisory只排除candidate regression，不证明GitHub、npm registry、代理、具体advisory或时间窗口的单一根因；
- maintenance构造阶段所有lock refresh、wrong-workdir、PowerShell、registry partial、unsupported flag与hash-capture setup errors；
- Node 20.19.0在candidate与clean exact base上相同的6 files / 79 tests WebCrypto realm失败；candidate regression
  `NOT_ESTABLISHED`，底层原因仍为`UNKNOWN`，required Node 22 PASS不覆盖它；
- maintenance fresh readback的README formal #1 marker-selection proof-facility ERROR与formal #2 anonymous rate
  exhaustion ERROR；后继README formal #3 PASS不回填前两项；
- anonymous rate/preflight多轮`remaining 0`、首次DateTimeOffset比较setup error与三次post-reset continuity history；
- finite closeout只对218项冻结索引负责；stdout自捕获项按独立mismatch identity保留。

这些事实只证明maintenance在保持原始失败身份的前提下恢复了required gate，不扩大本文的语义或施工边界。

## 3. successor 0.2授权对象仍是bounded A–J

本文最后门闭合、返回CONTROL LOOP且前提仍成立以后，唯一允许的private implementation scope如下：

| 项 | 最小施工责任 |
| --- | --- |
| A | 新建versioned private `POST_TERMINAL_DUAL_SUCCESSOR_0_1` Fact consumer factory、selector与claimed-route carrier；pre-terminal只绑定original inputs/context、完整Policy/Profile、Fact assignment、identity与一个shared slot，状态只能是`SEALED_NOT_ROUTABLE`。 |
| B | Fact terminal以后从同一original consumer与complete closure独立重验exact五分支，并机械形成total/disjoint的normal→Relation、四类negative→exact-input 0.2映射；不得读取downstream candidate反推branch。 |
| C | shared slot只允许`SEALED_NOT_ROUTABLE -> TERMINAL_READY -> CLAIMED_RELATION | CLAIMED_EXACT_INPUT`；pre-terminal、wrong-route、validation failure、copy-equal、replay、version mismatch或并发loss永久`REVOKED`，禁止fallback。 |
| D | normal route签发private Relation claimed-source carrier，完整保留same Policy/Profile、authoritative FactSet、accepted products、per-product MODULE closure、terminal history、original input与live `BudgetContext`；既有Relation transition入口只允许claim后委托同一执行体。 |
| E | 四类negative route只签发现有Fact→Coverage exact-input successor 0.2 carrier；其identity、original input/blob maps、五digest、terminal source、negative producer、independent validator与admission保持不变。 |
| F | application独立核对selector route与terminal branch；selector、Relation path及negative producer不得共享由downstream期望结果、denominator或candidate推导branch的关键projector。 |
| G | 每次读取继续重验same-object graph、same attempt、live context、deadline/stop、input seal、terminal source、route与consume state；copy、serialization、digest equality或重构不得继承authority。 |
| H | 实现冻结合同列出的八类private failure family；unsafe claim表示没有route authority，不生成合法`UNKNOWN`产品，也不修改既有Fact/Relation/Coverage reason enum。 |
| I | 保持`LEGACY`、`RELATION_TRANSITION`、exact-input 0.2、Fact terminal、corrected Relation Provider、positive/negative composition、public exports、Schema、manifest/Evidence/persistence与global composition authority bytes和行为不变。 |
| J | 增加focused private tests与audit fixtures，机械覆盖`PTDS-000`至`PTDS-017`，运行Python 3.10.6/3.13.13 × normal/`-O`、旧consumer回归、full Review Attention、compile/hygiene/scope/audit continuity并形成独立implementation candidate。 |

class、method、field、lock与retention布局仍由实现候选决定。可以复用既有canonical serializer、frozen enum、terminal source
revalidation与one-shot primitive；不得让selector与任一downstream producer共享被测试的关键branch projector。

## 4. authority ceiling

本文最后门闭合以后只允许：

```text
实现 bounded private dual-successor A–J
+ 增加对应private tests / audit fixtures
+ 运行冻结合同的PTDS矩阵、旧consumer与四格falsifiers
+ 形成独立implementation candidate
```

它不允许：

```text
修改Fact/Relation/Coverage Schema、reason order或terminal truth
修改existing Provider assignment / qualification / admission
让normal与negative route拥有两个consume slot或失败后fallback
恢复或消费旧global composition authorization
选择或实现manifest successor / same-attempt Evidence continuity
选择persistence
启动public Review、post-R1 Benchmark或R2–R6
发布tag / Release
```

`ALLOWED`不等于`IMPLEMENTED`、`EXACT_MAIN_VERIFIED`、`READBACK_QUALIFIED`或`FROZEN`。runtime patch必须拥有新的source、
branch、candidate head/tree、原始PR门、protected merge、exact-main双门、fresh installed-product readback与independent
reconciliation；真实反例出现时停止当前施工，只重开被击穿的最小边界。

## 5. implementation stop conditions

后继施工出现以下任一条件时，必须保留反例并停止：

1. complete terminal branch必须由requester、Relation candidate或Coverage candidate选择；
2. normal/negative route需要两个独立claim slot、失败后fallback或copy-equal successor；
3. new domain只能alias `LEGACY`或`RELATION_TRANSITION`才能工作；
4. Relation claimed-source adapter无法保留完整Policy/Fact truth或必须弱化existing transition；
5. exact-input route必须改变0.2 identity、carrier truth、negative producer、validator或admission oracle；
6. selector与任一downstream只能共享同一个关键branch/denominator projector；
7. bounded patch必须扩大public Schema、exports、manifest、Evidence、persistence或global composition authority；
8. deadline、stop、revocation、same-attempt binding或resource closure不能在claim前机械证明。

授权已经生效也不能成为修改oracle、扩大scope或静默reopen frozen contract的理由。

## 6. 本publication自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/345-r1-post-terminal-fact-dual-successor-private-implementation-authorization-successor-publication.md
docs/milestones.md
```

doc340–342、doc344、runtime、tests、workflows、fixtures、Fact/Relation/Coverage Schema、manifest、Evidence、persistence与
public产品必须保持`a1899bc…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、
required markers、`git diff --check`、read-only global/local hygiene、doc342/doc344 full-file SHA、#394与#396原始/exact-main双门、
四份maintenance formal PASS、全部retained non-success、两份independent reconciliation与finite closeout/integrity、primary
`audit.json` continuity。focused matrix与read-only feasibility audit必须从当前base fresh复算；它们只作witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc342 / doc344 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用#395失败
candidate的内容、#396 maintenance green、相同semantic digest或后继PASS替代本文任何一门。

## 7. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_395_FAILED_CLOSED_UNMERGED_NOT_QUALIFIED
R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_SUCCESSOR_0_2_PUBLICATION_CANDIDATE
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只把`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`变成当前事实，同时保持
`...PRIVATE_IMPLEMENTATION_NOT_STARTED`。随后必须返回CONTROL LOOP，才允许在本文ceiling内开始新的private implementation
candidate；不得把authority publication本身、#395失败world或#396 maintenance算作runtime证据。
