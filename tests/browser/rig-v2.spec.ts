import {test,expect} from '@playwright/test';
test('isolated V2 R1 loads original identities and actual embedded clips',async({page})=>{
  const errors:string[]=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/rig-v2.html');
  await expect(page.getByRole('heading',{name:'V2 · R1 experimental'})).toBeVisible();
  await expect(page.getByTestId('identity-count')).toHaveText('467',{timeout:120000});
  const selector=page.getByLabel('Animation',{exact:true});
  const names=await selector.locator('option').allTextContents();
  expect(names.length).toBeGreaterThanOrEqual(3);
  for(let index=1;index<Math.min(names.length,4);index++){
    await selector.selectOption({index});
    await page.getByLabel('Seek',{exact:true}).fill('0.5');
    await expect(page.getByTestId('clip-time')).toContainText('0.500');
    await page.getByRole('button',{name:'Play',exact:true}).click();
    await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible();
    await page.waitForTimeout(180);
    await page.getByRole('button',{name:'Pause',exact:true}).click();
    const paused=await page.getByTestId('clip-time').textContent();
    await page.waitForTimeout(120);
    await expect(page.getByTestId('clip-time')).toHaveText(paused!);
  }
  await page.getByRole('button',{name:'Real',exact:true}).click();
  await expect(page.getByRole('button',{name:'Real',exact:true})).toHaveAttribute('aria-pressed','true');
  await page.getByRole('button',{name:'Clean',exact:true}).click();
  const canvas=page.locator('canvas');
  const box=await canvas.boundingBox();
  expect(box).not.toBeNull();
  // Probe the visible torso/limbs through real canvas raycasting, not the catalogue.
  for(const [x,y] of [[.5,.4],[.47,.5],[.53,.5],[.5,.6],[.44,.3],[.56,.3]]){
    await canvas.click({position:{x:box!.width*x,y:box!.height*y}});
    if((await page.getByTestId('picked-muscle').textContent())?.includes('Stable ID:'))break;
  }
  await expect(page.getByTestId('picked-muscle')).toContainText('Stable ID:');
  await page.getByRole('button',{name:'Rest',exact:true}).click();
  await expect(selector).toHaveValue('');
  expect(errors).toEqual([]);
});

test('production R1 evidence: actual clip keyframes in front, side and back',async({page},testInfo)=>{
  await page.goto('/rig-v2.html');
  await expect(page.getByTestId('identity-count')).toHaveText('467',{timeout:120000});
  const selector=page.getByLabel('Animation',{exact:true});
  const names=await selector.locator('option').allTextContents();
  for(let index=1;index<names.length;index++){
    await selector.selectOption({index});
    const duration=Number((await page.getByLabel('Seek',{exact:true}).getAttribute('max')));
    for(const fraction of [0,.25,.5,.75,1]){
      await page.getByLabel('Seek',{exact:true}).fill(String(duration*fraction));
      if(fraction===.5){
        const escaped=await page.evaluate(()=>{
          let count=0;
          window.__rigV2!.scene.traverse(o=>{if('isSkinnedMesh' in o){const m=o as import('three').SkinnedMesh;const point=m.position.clone();for(let i=0;i<m.geometry.getAttribute('position').count;i++){m.getVertexPosition(i,point);if(!m.boundingBox!.containsPoint(point)||!m.boundingSphere!.containsPoint(point))count++;}}});
          return count;
        });
        expect(escaped).toBe(0);
      }
      for(const view of ['Front','Side','Back']){
        await page.getByRole('button',{name:view,exact:true}).click();
        await page.waitForTimeout(80);
        const name=`${names[index]}-${String(fraction).replace('.','_')}-${view}`;
        await page.screenshot({path:testInfo.outputPath(`${name}.png`)});
      }
    }
    const audit=await page.evaluate(()=>{
      const scene=window.__rigV2!.scene;
      const ids:string[]=[];let skins=0,unculled=0,badBounds=0;
      scene.traverse(o=>{if('isSkinnedMesh' in o){const m=o as import('three').SkinnedMesh;skins++;if(!m.frustumCulled)unculled++;if(!m.boundingBox||!m.boundingSphere||m.boundingBox.isEmpty()||!Number.isFinite(m.boundingSphere.radius))badBounds++;}if(o.userData.sourceName)ids.push(o.userData.sourceName);});
      return {skins,unculled,badBounds,unique:new Set(ids).size};
    });
    expect(audit).toEqual({skins:467,unculled:0,badBounds:0,unique:467});
    await page.getByRole('button',{name:'Front',exact:true}).click();
    await page.getByLabel('Seek',{exact:true}).fill('0');
    await page.getByRole('button',{name:'Play',exact:true}).click();
    await page.waitForTimeout(Math.min(duration*1000+100,9000));
    await page.getByRole('button',{name:'Pause',exact:true}).click();
  }
});

test('non-loop completion re-arms actual clips for replay and seeking',async({page})=>{
  await page.goto('/rig-v2.html');
  await expect(page.getByTestId('identity-count')).toHaveText('467',{timeout:120000});
  await page.getByLabel('Loop',{exact:true}).uncheck();
  for(const clip of ['CurlProbe','PulldownProbe']){
    await page.getByLabel('Animation',{exact:true}).selectOption(clip);
    const seek=page.getByLabel('Seek',{exact:true});
    const duration=Number(await seek.getAttribute('max'));
    await seek.fill(String(duration-.01));
    await page.getByRole('button',{name:'Play',exact:true}).click();
    await expect(page.getByRole('button',{name:'Play',exact:true})).toBeVisible();
    await expect(page.getByTestId('clip-time')).toHaveText(`${duration.toFixed(3)} / ${duration.toFixed(3)} s`);
    await page.getByRole('button',{name:'Play',exact:true}).click();
    await expect.poll(async()=>Number((await page.getByTestId('clip-time').textContent())!.split(' / ')[0])).toBeGreaterThan(0);
    await page.getByRole('button',{name:'Pause',exact:true}).click();
    const replayTime=Number((await page.getByTestId('clip-time').textContent())!.split(' / ')[0]);
    expect(replayTime).toBeLessThan(duration-.01);
    await seek.fill('1');
    await expect(page.getByTestId('clip-time')).toContainText('1.000 /');
    await page.getByRole('button',{name:'Play',exact:true}).click();
    await expect.poll(async()=>Number((await page.getByTestId('clip-time').textContent())!.split(' / ')[0])).toBeGreaterThan(1);
    await page.getByRole('button',{name:'Pause',exact:true}).click();
  }
});
