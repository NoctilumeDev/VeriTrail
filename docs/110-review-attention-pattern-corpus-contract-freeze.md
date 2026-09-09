# Review Attention Pattern Corpus 合同冻结状态发布

> 状态发布目标：`CORPUS_CONTRACT_0.1_FROZEN / LEDGER_OPEN / CORPUS_NOT_SELECTED / R1_BLOCKED`
>
> 合同候选合入基线：`main@8526c5551cce3a9a9e916917381e0e0463a082f0`
>
> 冻结合同：[文档 109](109-review-attention-pattern-corpus-freeze-contract.md)
>
> 影响层级：`L0_DOCUMENTATION + L2_CONTRACT_STATUS`；只发布合同候选已经通过的门禁、合入与公开读回
> 事实，不选择 Pattern、生成 manifest、追加 `FROZEN_PATTERN` revision 或启动 R1

## 1. 发布裁决

文档 109 已把 Ledger 到首个 Pattern Corpus 的输入、最小充分选择、非自指 manifest、exact source commit
和后继 closure 顺序限定为 0.1 合同。与它同一候选提交的 Ledger 只把 P2–P4 已保留的六条反例追加为
`RA-022` 至 `RA-027` 的完整 `GENERALIZED rev1`，没有把任何记录提升或选入 Corpus。

该候选已经完成自己的原始远端门禁、受保护主线合入、合入后 exact-main 门禁和两页 fresh anonymous
Chromium 产品读回。本文只发布这条已经形成的候选闭环，不增加选择语义。本文自身仍须再经过原始远端
门禁、受保护主线合入与合入后 exact-main 匿名读回；只有该链全部成立，`CORPUS_CONTRACT_0.1_FROZEN`
才成为当前主线事实。任何新反例仍可否决发布。

## 2. 候选提交、PR 与受保护主线

- 候选基线：`main@b2dae28fea70abe6e1bfa1066dbb1ddc4ff9c292`；
- 候选提交：`6b617412194a31ecf149f22eee088778fa0cfaf2`；
- [PR #85](https://github.com/NoctilumeDev/VeriTrail/pull/85) 的原始
  [Public CI run 34340040574](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34340040574)
  在 attempt 1 上生成 11 个 job，全部 `COMPLETED / SUCCESS`，没有 rerun；
- PR #85 以 merge commit `8526c5551cce3a9a9e916917381e0e0463a082f0` 合入受保护 `main`；
- merge tree 为 `66a16a7c7d542b062a1f1ac68adb507738478380`；parents 为候选基线
  `b2dae28fea70abe6e1bfa1066dbb1ddc4ff9c292` 与候选提交
  `6b617412194a31ecf149f22eee088778fa0cfaf2`。

合入后的 exact main 又独立完成：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 34341069511](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34341069511) | attempt 1，`11/11 SUCCESS`，`headSha=8526c555...` |
| [Browser Smoke 34341069566](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34341069566) | attempt 1，`1/1 SUCCESS`，`headSha=8526c555...` |

这组事实分别固定候选分支、受保护合入和合入后主线状态；任一层都不替代另一层。

## 3. Exact-main 匿名产品读回

产品 P2 Public Render Collector 从 `main@8526c555...` 的源码绑定环境，在 fresh anonymous Chromium
context 中串行读取 README 与文档 109：

| 页面 / viewport | artifact SHA-256 | marker | coverage / stability | facts digest |
| --- | --- | --- | --- | --- |
| `README.md` / desktop | `a8bc062332c4dbb42d6ad556ed86bc90b74a15da6c25f1af318364d5d3b5430d` | `Pattern Corpus`，6 次 | `COMPLETE`；三次 sample 均为 `8486498dd96ecfc92f883cf6e372bfcded1204f2494f0db5d46bed750804884a` | `97efeeeabb16a03efee231a92a76b991760212e51eeb1ca82e12f8beb96e1feb` |
| `docs/109-review-attention-pattern-corpus-freeze-contract.md` / narrow | `0af51d8af57cbcb0a2a4d40ddd9186d9b423dcf2cf67b6ee213038bf80aa2f57` | `CORPUS_CONTRACT_CANDIDATE`，2 次 | `COMPLETE`；三次 sample 均为 `56fb55b681b60c9a74e8d64a9b1daa242a7eb73f85853301bdc9d7699c1f001a` | `7f320faf2502e996ea6990965a6ff8b7d1c1429d2a7437984de952f3bd86a611` |

两页 requested/final path 都保持同一 exact-SHA 坐标并返回 HTTP 200；固定正文 scope 唯一且 usable，
response-body active streams 为 0，`errors / conflicts / cleanup_errors` 均为空。README 读回记录 152 个
请求、3 个只读策略阻断写请求与 8,003,157 delivered bytes；文档 109 记录 141 个请求、2 个阻断写请求与
7,630,200 delivered bytes。两页的阻断都不影响 coverage。

首个 README 请求误选 `CORPUS_CONTRACT_CANDIDATE` 作为 marker；页面本身仍返回 `COMPLETE`，但该词在
README 中 occurrence 为 0，因此这次请求没有被用作 marker 语义证据。后继只修正请求输入为 README
实际存在的 `Pattern Corpus`，没有把第一次不匹配改写成页面或网络失败。内置浏览器控制通道两次未能
建立可信 Node bridge，因此没有产生 UI 自动化证据；上述读回来自仓库自身冻结的产品 P2 Collector，
两类通道没有互相替代。

## 4. 冻结边界

合同 0.1 冻结后仍然只有以下事实成立：

```text
R0 architecture remains frozen
Pattern Ledger remains append-only/open
P2-P4 retained examples are materialized through RA-027
Corpus selection and manifest rules are frozen
```

以下事实仍不成立：

```text
no Pattern has been selected
no CONTRACT_CANDIDATE or FROZEN_PATTERN successor has been appended
no corpus manifest exists
no exact corpus source commit or manifest digest exists
R1 has not started
```

因此，合同冻结只让下一步能够按固定规则审查候选 revision；它不是 Corpus payload，也不解除 R1 的
`P4_AND_PATTERN_CORPUS_FREEZE` 停止线。本补丁不修改 Core、P1–P4、Workbench、Schema、CLI、Provider、
CI、标签或 Release。

## 5. 本状态发布的最后门

本补丁只允许本文、README、AGENTS、R 轨 Plan 与里程碑索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 从该 exact main 用产品 P2 Collector 和 fresh anonymous Chromium 读取 README 与本文；
5. 两页均须保持 exact-SHA URL、HTTP 200、唯一 usable scope、`COMPLETE`、三样本稳定、指定 marker
   存在，且没有 error、conflict 或 cleanup error。

只有上述事实全部成立，以下状态才成为当前主线事实：

```text
CORPUS_CONTRACT_0.1_FROZEN
LEDGER_OPEN
CORPUS_NOT_SELECTED
R1_BLOCKED
```

唯一允许的后继是从新的 exact main 串行完成候选 revision 的选择审查；不得在本状态发布中预生成
manifest、预填未来 Corpus source commit，或借“合同已冻结”提前进入 R1。
