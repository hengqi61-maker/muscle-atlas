# 原始手部的逐指绑定可行性：R1 文档范围

本页只提出未来接口与证据要求。当前冻结 R1 GLB、467 个源网格、27 骨层级和绑定均不修改；用户已允许隔离、非破坏性手部骨架实验；本轮尚未执行逐指弯曲实验，没有功能性抓握结论。正式运动资产中的逐指弯曲仍需另行批准。当前两个 `LeftFingerSocket` / `RightFingerSocket` 是非变形的通用接口，各自只有一个节点，不能称为已有十指关节。

## 已有源覆盖与真实缺口

依据本地固定 `public/models/mesh_mapping.json`，以下明确标记 hand/pollicis 的 32 个源条目均为 bp3d。此清单包含部分拇指前臂肌，不能把32条等同于32块手内在肌，也不涵盖所有经过手部的前臂肌腱。本项目实际锁定的源 GLB SHA256：

`6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f`

| 原始名称 | BP ID | FMA ID |
| --- | --- | --- |
| abductor digiti minimi of left hand | BP8737 | FMA37397 |
| abductor digiti minimi of right hand | BP7569 | FMA37396 |
| flexor digiti minimi brevis of left hand | BP8516 | FMA37399 |
| flexor digiti minimi brevis of right hand | BP4858 | FMA37398 |
| left abductor pollicis brevis | BP8706 | FMA37387 |
| left abductor pollicis longus | BP9144 | FMA38517 |
| left extensor pollicis brevis | BP9253 | FMA38520 |
| left extensor pollicis longus | BP8191 | FMA38523 |
| left flexor pollicis brevis | BP7575 | FMA37389 |
| left flexor pollicis longus | BP9106 | FMA38484 |
| left opponens pollicis | BP8596 | FMA37391 |
| oblique head of left adductor pollicis | BP8248 | FMA46122 |
| oblique head of right adductor pollicis | BP5560 | FMA46121 |
| opponens digiti minimi of left hand | BP8204 | FMA37401 |
| opponens digiti minimi of right hand | BP4860 | FMA37400 |
| right abductor pollicis brevis | BP4855 | FMA37386 |
| right abductor pollicis longus | BP4820 | FMA38516 |
| right extensor pollicis brevis | BP4818 | FMA38519 |
| right extensor pollicis longus | BP4816 | FMA38522 |
| right flexor pollicis brevis | BP8958 | FMA37388 |
| right flexor pollicis longus | BP4844 | FMA38482 |
| right opponens pollicis | BP4853 | FMA37390 |
| set of dorsal interossei of left hand | BP8036 | FMA42405 |
| set of dorsal interossei of right hand | BP6629 | FMA42404 |
| set of lumbricals of left hand | BP8053 | FMA42399 |
| set of lumbricals of right hand | BP6633 | FMA42398 |
| set of palmar interossei of left hand | BP8246 | FMA42403 |
| set of palmar interossei of right hand | BP6631 | FMA42402 |
| superficial head of left flexor pollicis brevis | BP8722 | FMA65199 |
| superficial head of right flexor pollicis brevis | BP5556 | FMA65198 |
| transverse head of left adductor pollicis | BP8885 | FMA46124 |
| transverse head of right adductor pollicis | BP5543 | FMA46123 |

例如 lumbricals、palmar/dorsal interossei 以 `set of …` 合并条目存在，不能从名称推断已逐指分段；分支、肌腹、肌腱端点和相邻指归属仍需逐网格/连通分量标注。此肌肉子集不提供可直接使用的逐指骨骼、关节局部坐标或皮肤接触外壳。不能拿 mesh 质心或整块包围盒当 CMC/MCP/PIP/DIP 的解剖中心。

源标签与空间侧别也不能混淆：`left flexor pollicis brevis` BP7575 在现有空间绑定中使用 RightHand/RightForearm；`right flexor pollicis brevis` BP8958 使用 LeftHand/LeftForearm。R1 保留原始名字和ID，只按源空间进行绑定，并未把标签修成另一侧。未来须带源侧别、实际空间侧别、确认人和证据，避免重复交换。

当前绑定仍是几何代理。BP8885/BP5543 的 transverse adductor 分配 Hand/Forearm；lumbrical 集合 BP8053/BP6633 与 palmar interossei BP8246/BP6631 当前主要/完全随 Hand，未建立逐指运动。`config/rig-v2/attachment-registry.json` 可查实际每顶点权重，confidence 为 `unvalidated-geometric-proxy`，不是已确认附着。

## 既有 P1 不是保留源网格可以解决的结论

M2 冻结审查 `32315ebc59b3be17c3e8c200ba1922e7f6312ee3` 的 [biomechanics](../reviews/lat-pulldown/32315ebc59b3be17c3e8c200ba1922e7f6312ee3/biomechanics.md) 和 [visual](../reviews/lat-pulldown/32315ebc59b3be17c3e8c200ba1922e7f6312ee3/visual.md) 记录 BP8885/BP5543 的原始 transverse adductor 三角面116 深入握柄：采样距轴约0.356mm，握柄半径24mm，深入约23.645mm，多个时刻持续。这是旧 M2 握杆场景的实际失败；不能转称 R1 无器械探针中的新测量。两个代理握点对齐不证明原始三角面有正确接触。

必须区分四层：源基底坐标/拓扑不变；蒙皮权重和骨层级新增；实际姿态形变；功能性接触/抓握。前一层通过不能替代后一层。保留源基底允许说明“未编辑原始网格”，却不代表正式运动资产的逐指弯曲获准。本轮没有手指弯曲、手壳、源组织折叠或有效握持证明。

## 未来非变形逐指接口草案（未实现、未定稿）

使用既有 Left/RightFingerSocket 作为命名空间锚点，未来子节点均 `deform=false`，先只承载参考坐标、关节候选及测量。不得把此草案写回冻结的 canonical-rig.json，或擅自升级为 Windows/OpenSim 交换标准。

| 后缀，前缀 Left/Right | 建议父节点 | 用途与待补证据 |
| --- | --- | --- |
| PalmFrame | FingerSocket | 掌侧/背侧、近远端、桡尺侧参考框；须由已标注源地标确定 |
| ThumbMetacarpalFrame | PalmFrame | 拇指掌骨参考，不是已知真实关节 |
| ThumbCMC | ThumbMetacarpalFrame | 拇指基部候选；轴、中心及耦合待验证 |
| ThumbMCP | ThumbCMC | 近节参考接口；无默认角度/限位 |
| ThumbIP | ThumbMCP | 远节参考接口；无默认角度/限位 |
| Index/Middle/Ring/LittleMetacarpalFrame | PalmFrame | 每指掌骨参考，不将掌面当刚性生理整体 |
| Index/Middle/Ring/LittleMCP | 对应 MetacarpalFrame | 每指近端接口，待标注局部基与中心 |
| Index/Middle/Ring/LittlePIP | 对应 MCP | 每指中间接口 |
| Index/Middle/Ring/LittleDIP | 对应 PIP | 每指远端接口 |

这是控制/观察接口的树，不是宣称真实骨段首尾应按此坐标放置。每节点未来记录 `status=proposed`、源ID/候选地标顶点、空间侧别、单位、坐标转换、parent-local matrix、world matrix、xyzw quaternion、DOF/轴定义、参考版本、证据、置信度和审批状态。当前不得填写猜测的关节坐标、标准角度范围或逐指解剖权重。现有 Hand 仍为唯一已实现的手级变形控制；骨与控制器须明确区分。

## 若获准探索，需要补齐什么

1. **标注与覆盖。** 对真实源网格分支及连通分量标注掌部、每指、近远端和肌腱走行；保留原 mesh ID/顶点/三角面映射。需要独立骨/关节参考才能定位手内关节，不能仅靠肌肉表面手绘估计后称医学地标。覆盖不足时明确缺失项，不生成替代皮肤或补造肌肉。
2. **权重与约束。** 先建立候选 per-digit bone groups，按实际组织附着和跨关节路径分配归一化非负权重，分别处理集合网格中的多指分支；验证最大影响数与 glTF 导出误差。需要受证据支持的局部轴、可用DOF、限位及拇指对掌/指间耦合约束；任何数值都需来源，不能默认采用通用人体模板。跨关节薄肌腱需要可移植修正/路径模型，并与皮肤蒙皮近似区别记录。
3. **接触任务。** 在获准的独立 `.blend` 实验中先验证原始张手、分指小范围姿态，再验证特定直径/姿态握柄。分别测实际组织三角面与有限实体的相交/间隙、掌/拇指方向、各指运动连续性和原始组织薄片塌缩；不能用虚拟掌点替代。裸露内部组织不是皮肤，未提供皮肤表面时不能声称“表面承压/握力”正确。
4. **回归和边界。** 独立重导入源模型证明源基底/索引不变；逐姿态比较 Blender 与 GLB 真正输出；检验面积/边长/有限数/自交、双侧及手腕跨界。保留同一统一层级及源身份，不给每个动作另造手骨，不通过隐藏组织消除问题。

## 参考与许可的取得要求

首选可核验的一手关节/运动学文献或可复现测量，包含手部局部坐标、关节中心/轴定义、姿态条件、受试者/标本和适用限制。对指定握法需正侧背及掌侧/拇指可见的连续参考，记拍摄视角、器械直径和动作范围；二维视频不能直接当三维标定。OpenSim 手模型若被选用，须先对其具体版本、坐标与关节约定、几何/数据来源和独立许可做核验，不直接映射 Euler 角或把它当本源模型已标定结果。

现有模型许可沿用 [资产来源与许可](../assets-and-licenses.md) 的固定下载衍生资产记录：BP3D 与 Z-Anatomy 的来源/版本/条款分别保留；软件许可不覆盖解剖资产。本页不重新解释或改标许可。未来引入图谱图像、骨模型、运动数据或教程视频前，需要记录精确版本、作者、URL、下载字节/hash、授权条件、可否改编/再分发和必要署名；参考动作不代表获得复制媒体或几何的许可。若许可或授权范围不明确，保留引用信息，不能打包进产物。付费资产、OAuth 或新素材获取按项目授权约束执行。

## 当前交付状态

已完成：实际源ID覆盖核对、既有P1归因、未来非变形接口草案、绑定/约束/参考/许可的证据要求。

新增绕行：无。永久债务修复：本页未修改生产或修复手部P1。延期/风险：逐指关节坐标与绑定未验证；原始张手不能证明功能性抓握；本轮未实施逐指实验；用户已允许在隔离文件中制作非破坏性手部骨架原型，正式运动资产的逐指弯曲仍需另行批准。后续可在已授权隔离范围内继续实验，再由独立审查检查真实输出。本页不阻塞现有实际数据交接，也不把这些缺口描述成完成。
