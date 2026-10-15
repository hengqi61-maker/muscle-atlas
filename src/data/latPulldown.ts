import {catalogue} from './catalogue';
import type {Exercise,Role} from '../types/domain';
/** Only source-verified anatomy IDs are included. This is a qualitative role map, not EMG or force. */
const anatomicalRoles: Array<{pattern:RegExp;role:Role}> = [
  {pattern:/latissimus dorsi/i,role:'primary'},
  {pattern:/teres major/i,role:'secondary'},
  {pattern:/biceps brachii|brachialis/i,role:'secondary'},
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
 animation:'equipment-only',source:'器械运动验证。人体解剖模型仍为静态，尚无骨骼蒙皮和手部 IK；肌群参与为定性关联。'
};
