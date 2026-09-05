# P1 Structured GitHub API Collector 实现与冻结事实 0.2

> 状态：`P1_FROZEN / P2_NOT_STARTED`
>
> 0.1 精确施工基线：`8d3728cd2255c6a042c41183f9dc9e63e7ce547d`
>
> 0.2 语义纠正施工基线：`9b45bd635dedd132dc8333c105c04723991c2670`
>
> 0.2 语义纠正提交：`7bd800fd9962fa4b4baa7a849128f373d7fa294a`
>
> 0.2 受保护主线实现基线：`5b363637f59be9786d58eed61a14e3bd663dd6d8`
>
> 影响层级：P1 合同、独立 `plugins/github-evidence` 事实结构与规范化语义；不修改 Core、Schema、Starter、
> Authoring Skill 或 Workbench 语义

## 1. 冻结结论

P1 已形成一条可运行的只读纵向切片：插件从 sealed `AcceptancePlan 0.1` 机械派生有界 observation
request，串行读取 GitHub REST API，规范化平台事实，并输出标准 VeriTrail `Evidence 0.1`。最终
`PASS / FAIL / INCONCLUSIVE / PENDING` 仍由 Core 按 sealed Plan 推导；插件不保存另一套期望值，
也不生成 Verdict-like 布尔值。

0.2 修正已经独立 PR、required checks、受保护 `main` 合入、精确主线读回和未登录 GitHub 页面
README/本文真实读回，因此 P1 冻结为 `P1_FROZEN`。冻结只覆盖本文件明确列出的 P1 语义与证据，
不自动授权 P2、P3 或 P4。

初始实现虽已完成本合同原 0.1 矩阵并由 PR #30 合入主线，但 Freeze 前反例证明 active rulesets 与
classic branch protection 被错误建模成 primary/fallback。0.2 只纠正这一处 Observation Model：两个
可同时适用的来源必须独立观察、聚合并保留 provenance。冻结事实 PR #31 因此关闭且未合并；既有绿灯
不覆盖新反例。

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
required checks、check runs/statuses、release、bounded tag peel 和 Pages API metadata。required-check
采集无条件分别访问 active rulesets 与 classic branch protection；Ruleset=A、BranchProtection=B 得到
A+B，Ruleset=[] 仍保留 B。同一 `context + integration/app identity` 来自两个来源时只形成一个有效
item，但 `sources[]` 保留全部 provenance。任一来源不可观察时，另一来源的成功不能把 coverage 冒充
为 `COMPLETE`。身份不足、重复资产、坐标不符、窗口内变化和可见性歧义进入显式 conflict/error；
`401/403/404/429/304/5xx`、timeout、网络错误、损坏 JSON 和上限触发均 fail closed。

最终 Evidence 不保留 Authorization、Cookie、原始 response body 或完整 request headers。发布采用
create-new 与 atomic publish，不覆盖已有产物；异常或取消后的 staging 必须清理。

## 5. 离线与兼容回归

插件现有 57 项测试，覆盖四个规范 JSON 向量、Plan-to-request 派生、四类身份分离、分页与预算、
PR/check/tag/release/Pages 正负链、HTTP/网络失败、凭据边界、Core 原字段断言、Evidence conformance
与原子发布，并新增 ruleset+branch protection、空 ruleset、跨来源同项及来源不可观察四组单变量
反例。串行本地结果为：

| 门禁 | CPython 3.10 | CPython 3.13 |
| --- | --- | --- |
| 插件普通 / `-O` | `57/57` / `57/57` | `57/57` / `57/57` |
| Core 普通 / `-O` | `383/383` / `383/383` | `383/383` / `383/383` |
| Starter 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |
| Authoring Skill 普通 / `-O` | `24/24` / `24/24` | `24/24` / `24/24` |

两个真实 Authoring DRAFT preset 均为 `PASS`，并继续保持
`NOT_RUN / NOT_SEALED / NO_VERDICT`。Workbench 完成 14 个文件、`173/173` 测试、零警告 lint、
type-check、生产 build 和 npm 官方审计端点 moderate 依赖审计零漏洞。插件源码与测试通过 Ruff
format/check。M3 真实 Chromium smoke 完成 5 项检查与 102 个网络请求，console/page/request/HTTP
错误均为零，最终 `PASS` 且端口释放。

公共 CI 新增双 Python 插件测试与 wheel 构建，并新增无 checkout 的 wheel-only 作业：它只下载并
安装同一矩阵产生的 Core wheel 与插件 wheel，再从 `site-packages` 验证公开版本、规范摘要向量和
CLI 入口。作业设置 `max-parallel: 1`，没有把真实 GitHub 的可变网络状态变成主门禁。

## 6. 真实 GitHub 只读纵向切片

参考 Plan 固定公开仓库 `NoctilumeDev/VeriTrail` 与不可变 commit：

```text
8d3728cd2255c6a042c41183f9dc9e63e7ce547d
```

0.2 候选使用两个匿名 request instance 各串行执行 2 个 `GET`，均得到 `COMPLETE`。两次规范化结果的
facts digest 相同：

```text
fffbdf2f5b76b898f386d379d3207c8463bc733544d26dde911780b6a33654bb
```

两次 request seal、collection session 与 Evidence SHA 均不同，符合“同一事实不等于同一次观察”。
`normalization_semantics_version` 已升级为 `github-rest-facts/0.2`，因此它不冒充 0.1 的事实身份。

另以只读认证会话请求 `rules.required_checks`：真实调用顺序为 repository、exact commit、active rules、
classic branch protection；active rules 返回 7 个 ruleset 要求，而 branch protection required-status
endpoint 返回语义不确定的 404。Collector 保留已观察的 7 项，同时输出 `PARTIAL` 与
`NOT_VISIBLE_OR_NOT_FOUND`，没有用 ruleset 成功遮蔽另一来源不可判；Evidence 的 token/Authorization/
Bearer/Cookie 形态扫描为零。这是本次语义纠正的真实负链，不是 `COMPLETE` 正链。

Python 3.10 与 3.13 还分别在无 checkout 的隔离环境中，只安装 Core `0.12.2` wheel 与插件 wheel，
从 `site-packages` 完成真实匿名 `COMPLETE` 采集，均得到上述 0.2 facts digest；没有从工作树偷导入
源码。

## 7. 范围外与停止线

本冻结基线没有进入：

- P2 浏览器公开渲染采集或 API/Render 双源关系；
- P3 自动 Core handoff、完整 Verdict pipeline 或远端调度；
- P4 插件标签、Release、Pages 发布或稳定安装坐标；
- GraphQL、GitHub Enterprise、自定义 host、webhook、scheduler 或组织级扫描；
- GitHub 之外的真实性锚点；
- Codex Security 深扫、攻击路径分析或“已经证明安全”的声明。

P1 只证明合同内的只读采集、事实规范化、Evidence 生成与 Core 可消费性。它不能证明封存前的事实
真实，也不判断提出者观点终极正确；未知与冲突必须继续可见。

## 8. 冻结闭环事实

1. 0.2 修正提交 `7bd800fd9962fa4b4baa7a849128f373d7fa294a` 从精确
   `main@9b45bd635dedd132dc8333c105c04723991c2670` 起步，未混入 P2/P3/P4；
2. [PR #32](https://github.com/NoctilumeDev/VeriTrail/pull/32) 的
   [公共 CI run 33976028039](https://github.com/NoctilumeDev/VeriTrail/actions/runs/33976028039)
   共 11 个 job，最终 11 项全部 `SUCCESS`；
3. PR #32 以 merge commit `5b363637f59be9786d58eed61a14e3bd663dd6d8` 合入受保护 `main`，
   合入后 `origin/main` 精确读回同一 SHA；
4. 从未登录 GitHub 公共页面真实渲染读取
   [README](https://github.com/NoctilumeDev/VeriTrail) 与
   [本文](https://github.com/NoctilumeDev/VeriTrail/blob/main/docs/84-p1-structured-github-api-collector-freeze-candidate.md)，
   页面实际显示 0.2 来源叠加语义、57 项插件测试、真实 `PARTIAL` 负链与 P2/P3/P4 停止线；
5. 旧冻结事实 PR #31 保持关闭且未合并，保留“全绿候选被新语义反例否决”的历史，不改写成从未发生。

P1 至此冻结。下一阶段若启动，只能另行定义 P2 公共渲染采集合同；当前明确为 `P2_NOT_STARTED`。
