# Windows / WSL2 独立研发平台

先读 [环境审计](environment-audit.md) 和 [实际结果](test-results.md)。分支 `infra/windows-biomechanics` 基于 `codex/motion-quality-infrastructure` 的 `9c9c971`，不修改动作实现。安装包、虚拟环境及录像均在 Git 之外。不要在 Anaconda base 安装项目依赖。

## 已实际安装的位置

|用途|本机路径|
|---|---|
|uv 0.13.1 引导环境|`D:\codex\.muscle-atlas-tools\Scripts\uv.exe`|
|CPython 3.11.17、MuJoCo、pytest、ruff、CMake、Ninja、FFmpeg|`D:\codex\.muscle-atlas-py311`|
|OpenSim 4.6 / Python 3.11 独立 Conda|`D:\codex\.muscle-atlas-opensim`|
|Blender 4.5.0 LTS 便携版|`D:\codex\.muscle-atlas-portable\blender-4.5.0-windows-x64\blender.exe`|

不修改全局 PATH。新 PowerShell 会话中直接使用这些绝对路径。FFmpeg 可执行路径由 `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` 查询。此包包含 FFmpeg 7.1，不需要单独系统安装。Blender 固定 4.5.0 用于可复现验证，并非声称最新补丁；升级补丁应另行验证生成器兼容性。

## 可重复安装

在仓库根目录，以普通用户运行。前提是已有 Git、Node >=22、npm、Python launcher 中的 3.13；本机均已满足。脚本无需管理员、不改执行策略；若组织策略禁止运行，停止并报告。安装使用磁盘缓存和已存在环境，不删除现有环境。

```powershell
powershell -NoProfile -File scripts/infra/setup-windows.ps1 -ToolsRoot D:\codex\.muscle-atlas-repro
# 按需安装官方 OpenSim 包与便携 Blender，默认不额外下载：
powershell -NoProfile -File scripts/infra/setup-windows.ps1 -ToolsRoot D:\codex\.muscle-atlas-repro -OpenSim -Blender
npm.cmd ci
```

默认脚本创建 bootstrap、py311 两个独立目录，uv 按 `requirements-win.lock.txt` 安装固定依赖，不删除额外包；不要把 ToolsRoot 指向用户共享环境。OpenSim 使用 Windows 专属 `opensim-win-64.explicit.txt`，不更改 Conda 全局 channels。已存在的 OpenSim 环境只做 smoke 验证，不自动升级。不同系统不能使用 win-64 锁。

Git 2.55 / LFS 已存在；未调用全局 `git lfs install`。Node 24.14.0 已满足 README，未替换系统 Node；项目只有 npm 锁，无 pnpm/yarn，不生成其他锁文件。Playwright 使用 `npm ci` 中的固定版本与已安装 Chrome，未下载另一套浏览器。

## 日常检查

```powershell
$python = 'D:\codex\.muscle-atlas-py311\Scripts\python.exe'
& $python scripts/infra/health.py
& $python -m pytest tests/infra -q
& $python -m ruff check scripts/infra tests/infra
& $python -m unittest discover -s tests -p 'test_*.py'
& $python scripts/infra/mujoco_smoke.py
& C:\ProgramData\Anaconda3\Scripts\conda.exe run -p D:\codex\.muscle-atlas-opensim python scripts/infra/opensim_smoke.py
npm.cmd run build
npm.cmd test
npm.cmd run test:quality
node scripts/infra/validate-assets.mjs public/models/anatomy-curl.glb public/models/anatomy-pulldown.glb
npm.cmd run test:e2e
node scripts/infra/benchmark.mjs --headed --seconds 5 --repeats 3
```

推荐一键执行 `& $python scripts/infra/run-checks.py --browser --opensim-prefix D:\codex\.muscle-atlas-opensim`。它将 exit code / 完整日志写入 `artifacts/windows/checks`，运行前暂存已有测试会写入的已跟踪 evidence，运行后将本次生成结果归档并恢复运行前字节。可用 `--only ruff --out artifacts/windows/lint-recheck` 单独复验失败项，避免覆盖初始失败日志。

`test:rig`、`test:pulldown` 会写入已有 docs/evidence，`test:e2e` 会更新历史截图。先确认工作树状态，将本次生成结果归档到 `artifacts/windows`，只恢复本次生成的历史路径，不覆盖用户改动。本次已保留现有审查文件，性能测试不覆盖 M0/M1。

## WSL

Ubuntu 24.04.4 已有 Git / CMake / Ninja / FFmpeg，未执行 sudo 或 apt 安装。Windows venv 不能供 WSL 使用。若以后需要 WSL MuJoCo，可在 Linux 文件系统创建自己的 Python 3.11 环境，安装 `requirements-ci.txt`；GPU 通过宿主驱动映射，不在 WSL 内安装 NVIDIA 显示驱动。本轮仅核验 WSL 命令和 GPU 可见性，未声称 WSL 仿真或 CUDA 内核运算已通过。

## 安装故障

Git 智能 HTTP 曾直连失败，PowerShell 官方 API 源码归档可访问；按内容哈希写入 Git blob 后原始 fast-forward 成功。不得用归档覆盖工作树或改动远端 SHA。OpenSim Conda 元数据首次求解回退完整 repodata 后成功，记录的是实际安装包版本。OpenSim 示例缺少显示几何会警告，headless 分析通过不表示 GUI 几何完整。
