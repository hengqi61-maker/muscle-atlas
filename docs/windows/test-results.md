# Windows 实际验证记录 · 2026-10-15

仓库 `D:\codex\muscle-atlas`；独立分支基于质量基础设施 `9c9c97125c1ea902478894f164669764677d3563`。main 为 `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`，运行源码/模型在这两个提交之间相同。本轮不改变生产实现、资产、旧测试和历史 M0/M1 报告。

## 本机已执行

|检查|实际结果|
|---|---|
|npm ci|152 packages；未修改 package-lock；安装审计 0 vulnerabilities|
|npm run build|exit 0；主 JS 1,396.18 kB（gzip 387.25 kB），保留 >500 kB 警告|
|Vitest|9 / 9 PASS|
|原 Python unittest|8 / 8 PASS|
|原质量门禁 Node tests|12 / 12 PASS；M1 仍等待 owner，不因软件绿灯放行|
|原 curl / pulldown runtime|均 exit 0，Khronos 0 errors / 0 warnings|
|真实 Chrome Playwright|3 / 3 PASS；页面资源、选择、拖动、暂停、风格、持久化和动作切换回归|
|新增 Python contract / MuJoCo 测试|10 / 10 PASS；覆盖坏数据与合成动力学回算|
|新增 GLB 原型负例/兼容性|4 / 4 PASS；缺失关节、非法四元数、循环层级均拒绝，CUBICSPLINE 零切线正确保留|
|ruff|最终 exit 0；早期 import 排序与显式 check 参数失败已修复并复验|
|motion contract 真实 adapter 输出|121 个采样点通过，模型 frame / 候选与资产哈希齐全；不作解剖质量判断|
|原 trajectory-check|121 点，无 failures；固定骨长变化最大约 1.01e-7 m，端点位置差 0|
|OpenSim|4.6，官方 arm26：2 坐标 / 6 肌肉、equilibrateMuscles、realizeDynamics、BodyKinematics 1 行输出|
|MuJoCo|3.16.0，2 DOF；Jacobian 最大误差 2.66e-7，逆/正动力学回算通过，1000 步 = 1 秒|
|CMake / Ninja|4.4.4 / 1.13.2；compiler-free 项目 configure 和 Ninja custom target 执行成功；不声称 C++ 编译器已安装|
|FFmpeg|7.1，生成 16×16 黑帧流并处理到 null 成功|
|Blender|官方 4.5.0 LTS ZIP SHA256 与官方清单一致；factory-startup 后台 Python 检查成功|
|安装脚本|在 `.muscle-atlas-repro` 新建第二套独立环境，重复执行复用固定依赖；无管理员/全局配置改动|
|WSL|Ubuntu 24.04.4 / WSL2、现有开发工具和宿主 GPU 可见性核验；未安装额外 apt 包|

## 失败、警告和未验证内容

- 原始 `anatomy.glb` 全量 Khronos 检查：**887 errors / 0 warnings / 42 infos**，无截断；错误为 `ACCESSOR_VECTOR3_NON_UNIT`，信息含退化三角形。严格原型检查返回非零，未修改来源 GLB，也没有将它列为 PASS。CI 对派生动作资源设严格门禁，原始资产问题单独保留；未来修复需保留来源文件及新派生资产 provenance。
- OpenSim 旧模型内存升级、重复 pathwrap 名称及缺少显示 `.vtp` 的警告保留于 `artifacts/windows/opensim.log` 和 runner 日志。无显示计算通过不代表 GUI 几何完整。
- 性能浏览器 console 报 1 条 `favicon.ico` 404；定位到 `http://127.0.0.1:5187/favicon.ico`。没有 pageerror。未为消除该警告改产品页面。
- 初次新增 runner 汇总 exit 1，唯一失败为新脚本 import 排序；已修复并保留初始日志。后一次完整运行暴露 OpenSim 示例原生退出码 `4294967295`：重复三次出现两次失败，阶段日志显示分析已完成、函数释放原生对象时退出。此前 `BodyKinematics` 独立拥有、引用 Model；改用 `model.addAnalysis(analysis)` 正确转交所有权（实测 `thisown` 从 True 变 False），相同 runner 连续三次成功。未重装、降级或忽略退出码；最终整套复验另存，保留原始失败以便重现。
- Git 直连端点失败；官方 API 归档补齐哈希一致的 Git blob 后 fast-forward 成功。随后使用 Windows 已配置的系统代理作为**单次 Git 命令**参数验证远端，无全局 proxy 配置变更。
- CUDA Toolkit / CUDA kernel 未运行，C++ toolchain 未验证；无 OpenSim GUI、真实 EMG、人体肌力或个体激活结果。Windows 核显成绩不能代表 RTX4060、Mac 或 GitHub Actions GPU。

## 浏览器观察原型

生产 build、Chrome 155.0.8059.40，1440×1000 页面；Canvas drawing buffer 865×832，pixel ratio 约 1。ANGLE D3D11 实际设备：**AMD Radeon 780M**。每场景预热 1.5 秒、采样 5 秒、重复 3 次；共享 context，非严格冷启动。下面是最终轮组三次中位 rAF/s 与各次 p95 范围，不能称为医学验收或正式性能 SLA。

|场景|中位 rAF/s|p95 帧间隔范围 ms|Draw Calls / Triangles（典型）|
|---|---:|---:|---|
|atlas 暂停|82.63|12.5–12.5|468 / 1,092,419|
|curl 播放|82.41|12.3–12.3|396 / 956,587|
|pulldown 暂停|14.38|72.9–84.9|507 / 1,093,414|
|pulldown 播放|13.75|84.8–97.0|507 / 1,093,414|

下拉暂停仍慢、主线程 TaskDuration 高是值得 trace 的候选信号，不足以排除 GPU/驱动/调度影响。GPU elapsed 未采到，明确为 null；rendererMemory 是对象数，不能报告成显存字节。完整报告含 JS heap、主线程任务时间、每资源加载时间/字节、相机、GPU 和资产哈希，路径 `artifacts/windows/performance-final.json`。安装、录屏和正式基准应避免同时运行。

## 证据与后续

原始日志在本地 `artifacts/windows/`；大截图/模型/录像/安装包和环境不提交。小型可提交摘要在 `docs/windows/validation-summary.json`。完整 runner 最终结果位于 `artifacts/windows/final-confirmed/results.json`，初始 lint 失败保留于 `checks/results.json`，原生生命周期失败在 `final-all` / `opensim-repro-*`，修复后重复测试在 `opensim-fixed-*`，局部复验在 `final-recheck` / `final-health`。

新增 GitHub Actions 分开执行 Linux CPU/结构检查与 Windows headless OpenSim；真实桌面/GPU benchmark 不加入 GPU 不存在的 runner。远端 CI 是否实际通过应以 PR checks 为准，未运行的 job 不算本机已验证。

优先事项：取得可授权共享的原始参考/标定数据；在现有 owner gate 下确定 M2 范围；追踪肩/腕解剖轴与接触验证；为原始法线问题建立可追溯派生修复；之后做受控 CPU/GPU 对照和 trace。当前不统一骨架、不新增动作、不开展大型优化。
