# Windows environment audit

Audit date: 2026-10-15 Asia/Shanghai. Before installation.
Repository: https://github.com/hengqi61-maker/muscle-atlas
Baseline commit: 7a0d258b59e9a2acc32021e8ab66f7098ff025ea. Branch: infra/windows-biomechanics.

## Verified host
- Windows 11 Home Chinese, 10.0.22631 build 22631; RAM 16,309,932,032 bytes.
- AMD Ryzen 7 7840H, 8 cores / 16 threads.
- NVIDIA RTX 4060 Laptop GPU: nvidia-smi reports 8188 MiB dedicated VRAM, driver 581.86, WDDM. Win32_VideoController AdapterRAM overflows near 4 GiB and is unsuitable for this measurement.
- AMD Radeon 780M integrated GPU; reported AdapterRAM is not total shared memory.
- Driver CUDA compatibility ceiling 13.0; nvcc not on PATH. CUDA Toolkit and CUDA compute execution NOT verified. Do not install a driver or toolkit for CPU simulation.
- WSL2 Ubuntu 24.04.4 LTS, kernel 6.18.40.1; GPU visible through /usr/lib/wsl/lib/nvidia-smi.

## Existing tools
Windows: Git 2.55.0.windows.2; Git LFS 3.7.1; Node 24.14.0; npm 11.11.1. Python on PATH is Anaconda 3.9.13, launcher also knows CPython 3.13. Python 3.11, uv, CMake, Ninja, FFmpeg and Blender not found on PATH. Chrome exists in Program Files.
WSL: Python 3.12.3, Node 24.14.0, Git 2.43.0, CMake 3.28.3, Ninja 1.11.1, FFmpeg 6.1.1; Blender/nvcc not on PATH.

## Project audit
React 19 / TypeScript / Vite 7; Three 0.180 / React Three Fiber 9 / Drei 10. Zustand and Dexie. npm package-lock.json exists; no packageManager or engines field. README requires Node22+. Preserve lock; npm ci only.
GLB source anatomy is static; derived curl/pulldown GLBs contain skins and baked animations. Blender generators use local quaternions, metre units, Z-up authoring to Y-up glTF export. Runtime uses AnimationMixer/SkeletonUtils and pose corrective morphs. No universal medically calibrated skeleton or joint-limit metadata.
Existing checks: Vitest, Python unittest, Khronos validator with actual Three runtime, Playwright Chrome. No checked-in GitHub Actions workflow at audit. Read README, AGENTS, architecture, model-pipeline, rig-verification, pulldown-motion-review and generator/validator scripts. Historical architecture statements are superseded by dated updates.

## Risks and installation decision
Use dedicated local environments, not Anaconda base. Native OpenSim requires matching Python/NumPy ABI and DLL loading. Prefer official isolated conda package and do not assume Python 3.11 support. MuJoCo uses official mujoco package, CPU dynamics requires no CUDA. Existing WSL tools avoid duplicate system installs; portable Windows tools may be added only as needed. Blender installation size warrants portable/LTS selection. No driver/proxy/firewall changes; no sudo/admin execution. GUI/GPU results must remain separate from headless CI. Models, environments, installers and generated local evidence stay untracked unless intentionally selected small text evidence.

## Quality-branch audit (after owner supplied branch)
Fast-forwarded the independent work branch to `9c9c97125c1ea902478894f164669764677d3563`, retaining main at `7a0d258`. Unlike main, this branch already has `.github/workflows/core-quality.yml`, motion freeze/measure/capture adapters, 12 quality gate tests, and preserved M0/M1 review reports. Its production src/public/generator tree exactly matches main (git diff exit 0). Read all docs/quality and the frozen M1 summary. M1 remains FAIL / WAIT_OWNER_SCOPE; no M2 fixes or new motion review were performed.

## Post-install state
Native independent Python 3.11.17, uv0.13.1, pytest9.1.1, ruff0.17.0, MuJoCo3.16.0, CMake4.4.4, Ninja1.13.2, packaged FFmpeg7.1, portable Blender4.5.0 LTS, OpenSim4.6 Python3.11/NumPy2.4.6 are installed and exercised. Windows Node24.14.0/npm11.11.1 and Git/LFS reused. No admin, driver, global proxy, firewall or system Python changes. CUDA Toolkit not installed; no CUDA execution claim. Actual Chrome WebGL selected AMD Radeon780M, so local browser numbers are NOT RTX4060 benchmarks.

Raw source anatomy GLB has validator errors (non-unit normals) and degenerate-triangle information. Derived curl/pulldown assets validate with zero errors/warnings. This preexisting raw asset problem stays visible and is not repaired or silently allowed by the strict prototype.
