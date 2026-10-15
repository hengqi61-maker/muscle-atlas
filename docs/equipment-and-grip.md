# 哑铃、握持与高位下拉 · 2026-10-15

## 用户反馈对应的实改
原圆柱哑铃替换为原创六角橡胶头模型：倒角胶头、几何滚花28mm金属握柄、连接肩、端面徽片和无品牌8字标记。胶头与握柄同轴；外部来源不是已经下载的资产。独立文件public/models/equipment/detailed-hex-dumbbell.glb，尺寸和哈希见docs/evidence/equipment-manifest.json，生成器scripts/build-equipment-preview.py。显示用标记不会改写用户实录重量。

原手指/肌腱张开导致握柄穿过空掌。动作模式新增原创闭合手部表面：连续掌面、四指弧、对握拇指、腕部连接、指甲；不是完整医学皮肤数据库或扫描手。原始静态atlas始终保留。动作派生资产将远端组织折入闭合表面，手部独立源mesh以coveredByGripSkin标记被表面遮盖；可切换“握持表面层”。这是一种显式呈现层，不把手指外观当肌腱力学结果。弯举中手和哑铃共享Forearm绑定；高位下拉有独立左右Hand骨，轴向对齐斜握柄。

## 外部资产调查与未完成项
[Innerscene原始六角哑铃](https://www.innerscene.com/tools/library/3d-parts/hex-weight-dumbbell-32966c1b)页面声明CC0、约5k三角面、33.9×13.3×15.3cm，并提供下载按钮。官方download API在本地返回403，未获得文件、未验证几何、没有绕过限制或使用其资产。另查[CreativeTrio/Poly Pizza](https://poly.pizza/m/PW9q10xh5g)，标CC0但low-poly，普通请求也未取得文件；GitHub候选未找到明确更好的真实资产。

本次使用原创细节模型；不将其称为下载模型或扫描模型。若以后普通授权下载可用，须校验字节/材质/许可并在同一握持基准下替换。当前第三方候选不参与本仓库资产授权。

## 高位下拉联动
选择性接入feat/lat-pulldown-equipment-prototype的器械代码，保留main中的真实绑定，不用旧分支覆盖。旧1.05m握宽与1.96m杆高超出现有人体坐姿臂展，因此调整为共享metric config，并同时校准器械和人体。

src/data/pulldown-config.json同时被Three器械、Blender烘焙与验证器读取。双臂解析两骨IK在Blender逐帧烘焙，不伸长骨骼或夹限不可达点；腕部控制对齐斜杆。髋/膝/踝骨设置坐姿；坐姿与肩带是近似模型，腿垫/皮肤接触尚需精修。真实467个源网格保留；没有用普通皮肤人冒充肌肉人体。

## 可运行和验证
- npm run build / npm test / npm run test:assets / npm run test:rig / npm run test:pulldown / npm run test:e2e。
- Blender重建：scripts/build-curl-rig.py、scripts/build-pulldown-rig.py、scripts/build-equipment-preview.py；共同几何在scripts/grip_geometry.py。
- curl/pulldown两个GLB的KhronosValidator与Three运行时报告在docs/evidence/。
- 高位下拉121帧实测双掌握点，误差阈值1mm，实际约0.03mm；手轴对杆方向误差<0.001°；骨长不发生可见伸长。这证明约束传输一致，不证明皮肤/器械完全无穿模。
- 弯举掌/柄锚点同帧误差0；实际浏览器检查暂停、拖动、切换、原肌肉选择与记录持久化。
- 三个Chrome流程使用独立5175端口并关闭HMR。曾因测试中修改源文件导致热更新重置状态；另修复响应监听晚于导航的竞态。原失败断言均保留并在干净服务下重跑。

## 剩余风险
手部是简化原创表面，尚未达到扫描资产质感或完整逐指骨骼；内肘、肩带、臀腿与腿垫局部软组织仍待校准。完整碰撞和肌腱负荷没有验证；动态皮肤层仅手部。多份GLB使首次切换下载体积较大，运行时使用本地缓存，无登录、收费和OAuth。
