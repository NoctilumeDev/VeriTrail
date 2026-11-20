# R1 GitHub Evidence 0.1.1 发行准备 exact-main formal 资格失败边界

> 状态：`FAILURE_BOUNDARY_CANDIDATE / NOT_QUALIFIED`
>
> 影响：`L0_DOCUMENTATION`
>
> 失败 world：`main@8075d61352b8f4719e625b0c48be3b6e941da6d8` / tree
> `7cf77597aac5b9e10149a5d614281c6c88fdd2a2` / Python 3.10 formal attempt 1
>
> 冻结上游：[维护发行与 P2 provenance 对齐合同](441-r1-github-evidence-0-1-1-maintenance-release-and-p2-provenance-contract.md)、
> [发行准备候选](442-r1-github-evidence-0-1-1-maintenance-release-preparation-candidate.md)与
> [证据反馈工作法](working-method.md)
>
> 本文只保存并归层失败，不修改 runtime、Schema、测试、workflow、重试预算、代理、tag、Release 或资产。

## 1. 失败以前已经成立的 exact 坐标

PR #505 以如下唯一 candidate identity 完成 original gate 并受保护合入：

```text
base   = 8493c6240fda4c6435198fe37d39ab51a56a95cd
head   = c1c8783041e864331ab07a167455930de757506e
tree   = 7cf77597aac5b9e10149a5d614281c6c88fdd2a2
scope  = 1 commit / 16 files
merge  = 8075d61352b8f4719e625b0c48be3b6e941da6d8
```

PR original Public CI `44804624282` attempt 1为15/15 SUCCESS；新exact main的Public CI
`44811437374`与Browser Smoke `44811437593`也均为attempt 1 SUCCESS（15/15、1/1）。original qualification与
exact-main gate记录SHA-256分别为：

```text
d15dafcc9901c2c728bc44b1f8a87795465f7e7a426d882cb9e66978676f30f4
2fe60e29e1db66a9397de5eaf938d72251cd1eb42ef36e18070713f1ab422803
```

这些事实只证明source candidate与公共门成立，不替代doc442要求的fresh installed-product formal。

## 2. fresh exact-main 产品矩阵没有先行反例

fresh detached worktree只认`8075d613...`。从该exact main重新构建Core 0.13.0与GitHub Evidence 0.1.1，
并建立六个全新环境：

```text
Python 3.10.6: base wheel PASS / sdist PASS / render extra PASS
Python 3.13.13: base wheel PASS / sdist PASS / render extra PASS
```

installed-product summary SHA-256为：

```text
171de16b6dcaba7605f87af866cc0480912d193382302f05038215e19139d41d
```

两个独立blocked-cleanup负链分别在约2.53秒返回，均观察到
`playwright-driver:deadline-terminated`，owned process tree residue为空；其SHA-256为：

```text
Python 3.10  2d7336cb0400bba26aba6ffe930b6b61ecd635c1609852966af3757b41dc8315
Python 3.13  5ba7d9978158677cb268c42ff1a3e138f54966df92718d08711dd8dd95e9221e
```

这些PASS仍只是该exact-main product world的witness，不会覆盖后述formal失败。

## 3. 唯一正式失败

formal以前的anonymous rate diagnostic观察到`remaining=8`；installed
`veritrail_github.transport.UrllibTransport` preflight随后对精确commit取得HTTP 200并观察到`remaining=7`。两份诊断都明确为
`NONE_DIAGNOSTIC_ONLY`，SHA-256为：

```text
rate diagnostic  5e4b00aec0f90e1fdefcb955060265e0cd0130565fdfb6f54839f4b844ad6b59
formal preflight  8fe1f2895e6c09997af6bc82ccc7c11db0886feb24addb5e6ac29c03c91b6433
```

随后只启动Python 3.10.6 installed-product formal attempt 1。P1 repository probe在同一正式collection session中执行三次，
均没有取得HTTP status、GitHub request ID或rate metadata：

| attempt | monotonic elapsed | outcome |
| --- | ---: | --- |
| 1 | 109 ms | `NETWORK_ERROR` |
| 2 | 109 ms | `NETWORK_ERROR` |
| 3 | 125 ms | `NETWORK_ERROR` |

因此P1 Evidence为`coverage=ERROR`，SHA-256为：

```text
479048f45ba68b7f8d609555850e69a25e07f8939f1d8cff1f9d14d19938e00b
```

同一次paired session的P2 Public Render完成exact-SHA README观察，HTTP 200、marker存在、
`coverage=COMPLETE`且cleanup errors为空；其Evidence SHA-256为：

```text
2a70ba94e1001c15c13b9332c9ed69207da71a8f0983a519fb73a90e41feac6f
```

runner在检查paired sides时按冻结oracle拒绝P1非完整状态并退出：

```text
RuntimeError: github-api was not complete
```

P3 handoff与Core evaluation没有执行；Python 3.13 formal没有启动。failure record与finite integrity identity为：

```text
a5cc817bbbad6724a672e8bf54a73597d69b438fddcdbed5aeb3a406d3572b86
dfe10dbb9ae9aeb4f623d44d229034f10316a23fc21376dbbd9f2b70177a1fe5
```

没有formal rerun，没有finalize validation summary/checksum，没有pre-tag核账，也没有创建tag、Release或公开资产。

## 4. 归层与认识论边界

当前证据只支持：

```text
FORMAL_INSTALLED_PRODUCT_PY310_GITHUB_API_NETWORK_ERROR
EXACT_MAIN_RELEASE_PREPARATION_QUALIFICATION_STOPPED
UNDERLYING_CAUSE_UNKNOWN
```

相邻preflight、remote Git读取与同session P2 Render成功，所以不能把失败推广为“全局网络不可用”。P1没有保存更低层异常对象，
三次尝试均未取得HTTP response，所以也不能证明GitHub、代理、DNS、TLS、Python 3.10、UrllibTransport或插件实现中的任一单一根因。
安装矩阵与负生命周期PASS不能把正式P1 ERROR改写成PASS；P2 COMPLETE也不能替代paired P1完整性。

因此本文不修改transport、重试集合、timeout、代理选择或formal oracle。若新的独立证据将来证明产品缺陷，只能显式reopen/version
bump被击穿的最小边界；在此以前根因保持`UNKNOWN`。

## 5. 本文自己的资格边界

本文只允许README、AGENTS、本文与milestones四个docs-only文件发生变化。final bytes必须完成：

1. Markdown链接与格式、global/local hygiene、`git diff --check`；
2. exact base/head/tree与四文件scope核账；
3. original PR required gate，不rerun覆盖失败；
4. protected exact-head merge与新exact-main Public CI 15/15、Browser Smoke 1/1；
5. fresh anonymous installed P1，以及README/doc442/doc443/milestones的raw/API/exact-Git readback；
6. independent reconciliation与finite closeout；
7. primary `audit.json` SHA-256连续保持
   `4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

全部成立后，本文最多成为：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_EXACT_MAIN_FORMAL_FAILURE_BOUNDARY_AUDITED
QUALIFIED_HISTORY
```

它不回填PR #505或`8075d613...`的formal资格，也不授权在同一exact world重跑attempt 1。

## 6. 后继停止线

本文资格链闭合后必须返回CONTROL LOOP。若产品边界与外部前提仍成立，后继只能从新的exact main、fresh build、fresh Plan/request/session、
新输出根和新的formal identity重建release-preparation recovery successor，并重新执行doc442的完整product/pre-tag/finite closeout门。

当前只能声明：

```text
P2_PUBLIC_RENDER_OWNED_BROWSER_LIFECYCLE_CORRECTION_IMPLEMENTATION_FROZEN
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_RELEASE_AND_P2_PROVENANCE_ALIGNMENT_CONTRACT_0_1_FROZEN
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_ORIGINAL_PR_504_FAILED_CLOSED_UNMERGED
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_LOCAL_SUCCESSOR_2F61_STOPPED_PRE_PR_NOT_QUALIFIED
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_PR_505_MERGED_EXACT_MAIN_DUAL_GATES_PASS_FORMAL_FAILED_NOT_QUALIFIED
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
R1_PICOMATCH_ADVISORY_WITHDRAWAL_WORKBENCH_AUDIT_RECOVERY_MERGED_EXACT_MAIN_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`proof_is_not_problem_solving = true`、`local_not_global = true`。本文不是网络修复，也不是release recovery。
