# R1 Parse product → Fact consumer binding 最小前合同审计

> 状态：`R1_PARSE_PRODUCT_FACT_CONSUMER_BINDING_PRECONTRACT_AUDITED /
> R1_PARSE_FULFILLMENT_CONTRACT_CANDIDATE /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED / NO_RUNTIME`
>
> 基线：`main@34b58014b1eadd0b30bc4deb73ab2cc97e2ed675`
>
> 证据坐标：文档 215 已完成 original PR、受保护合入、new exact-main 双门、fresh installed-product
> readback 与 independent reconciliation；本文只审计 admitted Parse product 成为 Fact consumer input 以前的
> product identity、reconciliation、least-authority 与 multi-Provider seam。

## 1. 结论

[文档 215](215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)的最后门已经闭合，
`R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDITED` 可以作为 qualified history 使用。重新进入
CONTROL LOOP 后，当前最小问题进一步拆成三层：

```text
consumer membership
    = 哪些 Parse obligations 已经 ACCEPTED 并有资格进入 Fact

exact product binding
    = 这些 members 绑定的是哪一个 admitted Parse product

product consumption authority
    = Fact Provider 取得并受约束于该 product，而不是只回显 identity 后重读 raw source
```

accepted subject IDs 只能回答第一层的一部分；product digest 只出现于 request/terminal 也不能证明第三层。current
`private-source-operation-projection/0.1` 与 Fact wire `/0.2` 的 authority object 仍是 source body，不能通过增加一个
product 字段静默变成 post-Parse consumer wire。

因此最小合法顺序不是直接起草 consumer correction contract，而是：

```text
Parse minimal contract
    -> complete denominator reconciliation
    -> application-owned admitted product / product-set semantics
    -> same-attempt exact product access boundary

future Fact consumer correction contract
    -> provider-bound product consumer projection
    -> provider-bound one-shot request claim
    -> Fact output / continuation binding
```

这不是把 Parse 与 Fact 合并成一个合同。它只确认 consumer contract 不能在 upstream product identity 尚未冻结时，
先以 placeholder 方式拥有它。本文不冻结 Parse contract，不起草 correction contract，不实现 parser、AST、product
carrier、Fact 或新 wire。

## 2. 文档 215 的资格链

文档 215 候选 PR #238 的坐标为：

```text
base  = 5593f48256acafeda6205ffde174441781c87c2e
head  = fdc3c3222615cf63eb1d98abf25706295ec25a33
merge = 34b58014b1eadd0b30bc4deb73ab2cc97e2ed675
tree  = 37a75ee670d0f1bd288486d351a137c353beaa85
```

PR original Public CI `36406936981` attempt 1 为 11/11 SUCCESS。new exact main 的 Public CI
`36409451476` attempt 1 为 11/11 SUCCESS，Browser Smoke `36409451412` attempt 1 为 1/1 SUCCESS。

README、文档 215 与 milestones 使用三个 fresh Plan/session 完成 anonymous installed-product readback：

| Path | Plan | Session | Result |
| --- | --- | --- | --- |
| README | `r1-parse-fact-prereq-readme` | `github-paired-b5196e986b034460b18b3cce5976f296` | `COMPLETE / PASS` |
| doc215 | `r1-parse-fact-prereq-doc215` | `github-paired-b5ca44da50714445af65a85c17fedb0b` | `COMPLETE / PASS` |
| milestones | `r1-parse-fact-prereq-milestones` | `github-paired-b0c38e88cd444f0abc9a093b2f1ca2bf` | `COMPLETE / PASS` |

三份 observation 均为 exact-SHA HTTP 200、三样本稳定、唯一 marker、零 active stream / cleanup error / conflict。
四份 public raw bytes 与 exact Git blobs 相等。独立 verifier 重新核对 original PR、merge/tree、exact-main gates、
Plan-before-observation、Core fields 与 source bytes，final manifest 为：

```text
sha256_json  = 4acc88bb15f35b7b362f9feacd446277547d82625e13f89a207390496f5dab79
sha256_bytes = 12a8004834b3b083f6a25f309666c8852cde7a8d062103907e2545e96ea9e80e
```

正式 readback 没有 ERROR。readback 前的 proxy TLS EOF、direct DNS failure、一次 stale progress assumption、仓库外
`gh run view` 漏传 `-R` 与 Playwright diagnostic shutdown warning 保持 setup/preflight identity，不升级为产品
observation，也没有被后继 PASS 删除。

## 3. Current source topology 只能绑定 source-body attempt

current runtime 与文档 208 的历史合同一致：

1. `build_fact_derivation_source_operation_projection()` 令 `operation_subject_ids` 等于全部 Language Support
   `ELIGIBLE` subjects；
2. `build_fact_source_operation_request_document()` 复制这些 subjects 的 exact raw blobs；
3. corrected operands 绑定 Snapshot / Policy / Profile、Provider descriptor、Language Support function / classification
   与 source-operation projection；
4. worker validator 要求 operation set 与 body set 的 cardinality、顺序、path、size、SHA-256、base64 恰好相等；
5. parent gate 绑定 original `BudgetContext`、parent `AttemptEligibility`、classification 与 exact input seal；每个
   Provider child 另有 one-shot eligibility 与 request-frame claim；
6. terminal 只回显 provider descriptor、operands digest 与 provider-run identity，并核对 reported Fact provenance。

这些约束能证明：

```text
this source-body request
    belongs to this provider child
    under this live parent attempt
```

但 current request、gate 与 terminal 都没有 Parse result/product 输入，因此不能证明：

```text
this Fact output
    consumed this admitted Parse product
```

强 attempt binding 不能补足缺失的 product dependency。

## 4. 四种 world 的 consumer qualification

Parse denominator 继续来自 exact Language Support `ELIGIBLE` subjects。post-Parse consumer input 必须由该
denominator 的 application-owned complete reconciliation 导出，而不是由 Provider output、caller subset 或
accepted IDs 单独定义。

| World | Parse reconciliation | Consumer semantic input资格 | 不能推出 |
| --- | --- | --- | --- |
| full accepted | 每个 denominator member 恰好一个 admitted success/product | 全部 admitted products 可进入 candidate product set | Fact 已完成或 Coverage closed |
| partial accepted | accepted 与 rejected 都完整、无 duplicate/dangling/cross-attempt | 仅 accepted members 的 admitted products 可进入 candidate product set | rejected raw bodies 可继续暴露 |
| all rejected | 每个 member 都有 admitted semantic rejection | known-empty admitted product set | Fact child 必须启动或 Fact/Coverage `CLOSED_EMPTY` |
| missing / parser non-success | 至少一个 obligation 未形成 admitted semantic terminal | normal consumer input 不成立 | empty accepted set 等于 known-empty |

duplicate、dangling、foreign-attempt 或同一 obligation 多 terminal 也不能被“取 accepted subset”修复；它们使正常
product-set reconciliation 不成立。diagnostic path 是否消费部分 observation 是另一条 authority，不得冒充 normal
Fact continuation。

## 5. accepted membership 不等于 exact product identity

两个 Parse worlds 可以具有同一 accepted subject set，却产生不同 product semantics：

```text
subject A -> ACCEPTED -> product P1
subject A -> ACCEPTED -> product P2

accepted subject IDs in both worlds = [A]
```

若 consumer projection 只保存 `[A]`，两者 canonical bytes 与 digest 完全碰撞。future binding 至少必须把每个
accepted subject 与 exact admitted product identity 共同纳入 application-owned product-set identity。

product identity 也不能脱离以下坐标成为一个裸 digest：

```text
exact subject / blob identity
Snapshot + Policy + Profile coordinates
versioned parser/function + invocation semantics
Parse terminal / reconciliation identity
```

本文不决定 product identity 是 canonical AST digest、opaque owned value identity、normalized tree identity 还是其他
carrier；它只拒绝 path-only、accepted-bit-only 与 unbound digest。

## 6. semantic product set 不拥有 live consumer authority

两个合法 attempts 可以产生逐字节相同的 product-set semantics。它们仍有不同的 original `BudgetContext`、parent
eligibility、one-shot Parse claims 与 continuation history：

```text
equal admitted product-set bytes
    != equal parent attempt
    != transferable Fact consumer claim
```

因此 future topology 至少分成：

```text
attempt-neutral semantic value
    application-owned reconciled product set

attempt-bound authority
    original context + parent eligibility
    + exact reconciled product-set identity
    + provider-bound child eligibility
    + one-shot request claim
```

semantic value 可以在相同 exact inputs/function 下复算；live claim 必须针对本次 attempt 重新取得。

## 7. 多 Provider 共享 product truth，但不共享 child claim

current multi-Provider controller 让多个 Provider children 共享同一 live context、parent eligibility 与 classification，
同时为每个 child 建立不同 Provider descriptor、projection、request frame 与 one-shot eligibility。这个 authority
shape 可以保留，但 upstream Parse truth 不能按 Provider 数量复制：

```text
one application-owned reconciled Parse product set
    -> Provider A consumer projection / claim
    -> Provider B consumer projection / claim
    -> optional Provider consumer projection / claim
```

每个 Provider 的 consumer projection 必须绑定相同 upstream product-set identity；Provider-specific descriptor 与
child claim 仍然不同。一个 Provider 的 completion、failure 或 output 不能修改 upstream product set，也不能替另一
Provider 领取 claim。

## 8. Echo product identity 不证明 product consumption

audit witness 构造一个只读取 raw source 的 Provider，并让 request/terminal 同时回显不同 product identity。两个
request 会得到不同 operands/run identity，但 Provider 仍能从同一 raw bytes 产生相同 semantic Fact：

```text
request(product=P1, raw=R) -> terminal binds P1 -> Fact F
request(product=P2, raw=R) -> terminal binds P2 -> Fact F

Provider actual read set = {raw source}
```

因此：

```text
product identity appears in request/operands/terminal
    != Provider consumed that product
```

future contract 在声称继承 Parse authority 前，必须冻结一种可机械执行的 product-use boundary。候选解空间至少包括：

```text
product is the only derivation-capable Provider input

or

application independently validates Fact projection against the admitted product
```

第二条会触及 Fact obligation-universe derivation/fulfillment，当前没有授权。本文因此不替后继选择方案，只确认
“product digest + existing raw-source wire”不足以成为 correction contract。

## 9. Least authority 与 raw source

无论 future carrier 如何选择，以下边界已经可以冻结为前合同要求：

- `REJECTED`、missing 与 non-success subjects 的 raw bodies 不得出现在 Fact Provider document、shared map、lookup
  service 或其他 provider-visible side channel；
- accepted product reference 必须解析到同一个 admitted immutable/copy-owned product，不能由 Provider 自行按 raw
  bytes 重建后声称 identity 相同；
- current source-body projection 继续只解释 historical pre-Parse bytes，不能复用其 `/0.1` identity；
- future protocol / operands / ProviderRun identity 必须是 versioned successor，具体编号与字段仍是 non-decision；
- 若 accepted raw bytes 将来确有辅助用途，必须另行定义其最小 authority，且不能成为替代 admitted product 的
  derivation authority。

本文不证明 accepted raw bytes 永远不能出现；它证明未受约束的 raw-source authority 与“必须消费 admitted product”
不能同时靠 terminal echo 自证成立。

## 10. zero accepted 调度仍是 non-decision

current source-body runtime 会对 denominator-empty、all-unsupported 与 later-empty worlds 启动 applicable Provider child，
发送 exact empty-body request，并用不同 projection identity 区分这些 worlds。该历史行为不自动决定 future product
consumer scheduling。

本轮只冻结：

```text
all rejected + complete reconciliation
    -> known-empty admitted product set

missing / non-success
    -> no normal admitted product set
```

future required Fact Provider 是否必须收到 exact empty-product request、由谁创建 empty FactSet、以及哪个 lifecycle
证明 required-provider closure，仍须在 Fact consumer correction contract 中裁决。known-empty product set 本身不等于
Fact 或 Coverage closure。

## 11. Paired-world falsifier

仓库外 audit-only script 位于：

```text
<local-workspace>/tmp/parse-fact-consumer-precontract-audit/consumer_matrix.py
```

script SHA-256：

```text
494b36e8158e0c6270ae23bad938f52aa562d12fae233cea51d3153f706ac113
```

它检查六个必须拒绝的弱绑定：

| ID | weak world | 观察 |
| --- | --- | --- |
| `PFC-PRE-001` | 同 accepted IDs，不同 product IDs | accepted-only projection bytes 碰撞 |
| `PFC-PRE-002` | all-rejected complete 与 missing result | empty accepted projection bytes 碰撞 |
| `PFC-PRE-003` | 不同 attempts，同 product-set semantics | semantic equality 与 live authority 分离 |
| `PFC-PRE-004` | request 回显 product，Provider 只读 raw source | operands 不同但 reported semantic Fact 相同 |
| `PFC-PRE-005` | 多 Provider children | upstream product set 共享，consumer claims 独立，Provider 不拥有 Parse truth |
| `PFC-PRE-006` | accepted field 正确但 rejected raw body 可见 | accepted-set 字段没有建立 least authority |

CPython 3.10.6 / 3.13.13、normal / `-O` 四格各产生 1456-byte canonical report，逐字节一致：

```text
38c4af75a33c7f9718cd980e8e8069a46bd888d311fd35e8500b603f31358f32
```

report 内部 canonical semantic digest 为：

```text
8b265187a4e1553b65daa960850c180fe11d325f38834afc568a664f828a7cc0
```

第一次额外 byte comparison 在四份 report 已成功生成并取得相同 size/hash 后，调用了 PowerShell 不支持的
`AsSpan()`，保留为 `INVALID_AUDIT_COMPARISON_SETUP`。它没有修改或重跑 report。后继只改用显式 byte-array
comparison，确认四份 bytes 相等。

这些 reports 是 precontract falsifier，不是产品 Evidence，也不选择 future product carrier、wire shape 或 Provider
implementation。

## 12. 必须拒绝的推理

| ID | world | 必须拒绝的推理 |
| --- | --- | --- |
| `PFCB-000` | accepted subject IDs 相同 | exact Parse product 相同 |
| `PFCB-001` | accepted set 为空 | Parse denominator complete 且 all rejected |
| `PFCB-002` | product digest 出现在 operands/terminal | Provider 实际消费了 product |
| `PFCB-003` | product-set bytes 相同 | 另一 attempt 可继承 live consumer claim |
| `PFCB-004` | 两个 Fact Providers 需要同一 source | 每个 Provider 可各自创建 Parse truth |
| `PFCB-005` | rejected body 不在 accepted list 里 | rejected body 可通过其他 request field/shared map 暴露 |
| `PFCB-006` | all rejected 已 complete | Fact child 必须启动或 Fact/Coverage 已 closed empty |
| `PFCB-007` | current empty-body tests 全绿 | future product-bound zero scheduling 已冻结 |
| `PFCB-008` | Parse precontract 已审计 | consumer correction contract 可以先于 product identity 冻结 |
| `PFCB-009` | Provider reparse 得到相同 tree/Fact | 新 observation 继承 upstream Parse authority |

## 13. 后继 Parse minimal contract 的最大边界

本文自己的最后门闭合后，CONTROL LOOP 最多可以重新判断一份 docs-only Parse minimal contract 是否仍是最小
合法问题。该合同可以冻结：

```text
Parse denominator = exact Language Support ELIGIBLE subjects
one shared obligation per exact subject / parent attempt
versioned parser/function and invocation semantics
grammar-parse result boundary
semantic result / execution lifecycle / complete reconciliation separation
exactly-one admitted result or explicit missing/invalid reconciliation
application-owned admitted product / product-set semantic identity
same-attempt immutable/copy-owned product access boundary
semantic value != live continuation authority
persistence remains OPEN
```

它不得同时冻结 Fact wire、Provider scheduling、Fact obligation universe、Fact fulfillment 或 Coverage。future Fact
consumer correction contract 只能在上述 product authority 成为 qualified upstream truth 后，继续冻结 provider-bound
projection/request 与 product-use enforcement。

## 14. 明确 non-decisions

本文不决定或授权：

```text
Parse contract bytes or frozen state
real parser implementation / subprocess topology
Parse terminal enum / reason composition
AST normalization / product carrier / digest algorithm / persistence
post-Parse Fact projection document shape or class
wire / operands / ProviderRun version number
product-only vs separately authorized ancillary accepted-source access
zero-accepted child scheduling
Fact obligation-universe derivation or fulfillment
public Artifact / Schema / Evidence / Manifest / publisher / Bundle
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / Coverage
CLI / Workbench / release
```

文档 208、current projection `/0.1`、Fact wire `/0.2` 与既有 Fact/Relation/Slice history 不被静默重写。后继新
identity 必须保留旧 identity 与历史 bytes 为只读事实。

## 15. 本地候选资格

本轮保留三次未形成候选失败的施工设施问题：

1. 第一次 AGENTS 追加补丁引用的尾段换行与实际文件不一致，`apply_patch` 在写入前拒绝，文件没有部分修改；
2. 第一次 changed-scope checker 使用 `git diff --name-only`，遗漏尚未跟踪的 doc216，因而错误报告三文件 scope；
   直接路径核对证明 doc216 已在目标 worktree，后继 checker 改用 `git status --porcelain`；
3. 第一次 related runtime 四格并行 wrapper 只打印前 30 个 dots，没有保存仍在运行的 session IDs 与 final
   summaries；四个进程自然结束后，该次保持 `NON_QUALIFYING_TEST_OBSERVATION`，随后用单一 orchestrator 保存完整
   outputs 与 exit codes。

这些都是 patch/checker/orchestration setup 问题，不是文档语义、runtime 或产品 observation failure。最终四文件
候选通过：

```text
changed scope                         4/4 PASS
relative Markdown links              532 PASS
UTF-8 without BOM / LF / final LF         PASS
balanced fences                           PASS
candidate marker                     4/4 PASS
audit script/report hashes                PASS
git diff --check                          PASS
```

绑定 exact checkout source paths 后，以下 docs/Schema suite 在 CPython 3.10.6 / 3.13.13、normal / `-O` 四格各
`40/40 PASS`：

```text
tests.test_markdown
tests.test_review_r1_admission_evidence_schema
tests.test_review_r1_derivation_evidence_schema_correction
tests.test_review_r1_schema_payload
```

与本文 source claims 直接相关的 gate / Fact wire / controller / multi-Provider suite 在同一四格各 `67/67 PASS`：

```text
tests.test_source_operation_gate
tests.test_source_operation_fact_wire
tests.test_source_operation_controller_integration
tests.test_multi_provider_fact_composition
```

这些结果只使 final docs-only candidate 具备提交资格，不替代 original PR、exact-main、installed-product readback 或
independent reconciliation，也不授予 contract/runtime authority。

## 16. 条件化状态

本文只条件化发布：

```text
R1_PARSE_FULFILLMENT_AUTHORITY_PROBLEM_AUDITED
R1_PARSE_FULFILLMENT_PRECONTRACT_AUDITED
R1_PARSE_TO_FACT_CONSUMER_PROJECTION_PREREQUISITE_AUDITED
R1_PARSE_PRODUCT_FACT_CONSUMER_BINDING_PRECONTRACT_AUDITED
R1_PARSE_FULFILLMENT_CONTRACT_CANDIDATE
R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

`PREREQUISITE_AUDITED` 来自文档 215 已闭合的独立资格链；本文仍只是 audit candidate。不得把两个状态同时出现
解释为 Parse contract、product identity 或 correction contract 已经冻结。

## 17. 本候选自己的最后门

本文是 docs-only precontract audit candidate。条件化状态只有在以下链条全部成立后生效：

```text
final README / AGENTS / milestones / 本文 bytes
    -> local docs / Schema / static gates
    -> original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> product-consumer binding precontract audit candidate becomes qualified history
```

任一 failure、ERROR、setup failure 或 UNKNOWN 保留原 identity；后继 PASS 不改写历史。audit script、current tests、
Provider output 与 CI 都只作 witness，不拥有 contract authority。

## 18. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP。下一步最多重新审计 Parse minimal contract 是否仍是最小合法问题；
不得按文档编号自动起草 consumer correction contract，不得实现 parser/AST/product/new wire/Fact、选择 persistence 或
恢复 ReviewSliceSet/Coverage。

若后继反例证明 product identity、product-use enforcement 或 zero-accepted scheduling 仍缺更早 authority seam，只重开
被击穿的最小边界；不得用本审计的四格一致性或绿色门禁替代该判断。

## 19. candidate qualification closure

上述 candidate gate 已从本文最终字节独立闭合。PR #239 的 exact coordinates 为：

```text
base  = 34b58014b1eadd0b30bc4deb73ab2cc97e2ed675
head  = ca90402e23e7dcf07f7d085882843eba19dd5dde
merge = 63daada4157e0068bb2a1333953f821f56f61894
tree  = 4ff61ed57f6b88c8dfbe4d1adb53c9652eab106a
```

PR original Public CI `36414215832` attempt 1 为 11/11 SUCCESS；new exact main 的 Public CI
`36416676877` attempt 1 为 11/11 SUCCESS，Browser Smoke `36416676883` attempt 1 为 1/1 SUCCESS。

README、本文与 milestones 使用三个 fresh Plan/session 完成 anonymous installed-product readback：

| Path | Plan | Session | Result |
| --- | --- | --- | --- |
| README | `r1-pfc-binding-readme` | `github-paired-b20148f0cbda4f2fb9c67aedac10334f` | `COMPLETE / PASS` |
| doc216 | `r1-pfc-binding-doc216` | `github-paired-da6fe8913e3b4c78b800b8ad4e2b4066` | `COMPLETE / PASS` |
| milestones | `r1-pfc-binding-milestones` | `github-paired-37b13845823947228e8c345f754f453f` | `COMPLETE / PASS` |

三份 observation 均为 exact-SHA HTTP 200、三样本稳定、唯一 marker、零 active stream / cleanup error / conflict。
README、AGENTS、本文与 milestones 四份 public raw bytes 与 exact Git blobs 相等。独立 verifier 重新核对 original PR、
merge/tree、exact-main gates、Plan-before-observation、Core fields 与 source bytes，final manifest 为：

```text
sha256_json  = 9b896e85c11efbd90cb4a19c8a12674652de568e80e7ed9619f80aba95649dc2
sha256_bytes = fd04d68753dff54f1b6f6f64d854cf3eb0267ac5b0bc5697286dd31544e22d5
```

readback preparation 期间，托管 worktree 因聊天根目录不是 Git repository 而拒绝、第一版脚本误判 template literal、
PATH `python` 误建 3.10.6 venv、两个 PowerShell marker counter 错误与一次 Playwright shutdown warning 均保留为
setup/preflight history；它们没有创建或改写正式 Plan/session/Evidence。最终三份 fresh readback 与 reconciliation 使用
明确的 CPython 3.13.13 venv，旧 setup outputs 没有被复用。

因此本文现在是 `PRECONTRACT_AUDITED` qualified history，只授权
[Parse fulfillment 最小合同 0.1](217-r1-parse-fulfillment-contract.md)的 docs-only candidate。它不授权 parser、AST
carrier、Fact correction、persistence、public Artifact 或 Coverage。

## 20. Parse freeze 后的 CONTROL LOOP 重入

[Parse private implementation 最终冻结发布](244-r1-parse-private-implementation-freeze-publication.md)的全部门闭合后，
CONTROL LOOP 从 exact `main@b166dee05fe995b17b2f3bb557d75c2feb4f5493` 重新审查本文当年缺失的三个前提。
current private Parse runtime 现在已经机械提供：

```text
application-owned admitted Parse product / product-set identity
complete denominator reconciliation
same-attempt one-shot immutable/copy-owned product access
```

同一 exact main 上，historical Fact runtime 仍使用 `private-source-operation-projection/0.1` 与
`veritrail-review-derivation-cell/0.2`，request 继续携带全部 Language Support eligible raw bodies；request、builder、
worker 与 multi-Provider state 没有 Parse product set 或 continuation。一个 partial-accepted audit world 中，Parse-rejected
source body 仍到达 Fact Provider，并产生 canonical Fact candidate。

第一次 audit fixture 因未构造出它声称的 rejected world 而停止，保留为
`INVALID_AUDIT_FIXTURE_SETUP / product_observation=false`；fresh attempt 2 的 CPython 3.10.6 / 3.13.13、normal /
`-O` 四格 report 逐字节一致。五个相关 existing test modules 四格各 86 项成立，只证明 frozen Parse truth 与 historical
raw-source Fact chain 同时稳定存在，不证明二者已经接通。

canonical audit summary SHA-256 为：

```text
9cdbec6bddd3dee187ade8e551ebc083a8d2d4568d55468f67dd19c9f5f366e4
```

因此本文原来的 upstream prerequisite 已经成为 frozen truth，而 consumer seam 仍然存在；没有发现更早的 authority
断口。[Parse product → Fact consumer correction 最小合同 0.1](245-r1-parse-to-fact-consumer-correction-contract.md)
现在可以作为 docs-only candidate 起草。该新资格不倒改本文的历史停止线，也不授权 runtime、Fact fulfillment、
persistence、public carrier 或 Coverage。
