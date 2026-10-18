# R1 CoverageLedger 0.3 child Schema / conformance 私有实现冻结发布

日期：2026-10-18

> 条件化状态目标：`R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_FROZEN`。本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@2dc923ba5b070aaa63d6b783c7d21c1135a9f6ca`；tree
> `2f2ebe2a31f6a198653b4b1260c96ad053f28388`。
>
> 上游：[root-binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)、
> [合同冻结发布](282-r1-review-slice-set-coverage-root-binding-correction-contract-freeze-publication.md)、
> [可行性审计](283-r1-review-coverage-ledger-0-3-schema-conformance-feasibility-audit.md)、
> [实现授权发布](284-r1-review-coverage-ledger-0-3-schema-conformance-implementation-authorization-publication.md)、
> [实现候选](285-r1-review-coverage-ledger-0-3-schema-conformance-implementation-candidate.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只发布 doc281–285 限定的 bounded private A–J 已完成施工、进入受保护 main，并取得候选自己的
local/original PR/exact-main/fresh installed-product/independent reconciliation 资格。它不修改 runtime、tests、workflows、
Schema、manifest、Profile、Policy、fixtures、vectors、corpus、public carrier、Evidence、Bundle、publisher、CLI、Workbench、
Core、tag 或 Release。

冻结对象仍是 private、validation-only、non-published CoverageLedger 0.3 child Schema / conformance。调用方必须显式提供 exact
candidate、application-owned Fact handoff source digest、stage projections 与 root terminal-history projections；validator只验证
candidate是否与这些冻结输入机械一致。它不枚举denominator、决定stage status、生成candidate、取得composition claim、消费
live continuation，或授予publication authority。

实现只接受 exact `COVERAGE_LEDGER / 0.3`，unknown、future与未物化的0.2均fail closed。八个规范world、closed
terminal-history vectors、ordered root chain、versioned conformance、direct falsifiers与0.1/common/manifest/history全字节守卫
属于本次冻结对象；semantic equality不继承attempt、claim、one-shot ownership、closure、admission或continuation authority。

## 2. Exact implementation qualification

```text
PR                   = #327
base                 = b4e741bc3b4029257f95cb1bfabbbd0e71c40bd3
head                 = 578714adc3ca84552a1aa7e3aa08c79096d3cf5f
ordinary merge       = 2dc923ba5b070aaa63d6b783c7d21c1135a9f6ca
candidate/merge tree = 2f2ebe2a31f6a198653b4b1260c96ad053f28388
diff                 = 1 commit / 10 files / +2373 / -6
```

[PR #327](https://github.com/NoctilumeDev/VeriTrail/pull/327) 的 original Public CI
[39103034772](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39103034772) attempt 1 为 11/11 SUCCESS。
exact-main Public CI [39104596339](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39104596339) attempt 1 为
11/11 SUCCESS；Browser Smoke [39104596336](https://github.com/NoctilumeDev/VeriTrail/actions/runs/39104596336)
attempt 1 为 1/1 SUCCESS。ordinary merge parents精确为上述base/head，merge tree等于受审candidate tree。

最终实现测试面由24项direct A–J tests与44项既有Schema regressions组成；CPython 3.10.6/3.13.13、normal/`-O`
四格各68/68 PASS。四份canonical reports逐字节一致：

```text
3690636fede8c31bb99cc2fac50cecaa3b5443c14b97a94b05f99a3f7c9d43d8
```

corpus与0.3 Schema摘要分别为：

```text
b4eb5f81c248cc898d28bf520ba689a19278640d40ad6bc11bfe58e757c1cd5c
d1fce2ba6fe6017bb73070896ad7c7801284157d1dc467c4c3bc2c507470dc83
```

本地host当时低于完整Public CI Core regression的4096 MiB soft gate，因此没有把已知资源余量不足环境中的宽回归冒充本地
资格；candidate original与exact-main Public CI各自承担其声明的完整远端门。

## 3. Candidate fresh installed-product readback

在detached exact `main@2dc923ba...`上建立fresh CPython 3.13.13 venv，安装冻结Core 0.13.0、GitHub Evidence
0.1.0、Playwright 1.62.0与matching cached Chromium。公开wheel只复用重新校验的既有Release字节，不声称本轮fresh
download；匿名产品观察清空token、`PYTHONPATH`、`PYTHONHOME`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| doc285 | `r1-cl03-impl-formal-doc285-1-2dc923b` | `github-paired-32d3637a2ffb434a99aad77f409b6d5b` | `ffa4301e412b3b7606d839c298354793ad00f712d76337f7d367ce594815172b` |
| milestones | `r1-cl03-impl-formal-milestones-2-2dc923b` | `github-paired-de10623d1f86486497d8638f54cdb27e` | `9515602bc8c0fb4b04c0d40eeea915c485fec342abef26bf13579e4fbc2cb052` |
| README | `r1-cl03-impl-formal-readme-1-2dc923b` | `github-paired-c72e6e1be3ea45aca8760e997df995ad` | `735eeda19e5c12d15c1d9691c87d0694855692cddc6f25eb0d030db6722f9858` |

三者均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零conflict/coverage reason/cleanup error/active
stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core，逐项等于producer report；三份public raw bytes逐字节
等于同一exact main的Git blobs。raw-byte check不替代正式产品路径。

candidate independent reconciliation PASS，SHA-256为：

```text
6fe3331f5eb24a5aaf057563c2c398d9c37945bb060388515ee87e04a83aa745
```

148-artifact finite closeout SHA-256：

```text
7f0635123b85d83d218c1b17358803e5d1170874f167fb5bf73108bee6767e9a
```

正式history为3 PASS / 1 ERROR。首个milestones formal observation的public render为COMPLETE、HTTP 200、marker 1，
但匿名GitHub API repository probe返回403、remaining 0，归为`ANONYMOUS_API_RATE_EXHAUSTION`；后继fresh身份PASS不覆盖
原ERROR。

## 4. Proof strength 与保留历史

本结果只证明fixed audited closed 0.3 Schema / conformance boundary。普通Python进程仍有宿主能力；validation-only
conformance不拥有application-owned history构造、composition、transport、persistence、publication或live continuation authority。

以下身份继续保留，later PASS不把它们改写成未发生：

- narrow attempt 1的fixture/local shape findings与attempt 2的negative-vector harness order error；
- Schema regression的successor integration findings与local import-path setup error；
- 四格runner import-path setup errors与final wrapper scalar-index summary setup error；
- final-scope untracked-directory enumeration setup error；
- candidate readback首个Plan ID超过64字符的`PLAN_ID_LENGTH_SETUP_ERROR`；
- milestones formal observation #1的匿名API额度耗尽ERROR；
- 记录该ERROR时首个Python `-c`调用被PowerShell引用破坏的`COMMAND_QUOTING_OPERATOR_ERROR`；
- anonymous rate/preflight diagnostics，其中一次rate endpoint与exact-commit preflight额度观察不一致；其路由/缓存归因不进入产品结论；
- 本publication首个final-local wrapper对`git status --porcelain`全输出调用`strip()`，误删第一条路径的首字符，归为
  `PROOF_FACILITY_STATUS_WHITESPACE_STRIP_SETUP_ERROR`；fresh wrapper只修正状态读取，attempt 2通过后本文补记该历史，
  因final文档字节变化仍不冒充最终资格；
- doc284及更早的FAIL、ERROR、CANCELLED、setup failure、fixture failure与UNKNOWN历史。

setup correction只缩短facility-only observation prefix，并在adapter freeze以前完成；产品字节、target marker、P1/P2 assertions、
budgets、sampling与cleanup oracle均未改变。candidate readback adapter freeze SHA-256为：

```text
6521cb7c897e63266842ae9d09fc401f095107bcdafcce32a2efe55a312eb572
```

doc281–285全文件SHA-256保持：

```text
doc281 = 241dc7b5922c981aabb61a1a6a765ed224bdf7ac47a588274a20a9bb3e311eaf
doc282 = 528a2f95c09b65b962465e61f565d1735335d9361e5308ace2f6293fdd5f1db4
doc283 = 6cbcdfd3942d80a5eba8df2024ad1a8034a30e153eb9d53f7c071e7133d88fb7
doc284 = 23a56a76b22b8ca5d56f709726883f8eb84731782e62f238af8805ed566debe3
doc285 = a8770fba000d10ef9f8d0ff6172cabbce9c45b6afc79c01fa1a1e68624158916
```

## 5. 本发布自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc281–285、runtime、tests、
workflows、Schema、manifest、Profile、Policy、fixtures、vectors、corpus与全部历史合同保持原字节。

本层final-byte local gates只重核publication自己的docs/Schema边界：CPython 3.10.6/3.13.13 normal/`-O`的
docs/Schema regressions、exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences/unique
headings、条件marker、敏感字面量、上述冻结字节连续性、`git diff --check`与read-only hygiene。implementation full runtime
matrix属于已经资格化的candidate tree；publication不重新解释它。Public CI仍执行自己的完整原始门。

当前publication final bytes的docs/Schema声明矩阵在CPython 3.10.6/3.13.13、normal/`-O`四格各69/69 PASS；
exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced fences/unique headings、条件marker、
敏感字面量、doc281–285冻结字节连续性、`git diff --check`与read-only hygiene均为PASS。该窄矩阵只证明本发布自己的
documentation/status边界，不替代candidate implementation的原资格链。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> separately approved exact head / protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core, source-byte, Bundle, identity and retained-history reconciliation
    -> target IMPLEMENTATION_FROZEN becomes effective
    -> return CONTROL LOOP
```

本门闭合前，branch中的`FROZEN`只是条件target。candidate readback不能替代本publication的fresh Plan/session/Evidence；
diagnostic不计入资格，所有formal non-success必须保留原身份，N从history机械导出。本地checkout对齐与cleanup是
housekeeping，不追加语义门。

## 6. 后继停止线

本发布不授权composition feasibility/runtime、seven-stage denominator/status/overall join、manifest successor、negative-world
transport、persistence Route A/B、public ReviewSliceSet/Coverage product、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
`CLAIM_FIDELITY`、tag或Release。

最后门闭合后必须返回[CONTROL LOOP](working-method.md)，重新绑定current main、冻结上游、并行PR与反例。Schema /
conformance private implementation frozen不自动授权composition或manifest successor；只有现实证明下一最小问题仍成立，才可另行
审计。R1完成以前，外部related work只进入研究账本，不改变当前合同、实现或调度。
