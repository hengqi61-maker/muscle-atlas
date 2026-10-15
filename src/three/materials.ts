export type VisualState='default'|'hovered'|'selected'|'related-primary'|'related-secondary'|'related-stabilizer'|'dimmed'|'hidden'|'heatmap';
export function resolveState(id:string,selected:string|null,hovered:string|null,hidden:string[],role?:string):VisualState {
 if(hidden.includes(id))return 'hidden';if(selected===id)return 'selected';if(hovered===id)return 'hovered';if(role)return `related-${role}` as VisualState;return selected?'dimmed':'default';
}
export function appearance(state:VisualState,style:'real'|'clean',heat=0){
 const colors:Record<VisualState,string>={default:style==='real'?'#943a3f':'#9aabb8',hovered:'#f5cf94',selected:'#66b5ff','related-primary':'#56e0bd','related-secondary':'#e6b56a','related-stabilizer':'#8e9dea',dimmed:style==='real'?'#512d36':'#53606c',hidden:'#000000',heatmap:`hsl(${160-heat*140},65%,55%)`};
 return {color:colors[state],roughness:style==='real'?.65:.38,metalness:style==='real'?.02:.15,transparent:state==='dimmed',opacity:state==='dimmed'?.28:1,visible:state!=='hidden'};
}
