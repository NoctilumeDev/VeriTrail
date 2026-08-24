# Entry Layer E2 `static-site` Implementation Facts

> 日期：2026-08-24
> 状态：`IMPLEMENTED / NOT_RELEASED`
> 影响层级：`L2 public contract + bounded L3 generation path`

## 1. 结论

E2 已在源码中完成第二个有限 Preset `static-site` 和 Authoring Skill 0.2，但尚未创建 GitHub Release、
发布资产或新标签。已发布的 Starter/Skill 0.1.0 与 Core 0.12.0 坐标没有移动。

新增链仍只产生可人工复核的 DRAFT：

```text
Answers 0.2
  -> Starter doctor / init / validate / review
  -> Profile + Plan + ToolBindings + snapshots
  -> AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT
```

## 2. 实现范围

- Starter 源码开发版本升级为 `0.2.0`；
- 新增严格的 `answers-0.2.schema.json`；
- 保留 Answers 0.1 `single-webapp`，新增 Answers 0.2 `static-site`；
- 固定使用显式 CPython console executable 和
  `-m http.server <port> --bind 127.0.0.1`；
- 新增普通 HTML 身份、Subject 内路径、逐级重解析点、build/remote/Shell/secret/loopback 边界；
- 旧工作区只能由 manifest 中记录的精确 Starter 版本复核；
- Authoring Skill 0.2 只增加有限候选识别和 Answers 0.2 路由，权限集合没有扩大；
- 固定黄金 Subject 位于 `examples/starter/static-site`；
- Public CI 增加 `static-site` Authoring DRAFT 链。

## 3. 自动化事实

| 门禁 | Python 3.10 | Python 3.13 | 结论 |
| --- | ---: | ---: | --- |
| Starter tests，普通模式 | 24/24 | 24/24 | 通过 |
| Starter tests，`python -O` | 24/24 | 24/24 | 通过 |
| Skill tests，普通模式 | 24/24 | 24/24 | 通过 |
| Skill tests，`python -O` | 24/24 | 24/24 | 通过 |
| 全仓 Python tests | 330/330 | 330/330 | 通过 |

源码环境另外完成 8 条真实 Authoring acceptance：两个 Python × 两个 Preset × 普通/优化模式。
每条链均生成 7 个逐字节确定的 DRAFT 文件，并保持权限停止线。

## 4. 打包与 clean-install

成功构建并读取：

- `veritrail-0.12.0-py3-none-any.whl`；
- `veritrail_starter-0.2.0-py3-none-any.whl`；
- `veritrail_starter-0.2.0.tar.gz`；
- `veritrail-authoring-0.2.0.zip`。

Starter wheel 与 sdist 均包含 Answers 0.1 和 0.2 Schema；Skill ZIP 通过官方 `quick_validate.py`，
打包最小性和确定性测试通过。两个 Schema 也通过 JSON Schema 元验证。Starter 的 PEP 639 license
元数据同时把构建后端下限固定为 `setuptools>=77`，避免声明可用的旧后端在直接构建 sdist 时失败。

Python 3.10 与 3.13 的独立临时虚拟环境均从本地 wheel clean-install Core 0.12.0 与 Starter 0.2.0，
成功读回两个 Schema、CLI help 和包版本。第一次真实链在未安装 Playwright 时按合同返回
`NEEDS_INPUT`；显式安装缓存中的 `playwright==1.62.0` 后，从头完成 8/8 clean-installed acceptance。
这个首次停止是 fail-closed 环境证据，不能从记录中删除或改写为首次成功。

## 5. 所有权、兼容性与消费者

- Starter 拥有 Answers 校验、doctor、DRAFT 生成和 workspace 复核；
- Authoring Skill 拥有有限候选与显式字段收集，只消费 Starter 的公开命令合同；
- Core 只在未来人工 handoff 后消费 Profile/Plan，不消费候选推断；
- 已发布 0.1.0 用户继续使用原标签与资产；源码 0.2.0 不形成公开安装承诺；
- Core Schema、Seal、Preview 批准、Run、Verdict、Workbench 和既有 Release 均未修改。

## 6. 未证明与后继门禁

E2 没有证明构建型前端、远程资源、包管理器、Docker、C2/C3、多服务、跨平台、恶意项目隔离或
自动环境修复。`two-process-app` 也未实现。

当前没有发布 Starter/Skill 0.2。若进入发布阶段，必须另立 Release 合同，重做版本资产、双 Python
clean-install、公共下载读回、GitHub 展示面和标签停止线，不能把本地源码验收直接当作 Release 事实。

Codex Security 深度扫描、攻击路径验证和极端环境攻击继续封存，待官方验证链恢复后另行执行；本轮只做
普通代码质量、契约、打包、测试和文档一致性审查。
