# Core 0.13.0 Release Candidate 施工计划

> 状态：`C1_IMPLEMENTING / CORE_0.13.0_NOT_RELEASED / P4_BLOCKED`
>
> 精确施工基线：`main@e69f3844254947f795564cb845056652f2dcf3ac`
>
> 影响层级：`L2_CONTRACT`；只把已经冻结的 Acceptance Core 公共能力绑定到新的发行身份，
> 不新增 Acceptance 语义，不重开 P1–P3，不移动任何历史标签或 Release

## 1. 施工目标

[文档 100](100-core-v0.13.0-acceptance-api-release-contract.md)与
[文档 101](101-core-v0.13.0-acceptance-api-contract-freeze.md)已经冻结 Core `0.13.0` 的发布边界。
C1 只建立 release candidate：更新源码发行身份、写出候选说明、修正验证坐标，并证明候选 wheel/sdist
包含既有 Acceptance API 且没有破坏冻结消费者。

C1 不创建 `v0.13.0` tag、GitHub Release 或最终公开资产。最终资产只能在候选经受保护主线合入后，
由 C2 从新的 exact main 重新构建。

## 2. 新发现的消费方坐标缺口

C1 开工前对共享 CI 安装链复核得到：

```text
Core candidate source
    -> 将声明 veritrail==0.13.0

Starter 0.2.0 source / public wheel
    -> Requires-Dist: veritrail>=0.12,<0.13
    -> runtime guard: Core >=0.12,<0.13

GitHub Evidence 0.1.0 source
    -> Requires-Dist: veritrail==0.12.2

现有共享 CI
    -> 先安装 editable Core
    -> 再正常安装 editable Starter 与 GitHub Evidence
```

若只把 Core 版本改为 `0.13.0` 而不改变验证方法，后续 `pip install` 可以拒绝该环境，或用满足旧依赖的
Core 替换候选。即使使用 `--no-deps` 阻止替换，Starter 自身的运行时守卫仍会正确拒绝 Core 0.13.0；
因此 `--no-deps` 不能被用来声称 Starter 源码前向兼容。此时测试结果不能证明实际导入的是当前 C1 Core，
也不能证明 Starter 接受了一个被其冻结合同明确排除的版本。

该问题属于：

```text
TEST_COORDINATE != IMPORT_COORDINATE
SOURCE_FORWARD_COMPATIBILITY != DECLARED_DISTRIBUTION_COMPATIBILITY
DECLARED_DISTRIBUTION_COMPATIBILITY != PUBLIC_CLEAN_INSTALL
```

## 3. 消费方验证坐标

### 3.1 Core 0.13.0 候选坐标

Core 自身回归只接受当前 checkout 或本次构建 wheel/sdist。门禁必须在消费者安装前后显式确认：

- `veritrail.__version__ == "0.13.0"`；
- editable lane 的 `veritrail.__file__` 位于当前 exact checkout 的 `src`；
- wheel/sdist lane 的模块来自新建仓库外环境的 `site-packages`；
- 依赖安装不得把候选替换成其他 Core 版本或其他 worktree。

### 3.2 Starter 0.2.0

Starter `0.2.0` 的公开 wheel/sdist 与依赖 metadata 已冻结，C1 不得在同一版本下静默扩展 `<0.13`。
其运行时 `require_compatible_core()` 也明确执行同一边界。C1 保留三条互不替代的证据：

1. 既有 E3 公共下载门继续使用其已发布、已声明支持的 Core 坐标；
2. Starter 0.2.0 在 exact Core 0.13.0 候选上必须 fail closed，并给出 `CORE_INCOMPATIBLE`；
3. 当前 Starter 0.2.0 源码在仓库外新环境中使用匿名下载且摘要匹配的公开 Core 0.12.2 wheel，完成
   Python 3.10/3.13 normal 与 `-O` 正向合同回归。

第三条只证明 Starter 当前源码仍满足其既有声明范围，不能升级为 Core 0.13.0 兼容证据。若未来需要
正式支持 Core 0.13.0，必须使用新的 Starter 版本与独立发布合同。

Authoring Skill `0.2.0` 的真实 DRAFT 链通过 Starter 的 `doctor/init/validate/review` 入口运行，因此继承
同一 Core `>=0.12,<0.13` 边界。其静态合同测试可在 Core 0.13.0 候选环境中运行，但不能替代真实链
兼容性证据。真实 `single-webapp`、`static-site` 两个 preset 的 normal 与 `-O` 验收必须与 Starter
一起在公开 Core 0.12.2 的独立环境中完成。

### 3.3 GitHub Evidence 0.1.0

插件依赖只能在 Core 0.13.0 完成 C2 公开发布与匿名读回以后，由 P4 从
`veritrail==0.12.2` 更新为 `veritrail==0.13.0`。C1 不修改插件 metadata。

C1 允许插件源码或候选 wheel 以 `--no-deps` 挂接 exact Core 0.13.0 候选，用于证明 P1–P3 代码没有被
Core 新发行身份破坏。该探针必须同时验证 Core 版本与导入来源，并明确不是公开 clean-install 证据。

## 4. 候选改动边界

C1 允许：

- 把 Core `[project].version` 与 `veritrail.__version__` 更新为 `0.13.0`；
- 增加 Core 0.13.0 候选 Release Notes；
- 更新当前状态、文档索引与版本合同测试，但保持公开稳定入口仍为 `v0.12.2`；
- 让 CI 分开标注 Core 候选、Starter 冻结边界、GitHub Evidence 源码前向兼容、历史公开兼容和
  wheel-only 证据；
- 增加 exact version/import provenance 断言；
- 明确 C2 最终资产的固定集合、生成顺序与非自指摘要规则。

C1 禁止：

- 修改 AcceptancePlan、Evidence binding、四 Verdict 优先级或 imported-snapshot 语义；
- 修改 P1/P2 facts、P3 handoff 或把 GitHub 领域语义加入 Core；
- 修改 Starter 0.2.0 或 GitHub Evidence 0.1.0 的依赖 metadata；
- 创建、移动或重制任何标签、Release 或历史资产；
- 把 candidate wheel、CI artifact 或源码前向兼容探针称为公开可安装发行证据；
- 创建插件 tag ruleset、tag、Release、validation summary 或 checksum。

## 5. C2 最低公开资产集合与生成顺序

固定资产集合为：

```text
veritrail-0.13.0-py3-none-any.whl
veritrail-0.13.0.tar.gz
veritrail-workbench-0.13.0.zip
core-v0.13.0-validation-summary.json
SHA256SUMS.txt
```

C1 只冻结名称和生成规则，不冻结最终字节。C2 必须按以下顺序从合入后的 exact main 重新生成：

1. 在 owned temporary root 构建 wheel、sdist 与 Workbench ZIP；
2. 验证版本 metadata、归档路径、重复条目、绝对路径、路径穿越和 clean install；
3. 运行双 Python、normal/`-O`、Acceptance 四 Verdict、imported-snapshot、Workbench 与 Browser Smoke；
4. 生成非自指 `core-v0.13.0-validation-summary.json`，记录 exact commit 与前三项 payload 摘要；
5. 生成 `SHA256SUMS.txt`，只覆盖前四项资产，不覆盖自身；
6. 复验 checksum 后以 create-new 方式上传，随后匿名重新下载并逐字节核验。

任何 C1 构建物只属于候选证据，不能直接上传为 C2 最终资产。

## 6. C1 串行验证矩阵

1. 当前 worktree、branch 与 base SHA 精确；无不相关改动；
2. Python 3.10、3.13 各自运行完整 Core normal 与 `-O` 回归；
3. Core wheel 与 sdist 分别在仓库外新环境 clean install，版本和模块来源精确；
4. Acceptance 四 Verdict 与同一 imported snapshot 纵向门通过；
5. Workbench tests、lint、type-check、build 与 dependency audit 通过；
6. Browser Smoke 与 Windows 生命周期/清理门通过；
7. Starter 0.2.0 对 Core 0.13.0 明确 fail closed，并在公开 Core 0.12.2 独立环境完成双 Python
   normal/`-O` 正向回归；Authoring Skill 0.2.0 的两个 preset 真实 DRAFT 链也在该历史兼容通道完成；
8. GitHub Evidence 源码/wheel 前向兼容探针以 `--no-deps` 运行，并确认 Playwright 仍为 optional extra；
   卸载门验证 distribution 与功能子模块均不可用、Core 仍能复算保留 Evidence，不把仅含解释器缓存的
   空 namespace 目录误报为插件能力；
9. E1/E3 历史公开资产下载与既有 Core 坐标复验继续通过；
10. 敏感信息、绝对本机路径、版本口径与文档链接检查通过；
11. 候选 PR 的原始 Public CI 全部成功，且没有通过 rerun 覆盖第一次失败。

## 7. 停止线与出口

出现以下任一情况必须停止 C1：

- 实际导入 Core 不是 `0.13.0` 或不来自声明的 checkout/wheel/sdist；
- 为获得绿灯必须修改已冻结 Acceptance 语义或放宽既有阈值；
- Starter 0.2.0 意外接受 Core 0.13.0，或 Starter/Authoring Skill 无法在公开 Core 0.12.2 的声明范围内
  完成各自正向回归；
- GitHub Evidence 只能通过改写既有发布 metadata 才能挂接候选 Core；
- wheel 与 sdist 提供的公共 API、版本或行为不一致；
- normal 与 `-O`、Python 3.10 与 3.13、源码与发行物之间出现无法解释的差异；
- C1 试图提前创建最终标签、Release、资产或插件发布坐标。

只有本节矩阵全部成立、候选经受保护主线合入后，才能进入 C2。C1 的出口最多是：

```text
CORE_0.13.0_RELEASE_CANDIDATE_MERGED
CORE_0.13.0_NOT_RELEASED
P4_BLOCKED
NO_CORE_0.13.0_TAG_OR_RELEASE
NO_GITHUB_EVIDENCE_TAG_OR_RELEASE
```
