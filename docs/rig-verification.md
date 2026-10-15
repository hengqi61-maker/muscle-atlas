# MODEL-RIG 单臂闭环 · 2026-10-15

## 实际交付
原始 anatomy.glb 的467个解剖 Mesh 全部保留，原始文件不变。派生 anatomy-curl.glb 添加左臂 UpperArm / Forearm 两骨、44个解剖蒙皮 Mesh、3个蒙皮哑铃部件。GLB只有1个 skin（由47个SkinnedMesh共享），不是47个独立骨架。静态探索仍使用原资产；动作模式已移除椭球人体。

长头和短头肱二头肌分别添加 BicepsBulge；混合权重表面添加45/90/120°姿态修正形态键。骨骼和所有形态键按30fps烘焙为一个4秒Clip，最终运行时使用Three.js AnimationMixer，独立 biceps 控制不会覆盖肘部修正。未使用不可导出的Blender Drivers。

来源、BP/FMA和独立mesh ID保留；从源坐标转成米制Z-up，经Blender导出Y-up。估算肩、肘、腕中心见curl-build.json，尚非医学标定。上臂骨保持固定，仅前臂骨屈伸。44网格中有未混合的上臂组织，它们正确保留原位。

## 方案和发现
比较单纯rigid-parent（无连续形变，不选）、Rigify自动权重（工作量大且不证明附着正确）、局部手工双骨（本次选择）。线性混合权重在肘窝有挤压；原生双四元数蒙皮不属于当前glTF通用导出路线，运行时私有shader增加兼容风险，因此采用可导出的姿态修正形态键。修正减少了测试肌肉的95分位拉伸，但不能宣称清除了局部压缩。

初次导出从frame1开始，运行时量测发现1/30秒偏移。修正为frame0..120，最终clip精确4秒。初次47项非根skinned-node警告通过移除不必要armature父级、保留modifier和bind数据解决；最后Validator0错误0警告。没有跳过失败断言。

## 可复现验收证据
- scripts/build-curl-rig.py：Blender干净后台运行，生成GLB和artifacts/curl-rig.blend。
- docs/evidence/curl-validator.json：Khronos glTF Validator **0 errors / 0 warnings**；信息提示不等于错误。
- docs/evidence/curl-runtime.json：Three.js实际加载；两骨、有效JOINTS/WEIGHTS且每顶点权重和1；动画骨角度实测约0/45.003/90.000/120.000°；上臂/肘中心不漂移；0°返回复原。
- 同报告：实际 brachioradialis929个顶点混合受两骨影响；独立BicepsBulge能在固定骨姿态下改变顶点。
- Playwright真Chrome：WebGL显示、动画画面变化、暂停、拖动、四角度、形态键单独控制、选择和记录持久化。不是仅结构校验。
- docs/evidence/curl-0.png / curl-45.png / curl-90.png / curl-120.png / curl-fullbody.png：目标网页截图；无骨骼变形假图。

## 通过与未通过的边界
通过：真实解剖来源、骨骼/权重/动画/形态键传输链路、目标渲染器播放与交互、源拓扑不拆断、静止无额外偏移。

未完整通过：大屈曲的软组织质量。在brachioradialis的12000条三角边观测（含共享边重复）中，90°有105条、120°有57条压缩到原长度20%以下；最小比例约6%。这不等于网格拓扑断裂，但明确表明局部压缩/折叠风险。没有全肌群碰撞/关节包覆验收，手掌保持源姿态而不是闭合握持；未加入真正皮肤层。形态键24%径向修正是手工视觉参数，不是生理规律、实测激活或力学仿真。

因此**最小工程链路通过，MODEL-RIG质量债务仍DEFERRED**。下一步局部重新绘制权重和肌腱附着校准、逐网格检查内肘接触、握持姿态；必要时保留原始来源的同时对局部拓扑重建。须在四角度前/侧/后视及压缩指标下复测，不能以Validator通过代替视觉质量。
