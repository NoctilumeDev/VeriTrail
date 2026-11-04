# R1 Workbench dependency audit recovery candidate

日期：2026-11-04

> 候选状态：`R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@2e9e5fbb56c84152de6a90be535345666becb733`，tree
> `be764de0a27d1b61cc1f0d51f14a29ad3894ce58`。
>
> 上游：[post-terminal Fact dual-successor private implementation feasibility audit](342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md)。
>
> 影响：`L1_MAINTENANCE / WORKBENCH_DEPENDENCY_BOUNDARY_ONLY`。本文恢复既有required Workbench
> dependency audit，不修改该oracle、workflow、Workbench source/tests、R1合同/runtime、Schema、Fact/Relation/Coverage
> semantics或任何public surface，也不授予private implementation authority。

## 1. 触发事实与边界归类

文档342已经完成自己的local/original PR/protected merge/exact-main双门、fresh anonymous installed-product readback、
independent reconciliation与finite closeout，因此是`FEASIBILITY_AUDITED / QUALIFIED_HISTORY`。基于该新事实建立的第一次
docs-only implementation authorization publication使用doc343身份；PR #395的exact坐标为：

```text
base = 2e9e5fbb56c84152de6a90be535345666becb733
head = a9824e8451cc61242884cefb23b6c772aba07bee
tree = 0725a796cbecda85397969c4762ce6d488b11a64
scope = README.md / AGENTS.md / docs/343... / docs/milestones.md
```

其original Public CI `41811545926` attempt 1真实结束为10个执行job中的9 SUCCESS、1 FAILURE，另有1个downstream job
SKIPPED。唯一失败job `126511760426`是required `Workbench tests, lint, build, and audit`；test、lint与build已经通过，
`npx --yes npm@11.19.1 audit --audit-level=moderate --registry=https://registry.npmjs.org`观察到16个moderate advisory后失败。
PR #395没有rerun，已经关闭且未合并；doc343继续只属于该失败candidate，不能在main复用编号、内容资格或状态身份。

同一时刻从clean exact base `2e9e5fb… / be764de…`、未修改的lock
`sha256:bd3bd3d6e8e6aba77ee7b02174fca07aee91d5ccc0deca16aac04be159d1880c`运行相同live audit，也得到16个
moderate advisory。由此只能成立：

```text
PR #395 original required gate failure = TRUE
authorization content failure established = FALSE
candidate regression established = FALSE
foundation dependency audit failure reproduced on exact base = TRUE
external advisory activation timing/root cause = UNKNOWN
```

后继维护资格不能覆盖、解释或回填#395，也不能把exact-base复现变成authorization PASS。

## 2. 最小恢复面

候选只修改`web/package.json`与npm 11.19.1生成的`web/package-lock.json`：

| 对象 | 候选值 | 责任 |
| --- | --- | --- |
| direct dev dependency | `glob@14.0.3` | 为Workbench dev graph提供单一patched exact coordinate |
| direct dev dependency | `minimatch@11.0.4` | 为Workbench dev graph提供单一patched exact coordinate |
| npm override | `glob: 14.0.3` | 约束`js-beautify`等transitive path，不依赖各upstream range碰巧收敛 |
| npm override | `minimatch: 11.0.4` | 约束ESLint、TypeScript ESLint、editorconfig与glob path |

最终`package.json`与lock SHA-256分别为：

```text
edcb01369745be8eba9a83462f47a26d861e07cae6a64e974e2e58d40ad71ab5
ff6b4bb86dbe3c369d29f6230633b7db57c73a650ddc3fe923e6d5c821aa9904
```

lock semantic diff覆盖39个package path；它把相关graph收敛到`glob@14.0.3`、`minimatch@11.0.4`与其必要的
`path-scurry@3.0.0`，移除不再可达的旧transitive nodes。没有更新Vue、Vite、Vitest、ESLint、TypeScript、jsdom或任何
Workbench runtime source；没有修改`.github/workflows/ci.yml`，moderate audit命令、level与registry保持原样。

## 3. 本地资格与独立反例

仓库required Workbench lane明确使用Node 22。候选在Node `v22.23.4`与npm `11.19.1`下fresh运行：

```text
npm ci                                            PASS
14 files / 179 Workbench tests                    PASS
eslint --max-warnings=0                           PASS
type-check + production build                     PASS
npm audit --audit-level=moderate                  PASS / 0 vulnerabilities
npm ls glob minimatch --all                       PASS / all relevant paths deduped
```

Node 22 qualification record SHA-256为
`13781a78e2e0c5ea29fd705ce8557ca372b98b7463c6fd526849aa225162edb1`。host Node `v24.14.0`的独立同范围
qualification也全部PASS，record SHA-256为
`baeb2a2fc9b2cac33984e8758fcc4ca1a7190d085934683d510f34799a1f837e`。这些PASS只证明当前candidate未被声明的
Workbench门击穿，不把live registry未来状态冻结成永久事实。

额外Node `20.19.0` / npm `11.19.1`诊断在candidate上出现6 files failed、79 tests failed，统一错误为WebCrypto
`SubtleCrypto.digest`拒绝另一个realm的`ArrayBuffer`。同一个bounded命令随后在clean exact base得到完全相同的6/79计数与错误；
comparison record SHA-256为
`9776b0ac67e6d4701df482b795a56f3c73abd3ebd5a781cb302316f0a2523c6d`。因此Node 20 candidate regression
`NOT_ESTABLISHED`，底层test-realm原因保持`UNKNOWN`。该失败是保留的non-qualifying diagnostic；它不被Node 22 PASS覆盖，
也不用于弱化或替换required Node 22 lane。

## 4. 保留的setup与candidate history

以下本地身份继续保留在独立evidence root，不删除、不覆盖，也不冒充产品失败：

- override-only lock refresh、targeted update、force refresh与`--no-save`均没有形成可用lock；attempt 1还得到`npm ci`
  lock/package mismatch；
- fresh lock attempt 5可通过audit但改变146个package path，因scope过宽未采用；初次wrapper session-id捕获失败保留；
- direct-pin attempt 6第一次在错误workdir生成8-package setup project，正确隔离后又因caret direct dependency与exact override
  `EOVERRIDE`；
- direct-pin attempt 7再次误入evidence root并覆盖attempt 6 setup byproduct；原字节未在覆盖前封存，后继不得声称恢复；
- repo root误生成的88-byte空lock已经移入evidence owner，不在candidate scope；首次adoption因预期hash错误安全停止；
- 首次local qualification因Git porcelain leading-space parser错误在npm前停止；PowerShell dependency-tree、registry partial、
  workflow wrong-path与`gh pr diff --stat` unsupported flag均保留；
- Node 20 candidate与exact-base diagnostics均保留为FAILED/NON_QUALIFYING，底层原因`UNKNOWN`。

这些记录的effect均不允许被后继PASS重写。primary `audit.json`保持
`sha256:4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

## 5. 本candidate自己的资格链

tracked scope只允许：

```text
README.md
AGENTS.md
docs/344-r1-workbench-dependency-audit-recovery.md
docs/milestones.md
web/package.json
web/package-lock.json
```

final bytes必须重新通过required Node 22 Workbench test/lint/build/unchanged moderate audit、exact dependency tree、
`git diff --check`、UTF-8/LF/final-LF、Markdown links/fences/headings、global/local hygiene、exact scope、#395与全部保留失败
identity、doc342资格事实、remote main与primary audit continuity。之后资格链仍是：

```text
final local gates
    -> original PR required gates（禁止rerun洗白）
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc342 / doc344 / milestones readback
    -> independent reconciliation + finite closeout
    -> R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何门失败都保留原身份并停止；later PASS不能回填#395或本candidate的任一失败attempt。

## 6. 当前状态与停止线

在本文完整资格链闭合以前只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_AUTHORIZATION_PR_395_FAILED_CLOSED_UNMERGED
R1_WORKBENCH_DEPENDENCY_AUDIT_RECOVERY_CANDIDATE_NOT_QUALIFIED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

本维护candidate只修复required Workbench dependency audit的exact bytes。全部门闭合后也不恢复#395、不复用doc343、不直接授权
runtime；必须返回CONTROL LOOP，从新的exact main建立新的versioned docs-only implementation authorization successor并重新取得完整资格。
