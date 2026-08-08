# 06. M2 真实浏览器证据

## 状态

`IMPLEMENTED`。验收合同已在提交 `de62ae043c8b7ec604eecfb4113bf0ccc11a9712` 独立冻结，
代码、自动化和真实运行证据已形成；在干净实现提交上完成最终复验并写入冻结记录之前，M2
仍不能标记为 `FROZEN`。M2 只建立有界的 Chromium 证据纵向闭环，不加入 Vue、SQLite、
项目命令执行、多角色并行或远程站点自动化。

## 目标问题

M2 只回答：

> 在 M1 资源预检允许启动的前提下，VeriTrail 能否按封存步骤串行操作一个真实 Chromium，
> 将 Console、页面异常、Network、截图、视口、步骤时间线和横向溢出事实安全地纳入同一证据包，
> 并由现有确定性规则裁决？

M2 不把截图、页面加载成功或 Playwright 用例绿色单独解释为真实链路通过。浏览器事实必须进入
M0 已冻结的 Evidence、Verdict、报告和哈希链路。

## 影响层级与消费者

- 声明层级：`L2_CONTRACT`；
- 所有者：VeriTrail Core / Browser Adapter；
- 新契约：`ExperimentPlan 0.3`、`browser.session` Evidence、二进制证据附件；
- 直接消费者：计划校验器、CLI、证据导入器、Artifact Store、JSON/Markdown 报告和测试；
- 后续消费者：SQLite 索引、Vue Workbench、真实项目自举与多 Context 适配器；
- 不在范围：M0/M1 裁决优先级、Plan 0.1/0.2 语义、任意 Shell、浏览器 Profile、凭据注入、
  远程 URL、服务生命周期管理和浏览器并行。

如果实现需要改变 Verdict 优先级、允许用户提供任意可执行程序、持久化认证材料，或让浏览器
直接写最终 `PASS/FAIL`，实际范围已经升级，必须停止并重新评审。

## 0.1 / 0.2 / 0.3 兼容矩阵

旧计划不原地增加字段：

| 操作 | Plan 0.1 | Plan 0.2 | Plan 0.3 |
| --- | --- | --- | --- |
| `seal` | 保持 M0 行为 | 保持 M1 行为 | 支持并封存浏览器策略 |
| `evaluate` | 保持 M0 行为 | 保持 M1 行为 | 支持导入浏览器证据 |
| `preflight` | 明确拒绝 | 保持 M1 行为 | 保持 M1 预检语义 |
| `browser-capture` | 明确拒绝 | 明确拒绝 | 先预检，再执行有界浏览器步骤 |

Plan 0.3 继承 Plan 0.2 的 `preflight`，并新增必填 `browser` 对象。Plan 0.3 必须同时要求
`runtime.preflight` 与 `browser.session`；至少一个决定性断言读取 `browser.session`。

## 浏览器策略

M2 的 `browser` 对象预注册：

| 字段 | 语义与边界 |
| --- | --- |
| `engine` | 固定为 `chromium` |
| `headless` | 是否无头运行；它是封存变量，CLI 不得临时覆盖 |
| `start_url` | 第一个页面，只允许显式回环 HTTP origin |
| `allowed_origins` | 1–8 个完整 `http://127.0.0.1:PORT` 或 `http://localhost:PORT` origin，无通配符、凭据、查询和片段 |
| `timeout_ms` | 单步骤与导航的上限，范围 1000–30000 ms |
| `viewports` | 1–4 个命名视口；M2 真实验收至少一个桌面和一个移动视口 |
| `steps` | 1–50 个结构化步骤，ID 唯一，按声明顺序对每个视口执行 |

M2 只支持 `goto`、`click`、`fill`、`press`、`expect_visible`、`expect_text` 和 `screenshot`。
每种动作只接受固定字段，未知字段被拒绝；不接受 JavaScript、函数、Shell、浏览器启动参数、
扩展或持久化 Profile。`screenshot` 动作最多 4 个且只采集当前视口，避免超长页面耗尽内存；
`fill` 只能保存非秘密夹具值，字段名或内容触发脱敏规则时计划封存失败。

所有 Context 串行运行，任一时刻最多一个 Browser、一个 Context、一个 Page。每个视口使用全新
Context，结束后关闭；M2 不支持共享登录态或多角色并行。步骤失败时不自动重放写操作，失败事实
进入时间线并结束当前视口，避免重试制造重复副作用。

## 启动门禁与资源边界

`browser-capture` 必须先执行 Plan 0.3 的 M1 预检：

```text
preflight ABORT          -> 不启动浏览器，ABORTED + PENDING（除非已有独立硬失败）
preflight STOP_ESCALATION -> 不增加浏览器负载，COMPLETED + PENDING
preflight PROCEED        -> 串行启动一个 Chromium，完成后关闭
```

命令不启动被测站点，不关闭用户浏览器，不修改代理、防火墙、端口或系统设置。Playwright 是可选的
`browser` 安装能力并锁定版本；浏览器二进制单独显式安装。缺少依赖或浏览器时安全报错，不留下
半成品 Run。

Console 最多记录 500 条、页面异常最多 100 条、Network 最多 1000 条；文本最长 4096 字符。
达到任一上限或发生截断都会记录采集错误并阻止 `capture_complete`，不能用丢弃尾部事实换取
表面 `PASS`。

## `browser.session` 证据

结构化证据至少包含：

- 采集器与 Playwright/Chromium 版本、运行模式和顺序；
- 每个视口的名称、宽高、移动标记和横向溢出像素；
- 每一步的 ID、动作、开始/结束时间、状态、耗时和脱敏错误类型；
- Console 的时间、级别和脱敏文本；
- 未捕获页面异常的时间、脱敏名称和文本；
- Network 的方法、去除查询值后的 URL、资源类型、状态、失败类型和重定向关系；
- 未解释的 JavaScript 错误、请求失败、4xx/5xx、重复写请求与溢出计数；
- 截图的逻辑名称、相对附件路径、SHA-256、大小与所属步骤；
- 采集是否完整、清理是否完成、采集错误与观察到的受控变量。

Network 不持久化请求/响应头、Cookie、请求体、响应体、认证材料或 URL 查询值。URL 中的
userinfo 被拒绝；查询参数只保留键并把值替换为固定占位符。Console、错误消息和路径在落盘前
继续经过统一隐私规则。

截图作为二进制附件进入证据清单和 Bundle 清单。附件名只能由适配器生成，必须位于本次临时
组装目录内；每个文件受 `max_artifact_bytes` 限制，哈希与 JSON 引用必须一致，不能接受路径
穿越或静默覆盖。

## 确定性浏览器断言

自举 Plan 至少封存以下 `HARD` 断言：

- `capture_complete == true`；
- `all_steps_passed == true`；
- `unexpected_console_error_count == 0`；
- `page_error_count == 0`；
- `failed_request_count == 0`；
- `unexpected_http_error_count == 0`；
- `duplicate_write_request_group_count == 0`；
- `horizontal_overflow_viewport_count == 0`；
- 桌面和移动视口、关键截图数量均达到计划值。

浏览器适配器只产生事实和计数，不直接决定 Verdict。失败步骤、Console 错误、页面异常、网络
失败、4xx/5xx 或重复写请求必须被保留；是否属于预注册允许情形由计划断言表达，不能在观察结果
后由采集器静默过滤。

## 自动化验收矩阵

- Plan 0.1/0.2 的冻结测试和已知计划哈希保持不变；
- Plan 0.1/0.2 调用 `browser-capture` 被明确拒绝且不产生输出；
- Plan 0.3 修改 origin、视口、步骤、超时或 headless 后原 Seal 失效；
- 非回环 URL、userinfo、无端口 origin、未知动作/字段、重复 ID、越界数量与超时被拒绝；
- STOP/ABORT 预检不启动 Playwright，状态与 Verdict 分离；
- 浏览器缺失、导航超时和步骤失败关闭 Context/Browser 且不留下 staging；
- 合成采集分别覆盖成功、Console 错误、页面异常、请求失败、4xx/5xx、重定向、重复写请求、
  横向溢出和步骤失败；
- URL 查询值、认证头、Cookie、正文、用户路径、邮箱、IP 与令牌不会进入证据包；
- 截图附件、Evidence 清单和 Bundle 清单逐字节哈希一致，重复名称与路径穿越被拒绝；
- JSON 与 Markdown 使用同一浏览器事实和 Verdict。

## 真实运行退出条件

在干净提交和当前 16 GB Windows 主机上串行执行：

1. 用轻量回环站点运行一个桌面和一个移动视口，完成点击、文本断言和关键截图；
2. 真实 Chromium 的 Console、Network、步骤、视口、截图和溢出事实全部进入证据包；
3. 单独运行负夹具，证明 JavaScript 错误与 4xx/5xx 不能静默得到 `PASS`；
4. 使用 Codex 内置浏览器再次真实操作同一用户链路，并检查 DevTools Console、Network、
   桌面/移动视口和未解释异常；
5. 逐字节核验 JSON、Markdown、证据附件与两层清单哈希；敏感扫描 0 命中；
6. 浏览器、Context、页面、回环服务器、端口和 `.veritrail-*` 临时目录均已释放；
7. Python 3.10 与 3.13 自动化、M0/M1 兼容回归通过，Git 工作区只包含预期提交；
8. 冻结提交与标签能从 GitHub 读回。

只有以上全部成立，M2 才能依次推进到 `FROZEN`。任何一项无法执行时，状态保持其真实阶段，
不得以“适配器已写完”替代最终验收。
