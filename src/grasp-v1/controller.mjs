/** Reusable grasp-controller v1. Applies local Euler heuristics to named bones. */
export const DIGITS = ['Thumb','Index','Middle','Ring','Little'];
export const CHAIN = {
  Thumb:['CMC','MCP','IP'],
  Index:['MCP','PIP','DIP'],
  Middle:['MCP','PIP','DIP'],
  Ring:['MCP','PIP','DIP'],
  Little:['MCP','PIP','DIP'],
};
export const FLEX = {CMC:0.35,MCP:1.15,PIP:1.25,DIP:0.85,IP:1.05};
export const THUMB_CMC_OPP = 0.55;
export const PRESETS = {
  open:{curl:0,thumb:0,spread:0.25},
  half:{curl:0.45,thumb:0.35,spread:0.12},
  closed:{curl:1,thumb:0.85,spread:0},
  'pulldown-bar':{curl:0.72,thumb:0.62,spread:0.06},
  'rope-end':{curl:0.88,thumb:0.78,spread:0.02},
};
export function boneName(side,digit,joint){return `${side}${digit}${joint}`;}
export function poseFor(preset, side='Left'){
  const p = PRESETS[preset];
  if(!p) throw new Error('unknown preset '+preset);
  const sign = side==='Left'?1:-1;
  const out = {};
  DIGITS.forEach((digit,di)=>{
    const spread=(di-2)*0.12*p.spread;
    const curl = digit==='Thumb'?p.thumb:p.curl;
    CHAIN[digit].forEach(joint=>{
      const flex=FLEX[joint]*curl;
      const opp=(digit==='Thumb'&&joint==='CMC')?THUMB_CMC_OPP*p.thumb:0;
      out[boneName(side,digit,joint)]={x:flex,y:opp*sign,z:spread*sign};
    });
  });
  return out;
}
export function lerpPose(a,b,t){
  const out={};
  for(const k of new Set([...Object.keys(a),...Object.keys(b)])){
    const A=a[k]||{x:0,y:0,z:0}; const B=b[k]||{x:0,y:0,z:0};
    out[k]={x:A.x+(B.x-A.x)*t,y:A.y+(B.y-A.y)*t,z:A.z+(B.z-A.z)*t};
  }
  return out;
}
export function applyToObject3D(root, pose){
  let hit=0;
  root.traverse(o=>{
    if(pose[o.name] && o.isBone){
      const e=pose[o.name];
      o.rotation.set(e.x,e.y,e.z);
      hit++;
    }
  });
  return hit;
}
