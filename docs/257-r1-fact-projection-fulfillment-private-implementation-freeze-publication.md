# R1 Fact projection / fulfillment 私有实现冻结发布

日期：2026-10-13

> 条件化状态目标：`R1_FACT_PROJECTION_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN`。本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@b11eb0bd857f87ed7c4da4b9b74b14fcaac884d4`；tree `6a807fea6ab9eed98320cc92ef73db3dfa4f3271`。
>
> 上游：[冻结合同](252-r1-fact-projection-universe-and-fulfillment-contract.md)、
> [可行性审计](254-r1-fact-projection-fulfillment-private-implementation-feasibility-audit.md)、
> [实现授权发布](255-r1-fact-projection-fulfillment-private-implementation-authorization-publication.md)、
> [实现候选](256-r1-fact-projection-fulfillment-private-implementation-candidate.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只发布 doc252 / doc254 / doc255 限定的 private A–J 已完成施工、进入受保护 main，并取得候选自己的
local/original PR/exact-main/fresh installed-product/independent reconciliation 资格。它不修改 runtime、tests、Schema、
Profile、Policy、既有合同、corpus、public carrier、Evidence、Bundle、publisher、CLI、Workbench、Core、tag 或 Release。

本次冻结的对象仍是 private、attempt-bound、non-published Fact projection / fulfillment closure：application 从完整 admitted
Parse products 与冻结规则独立构造 U/E；closed worker 只取得 copy-owned product-only input，不取得 raw source、repository
loader 或 expected answers；每个 applicable Provider 独立承担完整 U/E，以 one-shot claim 与 bounded child lifecycle 形成
terminal observation；application 再按 assigned product/node/alias、完整 semantic content、reported IDs 与真实 provenance 双向
核账。只有全部 requiredness、lifecycle 与 shared-safety reconciliation 成立，才形成同 original BudgetContext / Parse history 的
private FactSet 与 one-shot continuation。

zero denominator 与 all-rejected 保留不同 upstream identity，均不启动 Fact child，也不形成 empty FactSet 或 Fact-stage closure。
unrepresentable U 保留完整可构造 universe 与 blocker，不通过漏项、改名或改归 Parse REJECTED 获得较小的成功世界。

## 2. Exact implementation qualification

```text
PR                   = #295
base                 = 46eb3ab55bdeea17cd5e6bd2bf614a05b109c0f6
head                 = daf11eb76a33b4522da2b2f0fc14f0ec280e5f1f
ordinary merge       = b11eb0bd857f87ed7c4da4b9b74b14fcaac884d4
candidate/merge tree = 6a807fea6ab9eed98320cc92ef73db3dfa4f3271
diff                 = 1 commit / 11 files / +3183 / -3
```

[PR #295](https://github.com/NoctilumeDev/VeriTrail/pull/295) 的 original Public CI
[38274256272](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38274256272) attempt 1 为 11/11 SUCCESS。
exact-main Public CI [38278181528](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38278181528) attempt 1 为
11/11 SUCCESS；Browser Smoke [38278181407](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38278181407)
attempt 1 为 1/1 SUCCESS。ordinary merge parents 精确为上述 base/head，merge tree 等于受审 candidate tree。

最终 implementation bytes 的 full Review Attention 本地四格各运行 501 项：CPython 3.10.6 normal/`-O` 各
`500 PASS / skipped=1`，CPython 3.13.13 normal/`-O` 各 `501/501 PASS`。hosted original 与 exact-main CI 四格
各运行 501 项、`498 PASS / skipped=3`；三个 local-only exact-reference/Windows witnesses 在 runner 没有显式 reference
runtime，不能写成 501 项全部实际执行。

actual semantic corpus 固定 11 worlds/cell，共 52 actual reference Parse children / 56 actual bounded Fact children；U/E、
mapping history、negative states 与去 provenance FactSet 语义字节四格一致。finite Unicode corpus 检查全部
`0x110000` codepoints 的四类谓词与 11 个 component gold，canonical SHA-256 为
`ce98f52498212b15bb3c2d115d6c32073e3fb84c10b4b1dcf8ee32ba83fb94a0`。这些有限 witnesses 不证明所有字符串、
未来 Unicode 宿主或任意第三方 Provider。

## 3. Candidate fresh installed-product readback

在 detached exact `main@b11eb0bd...` 上建立 fresh CPython 3.13.13 venv，安装冻结 Core 0.13.0、GitHub Evidence
0.1.0、Playwright 1.62.0 与 matching Chromium。公开 wheel 使用重新校验的既有 Release 字节，不声称本轮 fresh download；
匿名产品观察清空 token、`PYTHONPATH`、`PYTHONHOME`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| doc256 | `r1-fact-impl-candidate-formal-doc256-1-b11eb0b` | `github-paired-6b985ea36e1b4ee7b0e7855bfab475aa` | `8bfdce22d1916430e0b52c6ed4c0ef5f75f3e47bdfcd94c419ac40661617b1e7` |
| milestones | `r1-fact-impl-candidate-formal-milestones-1-b11eb0b` | `github-paired-43e2f41abe6247bd9987f00fab455fa7` | `d4c26e8a812e37bb7488553e84a690c38e89b012a1d57833093b9fdeee06dd6b` |
| README | `r1-fact-impl-candidate-formal-readme-1-b11eb0b` | `github-paired-8a09275ccf294d56803a75b5d128dacd` | `d5f00c064f459e5455d6d173e0a9245925ae936ede8f87d4bfae6129611b6cbd` |

三者均为 exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定 marker、零 conflict/coverage reason/cleanup error/active
stream。独立 evaluator 从原 sealed Plan、handoff 与 Evidence 重算 Core，并逐项等于 producer report；三份 public raw bytes
逐字节等于同一 exact main 的 Git blobs。raw-byte check 不替代正式产品路径。

candidate independent reconciliation SHA-256：

```text
47a3069eb291c3cf69f59ce54454310c78d21df0ee20d807b0f0e8408cb4edcd
```

finite closeout SHA-256：

```text
ffb3ad21d42d7b45c84533d40efbe7a26a611243c996a00ab2cd5f5db4c9c137
```

## 4. Proof strength 与保留历史

本结果只证明 fixed audited closed conformance worker 与 private application-owned reconciliation。普通 Python 进程仍有宿主
能力；stateless validator 不拥有 live continuation authority，也不能证明任意第三方 Provider 没有读取其他宿主输入。
private observations 保留 terminal/frame 原字节，closure document 以摘要绑定这些 bytes；这不产生 public carrier 或
persistence authority。

以下身份继续保留，later PASS 不把它们改写成未发生：

- initializer 在 qualification 建立前创建 claims 的 `NEW_PRIVATE_IMPLEMENTATION_DEFECT`；
- raw-init fixture 未显式 empty prefix 的 `TEST_GOLD_MAPPING_SETUP_ERROR`；
- 首个 full 3.10 normal 在 600 秒 outer containment 终止，未取得 terminal suite count；
- source review 发现 observation 保存晚于 join 的 retention gap；
- operator patch path、ignored pyc 分类、GraphQL HTTP 504、UI attachment 上限与 CI watcher API EOF；
- candidate readback 首个 Plan ID 超过 64 字符的 `READBACK_PLAN_IDENTITY_SETUP_ERROR`；
- README 三份 exact-path 503 diagnostic，底层原因保持 UNKNOWN；后继 COMPLETE diagnostic/formal PASS 不解释或覆盖它们；
- doc255 及更早的 ERROR/FAIL/CANCELLED/UNKNOWN 历史。

setup1 在正式观察前失败，保留 47 份 nonqualifying artifacts；fresh setup2 只缩短 identity prefix，P1/P2、targets、
budgets、sampling 与 cleanup oracle 不变。setup2 有 8 份 render diagnostics、4 份 setup diagnostics，均为
nonqualifying；正式 history 为 3 PASS / 0 non-success。

## 5. 本发布自己的最后门

本 docs-only patch 只允许修改 `README.md`、`AGENTS.md`、`docs/milestones.md` 并新增本文。doc252–256、六个新 private
modules、`test_fact_fulfillment.py`、旧 `/0.1`、其他 runtime/tests/workflows/Schema/Profile/Policy 与全部历史合同保持原字节。

本层 final-byte local gates 只重核 publication 自己的 docs/Schema 边界：CPython 3.10.6/3.13.13 normal/`-O` 的
docs/Schema regressions、exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences/unique headings、
条件 marker、敏感字面量、冻结字节连续、`git diff --check` 与 read-only hygiene。implementation full runtime matrix 属于
已经资格化的 candidate tree；publication 不重新解释它。Public CI 仍执行自己的完整原始门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> target PRIVATE_IMPLEMENTATION_FROZEN becomes effective
    -> return CONTROL LOOP
```

本门闭合前，branch 中的 `FROZEN` 只是条件 target。候选 readback 不能替代本 publication 的 fresh Plan/session/Evidence；
diagnostic 不计入资格，所有 formal non-success 必须保留原身份，N 从 history 机械导出。本地 checkout 对齐与 cleanup 是
housekeeping，不追加语义门。

## 6. 后继停止线

本发布不授权 persistence Route A/B、zero-member Fact-stage closure、Fact→Coverage handoff、Relation/Slice public assembler、
ReviewSliceSet/seven-stage Coverage、public Schema/carrier、Evidence/Bundle/publisher、CLI/Workbench/Core、CLAIM_FIDELITY、
tag 或 Release。

最后门闭合后必须返回 CONTROL LOOP，从新的 exact main 重新审计 authoritative Fact history 是否已经足以支持同 attempt
Coverage handoff，还是仍有更早 seam。实现冻结、文档编号与绿色 CI 都不能自动启动后继合同或 runtime。
