# R1 public project-state projection recovery successor 0.3 contract

日期：2026-11-06

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@e5e8c8895e811f858850ae5f5094f7595eac9120`，tree
> `8848573c63db3561f9e23662a4524f360c0d4480`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改runtime、tests、workflow、Schema、
> Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP 输入：doc362已资格化，旧world仍不回填

[文档362](362-r1-public-state-projection-doc350-readback-recovery-publication.md)已经由PR #414以exact candidate
`base=605adc43602422361f52d1f62fc13b089177141a / head=6afe3286bbe34123f0c2bd4d18d2ddbaa83751fb /
tree=8848573c63db3561f9e23662a4524f360c0d4480`受保护合入本合同构造坐标。original Public CI
`42139119249`、exact-main Public CI `42142668773`与Browser Smoke `42142668786`均为attempt 1 SUCCESS
（11/11、11/11、1/1）。

fresh README、doc350、doc361、doc362各自唯一formal均为API/Render `COMPLETE`、marker一次、cleanup complete与Core
`PASS`；AGENTS/milestones各自唯一raw.githubusercontent、GitHub Contents API与exact Git观察逐字节一致。第一次anonymous
rate diagnostic与API preflight的`remaining=0 / 403`按原identity保留；reset后只以新编号继续，没有重复任何PASS。独立
reconciliation、150-artifact closeout、expected stdout self-capture mismatch与finite integrity SHA-256为：

```text
3cce7fd1a156e78c7c464d03654fac6fbd80cf37da44306a0b5992c53de64b3c
bb7e8509edaf5051ac3a0a3284ccf04de7970fb21aa1a4469d243175f11450d6
069b696b15ff9145efdc33e60188177e65726cfa2514d6ed4914fc436dd6c938
ba0a432f470bc5015080835a17f5be86ee9a0c16f6660643f895bb91f35646de
```

因此doc362现在是
`R1_PUBLIC_PROJECT_STATE_PROJECTION_DOC350_READBACK_RECOVERY_PUBLICATION_0_2_QUALIFIED_HISTORY`。这只解除重新判断
projection successor的阶段停止线；#401 marker drift、#402 persistence failure、#404 cancellation、#405 marker drift、#406
API exhaustion以及所有未运行目标、setup failure和`UNKNOWN`继续保持原身份。

## 2. 为什么不能直接冻结旧projection 0.2

[文档349](349-r1-public-project-state-projection-recovery-successor-contract.md)与本candidate修改前
[project-state](project-state.md)的0.2 candidate bytes绑定：

```text
source_exact_base = 34de9427d64ba8a3c77ac38eefe146fa8d2e2d77
source_tree = f6edc136e2bd156409fad553c6453ceee73ccd97
source_milestones_bytes = 568856
source_milestones_sha256 = d468191fcfbbaa8df31f592db35e494a8363ddd4f9c1c735dec26ab41a495ccf
```

其PR #401已经通过original/exact-main双门，但唯一README formal观察到sealed source marker一次、rendered marker零次，故产品在
Verdict形成前fail closed；projection 0.2与doc349保持`MERGED / READBACK_NOT_QUALIFIED / NOT_FROZEN`。后继doc350/doc351/
doc353/doc354/doc359/doc360/doc361/doc362及release-download maintenance形成了新的qualified/retained事实，完整milestones bytes也
已经变化。旧0.2 candidate不能通过后来的PASS获得新coordinate资格，也不能把旧source binding冒充current projection。

因此最小合法seam不是直接冻结0.2，而是版本化为0.3并重新绑定完整candidate milestones bytes。该version bump不重开P2、Core、
runtime或任何事实语义，只修正公开投影输入身份和reader-visible proof target。

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

## 4. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3`

0.3继续冻结以下投影合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes先独立完成，再机械计算摘要并写入projection；milestones不记录自己的摘要，因此没有自引用；
4. protected merge后必须把projection中声明的milestones摘要与exact merge中的真实blob重新对账；相同内容或摘要不能继承另一个
   base/head/tree/attempt的资格；
5. README/AGENTS可以提供短入口，但必须继续链接完整milestones并明确projection没有事实、qualification或scheduler authority；
6. 任一完整milestones bytes或current effective state变化都要求新的versioned publication/rebind；旧projection只保留历史；
7. old 0.2 candidate、#401 formal ERROR与全部后继failure chain继续保留，不被0.3 PASS覆盖；
8. 本合同只重开projection/readback target boundary，不修改Collector cap、Core充分性规则或任何产品runtime。

本candidate最终milestones绑定为：

```text
source_binding_kind = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes = 599729
source_milestones_sha256 = 4ad66def6e220eca45c334f65222022f5d5ace0ea5ad458873082acd0bd85fec
source_milestones_blob_sha1 = b2b983cacde0a6990d394a1087d92a3b78c83291
```

local qualification必须在commit前后各复算一次，并证明本文、project-state与final milestones bytes完全一致。

## 5. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/363-r1-public-project-state-projection-recovery-successor-0.3-contract.md
docs/project-state.md
docs/milestones.md
```

合入后只认新merge SHA，并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal |
| `docs/project-state.md` | anonymous Public Render diagnostic + unique formal；marker必须属于0.3 |
| doc349 | anonymous Public Render diagnostic + unique formal；保留0.2合同原身份 |
| doc350 | anonymous Public Render diagnostic + unique formal；保留#401 failure boundary |
| doc362 | anonymous Public Render diagnostic + unique formal；绑定授权本version bump的qualified history |
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
  -> fresh eight-target anonymous installed-product observations
  -> independent reconciliation + finite closeout
  -> R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_SUCCESSOR_0_3_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> R1_PROJECT_STATE_PUBLIC_PROJECTION_0_3_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> return CONTROL LOOP
```

## 7. 停止线

全部门成立以前，0.3仍只是candidate；0.2继续`MERGED / READBACK_NOT_QUALIFIED / NOT_FROZEN`。0.3 candidate即使完整
资格化，也必须返回CONTROL LOOP并建立独立docs-only freeze publication。不得把contract/projection candidate自动解释为private
implementation已冻结、global composition authority已恢复，或manifest/Evidence/persistence/public Review/R2–R6已获授权。
