# Post-Core 入口层 E3 0.2.0 独立发布合同 0.1

> 状态：`CONTRACT_FROZEN / IMPLEMENTATION_COMPLETE / RELEASED / PUBLIC_READBACK_PASS`
>
> 日期：`2026-08-24`
>
> 影响层级：`L2 public contract + bounded L3 release path`
>
> 只读基线：VeriTrail Core `0.12.0`、Starter/Authoring Skill `0.1.0` Release 与全部既有标签
>
> 完成事实：[VeriTrail 入口层 E3 0.2.0 发布说明](70-entry-layer-e3-0.2-release-notes.md)

## 1. 目标与边界

E3 只把 E2 已经实现并验收的 Starter `0.2.0` 与 Authoring Skill `0.2.0` 变成两个可独立下载、
校验、clean install 和公开读回的正式 Release。发布能力固定为两个有限 Preset：

```text
single-webapp (Answers 0.1)
static-site   (Answers 0.2)
```

E3 不新增 Preset，不实现 `two-process-app`，不修改 Core Schema、Seal、Preview、Run、Verdict 或
Workbench，也不把入口层能力回填成 Core `0.12.0` 已证明事实。Authoring Skill 仍只是一名
`AUTHORING_ASSISTANT`，只能生成 `DRAFT / NOT_SEALED / NOT_RUN / NO_VERDICT`。

## 2. 独立版本、标签与 Release

| 产品 | 版本 | 不可移动标签 | GitHub Release |
| --- | --- | --- | --- |
| VeriTrail Starter | `0.2.0` | `starter-v0.2.0` | `VeriTrail Starter 0.2.0` |
| VeriTrail Authoring Skill | `0.2.0` | `authoring-skill-v0.2.0` | `VeriTrail Authoring Skill 0.2.0` |

两个带注释标签必须指向同一个通过门禁的候选提交。不得移动或删除 Core `v0.12.0`、
`starter-v0.1.0`、`authoring-skill-v0.1.0` 及任一历史里程碑标签。两个 0.2 Release 都不能取代
Core `v0.12.0` 的仓库 Latest 身份。

Starter 继续只通过 GitHub Release 分发，不发布到 PyPI。Skill ZIP 继续作为独立资产分发，不把
仓库测试、缓存、用户答案或本机路径打进包内。

## 3. 固定资产集合

Starter Release 必须精确包含：

```text
veritrail_starter-0.2.0-py3-none-any.whl
veritrail_starter-0.2.0.tar.gz
starter-e3-validation-summary.json
SHA256SUMS-starter.txt
```

Authoring Skill Release 必须精确包含：

```text
veritrail-authoring-0.2.0.zip
authoring-skill-e3-validation-summary.json
SHA256SUMS-authoring-skill.txt
```

SHA-256 清单采用非自指约定，只覆盖同一 Release 的其他三个或两个 payload。候选目录、上传资产、
GitHub digest 与重新下载副本必须逐字节一致。

## 4. 候选提交门禁

创建标签前，候选提交必须满足：

1. 工作树无未跟踪发布残留，`main` 与 `origin/main` 对齐；
2. Public CI 与 Browser Smoke 在该提交上通过；
3. Core 全量回归、Starter/Skill 普通模式和 `python -O` 合同测试通过；
4. wheel、sdist 与 Skill ZIP 从干净临时目录构建，第二次构建的公开 payload 逐字节一致；
5. 官方 `skill-creator/quick_validate.py` 在隔离环境中通过；
6. Python 3.10 与 3.13 均从 Core `v0.12.0` 公共 wheel、Starter 候选资产和解压后的 Skill ZIP
   完成 clean install；
7. `single-webapp` 与 `static-site` 各自完成 direct Starter 与 Skill 两条 DRAFT 链；
8. 相同 Answers 的 direct/Skill 草案逐字节一致，普通/优化模式事实一致；
9. 重复 init、秘密、Shell、非回环、重解析点、远程依赖、构建型静态站点和不支持拓扑继续
   fail-closed；
10. Release 资产、摘要和文档不包含个人绝对路径、ToolBindings、秘密、临时目录或未冻结能力声明。

所有验证默认严格串行，以适配 16 GB Windows 主机；不得以并发压测替代发布正确性。

## 5. 双 Preset clean-install 矩阵

每个 Python 系列至少执行以下矩阵：

| 安装来源 | `single-webapp` | `static-site` | 目的 |
| --- | --- | --- | --- |
| Starter wheel + Skill ZIP | 普通 / `-O` | 普通 / `-O` | 验证最终二进制入口与 Skill 等价性 |
| Starter sdist | 版本与 Schema 读回 | 版本与 Schema 读回 | 验证独立构建和安装合同 |

wheel 环境必须读回 `answers-0.1.schema.json` 与 `answers-0.2.schema.json`；sdist 环境必须读回相同版本、
包元数据和两个 Schema。Skill 只允许调用 `doctor/init/validate/review`，不能调用 `handoff`，也不能
执行 Core 命令。

## 6. 验收摘要合同

两个验证摘要都必须是 UTF-8 JSON 普通文件，并至少记录：

- 产品、版本、Core 版本和公共 Core wheel SHA-256；
- Python 精确版本；
- wheel/sdist 或 Skill ZIP 的精确 digest；
- `single-webapp`、`static-site` 两套普通/优化 DRAFT 等价事实；
- 官方 Skill validator 状态；
- 权限集合与 `NOT_SEALED / NOT_RUN / NO_VERDICT` 停止线。

公开下载读回时，版本系列可以匹配相同 Python 3.10/3.13 系列，但除解释器补丁版本外的验证事实必须
与候选摘要一致。摘要不能只写总计 PASS 而省略 Preset 维度。

## 7. 标签、Release 与公共展示顺序

发布顺序固定为：

```text
候选提交通过本地门禁
  -> 推送候选提交
  -> 等待 Public CI / Browser Smoke
  -> 创建两个带注释标签并推送
  -> 创建两个非 Latest GitHub Release
  -> 上传固定资产
  -> 从公开 URL 重新下载并 clean-install
  -> 确认 Core v0.12.0 仍为 Latest
  -> 更新 README / START_HERE / Starter README / Release Notes
  -> 再次等待公共 CI 并读回 GitHub 展示面
```

发布前的 README 继续把 `0.2.0` 描述为源码候选，避免链接尚不存在的 Release；公共读回成功后，才把
稳定入口切换为 0.2.0。0.1.0 的 Release 页面和安装坐标继续保留，不做静默重写。

## 8. 公共读回

每个 Release 必须从 GitHub API 与实际资产下载 URL 双重核验：

- 标签对象、标签类型与最终提交；
- Release 名称、tag、draft/prerelease/Latest 状态；
- 精确资产集合、普通文件类型、大小与 `sha256:` digest；
- 上传候选、清单与下载副本的 SHA-256；
- 下载副本的双 Python clean install、双 Preset DRAFT 等价和官方 Skill 校验；
- README 徽章、入口表格、安装命令、文档索引、About/Topics 与 Release 正文的一致性。

任一公开读回失败时，E3 保持 `RELEASE_PENDING`；不得用本地构建成功代替公共发布成功，也不得改写
失败记录后直接宣布通过。

## 9. 明确封存的工作

Codex Security 深度扫描、攻击路径验证和极端环境攻击继续封存，等待官方验证链恢复后另立工作流。
E3 可以执行普通代码质量、契约、打包、依赖、文档、CI、Release 与公开展示检查，但不能把这些结果
冒充成已完成的深度安全结论。

## 10. 出口

E3 只有在候选提交、双 Python、双 Preset、官方 Skill 校验、两个 GitHub Release、七个下载资产、
Core Latest 身份、公共展示和最终工作树全部读回一致后，才能标记：

```text
FROZEN / RELEASED / PUBLIC_READBACK_PASS
```

出口事实必须另写发布说明，记录真实提交、标签、CI URL、发布时间、资产 SHA-256 与失败保留；本合同
只冻结门禁，不预先宣称 E3 已完成。
