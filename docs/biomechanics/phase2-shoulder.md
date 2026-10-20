# Phase 2：肩胛—肱骨与肘部独立参考

2026-10-18。结论 **INCONCLUSIVE**：本次是实际 OpenSim 4.6 原生进程的模型运动学分析，不能认证高位下拉、人体解剖或Mac蒙皮质量。未修改任何GLB、Blender权重或原始.osim。

## 来源与观测

模型为 OpenSim core 4.6 `52094cc61c3e795552c658e34a73d083f4662c6b` 的 `OpenSim/Tests/shared/ThoracoscapularShoulderModel.osim`；SHA256 `892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe`。模型许可、credits与适用性沿用 `model-assessment.md`，本轮不重新分发模型。

`research/phase2/shoulder/model-sweeps.json` 保留模型提供的所有Joint XML：局部PhysicalOffsetFrame、SpatialTransform轴、坐标与函数均保持原定义。这些轴不是Mac骨骼名称的同义词。胸廓/肩胛/肱骨参考用世界刚体矩阵显式计算 `inverse(T_world_parent) @ T_world_child`，结果列主序、m/rad、主动右手变换。报告角差是相对首个实验姿态的SO(3)主旋转角，不能冒充临床Euler角或肩肱节律。

实际运行14个人工指定姿态：GH抬臂0/15/30/45/60°；肩胛上旋0/3/6/9/12°；肘屈曲0/30/60/90°。每个姿态保留命令值、assemble后17坐标实际值、肩胛相对胸廓/肱骨相对肩胛/尺骨相对肱骨矩阵和AC点约束残差。AC最大残差 `7.016522229951154e-17 m` 只证明该模型约束数值满足。

肩部两组实验保留默认锁肘；肘部组明确在内存模型initSystem前解除默认锁定，实际肘坐标为0、0.5235987756、1.0471975512、1.5707963268 rad。它不是默认模型能力的隐式声称。首轮仅调用state.setLocked(false)随后assemble把角度恢复默认，原结果及日志保存在 `state-only-unlock-*`；最终程序的回归测试要求实际角度达到设定，避免悄悄发布没有运动的肘部实验。源模型字节未更改。

模型提供：肩胛胸廓关节、GH旋转轴/参考、AC闭环、肘单坐标、尺桡独立骨体和默认锁定。脚本计算：相对矩阵、姿态角变化和闭环残差。人工假设：各组设定姿态。未知：人群生理阈值、Mac解剖轴/关节中心标定、真实运动/负荷、肌力/激活/EMG。17坐标不是17个独立DOF；先前局部约束rank资料不扩展为所有姿态的全局证明。

## Mac可复核证据与限制

只读核对 Mac `1b06bf4d94169868acdca5f3a430bc964f2cafa0` 的 windows-interface、trajectory-format、receipt和v1全部7包。七包各27节点，现有exchange-v1 schema与语义检查通过。Mac raw trajectory为121帧/30fps、Blender Z-up、-Y-front、+X-subject-left；这是原始观察格式，不等于OpenSim角度，也不直接冒充exchange-v1。五关键帧packet不能证明完整周期连续性。

`peer-byte-provenance.json` 逐包记录Git原始bytes SHA256、长度、CRLF数及单独LF/CRLF渲染hash，未改写输入。重新确认Windows旧结果published LF SHA为 `242fa6bd38b754e74de1acc32bbcd9fb9949080e9eaeb57d2115ffe6b153c9c5`，原Windows CRLF导出SHA为 `62e1f48249d78ad4811a2a8b83e420e0e38d3e21c11e9c01b89e73106124c0a8`。二者是不同传输字节身份，数字内容一致，不应只发布一个无标签SHA。

沿用exchange-v1：`T_target=A*U_s(T_source)*B`，单位转换只缩放平移，A/B必须按明确参考姿态标定。Mac串联肩带结构与OpenSim胸廓->锁骨及胸廓->肩胛、AC闭环不同；Mac单Forearm与OpenSimulna/radius不同；模型右侧单臂、手焊接，无指骨/左侧独立数据。不能据参考角不同判Mac动作错误，不能把路径点当467源网格已标定附着。

给Mac的下一批数据要求：提供完整121帧原始矩阵、canonical层级与参考姿态、解剖关节中心/轴的证据类别、单位/左右侧/坐标变换、SHA与producer commit。先处理模型适用性与解剖参考差异，再定义高位下拉潜在异常阈值。目前异常筛查仍INCONCLUSIVE，不使用未经依据的肩胛固定比例。

## 重复运行与测试

在独立worktree根目录执行：

```powershell
$py='D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe'
& C:\ProgramData\Anaconda3\Scripts\conda.exe run -p D:\codex\.muscle-atlas-opensim python scripts/biomechanics/phase2_shoulder.py research/phase2/shoulder/model-sweeps.json --model D:\codex\muscle-atlas-opensim\artifacts\opensim-models\ThoracoscapularShoulderModel.osim
& $py scripts/biomechanics/phase2_shoulder.py research/phase2/shoulder/peer-byte-provenance.json --peer-commit 1b06bf4d94169868acdca5f3a430bc964f2cafa0
& $py -m pytest tests/biomechanics/test_phase2_shoulder.py -q
& $py -m ruff check scripts/biomechanics/phase2_shoulder.py tests/biomechanics/test_phase2_shoulder.py
```

真实原生运行日志 `native-run.log`；3项数值回归通过，ruff通过。回归检查使用真实原生运行结果，另有独立合成刚体矩阵真值测试；不是把合成数据称为OpenSim系统测试。没有创建后台服务或残留仿真进程；输出限定于本分支研究目录。缺失.vtp可视化资源警告保留，headless数值不据此宣称完整显示。
