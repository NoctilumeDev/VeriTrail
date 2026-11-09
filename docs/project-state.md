# VeriTrail 当前项目状态公开投影

> 本页是bounded current-state阅读投影，不是事实权威、状态机、roadmap scheduler、qualification record或施工授权。
> 完整append-only工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始PR attempt、exact-main gates、Artifact、
> fresh installed-product readback与independent reconciliation继续拥有各自事实。

## 投影身份

```text
projection_contract: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8
projection_status_rule: IF_DOC391_ALL_CANDIDATE_GATES_CLOSED_THEN_QUALIFIED_CANDIDATE_NOT_FROZEN_ELSE_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
freeze_publication_candidate: NOT_CREATED_NOT_AUTHORIZED
construction_exact_base: f2ab7b78f86a057431cf5c8f4cbc3b0337338118
construction_tree: 280cbc4f54427b86b81854892af8a490559fed7d
source_binding_kind: FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes: 682147
source_milestones_sha256: 2746732b39f502e1e4b0d9bd3b8c97b3dccadaade15bc31b302058f83dd270fc
source_milestones_blob_sha1: 123e0736ceb4f44c738b3c5dba92863eca5c4149
upstream_private_implementation_freeze_closeout_sha256: 2bc7ef165aebb24d4a9dc329ab99da5316256828cf4d1a94c571a59b072f420a
```

这些坐标和摘要只声明本publication candidate由哪组不可变输入起草。milestones不保存自己的摘要，因而没有自引用；
`projection_status_rule`不是自我认证：只有doc391声明的local qualification、original PR、protected merge、new exact-main双门、
fresh installed-product readback、independent reconciliation与finite closeout全部成立，`QUALIFIED_CANDIDATE / NOT_FROZEN`分支才由
外部证据生效。本文不能给自己升级状态；独立freeze publication尚未创建或授权。

## 当前有效事实

- PR #428已经使projection/contract 0.7完成独立freeze publication全部最后门；0.7继续是`FROZEN HISTORICAL`，
  其exact bytes、source binding与readback identity不被0.8改写；
- PR #429/doc377证明共同application-level output admission当时不存在，但其fresh milestones Render正确返回
  `PARTIAL / CONTENT_TRUNCATED`，所以doc377保持`READBACK_NOT_QUALIFIED / NOT_QUALIFIED_HISTORY`；
- PR #430/doc378只资格化readback-target correction，PR #431/doc379又从新exact main独立完成current-state audit successor；
- PR #432/doc380与PR #433/doc381分别完成application-level unified Review / Coverage output admission合同candidate及独立
  freeze publication，因此`R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_CONTRACT_FROZEN`已经生效；
- PR #434/doc382完成private implementation feasibility audit，PR #435/doc383完成bounded A–J implementation authority publication，
  因此`PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED / QUALIFIED_HISTORY`与`PRIVATE_IMPLEMENTATION_ALLOWED`已经成立；
- 首次implementation PR #436 original gate在两个Release资产下载路径持续HTTP 504后失败，已关闭且未合并；candidate regression、
  Subject failure与底层网络根因均未建立；
- PR #437/doc385虽通过original门并合入，但exact-main Public CI在Core 0.12.2 wheel下载连续三次15秒`TimeoutError`后fail closed，
  因此doc385保持`MERGED / NOT_QUALIFIED`；PR #438/doc386只使该exact-main failure boundary成为qualified history；
- PR #439合入实现successor后，exact-main Public CI在Python 3.10耗尽35分钟outer containment而`CANCELLED`；PR #440的首次
  35→45分钟maintenance又在Starter观察面真实`FAILURE`并关闭未合并；PR #441只资格化独立45分钟maintenance successor；
- PR #442/doc388以自己的完整链重新资格化不变的implementation bytes，使其成为
  `IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`；
- PR #443/doc389的original门与Browser成功，但exact-main Public CI在Python 3.10耗尽45分钟outer containment而`CANCELLED`；
  产品assertion failure、semantic regression与Subject failure均未建立，lower cause保持`UNKNOWN`，doc389不被后继PASS回填；
- PR #445只把aggregate outer timeout从45提高到55分钟，并以自己的完整链取得CI containment maintenance资格；它不拥有或传递
  semantic freeze authority；
- PR #446/doc390从maintenance后的新exact main重建完整freeze qualification：original/exact-main Public CI与Browser Smoke均attempt 1
  SUCCESS，fresh README/doc389/doc390各唯一formal PASS，AGENTS/milestones各唯一raw/API/Git全字节一致，independent
  reconciliation与144-artifact finite closeout成立；因此
  `R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN`已经生效；
- `R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED`；Review derivation manifest negative-world successor、
  same-attempt derivation Evidence continuity、language-support qualification persistence与public Review产品继续
  `NOT_STARTED / NOT_AUTHORIZED / OPEN`，R2–R6继续未启动；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY`；
- `R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY`；
- `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED`；
- PR #398 private implementation已经合入，original/exact-main双门成立；旧milestones Render正确返回
  `PARTIAL / CONTENT_TRUNCATED`，该旧readback world仍保持`READBACK_NOT_QUALIFIED`；
- PR #399 original Public CI真实失败，未rerun、已关闭且未合并，lower resource cause保持`UNKNOWN`；
- PR #400–#414的公开投影failure-boundary、证明设施修正、维护与恢复publication均按各自exact world保留；后继PASS不回填旧失败；
- PR #415使projection 0.3成为qualified candidate，PR #416又完成独立freeze publication，因此
  `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN`已经生效；
- PR #417/doc365完成local、original PR、protected merge、exact-main双门、fresh六目标formal、两项raw-byte observation、
  independent reconciliation与finite closeout；因此#398/doc346现在是
  `IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED`；
- #417第一个fresh root的README formal发生anonymous API budget exhaustion，第二个fresh root发生reader-visible marker target
  selection failure；两次Core Verdict均未创建，后继PASS不覆盖它们，底层原因保持`UNKNOWN`；
- PR #418/doc366的0.4 candidate已合入，但exact-main Public CI attempt 1真实失败且没有rerun；doc366与projection 0.4继续
  `MERGED / NOT_QUALIFIED / NOT_FROZEN`，decisive assertion与lower cause保持`UNKNOWN`；
- PR #419/doc367自己的original/exact-main双门通过，但fresh milestones Render正确返回`PARTIAL / CONTENT_TRUNCATED`；
  doc367保持`READBACK_NOT_QUALIFIED / NOT_QUALIFIED_HISTORY`，它的target regression不被README/doc367 PASS覆盖；
- PR #420/doc368完成local、original PR、protected merge、exact-main双门、fresh bounded Render、完整raw-byte observation、
  independent reconciliation与finite closeout，因此doc368成为dual failure-boundary qualified history；
- PR #421/doc369完成0.5 candidate完整资格链，PR #422/doc370完成独立freeze publication，因此
  `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN`已生效；
- PR #423/doc371完成local、original PR、protected merge、exact-main双门与fresh qualification。第一个fresh root的README
  marker在rendered text中出现零次，唯一formal以proof-target selection error停止且没有Core Verdict；第二个fresh root的六个
  Render formal与两项raw-byte observation全部独立通过。因此固定private `POST_TERMINAL_DUAL_SUCCESSOR_0_1` implementation
  现在是`FROZEN`，首个formal错误与lower cause `UNKNOWN`继续保留；
- PR #424/doc372的自动门、fresh marker readback与reconciliation曾记录0.6为qualified candidate；PR #425的README readback
  反例使doc373保持未资格化，PR #426又在任何产品observation前证明本页自身仍保留0.6的旧未资格化状态；因此0.6的semantic
  qualification已重开且从未冻结，#424–#426全部exact identity继续保留；
- PR #427曾使[文档375](375-r1-public-project-state-projection-successor-0.7-contract.md)与projection 0.7成为
  `QUALIFIED_CANDIDATE / NOT_FROZEN`；PR #428又使独立[文档376](376-r1-public-project-state-projection-0.7-freeze-publication.md)
  完成全部最后门，因此0.7现在只承担frozen historical身份；projection 0.5承担更早的冻结历史身份，0.4承担failed/not-qualified
  历史身份，0.6承担semantic qualification reopened历史身份；
- Review derivation manifest negative-world successor、same-attempt derivation Evidence continuity、language-support persistence与
  public Review产品继续`NOT_STARTED / NOT_AUTHORIZED / OPEN`；R2–R6继续未启动。

## 必须继续可见的failure boundary

### #443 / #445 / #446 实现冻结资格恢复链

#443/doc389的original Public CI `42538047126`为11/11 SUCCESS，Browser Smoke `42542428407`为1/1 SUCCESS；
exact-main Public CI `42542428301` attempt 1却在required Python 3.10耗尽45分钟outer containment后`CANCELLED`。取消前
Core、GitHub Evidence、Review Attention normal/optimized均成功，Starter/Authoring亦已发出PASS结果；但产品assertion failure、
candidate semantic regression与Subject failure均未建立，lower resource cause保持`UNKNOWN`。readback没有启动，doc389继续
`MERGED / NOT_QUALIFIED / NOT_FROZEN`。

#445只把aggregate outer timeout从45提高到55分钟；original/exact-main Public CI与Browser Smoke均成功，fresh workflow raw-byte
readback、independent reconciliation与finite closeout成立。因此只有CI containment maintenance取得资格，不能把#443回填成PASS，也
不能把maintenance资格继承为semantic freeze。

#446/doc390在新exact main重新取得本层local witness、original PR、protected merge、exact-main双门、fresh README/doc389/doc390
formal、raw AGENTS/milestones、independent reconciliation与finite closeout。它使固定private implementation在`f2ab7b78…`world内
成为`FROZEN`，同时保持#443 `CANCELLED`、`UNKNOWN`与doc389 not-qualified原identity。runner freeze-reference、reconciliation
formal-kind mismatch及其他setup errors继续保留，后继proof facility没有重复formal PASS。

### #436 / #437 / #439 / #440 实现与地基失败

#436 original Public CI在E3 multi-asset与Python 3.13 Core 0.12.2下载路径持续收到HTTP 504并耗尽有限恢复预算；PR已关闭未合并，
没有rerun。#437的original门成功并合入，但exact-main Public CI又在Python 3.10下载同一冻结wheel时连续三次15秒`TimeoutError`后
fail closed；doc385因此`MERGED / NOT_QUALIFIED`。#438只把第二个failure boundary资格化为历史，不回填前两者。

#439合入机械重建的successor implementation后，exact-main Public CI耗尽35分钟outer containment而`CANCELLED`；#440第一次
35→45分钟maintenance又在Starter观察面真实`FAILURE`并关闭未合并。#441只证明自己的45分钟maintenance world，#442只重新资格化
不变implementation bytes。candidate regression、Subject failure与lower resource cause没有由这些后继PASS反向建立。

### #429 current-state audit readback target failure

#429/doc377的original/exact-main双门与README/doc377 formal成功，但milestones唯一diagnostic观察到600693 UTF-8 rendered-text
bytes，超过frozen 524288-byte上限76405 bytes，正确终结为`PARTIAL / CONTENT_TRUNCATED`；formal未运行。被击穿的是把已知
超界完整milestones注册为Render target的proof seam，不是P2 oracle或doc377 semantic conclusion。#430只资格化target correction，
#431又从新exact main独立重跑current-state audit；它们不回填doc377。

### #425 / #426 公开状态语义矛盾

#425 exact-main的README diagnostic为`COMPLETE / HTTP 200`，但预注册reader-visible phrase出现零次；exact source inspection随后证明
README主状态仍把0.6写成未资格化，与#424/doc372的qualified-candidate记录冲突。#425 formal、其他target observation、raw formal与
Core Verdict均未开始，doc373保持`MERGED / NOT_QUALIFIED / NOT_EFFECTIVE`。

#426只修正README并version freeze-publication responsibility。它的original Public CI `42340071297`、exact-main Public CI
`42342585325`与Browser Smoke `42342585323`均attempt 1 SUCCESS（11/11、11/11、1/1），但fresh exact-main pre-observation
source validation又发现本页第11行仍是`CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`，第53行仍称0.6“尚未资格化或冻结”。所以
#426没有运行任何installed-product diagnostic、formal、raw formal或Core Verdict，doc374保持
`MERGED / EXACT_MAIN_DUAL_GATES_PASS / READBACK_NOT_QUALIFIED / NOT_EFFECTIVE`。后继0.7不能回填这两个失败world。

### #398 / #399入口失败

#398 milestones diagnostic观察到526260 UTF-8 bytes，超过frozen 524288-byte Public Render上限1972 bytes，故coverage为
`PARTIAL / CONTENT_TRUNCATED`；#399 required Python 3.13 fixture `git cat-file`在剩余acquisition budget内超时并正确映射
`SAFETY_BUDGET_EXHAUSTED`。两者不是同一world，也不能由#417 PASS覆盖。

### #401–#414公开投影恢复链

#401 marker drift、#402 Evidence持久化`FileNotFoundError`、#404 cancellation、#405 marker drift、#406/#410 anonymous API
exhaustion与#407/#408 HTTP 504预算耗尽继续保留各自run/head/job/target identity。后继failure-boundary audit、release-download
maintenance与recovery publication只证明自己的exact world，不重写首败或`UNKNOWN`。

### #417读回资格恢复的两个non-success world

第一次fresh root中README formal的anonymous API首个repository probe为`403 / COLLECTION_BUDGET_EXHAUSTED / remaining=0`，
Render仍`COMPLETE / 200`，Core Verdict未创建。第二次fresh root中API/Render均`COMPLETE / 200`，但选择的旧README
marker在source中一次、rendered text中零次，产品以`Render Evidence marker drifted`停止；这是readback target selection defect，
不是subject或candidate regression。第三个fresh root使用新的reader-visible marker取得独立PASS，不删除、不解释前两次失败。

### #418 exact-main gate failure

PR #418 original Public CI为11/11 SUCCESS，protected merge后的Browser Smoke为1/1 SUCCESS，但exact-main Public CI
`42211661846` attempt 1在required Python 3.10 test
`test_staging_failure_creates_public_error_bundle_after_reverse_cleanup`真实失败且没有rerun。产品已观察到
`EVIDENCE_STAGING_FAILED`、`EVIDENCE_ERROR / ERROR`与cleanup complete；public verdict为`FAIL`而不是test预期的`PENDING`。
failed output没有保留decisive assertion或临时Bundle，所以精确assertion为`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，lower cause仍为
`UNKNOWN`。后继绿灯不回填或解释该world。

### #419 readback-target failure

第一个fresh root因Markdown反引号marker在rendered text中不存在而fail closed，Core Verdict未创建。第二个root的README/doc367
各有唯一formal PASS；milestones唯一diagnostic则观察到571604 UTF-8 bytes，超过frozen 524288-byte上限47316 bytes，正确终结为
`PARTIAL / CONTENT_TRUNCATED`，formal未运行。该反例击穿doc367的target seam，不击穿P2 oracle；不同target结果不能拼成资格。

### #420 correction audit中的non-qualifying observations

第一个fresh root在产品调用前因proof-facility生成的Plan ID超过64字符而停止，qualification effect为NONE。第二个root中anonymous
rate diagnostic/preflight #1–#3观察到`remaining=0`并按原identity保留；可用窗口恢复后，README/doc368 unique formal与
AGENTS/milestones raw/API/Git观察才各自独立完成。expected closeout stdout self-capture mismatch也以semantic effect NONE保留。
这些后继PASS只使doc368成为qualified history，不使doc366、doc367或projection 0.4资格化。

### #423 implementation freeze readback中的proof-target error

第一个fresh root的六个Render diagnostic均为`COMPLETE / HTTP 200`，但旧README marker在source中一次、rendered text中零次。
唯一formal因此以`FORMAL_READBACK_ERROR / PROOF_TARGET_SELECTION_ERROR / RENDERED_TEXT_OCCURRENCES_ZERO`停止；API/Render仍完整，
Core Verdict未创建，lower cause保持`UNKNOWN`。第二个fresh root只重开marker target boundary，在diagnostic阶段先要求marker出现一次，
再取得六个唯一formal PASS与两项raw-byte PASS。后继PASS使fixed private implementation获得自己的冻结资格，但不删除、不解释首败，
也不把证明对象从private selector漂移成完整Review产品。

## 问题连续性边界

本投影把三层问题身份机械分开：产品原问题仍是用户提出的工程问题闭环；本candidate承接的原工程问题是准确、自洽、可公开
观察的有界project-state projection；当前证明义务只覆盖0.8 candidate final bytes、source binding与跨表面一致性；适用world只覆盖
本candidate的exact base/head/tree、final bytes、attempt与fresh readback identity。上游fixed private unified Review / Coverage output
admission implementation frozen只是本投影必须准确陈述的既有事实，不是本轮被重新证明的对象。局部projection qualification成立不等于
完整Review产品已经解决产品原问题；`proof_is_not_problem_solving = true`。

## 权威边界

| 主体 | 权威 | 明确不拥有 |
| --- | --- | --- |
| Reality | 现实事实 | 被文档、测试或Verdict创造 |
| 用户/人类授权者 | 目标、验收前提与必要Seal决定 | 被Business Layer或Core替代 |
| Provider | 自己实际观察到的事实及来源 | 全局事实或裁决权 |
| R/Q/O/T | 各自合同规定的分析、观察和调度职责 | 越界扩张或共享隐性权威 |
| Business Layer | 业务流程组织、能力选择、补证请求 | 证据充分性裁决或PASS宣布 |
| Core | 证据完整性、绑定、充分性及确定性裁决 | 现实事实的超级所有权 |
| `docs/milestones.md` | 完整append-only工程历史、链接与provenance | 必须落入Public Render窗口 |
| 本页 | 当前0.8 candidate world的有界公开阅读投影 | source of truth、scheduler、qualification或施工授权 |

验迹内部可以有很多插件、Provider、分析器和调度器，但最终优化目标始终是用户提出的工程问题，而不是插件自身的存在价值。

## 本页不能做什么

本页不能：

- 替代、裁剪、重写或删除`docs/milestones.md`；
- 把短投影冒充完整历史已经被Public Render观察；
- 修改P2 oracle、Collector coverage或Core充分性规则；
- 把任何旧FAIL/ERROR/CANCELLED/UNKNOWN升级为PASS；
- 决定证据充分性、qualification、state transition或下一合法seam；
- 把已经冻结的fixed private implementation扩张解释为完整Review产品、恢复global composition authority，或启动manifest、
  Evidence、persistence、public Review、R2–R6。

## 本candidate的生效条件

PR #446已经使fixed private unified Review / Coverage output admission implementation在自己的exact world内成为`FROZEN`；
independent reconciliation与144-artifact finite closeout SHA-256分别为
`b0da3502dcc11b2f6593c31fa15844b59e431930c27176d1fb1a378b3d39593e`与
`2bc7ef165aebb24d4a9dc329ab99da5316256828cf4d1a94c571a59b072f420a`。这些是0.8必须准确陈述的上游事实，
不是0.8自己的qualification。

只有[successor 0.8 contract](391-r1-public-project-state-projection-successor-0.8-contract.md)自己的local qualification、original PR
gates、protected exact-head merge、新exact-main Public CI与Browser Smoke、fresh anonymous installed-product README/本页/doc376/doc389/
doc390/doc391 Public Render、AGENTS/milestones public+API raw-byte observations、final milestones binding复算、independent reconciliation与
finite closeout全部成立后，`projection_status_rule`的`QUALIFIED_CANDIDATE / NOT_FROZEN`分支才生效。此前状态严格是
`CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`。独立freeze publication尚未创建；本页不是scheduler。
