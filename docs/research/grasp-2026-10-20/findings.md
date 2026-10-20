# 抓握为何尚未解决：来源核实与只读诊断（2026-10-20）

本轮只读GLB、复现构建脚本分区规则并核实专业资料，没有新生成动作，没有修改正式手部、POSITION、权重或冻结报告。不能用研究结论替代实际修复。

## 新实测
资产SHA256：40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff。
遍历实际GLB全部JOINTS_0/WEIGHTS_0的非零槽（>1e-7）：36个网格受附加指骨影响；30根指骨中只有16根出现有效权重。双侧Little MCP/PIP/DIP全部0；双侧Index DIP、Middle DIP、Ring PIP/DIP也为0。这是导出资产实测，不是根据骨名猜测。计数是影响槽，不能理解成独立顶点或临床指标。

构建规则的DIGITS=[Thumb,Index,Middle,Ring,Little]同时用于空间排布和分区，而di=4又重写为Thumb；实际上Little分区永远不可达。按同一横向坐标复现：Ring骨起点u=.03675m、Little起点u=.055m都被分为Thumb。Thumb还有特殊起点；不是简单改一个数组就能得到标定正确的手。

其他已证实问题：现有权重以空间分箱切割组织，而非沿肌腱/骨间肌真实附着；源467是选出的肌肉/肌腱集合，没有完整五指指腹接触表面。已有历史翻面/拉伸与接触FAIL保留。缺少皮肤不等于BodyParts3D整体没有手骨，更不意味着必须重新造皮肤壳。

复现：
```
node scripts/grasp-v1/research_weight_audit.mjs
python3 scripts/grasp-v1/research_mapping_audit.py
```
输出在artifacts/grasp-research；摘要audit.json。

## 核实来源及适用边界
访问日期均为2026-10-20。仅保存链接与自主总结，未下载受限模型或复制视频/论文插图。

- Khronos官方 glTF skinning教程：https://github.com/KhronosGroup/glTF-Tutorials/blob/main/gltfTutorial/gltfTutorial_020_Skins.md 。工程规范：关节矩阵/逆绑定/权重决定顶点运动，存在骨骼不等于相关表面受驱动。不是解剖依据。
- Blender5.2 Armature官方文档：https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/armature.html 。PreserveVolume改变变形插值，可缓解局部体积塌陷，但不能创造缺失表面或纠正组织指派。glTF默认矩阵线性混合，不能直接假设Blender开关在Three中等效。
- Blender glTF官方：https://docs.blender.org/manual/en/5.0/addons/import_export/scene_gltf2.html 。可导出骨骼/形态键动画；版本差异需本机5.2导出复测。
- GRAB官方项目：https://grab.is.tue.mpg.de/ 及 https://github.com/otaheri/GRAB 。人体+手+物体轨迹和接触可提供姿态/接触参考，不是当前源肌肉权重；需按身材、坐标与物体重定向。许可需逐项核对，不在本轮下载。
- ContactPose作者项目：https://contactpose.cc.gatech.edu/ 。真实手-物体接触数据；不能把生活物件抓握直接称为标准高位下拉。
- ContactOpt作者代码：https://github.com/facebookresearch/ContactOpt 。可借鉴接触目标驱动姿态优化；作者明确其方法允许一定网格互穿近似软组织，不能原封照搬作为本项目无穿模门禁，不能默默放宽当前阈值。使用MANO，不能直接替换源解剖资产。
- MANO官方：https://mano.is.tue.mpg.de/ 及 https://mano.is.tue.mpg.de/license.html 。扫描学习的手部外表面，不是解剖肌肉模型；模型下载需注册同意条款，公开许可标题是非商业科研。本轮未注册、下载或集成。
- BodyParts3D原作者建模笔记：https://lifesciencedb.jp/bp3d/info_en/userGuide/releaseNotes/modelingNote-2.0.pdf 。说明包含手骨（指骨/掌骨/腕骨），可研究同源骨性地标；资料版本旧，不能冒称与当前467选集或已下载4.0骨档完全同版本/已对齐。资产须验证映射、尺度、左右和版本许可。

## 三条路线比较
A（优先）：修复明确的指派程序错误，并用同源手骨/可靠手部地标标定现有30根骨骼，按实际组织连接建立权重。保留467原网格和基础几何。先局部一只手、一根手指验证；缺失的指腹不能冒称被修好。
B（第二步）：在A具备可信几何之后，定义圆柱握持参考，腕/掌面/拇指对握与四指关节约束联立求解；固定手到杆的局部变换，让全身动作跟随约束。不能只追腕部位置或以DIP关节原点当指尖。接触和关节连续性通过后再迁移整周期。
C（不采用直接替换）：MANO/现成外皮手虽便于视觉抓握，但不符合原始解剖外观要求，有许可与身份冲突；ContactOpt也不是插上就能修当前肌肉模型。只作参考，不加皮肤壳。

推荐A→B；单独换求解器、加骨骼或切DQS均不解决当前根因。

## 最小实验与门禁
1. 固定当前57骨失败资产；先增加“每根骨骼受影响顶点/组织列表”和每个目标指段是否有真实几何的资格表。零权重不一概判坏：缺几何应INCONCLUSIVE，但不能宣称手指闭合。
2. 以同源骨性地标校准一侧空间顺序/关节中心、局部轴和拇指基部对握。修正确认的命名/分区错误；不把现有分位坐标当医学起止。
3. 只对一条组织/指段做小范围、可归因附着权重对照，保持原POSITION，记录原/新权重及顶点/面ID。参考不足就停，不盲扫参数。
4. 先做独立固定杆open→half→closed，再测真正双手弯曲杆；真实组织三角面与杆的碰撞、翻面、边长/面积比、掌面方向、各指接触保持。修接触时不能把杆整体埋入掌心。
5. Blender与Three实测一致后，跑整周期121帧及原双动作全三角门禁和独立专业复核。骨骼控制、组织形变、可见解剖抓握分项判定。仍缺指段表面时报告能力边界；如确需增加同源真实手骨/肌腱作为可见结构，应另行明确资产范围和许可，不能用蒙皮伪造。

本轮结论：此前完成的是控制器与度量设施，不是完成了可用的手部附着模型。已确认更具体的程序缺陷，下一步具备针对性验证依据；本轮没有声称抓握已修复。
