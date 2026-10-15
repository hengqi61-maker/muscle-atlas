export const DURATION=4;
export function elbowAngle(time:number){return -(0.15+(1-Math.cos(time/DURATION*Math.PI*2))/2*1.9);}
export function advance(time:number,delta:number,speed:number,loop:boolean){const next=time+delta*speed;return loop?next%DURATION:Math.min(next,DURATION);}

/** Resume a paused clip, or restart a completed repetition at its beginning. */
export function togglePlayback(time:number,playing:boolean){return {time:!playing&&time>=DURATION?0:time,playing:!playing};}
