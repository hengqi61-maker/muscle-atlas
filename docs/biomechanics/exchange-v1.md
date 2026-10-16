# W2 · Muscle Atlas 运动学交换规范 1.0.0

共同冻结基线 `0914d4fad3fbe107ea90c08473b6d2a448345ba6`。Windows 分支 `codex/opensim-biomechanics`，Mac 分支 `codex/unified-rig-v2`。Mac 的 `c46d42ecda6b5a2f54da9da4b200baf70d7cc55e` 原始观测已实际读取；本规范回应其 `Windows-exchange-request.md`。历史 M2 FAIL / 两轮上限保持不变，不是第三轮修复。

## 文件与字段

`schemas/kinematics/packet-v1.schema.json` 是 JSON Schema 2020-12；`scripts/biomechanics/kinematics.py` 另做数值/层级语义检查，JSON Schema 单独通过不足以证明有效。根字段：

- `source`：模型/原始观测 URI、原文件 SHA256、来源 Git SHA、生成者 SHA、软件版本、许可状态；GLB 观测另外保留资产 SHA256。
- `coordinates`：规范包一律米/秒、右手系；轴含义必须显式注明。未标定轴不得标为解剖屈曲轴。
- `referencePose`：default-node / inverse-bind-derived / animation-time0 / model-default / operator-specified 分开；`anatomicallyCalibrated` 明示。
- `nodes`：稳定 id、parentId、侧别、局部/世界刚体矩阵、解剖轴是否已知。这里是导出框架标识，不替换 anatomyId。
- `samples`：秒时标、阶段标签、逐节点局部/世界矩阵、数据来源类别。允许空数组表达“只有参考姿态”，不伪造动作轨迹。
- `attachments`：肌肉、路径点、所属物理框架、局部米制位置及证据；路径控制点不是源网格已校准起止附着，也不是力/激活。
- `coverage` / `evidence`：左右覆盖、是否镜像、独立验证状态，模型提供/脚本推算/人工测试/生理假设、数值置信度及不确定性。镜像数据不能标成独立验证。

## 数学约定

所有矩阵为 4×4 齐次刚体、平铺 16 数 **column-major**，齐次**列向量**，主动右手旋转；`p_world = T_world_from_local * p_local`，`T_world_child = T_world_parent * T_parent_child`。矩阵左上 3×3 必须正交且 determinant +1；反射和隐含缩放被拒绝。GLB 中若有 scale（例如生产展示 1.45）应在独立的几何/单位步骤说明，不能混入刚体旋转。

不交换未声明顺序的 Euler，也不直接把 OpenSim 坐标当成骨骼旋转分量。Blender 若使用 wxyz 四元数，先明确转换成其数学等价的矩阵再序列化；Three/glTF 的 xyzw 不得直接喂给 wxyz。Blender 侧可以由 `Matrix` 按列导出，必须通过下面的非交换 90°测试。

映射公式：`T_target = A * U_s(T_source) * B`。`U_s` 只将平移乘以正的单位比例 s，旋转不变；A 是已声明的世界坐标/原点对齐，B 是每个目标局部框架相对于来源局部框架的参考偏移。单位相同则 s=1。逆映射为 `U_(1/s)(A^-1 * T_target * B^-1)`。

给定真实参考姿态 S0/T0，可计算 `B = U_s(S0)^-1 * A^-1 * T0`。这个方程确保数值零姿态对齐，**并不证明** A/B 的解剖意义或比例正确。不同肢段长度和肩关节中心必须另行标定；不能把关节中心平移校准藏在一个通用 Euler offset 中。

## 已执行的真实 Mac 数据适配

```powershell
D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe scripts/biomechanics/import_mac.py PATH_TO_MAC_OBSERVATIONS --producer-commit c46d42ecda6b5a2f54da9da4b200baf70d7cc55e --out research/opensim/mac-pulldown-default.packet.json
# 加 --pose inverse-bind-derived 单独提取 bind-derived frame
D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe -m pytest tests/biomechanics -q
```

已提交 `mac-pulldown-default.packet.json` 与 `mac-pulldown-bind.packet.json`，来自 Mac 发布的真实 GLB 观测，16 个关节、双侧原有骨架，未把默认/绑定帧合并，也未臆造 animation time0。两份均包含 Mac 观测文件和原 GLB 的哈希。源侧只有静态 atlas 时适配器明确失败，不捏造骨架；未来多个 skin 要先明确选择策略。

## Mac 最早可接入的内容

请在自己的分支按此 schema 导出统一骨架参考包和至少 0/25/50/75/100% 真实肩部姿态包，记录其精确源码/资产哈希；分别给出 default、bind 和 clip-time0 的实际含义。原始文件仍留在 Mac 分支，Windows 只读并产出报告。将 A/B、节点对应表、长度/关节中心标定和未知项单独提交后才能进行专业对照。

目前 W2 证明坐标/存储/单位/手性和真实 legacy 导入链路，不能批准肌肉表面、握持、肩胛协调或动作迁移。新 R1 资产的联合验收要以 Mac 实际发布的数据和新报告为准。
