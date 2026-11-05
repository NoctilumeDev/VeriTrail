# Release download multi-asset lane budget correction

日期：2026-11-05

> 候选状态：`RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_CANDIDATE_NOT_QUALIFIED`。
>
> 构造坐标：`main@95add9053c2984c0efe0cb87d1a4b64812215683`，tree
> `3619ceeba79145ebfe3af230e4ba22c89798c306`。
>
> 影响：`L1_COMPONENT_INTERNAL + L3_QUALIFICATION_BOUNDARY`。本修正只调整两个被真实反例击中的
> multi-asset Public CI lane 的显式可用性恢复预算；不修改下载器默认预算、重试错误集合、摘要校验、
> 不覆盖发布、owned partial 清理、产品 runtime、Schema、Provider、Collector、Core evaluator、Verdict、
> R1 frozen semantics 或任何 Release/tag/asset identity。

## 1. CONTROL LOOP 输入：两个独立 original-gate 失败

PR #407 与 PR #408 都从同一个未变化的 exact main 建立，但拥有不同 candidate head、不同 job、不同资产和不同
original Public CI attempt。两者都已关闭且未合并，没有 rerun：

| identity | PR #407 | PR #408 |
| --- | --- | --- |
| candidate head | `ade665c3b4e760a57c2d2de4fb1c92fcd21d1b98` | `3409a0a5136d4578762a9a8c68b4bede2d73d52b` |
| candidate tree | `66dad764b58927a29e0d7e3aeafb6f237f165510` | `c0893954c5ecb77221037eb25cb1ff3d67afa9ca` |
| original run | `42037283423` / attempt 1 | `42045973076` / attempt 1 |
| failed job | Python 3.10 `127278597232` | E3 0.2 `127308876973` |
| failed asset | `authoring-skill-e1-validation-summary.json` | `veritrail_starter-0.2.0-py3-none-any.whl` |
| asset position | E1 multi-asset list position 6 | first E3 asset after the Core wheel |
| conclusion | `FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED` | `FAILURE / CLOSED / UNMERGED / NOT_QUALIFIED` |

两条失败时间线都先得到一次约 11 秒的 HTTP 504，随后在同一个进程内按 `2 / 4 / 8 / 16 / 16` 秒退避；
第 2 至第 6 次 HTTP 504 很快返回。第 6 次 504 后，60 秒绝对预算已经不足以再支付 16 秒 capped backoff，
下载器以相同的 fail-closed 原因停止：

```text
release asset recovery budget cannot fund the next bounded retry
after retryable_http status=504
```

这不是[文档118](118-release-download-recovery-deadline-correction.md)已经修正的“退避表隐式拥有尝试上限”缺陷。
当前实现确实继续到绝对 deadline 成为停止所有者，也没有接受错误字节或留下 owned partial。

保留证据的 failure-boundary / failed closeout / finite integrity SHA-256 分别为：

```text
PR #407
48c43a66843c6fdf010650b186c6b82e3773a79fe641e2b59cbb2aaf3cf3323e
c01e86ea670dc0a2d0de9bdfb1c7d2145fe8c0185c7590f595d6198baa7ef896
b010e77087f24330a168e48023b3708005bd163503bdb29d701ef8696bb5607c

PR #408
032318a3eccfffd880943c31c9bda2ac4a6f87fe34883f492e4b6a14e0d4ada6
3114367067545beb3a9b9f2710e74c25d2587d884e742c75c3faaf475a29bcd8
0618adba88a223c04061e398cd1a3dacf9612fb0ba817c94b7c266ae5b105dda
```

同一 run 的其他成功 job 只能作为各自 attempt 的上下文，不与失败 job 拼接。PR #408 的 Python 3.10 E1 lane
成功也不能回填 PR #407，或证明特定资产是根因。

## 2. 归层与归因上限

当前证据只允许：

```text
classification = RELEASE_ASSET_HTTP_504_RECOVERY_BUDGET_EXHAUSTED
download tool fail-closed behavior = CONFORMING
target publication semantic regression = NOT_ESTABLISHED
workflow/runtime/test/oracle drift in failed candidates = NOT_ESTABLISHED
asset digest mismatch = NOT_OBSERVED
underlying GitHub/proxy/shared-egress/network cause = UNKNOWN
current 60-second window sufficient for these two observations = REFUTED
```

两次失败不证明 120 秒一定能覆盖未来任意外部中断，也不授权无限重试、retry-until-PASS、替换不可变资产坐标、
跳过 Release download acceptance 或把网络失败改名为产品 PASS。它们只击穿两个 multi-asset lane 对 60 秒默认值的
继续使用责任。

## 3. 最小 versioned 修正

下载器公共状态机和默认值保持不变：

```text
DEFAULT_RETRY_BUDGET_SECONDS = 60
DEFAULT_REQUEST_TIMEOUT_SECONDS = 15
DEFAULT_BACKOFF_SECONDS = 2 / 4 / 8 / 16 capped
retryable HTTP set = 408 / 429 / 500 / 502 / 503 / 504
```

只有两个被反例击中的 workflow block 显式传入：

```text
Download the frozen E1 entry-layer release assets
Download and verify the frozen Core and E3 release assets (E3 asset loop only)

--retry-budget-seconds 120
```

Core wheel 单项下载、Starter golden path 和其他 lane 继续使用默认 60 秒。Python required lane 的 35 分钟 containment
budget与E3 job的15分钟 containment budget都不改变。PR #407 的失败 job 在60秒下载失败时总历时32.27分钟；
成功 world 中 E1 clean-install acceptance 用时26秒。新增窗口只多出最多60秒，仍位于既有35分钟外层停止线内，
不把#404的历史 cancellation 或其 `UNKNOWN` duration variance重新解释为预算授权。

因此：

```text
lane-specific availability recovery window
!=
integrity relaxation
!=
outer containment expansion
```

## 4. 确定性 witness 与反例

定向测试必须证明：

1. 默认预算仍精确等于60秒；
2. 模拟首个504消费11秒、后五个504各消费0.2秒时，60秒窗口不能继续，而显式120秒 lane窗口可以完成
   `2 / 4 / 8 / 16 / 16 / 16`退避并在第7次尝试发布精确字节；
3. workflow中 `--retry-budget-seconds 120` 精确出现两次，且只属于E1/E3 multi-asset block；
4. 既有404、证书失败、摘要不一致、目标已存在、deadline后成功、partial清理与不覆盖反例继续成立；
5. Python 3.10.6 / 3.13.13 × normal/`-O`、Core、Starter、Authoring、GitHub Evidence、Review Attention、
   Workbench 与完整 Public CI 保持原声明门。

测试只作 witness。原始远端门若没有实际收到504，不能把本地脚本化恢复成功冒充成一次真实外部故障恢复；它只能证明
新exact workflow在当次公开环境下完成全部门。

## 5. 精确 scope 与禁止事项

本候选只允许：

```text
.github/workflows/ci.yml
tests/test_release_asset_download.py
README.md
AGENTS.md
docs/357-release-download-multi-asset-lane-budget-correction.md
docs/milestones.md
```

禁止：

```text
修改 scripts/download_release_asset.py 的默认值或错误分类
修改 immutable Release URL、asset name 或 frozen SHA-256
把 403/404、证书错误、digest mismatch 加入可重试集合
跳过 E1/E3 public-download or clean-install acceptance
扩张 35/15 分钟 workflow containment budget
重跑 #407/#408 或复用其失败候选
把同一 run 的成功 job 与失败 job 拼成 qualification
删除、覆盖或重命名任何 retained failure/setup/UNKNOWN identity
修改 primary audit.json
从本修正直接恢复 doc354/doc355/doc356 或启动 R2-R6
```

## 6. 本候选资格链

final bytes 至少通过下载状态机定向测试、workflow exact-placement witness、Python 3.10.6 / 3.13.13 ×
normal/`-O`、该层声明的完整回归、`git diff --check`、global/local hygiene、Markdown与primary audit continuity。

```text
final six-file maintenance bytes / declared local gates
    -> original PR required gates (attempt 1; no rerun laundering)
    -> protected exact-head merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc357 / milestones readback
    -> independent reconciliation + finite closeout
    -> RELEASE_DOWNLOAD_MULTI_ASSET_LANE_RECOVERY_0_2_FROZEN
    -> return CONTROL LOOP
```

任一 non-success 保留原身份并停止。候选自己的远端门、合入、exact-main门与readback全部闭合以前，状态保持
`CANDIDATE_NOT_QUALIFIED`；不得因本地测试或相同workflow文本提前宣称修正生效。

## 7. 后继停止线

本修正合格后只恢复“从新的 exact main 重建失败的docs-only审计”的资格。PR #407/#408 与其candidate head继续保持
关闭、未合并、未资格化；后继必须从新base重新构造，不得 cherry-pick 或复用 doc355/doc356 candidate qualification。
新事实形成后必须返回 CONTROL LOOP，再判断是联合发布两条original-gate failure boundary，还是进一步重开更小边界。

R1 public project-state projection、doc354后继、review derivation manifest、same-attempt continuity、language-support
qualification persistence、public Review与R2-R6都不因本修正自动获得施工权。
