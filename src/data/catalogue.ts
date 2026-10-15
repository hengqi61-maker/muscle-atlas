import raw from './mesh_mapping.json';
import {PropertyBinding} from 'three';
export interface MeshEntry {name:string;originalName:string;fmaId:string;bpId:string;source:string;isTendon:boolean;anatomyId:string;meshName:string;}
export const catalogue:MeshEntry[]=raw.map(r=>({...r,anatomyId:`${r.source}:${r.bpId||r.fmaId||"unmapped"}:${PropertyBinding.sanitizeNodeName(r.name)}`,meshName:PropertyBinding.sanitizeNodeName(r.name)}));
export const byMesh=new Map(catalogue.map(r=>[r.meshName,r]));
export const byId=new Map(catalogue.map(r=>[r.anatomyId,r]));
