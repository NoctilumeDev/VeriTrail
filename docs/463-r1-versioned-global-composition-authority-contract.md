# R1 versioned global composition authority contract

日期：2026-11-28

> 当前候选状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
> 本文自己的完整资格链闭合以前，本文内容不是冻结合同，也不授权任何runtime施工。
>
> 合同基线：`main@49a07ed029c15c5312a29aa0ef5f194ae3252489`，tree
> `7d8ba538886abfa4fe7d326bbbfd9bd634a61b64`。
>
> 上游：[Manifest 0.2 private implementation冻结发布](461-r1-review-derivation-manifest-0-2-private-implementation-freeze-publication.md)与
> [global composition authority当前状态审计](462-r1-global-composition-authority-current-state-audit.md)。
>
> 影响：`L0_DOCUMENTATION / VERSIONED_PRIVATE_AUTHORITY_CONTRACT_ONLY`。本文不创建runtime、Schema、fixture、test、workflow、
> public export、CLI、publisher、durable persistence、Core Verdict、HumanDisposition或公开Review产品。

## 1. CONTROL LOOP恢复与审计资格

PR #527把doc462精确合入：

```text
base                 = f0d7651ff1f03330a5d058c3ea2fa535369c5c36
head                 = 065976a3ba99ec27929fa8b8d427c2f193ceb2c7
candidate/merge tree = 7d8ba538886abfa4fe7d326bbbfd9bd634a61b64
ordinary merge       = 49a07ed029c15c5312a29aa0ef5f194ae3252489
diff                 = 1 commit / 4 files
```

三个远端门均只认original attempt：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #527 original Public CI | `46041949597` | 1 | 15/15 SUCCESS |
| exact-main Public CI | `46048835183` | 1 | 15/15 SUCCESS |
| exact-main Browser Smoke | `46048835207` | 1 | 1/1 SUCCESS |

fresh installed-product world只认`49a07ed...`。README formal #1因匿名API rate exhaustion得到
`FORMAL_READBACK_ERROR / API ERROR / Render COMPLETE / Core Verdict null`，底层出口桶差异原因保持`UNKNOWN`；reset后README formal #2
才是唯一qualifying PASS。doc461/doc462 Render与AGENTS/milestones raw-byte observation各有唯一qualifying PASS。independent
reconciliation、135-artifact finite closeout与post-closeout integrity SHA-256依次为：

```text
37c99d9ac3ec39443a4dedb2c29c2d8a266f356244c32fcaf449307a9b9ecdcb
2ef552b24dd06288d36ad56cc2169bd22663c8603445a3b5832708595996dd75
f0c8d69453c11d5770f8fdccae5055f8028b928e77b99bcab4bef6b28739d3c6
```

因此doc462现在是`CURRENT_STATE_AUDITED / QUALIFIED_HISTORY`。其finding没有被资格链改变：当前private组件可以机械组合，但没有
production owner、public export/CLI/publisher或global composition authority。本文从这个新exact main重新进入CONTROL LOOP，只冻结
下一层versioned private authority，不把“可机械组合”偷换成“应用已经存在”。

## 2. 合同identity与版本停止线

本合同冻结以下语义identity；后继实现可以选择私有Python名称，但不得更改或别名化这些identity：

```text
authority contract
  R1_GLOBAL_REVIEW_COMPOSITION_AUTHORITY_0_1

unique owner identity
  veritrail.review.global-composition-owner/0.1

attempt binding function
  r1-global-review-attempt-binding/0.1

composition function
  r1-global-review-composition/0.1

independent admission function
  r1-global-review-composition-admission/0.1

private admitted result identity
  veritrail.review.global-composition-result/0.1
```

字符串相同、digest相同、subclass、duck typing、legacy wrapper、反序列化副本或另一个live object都不能冒充这些owner identity。改变Provider
roster denominator、world partition、调用顺序、failure propagation、cleanup obligation、Core边界、private result shape或public停止线时，必须
显式version bump；不能静默修改0.1。

## 3. 唯一owner与authority ceiling

规范authority划分如下：

| owner | 可以决定 | 不得决定 |
| --- | --- | --- |
| Reality | 现实发生了什么 | 软件是否已经获得充分证据 |
| 用户 / 人类Seal authority | 目标、验收前提与需要人作出的Seal决定 | 伪造Provider观察或跳过冻结门 |
| Provider | 自己实际观察到的事实、来源与运行状态 | Core Verdict、全局充分性或其他Provider事实 |
| sealed Policy / Profile | 适用能力、Provider roster与冻结证明义务 | 在执行期自行扩张或缩小denominator |
| 各local stage owner | 自己合同内的claim、validation、admission与one-shot lifecycle | 全局attempt、其他stage truth或Core Verdict |
| global composition owner | 建立一个live attempt、机械选择冻结能力、安排同world顺序、传播失败并提交private result admission | 改变sealed obligation、把部分结果写成成功、宣布证据充分或产生Verdict |
| Manifest / carrier | copy-owned exact byte handoff与role/path/digest transport | truth、sufficiency、事实解释或Verdict |
| Core | sealed Plan/session的binding、integrity、sufficiency、determinacy与Verdict | 取得Reality/Provider的事实观察authority |
| HumanDisposition authority | 对机器Proposal作出身份确认的人类处置 | 把机器Attention Proposal冒充已确认缺陷 |

global composition owner是应用级证明装配者，不是现实事实超级owner，也不是新的隐性裁决器。它可以停止重复采集、并行独立任务或请求补充
条件，但这些动作只在sealed Policy/Profile允许的运行空间内发生；是否已经满足证明义务仍只由Core依据sealed合同裁决。

## 4. exact frozen input denominator

每个合法composition attempt必须在开始前机械绑定：

1. exact `DerivationInputSet` live object、canonical bytes、SourceSnapshot、ReviewPolicy、DerivationProfile与既有digest；
2. 一个新鲜、未消费的live `BudgetContext`、绝对monotonic deadline、stop/eligibility state与cleanup obligation；
3. 由sealed Policy/Profile机械派生的完整Provider roster、固定版本identity与适用性；caller不能删减、追加或替换Provider；
4. 当前冻结的Fact fulfillment、post-terminal dual successor、Fact→Relation transition、Relation→Slice/Coverage composition、unified
   application admission、same-attempt continuity、manifest carrier successor与Manifest 0.2 private implementation identity；
5. 同一attempt的controller capture slot、route claim、application admission、continuity、carrier admission与Manifest staging opportunity；
6. `normal`与qualified negative world共同的failure propagation、resource ownership与cleanup规则。

owner只能消费上述exact private successor identity。legacy/default/public入口、旧Manifest 0.1 producer、legacy Evidence 0.2 projector、fixture-only
compatibility world、另一个attempt的admission或path reread均不在denominator内。Provider discovery、网络下载、动态插件安装或运行期扩张roster不属于
0.1。

## 5. 八个live worlds与规范顺序

本合同只承认八个已经由上游冻结的live worlds：

| world | route | admitted application result |
| --- | --- | --- |
| `NORMAL_CONSISTENT` | `RELATION_HANDOFF` | Fact + Relation + ReviewSlice + Coverage |
| `NORMAL_BRANCH_EMPTY` | `RELATION_HANDOFF` | Fact + Relation + empty admitted ReviewSliceSet + Coverage |
| `NORMAL_SLICE_PARTIAL` | `RELATION_HANDOFF` | Fact + Relation + partial admitted ReviewSliceSet + Coverage |
| `NORMAL_RELATION_CONFLICT` | `RELATION_HANDOFF` | Fact + Relation + qualified-unknown Slice root + Coverage |
| `ZERO_PARSE_DENOMINATOR` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | qualified negative Coverage |
| `ALL_PARSE_REJECTED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | qualified negative Coverage |
| `PROJECTION_BLOCKED` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | qualified negative Coverage |
| `REQUIRED_PROVIDER_NON_SUCCESS` | `FACT_TO_COVERAGE_EXACT_INPUT_SUCCESSOR_0_2` | qualified negative Coverage |

每个attempt必须沿同一live object graph按以下顺序推进：

```text
bind exact inputs / roster / live BudgetContext / capture slot
  -> run complete Fact denominator and establish complete terminal Fact source
  -> consume the unique post-terminal route claim
  -> normal corrected transition and Slice/Coverage composition
       OR qualified negative Coverage successor
  -> exact application-level unified output admission
  -> same-attempt continuity reconciliation and commit
  -> manifest carrier projection / independent conformance / admission
  -> Manifest 0.2 candidate / independent conformance / admission / private staging
  -> independent global composition admission
  -> one private admitted global composition result
  -> owned cleanup and terminal lifecycle closure
```

四个qualified negative worlds是完整、成功的composition结果，不是runtime failure，也不得制造Fact/Relation/Slice placeholder。任何unsafe、
interrupted、revoked、incomplete、budget-exhausted或cleanup-failed attempt都不能借negative vocabulary取得admission。normal conflict不能被重分类为
negative；branch-empty与partial Slice仍有actual admitted bytes。

## 6. failure propagation与resource closure

owner必须fail closed并保留最早可归层reason。任何stage non-success都必须：

1. 停止尚未开始的后继stage；
2. 不生成缺失stage的placeholder、空文档、假digest或成功receipt；
3. 保留已发生的Provider/stage observation与原始failure identity；
4. 触发owned resource cleanup，并把cleanup结果纳入terminal lifecycle；
5. 禁止从equal bytes、copy、retry wrapper、另一个context或另一个attempt恢复已消费机会；
6. cleanup失败时拒绝global admission，即使此前所有semantic stage都已PASS。

0.1至少必须机械区分以下failure families：

```text
GLOBAL_COMPOSITION_VERSION_REJECTED
GLOBAL_COMPOSITION_INPUT_BINDING_REJECTED
GLOBAL_COMPOSITION_PROVIDER_ROSTER_REJECTED
GLOBAL_COMPOSITION_WORLD_SPLICE_REJECTED
GLOBAL_COMPOSITION_PARTIAL_RESULT_REJECTED
GLOBAL_COMPOSITION_LATE_MUTATION_REJECTED
GLOBAL_COMPOSITION_FOREIGN_CONTEXT_REJECTED
GLOBAL_COMPOSITION_COMPONENT_VERSION_REJECTED
GLOBAL_COMPOSITION_RESOURCE_CLEANUP_FAILED
GLOBAL_COMPOSITION_REPLAY_REJECTED
GLOBAL_COMPOSITION_ADMISSION_REJECTED
```

reason family只解释composition层拒绝，不覆盖或重命名下游原始reason。底层原因未知时必须继续是`UNKNOWN`。

## 7. private result、Manifest与persistence停止线

independent global admission只能签发一个不可公开构造、不可复制、不可pickle/JSON恢复、one-shot的private admitted result。它必须copy-own或
绑定以下已admit identity：

1. authority/owner/function/version identity与attempt binding；
2. exact input、Policy/Profile、Provider roster与live BudgetContext identity；
3. terminal branch、route、application admission与same-attempt continuity identity；
4. CoverageLedger 0.3 root-chain digest、root topology与actual child presence；
5. carrier admission、Manifest 0.2 admission、private staging receipt、raw digest与semantic digest；
6. terminal resource cleanup outcome。

该private result不是public Artifact、Evidence、Manifest替代品或Core Verdict。0.1只允许消费既有Manifest 0.2 private staging；不新增durable
persistence route，不写用户目录、数据库、Catalog、Run Bundle或网络服务。Manifest仍只运输role/path/digest，不解释事实或充分性。未来若要把
结果公开、持久化或送入Core产品路径，必须另开合同并重新资格化。

## 8. independent admission与直接falsifier

后继实现必须让independent admission不调用producer的expected-result projector，并从copy-owned exact material独立复算：

1. authority、owner、function与component版本dispatch；
2. exact input/roster/context/attempt binding；
3. terminal branch、route、world与actual child topology；
4. unified application admission、continuity、carrier、Manifest 0.2与staging identity；
5. raw/semantic digest、Coverage root chain与Manifest role/path/size一致性；
6. one-shot state、late mutation、resource cleanup与terminal closure。

至少必须有以下直接反例：composition replay、并发双消费、normal/negative cross-world splice、另一个attempt的admission、foreign
`BudgetContext`、roster删减/追加、partial stage success、candidate/admitted object late mutation、unknown component version、Manifest staging
replay与cleanup failure。每个反例在Python普通与`-O`下都必须由产品检查fail closed，不能依赖`assert`。

## 9. public Review与Core硬停止线

即使本合同未来冻结并实现，以下事实仍保持false：

```text
public/private chain export        = false
application CLI                    = false
Manifest publisher                 = false
durable persistence                = false
Core Verdict integration           = false
public Review product              = false
HumanDisposition automation        = false
R2-R6                              = false
post-R1 whole-project review       = false
```

后继private implementation不得修改`veritrail_review.__init__`公开面、`[project.scripts]`、现有SourceSnapshot publisher、Core evaluator、
Workbench、Route、Schema资源、Release或tag。它也不得以“业务编排”名义缩小sealed denominator、改变Core证明义务或把Attention Proposal写成
confirmed defect。

## 10. 后继private implementation最小边界

只有本文经过自己的完整资格链并由独立docs-only freeze publication发布为`CONTRACT_FROZEN`后，CONTROL LOOP才可审计private
implementation feasibility。即使可行性成立，仍需独立authorization publication；不得从合同冻结直接施工。

未来bounded implementation最多允许：

1. 一个私有versioned global composition owner/binding/admission/result模块；
2. 只导入当前冻结private successor，不修改其语义或公开面；
3. exact八world正向矩阵、上述直接falsifier与resource lifecycle测试；
4. Python 3.10.6 / 3.13.13 × normal / `-O`，并保留完整Review Attention regression；
5. private ephemeral staging，不创建public product或persistence。

若实现需要修改上游frozen identity、Core、public Schema、publisher、CLI、persistence或Provider事实语义，必须停止并只重开被击穿的最小边界。

## 11. 必须保留的non-success

后继PASS不得删除、覆盖、改名或重解释：

- doc462 audit attempt 1的normal `AssertionError`与两个`-O` false-PASS-shaped输出；
- audit attempt 2缺少cross-cell semantic projection的proof-target gap；
- PR #527 fresh README formal #1的anonymous rate exhaustion ERROR，以及preflight bucket与formal bucket不一致的`UNKNOWN`；
- PR #527 readback的worktree attachment cap、Windows wildcard、preformal capture schema与superseded facility setup failures；
- PR #519 original required failure、PR #525第一套readback topology错误及此前全部FAIL、ERROR、CANCELLED、setup failure与`UNKNOWN`。

primary `C:\Users\lenovo\Desktop\GitHubProjects\VeriTrail\audit.json`必须保持SHA-256
`4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 12. 本candidate的资格责任

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc461/462、runtime、Schema、fixture、test、
workflow、oracle、public export、CLI、publisher与primary `audit.json`必须保持base不变。

本层local gates至少重核：

1. exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings与required markers；
2. exact base/head/tree、PR #527 original/protected/exact-main gates与fresh readback continuity；
3. doc462 finding、八world、qualified-negative语义、owner/authority ceiling与当前private identity；
4. contract identity、exact denominator、one-attempt顺序、failure propagation、private result与public/Core停止线；
5. replay、cross-world splice、partial success、late mutation、foreign context、unknown version与cleanup falsifier完整性；
6. Python 3.10.6 / 3.13.13 × normal / `-O`的bounded contract/docs witness；
7. `git diff --check`、global/local hygiene与primary `audit.json` continuity；
8. original contract PR gate只认本candidate exact head/tree/attempt；
9. protected merge后只认新的merge SHA与new exact-main Public CI 15/15 + Browser Smoke 1/1；
10. fresh anonymous installed-product README/doc462/本文 Render与AGENTS/milestones raw/API/exact-Git byte observation；
11. independent source/contract/retained-failure/readback reconciliation与finite closeout。

## 13. Candidate qualification pipeline与停止线

```text
contract final bytes / declared local gates
  -> immutable pre-created PR body seal
  -> original contract PR Public CI 15/15 without metadata edit or rerun
  -> exact-head protected merge
  -> new exact-main Public CI 15/15 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / doc462 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observation
  -> independent source / contract / retained-failure / readback reconciliation
  -> finite closeout + post-closeout integrity
  -> target CONTRACT_CANDIDATE_QUALIFIED_NOT_FROZEN becomes effective
  -> return CONTROL LOOP for a separate docs-only contract freeze publication
```

本文进入仓库不等于合同资格成立。自己的完整资格链闭合以前只能记录：

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CURRENT_STATE_AUDITED_QUALIFIED_HISTORY
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后也只使本文成为`CONTRACT_CANDIDATE / QUALIFIED / NOT_FROZEN`。随后必须从新的exact main返回CONTROL LOOP，另建独立
docs-only contract freeze publication；不得直接施工runtime、公开private模块、启动public Review、R2–R6或R1后的human+AI全项目检查。
