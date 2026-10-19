# The Little Prince: Across the Stars — 技术研究与 Muscle Atlas 落地评估

- **研究日期**：2026-10-17
- **性质**：只读外部技术研究 / 代码审查 / 实验规划；未实现新代码，未修改人体资产，未执行实验
- **研究分支**：research/little-prince-technical-study（从 main 7a0d258b59e9a2acc32021e8ab66f7098ff025ea 分出；仅承载此研究文档）
- **研究对象**：https://littleprince.dev/；开发者 https://x.com/Saccc_c；关联 GitHub https://github.com/Sac-Y
- **Muscle Atlas 代码核查基线**：M2 PR#3 0914d4fad3fbe107ea90c08473b6d2a448345ba6；Mac V2 PR#5 fcb27068232ed1204786fd901bb8c58aa575a686；Windows OpenSim PR#6 9c363d965d1437cbde94d3c9fc05a29e559bce64。三者均非 main 正式发布，R1 未通过产品验收。

> **核心结论**：截至本研究，**官方游戏源码尚未获取**。可以核实开发者公开身份关联和联合发布的制作流程，不能声称检查过该游戏的 Unity 源码或具体动画、渲染算法。最有价值的可借鉴思路是“参考先行 → 单独资产 → 标准骨架 / 通用动画 → IK 道具接触修正 → 多视角独立审查”；这套方法必须在 Muscle Atlas 的真实解剖源网格上独立实现和验证。研究不授权现有骨架重构、正式手指姿态改变、购买工具或合并。

## 0. 证据分级及研究方法

- **A**：直接检查可获得的项目源码/文件/运行记录。用于 Muscle Atlas 当前代码及 GitHub 仓库元数据，不意味着见过小王子游戏源码。
- **B**：创作者、官方产品页面或直接合作方发布的材料；只支持这些材料实际明确提到的内容。
- **C**：第三方复述、转载、对网页构建文件的第三方分析；没有独立复核时不能升级为 A/B。
- **D**：工程判断、可行性假设、尚未实施的实验目标与成本估算，不是测试结果。

方法：检查 littleprince.dev 网站可见首页、Sac-Y GitHub 个人主页和公开仓库列表、Sac 的游戏公开帖子索引、Tripo 官方合作案例、第三方技术复盘。GitHub 连接器不接受用户资料 REST URL，GitHub 网页可核查其公开身份/仓库列表；X 直接页面请求被 HTTP403 拒绝，不能宣称已浏览完整原帖。未克隆未确认的第三方同名仓库；没有执行来源不明脚本，没有下载游戏资产，也没有对生产网站进行逆向突破。

## 1. 作者身份、官方源码状态、许可证 [A/B/C]

1. [A：公开 GitHub 元数据] https://github.com/Sac-Y 的个人简介直接链接 @Saccc_c（https://github.com/Sac-Y?tab=repositories）。这是账号关联的强证据，但**没有证明任何一个 GitHub 仓库就是游戏源码**。
2. [B/C] Sac 的发布帖在公开索引和转载中提到“后续会开源整个游戏及流程”。原始 X 页直接访问返回403。参考：https://x.com/Saccc_c/status/2109962425512734739 与 https://nitter.rdrama.net/demisama_ 。开源预告不是源码发布证明。
3. [A：公开仓库页面检查] Sac-Y 仓库列表可见 MiniMax-H3-Cloud、codex-host、magetic-memory、identity-skill、Physics-atlas、sac-ai.com、go-live、awesome-tg-channel 等，无可确认对应 The Little Prince: Across the Stars 的仓库；列表数量随 GitHub 页面缓存变化。检索“Sac-Y / littleprince.dev / Across the Stars”也没有查到经开发者背书的官方源码 URL。**官方源码尚未获取**，因此无可记录的官方源码提交 SHA、README、Release 或代码许可证。
4. [B] https://littleprince.dev/ 当前网页首页可公开访问，提示桌面 Chrome/Edge 游玩，未找到明确源码链接；网页构建发布本身不等于源代码或资产再分发许可。
5. [C，仅第三方主张] https://lijianfei.com/post/ai-3d-game-pipeline-opus-tripo-blender-unity-little-prince/ 声称某版本 Unity 6/WebGPU、Addressables 和约 2 GB 解码资源等；本研究未独立取得或校验部署清单、Unity 工程、优化配置，因此**不把精确版本号、115 个包、内存策略或 Auto-Rig Pro 命名后缀当作已证实实现**。
6. [A：排除误归因] 名称相近的 https://github.com/MMMvinki/little-prince-planet-world 是另一位作者的 React/Three.js 项目；未见证据表明是 Sac 的该游戏，不能把其代码当作目标工程或用于目标源码审查。

**源码位置可验证表**

| 调查项 | 可确认状态 | 证据级别 |
|---|---|---|
| 官方项目 README / 代码目录 / 核心源码行号 | **未获取，不存在可报告位置** | — |
| 官方项目 Git SHA / Release / 许可证文件 | **未获取，不得虚构** | — |
| 游戏官网源码指向 | 可见首页未发现；不是对全部动态内容的穷尽搜索 | B |
| 作者 GitHub 与 X 关联 | GitHub 个人主页直接列出 @Saccc_c | A（元数据） |
| 公开制作流程 | Tripo 合作案例详细描述 | B |
| 生产包大小、GPU/LOD/缓存内部策略 | 第三方说法，未独立检查 | C / 未验证 |

如果以后官方仓库上线：从作者 X、官网或已验证 GitHub 账号的相互链接确认；在 Muscle Atlas 仓库外独立 clone；记录许可证、固定 SHA、依赖/脚本/资产声明；先静态检查、必要时隔离运行；只形成带文件行号的补充审查，不直接复制进 Muscle Atlas。

## 2. 目标项目技术栈：证据与局限

[B，Tripo 的官方合作案例：https://www.tripo3d.ai/fr/blog/how-to-build-an-explorable-3d-game-with-tripo-and-ai] 文中描述：Fable 5.1 用于产品/叙事任务规划；Image 2.5 制作多视角参考；Tripo 将选定概念转为 3D 独立资产；Blender CLI 整理模型、场景及材质；Unity 组装场景和交互；Opus 5.5 辅助生产，Astra 帮助迭代。角色使用四视图 T Pose → Tripo Smart Mesh → Blender 中的商业插件 Auto-Rig Pro 绑定/蒙皮 → Mixamo 动画及重定向 → 在 Blender 用 IK 修正手与提壶把手的接触。页面本身不是完整游戏源代码、也不公开动画控制器实现或真实工程依赖清单。

[B 仅为案例描述；D 为适用性推论] 多视角先行、资产分治、通用动作打底、接触约束专项精修、盲审，是可以跨 Unity/Three.js 借鉴的**生产方法**，而非必须迁移 Unity 或使用付费工具的理由。

**当前无法确定**：实际运行中的 IK/FK 切换方法、骨骼层级与权重细节、动画层混合方式、是否使用运行时 IK、接触解算器、LOD 生成策略、动画资源如何复用、运行时 GPU 蒙皮路径、WebGPU 配置、纹理压缩设置、Addressables 触发条件、缓存/资源回收代码、GPU/CPU 性能测量。这些不得写为“源码已证实”。

## 3. Muscle Atlas 实际代码基线（已读指定文件）[A]

已检查 README.md、docs/rig-verification.md、docs/pulldown-motion-review.md、docs/equipment-and-grip.md、docs/roadmap.md、scripts/build-curl-rig.py、scripts/build-pulldown-rig.py、src/three/Scene.tsx（M2 分支）。旧文档中仍有已废弃的“闭合手部覆盖层”、早期“真实绑定未完成”等历史描述，**以较新的 M2 结果与 R1 实际报告为准**。

- README / docs/rig-verification.md / scripts/build-curl-rig.py：原静态 anatomy.glb 为 467 个独立源网格；弯举派生模型使用左臂两骨、蒙皮和姿态修正 Morph；旧版仍有肘窝压缩，源手张开。
- docs/pulldown-motion-review.md / scripts/build-pulldown-rig.py：高位下拉双臂解析式 IK、肩胛代理运动、121 时刻烘焙、共享器械时间轴；肩胛角度为创作假设，不是测得的生理轨迹。M2 最终版 32315eb 验收未通过，双侧拇收肌与拉杆穿透 P1 未消除；不能被新版 R1 探针的无器械视图“洗白”。
- docs/equipment-and-grip.md：曾试验假手壳后按用户要求撤销，后文旧段落是历史记录，源手仍不具有真实闭合包握；哑铃有本地原创六角器械资产。
- src/three/Scene.tsx：R3F Canvas、drei useGLTF、SkeletonUtils.clone、AnimationMixer，按运动时钟 seek，独立 anatomyId 选取、材质和角色颜色；当前弯举和下拉按模式加载两个派生 GLB，非统一发布资产。
- [R1 新事实，PR#5，fcb2706，docs/rig-v2/R1-summary.md]：Mac 已产出**隔离**的 27 关节共享原型，467 个基底源网格身份/坐标保留、两诊断 Clip、Blender 与 glTF 数值交换及三维浏览器探针。**未验收**：PulldownProbe 在 42/121 姿态触发既有面积塌缩门禁，最大边长拉伸约 3.988 倍；肩腋和肘部形变 P1 未解决；两个 FingerSocket 不是完整逐指 Rig。
- [Windows 新事实，PR#6，9c363d9，docs/biomechanics/exchange-v1.md]：已建立 OpenSim 独立环境、带版本的 JSON 坐标/姿态交换规范，区分模型参考态、绑定态和动画 0 秒；数值正确不等于解剖学正确。
- [A，源程序和独立验证] 软件和审查有真实 Node/Vitest/Playwright/GLB 验证；但零 glTF Validator 错误、标记点无偏移不是原始拇指接触或解剖正确性的证明。

**需要保留的实际接口**：每块肌肉独立 anatomyId/sourceName/BP/FMA、源三角形拓扑、原始手部不偷偷修改、两个动作与器械共享时钟、浏览器选择/材质/拖动、旧版失败证据、独立 M2/R1 审查及用户门禁。

## 4. 技术差距：可借鉴与不可直接迁移

| 主题 | 小王子证据 | Muscle Atlas 现状 | 最合适的研究结果 | 推荐 |
|---|---|---|---|---|
| 角色四视图 / 标准动作参考 | Tripo 合作案例 B | 已有高位下拉 reference.md 与有限多视角，无标定外部运动 | 为每个动作固定正侧背/手部/器械参考和变式/许可元数据 | **直接借鉴流程** |
| Auto-Rig Pro / 自动蒙皮 | 案例 B；内部代码不可得 | R1 隔离统一绑定，但肩腋变形失败 | 只把自动 Rig 当生成初稿；薄肌腱、独立肌群附着仍需自有约束 | **重新设计** |
| Mixamo / 动画重定向 | 案例 B | curl/pulldown 专门烘焙；R1 双诊断 Clip | 通用上肢骨骼动作可作初始关键姿态，不可视作负重标准动作或肌肉形变真值 | **可选研究** |
| IK/道具接触 | 提壶 IK 示例 B，内部算法未获取 | 下拉握点精确但真源手深穿杆 | 统一道具局部锚点、手掌/腕旋转与实际源三角形接触双检 | **优先验证** |
| 肩胛与肌腱 | 目标游戏无法提供内部解剖算法 | R1 附着与变形 P1；OpenSim 帧未完全标定 | 来源可追溯肌肉附着地标 + 修正姿态 + GLB 三角面检测 | **不能照搬游戏 Rig** |
| Blender 生产管线 | Blender CLI、分工、多视角审核 B | 各独立生成脚本及哈希/视觉包已存在 | 统一导入、参考态、烘焙、导出、哈希、50帧多视角检查的构建契约 | **优先验证** |
| LOD / WebGPU / GPU skin | 无目标源码；第三方声称 Unity WebGPU C | R3F/Three.js/WebGL 已工作；按动作切换 GLB | 先量加载、draw calls、帧耗时和内存，再小范围试 KTX2/Meshopt 或惰性加载 | **延后专项** |
| Multi-Agent | 官方案例含独立盲审提示词 B | 已有四专家复核、两轮上限、release gate | 把各阶段输入/输出和 owner 审批做成统一可复现构建契约 | **直接借鉴流程** |

### 4.1 角色 Rig 与真实解剖模型的根本差别

通用游戏角色常是表层连续网格与少量控制骨；Muscle Atlas 的 467 个**独立肌肉/肌腱/其它解剖结构**有不同的起点、止点和空间连续性问题。通用自动权重常按网格空间邻近传播，可能把跨关节肌肉“拉过关节”或让原始组织压到握杆内部。一个稳定的全身骨架是必要的、但不是充分的：每块肌肉的附着标定、姿态修正和真实网格测试必须单列。Mixamo 人体动作不包含本地拉杆、座椅、配重及肌腱物理边界；不采用所谓“让动画像游戏角色一样就算科学正确”的路径。[A/D]

### 4.2 Blender 可重复构建接口草案 [D，未实现]

建议未来约定输入：source_asset.sha256 + source_mesh_map + canonical_rig.json + attachment_registry + exercise_reference + clip_descriptor + equipment_contacts + blender_version + script_git_sha。输出：generated.glb、原生 .blend 源、joint_trajectories.json、manifest.json (模型 SHA、来源、依赖、许可)、preview 视频、50 帧关键图、质量检测 JSON、四个独立审查结论。

阶段顺序：动作与证据规格 → 冻结源与单位 → 导入/骨架 → 权重及附着 → Clip/IK → Bake → 导出 → glTF 验证与源身份核验 → 实际网格检测 → 浏览器取帧 → 盲审 → 所有者放行。生产 Agent 可在隔离工作树写资产；QA 与视觉/生物力学 Agent 独立只读；任何 FAIL/INCONCLUSIVE 均不得被 Build PASS 覆盖。失败时保留旧 SHA 和媒体，对候选分支回滚，不覆盖审查记录。

### 4.3 接触数据接口草案 [D，未实现]

动作级道具记录：rig_hand_id、original_hand_source_ids、prop_id、prop_local_frame (4×4)、wrist_reference_frame、grip_variant、time_s、controller_target、asset_hash、contact_rules。验收区别 **IK marker/桡骨位置** 与 **实际原始手/拇指三角面**；先核实左右掌坐标与拇指侧别；测试杆体为实际有限几何（不能只测无限轴线），步进 121 或更多时间样本，并独立记录夹挤、悬空和连续性。用户未批准正式逐指改变时，只能在隔离模拟夹具测 IK，对当前原始张手正式资产仍须标 K02 未通过。

## 5. 性能与资产管理：不能从目标游戏外推收益

[A：Three.js 官方 API] https://threejs.org/docs/pages/GLTFLoader 支持 Draco、Meshopt、KTX2；https://threejs.org/docs/pages/KTX2Loader 解释 GPU 压缩纹理，https://threejs.org/docs/pages/DRACOLoader 解释几何压缩。**这是 Muscle Atlas 可能用的能力，不是小王子已使用的证据**。

建议先采集：普通/运动/切换模式的实际 GLB 下载大小、纹理大小、scene mesh/draw calls、三角形数、主线程和 GPU 时间、WebGL context 与材料释放、cold/warm load、最低 FPS/95分位帧耗时。目标平台 macOS Chrome/Windows Chrome 各固定一组。候选措施按需加载/缓存、共享材质、延迟载入独立动作 GLB、KTX2/Meshopt、局部 LOD。所有性能数字必须在同一硬件、分辨率、相机、动作、材质和捕获负载下 A/B 比较；目前不能承诺具体百分比提升，也不推荐因 Unity/WebGPU 讨论直接迁移引擎。

## 6. 法律许可与来源风险

- **游戏工程源码**：官方仓库及许可证未取得，不能直接复制生产构建里的代码。
- **游戏角色/纹理/音视频**：网页可游玩不等于允许下载改编再分发；Tripo 平台与作者素材的授权须独立核查。
- **Auto-Rig Pro**：合作案例明确它是付费 Blender 扩展；本阶段不能购买或要求其为强制依赖，可先用 Blender 原生 Rig / bpy 完成研究。
- **Mixamo**：Adobe 官方 https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html 表示角色/动画可在许多项目中免版税使用；但将原始文件作为资源包分发、地区/账户条件及最新使用条款另需确认。此阶段仅研究接口，不下载再分发 Mixamo 原始动画。
- **《小王子》IP**：作品及具体角色形象的适用地域版权/商标/衍生设计权可能不同；仅研究技术方法，不复制角色或场景。
- **Muscle Atlas 自有源解剖模型**：BP3D / Z-Anatomy 各自原有许可与署名不可被项目源码许可证覆盖。

## 7. 三项最小验证实验（**尚未运行**；下列目标、成本与阈值均为 D）

### E1 统一骨架驱动弯举与高位下拉

- **目标**：在一个冻结 canonical rig + 467 源 ID / 基底几何上分别装载 curl 和 pulldown 两个 Clip，证明不必为每个动作重新生成整套绑定。
- **最小范围**：使用 Mac PR#5 的隔离 27 关节 R1 探针，不修改任何生产资产；只验证同一 skeleton 引用及两个独立 Clip 的运动、现有肩腋/肘窝形变警报和身份映射。
- **工具**：Blender bpy、glTF Validator、Three.js、Node/Vitest、Playwright；Windows PR#6 schema 做坐标对照。
- **建议未来改动位置**：scripts/rig-v2/、src/experimental/rig-v2/、tests/rig-v2/、docs/rig-v2/；本轮未改。
- **估计**：1–3 个工程日（复用 R1），现金成本零；不保证，取决于失败处与模型可用性。
- **机器门禁**：467 个源 ID 不变、float32 基底/三角顺序完全一致；同一冻结 GLB 上两段 Clip 可按任意相位 seek/重播；无 NaN/骨长明显漂移；沿用既有严重三角面积压缩检测，**不得把 R1 已知 42/121 FAIL 当作 PASS**。实际渲染 + 专业审查另设门禁。
- **失败条件**：需各自动作重新绑定骨架；丢 ID；损坏原始几何；现有 42/121 退化报警未改善却宣称通过；动作与绑定坐标不一致。
- **回滚**：只废弃试验分支/派生 GLB，保持 R1/M2 原始 SHA 和失败证据。

### E2 通用 IK 握持约束

- **目标**：通用局部道具握点+腕朝向+有限把手碰撞的输入输出能跨横杆和哑铃场景复用。
- **最小范围**：不改源手、不驱动正式手指，首先用单独的合成手部刚体/带标签测试代理和测试杆验证变换及实际有限实体接触算法；再只读回放当前下拉的原始拇收肌穿透失败，证明测试能拦截。
- **工具**：Blender IK、Three.js 网格接触几何、Node/Playwright，外部授权动作参考。
- **建议未来改动位置**：scripts/quality/、tests/quality/motion/、src/experimental/rig-v2/；本轮未改。
- **估计**：1–2 工程日初步契约；如增加原始逐指蒙皮需要另行立项和授权。
- **机器门禁**：左右局部坐标和杆半径声明；变换 round-trip 数值一致；合成测试真相集对相交/不相交正确判定；旧 M2 双侧拇收肌相交可稳定复现；相位 0/25/50/75/100 + 121 样本；虚拟标记点符合目标**不**自动令真实握持 PASS。
- **失败条件**：原始手组织穿杆却报告 PASS；反手镜像、无限杆轴线替代实际实体、擅自修改源手。
- **回滚**：隔离夹具删除或回退，旧生产 GLB 和 K02=P1 不变。

### E3 Blender 自动动作构建与多视角质量报告

- **目标**：在受控输入、固定 Blender 版本和源哈希条件下，重跑产生可比的派生动画资产和审查证据包。
- **最小范围**：选一个现有 curl 诊断 Clip 的隔离构建；命令行完成导入/绑定/烘焙/导出、Khronos 校验、121 轨迹、5 视角×5 相位×2 风格=50 张截图、视频和带 SHA 的 manifest；不修改生产模型和审查原文。
- **工具**：Blender CLI/bpy、Python、Three.js、Playwright、GLB Validator、现有 gate 机制。
- **建议未来改动位置**：scripts/rig-v2/、scripts/quality/、tests/rig-v2/、docs/research/；本轮未改。
- **估计**：2–4 工程日；基于现有 capture 管线复用，现金成本零。
- **机器门禁**：每次产物都记录源和结果 SHA、软件版本、命令、开始/结束状态；重跑在规定浮点/采样容差内相同；相机视图不裁切关键部位；所有人工审查可使用媒体；严格区分 EVIDENCE_COMPLETE 与 ANATOMY_PASS。
- **失败条件**：录屏非实际生产渲染、manifest 漏项、变更资产却未更新哈希、隐藏 P1 失败、未有真实动作证据却宣称完成。
- **回滚**：只回滚工作分支或输出目录；不触碰 main/PR#3/PR#5/PR#6 及审查冻结文件。

## 8. 按收益/难度/成本排序的建议路线

| 顺序 | 候选 | 预期收益 | 难度 | 成本 | 取舍与触发条件 |
|---|---|---|---|---|---|
| 1 | E3：标准化 Blender→GLB→多视角报告 | 很高 | 中 | 2–4 工程日 | 先证明重复生成/自动验收 |
| 2 | E2：通用接触与姿态约束 | 很高 | 中高 | 1–2 日起 | 当前握柄 P1 的直接验证，不越过手指授权 |
| 3 | E1：两个动作统一骨架实际复用 | 极高 | 高 | 1–3 日探索 | R1 目前有肩腋/肘窝 42/121 FAIL，不得仅演示两段 Clip 算成功 |
| 4 | 外部通用动作 retargeting 研究 | 中 | 中 | 研究 0.5–1 日 | 仅初始姿态/非运动标准；检查 Mixamo/其它源许可 |
| 5 | 网格/纹理压缩、LOD、缓存专项 | 不确定 | 中高 | 测量后估算 | 当前不阻塞质量；避免无证据性能改动 |
| 6 | Unity 重写、付费自动绑定或复制游戏资产 | 对当前目标低 | 极高 | 付费/迁移风险 | **不采用** |

建议 owner 在研究报告审阅后一次只批准单个最小实验；与 Mac R1 和 Windows OpenSim 双 PR 的已知缺陷并行比较，不得继续被“看起来流畅/单测绿色”误导。

## 9. Agent 协作、质量责任与停止条件

| 阶段 | 输入 → 输出 | 主要 Agent | 验收 |
|---|---|---|---|
| 需求/参考 | 动作变式、可靠参考、版权条款 → exercise brief | 科学/产品 | 引用与证据等级齐全 |
| 资产准备 | source SHA、ID map → 规范源/局部器械 | 资产维护 | 源 ID/几何校验 |
| 骨架与蒙皮 | canonical rig、附着地标 → 骨架资产 | Mac Rigging | 实际权重/肩腋/肘窝检查 |
| 动作与 IK | Clip、bar/grip targets → baked GLB | Mac 动画 | 真源几何而不只 marker |
| 运动对照 | Mac 姿态包 → schema/不确定性报告 | Windows/OpenSim | 坐标/矩阵/覆盖正确，不能假称临床 |
| 运行时 | 带签名模型/Clip → 三维交互 | Three.js 开发 | picking/seek/style/loop |
| 自动质量 | 真实候选 SHA/GLB → 数值、碰撞、录屏/截图 | 独立 QA | 报警强制显性，不能测试器绿代替模型绿 |
| 视觉和科学复核 | 不可变证据 → 四份独立结论 | 独立审核 | FAIL/INCONCLUSIVE 可阻断 |
| Owner 门禁 | 完整包+缺陷 → 批准/返工/停止 | 用户 | 明确批准前不得 merge |

已授权本次工作只包括**研究报告**。研究分支不得修改生产骨架、程序、模型和受审资产。后续若获得 Sac 游戏官方源码，先重新核定许可证与 SHA，再另写“源码复核增补报告”，不能悄悄把旧 C/D 推论升级。

## 10. 一手链接与可信度登记（访问日 2026-10-17）

- [B] 游戏官网：https://littleprince.dev/ （仅官网首页及用户可见说明；无源码）。
- [A：公开账号元数据] Sac-Y GitHub / 仓库：https://github.com/Sac-Y 、https://github.com/Sac-Y?tab=repositories （X 账户关联与公开库列表，不是目标游戏源码）。
- [B/C：原帖二手索引，X 正文直接抓取403] https://x.com/Saccc_c/status/2109962425512734739 、https://nitter.rdrama.net/demisama_ （作者开源预告）。
- [B：直接商业合作伙伴披露的制作流程] Tripo：https://www.tripo3d.ai/fr/blog/how-to-build-an-explorable-3d-game-with-tripo-and-ai 。
- [C：尚未独立复核的线上构建分析] https://lijianfei.com/post/ai-3d-game-pipeline-opus-tripo-blender-unity-little-prince/ 。
- [A：本项目代码与冻结审查] https://github.com/hengqi61-maker/muscle-atlas/pull/3 、https://github.com/hengqi61-maker/muscle-atlas/pull/5 、https://github.com/hengqi61-maker/muscle-atlas/pull/6 。
- [B：工具功能，不是游戏源码证据] https://threejs.org/docs/pages/GLTFLoader 、https://threejs.org/docs/pages/KTX2Loader 、https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html 。

**最终状态**：研究已完成、官方游戏源码未取得、未克隆或运行目标工程、三个实验均未执行、无源码或资产移植。等待 owner 审查后再决定是否另行授权编码。
