# R1 post-terminal Fact dual-successor 私有实现授权发布候选

日期：2026-11-04

> 状态：`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE`。
>
> 构造坐标：`main@2e9e5fbb56c84152de6a90be535345666becb733`，tree
> `be764de0a27d1b61cc1f0d51f14a29ad3894ce58`。
>
> 上游：[0.1合同](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)、
> [合同独立冻结发布](341-r1-post-terminal-fact-dual-successor-authority-recovery-contract-freeze-publication.md)与
> [private implementation feasibility audit](342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md)。
>
> 影响：`L0_DOCUMENTATION / AUTHORITY_PUBLICATION_ONLY`。本文只发布一份条件化的bounded private implementation
> authority；不修改runtime、tests、workflows、fixtures、Fact/Relation/Coverage Schema、manifest、Evidence、persistence或
> public Review。本文自己的完整资格链闭合以前，`ALLOWED`不生效。

## 1. publication输入已经取得资格

文档342由PR #394以
`base=99244df24360787b5f1b97a1cad89dc26d8aefe0 / head=3abf3afc56f9e00622e34f9e320ae16ae2f75d47 /
tree=be764de0a27d1b61cc1f0d51f14a29ad3894ce58`受保护合入本构造基线。三个公开门均使用原始attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #394 original Public CI | `40848292961` | 1 | 11/11 SUCCESS |
| exact-main Public CI | `40853811383` | 1 | 11/11 SUCCESS |
| exact-main Browser Smoke | `40853811154` | 1 | 1/1 SUCCESS |

fresh anonymous installed-product README、doc341、doc342与milestones各有唯一`FORMAL_READBACK_PASS`。independent
reconciliation、173-artifact finite closeout、保留的stdout self-capture mismatch与finite integrity分别为：

```text
94acea18208b363fef7ac23bc19fa3a39c43bc72347a2a41729beb0dd11d909c
87c64f49bb9bc2b086327ae68b4fb66a9d4267bd0a6d239f3e9b055c3e473d49
4087bc023c8a58e0a0b511a4cf304b30bffa9500a9b837abd99530045bada35c
f31e6ebab9f34522eee7b43717d1daf801bd531cb9fc2aa069ca901b797f5bd4
```

doc342 full-file SHA-256与exact-main dual-gate seal分别为：

```text
4ce3bc53842dc36052869ce38d550668219acedeec6b7e66ffd39009d225df75
b8e6d7a6361cf1d506121928e6eac47c62f992355aeef2b90639804e5192d418
```

因此doc342现在是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。合同保持`FROZEN`；runtime implementation在本文最后门
闭合以前仍是`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 保留的non-success不被授权发布重解释

以下身份继续按原样保留：

- feasibility candidate阶段的managed-worktree `sourceRoot`、embedded dataclass module registration与首次local-validation
  result-shape setup errors；它们的effect均为`NONE`；
- fresh readback首次anonymous rate diagnostic与API preflight记录`remaining 0`，preflight为`403`；它们不是readback PASS；
- reset后continuity check attempt 1选错setup-history文件名，attempt 2又选错source字段并生成不可用的property count；两项均为
  `POST_RESET_CONTINUITY_CHECK_SETUP_ERROR / NON_QUALIFYING / NONE`；
- anonymous rate diagnostic #2观察到`58/60`，但紧随的API preflight #2仍从另一个匿名配额视图收到`403 / remaining 0`；两个观察面
  没有被拼成一个可用world；
- 较晚reset后diagnostic #3与preflight #3才证明当前匿名窗口可用；后继四份formal PASS不回填任何先前non-success；
- finite closeout只对173项冻结索引负责；stdout自捕获项按独立mismatch identity保留，不能声明为逐字节自洽。

这些事实只证明proof facility在保留旧身份的前提下继续完成了新资格链，不扩大runtime authority，也不解释匿名配额视图的单一根因。

## 3. 授权对象是bounded A–J

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

class、method、field、lock与retention布局仍由实现候选决定。可以复用既有canonical serializer、frozen enum、terminal source revalidation与
one-shot primitive；不得让selector与任一downstream producer共享被测试的关键branch projector。

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
branch、candidate head/tree、原始PR门、protected merge、exact-main双门、fresh installed-product readback与independent reconciliation；
真实反例出现时停止当前施工，只重开被击穿的最小边界。

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
docs/343-r1-post-terminal-fact-dual-successor-private-implementation-authorization-publication.md
docs/milestones.md
```

doc340–342、runtime、tests、workflows、fixtures、Fact/Relation/Coverage Schema、manifest、Evidence、persistence与public产品必须保持
`2e9e5fb…` base bytes。local gates至少复算四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、
`git diff --check`、read-only global/local hygiene、doc342 full-file SHA、#394 original/exact-main双门、四份formal identity、全部retained
non-success、independent reconciliation、finite closeout与integrity、primary `audit.json` continuity。focused matrix与read-only feasibility
audit必须从当前base fresh复算；它们只作witness，不冒充授权生效。

```text
publication final bytes / declared local gates
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc342 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> PRIVATE_IMPLEMENTATION_ALLOWED becomes effective
    -> return CONTROL LOOP
```

每个required target必须有唯一qualifying PASS；formal non-success与setup/diagnostic history从实际记录机械枚举。不得用本publication的
original PR green、相同tree、相同semantic digest或后继PASS替代任何一门。

## 7. 当前publication target与停止线

全部门闭合以前只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PUBLICATION_CANDIDATE
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
candidate；不得把authority publication本身算作runtime证据。
