import {create} from 'zustand';
export type Mode='explore'|'exercise'|'training';
interface State {motionVersion:'original'|'unified'|'e03';mode:Mode;exerciseId:'dumbbell-curl'|'lat-pulldown';style:'real'|'clean';selected:string|null;hovered:string|null;playing:boolean;loop:boolean;speed:number;time:number;hidden:string[];reset:number;model:'anatomy'|'rigged'|'pulldown';focus:'full'|'arm'|'grip'|'back'|'side';morphMode:'baked'|'manual';morphWeight:number; set:(patch:Partial<State>)=>void;}
export const useAtlas=create<State>(set=>({motionVersion:'original',mode:'explore',exerciseId:'dumbbell-curl',style:'clean',selected:null,hovered:null,playing:false,loop:true,speed:1,time:0,hidden:[],reset:0,model:'anatomy',focus:'full',morphMode:'baked',morphWeight:0,set:patch=>set(patch)}));
