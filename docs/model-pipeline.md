# 模型管线与绑定验证

1. python3 scripts/fetch-models.py：官方项目 Pages 下载，Git blob 哈希校验，原子写入，无自动重试。
2. node scripts/inspect-glb.mjs：GLB magic/length/JSON 验证，生成 docs/model-inspection.json。
3. Blender 原生 glTF import：已实测 467 Mesh，0 Armature，见 blender-inspection.json。
4. Three.js GLTFLoader：原始 Z 上轴经 -90° X 转换为 Y，居中缩放；保留独立 Mesh 与源身份。
5. 静态场景点击/悬停/隐藏/风格切换；样式共用 geometry，不复制模型资源。

## 当前动画证据与差距
原型通过肘节点带动前臂与哑铃，保持上臂固定；暂停仍可 raycast 点击。不同时间有不同关节角，4 秒周期可拖动。这是可运行关节动画，不是蒙皮、更不是肌肉缩短。
真实 anatomy.glb 没有 skins 或 animations；Blender 成功导入不证明可正确绑定。

## 下一次 P2 实验
比较两条路线：A 手工上臂/前臂两骨绑定 + 每块肌肉独立权重；B 保留解剖静态参考 + 独立动作 rig，并映射相同 ID。A 更贴近目标但肌腱连接/关节形变复杂；B 可解释动作但不能满足动态解剖。优先制作 A 的单臂局部验证，未验证前不替换当前原型。

验收：导出 GLB 至少一个 skin、独立二头/三头/前臂对象和 curl animation；AnimationMixer 播放0/50/100%截图；暂停点击 ID；肌腱附着处不明显脱离；不同视角检查。不以整体旋转或自动权重无错误作为成功证据。

## 网络与工具证据
curl raw GitHub 连接 reset；urllib Pages 全文件可用并匹配公开 API blob。下载管线已有可复现验证方式；系统 curl/raw 网络问题延期排查，未修改代理。Blender MCP 服务固定工作区在另一个工程，因此脚本读取本工程绝对输入并生成本工程 JSON；其 saveTo 输出在服务工作区，交付路径需显式复制。后续用本工程独立 bpy CLI 脚本避免服务工作区耦合。
