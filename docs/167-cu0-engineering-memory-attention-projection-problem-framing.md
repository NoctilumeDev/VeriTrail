# Cu / Curation Cu0：工程记忆注意力投影的问题定位

> 身份：`CU0_CANDIDATE_DIRECTION / PRECONSTRUCTION_NOTE / NO_IMPLEMENTATION_AUTHORITY`。
>
> 当时坐标：`origin/main@301f5248b77c67284b5e52bf287c23f286590e6b`，2026-09-15。
>
> 影响层级：`L0_DOCUMENTATION_ONLY`。本文记录今天为何提出 Cu，不创建正式跨项目产品、算法、运行时、Artifact Schema、CI、标签或 Release；不预编 Cu1。

## 已见事实与问题

[README 阅读路径](../README.md#阅读路径)把 Review Attention 的多份合同、审计、实现候选和冻结发布连续列出；[AGENTS](../AGENTS.md)另有开始工作前的必读义务。文档数量本身不是缺陷，但针对 Relation 等具体接手任务，线性编号使直接合同、反证审计、冻结上游和历史材料混在一条长路径中。历史身份也有时间层次：例如[文档 160](160-r1-multi-provider-applicability-and-fact-composition-contract.md)保留起草时的 candidate 标记，后继[文档 163](163-r1-multi-provider-fact-composition-freeze-publication.md)发布冻结事实；不能为了当前导航而回写文档 160 的历史状态。

今天观察到的是**发现成本和误读风险**，尚未测得用户/Agent 因此产生的耗时或错误率。Cu 是暂用的候选命名；它面对的是有限注意力如何阅读工程记忆，不等同于整理 docs 文件夹、全局“正确排序”或用相似度重判权威。历史的一次性 Core release `C` 和 M10 topology `C0–C3` 已占用裸 `C`，因此只用全名 `Cu / Curation`、`Cu0`，不借用那些状态机。

## 候选方向与不可移动边界

给定**具体任务解释**和**精确工程状态**，可以研究一份只读、任务相关的导航/注意力投影，说明哪些原始文档先读、为什么、依据哪条引用或状态来源，并保留一次投影自身的条件和历史。它只组织阅读，不创造新的项目事实。

- 原始文档拥有内容，Git 拥有历史身份，项目状态文档及其证据链拥有状态声明；Cu 不把 candidate 改成 frozen，不重新裁决证据或 Verdict。
- 排序不改变权威，却会影响人最终看到什么；所以解释排名仍不够，还须暴露**定义的候选全集**、实际扫描范围、未看见的对象、看见但排除的对象和低排名对象。扫描覆盖率不证明候选全集已覆盖全部工程记忆。
- 任务由人给出或由 Agent 解释时，解释本身应可见、可纠正；一个精确算法也可能忠实排列错误任务。
- 强制读取义务不参与相关性竞争。现有 AGENTS 要求的 README 与文档 00–03 等必读内容不能被 Cu 降权或省略；任务相关材料才适合在满足硬约束后排序。
- Cu 关心“先看什么”；[Review Attention R](85-post-core-review-attention-plugin-plan.md)关心源码审查注意力；[Q0](119-q0-verification-scheduling-final-freeze-closure.md)只建模既定证明义务的调度。Cu 的相关性不能成为 Q 跳 Gate 或复用旧 Evidence 的依据。

## 未知、反证与重开条件

尚未定义首次真实任务的文档宇宙边界，也不知道静态索引、人工导航还是复杂推荐是否值得；不知道哪些平台证据或仓库外材料应纳入；不知道跨项目化是否有真实消费方。若现有阅读路径配合少量人工入口就能可靠完成接手，或 Cu 的候选集/过滤机制反而隐藏关键反证，就不应因为“文档很多”启动算法。

当前只有 Review Attention R 是串行施工主线。D0 的[真实任务入口候选](166-d0-product-delivery-problem-framing.md)可能将来产生更直接的阅读行为证据，但这不是 Cu 的固定技术依赖。届时必须从新的 exact main、真实任务、输入宇宙与遗漏事实重新判断；本文保存当时的问题，不授权 Cu 实现、排名规则冻结或跨项目产品化。
