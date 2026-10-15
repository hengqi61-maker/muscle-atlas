import {test,expect} from '@playwright/test';
test('real model, joint playback, selection and persistence',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');await expect(page.locator('canvas')).toBeVisible();
 await page.waitForResponse(r=>r.url().endsWith('anatomy.glb')&&r.status()===200);await page.waitForTimeout(2000);
 await page.screenshot({path:'docs/anatomy-browser.png'});
 const canvas=page.locator('canvas');const box=(await canvas.boundingBox())!;await page.mouse.click(box.x+box.width*.49,box.y+box.height*.28);await expect(page.getByText('来源：bp3d',{exact:false})).toBeVisible();
 await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(box.x+box.width/2+50,box.y+box.height/2+10);await page.mouse.up();await page.mouse.wheel(0,-100);await page.getByRole('button',{name:'视角复位'}).click();
 await page.getByRole('button',{name:'Real Anatomy',exact:true}).click();
 await page.getByRole('button',{name:'动作实验室',exact:true}).click();
 const initialPose=await page.locator('canvas').screenshot();await page.getByRole('button',{name:'▶',exact:true}).click();await page.waitForTimeout(600);await page.getByRole('button',{name:'Ⅱ',exact:true}).click();
 const movedPose=await page.locator('canvas').screenshot();expect(initialPose.equals(movedPose)).toBe(false);
 const progress=page.getByRole('slider',{name:'动画进度'});expect(Number(await progress.inputValue())).toBeGreaterThan(.2);
 const frozen=await progress.inputValue();await page.waitForTimeout(250);expect(await progress.inputValue()).toBe(frozen);
 await page.getByRole('button',{name:'肱二头肌 Biceps brachii'}).click();await expect(page.getByRole('heading',{name:'肱二头肌'})).toBeVisible();
 await page.getByRole('button',{name:'Clean Tech',exact:true}).click();await page.screenshot({path:'docs/prototype-browser.png'});
 await page.getByRole('button',{name:'训练记录',exact:true}).click();await page.getByRole('button',{name:'记录完成一组'}).click();await expect(page.getByRole('status')).toHaveText('已保存 1 组实际完成记录');
 await page.reload();await page.getByRole('button',{name:'训练记录',exact:true}).click();await expect(page.getByText('1 组完成',{exact:true})).toBeVisible();expect(errors).toEqual([]);
});
