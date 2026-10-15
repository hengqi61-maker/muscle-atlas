# 架构

React + TypeScript + Vite；R3F/Drei + Three.js；Zustand；Dexie IndexedDB schema v1；Vitest + Playwright。

- src/data/catalogue.ts：467 源映射条目，anatomyId = source:(BP ID 或 FMA 或 unmapped):固定源网格名称。17 条源条目共享 ontology/BP 身份，因此不可单用 BP/FMA 作为网格唯一键。名称仅用于网格查找；不把清洗后的对象名当稳定身份。
- src/three/Scene.tsx：一份 Canvas，OrbitControls，缓存 GLB，独立 prototype。坐标原始 Z 上轴转换为 Y；统一居中和比例。
- src/three/materials.ts：状态优先级 hidden > selected > hovered > relation > dimmed > default。基础视觉与交互解耦。热力图颜色解析已定义，数据热力图尚未接通。
- src/three/animation.ts：确定性 4 秒肘屈伸周期，暂停/速度/循环/拖动。当前是场景层级关节运动，无 SkinnedMesh，不是解剖变形。
- src/stores/useAtlas.ts：共享 UI/场景状态。模式不会重复下载 GLB。
- src/data/db.ts：plans / sessions 分表，schemaVersion=1 备份导出。记录只由用户创建。
- src/types/domain.ts：计划字段 calendarEventId/startTime/endTime/syncStatus 已预留。OAuth 尚未接入。

## 已知工程限制
原型左右肌群共享组 ID（不是左右单块 ID）；真实模型保持独立源 ID。真实解剖中文翻译、动作关系需逐项建立。当前材质更新遍历模型，后续基于性能测量优化；467 meshes 约 25MB，可做 LOD 和压缩。首版 JS 包偏大，需分块。资产导入验证 .blend 不属于运行时静态资源。

## 数据安全
浏览器 IndexedDB 绑定 origin。不上传记录。导出 JSON 后自行备份。尚无导入恢复、撤销或删除 UI。日期按本地日历，不将 UTC 截断作为本地日期。未来迁移须兼容导出 schemaVersion 并测试恢复。
