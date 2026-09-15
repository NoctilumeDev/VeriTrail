# Product Delivery D0：真实任务入口的问题定位

> 身份：`D0_CANDIDATE_DIRECTION / PRECONSTRUCTION_NOTE / NO_IMPLEMENTATION_AUTHORITY`。
>
> 当时坐标：`origin/main@301f5248b77c67284b5e52bf287c23f286590e6b`，2026-09-15。
>
> 影响层级：`L0_DOCUMENTATION_ONLY`。本文记录今天为何提出 D，不创建正式 D 轨、合同、源码、UI、CLI、Schema、CI、标签或 Release；不预编 D1。

## 已见事实与问题

[README](../README.md)与[首次使用入口](../START_HERE.md)已经提供发布的 Core `0.13.0`、Starter/Authoring Skill `0.2.0`、GitHub Evidence `0.1.0` 和只读 Workbench。D 不能以“尚未交付产品”为前提重做这些能力。[Review Attention R1](113-r1-deterministic-semantic-slice-contract.md)仍在结构事实、Relation、Slice 与 Coverage 的分步闭环中；它尚未交付人工注意力地图。

今天提出的 D 是一个**候选问题方向**：当真实用户带着自己的任务进入时，安装、选择有界入口、复核草案、由人 Seal、运行、理解 Bundle/失败、恢复或请求补证之间，是否存在现有入口无法清楚承接的断点？如果有，应怎样交付一个诚实的任务入口，而不让展示层取得 Seal、Evidence 来源或 Core Verdict 权？“产品壳”是对此问题的临时称呼，不是已决定的架构。

## 当前判断的边界

- 当前只把 Review Attention R 作为**唯一串行施工主线**；R 自己仍须逐项遵守现有合同门禁，[Relation 合同](165-r1-relation-derivation-authority-and-operand-continuity-contract.md)现在只是候选。优先顺序 `R → D → Cu → Q` 表示今天打算先从哪里取得问题证据，不表示 R0–R6 必须全部结束，也不是 D、Cu、Q 的实现授权。
- D 若消费 Review Artifact，须在真正开始时重新读取当时可用的 R 产物与真实用户任务。围绕已发布 Core/Entry 的交付问题也可能独立出现，不能为了字母顺序伪造 R 依赖。
- Starter 的 `DRAFT / NOT SEALED`、Workbench 的只读性质、人类 Seal/最终处置和 Core 独立 Verdict 不因 D 获得新权力。
- 现有入口可能已经足够；也可能只需改进某个既有入口，而无需独立 D 轨。今天没有使用路径或安装失败数据可证明哪一种成立。

## 未知、反证与重开条件

尚不知道首个具体用户任务、角色、机器环境和可消费 R Artifact；不知道用户究竟在安装、起草、Seal、运行、读懂失败还是恢复处迷路；也不知道完整有界串行验证的等待是否可接受。未来若真实任务表明现有入口已足够，或问题可以在现有产品边界内更小地解决，独立 D 方向应收敛。若串行路径因真实资源/等待事实不能使用，也应重新判断 Q 的时机，而不是按今天的顺序硬等。

只有在真实任务、当前 exact main、当时 R/Entry/Core 产物和环境事实重新读回后，才有资格讨论独立合同与最小交付。本文保存当时的问题和判断，不给未来施工命令。既有 [Q0 蓝图冻结记录](119-q0-verification-scheduling-final-freeze-closure.md)不因新的优先顺序被改写。
