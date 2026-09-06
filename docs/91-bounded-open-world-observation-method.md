# 受约束的开放世界观察方法 0.1

> 状态：`METHOD_NOTE / NON_CONTRACTUAL`
>
> 来源：P1 Structured GitHub API Collector 与 P2 Public Render Collector 的合同、反例、实现和冻结事实
>
> 影响层级：方法归纳；不修改 P1/P2 合同，不启动 P3、P4 或 Review Attention R1

## 1. 目的

开放世界采集器面对的是自己不能定义、不能完全控制、也不能一次看全的外部系统。它的任务不是把
现实包装成确定真理，而是在有限权限和明确预算内，保留足以复算、又不强于实际观察的事实。

```text
messy reality
    -> bounded observation
    -> explicit uncertainty
    -> retained Evidence
    -> deterministic judgment under a sealed Plan
```

这份方法来自 GitHub API 与真实 Chromium 的施工经验，但不把 GitHub、Playwright 或某一套实现写成
通用前提。它是一份可复用的设计与审查清单，不是新的产品能力或冻结合同。

## 2. 四类责任必须分开

一个可验证的外部观察能力通常同时包含四层：

| 层 | 只负责什么 | 不应越权到什么 |
| --- | --- | --- |
| 外部平台适配 | 坐标、协议、重定向与平台字段 | Verdict、业务真值 |
| 运行时控制 | 进程、会话、权限、预算、中断与清理 | 内容含义、验收期望 |
| 观察语义 | 作用域、投影、采样、规范化与 coverage | 证据充分性、最终结论 |
| 证据工程 | 身份、provenance、摘要、关联与不可变产物 | 把相关性升级为原子性或独立权威 |

同一部署单元可以高内聚地实现四层，但层间只能传递明确事实，不能共享一份含义不断膨胀的状态对象。
部署在一起不等于权威可以混在一起。

## 3. 先拆开“看起来相同”的命题

开放世界的模型错误经常不会抛异常。它们表现为实现和测试都稳定，但合同说得比证据更强。设计时应
主动检查下列非等价关系：

```text
request succeeded          != observation complete
HTTP 200                   != expected content present
final byte count correct   != producer-side hard limit enforced
browser error              != external platform failure
two equal samples          != declared three-sample stability
same session               != atomic snapshot
same facts                 != same Evidence artifact
test source coordinate     != imported implementation coordinate
wheel import succeeds      != optional capability is independently installable
stable render sample       != immutable render
```

这些区分不是为了增加状态数量，而是为了避免把来源、机制、观察与裁决压成一个布尔值。

## 4. 施工顺序

### 4.1 先冻结权威与身份

在写外部调用前先回答：

- 谁声明期望，谁只提供事实，谁产生 Verdict；
- 坐标、观察规格、请求实例、事实、Evidence 与执行分别由哪个身份表示；
- 哪些来源是替代、覆盖、优先或叠加关系；
- 缺失、冲突、不可观察和不适用分别如何保留。

不得用 `latest`、隐式目录顺序、首个成功结果或方便的 fallback 代替这些关系。

### 4.2 先证明底层机制能够兑现合同

当合同要求硬超时、硬字节预算、进程清理或隔离边界时，先用最小探针证明运行时原语真的支持它。
机制不可行时应回到合同修订，不得在实现中偷偷降级为事后统计、软提示或更宽阈值。

### 4.3 合成证据与现实证据分工

合成 fixture 用于制造稳定、单变量、可重复的边界条件；真实外部系统用于证明实现与当前现实兼容。

```text
synthetic evidence -> mechanism correctness
real-world slice    -> reality compatibility at an observed coordinate
```

两者都需要，且都不能替代另一方。真实探针的成功也不把当前观察扩张为平台永久保证。

### 4.4 把观察者效应归还给观察者

只读路由、请求阻断、重试、超时包装、mock 和测试 harness 都可能制造错误信号。保留信号的同时必须
记录其来源；采集器主动造成的现象不能直接归因给外部平台。

### 4.5 最后才组装 Evidence

先分别钉死请求、运行时、观察和规范化，再组装标准 Evidence。Evidence 只保存实际观察与来源，
不预计算“已通过”“一致”或“足够”的私有结论。充分性、完整性关系与 assertion 由 sealed Plan 和
Core 独立裁决。

## 5. 证据闭环

一个开放世界能力进入冻结候选前，至少需要以下不同层级的证据：

1. 合同矩阵逐项对应测试或明确的现实探针；
2. 单变量负例证明错误不会被成功路径掩盖；
3. 精确源码与实际导入模块属于同一坐标；
4. clean wheel 环境证明安装边界和可选依赖边界；
5. 合成纵向链证明机制可以从请求走到标准 Evidence；
6. 真实外部坐标证明当前实现与现实兼容；
7. 远端门禁、受保护主线、exact-main 与公开渲染分别读回。

门禁数量不是目标。真正的账目是：

```text
contract claim -> retained evidence
```

没有证据的格子保持未证明；新反例可以否决已有绿灯，但只能触发最小必要的模型修订。

## 6. 成本与边界

```text
working collector < bounded collector < verifiable collector
```

增加成本的不是调用 API 或读取 DOM 本身，而是明确权限、预算、身份、不确定性、清理和复算边界。
这种成本只在需要可审计结论时才值得承担；普通低风险抓取器不应机械复制整套结构。

同样，外部系统的所有细节也不应进入合同。抽象边界只保留当前 Claim 所需、能够可靠观察且可以
规范化的事实；其余内容保持范围外、`PARTIAL`、`ERROR` 或冲突，而不是无限增加字段追逐现实。

## 7. 对后继阶段的复用

- **P3**：不再观察 GitHub/Chromium；只消费 P1/P2 已产生的标准 Evidence，验证绑定、充分性、
  integrity、cross-Evidence assertion 与四态 Verdict。
- **P4**：把安装、标签、Release、下载资产与公开读回继续按不同证据层冻结。
- **Review Attention**：复用 provenance、coverage、observer effect、budget ownership 与
  “success 不等于 completeness”等模式；不把 P2 的浏览器实现复制进 R 轨。
- **其他工程**：只复用适用原则。先识别本项目的 authority、runtime primitive 和现实边界，再决定
  哪些检查值得进入合同。

归纳结论是：

> 让模型足够干净以便裁决，同时让不干净的现实仍能以不确定、冲突和来源事实进入模型；抽象，但不编造。
