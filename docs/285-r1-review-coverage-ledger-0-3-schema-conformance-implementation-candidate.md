# R1 CoverageLedger 0.3 child Schema / conformance 私有实现候选

日期：2026-10-18

> 状态：`R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_CANDIDATE`。
>
> 施工基线：`main@b4e741bc3b4029257f95cb1bfabbbd0e71c40bd3`，tree
> `b273a9655c6a4aac2cdabcb938ca2b1428281ebb`。
>
> 本文认领 doc284 A–J 的 bounded private implementation；不发布 merged、exact-main verified 或 frozen 状态，
> 不建立 composition、manifest successor、persistence 或 public Review 产品。

## 1. CONTROL LOOP 与生效授权

[root-binding correction 合同](281-r1-review-slice-set-coverage-root-binding-correction-contract.md)与
[独立冻结发布](282-r1-review-slice-set-coverage-root-binding-correction-contract-freeze-publication.md)保持原字节；
[可行性审计](283-r1-review-coverage-ledger-0-3-schema-conformance-feasibility-audit.md)已成为 qualified history。
[实现授权发布](284-r1-review-coverage-ledger-0-3-schema-conformance-implementation-authorization-publication.md)由 PR #326
合入本基线。它的 original Public CI、exact-main Public CI 与 Browser Smoke 均以各自 attempt 1 SUCCESS 闭合；fresh
README/doc283/doc284/milestones 为 4/4 qualifying PASS。independent reconciliation 与 149-artifact closeout 分别为：

```text
0c9358d34d234c29f4869de1a0b34b04cfb3b9282e10009074b11aacf5f5d19d
eb66acd79603423953c16cf12f25f6f54abf67b637d30e8c9979c0dacb61d027
```

doc283 与 doc284 的 full-file SHA-256 分别为：

```text
6cbcdfd3942d80a5eba8df2024ad1a8034a30e153eb9d53f7c071e7133d88fb7
23a56a76b22b8ca5d56f709726883f8eb84731782e62f238af8805ed566debe3
```

因此 `SCHEMA_IMPLEMENTATION_ALLOWED` 已生效。fresh CONTROL LOOP 重新核对 remote main、基线、open PR、冻结合同、
Schema、manifest、fixtures 与 retained counterexamples；remote main 仍为本基线，open PR 只有无关 Dependabot 更新，没有更早
semantic seam 或反例要求重开 Fact、Relation、ReviewSlice、Schema correction 或 root-binding contract。A–J 仍是当前最小
合法施工面。该结论不是由文档编号、相同内容或绿色 CI 自动推出。

## 2. 实现 topology 与 authority ceiling

本候选新增 exact `review-coverage-ledger-0.3.schema.json`，并在 Review Attention 私有包中新增
`r1-review-coverage-ledger-conformance/0.3`。调用方必须显式提供：

```text
exact candidate
+ application-owned Fact handoff source digest
+ application-owned stage projections
+ application-owned root terminal-history projections
```

conformance source在入口即转为 canonical、copy-owned bytes。validator只验证候选是否等于这些 frozen inputs 机械导出的结果；
它不枚举 denominator、决定 stage status、生成 candidate、修补 history、取得 composition claim、消费 live continuation，或授予
publication authority。

实现只接受 exact：

```text
artifact_kind = COVERAGE_LEDGER
schema_version = 0.3
```

unknown、future与未物化的0.2均 fail closed；不存在 closest-version fallback。semantic bytes、digest或相同 world也不继承
live attempt、claim、one-shot ownership、closure、admission或continuation authority。

## 3. A–J 落地

| ID | 本候选实现 |
| --- | --- |
| A | 新增 closed exact 0.3 child Schema，固定 `$id`、artifact/version、canonical profile、seven-stage shape与ordered root chain |
| B | 直接承载冻结的seven-stage、blocker、reason、canonical order与conservative join；不创建0.2文件 |
| C | 固定 `FACT_SET -> RELATION_SET -> REVIEW_SLICE_SET`，并对present / qualified absent / qualified unknown声明state-local required/forbidden members |
| D | 新增独立、versioned、fail-closed、validation-only conformance；Schema witness不能替代cross-field conformance |
| E | 从显式application history复算terminal-history、binding、predecessor、chain与Ledger digest，并拒绝candidate self-report |
| F | 固定八个positive worlds与对应identity vectors |
| G | 将 `RSCSC-000..016` 与 `RBCC-000..011` 全部落为直接测试身份 |
| H | exact 0.3 dispatch，明确拒绝0.2、future及unknown child |
| I | 对CoverageLedger 0.1、common 0.1、manifest 0.1与19个历史fixture文件建立全字节守卫 |
| J | 在CPython 3.10.6/3.13.13、normal/`-O`运行同一68项声明矩阵并比较canonical report bytes |

## 4. terminal history 不是 opaque digest

root binding不能只接受任意JSON后计算摘要。每个stage/terminal branch都具有closed、canonical name/value vector；实现检查：

```text
exact applicable member names
+ lexicographic canonical order
+ no duplicate / invented / omitted member
+ same-attempt source
+ exact predecessor binding where applicable
```

当前closed branches覆盖：

- Fact normal、zero denominator、all rejected、projection blocked与required Provider non-success；
- Relation admitted、admitted conflict、predecessor absent与known-prefix-only；
- ReviewSlice normal closed、closed empty、normal partial、predecessor absent与predecessor unknown。

因此删除一个适用history member、交换成员顺序、移植foreign predecessor或用caller字段改写历史都会在conformance boundary失败。
这只证明传入history与candidate一致；谁有资格形成application-owned history仍由上游冻结 authority拥有。

## 5. eight positive worlds

规范corpus包含：

```text
normal
branch_empty
slice_partial
zero_parse_denominator
all_parse_rejected
projection_blocked
required_provider_non_success
qualified_unknown
```

八个world各有独立root-chain与Ledger identity。branch-empty继续是present artifact；zero denominator、all rejected、projection
blocked与required Provider non-success不会被压成同一个absence；qualified unknown只能保存authoritative known prefix，任何observed
item越出该prefix都会失败。

## 6. direct falsifiers 与不可变字节

24项direct test完整覆盖：

- Schema缺字段、错误blocker family、cross-stage blocker、非canonical顺序、重复与partition不闭合；
- old digest domain、foreign attempt、unknown promotion、branch-empty改写absence、binding交换与foreign predecessor；
- terminal-history member遗漏、顺序变化与predecessor self-report；
- Schema通过但conformance必须拒绝的status、history、source与authority错层；
- 0.1 child / common / manifest / 历史fixtures immutable guards。

不可变摘要为：

```text
review-coverage-ledger-0.1.schema.json = e51836e40109741c631906aa8b31e97f61945683535d3b0c8e89ce5bff0b2545
review-r1-common-0.1.schema.json       = e36ff4006fa038a05b5b211d77dca4ab5ecde71b158d81a5d3fd6689b350da4a
review-derivation-manifest-0.1        = 6981e740215d9cf0a35fc78b7cb84b7d8f09792335609c1f089b3623ff5d6b91
19 historical fixture files          = 3b8923da003ea5c27926b0366981a972daf1f941452bcdd9cded3fbcbb5ebe9e
```

## 7. declared local qualification

最终实现测试面由24项direct A–J tests与44项既有Schema regressions组成，共68项。四格使用同一runner与final product bytes：

| Python | mode | 结果 |
| --- | --- | --- |
| 3.10.6 | normal | 68/68 PASS |
| 3.10.6 | `-O` | 68/68 PASS |
| 3.13.13 | normal | 68/68 PASS |
| 3.13.13 | `-O` | 68/68 PASS |

四份canonical reports逐字节一致：

```text
3690636fede8c31bb99cc2fac50cecaa3b5443c14b97a94b05f99a3f7c9d43d8
```

corpus与0.3 Schema当前摘要分别为：

```text
b4eb5f81c248cc898d28bf520ba689a19278640d40ad6bc11bfe58e757c1cd5c
d1fce2ba6fe6017bb73070896ad7c7801284157d1dc467c4c3bc2c507470dc83
```

本机检查时可用内存低于现有Public CI Core regression声明的4096 MiB soft gate，因此没有在已知资源不足的host上把更宽全套
回归冒充本地资格。该矩阵将在本候选final bytes的original Public CI中独立执行；绿色结果不能预先写入本文。

## 8. retained failure / setup history

以下身份保持原样，后继PASS没有覆盖或重新解释它们：

1. narrow attempt 1：13 pass / 3 fail / 4 error，暴露fixture与local shape findings；
2. narrow attempt 2：19 pass / 1 fail，归为negative-vector harness order error；
3. Schema regression attempt 1：62 pass / 2 fail，暴露open terminal-history object与registry omission；
4. Schema regression attempt 2：58 pass / 1 error，未设置明确source path，归为local test import-path setup error；
5. four-grid attempt 1：四格均为runner import-path setup error；runner修正后才以fresh attempt 2取得四格PASS。
6. final-bytes four-grid attempt 3的PowerShell convenience summary把scalar digest索引成首字符`3`；四份产品report
   均保留完整一致摘要，fresh read-only comparison PASS。该身份归为proof-facility summary setup error。

这些观察促成closed terminal-history vectors、successor registry与明确runner source path，但不被包装成产品、合同或上游失败。

## 9. 当前状态与 stop line

本文只允许发布：

```text
R1_REVIEW_SLICE_SET_COVERAGE_ROOT_BINDING_CORRECTION_CONTRACT_FROZEN
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_FEASIBILITY_AUDITED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_ALLOWED
R1_REVIEW_COVERAGE_LEDGER_0_3_SCHEMA_CONFORMANCE_IMPLEMENTATION_CANDIDATE
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_FEASIBILITY_NOT_STARTED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_IMPLEMENTATION_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_MANIFEST_SUCCESSOR_NOT_SELECTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
```

本候选不得：

- 创建assembler、枚举seven-stage denominator、决定stage status或overall join；
- 修改0.1/common/manifest或历史fixtures；
- 选择manifest successor、negative-world transport、persistence Route A/B或public carrier；
- 启动composition feasibility/runtime、public Review产品、Evidence/Bundle/publisher、CLI/Workbench/Core、R2/R3、
  `CLAIM_FIDELITY`、tag或Release。

出现必须从caller恢复stage truth、需要先实现composition/manifest/persistence、或direct falsifier击穿frozen contract时，必须保留
反例并停在被击穿的最小边界。

## 10. implementation candidate 自己的资格门

本文与实现进入分支不等于候选取得资格。final bytes仍需：

```text
declared local A–J gates
    -> original PR required gates
    -> separately approved exact-head protected merge
    -> new exact-main Public CI + Browser Smoke
    -> fresh anonymous installed-product README / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / retained-history reconciliation
    -> IMPLEMENTATION_CANDIDATE / EXACT_MAIN_VERIFIED / READBACK_QUALIFIED
```

上述链闭合以后仍不是 `FROZEN`。冻结只能由后继独立docs-only publication发布，并再次取得自己的完整资格。same patch、tree、
content、digest、semantic result或本地PASS都不能替代任一身份。本地checkout对齐只作housekeeping，不新增资格门。

当前停止线：

> CoverageLedger 0.3 child Schema与versioned conformance已经在bounded A–J内形成私有实现候选；它只验证application-owned
> exact history与候选的一致性，不拥有composition、transport、persistence或publication authority。
