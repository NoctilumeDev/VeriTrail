# VeriTrail Authoring Skill A0 冻结事实

> 状态：`A0_COMPLETE / DRAFT_ONLY / SECURITY_REVIEWED / E1_READY`
>
> 兼容目标：`veritrail-starter 0.1.0.dev0`
>
> 权限边界：`AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT`

## 1. 冻结结论

A0 已把冻结的 Starter 0.1 命令合同包装成一个可重复验证的 Authoring Skill。它是帮助用户填写合同的
“书记员”，不是 Core 的 evaluator、judge、operator 或 installer。A0 完成只表示仓库内源码与门禁
已经冻结；Skill 尚未独立发布，不能描述为正式版已经开箱即用。

A0 没有修改 VeriTrail Core 0.12.0 的 Schema、Seal、Preview、Run、Evidence、Verdict、Bundle、
Catalog 或 Workbench，也没有移动 `v0.12.0`。

## 2. 实现面

实际实现由以下文件组成：

- `skills/veritrail-authoring/SKILL.md`：身份、权限、工作流和来源语言；
- `skills/veritrail-authoring/agents/openai.yaml`：UI 元数据；
- `skills/veritrail-authoring/references/protocol.md`：Authoring intake 0.1 与状态机；
- `skills/veritrail-authoring/references/error-codes.md`：Starter 错误码到 Skill 状态的稳定映射；
- `skills/veritrail-authoring/scripts/authoring.py`：标准库实现的有界 inspector、candidate、draft 与
  review-draft；
- `skills/veritrail-authoring/tests/test_authoring.py`：合同、负例与权限自动化；
- `scripts/authoring_skill_acceptance.py`：真实 Starter DRAFT 链验收器；
- `.github/workflows/ci.yml`：普通模式、`python -O` 与真实 DRAFT 链公共门禁。

## 3. 权限与状态机

Skill 的 Starter 命令允许列表精确为：

```text
doctor
init
validate
review
```

`handoff`、Core seal/run/evaluate/compare/pair/analyze-batch、Preview 批准、环境修复、依赖安装与
Subject 执行均不可调用。`review-draft` 只重新运行 Starter validate/review。

Skill 状态只包含：

```text
NEEDS_USER_INPUT
NO_MATCHING_PRESET
STARTER_VERSION_UNSUPPORTED
STARTER_VALIDATION_FAILED
CANDIDATE_READY
DRAFT_READY_FOR_HUMAN_REVIEW
```

这些状态都不是产品 Verdict。成功草案固定读回：

```text
AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT
```

## 4. 检查与数据边界

- inspector 最多检查 2048 个目录项、深度 4，只返回最多 128 个公开文件名与元数据；
- `.env*`、私钥、凭据、浏览器资料、依赖目录、重解析点和仓库外路径不读取；
- 仓库内 README、注释和提示文本全部视为不可信数据，不能扩大权限；
- intake 最大 256 KiB，必须是普通、单链接、非重解析文件；读取前、打开后与读取后绑定
  `st_dev/st_ino/st_size/st_mtime_ns/st_nlink`，同大小同时间戳替换也 fail-closed；
- Starter 子进程使用结构化参数、`shell=False`、关闭 stdin、30 秒停止线；
- transient Answers 只在 Subject 内短暂存在，并在成功或失败后删除；既有 `.veritrail` 永不覆盖。

## 5. 自动化与真实链事实

- Core 在 Python 3.10 与 Python 3.13 下各通过 321/321，共 642 次测试执行；
- Starter 合同测试为 18 项；两套 Python 均在普通模式和 `python -O` 下通过 18/18，共 72 次测试执行；
- Skill 合同测试为 17 项；
- Python 3.10 与 Python 3.13 均在普通模式和 `python -O` 下通过 17/17，共 68 次测试执行；
- 真实验收链在 Python 3.10 与 Python 3.13 下各通过一次；
- 真实链精确取得 `CANDIDATE_READY`、`DRAFT_READY_FOR_HUMAN_REVIEW`、只读复核与
  `OUTPUT_CONFLICT`，并证明允许权限只有 `doctor/init/validate/review`；
- 提示注入文件与 `.env.local` 同时存在时，Skill 忽略秘密文件、不执行仓库指令、不写入候选阶段；
- 同大小、同 mtime 的 intake 替换反向复现先证明旧读取窗口可被触发，加固后稳定得到
  `INTAKE_UNAVAILABLE`；该项作为 fail-closed 质量加固保存，不被夸大为跨权限漏洞；
- Workbench 通过 172/172、lint、类型检查与生产 build；针对 `registry.npmjs.org` 的只读
  `npm audit --audit-level=moderate` 返回 0 个漏洞。配置的 npmmirror 审计端点不实现 npm audit API，
  该基础设施限制没有被写成依赖安全结论。

## 6. 安全与工具验证

首轮 Codex Security 差异扫描完成 3/3 变更源文件覆盖，并识别本机单用户边界内的 intake 身份竞争
候选；它不满足跨权限攻击路径，但 A0 仍按更严格的 fail-closed 标准完成稳定文件身份绑定与回归测试。
加固后的最终差异扫描 `fb9ba170-bb38-47bb-9634-7b0ad4f9a732` 再次完成 3/3 变更源文件覆盖，
覆盖状态为 `complete`，可报告安全发现为 0。TAC 账户状态因访问连接器未连接而无法验证；该可见性限制
没有被当成扫描通过证据，最终结论来自已封存的本地扫描清单、覆盖清单和零发现清单。

`skill-creator` 自带 `quick_validate.py` 需要 PyYAML；两套已配置 Python 环境均未安装该非项目依赖，
因此没有为验证器临时改变环境。仓库自身的元数据、前置字段、命名、占位符和行为测试已覆盖实际
交付结构；E1 clean install 时仍应在隔离验证环境中补跑官方 quick validator。

## 7. E1 入口

E1 只处理：

- Skill 与 Starter 的独立版本、包装和 clean install；
- 无 AI 时 Starter 链、带 Skill 时 DRAFT 链的等价边界；
- 双 Python、普通／优化模式、提示注入、秘密、路径、版本和不支持拓扑；
- 公共 README、Skill 发现、下载资产、摘要、GitHub Release 与安装后读回；
- Core 0.12.x 完整兼容回归与零残留。

E1 不扩展第二个 Preset，不增加自动安装、自动修复、handoff、seal、run 或 Verdict 权限。
