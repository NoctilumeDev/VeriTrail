# M14 安全整改与重新基线合同 0.1

> 状态：`REMEDIATION_IMPLEMENTED / BASELINE_PENDING`
>
> 日期：2026-08-23
>
> 上位合同：[M14 整改后终局复验与发布收束合同 0.1](54-m14-final-validation-and-release-contract.md)
>
> 第一轮触发扫描：Codex Security Standard Scan `95302e1c-5e1b-4d1d-9f0d-6da96e4c7237`
>
> 第二轮触发扫描：Codex Security Standard Scan `c029be23-8820-4569-9c57-6b6dd9171588`
>
> 整改工作树差异复审：Codex Security Diff Scan `b5be844f-eb7a-4e2d-8351-424694bda6bb`

## 1. 为什么必须重新基线

M14 入口候选 `457ca3fc3c0817f02fb5b237d21aad80dae9ccdf` 之后的第一轮全仓安全扫描确认了 7 项可报告
缺陷：3 项高风险、4 项中风险。第一轮整改完成后，第二轮完整扫描又确认 8 项相邻缺陷：2 项高风险、
5 项中风险、1 项低风险。两轮合计 15 项，触及读取快照、监听器所有权、Catalog 数据库身份、派生分析
权威、解释器参数语义、资源总预算、同步图片校验和惰性文本呈现，属于原 M14 合同明确禁止用测试、
CSS 或后置文档掩盖的 L2/L3 边界问题。

因此：

- 入口候选及其既有 M14 自身目标、InkNarratives 验收产物只能作为历史诊断事实；
- 这些历史产物不得被拼接进最终稳定版结论，也不得作为 `v0.12.0` 的 Release 证据；
- M14 状态退回 `VALIDATING`，原候选基线失效；
- 本合同只授权关闭两轮扫描已验证的 15 条攻击路径、补充强等价回归并建立新的不可移动候选基线；
- Schema 的版本、字段形状、Verdict、ExecutionStatus、支持矩阵、目标 ref 和预注册公共出口保持不变；
  唯一获准的 Schema 改动是为既有 `max_artifact_bytes` 增加 Core 同值的 `10 MiB` 固定上限，属于
  安全收紧，不新增字段、不扩大能力，也不改写已冻结合法样例。

整改实现与本文进入同一个候选提交。由于 Git 提交不能在自己的内容中预写自身 SHA，精确整改基线
必须由紧随其后的“基线绑定提交”写入本文及 M14 验收器；该绑定提交不得再修改 Core 或 Schema。
绑定提交推送并从 GitHub 读回前，不允许运行新的终局矩阵。

## 2. 已关闭攻击路径

| ID | 原缺陷 | 整改后的唯一边界 | 强等价回归 |
| --- | --- | --- | --- |
| SEC-M14-001 | readiness 通过后至浏览器采集期间，回环端口可能被非 Job 进程接管 | readiness 产出精确监听器身份；浏览器请求、WebSocket、步骤边界和采集结束均复核 PID、Job、根进程与进程集合连续性，任何漂移 fail closed | readiness 后、导航间和采集后替换监听器均拒绝；稳定控制组通过 |
| SEC-M14-002 | Comparison、Pairing、Batch 验证 Bundle 后按路径重开文件，可能出现“旧摘要 + 新语义” | `validate_bundle` 返回不可变 owned bytes/解析快照；全部派生分析只消费该快照，报告内路径再次经过 containment 校验 | 验证后替换 plan/report/evidence 不改变快照或被拒绝 |
| SEC-M14-003 | `x-api-key` 及 `{name, value}` 结构化认证头可能逃过脱敏 | 对敏感 header 名称和 header-pair 结构进行语义化脱敏，同时保留普通业务 `value` | opaque API key、Authorization、Cookie 与普通 Content-Type 对照组 |
| SEC-M14-004 | 动态值可逃逸 Markdown 行内代码或激活链接、图片 | reporting、comparison、pairing、batching 共用上下文安全的 Markdown 文本与代码编码器 | 反引号、链接、图片、HTML、换行组合只作为惰性数据呈现 |
| SEC-M14-005 | Catalog 可保留超长 run ID 和无总量预算字符串 | 导入端复用标识符约束，并限制单字段、集合、单 Bundle、Catalog retained metadata 和 API 响应预算 | 65 字符/大字符串/累计超额拒绝，64 字符及最大合法页通过 |
| SEC-M14-006 | loopback API 启动校验后按公共路径重开 SQLite | 启动时固定已验证数据库快照，服务生命周期内只使用同一私有 immutable read-only 连接并串行保护查询 | 启动后替换公共 SQLite 不改变 API 权威或扩大文件授权 |
| SEC-M14-007 | 通用 JSON loader 在验证前无界分配，部分调用存在 stat/open 竞态 | 所有路径输入统一使用普通、非 reparse、单链接、限长、单 handle、读前后身份稳定的 owned-byte loader | 超限、增长、替换、symlink/reparse/hardlink 和合法边界控制组 |
| SEC-M14-008 | CPython 短选项簇可把 `c` 隐藏在同一参数中，绕过行内代码禁令 | 按 CPython 的短选项消费语义解析最终 argv；显式处理 `-m`、`-W`、`-X`、`--` 与选项簇，任何 `c` 入口 fail closed | 合法模块入口、参数消费边界、`-ic`/`-qc` 与混合选项簇控制组 |
| SEC-M14-009 | 已验证 Catalog bytes 经可替换临时路径再次打开，形成 TOCTOU | 精确 Schema、行/字段预算和逻辑摘要通过后复制进受信内存数据库；临时路径在返回前关闭并删除 | 路径替换、Schema 漂移、逻辑摘要漂移和合法 Catalog 读回 |
| SEC-M14-010 | PNG CRC 校验在浏览器主线程对每个字节调用位运算辅助函数 | 使用预计算 CRC 表按字节单次推进，并保留固定文件、维度、像素与解码预算 | 已知 PNG、CRC 损坏、最大合法图片和 Python/TypeScript 几何一致性 |
| SEC-M14-011 | 单个 Unicode lone surrogate 会让整个 Catalog 构建异常退出 | 所有保留字符串在编码、摘要和插入前执行严格 UTF-8/Unicode 标量验证，单个非法 Bundle 局部拒绝 | 高低代理、合法补充平面字符和相邻有效 Bundle 控制组 |
| SEC-M14-012 | 不受信 SQLite 的 view 可在精确 Schema 与资源边界确立前执行 | 只接受固定表、列、类型、主键和索引签名；先以 BLOB 长度、行数和 DB 大小做原始预算，再读取受信字段 | view/trigger/额外对象、超长 BLOB、超量行和精确合法 Schema |
| SEC-M14-013 | 冲突的结构化 header 别名可能让认证值避开脱敏 | 对别名归一化后检测冲突；敏感 header 名及 `{name,value}`/映射形式统一 fail closed 脱敏 | 大小写、下划线/连字符、冲突别名、普通业务 value 对照组 |
| SEC-M14-014 | Plan 控制的附件上限与聚合 Evidence 输入缺少不可变总上限 | Schema 上限与 Core 固定上限取更小值；文件数、单文件、Evidence 总量、Bundle 总量和报告流式写入共同受限 | 边界值、越界值、多个合法单文件组合超总量和最终 Bundle 复核 |
| SEC-M14-015 | Markdown 转义仍可能被 GFM 将裸 URL/邮箱重新激活为链接 | 文本和代码上下文编码器额外中和裸 URL、邮箱与 GFM autolink 触发序列 | URL、邮箱、反引号、HTML、图片语法、换行组合与普通文本对照组 |

安全整改还把 Windows argv 约束、不可变资源预算和截图几何预算提取为单一所有者，消除不同调用层
各写一套近似规则的漂移风险。Workbench 与 Python 使用同一组图片维度、像素和解码预算事实，但两端
仍各自执行拒绝，前端没有因此获得 Core 裁决权。

Windows listener owner 运行事实现覆盖 IPv4 与 IPv6 两个表，但没有回写 M10 当时冻结的
`WINDOWS_IP_HELPER_CTYPES_IPV4` 历史记录；双栈后端只属于本次整改候选及其后继验收事实。

两轮整改完成后的工作树以 35 个变更面执行独立分组复核，并由差异扫描
`b5be844f-eb7a-4e2d-8351-424694bda6bb` 封卷；覆盖为 `35/35`，新增可报告发现为 `0`。这只证明当前
不可变工作树快照没有验证出新增安全回归，不替代后续绑定提交、双真实目标、真实浏览器与 Release 门禁。

## 3. 整改中暴露并关闭的相邻质量问题

完整回归发现 Playwright 1.62 的同步 `start()` 在所有权 hook 立即拒绝时，内部初始化 task 仍可能未完成；
随后关闭 event loop 会留下 `Task was destroyed` / `TargetClosedError` 诊断。浏览器层现在只在该特定
失败窗口有界等待已创建的内部初始化 task，并继续保证 Job、driver、Chromium 和 loop 的逆序清理。
真实 Playwright 回归会捕获 stderr、强制 GC 并证明没有 pending task。

Python 3.13 的 `ResourceWarning` 门禁还定位到一个测试直接构造 `CatalogApplication` 后未关闭固定的
SQLite 快照。测试现通过 `finally` 关闭应用；全量 3.13 以 `-W error::ResourceWarning` 运行，任何同类
生命周期遗漏都会成为硬失败。

## 4. 单兵工程中可复用的教训

这类缺陷确实常见于个人长期维护的复杂系统，但根因不是“一个人写代码必然不可靠”，而是：

1. 每一层局部测试都可能为绿，却没有证明同一个身份、同一份 bytes 和同一权威跨层连续；
2. 为了复用而按路径重新打开文件、按端口重新寻找服务、按请求重新打开数据库，会悄悄制造第二份事实；
3. 只给单文件设限而没有给保留对象、目录和最终响应设总预算，局部有界仍可能组合成全局无界；
4. 清理代码若只验证主进程退出，不验证异步 task、句柄、线程和 sidecar，偶发诊断会被误当作工具噪声；
5. 历史绿色不能继承给安全边界已经改变的新候选，必须主动宣布旧基线失效并从头复验。

对应的单兵工程法不是增加更多临场补丁，而是固定四个问题：

```text
谁拥有这份事实？
消费者使用的是否仍是被验证的同一份事实？
局部预算组合后是否仍然有界？
失败之后所有 owned 资源是否真的归零？
```

这段经验只作为工程复盘，不扩大 VeriTrail 的产品声明，也不把一次安全整改包装成通用形式化证明。

## 5. 重新基线后的不变量

新的整改基线一经绑定：

- `src/` 与 `schemas/` 除稳定版号文件 `src/veritrail/__init__.py` 外不得再变化；
- M14 验收器必须检查整改基线为 `HEAD` 祖先，并拒绝上述范围的其他差异；
- 当前 15 项发现必须先由攻击路径回归、双 Python、前端、两轮标准全仓扫描与整改差异复审共同复核；
- 自身目标和 InkNarratives 必须从新的干净提交重新运行，旧产物不计入最终门禁；
- 稳定版号提交后仍须重新运行完整门禁，不能把开发候选的绿色直接外推；
- 任一边界再次失败时，状态退回 `VALIDATING`，不创建或移动 `v0.12.0`。

## 6. 待绑定坐标

本节由下一提交一次性写入：

- 安全整改实现基线：`PENDING`；
- 基线绑定提交：由推送后远端读回记录；
- 允许的稳定版 Core 差异：仅 `src/veritrail/__init__.py`；
- 最终 Release 提交、标签对象和 GitHub Release URL：由后继事实文档记录。
