import {test,expect} from '@playwright/test';
import config from '../../src/data/pulldown-config.json' with {type:'json'};

test('production support solids retain configured fit and remain visible in inspection views',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');await page.getByRole('button',{name:'高位下拉',exact:true}).click();
 await expect(page.getByText('本地模型加载',{exact:false})).toHaveCount(0);
 await page.evaluate(()=>{
  const canvas=document.querySelector('canvas')! as HTMLCanvasElement&Record<string,any>;
  let fiber=canvas[Object.keys(canvas).find(k=>k.startsWith('__reactFiber'))!];
  for(;fiber;fiber=fiber.return)for(let hook=fiber.memoizedState;hook;hook=hook.next){
   const ref=hook.memoizedState?.current;if(ref?.camera&&ref?.scene&&ref?.get){const live=ref.get();if(live.controls){(window as any).supportScene=live;return;}}
  }
  throw Error('Production scene missing');
 });
 await expect.poll(()=>page.evaluate(()=>!!(window as any).supportScene.scene.getObjectByName('SeatPad'))).toBe(true);
 for(const time of [0,1.13,2,3.47,4]){
  await page.getByRole('slider',{name:'动画进度'}).fill(String(time));await page.waitForTimeout(100);
  const result=await page.evaluate(cfg=>{
   const state=(window as any).supportScene,scene=state.scene;
   const boxSpecs=[['SeatPad',cfg.supports.seat],['ThighPad',cfg.supports.thighPad],['SeatPedestal',cfg.supports.pedestal],['FootPlatform',cfg.supports.footPlatform]] as const;
   const beamSpecs:Array<readonly [string,{from:number[];to:number[];radius:number}]>=[['ThighRestraintCrossbar',cfg.supports.crossbar],...cfg.supports.brackets.map(b=>[`ThighRestraintBracket${b.name}`,b] as const)];
   const solids:any[]=[];const issues:string[]=[];
   for(const [name,spec] of boxSpecs){
    const mesh=scene.getObjectByName(name),p=mesh.geometry.parameters;
    if(JSON.stringify(mesh.position.toArray())!==JSON.stringify(spec.position)||[p.width,p.height,p.depth].some((v:number,i:number)=>Math.abs(v-spec.size[i])>1e-7))issues.push(`Config mismatch ${name}`);
    solids.push(mesh);
   }
   for(const [name,spec] of beamSpecs){
    const mesh=scene.getObjectByName(name),p=mesh.geometry.parameters;
    const length=Math.hypot(...spec.from.map((v:number,i:number)=>spec.to[i]-v));
    const start=mesh.position.clone().set(0,-p.height/2,0).applyQuaternion(mesh.quaternion).add(mesh.position);
    const end=mesh.position.clone().set(0,p.height/2,0).applyQuaternion(mesh.quaternion).add(mesh.position);
    if(Math.abs(p.height-length)>1e-7||Math.abs(p.radiusTop-spec.radius)>1e-7||start.distanceTo(start.clone().fromArray(spec.from))>1e-7||end.distanceTo(end.clone().fromArray(spec.to))>1e-7)issues.push(`Config mismatch ${name}`);
    // Each restraint reaches the seat support and the crossbar, rather than floating.
    if(name.startsWith('ThighRestraintBracket')){
     const seat=scene.getObjectByName('SeatPad'),crossbar=scene.getObjectByName('ThighRestraintCrossbar');
     const anchor=seat.worldToLocal(mesh.parent.localToWorld(start.clone()));const half=seat.geometry.parameters;
     const distance=Math.hypot(Math.max(Math.abs(anchor.x)-half.width/2,0),Math.max(Math.abs(anchor.y)-half.height/2,0),Math.max(Math.abs(anchor.z)-half.depth/2,0));
     const top=crossbar.worldToLocal(mesh.parent.localToWorld(end.clone()));const bar=crossbar.geometry.parameters;
     if(distance>p.radiusTop+1e-6||Math.abs(top.y)>bar.height/2+p.radiusTop||Math.hypot(top.x,top.z)>bar.radiusTop+p.radiusTop)issues.push(`Disconnected restraint ${name}`);
    }
    solids.push(mesh);
   }
   const seat=scene.getObjectByName('SeatPad'),pedestal=scene.getObjectByName('SeatPedestal');
   const seatBottom=seat.position.y-seat.geometry.parameters.height/2,pedestalTop=pedestal.position.y+pedestal.geometry.parameters.height/2;
   if(Math.abs(seatBottom-pedestalTop)>1e-5)issues.push('Seat disconnected from pedestal');
   // Convex planes come from the actual rendered box/cylinder triangles.
   const checks=solids.map(mesh=>{
    mesh.geometry.computeBoundingBox();const position=mesh.geometry.attributes.position,index=mesh.geometry.index,planes:any[]=[];
    const vertex=(i:number)=>mesh.position.clone().fromBufferAttribute(position,i);
    for(let i=0;i<index.count;i+=3){const a=vertex(index.getX(i)),b=vertex(index.getX(i+1)),c=vertex(index.getX(i+2));const normal=b.clone().sub(a).cross(c.clone().sub(a)).normalize();planes.push({normal,constant:-normal.dot(a)});}
    return {mesh,inverse:mesh.matrixWorld.clone().invert(),planes,interiorVertices:0,maxDepth:0};
   });
   const sources:any[]=[];scene.traverse((mesh:any)=>{if(mesh.isSkinnedMesh&&mesh.userData.entry)sources.push(mesh);});
   for(const source of sources)for(let i=0;i<source.geometry.attributes.position.count;i++){
    const world=source.localToWorld(source.getVertexPosition(i,source.position.clone()));
    for(const check of checks){const point=world.clone().applyMatrix4(check.inverse);if(!check.mesh.geometry.boundingBox.containsPoint(point))continue;let signed=-Infinity;
     for(const plane of check.planes){signed=Math.max(signed,plane.normal.dot(point)+plane.constant);if(signed>0)break;}
     if(signed< -1e-5){check.interiorVertices++;check.maxDepth=Math.max(check.maxDepth,-signed);}
    }
   }
   // Clip named actual source triangles to the actual pad footprint, then measure support gap.
   const regionGap=(name:string,names:string[],seat:boolean)=>{
    const solid=scene.getObjectByName(name),params=solid.geometry.parameters,inverse=solid.matrixWorld.clone().invert();let gap=Infinity,triangles=0;
    for(const source of sources.filter(m=>names.includes(m.userData.entry.name))){
     const index=source.geometry.index,position=source.geometry.attributes.position;
     const vertex=(i:number)=>source.localToWorld(source.getVertexPosition(i,source.position.clone())).applyMatrix4(inverse);
     for(let i=0;i<(index?.count??position.count);i+=3){let polygon=[0,1,2].map(j=>vertex(index?index.getX(i+j):i+j));
      for(const [axis,sign,limit] of [['x',1,params.width/2],['x',-1,params.width/2],['z',1,params.depth/2],['z',-1,params.depth/2]] as const){
       const output:any[]=[];for(let j=0;j<polygon.length;j++){const a=polygon[j],b=polygon[(j+1)%polygon.length],da=sign*a[axis]-limit,db=sign*b[axis]-limit;if(da<=0)output.push(a);if((da<=0)!==(db<=0))output.push(a.clone().lerp(b,da/(da-db)));}polygon=output;
      }
      if(polygon.length){triangles++;for(const p of polygon)gap=Math.min(gap,seat?p.y-params.height/2:-params.height/2-p.y);}
     }
    }
    return {gap,triangles};
   };
   return {issues,sourceCount:sources.length,solids:checks.map(c=>({name:c.mesh.name,count:c.interiorVertices,depth:c.maxDepth})),seat:regionGap('SeatPad',cfg.supportContactRegions.seatSourceNames,true),thigh:regionGap('ThighPad',cfg.supportContactRegions.thighSourceNames,false)};
  },config);
  expect(result.issues).toEqual([]);expect(result.sourceCount).toBe(467);
  for(const solid of result.solids)expect(solid.count,`${solid.name} penetration ${solid.depth}m`).toBe(0);
  // Distances are in support-local model metres after undoing the scene scale.
  for(const region of [result.seat,result.thigh]){expect(region.triangles).toBeGreaterThan(0);expect(region.gap).toBeGreaterThanOrEqual(-1e-5);expect(region.gap).toBeLessThan(.001);}
 }
 for(const view of ['背面观察','侧面观察','全身视角']){
  await page.getByRole('button',{name:view,exact:true}).click();
  const visible=await page.evaluate(()=>{const scene=(window as any).supportScene.scene;return ['SeatPad','ThighPad','SeatPedestal','ThighRestraintCrossbar','ThighRestraintBracketLeft','ThighRestraintBracketRight','FootPlatform'].every(name=>{let node=scene.getObjectByName(name);for(;node;node=node.parent)if(!node.visible)return false;return true;});});
  expect(visible).toBe(true);
 }
 // Match evidence capture presets and ensure actual source anatomy stays in frame.
 for(const time of [0,2,4]){
  await page.getByRole('slider',{name:'动画进度'}).fill(String(time));await page.waitForTimeout(100);
  for(const view of ['front','side','back']){
   const projection=await page.evaluate(view=>{
    const state=(window as any).supportScene,c=state.controls;
    c.object.position.set(...(view==='front'?[0,1,5.2]:view==='side'?[5.2,1,.1]:[0,1,-5.2]));c.target.set(0,0,.1);c.update();state.camera.updateMatrixWorld(true);
    let maxX=0,maxY=0,count=0;state.scene.traverse((mesh:any)=>{if(!mesh.isSkinnedMesh||!mesh.userData.entry)return;for(let i=0;i<mesh.geometry.attributes.position.count;i++){const p=mesh.localToWorld(mesh.getVertexPosition(i,mesh.position.clone())).project(state.camera);maxX=Math.max(maxX,Math.abs(p.x));maxY=Math.max(maxY,Math.abs(p.y));count++;}});
    return {maxX,maxY,count};
   },view);
   expect(projection.count).toBeGreaterThan(100000);expect(projection.maxX).toBeLessThan(.98);expect(projection.maxY).toBeLessThan(.98);
  }
 }
 expect(errors).toEqual([]);
});
