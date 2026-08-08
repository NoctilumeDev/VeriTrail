# 05. M1 资源与环境预检

## 状态

`FROZEN`。M1 已在可寻址提交上完成两套 Python 自动化、M0 兼容回归、三类真实主机预检、
证据包逐字节核验、敏感扫描和残留检查。M2 可以开始规划，但不得跳过自己的验收合同。

## 目标问题

M1 只回答：

> 在启动被测工作负载前，当前主机是否满足封存计划中的资源、安全与清洁起点？

它不执行被测项目命令，不启动或停止服务，不制造真实内存压力，也不声称已经具备运行中
持续监控和自动清理能力。后续执行编排器可以复用 M1 的采样与决策函数，但不属于本里程碑。

## 影响层级与消费者

- 声明层级：`L2_CONTRACT`；
- 所有者：VeriTrail Core；
- 新契约：`ExperimentPlan 0.2`、`runtime.preflight` Evidence；
- 直接消费者：计划校验器、CLI、证据导入器、JSON/Markdown 报告和测试；
- 后续消费者：执行编排器、SQLite 索引、Vue Workbench；
- 不在范围：浏览器、项目命令、服务控制、Docker 控制、系统网络修改和 SQLite。

如果实现需要改变 M0 Verdict 优先级、Evidence 0.1 或 Report 0.1，则实际 diff 已越过声明范围，
必须停止并重新评审，而不是把破坏性修改藏在资源功能中。

## 0.1 / 0.2 兼容矩阵

M0 的 `ExperimentPlan 0.1` 是冻结契约，不原地增加字段：

| 操作 | Plan 0.1 | Plan 0.2 |
| --- | --- | --- |
| `seal` | 保持原行为 | 支持并封存预检策略 |
| `evaluate` | 保持原行为 | 支持导入或生成的预检证据 |
| `preflight` | 明确拒绝并解释需升级 | 执行本机只读预检 |

`ExperimentPlan 0.2` 保留 M0 的主体、基线、变量、断言、负载、变更范围和复现/清理字段；
`resource_budget` 只保留证据文件上限，真实预检阈值进入新的 `preflight` 对象。这样不继续沿用
0.1 中语义不够清楚的 `memory_soft_mb / memory_hard_mb`。

## 预检策略

`preflight` 必须在计划封存前声明：

| 字段 | 语义 |
| --- | --- |
| `sample_count` | 启动前采样次数，范围 1–20 |
| `sampling_interval_ms` | 样本间隔，范围 0–5000 ms |
| `hard_breach_grace_samples` | 内存硬线连续命中多少次才中止 |
| `available_memory_soft_min_mb` | 可用内存低于此值时停止升压 |
| `available_memory_hard_min_mb` | 可用内存低于此值时中止；不得高于软线 |
| `disk_free_hard_min_mb` | 输出所在卷的最小可用空间 |
| `collector_rss_hard_max_mb` | VeriTrail 采集进程自身 RSS 硬上限 |
| `observer_rss_delta_soft_max_mb` | 采样期间采集器 RSS 增量软上限 |
| `ports` | 最多 32 个回环 TCP 端口及期望 `FREE / LISTENING` 状态 |
| `require_clean_staging` | 输出父目录不得残留 `.veritrail-*` 临时目录 |

软内存线必须大于或等于硬内存线；宽限样本数不得超过采样数；策略总等待时间必须有界。
阈值不接受 CLI 临时覆盖，观察结果后改变阈值必须生成 Plan 0.2 的新版本和新哈希。

## 只读采集边界

M1 使用 Python 标准库直接读取或探测：

- 操作系统、架构、Python 版本、逻辑 CPU、总内存和可用内存；
- 输出所在卷的总量与可用空间；
- VeriTrail 当前进程 RSS、采样耗时和 RSS 增量；
- HTTP/HTTPS/ALL/NO_PROXY 是否存在，只记录布尔值，不读取或保存代理地址；
- 计划显式列出的回环 TCP 端口是否可连接；
- 输出父目录是否有 VeriTrail 临时组装残留。

不采集用户名、主机名、IP、代理值、环境变量值、命令行、全部进程清单或全部监听端口。
端口探测只连接 `127.0.0.1`，不绑定、占用或关闭端口。M1 不读取 `.env`，不调用 Shell，
不启动/停止服务、容器或进程，也不修改防火墙、代理和系统参数。

## 决策状态机

资源决策独立于最终 Verdict：

```text
samples + port checks + staging check
  -> hard structural violation             -> ABORT
  -> consecutive hard resource breach      -> ABORT
  -> soft memory/observer threshold breach -> STOP_ESCALATION
  -> otherwise                             -> PROCEED
```

- `PROCEED`：当前起点允许进入下一阶段；不担保后续负载永不超限。
- `STOP_ESCALATION`：不增加负载或新并行度；本次预检本身可正常完成并保留证据。
- `ABORT`：不得启动工作负载，证据包的 ExecutionStatus 为 `ABORTED`。

资源 `ABORT` 不自动产生产品 `FAIL`。若中止前没有独立证据证明硬性不变量失败，Verdict 必须
保持 `PENDING`。采集失败写入 `collection_errors` 并安全中止，不能伪造完整快照。

## `runtime.preflight` 证据

生成的 Evidence 0.1 至少包含：

- 决策、原因码、采集完成状态和采集器版本；
- 脱敏环境摘要与稳定环境指纹；
- 每个样本的 UTC 时间、可用/总内存、卷空间和采集器 RSS；
- 软/硬阈值命中、最大连续硬线次数和端口结果；
- 观察者起始/峰值 RSS 与增量；
- 临时目录残留计数；
- 仅针对计划已声明名称生成的受控/干扰变量观察。

证据进入 M0 已冻结的脱敏、哈希、清单和报告链路。报告及清单只保存逻辑名称和相对路径，
不保存实际输出目录或卷路径。

## 自动化验收矩阵

- 0.1 的 21 项冻结测试继续在 Python 3.10 与 3.13 通过；
- 0.1 计划不能调用 `preflight`，错误必须明确且不产生半成品；
- 0.2 计划可稳定封存，修改任一阈值后原 Seal 失效；
- 不合法的软/硬关系、宽限次数、采样时长、重复/越界端口被拒绝；
- 合成样本分别确定地产生 `PROCEED / STOP_ESCALATION / ABORT`；
- 硬线只在要求的连续样本数达到后触发；非连续尖峰不能被误判为连续超限；
- 结构污染立即 `ABORT`，包括端口状态不符和临时目录残留；
- 端口测试使用测试进程自己的回环监听并在结束后释放；
- 代理只输出是否配置，构造的代理值不会进入证据包；
- 工具 RSS 与宿主资源分开，观察者增量越界只产生 `STOP_ESCALATION`；
- `ABORT` 生成 `ABORTED + PENDING`，不自动变成 `FAIL`；
- 证据与报告哈希、脱敏、防覆盖和相对路径约束继续成立。

## 真实运行退出条件

在干净提交和当前 16 GB Windows 主机上串行执行：

1. 使用保守阈值产生一次真实 `PROCEED`；
2. 只提高软线、保持硬线安全，产生一次真实 `STOP_ESCALATION`；
3. 使用不可能满足的预注册硬线产生一次安全 `ABORTED + PENDING`，不分配额外内存；
4. 三个 Run 的环境、资源、观察者、决策、报告和清单互相一致；
5. 所有清单文件逐字节 SHA-256 通过，敏感信息扫描 0 命中；
6. 运行后没有 `.veritrail-*`、测试监听、子进程或端口残留；
7. Git 工作区保持干净，冻结提交与标签可从 GitHub 读回。

只有以上全部成立，M1 才能从 `PLANNED` 依次推进到 `FROZEN`。M2 在此之前只允许规划，
不得实现。

## 冻结记录

验收日期：2026-08-09（Asia/Shanghai）。

- 代码基线：`21d555cf1a8d5b4f3bc9430b4241c3f70ff0d48f`；
- 版本：`0.2.0.dev1`；
- Python 3.10.6：42 项测试通过；
- Python 3.13.13：42 项测试通过；
- M0 兼容：Plan 0.1 哈希保持
  `90235a18c59e9f30cd2aa519d281a4fdb18f04e83bdf2fcc5ff98770dba8a2b8`，真实 Run 为 `PASS`；
- `PROCEED` Plan 哈希：`df1966bbab8e1f6c0288525747ff96bd5c7d3e26120dbfafea8f27367324f41b`；
- `STOP_ESCALATION` Plan 哈希：`e2ef3c20c6f278d8535c3210a10b0f0edd738452fdd1dedd42b480b5e231ad84`；
- `ABORT` Plan 哈希：`314c4590de0a58debf27dceba7deddedcb744cd307126c40ffb3150e7f38318a`，
  输出为 `ABORTED + PENDING`；
- 三个真实 M1 Run 各采集 3 个样本，最低可用内存约 8275.922 MiB，采集器 RSS 峰值不超过
  18.398 MiB，观测增量不超过 0.117 MiB，单次采集不超过 172 ms；
- M1 证据包 15 个文件、M0 兼容包 5 个文件逐字节 SHA-256 核验通过；
- 持久化敏感信息扫描 0 命中，`.veritrail-*` 残留 0，复验后 Git 工作区干净。

本地运行包位于 Git 忽略的 `artifacts/`，不进入仓库。以上性能数字只描述本次 16 GB Windows
主机上的采集器开销，不构成其他机器或后续工作负载的容量结论。
