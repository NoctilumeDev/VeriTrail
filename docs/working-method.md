# VeriTrail 证据反馈工作法

> 适用范围：所有 VeriTrail 合同、实现、维护、状态发布、公开读回与下一步选择。
>
> **本文件定义工作方法，不定义项目事实。当前 SHA、状态、authority 与下一合法 seam 必须始终从 exact main 和保留证据重建。**
>
> 仓库入口：[AGENTS.md](../AGENTS.md)。

## 1. 两层结构

VeriTrail 不是按 roadmap 或文档编号推进的线性流水线。每一刀都由两层过程控制：

```text
CONTROL LOOP
  决定“现在该不该做这一刀”

QUALIFICATION PIPELINE
  决定“做完以后凭什么算成立”
```

`publish state -> next document` 不是合法调度规则。状态发布只产生一项新事实；新事实必须重新进入
`CONTROL LOOP`。

## 2. 外层：证据反馈控制回路

### 2.1 定 exact 坐标

施工前重新核对：

```text
remote exact main
local checkout / active worktree
parallel or open PRs
commit / tree / final bytes
Plan / session / attempt
package / distribution identity
public project claims
```

聊天、摘要和旧文档只提供检索线索，不能替代当前坐标。

### 2.2 认领当前真正的问题

明确区分：

```text
frozen upstream facts
current candidate
mandatory read obligations
explicitly deferred capabilities
```

roadmap 中“原计划的下一步”只表示旧 exact world 的候选判断，不自动成为当前施工权。

### 2.3 复核旧判断与反证

重新检查旧结论依赖的前提，并把新观察分成：

```text
real contradiction
unproved seam
unknown
```

真实矛盾出现时先保存现场，不先修。先判断它属于产品、合同、fixture、test-support topology、环境、网络、
证明设施还是 operator/setup。

### 2.4 只授予仍成立的最小资格

每进入一个 seam，先问：

```text
denominator 谁拥有？
classification 谁拥有？
fulfillment 谁拥有？
admission / disposition 谁拥有？
谁只能观察，不能认证？
```

若前提失效，只显式 reopen 或 version bump 被击穿的最小边界。若前提仍成立，本阶段也必须取得自己的资格，
不能从上游绿灯继承。

### 2.5 新事实反馈整体状态

形成新事实以后：

1. 保留首败、原始 attempt 与未知归因；
2. 核对 candidate、merge、exact-main 与 product observation 身份；
3. 复核 README、AGENTS、milestones、合同正文、导航、图片及下游表述；
4. 修正 publication lag 或 drift，但不扩张事实强度；
5. 回到 2.1，重新判断下一合法 seam。

因此：

```text
document number != scheduler
README != next-step command
CI green != semantic state upgrade
previously planned next step != currently authorized next step
```

## 3. 内层：单次施工资格链

只有外层回路重新确认当前 seam 后，才进入：

```text
final bytes
    -> this layer's declared local qualification gates
    -> original PR gates
    -> protected merge
    -> new exact-main gates
    -> fresh installed-product observation
    -> independent reconciliation
    -> publish state
    -> return to CONTROL LOOP
```

Python 3.10 / 3.13、normal / `-O` 是当前 R1 某些层声明的具体矩阵，不是整个项目永久不变的唯一矩阵。稳定规则是：
**最终字节必须重新经过该层声明的完整资格门。**

publication 可以预先写入条件化 target marker；只有它冻结的全部生效条件成立后，target state 才成为事实。
本地 checkout fast-forward、归档或工作树整理属于 housekeeping，除非冻结合同明确规定，否则不得事后追加成
qualification gate。

## 4. 默认施工纪律

### 4.1 测试只作 witness

测试通过只证明指定 exact world 未被这些反例击穿。测试不能：

- 扩大合同；
- 解释未冻结的 reason；
- 授予下一层 authority；
- 把 execution completion 升格为 fulfillment；
- 把 candidate 升格为 frozen。

### 4.2 资格绑定 exact coordinate

SHA、tree、final bytes、Plan、session、attempt、package identity 与 readback identity 各自只证明自己的世界。
相同 patch、输出、semantic result 或 digest 不自动继承另一世界的 qualification、admission 或 continuation。

### 4.3 首败与后继观察并存

```text
FAIL / ERROR / CANCELLED / setup failure / UNKNOWN
    -> preserve identity

new independent observation
    -> may PASS

later PASS
    != erase or explain prior history
```

归因变化可以修正“失败属于哪一层”，不能改写失败是否发生。

### 4.4 分离不同施工面

合同、runtime、Schema、测试维护、状态发布与展示同步默认分开。测试或证明地基有缺口时，使用独立 maintenance
PR；maintenance qualified 后，原 semantic patch 必须绑定新的 exact main 并重新受审。

### 4.5 复用世界，不复用权力

允许按冻结合同复用 copy-owned immutable exact inputs；attempt、BudgetContext、continuation、ProviderRun、
qualification、admission、closure 与 disposition authority 必须重新取得。

### 4.6 private proof 先于 public surface

先证明 authority、denominator、fulfillment 与 reconciliation 可以形成 private closed proof，再决定 public
Schema、carrier、Evidence、Manifest、publisher 或 Bundle。既有 public shape 不反向授予语义 authority。

### 4.7 工具与环境不污染主机

代理按命令临时注入，不改全局 Git 或系统代理。匿名 installed-product readback 必须清理 token、`PYTHONPATH`
及其他可能改变观察面的环境。诊断路径不得替代正式产品路径。

## 5. 五个必须分开的状态

任何汇报、文档与实现都必须区分：

```text
content correct
execution complete
qualification established
state effective
next step authorized
```

VeriTrail 的辨识度不来自重复运行更多测试，而来自对这五件事及其 authority 的机械分离。

## 6. 压缩或模型切换后的恢复顺序

1. 读取本文件与 AGENTS；
2. 获取远端 exact main、活动 worktree/PR 与本地状态；
3. 从冻结合同、原始 CI attempt、Artifact 和 fresh readback 恢复当前事实；
4. 把聊天摘要当作待核线索；
5. 重新执行 CONTROL LOOP，不能从摘要中的“下一步”直接开工。
