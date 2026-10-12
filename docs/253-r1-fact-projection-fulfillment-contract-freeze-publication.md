# R1 Fact projection universe / fulfillment 最小合同冻结发布

日期：2026-10-12

## 1. 发布对象与条件状态

本文只发布[文档 252](252-r1-fact-projection-universe-and-fulfillment-contract.md)的最小语义合同
`r1-fact-projection-fulfillment/0.1`。文档 252 的全部已资格化字节保持不变；其中的 candidate marker 保存候选历史，
本发布自己的最后门闭合后才由本文承担当前冻结状态。

```text
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_PRIVATE_IMPLEMENTATION_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_CURRENT_STATE_AUDITED
R1_FACT_PROJECTION_FULFILLMENT_CONTRACT_FROZEN
R1_FACT_PROJECTION_FULFILLMENT_IMPLEMENTATION_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

这些 frozen 字节现在只表达 publication target。本文自己的 final-byte local gates、original PR qualification、
protected merge、new exact-main 双门、fresh anonymous installed-product observations 与 independent reconciliation
全部闭合以前，事实仍是 qualified contract candidate。合同冻结也不授予 implementation authority；完整 Fact
projection / fulfillment runtime 仍未开始。

| 坐标 | 值 |
| --- | --- |
| 当前状态再审计 | [文档 251](251-r1-fact-projection-fulfillment-current-state-audit.md) |
| 已冻结上游 consumer A–J | [文档 250](250-r1-parse-to-fact-consumer-private-implementation-freeze-publication.md) |
| 语义合同候选 | [文档 252](252-r1-fact-projection-universe-and-fulfillment-contract.md) |
| 候选 PR | [#290](https://github.com/NoctilumeDev/VeriTrail/pull/290) |
| 候选 base | `07e3e90e6b7976c660ae7643b0cde79cb9b97a8a` |
| 候选 final head | `63f0f31028416587f7db91358485fae71e6a0af2` |
| 候选 merge / 本发布 base | `da11ca26eef6739c3fd7560fe29b67e2618f4d1a` |
| 候选 head / merge tree | `05a0ae561ccec269368c1c5b230d03b946816f36` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围与证明强度

规范语义与 24 项 `FPFCT-001..024` 反例义务仍全部由文档 252 第 1–13 节定义。本文只发布其资格历史，不增删
predicate、reason、Provider membership、projection rule 或 successor requirement。最小边界为：

```text
complete admitted Parse products + reconciled Parse partition
    + sealed Policy mapping / frozen Profile / exact identity and anchor history
    -> application-owned complete obligation universe U
    -> independent expected semantic values E, or explicit projection block

each applicable closed Provider
    -> full U/E responsibility, separate child claim and actual child history
    -> full-content expected/output and bidirectional provenance reconciliation

all required qualified children + original live attempt authority
    -> one-shot normal continuation eligibility
```

未来 consumer `r1-parse-product-fact-consumer/0.2` 与 private protocol
`veritrail-review-parse-product-fact-cell/0.2` 是必须另受审的 successor 边界；旧 `/0.1` request、terminal、closure
或 token 不继承它们的 authority。frozen Fact identity、`r1-python-facts/0.1`、Profile、Policy 和 Schema 不变。

完整 universe 可枚举不保证全部 expected values 可表示。grammar ACCEPTED 的 normalized keyword declaration
不能被跳过、改名或改成 Parse REJECTED；正常 projection 必须显式阻断。总函数不承诺每个 grammar-accepted
source 都能产生 ordinary FactSet，也不允许用成功子集缩小 universe。

fulfillment 依赖实际 child history 与独立完整输出核账共同成立，不证明 worker 内部逐项执行，不要求逐项 receipt，
也不认证任意第三方 Provider sandbox。required 与 optional 的 lifecycle / failure 继续分别保留。

zero accepted 继续阻断 normal Fact child、empty-product request、FactSet 与 normal continuation；known-empty U
不产生 Fact-stage 或 Coverage closure。部分 ACCEPTED 与已对账 REJECTED 的混合世界，只闭合 accepted-product
domain，不把全仓源码 Coverage 写成 KNOWN。

## 3. 候选 source 与原始远端资格

PR #290 最终只有一个 commit、四个文件，`+383 / -2`：

```text
README.md
AGENTS.md
docs/252-r1-fact-projection-universe-and-fulfillment-contract.md
docs/milestones.md
```

受审 head 与 merge tree 完全相同。merge parents 依次为：

```text
07e3e90e6b7976c660ae7643b0cde79cb9b97a8a
63f0f31028416587f7db91358485fae71e6a0af2
```

| 门 | 原始 Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| #290 Public CI | [38172220489](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38172220489) | 1 | `11/11 SUCCESS` |
| candidate exact-main Public CI | [38174088676](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38174088676) | 1 | `11/11 SUCCESS` |
| candidate exact-main Browser Smoke | [38174088675](https://github.com/NoctilumeDev/VeriTrail/actions/runs/38174088675) | 1 | `1/1 SUCCESS` |

两个 Public CI run 的 Review Attention 四格均为 `473 reported / 471 passed / 2 skipped`，不能写成 473 项全部
实际通过。两个 skip 分别是 CI 缺少 local exact reference runtime witness，以及 explicit reference runtime / Windows
cell 组合 witness；远端绿灯不替代这些未执行的观察。

## 4. 候选本地 witness 与 byte continuity

候选最终字节 local qualification SHA-256：

```text
35e00ef41ef22c1e69b40e5251be00fea577e7c2a4a582247778fc1ad8cb083c
```

该记录绑定 169 份 terminal local witnesses。unchanged Parse/product-consumer/source-operation/multi-Provider 窄回归
在四格各 reported 128 项：CPython 3.10.6 normal / `-O` 各 `127 passed / 1 skipped`，CPython 3.13.13 两格各
`128 passed / 0 skipped`。三个 R1 Schema regression modules 在四格各 `36 passed / 0 skipped`。

normalized keyword boundary 三个 world 的四格共启动 12 个真实 reference Parse children，没有实际 Fact children；
CLASS terminal admission 只属 modeled witness，FUNCTION 在旧 protocol scope 外。四份 reduced report 同为
1,456 bytes，SHA-256：

```text
0d219416ae955fd8e29613646861a93247b8ed300d9eca079cd7ec80b57b1e3b
```

它们证明该有限 representability 边界，没有实现完整 projection，也不授予 successor authority。初次 direct-reference
diagnostic 未冒充 admitted-product witness。本发布不重跑这些 unchanged semantic worlds 来制造新的实现声明。

文档 252 的 qualified full-file SHA-256 必须继续等于：

```text
074852c5579443fe14af3497cc19ea1c649097cf211258ab3ee0104ecb011d81
```

## 5. 候选 fresh product observation 与保留历史

候选最终读回绑定 `main@da11ca26eef6739c3fd7560fe29b67e2618f4d1a`。fresh CPython 3.13.13 venv 从
`site-packages` 使用 released Core `0.13.0` 与 GitHub Evidence `0.1.0`，Playwright `1.62.0` / matching Chromium；
匿名路径清理 token 与 `PYTHONPATH`。公开 wheels 使用已封存下载字节，在新 venv 中核验并安装，不声称重新下载。

| Wheel | SHA-256 |
| --- | --- |
| Core 0.13.0 | `95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04` |
| GitHub Evidence 0.1.0 | `dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf` |

setup attempt 1 的 README readiness diagnostic 曾取得 P2 COMPLETE / HTTP 200，但所选 Fact marker occurrence 为 0。
独立的 NON-QUALIFYING instrumented diagnostic 捕获三份相同 innerText：2,660 bytes，SHA-256
`4109af4f3dbf6d940fc5666815badb5e93bc0824ac761a7247c95513c671dba2`。源码与 DOM 显示该 marker 位于关闭的
`details`，默认 innerText 不包含隐藏段落。该观察身份为 `MARKER_SELECTION_SETUP_ERROR_NON_QUALIFYING`，
不是产品 ERROR、合同 FAIL 或 formal readback；初次 setup 没有启动正式观察。

原 setup / diagnostic 的 36 份 immutable artifacts 被保留。新 setup attempt 2 使用 fresh venv、新 adapter freeze 与
全新 Plan/session/output identity。README 改选可见成熟度边界；doc252 与 milestones 仍观察 exact candidate marker。
这个改动不重解释旧 marker=0，也不声称 README P2 已读取折叠的 Fact 状态。

| Target | Fresh formal Plan | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-fact-contract-a2-formal-readme-1-da11ca2` | `github-paired-a3439e6549864637b75a46cf3c61a3f4` | `60b3f641a7b06a4c14da4bbe5daf61113ddaf91f0be76a240ca2c948260b19cb` |
| doc252 | `r1-fact-contract-a2-formal-doc252-1-da11ca2` | `github-paired-19bd84b617884ac9b4044b62a5719c93` | `29dfd3d9d68e615cfb68df906fcaac5a0788f916a57bc2a519e39b8e86501f0b` |
| milestones | `r1-fact-contract-a2-formal-milestones-1-da11ca2` | `github-paired-866803f850414f439504ce5e83178014` | `c37f4053d19bcfde0b77ea9eaf2760dc5beb798da8d72c0b4970c5efc5e397c7` |

三份正式观察均 P1/P2 COMPLETE、Core PASS，且 raw Markdown bytes 等于该 exact Git blobs。本 world 正式历史为
3 PASS / 0 formal non-success；三个新 readiness diagnostics 与之前的 marker-selection finding 都不参与资格。
README P2 证明的是可见句子“源码审查已有部分内部机制完成验证，完整产品尚未发布”；Fact candidate 状态由
doc252 / milestones 的产品观察与完整 source-byte reconciliation 绑定，不借隐藏文字替代观察。

independent Core / source-byte reconciliation SHA-256：

```text
ce57ba2d36b88795fb556669a69d438e94b09c910fef262a760e609bc8e0fec3
```

候选 closeout 绑定 95 份 terminal artifacts，SHA-256：

```text
144ca7521ec30fe9d3ad6e0ac808352f5ea31cd50a226deabb2a35329427bde5
```

[doc251 qualified history](251-r1-fact-projection-fulfillment-current-state-audit.md)的 cancelled runs、live-log snapshot
correction 与 setup warning，以及上游首败、formal ERROR、Windows hard-exit UNKNOWN 等均保留。新 PASS 不覆盖
旧历史，也不把旧 UNKNOWN 倒改为已知根因。本地 checkout 对齐和只读 hygiene 是关账整理，不是事后增加的冻结门。

## 6. 本发布自己的资格门

本轮只允许修改 README、AGENTS、milestones 并新增本文。doc252、所有旧合同、runtime、tests、workflows、Schema、
fixtures、Profile、Policy、identity vectors 与架构资产必须保持 qualified base bytes。

final publication bytes 提交前必须取得以下本地门：

1. 三个 unchanged R1 Schema regression modules：`test_review_r1_schema_payload.py`、
   `test_review_r1_admission_evidence_schema.py`、`test_review_r1_derivation_evidence_schema_correction.py`，
   CPython 3.10.6 / 3.13.13 normal / `-O` 四格，串行运行并保留实际 counts / skips；
2. exact four-file scope、其他 tracked bytes / doc252 hash continuity、UTF-8 without BOM、LF/final LF、relative links、
   balanced fences、unique headings、条件 marker / 禁止越权状态、敏感字面量和 `git diff --check`；
3. 重新核验候选 closeout、独立对账和被引用的 terminal witness seals；只读 repository hygiene，不删历史证据。

最终结果保存在本轮独立资格 Artifact。本节是预先固定的门，不冒充已执行 PASS；本地成功不替代 original PR checks。

```text
publication final bytes / declared local gates
    -> its original PR checks
    -> approved exact head / protected main merge
    -> that new exact main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc253 / milestones observations
    -> independent Core, source-byte and retained-history reconciliation
    -> CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

fresh readback 必须重新创建该 publication exact main 的 Plan/session/output identity，不复用候选观察。README 沿用
可见成熟度边界；doc253 与 milestones 观察 frozen target marker。doc252 的 unchanged full-file bytes 在对账中复核，
不修改它的历史 candidate marker，也不以匿名 raw bytes 替代 P1/P2 formal observation。

最终核账要求每个 required target 恰好选择一份 qualifying PASS，并机械枚举全部 retained formal observations、
diagnostics 和 setup findings；formal non-success 数量从历史导出，不预设 N。完整采集后的 Core FAIL/PENDING/
INCONCLUSIVE 继续保持自己的结论，未完成采集或未知 wrapper failure 才归 formal ERROR。任何后继观察都须独立身份。

新 main 若被其他 PR 推进，不拼接不同 SHA 的 readback set；本发布继续在自身 merge world 闭合，随后另回外环绑定
current main。出现反例先保留并归层，只重开被击穿的最小边界，不 rerun 洗白、不弱化门禁。

## 7. 生效后的停止线

合同冻结后只形成新的上游语义事实。下一次必须重读文档 252 第 13 节与 current runtime，审查 private feasibility /
implementation authorization 是否仍为最小合法问题；本文不替它们作出结论或预授施工权。

```text
Fact projection / fulfillment implementation = NOT_STARTED / NOT_AUTHORIZED
consumer / protocol successor implementation = NOT_STARTED / NOT_AUTHORIZED
Language Support / Parse / Fact persistence = OPEN / NOT_SELECTED
ReviewSliceSet / Coverage contract = NOT_STARTED
```

不启动 runtime、Schema、public carrier、Evidence / Bundle / publisher、Fact→Coverage handoff API、CLI / Workbench /
Core、其他顶层轨、CLAIM_FIDELITY、tag 或 Release；不把旧 A–J 的 product-use proof 扩大成完整 Fact fulfillment。
本发布仍不是 truth completeness、semantic completeness、bug completeness 或全仓审查完成的声明。
