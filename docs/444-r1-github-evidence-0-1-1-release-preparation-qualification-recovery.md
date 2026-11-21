# R1 GitHub Evidence 0.1.1 发行准备资格恢复发布

> 状态：`RECOVERY_PUBLICATION_CANDIDATE / NOT_QUALIFIED`
>
> 影响：`L0_DOCUMENTATION`
>
> recovery base：`main@3fdfdc25628637eed6d81360d7b2eea81c1ff3d0` / tree
> `f59a27da3fd23203e3d15bbd6efedb12849e31a0`
>
> 冻结上游：[维护发行与 P2 provenance 对齐合同](441-r1-github-evidence-0-1-1-maintenance-release-and-p2-provenance-contract.md)、
> [发行准备候选](442-r1-github-evidence-0-1-1-maintenance-release-preparation-candidate.md)、
> [exact-main formal 失败边界](443-r1-github-evidence-0-1-1-release-preparation-exact-main-formal-failure-boundary.md)与
> [证据反馈工作法](working-method.md)
>
> 本文只发布新的发行准备资格恢复事实；不修改 runtime、Schema、测试、workflow、传输、重试、代理、oracle、tag、Release
> 或公开资产。

## 1. failure boundary 已成为 qualified history

PR #506 只包含 README、AGENTS、文档 443 与 milestones，精确 identity 为：

```text
base   = 8075d61352b8f4719e625b0c48be3b6e941da6d8
head   = 265bae9ff190211e9af006586ee6f58a1da78dec
tree   = f59a27da3fd23203e3d15bbd6efedb12849e31a0
scope  = 1 commit / 4 files
merge  = 3fdfdc25628637eed6d81360d7b2eea81c1ff3d0
```

original Public CI `44822033360`、exact-main Public CI `44828488193`与Browser Smoke `44828488313`均为
attempt 1 SUCCESS（15/15、15/15、1/1）。fresh installed P1 API对精确commit取得`coverage=COMPLETE`；
README、doc442、doc443、milestones的raw/API/exact-Git bytes各自一致。independent reconciliation、47-artifact finite
closeout与post-closeout integrity SHA-256为：

```text
61a467db0a6b94592eedad404fc06a0b7da7c9a104735c671838e1c53fd91159
f86767ba08085522098a26ac7d8270ec0dbf325a3f79e5cdffbe931e1483f069
9fe499f1f30567f0672700ac35c25787e639d96affca9133bac7c171f3977eae
```

因此文档 443 现在是：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_EXACT_MAIN_FORMAL_FAILURE_BOUNDARY_AUDITED
QUALIFIED_HISTORY
```

这不回填 PR #505、`8075d613...` 或其 Python 3.10 formal attempt 1。原三次 P1 `NETWORK_ERROR / ERROR`、同session
P2 COMPLETE、未执行P3/Core、未启动Python 3.13 formal与`underlying_cause=UNKNOWN`均保持原身份；没有rerun。

## 2. fresh recovery world 与冻结边界

新的恢复施工只认`3fdfdc256...`。PR #506相对失败world只增加四个docs-only文件，插件runtime、Core、测试和workflow字节未变。
continuity复核固定以下冻结边界：

```text
contracts.py                                      5df8fd230e00352820a16d58b23bf9b7fe5175357efb13e9843ed76ebe02368c
public_render_browser.py                          0d14319eab081ca87247492135d169741172e1fac2b4853e3567ba9eb71b85e2
public_render_contracts.py                        efa3fcc995ab99ced9c7f2c48d078fb63d613a3a90bcbb67da8277ba0e116d02
tests/public_render/test_browser_session.py        2cea3841f62c17e27d1eb9d26c159fa9d1c8f8c4ab73d72b494a57aeaa8f720e
tests/public_render/test_chromium_fixture.py       fbec2e2558e85f5cc47676882acb53143ba96f99b587327faeecbe6ec778498d
```

这一步没有用“后来成功”推导旧失败根因，也没有因为根因未知就修改transport、timeout或retry。

## 3. source、构建与 installed-product 矩阵

fresh source矩阵逐格通过：

```text
GitHub Evidence: Python 3.10/3.13 × normal/-O = 194/194 each
Acceptance Core: Python 3.10/3.13 × normal/-O = 504/504 each
```

plugin执行两次独立source-copy build；wheel逐字节一致，normalized sdist一致。fresh Core 0.13.0 wheel与GitHub Evidence
0.1.1 wheel/sdist摘要为：

```text
Core wheel    efc60a41b72154c57ca2c5e1e115407890c85e243f8475c26aa440d47154b698
plugin wheel  c1f650448dd42595dd9ee139bfb399be8d776a47112fa0910428eca5ed6dc0e4
plugin sdist  a4203fd798b359d02b9bfd38b29621edf9be63ba7d1642053f7b6b7605d06f80
```

Python 3.10.6与3.13.13都完成base wheel、sdist、`render` extra、CLI/import/pip check、Playwright 1.62.0与匹配Chromium
启动；两个blocked-cleanup负链均观察到owned driver deadline termination且无残留。installed matrix SHA-256为：

```text
d5a76144a6e33e9baef8f4b18d2baaa939d87e79e37dfdc4c90bac96554ed0a3
```

## 4. formal recovery 使用新 identity

首次anonymous diagnostic在任何formal启动以前因fresh venv没有默认CA路径而出现
`SSLCertVerificationError: unable to get issuer certificate`。该identity永久保留为non-qualifying proof-facility setup failure；
没有把TLS验证关闭，也没有把它改写成产品失败。随后只把两个venv内pip vendored、逐字节相同的CA bundle显式交给urllib，
TLS验证继续启用；CA setup record SHA-256为：

```text
b874abe90e49fbe325a42e82b0df8dd8b1f85648dd942d96e0bd9b0a07fa0c23
```

新的diagnostic attempt 2与preflight attempt 2通过。因为之前没有formal开始，两个Python formal都使用各自唯一的attempt 1；共享
Plan但不复用collection session：

| Python | collection session | API Evidence | Render Evidence | Core report |
| --- | --- | --- | --- | --- |
| 3.10.6 | `github-paired-b067b119a37a4e838ee4a2c2f222dce6` | `d9c495a5a8bc3a2f05ffd7ea6c771c0053ff1138a05e62c6b13db65b420e3f0a` | `0cebad255852591f6edafbf670e4adc10a7ffcfb6e79d7fba14658d4fa032ee1` | `ae97317252b9b497b00738556070cc19fe8bcfb2d6f4a014a9e1b2f80b3431b0` |
| 3.13.13 | `github-paired-ee76ab73c9aa4f6882c6b373e676c914` | `1c511223596a4e3d9dacbf8dbca97fffc9463d93642c6c840014f4148774adbd` | `8fdc0cd60bbb6886df2c4ce541bbf73468347af1fddd36d17317dbeb53501c79` | `21d3a56858b02edb9963880ffd30cf857854a9bd29ece9d5f97b104b3ccd8883` |

共享Plan digest为`10fb318d85520c8736c60db4296ccd72aa0fcce0defbd77b8d292542cc84a0e3`。两次API与Render均为
`COMPLETE`，P3 handoff/Core均为`PASS`。插件卸载后，Core-only复算继续消费同一组Plan/API/Render identity并两次`PASS`；
formal summary与uninstall/Core-only summary SHA-256为：

```text
dd6d8b3dcd4ac098100e46d9a8aefd678d06e438ed020ecc0c9ba73e7983a4b3
fd52e55a94d69df66e6ebd42aeff047ec4e2fa0b195921fb9a61229e554a727f
```

这些是新exact world的新formal，不是PR #505失败identity的rerun或续期。

## 5. candidate assets 与 pre-tag 停止线

本地candidate按固定顺序形成wheel、sdist、non-self-referential validation summary与checksum；四项摘要分别为：

```text
wheel       c1f650448dd42595dd9ee139bfb399be8d776a47112fa0910428eca5ed6dc0e4
sdist       a4203fd798b359d02b9bfd38b29621edf9be63ba7d1642053f7b6b7605d06f80
summary     2a877f564f1eaef7b88b96b582e26957dfbcd28abddb53badc9312f5e1479016
checksum    af1e364f63718644410da9a7fbf7979e0e4a111e60acd182bfad8c45dad76dea
```

pre-tag核账确认ruleset `22613490`仍active、作用于`refs/tags/github-evidence-v*`、无bypass且禁止删除/非快进；历史
`github-evidence-v0.1.0`仍指向原坐标，Latest仍是Core `v0.13.0`。`github-evidence-v0.1.1` tag与Release均不存在。

这些candidate bytes只属于`3fdfdc256...`。本文若以后精确合入，会产生新的exact main；因此当前字节不得复用为最终公开资产。

## 6. retained non-success 与本地闭环

除首次anonymous diagnostic外，以下proof-facility事实都按原identity保留：PowerShell tree-ish解析错误、历史Core-only模板路径错误、
release-assets help返回形状误判、local qualification attempt 1 continuity路径错误、attempt 2生成`build/`残留导致四个local hygiene
`REVIEW_REQUIRED`，以及两个cleanup命令在CreateProcess以前被执行策略拒绝。已核验的generated `build/`随后被单独清理；attempt 3的
global/local hygiene 8/8 PASS。没有一个setup failure被解释成产品PASS或删除。

local qualification、independent reconciliation、223-artifact closeout与post-closeout integrity SHA-256为：

```text
afe2f7436dfe1a162de8bac262793f5743701792fd795e85879da5b2733d97ec
345868d034c8a0b6af8e3bfd548a0e79edd061cdba0983b29edcbe6dd6ebe969
479c3cea708cf39afa79d3dc89844d89c41627565c0edeb22d7288015d039748
332206d90f5fa33c1e3903effcc1c898b1c2a1103998f47da9605b42cba44fe5
```

local qualification的便利字段漏列了以`review-required`命名的attempt 2 record；独立reconciliation没有隐藏该差异，而是重新枚举并
绑定全部8个non-success identity。原文件均在，语义影响为NONE。

## 7. 本文自己的资格链

本文只允许README、AGENTS、本文与milestones四个docs-only文件变化。final bytes必须完成：

1. Markdown链接与格式、global/local hygiene、`git diff --check`和primary `audit.json`连续性；
2. exact base/head/tree、1 commit/4 files与original PR attempt 1 required gate；
3. protected exact-head merge与新exact-main Public CI 15/15、Browser Smoke 1/1；
4. 从新exact main重建fresh installed P1，并对README/doc442/doc443/doc444/milestones完成anonymous raw/API/exact-Git readback；
5. independent reconciliation与finite closeout；
6. primary `audit.json` SHA-256持续为
   `4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

全部成立后，本文才允许条件状态生效：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_CANDIDATE_EXACT_MAIN_VERIFIED
GITHUB_EVIDENCE_0_1_1_FINAL_ASSET_REBUILD_AND_PROTECTED_PUBLICATION_ALLOWED
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
```

这只授权从届时新的exact main重新构建最终四项资产，并按文档441/442执行受保护annotated tag、non-Latest Release、公开下载与
fresh installed-product/readback资格链。它不声明当前candidate bytes为final，不声明tag或Release已经存在。

## 8. 当前状态与后继停止线

本文资格链闭合以前只能声明：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_EXACT_MAIN_FORMAL_FAILURE_BOUNDARY_AUDITED_QUALIFIED_HISTORY
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_QUALIFICATION_RECOVERY_CANDIDATE_NOT_QUALIFIED
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_NOT_STARTED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R2_R6_NOT_STARTED
```

本文闭合后仍须返回CONTROL LOOP；只有冻结前提和公开坐标仍成立，才可执行最终protected publication。公开发行PASS也不得回填
PR #505、doc437、#498、Manifest 0.2、global composition或R2–R6。`proof_is_not_problem_solving = true`、
`local_not_global = true`；R1完成后的human+AI全项目检查仍是独立后续目标。
