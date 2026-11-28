# R1 global composition CI budget correction reader-visible failure-boundary audit

日期：2026-11-29

> 状态：
> `R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@c53082451a69a544703bd5b28ec03257b6727c32`，tree
> `67a2332a5116f6341a679399f5cea1f4f4ee0077`。
>
> 受审对象：PR #533 / doc468在original与exact-main双门成功后的fresh README reader-visible diagnostic failure。
>
> 影响：`L3_QUALIFICATION_BOUNDARY + L0_PUBLIC_DOCUMENTATION`。本文只保存失败identity、公开可见性边界、资格影响与最小后继责任；
> 不修改PR #532失败历史、doc467实现、doc468 correction语义、workflow、runtime、tests、fixtures、Schema、Provider、Collector、
> P2/Core oracle、Verdict、persistence或public Review，也不把失败候选升级为qualified history。

## 1. CONTROL LOOP进入点

PR #531的完整资格链已经使`R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_ALLOWED`生效。PR #532随后把
[文档467](467-r1-global-composition-authority-private-implementation-candidate.md)与bounded A–J private implementation精确合入
`main@2d56c97db41a208d999bad017cb00cf99c48f66e`，但exact-main Public CI `46158724296` attempt 1在Python 3.10
optimized Review Attention job运行约45分钟后被外层job预算取消。两个Windows barrier jobs随后按设计拒绝cancelled prerequisite，
四个下游jobs被跳过。该world没有rerun，也没有fresh readback；doc467因此仍`NOT_QUALIFIED / NOT_FROZEN`。

fresh CONTROL LOOP只重开失效的proof-facility外层预算。PR #533的
[文档468](468-r1-global-composition-authority-exact-main-ci-budget-correction.md)只把
`jobs.review-attention.timeout-minutes`从45改为60；725项test denominator、四格Python矩阵、inner deadline、required barrier、
fail-closed顺序、job名称与全部产品源码/test bytes保持不变。该maintenance不能回填PR #532，也不能自动资格化doc467。

## 2. PR #533 exact candidate与自动门

```text
base    = 2d56c97db41a208d999bad017cb00cf99c48f66e
head    = 14b6804bd390f9b39c6209cf773f4d260031ef24
tree    = 67a2332a5116f6341a679399f5cea1f4f4ee0077
merge   = c53082451a69a544703bd5b28ec03257b6727c32
parents = 2d56c97db41a208d999bad017cb00cf99c48f66e,
          14b6804bd390f9b39c6209cf773f4d260031ef24
scope   = .github/workflows/ci.yml
          README.md
          AGENTS.md
          docs/468-r1-global-composition-authority-exact-main-ci-budget-correction.md
          docs/milestones.md
```

local validation、Python 3.10/3.13 × normal/`-O` docs hygiene与exact-scope proof均PASS。original Public CI
`46164727472` attempt 1为15/15 SUCCESS；protected exact-head merge形成上述new main。new exact-main Public CI
`46170029735` attempt 1为15/15 SUCCESS，Browser Smoke `46170029613` attempt 1为1/1 SUCCESS；没有rerun。

local qualification、precommit seal、original qualification、protected merge与exact-main gate seal SHA-256依次为：

```text
52a40b4b334dcb0975a14053588a3a157ba0f46f1cb5f3b21edf5e87b16625cc
50d79381f649fcc3086d465a235a5a9edf917f134fa1179bd58dd6d0644ef753
486e03784a6d91456db367454c26df1fae507a936a37a986e74ad0fc50bbd0c5
47faf3ff89aac6d7ec7be01d898a2b330b6a16c9f08f8745b0d08096a7c9d5b4
22f34ace81665f912f82a77d461f5b47871e40030f21508891bd8aa6b4f32f3c
```

这些门只证明各自exact world。它们不能替代fresh installed-product readback，也不能把PR #532改写成PASS。

## 3. fresh readback world与setup identities

fresh detached worktree只认`c530824…`world。Python 3.13.13环境从公开Core 0.13.0与GitHub Evidence 0.1.1 wheel建立；
exact source、remote main、candidate/original/merge/gate identities与primary `audit.json`均重新核对。facility preparation与offline static
validation SHA-256为：

```text
30e6394304043d94031f41e7a6a95f6d21d16355e06ead93e9e94b837efcf59d
67c918ff24d870b87d30051dbf952c41585103edc6f07a6aa4448f7b05d7b551
```

anonymous rate diagnostic #1为HTTP 200、remaining 60；API preflight #1为HTTP 200、remaining 59。没有使用认证替代。
以下setup identities全部保留，qualification effect均为`NONE`：

- fresh readback worktree与本audit worktree的侧栏登记都因本聊天累计超过100个attachment identity失败；checkout本身创建成功；
- 第一次marker-cardinality inspection只返回输出截断提示，没有产生可用计数；bounded successor核得六个marker各唯一一次；
- 第一次`HEAD^{tree}`查询未使用字面参数边界，被PowerShell干扰；successor重新核得exact tree、parents、clean detached state与remote main；
- copied PR #531 proof-facility在任何匿名观察前显式重绑为PR #533 correction world，没有复用旧PASS。

本audit candidate施工期间的multi-file patch因milestones context不匹配被原子拒绝，没有产生修改；后继分文件patch成功。milestones第一次
append又因重复句锚点落在更早section，inspection在validation与commit前发现并机械移到当前文件末尾。local validation attempt 1随后因
porcelain helper的`.strip()`移除首行status前导空格，把`AGENTS.md`误解析成`GENTS.md`；其余检查与hygiene 8/8均PASS。attempt 1保持
`NON_SUCCESS`，versioned v2只修正raw status读取并改用新log identity，PASS SHA-256为：

```text
b415c5aaa7d90710703b035226b17c2d50664fd6a7d207820b7d55227cf467e9
```

这些都是proof-facility/setup identity，不能冒充产品反例，也不会被后继final validation删除。

## 4. README diagnostic直接反例

README diagnostic immutable identity为：

```text
identity              = r1-p533-gcacibc-diagnostic-readme-1-c530824
coverage              = COMPLETE
top-level HTTP status = 200
reader marker count   = 0
Core Verdict          = NONE
classification        = DIAGNOSTIC_ONLY_NON_QUALIFYING_ERROR
```

预注册reader marker是`R1 global composition authority exact-main CI budget correction`。exact README source在第1182行唯一包含该
doc468入口；GitHub默认Public Render的稳定content window中该reader marker出现0次。相同proof facility随后对doc467与doc468分别取得
`COMPLETE / HTTP 200 / marker=1`的唯一diagnostic。因而现有证据不支持网络、API、Render collector或目标文档不可用；它只支持：

```text
README_CORRECTION_PROJECTION_OUTSIDE_PUBLIC_RENDER_VISIBLE_WINDOW
lower platform mechanism = UNKNOWN
```

不能把source中的唯一链接等同于默认reader-visible公开投影，也不能换用与correction无关的顶部短语来冒充观察成功。

20-artifact non-success capture SHA-256为：

```text
a2cb7b4c7e446f36282f7db0e9bcba697c584194241f04d82e9594ef0135b334
```

README formal、三个Render target的formal以及AGENTS/milestones raw-byte observation均未启动；没有Core Verdict、independent
reconciliation、finite closeout或任何qualifying readback。不得重跑该README diagnostic，不得复用doc467/doc468的diagnostic PASS，
也不得把它们拼进后继exact world。

## 5. 当前资格影响与authority ceiling

机械状态只能是：

```text
doc468 = MERGED / ORIGINAL_GATE_PASS / EXACT_MAIN_DUAL_GATES_PASS /
         READBACK_NOT_QUALIFIED

doc467 = MERGED / NOT_QUALIFIED / NOT_FROZEN
global composition authority private implementation = STARTED / NOT_QUALIFIED / NOT_FROZEN
public Review = NOT_STARTED
R2-R6 = NOT_STARTED
```

PR #532的CANCELLED/FAILURE/SKIPPED链、gate artifact
`90cd4da3963429ac479f54d44edc648fce3539a32b2d272ec8a0ece8615e1ba1`与non-success capture
`259979d3de37d74c88ba39edbb2056a8ef36681ed762f0d63fffdd72e9b86bf7`继续保持原identity。PR #533的readback反例既不解释
PR #532 lower cause，也不被它解释；两个world不得拼接。

## 6. 禁止的伪恢复

```text
retry r1-p533-gcacibc-diagnostic-readme-1-c530824 until marker appears
replace the marker with an unrelated visible phrase while leaving doc468 correction hidden
change the proof facility to scroll, expand or search a state the default reader cannot see
splice PR #533 green gates with another exact-main readback world
reuse doc467/doc468 diagnostic PASS as formal qualification
rewrite PR #532 as PASS or doc467 as qualified/frozen
increase timeout again without a new counterexample and new exact identity
modify runtime/tests/oracle to make a documentation projection failure disappear
start public Review, external open-source integration, R2-R6 or the post-R1 whole-project review
```

理论遇到反例时先检查前提，而不是不断增加例外。本次被击穿的前提是“raw Markdown中的doc468链接等于默认reader-visible公开状态”；
因此最小重开对象是public projection责任，不是P2 oracle、doc467实现、CI预算或产品语义。

## 7. 最小合法后继seam

恢复必须串行进行：

1. 本docs-only failure-boundary audit先取得自己的完整资格，只固定PR #533 dual-gate成功、README reader-visible failure与authority ceiling；
2. 返回fresh CONTROL LOOP，从新的exact main建立独立public-projection correction；
3. correction只能让doc468未资格化、doc467未冻结及本failure boundary在README默认读者可见区准确出现，并重新绑定fresh readback；
4. correction闭合后仍须返回CONTROL LOOP建立独立implementation qualification recovery，不得继承PR #532或#533资格。

局部diagnostic成功不等于全局readback资格；doc467/doc468 marker=1不能覆盖README marker=0。

## 8. 本audit candidate的精确scope

tracked scope只允许：

```text
README.md
AGENTS.md
docs/469-r1-global-composition-ci-budget-correction-reader-visible-failure-boundary-audit.md
docs/milestones.md
```

doc467、doc468、workflow、runtime、tests、fixtures、Schema、Provider、Collector、P2/Core oracle、Verdict、persistence与全部frozen semantic
bytes必须保持`c530824…` base bytes。README只公开记录失败状态与本文入口；它不重试或修正doc468资格。

local gates至少核对exact four-file scope、UTF-8 without BOM、LF/final LF、links/fences/headings、reader-visible README audit marker、
PR #533 exact identities、retained readback counterexample hash、unchanged workflow/product/test/history bytes、`git diff --check`、read-only
global/local hygiene与primary `audit.json` continuity。

## 9. 本audit自己的资格链

```text
final docs-only audit bytes / declared local gates
    -> original PR required Public CI
    -> protected exact-head merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / doc467 / doc468 / 本文 Render observations
    -> fresh AGENTS / milestones raw.githubusercontent + Contents API + exact-Git observations
    -> independent reconciliation
    -> finite closeout
    -> READER_VISIBLE_FAILURE_BOUNDARY_AUDITED becomes qualified history
    -> return CONTROL LOOP
```

全部门闭合以前，本文只是candidate。闭合后也只允许进入独立public-projection correction；不得自动资格化doc468/doc467、冻结
implementation、启动public Review或R2–R6。

```text
R1_GLOBAL_COMPOSITION_AUTHORITY_CONTRACT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_ALLOWED
R1_GLOBAL_COMPOSITION_AUTHORITY_PRIVATE_IMPLEMENTATION_CANDIDATE_MERGED_NOT_QUALIFIED_NOT_FROZEN
R1_GLOBAL_COMPOSITION_AUTHORITY_EXACT_MAIN_CI_BUDGET_CORRECTION_MERGED_DUAL_GATES_PASS_READBACK_NOT_QUALIFIED
R1_GLOBAL_COMPOSITION_AUTHORITY_CI_BUDGET_CORRECTION_READER_VISIBLE_FAILURE_BOUNDARY_AUDIT_CANDIDATE_NOT_QUALIFIED
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

`proof_is_not_problem_solving = true`、`local_not_global = true`、
`post_r1_human_ai_global_check_required = true`；R1完成后仍必须由人类+AI共同执行独立全项目检查。
