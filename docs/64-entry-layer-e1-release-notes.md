# VeriTrail 入口层 E1 0.1.0 发布说明

> 状态：`RELEASE_CANDIDATE / PUBLIC_READBACK_PENDING`
>
> 产品：`VeriTrail Starter 0.1.0`、`VeriTrail Authoring Skill 0.1.0`
>
> Core：继续使用冻结的 `VeriTrail Core 0.12.0`

## 1. 这次发布解决什么

E1 把已经完成源码冻结的两个入口产品变成可独立下载、校验和 clean install 的发布候选：

- Starter 把显式 Answers 转换成确定性的 `DRAFT / NOT_SEALED` workspace；
- Authoring Skill 只做仓库只读盘点、有限 Preset 匹配、缺失信息追问和 Starter 调用；
- 有 Skill 与无 Skill 的路径对同一 Answers 必须生成逐字节相同的 DRAFT；
- 两个产品分别版本化和发布，不移动 Core `v0.12.0`，也不扩大 Core 的能力声明。

E1 仍只支持 Windows 11 上的 `single-webapp` 预设。多服务、远程依赖、容器、Shell、秘密和无法确定
进程所有权的拓扑继续 fail-closed。

## 2. 固定发布坐标

| 产品 | 标签 | GitHub Release | 资产数 |
| --- | --- | --- | ---: |
| Starter | `starter-v0.1.0` | `VeriTrail Starter 0.1.0` | 4 |
| Authoring Skill | `authoring-skill-v0.1.0` | `VeriTrail Authoring Skill 0.1.0` | 3 |

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

发布前这些坐标只是冻结合同；只有 GitHub Release、下载副本复验和 API 读回全部通过后，才能标记为
`RELEASED`。

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

## 5. 发布验收

候选发布必须同时满足：

- Python 3.10 与 3.13 的 wheel、sdist clean install；
- 普通模式与 `python -O` 行为一致；
- 官方 Skill quick validator 通过；
- Skill 与 direct Starter 的 DRAFT 逐字节一致；
- 重复 init 返回 `OUTPUT_CONFLICT` 且不覆盖既有 workspace；
- 提示注入、秘密、越界路径、不支持拓扑与版本漂移负例保持 fail-closed；
- Workbench test、lint、type-check、production build 和依赖审计通过；
- 标签、Release 名称、资产集合、大小、digest、SHA-256 与下载副本 clean-install 全部公开读回一致。

最终发布事实和确切摘要只在 Release 创建并从公开下载地址复验后记录；不以本地候选构建代替公开事实。
