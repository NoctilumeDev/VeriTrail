# R1 negative-world Coverage authority recovery 合同独立冻结发布

日期：2026-10-28

> 条件化状态目标：`R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_FROZEN`。
> 本文自己的最后门全部闭合以前，该目标不是生效事实。
>
> 发布基线：`main@a170489cf3adc59679b62da16c1d4aa9c2ae431c`；tree
> `6c2859f8758bf6e05a2fc461ea63dcd9b9585cc3`。
>
> 上游：[exact-input 后继审计](331-r1-negative-world-coverage-authority-recovery-after-exact-input-audit.md)、
> [0.1 合同候选](332-r1-negative-world-coverage-authority-recovery-contract.md)。
>
> 影响层级：`L0_DOCUMENTATION / STATUS_PUBLICATION_ONLY`。

## 1. 本次发布的有限事实

本文只条件化发布文档332已经取得资格的合同字节。冻结对象是一个private、same-attempt、one-shot的negative-world Coverage
authority-recovery seam：producer只构造CoverageLedger 0.3 candidate；independent validator必须从original 0.2 carrier重新枚举完整
Snapshot/Policy/Language/Parse/Fact denominator、branch-specific absent roots和stage history，再用自己构造的conformance source调用既有
0.3 validation；admission最后绑定同一live carrier/context/result并exactly once commit。

发布基线中该合同的精确状态是`QUALIFIED_CONTRACT_CANDIDATE / NOT_FROZEN`；本文自己的资格链闭合以前不得把该状态提前升级。

这不是runtime实现，也不新增CoverageLedger版本、Schema、reason、positive composition、manifest、Evidence、persistence、public Review、
CLI、Workbench、tag或Release。本文尤其不把producer/validator的agreement升级为original-input completeness，也不恢复旧composition
authorization为可消费authority。

## 2. Contract candidate exact qualification

```text
PR                   = #383
base                 = 348b3bdcbf8b459d52f17d2091cb1bb00a60197d
head                 = 434e7d15d5b43a7dd950e5ce0d0ff865c17fa7ac
ordinary merge       = a170489cf3adc59679b62da16c1d4aa9c2ae431c
candidate/merge tree = 6c2859f8758bf6e05a2fc461ea63dcd9b9585cc3
diff                 = 1 commit / 4 files
```

[PR #383](https://github.com/NoctilumeDev/VeriTrail/pull/383)的original Public CI
[40667909542](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40667909542) attempt 1为11/11 SUCCESS。
exact-main Public CI [40671677582](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40671677582) attempt 1为
11/11 SUCCESS；Browser Smoke [40671677399](https://github.com/NoctilumeDev/VeriTrail/actions/runs/40671677399)
attempt 1为1/1 SUCCESS。merge parents精确为上述base/head，merge tree等于candidate tree。

合同read-only audit的baseline canonical SHA-256为：

```text
ed0450c8a63a2c99222d996d6832cbf8f14dea82e5022c0ef6cb2bcbe4a9a903
```

candidate publication audit四格canonical SHA-256一致为：

```text
d130923dcf84d310da73ceb6bd7c25992bb077d31ddb20773d7231c1b32acd5a
```

focused matrix四格各139 tests / 138 passed / 1 skipped。local qualification、95-artifact pre-PR index、original PR
qualification、protected merge与candidate exact-main gate records的SHA-256分别为：

```text
7e3be2f3f8296da39be7eaa2557ea5121ce7721f9774bf54d2424857d29c46a8
18da23bba2d20136e0bc3e8d74baf3e14091d08bc6ab04a7a56fbd21b2c4f2e9
b05cf31e6bc8e96df61bfc8c05b1ad34fc969675582042f2e2683306a132457d
182ef4e7c62314eba7856dfe5833405ca13b2e544a85fddce37b4253267d3fd5
90b1a4e9f1deb45fa7e5f70d6dc481bbd6d8f30492739bbd59542d70916143a6
```

## 3. Candidate fresh installed-product readback

在detached exact `main@a170489…`建立fresh CPython 3.13 venv，安装冻结Core 0.13.0、GitHub Evidence 0.1.0、
Playwright 1.62.0与matching Chromium。公开wheel只复用重新校验的既有Release字节；匿名产品观察清空token、`PYTHONPATH`与
`PYTHONHOME`，代理只按命令注入。

| Target | Plan ID | Session | Report SHA-256 |
| --- | --- | --- | --- |
| README | `r1-nwcr-contract-formal-readme-1-a170489` | `github-paired-ad4f3bdfaf934df88df430a32625e821` | `4e22ff7301c6aafdda01186b6f619aefa856d9ded01818ce5986509f055e6ead` |
| doc331 | `r1-nwcr-contract-formal-doc331-1-a170489` | `github-paired-f6e2b23d99e14481ba509417d4882823` | `81a519acb282bdb68eb40b469f7c23801ecf4dd4bf8fd276b2d4872688e3066a` |
| doc332 | `r1-nwcr-contract-formal-doc332-1-a170489` | `github-paired-1dacf5b0e17047ebbf4ee1ae1bf6f7eb` | `0f4f12171a73761058181c53b8518047acf5819c90fb7c3d85061619806bbf95` |
| milestones | `r1-nwcr-contract-formal-milestones-1-a170489` | `github-paired-6265075afdd0474c9bd888311d9a761c` | `e37bf7214654db09cd64629d02dcd5c4da21274743374ad69c7759eac921748f` |

四者均为exact-SHA HTTP 200、P1/P2 COMPLETE、Core PASS、稳定marker、零conflict/coverage reason/cleanup error/active
stream。独立evaluator从原sealed Plan、handoff与Evidence重算Core并逐项等于producer report；四份public raw bytes逐字节等于
同一exact main的Git blobs。

independent reconciliation与171-artifact finite closeout的SHA-256为：

```text
e171b185d5d692cee8170c6b88a1ad6113144db44e87b91d0e3a1d4f2d3a2754
3c660100e363a67055101316cdbf983c6f66945e5f89205b9092e67b67876fca
```

closeout stdout self-capture mismatch与finite integrity的SHA-256分别为：

```text
e7be89c7e85431bb08a5528116c097d6e593b6e98b7c774cc1a1af430f3ab056
ef6e59d010f3ecb538f0b9bb7c92e23588f3e538d5d5bb11cf6a2725f5a44457
```

其余170项逐项终态一致；self-capture只涉及wrapper在enumeration前打开的closeout stdout，semantic effect与qualification
effect均为`NONE`，closeout字节保持不变。

## 4. 保留失败与认识论上限

以下事实继续按原identity保留，later PASS不解释或删除它们：

- contract prequalification audit facility曾把required-provider expected数误记成completed数；修正后的四格才取得资格；
- detached readback首次因本地尚未fetch merge object而失败，以及Windows `rg` positional glob setup error；
- adapter freeze attempt 1错误地把预先初始化的空formal history当成已有formal observation；attempt 2只修proof facility判断；
- rate diagnostic #1与anonymous preflight #1真实观察到remaining 0 / HTTP 403；北京时间19:21:55真实reset以后，diagnostic/preflight
  #2才观察到额度恢复；
- 四个render diagnostic均为非资格观察；171-artifact closeout stdout self-capture mismatch继续独立保留；
- doc331上游181-artifact closeout、180项稳定复算及其self-capture mismatch继续保持原资格边界。

本结果只证明固定合同字节与声明的公开观察取得资格。它不证明runtime已经存在，也不证明将来的producer与validator实现已经真正
避免common-mode failure；这些仍必须由后继implementation falsifier与独立资格链证明。

## 5. 本publication自己的最后门

本docs-only patch只允许修改`README.md`、`AGENTS.md`、`docs/milestones.md`并新增本文。doc331–332、runtime、tests、
workflows、CoverageLedger 0.3、positive composition与全部历史合同必须保持base bytes。

本层local gates只重核publication自己的docs边界：exact four-file scope、relative links、UTF-8 without BOM、LF/final LF、balanced
fences、unique headings、条件marker、doc332与candidate reconciliation/closeout/failure-history continuity、`git diff --check`及read-only
global/local hygiene。runtime full matrix属于已资格化contract candidate的witness；publication不重新解释它。Public CI仍执行自己的完整门。

```text
publication final bytes / declared local gates
    -> original publication PR gates
    -> exact-head protected merge
    -> new exact-main Public CI 11/11 + Browser Smoke 1/1
    -> fresh anonymous installed-product README / doc332 / 本文 / milestones readback
    -> independent Core / source-byte / Bundle / identity / candidate-history reconciliation
    -> target CONTRACT_FROZEN becomes effective
    -> return CONTROL LOOP
```

本门闭合前，branch中的`FROZEN`只是条件target。candidate readback不能替代本publication的fresh Plan/session/Evidence；diagnostic不
计入资格，所有formal non-success必须保留原identity，N从history机械导出。本地checkout alignment与cleanup只属于housekeeping。

## 6. 生效后的停止线

最后门闭合后，本文最多让negative-world Coverage authority recovery合同成为`FROZEN`。随后必须从新的exact main返回
CONTROL LOOP，重新审计bounded private implementation feasibility与common-mode falsifier可构造性；合同冻结不自动授予runtime
implementation authority。

本文不授权Coverage producer、旧positive composition consumption、manifest successor、Evidence continuity、persistence、public
Review、post-R1 Benchmark、R2–R6、tag或Release，也不把private negative-world Coverage扩张成repository truth、semantic、bug或全仓
审查完整性。

## 7. 当前publication target

本文进入仓库不等于冻结生效。在本发布自己的完整资格链闭合以前，只能记录：

```text
R1_FACT_TO_COVERAGE_HANDOFF_EXACT_INPUT_SUCCESSOR_PRIVATE_IMPLEMENTATION_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_AFTER_EXACT_INPUT_AUDITED_INPUT_AVAILABLE_PRODUCER_ABSENT
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_QUALIFIED_CANDIDATE_NOT_FROZEN
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_CONTRACT_FREEZE_PUBLICATION_CANDIDATE
R1_NEGATIVE_WORLD_COVERAGE_AUTHORITY_RECOVERY_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_REVIEW_SLICE_SET_COVERAGE_COMPOSITION_AUTHORITY_HISTORY_PRESERVED_NOT_CONSUMABLE
R1_REVIEW_DERIVATION_MANIFEST_NEGATIVE_WORLD_SUCCESSOR_IMPLEMENTATION_NOT_STARTED_NOT_AUTHORIZED
R1_SAME_ATTEMPT_DERIVATION_EVIDENCE_CONTINUITY_NOT_STARTED_NOT_AUTHORIZED
R1_LANGUAGE_SUPPORT_QUALIFICATION_PERSISTENCE_OPEN
R1_PUBLIC_REVIEW_PRODUCT_NOT_STARTED
R2_R6_NOT_STARTED
```

最后门闭合以后，本文开头的`CONTRACT_FROZEN` target才成为事实；随后只允许返回CONTROL LOOP。
