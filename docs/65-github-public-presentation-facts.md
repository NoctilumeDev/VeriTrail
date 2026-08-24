# GitHub 公共展示面收束事实

> 状态：`COMPLETE / PUBLIC_READBACK_PASS`
>
> 日期：`2026-08-24`
>
> 范围：VeriTrail 仓库首页、README 首屏、About 元数据与三个正式 Release

## 1. 为什么单独收束

代码、测试和 Release 已经成立，不代表第一次进入仓库的人能够迅速理解产品。此次审查把公共展示面
视为发布层，而不是装饰层：访客应当先看到真实产品、理解它解决什么、选择入口，然后再展开里程碑
和冻结事实。

审查前存在四项实际漂移：

- README 在入口之前展开 M0–M14 全部历史，首次阅读成本过高；
- About 没有 Topics，仓库缺少稳定的公共分类信号；
- GitHub 把最后发布的 Authoring Skill 标为整个仓库的 Latest Release，掩盖稳定 Core 坐标；
- Starter 与 Authoring Skill 的 Release 正文仍显示发布前的
  `RELEASE_CANDIDATE / PUBLIC_READBACK_PENDING`，与已完成的 E1 公开读回矛盾。

## 2. 已完成的公共展示改动

- README 首屏加入当前真实 Workbench 的完整桌面视口，不使用设计参考图冒充成品；
- 产品叙事调整为“真实界面 -> 一句话定位 -> 四条入口 -> 发布状态 -> 可展开冻结事实”；
- Core、Starter、Authoring Skill 使用独立版本徽章和独立下载入口；
- M0–M14 详细状态保留在可展开区域，没有删除工程事实，也不再阻塞新读者的黄金路径；
- About 增加 `acceptance-testing`、`end-to-end-testing`、`evidence`、`local-first`、
  `playwright`、`python`、`reproducibility`、`software-quality` 八个 Topics；
- `v0.12.0` 被明确标记为仓库 Latest Release；Starter 与 Skill 仍保留各自独立 Release；
- 两个入口层 Release 正文改用已完成公开读回的文档 64，状态统一为
  `RELEASED / PUBLIC_READBACK_PASS`。

## 3. 资产与读回

README 展示资产为：

```text
docs/assets/veritrail-workbench-catalog.png
1425 x 950
SHA-256 12650EA61EE47723F9E496428439BA75436ADF6618CE8D076C35DF7AFB6984D4
```

该图来自最终 Workbench 验收后的真实 `starter-s1-pass / starter-s1-fail` Catalog 视图。它不包含设计
参考图中的虚构数据，也不宣称 GitHub Pages 在线演示已经存在。

公开 API 读回确认：

- Latest Release 为 `VeriTrail 0.12.0` / `v0.12.0`；
- 八个 Topics 均存在；
- Starter 与 Authoring Skill Release 正文均以
  `RELEASED / PUBLIC_READBACK_PASS` 开头；
- README 经 GitHub GFM 渲染接口确认图片、入口表格与折叠区均进入最终 HTML；
- README 的 53 个本地链接目标全部存在，`git diff --check` 通过。

## 4. 明确保留的边界

- GitHub Pages 当前没有配置，因此 About 不填写虚构 Homepage，也不把本地回环地址写成在线演示；
- 仓库所有者看到的 branch protection 提示是 GitHub 的管理界面，不属于公共 README 视觉缺陷；分支
  保护策略应作为公共工程治理单独决策，不能借展示优化静默修改；
- 此轮没有调用 Codex Security 深度扫描或攻击路径验证。既有 Release 中已经封存的历史验证事实继续
  保留，但新的安全工作流按当前主线决定暂停；
- README 截图只证明界面真实呈现，不替代 Core、Starter、Skill、CI 或 Release 的合同与读回。

## 5. 后续复用规则

其余公开仓库按同一顺序审查：

```text
About / Topics
  -> README 首屏与真实视觉资产
  -> 价值、入口和边界叙述
  -> CI / Release / Demo 坐标
  -> 文档与公开元数据读回
```

没有真实在线演示就不填 Demo；没有真实截图就不放效果图；没有独立发布坐标就不制造版本徽章。
公共展示可以降低理解成本，但不能扩大项目已经证明的能力。
