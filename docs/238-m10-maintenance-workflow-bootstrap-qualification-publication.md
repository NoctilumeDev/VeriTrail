# M10 maintenance workflow bootstrap 资格发布

日期：2026-10-09

## 1. 发布对象与条件状态

本文只发布[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
第 5 节定义的 maintenance workflow bootstrap 与 phase-two governance 事实。本文自己的 final bytes、
original PR 门、受保护 main 合入、new exact-main Public CI / Browser Smoke、fresh anonymous
installed-product readback 与 independent reconciliation 全部成立后，以下目标才成为当前事实：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

最后门闭合以前，README、AGENTS 与 milestones 中的 target marker 只是条件化 publication bytes。本文不修改
runtime、tests、workflow、dependency、version、tag、Release、asset、Parse / Fact / Coverage 合同或
`DECLARED_CLAIM_FIDELITY`。

## 2. 合格输入与重新定界

[文档 237](237-m10-maintenance-dependency-drift-qualification-publication.md)已经把 dependency-drift 修正闭合为：

```text
main        = f20ce800bcc0f9f7a76da01555bdf466e9695eac
main tree   = 47b6334af4aba882261361c2dd2cb577c5a09faa
maintenance = 685b077203c4c9b74a1ef14649a4ee5f8d16d82c
lock blob   = 297be5c0bcc30729c0f4c3f4322be74641b2a916
lock SHA256 = D9FBF89CA905EC2602B9956E986E24F74C38AAF4DE3EA960D1DBA3905EBD00A4
```

重新进入 CONTROL LOOP 后，official-registry `npm 11.19.1 audit` 在 exact maintenance tip 上仍为 0
vulnerabilities；ruleset `24216773` 仍 active、无 bypass、只含 phase-one 的 deletion、non-fast-forward 与
pull-request rules；没有并行 maintenance PR。由此，fresh workflow-only bootstrap 仍是最小合法 seam。

相同 workflow patch 曾出现在关闭、未合入的 PR #264；patch bytes 相等不继承 #264 的 PR、CI、attempt、merge
或 qualification authority。

## 3. workflow-only candidate 的 final-byte 资格

fresh candidate 坐标为：

```text
base   = 685b077203c4c9b74a1ef14649a4ee5f8d16d82c
head   = 4b262eb24e101d8bfc7605b8a7a14ce0b15386fe
tree   = 7d7f9ed1ed9a8b7c7bc50ff843da182f77d680b4
branch = ci/m10-maintenance-workflow-bootstrap-685b077
```

候选只修改：

```text
.github/workflows/ci.yml
.github/workflows/browser-smoke.yml
```

精确变化只是在 Public CI 的 `push` / `pull_request` 与 Browser Smoke 的 `push` branch filter 中加入
`core-0.12-maintenance`。job、step、action pin、timeout、test command 与产品字节均未改变。

本地 final-byte witness：

| 门 | 结果 |
| --- | --- |
| exact diff / YAML / branch-filter static projection | Python 3.10 / 3.13、normal / `-O` 四格逐字节一致 PASS |
| Core / Starter / Authoring Skill | 四格各 `347/347` PASS |
| Workbench | `14 files / 172 tests`、lint、type-check/build PASS |
| dependency audit | npm `11.19.1`、official registry、0 vulnerabilities |
| Browser acceptance | `COMPLETED / PASS`、5 checks、102 requests、0 HTTP errors、端口释放 |

canonical patch SHA-256 为
`dd6f7535610d16c7053e9201fd43b3cf2cd976f86fab23d9e13c7c48ac67f65c`；四格 static projection
SHA-256 为 `9676e7583cef169e60ff835349893581d49a9ec87d02c6de7bb7177d0abdfd50`。

## 4. PR、ordinary merge 与 exact maintenance-tip 双门

[PR #271](https://github.com/NoctilumeDev/VeriTrail/pull/271)保持精确 base/head、单提交与双文件 scope，
无 review thread。original Public CI `37844968094` attempt 1 绑定候选 head，7/7 jobs 全部 SUCCESS。

PR 经 phase-one pull-request rule ordinary merge 为：

```text
merge   = ebc5d7f5084b1a4dae3c3a211a4e82e78c6bbc78
parents = 685b077203c4c9b74a1ef14649a4ee5f8d16d82c
          4b262eb24e101d8bfc7605b8a7a14ce0b15386fe
tree    = 7d7f9ed1ed9a8b7c7bc50ff843da182f77d680b4
```

merge tree 与 candidate tree 相同。新的 exact maintenance tip 自己产生：

```text
Public CI     37846426640  attempt 1  7/7 SUCCESS
Browser Smoke 37846426876  attempt 1  1/1 SUCCESS
```

两条均为 `push` event 并绑定 `ebc5d7f...`；PR run 不替代 exact-tip run。

## 5. phase-two ruleset 读回

exact-tip 双门闭合以后，同一 ruleset `24216773` 被升级并独立从 ruleset API 与 branch-effective-rules API
读回。当前事实为：

```text
name        = Protect Core 0.12 maintenance branch
target      = refs/heads/core-0.12-maintenance
enforcement = active
bypass      = none
delete      = denied
non-ff      = denied
pull request required
current user can bypass = never
```

required status checks 精确为：

```text
Python 3.10 on Windows
Python 3.13 on Windows
Wheel-only first run on Python 3.10
Wheel-only first run on Python 3.13
E3 0.2 release download acceptance
Workbench tests, lint, build, and audit
Starter PASS/FAIL golden path
```

`strict_required_status_checks_policy = true`，`do_not_enforce_on_create = false`。phase-two request bytes 的
SHA-256 为 `88ad0ec028cc0d536a70cf7b833feb61481690b8cca76ee73fa00104c0d97a2a`。最终 reconciliation 在
Python 3.10 / 3.13、normal / `-O` 四格逐字节一致 PASS；manifest bytes SHA-256 为
`325848797652FA8C68E02C9C80BA2819391F355F25D8363BF4730CBBA9392401`。

## 6. 保留的失败与非资格观察

以下身份继续保留，后继成功不改写它们：

- PR #252 的 environment-qualified failure、PR #264 original Public CI 的 dependency-drift FAILURE，以及两次旧
  workflow-bootstrap 本地失败；
- 本轮 PowerShell inline expression、system Python 缺少 PyYAML、browser summary shape 与首次 premerge
  full-index diff byte-definition 错误；它们都在 candidate bytes 之外停止；
- Codex PR Artifact attachment 因 thread attachment identity 超过 100 被拒；PR #271 与 GitHub gates 不受影响。

首次 premerge reconciler 没有产生资格 manifest；修正 byte definition 后的新四格输出才取得 PASS。没有增大预算、
删除测试、改 head、rerun GitHub Actions 或把 setup error 写成产品失败。

## 7. 本发布自己的资格门

本文与 README、AGENTS、milestones 的 final bytes 只发布第 1–6 节事实。生效链固定为：

```text
final-byte documentation gates
    -> original PR Public CI
    -> protected main merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback
       README / doc223 / doc237 / doc238 / milestones
    -> public raw bytes equal exact Git blobs
    -> independent Core and source-byte reconciliation
    -> target qualified state takes effect
```

任一非成功 observation 必须保留自己的 Plan/session/attempt 和 cause boundary；诊断或后继 PASS 不替代它。

## 8. 后继停止线

本发布闭合只证明 M0 workflow bootstrap 与 phase-two governance 已取得资格。它不证明 0.12.3 backport、版本升级、
release candidate、tag、Release、资产或 public product readback 已经开始。

闭合以后必须返回 CONTROL LOOP，重新核对 maintenance tip、phase-two ruleset、并行 PR、dependency advisory、
文档 223 §2 / §6 / §12 与 current source correction。只有这些前提仍成立，才能从 `ebc5d7f...` 创建 fresh M1
topic branch，并且只施工文档 223 已授权的 0.12.3 backport / release-candidate scope。

Parse / Fact / Coverage、public 0.13.x、main consumer migration 与 `DECLARED_CLAIM_FIDELITY` 继续未获授权。
