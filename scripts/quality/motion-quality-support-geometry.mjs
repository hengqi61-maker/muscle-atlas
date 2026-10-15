import {Box3,Vector3,Ray,Triangle} from 'three';
import {EPSILON_M,triangleBox} from './motion-quality-geometry.mjs';
export function supportSolids(cfg){
 const supports=cfg.supports;if(!supports)throw Error('Missing production config.supports; no legacy geometry fallback');
 const vector=(v,label)=>{if(!Array.isArray(v)||v.length!==3||!v.every(Number.isFinite))throw Error('Invalid '+label);return new Vector3(...v)};
 const boxes=['seat','thighPad','pedestal','footPlatform'].map(id=>{const s=supports[id];if(!s)throw Error('Missing supports.'+id);const center=vector(s.position,id+'.position'),size=vector(s.size,id+'.size');if(size.toArray().some(x=>x<=0))throw Error('Nonpositive box size '+id);const half=size.multiplyScalar(.5),box=new Box3(center.clone().sub(half),center.clone().add(half));return {id,type:'box',configPath:'supports.'+id,definition:s,box,broadBox:box,innerBox:new Box3(box.min.clone().addScalar(EPSILON_M),box.max.clone().addScalar(-EPSILON_M))}});
 const cylinders=[{...supports.crossbar,id:'crossbar',path:'supports.crossbar'},...(supports.brackets??[]).map((s,i)=>({...s,id:s.name??'bracket'+i,path:'supports.brackets.'+i}))].map(s=>{const from=vector(s.from,s.id+'.from'),to=vector(s.to,s.id+'.to'),axis=to.clone().sub(from),length=axis.length();if(!(length>0&&s.radius>EPSILON_M&&Number.isFinite(s.radius)))throw Error('Invalid cylinder '+s.id);axis.divideScalar(length);const extent=new Vector3(...axis.toArray().map(x=>s.radius*Math.sqrt(Math.max(0,1-x*x))));return {id:s.id,type:'cylinder',configPath:s.path,definition:{from:s.from,to:s.to,radius:s.radius},from,to,axis,length,radius:s.radius,broadBox:new Box3(from.clone().min(to).sub(extent),from.clone().max(to).add(extent))}});
 return [...boxes,...cylinders];
}
export function cylinderDepth(point,cylinder){const v=point.clone().sub(cylinder.from),z=v.dot(cylinder.axis),radial=v.addScaledVector(cylinder.axis,-z).length();return Math.min(z,cylinder.length-z,cylinder.radius-radial)}
export function cylinderSegmentInterior(a,b,cylinder){
 const p=a.clone().sub(cylinder.from),d=b.clone().sub(a),z=p.dot(cylinder.axis),dz=d.dot(cylinder.axis),pr=p.clone().addScaledVector(cylinder.axis,-z),dr=d.clone().addScaledVector(cylinder.axis,-dz),A=dr.lengthSq(),B=2*pr.dot(dr),C=pr.lengthSq()-cylinder.radius*cylinder.radius,times=[0,1];
 if(A>1e-24){const disc=B*B-4*A*C;if(disc>=0){times.push((-B-Math.sqrt(disc))/(2*A),(-B+Math.sqrt(disc))/(2*A))}}
 if(Math.abs(dz)>1e-15)times.push(-z/dz,(cylinder.length-z)/dz);
 const sorted=times.filter(t=>t>=0&&t<=1).sort((x,y)=>x-y);for(let i=1;i<sorted.length;i++){const point=a.clone().lerp(b,(sorted[i]+sorted[i-1])/2);if(cylinderDepth(point,cylinder)>EPSILON_M)return true}return false;
}
export function cylinderTriangleInterior(a,b,c,cylinder){
 if([a,b,c].some(p=>cylinderDepth(p,cylinder)>EPSILON_M))return true;
 if([[a,b],[b,c],[c,a]].some(([u,v])=>cylinderSegmentInterior(u,v,cylinder)))return true;
 const point=new Ray(cylinder.from,cylinder.axis).intersectTriangle(a,b,c,false,new Vector3());return !!point&&cylinderDepth(point,cylinder)>EPSILON_M;
}
export function inspectSupport(points,triangles,solid){
 let interiorVertices=0,triangleCandidates=0,confirmedInteriorTriangles=0,maxVertexDepth_m=0;
 for(const point of points){const depth=solid.type==='cylinder'?cylinderDepth(point,solid):Math.min(...point.toArray().map((v,i)=>Math.min(v-solid.box.min.getComponent(i),solid.box.max.getComponent(i)-v)));if(depth>EPSILON_M){interiorVertices++;maxVertexDepth_m=Math.max(maxVertexDepth_m,depth)}}
 for(const [ia,ib,ic]of triangles){const a=points[ia],b=points[ib],c=points[ic];if(!triangleBox(a,b,c,solid.broadBox))continue;triangleCandidates++;if(solid.type==='box'?triangleBox(a,b,c,solid.innerBox):cylinderTriangleInterior(a,b,c,solid))confirmedInteriorTriangles++}
 return {interiorVertices,triangleCandidates,confirmedInteriorTriangles,maxVertexDepth_m,status:interiorVertices||confirmedInteriorTriangles?'AUTO FAIL':'INCONCLUSIVE'};
}
export function supportFaceGap(points,solid,face){
 if(solid.type!=='box')throw Error('Face gap requires box');const samples=[];for(const p of points)if(p.x>=solid.box.min.x&&p.x<=solid.box.max.x&&p.z>=solid.box.min.z&&p.z<=solid.box.max.z)samples.push(face==='top'?p.y-solid.box.max.y:solid.box.min.y-p.y);
 return {face,sampledVerticesOverFootprint:samples.length,minSignedGap_m:samples.length?Math.min(...samples):null,minAbsoluteGap_m:samples.length?Math.min(...samples.map(Math.abs)):null,status:'INCONCLUSIVE',meaning:'Positive means outside support face; nearest source-muscle/tendon vertex only. A positive gap is not contact, and zero does not establish skin contact or load support.'};
}
export function clippedSupportFaceGap(points,triangles,solid,face){
 const samples=[];let contributingTriangles=0;
 for(const triangle of triangles){let polygon=triangle.map(i=>points[i]);for(const [axis,bound,greater]of [['x',solid.box.min.x,true],['x',solid.box.max.x,false],['z',solid.box.min.z,true],['z',solid.box.max.z,false]]){if(!polygon.length)break;const next=[];for(let i=0;i<polygon.length;i++){const a=polygon[i],b=polygon[(i+1)%polygon.length],insideA=greater?a[axis]>=bound:a[axis]<=bound,insideB=greater?b[axis]>=bound:b[axis]<=bound;if(insideA)next.push(a);if(insideA!==insideB)next.push(a.clone().lerp(b,(bound-a[axis])/(b[axis]-a[axis])))}polygon=next}
  if(polygon.length){contributingTriangles++;for(const p of polygon)samples.push(face==='top'?p.y-solid.box.max.y:solid.box.min.y-p.y)}
 }
 return {face,contributingTriangles,clippedPolygonVertices:samples.length,minSignedGap_m:samples.length?Math.min(...samples):null,minAbsoluteBoundaryVertexGap_m:samples.length?Math.min(...samples.map(Math.abs)):null,status:'INCONCLUSIVE',method:'Actual source triangle polygons clipped to production support XZ footprint, then signed vertical face gap. Extremum is exact for piecewise-linear triangles; absolute minimum is boundary-vertex diagnostic and not a full triangle/solid closest distance. Positive gap is geometric separation, not contact or skin/load support.'};
}
export function connectionWitness(a,b){
 if(a.type==='box'&&b.type==='box')return a.box.intersectsBox(b.box)?{method:'Exact box/box intersection'}:null;
 if(a.type==='box')return connectionWitness(b,a);
 if(b.type==='box'){
  for(const endpoint of [a.from,a.to]){const closest=b.box.clampPoint(endpoint,new Vector3()),delta=closest.clone().sub(endpoint);if(b.box.containsPoint(endpoint)||Math.abs(delta.dot(a.axis))<=EPSILON_M&&delta.length()<=a.radius)return {method:'Cylinder endpoint/cap disk contains point in box',point_m:closest.toArray()}}
  const middle=a.from.clone().lerp(a.to,.5),radialWitness=b.box.clampPoint(middle,new Vector3());if(cylinderDepth(radialWitness,a)>=-EPSILON_M)return {method:'Box point lies on/in finite cylinder within unchanged precision tolerance',point_m:radialWitness.toArray()};
  const point=new Ray(a.from,a.axis).intersectBox(b.box,new Vector3());if(point&&point.clone().sub(a.from).dot(a.axis)<=a.length)return {method:'Cylinder axis segment intersects box',point_m:point.toArray()};return null;
 }
 for(const endpoint of [a.from,a.to])if(cylinderDepth(endpoint,b)>=0)return {method:'Cylinder endpoint lies within other finite cylinder',point_m:endpoint.toArray()};
 for(const endpoint of [b.from,b.to])if(cylinderDepth(endpoint,a)>=0)return {method:'Cylinder endpoint lies within other finite cylinder',point_m:endpoint.toArray()};return null;
}
export function supportConnections(solids){
 const witnesses=[];for(let i=0;i<solids.length;i++)for(let j=i+1;j<solids.length;j++){const witness=connectionWitness(solids[i],solids[j]);if(witness)witnesses.push({solidIds:[solids[i].id,solids[j].id],...witness})}
 const reached=new Set(['pedestal']);for(let i=0;i<solids.length;i++)for(const {solidIds:[a,b]}of witnesses)if(reached.has(a)||reached.has(b)){reached.add(a);reached.add(b)}
 return {witnesses,connectedToPedestal:[...reached],noWitnessPathToPedestal:solids.filter(s=>!reached.has(s.id)).map(s=>s.id),status:'INCONCLUSIVE',limits:'Exact geometric witness graph only; absence of a witness is not proof of disconnection. No strength, welding, floor anchorage or physical load support validation.'};
}
