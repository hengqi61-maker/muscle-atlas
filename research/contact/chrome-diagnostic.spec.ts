import {test,expect} from '@playwright/test';
import fs from 'node:fs';
test('record original discovery predicate and await observed readiness',async({page},info)=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');await page.getByRole('button',{name:'高位下拉',exact:true}).click();
 await expect(page.getByText('本地模型加载',{exact:false})).toHaveCount(0);
 const inspect=()=>{
  const canvas=document.querySelector('canvas') as any;
  let fiber=canvas?.[Object.keys(canvas).find(k=>k.startsWith('__reactFiber'))!];
  let stores=0,controls=0,seat=false;
  for(;fiber;fiber=fiber.return)for(let hook=fiber.memoizedState;hook;hook=hook.next){
   const ref=hook.memoizedState?.current;
   if(ref?.camera&&ref?.scene&&ref?.get){stores++;const live=ref.get();
    if(live.controls){controls++;seat ||= !!live.scene.getObjectByName('SeatPad');}
   }
  }
  return {canvas:!!canvas,stores,controls,seat,at:performance.now()};
 };
 const initial=await page.evaluate(inspect);
 await expect.poll(async()=> (await page.evaluate(inspect)).seat,{timeout:10000}).toBe(true);
 const final=await page.evaluate(inspect);
 fs.mkdirSync('artifacts/v2/chrome-diagnostic',{recursive:true});
 fs.writeFileSync(`artifacts/v2/chrome-diagnostic/${info.repeatEachIndex}.json`,JSON.stringify({initial,final,errors},null,2));
 expect(errors).toEqual([]);
});
