# R1 Parse → Fact consumer correction private implementation 冻结发布

日期：2026-10-11

> 条件化状态目标：`R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FROZEN`。本文自己的最后门全部闭合以前，目标不是生效事实。
>
> 发布基线：`main@d9e6ce3021c1981c52ddafa5009568ef900dcac6`；tree `db5fe21ab4536ed67df6ed96a739e50610beafaf`。
>
> 上游：[冻结合同](245-r1-parse-to-fact-consumer-correction-contract.md)、
> [A–J feasibility](247-r1-parse-to-fact-consumer-private-implementation-feasibility-audit.md)、
> [授权发布](248-r1-parse-to-fact-consumer-private-implementation-authorization-publication.md)、
> [实现候选](249-r1-parse-to-fact-consumer-private-implementation-candidate.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

doc248 publication world `712b8ef42563c99434fa8d36455cb80693ce5aa8` 已以四份独立 PASS、六份原身份 ERROR 和
independent reconciliation `39c597fadf5d27e0157f8f08da39e07eeb3ed0f354351db5ff54110355026be0` 取得实现授权。
CONTROL LOOP 又绑定首页展示更新后的 `935adbfd55b974d7fa50535da2ea0c95a90b4f99`，核对该坐标自己的双门及
关键合同/runtime 字节连续性，才开始私有 A–J。历史授权 world 与实现 world 不混合。

本发布只冻结 application-owned post-Parse Fact consumer 的私有闭环：领取原 Parse continuation，重验 exact
products/input/classification history，为每个 existing-applicability Provider 机械分配完整 ACCEPTED membership，
使用独立 one-shot child claim、product-only fixed worker、逐 candidate provenance admission、完整 requiredness /
lifecycle reconciliation，再领取同 original BudgetContext/parent eligibility 的私有 continuation。

zero denominator 与 all-rejected 保持不同 upstream identity，accepted count 为零均阻断 claim/child/terminal /
FactSet/continuation。合法 nonempty product-bound child 可以报告零 Fact；这不缩小 membership，也不证明 Fact
fulfillment。历史 projection `/0.1`、wire `/0.2` 与 historical controller 保持原义，public Fact controller 未自动切换。

## 2. Exact implementation qualification

```text
PR                 = #287
base               = 935adbfd55b974d7fa50535da2ea0c95a90b4f99
head               = ab718cc6b4003a60de2a2707b50f71d0ff942690
ordinary merge     = d9e6ce3021c1981c52ddafa5009568ef900dcac6
candidate/merge tree = db5fe21ab4536ed67df6ed96a739e50610beafaf
diff               = 1 commit / 7 files / +2386 / -0
```

[PR #287](https://github.com/NoctilumeDev/VeriTrail/pull/287) 的 original Public CI
[38116549854](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38116549854) attempt 1 为 11/11 SUCCESS。
exact-main Public CI [38149116073](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38149116073)
attempt 1 为 11/11 SUCCESS；Browser Smoke
[38149116151](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38149116151) attempt 1 为 1/1 SUCCESS。
ordinary merge parents 精确为上述 base/head，merge tree 等于受审 candidate tree。

最终 implementation bytes 的 targeted suite 四格各 `34/34 PASS`；full Review Attention 在 CPython 3.10.6
normal/`-O` 各 `473 OK / skipped=1`，CPython 3.13.13 normal/`-O` 各 `473/473 PASS`。本地 3.10 skip 是既有
ambient-runtime impersonation 条件；3.13 实际执行该反例。hosted CI 的 Review Attention 四格各运行 473 项、
`OK / skipped=2`；两个 local-only exact-reference witnesses 在 runner 无可用 runtime，不能写成 473 项全部实际执行。

四类 real golden semantic worlds（mixed、two accepted、all rejected、zero denominator）四格逐字节一致，均为
26193 bytes，SHA-256 `c572ffd7590448674c07480151ee1cda741129ab034a283d429b6895bf98f861`。
比较不要求独立 attempt/run provenance 相同。候选独立资格摘要为
`dc5add7dd876be33605e322ce0aacab2904fff88835fc90b7c4b44244d4a8f0c`。

独立 wheel SHA-256 `8b196a4922759489148cd7be2e7d77046124060023925c8b9dca326b4011dec4`，219866 bytes。
fresh venv 继承 system-site dependencies；review package 与五个 proof modules 的 origin 均核对为该 venv 的
site-packages，并逐字节等于 candidate source。installed real Parse → two product-only Windows workers → join →
continuation 成立；这不是完全依赖隔离或公开 Release 声明。

## 3. Candidate fresh installed-product readback

在 detached implementation exact main 上，由独立 CPython 3.13.13 venv 安装冻结 Core 0.13.0、GitHub Evidence
0.1.0、Playwright 1.62.0 与 matching Chromium；Core/plugin 从 venv site-packages 导入。匿名观察清空 token、
PYTHONPATH/PYTHONHOME，代理只按命令注入。

| Target | 独立 Plan ID | 独立 Session | Report SHA-256 |
| --- | --- | --- | --- |
| doc249 | `r1-pfc-impl-formal-doc249-1-d9e6ce3` | `github-paired-ebb5694a76db428482aaac42507587aa` | `8eeaad1033669a0ed19cb91e1611e32a8a35a555794eb8375b22f031c4082faa` |
| milestones | `r1-pfc-impl-formal-milestones-1-d9e6ce3` | `github-paired-2868600eb13f49d78d18640ac6d7ecba` | `d628e88b63ca76df13ccd124769539fb6ae0e2f8d80683ea41397fbd71644412` |
| readme | `r1-pfc-impl-formal-readme-1-d9e6ce3` | `github-paired-1aa3aa4eed0e4b2d89fdd38c75bc99da` | `29f7cdddb847b0532ce51e1c8b8eeaa5c4f0bcaaa6b4d639fbd034c5435b896d` |

三个目标均取得 P1/P2 COMPLETE、Core PASS、稳定 marker、无 redirect/conflict/coverage reason/cleanup error /
active stream。独立 evaluator 从原 handoff/Evidence 与 sealed Plan 重算 Core，逐项等于 producer report；三份
public raw bytes 逐字节等于同 exact main 的 Git blobs。raw-byte 核账不替代正式 product path。

candidate independent reconciliation SHA-256：

```text
b787eba23c6322a910663540fd12f5e102d24f4b53102334f7bde11f8fd5cbf8
```

该 history 有三个 selected qualifying PASS 和 0 个保留 non-success formal observations；所有 formal history
完整枚举并验证保留字节，数量从 history 导出。render-only diagnostics 不计入资格。

## 4. Proof 强度与历史边界

这是固定、受审计的 closed conformance worker 的 product-use proof。worker request 不接收 raw body/source text /
repository loader，也没有 reparse 路径；普通 Python 进程仍具有宿主能力，本文不声称任意第三方 Provider 被
filesystem sandbox 隔离。raw bytes 只由 application 用于 exact anchor 转换与边界验证。

private observation 保留 exact terminal/frame bytes；closure 持有 observations，document projection 以摘要绑定这些
bytes。closure document 本身不包含完整 frame，也不产生 public carrier 或 persistence authority。

首个 targeted attempt 的 27 项中 26 PASS、1 FAIL 永久保留为 `TEST_ASSERTION_TARGET_SETUP_ERROR`：PFC-I-017
从历史 `/0.1` owner 寻找 `/0.2` marker，实际 owner 在 `_source_operation_fact_application.py`。只修测试定位，
不改旧协议；后继 PASS 不覆盖首败。更早 Windows 硬退出 UNKNOWN 和 doc248 六个 formal ERROR 仍保留。

candidate readback setup 的匿名 wheel 下载 TLS EOF 保留为 nonqualifying setup 网络错误、底层原因 UNKNOWN；
随后使用重新校验的冻结 Release 缓存字节装入全新环境，不声称 fresh public download 成功。Playwright 环境预检
shutdown warning 保留为 nonqualifying setup observation，无正式 Plan/session 资格。

candidate 独立对账 attempt 1 误把 `observations/sealed-input-plans` 当成第四份正式观察，且 capture metadata 从错误
目录读取预封存 Plan，保持 `RECONCILIATION_HARNESS_PATH_CLASSIFICATION_ERROR`。修正只按已保留的 pre-observation
Plans 恢复派生 metadata 与目录 owner；原 capture v1、脚本和失败日志保留，三个产品 Plan/Evidence/report 没有改变。
fresh reconciliation attempt 2 才取得上述 PASS，不把 attempt 1 改写为成功。

两个 ignored build/egg-info 残留未进入 patch，已外置由 qualification workspace 接管；删除命令在执行前被工具
策略拒绝，local deletion pending 与 clean repository candidate 分开，不追加为产品冻结门。

## 5. 本发布自己的最后门

本 docs-only patch 只允许 README、AGENTS、milestones 与本文。doc249 与全部历史合同/发布、runtime、tests、
Schema、Profile、Policy、corpus、identity vectors、architecture DOT/SVG 保持原字节。

本层 final-byte local gates 为 CPython 3.10.6/3.13.13 normal/`-O` docs/Schema regressions、exact four-file scope、
relative links、UTF-8 without BOM、LF/final-LF、balanced fences/unique headings、target marker、敏感路径复核、
上述字节连续性、git diff --check 与 read-only hygiene。implementation runtime matrix 属于其已资格化 tree 的
witness；本文不把它改写为新 publication coordinate 的测试结果。Public CI 仍执行自己的全部原始门。

```text
publication final bytes / local gates
    -> original publication PR gates
    -> protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc250 / milestones observations
    -> independent Core and source-byte reconciliation
    -> target PRIVATE_IMPLEMENTATION_FROZEN becomes effective
```

本门闭合前只能说 implementation 已合入并完成自己的 exact-main/candidate readback，不能说独立冻结发布已经
生效。每个 formal non-success 保持原身份，诊断不替代产品资格，任何 later PASS 不覆盖历史。

## 6. 后继停止线

本发布不授权 Fact obligation universe/fulfillment、persistence Route A/B、empty FactSet closure、ReviewSliceSet /
Coverage、public Schema/carrier、Evidence/Bundle/publisher、CLI、Workbench、Core、CLAIM_FIDELITY、tag 或 Release。

最后门成立后返回 [CONTROL LOOP](working-method.md)，重新绑定 current main、冻结上游、并行 PR 与反例。
private consumer frozen 不自动授权下一 seam；只有现实证明最小问题仍成立，才可另行审计后继边界。
