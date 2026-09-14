# R1 Fact/Evidence 冻结后下一闭环系统审计

> 状态（本文最后门全部成立后）：`R1_FACT_EVIDENCE_CLOSURE_FROZEN /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED /
> R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 审计基线：`main@7141999383489f51cf6f87806d2d271496499584`
>
> 上游冻结事实：[R1 Fact Admission / DerivationEvidence Closure 实现冻结发布](158-r1-fact-evidence-closure-freeze-publication.md)
>
> 影响层级：`L2_CONTRACT_AUDIT + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`；本轮不修改 Schema、corpus、
> identity vector、源码、测试、依赖、CI、Provider、parser、publisher、Relation、Slice、Coverage、Manifest、
> CLI、Workbench、Core、P/Q/D、tag 或 Release

## 1. 审计问题与停止线

Fact/Evidence closure 已经证明一个 single-Provider closed test path 可以在同一 `BudgetContext` 与 attempt
eligibility 下形成：

```text
Provider candidate
  -> application-canonical Fact
  -> owned non-published FactSet construction state

or

verified non-success phase
  -> owned non-published DerivationEvidence projection
  -> one-shot future DIAGNOSTIC eligibility where allowed
```

它没有授权任何 R1 文件发布，也没有决定 real parser、multi-Provider、Relation、Slice 或 Coverage 谁先施工。
本轮只问：

> 哪一个尚未冻结的接缝，已经成为最多后继能力共同依赖、且最可能被后继实现反向改写的 authority
> bottleneck？

本轮比较 `DIAGNOSTIC publisher`、real parser、multi-Provider Fact composition、RelationSet、ReviewSliceSet、
CoverageLedger 与 COMPLETE publisher。选择一个候选只意味着下一步可从新 exact main 起草它的 docs-only
合同；不产生实现授权。

## 2. 冻结输入与当前实现没有漂移

审计开始时的关键文件 SHA-256 为：

```text
cdf948e44bd7d57b78bdaffbaf949af8df61d22d5ebe972c8864cbbf79fe32f0  docs/113-r1-deterministic-semantic-slice-contract.md
86b02ac5717190f7e12c720257ab6c46b996f427e048f19d1e631ad92b4bc8b3  docs/120-r1-schema-and-canonical-identity-contract.md
7d3580d74b658450d07aa0ca7987d7278fe5441064869b9a45601b698bf43044  docs/137-r1-derivation-attempt-and-fact-provenance-contract.md
e70bdde807fcb1795bdca8e49d04c664024495b7e3f76ec4c696fc4ea48e8834  docs/155-r1-fact-admission-and-derivation-evidence-closure-contract.md
5cf243c6b4b0701a7a561e3de55e6c3bc90e0febd74613afb2a4989bd1e66e8b  docs/158-r1-fact-evidence-closure-freeze-publication.md

101aed88a4155d5ae907bb43a822bd925e8a2f9b52df02a2366cb93ff7cecf4f  schemas/review-policy-0.1.schema.json
e33be9db7cae98d7ccdfc23bc95b71c81ad6921729c1ec1a81d708d590c288c1  schemas/review-fact-set-0.1.schema.json
397124031139d69f664445bd341be0139d0bed953487eb0cad796779ca8b4744  schemas/review-relation-set-0.1.schema.json
e51834585f5356e753c62c0a2e64b52f2bbac0d590586bb9dc924a832f092545  schemas/review-coverage-ledger-0.1.schema.json
69819c82b040271285d59e32c57edcec1116fe50a0df34e2d96d071036fa6b91  schemas/review-derivation-manifest-0.1.schema.json

5cb46458ddf23673fcf0a2fef197637074e7dda16a538bace0b4d95b5d1bb696  tests/fixtures/review-r1-schema-0.1/compatibility-cases.json
b202f0063b1d94a6edc7bf5c9e8aa30e24a76ff6584638bf416c7739ce1283df  tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json

98e70d07cebd2cba7f731177462e04a56f73d00436a1668cba5e3fd1ccbceff9  plugins/review-attention/src/veritrail_review/_fact_evidence_values.py
9f030b03cedfc82dfe614047cd6d1e54dd960ca0235cb663d6ee61aa93abd04b  plugins/review-attention/src/veritrail_review/_fact_evidence_closure.py
1e201b782437c3c7a42032d9788c3db98ea758013f7ae5d914521a91643f2538  plugins/review-attention/src/veritrail_review/publisher.py
```

当前实现事实继续是：

- `OwnedFactSetConstructionState` 只拥有规范 FactSet bytes/value 与 single-Provider provenance；没有 path、writer、
  Manifest role 或 public lifecycle；
- `OwnedDerivationEvidenceProjection` 只拥有 non-success Evidence bytes/value；
- `_DiagnosticClosureEligibility` 是与原 attempt、原 `BudgetContext` 绑定的一次性 private capability；
- 唯一现存 publisher 只发布 SourceSnapshot 单文件切片，不是 R1 Derivation 通用 publisher；
- `ReviewPolicy.provider_requirements` 封存 capability、required flag 与 `CUMULATIVE` composition mode，但不封存
  provider implementation identity；
- 当前 integrated controller 只接受一个显式 closed test `ProviderBinding`，同 subject 不兼容 candidate 会作为
  nonconformant single-source output 拒绝，不会生成 multi-source conflict。

本轮没有证据要求修改已经冻结的 Fact identity、FactSet digest、Evidence 0.1.1、Manifest 0.1 或
`ReviewPolicy.execution_budget`。

## 3. 当前依赖图

```text
SourceSnapshot + sealed ReviewPolicy + DerivationProfile
                         |
                         v
               Provider applicability
                         |
                         v
          one shared derivation BudgetContext
                         |
                         v
             Provider runs and candidates
                         |
                         v
      multi-source merge / conflict / availability join
                         |
                         v
                 stable FactSet input
                    /           \
                   v             v
             RelationSet   DerivationEvidence
                   |             |
                   v             |
            ReviewSliceSet       |
                   |             |
                   v             v
             CoverageLedger + final outcome
                         |
                         v
              COMPLETE eight-file publication
```

DIAGNOSTIC publication 从 non-success terminal branch 横向离开这条 normal path。它很重要，但不生产
Relation/Slice/Coverage 共同消费的 stable FactSet。

## 4. 候选接缝比较

| 候选 | 已冻结基础 | 仍缺的语义 | 反向约束 / 下游依赖 | 当前裁决 |
| --- | --- | --- | --- | --- |
| DIAGNOSTIC output coordinate / publisher | 四文件 Manifest shape、一次性 eligibility、预算与 create-new 原则 | exact output coordinate、writer ownership、错误分类、四文件 atomic publication | 主要关闭 non-success 留档；不稳定 normal Fact 输入 | 合法独立后继，但不是共同瓶颈；延期 |
| real Python parser | Python 3.10 profile、encoding/anchor 规则、candidate/application authority | parser applicability、built-in/authorized identity、partial AST、typed diagnostics、真实 bytes 读取边界 | 会产生真实 candidate，但不能决定多个来源怎样组成一个 FactSet | 过早；先冻结 provider composition authority |
| multi-Provider applicability + Fact composition | capability requirements、CUMULATIVE、Fact/conflict Schema、Evidence provider runs、single-Provider closure | provider set 的授权与基数、共享预算内的运行顺序、required/optional join、same-ID provenance merge、same-subject conflict、normal/diagnostic eligibility | 同时决定 FactSet、Evidence、Relation 输入、Slice conflict gate、Coverage UNKNOWN 与最终 outcome | **下一最小合同** |
| RelationSet | Relation Schema、首版 relation kinds、FactSet digest binding | 从哪些 admitted Facts 派生、parser/candidate relation provenance、resolution/UNKNOWN 与 relation conflict | 依赖先得到稳定 conflict-bearing FactSet；不能替上游决定来源组合 | 延期 |
| ReviewSliceSet | BFS、inclusive budgets、frontier、conflict 时 `slices=[]` | Relation traversal implementation、anchor eligibility、identity closure | 依赖 RelationSet 与 conflict propagation | 延期 |
| CoverageLedger | 七阶段账册、KNOWN/UNKNOWN denominator、typed gaps | 各阶段候选全集与完成/失败来源、upstream denominator closure | 消费所有上游；不应倒过来替 Provider/Relation 定义 completeness | 延期 |
| COMPLETE publisher | 八文件固定 Manifest、create-new/atomic 原则 | 七个后继 Artifact 的 final bytes、cross-reference、预算、writer/errors | 所有 normal derivation 后继共同出口 | 明确过早；禁止 placeholder 或第三种 outcome |

## 5. 审计发现

### 5.1 `provider_requirements` 尚不能唯一导出实际 Provider set

sealed Policy 当前只回答：

```text
capability_id
required
composition_mode = CUMULATIVE
```

运行 binding 另行携带：

```text
provider_id / provider_version
parser_id / parser_version
runtime_id / runtime_version
```

因此仍缺一个不可由调用者随意拥有的映射：

```text
sealed capability requirement
  -> exact applicable provider descriptors
```

如果两个实现分别选择一个 Provider 或两个 Provider，它们都可能满足同一 Policy shape，却产生不同
FactSet/Evidence identity。真实 parser 先进入公共路径会让第一个实现事实上冻结这个选择，因此必须先决定
Provider set 的 authority：固定 built-in descriptor、独立版本化 authorization Artifact，或其他可复算边界。
本审计不替合同预选答案，但明确禁止 ambient discovery、entry-point 扫描或 caller-supplied arbitrary provider
成为隐含权威。

### 5.2 一个共享预算不能退化成“每个 Provider 一份预算”

文档 137 已冻结 whole derivation 只消费一份 `ReviewPolicy.execution_budget`。multi-Provider runtime 因此必须
继承同一绝对 deadline、memory containment 与 inclusive artifact budget；不能：

```text
Provider A -> new full budget
Provider B -> another full budget
```

否则 Provider 数量会偷偷放大执行权。合同还必须冻结首版运行顺序或证明结果与运行顺序无关；并发调度不能因
Q 蓝图存在而进入 R1。Q 不拥有 R1 Provider execution semantics。

### 5.3 cumulative composition 不是数组拼接

冻结规则至少要求区分：

```text
same fact_id, same semantic content
  -> one Fact identity
  -> provenance_refs = sorted unique union of all reporting ProviderRuns
  -> each reporting run still reports that fact_id

same subject_key_digest, incompatible fact_id/content
  -> preserve all candidates
  -> create deterministic FactConflict
  -> never last-write-wins

successful empty source
  -> contributes an observed empty set
  -> does not cancel another source's Facts
```

现有 single-Provider admission 把同 subject 不兼容值判为 Provider output nonconformance，这是当前 profile 的正确
行为；multi-Provider contract 不能通过删除该检查直接“顺便支持冲突”。它需要一个更晚的 derivation-level
composition boundary，先分别验证各 run 的 canonical candidates，再跨 run 合并。

### 5.4 required/optional status join 同时约束 Artifact eligibility

必须保持：

- required Provider 成功且为空，是成功来源事实；
- required Provider 不可用、失败或 nonconformant 时，成功来源的已观察前缀不能获得 normal FactSet publication
  identity；final reported arrays 必须服从 DIAGNOSTIC file set；
- optional Provider 失败不能从 Evidence 中消失，也不能删除它已造成的冲突；
- optional Provider failure 在没有其他 blocker 时不能单独把 frozen overall join 改成 non-completed；但它仍须
  留在 Evidence，并由后继 Coverage 保留缺口，不能被实现默认“忽略 optional”；
- conflict 是内容组合事实，不自动等同 execution failure；现有冻结文本允许 protocol `COMPLETE` 同时携带
  conflict，并要求 Slice 空集与 Coverage `UNKNOWN`。后继不得把冲突改写为 last-write winner 或直接变成
  Provider failure 来绕开这一语义。

### 5.5 Relation 不能成为 multi-source 冲突的解释器

RelationSet 必须消费一个已经完成来源合并、provenance union 与 conflict construction 的 FactSet。若 Relation
实现先行，它会被迫自行决定：

```text
冲突候选选哪一个？
不受冲突影响的 Fact 能否继续派生？
一个 Provider 缺失时，已知 Facts 是否代表完整分母？
```

这些不是 Relation authority。下一合同只需建立稳定的 conflict-bearing FactSet construction state 和
Evidence join，不需要提前定义 Relation 算法；Relation 后继再决定它在 frozen upstream state 上能做什么。

### 5.6 Coverage 是消费者，不是上游 completeness 的补丁

CoverageLedger 已冻结 `KNOWN / UNKNOWN` denominator、typed gap 和七阶段依赖链。它可以诚实保存 Provider
不可用、冲突或上游分母未知，但不能在上游只给出成功子集时自己猜“完整全集”。因此：

```text
Provider composition closes source set
  -> Fact derivation denominator may become knowable
  -> Relation/Slice derive their own candidate sets
  -> Coverage records the result
```

不能倒置成：

```text
Coverage needs a number
  -> silently treat observed Facts as the denominator
```

### 5.7 DIAGNOSTIC publisher 是真实能力，但当前不是 normal-path blocker

文档 155 已经为合法 non-budget non-success 冻结 one-shot eligibility 与预算约束。下一份 publisher 合同可以
独立关闭：

```text
owned exact inputs + final non-success Evidence
  -> reserve exact four-file bytes
  -> staged verify
  -> atomic create-new DIAGNOSTIC directory
```

但先完成它只会让失败 attempt 可公开留档，不会回答 normal FactSet 由哪些 Provider 构成，也不会让 Relation、
Slice 或 Coverage 获得稳定输入。本审计因此不否定它，只把它保留为正交后继，不让“已有 eligibility”被误读成
“必须最先实现 publisher”。

## 6. 选定的下一个最小合同闭环

下一步从本文最终合入后的新 exact main 起草一个独立 docs-only：

```text
R1 Multi-Provider Applicability and Fact Composition Contract 0.1
```

合同至少必须回答：

1. sealed `provider_requirements` 怎样导出 exact applicable Provider descriptor set，谁拥有这个映射；
2. 一个 capability 允许几个 Provider、同一 `(capability_id, provider_id)` 怎样保持唯一；
3. Provider set、运行顺序与 operands identity 怎样规范化；
4. 所有 Provider 怎样消费同一个 `BudgetContext`、absolute deadline 与 attempt identity；
5. required/optional Provider 的 `COMPLETED / INTERRUPTED / FAILED / UNAVAILABLE` 怎样机械汇合；
6. successful empty source、same-ID same-content、same-subject incompatible-content 怎样分别组合；
7. canonical Fact 的 provenance union、ProviderRun reported IDs 与 FactSet membership 怎样双向闭合；
8. `FactConflict` identity、candidate ordering 与 provenance union 怎样复算；
9. conflict、required-source unavailable 与 optional-source failure 怎样影响 normal continuation、diagnostic
   eligibility 与后继 denominator；
10. 哪些结果只形成 owned non-published construction state，禁止提前发布哪些 Artifact；
11. 哪些单变量向量必须证明 Provider 顺序不改变 semantic FactSet/conflict identity；
12. 现有 Schema/Policy 是否足够，若不够，只重开被反例击穿的最小字段或合同条款。

该合同即使冻结，也最多授权 closed deterministic multi-Provider test path、private Fact composition 与 Evidence
join。它不能自动授权 real parser、public Provider SPI/discovery、DIAGNOSTIC publisher、Relation、Slice、
Coverage、COMPLETE publisher、CLI 或 Workbench。

## 7. 最小反例矩阵

| # | 单变量反例 | 错误推理 | 必须保持的裁决 |
| ---: | --- | --- | --- |
| 1 | 同一 Policy 下 runtime 任选一个或两个实现 | capability 已 sealed，所以 Provider set 唯一 | 先冻结 capability -> descriptor set authority |
| 2 | A 与 B 各获得完整 wall-clock budget | 每个 Provider 都 bounded，所以 whole derivation bounded | 所有 run 只消费同一绝对预算 |
| 3 | A 空成功、B 报告 Fact | A 没结果，所以整体没结果 | 保留 A 空来源事实与 B Fact |
| 4 | A/B 报告同一 `fact_id` | 保留两份相同 Fact 或只留先到者 | 一份 Fact identity，provenance/reporting 双向并集 |
| 5 | A/B 对同 subject 报告不兼容内容 | 按 Provider priority 选一个 | 保留候选并形成 deterministic conflict |
| 6 | optional B 造成 conflict | optional 可以忽略 | conflict 不因 optional 删除 |
| 7 | required B 不可用，A 已成功 | 发布 A 的较小 FactSet | 无 normal FactSet publication；Evidence 保留失败 |
| 8 | optional B 不可用，required A 成功 | 完全删除 B | Evidence/Coverage 必须保留缺口 |
| 9 | Provider 完成顺序交换 | completion order 改变数组与 digest | 规范排序；semantic composition identity 不漂移 |
| 10 | single Provider 内同 subject 不兼容 | 直接生成 multi-source conflict | 仍是 nonconformant single-source output |
| 11 | conflict-bearing FactSet 进入 Relation | Relation 自己挑 candidate | Relation 不拥有上游冲突裁决权 |
| 12 | Coverage 只看到成功前缀 | 用已知前缀缩小 denominator | `UNKNOWN` 不得被重新命名为较小的 KNOWN |
| 13 | 先实现 real parser | 第一套 parser binding 自然就是标准 | parser applicability 必须先有权威来源 |
| 14 | 先实现 DIAGNOSTIC publisher | 失败可留档，所以 normal path 已闭合 | publisher 与 source composition 正交 |
| 15 | 先实现 COMPLETE publisher | 其余文件以后补 | 禁止 placeholder、partial directory 或第三种 outcome |

## 8. 本轮不改的边界

- Fact/FactSet semantic identity 与 run provenance 继续正交；
- `DerivationEvidence 0.1.1` 与 Manifest 0.1 字节不因本审计自动升级；
- `COMPLETE` 继续固定八文件，`DIAGNOSTIC` 继续固定四文件；
- terminal stop 后不恢复 Artifact work；已有 DIAGNOSTIC eligibility 不等于 publisher 已存在；
- real parser 的 encoding、anchor、partial AST 与授权模型继续延期；
- Relation 的 resolution/topology、RelationConflict 与局部 conflict-free traversal 继续延期；
- Slice、Coverage、CLI、Workbench、R2–R6、Q 与 D 不进入本闭环；
- Q 不负责 R1 Provider 排序、并行或预算语义，D 不为产品体验反向扩大 R1。

## 9. 本地审计证据

本轮从 clean independent worktree
`docs/r1-next-closure-system-audit@7141999383489f51cf6f87806d2d271496499584` 完成：

1. 读取 `README.md`、`AGENTS.md`、文档 00–03、113、120、137、155、158；
2. 复算第 2 节关键合同、Schema、corpus 与实现文件 SHA-256；
3. 审计 `ReviewPolicy.provider_requirements`、FactSet/RelationSet/CoverageLedger/Manifest Schema 的真实字段；
4. 审计 R1 compatibility corpus 中 cumulative composition、conflict、typed gap 与 interrupted publication
   obligations；
5. 审计 private integrated controller、one-shot diagnostic eligibility 与现存 SourceSnapshot-only publisher；
6. 建立第 3–7 节依赖、候选、authority 与反例矩阵。

本轮没有运行新的 runtime probe，因为当前结论来自冻结 bytes 间已经存在的组合约束，不需要为“多找一个问题”
制造新执行事实。后继合同应为 multi-Provider composition 补纯数据 conformance vectors；本审计不预造 fixture。

既有 Schema / identity / Evidence correction 边界从当前 worktree 绑定 `src`、plugin `src` 与 test root 后重跑：

| Runner | 结果 |
| --- | ---: |
| CPython 3.10 normal | `27/27` |
| CPython 3.10 `-O` | `27/27` |
| CPython 3.13 normal | `27/27` |
| CPython 3.13 `-O` | `27/27` |

裸解释器与既有通用 venv 的首次预检均因没有安装 `pytest/jsonschema` 而没有进入测试；该环境事实没有被记成
产品失败或测试通过。最终四格使用当前 worktree 内两套 Git 忽略的临时 venv，只安装锁定
`jsonschema==4.25.1`，并在 fresh process 中打印实际 `veritrail` / `veritrail_review` import coordinate 后执行
标准库 `unittest`。

本文变更范围只允许：

```text
AGENTS.md
README.md
docs/milestones.md
docs/159-r1-post-fact-evidence-next-closure-system-audit.md
```

并必须通过 relative Markdown links、fence、敏感/本机路径、exact scope 与 `git diff --check` 检查。它们只证明
审计材料自洽，不替代本文自己的远端 Public CI、Browser Smoke、受保护主线合入与 exact-main 公开读回。

## 10. 生效条件与 Fresh-Agent 交接

本文只有在以下事实全部成立后才成为当前审计基线：

1. docs-only PR 的原始 Public CI 完整通过；
2. PR 合入受保护 `main`；
3. 新 exact main 的 Public CI 与 Browser Smoke 通过；
4. 从新 exact main 对 README、本文与 milestones 完成 fresh anonymous public readback；
5. 读回使用 R1 本次审计专属 Evidence identity，不能复用 P4、Fact/Evidence freeze 或其他 claim label。

此前只能称本文为 audit candidate。最后门成立后，新的、没有聊天上下文的 Agent 应：

1. 读取 README、AGENTS 与文档 113、120、137、155、158、本文；
2. 从新的 exact main 建立独立 docs-only multi-Provider contract worktree；
3. 先用反例关闭 Provider applicability、共享预算、required/optional join、Fact merge/conflict 与 Evidence
   reported-ID closure；
4. 若发现 Policy/Schema 不足，只修正被单变量反例击穿的最小边界，不用“latest wins”覆盖冻结历史；
5. 合同没有完成自己的候选门、合入、exact-main 门、匿名读回与独立冻结发布以前，不开始实现；
6. 不创建 real parser、public Provider SPI/discovery、publisher、Relation、Slice、Coverage、CLI、Workbench 或
   COMPLETE Manifest。

本文最后门全部成立后，当前状态才可写成：

```text
R1_FACT_EVIDENCE_CLOSURE_FROZEN
R1_MULTI_PROVIDER_FACT_COMPOSITION_PRECONTRACT_AUDITED
R1_MULTI_PROVIDER_FACT_COMPOSITION_CONTRACT_NOT_STARTED
R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

审计选择 multi-Provider applicability and Fact composition，是因为它关闭最多后继共同依赖的 source-set、
provenance、conflict 与 availability authority；不是因为它在架构图上排在 Relation 前，也不表示其他候选没有
价值。任何新的反例仍可否决该选择或只重开被击穿的最小边界。
