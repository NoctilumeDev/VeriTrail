# R1 Parse fulfillment private implementation 实现授权发布

日期：2026-09-29

> 条件化状态目标（仅本文最后门全部成立后生效）：
> `R1_PARSE_FULFILLMENT_CONTRACT_FROZEN /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_FEASIBILITY_AUDITED /
> R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED /
> R1_PARSE_FULFILLMENT_IMPLEMENTATION_NOT_STARTED /
> R1_PARSE_TO_FACT_CONSUMER_CORRECTION_CONTRACT_NOT_STARTED /
> R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN /
> R1_REVIEW_SLICE_SET_COVERAGE_QUALIFICATION_CONTRACT_NOT_STARTED /
> R1_RELATION_SET_SLICE_COVERAGE_IMPLEMENTATION_NOT_STARTED`
>
> 发布基线：`main@23f9825e61791a78056d5154e4dfd3626a1167b1`，Git tree
> `ae1496ba1978ddb40b3a74e414b4e6f58f9bddd5`
>
> 冻结合同：[Parse fulfillment 最小合同 0.1](217-r1-parse-fulfillment-contract.md)
>
> 冻结发布：[Parse fulfillment 合同冻结发布](218-r1-parse-fulfillment-contract-freeze-publication.md)
>
> 可行性审计：[Parse private implementation 可行性审计](219-r1-parse-private-implementation-feasibility-audit.md)
>
> 影响层级：`L2_IMPLEMENTATION_AUTHORIZATION_PUBLICATION + L3_SYSTEM_AUDIT + L0_DOCUMENTATION`。本轮不修改
> runtime、tests、Schema、Profile、Policy、corpus、identity vector、Provider、Fact/Relation/Slice/Coverage、
> Evidence、Manifest、publisher、Bundle、CLI、Workbench、Core、P/Q/D/Cu/O/T、tag 或 Release。

## 1. CONTROL LOOP 结论

文档 219 的原始 PR、受保护合入、新 exact-main 双门、fresh installed-product readback 与 independent
reconciliation 已经全部成立，因此它不再只是 candidate；它现在是 qualified feasibility history。重新绑定
`main@23f9825e61791a78056d5154e4dfd3626a1167b1` 后，没有新证据击穿：

- `r1-python-parse/0.1` 的 CPython 3.10.6 reference semantics；
- exact Language Support `ELIGIBLE` denominator 与 source-gate object identity；
- controller 显式选择 exact reference executable 的 capability boundary；
- reference worker 产生 candidate semantic product、application 拥有 admission/reconciliation 的分权；
- private same-attempt canonical product 不等于 persistence 或 public Artifact；
- current Fact projection/request/wire 不得静默升级为 post-Parse consumer。

因此当前最小合法下一刀仍是文档 219 第 8 节的 private A–H implementation。合同冻结与可行性审计本身不自动
授予施工权；本文只条件化发布这项有限 authority。本文自己的最后门闭合以前，runtime 继续
`NOT_STARTED / NOT_AUTHORIZED`。

## 2. 可行性审计资格已经闭合

文档 219 候选 PR #242 的 exact coordinates 为：

```text
base  = bb912680d55ca8c96df4d5b9ded88187bbaf42ef
head  = ed3cfa2871df864e84068cc32f52081863de8878
merge = 23f9825e61791a78056d5154e4dfd3626a1167b1
tree  = ae1496ba1978ddb40b3a74e414b4e6f58f9bddd5
```

原始与 exact-main 远端门均在 attempt 1 成立：

| 门 | Run | 结果 |
| --- | --- | --- |
| PR #242 Public CI | `36440677161` | `11/11 SUCCESS` |
| exact-main Public CI | `36443544885` | `11/11 SUCCESS` |
| exact-main Browser Smoke | `36443544713` | `1/1 SUCCESS` |

从该 exact main 建立的 fresh CPython 3.13.13 installed-product readback 对 README、文档 219 与 milestones 使用三个
独立 Plan/session/output；P1/P2 均 `COMPLETE`，Core 均 `PASS`。AGENTS、README、文档 217、文档 218、
文档 219 与 milestones 六份匿名 raw source bytes 逐字节等于 exact Git blobs。独立 verifier 又核对 source
ancestry/tree、PR/CI identity、prior freeze manifest、Plan/Evidence/handoff/Core report 与 source bytes；最终
canonical manifest 为：

```text
sha256_json  = decd28d53dc3bfb7af0d9033e1e4ca1feadaa7e4daf300df29babe65bcb07ff7
sha256_bytes = 6624609f0b1ee6c7e78f7200f785a39fb69462f161bcefaeda70a10a480fca2f
```

资格轮询期间的六次只读网络观察错误分别保留为 GitHub API EOF、direct connect timeout 与 proxy TLS handshake
error；它们没有修改 candidate 或远端 run，也不是 CI failure。installed-environment preflight 在 exit 0 后产生的
Playwright async shutdown `TargetClosedError` 同样保留为 preflight history；正式 Plan/session 尚未开始，后继
三份 qualifying readback 没有覆盖或解释它。

## 3. exact main 的约束字节

```text
eb16303547bad45eb3f22b8209c0e6b46c681495f42bb0c8810666787235264f  docs/217-r1-parse-fulfillment-contract.md
a977cb22e73c812c5e081180f811d740de0a8b874a7239c82c201ab720f42b9a  docs/218-r1-parse-fulfillment-contract-freeze-publication.md
8fcecd73274e0c1d54021a7862e8d34ad68ceb6ae4f5f697e6c2fb17135bf774  docs/219-r1-parse-private-implementation-feasibility-audit.md

7705ba4b4a9d91697ba9a5c5e31d868b88fb22d9b4ba37fdb7ee8e188081c259  plugins/review-attention/src/veritrail_review/_source_operation_gate.py
c90412ec2218110350dc7fef87ad8292113ffc550ec770eddb9ea46bae852af3  plugins/review-attention/src/veritrail_review/_windows_execution_cell.py
e774cdba9cc3a2820c58e1806f76ec066558b9b07260f6558a564e91e08ebca5  plugins/review-attention/src/veritrail_review/_language_support.py
70286924c2590c1acfc494a52bfa800e3777c6cd8f80993045abad90339f5ace  plugins/review-attention/src/veritrail_review/_language_support_values.py
eeb82823563aeb7460cd06eec4cec08091e7342fdc74d251ed5f2a35234e0dbd  plugins/review-attention/src/veritrail_review/_source_operation_fact_application.py
252f8018404c294daffecedb74519203dce33fb6b734ce99cd9405db0b82b4f9  plugins/review-attention/src/veritrail_review/_source_operation_fact_worker.py
```

本文读取这些字节来限定 authority，不把 publication 解释成合同 version bump、runtime implementation、Fact wire
correction 或 persistence decision。

## 4. 发布的有限 authority

本文最后门全部成立后，下一分支只允许实现文档 219 第 8 节已经审计的 private stages：

```text
A. exact input / classification / blob-history revalidation
B. exact ELIGIBLE denominator + frozen decode construction
C. explicit CPython 3.10.6 runtime capability and per-subject one-shot claims
D. contained reference worker request / terminal and private canonical product
E. semantic result / lifecycle / infrastructure failure separation
F. missing / duplicate / dangling / foreign-attempt / cross-world reconciliation
G. application-owned admitted product / product-set semantic identity and copy-owned access
H. attempt-bound one-shot continuation + PFCT-000..016 hardening
```

实现 authority 还受以下约束：

1. 新对象与函数保持 `veritrail_review` private，不进入顶层 exports、CLI、entry point 或 plugin discovery；
2. denominator 只能来自 exact Language Support `ELIGIBLE` subjects；parser、Provider 与 caller subset 不拥有分母；
3. reference runtime 必须由 controller 以显式绝对路径选择并绑定本次 prepared attempt；不得使用 ambient
   `sys.executable`、PATH、`py` launcher、host feature emulation 或自动下载；
4. worker 必须要求 exact CPython 3.10.6，并只产生 candidate semantic result；version/descriptor 自报不能单独建立
   trusted runtime authority；
5. application 必须独立验证 lifecycle、terminal、binding 与完整 denominator，之后才能 admission product set；
6. reference runtime absence、启动/worker/terminal/release/timeout/resource failure 不得伪装 `PARSE_ERROR` 或空闭包；
7. private canonical product/product-set 可以形成 same-attempt semantic identity，但不是 public Artifact、Evidence、
   receipt、Coverage denominator 或 historical persistence；
8. continuation 必须 one-shot 绑定原 `BudgetContext`、parent eligibility、exact classification、全部 child claims、
   complete reconciliation 与本次 product-set binding；
9. current Fact projection/request/wire、Provider scheduling 与 product-use enforcement 保持原字节。

这项 authority 只允许开始实现，不预先声明实现正确、完成、合入、exact-main verified 或 frozen。

## 5. 不授权的邻接能力

```text
current Fact projection/request/wire changes
Fact Provider scheduling or Parse product-use enforcement
zero-accepted required-provider behavior
historical/offline product persistence Route B
public Parse Schema / carrier / corpus / identity vectors
runtime download / installation / signing / attestation
Fact fulfillment or obligation-universe derivation
shared Language Support / Parse / Fact receipt or ledger
ReviewSliceSet / CoverageLedger
Evidence / Manifest / publisher / output root / Bundle
CLI / Workbench / Core / Q / O / T runtime
tag / Release
```

尤其：

```text
PRIVATE_IMPLEMENTATION_ALLOWED
    != implementation started
    != parser integration completed
    != current Fact consumer corrected
    != persistence selected
    != Coverage authorized
```

## 6. 实现必须继续面对的反证

文档 219 的 `PFI-000..016` 全部继续约束 implementation。至少必须直接证明：

- equal exact inputs、classification 或 product bytes 不继承另一 attempt 的 claim/continuation；
- runtime unavailable 与 lifecycle failure 不生成 semantic result；
- one child completion 不关闭 parent denominator；
- missing、duplicate、dangling、foreign-attempt、cross-world 与 post-construction mutation fail closed；
- zero denominator 与 all-rejected complete identity 不同，且二者都不自动形成 Fact/Coverage closure；
- current Fact wire 能接收 eligible raw bytes 不证明它有权消费 Parse product；
- finite corpus、descriptor/version response 与 hash equality 都不能替代 owner-side validation。

若 implementation 审计发现 frozen semantics 不能在上述有限边界内成立，必须停止，保留反例，并只显式 reopen/version
被击穿的最小边界；不得以“publication 已授权”为由扩大实现。

## 7. implementation 的后继资格链

implementation 分支形成最终字节以后，仍必须独立经过：

```text
implementation final bytes
    -> implementation layer declared local gates
    -> original PR required checks
    -> protected main merge
    -> new exact-main Public CI + Browser Smoke
    -> required fresh product observation / reconciliation
    -> implementation fact publication
    -> return to CONTROL LOOP
```

本文不预先决定 implementation 的文件布局、private class 名称、test count、public readback surface 或后继 publication
形状。测试是 witness，不拥有扩张 A–H、修改 contract、选择 persistence 或启动 Fact/Coverage 的 authority。

## 8. 本 publication 的最后门

本 docs-only publication 只允许同步 `AGENTS.md`、`README.md`、`docs/milestones.md` 并新增本文。
doc217/218/219、runtime、tests、Schema、Profile、Policy、corpus、architecture DOT/SVG 与 identity vectors 必须保持
原字节。

提交前必须通过本层声明的双 Python normal/`-O` docs/Schema regressions、relative links、UTF-8 without BOM、
LF/final-LF、heading/fence、状态 marker、敏感路径、exact diff scope、frozen byte continuity 与
`git diff --check`。随后必须完成：

```text
original PR required checks
    -> protected main merge
    -> that exact main Public CI + Browser Smoke
    -> fresh anonymous installed-product readback of README / doc219 / 本文 / milestones
    -> independent Core and source-byte reconciliation
    -> conditional authorization state takes effect
```

任一非成功观察都保留原身份；后继 PASS 不覆盖首败。本文中的
`R1_PARSE_FULFILLMENT_PRIVATE_IMPLEMENTATION_ALLOWED` 在最后门闭合以前只是一项 target marker，不能授权
runtime branch 提前开始。最后门闭合后也必须先重新绑定新的 exact main 并再次执行 CONTROL LOOP；只有最小
A–H implementation 仍成立时，才可创建 implementation branch。

### 8.1 本地资格结果

施工中有五项 setup history：

1. 第一次试图用 JavaScript `TextEncoder` 生成 Python edit script，tool wrapper 在 shell 调用前以
   `ReferenceError: TextEncoder is not defined` 停止；没有命令执行或文件 mutation。
2. README 与 doc220 已由独立命令写入后，第一次 AGENTS append writer 在实际 `WriteAllText` 前把字符串换行替换
   误解析为 `String.Replace(Char, Char)`，以 `MethodException` 停止；该失败 invocation 没有对 AGENTS 产生
   mutation，后继使用明确 string overload 重新开始。
3. prequalification newline inspection 发现四个本轮文档文件均缺 final LF；第一次 correction one-liner 因 shell
   quoting 写入了反斜杠与字母 n 两个 literal bytes。随后四格 docs/Schema tests 仍然全绿，但 independent static
   gate 明确以 no-final-LF 停止。该结果保留为 INVALID_FINAL_BYTE_SETUP，证明 tests 不能替代 byte-level gate；
   后继用显式 byte values 统一修正四个文件，再从新 final bytes 重新资格化。
4. 更新本段 setup history 的两个外层 JavaScript template 都因待写 Markdown backticks 在 shell 启动前分别触发
   Unexpected identifier；没有命令执行或文件 mutation，后继移除 wrapper 歧义后重新开始。
5. final static checker 有两次 command-construction failure：第一次因两个 `ReadAllText` 调用各遗漏一个右括号，
   在 PowerShell 解析阶段以 `Missing ')' in method call` 停止；后继压缩版又把 `Join-Path` 与参数连成
   `Join-Pathdocs$r`，在完成 scope/hash/encoding 后于 link check 停止。两次都没有文件 mutation，也没有被当作
   static PASS；后继使用未压缩的完整 checker 从头重新运行。

修正后的 candidate bytes 首轮通过：

| Lane | 结果 |
| --- | --- |
| CPython 3.10.6 normal | `40/40 PASS` |
| CPython 3.10.6 `-O` | `40/40 PASS` |
| CPython 3.13.13 normal | `40/40 PASS` |
| CPython 3.13.13 `-O` | `40/40 PASS` |

每格运行 `tests.test_markdown`、`tests.test_review_r1_admission_evidence_schema`、
`tests.test_review_r1_derivation_evidence_schema_correction` 与 `tests.test_review_r1_schema_payload`。本节与全部 setup
history 写入后，同一 final bytes 的四格再次全部为 `40/40 PASS`。独立 static checker 又确认 exact diff scope 为
AGENTS、README、milestones 与 doc220 四个文档文件，doc217/218/219 与六个相关 runtime 文件的九份 SHA-256
连续，relative links、UTF-8 without BOM、LF/final-LF、heading/fence、target markers、敏感路径与
`git diff --check` 均成立。首轮 PASS、后继 PASS 与 static PASS 各自只作本 candidate 的 witness。
