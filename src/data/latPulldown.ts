import {catalogue} from './catalogue';
import type {Exercise,Role} from '../types/domain';
/** Only source-verified anatomy IDs are included. This is a qualitative role map, not EMG or force. */
const anatomicalRoles: Array<{pattern:RegExp;role:Role}> = [
  {pattern:/latissimus dorsi/i,role:'primary'},
  {pattern:/teres major/i,role:'secondary'},
  {pattern:/biceps brachii|(?:^| )brachialis\b/i,role:'secondary'},
  {pattern:/rhomboid|transverse part of .*trapezius|ascending part of .*trapezius/i,role:'stabilizer'}
];
export const latPulldownAnatomyRelations = catalogue.flatMap(entry=>{
 if(entry.isTendon)return [];
 const found=anatomicalRoles.find(item=>item.pattern.test(entry.originalName));
 return found?[{anatomyId:entry.anatomyId,role:found.role}]:[];
});
export const latPulldown:Exercise={
 id:'lat-pulldown',name:'坐姿高位下拉',english:'Seated Lat Pulldown',
 equipment:'高位滑轮训练器',relations:[],
 instructions:['坐稳并固定大腿，胸椎自然伸展。','从头顶将横杆拉向上胸，肘部朝下，避免明显后仰。','控制回程，手臂逐渐伸展。'],
 errors:['横杆绕到颈后','利用腰背大幅后仰借力'],
 animation:'anatomy-pulldown',source:'真实解剖坐姿蒙皮与双臂 IK 烘焙；握点共用器械时间轴。肩胛带与软组织为未标定运动示意，手部沿用原始网格，肌群角色不代表实测激活。'
};
