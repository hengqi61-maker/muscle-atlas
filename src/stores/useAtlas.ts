import {create} from 'zustand';
export type Mode='explore'|'exercise'|'training';
interface State {mode:Mode;style:'real'|'clean';selected:string|null;hovered:string|null;playing:boolean;loop:boolean;speed:number;time:number;hidden:string[];reset:number;model:'anatomy'|'rigged';focus:'full'|'arm';morphMode:'baked'|'manual';morphWeight:number; set:(patch:Partial<State>)=>void;}
export const useAtlas=create<State>(set=>({mode:'explore',style:'clean',selected:null,hovered:null,playing:false,loop:true,speed:1,time:0,hidden:[],reset:0,model:'anatomy',focus:'full',morphMode:'baked',morphWeight:0,set:patch=>set(patch)}));
