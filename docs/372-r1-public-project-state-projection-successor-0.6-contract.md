# R1 public project-state projection successor 0.6 contract

日期：2026-11-07

> 候选状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_CANDIDATE_NOT_QUALIFIED_NOT_FROZEN`。
>
> 构造坐标：`main@12d170633657871985727be6cf68d031534faf16`，tree
> `9b2e4420dc6a165dfa94cc4c094059d696a8f267`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_BINDING_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改runtime、tests、fixtures、
> workflow、Schema、Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics、projection 0.5 frozen
> bytes、0.4 failed bytes或任何其他frozen contract。

## 1. CONTROL LOOP 输入：fixed private implementation已经冻结

[文档371](371-r1-post-terminal-fact-dual-successor-private-implementation-freeze-publication.md)由PR #423以exact
`base=7049de0093f5967ea3dcce65d517b5daeea4123f / head=8b730b8263c5609e3d5cca928fc853b1062918c4 /
tree=9b2e4420dc6a165dfa94cc4c094059d696a8f267`受保护合入本合同构造坐标。original Public CI
`42310836886`、exact-main Public CI `42314707614`与Browser Smoke `42314707612`均为attempt 1 SUCCESS
（11/11、11/11、1/1）。

第一个fresh root的六个Render diagnostic均为`COMPLETE / HTTP 200`，但README proof marker在rendered text中出现零次；唯一
formal以`FORMAL_READBACK_ERROR / PROOF_TARGET_SELECTION_ERROR / RENDERED_TEXT_OCCURRENCES_ZERO`停止。API/Render仍完整，
Core Verdict没有创建，lower cause保持`UNKNOWN`。该root的
failure record与82-artifact closeout SHA-256为：

```text
8a33b12b1e4f1f4572cde33b61514da7666ecc32e140f95902abfe68920dd842
b098bd6e20031a56a4aceb3427c3be5182a27ec2126ea1c449c8aa9217f313fc
```

第二个fresh root只重开被击穿的marker target boundary，并在diagnostic阶段强制`rendered_text_occurrences == 1`。README、
project-state、doc346、doc365、doc370与doc371各有唯一formal `PASS`；AGENTS与milestones各有唯一raw/API/exact-Git全字节一致
观察。independent reconciliation、179-artifact closeout、expected stdout self-capture mismatch与finite integrity为：

```text
49cad261d6e27a7a298a305fe0df44c85f85b5bff034ee9e1367dd9343b98f3a
6f57930d592e659ab711329dc8041512cb445e67a8c902942f68ac4ec17f08b8
ceeef7d0a3ed6655dbc278696cc80a4daa5c162645f370d94a004e29852cd2a2
5ac8dc86827b89db999889b0a1fadb56f7542e1aa4ba14aea41980bd1f627a54
```

因此`R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN`已生效。首个formal错误没有被后继
PASS覆盖或解释。

## 2. 原问题、证明义务与适用world必须保持同一身份

本次状态变化只回答一个有界命题：doc340–346定义的versioned private `POST_TERMINAL_DUAL_SUCCESSOR_0_1` selector及其两个既有
downstream，在声明world内已经完成实现、exact-main双门、fresh readback与独立reconciliation并被冻结。

它没有把原问题换成“完整Review产品已经完成”，也没有证明application-level unified Review/Coverage output admission、manifest、
same-attempt Evidence continuity、persistence或public Review surface存在。形式证明只能升级其明确绑定的证明对象；不得用局部命题的
成立替代用户工程问题的完成。

因此本project-state rebind必须同时保留：

1. 原问题身份：用户需要可验证的工程问题闭环，而不是插件或private selector自身的存在；
2. 证明义务身份：本次只证明fixed private dual-successor implementation frozen；
3. 适用world身份：doc340–346声明的private 0.1 world、exact PR #398/#417/#423链与对应readback identity；
4. 未授权边界：global composition authority、manifest、Evidence continuity、persistence、public Review与R2–R6仍未启动。

## 3. 为什么最小seam是0.6，而不是直接恢复composition authority

projection 0.5冻结时，#398/doc346仍是`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`。PR #423闭合后，
这个事实已经变成`PRIVATE_IMPLEMENTATION_FROZEN`，所以0.5不再是current projection，只能保留frozen historical identity。

新事实没有提供application-level unified output admission、manifest carrier、same-attempt Evidence continuity或persistence证据。根据
project-state合同，current effective state变化必须version/rebind；根据CONTROL LOOP，新状态必须先反馈公开投影，再独立审计下一
最小authority seam。因此当前只能建立0.6 candidate，不能顺带施工runtime或宣布完整问题已解决。

## 4. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6`

0.6冻结以下投影合同：

1. `docs/project-state.md`必须小于65536 UTF-8 bytes，不复制完整milestones；
2. projection必须显式记录版本、candidate状态、构造base/tree、完整candidate milestones bytes/SHA-256/blob SHA-1、当前有效事实、
   retained failures、停止线与自身资格条件；
3. milestones candidate bytes先独立完成，再机械计算摘要并写入projection与本文；milestones不记录自己的摘要，因而没有自引用；
4. protected merge后必须把projection声明与exact merge中的真实milestones blob重新对账；相同内容或摘要不能继承另一个
   base/head/tree/attempt的资格；
5. README/AGENTS只提供短入口，必须继续链接完整milestones，并明确projection没有事实、qualification或scheduler authority；
6. 任一完整milestones bytes或current effective state变化都要求新的versioned publication/rebind；0.5只保留frozen historical
   identity，0.4只保留failed/not-qualified identity；
7. #398旧milestones truncation、#399 gate failure、#417两个formal non-success、#418 exact-main gate failure、#419
   proof-target/truncation failures、#420 plan-id/rate observations、#423首个README formal error与全部setup failure继续保留；
8. 本合同只重开projection binding/readback target boundary，不修改Collector cap、Core充分性规则、private implementation或产品runtime。

本candidate最终milestones绑定为：

```text
source_binding_kind = FINAL_SAME_CANDIDATE_MILESTONES_BYTES
source_milestones_bytes = 627708
source_milestones_sha256 = b288c3e344e2cbb547bf0619799ae01f55213097550dd8535b8384f9324b6a77
source_milestones_blob_sha1 = e8cf9edd57a2f7935caaa3eedbc627fc81385165
```

local qualification必须在commit前后各复算一次，并证明本文、project-state与final milestones bytes完全一致。

## 5. tracked scope与fresh observation

唯一允许的tracked scope是：

```text
README.md
AGENTS.md
docs/372-r1-public-project-state-projection-successor-0.6-contract.md
docs/project-state.md
docs/milestones.md
```

合入后只认新merge SHA，并取得：

| target | required fresh observation |
| --- | --- |
| `README.md` | anonymous Public Render diagnostic + unique formal；marker必须属于0.6 reader surface |
| `docs/project-state.md` | anonymous Public Render diagnostic + unique formal；marker必须属于0.6 |
| doc365 | anonymous Public Render diagnostic + unique formal；绑定#398 readback qualification recovery |
| doc370 | anonymous Public Render diagnostic + unique formal；绑定0.5 frozen historical identity |
| doc371 | anonymous Public Render diagnostic + unique formal；绑定授权本version bump的新frozen fact |
| 本文 | anonymous Public Render diagnostic + unique formal |
| `AGENTS.md` | exact-commit raw.githubusercontent + GitHub Contents API + exact Git全字节一致 |
| `docs/milestones.md` | exact-commit raw/API/Git全字节一致并核对projection声明摘要；raw bytes不冒充Render COMPLETE |

fresh产品调用必须清除token、`NO_PROXY`、`PYTHONPATH`与`PYTHONHOME`，只按命令使用代理。diagnostic必须先证明marker在rendered text中
恰好出现一次；任一non-success按自己的identity保留并停止，不得换target、重复target、使用认证访问替代或拼接旧PASS。

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
  -> R1_PUBLIC_PROJECT_STATE_PROJECTION_SUCCESSOR_0_6_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> R1_PROJECT_STATE_PUBLIC_PROJECTION_0_6_QUALIFIED_CANDIDATE_NOT_FROZEN
  -> return CONTROL LOOP
```

## 7. 停止线

全部门成立以前，0.6仍只是candidate；0.5继续是不可改写的frozen historical projection，0.4继续是不可回填的failed
not-qualified projection。0.6 candidate即使完整资格化，也必须返回CONTROL LOOP并建立独立docs-only freeze publication。不得把
contract/projection candidate自动解释为global composition authority已经恢复，或manifest/Evidence/persistence/public Review/
R2–R6已经获得授权。
