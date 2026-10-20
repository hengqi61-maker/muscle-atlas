/** Metric machine-space segments copied from LatPulldownMachine, not anatomical frames. */
export function officialBarTargets(config,progress,handReferenceX){
 const p=Math.max(0,Math.min(1,progress)),phase=(1-Math.cos(2*Math.PI*p))/2,barY=config.barTopY-config.barTravel*phase;
 if(!(handReferenceX.Left>0&&handReferenceX.Right<0))throw Error('Unverified canonical hand sidedness');
 return Object.fromEntries(['Left','Right'].map(side=>{const sign=Math.sign(handReferenceX[side]);const from=[sign*.32,barY-.01575,config.gripZ],to=[sign*.46,barY-.126,config.gripZ];const raw=[sign*config.gripHalfWidth,barY-config.gripDrop,config.gripZ],v=to.map((x,i)=>x-from[i]),length2=v.reduce((s,x)=>s+x*x,0);const t=raw.reduce((s,x,i)=>s+(x-from[i])*v[i],0)/length2;
 if(t<0||t>1)throw Error('Configured target outside grip');
 return [side,{machineSide:sign>0?'positive-x':'negative-x',from,to,target:from.map((x,i)=>x+t*v[i]),configuredTarget:raw,radius:.024,radialSegments:12,coordinateSpace:'shared local machine/glTF metric frame; not seated-anatomy registration'}];}));
}
