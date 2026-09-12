# R1 DerivationEvidence Schema 0.1.1 实现冻结候选

> 候选记录状态：`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_IMPLEMENTED /
> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FREEZE_CANDIDATE /
> R1_DERIVATION_PROVENANCE_IMPLEMENTATION_NOT_STARTED /
> R1_RELATION_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 冻结合同基线：`19cb4ff4300e6c7aeb08aa315802abb29e183d60`
>
> 实现提交：`4a2be77be6cbde6684aa7580b936eaba3c2147a5`
>
> 受保护主线实现基线：`99826ec1564e8447524c477ff9f271fa5d062ea6`
>
> 主线 Tree：`a060ed65177b516f4fe054d212f255cc1baf2f49`
>
> 影响层级：`L2_PUBLIC_CONTRACT + L3_SYSTEM`；只物化文档 140/141 冻结的 additive Schema、
> compatibility corpus 与可执行守卫，不实现任何 R1 推导运行时

## 1. 当前裁决

`DerivationEvidence 0.1.1` 修正 payload 已经实现并合入受保护主线。新 root 以自己的 path、`$id`、title
和 `schema_version = 0.1.1` 自描述，只增加两个 typed budget diagnostic，并把 non-completed run 与
non-completed overall Evidence 的 reported identity 闭空规则写入 Schema。旧 `0.1` root、完整 fixture、
identity vectors 和 Manifest 继续保持原字节与原语义。

本实现没有加入 memory/artifact budget primitive、Provider、parser、CodeFact、Relation、Slice、Coverage、
完整 Derivation publication、CLI 或 Workbench 能力。correction corpus 内的 DIAGNOSTIC manifest 只是
测试 specimen，用来证明冻结的四文件布局能绑定 corrected Evidence 的精确字节；它不授权运行时发布。

本文仍只是 docs-only freeze candidate。只有本文自己的原始远端门禁、受保护主线合入、候选 exact-main
门禁与匿名公共读回成立，再由后继独立状态发布记录最终事实，才允许写
`R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN`。

## 2. 实现边界

新公共 Schema 唯一坐标是：

```text
schemas/review-derivation-evidence-0.1.1.schema.json

$id:
https://github.com/NoctilumeDev/VeriTrail/schemas/review-derivation-evidence-0.1.1.schema.json
```

实现保持以下分离：

- document Schema identity 升为 `0.1.1`，semantic digest domain 仍为冻结的
  `veritrail.review.derivation-evidence/0.1`；`schema_version` 已在 payload 内，因此新旧 document 不会共享
  semantic digest；
- common Schema 没有被放宽，其他 R1 Artifact 不会意外接受补丁版本；
- `RequestProvenance` 与旧 root 同构，没有把通用 Artifact family 偷改成 exact-ref-only shape；
- `EXECUTION_MEMORY_BUDGET` 必须绑定 `PROVIDER_RUN` subject，并只能与 run/overall `INTERRUPTED` 组合；
- `EXECUTION_ARTIFACT_BUDGET` 只允许出现在 Evidence 顶层、`subject_ref = null`，不冒充某个 ProviderRun
  的局部失败；
- 任一 non-completed run 的 reported Fact/Relation IDs 必须为空；overall 非 `COMPLETED` 时，已完成 run
  的 reported IDs 同样必须为空；
- 跨对象“memory diagnostic 必须指向并复现在同一 run”由明确 conformance 守卫验证，不伪装成单文档
  JSON Schema 能表达的引用完整性；
- Manifest 自身继续是 `0.1`，没有新增 outcome、文件角色或 partial closure。

## 3. Correction corpus

独立 corpus 固定 `R1-DE-CV-001..010`：

| 坐标 | 单变量义务 | 预期 |
| --- | --- | --- |
| 001 | completed run 报告规范 Fact/Relation IDs | accept + digest recompute |
| 002 | memory containment stop，run/top typed tuple 同一身份 | accept + digest recompute |
| 003 | artifact staging stop，completed run 不被改写 | accept + digest recompute |
| 004–005 | non-completed run 报告 Fact / Relation ID | Schema reject |
| 006 | non-completed overall 中 completed run 报告 ID | Schema reject |
| 007 | memory code 配 completed run | Schema reject |
| 008 | memory subject 指向其他 run / 错误 subject kind | conformance / Schema reject |
| 009 | artifact code 放入 run diagnostics | Schema reject |
| 010 | artifact code 配非 interrupted overall / 非 null subject | Schema reject |

三个正例均保存完整 document、identity envelope 的 canonical UTF-8 bytes 与 expected digest。负例只从命名
正例改变一个 JSON pointer 所代表的语义变量；测试会把该 pointer 恢复并验证文档逐项回到原正例，避免用
坏 JSON、缺字段或错误摘要替代真正的语义反例。

## 4. 历史兼容与字节守卫

测试逐项固定文档 126 已发布的十个 `0.1` Schema 和十九个旧 corpus 文件，共二十九项。每一项 SHA-256
必须与冻结坐标相等；旧 corpus 目录的文件集合也必须精确相等。新 Schema 不是原位修改，旧 COMPLETE
Evidence、Manifest entry、`R1-CV-001..020` 与三十四个 identity vector 均未重写。

新测试还验证：

- 新旧 root 的 required set 与顶层 property set 相同；
- 除 `Diagnostic`、`ProviderRun` 和新增的 `ProviderRunDiagnostic` 外，旧 `$defs` 逐项同构；
- diagnostic 闭集只增加两个预算 code；
- frozen DIAGNOSTIC manifest 的第四项同时绑定 corrected Evidence 的 file SHA-256、size 与 semantic digest。

## 5. 本地候选证据

所有 Python 结果均显式把 Core、GitHub Evidence、Review Attention、Starter 与 test root 绑定到同一个
implementation worktree。最终串行矩阵为：

| 门 | CPython 3.10 | CPython 3.13 |
| --- | ---: | ---: |
| correction + historical Schema focused normal / `-O` | `27/27` / `27/27` | `27/27` / `27/27` |
| Core 全仓 normal / `-O` | `446/446` / `446/446` | `446/446` / `446/446` |
| GitHub Evidence normal / `-O` | `180/180` / `180/180` | `180/180` / `180/180` |
| Review Attention normal / `-O` | `61/61` / `61/61` | `61/61` / `61/61` |
| Authoring Skill normal / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |

Workbench 为 `173/173`，lint、type-check/build 与 `npm audit --audit-level=moderate` 全部通过，审计结果为
零 vulnerability。Core wheel 与 sdist 可构建；wheel METADATA 中 `jsonschema==4.25.1` 仍只属于
`schema-test` optional extra，不是 base runtime dependency。staged diff 仅含合同允许的五个路径。

第一次本地 Core 全仓运行没有绑定当前 worktree 的 GitHub plugin source，测试文件来自本 worktree，
`veritrail_github.handoff` 却不可导入；该次在 436 项后留下一个 loader error，不能作为产品回归证据。
最终矩阵在打印并核对三个实际 module path 均位于当前 worktree 后重新执行，没有用后续成功覆盖该失败事实。

## 6. 受保护主线事实

1. PR #121 的 base 为 `19cb4ff4300e6c7aeb08aa315802abb29e183d60`，head 为
   `4a2be77be6cbde6684aa7580b936eaba3c2147a5`，只含五个允许文件；
2. 原始 [Public CI run 34707150563](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707150563)
   为 attempt 1、11/11 success，没有 rerun；
3. PR #121 以 merge commit `99826ec1564e8447524c477ff9f271fa5d062ea6` 合入受保护 `main`；
4. merge parents 为冻结合同基线与 implementation commit，merge tree 与 implementation tree 同为
   `a060ed65177b516f4fe054d212f255cc1baf2f49`；
5. exact-main [Public CI run 34707869618](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707869618)
   为 attempt 1、11/11 success；
6. exact-main [Browser Smoke run 34707869586](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34707869586)
   为 attempt 1、1/1 success。

上述事实证明 implementation 与当前仓库门禁可以共同成立；它们不证明本文 docs-only 候选已经通过自己的
门，也不把 Windows 结果外推为 Linux/macOS 支持。

## 7. 匿名 exact-SHA 字节读回

在没有 GitHub token 的 fresh 请求中，从 `raw.githubusercontent.com` 的 exact merge commit 坐标读取新
Schema 与 correction corpus。三项 HTTP 200，最终 URL 保持 exact path，远端 bytes 与 merge tree 相等：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `schemas/review-derivation-evidence-0.1.1.schema.json` | 9671 | `a7c38af644626f8d9f529acda3ed5511b8083b672bd1d603e8d60966b5c11045` |
| `tests/fixtures/review-r1-derivation-evidence-0.1.1/README.md` | 888 | `16168eeab31757daa5a8b8b66165a2a00916b78517b6fa630938b9e33f5878ef` |
| `tests/fixtures/review-r1-derivation-evidence-0.1.1/compatibility-cases.json` | 20266 | `b202f0063b1d94a6edc7bf5c9e8aa30e24a76ff6584638bf416c7739ce1283df` |

该读回证明公开 exact bytes 可取得，不证明 GitHub 永久可用，也不把 raw transport success 提升为
Schema correctness；后者仍由 frozen contract、corpus 与验证门共同承担。

## 8. 停止线与下一门

本候选继续禁止：

- memory/artifact budget primitive、真实 Provider execution 或 parser；
- CodeFact、FactSet、DerivationEvidence runtime publication；
- Relation、conflict/UNKNOWN 传播、Slice、Coverage 或完整 Derivation Manifest；
- CLI、Workbench、Core handoff、Q scheduling/cache、D product shell、JPyxis 或 AI Execution OS 工作；
- version、tag、Release、Linux/macOS 与分布式能力声明。

本 docs-only 候选在 CPython 3.10 / 3.13 的 normal 与 `-O` 四种模式下，均通过由合同索引、correction
corpus 及历史 Schema payload 组成的 `35/35` 定向检查。该结果只证明本文和入口索引没有破坏这些本地
可执行约束；完整仓库与跨平台事实仍必须由候选自己的远端 required checks 建立。

本文必须继续满足：

```text
docs-only candidate 原始 required checks 全部成功
    -> exact candidate 合入受保护 main
    -> 新 exact main 的 Public CI / Browser Smoke 成立
    -> fresh anonymous 产品 Collector 读回 README、本文与 milestones
    -> 后继独立最终状态发布
    -> R1_DERIVATION_EVIDENCE_SCHEMA_CORRECTION_FROZEN
```

任何新反例仍可否决冻结。最终状态发布以前，下一步只能完成本候选的证据闭环；不得提前开始 budget
primitive feasibility 或 provenance runtime。
