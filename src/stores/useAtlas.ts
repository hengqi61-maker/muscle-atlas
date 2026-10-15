import {create} from 'zustand';
export type Mode='explore'|'exercise'|'training';
interface State {mode:Mode;exerciseId:'dumbbell-curl'|'lat-pulldown';style:'real'|'clean';selected:string|null;hovered:string|null;playing:boolean;loop:boolean;speed:number;time:number;hidden:string[];reset:number;model:'anatomy'|'prototype'; set:(patch:Partial<State>)=>void;}
export const useAtlas=create<State>(set=>({mode:'explore',exerciseId:'dumbbell-curl',style:'clean',selected:null,hovered:null,playing:false,loop:true,speed:1,time:0,hidden:[],reset:0,model:'anatomy',set:patch=>set(patch)}));
