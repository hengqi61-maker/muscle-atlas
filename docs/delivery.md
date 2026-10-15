# 首次交付 · 2026-10-15

## 已完成的阶段性目标
项目在当前 Git 根目录可直接启动。真实静态人体 GLB、独立点击/悬停/隐藏/淡化、两种共网格风格、三栏控制台、轨道相机、明确标记的哑铃弯举关节原型、播放器、肌群角色关联、实际训练单组实录、IndexedDB 保存与 JSON 导出。

真实解剖包含467网格（肌肉、肌腱和结缔组织）；英文源名称与 FMA/BP/source 身份保留。原型中文肌群索引只有7类，不代表完整中文解剖数据库。多条 mesh 共享概念编号，通过源网格名称后缀确保467独立身份。

## 真正执行的检查
- npm run build：TypeScript + Vite production通过；存在1.39MB主包警告，未隐藏。
- npm test：6项通过；关节周期、末端/循环、状态优先级、风格独立、实际组数、独立ID完整性。
- npx playwright test：1条端到端流程通过，真实 Chrome；GLB200、画布点击源结构、相机旋转/缩放/复位、风格切换、实际动画画面变化、暂停时间保持、详情选择、完成记录、刷新保留；pageerror为空。
- npm audit：0 vulnerabilities。
- node scripts/inspect-glb.mjs：467 meshes / 0 skins / 0 animations，完整GLB长度与SHA256。
- Blender5.2干净后台启动：本地 GLB 原生导入467Mesh / 0Armature；保存 artifacts/anatomy-import.blend，输出 docs/blender-inspection.json。
- 截图人工查看：docs/anatomy-browser.png、docs/prototype-browser.png。

## 占位与尚未实现
真实模型尚无动画骨骼/蒙皮；当前弯举是程序式肘关节层级运动，不是肌肉收缩。Real Anatomy 当前红色肌肉/浅色肌腱与灯光，不含真实纤维纹理。深层/骨骼/侧别/自动聚焦、计划编辑、训练热力图、历史趋势、备份恢复、Google Calendar均未实现。UI明确标注。

## 引入的替代方案
静态真实解剖 + 简化关节原型；网络改走官方 Pages、urllib并校验固定blob。未改变系统代理、未用 OAuth、未付费。网络替代没有被宣称为系统根因修复。

## 永久修复
升级脆弱测试依赖并审计清零；加载状态由正常DOM拥有，保留StrictMode与原失败断言；Blender路径通过独立根目录脚本修复，不依赖其他工程的MCP工作目录。

## 延期债务
MODEL-DOWNLOAD：curl/raw传输连接重置原因未清；已验证本地资产不依赖该路径。
MODEL-RIG：真实肌肉绑定与形变尚未验证，下阶段单臂两骨GLB试验。
无 ACCEPTED_RISK 项，无 OPEN 项。完整记录见 .codex/workaround-debt.md。

## 剩余风险/下一步证据
大型模型和JS包需性能基准、分块/压缩。许可证存在官方新版BP3D与上游衍生旧声明差异，保留双方来源；再分发改编资产前逐来源核对。训练数据目前只导出，恢复需实现并验证。首版浏览器origin存储不同于未来Tauri数据库，迁移必须测试。
