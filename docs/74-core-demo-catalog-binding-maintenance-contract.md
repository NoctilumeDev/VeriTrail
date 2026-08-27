# Core demo Catalog 最终位置绑定维护合同

> 状态：`IMPLEMENTING / NOT RELEASED`
>
> 当前稳定 Core：`0.12.1` @ 不可移动标签 `v0.12.1`
>
> 未发布源码坐标：`0.12.2.dev0`
>
> 影响层级：Core `demo -> catalog-serve` 公共组合合同 `L2_CONTRACT`

## 1. 已证明问题

Core `0.12.1` 的 `veritrail demo` 先在输出目录的同级 staging 中生成两个 Bundle 与 Catalog，
再把整个 staging 目录原子改名为最终 demo 目录。Catalog 在改名前把 staging 下 Artifact root 的
绝对位置摘要写入 SQLite 与 Manifest；改名后，官方 `catalog-serve` 会以最终 Artifact root 重新计算
摘要并正确拒绝它，错误码为 `ARTIFACT_ROOT_MISMATCH`。

两个 Run、Verdict、Bundle 摘要、`catalog_id` 与 issue 数均未漂移。缺陷只属于组合 producer 的
位置生命周期；`catalog-serve` 的 fail-closed 校验是正确行为，不得放宽。

## 2. 授权变更

本维护候选只允许：

1. 保留 demo 的同父目录 staging 与整目录原子发布；
2. 由 Catalog 模块内部的受限入口验证 `stage/artifacts -> FINAL/artifacts` 发布映射；
3. 在扫描 staging Artifact 时，从已经解析的共同父目录推导最终 Artifact root 摘要，使 Catalog
   从创建时就绑定最终位置；
4. 只计算一次绑定摘要，并把同一值写入 SQLite 与 Manifest；
5. 保持公共 `build_catalog(artifact_root, output)` 的签名与“绑定实际扫描根”语义不变；
6. 使用新的未发布源码坐标 `0.12.2.dev0`，不得重制 `0.12.1`。

受限入口必须拒绝不同父目录、错误的 `artifacts`／`catalog` 相对布局、已有最终目标，以及 symlink／
reparse staging 或 Artifact root。调用者不能传入任意 binding digest，也不能声称扫描 A 却绑定无关 B。

## 3. 禁止扩张

本合同不得：

- 修改 Catalog Schema、API、`catalog_id`、Run identity 或 Verdict；
- 在发布后直接改写 SQLite／Manifest；
- 让 verifier 自动重绑定、接受 sibling 目录，或为 demo 绕过根绑定；
- 把绝对路径、staging 路径或最终路径明文固化进 Bundle、Catalog、demo 摘要或 CLI 失败输出；
  CLI 成功摘要仍可按既有合同回显用户显式提供的输出参数；
- 改为相对路径或纯内容绑定，从而让整体搬移静默通过；
- 借机重写通用 atomic publication、增加新执行器、修改 Workbench，或开展已封存的深度安全扫描。

现有 `publish_staged_directory` 在恶意同用户并发、POSIX 空目录替换、网络文件系统与父目录被并发
重定向下并不构成完整沙箱或通用 no-replace 原语。Windows 下若另一个同用户进程持续持有 staging
内部文件的共享锁，外层改名与后续删除都可能被操作系统拒绝；候选必须非零退出且 CLI 错误保持脱敏，
但不能把这种合同外持续锁写成“必然零残留”。该既有边界不由本次局部修复扩张，也不得被描述成已经
解决。

## 4. 验收矩阵

自动化必须证明：

- demo 发布后可由 `CatalogApplication(FINAL/catalog, FINAL/artifacts, web)` 直接进入 `READY`；
- Catalog 包含同 Plan 的 `PASS`／故意 `FAIL` 两个 Run，issue 为零；
- 在最终 Artifact root 重新构建控制 Catalog 时，`catalog_id`、Bundle set 与数据库逻辑摘要一致；
- 完整移动 demo 后仍精确得到 `ARTIFACT_ROOT_MISMATCH`；
- 发布前的 staging Catalog 不能以 staging Artifact root 启动；
- 不同父目录、错误布局和已有最终目标被受限 producer 拒绝；
- Windows 下会被 Win32 改写的尾点／尾空格最终目录名必须在发布前拒绝，不能产生表面成功但
  最终绑定失效的 demo；
- 在没有合同外持续文件锁的受控 Catalog 构建或外层发布失败中，最终目录与两类 staging 残留均不
  暴露；持续同用户锁导致操作系统拒绝清理时明确记为既有边界，不得宣称零残留；
- JSON、Markdown、SQLite 与错误输出不含本机、runner、staging 或最终绝对路径明文。
- CLI 遇到未预期 demo 内部异常时以稳定 `DEMO_INTERNAL_ERROR` 非零退出，不输出 traceback 或原始路径。

回归至少包括 `test_demo`、Catalog／API／CLI、atomic publication、Python 3.10／3.13 普通与 `-O`
全量测试，以及 wheel-only、无 checkout 的仓库外真实 `demo -> catalog-serve` 读回。真实服务验收必须
读取 health、Catalog 和至少一个 Bundle 文件，并在结束后确认端口、进程、SQLite sidecar 与 staging
残留为零。

## 5. 发布停止线

本文件只建立维护候选，不宣布发布。只有候选经独立陌生读者复核、受保护 PR 的既有 required checks
通过、仓库外 wheel 真实链闭合，并以新的不可移动标签和 Release 资产完成公开下载及摘要读回后，
才能另行把源码从 `0.12.2.dev0` 固定到发布版本。`v0.12.0`、`v0.12.1` 及其资产始终保持不动。
