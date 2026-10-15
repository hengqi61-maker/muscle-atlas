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
export function indexedComponents(geometry){
 const n=geometry.attributes.position.count,parent=Array.from({length:n},(_,i)=>i);
 const root=i=>{while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i};
 for(const [a,b,c] of triangles(geometry)){parent[root(a)]=root(b);parent[root(b)]=root(c)}
 const groups=new Map();for(let i=0;i<n;i++){const r=root(i);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(i)}return [...groups.values()];
}
export function centroid(points){return points.reduce((sum,p)=>sum.add(p),new Vector3()).divideScalar(points.length)}
export function localizeComponents(points,components,bones,expectedBones){
 return components.map((indices,component)=>{const p=indices.map(i=>points[i]),center=centroid(p);const distances=Object.entries(bones).map(([name,xyz])=>({name,distance_m:center.distanceTo(new Vector3(...xyz))})).sort((a,b)=>a.distance_m-b.distance_m);const expected=distances.filter(d=>expectedBones.includes(d.name));return {component,indexVertexCount:indices.length,centroid_m:center.toArray(),bounds_m:bounds(p),nearestJoint:distances[0],expectedJointDistances:expected,spatialFlag:expected.length&& !expectedBones.includes(distances[0].name)?(/Hand/.test(distances[0].name)?'NEARER_OPPOSITE_HAND_JOINT':'NEARER_NON_HAND_JOINT'):'NO_NEAREST_JOINT_FLAG',verdict:'INCONCLUSIVE',method:'Actual index-connected component centroid to joint origins; relative localization only. Tendons/bundles may span multiple regions; no medical cutoff and no automatic wrong-anatomy verdict.'}});
}
export function boxContact(points,tri,box){
 let interiorVertices=0,intersectingTriangles=0;for(const p of points)if(box.containsPoint(p)&&Math.min(...p.toArray().map((v,a)=>Math.min(v-box.min.getComponent(a),box.max.getComponent(a)-v)))>EPSILON_M)interiorVertices++;
 for(const [a,b,c]of tri)if(triangleBox(points[a],points[b],points[c],box))intersectingTriangles++;
 return {interiorVertices,intersectingTriangles};
}
