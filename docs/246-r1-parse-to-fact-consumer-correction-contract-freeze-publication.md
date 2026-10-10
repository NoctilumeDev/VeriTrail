# R1 Parse → Fact consumer correction 最小合同冻结发布

日期：2026-10-10

## 1. 发布对象与条件状态

本文只发布[文档 245](245-r1-parse-to-fact-consumer-correction-contract.md)定义的 Parse → Fact consumer
correction 最小合同 `0.1`。本文自己的 final bytes、original PR 门、受保护主线合入、new exact-main Public CI /
Browser Smoke、fresh anonymous installed-product readback 与 independent reconciliation 全部成立后，以下目标才成为
当前主线事实：

```text
R1_PARSE_FULFILLMENT_CONTRACT_FROZEN
R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_FROZEN
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

最后门闭合以前，当前事实仍是 qualified contract candidate。把 frozen marker 写入本分支只表达 publication target，
不能代替资格链，也不授予 Fact wire、Provider scheduling、product-use enforcement 或其他 runtime authority。

| 坐标 | 值 |
| --- | --- |
| 前置审计 | [文档 215](215-r1-parse-to-fact-consumer-projection-prerequisite-audit.md)、[文档 216](216-r1-parse-product-fact-consumer-binding-precontract-audit.md) |
| 冻结上游 | [Parse private implementation 最终冻结发布](244-r1-parse-private-implementation-freeze-publication.md) |
| 合同候选 | [文档 245](245-r1-parse-to-fact-consumer-correction-contract.md) |
| 候选 PR | [#282](https://github.com/NoctilumeDev/VeriTrail/pull/282) |
| 候选 base | `b166dee05fe995b17b2f3bb557d75c2feb4f5493` |
| 候选 final head | `56d6438459d4bbb1fad734eb875c85211895f3f5` |
| 候选 merge | `3214586645c67156d5c498cbcd2ea5ed1a7d6b43` |
| 候选 head / merge tree | `9b25d6bd996a616ca9a9193db1b204ed0d29762e` |
| 发布影响层级 | `L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY` |

## 2. 冻结范围

本文不新增文档 245 之外的合同语义。冻结对象只有：

```text
complete admitted Parse product-set + same-attempt continuation
    -> exact post-Parse consumer input identity
existing application-owned Provider applicability
    -> one complete ordered ACCEPTED-product membership per Provider
provider-bound one-shot child claim
    -> product-only immutable/copy-owned derivation authority
all required consumer children
    -> same parent attempt / same product-set reconciliation
    -> normal continuation eligibility
```

由此只发布以下边界：

1. successor consumer identity 必须是 versioned post-Parse identity，历史 raw-source projection/wire 不得静默继承；
2. consumer membership 只能由 complete Parse reconciliation 中的全部 ACCEPTED products 机械产生；
3. 每个 applicable Provider 获得独立 one-shot child claim，但共享同一份 application-owned Parse truth；
4. Provider 只能消费 claim 分配的 admitted products；raw body、path reread、reparse、digest 或 identity 回显不能替代；
5. output 与 continuation 必须绑定同一 parent attempt、Provider claim 与 exact product set；
6. missing、duplicate、rejected、foreign-attempt、cross-world、未 claim、未消费或 lifecycle non-success 均 fail closed；
7. zero denominator 与 all-rejected complete 保留不同 identity，首版都阻断 normal Fact launch；
8. zero-accepted 阻断不创建 empty FactSet，不证明 Fact fulfillment，也不形成 Coverage closure。

以下继续不是本合同事实：

```text
Fact obligation-universe derivation
Fact fulfillment / exact completeness proof
zero-member FactSet or Coverage closure
persistence Route selection
public Schema / carrier / Evidence / Manifest / publisher / Bundle
ReviewSliceSet / CoverageLedger
CLI / Workbench / Core / other top-level tracks
DECLARED_CLAIM_FIDELITY
```

## 3. 候选精确链与 original qualification

PR #282 最终为两个 commits；第二个 commit 只恢复文档 216 的 qualified historical bytes，并把当前 CONTROL LOOP
re-entry 事实留给文档 245。最终 diff 只有：

```text
AGENTS.md
README.md
docs/245-r1-parse-to-fact-consumer-correction-contract.md
docs/milestones.md
```

文档 216 不在最终 diff；runtime、tests、Schema、Profile、Policy、corpus、identity vectors、architecture DOT/SVG 与
public product bytes均未修改。candidate 与 ordinary merge tree 相同，merge parents 依次为：

```text
b166dee05fe995b17b2f3bb557d75c2feb4f5493
56d6438459d4bbb1fad734eb875c85211895f3f5
```

PR final head 上保留两个独立 workflow run：

| Run | Trigger identity | Attempt | 结果 |
| --- | --- | ---: | --- |
| `38007576277` | edited-triggered | 1 | `CANCELLED` by concurrency，保留 |
| `38007576374` | fresh independent run | 1 | `11/11 SUCCESS` |

后者不是前者的 rerun；成功不覆盖或解释 cancelled identity。受保护合入后的 exact-main 门为：

| 门 | Run | Attempt | 结果 |
| --- | ---: | ---: | --- |
| Public CI | `38010089320` | 1 | `11/11 SUCCESS` |
| Browser Smoke | `38010089337` | 1 | `1/1 SUCCESS` |

候选最终字节本地资格的 canonical summary SHA-256 为：

```text
7e71d8e0a6c1cf0ccbb729da26a89b9b8b5b3e82d1893794ff09805dfe54a152
```

该 summary 记录 docs/Schema 四格各 `40/40 PASS`、相关 Parse/source-operation/Fact wire/controller/multi-Provider
suite 四格各 86 项（CPython 3.10.6 两格各 skipped=1），以及 exact four-file scope、links、encoding、markers、
敏感路径和 `git diff --check`。这些本地 witness 不替代 PR、exact-main 或 installed-product 资格。

## 4. 候选 fresh anonymous installed-product readback

候选读回从 detached exact `main@3214586645c67156d5c498cbcd2ea5ed1a7d6b43` 建立 fresh CPython
3.13.13 venv，安装公开 Core `0.13.0`、GitHub Evidence `0.1.0`、Playwright `1.62.0` 与 matching
Chromium。Core 与插件均从该 venv 的 `site-packages` 导入；token 与 `PYTHONPATH` 环境清空。公开 wheels：

```text
Core 0.13.0
95cb00c08fa4a29c21c798c7ca5a8200bb83f71cd11b31b1dea01c19ec5a8a04

GitHub Evidence 0.1.0
dcb788ec00eaf29c76e7b4a61d039a85e5fee0497703f8b97e4535ecf5a54caf
```

三个正式观察在 observation 前各自创建 sealed Plan，并使用互不复用的 Plan/session/output identity：

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-pfc-contract-readme` | `github-paired-43ea35b033db49b5b6491c793c4e9fa8` | `e3f54fafa220d90b22a1f8d826c89c54f6308ce62f468fd2989d4ba1dbe8953a` |
| 文档 245 | `r1-pfc-contract-doc245` | `github-paired-85a158eb4ec243d9b5b92bf54d134809` | `6ff9c3fced8d30926f38f4b9bc0780b86bd58b5be59962cbc5d42d6ab7282d97` |
| milestones | `r1-pfc-contract-milestones` | `github-paired-49622a07f837440ab82adc43a77c6a5f` | `eaebb706e4999755003342e359469643b770f155190e6b2f327f0227750227b4` |

三者均为 exact-SHA HTTP 200、P1/P2 `COMPLETE`、三样本稳定、唯一 candidate marker、零 conflict /
coverage reason / cleanup error / active stream，Core 为 `PASS`。README、文档 245 与 milestones 的匿名 raw-source
bytes 又逐字节等于 exact Git blobs；raw-source check 只作 byte reconciliation，不替代 P1/P2 Evidence。

## 5. 候选 independent reconciliation 与保留历史

独立 verifier 重新核对 merge identity/tree、三个 Plan/session/handoff、outer 与 Bundle Evidence bytes、Core reports、
public raw bytes 和 target marker。全部 11 项检查成立，canonical reconciliation SHA-256 为：

```text
db518b6da6d51e00097abb95baaae01081ff0e8694234852f3d6ca00df1e6fcf
```

资格链同时保留以下 non-qualifying observations：

1. static-check 首次把 PowerShell `*.py` 当作 literal path，未创建 formal Plan；
2. fresh venv 首次组合 package-version probe 在公开 wheels 安装成功、`pip check` 通过后，因 Playwright 尚未作为
   harness dependency 安装而 `PackageNotFoundError`；
3. environment preflight 成功写出 installed/API evidence 后，Playwright 在解释器 shutdown 时输出 pending-task /
   `TargetClosedError` warning；
4. reconciliation 已 PASS 并写出 bytes 后，外层 inspection 首次读取了旧文件名 `final-reconciliation.json`；
5. exact tree 核对首次把 `HEAD^{tree}` 未加引号交给 PowerShell，git 没有收到该 revision。

前两项是 setup error，第三项是 setup warning，后两项是 post-reconciliation operator inspection error。它们都没有
产品或合同失败身份，也没有被后继成功改写成未发生。reconciliation bytes 未因 inspection error 重跑或改写。

## 6. 未修改事实与未授权能力

文档 245 第 1–14 节语义、文档 215/216/217/244、runtime、tests、Schema、Profile、Policy、corpus、identity
vectors 与 architecture DOT/SVG 必须保持原字节。本文只把 qualified candidate 条件化发布为 frozen contract。

即使本发布最终生效，以下状态仍然成立：

```text
R1_PARSE_TO_FACT_CONSUMER_CORRECTION_IMPLEMENTATION_NOT_STARTED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED
R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED
```

因此不得直接修改 current Fact projection/request/wire、Provider scheduling、Parse product-use enforcement、Fact
output、persistence、public carrier、Fact fulfillment、Coverage、CLI、Workbench 或 Core。

## 7. 本发布自己的最后门

本 docs-only publication 只允许修改 `AGENTS.md`、`README.md`、
`docs/245-r1-parse-to-fact-consumer-correction-contract.md`、`docs/milestones.md` 并新增本文。

publication 施工中，第一次 README 多 hunk patch 使用的段落换行与 exact bytes 不一致，`apply_patch` 在写入前
原子拒绝；该 invocation 没有形成部分修改。后继按 exact line window 拆分补丁。该记录保留为
`PATCH_SETUP_ERROR / product_observation=false`，不具有合同或 runtime 失败身份。

提交前必须完成适用 docs/Schema regression 的 CPython 3.10.6 / 3.13.13、normal / `-O` 四格、relative links、
UTF-8 without BOM、LF/final LF、balanced fences、marker、敏感路径、exact scope、合同正文 continuity 与
`git diff --check`。本地门不能替代 publication 自己的 original required checks。

publication 最终文档字节的 docs/Schema regression 为：

| Lane | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `40/40 PASS` |
| CPython 3.10.6 `-O` | `40/40 PASS` |
| CPython 3.13.13 normal | `40/40 PASS` |
| CPython 3.13.13 `-O` | `40/40 PASS` |

四格严格串行执行，未修改 timeout、fixture 或 expected result。记录结果后，docs/Schema 与静态门必须在最终
publication bytes 上重新通过。

```text
publication final bytes
    -> original PR checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> target frozen state takes effect
```

任一非成功观察都保留原身份；诊断不计入资格，后继成功不改写先前观察。不得复用 #282 Evidence、拿候选绿灯
替代本发布门，或把相同内容解释成 qualification-path equivalence。

## 8. 后继停止线

本文最后门全部成立后，必须返回 CONTROL LOOP，从新的 exact main 重新读取文档 245 第 13 节和 current runtime，
再判断最小 private implementation audit 是否仍是当前合法问题。

合同 frozen 不自动授权实现。若新 evidence 揭示 consumer identity、membership、product-use、multi-Provider、
zero-accepted 或 continuation binding 前提失效，只重开被击穿的最小边界；不得按文档编号机械进入 runtime。
