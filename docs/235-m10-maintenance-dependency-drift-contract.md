# M10 0.12 maintenance dependency drift 最小合同

日期：2026-10-09

> 状态目标（仅后继独立冻结发布的最后门闭合后生效）：
> `M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN /
> M0_MAINTENANCE_DEPENDENCY_DRIFT_IMPLEMENTATION_NOT_STARTED`。本文只冻结 dependency drift 的 exact source、
> package-name-only 构造、14-entry lock closure、review、manual-dispatch witness、受保护合入、exact-tip
> reconciliation 与失败语义。本文不是 dependency candidate，不创建 branch / PR，不运行 workflow，不修改
> maintenance line，也不授权 workflow bootstrap、0.12.3 release、Parse / Fact / Coverage 或 claim fidelity。

## 1. 合格输入与合同问题

[文档 234](234-m10-maintenance-dependency-drift-precontract-audit.md)已经完成自己的资格链：

| gate | identity | result |
| --- | --- | --- |
| candidate PR | `#266`，head `0bb60c0b51c1abcaa0877ffda6a62c9216fecc48` | exact 4-file docs-only diff |
| original Public CI | `37808837143`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `7cf409940339d4068c3effd9e6d4deaca0c7861b` | merged |
| exact-main Browser Smoke | `37811755526`，attempt 1 | `1/1 SUCCESS` |
| exact-main Public CI | `37811755532`，attempt 1 | `11/11 SUCCESS` |

因此 precontract boundary 已成为 qualified history。当前最小合同问题是：

> 怎样只改变 exact 0.12 maintenance source 的一个 lockfile，以不可借用的 exact-head / exact-tip
> `workflow_dispatch` observations 证明新的 dependency qualification，同时保留 PR #264 的原始失败，且仍由
> phase-one ruleset 保证 maintenance tip 只能经 PR 改变？

合同只接受以下顺序：

```text
exact protected maintenance tip
    -> fresh one-file dependency-drift candidate
    -> deterministic lock reconstruction and local review
    -> protected PR identity
    -> exact candidate-head Public CI + Browser Smoke dispatch witnesses
    -> unchanged PR/ruleset reconciliation
    -> ordinary merge commit
    -> exact maintenance-tip Public CI + Browser Smoke dispatch witnesses
    -> independent reconciliation
    -> return to CONTROL LOOP
```

## 2. 冻结的 source 与治理输入

dependency candidate 开始以前必须重新读回并精确匹配：

| coordinate | frozen value |
| --- | --- |
| maintenance ref | `refs/heads/core-0.12-maintenance` |
| maintenance base commit | `6ed18ae8b3d8b98b6e5be7af709aa868590ee914` |
| maintenance base tree | `42732643af743ca4aa9e801d61e5b49a04c4f54f` |
| `web/package.json` Git blob | `b38efdf88c439528a5b8af799e7ab8935037b3fc` |
| base `web/package-lock.json` Git blob | `3b37cc4f29a74a370cd15e778953aedd372283b7` |
| base lock SHA-256 | `6A6F5D09C97B7C01501D04705575CDA11155840CF715EE88817711062A7EA01E` |
| Public CI workflow Git blob | `c094d2cb84a2147e2b8bba1a7e76f140905d1a4d` |
| Browser Smoke workflow Git blob | `413f35ad9f768eb323d0058b82bdd8eaca177be1` |
| phase-one ruleset | `24216773`，active |
| ruleset target | `refs/heads/core-0.12-maintenance` |
| bypass actors | empty；current user `never` |
| protected operations | deletion / non-fast-forward denied；PR required |
| required checks | none |
| open PRs into maintenance | `0` |

任一 source/blob/ref/ruleset coordinate 不匹配，当前合同实例不得继续。必须保留新观察并返回 CONTROL LOOP；不得把
drift 当成“仍是同一个 0.12 maintenance world”。ruleset 只拥有 merge governance。required checks 为空，因此它不能
证明 dependency candidate 合格；后文 manual dispatch runs 也不得冒充 original PR checks 或 required checks。

PR #264 必须继续保持：

```text
base    6ed18ae8b3d8b98b6e5be7af709aa868590ee914
head    585f98252d3c18727a0f19cb0eb1a28b362c9dc9
state   CLOSED / NOT MERGED
run     37795167502 / attempt 1 / FAILURE
scope   two workflow files only
```

不得 rerun、改 head、reopen、merge 或删除该失败身份。

## 3. 唯一允许的 dependency construction

从第 2 节 exact maintenance base 创建一个新的、未用于 #252、#264 或其他候选的 topic identity。固定工具与输入：

```text
Node
    v24.14.0

npm
    11.19.1

registry
    https://registry.npmjs.org

command, from web/
    npm update vue postcss-selector-parser source-map-js
        --package-lock-only
        --ignore-scripts
        --registry=https://registry.npmjs.org
```

`web/package.json` 必须保持第 2 节 blob 不变。禁止把 exact versions 写进 `npm update` 参数；npm `11.19.1` 已证明该
语法在写入前以 `EUPDATEARGS` 失败。三个 package name 只是 selection seed，允许输出由下一节完整 14-entry closure
定义，不能把三个名字偷换成变化 denominator。

构造完成后，working tree 只允许修改：

```text
web/package-lock.json
```

最终 lock identity 必须同时满足：

```text
Git blob
    297be5c0bcc30729c0f4c3f4322be74641b2a916

SHA-256
    D9FBF89CA905EC2602B9956E986E24F74C38AAF4DE3EA960D1DBA3905EBD00A4

exact diff
    web/package-lock.json only
    68 insertions / 68 deletions
```

行数只作辅助 witness；one-file exact patch、parsed projection、Git blob 与 SHA-256 共同约束内容 identity。

## 4. 完整 canonical 14-entry projection

base 与 candidate 的 `packages` map 必须恰有下列 14 个 entry 不同。每个 entry 的 `version / resolved / integrity /
dependencies` 均属于冻结投影；未列出的字段不得改变。`dependencies` 用 key-sorted、compact canonical JSON 表示。

| entry | version | resolved | integrity | dependencies |
| --- | --- | --- | --- | --- |
| `node_modules/@vue/compiler-core` | `3.5.43` | `https://registry.npmjs.org/@vue/compiler-core/-/compiler-core-3.5.43.tgz` | `sha512-zdiLhnbe1QQqgDT8xZMpNmyqZ3qlI+/Q/FHQco57Kwl/b05HhCzN6eVGN9QU9rbga4CrS0H5SYY8VGHZCt/1Hg==` | `{"@babel/parser":"^7.29.8","@vue/shared":"3.5.43","entities":"^7.0.1","estree-walker":"^2.0.2","source-map-js":"^1.2.1"}` |
| `node_modules/@vue/compiler-dom` | `3.5.43` | `https://registry.npmjs.org/@vue/compiler-dom/-/compiler-dom-3.5.43.tgz` | `sha512-PEZoAk3NQmsn/ejMzSOCyTYqwGqczrWm70PuhBKjjv1+TCoQAaO/zOqNwjV+honlNstT5ILxtc+8r8UUfj+iEQ==` | `{"@vue/compiler-core":"3.5.43","@vue/shared":"3.5.43"}` |
| `node_modules/@vue/compiler-sfc` | `3.5.43` | `https://registry.npmjs.org/@vue/compiler-sfc/-/compiler-sfc-3.5.43.tgz` | `sha512-FCbrG3XNCRl+js3huuKx4IVHBLTvMkJhVepjbxSPu1gn4yWLaYtGNQdjJGZaMytXB6qb76qQDDmDSLy/vkmleQ==` | `{"@babel/parser":"^7.29.8","@vue/compiler-core":"3.5.43","@vue/compiler-dom":"3.5.43","@vue/compiler-ssr":"3.5.43","@vue/shared":"3.5.43","estree-walker":"^2.0.2","magic-string":"^0.30.21","postcss":"^8.5.28","source-map-js":"^1.2.1"}` |
| `node_modules/@vue/compiler-ssr` | `3.5.43` | `https://registry.npmjs.org/@vue/compiler-ssr/-/compiler-ssr-3.5.43.tgz` | `sha512-GF62orf7KiJX9RqrHNGrYBudsQGD0OhJ5nDs90O8UiDuS40+YMYomiXu6w6EuvtXuRDc3MSNis3EaaSKAVSWpg==` | `{"@vue/compiler-dom":"3.5.43","@vue/shared":"3.5.43"}` |
| `node_modules/@vue/reactivity` | `3.5.43` | `https://registry.npmjs.org/@vue/reactivity/-/reactivity-3.5.43.tgz` | `sha512-G/c9GyOZNI2jVaaS6OX1EF1SSFSv7H0ERqNTl4+DTFMlZmB5eVAB53aLQNam/7NL2NPtaDD7RdVrzf8uJzMuOA==` | `{"@vue/shared":"3.5.43"}` |
| `node_modules/@vue/runtime-core` | `3.5.43` | `https://registry.npmjs.org/@vue/runtime-core/-/runtime-core-3.5.43.tgz` | `sha512-hU6U6VnVhBGQDpvlnnDlIB8ZGJBiOcgk2lh/0InltHiz3D8oSkluvuvY+do1G2H3+udeKFsmaBlgVYP7gXQzEw==` | `{"@vue/reactivity":"3.5.43","@vue/shared":"3.5.43"}` |
| `node_modules/@vue/runtime-dom` | `3.5.43` | `https://registry.npmjs.org/@vue/runtime-dom/-/runtime-dom-3.5.43.tgz` | `sha512-Bb2Jc0YjjJdMt1SJmb9b2L/IWd3I8lIT9x9eS/xvvP9CiVgna0ffua74xKRmt4/uSJ+0r4iN8ex1jrqkhQGWQw==` | `{"@vue/reactivity":"3.5.43","@vue/runtime-core":"3.5.43","@vue/shared":"3.5.43","csstype":"^3.2.3"}` |
| `node_modules/@vue/server-renderer` | `3.5.43` | `https://registry.npmjs.org/@vue/server-renderer/-/server-renderer-3.5.43.tgz` | `sha512-l2Ygjv9NehV94PSBxNWsAHC0j/eIIKbn92mBuWXAPGLnn6HfJ6MH5ubsd+Nk0YoZ5FRuxWI1P2VSoh+dbPQhCQ==` | `{"@vue/compiler-ssr":"3.5.43","@vue/runtime-dom":"3.5.43","@vue/shared":"3.5.43"}` |
| `node_modules/@vue/shared` | `3.5.43` | `https://registry.npmjs.org/@vue/shared/-/shared-3.5.43.tgz` | `sha512-uksS7YGMR5NZyr4JNq0Rp+QyLns0ueaz20KwzIPW9R0LH1Vnt4E+XUM29PNseEbf1www2gOuhuDi5AKOIXag9Q==` | `{}` |
| `node_modules/nanoid` | `3.3.20` | `https://registry.npmjs.org/nanoid/-/nanoid-3.3.20.tgz` | `sha512-uKdg2G3GNCKQn9byYOpxbGqrT2fGO5KRt5J/8b3pok8rT6qxGWF6hxMyJiEYtAf+FVyYuD9hRaDqX5uPFYJ4ZQ==` | `{}` |
| `node_modules/postcss` | `8.5.29` | `https://registry.npmjs.org/postcss/-/postcss-8.5.29.tgz` | `sha512-49cGhUbXj8Qenv0iTMxA1cFBzxXoctpC9Ujd77t1WcbJIr6nF/eI7g/8MgxrYldFRuAXvja7xQRwavoW7kgrxQ==` | `{"nanoid":"^3.3.19","picocolors":"^1.1.1","source-map-js":"^1.2.2"}` |
| `node_modules/postcss-selector-parser` | `7.1.6` | `https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-7.1.6.tgz` | `sha512-7qASPzhKF2l2KLboRZux8CCTRMdGiV08vWmyKzPz22qZ7ZjQBOeY7rNzNoCLSUiftJ7HUq0GERHmxw/t0dCdMw==` | `{"cssesc":"^3.0.0","util-deprecate":"^1.0.2"}` |
| `node_modules/source-map-js` | `1.2.2` | `https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.2.tgz` | `sha512-KGj/8Y43x35aZVDtt+J4mK1hoLGHULMYfSkODJNQjNDC3oW1PqPoxMwo0pLUsWM/UEGzON/NxeHywEfNXNP3Vw==` | `{}` |
| `node_modules/vue` | `3.5.43` | `https://registry.npmjs.org/vue/-/vue-3.5.43.tgz` | `sha512-o5qZoksdnjIKvW1srZ3ab7pcDNYAerBjRe54D0LBLfRdCYFrSgBHVXokMas35czQc0//lmx4/tuY4ZNQ+Rf2Ng==` | `{"@vue/compiler-dom":"3.5.43","@vue/compiler-sfc":"3.5.43","@vue/runtime-dom":"3.5.43","@vue/server-renderer":"3.5.43","@vue/shared":"3.5.43"}` |

`node_modules/vue` 的 `peerDependencies` 还必须精确为 `{"typescript":"*"}`。root package projection 必须保持：

```json
{
  "name": "@veritrail/workbench",
  "version": "0.12.0",
  "dependencies": {"vue": "^3.5.41"},
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "@types/node": "^24.10.0",
    "@vitejs/plugin-vue": "^6.0.8",
    "@vue/test-utils": "^2.4.11",
    "eslint": "^10.8.1",
    "eslint-plugin-vue": "^10.10.0",
    "globals": "^17.11.0",
    "jsdom": "~29.1.1",
    "typescript": "~6.0.3",
    "typescript-eslint": "^8.67.0",
    "vite": "^8.2.2",
    "vitest": "^4.1.11",
    "vue-tsc": "^3.3.10"
  },
  "engines": {"node": "^20.19.0 || >=22.12.0"}
}
```

current main 的相似 dependency updates 不转移 source、construction、review、CI、merge 或 exact-tip authority。

## 5. Deterministic reconstruction 与 local gates

candidate commit 以前必须：

1. 从第 2 节 exact base fresh 执行第 3 节命令；
2. 保存 lock bytes/blob/SHA、14-entry projection、root projection 与 exact patch；
3. restore 到 exact base，再用 fresh install/cache-independent workspace 重复构造；
4. 两次输出逐字节相同，且都只修改一个 lockfile；
5. 在最终 candidate bytes 上串行完成下列 local gates。

| witness | required result |
| --- | --- |
| fresh `npm ci --ignore-scripts` | 252 packages added；253 audited；0 vulnerabilities |
| Workbench regression | 14 files；172/172 PASS |
| lint | PASS |
| type-check + production build | PASS |
| `npm audit --audit-level=moderate` | exit 0；0 vulnerabilities |
| installed tree | Vue family `3.5.43`；selector parser `7.1.6`；source-map-js `1.2.2`；PostCSS `8.5.29`；Nano ID `3.3.20` |
| projection reconciliation | exact 14 entries；root unchanged |
| exact tracked diff | `web/package-lock.json` only |
| `git diff --check` | PASS |

必须保存 Node/npm/registry、命令、开始/结束 UTC、exit code 与输出。`npm audit` 是有 observation time 的 registry
observation，不是 lock bytes 的永久安全证明；candidate-head 与 maintenance-tip Public CI 必须各自重新观察。

## 6. Candidate commit、PR 与 exact-head qualification

local gates 成立后只允许产生一个 one-file candidate commit。push 前后须保存 exact topic ref、commit/parent/tree、lock
blob/SHA、完整 patch、Git/GitHub ref 双读回与 repository/owner identity。随后打开 base 为
`core-0.12-maintenance` 的 ordinary PR，并 fresh 读回：

```text
state         OPEN
draft         false
base SHA      6ed18ae8b3d8b98b6e5be7af709aa868590ee914
head SHA      exact candidate commit
commits       1
changed files 1
diff          web/package-lock.json only
```

对 unchanged topic ref 创建两条 fresh `workflow_dispatch` run：

| workflow | required identity and denominator |
| --- | --- |
| Public CI | `.github/workflows/ci.yml`，blob `c094d2cb...`，attempt 1，exact branch/head，七项 jobs 全部 success |
| Browser Smoke | `.github/workflows/browser-smoke.yml`，blob `413f35ad...`，attempt 1，exact branch/head，`Production Workbench smoke` success |

Public CI 七项 denominator 为 Python 3.10、Python 3.13、两个 wheel-only、E3 download acceptance、Workbench 与
Starter golden path。每次 dispatch 前、触发后、终结后都必须 fresh 读回 topic ref；只接纳 API 返回
`head_sha == exact candidate head`、`event == workflow_dispatch`、`run_attempt == 1` 的 run。一个 workflow 的 PASS、
旧 run、push/schedule run、最近绿色 run或 attempt > 1 均不能替代所需 identity。

## 7. Merge 前 reconciliation 与 protected merge

两条 candidate runs 成功以后，merge 前必须 fresh 确认：PR/head/base/one-file patch/final lock hash 未变；topic ref 未移；
maintenance tip 仍为第 2 节 base；ruleset 仍 active/no bypass/PR required；review threads resolved；原始 run identity
仍是 attempt 1 success。任一漂移都使 merge authority 失效；不得 rebase 后借用旧 runs。

只允许 ordinary merge commit，不得 squash 或 rebase merge。合入后必须保存并核对：

- merge commit SHA/tree；
- first parent = exact pre-merge maintenance tip；
- second parent = exact candidate head；
- protected ref = exact merge commit；
- merge tree 中 lock blob/SHA = 第 3 节 identity；
- parent1..merge diff 仍只修改 `web/package-lock.json`；
- ruleset readback、merge API 与 PR terminal state。

base 移动、冲突解决字节、parent/tree/hash 漂移或非 ordinary merge 都必须保留观察并返回 CONTROL LOOP。

## 8. Exact maintenance-tip qualification

不得复用第 6 节 candidate runs。必须对新的 exact `core-0.12-maintenance` tip 创建 fresh Public CI 与 Browser Smoke
`workflow_dispatch` identities，并在触发前后及终结后读回 ref：

```text
event       workflow_dispatch
run_attempt 1
head_branch core-0.12-maintenance
head_sha    exact merge commit
conclusion  success
```

Public CI 七项 jobs 与 Browser Smoke 一项 job 必须分别全成功。branch 在 observation 期间移动时，旧 SHA 的 runs 仍保留
为历史，但不能资格化新的 tip。

## 9. Failure、drift 与历史身份

| observation | retained identity | required action |
| --- | --- | --- |
| construction syntax/setup error | 精确命令、阶段、exit/output | 若未写入则不伪装 candidate；归层后重审 |
| local gate non-zero | `LOCAL_GATE_FAILURE` 或精确 setup/resource 分类 | 保留输出；不弱化门 |
| registry/API/network error | `ERROR`，root cause 只在有证据时声明 | 不伪造 observation，不借替代路径 |
| topic/PR head drift | old runs 绑定 old head | new head 重走全部 candidate gates |
| run `failure` | `FAILURE` | 保留 run/log/Artifact；不 rerun 洗白 |
| run `cancelled` | `CANCELLED` | 不是 PASS，也不自动解释为产品失败 |
| attempt > 1 PASS | diagnostic / non-qualifying | 不能替代 fresh attempt-1 run |
| job denominator missing/skipped | incomplete qualification | 不缩小 denominator |
| ruleset/base/merge topology drift | merge authority invalid | 停止并返回 CONTROL LOOP |
| exact-tip run head != branch tip | observation 属于另一 coordinate | 不资格化当前 tip |
| advisory later changes | new timed observation | 不改写旧 PASS；重新判断当前 seam |

PR #264、exact-version `EUPDATEARGS`、projection helper `KeyError`、doc228 resource stops 及本合同产生的首个非成功
observation 都永久保留。后来成功不得删除或重新解释它们。

## 10. Retained evidence 与发布 authority

最少保留：

1. exact source commit/tree/blob、Git/REST ref readback 与读取时间；
2. ruleset JSON bytes 与关键 projection；
3. Node/npm/registry/command 与两次 reconstruction/local gate logs；
4. base/final lock bytes、blob/SHA、完整 14-entry/root projection 与 exact patch；
5. PR REST/GraphQL bytes、commits/files/diff、review/mergeability 与 base/head；
6. candidate/tip 四条 run 的 API bytes、jobs、attempt、timestamps、conclusions、logs/Artifact metadata；
7. merge response、parents/tree/ref/ruleset readback；
8. 所有 ERROR/FAILURE/CANCELLED/setup/resource identities；
9. 一份 canonical reconciliation manifest，把 candidate 与 tip evidence 分开列出。

npm registry、dependency producer、PR 或 workflow run 都无权自行发布“qualified tip”。只有本合同所有 gate 对同一 exact
identities 完成 independent reconciliation 后，才可在后继独立状态 publication 中条件化发布 dependency qualification。

## 11. 闭合后的 continuation 与明确禁止

第 3–10 节成立只证明：

```text
exact new core-0.12-maintenance tip
    has a qualified dependency-drift correction
```

它不自动授权 workflow bootstrap。闭合后必须返回 CONTROL LOOP，重新核对 tip、ruleset、并行 PR、advisory surface 与
文档 223/224 的停止线，再判断 fresh workflow-only candidate 是否仍是最小合法问题。

本文不得被解释为授权：

- 当前创建/push/delete dependency topic、PR，或运行/rerun/cancel dispatch；
- 修改 maintenance ref、ruleset、workflow、runtime、tests、timeout、retry 或 budgets；
- 重开、改 head、rerun、merge或删除 #252/#264；
- 弱化、跳过或重解释 audit；
- phase two、backport、version/tag/Release/asset/public readback、consumer migration；
- R1 Parse/Fact/Coverage/claim-fidelity 施工，或修改其 frozen contract/Schema/publisher/Bundle。

## 12. 合同候选资格与冻结停止线

本文 final-byte qualification 已经闭合：

| gate | identity | result |
| --- | --- | --- |
| candidate PR | `#267`，head `8ed2f6f0e02e0a7a1e9f0d8006944e02eae1bb75` | 1 commit / 4 files |
| original Public CI | `37815845110`，attempt 1 | `11/11 SUCCESS` |
| protected-main merge | `933df49e61b8a5d3e3856afa648d27c1c21f5529` | ordinary merge |
| exact-main Public CI | `37818894300`，attempt 1 | `11/11 SUCCESS` |
| exact-main Browser Smoke | `37818894374`，attempt 1 | `1/1 SUCCESS` |
| installed-product readback | README / doc234 / 本文 / milestones | four independent `PASS` |
| public source bytes | AGENTS / README / doc234 / 本文 / milestones | `5/5 MATCH` |

independent reconciliation manifest：

```text
sha256_json  = 1bea6a3b59b452d7debda2b4778826a031e0ae2737e6523a19d55b02cac92960
sha256_bytes = ddbe3925167ae99b1babcc7ff47dcfbca2560bd3802378b31847f799f63ddda3
```

因此本文已经是 qualified contract candidate。候选写作阶段的 `@vue/reactivity` dependency 转录错误、正式 lifecycle
前 non-Git CWD repository-inference setup error 与 Playwright teardown warning 继续按原身份保留；它们不被后继
PASS 覆盖，也不冒充产品或合同失败。

当前事实仍是：

```text
M0_MAINTENANCE_DEPENDENCY_DRIFT_PROVEN
M0_MAINTENANCE_DEPENDENCY_DRIFT_PRECONTRACT_AUDITED
M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_CANDIDATE
M0_MAINTENANCE_DEPENDENCY_DRIFT_IMPLEMENTATION_NOT_STARTED
M0_MAINTENANCE_WORKFLOW_BOOTSTRAP_BLOCKED
CORE_0_12_3_MAINTENANCE_RELEASE_NOT_STARTED
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_NOT_AUTHORIZED
```

[文档 236](236-m10-maintenance-dependency-drift-contract-freeze-publication.md)是独立 docs-only freeze publication。只有该
publication 自己的 final bytes、original PR Public CI、受保护 main 合入、new exact-main Public CI + Browser Smoke、
fresh README / 本文 / doc236 / milestones installed-product readback 与 independent reconciliation 全部闭合后，
目标 `M0_MAINTENANCE_DEPENDENCY_DRIFT_CONTRACT_FROZEN` 才生效。

合同冻结也不自动开始 dependency implementation。必须返回 CONTROL LOOP，从新的 exact main 重新确认 one-file
dependency drift correction 是否仍是当前最小合法问题。

停止原则为：**相同 package 名、相同 advisory 修复范围或相同最终版本都不继承 authority；只有 exact maintenance
source 上可复算的 14-entry closure、one-file identity、两轮 manual-dispatch witness、受保护合入与失败保留共同闭合，
才有资格发布 dependency-drift qualification。**
