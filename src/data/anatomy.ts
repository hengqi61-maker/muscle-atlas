import type {AnatomicalMuscle,Exercise} from '../types/domain';
export const muscles:AnatomicalMuscle[]=[
{id:'biceps',name:'肱二头肌',english:'Biceps brachii',group:'上肢',region:'upper-arm',layer:'superficial'},
{id:'triceps',name:'肱三头肌',english:'Triceps brachii',group:'上肢',region:'upper-arm',layer:'superficial'},
{id:'deltoid',name:'三角肌',english:'Deltoid',group:'肩部',region:'shoulder',layer:'superficial'},
{id:'pectoralis',name:'胸大肌',english:'Pectoralis major',group:'胸部',region:'chest',layer:'superficial'},
{id:'abs',name:'腹直肌',english:'Rectus abdominis',group:'核心',region:'abdomen',layer:'superficial'},
{id:'quadriceps',name:'股四头肌',english:'Quadriceps group',group:'下肢',region:'thigh',layer:'superficial'},
{id:'forearm',name:'前臂肌群',english:'Forearm group',group:'上肢',region:'forearm',layer:'superficial'}];
export const curl:Exercise={id:'dumbbell-curl',name:'哑铃弯举',english:'Dumbbell Biceps Curl',equipment:'哑铃',relations:[{muscleId:'biceps',role:'primary'},{muscleId:'forearm',role:'secondary'},{muscleId:'deltoid',role:'stabilizer'}],instructions:['上臂保持靠近躯干，控制肘关节屈伸。','平稳抬起与放下，避免躯干摆动。'],errors:['摆动身体借力','肩部前移过多'],animation:'prototype-curl',source:'技术演示；参与角色为定性分类，非激活强度测量'};
