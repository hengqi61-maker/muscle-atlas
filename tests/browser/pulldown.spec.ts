import {test,expect} from '@playwright/test';
test('seated anatomy and lat machine share timeline and survive exercise switches',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/');
 const loaded=page.waitForResponse(r=>r.url().endsWith('anatomy-pulldown.glb')&&r.status()===200);
 await page.getByRole('button',{name:'高位下拉',exact:true}).click();await loaded;await expect(page.getByText('本地模型加载',{exact:false})).toHaveCount(0);await page.waitForTimeout(300);
 await expect(page.getByText('SEATED LAT PULLDOWN · 坐姿联动')).toBeVisible();
 const slider=page.getByRole('slider',{name:'动画进度'});
 for(const time of [0,1,2,3,4]){await slider.fill(String(time));await page.waitForTimeout(100);await page.screenshot({path:`docs/evidence/pulldown-${time}.png`});if(time===2)await page.locator('canvas').screenshot({path:'docs/evidence/pulldown-contact.png'});}
 await slider.fill('0');const start=await page.locator('canvas').screenshot();await page.getByRole('button',{name:'▶',exact:true}).click();await page.waitForTimeout(500);await page.getByRole('button',{name:'Ⅱ',exact:true}).click();expect(start.equals(await page.locator('canvas').screenshot())).toBe(false);
 const frozen=await slider.inputValue();await page.waitForTimeout(150);expect(await slider.inputValue()).toBe(frozen);
 await page.getByRole('button',{name:'哑铃弯举',exact:true}).click();await expect(page.getByRole('button',{name:'90°',exact:true})).toBeVisible();await page.getByRole('button',{name:'90°',exact:true}).click();
 await page.getByLabel('握持表面层').uncheck();await page.getByLabel('握持表面层').check();await page.getByRole('button',{name:'握持近景',exact:true}).click();await page.waitForTimeout(150);await page.screenshot({path:'docs/evidence/grip-upgrade.png'});await page.locator('canvas').screenshot({path:'docs/evidence/grip-closeup.png'});
 await page.getByRole('button',{name:'高位下拉',exact:true}).click();await expect(page.getByText('SEATED LAT PULLDOWN · 坐姿联动')).toBeVisible();expect(errors).toEqual([]);
});
