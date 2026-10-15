# 债务推进交付 · 2026-10-15

完成：真实左臂双骨蒙皮/形态键/GLB/AnimationMixer最小闭环，取代椭球原型；下载器缓存与中断恢复；保存可复现脚本、测试和截图。

验证：TypeScript/Vite构建、6项Vitest、8项Python下载器测试、2条Playwright真Chrome流程、KhronosValidator0错误0警告、Three.js实际顶点/骨角度采样。Blender每次干净后台加载原始GLB、生成派生资产和.blend。npm audit另行检查。主JS包体积警告仍存在，未隐藏。

替代方案：保留本地verified cache，下载工具采用系统代理感知urllib；有限重试只作传输恢复。真实资产使用手工双骨与烘焙姿态修正，未引入虚假肌肉生理指标。

永久修复：有效缓存不请求网络；无效/中断内容不会作为正式文件发布；权重/动画导出起始帧偏移修正为0..120；skinned node层级警告消除；目标网页已用真正SkinnedMesh和AnimationMixer替代层级椭球。

延期债务：MODEL-DOWNLOAD只剩原未指定代理curl直连与历史reset来源；MODEL-RIG只剩软组织质量、附着/接触与握持姿态。两个原始债务保留为DEFERRED，最小闭环不被偷换为全部解决。没有ACCEPTED_RISK或OPEN项。

剩余风险：内肘局部压缩指标异常（见rig-verification.md），没有完整皮肤层/碰撞测试/肌肉力学模型；左臂之外仍静态。大型资产约50MB总量与主包需后续性能优化；训练数据备份恢复/日历仍未实现。
