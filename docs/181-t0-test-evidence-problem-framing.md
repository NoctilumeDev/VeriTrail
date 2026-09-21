# T / Test Evidence T0：测试事实观察的问题定位

> 身份：`T0_TEST_EVIDENCE_CANDIDATE_DIRECTION / PRECONSTRUCTION_NOTE /
> NO_IMPLEMENTATION_AUTHORITY`。
>
> 当时坐标：`main@672a1c121aa3f2fb4cd89cb211b9acc7569f479f`，2026-09-21。
>
> 影响层级：`L0_DOCUMENTATION_ONLY`。本文保存问题、边界与反证，不创建正式 T 轨、插件、runner、
> Schema、运行时、CLI、CI、标签或 Release，也不预编 T1。

## 已见事实与问题

VeriTrail 已在本仓库使用 unittest、Playwright、前端回归、wheel-only 与 clean-install 门禁，也多次保留
“测试真正执行后失败”“测试发现/环境尚未成立”“后继 PASS 不解释早先 FAIL”等不同事实。但这些测试事实
目前分散在 CI、runner 输出、维护文档和验收 Bundle 中；它们不等于已经存在一个通用 Test Evidence 产品。

今天提出的 T 是一个**候选观察方向**：对 pytest、unittest、JUnit、Playwright、Maven 或其他 runner，能否
保存 exact source/environment、runner identity、discovery、selection、execution、fixture、attempt/retry、
exit code、passed/failed/skipped、duration、report 与 coverage Artifact 的事实身份，并让 sealed Plan 与 Core
决定这些事实能支持什么？

`T = Test Evidence` 是当前候选全名。这里刻意不用 `Test Execution`：T0 尚未证明测试选择、命令执行、重试
或 fixture 控制应该属于同一个插件。包名、标签、Release 与 Provider 名称均未决定。

## 候选责任与权威边界

```text
test runner / report / environment
    -> bounded observation
    -> execution facts + provenance + coverage + uncertainty
    -> standard Evidence boundary
    -> sealed assertions evaluated by Core
```

- T 首先只拥有自己产生的测试 observation Artifact、来源与采集生命周期；runner 和被测系统继续拥有各自状态。
- `exit_code=0`、全部已执行用例通过或 coverage 百分比达到阈值，都不能由 T 直接提升为系统 `PASS`。它们只证明
  明确 test universe、selection、source state 与环境坐标下的那一层事实。
- test discovery complete、selected set complete、execution complete 与 project assurance complete 是不同命题；
  未发现、未选择、未执行、skip、fixture error 和 unavailable 必须分别保留。
- retry/attempt identity 不得洗掉首败。后继 PASS 可以成为新的观察，不能自动解释或覆盖早先 FAIL。
- 测试工具的 line/branch/function coverage 与 Review Attention R 的 Relation/Slice observation coverage 是不同
  分母、不同 owner、不同 authority，不能共用一个裸 `coverage` 结论。
- T 不拥有 Core Verdict、Gate 定义、Q 的 verification schedule、R 的 AttentionProposal、O 的运行状态、
  CI 平台事实或仓库写权限。

## 执行权仍是 UNKNOWN

测试观察通常接近测试执行，但接近不等于同一所有权。T0 不预先决定以下能力归属：

```text
test selection
command execution
fixture setup / teardown
retry policy
sharding / parallelism
coverage production
artifact publication
```

如果未来 T 只读取既有报告，它可以保持 observer；如果它必须启动 runner，则 command ownership、预算、取消、
cleanup、attempt admission 与 report publication 都需要独立合同。若 Q 将来安排验证顺序，T 可以执行已授权 lane
或发布事实，但不能因此获得跳 Gate、缩小 test universe 或重解释历史结果的权力。

## 与 O 的边界

[O0](180-o0-operations-evidence-problem-framing.md)关心机器和系统运行时发生了什么；T0 关心哪些测试在什么
source/environment 下被发现、选择、执行并产生何种结果。一次测试可以同时产生：

```text
T fact: test_x failed during fixture setup
O fact: child process never owned the declared port
```

两条事实可以通过显式 identity 关联，但任何一方都不能原地改写另一方。删除 T 后，O 仍能观察 process/port；
删除 O 后，T 仍能保存 runner/report，只是不能声称具有缺失的运行诊断。是否共用实现必须等待真实 invariant，
不能因同一次 CI 运行就合并状态机。

## 最小反证与重开条件

1. runner `COMPLETED / exit 0`，但 required test 未被发现或未被选择：能否阻止“全部通过”的扩大解释？
2. discovered set 非空，部分 test 没有 execution outcome：能否保留 obligation 未履行，而不是从零 failure 猜 PASS？
3. attempt 1 FAIL、attempt 2 PASS：两次身份能否同时保留，且不会把 retry 变成首败解释？
4. fixture setup、collector、test body、teardown 与 report publication 分别失败时，能否定位层级而不揉成一个 FAIL？
5. current-source tests 通过、installed-product topology 未观察时，能否阻止来源正确被升级为安装拓扑等同？
6. tool coverage 高但 R observation domain 未闭合时，两个 coverage 是否仍保持独立？

若现有 CI Artifact 与小型 adapter 已足够，独立 T 插件可以不成立。只有真实任务证明 discovery、attempt、fixture
或 report identity 无法由既有公共边界诚实保存时，才从新的 exact main 起草合同。

## 当前非授权

本文不授权 runner、命令执行、selection、retry、fixture 控制、sharding、缓存、coverage 合并、CI 改动、
公共 Schema、Core compatibility change、T1 或产品发布。`PytestProvider / JUnitProvider /
PlaywrightTestProvider / MavenTestProvider / CoverageProvider` 只可作为问题示例，不能从本文推成施工清单。

当前串行施工坐标仍回到 Review Attention R 的冻结后 system audit。T0 保存记忆，不保存未来命令。
