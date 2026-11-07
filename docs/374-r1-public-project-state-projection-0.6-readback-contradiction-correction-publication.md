# R1 public project-state projection 0.6 readback contradiction correction publication

日期：2026-11-07

> 条件化状态目标：`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FROZEN`与
> `R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_FROZEN`。
> 本文自己的全部最后门闭合以前，这两个目标都不是生效事实。
>
> correction基线：`main@46493dc86422a7648d283881239787526b3ea039`，tree
> `8e1046ce3238dd752495dd3b1bd6e0bf89c0d342`。
>
> 上游：[0.6 contract candidate](372-r1-public-project-state-projection-successor-0.6-contract.md)、
> [failed freeze publication](373-r1-public-project-state-projection-0.6-freeze-publication.md)与
> [bounded public projection](project-state.md)。
>
> 影响：`L0_DOCUMENTATION / PUBLIC_STATE_AND_FREEZE_PUBLICATION_RESPONSIBILITY_CORRECTION_ONLY`。
> 本文不修改project-state、doc372、doc373、runtime、tests、fixtures、workflow、Schema、Provider、Collector、
> P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP：形式绿灯没有解决原工程问题

PR #424已经使doc372与projection 0.6成为`QUALIFIED_CANDIDATE / NOT_FROZEN`。PR #425随后把doc373 publication候选精确合入
新的main；candidate和exact-main自动门均为全绿。然而，publication target还要求fresh anonymous installed-product readback与
independent reconciliation。绿色CI不能替代这些门，也不能自行升级public state。

fresh README diagnostic触发了对exact source的复核：README的主状态仍称0.6 successor candidate“尚未资格化或冻结”，而同一
README后文、AGENTS、milestones与doc373都已经记录#424完整资格链及
`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_QUALIFIED_CANDIDATE_NOT_FROZEN`。这不是单纯的marker拼写问题，而是当前公开状态内部矛盾。

因此原始工程问题、当前证明义务与适用world必须继续机械分开：

```text
original engineering problem = 发布准确、自洽且可读回的projection 0.6冻结状态
current proof obligation      = 观察#425 exact-main公开产品表面并证明其与固定资格事实一致
applicability world           = main@46493dc86422a7648d283881239787526b3ea039
```

选择另一个恰好存在的marker也许能得到形式PASS，却会把证明对象从“公开状态是否准确”换成“某个字符串是否存在”。本文拒绝这种
proof drift，只重开被真实反例击穿的最小public-state/freeze-publication responsibility。

## 2. PR #425 exact身份与自动门

```text
PR                   = #425
base                 = 69a17b2da86a2f4d9dd09e5ab5724e5fa0ec82e0
head                 = 541689bb2f7f715bbe87fd9e7de259efbcf4fa43
ordinary merge       = 46493dc86422a7648d283881239787526b3ea039
candidate/merge tree = 8e1046ce3238dd752495dd3b1bd6e0bf89c0d342
diff                 = 1 commit / 4 files
```

original Public CI `42331317365`、exact-main Public CI `42333719108`与Browser Smoke `42333719103`均为attempt 1 SUCCESS，
分别为11/11、11/11与1/1；没有rerun。candidate local qualification、original qualification、protected merge与exact-main gate
evidence SHA-256为：

```text
0d4cb711d9b21d7ddd2359db4c55f0bc15403f866a2955ee9950c559c632426e
2b51f7993c1b3c1e6e794055bc1169c4581ef00225e3e6bc65e589467e1fae0f
729d6174b5b2346720645c4c64aa7c77b3115940b5eb29b1938cdfb4291102fe
3e7b4bbb100266de2f5fefae69518680958dd76452d7b122a4d00c85bd53712e
```

这些身份继续有效地证明各自门；它们不证明fresh public-state readback，也不使doc373 target自动生效。

## 3. 两个fresh proof-facility world与真实反例

第一个fresh root只认`46493dc…`world。proof-facility identity audit attempt 1先把自身脚本中的预期路径误判成引用旧world，保留为
self-inspection setup error；attempt 2通过。随后preformal发现facility仍读取旧gate字段`merge/tree`，而当前exact-main gate evidence
使用`merge_commit/merge_tree`。该world在任何网络observation、diagnostic、formal或Core Verdict前停止，分类为
`PROOF_FACILITY_GATE_SCHEMA_ERROR / REJECTED_NON_QUALIFYING`，有限closeout SHA-256为：

```text
195d10b08c66f0941f8fc481ccffa9ec1895543d6f46469ee66dfc9d07a5147a
```

第二个fresh root在独立目录中只修正facility gate schema，重新绑定original problem、proof obligation与applicability world，并从零
建立Python 3.13.13、Core 0.13.0、GitHub Evidence 0.1.0与Playwright 1.62.0 installed-product environment。proof identity audit、
adapter freeze与preformal validation SHA-256为：

```text
c48e256082f5352786a71a2f899f139354931ada46e700a9a9fe8dc57b7b0d00
7be6000fe22ec66126c4765c04fbecd36232057bd6861cfec089c1386433b2a1
16828af39ade7e838762a59b05d4c3eba8e34bb2e84ecb3851ce557999180e81
```

anonymous rate diagnostic #1观察到remaining 0并在reset前停止；reset后重新读取source/setup/adapter、复核remote main与primary
`audit.json`，diagnostic #2与API preflight #1分别观察到remaining 60与59。对应SHA-256为：

```text
5d23af0c468fe9755cb16f2def265fdc10c831eb345e310801318f745440a48d
38d69cf14092d4d4ee2d5449a8c89a5b6be10f4c23b91f7a9b91f9923cc8792d
8e1c9d85f120f01323dbfdf7eff729e1fa67fc183ae536d9e258e53652c53324
```

README diagnostic identity为`r1-psp-v6-freeze-publication-diagnostic-readme-1-46493dc`。API/Render均为`COMPLETE / HTTP 200`，但
预注册reader-visible phrase出现0次。该结果本身只触发source inspection；真实反例由exact source comparison建立：

```text
README primary state = 0.6 successor candidate尚未资格化或冻结
#424 qualified fact  = 0.6 QUALIFIED_CANDIDATE / NOT_FROZEN
```

diagnostic按原identity保留为`DIAGNOSTIC_ONLY_NON_QUALIFYING_ERROR`；Core Verdict为none，README formal、其他Render targets与
AGENTS/milestones raw formal均未开始。diagnostic history、Render artifact与failed readback closeout SHA-256为：

```text
3262d4a3f30bd0bc7aea15560a2abcdf91ad3d032befcf4ef137fbd5d6d4bde4
5a318bbef37ca735da8f8d3b5288aac47b851a5c2bb853b17c1a1da51d06a602
828bca82ea701e0fc23e61eee178c80ef6cf9eae1c35ad1d77bbaf458d9517b9
```

## 4. 失败边界与禁止的伪恢复

当前机械状态是：

```text
doc372 / projection 0.6 = QUALIFIED_CANDIDATE / NOT_FROZEN
doc373                     = MERGED / NOT_QUALIFIED / NOT_EFFECTIVE
manifest/Evidence/persistence/public Review/R2-R6 = NOT_STARTED / NOT_AUTHORIZED
```

被击穿的是README public-state与doc373 freeze-publication responsibility，不是doc372/project-state semantic bytes、P2 Collector、Core
oracle、runtime或tests。后继禁止：

```text
retry the same formal until PASS
pick a different marker while leaving the contradiction intact
splice #425 green gates with another readback world
rewrite doc373 as qualified or effective history
modify doc372/project-state/runtime/tests/oracle to hide the public-state error
infer downstream authority from a corrected README
```

所有setup failure、rate exhaustion与UNKNOWN继续保留；后继PASS只能建立新的qualified world，不能删除、解释或回填本次失败。

## 5. 本correction publication的精确scope

本docs-only candidate只允许修改：

```text
README.md
AGENTS.md
docs/milestones.md
docs/374-r1-public-project-state-projection-0.6-readback-contradiction-correction-publication.md
```

README只校正current public-state叙述并指向本文。AGENTS与milestones只追加#425失败事实、边界与后继资格责任。本文version新的
freeze-publication responsibility。`docs/project-state.md`、doc372、doc373、runtime、tests、fixtures、workflow、Schema、Provider、
Collector、P2/Core oracle、Verdict与全部frozen semantic bytes必须保持`46493dc…` base bytes。

本层local gates必须机械核对exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
reader-visible README current-state marker、#425 exact identities、两个fresh root、retained diagnostic/failure identities、unchanged semantic
files、`git diff --check`、read-only global/local hygiene、focused unchanged-runtime witness及primary `audit.json` continuity。

## 6. 本publication自己的资格链

```text
correction final bytes / declared local gates
  -> original correction PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc372 / doc373 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / identity / retained-history reconciliation
  -> target PROJECTION_0_6_FROZEN becomes effective
  -> return CONTROL LOOP
```

本publication的Plan/session/Evidence不可复用#424或#425 world。diagnostic不计入资格；任何non-success按原identity保留并停止。新的
fresh readback必须验证README current-state的完整语义一致性，不能只证明某个替代字符串存在。

## 7. 当前candidate状态与生效上限

本文进入仓库不等于correction或freeze生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_FREEZE_PUBLICATION_MERGED_NOT_QUALIFIED_NOT_EFFECTIVE
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_READBACK_CONTRADICTION_CORRECTION_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN_HISTORICAL
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部最后门闭合后，本文开头两个conditional target才成为事实；doc373仍保留为失败且未生效的publication history。随后必须从新
exact main返回CONTROL LOOP，重新判断下一最小合法seam，不能按文档编号自动恢复composition authority或启动manifest、Evidence、
persistence、public Review或R2–R6。
