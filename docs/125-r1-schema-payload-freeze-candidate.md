# Review Attention R1 Schema payload 冻结候选

## 1. 文档身份

> 候选状态：`R1_SCHEMA_PAYLOAD_CANDIDATE / R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED /
> R1_IMPLEMENTATION_NOT_STARTED`
>
> 精确施工基线：`main@4ef8b6434597b6557d6306100b91aebd9c1b3ecd`
>
> 上位合同：[R1 确定性语义切片合同 0.1](113-r1-deterministic-semantic-slice-contract.md)
>
> Schema 合同：[R1 Schema 与规范身份合同 0.1](120-r1-schema-and-canonical-identity-contract.md)
>
> 前置修正与重新冻结：[文档 123](123-r1-schema-payload-preflight-correction.md) / [文档 124](124-r1-schema-payload-preflight-refreeze-publication.md)
>
> 影响层级：`L2_CONTRACT_PAYLOAD + TEST_ONLY_CI_DEPENDENCY`

本文记录 R1 Schema payload 的实现候选。候选只把已经冻结的字段、闭集、规范身份和兼容义务物化为
公共 JSON Schema、纯数据向量与 conformance tests；它不创建 SourceSnapshot importer、Git reader、
Python parser、Fact/Relation producer、Slice engine、Coverage producer、CLI、Provider discovery、AI
proposal、HumanDisposition、Core Verdict、标签或 Release。

分支、本地测试或本文中的状态文字都不能建立冻结事实。只有候选自己的原始远端门禁、受保护主线合入、
新 exact-main 门禁与匿名公开读回全部成立后，才允许另开 docs-only 状态发布。

## 2. 公共 payload

### 2.1 Schema 文件集

候选严格创建上位合同指定的十个 Draft 2020-12 文件：

```text
schemas/review-r1-common-0.1.schema.json
schemas/review-source-snapshot-0.1.schema.json
schemas/review-policy-0.1.schema.json
schemas/review-derivation-profile-0.1.schema.json
schemas/review-derivation-evidence-0.1.schema.json
schemas/review-fact-set-0.1.schema.json
schemas/review-relation-set-0.1.schema.json
schemas/review-slice-set-0.1.schema.json
schemas/review-coverage-ledger-0.1.schema.json
schemas/review-derivation-manifest-0.1.schema.json
```

九个 root Schema 只通过相对引用消费 common definitions；测试拒绝网络引用或对其他 root Schema 的隐式
依赖。闭合对象默认使用 `additionalProperties: false`。三处表面占位只用于同一 Schema 内的判别分支：

```text
Manifest.files
    -> outcome_kind 决定 COMPLETE / DIAGNOSTIC 精确 tuple

Fact.semantic_attributes
    -> fact_kind 决定 exact attribute object

Relation.target
    -> relation_kind 决定 FACT / IMPORT_LITERAL target
```

静态测试固定这三个占位坐标；新增第四个开放 object/array 会直接失败。

### 2.2 数据型兼容 corpus

`tests/fixtures/review-r1-schema-0.1/` 包含：

```text
compatibility-cases.json
    20 个冻结兼容义务

identity-vectors/
    24 个冻结 identity domain 的 34 个 semantic vector
    1 个 raw policy-seal SHA-256 vector
    每项均含完整 envelope、expected canonical UTF-8 hex 与 expected digest

valid-complete/
    1 份由 9 个规范文件组成、内部一致的 synthetic COMPLETE bundle
```

每个 valid Artifact 都是 compact canonical JSON 加一个 LF；无 BOM、无 CR、无双换行。fixture
`manifest.json` 绑定另外八个文件的固定 role/path、字节长度、文件 SHA-256 与语义摘要。它只是兼容夹具，
不是 R1 真实仓库分析结果，也不构成 Review Attention runtime。

## 3. Schema 与 conformance 没有混权

JSON Schema 只证明局部结构：必填字段、类型、枚举、判别分支、额外字段拒绝与局部范围。候选测试另行
复算以下跨对象或算法性质：

```text
canonical bytes and domain-separated digests
raw Git path reversibility and ordering
Python 3.10 NFKC identifier legality
SourceAnchor within exact blob bounds
Policy/Profile rank ordering and uniqueness
Fact/Relation subject and content identities
IMPORT_TARGET_LITERAL alignment with its source import Fact
Provider cumulative composition and conflict preservation
Slice identity, frontier and mechanically derived coverage status
Coverage denominator equations, disjoint terminal partitions and conservative join
Provider/Evidence timestamp ordering
Manifest byte identity, semantic bindings and execution/outcome compatibility
```

负向向量刻意保留若干“Schema 可接受、conformance 必须拒绝”的文档，例如 keyword/NFKC 未规范化
identifier、越界 anchor、与 source Fact 不一致的 import literal、重复终态 Coverage item、陈旧 Slice
status、超出 derivation window 的 Provider 时间以及 `INTERRUPTED + COMPLETE manifest`。因此：

```text
Schema-valid != R1-conformant
R1-conformant != repository understood
```

## 4. 依赖与跨轨道边界

`jsonschema==4.25.1` 只位于 Core 的 `schema-test` optional extra，并只由 Public CI 的测试安装步骤消费。
Core base wheel 不安装或导入它；一次新 venv 的 `--no-deps` base-wheel probe 已证明 Core `0.13.0` 可独立
导入，且环境中不存在 `jsonschema`。

候选没有新增 `src/` 模块，也没有修改 GitHub Evidence、Starter、Authoring Skill、Workbench 或 Core
裁决语义。P/R/Q 之间仍只通过版本化 Artifact 与冻结合同组合：

```text
P does not produce R1 source facts
R does not import P implementation
Q does not acquire gate-skip authority
Core does not learn R1 parser or slice semantics
```

## 5. 本地候选证据

所有 Python 测试均显式把 Core `src`、GitHub plugin `src` 与 test root 绑定到当前 worktree；没有把其他
editable checkout 的模块当成本候选证据。

| 门 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| Schema/conformance focused normal | 22/22 | 22/22 |
| Schema/conformance focused `-O` | 22/22 | 22/22 |
| Core 全仓 normal（最终候选矩阵） | 441/441 | 441/441 |
| Core 全仓 `-O`（最终候选矩阵） | 441/441 | 441/441 |
| GitHub Evidence normal | 180/180 | 180/180 |
| GitHub Evidence `-O` | 180/180 | 180/180 |
| Authoring Skill normal | 24/24 | 24/24 |
| Authoring Skill `-O` | 24/24 | 24/24 |

上述 440 项 Core 结果产生于最终静态守卫加入以前，不能替代最后的 441 项候选矩阵。最终 Python 3.10
normal 首轮在 441 项中有三条既有 M10 真实 Chromium 用例失败；三条均未取得 Browser Evidence，并一致
记录：

```text
stop_reason = RESOURCE_MEMORY_SOFT_LIMIT
```

失败后宿主机可用物理内存约为 4974 MiB，而 sealed M10 profile 要求运行期可用内存不得低于 4096 MiB。
没有遗留本候选拥有的 Python、Node 或 Chromium 进程，用户 Chrome 与其他宿主应用也没有被测试或本轮
施工越权终止。该红灯因此保留为有效的宿主资源边界事实；剩余三组最终 Core runner mode 已暂停，不能用
局部重跑覆盖它。

随后只为分类而执行的一次 exact-worktree 单变量诊断使用相同的真实 Chromium 正向路径，结果为：

```text
stop_reason                       NONE
browser_present                   true
cleanup_complete                  true
host_available_memory_min_mb      4925.266
browser_peak_rss_mb               214.762
```

这说明当前没有证据把失败归因为 R1 Schema payload 或 Core/Browser 确定性回归；它也不能把第一次红灯改称
偶发。关闭用户 Browser 与腾讯视频、让宿主机恢复到约 9668.5 MiB 可用物理内存后，候选从第一项重新串行
执行完整 441 项四矩阵；Python 3.10 normal/`-O` 与 Python 3.13 normal/`-O` 分别在约
134.2/131.6/131.4/131.2 秒内完成，全部 `441/441`。该新矩阵恢复了本地候选资格，但没有覆盖或删除第一次
资源停止事实。施工没有降低 4096 MiB 生产阈值、伪造 host memory observation，或修改 M10 浏览器语义
测试来制造绿灯。

Workbench 另行完成 173 项测试、ESLint、TypeScript type-check、production build 与
`npm audit --audit-level=moderate`，结果均通过。`git diff --check` 通过。第一次 Workbench test 在当前
worktree 尚未执行 `npm ci` 时因 `vitest` 不存在而未进入测试；依赖按 lockfile 建立后才产生上述有效证据，
没有把环境缺失记录成产品失败或成功。

构建审计生成 Core `0.13.0` base wheel，并在新 venv 中确认：

```text
Core base import                 PASS
jsonschema installed            NO
schema-test extra metadata      PRESENT
runtime dependency expansion    NO
```

## 6. 候选最后门

本候选只有满足以下事实，才有资格进入独立冻结状态发布：

1. 最终变更严格限于十个 Schema、纯数据 corpus/vector、Schema/conformance tests、测试 extra、CI 测试
   安装与候选状态文档；
2. 最终候选在 Python 3.10/3.13、normal/`-O` 下重新完成 focused 与全仓矩阵；
3. 候选 Pull Request 的原始 Public CI 11/11 成功，不用 rerun 覆盖失败；
4. 候选只经受保护主线合入，未处理或混入并行 Dependabot PR；
5. 新 exact main 的 Public CI 11/11 与 Browser Smoke 1/1 成功；
6. 从 exact main 匿名逐字节读取十个 Schema 与 corpus 全部 19 个文件，并与合入工作树一致；
7. 使用已发布产品链匿名读取 README 与本文，取得 `PUBLISHED / COMPLETE / PASS`；
8. 仓库仍不存在 R1 runtime importer、parser、Fact/Relation/Slice/Coverage producer、CLI、Provider、标签或
   Release。

任一新反例都可以否决候选。现有本地绿灯不能被外推为 payload 已冻结，也不能授予 R1 运行实现入口。

## 7. 候选状态

```text
R1_SCHEMA_CONTRACT_FROZEN
R1_SCHEMA_PAYLOAD_CANDIDATE
R1_SCHEMA_PAYLOAD_FREEZE_NOT_STARTED
R1_IMPLEMENTATION_NOT_STARTED
```

后继若完成上述最后门，只允许从新的 exact main 建立独立 docs-only 冻结发布。冻结发布不得与 runtime
实现共用分支；是否解除实现施工资格必须由该发布显式裁决，不能由本候选自动继承。
