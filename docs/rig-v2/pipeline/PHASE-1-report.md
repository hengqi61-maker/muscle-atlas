# E3 / M-A–M-E 第一阶段实际交付

状态：**构建可重复、证据完整；动作几何仍失败，未获产品验收。** PR #8 以 PR #5 分支为基线。代码审查候选 `19ba4ee4d1e9ab06238f95ecb8422b877c7652f6`；本报告后续提交只加入证据和文档。main、冻结 R1、原始手部、正式动作及历史失败报告保持不变。

## M-A：实际执行，而非旧命令包装

从固定原始 GLB、467身份映射、现有27节点参考矩阵及原权重注册表重建干净 Blender 场景；不重新猜测骨架或权重。输入动作来自冻结原生 R1 的真实121帧观察，不是重写旧公式、人体实测或训练规范。原生轨迹有原 native SHA、原 Release ZIP/member 和来源说明。

|实际运行|执行边界|耗时|结果|
|---|---|---:|---|
|run-a / run-b|两个独立原生重建，再连接相同 encode/Chrome/geometry/validator/finalize 阶段链|原生782.211 / 753.190秒|GLB字节一致，完整媒体与软件消费通过|
|cold-cli-a / cold-cli-b|统一 `build_motion.py` 各自从空目录完整运行|565.146 / 568.451秒|两次 exit0，完整管线通过，几何FAIL|

四份 GLB SHA256均为 `65a3dcb59257394e2b97bc3ddb15a94fd923ffc43972ef6014dfdc1513395f25`。结构、源身份/基底面序、权重、inverse-bind与动画通道一致；121个姿态矩阵最大差0，优于预声明2e-5绝对元素容差。本实验比较器额外要求二进制buffer完全一致，拒绝缺帧、骨名错配、非有限值或短矩阵；没有把错误当前结果固化为解剖golden。

每次均有 GLB、Blend、121轨迹、50张原生关键帧、原生完整动作MP4、50张真实Chrome关键帧和独立完整周期WebM。50张为两种材质×五相位×正/侧/背/左右手。实际Three使用GLTFLoader/AnimationMixer，检查121时刻、源三角面拾取、暂停与完整循环；它不是虚拟握点验收。

两次 cold CLI 完成时的代码为 `1f6db60…`。之后 `19ba4ee…` 只修正 IN_PROGRESS/原子PASS或FAIL状态落盘，做了真实无效GLB失败回归和已有真实输出副本的成功finalization回归；**没有把这次元数据回归计作新的原生构建，也不声称19ba又冷启动了两遍**。原始清单未被覆盖。详见 [结果JSON](results/summary.json) 与执行阶段哈希。

## M-B：全三角面定位，保留失败

冻结 R1 SHA仍为 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`。

- 对全部1,092,000个导出三角面、每动作121时刻实际蒙皮计算：Curl39/121严重报警；Pulldown91/121。旧抽样Pulldown42/121结论保留，覆盖不同不能当作恶化或改善趋势。
- 弯举双侧肱桡肌 BP8244/BP4833 首次严重报警frame41；旋前圆肌BP8015/BP5568为47；肱二头长头BP8816/BP5566为54。细节包含真正三角/顶点索引、骨权重、关节世界矩阵和rest/posed坐标。
- 最大3.988438×边长比定位右肩胛下肌 BP4795/FMA13414、Pulldown frame0、triangle914、edge456–466。源边长0.001190418797m，权重涉及RightScapula/Humerus；frame0已是抬臂姿态，不是源模型rest。
- 选定详细证据源坐标回查540唯一、411重复坐标歧义、0未匹配；保留AMBIGUOUS，不把导出顶点或源GLB连通关系冒充上游Blender原始polygon ID。
- 生成10张带BP/FMA/相位/三角ID的真实网格局部rest/LBS对照。它们是隔离软件正交诊断，不证明周围组织接触或生理收缩。

新 Curl 派生资产同样全三角×121检查，39个姿态FAIL，最大边长比1.595631677。所有权威门禁仍是面积比<.05、每mesh数量>3 **OR** 比例>1%，边长比>2。保留的原生 `geometry.json` 是较早五阶段/边长3的非权威诊断；最终状态只由全三角121时刻的 `geometry-authoritative.json` 决定，未以较宽screen替代原门槛。

详见 [归因方法](attribution-method.md)、[归因结果](attribution-results.md) 与仓库 `artifacts/motion-pipeline/attribution/report.json`。

## M-C / M-D：复用与接口边界

独立结构检测证明冻结 R1 两 Clip共享一套skin、27joint、467源节点与实际positions/joints/weights/inverse-bind buffers；各81个相同joint目标通道。没有每动作重新绑定。**当前没有独立形态修正层，不能说它已通过跨动作修正验证。** 结构复用不意味着解剖连续性已满足。

Windows ff7fc70尚未发布通用contact schema。已在PR6提交具体数据请求及 [接口清单](windows-interface.md)。本阶段未私创不兼容规范、未虚构IK适配成功。原生 [轨迹说明](trajectory-format.md) 是内部观察，不是新的Windows交换格式；真正互通继续使用既有W2规范和A/B对齐。真实抓握与道具接触仍INCONCLUSIVE，未改变手指姿态。

## M-E：独立审查与实际验证

四位真实独立子Agent只读审查，随后核对元数据补丁与资产哈希；制作Agent没有自行放行动作。

|层级|实际结论|
|---|---|
|BUILD|PASS：重复结构、源/权重、字节buffer、121轨迹|
|SOFTWARE_TEST|PASS：24项新增回归；原app构建、13Vitest、26旧质量测试；实际Chrome消费；Khronos0errors/0warnings|
|MOTION_GEOMETRY|FAIL：完整三角面保持原报警|
|BIOMECHANICS / VISUAL|FAIL：工程形变/训练展示不合格；定位证据有效|
|EXERCISE SCIENCE|INCONCLUSIVE：附着/握持未标定，诊断声明边界合格|
|OWNER_APPROVAL|PENDING；不能merge或正式替换|

原两Clip冻结Chrome协议另实跑242时刻、100PNG、两完整cycle，47.863秒PASS。此测试使用600秒工作量预算，不是240秒SLA；没有声称FPS、跨机器、像素或Blend字节确定性通过。原生384px细节不足以单独做局部验收，需结合1000×900Three近景和隔离图。

[四份独立报告及审查元数据](reviews/) 保留原b50发现和最终适用性；报告由协调者记录真实独立返回，未模拟角色。两个软件返工分别修复候选commit绑定、校验失败后磁盘误留PASS；没有第三轮M2返工。历史M2两轮及失败结论不变。

## 可重跑命令

环境：本次实际Blender5.2.0LTS、Nodev26.5.0、Chrome155.0.8059.84；依赖由package-lock约束。定义中Blender/ffmpeg路径是可检查的本机工具配置；源资产与数据路径为仓库相对路径。输出目录必须全新，已有结果不能被覆盖。

```sh
npm ci
python3 scripts/rig-v2/pipeline/build_motion.py --definition config/rig-v2/motions/curl-probe.json --output artifacts/motion-pipeline/repro-a
python3 scripts/rig-v2/pipeline/build_motion.py --definition config/rig-v2/motions/curl-probe.json --output artifacts/motion-pipeline/repro-b
python3 scripts/rig-v2/pipeline/compare.py artifacts/motion-pipeline/repro-a artifacts/motion-pipeline/repro-b --output artifacts/motion-pipeline/repro-comparison.json
node --test tests/rig-v2/pipeline.node.mjs tests/rig-v2/attribution.node.mjs tests/rig-v2/reuse.node.mjs tests/rig-v2/pipeline-review.node.mjs
python3 tests/rig-v2/pipeline_compare.py
python3 tests/rig-v2/pipeline_failure.py
node scripts/quality/pipeline-review.mjs artifacts/motion-pipeline/cold-cli-a/manifest.json --review=docs/rig-v2/pipeline/reviews/review.json --candidate=19ba4ee4d1e9ab06238f95ecb8422b877c7652f6
```

加 `--release` 必须失败退出：当前几何FAIL、专业审查未全PASS、Owner未批准。新生成的不同资产/候选必须重新冻结审查，旧review不可借用。完整复现/阶段链命令见 `scripts/rig-v2/pipeline/README.md`。

## 债务与停止点

主目标：E3重复构建实验、已知P1归因、统一复用核验、Windows数据清单和自动审查交付已完成。保留workaround：无；WD0020世界节点/退出码、WD0021捕获器重复计算/取消后误写结果、WD0022候选绑定、WD0023失败状态落盘已实证RESOLVED。项目检查0OPEN、无新增ACCEPTED_RISK；历史解剖/抓握等DEFERRED没有被关闭。

当前结果满足源网格完整与结构复用，**没有同时满足解剖连续性**。已停止权重/形变修改，等待Owner选择后续实验：

1. 有来源的附着/骨轴标定＋局部单变量权重/运动敏感性对照：依据更强，先分离原因，成本是地标与双侧/留出姿态资料。
2. 可复用姿态空间修正：保留基底源几何、按关节姿态而非动作名索引，验证两Clip及插值；风险是过拟合或掩盖错误端点，须与附着依据一起审查。

不自行换正式骨架、改手指、开始面拉或合并main。
