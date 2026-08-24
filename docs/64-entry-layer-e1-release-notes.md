# VeriTrail 入口层 E1 0.1.0 发布说明

> 状态：`RELEASED / PUBLIC_READBACK_PASS`
>
> 产品：`VeriTrail Starter 0.1.0`、`VeriTrail Authoring Skill 0.1.0`
>
> Core：继续使用冻结的 `VeriTrail Core 0.12.0`

## 1. 这次发布解决什么

E1 把已经完成源码冻结的两个入口产品变成可独立下载、校验和 clean install 的正式发布：

- Starter 把显式 Answers 转换成确定性的 `DRAFT / NOT_SEALED` workspace；
- Authoring Skill 只做仓库只读盘点、有限 Preset 匹配、缺失信息追问和 Starter 调用；
- 有 Skill 与无 Skill 的路径对同一 Answers 必须生成逐字节相同的 DRAFT；
- 两个产品分别版本化和发布，不移动 Core `v0.12.0`，也不扩大 Core 的能力声明。

E1 仍只支持 Windows 11 上的 `single-webapp` 预设。多服务、远程依赖、容器、Shell、秘密和无法确定
进程所有权的拓扑继续 fail-closed。

## 2. 固定发布坐标

| 产品 | 标签 | GitHub Release | 资产数 |
| --- | --- | --- | ---: |
| Starter | `starter-v0.1.0` | [`VeriTrail Starter 0.1.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/starter-v0.1.0) | 4 |
| Authoring Skill | `authoring-skill-v0.1.0` | [`VeriTrail Authoring Skill 0.1.0`](https://github.com/NoctilumeDev/VeriTrail/releases/tag/authoring-skill-v0.1.0) | 3 |

Starter 资产：

```text
veritrail_starter-0.1.0-py3-none-any.whl
veritrail_starter-0.1.0.tar.gz
starter-e1-validation-summary.json
SHA256SUMS-starter.txt
```

Authoring Skill 资产：

```text
veritrail-authoring-0.1.0.zip
authoring-skill-e1-validation-summary.json
SHA256SUMS-authoring-skill.txt
```

两个带注释标签均解析到提交 `c7d3c8d2484899b150f47320acafa6553187de5a`，没有移动 Core
`v0.12.0`。Starter 发布于 `2026-08-24T01:42:51Z`，Authoring Skill 发布于
`2026-08-24T01:42:55Z`；均不是草稿或预发布。

## 3. Starter 安装与边界

Starter 不发布到 PyPI。先校验同一 Release 的 SHA-256 清单，再在干净虚拟环境中安装 Core 与 Starter
Release wheel：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install `
  https://github.com/NoctilumeDev/VeriTrail/releases/download/v0.12.0/veritrail-0.12.0-py3-none-any.whl `
  https://github.com/NoctilumeDev/VeriTrail/releases/download/starter-v0.1.0/veritrail_starter-0.1.0-py3-none-any.whl
```

最小作者链只有：

```powershell
veritrail-starter doctor --answers C:\absolute\path\answers.json
veritrail-starter init --preset single-webapp --answers C:\absolute\path\answers.json
veritrail-starter validate --workspace C:\absolute\subject\.veritrail
veritrail-starter review --workspace C:\absolute\subject\.veritrail
```

Starter 可以为高级人工操作者打印 manual handoff，但不会执行 handoff 中的 Core 命令。任何生成物仍是
草案，不能因为生成成功而被描述为 sealed、run 或 PASS。

## 4. Authoring Skill 安装与边界

下载并校验 `veritrail-authoring-0.1.0.zip` 后，将完整的 `veritrail-authoring` 目录安装到支持
`SKILL.md` 的 Codex Skill 目录。不要只复制脚本，也不要把仓库测试、缓存或本机 intake 一起打包。

Skill 的 Starter 权限精确为：

```text
doctor / init / validate / review
```

它不能调用 `handoff`，不能安装或修复环境，不能 seal、批准 Preview、run、比较、批次分析或决定
Verdict。Skill 输出中的解释没有证据权威，Starter DRAFT 才是作者链产物。

## 5. 发布验收事实

本次发布已同时满足：

- Python 3.10 与 3.13 的 wheel、sdist clean install；
- 普通模式与 `python -O` 行为一致；
- 官方 Skill quick validator 通过；
- Skill 与 direct Starter 的 DRAFT 逐字节一致；
- 重复 init 返回 `OUTPUT_CONFLICT` 且不覆盖既有 workspace；
- 提示注入、秘密、越界路径、不支持拓扑与版本漂移负例保持 fail-closed；
- Workbench test、lint、type-check、production build 和依赖审计通过；
- 标签、Release 名称、资产集合、大小、digest、SHA-256 与下载副本 clean-install 全部公开读回一致。

Public CI 与 Browser Smoke 在发布提交上通过：

- [Public CI 32680099398](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32680099398)
- [Browser Smoke 32680099411](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32680099411)

公开下载读回使用 Release 的 7 个资产，而不是仓库工作树或 editable 安装。Python 3.10.6 与
3.13.13 分别复验 Starter wheel、sdist、Core 0.12.0 公共 wheel 和 Skill ZIP；结果为：

```text
state                         PASS
asset set                     7 / 7
uploaded vs downloaded        BYTE_IDENTICAL
direct Starter vs Skill DRAFT BYTE_IDENTICAL
normal vs python -O facts     BYTE_IDENTICAL
official Skill validation     PASS
```

GitHub 公开资产摘要为：

| 资产 | SHA-256 |
| --- | --- |
| `veritrail_starter-0.1.0-py3-none-any.whl` | `b16b4b5e7ecdfc10692c7d26cef0668533d7d4db9fb3a7ba78651eed09d3bd69` |
| `veritrail_starter-0.1.0.tar.gz` | `2e7bd2fdced908d2bf7e8294c6b2f3f1cd427df77614cf95590cdb4e8aab46b0` |
| `starter-e1-validation-summary.json` | `5a588f88369406340f9bc88f2942b593faec045033a6f8d4749dff0ead3a4646` |
| `SHA256SUMS-starter.txt` | `920ed09abf317f88657a62e548e9fb85bb47665f6007ecf226eb977e5b04f196` |
| `veritrail-authoring-0.1.0.zip` | `1a72f4aba917b3c089ee90665038a17b5627e67e0e38d1c0b0b76e97621f6974` |
| `authoring-skill-e1-validation-summary.json` | `51a6066ea2738352ca4f7dfcd78ae25ed0ff4081f058c5f190024fc8a5aa49fc` |
| `SHA256SUMS-authoring-skill.txt` | `20684909030aa104cb3faadcb1707edcefa16be2b2832808ccd887996a8debfb` |

以上事实来自 GitHub API 与实际 Release 下载副本的双重读回；没有用本地候选构建代替公开发布成功。
