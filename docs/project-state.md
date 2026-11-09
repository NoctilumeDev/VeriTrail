# VeriTrail 当前项目状态公开投影

> 本页是bounded current-state阅读投影，不是事实权威、状态机、roadmap scheduler、qualification record或施工授权。
> 完整append-only工程历史继续保存在[里程碑索引](milestones.md)；冻结合同、原始PR attempt、exact-main gates、Artifact、
> fresh installed-product readback与independent reconciliation继续拥有各自事实。

## 投影身份

```text
projection_contract: R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8
projection_status_rule: IF_DOC393_ALL_FREEZE_GATES_CLOSED_THEN_FROZEN_ELSE_QUALIFIED_CANDIDATE_NOT_FROZEN
freeze_publication_candidate: DOC393_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN
construction_exact_base: 69c1832a560dc24e0d4ea06f5bd2d4198518accd
construction_tree: 89be58352da8e88e3a316b0c7e85d7b5fcf64866
freeze_publication_exact_base: cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3
freeze_publication_tree: 8b38acf9b4a6a061dd655fabd68c3353d4b1c50a
source_binding_kind: FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes: 692175
source_milestones_sha256: 612c67a3d65f739921d31e0d71c23f0039503acece868d5a22897fd2e824de3e
source_milestones_blob_sha1: 856459d50516de0244730a3ffd63d6df78fb3525
upstream_private_implementation_freeze_closeout_sha256: 2bc7ef165aebb24d4a9dc329ab99da5316256828cf4d1a94c571a59b072f420a
upstream_dual_failure_audit_closeout_sha256: ef937fab434c700dca09341566727b72cab4998a4f374c5f990a5d8042244ab4
upstream_projection_0_8_candidate_closeout_sha256: a1dddaf6df487c6781a9bd55843bf3115dde338abded3013961f573b13674751
```

这些坐标和摘要只声明candidate与freeze publication分别从哪组不可变输入起草。milestones不保存自己的摘要，因而没有自引用；
`projection_status_rule`不是自我认证。doc392声明的candidate资格链已经闭合，所以本文当前最多是
`QUALIFIED_CANDIDATE / NOT_FROZEN`；只有doc393声明的local qualification、original PR、protected merge、new exact-main双门、
fresh installed-product readback、independent reconciliation与finite closeout全部成立，`FROZEN`分支才由外部证据生效。

## 当前有效事实

- PR #428已经使projection/contract 0.7完成独立freeze publication全部最后门；0.7继续是`FROZEN HISTORICAL`，其exact bytes、
  source binding与readback identity不被0.8改写；
- PR #446/doc390完成original/exact-main双门、fresh README/doc389/doc390 formal、AGENTS/milestones raw-byte observation、
  independent reconciliation与finite closeout。因此
  `R1_APPLICATION_LEVEL_UNIFIED_REVIEW_COVERAGE_OUTPUT_ADMISSION_PRIVATE_IMPLEMENTATION_FROZEN`已经生效；
- PR #443的exact-main `CANCELLED`、lower cause `UNKNOWN`与doc389 `MERGED / NOT_QUALIFIED / NOT_FROZEN`继续保留；PR #445只拥有
  CI containment maintenance资格，不向semantic freeze提供继承权；
- PR #447 projection 0.8 candidate绑定`base=f2ab7b78… / head=1e554754… / tree=521c75df…`，其original Public CI
  `42568657029` attempt 1在三个required lane的冻结Release资产delivery path耗尽恢复预算而`FAILURE`。它已关闭、未合并、未重跑，
  旧doc391与project-state bytes只属于closed PR world；
- PR #448 first failure-boundary audit绑定`head=5dd1933f… / tree=bad7b851…`，original Public CI `42576411794` attempt 1又在
  Python 3.10 E1 asset step耗尽恢复预算而`FAILURE`。它也已关闭、未合并、未重跑，旧doc392没有进入main；
- PR #449只把release-asset recovery proof facility的default absolute recovery从60提高到120秒、E1/E3 multi-asset lane从120
  提高到240秒，其他边界不变；它在`main@6dd0b761…`完成自己的完整资格链，effect仅为`MAINTENANCE_EXACT_MAIN_QUALIFIED`；
- PR #450把[文档391](391-r1-public-project-state-projection-0.8-dual-original-gate-failure-boundary-recovery-audit.md)精确合入
  `main@69c1832a560dc24e0d4ea06f5bd2d4198518accd`。original Public CI `42599405745`、exact-main Public CI
  `42604418857`与Browser Smoke `42604418779`均attempt 1 SUCCESS（11/11、11/11、1/1）；fresh README/doc391 formal、
  AGENTS/milestones raw-byte observation、independent reconciliation与finite closeout成立。因此doc391现在是
  `DUAL_ORIGINAL_GATE_FAILURE_BOUNDARY_RECOVERY_AUDITED / QUALIFIED_HISTORY`；
- #450 README formal observation 1的anonymous API budget exhaustion、reconciliation attempts 1/2的remote-main TLS EOF、
  preformal错误摘要与worktree attachment cap都按原identity保留，后继PASS不覆盖它们；
- PR #447/#448的candidate regression、Subject failure、digest mismatch、oracle defect与共享单一根因均未建立，lower cause保持
  `UNKNOWN`；#449/#450不能回填两个original failures；
- 本页与[文档392](392-r1-public-project-state-projection-successor-0.8-reconstruction-contract.md)是从新的exact base独立重建的
  0.8 candidate；旧PR #447/#448的字节、commit、attempt与资格没有被继承；
- PR #451已经把该fresh candidate精确合入`main@cae001d1dbd58fb319ddaa45e6270cbb67ffa0f3`。original Public CI
  `42619102447`、exact-main Public CI `42624859116`与Browser Smoke `42624859171`均attempt 1 SUCCESS（11/11、11/11、1/1）；
  fresh README、本文、doc376、doc390、doc391、doc392 Render与AGENTS/milestones raw-byte observation、independent reconciliation、
  187-artifact closeout及finite integrity已经使doc392/本文成为`QUALIFIED_CANDIDATE / NOT_FROZEN`；
- #451 fresh doc391 formal observation 1仍以Render `ERROR`、four coverage reasons、lower cause `UNKNOWN`与no Core Verdict永久保留；
  postprocessor `AttributeError`是独立setup error，formal observation 2的PASS不覆盖、解释或回填它们；
- [文档393](393-r1-public-project-state-projection-0.8-freeze-publication.md)只条件化发布0.8 frozen state；自己的全部最后门闭合以前，
  本页仍是`QUALIFIED_CANDIDATE / NOT_FROZEN`；
- `R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED`；Review derivation manifest negative-world successor、
  same-attempt derivation Evidence continuity、language-support qualification persistence与public Review产品继续
  `NOT_STARTED / NOT_AUTHORIZED / OPEN`；R2–R6继续未启动。

## 必须继续可见的failure boundary

### PR #447 original-gate failure

required E3、Python 3.13与Python 3.10 jobs分别在Starter 0.2.0 sdist或Core 0.12.2 wheel上记录7、5、4次HTTP 504，并耗尽
120/60/60秒旧恢复预算。Workbench成功，依赖job groups因required predecessor未全部成功而跳过。错误字节未被接受，asset digest
mismatch未观察，下载器正确fail closed。没有fresh readback或reconciliation；旧0.8 semantic bytes不具mainline或qualification身份。

### PR #448 original-gate failure

required Python 3.10 job在Starter 0.1.0 sdist上记录8个retry outcome，并由第9个HTTP 504产生120秒bounded-budget failure。
append-only correction保留最初“8次总计”的错误记录并把实际总数更正为9；它不改变attempt、失败层或`UNKNOWN`。E3、Python 3.13、
Workbench及先前步骤成功不能拼成original gate通过。

### PR #450 qualifying readback中的non-success observations

fresh README formal observation 1的anonymous API probe返回`403 / COLLECTION_BUDGET_EXHAUSTED / remaining=0`，同session Render仍
`COMPLETE / 200`，Core Verdict未创建。额度恢复后的observation 2独立PASS。independent reconciliation attempts 1/2又只在
per-command remote-main query遇到TLS unexpected EOF；versioned proof facility只改变显式Git proxy传入，attempt 3 PASS。所有旧identity
永久保留，qualification effect为`NONE`；它们不是subject或candidate regression。

## 问题连续性边界

本投影机械分开三层问题身份：

```text
original engineering problem = 维护准确、自洽、可公开观察且不越权的bounded current-state projection
current proof obligation      = 0.8 frozen-status publication的全部最后门与跨表面一致性
applicability world           = exact base cae001d/tree 8b38acf、本freeze candidate final bytes、attempt与fresh readback identity
proof_is_not_problem_solving  = true
```

#446 semantic freeze与#450 qualified failure history只是本projection必须准确陈述的既有事实，不是本文重新证明的产品对象。0.8 candidate
资格成立也只表示该有界阅读面在自己的world内可消费；它不等于完整Review产品、manifest、Evidence continuity、persistence或语言支持
资格持久化已经完成。

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
| 本页 | 当前0.8 publication world的有界公开阅读投影 | source of truth、scheduler、qualification或施工授权 |

验迹内部可以有很多插件、Provider、分析器和调度器，但最终优化目标始终是用户提出的工程问题，而不是插件自身的存在价值。

## 本页不能做什么

本页不能：

- 替代、裁剪、重写或删除`docs/milestones.md`；
- 把短投影冒充完整历史已经被Public Render观察；
- 修改P2 oracle、Collector coverage、Core充分性规则、runtime、tests、workflow、Release资产或download policy；
- 把任何旧FAIL/ERROR/CANCELLED/UNKNOWN升级为PASS；
- 决定证据充分性、qualification、state transition或下一合法seam；
- 把bounded private implementation freeze扩张解释为完整Review产品；
- 恢复global composition authority，或启动manifest、Evidence、persistence、public Review、R2–R6。

## 本projection的冻结生效条件

[successor 0.8 reconstruction contract](392-r1-public-project-state-projection-successor-0.8-reconstruction-contract.md)自己的candidate资格链已经
闭合；它只使本文成为`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_QUALIFIED_CANDIDATE_NOT_FROZEN`。只有独立
[freeze publication](393-r1-public-project-state-projection-0.8-freeze-publication.md)自己的local qualification、original PR gates、
protected exact-head merge、新exact-main Public CI与Browser Smoke、fresh anonymous installed-product README/本页/doc376/doc390/
doc391/doc392/doc393 Public Render、AGENTS/milestones raw+API+exact-Git byte observations、final milestones binding复算、independent
reconciliation与finite closeout全部成立后，本页才可成为`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_8_FROZEN`。

即使冻结门全部成立，本页仍不是scheduler；后继必须返回CONTROL LOOP重新选择最小合法seam。
