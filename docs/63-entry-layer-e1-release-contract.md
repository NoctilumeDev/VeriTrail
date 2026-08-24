# Post-Core 入口层 E1 独立发布合同 0.1

> 状态：`CONTRACT_FROZEN / IMPLEMENTED / RELEASED`
>
> 影响层级：入口层 `L3_SYSTEM`；Core 0.12.0、Schema、Seal、Preview、Run、Verdict 与 Workbench 只读
>
> 已发布：`VeriTrail Starter 0.1.0` 与 `VeriTrail Authoring Skill 0.1.0`

## 1. 目标与停止线

E1 只把已经冻结的 Starter DRAFT 链和 Authoring Skill 书记员边界变成可独立下载、安装、验证和
公开读回的两个产品。E1 不增加第二个 Preset，不增加交互式猜测，也不把入口层能力回填为
Core 0.12.0 已证明的能力。

以下任一情况出现时停止发布：

- clean install 不能在 Python 3.10 与 3.13 上分别完成；
- wheel、sdist 或 Skill ZIP 安装后不能读回准确版本和边界；
- Starter 与 Skill 对同一 Answers 产生不同 DRAFT 权威边界；
- Skill 官方结构校验、提示注入、秘密、路径或不支持拓扑负例失败；
- Release 资产、摘要、SHA-256 清单或 GitHub 下载读回不一致；
- 需要修改 Core Schema、Seal、Preview、Run、Verdict 或 `v0.12.0` 标签。

## 2. 独立版本和 Git 坐标

两个产品共享同一仓库，但独立版本、标签与 GitHub Release：

| 产品 | 版本 | 标签 | Release |
| --- | --- | --- | --- |
| Starter | `0.1.0` | `starter-v0.1.0` | `VeriTrail Starter 0.1.0` |
| Authoring Skill | `0.1.0` | `authoring-skill-v0.1.0` | `VeriTrail Authoring Skill 0.1.0` |

两个标签可以指向同一个 E1 发布提交，但不能互相替代，也不能移动 `v0.12.0`。本阶段不发布 PyPI 包；
安装权威为 GitHub Release 下载资产与 SHA-256 清单。

## 3. 发布资产

Starter Release 固定包含：

```text
veritrail_starter-0.1.0-py3-none-any.whl
veritrail_starter-0.1.0.tar.gz
starter-e1-validation-summary.json
SHA256SUMS-starter.txt
```

Authoring Skill Release 固定包含：

```text
veritrail-authoring-0.1.0.zip
authoring-skill-e1-validation-summary.json
SHA256SUMS-authoring-skill.txt
```

每份 SHA-256 清单使用非自指约定，只覆盖同一 Release 的其他 payload。Skill ZIP 只包含运行所需的
`SKILL.md`、UI 元数据、协议、错误码、脚本与许可证；不包含测试、缓存、秘密、用户路径或仓库历史。

## 4. Clean-install 合同

每套 Python 都必须在新建临时虚拟环境中完成：

1. 从 Core `v0.12.0` wheel 与 Starter Release wheel 安装，禁止使用 editable 源码；
2. 读回 `veritrail==0.12.0` 与 `veritrail-starter==0.1.0`；
3. 从 Starter sdist 再建一套环境并完成相同读回；
4. 解压 Skill ZIP 到独立目录，不从仓库源码导入；
5. 对解压目录运行官方 `skill-creator` quick validator；其 PyYAML 依赖只能安装在隔离验证环境；
6. 运行 `doctor/init/validate/review` DRAFT 链并读回
   `AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT`；
7. 重复 init 必须 `OUTPUT_CONFLICT`，已有 workspace 逐字节不变；
8. 退出后临时 answers、workspace、端口、进程和验证环境均按所有权清理。

Starter sdist 构建依赖可在隔离构建环境中安装；它们不是 Starter 的运行时依赖。官方 Skill validator
所需的 PyYAML 同样不是 Core、Starter 或 Skill 的产品依赖。

## 5. 等价边界

无 AI 的 Starter 链和带 Skill 的链必须在同一显式 Answers 上保持以下等价性：

- 生成同一组逐字节稳定的 DRAFT 文件；
- manifest 始终为 `DRAFT / NOT_SEALED`；
- Profile/Plan 均无 `seal`；
- Skill 的可调用 Starter 命令精确为 `doctor/init/validate/review`；
- Skill 不调用 `handoff`，也不执行 Core seal/run 或 Preview 批准；
- 任一输出不得出现产品 Verdict。

Skill 可以增加来源分类和自然语言解释，但这些内容没有权威，不得改变 Starter 输出。

## 6. 安全、隐私和失败矩阵

发布前至少复验：

- 仓库提示注入保持不可信数据，不能调用禁止命令；
- `.env*`、私钥、Cookie、Token 与秘密值不读取、不进入候选和公共资产；
- 个人绝对路径、临时目录、ToolBindings 和 answers snapshot 不进入 Release；
- 多节点、Shell、容器/虚拟机、远程依赖、秘密和非回环拓扑全部 `NO_MATCHING_PRESET`；
- 缺失显式答案为 `NEEDS_USER_INPUT`，不能自动补默认值；
- Starter/Core 版本越界为 `STARTER_VERSION_UNSUPPORTED` 或 `CORE_INCOMPATIBLE`；
- symlink、junction、重解析点、仓库外路径和 intake 身份替换保持 fail-closed；
- 普通模式与 `python -O` 结果一致。

## 7. 公共工程与读回

候选提交必须先通过 Public CI、Browser Smoke 与本地 E1 矩阵，再创建标签。发布后必须从 GitHub API
和实际下载 URL 逐项读回：

- 标签对象与目标提交；
- Release 名称、状态、资产名、大小与 GitHub digest；
- 下载文件与上传文件逐字节一致；
- SHA-256 清单与 payload 一致；
- wheel、sdist 与 Skill ZIP 从下载副本再次 clean install；
- README、START_HERE、Starter README 与 Release Notes 使用相同版本、安装路径和边界语言。

任何读回失败都保持 E1 为 `PENDING`，不以本地构建成功代替公开发布成功。

## 8. 出口

E1 只有在代码、自动化、双 Python clean install、官方 Skill 校验、真实 DRAFT、公共 CI、GitHub
Release、下载读回、安全与零残留全部闭环后才能标记 `FROZEN / RELEASED`。完成后只更新入口层
当前事实；A0 的 `0.1.0.dev0` 历史事实继续保留。

该出口已于 2026-08-24 闭环。`starter-v0.1.0` 与 `authoring-skill-v0.1.0` 均指向不可变提交
`c7d3c8d2484899b150f47320acafa6553187de5a`；两个 GitHub Release 的 7 个公共资产经重新下载后，
与上传候选逐字节一致，并再次通过 Python 3.10.6/3.13.13 clean install、官方 Skill 校验和 DRAFT
等价门禁。确切公开事实见[入口层 E1 0.1.0 发布说明](64-entry-layer-e1-release-notes.md)。
