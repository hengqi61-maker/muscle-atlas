// Production browser observation; rAF is presentation timing, not GPU elapsed time.
import fs from 'node:fs';
import os from 'node:os';
import crypto from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {chromium} from 'playwright';
const arg=(name,fallback)=>process.argv.includes(name)?process.argv[process.argv.indexOf(name)+1]:fallback;
const out=arg('--out','artifacts/windows/performance.json');
const seconds=Number(arg('--seconds','5')),repeats=Number(arg('--repeats','3'));
if(!Number.isFinite(seconds)||seconds<2||!Number.isInteger(repeats)||repeats<1)throw Error('Require seconds>=2, integer repeats>=1');
const url=arg('--url','http://127.0.0.1:5187');
let server,browser;
const report={schemaVersion:1,commit:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),
  capturedAt:new Date().toISOString(),host:{platform:os.platform(),cpu:os.cpus()[0].model,ram:os.totalmem()},
  viewport:{width:1440,height:1000},seconds,repeats,runs:[],errors:[],warnings:[],
  gpuElapsed_ms:null,limitations:['rAF gaps are not GPU elapsed time','Renderer memory counts are not VRAM bytes','No CPU/GPU bottleneck verdict without controlled perturbation/trace','No physiological or milestone approval']};
try{
  if(!process.argv.includes('--url')){
    try{await fetch(url);throw Error('Benchmark port already occupied');}catch(e){if(e.message==='Benchmark port already occupied')throw e;}
    server=spawn(process.execPath,['node_modules/vite/bin/vite.js','preview','--host','127.0.0.1','--port','5187','--strictPort'],{stdio:'ignore',windowsHide:true});
    let ready=false;
    for(let n=0;n<100;n++){if(server.exitCode!==null)throw Error('Preview server exited');try{const r=await fetch(url);if(r.ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}
    if(!ready)throw Error('Preview not ready');
  }
  browser=await chromium.launch({channel:'chrome',headless:!process.argv.includes('--headed')});
  report.browserVersion=browser.version();
  const system=await browser.newBrowserCDPSession();
  report.gpu=(await system.send('SystemInfo.getInfo')).gpu;
  const context=await browser.newContext({viewport:report.viewport,deviceScaleFactor:1});
  for(let repeat=0;repeat<repeats;repeat++)for(const scenario of ['atlas-paused','curl-playing','pulldown-paused','pulldown-playing']){
    const page=await context.newPage();
    page.on('pageerror',e=>report.errors.push({scenario,message:e.message}));
    page.on('console',m=>{if(['warning','error'].includes(m.type()))report.warnings.push({scenario,type:m.type(),message:m.text(),location:m.location()});});
    page.on('response',r=>{if(r.status()>=400)report.warnings.push({scenario,type:'http',url:r.url(),status:r.status()});});
    await page.goto(url);
    if(scenario!=='atlas-paused'){
      await page.getByRole('button',{name:scenario.startsWith('curl')?'哑铃弯举':'高位下拉',exact:true}).click();
    }
    await page.getByText('本地模型加载',{exact:false}).waitFor({state:'hidden'});
    await page.waitForFunction(()=>{
      const canvas=document.querySelector('canvas');let fiber=canvas[Object.keys(canvas).find(k=>k.startsWith('__reactFiber'))];
      for(;fiber;fiber=fiber.return)for(let h=fiber.memoizedState;h;h=h.next){const r=h.memoizedState?.current;if(r?.get&&r?.camera&&r?.scene&&r.get().gl){window.infraR3F=r.get();return true;}}
      return false;
    });
    if(scenario.endsWith('playing'))await page.getByRole('button',{name:'▶',exact:true}).click();
    await page.waitForTimeout(1500);
    const cdp=await context.newCDPSession(page);await cdp.send('Performance.enable');
    const before=(await cdp.send('Performance.getMetrics')).metrics;
    const stats=await page.evaluate(async(seconds)=>{
      const frames=[],calls=[],triangles=[];let previous=performance.now();const start=previous;
      await new Promise(resolve=>{function frame(now){frames.push(now-previous);previous=now;const i=window.infraR3F.gl.info;calls.push(i.render.calls);triangles.push(i.render.triangles);if(now-start<seconds*1000)requestAnimationFrame(frame);else resolve();}requestAnimationFrame(frame);});
      const sorted=frames.slice(1).sort((a,b)=>a-b),q=p=>sorted[Math.min(sorted.length-1,Math.floor(sorted.length*p))];
      const gl=window.infraR3F.gl.getContext(),debug=gl.getExtension('WEBGL_debug_renderer_info');
      return {elapsed_ms:previous-start,frames:frames.length,fps:frames.length*1000/(previous-start),
        frame_ms:{p50:q(.5),p95:q(.95),p99:q(.99)},drawCalls:{min:Math.min(...calls),max:Math.max(...calls)},triangles:{min:Math.min(...triangles),max:Math.max(...triangles)},
        rendererMemory:window.infraR3F.gl.info.memory,canvas:{width:gl.drawingBufferWidth,height:gl.drawingBufferHeight,pixelRatio:window.infraR3F.gl.getPixelRatio()},camera:{position:window.infraR3F.camera.position.toArray(),fov:window.infraR3F.camera.fov,target:window.infraR3F.controls?.target.toArray()},jsHeap:performance.memory?{used:performance.memory.usedJSHeapSize,total:performance.memory.totalJSHeapSize,limit:performance.memory.jsHeapSizeLimit}:null,
        webglRenderer:debug?gl.getParameter(debug.UNMASKED_RENDERER_WEBGL):null,
        resources:performance.getEntriesByType('resource').filter(r=>r.name.includes('.glb')||r.name.endsWith('.js')).map(r=>({name:r.name,duration_ms:r.duration,transferSize:r.transferSize,decodedBodySize:r.decodedBodySize}))};
    },seconds);
    const after=(await cdp.send('Performance.getMetrics')).metrics;
    const metric=(rows,key)=>rows.find(r=>r.name===key)?.value;
    stats.mainThreadTaskTime_s=metric(after,'TaskDuration')-metric(before,'TaskDuration');
    report.runs.push({scenario,repeat,...stats});
    console.log(`${scenario} repeat ${repeat+1}: ${stats.fps.toFixed(1)} rAF/s, p95 ${stats.frame_ms.p95.toFixed(1)}ms`);
    await page.close();
  }
  report.assetHashes=Object.fromEntries(['anatomy.glb','anatomy-curl.glb','anatomy-pulldown.glb'].map(n=>[n,crypto.createHash('sha256').update(fs.readFileSync('public/models/'+n)).digest('hex')]));
}finally{
  if(browser)await browser.close();
  if(server)server.kill();
  fs.mkdirSync('artifacts/windows',{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2));
}
if(report.errors.length)process.exitCode=1;
