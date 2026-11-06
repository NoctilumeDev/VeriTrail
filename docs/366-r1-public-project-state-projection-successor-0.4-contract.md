# R1 public project-state projection successor 0.4 contract

日期：2026-11-06

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@27f0b93eeb5ace7b5428ebc0c07cb1ebe4199f25`，tree
> `f96b396e7bbdb42af9f4f6a75bbc8d730eede7af`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_BINDING_ONLY`。本文不修改runtime、tests、workflow、Schema、Provider、Collector、
> P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、projection 0.3 frozen bytes或任何其他frozen contract。

## 1. CONTROL LOOP 输入：doc365已资格化，旧world仍不回填

[文档365](365-r1-post-terminal-fact-dual-successor-private-implementation-readback-qualification-recovery.md)由PR #417以exact
`base=e0ab9d0679f1706cdde3103ef0e1076baa681b59 / head=d400a738e39c97e743ba7bec7315c68e9f534bb1 /
tree=f96b396e7bbdb42af9f4f6a75bbc8d730eede7af`受保护合入本构造坐标。original Public CI `42191635218`、
exact-main Public CI `42196105120`与Browser Smoke `42196105123`均为attempt 1 SUCCESS（11/11、11/11、1/1）。

第一次fresh readback root的README formal命中`403 / COLLECTION_BUDGET_EXHAUSTED / remaining=0`；第二个fresh root选择的
旧README marker在source中一次、rendered text中零次，产品以`Render Evidence marker drifted`停止。两个formal均未形成Core
Verdict；subject failure与candidate regression未建立，底层anonymous resource与GitHub presentation机制保持`UNKNOWN`。第三个fresh
root从空history建立新Plan/session/Evidence，README、project-state、doc345、doc346、doc364、doc365各自唯一formal均为
API/Render `COMPLETE`、cleanup complete与Core `PASS`；AGENTS/milestones各自唯一raw.githubusercontent、GitHub Contents API与
exact Git观察逐字节一致，没有复用早期PASS。

两个failure-boundary与各自failed closeout SHA-256为：

```text
f6398f3a086f1d463eb7d647049f074840d5fb10dc19054bcca465b5eebd049f
c01cf59cc90e05f5d27a953c325058f701465fda63ef84a91ad2ccc36d127a35
f72c7a68ff5505baf36f75282349e8b990c6a3a440830f8a8ffb258ec61a719c
ef25d072f6f8def9f30afb74ae983b90d4e51a54a097071ee06fd1ef4472bd7d
```

independent reconciliation、177-artifact closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
b5a02d33ce7423c4173f4196326c5deafdd829f9a0d531cdb36b18cf6a50d448
d9d69aec5da9baf0dc48a5966ce6595ac85f6d88aa2a4d8edaa7a9f1ea7d04c4
46ac81de42273097329102a46be88d412084d8ef57b2e531842aa22c86cd8c0a
e526f7ca23ba0d9ef3d25eb44dd745466efc6fe215f52f58e45ae2ba2f7e478f
```

因此doc365现在是qualified history，#398/doc346成为
`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。旧milestones truncation、#399 original gate failure、
两次readback recovery non-success及其`UNKNOWN`继续保持原身份。

## 2. 为什么projection 0.3必须成为历史投影

[projection 0.3 contract](363-r1-public-project-state-projection-recovery-successor-0.3-contract.md)与
[freeze publication](364-r1-public-project-state-projection-0.3-freeze-publication.md)已经完成独立资格链并冻结。其固定source binding为：

```text
source_milestones_bytes = 599729
source_milestones_sha256 = 4ad66def6e220eca45c334f65222022f5d5ace0ea5ad458873082acd0bd85fec
source_milestones_blob_sha1 = b2b983cacde0a6990d394a1087d92a3b78c83291
```

0.3冻结时#398仍是`READBACK_NOT_QUALIFIED / NOT_FROZEN`。doc365的后继完整链改变了当前有效事实，也使完整milestones bytes变化。
根据0.3自己的合同，任一source milestones bytes或current effective state变化都必须建立新的versioned publication/rebind。冻结历史不能
静默改写；因此`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_FROZEN`继续保留为`FROZEN_HISTORICAL`，但不能冒充当前投影。

最小合法seam只能是0.4：重新绑定final same-candidate milestones bytes并公开#398的新资格状态。0.4不直接冻结private implementation，
也不重开runtime、P2/Core或任何事实语义。

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

最终优化目标始终是用户提出的工程问题，而不是插件、Provider或编排器自身的存在价值。

## 4. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4`

0.4冻结以下投影合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因此没有自引用；
4. protected merge后必须把projection声明与exact merge中的真实milestones blob重新对账；相同内容或摘要不能继承另一个
   base/head/tree/attempt的资格；
5. README/AGENTS只提供短入口，必须继续链接完整milestones，并明确projection没有事实、qualification或scheduler authority；
6. 任一完整milestones bytes或current effective state变化都要求新的versioned publication/rebind；0.3只保留冻结历史身份；
7. #398旧truncation、#399 gate failure、#417两个readback non-success与全部早期failure chain继续保留，不被0.4 PASS覆盖；
8. 本合同只重开projection binding/readback boundary，不修改Collector cap、Core充分性规则、private implementation或产品runtime。

本candidate最终milestones绑定为：

```text
source_binding_kind = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes = 609477
source_milestones_sha256 = dd815b3a598e781debbb5eb6291dc3d8032e8d374b1c852c40da953fae6011c7
source_milestones_blob_sha1 = b250410a9641ecd13e7ff7fe2804b66a683433fe
```

local qualification必须在commit前后各复算一次，并证明本文、project-state与final milestones bytes完全一致。

## 5. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/366-r1-public-project-state-projection-successor-0.4-contract.md
docs/project-state.md
docs/milestones.md
```

合入后只认新merge SHA，并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal |
| `docs/project-state.md` | anonymous Public Render diagnostic + unique formal；marker必须属于0.4 |
| doc346 | anonymous Public Render diagnostic + unique formal；复核implementation candidate原始边界 |
| doc364 | anonymous Public Render diagnostic + unique formal；复核0.3 frozen historical identity |
| doc365 | anonymous Public Render diagnostic + unique formal；绑定授权本version bump的qualified history |
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
  -> R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_4_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> return CONTROL LOOP
```

## 7. 停止线

全部门成立以前，0.4仍只是candidate；0.3继续是不可改写的frozen historical projection。0.4 candidate即使完整资格化，也必须
返回CONTROL LOOP并建立独立docs-only freeze publication。不得把contract/projection candidate自动解释为#398 private implementation
已经冻结、global composition authority已恢复，或manifest/Evidence/persistence/public Review/R2–R6已获授权。
