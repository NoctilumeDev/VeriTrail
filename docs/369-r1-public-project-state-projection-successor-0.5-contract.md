# R1 public project-state projection successor 0.5 contract

日期：2026-11-07

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_5_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@9b87e61ce3a361abaa3da458f49e43d5c5a1b769`，tree
> `200b9a093d9669ef242f991510530cafcf56afd9`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_BINDING_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改runtime、tests、fixtures、
> workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、projection 0.3 frozen
> bytes、0.4 failed bytes或任何其他frozen contract。

## 1. CONTROL LOOP 输入：doc368已资格化，两条旧失败链仍不回填

[文档368](368-r1-public-project-state-projection-0.4-failure-boundary-readback-target-correction-audit.md)由PR #420以exact
`base=03060eef4f6579c1d187ab2cad9806d2133cfeee / head=9f3220b266da249d28cef8010d7e84752f44ad58 /
tree=200b9a093d9669ef242f991510530cafcf56afd9`受保护合入本合同构造坐标。original Public CI
`42238105618`、exact-main Public CI `42242907968`与Browser Smoke `42242908069`均为attempt 1 SUCCESS
（11/11、11/11、1/1）。PR #418的失败run没有rerun。

第一个fresh root在产品调用前因生成的`plan_id`超过Schema 64字符上限而停止；它是proof-facility setup error，没有产品采集或
Core Verdict。第二个fresh root只认`9b87e61…`world，README与doc368各取得唯一formal PASS，AGENTS与milestones各取得唯一
raw.githubusercontent / GitHub Contents API / exact Git全字节一致观察；没有重跑milestones Render。anonymous rate diagnostic与
preflight #1–#3的`remaining=0`继续作为non-qualifying setup observations保留，后继可用窗口不覆盖它们。

independent reconciliation、122-artifact closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
509015292fc32d5aa9c1275f3bf89779a4f4730c290f8060da9b8a3098a78990
79f9be2d2e8450c815a30e87e5e620164c365c59b45bdb77d8dffbf6fc2cebb9
c2f2b8623b570785210f5ddc99c5e967f1f976ffb12b2d44d4d572811fccee47
f8ea43a0e10582a017fcd1dc3f2b1d43b9fe6959d1b37d66abae6bd7a5ca5126
```

因此doc368现在是
`R1_PUBLIC_PROJECT_STATE_PROJECTION_0_4_DUAL_FAILURE_BOUNDARY_READBACK_TARGET_CORRECTION_AUDITED_QUALIFIED_HISTORY`。
这只证明两条失败链及正确target责任已经形成qualified history；doc366、doc367与projection 0.4不被回填。

## 2. 为什么最小seam是0.5，而不是test/runtime maintenance或0.4重放

PR #418的candidate只修改五个docs surface；相同tree的original Public CI通过，而exact-main attempt 1在unchanged required
Python 3.10 test中得到expected `PENDING`、actual `FAIL`。失败output没有保留decisive assertion或临时Bundle，所以精确assertion仍为
`UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`，lower cause仍为`UNKNOWN`。PR #419与#420都没有修改runtime、test或workflow，且各自
required lane在新的original与exact-main world完成。这些新事实只证明后继docs world无需弱化门；它们不解释#418，也没有建立
可授权maintenance的runtime/test defect。

PR #419进一步证明doc367错误地把已知超过frozen 524288-byte Render window的milestones重新列为formal target。doc368已经恢复
正确责任：bounded reader surface走Render，完整milestones只走raw/API/Git字节对账。这是qualification seam correction，不是P2
oracle或Subject修复。

doc366/0.4的exact-main required gate真实失败，不能通过后继PASS取得资格；doc367自身readback又未资格化。与此同时，doc368
qualified history与完整milestones bytes已经形成新的current-state输入。根据projection合同，current effective state或source
milestones bytes变化必须version/rebind。因此最小合法seam是新的0.5 candidate；不是空提交、0.4 retry或无证据的maintenance。

## 3. 权威边界保持不变

| 对象 | 拥有 | 不拥有 |
| --- | --- | --- |
| Reality | 现实事实 | 被文档、测试或Verdict创造 |
| 人类授权者 | 目标、验收前提与必要Seal决定 | 被Business Layer或Core替代 |
| Provider | 自己实际观察到的事实及来源 | 全局事实或裁决权 |
| R/Q/O/T | 各自冻结合同规定的分析、观察与调度职责 | 越界扩张或隐式共享权威 |
| Business Layer | 业务流程组织、能力选择与补证请求 | 证据充分性裁决或PASS宣布 |
| Core | 证据完整性、绑定、充分性与确定性裁决 | 现实事实的超级所有权 |
| `docs/milestones.md` | 完整append-only工程历史、链接与provenance | 必须落入Public Render窗口的义务 |
| `docs/project-state.md` | 有界current-state公开阅读投影 | source of truth、scheduler、qualification或施工授权 |

验迹内部可以有很多插件、Provider、分析器和调度器，但最终优化目标始终是用户提出的工程问题，而不是插件自身的存在价值。

## 4. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5`

0.5冻结以下投影合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因此没有自引用；
4. protected merge后必须把projection声明与exact merge中的真实milestones blob重新对账；相同内容或摘要不能继承另一个
   base/head/tree/attempt的资格；
5. README/AGENTS只提供短入口，必须继续链接完整milestones，并明确projection没有事实、qualification或scheduler authority；
6. 任一完整milestones bytes或current effective state变化都要求新的versioned publication/rebind；0.3只保留frozen historical
   identity，0.4只保留failed/not-qualified identity；
7. #418 exact-main failure、#419 proof-target与truncation failures、#420 plan-id setup error、anonymous rate exhaustion及全部早期
   failure chain继续保留，不被0.5 PASS覆盖；
8. 本合同只重开projection binding/readback target boundary，不修改Collector cap、Core充分性规则、private implementation或产品runtime。

本candidate最终milestones绑定为：

```text
source_binding_kind = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes = 619569
source_milestones_sha256 = 65c7c362fcfc0c2831bb7e60fc738b0d7278b37a4b4c2c5b8b83ae10425de7bd
source_milestones_blob_sha1 = a0d02fe3d24b855ed9609b0a8ac71bf1af814edc
```

local qualification必须在commit前后各复算一次，并证明本文、project-state与final milestones bytes完全一致。

## 5. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/369-r1-public-project-state-projection-successor-0.5-contract.md
docs/project-state.md
docs/milestones.md
```

合入后只认新merge SHA，并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal |
| `docs/project-state.md` | anonymous Public Render diagnostic + unique formal；marker必须属于0.5 |
| doc366 | anonymous Public Render diagnostic + unique formal；保留0.4 failed contract原身份 |
| doc367 | anonymous Public Render diagnostic + unique formal；保留自身readback未资格化原身份 |
| doc368 | anonymous Public Render diagnostic + unique formal；绑定授权本version bump的qualified history |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致并核对projection声明摘要；raw bytes不冒充Render COMPLETE |

fresh产品调用必须清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用代理。任一non-success按自己的identity保留并
停止，不得换target、重复target、使用认证访问替代或拼接旧PASS。

## 6. qualification pipeline

final bytes至少通过UTF-8 without BOM、LF/final LF、links/fences/headings、required markers、exact scope、milestones/projection
binding、`git diff --check`、global/local hygiene、primary audit continuity与Python 3.10.6/3.13.13 × normal/`-O` focused
unchanged-runtime witness。

```text
final docs-only bytes + local qualification + candidate milestones binding
  -> original PR required gates (attempt 1; no rerun laundering)
  -> protected exact-head merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh six-target anonymous installed-product observations + two raw-byte observations
  -> independent reconciliation + finite closeout
  -> R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_5_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> return CONTROL LOOP
```

## 7. 停止线

全部门成立以前，0.5仍只是candidate；0.3继续是不可改写的frozen historical projection，0.4继续是不可回填的failed
not-qualified projection。0.5 candidate即使完整资格化，也必须返回CONTROL LOOP并建立独立docs-only freeze publication。不得把
contract/projection candidate自动解释为#398 private implementation已经冻结、global composition authority已恢复，或
manifest/Evidence/persistence/public Review/R2–R6已获授权。
