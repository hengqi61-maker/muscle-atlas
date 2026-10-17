# W1 · 上肢/肩带模型实测评估

2026-10-16；共同 Muscle Atlas 基线 `0914d4fad3fbe107ea90c08473b6d2a448345ba6`。不从模型名称推断能力，不将多个模型未经验证地拼接。

|候选|真实获取/4.6兼容性|关节/肌肉/覆盖|许可与局限|
|---|---|---|---|
|Upper Extremity Dynamic Model / MoBL-ARMS|官方实验室链接与 SimTK group657 发布页可访问；4.1 unimanual 包的 download_confirm 返回登录脚本，**未取得包，未运行**|官方目录描述为右上肢动力学模型；本机未核验其具体版本的 DOF、肩带耦合或路径|官方模型目录列 MIT；下载包内许可未读，不能当成已清除。该名称与 MoBL 动力学是同一研究谱系，不假装是两个独立验证源|
|ScapulothoracicJointPlugin（历史）|源码仓库可读；未编译旧插件，也未安装未知 DLL|历史研究用于肩胛胸廓运动；不能把旧3.x插件兼容性套到4.6|仓库 Apache-2.0。当前4.6本身已有 ScapulothoracicJoint，因此不需要为本实验另编插件|
|**官方 core4.6 ThoracoscapularShoulderModel 测试模型（本轮选用）**|从官方仓库4.6不可变提交实际取得 `.osim`，4.6 Python 加载、初始化及两组姿态实验通过|7骨体、7Joint对象、17坐标、33肌肉、78路径点，单侧上肢；实际含锁骨、肩胛、肱骨、尺/桡骨和hand|仓库根 Apache-2.0；模型 credits保留 Ajay Seth、Meilin Dong、Ricardo Matias、Scott Delp，参数来源 van der Helm / Klein-Breteler。本PR不再分发.osim/几何，仅留来源和数值。模型特有引用/再分发条件仍需随未来产品用途复核|
|Kinematic Arm with Articulated Hand（后续候选）|官方目录发现，未下载/运行|目录描述为右侧手部附加20自由度、无肌肉；不当成本项目原手几何绑定真值|目录 License None 不等于可自由再分发；本轮不采用|

## 选用文件的精确来源

OpenSim repository commit：`52094cc61c3e795552c658e34a73d083f4662c6b`（4.6 tag）。文件 `OpenSim/Tests/shared/ThoracoscapularShoulderModel.osim`，SHA256 `892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe`。`fetch_model.py` 固定来源、校验 SHA256，缓存已有不匹配文件即失败，不覆盖来源。

选用的是**官方测试模型的这个版本**，不能等同于所有论文/SimTK发行包。历史文档曾描述无肌肉的肩胛模型，而该实测文件有33肌肉；本轮以读取结果为准。`.vtp` 缺失产生显示警告；headless路径/坐标计算通过，不宣称模型显示完整。

## 实际结构

|Joint|父 -> 子|API 类型|
|---|---|---|
|ground_thorax|ground -> thorax|CustomJoint，6坐标|
|sternoclavicular|thorax -> clavicle|CustomJoint，clav_prot / clav_elev|
|scapulothoracic|thorax -> scapula|ScapulothoracicJoint，abduction/elevation/upward rotation/winging|
|GlenoHumeral|scapula -> humerus|CustomJoint，plane_elv / shoulder_elv / axial_rot|
|elbow|humerus -> ulna|CustomJoint，elbow_flexion|
|radioulnar|ulna -> radius|CustomJoint，pro_sup|
|rc|radius -> hand|WeldJoint，无独立腕/指抓握|

锁骨与肩胛之间另有 `AC` **PointConstraint**，不是树中一个“clavicle父/scapula子”的简单关节。Mac R1 的串联层级与此不同；不能用父子名称相似来确认等价。17是坐标数，默认5个坐标锁定（3平移、肘、旋前/旋后），且存在AC约束；**不是17个无约束独立自由度**。未做约束Jacobian秩分析。

33肌肉中实际读取到肩袖各分束、三角肌、背阔肌、大圆肌、斜方肌、菱形肌、前锯肌等。全部名称、所属路径点框架和默认局部坐标见 `research/opensim/results/shoulder-report.json` / `shoulder.packet.json`。78个点包含via等路径控制点；不能把全部点都叫真实人体表面起止点。只有右侧通路，无左侧独立验证；hand是刚体且焊接，无指骨。

## 文献、许可证与可用范围

- [MoBL实验室资源页](https://mobl.wordpress.ncsu.edu/resources/) 和 [官方模型目录](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090607/Mus)：来源索引与许可提示，不能代替包内复核。
- [Saul等动态模型平台比较](https://pubmed.ncbi.nlm.nih.gov/24995410/)：模型和平台预测的研究背景；本轮未取得其受控动作原始数据。
- [Seth等肩胛胸廓关节研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC4712143/)：内部坐标与肩带建模依据；不提供本项目下拉的通用标准轨迹。
- [肩部肌肉运动/功研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC6856649/)：涉及肩带肌肉、耸肩/抬臂等研究任务；不表示当前Blender模型通过该论文验证。
- [插件源码/许可](https://github.com/opensim-org/ScapulothoracicJointPlugin)、[core许可](https://github.com/opensim-org/opensim-core/blob/4.6/LICENSE.txt)。文章许可与模型/几何许可分别处理。

本轮优先模型适合验证肩带坐标与肌肉路径随指定姿态变化的链路，不支持完整下拉/面拉技术、个体肌力、EMG或手指抓握的独立验收。
