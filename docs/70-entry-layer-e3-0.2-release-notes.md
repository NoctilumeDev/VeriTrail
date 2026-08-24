# VeriTrail 入口层 E3 0.2.0 发布说明

> 状态：`FROZEN / RELEASED / PUBLIC_READBACK_PASS`
>
> 日期：`2026-08-24`
>
> 影响层级：`L2 public contract + bounded L3 release path`

## 1. 发布结论

VeriTrail Starter `0.2.0` 与 VeriTrail Authoring Skill `0.2.0` 已作为两个独立入口产品发布。E3 没有
新增 Preset，只公开 E2 已经实现并验收的两个有限入口：

```text
single-webapp (Answers 0.1)
static-site   (Answers 0.2)
```

两个入口仍只能生成 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`。它们没有获得 Core seal/run、
Preview 批准、断言修改或 Verdict 权限，也没有修改 VeriTrail Core `0.12.0` 的 Schema、Bundle、
Workbench 或裁决语义。

## 2. 冻结坐标

通过门禁的候选提交为：

```text
c9592e1ac8aaf6c88a2b3cb067073c6a1dd6aa72
```

| 产品 | 带注释标签对象 | 标签最终提交 | GitHub Release |
| --- | --- | --- | --- |
| Starter 0.2.0 | `f87442292a705a5932b733b57c7c02318d6215f8` | `c9592e1ac8aaf6c88a2b3cb067073c6a1dd6aa72` | [VeriTrail Starter 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.2.0) |
| Authoring Skill 0.2.0 | `27a6e434797ea630c811ed38ba5f93592890293e` | `c9592e1ac8aaf6c88a2b3cb067073c6a1dd6aa72` | [VeriTrail Authoring Skill 0.2.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.2.0) |

Starter Release 发布于 `2026-08-24T12:37:15Z`，Authoring Skill Release 发布于
`2026-08-24T12:37:19Z`。两者均为非草稿、非预发布、非 Latest；仓库 Latest 继续是
[VeriTrail Core 0.12.0](https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.0)。E1 的
`starter-v0.1.0`、`authoring-skill-v0.1.0` 与原 Release 均保持不可变。

## 3. 固定资产与 SHA-256

### Starter

| 资产 | 字节 | SHA-256 |
| --- | ---: | --- |
| `veritrail_starter-0.2.0-py3-none-any.whl` | 25,685 | `ce6e9ea0730adc891aba97f8148fdb861fffdd5164989c980b5cbbaaa950771f` |
| `veritrail_starter-0.2.0.tar.gz` | 24,910 | `d86b836cad6f5b0bf2fbe17ce3d86fb309fa1fb1f2e592b757ef4b0f5f48188d` |
| `starter-e3-validation-summary.json` | 3,690 | `147ca81269b30eb93e56d4cd42526c9c9aedd26747643d724ad8aaf36c3ca979` |
| `SHA256SUMS-starter.txt` | 305 | `44ab7b1292e6170cad531bad906081b68848241cb36099b25a13f71a3b394791` |

### Authoring Skill

| 资产 | 字节 | SHA-256 |
| --- | ---: | --- |
| `veritrail-authoring-0.2.0.zip` | 17,707 | `591b064d4fb6f7e66083124939c1ffb21daa5a0f2e2c3b51267e738b203640b6` |
| `authoring-skill-e3-validation-summary.json` | 3,810 | `a8cfc0c33fdb2520dbc26b0338acd5d5bb2afcfe5bf18a9b9bb01fcaedccb45a` |
| `SHA256SUMS-authoring-skill.txt` | 205 | `e744512b3f8560f779a70c71ea6b5891554bb14ced6688ea865b2ad2a28a8456` |

两个 SHA-256 清单采用非自指约定。GitHub API 的资产名称、大小和 `sha256:` digest 与上述事实一致；
上传候选、清单和从公开下载 URL 取回的七个普通文件逐字节一致。

## 4. 候选门禁与公开读回

候选提交的 [Public CI](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32727073302) 与
[Browser Smoke](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32727073351) 均为 `success`。
发布资产从 GitHub 重新下载后，又完成以下串行读回：

- Python `3.10.6` 与 `3.13.13`；
- Core `0.12.0` 公共 wheel，SHA-256
  `d0293f06e6a2b0271870ce032b2197c6ef7956db0ff3889230ca48234ff2fa45`；
- Starter wheel 与 sdist clean install、版本和 Answers 0.1/0.2 Schema 读回；
- `single-webapp`、`static-site` 的 direct Starter 与 Skill 两条 DRAFT 链；
- 普通模式与 `python -O` 的事实等价；
- 相同 Answers 的 direct/Skill 草案逐字节一致；
- 官方 `skill-creator/quick_validate.py` 校验为 `PASS`；
- 成功结果继续停在 `AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT`。

公开读回摘要为 `PASS`，`draft_equivalence = BYTE_IDENTICAL`，
`summary_equivalence = BYTE_IDENTICAL_FACTS`。发布构建固定
`SOURCE_DATE_EPOCH = 1787529600`（`2026-08-24T00:00:00Z`）。

## 5. 失败保留与修复

第一次双构建比较暴露了 wheel/sdist 归档时间元数据漂移。该候选没有被发布，也没有把“内容相同”误写成
“逐字节可重复”。发布脚本随后固定构建 epoch，并对 sdist 的成员顺序、mtime、uid/gid、用户名、组名、
pax header 与 gzip header 做确定性归一化；新增的回归测试会主动改变归档时间和所有者元数据，确认第二
次构建仍逐字节一致。修复后的两个完整候选构建及 GitHub 下载副本全部保持相同 digest。

## 6. 明确保留的边界

- `two-process-app`、通用项目探测、Docker Compose、远程数据库、自动安装和跨平台入口未实现；
- AI Skill 不能调用 `handoff`，不能执行 Core 命令，也不能根据失败降低断言；
- Starter 仍只通过 GitHub Release 分发，不发布到 PyPI；
- Codex Security 深度扫描、攻击路径验证和极端环境攻击按既定决定继续封存；本轮普通契约、打包、CI、
  Release 与公开展示检查不冒充这些安全工作流。

## 7. 出口

E3 已满足合同要求的候选提交、双 Python、双 Preset、官方 Skill 校验、两个独立 Release、七个下载
资产、Core Latest 身份、公共展示与公开下载读回，最终状态冻结为：

```text
FROZEN / RELEASED / PUBLIC_READBACK_PASS
```
