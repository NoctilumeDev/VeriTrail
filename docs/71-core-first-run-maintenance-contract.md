# Core 无 checkout 首跑维护合同

> 状态：`RELEASE CANDIDATE / PENDING PUBLIC READBACK`
>
> 稳定基线：`VeriTrail Core 0.12.0` @ 不可移动标签 `v0.12.0`
>
> 候选发布坐标：`0.12.1`
>
> 影响层级：Core 公共 CLI／包合同 `L2_CONTRACT`，以及有界公开 CI `L3_SYSTEM`

## 1. 问题

原公共首跑文字先安装已发布 Core wheel，随后直接引用 `examples/minimal/plan.json` 与
`examples/minimal/evidence-pass.json`。这些文件存在于 Git checkout，但不是 wheel 包数据。陌生用户
如果只下载公开 wheel，就无法复现文档里的 Core 首跑。

这是入口合同缺陷，不是 Plan 封存、Evidence 导入、Verdict 计算、Bundle 不可变性或 Catalog 派生
缺陷。整改必须关闭打包缺口，但不能重开已经冻结的 `v0.12.0` 结论，也不能把 Core 改成自动猜项目
的系统。

## 2. 授权变更

候选版可以增加一条命令：

```text
veritrail demo --output <new-directory>
```

它不得要求仓库 checkout、外部示例文件、浏览器、Node.js、网络或第三方运行时依赖。它必须只从
Core wheel 内的常量生成：

1. 一份 sealed 合成 Plan；
2. 一份正向 Evidence 与一份受控负向 Evidence；
3. 使用相同 Plan digest 的一个不可变 `PASS` Bundle 和一个故意 `FAIL` Bundle；
4. 同时收录两个 Run 且 issue 为零的只读 Catalog；
5. 只记录输出内相对路径、边界标记精确为
   `SYNTHETIC_CORE_DEMO_NOT_PROJECT_ACCEPTANCE` 的摘要。

输出目录必须是新路径。命令必须在同一父目录 staging 后原子发布；失败后不得暴露半成品，也不得
覆盖既有路径。

## 3. 禁止扩张

命令不得：

- 探测或分类用户项目；
- 推断启动命令、端口、健康检查、断言或验收标准；
- 观察结果后修改 Plan 语义；
- 批准 Starter 草案、生成 Bootstrap Preview 批准或运行用户项目；
- 授予 Starter／Authoring Skill 任何 Seal、Run、Verdict、Comparison 或 Workbench 权限；
- 把合成 `PASS` 描述成 VeriTrail 自身或任何外部项目的验收证据；
- 移动或改写 `v0.12.0`，或把候选能力描述成已经发布。

## 4. 无 checkout 门禁

公开 CI 必须在正常 checkout job 中构建 Core wheel，并只把它作为短期 workflow artifact 上传。
另一组 Python 3.10／3.13 Windows matrix 随后必须：

1. 不执行 checkout；
2. 证明 workspace 没有 `.git`，也没有任何仓库文件；
3. 只下载对应的已构建 wheel，并以 `--no-deps` 安装；
4. 在 runner 临时目录运行 `veritrail demo`；
5. 验证 `PASS`、故意 `FAIL`、相同 Plan digest、两 Run／零 issue Catalog 与精确边界标记；
6. 拒绝生成 JSON／Markdown 中出现 runner 临时目录或 workspace 绝对路径。

仓库单元测试另行证明覆盖拒绝与失败原子性。Core 全量回归在普通和关闭断言的解释器模式下都必须
继续成立。

## 5. 发布停止线

实现完成和 PR 变绿本身不等于稳定能力。只有同时满足以下条件，才可以准备维护 Release：

- Python 3.10 与 3.13 的仓库既有门禁全部通过；
- 本机独立 clean 环境在仓库外只安装已构建 wheel，并复现同一事实；
- PR 合并且没有移动任何历史标签；
- Release Notes 明确区分合成 demo 与项目验收；
- GitHub 已发布 wheel 被再次公开下载，并在无 checkout 环境读回；
- README、`START_HERE.md`、包版本、标签、Release target、资产 digest 与公开读回事实一致。

进入发布候选以前，稳定 Core 必须保持 `0.12.0`，默认分支源码必须保持 `0.12.1.dev0`。实现门禁、
受保护 PR 与治理规则全部成立后，发布分支才可以把源码固定为 `0.12.1`；在公开 Release 资产完成
下载读回以前，它仍只能描述成维护候选，不能冒充已经公开发布的稳定事实。

## 6. 分支保护边界

候选 PR 建立稳定 check 名称后，`main` 必须增加公开保护规则：禁止 force-push 与删除，并要求通过
Pull Request 和当前 CI。由于这是单维护者仓库，规则不得要求无法完成的自我批准。分支保护属于仓库
治理变化，不改变 VeriTrail 执行或 Verdict 语义。

## 7. 候选实现与门禁事实

- `veritrail demo`、原子发布、边界摘要与覆盖拒绝已经实现；
- Core 在 Python 3.10／3.13 的普通与 `-O` 模式均通过 `341/341`；
- Starter 与 Authoring Skill 在双 Python、普通与 `-O` 模式均通过 `24/24`；
- Workbench 通过 `172/172`、lint、type-check、生产构建与依赖审计；
- 双 Python 公共 CI 已在无 checkout workspace 中只安装候选 wheel，并验证 PASS／故意 FAIL、
  同 Plan、两 Run／零 issue Catalog、边界标记与无本机路径泄漏；
- 本机仓库外 clean venv 也已在 Python 3.10.6／3.13.13 复现同一事实；
- PR #8 已在七项门禁全绿后合并；`main` 已禁止删除／强推并要求 PR 与七项严格检查；稳定 Core
  `v*` 标签已禁止删除和改写。
- 候选合并后的精确 merge commit `81b9625d1246a352287256ff8cb1c3cc3b66de40` 在
  [Public CI 32863463458](https://github.com/NoctilumeDev/VeriTrail/actions/runs/32863463458)
  如实暴露出 Starter S1 浏览器门禁使用 3 秒冷启动窗口的瞬态漂移。整改只把该真实链的单操作
  上限恢复到仓库其他浏览器样例使用的有界 10 秒，并在失败时输出实际裁决、失败断言和短期验收
  artifact；不得用 retry 把失败改写成绿色。

以上只允许切出 `0.12.1` 候选。只有 GitHub Release 资产公开下载、无 checkout 再验证、digest 与
Release target 读回并写入事实文档后，本合同才可改为 `RELEASED`。
