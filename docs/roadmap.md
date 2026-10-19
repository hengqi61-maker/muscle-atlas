# 路线图 · 2026-10-15 首次工程交付

## P0 已验证，绑定目标待继续
- [x] 工作区检查，建立 React/TypeScript/Vite 项目。
- [x] 研究指定三种来源；核对代码和模型许可差异。
- [x] 固定哈希导入真实 GLB + mapping，检查 467 网格 / 0 skins / 0 animations。
- [x] Blender 5.2 原生导入成功，467 Mesh / 0 Armature；可复现脚本及 .blend。
- [ ] 真实肌肉蒙皮绑定验证。下一步单臂两骨、肌腱连接与独立 Mesh 动画导出。

## P1 核心浏览可用
- [x] 三栏桌面布局 + 底部控制台。
- [x] 真实静态解剖人体，旋转/缩放/平移、悬停、点击、单对象高亮、其他淡化、隐藏/恢复。
- [x] 固定资产版本的独立 mesh anatomy ID；保留 FMA/BP/source。
- [x] 真实结构英文搜索 + 简化中文肌群索引。
- [x] 相同网格 Real Anatomy / Clean Tech 材质风格。
- [ ] 左右侧、表层/深层、骨骼、自动聚焦、纤维纹理、完整中文名称。

## P2 关节原型可用，真实动态解剖未完成
- [x] 哑铃弯举：肘节点驱动前臂与哑铃、上臂固定。
- [x] 播放/暂停/循环/速度/进度拖动/视角复位；暂停仍可选肌群。
- [x] 原型二头肌主要角色、前臂协同、三角肌稳定角色；选肌群可打开关联动作。
- [ ] 真实肌肉 skin / shape keys、GLB 动画、AnimationMixer、动作库扩展。

## P3 基础实录，规划分析未完成
- [x] IndexedDB schema v1，plans/sessions 分表；动作、重量、次数、RIR、日期实录。
- [x] 用户创建实际完成组；当日组数；刷新持久化；JSON 导出。
- [ ] 模板/日期计划编辑；热力图与时间范围；趋势；备份导入恢复。

## P4 / P5 待开发
- [ ] 独立 Google OAuth，只读训练日程，明确关联规则。
- [ ] 受控写入、智能规划、性能基准、模型压缩/LOD、Tauri。

## 验证范围
构建、Vitest 核心逻辑、Playwright 真 Chrome（WebGL 模型导入、画布点击、轨道操作、模式/风格切换、动画画面变化与暂停、实录/刷新）、Blender import。详见 delivery.md。

首次交付满足“静态真实解剖 + 明确标记关节原型”的可运行范围；整个长期项目没有完成。真实模型动态形变是下一阶段最大技术风险。

## 2026-10-15 · 第二次交付更新
- [x] 真实来源左臂双骨绑定，44独立解剖蒙皮mesh，GLB动画与BicepsBulge及肘部姿态修正targets。
- [x] AnimationMixer播放、四角度检查、独立形态键、变形后点击与近景；生产界面删除椭球人体。
- [x] Khronos Validator0错误0警告；Three运行时骨角度/权重/形态键证据；真Chrome2条流程。
- [x] 下载器SHA256缓存、有限恢复、安全续传、原子替换；8项Python测试；默认curl与系统代理路由差异定位。
- [ ] MODEL-RIG未整体关闭：大屈曲肘窝局部压缩、组织接触及手掌握持姿态待校准；不宣称医学级动态解剖。
- [ ] MODEL-DOWNLOAD残余：原始未指定代理curl直连仍失败；项目导入器使用系统代理且缓存离线可验，不改全局网络设置。

## 2026-10-15 · 器械与握持更新
- [x] 选择性接入高位下拉器械；重新校准握宽/杆高和footrest。
- [x] 真实源人体坐姿、双臂固定骨长IK、手腕杆轴对齐，导出4秒GLB；运行时和器械同时间轴。
- [x] 闭合握持表面、拇指/四指、腕部连接及可切换呈现层；保留静态原始解剖。
- [x] 六角胶头、倒角、滚花金属柄的原创哑铃精建，独立GLB可检查。
- [ ] 外部CC0候选下载403，未接入，保留资产获取债务；不冒称真实下载模型。
- [ ] 肩带、肘窝、腿垫接触及更细手部质感仍待精修。共享锚点通过不等于全身无穿模。

## 用户指定的手部回退
已移除原创闭合手部/皮肤/指甲及源手指折叠，动作模式恢复原始解剖手部；保留新版六角哑铃、握点约束和坐姿下拉。原始张手姿态不被宣称为闭合抓握。


## 2026-10-15 · M2 参考与质量测试（进行中）
- [x] 参考包：官方 ACE/Mayo 文字、研究摘要、肩胛综述和解剖学来源，逐项区分已核实、推导与未标定假设。外部视频未实测。
- [x] 固定旧版7a0d258的真实录像、多视角截图及首轮报告已公开为独立证据预发布：<https://github.com/hengqi61-maker/muscle-atlas/releases/tag/evidence-baseline-7a0d258>。不是产品验收。
- [x] 独立121时刻真实网格检查已在旧版复现肩袖冻结、足部穿透；当前原型仍存在肩袖塌缩。
- [ ] 八块肩袖局部姿态修正正在制作，须重新生成GLB、源身份验证、实际网格检查和四位独立复审。
- [ ] 真实手部抓握、精确解剖附着、完整M2验收仍未通过。
- [ ] 不进行统一骨架重构、专项FPS工程或面拉制作，不自动合并main。


## 2026-10-16 · M2两轮复核结束，未通过验收
已完成参考包、旧版缺陷复现、八肩袖/双掌长肌修正、全源实体支撑检测、五项Chrome回归与两轮独立复核。最终候选32315eb，完整报告见docs/reviews/lat-pulldown/32315ebc59b3be17c3e8c200ba1922e7f6312ee3/M2-summary.md。真实原始拇指/横杆P1仍阻止验收；解剖附着标定、组织归因、真实接触和受控性能对照未关闭。两轮自动返工上限已到，等待Owner新范围；main未合并，面拉未开始。


## 2026-10-16 · V2 R0/R1 独立原型与双机交换
Owner已授权统一骨架研究；旧M2两轮失败结论及正式资产保留。独立分支codex/unified-rig-v2建立27骨骼、467源网格共享蒙皮与两段诊断动画，未替换正式动作。源基础几何独立核验467/467一致；实际Chrome7/7通过。R1下拉仍有肩袖面积塌缩和异常拉伸，不能产品放行。
Mac已采用Windows PR6固定c12e30e的v1合同，真实导出7份27骨骼packet，坐标/参考姿态映射与Blender写入、保存、重开回读完成。Windows22测试和Mac3交换测试通过；最大实际原生/glTF矩阵元素误差6.9983e-7。该数字不代表解剖标定或OpenSim模型等价。数据、SHA256及生成命令位于docs/rig-v2/handoff/，后续由Windows独立研究对照。无main合并、无面拉制作、无正式逐指动画。


## 2026-10-17 · E3流水线与P1网格级归因
独立PR8基于PR5，原source/R1/手部/正式资产不变。两次分阶段重建＋两次统一入口全冷启动完成，同GLB字节与121矩阵差0，每次50native＋50Three关键帧和完整视频。24新增测试、原build/13Vitest/26quality通过。权威全三角检查仍FAIL：新Curl39/121，冻结R1完整覆盖Curl39/Pulldown91；旧抽样42保留。四独立专业审查阻止正式放行。WD0020–23耐久修复；待Owner选择附着/骨轴与局部权重敏感性，或可复用姿态修正。Windowscontact规范待发布，未造假适配。完整报告docs/rig-v2/pipeline/PHASE-1-report.md。

## Issue #13 · project-local Blender Skills pilot

Pinned upstream `71d031d` core/pipeline/QA in isolated project scope. Actual same-fixture A/B repeated twice: byte-identical GLB, additive QA detects intentional detached cube; no anatomy/production repair claim. Existing build, 13 unit, 26 quality, 4 rig-reuse, 2 pin/protected tests and one Chrome smoke run. See `docs/blender-skills/README.md`; independent review and Owner acceptance pending.
