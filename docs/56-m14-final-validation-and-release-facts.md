# M14 整改后终局复验与发布事实 1.0

## 1. 结论与发布坐标

- 里程碑：M14“整改后终局复验与发布收束”；
- 结论：`FROZEN / RELEASED`；
- 稳定版本：`0.12.0`；
- 注释标签：`v0.12.0`；
- GitHub Release：<https://github.com/NoctilumeDev/VeriTrail/releases/tag/v0.12.0>；
- 产品候选代码提交：`3dfae7b698de5d43b03cccb088fd9810ddf429fb`；
- 最终发布提交：由不可移动坐标 `v0.12.0^{}` 唯一解析。

本文是文档 54 的执行事实，不改写 M0–M13 的冻结结论，也不增加新能力。M14 的代码影响范围为
安全整改后的既有 L1 所有者、发布元数据和 L0 文档；最终候选没有新增 L2 Schema、Verdict 语义或
L3 数据所有权。

Git 提交不能在自身内容中写入自己的最终 SHA。为避免伪造“自指哈希”，本文使用可验证的注释标签
`v0.12.0^{}` 表达最终发布提交；Release 附件 `m14-validation-summary.json` 在发布提交形成后记录其
字面 SHA，远端标签、Release target 和该字段必须三方一致。

## 2. 冻结环境与支持矩阵

| 维度 | 冻结事实 |
| --- | --- |
| 宿主 | Windows 11 Home，64 位，build 26200 |
| 资源级别 | C1，16 GiB 单机，严格串行 |
| Python | 3.10.6 与 3.13.13 |
| Node / npm | Node 24.14.0 / npm 11.9.0 |
| Browser | Playwright 1.62.0 的真实 Chromium，固定回环 origin |
| Workbench | Vue 3.5.41 / Vite 8.2.1，生产构建 |
| 真实目标 | VeriTrail 自证目标 + InkNarratives 精确提交 |

Python 包声明 `Requires-Python >=3.10`，但本次最终产品级冻结只对上表的 Windows/C1 与双 Python
组合负责。macOS、Linux、C0/C2/C3、Docker、多服务拓扑和不可信代码隔离没有因本次发布而获得证明。

## 3. 自动化、依赖与构建门禁

| 门禁 | 结果 |
| --- | --- |
| Python 3.10 全量回归 | `318/318 PASS` |
| Python 3.13 全量回归 | `318/318 PASS`，并启用 `ResourceWarning` fail-closed |
| Workbench 单元测试 | `171/171 PASS` |
| Workbench lint | `PASS` |
| Workbench type-check | `PASS` |
| Workbench production build | `PASS`，无未解释弃用警告 |
| 两套 Python `pip check` | `PASS` |
| npm production/full audit | `0 vulnerabilities` |
| wheel 与 sdist 构建 | `PASS` |
| wheel 独立安装与最小 seal/evaluate | `PASS` |
| sdist 独立安装与最小 seal/evaluate | `PASS` |
| Workbench ZIP 解包逐文件复核 | `63/63` 与生产 `dist` 内容一致 |

wheel 与 sdist 均在全新的临时环境中安装，并真实执行最小 Plan 的 `seal -> evaluate`，得到
`COMPLETED / PASS`；因此这里不以“文件能够构建”冒充“安装后能够运行”。

## 4. 安全终审

M14 先按文档 55 关闭两轮旧扫描中 15 项有效问题，再重新建立基线。最终标准安全扫描：

- Scan ID：`503eb9ca-5576-4888-8218-7a9f76a5f0e5`；
- 覆盖：375 个文件、12 个攻击面；
- 可报告发现：`0`；
- 独立静态复核：`0` 个新增可报告问题；
- 最终候选相对扫描基线的后续变化仅为版本、许可证与发布元数据，不改变运行时信任边界。

以下仍是明确边界，不得被 Release 绿灯解释为已解决：

1. 已经控制本机宿主或当前用户的攻击者；
2. 截图像素中的业务敏感信息；
3. 可执行文件映射到启动之间的 TOCTOU；
4. 可信 Subject 自身的任意文件写入或外连能力；
5. Windows Job Object 与结构化命令约束不是恶意代码沙箱。

## 5. VeriTrail 自证目标

最终候选在常规模式与 `python -O` 优化模式下各完成一轮 13 项预注册真实验收。两轮均满足：

- Catalog：`COMPLETED`；
- Run：13 个；Catalog issue：0；
- 正向重复 Comparison：`MATCH`，0 differences；
- 敏感扫描：0 命中；
- application 端口、staging、线程与 SQLite sidecar：0 残留；
- Pairing/Batch 对该目标按预注册边界得到 `SOURCE_PLAN_VERSION_UNSUPPORTED`，不是伪造通过。

13 个公共出口按顺序为：

| # | 场景 | ExecutionStatus | Verdict |
| ---: | --- | --- | --- |
| 1 | positive-01 | `COMPLETED` | `PASS` |
| 2 | positive-02 | `COMPLETED` | `PASS` |
| 3 | early exit | `COMPLETED` | `FAIL` |
| 4 | readiness timeout | `ABORTED` | `FAIL` |
| 5 | owner mismatch | `ABORTED` | `FAIL` |
| 6 | port conflict | `ABORTED` | `PENDING` |
| 7 | user cancel | `ABORTED` | `PENDING` |
| 8 | browser negative | `COMPLETED` | `FAIL` |
| 9 | collector error | `ERROR` | `PENDING` |
| 10 | subject drift | `COMPLETED` | `INCONCLUSIVE` |
| 11 | cleanup failure | `ERROR` | `FAIL` |
| 12 | staging failure | `ERROR` | `PENDING` |
| 13 | memory stop | `ABORTED` | `PENDING` |

常规模式启动时可用内存为 8403 MiB；真实浏览器峰值约 217 MiB。memory-stop 使用预注册停止夹具，
只证明停止语义与现场保留，不把人为降低阈值写成生产容量。

## 6. InkNarratives 真实目标

真实项目验收绑定 InkNarratives 精确提交：
`076be2f92194b90e31535d4583ac4d5e72922794`。使用干净临时克隆，开始和结束均验证：

- `origin` 与精确提交一致；
- 工作区干净；
- 项目原生 verifier 在验收前后均 `PASS`；
- 常规与优化模式各得到 `PASS / FAIL / PENDING / PASS`；
- 恢复 Comparison 为 `MATCH`、0 differences；
- 损坏副本被隔离，Catalog 为 `COMPLETED_WITH_ISSUES`，4 个有效 Run、1 个隔离 issue；
- 敏感扫描 0 命中，端口、staging 与自有进程 0 残留；
- subject 浏览器峰值最大 1073.719 MiB，Core 峰值最大 55.25 MiB，宿主可用内存最低
  6987.617 MiB。

该目标不适用 Pairing/Batch；本次没有把“不适用”改写成 `PASS`。

## 7. 生产 Workbench 与内置浏览器

最终浏览器验收只使用 Release Workbench ZIP 解包后的生产文件与本轮真实 Catalog，不使用 Vite
开发服务器或测试夹具代替发布产品。内置浏览器实际检查：

- 桌面 `1440 x 960`；
- 移动 `390 x 844` 与 `360 x 800`；
- Runs 目录、Run 详情、返回目录、Pairing、Batch、Comparison；
- Run 详情与返回目录没有旧页面闪现；
- 三个数据视图使用各自正确的 `fixture/sample`；
- 三种视口根横向溢出均为 0；
- Console 为 0 条错误；
- 页面资源均为同源或 `data:`，无未解释外网资源；
- 最终可视检查未发现错位、裁切、遮挡或历史样式残留。

Workbench 仍是 Bundle 的只读消费者。它不重算 Verdict，不拥有不可变事实，也不因视觉状态改写
Core 结论。

## 8. 发布资产与校验

GitHub Release 必须包含五个资产：

| 资产 | 大小 | SHA-256 |
| --- | ---: | --- |
| `veritrail-0.12.0-py3-none-any.whl` | 193116 bytes | `d0293f06e6a2b0271870ce032b2197c6ef7956db0ff3889230ca48234ff2fa45` |
| `veritrail-0.12.0.tar.gz` | 268448 bytes | `88b437d916574d884eef4a6449165f2b156da6f7aae49edd80a05782058ead68` |
| `veritrail-workbench-0.12.0.zip` | 7779314 bytes | `8ffe5fd50cbb8bdbb0677140ececcf3c3630c05a14a93e2b38a88d040391155d` |
| `m14-validation-summary.json` | 发布时生成 | 见 `SHA256SUMS.txt` |
| `SHA256SUMS.txt` | 发布时生成 | 由 GitHub asset readback 单独复核 |

`SHA256SUMS.txt` 按标准非自指约定覆盖其余四个 payload；它不能包含自己的哈希。第五个资产本身通过
GitHub Release API 下载回读计算 SHA-256，并与本地上传文件比较。Release 的 tag target、附件数量、
附件大小和所有摘要都必须在发布后读回，任何不一致都阻止最终宣布完成。

## 9. 失败恢复与剩余边界

- 安装失败：保留命令、解释器、wheel/sdist 摘要与 `pip check` 输出，不改 Verdict；
- Browser 失败：保存 Bundle/Console/Network/截图，先清理自有进程和端口，再启动新 Run；
- Subject 漂移：标记 `INCONCLUSIVE`，重新封存新 Plan，不移动旧标准；
- 资源停止：保存现场并标记 `ABORTED`，不伪造产品 `FAIL`；
- Release 上传或读回失败：不移动标签，修正后重新执行发布门禁。

M14 冻结的是 VeriTrail Core 0.12.0 和当前只读 Workbench。通用项目探测、自动安装、脚手架、AI
Authoring Skill、跨平台完整自举、Docker、多服务编排与恶意代码隔离均属于发布后的独立入口层或
后继项目，不进入本次结论。

## 10. 最终读回规则

最终完成必须同时满足：

1. `origin/main`、`v0.12.0^{}` 和 GitHub Release target 指向同一提交；
2. `Public CI` 与 `Browser Smoke` 对该提交为绿色；
3. Release 不是 draft，也不是 prerelease；
4. 五个资产全部存在并通过下载回读；
5. `m14-validation-summary.json` 的提交、环境、目标、测试和摘要与本文一致；
6. 本地工作区干净，验收服务、端口与临时进程无残留。

满足以上条件后，M14 与 VeriTrail Core 0.12.0 才可保持 `FROZEN / RELEASED`。
