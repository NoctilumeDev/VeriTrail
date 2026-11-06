# R1 post-terminal Fact dual-successor 私有实现冻结发布

日期：2026-11-07

> 条件化状态目标：
> `R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@7049de0093f5967ea3dcce65d517b5daeea4123f`，tree
> `f11beb78d3262a783f03fc77e26f2fd3e8c23807`。
>
> 上游：[冻结合同](340-r1-post-terminal-fact-dual-successor-authority-recovery-contract.md)、
> [合同冻结发布](341-r1-post-terminal-fact-dual-successor-authority-recovery-contract-freeze-publication.md)、
> [可行性审计](342-r1-post-terminal-fact-dual-successor-private-implementation-feasibility-audit.md)、
> [授权发布](345-r1-post-terminal-fact-dual-successor-private-implementation-authorization-successor-publication.md)、
> [实现候选](346-r1-post-terminal-fact-dual-successor-private-implementation-candidate.md)、
> [读回资格恢复](365-r1-post-terminal-fact-dual-successor-private-implementation-readback-qualification-recovery.md)与
> [project-state projection 0.5冻结发布](370-r1-public-project-state-projection-0.5-freeze-publication.md)。
>
> 影响：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。本文不修改private runtime、tests、fixtures、workflow、Schema、
> Provider、Collector、P2/Core oracle、Verdict、Fact/Relation/Coverage semantics或任何frozen contract。

## 1. CONTROL LOOP 与本publication的唯一职责

PR #398已经把bounded private post-terminal dual-successor实现精确合入受保护主线，并完成original PR与new exact-main双门；
但它的旧fresh readback把已超过524288-byte窗口的完整milestones错误预注册为Public Render formal target，因此真实终结为
`PARTIAL / CONTENT_TRUNCATED`。PR #417随后只version readback target，以冻结的bounded project-state承担读者Render，并继续对完整
milestones做raw/API/Git全字节观察；该独立链闭合后，#398/doc346最多成为：

```text
IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN
```

doc365要求该新状态先通过versioned project-state rebind公开，再独立判断implementation freeze。0.4 candidate的exact-main required
gate与后继readback target各自暴露真实失败；两条失败链已经由doc368形成qualified history，且没有建立可授权的runtime/test defect。
0.5 successor与独立freeze publication随后分别完成自己的完整资格链。PR #422闭合后，
`R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN`已经生效，#418/#419 failure identity仍保持原状。

fresh CONTROL LOOP又从本发布基线机械复算：PR #398的五个implementation/test blob、doc340/doc341/doc342/doc345/doc346与其
冻结语义从implementation merge到当前exact main均未漂移；#417 readback qualification、0.5 projection freeze与primary
`audit.json`也都保持精确绑定。没有新反例击穿private implementation边界。

因此下一最小合法seam是本文：只把已经`IMPLEMENTED / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED / NOT_FROZEN`的固定实现候选，
通过一条新的docs-only完整资格链发布为`FROZEN`。本文不把“证明了固定实现”偷换成“解决了完整Review产品问题”，不改写原问题、
证明义务或适用world，也不恢复global composition authority。

## 2. Exact implementation qualification

```text
PR                   = #398
base                 = aa0cd335a98269dcdb843645f9643c0e7982a5c8
head                 = c1952d76f82808d2c9c7ccca719d32db20364000
ordinary merge       = 6a30957429c7b6a815608e8355893deb35873f24
candidate/merge tree = 81790b398fb3d07ed53d67269b80d99d94675807
diff                 = 1 commit / 9 files
```

original Public CI `41893051274`、exact-main Public CI `41898679833`与Browser Smoke `41898679711`均为attempt 1
SUCCESS，分别为11/11、11/11与1/1。final focused四格各174项，均为173 passed / 1 skipped；full Review Attention
四格各621项，Python 3.10.6两格为618 passed / 3 skipped，Python 3.13.13两格为619 passed / 2 skipped。
semantic audit四格逐字节一致：

```text
638b370d5cca5f3d8e854513386664de6e5ce33c5cea3796e29c8e2a48b69b16
```

pre-PR final seal、post-commit seal、original qualification、protected merge与exact-main dual-gate evidence SHA-256为：

```text
bf1637fdd55c90f6f63b7f30a81b68890314f8140ff76a61a77830dd42ec90c6
065df892d68953acad1a3f898804c8f5cb6751d52dcc4b32ddc116dbcbad44da
0ea0f6d03f2c8754406dbc608ee788073609cfd78811e1932e63fb977c0639f6
7d180c9fd03f9781bac0e4e6abc9cda6013b084d02d32cfb0d6ed5544ec9d57e
9e71515dec4eedcc0cdc6d621479ac74c2433ef209761cd3682899911d946b9d
```

本发布基线重新取得的五个blob与doc365固定值逐字节一致：

| path | blob SHA-1 |
| --- | --- |
| `_fact_fulfillment.py` | `cb8e25c7a2a93fac6f038c52cc62ac8019c6c2fe` |
| `_fact_relation_transition.py` | `57e672eeadb6741cc43f5478026bb76a98cd3aca` |
| `_fact_to_coverage_exact_input_handoff.py` | `241bc177247d4343e59001cef461710e3d61d475` |
| `_post_terminal_fact_dual_successor.py` | `68cbb622dbc9d33d0c88e6954f9db77ee16438ce` |
| `test_post_terminal_fact_dual_successor.py` | `3778f3c1c9b7bcbe8852ff0b5f35f0c615467215` |

## 3. Readback qualification recovery 与公开投影前置条件

PR #417以exact
`base=e0ab9d0679f1706cdde3103ef0e1076baa681b59 / head=d400a738e39c97e743ba7bec7315c68e9f534bb1 /
tree=f96b396e7bbdb42af9f4f6a75bbc8d730eede7af`合入`main@27f0b93eeb5ace7b5428ebc0c07cb1ebe4199f25`。
original Public CI `42191635218`、exact-main Public CI `42196105120`与Browser Smoke `42196105123`均attempt 1
SUCCESS。第三个fresh root中的README、project-state、doc345、doc346、doc364与doc365各自唯一formal均为API/Render
`COMPLETE`、HTTP 200与Core `PASS`；AGENTS/milestones raw/API/exact-Git逐字节一致。independent reconciliation、
177-artifact closeout、stdout self-capture mismatch与finite integrity为：

```text
b5a02d33ce7423c4173f4196326c5deafdd829f9a0d531cdb36b18cf6a50d448
d9d69aec5da9baf0dc48a5966ce6595ac85f6d88aa2a4d8edaa7a9f1ea7d04c4
46ac81de42273097329102a46be88d412084d8ef57b2e531842aa22c86cd8c0a
e526f7ca23ba0d9ef3d25eb44dd745466efc6fe215f52f58e45ae2ba2f7e478f
```

前两个fresh root中的anonymous API budget exhaustion与reader-visible marker selection failure均保留，Core Verdict没有创建；
旧#398 milestones truncation与#399 original gate failure也不被回填。

PR #422又以exact
`base=e132e422706fa96dfa1882587a726b9b48b072c2 / head=5477578190b17e4391a04d1da5b120ab41f5c792 /
tree=f11beb78d3262a783f03fc77e26f2fd3e8c23807`合入本发布基线。original Public CI `42298562890`、exact-main
Public CI `42302259402`与Browser Smoke `42302259372`均attempt 1 SUCCESS。fresh README、project-state、doc369与doc370
各唯一formal PASS，AGENTS/milestones raw/API/Git全字节一致。independent reconciliation、137-artifact closeout、expected
self-capture mismatch与finite integrity SHA-256为：

```text
84ad574bc4c899bf79572e7d0ff451d6054a3b32d8bacb7463810eef9b489298
cb84dac7460e48f409a0a3fa86ed480d5881f0b7688cd2a730e8f1a1e0cd0196
a958dd02bf784153c792216566a5af429b0e91e697763a33f52a92fc8e668eaf
45a4ab618dd669a00a94f018a4a2cfbf4f9a705911e698f7ec7c94340a81e2aa
```

因此0.5 projection/contract现在是`FROZEN`，但它只提供有界公开阅读投影；不会替本文授予implementation freeze。

## 4. 冻结对象与proof strength

本文冻结的只是doc340–346限定的versioned private `POST_TERMINAL_DUAL_SUCCESSOR_0_1`：

1. successor在Fact pre-terminal阶段只绑定original inputs、Policy/Profile、assignment、live context与shared slot，不签发route；
2. complete terminal source重验以后，`NORMAL_FULFILLED`只能claim existing Relation transition，四类negative只能claim exact-input
   successor 0.2；
3. 两条route共享同一个one-shot，wrong-route、validation failure、copy、replay、version mismatch、late stop与并发loss永久撤销，
   没有fallback；
4. Relation claimed-source与negative exact-input carrier都保持same attempt、original object graph、input seal、live context及既有
   downstream admission，不修改public/default路径或reason enum；
5. 八类private failure family、18项falsifier与旧consumer回归继续固定本实现适用world。

这只证明固定private selector与两个已冻结downstream在声明world内取得资格。它不证明application-level unified Review/Coverage
output admission、manifest successor、same-attempt Evidence continuity、persistence或public Review已经存在。测试、语义摘要和本发布
都不能把待证明命题从“fixed private implementation”漂移成“完整用户工程问题已经解决”。

## 5. 必须继续保留的non-success

后继PASS不得删除、改名或解释以下身份：

- implementation formal以前的required-provider terminal validation与typed replay两项private defect及其修正前日志；
- candidate local validation terminal blank-line failure、未覆盖untracked doc的proof-surface failure及旧146-artifact non-qualifying seal；
- wrong worktree/path/Python/PowerShell/glob/tree-expression与其他setup/proof-facility errors；
- #398 milestones `PARTIAL / CONTENT_TRUNCATED`与failed-readback closeout；
- #399 original required gate failure、`SAFETY_BUDGET_EXHAUSTED`、未合入head与lower cause `UNKNOWN`；
- #417前两个fresh root的formal ERROR、其无Verdict状态与underlying cause `UNKNOWN`；
- #418 exact-main required gate failure、decisive assertion `UNKNOWN_NOT_RETAINED_BY_TEST_OUTPUT`与lower cause `UNKNOWN`；
- #419 marker target failure及milestones `PARTIAL / CONTENT_TRUNCATED`；
- #420/#421/#422的全部setup、rate diagnostic、self-capture与Codex attachment-cap observations。

这些事实分别属于自己的exact world；none可以由本publication覆盖或拼接成另一门资格。

## 6. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc340–346、doc365、doc369、doc370、
`docs/project-state.md`、private runtime、tests、fixtures、workflows、Schema、Provider、Collector、P2/Core oracle与全部frozen
semantic bytes必须保持base不变。

本层local gates重核exact four-file scope、UTF-8 without BOM、LF/final LF、relative links、balanced fences、unique headings、
required markers、五个implementation/test blob、上游semantic doc、#398/#417/#422 coordinate与Artifact continuity、全部retained
failure identity、`git diff --check`、read-only global/local hygiene、focused unchanged-runtime witnesses及primary `audit.json` continuity。

```text
publication final bytes / declared local gates
  -> original publication PR gates
  -> exact-head protected merge
  -> new exact-main Public CI 11/11 + Browser Smoke 1/1
  -> fresh anonymous installed-product README / project-state / doc346 / doc365 / doc370 / 本文 Public Render
  -> fresh AGENTS / milestones raw+API+exact-Git byte observations
  -> independent Core / source-byte / identity / retained-history reconciliation
  -> target PRIVATE_IMPLEMENTATION_FROZEN becomes effective
  -> return CONTROL LOOP
```

publication自己的fresh Plan/session/Evidence不可复用#417或#422 readback；diagnostic不计入资格，任何non-success按原identity保留并停止。
本地checkout alignment与cleanup只属于housekeeping，不追加语义门。

## 7. 当前publication target与停止线

本文进入仓库不等于冻结生效。在自己的完整资格链闭合以前，只能记录：

```text
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_CONTRACT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_IMPLEMENTED_EXACT_MAIN_VERIFIED_READBACK_QUALIFIED_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_AUTHORITY_RECOVERY_PRIVATE_IMPLEMENTATION_FREEZE_PUBLICATION_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_5_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_4_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合后只使本文开头的`PRIVATE_IMPLEMENTATION_FROZEN` target成为事实。这个新状态会使projection 0.5成为历史投影；随后
必须从新的exact main返回CONTROL LOOP，先version/rebind current project-state，再重新审计application-level unified Review/Coverage
output admission。不得按文档编号自动恢复global composition authority或启动manifest、Evidence、persistence、public Review或R2–R6。
