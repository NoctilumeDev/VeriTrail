# R1 same-attempt continuity private implementation exact-main Browser Smoke failure-boundary audit

日期：2026-11-11

> 候选状态：`R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@a41b8ba3575419e754099725b5e1616af6cd1af4`，tree
> `c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255`。
>
> 受审对象：[文档405](405-r1-same-attempt-derivation-evidence-continuity-private-implementation-candidate.md)与PR #464的
> exact-main Browser Smoke qualification failure。
>
> 影响：`L0_DOCUMENTATION / QUALIFICATION_FAILURE_BOUNDARY_ONLY`。本文只保存失败identity、资格影响、`UNKNOWN` lower cause与
> 最小后继责任；不修改runtime、tests、workflow、Browser oracle、Playwright安装命令、retry、timeout、Schema、manifest、
> persistence、public Review、Core Verdict、global composition authority或R2–R6。

## 1. CONTROL LOOP触发事实

[文档404](404-r1-same-attempt-derivation-evidence-continuity-private-implementation-authorization-publication.md)已完成自己的完整
资格链，使bounded A–J private implementation authority生效。后继PR #464绑定：

```text
base   = b5ff07e03630d57060384883d28a49dc57bdf0df
head   = b4fa42cc16b814f9d23e8c025bc4499dcb412084
tree   = c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255
shape  = 1 commit / 10 files
```

候选只在授权范围内增加versioned private continuity owner、controller capture、normal/四类negative exact binding、one-shot
lifecycle、independent reconciliation与`DEC-000`至`DEC-029` falsifiers；没有public export、Schema、manifest、persistence、Core
Verdict或global composition authority。本地semantic四格、focused四格、完整Review Attention四格、compile、diff、hygiene、public
export guard与primary `audit.json` continuity均PASS。original Public CI `43034543495` attempt 1为11/11 SUCCESS。

保留证据中，local qualification、51-artifact local evidence seal、post-commit seal与original PR qualification SHA-256分别为：

```text
92d828ddb62a3fa480989023d0c932bc752b991ce33ff1ab6bb14abbaf9c8669
9dddcc1c6c99c161035833fda2b38ca0ad60feb2db8c141d05cecb302814db59
239f423d9f0c742f22c87f8af8623d3a7df749705ec5fc038813983b9bfac092
f975559bc2c160e2b10ff78d4bf9e41fcf8dd96eb98f372a1063afd2a846affd
```

protected exact-head merge形成：

```text
merge   = a41b8ba3575419e754099725b5e1616af6cd1af4
tree    = c8f0bd16e9e69a0ef7bdea3da8526d8fb0f3f255
parents = b5ff07e03630d57060384883d28a49dc57bdf0df
          b4fa42cc16b814f9d23e8c025bc4499dcb412084
```

protected merge evidence SHA-256为
`57f7f560610eda027e055d0795ea2d0e5fabab16dd277e710a4cef718618e6b2`。

new exact-main Public CI `43040847982` attempt 1最终为11/11 SUCCESS；new exact-main Browser Smoke
`43040847817` attempt 1在唯一required job中FAILURE，没有rerun。fresh installed-product readback、independent reconciliation与
finite qualifying closeout没有启动。

因此doc405与实现世界的资格链在new exact-main Browser Smoke停止：

```text
implementation bytes = MERGED
exact-main Public CI  = PASS / 11 of 11
exact-main Browser    = FAIL / setup did not reach product smoke
readback              = NOT_STARTED
qualification         = NOT_QUALIFIED
freeze                = NOT_FROZEN
```

original PR绿灯、exact-main Public CI绿灯与相同tree均不能替代失败的Browser gate。

## 2. Browser Smoke失败的直接事实

失败坐标：

```text
run         = 43040847817 / attempt 1
workflow    = Browser Smoke
job         = Production Workbench smoke / 130591908382
failed step = Install Chromium / step 6
command     = python -m playwright install --with-deps chromium
```

checkout、Python 3.13、Node.js 22与browser adapter安装均SUCCESS。Chromium安装开始后，Ubuntu mirror与security域名持续报告：

```text
Temporary failure resolving 'azure.archive.ubuntu.com'
Temporary failure resolving 'archive.ubuntu.com'
Temporary failure resolving 'security.ubuntu.com'
```

依赖下载最终以`apt` code 100、Playwright安装失败、step process exit 1终结。其后：

- `Build the production Workbench`为SKIPPED；
- `Run the bounded browser smoke`为SKIPPED；
- workflow的upload step显示SUCCESS，但Actions Artifact API返回`total_count = 0`；
- 没有产品页面、浏览器断言、console、request或screenshot结果可用于裁定subject。

直接证据只允许：

```text
classification                                  EXACT_MAIN_BROWSER_SMOKE_CHROMIUM_INSTALL_DNS_SETUP_FAILURE
required exact-main Browser gate failure       ESTABLISHED
Chromium dependency-install DNS setup failure  ESTABLISHED
product build executed                         FALSE
product browser smoke executed                 FALSE
subject failure                                NOT_ESTABLISHED
candidate regression                           NOT_ESTABLISHED
exact lower runner / DNS / network cause       UNKNOWN
```

`UNKNOWN`不能被改名为GitHub、Ubuntu mirror、runner、代理或候选代码的已知单一根因。

finite failure evidence与exact-main gate summary SHA-256分别为：

```text
697ffe7ae94d7f86d8c51bf5194a0f7e4b90e9d4a360566c047875dc4841a75b
2460a3d70cfd6c1ed2ecc31e1979bf52ac269e30e5a933e4ecccf3389d62da1c
```

## 3. qualification failure与implementation semantics分离

该失败足以否定doc405的exact-main资格，但没有执行产品smoke，因此不能推翻本地runtime witness、frozen continuity contract或
doc404 authorization。必须同时保留：

```text
semantic/local result
    bounded private implementation在声明world中的final source/test witness通过

qualification result
    merged implementation没有通过自己预注册的exact-main Browser gate
```

前者不能覆盖后者；后者也不能扩大成continuity owner、Fact/Relation capture、terminal route、Coverage reconciliation或one-shot
lifecycle缺陷。`proof_is_not_problem_solving = true`：正确描述setup failure不等于实现已经取得资格。

## 4. Browser oracle与workflow边界没有被击穿

本次没有进入production Workbench build或bounded browser smoke，因此没有观察到Browser oracle误判、截图义务被满足或产品failure
被错误接受。失败发生在产品观察以前，现有证据不授权：

```text
rerun 43040847817
retry until PASS
删除、降级或skip Browser Smoke
把Playwright --with-deps改成无依赖安装以绕过required gate
扩大timeout或增加无限网络retry
用Public CI 11/11替代Browser 1/1
用original PR Browser环境的隐含成功替代exact-main attempt
在Browser gate失败后启动fresh installed-product readback
把后继成功回填成a41b8ba世界的Browser PASS
```

若后继世界在unchanged gate下成功，它只能证明新world不需要弱化门；不能解释本次DNS失败，也不能改写run
`43040847817`。

## 5. 最小合法recovery seam

当前最小合法问题不是“再跑一次Browser”，而是：

> 怎样先把PR #464 exact-main Browser setup failure变成有界、可复算的qualified history，再让已经合入的implementation bytes在
> 新exact main上承担一条完整且独立的qualification recovery？

恢复必须串行：

1. 本docs-only failure-boundary audit先通过自己的local、original PR、protected merge、new exact-main双门、fresh readback与
   independent reconciliation，只升级失败identity与authority ceiling；
2. 如果本审计的unchanged Browser gate成功，只证明恢复无需弱化门，不解释也不回填`43040847817`；
3. publication形成新事实后返回CONTROL LOOP，复核doc404 authority、doc405 exact source hashes、merge world与保留首败；
4. 只有没有新的runtime/test/oracle反例时，才允许从新的exact main建立独立docs-only implementation qualification recovery
   publication，机械绑定现存implementation bytes并取得新的original/exact-main/readback/reconciliation资格；
5. recovery publication最多把implementation升级为`EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`；冻结仍必须由后继独立
   docs-only publication取得；
6. 若本审计自己的Browser gate再次失败，保留新identity并重新判断proof-facility/environment边界，不把重复失败当作弱化oracle
   或重跑旧attempt的理由。

本文不直接恢复implementation qualification，不创建runtime patch，也不授权manifest、persistence、public Review、global
composition或R2–R6。

## 6. 本audit自己的资格门

tracked scope只允许：

```text
README.md
AGENTS.md
docs/406-r1-same-attempt-continuity-private-implementation-exact-main-browser-smoke-failure-boundary-audit.md
docs/milestones.md
```

doc405、private runtime/tests、workflows、Browser oracle、Schema、manifest、persistence、Review、Core Verdict与全部frozen semantic
bytes必须保持`a41b8ba…` base bytes。final bytes至少通过exact四文件scope、UTF-8 without BOM、LF/final LF、links/fences/headings、
required markers、failure identity、`git diff --check`、global/local hygiene、focused Python 3.10/3.13 × normal/`-O`与primary
`audit.json` continuity。

```text
final docs-only failure-boundary bytes / declared local gates
    -> original PR Public CI attempt 1
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc405 / doc406 / milestones observation
    -> independent source / failure / authority reconciliation
    -> finite closeout / integrity
    -> EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY
    -> return CONTROL LOOP
```

任何non-success保留原identity并停止；不得重复已有PASS。

## 7. 当前状态与停止线

全部最后门闭合以前只能记录：

```text
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_CONTRACT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED_QUALIFIED_HISTORY
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_MERGED_EXACT_MAIN_PUBLIC_CI_PASS_BROWSER_SMOKE_FAILED_NOT_QUALIFIED_NOT_FROZEN
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_PRIVATE_IMPLEMENTATION_EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

全部门闭合后只把本文升级为`EXACT_MAIN_BROWSER_SMOKE_FAILURE_BOUNDARY_AUDITED / QUALIFIED_HISTORY`。doc405继续保持
`MERGED / NOT_QUALIFIED / NOT_FROZEN`，run `43040847817`与lower `UNKNOWN`不回填。随后必须返回CONTROL LOOP，不能按文档号
自动建立recovery、冻结implementation、恢复manifest/global composition或进入R2–R6。
