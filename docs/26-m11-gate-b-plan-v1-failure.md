# M11 Gate B Plan v1 首次真实失败

> 状态：`PRESERVED_FAILURE / PLAN_V2_PREREGISTERED / M11_PLANNED`
> 日期：2026-08-14
> 影响层级：`L3_SYSTEM`
> 预注册提交：`2c14393734014e865f447876a2aea9bd3256a2ca`
> 目标：`InkNarratives @ b443a1c967bbc4c50f1bec7ece62abc4c4196fdb`

## 1. 结论

Gate B Plan v1 的首个正向 Run 没有通过，后续三个 v1 Run 未启动。公共 Bundle 的结果是
`BROWSER_HARD_FAILURE / COMPLETED / FAIL`，不是资源中止、Subject 漂移、Core 污染或目标服务失败。

失败目录固定为 `tmp/m11-gateb-contract03-20260814-160143`。该目录包含 v1 positive/negative sealed
Plan、同一 sealed Profile、Preview 与失败 Bundle，必须继续保留；不得把 v2 结果倒填进去。
Catalog 独立验真的失败 Bundle 摘要为
`192efed293e231dd93c6cf840ddc7e7f98c0c9ea35e031d350ad801a8d9b819f`。

## 2. 已成立与未成立的事实

- InkNarratives 本地 HEAD、公开 `origin/main` 与预注册 ref 一致，工作区前后干净，无 `.env`；
- Python 3.10.6 的 owned `http.server` 进入 READY，王维页连续两次返回 200 和 31,741 字节；
- 十次页面文档请求全部 HTTP 200，Console、page error、failed request、4xx/5xx 与横向溢出均为 0；
- 桌面视口 31 个步骤全部通过；移动视口在长卷页第 28 个步骤停止；
- 已生成七张截图，缺少移动端长卷阅读层截图，因此 `capture_complete=false`；
- application/Browser Job、reader、staging、run-work 与 18775 均完成清理，Subject 未变化。

这些事实不能合并成正向 PASS。缺失第八张截图和移动端最后交互已经触发三个 HARD 断言失败。

## 3. 根因与分层判断

Plan v1 规定桌面和移动端都点击 `a[href="#cabin"]`。目标在 `@media (max-width: 760px)` 下把
`.chapter-nav` 设为 `display: none`，所以该元素存在于 DOM，却不是移动用户可点击元素。自动浏览器等待
10 秒后按预注册规则失败。

这是 Gate B 目标交互合同错误：同一个目标页面在两个响应式视口没有同形导航。它没有要求修改
ProjectProfile、Plan Schema、Browser Adapter、collector、状态机或 Verdict；页面内真实书册在两个视口
都可操作。因此不回到新版 Gate A，也不修改 InkNarratives，而是按“观察后变更必须升版本”创建
Contract 0.4 / Plan v2。

## 4. Plan v2 边界

Profile v1、目标 ref、端口、readiness、资源预算、页面顺序、标题、截图点、失败 selector 和裁决均保持
不变。只把两个 Plan 升为 version 2，把长卷页的隐藏导航点击替换为：

1. 验证 `#cabin` 可见；
2. 点击 `.book[data-book="mountain"]`；
3. 验证 `#reader-title` 包含 `空山之后`。

v2 四个 Run 使用全新 ID，从 Run 1 严格串行开始。v2 authority 必须先提交并从 GitHub 读回；如果 v2
再次暴露通用能力缺口，停止 Gate，不继续修订结果。
