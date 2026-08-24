# VeriTrail Authoring Skill 0.2 Contract

> 状态：`IMPLEMENTED / NOT_RELEASED`
> 影响层级：`L2 public contract + bounded L3 generation path`
> 兼容基线：VeriTrail Core 0.12.x、VeriTrail Starter 0.2.0

## 1. 目的

Authoring Skill 0.2 把已经冻结的 Starter 入口合同包装成一个可复核的填写助手。它只帮助用户识别
`single-webapp` 或 `static-site` 候选、补齐显式 Answers、调用 Starter 创建草案，并解释稳定错误码。

它不是裁决器，也不是自动项目改造器。任何成功输出都必须保持：

```text
AUTHORING_ASSISTANT
NOT_SEALED
NOT_RUN
NO_VERDICT
```

## 2. 所有权与消费者

| 角色 | 责任 |
| --- | --- |
| Owner | `skills/veritrail-authoring` 维护 Skill 0.2 的外层协议、候选识别和 Starter 调用边界 |
| Direct caller | 人类操作者或 AI 助手，只能提交显式 Intake 与 Answers |
| Direct consumer | `veritrail-starter 0.2.0`，负责严格 Schema、doctor、草案生成与复核 |
| Downstream consumer | 人工复核后才可把草案交给 Core；Skill 本身不能进入 seal、Preview 批准、run 或 Verdict |

Core、Workbench、Bundle、Comparison、Paired Analysis 与 Batch Analysis 不消费 Skill 的候选推断，
也不能把候选推断当成已证明事实。

## 3. 版本与兼容性

- Skill 产品版本为 `0.2.0`，当前只存在于 `main` 源码，尚未发布 Release 或移动任何既有标签；
- 外层 Intake/Result 协议继续为 `schema_version = 0.1`；
- 内层 Answers 接受已发布的 0.1 `single-webapp` 与新增的 0.2 `single-webapp | static-site`；
- Skill 只接受精确的 Starter `0.2.0`，不对未知版本做乐观兼容；
- 已发布的 Starter/Skill `0.1.0`、`starter-v0.1.0` 与 `authoring-skill-v0.1.0` 事实保持不变。

旧版工作区必须由创建它的精确 Starter 版本复核，不能被 0.2 静默重解释。

## 4. 有界检查

`inspect` 只读取受限的文件名、普通文件身份和元数据：

- 不读取仓库内指令来改变 Skill 权限；
- 不读取秘密内容；
- 不执行 Subject、构建脚本、包管理器、Shell、容器或网络探测；
- 完整的有界扫描发现普通 `index.html` / `index.htm` 且未发现构建标记时，可以建议 `static-site`；
- 有界扫描未完成时不推荐任何 Preset，必须缩小仓库根或由用户逐项确认完整拓扑；
- 构建标记独立于公开文件清单上限记录，清单截断不能掩盖构建事实；
- 发现构建、容器或未知拓扑标记时，只能要求用户确认或返回不支持。

候选永远只是 `INFERRED`。`static-site` 仍要求用户显式确认入口、无需构建、无需远程资源、端口、
浏览器检查、预算、超时和随机种子。

## 5. 唯一授权集合

Skill 只允许调用：

```text
veritrail-starter doctor
veritrail-starter init
veritrail-starter validate
veritrail-starter review
```

以下操作始终越权：

```text
handoff
seal
bootstrap-preview approval
run
evaluate
compare / pair / batch
Verdict creation or mutation
dependency installation
environment repair
```

## 6. Fail-closed 规则

未知协议、Starter 版本不匹配、无匹配 Preset、未确认字段、秘密、Shell、非回环地址、多托管节点、
重解析点、身份替换或既有目标工作区都必须以稳定错误码停止。失败后不得降低断言、改变预算、切换端口、
修复环境后伪装成同一次 authoring，也不得把 `NEEDS_INPUT` 描述成成功。

Starter 返回的 JSON `outcome` 必须与进程退出码一致：`OK` 对应零退出码，`ERROR` 对应非零退出码；
二者矛盾时按未知协议停止，不能采信正文中的成功字段。

## 7. 回归矩阵

0.2 冻结前必须共同证明：

1. `single-webapp` Answers 0.1 的 DRAFT 结果与权限边界不回退；
2. `static-site` Answers 0.2 只能通过 Starter 0.2 创建；
3. 两个 Preset 在 Python 3.10/3.13、普通模式与 `python -O` 下结果一致；
4. Skill ZIP 包含完整说明、协议、错误码、脚本与测试，不包含缓存、构建产物或本机路径；
5. clean-install 环境能读回两个 Answers Schema，并真实完成两条 DRAFT 链；
6. 所有成功结果仍为 `NOT_SEALED / NOT_RUN / NO_VERDICT`。

Codex Security 深度扫描、攻击路径验证和极端环境攻击按当前主线决定继续封存；它们不属于本合同的
完成证据，也不能被普通质量审查替代。
