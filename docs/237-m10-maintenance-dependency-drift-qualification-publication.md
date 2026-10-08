# M10 maintenance dependency drift 资格发布

日期：2026-10-09

## 1. 发布对象与生效条件

本文只发布[文档 235](235-m10-maintenance-dependency-drift-contract.md)与
[文档 236](236-m10-maintenance-dependency-drift-contract-freeze-publication.md)所约束的 dependency-drift correction
资格。本文自身的 final-byte local gates、original PR Public CI、受保护 `main` 合入、new exact-main Public CI /
Browser Smoke、fresh anonymous installed-product readback 与 independent reconciliation 全部成立后，以下目标才成为
有效状态：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_QUALIFIED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_NOT_STARTED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

写出 target marker 不代替这些门。dependency qualification 只证明 exact maintenance tip 上的一次有界修正已经按冻结
合同闭合；它不自动授权 workflow bootstrap、phase two、release、consumer migration 或 R1 后继施工。

## 2. 合同冻结 source state

文档 236 的独立冻结发布已经完成：

| gate | identity | result |
| --- | --- | --- |
| freeze PR | [#268](https://github.com/NoctilumeDev/VeriTrail/pull/268)，head `a55c9bf5c66d8808cb728392b413249e0b158eea` | exact 5-file docs-only diff |
| original Public CI | `37823219183`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `295afd0637385068e92b581c837249166bcf9919` | ordinary merge |
| exact-main Public CI | `37826445149`，attempt 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `37826445084`，attempt 1 | `1/1 SUCCESS` |
| installed-product readback | README / doc235 / doc236 / milestones | four independent `PASS` |

五份 public raw bytes 与 exact Git blobs `5/5 MATCH`。最终 independent reconciliation：

```text
sha256_json  = 162cabd962e192568c8405f65cb0486e1748038c9047a49858eda72dc97de847
sha256_bytes = e20d4e9aa9aacc07fe9b48603c722940ef0b35b37d6bc43388e2ba7fae806eed
```

第一次错误地对 no-argument public-byte checker 使用 `--help`，命令实际执行且因未设置代理发生 network reset；另一次
reconciliation 使用了与 sealed summary creation-time label 不同的 target label。两次均发生在新 manifest 形成以前，
原 formal reports 不变；后继成功不覆盖这些 setup/evidence-tooling failure。合同因此已经 `FROZEN`，实现没有由冻结
自动开始。

## 3. Exact implementation source 与 candidate bytes

CONTROL LOOP 从 exact source state 重新确认：

| coordinate | value |
| --- | --- |
| contract main | `295afd0637385068e92b581c837249166bcf9919` |
| maintenance base | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` |
| base/final tree | `42732643af743ca4aa9e801d61e5b49a04c4f54f` / `eaf3314a60d3607f8d62920bd19553600326cd8b` |
| final lock blob | `297be5c0bcc30729c0f4c3f4322be74641b2a916` |
| final lock SHA-256 | `D9FBF89CA905EC2602B9956E986E24F74C38AAF4DE3EA960D1DBA3905EBD00A4` |
| phase-one ruleset | `24216773`，active、无 bypass、PR required |
| parallel maintenance PR | none |

host npm 为 `11.9.0`，因此施工只通过 process-local `npx npm@11.19.1` 使用冻结 tool identity；没有修改全局 npm 或
Git proxy 配置。两个独立 exact-base worktree、两个独立 cache 运行冻结的 package-name-only update，逐字节得到同一
lock bytes。candidate 只修改 `web/package-lock.json`，`68 insertions / 68 deletions`，完整 14-entry projection、Vue
peer dependency 与 root package projection 均和文档 235 一致。

最终 candidate bytes 串行完成：fresh `npm ci --ignore-scripts`、Workbench `14 files / 172 tests`、lint、type-check /
production build、moderate audit `0 vulnerabilities`、installed-tree projection、exact one-file diff 与
`git diff --check`。candidate commit：

```text
head   = 6efccfb89d362819d6deaaef1616fe221eae52b2
tree   = eaf3314a60d3607f8d62920bd19553600326cd8b
parent = 6ed18ae8b3d8b98b6e5be7af709aa868590ee914
```

## 4. Candidate qualification 与 protected merge

[PR #269](https://github.com/NoctilumeDev/VeriTrail/pull/269)绑定 exact base/head、1 commit、1 file 与 one-file lock
patch。candidate ref 上两条 fresh dispatch 为：

| workflow | run | event / attempt | exact head | denominator | result |
| --- | --- | --- | --- | --- | --- |
| Public CI | `37831705180` | `workflow_dispatch` / 1 | `6efccfb89d362819d6deaaef1616fe221eae52b2` | 7/7 | SUCCESS |
| Browser Smoke | `37831710041` | `workflow_dispatch` / 1 | `6efccfb89d362819d6deaaef1616fe221eae52b2` | 1/1 | SUCCESS |

两条 run 是 exact-head witnesses，不冒充 original PR required checks。fresh pre-merge reconciliation 确认 PR
`OPEN / CLEAN / MERGEABLE`、0 unresolved review threads、base/head/patch/lock/ruleset 与 maintenance tip 均未漂移。
ordinary merge 形成：

```text
merge   = 685b077203c4c9b74a1ef14649a4ee5f8d16d82c
tree    = eaf3314a60d3607f8d62920bd19553600326cd8b
parent1 = 6ed18ae8b3d8b98b6e5be7af709aa868590ee914
parent2 = 6efccfb89d362819d6deaaef1616fe221eae52b2
```

protected maintenance ref 随后精确指向 merge commit；parent1..merge 仍只修改 lockfile，ruleset 保持 active、无 bypass、
PR required。

## 5. Exact maintenance-tip qualification

candidate runs 没有转移给 merge tip。新的 exact `core-0.12-maintenance@685b077...` 取得两条 fresh run：

| workflow | run | event / attempt | exact head | denominator | result |
| --- | --- | --- | --- | --- | --- |
| Public CI | `37832912010` | `workflow_dispatch` / 1 | `685b077203c4c9b74a1ef14649a4ee5f8d16d82c` | 7/7 | SUCCESS |
| Browser Smoke | `37832916430` | `workflow_dispatch` / 1 | `685b077203c4c9b74a1ef14649a4ee5f8d16d82c` | 1/1 | SUCCESS |

maintenance ref 在触发前、触发后和终结后保持 exact merge SHA。Browser Chromium 安装约十一分钟，但仍在既有 25 分钟
workflow containment 内成功；没有修改 timeout，也没有借用 candidate observation。

## 6. 独立 reconciliation 与保留观察

独立 verifier 核对合同、两次 reconstruction、local gates、candidate commit/PR/ref、ruleset、ordinary merge topology、
四条 workflow runs、job denominators、logs / Artifact metadata、maintenance ref 与 final lock bytes。canonical
manifest：

```text
sha256_json  = 105a44f4342f0496e76d4c056fbe7e91cc322a62cdf546e06894f08c5c8ab547
sha256_bytes = 899b0571ea644ad99441af5ea6c9ebebf4510c187a6f6547b885241f2a8d1523
evidence     = 48 files
```

以下 observation 按原身份保留：

- PR #264 / Public CI `37795167502` attempt 1 = `FAILURE`，未合入、未 rerun；
- 首次 read-only audit 继承 host npm mirror，security endpoint 返回 404，分类为 environment registry configuration error；
- 后继 official-registry audit 在 exact base 重新观察到 `1 moderate / 3 high`，不覆盖前一项；
- projection helper extra-path `FileNotFoundError` 与 final-audit PowerShell unmatched-parenthesis 均为 setup error；
- 两条 candidate dispatch 已创建，但第一次 created-at filter 返回空数组；run identity 由命令返回 URL 和 direct API 恢复；
- PR Artifact attachment 因当前 task 已有过多 attachment identity 失败，未改变 PR 或产品资格。

上游 #252、exact-version `EUPDATEARGS`、projection helper `KeyError` 与 doc228 resource stops 继续原样保留。后来成功没有
把任一事件改写成“未发生”，也没有把环境/setup failure 冒充产品 failure。

## 7. 本 publication 的 final-byte local gates

本 publication 只修改 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。文档 235 / 236、dependency、
maintenance ref、workflow、ruleset、runtime、tests、Schema、publisher 与 Bundle 保持不变。

提交前必须在最终字节上完成本层适用的 CPython 3.10 / 3.13、normal / `-O` Markdown regression、relative links、
UTF-8 无 BOM、LF/final LF、fence/heading、required markers、敏感路径、exact four-file scope 与
`git diff --check`。本地门不能替代 original PR checks。

最终四文件字节已经完成 CPython 3.10.6 / 3.13.13、normal / `-O` 四格 `tests.test_markdown`，各格
`4/4 PASS`。静态门检查 265 份 Markdown、3485 个 headings 与 1186 个 relative links；UTF-8 无 BOM、LF/final
LF、balanced fences、required markers、敏感路径、exact four-file scope 与 `git diff --check` 均成立。

```text
final-byte local documentation gates
    -> original PR Public CI
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback:
         README / doc235 / doc236 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target qualified state takes effect
```

任一非成功观察都必须保存原 identity。不得 rerun 洗白、复用文档 236 的 Evidence、拿相同内容或 digest 继承资格，
也不得在观察以后修改发布标准。

## 8. 后继停止线

最后门闭合后必须返回 CONTROL LOOP，从新的 exact main 重新核对 maintenance tip、ruleset、并行 PR、当前 advisory
surface，以及文档 223 / 224 / 225–227 的停止线。只有新证据仍证明 fresh workflow-only bootstrap 是当前最小合法
问题，才可用全新 branch/PR identity 进入其资格审计。

本文不授权修改 workflow/ruleset、重开 #252/#264、复用旧 bootstrap candidate、phase two、0.12.3 backport/release、
asset/public consumer migration、R1 Parse / Fact / Coverage、`DECLARED_CLAIM_FIDELITY` 或其他顶层轨。

发布原则为：**qualified correction 只属于 exact source、candidate、merge topology、exact-tip observations 与
reconciliation 共同闭合的世界；相同 lock bytes、版本或终态 PASS 不把 authority 转移到下一项施工。**
