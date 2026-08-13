# M10 第二轮 16 GB 有界压力审计

> 状态：`PREREGISTERED / NOT_RUN`
> 计划日期：2026-08-13
> 随机种子：`20260813`
> 代码候选：`c3118d8`；串行基线：`47d0581`
> 依据：[M10 完成、地基审查与双轮冻结计划 0.1](16-m10-completion-and-foundation-audit.md) 第 6 节

## 1. 本轮只回答什么

本轮诊断 M10 在 16 GB Windows 主机上的所有权、隔离、证据、清理与资源停止线，不能把通过结果
宣传为生产吞吐或正式通用并行支持。变量一次只增加一个：相同端口竞争、独立 Profile 并发度、取消
交错、HTTP 最大在途数。任何安全、Evidence、Verdict 或清理不变量失败都阻断 M10；资源停止线按计划
触发只形成边界事实。

起点实时快照：物理内存 15.78 GB、可用内存 8.21 GB，C 盘可用 139.46 GB；18870–18890 全部空闲。

## 2. 固定资源与停止线

| 项目 | 冻结值 |
| --- | --- |
| 可用内存软停止线 | 3072 MiB；到达后不启动下一 wave |
| 可用内存硬中止线 | 2048 MiB；当前 wave 请求 cooperative cancel/终止自有 harness 并保留现场 |
| 最大 M10 Run 并发度 | 3 |
| 单 Run 内部 | 1 dependency + 1 application + 1 Chromium Context，仍严格串行启动 |
| 请求总量 | 整个 HTTP 阶梯合计 1000，不是每阶 1000、1000 浏览器或 1000 RPS |
| 请求阶梯 | 最大在途 `1 -> 10 -> 50 -> 100`，分配 `100 + 200 + 300 + 400 = 1000` |
| 输出 | 系统 TEMP 下唯一根目录；每 Run 独立 Bundle/work/staging；成功记录摘要后删除 |
| 网络 | 仅 `127.0.0.1`；HTTP 客户端禁用环境代理并复用有界连接池 |

端口预注册如下，不在观察结果后换成“更容易通过”的端口：

| 场景 | dependency/application 或 target 端口 |
| --- | --- |
| 同 Profile 竞争 | 18870 / 18871 |
| 独立 wave 1 | 18872 / 18873 |
| 独立 wave 2 | 18874 / 18875，18876 / 18877 |
| 独立 wave 3 | 18878 / 18879，18880 / 18881，18882 / 18883 |
| 取消/清理交错 | 18884 / 18885，18886 / 18887，18888 / 18889 |
| HTTP 1000 请求 | 18890 |

## 3. Wave A：同 Profile、同端口竞争

两个 Run 先对同一 sealed Plan/Profile 分别生成审批摘要，再以固定种子顺序近同时启动，Bundle 输出
分离。允许结果只有：至多一个 `COMPLETED/PASS`；另一 Run 在 preflight 发现端口竞争后
`ABORTED/PENDING`，或在 owned readiness 中形成可解释的 `FAIL/ABORTED`。禁止出现两个 PASS、误杀
同伴/外部进程、读取对方 listener 为己有、Bundle 互相覆盖、未知异常或 wave 后残留。

## 4. Wave B：独立 Profile 微并行阶梯

按 `1 -> 2 -> 3` 运行完全独立的 sealed Profile、端口、subject、Plan 和 Bundle。上一阶只有在所有
Run `COMPLETED/PASS`、Bundle 独立验真、资源未越线且 helper/端口/staging 回零后才进入下一阶。
并发 3 是本机上限，不因资源仍有余量继续升阶。

每个 Run 记录 wall time、ExecutionStatus/Verdict、Bundle 文件数、Core/dependency/application/
browser peak RSS、采样完整性与清理事实；每个 wave 记录起止可用内存和最低观测值。

## 5. Wave C：取消与清理交错

三个独立 Run 使用种子 `20260813` 派生的固定启动顺序与毫秒级取消延迟。取消只能在 application READY
后、Browser 创建前生效；每个 Run 必须形成 `USER_CANCELLED / ABORTED/PENDING`、零 browser Evidence、
application→dependency 逆序清理和独立可验 Bundle。任一 Run 取消过早、继续启动 Browser、误清理
同伴或留下端口，都阻断本轮。

## 6. Wave D：1000 总请求

启动一个 owned、已就绪的轻量回环 application；四阶请求分别为 100/200/300/400。每阶记录完成数、
错误分类、P50/P95/P99、吞吐、进程 RSS、可用内存、TCP 状态和 listener owner。只在前一阶完成数正确、
错误为零、owner 未变且资源在线内时升阶。最后终止自有进程并证明 18890、连接和进程释放。

HTTP 响应只验证稳定的只读 health/body，不执行写操作；因此本 wave 只诊断连接/读取与清理，不声称
数据库、幂等、库存或业务一致性。M10 的一致性不变量具体表现为：Run/Bundle 不交叉污染、所有权不
串线、负向不能变 PASS、已封存 Bundle 不被后续 wave 修改、每 wave 都回到清洁起点。

## 7. 固定执行顺序与退出

```text
preflight snapshot
  -> Wave A same-port competition
  -> zero-residue gate
  -> Wave B degree 1
  -> zero-residue gate
  -> Wave B degree 2
  -> zero-residue gate
  -> Wave B degree 3
  -> zero-residue gate
  -> Wave C cancellation interleave
  -> zero-residue gate
  -> Wave D 1000 total requests
  -> final bundle/catalog/security/residue verification
```

本文件提交后才允许实现/运行 harness。任一 wave 失败即停止，不执行后续 wave；修复后必须建立新候选
并从 Wave A 重跑，不能把不同实现的局部绿色拼成 `STRESS_AUDITED`。

## 8. 运行记录

尚未运行。计划文字、端口为空或已有串行测试都不能预填压力事实。
