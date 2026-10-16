# 生物力学平台可行性与边界

2026-10-15 已在 Windows 原生隔离环境运行 OpenSim 4.6 和 MuJoCo 3.16.0。独立示例不读取 Muscle Atlas 生产动作资产。

## 安装与验证

OpenSim 官方最新 core release 查询为 [4.6](https://github.com/opensim-org/opensim-core/releases/tag/4.6)，官方 [opensim-org 包索引](https://api.anaconda.org/package/opensim-org/opensim) 提供 win-64 `opensim-4.6-py311np24.conda`。本机用 Python 3.11.17 / NumPy 2.4.6，完整传递依赖锁于 `opensim-win-64.explicit.txt`。API 必须通过该 Conda 环境运行，避免 Anaconda 3.9、CPython 3.13 或另一 venv 的 DLL/NumPy ABI 混用。[官方 Conda 指南](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53116061/Conda%2BPackage) 说明包与 GUI 发行版独立；旧文档示例版本不能代替本次包索引检查。

`opensim_smoke.py` 加载包自带 `arm26.osim`（SHA256 `5247bde715582aa2ad462e5ee2a099ef30b53d21bccc58d4527073313cdecb29`），初始化 2 坐标/6 肌肉，平衡肌肉，realizeDynamics，计算有限质心并产生 BodyKinematics 数据。官方旧模型被内存升级、重复 pathwrap 重命名、显示 .vtp 缺失均在原始日志记录。headless 分析成功；未安装单独 GUI，不声称显示几何完整、临床标定或人体预测有效。

Python API 的 native 对象生命周期必须显式管理：本轮原型的独立 BodyKinematics 在函数退出时曾导致间歇性原生失败；通过 `model.addAnalysis()` 交由 Model 持有后，三次同路径重复验证通过。不得用忽略非零退出、强制 `os._exit()` 或不释放模型来掩盖问题。测试使用 `thisown` 验证所有权已转移。

MuJoCo 按 [官方 Python API](https://mujoco.readthedocs.io/en/stable/python.html) 安装 `mujoco`，使用隔离 venv，不使用历史 `mujoco-py`。自建米制双关节刚体模型：有限差分 Jacobian 最大误差约 `2.66e-7`；逆动力学所求力矩再用于正动力学得到目标加速度（绝对容差 1e-9），1000 步得到 1 秒。这里的 1e-9 是同一数值模型的回算容差，不是人体预测精度。无需 GPU/CUDA，也未验证 GPU 仿真。

## 可声称的层次

|层次|输入和输出|现阶段边界|
|---|---|---|
|骨架运动学|关节姿态/参考标记 -> 位置、速度、角度|动画能提供姿态，需解剖轴/比例校准；图形四元数不是现成解剖角|
|力矩/逆动力学|惯性、运动、外部载荷、接触 -> 净关节力矩|MuJoCo 合成模型回算通过；真实人和器械参数未知|
|肌肉力估计|力臂、肌肉路径/参数、净力矩、优化约束 -> 模型肌力|OpenSim 可研究；净力矩不足以唯一确定多肌肉共同收缩|
|肌肉激活估计|控制/肌腱-肌纤维动力学、校准和目标 -> 预测激活|不是图形 morph 权重，也不是 UI 颜色|
|EMG 实测|电极、采样、滤波、归一化和时序校准 -> 电信号特征|没有受试者 EMG 输入；预测激活不等于 EMG，也不能从 EMG 直接读出精确肌力|

所有预测应携带模型版本、输入来源、参数、单位、假设、误差与验证数据集；UI 必须分别标记“示意”“模型预测”“实测”。本轮没有产生真人激活、肌力或训练刺激百分比。

## 参考体系和下一步

首个参考 profile 位于 `docs/quality/references/lat-pulldown.json`，记录两篇已核验原始研究的题名、链接、读取层级、适用范围和不能支持的结论。[握宽研究](https://pubmed.ncbi.nlm.nih.gov/24662157/) 用于动作变式/EMG语境；[负荷下肩胛运动研究](https://pubmed.ncbi.nlm.nih.gov/33493783/) 用于提醒任务和负荷相关性，并非本项目下拉轨迹的数值真值。当前只读到摘要，没有把全文、视频权限或原始数据获取伪造成已完成。

优先补充经授权且有相机/坐标标定的前、侧、后参考录像和可复核地标，再定义肩/肘/腕角度。任何后续数据必须标注来源许可、受试人群、负荷、握法、采样率、置信度及同步方法。先以工程不变量发现缺失关节/NaN/跳变，再与适用数据比较；不能用单一固定肩胛比例作为通用真值。已有 M1 的 B01/B02/V01 等结论原样保留，修复仍等待用户批准。
