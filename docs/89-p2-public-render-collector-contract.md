# P2 Public Render Collector 施工合同 0.1

> 状态：`P2_CONTRACT_0.1_FROZEN`
>
> 后继实现状态：`P2_FROZEN / P3_NOT_STARTED`
>
> 精确施工基线：`cdc2c250f21b37a0be9f815295f7b7c3c5081d0d`
>
> 基线 Tree：`6643e311a61f7ef6a4c8854a61c004f5d67c2742`
>
> 最终合同候选：`cdb589125ddbb8554f9a7bb77fc35482536bd5d1`
>
> 受保护主线合同基线：`8c624ec3aa83fe462e3578d8aa215e8ef9908332`
>
> 合同基线 Tree：`ddc84f65408831b6cd62640b572594e51fc1cc63`
>
> Pages 根坐标修正候选：`220765010b51a12cc2393e0c95439022fe893907`
>
> 修正后受保护主线基线：`4d0edfc8b94e7b8c8a07d47b61a25c8758725c2a`
>
> 修正后基线 Tree：`0bf3bd4fc43062b070c567d96be84f30e3c266ca`
>
> Response-budget 修正候选：`a769b338bc4928c489ce5bdcddcaef22e5ec56f5`
>
> Response-budget 受保护主线基线：`55babcf2171baa29db3718d53f6abc46885c23e4`
>
> Response-budget 基线 Tree：`5a8db1a68d7592f507948476aefc929e58a194ef`
>
> 影响层级：`L2_CONTRACT + L3_SYSTEM / DESIGN_ONLY`
>
> 本合同只冻结公开渲染观察语义；后继实现事实见
> [文档 90](90-p2-public-render-collector-freeze-candidate.md)，P3 handoff、标签与 Release 仍未创建

## 1. 本轮裁决

P1 已冻结只读 Structured GitHub API Collector。P2 只补同一 GitHub 信任域中的另一个观察面：

> 能否从 sealed AcceptancePlan 机械派生一个有界、匿名、只读的公开页面观察请求，并在全新的非持久
> Chromium Context 中，把 GitHub README、Release 或默认 GitHub Pages 的渲染结果规范化为 Core 可
> 独立读取的 Evidence？

P2 不证明页面内容在终极意义上真实，不把 GitHub API 与公开页面说成两个独立权威，也不以浏览器
`goto` 成功代替页面内容正确。它更不负责把 API/Render 事实配对后直接宣布通过；P3 才负责正式
handoff 与完整正负 Verdict 链。

本合同已先于实现完成受保护主线合入与匿名公开读回。冻结没有创建 P2 源码、Schema、CLI、CI job 或
安装依赖；实现仍须从新的 exact-main worktree 独立开始。

## 2. 分层、权威与唯一所有权

```text
sealed AcceptancePlan
        │  owns expected values, required Evidence and assertions
        ▼
Plan-to-render-request derivation 0.1
        │  derives coordinates and projections only
        ▼
GitHub Public Render Request 0.1
        │  says where and what to observe; does not claim success
        ▼
Render Collection Session
        │  owns one bounded browser execution and provenance window
        ▼
Public Render Collector
        │  navigates, scopes, extracts and normalizes; never judges
        ▼
Evidence 0.1 · platform.github.public-render
        │
        ▼
VeriTrail Acceptance Core
             owns binding, sufficiency, integrity, assertions and Verdict
```

| 对象 | 唯一权威 | 明确不得拥有 |
| --- | --- | --- |
| sealed AcceptancePlan | 期望值、Evidence requirement、观察规格、断言与 Seal 决定 | 页面事实、浏览器状态 |
| derivation contract | Plan 字段到 render request 的机械映射 | 新期望、自由选择器、网络行为 |
| Render Policy | 浏览器引擎、资源、网络、稳定窗口和容量上限 | 验收答案、通过/失败规则 |
| request | 公开目标坐标、固定投影、视口和字面观察项 | `expected.*`、Verdict、采集成功声明 |
| collection session | 一次实际采集、串行顺序和 monotonic 窗口 | 可信时间、事实语义、跨次观察合并 |
| Collector | 浏览器观察、固定作用域抽取、规范化和 provenance | Plan 改写、GitHub 写操作、Core Verdict |
| Acceptance Core | Evidence 绑定、充分性/完整性/断言和 Verdict | 浏览器、GitHub 私有解析、网络调用 |

必须继续保持：

```text
Navigation Success != Correct Content != Complete Observation
Anonymous Initial State != Zero Cookies After Navigation
Same Session != Atomic Snapshot != Same Evidence
API Evidence != Render Evidence
Fact Identity != Evidence Identity != Request Identity
```

## 3. 代码与依赖边界

P2 实现只能在既有独立插件包内新增公开渲染能力：

```text
plugins/github-evidence/
  src/veritrail_github/
    public_render_contracts.py
    public_render_collector.py
    paired_collection.py
  tests/
    public_render/
```

允许依赖：

- Python 标准库；
- 插件已经使用的 Core 公共 AcceptancePlan、seal 与 Evidence 0.1 合同；
- 插件公开的 P1 `GitHubCollector` 构造边界；
- `playwright==1.62.0` 和该版本预置、匹配的 bundled Chromium；
- 测试中的本地 fixture server，以及冻结门中的公开 `github.com` / 默认 GitHub Pages 只读页面。

禁止：

- 修改 `src/veritrail/browser.py` 或把 P2 塞进 M2/M3 的 ExperimentPlan Browser Adapter；
- Core 导入 `veritrail_github`，或插件导入 Core 私有符号；
- 复用用户浏览器 Profile、登录态、扩展、系统 Cookie、storage state 或默认持久 Context；
- 接受任意 URL、任意 host、CSS/XPath selector、正则、JavaScript、`eval`、点击、输入或上传；
- 启动 Shell、读取本地文件、下载文件、打开外部应用、写 GitHub 或修复平台状态；
- 把 screenshot、console 是否报错、HTTP 200 或某个 DOM 选择器存在压成 Verdict-like boolean；
- 为 P2 修改 P1 facts、Core Assertion 语义、Workbench、Starter、Authoring Skill 或 R0 合同；
- 在 P2 生成正式 AcceptanceBundle、发布标签、Release、轮询器或定时监控。

Collector 不得在运行时下载浏览器、调用 `playwright install`、包管理器或系统 Chrome。浏览器安装是
显式的部署前提；preflight 只能验证匹配 binary 已存在，不得为了“自动修好环境”扩大执行权限。

插件卸载后，Core、P1、历史 Evidence 与旧消费者必须继续工作；P2 不得成为 Core 的隐式依赖。

## 4. Plan-to-render-request derivation 0.1

P2 只接受 Core 公共 validator 已验证且 seal 可重算一致的 `AcceptancePlan 0.1`。适用
`observation_specs[]` 必须声明：

```json
{
  "id": "github-public-readme",
  "contract": {"id": "github-public-render-request", "version": "0.1"},
  "evidence_type": "platform.github.public-render",
  "coordinates": {
    "owner": "NoctilumeDev",
    "repository": "VeriTrail",
    "target_kind": "GITHUB_MARKDOWN_FILE",
    "target_commit_sha": "cdc2c250f21b37a0be9f815295f7b7c3c5081d0d",
    "repository_path": "README.md",
    "viewport_profile": "DESKTOP_1365X768"
  },
  "projections": [
    "content.rendered_text_signature",
    "content.scope",
    "navigation.identity"
  ],
  "canonicalization_profile": "veritrail-json-c14n/1"
}
```

该示例 spec 已由当前 Core 0.12.2 公共 `observation_spec_digest()` 在 Python 3.10/3.13 独立复算为：

```text
fcdaaf5428814d2556426fdf0626199e0400f386172de764203ead7f0e6c28d8
```

完整向量保存在
[`plugins/github-evidence/examples/public-render-acceptance-plan.json`](../plugins/github-evidence/examples/public-render-acceptance-plan.json)。
两套 Python 对它得到同一 Plan seal
`d08e2da6b665ebedaa1032eaf9834950a3d1e984b5b7c9e31f3d63d5ec4097ae`。这两项是 P2 实现必须保留的
公开兼容向量；它们不代表页面已经采集。

derivation 必须在启动浏览器前：

1. 重算 sealed Plan digest；
2. 校验 observation spec、目标类型、坐标、投影、视口和字面观察项；
3. 由坐标生成唯一目标 URL，不接受 request 自带 URL；
4. 对投影和字面观察项作确定性规范化；
5. 生成独立的 `observation_spec_digest`、Policy digest 与 request seal；
6. 拒绝未知字段、未知能力、复制的 `expected.*`、凭据和执行文本。

Plan 可以声明“哪些 Evidence 字段满足条件”，request 只能声明“采哪些事实”。字面观察项是被检索的
对象，不是“必须存在”的答案；Collector 输出出现次数和作用域事实，是否满足仍由 Core assertion 决定。

### 4.1 Render Request 0.1

request envelope 至少包含：

```text
schema_version = 0.1
request_id
plan_digest
derivation_contract { id, version }
observation_spec
observation_spec_digest
render_policy
render_policy_digest
canonicalization_profile = veritrail-json-c14n/1
seal { algorithm = sha256, digest }
```

`viewport_profile` 与可选 `literal_markers` 都是 `coordinates` 的受限字段，不得扩张 AcceptancePlan 0.1
已冻结的 observation spec 顶层。`observation_spec_digest` 只绑定 render contract/version、结构化目标
坐标、规范化投影、viewport profile 与字面观察项；不得包含 Plan digest、request ID、Policy、session、
浏览器实现或墙钟时间。

`render_policy_digest` 只绑定实际执行边界：

```text
engine = CHROMIUM
playwright_version = 1.62.0
browser_distribution = BUNDLED_MATCHING
headless = true
java_script_enabled = true
accept_downloads = false
network_profile = github-public-readonly/0.1
navigation_timeout_ms = 30000
scope_timeout_ms = 10000
settle_delay_ms = 1000
sample_count = 3
sample_interval_ms = 500
max_redirects = 10
max_requests = 512
max_main_document_response_body_bytes = 8388608
max_total_response_body_bytes = 33554432
response_body_read_chunk_bytes = 65536
content_encoding = IDENTITY_ONLY
max_elapsed_ms = 45000
retries = 0
service_workers = BLOCK
http_cache = DISABLED
```

Policy 不得携带 expected value、marker 是否应出现、用户名、代理 endpoint、任意 host 或自由 browser args。
request seal 对除 `seal` 自身外的完整 request envelope 计算；`request_id` 因而属于 request instance 身份，
但不属于 observation/fact identity。`collection_session_id` 只在执行开始时产生，绝不能预写进 request。

### 4.2 0.1 不采集的对象

P2 0.1 不生成 screenshot、PDF、video、trace、HAR、raw HTML、完整正文或 accessibility tree。以后若要加入，
必须另立 Artifact、大小、脱敏、身份和清理合同；不能把它们偷偷塞进 Evidence metadata。

## 5. 公开目标坐标

P2 0.1 只允许由结构化坐标生成以下四类 HTTPS 目标：

| `target_kind` | 必需坐标 | 唯一生成目标 |
| --- | --- | --- |
| `GITHUB_REPOSITORY_README` | `owner`, `repository` | `https://github.com/{owner}/{repository}` |
| `GITHUB_MARKDOWN_FILE` | `owner`, `repository`, `target_commit_sha`, `repository_path` | exact commit blob 页面 |
| `GITHUB_RELEASE` | `owner`, `repository`, `release_tag` | `https://github.com/{owner}/{repository}/releases/tag/{tag}` |
| `GITHUB_PAGES_DEFAULT` | `owner`, `repository`, `site_kind`, `pages_path` | GitHub 默认 `github.io` 域名；空字符串精确表示站点根路径 |

所有目标还必须在 `coordinates` 中携带一个允许的 `viewport_profile`；只有请求
`content.literal_markers` 时才允许并要求 `literal_markers`。其余 target-specific 字段出现即拒绝，不能
因为字段“暂时用不到”而静默忽略。

约束：

- `owner` / `repository` 精确复用 P1 冻结的保守子集：owner 为
  `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$`，repository 为 `^[A-Za-z0-9_.-]{1,100}$` 且不以 `.git`
  结尾，并额外拒绝 `.` / `..`；不接受通配符、URL、userinfo、端口或 host；
- `target_commit_sha` 必须是 40 位小写十六进制；Markdown 永久链接不得用 branch/tag 替代 exact SHA；
- `repository_path` 必须是非空相对 POSIX 路径，拒绝 `..`、控制字符、反斜杠、预编码分隔符和空路径段；
- `pages_path` 只有两种合法形态：空字符串精确表示站点根路径，或满足上述约束的非空相对 POSIX 路径；
  `/`、`.`、`./`、尾随 `/` 和其他“依赖 redirect 才回到根”的写法均拒绝，不能用 `index.html` 冒充 `/`；
- `release_tag` 复用 P1 的 `^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$` 子集，拒绝空/`.`/`..` 路径段与
  连续 `/`；固定 encoder 逐段编码并保留合法 slash 层级，不接受预编码 URL 或查询参数；
- `GITHUB_PAGES_DEFAULT` 的 `site_kind=OWNER` 时要求 repository 大小写不敏感地等于
  `{owner}.github.io`；空 `pages_path` 生成 `https://{lowercase-owner}.github.io/`，非空时生成
  `https://{lowercase-owner}.github.io/{pages_path}`。`site_kind=PROJECT` 的空路径生成
  `https://{lowercase-owner}.github.io/{repository}/`，非空时才在其后追加编码后的 `pages_path`。
  它只允许这两种默认 `github.io` 坐标；自定义域名、CNAME 重定向和任意站点均推迟到后继合同；
- 所有查询值和 fragment 都禁止出现在请求坐标中。

exact commit Markdown 提供不可变的源坐标；它在 GitHub 上的公共 HTML 仍是带采集时间、renderer 与
平台实现语境的一次 Render observation，不得宣称为不可变渲染。repository 首页 README 是默认分支的
当前公开展示面。两者不能互相替代：`source coordinate stability != render stability`。GitHub 关于永久文件
链接和 README 展示的公开规则见：
[permanent links](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files)
与 [about READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)。

## 6. 投影、视口与固定作用域

### 6.1 投影

`projections` 是去重、有序无关的固定能力集合：

```text
navigation.identity
document.identity
content.scope
content.headings
content.links
content.literal_markers
content.rendered_text_signature
```

P2 0.1 不接受自由 selector。目标类型决定唯一内容作用域：

| 目标 | 固定作用域 | 要求 |
| --- | --- | --- |
| repository README | `article.markdown-body` | 必须恰好一个 |
| exact Markdown file | `article.markdown-body` | 必须恰好一个 |
| Release | `main .markdown-body` | 必须恰好一个 |
| default Pages | `main` | 必须恰好一个；0 个或多个不回退到整页 `body` |

缺失或多重作用域不会抹掉已经取得的 navigation facts，但内容投影不得标记 `COMPLETE`。

### 6.2 字面观察项

`content.literal_markers` 适用时，spec 可携带最多 `32` 个 UTF-8 字面字符串，每个规范化后为
`1..256` 个 Unicode scalar；拒绝正则、selector、脚本和空白-only 值。Collector 只输出：

```text
literal
rendered_text_occurrences
```

`literal` 本身与固定作用域的 `innerText` 使用 8.3 节同一 normalization profile。随后在规范化正文中按
Unicode code point 执行大小写敏感、从左到右、不重叠的精确子串计数；命中后下一次搜索从本次命中末尾
继续。`rendered_text_occurrences` 只保存该确定性计数。它不叫 `marker_ok`，也不承诺该文本在首屏、没有
被遮挡或一定被人看见。

### 6.3 视口

P2 0.1 只允许：

```text
DESKTOP_1365X768  = 1365 × 768, device_scale_factor 1
NARROW_390X844    = 390 × 844, device_scale_factor 1
```

viewport profile 属于 observation spec 和 fact identity，因为响应式页面可在不同视口呈现不同内容。
两者都明确使用 `is_mobile=false / has_touch=false` 与 bundled Chromium 默认 UA；`NARROW` 只证明窄视口
响应式渲染，不冒充真实手机设备。固定浏览器环境还包括 `en-US` locale、`UTC` timezone、light color
scheme、reduced motion、无地理位置和空 permission set。

P2 对元素只使用明确命名的 `playwright_visible` 与 `in_initial_viewport` 事实，不使用含混的
“human visible”。Playwright 的 visible 语义要求非空 bounding box 且不为 `visibility:hidden`，但
`opacity:0` 仍可被视为 visible；该限制必须保留，不能包装成更强的人眼可见性声明。参考：
[Playwright actionability](https://playwright.dev/python/docs/actionability#visible)。

`in_initial_viewport` 固定定义为：在最终主文档导航完成后、Collector 未执行任何滚动或交互时，元素的
CSS-pixel bounding box 与初始 viewport 矩形 `[0,width) x [0,height)` 存在正面积交集。仅接触边界、空
bounding box 或无法取得 bounding box 均为 `false`；它不要求元素完整落入 viewport，也不替代
`playwright_visible`。该字段属于三次规范化样本，位置事实不一致同样使稳定窗口为 `PARTIAL`。

## 7. 匿名浏览器与网络边界

### 7.1 Fresh Context

每次执行必须启动新的 Chromium process 与 non-persistent BrowserContext：

- 不提供 `user_data_dir`、`storage_state`、Cookie、Authorization、client certificate 或代理凭据；
- 首次导航前读取 context storage state，证明 cookies 与 origins 均为空；非空则联网前拒绝；
- 导航后网站自行设置的匿名 Cookie 只记录安全计数与分类，不反推“已经登录”；
- 不复用前一次 context、HTTP cache、service worker、页面或下载目录；
- 最终 Evidence 只声明 `ANONYMOUS_FRESH_CONTEXT`，不记录本机账号、Cookie 值或浏览器 Profile 路径。

Playwright 的 non-persistent context 不与其他 context 共享 cookies/cache；P2 仍必须自己验证初态，而
不能只因调用了 API 就宣称匿名。参考：
[BrowserContext](https://playwright.dev/python/docs/api/class-browsercontext)。

### 7.2 网络策略

Collector 在 context 级路由所有请求；路由会关闭 HTTP cache，service worker 必须设为 `block`。0.1：

- 只允许 `GET` / `HEAD`，所有 `POST` / `PUT` / `PATCH` / `DELETE` 等方法阻断并记录；
- WebSocket、download、popup、新页面和外部协议全部阻断；
- GitHub.com 主文档只允许 exact `github.com:443`；它的只读子资源只允许 exact `github.com`、
  DNS label 边界匹配的 `*.github.com`、`*.githubassets.com` 与 `*.githubusercontent.com`；字符串后缀相似
  但不处于 label 边界的 host 必须拒绝；
- default Pages 只允许目标同源 `GET` / `HEAD` 子资源；
- redirect 每一跳都重新校验 scheme、host、port、userinfo、目标类型与最大跳数；requested coordinate 与
  final coordinate 必须分别保留。即使最终仍在允许域内，owner、repository、path、tag 或 Pages site
  coordinate 经目标类型规范化后发生语义变化，也必须形成显式 conflict，不能把 repository rename、
  transfer 或其他 canonical redirect 透明洗成原请求坐标；
- 最终主文档 response body 与本页全部可渲染 response body 必须由 Chromium CDP 响应阶段拦截执行
  `8 MiB / 32 MiB` 硬上限；超限立即停止加载、关闭 context、关闭未完成 stream 并形成 `ERROR`，不能
  只在完整响应或整页进入内存后才检查；
- 意外 read host 必须阻断并使 coverage 非 `COMPLETE`；预期被阻断的 telemetry write 不自动降低 coverage；
- 不保存原始 headers、body、Cookie、query values、HAR、trace 或完整 DOM。

Policy 默认上限：一页、零重试、最多 `10` 次 redirect、`512` 个网络请求、`8 MiB` 最终主文档
response body、`32 MiB` 全页 response body 与 `45_000ms` monotonic 总窗口。超过上限不扩大权限或
偷偷重跑；需要重试时必须建立新的 collection session。

#### 7.2.1 Response-body 预算的精确语义

冻结合同原先使用 `max_total_encoded_bytes` 与“encoded transfer”，但这会把至少三种不同对象混在一起：

```text
response body octets
HTTP headers / transfer framing / TLS bytes
Chromium completion-time encodedDataLength
```

P2 0.1 只对第一种建立可执行硬上限。Collector 必须在 `Network.enable` 后以
`Network.setExtraHTTPHeaders` 为全部请求显式设置 `Accept-Encoding: identity`；响应头仍出现非
`identity` 的 `Content-Encoding` 时，必须在读取或交付 body 前 fail closed。计量值固定为 CDP
`Fetch.takeResponseBodyAsStream` 返回的顺序流经 `IO.read` 取得的 body octets：base64 数据先解码，
非 base64 数据按 UTF-8 还原字节。它不包含 request bytes、response headers、HTTP/2/3 framing、TLS 或
服务端在连接关闭前已经进入传输缓冲区但尚未被 Collector 读取的字节，因此不得再命名或展示为
“总线速传输量”。参考 [CDP Fetch](https://chromedevtools.github.io/devtools-protocol/tot/Fetch/)、
[CDP IO](https://chromedevtools.github.io/devtools-protocol/tot/IO/) 与
[CDP Network](https://chromedevtools.github.io/devtools-protocol/tot/Network/)。

每个有 body 的响应必须在 `HeadersReceived` 阶段暂停，逐块读取并先计入一个 session 共享的 monotonic
预算协调器；单次 `IO.read` 请求不得超过 `65_536` bytes。只有响应完整、未越界且通过响应头检查后，
才能以原 status、允许的响应头和逐字节相同 body 交回 Chromium。`HEAD`、`1xx`、`204`、`304` 与
redirect 是无渲染 body 的控制响应，必须以空 body 交回并保留 status/redirect headers，不能走一个
不受预算约束的透明 continue 路径。该响应替换属于已声明的 observer effect，必须进入 Policy
provenance；它不冒充未经拦截的原生网络时序。

预算首次越界允许 Collector 为判定多读取至多一个受限 read chunk；浏览器/内核已在途缓冲也可能使
服务端发送量略高于阈值。P2 的“硬上限”准确承诺是：越界 body 不会被完整物化或交付给 renderer，
Collector 会停止页面并关闭 context/stream，且慢速生产端夹具必须证明完整响应没有发送完成、连接已
被中断。它不承诺在 TCP/TLS 线上恰好第 `8_388_608` 或 `33_554_432` 个字节处断线。

`Network.dataReceived`、`Network.streamResourceContent` 与 `Network.loadingFinished.encodedDataLength`
可以作为诊断 provenance，但不能承担硬截断权威。设计期反例已证明大脚本的 `dataReceived` 可能在
服务端完成全部响应后才把足够事件交给客户端；`loadingFinished` 按定义更是完成事件。实现不得因为
这些事件最终给出正确总数，就把事后观察改写成实时控制。

代理只属于运行时 provenance：允许由明确 CLI/runtime 参数给 Chromium 提供 `http(s)` 出口代理，但它
不得进入 observation/fact identity，也不得从系统全局配置隐式推断认证信息。Evidence 只记录
`DIRECT | EXPLICIT_PROXY` 和脱敏代理类别，不记录 host、端口、用户名或密码。

## 8. 导航、稳定窗口与内容规范化

### 8.1 导航不是 Verdict

`page.goto()` 返回最终主文档 Response 时，Collector 保存 requested URL、每跳 URL 的安全规范化形式、
final URL、top-level HTTP status 与规范化 media type。Playwright 对 `404`/`500` 不会像网络失败那样
自动抛错，因此：

```text
HTTP 404/500 + 可取得 Response
    -> 可以形成 COMPLETE navigation observation
    -> HTTP status 作为事实交给 Core assertion

DNS/TLS/timeout/browser crash/no final Response
    -> ERROR
    -> 不得用旧页面、缓存或最近成功 Evidence 代替
```

内容投影只接受最终主文档 media type 为 `text/html` 或 `application/xhtml+xml`。其他 media type 仍可
保留 navigation facts，但内容 coverage 非 `COMPLETE`。稳定窗口中若 main frame 再次导航，必须保留
新的安全 URL/状态并标记冲突，不得把首次 Response 与后来 DOM 拼成一份不存在过的页面。

参考：[page.goto](https://playwright.dev/python/docs/api/class-page#page-goto)。

### 8.2 稳定窗口

`DOMContentLoaded` 与固定作用域出现后，Collector 等待固定 `settle_delay_ms`，再按固定间隔取得三次
作用域样本。只有三次规范化结果全部一致时，内容可被视为本次采集稳定；未稳定则保留各样本 digest，
coverage 为 `PARTIAL`，不得任取第一份或最后一份冒充当前事实。

稳定只说明短窗口内观察一致，不说明 GitHub 原子快照，也不证明 API 与 Render 同时发生。

### 8.3 文本、标题与链接

固定作用域的 `innerText` 只在内存中处理，规范化 profile `github-public-render-facts/0.1`：

1. Unicode NFC；
2. `CRLF/CR -> LF`；
3. 每行内部连续 Unicode whitespace 折叠为一个 ASCII space；
4. 行首尾 whitespace 去除，空行移除；
5. 剩余行以 `LF` 连接。

Evidence 默认只保存文本 SHA-256、UTF-8 byte length、line count 与字面观察结果，不保存整段正文。
作用域文本上限 `524_288` UTF-8 bytes；标题最多 `256` 个，链接最多 `512` 个。超限时保留已观察的
计数、上限和 truncation 原因，coverage 为 `PARTIAL`。

标题按文档顺序保存 `level`、规范化文本、`playwright_visible` 与 `in_initial_viewport`。链接按文档顺序
保存 ordinal、规范化显示文本和解析后的安全目标：

- relative URL 以 final URL 解析；
- `https` 目标保存 origin + path、是否存在 query/fragment，但不保存 query value；
- `mailto`、`tel`、`javascript`、`data` 等只保存 scheme class，不保存 payload；
- userinfo、控制字符或解析失败形成显式 conflict，不静默改写；
- 重复链接按出现次数保留，不能用集合去重抹掉页面结构。

因此，query value 本身明确不在 P2 0.1 的可裁决事实空间内；若 AcceptancePlan 要求比较精确 query，
该 observation spec 必须在联网前判为不受支持，不能拿“query 存在”代替精确目标。

## 9. 事实、Provenance 与摘要身份

`facts` 只保存请求投影需要的规范化字段：

```text
target
navigation
document
content
conflicts
```

其中：

- `target` 保存结构化页面类型与源坐标，不把生成 URL 当作唯一身份；
- `navigation` 保存 requested/final URL、redirect chain 与 top-level status；
- `document` 只保存规范化 `document.title` 与 `html[lang]`；requested page kind 留在 `target`，Collector
  不用 DOM 猜一个新的 kind；
- `content` 保存 scope profile/cardinality、稳定样本、标题、链接、字面项和正文签名；
- `conflicts` 保存无法安全归一的 URL、分类或多重作用域，不把冲突压成空值。

具体 Evidence 的 provenance 另保留：

```text
browser / Playwright implementation version
render_policy_digest
initial_state_check
post_navigation_cookie_count
blocked method / host counters
console / page / request error categories
probe-level monotonic elapsed
collection window
request identity
```

console error、被阻断 telemetry POST 或匿名 Cookie 的出现是观察 provenance，不自动进入 facts 或决定
coverage。若它们阻断了请求投影或越过策略边界，才通过显式 coverage reason 产生影响。

`COMPLETE` 只表示公开页面中选定作用域被完整观察，不表示 GitHub 上的源文件全文已渲染。GitHub 会
截断超过其展示上限的 README；如果 Plan 要证明源文件完整性，必须使用另一个明确的数据来源，P2 不得
拿页面 scope 冒充源码全文。

摘要关系固定为：

```text
observation_spec_digest
  = sha256_json({
      canonicalization_profile,
      contract,
      evidence_type,
      coordinates,
      projections
    })

facts_digest
  = sha256_json({
      canonicalization_profile,
      observation_spec_digest,
      normalization_semantics_version,
      source_coordinates,
      facts
    })

Evidence artifact SHA-256
  = canonical(whole Evidence document)
```

`facts_digest` 不得包含 request ID、Plan digest、request seal、collection session、墙钟时间、代理、Policy、
timeout、blocked telemetry、Cookie count、browser/Playwright version、截图或 console message。相同页面事实
在不同执行中可以有相同 facts digest 与不同 Evidence SHA。

浏览器/API/解析器版本属于 provenance；只有固定作用域、可见性、URL 或文本规范化含义改变时才升级
`normalization_semantics_version`。所有摘要继续使用 `veritrail-json-c14n/1`，不得引入 float/NaN/Infinity。

## 10. Evidence 0.1 映射与 coverage

输出 `evidence_type` 固定为 `platform.github.public-render`。`metadata.veritrail_observation` 写入：

```text
schema_version = 0.1
canonicalization_profile = veritrail-json-c14n/1
plan_digest
observation_spec_digest
request_seal_digest
collection_session_id
collector_role = github-public-render
coverage
normalization_semantics_version = github-public-render-facts/0.1
facts_digest
```

`coverage` 继续只允许 `COMPLETE | PARTIAL | ERROR | NOT_APPLICABLE`：

| Coverage | P2 语义 |
| --- | --- |
| `COMPLETE` | 初态、导航、redirect，以及请求适用时的作用域/稳定窗口和全部投影均在合同上限内完整观察 |
| `PARTIAL` | 已有可用事实，但作用域歧义、未稳定、截断、意外 read host 或部分投影失败 |
| `ERROR` | 浏览器启动、DNS/TLS、timeout、crash、无主文档 Response 或产物校验失败 |
| `NOT_APPLICABLE` | 为兼容 Core Evidence 公共枚举而保留；P2 0.1 Collector 不主动产生 |

P2 0.1 的合法 sealed spec 对其合法 target 必然适用。未知 target、缺字段、不受支持投影或不合法坐标必须在
联网和创建 session 前拒绝，不能被改写成 `NOT_APPLICABLE`。未来只有新合同显式冻结 applicability 条件后，
Collector 才能产生该状态。

以下情况单独不改变 `COMPLETE`：

- top-level HTTP `404`/`500` 已完整观察；
- GitHub 页面发起但被策略阻断的 telemetry POST；
- console 出现不影响请求投影的 error；
- 站点在 fresh context 导航后设置匿名 Cookie；
- 标题位于首屏以下，但请求只要求文档内 rendered text。

Coverage 描述“有没有按合同观察完”，不是“观察结果好不好”。Collector 禁止生成：

```text
page_is_current
render_matches_api
all_markers_present
release_is_correct
public_delivery_passed
```

## 11. API / Render 同会话关系

P0 文档中的“same sealed request”在 P1/P2 分成两种 observation spec 后不再适用。0.1 的 governing
refinement 是：

```text
same sealed AcceptancePlan
        +
same plugin-created collection_session_id
        +
separate P1 API request seal
        +
separate P2 Render request seal
```

P2 可以在插件内新增薄的 `PairedCollectionCoordinator`，但它只能：

1. 接受同一 sealed AcceptancePlan 机械派生的一个 P1 request 与一个 P2 request；
2. 内部生成不可由 caller 提供的全新 `collection_session_id`；
3. 把同一 session factory 注入已公开支持该边界的 P1 Collector 与 P2 Collector；
4. 固定按 `P1 API -> P2 Render` 严格串行采集，并分别原子发布两份标准 Evidence；
5. 返回两份 Artifact 路径与安全的执行 provenance。

它不得拼接 facts、挑选“最好看”的产物、生成匹配布尔值、调用 Core 或输出 AcceptanceBundle。同一 session
只是相关性窗口，不是 GitHub 原子快照。不同 session 的两份 Evidence 即便坐标相同，也不能冒充同一次
观察；Core 的 integrity rule 必须能比较两份 Evidence 的 `collection_session_id`，最终正式 handoff 仍在 P3。

两份 request 必须先一起完成离线验证，任一无效则不创建 session。进入 session 后，两侧观察互不作为
另一侧的前置成功条件：API 得到 `ERROR` 时仍应尝试安全的 Render，反之亦然。一个 Artifact 已经原子
发布后，后续失败不得把它删除或重写；结果必须显式暴露缺失/ERROR 对侧，不能只返回成功那份。

## 12. 错误、清理与发布语义

| 条件 | Collector 结果 | 禁止推断 |
| --- | --- | --- |
| Plan/spec/request/policy/seal 不一致 | 启动浏览器前拒绝 | 不得相信外带 digest |
| 非空初始 Cookie/storage | 启动导航前拒绝 | 不得称为匿名 |
| 任意 URL/selector/script/unknown projection | 联网前拒绝 | 不得降级猜测 |
| redirect 越界或进入登录/任意域 | `PARTIAL/ERROR` + chain | 不得跟随到成功页洗白 |
| 允许域内但 final coordinate 与 requested coordinate 语义不同 | `PARTIAL` + 两份坐标 + conflict | 不得把 rename/transfer 当成原坐标成功 |
| HTTP 404/500 + Response | 保留 status 和内容观察 | 不等于 navigation error，也不等于通过 |
| DNS/TLS/timeout/crash/no Response | `ERROR` | 不得复用缓存或旧 Evidence |
| scope 为 0 或多个 | navigation 可保留，content 非 COMPLETE | 不得退回 full body |
| 内容未稳定 | `PARTIAL` + sample digests | 不得选最后一次 |
| 文本/标题/链接/请求上限到达 | `PARTIAL` + truncation | 不得静默裁剪后称完整 |
| 意外 read host | 阻断 + `PARTIAL/ERROR` | 不得扩大 allowlist 临时放行 |
| 被阻断 telemetry write | provenance counter | 不自动等于页面失败 |

最终 Evidence 必须 create-new + atomic publish，不覆盖既有文件。异常、取消或进程终止后，临时 context、
Chromium 进程、staging、download、trace、HAR 和临时代理配置必须为零；P2 没有远端 cleanup 权限。

## 13. 首条纵向切片

P2 0.1 的首个真实闭环固定为：

```text
one sealed AcceptancePlan
    ├─ P1: public repository + exact main SHA API observation
    └─ P2: exact-commit README public render observation

one plugin-created collection_session_id
two independent request seals
two independent Evidence artifacts
desktop viewport
anonymous fresh Chromium context
no screenshots, no login, no custom domain
```

正向目标必须是本仓库受保护主线的 exact commit README；单变量负链至少把 expected literal heading 或
expected content signature 改错，由 Core 在独立测试中得到非 PASS。P2 本身只证明可产生两份可关联、
可校验的 Evidence；完整 handoff 仍不得提前记为 P3 已完成。

## 14. P2 验收矩阵

每个负例只改变一个预注册变量。实现候选必须严格串行：

### 14.1 纯离线合同

1. target kind、坐标、Pages 根路径/非根路径、路径/tag 编码、投影、viewport 与 marker 上限全部在浏览器启动前验证；
2. arbitrary URL/host、query、userinfo、`..`、预编码分隔符、selector、regex、script 和凭据均拒绝；
3. 同一 spec 确定性派生同一 spec digest；Policy/request/session 变化不污染 fact identity；
4. viewport 或 normalization semantics 变化必须改变 fact identity；浏览器实现版本变化不得改变 facts digest；
5. 相同 facts 的两次采集得到相同 facts digest、不同 Evidence SHA；
6. URL 安全表示不保留 query value、userinfo、mailto/tel/data/javascript payload 或个人路径；
7. P0 “same request” 历史表述由本合同显式细化为 same Plan/session + separate request seals。

### 14.2 本地 fixture browser

8. fresh context 初态为空；预置 Cookie 或 storage 单变量负例在导航前拒绝；
9. 页面导航后设置匿名 Cookie：保留安全计数，但仍可证明 fresh initial state；
10. 正常 200、404 与 500 均生成 top-level status 事实；DNS/TLS/timeout/no Response 为 ERROR；
11. `12 MiB` 慢速主文档触发 `8 MiB` response-body 上限：服务端未发送完成、连接被中断、body 未交付；
12. 小主文档引用 `40 MiB` 慢速子资源并触发 `32 MiB` 总上限：同样证明生产端未完成与零越界交付；
13. 同一超限夹具只使用 `Network.dataReceived` 时保留“服务端已完成后才触发”的负证据，不能算硬截断；
14. 服务端忽略 `Accept-Encoding: identity` 并返回 gzip/br/zstd 时在 body 读取/交付前 fail closed；
15. 允许范围内的多资源页面经流式计量与逐字节回放后仍产生正确 status、唯一作用域和正文；无 body
    控制响应使用空 body 回放，不存在透明未计量旁路；
16. 保持同一规范化坐标的 redirect、语义坐标漂移、unexpected host、auth redirect、redirect loop 与超过
    10 跳分别可辨；
17. GitHub-like 页面发起 telemetry POST 和 console error、正文仍完整：阻断 write 且 coverage 不自动降级；
18. unexpected GET host 被阻断并使 coverage 非 COMPLETE；service worker/WebSocket/popup/download 全阻断；
19. 四种 target kind 各自只使用固定作用域；scope 0/multiple 不回退 full body；
20. heading 位于首屏、首屏以下、仅接触 viewport 边界、`visibility:hidden` 与 `opacity:0` 的语义分别按
    `playwright_visible` / 正面积相交规则保留；
21. 固定采集三个样本；仅 `S1 == S2 == S3` 为稳定，任何不一致均为 PARTIAL，不能选择 first/last；
22. 文本超 512 KiB、heading/link/request 上限分别触发显式 truncation；
23. 重复链接保留，relative URL 正确解析，secret-like query value 不落盘；
24. literal marker 与正文使用同一规范化，并按大小写敏感、Unicode code point、非重叠规则只输出
    occurrence，不输出 present/ok/pass；
25. desktop/narrow 两个 profile 分开产生事实，不能将一端结果代替另一端或把 narrow 冒充真实手机。

### 14.3 P1、Core 与旧消费者

26. P1 API request seal 与 P2 Render request seal 不同，plan digest 与内部 session 相同；
27. caller 不能注入 session；同 coordinator 两份 Evidence 可由 Core integrity operand 验证相等；
28. 跨 session 组合由 Core 得到 `INCONCLUSIVE`，插件不得先筛选或改写；
29. P1 既有测试与 facts digest 逐项不漂移；P2 不导入/改写 P1 私有实现；
30. Core 普通/`-O`、双 Python、Starter/Skill、Workbench、M2/M3 Browser 与历史 digest 全回归；
31. 插件卸载后 Core 与 P1 Evidence 继续可读，P2 Evidence 仍是标准 Evidence 0.1。

### 14.4 真实匿名 GitHub

32. exact commit README 在 fresh desktop context 读取 final URL、200、唯一 Markdown scope、heading 与 signature；
33. repository 首页 README 作为 current surface 单独采集，不冒充 exact permalink；
34. Release 页面使用独立 scope；不存在 tag 的 404 仍形成完整 navigation fact；
35. 默认 GitHub Pages 只允许默认域与同源子资源；custom-domain redirect 按合同阻断；
36. 真实 GitHub telemetry write 即使被阻断，也不能因 console noise 抹掉完整正文；
37. 同一 Plan 固定按 P1/API 再 P2/Render 严格串行、同 session、两份 Evidence，Core 可校验相关性；
38. wheel clean install 从 `site-packages` 启动匹配 Chromium，不从 checkout 偷导入；
39. 两个视口、代理/直连可用路径、敏感扫描、browser/staging/download/trace/HAR 残留全部检查。

wheel-only 环境必须使用预先安装且与 `playwright==1.62.0` 匹配的 bundled Chromium；Collector 自动下载
浏览器或回退到系统 Chrome 属于失败，而不是便利功能。

真实网络只作为人工候选冻结门，不能成为依赖 GitHub 永远稳定的唯一 CI 成功条件。CI 主门禁使用真实
Chromium、test-only 注入且公共 CLI/request 不可达的 route fulfill 与冻结的合成 HTML/contract vectors；
不得复制第三方完整页面作为夹具，mock DOM 也不能替代真实 Chromium。

## 15. Semantic Reality Review

Freeze 前必须再问一次“合同是否忠实描述真实浏览器”，而不只检查代码是否忠实实现合同：

- `goto` 成功是否被误写成 HTTP/content success；
- fresh anonymous 是否被误写成导航后 zero-cookie；
- Playwright visible 是否被误写成人眼可见；
- GitHub chrome、README/Release 正文和 Pages `main` 是否被混成同一 selector；
- 被阻断 telemetry 是否被误写成内容不完整，或反过来被完全丢失；
- API 与 Render 是否被误写成两个 authority、同一个 request 或平台原子快照；
- exact permalink 与 current repository surface 是否被互相替代；
- browser version、采集时间和代理是否污染了事实身份；
- custom domain、任意 URL 或登录态是否从“方便”路径偷偷越界。
- response-body payload、encoded wire transfer 与完成事件是否被误写成同一种计量；
- 本地计数器越界是否同时有生产端“未完成 + 被断开”的外部证据；
- response-stage body replay 的 observer effect 是否被保留，而不是冒充原生网络时序。

任何真实反例均可否决既有测试和 CI 绿灯。修正必须显式升级受影响合同/规范化语义，不得在实现里加
隐藏 fallback。

## 16. 设计期只读探针

在本合同写入前，曾用锁定 Playwright 与匹配 Chromium 对本仓库 exact README、main README 和
`v0.12.2` Release 做一次 fresh anonymous、GET/HEAD-only 只读探针。它只用于发现合同反例，不是 P2
Evidence，也不作为实现完成证明。观察到：

- 三个主文档均返回 200，README 有唯一 `article.markdown-body`，Release 使用独立 `.markdown-body`；
- 页面正文可完整出现，同时 GitHub 前端仍尝试 telemetry POST 并产生 console error；
- Context 导航前 cookies/origins 为空，导航后 GitHub 会设置匿名 Cookie；
- 这证明“blocked telemetry != incomplete content”和“fresh anonymous != post-navigation zero cookie”；
- 工具侧内置浏览器控制通道曾不可用，随后成功的独立 Playwright 探针不能覆盖该失败事实；
- 本机 Git 未继承 Windows system proxy，直连远端超时；显式单次代理成功不证明全局网络正常。

这些发现只决定 P2 合同需要表达哪些变量，不能单独证明合同冻结，更不得被包装为 P2 Collector 已实现。

## 17. 出口与停止线

### 合同冻结出口

1. 本文与 README/AGENTS 索引通过文档一致性、链接、敏感信息和越界检查；
2. 候选只含文档，不创建运行代码、依赖、Schema、CLI、CI job、标签或 Release；
3. 候选经独立 PR、required checks、受保护主线合入；
4. 合入后读回 exact `origin/main` SHA；
5. 在未登录公开 GitHub 页面真实读回 README 与本文的候选状态、边界和停止线；
6. 再以 docs-only closure 记录精确冻结坐标，状态才可变为
   `P2_CONTRACT_0.1_FROZEN / P2_IMPLEMENTATION_NOT_STARTED`。

### 实现停止线

合同未冻结前不得实现。合同冻结后，P2 实现必须从新的 exact main worktree 开始，并在第 14 节全部
适用矩阵与第 15 节 reality review 完成前保持 `P2_IMPLEMENTING`。P2 冻结前不得进入：

- P3 Core handoff、正式 AcceptanceBundle 和完整 Verdict pipeline；
- P4 插件独立版本、tag、Release 与公开下载读回；
- Review Attention R1 代码、Corpus 冻结或自动处置；
- 登录态/私有 GitHub、custom Pages domain、任意浏览器脚本或外部真实性锚；
- “页面真实”“用户想法正确”或“未发现问题”的越权结论。

P2 只能把公开渲染变成一份有界、可追溯的观察。现实拥有真相，Plan 拥有验收声明，Core 拥有裁决；
Collector 只拥有它实际看见并能按合同保留下来的事实。

## 18. 合同冻结闭环事实

### 18.1 候选、反例与语义修正

1. 第一份合同候选 `8805377e78b005eb58d912c057edbc61dca7b476` 从精确
   `main@cdc2c250f21b37a0be9f815295f7b7c3c5081d0d` 起步，只改 README、AGENTS、milestones 与本文；
2. Freeze 前外部语义复核否决了“两份相同样本即可稳定”和“exact commit 是不可变渲染面”两处表述，并
   要求冻结 literal occurrence、initial viewport、redirect coordinate drift、`NOT_APPLICABLE` 与配对
   顺序；最终候选 `cdb589125ddbb8554f9a7bb77fc35482536bd5d1` 将七处语义全部收回合同，没有在
   实现里增加兼容 fallback；
3. 修正后固定为三样本全等、source coordinate 与 render observation 分离、大小写敏感的 Unicode
   非重叠字面计数、viewport 正面积相交、requested/final coordinate 并存、0.1 不主动产生
   `NOT_APPLICABLE`，以及 `P1 API -> P2 Render` 串行顺序；
4. 本地第一次 P1 回归命令使用了不存在的下划线目录，第二次又缺少测试 `support` 导入路径，两轮都在
   collection/import 阶段停止，均不计代码失败或通过；绑定当前 checkout 的 Core、插件源码与测试目录后，
   P1 `57/57` 和 Acceptance Core `35/35` 在 Python 3.10/3.13、普通/`-O` 四组全部通过。

### 18.2 远端门禁与受保护主线

1. [PR #38](https://github.com/NoctilumeDev/VeriTrail/pull/38) 第一候选的
   [Public CI run 34009054178](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34009054178)
   attempt 1 在 Python 3.10 `-O` 的既有 M10 生命周期测试中观察到 `12.938s`，超过合同内 `<9s`；普通
   3.10 与整条 3.13 已通过。精确单测随后在本机串行三次以 `5.278s / 5.239s / 5.301s` 通过，紧邻主线
   的同一冻结 Core 也曾通过；未改 `<9s` 阈值或 Core 源码，失败 attempt 保留在 PR 历史；
2. 只重跑失败作业后，run 34009054178 attempt 2 的 11 个 job 全部 `SUCCESS`。该证据支持一次 hosted
   runner/browser 时序偏移，但不把第一次失败改写成未发生；
3. 最终合同 head 上较早的 run
   [34009994100](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34009994100) 因同 SHA 的更新
   run 在 concurrency policy 下被取消，不计成功或失败；最终
   [run 34010024076](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34010024076) 的 11 个 job
   全部 `SUCCESS`；
4. PR #38 以 merge commit `8c624ec3aa83fe462e3578d8aa215e8ef9908332` 合入受保护 `main`，随后
   `origin/main` 精确读回同一 SHA 与 tree `ddc84f65408831b6cd62640b572594e51fc1cc63`。

### 18.3 匿名公开 Render 读回

内置浏览器技能声明路径与本机插件缓存版本不一致，不能作为完成证据。独立读回使用锁定的
`playwright==1.62.0`、matching bundled Chromium、显式出口代理、全新非持久 desktop context 和
`GET/HEAD`-only 路由，目标均绑定 exact merge SHA，而不是 `blob/main`：

1. 第一次读回在导航前访问 `about:blank localStorage` 时触发 origin `SecurityError`，没有产生页面事实；
   context/browser 随后关闭且无 Playwright 残留。第二次改用 `BrowserContext.storage_state()` 检查初态，
   不放宽网络、匿名或作用域边界；
2. [exact README](https://github.com/NoctilumeDev/VeriTrail/blob/8c624ec3aa83fe462e3578d8aa215e8ef9908332/README.md)
   返回 `200`、requested/final URL 相同、唯一 `article.markdown-body`，三次正文摘要均为
   `62a5249944170da4e4f40ea49ff6742f0c9ca5636f97ec80001ed82738785323`；页面实际命中
   `P2_CONTRACT_0.1_CANDIDATE` 与 `P2_IMPLEMENTATION_NOT_STARTED`；
3. [exact 本文](https://github.com/NoctilumeDev/VeriTrail/blob/8c624ec3aa83fe462e3578d8aa215e8ef9908332/docs/89-p2-public-render-collector-contract.md)
   同样返回 `200`、坐标未漂移、唯一正文作用域，三次正文摘要均为
   `82495e1f0e6624004b96ea3895ea44dffaab8d7a83fcce27570a54e0350101d2`；标题、候选状态、实现停止线
   均在真实渲染正文中出现；
4. 两页初始 cookies/origins 均为 `0/0`，导航后匿名 Cookie 数均为 `6`；每页阻断 telemetry write `2`
   次并观察 console error `2` 次，unexpected read host 为 `0`，三样本正文仍稳定完整。关闭后无
   bundled Chromium 残留。这些 noise 没有被抹掉，也没有被误判为正文失败。

上述闭环只冻结 P2 0.1 合同。该阶段仍为 `P2_IMPLEMENTATION_NOT_STARTED`；下一步只能从冻结后的新
exact-main worktree 进入 `P2_IMPLEMENTING`，不得提前进入 P3、P4 或 Review Attention R1。

### 18.4 Pages 根坐标反例与合同重开

实现 worktree 从 `main@c0ec6e29ee9f43e69846535af8b2e79be52a4fc1` 建立后、首个源码提交产生前，
外部语义复核发现冻结合同没有为默认 GitHub Pages 的站点根路径 `/` 定义规范坐标：空字符串会与
“拒绝空路径段”冲突，`/` 不是相对路径，`.` 依赖 redirect，`index.html` 又不是根坐标。该反例会直接
影响 request identity、spec digest、URL derivation 和 fixture，因而否决立即进入实现。

本修正只把 `pages_path = ""` 冻结为 Pages 专用的站点根坐标，并继续拒绝 repository Markdown 的空路径、
尾随斜杠、`.` 和 redirect-based alias；它不开放任意 URL、自定义 Pages 域名、query、fragment 或新
target kind。此前未提交的离线实现草案已经撤回，候选保持 docs-only。

修正候选 `220765010b51a12cc2393e0c95439022fe893907` 经
[PR #40](https://github.com/NoctilumeDev/VeriTrail/pull/40) 的 Public CI
[run 34012098362](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34012098362) 11 项门禁全部
`SUCCESS`，以 merge commit `4d0edfc8b94e7b8c8a07d47b61a25c8758725c2a` 合入受保护 `main`；随后
`origin/main` 与 tree 分别精确读回为该 SHA 和 `0bf3bd4fc43062b070c567d96be84f30e3c266ca`。

锁定 Playwright 1.62.0 与 matching bundled Chromium 在 fresh、匿名、non-persistent desktop context 中
读回 exact merge SHA：README 和本文均返回 200、requested/final URL 相同、恰好一个
`article.markdown-body`，三次规范化正文摘要分别稳定为
`8525538c2279480783c241b05a453679d91585bedc25c8237f4b8ec58b8fbd6e` 与
`781220253e77cf29f27f20406d457d68b4fdf95d20b2298c7af8ba74665ef37b`。README 实际命中修正候选状态；
本文实际命中 `pages_path = ""` 与“Pages 根坐标反例与合同重开”。两页初态 cookies/origins 均为 0/0，
导航后 Cookie 为 6，各阻断 telemetry write 2 次、观察 console error 2 次、unexpected read host 为 0；
关闭后 matching Chromium 进程为 0。noise 没有被抹掉，也没有被解释成正文失败。

该读回只证明 docs-only 修正已进入公开渲染面，不证明 P2 Collector 已实现。该阶段状态恢复为
`P2_CONTRACT_0.1_FROZEN / P2_IMPLEMENTATION_NOT_STARTED`；下一步必须从本 closure 合入后的新 exact
main 开始 optional-capability 与 network-budget feasibility 施工，仍不得提前进入 P3、P4 或 R1。

### 18.5 Response-budget 可行性反例与合同重开

实现分支从 Pages 根坐标 closure 后的 `main@0ab22fbee7bb5e7a7d821c479cc7f3f4a744e332` 建立，先完成
Playwright optional extra 隔离与 matching bundled Chromium preflight，没有创建 Collector。随后按停止线
只做本地慢速生产端可行性探针，发现原文字面不能直接作为实现合同：

1. `Network.dataReceived.encodedDataLength` 对 `12 MiB` 主文档为 0，只有完成事件能给出最终值；对
   `40 MiB` parser-blocking script，即使同步/异步客户端持续泵事件，阈值也在服务端完整发送后才可见；
2. 因此“最终字节数正确”不等于“能在上游完成前硬截断”，`Network.dataReceived`、
   `streamResourceContent` 或 `loadingFinished` 均不得单独承担控制权；
3. 改用 response-stage `Fetch.takeResponseBodyAsStream + IO.read` 后，`8 MiB` 主文档实验在 Collector
   读取 `8_454_144` bytes 时停止；服务端只发送 `8_519_680 / 12_582_912` bytes，`completed=false`、
   `disconnected=true`；
4. `32 MiB` 全页实验在 Collector 读取 `33_554_480` bytes 时停止；服务端只发送
   `33_619_968 / 41_943_040` bytes，同样 `completed=false / disconnected=true`；
5. 使用 `Accept-Encoding: identity`、非 identity 响应 fail closed、response-stage body stream 与受控回放
   后，真实 exact-SHA GitHub README 返回 200、唯一 `article.markdown-body`；149 个响应中 1 个 302 以
   空 body 控制响应回放，其余成功计量/回放，合计 body `7_620_445` bytes、错误为 0。

这组探针只证明候选原语可行，不是 P2 Evidence，也不证明 Collector 已实现。它同时证明原合同的
`encoded transfer` 命名把 response body 与协议/传输层字节混为一谈。本候选因此只重开预算计量语义：
旧的 `max_main_document_bytes / max_total_encoded_bytes` 名称不再合法，改为精确的 response-body
字段；P2 仍保持一页、`8/32 MiB`、45 秒、512 请求、零重试、匿名只读与零越界交付边界。只有本修正
经 docs-only PR、完整门禁、受保护主线、exact-SHA 匿名公开读回和 docs-only closure 后，状态才可恢复为
`P2_CONTRACT_0.1_FROZEN`，实现分支才能重建于新主线并继续。

修正候选的合同提交 `91bdce640ab44efa7be8267b12ae394e9b6995cc` 与 append-only Ledger 提交
`a769b338bc4928c489ce5bdcddcaef22e5ec56f5` 经
[PR #42](https://github.com/NoctilumeDev/VeriTrail/pull/42) 的 Public CI
[run 34015482222](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34015482222) 11 项门禁全部
`SUCCESS`，以 merge commit `55babcf2171baa29db3718d53f6abc46885c23e4` 合入受保护 `main`；随后
`origin/main` 与 tree 精确读回为该 SHA 与 `5a8db1a68d7592f507948476aefc929e58a194ef`，merge parents 也精确包含
此前主线 `0ab22fbee7bb5e7a7d821c479cc7f3f4a744e332` 与候选 head。

内置 browser skill 声明的本地文件仍不存在，不能作为完成证据。独立读回使用锁定 Playwright 1.62.0、
matching bundled Chromium、全新匿名 non-persistent desktop context 与 `GET/HEAD`-only 路由，对 exact
merge SHA 逐页观察：

- README 返回 200、URL 不变、唯一 `article.markdown-body`，三次正文摘要稳定为
  `31500768081b384892367ce599c93fbaec69175ad9017b801709530119a30c68`；候选状态命中 2 次，
  `RA-017` 与 `Network.dataReceived` 各命中 1 次；
- 本文返回 200、URL 不变、唯一作用域，三次摘要稳定为
  `082d401db942181cd7ae316129153ab2207c78aa6b2bffc10d38a883d77fa0db`；“Response-budget 可行性
  反例与合同重开”命中 1 次、`Fetch.takeResponseBodyAsStream` 命中 2 次，新总预算字段命中 1 次；
- Pattern Ledger 返回 200、URL 不变、唯一作用域，三次摘要稳定为
  `0b9eb8f70472a27015cefd07a4560c92cdf057b81d0cb6b6ed7352a9df12b79a`；`RA-017 rev1`、其
  `record_digest` 与 `CapabilitySemantics` 各命中 1 次。

三页初始 cookies/origins 均为 0/0，导航后 Cookie 均为 6；被阻断 telemetry write 分别为 2/3/2，
console error 分别为 2/3/2，unexpected read host 均为 0，关闭后 matching Chromium 和 staging 残留均为
0。noise 没有被隐藏，也没有被解释成正文失败。

这次 closure 只重新冻结 response-body 预算合同和 `RA-017` 账本事实，不证明 P2 Collector 已实现。
该阶段状态为 `P2_CONTRACT_0.1_FROZEN / P2_IMPLEMENTATION_FEASIBILITY_ONLY`；下一步必须从本 closure
合入后的新 exact main 重建实现分支，恢复 optional dependency/preflight 候选，再开始受合同约束的
response-body budget 与 Collector 施工。P3、P4 与 R1 仍未开始。

### 18.6 Freeze Gate 暴露的 M10 清理预算债务

第一次 docs-only closure 候选 [PR #43](https://github.com/NoctilumeDev/VeriTrail/pull/43) 没有获得冻结
资格。其 Public CI [run 34016126981](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34016126981)
在 Python 3.10 `-O` 再次触发既有 M10 Chromium 生命周期测试：5 秒 lifecycle deadline 之后，正常释放与
强制终止确认分别取得一份新的 3 秒相对等待，实测 10.329 秒，超过既有 `< 9s` 边界。该失败与 PR #38
曾观察到的 12.938 秒同向，因而不能继续归为一次性抖动；#43 被明确关闭且未合并，首次红灯没有通过
rerun 洗白。

独立修复 [PR #44](https://github.com/NoctilumeDev/VeriTrail/pull/44) 将清理权限定为一个绝对 3 秒
deadline：`browser.close()` 后只给子进程一个 scheduler slice 发布退出，仍存活时升级为 owned Job
termination，并用同一 deadline 的剩余时间确认释放。它没有调整 5 秒 lifecycle deadline、3 秒清理预算或
`< 9s` 验收阈值。假时钟在修复前稳定复现 6.02 秒双重清理预算；修复后，永久存活进程不超过 3.05 秒，
终止后立即 signalled 的进程不超过 0.1 秒。真实 Chromium 精确生命周期用例在 Python 3.10/3.13 的普通与
`-O` 四条路径均约为 5.17–5.23 秒，四套完整 Core 回归均为 385/385。

这轮本地验证还发现测试文件来自当前 worktree、生产模块却通过旧 editable metadata 导入其他 checkout；
该结果被主动作废，随后所有命令以当前 `src` 重新绑定。两个反例分别以 `RA-018` 和 `RA-019` 追加到
Pattern Ledger，只作为预算语义和执行来源的复核触发器，不自动宣判缺陷，也不启动 R1。

PR #44 的 Public CI
[run 34017648913](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34017648913) 11 项门禁全部
`SUCCESS`，以 merge commit `25ff62f50a01fddc086c41740af802d9c2df0495` 合入受保护 `main`。随后
`origin/main`、tree 与 merge parents 精确读回为该 SHA、`d71b62aef7f7179c4ad3e2490ed4a1af121f57dd`、
此前主线 `55babcf2171baa29db3718d53f6abc46885c23e4` 与候选 head
`1894c7e08a82b72a92bda0a97413e75a01450b8d`。

锁定 Playwright 1.62.0 与 matching bundled Chromium 又从 fresh anonymous non-persistent context 对该
exact main 串行读回：

- README 返回 200、URL 不变、唯一 `article.markdown-body`，三次正文摘要稳定为
  `31500768081b384892367ce599c93fbaec69175ad9017b801709530119a30c68`；当时仍如实显示 response-budget
  correction candidate 与 implementation pause；
- 本文返回 200、URL 不变、唯一作用域，三次摘要稳定为
  `082d401db942181cd7ae316129153ab2207c78aa6b2bffc10d38a883d77fa0db`；反例标题命中 1 次，
  `Fetch.takeResponseBodyAsStream` 命中 2 次；
- Pattern Ledger 返回 200、URL 不变、唯一作用域，三次摘要稳定为
  `78cbef6b12662078261a6e6a2e998a92eee2dcf71164fff3f7f02312218311f0`；`RA-017/018/019 rev1` 与
  RA-018、RA-019 的精确 `record_digest` 均各命中 1 次。

三页初态 cookies/origins 均为 0/0，导航后 Cookie 均为 6；每页阻断 2 个 telemetry write，合同与 Ledger
各保留 2 个 console error，关闭后 matching Chromium 为 0。上述 noise 没有被抹掉，也没有被用来替代
正文事实。新的 closure 必须从 `main@25ff62f...` 独立产生；只有本 docs-only 候选重新通过完整门禁、受保护
主线合入与合入后匿名读回，P2 0.1 才恢复冻结。该闭环仍不证明 P2 Collector 已实现。

### 18.7 Literal marker 公共向量重开

P2 request validator 施工前复算公共向量时发现：第 4 节示例在未请求
`content.literal_markers` 投影时仍携带 `literal_markers: []`，而第 5 节要求该字段只有在请求该投影时才
允许并要求。两条规则不能同时成立，旧 spec digest 因而不能继续作为冻结向量。

本轮只删除未适用字段，并保留既有能力边界：未请求 literal-marker 投影时字段必须不存在；请求时字段
必须存在且可包含 0 至 32 个受限字面量。修正后的 spec digest 为
`fcdaaf5428814d2556426fdf0626199e0400f386172de764203ead7f0e6c28d8`。为避免再次出现“只给 seal、不给
被 seal 对象”的不可复算证据，本轮同时加入完整 AcceptancePlan fixture，其 seal 为
`d08e2da6b665ebedaa1032eaf9834950a3d1e984b5b7c9e31f3d63d5ec4097ae`。

该修正不改变 P1、网络预算、浏览器 preflight 或任何运行代码。P2 实现保持暂停；只有修正候选通过完整
门禁、合入受保护主线，并从该 exact main 完成匿名公共读回后，才能另立 closure 恢复
`P2_CONTRACT_0.1_FROZEN`。

### 18.8 Literal marker 公共向量再冻结

修正候选 `9a3ad95485b47f2eca6269eeb7335fbe7e8f249c` 经
[PR #47](https://github.com/NoctilumeDev/VeriTrail/pull/47) 的 Public CI
[run 34022023354](https://github.com/NoctilumeDev/VeriTrail/actions/runs/34022023354) 11 项门禁全部
`SUCCESS`，没有通过 rerun 覆盖首次结果；随后以 merge commit
`c06123446fabac0b75d3bbd20195ad6cd40d596e` 合入受保护 `main`。`origin/main`、tree 与 merge parents
分别精确读回为该 SHA、`edcb661f5b52df87f5f4a57e787d361053734088`、此前主线
`6e0db839a812fcd33da55a25e21bcc33818d49b1` 与候选 head。

内置 browser skill 声明的本地文件仍不存在，不能作为完成证据。独立读回使用锁定 Playwright 1.62.0、
matching bundled Chromium 151.0.7922.34，并为两个目标分别建立 fresh、匿名、non-persistent desktop
context；只允许 `GET/HEAD`，从 exact merge SHA 串行观察：

- 本文返回 200、requested/final URL 相同且恰好存在一个 `article.markdown-body`；三次 NFC 与换行规范化
  正文摘要稳定为 `2186e7d095c10f96a1201596d9fac2ea00e33e52262f8dfe05f1f9f5b0f25ab1`。页面实际显示
  `P2_CONTRACT_0.1_REOPENED / P2_IMPLEMENTATION_PAUSED`，命中新 spec digest、完整 Plan seal 与第 18.7
  节，并确认旧 spec digest 不再出现；
- 完整 AcceptancePlan fixture 页面返回 200、URL 不变，共观察到 94 个 GitHub code cell；三次同规则
  规范化摘要稳定为 `25d7384c577005ef06f5965df3f665ba518f085cec25de66dd5d2f794a5b0f6f`。页面命中
  `github-p2-public-render-fixture`、Plan seal 与 `content.rendered_text_signature`，并确认未出现
  `literal_markers` 字段。

两个 context 的初态 cookies/origins 均为 0/0，页面显示 `Sign in`，导航后 Cookie 均为 6；分别阻断
3/2 个 telemetry `POST`，保留 3/2 个 console error，读请求只到 `github.com`、
`github.githubassets.com` 与 `avatars.githubusercontent.com`。关闭后 matching Playwright Chromium/driver
进程为 0。上述 noise 没有被抹掉，也没有被解释成正文失败。

这次 closure 只重新冻结 literal-marker 投影边界、spec digest 与完整 Plan fixture，不证明 P2 Collector
已实现。该阶段状态恢复为 `P2_CONTRACT_0.1_FROZEN / P2_IMPLEMENTATION_FEASIBILITY_ONLY`；下一步必须
从本 closure 合入后的新 exact main 重新绑定既有 P2 feasibility commits，再继续 request
derivation/URL safety。P3、P4 与 Review Attention R1 仍未开始。
