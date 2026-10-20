# Muscle Atlas 当前状态

唯一日常入口：`npm run dev` → http://127.0.0.1:5173/ 。先从肌肉探索开始；动作预览和训练记录各自独立。研发说明和诊断工具默认折叠。

## 已达成
- 467 个真实解剖网格、结构搜索/点击拾取、双材质、隐藏与恢复。
- 哑铃弯举与坐姿高位下拉器械联动预览；统一播放、暂停和拖动。
- 本地实际训练记录、重量/次数/RIR、JSON 导出；无伪造历史。
- 隔离的27关节统一骨架、30根附加指骨实验、可重复动作构建与121帧检查。
- Blender/Three坐标适配修复、跨引擎接触验证、Windows/OpenSim参考及独立历史审查。

## 未达成
动作尚未获得产品验收。抓握穿模、肩腋和肘窝形变仍FAIL。诊断Probe不是标准训练动作。计划/热力图/GoogleCalendar尚未接入；没有定量肌肉力或激活模拟。

## 阅读顺序
产品目标：[PRD](PRD.md)；结构：[architecture](architecture.md)；最新动作结果：[continuation-report](grasp-v1/continuation-report.md)；资产许可：[assets-and-licenses](assets-and-licenses.md)。历史review/证据仅对各自固定SHA有效，不能当成最新成功结论。不要根据目录名推断代码正确性。

## 整理边界
移除主页重复动作入口、重复警告、过期E03探测请求与快捷入口。保留诊断能力但默认折叠。保留唯一源码、模型、测试及冻结失败报告；只删除已经核对在完整备份中存在的重复打包中间文件。旧实验不自动并入生产。

纯文本源码审阅：`python3 scripts/export/review_text.py --output /tmp/Muscle-Atlas-Source-Review.txt`。只输出当前核心源码和少量必要说明，不嵌入PNG/GLB/压缩包或全量轨迹。

本次删除206,134,727字节重复打包文件（已逐项核对完整ZIP内相同内容或已上传的固定SHA证据包）；保留两份分享ZIP及全部唯一证据。删除清单位于分享目录cleanup-inventory.json。未重写Git历史，也未清除历史失败门禁。
