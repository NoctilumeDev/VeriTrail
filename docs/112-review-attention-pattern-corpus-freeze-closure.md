# Review Attention 首个 Pattern Corpus 冻结闭环

> 状态发布目标：`PATTERN_CORPUS_0.1_FROZEN / LEDGER_OPEN / R1_ENTRY_UNBLOCKED / R1_IMPLEMENTATION_NOT_STARTED`
>
> Corpus source commit：`9bdcef30517309bbc87ed7fdb0fec395197ef58a`
>
> Manifest digest：`sha256:ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`
>
> 冻结合同：[文档 109](109-review-attention-pattern-corpus-freeze-contract.md)
>
> Payload 选择：[文档 111](111-review-attention-pattern-corpus-selection-candidate.md)
>
> 影响层级：`L0_DOCUMENTATION + L2_CONTRACT_STATUS`；只外部绑定已经合入的 Corpus source commit、
> manifest 摘要与公开读回事实，不修改 Ledger、manifest、Core、P 插件或任何 R1 实现

## 1. 发布裁决

首个 Review Attention Pattern Corpus 已在独立 payload 中按冻结合同完成选择：`RA-003 / RA-004 /
RA-008 / RA-023` 的精确 `FROZEN_PATTERN` successor 构成最小集合，manifest 不包含自身摘要、Git commit、
时间戳、当前 HEAD 或 Verdict。Payload 已经完成原始远端门禁、受保护主线合入、合入后 exact-main 门禁、
四组独立复算与匿名 exact-SHA 读回。

本文只发布已经形成的外部身份绑定。本文自身仍须经过原始远端门禁、受保护主线合入与合入后 exact-main
匿名读回；只有这条链全部成立，`PATTERN_CORPUS_0.1_FROZEN` 才成为当前主线事实。新反例仍可否决发布。

## 2. Payload、PR 与受保护主线

- Payload 起始基线：`main@37b41f5f8305cc1322c07ae53b72c1bb90a9b78a`；
- Payload 候选提交：`415bc3d28ae86ab298cb99f9e6a16164094e67f4`；
- [PR #87](https://github.com/NoctilumeDev/VeriTrail/pull/87) 的原始
  [Public CI run 34364181249](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34364181249)
  在 attempt 1 上生成 11 个 job，全部 `COMPLETED / SUCCESS`，没有 rerun；
- PR #87 以 merge commit `9bdcef30517309bbc87ed7fdb0fec395197ef58a` 合入受保护 `main`；
- merge tree 为 `5a4c539fd3fcbd0b159da6daafae10cf828e42aa`；parents 为 payload 基线
  `37b41f5f8305cc1322c07ae53b72c1bb90a9b78a` 与候选提交
  `415bc3d28ae86ab298cb99f9e6a16164094e67f4`。

合入后的 exact main 又独立完成：

| 门禁 | 结果 |
| --- | --- |
| [Public CI 34365607388](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34365607388) | attempt 1，`11/11 SUCCESS`，`headSha=9bdcef305...` |
| [Browser Smoke 34365607418](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34365607418) | attempt 1，`1/1 SUCCESS`，`headSha=9bdcef305...` |

候选分支、受保护合入与合入后主线是三个不同坐标；任一层都不替代另一层。

## 3. Corpus 身份与独立复算

Corpus 身份由 closure 外部绑定，不写回 manifest：

```text
Corpus source commit
    = 9bdcef30517309bbc87ed7fdb0fec395197ef58a

Manifest path
    = docs/review-attention-pattern-corpus-0.1.json

Manifest SHA-256
    = ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d
```

该 source commit 上的 manifest 精确选择：

| Pattern | Revision | Selected record digest |
| --- | ---: | --- |
| `RA-003` | 2 | `sha256:1e20737718ec5e4056dc39d91f750e81c0ccbfefa965b72c1d918bd679f669f7` |
| `RA-004` | 2 | `sha256:1915e4aba5b7604ed417c640ff54494c720cc2bb72c815bf4305f65f4d439077` |
| `RA-008` | 2 | `sha256:194cd1eae23cf3d063a41a9f0b5b3f664a19b3b4b283034acaee07bbddb2198f` |
| `RA-023` | 3 | `sha256:fcf5d2a2364aa89413ae6d9884380cf7a3ff3f43a309970230d3e204d91b538b` |

Closure 从 exact source commit 重新解析 Ledger 与 manifest，使用 CPython 3.10.6、3.13.13 的 normal 和
`-O` 四条路径运行不依赖 `assert` 的审计。四次均得到：20 条完整 revision、14 条线性 chain、4 个
manifest entry、相同的四条选择与相同 manifest 摘要。每条记录的 canonical digest、revision 连续性、
`supersedes_digest`、`FROZEN_PATTERN` 状态、分类投影、manifest 字段闭集与排序均重新验证，没有复用
payload 文档中的结论作为计算输入。

## 4. Exact-source 匿名公开读回

### 4.1 产品 P2 Render 读回

产品 P2 Public Render Collector 从 `main@9bdcef305...` 的源码绑定环境，在 fresh anonymous Chromium
context 中串行读取 README 与文档 111：

| 页面 / viewport | Artifact SHA-256 | Marker | Coverage / stability | Facts digest |
| --- | --- | --- | --- | --- |
| `README.md` / desktop | `91773af8636677d1d2191266840fc4c3000ab287f74ce611aaf8d25ea8635563` | `CORPUS_PAYLOAD_CANDIDATE`，1 次 | `COMPLETE`；三次 sample 均为 `a40290a41cf0461c6b9ee046b3915754231a7fec5c370babdfdb48f6ff3e93c7` | `68c141770243a059bfc82f12f0692e868b5087f407f1389c805e6f33ce37e6e3` |
| `docs/111-review-attention-pattern-corpus-selection-candidate.md` / narrow | `1ef4f9076872289e629db0e55d99785c7c3024a2041cce861536d722023ead0c` | `CORPUS_PAYLOAD_CANDIDATE`，1 次 | `COMPLETE`；三次 sample 均为 `dd5756f43e1c1f74e7619a691d45102ab1a14a0ff6edf11be26dc32fcfd22e29` | `898cadc0a779536556d6bd4495d0ef294494735308472d3ab83c21edb00406ae` |

两页 requested/final path 都保持同一 exact-SHA 坐标并返回 HTTP 200；固定正文 scope 唯一，response-body
active streams 为 0，`errors / conflicts / cleanup_errors` 均为空。README 读回记录 151 个请求、2 个只读
策略阻断写请求与 8,009,376 delivered bytes；文档 111 记录 142 个请求、2 个阻断写请求与 7,631,825
delivered bytes。策略阻断没有被误写成平台失败。

前三次接受结果汇总脚本分别误读了 scope、`facts_digest` 和 collection 级错误字段的位置，因此没有形成
完整可用报告，也没有被记为产品 `PASS` 或产品失败。修正只发生在临时汇总脚本；第四次从头采集并按
公共 Evidence Schema 读取后得到上表事实，产品代码、合同和验收阈值均未改变。

### 4.2 Manifest 原始字节读回

同一 source commit 的 raw HTTPS 坐标在无 Authorization 的匿名请求中返回 HTTP 200，final URI 未漂移。
下载的 1,085 bytes 与 exact-main 工作树中的 manifest 逐字节相同，SHA-256 为
`ef7f65f7384f39d6afe3f1e44ac0463d8d5a0b85888dfe31ef069f0fbf6eea5d`。公开页面观察与原始字节身份各自
提供不同证据，互不代替。

## 5. 冻结边界

闭环成立后，只有以下新事实成立：

```text
PATTERN_CORPUS_0.1_FROZEN
LEDGER_OPEN
R1_ENTRY_UNBLOCKED
R1_IMPLEMENTATION_NOT_STARTED
```

这表示 R1 的 `P4_AND_PATTERN_CORPUS_FREEZE` 双前置门已经满足，可以从 closure 合入后的新 exact main
单独起草 R1 合同；它不表示 R1 的 SourceSnapshot、关系图、Semantic Review Slice、Schema、源码包、
CLI、CI、标签或 Release 已经设计或实现。Ledger 继续 append-only/open；未选记录不被改成 `REJECTED`，
以后新增 revision 也不改变 Corpus 0.1 身份。

本文不修改 Core、P1–P4、Workbench、Provider、Ledger、manifest、Schema、CLI、CI、标签或 Release。

## 6. 本状态发布的最后门

本补丁只允许本文、README、AGENTS、R 轨 Plan 与里程碑索引变化，并必须独立完成：

1. 原始远端 Public CI 11 个 job 全部成功，不以 rerun 覆盖失败；
2. 通过受保护主线合入；
3. fetch 并确认新的 exact `origin/main`、tree 与 merge parents；
4. 该 exact main 的 Public CI 与 Browser Smoke 均成功；
5. 从该 exact main 用产品 P2 Collector 和 fresh anonymous Chromium 读取 README 与本文；
6. 两页均须保持 exact-SHA URL、HTTP 200、唯一 usable scope、`COMPLETE`、三样本稳定、指定 marker
   存在，且没有 error、conflict 或 cleanup error；
7. 匿名重新下载 source commit 上的 manifest，并再次得到相同字节数与 SHA-256。

任一门失败或出现新反例，状态继续是 `CORPUS_CLOSURE_CANDIDATE / R1_BLOCKED`。只有全部成立，本文的
状态发布目标才成为当前主线事实。后继必须从新的 exact main 单独进入 R1 合同阶段，不得在本闭环中
顺带创建 R1 实现。
