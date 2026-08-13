# M10 第二轮 16 GB 有界压力审计

> 状态：`STRESS_AUDITED`
> 计划日期：2026-08-13
> 随机种子：`20260813`
> 通过候选：`88d083a`；串行基线：`47d0581`
> 压力 harness：`scripts/m10_stress_acceptance.py`
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

## 8. 实施中保留的失败事实

本轮没有把不同实现的局部绿色拼接成通过。每次更改 harness 后都建立新候选，并从 Wave A 完整
重跑；前三次失败与处置如下：

| 次数 | 停止位置与事实 | 判断与处置 |
| --- | --- | --- |
| 1 | Wave A 两个竞争 Run 均安全形成 `LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL`，端口、helper 与 staging 最终为零；harness 却要求必须恰有一个 PASS | 预注册条件是“至多一个 PASS”，不是“必须一个 PASS”。修正错误的验收器断言，候选推进至 `664479f` |
| 2 | Wave A 一个 Run PASS；另一 Run 在竞争者仍占用共同声明端口时形成 `CLEANUP_ERROR / ERROR/FAIL`。其自有 Job、handle、reader、work、staging 均已释放，只有 `ports_free=false`；wave 结束后端口为零 | 既有 Contract/测试明确要求外部 listener 仍在时不得伪装 clean。harness 改为只接受精确 contention 签名并继续要求 wave 终态清零，候选推进至 `708b796` |
| 3 | Wave A、并发度 1/2/3 和取消交错均通过；HTTP wave 在启动时停止，因为 Windows venv launcher PID 与真实 listener PID 不同，原 harness 无法证明所有权 | 未降低 owner 门禁。HTTP 服务改由 Windows Job 持有，用 Job 进程集合证明 listener owner 并统一采样/回收，候选推进至 `1191181` |
| 4 | `1191181` 首次完成六 wave 后，发布代码审查发现硬内存停止/worker 超时分支只终止 launcher 就抛错，未等待或证明 venv launcher 的真实子树退出；该分支本次没有触发，但仍是冻结阻断项 | 增加 owned worker-tree 强制回收、launcher/pipe 等待和 wave 端口/staging 复核；双 Python 真实 launcher→子监听树测试均通过。候选推进至 `88d083a`，再从 Wave A 完整重跑 |

以上失败目录均位于系统 TEMP，只含可重建验收数据；提取事实后已删除。它们不作为最终通过证据，
但其失败原因、候选边界与从头重跑纪律保留在本文件和 Git 历史中。

## 9. 最终完整重跑事实

候选 `88d083a` 从 Wave A 开始一次性完成全部六个 wave，最终汇总为
`execution_status=COMPLETED / verdict=PASS`。起始、最低与结束可用内存分别为 8066、7323、8163 MiB；
最低值高于 3072 MiB 软停止线，也远高于 2048 MiB 硬中止线，没有越过资源门禁。

| Wave | 运行事实 | 最低可用内存 | 清理事实 |
| --- | --- | ---: | --- |
| 同端口竞争 | 两个 Run 均拒绝错误 listener，形成 `LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL`；没有 Run 被误判 PASS | 7989 MiB | 两个 Run 的 Job/handle/reader/端口/work/staging/reverse-order 全部为真；wave 后端口与 staging 为零 |
| 独立度 1 | 1/1 `COMPLETED/PASS`；Browser peak RSS 216.129 MiB | 7754 MiB | Run 与 wave 均 clean |
| 独立度 2 | 2/2 `COMPLETED/PASS`；Browser peak RSS 248.840/218.922 MiB | 7550 MiB | 两个 Run 与 wave 均 clean |
| 独立度 3 | 3/3 `COMPLETED/PASS`；Browser peak RSS 216.133/224.520/223.961 MiB | 7323 MiB | 三个 Run 与 wave 均 clean；达到预注册上限后停止升阶 |
| 取消交错 | 固定启动顺序 `cancel-c -> cancel-b -> cancel-a`，延迟 90/30/10 ms；3/3 为 `USER_CANCELLED / ABORTED/PENDING`，Browser 均未启动 | 7891 MiB | 三个 Run 的 application→dependency 清理及 wave 终态均 clean |
| HTTP 1000 | listener owner 由 Job 进程集合验证；100/200/300/400 四阶全部完成、错误均为零 | 7988 MiB | Job empty、handle/reader/18890 释放均为真 |

HTTP 阶梯的诊断数据如下。它只描述本机回环只读服务，不是生产容量声明：

| 最大在途 | 请求数 | RPS | P50 | P95 | P99 | server RSS |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100 | 81.283 | 0.120 ms | 0.292 ms | 0.933 ms | 39.355 MiB |
| 10 | 200 | 164.239 | 0.686 ms | 1.875 ms | 3.301 ms | 39.477 MiB |
| 50 | 300 | 224.992 | 1.829 ms | 6.240 ms | 12.858 ms | 39.773 MiB |
| 100 | 400 | 239.221 | 1.960 ms | 8.771 ms | 13.367 ms | 39.863 MiB |

## 10. 独立回读与结论边界

harness 结束后再次从磁盘独立调用 Bundle validator 与 Catalog 只读接口：11/11 Bundle 验真，11 个
`bundle_sha256` 均不同；状态分布为 6 个 `COMPLETED/PASS`、3 个 `ABORTED/PENDING`、2 个
`ABORTED/FAIL`。Catalog 为 `COMPLETED`，`run_count=11`、`issue_count=0`、`duplicate_count=0`，
SQLite 记录 150 个受管文件，`bundle_set_sha256` 为
`148764a1fcbde14f8435df6cfbc5f6023b50540c38bc9cc86cd254bd52f61f84`。

独立残留复核确认 18870–18890 无 listener、相关 harness/helper 进程为零、staging 为零。最终 TEMP
目录仅为可重建验收产物，事实写入本文后删除，不进入 Git。

因此阶段 D 标记为 `STRESS_AUDITED`。这个状态只证明 M10 在预注册的 16 GB Windows/C1、有界微并行
与回环只读负载内守住所有权、隔离、Evidence、Verdict、资源和清理不变量；它不证明正式通用并行、
生产吞吐、其他平台、第二种真实项目或 M11 能力。M10 仍未 `FROZEN`，必须继续完成最终候选回归、
新增 harness 的系统/代码质量复核、发布级内置浏览器与安全/残留门禁，以及 GitHub 提交和
`m10-v0.11.0` 标签读回。
