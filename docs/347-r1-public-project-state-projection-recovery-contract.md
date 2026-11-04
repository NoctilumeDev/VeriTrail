# R1 公开项目状态投影恢复合同候选

日期：2026-11-05

> 状态：`R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_CONTRACT_CANDIDATE / NOT_QUALIFIED / NOT_FROZEN`。
>
> exact base：`main@6a30957429c7b6a815608e8355893deb35873f24`，tree
> `81790b398fb3d07ed53d67269b80d99d94675807`。
>
> 影响：`PUBLIC_PROJECT_STATE_PROJECTION_AND_READBACK_TARGET_BOUNDARY_ONLY`。本文不修改 P2 Collector、
> 512 KiB Render oracle、private runtime、tests、workflow、Schema、Verdict 或 frozen semantic contract。

## 1. 触发事实与失败保留

PR #398 candidate `base=aa0cd335a98269dcdb843645f9643c0e7982a5c8 / head=c1952d76f82808d2c9c7ccca719d32db20364000 /
tree=81790b398fb3d07ed53d67269b80d99d94675807` 已受保护合入本合同 exact base。original Public CI
`41893051274`、exact-main Public CI `41898679833` 与 Browser Smoke `41898679711` 均为 attempt 1 SUCCESS，
分别为 11/11、11/11 与 1/1。

fresh anonymous installed-product README、doc345、doc346 formal readback 各取得唯一 PASS。随后 milestones 首次且唯一
diagnostic `r1-ptds-impl-diagnostic-milestones-1-6a30957` 在 HTTP 200、marker occurrence 1、cleanup complete 的同时观察到
526260 UTF-8 bytes，超过冻结 524288-byte 上限 1972 bytes，正确返回 `PARTIAL / CONTENT_TRUNCATED`。milestones formal
因此没有运行；同一 exact world 的 readback qualification 失败并以 152-artifact closeout
`1b3c3a64bace28e5eab3bb2e6674823ed4f5edaf9adc1c5943b8e90d118a91ff` 封存。

独立 exact-base control diagnostic 在 `aa0cd335a98269dcdb843645f9643c0e7982a5c8` 上为 `COMPLETE`。失败边界只建立：

```text
collector behavior against frozen P2 contract: CONFORMING
collector regression: NOT_ESTABLISHED
private runtime semantic regression: NOT_ESTABLISHED
public projection capacity boundary crossing: ESTABLISHED
underlying cause: KNOWN_FIXED_512_KIB_RENDERED_TEXT_BOUND
```

后继不得 rerun 该 diagnostic、补跑 milestones formal、提高上限、删除三项 PASS、把后继 PASS 回填 #398，或把完整账本改短来
制造 `COMPLETE`。

## 2. 最小 reopen：展示投影，不是历史或裁决权威

`docs/milestones.md` 同时承担完整 append-only 历史、失败 provenance 与链接索引责任。它的 exact-base bytes 为 565121，
SHA-256 为：

```text
5c16f46bcd407cd8932a1233c25afe306288f916e04a41c6cf7dcfae77a6c926
```

该文件必须保持原字节；本合同不把 Render 容量变成历史删除授权。新增
[当前项目状态公开投影](project-state.md)只提供有界 current-state 阅读面，并以 frozen projection contract version、
source exact base/tree 与完整 milestones SHA 机械绑定。它没有新语义，也不成为 scheduler。

责任划分固定为：

| 对象 | 拥有 | 不拥有 |
| --- | --- | --- |
| `docs/milestones.md` | 完整 append-only 工程历史与 provenance | 必须落入 Public Render 512 KiB window 的义务 |
| `docs/project-state.md` | 有界 current-state 公开阅读投影 | 历史事实、资格、状态升级或施工授权 |
| GitHub Contents/raw observation | exact-main 完整文件 bytes 与 SHA observation | rendered semantic completeness |
| P2 Public Render Collector | 冻结上限内的匿名页面观察与显式 truncation | 提高上限或把 PARTIAL 冒充 COMPLETE |
| independent reconciliation | exact main、raw bytes、投影记录与 formal readback 的机械一致性 | 创造缺失事实或覆盖失败 |

## 3. `R1_PROJECT_STATE_PUBLIC_PROJECTION_0_1`

首个 versioned contract 固定：

1. `docs/project-state.md` 必须小于 64 KiB UTF-8，且不得嵌入完整 milestones 内容；
2. 它必须记录唯一 `source_milestones_sha256`、source exact base/tree、候选状态、当前有效事实、保留失败与停止线；
3. README/AGENTS 可以把它作为当前状态的短入口，但必须同时链接完整 milestones，并明确它不是 authority；
4. `docs/milestones.md` 在本候选中必须 byte-for-byte 等于 exact base；
5. qualification 时，README、投影、本文各自先做 fresh diagnostic，再各运行唯一一次 formal；每项必须
   `COMPLETE / FORMAL_READBACK_PASS`；
6. qualification 还必须通过匿名 public raw/API 读取 exact-main `docs/milestones.md` 全字节，并验证其 SHA 与投影记录一致；
7. independent reconciliation 必须同时核对 candidate base/head/tree、protected merge、新 exact-main gates、三项 formal
   identity、完整 milestones public bytes SHA、projection source binding 与 primary audit continuity；
8. 任一 non-success 保留原 identity 并停止，不得用另一个 target、world、attempt 或相同 semantic result 替代；
9. 每次完整 milestones bytes 或 current effective state 改变，投影必须在独立 publication 中更新 source SHA 与状态；旧投影保留为
   其 exact world 的历史，不静默追写；
10. 本合同只 version bump 被击穿的 public projection/readback target boundary，不重开 P2、R1 runtime 或 frozen upstream。

## 4. 本候选的资格链

tracked scope 只能是：

```text
README.md
AGENTS.md
docs/project-state.md
docs/347-r1-public-project-state-projection-recovery-contract.md
```

`docs/milestones.md` 必须保持 exact-base SHA。最终字节必须完成：

```text
exact scope / milestones byte continuity / links / markdown / global+local hygiene
    -> original PR required gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / project-state / doc347 formal readback
    -> full milestones public raw bytes + SHA binding
    -> independent reconciliation + finite closeout
```

全部成立后，本文最多升级为：

```text
R1_PUBLIC_PROJECT_STATE_PROJECTION_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_PROJECT_STATE_PUBLIC_PROJECTION_0_1_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_POST_TERMINAL_FACT_DUAL_SUCCESSOR_PRIVATE_IMPLEMENTATION_MERGED_EXACT_MAIN_GATES_PASS_READBACK_NOT_QUALIFIED_NOT_FROZEN
```

## 5. 停止线

合同冻结必须由后继独立 docs-only publication取得自己的完整资格链。在那以前：

- 本投影不能替代当前 frozen qualification target；
- PR #398 不得升级为 `READBACK_QUALIFIED` 或 `FROZEN`；
- 不得建立 implementation freeze publication；
- 不得恢复 global composition authority；
- 不得启动 manifest、Evidence、persistence、public Review 或 R2–R6。

本文形成任何新事实以后必须返回 CONTROL LOOP。只有新的 exact main 仍支持同一最小边界，才允许建立独立 freeze publication；
文档编号与绿色 CI 都不是调度器。
