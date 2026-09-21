# O / Operations Evidence O0：运行事实观察的问题定位

> 身份：`O0_OPERATIONS_EVIDENCE_CANDIDATE_DIRECTION / PRECONSTRUCTION_NOTE /
> NO_IMPLEMENTATION_AUTHORITY`。
>
> 当时坐标：`main@672a1c121aa3f2fb4cd89cb211b9acc7569f479f`，2026-09-21。
>
> 影响层级：`L0_DOCUMENTATION_ONLY`。本文保存问题、边界与反证，不创建正式 O 轨、插件、Provider、
> Schema、运行时、CLI、CI、标签或 Release，也不预编 O1。

## 已见事实与问题

[产品定义](00-product-brief.md)已经把 Core 收敛为 Plan、Subject、Variables、资源边界、Evidence、
Assertions 与 Verdict；它不预设前端、后端、数据库、语言或中间件。[能力地图](114-capability-boundary-and-system-map.md)
也要求跨闭环只通过稳定合同和不可变 Artifact 组合。M5、M9、M10 等冻结能力已经观察过进程、端口、
readiness、资源与 cleanup，但这些能力服务各自的有界运行合同，不等于仓库已经交付一个可拔除、可复用的
Operations Evidence 产品。

今天提出的 O 是一个**候选观察方向**：当真实任务需要解释进程、PID、端口、socket、线程、RSS、heap、
GC、DNS、proxy、TLS、HTTP、容器、中间件、startup、readiness、shutdown、residue 或 recovery 时，能否由
独立 Evidence producer 忠实保存观察值、来源、窗口、覆盖、不确定性与失败，而不把这些领域名词塞进 Core？

`O = Operations Evidence` 是当前候选全名。标题始终写出全名，避免把 `O0` 与 `00` 混淆；包名、标签、
Release 和内部 Provider 名称均未决定。

## 候选责任与权威边界

O 的第一职责是**观察运行事实**。它不是部署器、修复器或自动运维 Agent。

```text
operating reality
    -> bounded observation
    -> versioned facts + provenance + coverage + uncertainty
    -> standard Evidence boundary
    -> sealed assertions evaluated by Core
```

- Reality 继续拥有事实；O 只拥有自己产生的 observation Artifact、provenance 与采集生命周期。
- O 可以报告 `process_rss`、端口 owner、采样窗口、错误与缺失；没有独立冻结语义时，不得直接报告
  `MEMORY_LEAK=true`、`HEALTHY=true` 或系统 `PASS`。
- O 默认不拥有 deploy、restart、kill、repair、recovery、production write、凭据或外部系统状态。未来若真实
  任务需要动作能力，必须另行定义权限、幂等、补偿与恢复边界，不能从“能看见”继承“能修改”。
- O 不向 Core 增加 `dns_status`、`jvm_gc`、`container_health` 等领域字段。若现有公共 Evidence 合同能诚实承载
  事实，就通过 adapter 使用；不能承载时，先证明是通用合同缺口，再考虑独立兼容合同。
- O 可以消费版本化输入或外部 Artifact，但不能导入 P、R、T、Q 私有实现、修改其状态，或让解释覆盖原事实。
- 删除 O 后，Core Verdict、P Evidence、R Artifact、T 的测试事实与 Q 的证明义务必须保持原语义；系统只失去
  对应运行观察能力。

## 为什么暂时与 T 分开记忆

[T0](181-t0-test-evidence-problem-framing.md)面对 test discovery、runner、fixture、retry 与报告身份。O 更接近
运行环境和系统状态的观察。两者可能共享时间窗口、进程或资源事实，也可能最终共用一部分 Provider；这种
重叠不足以证明应合并为一个插件。

真正施工前要重新问：它们是否拥有相同 state owner、权限、生命周期、失败恢复和发行节奏。若测试执行开始
拥有 selection、command、retry 与 fixture state，而 O 仍保持只读观察，两条闭环应继续分开；若真实反例证明
它们只维护同一个不可分 invariant，则应允许收敛。边界由 invariant 决定，不由“运维/测试”两个名词决定。

## 最小反证与重开条件

以下问题用于检查 Core 的通用性和 O 的必要性，不是已授权测试矩阵：

1. 没有前端、数据库或浏览器，只有 process owner、listener、natural exit、port release 与 residue，现有公共
   Plan/Evidence/Assertion 是否能诚实表达？
2. 只改变 proxy 路径，观察 DNS、direct HTTP、proxy HTTP、TLS 与错误归因时，是否必须伪造 Web 项目字段？
3. 只改变 workload，保存 thread/RSS/heap/GC 时间窗并恢复 baseline 时，插件能否只报告事实而不偷判 leak？
4. O 采集失败或部分不可用时，coverage/UNKNOWN 是否继续可见，还是被空值误读成正常？
5. 删除 O 后，其他轨道是否仍可独立运行且语义不变？

若现有有界 runner 和少量 adapter 已足够，独立 O 插件可以不成立。若反例只能通过虚构字段、领域布尔值或
Core 私有导入才能表达，才有资格从新的 exact main 起草最小合同。任何 Core 变更都必须晚于插件侧反例，且只
修复被证明的通用缺口。

## 当前非授权

本文不授权 Provider 树、采样频率、agent、daemon、数据库、凭据、远程命令、自动恢复、跨平台承诺、公共
Schema、Core compatibility change、O1 或产品发布。`ProcessProvider / NetworkProvider / JvmProvider /
ContainerProvider / MiddlewareProvider` 只可作为问题示例，不能从本文推成施工清单。

当前串行施工坐标仍回到 Review Attention R 的冻结后 system audit。O0 保存记忆，不保存未来命令。
