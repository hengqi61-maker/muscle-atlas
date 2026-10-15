import {test,expect} from '@playwright/test';

test('finished non-loop playback restarts and paused source picking survives nonmonotonic seeks',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');await page.getByRole('button',{name:'高位下拉',exact:true}).click();
 await expect(page.getByText('本地模型加载',{exact:false})).toHaveCount(0);
 const slider=page.getByRole('slider',{name:'动画进度'});
 await page.getByRole('button',{name:'循环',exact:true}).click();
 await slider.fill('3.95');await page.getByRole('button',{name:'▶',exact:true}).click();
 await expect(page.getByRole('button',{name:'▶',exact:true})).toBeVisible();await expect(slider).toHaveValue('4');
 await page.getByRole('button',{name:'▶',exact:true}).click();
 await expect.poll(async()=>Number(await slider.inputValue())).toBeGreaterThan(0);
 expect(Number(await slider.inputValue())).toBeLessThan(4);
 await page.getByRole('button',{name:'Ⅱ',exact:true}).click();
 const frozen=await slider.inputValue();await page.waitForTimeout(150);await expect(slider).toHaveValue(frozen);
 await page.getByRole('button',{name:'背面观察',exact:true}).click();
 // Read the actual production scene through React/Fiber; no test-only application hook.
 await page.evaluate(()=>{
  const canvas=document.querySelector('canvas')! as HTMLCanvasElement&Record<string,any>;
  let fiber=canvas[Object.keys(canvas).find(k=>k.startsWith('__reactFiber'))!];
  for(;fiber;fiber=fiber.return)for(let hook=fiber.memoizedState;hook;hook=hook.next){
   const ref=hook.memoizedState?.current;if(ref?.camera&&ref?.scene&&ref?.get){const live=ref.get();if(live.controls){(window as any).runtimeScene=live;return;}}
  }
  throw Error('Production R3F scene missing');
 });
 for(const [index,time] of [0,2,4,.37,1.13,3.47,1,3,0].entries()){
  await page.getByRole('button',{name:index%2===0?'Clean Tech':'Real Anatomy',exact:true}).click();
  await slider.fill(String(time));await page.waitForTimeout(120);
  const result=await page.evaluate(()=>{
   const s=(window as any).runtimeScene,m=s.scene.getObjectByName('left_latissimus_dorsi');
   const point=s.camera.position.clone().set(0,0,0);let n=0,maxOutside=-Infinity,sourceMeshes=0,checkedVertices=0;const morphIds:string[]=[];
   s.scene.traverse((mesh:any)=>{if(!mesh.isSkinnedMesh||!mesh.userData.entry)return;sourceMeshes++;if(mesh.geometry.morphAttributes.position?.length)morphIds.push(mesh.userData.entry.bpId);
    for(let i=0;i<mesh.geometry.attributes.position.count;i++){
     const vertex=mesh.getVertexPosition(i,s.camera.position.clone().set(0,0,0));checkedVertices++;
     maxOutside=Math.max(maxOutside,vertex.distanceTo(mesh.boundingSphere.center)-mesh.boundingSphere.radius);
     if(!mesh.boundingBox.containsPoint(vertex))throw Error(`Current skin box misses ${mesh.name} vertex ${i}`);
    }
   });
   for(let i=0;i<m.geometry.attributes.position.count;i++){
    const vertex=m.getVertexPosition(i,s.camera.position.clone().set(0,0,0));
    maxOutside=Math.max(maxOutside,vertex.distanceTo(m.boundingSphere.center)-m.boundingSphere.radius);
    if(i%20===0){point.add(m.localToWorld(vertex));n++;}
   }
   point.divideScalar(n).project(s.camera);const rect=s.gl.domElement.getBoundingClientRect();
   return {maxOutside,sourceMeshes,checkedVertices,morphIds:morphIds.sort(),x:rect.x+(point.x+1)*rect.width/2,y:rect.y+(1-point.y)*rect.height/2};
  });
  expect(result.sourceMeshes).toBe(467);expect(result.morphIds).toEqual(['BP8965','BP7781','BP8214','BP8376','BP9197','BP4797','BP4839','BP4795','BP4791','BP4793'].sort());expect(result.checkedVertices).toBeGreaterThan(100000);
  expect(result.maxOutside).toBeLessThan(1e-5);
  await page.mouse.click(result.x,result.y);
  await expect(page.locator('aside.right')).toContainText('z-anatomy:unmapped:left_latissimus_dorsi');
 }
 await page.getByRole('button',{name:'Real Anatomy',exact:true}).click();
 await expect(page.locator('aside.right')).toContainText('z-anatomy:unmapped:left_latissimus_dorsi');
 // Slow playback crosses the endpoint and continues rather than stopping.
 await page.getByRole('button',{name:'循环',exact:true}).click();
 await page.getByLabel('播放速度').selectOption('0.25');await slider.fill('3.95');
 await page.getByRole('button',{name:'▶',exact:true}).click();
 await expect.poll(async()=>Number(await slider.inputValue())).toBeLessThan(1);
 await expect(page.getByRole('button',{name:'Ⅱ',exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Ⅱ',exact:true}).click();
 const wrapped=await slider.inputValue();await page.waitForTimeout(150);await expect(slider).toHaveValue(wrapped);
 // Exercise remount restores the requested clock and source model, then remains seekable.
 await page.getByRole('button',{name:'哑铃弯举',exact:true}).click();
 await expect(page.getByRole('button',{name:'90°',exact:true})).toBeVisible();
 await page.getByRole('button',{name:'90°',exact:true}).click();
 await expect.poll(async()=>Number(await slider.inputValue())).toBeCloseTo(4/3);
 await page.getByRole('button',{name:'高位下拉',exact:true}).click();
 await expect(slider).toHaveValue('0');await expect(page.getByRole('button',{name:'▶',exact:true})).toBeVisible();
 await slider.fill('2');await page.waitForTimeout(150);
 const restored=await page.evaluate(()=>{
  const scene=(window as any).runtimeScene.scene;let sources=0;scene.traverse((o:any)=>{if(o.isSkinnedMesh&&o.userData.entry)sources++;});
  return {sources,hasMachine:!!scene.getObjectByName('MovingLatBar')};
 });
 expect(restored).toEqual({sources:467,hasMachine:true});
 expect(errors).toEqual([]);
});
