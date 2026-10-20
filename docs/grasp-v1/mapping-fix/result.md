# 实际抓握返工：候选被拒绝（2026-10-20）

## 结论
实际执行了修复、Blender构建、121帧双动作全三角检查、跨引擎测量、真实渲染和浏览器检查。**真实抓握未修好；候选被拒绝，未接入主页或替换生产资产。** 未将本次叫作旧M2的新一轮通过。

## 实际修复代码
复用现有30指骨/API：纠正手指空间顺序与分类不一致、小指分区不可达、供体权重不守恒、Wrist计入但未扣减、骨骼与顶点分区坐标不同的问题。前臂膜和腕部支持组织不再被当作指段重新分配。

Blender构建前后467网格基础坐标散列相同、27原骨参考矩阵相同。供体质量误差最大2.98e-8，非供体预导出误差0。实际导出22/30指骨有权重，小指每侧MCP28个影响槽；PIP/DIP仍缺失，不强行把肌肉变成指腹。

## 实测与拒绝原因
- 第一个GLB `3c1274de4492270dea8e0bb787a1703984ce42123302dda86870f9a1aa7e85b6`：原生导出产生微小坐标舍入，不能满足严格原POSITION要求；保留并拒绝。
- 第二个GLB `f33ae9dbe95973e98f41fa7bd178d2946971dfed4cebf4dff58464ac7c45d11b`：在冻结原GLB上只附加指骨和新权重数据，原二进制前缀/POSITION/index和27原骨节点保留。实际导出坐标集合差异0，原27骨世界矩阵差异0。
- 但按POSITION最近点搬运不能证明重复坐标源顶点的逐一身份。权重对应检查标记INCONCLUSIVE；初版过宽PASS输出另存，独立审查后缩小声明，未删除最初证据。
- 两版双动作各121帧、全1,092,000三角检查：Curl39/121、Pulldown91/121严重压缩；最大边长比约265.51，比原控制器修复版77.886更差。
- 真实握柄接触仍FAIL，保留版本最小有符号距离约−23.16mm。原生Blender/Three最小距离最大差约0.2077mm，未解释，不宣布接触数值一致。
- 新骨架局部姿态121样本Blender/Three关节原点差最大0.624微米，仅该适配检查通过。
- 真实Blender31帧/视频、Three浏览器15张关键帧/视频；播放、暂停、重播通过，但画面可见组织散开，不能通过视觉验收。
- 软件构建、16项Vitest、26项quality、10项grasp测试通过。软件测试不能推翻上述FAIL。

## 独立复核
只读子Agent grasp_candidate_review实际审查生成代码、报告及第15帧，结论REJECT。确认程序顺序/守恒修正；发现导出后验证缺口及最近POSITION对应的盲区。没有模拟四类专业角色、没有Owner批准。

## 根因边界
现有空间分区不是解剖附着：小指肌仍大量落到中/无名指，拇短展肌跨拇/食指，骨间肌会落到拇指。现有467选集没有完整五指指腹表面。刚性杆埋入掌心与缺失接触几何不能靠加大屈曲角度解决。继续使用该启发式当成真附着会造成更大拉伸，故停止该候选修改。

生产仍使用原版本并保留未验收标记。需要真实手骨/肌腱的同版本对应、关节与组织附着地标及缺失可见结构的明确处理范围；不能擅自补皮肤壳或把缺失组织拉成手指。

## 重跑
```
blender -b --python-exit-code 1 --python scripts/grasp-v1/build_mapping_fix.py
node scripts/grasp-v1/preserve_source_glb.mjs
GRASP_ASSET=artifacts/grasp-fix/mapping-preserved.glb GRASP_EXPORT_REPORT=artifacts/grasp-fix/preserved-export-verification.json node scripts/grasp-v1/verify_mapping_export.mjs
GRASP_ASSET=artifacts/grasp-fix/mapping-preserved.glb GRASP_SEQUENCE_OUTPUT=artifacts/grasp-fix/preserved-sequence node scripts/grasp-v1/official_sequence.mjs
node scripts/grasp-v1/full_regression.mjs --asset artifacts/grasp-fix/mapping-preserved.glb --sha256 f33ae9dbe95973e98f41fa7bd178d2946971dfed4cebf4dff58464ac7c45d11b --output artifacts/grasp-fix/preserved-regression
```
固定工具Blender5.2.0 LTS、Node26.5.0。原生导出首次构建散列已记录，重新构建需重新计算并明确传递新散列；禁止默认相信路径。证据中的脚本快照记录实际执行版本。
