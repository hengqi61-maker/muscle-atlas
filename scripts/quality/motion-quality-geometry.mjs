import {Vector3, Box3, Triangle} from 'three';
export const EPSILON_M = 1e-6;
export function triangleBox(a,b,c,box) { return box.intersectsTriangle(new Triangle(a,b,c)); }
export function triangles(geometry) {
 const ix=geometry.index, n=ix?ix.count:geometry.attributes.position.count, out=[];
 for(let i=0;i+2<n;i+=3)out.push([ix?ix.getX(i):i,ix?ix.getX(i+1):i+1,ix?ix.getX(i+2):i+2]);
 return out;
}
export function topology(geometry) {
 const n=geometry.attributes.position.count, p=Array.from({length:n},(_,i)=>i), root=x=>{while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x};
 for(const [a,b,c] of triangles(geometry)){p[root(a)]=root(b);p[root(b)]=root(c)}
 return {indexConnectedComponents:new Set(p.map((_,i)=>root(i))).size, note:'Index connectivity; duplicated seam vertices and anatomically separate bundles can increase count. Count is evidence, never automatic failure.'};
}
export function area(a,b,c){return new Vector3().subVectors(b,a).cross(new Vector3().subVectors(c,a)).length()/2}
export function vertices(mesh){return Array.from({length:mesh.geometry.attributes.position.count},(_,i)=>mesh.localToWorld(mesh.getVertexPosition(i,new Vector3())))}
export function bounds(points){const box=new Box3();for(const p of points)box.expandByPoint(p);return {min:box.min.toArray(),max:box.max.toArray()}}
export function surfaceContact(points, x, y, z, radius=.019){
 let min=Infinity, nearest=null;
 for(let i=0;i<points.length;i++){const p=points[i], dx=Math.max(Math.abs(p.x)-Math.abs(x),0), gap=Math.abs(Math.hypot(dx,p.y-y,p.z-z)-radius);if(gap<min){min=gap;nearest=i}}
 return {nearestVertexRadialGap_m:min,nearestVertex:nearest,method:'Actual source vertices to finite handle capsule surface; unsigned nearest-vertex distance. No palm/thumb labels; no triangle closest point or contact force. Cannot prove grasp.'};
}
export function severeCollapse(collapsed,eligible){return collapsed>3||collapsed>.01*eligible}
