# Release 资产下载恢复截止时间修正

当前状态：`L1_COMPONENT_INTERNAL / Q0_FREEZE_CLOSURE_HELD`

本修正只处理 Public CI 下载既有不可变 Release 资产时，退避阶段与绝对恢复预算之间的组合语义。
它不改变 Release 坐标、冻结 SHA-256、P4/Q0 合同、验收阈值或 Core/插件公共语义。

## 1. 触发事实

Q0 状态发布经 PR #93 合入 `main@39b5eb37ebd8f2e502925f2a026be2ccf4c25101` 后，匿名
README、本文前序文档与里程碑读回均为 `COMPLETE / PASS`，Browser Smoke 也为 1/1 `SUCCESS`。
但是同一 exact main 的原始
[Public CI run 34419511498](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34419511498)
只有 10/11 项成功；E3 0.2 Release 下载验收在
[job 102691680453](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34419511498/job/102691680453)
停止。

失败路径下载的是不可变 Core `v0.12.0` wheel：

```text
veritrail-0.12.0-py3-none-any.whl

attempt 1: HTTP 500
sleep 2s
attempt 2: HTTP 500
sleep 4s
attempt 3: HTTP 500
sleep 8s
attempt 4: HTTP 500
sleep 16s
attempt 5: HTTP 500
stop
```

下载器在约 31 秒后因五次尝试上限退出，而声明的 60 秒 monotonic 绝对恢复预算仍剩约 29 秒。
因此文档 117 要求的合入后 exact-main 全门禁并未成立；Q0 冻结发布不能用先前 PR 门禁、匿名读回或
Browser Smoke 替代这一项失败。

随后对同一公开 URL 的独立匿名下载成功，字节 SHA-256 为：

```text
d0293f06e6a2b0271870ce032b2197c6ef7956db0ff3889230ca48234ff2fa45
```

该值与冻结坐标一致。现有证据支持恢复策略提前停止，不支持推断 GitHub 内部、代理、校园网或其他传输
环节的唯一根因，也不支持把原始 HTTP 500 改写成资产损坏。

## 2. 语义缺口

[文档 98](98-release-download-recovery-correction.md) 已经声明：所有请求与 sleep 共同消费一个默认
60 秒的绝对恢复预算，退避阶段为 `2 / 4 / 8 / 16` 秒。旧实现却同时隐含了：

```text
attempt_count = len(backoff_stages) + 1
```

这使退避表同时拥有了两种不相容的含义：

```text
声明语义：逐步增加后达到最大等待间隔
实现语义：穷尽表项后立即终止全部恢复
```

因此：

```text
attempt limit
!=
recovery deadline
```

绝对预算本应是恢复窗口的最终所有者；有限退避表只定义等待间隔如何增长，不能静默创建一个更短的第二
停止条件。

## 3. 最小修正

默认恢复状态机修正为：

1. `2 / 4 / 8 / 16` 仍是确定的退避阶段；
2. 到达最后一个正间隔后，`16s` 成为退避上限，而不是隐式最大尝试数；
3. 后继尝试继续消费同一个 `deadline = started + retry_budget`；
4. 只有剩余预算严格足以支付下一次 sleep，并为后继请求留下正剩余时间时，才允许继续；
5. 每次请求的 timeout 仍取单次上限与当前剩余预算的较小值；
6. 空退避表仍表示不重试；以零结束的自定义退避表不得形成零等待忙循环；
7. `404`、证书验证失败、非法配置、摘要不一致与已存在目标继续立即失败；
8. 每次尝试继续使用独立 owned partial，失败即清理；只有 SHA-256 相等的完整字节才可不覆盖地发布。

因此本修正只扩大**可用性恢复对既有预算的实际利用率**，不扩大错误接受集合：

```text
recovery window utilization
!=
integrity relaxation
```

## 4. 本地确定性证据

使用假时钟与脚本化下载结果新增两个单变量反例：

- 五次 HTTP 500 后第六次成功：sleep 为 `2 / 4 / 8 / 16 / 16`，第六次发布精确字节；
- 六次 HTTP 500：同样完成五次 sleep 后，因剩余 14 秒不足以支付下一次 16 秒退避而以
  `RetryBudgetExceeded` 停止，没有目标文件或 partial 残留。

下载状态机定向测试当前为 12 项，并已在以下四组全部通过：

```text
Python 3.10.6          12/12
Python 3.10.6 -O       12/12
Python 3.13            12/12
Python 3.13 -O         12/12
```

既有用例继续证明 404、证书错误和摘要不一致不重试，connection reset/timeout 可恢复，所有尝试共享一个
deadline，绝对截止时间之后返回的成功字节不得发布，目标不覆盖且 partial 必须清理。

在显式绑定当前工作树的 Core、Starter 与 GitHub Evidence Plugin 源码坐标后，本候选还取得：

```text
Core regression
Python 3.10.6          417/417
Python 3.10.6 -O       417/417
Python 3.13            417/417
Python 3.13 -O         417/417

GitHub Evidence Plugin
Python 3.10.6          180/180
Python 3.10.6 -O       180/180
Python 3.13            180/180
Python 3.13 -O         180/180
```

同一代理环境中的 fresh anonymous live probe 又由当前下载器读取 exact `v0.12.0` wheel，在第一次尝试
1.219 秒内成功，并重新得到冻结 SHA-256
`d0293f06e6a2b0271870ce032b2197c6ef7956db0ff3889230ca48234ff2fa45`。该成功只证明此时公开资产可读且
摘要成立，不覆盖 exact-main 历史门禁中的五次 HTTP 500。

第一次 Core 3.10 普通回归没有绑定当前工作树 `src`；测试源来自本候选，但 Python 实际从旧
`veritrail-r0-review-plugin` editable install 导入 Core 0.12.2，产生 343 项中的导入错误、版本错配与旧
生命周期断言失败。该运行只证明 execution provenance 错配，不能归因给本补丁，也不构成通过证据。后继
运行先读回三套模块的 `__file__` 均属于当前工作树，再从头得到上述有效结果。

一次直接 Starter 0.2 测试又错误地把该入口产品绑定到当前 Core 0.13 源码；Starter 的冻结兼容 lane 明确
要求 Core `>=0.12,<0.13`，所以产生的 `CORE_INCOMPATIBLE` 不属于产品回归。该无效组合没有通过放宽
Starter 版本边界处理；正确的 Core 0.12.2 clean-install lane 仍由既有远端门禁复验。

## 5. 后继门

以上只是本地候选证据。后继必须保持独立因果链：

```text
component correction PR
-> original Public CI 11/11
-> protected-main merge
-> new exact-main Public CI 11/11 + Browser Smoke
-> Q0 docs-only closure rebuilt from that exact main
-> closure PR original Public CI 11/11
-> protected-main merge
-> final exact-main gates
-> fresh anonymous product readback
```

在这条链全部成立前，当前状态保持：

```text
Q0_FREEZE_CLOSURE_HELD
Q_IMPLEMENTATION_NOT_STARTED
NO_GATE_SKIP_AUTHORITY
README_RESTRUCTURE_NOT_STARTED
R1_SCHEMA_NOT_RESUMED
```

旧失败不通过 rerun 洗白；README 读者骨架、SVG 和 R1 Schema 不能叠加进本修正分支。
