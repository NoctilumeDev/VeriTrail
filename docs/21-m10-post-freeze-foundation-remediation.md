# M10 冻结后地基纠偏与重新验收

> 状态：`FROZEN / REMOTE_READBACK_VERIFIED`
> 日期：2026-08-13 至 2026-08-14
> 影响层级：`L3_SYSTEM`
> 历史基线：`m10-v0.11.0` @ `008444319a4af54de3291fe5c0ab602001c30754`
> 修复版本：Python Core `0.11.1.dev1`，Workbench `0.11.1-dev.1`
> 补丁基线：`m10-v0.11.1` @ `f4efdd25c50b19077c61994bce3e2aca5244d5ec`

## 1. 结论与基线边界

冻结后的 M0-M10 系统审查发现 Verdict、Browser 所有权、生命周期停止、运行期资源与 Evidence
优先级存在跨层缺口。它们已经越过旧标签的兼容容差，所以 `m10-v0.11.0` 只保留为历史事实，
标签对象 `70c26b827b13857b0663fd158f5aa30862d87bb1` 及其提交
`008444319a4af54de3291fe5c0ab602001c30754` 不移动、不覆盖。

当前补丁已完成代码修复、M0-M10 全仓回归、公共出口、16 GB 有界压力、生产 Workbench、
Codex 内置浏览器、依赖、安全和清理复验。首次冻结读回时，GitHub `main` 与
`m10-v0.11.1^{}` 均精确指向实现提交 `f4efdd25c50b19077c61994bce3e2aca5244d5ec`，因此形成新的
可寻址 `FROZEN` 补丁基线。M11 继续保持 `PLANNED`。

## 2. 缺陷与系统级修复

| ID | 旧风险 | 修复后的系统不变量 |
| --- | --- | --- |
| PF-001 | 污染 Run 的 HARD 失败先于未知变量、漂移或证据冲突，被错误裁为 `FAIL` | 归因阻断先于普通 HARD 失败；有同一 Evidence 决定性断言证明的 cleanup 直接失败仍为 `FAIL`；Catalog 使用同一规则重推导 |
| PF-002 | application READY 后的同步 Browser 不能及时响应取消和 lifecycle deadline | readiness、Browser、lifecycle 与资源 monitor 共享带原因 `StopSignal`；Browser 在启动、viewport、导航和步骤边界检查，单操作 timeout 受剩余生命周期约束 |
| PF-003 | Browser 取消可能发生在 Playwright driver 进入 owned Job 之前 | 必需所有权 hook 先于 Chromium 后代启动；启动期取消只在 hook 成功后生效，hook 失败不能被同时到达的取消掩盖 |
| PF-004 | Browser 中止或 collector error 丢失 Job、采样与 cleanup 事实 | 专用中止/采集异常携带资源、Job 限制、handles 与进程释放事实；公共 Bundle 分别形成 `ABORTED/PENDING` 或 `ERROR/PENDING`，不伪装业务 `FAIL` |
| PF-005 | 运行期只记录 Core、节点与 Browser RSS，没有执行 sealed 宿主机可用内存停止线 | 运行前完成 grace 采样，运行中持续采样 available memory；软线先停止、持续硬越界再升级，阈值和触发事实进入 `runtime.bootstrap` 0.2 |
| PF-006 | 资源采样失败可能继续启动工作负载 | fail closed 为 `COLLECTOR_ERROR`，不启动被测进程，公共 Evidence 为 `EVIDENCE_ERROR / ERROR/PENDING` |
| PF-007 | 资源/用户中止时 `services_ready=false` 会制造额外业务 `FAIL` | 被中止阶段的 readiness 断言为 `NOT_EVALUATED`；已独立证明的 readiness 或 cleanup 失败仍保持确定性 `FAIL` |
| PF-008 | subject drift 可能先于不完整资源/subject 观察，掩盖 Evidence 完整性错误 | 不完整观察优先形成 `EVIDENCE_ERROR`；validator 拒绝伪造的停止优先级 |
| PF-009 | 压力 HTTP server 默认 backlog 5 在 100 in-flight 下产生连接重置 | 验收夹具 backlog 固定为 128；失败轮保留，修复后同一固定种子从头重跑 |
| PF-010 | Windows 可能短暂锁住刚写完的 staging 文件，使 Bundle、Comparison、Pairing、Batch 或 Catalog 的同卷目录发布随机 `WinError 5` | 五类不可变产物共用窄原子发布助手；仅对 Windows sharing/access/lock violation 做 20 次、每次 50 ms 的有界重试；目标一旦出现或错误不匹配立即拒绝，绝不覆盖 |
| PF-011 | M3 浏览器验收仍用裸静态服务器，当前 Workbench 请求 Catalog 时制造 404；M3/M4 脚本又把损坏夹具错误码锁在旧 `HASH_MISMATCH` | M3 兼容入口提供合法只读空 Catalog；两条脚本精确验证当前夹具的 `MISSING_ROOT_FILE`、无部分可信状态和显式恢复，不放宽 Loader |

## 3. 权威、兼容与代码质量

- `runtime.bootstrap` 当前生产者固定为 `bootstrap-lifecycle/0.2`；validator 只读兼容冻结的 0.1
  形状，0.1 不能声称新的运行期宿主机停止事实；
- 公共 M2 `collect_browser_evidence(plan)` 合同不变；停止、deadline 与 Chromium Job 观察只进入
  M10 内部入口；Plan 0.1-0.5 的冻结哈希和消费者继续回归；
- 外部用户取消保留操作者意图；资源 soft 可升级为 hard；Evidence/cleanup 错误可以改变最终
  stop reason，但资源触发仍保留在 resource observation；
- Pairing/Batch 继续拒绝 Plan 0.6，Comparison 继续同时验证 Plan/Profile，Workbench 仍只读消费
  Core 裁决；没有把前端扩展成第二套规则引擎；
- 停止原因只有一个同步所有者；Browser 中止、collector error 和业务失败使用不同类型；新 Evidence
  字段采用精确字段集、枚举、阈值关系和 Plan 漂移校验；
- 同卷目录发布的重试只解决 Windows 短暂共享锁，不把 copy/delete 冒充原子发布，也不把已存在目标
  解释为成功；产物字节、Manifest 哈希与拒绝覆盖语义不变；
- 资源 monitor 只有一个 50 ms 采样线程。压力阶段只在预注册波次使用度数 1/2/3 的受限微并行，
  没有按 24 逻辑处理器无界扩张；
- `bootstrap_evidence.py`、`bootstrap_run.py` 等地基模块偏大，但本轮不为拆分而拆分。状态机和公共
  Evidence 正在变更时做结构重写会扩大爆炸半径；先冻结语义和真实证据，后续重构必须独立立项；
- 两个 Git 忽略的项目虚拟环境已重新绑定当前源码，运行时版本与包元数据均为 `0.11.1.dev1`，
  不再依赖旧 editable metadata。没有修改全局 Python。

## 4. 自动化与公共出口

| 门禁 | 结果 |
| --- | --- |
| 受影响 M10/系统模块 | `87/87 PASS`，73.787 s |
| 严格公共出口矩阵 | `17/17` 方法、`19/19` 公共场景，53.923 s |
| Python 3.10.6 全仓 | `262/262 PASS`，126.055 s |
| Python 3.13.13 全仓 | `262/262 PASS`，126.302 s |
| 双 Python `compileall` / `pip check` | PASS / `No broken requirements found` |
| Workbench | `59/59 PASS`；lint、type-check、production build PASS |
| npm 官方源审计 | production 0、完整依赖 0 vulnerabilities |
| 生产 Catalog 浏览器 | `7/7 PASS`；54 请求，HTTP/外部/写请求均为 0 |
| M3 兼容浏览器 | `5/5 PASS`；66 请求，HTTP 错误为 0 |
| `git diff --check` | PASS |

公共矩阵覆盖原 13 类出口，并增加 Browser cleanup failure、资源 soft/hard/sampling error、Browser
执行中用户取消和 Browser collector error。等值 soft/hard 阈值继续合法，与冻结 Plan 0.6 语义一致。

Python 3.13 首次误用全局 `py -3.13`，在收集阶段因包未安装产生 38 个 import errors、0 个产品测试；
随后项目 `.venv313` 又因缺少 `setuptools.build_meta` 无法重绑。补齐隔离环境构建工具并重新绑定后，
从头完成上述 258 项；失败入口没有被改写为产品失败或隐藏。

补丁冻结轮第一次误用 1 秒外层超时，随后与第二次全仓测试重叠，产生的 18 个 `WinError 5` 不作为
串行产品结论；进程和端口清零后，Batch 定向复跑仍复现 2 个相同随机发布失败，由此确认 PF-010。
公共发布助手的 4 个边界测试与五个消费者定向回归通过后，双 Python 都从头完成 262 项。生产浏览器
先后保留两次旧验收合同失败：M3 裸静态入口的 Catalog 404，以及 M4 对旧错误码的硬编码；PF-011
修复后两条入口均从头通过。

## 5. 16 GB 有界压力终验

补丁冻结轮最终有效输出为 TEMP 下 `veritrail-m10-patch-stress-22dc28ce9953466aa238e19e126f8578`，
固定种子 `20260813`：

- Catalog：11 Runs，0 issue，0 duplicate，bundle set SHA-256
  `1dcb36e3793f524a82ebf763e85489aab2880624924cfc4c6ce74d9cb19bc76c`；
- 独立度 1/2/3：`6/6 COMPLETED/PASS`；
- READY 后取消：`3/3 ABORTED/PENDING`，均为 `USER_CANCELLED` 且逆序清理完整；
- 同端口竞争：两个错误 owner 均被拒绝为 `LISTENER_OWNERSHIP_MISMATCH / ABORTED/FAIL`，外部所有者
  未被接管；
- HTTP 阶梯为 `100@1 -> 200@10 -> 300@50 -> 400@100`，总计 1000 请求、0 error；
- 最低宿主机可用内存 6280 MiB，高于 3072/2048 MiB soft/hard 线；结束时 6169 MiB；
- 最终端口释放、仓库 staging 为 0，所有 Bundle 经 Catalog 独立验真。

一次早期修复轮在 `400@100` 观察到 9 个 `ConnectionResetError`，明确形成 `ERROR/FAIL`。根因是
验收 HTTP server 的默认 request backlog 5，不是内存停止线；backlog 固定为 128 后，后续五轮和
本轮最终候选均以相同种子从头通过。历史 TEMP 目录只包含可重建的诊断与验收输出；本轮清理命令
被执行策略阻止，7 个已核对目标仍待本地清理，不把未执行的清理写成已经完成。

## 6. Codex 内置浏览器终验

生产构建由只读 Catalog API 在 `127.0.0.1:18770` 提供，本轮真实操作结果：

- 目录读出 11 Runs，与 summary 一致：6 PASS、3 PENDING、2 FAIL；
- 分别打开 `COMPLETED/PASS`、`ABORTED/PENDING`、`ABORTED/FAIL`，Evidence 适用性、
  `NOT_EVALUATED`、cleanup 与 Browser 缺口语义正确；
- 刷新、后退、前进均按 URL 恢复正确 Run 和既有 Core 裁决；
- 桌面 1280x720 与移动 390x844 均无页面级横向溢出，移动状态卡和 Run 列表不重叠；
- 页面 Console/Warning 为 0；页面资源账册全部为 `127.0.0.1:18770`，包含生产 JS/CSS、
  `/api/v1/catalog`、Bundle 文件和证据截图，无 CDN、远程字体或第三方页面请求；
- Codex 浏览器宿主曾对 `ab.chatgpt.com` 的遥测 POST 超时；它不在页面资源账册和页面 Console 中，
  单列为宿主网络噪声，不计作 VeriTrail 请求；
- 冻结终验时，内置浏览器两条合成键盘通道的 `Tab` 都未移动焦点，符合项目已保留的工具限制；
  当时只记录 DOM 原生顺序，不伪称“物理 Tab 已通过”；
- 2026-08-14 的冻结后人工物理键盘补验发现两项真实 L0 缺陷：四个透明文件输入只有 `1px × 1px`
  焦点区域，且浏览器事实页签的外置焦点环被横向滚动容器裁切。修复后，物理 `Tab` 已依次通过
  来源按钮、四个可见文件入口、适用边界、断言筛选和浏览器事实当前页签；浏览器事实页签组按标准
  ARIA 模式使用左右方向键在“步骤 / Console / Network / 截图”间移动，焦点环持续可见。前端全量
  `59/59`、Lint、类型检查与生产构建通过。该补验是冻结后工作树事实，不倒填为 `0084443` 的
  原始冻结证据。

浏览器关闭后，owned Catalog PID 已按完整命令行身份停止，端口 18770 释放。

## 7. 安全、完整性与最终清理

- tracked 敏感模式扫描未读取 `.env`；GitHub token 形态全部是测试声明的假 canary
  `ghp_12345678901234567890`，测试邮箱全部使用保留域 `example.test`，lockfile 邮箱仅来自公开依赖
  元数据；没有发现真实令牌、私钥或用户账号；
- `git diff --check`、Markdown 本地链接检查和 `git fsck --full --no-dangling` 通过；历史标签对象与
  解引用提交仍精确为 `70c26b8...` 和 `0084443...`；
- 7 个已核对的 TEMP 诊断、浏览器、压力与预览输出目录仍存在；递归清理命令被执行策略阻止，未
  尝试绕过，也没有删除仓库、虚拟环境或用户项目数据。它们是可重建输出，不属于提交或产品运行
  残留；
- 最终端口段 18765-18891 无监听，仓库无 `.veritrail-*` staging；没有项目 helper、Catalog 或
  Chromium 进程残留；宿主机复核时约 6880 MiB 可用内存。

## 8. 当前门禁

- [x] Verdict 优先级、直接 cleanup 失败和 Catalog 重推导；
- [x] Browser 执行中停止、ownership、collector/cleanup 失败与公共 Bundle；
- [x] 宿主机 soft/hard/grace、采样失败、停止原因和逆序清理；
- [x] 旧 `runtime.bootstrap` 0.1 只读兼容；
- [x] 双 Python 全仓、compileall、pip check 与 editable 版本一致；
- [x] Workbench test/lint/type-check/build 和官方源依赖审计；
- [x] 公共出口、受限多实例、取消交错、1000 请求与 Catalog；
- [x] Codex 内置浏览器三态、导航、Console、Network、桌面/移动与人工物理键盘；
- [x] Windows 瞬时目录锁的原子发布有界恢复与五类消费者回归；
- [x] 当前 Catalog 与历史 M3 两条生产 Chromium 验收入口；
- [x] 新提交、新标签与远端读回：`m10-v0.11.1^{}` @ `f4efdd2`；
- [ ] M11：继续 `PLANNED`，不得把本文件解释为已进入后继里程碑。

当前准确结论是：**M0-M10 冻结后补丁已完成本地发布级重新验收和 GitHub 精确读回，没有新的已知
阻断项；`m10-v0.11.1` 是进入 M11 合同规划前必须引用的当前地基基线。**
