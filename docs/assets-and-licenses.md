# 资产来源与许可（2026-10-15）

## 本次导入
[BodyExplorer](https://github.com/JohanBellander/BodyExplorer) 提供可直接加载的 GLB。未复制其源码；源码 README 声明 MIT，但代码许可不能覆盖资产。

anatomy.glb 25,133,568 bytes；Git blob SHA1 a112885444785a9dd93c5753b46ac790e6e036b3；SHA256 见 model-inspection.json。mesh_mapping.json blob 6e702859c44aa0a36eb3b44d988076c48675c493。固定资产 blob，而不是浮动 main 版本；抓取脚本遇到哈希变化会停止。467 网格中 401 bp3d + 66 z-anatomy；包含肌肉、肌腱、结缔组织，不是 467 块肌肉。

[上游署名与许可](https://github.com/JohanBellander/BodyExplorer#attribution)：BodyParts3D, © The Database Center for Life Science, CC Attribution-Share Alike 2.1 Japan；Z-Anatomy by Gauthier Kervyn, CC BY-SA 4.0。原文件保持不变；运行时改变材质、坐标。后续分发改编网格需要保留来源、变化说明与适用 ShareAlike 条款。

## 需保留的许可差异
[BodyParts3D 当前官方许可页](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html) 标记 2025-02-27 更新为 CC BY 4.0；BodyExplorer 仍列旧版 CC BY-SA 2.1 Japan。本次按下载衍生资产的上游声明保留旧版署名，不擅自将混合 GLB 改标为统一 CC BY 4.0。若以后直接导入新版 BP3D，必须对具体下载版本重新核对。

[Z-Anatomy 仓库](https://github.com/Z-Anatomy/Models-of-human-anatomy) 是 Blender atlas template，主内容声明 CC BY-SA 4.0，但 README 另列部分器官第三方条款（含 NC）。本次仅使用 BodyExplorer 的肌肉子集；完整 atlas 后续必须逐资产审核，不能用全项目声明覆盖器官例外。

## 三条技术路线
|来源|已核实格式/拆分|当前证据|绑定判断|
|---|---|---|---|
|BodyExplorer|GLB 独立命名网格 + 映射|本地 Three.js 显示与 Blender 导入；467 meshes|0 skins / 0 animations，无现成 rig|
|Z-Anatomy|Blender atlas 模板、ZIP|官方 README 与许可已查看；完整包未导入|可在 Blender 处理，但绑定质量未验证|
|BodyParts3D|官方 OBJ 包 + ID 数据|官方下载与许可页已查看；未下载完整 OBJ 包|静态网格需自行绑定，不能保证自动权重可用|

[BodyParts3D 下载页](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html)。目标路线选择已验证的 BodyExplorer GLB 先浏览；保留逐网格 provenance。不存在已验证的医学级动态模型。

## 原创原型
简化几何和关节周期为本项目生成，无第三方人体资产。不是完整人体解剖替代品。
