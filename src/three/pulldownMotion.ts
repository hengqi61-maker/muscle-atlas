import config from '../data/pulldown-config.json';
/** One shared metric timeline, consumed by machine and offline baked human IK. */
export function latPulldownPhase(progress:number){const p=Number.isFinite(progress)?Math.min(1,Math.max(0,progress)):0;return (1-Math.cos(2*Math.PI*p))/2;}
export function latPulldownFrame(progress:number){
 const phase=latPulldownPhase(progress),barY=config.barTopY-config.barTravel*phase,weightY=.42+config.barTravel*phase;
 return {phase,barY,weightY,leftGrip:[-config.gripHalfWidth,barY-config.gripDrop,config.gripZ] as const,rightGrip:[config.gripHalfWidth,barY-config.gripDrop,config.gripZ] as const};
}
