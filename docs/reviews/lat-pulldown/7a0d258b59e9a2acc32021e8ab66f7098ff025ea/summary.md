# Muscle Atlas · 精确旧版盲审 M0 / M1

**M0完成；M1首报已冻结，候选动作FAIL。M2、面拉均未开始，USER APPROVAL: pending。**

候选Git SHA：`7a0d258b59e9a2acc32021e8ab66f7098ff025ea`。
高位下拉GLB SHA256：`56b3ca231dda14100d64233758da2116282547b472afd4fc9b24160f345fee05`。

## 版本与隔离

精确提交在独立worktree检出。源码归档、原始/动画GLB、全部生产输入哈希、轨迹与相机参数均保存。Git没有受管理的.blend：另保存本地相关场景及SHA256，标为UNVERIFIED且未用作首报依据，不能声称与GLB一一对应。

PR#2的13项改动全部检查，运行源码/资产与候选一致；复用其角色、流程、验收、CI和完整性脚本。新增基础设施在另一分支codex/motion-quality-infrastructure，不覆盖main。刚开始的M2在最新指令到达后已中止，未做产品修改。

四位审查者为重新实际启动的独立子Agent（fork_turns=none），提交前禁止旧缺陷记录及彼此报告。三子Agent并发限制下分批执行。首报哈希见[first-report-freeze.json](first-report-freeze.json)；然后才写[历史对照](historical-comparison.md)。协调者保留先前上下文，未声称其自身也是盲的。角色只读要求不是OS安全沙箱。

## 独立审查结论

|角色|结论|边界/报告|
|---|---|---|
|Biomechanics Reviewer|FAIL|[原始首报](reviews/round1/biomechanics.md)：足部穿透与肩袖附着问题；骨长/躯干等仅窄范围PASS|
|Visual Reviewer|FAIL|[原始首报](reviews/round1/visual.md)：跨材质、关键帧与视频确认悬离解剖组织；握持方向INCONCLUSIVE|
|Exercise Science Reviewer|PASS（限定）|[原始首报](reviews/round1/exerciseScience.md)：定性角色和提示合理；不批准完整动作技术|
|Software QA Reviewer|功能检查PASS；性能适用性INCONCLUSIVE|[原始首报](reviews/round1/softwareQa.md)：身份、控件和资源有效，不是运动学放行|

## 缺陷优先级

未建立有充分证据的P0。下列为未修复问题，不是已接受风险。

|ID|级别|证据与可复现问题|
|---|---|---|
|B01|P1|双侧冈上肌、冈下肌、肩胛下肌、小圆肌全部权重100%Thorax；21时刻实际顶点位移0，而肩中心移动约41.5mm、肩带旋转12°。src生成器默认attach=0，组织附着随动缺失|
|B02|P1|左右足背短伸肌各397个实际顶点处于踏板实体内；21时刻持续。模型坐标平台y[.26,.30]m，实际网格bbox穿入。不是凭画面推断悬空|
|V01|P1|悬离的解剖材质片段位于拉索附近，双手近景、两种材质及录像均可复现。视觉首报未强行命名其节点；需要隔离/绑定追溯|
|Q01|P2|非循环到4秒后再点播放不能重启，必须手动拖回0；由新软件Agent在生产浏览器独立复现|
|Q02|P2观察/证据缺口|暂停仍更新蒙皮边界；采样约14–16rAF帧/秒但存在并行采集负荷、没有约定预算，不宣称性能回归或硬件上限|
|S01|P2|肌群映射为选择性覆盖，肱桡肌等未说明覆盖范围；应标明代表性列表或补覆盖依据|
|S02|P2|源ID可追溯但角色分类缺少逐项科学依据/置信度元数据，尤其肩胛稳定与动态控制的关系|

K02掌面朝向/拇指对握/真实表面接触仍INCONCLUSIVE，不能因标记误差小而通过，也不能因遮挡就断言反握。肩带已动不等于肩胛-肱骨协调已验证。K06仅示意同步PASS，完整绕轮物理连续性未认证。座椅/压腿垫完整接触、主动播放每帧速度与警告清单仍有覆盖缺口。

## 真实运行与材料

- [47.32秒实际网页录像](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/full-rep.mp4)，另保留[原生WEBM](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/full-rep.webm)。四视角、各两次循环，1×真实播放，不是插图或静帧插值。握持录像相机固定，另以逐阶段近景补充。
- [20帧总览](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/contact-sheet.png)，另有Clean/Real两种材质、正侧背和左右手共50张全尺寸图，metadata记录相机和遮挡设置。
- [121时刻运动轨迹CSV](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/joint-trajectories.csv)、[关节变换JSON](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/transforms.json)、[467网格×21时刻实际顶点统计](/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258/artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/mesh-kinematics.json)、[数值连续性检查](trajectory-check.json)。顶点入盒是穿透证据，零计数不是无三角面穿透证明。
- 新工作目录npm ci、build、9项unit、8项asset、两项GLB检查、3条Chrome流程全部exit0；验证器0错误0警告。生产页面另测实际选取、seek、暂停、循环和风格。各Agent区分亲自运行与使用提供的日志。
- 新基础设施12项门禁测试通过；TOML语法/角色必填字段通过；freeze、measure、mesh测量、完整capture包装命令真实跑过。骨长变差约10^-7m、采样相邻最大旋转3.49°、首尾关节位置差0：这些只证明数值约束，不证明动作科学。
- review门禁通过；release负向测试正确拒绝：专业非全PASS、P1未解决、owner未批准。next-action输出WAIT_OWNER_SCOPE、mayModifyProduction=false。自动测试和材料齐全不是专业验收。

## 可复用基础设施与边界

新增根协调角色，复用五个专业配置；提供命令化freeze/measure/mesh-kinematics/capture、源身份/哈希、轨迹检测、报告冻结、证据完整性、独立会话与生产者隔离检查、两轮返工上限、owner审批和CI测试。高位下拉是首个adapter；未来动作需新增自己的adapter和验收地标，不宣称已经实现面拉。

本地Codex CLI缺少原生可执行文件，官方文档直接获取链路也失败。桌面真实子Agent已使用；CLI角色自动加载与最新配置语义没有运行验证。没有改系统安全设置、购买资产、覆盖main或合并PR。配置文件的行为约束不能替代真实权限隔离；JSON审批字段也不是身份认证，必须查验真实用户审批来源。

## 下一阶段待你决定

建议M2先处理B01肩袖附着、B02支撑接触、V01组织脱离，并补K02原始手部几何地标/接触测量；保留原始手，不生成替代手壳、不擅自折叠源手指。修复后换新SHA、新证据和独立复核，完整返工最多两轮。Q01可作为小范围软件修复；面拉另立里程碑，在你明确批准后再开始。

本轮没有执行这些产品修复，也没有用“已知限制”关闭关键问题。

## 任务与债务结算

- 完成：精确M0、四新上下文盲审M1、首报冻结后对照、可执行基础设施与真实验证。
- 产品变通：无，基线源码/GLB未改。
- 已解决：采集工具使用当前R3F状态和固定Playwright ffmpeg依赖，复用完整原生录制路径成功；基础设施问题修正不等于产品问题修复。
- 延期：MODEL-RIG及本报告问题等待M2批准；CLI原生文件缺失和官方文档抓取故障保持DEFERRED。无ACCEPTED_RISK，无任务相关OPEN。
- 风险/下一证据：肩/腕解剖标定、真实表面接触、组织碰撞和物理绳路、受控性能基准仍未建立。不得自行宣布产品级通过。
