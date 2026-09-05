# P1 Structured GitHub API Collector 实现与冻结事实 0.1

> 状态：`P1_FROZEN / P2_NOT_STARTED`
>
> 精确施工基线：`8d3728cd2255c6a042c41183f9dc9e63e7ce547d`
>
> 完整实现候选：`244c54b60986673622704a361da76dbc86a90788`
>
> 受保护主线实现基线：`9b45bd635dedd132dc8333c105c04723991c2670`
>
> 影响层级：独立 `plugins/github-evidence` 包与公共 CI；不修改 Core、Schema、Starter、
> Authoring Skill 或 Workbench 语义

## 1. 冻结结论

P1 已形成一条可运行的只读纵向切片：插件从 sealed `AcceptancePlan 0.1` 机械派生有界 observation
request，串行读取 GitHub REST API，规范化平台事实，并输出标准 VeriTrail `Evidence 0.1`。最终
`PASS / FAIL / INCONCLUSIVE / PENDING` 仍由 Core 按 sealed Plan 推导；插件不保存另一套期望值，
也不生成 Verdict-like 布尔值。

候选已经过独立 PR、11 项远端 checks、受保护 `main` 合入、真实 GitHub Markdown 渲染与匿名公开
HTML 读回，因此 P1 在本文合同范围内标记 `FROZEN`。这不是插件 Release，也不授权进入 P2。

## 2. 分层与依赖边界

新增实现全部位于：

```text
plugins/github-evidence/
├── pyproject.toml
├── README.md
├── examples/acceptance-plan.json
├── src/veritrail_github/
└── tests/
```

插件只依赖 Core `0.12.2` 的公开合同：Plan 验证与 seal、规范 JSON、Evidence 导入/复验以及
observation metadata 校验。Core 不导入插件；插件不导入 Core 私有符号、不复制 Core validator、
不 monkey patch 既有消费者。Comparison、Pairing、Batch、Starter、Authoring Skill 和 Workbench
继续保持 PC2 已冻结的边界。

## 3. 身份、事实与证据

实现分别维护：

```text
Observation Spec Digest   要观察什么
Collector Policy Digest  本次按什么有界策略采集
Request Seal Digest       哪一份派生请求实例
Facts Digest              规范化后看见了什么
Evidence SHA-256          哪一份具体证据产物
Collection Session        哪一次真实采集
```

`facts_digest` 只包含 observation spec、规范化事实和规范化语义版本；request id、采集时间、重试、
API/client/parser 实现版本和访问模式只进入请求或 Evidence provenance。相同平台事实可以得到相同
facts digest，但两次采集仍有不同 session 与 Evidence SHA。插件拥有 GitHub 事实规范化与 facts
digest 复算；Core 只拥有通用 Evidence 合同与最终裁决。

## 4. 有界 GitHub 采集

网络层只允许 `GET`，默认匿名；可选 token 只能从 `VERITRAIL_GITHUB_TOKEN` 运行时内存读取，CLI
没有 token 参数。重定向保持同源，请求数、分页、tag peel、响应体、重试和总采集窗口均有上限；
总窗口使用 monotonic elapsed，不把墙钟当作预算权威。

已实现的规范化投影覆盖 repository、exact commit、pull request、active rules/branch protection、
required checks、check runs/statuses、release、bounded tag peel 和 Pages API metadata。同名异源检查
保持独立；身份不足、重复资产、坐标不符、窗口内变化和可见性歧义进入显式 conflict/error，不能
静默合并为成功事实。`401/403/404/429/304/5xx`、timeout、网络错误、损坏 JSON 和上限触发均
fail closed。

最终 Evidence 不保留 Authorization、Cookie、原始 response body 或完整 request headers。发布采用
create-new 与 atomic publish，不覆盖已有产物；异常或取消后的 staging 必须清理。

## 5. 离线与兼容回归

插件现有 53 项测试，覆盖四个规范 JSON 向量、Plan-to-request 派生、四类身份分离、分页与预算、
PR/check/tag/release/Pages 正负链、HTTP/网络失败、凭据边界、Core 原字段断言、Evidence conformance
与原子发布。串行本地结果为：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| 插件普通 / `-O` | `53/53` / `53/53` | `53/53` / `53/53` |
| Core 普通 / `-O` | `383/383` / `383/383` | `383/383` / `383/383` |
| Starter 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring Skill 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |

两个真实 Authoring DRAFT preset 均为 `PASS`，并继续保持
`NOT_RUN / NOT_SEALED / NO_VERDICT`。Workbench 完成 14 个文件、`173/173` 测试、零警告 lint、
type-check、生产 build 和 moderate 依赖审计零漏洞。插件源码与测试通过 Ruff format/check；CI YAML
由独立解析器读回 7 个作业。既有 M3 真实 Chromium smoke 完成 5 项检查与 102 个网络请求，HTTP
错误为零，最终 `PASS` 且端口释放。

公共 CI 新增双 Python 插件测试与 wheel 构建，并新增无 checkout 的 wheel-only 作业：它只下载并
安装同一矩阵产生的 Core wheel 与插件 wheel，再从 `site-packages` 验证公开版本、规范摘要向量和
CLI 入口。作业设置 `max-parallel: 1`，没有把真实 GitHub 的可变网络状态变成主门禁。

## 6. 真实 GitHub 只读纵向切片

参考 Plan 固定公开仓库 `NoctilumeDev/VeriTrail` 与不可变 commit：

```text
8d3728cd2255c6a042c41183f9dc9e63e7ce547d
```

最终候选复验分别使用匿名与认证会话，各串行执行 2 个 `GET`，均得到 `COMPLETE`。两次规范化结果的
facts digest 相同：

```text
1f99eda3c22e553e303c6f523c624b5c8c95a90fc44e5bfadc65fe33516cf136
```

两次 request seal、collection session 与 Evidence SHA 均不同，符合“同一事实不等于同一次观察”。
认证会话只改变安全 provenance；最终 JSON 对 `Authorization`、`Bearer`、`Cookie` 与 token 形态扫描
为零。另一次同坐标正链由 Core 得到 `PASS`；只改变 sealed assertion 期望的单变量负链由 Core 得到
`FAIL`，证明 Collector coverage 与最终 Verdict 没有混成一层。

Python 3.10 与 3.13 还分别在无 checkout 的隔离环境中，只安装 Core `0.12.2` wheel 与插件 wheel，
从 `site-packages` 完成真实匿名 `COMPLETE` 采集；没有从工作树偷导入源码。

## 7. 范围外与停止线

本候选没有进入：

- P2 浏览器公开渲染采集或 API/Render 双源关系；
- P3 自动 Core handoff、完整 Verdict pipeline 或远端调度；
- P4 插件标签、Release、Pages 发布或稳定安装坐标；
- GraphQL、GitHub Enterprise、自定义 host、webhook、scheduler 或组织级扫描；
- GitHub 之外的真实性锚点；
- Codex Security 深扫、攻击路径分析或“已经证明安全”的声明。

P1 只证明合同内的只读采集、事实规范化、Evidence 生成与 Core 可消费性。它不能证明封存前的事实
真实，也不判断提出者观点终极正确；未知与冲突必须继续可见。

## 8. 远端门禁、主线与公开读回事实

- [PR #30](https://github.com/NoctilumeDev/VeriTrail/pull/30) 从精确基线
  `8d3728cd2255c6a042c41183f9dc9e63e7ce547d` 审查候选
  `244c54b60986673622704a361da76dbc86a90788`；合并前为 `CLEAN / MERGEABLE`。
- [Public CI 运行 33972086544](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33972086544)
  的 11 项检查全部 `SUCCESS`：Python 3.10/3.13、E3 下载验收、Workbench、Starter golden path、
  双 Core wheel-only、双 Acceptance Core freeze 与新增的双 GitHub Evidence wheel-only。
- PR 于 `2026-09-05` 合入受保护 `main`，merge commit 与远端 `refs/heads/main` 均读回
  `9b45bd635dedd132dc8333c105c04723991c2670`。
- 真实 GitHub Markdown 页面随后读回 README 的“P1 实现冻结候选”入口与本文全部八节；标题、
  候选状态、测试矩阵、facts digest、P2/P3/P4 停止线和 README 链接均为渲染后的可见内容。
- 唯一内置浏览器实例当时已有 GitHub 登录会话，因此没有把它谎称为“未登录浏览器”。另以不发送
  Cookie 或 Authorization 的匿名请求读取两个公开 GitHub HTML 页面，均返回 `200`，并逐项读回
  README 标题/本文链接以及本文标题、状态和停止线。API 文本没有替代 GitHub 页面层。

## 9. 冻结后的边界

P1 当前为 `P1_FROZEN / P2_NOT_STARTED`。后继若继续，只能另立 P2 浏览器采集合同；不得把本轮源码
候选自动升级为插件 tag、Release 或稳定安装坐标，也不得在 P1 事实补丁中提前施工 P2、P3 或 P4。
