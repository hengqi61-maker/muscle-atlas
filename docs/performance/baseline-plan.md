# 可重复浏览器性能基线

运行框架为 React Three Fiber / Three.js WebGL。当前测量不改变渲染器或骨架。既有 Mac M1 录像中的暂停/并行采集帧率不是硬件基线；本轮另建原型。

```powershell
npm.cmd run build
node scripts/infra/benchmark.mjs --headed --seconds 5 --repeats 3
```

默认独占 `127.0.0.1:5187` 生产 preview；占用即失败，不复用未知服务器。工具只关闭自己启动的进程。也可显式 `--url` 指向已知本机生产 preview。输出 `artifacts/windows/performance.json`。不记录录像以免编码负荷污染采样。每轮新页面，共同 Chrome context，后续轮次可能缓存命中；资源 timing 中 transferSize/decodedBodySize 保留，冷热数据不能混在一组宣称冷启动。首个结果为原型基线，不是 SLA。

四种场景：静态 atlas、curl 播放、pulldown 暂停、pulldown 播放；每种 1.5 秒预热、5 秒采样，重复 3 次。窗口 1440×1000 / deviceScaleFactor 1，实际 Canvas pixel ratio、相机、机器电源模式/刷新率/温度应在正式基准补充固定。动态场景保留原 UI 的循环/1×播放。所有生产模型/脚本 SHA 和浏览器/GPU 适配器记录，GPU 不能假定为独显。

|指标|采集来源|解释|
|---|---|---|
|rAF/s、帧间隔 p50/p95/p99|浏览器 rAF 时钟|显示调度与主线程共同影响，不等于 GPU timer|
|Draw Calls、Triangles|当前 Three renderer.info|每帧调用与三角形范围；不等于独立网格数|
|几何/纹理对象数|renderer.info.memory|不是 RAM 或显存字节|
|JS heap 字节|Chromium performance.memory|可能受 GC/精度限制，不是进程 RSS|
|主线程 TaskDuration|CDP Performance metrics 区间差|忙碌时间，仍需 trace 定位函数|
|资源加载毫秒与传输字节|Resource Timing|缓存、解析和解压要分别解释|
|GPU 设备和 renderer|CDP SystemInfo / WebGL renderer|实际适配器；GPU elapsed 当前为 null，未伪造|

只凭帧率不能区分 CPU/GPU。下一步在冻结资产/相机条件下做独立实验：降低 DPR 看像素填充敏感性，减少可见几何看提交/顶点敏感性，暂停动画与蒙皮更新做 CPU 对照，并结合 Chrome trace 的 JS/GC/布局与 GPU timer query（必须检查 disjoint）。本轮采样观察可指出问题候选，不能给出已证实的 GPU 瓶颈结论。

LOD 需可测的几何负荷与源身份/拾取映射保留；实例化仅适合重复几何/材料和兼容变换，独立解剖网格并非天然适合；蒙皮优化需先量测 CPU 边界更新、骨矩阵和顶点负荷。上述均为条件评估，不在本轮重构。

GitHub Actions 只跑 headless 结构/数值验证。真实 Windows GPU/桌面 Chrome 基准本地执行，不能把 Actions 软件渲染结果称为 RTX 4060 成绩。最终数字见 `docs/windows/test-results.md`。
