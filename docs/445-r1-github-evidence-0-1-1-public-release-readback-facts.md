# R1 GitHub Evidence 0.1.1 公开发行与读回事实

> 状态：`PUBLIC_RELEASE_FACTS_PUBLICATION_CANDIDATE / NOT_QUALIFIED`
>
> 影响：`L0_PRESENTATION + L2_PUBLIC_DISTRIBUTION_STATUS`
>
> 发布源码：`main@f65b611749fe668c1dbba4d5b972c1221d76bf60` / tree
> `88d3e2479c4cbe0d213b67f57d48270b294d0b79`
>
> 冻结上游：[0.1.1 维护发行合同](441-r1-github-evidence-0-1-1-maintenance-release-and-p2-provenance-contract.md)、
> [发行准备候选](442-r1-github-evidence-0-1-1-maintenance-release-preparation-candidate.md)、
> [exact-main formal 失败边界](443-r1-github-evidence-0-1-1-release-preparation-exact-main-formal-failure-boundary.md)、
> [资格恢复发布](444-r1-github-evidence-0-1-1-release-preparation-qualification-recovery.md)与
> [证据反馈工作法](working-method.md)
>
> 本文只记录已经发生的 tag、Release、公开资产与 downloaded-product 读回；不修改 runtime、Schema、测试、workflow、
> Collector、Core、Verdict、doc437、Manifest 0.2、global composition 或 R2–R6 authority。

## 1. 文档 444 已闭合发行入口

PR #507 的精确 identity 为：

```text
base   = 3fdfdc25628637eed6d81360d7b2eea81c1ff3d0
head   = 0275634d393c379cdebda5c45259422c6c7ab9b9
tree   = 88d3e2479c4cbe0d213b67f57d48270b294d0b79
scope  = 1 commit / 4 files
merge  = f65b611749fe668c1dbba4d5b972c1221d76bf60
```

original Public CI `44842512006`、exact-main Public CI `44847680442`与Browser Smoke `44847680412`均为
attempt 1 SUCCESS（15/15、15/15、1/1）。fresh installed P1、README/doc442/doc443/doc444/milestones
raw/API/exact-Git readback、independent reconciliation、68-artifact finite closeout与post-closeout integrity全部成立；
后四项关键 SHA-256 为：

```text
original qualification       7b71f5bd3c310101a30d796b4bf9f490747ae9714a528b6f917806a3b205487f
independent reconciliation   49be7f4021b18e616b6a69727bd158f4d56d7c1dd838ea8237f36c1f2e4c10eb
finite closeout              f267b0d7ffb0042a7c51295a7c253c5dfba07ae95a08845999fcfc6dcb6c662f
post-closeout integrity      269b58f8daa6dc4356bf01a043fa023e2e0e740983f76060c6e91c2fb9d6fa21
```

因此以下状态已经生效：

```text
GITHUB_EVIDENCE_0_1_1_RELEASE_PREPARATION_CANDIDATE_EXACT_MAIN_VERIFIED
GITHUB_EVIDENCE_0_1_1_FINAL_ASSET_REBUILD_AND_PROTECTED_PUBLICATION_ALLOWED
```

README formal attempt 1 的匿名 API rate exhaustion、reconciliation attempt 1 的 retained-non-success shape错误、
PowerShell revision表达式与其他setup failures均继续保持原identity；后继PASS不回填它们。PR #505的P1三次
`NETWORK_ERROR / ERROR`和`underlying_cause=UNKNOWN`同样不变。

## 2. final assets 没有复用 candidate bytes

最终构建只认上述exact main，并在fresh stage重新生成Core 0.13.0 wheel与插件double-build。pre-tag核账确认：

- ruleset `22613490`仍active，覆盖`refs/tags/github-evidence-v*`，无bypass，禁止删除与non-fast-forward；
- 历史`github-evidence-v0.1.0`身份未移动；
- `github-evidence-v0.1.1`在tag创建前不存在；
- Latest仍为Core `v0.13.0`，Release ID `385190618`；
- primary `audit.json` SHA-256仍为
  `4eb732f4af9719993b94af95227f1d91d36fde7165ec8551199f985122b7598c`。

最终四项资产、大小与摘要为：

| 资产 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `veritrail_github_evidence-0.1.1-py3-none-any.whl` | 71,953 | `2f152cf40e3e705ffa9453b64c5446bd4da8e17e6ea7052d792af1349b3366d5` |
| `veritrail_github_evidence-0.1.1.tar.gz` | 83,515 | `585306788c522ddfba169e1a19a15dd0f0b715a8c2f00c30b13b24e70a986131` |
| `github-evidence-v0.1.1-validation-summary.json` | 2,728 | `fd11b64bed8f8c8317545deb1bdd5c09d6f004d0b455261767e3884526e7164e` |
| `SHA256SUMS-github-evidence.txt` | 333 | `603e5ce9e1cc7eadd7d02ccda1d56661f2eea9dec3c1333faa83aeec9b997ff9` |

final staging summary SHA-256为
`5b76874e634a1162de319a7673b9084533edeedc33508f716d97832587668819`。validation summary准确保留生成时的
`RELEASE_CANDIDATE`切片；发布后没有重制它来伪装成事后状态。checksum只覆盖wheel、sdist与validation summary，
不自指。

## 3. protected tag 与 non-Latest Release

串行发布形成以下公开坐标：

- protected annotated tag：`github-evidence-v0.1.1`；
- tag object：`132a01320fb06f991a6825bb6307ba06d94bd8f8`；
- peeled commit：`f65b611749fe668c1dbba4d5b972c1221d76bf60`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/github-evidence-v0.1.1>；
- Release ID：`453384323`；
- published at：`2026-11-21T02:33:03Z`；
- Release name：`VeriTrail GitHub Evidence Plugin 0.1.1`；
- `draft=false / prerelease=false / immutable=false`；
- non-Latest；匿名Latest API继续返回Core `v0.13.0`与Release ID `385190618`。

四个asset ID分别为`774144471 / 774144477 / 774144478 / 774144480`，GitHub API均返回
`state=uploaded`，大小与`sha256:` digest和上表一致。tag治理、Git对象、Release平台状态、asset digest与匿名下载
承担不同身份职责；Release的`immutable=false`被如实保留，没有被受保护tag偷换成平台对象不可变。

authenticated publication、publication capture reconciliation与protected tag evidence SHA-256为：

```text
a23096eecc5714c6dc31e819aafd0a771c19d0b5bb1386c1ec0316491ba8f6cd
84ec40d8808ec38a88001abe9994aeb4e542a8db5b4d50f2c7da6bf28d92c1c1
2ff9ef2ec2bf2a725a7bd73df8c4c1fb6c8225de3876590b3eae0ced999553c9
```

## 4. fresh anonymous asset 与 installed-product 读回

无GitHub token的fresh world读取Release API与Latest API，并通过公开URL下载四项插件资产；逐项大小和SHA-256均与
final staging一致。公开Core `veritrail-0.13.0-py3-none-any.whl`也重新下载并固定为
`95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04`。anonymous release/download
evidence SHA-256为
`2d5a03daf9bd874799cb03edc1c9e3a091e152814dfaa2d06a590fb630da7019`。

公开下载产品矩阵只使用这些公开字节，在Python 3.10.6与3.13.13中分别完成：

| 输入/能力 | Python 3.10.6 | Python 3.13.13 |
| --- | --- | --- |
| base wheel / metadata / import / CLI / `pip check` | PASS | PASS |
| normalized sdist build/install | PASS | PASS |
| `render` extra / Playwright / matching Chromium | PASS | PASS |
| normal public Release P2 | `COMPLETE` / PASS | `COMPLETE` / PASS |
| blocked-cleanup negative lifecycle | bounded return / terminal driver / zero residue | 同左 |
| plugin uninstall / Core 0.13.0 remains / `pip check` | PASS | PASS |

两个normal P2 Evidence的`collector_version=0.1.1`，normalization semantics仍为
`github-public-render-facts/0.1`，facts digest逐字相同：

```text
ea6c5f5a6af5f097cdf9a3525ed86631d849fb485321c5db503cfc210b6606fc
```

两个negative v3使用同一Plan digest
`b600e11f3ebc25eec2837df499a5e27d3d35f8e1e80a7fcfd957434b98d09ada`，分别约2.515秒与2.523秒返回；
两者都记录`playwright-driver:deadline-terminated`、driver terminal和空residual process集合。matrix SHA-256为
`afe60f39b05ce3bf496a2bedb6166a21477f431ded7e097674e256aba1b881a4`。

本节只声称冻结合同要求的公开下载产品读回。发行准备阶段的P1 -> P2 -> P3/Core formal继续由文档444所绑定的
新Plan、独立collection session与exact-source证据承担；本文不把normal P2单面读回冒充一条新的paired formal链。

## 5. retained non-success 没有被后继 PASS 删除

最终发行与公开读回期间新增并保留：

1. draft tag endpoint返回404，而draft与assets已由Release ID证实存在；
2. ad hoc `gh release list --json id`使用了不支持的字段；
3. body comparison v2错误剥离final newline，原始bytes实际相等；
4. 首个publish capture把draft `untagged-*` URL与published tagged URL当作稳定字段；
5. anonymous readback attempt 1误读validation summary的嵌套source commit；
6. downloaded-product attempt 1缺少HARD assertion，v2又把额外navigation放在deadline capture之外；
7. 对Python脚本误用PowerShell `ScriptBlock.Create`；
8. independent reconciliation的preformal review发现top-level `state`路径误写并在formal前修正；
9. CONTROL LOOP首次tree读取的PowerShell revision表达式被转码。

这些事实分别保留为setup/proof-facility error或preformal finding，qualification effect均为NONE。successor没有重复已成功的
下载、没有重新上传asset、没有重发Release，也没有把旧失败改名为PASS。

## 6. independent reconciliation 与有限 closeout

formal independent reconciliation重新读取fresh anonymous live Release/Latest API与remote refs，机械绑定source gates、tag、Release、
四项公开字节、双Python产品矩阵、normal/negative P2、uninstall/Core-only结果、retained failures与primary audit。其结果为PASS，
SHA-256为：

```text
d0e1a9597da9b08c9abd21d6fbc253482481637cecece96bb7805d1a80b8c995
```

随后建立271-artifact finite closeout与post-closeout integrity；二者SHA-256为：

```text
792a7df8126f8d5b633109b85aa461d79ce315d4d446f750a3ef4f54c4c6062f
9c9fde092d3114e35f49c780a111994680ad3c160452c1be93a275386f7924be
```

integrity复核0 mismatch；可重建venv显式排除，closeout与integrity均不作不可能的self-inclusion声明。

## 7. 本文自己的资格链

本文只允许README、AGENTS、本文与milestones四个docs-only文件变化。final bytes必须完成：

1. Markdown链接/格式、global/local hygiene、`git diff --check`与primary `audit.json`连续性；
2. exact base/head/tree、1 commit/4 files与original PR attempt 1 required gate；
3. protected exact-head merge与新exact-main Public CI 15/15、Browser Smoke 1/1；
4. 从新exact main建立fresh installed P1，并对README/doc441/doc442/doc443/doc444/本文/milestones执行anonymous
   raw/API/exact-Git readback；
5. independent reconciliation与finite closeout；
6. primary `audit.json`继续保持既定SHA-256。

全部成立后，本文才允许以下状态成为当前主线事实：

```text
GITHUB_EVIDENCE_0_1_1_RELEASED
GITHUB_EVIDENCE_0_1_1_PUBLIC_READBACK_COMPLETE
GITHUB_EVIDENCE_0_1_1_MAINTENANCE_FROZEN
```

这只是0.1.1公开产品坐标的状态发布。GitHub API、Release页面与download仍属于同一平台信任域，不是独立现实真实性权威；
普通CI与读回也不冒充Codex Security深扫或攻击路径验证。

## 8. 当前状态与后继停止线

本文自己的完整资格链闭合以前只能声明：

```text
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_EXISTS_READBACK_QUALIFIED_PENDING_STATE_PUBLICATION
GITHUB_EVIDENCE_0_1_1_PUBLIC_RELEASE_FACTS_PUBLICATION_CANDIDATE_NOT_QUALIFIED
R1_REVIEW_DERIVATION_MANIFEST_0_2_PRIVATE_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_GLOBAL_COMPOSITION_AUTHORITY_NOT_RESTORED_NOT_AUTHORIZED
R2_R6_NOT_STARTED
```

本文闭合后必须返回CONTROL LOOP。只有届时重新核对doc437问题、公开0.1.1 installed-product与现存冻结合同后，才可决定
doc437 successor、Manifest 0.2或更窄的下一条seam；不得按文档编号自动恢复global composition。`proof_is_not_problem_solving = true`、
`local_not_global = true`；R1完成后的human+AI全项目检查仍是独立后续目标。
