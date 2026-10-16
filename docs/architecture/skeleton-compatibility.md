# 骨架、动作与参考数据兼容性

接口设计版本 1，仅供独立诊断。生产运行时、GLB 和生成器保持原样。基线为 `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`，质量基础设施为 `9c9c971`。

## 实际骨架

静态 `anatomy.glb` 无骨架。curl 为 `UpperArm -> Forearm` 两骨；pulldown 共 16 骨：

```text
SpineRoot
  Thorax
    LeftScapula -> UpperArm -> Forearm -> LeftHand
    RightScapula -> RightUpperArm -> RightForearm -> RightHand
  LeftThigh -> LeftShin -> LeftFoot
  RightThigh -> RightShin -> RightFoot
```

不将无前缀的 `UpperArm` 误配为右臂。不把源网格名称、骨骼名和 anatomyId 当作同一种 ID。467 个来源网格保留独立身份；BP/FMA 可能多网格共享，不能直接作为骨架关节映射键。

Blender 以米制 Z-up 编制派生骨架、四元数插值并烘焙 frame 0..120（30 Hz，4 秒）；导出 GLB 为 Y-up。glTF 使用右手系、米和秒、四元数 xyzw，节点 TRS 为父局部变换；世界旋转必须先组合父变换。原静态人体在 Scene 另有 -π/2 X 转换；不能再对已导出的动作 GLB重复转换。pulldown 场景外层是 `scene = 1.45 * model + (0,-1.45,0)`；器械配置与模型测量在共同的 model frame，报告必须写明所处 frame。

curl 形态键是艺术/姿态修正，pulldown 为烘焙双臂 IK、肩带、躯干与腿部。生产 `AnimationMixer` 采样第一条动画，器械由共享 4 秒时间轴计算。局部骨旋转不等于解剖屈曲、旋前或肩胛角度；没有经校准的解剖轴、个体关节范围、质量惯性或肌腱力学参数。现有 120° curl 示意上限不是人群生理关节限制。

## 格式转换

|路径|可行性|必须验证/会丢失|
|---|---|---|
|GLB ↔ glTF|同一规范的容器转换可行|外部 buffer/纹理 URI、二进制对齐、扩展、skin inverse bind matrices、morph 与 animation 全部校验|
|GLB -> BVH|可导出层级、offset 和采样姿态的研究副本|BVH 不承载肌肉网格、皮肤权重、morph、材料、稳定源 ID；Euler 顺序和轴向必须声明，不能声称无损|
|BVH -> 当前 GLB|需逐关节映射和参考姿态 retarget|根运动、单位、身高比例、rest pose、Euler 顺序、左右手性、缺失肩胛/手骨、脚部接触；重建派生副本后与原轨迹比较|
|GLB -> OpenSim/MuJoCo|运动学参考可行，不能直接得到肌骨模型|需解剖坐标、约束、惯性、关节自由度、负荷/接触及肌肉路径；图形 skin 不是生物力学肌肉|

本轮不执行 retarget 或替换骨架。Blender 的 BVH 导入/导出作为后续受控副本实验，不把没有参考标定的转换称为已验证。

## 独立工具和测试数据接口

`scripts/infra/validate-assets.mjs` 组合 Khronos Validator 与真实 GLTFLoader，检查层级合法性、必需关节、有限变换/顶点/轨迹、四元数、时间单调、蒙皮索引与权重。报告记录资产 SHA256、骨层级、动作时长、SkinnedMesh 数量；SkinnedMesh 数不能当成 glTF skin 数。原始静态 GLB 法线错误会返回失败；动作 GLB 通过不豁免源文件问题。

`motion_contract.py samples.json profile.json` 使用以下中间结构；它是对既有 `transforms.json` 的独立包装，不改旧格式。样本由既有 measure adapter 获得，只加元数据、不变换数值：

```json
{"schemaVersion":1,"candidateCommit":"40hex","assetSha256":"64hex","coordinateFrame":"glb-model-y-up-metres","samples":[{"time_s":0,"joints":{"Forearm":{"position_m":[0,0,0],"quaternion_xyzw":[0,0,0,1]}}}]}
```

实际要求至少 21 个单调采样点，示例只展示单条。关节异常范围通过 profile 的 `angleLimits` 声明 `name, range_deg, angleDefinition, referenceId, applicability`，样本必须提供对应的 `angles_deg`。缺失参考、未定义解剖轴或缺失角度一律不能通过范围验证。当前 pulldown profile 的范围为空，明确标记待标定，绝不由 quaternion 分量臆造医学范围。有限数据/工程约束通过不等于质量里程碑批准。

规范依据：[Khronos glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)、[Blender BVH 文档](https://docs.blender.org/manual/en/5.4/files/import_export/bvh.html)（格式说明，不是本机 Blender 版本证明）。
