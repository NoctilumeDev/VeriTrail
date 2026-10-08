# VeriTrail 仓库遗留物收口门禁

> 本门禁属于仓库 closeout hygiene。它不定义产品语义，不授予冻结状态，也不替代
> [证据反馈工作法](working-method.md)中的 CONTROL LOOP 与 QUALIFICATION PIPELINE。

## 1. 目的与时机

项目施工阶段可以产生临时构建物、运行目录、截图和诊断输出；重要 milestone 或 release 退出以前，必须判断
哪些对象仍承担职责，哪些已经成为可回收残留。

推荐顺序是：

```text
implementation
  -> declared tests / qualification
  -> documentation and public readback where required
  -> Residual Hygiene Gate
  -> milestone / release closeout
```

门禁不以仓库大小为 KPI。大文件可以有合法 owner，小文件也可能完全没有保留资格。

## 2. 分类规则

| 分类 | 判定 |
| --- | --- |
| `KEEP` | 仍有 active consumer、proof obligation、provenance responsibility 或唯一 local state |
| `DELETE_CANDIDATE` | 没有上述 owner，能够从 authoritative source 重建，且删除不改变当前事实 |
| `ARCHIVE_OR_EXTERNALIZE` | 确有历史或发行责任，但不应继续由当前工作树承担；必须先指定新 owner |
| `REVIEW_REQUIRED` | owner、consumer、唯一状态或证据身份尚未查清，禁止自动删除 |

核心不变量是：

```text
historical existence != retention authority
unreferenced now       != ownerless
rebuildable artifact   != release evidence
same bytes             != same proof identity
```

## 3. VeriTrail 的明确保留责任

以下对象不能因“旧”“大”“看起来未引用”被清理：

- R1 合同、问题审计、首败、资格记录、fixtures、Schema 与 installed-product readback identity；它们承担
  proof / provenance responsibility；
- `docs/design-references/m12/`；其内容由 M12 视觉参考合同绑定，仍是设计 authority；
- README 和当前架构文档消费的 `docs/assets/`；
- Workbench 消费的 `web/public/fixtures/` 与 `web/public/textures/`；
- 已发布 tag、Release asset 及其冻结记录；
- 含未提交、未跟踪、ignored-only 唯一状态，或仍保存正式 observation / failure identity 的 worktree。

当前未能证明 owner 的图片、证据目录或 worktree 一律是 `REVIEW_REQUIRED`，不是删除候选。

## 4. 默认删除候选

在确认没有唯一 local state 后，下列对象通常属于 `DELETE_CANDIDATE`：

- `dist/`、`build/`、`web/dist/`、临时 wheel/sdist 副本；
- `node_modules/`、Python virtualenv、解释器和工具 cache；
- `.veritrail/`、`runs/`、`artifacts/` 中未被正式 evidence identity 拥有的本地运行输出；
- Playwright、coverage、日志、临时数据库和一次性诊断输出；
- 只有像素调整过程价值、没有页面 consumer 或 proof responsibility 的中间截图。

自动门禁只报告，不删除。Git diff 已经记录 tracked 删除，无需再生成截图、逐文件摘要或永久 cleanup ledger 来
证明清理发生过。

## 5. 自动检查与人工责任

默认只读检查：

```powershell
python -B scripts/check_hygiene.py
```

阶段退出时再检查已知本地残留：

```powershell
python -B scripts/check_hygiene.py --local
```

自动检查覆盖：

- tracked/unignored surface 中已知的构建、运行、secret 与临时残留；
- README、START_HERE、CONTRIBUTING、AGENTS、本工作法与本门禁的本地链接。

人工检查仍然拥有：

- 图片是否仍有语义 consumer；
- evidence、fixture、Schema 与失败历史是否仍承担证明责任；
- worktree、容器、volume、服务或外部目录是否含唯一状态；
- Release owner 是否已经接管应外置的发行物；
- 当前 checkout 是否有资格声明 `LOCAL_DORMANT`。

`--local` 没发现已知残留也不自动产生 `LOCAL_DORMANT`。只有人工证明源码、锁文件、迁移、运行脚本与必要
证据都已由远端或指定 owner 保存，并确认没有唯一 local state 后，才能作出该声明。

## 6. 当前仓库审计边界

在建立本门禁的 exact source world 中，tracked surface 没有发现已知 transient residue；主要图片集合均有当前
consumer 或冻结的 provenance owner。因此本轮不删除 R1 proof、M12 参考图、Workbench fixtures/textures 或
历史 worktree。

本结论只覆盖当前 tracked surface 与显式检查过的已知路径。其他 worktree、外部 service、容器、volume 与
用户目录保持 `REVIEW_REQUIRED`，不得据此声明整个主机已经 dormant。
