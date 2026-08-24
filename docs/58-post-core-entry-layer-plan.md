# Post-Core 独立入口层 Plan v1

> 状态：`FROZEN / E0_COMPLETE / S0_COMPLETE / S1_COMPLETE / A0_COMPLETE / E1_COMPLETE / RELEASED`
>
> 基线：`VeriTrail Core 0.12.0` @ `v0.12.0`
>
> 影响层级：入口层 `L3_SYSTEM`；Core 为只读依赖，不修改其 Schema、Seal、Verdict 或 Workbench

## 1. 产品判断

Core 0.12.0 已经证明验证链的正确性、边界和可复验性，但公共入口仍要求用户先理解 Profile、Plan、
Evidence、Bundle、ExecutionStatus、Verdict、seal、preview 和清理所有权。当前问题是产品化入口缺失，
不是 Core 裁决不足。

入口层采用三层结构：

```text
VeriTrail Authoring Skill 0.1（可选书记员）
                 |
                 v
VeriTrail Starter 0.1（有限模板、doctor、草案与复核）
                 |
                 v
VeriTrail Core 0.12.x（封存、运行、证据与确定性裁决）
                 |
                 v
Read-only Workbench（案卷阅览）
```

入口层降低填写合同和定位环境问题的成本，但不降低证据标准。

## 2. 产品与版本所有权

| 产品 | 首个版本 | 唯一所有权 | 明确不负责 |
| --- | --- | --- | --- |
| VeriTrail Core | `0.12.x` | Schema、Seal、Preview、Run、Evidence、Verdict、Bundle、Catalog | 自动猜项目、自动安装、AI 作者身份 |
| VeriTrail Starter | `0.1.x` | 有限 Preset、doctor、答案快照、DRAFT 生成、静态复核、Core handoff | 自动 seal、自动 run、修改 Verdict、通用拓扑 |
| VeriTrail Authoring Skill | `0.1.x` | 仓库只读盘点、选择有限 Preset、追问缺失信息、调用 Starter | 自己发明合同、读取秘密、封存、运行、裁决 |

三个产品独立版本化。Starter 或 Skill 的变更不能移动 `v0.12.0`，也不能被描述为 Core 0.12.0 已证明
的新能力。

## 3. 固定实施顺序

```text
E0 入口治理与文档基线
  -> S0 Starter single-webapp 草案链
  -> S1 PASS/FAIL 黄金路径与真实验收
  -> A0 Authoring Skill 包装
  -> E1 独立发布与公共读回
```

### E0：入口治理与文档基线

交付：

- 根目录 `START_HERE.md`；
- 本 Plan；
- [Starter 0.1 合同](59-starter-single-webapp-contract.md)；
- [Authoring Skill 0.1 合同](60-authoring-skill-contract.md)；
- README 与里程碑索引；
- 文档链接、边界语言和历史标签不漂移检查。

E0 只改文档，不新增 CLI，不修改 Core。

### S0：Starter 0.1 最小纵向切片

首个实现只能包含：

```text
veritrail-starter doctor
veritrail-starter init --preset single-webapp --answers <json>
veritrail-starter validate --workspace <directory>
veritrail-starter review --workspace <directory>
veritrail-starter handoff --workspace <directory>
```

命令名是 S0 实现合同，不代表 E0 完成时已经可用。S0 默认非交互地消费答案文件；未来可以增加交互
问答，但最终答案仍必须固化为可审计 JSON，且相同输入应产生逐字节稳定的草案。

S0 的实现必须位于独立包和独立命名空间中。它可以声明对 Core `>=0.12,<0.13` 的兼容依赖并复用公开
验证器，但不得导入下划线私有函数，不得在 Core CLI 中偷偷增加自动 authoring 分支。

### S1：十分钟黄金路径

黄金路径固定使用仓库内合成、脱敏、单节点 Web 示例：

```text
doctor
  -> init DRAFT
  -> validate/review
  -> 用户显式执行 Core seal
  -> 用户批准 Preview
  -> PASS Run
  -> 只改变一个预注册业务事实
  -> 独立 FAIL Run
  -> Catalog/Workbench 同时读回两份 Bundle
```

FAIL 是教材的一部分，不能在清理示例时删除。教程必须解释“运行完成、证据完整、断言成立和 Verdict”
四者不同。

### A0：Authoring Skill

A0 只能在 Starter 0.1 的命令、输入输出和错误码冻结后开始。Skill 必须调用 Starter，不得让模型按每次
对话重新发明 Profile/Plan。所有模型建议保持候选事实；不能封存、运行或裁决。

### E1：独立发布

发布前必须验证：

- Starter clean install、双 Python、Windows 11/C1 真实黄金路径；
- PASS/FAIL 两个 Bundle、Catalog/Workbench 桌面与移动读回；
- 相同答案逐字节稳定、重复 init 拒绝覆盖、越界项目 fail-closed；
- ToolBindings 不进入版本库，秘密值和个人绝对路径不进入公共产物；
- Skill 对仓库内提示注入、秘密文件、缺失信息和不支持拓扑保持拒绝；
- Core 0.12.x 全量兼容回归；
- 独立版本、标签、Release、摘要和下载回读。

## 4. 首个 Preset

唯一首发 Preset 为 `single-webapp`：

- Windows 11；
- `C1_PROCESS_COLD`；
- 一个由 Run 创建并拥有的可信 application；
- 直接可执行文件加结构化参数，不经过 Shell；
- IPv4 loopback 固定端口；
- `HTTP_GET_LOOPBACK_OWNED_PID` readiness；
- 必需的真实 Chromium，同源入口；
- 明确的 subject watch root、预算、停止线和逆序清理；
- 用户显式声明业务断言。

`static-site` 和 `two-process-app` 只能在 `single-webapp` 冻结后分别立合同，不与首发切片并行扩大。

## 5. 全局不变量

1. 所有生成 Profile/Plan 都无 `seal`，文件名包含 `.draft`，workspace manifest 标记
   `DRAFT / NOT_SEALED`。
2. Starter 不暴露 `--auto-seal`、`--auto-run`、`--fix` 或等价捷径。
3. doctor 只报告 `READY / NEEDS_INPUT / UNSUPPORTED`，不得产生产品 `PASS / FAIL`。
4. 自动发现只能列候选；可执行文件、参数、端口、健康路径和业务断言必须来自显式答案。
5. 发现多个服务、非回环依赖、远程数据库、容器、凭据或来源不明进程时停止。
6. 生成失败不能留下半个 workspace；重复生成不能覆盖已有文件。
7. ToolBindings 是本机私有材料；公开示例只能使用仓库内合成路径和占位符。
8. AI 的自然语言不能成为 Seal、Verdict 或运行时权威。
9. Core 和 Workbench 的既有测试必须保持通过；入口层不能借便利性重写冻结历史。

## 6. 资源与实施纪律

- 16 GB Windows 主机默认串行；S0/S1 不引入并发项目探测或后台常驻进程；
- doctor 不联网、不安装依赖、不改 PATH、代理、注册表、服务或全局包；
- 验收服务和 Chromium 必须按 PID、端口、工作目录和所有权清理；
- 每一阶段先冻结合同，再实现，再保存自动化、真实运行、浏览器、安全和零残留事实；
- 发现需要修改 Core Schema 或 Verdict 时，入口层立即停止并单独上浮，不得在适配代码里绕过。

## 7. E0 出口

E0 完成要求：

- 四份入口文档互相一致；
- README 对初学者给出真实、非误导的入口；
- 文档不声称 Starter/Skill 已发布；
- 本地 Markdown 链接检查为 0 缺失；
- `git diff --check`、敏感文本与冻结标签语言检查通过；
- diff 仅属于文档与入口治理。

满足后，S0 才能进入实现。

## 8. E0 冻结事实

- 变更范围仅为 `START_HERE.md`、入口合同、README／里程碑索引和代理治理说明；
- Core 源码、Schema、CLI、Workbench、测试、构建与发布版本均未修改；
- Starter／Skill 均明确标记为尚未发布，未来命令没有被写成当前可用能力；
- Core 安装示例指向 GitHub Release `v0.12.0` 的实际 wheel 资产；
- 本地 Markdown 链接、敏感文本、冻结标签语言和 `git diff --check` 均通过；
- E0 冻结时的下一阶段为 S0，且只能实现 `single-webapp` 的确定性 DRAFT 链。

## 9. S0 冻结事实

- 独立包 `veritrail-starter 0.1.0.dev0` 已实现 `doctor`、`init`、`validate`、`review` 与 `handoff`；
- 五条命令的 stdout 固定为一个版本化 JSON，`handoff.ps1` 只打印命令，不执行 Core；
- `single-webapp` Answers 0.1、严格 Schema、确定性 DRAFT、原子创建、无覆盖、路径与重解析点边界、
  秘密／Shell／非回环拒绝、workspace 双快照和稳定错误码均已有自动化负例；
- Starter 合同测试为 18 项，并在 Python 3.10/3.13 的普通模式与 `python -O` 下各通过一次，共 72 次；
- Core 318/318 回归通过；Workbench 171/171、lint、类型检查和生产构建通过；
- Core wheel、Starter wheel 与 Starter sdist 已分别完成 clean install，包内 Answers Schema 和真实
  Windows 11 `doctor` 均完成读回；
- S0 没有修改 Core Schema、Seal、Verdict 或 Workbench；版本仍为开发版，不能发布；
- 下一阶段为 S1：在仓库内合成单应用上完成真实 doctor/init/review/handoff、人工 Core handoff、
  独立 PASS/FAIL Bundle 与 Workbench 读回。

## 10. S1 冻结事实

- 固定合成 Subject 位于 `examples/starter/single-webapp`，不包含秘密、远程依赖或本机路径；
- PASS 与 FAIL Subject 只在 `app/fact.json` 的 `status` 上不同，预注册期望始终为
  `evidence ready: starter-demo`；
- 两次 Run 共用同一 sealed Profile 与 Plan，但分别重新生成并批准 BootstrapPreview；它们是独立
  验收对，不创建或暗示因果 Comparison；
- 真实链以 `COMPLETED/PASS` 与 `COMPLETED/FAIL` 各生成一份可验证 Bundle；FAIL 的一个根业务
  事实同时派生出 business steps、capture complete 与 screenshot coverage 三项 HARD 失败；
- Catalog 精确读回 2 个 Run、0 个 issue；生产 Workbench 在 1440×960 与 390×844 下完成目录、
  PASS 详情和 FAIL 详情读回，Console、page error、request failure 与 HTTP error 均为 0；
- 两个 Preview、Profile、Plan 与 Bundle 均有 SHA-256 权威；应用与 Catalog 固定端口最终释放，
  owned bootstrap 临时目录为 0；公开验收摘要不包含本机绝对路径；
- `scripts/starter_single_webapp_acceptance.py` 是真实链验收器，不替代 Starter 的人工复核边界；
  Public CI 只在 Core、Starter 与 Workbench 门禁通过后运行它；
- S1 冻结轮中 Core 在 Python 3.10 下为 321/321；Python 3.13 首轮为 320/321，其中唯一失败是
  `sampling_complete=false` 的瞬态资源采样检查，定向 10/10 与第二次完整 321/321 均通过；该首轮事实
  继续保留，不能被后续成功覆盖；
- Starter 合同矩阵在 Python 3.10/3.13 的普通模式与 `python -O` 下共 72/72；Workbench 为
  172/172，lint、类型检查、生产构建和依赖审计均通过；
- S1 没有修改 Core Schema、Seal 或 Verdict；Workbench 仅做 L0 Run 详情装饰框所有权纠偏并增加
  对应回归门禁。下一阶段为 A0：只把冻结的 Starter 命令合同包装成 DRAFT-only Authoring Skill。

## 11. A0 冻结事实

- 实际 Skill 位于 `skills/veritrail-authoring`，身份固定为 `AUTHORING_ASSISTANT`；仓库内容始终按
  不可信数据处理，不读取秘密内容、不执行 Subject、不修复环境；
- Skill 只兼容 `veritrail-starter 0.1.0.dev0`，唯一 Starter 权限为 `doctor`、`init`、`validate`
  与 `review`；`handoff`、Core seal/run、Preview 批准和 Verdict 均不在可调用集合；
- `inspect` 只做有界文件名与元数据盘点；`candidate` 只形成候选；`draft` 只创建不可覆盖的
  `.veritrail` DRAFT；`review-draft` 只重新 validate/review；
- 所有成功草案固定显示 `AUTHORING_ASSISTANT / NOT_SEALED / NOT_RUN / NO_VERDICT`，无匹配 Preset、
  未确认字段、秘密、Shell、非回环、多节点或未知协议均 fail-closed；
- A0 合同、双解释器普通／优化模式、真实 DRAFT 链、提示注入、秘密文件、既有 workspace、稳定文件
  身份替换、敏感信息和安全差异审查事实见
  [A0 冻结事实](62-authoring-skill-a0-facts.md)；
- A0 没有修改 Core Schema、Seal、Verdict、Workbench 或 `v0.12.0`；Skill 仍未独立发布。下一阶段
  为 E1，只处理独立包装、clean install、公共读回与发布边界。

## 12. E1 发布事实

- Starter 与 Authoring Skill 已分别以 `0.1.0` 独立版本化，并由带注释标签
  `starter-v0.1.0`、`authoring-skill-v0.1.0` 固定到提交
  `c7d3c8d2484899b150f47320acafa6553187de5a`；
- 两个 GitHub Release 共包含 7 个固定资产；上传候选、GitHub digest、SHA-256 清单与重新下载副本
  逐字节一致；
- Python 3.10.6 与 3.13.13 均完成 Starter wheel、sdist、Core 0.12.0 公共 wheel 与 Skill ZIP 的
  clean install、官方 Skill 校验和 DRAFT 等价读回；
- 当前 `main` 上的 Public CI 与 Browser Smoke 已重新通过，入口层发布没有移动 Core `v0.12.0`，
  也没有扩大 Seal、Run 或 Verdict 权限；
- E1 的完整合同、资产坐标与公共读回事实见
  [E1 发布合同](63-entry-layer-e1-release-contract.md)和
  [E1 0.1.0 发布说明](64-entry-layer-e1-release-notes.md)。

E1 至此闭环。后续有限 Preset 必须另立合同、独立验收；不得把 E1 的 `single-webapp` 事实外推为
`static-site`、`two-process-app` 或通用项目探测已经受支持。
