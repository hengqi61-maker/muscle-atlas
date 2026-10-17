# W3 · 真实肩部实验与 Mac R1 独立数值对接

状态：W0安装/模型载入、W1能力评估、W2数据链路及W3指定姿态实验已实际执行。**跨模型运动学医学结论 INCONCLUSIVE**，不批准 M2/R1 动作质量或正式资产替换。

## 可重复命令

本机已有隔离 OpenSim4.6/CPython3.11环境，不重装系统工具。新工具依赖锁在 `research/opensim/requirements.lock.txt`；基础设施/完整Windows锁见 Draft PR#4。运行根目录为独立 worktree `D:\codex\muscle-atlas-opensim`。

```powershell
$py='D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe'
& $py scripts/biomechanics/fetch_model.py
& C:\ProgramData\Anaconda3\Scripts\conda.exe run -p D:\codex\.muscle-atlas-opensim python scripts/biomechanics/opensim_experiment.py artifacts/opensim-models/ThoracoscapularShoulderModel.osim --source-commit 52094cc61c3e795552c658e34a73d083f4662c6b --out research/opensim/results
& $py scripts/biomechanics/compare_packets.py research/opensim/mac-r1/PulldownProbe.packet.json research/opensim/results/shoulder.packet.json research/opensim/r1-shoulder-mapping.json --out research/opensim/results/mac-r1-comparison.json
& $py -m pytest tests/biomechanics -q
& $py -m ruff check scripts/biomechanics tests/biomechanics
```

实际实验代码提交 `9c363d965d1437cbde94d3c9fc05a29e559bce64`；结果单独提交，`source.producerCommit` 指向先发布的代码版本，不用结果提交自引用。OpenSim版本、模型SHA、脚本SHA、坐标值、范围和锁定状态均在输出中。两次独立进程的33肌肉×10姿态路径长度最大差 **0 m**（同一软件/参数的可复现性，不是人体精度）。

## 实验的四类数值

1. **模型提供**：7骨体/7joint/17坐标/33肌肉/78路径点、默认值、约束和允许区间。模型区间不是经本项目验证的人群生理范围。
2. **人工指定**：GH elevation目标0/15/30/45/60°；另一组scapula_upward_rot目标0/3/6/9/12°；其余坐标从模型默认值开始。不是实际下拉、面拉或测量受试者。
3. **脚本/求解器输出**：assemble后坐标、骨体局部/世界矩阵、实际肌肉路径长度。AC闭环约束会调整第二组坐标，例如命令0°后实际约1.89°，因此command与actual分列，绝不悄悄强称已达到输入角度。
4. **未支持的假设**：协调节律、负荷、人体惯性标定、真实软组织/肌力/激活/EMG均未解算或验证。sample秒时标只是姿态序号0..9，跨实验跳转不代表连续真实运动速度。

抬臂组例如 Infraspinatus_S 路径由0.1514323m至0.1413636m，Subscapularis_S由0.1110159m至0.1170754m；第二组肩胛改变时部分肩袖路径几乎不变、背阔路径变化。这里只报告模型几何响应，不从长度变化推断肌肉激活、训练刺激或正确动作。

初次脚本在realizePosition后设置time导致SimTK缓存降到Instance，再读肌肉长度报错；已保留 `artifacts/shoulder-first-failure.log`，修正为先设时间再assemble/realize，原命令两进程通过，未忽略错误或降级环境。

## Mac→Windows 实际交换

读取 Mac Draft PR#5 的 `ccf51104e309303ea3853df41a4697928a541147` handoff。原始37,579,810字节文件SHA256为 `cf27f3ff63c5dd73fef0d5ae29657bf296879cd02531f4494ac0d5f173bf117c`，实际导入前已核验；原R1GLB `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`。

`import_mac_v2.py` 独立验证两条Clip各121帧×27关节：有限值、det+1、局部/世界/实际父矩阵、xyzw四元数与矩阵等价、时间单调、名称/层级一致。每Clip提交0/25/50/75/100%五个真实采样帧的小包；不复制37MB原观测、28MB附着注册表或41MBGLB，不在Windows改Mac资产。嵌套Blender row-major/Z-up参考保留原文件，不误读为glTF矩阵。`research/opensim/mac-r1/import-report.json` 记录全121帧检查。

`compare_packets.py` 读取上述真实 Mac 数据及真实 OpenSim packet。映射只覆盖Thorax和右锁骨/肩胛/肱骨；左侧、前臂双骨、腕与指明确未覆盖。基准偏移数值往返残差最大约 `2.22e-16`，这由代数对齐而来，不能成为解剖正确证明。20行报告给出关节与时间、相对胸廓运动及待核实问题，整体 **INCONCLUSIVE**、`mayApproveMotion=false`。

两边姿态不是相同测量任务，故没有伪造逐帧“OpenSim标准误差”、通用肩胛比例或医学阈值。下一步必须确定解剖轴、肩关节中心、人体比例、匹配任务和独立参考后才可作适用比较。真实肌肉表面拉伸/碰撞仍由Mac的几何检查承担。

## GitHub 双机交接与未完成联合验收

Windows Draft PR#6 已在 Mac PR#5 以及原PR#3留言，公开版本化规范、fixtures与精确提交；已收到并实际解析Mac原始成果。发布到GitHub不等于确认Mac已读取/采用；后续以其PR提交/评论的实际回应为准。没有跨机器远程控制，也未向不可访问的Mac聊天伪造消息。

保留M2两轮失败和owner gate；不开展第三轮维修、面拉、MuJoCo/MyoSuite/SOFA完整集成或渲染重构。W2矩阵互通通过不意味着统一人体R1通过产品/生物力学验收。
