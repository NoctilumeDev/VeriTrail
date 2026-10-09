# M10 required Starter lane 迁移资格发布

日期：2026-10-09

> 状态发布目标：
> `M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED /
> M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE /
> CORE_0_12_3_RELEASED /
> CORE_0_12_3_PUBLIC_READBACK_COMPLETE /
> CORE_0_12_3_MAINTENANCE_FROZEN /
> W1_REQUIRED_STARTER_LANE_MIGRATION_QUALIFIED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED`
>
> 状态发布基线：`main@594f1b10c2e441b7e73bd607d4d3d2623afd3704`，Git tree
> `59aa0c140d923160f92104316ef6200e8db4ee9e`
>
> 影响层级：`L0_DOCUMENTATION + L2_WORKFLOW_CONSUMER_IDENTITY`。本文只发布[文档 223](223-m10-browser-host-socket-classification-correction-release-consumer-contract.md)
> 第 8、9、12 节定义的 W1 consumer migration 事实；当前候选不修改 runtime、tests、workflow、timeout、retry、
> required-check、Release、Schema、Parse、Fact、Coverage 或 persistence。

## 1. 发布对象与条件状态

[文档 239](239-core-v0.12.3-release-readback-facts.md)已经把 Core 0.12.3 的 maintenance source、受保护 tag、
非 Latest Release、四项 assets 与匿名产品读回发布成 qualified history。返回 CONTROL LOOP 后，public release
coordinate、并行 PR 与文档 223 §8–9 仍支持一条更窄的后继 seam：只迁移 main 上 required Starter golden path 的
consumer identity。

本文自己的 final bytes、original PR Public CI、受保护 `main` 合入、new exact-main Public CI + Browser Smoke、
fresh anonymous installed-product readback 与 independent reconciliation 全部闭合后，以下目标才成为当前事实：

```text
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_QUALIFIED
M0_MAINTENANCE_PHASE_TWO_RULESET_ACTIVE
CORE_0_12_3_RELEASED
CORE_0_12_3_PUBLIC_READBACK_COMPLETE
CORE_0_12_3_MAINTENANCE_FROZEN
W1_REQUIRED_STARTER_LANE_MIGRATION_QUALIFIED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
```

最后门闭合以前，这些 marker 只是条件化 publication bytes。W1 workflow 已经合入并通过自己的 exact-main 双门，
不等于本文的公开状态发布已经生效。

## 2. W1 candidate 与边界

W1 candidate 的不可移动坐标为：

```text
base commit = c1e0318827162c7302e2a4bf4f8a83742f51cfbc
head commit = ecc09bcb1d278a399cdc2685dcdb1f9110122283
head tree   = 59aa0c140d923160f92104316ef6200e8db4ee9e
PR          = #275
changed     = .github/workflows/ci.yml only
diff        = +5 / -5
```

candidate 只修改独立 top-level job `Starter PASS/FAIL golden path`：

```text
public wheel URL
    v0.12.2 -> v0.12.3

wheel SHA-256
    3a42f28d... -> 360add85...

expected installed Core version
    0.12.2 -> 0.12.3
```

job name、15 分钟 containment、real PASS / intentional FAIL、Catalog、Workbench、cleanup 与 failed-evidence upload
保持原义。Python matrix 内 `Run Starter and Authoring Skill 0.2.0 on their declared Core 0.12.2 lane` 是冻结的
compatibility floor，不属于 W1 required consumer migration，因此继续固定 0.12.2 URL、SHA-256 与 version checks。

这一区分同时禁止两个错误结论：

```text
required golden path 已迁移
    ≠ Starter / Authoring compatibility floor 已上调

compatibility floor 仍是 0.12.2
    ≠ required golden path 仍消费 0.12.2
```

## 3. candidate 本地产品 witness

candidate final workflow 的本地 witness 使用 public Core 0.12.3 wheel 与 Starter 0.2.0，在 fresh Python 3.13 venv
中执行真实 `starter_single_webapp_acceptance.py`：

- public Core wheel SHA-256 等于
  `360add853dbaf3bbd18b51d21b494b20891010c6f1bc4b122b9e87d77ce53308`；
- Core 0.12.3 与 Starter 0.2.0 均从声明的非工作区安装位置加载；
- expected PASS Run 与 intentional FAIL Run 均按合同成立；
- Catalog 为两条 Run、零 issue；desktop/mobile 六张截图存在；
- console、HTTP、page 与 request failure 均为零；application/Catalog 端口释放，owned residue 为零；
- Workbench fresh `npm ci`、build 与 audit 0 vulnerabilities 成立。

local record `w1-local-qualification.json` 中 acceptance projection 的 SHA-256 为
`ab390ce6bcd6db1183eda2e8d31c3e202894708e4e98a7ba0da272bef91f8f9c`；candidate workflow SHA-256 为
`ad85f4755d6b5c5605806960a6a12788a403de99a17e13bab1b3a0ce2c6967e7`。这些 witness 只证明候选字节的
可执行性，不替代 PR、merge、exact-main 或 public status readback。

## 4. original PR 与 exact-main 双门

[PR #275](https://github.com/NoctilumeDev/VeriTrail/pull/275)保持单提交、单文件与精确 base/head；没有 review
thread。original Public CI `37868238477` attempt 1 绑定 `ecc09bcb...`，11/11 jobs 全部 SUCCESS，其中
`Starter PASS/FAIL golden path` 实际消费 public 0.12.3 coordinate 并成功。

ordinary merge 形成：

```text
main commit = 594f1b10c2e441b7e73bd607d4d3d2623afd3704
main tree   = 59aa0c140d923160f92104316ef6200e8db4ee9e
parent 1    = c1e0318827162c7302e2a4bf4f8a83742f51cfbc
parent 2    = ecc09bcb1d278a399cdc2685dcdb1f9110122283
```

merge tree 与 candidate tree 相同。new exact-main Browser Smoke `37870151759` attempt 1 为 1/1 SUCCESS；
Public CI `37870151887` attempt 1 为 11/11 SUCCESS。两条 run 的 `head_sha` 都是 `594f1b10...`，没有 rerun。

## 5. fresh anonymous status readback 与 reconciliation

exact-main 双门闭合后，fresh readback 清除了 `GH_TOKEN`、`GITHUB_TOKEN` 与 enterprise token 环境，并从公开
raw/API 路径独立取得：

- exact-SHA `.github/workflows/ci.yml`；
- PR #275 merge facts；
- Public CI `37870151887` 及其 11 jobs；
- Browser Smoke `37870151759` 及其唯一 job；
- public `v0.12.3` Release 与 wheel digest。

全部请求为 HTTP 200。public workflow raw bytes 与 exact Git blob 均为 41,603 bytes，SHA-256 同为：

```text
ad85f4755d6b5c5605806960a6a12788a403de99a17e13bab1b3a0ce2c6967e7
```

reconciliation 机械确认：

1. golden-path job 名与 15 分钟 containment 不变；
2. golden-path block 精确选择 public Core 0.12.3 URL、qualified SHA-256 与 version checks，且不残留 0.12.2；
3. Python matrix 的 declared compatibility block 仍精确选择 0.12.2 URL、原 SHA-256 与 version checks；
4. PR #275 base/head/merge 与 one-file `+5/-5` scope 一致；
5. exact-main Public CI 为 attempt 1、11/11 SUCCESS，且 Starter golden path SUCCESS；
6. exact-main Browser Smoke 为 attempt 1、1/1 SUCCESS；
7. public v0.12.3 Release 仍为非 draft、非 prerelease，wheel digest 与 workflow pin 一致。

Python 3.10 / 3.13、normal / `-O` 四格对同一 retained public evidence 生成逐字节相同的 canonical JSON：

```text
size    = 2897 bytes
sha256  = 86dc70f0d5a7b31bb5c30a7f13baf163ca3a7f4e44e10ece4cdc7d8b29e8c32a
result  = PASS
```

## 6. 保留的失败与非资格观察

后继 PASS 不改写以下身份：

1. outer-loop 首次使用不受支持的 `gh release view --json isLatest` 字段，以 read-only `SETUP_ERROR` 停止；
   后继改用 public Release REST 字段重新观察，没有改变 Release；
2. Codex PR Artifact attachment 因 thread attachment identity 超过 100 被拒；PR #275 与 GitHub gates 不受影响；
3. status reconciliation launch attempt 1 因 PowerShell launcher 参数错误，在读取 evidence 前以 `SETUP_ERROR` 停止；
4. reconciliation attempt 2 的 workflow block parser 把缩进 step 误认成下一个 top-level job，以
   `EVIDENCE_TOOLING_ERROR` 停止；public workflow bytes 未改变，fresh attempt 3 才取得四格 PASS；
5. 托管 worktree 创建从父目录调用，返回 `Not a git repository`；后继 checkout 由 VeriTrail repo 创建；该
   unmanaged checkout 不能附加为 Codex managed worktree。两次都是 publication setup error，不是产品 observation。

所有 retained evidence 位于仓库外的 machine-local evidence roots；本文只保存稳定 identity、分类与摘要，不把
主机绝对路径写入公开文档。

## 7. 本发布自己的资格门

本文与 README、AGENTS、milestones 的 final bytes 只发布第 1–6 节事实。生效链固定为：

```text
final-byte local documentation gates
    -> original PR Public CI
    -> protected main merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback
         README / doc223 / doc239 / doc240 / milestones / AGENTS
    -> public raw bytes equal exact Git blobs
    -> independent Core and source-byte reconciliation
    -> target qualified state takes effect
```

任一非成功 observation 必须保留自己的 Plan、session、attempt 与 cause boundary；诊断或后继 PASS 不替代它。

## 8. 后继停止线

本文闭合只证明 W1 required Starter consumer identity 已迁移到 qualified public Core 0.12.3，并且迁移后的 main
取得自己的 exact-main end-to-end qualification。它不证明：

- Starter / Authoring 的兼容性底线已从 0.12.2 上调；
- Parse private implementation 已获得授权或 PR #243 可以重开；
- Parse-to-Fact correction、Fact fulfillment、Coverage、Schema、publisher 或 Bundle 已开始；
- Language Support persistence 已被选择；
- `DECLARED_CLAIM_FIDELITY` 已进入 R1 normative surface。

最后门闭合以后必须返回 CONTROL LOOP，重新绑定新的 exact main、读取 frozen Parse contract 与文档 219–221、
核对并行 PR 和保留反例，再判断 Parse private implementation authorization 是否仍是最小合法问题。W1 qualified
只恢复这次重审资格，不预先决定结果。

## 9. 当前 final-byte 本地证据

候选四文件已经完成两套 Python normal / `-O` 的 Markdown + Hygiene 四格：

- exact staged scope 为 README、AGENTS、本文与 milestones；
- 620 个 local Markdown links 逐项解析到 repository 内存在的目标；
- UTF-8 无 BOM、LF/final LF、balanced fences、required markers 与敏感路径检查全部 PASS；
- `git diff --cached --check` PASS；
- 四格 canonical output 逐字节一致；
- `scripts/check_hygiene.py --local` 四格均为 `Residual Hygiene: PASS`，surface files 为 825，active Markdown
  entries 为 6，本 worktree 没有已知 local residual。

这些本地门只使 publication candidate 具备提交资格；它们不替代 original PR、merge、exact-main、fresh
installed-product readback 或 independent reconciliation。
