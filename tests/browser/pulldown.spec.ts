import {test,expect} from '@playwright/test';
test('lat pulldown equipment follows shared player without claiming body rig',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');
 await page.getByRole('button',{name:'高位下拉',exact:true}).click();
 await expect(page.getByText('仅器械运动：真实人体的坐姿骨骼绑定尚未完成')).toBeVisible();
 await expect(page.getByText('人体待绑定',{exact:false}).last()).toBeVisible();
 const initial=await page.locator('canvas').screenshot();
 await page.getByRole('button',{name:'▶',exact:true}).click();
 await page.waitForTimeout(650);
 await page.getByRole('button',{name:'Ⅱ',exact:true}).click();
 const next=await page.locator('canvas').screenshot();
 expect(initial.equals(next)).toBe(false);
 const progress=page.getByRole('slider',{name:'动画进度'});
 expect(Number(await progress.inputValue())).toBeGreaterThan(0);
 const stopped=await progress.inputValue();await page.waitForTimeout(200);
 expect(await progress.inputValue()).toBe(stopped);
 expect(errors).toEqual([]);
});
